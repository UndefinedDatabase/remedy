# Context — F008 SSE event stream

## Active Branch
feature/f008-sse-event-stream, cut from `main` at `7c03adfa`, the merge commit
of pull request #208, which R1 merged at the Open PR Gate. Self-drive session
per docs/agents/self_drive_protocol.md: the main session plans and reviews and
writes nothing in the work tree, one delegated worker per round makes every
commit. The branch is mid-feature and carries no pull request.

## Scope
In: a per-job SSE endpoint served by the existing UI server, carrying the
Part E envelope with the ledger's own position as the event id, a 15 s
heartbeat frame, Last-Event-ID resume replaying the missed span out of the
ledger, 404 for an unknown job and a max-connections-per-job guard answering
429 beyond it; plus a client hook with reconnect backoff, gap detection, a
polling fallback on the same interface, and the status surface live,
reconnecting or delayed.

Out, per the feature file's Do not touch: command and write paths, the event
content and schema (Part E owns them) and the ledger format. Any POST surface
belongs to the NEXT feature and is rejected here.

## Constraints
- Merges only at the Open PR Gate; never force-push; never work on main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/** also gates
  tests/docs/ and tests/orchestration/test_roadmap_index.py — the second by
  R-0493, tests/docs/ asserting nothing about a feature file's body — and a
  round rewriting `.agent/` state or touching the UI server also gates
  tests/ui_server/, tests/orchestration/test_test_runner.py,
  tests/regression/test_resource_safety.py and
  tests/orchestration/test_integrity_gate.py. Destructive and red-proof checks
  run only inside a disposable git worktree under .remedy-wt/, so resource
  safety stays intact. Two pytest processes never run at once.
- COUNT BY PASSED-PLUS-SKIPPED. Three data-dependent `pytest.skip(...)` calls
  in tests/ui_server/test_brain_view_model.py and test_dashboard_contract.py
  make the split vary run to run at an unchanged tree, so a bare passed count
  is not a stable gate value and a skip is not a failure.
- DECISION F008 D1 IS FULLY LANDED as of R5 and both its rulings are reviewed:
  the server is threaded, so a long-lived response no longer blocks the
  cockpit, and the events reader exposes the ledger position as `seq` rather
  than assigning a counter. T001's endpoint itself is NOT built yet.
- This is a UI feature: docs/ui/design_reference/ is binding for every visual
  surface and assets_spec.md is the asset authority. Any deviation needs an
  assumption_log entry carrying a technical reason.
- Repository-wide `ruff check .` is RED and is NOT a gate (R-0364): 26 errors
  measured at the claim — 20 I001, 4 F401, 1 UP035 and 1 F821. Ruff is gated
  scoped to the files a round touches, measured against the SAME files at the
  base, so a pre-existing error is never read as a new one.
- 185 findings are open and none is a code defect of F008. R-0403, R-0607,
  R-0608, R-0609, R-0611 and R-0613 stay routed to a paydown branch, together
  with promoting the fix clauses of R-0387 and R-0573 into the §3 checklist —
  both are rules that live in a finding body, and both recurred in this
  feature because a finding body binds no later block.

## Steps
Stated once, in `.agent/plan.md`. This file tracks scope and constraints only.
