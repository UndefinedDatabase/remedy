# Handoff — F269 Contract & contract templates · Round 1 (T001)

## Session

SESSION 1 of feature F269 · round 1 · rounds so far 1

Context self-assessment: the round fit comfortably in one worker context; every gate below was run in this session, and none was carried over from memory.

## Range

Review of 0955dd4c..HEAD — branch `feature/f269-contract`.

## Summary

Round 1 claims F269 and lands T001:

- C1 claims F269: the payload byte copies, plan, context, the live-review re-head with F268 round 13's verdict, DECISIONs F269 D2 and D3, and STATUS `[~]`.
- C2a adds `packages/orchestration/mission_contract.py`, the contract record per D2 and D3 (1)(2). Only two docstrings change in `mission_state.py`.
- C2b adds its tests.
- C3 makes the orchestrator's `MOVE_DISPATCH_JOB` branch record `metadata["milestone_id"]` on the dispatched job.
- C4 adds `remedy mission contract` and `remedy job contract`, and regenerates the reachability allowlist.
- C5 is this handoff.

## Commits

### 040c4ff2 F269 R1 C1: claim F269 — plan, context, live review re-head, DECISIONs D2 and D3, STATUS in progress
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f269-r1-block.md` | +114 / -0 | Byte copy of block.md |
| `.agent/authored/f269-r1-context.md` | +41 / -0 | Byte copy of context.md |
| `.agent/authored/f269-r1-decisions.md` | +49 / -0 | Byte copy of decisions.md |
| `.agent/authored/f269-r1-ledger.md` | +2 / -0 | Byte copy of ledger.md |
| `.agent/authored/f269-r1-live_review_head.md` | +24 / -0 | Byte copy of live_review_head.md |
| `.agent/authored/f269-r1-plan.md` | +30 / -0 | Byte copy of plan.md |
| `.agent/authored/f269-r1-status_from.txt` | +1 / -0 | Byte copy of status_from.txt |
| `.agent/authored/f269-r1-status_to.txt` | +1 / -0 | Byte copy of status_to.txt |
| `.agent/context.md` | +25 / -27 | := context.md |
| `.agent/decisions.md` | +49 / -0 | `0955dd4c` bytes + decisions.md (D2, D3) |
| `.agent/live_review.md` | +19 / -19 | head + `0955dd4c` bytes from `## Findings` + ledger.md (Gate F268 R13 PASS) |
| `.agent/plan.md` | +20 / -13 | := plan.md |
| `docs/roadmap/STATUS.md` | +1 / -1 | F269 line `[ ]` → `[~]` (status_from → status_to) |

### 27f3d073 F269 R1 C2a: the contract record — mission_contract module per DECISIONs F269 D2 and D3
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/mission_contract.py` | +306 / -0 | New module. It holds `ContractCriterion` and `MissionContract` (frozen, `to_json`/`from_json`), `ContractError(ValueError)` with `.rule`, `write_mission_contract`, `read_mission_contract`, `job_contract_slice`, `read_job_milestone`, `record_job_milestone` and `render_contract_lines`. |
| `packages/orchestration/mission_state.py` | +12 / -12 | Two docstrings only, `Mission`'s `contract` paragraph and `set_mission_contract`, now name the new module as the shape's owner |

### 8f62302b F269 R1 C2b: tests for the contract record, the D2 refusals, the job slice and the milestone recorder
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_mission_contract.py` | +234 / -0 | Covers the round trip. The 20-row D2 refusal table is parametrized on write AND on read of a raw-stored body. Also covers the slice M1 → [C001, C002] and no milestone → [C001], the recorder writing, and False for an unknown job with nothing written. |

