# Handback — F027 Task veto · Round 1

## Session

SESSION 1 of feature F027 · round 1 · rounds so far 1

The large majority of the session's context budget remained at the point this handback was
written. This round claimed F027, re-headed the live review record, booked F285's round 6 verdict,
recorded DECISION F027 D1, and landed the first part of T001: the `TASK_VETOED` status and a new
module `packages/orchestration/task_veto.py` (the mandatory verbatim reason, the pure state gate,
the unreachable set, the create-only control file, the command effect and its `task_vetoed`
event), with its unit tests and a mutation tool proving they bite.

## Range

Review of 557cbbcc5..HEAD

## Commits

### c63d3f1e5 F027 R1 C1a: copy round 1 block and state payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f027-r1-block.md | +331/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f027-r1-context.md | +37/-0 | copy of the context.md payload |
| .agent/authored/f027-r1-plan.md | +37/-0 | copy of the plan.md payload |

405 insertions by `git show --numstat` (331 for the block plus 74 for the two payloads: 37+37) —
matches the block's stated expectation exactly (block line count 331 plus 74), under the 500-line
cap.

### 84115d5bd F027 R1 C1b: copy round 1 claim diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f027-r1-claim.diff | +163/-0 | copy of the claim.diff payload |

163 insertions by `git show --numstat` — matches the block's stated expectation (163) exactly.

### 16de198d5 F027 R1 C2: claim F027, re-head the live review record, book F285 R6, record D1
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | +15/-11 | rewritten whole to the context.md payload |
| .agent/decisions.md | +84/-0 | DECISION F027 D1 appended, verbatim from claim.diff |
| .agent/live_review.md | +22/-20 | re-headed (heading + intro + Steps) and F285 R6's Gate entry appended |
| .agent/plan.md | +24/-13 | rewritten whole to the plan.md payload |
| docs/roadmap/STATUS.md | +1/-1 | F027's line `[ ]` → `[~]` |

15/11 context.md, 84/0 decisions.md, 22/20 live_review.md, 24/13 plan.md, 1/1 STATUS.md by
`git show --numstat` — matches the block's stated expectation exactly.

### 95dfdc1f8 F027 R1 C3: add the task veto control protocol and the vetoed task status
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/event_names.py | +1/-0 | `"task_vetoed"` added to `EVENT_NAMES` in sorted place |
| packages/orchestration/pingpong_job.py | +3/-0 | `TASK_VETOED = "vetoed"` added after `TASK_SPLIT`, with its DECISION F027 D1 comment |
| packages/orchestration/task_veto.py | +488/-0 | NEW: S1–S9 — the veto control protocol module |
| tests/test_no_orphan_modules.py | +3/-0 | `ALLOWED_UNWIRED` entry for the new, not-yet-wired module |

495 insertions by `git show --numstat` (no expectation was stated for C3; reported as measured),
under the 500-line cap.

### 7f5383abd F027 R1 C4a: test the veto reason, gate, unreachable set and control files (part 1 of 2)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_task_veto.py | +350/-0 | NEW (part 1 of 2): constants, S3 reason tests, S4 gate matrix, S5 unreachable-set tests, S6 control-file tests |

350 insertions by `git show --numstat`.

### f93fb8028 F027 R1 C4b: test the command effect and its event, add the mutation tool (part 2 of 2)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_task_veto.py | +183/-0 | REST (part 2 of 2): S7 command-effect tests, S8 event tests |
| .agent/authored/f027-r1-mutations.py | +234/-0 | NEW: the G5 mutation tool, 15 mutations over `task_veto.py` |

417 insertions by `git show --numstat` (no expectation was stated for C4; reported as measured),
under the 500-line cap. See Deviations: C4 was split into C4a/C4b because the whole tests file plus
the mutation tool (767 insertions together) would have exceeded the 500-line cap in one commit.

## External actions

