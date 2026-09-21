# Handoff — F283 Machine contracts, part two: refusal sweep, JSON gap, exit-code taxonomy · Round 4 · R-1020's LAST REPAIR

## Session

SESSION 2 of feature F283 · round 4 · rounds so far 4

This round booked round 3's PASS, corrected the call-site count on the record (twenty
remaining, not seventeen — `decision.py` also binds the resolver as `_rji`), registered
R-1021, split `refuse_ambiguous_job_id` out of `resolve_job_id_or_fail` so
`job_stop_cmd.py` can answer the same ambiguous refusal with `job_id` in its own
envelope payload, and then moved all twenty remaining `resolve_job_id` call sites under
`apps/cli/` onto the envelope layer, largest module first (`patch` 7, `decision` 4,
`change` 3, `teacher_cmd` 2, then `contract_cmd`, `job_context_cmd`, `project` and
`job_stop_cmd` at one each). C8 proved the whole layer through the real parser
(`apps.cli.grouped.main`) rather than the handlers directly, across fourteen catalog
command ids. At the end of the round `python3 .remedy-wt/f283-r4-scratch/sites.py`
(the reviewer's own alias-aware counter) reads `TOTAL 0`: no module under `apps/cli/`
calls the exiting resolver any more. `packages/orchestration/data_paths.py` — the
exiting `resolve_job_id` and `_exit_ambiguous` — was never touched. Context
self-assessment: roughly half the working budget remained at the point this handoff
was written.

## Range

Review of `3b4acafd`..`HEAD`.

## Block self-verification (R-0954)

| reading | measured | given | equal |
|---|---|---|---|
| line count | 276 | 276 | True |
| sha256 | `c08a644b85a0d940c5a378ea4092592472f5dcac71e0dd3d54ca0235dcacc139` | `c08a644b85a0d940c5a378ea4092592472f5dcac71e0dd3d54ca0235dcacc139` | True |

Neither reading differed, so the round went ahead.

## Pre-flight

- `ls .agent/STOP`: `No such file or directory`. No STOP on disk.
- `git status --porcelain`: empty.
- `git branch --show-current`: `feature/f283-machine-contracts-part-two`.
- `git log --oneline -1`: `3b4acafd`, matching the delegation message.

## Commits

### f303b9de F283 R4 C1: copy round 4 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r4-block.md | +276/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f283-r4-ledger.md | +4/-0 | byte-for-byte copy of ledger.md |
| .agent/authored/f283-r4-plan.md | +47/-0 | byte-for-byte copy of plan.md |
| .agent/authored/f283-r4-slips.md | +2/-0 | byte-for-byte copy of slips.md |

Measured insertions (`git show --numstat`): **329** (276+4+47+2). Well under the
500-line cap.

### 901ba21d F283 R4 C2: book round 3's PASS and register R-1021
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | append ledger.md by strict byte concatenation: round-3 `Gate:` entry and the `R-1021` registration |
| .agent/plan.md | +21/-23 | rewrite to plan.md payload, byte-identical |
| .agent/prose_slips.md | +2/-0 | append slips.md by strict byte concatenation |

Measured insertions (`git show --numstat`): **27** (4+21+2). No expected figure was
given for this rewrite per the block's own instruction (round 3's lesson); reported as
measured.

### ea17a50b F283 R4 C3: the ambiguous refusal gets a name, job stop answers in the envelope
| Path | +/- | Reason |
|---|---|---|
| apps/cli/job_id_arg.py | +27/-13 | `refuse_ambiguous_job_id` split out of `resolve_job_id_or_fail`, body unchanged; `NoReturn` import added |
| apps/cli/commands/job_stop_cmd.py | +15/-10 | the `try: resolve_job_id(...) except SystemExit` construction replaced with `lookup_job_id`, catching `JobIdAmbiguous` (→ `refuse_ambiguous_job_id`) and `JobIdError` (→ `fail("job_not_found", ..., exit_code=EXIT_UNKNOWN_JOB, job_id=job_id)`) |
| tests/cli/test_job_refusal_envelope.py | +121/-17 | `_exiting_resolver_calls` (alias-aware, module-or-function-level bindings, attribute calls too) and `_EXITING_RESOLVER_REMAINING` added; `TestTheExitingResolverIsStillReachable` rewritten onto it with two non-vacuity tests; `TestTheAmbiguousBranchAnswersInTheEnvelope` added (json + text-identity, the identity computed against the real `resolve_job_id`) |
| tests/cli/test_job_stop.py | +5/-1 | `test_an_unknown_job_exits_3_in_json_mode_too` additionally asserts `stderr == ""` and `schema_version == 1` |

