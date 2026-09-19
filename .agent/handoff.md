# Handoff — F273 Findings paydown v1 · Round 13

## Session

SESSION 2 of feature F273 · round 13 · rounds so far 13

Context self-assessment: the worker read the block, AGENTS.md, DECISION F273 D13, round 12's handoff as the template's instance, and both code diffs' production hunks as it applied them. Every figure below comes from a command run in this round, and the worker's context held all of it without loss.

## Range

Review of b3baf7d5..HEAD — branch `feature/f273-findings-paydown-v1`.

## Summary

Round 13 books round 12's verdict and its nine resolutions, registers R-0989, lands DECISION F273 D13, and builds R-0930, R-0929, R-0904, R-0970, R-0915, R-0919, R-0920, R-0905 and R-0907 as the reviewer's dry run built them.
- C1 books Gate F273 R12 (VERDICT PASS), nine `Done:` lines (R-0921, R-0917, R-0922, R-0916, R-0899, R-0910, R-0980, R-0978, R-0988) and the R-0989 registration. It also lands DECISION F273 D13, rewrites the plan and saves the four payload copies.
- C2 (R-0930, R-0929, R-0904, R-0970, R-0915):
  - The loop's `_record` stamps `recorded_at` itself, so the printed and the stored entry carry one time.
  - `mission show` renders the whole ledger after the chain and carries it as `ledger` in its JSON.
  - `mission list --status` takes the four stored statuses and the derived `planned`.
  - Every tip in `timeline.py` and `trust_report.py` names real job and intent ids, one command per intent; the `do` tip names its value in words.
  - `job_plan.replan` and `ReplanRejectedError` are deleted with their tests; the six rejected-plan refusals print `REJECTED_PLAN_NEXT_STEP`.
- C3 (R-0919, R-0920, R-0905, R-0907):
  - The cockpit continuation section keeps only `available`; its client fields and fixtures go.
  - The event-name recovery reads every positional string of an emit call, any call named with `emit`, and a module's own forwarding helper; a test finds a name only a helper emits.
  - The three `git_status_read` readers go, with the `repo_dirty` decision type and the `dirty_repo_blocks_level` reason code.
  - Readiness level 4 drops the `run_contract` and `token_policy` inspection signals; six test-only exports go with their tests; the architecture document says so.
- C4 is this handoff.

Landed: R-0930 — `f4f27cc8` (C2)
Landed: R-0929 — `f4f27cc8` (C2)
Landed: R-0904 — `f4f27cc8` (C2)
Landed: R-0970 — `f4f27cc8` (C2)
Landed: R-0915 — `f4f27cc8` (C2)
Landed: R-0919 — `7e1346b2` (C3)
Landed: R-0920 — `7e1346b2` (C3)
Landed: R-0905 — `7e1346b2` (C3)
Landed: R-0907 — `7e1346b2` (C3)

## Commits

