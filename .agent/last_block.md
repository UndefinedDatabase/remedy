You are the worker (Window 2), fresh session. Feature: F052 —
Self-healing test rounds. Round id: f052-r1 (LARGE bundle). Read
AGENTS.md and docs/roadmap/features/T1_F052.md COMPLETELY before any
code. Save THIS ENTIRE block to .agent/last_block.md first
(OUTCOME: pending → executed at handback). Hash-stamp rule is in force:
every applied string below travels in a sha256-stamped block.

STEP 0 — OPEN PR GATE
gh pr list --state open --json number,headRefName,isDraft
Reviewer verified this is empty; if NOT empty now → STOP, hand back.
git checkout main && git pull --ff-only

STEP 1 — BRANCH + CLAIM (commit A)
git checkout -b feature/f052-self-healing-rounds
Save the three authored texts below to .agent/authored/<name>.md,
verify each sha256 BEFORE use (wrapped lines: rejoin with a single
space, re-hash; persistent mismatch = STOP).
- Replace the unique STATUS.md line "- [ ] F052 — Self-healing test
  rounds" with the single line of f052-r1-3.md (grep -c proofs: old
  1→0, new 0→1; touch no other line).
- Copy f052-r1-1.md over .agent/live_review.md, f052-r1-2.md over
  .agent/plan.md (cmp -> 0 proofs).
Commit STATUS.md + .agent/{live_review,plan,last_block}.md +
.agent/authored/f052-r1-*.md as:
chore(f052): claim F052 + state reset
Push -u origin feature/f052-self-healing-rounds.

── STEP T001–T002/2 — F052 (LARGE) ────────────────────────────
Goal:        Whole feature except closure: verify-failure → bounded
             auto-repair through the EXISTING repair loop.
Bundle (strict order, stop-on-red between items):
  1. INSPECT (no code, findings go in the handback): where a cycle's
     verify failure surfaces; the exact function/entry point by which
     the EXISTING ping-pong repair loop accepts findings; where its
     round cap is configured; how budgets count repair calls; the
     postmortem test-failure class name. If NO existing repair path
     is reachable from cycle verify, STOP and hand back — that is a
     spec finding, not something to solve by building a new loop.
  2. T001: verify→findings→repair trigger + cap (config key
     cycles.repair_rounds, default 2) + healed path. Findings payload
     from the test output: failing test ids, tail of failure text,
     this cycle's changed files as hint. Re-run verify after each
     repair round. Healed → cycle completes normally; cycle evidence
     records "healed after N repair rounds" and reports show it.
     Fixture: a one-line assertion break heals in round one.
  3. T002: stubborn fixture (fake provider never fixes) → EXACTLY two
     rounds, then the existing test-failure classification; the
     postmortem references the repair-round evidence. Budget
     attribution asserted via actuals. A stop request between repair
     rounds stops cleanly at the existing safe points (assert, don't
     assume). Edge cases (A9): verify failing for non-test reasons
     (missing command, config) → classified config/unknown, NO repair
     rounds; a heal that changed no files records "healed without
     changes (flaky?)".
Change:      Trigger/wiring + tests only. New tests in
             tests/orchestration/test_self_healing_cycles.py.
Constraints: Do-not-touch: the repair loop's internals, flaky-test
             quarantine, review policies. NO new repair entry point —
             any diff adding one will be rejected in review (A6).
             Repair rounds flow through existing fences, budgets,
             stop safe points. Commits small (<500 lines), one
             logical step each.
Done when:   All green with raw tails + exit codes in the handback:
             python3 -m pytest tests/orchestration/test_self_healing_cycles.py -q
             python3 -m pytest tests/orchestration/ -q
             python3 -m pytest tests/docs/ -q            (expect 293)
             python3 -m pytest tests/cli/test_golden_path.py -q (42)
             plus a visible transcript line showing the healed-cycle
             evidence in a status/report rendering.
Handback:    completion report + rewrite .agent/handoff.md per
             docs/agents/handback_template.md (range main..HEAD,
             per-commit changed-files tables, inspect findings from
             item 1, sha256sum output of the three authored files,
             gate transcripts, deviations honest). Flip OUTCOME to
             executed. Commit: chore(f052): handback R1. Push. Do
             NOT create a PR yet — the reviewer orders it after the
             integration gate. Never merge anything.
──────────────────────────────────────────────────────────────

--- BEGIN f052-r1-1 sha256=8ba4dc102c31225686db256ac05863a8cf266a09525d6d936f0339bfc3990c96 ---
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
  In progress.

## Findings
- (none yet)
- Next free ID: R-0158.

## Verdicts
- R1: PENDING (reviewer).
--- END f052-r1-1 ---

--- BEGIN f052-r1-2 sha256=7c57cbadbe37f2dc61111c457fac71370cbf0f116361fc5fbaf137edd62c01d4 ---
# Plan — F052 Self-healing test rounds

## Goal
Trivial test breakage no longer kills unattended cycles: on a cycle
verify failure, up to cycles.repair_rounds (default 2) bounded
auto-repair rounds run through the EXISTING repair loop, verify
re-runs after each round, healed cycles record "healed after N
repair rounds" visibly, stubborn breaks fail after exactly two
rounds with the existing test-failure classification and linked
repair evidence, and repair cost lands on the job budget. DONE per
docs/roadmap/features/T1_F052.md: a one-line break heals in round
one; a stubborn break stops after exactly two rounds with an honest
trail; costs attributed via actuals.

## Next Steps
- R1 (LARGE): inspect repair-loop intake → T001 trigger + cap +
  healed path → T002 stubborn path + budget + stop request.
- Then: integration gate round; closure its own round (never
  bundled).
--- END f052-r1-2 ---

--- BEGIN f052-r1-3 sha256=7c0b8fd0a7679e9bc26f46548733ebf29d3e97d4d33b8a539c0cac0eef67d137 ---
- [~] F052 — Self-healing test rounds
--- END f052-r1-3 ---

OUTCOME: pending