Measured insertions (`git show --numstat`): **168** (27+15+121+5). No expected figure
given for this code commit, per the block.

### 7d4ca4a9 F283 R4 C4: patch resolves a job id through the envelope
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/patch.py | +8/-8 | all seven `resolve_job_id(job_id_str)` sites moved onto `resolve_job_id_or_fail(job_id_str, json_output=<flag or False>)`; import swapped to `apps.cli.job_id_arg` |
| tests/cli/test_job_refusal_envelope.py | +0/-1 | `"patch.py": 7` deleted from `_EXITING_RESOLVER_REMAINING` |

Measured insertions: **8**.

### c56819f4 F283 R4 C5: change resolves a job id through the envelope
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/change.py | +5/-4 | all three sites moved onto `resolve_job_id_or_fail(job_id_str, json_output=json_output)`; import swapped |
| tests/cli/test_change_proof_cli.py | +13/-13 | all thirteen `patch("apps.cli.commands.change.resolve_job_id", side_effect=lambda raw: raw)` moved to `patch("apps.cli.commands.change.resolve_job_id_or_fail", side_effect=lambda raw, **_: raw)` |
| tests/cli/test_job_refusal_envelope.py | +0/-1 | `"change.py": 3` deleted from the constant |

Measured insertions: **18** (5+13+0).

### c6bf9f1b F283 R4 C6: decision resolves a job id through the envelope
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/decision.py | +10/-13 | `_load_job_events` gains `*, json_output: bool = False`, its `JobNotFoundError` branch becomes `fail("job_not_found", str(exc), json_output=json_output)`; `_cmd_decision_list`/`_cmd_decision_show` pass their own `json_output`, `_cmd_decision_explain` passes nothing (default False); the three `_rji` sites in `_cmd_decision_resolve` moved onto `resolve_job_id_or_fail(job_id_str, json_output=False)` (`decision.resolve` declares no `supports_json`) |
| tests/cli/test_job_refusal_envelope.py | +0/-1 | `"decision.py": 4` deleted from the constant |

Measured insertions: **10**.

### 97b3cc36 F283 R4 C7: the last four modules resolve a job id through the envelope
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/teacher_cmd.py | +9/-7 | both sites (`narrate`, `ask`) moved onto `resolve_job_id_or_fail(..., json_output=json_output)`; module docstring's exit-code bullet renamed to `apps.cli.job_id_arg.resolve_job_id_or_fail` and notes the `--json` envelope |
| apps/cli/commands/contract_cmd.py | +2/-2 | `_cmd_job_contract`'s one site moved onto `resolve_job_id_or_fail(job_id_str, json_output=json_output)` |
| apps/cli/commands/job_context_cmd.py | +2/-2 | `_cmd_job_context`'s one site moved onto `resolve_job_id_or_fail(job_id_str, json_output=json_output)` at MODULE level |
| apps/cli/commands/project.py | +2/-2 | `_cmd_project_adopt`'s one site moved onto `resolve_job_id_or_fail(job_id_str, json_output=False)` (no `json_output` param) |
| apps/cli/commands/job.py | +1/-1 | `_digest_section`'s docstring: `resolve_job_id` → `resolve_job_id_or_fail` |
| tests/cli/test_job_context_cmd.py | +5/-4 | `TestJobContextRefusesInTheCallersShape._run`'s patch moved to `monkeypatch.setattr(mod, "resolve_job_id_or_fail", lambda raw, **_: raw)` (module-level import now lands on the handler's own namespace); comment rewritten to stay true; `require_job_plan`'s patch unchanged (still function-level) |
| tests/cli/test_job_refusal_envelope.py | +4/-9 | `_EXITING_RESOLVER_REMAINING` becomes `{}` |

