import unittest
from math import pi

from ardupilot_coordinate_adapter import *
from gcf_rescue_v02 import GnssState, Vec2


class CoordinateAdapterTests(unittest.TestCase):
    def setUp(self):
        self.a = RouteFrameAlignment(LocalNed(100, 200, -5), pi / 2, 10.0)
        self.adapter = ArduPilotTelemetryAdapter(self.a, frozenset({"external_nav", "optical_flow"}))

    def test_route_ned_round_trip_preserves_position_and_altitude(self):
        ned = self.a.route_to_ned(Vec2(10, 5), 20)
        xy, up = self.a.ned_to_route(ned)
        self.assertAlmostEqual(xy.x, 10)
        self.assertAlmostEqual(xy.y, 5)
        self.assertAlmostEqual(up, 20)

    def test_velocity_inverse_rotation_is_correct(self):
        # At +90°, NED East velocity becomes route-forward velocity.
        route_v = self.a.ned_velocity_to_route(LocalNedVelocity(0, 3, 0))
        self.assertAlmostEqual(route_v.x, 3)
        self.assertAlmostEqual(route_v.y, 0)

    def test_stable_gnss_provides_route_position(self):
        t = ArduPilotLocalTelemetry(11, LocalNed(95, 210, -20), LocalNedVelocity(0, 1, 0),
                                    True, GnssState.STABLE, 1, 1, 20, 1, 1, 0, True, 1, "external_nav")
        s = self.adapter.to_sensor_snapshot(t)
        self.assertIsNotNone(s.route_xy_m)
        self.assertAlmostEqual(s.route_xy_m.x, 10)

    def test_lost_gnss_does_not_provide_a_new_gnss_anchor(self):
        t = ArduPilotLocalTelemetry(11, LocalNed(95, 210, -20), LocalNedVelocity(0, 1, 0),
                                    True, GnssState.LOST, 0, 1, 20, 1, 1, 0, True, 1, "external_nav")
        s = self.adapter.to_sensor_snapshot(t)
        self.assertIsNone(s.route_xy_m)

    def test_unapproved_ekf_source_is_rejected(self):
        t = ArduPilotLocalTelemetry(11, LocalNed(0, 0, 0), LocalNedVelocity(0, 0, 0),
                                    True, GnssState.LOST, 0, 1, 0, 1, 1, 0, True, 1, "gps")
        with self.assertRaises(ValueError):
            self.adapter.to_sensor_snapshot(t)


if __name__ == "__main__":
    unittest.main()
