# Handback — F307 round 19: book round 18; T013: `plan_source` leaves the interface (R-1311) and the digest names each mission's orders and each job's order (R-1282)

## Session

SESSION 5 of feature F307 · round 19 · rounds so far 19

Context self-assessment: this worker verified every prepared digest before any write, applied C1 by a byte-proof script and C2/C3 by hand-editing the named files exactly as DECISION F307 D19 specifies, ran the generated-page writers with cwd the root, read each staged diff before committing, and ran each gate once; context is ample and nothing was lost.

Fortschritt: ~80 % (T001 to T006, T008 to T011, T014, R-1280, R-1290, R-1292, R-1297, R-1298, R-1301, R-1414, R-1415 and R-1416 landed, R-1281's writer part landed, T013 under review · the rest open) — Schätzung

## Range

Review of `35e7662a6`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### 943ebe4ed F307 R19 C1: book round 18 with R-1303, R-1304, R-1305, R-1308 and R-1309, DECISION F307 D19, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r19.md` | 134/0 | NEW FILE, this round's block, byte copy (134 lines, sha256 `ad9773837ae276a8950751a21ea44d716d3da8df3296901f4e6ce6060ae14fb2`, equal to `block.md`) |
| `.agent/decisions.md` | 12/0 | prepared slice appended (DECISION F307 D19) |
| `.agent/live_review.md` | 12/0 | prepared slice appended (round 18's Gate verdict PASS, R-1303/R-1304/R-1305/R-1308/R-1309 done) |
| `.agent/plan.md` | 7/7 | replaced with the prepared file |

165 insertions, 7 deletions over 4 files (`git show --shortstat`).

### c4317dd46 F307 R19 C2: plan_source, a key no order batch ever carried, leaves the record and the interface at 1.27 (R-1311)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/mission_record.py` | 2/4 | `MissionOrderBatch.plan_source` field, its `to_json` key and its `from_json` argument deleted; docstring's cross-reference moved to `correlation_id` |
| `apps/cli/client_interface.py` | 1/1 | `"plan_source": {}, ` deleted from the `mission.abandon` `orders` tree; file stays at 942 lines |
| `docs/system/api-release-matrix-v1.json` | 7/1 | 1.27's `value_changes` gains the `orders.plan_source` removal entry; `rule` names the one removed key |
| `docs/system/machine-client-contract-v1.md` | 1/1 | generated section rewritten by `write_client_interface_page()`: `orders` key list drops `plan_source` |
| `tests/orchestration/test_mission_upkeep.py` | 14/0 | new test `test_an_order_batch_has_no_plan_source_and_reads_a_record_that_held_one` |

25 insertions, 7 deletions over 5 files (`git show --shortstat`).

### 473d7efad F307 R19 C3: the digest names each mission's orders and each job's order, at 1.27 (R-1282)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/client_digest.py` | 28/0 | `_order_batch_entry` and `_job_order_id` helpers added above `_mission_entry` and `_job_entry`; `orders` and `order_id` keys added; `build_client_digest` untouched |
| `apps/cli/client_interface_digest.py` | 5/1 | `DIGEST_KEY_TREE` gains missions' `orders` and jobs' `order_id`; comment cites R-1282 |
| `docs/system/api-release-matrix-v1.json` | 3/1 | 1.27's `added` gains the digest/changes `orders` and `order_id` entry |
| `docs/system/machine-client-contract-v1.md` | 11/6 | hand-written "JSON keys" table gains `orders` and `order_id` rows; generated section rewritten by `write_client_interface_page()` and `write_public_api_page()` (the latter changed nothing) |
| `tests/orchestration/test_client_digest.py` | 107/0 | three new tests: `test_a_missions_entry_names_each_order_with_the_jobs_it_asked_for`, `test_a_job_entry_names_its_order`, `test_a_mission_with_no_order_batches_reads_orders_empty` |

154 insertions, 8 deletions over 5 files (`git show --shortstat`).

### (this commit) F307 R19 C4: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | HEAD and `origin/feature/f307-findings-paydown-v9` both `35e7662a6a74b4ccd368e4cceb904493602af5b8`, tree clean, no pull run, no `.agent/STOP` |
| C1 | done | commit `943ebe4ed`, 165 insertions, byte proofs all held |
| C2 | done | commit `c4317dd46`, 25 insertions, `plan_source` gone from record, interface and matrix |
| C3 | done | commit `473d7efad`, 154 insertions, `build_client_digest` untouched, `client_interface.py` 942 lines |
| C4 | done | this handback commit |
| Gate 1 | done | `git status --porcelain` empty |
| Gate 2 | done | `ruff over 6 files: exit 0`, `All checks passed!` |
| Gate 3 | done | `paths 104`, `exit 0`, `4797 passed, 2 skipped in 51.36s` |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | `18` |
| Gate 6 | done | no hunk inside `build_client_digest`; `client_interface.py` still 942 lines |
| Push | pending | runs after this commit; reported in the session reply |

## External actions

None before this commit; the push follows it and is reported in the session reply. `.remedy-wt/f307-r19-worker/` (created this round) holds the digest-verification script, the C1 byte-proof script, the generated-page writer scripts, the ruff scripts, the integrity-check script, the three commit-message files and the selection output. No provider call.

## Verification

1. Digests, before any write: `digests.txt` sha256 `a55967cb41b6e7e779d453da65b7785ae85e4a79b8734cd062c2c6001b4f9077` and `block.md` sha256 `ad9773837ae276a8950751a21ea44d716d3da8df3296901f4e6ce6060ae14fb2` (134 lines) both equal the delivering prompt; the six other listed entries matched (by a python3 script, since `digests.txt` is tab-separated).
2. C0: branch `feature/f307-findings-paydown-v9`; HEAD equals `origin/feature/f307-findings-paydown-v9` at `35e7662a6a74b4ccd368e4cceb904493602af5b8`; tree clean.
3. Gate 1: `git -C <root> status --porcelain` — empty (read after C3, before C4).
4. Gate 2: `python3 .remedy-wt/f307-r19/prep/ruff_touched.py <root>` — `files: apps/cli/client_interface.py apps/cli/client_interface_digest.py packages/orchestration/client_digest.py packages/orchestration/mission_record.py tests/orchestration/test_client_digest.py tests/orchestration/test_mission_upkeep.py`, `ruff over 6 files: exit 0`, `All checks passed!`.
5. Gate 3: `python3 .remedy-wt/f307-r19/prep/run_selection.py <root> .remedy-wt/f307-r19-worker/selection-output.txt` — `paths 104`, `exit 0`, `4797 passed, 2 skipped in 51.36s`. SKIPPED: `tests/test_install_smoke.py:175` (opt-in, `REMEDY_INSTALL_SMOKE=1`), `tests/test_agent_tooling.py:43` (D12 quarantine, F252). No FAILED, ERROR or "process(es) behind" line.
6. Gate 4: `python3 -m apps.cli.main integrity check --json` via a python3 script with `cwd=<root>` — exit 0, `fail_count` 0; `handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`, `repo_root_hygiene`, `high_blockers_open` all pass.
7. Gate 5: `python3 .remedy-wt/f307-r10/open_count.py <root>` — `18`.
8. Gate 6: `git -C <root> diff 35e7662a6 HEAD -- packages/orchestration/client_digest.py` read in full — both hunks sit strictly between `_decision_entry` and `build_client_digest`, touching only `_mission_entry`, `_job_entry` and two new private helpers above each; no hunk inside `build_client_digest`. `wc -l apps/cli/client_interface.py` — `942`.

Single-test runs made while writing (not gates, reported for completeness): `tests/orchestration/test_mission_upkeep.py` (67 passed), `tests/cli/test_client_interface.py` (95 passed), `tests/orchestration/test_mission_contract.py` (132 passed), `tests/orchestration/test_api_release_matrix.py` (3 passed) after C2; `tests/orchestration/test_client_digest.py` (80 passed), `tests/cli/test_client_interface.py` (95 passed), `tests/cli/test_status_cmd.py` (18 passed), `tests/orchestration/test_client_changes.py` (15 passed), `tests/orchestration/test_api_release_matrix.py` (3 passed) after C3.

## Authored-text proofs

`.agent/authored/f307-r19.md` equals `block.md`: 134 lines, sha256 `ad9773837ae276a8950751a21ea44d716d3da8df3296901f4e6ce6060ae14fb2` on both sides. The `.agent/live_review.md` and `.agent/decisions.md` appends (each equal to pre-image plus slice) and the `.agent/plan.md` replacement were each proved byte for byte by one script right after writing, in the same run that applied them. C2 and C3 were not prepared patches this round — DECISION F307 D19 is the spec and the worker hand-edited the named files to match it exactly, verified by reading each diff in full before committing (see Commits above and gate 6).

## Deviations & assumptions

- The block names no test file for C2's `plan_source` test beyond "find it by `git grep -l mission_record tests`, else the one nearest `mission_record.py`"; several files in that grep hit import `MissionOrderBatch`. This worker chose `tests/orchestration/test_mission_upkeep.py` because it already imports `Mission` and `MissionOrderBatch` directly from `mission_record` at module level and already instantiates `MissionOrderBatch` in an existing test, needing no new import path. Flagging this as a judgment call rather than an unambiguous match.
- Otherwise none. The commit sequence landed exactly as ordered (C1 to C4), each touching only its named paths. No mutation red-proof, no full suite outside the selection, `REMEDY_TEST_MAX_WORKERS` never set, `.data` never read, no amend, rebase, force-push or `--no-verify`, no PR; each gate ran once and never concurrently.

## For the operator, in plain sentences

A program that reads Remedy's overview now sees every order a mission was given, with the jobs each order asked for, and each job says which order it belongs to; a field that was described but never filled is gone from the description of a mission.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Review round 19's handback and book its verdict, with R-1282 and R-1311, in the next round's first commit.
4. T015, R-1323 (the fake provider reports token usage).

Operator questions open: 0. Open findings count gate 5 printed: 18.