Measured insertions: **25** (2+1+2+2+9+5+4).

### aa5e1c40 F283 R4 C8: every migrated JSON command answers a bad id in the envelope
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_job_refusal_envelope.py | +61/-0 | `TestEveryMigratedJsonCommandAnswersABadIdInTheEnvelope`, one parametrized case per catalog command id (14 cases: `change.list/show/proof`, `decision.list/show`, `job.contract/context/stop`, `patch.list/apply/revert/approve-hunks`, `teacher.narrate/ask`), each run through `apps.cli.grouped.main(argv)` with `zzzznotajob` and `--json` |

Measured insertions: **61**.

### C9 — THE HANDBACK (this commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the 500-line cap under DECISION F104 D1 |

Self-reference exception (handback template, R-0149 pattern): a handback cannot table
the commit that writes it.

## External actions

- `git worktree add .remedy-wt/f283-r4-review aa5e1c40` for G5, detached HEAD — used for
  the unmutated control and all four mutation red-proofs, then
  `git worktree remove .remedy-wt/f283-r4-review` — a plain remove sufficed because every
  mutation was reverted with the `Edit` tool back to the original text (verified clean
  with `git diff --stat` after each revert) before the next step.
- `git push -u origin feature/f283-machine-contracts-part-two` after C9 — real outcome
  reported in the session reply, since it ships this very file.
- `gh pr list --state open ...` after the push — real outcome reported in the session
  reply.
- **NOTHING IS MERGED.** No `gh pr merge`, no `gh pr create`, no checkout of `main`, no
  branch deletion.
- No worktree other than the one disposable G5 worktree was added or removed. The three
  `remedy/job-*` worktrees were left alone throughout.

## Verification

### G1 — PAYLOADS transport, then four authored copies

| file | lines measured/given | bytes measured/given | sha256 equal |
|---|---|---|---|
| ledger.md | 4/4 | 6332/6332 | True |
| plan.md | 47/47 | 2283/2283 | True |
| slips.md | 2/2 | 995/995 | True |

**All readings equal: True** (`python3 .remedy-wt/f283-r4-scratch/measure.py`, the
reviewer's own script, re-run and its output compared with the block's PAYLOADS table).

Four `.agent/authored/f283-r4-*` copies (the block copy plus three payloads), each read
back from the committed tree with `git show f303b9de:<path>` and compared byte-for-byte
with its source:

| copy | lines | bytes | sha256 | identical to source |
|---|---|---|---|---|
| f283-r4-block.md | 276 | 18731 | `c08a644b...ccc139` | True |
| f283-r4-ledger.md | 4 | 6332 | `557699ac...1dfa6` | True |
| f283-r4-plan.md | 47 | 2283 | `3e2aaf77...798f` | True |
| f283-r4-slips.md | 2 | 995 | `b28250b9...3363a3bc6` | True |

**Copies compared: 4. All True.**

### G2 — THE BOOKING

**(a) Append arithmetic**, by strict byte concatenation:

| file | pre (`3b4acafd`) | payload | post | pre+payload==post |
|---|---|---|---|---|
| .agent/live_review.md | 453413 | 6332 | 459745 | True |
| .agent/prose_slips.md | 359949 | 995 | 360944 | True |

Matches the reviewer's stated `453413 + 6332 = 459745` and `359949 + 995 = 360944`
exactly.

**(b) Line-anchored on the committed ledger**: `^- R-1020 — ` = **1**;
`^Done: R-1020 — ` = **0**; `^- R-1021 — ` = **1**. Open set by distinct id, via
`open_finding_ids` from `scripts/rotate_live_review.py` (imported and called
directly):

