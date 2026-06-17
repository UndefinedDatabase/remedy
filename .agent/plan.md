# Plan — Steps 2716-2835: Execution Approval Policy + Policy-Gated Mission Continuation v0

## Goal
Add bounded policy layer so operator can configure automatic approval metadata
for known worker/template/task combinations. Policy disabled by default.
Policy creates metadata only — never executes anything.

## Steps
- [x] Core model: ExecutionApprovalPolicy, ExecutionApprovalPolicyDecision, PolicyDecisionCode
- [x] Storage: save/load/list with secret/path rejection, atomic writes
- [x] Integrity scanner: conflicts, secrets, paths, uses, expiry
- [x] Evaluation: template→session→adapter→policies→per-condition checks
- [x] Grant: evaluate → decrement uses → approve_managed_execution()
- [x] Summary: safe export for review bundles
- [x] Default policies: 3 disabled (fixture-echo, claude-code-repair, generic-cli)
- [x] CLI commands: 6 approval.* entries in catalog + handlers in worker_facade_cmd
- [x] Contract actions: 6 APPROVAL_POLICY_* in run_contract
- [x] Mission loop: _try_policy_grant() hook at WAITING_FOR_APPROVAL + status transition
- [x] Morning report: 6 policy fields
- [x] Product spine tests: approval group + commands + handler registry
- [x] Policy model/storage/integrity/evaluation/grant tests (52 passing)
- [x] Mission loop policy tests: manual default, fixture grant, denied, no fake done (5 tests)
- [x] Morning report policy tests: fields, defaults, JSON safe (3 tests)
- [x] CLI approval tests: list/show, enable/disable, evaluate, grant, invalid IDs (13 tests)
- [x] Docs: execution-approval-policy-v0.md
- [x] Fast lane: added policy tests (472 passing, 0.77s)
- [x] Lint: ruff clean, mypy clean (192 files)
- [x] Full suite: 6961 passed, 0 failed
- [ ] Commit + PR

## Hard rules
Policy disabled by default. No auto-apply/PR/merge. Metadata only.
