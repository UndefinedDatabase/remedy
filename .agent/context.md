# Context — F008 SSE event stream

## Active Branch
feature/f008-sse-event-stream, cut from `main` at the merge commit of pull
request #208, which this round merged at the Open PR Gate. Self-drive session
per docs/agents/self_drive_protocol.md: the main session plans and reviews and
writes nothing in the work tree, one delegated worker per round makes every
commit.

## Scope
In: a per-job SSE endpoint served by the existing UI server, carrying the
Part E envelope with the ledger's own monotonic seq as the event id, a 15 s
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
  tests/docs/ and tests/orchestration/test_roadmap_index.py, and a round
  rewriting `.agent/` state also gates the four files that read that state
  live: tests/orchestration/test_test_runner.py,
  tests/ui_server/test_dashboard_contract.py,
  tests/regression/test_resource_safety.py and
  tests/orchestration/test_integrity_gate.py. Destructive and red-proof checks
  run only inside a disposable git worktree under .remedy-wt/, so resource
  safety stays intact. Two pytest processes never run at once.
- THE SERVER-CAPABILITY FINDING GATES EVERYTHING: the feature file's
  Orchestrator brief dispatches it first, so R2 measures in the source whether
  ledger entries already carry a monotonic index and whether the UI server can
  hold a long-lived response without blocking every other request, and no
  endpoint is written before R3 rules the shape as a DECISION.
- This is a UI feature: docs/ui/design_reference/ is binding for every visual
  surface and assets_spec.md is the asset authority. Any deviation needs an
  assumption_log entry carrying a technical reason.
- Repository-wide `ruff check .` is RED at the claim and is NOT a gate
  (R-0364): the reviewer measured 26 errors at `8e08c0da` — 20 I001, 4 F401,
  1 UP035 and 1 F821. Ruff is gated scoped to the files a round touches,
  measured against the SAME files at the claim, so a pre-existing error is
  never read as a new one.
- 183 findings are open at this reset, all carried forward per DECISION F057
  D1, and none is a code defect of F008. R-0403, R-0607, R-0608, R-0609 and
  R-0611 stay routed to a paydown branch and are deliberately not fixed here.

## Steps
Stated once, in `.agent/plan.md`. This file tracks scope and constraints only.