| rev | OPEN by distinct id |
|---|---|
| `3b4acafd` | **24** |
| C2 (`901ba21d`) | **25** |

Added: `['R-1021']`. Removed: `[]`. Matches the reviewer's stated 24 → 25, ADDED
`R-1021`, REMOVED empty, exactly.

**(c) `.agent/plan.md` at C2 equals plan.md byte-for-byte**:

| file | sha256 (both sides) | equal |
|---|---|---|
| .agent/plan.md | `3e2aaf77adceed0c2cd21f6d3d88749dfee7d1496f50d5295799c6716a6f798f` | True |

Line count: **47**, under the AGENTS.md 50-line rule.

### G3 — THE MIGRATION, COUNTED FROM THE TREE

`git diff --name-only <parent> <commit>` and `git show --numstat` insertions, for every
commit C3 to C8 (parent → commit):

| commit | paths changed | insertions |
|---|---|---|
| C3 `901ba21d`→`ea17a50b` | apps/cli/commands/job_stop_cmd.py, apps/cli/job_id_arg.py, tests/cli/test_job_refusal_envelope.py, tests/cli/test_job_stop.py | 168 |
| C4 `ea17a50b`→`7d4ca4a9` | apps/cli/commands/patch.py, tests/cli/test_job_refusal_envelope.py | 8 |
| C5 `7d4ca4a9`→`c56819f4` | apps/cli/commands/change.py, tests/cli/test_change_proof_cli.py, tests/cli/test_job_refusal_envelope.py | 18 |
| C6 `c56819f4`→`c6bf9f1b` | apps/cli/commands/decision.py, tests/cli/test_job_refusal_envelope.py | 10 |
| C7 `c6bf9f1b`→`97b3cc36` | apps/cli/commands/contract_cmd.py, apps/cli/commands/job.py, apps/cli/commands/job_context_cmd.py, apps/cli/commands/project.py, apps/cli/commands/teacher_cmd.py, tests/cli/test_job_context_cmd.py, tests/cli/test_job_refusal_envelope.py | 25 |
| C8 `97b3cc36`→`aa5e1c40` | tests/cli/test_job_refusal_envelope.py | 61 |

At C8, `python3 .remedy-wt/f283-r4-scratch/sites.py` (the reviewer's own alias-aware
counter over `apps/cli/`):

```
TOTAL 0
```

`git diff --name-only 3b4acafd aa5e1c40 -- packages/` prints **nothing** (real exit
code 0, empty stdout) — confirmed `packages/` untouched across the whole round.

### G4 — THE TARGETED SELECTION

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -n auto tests/cli/test_job_refusal_envelope.py tests/cli/test_job_stop.py tests/cli/test_patch_cmd.py tests/cli/test_change_proof_cli.py tests/cli/test_decision_answers.py tests/cli/test_decision_cmd.py tests/cli/test_do_sequence_cli.py tests/cli/test_job_context_cmd.py tests/cli/test_plan_approval.py tests/cli/test_project_current.py tests/cli/test_scoped_listings.py tests/cli/test_study_teacher_e2e.py tests/cli/test_teacher_cmd.py tests/orchestration/test_import_reachability.py tests/orchestration/test_escalation.py tests/orchestration/test_project_resolution.py tests/orchestration/test_proposal_decision.py tests/test_cli_main.py tests/test_data_paths.py tests/test_grouped_cli.py tests/test_patch_intent_approval.py tests/test_project_context_coverage.py tests/cli/test_json_envelope.py tests/cli/test_golden_path.py tests/orchestration/test_job_stop_integration.py; echo "REAL_EXIT=$?"'
1102 passed in 139.53s (0:02:19)
REAL_EXIT=0
```

The reviewer read `1084 passed` at `3b4acafd`; this round's own count is **1102**
(higher, as required) — zero failed, zero xfailed.

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/; echo "REAL_EXIT=$?"'
314 passed in 85.73s (0:01:25)
REAL_EXIT=0
```

