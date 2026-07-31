Round f053-r4 — REPAIR (gate confirmation). Findings persist FIRST, then
fix, then the full suite; STOP on any red. No closure work; never merge
anything.

COMMIT A (first, own commit): in .agent/live_review.md replace the R3
"In progress." Steps bullet with f053-r4-1, append f053-r4-2 to
"## Verdicts" after the R2 entry, replace the block from
"- Open: R-0161 (product, Low," through "- Next free ID: R-0162." with
f053-r4-3. cmp proofs.

COMMIT B — fix R-0162 + doc amendments:
- .agent/context.md replaced ENTIRELY with f053-r4-4 (cmp 0 against the
  saved copy).
- docs/agents/planner_reviewer_prompt.md §4 item 11: f053-r4-5 inserted
  directly AFTER the sentence ending "stays with F252." (same
  indentation, part of item 11).
- docs/agents/integration_gate.md step 3: the three lines "parity before
  the base run (share or copy the primary checkout's / `apps/ui/
  node_modules` and `apps/ui/dist` into the base / worktree, or run the
  same install/build there), or attribute" replaced with f053-r4-6.
cmp proofs for all three regions. Mark Done: R-0162 in the commit body.

GATE CONFIRMATION, in this order, STOP at the first red:
1. pytest "tests/ui_server/test_dashboard_contract.py::
   TestLiveReviewAndAgentStateRefs::test_context_md_no_stale_steps" -q
   → must pass.
2. pytest tests/ui_server/test_dashboard_contract.py -q → whole file
   green (guards against a new token regression).
3. pytest -n auto -q → FULL suite; expected 14610 passed, 19 skipped,
   0 failed. Raw tail, exit code, wall time. Any failure: record raw,
   STOP, hand back — no further fixes in this round.
4. pytest tests/docs/ -q → 293.
5. pytest tests/cli/test_golden_path.py -q → 42.

Handback per docs/agents/handback_template.md: per-commit tables,
item-status table (A, B, gate 1-5), authored-text proofs (sha256sum +
saved-copy cmp + applied-region cmp), full-suite raw tail + wall clock.
Do NOT write ## Verdicts beyond applying f053-r4-2 verbatim. Then await
the reviewer. Closure is R5, its own round — the reviewer opens it only
after this gate confirms green.
Authored texts f053-r4-{1..6} (sha256 verified before use, saved
verbatim under .agent/authored/, applied by copy).
OUTCOME: executed
