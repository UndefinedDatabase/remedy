# Handoff — F283 Machine contracts, part two: refusal sweep, JSON gap, exit-code taxonomy · Round 11 · `stats` refusals, `job stop`, R-1026 booked

## Session

SESSION 3 of feature F283 · round 11 · rounds so far 11

This round booked round 10's PASS (verdict PASS on all six gates, R-1026
resolved). Then, one commit each: every refusal in `stats_ledger_cmd.py`,
`bench_cmd.py` and `failure_stats_cmd.py` moved onto `fail()`, the exiting
helpers (`_validate_by`, `_validate_period_bound`, `_one_project_ledger`,
`_require_evidence_dir`, `_validate_multiplier`, `_one_project_history`,
`_validate_since`) gaining a REQUIRED `json_output` every caller now passes;
`job_stop_cmd.py`'s four `raise SystemExit` refusals (`_unknown_job`, the
`validate_job_id` refusal, `job_not_stoppable`, `stop_not_requested`) moved the
same way, leaving `job_stop_cmd.py` with no `raise SystemExit` at all; and the
two refusals round 10's own probe found unpinned — `_cmd_test_status`'s
`job_not_found` and `_cmd_discover_commands`'s `job_store_error` — gained tests,
plus the mis-attributed DECISION F283 D5 citation in
`tests/test_command_discovery.py`'s docstring was corrected.
Context self-assessment: roughly 98% of the working budget remained at the
point this handoff was written.

## Range

Review of `590abe57`..`HEAD`.

## Block self-verification (R-0954)

| reading | measured | given | equal |
|---|---|---|---|
| line count | 221 | 221 | True |
| sha256 | `4e9166abec91d27b0b5f02edb0077338177dd9d3e454f2e4b330387bcd3c50fe` | `4e9166abec91d27b0b5f02edb0077338177dd9d3e454f2e4b330387bcd3c50fe` | True |

Neither reading differed, so the round went ahead.

## Pre-flight

- `ls .agent/STOP`: `No such file or directory`. No STOP on disk.
- `git status --porcelain`: empty.
- `git branch --show-current`: `feature/f283-machine-contracts-part-two`.
- `git log --oneline -1`: `590abe57`, matching the delegation message.

## Commits

### 4f4128f8 F283 R11 C1: copy round 11 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r11-block.md | +221/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f283-r11-ledger.md | +4/-0 | byte-for-byte copy of ledger.md |
| .agent/authored/f283-r11-plan.md | +36/-0 | byte-for-byte copy of plan.md |

Measured insertions (`git show --numstat`): **261** (221+4+36).

### d077d310 F283 R11 C2: book round 10's PASS, resolve R-1026
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | append ledger.md by strict byte concatenation: round-10 `Gate:` entry, `Done:` line resolving R-1026 |
| .agent/plan.md | +11/-14 | rewrite to plan.md payload, byte-identical; git's line diff shows only the lines that changed |

Measured insertions: **15** (4+11); 14 deletions from the plan.md rewrite.

