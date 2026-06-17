# Plan — Steps 2446-2505: Run Replay to Self-Repair Proposal v0

## Goal
Turn run replay analysis into a safe self-repair proposal that a human operator
can approve, deny, or edit before it becomes a Worker prompt.

## Steps
- [x] Phase 1: Architecture doc (docs/run-replay-to-self-repair-proposal-v0.md)
- [x] Phase 2: Core proposal module (packages/orchestration/self_repair_proposal.py)
- [x] Phase 3: Proposal generation from replay (create_self_repair_proposal_from_replay)
- [x] Phase 4: Operator decision flow (approve/deny/edit/convert)
- [x] Phase 5: Storage (save/load/list with atomic writes)
- [x] Phase 6: CLI surface (apps/cli/commands/self_repair_cmd.py)
- [x] Phase 7: Command catalog + run contract (7 commands, 7 contract actions)
- [x] Phase 8: Review bundle / progress / cockpit (self_repair_proposal_summary.json)
- [x] Phase 9: Integrity checks (7 invariants in self_repair_proposal_integrity)
- [x] Phase 10: User guide doc (docs/self-repair-proposal-user-guide-v0.md)
- [x] Phase 11: Targeted tests + lint (49 proposal + 90 bundle + 18 catalog + 64 dogfood + 119 contract = all pass)
- [x] Phase 12: Full suite (6734 passed, 0 failed, 8 skipped)
- [ ] Self-review + commit + push + PR

## Hard rules
No provider execution; no auto-apply/approve/PR/git; no shell=True; no secret storage;
no raw log/prompt/transcript leaks; no MemPalace/embeddings.
