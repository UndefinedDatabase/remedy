# Plan — Process-Hardening v2 (R-0149 amendment round, no feature)

## Goal
Apply the operator ruling on R-0149 to the workflow docs: (a) handoff cap
≤60 lines, ≤100 when per-commit tables of >5 commits require it; the
self-reference grouped-table rule; the sha256 BEGIN-marker transport
guard. Docs only. Operator directive 2026-07-27 (ruling relay).

## Checklist
- [x] Part 0: branch chore/process-hardening-v2 off main; plan.md
- [x] Part 1: persist 7 authored texts, 7/7 sha256 verified; R-0149 ruling
      appended to .agent/live_review.md
- [x] A1 docs/agents/handback_template.md (full replace, phv2-r1-1)
- [x] A2 AGENTS.md handoff Purpose paragraph (phv2-r1-2)
- [x] A3+A4+A5 split_workflow.md (phv2-r1-3, r1-4, r1-5)
- [x] A6 planner_reviewer_prompt.md §4 item 9 (phv2-r1-6)
- [x] Part 3: proof script PROOFS: PASS + golden-path canary
- [x] PR #155 into main (created, NOT merged)
- [x] PH-5 Part 1: phv2-r2-1 hash-verified; live_review.md replaced
- [ ] PH-5 Part 2: final handoff, push
- [ ] PH-5 Part 3: merge PR #155, checkout main, pull --ff-only

## Current Step
PH-5 merge round. PH-4 verdict PASS persisted, R-0149 RESOLVED. Next and
last action: merge PR #155. Nothing is committed after the merge.

## Next Steps
None on this branch. Next session: Open PR Gate merges PR #153 (F047),
then A5 → F048.

## Risks
- D1: PR #153 (F047 closure) stays open and untouched; it merges at the
  F048 start (operator directive 2026-07-27).
- D2: branch is chore/* not feature/* (same directive).
- D3: this round's PR is created but NOT merged in this block.
- The GONE checks make each replacement destructive by design — the old
  wording must not survive anywhere in the target file.
