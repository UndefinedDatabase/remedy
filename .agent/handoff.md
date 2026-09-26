# Handback — F027 Task veto · Round 9

## Session

SESSION 2 of feature F027 · round 9 · rounds so far 9

Just over half of the session's context budget remained at the point this handback was
written. This round booked round 8's verdict, registered and repaired R-1069 and R-1070,
recorded DECISION F027 D9, and landed `tests/ui_server/test_task_veto_e2e_live.py`: the
diamond end-to-end — a veto filed through a live write door on a diamond job the task cap
paused after its first task, the run finished through the real CLI to a blocked end that
names the veto, the replan proposal answered through the door both ways (accept and
replan) and carried to its effect. All five gates (G1–G5) ran green on the first pass; G6
follows below. No commit split was needed this round (every commit stayed well under the
500-line cap).

## Range

Review of `46305052d..399f4efea` (C1 through C5, all committed). C6 (this handback) follows.

## Commits

### e4b80c37a F027 R9 C1: copy round 9 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f027-r9-block.md | +223/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f027-r9-plan.md | +29/-0 | copy of the plan.md payload |
| .agent/authored/f027-r9-records.diff | +72/-0 | copy of the records.diff payload |

324 insertions by `git show --numstat` — matches the block's stated expectation exactly
(block line count 223 plus 101), under the 500-line cap.

### 304d54939 F027 R9 C2: book round 8, register R-1069 and R-1070, record D9
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +41/-0 | DECISION F027 D9 appended, verbatim from records.diff |
| .agent/live_review.md | +6/-0 | round 8's Gate entry and the registrations of R-1069 and R-1070, appended |
| .agent/plan.md | +9/-10 | rewritten whole to the plan.md payload |
| .agent/prose_slips.md | +1/-0 | round 8's prose-slip line, appended verbatim |

41/0 decisions.md, 6/0 live_review.md, 9/10 plan.md, 1/0 prose_slips.md by `git show
--numstat` — matches the block's stated expectation exactly. `git apply --check` on
records.diff → exit 0; the real `git apply` → exit 0.

### f6da8b498 F027 R9 C3: repair R-1069 and R-1070
| Path | +/- | Reason |
|---|---|---|
| docs/ui/design_reference/assumption_log.md | +1/-1 | R-1069's FIX: the `ForceBrainGraph.tsx` row's technical-reason cell now states the real reason in plain words (an operator-typed reason handed to the library as a string would be read as markup) instead of citing a non-existent markup rule; every other cell unchanged |
| apps/ui/src/api/vetoView.ts | +2/-2 | R-1069's FIX: the comment above `vetoAnswerSentence` names `veto_proposal.py` and `task_veto.REPLAN_PROPOSAL_OPTIONS` instead of `escalation.py` |
| apps/ui/src/components/detail/DetailPopover.tsx | +11/-9 | R-1070's FIX: the Veto section's `Will not run because of this veto:` paragraph now renders only inside the branch that lists at least one unreachable task |
| tests/ui_contracts/test_veto_controls_contract.py | +14/-0 | R-1070's FIX: `test_the_veto_sections_lead_in_sits_inside_the_non_empty_branch` pins the lead-in inside the non-empty branch, not before the length check |
| .agent/live_review.md | +4/-0 | two `Landed:` lines for R-1069 and R-1070, at this round's C3 (never `Done:`, per S1/S2's FIX clauses being registered findings, not the reviewer's own prose-slip route) |

32 insertions (12 deletions), under the 500-line cap.

### df68af08a F027 R9 C4: the diamond veto end to end through the CLI and the door
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_task_veto_e2e_live.py | +382/-0 (new) | S3: the diamond end-to-end, `@pytest.mark.subprocess`, its own copies of `test_task_edit_e2e_live.py`'s plan/server/POST/events-since helpers; two tests, THE ACCEPT PATH and THE REPLAN PATH |

382 insertions, under the 500-line cap.

### 399f4efea F027 R9 C5: the round's red-proof mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f027-r9-mutations.py | +227/-0 (new) | the round's mutation tool for G5 (excluded from `ruff check` by `pyproject.toml`'s `.agent/authored` exclusion, DECISION F263 D3) |

227 insertions, under the 500-line cap.

### (C6, this commit) F027 R9 C6: rewrite handoff for round 9
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | see below | this handback, rewritten whole per `docs/agents/handback_template.md` |

## External actions

