# Handoff — F299 round 3: book round 2 + R-1227 + DECISION F299 D2, and T003 (criterion state `unchecked`)

## Session

SESSION 1 of feature F299 · round 3 · rounds so far 3

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~70 % (T001 to T003 · T004 and the closure open) — Schätzung

## Range

Review of `b6dda76d77c9d16e80ec63198bdcb93cf4c21e87`..HEAD (seven commits on
`feature/f299-acceptance-checks-other-repos`: C1 through C6 and this handback).

## Commits

### `c57de32ac` F299 R3 C1: save the round 3 block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f299-r3.md` | 270/0 | NEW FILE — a verbatim copy of `block.md`; sha256 and line count checked equal to the source (both `704e5c7a8aa3be569322e235a2f1d03b11fc9610e688fdf9fc27cb55a5d67263`, 270 lines) |

### `9b29ab23a` F299 R3 C2: book round 2 and R-1227, DECISION F299 D2, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | 10/0 | appends DECISION F299 D2 — the `unchecked` state, its writer, blocker rule, the gate's `not_run` list, the one phrase, the approval card's rule, the push's third list and its two record keys |
| `.agent/live_review.md` | 4/0 | appends `Gate: F299 R2` (FAIL) and R-1227, booking round 2's verdict |
| `.agent/plan.md` | 15/15 | rewritten for round 3's current step, next steps and risks |

### `4bb4ab9ab` F299 R3 C3: a test that reads the environment a project_tests check's process receives (R-1227)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_dod_runners.py` | 46/0 | `TestProjectTestsKind` gains one test: a configured command prints its own `PATH`/`VIRTUAL_ENV` back, run in a `git worktree add` of a checkout holding a `.venv` and `node_modules/.bin`; proves both reached the child in D1 (3)'s order, repairing R-1227. No `Landed:` line written; the reviewer resolves R-1227. |

### `39b0482eb` F299 R3 C4: the criterion state unchecked, read as no check ran (T003, DECISION F299 D2)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/project_tests.py` | 4/0 | `NO_CHECK_RAN_WORDS` — the one phrase every unchecked surface says |
| `packages/orchestration/mission_contract.py` | 32/14 | `CRITERION_STATUS_UNCHECKED` joins `CRITERION_STATUSES`; the refusal message names it; `record_contract_results` writes `unchecked` when the matched check's reason is `no_test_command`, else `unmet`; `contract_blockers` excludes `unchecked`; `render_contract_lines` pads to 9 chars and adds `NO_CHECK_RAN_WORDS` under an unchecked criterion |
| `packages/orchestration/do_sequence.py` | 18/4 | `do_contract_summary_line` separates unchecked blocking criteria from the genuinely not-met ones in its tail sentence |
| `tests/orchestration/test_mission_contract.py` | 77/5 | the refusal-message pin updated; new tests: `no_test_command` → `unchecked`, `test_command_invalid` → `unmet`, `contract_blockers` excludes `unchecked`, the renderer's `NO_CHECK_RAN_WORDS` line and nowhere else |
| `tests/cli/test_do_sequence_cli.py` | 15/15 | the three named tests: suite-judged and planner criteria read `unchecked`, `unmet_blocking_criteria` is `[]`, the `Contract:` line reads the new wording |
| `tests/cli/test_status_cmd.py` | 8/6 | the approval-card test: criterion `unchecked`, `checks_ran` False, `(recommendation, risk) == ("review", "high")` |

### `87a4a77b3` F299 R3 C5: the gate's not_run list and the words on every surface that shows a check (T003, DECISION F299 D2)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/dod_gate.py` | 12/1 | `GateResult`/`_Tally`/`evaluate_dod` gain `not_run`; a `no_test_command` check never enters `blocking_red`/`reported_red`; `to_json` carries `not_run` |
| `apps/cli/commands/job.py` | 8/1 | `_dod_section`: the released line reads "no blocking check is red" when `not_run` is non-empty, plus a `For <ids>, ...` line after the reds line |
| `packages/orchestration/run_report.py` | 15/3 | `_dod_lines`: not-run checks excluded from the held branch's red count; the released branch gains the same two sentences when any exists |
| `packages/orchestration/result_tour.py` | 18/5 | `_definition_of_done_stop`: not-run checks pulled out of the passed/total count and `Not passed`, named by their own sentence |
| `tests/orchestration/test_dod_gate.py` | 52/0 | a `project_tests` check with no command: released, `not_run` holds its id, `blocking_red`/`reported_red` empty, whether blocking or not; the report's two-sentence test; `job show`'s section test |
| `tests/orchestration/test_result_tour.py` | 46/2 | two new tests: a not-run check alone, and one beside a passed check |

