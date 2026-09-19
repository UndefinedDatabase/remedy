# Handoff — F273 Findings paydown v1 · Round 7

## Session

SESSION 1 of feature F273 · round 7 · rounds so far 7

Context self-assessment: the worker read the block, AGENTS.md, DECISION F273 D7, the handback template, the questions-file rule of the self-drive protocol and both code diffs hunk by hunk as it applied them; every figure below comes from a command run in this round, and the worker's context held all of it without loss.

## Range

Review of 00b995e7..HEAD — branch `feature/f273-findings-paydown-v1`.

## Summary

Round 7 books round 6's verdict and the resolutions of the twenty findings rounds 3 to 6 landed, lands DECISION F273 D7, and builds R-0568 and the self-use track's repairs (T012 with R-0838 and R-0972) as the reviewer's dry run built them.
- C1 books Gate F273 R6 (VERDICT PASS) and twenty `Done:` lines (R-0645, R-0985, R-0839, R-0983, R-0518, R-0569, R-0649, R-0664, R-0691, R-0708, R-0734, R-0815, R-0648, R-0469, R-0482, R-0468, R-0753, R-0745, R-0685, R-0378), lands DECISION F273 D7, rewrites the plan and saves the four payload copies.
- C2 (R-0568): `FailureClass.RESOURCE_LIMIT` and `SIGNAL_GUARD_TRIP`; `FailureSignals.tripped_limit` feeds a `classify` branch below the typed exception and above the terminal status; `_completed_process_from_guarded` attaches `tripped_limit` (`TRIPPED_LIMIT_ATTR`) to the stdlib `TimeoutExpired` it raises and the `CompletedProcess` it returns; `_run_test_command` returns the trip of a failing run, `PingPongRound.test_tripped_limit` and `TaskEntry.tripped_limit` carry it (saved and loaded, absent in older records), and `build_task_rollup`'s `raw_reason` names the limit. `T2_F085.md` records that F273 T009 closes the gap.
- C3 (R-0784, R-0785, R-0786, R-0838, R-0972): Tier 1 skips any finding an existing queue entry's provenance already targets (R-0838); the generator's docstring states a builder-impossible item blocks at the approval gate by design (R-0784); `append_generated_item` writes with `ensure_ascii=False` and `scripts/self_use_queue.json` is re-serialised once that way, every parsed value unchanged except the description (R-0785), which now names both sources of an item and the generator module (R-0786); `describe_self_use_run_defects` answers a stopped job's `stop_reason`/`stop_source` and a task whose `final_status` is `stopped` (R-0972).
- C4 is this handoff.

Landed: R-0568 — `b77fec5e`
Landed: R-0784 — `8a162c39`
Landed: R-0785 — `8a162c39`
Landed: R-0786 — `8a162c39`
Landed: R-0838 — `8a162c39`
Landed: R-0972 — `8a162c39`

## Commits

