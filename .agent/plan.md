# Plan

## Goal
Step 21.2: Project Constitution final safety/test hygiene.

## Prior step
Step 21.1 polished trust-report and timeline integration for the constitution.

## Status
COMPLETE — 983 tests pass.

## Steps
1. [x] Fix fragile run-log redaction test (f loop variable → combined_raw_content)
2. [x] Add symlink escape test (_is_safe_path blocks symlinks pointing outside repo_root)
3. [x] Remove duplicate _FORBIDDEN_PATTERNS.search() call in _extract_text_rules
4. [x] Docs: advisory note on tox.ini/pytest.ini commands as hints not exact invocations
5. [x] Update .agent files
6. [x] Run full suite (983 pass)
7. [ ] Commit Step 21.2 changes
8. [ ] Push to feature/step21-project-constitution-v1

## Branch
feature/step21-project-constitution-v1
