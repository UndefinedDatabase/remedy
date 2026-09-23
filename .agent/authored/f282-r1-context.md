# Context — F282 Findings paydown v2

## Active Branch
feature/f282-findings-paydown-v2, cut from `main` at `b8fa02ba`
(the merge commit of pull request 269, amend0923-selfuse-write).

## Scope
F282 (Tier 2), registered 2026-09-19 by F273's closure under operator
amendment amend0911-feedback rule B, the rolling findings paydown. It
repairs the open findings each by the fix its own text names, one slice
per module, as `docs/roadmap/features/T2_F282.md` lists them; its soft
limit is 8 sessions, after which it closes and carries the rest.

## Do not touch
The resolutions earlier features landed: the record is append-only. The
approval gate, and the reviewer's write mode in
`packages/orchestration/pingpong_loop.py`.

## Active assumptions
- A finding's own FIX clause is its spec; a repair that needs a ruling the
  clause does not give is recorded as a dated DECISION F282 D<n>.
- A resolution by evidence alone names the commit or hosted run it read.

## Constraints
- `python3 -m ruff check <path>` is the spelling every gate orders.
- A round touching `docs/roadmap/**` also gates `tests/docs/` and
  `tests/orchestration/test_roadmap_index.py`.
- A new `# noqa: BLE001` handler is never added: `tests/test_ble001_ratchet.py`
  holds the count at its frozen ceiling, so a handler names what it catches.
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
