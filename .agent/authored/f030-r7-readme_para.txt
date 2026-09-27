F030 steering notes (you can now write a note to one task while a job runs: select the task
in the graph and type in the box under the activity feed, or run `remedy job steer` with the
task named after `--task`; the note is recorded, and that task reads it at the start of its
next round, never in the middle of a call to a model, as a numbered note it must follow in
that round and every round after; the activity feed shows your note as your own line, and
the builder's next action is the only answer, because Remedy never writes a reply; when the
task finishes before it starts another round, the job's report and `remedy chat show` say
that the note was not taken in; with no task selected, the box still steers the whole job).
