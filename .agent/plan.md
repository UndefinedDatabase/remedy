# Plan — F045 Loop definitions

Branch: feature/f045-loop-definitions, cut from main at cb3ef34f. No PR open;
nothing merged this round. Next free finding ID: R-0351. Open findings: 1
(R-0350, OPEN in `.agent/live_review.md`); R-0344..R-0349 carry a `Done:` line
as of R5. The 15 carried from F115 live in git history at 57a24947.

## Goal
Recurring work gets a declarative, versionable form: a LOOP defines trigger,
scope, action, budget and stop rules in the project's config file, and
`remedy loop run` executes one as a completely normal job/mission with loop
provenance in evidence. DONE when a fixture loop validates, runs through the
standard pipeline unchanged, and an invalid spec fails validation with precise
messages before anything runs (docs/roadmap/features/T2_F045.md).

## Current Step
R6 (bookkeeping) HALTED on a block/disk contradiction before its first commit.
Block `f045-r6-1` ITEM 2 orders R-0351's paragraph written VERBATIM, and that
paragraph places `(save or _save_job)(job)` at
`packages/orchestration/loop_run.py:157`. On disk at `1a86c36d` line 157 is the
closing `)` of the `Job(...)` call; `grep -n "save or _save_job"` puts the save
at line 159. Writing the ordered bytes would put a citation into the durable
review record that does not resolve on the disk — the R-0342/R-0349 family the
block's own counter-measure exists to prevent — so nothing was registered.
Every other claim in ITEM 2 was checked against the disk and holds. Only this
halt record changed; R5 stands reviewed PASS at `1a86c36d`.

## Next Steps
1. Re-emit the R6 block with `loop_run.py:159` in R-0351's paragraph; nothing
   else in it needs to change.
2. Then R6 as ordered: register R-0351 and R-0352, fix them FIRST (thread the
   mission text and `root` into `_materialize_loop_job` so the PERSISTED job
   carries both), then the CLI (`remedy loop list | validate | run`).
3. Then the integration gate, then closure per STATUS_closure_protocol.md.

## Risks
- Loops are parsed from a config file that does not exist in this repo (no
  ./remedy.toml). Every test builds its own tmp config path; nothing may
  depend on a repo-level config file appearing.
- Schedule and event triggers are parsed and validated but INERT until the
  scheduler feature. Running one must say so honestly, never silently behave
  like a manual trigger.
- The mission path persists jobs and missions through two different root
  resolutions: `run_loop(root=X)` reaches `create_mission`/`link_job_to_mission`
  but not `_materialize_loop_job`, whose default save resolves the process-wide
  jobs dir. No caller may rely on `root` isolating a whole run until that is
  fixed. Verified on disk; not yet a registered finding — see the halt above.

Fortschritt: ~60 % (T001 ✅ · T002 ✅ · T003 läuft) — Schätzung
