from __future__ import annotations

import argparse
import logging
import math
from pathlib import Path

from config import MapConfig, PIDConfig, RobotConfig, SensorConfig, SimConfig
from control import PIDController
from fsm import NavState, ObstacleAvoidanceFSM
from planner import PathPlanner
from robot import DifferentialDriveRobot
from world import GridWorld, Pose


def setup_logging(sim_cfg: SimConfig) -> None:
    log_level = getattr(logging, sim_cfg.log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(sim_cfg.log_path, mode="w")],
    )


def heading_to_target(cur_x: float, cur_y: float, tgt_x: float, tgt_y: float) -> float:
    return math.atan2(tgt_y - cur_y, tgt_x - cur_x)


def angle_wrap(a: float) -> float:
    while a > math.pi:
        a -= 2 * math.pi
    while a < -math.pi:
        a += 2 * math.pi
    return a


def run_simulation(project_dir: Path) -> int:
    map_cfg = MapConfig()
    robot_cfg = RobotConfig()
    sensor_cfg = SensorConfig()
    sim_cfg = SimConfig(log_path=project_dir / "simulation.log")
    pid_cfg = PIDConfig()

    setup_logging(sim_cfg)
    world = GridWorld(map_cfg)
    start = world.choose_free_cell()
    goal = world.choose_free_cell()
    world.set_free(*start)
    world.set_free(*goal)

    planner = PathPlanner(world)
    try:
        path = planner.bfs(start, goal)
    except ValueError as exc:
        logging.exception("Path planning failed: %s", exc)
        return 2

    robot = DifferentialDriveRobot(robot_cfg, sensor_cfg, world, Pose(float(start[0]), float(start[1]), 0.0))
    fsm = ObstacleAvoidanceFSM()
    pid = PIDController(pid_cfg)

    waypoint_idx = 1
    logging.info("Start=%s Goal=%s Path length=%d", start, goal, len(path))
    logging.info("Map:\n%s", world.render((start[0], start[1]), (goal[0], goal[1])))

    for step in range(sim_cfg.max_steps):
        scan = robot.sense()
        front = scan[len(scan) // 2]

        if waypoint_idx >= len(path):
            target = goal
        else:
            target = path[waypoint_idx]

        dist_to_goal = math.hypot(goal[0] - robot.state.x, goal[1] - robot.state.y)
        nav_state = fsm.update(front_distance=front, at_goal=(dist_to_goal < robot_cfg.goal_tolerance))

        if nav_state == NavState.GOAL_REACHED:
            logging.info("Goal reached at step %d pos=(%.2f, %.2f)", step, robot.state.x, robot.state.y)
            return 0

        if nav_state == NavState.AVOID_OBSTACLE:
            robot.apply_control(v_cmd=0.2, w_cmd=0.9)
        else:
            heading_ref = heading_to_target(robot.state.x, robot.state.y, float(target[0]), float(target[1]))
            heading_err = angle_wrap(heading_ref - robot.state.heading)
            w_cmd = pid.update(target=0.0, current=-heading_err, dt=robot_cfg.dt)
            v_cmd = min(robot_cfg.max_speed, max(0.25, dist_to_goal * 0.45))
            robot.apply_control(v_cmd=v_cmd, w_cmd=w_cmd)

            dist_to_wp = math.hypot(target[0] - robot.state.x, target[1] - robot.state.y)
            if dist_to_wp < 0.7 and waypoint_idx < len(path) - 1:
                waypoint_idx += 1

        robot.step()
        logging.debug(
            "step=%03d state=%s pos=(%.2f,%.2f) h=%.2f v=%.2f w=%.2f front=%.2f wp=%s",
            step,
            nav_state.name,
            robot.state.x,
            robot.state.y,
            robot.state.heading,
            robot.state.v,
            robot.state.w,
            front,
            target,
        )

    logging.warning("Simulation ended without reaching goal")
    return 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="2D robot autonomous navigation simulation")
    parser.add_argument("--project-dir", type=Path, default=Path(__file__).resolve().parent)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        return run_simulation(args.project_dir)
    except Exception as exc:
        logging.exception("Unhandled simulation error: %s", exc)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
