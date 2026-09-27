# Research agenda

## Central question
**When does a nearest-feasible multi-agent allocator fail badly enough to justify learned or optimization-based coordination?**

## Hypotheses
### H1
Greedy nearest assignment performs reasonably under sparse balanced demand but degrades under clustered/high-load demand.

### H2
Task ordering materially changes unserved demand when capacity is tight.

### H3
Global optimization or MARL should show the largest gains in adversarial distributions rather than easy random cases.

## Experiments
1. Compare random vs load-descending task order.
2. Generate clustered and uniform task distributions at varying load/capacity ratios.
3. Benchmark greedy results against a future assignment-optimization baseline.

## Metrics
- unassigned-task rate
- total travel distance
- capacity utilization
- assignment imbalance
- regret vs future optimal baseline

## Historical/candidate paper lineage
- **Multi-Agent Coordination via Linear Statistical Models and Reinforcement Learning**
- **Scalable Architectures for Distributed Intelligent Agents**

Research directions only; not publication claims.
