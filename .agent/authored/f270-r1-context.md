# Context — F270 History apply: one commit per task, merge on demand

## Active Branch
feature/f270-history-apply, cut from `main` at `b7f966c0` (the merge
commit of pull request 257, F269's closure).

## Scope
F270 (Tier 2). Per `docs/roadmap/features/T2_F270.md`: every applied task
lands as one commit on the job worktree branch `remedy/job-<job id>`;
`job apply --approve --commit-with-history` merges that branch into the
operator's current branch with `--no-ff`; `--commit "<message>"` and
`--commit-auto` land one commit of what apply copied; `--push` pushes the
branch committed to, once per mission; `apply.push_after_mission` makes
unattended runs push. Remedy never commits on the operator's branch
without one of those flags or that key.

## Do not touch
The apply gate's approval semantics, the snapshot guard, the worktree
lifecycle (creation, reuse, cleanup) beyond committing on it. Nothing
pushes to a branch other than the one committed to, and nothing pushes
without the operator's flag or config key.

## Constraints
- `python3 -m ruff check <path>` is the spelling every gate orders.
- A round touching `docs/roadmap/**` also gates `tests/docs/` and
  `tests/orchestration/test_roadmap_index.py`.
- A round writing a `remedy ...` command into README.md or docs/ gates
  `tests/cli/test_advertised_commands.py`.
- Destructive verification runs only inside a disposable git worktree
  under `.remedy-wt/`, never in the primary checkout, which satisfies
  `git status --porcelain` empty at every verdict.
- Per operator amendment amend0917-throughput (2026-09-17): the full
  pytest suite runs exactly once per feature, in the closure sequence's
  integration-gate round; a round runs targeted pytest files, the golden
  path, `tests/docs/` when `docs/roadmap/**` changed, and ruff.
- No test calls a real provider; `REMEDY_DATA_DIR` is set through
  `monkeypatch.setenv` or the subprocess env of the test helper.

This feature is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`.