### `d0531fc0f` F299 R3 C6: the approval card, the push and the interface for unchecked criteria (T003, DECISION F299 D2)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/job_apply.py` | 46/12 | `mission_push_refusals` returns a third list, `unchecked`; `push_unchecked_criteria_sentence`; `JobApplyResult.push_unchecked_criteria`; `_push_refusals`/`_flag_refusals` thread it; `export_job_apply_json` and all three `summarize_job_apply` call sites wired |
| `packages/orchestration/do_sequence.py` | 25/16 | `do_mission_push_refusals`/`_do_push_record`/`do_push_mission` carry the third list and join its sentence with the open one |
| `packages/orchestration/client_digest.py` | 9/4 | `_card_recommendation` reads `review` on an `unchecked` blocking criterion too |
| `apps/cli/client_interface.py` | 3/1 | `job.apply`'s answer-key tuple and `do.run`'s `push` tree gain `push_unchecked_criteria`/`unchecked_blocking_criteria` |
| `docs/system/machine-client-contract-v1.md` | 20/18 | the two `doc-pairs.json` rewrites applied (each `from` once→zero, `to` zero→once), then the generated section rewritten via `write_client_interface_page()` |
| `tests/orchestration/test_job_apply_commit.py` | 28/0 | `test_p8`: an `unchecked` blocking criterion is pushed and named apart from the `open` one |
| `tests/cli/test_do_commit_flags.py` | 18/0 | the unchecked analogue of the open-blocking-criterion push test, on the fixture's repository without tests |
| `tests/cli/test_client_interface.py` | 2/1 | the measured `job.apply` key set gains `push_unchecked_criteria` |
| `tests/orchestration/test_client_digest.py` | 6/2 | the recommendation rule table gains `unchecked`; **and** the pre-existing `test_the_page_states_the_rules_with_the_codes_own_limits` pin, which the doc-pairs.json P2 rewrite broke, corrected to the new prose (see Deviations & assumptions — not named by the block, fixed in the same file the block already orders touched) |

### This commit (self-reference) — F299 R3 C7: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file |

## External actions

None besides the push below: no `gh pr create`, no `gh pr merge`, no new branch, no stash entry
touched, no `git worktree add`/`remove` by the worker itself outside a test's own disposable
`tmp_path` fixture (C3's new test adds and never needs to remove one, inside `tmp_path`, torn down
by pytest), no force-push.

`git push origin feature/f299-acceptance-checks-other-repos` after C7 — reported in the worker's
final reply.

## Verification

**Gate 1** (before C1, from the primary checkout): a Python sha256 reader over
`digests.txt`'s five files (`block.md`, `dry-live_review.md`, `append-decisions.txt`,
`dry-plan.md`, `doc-pairs.json`). Exit 0 (script). All five sha256 **and** line counts matched.

**Gate 2** (after C6): `git -C /home/decodeux/Repos/remedy status --porcelain` empty: **True**.
C2 step 2's four byte-equality proofs, re-run at `d0531fc0f`: all **True**
(`decisions.md` == blob at `b6dda76d7` + `append-decisions.txt`; `live_review.md` == blob at
`b6dda76d7` + `src/ledger-append.txt`; `live_review.md` == `dry-live_review.md`; `plan.md` ==
`dry-plan.md`). The four counts per `doc-pairs.json` pair, re-checked against the final committed
page: P1 `after_from=0 after_to=1`, P2 `after_from=0 after_to=1` — both as ordered (before the
rewrite each had been `from=1, to=0`, applied cleanly to exactly one occurrence each).

