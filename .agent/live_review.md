# Live Review — F062 Product smoke as the closing gate (Tier 1)

Branch: feature/f062-product-smoke
Scope: a standard DoD block proving a runnable app STARTS, its core
paths RESPOND, and the console stream is clean, before a job may end
green; not-applicable (no runtime) reported honestly, never silently
green; fixtures are real mini-apps in the test tree. v1 is
HTTP-level — no browser dependency (reject any diff adding one).

## Steps
- R1 (SPLIT): claim + T001 — standard-block registration +
  app_starts + not-applicable path + fixture apps (green-tests/
  broken-start job held open with a concrete probe reason).
- R2: T002 core_paths_respond + path extraction hand-off from the
  DoD compiler + fixtures (ok, wrong status, missing marker).
- R3: T003 clean_console + documented pattern list +
  teardown-always (no zombie processes even on red); then the
  integration gate per docs/agents/integration_gate.md.
- R4: closure per docs/roadmap/STATUS_closure_protocol.md.

## Findings
- Next free ID: R-0166.

## Verdicts
- (none yet — R1 pending)
