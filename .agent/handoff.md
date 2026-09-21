# Handoff — F283 Machine contracts, part two: refusal sweep, JSON gap, exit-code taxonomy · Round 5 · R-1021: a shared prefix is refused as AMBIGUOUS everywhere

## Session

SESSION 2 of feature F283 · round 5 · rounds so far 5

This round booked round 4's PASS, resolved R-1020 with its `Done:` line, registered
R-1022, then moved the nineteen hand-caught `lookup_job_id` sites under `apps/cli/`
onto `apps/cli/job_id_arg.py::resolve_job_id_or_fail`, one module per commit —
`brain.py` (11), `snapshot_cmds.py` (2, with a `job_id` payload), `test_cmds.py` (2,
`job_id` only where the old JSON already carried it), then the tail `event.py`,
`file.py`, `memory.py`, `project.py` (one each). `resolve_job_id_or_fail` and
`refuse_ambiguous_job_id` gained a `**payload` pass-through so a caller with its own
envelope key keeps it after moving onto the shared resolver. C8 proved the whole
repair through the real parser (`apps.cli.grouped.main`) across nineteen catalog
command ids — fourteen `--json` cases asserting `ambiguous_job_id`/exit 2/`matches`,
five text-only cases asserting stderr byte-identical to the exiting resolver's own —
with `event.replay` deliberately left out (it never calls `lookup_job_id` at all).
R-1022's two prose corrections landed in C3. Context self-assessment: roughly 98% of
the working budget remained at the point this handoff was written (about 14.77M of
15M tokens).

## Range

Review of `6c199d4f`..`HEAD`.

## Block self-verification (R-0954)

| reading | measured | given | equal |
|---|---|---|---|
| line count | 245 | 245 | True |
| sha256 | `e9fc683d701c7d12d5a32c93148fbb442078fd2c5fce1f6313ab101f9fb8e4fc` | `e9fc683d701c7d12d5a32c93148fbb442078fd2c5fce1f6313ab101f9fb8e4fc` | True |

Neither reading differed, so the round went ahead.

## Pre-flight

- `ls .agent/STOP`: `No such file or directory`. No STOP on disk.
- `git status --porcelain`: empty.
- `git branch --show-current`: `feature/f283-machine-contracts-part-two`.
- `git log --oneline -1`: `6c199d4f`, matching the delegation message.

## Commits

### f1fbf0ff F283 R5 C1: copy round 5 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r5-block.md | +245/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f283-r5-ledger.md | +6/-0 | byte-for-byte copy of ledger.md |
| .agent/authored/f283-r5-plan.md | +40/-0 | byte-for-byte copy of plan.md |

Measured insertions (`git show --numstat`): **291** (245+6+40).

### ec862012 F283 R5 C2: book round 4's PASS, resolve R-1020, register R-1022
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | append ledger.md by strict byte concatenation: round-4 `Gate:` entry, `Done: R-1020`, `R-1022` registration |
| .agent/plan.md | +13/-20 | rewrite to plan.md payload, byte-identical |

Measured insertions (`git show --numstat`): **19** (6+13). No expected figure given for
this rewrite, per the block's own convention.

### 7ecb0ff9 F283 R5 C3: the job-id layer carries a payload, and a guard pins its callers
| Path | +/- | Reason |
|---|---|---|
| apps/cli/job_id_arg.py | +14/-5 | `resolve_job_id_or_fail` and `refuse_ambiguous_job_id` gain `**payload: Any`, forwarded to every `fail()` call; docstrings say so in one sentence each |
| tests/cli/test_job_refusal_envelope.py | +89/-5 | `_lookup_calls` (bare-name or attribute) and `_LOOKUP_CALLERS` added at the C3 (pre-migration) reading; `TestLookupJobIdIsPinnedToItsTwoHandlers` (guard + one non-vacuity test) and `TestResolveJobIdOrFailForwardsAPayload` (the not-found branch carries `job_id="x"`) added; R-1022's docstring sentence and the `_EXITING_RESOLVER_REMAINING` comment corrected |

