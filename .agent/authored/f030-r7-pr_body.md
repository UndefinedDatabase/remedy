## What

F030 — Steering messages. A note typed while a job runs reaches the one task it is meant for: that
task reads it at the start of its next round, never inside a call to a model, as a binding operator
note; the feed shows the note as the operator's own line and the builder's next action as the only
answer; and a note whose task finished first is reported as not taken in. F030 builds on F264's
steering channel instead of adding a second one.

- **T001, the address, the drain, the segment and the report.** `packages/orchestration/steering.py`:
  a steering message may carry a `task_id`, and only that task's round consumes it, never amending a
  mission's contract; `packages/orchestration/pingpong_loop.py` carries the task's consumed notes in
  ONE segment, `builder_operator_notes`, at the steering rank, numbered and verbatim, in every later
  round of the task; `export_job_report` and the text report list a note its task finished without.
- **T002, the command.** One function, `steer_task_command`, answers both doors and refuses an
  unusable text, an ended job, an unknown task and a task that will not run again; the command line
  is `remedy job steer` with `--task`, and the write door's command is the same catalog id,
  `job.steer`; `remedy chat show` names each note's task and says when it was not taken in.
- **T003, the feed, the input and the proof.** A received note's stream frame carries its text; the
  feed shows it as the operator's line with a "Y" disc named "You"; the input sends `job.steer` for
  the task selected in the graph and stays job-wide otherwise, and its copy promises a note read at
  the next round, never a reply. A live end-to-end test holds a real job's build call in flight,
  posts a note through the write door, and reads it in round 2's trace and in the stream, and a
  second scenario shows a note whose task passed first reported as not taken in.

## Why

T5_F030 asks for a note that reaches the next round of the task it addresses without interrupting a
call, a feed that shows it without inventing a conversation, and an honest account of a note that
arrived too late. F264 had already built the job-wide channel, so F030 gives it a task address.

## Key decisions (in `.agent/decisions.md`)

- F030 D1 — a note is F264's steering message with a task address; the drain, the segment, the
  report; no second inbox and no new event name.
- F030 D2 — `job.steer`, one id on both doors, one shared command, the task state gate, the exit
  codes and `chat show`.
- F030 D3 — the stream's `note`, the operator's own row, the selected task reaching the input, and
  the copy and framing that promise no reply.

## How to review

Start with `packages/orchestration/steering.py` (`record_steering_message`,
`consume_pending_steering`, `render_operator_notes_segment`, `steer_task_command`,
`steering_overview`), then `_operator_notes_text_for_round` and the `builder_operator_notes`
registration in `packages/orchestration/pingpong_loop.py`, `_task_steering_not_consumed_map` in
`packages/orchestration/pingpong_job.py`, `apps/cli/commands/job_steer_cmd.py`, the `job.steer`
branch and `_steering_note_summary_payload` in `packages/orchestration/ui_server.py`, and
`apps/ui/src/api/steeringNote.ts`, `steeringSend.ts` and `components/panels/ActivityFeedCard.tsx`.
The Built State of `docs/roadmap/features/T5_F030.md` names the test for each acceptance line; the
live proof is `tests/ui_server/test_steering_note_e2e_live.py`. Each building round's mutation tool
is `.agent/authored/f030-r<n>-mutations.py`.

## Changed files

36 files outside `.agent/` against the fork point `15f5d384`, counted by `git diff --name-only`
before the closure commit plus `README.md`: 8 under `packages/` and `apps/cli/`, 12 under `apps/ui/`
for the note and send modules, the feed card, the input, the panel, the shell and their vitest
suites, 10 under `tests/` — 9 Python test files and the import-reachability allowlist — and 6
others — `docs/guides/exit-codes.md`, `docs/ui/design_reference/assumption_log.md`, the feature
file, the checklist's consolidation paragraph in `docs/agents/planner_reviewer_prompt.md`,
`docs/roadmap/STATUS.md` and `README.md`. `git diff --stat 15f5d384..HEAD` lists them.

## Verification

- The one full suite on the tree that ships: `20184 passed, 20 skipped` at exit 0, no bad node
  (`.agent/authored/f030-closure-suite.txt`).
- The reviewer's headless-Chrome render of the feed card at round 3: the note as the operator's
  own row, both placeholders, the tooltip, and a focused and an unfocused send.
- The closure's self-use item: none — the queue held no pending item and the generator found no
  source (`self-use NONE (queue exhausted)`).
- Evidence job `f030r6e1001` against the fork point `15f5d384`: 1251 selected tests passed at exit 0.
- Review package `remedy-review-20260927-234033-READY_FOR_REVIEW.zip`, SHA-256
  `8b7e2f9ceaee61acc87a55ae5bd2c2b3f467b44ab3136076e34d5b3b666ea452`, READY_FOR_REVIEW.

## Findings and notes

Latest verdict PASS; accepted PASS. F030 registered no finding. No finding is open.

## Runtime actuals

Seven rounds in one session, from the branch's first commit at 21:29 to the accepted head at 23:38
on 2026-09-27; reviewer and workers ran as Claude Opus 5.5; tokens and cost not measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
