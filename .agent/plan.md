# Plan — Steps 2366-2445: Review Closure (R-0124..R-0130)

## Goal
Fix 7 reviewer findings from PASS WITH RISKS verdict on PR #82. Expand config
system with diagnostics, path redaction, CLI completeness, key registry 18+.

## Steps
- [x] Phase 0-10: Initial implementation (a0fda56)
- [x] R-0124: Fix quoted key=value redaction in _SECRET_RE
- [x] R-0125: Reject unknown/secret keys in set_config_value + CLI
- [x] R-0126: Structured diagnostics for malformed TOML and unknown keys
- [x] R-0127: Redact absolute paths in to_summary_dict + config sources CLI
- [x] R-0128: Add config show, --json on init/set, --path on init/set, fix CLI test
- [x] R-0129: Expand key registry to 18 keys (ui, tests, quality, logging, provider flags)
- [x] R-0130: Changed Line Map (this commit)
- [x] Full suite: 6677 passed, 0 failed (excl pre-existing), 8 skipped
- [ ] Commit + push + reviewer re-evaluation

## Hard rules
No provider execution; no shell=True; no auto-apply/approve/PR/git; no secret storage in config.