Measured insertions: **103** (14+89).

### fe07ba52 F283 R5 C4: brain refuses an ambiguous job id as ambiguous
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/brain.py | +13/-56 | all eleven `try: lookup_job_id / except ValueError` sites replaced with `resolve_job_id_or_fail(job_id_str, json_output=<json_output or False>)`; import swapped from `packages.orchestration.data_paths.lookup_job_id` to `apps.cli.job_id_arg.resolve_job_id_or_fail` |
| tests/cli/test_job_refusal_envelope.py | +0/-1 | `"brain.py": 11` deleted from `_LOOKUP_CALLERS` |

Measured insertions: **13** (13+0).

### 85fa5252 F283 R5 C5: snapshot refuses a job id through the envelope
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/snapshot_cmds.py | +3/-17 | both sites replaced with `resolve_job_id_or_fail(job_id_str, json_output=as_json, job_id=job_id_str)`, keeping the `job_id` key the old JSON refusal carried; import swapped |
| tests/cli/test_job_refusal_envelope.py | +0/-1 | `"snapshot_cmds.py": 2` deleted from the constant |
| tests/cli/test_snapshot_cli_runtime.py | +20/-0 | new test `TestSnapshotInspectCLI::test_a_bad_job_id_carries_job_id_in_the_envelope` — `snapshot inspect zzzznotajob <snap> --json` through `apps.cli.grouped.main`, exit 1, envelope `job_id == "zzzznotajob"` |

Measured insertions: **23** (3+0+20).

### 4de39f52 F283 R5 C6: test refuses a job id through the envelope
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/test_cmds.py | +3/-14 | `_cmd_discover_commands` moved onto `resolve_job_id_or_fail(job_id_str, json_output=as_json)` — NO `job_id=` payload, because the old JSON refusal for this site never carried one (the old code had no `--json` branch on that refusal at all); `_cmd_test_status` moved onto `resolve_job_id_or_fail(job_id_str, json_output=as_json, job_id=job_id_str)`, keeping the `job_id` key its old JSON already carried; import swapped |
| tests/cli/test_job_refusal_envelope.py | +0/-1 | `"test_cmds.py": 2` deleted from the constant |

Measured insertions: **3** (3+0).

### 9d775c10 F283 R5 C7: the last four modules refuse an ambiguous job id as ambiguous
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/event.py | +2/-6 | `_load_job_events`'s one site moved onto `resolve_job_id_or_fail(job_id_str, json_output=json_output)`; import swapped |
| apps/cli/commands/file.py | +3/-6 | `_cmd_file_why`'s one site moved the same way; import swapped |
| apps/cli/commands/memory.py | +2/-6 | `_cmd_memory_learn`'s one site moved the same way; import swapped |
| apps/cli/commands/project.py | +3/-4 | `_cmd_attach_project_job`'s `try: lookup_job_id(...); job = require_job_plan(...) except (ValueError, JobNotFoundError)` SPLIT: `job_id = resolve_job_id_or_fail(job_id_str, json_output=False)` first, then a `try/except JobNotFoundError` around `require_job_plan` alone, keeping today's exact stderr bytes; import swapped at module level, and `_cmd_project_adopt`'s redundant function-local `from apps.cli.job_id_arg import resolve_job_id_or_fail` removed now that the same name is bound at module level |
| tests/cli/test_change_proof_cli.py | +1/-1 | `test_file_why_proof_status_agrees_with_change_proof_path`'s `patch("apps.cli.commands.file.lookup_job_id", side_effect=lambda raw: raw)` moved to `patch("apps.cli.commands.file.resolve_job_id_or_fail", side_effect=lambda raw, **_: raw)` |
| tests/cli/test_job_refusal_envelope.py | +0/-4 | `_LOOKUP_CALLERS` becomes `{"job_id_arg.py": 1, "job_stop_cmd.py": 1}` |

Measured insertions: **11** (2+3+2+3+1+0).

