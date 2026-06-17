# Live Review — Steps 2296-2365: Review Bundle Structured Error Reporting v1

Reviewer: parallel reviewer (independent; owns verdict — builder self-report does not set verdict;
a builder `Done:` marker is NOT reviewer `Resolved`).
Scope (ALLOWED): review bundle structured section error model; safe exception redaction;
review bundle section registry; safe section builder wrapper; removal of repeated section
assembly try/except boilerplate; degraded section count/summary; review bundle docs/tests;
CLI/runtime degraded-section behavior; `.agent/context.md` / `.agent/plan.md` backlog update.
Must NOT: review_bundle package split; ui_server split; orchestration subpackage split;
config system; README rewrite; provider execution; Claude/Pi/OpenCode/Ollama; provider SDK;
auto-apply; auto-approval; auto-PR/git; direct repo mutation; shell=True; arbitrary shell;
semantic memory; MemPalace; UI redesign; MCP.
REVIEW BUNDLE STRUCTURED ERROR REPORTING BLOCK — diagnostics, not features.
Timestamp: 2026-06-17

## Verdict (reviewer-owned)
**PASS** @ ef55c00 (3 commits: 927f034 + 0a5a8d9 + ef55c00). Zero open Blocker/High/Medium.
3 Low findings (R-0121 pre-existing, R-0122 dead code, R-0123 unused dataclass).
All 11 checks PASS.
90 targeted tests passed (review_bundle). 29 CLI/catalog tests passed. 6600 full suite passed
(8 skipped, 1 deselected). 0 failed.
Ruff: All checks passed. Mypy: 186 files, no issues. compileall: clean.
Uncommitted changes: .agent/live_review.md (reviewer-owned) + .agent/plan.md (builder completion update).

## Prior block
Steps 2226-2295: PASS @ cdcee97 (R-0119, R-0120 Resolved).
Merged to main via PR #80 -> 99e6fe1.

## Changed files (Steps 2296-2365 @ ef55c00)
| File | What changed |
|------|-------------|
| packages/orchestration/review_bundle.py | +269/-356: Structured error model (ReviewBundleSectionError, _categorize_exception, _safe_exception_message), section registry (_REVIEW_BUNDLE_SECTION_SPECS, 37 specs), _build_section_safe wrapper, build_review_bundle refactored to loop, top-level diagnostics (degraded_section_count, etc), 47→2 broad exceptions, export/summary updated |
| tests/orchestration/test_review_bundle.py | +365/-51: 8 new test classes, 28 new tests (90 total, was 62): structured error model, categorization, redaction, registry, safe wrapper, degraded summary, manifest diagnostics |
| docs/review-bundle-structured-error-reporting-v1.md | NEW +96L: problem/solution, error categories, redaction rules, operator guidance, future work |
| .agent/context.md | Updated scope, modified files, backlog 4/30, resource safety section |
| .agent/plan.md | Updated for 2296-2365, 14 phases completed |

