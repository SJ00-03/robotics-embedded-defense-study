from __future__ import annotations

from dataclasses import dataclass

from config import PIDConfig


@dataclass
class PIDController:
    cfg: PIDConfig
    integral: float = 0.0
    prev_error: float = 0.0

    def update(self, target: float, current: float, dt: float) -> float:
        error = target - current
        self.integral += error * dt
        self.integral = max(-self.cfg.integral_limit, min(self.integral, self.cfg.integral_limit))
        derivative = (error - self.prev_error) / dt if dt > 0 else 0.0
        self.prev_error = error
        return (
            self.cfg.kp * error
            + self.cfg.ki * self.integral
            + self.cfg.kd * derivative
        )
