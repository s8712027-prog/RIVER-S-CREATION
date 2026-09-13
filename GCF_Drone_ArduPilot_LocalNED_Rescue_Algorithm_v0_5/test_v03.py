import unittest

from gcf_rescue_v02 import Action, GcfRescueV02, GnssState, RescueConfig, SensorSnapshot, Vec2
from replay_harness import synthetic_gnss_mask_replay
from route_planner import GeofenceRoutePlanner, GridMap, validate_intent


class V03Tests(unittest.TestCase):
    def test_planner_avoids_no_go_cells(self):
        grid = GridMap(50, 50, 10, frozenset({(2, 1), (2, 2), (2, 3)}))
        route = GeofenceRoutePlanner(grid).plan(Vec2(5, 15), Vec2(45, 15))
        self.assertIsNotNone(route)
        self.assertFalse(any(c in grid.blocked for c in route))

    def test_rescue_decision_becomes_high_level_route_intent(self):
        core = GcfRescueV02(RescueConfig(Vec2(90, 10), Vec2(10, 10), max_update_gap_s=100))
        core.update(SensorSnapshot(0, GnssState.STABLE, Vec2(3, 0), 10, Vec2(10, 10), 1, 1, 1, 1, 0, True, 1))
        decision = core.update(SensorSnapshot(7, GnssState.LOST, Vec2(3, 0), 10, None, 0, 1, 1, 1, 0, True, 1))
        intent = GeofenceRoutePlanner.from_demo_map().translate(decision)
        self.assertEqual(intent.action, Action.REPLAN)
        self.assertTrue(intent.not_a_gps_fix)
        validate_intent(intent)

    def test_long_loss_changes_goal_to_safe_zone(self):
        rows = synthetic_gnss_mask_replay()
        final = rows[-1].navigation_intent
        self.assertEqual(final.action, Action.RETURN_SAFE)
        self.assertEqual(final.final_target_xy_m, Vec2(10, 10))

    def test_planner_holds_if_destination_is_illegal(self):
        grid = GridMap(30, 30, 10, frozenset({(2, 2)}))
        core = GcfRescueV02(RescueConfig(Vec2(25, 25), Vec2(5, 5), max_update_gap_s=100))
        core.update(SensorSnapshot(0, GnssState.STABLE, Vec2(1, 0), 0, Vec2(5, 5), 1, 1, 1, 1, 0, True, 1))
        d = core.update(SensorSnapshot(6, GnssState.LOST, Vec2(1, 0), 0, None, 0, 1, 1, 1, 0, True, 1))
        self.assertEqual(GeofenceRoutePlanner(grid).translate(d).action, Action.HOLD)


if __name__ == "__main__":
    unittest.main()