## Check matrix (Steps 2296-2365 @ ef55c00)
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Mainline closure | PASS | PR #80 merged -> main 99e6fe1; branch forked from a9bea59; context.md + plan.md reconciled; clean tree (only reviewer-owned + builder plan update) |
| 2 | Baseline audit | PASS | Initial: 2251 lines, 47 except Exception, 37 REQUIRED_SECTIONS. Current: 2165 lines (-86), 2 except Exception (-45), 39 REQUIRED_SECTIONS (+2: run_contract_summary.json, test_execution_summary.json). 37 registry specs match 39 required minus 2 generated. |
| 3 | Structured error model | PASS | ReviewBundleSectionError has section_name, error_type, error_category, safe_message, is_bug, is_optional_dependency, occurred_at. Degraded JSON exposes: status, reason, error_type, error_category, error_message, section_name. No raw traceback in public. Message bounded (240 chars). Message redacted (secrets via _SECRET_RE, private paths via _HOME_RE, protected paths via _PROTECTED_PATH_RE). JSON safe. |
| 4 | Safe section wrapper | PASS | _build_section_safe: success -> included section with content. Failure -> degraded section with structured JSON, error logged with exc_info=True (traceback in logs only), ReviewBundleSection carries error_type/error_category/error_message. No generic "build failed" with zero diagnostics. |
| 5 | Section registry / boilerplate removal | PASS | _REVIEW_BUNDLE_SECTION_SPECS: 37 specs in deterministic tuple. build_review_bundle: simple for-loop replaces 35 copy-pasted try/except blocks. Output filenames unchanged. Ordering deterministic. bundle_readme.md + manifest.json still built separately (compatible). REQUIRED_SECTIONS correct. |
| 6 | Broad exception handling | PASS | 47 -> 2. L386: _build_section_safe (intentional wrapper, categorizes + redacts + logs). L1974: load_job in build_review_bundle (documented: multiple exception types). 8 section builders narrowed to (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError). Ruff passes. |
| 7 | Top-level degraded summary | PASS | ReviewBundleResult: diagnostics_version=1, degraded_section_count (int), degraded_sections (list[str]), section_error_summary (list[dict]). Clean bundle defaults: count=0, sections=[], summary=[]. Manifest JSON includes all 4 fields. export_review_bundle_json includes all 4 fields. Backward-compatible. |
| 8 | Redaction | PASS | Tests cover: secret token (sk-test12345678), private path (/home/user), truncation (500->244 chars), no traceback, no secret in degraded content. Manual verification: sk-ant-api03-* redacted, ghp_* redacted. R-0121 (Low): api_key=value partial redaction (pre-existing _SECRET_RE gap). |
| 9 | CLI/runtime | PASS | 11 CLI runtime tests pass. JSON output includes diagnostics. Non-JSON summarize_review_bundle shows degraded sections without traceback. Invalid paths safe. |
| 10 | 30-task backlog | PASS | Previous 3/30 in prior block. Updated to 4/30 (Ruff, Mypy, Coverage baselines + Review Bundle Structured Error Reporting v1). No duplicate brainstorm. No false claims. |
| 11 | Runtime behavior | PASS | No provider/model execution. No shell=True. No subprocess. No repo mutation. No behavior refactor outside review bundle diagnostics. Pre-existing Ollama references (L1353/1391) are data model fields, not execution. Existing bundle output compatible. |

## Findings — Steps 2296-2365

### R-0121 — Pre-existing key=value redaction gap (Low, NOT INTRODUCED)
`_SECRET_RE` in redaction_patterns.py: pattern `(?:password|api_key|secret|token|credential)\s*=`
matches only the key prefix, not the following value. Example: `api_key=mysecret123` ->
`[REDACTED]mysecret123` — value leaks. New `_safe_exception_message` inherits this gap.
Scope: pre-existing in shared infrastructure, not introduced by this block.
Most critical patterns (sk-*, ghp_*, xoxb-*, PEM headers) work correctly.
**Severity: Low** — pre-existing, partial coverage, primary token formats all work.

### R-0122 — Dead code: is_optional/is_bug in _build_section_safe (Low)
`_build_section_safe` L390-391 computes `is_optional` and `is_bug` but neither variable is
stored in the section, returned, or used anywhere. Ruff F841 suppressed in pyproject.toml.
**Severity: Low** — harmless dead code, no behavioral impact.

### R-0123 — ReviewBundleSectionError never instantiated in production (Low)
`ReviewBundleSectionError` dataclass (L146) is defined and tested (test_section_error_to_dict)
but never instantiated in production code. `_build_section_safe` creates `ReviewBundleSection`
directly. Designed for future consumption but currently unused.
**Severity: Low** — no behavioral impact, well-tested standalone.

Next id: R-0124.

## Reviewer test runs

