# Live Review — Steps 11161-11360 — F012 hardening round 18

## Verdict (reviewer-owned)
**PENDING** — F012 hardened (7 external findings), awaiting re-review (NOT accepted)

## Builder Handoff

Operator-built by hand: no Builder, no Reviewer, no provider GENERATION call (0), no Fable, no
subagents, no Evidence `job-flow`/`job-run`, no Docker, no new dependency, **no database**, **no
LLM rerun**, no network. Raw-stream format unchanged; F001 timeout/retry unchanged; F010/F011 not
weakened; no manifest field added.

External review of `remedy-review-20260717-193046-READY_FOR_REVIEW.zip` returned SEVEN findings,
all in the file-to-archive trust boundary. Fixed as one coherent block across six commits (plus
one follow-up for a bug the F3 change surfaced); each reproduced against the production seam first
(table in `.agent/plan.md`).

- **F1** — one typed ArchivePlanV1 drives the package; every ReviewSubject file gets one
  disposition, and bundle discovery includes symlinks so an authoritative one is never dropped.
- **F2** — member type and mode are preserved (executable stays 0755; symlink carries S_IFLNK).
- **F3** — `secure_fs.read_verified_file_at` is the one atomically no-follow reader, used by dirty
  hashing, content-proof verification and every ZIP member read.
- **F4** — the ReviewSubject schema is exact recursively (commits + file kinds/modes closed,
  metadata scanned for secrets/paths).
- **F5** — recompute compares the COMPLETE ReviewFileV1 record.
- **F6** — post-build verification checks member type, mode, timestamp and rejects directory
  entries; a regular member cannot pass as a symlink.
- **F7** — the real `make_review_zip.sh` is tested end to end on symlinks, executables,
  newline/Unicode names, special files and external symlinks.

## Verification (authoritative pytest summaries — each recorded as its own Evidence command)

- New round-18 suites (archive_plan, zip_member_metadata, file_read_races, recursive_schema,
  package_full_integration) → recorded per the packaged `verification_tests.json`.
- Every F012 suite → **1835 passed**.
- F010/F011/Evidence integration → **502 passed**.
- Authoritative CLI matrix (`tests/test_do_job_flow.py` + `tests/cli`, excluding the two
  PRE-EXISTING suites) → **1030 passed**.
- Docs consistency → **156 passed**.
- compileall (`packages apps scripts tests`) exit 0; `bash -n scripts/make_review_zip.sh` clean;
  `git diff --check` clean.

## Pre-existing failures OUTSIDE this block (not introduced, not fixed)

`tests/cli/test_do_cmd_summary.py` and `tests/cli/test_product_spine.py` fail 18 tests at the base
itself: they require flat doc paths an earlier restructure moved. Round 18 touches none of them.
The recorded CLI command excludes exactly those two files and the debt is reported here rather
than hidden by a green number.

## Status

F012 `[~]` — **not externally accepted**. F017 and later not started. Branch locally committed,
unpushed, unmerged.
