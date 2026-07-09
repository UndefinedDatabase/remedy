# Plan — Steps 5821-5900 — F003 Close-out, then F004

## Goal
Close F003 (externally accepted), commit + push the accepted F001–F003 work,
update PR #123, merge it, then start F004 conventionally on a fresh branch.

## Current Step
F003 accepted (PASS_WITH_RISKS). STATUS.md marked `[x]` with PR + evidence refs.
Committing the accepted 22-file source/test change in small logical commits,
then push → update PR #123 → Open PR Gate → merge → start F004.

## Accepted F003 references
- Implementation bundle: `remedy-review-20260708-211448-READY_FOR_REVIEW.zip`
- Manual completion job: `4042c805f69e4949`
- Runtime actuals: job `231d28005af344a1` / run `2ece61689cc046c3`
- Runtime totals: 2 provider / 2 actual / 2 cost calls · 11,963 actual tokens ·
  USD 0.153934 · provider_actuals · confidence high · CLI 2.1.204

## Test baselines (all terminate normally)
- token/provider battery → 284 passed
- manual-evidence battery → 291 passed
- provider timeouts → 25 passed
- compileall · `bash -n scripts/make_review_zip.sh` · `git diff --check` clean

## Next Steps
1. Commit F003 work (≤500 lines/commit), push branch.
2. Update PR #123 body to cover F001–F003 accurately.
3. Open PR Gate → merge #123 → `main` → pull --ff-only.
4. Branch `feature/f004-raw-stream-evidence`; set F004 `[~]` when code starts.
5. F004: opt-in `--stream-evidence` (stream-json), redaction before persist,
   bounded raw JSONL + normalized run events with raw offsets. Default stays the
   F003 JSON mode. Built conventionally — no Remedy self-build, no nested agents.

## Hard Rules
No Fable; no nested Builders/Reviewers/subagents; no `job-flow`/`job-run` for
implementation. Do not commit/push F004 before external acceptance. Do not touch
F005/F006. Deferred evidence-metadata notes recorded in `.agent/decisions.md`.
