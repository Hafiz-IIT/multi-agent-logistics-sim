from __future__ import annotations

from dataclasses import dataclass
from math import hypot

from multi_agent_logistics_sim import Agent, Task


@dataclass(frozen=True)
class Bid:
    agent: str
    task_id: str
    score: float


def bid(agent: Agent, task: Task, *, load_penalty: float = 0.1) -> Bid | None:
    if agent.remaining_capacity < task.load:
        return None
    travel = hypot(agent.x - task.x, agent.y - task.y)
    utilization_penalty = load_penalty * (
        task.load / max(agent.remaining_capacity, 1e-12)
    )
    return Bid(agent.name, task.task_id, travel + utilization_penalty)


def auction_assign(
    agents: list[Agent],
    tasks: list[Task],
    *,
    load_penalty: float = 0.1,
) -> dict:
    assignments: dict[str, str] = {}
    winning_bids: dict[str, float] = {}
    unassigned: list[str] = []

    for task in sorted(tasks, key=lambda t: t.task_id):
        candidates = [
            candidate
            for agent in agents
            if (candidate := bid(agent, task, load_penalty=load_penalty)) is not None
        ]
        if not candidates:
            unassigned.append(task.task_id)
            continue

        winner = min(candidates, key=lambda b: (b.score, b.agent))
        agent = next(a for a in agents if a.name == winner.agent)
        assignments[task.task_id] = agent.name
        winning_bids[task.task_id] = winner.score
        agent.remaining_capacity -= task.load
        agent.x, agent.y = task.x, task.y

    return {
        "assignments": assignments,
        "winning_bids": winning_bids,
        "unassigned": unassigned,
    }
