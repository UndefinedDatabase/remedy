## What and why

F301 makes a mission keep its project clean by itself. Before it, a mission's jobs each carried
their reviewer's findings, and nothing collected what stayed open across jobs, measured the
project's structure or scheduled any cleanup: the process that kept Remedy itself workable lived in
the build loop's documents, outside the product. Measured at the claim on `fdbf0802e`
(`.agent/f301_inventory.md`).

Now:
- **Structural steps first (structure rule 2; DECISIONs F301 D1 and D2).** The dispatch branch of `execute_move` became
  `dispatch_milestone_job` in `packages/orchestration/orchestrator_dispatch.py`; the command
  catalog's types and its `mission` group moved to `apps/cli/command_catalog_types.py` and
  `apps/cli/command_catalog_mission.py`; `ConfigKeySpec` and the mission orchestrator's keys moved to
  `packages/orchestration/config_key_spec.py` and `config_keys_mission.py`. No behaviour changed;
  every row and pin of the structure ratchet they shrank fell with them.
- **T002, the upkeep ledger (DECISIONs F301 D1 and D4).** `packages/orchestration/mission_upkeep.py`
  keeps each project's append-only `upkeep_ledger.jsonl` under the data root. A job's `job_closed`
  line, written once it has ended, or has halted while its mission moved on, holds the findings of
  its final review and of its blocked tasks' last round, and the replaced files it left.
- **T003, the cadence (DECISIONs F301 D1, D3 and D4).** The setting `mission.upkeep_every`, five unless set.
  After that many completed jobs, `remedy mission continue` and the orchestrator's dispatch make the
  next job an ordinary follow-up job whose one step lists, by fixed rules, the oldest open findings
  up to five, the longest function and code file above the structure limits, and the replaced files
  to delete. When nothing is left, no job is made and that is recorded. `--skip-upkeep <reason>` is
  the one recorded skip; the orchestrator never skips.
- **T004, replacing is deleting (narrowed by D1).** The round's hygiene rule fails a round that
  leaves a file beside the one it replaces; the halted job's line records the pair, and an upkeep
  plan carries it while both files exist.
- **T005, visible (DECISION F301 D5).** `remedy mission show` says when the next upkeep job comes and
  what it would carry; the client digest gives each mission `upkeep_every`, `upkeep_jobs_left` and
  `upkeep_open_findings`; the client interface is at 1.6. Neither writes.

## Key decisions
- DECISION F301 D1: one append-only ledger file per project, a cadence counted in a mission's
  completed jobs, and an upkeep job that is an ordinary follow-up job whose one step Remedy
  compiles; T004 narrowed to the hygiene rule and the ledger.
- DECISION F301 D2: two structural steps before the new option and key, the command catalog's
  types and `mission` group, and the config registry's key spec.
- DECISION F301 D3: the cadence's slots, the structure item and the replaced pairs, stated as rules.
- DECISION F301 D4: a job halted blocked or stopped counts as ended once a later job of its mission
  is linked (R-1234), and the orchestrator's upkeep job runs through `run_upkeep_job`.
- DECISION F301 D5: what a person and a client see, computed by `upkeep_preview` without writing.

## How to review
Read `docs/system/mission-upkeep-v1.md`, then `packages/orchestration/mission_upkeep.py` with
`tests/orchestration/test_mission_upkeep.py`, then the cadence in `apps/cli/commands/mission_cmd.py`
and `dispatch_milestone_job`, then `tests/regression/test_f301_acceptance.py`, which walks a
mission of six jobs through the command line.

## Changed files (at the accepted head `1a49c7938`, against the fork point `fdbf0802e`)

| Path | Lines |
|---|---|
| `apps/cli/client_interface.py` | +6 / -2 |
| `apps/cli/command_catalog.py` | +34 / -394 |
| `apps/cli/command_catalog_mission.py` | +252 / -0 |
| `apps/cli/command_catalog_types.py` | +172 / -0 |
| `apps/cli/commands/mission_cmd.py` | +91 / -7 |
| `docs/README.md` | +2 / -0 |
| `docs/agents/planner_reviewer_prompt.md` | +10 / -0 |
| `docs/guides/environment.md` | +1 / -0 |
| `docs/roadmap/STATUS.md` | +1 / -1 |
| `docs/roadmap/features/T7_F301.md` | +63 / -0 |
| `docs/system/machine-client-contract-v1.md` | +4 / -4 |
| `docs/system/mission-upkeep-v1.md` | +78 / -0 |
| `docs/system/structure-ledger-v1.md` | +17 / -6 |
| `packages/orchestration/client_digest.py` | +11 / -1 |
| `packages/orchestration/config.py` | +5 / -57 |
| `packages/orchestration/config_key_spec.py` | +44 / -0 |
| `packages/orchestration/config_keys_mission.py` | +51 / -0 |
| `packages/orchestration/lessons.py` | +4 / -3 |
| `packages/orchestration/mission_upkeep.py` | +490 / -0 |
| `packages/orchestration/orchestrator_dispatch.py` | +108 / -0 |
| `packages/orchestration/orchestrator_loop.py` | +6 / -47 |
| `packages/orchestration/role_config.py` | +2 / -2 |
| `scripts/self_use_queue.json` | +8 / -0 |
| `tests/cli/test_client_interface.py` | +1 / -1 |
| `tests/cli/test_mission_cmd.py` | +156 / -0 |
| `tests/cli/test_status_cmd.py` | +9 / -0 |
| `tests/orchestration/import_reachability_allowlist.txt` | +6 / -0 |
| `tests/orchestration/test_lessons.py` | +8 / -0 |
| `tests/orchestration/test_mission_upkeep.py` | +669 / -0 |
| `tests/orchestration/test_orchestrator_dispatch.py` | +163 / -0 |
| `tests/regression/test_f301_acceptance.py` | +158 / -0 |
| `tests/test_structure_ratchet.py` | +3 / -3 |
| `.agent/` (30 files: blocks, ledger, decisions, plan, inventory, self-use record, closure suite) | +2502 / -222 |

The closing round adds the ledger's rotation, the STATUS line, the README sync, SU-053's
`consumed_by`, the Built State's closure paragraph and the handoff.

## Verification
- The closure's one full suite on the tree that ships: `22362 passed, 22 skipped`, exit 0
  (`.agent/authored/f301-closure-suite.txt`), 1228.95 CPU seconds, 2.8 percent below F300's.
- Evidence job `f301r10e1001` on `1a49c7938`: 3120 node ids, 3116 passed, 4 skipped,
  `is_valid_current_run True`.
- Package `remedy-review-20261010-061122-READY_FOR_REVIEW.zip`, SHA-256
  `d3512a9709dbfda22fb99e99dd2a172c2122e81d8eec24c4fa205b252f267ba5`, `READY_FOR_REVIEW`, review
  subject `fdbf0802e`..`1a49c7938`, in `/home/decodeux/Repos/remedy-history/zips`.
- Every production change was mutation-proved by the reviewer in a disposable worktree; the
  acceptance test's eight mutations each turn it red.

## Latest verdict and findings
Rounds 1 to 10 reviewed; round 11, the closing round, is reviewed on this pull request. F301 is
accepted PASS_WITH_RISKS: its own findings R-1233 and R-1234 are resolved, and 15 findings stay
open, all owned by the findings paydown F297.

## Runtime actuals
Eleven delegated rounds in two sessions on 2026-10-10; the self-use job measured 2 provider calls
and 9926 tokens on `claude-cli` with `claude-sonnet-4-6`; the session's own model calls are not
measured by Remedy's ledger.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
