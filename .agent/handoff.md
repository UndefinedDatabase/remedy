# Handoff — F273 Findings paydown v1 · Round 9

## Session

SESSION 2 of feature F273 · round 9 · rounds so far 9

Context self-assessment: the worker read the block, AGENTS.md, DECISION F273 D9, round 8's handoff as the template's instance and all four code diffs as it applied them; every figure below comes from a command run in this round, and the worker's context held all of it without loss.

## Range

Review of db9a05cc..HEAD — branch `feature/f273-findings-paydown-v1`.

## Summary

Round 9 books round 8's verdict and its nine resolutions, lands DECISION F273 D9, and builds T010 (R-0411) and T007's R-0796 with F267's amendment as the reviewer's dry run built them.
- C1 books Gate F273 R8 (VERDICT PASS) and nine `Done:` lines (R-0570, R-0769, R-0665, R-0752, R-0666, R-0667, R-0668, R-0986, R-0987), lands DECISION F273 D9, rewrites the plan and saves the four payload copies.
- C2 (R-0411 part 1): `scripts/bench_sample_project/` is a stdlib-only fixture (a WSGI item service and a static widget); an order may name it with `bench_template`; the bench manifest freezes it by `bench_template_digest`; `RunnerDeps.template_dir_fn` (default `None`) lets `_evidence_body` digest the template the run was copied from, and `bench_run.bench_deps` hands one template choice to both the copy and the digest.
- C3 (R-0411 part 2): orders `b04-api-create-endpoint` and `b05-widget-count-badge` against the bench fixture, `BENCH_ORDER_SET_VERSION` 2, their premises tested by behaviour, and `T2_F082.md` updated.
- C4 (R-0796): `test.list`, `mission.list`, `change.list` and `event.list` go through `apply_list_options`, each with tests for an unknown sort field, the limit and the time window; `T2_F267.md` states T001 landed in F273 and keeps T002 and T003.
- C5 is this handoff.

Landed: R-0411 — `7347edba` (C2) and `6f503e7a` (C3)
Landed: R-0796 — `1aabd747` (C4)

## Commits