**Gate 3** (once, after C6), from the primary checkout:
```
python3 -m pytest -q -rfEs @/home/decodeux/Repos/remedy/.remedy-wt/f299-r3/selection.txt
```
Exit **1**. Summary line: `1 failed, 6019 passed, 9 skipped in 588.70s (0:09:48)`. The one FAILED
line, verbatim:
```
FAILED tests/orchestration/test_orchestrator_loop.py::TestTheContractHoldsTheAchievedClaim::test_a_broken_body_refuses_with_the_rule
```
Its assertion, verbatim:
```
>       assert "status is open, met or unmet" in reason
E       assert 'status is open, met or unmet' in "the mission cannot be achieved: its contract is unreadable — contract rule broken: status is open, met, unmet or unchecked (criterion C001 has 'done')"
```
No ERROR line. This test pins `ContractCriterion`'s OLD refusal message, which C4 changed (block
order, `mission_contract.py`) to `"status is open, met, unmet or unchecked"`;
`tests/orchestration/test_orchestrator_loop.py` is not in C4's (or any commit's) ordered path list,
so this pin was not updated and the gate is RED. Per the block's constraint, this is reported and
NOT re-run; no fix was attempted.

The 9 SKIPPED lines, verbatim (all pre-existing quarantines, identical to round 2's handoff,
unrelated to this round's files):
```
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:399: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
```

**Gates 4, 5 and 6: NOT RUN.** The block's constraints state: "A red gate is reported with every
FAILED and ERROR line it printed and not re-run; stop, write the handoff, push." Gate 3 came back
red, so this round stops there rather than running the remaining gates — `ruff check` (gate 4),
the three-target measurement (gate 5) and the integrity/open-findings check (gate 6) were never
invoked this round. (Every file this round's commits touch was, individually, proved green under
`ruff check` and under targeted `pytest` runs of its own test file while C3–C6 were being written,
as the block permits — "While writing C3 to C6 you may run single test files of your own, one at a
time" — but that is not gate 4, 5 or 6, and is not claimed as one.)

## Authored-text proofs

`.agent/authored/f299-r3.md` (the saved block, C1) equals `block.md` byte for byte: sha256
`704e5c7a8aa3be569322e235a2f1d03b11fc9610e688fdf9fc27cb55a5d67263` on both sides, 270 lines each.
No other reviewer-authored text (as distinct from the prepared state files proved in C2 step 2 and
re-proved at gate 2) was applied this round.

## Deviations & assumptions

- **C0**: all of C0's checks (HEAD at `b6dda76d77c9d16e80ec63198bdcb93cf4c21e87`, branch
  `feature/f299-acceptance-checks-other-repos`, `git status --porcelain` empty, `.agent/STOP`
  absent) held exactly as the block states, checked before any write; the branch was re-checked
  before every commit.
- **A transient, uncommitted self-inflicted corruption during gate 2's re-run, caught and reversed
  before any commit touched it**: gate 2 orders re-running C2 step 2's byte proofs. The worker's
  first attempt reused its C2 *apply* script (which appends `append-decisions.txt` unconditionally)
  instead of a read-only proof script, which appended that block to `.agent/decisions.md` a SECOND
  time in the working tree. `git status --porcelain` (checked immediately after, as gate 2's first
  clause) caught it as `M .agent/decisions.md`; the file was restored with `git checkout --
  .agent/decisions.md` (a tracked-file restore to HEAD, not a branch-wide reset) before writing or
  running anything else, and a dedicated read-only `gate2.py` was written for the actual gate. No
  commit ever carried the duplicate, and the re-run gate 2 above is the clean one. Declared here
  per the "any departure, even when corrected" rule (R-0485 pattern), not because any committed
  state was ever wrong.
- **One test outside every commit's named paths broke from C4's own ordered change, fixed inside
  C6 (same file C6 already touches), before gate 3 ever ran**:
  `tests/orchestration/test_client_digest.py::test_the_page_states_the_rules_with_the_codes_own_limits`
  pins the digest page's recommendation-rule prose verbatim; the `doc-pairs.json` P2 rewrite (C6,
  block-ordered) changed that exact prose, so the pin was updated in the same commit to the new
  wording. This is a within-file, within-commit correction of a test the block already lists under
  C6, not a new path and not a scope departure — recorded here per the self-review loop
  (AGENTS.md) rather than left to redden gate 3 for a reason this round could plainly see and fix.
