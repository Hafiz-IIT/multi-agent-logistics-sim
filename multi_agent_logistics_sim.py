from __future__ import annotations

from dataclasses import dataclass
from math import hypot, isfinite


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


def validate_inputs(agents: list[Agent], tasks: list[Task]) -> None:
    agent_names = []
    for agent in agents:
        if not isinstance(agent.name, str) or not agent.name.strip():
            raise ValueError("agent name must be non-empty")
        agent_names.append(agent.name)
        values = (agent.x, agent.y, agent.remaining_capacity)
        if not all(isinstance(v, (int, float)) and not isinstance(v, bool) and isfinite(v) for v in values):
            raise ValueError("agent coordinates and capacity must be finite numbers")
        if agent.remaining_capacity < 0:
            raise ValueError("agent capacity must be non-negative")
    if len(agent_names) != len(set(agent_names)):
        raise ValueError("agent names must be unique")

    task_ids = []
    for task in tasks:
        if not isinstance(task.task_id, str) or not task.task_id.strip():
            raise ValueError("task_id must be non-empty")
        task_ids.append(task.task_id)
        values = (task.x, task.y, task.load)
        if not all(isinstance(v, (int, float)) and not isinstance(v, bool) and isfinite(v) for v in values):
            raise ValueError("task coordinates and load must be finite numbers")
        if task.load <= 0:
            raise ValueError("task load must be positive")
    if len(task_ids) != len(set(task_ids)):
        raise ValueError("task IDs must be unique")


def distance(agent: Agent, task: Task) -> float:
    return hypot(agent.x - task.x, agent.y - task.y)


def assign(agents: list[Agent], tasks: list[Task]) -> dict:
    validate_inputs(agents, tasks)
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
