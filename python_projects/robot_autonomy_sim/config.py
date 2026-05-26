from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MapConfig:
    width: int = 20
    height: int = 20
    obstacle_ratio: float = 0.16
    random_seed: int = 42


@dataclass(frozen=True)
class RobotConfig:
    wheel_base: float = 0.4
    max_speed: float = 1.8
    dt: float = 0.1
    goal_tolerance: float = 0.6


@dataclass(frozen=True)
class SensorConfig:
    beam_count: int = 9
    max_range: float = 6.0
    noise_std: float = 0.03
    buffer_size: int = 16


@dataclass(frozen=True)
class PIDConfig:
    kp: float = 1.1
    ki: float = 0.05
    kd: float = 0.18
    integral_limit: float = 1.8


@dataclass(frozen=True)
class SimConfig:
    max_steps: int = 350
    log_level: str = "INFO"
    log_path: Path = Path("simulation.log")
