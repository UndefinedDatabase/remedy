# Handback — F027 Task veto · Round 11 (closure sequence's repair round)

## Session

SESSION 2 of feature F027 · round 11 · rounds so far 11

Roughly two-thirds of the session's context budget remained at the point this handback was
written. This round booked round 10's PASS, registered R-1071, repaired it in
`tests/orchestration/test_task_expectation_episode_context.py` (the pin now names the three
statuses DECISION F027 D4 (5) rules, with a comment naming that decision and R-1071; the
parametrization of `test_a_completed_executed_task_that_actually_completed_passes` gained
`"vetoed"`; `packages/orchestration/run_manifest.py` did not change), built the round's
red-proof mutation tool, and took the feature's one full suite again on the repaired tree.
The repaired suite is still RED, but on a DIFFERENT node than round 10's: round 10's pinned
node (`test_the_context_helper_is_tight_for_completed_worked`) now PASSES, and a new,
unrelated node is bad — `tests/ui_server/test_pause_door_live.py::TestWithdrawLiveDoor::test_a_withdrawn_pause_never_parks_the_relaunch`.
That is a node newly bad against round 10's set, which constraint 4 forbids the repair from
producing; per that same constraint the transcript is committed exactly as measured and the
matter is handed back, not silently retried into a clean-looking run.

## Range

Review of `2425626ad..HEAD` (C1 through C5, this commit closes C5).

## Commits

### 8d68bcddc F027 R11 C1: copy round 11 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f027-r11-block.md | +149/-0 (new) | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f027-r11-plan.md | +29/-0 (new) | copy of the plan.md payload |
| .agent/authored/f027-r11-records.diff | +12/-0 (new) | copy of the records.diff payload |

190 insertions by `git show --numstat` — matches the block's stated expectation exactly
(block line count 149 plus 41), under the 500-line cap.

### 48cd71678 F027 R11 C2: book round 10, register R-1071
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | round 10's Gate entry and R-1071's registration, appended via `git apply` of records.diff |
| .agent/plan.md | +8/-9 | rewritten whole to the plan.md payload |

4/0 live_review.md, 8/9 plan.md by `git show --numstat` — matches the block's G2 table
exactly. `git apply --check` on records.diff → exit 0; the real `git apply` → exit 0.

### 0a1e65584 F027 R11 C3: the completed episode's tight-set pin reads the vetoed status D4 rules (R-1071)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_task_expectation_episode_context.py | +4/-2 | S1: `test_the_context_helper_is_tight_for_completed_worked` now asserts the three-status set with a comment naming D4 (5) and R-1071; `test_a_completed_executed_task_that_actually_completed_passes` gains the `"vetoed"` case |
| .agent/live_review.md | +2/-0 | the `Landed: R-1071 — ` line appended |

`packages/orchestration/run_manifest.py` did not change, as S1 required. `ruff check`
over the touched test file → clean (see G3 below).

### 29b0c2d20 F027 R11 C4: the round's red-proof mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f027-r11-mutations.py | +142/-0 (new) | the two-mutation red-proof tool for m1/m2 (G4) |

### (this commit) F027 R11 C5: record the closure suite on the repaired tree and rewrite handoff for round 11
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f027-closure-suite.txt | +4/-4 | rewritten whole: the repeated full suite's command, real exit code, wall time, summary line, the one (different) bad node id, and the tree it ran on, replacing round 10's run |
| .agent/handoff.md | see below | this handback, rewritten whole per `docs/agents/handback_template.md` |

## External actions

