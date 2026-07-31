# Live Review — F052 Self-healing test rounds (Tier 1)

Branch: feature/f052-self-healing-rounds
Scope: cycle verify failure → bounded auto-repair via the EXISTING
repair loop (no second mechanism, A6): findings payload from test
output, cap cycles.repair_rounds (default 2), healed path with a
visible evidence line, stubborn path with the existing test-failure
classification + linked repair evidence, budget attribution, safe-
point stop between rounds (docs/roadmap/features/T1_F052.md).

## Steps
- R1 (LARGE): claim + state reset + inspect report + T001 + T002.
  Done.
- R2: persist R1 verdict + DECISION D1 + feature-file amendment +
  Built State + integration gate per docs/agents/integration_gate.md
  (R-0155 amendment in force). Done.
- R3: persist R2 verdict; register R-0158 + R-0159; fix R-0158
  (integration_gate.md path correction); closure stays its own
  round. Done.
- R4: closure per docs/roadmap/STATUS_closure_protocol.md v4:
  preconditions, evidence job, READY zip, evidence commit, then ONE
  final commit = STATUS [x] + README sync + final .agent state.
  In progress.

## Findings
- DECISION D1 (2026-07-30, §4.7, reviewer): the executing repair
  loop F052 triggers is builder_bridge.run_builder_bridge_loop, NOT
  the ping-pong loop the feature file's "How it fits" names —
  ping-pong is unreachable from run_cycles (own-reviewer findings,
  no injection seam, JobPlan world) and the core-Job repair_loop
  v0/v1/v2 modules are human-gated proposal flows by contract.
  Alternatives considered: adapt ping-pong (rejected: a new seam is
  a new mechanism, A6); a cycle-local loop (rejected: A6, verbatim).
  Reversal: any later relay may re-route the trigger once ping-pong
  gains a findings-injection seam; the repair= seam in run_cycles
  keeps that a one-function swap.
- Resolved: R-0158 (process, Low) 2026-07-30: integration_gate.md
  now names `apps/ui/node_modules` (+ `apps/ui/dist`) as the parity
  targets, notes the ROOT `node_modules` is only a `.vite` cache,
  and folds the non-restorable `.git`-directory class (R-0159) into
  the attribution rule.
  Done: R-0158 (commit f9dadc0 — the doc diff is the evidence).
- Open: R-0159 (process, Low): the 2 ids in
  tests/cli/test_self_dogfood_execution_cli.py cannot pass in ANY
  linked worktree — self_dogfood_execution.current_branch() reads
  Path(".git")/"HEAD", and a worktree's .git is a regular FILE, so
  the guard answers main_branch_unsafe/blocked. They land in
  comm -23 on every gate run. Fix: read the real HEAD (e.g. via
  git rev-parse) — its own reviewer-gated micro-round; documented
  Low risk until then.
- Next free ID: R-0160.

## Verdicts
- R1: PASS (reviewer, 2026-07-30). Range 92c998c..21638c6. All 3
  authored texts cmp 0 disk-to-disk; STATUS claim one line exactly.
  Reviewer's own runs: test_self_healing_cycles 50 passed;
  tests/orchestration 8788 passed, 7 skipped (-n auto, 1:57);
  tests/docs 293; canary 42. Mutation check in a throwaway worktree
  (round cap < mutated to <=) killed by 3 tests incl.
  test_exactly_two_rounds_not_one_not_three; worktree removed +
  pruned. A6 verified: no repair-loop internals touched, trigger
  reuses builder_bridge + repair_context intake (DECISION D1).
  Deviations 1-4 accepted (4-commit split; CycleLimits field default
  0 vs config 2, deliberate + documented; budget attribution proven
  on the default seam; bridge loop monkeypatched in unit round —
  real behavior belongs to the gate). LAST_REVIEWED_SHA = 21638c6.
- R2: PASS — INTEGRATION GATE PASS (reviewer, 2026-07-30). Range
  21638c6..d410ce5. All 4 authored texts cmp 0 disk-to-disk; Built
  State verified strictly factual against the r1 diff; amendment
  placed at the end of How it fits. Gate: reviewer's own full run
  at d410ce5 — 14486 passed, 0 failed, 19 skipped, 2:11 — makes the
  branch-only failure set empty by construction; the worker's
  branch run matches (14486/0/19, 2:01). comm -13 = 0. comm -23 =
  2, attributed by direct evidence and REPRODUCED by the reviewer
  (worktree .git is a regular file → dogfood guard unsafe → 2
  failed; primary checkout 6/6 green). Parity per the R-0155
  amendment caught the amendment's own wrong path (ROOT
  node_modules holds only .vite; the real tree is
  apps/ui/node_modules) → R-0158 registered. New suite baseline
  14486/0/19 (+51 = 50 self-healing + 1 count pin). Wall clock
  under budget, no perf pass. LAST_REVIEWED_SHA = d410ce5.
- R3: PASS (reviewer, 2026-07-31). Range d410ce5..7262f5b. All 5
  authored texts verified against the recorded BEGIN digests by the
  reviewer's own sha256sum recompute (the reviewer scratchpad died
  between rounds — the digest fallback per project practice, not a
  worker fault); registrations and the R-0158 resolution applied
  byte-exact, Done sha f9dadc0 confirmed against the real doc diff.
  integration_gate.md paragraph replacement verified: parity
  targets corrected to apps/ui/node_modules + apps/ui/dist, ROOT
  node_modules named a .vite cache, non-restorable .git-directory
  class folded into the attribution rule. R-0159 deliberately Open
  (documented Low). Reviewer's own gates: tests/docs 293, canary
  42. Closure preconditions met: latest verdict PASS, all findings
  Resolved or documented risk, Built State current, tree clean.
  LAST_REVIEWED_SHA = 7262f5b.