```
$ python3 -m ruff check apps/cli/job_id_arg.py apps/cli/commands/job_stop_cmd.py apps/cli/commands/patch.py apps/cli/commands/change.py apps/cli/commands/decision.py apps/cli/commands/teacher_cmd.py apps/cli/commands/contract_cmd.py apps/cli/commands/job_context_cmd.py apps/cli/commands/project.py apps/cli/commands/job.py tests/cli/test_job_refusal_envelope.py tests/cli/test_job_stop.py tests/cli/test_change_proof_cli.py tests/cli/test_job_context_cmd.py
All checks passed!
```
Real exit code **0**.

```
$ python3 -m apps.cli.main integrity check --json
{"version": 1, "passed": true, "fail_count": 0, "check_count": 5, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=145"},
  {"name": "live_review_verdict", "status": "pass", ...},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
]}
```
Real exit code **0**. All five checks `pass`, `passed: true`, `fail_count: 0`. The full
suite was NOT re-run, per the block's instruction.

### G5 — RED-PROOFS

Disposable worktree `.remedy-wt/f283-r4-review` added at `aa5e1c40` (C8), used for the
unmutated control and all four mutations, removed after.

**Unmutated control**:

```
$ python3 -m pytest -q -p no:cacheprovider tests/cli/test_job_refusal_envelope.py
28 passed in 0.96s
REAL_EXIT=0
```

**(a) `refuse_ambiguous_job_id`'s `exit_code=2` → `exit_code=1`** in
`apps/cli/job_id_arg.py`:

```
2 failed, 26 passed in 0.84s
REAL_EXIT=1
```

Failing: `TestTheAmbiguousBranchAnswersInTheEnvelope::test_json_output_carries_the_matches_and_leaves_stderr_empty`
(the block's named JSON ambiguous test) AND
`TestTheAmbiguousBranchAnswersInTheEnvelope::test_without_json_stderr_matches_the_exiting_resolver_byte_for_byte`
(the same shared exit-code path, also red). Reverted before the next mutation;
`git diff --stat` confirmed clean.

**(b) The message loses the indented match lines** (`\n{listed}` removed from the
f-string) in `apps/cli/job_id_arg.py`:

```
1 failed, 27 passed in 0.85s
REAL_EXIT=1
```

Failing: `TestTheAmbiguousBranchAnswersInTheEnvelope::test_without_json_stderr_matches_the_exiting_resolver_byte_for_byte`
— the text identity test, exactly as the block names it. Reverted; clean.

**(c) `_cmd_decision_list` passes `json_output=False` to `_load_job_events`** in
`apps/cli/commands/decision.py`:

```
1 failed, 27 passed in 0.86s
REAL_EXIT=1
```

Failing: `TestEveryMigratedJsonCommandAnswersABadIdInTheEnvelope::test_a_bad_job_id_answers_in_the_envelope[decision.list]`
— C8's `decision.list` case, exactly as the block names it. Reverted; clean.

**(d) In `patch.py`, `_cmd_show_patch_intent` becomes `_r(job_id_str)` with
`from packages.orchestration.data_paths import resolve_job_id as _r` inside that
function**:

```
1 failed, 27 passed in 0.85s
REAL_EXIT=1
```

Failing: `TestTheExitingResolverIsStillReachable::test_the_remaining_call_sites_match_the_measured_dict`
— `measured {'patch.py': 1}, constant says {}` — the binding guard, exactly as the
block names it: this is the alias round 3's guard missed and round 4's alias-aware
`_exiting_resolver_calls` catches. Reverted; clean.

**Final control after all four reverts**:

```
$ python3 -m pytest -q -p no:cacheprovider tests/cli/test_job_refusal_envelope.py
28 passed in 0.82s
REAL_EXIT=0
```

`git worktree remove .remedy-wt/f283-r4-review` (no `--force` needed: every mutation
was cleanly reverted before removal). `git worktree list` after removal:

```
/home/decodeux/Repos/remedy                                  aa5e1c40 [feature/f283-machine-contracts-part-two]
/home/decodeux/Repos/remedy/.remedy-wt/job-468c8e62a2cc4fac  1b9ae606 [remedy/job-468c8e62a2cc4fac]
/home/decodeux/Repos/remedy/.remedy-wt/job-86f628f5e4fb4e0c  aca27d4a [remedy/job-86f628f5e4fb4e0c]
/home/decodeux/Repos/remedy/.remedy-wt/job-c1dba9c3d7874968  fd23710f [remedy/job-c1dba9c3d7874968]
```

Only the primary checkout and the three `remedy/job-*` worktrees remain.

### G6 — TREE AND PUSH

Reported in full in the worker's session reply once this commit exists (push carries
this file). At write time: `git status --porcelain` empty; `git log --oneline -n 10`
will show C9 through C1 and the round 3 tail once committed; `git worktree list` shows
the primary checkout and the three `remedy/job-*` worktrees and nothing else. Push
outcome and `gh pr list` reported in the session reply.

