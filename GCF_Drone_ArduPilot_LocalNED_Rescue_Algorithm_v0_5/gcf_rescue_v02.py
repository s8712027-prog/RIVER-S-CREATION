"""GCF-Drone v0.2: GNSS-denied high-level rescue-navigation reference core.

Safety boundary: returns only high-level navigation intent. This module never
creates GPS measurements, attitude/rate setpoints, motor commands, or actuator
commands. A certified flight-controller adapter must preserve geofence,
failsafe, collision-avoidance, and pilot-override authority.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from math import hypot, isfinite, sqrt
from typing import Optional


class GnssState(str, Enum):
    STABLE = "stable"
    DEGRADED = "degraded"
    LOST = "lost"


class NavState(str, Enum):
    NO_ANCHOR = "no_anchor"
    NORMAL = "normal"
    CAUTIOUS = "cautious"
    RESCUE_INIT = "rescue_init"
    RESCUE_GUIDANCE = "rescue_guidance"
    CONTAINMENT = "containment"
    RECOVERY_VERIFY = "recovery_verify"
    ABORT = "abort"


class Action(str, Enum):
    PROCEED = "proceed_route"
    SLOW = "slow_route"
    HOLD = "hold_reobserve"
    REPLAN = "replan_to_target"
    RETURN_SAFE = "return_to_safe_zone"
    LAND_MANUAL = "land_or_manual"


@dataclass(frozen=True)
class Vec2:
    x: float
    y: float

    def advance(self, vx: float, vy: float, dt: float) -> "Vec2":
        return Vec2(self.x + vx * dt, self.y + vy * dt)


@dataclass(frozen=True)
class SensorSnapshot:
    """Inputs must be time-aligned by the platform-specific telemetry adapter.

    route_xy_m is mandatory only when gnss=STABLE. It is expressed in one
    mission-local route frame, not latitude/longitude and not fake GPS.
    """
    t_s: float
    gnss: GnssState
    velocity_route_mps: Vec2
    baro_alt_m: float
    route_xy_m: Optional[Vec2] = None
    gnss_quality: float = 0.0
    velocity_quality: float = 0.0
    visual_quality: float = 0.0
    optical_flow_quality: float = 0.0
    obstacle_risk: float = 0.0
    link_alive: bool = True
    battery_ratio: float = 1.0


@dataclass(frozen=True)
class RescueConfig:
    target_xy_m: Vec2
    safe_xy_m: Vec2
    corridor_half_width_m: float = 20.0
    normal_speed_mps: float = 8.0
    cautious_speed_mps: float = 3.0
    rescue_speed_mps: float = 2.0
    rescue_init_s: float = 5.0
    containment_s: float = 45.0
    hard_timeout_s: float = 90.0
    containment_sigma_m: float = 40.0
    abort_sigma_m: float = 80.0
    initial_sigma_m: float = 3.0
    velocity_noise_mps: float = 0.45
    min_gnss_quality: float = 0.70
    min_velocity_quality: float = 0.35
    min_battery_ratio: float = 0.18
    max_obstacle_risk: float = 0.80
    vision_enabled: bool = True
    optical_flow_enabled: bool = True
    min_perception_quality: float = 0.15
    recovery_confirmations: int = 3
    recovery_sample_delta_m: float = 8.0
    max_update_gap_s: float = 1.0


@dataclass
class Estimate:
    xy_m: Optional[Vec2] = None
    altitude_m: Optional[float] = None
    sigma_m: float = 3.0
    last_t_s: Optional[float] = None
    last_good_gnss_t_s: Optional[float] = None
    recovery_candidate_xy_m: Optional[Vec2] = None
    recovery_count: int = 0


@dataclass(frozen=True)
class DecisionPacket:
    packet_type: str
    t_s: float
    nav_state: NavState
    action: Action
    target_xy_m: Vec2
    estimated_xy_m: Optional[Vec2]
    uncertainty_sigma_m: float
    desired_ground_speed_mps: float
    corridor_half_width_m: float
    gnss: GnssState
    link_alive: bool
    reason: str
    authority: str = "GCF_HIGH_LEVEL_ROUTE_DECISION"
    not_a_gps_fix: bool = True
    not_low_level_flight_control: bool = True

    def to_dict(self) -> dict:
        return asdict(self)


class GcfRescueV02:
    def __init__(self, cfg: RescueConfig):
        self.cfg = cfg
        self.est = Estimate(sigma_m=cfg.initial_sigma_m)
        self.was_lost = False

    @staticmethod
    def _finite(v: float) -> bool:
        return isfinite(v)

    def _validate(self, s: SensorSnapshot) -> None:
        values = (s.t_s, s.velocity_route_mps.x, s.velocity_route_mps.y,
                  s.baro_alt_m, s.gnss_quality, s.velocity_quality,
                  s.visual_quality, s.optical_flow_quality, s.obstacle_risk,
                  s.battery_ratio)
        if not all(self._finite(v) for v in values):
            raise ValueError("non-finite telemetry")
        if not all(0.0 <= v <= 1.0 for v in values[4:]):
            raise ValueError("telemetry quality outside [0, 1]")
        if s.gnss is GnssState.STABLE and s.route_xy_m is None:
            raise ValueError("stable GNSS requires a route-frame position")

    def _perception_usable(self, s: SensorSnapshot) -> bool:
        qualities = []
        if self.cfg.vision_enabled:
            qualities.append(s.visual_quality)
        if self.cfg.optical_flow_enabled:
            qualities.append(s.optical_flow_quality)
        # A platform with neither modality must use a separate obstacle adapter;
        # it is not treated as a failed camera by default.
        return not qualities or max(qualities) >= self.cfg.min_perception_quality

    def _propagate(self, s: SensorSnapshot, dt: float) -> None:
        if self.est.xy_m is None:
            return
        self.est.xy_m = self.est.xy_m.advance(s.velocity_route_mps.x,
                                              s.velocity_route_mps.y, dt)
        self.est.altitude_m = s.baro_alt_m
        quality_penalty = 1.0 + (1.0 - s.velocity_quality) * 2.0
        growth = self.cfg.velocity_noise_mps * quality_penalty * dt
        self.est.sigma_m = hypot(self.est.sigma_m, growth)

    def _accept_gnss_anchor(self, s: SensorSnapshot) -> None:
        assert s.route_xy_m is not None
        self.est.xy_m = s.route_xy_m
        self.est.altitude_m = s.baro_alt_m
        self.est.sigma_m = self.cfg.initial_sigma_m
        self.est.last_good_gnss_t_s = s.t_s
        self.est.recovery_candidate_xy_m = None
        self.est.recovery_count = 0
        self.was_lost = False

    def _confirm_recovery(self, s: SensorSnapshot) -> bool:
        assert s.route_xy_m is not None
        c = self.est.recovery_candidate_xy_m
        if c is None or hypot(s.route_xy_m.x - c.x, s.route_xy_m.y - c.y) > self.cfg.recovery_sample_delta_m:
            self.est.recovery_candidate_xy_m = s.route_xy_m
            self.est.recovery_count = 1
        else:
            self.est.recovery_count += 1
            self.est.recovery_candidate_xy_m = s.route_xy_m
        return self.est.recovery_count >= self.cfg.recovery_confirmations

    def _gap_s(self, now_s: float) -> float:
        if self.est.last_good_gnss_t_s is None:
            return float("inf")
        return max(0.0, now_s - self.est.last_good_gnss_t_s)

    def _packet(self, s: SensorSnapshot, state: NavState, action: Action,
                target: Vec2, speed: float, reason: str) -> DecisionPacket:
        return DecisionPacket(
            packet_type="GCF_HIGH_LEVEL_RESCUE_DECISION", t_s=s.t_s,
            nav_state=state, action=action, target_xy_m=target,
            estimated_xy_m=self.est.xy_m, uncertainty_sigma_m=self.est.sigma_m,
            desired_ground_speed_mps=speed,
            corridor_half_width_m=self.cfg.corridor_half_width_m + self.est.sigma_m,
            gnss=s.gnss, link_alive=s.link_alive, reason=reason,
        )

    def update(self, s: SensorSnapshot) -> DecisionPacket:
        self._validate(s)
        dt = 0.0 if self.est.last_t_s is None else s.t_s - self.est.last_t_s
        if dt < 0:
            raise ValueError("out-of-order telemetry")
        self.est.last_t_s = s.t_s
        if dt > self.cfg.max_update_gap_s:
            return self._packet(s, NavState.ABORT, Action.LAND_MANUAL,
                                self.cfg.safe_xy_m, 0.0, "telemetry stale")
        self._propagate(s, dt)

        if s.battery_ratio < self.cfg.min_battery_ratio:
            return self._packet(s, NavState.ABORT, Action.LAND_MANUAL,
                                self.cfg.safe_xy_m, 0.0, "battery floor")
        if not self._perception_usable(s) or s.obstacle_risk >= self.cfg.max_obstacle_risk:
            return self._packet(s, NavState.CAUTIOUS, Action.HOLD,
                                self.cfg.safe_xy_m, 0.0, "perception safety floor")

        if s.gnss is GnssState.STABLE and s.gnss_quality >= self.cfg.min_gnss_quality:
            if self.was_lost:
                if not self._confirm_recovery(s):
                    return self._packet(s, NavState.RECOVERY_VERIFY, Action.HOLD,
                                        self.cfg.safe_xy_m, 0.0, "verify GNSS recovery")
            self._accept_gnss_anchor(s)
            return self._packet(s, NavState.NORMAL, Action.PROCEED,
                                self.cfg.target_xy_m, self.cfg.normal_speed_mps,
                                "trusted GNSS anchor")

        # Without an anchor, a target vector has no trustworthy coordinate frame.
        if self.est.xy_m is None or self.est.last_good_gnss_t_s is None:
            self.was_lost = True
            return self._packet(s, NavState.NO_ANCHOR, Action.LAND_MANUAL,
                                self.cfg.safe_xy_m, 0.0, "no trusted GNSS anchor")

        self.was_lost = True
        gap = self._gap_s(s.t_s)
        if gap >= self.cfg.hard_timeout_s or self.est.sigma_m >= self.cfg.abort_sigma_m:
            return self._packet(s, NavState.ABORT, Action.LAND_MANUAL,
                                self.cfg.safe_xy_m, 0.0, "time/uncertainty abort floor")
        if gap >= self.cfg.containment_s or self.est.sigma_m >= self.cfg.containment_sigma_m:
            return self._packet(s, NavState.CONTAINMENT, Action.RETURN_SAFE,
                                self.cfg.safe_xy_m, self.cfg.rescue_speed_mps,
                                "long gap or uncertainty containment")
        if s.gnss is GnssState.DEGRADED:
            return self._packet(s, NavState.CAUTIOUS, Action.SLOW,
                                self.cfg.target_xy_m, self.cfg.cautious_speed_mps,
                                "GNSS degraded")
        if gap < self.cfg.rescue_init_s:
            return self._packet(s, NavState.RESCUE_INIT, Action.HOLD,
                                self.cfg.safe_xy_m, 0.0, "stabilize rescue estimate")
        return self._packet(s, NavState.RESCUE_GUIDANCE, Action.REPLAN,
                            self.cfg.target_xy_m, self.cfg.rescue_speed_mps,
                            "route-relative rescue guidance")


def validate_for_flight_controller_adapter(packet: DecisionPacket) -> None:
    """Mandatory adapter gate. Rejects packets that cross the authority boundary."""
    if packet.packet_type != "GCF_HIGH_LEVEL_RESCUE_DECISION":
        raise ValueError("unexpected packet type")
    if not packet.not_a_gps_fix or not packet.not_low_level_flight_control:
        raise ValueError("unsafe authority boundary")
    if packet.desired_ground_speed_mps < 0 or packet.corridor_half_width_m <= 0:
        raise ValueError("invalid navigation intent")
