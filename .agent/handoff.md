# Handoff — F283 Machine contracts, part two: refusal sweep, JSON gap, exit-code taxonomy · Round 7 · R-1023, R-1024, and the `brain` and `patch` groups

## Session

SESSION 2 of feature F283 · round 7 · rounds so far 7

This round booked round 6's PASS and R-1022's `Done:` line, registered R-1023 and
R-1024, recorded DECISION F283 D2, repaired both findings (`decision.py`'s two
forked tokens join `no_project`/`invalid_argument`; `confirm_cost_preview` takes
`json_output` and keeps stdout the one parseable object under `--json`), and moved
the `brain` group's 13 mechanical refusal pairs and the `patch` group's 11 (of 13
mechanical, two excluded by the multi-print rule) onto `fail()`. Context
self-assessment: roughly 98% of the working budget remained at the point this
handoff was written (about 14.7M of 15M tokens).

## Range

Review of `037acc3d`..`HEAD`.

## Block self-verification (R-0954)

| reading | measured | given | equal |
|---|---|---|---|
| line count | 220 | 220 | True |
| sha256 | `f9d7d490bd38ebb0a5c863379881c643793c12c454951ae6b5d3247a13a7ce42` | `f9d7d490bd38ebb0a5c863379881c643793c12c454951ae6b5d3247a13a7ce42` | True |

Neither reading differed, so the round went ahead.

## Pre-flight

- `ls .agent/STOP`: `No such file or directory`. No STOP on disk.
- `git status --porcelain`: empty.
- `git branch --show-current`: `feature/f283-machine-contracts-part-two`.
- `git log --oneline -1`: `037acc3d`, matching the delegation message.

## Commits

### 2af97f4d F283 R7 C1: copy round 7 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r7-block.md | +220/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f283-r7-decisions.md | +28/-0 | byte-for-byte copy of decisions.md |
| .agent/authored/f283-r7-ledger.md | +8/-0 | byte-for-byte copy of ledger.md |
| .agent/authored/f283-r7-plan.md | +36/-0 | byte-for-byte copy of plan.md |

Measured insertions (`git show --numstat`): **292** (220+28+8+36).

### f53b606e F283 R7 C2: book round 6's PASS, resolve R-1022, register R-1023 and R-1024
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +28/-0 | append decisions.md: DECISION F283 D2 |
| .agent/live_review.md | +8/-0 | append ledger.md by strict byte concatenation: round-6 `Gate:` entry, `Done: R-1022`, `R-1023` and `R-1024` registrations |
| .agent/plan.md | +15/-21 | rewrite to plan.md payload, byte-identical; git's line diff shows only the lines that changed, not the whole file |

Measured insertions (`git show --numstat`): **51** (28+8+15); 21 deletions from the plan.md rewrite.

### bb5bbb4e F283 R7 C3: decision's tokens join the vocabulary the product already has
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/decision.py | +3/-3 | `job_has_no_project` → `no_project` (L179); both `invalid_reason` sites → `invalid_argument` (L352, L409) |
| tests/cli/test_decision_cmd.py | +45/-0 | `TestTheTokenVocabularyJoinsTheProduct`: an AST-read pinned SET of every token `decision.py` passes to `fail()`, naming R-1023 and DECISION F277 D8 |

Measured insertions: **48** (3+45).

### 7d2872a6 F283 R7 C4: the cost-preview gate keeps stdout for the machine under --json
| Path | +/- | Reason |
|---|---|---|
| apps/cli/cost_preview_confirm.py | +27/-8 | `confirm_cost_preview` gains `json_output: bool = False`; with it on, every human line (including the `input()` prompt) writes to stderr instead of stdout, byte-identical text; the non-terminal refusal answers `fail("confirmation_required", ..., exit_code=EXIT_USAGE)`; flag off is byte-identical to the prior behavior |
| apps/cli/commands/job.py | +1/-0 | `_cmd_job_run_cycles`'s single call site passes `json_output=json_output` |
| tests/cli/test_cost_preview_confirm.py | +33/-0 | `TestJsonOutputKeepsStdoutTheOneParseableObject`: under `json_output=True` the `--yes` path writes nothing to stdout and the line to stderr; the non-terminal path exits `EXIT_USAGE` with empty stderr and envelope `confirmation_required` |
| tests/orchestration/test_long_run_executor.py | +1/-1 | `fake_confirm`'s signature gains `json_output=False`, recording nothing new |
| tests/test_cli_main.py | +5/-4 | `test_the_run_cycles_caller_threads_json_output` now parses the WHOLE of stdout as one object (the cost-preview note moved to stderr) |