### Targeted (review_bundle)
90 passed in 1.63s — tests/orchestration/test_review_bundle.py

### Targeted (CLI + catalog)
29 passed in 2.90s — tests/cli/test_review_bundle_runtime.py (11) +
tests/test_command_catalog.py (18)

### Lint
scripts/remedy_lint.sh: Ruff all checks passed + Mypy 186 files no issues.
python3 -m ruff check packages/orchestration/review_bundle.py tests/orchestration/test_review_bundle.py: passed.

### compileall
python3 -m compileall -q packages apps tests: clean.

### Full suite
scripts/remedy_pytest.sh -k "not test_full_chain_order":
6600 passed, 8 skipped, 1 deselected in 171.74s. Zero failures.

## Structured error reporting assessment
35 copy-pasted try/except blocks replaced with declarative registry + safe wrapper.
Structured degraded JSON: error_type, error_category, error_message (redacted), section_name,
status, reason. Top-level diagnostics: degraded_section_count, degraded_sections,
section_error_summary, diagnostics_version. Traceback logged (exc_info) but never in public
bundle. Redaction covers sk-*, ghp_*, xoxb-*, PEM, private paths, protected paths, truncation.

## Degraded summary assessment
ReviewBundleResult carries all 4 required fields with backward-compatible defaults.
Manifest JSON and export JSON both include diagnostics. summarize_review_bundle shows degraded
section details in text output. Clean bundles report zero degraded.

## Redaction assessment
7 tests: clean message, secret redacted, private path, truncation, empty, no traceback, type
not in message. 2 wrapper tests: no traceback in content, no secret in content.
Manual verification: sk-ant-*, ghp_*, /home/path all correctly redacted.
Gap: api_key=value partial (R-0121, pre-existing, Low).

## Baseline audit
| Metric | Before | After |
|--------|--------|-------|
| Lines | 2251 | 2165 (-86) |
| except Exception | 47 | 2 (-45) |
| REQUIRED_SECTIONS | 37 | 39 (+2) |
| Registry specs | 0 | 37 |
| Test count (file) | 62 | 90 (+28) |
| Full suite | 6569 | 6600 (+31) |

## Top risks
None critical. Three Low findings documented. Pre-existing redaction gap inherited but not
worsened. Dead code is benign and testable. Unused dataclass is designed for future use.

## Merge-readiness
Merge-ready. Zero open Blocker/High/Medium. R-0121/R-0122/R-0123 all Low.
PR #81 exists, non-draft, feature/steps-2296-2365 -> main.
Merge-autonomy applies: auto-merge on PASS.

## Reviewer audit log
- Block opened for Steps 2296-2365 (Review Bundle Structured Error Reporting v1).
- Prior block 2226-2295 PASS @ cdcee97 merged via PR #80 -> main 99e6fe1.
- Check 1 (mainline closure) PASS: PR #80 merged, branch fresh from a9bea59.
- WIP pre-scan: review_bundle.py growing from +157 to +269, test file +364L. No danger imports.
- PermissionError/OSError bug found in WIP — builder fixed before committing.
- 3 commits detected: 927f034 (code+docs) + 0a5a8d9 (tests+agent) + ef55c00 (context update).
- Full line-level review: all 11 checks assessed.
- R-0121 noted (pre-existing redaction gap, Low). R-0122 noted (dead code, Low). R-0123 noted (unused class, Low).
- Ruff: all checks passed. Mypy: 186 files, no issues. compileall: clean.
- Targeted: 90 + 29 passed. Full suite: 6600 passed, 0 failed.
- German scan: zero matches.
- Danger scan: clean (no subprocess, shell=True, provider).
- Uncommitted: .agent/live_review.md (reviewer-owned) + .agent/plan.md (builder completion update, reviewed, clean).
- Reviewer verdict: PASS @ ef55c00 (3 Low findings, zero Blocker/High/Medium).
- Merge-autonomy: PR #81 auto-merge triggered.
