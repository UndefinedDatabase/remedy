# Plan — F045 Loop definitions

Branch: feature/f045-loop-definitions, cut from main at cb3ef34f. No PR open;
nothing merged this round. Next free finding ID: R-0348. Open findings: 4
(R-0344..R-0347, all OPEN in `.agent/live_review.md`); the 15 carried from
F115 live in git history at 57a24947.

## Goal
Recurring work gets a declarative, versionable form: a LOOP defines trigger,
scope, action, budget and stop rules in the project's config file, and
`remedy loop run` executes one as a completely normal job/mission with loop
provenance in evidence. DONE when a fixture loop validates, runs through the
standard pipeline unchanged, and an invalid spec fails validation with precise
messages before anything runs (docs/roadmap/features/T2_F045.md).

## Current Step
R3 HALTED after ITEM 1. The block was saved verbatim (split into two commits
for the 500-insertion cap); nothing after that landed. Blocker: ITEM 3 orders
DECISION F045 D5 written byte-for-byte, and its premise is contradicted by the
file it describes. `packages/orchestration/mission_state.py` lines 175-179
document that `mission_plan` (F069) was ADDED to the frozen `Mission`
dataclass as an additive optional field and that `MISSION_SCHEMA_VERSION`
"does NOT move for it" — so D5's claim that a provenance field "moves that
schema version" has a live counterexample in the same file, and D5's reversal
clause would bump a version `Mission.from_json` (line 217) uses to refuse
every existing record. D5's field list also omits `dossier_ref` and
`mission_plan`. Verbatim text is not the worker's to repair. Second blocker,
repairable: ITEM 8 names `mission_state.start_follow_up`, a name that exists
nowhere in the repo (`continue_mission` is what sets `job.mission`).

## Next Steps
1. Reviewer reissues ITEM 3's D5 with a rationale matching `mission_state.py`
   and ITEM 8 with the real function name. The conclusion (loop_ref rides on
   the JOB) is untouched by both defects.
2. Then the rest of R3 as written: R-0344..R-0347, D4, the protocol STOP
   re-check, mission-template validation, `run_loop`, `last_run_for_loop`.
3. R4 = the CLI, then the integration gate, then closure.

## Risks
- Loops are parsed from a config file that does not exist in this repo (no
  ./remedy.toml). Every test builds its own tmp config path; nothing may
  depend on a repo-level config file appearing.
- Schedule and event triggers are parsed and validated but INERT until the
  scheduler feature. Running one must say so honestly, never silently behave
  like a manual trigger.
- Action dispatch and the mission path still do NOT exist: `loop_to_job`
  refuses any kind but `job` (D3). No caller may treat it as the entry point.

Fortschritt: ~35 % (T001 ✅ · T002 ✅ · T003 offen) — Schätzung
