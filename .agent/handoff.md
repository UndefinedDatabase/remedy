# Handoff — F254, session close (S4 self-drive rehearsal)

Read cold: the ONLY return channel out of a session that ENDED. Feature
**T2_F254 — model alias table & dead-model doctor check**, branch
**`feature/f254-model-alias-table`**, HEAD **`00703e8e`**, pushed, tree
clean. **BUILT and gate-green but NOT CLOSED**: the session hit its
capacity limit at R8, and per self_drive_protocol.md **G7** a session
ending at its limit with a written handoff is a **SUCCESS**. All rounds
SPLIT — reviewer in the main session, one delegated worker subagent per
round; the single-writer rule held.

## Round ledger R1-R8
| R | What it did | Verdict |
|---|---|---|
| R1 | Open PR Gate (merged PR #185), cut branch, claim `[~]`, reset .agent state | PASS |
| R2 | Alias module `packages/orchestration/model_aliases.py`, 5 built-in ids routed | PASS |
| R3 | Route last 3 built-in ids (2 Ollama providers, `ollama.model`), amend Acceptance | PASS |
| R4 | Known-dead list `scripts/dead_models.json`, loader, config extension, tests | PASS |
| R5 | Wire the dead-model check into `remedy doctor core` as an advisory warning | PASS |
| R6 | Fix warning verbosity + miscount, add repo-scan pin, write and index the doc | PASS |
| R7 | Persist R6, fix R-0216, then the integration gate — full suite | PASS, gate GREEN |
| R8 | Persist R7, register R-0217, write this handoff — session-closing round | PENDING (this handback) |

## Commit range and PR state
Merge base with `main`: `fc023265` (the PR #185 merge commit). Branch
range **`ef71d83e`..`00703e8e`** — first commit after the merge base
through HEAD — **23 commits**, 40 paths: 20 authored receipts, 5 `.agent`
files, 4 docs (incl. the `STATUS.md` `[~]` claim and the `docs/README.md`
index entry), 8 source files, 3 new test files.
**PR #185** (`feature/selfdrive-skill` → `main`, the S1+S2 self-drive
skill) is **MERGED**, `mergedAt` 2026-08-07T14:26:32Z, at R1's Open PR
Gate. **NO PR exists for this branch**: `gh pr list --head
feature/f254-model-alias-table --state all` → `[]`, `gh pr list --state
open` → `[]`. The F254 PR is the closure round's job.

## Integration gate (R7) — three real runs
| Run | Where | Result (`python3 -m pytest -n auto -q`) |
|---|---|---|
| Branch | repo root @ `0ea95c88` | exit 1 · 1 failed, 16015 passed, 19 skipped · 128s |
| Base | worktree @ merge-base `fc023265` | exit 1 · 5 failed, 15950 passed, 19 skipped · 147s |
| Reviewer, independent | repo root @ `a310cd13` | **16016 passed, 19 skipped, 0 failed** · 124s |

**Branch-only failures: ZERO.** The one shared failure
(`test_product_smoke.py::test_no_zombie_processes_after_every_outcome`)
exists at the base and passes serially — xdist flake. The four base-only
failures were the `apps/ui/dist` build-output class (R-0155/R-0158),
measured rather than waved away; the reviewer's third run settles it.
**R-0217c: the gate LOGS did not survive their session's scratchpad** —
the R7 block forbade a sixth path, blocking integration_gate.md §2's own
instruction to copy them into `.agent/gate_*`. The numbers survive in the
R7 verdict; the raw transcripts do not. **The closure round MUST produce
gate evidence into the repo before flipping the STATUS line.**

## Findings
R-0211 … R-0216, R-0217a, R-0217b: **Done**. **R-0217c: CARRIED** (above).
**Open findings: 0. Next free ID: R-0218.** Four of seven were
reviewer-authoring defects, two the same defect twice (a FROM that edits
a list must span the whole list); the worker caught each by refusing to
improvise. **`.agent/candidates.md` holds ONE entry** — the R-0214
handoff-cap amendment — and is a **BLOCK CONDITION at the next feature
claim**: the first reviewed round of what comes next must register or
resolve it and empty the file.

## What the next session must do, in order
1. **Phase 0 probe**: `git status --porcelain`, branch, `git log -n 8`,
   `gh pr list --state open`, `remedy plan status`, `remedy plan next`;
   then read from DISK `.agent/handoff.md`, `plan.md`, `live_review.md`,
   `candidates.md`, `docs/roadmap/features/T2_F254.md`. Never from memory.
2. **Closure round (R9)** per `docs/roadmap/STATUS_closure_protocol.md`:
   evidence job (feature-scoped, fresh job id) → **FRESH review zip**
   (`scripts/make_review_zip.sh`; **a zip failure is a closure BLOCKER**)
   → **gate evidence into the repo** (R-0217c) → reviewer authors the
   STATUS `[ ]`→`[x]` line, worker commits it **LAST** → `gh pr create`.
   **That PR is NOT merged in the session that creates it.**
3. After F254: **F103** (Token ledger, SQLite), which Rule A5 names —
   where the candidates.md block condition fires.

## This round (R8) — changed files and proofs
| Path | + | - |
|---|---|---|
| .agent/authored/f254-r8-1.md | 114 | 0 |
| .agent/authored/f254-r8-2.md | 43 | 0 |
| .agent/live_review.md | 70 | 9 |
| .agent/plan.md | 29 | 40 |
| .agent/handoff.md | rewritten (commit 2, self-reference) | |

Transport: `cp` then `cmp` vs the reviewer's scratchpad originals, both
**exit 0**; sha256 identical on both sides —
`fb7cb6a83e21a368432fa16510bdda3389e657c1295c58a09422c0486e6ea85d` r8-1,
`50c6c2fb9729aea88e629378ded93423f47757b66028a8ce9d8337283d2ab55b` r8-2.
Three pairs → live_review.md, all REWRITE-shaped, pre FROM 1x / TO 0x →
post FROM 0x / TO 1x each. plan.md was a full-file `cp`, `cmp` exit 0,
now **43 lines** (was 54 — R-0217b fixed), `## Goal` and `## Next Steps`
present. live_review.md keeps `## Steps`, `## Findings`, `## Decisions`,
`## Verdicts` 1x each and exactly one `- R6` bullet inside `## Steps`
(whole-file `grep -c '^- R6'` is 2: step bullet + R6 verdict line —
R-0217a, not a defect). Round gate, all exit 0: dashboard contract **70**
· test_test_runner **51** · resource safety **21** · golden path **42**.
Commit 1 `00703e8e`, commit 2 = this handoff, both pushed; tree clean,
`git worktree list` primary only, no force-push, no PR, STATUS untouched.

## Item status
| Item | Status | Reason |
|---|---|---|
| A1 apply f254-r8-1 (3 pairs) | done | all REWRITE-clean |
| A2 apply f254-r8-2 (full file) | done | cmp 0, plan.md 43 lines |
| Commit 1 + push | done | `00703e8e` |
| B session-closing handoff | done | this file |
| Commit 2 + push | done | reported in the handback message |

Length: **116 lines**, over the 100 the >5-commit allowance stretches to.
Declared, not hidden — R-0214's fifth measurement. No section dropped.

## Next expected action
A fresh session runs Phase 0, then the closure round above. Nothing is
in-flight and nothing waits on the operator.