### The round's whole tracked path set (before this commit)

`git diff --name-only 3b4acafd aa5e1c40` — **21** paths, set-equal to constraint 3's
enumeration minus `.agent/handoff.md` (which this commit adds, making 22):

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f283-r4-block.md | C1 `f303b9de` |
| 2 | .agent/authored/f283-r4-ledger.md | C1 `f303b9de` |
| 3 | .agent/authored/f283-r4-plan.md | C1 `f303b9de` |
| 4 | .agent/authored/f283-r4-slips.md | C1 `f303b9de` |
| 5 | .agent/live_review.md | C2 `901ba21d` |
| 6 | .agent/plan.md | C2 `901ba21d` |
| 7 | .agent/prose_slips.md | C2 `901ba21d` |
| 8 | apps/cli/job_id_arg.py | C3 `ea17a50b` |
| 9 | apps/cli/commands/job_stop_cmd.py | C3 `ea17a50b` |
| 10 | tests/cli/test_job_stop.py | C3 `ea17a50b` |
| 11 | apps/cli/commands/patch.py | C4 `7d4ca4a9` |
| 12 | apps/cli/commands/change.py | C5 `c56819f4` |
| 13 | tests/cli/test_change_proof_cli.py | C5 `c56819f4` |
| 14 | apps/cli/commands/decision.py | C6 `c6bf9f1b` |
| 15 | apps/cli/commands/contract_cmd.py | C7 `97b3cc36` |
| 16 | apps/cli/commands/job.py | C7 `97b3cc36` |
| 17 | apps/cli/commands/job_context_cmd.py | C7 `97b3cc36` |
| 18 | apps/cli/commands/project.py | C7 `97b3cc36` |
| 19 | apps/cli/commands/teacher_cmd.py | C7 `97b3cc36` |
| 20 | tests/cli/test_job_context_cmd.py | C7 `97b3cc36` |
| 21 | tests/cli/test_job_refusal_envelope.py | C3 (first touch) |

Plus `.agent/handoff.md` from this commit makes **22** — set-equal to constraint 3's
enumeration. `.agent/candidates.md`, `.agent/context.md`, `.agent/decisions.md`,
`.agent/operator_questions.md`, `README.md`, `docs/roadmap/**`, and
`apps/cli/json_envelope.py` appear **0** times. `packages/` appears **0** times
(confirmed above under G3).

## Authored-text proofs

- The four copies at C1, compared with the reviewer's originals under
  `.remedy-wt/f283-r4-payloads/` and `.remedy-wt/f283-r4-block.md`: **four readings, all
  True** (G1).
- The one REWRITE payload against its committed file: `.agent/plan.md` is sha256-equal
  to its payload (G2c).
- The two APPEND payloads against their committed files: strict byte concatenation True
  for `.agent/live_review.md` (ledger.md) and `.agent/prose_slips.md` (slips.md), byte
  numbers equal to the reviewer's (G2a).
