# Live Review — F115 Prompt breakdown & cost report

> Round-by-round review record for F115, reset at the feature claim. The F111
> record is preserved in git history at its closure commit 98a49b5c. Finding
> IDs continue monotonically across features and are never renumbered.

## Steps
R1 claim, state reset and shape inventory → T001 manifest-alongside-actuals
persistence with backfill tolerance → T002 aggregation queries, the pure
renderer and its goldens → T003 CLI, period comparison and json schema →
integration gate → closure.

## Findings

- R-0320 — Low — carried forward from the F111 closure-candidates file under
  the disk-vehicle rule (docs/roadmap/STATUS_closure_protocol.md,
  "Closure-candidate findings"). A stop reason no code can ever emit:
  `STOP_REASONS` in `packages/orchestration/builder_bridge.py` declares
  `stale_diff_context`, and a repo-wide grep over every `.py` file finds that
  string in exactly one place — the frozenset itself. Nothing raises it,
  nothing tests it, nothing reads it. It predates the F111 branch (it is
  present at the merge base 4e0b762e), so it was not an F111 defect and was
  deliberately not fixed there. It is not fixed in F115 either: AGENTS.md bars
  mixing an unrelated fix into a feature branch, and F115 opens the token
  ledger and the report renderer, not the builder bridge. The remedy — wire it
  to the condition it names, or delete it — is a one-commit change that
  belongs to whichever feature next has a legitimate reason to open
  `builder_bridge.py`. Recording it here keeps it findable after
  `.agent/candidates.md` is emptied, which is the whole point of the
  carry-forward rule. OPEN.

- R-0321 — Low — `.agent/f115_inventory.md` says "only four of the eight
  `build_trace_entry` call sites pass `composed_prompt`". The count of
  non-test call sites is SEVEN, not eight: `intake.py:135`,
  `flight_plan.py:181`, `orchestrator_loop.py:920`, `mission_compiler.py:280`,
  `pingpong_loop.py:2824`, `pingpong_loop.py:3010` and
  `apps/cli/commands/job.py:236`. The inventory's own enumeration names four
  that pass and three that do not, which is seven, so the number contradicts
  the list directly above it. Every individual citation is correct and the
  round's conclusion is unaffected — this is an arithmetic slip in prose, not
  a bad reading of the source, and it is registered rather than waved through
  because a wrong total in an inventory is exactly the kind of number a later
  round quotes without re-counting. Fix: change "eight" to "seven" in that
  sentence and nothing else. OPEN.

- R-0322 — Medium — the suite is RED at this branch's merge base. Five ids in
  `tests/orchestration/test_role_conventions.py` fail, every one a
  `[reviewer]` parametrization, each raising `PromptSegmentError: prompt
  segment 'reviewer_conventions' is over its token cap: 954 tokens estimated,
  cap 800` before any assertion in the test runs. Measured by the reviewer at
  the R2 gate: `5 failed, 21 passed in 0.14s`. It is NOT an F115 defect —
  `docs/agents/reviewer_conventions.md` was last touched at a85e82f5 on
  2026-08-12, before this branch existed, and
  `git diff --name-only 0d6c97aa..HEAD` over that path and over
  `prompt_facts.py` is empty. It is the same class F111 recorded as R-0286 and
  attributed at its integration gate in both trees. It is registered here
  rather than inherited silently because F115's own integration gate will meet
  it, and a gate that has to rediscover a known red spends a round proving
  something already known. It is deliberately NOT fixed on this branch:
  AGENTS.md bars mixing an unrelated fix into a feature branch. The fix
  belongs to a round that legitimately opens the conventions document or the
  cap. OPEN.
