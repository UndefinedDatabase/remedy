# Handback — F307 round 12: book round 11 with R-1297, R-1414 and R-1415; R-1281's writer part lands — `create_mission` writes no umbrella mission

## Session

SESSION 3 of feature F307 · round 12 · rounds so far 12

Context self-assessment: this worker verified both prepared digests before any write, applied C1 through a byte-proof script, removed `create_mission`'s `project_ids` keyword and its spanned-project check, rewrote every test that built an umbrella mission through that keyword to write the legacy record directly with `save_mission(Mission(...))`, deleted the two writer-only tests `test_create_refuses_projects_that_do_not_fit` and `test_create_refuses_a_project_id_that_cannot_be_a_path`, added a refusal test for the dropped keyword, ran each gate once, and found both `git grep` readings clean on the first pass; context is ample and nothing was lost.

Session end (the reviewer, after its verdict on round 12): this session ran three delegated rounds, 10 to 12, below the target of six to eight, because the next slice in DECISION F307 D5's order, T005, needs structural steps in two listed files, `packages/orchestration/pingpong_loop.py` and `packages/orchestration/pingpong_provider.py`, before any of its five findings can land, and planning those steps explicitly needs a fresh session's context; one prose slip was written this session.

Fortschritt: ~60 % (T001 to T004, T010, T011, T014, R-1280, R-1290, R-1292, R-1297, R-1298, R-1301, R-1414 and R-1415 landed, R-1281's writer part under review · the rest open) — Schätzung

## Range

Review of `143789322`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### b750c67bd F307 R12 C1: book round 11 with R-1297, R-1414 and R-1415, DECISION F307 D12, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r12.md` | 106/0 | NEW FILE, this round's block, byte copy (106 lines, sha256 `5488d24eb862233b8bb17bfbe2450a5138b0c5079353a5284a34c75c5a0ed143`, equal to `block.md`) |
| `.agent/decisions.md` | 12/0 | prepared slice appended (DECISION F307 D12: R-1281's writer part lands now, the gauntlet's route and the umbrella readers carried) |
| `.agent/live_review.md` | 8/0 | prepared slice appended (round 11's Gate verdict PASS, and the R-1297/R-1414/R-1415 resolutions) |
| `.agent/plan.md` | 8/9 | replaced with the prepared file (round 12's current step: R-1281's writer part) |

### 0a5d146c8 F307 R12 C2: create_mission writes no umbrella mission; tests write legacy records directly (R-1281)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/mission_state.py` | 4/15 | `create_mission` loses the `project_ids` keyword, the `spanned` computation and its `check_spanned_project_ids` call; the `Mission(...)` it builds no longer passes `project_ids`; docstring rewritten per DECISION F307 D12; the now-unused `check_spanned_project_ids` import dropped |
| `tests/orchestration/test_client_digest.py` | 7/2 | the one umbrella-building `create_mission(..., project_ids=...)` call replaced inline with `save_mission(Mission(...))`, same tuple, a fixed ISO `created_at` |
| `tests/orchestration/test_mission_projects.py` | 16/31 | new helper `_legacy_umbrella` used at every former umbrella-building call site (5 of them); `test_naming_only_its_own_project_is_a_mission_of_one_project`, `test_create_refuses_projects_that_do_not_fit` and `test_create_refuses_a_project_id_that_cannot_be_a_path` deleted; `test_a_record_whose_projects_do_not_fit_will_not_read` and every other test kept |
| `tests/orchestration/test_mission_state.py` | 8/0 | new test `test_a_project_ids_keyword_is_refused_and_writes_nothing`: the keyword now raises `TypeError` and writes no mission directory |
| `tests/orchestration/test_mission_upkeep.py` | 7/3 | the one umbrella-building call in `_mission` replaced with `save_mission(Mission(...))` |
| `tests/orchestration/test_orchestrator_dispatch.py` | 11/3 | the one umbrella-building call replaced with `save_mission(Mission(...))` |
| `tests/orchestration/test_repo_mission.py` | 4/2 | the one umbrella-building call in a cross-repository reconcile test replaced with `save_mission(Mission(...))` |
| `tests/orchestration/test_repo_mission_reconcile.py` | 5/2 | the one umbrella-building call in `_umbrella` replaced with `save_mission(Mission(...))` |

### (this commit) F307 R12 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | base confirmed: HEAD and `origin/feature/f307-findings-paydown-v9` both `14378932203717e19ca227327ec41586c80c5f14`, tree clean, no pull run |
| C1 | done | commit `b750c67bd`, 134 insertions (at or below the 500 cap) |
| C2 | done | commit `0a5d146c8`, 62 insertions (at or below the 500 cap) |
| C3 | done | this handback commit |
| Gate 1 | done | `git -C <root> status --porcelain` — empty |
| Gate 2 | done | `ruff over 8 files: exit 0`, `All checks passed!` |
| Gate 3 | done | `paths 115`, `exit 0`, `5346 passed, 2 skipped in 74.49s`, no FAILED/ERROR/`process(es) behind` line |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | open findings count printed `30` |
| Push | pending | runs after this commit; reported in the session reply |

## External actions

No push, PR or `gh` command before this commit; the push follows it and is reported in the session reply. No worktree of my own created or entered; the reviewer's prepared `.remedy-wt/f307-r12/prep/` was only read, never written into. `.remedy-wt/f307-r12-worker/` (created this round) holds the C1 byte-proof script, the gate-4 integrity-check script and the three commit-message files. No provider call.

## Verification

1. Digests checked first, before any write: `block.md` sha256 `5488d24eb862233b8bb17bfbe2450a5138b0c5079353a5284a34c75c5a0ed143` and `digests.txt` sha256 `8aeebea447ac04a2bd0a3d02d0b25204cc26a79935430687c5ed05ebcb50740f`, both equal to the delivering prompt. Every other file `digests.txt` lists (`c1-.agent__plan.md`, `c1-decisions-append.txt`, `c1-live_review-append.txt`, `ruff_touched.py`, `run_selection.py`, `selection.txt`) was hashed individually and matched.
2. C0: branch `feature/f307-findings-paydown-v9`; `git rev-parse HEAD` and `origin/feature/f307-findings-paydown-v9` both `14378932203717e19ca227327ec41586c80c5f14`; tree clean; no `git pull` run.
3. Gate 1: `git -C <root> status --porcelain` — empty.
4. Gate 2: `python3 .remedy-wt/f307-r12/prep/ruff_touched.py <root>` — `files: packages/orchestration/mission_state.py tests/orchestration/test_client_digest.py tests/orchestration/test_mission_projects.py tests/orchestration/test_mission_state.py tests/orchestration/test_mission_upkeep.py tests/orchestration/test_orchestrator_dispatch.py tests/orchestration/test_repo_mission.py tests/orchestration/test_repo_mission_reconcile.py`, `ruff over 8 files: exit 0`, `All checks passed!`.
5. Gate 3: `python3 .remedy-wt/f307-r12/prep/run_selection.py <root> .remedy-wt/f307-r12-worker/selection-output.txt` — `paths 115`, `exit 0`, `5346 passed, 2 skipped in 74.49s (0:01:14)`. SKIPPED: `tests/test_agent_tooling.py:43` (D12 quarantine, F252 — the read-only reviewer contract now lives at the split-workflow docs) and `tests/test_install_smoke.py:175` (install smoke is opt-in, `REMEDY_INSTALL_SMOKE=1`). No FAILED, ERROR or "process(es) behind" line.
6. Gate 4: `python3 -m apps.cli.main integrity check --json` (run through a python3 script with `cwd=<root>`) — `fail_count` 0; `handler_import` pass (`handlers=194`), `live_review_verdict` pass (last Gate verdict PASS), `plan_consistency` pass (`unchecked=0, context_complete=False`), `relevant_untracked` pass (`untracked=0, relevant=0`), `repo_root_hygiene` pass (no reviewer scratch, evidence dir or archive at the root), `high_blockers_open` pass (no open blocker/high findings).
7. Gate 5: `python3 .remedy-wt/f307-r10/open_count.py <root>` — `30`.
8. The two `git grep` readings named in the block, run after C2: `git grep -n "project_ids=" -- tests` lists 7 lines, none a `create_mission(` call (the surviving calls build a `Mission(...)` directly, or — `test_job_insight.py` — are an unrelated function); `git grep -n "project_ids" -- packages/orchestration/mission_state.py` lists 5 lines, none a parameter of `create_mission` (the function `project_ids_with_missions`, and `mission.project_ids` attribute reads inside `link_job_to_mission`).
9. Single-file runs while writing (not gates, each once): `tests/orchestration/test_orchestrator_dispatch.py` — `6 passed`; `tests/orchestration/test_mission_upkeep.py` — `66 passed`; `tests/orchestration/test_client_digest.py` — `77 passed`; `tests/orchestration/test_repo_mission_reconcile.py` — `15 passed`; `tests/orchestration/test_repo_mission.py` — `29 passed`; `tests/orchestration/test_mission_projects.py` — `15 passed`; `tests/orchestration/test_mission_state.py` — `101 passed`; a combined run of all seven touched test modules together — `309 passed`.

## Authored-text proofs

`.agent/authored/f307-r12.md` equals `block.md`: 106 lines, sha256 `5488d24eb862233b8bb17bfbe2450a5138b0c5079353a5284a34c75c5a0ed143` on both sides. The `.agent/live_review.md` and `.agent/decisions.md` appends, and the `.agent/plan.md` replacement, were each proved byte-for-byte (pre-image + prepared slice == result, or copy == source) by a one-shot apply script run immediately after writing: all four checks read `True`.

## Deviations & assumptions

None. The commit sequence landed exactly as ordered (C1, C2, each touching only its named paths); no mutation red-proof was run; no full suite was run; `REMEDY_TEST_MAX_WORKERS` was never set; `.data` was never read; no `amend`, `rebase`, force-push or `--no-verify`; each gate ran once and never concurrently with another; no PR was opened, per the block. Every repository-state command (file writes, `git -C <root> add`, `git -C <root> commit -F <file>`, the three gate scripts, the single-file test runs while writing) used `git -C` or a `python3` script taking explicit paths, with no `cd`, no `VAR=x cmd`, no command substitution and no pipe into a second program.

## Reviewer verdict of round 12 (carried here under amend0827 rule 1)

VERDICT PASS. Book these two paragraphs byte for byte, each preceded by one empty line, at the end of
`.agent/live_review.md` in the next round's first commit:

Gate: F307 R12 — the F307 round 12 entry, over `143789322`..`adf22d1f8` (3 commits, each single-parent; insertions by `git show --shortstat`: `b750c67bd` 134, `0a5d146c8` 62, `adf22d1f8` 92). VERDICT PASS. The records commit is byte-exact: the ledger and the decisions file each equal their pre-image plus the prepared slice, and the plan and the saved block equal the prepared files. C2 removes `create_mission`'s `project_ids` keyword and its spanned-project checks; every umbrella record a test needs is written directly with `save_mission`, and the only assertions removed belong to the three writer tests the block named. In a disposable worktree at `adf22d1f8`, `test_a_project_ids_keyword_is_refused_and_writes_nothing` failed with `mission_state.py` as it stood at `b750c67bd`. The reviewer's own run of the selection read `5346 passed, 2 skipped` with exit 0 over 115 paths, the worker's one run the same; ruff read clean over the eight Python files, the integrity check `fail_count` 0, and the open set 30 ids.

Landed: R-1281 — in part, at F307 R12: `0a5d146c8` removed the umbrella writer, `create_mission`'s `project_ids` keyword, held by `test_a_project_ids_keyword_is_refused_and_writes_nothing` (red with the module as it stood at `b750c67bd`). The gauntlet's route through the repository mission and the deletion of the umbrella readers stay open, carried to the next findings paydown by DECISION F307 D12 (2) and (3).

## Scoping note for T005 (the reviewer, for the next session)

- R-1287 (a stop check between links) and R-1289 (the chains resolved once per run) both need the run's
  stop check or a resolved table handed into the provider the run builds, which means editing
  `run_pingpong` or `_call_with_retry` in `packages/orchestration/pingpong_loop.py`, both listed, so
  each needs its structural step first.
- R-1278's own repair text gives each link its own `stream_rel_prefix`, but the closed call-ref grammar
  in `packages/orchestration/run_manifest.py` (`streams/<role>/round-NN/<kind>-II`, a role that must
  agree with the call's identity) would refuse a link prefix such as `streams/builder-link-1`. A repair
  that keeps the grammar builds each link once per wrapper, forwards `begin_stream_call` and
  `offer_stable_prefix`, and lets the links continue the primary's stream counters, which touches
  `ClaudeCliProvider` in the listed `packages/orchestration/pingpong_provider.py`. Record the choice as a
  DECISION in the round that lands it, and name the existing assertion
  `assert fp.begin_stream_call == primary.begin_stream_call` in `tests/orchestration/test_model_failover.py`,
  which the forwarding changes.
- R-1276 and R-1277 sit in `pingpong_loop.py` too.

## For the operator, in plain sentences

No part of Remedy can now create a new mission spanning several projects. Missions of that old shape still read as before. The test harness that exercises whole orders and the removal of the old readers wait for a later round, because the readers must stay until the old missions on the operator's machine have been folded.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Round 12 is reviewed (PASS): book the two paragraphs of the section "Reviewer verdict of round 12" above in the next round's first commit.
4. The listed-file slices in their written order, from T005.

Operator questions open: 0. Open findings count gate 5 printed: 30.
