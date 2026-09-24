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

## Exit codes

`remedy chat send` exits 0 when the message was recorded, 2 when the message itself is
unusable (empty, too long, or containing a NUL character), and 3 when the job has ended or
its record cannot be read. `remedy chat show` exits 3 when the job's record cannot be read.
An unknown job id exits 1. The full list is in [exit-codes.md](exit-codes.md).
