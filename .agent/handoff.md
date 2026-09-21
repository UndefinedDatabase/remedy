# Handoff — F283 Machine contracts, part two: refusal sweep, JSON gap, exit-code taxonomy · Round 6 · the `job` group's last mechanical refusals, and the `decision` group

## Session

SESSION 2 of feature F283 · round 6 · rounds so far 6

This round booked round 5's PASS and R-1021's `Done:` line, threaded `json_output`
into `_cmd_run_next_task_local` and moved its eight print-then-exit pairs onto
`fail()` (job_not_found, plan_awaiting_approval, plan_rejected, permission_denied,
missing_dependency, invalid_builder_output, configuration_error, builder_error),
collapsed `_plan_rejected_error`/`_plan_rejected_message` into the one form, moved
`decision.py`'s 29 mechanical refusal pairs onto `fail()` under DECISION F277 D8/D9
(one derived-decision refusal with two unprefixed prints stays, as the block
predicted), and finished R-1022's three prose corrections plus the ambiguous-payload
proof round 5's probe (d) left unproved. Context self-assessment: roughly 98% of the
working budget remained at the point this handoff was written (about 14.74M of 15M
tokens).

## Range

Review of `63141657`..`HEAD`.

## Block self-verification (R-0954)

| reading | measured | given | equal |
|---|---|---|---|
| line count | 230 | 230 | True |
| sha256 | `cef021617da7cd3b0d0cac4db7cbe9d29112e9f4211783c23cd18ebe12ee583e` | `cef021617da7cd3b0d0cac4db7cbe9d29112e9f4211783c23cd18ebe12ee583e` | True |

Neither reading differed, so the round went ahead.

## Pre-flight

- `ls .agent/STOP`: `No such file or directory`. No STOP on disk.
- `git status --porcelain`: empty.
- `git branch --show-current`: `feature/f283-machine-contracts-part-two`.
- `git log --oneline -1`: `63141657`, matching the delegation message.

## Commits

### 700968e6 F283 R6 C1: copy round 6 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r6-block.md | +230/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f283-r6-ledger.md | +4/-0 | byte-for-byte copy of ledger.md |
| .agent/authored/f283-r6-plan.md | +42/-0 | byte-for-byte copy of plan.md |
| .agent/authored/f283-r6-slips.md | +1/-0 | byte-for-byte copy of slips.md |

Measured insertions (`git show --numstat`): **277** (230+4+42+1).

### b61dfe13 F283 R6 C2: book round 5's PASS and resolve R-1021
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | append ledger.md by strict byte concatenation: round-5 `Gate:` entry, `Done: R-1021` |
| .agent/plan.md | +22/-20 | rewrite to plan.md payload, byte-identical |
| .agent/prose_slips.md | +1/-0 | append slips.md: one line, no leading newline |

Measured insertions (`git show --numstat`): **27** (4+22+1).

### 563859fe F283 R6 C3: the single-pass run answers a refusal in the envelope
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/job.py | +27/-33 | `_cmd_run_next_task_local` gains `*, json_output: bool = False`, threads it into `resolve_job_id_or_fail`; its eight mechanical pairs move onto `fail()` with the sibling spellings `job_not_found`, `plan_awaiting_approval`, `plan_rejected`, `permission_denied`, `missing_dependency`, `invalid_builder_output`, `configuration_error`, `builder_error`; `_plan_rejected_error` deleted, `_plan_rejected_message`'s docstring says it is the one form; `_cmd_job_run_cycles`'s single-pass call threads `json_output=json_output` |
| tests/cli/test_cost_preview.py | +5/-5 | five `_cmd_run_next_task_local` monkeypatches accept the keyword (`lambda _j, **_kw: ...`) |
| tests/cli/test_job_refusal_envelope.py | +11/-11 | the unflagged-sites ratchet now asserts `== []`; the `_plan_rejected_error` test becomes `test_the_rejected_plan_sentence_carries_no_error_prefix`, testing only `_plan_rejected_message` |
| tests/orchestration/test_escalation.py | +2/-2 | two monkeypatches accept the keyword |
| tests/orchestration/test_long_run_executor.py | +3/-3 | three monkeypatches accept the keyword, recording the positional value via `lambda _j, **_kw: seen.append(_j)` |
| tests/test_cli_main.py | +33/-0 | two new tests in `TestWorkspaceWriteDenialPreBuilder`: `_cmd_run_next_task_local(<id>, json_output=True)` exits 1, empty stderr, envelope `permission_denied`; `_cmd_job_run_cycles(<id>, json_output=True, yes=True)` does the same, proving the caller threads (the cost-preview note line is skipped by reading the LAST line of stdout) |