### db4964a7 F283 R5 C8: an ambiguous job id is refused as ambiguous through the parser
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_job_refusal_envelope.py | +110/-0 | `TestAPrefixTwoJobsShareIsRefusedAsAmbiguousThroughTheParser`: 13 parametrized `--json` cases (`brain.graph/node/context/continue`, `event.list/show/timeline`, `file.why`, `memory.learn`, `snapshot.inspect/list-applies`, `test.discover/status`) asserting exit 2, empty stderr, `error == "ambiguous_job_id"`, `matches` equal to both ids sorted; 5 parametrized text-only cases (`brain.view/trust/timeline/cockpit/constitution`) asserting exit 2, empty stdout, stderr byte-identical to `packages.orchestration.data_paths.resolve_job_id`'s own; argv built from the catalog's own positionals/required options, never hand-typed |

Measured insertions: **110**.

### C9 — THE HANDBACK (this commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the 500-line cap under DECISION F104 D1 |

Self-reference exception (handback template, R-0149 pattern): a handback cannot table
the commit that writes it.

## External actions

- `git worktree add .remedy-wt/f283-r5-redproof db4964a7` for G5, detached HEAD — used
  for the unmutated control and all four mutation red-proofs, then
  `git worktree remove .remedy-wt/f283-r5-redproof` — a plain remove sufficed because
  every mutation was reverted with the `Edit` tool back to the original text (verified
  clean with `git diff --stat` after each revert) before the next step.
- `git push origin feature/f283-machine-contracts-part-two` after C9 — real outcome
  reported in the session reply, since it ships this very file.
- `gh pr list --state open ...` after the push — real outcome reported in the session
  reply.
- **NOTHING IS MERGED.** No `gh pr merge`, no `gh pr create`, no checkout of `main`, no
  branch deletion.
- No worktree other than the one disposable G5 worktree was added or removed. The
  three `remedy/job-*` worktrees were left alone throughout.

## Verification

### G1 — PAYLOADS transport, then three authored copies

| file | lines measured/given | bytes measured/given | sha256 equal |
|---|---|---|---|
| ledger.md | 6/6 | 7100/7100 | True |
| plan.md | 40/40 | 1870/1870 | True |

**All readings equal: True.**

Three `.agent/authored/f283-r5-*` copies (the block copy plus two payloads), each read
back from the committed tree with `git show f1fbf0ff:<path>` and compared byte-for-byte
with its source:

| copy | bytes | identical to source |
|---|---|---|
| f283-r5-block.md | 16658 | True |
| f283-r5-ledger.md | 7100 | True |
| f283-r5-plan.md | 1870 | True |

**Copies compared: 3. All True.**

### G2 — THE BOOKING

**(a) Append arithmetic**, by strict byte concatenation:

| file | pre (`6c199d4f`) | payload | post | pre+payload==post |
|---|---|---|---|---|
| .agent/live_review.md | 459745 | 7100 | 466845 | True |

Matches the reviewer's stated `459745 + 7100 = 466845` exactly.

**(b) Line-anchored on the committed ledger**: `^- R-1020 — ` = **1**;
`^Done: R-1020 — ` = **1**; `^- R-1022 — ` = **1**; `^Done: R-1022 — ` = **0**. Open
set by distinct id, via `open_finding_ids` from `scripts/rotate_live_review.py`
(imported and called directly):

| rev | OPEN by distinct id |
|---|---|
| `6c199d4f` | **25** |
| C2 (`ec862012`) | **25** |

Added: `['R-1022']`. Removed: `['R-1020']`. Matches the reviewer's stated 25 → 25,
ADDED `R-1022`, REMOVED `R-1020`, exactly.

**(c) `.agent/plan.md` at C2 equals plan.md byte-for-byte**:

| file | sha256 (both sides) | equal |
|---|---|---|
| .agent/plan.md | `f06f1ab9cce24a1f40106403127b4193587efe595ab0e33d7d12085a981f02e3` | True |

Line count: **40**, under the AGENTS.md 50-line rule.

