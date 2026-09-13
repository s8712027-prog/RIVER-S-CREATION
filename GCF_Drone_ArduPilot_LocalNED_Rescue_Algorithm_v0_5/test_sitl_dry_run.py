import unittest

from ardupilot_adapter import *
from ardupilot_sitl_dry_run import to_sitl_preview
from gcf_rescue_v02 import Action, Vec2
from route_planner import NavigationIntent


class SitlDryRunTests(unittest.TestCase):
    def test_preview_is_position_target_but_never_transmits(self):
        adapter = ArduPilotGuidedAdapter(ArduPilotAdapterConfig(RouteFrameToNed(0, 0), -10))
        intent = NavigationIntent("GCF_HIGH_LEVEL_NAVIGATION_INTENT", Action.REPLAN, Vec2(10, 5), Vec2(20, 5), 2,
                                  ((0, 0), (1, 0)), "test")
        status, request = adapter.build(intent, ArduPilotState("GUIDED", True, True, "external_nav", True))
        self.assertEqual(status, AdapterStatus.READY)
        preview = to_sitl_preview(request, 123)
        self.assertFalse(preview["transmit"])
        self.assertEqual(preview["message"], "SET_POSITION_TARGET_LOCAL_NED")
        self.assertTrue(preview["not_a_gps_fix"])


if __name__ == "__main__":
    unittest.main()