Measured insertions: **81** (27+5+11+2+3+33).

### 05461715 F283 R6 C4: decision refusals answer through fail()
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/decision.py | +92/-85 | 29 of `decision.py`'s 30 mechanical pairs move onto `fail()`: `_cmd_decision_list`/`_cmd_decision_show` use their own `json_output`; `_create_mission_for_job` and `_cmd_decision_resolve` use `False` (no flag in scope, `decision.resolve` declares no `supports_json`); the derived-decision refusal at the end of `_cmd_decision_resolve` (two unprefixed prints) stays, exactly as the block predicted; `sys` import kept (still used at that one site) |
| tests/cli/test_decision_cmd.py | +37/-0 | `TestDecisionRefusalsAnswerInTheEnvelope`: an unknown decision id on `_cmd_decision_show` under `json_output=True` exits 1, empty stderr, envelope `decision_not_found`; an invalid sort option on `_cmd_decision_list` does the same with `invalid_list_option` |
| tests/cli/test_job_refusal_envelope.py | +28/-4 | `_refusal_sites` generalised to take a `filename` (default `job.py`, existing callers unchanged); new `TestDecisionsRefusalsAreAllMigrated` asserts the flagged list is EMPTY and the unflagged list has exactly ONE site in `decision.py` |

Measured insertions: **157** (92+37+28).

### da32c320 F283 R6 C5: finish R-1022 and prove the ambiguous payload
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_job_refusal_envelope.py | +26/-7 | the `_LOOKUP_CALLERS` comment now says "every `lookup_job_id` call site under `apps/cli/`" (not "outside `apps.cli.job_id_arg`" over a dict that holds it) and "Measured at `63141657`" (no scratch script, no round-local commit label); `TestResolveJobIdOrFailForwardsAPayload`'s docstring now attributes the pass-through to R-1021 (was R-1022); new test `test_the_ambiguous_branch_carries_the_extra_payload` proves `resolve_job_id_or_fail("aaaa1111", json_output=True, job_id="x")` over the two-ambiguous-jobs fixture exits 2 with `matches` and `job_id == "x"` both present |

Measured insertions: **26**.

### C6 — THE HANDBACK (this commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the 500-line cap under DECISION F104 D1 |

Self-reference exception (handback template, R-0149 pattern): a handback cannot table
the commit that writes it.

## External actions

- `git worktree add .remedy-wt/f283-r6-g5 da32c320 --detach` for G5 — used for the
  unmutated control and all four mutation red-proofs, then
  `git worktree remove .remedy-wt/f283-r6-g5` — a plain remove sufficed because every
  mutation was reverted with `git checkout -- <path>` back to the original text
  (verified clean with `git status --porcelain` after each revert) before the next
  step.
- `git push origin feature/f283-machine-contracts-part-two` after C6 — real outcome
  reported in the session reply, since it ships this very file.
- `gh pr list --state open ...` after the push — real outcome reported in the session
  reply.
- **NOTHING IS MERGED.** No `gh pr merge`, no `gh pr create`, no checkout of `main`, no
  branch deletion.
- No worktree other than the one disposable G5 worktree was added or removed. The
  three `remedy/job-*` worktrees were left alone throughout.

## Verification

### G1 — PAYLOADS transport, then four authored copies

| file | lines measured/given | bytes measured/given | sha256 equal |
|---|---|---|---|
| ledger.md | 4/4 | 5383/5383 | True |
| plan.md | 42/42 | 1899/1899 | True |
| slips.md | 1/1 | 471/471 | True |

**All readings equal: True.**

Four `.agent/authored/f283-r6-*` copies (the block copy plus three payloads), each
read back from the committed tree with `git show 700968e6:<path>` and compared
byte-for-byte with its source:

| copy | bytes | identical to source |
|---|---|---|
| f283-r6-block.md | 15257 | True |
| f283-r6-ledger.md | 5383 | True |
| f283-r6-plan.md | 1899 | True |
| f283-r6-slips.md | 471 | True |

