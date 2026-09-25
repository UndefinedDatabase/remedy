# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q1 — Post-task lessons start switched off (2026-09-24, F265, round 1)

**What needs deciding.** Remedy can now write a short lesson after each finished task of a
job. The lesson explains the change that task really made to the code: what was built, which
functions and language features it uses, what they do, why they fit there, and whether that is
good practice, stated as the teacher's opinion. Writing one lesson costs one call to the
teacher's model for every finished task. I have made lessons switched off unless you turn them
on, with the setting named `teacher.lessons` in your project's settings file or the environment
variable named `REMEDY_TEACHER_LESSONS`. You can tell me they should be on unless switched off.

**Why it matters.** With lessons on, every finished task makes one extra model call, and a large
job has many tasks. I also set a spending limit for these calls in each job: at most thirty
calls, and at most three hundred thousand tokens, which are the units a model counts its reading
and writing in. When a job reaches either limit, the tasks after it get an empty lesson that says
the limit was reached, never a shortened one.

**My recommendation.** Keep lessons off until you switch them on. A run should never spend money
on something the person running it did not ask for, and the optional written summary of a failed
run already follows that same rule. Switching lessons on is a single setting.

**What happens if you say nothing.** The recommendation is already executed and stands until you
say otherwise. Lessons stay off until you switch them on, and the spending limit for each job
applies from the first lesson.

### Q2 — Live graph reads today's event stream (2026-09-24, F019, round 1)

**What needs deciding.** The next feature makes the job graph in the browser grow while a job
runs: the job in the middle, its tasks around it, and a small node for each attempt, review and
check as it happens. The plan for this feature expected the server to send richer event messages
than it really sends. Today each message names what happened and which task it belongs to, but not
which attempt, and some kinds of message name no task or no result at all. I have built the graph
from the messages as they really are, without changing what the server sends, because the plan
lists the message format as something this feature must not change. You can tell me to widen the
messages instead.

**Why it matters.** Two things follow. First, the tasks appear when the task list appears on the
dashboard, not at the moment the plan is approved, because approving a plan sends no message.
Second, runs of the test command and the automatic repair loop do not show up as their own nodes
yet, because their messages do not say which task they belong to or whether they passed. The
graph never shows a result it was not told, so it leaves those nodes out rather than guess.
Builder attempts, reviews and checks do appear, each with its real result.

**My recommendation.** Keep the message format as it is for now. Changing it touches every
consumer of the stream at once, and a later feature can add the missing fields on purpose, after
which the graph can draw those nodes with a small change.

**What happens if you say nothing.** The recommendation is already executed and stands until you
say otherwise. The graph grows from the messages that exist today, and the test and repair nodes
stay out until the messages carry what they need.

### Q3 — Prompt dots move to simple view (2026-09-24, F019, round 3)

**What needs deciding.** The job graph in the browser now has two pictures. The new live picture
is the default: it draws the job in the middle, its tasks around it and a small node for each
attempt, review and check, and it is the picture that will grow on its own while a job runs. The
older, simpler picture is one click away behind a new button named "Simple view". Only the simple
picture shows the small dots beside each task that stand for the prompts Remedy sent to the model,
the ones you can click to read a prompt. I have not put those prompt dots into the live picture.
You can tell me to add them there now.

**Why it matters.** The live picture only draws things its data model knows about, and that model
has no kind of node for a prompt yet. A later feature, the one that gives every kind of node its
own look, is planned to add prompts as their own nodes. Until then, a person who wants the prompt
dots has to press "Simple view". Reading a prompt from a task's detail card works in both pictures,
and so do the task list and the keyboard, because the simple picture is also the one whose nodes
can be reached with the keyboard.

**My recommendation.** Keep the prompt dots in the simple picture for now. Adding them to the live
picture today would draw nodes the data model does not hold, which the design rules for the graph
forbid, and the later feature adds them properly.

**What happens if you say nothing.** The recommendation is already executed and stands until you
say otherwise. The live picture is the default and the prompt dots stay one click away in the
simple picture.

### Q4 — Browser resume points at relaunch (2026-09-25, F025, round 4)

**What needs deciding.** You can now pause a running job, either the whole job or one of its
tasks, from the browser or from the command line. A paused job does not keep a program running
while it waits: it saves where it stood and the program ends. To continue, the job has to be
started again with the command `remedy job run` followed by the job's name, and it then carries on
from exactly where it stopped. The browser page cannot start a program, because the part of Remedy
that takes commands from the browser is deliberately not allowed to launch anything. So when you
press resume in the browser on a job that is already paused and saved, the page will tell you that
the job is paused and show you the command that continues it, instead of continuing it by itself.
You can tell me to give the browser a way to start the job again.

**Why it matters.** A resume that only shows a command is one extra step for you. The alternative
is a small helper that is allowed to start jobs on your behalf, which widens what a click in the
browser can do on your machine. Resuming a single paused task inside a job that is still running
needs no extra step: the running job picks the task up again at its next safe moment. Taking back
a pause that the job has not reached yet also needs no extra step.

**My recommendation.** Keep the browser from starting programs. Showing the exact command is
honest and safe, and a later feature can add a launcher on purpose, with its own safety rules.

**What happens if you say nothing.** The recommendation is already executed and stands until you
say otherwise. Resume in the browser takes back a waiting pause or releases a paused task at once,
and for a job that is already paused and saved it shows the command that continues it.