### 6672ff15 F283 R11 C3: stats refusals answer through fail(), helpers take the flag
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/stats_ledger_cmd.py | +46/-46 | `fail` imported (`sys` import dropped, now unused); `_validate_by`, `_validate_period_bound`, `_one_project_ledger`, `_require_evidence_dir` gain a required `json_output`, every caller passes its own; `_load_ledger_reports`'s and `_cmd_stats_report`'s branched `sqlite3.Error` catches become one `fail("ledger_unreadable", ...)` each |
| apps/cli/commands/bench_cmd.py | +13/-13 | `fail` imported (`sys` dropped); `_validate_multiplier`, `_one_project_history` gain a required `json_output`, `_cmd_stats_bench` passes its own |
| apps/cli/commands/failure_stats_cmd.py | +10/-12 | `fail` imported (`sys` dropped); `_validate_since` gains a required `json_output`; the branched `FailureStatsError` catch becomes `fail("evidence_unreadable", str(exc), json_output=json_output)` |
| tests/cli/test_stats_cost.py | +19/-0 | `test_an_unreadable_ledger_answers_ledger_unreadable_under_json`: one envelope (`ledger_unreadable`), empty stderr |
| tests/cli/test_stats_report.py | +18/-0 | `test_a_bad_until_answers_invalid_argument_under_json`: one envelope (`invalid_argument`), empty stderr |
| tests/cli/test_stats_bench.py | +18/-0 | `test_an_unusable_multiplier_answers_invalid_argument_under_json`: one envelope (`invalid_argument`), empty stderr |
| tests/cli/test_failure_cmd.py | +23/-0 | `test_an_unreadable_evidence_root_answers_evidence_unreadable_under_json`: one envelope (`evidence_unreadable`), empty stderr |
| tests/cli/test_job_refusal_envelope.py | +56/-0 | new `_raise_systemexit_lines` AST helper and `TestStatsRefusalsAreAllMigrated`: no mechanical print-then-exit pair in the three modules, `stats_ledger_cmd.py` keeps exactly one `raise SystemExit` (`EXIT_DRIFT`), `bench_cmd.py`/`failure_stats_cmd.py` keep none |

Measured insertions: **203** (46+13+10+19+18+18+23+56); 71 deletions.

### 5f598cf3 F283 R11 C4: job stop refusals answer through fail()
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/job_stop_cmd.py | +14/-25 | `fail` imported at module level (`sys` dropped); `_unknown_job`'s branched pair, `validate_job_id`'s `StopControlError` branch, `job_not_stoppable`'s branched pair and `stop_not_requested`'s branched pair all become one `fail()` call each, keeping every payload key (`job_id`, `job_status`, `detail`) the old JSON object carried |
| tests/cli/test_job_refusal_envelope.py | +8/-2 | `TestStatsRefusalsAreAllMigrated` extended to `job_stop_cmd.py`: added to `_MODULES`, new `test_job_stop_has_no_raise_systemexit_left` |
| tests/cli/test_job_stop.py | +25/-2 | `test_an_unknown_job_exits_3_in_json_mode_too` gains a `job_id` assertion; new `test_a_malformed_job_id_answers_invalid_job_id_under_json`; `test_a_completed_job_says_so_in_json_too` gains `schema_version`/`job_id` assertions; `test_an_unwritable_control_area_says_so_in_json_too` gains `schema_version`/`job_id`/`detail` assertions |

Measured insertions: **47** (14+8+25); 29 deletions.

### 861e10be F283 R11 C5: pin the two test-group refusals round 10 left untested
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_job_refusal_envelope.py | +60/-0 | new `TestRound10sUntestedRefusalsNowPinned`: `_cmd_test_status`'s `job_not_found` (a fresh UUID the resolver accepts, a store that holds nothing) and `_cmd_discover_commands`'s `job_store_error` (`require_job_plan` monkeypatched to raise) each answer one envelope with an empty stderr |
| tests/test_command_discovery.py | +3/-2 | `TestDiscoverNoTargetRepoAnswersInTheEnvelope`'s docstring corrected: the branched-site rule is the migration rule's own (F277 D7-D9), not DECISION F283 D5, which is `do --json`'s one-envelope rule |

Measured insertions: **63** (60+3); 2 deletions. No `Done:` line written — the reviewer writes it.

### C6 — THE HANDBACK (this commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the 500-line cap under DECISION F104 D1 |

Self-reference exception (handback template, R-0149 pattern): a handback cannot
table the commit that writes it.

## External actions

- `git worktree add .remedy-wt/f283-r11-redproof HEAD` (at `861e10be`) for G5 —
  used for the unmutated control and all four mutation red-proofs, then
  `git worktree remove .remedy-wt/f283-r11-redproof` — a plain remove sufficed
  because every mutation was reverted with `git checkout --` back to the
  original committed text (verified clean with `git status --porcelain` after
  each revert) before removal.
- `git push origin feature/f283-machine-contracts-part-two` after C6 — real
  outcome reported in the session reply, since it ships this very file.
