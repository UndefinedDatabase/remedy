# Handback — F027 Task veto · Round 5 (BLOCKED)

## Session

SESSION 1 of feature F027 · round 5 · rounds so far 5

Roughly half the session's context budget remained at the point this handback was written.
This round booked round 4's verdict, registered and repaired R-1067 (the accept answer now
names `remedy job run`, not `remedy job resume`), and landed `job.veto-task` in the catalog and
the CLI. C5 — the write door's veto clause, its answer of a `veto:` replan proposal, and the
inbox's mirrored predicate — is WRITTEN but NOT COMMITTED: its own S6 guard test goes red for a
reason plan.md's own Risks section named in advance ("The door may reach no new forbidden
module"), and the block's own S6 clause orders a stop exactly here: "if the transitive test goes
red you stop and report it." This handback is that stop.

## Range

Review of c1c366568..d98f9922f (C1 through C4, all committed and pushed). C5's diff exists only
in the working tree, uncommitted, and is described in full under Deviations below.

## Commits

### a540e6e68 F027 R5 C1: copy round 5 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f027-r5-block.md | +244/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f027-r5-plan.md | +32/-0 | copy of the plan.md payload |
| .agent/authored/f027-r5-records.diff | +68/-0 | copy of the records.diff payload |

344 insertions by `git show --numstat` — matches the block's stated expectation exactly (block
line count 244 plus 100), under the 500-line cap.

### 2bb422d4a F027 R5 C2: book round 4, register R-1067, record D5
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +48/-0 | DECISION F027 D5 appended, verbatim from records.diff |
| .agent/live_review.md | +4/-0 | round 4's Gate entry and R-1067's registration appended |
| .agent/plan.md | +11/-11 | rewritten whole to the plan.md payload |

48/0 decisions.md, 4/0 live_review.md, 11/11 plan.md by `git show --numstat` — matches the
block's stated expectation exactly. `git apply --check` on records.diff → exit 0; the real
`git apply` → exit 0.

### 90e5b5292 F027 R5 C3: repair R-1067, name job run for an accepted scope
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/decision.py | +1/-1 | S1: the `veto:` accept sentence now names `remedy job run <job>`, not `remedy job resume` |
| tests/cli/test_decision_cmd.py | +14/-0 | a new non-JSON test on the accept path pins `remedy job run <job.job_id>` in stdout and pins `remedy job resume` absent |

15 insertions by `git show --numstat`. `python3 -m pytest tests/cli/test_decision_cmd.py -k TestDecisionResolveVetoAnswersJSONThroughTheDispatcher` → 4 passed. `ruff check` on both files → clean.

### d98f9922f F027 R5 C4: job.veto-task in the catalog and the CLI
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | +24/-0 | S2: `CommandEntry` `job.veto-task` beside `job.edit-task` (positional `job_id`, `task`; required `--reason`; exit codes 0/1/2/3); joins `UI_EXPOSED_COMMANDS` |
| apps/cli/commands/__init__.py | +2/-1 | registers `job_veto_cmd` in the import list and the handler-collection tuple |
| apps/cli/commands/job_veto_cmd.py | +79/-0 (new) | S3: the CLI handler — loads the job, resolves the task via `job_plan_cmd._resolve_task_arg`, calls `veto_task_command` as `cli`, prints the vetoed task/request id/unreachable set or `--json`'s own keys, maps refusals to exit 2 (`reason_required`, `reason_too_long`, `reason_invalid`, `unknown_task`), 3 (`job_not_vetoable`, `task_not_vetoable`, `task_already_vetoed`) or `fail()`'s default 1 (job not found) |
| docs/guides/exit-codes.md | +1/-0 | `remedy job veto-task` row, reading 3, beside `remedy job edit-task`'s |
| tests/orchestration/import_reachability_allowlist.txt | +1/-0 | `apps.cli.commands.job_veto_cmd` in its sorted place |
| tests/cli/test_job_veto.py | +212/-0 (new) | veto by the task's own id and by its plan id, the printed request id and unreachable set, `--json`'s keys, every refusal's exit code (including a job that does not exist → 1), a blank reason writing nothing, and the `task_vetoed` event's reason held verbatim |

319 insertions by `git show --numstat`, under the 500-line cap. `ruff check` over all six files →
clean. `python3 -m apps.cli.main job veto-task --help` → prints the usage, arguments and options
correctly (captured in full below). Test selection run: `tests/cli/test_job_veto.py` (13 passed),
plus the broader C4 selection (`test_job_plan_cmd.py`, `test_job_pause.py`,
`test_command_catalog.py`, `test_advertised_commands.py`, `test_exit_codes.py`,
`test_import_reachability.py`, `test_no_orphan_modules.py`, `test_event_names.py`, `tests/docs`,
`test_golden_path.py`) — 883 passed. One deviation inside this commit: the `--reason` ArgDef's
help text was worded "Why the job plan's task is being vetoed (required)" rather than a plainer
phrasing, because `tests/docs/test_vocabulary.py`'s enforced-mode check requires every catalog
description using a binding word ("task") to also carry one of that word's page-defined meaning
fragments ("job plan", "step" or "run"); the plainer wording failed
`test_every_binding_word_in_a_description_carries_the_pages_meaning` until "job plan" was folded
in.