`git checkout -b feature/f027-task-veto` from `main` at `557cbbcc5` — branch created.
`git worktree add --detach .remedy-wt/f027-r1-mut f93fb8028` — worktree created for the G5 mutation
sweep.
`git worktree remove --force .remedy-wt/f027-r1-mut` — removed after the sweep completed.
`git worktree prune` — no-op (nothing stale).
`git push -u origin feature/f027-task-veto` — pushed after C5 (outcome reported in the final reply,
since C5 cannot contain it per the block).
No PR created (the block forbids it this round; F027's PR opens at closure).

## Verification

BEFORE ANYTHING ELSE:
- `ls .agent/STOP` → `ls: cannot access '.agent/STOP': No such file or directory`, exit 2 (absent, as
  required).
- `pwd` → `/home/decodeux/Repos/remedy`; `git status --porcelain` → empty; `git branch --show-current`
  → `main`; `git log --oneline -1` → `557cbbcc5 Merge pull request #282 ...`. All three matched.
  `git checkout -b feature/f027-task-veto` → `Switched to a new branch 'feature/f027-task-veto'`.
- Block bytes: measured line count 331, sha256
  `42bfc4e4e7fd4c11e8ae18f426e8cbb31fbbfc993cef0d84935310f12f53ddb3` — both matched the delegation
  message's two readings exactly.
- `git worktree list` reported as found (see the pre-round listing in the round transcript; all
  entries constraint 6 names, unchanged by this round until the G5 worktree was added and removed).

PAYLOADS (measured against the block's table, all matched):
| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 163 | 18444 | 2a11dfd7...78bfbe |
| context.md | 37 | 1520 | d3ca4f45...2f51841 |
| plan.md | 37 | 1533 | de29e39c...5080465fcaaa8a392 |

`git apply --check` on claim.diff → exit 0. `git apply` (real) → exit 0.

G1 TRANSPORT — each `.agent/authored/f027-r1-*` copy compared byte for byte, read back with
`git show <commit>:<path>`, against its source:
- `f027-r1-block.md` @ c63d3f1e5 == `.remedy-wt/f027-r1/block.md`: match=True (sha256
  `42bfc4e4...f53ddb3` both sides)
- `f027-r1-plan.md` @ c63d3f1e5 == payload plan.md: match=True
- `f027-r1-context.md` @ c63d3f1e5 == payload context.md: match=True
- `f027-r1-claim.diff` @ 84115d5bd == payload claim.diff: match=True

G2 THE CLAIM — each file's sha256, read with `git show 16de198d5:<path>`, against the reviewer's
table:
| path | bytes | sha256 | match |
|---|---|---|---|
| .agent/live_review.md | 290468 | 1e4eb4d2...53146382 | True |
| docs/roadmap/STATUS.md | 53437 | b52bb1a5...09f1222e | True |
| .agent/decisions.md | 2155629 | fd65eba3...34c9d8418 | True |
| .agent/plan.md | 1533 | de29e39c...5080465fcaaa8a392 | True |
| .agent/context.md | 1520 | d3ca4f45...2f51841 | True |

Open finding ids via `open_finding_ids` (scripts/rotate_live_review.py): at `557cbbcc5` → `[]`; at
`16de198d5` → `[]`. Both empty, matching the reviewer's reading.
`## Findings` heading count at C2: 1. `## Steps` heading count at C2: 1. Last non-blank line of
the ledger at C2 begins `Gate: F285 R6 — ` (confirmed verbatim).
F027's STATUS line at C2, read in full: `- [~] F027 — Task veto`.
`git diff --name-only 84115d5bd 16de198d5` → `.agent/context.md`, `.agent/decisions.md`,
`.agent/live_review.md`, `.agent/plan.md`, `docs/roadmap/STATUS.md` — exactly the table's five
paths.

G3 THE CODE:
```
$ python3 -m ruff check packages/orchestration/pingpong_job.py packages/orchestration/task_veto.py packages/orchestration/event_names.py tests/test_no_orphan_modules.py tests/orchestration/test_task_veto.py
All checks passed!
```
(run again at C4, same result: `All checks passed!`)

`git diff -U0 84115d5bd 95dfdc1f8 -- packages/orchestration/pingpong_job.py packages/orchestration/event_names.py`
— whole diff:
```
diff --git a/packages/orchestration/event_names.py b/packages/orchestration/event_names.py
+        "task_vetoed",
diff --git a/packages/orchestration/pingpong_job.py b/packages/orchestration/pingpong_job.py
+# DECISION F027 D1: terminal for the task — a runner's fold writes this status at its
+# safe points once a control file records the veto; the veto command itself never writes it.
+TASK_VETOED = "vetoed"
```
Adds the constant with its comment and the one event name, nothing else — confirmed.

AST reading of every module `task_veto.py` imports (each `Import`/`ImportFrom`, any depth):
`['__future__', 'dataclasses', 'hashlib', 'json', 'os', 'packages.common',
'packages.orchestration', 'packages.orchestration.dag_schedule',
'packages.orchestration.data_paths', 'packages.orchestration.failure_postmortem',
'packages.orchestration.pingpong_job', 'packages.orchestration.run_log',
'packages.orchestration.stream_evidence', 'pathlib', 're', 'typing']`. Banned-set intersection
(`subprocess`, `threading`, `signal`, `packages.orchestration.pause_control`): empty set. Confirmed
none present.

G4 THE TESTS — serial run in the primary checkout at C4b (real exit code):
```
$ python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_task_veto.py tests/orchestration/test_pause_control.py tests/orchestration/test_dag_schedule.py tests/orchestration/test_event_names.py tests/test_no_orphan_modules.py tests/orchestration/test_task_edit_runtime.py tests/orchestration/test_task_expectation_status_truth.py tests/orchestration/test_import_reachability.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): ...
960 passed, 1 skipped in 86.81s (0:01:26)
REAL_EXIT=0
```
Only one `SKIPPED` line printed by `-rs`: the D12 quarantine in `tests/test_agent_tooling.py`
(stays skipped, as expected). Both toolchain nodes the reviewer's run skipped (the typescript node
in `tests/ui_server/test_dashboard_contract.py`, the vitest node in
`tests/orchestration/test_test_runner.py`) PASSED here, not skipped.

`--collect-only -q` on the new file alone: `127 tests collected`.

Accounting for the difference from the reviewer's `789 passed, 3 skipped`: reviewer's selection
omitted the new test file and the golden path. `789 + 127 (new file) + 42 (golden path,
`--collect-only -q tests/cli/test_golden_path.py` → `42 tests collected`) = 958`; plus the 2
toolchain skips that now pass instead of skip = `960` passed, with only the 1 permanent skip
remaining — `958 + 2 = 960` passed, `1` skipped, total `961` nodes selected, matching
`792 (reviewer's 789+3) - 3 + 127 + 42 = 961` exactly.

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, ... "fail_count": 0, "ok": true, "passed": true, ...}
REAL_EXIT=0
```
All six checks read `pass`, `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f027-r1-mut f93fb8028` (exit 0), then
`python3 -B .agent/authored/f027-r1-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f027-r1-mut`:
```
--- control run (unmutated, before) ---
control: exit=0
127 passed in 0.49s
m1 a whitespace-only reason is accepted: exit=1 failed=3 failing_node_ids=[...3 nodes...]
restored byte-identical: True
m2 a 501-character reason is accepted: exit=1 failed=1 failing_node_ids=[...1 node...]
restored byte-identical: True
m3 a reason holding a control character is accepted: exit=1 failed=4 failing_node_ids=[...4 nodes...]
restored byte-identical: True
m4 a secret-shaped reason is accepted: exit=1 failed=1 failing_node_ids=[...1 node...]
restored byte-identical: True
m5 an accepted reason is returned stripped: exit=1 failed=1 failing_node_ids=[...1 node...]
restored byte-identical: True
m6 the gate admits a completed job: exit=1 failed=12 failing_node_ids=[...12 nodes...]
restored byte-identical: True
m7 the gate admits an applied_to_job_workspace task: exit=1 failed=7 failing_node_ids=[...7 nodes...]
restored byte-identical: True
m8 the gate refuses a skipped task: exit=1 failed=7 failing_node_ids=[...7 nodes...]
restored byte-identical: True
m9 the gate ignores already_vetoed: exit=1 failed=3 failing_node_ids=[...3 nodes...]
restored byte-identical: True
m10 the control file is named by the task id itself instead of its digest: exit=1 failed=2 failing_node_ids=[...2 nodes...]
restored byte-identical: True
m11 the unreachable set keeps a task whose work is done: exit=1 failed=1 failing_node_ids=[...1 node...]
restored byte-identical: True
m12 the control file is published without create_only, so a second veto replaces the first: exit=1 failed=2 failing_node_ids=[...2 nodes...]
restored byte-identical: True
m13 the command writes the event without reading the ledger first: exit=1 failed=1 failing_node_ids=[...1 node...]
restored byte-identical: True
m14 the command checks the task before the reason: exit=1 failed=1 failing_node_ids=[...1 node...]
restored byte-identical: True
m15 the command's unreachable set keeps another veto's tasks: exit=1 failed=1 failing_node_ids=[...1 node...]
restored byte-identical: True
--- control run (unmutated, after) ---
control: exit=0
127 passed in 0.49s
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
REAL_EXIT=0 (full untrimmed output, including every named failing node id, is in the round
transcript and reproducible by re-running the tool). Every one of the 15 mutations was red with at
least one failing node; none stayed green; every restoration was byte-identical.

