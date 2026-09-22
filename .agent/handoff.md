# Handoff — F283 Machine contracts, part two: refusal sweep, JSON gap, exit-code taxonomy · Round 15 · T001's catalog half, second group (D9)

## Session

SESSION 4 of feature F283 · round 15 · rounds so far 15

This round booked round 14's PASS and a prose slip, then pinned the two
properties round 14's review found unpinned (`blocker resolve`'s full id in
the envelope; `patch show`'s two-line text refusal). Then, in the order D9's
groups land: `decision resolve` and `decision explain` declared
`supports_json` (`decision resolve` answers one envelope per success family —
`sr:` resolved, `td:` answered, `plan:` approved/rejected, `proposal:`
approved/rejected/deferred — and its derived-decision refusal moved onto
`fail("decision_not_resolvable", ...)` under `--json` while keeping its text
byte-for-byte; `decision explain` answers `emit_ok(job_id=..., text=...)`).
Then `job plan` declared `supports_json` and answers `emit_ok(job_id=...,
changed=..., model=..., task_count=..., log_path=..., elapsed_ms=...)` when it
changed the plan. Then the seven `brain` report and viewer commands (`view`,
`trust`, `timeline`, `cockpit`, `constitution`, `open`, `export-viewer`)
declared `supports_json`, threading the flag through the shared
`_prepare_viewer` helper too. The ratchet shrank from twenty to exactly the
ten `ui` and `project` commands. One unordered commit was needed this round
(reported under Deviations): self-review after C6 found a test that invoked
the real platform opener with no mock, a live side effect worth fixing before
push.
Context self-assessment: roughly 45% of the working budget remained at the
point this handoff was written.

## Range

Review of `dfce6076`..`HEAD`.

## Block self-verification (R-0954)

| reading | measured | given | equal |
|---|---|---|---|
| line count | 232 | 232 | True |
| sha256 | `931a381b02a3eb0795d817aa9356f294a4ea8a72ae2efd7561ca533aa1294951` | `931a381b02a3eb0795d817aa9356f294a4ea8a72ae2efd7561ca533aa1294951` | True |

Neither reading differed, so the round went ahead.

## Pre-flight

- `ls .agent/STOP`: `No such file or directory`. No STOP on disk.
- `git status --porcelain`: empty.
- `git branch --show-current`: `feature/f283-machine-contracts-part-two`.
- `git log --oneline -1`: `dfce6076`, matching the delegation message.

## Commits

### 7f089cb4 F283 R15 C1: copy round 15 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r15-block.md | +232/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f283-r15-ledger.md | +2/-0 | byte-for-byte copy of ledger.md |
| .agent/authored/f283-r15-plan.md | +35/-0 | byte-for-byte copy of plan.md |
| .agent/authored/f283-r15-slips.md | +1/-0 | byte-for-byte copy of slips.md |

Measured insertions (`git show --numstat`): **270** (232+2+35+1).

### 7c5047cd F283 R15 C2: book round 14's PASS and a prose slip
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | append ledger.md by strict byte concatenation: round-14 `Gate:` entry |
| .agent/plan.md | +9/-11 | rewrite to plan.md payload, byte-identical; git's line diff shows only the lines that changed |
| .agent/prose_slips.md | +1/-0 | append slips.md: one dated prose-slip line |

Measured insertions: **12** (2+9+1); 11 deletions from the plan.md rewrite.

### c5ce1789 F283 R15 C3: pin blocker resolve's full id and patch show's text refusal
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_blocker_cmd.py | +19/-0 | new `test_resolve_answers_the_full_id_not_the_text_branchs_short_one`: a stop id longer than eight characters, asserting the envelope's `id` is the FULL id, not the text branch's `[:8]` truncation |
| tests/cli/test_patch_cmd.py | +25/-0 | new `test_show_refusal_without_json_is_the_two_old_stderr_lines`: `patch show` without `--json` on a missing intent writes exactly the two old stderr lines, byte-for-byte, and exits 1 |

Measured insertions: **44** (19+25); 0 deletions. Both properties were already
correct on disk (round 14 left them unpinned, not wrong); this commit spends
no code change, only tests.

