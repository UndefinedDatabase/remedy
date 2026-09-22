# Context — F278 Durable writes & loud failures

## Active Branch
feature/f278-durable-writes-loud-failures, cut from `main` at `9817a927` (the
merge commit of pull request 265, F283's closure).

## Scope
F278 (Tier 2), registered 2026-09-08 by operator order
amend0908-brainstorm-intake. T001 adds ONE path-based durable write to
`packages/common/secure_fs.py`. T002 migrates every surviving private
atomic-write helper onto it and deletes the copy (AGENTS.md, "Replacing is
deleting"), then an AST guard holds the line. T003 enables ruff's BLE001 with a
frozen ignore list and makes the F004 stream evidence writer record the step
that failed instead of swallowing it.

## Do not touch
`storage.py`'s existing `mkstemp` placement. The stream artifact's existing
fields. The BLE001 ignore list's size upward. The existing descriptor-anchored
writers in `secure_fs.py` (`write_file_atomically`, `append_line_at`,
`publish_dir_atomically`), which hold a directory fd and are a different
contract from a write by path.

## Active assumptions
- F275 has landed, so the survivor list T002 migrates is re-derived from the
  tree at the round that takes it; the feature file's 2026-09-08 counts are
  history, not a plan.
- A migrated call site keeps its return-type contract and its file mode; a
  site that relied on the umask passes the mode it used to get explicitly.

## Constraints
- `python3 -m ruff check <path>` is the spelling every gate orders.
- A round touching `docs/roadmap/**` also gates `tests/docs/` and
  `tests/orchestration/test_roadmap_index.py`.
- A new module under `packages/` reachable from the entry points is added to
  `tests/orchestration/import_reachability_allowlist.txt` in the same commit.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout, which satisfies
  `git status --porcelain` empty at every verdict.
- Per operator amendment amend0917-throughput (2026-09-17): the full pytest
  suite runs exactly once per feature, in the closure sequence's
  integration-gate round; a round runs targeted pytest files, the golden
  path, `tests/docs/` when `docs/roadmap/**` changed, and ruff.
- No finding is resolved by deleting a test, weakening an assertion or
  raising a ceiling.

This feature is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`.
