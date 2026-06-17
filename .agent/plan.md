# Plan — Steps 2296-2365: Review Bundle Structured Error Reporting v1

## Goal
Turn silent/generic section failures into structured, redacted, diagnosable error reports.

## Steps
- [x] Phase 1: Baseline audit (2251 lines, 47 except Exception, 37 REQUIRED_SECTIONS)
- [x] Phase 2: ReviewBundleSectionError dataclass + error categories
- [x] Phase 3: _safe_exception_message with redaction
- [x] Phase 4: ReviewBundleSectionSpec registry (37 specs)
- [x] Phase 5: _build_section_safe wrapper
- [x] Phase 6: Replace 35 copy-pasted try/except blocks with registry loop
- [x] Phase 7: Eliminate bare except Exception (47 -> 2 intentional)
- [x] Phase 8: Top-level summary fields (degraded_section_count, etc)
- [x] Phase 9: CLI behavior verified (no traceback, JSON safe)
- [x] Phase 10: Docs (review-bundle-structured-error-reporting-v1.md)
- [x] Phase 11: Backlog update (4/30 strict)
- [ ] Phase 12-14: Lint + targeted tests + coverage + full suite + commit + PR

## Hard rules
No review_bundle package split; no provider SDK; no shell=True; no auto-apply/approve/PR/git.
