F025 pause and resume (a running job can now be paused as a whole, or one of
its tasks can be paused, from the command line with `remedy job pause` or from
the browser; the step that is already running finishes and nothing new starts,
and the job saves where it stood and its program ends instead of waiting in the
background; the browser shows an orange PAUSED banner above the graph, says
"Paused by you" where it tells you what the agent is doing, marks a paused task
with two small orange bars, and offers pause and resume buttons for the job and
for each task that has not started yet; a paused task waits together with the
tasks after it in an ordinary job, and in a job whose tasks form a graph only
the tasks that depend on it wait while the rest keeps going; to continue a paused
job you start it again with `remedy job run` and the job's id, which the page
also shows, and it carries on from exactly where it stopped without redoing
finished tasks; a stop always wins over a pause, and the job's time limit keeps
counting while it is paused; one thing is not done yet: the AI conversation of
a task that a pause interrupted starts afresh when the job continues).
