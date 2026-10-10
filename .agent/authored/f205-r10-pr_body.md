## What and why

F205 lets one mission span several repositories. Luna's universe workspace is nine git
repositories, and most of its features change two to four of them in a fixed order, while a Remedy
job works in one repository (DECISION amend1007b D8). The inventory at the claim on `c72d2a7ec`
(`.agent/f205_inventory.md`) found that every record a mission writes already falls in a class of
the data root, so no new store and no manifest under the home folder were made.

Now:
- **Structural steps first (structure rule 2).** The mission record moved to
  `packages/orchestration/mission_record.py`; `do_sequence.py` split into `do_context.py`,
  `do_targets.py`, `do_cockpit.py`, `do_summary.py` and `do_apply.py`; what `remedy do` reads
  before any step moved to `apps/cli/commands/do_order_input.py`; the public API's write builders
  moved to `packages/orchestration/public_api_writes.py`; and one job's digest entry became
  `_job_entry`. No behaviour changed, and every row and pin they shrank fell with them;
  `mission_state.py`, `do_sequence.py` and `public_api.py` left the table.
- **The record (DECISION F205 D2).** A mission over several projects keeps its record under the
  first project its order names, with `project_ids` on the mission and each link's `project_id`
  read from the job's own record; a job of a project the mission does not span is refused with
  `MissionProjectError`. Records of one project keep their bytes.
- **The order and the walk (DECISION F205 D4).** An order file may repeat its `project` line.
  `remedy do` then plans one job per repository under one mission, applies and commits each in its
  own repository, and pushes each repository once, never forced, stopping at the first refusal;
  `--project`, `--repo` and the force flags are refused beside several projects.
- **The chain (DECISION F205 D5).** The next job of such a mission works in the project and
  repository where its chain ends.
- **The digest and the API (DECISION F205 D6).** The digest names each job's `repo_path` and each
  mission's `project_ids`; the client interface stands at `1.9`. R-1236 (High) was found and
  repaired here: the order route checked a client's policy against the first project only, and
  now resolves and checks every project an order names.
- **The upkeep and the leak regression (DECISION F205 D7).** The upkeep measures and carries the
  project where the chain ends, and a regression over a mission of two repositories holds F148's
  leak property: each project lists its own job, and the mission names the other only by reference.
- **The cockpit's chain band** moved to F305, registered directly after F205.

## Key decisions
- DECISION F205 D1: the records stay in the data root's classes, under the first project; the
  structural step comes first; the jobs follow the order's projects until F206 exists.
- DECISION F205 D2: `project_ids` and the link's `project_id`, written only on such a mission.
- DECISION F205 D3: the walk's parts leave `do_sequence.py` and `do_cmd.py` before it changes.
- DECISION F205 D4: one `project` line per project; one job per repository; one push per
  repository.
- DECISION F205 D5: the next job works where its chain ends; the loop picks no project itself.
- DECISION F205 D6: the digest names repositories; the order route checks every project.
- DECISION F205 D7: the upkeep works where the chain ends; the leak regression.

## How to review
Read DECISIONs F205 D1 to D7 in `.agent/decisions.md`, then `packages/orchestration/mission_record.py`
with `tests/orchestration/test_mission_projects.py`, then `packages/orchestration/do_targets.py` and
`packages/orchestration/do_apply.py` with `tests/cli/test_do_several_projects.py`, then
`packages/orchestration/client_digest.py` and `packages/orchestration/public_api.py` with their
tests, then `packages/orchestration/mission_upkeep.py`.

## Changed files (at the accepted head `1ee1bac31`, against the fork point `c72d2a7ec`)