Measured insertions: **67** (27+1+33+1+5).

### 21834280 F283 R7 C5: brain refusals answer through fail()
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/brain.py | +14/-26 | all 13 mechanical print-then-exit pairs (each single-print, `Error: `-prefixed) move onto `fail()`: `job_not_found` at 11 sites, `node_not_found` (new) at the two `ValueError` sites in `_cmd_brain_node` and `_cmd_brain_continue`; each uses its own handler's `json_output` where the handler carries one, else `False` |
| tests/cli/test_job_refusal_envelope.py | +19/-0 | `TestBrainRefusalsAreAllMigrated`: no flagged, no unflagged site left in `brain.py` |
| tests/test_brain_smoke.py | +47/-10 | `TestBrainNodeUnknownNode`'s three tests that asserted the OLD stderr-prose shape repaired to the envelope shape (the migration this round makes); new `TestBrainGraphJobRecordMissing` — the required envelope test: a `--json` `brain graph` command whose job id resolves (a fresh UUID) but whose job record is missing answers `job_not_found` with empty stderr |

Measured insertions: **80** (14+19+47).

### 8e715c87 F283 R7 C6: patch refusals answer through fail()
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/patch.py | +12/-22 | 11 of 13 mechanical pairs move onto `fail()`: `job_not_found` at 6 sites, `invalid_list_option` (reused) at 1, `patch_intent_not_found` (new) at 2 (`set_approval_state`'s `ValueError`, both approve/reject), `patch_apply_blocked` (new) at 1 (`apply_patch_intent`'s "blocked" state); the two multi-print sites (`_cmd_show_patch_intent`'s intent-not-found, `_cmd_revert_patch_intent`'s revert-blocked) stay, per the rule |
| tests/cli/test_job_refusal_envelope.py | +23/-0 | `TestPatchRefusalsAreAllMigrated`: exactly one flagged site remains (the revert-blocked multi-print) and exactly one unflagged site remains (the show-intent multi-print) |
| tests/cli/test_patch_cmd.py | +17/-0 | `TestARefusalIsAnEnvelopeUnderJson`: an unknown job id on `_cmd_approve_hunks` under `json_output=True` answers `job_not_found` in the envelope with empty stderr |

Measured insertions: **52** (12+23+17).

### C7 — THE HANDBACK (this commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the 500-line cap under DECISION F104 D1 |

Self-reference exception (handback template, R-0149 pattern): a handback cannot
table the commit that writes it.

## External actions

- `git worktree add .remedy-wt/f283-r7-redproof 8e715c87 --detach` for G5 — used
  for the unmutated control and all five mutation red-proofs, then
  `git worktree remove .remedy-wt/f283-r7-redproof` — a plain remove sufficed
  because every mutation was reverted by hand back to the original text (verified
  clean with `git status --porcelain` after each revert) before the next step.
- `git push origin feature/f283-machine-contracts-part-two` after C7 — real
  outcome reported in the session reply, since it ships this very file.
- `gh pr list --state open ...` after the push — real outcome reported in the
  session reply.
- **NOTHING IS MERGED.** No `gh pr merge`, no `gh pr create`, no checkout of
  `main`, no branch deletion.
- No worktree other than the one disposable G5 worktree was added or removed.
  The three `remedy/job-*` worktrees were left alone throughout.

## Verification

### G1 — PAYLOADS transport, then four authored copies

| file | lines measured/given | bytes measured/given | sha256 equal |
|---|---|---|---|
| decisions.md | 28/28 | 2089/2089 | True |
| ledger.md | 8/8 | 7647/7647 | True |
| plan.md | 36/36 | 1616/1616 | True |

**All readings equal: True.**

Four `.agent/authored/f283-r7-*` copies (the block copy plus three payloads), each
read back from the committed tree with `git show 2af97f4d:<path>` and compared
byte-for-byte with its source:

| copy | bytes | identical to source |
|---|---|---|
| f283-r7-block.md | 14794 | True |
| f283-r7-decisions.md | 2089 | True |
| f283-r7-ledger.md | 7647 | True |
| f283-r7-plan.md | 1616 | True |

**Copies compared: 4. All True.**

