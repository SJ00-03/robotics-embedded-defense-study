from config import MapConfig
from fsm import NavState, ObstacleAvoidanceFSM
from planner import PathPlanner
from world import GridWorld


def test_bfs_finds_path() -> None:
    world = GridWorld(MapConfig(width=10, height=10, obstacle_ratio=0.0, random_seed=1))
    planner = PathPlanner(world)
    path = planner.bfs((1, 1), (8, 8))
    assert path[0] == (1, 1)
    assert path[-1] == (8, 8)
    assert len(path) > 0


def test_fsm_transitions() -> None:
    fsm = ObstacleAvoidanceFSM(stop_distance=1.0, clear_distance=1.5)
    assert fsm.update(front_distance=2.0, at_goal=False) == NavState.NAVIGATING
    assert fsm.update(front_distance=0.7, at_goal=False) == NavState.AVOID_OBSTACLE
    assert fsm.update(front_distance=2.0, at_goal=False) == NavState.NAVIGATING
    assert fsm.update(front_distance=2.0, at_goal=True) == NavState.GOAL_REACHED
