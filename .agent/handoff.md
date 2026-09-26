# Handoff — F288, round 1

## Session

SESSION 1 of feature F288 · round 1 · rounds so far 1. Context remaining at
handback: ample — the round finished its full specification, tests and red
proofs inside a single session with no repair needed.

## Range

Review of `db691093`..`HEAD` (`HEAD` is this handback's own commit, `F288 R1
C5`, on `feature/f288-event-stream-completeness`).

## Commits

### edb28f5e4 F288 R1 C1a: copy round 1 block and state payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f288-r1-block.md | 313/0 | copy of this round's block (`shutil.copyfile`) |
| .agent/authored/f288-r1-context.md | 35/0 | copy of the context.md payload |
| .agent/authored/f288-r1-plan.md | 33/0 | copy of the plan.md payload |

Measured insertions: 381 (313+35+33), matching the block's expectation
(block's own line count 313 plus 68).

### 717a96ee1 F288 R1 C1b: copy round 1 claim diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f288-r1-claim.diff | 146/0 | copy of the claim.diff payload |

Expected by the block: 146 — measured identically.

### 1896f177b F288 R1 C2: claim F288, re-head the live review record, book F289 R7, record D1
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | 13/16 | rewritten to the context.md payload |
| .agent/decisions.md | 63/0 | DECISION F288 D1 appended (`git apply claim.diff`) |
| .agent/live_review.md | 23/22 | re-headed + F289 R7 gate entry appended (`git apply claim.diff`) |
| .agent/plan.md | 20/13 | rewritten to the plan.md payload |
| docs/roadmap/STATUS.md | 1/1 | F288's line `[ ]` → `[~]` (`git apply claim.diff`) |

Expected by the block: 13/16 context.md, 63/0 decisions.md, 23/22
live_review.md, 20/13 plan.md, 1/1 STATUS.md — measured identically.

### 97d84b332 F288 R1 C3: mint each execution's attempt id, write a test and a repair event per round, and carry the attempt id in the stream
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/humanizeCatalog.ts | 2/0 | S5: `task_round_repaired`/`task_round_tested` catalog lines |
| packages/orchestration/event_names.py | 2/0 | S5: `EVENT_NAMES` gains the two names |
| packages/orchestration/pingpong_job.py | 69/23 | S2/S3: attempt id minted, `_repair_result`, the two new round events, `attempt_id` threaded through `_log_task_started`/`_log_task_rounds`/`_log_task_ended` and every call site |
| packages/orchestration/pingpong_loop.py | 9/0 | S1: `run_pingpong` gains the `run_id` keyword |
| packages/orchestration/teacher_narration.py | 7/2 | S5: `NARRATED_EVENTS` gains the two templates |
| packages/orchestration/timeline.py | 15/0 | S6: `_render_task_block`'s rounds line |
| packages/orchestration/ui_server.py | 22/0 | S4: `ATTEMPT_EVENT_KINDS` and the envelope's conditional `attempt_id` |

Measured insertions: 126 (2+2+69+9+7+15+22). No count was expected by the
block for C3 (it says "none is expected for C3 and C4 — report what you
measure"); this is what was measured. `ruff check` over these seven files
(the `.ts` file is not a ruff target; the six Python files are): all checks
passed, real exit 0.

### f5c118f20 F288 R1 C4a: test the attempt id, the round events, the envelope and their readers
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_job_task_runner.py | 160/0 | `TestAttemptIdAndRoundEvents`: the E2E ordered-sequence test, the no-test-result test, the `_log_task_started`/`_log_task_ended` attempt-id test, the `_repair_result` classification test |
| tests/orchestration/test_mint_call_sites.py | 27/0 | AST test: exactly one `attempt_id = ...` assignment, calling `mint_run_id` |
| tests/orchestration/test_pingpong.py | 17/0 | `TestRunPingpongAdoptsGivenRunId`: a given `run_id` is adopted; none mints a different 16-hex id |
| tests/orchestration/test_teacher_narration.py | 16/0 | pinned sorted list gains the two names; exact-sentence test for each |
| tests/test_timeline.py | 51/0 | `TestRenderRoundsLine`: exact rounds-line text; no line when no `task_round_completed` |
| tests/ui_server/test_sse_stream.py | 51/0 | `TestAttemptEventKinds`: the pinned set, key order, metadata-only read, top-level ignored, base kinds unchanged |

Measured insertions: 322 (160+27+17+16+51+51). No count was expected by the
block for C4 either; this is what was measured.

### 3ad8ec04b F288 R1 C4b: add the mutation tool for the round's red proofs
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f288-r1-mutations.py | 261/0 | the round's G5 mutation/red-proof tool |

**DEVIATION** (declared before commit, per constraint 2): the block names one
commit "C4 — THE TESTS AND THE TOOL". Combined, the six test files (322
insertions) plus the mutation tool (261 insertions) total 583 insertions,
over the 500-insertion cap. Split into C4a (the six test files, 322) and C4b
(the tool, 261), each under the cap, exactly as constraint 2 directs ("split
a commit that would reach it into parts with their own subjects (C3a and
C3b, C4a and C4b), and say so").

### (this commit) F288 R1 C5: rewrite handoff for round 1
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this handback (a handback cannot table the commit that writes it) |

## External actions

- `git checkout -b feature/f288-event-stream-completeness` from `main` at
  `db691093` — real outcome reported in the reply (BEFORE ANYTHING ELSE).
- `git worktree add --detach .remedy-wt/f288-r1-basecount db691093`, used to
  measure the base `--collect-only` node count for G4's accounting, then
  `git worktree remove --force .remedy-wt/f288-r1-basecount` and `git
  worktree prune` — count restored to the step-4 reading (62) before
  continuing. Not one of the block's named directories; added and removed
  entirely inside this round for a read-only measurement, per constraint 6
  (no branch was created — `--detach`) and left no trace.
- `git worktree add --detach .remedy-wt/f288-r1-mut <C4b>` for G5, then
  `git worktree remove --force .remedy-wt/f288-r1-mut` and `git worktree
  prune` after the tool ran — count restored to 62. Reported in full in the
  reply (G5).
- `git push -u origin feature/f288-event-stream-completeness` after C5 —
  real outcome reported in the reply (G6), since this file cannot contain
  the reading of its own commit.
- No merge, no `gh pr create`, no checkout of `main`, no branch deletion, no
  force-push, no stash.

## Verification

BEFORE ANYTHING ELSE:
- `ls .agent/STOP` → `No such file or directory` (does not exist).
- `pwd` → `/home/decodeux/Repos/remedy`. `git status --porcelain` → empty.
  `git branch --show-current` → `main`. `git log --oneline -1` →
  `db6910931 Merge pull request #285 from
  UndefinedDatabase/feature/f289-self-use-sources` — all matched the
  delegation message exactly. Then `git checkout -b
  feature/f288-event-stream-completeness` → `Switched to a new branch
  'feature/f288-event-stream-completeness'`.
- Block bytes: measured 313 lines, sha256
  `8afd8e04ae570bb0aebc22dfbe1e185c80143273d0e43a610b0703fad40b8511` against
  `.remedy-wt/f288-r1/block.md` — both matched the delegation message
  exactly.
- `git worktree list | wc -l` → 62 (step-4 reading, reported again unchanged
  in the reply's G6).

PAYLOADS (measured against the table, before use, all three matched exactly
on lines, bytes and sha256): claim.diff (146/17375/`cea11c4a...`), context.md
(35/1535/`7a4891c5...`), plan.md (33/1257/`22c7cdd6...`).

G1 TRANSPORT — every payload matched the table (see PAYLOADS above); every
`.agent/authored/f288-r1-*` copy read back with `git show <commit>:<path>`
compared byte-for-byte against its source: all four byte-identical (block
copy at `edb28f5e4` against `.remedy-wt/f288-r1/block.md`; plan/context
copies at `edb28f5e4` against their payloads; claim.diff copy at `717a96ee1`
against its payload). Full readings in the reply.

G2 THE CLAIM — read with `git show 1896f177b:<path>`, all five matched the
reviewer's table exactly:
| path | bytes | sha256 match |
|---|---|---|
| docs/roadmap/STATUS.md | 54469 | yes |
| .agent/live_review.md | 298511 | yes |
| .agent/decisions.md | 2224108 | yes |
| .agent/plan.md | 1257 | yes |
| .agent/context.md | 1535 | yes |

`open_finding_ids` over `.agent/live_review.md` at `db691093` and at
`1896f177b` → `[]` both times. Exactly one `## Findings` line and one `##
Steps` line at C2. Last line of the ledger at C2 begins `Gate: F289 R7 — `.
STATUS line at C2 begins `- [~] F288 — `. `git diff --name-only 717a96ee1
1896f177b` names exactly the five paths of the table above.

G3 THE CODE — `python3 -m ruff check` over the six Python files C3 names
plus the six test files, at C4b: **all checks passed, real exit 0**. Quoted
from `git show 97d84b332`:

The `run_pingpong` call's new keyword:
```
                    resumed_from_run_id=task.run_id if resume_sessions else "",
+                    run_id=attempt_id,
                 )