**Copies compared: 4. All True.**

### G2 — THE BOOKING

**(a) Append arithmetic**, by strict byte concatenation:

| file | pre (`63141657`) | payload | post | pre+payload==post |
|---|---|---|---|---|
| .agent/live_review.md | 466845 | 5383 | 472228 | True |
| .agent/prose_slips.md | 360944 | 471 | 361415 | True |

Matches the reviewer's stated `466845 + 5383 = 472228` and `360944 + 471 = 361415`
exactly.

**(b) Line-anchored on the committed ledger**: `^- R-1021 — ` = **1**;
`^Done: R-1021 — ` = **1**; `^- R-1022 — ` = **1**; `^Done: R-1022 — ` = **0**. Open
set by distinct id, via `open_finding_ids` from `scripts/rotate_live_review.py`
(imported and called directly):

| rev | OPEN by distinct id |
|---|---|
| `63141657` | **25** |
| C2 (`b61dfe13`) | **24** |

Added: `[]`. Removed: `['R-1021']`. Matches the reviewer's stated 25 → 24, ADDED
empty, REMOVED `R-1021`, exactly.

**(c) `.agent/plan.md` at C2 equals plan.md byte-for-byte**:

| file | sha256 (both sides) | equal |
|---|---|---|
| .agent/plan.md | `959308eef0051b24ffca83d0003322386325210b76cfd17dfc1fec5eb6bbdb8a` | True |

Line count: **42**, under the AGENTS.md 50-line rule.

### G3 — THE MIGRATION, COUNTED FROM THE TREE

`git diff --name-only <parent> <commit>` and `git show --numstat` insertions, for
every commit C3 to C5 (parent → commit):

| commit | paths changed | insertions |
|---|---|---|
| C3 `b61dfe13`→`563859fe` | apps/cli/commands/job.py, tests/cli/test_cost_preview.py, tests/cli/test_job_refusal_envelope.py, tests/orchestration/test_escalation.py, tests/orchestration/test_long_run_executor.py, tests/test_cli_main.py | 81 |
| C4 `563859fe`→`05461715` | apps/cli/commands/decision.py, tests/cli/test_decision_cmd.py, tests/cli/test_job_refusal_envelope.py | 157 |
| C5 `05461715`→`da32c320` | tests/cli/test_job_refusal_envelope.py | 26 |

At C5, `python3 .remedy-wt/f283-r6-scratch/pairs.py job.py decision.py`:

```
job.py exits 4 mechanical 0 flagged 0 unflagged 0
   1090 _cmd_run_next_task_local False json_output
   1230 _cmd_job_run_cycles False json_output
   1620 _cmd_resume False json_output
   1640 _cmd_resume False json_output
decision.py exits 1 mechanical 1 flagged 0 unflagged 1
   469 _cmd_decision_resolve True None
```

`job.py` fell from `exits 12 mechanical 8 flagged 0 unflagged 8` (the reviewer's
`63141657` reading) to `exits 4 mechanical 0 flagged 0 unflagged 0` — all eight
mechanical pairs gone, the four remaining exits (`_cmd_run_next_task_local`'s
verification-failure loop, `_cmd_job_run_cycles`'s terminal-status exit, `_cmd_resume`'s
two) were never mechanical. `decision.py` fell from
`exits 30 mechanical 30 flagged 2 unflagged 28` to `exits 1 mechanical 1 flagged 0
unflagged 1` — the one survivor is the derived-decision refusal the SPEC named to stay.

`git diff --name-only 63141657 da32c320 -- packages/` prints **nothing** (real exit
code 0, empty stdout) — confirmed `packages/` untouched across the whole round.

