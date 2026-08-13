# Plan — F045 Loop definitions

Branch: feature/f045-loop-definitions, cut from main at cb3ef34f. No PR open;
nothing merged this round. Next free finding ID: R-0357. Open findings: 5 —
R-0350, R-0353, R-0354, R-0355 and R-0356 — RECOMPUTED from
`.agent/live_review.md` this round (every `^- R-\d+ — ` paragraph minus every
`^Done: R-\d+ — ` line) rather than carried forward, which is what R-0356 is
about. R-0344..R-0349, R-0351 and R-0352 are resolved there; the 15 carried
from F115 live in git history at 57a24947.

## Goal
Recurring work gets a declarative, versionable form: a LOOP defines trigger,
scope, action, budget and stop rules in the project's config file, and
`remedy loop run` executes one as a completely normal job/mission with loop
provenance in evidence. DONE when a fixture loop validates, runs through the
standard pipeline unchanged, and an invalid spec fails validation with precise
messages before anything runs (docs/roadmap/features/T2_F045.md).

## Current Step
R10: the T003 CLI is COMPLETE — `loop list`, `loop validate` and now
`loop run <name> [--yes]`. `run` resolves the project the way every other
command group does, selects the named spec, confirms (and REFUSES to prompt
when stdin is not a terminal, so a piped run cannot hang), materializes through
`loop_run.run_loop` and STOPS: the job is PLANNED and the last line printed
names `remedy job run <id>`, so the stop is visible instead of implied.
DECISION F045 D7 records that `--yes` confirms the MATERIALIZATION
and approves nothing else. The inert-run notice is printed off
`outcome.notice`, never off the constant — R-0355's shape. A loop now reaches
a planned job through an operator-visible path, so loop_ref provenance is
exercised end to end for the first time. The feature is NOT closed.

## Next Steps
1. R11 applies the on-disk counter-measures for R-0353 and R-0356 to
   `docs/agents/planner_reviewer_prompt.md` §3 and writes the session-closing
   handoff.
2. AFTER this session: the end-to-end fixture loop through the fake-provider
   pipeline, then the integration gate, then closure per
   docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Loops are parsed from a config file that does not exist in this repo (no
  ./remedy.toml). Every test builds its own tmp config; nothing may depend on
  a repo-level config file appearing.
- Schedule and event triggers are parsed and validated but INERT until the
  scheduler feature. `loop run` says so off `LoopRunOutcome.notice`.
- `loop run` writes to the REAL job store by design (it passes no `root`), so
  every test isolates through `REMEDY_DATA_DIR`; the real-store gate proves it.

Fortschritt: ~60 % (T001 ✅ · T002 ✅ · T003 läuft) — Schätzung
