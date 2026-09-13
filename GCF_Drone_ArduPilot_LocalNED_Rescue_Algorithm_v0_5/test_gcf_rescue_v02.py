import unittest
from gcf_rescue_v02 import *


class GcfRescueV02Tests(unittest.TestCase):
    def setUp(self):
        self.core = GcfRescueV02(RescueConfig(
            target_xy_m=Vec2(500, 0), safe_xy_m=Vec2(0, 0),
            recovery_confirmations=3, max_update_gap_s=100.0,
        ))

    def sample(self, t, gnss, pos=None, *, quality=1.0, velocity_q=1.0,
               vision=1.0, flow=1.0, battery=1.0, risk=0.0):
        return SensorSnapshot(t, gnss, Vec2(5, 0), 10, pos, quality,
                              velocity_q, vision, flow, risk, True, battery)

    def anchor(self):
        return self.core.update(self.sample(0, GnssState.STABLE, Vec2(100, 0)))

    def test_stable_gnss_sets_true_route_anchor(self):
        self.anchor()
        self.assertEqual(self.core.est.xy_m, Vec2(100, 0))

    def test_loss_without_anchor_fails_closed(self):
        d = self.core.update(self.sample(0, GnssState.LOST))
        self.assertEqual((d.nav_state, d.action), (NavState.NO_ANCHOR, Action.LAND_MANUAL))

    def test_uncertainty_floor_contains_before_time_budget(self):
        self.anchor()
        self.core.est.sigma_m = self.core.cfg.containment_sigma_m
        d = self.core.update(self.sample(10, GnssState.LOST))
        self.assertEqual((d.nav_state, d.action), (NavState.CONTAINMENT, Action.RETURN_SAFE))

    def test_recovery_requires_consecutive_consistent_samples(self):
        self.anchor()
        self.core.update(self.sample(10, GnssState.LOST))
        d1 = self.core.update(self.sample(11, GnssState.STABLE, Vec2(160, 0)))
        d2 = self.core.update(self.sample(12, GnssState.STABLE, Vec2(161, 0)))
        d3 = self.core.update(self.sample(13, GnssState.STABLE, Vec2(162, 0)))
        self.assertEqual(d1.nav_state, NavState.RECOVERY_VERIFY)
        self.assertEqual(d2.nav_state, NavState.RECOVERY_VERIFY)
        self.assertEqual(d3.nav_state, NavState.NORMAL)

    def test_optical_flow_can_cover_disabled_vision(self):
        cfg = RescueConfig(Vec2(10, 0), Vec2(0, 0), vision_enabled=False,
                           optical_flow_enabled=True, max_update_gap_s=100)
        core = GcfRescueV02(cfg)
        d = core.update(SensorSnapshot(0, GnssState.STABLE, Vec2(0, 0), 0,
                                       Vec2(0, 0), 1, 1, 0, 1, 0, True, 1))
        self.assertEqual(d.action, Action.PROCEED)

    def test_stale_input_fails_closed(self):
        self.anchor()
        self.core.cfg = RescueConfig(Vec2(500, 0), Vec2(0, 0), max_update_gap_s=1.0)
        d = self.core.update(self.sample(3, GnssState.LOST))
        self.assertEqual(d.action, Action.LAND_MANUAL)

    def test_packet_cannot_be_interpreted_as_gps_or_low_level_control(self):
        d = self.anchor()
        validate_for_flight_controller_adapter(d)
        self.assertTrue(d.not_a_gps_fix and d.not_low_level_flight_control)


if __name__ == "__main__":
    unittest.main()