## External actions

`git push -u origin feature/f027-task-veto` after C4 → succeeded (reported below under
Verification, since it was re-checked at handback time too). No PR created (constraint 5:
nothing is merged, and none was open before this round — see the Open PR Gate reading below).
No worktree added or removed this round; C5's own worktree-add step (constraint 6, "the worktree
G5 adds") was never reached because C5 was never committed.

## Verification

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` at round start → `[]`
(empty; matches G6's requirement and confirms no PR needed opening or merging first).

C1–C4's own gates (G1 transport proofs, G2 records proofs, ruff, `--help`, and the test
selections named in each commit's table above) all read as described above and in the item-status
table below — every one of them a real, re-runnable command, not a summary.

C5's own gates were run against the UNCOMMITTED working tree (S4 in
`packages/orchestration/ui_server.py`, S5 in `packages/orchestration/decision_inbox.py`, the rest
of S6 in `tests/ui_server/test_command_channel.py` and
`tests/orchestration/test_decision_inbox.py`):

```
$ ruff check packages/orchestration/ui_server.py packages/orchestration/decision_inbox.py tests/ui_server/test_command_channel.py tests/orchestration/test_decision_inbox.py
All checks passed!
REAL_EXIT=0

$ pytest -q tests/orchestration/test_decision_inbox.py
47 passed
REAL_EXIT=0

$ pytest -q tests/ui_server/test_command_channel.py
108 passed, 1 failed
REAL_EXIT=1
FAILED tests/ui_server/test_command_channel.py::TestCommandDoorImportGuard::test_the_door_reaches_only_the_accepted_forbidden_modules_transitively
AssertionError: {'unrecorded': ['packages.orchestration.exec_guard', 'subprocess'], 'vanished': []}

$ pytest -q tests/ui_server/test_command_dispatch.py tests/ui_contracts/test_steering_send_contract.py tests/orchestration/test_veto_proposal.py tests/orchestration/test_task_veto.py tests/cli/test_decision_cmd.py tests/test_command_catalog.py tests/cli/test_advertised_commands.py tests/orchestration/test_event_names.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py
384 passed
REAL_EXIT=0

$ pytest -q tests/docs
327 passed
REAL_EXIT=0
```

`python3 -m apps.cli.main job veto-task --help` (unaffected by C5's uncommitted diff, since the
CLI help comes from the already-committed C4 catalog entry):

```
 Usage: remedy job veto-task [OPTIONS] JOB_ID TASK

 Veto one task of a job, so it and everything that depends on it will not run (F027).

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│  job_id  UUID of the job (under its mission)                                 │
│  task    The task: its id in the job, or its id in the job plan, as `remedy  │
│          job plan-show` prints them                                          │
╰──────────────────────────────────────────────────────────────────────────────╯

╭─ Options ────────────────────────────────────────────────────────────────────╮
│  --reason  Why the job plan's task is being vetoed (required)                │
│  --json    Output as JSON                                                    │
│  --help    Show this message and exit.                                       │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## Authored-text proofs

Block copy: `git show a540e6e68:.agent/authored/f027-r5-block.md` byte-compared (`cmp`) against
`.remedy-wt/f027-r5/block.md` → identical (exit 0). Plan payload copy: same comparison against
`.remedy-wt/f027-r5-payloads/plan.md` → identical. Records-diff copy: same comparison against
`.remedy-wt/f027-r5-payloads/records.diff` → identical. Post-C2, the sha256 of `.agent/live_review.md`,
`.agent/decisions.md` and `.agent/plan.md` read via `git show 2bb422d4a:<path> | sha256sum` all
matched the block's G2 table exactly: `6701311c7082de519bd0a555414149dcffd415b9d32fb234bf06887817db0a44`,
`864434df8a8ac0d3b4d2fee6df1e54cc5a6423a0e063b8b53c737cdc8028e03f`,
`29f5c082baba39c3069ede2fd126ff15e72222dc011bb66b2c84449398834a40`. `open_finding_ids` over that
same reading → `['R-1067']`; the ledger's last line begins `- R-1067 — `. Both match the block's
stated readings.

## Deviations & assumptions

