# Context — F269 Contract & contract templates

## Active Branch
feature/f269-contract, cut from `main` at `0955dd4c` (the merge commit of
pull request 256, F268's closure).

## Scope
F269 (Tier 2). Per `docs/roadmap/features/T2_F269.md`: a mission's
contract is its acceptance criteria, compiled to checks by F061's DoD
compiler, gated one level above the job gate by `dod_gate.py`, seeded by
one of four templates under `docs/contracts/`, amended by later operator
messages, and answered at budget end by a remainder proposal. A job's
contract is the derived slice for that job.

## Do not touch
F061's check kinds and runners, F031's inbox contract, F264's channel
(this feature gives it a shape, not a route), F072's renderer. No second
DoD mechanism: the compiler and the gate are F061's, called.

## Constraints
- `python3 -m ruff check <path>` is the spelling every gate orders.
- A round touching `docs/roadmap/**` also gates `tests/docs/` and
  `tests/orchestration/test_roadmap_index.py`.
- A new module reached from a CLI entry point changes what
  `tests/orchestration/test_import_reachability.py` measures; its
  allowlist is regenerated from `reachable_closure()`, never hand-edited.
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