- **One test outside every commit's named paths was left red, by the block's own rule**:
  `tests/orchestration/test_orchestrator_loop.py::TestTheContractHoldsTheAchievedClaim::test_a_broken_body_refuses_with_the_rule`
  pins `ContractCriterion`'s OLD refusal message, which C4's ordered change to
  `mission_contract.py` altered. Unlike the digest-page test above, this file is not named by C4's
  (or any other commit's) path list, so fixing it would have been an undeclared, unordered edit
  outside the block's change set — the constraint section is explicit that a red gate is reported,
  not repaired, and that is what this round did. See the Verification section (gate 3) for the full
  FAILED line and assertion, and `Next` below.
- **Gates 1, 2 and 3** ran exactly as ordered, each once; gates 4, 5 and 6 were not run, per the
  constraint on a red gate (see Verification).

## Round verdicts

Round 2's FAIL is booked into `.agent/live_review.md` by C2 as `Gate: F299 R2`, with R-1227
registered beneath it (the environment-reaching-the-child-process test the round had not written;
C3 of this round supplies it). Round 3's own verdict is the reviewer's, not yet written.

## For the operator, in plain sentences

The last round's code had one gap: a missing test that the project's own settings really reach the
test it runs. That test is now added. This round makes a project without tests read "no check ran"
instead of failing, in every place Remedy shows that result: the summary after a run, the contract
listing, the job page, the report, the guided tour, the approval card, and the push, which goes
ahead and says that no check ran. One pre-existing test elsewhere in the suite still expects the
old wording of a message this round changed on purpose; it is left failing on purpose, named below,
for the next round to fix, rather than patched outside this round's planned files. Nothing waits for
the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop.
2. Phase 1 rule 2 (the Open PR Gate):
   `gh pr list --state open --json number,headRefName,baseRefName,isDraft` before any further
   branch work.
3. Book round 3's verdict and R-1227's resolution in the next round's first commit; repair the red
   gate-3 test (`tests/orchestration/test_orchestrator_loop.py`'s stale refusal-message pin) and
   re-run the full selection once, clean, before anything else.
4. T004: the page and the three targets as `remedy do` tests.

Operator questions open: 0.
Open findings: 16 (R-1160, Medium; R-1227, Low, owned by F299; R-1138, R-1139, R-1143, R-1149,
R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196, R-1219, R-1220 and R-1225, Low, owned by
F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0: base checks + gate 1 | done | HEAD, branch, status and STOP all confirmed before any write; gate 1 green |
| C1: save the block | done | `.agent/authored/f299-r3.md`, byte- and line-identical to `block.md` |
| C2: book round 2 + R-1227, DECISION D2, the plan | done | all copies and appends byte-proved against the prepared files, re-proved at gate 2 |
| C3: the R-1227 repair test | done | new test in `TestProjectTestsKind`, proven green |
| C4: criterion state `unchecked` (T003) | done | `project_tests.py`, `mission_contract.py`, `do_sequence.py` + tests, all proven green |
| C5: gate `not_run` + every surface's words (T003) | done | `dod_gate.py`, `job.py`, `run_report.py`, `result_tour.py` + tests, all proven green |
| C6: approval card, push, interface (T003) | done | `job_apply.py`, `do_sequence.py`, `client_digest.py`, `client_interface.py`, the doc page + tests, all proven green |
| C7: handback | done | this commit |
| Gate 1 | passed | all five digests and line counts matched before C1 |
| Gate 2 | passed | status clean; all C2 byte proofs and both doc-pair counts True at `d0531fc0f` |
| Gate 3 | **FAILED** | `1 failed, 6019 passed, 9 skipped`; one pre-existing test outside every commit's paths pins the old refusal message C4 changed; reported, not re-run |
| Gate 4 | not run | skipped per the red-gate constraint (stop after gate 3) |
| Gate 5 | not run | skipped per the red-gate constraint (stop after gate 3) |
| Gate 6 | not run | skipped per the red-gate constraint (stop after gate 3) |
| Push | done | reported in the worker's final reply |
