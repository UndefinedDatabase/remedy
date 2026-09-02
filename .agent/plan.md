# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 6, round 20.

## Goal
Repair rounds stop resending the world: where the provider supports resuming
a session, a repair call resumes the original session and sends only the
findings delta, with an honest automatic fallback to full context when the
session is gone, flagged in evidence. Correctness never depends on resume
working.

## Current Step
Closure preconditions 2, 3 and 4 are MET. This round advances precondition
6 (self-use track consumption): the queue's next pending item, SU-003
("Give apps/ui's ESLint config a TypeScript parser"), is planned via
`self_use_job.plan_next_self_use_item` and RUN via
`self_use_runner.run_next_self_use_item` to the normal approval gate,
inside an isolated worktree with an isolated `REMEDY_DATA_DIR`, never
promoted, `scripts/self_use_queue.json` left byte-identical (`consumed_by`
is a closure-commit edit only). The run's real evidence is committed to
`.agent/gate_f106_r20/self_use_run.txt`. Finding registration for any
non-empty `describe_self_use_run_defects` output is deferred to round 21,
once the reviewer has read this round's real evidence and can author exact
finding text — never authored blind ahead of the run.

## Next Steps
1. Round 21: read round 20's real evidence; register any defect finding(s)
   `describe_self_use_run_defects` (or the reviewer's own reading)
   surfaced, or state explicitly that none were found.
2. Precondition 6 is MET once SU-003 has been run and any defects handled;
   `scripts/self_use_queue.json`'s `consumed_by` edit itself waits for the
   closure commit, per DECISION F257 D2.
3. Evidence job, review zip, STATUS line, PR — the closure algorithm's
   remaining steps. The closure commit also owes DECISION F106 D2's
   `.agent/candidates.md` entry (job/mission resume deferral).

## Risks
- The self-use run calls a REAL local provider (ollama, product default) —
  outcome (completed/blocked, quality of any edit) is not knowable ahead of
  time; the round records whatever it is honestly.
