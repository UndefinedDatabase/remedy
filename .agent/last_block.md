Round f053-r5 — REPAIR 2 (gate confirmation, second attempt). Findings
persist FIRST, then the fix, then gate steps 3-5; STOP on any red.
No closure work; never merge anything.

COMMIT A (first, own commit): in .agent/live_review.md replace the R4
"In progress." Steps bullet with f053-r5-1, append f053-r5-2 to
"## Verdicts" after the R3 entry, replace the block from
"- Open: R-0162 (process, Low," through "- Next free ID: R-0163." with
f053-r5-3. cmp proofs.

COMMIT B — corrected fix:
- .agent/context.md replaced ENTIRELY with f053-r5-4 (whole-file cmp 0
  against the saved copy). Pre-validated against all 13 real-file
  assertions.
- docs/agents/planner_reviewer_prompt.md §4 item 11: replace the
  six-line block beginning "    The same contract class covers
  `.agent/context.md`: the" (the applied r4-5 text, starting on the line
  after "stays with F252.") with f053-r5-5.
cmp proofs for both regions. Mark Done: R-0162 in the commit body.

GATE CONFIRMATION, in this order, STOP at the first red:
1. pytest tests/regression/test_resource_safety.py
   tests/ui_server/test_dashboard_contract.py -q → both context.md
   reader files green.
2. pytest -n auto -q → FULL suite; expected 14610 passed, 19 skipped,
   0 failed. Raw tail, exit code, wall time. Any failure: record raw,
   STOP, hand back.
3. pytest tests/docs/ -q → 293.
4. pytest tests/cli/test_golden_path.py -q → 42.

Handback per docs/agents/handback_template.md: per-commit tables,
item-status table (A, B, gate 1-4), authored-text proofs (sha256sum +
saved-copy cmp + applied-region cmp), full-suite raw tail + wall clock.
Do NOT write ## Verdicts beyond applying f053-r5-2 verbatim. Then await
the reviewer. Closure is R6, its own round — the reviewer opens it only
after this gate confirms green.
Authored texts f053-r5-{1..5} (sha256 verified before use, saved
verbatim under .agent/authored/, applied by copy).
OUTCOME: executed