### 9748191f F283 R15 C4: decision resolve and decision explain answer --json in the envelope
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | +4/-1 | `decision.resolve` and `decision.explain` gain `_JSON_OPT` and `supports_json=True` |
| apps/cli/commands/decision.py | +127/-63 | `_cmd_decision_resolve` and `_cmd_decision_explain` take `json_output`, threaded to every refusal they reach (`_load_job_events` already had the parameter); `_create_mission_for_job` takes `json_output`, prints its three lines only in text mode, and returns the mission's id to its caller; `decision explain --json` answers `emit_ok(job_id=..., text=<explanation>)`; `decision resolve --json` answers one envelope per success family (`sr:` → `resolved`/`stop_id`/`reason_code`; `td:` → `answered`/`answer`/`cross_references`/`follow_up_mission`/`next_command`; `plan:` approve → `approved`/`answers`/`assumption_log`/`mission_id`; `plan:` reject → `rejected`/`next_step`; `proposal:` → `approved`/`rejected`/`deferred` with `task_id`); the derived-decision refusal at the end reshapes onto `if json_output: fail("decision_not_resolvable", <two lines joined by \n>, json_output=True) else: <the two old prints>` followed by one shared `sys.exit(1)`, so no print-then-exit pair survives; text branches unchanged |
| tests/cli/test_decision_answers.py | +36/-0 | new `TestDecisionResolveTaskAnswerAnswersJSONThroughTheDispatcher`: the `td:` (`answered`) family's envelope through the CLI dispatcher, asserting `answer`, `cross_references`, `follow_up_mission` (null) and `next_command` |
| tests/cli/test_decision_cmd.py | +111/-0 | `_PINNED_TOKENS` gains `decision_not_resolvable`; new `TestDecisionExplainAndResolveAnswerJSONThroughTheDispatcher` (`explain` success, `sr:` resolved success, `decision_not_found` refusal, `decision_not_resolvable` refusal) and `TestDecisionResolveProposalAnswersJSONThroughTheDispatcher` (the `proposal:` reject outcome, over a real proposed-task store) |
| tests/cli/test_job_refusal_envelope.py | +9/-7 | `TestDecisionsRefusalsAreAllMigrated.test_exactly_one_unflagged_site_remains` now asserts `unflagged == []` — the derived-decision pair's shared `sys.exit(1)` no longer sits directly after a stderr print in the same body, so the ratchet's AST rule counts no site at all; class docstring corrected |
| tests/cli/test_plan_approval.py | +43/-0 | new `TestDecisionResolvePlanAnswersJSONThroughTheDispatcher`: the `plan:` approve and reject outcomes' envelopes through the CLI dispatcher |
| tests/test_command_catalog.py | +7/-8 | ratchet constant loses `decision.resolve` and `decision.explain` (20→18); docstring updated |

Measured insertions: **337** (4+127+36+111+9+43+7); 79 deletions.

### 768c97fe F283 R15 C5: job plan answers --json in the envelope
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | +2/-1 | `job.plan` gains `_JSON_OPT` and `supports_json=True` |
| apps/cli/commands/job.py | +25/-13 | `_cmd_plan_job_local` takes `json_output`, threaded to every refusal it reaches (`planner_capability_missing`, `planner_output_invalid`, `missing_dependency`, `planner_failed`, plus the pass-through `job_not_found`); success answers `emit_ok(job_id=..., changed=<bool>, model=..., task_count=..., log_path=...)`, plus `elapsed_ms` when the plan changed; text branches unchanged |
| tests/orchestration/test_structured_planner_cli.py | +36/-0 | new `TestPlanJobAnswersJSONThroughTheDispatcher`: a success envelope (asserting all six keys) and a `planner_failed` refusal envelope, both through the CLI dispatcher |
| tests/test_command_catalog.py | +4/-5 | ratchet constant loses `job.plan` (18→17); docstring updated |

Measured insertions: **67** (2+25+36+4); 19 deletions.

