# Handoff — F283 Machine contracts, part two: refusal sweep, JSON gap, exit-code taxonomy · Round 12 · rest of the refusal tail, D7

## Session

SESSION 3 of feature F283 · round 12 · rounds so far 12

This round booked round 11's PASS and recorded DECISION F283 D7 (a refusal in a
`--json` handler that `fail()` cannot write byte for byte answers the envelope
under `--json` and keeps its text). Then, one commit each: the `patch`,
`snapshot`, `real_test_execution` and `self` refusals moved onto `fail()`
(`_cmd_revert_patch_intent`'s three branched sites, `snapshot_cmds.py`'s three,
`real_test_execution_cmd.py`'s three, `self_cmd.py`'s `--top` refusal); then
under D7, `config_cmd.py` (`list` by the plain rule, `get`/`init`/`set` under
D7), `project.py::_cmd_project_current`'s branch, `patch.py::_cmd_approve_hunks`'s
refusal, `worker_facade_cmd.py`'s `_err` deletion and `cost_preview_confirm.py`'s
collapse to one `fail()`; then the three `stats` refusals round 11 left
unpinned gained tests. A self-review after C5 (this round's own G3 pair-count
check, constraint 4) found `config_cmd.py` reading `mechanical 3` against the
block's stated `mechanical 1` at C5, traced to C4 nesting `sys.exit(1)` inside
the `else` of `config_init`/`config_set`; one small follow-up commit restored
the original exit placement. See Deviations.
Context self-assessment: roughly 98% of the working budget remained at the
point this handoff was written.

## Range

Review of `e964343b`..`HEAD`.

## Block self-verification (R-0954)

| reading | measured | given | equal |
|---|---|---|---|
| line count | 233 | 233 | True |
| sha256 | `e36debd6d346736da01089b6232d30d5da1d552f2e435b81e89ea82fbd58fa86` | `e36debd6d346736da01089b6232d30d5da1d552f2e435b81e89ea82fbd58fa86` | True |

Neither reading differed, so the round went ahead.

## Pre-flight

- `ls .agent/STOP`: `No such file or directory`. No STOP on disk.
- `git status --porcelain`: empty.
- `git branch --show-current`: `feature/f283-machine-contracts-part-two`.
- `git log --oneline -1`: `e964343b`, matching the delegation message.

## Commits

### a87de5c4 F283 R12 C1: copy round 12 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r12-block.md | +233/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f283-r12-decisions.md | +36/-0 | byte-for-byte copy of decisions.md |
| .agent/authored/f283-r12-ledger.md | +2/-0 | byte-for-byte copy of ledger.md |
| .agent/authored/f283-r12-plan.md | +33/-0 | byte-for-byte copy of plan.md |

Measured insertions (`git show --numstat`): **304** (233+36+2+33).

### 0949ef94 F283 R12 C2: book round 11's PASS, record D7
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | append ledger.md by strict byte concatenation: round-11 `Gate:` entry |
| .agent/decisions.md | +36/-0 | append decisions.md: DECISION F283 D7 |
| .agent/plan.md | +11/-14 | rewrite to plan.md payload, byte-identical; git's line diff shows only the lines that changed |

Measured insertions: **49** (2+36+11); 14 deletions from the plan.md rewrite.

### e91adf87 F283 R12 C3: patch, snapshot, test-record and self refusals answer through fail()
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/patch.py | +21/-27 | `_cmd_revert_patch_intent`'s three BRANCHED sites (`ambiguous_intent_id`, `no_apply_record`, `no_target_repo`) become one `fail()` call each, keeping `intent_id`/`apply_ids`/`job_id` |
| apps/cli/commands/real_test_execution_cmd.py | +5/-7 | `fail` imported (`sys` dropped, now unused); `_cmd_test_result`'s `test_run_not_found`, `_cmd_test_list`'s `invalid_list_option`, `_cmd_snapshot_show`'s `snapshot_proof_not_found` move onto `fail()` by the plain rule |
| apps/cli/commands/self_cmd.py | +3/-3 | `fail` imported (`sys` dropped); `_cmd_self_propose`'s `--top` refusal answers `invalid_argument` |
| apps/cli/commands/snapshot_cmds.py | +19/-16 | `fail` imported (`sys` dropped); `_cmd_snapshot_inspect`'s two branched sites (`job_not_found`, `snapshot_not_found`) and `_cmd_snapshot_list_applies`'s one (`job_not_found`) become one `fail()` call each |
| tests/cli/test_job_refusal_envelope.py | +84/-1 | `TestPatchRefusalsAreAllMigrated` docstring notes round 12 (its two counts unchanged — neither branched site was ever a mechanical pair by the AST rule); new `TestSnapshotCmdsRefusalsAreAllMigrated`, `TestRealTestExecutionRefusalsAreAllMigrated`, `TestSelfCmdRefusalsAreAllMigrated` ratchets, each asserting no pair (mechanical or branched) survives and `fail` is imported |
| tests/cli/test_real_test_execution_cli.py | +35/-1 | repaired `test_test_list_unknown_sort_field_exits_nonzero` (the old `invalid_list_option` site always printed to stderr regardless of `--json`; now it answers the envelope on stdout when the flag holds); new envelope tests for `test result` (`test_run_not_found`) and `snapshot show` (`snapshot_proof_not_found`) |
| tests/cli/test_self_dogfood_cli.py | +13/-0 | new `test_propose_bad_top_answers_the_envelope`: `invalid_argument`, exit 1, empty stderr |
| tests/cli/test_snapshot_cli_runtime.py | +46/-0 | new `test_an_unknown_snapshot_answers_the_envelope` (`snapshot_not_found`, kept `snapshot_id`) and `test_no_apply_record_answers_the_envelope` (patch revert, `no_apply_record`, kept `intent_id`) — patch revert's envelope test lives here because `TestPatchRevertCLI` already holds this command's tests |

