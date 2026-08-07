# Handoff — F254 R10, R9's unpaid remainder, COMPLETE

Feature **T2_F254 — model alias table & dead-model doctor check**, branch
**`feature/f254-model-alias-table`**, HEAD **`439a9d5e`** + this handoff
commit, pushed. SPLIT round, worker subagent. `.agent/STOP` was absent at
round start and re-checked before every commit — never present.

## Commits, in order
`fd251be5` A persist R9 verdict + re-author plan · `b09728bf` B built
state on the feature file · `439a9d5e` C gate evidence · D = this file.

## Item status
| Item | Status | Reason |
|---|---|---|
| A persist R9 verdict, replace plan.md | done | `fd251be5` |
| B Built State on T2_F254.md | done | `b09728bf`, receipt f254-r10-3 |
| C gate evidence in .agent/gate_f254_r9/ | done | `439a9d5e` |
| D rewrite handoff | done | this file |

## Changed files (`git diff --numstat f3eb61ba..HEAD`, A+B+C)
| Path | + | - |
|---|---|---|
| .agent/authored/f254-r10-1.md | 115 | 0 |
| .agent/authored/f254-r10-2.md | 46 | 0 |
| .agent/authored/f254-r10-3.md | 102 | 0 |
| .agent/gate_f254_r9/attribution.txt | 31 | 0 |
| .agent/gate_f254_r9/branch_failed.txt | 0 | 0 |
| .agent/gate_f254_r9/branch_run.txt | 42 | 0 |
| .agent/live_review.md | 62 | 8 |
| .agent/plan.md | 14 | 13 |
| docs/roadmap/features/T2_F254.md | 74 | 0 |

## Verification (real commands, real exit codes)
Transport: `cp` then `cmp` vs the reviewer's scratchpad originals —
**cmp exit 0 ×3**; sha256 matches the block exactly (`911efb18…891b18`
r10-1, `a3c1d259…76a71b` r10-2, `4a1390d0…d89878` r10-3).
`cmp .agent/plan.md .agent/authored/f254-r10-2.md` **exit 0**.
Pairs, applied byte-exact by the scratchpad applier, under their declared
shape: r10-1 PAIR 1 REWRITE pre FROM 1x → post FROM 0x / TO 1x; PAIR 2
REWRITE pre FROM 1x → post FROM 0x / TO 1x. r10-3 PAIR 1 **APPEND** pre
FROM 1x → post FROM **1x** (0x unattainable), all **71 TO-ONLY lines 1x**.
State contracts: `wc -l .agent/plan.md` **46** (<50) · `^## Goal` **1** ·
`^## Next Steps` **1** · live_review 4-section grep **4** · `- R6`
bullets inside `## Steps` **1**.
**Integration gate, branch-only per DECISION D14** — `python3 -m pytest
-n auto -q` at head `b09728bf` (clean tree, A+B already committed):
**exit 0**, **16016 passed, 19 skipped in 162.54s (0:02:42)**, wrapper
wall clock **163s**. `grep '^FAILED'` → **0 lines**, so
`branch_failed.txt` is empty and **no attribution was owed**; stated so
in attribution.txt together with D14's no-base-run and R7's zero
branch-only failures. Log written OUTSIDE the worktree during the run
and copied in after (R-0176); all files `.txt` (R-0169). **No base
worktree created; no run at the merge base.** R-0217c is now PAID.
Docs gate (commit B touches docs/roadmap/**) `tests/docs/ -q` exit **0**,
**294 passed** (run pre-commit and re-run at HEAD, same result).
Round gate exit **0**, **142 passed**. Canary
tests/cli/test_golden_path.py exit **0**, **42 passed**.
`git status --porcelain` **empty** · `git worktree list` **primary only**
· `git diff f3eb61ba..HEAD -- .agent/authored/f254-r9-3.md` **no output**
(superseded receipt untouched) · pushed `f3eb61ba..439a9d5e`, exit 0.
No force-push, no history rewrite, no PR, no STATUS edit, no README edit.

## Findings
R-0211…R-0217b Done. **R-0217c: PAID** — `.agent/gate_f254_r9/` exists on
the branch with the raw branch-run evidence. **Open findings: 0. Next
free ID: R-0218.** `.agent/candidates.md` still holds the R-0214
handoff-cap amendment — block condition at the NEXT feature claim.

## Deviations, declared
None. All four bundle items were completed as specified; no scope was
widened and no reviewer-authored text was edited.

## Next expected action
Reviewer gates `fd251be5..HEAD` (R10). Then **R11 = closure** per
docs/roadmap/STATUS_closure_protocol.md: evidence job (feature-scoped,
fresh id) → FRESH review zip (a zip failure is a closure BLOCKER) →
closure commit with STATUS `[~]`→`[x]` **plus** the README capability
sync in the SAME commit (R-0154), last on the branch → `gh pr create`,
NOT merged in the session that creates it.

Length: **82 lines**, over the 60-line cap and under the 100-line
allowance. Declared, no section dropped — R-0214's seventh measurement.
