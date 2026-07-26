# Plan — F046 Multi-cycle loop

## Goal
Remedy works in bounded cycles: check should_stop → execute ready batch →
verify → persist, repeated until all_green, budget_exhausted,
deadline_reached, stopped_by_operator, or blocked. Five-cycle fixture
proves every stop cause; each cycle leaves its own evidence record;
DEFAULT stays one cycle until the F075 gate.

## Checklist
- [x] Setup: Open PR Gate (#151 merged), branch, STATUS claim, state files
- [x] T001 loop skeleton + terminal-status matrix + five-cycle fixture
- [x] T002 cycle evidence + CLI/config + single-pass regression
- [x] Integration gate
- [ ] Closure

## Current Step
Closure — evidence job, review package, Built State, STATUS line, PR
#152 finalized. NOT merged (Open PR Gate at next feature start).

## Next Steps
Reviewer verdict on the integration gate, then Closure (evidence job,
review package, Built State in T1_F046.md, authored STATUS line).

## Risks
- Conductor must wrap existing parts (A6) — no parallel executor.
- Pre-existing full-suite nondeterminism (backlog F135/F052).