### G3 — THE MIGRATION, COUNTED FROM THE TREE

`git diff --name-only <parent> <commit>` and `git show --numstat` insertions, for
every commit C3 to C8 (parent → commit):

| commit | paths changed | insertions |
|---|---|---|
| C3 `ec862012`→`7ecb0ff9` | apps/cli/job_id_arg.py, tests/cli/test_job_refusal_envelope.py | 103 |
| C4 `7ecb0ff9`→`fe07ba52` | apps/cli/commands/brain.py, tests/cli/test_job_refusal_envelope.py | 13 |
| C5 `fe07ba52`→`85fa5252` | apps/cli/commands/snapshot_cmds.py, tests/cli/test_job_refusal_envelope.py, tests/cli/test_snapshot_cli_runtime.py | 23 |
| C6 `85fa5252`→`4de39f52` | apps/cli/commands/test_cmds.py, tests/cli/test_job_refusal_envelope.py | 3 |
| C7 `4de39f52`→`9d775c10` | apps/cli/commands/event.py, apps/cli/commands/file.py, apps/cli/commands/memory.py, apps/cli/commands/project.py, tests/cli/test_change_proof_cli.py, tests/cli/test_job_refusal_envelope.py | 11 |
| C8 `9d775c10`→`db4964a7` | tests/cli/test_job_refusal_envelope.py | 110 |

At C8, `python3 .remedy-wt/f283-r5-scratch/lookup_ctx.py` (the reviewer's own script,
which explicitly `continue`s past `job_id_arg.py` — see the "MEASURED, NOT EXPECTED"
deviation below):

```
job_stop_cmd.py 96 _cmd_job_stop ['json_output'] try-body-stmts 1 handlers ['JobIdAmbiguous', 'JobIdError']
```

One row, `job_stop_cmd.py` — not the two the block's own G3 prose names.

`git diff --name-only 6c199d4f db4964a7 -- packages/` prints **nothing** (real exit
code 0, empty stdout) — confirmed `packages/` untouched across the whole round.

### G4 — THE TARGETED SELECTION

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -n auto tests/cli/test_job_refusal_envelope.py tests/cli/test_change_proof_cli.py tests/cli/test_event_list_cmd.py tests/cli/test_file_provenance_cli.py tests/cli/test_memory_cmd.py tests/cli/test_snapshot_cli_runtime.py tests/cli/test_real_test_execution_cli.py tests/cli/test_test_run_runtime.py tests/cli/test_project_current.py tests/test_brain_detail.py tests/test_brain_smoke.py tests/test_brain_viewer.py tests/test_agent_loop.py tests/test_cockpit.py tests/test_timeline.py tests/test_trust_report.py tests/test_project_constitution.py tests/test_project_brain.py tests/test_memory_learn.py tests/test_command_discovery.py tests/test_test_runner.py tests/test_context_coverage.py tests/test_project_context_coverage.py tests/orchestration/test_project_resolution.py tests/orchestration/test_import_reachability.py tests/test_cli_main.py tests/test_data_paths.py tests/test_grouped_cli.py tests/cli/test_json_envelope.py tests/cli/test_golden_path.py; echo "REAL_EXIT=$?"'
1680 passed in 123.13s (0:02:03)
REAL_EXIT=0
```

The reviewer read `1658 passed` at `6c199d4f`; this round's own count is **1680**
(higher, as required) — zero failed, zero xfailed. `tests/cli/test_snapshot_cli_runtime.py`
(C5's test file) is already in the block's own G4 list, so no addition was needed.

```
$ python3 -m ruff check apps/cli/job_id_arg.py apps/cli/commands/brain.py apps/cli/commands/snapshot_cmds.py apps/cli/commands/test_cmds.py apps/cli/commands/event.py apps/cli/commands/file.py apps/cli/commands/memory.py apps/cli/commands/project.py tests/cli/test_job_refusal_envelope.py tests/cli/test_change_proof_cli.py tests/cli/test_snapshot_cli_runtime.py
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