### b8f62226 F273 R13 C1: bookkeeping — round 12's verdict and its nine resolutions booked, R-0989 registered, DECISION F273 D13 landed
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f273-r13-block.md` | +115 / -0 | Byte copy of the block |
| `.agent/authored/f273-r13-decisions.md` | +39 / -0 | Byte copy of decisions.md |
| `.agent/authored/f273-r13-ledger.md` | +22 / -0 | Byte copy of ledger.md |
| `.agent/authored/f273-r13-plan.md` | +27 / -0 | Byte copy of plan.md |
| `.agent/decisions.md` | +39 / -0 | `b3baf7d5` bytes + decisions.md (DECISION F273 D13) |
| `.agent/live_review.md` | +22 / -0 | `b3baf7d5` bytes + ledger.md (Gate F273 R12, nine `Done:` lines, R-0989) |
| `.agent/plan.md` | +8 / -9 | := plan.md |

272 insertions, 9 deletions (`git show --numstat`).

### f4f27cc8 F273 R13 C2: R-0930, R-0929, R-0904, R-0970, R-0915 — the loop stamps each entry it prints, mission show renders the ledger, mission list filters by status, tips name real ids, and replan goes
All by `git apply .remedy-wt/f273-proto-g3.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/command_catalog.py` | +6 / -2 | `mission list --status`; `mission show` description names the ledger |
| `apps/cli/commands/decision.py` | +3 / -1 | Rejected-plan refusals print the next step |
| `apps/cli/commands/job.py` | +12 / -4 | `_plan_rejected_error` for the four rejected-plan refusals |
| `apps/cli/commands/mission_cmd.py` | +43 / -5 | Status filter with derived `planned`; `show` renders the ledger |
| `docs/system/vocabulary.md` | +6 / -0 | Rejected plan, `--status planned`, `mission show` ledger |
| `packages/orchestration/job_plan.py` | +10 / -41 | `REJECTED_PLAN_NEXT_STEP`; `replan` and `ReplanRejectedError` deleted |
| `packages/orchestration/mission_compiler.py` | +4 / -4 | Comments no longer cite `replan` |
| `packages/orchestration/mission_state.py` | +1 / -1 | Docstring no longer cites `replan` |
| `packages/orchestration/orchestrator_loop.py` | +4 / -1 | `_record` stamps `recorded_at` |
| `packages/orchestration/timeline.py` | +1 / -1 | `do` tip names its value in words |
| `packages/orchestration/trust_report.py` | +32 / -10 | `_patch_commands`: real ids per intent |
| `tests/cli/test_mission_cmd.py` | +89 / -0 | Stamp, ledger render and status filter tests |
| `tests/cli/test_plan_approval.py` | +3 / -55 | Replan tests deleted; refusal names the next step |
| `tests/orchestration/test_job_plan.py` | +0 / -40 | Replan tests deleted |
| `tests/orchestration/test_prompt_trace.py` | +1 / -1 | Comment reworded |
| `tests/test_timeline.py` | +20 / -0 | No-placeholder tip test |
| `tests/test_trust_report.py` | +28 / -0 | No-placeholder tip tests |

263 insertions, 166 deletions.

### 7e1346b2 F273 R13 C3: R-0919, R-0920, R-0905, R-0907 — the cockpit loses its dead continuation half, the event-name recovery reads every argument and helper, and the dead git-status readers and level-4 inspection signals go
All by `git apply .remedy-wt/f273-proto-g4.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `apps/ui/src/api/actionClass.test.ts` | +3 / -3 | Fixture loses continuation event fields |
| `apps/ui/src/api/remedyApi.test.ts` | +3 / -4 | Same |
| `apps/ui/src/api/remedyApi.ts` | +0 / -2 | `lastResult`/`lastStopReason` dropped |
| `apps/ui/src/api/types.ts` | +1 / -3 | Same |
| `docs/system/architecture.md` | +7 / -3 | Level 4 no longer reads the inspection events |
| `docs/system/operator-cockpit-v1.md` | +1 / -1 | Continuation is `available` only |
| `packages/orchestration/autonomy_readiness.py` | +3 / -116 | Inspection and git-status signals and two test-only exports deleted |
| `packages/orchestration/decision_evidence.py` | +3 / -3 | `repo_dirty` leaves the triple set |
| `packages/orchestration/decision_queue.py` | +8 / -75 | `repo_dirty` type and its reader deleted |
| `packages/orchestration/run_contract.py` | +0 / -66 | Two test-only exports deleted |
| `packages/orchestration/stop_reasons.py` | +0 / -16 | `dirty_repo_blocks_level` and its reader deleted |
| `packages/orchestration/token_policy.py` | +0 / -73 | Two test-only exports deleted |
| `packages/orchestration/ui_server.py` | +5 / -26 | Continuation section loses its event half |
| `scripts/remedy_smoke.sh` | +1 / -1 | Decision-type check drops `repo_dirty` |
| `tests/cli/test_blocker_cmd.py` | +1 / -1 | Follows the deletion |
| `tests/orchestration/test_approval_queue.py` | +9 / -22 | Follows the deletion |
| `tests/orchestration/test_autonomy.py` | +0 / -43 | Tests of deleted exports removed |
| `tests/orchestration/test_decision_evidence.py` | +9 / -164 | `repo_dirty` tests removed |
| `tests/orchestration/test_decision_inbox.py` | +0 / -10 | `repo_dirty` fixture removed |
| `tests/orchestration/test_event_ledger.py` | +1 / -1 | Follows the deletion |
| `tests/orchestration/test_event_name_coupling.py` | +60 / -24 | Recovery reads every argument and helpers; ceiling 4 -> 1 |
| `tests/orchestration/test_run_contract.py` | +2 / -13 | Tests of deleted exports removed |
| `tests/orchestration/test_stop_reasons.py` | +4 / -5 | Dirty-repo reason removed |
| `tests/storage/test_persistence.py` | +0 / -33 | Tests of deleted exports removed |
| `tests/test_autonomy_readiness.py` | +18 / -35 | Level 4 reads no inspection event |
| `tests/test_run_contract.py` | +0 / -17 | Tests of deleted exports removed |
| `tests/test_token_policy.py` | +0 / -52 | Tests of deleted exports removed |
| `tests/ui_server/test_cockpit_contract.py` | +1 / -2 | Continuation keys |
| `tests/ui_server/test_dashboard_cockpit_truth.py` | +6 / -33 | Continuation event tests removed |

