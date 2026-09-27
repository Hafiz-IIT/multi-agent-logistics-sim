# Multi-Agent Logistics Simulator

> **A small coordination testbed for capacity-constrained task allocation among moving logistics agents.**

The older multi-agent logistics and automated-agent ideas need a concrete baseline before introducing MARL. This repository models agents, tasks, capacity, location, and greedy allocation so more advanced coordination methods have an inspectable comparator.

## Implemented
- agent position/capacity state
- task location/load model
- Euclidean distance
- nearest-feasible assignment
- capacity updates
- agent position updates
- unassigned-task reporting

## Run
```bash
python -m unittest discover -s tests -v
python multi_agent_logistics_sim.py
```

## Repository map
`multi_agent_logistics_sim.py` core · `tests/` tests · `examples/` fixtures · `docs/architecture.md` design · `docs/research-agenda.md` experiments · `STATUS.md` claims · `CITATION.cff` citation

## Pipeline
**agents + tasks → feasibility → distance → assignment → state update → unserved tasks**

## Research lineage
This consolidates older multi-agent logistics coordination, cargo allocation, automated-agent, and distributed-agent research directions.

## Evaluation direction
Stress the greedy allocator with clustered demand, asymmetric capacity, task ordering, and adversarial demand distributions; later compare against auction, optimization, or multi-agent RL policies.

## Maturity
**Research prototype.** This is not multi-agent reinforcement learning, a real dispatch system, or an optimal assignment solver.