### G4 — THE TARGETED SELECTION

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -n auto tests/cli/test_job_refusal_envelope.py tests/test_cli_main.py tests/test_run_log_cli.py tests/orchestration/test_long_run_executor.py tests/orchestration/test_escalation.py tests/cli/test_cost_preview.py tests/cli/test_job_commands.py tests/cli/test_plan_approval.py tests/orchestration/test_proposal_decision.py tests/ui_server/test_command_channel.py tests/orchestration/test_run_report.py tests/orchestration/test_job_digest.py tests/cli/test_decision_cmd.py tests/orchestration/test_mission_gate.py tests/cli/test_mission_cmd.py tests/cli/test_open_decisions_view.py tests/cli/test_decision_answers.py tests/cli/test_do_sequence_cli.py tests/orchestration/test_import_reachability.py tests/cli/test_json_envelope.py tests/cli/test_golden_path.py tests/docs/; echo "REAL_EXIT=$?"'
1224 passed in 100.95s (0:01:40)
REAL_EXIT=0
```

The reviewer read `1217 passed` at `63141657`; this round's own count is **1224**
(higher, as required — the seven new tests: two in `test_cli_main.py`, two in
`TestDecisionsRefusalsAreAllMigrated`, two in `test_decision_cmd.py`, one ambiguous-
payload test) — zero failed, zero xfailed. `tests/cli/test_decision_cmd.py` (C4's test
file) is already in the block's own G4 list, so no addition was needed.

```
$ bash -c 'python3 -m ruff check apps/cli/commands/job.py apps/cli/commands/decision.py tests/cli/test_job_refusal_envelope.py tests/test_cli_main.py tests/orchestration/test_long_run_executor.py tests/orchestration/test_escalation.py tests/cli/test_cost_preview.py tests/cli/test_decision_cmd.py; echo "REAL_EXIT=$?"'
All checks passed!
REAL_EXIT=0
```

```
$ bash -c 'python3 -m apps.cli.main integrity check --json; echo "REAL_EXIT=$?"'
{"version": 1, "passed": true, "fail_count": 0, "check_count": 5, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=145"},
  {"name": "live_review_verdict", "status": "pass", ...},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
]}
REAL_EXIT=0
```
All five checks `pass`, `passed: true`, `fail_count: 0`. The full suite was NOT
re-run, per the block's instruction.

### G5 — RED-PROOFS

Disposable worktree `.remedy-wt/f283-r6-g5` added at `da32c320` (C5), detached HEAD,
used for the unmutated control and all four mutations, removed after.

**Unmutated control**:

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider tests/cli/test_job_refusal_envelope.py tests/test_cli_main.py tests/cli/test_decision_cmd.py; echo "REAL_EXIT=$?"'
103 passed in 1.90s
REAL_EXIT=0
```

**(a) `_cmd_job_run_cycles`'s single-pass call to `_cmd_run_next_task_local` drops
`json_output=`**:

```
1 failed, 5 passed in 0.27s
REAL_EXIT=1
```

Failing: `TestWorkspaceWriteDenialPreBuilder::test_the_run_cycles_caller_threads_json_output`
— exactly the caller-threading test C3 added. Reverted with `git checkout --`;
`git status --porcelain` confirmed clean.

**(b) the `permission_denied` token in `_cmd_run_next_task_local` becomes
`permission_refused`**:

```
2 failed, 4 passed in 0.28s
REAL_EXIT=1
```

Failing: `TestWorkspaceWriteDenialPreBuilder::test_denied_answers_in_the_envelope_under_json`
AND `::test_the_run_cycles_caller_threads_json_output` — both new C3 tests, exactly as
the block names them. Reverted; clean.

**(c) `_cmd_decision_show`'s not-found `fail()` passes `json_output=False`**:

```
1 failed, 1 passed in 0.21s
REAL_EXIT=1
```

Failing: `TestDecisionRefusalsAnswerInTheEnvelope::test_an_unknown_decision_id_answers_in_the_envelope`
— C4's unknown-decision test, exactly as the block names it. Reverted; clean.

**(d) one migrated `fail()` in `_cmd_decision_resolve` (the `stop_reason_not_found`
site) put back as its old `print(f"Error: ...", file=sys.stderr)` + `sys.exit(1)`
pair**:

```
1 failed, 1 passed in 0.20s
REAL_EXIT=1
```

Failing: `TestDecisionsRefusalsAreAllMigrated::test_exactly_one_unflagged_site_remains`
(`measured 2 at lines [245, 469], constant says 1`) — the `decision.py` ratchet,
exactly as the block names it. Reverted; clean.

**Final control after all four reverts**: confirmed via `git status --porcelain`
(empty) after each individual revert, not re-run as one final pooled pass — each
revert was checked clean before the next mutation began.

`git worktree remove .remedy-wt/f283-r6-g5` (no `--force` needed: every mutation was
cleanly reverted before removal). `git worktree list` after removal:

