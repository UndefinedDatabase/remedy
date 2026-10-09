# Handoff — F253 round 30: book round 29, run the closure's self-use item to its approval gate

## Session

SESSION 6 of feature F253 · round 30 · rounds so far 30

Context self-assessment: the reviewer's context holds; the session continues with the closure sequence.

Fortschritt: ~98 % (building, the hardening stage and the closure's self-use run done · the one full suite, the consolidation pass, the evidence, the package and the closing commit remain) — Schätzung

## Range

Review of `86af8f740eaf7754a7d74245faf12296f12f069f`..`e2d06cdc1` (the last commit before this handback, C3).

## Commits

### 0baf38c7e F253 R30 C1: book round 29, resolve R-1221, the plan, save the block and the self-use script

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f253-r30-selfuse.py` | 122/0 | new file, byte copy of `selfuse.py` |
| `.agent/authored/f253-r30.md` | 134/0 | new file, byte copy of `block.md` (134 lines, sha256 `8270bc04e8cf915047f29cf9ef352ad2bd907de36cadc2022513854eff46cb97`) |
| `.agent/live_review.md` | 4/0 | `append-live_review.txt` appended: round 29's gate entry (PASS) and R-1221's Done line |
| `.agent/plan.md` | 9/10 | `dry-plan.md`, byte for byte |

### e2d06cdc1 F253 R30 C2: the closure's self-use item run to its approval gate, never applied

| Path | +/- | Reason |
|---|---|---|
| `.agent/selfuse_f253/SU-050.md` | 13/0 | the item's job file |
| `.agent/selfuse_f253/changed_paths.txt` | 2/0 | the paths the job changed |
| `.agent/selfuse_f253/entry_and_job_file.txt` | 5/0 | the queue entry and job file path |
| `.agent/selfuse_f253/execution_config.txt` | 39/0 | the job's execution configuration |
| `.agent/selfuse_f253/full_transcript.txt` | 14/0 | the job summary |
| `.agent/selfuse_f253/job_diff.txt` | 42/0 | the job branch's diff over the start commit |
| `.agent/selfuse_f253/result_state.txt` | 12/0 | job state, budgets, task states |
| `.agent/selfuse_f253/run_defects.txt` | 1/0 | `describe_self_use_run_defects` output |
| `.agent/selfuse_f253/staleness_after.txt` | 2/0 | staleness catalog over the job branch |
| `.agent/selfuse_f253/timing.txt` | 3/0 | start, finish, wall seconds |
| `scripts/self_use_queue.json` | 8/0 | the generator's one appended entry, SU-050, `consumed_by` empty |

### This commit (self-reference)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file |

## External actions

- `python3 .remedy-wt/f253-r30/launch_selfuse.py` once, then `wait_selfuse.py` once (it printed `exit 0`): the self-use run, real provider spend, see Self-use run.
- The script added and removed one temporary worktree itself (`.remedy-wt/f253-r30-jobtree`) and left the job's branch `remedy/job-ad0292aa498b4ce7` and its workspace `.remedy-wt/job-ad0292aa498b4ce7`.
- `git push origin feature/f253-public-http-api`: reported in the worker's reply, not here.
- No pull request, no full suite, no mutation, no worktree of my own, no merge, no force-push, no pull.

## Verification

0. Preconditions: `block.md` and the seven other prepared files matched their sha256 (`block.md` 134 lines); HEAD and origin both `86af8f740eaf7754a7d74245faf12296f12f069f`; `git status --porcelain` empty; `.agent/STOP` absent; branch `feature/f253-public-http-api`.
1. **Gate 1**: `git status --porcelain` empty after C2. Byte proofs against `0baf38c7e`, all True: block copy, self-use script copy, plan, and `.agent/live_review.md` equals its blob at `86af8f740` plus `append-live_review.txt`.
2. **Gate 2**: the ten files under `.agent/selfuse_f253/`, all non-empty. Bytes: `SU-050.md` 943, `entry_and_job_file.txt` 391, `execution_config.txt` 1203, `result_state.txt` 810, `timing.txt` 105, `changed_paths.txt` 54, `full_transcript.txt` 1416, `staleness_after.txt` 59, `job_diff.txt` 2014, `run_defects.txt` 5.
3. **Gate 3: RED**, run once and not re-run. `python3 .remedy-wt/f253-r30/run_selection.py /home/decodeux/Repos/remedy`, exit 1:

```
exit 1
FAILED tests/test_parametrize_ids_stable.py::test_no_parametrize_argument_draws_a_fresh_value_at_collection
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
1 failed, 3758 passed, 3 skipped in 121.93s (0:02:01)
```

   No ERROR line and no `process(es) behind` line. The failing test asserts `fresh_value_parametrize_sites(TESTS) == []` over `tests/`; I did not run it again, so the offending site is not read.
4. **Gate 4**: not run, because gate 3 was red and the block orders a stop at a red gate.
5. Gate 5 (after the push): reported in the worker's reply, not here.

## Authored-text proofs

- `block.md` to `.agent/authored/f253-r30.md`: 134 lines, byte-equal, sha256 `8270bc04e8cf915047f29cf9ef352ad2bd907de36cadc2022513854eff46cb97`.
- `selfuse.py` to `.agent/authored/f253-r30-selfuse.py`: byte-equal (`git show 0baf38c7e:<path>` against the prepared file).
- `append-live_review.txt`: "post equals pre plus slice" True against the blob at `86af8f740`.
- `dry-plan.md` to `.agent/plan.md`: byte-equal.

## Self-use run

Script exit code 0, run once. Its console output was saved as the ten files under `.agent/selfuse_f253/`.

- Entry id: SU-050. Title: Narrow the excused handler at apps/cli/commands/job.py:867. Provenance: generated (self-use-generator tier 4, excused handler). The generator supplied it (`generate_and_append_if_empty()` returned it).
- Job id: `ad0292aa498b4ce7`.
- Builder: provider `claude-cli`, model `claude-sonnet-4-6`, effort medium. Reviewer: provider `claude-cli`, model `claude-sonnet-4-6`, effort medium (`execution_config.txt`).
- Job state: `completed`. Stop reason: empty. Stop source: empty. Error: empty.
- Task T001: status `applied_to_job_workspace`, reviewer verdict `pass`, final status `staged_review_passed`, repair rounds used 0.
- Budgets: `max_cost_usd` 6.0, `max_provider_calls` 8. Actuals: 2 provider calls, 16334 tokens, measured cost 0.9586805999999999 USD.
- Wall seconds (`timing.txt`): 251.6.
- `changed_paths.txt`: `apps/cli/commands/job.py`, `tests/test_ble001_ratchet.py`.
- `staleness_after.txt`: read from the job branch `remedy/job-ad0292aa498b4ce7`; `NONE`.

`job_diff.txt` verbatim:

```
$ git diff HEAD...remedy/job-ad0292aa498b4ce7  (exit 0)
diff --git a/apps/cli/commands/job.py b/apps/cli/commands/job.py
index 9db1b6ad8..9ae22f22b 100644
--- a/apps/cli/commands/job.py
+++ b/apps/cli/commands/job.py
@@ -843,6 +843,14 @@ def _cmd_plan_job_local(job_id_str: str, *, json_output: bool = False) -> None:
             except OSError:
                 pass
 
+    try:
+        import ollama as _ollama_mod
+        _plan_error_types: tuple[type[BaseException], ...] = (
+            OSError, RuntimeError, ValueError,
+            _ollama_mod.RequestError, _ollama_mod.ResponseError,
+        )
+    except ImportError:
+        _plan_error_types = (OSError, RuntimeError, ValueError)
     start = time.monotonic()
     try:
         result: PlanJobResult = plan_job_with_llm(
@@ -864,7 +872,7 @@ def _cmd_plan_job_local(job_id_str: str, *, json_output: bool = False) -> None:
         log.log("planning_failed", provider="ollama", role="planner", model=planner.model,
                 outcome="error", message="planning failed", error_category=type(exc).__name__)
         fail("missing_dependency", str(exc), json_output=json_output)
-    except Exception as exc:  # noqa: BLE001 — any planner failure is reported, never crashes the CLI
+    except _plan_error_types as exc:
         _persist_plan_traces()
         log.log("planning_failed", provider="ollama", role="planner", model=planner.model,
                 outcome="error", message="planning failed", error_category=type(exc).__name__)
diff --git a/tests/test_ble001_ratchet.py b/tests/test_ble001_ratchet.py
index ff1f68ae3..cb21e641a 100644
--- a/tests/test_ble001_ratchet.py
+++ b/tests/test_ble001_ratchet.py
@@ -18,7 +18,7 @@ REASONED = re.compile(r"^ — \S")
 
 #: The number of excused blind handlers when BLE001 was turned on. Only ever falls: the
 #: commit that removes a mark lowers this number in the same commit, and it is never raised.
-MAX_EXCUSED = 285
+MAX_EXCUSED = 284
 
 
 def _marks() -> list[tuple[str, int, str]]:
```

`run_defects.txt` verbatim:

```
NONE
```

## Deviations & assumptions

- Gate 3 was red (one FAILED line, above). Per the block it was not re-run, gate 4 was not run, and the handback was written and pushed. I did not read which parametrize site the failing test names.
- `.agent/plan.md` was not updated with the blocker: the block names it a C1 path only, and the block forbids files outside the named paths. The plan still reads as C1 wrote it.

## Round verdicts

Round 29 PASS, with R-1221 resolved, is booked by C1. Round 30's verdict is the reviewer's, to be booked in the next round's first commit.

## For the operator, in plain sentences

Before a feature closes, Remedy runs one real piece of work on itself with a paid model, to show it is used on itself. This time the work was to narrow one place in its own command-line code that catches every kind of error. The run stops before anything is applied; its record is saved for the next round to read. The run cost about 96 cents (0.9587 US dollars, two provider calls). It ended cleanly: the job finished, its reviewer passed the one task, and nothing was applied. One test in the wider check I ran afterwards failed, so the reviewer will look at that first. Nothing waits for you.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and stop.
2. Phase 1 rule 2 (Open PR Gate): no pull request is open for this branch yet.
3. The reviewer reviews round 30, books its verdict and registers every self-use run defect in the next round's first commit; gate 3's failed test `tests/test_parametrize_ids_stable.py::test_no_parametrize_argument_draws_a_fresh_value_at_collection` is the first thing to read.
4. The integration-gate round: the one full suite.
5. The consolidation pass, the evidence bundle, the review package, the rotation, the STATUS line and the pull request.

Operator questions open: 4.
Open findings: 14 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196, R-1219 and R-1220, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 29, resolve R-1221, the plan, save the block and the self-use script | done | `0baf38c7e` |
| C2: the closure's self-use item run to its approval gate, never applied | done | `e2d06cdc1`, SU-050, job `ad0292aa498b4ce7`, verdict pass |
| Gate 1 | done | green |
| Gate 2 | done | ten files non-empty |
| Gate 3 | deviated | red: 1 failed, 3758 passed, 3 skipped; not re-run |
| Gate 4 | skipped | not run after the red gate 3, as the block orders |
| C3: this handback | done | this commit |
| Push, Gate 5 | pending | reported in the worker's reply |
