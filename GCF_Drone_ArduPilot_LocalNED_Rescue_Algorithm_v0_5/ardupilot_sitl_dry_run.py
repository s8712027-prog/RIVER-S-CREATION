"""Dry-run serialization of approved ArduPilot Guided requests.

This module creates a reviewable dict matching the position-target fields. It
does not import pymavlink, create sockets, or transmit MAVLink packets.
"""
from __future__ import annotations

from dataclasses import asdict

from ardupilot_adapter import MavlinkRequest, validate_mavlink_request


def to_sitl_preview(request: MavlinkRequest, time_boot_ms: int = 0) -> dict:
    validate_mavlink_request(request)
    if request.request_type != "SET_POSITION_TARGET_LOCAL_NED":
        return {"dry_run": True, "request": asdict(request), "transmit": False}
    return {
        "dry_run": True,
        "transmit": False,
        "message": "SET_POSITION_TARGET_LOCAL_NED",
        "time_boot_ms": time_boot_ms,
        "coordinate_frame": request.coordinate_frame,
        "type_mask": request.type_mask,
        "x_north_m": request.north_m,
        "y_east_m": request.east_m,
        "z_down_m": request.down_m,
        "not_a_gps_fix": True,
        "not_low_level_flight_control": True,
        "reason": request.reason,
    }
