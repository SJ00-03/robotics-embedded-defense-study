from __future__ import annotations

from collections import deque

from world import GridWorld


class PathPlanner:
    def __init__(self, world: GridWorld) -> None:
        self.world = world

    def bfs(self, start: tuple[int, int], goal: tuple[int, int]) -> list[tuple[int, int]]:
        q: deque[tuple[int, int]] = deque([start])
        parent: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
        while q:
            cur = q.popleft()
            if cur == goal:
                break
            for nxt in self.world.neighbors(*cur):
                if nxt in parent:
                    continue
                parent[nxt] = cur
                q.append(nxt)

        if goal not in parent:
            raise ValueError(f"No route from {start} to {goal}")

        path: list[tuple[int, int]] = []
        node: tuple[int, int] | None = goal
        while node is not None:
            path.append(node)
            node = parent[node]
        path.reverse()
        return path
