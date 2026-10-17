# Plan — scale correctness (operator order 2026-10-17, audit remedy_scale_audit_2026-10-17.md)

## Goal
Minimal correct work for small orders, reliable work for medium ones, controlled decomposition for
risky or multi-repo ones. A focused change of the lane decision, plan normalization and the
cost policy; no new orchestrator. Branch feature/scale-correctness-routing; roadmap queue F078 untouched.
`.agent/STOP` kept; no unattended loop, no real model call, no merge, no install.

## Current Step
Code, tests, docs and DECISION scale-1017 D1 to D11 are committed. The first full local run found 9
reds (structure ratchet, client interface, import allowlist, context/plan files, one HTTP test);
being repaired, then one full run again.

## Next Steps
- Repair the reds; rerun the full local gate once; record SHA, tree, commands, result.
- Scale matrix table (before/after), live_review entry, handoff.
- Push, open the PR (no merge); propose the real Pi/Ollama calibration (needs approval).

## Risks
- Verification scope by changed language/package is not built (project_tests runs one command).
- A waiting job keeps the leftover cap, not a joint one.
