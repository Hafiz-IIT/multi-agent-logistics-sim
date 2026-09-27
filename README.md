# Multi-Agent Logistics Simulator

A simple coordination simulator where delivery agents compete for tasks under capacity and distance constraints.

## Implemented
- agents with location/capacity
- tasks with location/load
- greedy nearest-feasible assignment
- capacity updates
- unassigned-task reporting
- deterministic tests

## Run
```bash
python -m unittest discover -s tests -v
python multi_agent_logistics_sim.py
```

## Scope
This is a coordination toy model for studying allocation logic. It is not a trained multi-agent RL system or real dispatch product.
