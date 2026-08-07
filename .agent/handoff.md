# Handoff — F254 R11, closure part 1, COMPLETE

Feature **T2_F254 — model alias table & dead-model doctor check**, branch
**`feature/f254-model-alias-table`**, pushed. SPLIT round, worker subagent.
`.agent/STOP` absent at round start and re-checked before every commit.

## THE FOUR CLOSURE VALUES (the reviewer authors the STATUS line from these)
- Evidence job id: **`f254-closure`**
- Package: **`remedy-review-20260807-204305-READY_FOR_REVIEW.zip`**
- SHA-256: **`1b4995fa9e3ab76f7be8398be66ed69ec47e99f6e825d16cc97aa826a95a05c0`**
- Accepted HEAD: **`b71c9bdd93cbeb21d4b98842cdf6baa998c3ac26`**

## Commits, in order
`b71c9bdd` A persist the R10 verdict + replace plan.md (ACCEPTED HEAD) · E =
this handoff commit. B, C and D produce no commit by design.

## Item status
| Item | Status | Reason |
|---|---|---|
| A content commit | done | `b71c9bdd` |
| B preconditions | done | clean tree, integrity PASS, pushed |
| C evidence job | done | `f254-closure`, dir outside the repo |
| D review zip | done | READY_FOR_REVIEW at `b71c9bdd` |
| E rewrite handoff | done | this file |

## Changed files (`git diff --numstat 0c44cd6f..HEAD`, item A)
| Path | + | - |
|---|---|---|
| .agent/authored/f254-r11-1.md | 103 | 0 |
| .agent/authored/f254-r11-2.md | 47 | 0 |
| .agent/live_review.md | 63 | 13 |
| .agent/plan.md | 36 | 35 |

## Verification (real commands, real exit codes)
Transport: `cmp` vs the reviewer's scratchpad originals **exit 0 x2**, sha256
matching the block; `cmp .agent/plan.md .agent/authored/f254-r11-2.md` **0**.
Both live_review pairs REWRITE: pre FROM **1x** → post FROM **0x**, TO **1x**.
State contracts: plan.md **47** lines (<50) · `^## Goal` **1** · `^## Next
Steps` **1** · live_review 4-section grep **4** · `- R6` inside `## Steps`
**1**. Round gate exit **0**, **142 passed**; canary golden path exit **0**,
**42 passed**. `remedy integrity check --json` **passed true**, 5/5 pass,
fail_count 0, no non-pass check. `git status --porcelain` **empty** before and
after both artifact builds · `git worktree list` **primary only** · no
force-push, no PR, no STATUS or README edit.

## Artifact builds (both attempted, both succeeded)
**Evidence job** `create_manual_completion_bundle(review_feature_id="f254")`,
base `fc023265…48cc3` → head `b71c9bdd…`, R1-R11, evidence dir OUTSIDE the
repo: authority 16 · commits 31 · partition 6/6/4 · total_passed **110** ·
verdict **PASS_WITH_RISKS** (operator-attested model warnings only;
unresolved_findings `[]`, missing_evidence `[]`). Three SCOPED suites with
real `--collect-only` node ids and `len(node_ids) == selected`: model_aliases
**24** · dead_model_list **23** · worker_facade_cmd **63**, each exit 0 / 0
failed. No full-suite node-id list recorded (protocol pitfall d).
**Review zip** `bash scripts/make_review_zip.sh --evidence-dir <scratchpad>`
exit **0** → **READY_FOR_REVIEW**, evidence authoritative, alignment PASS,
2151 members, `testzip()` None, ready_gate_matrix ok / blocking_reasons `[]`.
`committed_review_subject` spans `fc023265…48cc3` → `b71c9bdd…c26`, 31
commits / 52 files. Zip gitignored (`.gitignore:223`); evidence never
committed.

## Findings
R-0211…R-0217 all Done. **Open findings: 0. Next free ID: R-0218.**
`.agent/candidates.md` still holds the R-0214 handoff-cap amendment — a
block condition at the NEXT feature claim, not at this closure.

## Deviations, declared
None. No scope widened, no reviewer-authored text edited. This file is 76
lines, over the 60-line cap with no section dropped — R-0214's eighth
measurement, caused by the four closure values plus the two artifact records.

## Next expected action
Reviewer gates `b71c9bdd..HEAD` (R11), then authors the R12 STATUS line from
the four values above. R12 = closure part 2: STATUS `[~]`→`[x]` plus the
README capability sync in the SAME commit (R-0154), LAST on the branch, then
`gh pr create` — NOT merged in the session that creates it.
