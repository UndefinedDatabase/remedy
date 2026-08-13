# Plan — F045 Loop definitions

Branch: feature/f045-loop-definitions, cut from main at cb3ef34f. No PR open;
nothing merged this round. Next free finding ID: R-0357. Open findings: 5 —
R-0350, R-0353, R-0354, R-0355 and R-0356 — RECOMPUTED this round from
`.agent/live_review.md` (every `^- R-\d+ — ` paragraph minus every
`^Done: R-\d+ — ` line), never carried forward from the previous plan.

## Goal
Recurring work gets a declarative, versionable form: a LOOP defines trigger,
scope, action, budget and stop rules in the project's config file, and
`remedy loop run` executes one as a completely normal job/mission with loop
provenance in evidence. DONE when a fixture loop validates, runs through the
standard pipeline unchanged, and an invalid spec fails validation with precise
messages before anything runs (docs/roadmap/features/T2_F045.md).

## Current Step
R11, the session close. The T003 CLI is COMPLETE — `loop list`, `loop validate`
and `loop run <name> [--yes]`. This round changes no code: it puts the two
outstanding reviewer counter-measures ON DISK, where R-0347 proved they have to
live. `docs/agents/planner_reviewer_prompt.md` §3 now carries checklist item 9
(citations re-measured against the current branch's own edits, R-0353) and item
10 (the open-finding set recomputed, never carried forward, R-0354 and R-0356),
and its stale intro count went from six to ten. The session closes here at its
DECLARED round cap (self-drive protocol G7). F045 is NOT closed.

## Next Steps
1. The next session's FIRST bookkeeping act: verify this round's checklist edit
   and write the `Done:` lines for R-0353 and R-0356 in
   `.agent/live_review.md`. They stay OPEN until then — the round that applied
   the fix may not certify it.
2. The end-to-end fixture loop through the fake-provider pipeline.
3. The integration gate (docs/agents/integration_gate.md).
4. Closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Loops are parsed from a config file that does not exist in this repo (no
  ./remedy.toml). Every test builds its own tmp config; nothing may depend on
  a repo-level config file appearing.
- Schedule and event triggers are parsed and validated but INERT until the
  scheduler feature. `loop run` says so off `LoopRunOutcome.notice`.
- `loop run` writes to the REAL job store by design (it passes no `root`), so
  every test isolates through `REMEDY_DATA_DIR`.
- This branch has carried no PR across several sessions. Whether to open one is
  the operator's call; this session did not make it either way.

Fortschritt: ~60 % (T001 ✅ · T002 ✅ · T003 läuft) — Schätzung