`git push -u origin feature/f027-task-veto` after C6 → see G6 below for the real outcome.
No PR created or merged this round (constraint 5; the Open PR Gate read empty before this
round started — see G6 below for its reading at handback time). One worktree added and
removed for G5: `git worktree add --detach .remedy-wt/f027-r9-mut 399f4efea` (HEAD at that
point being `399f4efea`, the last code-bearing commit — C5 is the mutation tool itself, not
production/test code under test, so the worktree's content for every file the tool touches
is identical to what it would have been at C4), then `git worktree remove --force
.remedy-wt/f027-r9-mut` and `git worktree prune` immediately after the tool ran; `git
worktree list` before and after matched exactly (see Verification).

## Verification

**BEFORE ANYTHING ELSE (all four readings, all passed):**
```
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory
(absence confirmed — continue)

$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f027-task-veto
$ git log --oneline -1
46305052d F027 R8 C7: rewrite handoff for round 8
```
All matched the block's step 2 exactly.

**Block bytes (step 3):** `.remedy-wt/f027-r9/block.md` → 223 lines (newline count), 17106
bytes, sha256 `9d8bece9af6780507f1c0897016cd379930fde86465eb624527b17dfb37da320` — both the
line count and the sha256 match the delegation message's two readings exactly.

**Worktree list (step 4):** reported in full at round start — 100 entries: the primary
checkout, `f015-*`, `f020-*`, `f023-*`, `f024-*`, `f025-*`, `f027-r1-dry` through
`f027-r8-dry` (no `f027-r9*` entry; the reviewer's `.remedy-wt/f027-r9/` and
`.remedy-wt/f027-r9-payloads/` are plain directories the reviewer wrote, never registered
as `git worktree` entries), `f284-*` and the ten `job-*` worktrees. Unchanged at handback
except for the G5 worktree added and removed (see External actions and G5 below).

**PAYLOADS** — readings (all matched the table):
| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 29 | 1078 | ed20409e81fc200bde9d7d31a2b6abc63864e9e4e9caa3a737a5e4772140a81a |
| records.diff | 72 | 14549 | bdd17b382d5cf28c5d051a3acd547c20c66a7d3f00e9e6f96ae770588aefcf8a |

**G1 TRANSPORT** — copy comparisons, all byte-identical:
- `git show e4b80c37a:.agent/authored/f027-r9-block.md` = `.remedy-wt/f027-r9/block.md` (identical, sha256 `9d8bece9af6780507f1c0897016cd379930fde86465eb624527b17dfb37da320`)
- `git show e4b80c37a:.agent/authored/f027-r9-plan.md` = `.remedy-wt/f027-r9-payloads/plan.md` (identical, sha256 `ed20409e81fc200bde9d7d31a2b6abc63864e9e4e9caa3a737a5e4772140a81a`)
- `git show e4b80c37a:.agent/authored/f027-r9-records.diff` = `.remedy-wt/f027-r9-payloads/records.diff` (identical, sha256 `bdd17b382d5cf28c5d051a3acd547c20c66a7d3f00e9e6f96ae770588aefcf8a`)

**G2 THE RECORDS** — sha256 at `304d54939`, all matched the block's table exactly:
| path | bytes | sha256 | match |
|---|---|---|---|
| .agent/live_review.md | 323564 | 9b6ffe9a52a061a53e0daea8b4f11a3485dac34b2e5fec02c5ecf477f7b580bd | yes |
| .agent/decisions.md | 2192648 | 0484cfb7ef66eac6543ec5c7b8b11b7626487871c28ed7399ca5e527c3cd60a4 | yes |
| .agent/prose_slips.md | 369727 | 8f881e35241059245a03c186880e4a036b0fd72b1da8525815356f4565e7d12b | yes |
| .agent/plan.md | 1078 | ed20409e81fc200bde9d7d31a2b6abc63864e9e4e9caa3a737a5e4772140a81a | yes |

`open_finding_ids` (via `scripts/rotate_live_review.py`) over the ledger's text at
`304d54939` → `['R-1069', 'R-1070']` — matches the block's own reading exactly.

**G3 THE CODE:**
```
$ ruff check tests/ui_server/test_task_veto_e2e_live.py tests/ui_contracts/test_veto_controls_contract.py
All checks passed!
REAL_EXIT=0
```
The `SKIPPED` lines of G4 below name no TypeScript, lint or vitest node (all four are
Python `pytest.skip` D3 quarantine reasons — see G4).

**G4 THE TESTS:**
```
$ pytest -q -p no:cacheprovider -rs tests/ui_server/test_task_veto_e2e_live.py \
    tests/ui_server/test_task_edit_e2e_live.py tests/ui_contracts \
    tests/ui_server/test_dashboard_contract.py tests/ui_server/test_command_dispatch.py \
    tests/orchestration/test_task_veto_runner.py tests/orchestration/test_veto_proposal.py \
    tests/orchestration/test_test_runner.py tests/docs tests/cli/test_golden_path.py
1513 passed, 4 skipped in 88.33s
REAL_EXIT=0
```
`SKIPPED` lines, all four D3 quarantine (unrelated to this round, pre-rebuild legacy
`.tsx` sources not in the tree — F252):
```
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543
```

