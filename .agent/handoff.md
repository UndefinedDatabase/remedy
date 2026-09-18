# Handoff — F266 Round 6

## Session

SESSION 1 of feature F266 · round 6 · rounds so far 6

## Range

Review of 7490d152..01f52cc9

## Commits

### 09ecdea5 F266 C1: bookkeeping — state file, plan update
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | 15 | Updated plan for round 6: SOURCE_STUDY implementation |

### 25b5112f F266 C2: teacher_qa.py — add SOURCE_STUDY grounding source
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/teacher_qa.py` | 11 | Added SOURCE_STUDY, updated GROUNDING_SOURCES, added honesty rule, added study_cards parameter to build_teacher_context() |
| `docs/agents/teacher_conventions.md` | 6 | Updated grounding sources section to describe the fourth source (repository comprehension cards) |
| `tests/orchestration/test_teacher_qa.py` | 20 | Added 4 tests: study cards in facts, no study facts when empty, study block in prompt, GROUNDING_SOURCES order |

### 3cb2d3b1 F266 C3: ask_teacher — thread study_cards parameter through
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/teacher_model.py` | 2 | Added study_cards parameter to ask_teacher(), pass through to build_teacher_context() |
| `tests/orchestration/test_teacher_model.py` | 14 | Added test verifying study_cards reach the rendered prompt |

### 01f52cc9 F266 C4: _cmd_teacher_ask — fetch and dedupe study cards from memory
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/commands/teacher_cmd.py` | 21 | Added study card fetching and deduplication logic, pass to both contexts |
| `tests/cli/test_teacher_cmd.py` | 95 | Added 3 tests: grounds from cards, dedupes keeping newest, omits source when empty |
| `tests/orchestration/test_teacher_qa.py` | 5 | Fixed test to include study cards when testing all grounding sources |

## External actions

```
git push origin feature/f266-remedy-study
To github.com:UndefinedDatabase/remedy.git
   7490d152..01f52cc9  feature/f266-remedy-study -> feature/f266-remedy-study
```

## Verification

Gate 1: python3 -m pytest tests/orchestration/test_teacher_qa.py tests/orchestration/test_teacher_model.py tests/cli/test_teacher_cmd.py tests/orchestration/test_role_conventions.py tests/cli/test_golden_path.py -q

Exit code: 0

```
........................................................................ [ 48%]
........................................................................ [ 97%]
...                                                                      [100%]
147 passed in 18.16s
```

Gate 2: python3 -m ruff check packages/orchestration/teacher_qa.py packages/orchestration/teacher_model.py apps/cli/commands/teacher_cmd.py

Exit code: 0

```
All checks passed!
```

Gate 3: git status --porcelain

Exit code: 0

```
(clean)
```

## Authored-text proofs

`.agent/plan.md` replacement (C1): Disk-to-disk comparison verified. Full replacement applied, read back from disk confirming all lines match the block in the plan.

`docs/agents/teacher_conventions.md` edit (C2): Token estimate after edit: 527 tokens (under 800-token cap, CONVENTIONS_TOKEN_CAP verified in tests/orchestration/test_role_conventions.py).

## Deviations & assumptions

None. All four commits follow the plan. Implementation complete: SOURCE_STUDY added as fourth grounding source, threaded through ask_teacher, and integrated into _cmd_teacher_ask CLI command with deduplication logic keeping the newest value per key.

## Next

T003 — the three-step proved end to end against a foreign repository fixture: `study run` then `teacher ask` genuinely answering from what it found, plus closure sequence.