| Path | Lines |
|---|---|
| `README.md` | +2 / -2 |
| `apps/cli/client_interface.py` | +20 / -4 |
| `apps/cli/commands/do_cmd.py` | +13 / -88 |
| `apps/cli/commands/do_order_input.py` | +180 / -0 |
| `docs/agents/planner_reviewer_prompt.md` | +12 / -0 |
| `docs/roadmap/STATUS.md` | +2 / -1 |
| `docs/roadmap/features/T13_F205.md` | +14 / -0 |
| `docs/roadmap/features/T13_F206.md` | +1 / -1 |
| `docs/roadmap/features/T13_F207.md` | +1 / -1 |
| `docs/roadmap/features/T13_F305.md` | +32 / -0 |
| `docs/system/machine-client-contract-v1.md` | +23 / -11 |
| `docs/system/mission-upkeep-v1.md` | +6 / -0 |
| `docs/system/structure-ledger-v1.md` | +29 / -6 |
| `packages/orchestration/client_digest.py` | +27 / -13 |
| `packages/orchestration/do_apply.py` | +234 / -0 |
| `packages/orchestration/do_cockpit.py` | +115 / -0 |
| `packages/orchestration/do_context.py` | +181 / -0 |
| `packages/orchestration/do_sequence.py` | +108 / -655 |
| `packages/orchestration/do_summary.py` | +152 / -0 |
| `packages/orchestration/do_targets.py` | +209 / -0 |
| `packages/orchestration/mission_record.py` | +328 / -0 |
| `packages/orchestration/mission_state.py` | +71 / -243 |
| `packages/orchestration/mission_upkeep.py` | +40 / -5 |
| `packages/orchestration/order_file.py` | +25 / -5 |
| `packages/orchestration/public_api.py` | +29 / -189 |
| `packages/orchestration/public_api_writes.py` | +206 / -0 |
| `scripts/self_use_queue.json` | +8 / -0 |
| `tests/cli/test_client_interface.py` | +15 / -12 |
| `tests/cli/test_do_commit_flags.py` | +2 / -1 |
| `tests/cli/test_do_several_projects.py` | +289 / -0 |
| `tests/docs/test_docs_consistency.py` | +4 / -1 |
| `tests/orchestration/import_reachability_allowlist.txt` | +8 / -0 |
| `tests/orchestration/test_client_digest.py` | +45 / -0 |
| `tests/orchestration/test_mission_contract.py` | +3 / -0 |
| `tests/orchestration/test_mission_projects.py` | +178 / -0 |
| `tests/orchestration/test_mission_upkeep.py` | +43 / -0 |
| `tests/orchestration/test_orchestrator_dispatch.py` | +22 / -0 |
| `tests/orchestration/test_order_file.py` | +14 / -2 |
| `tests/orchestration/test_serve_daemon.py` | +2 / -2 |
| `tests/test_structure_ratchet.py` | +3 / -3 |
| `tests/ui_server/test_public_api.py` | +37 / -0 |
| `.agent/` (29 files: blocks, scripts, ledger, decisions, plan, inventory, self-use record, closure suite) | +2244 / -227 |

The closing round adds the ledger's rotation, the STATUS line, the README sync, SU-055's
`consumed_by`, the Built State's closure paragraph and the handoff.

## Verification
- The closure's one full suite on the tree that ships: `22462 passed, 22 skipped`, exit 0
  (`.agent/authored/f205-closure-suite.txt`), 1228.60 CPU seconds, 1.3 percent above F302's.
- Evidence job `f205r9e1001` on `1ee1bac31`: 3124 tests, 3120 passed, 4 skipped,
  `is_valid_current_run True`.
- Package `remedy-review-20261010-182009-READY_FOR_REVIEW.zip`, SHA-256
  `c52ca63b254ed55d95b04237f6d50422f2d2f0752e4578a1a24778645335e9d3`, `READY_FOR_REVIEW`, review
  subject `c72d2a7ec`..`1ee1bac31`, 38 commits, in `/home/decodeux/Repos/remedy-history/zips`.
- Every behaviour change was mutation-checked by the reviewer in a disposable worktree: ten
  mutations in round 2, eighteen in round 4, three in round 5, four in round 6 and three in round
  7, each turning a test red.

## Latest verdict and findings
Rounds 1 to 9 reviewed; round 10, the closing round, is reviewed on this pull request. F205 is
accepted PASS_WITH_RISKS: R-1236 and R-1237 were repaired in this feature; 16 earlier findings stay
open, all owned by the findings paydown F297.

## Runtime actuals
Ten delegated rounds in one session on 2026-10-10. Provider calls F205 itself made: four, in the
closure's self-use job `0fcd1aef0852454d`, on `claude-cli` with `claude-sonnet-4-6`; the session's
own model calls are not measured by Remedy's ledger.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