### G2 — THE BOOKING

**(a) Append arithmetic**, by strict byte concatenation:

| file | pre (`037acc3d`) | payload | post | pre+payload==post |
|---|---|---|---|---|
| .agent/live_review.md | 472228 | 7647 | 479875 | True |
| .agent/decisions.md | 1791820 | 2089 | 1793909 | True |

Matches the reviewer's stated `472228 + ledger.md = 479875` and
`1791820 + decisions.md = 1793909` exactly.

**(b) Line-anchored on the committed ledger**: `^- R-1022 — ` = **1**;
`^Done: R-1022 — ` = **1**; `^- R-1023 — ` = **1**; `^- R-1024 — ` = **1**;
`^Done: R-1023 — ` = **0**; `^Done: R-1024 — ` = **0**. Open set by distinct id,
via `open_finding_ids` from `scripts/rotate_live_review.py` (imported and called
directly):

| rev | OPEN by distinct id |
|---|---|
| `037acc3d` | **24** |
| C2 (`f53b606e`) | **25** |

Added: `['R-1023', 'R-1024']`. Removed: `['R-1022']`. Matches the reviewer's
stated 24 → 25, ADDED `R-1023`/`R-1024`, REMOVED `R-1022`, exactly.

**(c) `.agent/plan.md` at C2 equals plan.md byte-for-byte**:

| file | sha256 (both sides) | equal |
|---|---|---|
| .agent/plan.md | `ae212d0a0781e0a438146e0d209b90621cc68823ed218525e3b5d20ed75bcbd8` | True |

Line count: **36**, under the AGENTS.md 50-line rule.

### G3 — THE MIGRATION, COUNTED FROM THE TREE

`git diff --name-only <parent> <commit>` and `git show --numstat` insertions, for
every commit C3 to C6 (parent → commit):

| commit | paths changed | insertions |
|---|---|---|
| C3 `f53b606e`→`bb5bbb4e` | apps/cli/commands/decision.py, tests/cli/test_decision_cmd.py | 48 |
| C4 `bb5bbb4e`→`7d2872a6` | apps/cli/commands/job.py, apps/cli/cost_preview_confirm.py, tests/cli/test_cost_preview_confirm.py, tests/orchestration/test_long_run_executor.py, tests/test_cli_main.py | 67 |
| C5 `7d2872a6`→`21834280` | apps/cli/commands/brain.py, tests/cli/test_job_refusal_envelope.py, tests/test_brain_smoke.py | 80 |
| C6 `21834280`→`8e715c87` | apps/cli/commands/patch.py, tests/cli/test_job_refusal_envelope.py, tests/cli/test_patch_cmd.py | 52 |

At C6, `python3 .remedy-wt/f283-r6-scratch/pairs.py brain.py patch.py decision.py`:

```
brain.py exits 0 mechanical 0 flagged 0 unflagged 0
patch.py exits 7 mechanical 2 flagged 1 unflagged 1
   78 _cmd_show_patch_intent True None
   252 _cmd_revert_patch_intent False json_output
   278 _cmd_revert_patch_intent True json_output
   374 _cmd_approve_hunks False json_output
   272 _cmd_revert_patch_intent False json_output
   233 _cmd_revert_patch_intent False json_output
   243 _cmd_revert_patch_intent False json_output
decision.py exits 1 mechanical 1 flagged 0 unflagged 1
   469 _cmd_decision_resolve True None
```

