
## DECISION F268 D9 (2026-09-18, reviewer, round 4) — the cockpit opens detached, `--apply` applies every job, and the flags of unbuilt features refuse before any step
CONTEXT: measured at `f831d374`, `ui._cmd_ui_start` in `apps/cli/commands/ui.py` blocks in
`start_ui_server`'s serve loop and opens the browser itself unless `--no-open`; `ui stop` stops every
running UI session; `job_apply.apply_job(job_id, target_repo, approve=True)` applies one job; F269
and F270 are `[ ]` in `docs/roadmap/STATUS.md`.
CHOSEN: (1) unless `--no-ui`, the ui step starts `remedy ui start <job id> --port 0 --info-file <path>`
for the walk's last job as a DETACHED child process (its own session, output to a log file under the
data root, never the repository), waits a bounded time for the info file, and reports the cockpit's
URL and the stop command `remedy ui stop`; a launch that does not come up in time is reported
`skipped` with the reason and the manual command, because the run's result does not depend on the
cockpit. The launcher is a function the walk's context carries, so tests never start a server.
(2) `--apply` makes the apply step call `apply_job(<job id>, <repo root>, approve=True)` for every job
of the walk in order, stopping at the first that is not applied and naming why; `--json`'s
`stopped_before_apply` is then false. Without `--apply` the step is unchanged. (3) `--contract
<template>` (F269) and `--commit "<message>"`, `--commit-auto`, `--commit-with-history`, `--push`
(F270) are declared on `do.run` and, while their feature is not `[x]`, each exits 2 before any step
runs, printing that it is not yet available and which feature brings it; the old name
`--with-history` is never created. ALTERNATIVES: run the cockpit in-process on a thread, rejected
because the server's serve loop would hold `do` open after its last step; omit the unbuilt flags,
rejected because T2_F268.md's Design names them as a documented dependency. REVERSE: delete the
launcher, the `--apply` branch and the refusing flags; delete this paragraph.
