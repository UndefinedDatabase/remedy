# Plan — F062 Product smoke as the closing gate

## Goal
Green tests can still mean a broken product. For jobs touching a
runnable app, a standard DoD block proves the app STARTS, its core
paths RESPOND, and the console stream is free of errors, before the
job may end green. DONE when a fixture app with green unit tests but a
broken startup keeps its job OPEN and the smoke's finding reads
concretely ("start failed: <probe reason>"), not vaguely. No runtime
configured → "smoke: not applicable (no runtime configured)", honest
and non-gating, never silently green.

## Current Step
R2 (LARGE): R-0166 fix (push first), then T002 core_paths_respond —
closed probe vocabulary, path hand-off from intent/plan, OK-status
rule, fixtures for ok / wrong status / missing marker; then T003
clean_console — a small documented CASE-SENSITIVE pattern base that
config EXTENDS but never replaces, red with the matched lines quoted,
plus the smoke config table (enabled, paths override, error-pattern
additions, readiness window); then the integration gate per
docs/agents/integration_gate.md. Per-slice verification, stop-on-red.

## Next Steps
- R3: closure per docs/roadmap/STATUS_closure_protocol.md (its own
  round: Built State, preconditions, evidence job, review zip,
  STATUS [x] + README sync, PR).

## Risks
- The harness owns process semantics; the smoke only ORCHESTRATES its
  existing verbs. A diff changing harness process behaviour is out of
  scope.
- v1 is HTTP-level on purpose. Any diff pulling in a browser
  dependency is rejected at self-review; clickable flows stay in the
  DoD's runtime_flow kind.
- Teardown must run on every outcome, including failure and retry — a
  leaked process is a red result, never a quiet one.
