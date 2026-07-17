# Live Review — Steps 10961-11160 — F012 hardening round 17

## Verdict (reviewer-owned)
**PENDING** — F012 hardened (10 external findings), awaiting re-review (NOT accepted)

## Builder Handoff

Operator-built by hand: no Builder, no Reviewer, no provider GENERATION call (0), no Fable, no
subagents, no Evidence `job-flow`/`job-run`, no Docker, no new dependency, **no database**, **no
LLM rerun**, no network. Raw-stream format unchanged; F001 timeout/retry unchanged; F010/F011 not
weakened; no manifest field added (`base_kind`/`base_mode`/`current_mode` are additive ReviewFile
fields only).

External review of `remedy-review-20260717-172441-READY_FOR_REVIEW.zip` returned TEN findings.
All fixed as one trust-chain block across six local commits; each reproduced against the
production seam first (table in `.agent/plan.md`).

- **F1** — task truth is read in the EPISODE's context: a completed/worked episode's executed or
  prior task must be applied/passed, not pending/running/failed/blocked; the permissive states
  stay legal only where a stop produces them.
- **F2** — a completed task's terminal STATUS is frozen across episodes, alongside its already-
  frozen run/ledger.
- **F2(files)** — `merge_review_file_state` is the one lossless typed merge; a dirty symlink over
  a committed regular file no longer comes back a regular file.
- **F3** — committed kinds/modes come from `git diff --raw`; a committed symlink's target is read
  from its git blob, never followed.
- **F4** — the content-proof check is typed and no-follow (`lstat` + hash by kind).
- **F5** — dirty deletions carry a base tombstone; dirty renames carry old path + both hashes.
- **F6** — `do job-flow` forwards the declared review base like `do job-evidence`.
- **F7** — strict `review_subject.json` schema; `subject.commits == chain.commits`.
- **F8** — the ZIP is built NUL-safely from an exact model; hostile-but-legal names survive.
- **F9** — containment by `os.path.commonpath`; a sibling `repo-evil` is refused.
- **F10** — the finished ZIP is reopened and every member verified against the model.

## Verification (authoritative pytest summaries — each recorded as its own Evidence command)

- New/repaired round-17 suites (episode_context, dirty_union, committed_path_kinds,
  dirty_tombstones, strict_schema, package_symlink_integrity, package_containment,
  zip_hostile_paths, do_job_flow_review_base) → recorded per the packaged `verification_tests.json`.
- Every F012 suite → **1781 passed**.
- F010/F011/Evidence integration → **502 passed**.
- Authoritative CLI matrix (`tests/test_do_job_flow.py` + `tests/cli`, excluding the two
  PRE-EXISTING suites) → **1030 passed**.
- Docs consistency → **145 passed**.
- compileall (`packages apps scripts tests`) exit 0; `bash -n scripts/make_review_zip.sh` clean;
  `git diff --check` clean.

## Pre-existing failures OUTSIDE this block (not introduced, not fixed)

`tests/cli/test_do_cmd_summary.py` and `tests/cli/test_product_spine.py` fail 18 tests at the base
itself: they require flat doc paths an earlier restructure moved. Round 17 touches none of them.
The recorded CLI command excludes exactly those two files and the debt is reported here rather
than hidden by a green number.

## Status

F012 `[~]` — **not externally accepted**. F017 and later not started. Branch locally committed,
unpushed, unmerged.