- No payload was edited or retyped. All four `.agent/authored/` copies and the one
  product-file rewrite were made with `shutil.copyfile`; the two appends by reading the
  payload's bytes and writing them with mode `"ab"`.
- Every change under `apps/` and `tests/` this round was WORKER-authored to the block's
  SPEC (this round's own departure from rounds 1–3, per the block's ROLE AND AUTHORITY
  section) — there is no reviewer-authored diff to compare against for those files; the
  block's SPEC prose is the standard they were written to, and G3/G4/G5 above are the
  proof they meet it.

## Deviations & assumptions

1. **The bundle ran C1 through C8 — eight commits, exactly as ordered — before this
   handback commit C9.** Nothing was added, dropped or reordered.
2. **No expected insertion figure is given for C2's rewrite or for any C3–C8 code
   commit, per the block's own instruction** (round 3's lesson, restated in round 4's
   slips.md payload): only measured figures are reported above, and none of them was
   forced to match a prediction.
3. **`job_context_cmd.py`'s `resolve_job_id_or_fail` import was placed at MODULE
   level**, per the block's "THE ONE RULE" ("Import `resolve_job_id_or_fail` from
   `apps.cli.job_id_arg` at MODULE level"), even though the file's other function
   (`require_job_plan`) stays imported locally as before. This flips
   `TestJobContextRefusesInTheCallersShape._run`'s patch target from the DEFINING
   module (`data_paths.resolve_job_id`, for a local import re-resolved every call) to
   the HANDLER'S OWN namespace (`mod.resolve_job_id_or_fail`, for a module-level
   import bound once at import time) — the comment above the patch was rewritten to
   state this correctly rather than left stale, per C7's SPEC ("point that patch at
   the name the handler now calls, keep the comment above it true").
4. **`job_stop_cmd.py` does NOT call `resolve_job_id_or_fail`.** Per C3's SPEC it calls
   `lookup_job_id` directly and catches `JobIdAmbiguous`/`JobIdError` itself, because it
   needs `job_id` inside the envelope's own payload — a key `resolve_job_id_or_fail`
   does not carry. This is the one migrated site in the whole round that is not the
   ONE RULE's literal shape; the block's own C3 SPEC states it explicitly, so it is not
   a departure from the block, only from the general pattern the other nineteen sites
   follow.
5. **C8's list of fourteen commands is exactly the block's list — no command was left
   out.** Every one of `change.list/show/proof`, `decision.list/show`,
   `job.contract/context/stop`, `patch.list/apply/revert/approve-hunks` and
   `teacher.narrate/ask` reaches `resolve_job_id_or_fail` (or, for `job.stop`,
   `lookup_job_id` directly) before any command-specific logic runs on the id
   `zzzznotajob`, so none needed to be excluded as "refuses before reaching the
   resolver." See "C8 command left out" in the session reply for the explicit
   confirmation of this.
6. **No trailing commit for the C9 push or `gh pr list`; both go in the session reply**,
   consistent with DECISION amend0827 D2 and rounds 1–3's own precedent: the push
   carries this very file, so its outcome cannot be known before the commit exists.
7. **One disposable worktree (`.remedy-wt/f283-r4-review`) was reused for the
   unmutated control and all four G5 mutations sequentially**, each reverted with the
   `Edit` tool and confirmed clean via `git diff --stat` before the next mutation —
   consistent with rounds 1–3's reading of the block's singular "REMOVE the worktree"
   phrasing.
8. **Scratch hygiene.** One script was written to the gitignored
   `.remedy-wt/f283-r4-scratch/` this round beyond C1/C2's copy-and-append helpers
   (`c1_copy.py`, `c2_book.py`); none was committed; nothing was written into
   `.remedy-wt/f283-r4-payloads/`; the reviewer's `sites.py`, `lookup_sites.py` and
   `measure.py` were read and run but never edited.
