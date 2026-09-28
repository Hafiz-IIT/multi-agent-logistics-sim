# Multi-Agent Logistics Simulator

> Transparent multi-agent logistics allocation simulator with distance, load capacity and task feasibility constraints.

## Status
**Reproducible simulation/research prototype** with executable code, tests, CI, architecture, evaluation and roadmap documentation.

## Problem
Fleet coordination requires assigning tasks across multiple agents without violating capacity while controlling travel cost and imbalance.

## Architecture
Agent state + task set → feasibility filter → distance score → assignment → capacity/location update → unassigned-task report.

## Quick start
```bash
python -m unittest discover -s tests -v
python multi_agent_logistics_sim.py
```

## Implemented
- Agent position/capacity state
- Task load/location state
- Euclidean distance scoring
- Feasibility filtering
- Greedy nearest-agent allocation
- Capacity updates
- Unassigned reporting
- Tests and CI

## Research lineage
- *Multi-Agent Coordination via Linear Statistical Models and Reinforcement Learning*
- *Integrated Linear Models for Multi-Agent Systems*
- *Scalable Architectures for Distributed Intelligent Agents*

## Evaluation
Current tests cover nearest-feasible choice and capacity exhaustion; future experiments should compare centralized, auction and learned policies.

## Limitations
- Greedy centralized allocator
- No communication model
- No time windows
- No RL policy yet
- Synthetic coordinates only

## License
MIT.

## Extended implementation

- `auction_allocator.py` adds feasible-agent bidding with travel/load scoring and explicit assignment results.
