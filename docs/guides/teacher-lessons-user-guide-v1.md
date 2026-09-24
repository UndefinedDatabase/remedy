# Post-task lessons from the teacher (v1)

After each task of a job finishes, Remedy's teacher can write a short lesson about the change
that task really made. The lesson says what was built, which functions and language features the
change uses, what each one does, why it fits there, and whether that is good practice, with that
last part stated as the teacher's opinion. You read the lessons in the cockpit, in a learning
sheet you open over the job's dashboard.

A lesson is written from the task's recorded change and from nothing else. It is never written
from the plan, because the plan is what was intended and the change is what shipped.

## Switching lessons on

Lessons are off until you switch them on, because each lesson costs one call to the teacher's
model for every task that finishes. Switch them on in your project's `remedy.toml`:

```toml
[remedy.teacher]
lessons = true
```

or set the environment variable `REMEDY_TEACHER_LESSONS` to `1` for the run. The teacher uses its
own model. Set it with `model` under the same `[remedy.teacher]` table, or with
`REMEDY_TEACHER_MODEL`. Today the teacher can call a local Ollama model only.

## What a lesson may spend

Each job has its own spending limit for lessons. By default a job may make at most thirty teacher
calls, and those calls may use at most three hundred thousand tokens (the units a model counts
its reading and writing in). Change the limits with `lesson_max_calls` and `lesson_max_tokens`
under `[remedy.teacher]`. Every call is recorded in the cost ledger under the role `teacher`, so
spend grouped by role shows the teacher apart from the builder.

When a job reaches either limit, the tasks after that get an empty lesson that says so. You never
get a shortened lesson that looks complete.

## When there is no lesson

The index always says why a task has no lesson, in one of these ways:

- the task has not run yet;
- lessons are switched off;
- the task recorded no change, so there is nothing to teach;
- the change is too large to send whole, and a lesson about part of it would mislead;
- the job belongs to no registered project, so the teacher's spend could not be recorded;
- the spending limit is reached;
- the teacher's model could not be reached;
- the teacher's answer could not be read.

## Reading the lessons

Open a job's dashboard from its own link and press **Lessons** in the right-hand panel. The index
of the job's tasks is on the left, and the chosen task's lesson is on the right. **Previous** and
**Next** move between tasks, and the Escape key or **Close lessons** closes the sheet. While the
sheet is open, it reads the index again whenever the job announces a new lesson, so a lesson
appears as soon as its task finishes.

A lesson lists only the functions and features that actually appear in the lines the change adds.
If the teacher named something the change does not contain, it is left out, and the lesson says
how many names were left out.

## The Commands mode

Press **Commands** at the top of the sheet to see, for the chosen task, the Remedy commands its
change touched: every command whose code the change edited, and every command whose catalog entry
it edited. Each one is shown with the description Remedy ships today, read from the command
catalog when you open the sheet and never from a copy saved earlier. Press **Lesson** to go back.

## Where lessons are kept

Each lesson is stored once, beside the task's recorded change, and it is sealed so that any later
edit to it is noticed. Opening a lesson again reads the stored file and costs nothing. A lesson
that fails its seal is named as damaged in the index, and its text is not shown.
