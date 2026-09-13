import unittest

from ardupilot_adapter import *
from gcf_rescue_v02 import Action, Vec2
from route_planner import NavigationIntent


def intent(action=Action.REPLAN, waypoint=Vec2(10, 5)):
    return NavigationIntent("GCF_HIGH_LEVEL_NAVIGATION_INTENT", action, waypoint,
                            Vec2(100, 50), 2.0, ((0, 0), (1, 1)), "unit-test")


class ArduPilotAdapterTests(unittest.TestCase):
    def setUp(self):
        self.adapter = ArduPilotGuidedAdapter(ArduPilotAdapterConfig(
            RouteFrameToNed(100, 200), command_down_m=-20.0))
        self.ready = ArduPilotState("GUIDED", True, True, "external_nav", True)

    def test_creates_position_only_local_ned_request(self):
        status, request = self.adapter.build(intent(), self.ready)
        self.assertEqual(status, AdapterStatus.READY)
        self.assertEqual(request.request_type, "SET_POSITION_TARGET_LOCAL_NED")
        self.assertEqual((request.north_m, request.east_m, request.down_m), (110, 205, -20.0))
        validate_mavlink_request(request)

    def test_never_uses_guided_position_without_local_ekf(self):
        status, request = self.adapter.build(intent(), ArduPilotState("GUIDED", True, False, "external_nav", True))
        self.assertEqual(status, AdapterStatus.BLOCKED)
        self.assertIn("EKF", request.reason)

    def test_not_guided_is_blocked(self):
        status, _ = self.adapter.build(intent(), ArduPilotState("LOITER", True, True, "optical_flow", True))
        self.assertEqual(status, AdapterStatus.BLOCKED)

    def test_hold_never_builds_motion_request(self):
        status, request = self.adapter.build(intent(Action.HOLD, None), self.ready)
        self.assertEqual(status, AdapterStatus.HOLD)
        self.assertEqual(request.request_type, "REQUEST_GUIDED_HOLD")

    def test_land_manual_defers_to_native_failsafe_or_operator(self):
        status, request = self.adapter.build(intent(Action.LAND_MANUAL, None), self.ready)
        self.assertEqual(status, AdapterStatus.FAILSAFE_REQUIRED)
        self.assertEqual(request.request_type, "REQUEST_OPERATOR_OR_ARDUPILOT_FAILSAFE")


if __name__ == "__main__":
    unittest.main()
