## What

F288 — Event stream completeness & prompt nodes in the live graph. The live graph now shows a node
for every kind the simple view shows.

- **T001, the event fields.** An attempt is one execution of a task. Its id is minted before
  `task_run_started` and handed to the ping-pong as its run id, so the id every event carries is the
  run id every prompt names. `run_job` writes `task_round_repaired` and `task_round_tested` per round;
  the run-next path, the test service (whose attempt id is its test run id) and the long-run cycles
  (`cycle-<index>`) carry the attempt id, the task id and the result as `outcome`. A new
  `plan_approved` event names the approved plan's task ids after a human or an unattended approval.
  The stream's envelope adds `attempt_id` for the 19 kinds of `ATTEMPT_EVENT_KINDS` and a `plan`
  block for `plan_approved`; every other frame is byte-identical. Every reader of the vocabulary is
  updated: `EVENT_NAMES`, the humanized catalog, the narration, `remedy event timeline` and the
  architecture doc.
- **T002, the reducer.** Rows carry `attemptId` and `planTaskIds`; the live graph births the plan's
  tasks at plan approval, a test-run node per tested round and per linked test run, and a repair-run
  node per repair round, each under its task with its attempt in its meta. The demo recording was
  captured again from the widened stream (R-1075).
- **T003, prompt nodes.** A prompt is a `synapse` node composed from the dashboard's prompt trace
  onto the live model only (`promptNodes.ts`); a click selects the prompt itself. The keyboard reaches
  the prompts through `PromptNodeList`, a list of native buttons hidden until it holds focus, while
  the canvas stays `aria-hidden`.

## Why

F019 built the live graph without changing the message format, so tasks appeared late, test runs and
repairs had no nodes, and the prompt dots stayed in the simple view. The operator asked for the
missing fields and prompt nodes as their own feature (operator questions Q2 and Q3).

## Key decisions (in `.agent/decisions.md`)

- F288 D1 — the attempt and its id, the round events, the envelope's attempt kinds.
- F288 D2 — the run-next path, the test service's attempts, the `plan_approved` event.
- F288 D3 — the long-run cycle's attempt, the row fields, what the reducer births and from which event.
- F288 D4 — R-1075's fix reaches every reader of the recaptured demo recording.
- F288 D5 — prompts as `synapse` nodes of the live model, a child of their task.
- F288 D6 — the keyboard's parallel list and the headless-browser proof.

## How to review

Start with `packages/orchestration/pingpong_job.py` (`run_job`) and `_safe_event_summary` in
`packages/orchestration/ui_server.py`, then `applyBrainEvent` in
`apps/ui/src/components/graph/brainReducer.ts`, then `withPromptNodes` in `promptNodes.ts` and
`PromptNodeList.tsx`. The Built State of `docs/roadmap/features/T5_F288.md` names the test for each
acceptance line. Each building round's mutation tool is `.agent/authored/f288-r<n>-mutations.py`;
`.agent/authored/f288-r6-render_measure.py` renders the live graph and the prompt list in headless
Chrome.

## Changed files

59 files outside `.agent/` against the fork point `db691093`, counted by `git diff --name-only`
before the closure commit plus `README.md`: 12 under `packages/` and `apps/cli/` for the events, 25
under `apps/ui/` for the rows, the reducer, the prompt nodes and their vitest suites, 15 Python test
files under `tests/`, and 7 others — `docs/system/architecture.md`, the feature file,
`docs/guides/remedy-toml-user-guide.md` from the self-use run, the checklist's consolidation
paragraph in `docs/agents/planner_reviewer_prompt.md`, and `docs/roadmap/STATUS.md`, `README.md`
and `scripts/self_use_queue.json`. `git diff --stat db691093..HEAD` lists them.

## Verification

- The one full suite on the tree that ships: `19813 passed, 20 skipped` at exit 0, no bad node
  (`.agent/authored/f288-closure-suite.txt`).
- The headless-Chrome proof: the list hidden before focus, Tab reaching it, Enter and Space selecting
  the first and second prompts, and a synapse drawn per entry (`.agent/authored/f288-r6-render.txt`).
- The closure's self-use item `SU-034`, from the documentation-staleness catalog: job
  `8356faebdc904fd1` on `claude-cli` added the missing `remedy config show` row to the `remedy.toml`
  guide in 2 calls for 1.07 USD, its reviewer passed it, and the one line landed verbatim.
- Evidence job `f288r9e1001` against the fork point `db691093`: 1367 selected tests passed at exit 0.
- Review package `remedy-review-20260927-060235-READY_FOR_REVIEW.zip`, SHA-256
  `184f155676e7fdfc8bdf8f2db736ed0b96b127f84fb3873580fefe38c10373d2`, READY_FOR_REVIEW.

## Findings and notes

Latest verdict PASS; accepted PASS. F288 registered R-1075 and resolved it. No finding is open. The
self-use job left the branch `remedy/job-8356faebdc904fd1`, which the operator may delete.

## Runtime actuals

Ten rounds in two sessions, from the branch's first commit at 00:07 to the accepted head at 05:58 on
2026-09-27; reviewer and workers ran as Claude Opus 5.5; the self-use run cost 1.07 USD; other tokens
not measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
