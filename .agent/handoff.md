# Handoff — F283 Machine contracts, part two: refusal sweep, JSON gap, exit-code taxonomy · Round 18 · T002's success half, second batch (D10)

## Session

SESSION 4 of feature F283 · round 18 · rounds so far 18

This round booked round 17's PASS, registered and repaired R-1031 (seven
round-17-converted modules — `job_stop_cmd.py`, `change.py`, `bench_cmd.py`,
`blocker.py`, `decision.py`, `roadmap_cmd.py`, `snapshot_cmds.py` — had no
test that would notice their envelope breaking; one test per module now runs
through the real CLI dispatcher, `apps.cli.grouped.main`, asserting
`schema_version` 1, `ok` true and an old-document key), resolved R-1030 on
the record (it landed at round 17's own C3, re-derived clean by this round's
reviewer), then converted the eight modules the block named to DECISION
F283 D10's envelope: HALF A (`runtime_cmd.py`, `do_cmd.py`,
`real_test_execution_cmd.py`, `event.py`) and HALF B (`memory.py`,
`patch.py`, `stats_ledger_cmd.py`, `brain.py`). Every raw
`print(<json>.dumps(...))` site in those eight modules now answers
`emit_ok(**document)`. Three sites needed more than a mechanical wrap:
`do_cmd.py`'s `run list --json` answered a bare list today and, on an EMPTY
store, printed the TEXT prose line even under `--json` (the routing bug the
block named by hand) — it now always answers `emit_ok(runs=<the list>)`
under `--json`, the prose line staying in the text branch, and the three
tests that pinned the old shape were repaired (D10 (4)); `patch.py`'s
`_cmd_revert_patch_intent` and `stats_ledger_cmd.py`'s
`_cmd_stats_verify_ledger` each printed a result document THEN exited
non-zero on failure — both now answer ONE failure envelope under `--json`
(`fail(<token>, ...)`) instead (D10 (3)), the revert path's token drawn from
`result.block_reason` (reusing this module's own pre-check vocabulary) or
`result.state`, the verify-ledger path's token a new one, `ledger_drift`.
`real_test_execution_cmd.py`'s `snapshot create`/`snapshot show` success
documents carry their OWN `schema_version` (a domain string,
`SnapshotProof.to_dict()`'s record-schema version, unrelated to and
predating the envelope's integer of the same name) — `emit_ok()` refuses a
payload carrying that reserved key by name, so a small helper,
`_envelope_safe`, renames it to `record_schema_version` (value unchanged)
before the two calls. Twenty tests across eight files pinned the OLD exact
key-set or byte shape and are repaired, keeping what each asserted (per the
reviewer's `dry_a_bad.txt` dry run); the per-module test obligation is met
for every one of the eight modules, each with an explicit
`schema_version == 1` / `ok is True` (or, for the two D10 (3) sites, `ok is
False` / the failure token) assertion, not merely a key-set membership
check. The ratchet now names only the six modules T002's last batch will
convert (`job.py`, `mission_cmd.py`, `self_cmd.py`, `project.py`,
`config_cmd.py`, `worker.py`; 51 raw sites).
Context self-assessment: roughly half the working budget remained at the
point this handoff was written.

## Range

Review of `9f36956f`..`HEAD`.

## Block self-verification (R-0954)

| reading | measured | given | equal |
|---|---|---|---|
| line count | 198 | 198 | True |
| sha256 | `5d35abf842b668da03744be36c16713bbb7e143ad757d517850ad89e83600d86` | `5d35abf842b668da03744be36c16713bbb7e143ad757d517850ad89e83600d86` | True |

Neither reading differed, so the round went ahead.

## Pre-flight

- `ls .agent/STOP`: `No such file or directory`. No STOP on disk.
- `git status --porcelain`: empty.
- `git branch --show-current`: `feature/f283-machine-contracts-part-two`.
- `git log --oneline -1`: `9f36956f`, matching the delegation message.

## Commits

### 0f81a255 F283 R18 C1: copy round 18 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r18-block.md | +198/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f283-r18-ledger.md | +6/-0 | byte-for-byte copy of ledger.md |
| .agent/authored/f283-r18-plan.md | +35/-0 | byte-for-byte copy of plan.md |

Measured insertions (`git show --numstat`): **239** (198+6+35).

### ba8d29cd F283 R18 C2: book round 17's PASS, register R-1031, resolve R-1030
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | append ledger.md by strict byte concatenation: the round-17 `Gate:` entry, R-1031's registration, R-1030's `Done:` paragraph |
| .agent/plan.md | +9/-11 | rewrite to plan.md payload, byte-identical; git's line diff shows only the lines that changed |

Measured insertions: **15** (6+9); 11 deletions from the plan.md rewrite.

### ebfb6cc8 F283 R18 C3: pin the envelope of seven round-17 modules (R-1031)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +1/-0 | the one `Landed: R-1031 — ...` line, appended, nothing else |
| tests/cli/test_blocker_cmd.py | +18/-0 | new `TestBlockerListAnswersJSONThroughTheDispatcher`: `blocker list`, through `apps.cli.grouped.main`, asserts `schema_version`/`ok`/`job_id` |
| tests/cli/test_change_proof_cli.py | +21/-0 | new `test_change_proof_answers_the_envelope_through_the_dispatcher`: `change proof` through `main`, asserts `schema_version`/`ok`/`version` |
| tests/cli/test_decision_cmd.py | +18/-0 | new `TestDecisionListAnswersJSONThroughTheDispatcher`: `decision list` through `main` |
| tests/cli/test_job_stop.py | +15/-0 | new `TestJSONThroughTheDispatcher::test_stop_answers_the_envelope`: `job stop` through `main` |
| tests/cli/test_plan_cli.py | +4/-0 | `TestRoadmapNext::test_json_shape` gains `schema_version`/`ok` assertions (subprocess dispatcher, pre-existing) |
| tests/cli/test_snapshot_cli_runtime.py | +20/-0 | new `test_answers_the_envelope_for_a_real_job`: `snapshot list-applies` through the subprocess dispatcher |
| tests/cli/test_stats_bench.py | +14/-0 | new `test_answers_the_envelope_through_the_argv_dispatcher`: `stats bench` through `main` |

Measured insertions: **111** (1+18+21+18+15+4+20+14).

### f35d07d1 F283 R18 C4: runtime, do, test and event answer --json success in the envelope (D10)
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/do_cmd.py | +9/-10 | `_cmd_run_show`, `_cmd_job_run`, `_cmd_job_evidence`, `_cmd_job_apply` answer `emit_ok(...)`; `_cmd_run_list` restructured so `--json` ALWAYS answers `emit_ok(runs=<the list>)`, even when empty — the empty check moves after the `json_output` branch, fixing the bug where an empty store printed the TEXT prose line even under `--json` (D10 (4)) |
| apps/cli/commands/event.py | +13/-14 | `_cmd_event_list`, `_cmd_event_show`, `_cmd_event_timeline`, `_cmd_event_replay` answer `emit_ok(...)` |
| apps/cli/commands/real_test_execution_cmd.py | +25/-7 | `_cmd_test_result`, `_cmd_test_list`, `_cmd_test_integrity` answer `emit_ok(...)`; `_cmd_snapshot_create`/`_cmd_snapshot_show` route through a new `_envelope_safe` helper that renames a document's own `schema_version` key to `record_schema_version` before `emit_ok`, since `SnapshotProof.to_dict()` carries that key already and `emit_ok` refuses a reserved-name clash |
| apps/cli/commands/runtime_cmd.py | +8/-9 | `_cmd_runtime_serve` (two sites), `_cmd_runtime_probe` (two sites), `_cmd_runtime_stop` answer `emit_ok(...)`; every site whose payload's own `to_json()` carried `"ok"` filters it out first (D10 (2)) |
| tests/cli/test_cli_ux.py | +25/-4 | `TestRunList`'s three tests repaired for the `runs` key; a new `test_empty_store_answers_the_envelope_with_an_empty_runs_list` (D10 (4)'s obligation) plus its text-mode sibling |
| tests/cli/test_event_list_cmd.py | +15/-0 | new `test_the_success_document_answers_the_envelope`: `schema_version`/`ok`/`job_id`/`version` on `event list`'s converted output |
| tests/cli/test_json_envelope.py | +1/-5 | the ratchet dict loses the four HALF A modules; pinned total 87→68 |
| tests/cli/test_real_test_execution_cli.py | +13/-1 | `test_snapshot_create_show` gains `schema_version`/`ok`/`record_schema_version` assertions |
| tests/cli/test_runtime_cmd.py | +3/-0 | `test_serve_starts_and_leaves_the_server_running` gains a `schema_version == 1` assertion |

Measured insertions: **112** (9+13+25+8+25+15+1+13+3); 50 deletions.

### 8abd1553 F283 R18 C5: memory, patch, stats and brain answer --json success in the envelope (D10)
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/brain.py | +13/-15 | `_cmd_brain`, `_cmd_brain_node`, `_cmd_viewer_path`, `_cmd_context`, `_cmd_brain_continue` answer `emit_ok(...)` |
| apps/cli/commands/memory.py | +14/-15 | `_cmd_memory_recall`, `_cmd_memory_list`, `_cmd_memory_learn`, `_cmd_memory_card_show` answer `emit_ok(...)` |
| apps/cli/commands/patch.py | +22/-17 | `_cmd_list_patch_intents`, `_cmd_apply_patch_intent`, `_cmd_approve_hunks` answer `emit_ok(...)`; `_cmd_revert_patch_intent` restructured under D10 (3) — success answers `emit_ok(**document)`, failure answers ONE `fail(<token>, ...)` where `<token>` is `result.block_reason or result.state or "revert_failed"` |
| apps/cli/commands/stats_ledger_cmd.py | +42/-33 | `_cmd_stats_cost`, `_cmd_stats_cache`, `_cmd_stats_backfill_ledger` answer `emit_ok(...)`; `_cmd_stats_verify_ledger` restructured under D10 (3) — a clean reconcile answers `emit_ok(**document)`, drift answers ONE `fail("ledger_drift", ..., exit_code=EXIT_DRIFT, **document)` instead of the raw document followed by a bare exit; the text branch is byte-for-byte unchanged, re-indented only |
| tests/cli/test_json_envelope.py | +1/-5 | the ratchet dict loses the four HALF B modules; pinned total 68→51, naming only the six text-branch-survivor modules T002's last batch converts |
| tests/cli/test_memory_cmd.py | +36/-0 | new `TestTheReadPathsAnswerTheEnvelope`: `memory card-show`/`recall`/`list` each asserted `schema_version`/`ok` |
| tests/cli/test_patch_cmd.py | +10/-5 | `test_json_output_is_the_exported_record` gains `schema_version`/`ok` assertions and excludes both from the stored-record equality check |
| tests/cli/test_stats_cost.py | +9/-0 | `TestCostJsonShape` gains `schema_version`/`ok`; `TestVerifyLedger::test_drift_is_visible_in_json_too` gains `schema_version`/`ok is False`/`error == "ledger_drift"` |
| tests/test_brain_detail.py | +2/-0 | `test_json_flag_top_level_keys`'s expected key set gains `schema_version`/`ok` |
| tests/test_brain_smoke.py | +2/-0 | the shared `_DETAIL_KEYS` constant gains `schema_version`/`ok`, covering all sixteen `TestBrainNodeJsonAllTypes`/`TestBrainLifecycle` cases |
| tests/test_context_coverage.py | +2/-0 | `_BRAIN_NODE_DETAIL_KEYS` gains the same two |
| tests/test_project_brain.py | +8/-1 | `test_json_flag_output_has_correct_top_level_keys` gains `schema_version == 1`/`ok is True` plus the two keys in its set |

Measured insertions: **161** (13+14+22+42+1+36+10+9+2+2+2+8); 91 deletions.

### C6 — THE HANDBACK (this commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the 500-line cap under DECISION F104 D1 |

Self-reference exception (handback template, R-0149 pattern): a handback cannot
table the commit that writes it.

## External actions

- `git worktree add .remedy-wt/f283-r18-redproof 8abd1553` at C5 for G5 —
  used for the unmutated control (run twice) and all six named mutation
  red-proofs, each reverted with `git checkout --` before the next.
- `git worktree remove .remedy-wt/f283-r18-redproof` after G5.
- `git push origin feature/f283-machine-contracts-part-two` after C6 — real
  outcome reported in the session reply, since it ships this very file.
- `gh pr list --state open ...` after the push — real outcome reported in
  the session reply.
- **NOTHING IS MERGED.** No `gh pr merge`, no `gh pr create`, no checkout of
  `main`, no branch deletion.
- No worktree other than the one disposable G5 worktree above was added; it
  was removed. `git worktree list` shows the primary checkout alone both
  before C1 and again here before C6.

## Verification

### G1 — PAYLOADS transport, then three authored copies

| file | lines measured/given | bytes measured/given | sha256 equal |
|---|---|---|---|
| ledger.md | 6/6 | 5779/5779 | True |
| plan.md | 35/35 | 1510/1510 | True |

**All readings equal: True.**

Three `.agent/authored/f283-r18-*` copies (the block copy plus two
payloads), each read back from the committed tree with
`git show 0f81a255:<path>` and compared byte-for-byte with its source:

| copy | equal to source |
|---|---|
| f283-r18-block.md | True |
| f283-r18-ledger.md | True |
| f283-r18-plan.md | True |

**Copies compared: 3. All True.**

### G2 — THE BOOKING

**(a) Append arithmetic**, by strict byte concatenation, pre-file read at
`9f36956f`:

| file | pre | payload | post | pre+payload==post |
|---|---|---|---|---|
| .agent/live_review.md | 529803 | 5779 | 535582 | True |

Matches the block's stated composition exactly (the reviewer's own reading,
535582).

**(b) Line-anchored on the committed ledger**: `^Gate: F283 R17 — ` = **1**,
`^- R-1031 — ` = **1**, `^Done: R-1030 — ` = **1**. Open set by distinct id,
via `open_finding_ids` from `scripts/rotate_live_review.py` (imported and
called directly):

| rev | OPEN by distinct id |
|---|---|
| `9f36956f` | **25** |
| C2 (`ba8d29cd`) | **25** |

Added: `["R-1031"]`. Removed: `["R-1030"]`. Matches the block's stated 25 →
25, ADDED `R-1031`, REMOVED `R-1030`, exactly.

**(c) `.agent/plan.md` at C2 equals plan.md byte-for-byte**: sha256-equal to
the payload (`cd1c8e349ce5525a1c038fab3f56ed50a9bbb4e3ed0ff03a9519d367faa15c41`
both). Line count: **35**, under the AGENTS.md 50-line rule.

### G3 — THE CHANGE, COUNTED FROM THE TREE

`git diff --name-only <parent> <commit>` and `git show --numstat` insertions:

| commit | paths changed | insertions |
|---|---|---|
| C3 `ba8d29cd`→`ebfb6cc8` | .agent/live_review.md + 7 test files (through-the-dispatcher tests, one per R-1031 module) | 111 |
| C4 `ebfb6cc8`→`f35d07d1` | the four HALF A modules + 5 test files | 112 |
| C5 `f35d07d1`→`8abd1553` | the four HALF B modules + 8 test files | 161 |

`raw_sites.py .`'s TOTAL line:

| when | TOTAL | modules |
|---|---|---|
| `9f36956f` (round start) | 87 | 14 |
| after C4 | 68 | 10 |
| after C5 | 51 | 6 |

Module rows left after C5 (the six text-branch-survivor modules T002's last
batch converts, unchanged by this round):

    13 apps/cli/commands/job.py
    11 apps/cli/commands/mission_cmd.py
     8 apps/cli/commands/self_cmd.py
     7 apps/cli/commands/project.py
     6 apps/cli/commands/config_cmd.py
     6 apps/cli/commands/worker.py

At C3, the `Landed: R-1031 — ` line reads: "for each of the seven converted
modules (job_stop_cmd.py, change.py, bench_cmd.py, blocker.py, decision.py,
roadmap_cmd.py, snapshot_cmds.py) one test now runs through the real CLI
dispatcher and asserts schema_version 1, ok true and an old-document key on
a converted success output; landed at this round's C3."

Every token the round's `fail(`/`emit_error(` calls introduce or reuse
(searched the whole round's diff under `apps/cli/commands/`), each with its
`git grep -c` count over `apps/` at `9f36956f`:

| token | introduced in | count at `9f36956f` | new or reused |
|---|---|---|---|
| ledger_drift | stats_ledger_cmd.py (C5, `_cmd_stats_verify_ledger`) | 0 | **new** |
| revert_failed | patch.py (C5, `_cmd_revert_patch_intent`'s literal fallback) | 1 (`apps/ui/src/api/humanizeCatalog.ts`, a UI label string) | reused (as a label; not previously a `fail()` token in `apps/cli/`) |

`_cmd_revert_patch_intent`'s new `fail()` call is DYNAMIC — its token at
runtime is `result.block_reason` (this module's own pre-check vocabulary:
`no_apply_record`, `no_snapshot`, `post_apply_drift`, `permission_denied`,
`contract_denied`, `verify_failed`) when non-empty, else `result.state`
(`revert_failed`, `partial_revert`, `blocked`), else the literal
`"revert_failed"` fallback. Counts of the remaining reachable values at
`9f36956f` over `apps/`: `no_apply_record` 1 (this module's own earlier
pre-check, same file), `no_snapshot` 0, `post_apply_drift` 0,
`permission_denied` 3, `contract_denied` 0, `verify_failed` 0,
`partial_revert` 0, `blocked` 26. None of the nine is a NEW literal written
by this round's diff except the `"revert_failed"` fallback already counted
above; the rest are reused domain vocabulary `RepositoryRevertResult.state`
already defines (`packages/orchestration/repository_snapshot.py`).

`git diff --name-only 9f36956f 8abd1553 -- packages/` prints **nothing**.

### G4 — TARGETED SELECTION, ruff, integrity

`.remedy-wt/f283-r18-scratch/selection.txt`: **304** space-separated paths
(`-n auto`). `selection_serial.txt`: **5** paths, serial. The reviewer's
`9f36956f` reading: A `11340 passed, 13 skipped`, B `204 passed`, both exit 0.

| when | A exit | A summary | B exit | B summary |
|---|---|---|---|---|
| after C3 | 0 | 11346 passed, 13 skipped | 0 | 204 passed |
| after C4 | 0 | 11348 passed, 13 skipped | 0 | 204 passed |
| after C5 | 0 | 11351 passed, 13 skipped | 0 | 204 passed |

Zero failed, zero errors at each; the passed count only rose (+6 at C3, +2
at C4, +3 at C5; B unchanged throughout, as expected — every new/changed
test in this round lives in selection A).

`python3 -m ruff check` over every `.py` path the round touched (8 converted
modules + 19 touched test files, 27 paths): **All checks passed!**

`python3 -m apps.cli.main integrity check --json`, run after C5:
`"passed": true, "fail_count": 0`, all five checks (`handler_import`,
`live_review_verdict`, `plan_consistency`, `relevant_untracked`,
`high_blockers_open`) read `"status": "pass"`; the command itself now
answers the envelope (`"schema_version": 1, "ok": true`), as it has since
round 17.

`python3 -m pytest tests/cli/test_golden_path.py -q`, run once after C5:
**42 passed**, exit 0.

### G5 — RED-PROOFS

Disposable worktree `.remedy-wt/f283-r18-redproof` at C5 (`8abd1553`), never
committed. Files: every test file C3, C4 and C5 changed —
`tests/cli/test_blocker_cmd.py`, `tests/cli/test_change_proof_cli.py`,
`tests/cli/test_cli_ux.py`, `tests/cli/test_decision_cmd.py`,
`tests/cli/test_event_list_cmd.py`, `tests/cli/test_job_stop.py`,
`tests/cli/test_json_envelope.py`, `tests/cli/test_memory_cmd.py`,
`tests/cli/test_patch_cmd.py`, `tests/cli/test_plan_cli.py`,
`tests/cli/test_real_test_execution_cli.py`, `tests/cli/test_runtime_cmd.py`,
`tests/cli/test_snapshot_cli_runtime.py`, `tests/cli/test_stats_bench.py`,
`tests/cli/test_stats_cost.py`, `tests/test_brain_detail.py`,
`tests/test_brain_smoke.py`, `tests/test_context_coverage.py`,
`tests/test_project_brain.py` — nineteen files (`tests/cli/test_json_envelope.py`
already among them), run together as the control, TWICE:

| step | exit code | result |
|---|---|---|
| control run 1 | 0 | 653 passed |
| control run 2 | 0 | 653 passed |

No UI build and no reddening on either run — this file list touches no UI
server suite. Every mutation below is judged against 653 passed.

| mutation | exit code | result | failing test(s) |
|---|---|---|---|
| (a) `roadmap next --json` prints its raw document again | 1 | 2 failed, 651 passed | `TestRawJSONDocumentSitesRatchet::test_the_pinned_counts_match_the_scan`, `TestRoadmapNext::test_json_shape` |
| (b) `run list --json` with no runs prints the prose line again | 1 | 1 failed, 652 passed | `TestRunList::test_empty_store_answers_the_envelope_with_an_empty_runs_list` |
| (c) `run list --json` writes the bare list again | 1 | 4 failed, 649 passed | `TestRawJSONDocumentSitesRatchet::test_the_pinned_counts_match_the_scan`, `TestRunList::test_empty_store_answers_the_envelope_with_an_empty_runs_list`, `TestRunList::test_limit_flag_is_honoured`, `TestRunList::test_no_flag_prints_list_runs_verbatim` |
| (d) one converted success document of `runtime_cmd.py` prints raw again | 1 | 3 failed, 650 passed | `TestRawJSONDocumentSitesRatchet::test_the_pinned_counts_match_the_scan`, `TestServe::test_serve_starts_and_leaves_the_server_running`, `TestTheSupervisorEnvironmentIsScrubbed::test_a_secret_parent_variable_never_reaches_the_supervisor` |
| (e) `brain node --json` prints its raw document again | 1 | 19 failed, 634 passed | the ratchet plus every `TestBrainNodeJsonAllTypes`/`TestBrainLifecycle` case in `tests/test_brain_smoke.py` (16), `test_brain_detail.py::TestCLIBrainNode::test_json_flag_top_level_keys`, `test_context_coverage.py::TestBrainNodeContextCoverageDetail::test_context_coverage_node_json_keys` |
| (f) one converted `memory.py` success document drops `schema_version` | 1 | 2 failed, 651 passed | `TestRawJSONDocumentSitesRatchet::test_the_pinned_counts_match_the_scan`, `TestTheReadPathsAnswerTheEnvelope::test_card_show_answers_the_envelope` |

Each mutation reddened its named target(s) and nothing else unexpected —
(a), (c), (d) and (f) additionally reddened the AST ratchet, since each
reintroduces a raw `print(json.dumps(...))` site the scanner counts; that is
the ratchet doing its job, not a spurious failure. Each mutation was
reverted with `git checkout --` and confirmed clean
(`git status --porcelain`, empty) before the next.
`git worktree remove .remedy-wt/f283-r18-redproof` afterward.
`git worktree list` (post-removal): the primary checkout alone.

## Deviations & assumptions

1. **`_cmd_revert_patch_intent` (patch.py) and `_cmd_stats_verify_ledger`
   (stats_ledger_cmd.py) needed a D10 (3) restructure the block did not name
   by hand.** Both printed a raw result document under `--json` and THEN
   exited non-zero on failure — exactly the shape DECISION F283 D10 (3)
   rules on ("a path that prints a result document and then exits non-zero
   answers ONE failure envelope instead"). Neither document carries a key
   colliding with `fail()`'s own parameters, so each failure path now calls
   `fail(<token>, <message>, json_output=True, exit_code=<the same code>,
   **document)` directly. `_cmd_stats_verify_ledger`'s token, `ledger_drift`,
   is new; `_cmd_revert_patch_intent`'s token is dynamic
   (`result.block_reason or result.state or "revert_failed"`), reusing this
   module's own existing pre-check vocabulary. See G3's token table for the
   full accounting.
2. **`real_test_execution_cmd.py`'s `snapshot create`/`snapshot show` needed
   a key rename, not a mechanical wrap.** `SnapshotProof.to_dict()`
   (`packages/orchestration/real_test_execution.py`) carries its own
   `"schema_version"` key — a domain record-schema version STRING
   (`"real-test-execution-v1"`) that predates and is unrelated to the
   envelope's integer of the same name. `emit_ok()`'s `_reject_reserved`
   raises `ValueError` on exactly this collision by design (F277 T002); the
   new `_envelope_safe()` helper renames the domain key to
   `record_schema_version` (value unchanged) before the two `emit_ok()`
   calls, so no information is dropped and the two concepts are told apart
   by name. Confirmed no other converted module in either half carries a
   top-level `"schema_version"` or `"ok"` key besides the `"ok"` sites D10
   (2) already names (the four `runtime_cmd.py` sites whose payload's own
   `to_json()` includes `"ok"`, filtered out before `emit_ok`).
3. **Twenty tests across eight files pinned the OLD exact shape and needed
   repair beyond the reviewer's `dry_a_bad.txt` list's four named entries**
   — the dry run's mechanical conversion did not restructure
   `_cmd_run_list`'s routing bug, so `TestRunList::test_empty_store_...`
   was not itself listed red by the dry run, but the block's own text
   explicitly orders the empty-runs case as an obligation
   ("one test asserts `run list --json` with no runs answers `runs`
   empty"), so it is treated as one of this round's required repairs. The
   other nineteen (`test_json_output_is_the_exported_record` and eighteen
   brain/context-coverage/project-brain key-set pins) match `dry_a_bad.txt`
   exactly.
4. **Constraints 1, 2, 3, 4, 6 and 7 held throughout.** No payload was
   edited or retyped; every commit stayed under 500 insertions (239, 15,
   111, 112, 161; this handoff exempt as a single `.agent/**` state file);
   the round's tracked path set (32 distinct paths before this commit, 33
   after) is EXACTLY constraint 3's full enumeration, with nothing outside
   it and nothing missing; `packages/` shows nothing touched; every commit
   from C3 on left both selections at zero failed and zero errors, the
   passed count only rising; nothing was merged, no PR created, no checkout
   of `main`; the one G5 worktree was removed as its own last action.

### The round's whole tracked path set (before this commit)

`git diff --name-only 9f36956f 8abd1553` — **32** distinct paths; plus
`.agent/handoff.md` from this commit makes **33** — EXACTLY constraint 3's
full enumeration (3 authored copies + 2 `.agent/**` state files + 8
converted modules + 19 distinct test files + `.agent/handoff.md`):

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f283-r18-block.md | C1 `0f81a255` |
| 2 | .agent/authored/f283-r18-ledger.md | C1 `0f81a255` |
| 3 | .agent/authored/f283-r18-plan.md | C1 `0f81a255` |
| 4 | .agent/live_review.md | C2 `ba8d29cd`, appended again by C3 `ebfb6cc8` |
| 5 | .agent/plan.md | C2 `ba8d29cd` |
| 6 | tests/cli/test_blocker_cmd.py | C3 `ebfb6cc8` |
| 7 | tests/cli/test_change_proof_cli.py | C3 `ebfb6cc8` |
| 8 | tests/cli/test_decision_cmd.py | C3 `ebfb6cc8` |
| 9 | tests/cli/test_job_stop.py | C3 `ebfb6cc8` |
| 10 | tests/cli/test_plan_cli.py | C3 `ebfb6cc8` |
| 11 | tests/cli/test_snapshot_cli_runtime.py | C3 `ebfb6cc8`, touched again by C4 |
| 12 | tests/cli/test_stats_bench.py | C3 `ebfb6cc8` |
| 13 | apps/cli/commands/do_cmd.py | C4 `f35d07d1` |
| 14 | apps/cli/commands/event.py | C4 `f35d07d1` |
| 15 | apps/cli/commands/real_test_execution_cmd.py | C4 `f35d07d1` |
| 16 | apps/cli/commands/runtime_cmd.py | C4 `f35d07d1` |
| 17 | tests/cli/test_cli_ux.py | C4 `f35d07d1` |
| 18 | tests/cli/test_event_list_cmd.py | C4 `f35d07d1` |
| 19 | tests/cli/test_json_envelope.py | C4 `f35d07d1`, touched again by C5 |
| 20 | tests/cli/test_real_test_execution_cli.py | C4 `f35d07d1` |
| 21 | tests/cli/test_runtime_cmd.py | C4 `f35d07d1` |
| 22 | apps/cli/commands/brain.py | C5 `8abd1553` |
| 23 | apps/cli/commands/memory.py | C5 `8abd1553` |
| 24 | apps/cli/commands/patch.py | C5 `8abd1553` |
| 25 | apps/cli/commands/stats_ledger_cmd.py | C5 `8abd1553` |
| 26 | tests/cli/test_memory_cmd.py | C5 `8abd1553` |
| 27 | tests/cli/test_patch_cmd.py | C5 `8abd1553` |
| 28 | tests/cli/test_stats_cost.py | C5 `8abd1553` |
| 29 | tests/test_brain_detail.py | C5 `8abd1553` |
| 30 | tests/test_brain_smoke.py | C5 `8abd1553` |
| 31 | tests/test_context_coverage.py | C5 `8abd1553` |
| 32 | tests/test_project_brain.py | C5 `8abd1553` |
| 33 | .agent/handoff.md | C6 (this commit) |

No path outside constraint 3's enumeration was touched: `.agent/decisions.md`,
`.agent/candidates.md`, `.agent/context.md`, `.agent/operator_questions.md`,
`.agent/prose_slips.md`, `README.md`, `docs/**`, `scripts/**` appear **0**
times.

## Authored-text proofs

- The three copies at C1, compared with the block's originals under
  `.remedy-wt/f283-r18-payloads/` and `.remedy-wt/f283-r18-block.md`: **three
  readings, all True** (G1).
- The one APPEND payload against its committed file: strict byte
  concatenation True for `.agent/live_review.md` (ledger.md), byte number
  equal to the block's (529803+5779=535582) and the reviewer's own stated
  composition (G2a).
- The one REWRITE payload against its committed file: `.agent/plan.md`'s
  committed sha256 equals the payload's sha256 (G2c).
- No payload was edited or retyped. The block copy and two payload copies
  were made with `shutil.copyfile`; the one append by reading the payload's
  bytes and writing base+payload back to disk; the plan.md rewrite by
  `shutil.copyfile`.
- Every change under `apps/` and `tests/` this round was WORKER-authored to
  the block's SPEC and DECISION F283 D10 — there is no reviewer-authored
  diff to compare against for those files; G3/G4/G5 above are the proof
  they meet the SPEC.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Pre-flight (STOP, git state, block self-verify) | done | no STOP; tree clean at `9f36956f`; block 198 lines / matching sha256 |
| C1 copy block + 2 payloads | done | 239 insertions |
| C2 book round 17 PASS, register R-1031, resolve R-1030 | done | 15 insertions (6+9, 11 deletions from plan rewrite); open set 25→25, added R-1031, removed R-1030 |
| C3 pin the envelope of seven round-17 modules (R-1031) | done | 111 insertions; one dispatcher test per module, each naming its test below |
| C4 runtime, do, test, event answer --json success | done | 112 insertions; ratchet 87→68; D10 (4) `run list` routing fixed |
| C5 memory, patch, stats, brain answer --json success | done | 161 insertions; ratchet 68→51; D10 (3) applied at two new sites |
| C6 the handback | done | this commit |
| G1 payload transport + authored copies | done | 2/2 payload readings equal; 3/3 authored copies byte-identical |
| G2(a) live_review.md append | done | 529803+5779=535582 |
| G2(b) open set by distinct id | done | 1 Gate line, 1 R-1031 line, 1 Done line; 25→25, added R-1031, removed R-1030 |
| G2(c) plan.md rewrite | done | sha256-equal to payload; 35 lines, under 50 |
| G3 change counted from the tree | done | per-commit diffs and insertions reported; ratchet 87→68→51; Landed line quoted; two new/reused tokens with counts; nothing under `packages/` |
| G4 targeted selection, ruff, integrity, golden path | done | A: 11346/11348/11351 passed after C3/C4/C5 (up from 11340); B: 204 passed unchanged throughout; 0 failed/errors at each; ruff exit 0 over 28 paths; integrity all 5 pass, fail_count 0; golden path 42 passed |
| G5 red-proofs (a)(b)(c)(d)(e)(f) | done | all six go RED, each reddening its named target(s) plus the ratchet where the mutation reintroduces a raw print site; unmutated control run twice (653/653 passed, no UI build in this file set) |
| R-1031 module test — job_stop_cmd.py | done | `tests/cli/test_job_stop.py::TestJSONThroughTheDispatcher::test_stop_answers_the_envelope` |
| R-1031 module test — change.py | done | `tests/cli/test_change_proof_cli.py::test_change_proof_answers_the_envelope_through_the_dispatcher` |
| R-1031 module test — bench_cmd.py | done | `tests/cli/test_stats_bench.py::TestRegistration::test_answers_the_envelope_through_the_argv_dispatcher` |
| R-1031 module test — blocker.py | done | `tests/cli/test_blocker_cmd.py::TestBlockerListAnswersJSONThroughTheDispatcher::test_list_answers_the_envelope` |
| R-1031 module test — decision.py | done | `tests/cli/test_decision_cmd.py::TestDecisionListAnswersJSONThroughTheDispatcher::test_list_answers_the_envelope` |
| R-1031 module test — roadmap_cmd.py | done | `tests/cli/test_plan_cli.py::TestRoadmapNext::test_json_shape` (extended) |
| R-1031 module test — snapshot_cmds.py | done | `tests/cli/test_snapshot_cli_runtime.py::TestSnapshotListAppliesCLI::test_answers_the_envelope_for_a_real_job` |
| C4 module test — runtime_cmd.py | done | `tests/cli/test_runtime_cmd.py::TestServe::test_serve_starts_and_leaves_the_server_running` (extended) |
| C4 module test — do_cmd.py | done | `tests/cli/test_cli_ux.py::TestRunList::test_no_flag_prints_list_runs_verbatim` + `test_empty_store_answers_the_envelope_with_an_empty_runs_list` (the D10 (4) empty-runs obligation) |
| C4 module test — real_test_execution_cmd.py | done | `tests/cli/test_real_test_execution_cli.py::test_snapshot_create_show` (extended) |
| C4 module test — event.py | done | `tests/cli/test_event_list_cmd.py::test_the_success_document_answers_the_envelope` |
| C5 module test — memory.py | done | `tests/cli/test_memory_cmd.py::TestTheReadPathsAnswerTheEnvelope` (3 cases) |
| C5 module test — patch.py | done | `tests/cli/test_patch_cmd.py::TestTheHappyPath::test_json_output_is_the_exported_record` (extended) |
| C5 module test — stats_ledger_cmd.py | done | `tests/cli/test_stats_cost.py::TestCostJsonShape::test_the_document_carries_its_figures_basis_and_provenance` (extended); D10 (3) drift path in `TestVerifyLedger::test_drift_is_visible_in_json_too` |
| C5 module test — brain.py | done | `tests/test_project_brain.py::TestCLIBrain::test_json_flag_output_has_correct_top_level_keys` (extended) |
| G6 tree, push, PR list | pending at write time | reported in the worker's session reply with real exit codes |
| Constraint 1 no payload edited/retyped | done | `shutil.copyfile`, byte concatenation only |
| Constraint 2 every commit under 500 insertions | done | 239, 15, 111, 112, 161; this handoff exempt as single `.agent/**` state file |
| Constraint 3 no unnamed file touched | done | 32 paths before this commit (33 after), EXACTLY the full enumeration |
| Constraint 4 both selections at zero failed after every commit | done | A 11346/11348/11351, B 204/204/204 passed, 0 failed/errors at each |
| Constraint 5 STOP if a gate goes red outside constraint 3's path set | done (n/a) | no gate went red outside the named paths; no STOP was needed |
| Constraint 6 nothing is merged | done | no `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch deletion |
| Constraint 7 G5 worktree under .remedy-wt/, removed, listed | done | `.remedy-wt/f283-r18-redproof`, removed, `git worktree list` reported after; no other worktree disturbed |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 18 — C1 through C6, all six gates re-derived.
3. Then T002's last success batch, as `.agent/plan.md` lists it: `job`,
   `mission`, `self`, `project`, `config`, `worker`, leaving the ratchet at
   the text-branch survivors.

Open findings count: **25** (R-1031 landed, awaiting review). Operator-questions
count: **0**.
