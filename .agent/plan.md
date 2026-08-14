# Plan — F045 Loop definitions

Branch: feature/f045-loop-definitions, cut from main at cb3ef34f. No PR open;
nothing merged this round. Next free finding ID: R-0357. Open findings: 2 —
R-0350 and R-0354 — RECOMPUTED this round from `.agent/live_review.md` (every
`^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line), never carried
forward from the previous plan. R-0353, R-0355 and R-0356 were closed at the
R12 gate by reviewer-authored `Done:` text.

## Goal
Recurring work gets a declarative, versionable form: a LOOP defines trigger,
scope, action, budget and stop rules in the project's config file, and
`remedy loop run` executes one as a completely normal job/mission with loop
provenance in evidence. DONE when a fixture loop validates, runs through the
standard pipeline unchanged, and an invalid spec fails validation with precise
messages before anything runs (docs/roadmap/features/T2_F045.md).

## Current Step
R12, bookkeeping plus the ground survey T003's last item needs. The CLI is
complete — `loop list`, `loop validate`, `loop run <name> [--yes]` — and
`loop_ref` reaches `job.metadata`, but it appears in no evidence writer and no
report builder, so the feature file's Acceptance line "loop_ref visible in
evidence and report" is NOT met yet. This round writes no production code: it
closes three findings and inventories the fake-provider pipeline into
`.agent/f045_e2e_inventory.md` so the next round can author the end-to-end
fixture test from measured facts instead of from assumptions.

## Next Steps
1. R13: the end-to-end fixture loop through the fake-provider pipeline, built
   on the inventory — a loop materializes a job, the job runs, and `loop_ref`
   is visible in evidence and in the report.
2. The integration gate (docs/agents/integration_gate.md).
3. Closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Loops are parsed from a config file that does not exist in this repo (no
  ./remedy.toml). Every test builds its own tmp config; nothing may depend on
  a repo-level config file appearing.
- Schedule and event triggers are parsed and validated but INERT until the
  scheduler feature. `loop run` says so off `LoopRunOutcome.notice`.
- `loop run` writes to the REAL job store unless given `root`, so every test
  isolates through `REMEDY_DATA_DIR` or an explicit root.
- Surfacing `loop_ref` in evidence and report may need production changes in
  modules F045 has not touched; R13 must size that before ordering it.
- This branch has carried no PR across several sessions. Whether to open one is
  the operator's call; this session did not make it either way.

Fortschritt: ~65 % (T001 ✅ · T002 ✅ · T003 läuft) — Schätzung