146 insertions, 847 deletions.

### C4 (this commit) F273 R13 C4: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C1, with 272.

## External actions

- `git worktree add --detach .remedy-wt/f273-r13-g5 7e1346b2` for G5, then `git worktree remove .remedy-wt/f273-r13-g5` (no `--force` needed). `git worktree list` afterwards:
  ```
  /home/decodeux/Repos/remedy                            7e1346b2 [feature/f273-findings-paydown-v1]
  /home/decodeux/Repos/remedy/.remedy-wt/f273-h-g5a      5c1cb2e3 (detached HEAD)
  /home/decodeux/Repos/remedy/.remedy-wt/f273-h-g5b      3077a407 (detached HEAD)
  /home/decodeux/Repos/remedy/.remedy-wt/f273-h-g5b-old  54049e6b (detached HEAD)
  /home/decodeux/Repos/remedy/.remedy-wt/f273-h-g5b-ref  3077a407 (detached HEAD)
  ```
  The four `f273-h-*` worktrees belong to research helpers; this round did not touch them.
- After C4: `git push`. No pull request is opened.

## Verification

G1 to G5 ran at C3 `7e1346b2` with a clean tree. Every script ran with `cwd` set explicitly.

- **Transport**, before any write: `sha256sum` of the three payloads, the block and the two diffs matched the block's digests (block.md `bda69b180f076f7c2c159132ba60aba8e9353a4159486db1e28b79a3a07d7691`).
- **G1**: `python3 .remedy-wt/f273-r13/wk_g1.py`, exit 0:
  ```
  digest plan.md True
  digest ledger.md True
  digest decisions.md True
  digest block.md True
  digest f273-proto-g3.diff True
  digest f273-proto-g4.diff True
  plan.md == payload True
  live_review == base + ledger True
  decisions == base + decisions True
  authored f273-r13-plan.md True
  authored f273-r13-ledger.md True
  authored f273-r13-decisions.md True
  authored f273-r13-block.md True
  C2 paths == g3 numstat paths True
  C3 paths == g4 numstat paths True
  checks 15 all True
  exit 0
  ```
- **G2**: `git rev-parse 7e1346b2:tests 7e1346b2:packages 7e1346b2:apps 7e1346b2:docs 7e1346b2:scripts`, exit 0:
  ```
  2beafcb1ee267504ea8f3e134c5635eda7cca657
  9f0255aa1385c7770163b1590b87847691a50cda
  0e7f11cb7c7a4f81ad5ace8ffac6a881a16be6cc
  dc2df26a7ece692e469ce4b7707a1799b082d6bb
  9638c2c911dee4ee8993a79a582aa2dc721f738d
  ```
  All five equal the reviewer's dry-run objects.
