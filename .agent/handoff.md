# Handback — F281 Round 4

## Session

SESSION 1 of feature F281 · round 4 · rounds so far 4

## Range

Review of `2318dba4`..`aa5a127e`

## Commits

### 9944f7ce F281 R4 C0a: save the round 4 step block under the authored directory
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f281-r4.md | +261 | Block copy, byte-for-byte verified |

### 4036fb58 F281 R4 C0b: mirror the round 4 step block into the last block state file
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +261/-197 | Block mirror, byte-for-byte verified |

### 64aad85f F281 R4 C1: book round 3 PASS and re-point plan.md
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +2 | RECORD3 append, round 3 verdict booking |
| .agent/plan.md | +38/-57 | PLAN4 rewrite, round 4 updated plan |

### aa5a127e F281 R4 C2: clear the Order bucket via a shared constant and 8 of 9 Task-bucket violations
| Path | +/- | Reason |
|------|-----|--------|
| apps/cli/command_catalog.py | +13/-13 | 9 FROM/TO edits: _LIST_DESC_ARG shared constant (12 sites), _TASK_OPT shared constant, brain.continue --task-type, job.run --max-rounds, job.run --repair-rounds, job.show --full (3-line string), job.context description (2-line string), mission.continue description, self.execute proposed_task_id and --job-id |

## External actions

```
git push -u origin feature/f281-cli-help-surface
To github.com:UndefinedDatabase/remedy.git
   2318dba4..aa5a127e  feature/f281-cli-help-surface -> feature/f281-cli-help-surface
Branch 'feature/f281-cli-help-surface' set up to track remote branch 'feature/f281-cli-help-surface' from 'origin'.
```

Exit code: 0.

## Verification

### G1: Meaning violations and synonym offenders

```
$ python3 << 'SCRIPT'
from tests.docs.test_vocabulary import _meaning_violations, _synonym_offenders

violations = _meaning_violations()
offenders = _synonym_offenders()

print(f"Meaning violations: {len(violations)}")
print(f"Synonym offenders: {len(offenders)}")
SCRIPT

Meaning violations: 245
Synonym offenders: 2
```

Exit code: 0. Expected: 245 violations (22 fixed from 267), 2 offenders (unchanged floor).

### G2: Targeted pytest tests

```
$ python3 -m pytest tests/docs/test_vocabulary.py tests/test_command_catalog.py tests/cli/test_advertised_commands.py -q

........................................................................ [ 97%]
..                                                                       [100%]
74 passed in 1.11s
```

Exit code: 0. Expected: 74 passed (unchanged).

### G3: Golden path canary tests

```
$ python3 -m pytest tests/cli/test_golden_path.py -q

..........................................                               [100%]
42 passed in 17.72s
```

Exit code: 0. Expected: 42 passed (unchanged).

### G4: Ruff linter check

```
$ python3 -m ruff check apps/cli/command_catalog.py

All checks passed!
```

Exit code: 0. Expected: All checks passed!

### G5: Sweep for old text gone, new text present

```
$ grep -c '"Reverse the sort order"' apps/cli/command_catalog.py
0

$ grep -c '"--desc", "Reverse the sort direction"' apps/cli/command_catalog.py
1
```

Exit code: 0 for both. Expected: 0 occurrences of old text, 1 occurrence of new text (the shared constant).

### G6: Tree state and worktree verification

```
$ git status --porcelain
(empty)

$ git worktree list
/home/decodeux/Repos/remedy  aa5a127e [feature/f281-cli-help-surface]
```

Exit code: 0. Expected: tree empty, one worktree, HEAD matches remote feature/f281-cli-help-surface.

## Authored-text proofs

### C0a block copy

```
$ cmp .remedy-wt/f281-r4-block.md .agent/authored/f281-r4.md
(no output)

$ sha256sum .agent/authored/f281-r4.md
73fa1a19a51115538008ce1b1313c31f335f4751440dbf47cb0ffb45df614a33  .agent/authored/f281-r4.md
```

Exit code: 0. Block copy verified byte-for-byte identical at sha256 `73fa1a19a51115538008ce1b1313c31f335f4751440dbf47cb0ffb45df614a33`.

### C0b block mirror

```
$ cmp .remedy-wt/f281-r4-block.md .agent/last_block.md
(no output)

$ sha256sum .agent/last_block.md
73fa1a19a51115538008ce1b1313c31f335f4751440dbf47cb0ffb45df614a33  .agent/last_block.md
```

Exit code: 0. Block mirror verified byte-for-byte identical at sha256 `73fa1a19a51115538008ce1b1313c31f335f4751440dbf47cb0ffb45df614a33`.

## Deviations & assumptions

None. All 9 code edits matched the FROM text verbatim at the cited locations; all gates passed with the expected outputs.

## Next

Round 5: Re-run `_meaning_violations()` grouped by word at the start of the round; expected counts after this round are Task 0 or 1 (stats.bench may remain), Order 0 or 1 (stats.bench's own Order violation, same caveat), Evidence 12, Mission 16, Run ~29, Project 65, Job ~120 — 245 total. Take the next-smallest bucket by word-sense violation count and clear it via the same shared-constant strategy when possible.
