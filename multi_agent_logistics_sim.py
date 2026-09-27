from __future__ import annotations

from dataclasses import dataclass
from math import hypot


@dataclass
class Agent:
    name: str
    x: float
    y: float
    remaining_capacity: float


@dataclass(frozen=True)
class Task:
    task_id: str
    x: float
    y: float
    load: float


def distance(agent: Agent, task: Task) -> float:
    return hypot(agent.x - task.x, agent.y - task.y)


def assign(agents: list[Agent], tasks: list[Task]) -> dict:
    assignments: dict[str, str] = {}
    unassigned: list[str] = []

    for task in sorted(tasks, key=lambda t: (-t.load, t.task_id)):
        feasible = [a for a in agents if a.remaining_capacity >= task.load]
        if not feasible:
            unassigned.append(task.task_id)
            continue
        chosen = min(feasible, key=lambda a: (distance(a, task), a.name))
        assignments[task.task_id] = chosen.name
        chosen.remaining_capacity -= task.load
        chosen.x, chosen.y = task.x, task.y

    return {"assignments": assignments, "unassigned": unassigned}


if __name__ == "__main__":
    agents = [Agent("A", 0, 0, 5), Agent("B", 10, 0, 5)]
    tasks = [Task("T1", 1, 0, 2), Task("T2", 9, 0, 3)]
    print(assign(agents, tasks))
