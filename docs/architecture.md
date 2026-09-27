# Architecture

```mermaid
flowchart LR
    N0[agents + tasks] --> N1
    N1[feasibility] --> N2
    N2[distance] --> N3
    N3[assignment] --> N4
    N4[state update] --> N5
    N5[unserved tasks]
```

## Agent state
Each agent has a name, 2-D position, and remaining capacity.

## Task state
Each task has a location and load requirement.

## Feasibility
Only agents with sufficient remaining capacity are candidates.

## Greedy coordinator
Chooses the nearest feasible agent, then updates capacity and position.

## Principle
Start with a transparent coordination baseline whose failures can be measured before adding learning.