### 0dbafbc2 F273 R7 C1: bookkeeping — round 6's verdict and the resolutions rounds 3 to 6 landed booked, DECISION F273 D7 landed
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f273-r7-block.md` | +108 / -0 | Byte copy of the block |
| `.agent/authored/f273-r7-decisions.md` | +40 / -0 | Byte copy of decisions.md |
| `.agent/authored/f273-r7-ledger.md` | +42 / -0 | Byte copy of ledger.md |
| `.agent/authored/f273-r7-plan.md` | +27 / -0 | Byte copy of plan.md |
| `.agent/decisions.md` | +40 / -0 | `00b995e7` bytes + decisions.md (DECISION F273 D7) |
| `.agent/live_review.md` | +42 / -0 | `00b995e7` bytes + ledger.md (Gate F273 R6, twenty `Done:` lines) |
| `.agent/plan.md` | +8 / -11 | := plan.md |

307 insertions, 11 deletions (`git show --numstat`).

### b77fec5e F273 R7 C2: R-0568 — a guard trip on a non-provider subprocess is resource_limit and the task post-mortem names the limit
| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/features/T2_F085.md` | +5 / -1 | F273 T009 closes the classification gap — `git apply .remedy-wt/f273-proto-r0568.diff` |
| `packages/orchestration/exec_guard.py` | +19 / -2 | `TRIPPED_LIMIT_ATTR`; the trip rides on the returned or raised stdlib object — same diff |
| `packages/orchestration/failure_postmortem.py` | +30 / -1 | `RESOURCE_LIMIT`, `SIGNAL_GUARD_TRIP`, `FailureSignals.tripped_limit`, the `classify` branch, rollup `raw_reason` — same diff |
| `packages/orchestration/pingpong_job.py` | +9 / -0 | `TaskEntry.tripped_limit`, saved, loaded, set from the last round — same diff |
| `packages/orchestration/pingpong_loop.py` | +17 / -9 | `_run_test_command` returns the trip; `PingPongRound.test_tripped_limit` — same diff |
| `tests/orchestration/test_exec_guard.py` | +31 / -0 | Wall and output trips carry `tripped_limit` on unchanged stdlib types — same diff |
| `tests/orchestration/test_failure_postmortem.py` | +45 / -0 | `TestGuardTrip`; the enum-reachability set includes the trip — same diff |
| `tests/orchestration/test_failure_wiring.py` | +48 / -0 | End-to-end job run: wall trip is `resource_limit`, plain failure stays `test_failed` — same diff |
| `tests/orchestration/test_pingpong.py` | +2 / -1 | The three-tuple return of `_run_test_command` — same diff |

206 insertions, 14 deletions.