### 39e0c1e3 F283 R15 C6: the brain report and viewer commands answer --json in the envelope
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | +14/-6 | `brain.view`, `brain.trust`, `brain.timeline`, `brain.cockpit`, `brain.constitution`, `brain.open`, `brain.export-viewer` each gain `_JSON_OPT` and `supports_json=True` |
| apps/cli/commands/brain.py | +84/-40 | each of the seven handlers and the shared `_prepare_viewer` take `json_output`, threaded to every refusal; success under `--json`: `view` → `job_id`/`index_path`/`node_count`/`edge_count`/`detail_count`; `trust`/`cockpit`/`constitution` → `job_id`/`text`; `timeline` → `job_id`/`event_count`/`text` (its no-events line when there are none); `open` → `job_id`/`index_path`/`opened` (the opener still runs); `export-viewer` → `job_id`/`out_dir`/`files`; text branches and stderr warnings unchanged |
| tests/test_brain_viewer.py | +139/-0 | new `TestBrainCommandsAnswerJSONThroughTheDispatcher`: one success envelope per command (asserting its keys; `timeline` with no events among them) and one `job_not_found` refusal, through the real CLI (`apps.cli.main.main`) |
| tests/test_command_catalog.py | +6/-13 | ratchet constant loses the seven `brain.*` ids (17→10), now exactly the ten `ui` and `project` commands; docstring updated |

Measured insertions: **243** (14+84+139+6); 59 deletions.

### 1660703c F283 R15 C6-fix: mock the opener in brain open's --json test (unordered — see Deviations)
| Path | +/- | Reason |
|---|---|---|
| tests/test_brain_viewer.py | +10/-2 | `test_open_answers_the_envelope` patches `subprocess.Popen` so the real platform opener (`xdg-open` on this machine) is never actually launched; self-review after C6 caught it running live during a local test pass |

Measured insertions: **10**; 2 deletions.

### C7 — THE HANDBACK (this commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the 500-line cap under DECISION F104 D1 |

Self-reference exception (handback template, R-0149 pattern): a handback cannot
table the commit that writes it.

## External actions

- `git worktree add .remedy-wt/f283-r15-redproof 39e0c1e3` for a first G5 pass —
  removed with `git worktree remove --force` once the C6-fix commit was made,
  since that fix changed the very file the red-proofs run against.
- `git worktree add .remedy-wt/f283-r15-redproof 1660703c` for the final G5
  pass — used for the unmutated control and all six mutation red-proofs, each
  reverted with `git checkout --` before the next — then `git worktree remove
  --force .remedy-wt/f283-r15-redproof`.
- `git push origin feature/f283-machine-contracts-part-two` after C7 — real
  outcome reported in the session reply, since it ships this very file.
- `gh pr list --state open ...` after the push — real outcome reported in the
  session reply.
- **NOTHING IS MERGED.** No `gh pr merge`, no `gh pr create`, no checkout of
  `main`, no branch deletion.
- No worktree other than the two (sequential, not concurrent) disposable G5
  worktrees above was added; both removed. No `remedy/job-*` worktree existed
  this round (`git worktree list` shows the primary checkout alone both
  before C1 and again here before C7).

## Verification

### G1 — PAYLOADS transport, then four authored copies

| file | lines measured/given | bytes measured/given | sha256 equal |
|---|---|---|---|
| ledger.md | 2/2 | 3399/3399 | True |
| plan.md | 35/35 | 1537/1537 | True |
| slips.md | 1/1 | 657/657 | True |

**All readings equal: True.**

Four `.agent/authored/f283-r15-*` copies (the block copy plus three payloads),
each read back from the committed tree with `git show 7f089cb4:<path>` and
compared byte-for-byte with its source:

| copy | equal to source |
|---|---|
| f283-r15-block.md | True |
| f283-r15-ledger.md | True |
| f283-r15-plan.md | True |
| f283-r15-slips.md | True |

**Copies compared: 4. All True.**

### G2 — THE BOOKING

**(a) Append arithmetic**, by strict byte concatenation, pre-file read at
`dfce6076`:

| file | pre | payload | post | pre+payload==post |
|---|---|---|---|---|
| .agent/live_review.md | 517382 | 3399 | 520781 | True |
| .agent/prose_slips.md | 361828 | 657 | 362485 | True |

Matches the block's stated compositions (517382+ledger.md=520781,
361828+slips.md=362485) exactly.

