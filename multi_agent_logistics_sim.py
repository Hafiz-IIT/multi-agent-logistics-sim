from __future__ import annotations

from dataclasses import dataclass
from math import hypot, isfinite


def _finite_float(name: str, value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite number")
    try:
        normalized = float(value)
    except (OverflowError, TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a finite number") from exc
    if not isfinite(normalized):
        raise ValueError(f"{name} must be a finite number")
    return normalized


@dataclass
class Agent:
    name: str
    x: float
    y: float
    remaining_capacity: float

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("agent name is required")
        self.name = self.name.strip()
        self.x = _finite_float("agent x", self.x)
        self.y = _finite_float("agent y", self.y)
        self.remaining_capacity = _finite_float("agent capacity", self.remaining_capacity)
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
        object.__setattr__(self, "task_id", self.task_id.strip())
        object.__setattr__(self, "x", _finite_float("task x", self.x))
        object.__setattr__(self, "y", _finite_float("task y", self.y))
        load = _finite_float("task load", self.load)
        if load <= 0:
            raise ValueError("task load must be finite and positive")
        object.__setattr__(self, "load", load)


def prepare_allocation_inputs(agents: list[Agent], tasks: list[Task]) -> list[Agent]:
    if not isinstance(agents, list) or not isinstance(tasks, list):
        raise ValueError("agents and tasks must be lists")
    if any(not isinstance(agent, Agent) for agent in agents) or any(not isinstance(task, Task) for task in tasks):
        raise ValueError("agents and tasks must contain Agent and Task instances")
    # Reconstruct agents first: callers may have mutated the public mutable
    # Agent instances after construction, so revalidate before checking identity.
    working_agents = [Agent(agent.name, agent.x, agent.y, agent.remaining_capacity) for agent in agents]
    agent_names = [agent.name for agent in working_agents]
    task_ids = [task.task_id for task in tasks]
    if len(set(agent_names)) != len(agent_names):
        raise ValueError("agent names must be unique")
    if len(set(task_ids)) != len(task_ids):
        raise ValueError("task identifiers must be unique")
    # Allocation runs against private working copies; caller-owned objects are not mutated.
    return working_agents


def distance(agent: Agent, task: Task) -> float:
    if not isinstance(agent, Agent) or not isinstance(task, Task):
        raise TypeError("distance requires Agent and Task values")
    agent = Agent(agent.name, agent.x, agent.y, agent.remaining_capacity)
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
