# Steering a running job (user guide, v1)

A job that is heading the wrong way used to leave you one choice: stop it. Steering gives
you a cheaper one. You send the running job a short message in your own words, the job
reads it at its next safe point, and it tells you what it understood and from which round
it applies. The job keeps the rounds that were already fine.

Steering was built by feature F264. The design is in
[T5_F264.md](../roadmap/features/T5_F264.md), and the decisions behind it are the
`DECISION F264 D1` to `D7` entries in `.agent/decisions.md`.

## Send a message

From a terminal:

    remedy chat send <job_id> "Keep the public function names; rename only the private helpers."

The short form does the same thing:

    remedy chat <job_id> "Keep the public function names; rename only the private helpers."

The job id may be the full id or any prefix of it that names one job. Quote the message so
that it arrives as one argument. The command prints the message's id, for example
`sm-0001`, and says that the job reads it at its next safe point. Add `--json` to get the
message id, the time it was received and the seal of its record as JSON instead.

From the cockpit (`remedy ui start <job_id>`), type the message into the input at the
bottom of the activity card and press Enter or the arrow button. The sentence under the
input says what happened: the message was recorded, or it was refused and why. A refused
message stays in the input so that you can correct it and send it again.

A message must not be empty and may be at most 2000 characters long. A job that has
already ended takes no message, because no run would ever read it: the command exits with
code 3 and the cockpit input is shown disabled with that reason.

## When the job reads it

A job does its work as tasks, and each task runs in rounds: the builder model writes a
change, a reviewer checks it, and the next round repairs what the review found. The SAFE
POINT is the start of a round, before anything of that round is sent to a model.

- A message never reaches a model call that is already running. A message you send while
  round 2 is being built waits, and round 3 is the first round that sees it.
- Once a round has taken a message in, every later round of the job carries it too, in
  every task, in the order the messages were sent, and the builder is told that where two
  messages disagree, the later one wins.
- The message goes into the builder's prompt word for word, never shortened and never
  paraphrased.
- If the job belongs to a mission, taking the message in also adds it to the mission's
  contract as a new requirement, once, from the mission's next round.

A message that arrives during the job's very last round is never taken in, because no
later round exists to read it. `remedy chat show` then says so plainly, rather than leaving
you to assume the job followed it.

## See what the job understood

    remedy chat show <job_id>

This lists every message of the job, oldest first, with the channel it came through. Under
each one it prints one of three answers:

- `taken in at round 3 of task <task_id>: ...` followed by the job's restatement, which
  quotes your message and names the round it applies from, and for a mission's job also the
  contract requirement it became;
- `waiting`, when the job has not reached a safe point since the message arrived;
- `not taken in`, when the job ended before it reached another round.

Add `--json` for the same list as JSON.

The cockpit shows the same acknowledgement as its own line in the activity feed, directly
above the input: "Steering taken in at round 3: ..." followed by the same restatement.
Both views read the one event the job writes when it takes a message in, so they cannot
disagree.

## What is kept as evidence

Every message is written as a sealed record in the job's evidence folder, under
`steering/`, before the job is told about it, and a `steering_message_received` event in
the job's run log carries the record's seal. When a round takes the message in, a sealed
marker under `steering/consumed/` names the task and the round, and a
`steering_message_consumed` event records the restatement. A record whose seal no longer
matches its text stops the job loudly instead of feeding it text nobody can prove you
sent.

## Ask a question, or ask for an action

A steering message is read by the builder. The chat, built by feature F038, is for you: it
answers questions from the job's own records, and it turns a request into a card that says
exactly what would be done, which is done only when you confirm it.

    remedy chat ask <job_id> "Did the tests pass?" --task <task_id>

With `--task`, the answer comes only from that task's records: its status, its rounds, its
prompts (never their text), its changes and its events. Without it, the answer comes from the
records of the project that owns the job's repository. The output says which of the two it
used, how the answer was written, the answer itself, and one numbered line per record it read.
Every sentence of the answer ends with the numbers of the records it restates; a sentence that
cannot be traced to one is marked `[unsupported]`, and a question the records do not answer gets
the answer `Not in evidence.` rather than a guess. Answers are built from the records without a
model unless you switch on `chat.model_written`, described in
[environment.md](environment.md); a model's answer is checked in the same way.

A line that is not a question is read as a request: stop, pause, resume, a note to the builder,
veto or rerun. The command prints a card naming the job, the task, the message or reason, and the
command it would send. It sends the card to the job's running cockpit only when the card is
complete and you confirm it, either by typing `y` at the `Send it? [y/N]` line or by adding
`--yes`; without a terminal and without `--yes`, nothing is sent and the output says why. The
cockpit must be running (`remedy ui start <job_id>`), because the card goes through the same
checked entrance as a button in the browser, and its record is the cockpit's own audit line.

In the cockpit, the same chat is the Chat tab of a run's evidence panel. It asks about that
run's task, or about the whole project when you tick the box beside the input. Each sentence of
an answer carries numbered links to the records listed under it, or a dashed "unsupported"
mark, and a card has a Confirm button that sends it once.

## Exit codes

`remedy chat send` exits 0 when the message was recorded, 2 when the message itself is
unusable (empty, too long, or containing a NUL character), and 3 when the job has ended or
its record cannot be read. `remedy chat show` exits 3 when the job's record cannot be read.
`remedy chat ask` exits 0 whether or not a card was sent, 2 for a task id that names no
task of the job, 3 when the job's record cannot be read or no cockpit for the job is running
or answering, and 1 when the cockpit refuses the card. An unknown job id exits 1. The full
list is in [exit-codes.md](exit-codes.md).