### e77595ab F273 R9 C1: bookkeeping — round 8's verdict and its nine resolutions booked, DECISION F273 D9 landed
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f273-r9-block.md` | +116 / -0 | Byte copy of the block |
| `.agent/authored/f273-r9-decisions.md` | +39 / -0 | Byte copy of decisions.md |
| `.agent/authored/f273-r9-ledger.md` | +20 / -0 | Byte copy of ledger.md |
| `.agent/authored/f273-r9-plan.md` | +28 / -0 | Byte copy of plan.md |
| `.agent/decisions.md` | +39 / -0 | `db9a05cc` bytes + decisions.md (DECISION F273 D9) |
| `.agent/live_review.md` | +20 / -0 | `db9a05cc` bytes + ledger.md (Gate F273 R8, nine `Done:` lines) |
| `.agent/plan.md` | +7 / -7 | := plan.md |

269 insertions, 7 deletions (`git show --numstat`).

### 7347edba F273 R9 C2: R-0411 part 1 — the bench owns its sample project, freezes it by digest, and its evidence digests the template it copied
All by `git apply .remedy-wt/f273-proto-t010a.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/bench_orders.py` | +34 / -2 | `bench_template`, `BenchOrder.template_dir`, fixture digest freeze |
| `packages/orchestration/bench_run.py` | +30 / -4 | `bench_deps`: one template choice for copy and digest |
| `packages/orchestration/gauntlet_runner.py` | +13 / -6 | `RunnerDeps.template_dir_fn`; `_template_digest(template_dir)` |
| `pyproject.toml` | +1 / -1 | Ruff `src` gains `scripts/bench_sample_project` |
| `scripts/bench_orders/manifest.json` | +1 / -0 | `bench_template_digest` |
| `scripts/bench_sample_project/README.md` | +5 / -0 | New fixture |
| `scripts/bench_sample_project/benchproj/__init__.py` | +1 / -0 | New fixture |
| `scripts/bench_sample_project/benchproj/api.py` | +47 / -0 | WSGI item service |
| `scripts/bench_sample_project/benchproj/web/widget.html` | +11 / -0 | Static widget |
| `scripts/bench_sample_project/benchproj/web/widget.js` | +17 / -0 | Static widget |
| `scripts/bench_sample_project/conftest.py` | +9 / -0 | Fixture test setup |
| `scripts/bench_sample_project/tests/test_api.py` | +37 / -0 | Fixture's own tests |
| `tests/orchestration/test_bench_orders.py` | +32 / -1 | Template key and fixture freeze |
| `tests/orchestration/test_bench_run.py` | +56 / -3 | Evidence names the bench template |
| `tests/orchestration/test_bench_sample_project.py` | +22 / -0 | New: fixture behaviour |
| `tests/test_no_orphan_modules.py` | +2 / -0 | Fixture directory excluded like the gauntlet's |

318 insertions, 17 deletions.

### 6f503e7a F273 R9 C3: R-0411 part 2 — the two bench orders b04 and b05 against the bench's own fixture
All by `git apply .remedy-wt/f273-proto-t010b.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/features/T2_F082.md` | +9 / -7 | Five orders; the R-0411 absence removed |
| `packages/orchestration/bench_orders.py` | +4 / -1 | `BENCH_ORDER_SET_VERSION = 2` |
| `scripts/bench_orders/b04-api-create-endpoint.json` | +32 / -0 | New order |
| `scripts/bench_orders/b05-widget-count-badge.json` | +32 / -0 | New order |
| `scripts/bench_orders/manifest.json` | +17 / -1 | b04 and b05 listed |
| `tests/orchestration/test_bench_orders.py` | +9 / -3 | Five-order set |
| `tests/orchestration/test_bench_run.py` | +8 / -0 | b04/b05 run in the bench fixture |
| `tests/orchestration/test_bench_sample_project.py` | +54 / -3 | b04 and b05 premises by behaviour |

165 insertions, 15 deletions.

### 1aabd747 F273 R9 C4: R-0796 — test, mission, change and event list take the shared list options, and F267 keeps T002 and T003
`git apply .remedy-wt/f273-proto-t007.diff`, then `git apply .remedy-wt/f273-r9/f267.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/command_catalog.py` | +3 / -4 | `event.list` keeps only its own `--limit` |
| `apps/cli/commands/change.py` | +40 / -2 | `apply_list_options` by the intent's `created_at` |
| `apps/cli/commands/event.py` | +27 / -3 | `apply_list_options`, newest first |
| `apps/cli/commands/mission_cmd.py` | +24 / -1 | `apply_list_options` |
| `apps/cli/commands/real_test_execution_cmd.py` | +18 / -1 | `apply_list_options` |
| `tests/cli/test_change_proof_cli.py` | +43 / -0 | Sort, limit, window, unknown field |
| `tests/cli/test_event_list_cmd.py` | +66 / -0 | New: sort, limit, window, unknown field, parse-to-handler |
| `tests/cli/test_mission_cmd.py` | +33 / -0 | Sort, limit, window, unknown field |
| `tests/cli/test_real_test_execution_cli.py` | +42 / -0 | Sort, limit, window, unknown field |
| `docs/roadmap/features/T2_F267.md` | +10 / -1 | T001 landed in F273; T002 and T003 remain (f267.diff) |

306 insertions, 12 deletions.

### C5 (this commit) F273 R9 C5: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C2, with 318.

## External actions

- `git worktree add --detach .remedy-wt/f273-r9-g5 1aabd747` for G5 (exit 0), then `git worktree remove .remedy-wt/f273-r9-g5` (exit 0). `git worktree list` afterwards:
  ```
  /home/decodeux/Repos/remedy                          1aabd747 [feature/f273-findings-paydown-v1]
  /home/decodeux/Repos/remedy/.remedy-wt/f273-h-r0762  db9a05cc (detached HEAD)
  ```
  The `f273-h-r0762` worktree is a research helper's; this round did not touch it.
- After C5: `git push`. No pull request is opened.

## Verification

G1 to G5 ran at C4 `1aabd747` with a clean tree, every script with `cwd` set explicitly.

- **Transport**, before any write: `sha256sum` of the three payloads, the block and the four diffs matched the block's digests (block.md `d3202f52c46bafaeefaff15134d4e61756268d363bcff04913b84fb7fb47e6fa`).
- **G1**: `python3 .remedy-wt/f273-r9/wk_g1.py`, exit=0 (C4's path set is compared with the union of the t007 and f267 diffs' `git apply --numstat` paths):
  ```
  digest plan.md True
  digest ledger.md True
  digest decisions.md True
  digest block.md True
  digest f273-proto-t010a.diff True
  digest f273-proto-t010b.diff True
  digest f273-proto-t007.diff True
  digest f267.diff True
  plan.md == payload True
  live_review.md == base + ledger True
  decisions.md == base + decisions True
  authored f273-r9-plan.md == payload True
  authored f273-r9-ledger.md == payload True
  authored f273-r9-decisions.md == payload True
  authored f273-r9-block.md == payload True
  C2 7347edba paths == diff numstat paths True 16
  C3 6f503e7a paths == diff numstat paths True 8
  C4 1aabd747 paths == diff numstat paths True 10
  ```
- **G2**: `git rev-parse 1aabd747:tests 1aabd747:packages 1aabd747:scripts 1aabd747:docs 1aabd747:apps 1aabd747:pyproject.toml`, exit=0:
  ```
  e3f1e31676ef32f3b2c2dfedd7a3af6ff1d5fdad
  2d5e2ac415e5fa1047098f60943ca49dacab4766
  be7597b0b73946138a69c98d427fbd1c5873c51c
  1d9ff5b4eaa1462d91d455153cfeba2b831af225
  a067589349e82f806957e9fef44aca6ee642fed2
  93acca6ef06eaa797e65333658003f3c11289e97
  ```
  All six equal the reviewer's dry-run objects.
- **G3** (primary checkout, serial, the block's 32 targets, full output in `.remedy-wt/f273-r9/g3.log`): `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_bench_dry_run.py ... tests/cli/test_golden_path.py`, exit=0:
  ```
  1491 passed in 227.96s (0:03:47)
  ```
  0 failed; `grep -c "R-0803:"` on the full output: 0. `git status --porcelain` empty afterwards.
- **G4**: `python3 -m ruff check . --output-format concise` from the primary checkout's root, exit=0:
  ```
  All checks passed!
  ```
- **G5** (`python3 .remedy-wt/f273-r9/wk_g5.py`, one worktree at `1aabd747`, `python3 -B -m pytest -q -p no:cacheprovider` from its root, `__pycache__` purged before every run, each FROM counted as a whole line with its newline in the named file first, each reverted from its saved bytes), exit=0, full output in `.remedy-wt/f273-r9/g5.log`:
  ```
  bench_run path: /home/decodeux/Repos/remedy/.remedy-wt/f273-r9-g5/packages/orchestration/bench_run.py
  [control] exit=0 summary=215 passed in 47.23s
  [a] FROM whole-line count in packages/orchestration/bench_run.py: 1
  [a] exit=1 summary=2 failed, 71 passed in 3.97s
      FAILED tests/orchestration/test_bench_run.py::test_an_order_naming_the_bench_template_runs_in_it_and_its_evidence_says_so
      FAILED tests/orchestration/test_bench_run.py::test_b04_and_b05_run_in_the_bench_fixture_and_the_rest_in_the_gauntlets
  [a] restored: True
  [b] FROM whole-line count in packages/orchestration/gauntlet_runner.py: 1
  [b] exit=1 summary=2 failed, 71 passed in 3.96s
      FAILED tests/orchestration/test_bench_run.py::test_an_order_naming_the_bench_template_runs_in_it_and_its_evidence_says_so
      FAILED tests/orchestration/test_bench_run.py::test_b04_and_b05_run_in_the_bench_fixture_and_the_rest_in_the_gauntlets
  [b] restored: True
  [c] FROM whole-line count in scripts/bench_sample_project/benchproj/api.py: 1
  [c] exit=1 summary=1 failed, 2 passed in 0.41s
      FAILED tests/orchestration/test_bench_sample_project.py::test_b04_premise_the_service_has_no_create_endpoint_today
  [c] restored: True
  [d] FROM whole-line count in packages/orchestration/bench_orders.py: 1
  [d] exit=1 summary=1 failed, 72 passed in 4.11s
      FAILED tests/orchestration/test_bench_orders.py::test_editing_the_bench_fixture_is_refused
  [d] restored: True
  [e] FROM whole-line count in apps/cli/commands/event.py: 1
  [e] exit=1 summary=5 failed, 1 passed in 0.24s
      FAILED tests/cli/test_event_list_cmd.py::test_the_newest_event_leads_by_default
      FAILED tests/cli/test_event_list_cmd.py::test_limit_keeps_the_newest_events
      FAILED tests/cli/test_event_list_cmd.py::test_since_and_until_filter_by_the_events_timestamp
      FAILED tests/cli/test_event_list_cmd.py::test_an_unknown_sort_field_exits_nonzero_naming_the_valid_set
      FAILED tests/cli/test_event_list_cmd.py::test_the_parsed_command_line_reaches_the_handler
  [e] restored: True
  [f] FROM whole-line count in apps/cli/commands/change.py: 1
  [f] exit=1 summary=3 failed, 17 passed in 0.29s
      FAILED tests/cli/test_change_proof_cli.py::test_change_list_is_newest_first_by_its_intents_created_at
      FAILED tests/cli/test_change_proof_cli.py::test_change_list_limit_and_time_window_filter_the_rows
      FAILED tests/cli/test_change_proof_cli.py::test_change_list_unknown_sort_field_exits_nonzero
  [f] restored: True
  [g] FROM whole-line count in apps/cli/commands/real_test_execution_cmd.py: 1
  [g] exit=1 summary=3 failed, 7 passed in 1.84s
      FAILED tests/cli/test_real_test_execution_cli.py::test_test_list_is_newest_first_and_limit_caps_it
      FAILED tests/cli/test_real_test_execution_cli.py::test_test_list_since_and_until_filter_by_created_at
      FAILED tests/cli/test_real_test_execution_cli.py::test_test_list_unknown_sort_field_exits_nonzero
  [g] restored: True
  [h] FROM whole-line count in apps/cli/commands/mission_cmd.py: 1
  [h] exit=1 summary=3 failed, 103 passed in 43.67s
      FAILED tests/cli/test_mission_cmd.py::TestListOptions::test_the_newest_mission_leads_and_limit_caps_the_rows
      FAILED tests/cli/test_mission_cmd.py::TestListOptions::test_until_filters_by_the_missions_own_date
      FAILED tests/cli/test_mission_cmd.py::TestListOptions::test_an_unknown_sort_field_exits_nonzero_naming_the_valid_set
  [h] restored: True
  worktree status after restores: ''
  ```
  The control ran over B and the four `tests/cli/` files together. Every mutation went red; none stayed green.
- **G6** runs after the push and is reported in the round report, because this commit precedes it.
- Full suite: not run (amend0917-throughput).

## Authored-text proofs

- Every edited `.agent/` file in C1 was built by `python3 .remedy-wt/f273-r9/wk_c1.py` from `git show db9a05cc:<path>` bytes and the payload bytes. Nothing was hand-edited. G1 re-proves every file and every `.agent/authored/f273-r9-*` copy against its payload.
- The code arrived only by `git apply` of the four reviewer-verified diffs, in the block's order. G2's object ids equal the reviewer's dry-run objects.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `e77595ab` |
| C2 R-0411 part 1 | done | `7347edba` |
| C3 R-0411 part 2 | done | `6f503e7a` |
| C4 R-0796 + F267 amendment | done | `1aabd747` |
| C5 handoff + push | done | This commit, then the push |
| G1 to G5 | done | All green as above |
| G6 | done | After the push; in the round report |

## Open findings

Measured by `.remedy-wt/f273-r9/wk_measure.py`, which loads `scripts/rotate_live_review.py` by path and calls `count_open_findings` (by distinct id) on the committed `.agent/live_review.md`:
- at `1aabd747` (C1 onwards; C2 to C4 do not touch it): **89 open**;
- at `db9a05cc`: 98 open.

C1's nine `Done:` lines close nine distinct ids and register none. The two ids landed this round (R-0411, R-0796) are still open in the ledger, as is R-0762. Open blocker/high ids: R-0803, R-0807.

## Deviations & assumptions

- **Commit sequence:** as ordered: C1 to C5, then the push. No extra commit.
- **Payload copies:** "every payload above" was read as the four files listed under PAYLOADS (plan, ledger, decisions, block), as in rounds 2 to 8. The four code diffs are listed under CODE and are not copied into `.agent/authored/`.
- **G5 set B:** read as the seven `test_bench_*` files of G3 plus `test_capability_bench.py`, eight files in all.
- **Scratch:** gitignored under `.remedy-wt/f273-r9/`: `wk_c1.py`, `wk_g1.py`, `wk_g5.py`, `wk_measure.py`, and the outputs `g3.log`, `g5.log`. `pyfiles.txt` there is the reviewer's, not read by any gate.

## Next

1. Phase 1 rule 1 (`.agent/STOP`), then the review of round 9.

Operator questions open: 5
