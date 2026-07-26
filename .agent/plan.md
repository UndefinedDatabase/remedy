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
- [ ] Integration gate
- [ ] Closure

## Current Step
Round 1 handed back for review (Setup+T001+T002 built and verified).
Next expected action: reviewer verdict in .agent/live_review.md, then the
integration gate. Closure is a later step.

## Risks
- Conductor must wrap existing parts (A6) — no parallel executor.
- Pre-existing full-suite nondeterminism (backlog F135/F052).
