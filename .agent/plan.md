# Plan — F045 Loop definitions

Branch: feature/f045-loop-definitions, cut from main at cb3ef34f. No PR open;
nothing merged this round. Next free finding ID: R-0355. Open findings: 2 —
R-0350 and R-0354, both OPEN in `.agent/live_review.md`, both Low. R-0344..R-0349,
R-0351 and R-0352 each carry a `Done:` line there. The 15 carried from F115 live
in git history at 57a24947.

## Goal
Recurring work gets a declarative, versionable form: a LOOP defines trigger,
scope, action, budget and stop rules in the project's config file, and
`remedy loop run` executes one as a completely normal job/mission with loop
provenance in evidence. DONE when a fixture loop validates, runs through the
standard pipeline unchanged, and an invalid spec fails validation with precise
messages before anything runs (docs/roadmap/features/T2_F045.md).

## Current Step
R8 landed the READ-ONLY half of the T003 CLI. `apps/cli/commands/loop_cmd.py`
adds `remedy loop list` (name, trigger with an `inert` mark, action kind, and
the last run read from the job store through `last_run_for_loop`) and
`remedy loop validate` (every error on stderr, nonzero exit; a clean config says
how many loops validated). Both are reachable through `collect_all_handlers`,
registered in BOTH the import list and the module tuple, and both are in
`CATALOG` as `read_only` under a new `loop` group. `tests/cli/test_loop_cmd.py`
drives them through that registered table, never through a `_cmd_*` import, and
went red in a disposable worktree at the pre-wiring SHA.

The reviewer closed R-0351 and R-0352 in `.agent/live_review.md` with its own
verified text after re-running R7's proof itself; R-0354 was registered in the
same commit. Open findings are now exactly two: R-0350 and R-0354.

## Next Steps
1. R9 is `remedy loop run <name> [--yes]` plus the end-to-end fixture loop
   through the fake-provider pipeline.
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
