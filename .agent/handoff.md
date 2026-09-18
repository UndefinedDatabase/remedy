# Handoff — F266 remedy study

## Session

SESSION 1 of feature F266 · round 2 · rounds so far 2

## Range

Review of 23ebf914..0e72585d

## Commits

### 408cef08 F266 T001 C1: bounded repository comprehension pass
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/study.py | +267 | Module implementing run_study: STUDY_EXCLUDE_DIRS frozenset, STUDY_CATEGORIES tuple, DEFAULT_MAX_ENTRIES constant, _walk_repo bounded walk with BEFORE cap checks, _detect_entry_points finder, _detect_conventions detector, StudyResult dataclass, run_study main function with job_id synthesis, heuristic computation, optional call_fn with should_stop/BudgetCounters budget guard, memory card writes with provenance="machine-study" |

### 5288a53c F266 T001 C2: study pass tests
| Path | +/- | Reason |
|------|-----|--------|
| tests/orchestration/test_study.py | +197 | Five test cases covering four-category card writing with provenance and auto-approval end-to-end, entry-cap enforcement with partial result reporting, read-only property via hash-tree before/after comparison, provider-call budget enforcement with heuristic fallback, call_fn exception handling with fallback to heuristic exact match |

### 0e72585d F266 T001 C3: update plan.md
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +15/-15 | Full replacement per handback_template.md: Current Step now describes ROUND 2 completion (T001 bounded comprehension pass); Next Steps reordered (CLI wiring, T003 end-to-end, closure) |

## External actions

- `git push -u origin feature/f266-remedy-study`: Pushed 3 commits (408cef08..0e72585d) to remote, branch already tracked origin/feature/f266-remedy-study.

## Verification

**Gate 1: python3 -m pytest tests/orchestration/test_study.py tests/cli/test_golden_path.py -q**

```
Exit code: 0
47 passed in 17.66s
```

**Gate 2: python3 -m ruff check packages/orchestration/study.py tests/orchestration/test_study.py**

```
Exit code: 0
All checks passed!
```

**Gate 3: git status --porcelain**

```
Exit code: 0
(no output — working tree clean)
```

## Authored-text proofs

Plan.md replacement (per handback_template.md, no line cap enforcement):
- Disk file line count: 39 lines (well under 50-line target for state files)
- Head verification (lines 1-5):
  ```
  # Plan — F266 remedy study (repo comprehension pass)
  
  Branch: feature/f266-remedy-study, cut from `main` at the merge commit of
  pull request 254 (F281's closure).
  ```

## Deviations & assumptions

None. Round 2 spec was fully implemented:
- T001 module docstring describes bounded read-only comprehension pass per spec
- STUDY_EXCLUDE_DIRS contains all required directories (.git, node_modules, venv, .venv, __pycache__, .data, dist, build, .pytest_cache, .mypy_cache)
- STUDY_CATEGORIES tuple in correct fixed order: structure, core_modules, conventions, entry_points
- DEFAULT_MAX_ENTRIES set to 2000 (reasonable default)
- _walk_repo implements BEFORE cap checking (cap checked before appending each directory and each file) and prunes STUDY_EXCLUDE_DIRS and dotdirs, sorted for determinism
- _detect_entry_points checks pyproject.toml, setup.py, package.json, Makefile, main.py, manage.py at root only
- _detect_conventions detects test directories, AGENTS.md, README files with English notes
- StudyResult dataclass with all required fields: project_id, job_id, cards_written, partial, stopped_reason, entries_scanned
- run_study implements spec exactly: job_id synthesis with validate_job_id, heuristic computation before model call, should_stop budget guard integration, call_fn never crashes (wrapped in try/except), falls back to heuristic on exhaustion or exception, writes four memory cards with provenance="machine-study"
- All five tests pass and verify end-to-end behavior including memory card provenance and auto-approval
- Linting clean, gates all green, working tree clean

## Next

CLI wiring: create standalone `study` command in the catalog and the `resolve_role_config("study", ...)` bridge call site with `ROLE_CONFIG_CALL_SITES` inventory update. This provides the CLI plumbing required for T003's three-step end-to-end test against a foreign repository.