**THE BLOCKER (constraint 4 / S6's own stop clause).** S4 requires the write door to import
`task_veto.veto_task_command` and `task_veto.validate_veto_reason` (and `veto_proposal.answer_replan_proposal`)
inside its own methods. The moment ANY name is imported from `packages.orchestration.task_veto`
inside a scanned door method, `TestCommandDoorImportGuard`'s
`test_the_door_reaches_only_the_accepted_forbidden_modules_transitively` seeds its static
module-level closure from `packages.orchestration.task_veto`, which — at `9f884fbb` and untouched
by this round (`task_veto.py` is on the round's do-not-touch list) — imports
`packages.orchestration.stream_evidence` at module level for `redact_text`.
`stream_evidence.py` in turn carries, inside an `if TYPE_CHECKING:` block, `from
packages.orchestration.exec_guard import ExecGuardPolicy` (a type-only import; the runtime import
is function-scoped, right next to its one real use, per that file's own comment). The guard's
`_module_level_closure` helper does not special-case `TYPE_CHECKING` blocks — it walks every
`ast.If` body via plain `ast.iter_child_nodes` recursion — so it counts this type-only import as
real, and `exec_guard` (which imports `subprocess`) enters the transitive-forbidden set for the
first time the door ever reaches `task_veto.py` at all. I confirmed with a standalone script
(`.remedy-wt/f027-r5-worker/trace_closure2.py`) that this reach is exactly
`task_veto → stream_evidence → (TYPE_CHECKING) exec_guard → subprocess`, and confirmed the SAME
result from the real pytest run, not just the script. `ACCEPTED_TRANSITIVE_FORBIDDEN` is
"stays as it is" per S6 — I did not touch it — so the guard reads it red. `.agent/plan.md`'s own
Risks section, written by the reviewer BEFORE this round started, already named this exact risk
("The door may reach no new forbidden module"), which is why I read this as the anticipated stop
rather than a defect in my own code: every OTHER test the round's changes touch is green (108/109
in `test_command_channel.py`, 47/47 in `test_decision_inbox.py`, 384/384 across the rest of G4's
selection, 327/327 in `tests/docs`, ruff clean).

I did NOT commit C5. The working tree carries S4 (in `packages/orchestration/ui_server.py`: a
`JOB_VETO_TASK_COMMAND_ID` constant, the `_read_command_payload` shape check for `task_id` and
`reason` — the latter via `task_veto.validate_veto_reason`, caught as `TaskVetoRefused`, which I
also had to import beside it because there is no way to detect its three failure codes without
naming its exception class, and no way to add a NEW blind `except Exception` instead: the
project's frozen `tests/test_ble001_ratchet.py` (`MAX_EXCUSED = 290`, not in this round's tracked
path set) forbids growing that count — a new clause in `_handle_command_submission` beside the
pause's calling a new `_dispatch_veto_task` method, and a `veto:` branch in
`_dispatch_decision_resolve` before the escalation route calling
`veto_proposal.answer_replan_proposal`), S5 (in `packages/orchestration/decision_inbox.py`:
`_answerable_by_decision_resolve` gains a `veto:` branch, true while a `vetoed_tasks` entry
exists with no `veto_answers` entry, false on `TaskVetoError`), and the rest of S6
(`tests/ui_server/test_command_channel.py`: `DOOR_METHODS` gains `_dispatch_veto_task`;
`ALLOWED_IMPORTS` gains FOUR entries, not the block's stated three —
`task_veto.veto_task_command`, `task_veto.validate_veto_reason`, `task_veto.TaskVetoRefused` and
`veto_proposal.answer_replan_proposal` — for the reason just given; two OTHER existing tests in
that file needed updating for C4's already-committed catalog widening
(`test_every_exposed_command_reaches_the_answer_its_effect_gives` gains a `job.veto-task` branch
expecting 400 on `task_id`, and `test_the_set_holds_exactly_the_ruled_ids_and_no_other`'s literal
list gains `job.veto-task`); `tests/orchestration/test_decision_inbox.py`: `ANSWERABLE_DECISION_TYPES`
gains `replan_proposal`, and a new test proves a `veto:` card answerable while open and — since
an ANSWERED veto's `replan_proposal` decision is filtered out of `list_decisions` entirely by
`veto_proposal._qualifying_entries` rather than merely marked resolved (unlike `task_decision`) —
not answerable once answered, read directly off `_answerable_by_decision_resolve` rather than off
a vanished card). `tests/ui_server/test_command_dispatch.py`'s own door-veto tests (THE TESTS
section's HTTP-level coverage: a 200 with the veto written, a blank/too-long/secret-shaped reason
each 400 with no control file written and no job read, a missing `task_id` a 400, an already
vetoed task and a finished job each 409 naming the code, the audit outcomes, and the door's
answer of a `veto:` proposal) were NOT YET WRITTEN — I stopped at the guard failure rather than
completing C5's remaining test surface, since the blocker does not depend on those tests and
completing them first would not have changed the stop.

C1–C4 have no deviations beyond the one already noted in C4's own row above (the `--reason`
wording, forced by the vocabulary test).

## Next

The reviewer's ruling on the transitive-forbidden guard: either `ACCEPTED_TRANSITIVE_FORBIDDEN`
gains `packages.orchestration.exec_guard` and `subprocess` under a new DECISION explaining that a
`TYPE_CHECKING`-only import is what is actually reached (never a runtime one), or a different
design reaches `veto_task_command`/`validate_veto_reason`/`answer_replan_proposal` without
seeding the closure from `task_veto.py`/`veto_proposal.py` at all. Once ruled, land C5 (adding
`tests/ui_server/test_command_dispatch.py`'s door-veto tests), C6 (the mutation tool) and C7 (the
real handback), then re-run G1–G6 in full. Open findings: 1 — R-1067, landed at `90e5b5292` but
not yet booked as `Landed:` in `.agent/live_review.md` (deferred to the round that reaches C7,
since G1–G5 must pass before that line is written and they have not). Operator-questions count: 5.
