## What

F029 — Subtree rerun. "Do that part again" is safe and cheap: a rerun from a task in the middle of a
job resets that task and everything depending on it to its state before the task, proved by tree
hashes, keeps every earlier attempt as evidence, and may run with a model override that the evidence
and the report record.

- **T001, the reset.** `packages/orchestration/subtree_rerun.py`: a task's commit on the job branch is
  the per-task ref; the subtree is the task and everything depending on it; the reset is ONE new
  commit that puts back exactly the paths the subtree changed, refused for a moved or dirty worktree
  and for interleaving work outside the subtree, which it names; the reset proves its tree against
  the tree before the task.
- **T002, the preparation and the command.** `prepare_subtree_rerun` re-adds a completed job's
  worktree, resets the subtree, keeps each task's finished attempt in its new `attempts` list, moves
  its stream evidence aside unchanged and records the override; `run_job` passes a task's override to
  the builder. `remedy job rerun-subtree` prices the subtree through the cost preview first and names
  the `remedy job run` command that runs it.
- **T003, the surfaces and the proof.** The write door's `job.rerun-subtree` answers
  `needs_confirmation` with the estimate and prepares only with `confirm_cost`; the run-log event
  `subtree_rerun_prepared`; the dashboard's `attempt` and `attempts`; the `attempt <n>` canvas chip
  and the Attempts list in the detail popover; the run detail's Rerun control with its model field
  and its cost confirmation; the report's ` — attempt <n>, run on <model>` clause; and a rerun of a
  mission's job noted in the mission's dossier. A live end-to-end test runs a job, reruns its middle
  task through the door and through `--yes`, runs the subtree again and reads both attempts back.

## Why

T5_F029 asks for a mid-job rerun that restores the exact pre-task state and keeps its history: the
reset is one addressable commit instead of a stash, earlier attempts are never rewritten, and the
cost preview gates the canonical expensive action.

## Key decisions (in `.agent/decisions.md`)

- F029 D1 — the task's commit is the per-task ref; the reset is one proved commit; the refusals.
- F029 D2 — prepare, then run; admission, the fold, the moved stream evidence, the per-task override.
- F029 D3 — `remedy job rerun-subtree`, its estimate from the plan bands and the cost preview.
- F029 D4 — the door command, `needs_confirmation`, the event and the dashboard's attempts.
- F029 D5 — the `attempt <n>` chip and the Attempts list.
- F029 D6 — the Rerun control, its sentences and the report's attempt clause.
- F029 D7 — a rerun of a mission's job noted in the mission's dossier.

## How to review

Start with `packages/orchestration/subtree_rerun.py` (`plan_subtree_reset`, `apply_subtree_reset`,
`prepare_subtree_rerun`, `rerun_subtree_command`), then the `model_override` line of `run_job` in
`packages/orchestration/pingpong_job.py`, `apps/cli/commands/job_rerun_cmd.py`,
`_dispatch_rerun_subtree` in `packages/orchestration/ui_server.py`, and
`apps/ui/src/components/graph/RunDetailPopover.tsx` with `apps/ui/src/api/rerunSend.ts`. The Built
State of `docs/roadmap/features/T5_F029.md` names the test for each acceptance line; the live proof
is `tests/ui_server/test_subtree_rerun_e2e_live.py`. Each building round's mutation tool is
`.agent/authored/f029-r<n>-mutations.py`.

## Changed files

49 files outside `.agent/` against the fork point `b2863af4`, counted by `git diff --name-only`
before the closure commit plus `README.md`: 9 under `packages/` and `apps/cli/`, 21 under `apps/ui/`
for the send and view modules, the attempt list, the Rerun control, the canvas chip and their vitest
suites, 13 under `tests/` — 12 Python test files and the import-reachability allowlist — and 6
others — `docs/guides/exit-codes.md`, `docs/ui/design_reference/assumption_log.md`, the feature
file, the checklist's consolidation paragraph in `docs/agents/planner_reviewer_prompt.md`,
`docs/roadmap/STATUS.md` and `README.md`. `git diff --stat b2863af4..HEAD` lists them.

## Verification

- The one full suite on the tree that ships: `20118 passed, 20 skipped` at exit 0, no bad node
  (`.agent/authored/f029-closure-suite.txt`).
- The reviewer's headless-Chrome renders of the Attempts list, the Rerun control and its
  confirmation row at rounds 5, 6 and 7.
- The closure's self-use item: none — the queue held no pending item and the generator found no
  source (`self-use NONE (queue exhausted)`).
- Evidence job `f029r10e1001` against the fork point `b2863af4`: 1286 selected tests passed at exit 0.
- Review package `remedy-review-20260927-201630-READY_FOR_REVIEW.zip`, SHA-256
  `9a0d0eb2ac1576e96149aca426e6aec301eedc6247c9ee0fb0b4a8eb01e9bf4b`, READY_FOR_REVIEW.

## Findings and notes

Latest verdict PASS; accepted PASS. F029 registered R-1080 and R-1081 and resolved both. No finding
is open.

## Runtime actuals

Eleven rounds in two sessions, from the branch's first commit at 14:25 to the accepted head at 20:13
on 2026-09-27; reviewer and workers ran as Claude Opus 5.5; tokens and cost not measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
