# Plan — Steps 5961-6020 — F005 — Enforced structured outputs

## Goal
Replace fragile free-text Reviewer and Planner parsing with small enforced JSON
schemas. Every structured provider call sends a JSON schema, carries a compact
`schema_v`, validates the returned value, classifies invalid data as error class
`parse`, allows at most one logical parse retry, and never enters an unbounded
repair loop. Schemas stay deliberately small.

## Current Step
**F005 ACCEPTED — external verdict `PASS_WITH_RISKS — ACCEPTED`.
Ready for commit / push / PR / merge.**

## Accepted evidence
- Manual completion job `e943e67937ef4124` (3 non-overlapping scopes, 24
  content-proof files, **0 materialization provider calls**).
  Hidden evidence: `.data/evidence_exports/e943e67937ef4124`.
- ZIP `remedy-review-20260711-132104-READY_FOR_REVIEW.zip`
  sha256 `62565a9806e16a95440cf7d70fc7422976b7a8b0ae7b9c5187ae419f78d2c2d6`.
- Gates: package_status READY_FOR_REVIEW · evidence_authoritative true ·
  review_bundle_integrity PASS · alignment PASS · final_verifier PASS_WITH_RISKS ·
  artifact_contract / change_provenance / fresh_evidence / runtime_integration
  PASS · commit_execution_gate NEEDS_HUMAN_APPROVAL · hash mismatches [] ·
  missing proofs [] · uncovered files [] · human final review required.
- Evidence verification tests: **700 passed, 0 failed**.

## Delivered
- `schemas/` — compact models with a REQUIRED top-level `schema_v`
  (ReviewVerdict `rv1`, PlannerPlan `pp1`, DesignSpec `ds1` placeholder), strict
  extra-field rejection, JSON-schema export, and a `validate_response` primitive
  that classifies any bad response as error class `parse` with a concise hint.
- Native provider schema enforcement: Claude CLI `--json-schema` (JSON and
  stream modes, reading `structured_output`) and Ollama `format=<schema>`.
- Hard maximum of ONE logical parse retry; transport retries stay separate.
- Native structured-output exhaustion is classified `parse` (not a provider
  error) on exit 0 and nonzero, and its Usage/cost are retained so failed
  structured calls still count toward token/cost totals.
- One prompt-trace entry per ACTUAL provider call (Reviewer and Planner),
  carrying `schema_v`, phase and transport-attempt, with prompt hashes equal to
  the exact strings sent.
- Legacy free-text paths remain, behind explicit compatibility flags only.

## Tests (accepted)
- Focused F005 group — 127 passed.
- Stream / reviewer / retry group — 242 passed.
- Provider / planner / CLI group — 312 passed.
- compileall, `bash -n scripts/make_review_zip.sh`, `git diff --check` clean.

## Next
Commit, push, open the F005 PR, apply the Open PR Gate, merge. After merge start
**F006 — Worktree isolation per run** on `feature/f006-worktree-isolation`.

## Hard Rules
No Fable; no nested Builders/Reviewers/subagents; no `job-flow`/`job-run` for
implementation. Do not touch F007. F004 accepted/merged (PR #124, merge commit
`cb55909`).
