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
R1 (SPLIT): claim F062, then T001 — register the product-smoke
standard block into the seam F061 left in the DoD compiler; compile it
into ordered blocking checks (this round: app_starts only). app_starts
orchestrates the F007 harness verbs (start, readiness probe within the
configured window, teardown ALWAYS) with one retry after a short
backoff recorded as "passed on retry", and a port conflict reported as
a start failure carrying the harness's own reason. Two REAL fixture
mini-apps in the test tree: one starting clean, one whose unit tests
are green but whose startup is broken.

## Next Steps
- R2: T002 core_paths_respond + path extraction hand-off from the DoD
  compiler + fixtures (ok, wrong status, missing marker).
- R3: T003 clean_console + the documented pattern list +
  teardown-always (no zombie processes even on red); then the
  integration gate per docs/agents/integration_gate.md.
- R4: closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- The harness owns process semantics; the smoke only ORCHESTRATES its
  existing verbs. A diff changing harness process behaviour is out of
  scope.
- v1 is HTTP-level on purpose. Any diff pulling in a browser
  dependency is rejected at self-review; clickable flows stay in the
  DoD's runtime_flow kind.
- Teardown must run on every outcome, including failure and retry — a
  leaked process is a red result, never a quiet one.
