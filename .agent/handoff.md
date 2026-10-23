# Handback — operator order fix1022-review-findings

## Session

SESSION 1 of operator order fix1022-review-findings (not a loop round; one session, one branch).

Context self-assessment: every finding was proved red before its repair, each repair is its own
commit, and context stayed ample throughout.

Fortschritt: 100 % of the order's repairs landed; the pull request merges only on a green hosted
run — Schätzung

## State

| Field | Value |
|---|---|
| Branch | `feature/fix1022-review-findings`, from `main` at `4ded1afbe` (the merge of pull request 380, F074, merged by this session's Open PR Gate) |
| Head before this handoff | `79adde111` |
| Findings | R-1422, R-1423, R-1424 resolved; R-1425 registered OPEN, owner F314 |
| Open findings | 11: R-1246, R-1281, R-1326, R-1351, R-1353, R-1418, R-1421, R-1425 to R-1428 (all F314's) |
| Merge | NOT merged: second hosted run red; operator question Q24 |
| Contract | public API and client interface 1.27 → 1.28 |
| mypy 2.3.1, `packages apps` | before: 440 errors in 110 files (`main` at `4ded1afbe`); after: 410 errors in 100 files |

## Item status

| Item | Status | Reason |
|---|---|---|
| R-1422 (R-NEW1) | deviated | resolved; the order's red test lacked `provider_attempts` on its namespace, added (DECISION fix1022 (5)) |
| R-1423 (R-NEW2) | done | |
| R-1424 (R-NEW3) | deviated | resolved; the check sits in two helpers, not inline, to keep `answer_budget_decision` at its structure-ledger row (DECISION fix1022 (6)) |
| R-1425 (R-NEW4) | done | ten modules repaired, none skipped; registered OPEN for F314 as ordered |

## Commits

| Commit | Subject | Insertions |
|---|---|---|
| `ad793b0bb` | R-1422 red test (with plan and context rewritten for the order) | 45 |
| `6a4098218` | R-1422 fix: `_with_calls(..., primary_served=)` | 12 |
| `a93e7ccbb` | R-1422 record: failover doc, F307 Built State, ledger | 11 |
| `94910ef68` | R-1423 red tests (running reads 5, expected 9; stopped holds 5) | 29 |
| `950185129` | R-1423 fix: `budget_work_seconds(..., in_flight=)` | 10 |
| `eaa68379b` | R-1423 contract 1.28: versions, matrix, both docs, regenerated pages, pins | 41 |
| `6013facba` | R-1423 kit seed to version-3 actuals, client answers re-recorded | 9 |
| `2dc1178f7` | R-1423 record: F311 Built State, ledger | 10 |
| `6b6ab5e97` | R-1424 red tests (two) | 26 |
| `3f62e03ad` | R-1424 fix: `_doubled_answers`, `_missing_answer_detail` | 22 |
| `10174b946` | R-1424 record: budget doc, F310 Built State, ledger | 15 |
| `48685c746`, `394c1b0d1`, `a3dc14324`, `1f4c417cb`, `3cf61876a`, `a6406ef61`, `e63ba38da`, `a5f811719`, `c5c57fa8b`, `613d3f9cf` | R-1425, one module each (cost_preview with its one-cent test) | 18, 4, 2, 8, 27, 3, 3, 1, 3, 2 |
| `79adde111` | R-1425 registration, CHANGELOG, DECISION fix1022 | 52 |
| `6efb41e7f` | context file: `Steps` heading and pytest constraint restored | 5 |
| `c93df184a` | the handoff | — |
| `84000eabb` | hosted run 39856076613 red: R-1426 registered with its 166 nodes | — |
| `a8abb7c94` | R-1426 repair: the workflow's tool-sandbox step, its guard test, the CI doc | — |
| (this commit) | R-1426 `Landed:` line, DECISION fix1022 (9), this handoff | — |

Every commit is under 500 insertions.

## Verification

Interpreter: Python 3.10.12. Taken on `79adde111` (tree `cebf1a0a0`) unless noted.

| Command | Result |
|---|---|
| `scripts/remedy_lint.sh ruff` | `All lint checks passed.` |
| `python3 -m pytest tests/docs -q` | `346 passed` |
| `python3 -m pytest tests/cli/test_golden_path.py -q` (canary) | `42 passed` |
| Parts 1 to 4 selection (every suite the order names, plus the structure ratchet) | `1895 passed in 201.84s` |
| `python3 scripts/record_client_answers.py --check` | `client answers: match` |
| `scripts/remedy_test_fast.sh main` | exit 1: `2 failed, 6696 passed`; `test_context_md_no_stale_steps` and `test_context_mentions_resource_safety`, both red because this order's rewrite of `.agent/context.md` dropped its `Steps` heading and its pytest constraint; restored at `6efb41e7f`, the two modules then read `33 passed` |
| `scripts/remedy_test_fast.sh main` on the final tree | recorded in the pull request body with its commit and tree, because this handoff is part of that tree |
| mypy 2.3.1 `packages apps` | 440 errors in 110 files before (`4ded1afbe`), 410 in 100 after; the order's grep over the ten repaired modules prints nothing |

Red proofs: R-1422 `AttributeError: 'BuilderOutput' object has no attribute 'failover_calls'`;
R-1423 `assert 5 == 9`; R-1424 the generic sentence and `budget_limit_not_raised` where
`missing_argument` was expected.

## Hosted CI

1. Run 39856076613 over `c93df184a`: red, `129 failed, 17561 passed` and `36 failed, 5572 passed`
   and `1 failed, 22 passed` per stage, the same 166 nodes in 3.10 and 3.12, all
   `sandbox_unavailable` (no Bubblewrap on the runner). None is in a test file this branch changed.
   Registered as R-1426 (Low, F314); repaired in the workflow at `a8abb7c94`.
2. Run 39861110995 over `694f9aec4`: red, but 166 failures fell to 2: `17708 passed` / `1 failed, 17707 passed`
   and `1 failed, 5607 passed` per column. R-1427 (`test_do_order_budget`, both columns, `TypeError`)
   and R-1428 (`test_tool_sandbox` disk search, 3.12 only, timeout), both green locally, registered
   Low for F314. A second red run is never merged: pull request 381 stays OPEN and question Q24
   waits for the operator.

## Deviations & assumptions

1. ORIG_BRANCH was `feature/f074-estimate-calibration`; the Open PR Gate merged its pull request
   380 with `--delete-branch`, which removed it, so the session ends on `main`.
2. Finding ids R-NEW1 to R-NEW4 are R-1422 to R-1425.
3. R-1422's test: `SimpleNamespace(builder_model="sonnet")` raised `AttributeError` on
   `provider_attempts` once the walk attached its call; the namespace gained
   `provider_attempts=[]` and one more assertion. It was red without the fix in both forms.
4. R-1424: inserted inline, the order's nine lines grew `answer_budget_decision` from its
   structure-ledger row of 155 to 164 lines and turned `tests/test_structure_ratchet.py` red. The
   same rule now lives in `_doubled_answers` and `_missing_answer_detail`; the refusal code and
   sentence are the order's, and the function stays at 155.
5. R-1423's stopped-job twin shares one helper with the running test instead of a copied record.
6. mypy: the interpreter carries mypy 2.1.0; the counts were taken with 2.3.1, the pin, in a
   disposable venv under `.remedy-wt/` over the installed packages. `job_certificate_verify` had
   one error and one note (the order said 1, the plain grep reads 2 lines).
7. `_autonomy_value` raises `KeyError` for a key the schema does not hold, where the code raised
   `AttributeError` before; no configuration reaches that path.
8. The first fast-lane run was red on two `.agent/context.md` guards my rewrite tripped;
   repaired at `6efb41e7f`, no test changed.
9. R-1426 is one finding for 166 nodes of one cause (DECISION fix1022 (9)).
10. The R-1423 re-recording changed only the stub server's port and one second of silence.

## Next

1. The operator answers Q24: merge pull request 381 as it stands, or repair R-1427 and R-1428 first.
2. F314 owns R-1425's remaining growth (`pingpong_loop`, `pingpong_provider`,
   `role_provider_factory`, `do_sequence`) and the question of a mypy ratchet.