**(b) Line-anchored on the committed ledger**: `^Gate: F283 R14 — ` = **1**.
Open set by distinct id, via `open_finding_ids` from
`scripts/rotate_live_review.py` (imported and called directly):

| rev | OPEN by distinct id |
|---|---|
| `dfce6076` | **24** |
| C2 (`7c5047cd`) | **24** |

Added: `[]`. Removed: `[]`. Matches the block's stated 24 → 24, ADDED empty,
REMOVED empty, exactly.

**(c) `.agent/plan.md` at C2 equals plan.md byte-for-byte**: sha256-equal to
the payload (`5c68196e44ad2359a590f140a05d23aac0de69cae40715e9a7f9723193b8d1e5`
both). Line count: **35**, under the AGENTS.md 50-line rule.

### G3 — THE CHANGE, COUNTED FROM THE TREE

`git diff --name-only <parent> <commit>` and `git show --numstat` insertions:

| commit | paths changed | insertions |
|---|---|---|
| C4 `c5ce1789`→`9748191f` | apps/cli/command_catalog.py, apps/cli/commands/decision.py, tests/cli/test_decision_answers.py, tests/cli/test_decision_cmd.py, tests/cli/test_job_refusal_envelope.py, tests/cli/test_plan_approval.py, tests/test_command_catalog.py | 337 |
| C5 `9748191f`→`768c97fe` | apps/cli/command_catalog.py, apps/cli/commands/job.py, tests/orchestration/test_structured_planner_cli.py, tests/test_command_catalog.py | 67 |
| C6 `768c97fe`→`39e0c1e3` | apps/cli/command_catalog.py, apps/cli/commands/brain.py, tests/test_brain_viewer.py, tests/test_command_catalog.py | 243 |

The derived set (D9's rule — neither `may_mutate_repo` nor `may_execute_commands`
nor `supports_json`, computed by importing `CATALOG` fresh after each commit
in the primary checkout, taken right after that commit landed):

| commit | derived set size |
|---|---|
| C4 `9748191f` | **18** |
| C5 `768c97fe` | **17** |
| C6 `39e0c1e3` | **10**, exactly the five `ui` and five `project` commands (confirmed by direct set comparison: `project.adopt`, `project.attach`, `project.attach-job`, `project.attach-repo`, `project.create`, `ui.latest`, `ui.open`, `ui.start`, `ui.status`, `ui.stop`) |

`python3 .remedy-wt/f283-r6-scratch/pairs.py decision.py brain.py job.py` at
`39e0c1e3` (C6):

| module | summary |
|---|---|
| decision.py | `exits 1 mechanical 0 flagged 0 unflagged 0` |
| brain.py | `exits 0 mechanical 0 flagged 0 unflagged 0` |
| job.py | `exits 2 mechanical 0 flagged 0 unflagged 0` |

