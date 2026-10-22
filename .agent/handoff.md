# Handback — F113 round 2: book round 1, DECISION F113 D2, and T003a: a task run's side-role calls in its evidence and the cost ledger

## Session

SESSION 1 of feature F113 · round 2 · rounds so far 2

Context self-assessment: this worker verified the block and manifest digests before any write, copied each prepared file by a script with a byte-for-byte proof, ran each gate once after C2, and context stayed ample throughout.

Fortschritt: ~50 % (T001, T002 and T003a landed · T003b and T003c open) — Schätzung

## Range

Review of `3e66bbc7b`..`HEAD` on `feature/f113-local-side-roles`.

## Commits

### d2e9b19e4 F113 R2 C1: book round 1, DECISION F113 D2, the plan, the block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f113-r2.md` | +97/-0 | NEW FILE, this round's block, byte copy equal to `block.md` (97 lines, sha256 `3086c1d2...6269c`) |
| `.agent/decisions.md` | see commit | DECISION F113 D2 |
| `.agent/live_review.md` | see commit | round 1's verdict booked |
| `.agent/plan.md` | see commit | rewritten for round 2 |

Total 117 insertions, 7 deletions, under 500.

### 6cf30dd2e F113 R2 C2: the side-role calls of a task run in its evidence and the cost ledger, with the basis local_zero
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/side_role_calls.py` | +183/-0 | NEW FILE, reads the cached routed summaries, writes the evidence file and the ledger rows |
| `packages/orchestration/job_evidence.py` | +4/-4 | one import and one call beside the tier outcomes; line count unchanged |
| `tests/orchestration/test_side_role_calls.py` | +165/-0 | NEW FILE |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | the new module |
| `docs/system/local-side-roles-v1.md` | +9/-9 | the ledger section |
| `docs/README.md` | +1/-1 | the page's index row |

Total 368 insertions, 9 deletions, under 500.

### (this commit) F113 R2 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback (a handoff cannot table the commit that writes it) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | branch, HEAD `3e66bbc7b` equal to origin, status empty, no `.agent/STOP`, open PR list `[]` |
| C1 | done | commit `d2e9b19e4`; four paths byte-proved equal; block copy 97 lines, sha256 equal to `block.md` |
| C2 | done | commit `6cf30dd2e`; six paths byte-proved equal; 368 insertions |
| C3 | done | this commit |
| Gate 1 | done | status porcelain empty; `verify.py .` ended `ALL True` (C3 `absent`, as it was not yet committed) |
| Gate 2 | done | `ruff_touched.py .` over 3 files, exit 0, `All checks passed!` |
| Gate 3 | done | exit 0, `7083 passed, 2 skipped in 71.05s`, no FAILED, ERROR or `process(es) behind` line |
| Gate 4 | done | `integrity check --json` exit 0, `fail_count` 0 |
| Gate 5 | done | printed `7` |
| Push | pending | runs after this commit; its result is reported in the session reply |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` printed `[]`. No pull request is opened by this round. `git push origin feature/f113-local-side-roles` runs right after this commit; its result is reported in the session reply.

## Verification

1. Digests before any write: `block.md` sha256 `3086c1d27e6d8dc98d0baaf2d4f22c8932764616b6e6636ce5a5600618d6269c`; `digests.txt` sha256 `778121e5aea81f26172b924c7696bbb81a047565ca22b52a057db6f7cce8b8aa`; every listed file `True`.
2. Gate 1: `git status --porcelain` empty after C2; `verify.py .` exit 0, every line `True`, `absent` for C3, last line `ALL True`.
3. Gate 2: `ruff_touched.py .` exit 0: `ruff over 3 files: exit 0`, `All checks passed!`.
4. Gate 3: `run_selection.py` exit 0 (175 paths): `7083 passed, 2 skipped in 71.05s (0:01:11)`. Skipped lines: `tests/test_agent_tooling.py:43` (D12 quarantine, F252), `tests/test_install_smoke.py:175` (opt-in install smoke).
5. Gate 4: `integrity check --json` exit 0; six checks `pass`, `"fail_count": 0`, `"ok": true`.
6. Gate 5: `open_finding_ids` over the live review printed `7`.

## Authored-text proofs

All prepared files of C1 and C2 (10 paths) were proved equal over bytes by a script that copies and then compares, and `verify.py` re-proved them after C2. The saved block `.agent/authored/f113-r2.md` equals `block.md` (97 lines, same sha256).

## Deviations & assumptions

None. C1 and C2 landed in the ordered sequence, each touching only its named paths. No amend, rebase, force-push or `--no-verify`. No mutation proofs, no full suite, no `REMEDY_TEST_MAX_WORKERS`; each gate ran once. The working directory was never changed; commands needing the repository root ran through scripts under `.remedy-wt/f113-r2-worker/` that pass `cwd=`.

## For the operator, in plain sentences

When a task run sends a summary to a model server on your own machine, Remedy now keeps a record of that call next to the task's other evidence. The same calls also appear in the cost record, where a call to your own server is counted as costing nothing in paid tokens. Runs that use no local server show no change. Still missing are the quality check that switches a server off when its summaries are poor, and the end-to-end demonstration.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Book round 2's verdict in the next round's first commit.
4. T003b: the spot-check set, the flip, the dwell rule and the status line.

Operator questions open: 0. Open findings: 7.
