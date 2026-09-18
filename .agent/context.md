# Context — F281 CLI help surface

## Active Branch
feature/f281-cli-help-surface, cut from `main` at
`c617dd74df26b8e677161b265a88d5926f4d78ab`, the merge commit of pull request 253
(F280's closure).

## Scope
F281 (Tier 2; depends on F280): T001 carries whole, verbatim, F280's own T002
(itself F261's old T004) — catalog descriptions, role labels, help wrapping, the
D11a catalog test, the D11d doctor check, the F259 enforced flip, the
D4/amend0911-feedback visible group order, and the README quickstart. Task
slicing per `docs/roadmap/features/T2_F281.md`'s Orchestrator brief: descriptions
and role labels first, then help wrap and `doctor core`, then the visible-order
test and the F259 enforced flip, the README quickstart last.

## Do not touch
The concept model (F259 owns the words), the job model (F260), STATUS
semantics, and behaviour behind a name: this feature rewrites what help says,
not what a command does. The catalog's set of groups and commands is F280's;
this feature changes NO COMMAND ID — see the open scope question in
`.agent/plan.md` about `dev.agent-loop`'s own command_id colliding with this
rule.

## Assumptions
- "Builder"/"Reviewer" is the role-label pairing DECISION amend0905-vocab D1
  names; every production "Worker:" print that means the BUILDER role (not the
  `worker` command group's own adapter/process noun) becomes "Builder:" — see
  DECISION F281 D1 for the full site-by-site boundary.
- Cleanliness before compatibility (DECISION D-A of
  `docs/roadmap/features/T2_F261.md`): no alias, no migration shim.

## Constraints
The bullets below are STANDING project constraints, carried forward from F280's
context file.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree, never in
  the primary checkout, which satisfies `git status --porcelain` empty at every
  verdict.
- Bare `ruff` is DENIED to this session's shell; `python3 -m ruff check <path>`
  is the spelling every gate of this feature orders.
- `remedy` (the built CLI) may or may not be denied to this session's reviewer
  — try the binary once before falling back to `python3 -m apps.cli.main` or
  the disk-fallback route.
- The shell guard refuses shell loops, `$(...)` substitution and `$?` inside a
  compound command; such checks are written in Python.
- The editable install resolves `apps` and `packages` to the PRIMARY checkout,
  so a test run inside a worktree proves where its modules loaded from before
  its result is read.
- A fresh worktree has neither `apps/ui/node_modules` nor a built
  `apps/ui/dist`.
- Never call `run_job` or any runner from inside a checkout: a job run creates
  a `remedy/job-*` branch there.
- Per operator amendment amend0917-throughput (2026-09-17): the full suite runs
  exactly once per feature, in the closure sequence's integration-gate round;
  no round block may order it. A round's verification is targeted tests plus
  `tests/cli/test_golden_path.py`, `tests/docs/` when `docs/roadmap/**`
  changed, and `ruff check` on touched files. A round orders at most six
  gates; the plan slice, verdict booking, prose-slip lines and any DECISION
  land in ONE commit.

This feature is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`.