At `037acc3d` (before this round's migration) the same script read exactly the
reviewer's stated `brain.py exits 13 mechanical 13 flagged 6 unflagged 7` and
`patch.py exits 18 mechanical 13 flagged 7 unflagged 6` — reproduced independently
before any edit this round, confirmed identical to the block's readings. `brain.py`
fell to `exits 0 mechanical 0 flagged 0 unflagged 0` — all 13 migrated, none
excluded. `patch.py` fell to `exits 7 mechanical 2 flagged 1 unflagged 1` — 11 of
13 mechanical pairs migrated; the 2 that stayed are the multi-print sites (line 78
`_cmd_show_patch_intent`, unflagged; line 278 `_cmd_revert_patch_intent`, flagged)
the migration rule excludes, plus 5 sites (233, 243, 252, 272, 374) that were never
print-then-exit pairs to begin with (pre-branched `if json_output: ... else: ...`
shapes) — untouched, both before and after, invisible to this detector either way.
`decision.py` is unchanged by this round's tree-shape (still `exits 1 mechanical 1
flagged 0 unflagged 1` — the one derived-decision refusal C3 did not touch, only
its neighbors' token spellings changed).

`git diff --name-only 037acc3d 8e715c87 -- packages/` prints **nothing** (real
exit code 0, empty stdout) — confirmed `packages/` untouched across the whole
round.

### G4 — THE TARGETED SELECTION

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -n auto tests/cli/test_job_refusal_envelope.py tests/cli/test_decision_cmd.py tests/cli/test_decision_answers.py tests/cli/test_plan_approval.py tests/orchestration/test_proposal_decision.py tests/cli/test_mission_cmd.py tests/cli/test_cost_preview.py tests/cli/test_cost_preview_confirm.py tests/orchestration/test_long_run_executor.py tests/test_cli_main.py tests/test_brain_detail.py tests/test_brain_smoke.py tests/test_brain_viewer.py tests/test_agent_loop.py tests/test_cockpit.py tests/test_timeline.py tests/test_trust_report.py tests/test_project_constitution.py tests/test_project_brain.py tests/test_context_coverage.py tests/test_patch_intent_approval.py tests/test_patch_apply.py tests/cli/test_patch_cmd.py tests/cli/test_snapshot_cli_runtime.py tests/cli/test_cli_ux.py tests/test_grouped_cli.py tests/orchestration/test_import_reachability.py tests/cli/test_json_envelope.py tests/cli/test_golden_path.py tests/docs/; echo "REAL_EXIT=$?"'
2080 passed in 102.11s (0:01:42)
REAL_EXIT=0
```

The reviewer read `2071 passed` at `037acc3d`; this round's own count is **2080**
(higher, as required — the nine new tests: one pinned-token test in C3, two in
`TestJsonOutputKeepsStdoutTheOneParseableObject` (C4), three in C5
(`TestBrainRefusalsAreAllMigrated` ×2 + `TestBrainGraphJobRecordMissing` ×1), three
in C6 (`TestPatchRefusalsAreAllMigrated` ×2 + `TestARefusalIsAnEnvelopeUnderJson`
×1)) — zero failed, zero xfailed. `tests/test_brain_smoke.py` (C5's chosen brain
test file) and `tests/cli/test_patch_cmd.py` (C6's named test file) were already in
the block's own G4 list, so no addition was needed.

```
$ bash -c 'python3 -m ruff check apps/cli/commands/decision.py apps/cli/cost_preview_confirm.py apps/cli/commands/job.py apps/cli/commands/brain.py apps/cli/commands/patch.py tests/cli/test_decision_cmd.py tests/cli/test_cost_preview_confirm.py tests/test_cli_main.py tests/orchestration/test_long_run_executor.py tests/cli/test_job_refusal_envelope.py tests/cli/test_patch_cmd.py tests/test_brain_smoke.py; echo "REAL_EXIT=$?"'
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

Disposable worktree `.remedy-wt/f283-r7-redproof` added at `8e715c87` (C6),
detached HEAD, used for the unmutated control and all five mutations, removed
after.

**Unmutated control**:

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -n auto tests/cli/test_decision_cmd.py tests/cli/test_cost_preview_confirm.py tests/test_cli_main.py tests/orchestration/test_long_run_executor.py tests/cli/test_job_refusal_envelope.py tests/test_brain_smoke.py tests/cli/test_patch_cmd.py; echo "REAL_EXIT=$?"'
252 passed in 1.86s
REAL_EXIT=0
```

**(a) `no_project` in `decision.py` reverted to `job_has_no_project`**:

```
1 failed, 6 passed in 0.22s
REAL_EXIT=1
```

Failing: `TestTheTokenVocabularyJoinsTheProduct::test_the_fail_call_tokens_match_the_pin`
— C3's pinned-set test, exactly as the block names it. Reverted by hand;
`git status --porcelain` confirmed clean.

**(b) `confirm_cost_preview`'s `--yes` branch prints to stdout even under
`json_output`**:

```
2 failed, 57 passed in 0.48s
REAL_EXIT=1
```

Failing: `TestJsonOutputKeepsStdoutTheOneParseableObject::test_yes_under_json_writes_nothing_to_stdout_and_the_line_to_stderr`
AND `TestWorkspaceWriteDenialPreBuilder::test_the_run_cycles_caller_threads_json_output`
— C4's own test and the threading test, exactly as the block names them. Reverted;
clean.

**(c) `_cmd_job_run_cycles` stops passing `json_output` to `confirm_cost_preview`**:

```
1 failed, 134 passed in 0.82s
REAL_EXIT=1
```

Failing: `TestWorkspaceWriteDenialPreBuilder::test_the_run_cycles_caller_threads_json_output`
— a probe, not a colour, per the block's own framing: this IS a real red, the same
test (b) also reddens, because with the flag no longer threaded the cost-preview
note reverts to stdout and the caller test's stderr assertion fails. Reverted;
clean.

**(d) one migrated `fail()` in `brain.py` (`_cmd_brain`'s `job_not_found` site)
put back as its old `print(f"Error: ...", file=sys.stderr)` + `sys.exit(1)`
pair**:

```
2 failed, 94 passed in 3.06s
REAL_EXIT=1
```

Failing: `TestBrainRefusalsAreAllMigrated::test_no_flagged_print_then_exit_pair_survives`
(C5's ratchet, `found [25]`) AND
`TestBrainGraphJobRecordMissing::test_a_resolvable_id_with_no_job_record_answers_job_not_found`
(the required envelope test, since it exercises this exact site) — both exactly as
expected. Reverted; clean.

**(e) one migrated `fail()` in `patch.py` (`_cmd_list_patch_intents`'s
`job_not_found` site) put back the same way**:

```
1 failed, 69 passed in 1.49s
REAL_EXIT=1
```

Failing: `TestPatchRefusalsAreAllMigrated::test_exactly_one_flagged_site_remains`
(C6's ratchet, `found 2 at lines [279, 33]`) — exactly as the block names it.
Reverted; clean.

`git worktree remove .remedy-wt/f283-r7-redproof` (no `--force` needed: every
mutation was cleanly reverted before removal). `git worktree list` after removal:

```
/home/decodeux/Repos/remedy                                  8e715c87 [feature/f283-machine-contracts-part-two]
/home/decodeux/Repos/remedy/.remedy-wt/job-468c8e62a2cc4fac  1b9ae606 [remedy/job-468c8e62a2cc4fac]
/home/decodeux/Repos/remedy/.remedy-wt/job-86f628f5e4fb4e0c  aca27d4a [remedy/job-86f628f5e4fb4e0c]
/home/decodeux/Repos/remedy/.remedy-wt/job-c1dba9c3d7874968  fd23710f [remedy/job-c1dba9c3d7874968]
```

Only the primary checkout and the three `remedy/job-*` worktrees remain.

### G6 — TREE AND PUSH

Reported in full in the worker's session reply once this commit exists (push
carries this file). At write time: `git status --porcelain` empty; `git log
--oneline -n 9` will show C7 through round 6's tail once committed; `git worktree
list` shows the primary checkout and the three `remedy/job-*` worktrees and
nothing else. Push outcome and `gh pr list` reported in the session reply.

### Token list — every `fail()` token this round's commits (C3–C6) use, its line, new or reused

| commit | line | token | new/reused | search behind a `new` one |
|---|---|---|---|---|
| C3 | 179 | no_project | reused (job.py, mission_cmd.py) | — |
| C3 | 352 | invalid_argument | reused (job.py, mission_cmd.py) | — |
| C3 | 409 | invalid_argument | reused (second site, same commit) | — |
| C4 | 79 | confirmation_required | new | `grep -rn "confirmation_required" apps/cli/` → 0 hits before this commit |
| C5 | 24 | job_not_found | reused (18 sites repo-wide before this round) | — |
| C5 | 66 | job_not_found | reused | — |
| C5 | 91 | node_not_found | new | full `fail("` token search over `apps/cli/**/*.py` → 0 hits before this commit |
| C5 | 111 | job_not_found | reused | — |
| C5 | 159 | job_not_found | reused | — |
| C5 | 267 | job_not_found | reused | — |
| C5 | 316 | job_not_found | reused | — |
| C5 | 336 | job_not_found | reused | — |
| C5 | 352 | job_not_found | reused | — |
| C5 | 372 | job_not_found | reused | — |
| C5 | 402 | job_not_found | reused | — |
| C5 | 425 | node_not_found | new (second site, same commit) | same search as L91 |
| C5 | 444 | job_not_found | reused | — |
| C6 | 32 | job_not_found | reused | — |
| C6 | 50 | invalid_list_option | reused (8 sites repo-wide before this round, e.g. blocker.py) | — |
| C6 | 66 | job_not_found | reused | — |
| C6 | 94 | job_not_found | reused | — |
| C6 | 102 | patch_intent_not_found | new | full `fail("` token search over `apps/cli/**/*.py` → 0 hits before this commit; both `set_approval_state` call sites' only reachable `ValueError` is "Patch intent ... not found", the "invalid approval state" branch being unreachable from a literal `"approved"`/`"rejected"` argument |
| C6 | 121 | job_not_found | reused | — |
| C6 | 129 | patch_intent_not_found | new (second site, same commit) | same search/reasoning as L102 |
| C6 | 148 | job_not_found | reused | — |
| C6 | 158 | patch_apply_blocked | new | full `fail("` token search over `apps/cli/**/*.py` → 0 hits before this commit; named for `result.state == "blocked"` (the boundary function's own state name) rather than for one of its 14 distinguishable-but-dynamic `blocked_reason` strings, matching the D9 precedent (`mission_error`, `builder_error`) for a boundary whose many prose reasons are not modeled as a token hierarchy at the CLI layer — the specific reason stays in `message` |
| C6 | 190 | job_not_found | reused | — |
| C6 | 320 | job_not_found | reused | — |

The full-repo search this round's rule required (run once, before any token was
used, and independently re-verified in a disposable worktree at `037acc3d` while
writing this handback — added and removed outside G5, not counted against it):
an AST-based `fail("..."` token scan over every `.py` under `apps/cli/`, matched
127 `fail()` call sites across 62 distinct tokens at `037acc3d`, confirming
`no_project` (job.py, mission_cmd.py) and `invalid_argument` (job.py,
mission_cmd.py) as existing spellings before C3 touched `decision.py`, and
confirming `confirmation_required`, `node_not_found`, `patch_intent_not_found`,
and `patch_apply_blocked` all ABSENT before this round's commits minted them.
Re-run after C6 (`.remedy-wt/f283-r7-scratch/tokens_search.py`) confirms each new
token appears ONLY at the lines this table lists — no second fork was created.

### The round's whole tracked path set (before this commit)

`git diff --name-only 037acc3d 8e715c87` — **19** paths; plus `.agent/handoff.md`
from this commit makes **20** — set-equal to constraint 3's enumeration (four
authored copies + live_review.md + decisions.md + plan.md + handoff.md +
decision.py + cost_preview_confirm.py + job.py + brain.py + patch.py + the six
named test files + the one brain test file C5 names):

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f283-r7-block.md | C1 `2af97f4d` |
| 2 | .agent/authored/f283-r7-decisions.md | C1 `2af97f4d` |
| 3 | .agent/authored/f283-r7-ledger.md | C1 `2af97f4d` |
| 4 | .agent/authored/f283-r7-plan.md | C1 `2af97f4d` |
| 5 | .agent/decisions.md | C2 `f53b606e` |
| 6 | .agent/live_review.md | C2 `f53b606e` |
| 7 | .agent/plan.md | C2 `f53b606e` |
| 8 | apps/cli/commands/decision.py | C3 `bb5bbb4e` |
| 9 | tests/cli/test_decision_cmd.py | C3 `bb5bbb4e` |
| 10 | apps/cli/commands/job.py | C4 `7d2872a6` |
| 11 | apps/cli/cost_preview_confirm.py | C4 `7d2872a6` |
| 12 | tests/cli/test_cost_preview_confirm.py | C4 `7d2872a6` |
| 13 | tests/orchestration/test_long_run_executor.py | C4 `7d2872a6` |
| 14 | tests/test_cli_main.py | C4 `7d2872a6` |
| 15 | apps/cli/commands/brain.py | C5 `21834280` |
| 16 | tests/cli/test_job_refusal_envelope.py | C5 (first touch) |
| 17 | tests/test_brain_smoke.py | C5 `21834280` |
| 18 | apps/cli/commands/patch.py | C6 `8e715c87` |
| 19 | tests/cli/test_patch_cmd.py | C6 `8e715c87` |

Plus `.agent/handoff.md` from this commit makes **20** — set-equal to constraint
3's enumeration. `.agent/candidates.md`, `.agent/context.md`,
`.agent/operator_questions.md`, `.agent/prose_slips.md`, `README.md`,
`docs/roadmap/**`, and `apps/cli/json_envelope.py` appear **0** times. `packages/`
appears **0** times (confirmed above under G3).

## Authored-text proofs

- The four copies at C1, compared with the reviewer's originals under
  `.remedy-wt/f283-r7-payloads/` and `.remedy-wt/f283-r7-block.md`: **four
  readings, all True** (G1).
- The one REWRITE payload against its committed file: `.agent/plan.md` is
  sha256-equal to its payload (G2c).
- The two APPEND payloads against their committed files: strict byte
  concatenation True for `.agent/live_review.md` (ledger.md) and
  `.agent/decisions.md` (decisions.md), byte numbers equal to the reviewer's
  (G2a).
- No payload was edited or retyped. All four `.agent/authored/` copies and the
  one product-file rewrite were made with `shutil.copyfile`; the two appends by
  reading each payload's bytes and writing base+payload back to disk.
- Every change under `apps/` and `tests/` this round was WORKER-authored to the
  block's SPEC — there is no reviewer-authored diff to compare against for those
  files; the block's SPEC prose is the standard they were written to, and
  G3/G4/G5 above are the proof they meet it.

## Deviations & assumptions

1. **The bundle ran C1 through C6 — six commits, exactly as ordered — before
   this handback commit C7.** Nothing was added, dropped or reordered.
2. **No expected insertion figure is given for C2's rewrite or for any C3–C6
   code commit, per the block's own convention**: only measured figures are
   reported above, and none of them was forced to match a prediction.
3. **The two `patch.py` `ValueError` sites (from `set_approval_state`) migrated as
   `patch_intent_not_found` rather than a `<layer>_error` catch-all**, because —
   unlike D9's `MissionError`
   case — `set_approval_state`'s OTHER `ValueError` branch ("invalid approval
   state") is unreachable from either call site (both pass a literal `"approved"`
   or `"rejected"`, always a valid state), so the condition these two sites can
   actually raise is single and nameable, not genuinely ambiguous prose.
4. **`patch_apply_blocked` was minted as a single catch-all for
   `_cmd_apply_patch_intent`'s "blocked" branch**, rather than as 14 distinct
   tokens mirroring `apply_patch_intent`'s internal `blocked_reason` values
   (`repo_missing`, `unsafe_path`, `not_approved:<state>`, …), because those
   reasons are dynamic strings (some carry embedded values via an f-string), not
   a fixed vocabulary, and minting 14 tokens for one CLI call site is scope this
   round's SPEC does not order; the DECISION F277 D9 precedent (name for the
   layer/outcome, keep the specific reason in `message`) is the closer fit.
   `result.blocked_reason` is passed as `message` unchanged, so no information is
   lost — a future round can still split this by reason if a consumer needs to.
5. **Two `patch.py` sites the migration rule structurally cannot see were left
   alone without further comment beyond G3's note**: `_cmd_revert_patch_intent`'s
   three `if json_output: ... else: print(...); sys.exit(1)` branches (ambiguous
   intent id, no apply record, no target repo) and `_cmd_approve_hunks`'s
   `HunkApprovalRefusal` if/else — none of these is a `print(...)` IMMEDIATELY
   preceding `sys.exit`, so `_refusal_sites`/`pairs.py` never counted them as
   pairs either before or after this round; they are not migrations the rule
   excluded, they are outside its pattern entirely.
6. **G5's mutations (d) and (e) each targeted one arbitrarily chosen
   `job_not_found` site** (`_cmd_brain`'s in brain.py, `_cmd_list_patch_intents`'s
   in patch.py) rather than a site the block names by line, since the block's own
   SPEC says only "one migrated `fail()`" without naming which; any of the
   migrated sites would have red-proofed the same ratchet identically.
7. **No trailing commit for the C7 push or `gh pr list`; both go in the session
   reply**, consistent with DECISION amend0827 D2 and prior rounds' own
   precedent: the push carries this very file, so its outcome cannot be known
   before the commit exists.
8. **One disposable worktree (`.remedy-wt/f283-r7-redproof`) was reused for the
   unmutated control and all five G5 mutations sequentially**, each reverted by
   hand and confirmed clean via `git status --porcelain` before the next
   mutation.
9. **Constraints 1, 3 and 4 held throughout.** No payload was edited or
   retyped; only the twenty paths named in the block's enumeration were touched
   (verified by set-equality above, C7 included); `packages/` was never
   touched; the rule reached exactly `brain.py`'s 13 mechanical pairs (all
   migrated) and `patch.py`'s 13 mechanical pairs (11 migrated, 2 excluded by
   the multi-print clause); every commit left the targeted G4 selection green
   (re-run in full at C6, above) — no migration broke a test outside the same
   commit that fixed it.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Pre-flight (STOP, git state, block self-verify) | done | no STOP; tree clean at `037acc3d`; block 220 lines / matching sha256 |
