# Context — F271 No more legacy: ownership, reachability, replace-is-delete

## Active Branch
feature/f271-no-more-legacy, cut from `main` at `a4f79a94` (the merge
commit of pull request 258, F270's closure).

## Scope
F271 (Tier 2). Per `docs/roadmap/features/T2_F271.md` and DECISION
amend0905-vocab D11: every command group in the catalog names its owning
feature and its reach, and a catalog test refuses a group without both; a
feature that replaces a mechanism deletes it in the same closure sequence
(the AGENTS.md rule "Replacing is deleting", cited, not restated); a test
fails on any module no product path imports; `remedy doctor core` lists
dead commands as a section.

## Do not touch
The reachability allowlist's content beyond what F260 decided (widening
it is a feature-file statement, not a test edit), the dead-model check
itself, the catalog's command set (F261 owns it).

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
- A deletion is one commit with its grep-to-zero proof; no stub, no copy.

This feature is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`.