Against the block's `dfce6076` reading (`decision.py exits 1 mechanical 1
flagged 0 unflagged 1`, `brain.py exits 0 mechanical 0 flagged 0 unflagged 0`,
`job.py exits 2 mechanical 0 flagged 0 unflagged 0`): `decision.py`'s one
`sys.exit(1)` is unchanged in COUNT but no longer "mechanical" — it now sits
after an `if`/`else` compound rather than directly after a stderr print, so
the AST rule stops counting it as a print-then-exit pair at all (mechanical
1→0, unflagged 1→0); `brain.py` and `job.py` are byte-for-byte unchanged in
this reading, since neither module's raw `sys.exit` sites (both in `job.py`,
none in `brain.py`) were touched this round.

`git diff --name-only dfce6076 39e0c1e3 -- packages/` prints **nothing** (real
exit code 0, empty stdout) — confirmed `packages/` untouched across the whole
round.

### Token list — every token this round's `fail(`/`emit_error(` calls introduce or reuse

Computed by diffing each touched module's AST between `dfce6076` and `39e0c1e3`
and keeping only `fail()`/`emit_error()` calls whose line range overlaps a
changed line (so untouched refusal sites in the same file — e.g.
`decision.py`'s `invalid_list_option`, only in the untouched `_cmd_decision_list`
— are excluded). Each token's `git grep -c '"<token>"' dfce6076 -- apps/cli/`
count (summed across files) at the round's base:

| token | touched in | count at `dfce6076` | new or reused |
|---|---|---|---|
| answer_parse_error | decision.py | 1 | reused |
| clarifications_already_resolved | decision.py | 1 | reused |
| decision_already_answered | decision.py | 1 | reused |
| decision_not_found | decision.py | 2 | reused |
| decision_not_resolvable | decision.py | 0 | **new** |
| follow_up_mission_error | decision.py | 1 | reused |
| invalid_argument | decision.py | 19 | reused |
| job_not_found | decision.py, job.py, brain.py | 44 | reused |
| missing_argument | decision.py | 6 | reused |
| missing_dependency | job.py | 3 | reused |
| mission_already_linked | decision.py | 1 | reused |
| mission_error | decision.py | 6 | reused |
| no_pending_plan_approval | decision.py | 1 | reused |
| no_project | decision.py | 6 | reused |
| option_not_applicable | decision.py | 5 | reused |
| planner_capability_missing | job.py | 1 | reused |
| planner_failed | job.py | 1 | reused |
| planner_output_invalid | job.py | 1 | reused |
| proposed_task_invalid_state | decision.py | 3 | reused |
| proposed_task_not_found | decision.py | 1 | reused |
| proposed_task_operation_failed | decision.py | 4 | reused |
| stop_reason_not_found | decision.py | 1 | reused |

Exactly one token this round's `fail()`/`emit_error()` calls introduce is new
at `apps/cli/` level: `decision_not_resolvable` (0 hits at `dfce6076`). Every
other token touched by the diff already existed in `apps/cli/` before this
round (`decision.py`'s guard clauses, `job.py`'s plan-refusal branches and
`brain.py`'s shared `job_not_found` refusal all reuse pre-existing tokens).

### G4 — TARGETED SELECTION, ruff, integrity

`.remedy-wt/f283-r15-scratch/selection.txt`: **197** space-separated paths
(`-n auto`). The block's `dfce6076` reading: `8452 passed, 10 skipped`, exit 0.

| when | exit code | summary |
|---|---|---|
| after C3 | 0 | 8454 passed, 10 skipped |
| after C4 | 0 | 8462 passed, 10 skipped |
| after C5 | 0 | 8464 passed, 10 skipped |
| after C6 | 0 | 8472 passed, 10 skipped |
| after C6-fix (extra, since it touched a C6 test file) | 0 | 8472 passed, 10 skipped |

Zero failed, zero errors at each; the passed count only rose (+2 at C3, +8 at
C4, +2 at C5, +8 at C6, unchanged at C6-fix — it edits an existing test rather
than adding one; skipped unchanged at 10 throughout).

`python3 -m ruff check` over every `.py` path the round touched
(`apps/cli/command_catalog.py`, `apps/cli/commands/brain.py`,
`apps/cli/commands/decision.py`, `apps/cli/commands/job.py`,
`tests/cli/test_blocker_cmd.py`, `tests/cli/test_decision_answers.py`,
`tests/cli/test_decision_cmd.py`, `tests/cli/test_job_refusal_envelope.py`,
`tests/cli/test_patch_cmd.py`, `tests/cli/test_plan_approval.py`,
`tests/orchestration/test_structured_planner_cli.py`,
`tests/test_brain_viewer.py`, `tests/test_command_catalog.py`), run after
C6-fix: **All checks passed!**

`python3 -m apps.cli.main integrity check --json`, run after C6-fix: `"passed":
true, "fail_count": 0`, all five checks (`handler_import`,
`live_review_verdict`, `plan_consistency`, `relevant_untracked`,
`high_blockers_open`) read `"status": "pass"`.

`python3 -m pytest tests/cli/test_golden_path.py -q`, run once after C6:
**42 passed**, exit 0.

### G5 — RED-PROOFS

Final disposable worktree `.remedy-wt/f283-r15-redproof` at `1660703c`
(C6-fix), never committed. Ran `tests/cli/test_blocker_cmd.py`,
`tests/cli/test_patch_cmd.py`, `tests/cli/test_decision_cmd.py`,
`tests/cli/test_decision_answers.py`, `tests/cli/test_plan_approval.py`,
`tests/orchestration/test_structured_planner_cli.py` and
`tests/test_brain_viewer.py` UNMUTATED first, then each mutation alone,
reverted with `git checkout --` before the next:

| step | exit code | result | failing tests |
|---|---|---|---|
| unmutated control | 0 | 233 passed | — |
| (a) `blocker resolve`'s envelope carries `sr.id[:8]` as `id` | 1 | 1 failed, 9 passed (file-scoped) | `TestBlockerResolveAnswersJSONThroughTheDispatcher::test_resolve_answers_the_full_id_not_the_text_branchs_short_one` |
| (b) `patch show`'s not-found message joins its two lines with a space | 1 | 1 failed, 19 passed (file-scoped) | `TestShowApproveRejectAnswerJSONThroughTheDispatcher::test_show_refusal_without_json_is_the_two_old_stderr_lines` |
| (c) the derived-decision refusal passes `json_output=False` under `--json` | 1 | 1 failed, 72 passed (3-file-scoped) | `TestDecisionExplainAndResolveAnswerJSONThroughTheDispatcher::test_resolve_a_derived_decision_is_not_resolvable_in_the_envelope` |
| (d) the `plan:` approve branch prints its text even under `--json` | 1 | 1 failed, 72 passed (3-file-scoped) | `TestDecisionResolvePlanAnswersJSONThroughTheDispatcher::test_approve_answers_the_envelope` |
| (e) `job plan`'s `planner_failed` refusal passes `json_output=False` | 1 | 1 failed, 18 passed (file-scoped) | `TestPlanJobAnswersJSONThroughTheDispatcher::test_planner_failure_is_the_envelope_through_the_dispatcher` |
| (f) `brain timeline`'s no-events branch prints its line even under `--json` | 1 | 1 failed, 110 passed (file-scoped) | `TestBrainCommandsAnswerJSONThroughTheDispatcher::test_timeline_with_no_events_answers_the_envelope` |

Each mutation reddened exactly its named target and nothing else. Each was
reverted with `git checkout --` and confirmed clean (`git status --porcelain`,
empty) before the next. `git worktree remove --force
.remedy-wt/f283-r15-redproof` afterward. `git worktree list` (post-removal):
the primary checkout alone —
`/home/decodeux/Repos/remedy 1660703c [feature/f283-machine-contracts-part-two]`.

## Deviations & assumptions

1. **One unordered commit, `1660703c` "F283 R15 C6-fix", lands between C6 and
   C7.** Self-review after C6 found `tests/test_brain_viewer.py`'s
   `test_open_answers_the_envelope` invoking the REAL platform opener
   (`subprocess.Popen(["xdg-open", ...])`) with no mock — it launched an
   actual browser session on this machine during a local pytest run (visible
   in captured stdout as "Opening in existing browser session."). This is a
   genuine test-hygiene defect the block's SPEC does not itself create (the
   SPEC only asks for `opened` in the envelope; nothing requires the test to
   exercise the real subprocess call), so it was fixed as its own small commit
   — touching only `tests/test_brain_viewer.py`, already inside constraint
   3's path set, 10 insertions, well under the 500-line cap — rather than
   folded silently into C6 by amending (never done once a commit exists, per
   the git safety protocol) or left unfixed and shipped with a live side
   effect. The block's own G5 mutation (f) and the derived-set/selection
   readings above are all taken from AFTER this fix, so nothing in this
   handback's verification depends on the pre-fix state.
2. **`decision.py`'s three commits' worth of catalog and handler edits were
   written directly against each commit's own slice**, C4 then C5 then C6, in
   that order, with no draft-then-restore cycle — unlike round 14's noted
   editing-order deviation, this round's C3/C4/C5/C6 boundaries followed the
   block's group order directly (pins first, then `decision`, then `job
   plan`, then `brain`), so there is nothing to report here beyond the one
   item above.
3. **`assumption_log` in `decision resolve`'s `plan:` approve envelope carries
   the raw `Path` object**, not a pre-stringified one; `apps/cli/json_envelope.py`'s
   `_write` already serializes with `json.dumps(..., default=str)`, so the
   envelope's JSON is a plain string either way — passing the `Path` directly
   avoids a redundant `str()` call and matches how `mission_id` (also
   sometimes `None`) is passed unconverted.
4. **`next_command` on the `td:` (task-decision) `answered` family carries the
   FULL printed line** (`"Resume the run: remedy job resume <job_id> --json"`),
   not the bare command, reading the block's parenthetical "(the resume line
   it prints)" literally as the line's whole text rather than a stripped
   command fragment.
5. **Constraints 1, 2, 3, 4, 6 and 7 held throughout.** No payload was edited
   or retyped; every commit stayed under 500 insertions (270, 12, 44, 337, 67,
   243, 10; this handoff exempt as a single `.agent/**` state file); the
   round's tracked path set (20 distinct paths before this commit, 21 after)
   is EXACTLY constraint 3's full enumeration, with nothing outside it and
   nothing missing; `packages/` was never touched; every commit from C3 on
   left selection A at zero failed and zero errors; nothing was merged, no PR
   created, no checkout of `main`; both G5 worktrees were removed as their own
   last action.

### The round's whole tracked path set (before this commit)

`git diff --name-only dfce6076 1660703c` — **20** distinct paths
(`apps/cli/command_catalog.py` touched by C4, C5 and C6;
`tests/test_command_catalog.py` touched by C4, C5 and C6;
`tests/test_brain_viewer.py` touched by C6 and C6-fix — each counted once);
plus `.agent/handoff.md` from this commit makes **21** — EXACTLY constraint
3's full enumeration:

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f283-r15-block.md | C1 `7f089cb4` |
| 2 | .agent/authored/f283-r15-ledger.md | C1 `7f089cb4` |
| 3 | .agent/authored/f283-r15-plan.md | C1 `7f089cb4` |
| 4 | .agent/authored/f283-r15-slips.md | C1 `7f089cb4` |
| 5 | .agent/live_review.md | C2 `7c5047cd` |
| 6 | .agent/plan.md | C2 `7c5047cd` |
| 7 | .agent/prose_slips.md | C2 `7c5047cd` |
| 8 | tests/cli/test_blocker_cmd.py | C3 `c5ce1789` |
| 9 | tests/cli/test_patch_cmd.py | C3 `c5ce1789` |
| 10 | apps/cli/command_catalog.py | C4 `9748191f`, touched again by C5 `768c97fe` and C6 `39e0c1e3` |
| 11 | apps/cli/commands/decision.py | C4 `9748191f` |
| 12 | tests/cli/test_decision_answers.py | C4 `9748191f` |
| 13 | tests/cli/test_decision_cmd.py | C4 `9748191f` |
| 14 | tests/cli/test_job_refusal_envelope.py | C4 `9748191f` |
| 15 | tests/cli/test_plan_approval.py | C4 `9748191f` |
| 16 | tests/test_command_catalog.py | C4 `9748191f`, touched again by C5 `768c97fe` and C6 `39e0c1e3` |
| 17 | apps/cli/commands/job.py | C5 `768c97fe` |
| 18 | tests/orchestration/test_structured_planner_cli.py | C5 `768c97fe` |
| 19 | apps/cli/commands/brain.py | C6 `39e0c1e3` |
| 20 | tests/test_brain_viewer.py | C6 `39e0c1e3`, touched again by C6-fix `1660703c` |
| 21 | .agent/handoff.md | C7 (this commit) |

No path outside constraint 3's enumeration was touched: `.agent/candidates.md`,
`.agent/context.md`, `.agent/operator_questions.md`, `.agent/decisions.md`,
`README.md`, `docs/roadmap/**`, `scripts/**`, `apps/cli/json_envelope.py` and
`apps/cli/grouped.py` appear **0** times. `packages/` appears **0** times
(confirmed above under G3).

## Authored-text proofs

- The four copies at C1, compared with the block's originals under
  `.remedy-wt/f283-r15-payloads/` and `.remedy-wt/f283-r15-block.md`: **four
  readings, all True** (G1).
- The two APPEND payloads against their committed files: strict byte
  concatenation True for `.agent/live_review.md` (ledger.md) and
  `.agent/prose_slips.md` (slips.md), byte numbers equal to the block's (G2a).
- The one REWRITE payload against its committed file: `.agent/plan.md`'s
  committed sha256 equals the payload's sha256 (G2c).
- No payload was edited or retyped. The block copy and three payload copies
  were made with `shutil.copyfile`; the two appends by reading each payload's
  bytes and writing base+payload back to disk; the plan.md rewrite by
  `shutil.copyfile`.
- Every change under `apps/` and `tests/` this round was WORKER-authored to
  the block's SPEC and DECISIONs F283 D9/D7 — there is no reviewer-authored
  diff to compare against for those files; G3/G4/G5 above are the proof they
  meet the SPEC.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Pre-flight (STOP, git state, block self-verify) | done | no STOP; tree clean at `dfce6076`; block 232 lines / matching sha256 |
| C1 copy block + 3 payloads | done | 270 insertions |
| C2 book round 14 PASS and a prose slip | done | 12 insertions (2+9+1, 11 deletions from plan rewrite); open set 24→24, added/removed empty |
| C3 pin blocker resolve's full id and patch show's text refusal | done | 44 insertions, tests only; both properties already correct on disk |
| C4 decision resolve and decision explain answer --json | done | 337 insertions; derived set 18 |
| C5 job plan answers --json | done | 67 insertions; derived set 17 |
| C6 the brain report and viewer commands answer --json | done | 243 insertions; derived set 10, exactly the `ui`/`project` leaves |
| C6-fix mock the opener (unordered, reported above) | done | 10 insertions, no code change, test hygiene only |
| C7 the handback | done | this commit |
| G1 payload transport + authored copies | done | 3/3 payload readings equal; 4/4 authored copies byte-identical |
| G2(a) live_review.md + prose_slips.md append | done | 517382+3399=520781; 361828+657=362485 |
| G2(b) open set by distinct id | done | 1 Gate line; 24→24, added none, removed none |
| G2(c) plan.md rewrite | done | sha256-equal to payload; 35 lines, under 50 |
| G3 change counted from the tree | done | per-commit diffs and insertions reported; derived set 18→17→10; pairs.py decision.py/brain.py/job.py exits unchanged in count, decision.py's one exit no longer mechanical; 0 paths under `packages/` |
| Token list | done | `decision_not_resolvable` is new (0 hits at base); all 21 other touched tokens reused |
| G4 targeted selection, ruff, integrity, golden path | done | 8454/8462/8464/8472/8472 passed after C3/C4/C5/C6/C6-fix (up from 8452), 0 failed/errors at each; ruff exit 0; integrity all 5 pass, fail_count 0; golden path 42 passed |
| G5 red-proofs (a)(b)(c)(d)(e)(f) | done | all six go RED, each reddening exactly its named target; unmutated control 233 passed |
| G6 tree, push, PR list | pending at write time | reported in the worker's session reply with real exit codes |
| Constraint 1 no payload edited/retyped | done | `shutil.copyfile`, byte concatenation only |
| Constraint 2 every commit under 500 insertions | done | 270, 12, 44, 337, 67, 243, 10; this handoff exempt as single `.agent/**` state file |
| Constraint 3 no unnamed file touched | done | 20 paths before this commit (21 after), EXACTLY the full enumeration |
| Constraint 4 G4 selection at zero failed after every commit | done | 8454/8462/8464/8472 passed, 0 failed/errors at each |
| Constraint 5 STOP if a gate goes red outside constraint 3's path set | done (n/a) | no gate went red outside the named paths; no STOP was needed |
| Constraint 6 nothing is merged | done | no `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch deletion |
| Constraint 7 G5 worktree under .remedy-wt/, removed, listed | done | `.remedy-wt/f283-r15-redproof` (two sequential instances), both removed, `git worktree list` reported after; no other worktree disturbed |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 15 — C1 through C7 (including the unordered C6-fix),
   all six gates re-derived.
3. Then T001's catalog half's last group, as `.agent/plan.md` lists it: the
   five `ui` and five `project` commands, with the ratchet asserting the set
   empty.

Open findings count: **24**. Operator-questions count: **0**.
