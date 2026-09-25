F026 task edit at runtime (a task of an approved plan can now be changed while its job
is not running — its title, goal, acceptance criteria, size or file hints — when the
task is still waiting, is paused, or has failed; you edit it from the command line with
`remedy job edit-task`, naming the task and the version you are changing, or from the
task's detail panel in the browser, which offers an "Edit task" form only for a task
that can take an edit; every edit gives the task a new version number, keeps the old
version on disk, and is recorded with who made it; a task that had failed goes back in
the queue together with the tasks its failure had skipped, and you start the job again
with `remedy job run` and the job's id; the next run uses the new text, which the
record of what the agent was told shows; in the browser an edited task carries a small
version label such as "v2" beside it on the graph and in its detail panel, which also
lists every version and what changed; a running job, and a task that is running or
already done, cannot be edited, and the reason is named).