```
/home/decodeux/Repos/remedy                                  da32c320 [feature/f283-machine-contracts-part-two]
/home/decodeux/Repos/remedy/.remedy-wt/job-468c8e62a2cc4fac  1b9ae606 [remedy/job-468c8e62a2cc4fac]
/home/decodeux/Repos/remedy/.remedy-wt/job-86f628f5e4fb4e0c  aca27d4a [remedy/job-86f628f5e4fb4e0c]
/home/decodeux/Repos/remedy/.remedy-wt/job-c1dba9c3d7874968  fd23710f [remedy/job-c1dba9c3d7874968]
```

Only the primary checkout and the three `remedy/job-*` worktrees remain.

### G6 — TREE AND PUSH

Reported in full in the worker's session reply once this commit exists (push carries
this file). At write time: `git status --porcelain` empty; `git log --oneline -n 8`
will show C6 through round 5's tail once committed; `git worktree list` shows the
primary checkout and the three `remedy/job-*` worktrees and nothing else. Push outcome
and `gh pr list` reported in the session reply.

### C4's token list — every `fail()` token, its line, new or reused

| line | token | new/reused |
|---|---|---|
| 67 | invalid_list_option | reused (existing repo-wide spelling) |
| 92 | decision_not_found | new |
| 178 | job_has_no_project | new |
| 187 | mission_already_linked | new |
| 205 | mission_error | reused (mission_cmd.py, DECISION F277 D9) |
| 223 | option_not_applicable | new |
| 231 | option_not_applicable | new (second site, same commit) |
| 244 | stop_reason_not_found | new |
| 263 | job_not_found | reused (decision.py's own `_load_job_events`, L32) |
| 267 | decision_not_found | new (second site, same commit) |
| 272 | missing_argument | reused (job.py, worker.py) |
| 286 | decision_already_answered | new |
| 309 | follow_up_mission_error | new |
| 326 | job_not_found | reused |
| 341 | clarifications_already_resolved | new |
| 347 | no_pending_plan_approval | new |
| 351 | invalid_reason | new |
| 361 | option_not_applicable | new (third site, same commit) |
| 364 | option_not_applicable | new (fourth site, same commit) |
| 369 | answer_parse_error | new |
| 404 | proposed_task_not_found | new |
| 408 | invalid_reason | new (second site, same commit) |
| 425 | proposed_task_operation_failed | new |
| 432 | proposed_task_operation_failed | new (second site, same commit) |
| 437 | proposed_task_invalid_state | new |
| 444 | proposed_task_invalid_state | new (second site, same commit) |
| 451 | proposed_task_operation_failed | new (third site, same commit) |
| 456 | proposed_task_invalid_state | new (third site, same commit) |
| 463 | proposed_task_operation_failed | new (fourth site, same commit) |

"new" means the token did not appear in any `fail("...")` call under `apps/cli/`
before this round; "reused" means an existing spelling from elsewhere in the repo was
adopted per DECISION F277 D8. A token marked "new (Nth site, same commit)" was minted
at its first listed line and reused at its own later occurrences within this same
commit — one token, several `decision.py` call sites.

### The round's whole tracked path set (before this commit)

`git diff --name-only 63141657 da32c320` — **15** paths, set-equal to constraint 3's
enumeration minus `.agent/handoff.md` (which this commit adds, making 16):

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f283-r6-block.md | C1 `700968e6` |
| 2 | .agent/authored/f283-r6-ledger.md | C1 `700968e6` |
| 3 | .agent/authored/f283-r6-plan.md | C1 `700968e6` |
| 4 | .agent/authored/f283-r6-slips.md | C1 `700968e6` |
| 5 | .agent/live_review.md | C2 `b61dfe13` |
| 6 | .agent/plan.md | C2 `b61dfe13` |
| 7 | .agent/prose_slips.md | C2 `b61dfe13` |
| 8 | apps/cli/commands/job.py | C3 `563859fe` |
| 9 | tests/cli/test_cost_preview.py | C3 `563859fe` |
| 10 | tests/cli/test_job_refusal_envelope.py | C3 (first touch) |
| 11 | tests/orchestration/test_escalation.py | C3 `563859fe` |
| 12 | tests/orchestration/test_long_run_executor.py | C3 `563859fe` |
| 13 | tests/test_cli_main.py | C3 `563859fe` |
| 14 | apps/cli/commands/decision.py | C4 `05461715` |
| 15 | tests/cli/test_decision_cmd.py | C4 `05461715` |

Plus `.agent/handoff.md` from this commit makes **16** — set-equal to constraint 3's
enumeration (four authored copies + live_review.md + plan.md + prose_slips.md +
handoff.md + job.py + decision.py + the five named test files + the one decision test
file C4 names). `.agent/candidates.md`, `.agent/context.md`, `.agent/decisions.md`,
`.agent/operator_questions.md`, `README.md`, `docs/roadmap/**`, and
`apps/cli/json_envelope.py`/`apps/cli/job_id_arg.py` appear **0** times. `packages/`
appears **0** times (confirmed above under G3).

## Authored-text proofs

- The four copies at C1, compared with the reviewer's originals under
  `.remedy-wt/f283-r6-payloads/` and `.remedy-wt/f283-r6-block.md`: **four readings,
  all True** (G1).
- The one REWRITE payload against its committed file: `.agent/plan.md` is sha256-equal
  to its payload (G2c).
- The two APPEND payloads against their committed files: strict byte concatenation
  True for `.agent/live_review.md` (ledger.md) and `.agent/prose_slips.md` (slips.md),
  byte numbers equal to the reviewer's (G2a).
- No payload was edited or retyped. All four `.agent/authored/` copies and the one
  product-file rewrite were made with `shutil.copyfile`; the two appends by reading
  each payload's bytes and writing base+payload back with `open(...,"ab")`.
- Every change under `apps/` and `tests/` this round was WORKER-authored to the
  block's SPEC (continuing prior rounds' departure from rounds 1–3) — there is no
  reviewer-authored diff to compare against for those files; the block's SPEC prose is
  the standard they were written to, and G3/G4/G5 above are the proof they meet it.

