"""Bidirectional GCF route-frame ↔ ArduPilot EKF local-NED conversion.

No global latitude/longitude is produced or consumed here.  The adapter only
works after a route frame has been explicitly aligned to ArduPilot's local-NED
EKF frame while navigation is trusted.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import cos, isfinite, sin
from typing import Optional

from gcf_rescue_v02 import GnssState, SensorSnapshot, Vec2


@dataclass(frozen=True)
class LocalNed:
    north_m: float
    east_m: float
    down_m: float


@dataclass(frozen=True)
class LocalNedVelocity:
    north_mps: float
    east_mps: float
    down_mps: float


@dataclass(frozen=True)
class RouteFrameAlignment:
    """Fixed transform from GCF route coordinates into ArduPilot local NED.

    `route_to_ned_yaw_rad` is the angle from route +X to NED North.  This is
    established only while the frame is trusted; it must not be re-anchored
    from a degraded/lost GNSS measurement.
    """
    route_origin_ned: LocalNed
    route_to_ned_yaw_rad: float
    locked_at_t_s: float
    source: str = "pre_loss_trusted_alignment"

    def route_to_ned(self, route_xy: Vec2, route_alt_up_m: float) -> LocalNed:
        c, s = cos(self.route_to_ned_yaw_rad), sin(self.route_to_ned_yaw_rad)
        return LocalNed(
            self.route_origin_ned.north_m + c * route_xy.x - s * route_xy.y,
            self.route_origin_ned.east_m + s * route_xy.x + c * route_xy.y,
            self.route_origin_ned.down_m - route_alt_up_m,
        )

    def ned_to_route(self, ned: LocalNed) -> tuple[Vec2, float]:
        dn = ned.north_m - self.route_origin_ned.north_m
        de = ned.east_m - self.route_origin_ned.east_m
        c, s = cos(self.route_to_ned_yaw_rad), sin(self.route_to_ned_yaw_rad)
        # inverse rotation maps NED North/East back into route X/Y
        return Vec2(c * dn + s * de, -s * dn + c * de), self.route_origin_ned.down_m - ned.down_m

    def ned_velocity_to_route(self, v: LocalNedVelocity) -> Vec2:
        c, s = cos(self.route_to_ned_yaw_rad), sin(self.route_to_ned_yaw_rad)
        return Vec2(c * v.north_mps + s * v.east_mps,
                    -s * v.north_mps + c * v.east_mps)


@dataclass(frozen=True)
class ArduPilotLocalTelemetry:
    """Normalized values sourced by an ArduPilot/MAVLink telemetry reader.

    The reader must derive `local_position_valid` and `gnss_state` from real
    EKF/GNSS health messages; this class deliberately does not infer them from
    the coordinate values themselves.
    """
    t_s: float
    position_ned: LocalNed
    velocity_ned: LocalNedVelocity
    local_position_valid: bool
    gnss_state: GnssState
    gnss_quality: float
    velocity_quality: float
    baro_alt_up_m: float
    visual_quality: float
    optical_flow_quality: float
    obstacle_risk: float
    link_alive: bool
    battery_ratio: float
    ekf_source: str


class ArduPilotTelemetryAdapter:
    """Converts trustworthy ArduPilot local-NED telemetry into GCF input."""
    def __init__(self, alignment: RouteFrameAlignment, allowed_sources: frozenset[str]):
        self.alignment = alignment
        self.allowed_sources = allowed_sources

    @staticmethod
    def _check_finite(*values: float) -> None:
        if not all(isfinite(v) for v in values):
            raise ValueError("non-finite local-NED telemetry")

    def to_sensor_snapshot(self, t: ArduPilotLocalTelemetry) -> SensorSnapshot:
        self._check_finite(t.t_s, t.position_ned.north_m, t.position_ned.east_m,
                           t.position_ned.down_m, t.velocity_ned.north_mps,
                           t.velocity_ned.east_mps, t.baro_alt_up_m)
        if t.ekf_source not in self.allowed_sources:
            raise ValueError("unapproved EKF navigation source")
        route_xy, _ = self.alignment.ned_to_route(t.position_ned)
        route_velocity = self.alignment.ned_velocity_to_route(t.velocity_ned)
        # A stable route position is supplied only when GNSS itself is trusted.
        # During GNSS loss GCF propagates from its last trusted anchor; local-NED
        # remains an independent validity gate for the ArduPilot command adapter.
        position_for_gnss = route_xy if t.gnss_state is GnssState.STABLE else None
        return SensorSnapshot(
            t_s=t.t_s, gnss=t.gnss_state, velocity_route_mps=route_velocity,
            baro_alt_m=t.baro_alt_up_m, route_xy_m=position_for_gnss,
            gnss_quality=t.gnss_quality, velocity_quality=t.velocity_quality,
            visual_quality=t.visual_quality, optical_flow_quality=t.optical_flow_quality,
            obstacle_risk=t.obstacle_risk, link_alive=t.link_alive,
            battery_ratio=t.battery_ratio,
        )


def validate_alignment(a: RouteFrameAlignment) -> None:
    values = (a.route_origin_ned.north_m, a.route_origin_ned.east_m,
              a.route_origin_ned.down_m, a.route_to_ned_yaw_rad, a.locked_at_t_s)
    if not all(isfinite(v) for v in values):
        raise ValueError("invalid route/local-NED alignment")
    if a.source != "pre_loss_trusted_alignment":
        raise ValueError("alignment must be created before GNSS degradation")