| C1 copy block + 3 payloads | done | 292 insertions |
| C2 book round 6 PASS, resolve R-1022, register R-1023/R-1024 | done | 51 insertions (28+8+15, 21 deletions from plan rewrite); open set 24→25, added R-1023/R-1024, removed R-1022 |
| C3 decision.py's two forked tokens join the vocabulary | done | 48 insertions; 2 paths; pinned-token test added |
| C4 cost-preview gate takes json_output | done | 67 insertions; 5 paths; DECISION F283 D2 |
| C5 brain group migrates | done | 80 insertions; 3 paths; 13/13 mechanical pairs migrated, 2 new tokens |
| C6 patch group migrates | done | 52 insertions; 3 paths; 11/13 mechanical pairs migrated (2 excluded, multi-print), 2 new tokens |
| C7 the handback | done | this commit |
| G1 payload transport + authored copies | done | 3/3 payload readings equal; 4/4 authored copies byte-identical |
| G2(a) live_review.md + decisions.md append | done | 472228+7647=479875; 1791820+2089=1793909 |
| G2(b) R-1022/R-1023/R-1024 pairing + open set by distinct id | done | 1 R-1022 reg / 1 Done / 1 R-1023 reg / 1 R-1024 reg / 0 Done for either new one; 24→25, added R-1023/R-1024, removed R-1022 |
| G2(c) plan.md rewrite | done | sha256-equal to payload; 36 lines, under 50 |
| G3 migration counted from the tree | done | per-commit diffs and insertions all reported; `pairs.py` reproduced the reviewer's `037acc3d` baseline exactly before editing, brain.py/patch.py both driven to their post-migration shape; 0 paths under `packages/` |
| G4 targeted selection, ruff, integrity | done | 2080 passed/0 failed/0 xfailed (up from 2071); ruff exit 0; integrity all 5 pass, fail_count 0 |
| G5 red-proofs (a)(b)(c)(d)(e) | done | all five go RED at exactly the test(s) named or predicted; (c) reported as a probe per the block's framing; unmutated control 252 passed |
| G6 tree, push, PR list | pending at write time | reported in the worker's session reply with real exit codes |
| Constraint 1 no payload edited/retyped | done | `shutil.copyfile`, byte concatenation only |
| Constraint 2 every commit under 500 insertions | done | 292, 51, 48, 67, 80, 52; this handoff exempt as single `.agent/**` state file |
| Constraint 3 no unnamed file touched | done | 20 paths after this commit, set-equal to the enumeration |
| Constraint 4 migrate only what the rule reaches | done | `packages/` untouched; `patch.py`'s two multi-print sites and five pre-branched sites stayed, `decision.py`'s one derived-decision refusal untouched |
| Constraint 5 targeted selection green every commit | done | re-run in full at C6, above; no migration broke a test outside its own commit |
| Constraint 6 STOP if a gate goes red outside constraint 3's path set | done (n/a) | no gate went red for a reason outside the named paths; no STOP was needed |
| Constraint 7 nothing is merged | done | no `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch deletion |
| Constraint 8 G5 worktree under .remedy-wt/, removed, listed | done | `.remedy-wt/f283-r7-redproof`, removed as G5's last action, `git worktree list` reported after; the three `remedy/job-*` worktrees untouched |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 7 — C1 through C7, with all six gates re-derived.
3. Then round 8 — R-1023's and R-1024's `Done:` lines booked in its first commit,
   and the non-mechanical `job.py` sites: the verification-failure loop, the
   single-pass `job run --json` success line (which is prose), and
   `_cmd_resume`'s two hand-rolled objects.

Open findings count: **25** (unchanged in NET terms by this round's own repairs —
R-1022 closed this round; R-1023 and R-1024 opened this round and stay open until
round 8 books their `Done:` lines). Operator-questions count: **2** (Q1, Q2 — both
unchanged by this round).