- `gh pr list --state open ...` after the push — real outcome reported in the
  session reply.
- **NOTHING IS MERGED.** No `gh pr merge`, no `gh pr create`, no checkout of
  `main`, no branch deletion.
- No worktree other than the one disposable G5 worktree was added or removed.
  The three `remedy/job-*` worktrees were left alone throughout.

## Verification

### G1 — PAYLOADS transport, then three authored copies

| file | lines measured/given | bytes measured/given | sha256 equal |
|---|---|---|---|
| ledger.md | 4/4 | 4563/4563 | True |
| plan.md | 36/36 | 1555/1555 | True |

**All readings equal: True.**

Three `.agent/authored/f283-r11-*` copies (the block copy plus two payloads),
each read back from the committed tree with `git show 4f4128f8:<path>` and
compared byte-for-byte with its source:

| copy | bytes | identical to source |
|---|---|---|
| f283-r11-block.md | 14202 | True |
| f283-r11-ledger.md | 4563 | True |
| f283-r11-plan.md | 1555 | True |

**Copies compared: 3. All True.**

### G2 — THE BOOKING

**(a) Append arithmetic**, by strict byte concatenation:

| file | pre (`590abe57`) | payload | post | pre+payload==post |
|---|---|---|---|---|
| .agent/live_review.md | 496649 | 4563 | 501212 | True |

Matches the reviewer's stated `496649 + ledger.md = 501212` exactly.

**(b) Line-anchored on the committed ledger**: `^Gate: F283 R10 — ` = **1**;
`^Done: R-1026 — ` = **1**. Open set by distinct id, via `open_finding_ids` from
`scripts/rotate_live_review.py` (imported and called directly):

| rev | OPEN by distinct id |
|---|---|
| `590abe57` | **23** |
| C2 (`d077d310`) | **22** |

Added: `[]`. Removed: `['R-1026']`. Matches the reviewer's stated 23 → 22, ADDED
empty, REMOVED `R-1026`, exactly.

**(c) `.agent/plan.md` at C2 equals plan.md byte-for-byte**: sha256-equal to the
payload (`6d159a6c91398989243abf4115b95d88ed9b90d6a77460b76a8895ebeff9576c` both).

Line count: **36**, under the AGENTS.md 50-line rule.

### G3 — THE CHANGE, COUNTED FROM THE TREE

`git diff --name-only <parent> <commit>` and `git show --numstat` insertions:

| commit | paths changed | insertions |
|---|---|---|
| C3 `d077d310`→`6672ff15` | apps/cli/commands/bench_cmd.py, apps/cli/commands/failure_stats_cmd.py, apps/cli/commands/stats_ledger_cmd.py, tests/cli/test_failure_cmd.py, tests/cli/test_job_refusal_envelope.py, tests/cli/test_stats_bench.py, tests/cli/test_stats_cost.py, tests/cli/test_stats_report.py | 203 |
| C4 `6672ff15`→`5f598cf3` | apps/cli/commands/job_stop_cmd.py, tests/cli/test_job_refusal_envelope.py, tests/cli/test_job_stop.py | 47 |
| C5 `5f598cf3`→`861e10be` | tests/cli/test_job_refusal_envelope.py, tests/test_command_discovery.py | 63 |

**`raise SystemExit` count per module, before (`590abe57`) and after C4:**

| module | before | after |
|---|---|---|
| stats_ledger_cmd.py | 9 | 1 (the surviving `verify-ledger` `EXIT_DRIFT`, a RESULT not a refusal) |
| bench_cmd.py | 3 | 0 |
| failure_stats_cmd.py | 2 | 0 |
| job_stop_cmd.py | 4 | 0 |

Matches the reviewer's stated readings (9/3/2/4 before, 1/0/0/0 after) exactly.

`git diff --name-only 590abe57 861e10be -- packages/` prints **nothing** (real
exit code implicit 0, empty stdout) — confirmed `packages/` untouched across the
whole round.

### Token list — every `fail()` token C3 and C4 use, its line, new or reused

