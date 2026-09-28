## What

F035 — Ownership ledger. Every job now answers "who decided what": one ledger per job lists every
human-attributable action, who acted and through which door, when, in their own words, and what it
caused, and every choice Remedy made by itself is attributed to Remedy under the job's
configuration. The ledger is a pure pass over records earlier features already write; F035 changes
none of them.

- **T001, the ledger.** `packages/orchestration/ownership.py`: `build_ownership_ledger` reads one
  job's vetoes and their replan answers, confirmed injections, subtree reruns, plan and runtime task
  edits, steering messages and task notes, pause, resume, stop and approval events, decided hunks,
  answered decisions, resolved clarifications and a rejected plan, and answers entries of one
  checked shape (`ownership_entry_problems`). The actor names the door and never more: `browser`
  with a token number, `cockpit`, `ui`, `cli`, `auto_approved` for an unattended `--yes`,
  `default_policy`, or `remedy`. A decorator on `run_job` in `packages/orchestration/pingpong_job.py`
  saves `ownership.json` into the job's evidence after every return, logging and never raising on a
  failure.
- **T002, the sentences.** `packages/orchestration/ownership_phrases.py` is the one catalog that
  words an entry in the dialect "you did X", quoting every reason, answer and note verbatim. The
  job report gains an `Ownership:` section in place of the per-task `Vetoed by` line, and the
  digest's `ownership` key, empty since F040, carries the same sentences.
- **T003, the surfaces.** `remedy job ownership <job_id> [--json]`
  (`apps/cli/commands/job_ownership_cmd.py`) and the read route `/api/jobs/<id>/ownership` share
  one view; `apps/ui/src/api/ownership.ts` decodes it whole or not at all; the task detail shows a
  "Who did what" section and the evidence panel a fourth tab, "Ownership", for the whole job.

## Why

T5_F035 asks that who decided what stays answerable after the run. Every decision door built so far
already records its own act; F035 joins them into one account instead of adding a second audit.

## Key decisions (in `.agent/decisions.md`)

- F035 D1 — a pure pass over existing records; the actor names the door, never a person; the
  command audit is not joined.
- F035 D2 — the ledger is written at the end of every `run_job` by one decorator; a failure is
  logged, never raised.
- F035 D3 — one phrase catalog, the report's Ownership section and the digest's `ownership` key.
- F035 D4 — the command and the route share one view, and plan edits read in plain verbs.
- F035 D5 — the task detail's "Who did what" section; it corrects D4's exit code.
- F035 D6 — the evidence panel's Ownership tab, and the headless render that proves both views.
- F035 D7 and D8 — the live end-to-end proof through both doors; D8 corrects D7's wording of the
  browser's job-wide steering message.

## How to review

Start with `build_ownership_ledger` and `ownership_entry_problems` in
`packages/orchestration/ownership.py`, then `ownership_sentence` and `ownership_view` in
`packages/orchestration/ownership_phrases.py`, the `run_job` decorator in
`packages/orchestration/pingpong_job.py`, the digest in `packages/orchestration/job_digest.py`,
`apps/cli/commands/job_ownership_cmd.py`, the route in `packages/orchestration/ui_server.py`, and
`apps/ui/src/api/ownership.ts`, `components/detail/DetailPopover.tsx`,
`components/graph/EvidencePanel.tsx` and `components/shell/RemedyShell.tsx`. The Built State of
`docs/roadmap/features/T5_F035.md` names the test for each acceptance line; the live proof is
`tests/ui_server/test_ownership_e2e_live.py`. Each building round's mutation tool is
`.agent/authored/f035-r<n>-mutations.py`.

## Changed files

40 files outside `.agent/` against the fork point `a0b287a5`, counted by `git diff --name-only`
before the closure commit plus `README.md`: 8 under `packages/` and `apps/cli/`, 13 under `apps/ui/`
for the ownership decoder, the task detail, the evidence panel, the shell and their vitest suites,
13 under `tests/` — 11 Python test files, the sentence golden and the import-reachability
allowlist — and 6 others — `docs/guides/exit-codes.md`,
`docs/ui/design_reference/assumption_log.md`, the feature file, the checklist's consolidation
paragraph in `docs/agents/planner_reviewer_prompt.md`, `docs/roadmap/STATUS.md` and `README.md`.
`git diff --stat a0b287a5..HEAD` lists them.

## Verification

- The one full suite on the tree that ships: `20294 passed, 20 skipped` at exit 0, no bad node
  (`.agent/authored/f035-closure-suite.txt`).
- The reviewer's headless-Chrome render of the task detail's section and the evidence panel's tab,
  seven checks (`.agent/authored/f035-r7-render_*`).
- The closure's self-use item: none — the queue held no pending item and the generator found no
  source (`self-use NONE (queue exhausted)`).
- Evidence job `f035r9e1001` against the fork point `a0b287a5`: 1068 selected tests passed at exit 0.
- Review package `remedy-review-20260928-050815-READY_FOR_REVIEW.zip`, SHA-256
  `9b3e3841d2c11725c8a03579fa2a7d5dcb963aac3386faeb5a6ab5517ac2b8aa`, READY_FOR_REVIEW.

## Findings and notes

Latest verdict PASS; accepted PASS. F035 registered five Low findings, R-1082 to R-1086, all its
own and all repaired inside it with a red-proof. No finding is open.

## Runtime actuals

Ten rounds in two sessions, from the branch's first commit at 00:58 to the accepted head at 05:04
on 2026-09-28; reviewer and workers ran as Claude Opus 5.5; tokens and cost not measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