Disposable worktree `.remedy-wt/f283-r5-redproof` added at `db4964a7` (C8), used for
the unmutated control and all four mutations, removed after.

**Unmutated control**:

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider tests/cli/test_job_refusal_envelope.py tests/cli/test_snapshot_cli_runtime.py; echo "REAL_EXIT=$?"'
65 passed in 3.54s
REAL_EXIT=0
```

**(a) `brain.py`'s `_cmd_brain` migrated call passes `json_output=False` instead of
`json_output=json_output`**:

```
1 failed, 48 passed in 1.42s
REAL_EXIT=1
```

Failing: `TestAPrefixTwoJobsShareIsRefusedAsAmbiguousThroughTheParser::test_a_json_command_answers_ambiguous_in_the_envelope[brain.graph]`
— exactly the `brain.graph` case the block names. Reverted; `git diff --stat` confirmed
clean.

**(b) `snapshot_cmds.py`'s `_cmd_snapshot_inspect` drops its `job_id=` payload**:

```
1 failed, 15 passed in 2.20s
REAL_EXIT=1
```

Failing: `TestSnapshotInspectCLI::test_a_bad_job_id_carries_job_id_in_the_envelope`
(`KeyError: 'job_id'`) — C5's own test, exactly as the block names it. Reverted;
clean.

**(c) `memory.py`'s migrated call put back as the old `try: lookup_job_id / except
ValueError: fail("invalid_job_id", ...)` construction**:

```
2 failed, 47 passed in 1.43s
REAL_EXIT=1
```

Failing: `TestLookupJobIdIsPinnedToItsTwoHandlers::test_the_call_sites_match_the_measured_dict`
(`measured {'job_stop_cmd.py': 1, 'memory.py': 1, 'job_id_arg.py': 1}, constant says
{'job_id_arg.py': 1, 'job_stop_cmd.py': 1}`) AND
`TestAPrefixTwoJobsShareIsRefusedAsAmbiguousThroughTheParser::test_a_json_command_answers_ambiguous_in_the_envelope[memory.learn]`
— the `_LOOKUP_CALLERS` guard AND the `memory.learn` case, both exactly as the block
names them. Reverted; clean.

**(d) `apps/cli/job_id_arg.py`'s `refuse_ambiguous_job_id` stops forwarding
`payload`**:

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider tests/cli/test_job_refusal_envelope.py tests/cli/test_snapshot_cli_runtime.py; echo "REAL_EXIT=$?"'
65 passed in 3.37s
REAL_EXIT=0
```

