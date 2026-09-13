"""Deterministic GNSS-mask replay harness for offline/SITL preparation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from gcf_rescue_v02 import GcfRescueV02, GnssState, RescueConfig, SensorSnapshot, Vec2
from route_planner import GeofenceRoutePlanner, NavigationIntent


@dataclass(frozen=True)
class ReplayRecord:
    t_s: float
    gnss: GnssState
    actual_xy_m: Vec2
    decision_action: str
    navigation_intent: NavigationIntent
    uncertainty_m: float


def synthetic_gnss_mask_replay() -> list[ReplayRecord]:
    """A deterministic scenario: anchor, GNSS loss, rescue, then containment.

    This validates decision-flow behavior only. It is not a flight-accuracy claim.
    """
    cfg = RescueConfig(target_xy_m=Vec2(90, 10), safe_xy_m=Vec2(10, 10),
                       max_update_gap_s=2.0, containment_s=12.0,
                       hard_timeout_s=25.0, rescue_init_s=3.0)
    core = GcfRescueV02(cfg)
    grid = GeofenceRoutePlanner.from_demo_map()
    records = []
    for t in range(0, 20):
        actual = Vec2(10 + t * 3.0, 10.0)
        gnss = GnssState.STABLE if t < 3 else GnssState.LOST
        observed = actual if gnss is GnssState.STABLE else None
        s = SensorSnapshot(t, gnss, Vec2(3.0, 0.0), 10.0, observed,
                           gnss_quality=1.0 if observed else 0.0,
                           velocity_quality=0.8, visual_quality=1.0,
                           optical_flow_quality=1.0, obstacle_risk=0.0,
                           link_alive=True, battery_ratio=0.9)
        d = core.update(s)
        intent = grid.translate(d)
        records.append(ReplayRecord(t, gnss, actual, d.action.value, intent, d.uncertainty_sigma_m))
    return records


def _demo_map() -> "GridMap":
    from route_planner import GridMap
    # A small rectangular no-go block that forces a non-straight planned route.
    blocked = frozenset((x, 0) for x in range(4, 7))
    return GridMap(120, 40, 10, blocked)


# Kept here so the harness creates a reproducible map without external files.
GeofenceRoutePlanner.from_demo_map = staticmethod(lambda: GeofenceRoutePlanner(_demo_map()))