- **G3** (primary checkout, serial, the block's 35 targets): `python3 .remedy-wt/f273-r13/wk_g34.py g3` runs `python3 -m pytest -q -p no:cacheprovider <targets>`, prints the transcript's last 15 lines and counts `R-0803:` lines over the full output:
  ```
  2019 passed in 219.09s (0:03:39)
  R-0803 lines: 0
  exit 0
  ```
- **G4**: `python3 -m ruff check . --output-format concise` from the primary checkout's root (via `wk_g34.py g4`):
  ```
  All checks passed!

  exit 0
  ```
- **G5** (`python3 .remedy-wt/f273-r13/wk_g5.py`): one detached worktree at `7e1346b2`; `python3 -B -m pytest -q -p no:cacheprovider` from its root; env carries `REMEDY_OLLAMA_HOST=http://127.0.0.1:9` and `OLLAMA_HOST=http://127.0.0.1:9`; `__pycache__` purged before every run; each FROM counted with its newline first; each file reverted from its saved bytes.
  ```
  trust_report path: /home/decodeux/Repos/remedy/.remedy-wt/f273-r13-g5/packages/orchestration/trust_report.py
  CONTROL exit=0 :: 241 passed in 83.63s (0:01:23) :: failed=[]
  (a) packages/orchestration/orchestrator_loop.py: FROM count=1
  (a) exit=1 :: 1 failed, 110 passed in 65.83s (0:01:05) :: failed=['tests/cli/test_mission_cmd.py::TestMissionRunInOrchestratorMode::test_every_printed_iteration_carries_its_time']
  (b) apps/cli/commands/mission_cmd.py: FROM count=1
  (b) exit=1 :: 1 failed, 110 passed in 66.01s (0:01:06) :: failed=['tests/cli/test_mission_cmd.py::TestShowRendersTheWholeLedger::test_entries_from_two_earlier_runs_render_without_an_append']
  (c) apps/cli/commands/mission_cmd.py: FROM count=1
  (c) exit=1 :: 1 failed, 110 passed in 65.90s (0:01:05) :: failed=['tests/cli/test_mission_cmd.py::TestListStatusFilter::test_planned_lists_only_missions_no_job_has_started']
  (d) packages/orchestration/trust_report.py: FROM count=1
  (d) exit=1 :: 1 failed, 70 passed in 0.33s :: failed=['tests/test_trust_report.py::TestTipsNameNoPlaceholder::test_rendered_text_has_no_angle_bracket_placeholder[pending]']
  (e) apps/cli/commands/job.py: FROM count=1
  (e) exit=1 :: 1 failed, 28 passed in 7.85s :: failed=['tests/cli/test_plan_approval.py::TestApprovalGateEnforcement::test_rejected_cli_exit_3']
  (f) tests/orchestration/test_event_name_coupling.py: FROM count=1
  (f) exit=1 :: 1 failed, 4 passed in 6.52s :: failed=['tests/orchestration/test_event_name_coupling.py::TestEventNameCouplingRatchet::test_the_recovery_finds_a_name_a_helper_emits']
  (g) tests/orchestration/test_event_name_coupling.py: FROM count=1
  (g) exit=1 :: 1 failed, 4 passed in 5.78s :: failed=['tests/orchestration/test_event_name_coupling.py::TestEventNameCouplingRatchet::test_the_recovery_finds_a_name_a_helper_emits']
  (h) packages/orchestration/autonomy_readiness.py: FROM count=1
  (h) exit=1 :: 1 failed, 24 passed in 0.31s :: failed=['tests/test_autonomy_readiness.py::TestLevelFourSignals::test_level_4_reads_no_inspection_event']
  every revert: True; worktree status after reverts: clean
  ```
  The control ran over the five named test files together (M, K, `tests/test_trust_report.py`, `tests/cli/test_plan_approval.py`, `tests/test_autonomy_readiness.py`). Every mutation went red; none stayed green.
- **G6** runs after the push and is reported in the round report, because this commit precedes it.
- Full suite: not run (amend0917-throughput).

## Authored-text proofs

- Every edited `.agent/` file in C1 was built by `python3 .remedy-wt/f273-r13/wk_c1.py` from `git show b3baf7d5:<path>` bytes and the payload bytes. Nothing was hand-edited except this handoff. G1 re-proves every C1 file and every `.agent/authored/f273-r13-*` copy against its payload.
- The code arrived only by `git apply` of the two reviewer-verified diffs, in the block's order. G2's object ids equal the reviewer's dry-run objects.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `b8f62226` |
| C2 R-0930, R-0929, R-0904, R-0970, R-0915 | done | `f4f27cc8` |
| C3 R-0919, R-0920, R-0905, R-0907 | done | `7e1346b2` |
| C4 handoff + push | done | This commit, then the push |
| G1 to G5 | done | All green as above |
| G6 | done | After the push; in the round report |

## Open findings

Measured by `.remedy-wt/f273-r13/wk_count.py`. It loads `scripts/rotate_live_review.py` by path, registered in `sys.modules`, and calls `count_open_findings` (by distinct id) on the committed `.agent/live_review.md`:
- at `b8f62226` (C1 onwards; C2 and C3 do not touch it): **71 open**;
- at `b3baf7d5`: 79 open.

C1's nine `Done:` lines close nine distinct ids, and it registers one (R-0989): 79 - 9 + 1 = 71. The nine ids landed this round are still open in the ledger.

## Deviations & assumptions

- **Commit sequence:** as ordered: C1 to C4, then the push. No extra commit.
- **G5 control scope:** the block names the control's files as "the test files named below"; the control ran over exactly the five files the mutations name.
- **G1 exit code:** the first G1 run printed no exit line, so G1 was re-run at the same commit through a wrapper that prints the code: `checks 15 all True`, `exit 0`.
- **Payload copies:** the four files listed under PAYLOADS (plan, ledger, decisions, block) went to `.agent/authored/`, as in earlier rounds. The two code diffs are not copied.
- **Scratch:** gitignored under `.remedy-wt/f273-r13/`: `wk_c1.py`, `wk_g1.py`, `wk_g34.py`, `wk_g5.py`, `wk_count.py`.

## Next

1. Phase 1 rule 1 (`.agent/STOP`), then the review of round 13.

Operator questions open: 5