Measured insertions: **226** (21+5+3+19+84+35+13+46); 55 deletions.

### 43435546 F283 R12 C4: config, project current, approve-hunks and mission run answer the envelope (D7)
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/config_cmd.py | +12/-10 | `fail` imported; `config list`'s `ListOptionError` by the plain rule (`invalid_list_option`); `config get`/`init`/`set` under D7 — each gains an `if use_json: fail(...) else: <original two lines>` guard, the original text branch byte-identical (`unknown_config_key`, `config_file_exists`, `invalid_config_value`) |
| apps/cli/commands/patch.py | +2/-6 | `_cmd_approve_hunks`'s `HunkApprovalRefusal` branch collapses its json half to `fail(result.code, result.message, json_output=True, hunk_ids=...)`; the old `code` key is now the envelope's `error` and is not repeated; text branch untouched |
| apps/cli/commands/project.py | +10/-2 | `_cmd_project_current`'s `(ProjectNotFoundError, InvalidProjectSelectorError)` branch gains an `if json_output:` guard answering `project_not_found` or `invalid_project_selector` (by `isinstance`) at exit 3; else clause is the original two lines, untouched |
| apps/cli/commands/worker_facade_cmd.py | +4/-8 | `_err` deleted (`sys`, `NoReturn` imports dropped, now unused); its one caller calls `fail("missing_argument", "run_id required", json_output=<flag>)` — the deliberate text change D7 names (the old `{"error": ...}` STDERR object in both modes becomes `Error: run_id required` in text mode) |
| apps/cli/cost_preview_confirm.py | +1/-4 | the non-tty refusal's `if json_output: fail(...) ; print(...); sys.exit(...)` fallthrough collapses to one unconditional `fail()` call; no change to either branch |
| tests/cli/test_config_cmd.py | +58/-3 | repaired `test_config_set_rejects_unknown` (old `{"error": <sentence>}` shape → envelope, token `invalid_config_value`) and `test_config_list_unknown_sort_field_exits_nonzero` (prose moved from stderr to the stdout envelope); new text-mode-pin and `--json`-envelope tests for `config get` and a `--json`-envelope test for `config init`'s refusal |
| tests/cli/test_job_refusal_envelope.py | +7/-1 | `TestProjectRefusalsAreAllMigrated` docstring notes round 12: the one flagged site now sits behind an `if json_output:` guard, same count |
| tests/cli/test_patch_cmd.py | +6/-2 | two `payload["code"]` assertions repaired to `payload["error"]`, `schema_version`/`ok` added |
| tests/cli/test_project_current.py | +61/-0 | new `TestProjectCurrentNotFoundAndInvalidSelector`: `--json` envelope tests for `project_not_found` and `invalid_project_selector` (exit 3 each) and a text-mode byte-pin test |
| tests/cli/test_worker_facade_cmd.py | +33/-0 | new envelope test (`missing_argument`) and text-mode pin test (`Error: run_id required`) for `mission run`'s empty-id refusal |

Measured insertions: **194** (12+2+10+4+1+58+7+6+61+33); 36 deletions.

### f14c67d6 F283 R12 C5: pin the three stats refusals round 11 left unpinned
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_failure_cmd.py | +16/-0 | new `test_an_invalid_since_under_json_answers_the_envelope`: `_validate_since`'s refusal under `--json`, `invalid_argument` at exit 2, empty stderr |
| tests/cli/test_stats_cost.py | +34/-0 | new `test_a_missing_evidence_directory_under_json_answers_path_not_found` and `test_all_projects_under_json_answers_option_not_applicable`, both via `backfill-ledger`, both exit 2, empty stderr |

