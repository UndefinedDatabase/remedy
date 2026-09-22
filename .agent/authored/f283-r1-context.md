# Context — F283 Machine contracts, part two: the refusal sweep, the JSON gap and the exit-code taxonomy

## Active Branch
feature/f283-machine-contracts-part-two, cut from `main` at `d0d40e89` (the
merge commit of pull request 263, F277's closure).

## Scope
F283 (Tier 2), registered by F277's split-and-close under DECISION F277 D10 and
placed directly behind its parent under amend0906-split-placement. T001 is the
refusal sweep carried over from F277's T003, verbatim and not re-planned: the
`print(...); sys.exit(...)` pairs move onto the shared `fail()`, one command
group per commit, the `--json` commands that answer a failure in prose are
fixed, and the read-only-without-`supports_json` set becomes empty. T002 is
F277's T004 whole: the exit-code taxonomy documented under `docs/guides/` and
asserted from the catalog, with `tests/cli/test_json_contract.py` sweeping
every reachable `supports_json` command on success AND on a deliberately
invalid argument. T002 lands last because its sweep is T001's acceptance
evidence.

## Do not touch
The event names and `packages/orchestration/event_names.py`: F277 declared that
vocabulary and this feature does not rename it. `apps/cli/json_envelope.py`'s
shape — the envelope, its two reserved keys and `fail`'s signature are F277's
contract, and a change to them is a new decision, not a sweep. The catalog's
command SET, which F261 owns. The nine modules F277 already migrated
(`blocker`, `change`, `contract_cmd`, `event`, `file`, `job_context_cmd`,
`memory`, `mission_cmd`, `worker`) are not re-migrated.

## Active assumptions
- A migrated site keeps the exit code it already used. The taxonomy is T002's
  work, and re-numbering a code during T001 would hide a behaviour change
  inside a rename.
- `fail()` writes the `Error: ` prefix itself, so a migrated site passes its
  message WITHOUT the prefix. That is the one transformation a reader must
  check at every site, and the existing suite asserts several of those lines
  byte-for-byte.
- A token is named for the CONDITION (DECISION F277 D8); a catch-all handler
  gets a token named for the layer that refused (DECISION F277 D9). One
  spelling per concept: `job_not_found`, `invalid_list_option`,
  `permission_denied`, `invalid_argument`, `missing_argument`, `no_project`
  and `missing_dependency` already exist and are reused, never re-spelled.

## Constraints
- `python3 -m ruff check <path>` is the spelling every gate orders.
- A round touching `docs/roadmap/**` also gates `tests/docs/` and
  `tests/orchestration/test_roadmap_index.py`.
- A new module under `packages/` reachable from the entry points must be added
  to `tests/orchestration/import_reachability_allowlist.txt` in the same
  commit, or `tests/orchestration/test_import_reachability.py` goes red.
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
