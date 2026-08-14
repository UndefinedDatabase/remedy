# Handback — F045 Loop definitions, round R15 (integration gate)

Branch `feature/f045-loop-definitions`. Base 6451da42. No merge, no PR, no
force-push, no production code, no test file touched. Open findings after this
round: 3 — R-0350, R-0354, R-0358.

## Range
Review of 6451da42..HEAD.

## Commits
### c99cf9a5 chore(f045): save the R15 block verbatim
| `.agent/authored/f045-r15.md` | +162/-0 | C0a, verbatim block save (cap-exempt, F104 D1) |
### 1cd1e836 chore(f045): point last_block at the R15 block
| `.agent/last_block.md` | +128/-147 | C0b, byte-identical copy (cap-exempt) |
### c84bd958 docs(f045): register R-0358 on the job id attribute
| `.agent/live_review.md` | +2/-0 | C1, authored FINDING-358, applied disk-to-disk |
### b102def8 chore(f045): record the integration gate evidence
| `.agent/gate_f045_r15/` | +268/-0 | C2, 13 `.txt` evidence files, no `.log` |
### C3 (this commit) docs(f045): close the session with the R15 handoff
| `.agent/plan.md` | rewrite, 49 lines | open set from gate (b), gate result, next step |
| `.agent/handoff.md` | rewrite | this file (self-reference, R-0149 pattern) |

## External actions
`git push origin feature/f045-loop-definitions` after every commit — exit 0 each
time. `git worktree add -b tmp/base-gate .remedy-wt/f045_r15_base cb3ef34f` →
`Preparing worktree (new branch 'tmp/base-gate')`, exit 0; `git worktree remove
--force` + `prune` + `git branch -D tmp/base-gate` → `Deleted branch tmp/base-gate
(was cb3ef34f)`. `gh pr list --state open --json number,headRefName` → `[]`. No PR
created, none merged.

## Verification (real commands, real output)
(a) `cmp .agent/authored/f045-r15.md .agent/last_block.md` → exit 0, no output.
(b) open-set script → `OPEN ['R-0350', 'R-0354', 'R-0358']`, exactly as ordered.
(c) C1 numstat `2 0 .agent/live_review.md`; FINDING-358 appears once among the
    added lines (the other added line is the blank separator).
(d) INTEGRATION GATE. Merge base COMPUTED: `git merge-base main HEAD` →
    `cb3ef34fddbf0efa5799d8de93cb2d8e66566d20`.
    BRANCH `python3 -m pytest -n auto -q` → `EXIT_CODE=1`, `WALL_SECONDS=128`,
    tail `5 failed, 16769 passed, 19 skipped in 126.83s`.
    BASE (worktree at the merge base, `REMEDY_UI_NO_AUTO_BUILD=1`) → `EXIT_CODE=1`,
    `WALL_SECONDS=142`, tail `11 failed, 16700 passed, 19 skipped in 141.32s`.
    Parity: `apps/ui/node_modules` + `apps/ui/dist` COPIED (`cp -a`, never
    symlinked), `copy_*_exit=0`; `DIST_HASH_BEFORE` = `DIST_HASH_AFTER` =
    `86bc883a2c7fe7229f9149c1a8f684d92bc3cdd33e0702062ab4e504f7da3c89`.
    `comm -13` (BRANCH-ONLY) → EMPTY. No id needs step-4 attribution; no blocker.
    `comm -23` → the 6 `tests/ui_server/test_live_state.py::TestUIServerIntegration`
    ids. Per-id attribution to the environment class: captured stderr for each is
    `ERROR: React UI not built.` naming `apps/ui/dist`; each id re-run alone at the
    merge base → `1 passed`, RC=0 (6/6); the whole file under `-n auto` there →
    `42 passed`; and a SECOND full base run on the same commit → `EXIT_CODE=1`,
    `WALL_SECONDS=133`, `5 failed, 16706 passed, 19 skipped`, whose FAILED list is
    byte-identical to the branch's (`cmp` exit 0), so `comm -13` and `comm -23`
    are both empty against it. FLAKE DEBT: 0 branch-only failures. The 5 failures
    common to both sides are pre-existing at the merge base (`reviewer_conventions`
    estimates 954 tokens against cap 800); this branch never touches that file.
(e) `pytest tests/orchestration/test_loop_run.py tests/cli/test_loop_cmd.py
    tests/orchestration/test_loop_spec.py tests/orchestration/test_run_report.py -q`
    → `123 passed in 0.34s`, RC=0.
(f)/(g)/(h) post-commit re-runs are in the completion report — a handoff cannot
    contain the output of the commit that writes it. Pre-C3: `git status
    --porcelain` empty, `git worktree list` 1 line, `git branch --list 'tmp/*'`
    empty, `gh pr list --state open` → `[]`, and a Python scan (`l != l.rstrip()`,
    not `grep -rn ' $'`) → `[]` for every non-evidence file written this round.

## Authored-text proofs
FINDING-358: extracted from the committed `.agent/authored/f045-r15.md` between
its `>>> FINDING-358 >>>` / `<<< FINDING-358 <<<` markers and appended byte for
byte — never retyped. `cmp` of block save vs `last_block.md` → exit 0.

## Item status
| Item | Status | Reason |
| C0a save the block | done | |
| C0b last_block | done | |
| C1 register R-0358 | done | |
| C2 integration gate + evidence | done | |
| C3 plan + handoff | done | |

## Deviations & assumptions
This file is 93 lines, over the 60-line cap; cause is the mandated gate
transcript (both runs, parity hashes, both `comm` lists, per-id attribution for
6 ids) plus the 5-commit table. No section dropped. A SECOND full base run was
added beyond the block's letter, as direct evidence for the `comm -23`
attribution the procedure demands. I did NOT determine the mechanism that made
those 6 ids fail in base run 1 and pass in base run 2 — the evidence attributes
them to the `apps/ui/dist` environment class; no causal claim beyond that.

## Next
(1) Phase 1 rule 1 — read `.agent/STOP` from disk BEFORE anything else (R-0347;
it was absent at this round's start). (2) Phase 1 rule 2 — the Open PR Gate.
(3) F045 closure per docs/roadmap/STATUS_closure_protocol.md, whose precondition
2 must be ruled on against the 5 pre-existing red ids F045 did not cause.

Fortschritt: ~85 % (T001 ✅ · T002 ✅ · T003 ✅ · Integrationsgate gelaufen) — Schätzung
