# Plan — Steps 2366-2445: Final Closure (R-0131..R-0134)

## Goal
Fix remaining closure gaps: validate --path, warning path redaction, reviewer-grade CLM.

## Steps
- [x] Phase 0-10: Initial implementation (a0fda56)
- [x] R-0124..R-0130: Closure fixes (ceebe13)
- [x] R-0131: Add --path to config validate (catalog + handler)
- [x] R-0132: Redact absolute paths in warning strings for public export
- [x] R-0133: Reviewer-grade Changed Line Map in handoff
- [x] R-0134: Builder handoff states reviewer re-assessment required
- [x] Tests: 59 config + 17 CLI + 18 catalog + 90 review_bundle = 184 targeted; 6684 full suite
- [ ] Commit + push + reviewer re-assessment

## Hard rules
No provider execution; no shell=True; no auto-apply/approve/PR/git; no secret storage in config.
