# GCF-Drone v0.5: ArduCopter local-NED Conversion and Dry Run

v0.5 retains the rescue core, planner and Guided adapter, then adds:

- `route_planner.py`: A* route planning in a mission-local grid with no-go/geofence cells.
- `replay_harness.py`: deterministic GNSS-mask replay that tests the sequence `anchor → rescue guidance → containment`.
- `ardupilot_adapter.py`: strict local-NED Guided request builder with EKF and mode gates.
- `ardupilot_coordinate_adapter.py`: locked bidirectional route-frame/local-NED transform and telemetry conversion.
- `ardupilot_sitl_dry_run.py`: non-transmitting MAVLink-shaped review output.

The output remains high-level: `NavigationIntent` then a local-NED Guided request. It is not a GPS packet, MAVLink actuator packet, attitude target, or low-level flight-control command. See `ARDUPILOT_INTEGRATION.md` and `ARDUPILOT_LOCAL_NED_CONVERSION.md`.

Run all verification:

```text
python -m unittest -v
```

The demo scenario is intentionally synthetic. Its result verifies state-machine and safety-routing behavior, not navigation accuracy or real-flight performance.
