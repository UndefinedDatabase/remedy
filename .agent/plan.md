# Plan — operator amendment amend1024-one-real-order

## Goal
An everyday order with no header and no file path is read by a strong model, built as ONE job
by default, tried out by its builder, and lands as an applicable change. Nothing that does not
serve this is touched (operator amendment amend1024-one-real-order, 2026-10-24).

## Current Step
Parts A to F on `feature/amend1024-one-real-order`; E and F2/F5 delegated to two isolated
workers whose branches are merged into this one.

## Next Steps
1. A: claude-cli is the product default for planner, builder, reviewer, repair; the planner
   reads `[roles]` (R-1448); host_tools HTTP clients default to claude-cli, others stay as before.
2. B: the scope decision (one job unless the planner says otherwise with a reason), evidence
   `scope_decision.json`, regex lanes only as fallback; the probe test proves the new behaviour.
3. C: the claude-cli builder's Bash allowlist, documented, refusal tested and logged.
4. D: the isolation allowlist widened; a real claude call through the adapter, evidence, ADR.
5. E (worker): USD hidden unless `cost.show_usd`; advanced commands hidden; max-cost-usd discouraged.
6. F: register and close F317; park the named features (worker: dependency check, F5 apps/ui);
   F316 trimmed; ratchet rows raised with a sentence each.
7. G: the real run over the public API with a host_tools client; evidence under `evidence/current`.
8. One full suite at the end, review and repair loop until green; ruff green; merge to main.

## Risks
- The real run (G) needs the real `claude` binary and the operator's login through the adapter.
- The running serve supervisor (pid 740108, started 2026-10-20) runs old code; G needs its own server.