```

The whole of `_log_task_rounds` and `_repair_result`:
```
+def _repair_result(rnd: Any) -> str:
+    """The outcome of a repair round for ``task_round_repaired`` (DECISION F288 D1):
+    ``"error"`` when the round has no builder output or its output names an error,
+    ``"changed"`` when its output names at least one changed file, and ``"unchanged"``
+    otherwise."""
+    output = rnd.builder_output
+    if output is None or output.error:
+        return "error"
+    if output.files_changed:
+        return "changed"
+    return "unchanged"
+
+
 def _log_task_rounds(log: Any, task: TaskEntry, result: Any, attempt_id: str) -> None:
-    """One ``task_round_completed`` per ping-pong round, with the reviewer's verdict."""
+    """For each ping-pong round, in round order (DECISION F288 D1): ``task_round_repaired``
+    when the round is a repair, ``task_round_tested`` when its test ran, then
+    ``task_round_completed`` as before, with the reviewer's verdict. Every event carries
+    ``attempt_id``.
+    """
     try:
         for rnd in (result.rounds if log is not None else ()):
+            if rnd.kind == "repair":
+                log.log("task_round_repaired", task_id=task.task_id,
+                        outcome=_repair_result(rnd), round_number=rnd.round_number,
+                        attempt_id=attempt_id)
+            if rnd.test_passed is not None:
+                log.log("task_round_tested", task_id=task.task_id,
+                        outcome="pass" if rnd.test_passed else "fail",
+                        round_number=rnd.round_number, attempt_id=attempt_id)
             verdict = rnd.reviewer_output.verdict if rnd.reviewer_output else ""
             log.log("task_round_completed", task_id=task.task_id,
                     outcome=verdict or "no_review", round_number=rnd.round_number,
-                    round_kind=rnd.kind, test_passed=rnd.test_passed)
+                    round_kind=rnd.kind, test_passed=rnd.test_passed, attempt_id=attempt_id)
     except _TASK_LOG_ERRORS:
         pass
