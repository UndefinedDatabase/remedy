# Live Review — Steps 3519-3555: Workspace-Staged Fulfillment Safety Closure v0.2

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Timestamp: 2026-06-22

## Verdict (reviewer-owned)
**FAIL** @ 2d52bca

6 files changed, +786/-40. PR #101 open (builder did NOT self-merge).
Builder did NOT write reviewer verdict. Working tree clean.

## Protocol note
Builder reused branch `feature/steps-3276-3355-job-fulfillment-spine-v0` (from merged PR #100)
instead of creating a new branch for Steps 3519-3555. Protocol violation per AGENTS.md but Low
severity — no data corruption risk.

## Findings

### R-0201 Blocker — Target repo metadata mutation (NOT RESOLVED)
Line 774 of `job_fulfillment.py`: `job.metadata["target_repo"] = str(staging_ws.staging_dir.resolve())`
followed by `save_job(job, root=data_dir)` at line 775.

Saved job record on disk points to staging path during apply/test/proof phases. If exception
occurs between line 775 and any restoration point (lines 850, 918, 958), job metadata is
permanently corrupted — pointing to a temp dir that will be deleted.

The `atexit` handler (line 787-789) cleans up staging dir but does NOT restore metadata.
Prompt says: "PASS only if saved job metadata remains the real target repo throughout
success, blocked, and exception paths."

Fix: pass staging dir as explicit override parameter to apply/test, never mutate saved metadata.

### R-0202 Blocker — Completion without promotion truth (NOT RESOLVED)
`JobFulfillmentContract.check()` (line 127-128) checks `requires_staging` →
`record.staging_used` but does NOT check `record.staging_promoted`.

Contract check runs at line 903-904 BEFORE promotion at line 909. If contract passes
but promotion returns `promoted=False` (e.g. all files skipped), line 932 still sets
`COMPLETED_VERIFIED`.

Fix: contract must require `staging_promoted=True` when staging is required. Or check
promotion result before setting completed status.

### R-0203 High — Blocked jobs report code_applied=true (NOT RESOLVED)
`_extract_job_truth()` in job.py (lines 738-787) determines `code_applied` from:
1. Artifact metadata `patch_intent_apply_records` with state "applied"
2. Timeline event `fulfillment_applied`

When staged apply happens, `apply_patch_intent` writes apply records to artifact metadata
as "applied" (even though it wrote to staging, not target). For blocked jobs (test failure),
`code_applied` would be True from artifact metadata despite target being untouched.

No test verifies `code_applied=false` for blocked/failing-test cases.

### R-0204 High — Unsafe filtered copy (NOT RESOLVED)
`staging_workspace.py` `_should_exclude()`:

1. `.env` variant gap: `_EXCLUDE_PATTERNS` has `{".env", ".env.local", ".env.production"}`.
   Missing: `.env.dev`, `.env.test`, `.env.staging`, `config/.env.staging`, any `.env.*` variant.
   Fix: use `name.startswith(".env")` instead of exact set match.

2. Symlink escape: `_copy_tree()` uses `item.is_file()` and `item.is_dir()` which follow
   symlinks. A symlink to `/etc/passwd` or external directory would be copied/recursed into.
   No `is_symlink()` check exists. No path containment verification.
   Fix: check `item.is_symlink()` before following, verify resolved path is under target_repo.

3. No test exists for `.env.dev`, `.env.test`, symlink escape, or symlink loop.

### R-0205 High — Unsafe promotion path (NOT RESOLVED)
`promote_staged_changes()`: `rec.relative_path` is used directly to construct
`target_path = workspace.target_repo / rec.relative_path`. No path containment check.

`../escape.md` would resolve to outside the target repo and be written there.

Non-.md files get `shutil.copy2` (direct overwrite) — not restricted to Markdown-only in
fixture mode despite the docstring claiming "only .md expected in v0".

Fix: validate `target_path.resolve()` is under `workspace.target_repo.resolve()`.
Add explicit Markdown-only gate for fixture mode.

### R-0206 High — Existing Markdown append-only uses line-set diff (NOT RESOLVED)
Lines 224-229 of `staging_workspace.py`:
```python
target_lines_set = set(target_content.splitlines())
for line in staged_content.splitlines():
    if line not in target_lines_set:
        new_lines.append(line)
```

This is exactly line-set diff. Problems:
- Duplicate lines in staged content are deduplicated against target
- Reordered content is silently accepted
- Content can be replacement-appended
- Does NOT verify staged starts with exact target content

Prompt says: "FAIL if existing Markdown promotion uses line-set diff."

Fix: verify `staged_content.startswith(target_content)`, append only the suffix.

### R-0207 Medium — Demo docs include unverified command sequence
Demo doc shows `remedy job create "..." --json` then `remedy job attach-repo ...` as separate
commands. Sequence is plausible (both exist in catalog) but never tested as end-to-end flow.
Low risk — commands exist individually.

### R-0208 Medium — Review bundle missing staging truth (NOT RESOLVED)
`review_bundle.py` not touched. Fulfillment summary in review bundle does not include
`staging_used`, `staging_promoted`, staged vs promoted file lists.

### R-0209 Medium — Missing target unchanged proof (NOT RESOLVED)
No test hashes target repo before and after blocked/failing-test cases to prove target
was truly untouched. `test_staging_discarded_on_test_failure` checks metadata restoration
but not file-level target integrity.

### R-0210 Medium — data_dir inconsistency (PARTIAL)
`_approve_and_apply_intent` passes `data_dir` explicitly. `execute_test_run` does NOT
accept data_dir — relies on job metadata `target_repo` (which was mutated to staging).
This "works" only because of the metadata mutation (R-0201). If R-0201 is fixed properly,
test execution needs explicit staging root override.

### R-0211 Medium — Test isolation failure (NEW)
`run_job_fulfill()` uses `atexit.register(_cleanup_staging)` (line 789) and mid-function
`import tempfile` / `import shutil as _shutil` (lines 758, 785). In full test suite:
17 fulfillment tests fail due to cross-test state corruption from atexit handlers.
Tests pass targeted (66 passed) but fail in full suite.

Fix: use try/finally instead of atexit. Move imports to module level.

### R-0212 Low — Branch reuse protocol violation
Builder used merged PR #100's branch for PR #101 instead of creating new branch.
AGENTS.md requires new feature branch. No data risk — cosmetic protocol issue.

### R-0213 Low — Lint not clean
Ruff reports import sorting (I001) and format style (UP032) issues in `job_fulfillment.py`.

## Required checks assessment
1. Protocol compliance — **PASS** (with R-0212 Low). Builder did not self-merge, did not write verdict.
2. Metadata mutation — **FAIL** (R-0201 Blocker). Saved job metadata mutated to staging path.
3. Explicit staged apply/test/proof — **FAIL** (R-0201, R-0210). Not explicit overrides — works via metadata mutation.
4. Staging workspace location — **PASS**. Under tmpdir (system temp), cleaned up on success.
5. Filtered copy safety — **FAIL** (R-0204 High). `.env.*` gap, symlink escape.
6. Symlink/secret exclusion — **FAIL** (R-0204 High). No symlink check.
7. Path containment — **FAIL** (R-0205 High). No traversal guard.
8. Promotion safety — **FAIL** (R-0205, R-0206 High). Path traversal, non-md allowed, line-set diff.
9. Existing Markdown behavior — **FAIL** (R-0206 High). Line-set diff, not prefix+suffix.
10. Completion contract truth — **FAIL** (R-0202 Blocker). Promotion not in contract.
11. Failure truth — **FAIL** (R-0203 High). Blocked jobs may report code_applied=true.
12. Status/report/review-bundle truth — **FAIL** (R-0208 Medium). Review bundle missing staging.
13. Demo docs exactness — **PASS** (with R-0207 Medium risk).
14. Target unchanged proof — **FAIL** (R-0209 Medium). No hash-based verification.

## Test evidence (reviewer-run)
- Compileall: clean
- Fulfillment tests (targeted): 66 passed, 4.03s
- Product spine: 72 passed, 0.13s
- Command catalog: 23 passed, 0.41s
- Boundary guard: 18 passed, 0.19s
- Fast lane: 571 passed, 0.88s
- Runtime lane: 4/4 suites passed
- Lint: NOT clean (I001, UP032)
- Full suite: 7112 passed, 17 failed, 8 skipped, 1 deselected, 386s
  - 17 failures all in test_job_fulfillment.py (test isolation from atexit, R-0211)
  - 1 pre-existing failure (test_full_chain_order) deselected

## Architecture guard scan
- No `shell=True` found
- No provider SDK imports found
- No network calls found
- No subprocess calls in staging_workspace.py or job_fulfillment.py engine
- No git operations found
- No `.agent/live_review.md` runtime dependency found
- No raw absolute path in JSON output (export uses safe fields)
- `target_repo` mutation to staging confirmed (R-0201)

## Changed Line Map spot-check
- packages/orchestration/staging_workspace.py (+308, NEW): filtered copy, find changes, promote, discard, export. Line-set diff for .md append. No symlink check. No path containment.
- packages/orchestration/job_fulfillment.py (+123): staging workspace integration, atexit handler, metadata mutation pattern, promotion gate.
- apps/cli/commands/job.py (+8): staging_used/staging_promoted in truth extraction and status/report output.
- tests/orchestration/test_job_fulfillment.py (+326): 15 staging tests. No symlink/env-variant/path-traversal/hash tests.
- docs/first-fulfilled-job-demo-v0.md (+29/-4): staging invariants added to demo guide.
- .agent/plan.md (+32): updated plan.

## Top risks
2 Blocker findings (R-0201, R-0202), 4 High findings (R-0203, R-0204, R-0205, R-0206),
4 Medium findings (R-0207, R-0208, R-0209, R-0210, R-0211), 2 Low (R-0212, R-0213).

## Merge readiness
NOT ready to merge. 2 Blocker + 4 High + 5 Medium findings open.
17 full-suite test failures from test isolation bug.

NO PR unless user asks.

## Reviewer audit log
- PR #101 @ 2d52bca. 6 files changed, +786/-40.
- Code review: staging_workspace.py (308 lines), job_fulfillment.py delta (+123), job.py (+8).
- Targeted tests: 66 passed. Full suite: 7112 passed, 17 failed.
- Architecture guard: clean except metadata mutation.
- Findings: 2 Blocker, 4 High, 5 Medium, 2 Low.
- Verdict: **FAIL** @ 2d52bca — 11 open findings including 2 Blockers.
