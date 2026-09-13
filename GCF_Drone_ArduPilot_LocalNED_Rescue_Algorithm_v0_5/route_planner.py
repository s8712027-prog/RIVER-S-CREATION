"""Platform-neutral, high-level route planner for GCF-Drone v0.3.

It plans only in a mission-local 2-D grid and returns navigation intent. A
flight-controller adapter remains responsible for vehicle limits and execution.
"""
from __future__ import annotations

from dataclasses import dataclass
from heapq import heappop, heappush
from math import ceil, hypot
from typing import Iterable, Optional

from gcf_rescue_v02 import Action, DecisionPacket, Vec2


Cell = tuple[int, int]


@dataclass(frozen=True)
class GridMap:
    width_m: float
    height_m: float
    resolution_m: float
    blocked: frozenset[Cell]

    @property
    def width_cells(self) -> int:
        return int(ceil(self.width_m / self.resolution_m))

    @property
    def height_cells(self) -> int:
        return int(ceil(self.height_m / self.resolution_m))

    def to_cell(self, p: Vec2) -> Cell:
        return (int(p.x // self.resolution_m), int(p.y // self.resolution_m))

    def to_point(self, c: Cell) -> Vec2:
        half = self.resolution_m / 2.0
        return Vec2((c[0] * self.resolution_m) + half,
                    (c[1] * self.resolution_m) + half)

    def legal(self, c: Cell) -> bool:
        return 0 <= c[0] < self.width_cells and 0 <= c[1] < self.height_cells and c not in self.blocked


@dataclass(frozen=True)
class NavigationIntent:
    packet_type: str
    action: Action
    waypoint_xy_m: Optional[Vec2]
    final_target_xy_m: Vec2
    speed_mps: float
    route_cells: tuple[Cell, ...]
    reason: str
    not_a_gps_fix: bool = True
    not_low_level_flight_control: bool = True


class GeofenceRoutePlanner:
    def __init__(self, grid: GridMap):
        self.grid = grid

    @staticmethod
    def _neighbors(c: Cell) -> Iterable[Cell]:
        x, y = c
        yield x + 1, y
        yield x - 1, y
        yield x, y + 1
        yield x, y - 1

    @staticmethod
    def _h(a: Cell, b: Cell) -> float:
        return hypot(a[0] - b[0], a[1] - b[1])

    def plan(self, origin: Vec2, target: Vec2) -> Optional[tuple[Cell, ...]]:
        start, goal = self.grid.to_cell(origin), self.grid.to_cell(target)
        if not self.grid.legal(start) or not self.grid.legal(goal):
            return None
        queue: list[tuple[float, Cell]] = [(0.0, start)]
        parent: dict[Cell, Optional[Cell]] = {start: None}
        cost: dict[Cell, float] = {start: 0.0}
        while queue:
            _, current = heappop(queue)
            if current == goal:
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                return tuple(reversed(path))
            for nxt in self._neighbors(current):
                if not self.grid.legal(nxt):
                    continue
                proposal = cost[current] + 1.0
                if proposal < cost.get(nxt, float("inf")):
                    cost[nxt] = proposal
                    parent[nxt] = current
                    heappush(queue, (proposal + self._h(nxt, goal), nxt))
        return None

    def translate(self, d: DecisionPacket) -> NavigationIntent:
        if d.action in (Action.HOLD, Action.LAND_MANUAL) or d.estimated_xy_m is None:
            return NavigationIntent("GCF_HIGH_LEVEL_NAVIGATION_INTENT", d.action, None,
                                    d.target_xy_m, 0.0, (), d.reason)
        cells = self.plan(d.estimated_xy_m, d.target_xy_m)
        if cells is None:
            return NavigationIntent("GCF_HIGH_LEVEL_NAVIGATION_INTENT", Action.HOLD, None,
                                    d.target_xy_m, 0.0, (), "no legal geofence route")
        waypoint = self.grid.to_point(cells[min(1, len(cells) - 1)])
        return NavigationIntent("GCF_HIGH_LEVEL_NAVIGATION_INTENT", d.action, waypoint,
                                d.target_xy_m, d.desired_ground_speed_mps, cells, d.reason)


def validate_intent(intent: NavigationIntent) -> None:
    if intent.packet_type != "GCF_HIGH_LEVEL_NAVIGATION_INTENT":
        raise ValueError("unexpected intent type")
    if not intent.not_a_gps_fix or not intent.not_low_level_flight_control:
        raise ValueError("authority-boundary breach")
    if intent.speed_mps < 0:
        raise ValueError("invalid speed")