`git worktree remove --force .remedy-wt/f027-r1-mut` → exit 0. `git worktree prune` → exit 0.
`git worktree list` afterward: primary checkout plus exactly the worktrees constraint 6 names
(`f015-*`, `f020-*`, `f023-*`, `f024-*`, `f025-*`, `f027-r1-dry`, `f284-*`, and the `job-*`
worktrees) — nothing else.

CONSTRAINT 3 — round path set: `git diff --name-only 557cbbcc5` (before C5) named exactly:
`.agent/authored/f027-r1-block.md`, `.agent/authored/f027-r1-claim.diff`,
`.agent/authored/f027-r1-context.md`, `.agent/authored/f027-r1-mutations.py`,
`.agent/authored/f027-r1-plan.md`, `.agent/context.md`, `.agent/decisions.md`,
`.agent/live_review.md`, `.agent/plan.md`, `docs/roadmap/STATUS.md`,
`packages/orchestration/event_names.py`, `packages/orchestration/pingpong_job.py`,
`packages/orchestration/task_veto.py`, `tests/orchestration/test_task_veto.py`,
`tests/test_no_orphan_modules.py` — the block's whole named set, nothing extra. None of the
forbidden paths (pause_control.py, safe_points.py, dag_schedule.py, ui_server.py,
command_catalog.py, apps/ui/**, prose_slips.md, candidates.md, operator_questions.md, README.md,
T5_F027.md) were touched.

G6 TREE AND PUSH — real readings reported in the final reply (this file cannot contain them, since
they are measured AFTER this commit).

## Authored-text proofs

Every `.agent/authored/f027-r1-*` copy was compared disk-to-disk against its committed source and
matched byte for byte (see G1 above): the block copy, the plan and context payload copies, and the
claim diff copy. `f027-r1-mutations.py` is the worker's own tool, not a reviewer-authored payload —
no fidelity proof applies to it.

## Deviations & assumptions

1. C4 was split into C4a and C4b. The block's bundle names C4 as one commit ("THE TESTS AND THE
   MUTATION TOOL"), but the whole test file (533 insertions) plus the mutation tool (234
   insertions) totals 767 insertions — over the 500-line cap even before considering the test file
   alone exceeds it (533). Per AGENTS.md's commit-size rule and this block's constraint 2 ("split a
   commit that would reach it into parts with their own subjects (C3a and C3b, C4a and C4b)"), the
   test file was split at a natural class boundary (end of `TestControlFiles`, S3–S6 coverage) into
   C4a (350 insertions: constants, S3, S4, S5, S6 tests) and C4b (417 insertions: the rest of the
   test file — S7, S8 tests — plus the mutation tool). Both stay under the 500-line cap. This is
   the only oversize-avoidance split in this round.
2. The command effect's exact response shape for the race-lost branch (`record_task_veto`
   answering `False` after the S4 gate already passed) required an interpretive decision the block
   states somewhat ambiguously: whether `nothing written by a refusal` (an S7 test requirement)
   applies to the `task_already_vetoed` OUTCOME the block describes for that branch. This worker
   read `refused` (with a `code`) and the bare `task_already_vetoed` outcome as two DISTINCT
   response shapes — the pre-check gate refusal writes nothing at all (satisfying "nothing written
   by a refusal"), while the race-lost branch (reachable only via a genuine create-only race, never
   via a second sequential command call once an entry is known) is the one that performs the S8
   event-repair check, since it alone is where "a retry after a failed event write repairs the
   audit line exactly once" is actually reachable. This reading is implemented, unit-tested directly
   (`TestTaskVetoedEvent.test_a_retry_repairs_a_missing_event_after_a_failed_write`) and red-proved
   by mutations m9 and m13.
3. No other deviation from the block's ordered commit sequence, specification or constraints.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4a | deviated | C4 split into C4a/C4b — the whole file plus tool exceeds the 500-line cap |
| C4b | deviated | see C4a |
| C5 | done | |
| G1 TRANSPORT | done | |
| G2 THE CLAIM | done | |
| G3 THE CODE | done | |
| G4 THE TESTS | done | |
| G5 THE RED PROOFS | done | |
| G6 TREE AND PUSH | done | reported in the final reply, not this file, per the block |

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 1, then the rest of T001:
the runners fold a veto at their safe points, the in-progress finish rule, and the terminal
accounting. Open findings: 0. Operator questions: 5.
