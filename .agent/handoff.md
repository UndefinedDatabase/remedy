# Handoff — F266 T001 Round 3

## Session

SESSION 1 of feature F266 · round 3 · rounds so far 3

## Range

Review of f9b98015..cce0b48f

## Commits

### 2bf53622 F266 T001 C1: update state files for round 3
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +1 line | Register R-0958 defect (root-level dotfile name mangling in _walk_repo) |
| .agent/plan.md | ±5 lines | Rewrite to describe round 3 work (fix R-0958 + study provider bridge) |

### 8d163a7c F266 T001 C2: fix R-0958 dotfile mangling bug
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/study.py | +2, -1 | Replace `lstrip("./")` with explicit prefix join to preserve root dotfiles like .gitignore |
| tests/orchestration/test_study.py | +12, -1 | Add regression test for root-level dotfile round-trip through _walk_repo |

### cce0b48f F266 T001 C3: land the study provider bridge
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/study.py | +31, -0 | Add StudyCategoryNarration schema and study_call_fn() function |
| packages/orchestration/model_routing.py | +1, -0 | Add ("packages/orchestration/study.py", "study") to ROLE_CONFIG_CALL_SITES tuple |
| tests/orchestration/test_study.py | +23, -0 | Add two tests: study_call_fn returns None without Ollama, returns callable with Ollama |
| tests/orchestration/test_model_routing.py | +2, -2 | Update call-site count assertions: 8 total (was 7), 3 literal roles (was 2) |

## External actions

Push: `git push -u origin feature/f266-remedy-study` — updated remote branch to cce0b48f

## Verification

### pytest gates (command, exit code, trimmed output)

```bash
python3 -m pytest tests/orchestration/test_study.py tests/orchestration/test_model_routing.py tests/cli/test_golden_path.py -q
```

Exit code: 0

```
460 passed, 3 skipped, 1 warning in 20.69s
```

(Full output includes all test progress and one expected UserWarning about undeclared role in test_model_routing.py)

### ruff gates (command, exit code)

```bash
python3 -m ruff check packages/orchestration/study.py packages/orchestration/model_routing.py tests/orchestration/test_study.py tests/orchestration/test_model_routing.py
```

Exit code: 0

```
All checks passed!
```

### git status (command, exit code)

```bash
git status --porcelain
```

Exit code: 0, output: (empty — clean working tree)

## Authored-text proofs

R-0958 finding in `.agent/live_review.md` (C1 Edit 1):
- Confirmed: `grep -c "R-0958"` returned 1 (exactly once)
- Added immediately before `## Triage 2026-09-06 — routing for the findings that stay open` heading
- Full defect description matches specification: low severity, dotfile mangling in _walk_repo via lstrip, fix uses explicit prefix join, regression test asserts .gitignore round-trip

`.agent/plan.md` line count (C1 Edit 2):
- File is 39 lines, under 50-line requirement
- Content: ROUND 3 phrasing, R-0958 fix, StudyCategoryNarration and study_call_fn() naming, ROLE_CONFIG_CALL_SITES inventory entry, Next steps correct

## Deviations & assumptions

None. Block executed as specified. Three commits (C1, C2, C3) plus this handoff commit (C4) complete round 3.

## Next

CLI wiring — add standalone `study` command in the catalog with `study_call_fn()` as default `call_fn` and catalog descriptor entry (resolves study role configuration).
