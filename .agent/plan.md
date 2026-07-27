# Plan — Process-Hardening v1 (chore round, no feature)

## Goal
Move accepted process lessons (F016..F047) from session memory into the
workflow docs. Docs + index only. No production code, no tests, no
STATUS.md feature lines.

## Checklist
- [x] Part 0: branch chore/process-hardening-v1 off main; plan.md
- [x] Part 1: persist 10 reviewer-authored texts to .agent/authored/
- [x] C1 docs/agents/handback_template.md (new, from phv1-r1-1)
- [ ] C5 docs/agents/integration_gate.md (new, from phv1-r1-2)
- [ ] C2 split_workflow.md += phv1-r1-3, phv1-r1-4
- [ ] C3+C6 planner_reviewer_prompt.md += phv1-r1-5, r1-6 (replace), r1-7
- [ ] C4 AGENTS.md += phv1-r1-8
- [ ] IDX docs/README.md += phv1-r1-9, phv1-r1-10
- [ ] Part 3: proof script PROOFS: PASS + golden-path canary
- [ ] PR into main (created, NOT merged)

## Current Step
C1 applied (handback_template.md). Next: C5.

## Next Steps
Apply each target area as its own small commit in the order above, full
self-review loop + Commit Gate before each, push after committing. Then
run the proof script and the golden-path canary, then open the PR.

## Risks
- D1: PR #153 (F047 closure) stays open and untouched this round; it
  merges at the next feature's start (operator process-hardening
  directive 2026-07-27).
- D2: branch is chore/* not feature/* (same directive).
- D3: this round's PR is created but not merged in this block.
- phv1-r1-10 line 2 of the second table row appears hard-wrapped
  ("...by paste\nblocks) |"), which breaks the markdown table row. Saved
  and applied verbatim per the no-fix rule; reported as a suspected
  authored-text error.
