# Plan — Steps 1681-1716: External Builder Sandbox v0

## Goal
First SAFE ingress for EXTERNAL builder work. Remedy can export a safe request package to an
external worker (Claude/Pi/another agent/human) and ingest the worker's result — but the result
stays fully UNTRUSTED until it passes the same quarantine → Trust Gate → Verification →
Materialization → (human) Approval → do_continue path as local candidates. Worker execute,
Remedy governs.

## Core principle
External builder output is untrusted input. No execution in Remedy. Routing feedback is read-only
confidence only — never starts work. Approval + apply stay separate.

## Current Step
1706 — code/tests/docs complete; handoff; reviewer owns verdict; PR HELD

## Steps
- [x] 1681: merge closure (PR #67 PASS → main 7cec21c; fresh branch) [user-confirmed merge]
- [x] 1682: scope contract doc (external-builder-sandbox-v0.md) — anti-goals explicit
- [x] 1683-1685: models (request package / submission) + safe export + private storage
- [x] 1688: bridge into existing trust/verification/materialization seams (provider label external_builder:<src>)
- [x] 1686-1687: CLI package-create/show/list + submit + submission-show/list + evaluate + integrity; catalog; run_contract (no execution)
- [x] 1689: candidate_quality external-submission evaluation (model/route override; same ceilings)
- [x] 1690: builder_routing read-only external feedback (poor→human review; never starts work)
- [x] 1691-1693: progress/feature/review-bundle(28)/cockpit
- [x] 1695: integrity invariants (no submission without package; no raw markers/abs paths in public)
- [x] 1696: external-builder-worker-contract-v0 doc
- [x] 1697-1703,1705: tests (26 unit + 7 CLI + bundle/cockpit; redaction-torture; arch; smoke) + full pytest once (5969 passed)
- [x] 1704,1706: changed-files table (context.md) + final report
- [ ] 1707-1716: reserved for reviewer findings (R-0091+)

## Product readiness
External Builder Sandbox v0 complete: safe request-package export + bounded/protected untrusted
candidate ingress → existing Trust Gate + Verification + Materialization + human approval; quality
evaluation of external submissions; read-only routing feedback. No execution/apply/approve/test/
git/PR. Readiness ~85% (ingress rail complete; tournament harness deferred). Next: Model/Route
Tournament Harness v0 (only if this block PASS).

## Hard rules
- NO provider/model calls, network, browser, subprocess, shell=True.
- NO apply / approve / reject / test-run / git / PR / merge.
- NO automatic generation / repair / materialization-without-existing-approval-gates.
- External output ALWAYS untrusted; raw candidate quarantined privately, never rendered.
- Routing feedback only influences confidence/recommendation, never starts work.
- No raw prompt/candidate/diff/stdout/stderr/traceback/secrets/abs paths in public surfaces.
- Every next_safe_action catalog-backed + entity-backed.
- Tests via scripts/remedy_pytest.sh; full suite at most once at end. No background pytest.
- NO PR unless the user explicitly asks.

## Next block
Model/Route Tournament Harness v0 (only if this block PASS).
