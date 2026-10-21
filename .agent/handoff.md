# Handback — F307 round 7: book round 6, R-1300, R-1285 and R-1299, register R-1413; R-1311, the mission leftovers cleaned up, the safe job loader never raises

## Session

SESSION 1 of feature F307 · round 7 · rounds so far 7

Context self-assessment: this worker verified every prepared digest before use, byte-copied the prepared files, self-reviewed each diff before committing, ran each gate once and wrote this handback from what it read; context is ample and nothing was lost. This round ends session 1.

Fortschritt: ~40 % (T001 to T004, T010, T014, R-1280, R-1290 and R-1292 landed · the rest open) — Schätzung

## Range

Review of `d9f3c26bc`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### 6357dfc98 F307 R7 C1: book round 6, R-1300, R-1285 and R-1299, register R-1413, DECISION F307 D8, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r7.md` | 102/0 | NEW FILE, this round's block, byte copy (102 lines, sha256 `b4e823c8461393ecaa31faad961825dd843a69fc4f716c76649ebe9154ddca31`, equal to `block.md`) |
| `.agent/decisions.md` | 12/0 | prepared file, byte copy (DECISION F307 D8) |
| `.agent/live_review.md` | 10/0 | prepared file, byte copy (round 6's verdict and its three resolutions booked: R-1300, R-1285, R-1299; R-1413 registered) |
| `.agent/plan.md` | 8/7 | prepared file, byte copy |
| `docs/roadmap/features/T2_F307.md` | 3/1 | prepared file, byte copy (the T013 line and an Acceptance line for R-1413) |

### bb851e664 F307 R7 C2: the mission leftovers cleaned up without a change of behaviour (R-1311)
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/do_cmd.py` | 1/1 | prepared file, byte copy (import of `running_mission_for_order_file` switched to `repo_mission`) |
| `apps/cli/commands/mission_cmd.py` | 5/5 | prepared file, byte copy (module docstring brought up to the one-mission model) |
| `packages/orchestration/do_sequence.py` | 5/3 | prepared file, byte copy (module docstring brought up to the one-mission model) |
| `packages/orchestration/mission_compiler.py` | 2/2 | prepared file, byte copy (`plan_mission`'s refusal sentence names a new order as the route) |
| `packages/orchestration/mission_state.py` | 8/15 | prepared file, byte copy (forwarding `running_mission_for_order_file` deleted; `create_mission`'s docstring updated) |
| `packages/orchestration/public_api.py` | 1/1 | prepared file, byte copy (import switched to `repo_mission`) |
| `packages/orchestration/repo_catalog.py` | 3/3 | prepared file, byte copy (`_reachable_pids` renamed `reachable_catalog_pids`, loses its underscore; module docstring updated) |
| `packages/orchestration/repo_catalog_plausibility.py` | 2/20 | prepared file, byte copy (its own duplicate of the reachability helper deleted; imports the one definition) |
| `packages/orchestration/repo_mission.py` | 13/15 | prepared file, byte copy (`ORDER_KIND_READ_ONLY` deleted; `_find_or_create` answers whether it created the mission; each refusal computed once) |
| `tests/cli/test_do_several_projects.py` | 3/2 | prepared file, byte copy (docstring updated to the one-mission model) |
| `tests/orchestration/test_mission_state.py` | 1/1 | prepared file, byte copy (import of `running_mission_for_order_file` switched to `repo_mission`) |
| `tests/ui_server/test_public_api.py` | 2/2 | prepared file, byte copy (the stand-in patches `repo_mission`, not `mission_state`) |

### e88ddf14a F307 R7 C3: the safe job loader never raises and the failure path of an order's planning uses it (R-1311, R-1413)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/do_sequence.py` | 2/2 | prepared file, byte copy (`_stop_unrun_shape_jobs` reads each job with the safe loader, passing over a damaged record) |
| `packages/orchestration/pingpong_job.py` | 3/3 | prepared file, byte copy (`load_job_plan_safe` also catches `AttributeError`, as its docstring promises) |
| `tests/orchestration/test_order_shape_repair.py` | 41/0 | prepared file, byte copy (new test: a damaged job record does not end the failure path) |
| `tests/orchestration/test_pingpong_job_loading.py` | 24/0 | NEW FILE, prepared file, byte copy (the safe loader answers a damaged record as damaged, parametrized over three wrong shapes) |

### (this commit) F307 R7 C4: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | base confirmed: HEAD `d9f3c26bc` equal to `origin/feature/f307-findings-paydown-v9`, tree clean, no pull run |
| C1 | done | records commit `6357dfc98` |
| C2 | done | R-1311 cleanup commit `bb851e664` |
| C3 | done | R-1311/R-1413 behaviour commit `e88ddf14a` |
| C4 | done | this handback commit |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` printed `True` on every counted line, `absent C4` (not yet counted), last line `ALL True` |
| Gate 2 | done | `ruff check` over 15 files printed `All checks passed!`, exit 0 |
| Gate 3 | done | 90 paths, exit 0, `4299 passed, 2 skipped in 59.21s`, two SKIPPED lines, no FAILED, ERROR or `process(es) behind` line |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | open findings count printed `38` |
| Push | pending | runs after this commit; reported in the session reply |

## External actions

No push, PR or `gh` command before this commit; the push follows it and is reported in the session reply. No worktree of my own, no provider call, no rotation.

## Verification

1. Digests: a python check over the 26 lines of `digests.txt` — every prepared file's sha256 read `OK` against the listed digest, last line `ALL_DIGESTS_OK: True`; `block.md` and `digests.txt` themselves were also hashed first and matched the values given in the delivering prompt (`digests.txt` sha256 `580bc0db9fd9f2eeb556130fbf32266df869de2942d7e26b3d9f2e32e6263f47`).
2. C0: `git branch --show-current` read `feature/f307-findings-paydown-v9`; `git rev-parse HEAD` and `git rev-parse origin/feature/f307-findings-paydown-v9` both read `d9f3c26bc3e882516a042fa392b1ce20888a3d06`; `git status --porcelain` was empty before any write; no pull was run.
3. Each of C1, C2 and C3: every prepared file was copied over its path and re-hashed; every copy's sha256 equaled the prepared file's sha256 before staging. `git diff --cached` was read in full before each commit; each diff matched the block's description of that commit, touched no path outside the ones the block names for it, and carried no debug leftover or unrelated change.
4. Gate 1: `git status --porcelain` (through `git -C`) — empty. `python3 .remedy-wt/f307-r7/prep/verify.py .` — exit 0; every per-commit, per-path and structural line read `True` (single-parent checks on all three commits, the Cn-subject count `3 of 3`, the branch check, every C1 through C3 path-set-exactly check and per-path byte-equality check, and "the saved block equals block.md"); one line `absent	C4` (C4 did not exist yet when the gate ran); last line `ALL True`.
5. Gate 2: `python3 .remedy-wt/f307-r7/prep/ruff_touched.py .`, run from the primary checkout — `ruff over 15 files: exit 0`, `All checks passed!`.
6. Gate 3: `python3 .remedy-wt/f307-r7/prep/run_selection.py . .remedy-wt/f307-r7-worker/selection-output.txt` — `paths 90`, `exit 0`, `4299 passed, 2 skipped in 59.21s`. SKIPPED lines: `tests/test_agent_tooling.py:43` (D12 quarantine, F252 — the read-only reviewer contract now lives on the split-workflow docs) and `tests/test_install_smoke.py:175` (install smoke is opt-in: set `REMEDY_INSTALL_SMOKE=1` on a host with network access). No FAILED, no ERROR, no `process(es) behind` line.
7. Gate 4: `python3 -m apps.cli.main integrity check --json` exit 0 — `fail_count` 0; all six checks pass: `handler_import` ("handlers=194"), `live_review_verdict` ("last Gate verdict PASS"), `plan_consistency` ("unchecked=0, context_complete=False"), `relevant_untracked` ("untracked=0, relevant=0"), `repo_root_hygiene` ("no reviewer scratch, evidence dir or archive at the root"), `high_blockers_open` ("no open blocker/high findings").
8. Gate 5: `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` — `38`.

## Authored-text proofs

C1's five prepared files, C2's twelve prepared files and C3's four prepared files are byte copies of the prepared files; each was proved equal by a `sha256` comparison right after the copy, before staging, and `verify.py` re-proved every one of them (`True`). `.agent/authored/f307-r7.md` equals `block.md`: 102 lines, sha256 `b4e823c8461393ecaa31faad961825dd843a69fc4f716c76649ebe9154ddca31` on both sides.

## Deviations & assumptions

None. The commit sequence, paths and gate commands followed the block exactly; no file outside the named paths per commit was touched; each gate ran exactly once, in order; no mutation or full-suite run was attempted; `REMEDY_TEST_MAX_WORKERS` was not set; `.data` was not read; every commit used `git -C <repository root> commit -F <message file>`, never `cd` joined to another command; no amend, rebase or force was used; `.agent/STOP` was checked and is absent.

## For the operator, in plain sentences

This round booked the previous round's closing verdict and its three resolutions into the running record, registered one new finding about a loader that could crash instead of reporting a damaged record, and recorded a decision covering ten leftovers of an earlier model change. Seven of those leftovers were cleaned up with no change in what the program does: one unused distinction was removed, one small forwarding function was deleted in favour of the module that already did the real work, a couple of answers that used to be computed twice are now computed once, a helper that already told its caller something useful now also says whether it just created what it returned, one small helper that existed twice in two files now exists once, and several explanatory texts that described an older way of working were brought up to date. One of the ten leftovers turned out to be a real defect rather than a leftover: a part of the program that reads a batch of saved jobs one at a time, to stop the ones that never ran, used a loader that could crash on a single damaged record and so leave every later job in that batch untouched; that loader now treats such a record the same safe way it already treats every other kind of damage, so it reports the problem instead of crashing, and the jobs after the damaged one are still stopped as intended. One of the ten leftovers was found to rest on a wrong premise, and one was deferred to a later step that already touches the same shared interface for an unrelated reason, so that interface only has to change once. All five required checks ran once each and came back exactly as expected. Separately: two small web servers left over from a test run three days ago are still running on this machine and answer on every network address; this session did not stop them because it did not start them, and the operator may stop them. No question waits for the operator.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Review round 7's handback and book its verdict, with R-1311's resolution, in the next round's first commit.
4. T011, the mission reconcile: R-1283, R-1284, R-1295 and R-1296.

Operator questions open: 0. Open findings count gate 5 printed: 38.
