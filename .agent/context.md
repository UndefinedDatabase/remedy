# Context

## Active Branch
feature/steps-975-994-review-bundle-v1

## Scope
Steps 975-994: Review Bundle v1 + Repair Runtime Gap Closure

## Prior Step Status
Steps 905-924: PASS WITH RISKS — remedy do v1 Cohesive Flow. PR #48 merged.
Steps 925-939: PASS — remedy do v1 Truth Closure.
Steps 940-974: PASS WITH RISKS — Repair Loop v0 + Truth Closure. PR #49 merged.
  Remaining: R-0006 (Low) — no subprocess test for --fixture-patch-intent.

## Current Work
1. Close R-0006: add subprocess test for `--fixture-patch-intent --json`
2. Build Review Bundle v1: safe state package for reviewers
3. CLI command: `remedy review bundle <job_id> [--output <path>] [--json]`
4. Bundle safety: no raw content, no caches, no secrets
5. Review zip script hygiene

## Builder/Reviewer Handoff Rules
- Before final handoff, builder MUST read `.agent/live_review.md`.
- Every open finding must have `Done: R-XXXX` marker or be listed as remaining risk.
- See `.agent/review_protocol.md` for full finding format and resolution rules.

## Pre-existing Issue
`tests/orchestration/test_project_brain.py::TestFileProvenanceChain::test_full_chain_order` fails on main.

## Resource Safety
Use `scripts/remedy_pytest.sh`. No direct pytest, no background pytest, no `shell=True`.