```

The whole of `_safe_event_summary`'s new branch:
```
+# DECISION F288 D1 (5): the kinds an attempt (one execution of a task by `run_job`)
+# writes, round 1. Round 2 adds the rest of T001's kinds — the run-next path, the test
+# service, the long-run executor's repair events and the plan-approved event.
+ATTEMPT_EVENT_KINDS: frozenset[str] = frozenset({
+    "task_run_started",
+    "task_round_repaired",
+    "task_round_tested",
+    "task_round_completed",
+    "task_run_completed",
+    "task_run_failed",
+})
...
+    if kind in ATTEMPT_EVENT_KINDS:
+        attempt_id = metadata.get("attempt_id") if isinstance(metadata, dict) else None
+        summary["attempt_id"] = attempt_id if isinstance(attempt_id, str) else ""
```

G4 THE TESTS — in the primary checkout at C4b, SERIALLY:
```
1763 passed, 1 skipped in 190.03s (0:03:10)
REAL_EXIT=0
```
SKIPPED line printed by `-rs`:
```
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
```
Accounting: base selection (per the block) was 1743 passed, 1 skipped.
`--collect-only -q` on the six edited test files: 428 nodes at `db691093`,
448 nodes at C4b — the round adds 20 nodes. 1743 + 20 = 1763, matching the
measured total exactly; no unexplained difference.

`python3 -m apps.cli.main integrity check --json`:
```
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=161"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true}
```
Six of six `pass`, `fail_count` 0, real exit 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f288-r1-mut
3ad8ec04b`, then `python3 -B .agent/authored/f288-r1-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f288-r1-mut`, real exit 0. Full
output (all 13 mutations caught, both controls clean, all six files
restored byte-identical) reported in the reply. Then `git worktree remove
--force .remedy-wt/f288-r1-mut`, `git worktree prune`; `git worktree list |
wc -l` → 62 (unchanged from step 4).

G6 TREE AND PUSH — reported in full in the reply, since C5 cannot contain
the reading of its own commit.

## Authored-text proofs

