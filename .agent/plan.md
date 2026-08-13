# Plan — F045 Loop definitions

Branch: feature/f045-loop-definitions, cut from main at cb3ef34f. No PR open;
nothing merged this round. Next free finding ID: R-0354. Open findings: 4
(R-0350, R-0351, R-0352, R-0353, all OPEN in `.agent/live_review.md`);
R-0344..R-0349 carry a `Done:` line as of R5. The 15 carried from F115 live in
git history at 57a24947.

## Goal
Recurring work gets a declarative, versionable form: a LOOP defines trigger,
scope, action, budget and stop rules in the project's config file, and
`remedy loop run` executes one as a completely normal job/mission with loop
provenance in evidence. DONE when a fixture loop validates, runs through the
standard pipeline unchanged, and an invalid spec fails validation with precise
messages before anything runs (docs/roadmap/features/T2_F045.md).

## Current Step
R7 handed back, awaiting the reviewer's verdict. R-0351 and R-0352 are fixed in
code and pinned by tests that read the STORE: `_materialize_loop_job` now takes
`mission` and `root`, sets the mission text in the `Job(...)` constructor so the
PERSISTED record carries it, and its default save calls
`storage.save_job(job, root)`; `loop_to_job` and both `run_loop` branches thread
`root`; the post-hoc `job.mission = mission.goal` assignment is deleted.
DECISION F045 D6 records that an explicit `save` overrides `root` and is still
called with the job alone. The red-proof ran in a disposable worktree at the
pre-fix SHA and the three new tests failed there.

Open findings stay 4. R-0351 and R-0352 are repaired but NOT marked resolved:
only the reviewer writes a `Done:` line, and `.agent/live_review.md` was
deliberately left untouched this round so the fix is not self-certified.
R-0350 is untouched; R-0353's counter-measure was applied by the block author
at emission and all 12 of its citations resolved on disk.

## Next Steps
1. R8 is the CLI: `remedy loop list`, `remedy loop validate`,
   `remedy loop run <name> [--yes]`, the last-run display, and the end-to-end
   fixture loop.
2. Then the integration gate.
3. Then closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Loops are parsed from a config file that does not exist in this repo (no
  ./remedy.toml). Every test builds its own tmp config path; nothing may
  depend on a repo-level config file appearing.
- Schedule and event triggers are parsed and validated but INERT until the
  scheduler feature. Running one must say so honestly, never silently behave
  like a manual trigger.

Fortschritt: ~60 % (T001 ✅ · T002 ✅ · T003 läuft) — Schätzung