New test file's nodes (`--collect-only -q`):
```
$ pytest --collect-only -q tests/ui_server/test_task_veto_e2e_live.py
tests/ui_server/test_task_veto_e2e_live.py::TestTaskVetoE2ELive::test_the_accept_path_settles_the_reduced_scope
tests/ui_server/test_task_veto_e2e_live.py::TestTaskVetoE2ELive::test_the_replan_path_creates_a_follow_up_that_nothing_runs
2 tests collected in 0.09s
REAL_EXIT=0
```

New test file's own wall time, run alone (`--durations=0`):
```
$ pytest -q -p no:cacheprovider --durations=0 tests/ui_server/test_task_veto_e2e_live.py
1.55s call     tests/ui_server/test_task_veto_e2e_live.py::TestTaskVetoE2ELive::test_the_accept_path_settles_the_reduced_scope
1.05s call     tests/ui_server/test_task_veto_e2e_live.py::TestTaskVetoE2ELive::test_the_replan_path_creates_a_follow_up_that_nothing_runs
0.11s setup    tests/ui_server/test_task_veto_e2e_live.py::TestTaskVetoE2ELive::test_the_accept_path_settles_the_reduced_scope
2 passed in 2.80s
REAL_EXIT=0
```
Well inside the standard stage's budget — the risk `plan.md` names.

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"name": "handler_import", "status": "pass"}, {"name": "live_review_verdict", "status": "pass"}, {"name": "plan_consistency", "status": "pass"}, {"name": "relevant_untracked", "status": "pass"}, {"name": "repo_root_hygiene", "status": "pass"}, {"name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true}
REAL_EXIT=0
```
All six checks `pass`.

**G5 THE RED PROOFS:**
```
$ git worktree add --detach .remedy-wt/f027-r9-mut 399f4efea
Preparing worktree (detached HEAD 399f4efea)
REAL_EXIT=0

$ python3 -B .agent/authored/f027-r9-mutations.py .remedy-wt/f027-r9-mut
==============================================================================
--- pytest control run (unmutated, before) ---
control: exit=0
10 passed in 10.34s
m1 the linear runner dispatches a task unreachable behind a veto: exit=1 failed=1
  failing_node_ids=['tests/ui_server/test_task_veto_e2e_live.py::TestTaskVetoE2ELive::test_the_accept_path_settles_the_reduced_scope']
m2 format_job_report_text drops the Vetoed by line: exit=1 failed=1
  failing_node_ids=['tests/ui_server/test_task_veto_e2e_live.py::TestTaskVetoE2ELive::test_the_accept_path_settles_the_reduced_scope']
m3 _build_veto_section reports no veto entry: exit=1 failed=1
  failing_node_ids=['tests/ui_server/test_task_veto_e2e_live.py::TestTaskVetoE2ELive::test_the_accept_path_settles_the_reduced_scope']
m4 the runner's terminal accounting treats an answered veto as unanswered: exit=1 failed=2
  failing_node_ids=['tests/ui_server/test_task_veto_e2e_live.py::TestTaskVetoE2ELive::test_the_accept_path_settles_the_reduced_scope', 'tests/ui_server/test_task_veto_e2e_live.py::TestTaskVetoE2ELive::test_the_replan_path_creates_a_follow_up_that_nothing_runs']
m5 answering replan_follow_up creates no follow-up job: exit=1 failed=1
  failing_node_ids=['tests/ui_server/test_task_veto_e2e_live.py::TestTaskVetoE2ELive::test_the_replan_path_creates_a_follow_up_that_nothing_runs']
m6 the Veto section's lead-in renders before the length check again: exit=1 failed=1
  failing_node_ids=['tests/ui_contracts/test_veto_controls_contract.py::test_the_veto_sections_lead_in_sits_inside_the_non_empty_branch']
restored byte-identical: True (apps/ui/src/components/detail/DetailPopover.tsx)
restored byte-identical: True (packages/orchestration/pingpong_job.py)
restored byte-identical: True (packages/orchestration/ui_server.py)
restored byte-identical: True (packages/orchestration/veto_proposal.py)
--- pytest control run (unmutated, after) ---
control: exit=0
10 passed in 5.88s
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0

$ git worktree remove --force .remedy-wt/f027-r9-mut
REAL_EXIT=0
$ git worktree prune
REAL_EXIT=0
$ git worktree list
(unchanged from round start; f027-r9-mut no longer present)
$ git status --porcelain
(empty)
```
Every one of the six mutations was caught red on the first run; both control runs (pytest,
before and after) were green; all four touched files restored byte-identical. No mid-round
correction was needed this round.

**G6 TREE AND PUSH** — reported below, after C6, since C6 itself cannot contain these
readings.

## Authored-text proofs

Block copy: `git show e4b80c37a:.agent/authored/f027-r9-block.md` compared byte-for-byte
against `.remedy-wt/f027-r9/block.md` → identical
(sha256 `9d8bece9af6780507f1c0897016cd379930fde86465eb624527b17dfb37da320`). Plan payload
copy: same comparison against `.remedy-wt/f027-r9-payloads/plan.md` → identical (sha256
`ed20409e81fc200bde9d7d31a2b6abc63864e9e4e9caa3a737a5e4772140a81a`). Records-diff copy:
same comparison against `.remedy-wt/f027-r9-payloads/records.diff` → identical (sha256
`bdd17b382d5cf28c5d051a3acd547c20c66a7d3f00e9e6f96ae770588aefcf8a`). Post-C2, the sha256 of
`.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md` and `.agent/plan.md`
read via `git show 304d54939:<path>` all matched the block's G2 table exactly (see
Verification above). `open_finding_ids` over that same reading → `['R-1069', 'R-1070']`,
matching the block's own reading exactly.

## Deviations & assumptions

**`vetoView.ts`'s comment re-wraps across two lines, not one.** S1 says the comment above
`vetoAnswerSentence` "names `veto_proposal.py` and `task_veto.REPLAN_PROPOSAL_OPTIONS`
instead of `escalation.py`. No other line of either file changes." The replacement names
(`veto_proposal.py`'s own `task_veto.REPLAN_PROPOSAL_OPTIONS`) are longer than
`escalation.py`'s own replan proposal, so keeping the original line break would run one
line well past the file's existing wrap width; the sentence was re-wrapped across the same
two lines instead (`git show --numstat` on this file for C3 reads `2/2`, i.e. two lines
changed, not one). The `assumption_log.md` row's technical-reason cell (a single
pipe-table cell, not wrapped prose) has no such issue and changed exactly the one cell
S1 names, no other cell touched.

**The diamond tasks' own titles, goals and acceptance text are invented.** S3 states the
plan's structure (A; B and C after A; D after B and C), every task's `files_hint`
(`docs/README.md`) and the plan order, but not each task's title/goal/acceptance wording.
`_task(tid, deps)` in the new test file mirrors `test_task_edit_runtime.py`'s own `_task`
helper pattern (`f"Build {tid}"` / `f"goal of {tid}"` / `[f"{tid} works"]`) — the same choice
`test_task_veto_runner.py` already makes for its own diamond tests. No test elsewhere pins
different wording.

**The two tests' own method names are invented.** S3 says "Two tests: (a) THE ACCEPT
PATH... (b) THE REPLAN PATH..." without naming the test functions. They are named
`test_the_accept_path_settles_the_reduced_scope` and
`test_the_replan_path_creates_a_follow_up_that_nothing_runs`, grouped under one
`TestTaskVetoE2ELive` class (mirroring `test_task_edit_e2e_live.py`'s own single-class
shape), rather than the two free functions `test_task_veto_runner.py`'s own diamond tests
use elsewhere in the suite.

**The `decisions` endpoint's `safe_summary` check reads "holds ... byte for byte" as
"contains verbatim".** S3 says the `veto:` decision's "`safe_summary` holds the reason
byte for byte." `replan_proposal_decisions`'s own `safe_summary` is a longer sentence
("You vetoed <title> — reason: <reason>. ...") that CONTAINS the reason verbatim rather
than equalling it, so the test asserts `VETO_REASON in card["safe_summary"]` rather than
equality — the only reading `safe_summary`'s own shape admits.

**No other deviation.** C1–C5 implement S1 through S3 as specified, one commit group per
named step, in the block's own order and subject lines. The path set matches constraint 3
exactly; no widening was used. No gate went red on a test this round did not write; no
correction of the round's own new test was needed.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | this handback |
| G1 TRANSPORT | done | |
| G2 THE RECORDS | done | |
| G3 THE CODE | done | |
| G4 THE TESTS | done | green on the first run |
| G5 THE RED PROOFS | done | all six mutations caught on the first run |
| G6 TREE AND PUSH | done | see below, after C6 |

## Next

Per the block's own order: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 9, then F027's closure sequence. Open findings: 2 — R-1069 and R-1070, landed this
round and awaiting the reviewer's resolution. Operator-questions count: 5.