### 8a162c39 F273 R7 C3: R-0784, R-0785, R-0786, R-0838, R-0972 — the self-use track stops re-selecting a targeted finding, keeps its bytes, names its generator and surfaces a stop
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/self_use_findings.py` | +27 / -12 | A stopped job and a `final_status=stopped` task are defects (R-0972) — `git apply .remedy-wt/f273-proto-t012.diff` |
| `packages/orchestration/self_use_generator.py` | +43 / -11 | Targeted-finding exclusion (R-0838), R-0784 docstring, `ensure_ascii=False` (R-0785) — same diff |
| `scripts/self_use_queue.json` | +43 / -43 | Re-serialised once without escapes (R-0785); description names both sources and the generator (R-0786) — same diff |
| `tests/orchestration/test_self_use_findings.py` | +29 / -1 | Budget-stopped run with blank errors surfaces the stop — same diff |
| `tests/orchestration/test_self_use_generator.py` | +35 / -0 | Consumed-entry target skipped; non-ASCII bytes kept on append — same diff |
| `tests/orchestration/test_self_use_queue.py` | +6 / -0 | The description names the generator module — same diff |

183 insertions, 67 deletions.

### C4 (this commit) F273 R7 C4: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C1, with 307.

## External actions

- `git worktree add --detach .remedy-wt/f273-r7-g5 8a162c39` for G5 (exit 0), then `git worktree remove .remedy-wt/f273-r7-g5` (exit 0). `git worktree list` afterwards:
  ```
  /home/decodeux/Repos/remedy                                  8a162c39 [feature/f273-findings-paydown-v1]
  /home/decodeux/Repos/remedy/.remedy-wt/f273-r7-dry           00b995e7 (detached HEAD)
  /home/decodeux/Repos/remedy/.remedy-wt/job-ebbc4e9a152746fa  00b995e7 [remedy/job-ebbc4e9a152746fa]
  ```
- After C4: `git push`. No pull request is opened.

## Verification

G1 to G5 ran at C3 `8a162c39` with a clean tree, every script with `cwd` set explicitly.

- **Transport**, before any write: `sha256sum` of the three payloads, the block and the two diffs matched the block's digests (block.md `a32582a02a09be4d77e85286ad5b38e2e97cdcfd4a5eb782ad6ead910e7b1ac5`); `wk_c1.py` re-asserted the four payload digests before writing.
- **G1**: `python3 .remedy-wt/f273-r7/wk_g1.py`, exit=0 (the C2 and C3 path sets are `git show --name-only --format=` compared with `git apply --numstat <diff>`):
  ```
  True digest plan.md
  True digest ledger.md
  True digest decisions.md
  True digest block.md
  True digest f273-proto-r0568.diff
  True digest f273-proto-t012.diff
  True plan.md == payload
  True live_review.md == base + ledger
  True decisions.md == base + decisions
  True authored f273-r7-plan.md
  True authored f273-r7-ledger.md
  True authored f273-r7-decisions.md
  True authored f273-r7-block.md
  True b77fec5e paths == numstat of f273-proto-r0568.diff
  True 8a162c39 paths == numstat of f273-proto-t012.diff
  ALL True 15
  ```
- **G2**: `git rev-parse 8a162c39:tests 8a162c39:packages 8a162c39:scripts 8a162c39:docs`, exit=0:
  ```
  f93cf09ef075d7c30bc7efbe56f14eed55194221
  a7de87d1c4ce4abf3ce2a07838fec2508c37df73
  b3754f08c41d508ebcdf0d2bedb15073e9a2dbb6
  02a05b9351d90dff4a68a0468b421365d39d6ae5
  ```
  All four equal the reviewer's dry-run subtrees.
- **G3** (primary checkout, serial, the block's 30 targets, full output in `.remedy-wt/f273-r7/wk_g3_out.txt`, 24 lines): `python3 .remedy-wt/f273-r7/wk_g3.py` running `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_applicator_fences.py ... tests/cli/test_golden_path.py`, exit=0:
  ```
  1656 passed in 213.40s (0:03:33)
  ```
  0 failed; the wrapper counted `R-0803:` lines in the full output: 0.
- **G4**: `python3 -m ruff check . --output-format concise` with `cwd` the primary checkout's root, exit=0:
  ```
  All checks passed!
  ```
- **G5** (`python3 .remedy-wt/f273-r7/wk_g5.py`, one worktree at `8a162c39`, `python3 -B -m pytest -q -p no:cacheprovider` from its root, `__pycache__` purged before every run, each FROM counted in the named file first, each reverted from its saved bytes with `git status --porcelain` empty after), exit=0:
  ```
  import path: /home/decodeux/Repos/remedy/.remedy-wt/f273-r7-g5/packages/orchestration/failure_postmortem.py
  [control] exit=0 summary: 258 passed in 4.29s
  [a] packages/orchestration/failure_postmortem.py: FROM count = 1
  [a] exit=1 summary: 6 failed, 142 passed in 0.68s
      FAILED tests/orchestration/test_failure_postmortem.py::TestClassifyEveryClass::test_every_enum_member_is_reachable
      FAILED tests/orchestration/test_failure_postmortem.py::TestGuardTrip::test_a_trip_is_resource_limit_and_the_reason_names_the_limit[wall_timeout]
      FAILED tests/orchestration/test_failure_postmortem.py::TestGuardTrip::test_a_trip_is_resource_limit_and_the_reason_names_the_limit[cpu_seconds]
      FAILED tests/orchestration/test_failure_postmortem.py::TestGuardTrip::test_a_trip_is_resource_limit_and_the_reason_names_the_limit[output_bytes]
      FAILED tests/orchestration/test_failure_postmortem.py::TestGuardTrip::test_a_trip_beats_the_test_failed_status_the_layer_gave_up_with
      FAILED tests/orchestration/test_failure_postmortem.py::TestGuardTrip::test_the_task_rollup_names_the_limit_in_its_raw_reason
  [b] packages/orchestration/pingpong_job.py: FROM count = 1
  [b] exit=1 summary: 1 failed, 59 passed in 2.58s
      FAILED tests/orchestration/test_failure_wiring.py::TestGuardTripReachesTheTaskRollup::test_a_wall_trip_on_the_test_command_is_resource_limit
  [c] packages/orchestration/self_use_generator.py: FROM count = 1
  [c] exit=1 summary: 1 failed, 21 passed in 0.30s
      FAILED tests/orchestration/test_self_use_generator.py::TestAppendGeneratedItem::test_non_ascii_it_did_not_author_keeps_its_bytes
  [d] packages/orchestration/self_use_generator.py: FROM count = 1
  [d] exit=1 summary: 1 failed, 21 passed in 0.29s
      FAILED tests/orchestration/test_self_use_generator.py::TestLedgerTierPicksTheOldestEligibleFinding::test_a_finding_a_consumed_entry_targeted_is_skipped_for_the_next
  [e] packages/orchestration/self_use_findings.py: FROM count = 1
  [e] exit=1 summary: 1 failed, 3 passed in 0.93s
      FAILED tests/orchestration/test_self_use_findings.py::TestDescribeSelfUseRunDefects::test_a_budget_stopped_run_with_blank_errors_surfaces_the_stop
  [f] scripts/self_use_queue.json: base bytes differ from C3 bytes: True
  [f] exit=1 summary: 1 failed, 23 passed in 0.29s
      FAILED tests/orchestration/test_self_use_queue.py::TestShippedQueueLoads::test_the_description_names_the_generator_that_appends_items
  ```
  The control ran over the five test files the mutations name. Every mutation went red; none stayed green. Each revert printed `git status --porcelain empty: True`. Full per-run output is in `.remedy-wt/f273-r7/wk_g5_log.txt`.
- **G6** runs after the push and is reported in the round report, because this commit precedes it.
- Full suite: not run (amend0917-throughput).

## Authored-text proofs

- Every edited `.agent/` file in C1 was built by `python3 .remedy-wt/f273-r7/wk_c1.py` from `git show 00b995e7:<path>` bytes and the payload bytes. Nothing was hand-edited. G1 re-proves every file and every `.agent/authored/f273-r7-*` copy against its payload.
- The code arrived only by `git apply` of the two reviewer-verified diffs, in the block's order. G2's subtree ids equal the reviewer's dry-run subtrees.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `0dbafbc2` |
| C2 R-0568 | done | `b77fec5e` |
| C3 R-0784, R-0785, R-0786, R-0838, R-0972 | done | `8a162c39` |
| C4 handoff + push | done | This commit, then the push |
| G1 to G5 | done | All green as above |
| G6 | done | After the push; in the round report |

## Open findings

Measured by `.remedy-wt/f273-r7/wk_measure.py`, which loads `scripts/rotate_live_review.py` by path and calls `count_open_findings` (by distinct id) on the committed `.agent/live_review.md`:
- at `8a162c39` (C1 onwards; C2 and C3 do not touch it): **103 open**;
- at `00b995e7`: 123 open.

C1's twenty `Done:` lines close twenty distinct ids and register none. The six ids landed this round (R-0568, R-0784, R-0785, R-0786, R-0838, R-0972) are still open in the ledger. Open blocker/high ids: R-0803, R-0807. Highest registered id R-0986.

## Deviations & assumptions

- **Commit sequence:** as ordered: C1 to C4, then the push. No extra commit.
- **Payload copies:** "every payload above" was read as the four files listed under PAYLOADS (plan, ledger, decisions, block), as in rounds 2 to 6. The two code diffs are listed under CODE and are not copied into `.agent/authored/`.
- **G5 FROM counts:** (a) was counted as the six named lines joined with their newlines; (b), (d) and (e) as the named whole line with its newline; (c) as the string `json.dumps(body, indent=2, ensure_ascii=False)` replaced by `json.dumps(body, indent=2)`; (f) is a whole-file replacement, so the script printed that the `00b995e7` bytes differ from C3's instead of a count. Each count was 1.
- **Scratch:** the worker's shell cwd was the reviewer's `.remedy-wt/f273-r7-dry` worktree; nothing was run in it. Every git command used `git -C` on the primary checkout and every script an explicit `cwd`. Gitignored scratch under `.remedy-wt/f273-r7/`: `wk_c1.py`, `wk_queue_check.py` (the queue re-serialisation changes only `description` among parsed values), `wk_g1.py`, `wk_g3.py`, `wk_g4.py`, `wk_g5.py`, `wk_measure.py`, and the outputs `wk_g3_out.txt`, `wk_g5_log.txt`.
- **A job worktree this round did not make:** `git worktree list` shows `.remedy-wt/job-ebbc4e9a152746fa` at `00b995e7` on branch `remedy/job-ebbc4e9a152746fa`. Its directory is dated 08:19:56, before this round's first write at 08:37:33, and both G3 and G5 ran at `8a162c39`, so it predates this round. The worker left it untouched.

## Next

1. Phase 1 rule 1 (`.agent/STOP`), then the review of round 7.

Operator questions open: 5
