# Live Review — Steps 10761-10960 — F012 hardening round 16

## Verdict (reviewer-owned)
**PENDING** — F012 hardened (8 external findings), awaiting re-review (NOT accepted)

## Builder Handoff

Operator-built by hand: no Builder, no Reviewer, no provider GENERATION call (0), no Fable, no
subagents, no Evidence `job-flow`/`job-run`, no Docker, no new dependency, **no database**, **no
LLM rerun**, no network. Raw-stream format unchanged; F001 timeout/retry unchanged; F010/F011 not
weakened; no manifest field added (`kind`/`link_target` are additive ReviewFile fields).

External review of `remedy-review-20260717-145620-READY_FOR_REVIEW.zip` returned EIGHT findings.
All fixed as one block; each reproduced against the production seam first (table in
`.agent/plan.md`).

- **F1** — `do job-flow` restored. The hint now reports what `run_job` RESOLVED and persisted, so
  the invocation's omission sentinel is not defeated by re-resolving a default at the call site.
  `tests/test_do_job_flow.py`: 69 failed / 99 passed → **178 passed**.
- **F2** — one closed task-status/expectation truth table, enforced everywhere. All four forged
  `skipped` + worked-status pairs now block; the permissive rows (F011 mid-flight stop, post-run
  gate failures) are kept because production really produces them.
- **F3** — every commit-chain field recomputed: `chain_v`, `subject`, `changed_files` (sorted,
  duplicate-free) as well as commit/tree/parents/patch hash.
- **F4** — the packager recomputes the whole ReviewSubject and compares record by record; every
  forged tombstone/rename/status case from the finding blocks.
- **F5** — typed path kinds via `lstat`, never followed. A symlink is proven by its target text;
  one escaping the repository blocks packaging instead of being followed or silently omitted.
- **F6** — the review base travels explicitly; the resolver reads no environment and no CWD, and
  children never inherit the declaration.
- **F7** — `review_commit_patches/<full-sha>.patch` ships the exact hashed bytes, so a ZIP-only
  reviewer can recompute `patch_sha256` without the repository.
- **F8** — a changed source file requires its known regression suite to have run GREEN; a red
  relevant suite takes the Missing-Tests gate to NEEDS_TESTS.

## Verification (authoritative pytest summaries — each recorded as its own Evidence command)

- New/repaired round-16 suites (do_job_flow, task_expectation_status_truth,
  review_subject_artifact_integrity, review_subject_path_kinds, review_subject_explicit_base,
  review_commit_patch_artifacts) → **322 passed**.
- Every F012 suite → see the packaged `verification_tests.json`.
- F010/F011/Evidence integration → **499 passed**.
- Authoritative CLI matrix (`tests/test_do_job_flow.py` + `tests/cli`, excluding the two suites
  under PRE-EXISTING) → **1026 passed**.
- Docs consistency → **131 passed**.
- compileall (`packages apps scripts tests`) exit 0; `bash -n scripts/make_review_zip.sh` clean;
  `git diff --check` clean.

## Pre-existing failures OUTSIDE this block (not introduced, not fixed)

`tests/cli/test_do_cmd_summary.py` and `tests/cli/test_product_spine.py` fail 18 tests at the
base itself: they require `docs/core-product-spine-v0.md` and sibling flat docs that an earlier
restructure moved. Round 16 touches none of those paths. The recorded CLI command excludes exactly
those two files and the debt is reported here rather than hidden by a green number.

## Status

F012 `[~]` — **not externally accepted**. F017 and later not started. Branch locally committed,
unpushed, unmerged.
