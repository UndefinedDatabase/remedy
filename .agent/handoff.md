# Handoff — F283 Machine contracts, part two: refusal sweep, JSON gap, exit-code taxonomy · Round 17 · T002's success half, first batch (D10)

## Session

SESSION 4 of feature F283 · round 17 · rounds so far 17

This round booked round 16's PASS, registered and repaired R-1030 (a
comment in `start_ui_server` naming the wrong module as its function-scoped
import's precedent — it now names `_command_is_ui_exposed`, this same
file, with no claim about `apps/cli/json_envelope.py`), pinned the three
probes round 16's review found unpinned (`project attach-job`'s
already-attached case answers `added` false; `ui stop`'s `os.kill` failure
answers a `failed` entry carrying `pid`/`job_id`/`error`; `start_ui_server`
answers `job_not_found` for a 404 job and `invalid_job_id` for a 400 one),
recorded DECISION F283 D10 (every `--json` success path writes its document
through the envelope, additively, and a failed result is a failure
envelope) and landed its ratchet (a self-contained AST scanner and a pinned
per-module dict, 122 raw sites over 34 modules at the round's base), then
converted the twenty smaller command modules the block named: HALF A
(`job_stop_cmd`, `test_cmds`, `change`, `bench_cmd`, `blocker`,
`contract_cmd`, `data_cmd`, `decision`, `roadmap_cmd`, `snapshot_cmds`) and
HALF B (`teacher_cmd`, `dev`, `failure_stats_cmd`, `file`, `init_cmd`,
`integrity_cmd`, `job_context_cmd`, `status_cmd`, `study_cmd`,
`worker_facade_cmd`). Every raw `print(<json>.dumps(...))` site in those
twenty modules now answers `emit_ok(**document)`; `test run --json`'s
failed-run path answers one `emit_error("test_run_failed", ..., **document)`
because its document carries `exit_code`, one of `fail()`'s own parameter
names (D10 (3)); `integrity check --json`'s failing-gate path, which the
same rule reaches and the block did not name explicitly, answers
`fail("integrity_failed", ..., **document)` since its document carries no
colliding key. The ratchet now names only the fourteen larger modules
round 18 will convert (87 raw sites). Self-review after C5 found the new
`test run` failure-envelope conversion untested for its `ok`/`error` shape
— the existing test only asserted `status`/`exit_code`, both of which
survive under `emit_ok` too — so an unordered fix-forward commit, C6-fix,
adds that assertion; see Deviations.
Context self-assessment: the large majority of the working budget remained
at the point this handoff was written.

## Range

Review of `488fd05a`..`HEAD`.

## Block self-verification (R-0954)

| reading | measured | given | equal |
|---|---|---|---|
| line count | 204 | 204 | True |
| sha256 | `c48a6aa00c6ac73b656cfdc1551455606f75feaecdc9e35251aa5787c98d24d8` | `c48a6aa00c6ac73b656cfdc1551455606f75feaecdc9e35251aa5787c98d24d8` | True |

Neither reading differed, so the round went ahead.

## Pre-flight

- `ls .agent/STOP`: `No such file or directory`. No STOP on disk.
- `git status --porcelain`: empty.
- `git branch --show-current`: `feature/f283-machine-contracts-part-two`.
- `git log --oneline -1`: `488fd05a`, matching the delegation message.

## Commits

### 6631e250 F283 R17 C1: copy round 17 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r17-block.md | +204/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f283-r17-decisions.md | +40/-0 | byte-for-byte copy of decisions.md |
| .agent/authored/f283-r17-ledger.md | +4/-0 | byte-for-byte copy of ledger.md |
| .agent/authored/f283-r17-plan.md | +37/-0 | byte-for-byte copy of plan.md |

Measured insertions (`git show --numstat`): **285** (204+40+4+37).

### 6b5e6e9b F283 R17 C2: book round 16's PASS, register R-1030, record D10
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +40/-0 | append decisions.md: DECISION F283 D10 |
| .agent/live_review.md | +4/-0 | append ledger.md by strict byte concatenation: round-16 `Gate:` entry and R-1030's registration |
| .agent/plan.md | +16/-13 | rewrite to plan.md payload, byte-identical; git's line diff shows only the lines that changed |

Measured insertions: **60** (40+4+16); 13 deletions from the plan.md rewrite.

### 81d28ed4 F283 R17 C3: repair R-1030's comment; pin attach-job, ui stop and ui start
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +1/-0 | the one `Landed: R-1030 — ...` line, appended, nothing else |
| packages/orchestration/ui_server.py | +4/-4 | the comment above `start_ui_server`'s function-scoped `apps.cli.json_envelope` import now names `_command_is_ui_exposed`, this same file, as the precedent, with no claim about `json_envelope.py` |
| tests/cli/test_project_current.py | +20/-0 | new `test_attach_job_already_attached_answers_added_false`: a second `project attach-job --json` on the same job answers `added` false |
| tests/ui_server/test_live_state.py | +51/-0 | new `test_stop_kill_failure_answers_a_failed_entry` (`os.kill` raising answers a `failed` entry carrying `pid`/`job_id`/`error`), `test_missing_job_answers_job_not_found` and `test_malformed_job_id_answers_invalid_job_id` (`start_ui_server`'s 404/400 branches) |

Measured insertions: **76** (1+4+20+51); 4 deletions.

### ccbc428a F283 R17 C4: a ratchet on the raw --json documents left under apps/cli (D10)
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_json_envelope.py | +97/-0 | `_raw_json_document_sites_by_module()` (a self-contained copy of the reviewer's `raw_sites.py` scanner, so the ratchet needs no scratch file) and `TestRawJSONDocumentSitesRatchet`, pinning all 34 modules by equality against the round's base reading, 122 total |

Measured insertions: **97**.

### dbc49b6b F283 R17 C5: ten command modules answer --json success in the envelope (D10)
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/bench_cmd.py | +7/-8 | `_cmd_stats_bench`'s three `--json` sites (empty history, no row of the series, the normal render) answer `emit_ok(**_bench_payload(...))`, the first two merging in `empty_reason` |
| apps/cli/commands/blocker.py | +10/-11 | `_cmd_blocker_list` and `_cmd_blocker_show` answer `emit_ok(version=1, ...)` |
| apps/cli/commands/change.py | +4/-5 | `_cmd_change_list`, `_cmd_change_show`, `_cmd_change_proof` answer `emit_ok(**export_*_json(...))` |
| apps/cli/commands/contract_cmd.py | +12/-15 | `_cmd_mission_contract` and `_cmd_job_contract` answer `emit_ok(...)` |
| apps/cli/commands/data_cmd.py | +4/-3 | `_cmd_data_usage` and `_print_reclaim` answer `emit_ok(**export_footprint_json(...))` / `emit_ok(**export_reclaim_json(...))` |
| apps/cli/commands/decision.py | +10/-11 | `_cmd_decision_list` and `_cmd_decision_show` answer `emit_ok(version=1, ...)` |
| apps/cli/commands/job_stop_cmd.py | +8/-11 | `_print_status`, and `_cmd_job_stop`'s two success sites, answer `emit_ok(...)`; the two sites whose old document carried `"ok": True` drop it |
| apps/cli/commands/roadmap_cmd.py | +10/-9 | `_cmd_roadmap_status` and `_cmd_roadmap_next` answer `emit_ok(...)` |
| apps/cli/commands/snapshot_cmds.py | +3/-4 | `_cmd_snapshot_inspect` and `_cmd_snapshot_list_applies` answer `emit_ok(**out)` |
| apps/cli/commands/test_cmds.py | +9/-7 | `_cmd_discover_commands` and `_cmd_test_status` answer `emit_ok(...)`; `_cmd_run_tests`'s failed-run path answers `emit_error("test_run_failed", ..., **document)` then the existing `sys.exit(1)`, because `document` (`asdict(result)`) carries `exit_code` (D10 (3)) |
| tests/cli/test_contract_cmd.py | +3/-2 | the two exact-body pins (`test_json_carries_the_stored_body`, `test_a_job_in_no_mission_is_one_sentence_and_null`) gain `"schema_version": 1, "ok": True` |
| tests/cli/test_json_envelope.py | +1/-11 | the ratchet dict loses the ten HALF A modules; pinned total 122→98 |
| tests/orchestration/test_data_reclaim.py | +4/-0 | the three `set(body) == {...}` key-set pins and the one byte-for-byte `json.dumps(expected, sort_keys=True)` pin each gain `schema_version`/`ok` |

Measured insertions: **85** (7+10+4+12+4+10+8+10+3+9+3+1+4); 96 deletions.

### 1be65fe7 F283 R17 C6: ten more command modules answer --json success in the envelope (D10)
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/dev.py | +1/-1 | `_dev_status` answers `emit_ok(**status)` |
| apps/cli/commands/failure_stats_cmd.py | +2/-3 | `_cmd_stats_failures` answers `emit_ok(**result)` |
| apps/cli/commands/file.py | +2/-3 | `_cmd_file_why` answers `emit_ok(**export_file_provenance_json(prov))` |
| apps/cli/commands/init_cmd.py | +2/-4 | `_handle_init` answers `emit_ok(steps=steps, summary=summary)` in place of `_json.dump(..., indent=2)` + a bare `print()` |
| apps/cli/commands/integrity_cmd.py | +10/-5 | `_cmd_integrity_check`: a passing gate answers `emit_ok(**document)`; a failing one answers ONE `fail("integrity_failed", ..., json_output=True, **document)` instead of a raw document followed by a bare `sys.exit(1)` (D10 (3), reached by the same rule though the block did not name this module's failure path by hand) — the text branch's `sys.exit(1)` after `summarize_integrity` is unchanged |
| apps/cli/commands/job_context_cmd.py | +2/-3 | `_cmd_job_context` answers `emit_ok(**result)` |
| apps/cli/commands/status_cmd.py | +3/-2 | `_cmd_status` answers `emit_ok(**result)` |
| apps/cli/commands/study_cmd.py | +10/-9 | `_cmd_study_run` answers `emit_ok(...)` |
| apps/cli/commands/teacher_cmd.py | +18/-20 | `_cmd_teacher_narrate` and `_cmd_teacher_ask` answer `emit_ok(...)` |
| apps/cli/commands/worker_facade_cmd.py | +2/-3 | `_cmd_doctor_core` answers `emit_ok(**result)` |
| tests/cli/test_failure_cmd.py | +3/-0 | `test_the_filters_reach_the_aggregator` gains `schema_version`/`ok` assertions on the success document |
| tests/cli/test_file_provenance_cli.py | +6/-0 | `test_file_why_json_no_private_path_leak` gains the same |
| tests/cli/test_init_cmd.py | +3/-0 | `test_json_output_valid` gains the same |
| tests/cli/test_job_context_cmd.py | +5/-1 | the shared `_run_json` helper asserts `schema_version`/`ok` once, covering every caller |
| tests/cli/test_json_envelope.py | +1/-11 | the ratchet dict loses the ten HALF B modules; pinned total 98→87 |
| tests/cli/test_scoped_listings.py | +3/-0 | `test_status_scoped` gains the same |
| tests/cli/test_study_cmd.py | +3/-0 | `test_study_run_writes_cards_for_a_fixture_repo` gains the same |
| tests/cli/test_teacher_cmd.py | +3/-0 | `test_json_output_carries_the_row_id_and_the_billed_flag` gains the same |
| tests/cli/test_worker_facade_cmd.py | +3/-0 | `test_core_all_ready` gains the same |
| tests/orchestration/test_integrity_gate.py | +43/-0 | new `TestIntegrityCheckJSONEnvelope`: a passing gate answers `emit_ok`; a failing one answers one `integrity_failed` envelope and exits 1 — `integrity_cmd.py` had no existing CLI-level test, so this is the module's whole D10 test obligation |
| tests/regression/test_named_bugs.py | +3/-0 | `test_dev_status_json` gains `schema_version`/`ok` assertions |

Measured insertions: **128** (1+2+2+2+10+2+3+10+18+2+3+6+3+5+1+3+3+3+3+43+3); 65 deletions.

### afc06b7f F283 R17 C6-fix: pin test run --json's failure envelope (D10 (3))
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_test_run_runtime.py | +6/-1 | `test_failing_repo_json` gains `schema_version == 1`, `ok is False`, `error == "test_run_failed"`; `r.returncode != 0` tightened to `== 1` |

Measured insertions: **6** (unordered fix-forward; see Deviations). 1 deletion.

### C7 — THE HANDBACK (this commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the 500-line cap under DECISION F104 D1 |

Self-reference exception (handback template, R-0149 pattern): a handback cannot
table the commit that writes it.

## External actions

- `git worktree add .remedy-wt/f283-r17-worker HEAD` at C6 (`1be65fe7`) for
  G5 — used for the unmutated control (run twice; the first run built the
  UI and reddened seven UI-integration tests, the second read clean) and
  all six named mutation red-proofs, each reverted with `git checkout --`
  before the next.
- After C6-fix landed, `git -C .remedy-wt/f283-r17-worker checkout afc06b7f`
  moved the same worktree onto the corrected tree; the control was re-run
  once more (442 passed, 6 skipped) before mutations (e) and (f) — the only
  two whose files the fix touched or whose target moved — were re-proved
  against it; (a), (b), (c), (d) were already proved against `1be65fe7` and
  the fix touched neither their files nor their targets.
- `git worktree remove .remedy-wt/f283-r17-worker --force` after G5.
- `git push origin feature/f283-machine-contracts-part-two` after C7 — real
  outcome reported in the session reply, since it ships this very file.
- `gh pr list --state open ...` after the push — real outcome reported in
  the session reply.
- **NOTHING IS MERGED.** No `gh pr merge`, no `gh pr create`, no checkout of
  `main`, no branch deletion.
- No worktree other than the one disposable G5 worktree above was added; it
  was removed. `git worktree list` shows the primary checkout alone both
  before C1 and again here before C7.

## Verification

### G1 — PAYLOADS transport, then four authored copies

| file | lines measured/given | bytes measured/given | sha256 equal |
|---|---|---|---|
| ledger.md | 4/4 | 5061/5061 | True |
| decisions.md | 40/40 | 3155/3155 | True |
| plan.md | 37/37 | 1636/1636 | True |

**All readings equal: True.**

Four `.agent/authored/f283-r17-*` copies (the block copy plus three
payloads), each read back from the committed tree with
`git show 6631e250:<path>` and compared byte-for-byte with its source:

| copy | equal to source |
|---|---|
| f283-r17-block.md | True |
| f283-r17-ledger.md | True |
| f283-r17-decisions.md | True |
| f283-r17-plan.md | True |

**Copies compared: 4. All True.**

### G2 — THE BOOKING

**(a) Append arithmetic**, by strict byte concatenation, pre-file read at
`488fd05a`:

| file | pre | payload | post | pre+payload==post |
|---|---|---|---|---|
| .agent/live_review.md | 524486 | 5061 | 529547 | True |
| .agent/decisions.md | 1823772 | 3155 | 1826927 | True |

Matches the block's stated compositions exactly.

**(b) Line-anchored on the committed ledger**: `^Gate: F283 R16 — ` = **1**,
`^- R-1030 — ` = **1**. Open set by distinct id, via `open_finding_ids` from
`scripts/rotate_live_review.py` (imported and called directly):

| rev | OPEN by distinct id |
|---|---|
| `488fd05a` | **24** |
| C2 (`6b5e6e9b`) | **25** |

Added: `["R-1030"]`. Removed: `[]`. Matches the block's stated 24 → 25,
ADDED `R-1030`, REMOVED empty, exactly.

**(c) `.agent/plan.md` at C2 equals plan.md byte-for-byte**: sha256-equal to
the payload (`9b0cda9c028c12389e30ebe0b6cd0de4c14c7ab4087dcaa94b11afa230c5372f`
both). Line count: **37**, under the AGENTS.md 50-line rule.

### G3 — THE CHANGE, COUNTED FROM THE TREE

`git diff --name-only <parent> <commit>` and `git show --numstat` insertions:

| commit | paths changed | insertions |
|---|---|---|
| C3 `6b5e6e9b`→`81d28ed4` | .agent/live_review.md, packages/orchestration/ui_server.py, tests/cli/test_project_current.py, tests/ui_server/test_live_state.py | 76 |
| C4 `81d28ed4`→`ccbc428a` | tests/cli/test_json_envelope.py | 97 |
| C5 `ccbc428a`→`dbc49b6b` | the ten HALF A modules + tests/cli/test_contract_cmd.py, tests/cli/test_json_envelope.py, tests/orchestration/test_data_reclaim.py | 85 |
| C6 `dbc49b6b`→`1be65fe7` | the ten HALF B modules + 11 test files | 128 |

`raw_sites.py .`'s TOTAL line:

| when | TOTAL | modules |
|---|---|---|
| `488fd05a` (block's own reading) | 122 | 34 |
| after C4 | 122 | 34 (unchanged — C4 is test-only) |
| after C5 | 98 | 24 |
| after C6 | 87 | 14 |

Module rows left after C6 (the fourteen larger modules for round 18's
second batch, unchanged by this round):

    13 apps/cli/commands/job.py
    11 apps/cli/commands/mission_cmd.py
     8 apps/cli/commands/self_cmd.py
     7 apps/cli/commands/project.py
     6 apps/cli/commands/config_cmd.py
     6 apps/cli/commands/worker.py
     5 apps/cli/commands/brain.py
     5 apps/cli/commands/do_cmd.py
     5 apps/cli/commands/real_test_execution_cmd.py
     5 apps/cli/commands/runtime_cmd.py
     4 apps/cli/commands/event.py
     4 apps/cli/commands/memory.py
     4 apps/cli/commands/patch.py
     4 apps/cli/commands/stats_ledger_cmd.py

At C3, the `Landed: R-1030 — ` line reads: "the comment above the
function-scoped `apps.cli.json_envelope` import in `start_ui_server` now
names `_command_is_ui_exposed`, this same file, as the precedent, with no
claim about `apps/cli/json_envelope.py`; landed at this round's C3." The
new comment reads: "F283 R16 C5 (DECISION F283 D9), comment repaired at
R-1030: imported inside the function, the idiom this module's own
`_command_is_ui_exposed` already uses for `apps.cli.command_catalog` —
this module lives under `packages/` and must not take an `apps/` import at
module scope."

Every token the round's `fail(`/`emit_error(` calls introduce or reuse
(searched the whole round's diff under `apps/cli/commands/`), each with its
`git grep -c` count over `apps/` at `488fd05a`:

| token | introduced in | count at `488fd05a` | new or reused |
|---|---|---|---|
| test_run_failed | test_cmds.py (C5) | 0 | **new** |
| integrity_failed | integrity_cmd.py (C6) | 0 under `apps/` | reused — already spelled in `packages/orchestration/mission_readiness.py` |

`git diff --name-only 488fd05a 1be65fe7 -- packages/` prints
**`packages/orchestration/ui_server.py`** alone.

### G4 — TARGETED SELECTION, ruff, integrity

`.remedy-wt/f283-r17-scratch/selection.txt`: **299** space-separated paths
(`-n auto`). The block's `488fd05a` reading: `11250 passed, 13 skipped`,
exit 0.

| when | exit code | summary |
|---|---|---|
| after C3 | 0 | 11254 passed, 13 skipped |
| after C4 | 0 | 11256 passed, 13 skipped |
| after C5 | 0 | 11256 passed, 13 skipped |
| after C6 | 0 | 11258 passed, 13 skipped |
| after C6-fix | 0 | 11258 passed, 13 skipped (same test count; two assertions strengthened, none added) |

Zero failed, zero errors at each; the passed count only rose (+4 at C3, +2
at C4, +0 at C5, +2 at C6; skipped unchanged at 13 throughout).

`python3 -m ruff check` over every `.py` path the round touched (36 paths:
the twenty converted modules, `packages/orchestration/ui_server.py`, and
fifteen touched test files plus `tests/cli/test_test_run_runtime.py`), run
after C6-fix: **All checks passed!**

`python3 -m apps.cli.main integrity check --json`, run after C6-fix:
`"passed": true, "fail_count": 0`, all five checks (`handler_import`,
`live_review_verdict`, `plan_consistency`, `relevant_untracked`,
`high_blockers_open`) read `"status": "pass"`.

`python3 -m pytest tests/cli/test_golden_path.py -q`, run once after C6:
**42 passed**, exit 0 (unaffected by C6-fix, which touches no golden-path
file).

### G5 — RED-PROOFS

Disposable worktree `.remedy-wt/f283-r17-worker` at C6 (`1be65fe7`), never
committed, later moved to `afc06b7f` after the fix-forward commit landed.
Files: `tests/cli/test_project_current.py`, `tests/ui_server/test_live_state.py`,
`tests/cli/test_json_envelope.py`, and every test file C5 and C6 changed —
`tests/cli/test_contract_cmd.py`, `tests/orchestration/test_data_reclaim.py`,
`tests/cli/test_failure_cmd.py`, `tests/cli/test_file_provenance_cli.py`,
`tests/cli/test_init_cmd.py`, `tests/cli/test_job_context_cmd.py`,
`tests/cli/test_scoped_listings.py`, `tests/cli/test_study_cmd.py`,
`tests/cli/test_teacher_cmd.py`, `tests/cli/test_worker_facade_cmd.py`,
`tests/orchestration/test_integrity_gate.py`,
`tests/regression/test_named_bugs.py` — fifteen files, run together as the
control, TWICE:

| step | exit code | result |
|---|---|---|
| control run 1 (fresh worktree, builds the UI) | 1 | 7 failed, 412 passed, 6 skipped |
| control run 2 | 0 | 419 passed, 6 skipped |

The seven reds of run 1 are `TestUIServerIntegration`/`TestUIStartAnswersTheEnvelope`
cases inside `tests/ui_server/test_live_state.py`, all from `npm run build`
failing (`npm` not installed in this sandbox) the FIRST time `dist/` is
missing; every later run passes them, matching the round 16 precedent
exactly. Every mutation below is judged against run 2 (419 passed).

| mutation | exit code | result | failing test(s) |
|---|---|---|---|
| (a) `project attach-job`'s envelope carries `added=True` always | 1 | 1 failed, 29 passed (file-scoped) | `TestProjectCreateAndAttachAnswerJSONThroughTheDispatcher::test_attach_job_already_attached_answers_added_false` |
| (b) `ui stop`'s `failed` entries drop `error` | 1 | 1 failed, 57 passed (file-scoped) | `TestUISessionCommandsAnswerTheEnvelope::test_stop_kill_failure_answers_a_failed_entry` |
| (c) `start_ui_server` answers a 404 job with `invalid_job_id` | 1 | 1 failed, 57 passed (file-scoped) | `TestUIStartAnswersTheEnvelope::test_missing_job_answers_job_not_found` |
| (d) one converted `blocker list --json` site goes back to `print(_json.dumps(...))` | 1 | 1 failed, 32 passed (file-scoped, `test_json_envelope.py` + `test_blocker_cmd.py` together) | `TestRawJSONDocumentSitesRatchet::test_the_pinned_counts_match_the_scan` — no other test failed alongside it; `test_blocker_cmd.py`'s own tests all stayed green because the mutation's bytes are otherwise identical to what the envelope would have written minus `schema_version`/`ok` |
| (e) `test run --json` on a failed run answers `emit_ok` | 1 | 1 failed, 22 passed (file-scoped, re-proved against `afc06b7f` after the fix) | `TestFailingRun::test_failing_repo_json` |
| (f) `dev status --json` prints its raw document again | 1 | 1 failed, 58 passed, 6 skipped (file-scoped) | `TestDevStatusCommandSchema::test_dev_status_json` |

Each mutation reddened exactly its named target(s) — (d) additionally
confirmed no OTHER test failed alongside the ratchet — and nothing else.
Each was reverted with `git checkout --` and confirmed clean
(`git status --porcelain`, empty) before the next.
`git worktree remove .remedy-wt/f283-r17-worker --force` afterward.
`git worktree list` (post-removal): the primary checkout alone —
`/home/decodeux/Repos/remedy afc06b7f [feature/f283-machine-contracts-part-two]`.

## Deviations & assumptions

1. **One unordered commit this round: C6-fix (`afc06b7f`).** Self-review
   after C5 found that `_cmd_run_tests`'s new failure-envelope conversion
   (D10 (3), `emit_error("test_run_failed", ...)`) had NO test asserting
   the envelope's `ok`/`error` shape — the existing
   `test_failing_repo_json` asserted only `out["status"]` and
   `out["exit_code"]`, both of which are present and unchanged whether the
   path answers `emit_ok` or `emit_error`, so mutation (e) above would have
   reddened nothing had this fix not landed. Caught while building G5's
   mutation list, before any red-proof ran, not by a red gate. Fixed
   forward with one commit adding three assertions
   (`schema_version == 1`, `ok is False`, `error == "test_run_failed"`) and
   tightening `r.returncode != 0` to `== 1`; no product file changed. The
   disposable G5 worktree was moved onto `afc06b7f` and the control and
   mutations (e)/(f) re-proved against it; (a)-(d) were already proved
   against `1be65fe7` and the fix touched neither their files nor targets.
2. **`integrity_cmd.py`'s failure path is converted though the block named
   only its success document.** DECISION F283 D10 (3)'s rule ("a path that
   prints a result document and then exits non-zero answers ONE failure
   envelope instead") reaches `_cmd_integrity_check` exactly as it reaches
   `test_cmds.py`'s: the old code printed `export_integrity_json(result)`
   unconditionally then called `sys.exit(1)` when `not result.passed`. The
   document carries no key colliding with `fail()`'s own parameters, so the
   failure path calls `fail("integrity_failed", ..., json_output=True,
   **document)` directly rather than `emit_error()` + `sys.exit()`; the
   token `integrity_failed` is REUSED from
   `packages/orchestration/mission_readiness.py` per DECISION F277 D8 part
   (a)'s "the existing spelling wins" rule. `integrity_cmd.py` had no
   existing CLI-level test file, so its whole D10 test obligation (a
   passing-gate `emit_ok` test and a failing-gate `integrity_failed` test)
   is new, added to `tests/orchestration/test_integrity_gate.py` in C6.
3. **Constraints 1, 2, 3, 4, 6 and 7 held throughout.** No payload was
   edited or retyped; every commit stayed under 500 insertions (285, 60,
   76, 97, 85, 128, 6; this handoff exempt as a single `.agent/**` state
   file); the round's tracked path set (44 distinct paths before this
   commit, 45 after) is EXACTLY constraint 3's full enumeration, with
   nothing outside it and nothing missing; `packages/` shows exactly the
   one file the block predicts (`packages/orchestration/ui_server.py`);
   every commit from C3 on left selection A at zero failed and zero
   errors, the passed count only rising; nothing was merged, no PR
   created, no checkout of `main`; the one G5 worktree was removed as its
   own last action.

### The round's whole tracked path set (before this commit)

`git diff --name-only 488fd05a afc06b7f` — **44** distinct paths; plus
`.agent/handoff.md` from this commit makes **45** — EXACTLY constraint 3's
full enumeration (4 authored copies + 3 `.agent/**` state files + 1
`packages/` file + 20 converted modules + 16 distinct test files +
`.agent/handoff.md`):

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f283-r17-block.md | C1 `6631e250` |
| 2 | .agent/authored/f283-r17-decisions.md | C1 `6631e250` |
| 3 | .agent/authored/f283-r17-ledger.md | C1 `6631e250` |
| 4 | .agent/authored/f283-r17-plan.md | C1 `6631e250` |
| 5 | .agent/decisions.md | C2 `6b5e6e9b` |
| 6 | .agent/live_review.md | C2 `6b5e6e9b`, appended again by C3 `81d28ed4` |
| 7 | .agent/plan.md | C2 `6b5e6e9b` |
| 8 | packages/orchestration/ui_server.py | C3 `81d28ed4` |
| 9 | tests/cli/test_project_current.py | C3 `81d28ed4` |
| 10 | tests/ui_server/test_live_state.py | C3 `81d28ed4` |
| 11 | tests/cli/test_json_envelope.py | C4 `ccbc428a`, touched again by C5 `dbc49b6b` and C6 `1be65fe7` |
| 12 | apps/cli/commands/bench_cmd.py | C5 `dbc49b6b` |
| 13 | apps/cli/commands/blocker.py | C5 `dbc49b6b` |
| 14 | apps/cli/commands/change.py | C5 `dbc49b6b` |
| 15 | apps/cli/commands/contract_cmd.py | C5 `dbc49b6b` |
| 16 | apps/cli/commands/data_cmd.py | C5 `dbc49b6b` |
| 17 | apps/cli/commands/decision.py | C5 `dbc49b6b` |
| 18 | apps/cli/commands/job_stop_cmd.py | C5 `dbc49b6b` |
| 19 | apps/cli/commands/roadmap_cmd.py | C5 `dbc49b6b` |
| 20 | apps/cli/commands/snapshot_cmds.py | C5 `dbc49b6b` |
| 21 | apps/cli/commands/test_cmds.py | C5 `dbc49b6b` |
| 22 | tests/cli/test_contract_cmd.py | C5 `dbc49b6b` |
| 23 | tests/orchestration/test_data_reclaim.py | C5 `dbc49b6b` |
| 24 | apps/cli/commands/dev.py | C6 `1be65fe7` |
| 25 | apps/cli/commands/failure_stats_cmd.py | C6 `1be65fe7` |
| 26 | apps/cli/commands/file.py | C6 `1be65fe7` |
| 27 | apps/cli/commands/init_cmd.py | C6 `1be65fe7` |
| 28 | apps/cli/commands/integrity_cmd.py | C6 `1be65fe7` |
| 29 | apps/cli/commands/job_context_cmd.py | C6 `1be65fe7` |
| 30 | apps/cli/commands/status_cmd.py | C6 `1be65fe7` |
| 31 | apps/cli/commands/study_cmd.py | C6 `1be65fe7` |
| 32 | apps/cli/commands/teacher_cmd.py | C6 `1be65fe7` |
| 33 | apps/cli/commands/worker_facade_cmd.py | C6 `1be65fe7` |
| 34 | tests/cli/test_failure_cmd.py | C6 `1be65fe7` |
| 35 | tests/cli/test_file_provenance_cli.py | C6 `1be65fe7` |
| 36 | tests/cli/test_init_cmd.py | C6 `1be65fe7` |
| 37 | tests/cli/test_job_context_cmd.py | C6 `1be65fe7` |
| 38 | tests/cli/test_scoped_listings.py | C6 `1be65fe7` |
| 39 | tests/cli/test_study_cmd.py | C6 `1be65fe7` |
| 40 | tests/cli/test_teacher_cmd.py | C6 `1be65fe7` |
| 41 | tests/cli/test_worker_facade_cmd.py | C6 `1be65fe7` |
| 42 | tests/orchestration/test_integrity_gate.py | C6 `1be65fe7` |
| 43 | tests/regression/test_named_bugs.py | C6 `1be65fe7` |
| 44 | tests/cli/test_test_run_runtime.py | C6-fix `afc06b7f` |
| 45 | .agent/handoff.md | C7 (this commit) |

No path outside constraint 3's enumeration was touched: `.agent/candidates.md`,
`.agent/context.md`, `.agent/operator_questions.md`, `.agent/prose_slips.md`,
`README.md`, `docs/**`, `scripts/**` appear **0** times.

## Authored-text proofs

- The four copies at C1, compared with the block's originals under
  `.remedy-wt/f283-r17-payloads/` and `.remedy-wt/f283-r17-block.md`: **four
  readings, all True** (G1).
- The two APPEND payloads against their committed files: strict byte
  concatenation True for `.agent/live_review.md` (ledger.md) and
  `.agent/decisions.md` (decisions.md), byte numbers equal to the block's
  (G2a).
- The one REWRITE payload against its committed file: `.agent/plan.md`'s
  committed sha256 equals the payload's sha256 (G2c).
- No payload was edited or retyped. The block copy and three payload copies
  were made with `shutil.copyfile`; the two appends by reading each
  payload's bytes and writing base+payload back to disk; the plan.md
  rewrite by `shutil.copyfile`.
- Every change under `apps/`, `packages/` and `tests/` this round was
  WORKER-authored to the block's SPEC and DECISION F283 D10 — there is no
  reviewer-authored diff to compare against for those files; G3/G4/G5 above
  are the proof they meet the SPEC.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Pre-flight (STOP, git state, block self-verify) | done | no STOP; tree clean at `488fd05a`; block 204 lines / matching sha256 |
| C1 copy block + 3 payloads | done | 285 insertions |
| C2 book round 16 PASS, register R-1030, record D10 | done | 60 insertions (40+4+16, 13 deletions from plan rewrite); open set 24→25, added R-1030 |
| C3 repair R-1030's comment; pin attach-job, ui stop, ui start | done | 76 insertions |
| C4 the raw-document ratchet | done | 97 insertions; base reading 122 modules 34 |
| C5 HALF A: ten command modules answer --json success | done | 85 insertions; ratchet 122→98 |
| C6 HALF B: ten more command modules answer --json success | done | 128 insertions; ratchet 98→87 |
| C6-fix pin test run --json's failure envelope | deviated | unordered fix-forward, 6 insertions; see Deviations #1 |
| C7 the handback | done | this commit |
| G1 payload transport + authored copies | done | 3/3 payload readings equal; 4/4 authored copies byte-identical |
| G2(a) live_review.md + decisions.md append | done | 524486+5061=529547; 1823772+3155=1826927 |
| G2(b) open set by distinct id | done | 1 Gate line, 1 R-1030 line; 24→25, added R-1030, removed none |
| G2(c) plan.md rewrite | done | sha256-equal to payload; 37 lines, under 50 |
| G3 change counted from the tree | done | per-commit diffs and insertions reported; ratchet 122→98→87; Landed line and new comment text quoted; two tokens (`test_run_failed` new, `integrity_failed` reused); exactly 1 path under `packages/` |
| G4 targeted selection, ruff, integrity, golden path | done | 11254/11256/11256/11258 passed after C3/C4/C5/C6 (up from 11250), 0 failed/errors at each, unchanged at 11258 after the fix; ruff exit 0 over 36 paths; integrity all 5 pass, fail_count 0; golden path 42 passed |
| G5 red-proofs (a)(b)(c)(d)(e)(f) | done | all six go RED, each reddening exactly its named target(s), (d) confirmed alone; unmutated control run twice (7 failed→419 passed, the UI-build pattern); (e)/(f) re-proved after the fix |
| G6 tree, push, PR list | pending at write time | reported in the worker's session reply with real exit codes |
| Constraint 1 no payload edited/retyped | done | `shutil.copyfile`, byte concatenation only |
| Constraint 2 every commit under 500 insertions | done | 285, 60, 76, 97, 85, 128, 6; this handoff exempt as single `.agent/**` state file |
| Constraint 3 no unnamed file touched | done | 44 paths before this commit (45 after), EXACTLY the full enumeration |
| Constraint 4 G4 selection at zero failed after every commit | done | 11254/11256/11256/11258 passed, 0 failed/errors at each |
| Constraint 5 STOP if a gate goes red outside constraint 3's path set | done (n/a) | no gate went red outside the named paths; no STOP was needed |
| Constraint 6 nothing is merged | done | no `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch deletion |
| Constraint 7 G5 worktree under .remedy-wt/, removed, listed | done | `.remedy-wt/f283-r17-worker`, removed, `git worktree list` reported after; no other worktree disturbed |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 17 — C1 through C7 plus the C6-fix deviation, all
   six gates re-derived.
3. Then T002's second batch, as `.agent/plan.md` lists it: the fourteen
   modules with the most raw-document sites (`job`, `mission`, `self`,
   `project`, `config`, `worker`, `brain`, `do`, `test`, `runtime`,
   `event`, `memory`, `patch`, `stats`), leaving the ratchet at the
   text-branch survivors.

Open findings count: **25** (R-1030 landed, awaiting review). Operator-questions
count: **0**.