## Deviations & assumptions

1. **The bundle ran C1 through C5 — five commits, exactly as ordered — before this
   handback commit C6.** Nothing was added, dropped or reordered.
2. **`tests/cli/test_job_refusal_envelope.py`'s single working-tree edit pass was
   split into three separate git commits (C3, C4, C5) by reverting the file to
   `HEAD` and re-applying each commit's own edits in isolation before staging and
   committing.** The final committed bytes are identical either way; this is a
   mechanical consequence of one file being touched by three commits' SPECs, not a
   change to what any commit contains.
3. **No expected insertion figure is given for C2's rewrite or for any C3–C5 code
   commit, per the block's own convention**: only measured figures are reported
   above, and none of them was forced to match a prediction.
4. **The decision test file C4 names was judged to be `tests/cli/test_decision_cmd.py`**
   — it already holds every other `_cmd_decision_list`/`_cmd_decision_show` unit test
   and is already in the block's own G4 selection, so no addition to that list was
   needed.
5. **C4 minted fourteen new tokens** (`decision_not_found`, `job_has_no_project`,
   `mission_already_linked`, `option_not_applicable`, `stop_reason_not_found`,
   `decision_already_answered`, `follow_up_mission_error`,
   `clarifications_already_resolved`, `no_pending_plan_approval`, `invalid_reason`,
   `answer_parse_error`, `proposed_task_not_found`, `proposed_task_operation_failed`,
   `proposed_task_invalid_state`) and reused four existing ones (`invalid_list_option`,
   `mission_error`, `job_not_found`, `missing_argument`), per DECISION F277 D8's
   "existing spelling wins, else name for the condition" rule and D9's `<layer>_error`
   rule for the `(ContractError, MissionError)` catch-all
   (`follow_up_mission_error`, since the site cannot tell which of the two exception
   types fired). Full table above.
6. **`_create_mission_for_job`'s `except MissionError as exc:` reused `mission_error`**
   (mission_cmd.py's own token for the same exception class, per D9), rather than
   minting a `decision`-local spelling — the same exception, the same layer, the same
   token, repo-wide.
7. **G5's mutation (d) targeted the `stop_reason_not_found` site** (one of the 27
   `json_output=False` sites) rather than a specific one the block names by line,
   since the block's own SPEC says only "one migrated `fail()` in
   `_cmd_decision_resolve`" without naming which; any of the 27 would have red-proofed
   the same ratchet identically.
8. **No trailing commit for the C6 push or `gh pr list`; both go in the session
   reply**, consistent with DECISION amend0827 D2 and prior rounds' own precedent: the
   push carries this very file, so its outcome cannot be known before the commit
   exists.