`git worktree add --detach .remedy-wt/f027-r11-mut 29b0c2d20` for G4's mutation run, then
`git worktree remove --force .remedy-wt/f027-r11-mut` immediately after — both succeeded;
`git worktree list` afterward shows every pre-existing worktree unchanged and
`f027-r11-mut` gone. `bash -c 'npm --prefix apps/ui run build ...'` — the one npm command
this round may run — exit 0. `git push origin feature/f027-task-veto` after this commit →
see G6 below for the real outcome. No pull request this round (block goal: "the evidence
bundle and the pull request belong to later rounds").

## Verification

**BEFORE ANYTHING ELSE (all four readings, all matched):**
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
2425626ad F027 R10 C4: record the closure suite transcript and rewrite handoff for round 10
```
All matched the block's step 2 exactly.

**Block bytes (step 3):** `.remedy-wt/f027-r11/block.md` → 149 lines (newline count), sha256
`0b3d50e25db460f3550bb87fde46bf9b9c8f84b79392bf66208841732429d207` — both the line count
and the sha256 match the delegation message's two readings exactly.

**Worktree list / job branches (step 4):** `git worktree list` — the primary checkout at
`2425626ad`, `f015-*` (1 through 9, dry+sim), `f020-*` (1 through 8, dry+sim), `f023-*` (1
through 10, dry+sim), `f024-*` (1 through 9, dry+sim/dry-only for 9), `f025-*` (r1-dry,
r2–r5-sim), `f027-r1-dry` through `f027-r8-dry`, `f284-*` (1 through 4, dry+sim), and ten
`job-*` worktrees. `git branch --list 'remedy/job-*'` — 48 branches. Both unchanged
across the round except for the G4 worktree's own add-then-remove.

**PAYLOADS** — readings (all matched the table):
| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 29 | 1039 | b3e9e2e2aa28f70720b555ef8b42680d629d32808459eb6bc1b6752e2bc583c6 |
| records.diff | 12 | 5070 | 412c10e61b096ad09ecb199e0d96a4009c06d0c138aafbae547c8edc84b5c01c |

**G1 TRANSPORT** — copy comparisons, all byte-identical:
- `git show 8d68bcddc:.agent/authored/f027-r11-block.md` compared against
  `.remedy-wt/f027-r11/block.md` via `cmp` → identical
- `git show 8d68bcddc:.agent/authored/f027-r11-plan.md` compared against
  `.remedy-wt/f027-r11-payloads/plan.md` via `cmp` → identical
- `git show 8d68bcddc:.agent/authored/f027-r11-records.diff` compared against
  `.remedy-wt/f027-r11-payloads/records.diff` via `cmp` → identical

**G2 THE RECORDS** — all matched the block's table exactly:
| read at | path | bytes | sha256 | match |
|---|---|---|---|---|
| C2 (48cd71678) | .agent/live_review.md | 331521 | eb8b293299b3f82a2cc3786fe08922a89caa61ce00bdabbb4aa5f96fa7819d1f | yes |
| C2 (48cd71678) | .agent/plan.md | 1039 | b3e9e2e2aa28f70720b555ef8b42680d629d32808459eb6bc1b6752e2bc583c6 | yes |

`open_finding_ids` (via `scripts/rotate_live_review.py`) over the ledger's text at
`48cd71678` → `['R-1071']` — matches the block's own reading exactly. Re-read over the
working tree after C4 (i.e. as it stands at C4, since C4 does not touch the ledger) →
still `['R-1071']`, matching the block's "at C2 and at C4" requirement. The ledger's last
line at C3 (`0a1e65584`) begins `Landed: R-1071 — ` — confirmed by reading the first 30
characters of `git show 0a1e65584:.agent/live_review.md | tail -1`.

**G3 THE CODE:**
```
$ python3 -m ruff check tests/orchestration/test_task_expectation_episode_context.py
All checks passed!
```
(Run at C3, i.e. the working tree was already at `0a1e65584` when this ran.)

`git diff 2425626a 0a1e65584 -- tests/orchestration/test_task_expectation_episode_context.py`
(whole, verbatim):
```diff
diff --git a/tests/orchestration/test_task_expectation_episode_context.py b/tests/orchestration/test_task_expectation_episode_context.py
index 99f66444f..7db3f60d3 100644
--- a/tests/orchestration/test_task_expectation_episode_context.py
+++ b/tests/orchestration/test_task_expectation_episode_context.py
@@ -63,14 +63,16 @@ class TestCompletedWorkedIsNarrow:
         probs = self._forge(status)
         assert any("impossible task record" in p for p in probs), (status, probs)
 
-    @pytest.mark.parametrize("status", ["passed", "applied_to_job_workspace"])
+    @pytest.mark.parametrize("status", ["passed", "applied_to_job_workspace", "vetoed"])
     def test_a_completed_executed_task_that_actually_completed_passes(self, status):
         assert self._forge(status) == []
 
     def test_the_context_helper_is_tight_for_completed_worked(self):
+        # DECISION F027 D4 (5) / R-1071: the completed-worked tight set carries `vetoed`
+        # too — a settled completion can finish a job carrying a vetoed task.
         for exp in (EXPECT_EXECUTED, EXPECT_PRIOR_EPISODE):
             allowed = _allowed_statuses_for(exp, "completed", PHASE_WORKED)
-            assert allowed == {"passed", "applied_to_job_workspace"}
+            assert allowed == {"passed", "applied_to_job_workspace", "vetoed"}
 
     def test_the_context_helper_stays_permissive_for_stopped_worked(self):
         """A stop can leave any of these — that is F011, and it must not regress."""
```

**G4 THE TESTS AND THE RED PROOFS** (at C4, `29b0c2d20`, serially):
```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider
    tests/orchestration/test_task_expectation_episode_context.py
    tests/orchestration/test_task_expectation_status_truth.py tests/orchestration/test_task_veto_runner.py
    tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py
    tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
219 passed in 64.32s (0:01:04)
REAL_EXIT=0
```
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=161", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
All six checks `pass`, `fail_count` 0.

**The mutation tool**, `.agent/authored/f027-r11-mutations.py`, run in
`git worktree add --detach .remedy-wt/f027-r11-mut 29b0c2d20` via
`python3 -B .agent/authored/f027-r11-mutations.py .remedy-wt/f027-r11-mut`, whole output:
```
==============================================================================
--- pytest control run (unmutated, before) ---
control: exit=0
33 passed in 0.35s
m1 vetoed leaves the completed worked EXPECT_EXECUTED tight set: exit=1 failed=2 failing_node_ids=['tests/orchestration/test_task_expectation_episode_context.py::TestCompletedWorkedIsNarrow::test_a_completed_executed_task_that_actually_completed_passes[vetoed]', 'tests/orchestration/test_task_expectation_episode_context.py::TestCompletedWorkedIsNarrow::test_the_context_helper_is_tight_for_completed_worked']
m2 vetoed leaves the completed worked EXPECT_PRIOR_EPISODE tight set: exit=1 failed=1 failing_node_ids=['tests/orchestration/test_task_expectation_episode_context.py::TestCompletedWorkedIsNarrow::test_the_context_helper_is_tight_for_completed_worked']
restored byte-identical: True (packages/orchestration/run_manifest.py)
--- pytest control run (unmutated, after) ---
control: exit=0
33 passed in 0.35s
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
Control first and last both green; each mutation caught exactly as the block's spec named
it (m1 reddens both the new `vetoed` case and the pin; m2 reddens only the pin, since the
parametrized "actually completed" test only ever forges `EXPECT_EXECUTED`); the touched
file restored byte-identical; the last line reads `True`. `git worktree remove --force
.remedy-wt/f027-r11-mut` → succeeded; `git worktree list` afterward shows it gone, every
other worktree unchanged.

**C5(a) THE UI BUILD:**
```
$ bash -c 'npm --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'
✓ built in 2.21s
REAL_EXIT=0
$ git status --porcelain
(empty)
```

**C5(b) THE CLOSURE SUITE** (log under `.remedy-wt/f027-r11-worker/full_suite.log`; the
committed transcript is `.agent/authored/f027-closure-suite.txt`):
```
$ time python3 -m pytest -n auto -q > .remedy-wt/f027-r11-worker/full_suite.log 2>&1
REAL_EXIT=1
real 3m28.426s (pytest's own report: 207.77s / 0:03:27)
```
Summary line: `1 failed, 19693 passed, 20 skipped, 1 warning in 207.77s (0:03:27)`

Bad node ids (failed plus errors — the FULL list, one entry):
```
tests/ui_server/test_pause_door_live.py::TestWithdrawLiveDoor::test_a_withdrawn_pause_never_parks_the_relaunch
```
Tree it ran on: C4's SHA `29b0c2d204c935aa812adfa6fdd37400758a0abb`.

**Whether round 10's bad node passes:** YES. Round 10's pinned node,
`tests/orchestration/test_task_expectation_episode_context.py::TestCompletedWorkedIsNarrow::test_the_context_helper_is_tight_for_completed_worked`,
is absent from this run's `FAILED`/`ERROR` lines, and the passed count rose by exactly one
(19692 → 19693) against round 10's run, consistent with that one node flipping from bad to
good and no other count shifting. The standalone file run at C3
(`tests/orchestration/test_task_expectation_episode_context.py`, 33 passed) already showed
the same thing in isolation.

**Whether any node is newly bad:** YES — `tests/ui_server/test_pause_door_live.py::TestWithdrawLiveDoor::test_a_withdrawn_pause_never_parks_the_relaunch`
was not in round 10's bad set (round 10's set was the one pin node named above) and is bad
in this run. Constraint 4 requires the repair to strictly shrink the bad set with no node
newly bad; this run does not meet that bar, even though the R-1071 repair itself is correct
and the pin now passes. Diagnostic-only (not part of the committed transcript, run
separately after the measured suite and not substituted for it): the same node run alone,
serially — `python3 -m pytest -q -p no:cacheprovider
tests/ui_server/test_pause_door_live.py::TestWithdrawLiveDoor::test_a_withdrawn_pause_never_parks_the_relaunch`
— passed (`1 passed in 3.90s`, exit 0), consistent with an xdist/parallel-scheduling flake
under `-n auto` rather than a regression the S1 repair caused; nothing in this round's diff
(`tests/orchestration/test_task_expectation_episode_context.py`, `.agent/live_review.md`,
`.agent/plan.md`, `.agent/authored/f027-r11-*`) touches `test_pause_door_live.py` or the
pause/live-door code it exercises. This finding is left for the reviewer to register and
rule on, per constraint 4's own instruction to commit the transcript exactly as measured
and hand back rather than retry toward a clean-looking run.