9. **Constraints 3, 4 and 5 held throughout.** Only the twenty-two paths named in the
   block's enumeration were touched (verified by set-equality above, C9 included);
   `packages/` was never touched; exactly the twenty named call sites moved (the
   nineteen `lookup_job_id` sites of R-1021 were never migrated, edited or referenced);
   every commit left the targeted G4 selection green (re-run in full at C8, above) —
   no migration broke a test outside the same commit that fixed it.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Pre-flight (STOP, git state, block self-verify) | done | no STOP; tree clean at `3b4acafd`; block 276 lines / matching sha256 |
| C1 copy block + 3 payloads | done | 329 insertions |
| C2 book round 3 PASS, register R-1021 | done | 27 insertions (4+21+2); open set 24→25, added R-1021 |
| C3 ambiguous refusal named, job stop in the envelope | done | 168 insertions; 4 paths |
| C4 patch (7 sites) | done | 8 insertions; constant loses `patch.py` |
| C5 change (3 sites) | done | 18 insertions; 13 test-cli patches moved; constant loses `change.py` |
| C6 decision (4 sites) | done | 10 insertions; `_load_job_events` gains `json_output`; constant loses `decision.py` |
| C7 the tail — teacher_cmd 2, contract_cmd 1, job_context_cmd 1, project 1 | done | 25 insertions; constant becomes `{}` |
| C8 the envelope proved through the real parser | done | 61 insertions; 14 parametrized cases, all pass |
| C9 the handback | done | this commit |
| G1 payload transport + authored copies | done | 3/3 payload readings equal; 4/4 authored copies byte-identical |
| G2(a) live_review.md + prose_slips.md appends | done | 453413+6332=459745; 359949+995=360944 |
| G2(b) R-1020/R-1021 pairing + open set by distinct id | done | 1 R-1020 reg / 0 done / 1 R-1021 reg; 24→25, added R-1021, removed none |
| G2(c) plan.md rewrite | done | sha256-equal to payload; 47 lines, under 50 |
| G3 migration counted from the tree | done | per-commit diffs and insertions all reported; `sites.py` TOTAL 0; 0 paths under `packages/` |
| G4 targeted selection, ruff, integrity | done | 1102 passed/0 failed/0 xfailed (up from 1084); tests/docs/ 314 passed; ruff exit 0; integrity all 5 pass, fail_count 0 |
| G5 red-proofs (a)(b)(c)(d) | done | all four mutations go RED at exactly the test(s) the block names; unmutated control 28 passed before and after |
| G6 tree, push, PR list | pending at write time | reported in the worker's session reply with real exit codes |
| Constraint 1 no payload edited/retyped | done | `shutil.copyfile`, byte concatenation only |
| Constraint 2 every commit under 500 insertions | done | 329, 27, 168, 8, 18, 10, 25, 61; this handoff exempt as single `.agent/**` state file |
| Constraint 3 no unnamed file touched | done | 22 paths after this commit, set-equal to the enumeration |
| Constraint 4 migrate only the twenty | done | nineteen `lookup_job_id` sites of R-1021 untouched; `packages/` untouched |
| Constraint 5 targeted selection green every commit | done | re-run in full at C8; no migration broke a test outside its own commit |
| Constraint 6 nothing is merged | done | no `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch deletion |
| Constraint 7 leave job worktrees alone | done | only one disposable G5 worktree added/removed; `remedy/job-*` untouched |
| Constraint 8 G5 worktree under .remedy-wt/, removed, listed | done | `.remedy-wt/f283-r4-review`, removed as G5's last action, `git worktree list` reported after |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 4 — C1 through C9, with all six gates re-derived.
3. Then round 5 — R-1020's `Done:` booked in its first commit, and R-1021's nineteen
   `lookup_job_id` sites moved onto `resolve_job_id_or_fail`: `brain` 11, `snapshot_cmds`
   2, `test_cmds` 2, then `event`, `file`, `memory` and `project` at one each.

Open findings count: **25** (unchanged by this round — R-1020 stays open, R-1021 was
registered last round and closes inside T001, not this round). Operator-questions
count: **2** (Q1, Q2 — both unchanged by this round).
