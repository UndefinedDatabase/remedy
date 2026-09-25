
## Built State (F025, 2026-09-25)

What exists on disk at the close of F025, built in eight rounds over two sessions on
`feature/f025-pause-resume`, cut from `main` at `49624d5c`. Every DECISION named lives in
`.agent/decisions.md`; every round's verdict in `.agent/live_review.md` or, once rotated, its
archive.

**T001 — the control kinds, the park and the mask.** `packages/orchestration/pause_control.py`
keeps a job pause as a create-only control file beside the kill switch's, settled into
`pause_archive/` before it is removed, and a task pause as one create-only file per task under
`paused_tasks/`, named by a digest of the task id; its pure mask withholds, on the linear runner,
the first paused pending task and everything after it, and on a graph the paused pending tasks with
their transitive dependents. `run_job` reads the job pause and the mask at the stop's own safe
points, after every stop: the call in flight finishes, the interrupted task returns to `pending`,
the job persists as `paused` with its pause record, one `job_paused` is written per request, and the
process exits. The relaunch is the resume: a job still paused or still withheld stays parked with
no call and no event, and otherwise lifts the record with one `job_resumed` and carries on. A stop
beats a pause, and the deadline keeps counting through one. `run_cycles` parks the same way under
its terminal `paused_by_operator`, withholding paused branches and naming them in its cycle record
while siblings proceed (DECISION F025 D1).

**T002 — the channel and the CLI.** `job.pause` and `job.unpause`, each with an optional task, are
catalog commands, the CLI verbs of `apps/cli/commands/job_pause_cmd.py`, and two clauses of the
write door, all sharing `pause_job_command` and `unpause_job_command`. A terminal job or an unknown
task is refused with its state or id named, 409 at the door; `job.unpause` releases a task,
withdraws a pause no safe point has served, answers a parked job with `parked` and the relaunch
command, and otherwise `not_paused`. `task_paused` and `task_resumed` are written exactly once per
request by the ledger (DECISION F025 D2; R-1051 and R-1052). The door starts no process, so a
browser resume of a parked job shows the command, as operator question Q4 records.

**T003 — the page, the manifest and the end-to-end.** The dashboard serves `pause` — the record,
whether a pause is pending, the paused pending tasks and any control error — and the graph has the
node state `paused`: a planned node with an orange two-bar pause mark, set by `task_paused`, seeded
from the dashboard and cleared by `task_resumed` (DECISION F025 D3). `apps/ui/src/api/pauseSend.ts`
sends both commands and reads the door's answer; `pauseView.ts` derives the banner, the NowCard's
"Paused by you" and the two controls' actions; `PauseControl.tsx` is mounted below the NowCard and
in the task popover, and the banner sits in the graph's chrome (DECISION F025 D4; R-1053 and
R-1054). A park records the episode it ends in the run manifest under the status `paused`, so a
relaunched job writes its manifest over both episodes (DECISION F025 D6; R-1056).
`tests/ui_server/test_pause_e2e_live.py` pauses a live job of both scopes through the door,
relaunches it with the real `python3 -m apps.cli.main job run`, and compares it with an unpaused
control run of the same job file (DECISION F025 D5).

**Acceptance, by the test that proves it.** Both scopes pause before the next call:
`TestRow1JobPauseDuringABuildCall` and `TestRow4AMidPlanTaskPause` in
`tests/orchestration/test_pause_resume.py`, and `tests/ui_server/test_pause_door_live.py` through
the real door. They resume exactly, with final state equal to a control run's by the normalized
record, the workspace bytes and the ordered task events: `tests/ui_server/test_pause_e2e_live.py`.
Downstream of a paused node waits with the reason visible while siblings proceed:
`TestC3TheDiamondWithBPaused` and `TestC6AnAwaitingBranchBesideAPausedBranch` in
`tests/orchestration/test_pause_resume_cycles.py`. Deadline honesty during a pause:
`TestRow7TheDeadlineKeepsCountingThroughAPause` and `TestC8TheDeadlineKeepsCountingThroughAPause`.
No daemon lingers: the process checks of the two live door files. A pause never strands a job: the
relaunch tests of both runners and `tests/orchestration/test_pause_manifest.py`. The edge cases —
a terminal job refused with its state named, a double pause idempotent, a stale approval still
refusing the relaunch — are `tests/cli/test_job_pause.py`, `tests/orchestration/test_pause_control.py`
and `TestRow11AStaleApprovalRefusesTheRelaunch`. Each round's mutation proofs are its
`.agent/authored/f025-r<n>-mutations.py`.

**Not met: provider sessions across a park.** The Done clause's "the resumed run provably reuses
its provider sessions where supported" is not met: Remedy's resume keeps no provider session across
processes, and a park returns the interrupted task to `pending`, so its relaunch starts a new
session. The finished tasks are never run again. Finding R-1055 records it, owned by F285, whose
Acceptance names it (DECISION F025 D5).

**Modules and lists (closure precondition 7).** F025 added `packages/orchestration/pause_control.py`
and `apps/cli/commands/job_pause_cmd.py`, and both lines to
`tests/orchestration/import_reachability_allowlist.txt`, `packages.orchestration.pause_control` and
`apps.cli.commands.job_pause_cmd`; nothing to `ALLOWED_UNWIRED` or to `RESERVED_NAMESPACES` in
`tests/test_no_orphan_modules.py`. Its other new modules are TypeScript under `apps/ui/src/`.

**Beyond the code.** Two rows of `docs/ui/design_reference/assumption_log.md`, and one of
`assets_spec.md` §4, record the paused node state, its mark, the banner and the buttons, none of
which the design reference drew. The kill switch's terminals, the checkpoint format and the session
mechanics are untouched.

**Findings.** F025 registered R-1049 to R-1056 and resolved all but one: R-1055, owned by F285.
The one open finding at its claim, R-1008, is owned by F285 and was neither touched nor re-assigned.