The block copy (`.agent/authored/f288-r1-block.md`) and the two state-payload
copies (`plan.md`, `context.md`), read back at `edb28f5e4`, equal the
reviewer's originals byte for byte (G1). The claim-diff copy
(`.agent/authored/f288-r1-claim.diff`), read back at `717a96ee1`, equals its
payload byte for byte (G1). `claim.diff` was applied with `git apply`
unedited (constraint 1: `git apply --check` real exit 0, then the real `git
apply`, also real exit 0), confirmed byte-identical by the G2 sha256
readings of all five touched files. `plan.md` and `context.md` were
rewritten into `.agent/plan.md` and `.agent/context.md` verbatim via
`shutil.copyfile`, also confirmed byte-identical by the G2 sha256 readings.
No payload was retyped or edited.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| BEFORE ANYTHING ELSE 1–4 | done | |
| PAYLOADS verification | done | all three matched |
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4 | deviated | split into C4a and C4b — see Deviations |
| C5 | done | this handback |
| G1 | done | |
| G2 | done | |
| G3 | done | ruff clean; diffs quoted in Verification |
| G4 | done | 1763 passed, 1 skipped, accounted for exactly |
| G5 | done | all 13 mutations caught, both controls clean |
| G6 | done | reported in the reply |
| Constraint 1 (no retype, `git apply --check` first) | done | |
| Constraint 2 (every commit under 500 insertions) | deviated | C4 split into C4a (322) and C4b (261) |
| Constraint 3 (tracked path set) | done | matches exactly, see reply |
| Constraint 4 (stop/handoff if a gate goes red) | done | no gate was red, so no stop path was needed |
| Constraint 5 (nothing merged) | done | no PR created, no checkout of main, no branch deletion, no force-push, no stash |
| Constraint 6 (leave other worktrees/branches/stashes alone) | done | only the base-count and G5 worktrees were added, both removed; count restored to 62 |
| Constraint 7 (no full-suite run) | done | only the ordered selection and `integrity check` ran |

## Deviations & assumptions

1. **C4 split into C4a and C4b** (declared above and here, per constraint
   2): the block's single "C4 — THE TESTS AND THE TOOL" commit would have
   totaled 583 insertions (322 test files + 261 mutation tool), over the
   500-insertion cap. Split into C4a (six test files, 322 insertions) and
   C4b (the mutation tool, 261 insertions), each its own subject, per
   constraint 2's own instruction to split such a commit "into parts with
   their own subjects (C3a and C3b, C4a and C4b)". No content differs from
   what a single C4 would have carried; only the commit boundary changed.
2. **THE TESTS section's "monkeypatched onto `packages.orchestration.pingpong_job`"
   reading**: `run_job` imports `run_pingpong` with a LOCAL import inside its
   own body (`from packages.orchestration.pingpong_loop import (... ,
   run_pingpong)`, at the call site) — `pingpong_job` module itself carries
   no module-level `run_pingpong` attribute to monkeypatch (confirmed:
   `grep run_pingpong packages/orchestration/pingpong_job.py` shows only the
   local import and the call, and every existing stand-in pattern already in
   this test file — six of them — monkeypatches
   `packages.orchestration.pingpong_loop.run_pingpong`, the module the local
   import actually reads from at call time). The new E2E test in
   `TestAttemptIdAndRoundEvents` therefore monkeypatches
   `packages.orchestration.pingpong_loop.run_pingpong`, exactly like every
   other stand-in already in this file, rather than a `pingpong_job`
   attribute that does not exist. This reproduces the described BEHAVIOUR
   (a `*args, **kwargs` stand-in that records the given `run_id` and returns
   a carrying `PingPongResult`) via the only mechanism that can actually
   reach `run_job`'s call.
3. **The two round-shape scenarios (`_log_task_rounds`'s no-test-result case,
   and `_repair_result`'s three classifications) are unit tests against the
   private helpers with a minimal recording log/`types.SimpleNamespace`**,
   rather than driven end-to-end through `run_job`. The full E2E ordered
   sequence (started → tested fail → completed needs_repair → repaired
   changed → tested pass → completed pass → completed) IS driven end-to-end
   with a `run_pingpong` stand-in and a real `run_job` call, covering the
   spec's primary scenario; the edge cases (no test ran; no builder output;
   an errored output; a no-file output) are covered directly against the
   functions that decide them, which is more precise than routing three
   extra shapes through the full apply pipeline and exercises the same
   production code.

No gate read red. No existing test was edited. No test this round wrote was
found wrong before C5, so no test correction was needed.

## Next

Phase 1 rule 1: read `.agent/STOP` from disk at the start of the next
session. Then the review of round 1. Then the second half of T001: the
run-next path, the test service, the long-run repair events and the
plan-approved event. Open findings, as `open_finding_ids` would read the
ledger: 0. Operator questions open: 0.
