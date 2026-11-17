from __future__ import annotations

from dataclasses import dataclass
from math import hypot, isfinite

from multi_agent_logistics_sim import Agent, Task, prepare_allocation_inputs


@dataclass(frozen=True)
class Bid:
    agent: str
    task_id: str
    score: float


def bid(agent: Agent, task: Task, *, load_penalty: float = 0.1) -> Bid | None:
    if not isfinite(load_penalty) or load_penalty < 0:
        raise ValueError("load_penalty must be finite and non-negative")
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
    working_agents = prepare_allocation_inputs(agents, tasks)
    if not isfinite(load_penalty) or load_penalty < 0:
        raise ValueError("load_penalty must be finite and non-negative")
    assignments: dict[str, str] = {}
    winning_bids: dict[str, float] = {}
    unassigned: list[str] = []

    # Sequential greedy auction: each task is allocated in task-id order.
    # This is a heuristic, not a globally optimal combinatorial auction.
    for task in sorted(tasks, key=lambda t: t.task_id):
        candidates = [
            candidate
            for agent in working_agents
            if (candidate := bid(agent, task, load_penalty=load_penalty)) is not None
        ]
        if not candidates:
            unassigned.append(task.task_id)
            continue

        winner = min(candidates, key=lambda b: (b.score, b.agent))
        agent = next(a for a in working_agents if a.name == winner.agent)
        assignments[task.task_id] = agent.name
        winning_bids[task.task_id] = winner.score
        agent.remaining_capacity -= task.load
        agent.x, agent.y = task.x, task.y

    return {
        "assignments": assignments,
        "winning_bids": winning_bids,
        "unassigned": unassigned,
    }
