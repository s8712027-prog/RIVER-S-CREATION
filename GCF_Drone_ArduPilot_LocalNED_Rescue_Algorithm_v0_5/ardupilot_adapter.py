"""ArduCopter Guided-mode adapter for GCF high-level navigation intent.

The adapter creates MAVLink-shaped *requests* for SITL/HITL validation.  It
does not open a serial/UDP link and it cannot emit motor, attitude, rate, or
fake-GPS messages.  Production transport is intentionally out of scope.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import cos, sin
from typing import Optional

from route_planner import NavigationIntent
from gcf_rescue_v02 import Action, Vec2


MAV_FRAME_LOCAL_NED = 1
POSITION_ONLY_TYPE_MASK = 3576  # ArduPilot documented position-only mask


class AdapterStatus(str, Enum):
    READY = "ready"
    BLOCKED = "blocked"
    HOLD = "hold"
    FAILSAFE_REQUIRED = "failsafe_required"


@dataclass(frozen=True)
class ArduPilotState:
    mode: str
    armed: bool
    ekf_local_position_valid: bool
    ekf_source: str  # e.g. external_nav, optical_flow, trusted_dead_reckoning
    pilot_override_available: bool


@dataclass(frozen=True)
class RouteFrameToNed:
    """Rigid transform fixed before GNSS loss: route X/Y → EKF local N/E."""
    origin_north_m: float
    origin_east_m: float
    yaw_rad: float = 0.0

    def convert(self, route_xy: Vec2) -> Vec2:
        c, s = cos(self.yaw_rad), sin(self.yaw_rad)
        return Vec2(self.origin_north_m + c * route_xy.x - s * route_xy.y,
                    self.origin_east_m + s * route_xy.x + c * route_xy.y)


@dataclass(frozen=True)
class ArduPilotAdapterConfig:
    frame: RouteFrameToNed
    command_down_m: float
    require_guided_mode: bool = True
    allowed_ekf_sources: frozenset[str] = frozenset({"external_nav", "optical_flow", "trusted_dead_reckoning"})


@dataclass(frozen=True)
class MavlinkRequest:
    request_type: str
    coordinate_frame: Optional[int]
    type_mask: Optional[int]
    north_m: Optional[float]
    east_m: Optional[float]
    down_m: Optional[float]
    reason: str
    source: str = "GCF_HIGH_LEVEL_ROUTE_DECISION"
    not_a_gps_fix: bool = True
    not_low_level_flight_control: bool = True


class ArduPilotGuidedAdapter:
    def __init__(self, cfg: ArduPilotAdapterConfig):
        self.cfg = cfg

    def _position_authority_ready(self, vehicle: ArduPilotState) -> Optional[str]:
        if not vehicle.armed:
            return "vehicle not armed"
        if self.cfg.require_guided_mode and vehicle.mode.upper() != "GUIDED":
            return "ArduPilot not in GUIDED mode"
        if not vehicle.ekf_local_position_valid:
            return "EKF local-NED position invalid"
        if vehicle.ekf_source not in self.cfg.allowed_ekf_sources:
            return "EKF source is not approved for GNSS-denied navigation"
        return None

    def build(self, intent: NavigationIntent, vehicle: ArduPilotState) -> tuple[AdapterStatus, MavlinkRequest]:
        if not intent.not_a_gps_fix or not intent.not_low_level_flight_control:
            return AdapterStatus.BLOCKED, MavlinkRequest("BLOCKED", None, None, None, None, None,
                                                          "GCF authority boundary invalid")

        if intent.action is Action.LAND_MANUAL:
            # The adapter intentionally does not command LAND: vehicle-native failsafes
            # and a human operator remain responsible when no positioning authority exists.
            return AdapterStatus.FAILSAFE_REQUIRED, MavlinkRequest(
                "REQUEST_OPERATOR_OR_ARDUPILOT_FAILSAFE", None, None, None, None, None, intent.reason)
        if intent.action is Action.HOLD:
            return AdapterStatus.HOLD, MavlinkRequest(
                "REQUEST_GUIDED_HOLD", None, None, None, None, None, intent.reason)

        not_ready = self._position_authority_ready(vehicle)
        if not_ready:
            return AdapterStatus.BLOCKED, MavlinkRequest("BLOCKED", None, None, None, None, None, not_ready)
        if intent.waypoint_xy_m is None:
            return AdapterStatus.BLOCKED, MavlinkRequest("BLOCKED", None, None, None, None, None,
                                                          "missing high-level waypoint")

        ned = self.cfg.frame.convert(intent.waypoint_xy_m)
        return AdapterStatus.READY, MavlinkRequest(
            request_type="SET_POSITION_TARGET_LOCAL_NED",
            coordinate_frame=MAV_FRAME_LOCAL_NED,
            type_mask=POSITION_ONLY_TYPE_MASK,
            north_m=ned.x, east_m=ned.y, down_m=self.cfg.command_down_m,
            reason=intent.reason,
        )


def validate_mavlink_request(r: MavlinkRequest) -> None:
    if not r.not_a_gps_fix or not r.not_low_level_flight_control:
        raise ValueError("authority-boundary breach")
    if r.request_type == "SET_POSITION_TARGET_LOCAL_NED":
        if (r.coordinate_frame, r.type_mask) != (MAV_FRAME_LOCAL_NED, POSITION_ONLY_TYPE_MASK):
            raise ValueError("unexpected ArduPilot Guided setpoint")
        if None in (r.north_m, r.east_m, r.down_m):
            raise ValueError("incomplete position request")
