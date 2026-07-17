# Live Review — Steps 11361-11560 — F012 hardening round 19 (closure block)

## Verdict (reviewer-owned)
**PENDING** — F012 hardened (12 external findings, the closure block), awaiting re-review (NOT
accepted).

## Builder Handoff

Operator-built by hand: no Builder, no Reviewer, no provider GENERATION call (0), no Fable, no
subagents, no Evidence `job-flow`/`job-run`, no Docker, no new dependency, **no database**, **no
LLM rerun**, no network. Raw-stream format unchanged; F001 timeout/retry unchanged; F010/F011 not
weakened; no manifest field added beyond the additive `current_evidence.review_archive` reference.

External review of `remedy-review-20260717-210512-READY_FOR_REVIEW.zip` (SHA
`17e1f70e…b877b`, Evidence job `384f2db9a1bc430e`) returned TWELVE findings, all in the
file-to-archive trust boundary. The reviewer's factual correction is honoured: the content proof is
18 authoritative files; the ReviewSubject is 21 (the three extra are `.agent/context.md`,
`.agent/live_review.md`, `.agent/plan.md` — intentional, non-authoritative Operator State). Fixed
as one coherent closure block across eight commits; each finding reproduced against the production
seam first (table in `.agent/plan.md`).

- **F1** — authority is passed EXPLICITLY as the Content-Proof set; a member is authoritative iff
  its path is in it. `.agent/` state is operator-context, never authoritative. `source_class` is
  distinct from authority.
- **F2** — the typed plan and its verification report are packaged as verified members under
  `evidence/current/` and named by the manifest; the build aborts unless the archive matches the
  plan, so a packaged report always describes a verified archive.
- **F3** — a dirty working-tree chmod is captured as the current git mode from the read's own
  fstat.
- **F4** — the planned regular mode is bound to the opened source's executability (`expected_mode`).
- **F5** — a regular read is a stable same-inode read; a file rewritten mid-read is a torn read and
  discarded.
- **F6** — a symlink's target/containment is validated on the exact stability-checked bytes.
- **F7** — one bundle-safety policy (`classify_bundle_path`) decides INCLUDE / OPERATOR_CONTEXT /
  TOMBSTONE / BLOCK_SENSITIVE / BLOCK_UNSUPPORTED from the path alone, before any read.
- **F8** — the Evidence tree is a typed no-follow inventory; a symlink/FIFO/device blocks (never
  skipped, never followed), replacing `find -type f` + `cp`.
- **F9** — the ReviewSubject schema is coherent, not merely field-typed (missing hashes, base
  symlink with a regular mode, copy without old_path, no-op type change all rejected).
- **F10** — the subject loader fails closed; only an absent `--subject-json` is the legacy empty
  subject.
- **F11** — a symlink member's permission bits, create_system, compression method and encryption
  are checked post-build.
- **F12** — per-member (64 MiB), aggregate (2 GiB), member-count and expansion-ratio (200x) caps
  refuse a bomb before it is read into RAM.

## Verification (authoritative pytest summaries — each recorded as its own Evidence command)

- New round-19 suites (archive_authority, archive_artifacts, dirty_modes, file_stable_reads,
  symlink_atomic_policy, evidence_inventory, subject_coherence, zip_fail_closed, archive_limits) →
  **60 passed**.
- Every F012 review / subject / manifest / evidence suite slice → **1554 passed**.
- Full `tests/orchestration` + docs consistency → **7006 passed, 7 skipped** (26 PRE-EXISTING
  failures unchanged, see below).
- Docs consistency (incl. `TestF012Round19IsPinned`) → **167 passed**.
- Full-package integration (`test_review_package_full_integration.py`, 6 REAL cases, no skips) →
  **6 passed in ~2.0s**.
- compileall (`packages apps scripts tests`) exit 0; `bash -n scripts/make_review_zip.sh` clean;
  `git diff --check` clean.

## Pre-existing failures OUTSIDE this block (not introduced, not fixed)

The full `tests/orchestration` + docs run shows **26 failures**. Verified against a clean worktree
of the round-19 base `980ec10`: the SAME 26 fail there, so round 19 introduces zero regressions.
They are stale fixtures / doc-path debt in files this block does not touch —
`test_job_fulfillment.py` (9), `test_project_brain.py` (4), `test_project_summary.py` (4),
`test_worker_queue.py::TestWorkerDocs` (4), `test_event_replay.py` (2),
`test_development_artifact_boundary.py` (1), `test_job_worktree_handoff.py` (1), and
`test_stream_export_e2e.py` (1, whose minimal-repo fixture never added `build_review_zip.py` as a
dependency). The debt is reported here rather than hidden by a green number.

## Status

F012 `[~]` — **not externally accepted**. F017 and later not started. Branch locally committed,
unpushed, unmerged.
