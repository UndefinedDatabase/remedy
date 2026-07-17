# Live Review — Steps 10561-10760 — F012 hardening round 15

## Verdict (reviewer-owned)
**PENDING** — F012 hardened (7 external findings), awaiting re-review (NOT accepted)

## Builder Handoff

Operator-built by hand: no Builder, no Reviewer, no provider GENERATION call (0), no Fable, no
subagents, no Evidence `job-flow`/`job-run`, no Docker, no new dependency, **no database**, **no
LLM rerun**, no network. Raw-stream format unchanged; F001 timeout/retry unchanged; F010/F011 not
weakened; no manifest field added.

External review of `remedy-review-20260717-113313-READY_FOR_REVIEW.zip` (formally clean, verdict
FINDINGS) reported five correctness/process gaps plus two process items. All fixed; each
reproduced against the production seam first (table in `.agent/plan.md`).

- **F1 — task lifecycle is monotonic.** Round 14 stopped a later episode rewriting a run it
  admitted to; it could still OMIT the ledger and call an applied task `skipped`. The omission was
  the erasure. `validate_task_lifecycle_chain()` binds terminal tasks to `prior_episode` with the
  same run and frozen ledger, keeps a skipped task skipped, and deliberately leaves a stopped
  `pending` task free to start a new run — F011's resume.
- **F2 — call-ref numbers have one text form.** `int()` read `round-01`/`round-001`/`round-000001`
  as one round and `attempt-00` as index 0. One shared formatter in `call_identity.py`, canonicality
  decided by reconstruction, all three production generators pinned to it.
- **F3/F5 — the review subject is typed, verified, and resolved by ONE production helper.** An
  invalid base was silently ignored (a smaller review, no error); a non-ancestor base pulled in
  another branch's files. Both now raise. Base/head are full SHAs recorded in `review_subject.json`,
  the content proof and the ZIP manifest. `REMEDY_REVIEW_BASE` is read in exactly one module, and a
  test enforces that.
- **F4 — deletions and renames are provable.** A deleted path carries a tombstone (`base_sha256`);
  a rename carries `old_path` plus both hashes; paths come from one NUL-delimited command.
- **F6 — coverage understands directory arguments.** `pytest tests/docs` now covers the files
  beneath it, and `--ignore` is honoured. The round-14 NEEDS_TESTS was about two tests that had
  just run green.
- **F7 — the commit chain is an artifact.** `review_commit_chain.json` is recomputed and verified
  by the packager; the handoff's commit list comes from it, not from prose.

## Local commits this round (from `review_commit_chain.json`, not prose)

| SHA | Subject |
|---|---|
| `7eef9d4` | fix(f012): preserve task lifecycle across episodes |
| `89e3dd6` | fix(f012): canonicalize call reference numbers |
| `033b65d` | fix(evidence): bind committed review subjects to a verified base |
| `cf02a7b` | test(f012): prove task history and committed review subjects |
| `ec43213` | fix(evidence): prove deletions renames and commit ancestry |
| `f5778e2` | docs(f012): document chain and review subject contracts |

## Verification (authoritative pytest summaries — each recorded as its own Evidence command)

- New round-15 suites (task_history_chain, call_ref_canonical_numbers, review_subject_resolution,
  review_subject_deletions, review_commit_chain) → **151 passed**.
- Every F012 suite → **1330 passed**.
- F010/F011/Evidence integration → **499 passed**.
- CLI regressions (`tests/cli`, excluding the two suites under PRE-EXISTING) → **848 passed**.
- Docs consistency → **118 passed**.
- compileall exit 0; `bash -n scripts/make_review_zip.sh` clean; `git diff --check` clean;
  `remedy integrity check` all checks pass.

## Pre-existing failures OUTSIDE this block (not introduced, not fixed)

1. `tests/cli/test_do_cmd_summary.py` + `tests/cli/test_product_spine.py` — 18 failures at base
   `b0ba27a` (they require `docs/core-product-spine-v0.md`, removed by an earlier restructure).
   Excluded from the recorded CLI command.
2. `tests/test_do_job_flow.py` — **69 failures at the reviewed round-14 HEAD `bddff63` itself**,
   verified with round-15 changes stashed: `NameError: name 'timeout_sec' is not defined` at
   `apps/cli/commands/do_cmd.py:2209`. A real product bug in `remedy do job-flow`, present at base
   `b0ba27a` (introduced by `50e40d0`, long before this branch). Not in any authoritative command.
   Reported, not fixed — outside this round's findings.

## Known gap (unchanged, recorded honestly)

The preferred filesystem-tree identity for genuinely non-Git workspaces is still not implemented:
such a workspace records an explicit `unavailable` identity and therefore INCOMPLETE input
coverage — the finding's own stated fallback. It never yields `same_inputs=true`.

## Status

F012 `[~]` — **not externally accepted**. F017 and later not started. Branch committed locally,
**unpushed, unmerged**.
