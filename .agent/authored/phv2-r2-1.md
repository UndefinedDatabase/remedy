# Live Review — Process-Hardening v1+v2 (chore rounds)

Branch: chore/process-hardening-v2 (PR #155)
LAST_REVIEWED_SHA: fca6b12
Finding IDs continue monotonically; next free ID: R-0150.
The F046 ledger is archived in git history.

## Findings

- R-0148 · Medium · PH round 1 — RESOLVED (PH-2, commit b586e5c).
  Transport-wrapped index row; full entry in git history (PR #154).

- R-0149 · Medium · PH round 1 — RESOLVED (PH-4, 86a55b8..fca6b12)
  Handback-template cap collision plus final-commit self-reference.
  Operator ruling (a) applied in full: AGENTS.md handoff cap is now
  "≤60 lines (≤100 when per-commit tables of >5 commits require it —
  sections are never dropped)", mirrored in split_workflow.md; the
  self-reference grouped-table rule is codified in
  handback_template.md; the sha256 BEGIN-marker transport guard is
  codified in split_workflow.md (protocol paragraph + bootstrap
  bullet) and planner_reviewer_prompt.md item 9. Reviewer verified
  all seven authored texts byte-identical to the authoring originals
  (cmp) and all six superseded wordings gone. Resolved by this
  reviewer-authored entry.

## Verdicts

- PH-4 (a1a0db7..fca6b12): PASS — issued by the reviewer after
  independent verification: 7/7 committed authored files
  byte-identical to the reviewer's originals (cmp); proof script
  re-run — 7 applications + 6 gone-checks all OK, exit 0; canary
  re-run 42 passed; tree clean; PR #155 untouched. First live run of
  the sha256 receipt guard: 7/7 marker hashes matched. Accepted
  documented deviation: one wording-identical re-wrap of the
  split_workflow "Purpose" paragraph (verified word-by-word).
  Verification tier: round gate (scoped) + canary.
  LAST_REVIEWED_SHA = fca6b12. Merge of PR #155 instructed (operator
  ruling relay 2026-07-27: the amendment completes before F048).