**G6 TREE AND PUSH** — reported below, after this commit and the push.

## Authored-text proofs

Block copy: `.remedy-wt/f027-r11/block.md` compared byte-for-byte via `cmp` against
`git show 8d68bcddc:.agent/authored/f027-r11-block.md`'s source file → identical (sha256
`0b3d50e25db460f3550bb87fde46bf9b9c8f84b79392bf66208841732429d207`). Payload copies: same
`cmp` comparison against each of `.remedy-wt/f027-r11-payloads/{plan.md,records.diff}` →
both identical (sha256 values in the PAYLOADS table above). Post-C2, the sha256 of
`.agent/live_review.md` and `.agent/plan.md`, read via `git show <sha>:<path>`, matched the
block's G2 table exactly (see Verification above). `open_finding_ids` over the C2 reading
→ `['R-1071']`, matching the block's own reading exactly; the same read at C4 (working
tree) → still `['R-1071']`.

## Deviations & assumptions

**None in C1–C4.** Every commit matches the block's stated `git show --numstat` expectation
exactly; the payload was not retyped or edited; `git apply --check` preceded the real
`git apply` and both returned exit 0.

**C5(b)'s repeated full suite is RED, on a node DIFFERENT from round 10's pin, which is a
newly-bad node under constraint 4.** Constraint 4 states the repair must strictly shrink
the bad set with no node newly bad, and separately states what to do "if C5's suite is
red": commit the transcript exactly as measured, report every bad node id, and hand back —
never weaken an assertion, delete a test or mark anything xfail. That is exactly what this
round did. The S1 repair itself is verified correct (G3's diff, G4's green selection and
red proofs, and round 10's pinned node now passing all agree); the new red node,
`tests/ui_server/test_pause_door_live.py::TestWithdrawLiveDoor::test_a_withdrawn_pause_never_parks_the_relaunch`,
sits in a file this round never touched and passed cleanly when run alone (diagnostic run,
reported above, not substituted for the measured transcript), which points to a
parallel-scheduling flake rather than a regression from S1 — but that judgment is left to
the reviewer, not asserted as this handback's verdict. No assertion was weakened, no test
deleted, nothing marked `xfail`.

**No other deviation.** C1 through C5 implement the block's steps in the block's own order
and subject lines. The round's tracked path set matches constraint 3 exactly. No edit
touched `packages/`, `apps/`, any other test, `README.md`, `docs/`, `scripts/`,
`.agent/decisions.md`, `.agent/candidates.md` or `.agent/operator_questions.md`.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 (S1 repair) | done | pin now names three statuses with the D4(5)/R-1071 comment; parametrization gains `vetoed`; `run_manifest.py` unchanged |
| C3 Landed line | done | appended to `.agent/live_review.md` |
| C4 mutation tool | done | both mutations caught, control green before/after, file restored byte-identical |
| C5(a) UI build | done | exit 0 |
| C5(b) full suite | done | RED, 1 bad node id (newly bad, not round 10's pin), committed as measured per constraint 4 |
| C5(c) transcript + handoff | done | this handback |
| G1 TRANSPORT | done | |
| G2 THE RECORDS | done | |
| G3 THE CODE | done | |
| G4 THE TESTS AND THE RED PROOFS | done | |
| G5 THE INTEGRATION GATE | done | RED full suite declared, newly-bad node flagged, not silently retried |
| G6 TREE AND PUSH | done | see below, after this commit |

## Next

Per the block's own order: Phase 1 rule 1, the review of round 11, then the closure's
evidence round — the booking of round 11, the Built State's note on R-1071, the evidence
bundle and the review package — and then the closing round. Open findings: 1 (`R-1071`,
per `open_finding_ids` at C4 — landed but not yet booked as resolved by a Gate entry).
Operator questions open: 5.
