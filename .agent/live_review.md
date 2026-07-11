# Live Review — Steps 5961-6020 — F005 — Enforced structured outputs

Reviewer: external final reviewer (independent; owns verdict).

## Verdict

**`PASS_WITH_RISKS — ACCEPTED`.** F005 is externally accepted and ready for
commit, push, PR and merge. F001–F004 are accepted and merged (F004 = PR #124,
merge commit `cb55909`).

## Branch / Base

- Branch: `feature/f005-structured-outputs`
- Base/HEAD before commit: `cb55909`

## Scope

F005 — Enforced structured outputs. Small enforced JSON schemas replace fragile
free-text Reviewer and Planner parsing: mandatory top-level `schema_v`
(ReviewVerdict `rv1`, PlannerPlan `pp1`, DesignSpec `ds1` placeholder), native
Claude `--json-schema` (JSON + stream `structured_output`) and native Ollama
`format=<schema>`, a hard maximum of one logical parse retry, honest `parse`
classification of native structured-output exhaustion with Usage/cost retained,
one prompt trace per actual provider call with exact sent-prompt hashes, and
legacy free-text paths only behind explicit compatibility flags.

## Accepted package

- Job `e943e67937ef4124`; hidden evidence `.data/evidence_exports/e943e67937ef4124`.
- ZIP `remedy-review-20260711-132104-READY_FOR_REVIEW.zip`
  sha256 `62565a9806e16a95440cf7d70fc7422976b7a8b0ae7b9c5187ae419f78d2c2d6`.
- 24 content-proof files; 0 materialization provider calls.
- Evidence verification tests: 700 passed, 0 failed.
- All gates green; commit_execution_gate = NEEDS_HUMAN_APPROVAL; human final
  reviewer required.

## Verification (accepted)

- Focused F005 group — 127 passed.
- Stream / reviewer / retry group — 242 passed.
- Provider / planner / CLI group — 312 passed.
- compileall, `bash -n scripts/make_review_zip.sh`, `git diff --check` clean.
- Independent external validation confirmed 24/24 current content hashes.

## Status

F005 accepted and ready for commit/push/PR/merge. F006 begins only after the
F005 merge. F007 untouched.