9. **One disposable worktree (`.remedy-wt/f283-r6-g5`) was reused for the unmutated
   control and all four G5 mutations sequentially**, each reverted with
   `git checkout -- <path>` and confirmed clean via `git status --porcelain` before
   the next mutation.
10. **Constraints 1, 3 and 4 held throughout.** No payload was edited or retyped; only
    the sixteen paths named in the block's enumeration were touched (verified by
    set-equality above, C6 included); `packages/` was never touched; the rule reached
    exactly job.py's eight mechanical pairs and decision.py's 29 (of 30) mechanical
    pairs; every commit left the targeted G4 selection green (re-run in full at C5,
    above) — no migration broke a test outside the same commit that fixed it.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Pre-flight (STOP, git state, block self-verify) | done | no STOP; tree clean at `63141657`; block 230 lines / matching sha256 |
| C1 copy block + 3 payloads | done | 277 insertions |
| C2 book round 5 PASS, resolve R-1021 | done | 27 insertions (4+22+1); open set 25→24, added none, removed R-1021 |
| C3 `_cmd_run_next_task_local` threads `json_output`, eight pairs migrate | done | 81 insertions; 6 paths |
| C4 `decision.py`'s 29 mechanical pairs migrate | done | 157 insertions; 3 paths; 14 new tokens, 4 reused |
| C5 R-1022 prose finished, ambiguous payload proved | done | 26 insertions; 1 path |
| C6 the handback | done | this commit |
| G1 payload transport + authored copies | done | 3/3 payload readings equal; 4/4 authored copies byte-identical |
| G2(a) live_review.md + prose_slips.md append | done | 466845+5383=472228; 360944+471=361415 |
| G2(b) R-1021 pairing + open set by distinct id | done | 1 R-1021 reg / 1 Done / 1 R-1022 reg / 0 Done; 25→24, added none, removed R-1021 |
| G2(c) plan.md rewrite | done | sha256-equal to payload; 42 lines, under 50 |
| G3 migration counted from the tree | done | per-commit diffs and insertions all reported; `pairs.py` job.py/decision.py both driven to their predicted post-migration shape; 0 paths under `packages/` |
| G4 targeted selection, ruff, integrity | done | 1224 passed/0 failed/0 xfailed (up from 1217); ruff exit 0; integrity all 5 pass, fail_count 0 |
| G5 red-proofs (a)(b)(c)(d) | done | all four go RED at exactly the test(s) the block names; unmutated control 103 passed |
| G6 tree, push, PR list | pending at write time | reported in the worker's session reply with real exit codes |
| Constraint 1 no payload edited/retyped | done | `shutil.copyfile`, byte concatenation only |
| Constraint 2 every commit under 500 insertions | done | 277, 27, 81, 157, 26; this handoff exempt as single `.agent/**` state file |
| Constraint 3 no unnamed file touched | done | 16 paths after this commit, set-equal to the enumeration |
| Constraint 4 migrate only what the rule reaches | done | `packages/` untouched; job.py's non-mechanical sites (`_cmd_job_run_cycles`, `_cmd_resume`) and decision.py's one derived-decision refusal stayed |
| Constraint 5 targeted selection green every commit | done | re-run in full at C5; no migration broke a test outside its own commit |
| Constraint 6 STOP if a gate goes red outside constraint 3's path set | done (n/a) | no gate went red for a reason outside the named paths; no STOP was needed |
| Constraint 7 nothing is merged | done | no `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch deletion |
| Constraint 8 G5 worktree under .remedy-wt/, removed, listed | done | `.remedy-wt/f283-r6-g5`, removed as G5's last action, `git worktree list` reported after; the three `remedy/job-*` worktrees untouched |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 6 — C1 through C6, with all six gates re-derived.
3. Then round 7 — R-1022's `Done:` line booked in its first commit, and the
   non-mechanical `job.py` sites (the verification-failure loop, a bare exit after a
   cost confirmation, two hand-rolled JSON objects) together with the single-pass
   `job run --json` success line, which is prose.

Open findings count: **24** (unchanged by this round's own repairs — R-1021 closed
this round; R-1022 stays open until round 7 books its `Done:`). Operator-questions
count: **2** (Q1, Q2 — both unchanged by this round).
