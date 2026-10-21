# Handback — F307 round 10: book round 9 with R-1298; R-1297, an order batch records the repository it was accepted for, and a mission of a second repository continues there

## Session

SESSION 3 of feature F307 · round 10 · rounds so far 10

Context self-assessment: this worker verified both prepared digests before any write, applied C1 through a byte-proof script, implemented C2 from DECISION F307 D11's five numbered points with five new tests across four modules, self-reviewed each diff before committing, ran each gate once, and found and diagnosed one real gate-3 regression outside this round's authorized file set rather than silently fixing it; context is ample and nothing was lost.

Fortschritt: ~55 % (T001 to T004, T010, T011, T014, R-1280, R-1290, R-1292, R-1297, R-1298 and R-1301 landed · the rest open) — Schätzung

## Range

Review of `9ca3d2748`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### e917da3d4 F307 R10 C1: book round 9 with R-1298, DECISION F307 D11, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r10.md` | 115/0 | NEW FILE, this round's block, byte copy (115 lines, sha256 `8cd024f72aebd20112854722b65719aef9ea3155d89514a1cda0b476ba7665f3`, equal to `block.md`) |
| `.agent/live_review.md` | 4/0 | prepared slice appended (round 9's Gate verdict and R-1298's Done entry) |
| `.agent/decisions.md` | 12/0 | prepared slice appended (DECISION F307 D11) |
| `.agent/plan.md` | 13/6 | replaced with the prepared file (round 10's current step, R-1297) |

### dbc1367b2 F307 R10 C2: an order batch records its repository, and a mission of a second repository continues there (R-1297)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/mission_record.py` | 55/16 | `MissionOrderBatch.repo_path`, written/read additively; `Mission.order_repo_path()`; `follow_up_target` answers a second repository's project and repository for a one-project mission keyed to it |
| `packages/orchestration/repo_mission.py` | 10/1 | `accept_order` records `repo_path=str(repo_root)` on every batch; new `mission_repo_root(mission)` beside `project_repo_root`, with its WHY comment |
| `packages/orchestration/mission_upkeep.py` | 10/4 | `upkeep_target` always calls `follow_up_target`, reusing its answer for a second-repository mission instead of writing a second rule |
| `packages/orchestration/mission_contract.py` | 4/2 | `start_remainder_follow_up_mission` accepts the remainder into `mission_repo_root(mission)`; file stays at 991 lines, line-neutral |
| `apps/cli/commands/decision.py` | 4/2 | `_create_mission_for_job` accepts into the job's own `repo_path` when set, else `project_repo_root(owner)`; `_cmd_decision_resolve` untouched |
| `docs/system/mission-upkeep-v1.md` | 4/0 | one paragraph after "A repository has one lasting mission...", naming DECISION F307 D11's behaviour |
| `tests/orchestration/test_repo_mission.py` | 17/0 | T1: a batch accepted for a second repository records its root; one accepted with none writes no key |
| `tests/orchestration/test_mission_projects.py` | 20/1 | T2: `follow_up_target` of a second-repository mission answers it; a canonical-keyed mission answers `{}` (control) |
| `tests/orchestration/test_mission_upkeep.py` | 12/0 | T3: `upkeep_target` of a second-repository mission answers that repository |
| `tests/orchestration/test_mission_contract.py` | 26/0 | T4: the remainder of a second repository's mission is accepted into that repository's mission |
| `tests/cli/test_decision_cmd.py` | 47/0 | T5: a goal approved from a job with its own `repo_path` is accepted there; one from a job with none falls back to the project's repository |

### (this commit) F307 R10 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | base confirmed: HEAD and `origin/feature/f307-findings-paydown-v9` both `9ca3d2748409f6e0be5fe351e99a7251d93d4fd2`, tree clean, no pull run |
| C1 | done | commit `e917da3d4` |
| C2 | done | commit `dbc1367b2`, 185 insertions by `git show --shortstat` (at or below the 500 cap) |
| C3 | done | this handback commit |
| Gate 1 | done | `git -C <root> status --porcelain` — empty |
| Gate 2 | done | `ruff over 10 files: exit 0`, `All checks passed!` |
| Gate 3 | deviated | `paths 92`, `exit 1`, `1 failed, 4509 passed, 2 skipped in 45.49s`; see Deviations for the one failing node and its root cause — the fix needs a file outside this round's authorized path list |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | open findings count printed `31` |
| Push | pending | runs after this commit; reported in the session reply |

## External actions

No push, PR or `gh` command before this commit; the push follows it and is reported in the session reply. No worktree of my own created or entered; the reviewer's prepared `.remedy-wt/f307-r10/prep/` was only read, never written into or `cd`-ed into. No provider call.

## Verification

1. `block.md` and `digests.txt` hashed first: `8cd024f7...65f3` and `5d2259ec...706`, both equal to the delivering prompt. Every other prepared file under `.remedy-wt/f307-r10/prep/` was hashed too and matched `digests.txt` before use.
2. C0: branch `feature/f307-findings-paydown-v9`; `git rev-parse HEAD` and `origin/feature/f307-findings-paydown-v9` both `9ca3d2748409f6e0be5fe351e99a7251d93d4fd2`; tree clean.
3. Gate 1: `git -C <root> status --porcelain` — empty.
4. Gate 2: `python3 .remedy-wt/f307-r10/prep/ruff_touched.py <root>` — `files: apps/cli/commands/decision.py packages/orchestration/mission_contract.py packages/orchestration/mission_record.py packages/orchestration/mission_upkeep.py packages/orchestration/repo_mission.py tests/cli/test_decision_cmd.py tests/orchestration/test_mission_contract.py tests/orchestration/test_mission_projects.py tests/orchestration/test_mission_upkeep.py tests/orchestration/test_repo_mission.py`, `ruff over 10 files: exit 0`, `All checks passed!`.
5. Gate 3: `python3 .remedy-wt/f307-r10/prep/run_selection.py <root> .remedy-wt/f307-r10-worker/selection-output.txt` — `paths 92`, `exit 1`, `1 failed, 4509 passed, 2 skipped in 45.49s`. SKIPPED: `tests/test_agent_tooling.py:43` (D12 quarantine, F252) and `tests/test_install_smoke.py:175` (opt-in install smoke). The one FAILED node: `tests/cli/test_client_interface.py::test_a_real_runs_answers_return_only_keys_the_interface_names`, `AssertionError: assert [('mission', 'orders', 'repo_path')] == []`. No `process(es) behind` line.
6. Gate 4: `python3 -m apps.cli.main integrity check --json` — `fail_count` 0; `handler_import` pass (handlers=194), `live_review_verdict` pass (last Gate verdict PASS), `plan_consistency` pass, `relevant_untracked` pass, `repo_root_hygiene` pass, `high_blockers_open` pass.
7. Gate 5: `rotate_live_review.open_finding_ids` count — `31`.

## Authored-text proofs

`.agent/authored/f307-r10.md` equals `block.md`: 115 lines, sha256 `8cd024f72aebd20112854722b65719aef9ea3155d89514a1cda0b476ba7665f3` on both sides. The `.agent/live_review.md` and `.agent/decisions.md` appends, and the `.agent/plan.md` replacement, were each proved byte-for-byte (pre-image + prepared slice == result) by the apply script right after writing.

## Deviations & assumptions

Gate 3 is red, and I did not fix it in this round. Root cause, confirmed by running the same test on the round's base commit `9ca3d2748` in the reviewer's prepared dry worktree (`.remedy-wt/f307-r10-dry`, read-only, not entered or written into): it passes there and fails only after C2. `accept_order` now writes `repo_path` onto every batch given a non-empty repository root (DECISION F307 D11 (1), unconditional on `str(repo_root)`), which is true of an ordinary canonical-repository order too, not only a second repository's. `mission.abandon`'s answer therefore now carries `orders[].repo_path` for a real run, and `apps/cli/client_interface.py`'s `ANSWER_KEY_TREES["mission.abandon"]["mission"]["orders"]` does not declare it, so `tests/cli/test_client_interface.py::test_a_real_runs_answers_return_only_keys_the_interface_names` fails with one undeclared path. The fix is three edits in two files this round's block does not name and its Constraints forbid touching: add `"repo_path": {}` to that `orders` dict in `apps/cli/client_interface.py`, bump `CLIENT_INTERFACE_VERSION` and its docstring list per that file's own convention, and update the hardcoded `"1.25"` in `tests/cli/test_client_interface.py::test_the_document_carries_its_own_version` (an existing assertion the block forbids changing). I registered no new finding id myself, since this round's block names no finding-registration step; the next round's planner should book it (a Low/Medium finding against `mission.abandon`'s interface declaration) before claiming further T012 work. No other deviation in the commit sequence, paths or gate order: no mutation run, no full-suite run, `REMEDY_TEST_MAX_WORKERS` not set, `.data` not read, no amend, rebase or force, gates run once each and never concurrently.

## For the operator, in plain sentences

The work a mission of a project's second repository goes on to do now stays in that repository instead of moving to the project's main one.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Review round 10's handback and book its verdict, with the resolution of R-1297, in the next round's first commit.
4. The rest of T012: R-1281.

Operator questions open: 0. Open findings count gate 5 printed: 31.