### e38d21f9 F269 R1 C3: the dispatch branch records the milestone a job serves on the job record
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/orchestrator_loop.py` | +12 / -0 | Adds `record_job_milestone(job_id, payload["milestone_id"], root)` beside `attach_milestone_dod`. On True, the same key is also set on the in-memory job the executor is handed. |
| `tests/orchestration/test_orchestrator_loop.py` | +27 / -0 | `test_a_dispatched_job_records_its_milestone_on_disk` runs the REAL `continue_mission` dispatch and checks two things: `metadata["milestone_id"] == "M001"` on disk, and on the job passed to `execute` |

### cc206f50 F269 R1 C4: mission contract and job contract, read-only with --json, and the regenerated reachability allowlist
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/command_catalog.py` | +24 / -0 | `job.contract` (job id, `--json`) and `mission.contract` (mission id, `--project`, `--json`). Both are `read_only` with `supports_json=True`. `related=` names only live ids. |
| `apps/cli/commands/__init__.py` | +2 / -1 | Registers `contract_cmd` |
| `apps/cli/commands/contract_cmd.py` | +130 / -0 | The two handlers. Exit codes and JSON follow D3 (3), and one renderer serves both. |
| `tests/cli/test_contract_cmd.py` | +221 / -0 | Runs subprocesses through the `test_mission_cmd.py` helpers. The mission view renders 3 criteria and the M1 job view renders 2. The job's `--json` criteria equal the mission's. No contract, and a job in no mission, each print the sentence with exit 0 and `null`. An unknown mission or job exits 1, and a broken body exits 1 naming the rule. |
| `tests/orchestration/import_reachability_allowlist.txt` | +4 / -3 | Regenerated from `reachable_closure()`, keeping the 5 header lines |

### C5 (this commit) F269 R1 C5: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | This file |

## External actions

- `git worktree add --detach .remedy-wt/f269-r1-g4 cc206f50` for G4. It was removed with `git worktree remove .remedy-wt/f269-r1-g4`, and `git worktree list` afterwards showed only the primary checkout.
- `git push -u origin feature/f269-contract` runs after this commit. Its outcome and G5 are in the worker's final report, because this file cannot record a push that follows it.
- No PR was created or merged. `gh pr list --state open` read `[]` before the branch was cut.

## Verification

All gates ran at C4 `cc206f50`, before this commit.

G1, transport and state:
- `sha256sum` of all 8 payloads matched the block's digests. The block itself is `a832ca8da2a594723253ebcaed08d48b6739961e73d3c8f2088c05c11332d989`.
- `cmp .agent/plan.md .remedy-wt/f269-r1/plan.md` exited 0 with no output.
- `cmp .agent/context.md .remedy-wt/f269-r1/context.md` exited 0 with no output.
- `python3 .remedy-wt/f269-r1/g1.py` printed:
```
plan.md: payload True, authored copy True
context.md: payload True, authored copy True
live_review_head.md: payload True, authored copy True
ledger.md: payload True, authored copy True
decisions.md: payload True, authored copy True
status_from.txt: payload True, authored copy True
status_to.txt: payload True, authored copy True
block.md: payload True, authored copy True
live_review.md == head + 0955dd4c from '## Findings' + ledger.md: True
decisions.md == 0955dd4c bytes + decisions.md: True
STATUS FROM count 0 TO count 1
```
The C1 script's own STATUS reading was `TO contains FROM: False` / `FROM before 1 after 0 TO after 1`.

G2: the block's 17 paths, run serially with `python3 -m pytest -q -p no:cacheprovider …`, read `1381 passed in 152.42s (0:02:32)` with exit 0.

G3: `python3 -m ruff check` over the 9 .py files C2 to C4 touched read `All checks passed!`.

G4: `python3 .remedy-wt/f269-r1/g4.py` ran in one worktree at `cc206f50`. It uses `python3 -B -m pytest` from the worktree root, purges `__pycache__` before each run and sets `PYTHONDONTWRITEBYTECODE=1`.
```
mission_contract resolves to: /home/decodeux/Repos/remedy/.remedy-wt/f269-r1-g4/packages/orchestration/mission_contract.py
--- control (unmutated): exit=0   260 passed
--- (a) job slice returns every criterion: exit=1   4 failed, 256 passed
    tests/cli/test_contract_cmd.py::TestTheJobView::test_a_job_for_m1_renders_the_whole_mission_and_m1_criteria
    tests/cli/test_contract_cmd.py::TestTheJobView::test_every_job_criterion_equals_the_mission_criterion_of_its_id
    tests/orchestration/test_mission_contract.py::TestTheJobSlice::test_a_job_of_m1_gets_the_whole_mission_and_m1_criteria_in_order
    tests/orchestration/test_mission_contract.py::TestTheJobSlice::test_a_job_with_no_milestone_gets_the_whole_mission_criteria_only
--- (b) origin rule not checked: exit=1   3 failed, 257 passed
    tests/cli/test_contract_cmd.py::TestTheMissionView::test_a_body_breaking_a_rule_exits_1_naming_it
    tests/orchestration/test_mission_contract.py::TestTheContractRecord::test_a_broken_body_is_refused_on_write[13-origin is template, planner or amendment]
    tests/orchestration/test_mission_contract.py::TestTheContractRecord::test_a_broken_body_stored_raw_is_refused_on_read[13-origin is template, planner or amendment]
--- (c) C3's call removed: exit=1   1 failed, 259 passed
    tests/orchestration/test_orchestrator_loop.py::TestEveryMoveKindIsExercised::test_a_dispatched_job_records_its_milestone_on_disk
```
The script's FAILED regex stops at the first space, so it printed the two parametrized ids in (b) cut at `[13-origin`. The full ids are shown above. The worktree was clean (`git status --porcelain` empty) after every revert, then removed.

