# Architecture

Agent state + task set → feasibility filter → distance score → assignment → capacity/location update → unassigned-task report.

## Invariants
1. An agent cannot receive load above remaining capacity.
2. Every assigned task maps to exactly one agent.
3. Unassignable tasks remain explicit.
