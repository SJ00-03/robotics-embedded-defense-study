from __future__ import annotations

from enum import Enum, auto


class NavState(Enum):
    NAVIGATING = auto()
    AVOID_OBSTACLE = auto()
    GOAL_REACHED = auto()
    FAILED = auto()


class ObstacleAvoidanceFSM:
    def __init__(self, stop_distance: float = 0.8, clear_distance: float = 1.4) -> None:
        self.state = NavState.NAVIGATING
        self.stop_distance = stop_distance
        self.clear_distance = clear_distance

    def update(self, front_distance: float, at_goal: bool) -> NavState:
        if at_goal:
            self.state = NavState.GOAL_REACHED
            return self.state

        if self.state == NavState.NAVIGATING and front_distance <= self.stop_distance:
            self.state = NavState.AVOID_OBSTACLE
        elif self.state == NavState.AVOID_OBSTACLE and front_distance >= self.clear_distance:
            self.state = NavState.NAVIGATING

        return self.state
