from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable

from config import MapConfig


@dataclass(frozen=True)
class Pose:
    x: float
    y: float
    heading: float


class GridWorld:
    def __init__(self, cfg: MapConfig) -> None:
        self.width = cfg.width
        self.height = cfg.height
        self._rng = random.Random(cfg.random_seed)
        self._grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self._build_obstacles(cfg.obstacle_ratio)

    def _build_obstacles(self, ratio: float) -> None:
        for y in range(self.height):
            for x in range(self.width):
                if x in (0, self.width - 1) or y in (0, self.height - 1):
                    self._grid[y][x] = 1
                    continue
                if self._rng.random() < ratio:
                    self._grid[y][x] = 1

    def is_obstacle(self, x: int, y: int) -> bool:
        if not (0 <= x < self.width and 0 <= y < self.height):
            return True
        return self._grid[y][x] == 1

    def set_free(self, x: int, y: int) -> None:
        self._grid[y][x] = 0

    def neighbors(self, x: int, y: int) -> Iterable[tuple[int, int]]:
        candidates = ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
        for nx, ny in candidates:
            if not self.is_obstacle(nx, ny):
                yield nx, ny

    def choose_free_cell(self) -> tuple[int, int]:
        for _ in range(1000):
            x = self._rng.randrange(1, self.width - 1)
            y = self._rng.randrange(1, self.height - 1)
            if not self.is_obstacle(x, y):
                return x, y
        raise RuntimeError("No free cell available")

    def render(self, robot_xy: tuple[int, int], goal_xy: tuple[int, int]) -> str:
        rows: list[str] = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if (x, y) == robot_xy:
                    row.append("R")
                elif (x, y) == goal_xy:
                    row.append("G")
                elif self.is_obstacle(x, y):
                    row.append("#")
                else:
                    row.append(".")
            rows.append("".join(row))
        return "\n".join(rows)
