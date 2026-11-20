from __future__ import annotations

from dataclasses import dataclass
from math import hypot, isfinite


@dataclass
class Agent:
    name: str
    x: float
    y: float
    remaining_capacity: float

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("agent name is required")
        if any(isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value)
               for value in (self.x, self.y, self.remaining_capacity)):
            raise ValueError("agent coordinates and capacity must be finite")
        if self.remaining_capacity < 0:
            raise ValueError("agent capacity must be non-negative")


@dataclass(frozen=True)
class Task:
    task_id: str
    x: float
    y: float
    load: float

    def __post_init__(self):
        if not isinstance(self.task_id, str) or not self.task_id.strip():
            raise ValueError("task_id is required")
        if any(isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value)
               for value in (self.x, self.y, self.load)) or self.load <= 0:
            raise ValueError("task coordinates must be finite and load must be finite and positive")


def prepare_allocation_inputs(agents: list[Agent], tasks: list[Task]) -> list[Agent]:
    if not isinstance(agents, list) or not isinstance(tasks, list):
        raise ValueError("agents and tasks must be lists")
    if any(not isinstance(agent, Agent) for agent in agents) or any(not isinstance(task, Task) for task in tasks):
        raise ValueError("agents and tasks must contain Agent and Task instances")
    agent_names = [agent.name for agent in agents]
    task_ids = [task.task_id for task in tasks]
    if len(set(agent_names)) != len(agent_names):
        raise ValueError("agent names must be unique")
    if len(set(task_ids)) != len(task_ids):
        raise ValueError("task identifiers must be unique")
    # Allocation runs against private working copies; caller-owned objects are not mutated.
    return [Agent(agent.name, agent.x, agent.y, agent.remaining_capacity) for agent in agents]


def distance(agent: Agent, task: Task) -> float:
    value = hypot(agent.x - task.x, agent.y - task.y)
    if not isfinite(value):
        raise OverflowError("distance is not representable as a finite float")
    return value


def assign(agents: list[Agent], tasks: list[Task]) -> dict:
    working_agents = prepare_allocation_inputs(agents, tasks)
    assignments: dict[str, str] = {}
    unassigned: list[str] = []

    for task in sorted(tasks, key=lambda t: (-t.load, t.task_id)):
        feasible = [a for a in working_agents if a.remaining_capacity >= task.load]
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