The full suite was not run (amend0917-throughput).

## Authored-text proofs

- All 8 payloads are committed byte-identical as `.agent/authored/f269-r1-*`, and G1 printed `authored copy True` for each.
- `.agent/plan.md` and `.agent/context.md` pass `cmp` against their payloads with exit 0.
- `.agent/live_review.md` and `.agent/decisions.md` equal their construction from the `0955dd4c` bytes (G1 True).
- STATUS: FROM 1x before and 0x after; TO 1x after.

## Deviations & assumptions

1. C2 is two commits, C2a (code, 318 insertions) and C2b (tests, 234). As one commit it would be 552 insertions, and constraint 1 orders the split.
2. C3's test is a new test and does not extend an existing one. The block said to extend the nearest dispatch test that creates a real job record, but no such test exists: every dispatch test in `test_orchestrator_loop.py` uses the `dispatched` fixture's `_FakeJob`. So I added a new test beside `test_dispatch_job_goes_through_the_dispatch_verb`. It uses the real `continue_mission`, with `REMEDY_DATA_DIR` set to `tmp_path` and `root=tmp_path`.
3. C3 also puts the milestone key on the in-memory job. `execute_dispatched_job` hands that same object to `run_cycles`, which saves it again, and without the key that save would drop the milestone from disk. The key is set only when `record_job_milestone` returned True, and the test asserts it.
4. `record_job_milestone` gets the loop's `root`. That is the same data root `missions_dir`/`jobs_dir` hang off, and it is None in production. This keeps the fake-dispatch tests from looking under the real data root.
5. Regenerating the allowlist removed `packages.orchestration.redaction_patterns`. The module still exists but is not in `reachable_closure()` at this tip, and this round only adds imports, so it was already unreachable at base. The regeneration also moved two entries that were out of sorted order at base, `packages.orchestration.job_plan` and `packages.orchestration.study`, into their sorted places.
6. Readings of D2 where the text leaves the encoding open:
   - `milestones` is checked as a list of distinct non-empty strings, NOT against the mission plan's milestone ids.
   - Unknown fields are refused, under the rule `fields are known`.
   - Required fields are `schema` and `criteria` at the top level, and `id`, `text` and `origin` per criterion.
   - The other fields take D2's defaults (blocking true, status open) or empty/null (milestones [], check null, evidence_ref null, template null, amendments []). `to_json` always writes all keys.
7. The first wording of the `mission.contract` description said "in order". That tripped `test_every_binding_word_in_a_description_carries_the_pages_meaning` with the binding word "Order", so it was reworded before C4 was committed.
8. The docstring of `tests/orchestration/test_mission_state.py::…::test_the_contract_round_trips_through_disk` still reads "RESERVED for F269 … empty until then". It is outside this round's change set and was left unedited. The test is storage-level and still passes.

| Item | Status | Reason |
|------|--------|--------|
| C1 claim | done | |
| C2 the record | deviated | split into C2a/C2b per constraint 1 |
| C3 dispatch | deviated | new test instead of extending one (none creates a real job record); in-memory key sync |
| C4 commands | done | |
| C5 handoff + push | done | push follows this commit |

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Then the review of round 1 (T001), with its verdict booked in round 2's first commit.

Operator questions open: 3
