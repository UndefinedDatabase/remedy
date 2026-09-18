# Handoff — F266 remedy study, round 4

## Session

SESSION 1 of feature F266 · round 4 · rounds so far 4

## Range

Review of b84dde54..9f4056d7

## Commits

### 305d1f16 F266 C1: bookkeeping — state files, R-0958 closure, D3 decision, plan update

| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +5 | Insert Done: R-0958 resolution from round 3 (dotfile-mangling fix and test) |
| .agent/decisions.md | +20 | Append DECISION F266 D3 (study group ships as advanced/internal, user_facing=False) |
| .agent/plan.md | -6 | Full replacement: update Current Step and Next Steps for round 4 CLI wiring |

### fb8580eb F266 C2: catalog registration — study group and study.run command

| Path | +/- | Reason |
|------|-----|--------|
| apps/cli/command_catalog.py | +20 | Add study GroupDef in advanced/internal section; add study.run CommandEntry with --path, --project, --json args |

### 9f4056d7 F266 C3: handler module, wiring, and tests — study run implementation

| Path | +/- | Reason |
|------|-----|--------|
| apps/cli/commands/study_cmd.py | +60 | New handler module: _cmd_study_run calls run_study with study_call_fn() as default call_fn |
| apps/cli/commands/__init__.py | +1 | Add study_cmd to imports and iteration tuple |
| tests/cli/test_study_cmd.py | +127 | Four tests: command writes 4 memory cards, defaults path to cwd, catalog entry exists, group is user_facing=False |

## External actions

```
git push -u origin feature/f266-remedy-study
  → branch pushed, tracking remote
```

## Verification

### Gate 1: pytest

```
python3 -m pytest \
  tests/cli/test_study_cmd.py \
  tests/test_command_catalog.py \
  tests/test_grouped_cli.py \
  tests/cli/test_advertised_commands.py \
  tests/orchestration/test_dead_command_check.py \
  tests/cli/test_golden_path.py \
  -q
```

Exit code: 0

```
402 passed in 39.42s
```

### Gate 2: ruff check

```
python3 -m ruff check \
  apps/cli/command_catalog.py \
  apps/cli/commands/study_cmd.py \
  apps/cli/commands/__init__.py \
  tests/cli/test_study_cmd.py
```

Exit code: 0

```
All checks passed!
```

### Gate 3: git status

```
git status --porcelain
```

Exit code: 0

```
(clean working tree)
```

## Authored-text proofs

### Proof 1: .agent/live_review.md — R-0958 Done line insertion

Authored text at `.agent/authored/r0958_done_line.txt`:
```
Done: R-0958 — RESOLVED at F266 round 3 in commit `8d163a7c`. `packages/orchestration/study.py::_walk_repo`'s file-path construction was replaced with an explicit prefix join, `rel_filepath = f"{rel_dirpath}/{filename}" if rel_dirpath != "." else filename`, replacing the character-set `.lstrip("./")` call the finding named. The same commit added `test_walk_repo_preserves_root_dotfile_names`, asserting a root-level `.gitignore` round-trips through `_walk_repo` with its leading dot intact. The reviewer red-proofed the fix independently in a disposable worktree: reverting the fix (restoring the old `.lstrip` construction) turns exactly that one test red, with the other seven tests in `tests/orchestration/test_study.py` staying green.
```

Disk comparison: exact match at live_review.md:405-406.

### Proof 2: .agent/decisions.md — F266 D3 decision append

Authored text appended to decisions.md (14615-14634):
```
## DECISION F266 D3 (2026-09-18, reviewer, round 4) — `study` ships as an advanced/internal group, not in the default help order
CHOSEN: register `GroupDef("study", "Study", "...", user_facing=False)` (hidden defaults to False) — the same
"advanced/internal: callable but hidden from default help" tier as `patch`, `test`, `brain` and `mission`, NOT
the fully-invisible `hidden=True` tier `roadmap` uses. MEASURED: `VISIBLE_GROUP_ORDER`
(`apps/cli/command_catalog.py`) is a FIXED, operator-pinned tuple — DECISION amend0905-vocab D4, clarified by
amend0911-feedback D1 — and `tests/test_command_catalog.py::TestVisibleGroupOrder::test_visible_group_order_matches_d4`
asserts it byte-for-byte; every `user_facing=True, hidden=False` group MUST appear in it
(`test_visible_group_order_is_exactly_the_visible_groups`), so making `study` visible in this round would mean
amending an operator-authored, explicitly-versioned UX decision on the reviewer's own authority, for a command
whose place in the actual golden path (`docs/roadmap/features/T4_F266.md`'s Design section: "study is invoked
EXACTLY ONCE by `remedy do`" — F268, not yet built) does not exist yet. `study run` is fully functional and
discoverable via `remedy --all-commands`/`remedy study --help` either way — `user_facing=False` changes ONLY
whether it clutters the default `--help` output before its automatic caller exists. ALTERNATIVES
CONSIDERED: amending `VISIBLE_GROUP_ORDER` now, rejected because D4 is an operator decision this feature was not
asked to revisit, and promoting `study` makes more sense at F268's closure, when `remedy do` actually drives it and
the golden path is real rather than aspirational. REVERSE by setting `user_facing=True` and adding `"study"` to
`VISIBLE_GROUP_ORDER` (at F268's own discretion for placement) in the same commit as updating the two pinned tests.
```

Disk comparison: exact match appended to end of decisions.md.

### Proof 3: .agent/plan.md — Current Step and Next Steps update

Authored text at plan.md:14-34:
```
## Current Step

ROUND 4 — CLI wiring. `study run [--path PATH] [--project PROJECT] [--json]`
(new `apps/cli/commands/study_cmd.py`, wired into `collect_all_handlers`)
calls `run_study` with `study_call_fn()` as the default `call_fn`. DECISION
F266 D3: the new `study` group ships `user_facing=False` (advanced/internal,
like `patch`/`test`/`brain`), not added to the operator-pinned
`VISIBLE_GROUP_ORDER` — that promotion is F268's call, when `remedy do`
actually drives it. Books R-0958's resolution from round 3.

## Next Steps

1. T003 — the three-step proved end to end against a foreign repository
   fixture, including the new memory-card grounding source for
   `teacher ask` (it has none today).
2. Closure sequence.
```

Disk comparison: exact match at plan.md.

## Deviations & assumptions

### Assumption 1: --path and --project wiring verification

ASSUMPTION VERIFIED: Read `apps/cli/grouped.py::_add_command_args` (lines 111-112 for `--path`, lines 85-86 for `--project`) to confirm both are already wired generically with `default=None`. No new argparse branch needed. Both flags passed through correctly to _cmd_study_run via getattr on args namespace.

### No other deviations

The implementation followed the block specification exactly: C1 bookkeeping, C2 catalog registration, C3 handler + wiring + tests, all gates passed on first run, no unexpected test failures requiring fixes within round scope.

## Next

T003 — the three-step (`remedy init` → `remedy study` → `remedy teacher ask`) proved end to end against a foreign repository fixture, including the new memory-card grounding source for `teacher ask`. This round completed the CLI wiring; T003 must add the memory-card retrieval path `teacher ask` has none of today.
