# Multi-Agent Logistics Simulator

<p align="center"><strong>Fleet Coordination Under Capacity Constraints</strong><br/><sub>Transparent allocation experiments for agents, tasks, travel and load.</sub></p>

<p align="center"><img src="https://img.shields.io/badge/status-reproducible%20simulation-blue" alt="Simulation"/> <img src="https://img.shields.io/badge/focus-multi--agent%20allocation-purple" alt="Allocation"/></p>

## Question

**How should logistics tasks be allocated when agents differ in location and remaining capacity?**

```
Agents + tasks
      ↓
Feasibility filter
      ↓
Distance / load score
      ↓
Assignment
      ↓
Capacity + location update
      ↓
Unassigned-task report
```

## Try it

```bash
python multi_agent_logistics_sim.py
python -m unittest discover -s tests -v
```

`auction_allocator.py` adds a bidding-based allocation strategy with explicit winning bids and unassigned tasks.

## Implemented

- agent position/capacity state
- task load/location state
- feasibility filtering
- distance scoring
- greedy allocation baseline
- auction-style allocation
- capacity updates
- explicit unassigned reporting
- deterministic CI

## Research boundary

Simulation only. No claim of deployment in a real fleet or optimality under real-world routing constraints.

Related: [Logistics Optimization Lab](https://github.com/Hafiz-IIT/logistics-optimization-lab) · [Port Operations Simulator](https://github.com/Hafiz-IIT/port-operations-simulator)