Measured insertions: **50** (16+34); 0 deletions.

### 06ace93e F283 R12 fix: config_init/config_set keep sys.exit outside the guard
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/config_cmd.py | +2/-2 | moves `sys.exit(1)` back OUTSIDE the `if use_json: fail(...) else: print(...)` guard in `_cmd_config_init` and `_cmd_config_set`, restoring the pre-round exit placement so their print-then-exit pairs read non-mechanical again (only `config_get`'s stays mechanical, matching G3's stated C5 baseline) |

Measured insertions: **2**; 2 deletions. See Deviations — this is an UNORDERED sixth code commit, found and fixed before push.

### C6 — THE HANDBACK (this commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the 500-line cap under DECISION F104 D1 |

Self-reference exception (handback template, R-0149 pattern): a handback cannot
table the commit that writes it.

## External actions

- `git worktree add --detach .remedy-wt/f283-r12-c3check e91adf87` — a
  MISSTEP (see Deviations): built without `apps/ui`'s dist, so it read 64
  failures unrelated to this round's code. Removed with `git worktree remove
  --force .remedy-wt/f283-r12-c3check` immediately after discovering the
  cause, never used for a reported reading.
- `git checkout e91adf87` then `git checkout feature/f283-machine-contracts-part-two`
  in the PRIMARY checkout, to re-derive the "after C3" G4 reading with the
  already-built `dist` in place (the block's own "in the primary checkout"
  instruction) since G4 was not run there before C4 landed. Tree was clean
  before and after both checkouts; nothing uncommitted was ever at risk.
- `git worktree add --detach .remedy-wt/f283-r12-g5 06ace93e` for G5 — used for
  the unmutated control and all five mutation red-proofs, each reverted with
  the file tool and confirmed clean with `git status --porcelain` before the
  next — then `git worktree remove --force .remedy-wt/f283-r12-g5`.
- `git push origin feature/f283-machine-contracts-part-two` after C6 — real
  outcome reported in the session reply, since it ships this very file.
- `gh pr list --state open ...` after the push — real outcome reported in the
  session reply.
- **NOTHING IS MERGED.** No `gh pr merge`, no `gh pr create`, no checkout of
  `main`, no branch deletion.
- No worktree other than the two disposable ones above (both removed) was
  added. The three `remedy/job-*` worktrees were left alone throughout.

## Verification

### G1 — PAYLOADS transport, then four authored copies

| file | lines measured/given | bytes measured/given | sha256 equal |
|---|---|---|---|
| decisions.md | 36/36 | 2806/2806 | True |
| ledger.md | 2/2 | 3013/3013 | True |
| plan.md | 33/33 | 1338/1338 | True |

**All readings equal: True.**

Four `.agent/authored/f283-r12-*` copies (the block copy plus three payloads),
each read back from the committed tree with `git show a87de5c4:<path>` and
compared byte-for-byte (sha256) with its source:

| copy | sha256 equal to source |
|---|---|
| f283-r12-block.md | True |
| f283-r12-decisions.md | True |
| f283-r12-ledger.md | True |
| f283-r12-plan.md | True |

**Copies compared: 4. All True.**

### G2 — THE BOOKING

**(a) Append arithmetic**, by strict byte concatenation:

| file | pre (`e964343b`) | payload | post | pre+payload==post |
|---|---|---|---|---|
| .agent/live_review.md | 501212 | 3013 | 504225 | True |
| .agent/decisions.md | 1803831 | 2806 | 1806637 | True |

Matches the reviewer's stated compositions (501212+ledger.md=504225,
1803831+decisions.md=1806637) exactly.

**(b) Line-anchored on the committed ledger**: `^Gate: F283 R11 — ` = **1**.
Open set by distinct id, via `open_finding_ids` from
`scripts/rotate_live_review.py` (imported and called directly):

| rev | OPEN by distinct id |
|---|---|
| `e964343b` | **22** |
| C2 (`0949ef94`) | **22** |

Added: `[]`. Removed: `[]`. Matches the reviewer's stated 22 → 22, ADDED empty,
REMOVED empty, exactly.

**(c) `.agent/plan.md` at C2 equals plan.md byte-for-byte**: sha256-equal to the
payload (`47e3b3c01045a93600566b7036f11e3093658cebdc1c0c0efe774b5d5b6abd96` both).

Line count: **33**, under the AGENTS.md 50-line rule.

### G3 — THE CHANGE, COUNTED FROM THE TREE

`git diff --name-only <parent> <commit>` and `git show --numstat` insertions:

| commit | paths changed | insertions |
|---|---|---|
| C3 `0949ef94`→`e91adf87` | apps/cli/commands/patch.py, apps/cli/commands/real_test_execution_cmd.py, apps/cli/commands/self_cmd.py, apps/cli/commands/snapshot_cmds.py, tests/cli/test_job_refusal_envelope.py, tests/cli/test_real_test_execution_cli.py, tests/cli/test_self_dogfood_cli.py, tests/cli/test_snapshot_cli_runtime.py | 226 |
| C4 `e91adf87`→`43435546` | apps/cli/commands/config_cmd.py, apps/cli/commands/patch.py, apps/cli/commands/project.py, apps/cli/commands/worker_facade_cmd.py, apps/cli/cost_preview_confirm.py, tests/cli/test_config_cmd.py, tests/cli/test_job_refusal_envelope.py, tests/cli/test_patch_cmd.py, tests/cli/test_project_current.py, tests/cli/test_worker_facade_cmd.py | 194 |
| C5 `43435546`→`f14c67d6` | tests/cli/test_failure_cmd.py, tests/cli/test_stats_cost.py | 50 |
| fix `f14c67d6`→`06ace93e` | apps/cli/commands/config_cmd.py | 2 |

`python3 .remedy-wt/f283-r6-scratch/pairs.py patch.py config_cmd.py
real_test_execution_cmd.py self_cmd.py worker_facade_cmd.py
../cost_preview_confirm.py project.py snapshot_cmds.py`, run AFTER the fix
commit:

| module | exits | mechanical | reviewer's e964343b baseline | matches C5 expectation |
|---|---|---|---|---|
| patch.py | 4 | 2 | mechanical 2 | True — unchanged |
| config_cmd.py | 3 | 1 | mechanical 2 | True — 1 (the `get` text branch D7 keeps) |
| real_test_execution_cmd.py | 0 | 0 | mechanical 3 | True — 0 |
| self_cmd.py | 0 | 0 | mechanical 1 | True — 0 |
| worker_facade_cmd.py | 0 | 0 | mechanical 1 | True — 0 |
| cost_preview_confirm.py | 0 | 0 | mechanical 1 | True — 0 |
| project.py | 2 | 2 | mechanical 2 | True — unchanged |
| snapshot_cmds.py | 0 | 0 | exits 3 mechanical 0 | True — exits 0 |

Every reading matches the block's stated C5 expectation exactly (this took a
follow-up commit — see Deviations; the FIRST reading after C4/C5, before the
fix, read `config_cmd.py mechanical 3`, a genuine mismatch this round caught
and repaired itself).

`git diff --name-only e964343b 06ace93e -- packages/` prints **nothing** (real
exit code implicit 0, empty stdout) — confirmed `packages/` untouched across
the whole round.

### Token list — every `fail()` token C3 and C4 use, its line, new or reused

| commit | module | line | token | new/reused | search behind a `new` one |
|---|---|---|---|---|---|
| C3 | patch.py | 221 | ambiguous_intent_id | new (as a `fail()` token — the raw string already existed as the OLD hand-rolled JSON literal's value at this exact site) | `git grep -c 'fail("ambiguous_intent_id"' 0949ef94 -- apps/cli/`: 0 hits |
| C3 | patch.py | 230 | no_apply_record | new (same caveat: pre-existing as a JSON literal, not as a `fail()` call) | `git grep -c 'fail("no_apply_record"' 0949ef94 -- apps/cli/`: 0 hits |
| C3 | patch.py | 241 | no_target_repo | reused (`job_context_cmd.py`, `test_cmds.py` already call `fail("no_target_repo"`) | — |
| C3 | snapshot_cmds.py | 28 | job_not_found | reused (16 other modules already call `fail("job_not_found"`) | — |
| C3 | snapshot_cmds.py | 38 | snapshot_not_found | new | `git grep -c 'fail("snapshot_not_found"' 0949ef94 -- apps/cli/`: 0 hits |
| C3 | snapshot_cmds.py | 99 | job_not_found | reused (same as L28) | — |
| C3 | real_test_execution_cmd.py | 24 | test_run_not_found | new | `git grep -c 'fail("test_run_not_found"' 0949ef94 -- apps/cli/`: 0 hits |
| C3 | real_test_execution_cmd.py | 49 | invalid_list_option | reused (10 other modules already call `fail("invalid_list_option"`) | — |
| C3 | real_test_execution_cmd.py | 91 | snapshot_proof_not_found | new | `git grep -c 'fail("snapshot_proof_not_found"' 0949ef94 -- apps/cli/`: 0 hits |
| C3 | self_cmd.py | 66 | invalid_argument | reused (8 other modules already call `fail("invalid_argument"`) | — |
| C4 | config_cmd.py | 51 | invalid_list_option | reused (same as above) | — |
| C4 | config_cmd.py | 93 | unknown_config_key | new | `git grep -c 'fail("unknown_config_key"' e91adf87 -- apps/cli/`: 0 hits |
| C4 | config_cmd.py | 161 (call opens; token on next line) | config_file_exists | new | `git grep -c 'fail("config_file_exists"' e91adf87 -- apps/cli/`: 0 hits |
| C4 | config_cmd.py | 186 | invalid_config_value | new | `git grep -c 'fail("invalid_config_value"' e91adf87 -- apps/cli/`: 0 hits |
| C4 | patch.py | 359 | `result.code` (dynamic; the decision core's own refusal code, e.g. `REFUSAL_MISSING_REASON`) | relocated, not a new literal — was already the old `code` key's value, now the envelope's `error` | — |
| C4 | project.py | 350 | project_not_found | **reused, not new** — DEVIATION from the block's own "(new)" marking; `project.py` already calls `fail("project_not_found"` 6 times (lines 94, 119, 147, 186, 225, 279) for a different condition (project not found by ID). The CALL SITE is new; the token string was already in this file's `fail()` vocabulary | `git grep -n 'fail("project_not_found"' e91adf87 -- apps/cli/commands/project.py`: 6 hits before this commit |
| C4 | project.py | 350 | invalid_project_selector | new | `git grep -c 'fail("invalid_project_selector"' e91adf87 -- apps/cli/`: 0 hits |
| C4 | worker_facade_cmd.py | 36 | missing_argument | reused (`decision.py`, `job.py`, `stats_ledger_cmd.py`, `worker.py`, `grouped.py` already call it) | — |
| C4 | cost_preview_confirm.py | 78 | confirmation_required | reused (this exact file already called it, inside the `if json_output:` half the collapse removes) | — |

New tokens this round (as `fail()` calls, by the search above):
`ambiguous_intent_id`, `no_apply_record`, `snapshot_not_found`,
`test_run_not_found`, `snapshot_proof_not_found`, `unknown_config_key`,
`config_file_exists`, `invalid_config_value`, `invalid_project_selector` —
nine, each confirmed absent as a `fail("<token>"` call before its introducing
commit. `project_not_found` is corrected to REUSED above; see Deviations.

### G4 — TARGETED SELECTION, ruff, integrity

`.remedy-wt/f283-r12-scratch/selection.txt`: **110** space-separated paths
(round 11's selection plus every test file a search for this round's targets
found; pre-built by the reviewer, verified against this reading independently).

| when | where | exit code | summary |
|---|---|---|---|
| after C3 | primary checkout, `git checkout e91adf87` (detached), then back | 0 | 4559 passed, 1 skipped |
| after C4 | primary checkout, branch tip | 0 | 4567 passed, 1 skipped |
| after C5 + fix | primary checkout, branch tip | 0 | 4570 passed, 1 skipped |

Zero failed, zero errors at each; the reviewer read `4548 passed, 1 skipped` at
`e964343b` — the passed count only rose, at every step (+11 at C3, +8 at C4,
+3 at C5). See Deviations for the FIRST "after C3" attempt, in a fresh
side-worktree lacking a built `apps/ui` dist, which read `64 failed` — an
environment artifact, not a code regression, discarded and re-run in the
primary checkout per the block's own "in the primary checkout" instruction.
`python3 -m ruff check` over every `.py` path the round touched
(`apps/cli/commands/config_cmd.py`, `apps/cli/commands/patch.py`,
`apps/cli/commands/project.py`, `apps/cli/commands/real_test_execution_cmd.py`,
`apps/cli/commands/self_cmd.py`, `apps/cli/commands/snapshot_cmds.py`,
`apps/cli/commands/worker_facade_cmd.py`, `apps/cli/cost_preview_confirm.py`,
`tests/cli/test_config_cmd.py`, `tests/cli/test_failure_cmd.py`,
`tests/cli/test_job_refusal_envelope.py`, `tests/cli/test_patch_cmd.py`,
`tests/cli/test_project_current.py`, `tests/cli/test_real_test_execution_cli.py`,
`tests/cli/test_self_dogfood_cli.py`, `tests/cli/test_snapshot_cli_runtime.py`,
`tests/cli/test_stats_cost.py`, `tests/cli/test_worker_facade_cmd.py`): **All
checks passed!**
`python3 -m apps.cli.main integrity check --json`: `"passed": true,
"fail_count": 0`, all five checks (`handler_import`, `live_review_verdict`,
`plan_consistency`, `relevant_untracked`, `high_blockers_open`) read
`"status": "pass"`.

### G5 — RED-PROOFS

Disposable worktree `.remedy-wt/f283-r12-g5` at `06ace93e`, never committed.
Ran the ten test files C3 to C5 touched unmutated first
(`test_snapshot_cli_runtime.py`, `test_real_test_execution_cli.py`,
`test_self_dogfood_cli.py`, `test_job_refusal_envelope.py`,
`test_config_cmd.py`, `test_project_current.py`, `test_patch_cmd.py`,
`test_worker_facade_cmd.py`, `test_failure_cmd.py`, `test_stats_cost.py`):

| step | exit code | result |
|---|---|---|
| unmutated control | 0 | 286 passed |
| (a) `snapshot_cmds.py`'s `snapshot_not_found` `fail()` call forced to `json_output=False` | 1 | `1 failed, 17 passed` (`test_snapshot_cli_runtime.py` alone) — `test_an_unknown_snapshot_answers_the_envelope` (the target, alone) |
| (b) `real_test_execution_cmd.py`'s `test_run_not_found` renamed to `test_run_not_found_RENAMED` | 1 | `1 failed, 11 passed` (`test_real_test_execution_cli.py` alone) — `test_test_result_not_found_answers_the_envelope` (the target, alone) |
| (c) `project.py::_cmd_project_current`'s `--json` guard replaced with `if False:` | 1 | `2 failed, 21 passed` (`test_project_current.py` alone) — both new `TestProjectCurrentNotFoundAndInvalidSelector` tests (the target pair, alone) |
| (d) `config_cmd.py`'s `invalid_config_value` renamed to `invalid_config_value_RENAMED` | 1 | `1 failed, 18 passed` (`test_config_cmd.py` alone) — `test_config_set_rejects_unknown` (the target, alone) |
| (e) `failure_stats_cmd.py::_validate_since`'s `fail()` call forced to `json_output=False` | 1 | `1 failed, 28 passed` (`test_failure_cmd.py` alone) — `test_an_invalid_since_under_json_answers_the_envelope` (the target, alone) |

Each mutation was reverted with the file tool and confirmed clean with `git
status --porcelain` before the next. `git worktree remove --force
.remedy-wt/f283-r12-g5` afterward. `git worktree list` (post-removal): the
primary checkout at `06ace93e` plus the three `remedy/job-*` worktrees —
`.remedy-wt/job-468c8e62a2cc4fac`, `.remedy-wt/job-86f628f5e4fb4e0c`,
`.remedy-wt/job-c1dba9c3d7874968` — untouched throughout.

## Deviations & assumptions

1. **A sixth CODE commit, `06ace93e`, was added after C5 and before this
   handback.** The block ordered exactly C1 through C6; this is an UNORDERED
   insertion. Cause: this round's own G3 pair-count check (constraint 4's
   spirit, run proactively) found `config_cmd.py` reading `mechanical 3` after
   C5 against the block's stated `mechanical 1` at C5 — C4's edit to
   `_cmd_config_init`/`_cmd_config_set` had nested `sys.exit(1)` INSIDE the
   `else` branch of the new `if use_json: fail(...) else: ...` guard, which
   made the print-then-exit pair register as mechanical again by the AST rule
   `_refusal_sites`/`pairs.py` both use. The fix moves `sys.exit(1)` back
   OUTSIDE the guard (a sibling of the `if`/`else`, unreachable when `fail()`
   already exited), matching the ORIGINAL pre-round placement and the block's
   stated C5 baseline exactly. Never amended: AGENTS.md's git safety protocol
   forbids rewriting an existing commit and forbids `git reset --hard` without
   explicit instruction, so the correction is its own commit rather than a
   `--amend` of C4. Behavior is byte-for-byte unchanged (confirmed:
   `tests/cli/test_config_cmd.py` passes in full before and after; the G4
   selection's passed count only rose after this commit too).
2. **The G4 "after C3" reading was taken twice.** The FIRST attempt used a
   fresh disposable worktree (`.remedy-wt/f283-r12-c3check`, detached at
   `e91adf87`), which read `64 failed` — all in `tests/ui_server/` and
   React-bundle checks, a cold/missing `apps/ui` dist in the fresh worktree
   (a known environment artifact, not a code regression: the primary checkout
   already has `dist` built). Discarded, worktree removed, and re-run per the
   block's own G4 instruction ("in the primary checkout"): `git checkout
   e91adf87` in the PRIMARY tree (clean before and after, nothing at risk),
   read `4559 passed, 1 skipped` at exit 0, then `git checkout
   feature/f283-machine-contracts-part-two` to return to the branch tip. This
   is the reading reported in G4 above.
3. **`project_not_found` is corrected to REUSED, not new**, contradicting the
   block's tokens section ("`project_not_found` / `invalid_project_selector`
   (new)"). The measured search (`git grep -n 'fail("project_not_found"'
   e91adf87 -- apps/cli/commands/project.py`) found 6 pre-existing calls in
   this exact file, for a different refusal (project not found BY ID, in
   `_cmd_show_project` and others). The CALL SITE `_cmd_project_current` adds
   is new; the TOKEN STRING was already in this file's `fail()` vocabulary
   before this round. Generate, don't transcribe (R-1014): the search is
   reported as measured, not as the block characterized it.
4. **`ambiguous_intent_id` and `no_apply_record` are new as `fail()` tokens,
   not as raw strings.** Both already existed at their exact call sites as the
   OLD hand-rolled JSON literal's `"error"` value before this round (e.g.
   `json.dumps({"error": "ambiguous_intent_id", ...})`); converting the
   branched site to `fail()` is their first appearance as a `fail("<token>"`
   call, which is the sense the tokens list's "(new)" marking is read to mean
   throughout this table.
5. **Constraints 1, 3, 4, 6 and 7 held throughout** (constraint 4's own
   proactive check is what caught the config_cmd.py mismatch item 1 above
   describes). No payload was edited or retyped; the round's tracked path set
   is 25 distinct paths before this commit (26 after, with `.agent/handoff.md`)
   — verified below to be a SUBSET of constraint 3's enumeration (it omits
   `tests/cli/test_cost_preview_confirm.py`, which needed no repair since the
   collapse in `cost_preview_confirm.py` changed no observable behavior);
   `packages/` was never touched; every commit from C3 on left the targeted G4
   selection at zero failed; nothing was merged, no PR created, no checkout of
   `main` beyond the two round-trips item 2 describes; the two G5/verification
   worktrees were removed as their own last action and the three
   `remedy/job-*` worktrees were left alone.

### The round's whole tracked path set (before this commit)

`git diff --name-only e964343b 06ace93e` — **25** distinct paths (`patch.py`
touched by C3 and C4; `config_cmd.py` touched by C4 and the fix commit;
`test_job_refusal_envelope.py` touched by C3 and C4 — each counted once);
plus `.agent/handoff.md` from this commit makes **26** — a SUBSET of
constraint 3's 27-path enumeration (every allowed path used except
`tests/cli/test_cost_preview_confirm.py`):

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f283-r12-block.md | C1 `a87de5c4` |
| 2 | .agent/authored/f283-r12-decisions.md | C1 `a87de5c4` |
| 3 | .agent/authored/f283-r12-ledger.md | C1 `a87de5c4` |
| 4 | .agent/authored/f283-r12-plan.md | C1 `a87de5c4` |
| 5 | .agent/live_review.md | C2 `0949ef94` |
| 6 | .agent/decisions.md | C2 `0949ef94` |
| 7 | .agent/plan.md | C2 `0949ef94` |
| 8 | apps/cli/commands/patch.py | C3 `e91adf87`, touched again by C4 `43435546` |
| 9 | apps/cli/commands/real_test_execution_cmd.py | C3 `e91adf87` |
| 10 | apps/cli/commands/self_cmd.py | C3 `e91adf87` |
| 11 | apps/cli/commands/snapshot_cmds.py | C3 `e91adf87` |
| 12 | tests/cli/test_job_refusal_envelope.py | C3 `e91adf87`, touched again by C4 `43435546` |
| 13 | tests/cli/test_real_test_execution_cli.py | C3 `e91adf87` |
| 14 | tests/cli/test_self_dogfood_cli.py | C3 `e91adf87` |
| 15 | tests/cli/test_snapshot_cli_runtime.py | C3 `e91adf87` |
| 16 | apps/cli/commands/config_cmd.py | C4 `43435546`, touched again by fix `06ace93e` |
| 17 | apps/cli/commands/project.py | C4 `43435546` |
| 18 | apps/cli/commands/worker_facade_cmd.py | C4 `43435546` |
| 19 | apps/cli/cost_preview_confirm.py | C4 `43435546` |
| 20 | tests/cli/test_config_cmd.py | C4 `43435546` |
| 21 | tests/cli/test_patch_cmd.py | C4 `43435546` |
| 22 | tests/cli/test_project_current.py | C4 `43435546` |
| 23 | tests/cli/test_worker_facade_cmd.py | C4 `43435546` |
| 24 | tests/cli/test_failure_cmd.py | C5 `f14c67d6` |
| 25 | tests/cli/test_stats_cost.py | C5 `f14c67d6` |
| 26 | .agent/handoff.md | C6 (this commit) |

No path outside constraint 3's enumeration was touched: `.agent/candidates.md`,
`.agent/context.md`, `.agent/operator_questions.md`, `.agent/prose_slips.md`,
`README.md`, `docs/roadmap/**`, `scripts/**` and `apps/cli/json_envelope.py`
appear **0** times. `packages/` appears **0** times (confirmed above under G3).

## Authored-text proofs

- The four copies at C1, compared with the reviewer's originals under
  `.remedy-wt/f283-r12-payloads/` and `.remedy-wt/f283-r12-block.md`: **four
  readings, all True** (G1).
- The one REWRITE payload against its committed file: `.agent/plan.md`'s
  committed sha256 equals the payload's sha256 (G2c).
- The two APPEND payloads against their committed files: strict byte
  concatenation True for `.agent/live_review.md` (ledger.md) and
  `.agent/decisions.md` (decisions.md), byte numbers equal to the reviewer's
  (G2a).
- No payload was edited or retyped. All four `.agent/authored/` copies and the
  one product-file rewrite were made with `shutil.copyfile`; the two appends
  by reading each payload's bytes and writing base+payload back to disk.
- Every change under `apps/` and `tests/` this round was WORKER-authored to
  the block's SPEC — there is no reviewer-authored diff to compare against for
  those files; the block's SPEC prose is the standard they were written to,
  and G3/G4/G5 above are the proof they meet it.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Pre-flight (STOP, git state, block self-verify) | done | no STOP; tree clean at `e964343b`; block 233 lines / matching sha256 |
| C1 copy block + 3 payloads | done | 304 insertions |
| C2 book round 11 PASS, record D7 | done | 49 insertions (2+36+11, 14 deletions from plan rewrite); open set 22→22, added/removed empty |
| C3 patch, snapshot, test-record, self refusals answer through fail() | done | 226 insertions; 5 new tokens, 5 reused (see token list deviations) |
| C4 config, project current, approve-hunks, mission run answer the envelope (D7) | done | 194 insertions; block claimed 5 new tokens, measured 4 (`project_not_found` corrected to reused — see Deviations), 4 reused, 1 relocated (dynamic) |
| C5 pin the three stats refusals round 11 left unpinned | done | 50 insertions; three new envelope tests, no source change |
| fix config_init/config_set exit placement | deviated | unordered sixth code commit; self-caught by this round's own G3 check; see Deviations item 1 |
| C6 the handback | done | this commit |
| G1 payload transport + authored copies | done | 3/3 payload readings equal; 4/4 authored copies byte-identical |
| G2(a) live_review.md + decisions.md append | done | 501212+3013=504225; 1803831+2806=1806637 |
| G2(b) open set by distinct id | done | 1 Gate line; 22→22, added none, removed none |
| G2(c) plan.md rewrite | done | sha256-equal to payload; 33 lines, under 50 |
| G3 change counted from the tree | done | per-commit diffs and insertions reported; pairs.py mechanical counts match the block's C5 baseline exactly after the fix commit; 0 paths under `packages/` |
| G4 targeted selection, ruff, integrity | done | 4559/4567/4570 passed, 0 failed/errors at each (up from 4548); one discarded side-worktree reading (environment artifact, declared); ruff exit 0; integrity all 5 pass, fail_count 0 |
| G5 red-proofs (a)(b)(c)(d)(e) | done | all five go RED, each reddening exactly its named target test(s); unmutated control 286 passed |
| G6 tree, push, PR list | pending at write time | reported in the worker's session reply with real exit codes |
| Constraint 1 no payload edited/retyped | done | `shutil.copyfile`, byte concatenation only |
| Constraint 2 every commit under 500 insertions | done | 304, 49, 226, 194, 50, 2; this handoff exempt as single `.agent/**` state file |
| Constraint 3 no unnamed file touched | done | 25 paths before this commit (26 after), a SUBSET of the 27-path enumeration |
| Constraint 4 G4 selection at zero failed after every commit | done | 4559/4567/4570 passed, 0 failed/errors at each; this check is what caught item 1's mismatch |
| Constraint 5 STOP if a gate goes red outside constraint 3's path set | done (n/a) | no gate went red outside the named paths; no STOP was needed |
| Constraint 6 nothing is merged | done | no `gh pr merge`, no `gh pr create`, no checkout of `main` left uncommitted, no branch deletion |
| Constraint 7 G5 worktree under .remedy-wt/, removed, listed | done | `.remedy-wt/f283-r12-g5` (plus the discarded `.remedy-wt/f283-r12-c3check`), both removed, `git worktree list` reported after; the three `remedy/job-*` worktrees untouched |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 12 — C1 through C6 plus the unordered fix commit, with
   all six gates re-derived.
3. Then `runtime_cmd.py` as `.agent/plan.md` lists it, its own round.

Open findings count: **22**. Operator-questions count: **2**.
