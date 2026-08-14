# Plan — F077 Autonomy watchdog · CLOSED

Branch: feature/f077-autonomy-watchdog. F077 is `[x]` in docs/roadmap/STATUS.md
as of this commit, which is the LAST on the branch. Next free finding id:
R-0403. Open findings: THIRTY-TWO, all Medium or Low, none a blocker — the
verdict is PASS_WITH_RISKS and the ids are named in the closure PR and in
`.agent/live_review.md`, which is the source of truth.

## Goal
Continuous operation gets a tripwire independent of the thing it watches. A
watchdog reads the orchestrator loop's ledger and on no-progress repetition, a
burn-rate anomaly or goal drift it PAUSES the mission and raises one decision
per trip class carrying the evidence triple. It stops; it never repairs.
Thresholds live in config, not code. DONE: T001, T002 and T003 are built,
tested and green, the integration gate ran on the branch and at the merge base
with zero branch-only failures, and `docs/system/autonomy-watchdog-v1.md`
records the built state.

## Current Step
None. The feature is closed and the PR is open and UNMERGED by design: it
merges at the next feature's start via the AGENTS.md Open PR Gate, which is the
operator's manual-review window. The operator may merge it manually at any time.

## Next Steps
1. A NEW session, per docs/agents/self_drive_protocol.md Phase 1: rule 1
   re-reads `.agent/STOP` from disk FIRST, then rule 2 runs the Open PR Gate,
   which merges this feature's PR before any new branch exists.
2. Then Rule A5 claims the next feature in STATUS order: F082 — Self-benchmark.
3. `.agent/candidates.md` is empty, so no candidate registration is owed at that
   claim.

## Risks
- A mission resumed AFTER its watchdog decision is answered still carries the
  tripping run in its ledger and trips again for all three tripwires, so
  `mission resume` buys exactly one iteration. DECISION F077 D12 does not
  address the re-trip; it is recorded in the feature file's Built State as a
  known limit and no feature owns it yet.
- R-0396's amendment target, docs/agents/integration_gate.md, is outside this
  feature's change set, so every future integration gate reproduces the eight
  phantom ui_server base failures until some feature owns that doc.