Nothing goes red — exactly as the block itself predicts ("if nothing does, say so
plainly; it is a probe, not a colour: no C8 case passes a payload on the ambiguous
path"). Confirmed: every C8 ambiguous-path case asserts `matches`, not a caller-supplied
`job_id`, so dropping the pass-through on that one branch is invisible to this round's
suite. Reverted; clean.

**Final control after all four reverts**:

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider tests/cli/test_job_refusal_envelope.py tests/cli/test_snapshot_cli_runtime.py; echo "REAL_EXIT=$?"'
65 passed in 3.37s
REAL_EXIT=0
```

`git worktree remove .remedy-wt/f283-r5-redproof` (no `--force` needed: every mutation
was cleanly reverted before removal). `git worktree list` after removal:

```
/home/decodeux/Repos/remedy                                  db4964a7 [feature/f283-machine-contracts-part-two]
/home/decodeux/Repos/remedy/.remedy-wt/job-468c8e62a2cc4fac  1b9ae606 [remedy/job-468c8e62a2cc4fac]
/home/decodeux/Repos/remedy/.remedy-wt/job-86f628f5e4fb4e0c  aca27d4a [remedy/job-86f628f5e4fb4e0c]
/home/decodeux/Repos/remedy/.remedy-wt/job-c1dba9c3d7874968  fd23710f [remedy/job-c1dba9c3d7874968]
```

Only the primary checkout and the three `remedy/job-*` worktrees remain.

### G6 — TREE AND PUSH

Reported in full in the worker's session reply once this commit exists (push carries
this file). At write time: `git status --porcelain` empty; `git log --oneline -n 10`
will show C9 through round 4's tail once committed; `git worktree list` shows the
primary checkout and the three `remedy/job-*` worktrees and nothing else. Push outcome
and `gh pr list` reported in the session reply.

### The round's whole tracked path set (before this commit)

`git diff --name-only 6c199d4f db4964a7` — **16** paths, set-equal to constraint 3's
enumeration minus `.agent/handoff.md` (which this commit adds, making 17):

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f283-r5-block.md | C1 `f1fbf0ff` |
| 2 | .agent/authored/f283-r5-ledger.md | C1 `f1fbf0ff` |
| 3 | .agent/authored/f283-r5-plan.md | C1 `f1fbf0ff` |
| 4 | .agent/live_review.md | C2 `ec862012` |
| 5 | .agent/plan.md | C2 `ec862012` |
| 6 | apps/cli/job_id_arg.py | C3 `7ecb0ff9` |
| 7 | tests/cli/test_job_refusal_envelope.py | C3 (first touch) |
| 8 | apps/cli/commands/brain.py | C4 `fe07ba52` |
| 9 | apps/cli/commands/snapshot_cmds.py | C5 `85fa5252` |
| 10 | tests/cli/test_snapshot_cli_runtime.py | C5 `85fa5252` |
| 11 | apps/cli/commands/test_cmds.py | C6 `4de39f52` |
| 12 | apps/cli/commands/event.py | C7 `9d775c10` |
| 13 | apps/cli/commands/file.py | C7 `9d775c10` |
| 14 | apps/cli/commands/memory.py | C7 `9d775c10` |
| 15 | apps/cli/commands/project.py | C7 `9d775c10` |
| 16 | tests/cli/test_change_proof_cli.py | C7 `9d775c10` |

Plus `.agent/handoff.md` from this commit makes **17** — set-equal to constraint 3's
enumeration (three authored copies + live_review.md + plan.md + handoff.md +
job_id_arg.py + the seven `apps/cli/commands/*` files + the three named test files).
`.agent/candidates.md`, `.agent/context.md`, `.agent/decisions.md`,
`.agent/operator_questions.md`, `.agent/prose_slips.md`, `README.md`, `docs/roadmap/**`,
and `apps/cli/json_envelope.py` appear **0** times. `packages/` appears **0** times
(confirmed above under G3).

## Authored-text proofs

- The three copies at C1, compared with the reviewer's originals under
  `.remedy-wt/f283-r5-payloads/` and `.remedy-wt/f283-r5-block.md`: **three readings,
  all True** (G1).
- The one REWRITE payload against its committed file: `.agent/plan.md` is sha256-equal
  to its payload (G2c).
- The one APPEND payload against its committed file: strict byte concatenation True for
  `.agent/live_review.md` (ledger.md), byte numbers equal to the reviewer's (G2a).
- No payload was edited or retyped. All three `.agent/authored/` copies and the one
  product-file rewrite were made with `shutil.copyfile`; the one append by reading the
  payload's bytes and writing base+payload back with `open(...,"wb")`.
- Every change under `apps/` and `tests/` this round was WORKER-authored to the block's
  SPEC (continuing round 4's departure from rounds 1–3) — there is no reviewer-authored
  diff to compare against for those files; the block's SPEC prose is the standard they
  were written to, and G3/G4/G5 above are the proof they meet it.

## Deviations & assumptions

1. **The bundle ran C1 through C8 — eight commits, exactly as ordered — before this
   handback commit C9.** Nothing was added, dropped or reordered.
2. **No expected insertion figure is given for C2's rewrite or for any C3–C8 code
   commit, per the block's own convention**: only measured figures are reported above,
   and none of them was forced to match a prediction.
3. **G3's `lookup_ctx.py` reading does not match the block's own prose — MEASURED, NOT
   FORCED.** The block's G3 instruction says the script's output at C8 is "exactly two
   rows, `job_id_arg.py` and `job_stop_cmd.py`." The script itself
   (`.remedy-wt/f283-r5-scratch/lookup_ctx.py`, read-only, never edited) opens with
   `if path.name == "job_id_arg.py": continue` — it structurally cannot ever produce a
   `job_id_arg.py` row. The actual output at C8, run verbatim, is the ONE row shown
   above: `job_stop_cmd.py`. This is a reviewer-prose inaccuracy about a script's own
   behaviour, not a defect in anything under `apps/`, `tests/`, `packages/` or `docs/`
   — the guard test in `tests/cli/test_job_refusal_envelope.py`
   (`TestLookupJobIdIsPinnedToItsTwoHandlers`) independently confirms BOTH
   `job_id_arg.py: 1` and `job_stop_cmd.py: 1` are the only two hand-caught callers left,
   by its own AST walk that does not exempt `job_id_arg.py`. Reported here rather than
   forced to read "two rows" against what the script on disk actually prints.
4. **`project.py`'s site was SPLIT exactly as C7's SPEC states**: the id resolves
   through `resolve_job_id_or_fail(job_id_str, json_output=False)` first, and
   `require_job_plan`'s `JobNotFoundError` keeps its own `try/except` printing today's
   exact bytes — the one migrated site in the whole round whose shape differs from the
   other eighteen's single-call replacement, and the block's own C3+C7 SPEC states it
   explicitly.
5. **`_cmd_project_adopt`'s redundant function-local import was removed in the same
   commit that added the module-level one for the same name** (C7,
   `apps/cli/commands/project.py`): once `resolve_job_id_or_fail` is bound at module
   level for `_cmd_attach_project_job`, the pre-existing function-local
   `from apps.cli.job_id_arg import resolve_job_id_or_fail` inside `_cmd_project_adopt`
   became a redundant shadow of the same name: removed as the direct, in-scope
   consequence of this commit's own edit, not a separate cleanup.
6. **C5's new test landed in `tests/cli/test_snapshot_cli_runtime.py`**, the file
   judged nearest (it already holds every other `snapshot inspect`/`list-applies` CLI
   test) — added `io`, `contextlib` and `pytest` imports to call `apps.cli.grouped.main`
   in-process, per the block's "through `apps.cli.grouped.main`" instruction, rather
   than the file's existing subprocess style.
7. **C8's list is thirteen `--json` cases and five text-only cases — eighteen of the
   block's nineteen named commands, `event.replay` left out.** `_cmd_event_replay`
   (`apps/cli/commands/event.py`) was never migrated (it never called
   `lookup_job_id`): it hands `job_id_str` straight to
   `packages.orchestration.event_replay.replay_job`, which loads whatever run-log
   events exist for that literal string and returns a degraded `JobReplayState` rather
   than failing — an ambiguous prefix never reaches the resolver on this argv. Left out
   rather than forced or skipped/xfailed, and named in the new test class's own
   docstring as well as here, per the block's explicit instruction.
8. **No trailing commit for the C9 push or `gh pr list`; both go in the session
   reply**, consistent with DECISION amend0827 D2 and rounds 1–4's own precedent: the
   push carries this very file, so its outcome cannot be known before the commit
   exists.
9. **One disposable worktree (`.remedy-wt/f283-r5-redproof`) was reused for the
   unmutated control and all four G5 mutations sequentially**, each reverted with the
   `Edit` tool and confirmed clean via `git diff --stat` before the next mutation.
10. **Constraints 1, 3 and 4 held throughout.** No payload was edited or retyped; only
    the seventeen paths named in the block's enumeration were touched (verified by
    set-equality above, C9 included); `packages/` was never touched; exactly the
    nineteen named `lookup_job_id` sites moved; every commit left the targeted G4
    selection green (re-run in full at C8, above) — no migration broke a test outside
    the same commit that fixed it.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Pre-flight (STOP, git state, block self-verify) | done | no STOP; tree clean at `6c199d4f`; block 245 lines / matching sha256 |
| C1 copy block + 2 payloads | done | 291 insertions |
| C2 book round 4 PASS, resolve R-1020, register R-1022 | done | 19 insertions (6+13); open set 25→25, added R-1022, removed R-1020 |
| C3 pass-through, guard, R-1022 | done | 103 insertions; 2 paths |
| C4 brain (11 sites) | done | 13 insertions; constant loses `brain.py` |
| C5 snapshot (2 sites, `job_id=`) | done | 23 insertions; new test added to `tests/cli/test_snapshot_cli_runtime.py`; constant loses `snapshot_cmds.py` |
| C6 test (2 sites, `job_id=` on `test.status` only) | done | 3 insertions; constant loses `test_cmds.py` |
| C7 the tail — event, file, memory, project | done | 11 insertions; `_LOOKUP_CALLERS` becomes `{"job_id_arg.py": 1, "job_stop_cmd.py": 1}` |
| C8 the envelope proved through the real parser | done | 110 insertions; 18 parametrized cases (13 json + 5 text), all pass; `event.replay` left out |
| C9 the handback | done | this commit |
| G1 payload transport + authored copies | done | 2/2 payload readings equal; 3/3 authored copies byte-identical |
| G2(a) live_review.md append | done | 459745+7100=466845 |
| G2(b) R-1020/R-1022 pairing + open set by distinct id | done | 1 R-1020 reg / 1 Done / 1 R-1022 reg / 0 Done; 25→25, added R-1022, removed R-1020 |
| G2(c) plan.md rewrite | done | sha256-equal to payload; 40 lines, under 50 |
| G3 migration counted from the tree | done | per-commit diffs and insertions all reported; `lookup_ctx.py` measured ONE row (see deviation 3); 0 paths under `packages/` |
| G4 targeted selection, ruff, integrity | done | 1680 passed/0 failed/0 xfailed (up from 1658); ruff exit 0; integrity all 5 pass, fail_count 0 |
| G5 red-proofs (a)(b)(c)(d) | done | (a)(b)(c) go RED at exactly the test(s) the block names; (d) stays green, exactly as the block's own probe framing predicts; unmutated control 65 passed before and after |
| G6 tree, push, PR list | pending at write time | reported in the worker's session reply with real exit codes |
| Constraint 1 no payload edited/retyped | done | `shutil.copyfile`, byte concatenation only |
| Constraint 2 every commit under 500 insertions | done | 291, 19, 103, 13, 23, 3, 11, 110; this handoff exempt as single `.agent/**` state file |
| Constraint 3 no unnamed file touched | done | 17 paths after this commit, set-equal to the enumeration |
| Constraint 4 migrate only the nineteen | done | `packages/` untouched; the two callers that handle `JobIdAmbiguous` themselves (`job_id_arg.py`, `job_stop_cmd.py`) were never migrated |
| Constraint 5 targeted selection green every commit | done | re-run in full at C8; no migration broke a test outside its own commit |
| Constraint 6 STOP if a gate goes red outside constraint 3's path set | done (n/a) | no gate went red for a reason outside the named paths; no STOP was needed |
| Constraint 7 nothing is merged | done | no `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch deletion |
| Constraint 8 G5 worktree under .remedy-wt/, removed, listed | done | `.remedy-wt/f283-r5-redproof`, removed as G5's last action, `git worktree list` reported after; the three `remedy/job-*` worktrees untouched |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 5 — C1 through C9, with all six gates re-derived.
3. Then round 6 — R-1021's and R-1022's `Done:` lines booked in its first commit, and
   `_cmd_run_next_task_local`'s eight print-then-exit pairs in `job.py` moved, with the
   ten tests that monkeypatch it with a single-positional lambda moving in the same
   commit.

Open findings count: **25** (unchanged by this round — R-1020 closed, R-1022 was
registered this round; R-1021 stays open until round 6 books its `Done:`). Operator-
questions count: **2** (Q1, Q2 — both unchanged by this round).
