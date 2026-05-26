from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass
from typing import Deque

from config import RobotConfig, SensorConfig
from world import GridWorld, Pose


@dataclass
class RobotState:
    x: float
    y: float
    heading: float
    v: float
    w: float


class MockLidar:
    def __init__(self, world: GridWorld, cfg: SensorConfig) -> None:
        self.world = world
        self.cfg = cfg

    def scan(self, state: RobotState) -> list[float]:
        readings: list[float] = []
        base = state.heading
        half = self.cfg.beam_count // 2
        for i in range(self.cfg.beam_count):
            offset = (i - half) * (math.pi / max(self.cfg.beam_count - 1, 1))
            angle = base + offset
            readings.append(self._ray_cast(state.x, state.y, angle))
        return readings

    def _ray_cast(self, x: float, y: float, angle: float) -> float:
        d = 0.0
        step = 0.15
        while d <= self.cfg.max_range:
            tx = int(round(x + d * math.cos(angle)))
            ty = int(round(y + d * math.sin(angle)))
            if self.world.is_obstacle(tx, ty):
                return d
            d += step
        return self.cfg.max_range


class DifferentialDriveRobot:
    def __init__(self, cfg: RobotConfig, sensor_cfg: SensorConfig, world: GridWorld, initial_pose: Pose) -> None:
        self.cfg = cfg
        self.state = RobotState(initial_pose.x, initial_pose.y, initial_pose.heading, 0.0, 0.0)
        self.lidar = MockLidar(world, sensor_cfg)
        self.sensor_buffer: Deque[list[float]] = deque(maxlen=sensor_cfg.buffer_size)

    def apply_control(self, v_cmd: float, w_cmd: float) -> None:
        self.state.v = max(-self.cfg.max_speed, min(self.cfg.max_speed, v_cmd))
        self.state.w = w_cmd

    def step(self) -> None:
        dt = self.cfg.dt
        # wheel odometry style integration
        self.state.heading += self.state.w * dt
        self.state.x += self.state.v * math.cos(self.state.heading) * dt
        self.state.y += self.state.v * math.sin(self.state.heading) * dt

    def sense(self) -> list[float]:
        scan = self.lidar.scan(self.state)
        self.sensor_buffer.append(scan)
        return scan
