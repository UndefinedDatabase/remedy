# Handback — F281 Round 8

## Session

SESSION 1 of feature F281 · round 8 · rounds so far 8. This is the 8th delegated round of session 1, at the TOP of the operator's 6-to-8 target. The session's next action is an honest assessment of whether to continue or end.

## Range

Review of `d21b585b`..`73531f9c`.

## Commits

### 47e694b7 F281 R8 C0a: save the round 8 step block under the authored directory
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/authored/f281-r8.md | +213 | Block copy, byte-for-byte verified |

### 0337abb7 F281 R8 C0b: mirror the round 8 step block into the last block state file
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/last_block.md | +213/-452 | Block mirror, byte-for-byte verified |

### 35d231b4 F281 R8 C1: book round 7 PASS and re-point plan.md
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/live_review.md | +1 | RECORD7 append, round 7 verdict booking |
| .agent/plan.md | +65/-62 | PLAN8 rewrite, round 8 updated plan |

### 73531f9c F281 R8 C2: clear the Project bucket violations (33 fixes via 4 shared-literal edits)
| Path | +/- | Reason |
| --- | --- | --- |
| apps/cli/command_catalog.py | +13/-13 | 4 FROM/TO edits: _PROJECT_SCOPE_OPT constant (1 definition, 21 call sites fixed), "Project slug or UUID" literal (3 sites: project.current, project.attach, project.adopt), "Project UUID scope" literal (3 sites: memory.store, memory.recall, memory.list), "Project ID scope" literal (6 sites: memory.card-show, memory.card-approve, memory.card-reject, memory.card-stale, memory.card-supersede, memory.card-contradict) |

## External actions

```
git push origin feature/f281-cli-help-surface
To github.com:UndefinedDatabase/remedy.git
   d21b585b..73531f9c  feature/f281-cli-help-surface -> feature/f281-cli-help-surface
```

Exit code: 0.

## Verification

### G1: Meaning violations and synonym offenders

```
$ python3 -c "
from tests.docs.test_vocabulary import _meaning_violations, _synonym_offenders
violations = _meaning_violations()
offenders = _synonym_offenders()
print(f'_meaning_violations() = {len(violations)}')
print(f'_synonym_offenders() = {len(offenders)}')
"

_meaning_violations() = 151
_synonym_offenders() = 2
```

Exit code: 0. Expected: 151 violations (184 → 151, 33 fixed), 2 offenders (unchanged). Delta: 184 → 151, exactly matching the block's prediction (33 Project bucket fixes).

### G2: Targeted pytest tests

```
$ python3 -m pytest tests/docs/test_vocabulary.py tests/test_command_catalog.py tests/cli/test_advertised_commands.py -q

........................................................................ [ 97%]
..                                                                       [100%]
74 passed in 1.09s
```

Exit code: 0. Expected: 74 passed (unchanged).

### G3: Golden path canary tests

```
$ python3 -m pytest tests/cli/test_golden_path.py -q

..........................................                               [100%]
42 passed in 17.69s
```

Exit code: 0. Expected: 42 passed (unchanged).

### G4: Ruff linter check

```
$ python3 -m ruff check apps/cli/command_catalog.py

All checks passed!
```

Exit code: 0. Expected: All checks passed!

### G5: Sweep for new text present, old text gone

```
$ grep -c "Scope to a project's repo (slug or UUID)" apps/cli/command_catalog.py

1
```

Exit code: 0. Count of edit 1 (constant definition): 1.

```
$ grep -c "Project's repo, slug or UUID" apps/cli/command_catalog.py

3
```

Exit code: 0. Count of edit 2 (project.current, project.attach, project.adopt): 3.

```
$ grep -c "Project's repo, UUID scope" apps/cli/command_catalog.py

3
```

Exit code: 0. Count of edit 3 (memory.store, memory.recall, memory.list): 3.

```
$ grep -c "Project's repo, ID scope" apps/cli/command_catalog.py

6
```

Exit code: 0. Count of edit 4 (memory.card-*): 6.

```
$ grep -c "Project slug or UUID\|Project UUID scope\|Project ID scope" apps/cli/command_catalog.py

0
```

Exit code: 0. Old strings completely gone (all three old literals unmatched).

### G6: Tree state and worktree verification

```
$ git status --porcelain
(empty)

$ git worktree list
/home/decodeux/Repos/remedy  73531f9c [feature/f281-cli-help-surface]

$ git log --oneline -1
73531f9c F281 R8 C2: clear the Project bucket violations (33 fixes via 4 shared-literal edits)
```

Exit code: 0. Tree clean, one worktree, branch pushed to origin.

## Authored-text proofs

### C0a block copy

```
$ cmp .remedy-wt/f281-r8-block.md .agent/authored/f281-r8.md
(exit 0)

$ sha256sum .agent/authored/f281-r8.md
1db42cce3a02f9d17cc371935c6a0407c47df752fe0a224222951662d79250bd  .agent/authored/f281-r8.md
```

Exit code: 0. Block copy verified byte-for-byte identical at sha256 `1db42cce3a02f9d17cc371935c6a0407c47df752fe0a224222951662d79250bd`.

### C0b block mirror

```
$ cmp .remedy-wt/f281-r8-block.md .agent/last_block.md
(exit 0)

$ sha256sum .agent/last_block.md
1db42cce3a02f9d17cc371935c6a0407c47df752fe0a224222951662d79250bd  .agent/last_block.md
```

Exit code: 0. Block mirror verified byte-for-byte identical at sha256 `1db42cce3a02f9d17cc371935c6a0407c47df752fe0a224222951662d79250bd`.

## Deviations & assumptions

None. All 4 code edits matched the FROM text verbatim at the cited locations (1 definition, 3 + 3 + 6 = 12 call sites); all gates passed with the exact outputs predicted (G1: 151 violations and 2 offenders, 33-violation improvement from 184; G2: 74 passed; G3: 42 passed; G4: All checks passed; G5: 1 + 3 + 3 + 6 = 13 new occurrences, 0 old); the vocabulary function measurements match exactly (184 → 151 meaning violations, 2 synonym offenders unchanged, 33 total fixed: Project bucket only, per the round's scope).

## Next

Round 9: Re-run `_meaning_violations()` grouped by word at the start of round 9; expected: Project (~32) and Job (~118) are the only two buckets left (plus Order's 1 unfixed `stats.bench` collision), at approximately 150-151 total (re-measure rather than trust). Job is now by far the largest; continue looking for shared constants there first (the many `job_id` ArgDefs are the obvious candidate) before writing per-command edits.