| commit | module | line | token | new/reused | search behind a `new` one |
|---|---|---|---|---|---|
| C3 | stats_ledger_cmd.py | 75 | invalid_argument | reused (`decision.py`, `do_cmd.py`, `job.py`, `mission_cmd.py`, `grouped.py` already use it) | — |
| C3 | stats_ledger_cmd.py | 104 | invalid_argument | reused (same as above) | — |
| C3 | stats_ledger_cmd.py | 146 | option_not_applicable | reused (`decision.py` already uses it) | — |
| C3 | stats_ledger_cmd.py | 155 | no_project | reused (`decision.py`, `job.py`, `mission_cmd.py`, `project.py` already use it) | — |
| C3 | stats_ledger_cmd.py | 167 | missing_argument | reused (`decision.py`, `job.py`, `worker.py`, `grouped.py` already use it) | — |
| C3 | stats_ledger_cmd.py | 171 | path_not_found | new | `git grep -l '"path_not_found"' 590abe57 -- apps/cli/`: 0 hits anywhere |
| C3 | stats_ledger_cmd.py | 337 | ledger_unreadable | new | `git grep -l '"ledger_unreadable"' 590abe57 -- apps/cli/`: 0 hits anywhere |
| C3 | stats_ledger_cmd.py | 556 | ledger_unreadable | reused (same commit, L337) | — |
| C3 | bench_cmd.py | 99 | invalid_argument | reused (see above) | — |
| C3 | bench_cmd.py | 102 | invalid_argument | reused (same commit, L99) | — |
| C3 | bench_cmd.py | 119 | no_project | reused (see above) | — |
| C3 | failure_stats_cmd.py | 27 | invalid_argument | reused (see above) | — |
| C3 | failure_stats_cmd.py | 62 | evidence_unreadable | new | `git grep -l '"evidence_unreadable"' 590abe57 -- apps/cli/`: 0 hits anywhere |
| C4 | job_stop_cmd.py | 66 | job_not_found | reused (this module's own pre-existing `fail()` call at old L100-106 already used it; 15 other modules do too) | — |
| C4 | job_stop_cmd.py | 86 | invalid_job_id | reused (`apps/cli/job_id_arg.py` already uses this spelling for the identical malformed-id condition) | — |
| C4 | job_stop_cmd.py | 145 | job_not_stoppable | reused (this file's own OLD JSON literal, at `590abe57`, already spelled this condition this way — the migration keeps the existing spelling, DECISION F277 D8 part (a)) | — |
| C4 | job_stop_cmd.py | 153 | stop_not_requested | reused (same reasoning as `job_not_stoppable`, this file's own old JSON literal) | — |

New tokens this round: `path_not_found`, `ledger_unreadable`, `evidence_unreadable`
— three, each confirmed absent from any `fail("<token>"`/`"<token>"` search over
`apps/cli/` before its introducing commit.

### G4 — TARGETED SELECTION, ruff, integrity

`.remedy-wt/f283-r11-scratch/selection.txt`: **106** space-separated paths
(round 10's selection plus every test file a search for this round's targets
found).

| when | exit code | summary |
|---|---|---|
| after C3 | 0 | 4464 passed, 1 skipped |
| after C4 | 0 | 4466 passed, 1 skipped |
| after C5 | 0 | 4468 passed, 1 skipped |

Zero failed, zero errors at each; the reviewer read `4457 passed, 1 skipped` at
`590abe57` — the passed count only rose, at every step (+7 at C3, +2 at C4, +2
at C5 — one new test per new commit-level envelope test, plus C3's three new
`TestStatsRefusalsAreAllMigrated` ratchet tests and C4's one extension).
`python3 -m ruff check` over every `.py` path the round touched
(`apps/cli/commands/bench_cmd.py`, `apps/cli/commands/failure_stats_cmd.py`,
`apps/cli/commands/job_stop_cmd.py`, `apps/cli/commands/stats_ledger_cmd.py`,
`tests/cli/test_failure_cmd.py`, `tests/cli/test_job_refusal_envelope.py`,
`tests/cli/test_job_stop.py`, `tests/cli/test_stats_bench.py`,
`tests/cli/test_stats_cost.py`, `tests/cli/test_stats_report.py`,
`tests/test_command_discovery.py`): **All checks passed!**
`python3 -m apps.cli.main integrity check --json`: `"passed": true, "fail_count": 0`,
all five checks (`handler_import`, `live_review_verdict`, `plan_consistency`,
`relevant_untracked`, `high_blockers_open`) read `"status": "pass"`.

### G5 — RED-PROOFS

Disposable worktree `.remedy-wt/f283-r11-redproof` at `861e10be`, never
committed. Ran the seven test files C3 to C5 touched (`test_stats_cost.py`,
`test_stats_report.py`, `test_stats_bench.py`, `test_failure_cmd.py`,
`test_job_stop.py`, `test_job_refusal_envelope.py`, `test_command_discovery.py`).

| step | exit code | result |
|---|---|---|
| unmutated control | 0 | 301 passed |
| (a) `_load_ledger_reports`'s `ledger_unreadable` `fail()` call forced to `json_output=False` | 1 | `1 failed, 41 passed` (`tests/cli/test_stats_cost.py` alone) — C3's `test_an_unreadable_ledger_answers_ledger_unreadable_under_json` (the target, alone) |
| (b) `bench_cmd.py::_validate_multiplier`'s first branch put back as its old `print` + `raise SystemExit(EXIT_USAGE) from None` (named: `_validate_multiplier`) | 1 | `2 failed, 93 passed` (`tests/cli/test_stats_bench.py` + `tests/cli/test_job_refusal_envelope.py`) — C3's `test_an_unusable_multiplier_answers_invalid_argument_under_json` (the target) and the C3 ratchet `TestStatsRefusalsAreAllMigrated::test_bench_and_failure_stats_have_no_raise_systemexit_left` |
| (c) `job_stop_cmd.py`'s `invalid_job_id` refusal passes `"bad_job_id"` instead | 1 | `1 failed, 26 passed` (`tests/cli/test_job_stop.py` alone) — C4's `test_a_malformed_job_id_answers_invalid_job_id_under_json` (the target, alone) |
| (d) `test_cmds.py::_cmd_test_status`'s `job_not_found` refusal passes `"no_such_job"` instead | 1 | `1 failed, 68 passed` (`tests/cli/test_job_refusal_envelope.py` alone) — C5's `test_test_status_job_not_found_answers_in_the_envelope` (the target, alone) |

Each mutation was reverted with `git checkout --` and confirmed clean with
`git status --porcelain` before the next. `git worktree remove
.remedy-wt/f283-r11-redproof` afterward. `git worktree list` (post-removal): the
primary checkout at `861e10be` plus the three `remedy/job-*` worktrees —
`.remedy-wt/job-468c8e62a2cc4fac`, `.remedy-wt/job-86f628f5e4fb4e0c`,
`.remedy-wt/job-c1dba9c3d7874968` — untouched throughout.

## Deviations & assumptions

1. **The bundle ran C1 through C5 — five commits, exactly as ordered — before
   this handback commit C6.** Nothing was added, dropped or reordered.
2. **Mutation (b)'s named helper is `bench_cmd.py::_validate_multiplier`, not
   `_one_project_history`.** The block names the helper to restore only as
   "one helper's `fail()`", leaving the choice to the worker; `_one_project_history`
   was tried first and reverted unused, because it has no dedicated `--json`
   envelope test of its own (only a text-mode one), so mutating it would have
   reddened the C3 ratchet alone and left the block's "that helper's envelope
   test must fail" clause unmet. `_validate_multiplier` has both.
3. **`_load_ledger_reports`'s and `_cmd_stats_report`'s `ledger_unreadable`
   message keeps the old prose's exact wording** (`"cannot read the token
   ledger: {exc}"`) rather than the bare `str(exc)` the tokens list's aside
   ("their old JSON put the exception text in `error`; it now sits in
   `message`") might suggest in isolation. This keeps the migration rule's own,
   more specific instruction — "the text branch stays byte-identical" for a
   BRANCHED site — satisfied exactly: `fail()` writes one message to both
   branches, so the text branch's `Error: cannot read the token ledger: {exc}`
   line is unchanged byte-for-byte, and the JSON branch's `message` key carries
   that same sentence (still containing the raw exception text) where the old
   JSON's `error` key held only `str(exc)`.
4. **No expected insertion figure is given for C2's rewrite or for C3/C4/C5,
   per the block's own convention**: only measured figures are reported above,
   none forced to match a prediction.
5. **Constraints 1, 3, 4, 6 and 7 held throughout.** No payload was edited or
   retyped; the round's tracked path set is exactly the 16 paths (before this
   commit) constraint 3 enumerates plus `.agent/handoff.md` from this commit
   makes 17 (verified by set-equality below); `packages/` was never touched;
   every commit from C3 on left the targeted G4 selection at zero failed;
   nothing was merged, no PR created, no checkout of `main`; the one G5
   worktree was removed as G5's last action and the three `remedy/job-*`
   worktrees were left alone.

### The round's whole tracked path set (before this commit)

`git diff --name-only 590abe57 861e10be` — **16** distinct paths
(`tests/cli/test_job_refusal_envelope.py` touched by C3, C4 and C5 — counted
once); plus `.agent/handoff.md` from this commit makes **17** — set-equal to
constraint 3's enumeration (3 authored copies + live_review.md + plan.md +
handoff.md + stats_ledger_cmd.py + bench_cmd.py + failure_stats_cmd.py +
job_stop_cmd.py + test_stats_cost.py + test_stats_report.py + test_stats_bench.py
+ test_failure_cmd.py + test_job_stop.py + test_job_refusal_envelope.py +
test_command_discovery.py):

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f283-r11-block.md | C1 `4f4128f8` |
| 2 | .agent/authored/f283-r11-ledger.md | C1 `4f4128f8` |
| 3 | .agent/authored/f283-r11-plan.md | C1 `4f4128f8` |
| 4 | .agent/live_review.md | C2 `d077d310` |
| 5 | .agent/plan.md | C2 `d077d310` |
| 6 | apps/cli/commands/bench_cmd.py | C3 `6672ff15` |
| 7 | apps/cli/commands/failure_stats_cmd.py | C3 `6672ff15` |
| 8 | apps/cli/commands/stats_ledger_cmd.py | C3 `6672ff15` |
| 9 | tests/cli/test_failure_cmd.py | C3 `6672ff15` |
| 10 | tests/cli/test_job_refusal_envelope.py | C3 `6672ff15`, touched again by C4 `5f598cf3` and C5 `861e10be` |
| 11 | tests/cli/test_stats_bench.py | C3 `6672ff15` |
| 12 | tests/cli/test_stats_cost.py | C3 `6672ff15` |
| 13 | tests/cli/test_stats_report.py | C3 `6672ff15` |
| 14 | apps/cli/commands/job_stop_cmd.py | C4 `5f598cf3` |
| 15 | tests/cli/test_job_stop.py | C4 `5f598cf3` |
| 16 | tests/test_command_discovery.py | C5 `861e10be` |
| 17 | .agent/handoff.md | C6 (this commit) |

No path outside the enumeration was touched: `.agent/candidates.md`,
`.agent/context.md`, `.agent/decisions.md`, `.agent/operator_questions.md`,
`.agent/prose_slips.md`, `README.md`, `docs/roadmap/**`, `scripts/**` and
`apps/cli/json_envelope.py` appear **0** times. `packages/` appears **0** times
(confirmed above under G3).

## Authored-text proofs

- The three copies at C1, compared with the reviewer's originals under
  `.remedy-wt/f283-r11-payloads/` and `.remedy-wt/f283-r11-block.md`: **three
  readings, all True** (G1).
- The one REWRITE payload against its committed file: `.agent/plan.md`'s
  committed sha256 equals the payload's sha256 (G2c).
- The one APPEND payload against its committed file: strict byte concatenation
  True for `.agent/live_review.md` (ledger.md), byte numbers equal to the
  reviewer's (G2a).
- No payload was edited or retyped. Both `.agent/authored/` copies of the
  payloads and the one product-file rewrite were made with `shutil.copyfile`;
  the one append by reading the payload's bytes and writing base+payload back
  to disk.
- Every change under `apps/` and `tests/` this round was WORKER-authored to the
  block's SPEC — there is no reviewer-authored diff to compare against for
  those files; the block's SPEC prose is the standard they were written to,
  and G3/G4/G5 above are the proof they meet it.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Pre-flight (STOP, git state, block self-verify) | done | no STOP; tree clean at `590abe57`; block 221 lines / matching sha256 |
| C1 copy block + 2 payloads | done | 261 insertions |
| C2 book round 10 PASS, resolve R-1026 | done | 15 insertions (4+11, 14 deletions from plan rewrite); open set 23→22, removed R-1026 |
| C3 stats refusals answer through fail() | done | 203 insertions; 3 new tokens (`path_not_found`, `ledger_unreadable`, `evidence_unreadable`), 10 reused |
| C4 job stop refusals answer through fail() | done | 47 insertions; 0 new tokens (all 4 reused), `job_stop_cmd.py` left with 0 `raise SystemExit` |
| C5 pin the two test-group refusals round 10 left untested | done | 63 insertions; two new tests plus the docstring correction |
| C6 the handback | done | this commit |
| G1 payload transport + authored copies | done | 2/2 payload readings equal; 3/3 authored copies byte-identical |
| G2(a) live_review.md append | done | 496649+4563=501212 |
| G2(b) R-1026 resolution pairing + open set by distinct id | done | 1 Gate line, 1 Done line; 23→22, removed R-1026, added none |
| G2(c) plan.md rewrite | done | sha256-equal to payload; 36 lines, under 50 |
| G3 change counted from the tree | done | per-commit diffs and insertions reported; raise-SystemExit counts 9/3/2/4→1/0/0/0; 0 paths under `packages/` |
| G4 targeted selection, ruff, integrity | done | 4464/4466/4468 passed, 0 failed/errors at each (up from 4457); ruff exit 0; integrity all 5 pass, fail_count 0 |
| G5 red-proofs (a)(b)(c)(d) | done | all four go RED, each reddening exactly its named target test (plus, for (b), the C3 ratchet the block itself names); unmutated control 301 passed |
| G6 tree, push, PR list | pending at write time | reported in the worker's session reply with real exit codes |
| Constraint 1 no payload edited/retyped | done | `shutil.copyfile`, byte concatenation only |
| Constraint 2 every commit under 500 insertions | done | 261, 15, 203, 47, 63; this handoff exempt as single `.agent/**` state file |
| Constraint 3 no unnamed file touched | done | 16 paths before this commit (17 after), set-equal to the enumeration |
| Constraint 4 G4 selection at zero failed after every commit | done | 4464/4466/4468 passed, 0 failed/errors at each |
| Constraint 5 STOP if a gate goes red outside constraint 3's path set | done (n/a) | no gate went red outside the named paths; no STOP was needed |
| Constraint 6 nothing is merged | done | no `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch deletion |
| Constraint 7 G5 worktree under .remedy-wt/, removed, listed | done | `.remedy-wt/f283-r11-redproof`, removed as G5's last action, `git worktree list` reported after; the three `remedy/job-*` worktrees untouched |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 11 — C1 through C6, with all six gates re-derived.
3. Then the rest of the tail as `.agent/plan.md` lists it: `patch`, `config`,
   `real_test_execution`, `snapshot`, `self`, `worker_facade`, the cost-preview
   confirmation, and the unprefixed refusals of `--json` handlers;
   `runtime_cmd.py` as its own round; then T001's catalog half and T002's
   success-envelope half.

Open findings count: **22**. Operator-questions count: **2**.
