── STEP R10/n — F280 ────────────────────────────────────────
Goal: book round 9's independently-reviewed PASS (Gate: F280 R9, no new finding), and land the
first half of DECISION F280 D5's own CONSEQUENCE paragraph: the module rename
`flight_plan.py` -> `job_plan.py`, `FlightPlanResult` -> `TaskPlanResult`, and D5's eight named
lowercase function names take the `task_plan` spelling, across every importer and every stale
comment reference. This round does NOT touch any persisted literal, any English-prose noun, or
`FLIGHT_PLAN_SCHEMA_V`/`_MAX_FLIGHT_PLAN_TASKS` (both live in `schemas/models.py`, not in the
renamed module, and the schema-tag constant's VALUE is a persisted literal owed to the next
round together with its sibling literals).

Bundle:
  1. Copy this block to `.agent/authored/f280-r10.md` and mirror to `.agent/last_block.md`.
  2. Append the Gate:F280 R9 entry to `.agent/live_review.md` (no new finding this round), and
     replace `.agent/plan.md` with the new full content — both pre-built and pre-verified by
     the reviewer in disposable worktrees.
  3. Apply the pre-built rename patch.
  4. Run the done-when gates, run the canary, write the handoff, commit, push.

Change — exact files, exact source:
  All three source files below live under `/home/decodeux/Repos/remedy/.remedy-wt/` (repo-root
  scratch, NOT a git ref — plain files on disk in the primary checkout's own working tree).
  Copy each BYTE-FOR-BYTE with `shutil.copyfile` or equivalent; do not retype.

  (a) `.agent/live_review.md` — append, IN THIS ORDER, to the end of the current file (which
      currently ends in exactly one `\n`):
        1. one `\n` byte (blank-line paragraph separator)
        2. the exact bytes of `.remedy-wt/gate_r9_entry.txt` (sha256
           `b1f2bd955cee469fb120c8c19a5ec6e76e37cd29d20802291a01fc51b0cdfb73`, 3303 bytes,
           already ends in its own single `\n`)
      i.e. `new_bytes = old_bytes + b"\n" + gate_r9_entry`. There is no finding to register this
      round — round 9 found no new defect, so there is no `- R-xxxx` block to append.
  (b) `.agent/plan.md` — REPLACE THE WHOLE FILE with the exact bytes of
      `.remedy-wt/f280-r10-plan.md` (sha256
      `6d9dcd9b070e10d27d6fb9a0b85bda45914a4339c0a60fa269187d13f6645e5a`, 2406 bytes, 42 lines).
      This is a rewrite per AGENTS.md `.agent/plan.md` convention, not an append.
  (c) Apply `.remedy-wt/f280-r10-rename.patch` (sha256
      `d8eced2122046bf439b774883b1c6cd7a3e8e2dbcd282830a6935411e349a267`, 62143 bytes, 1142
      lines) with `git apply --check` then `git apply` from the repo root, then `git add -A`
      (the patch is a plain `git apply`-style diff, not `git am` — it does NOT stage the file
      renames itself; `git add -A` after applying is what turns the delete+create pairs for
      `packages/orchestration/flight_plan.py`/`job_plan.py`,
      `tests/orchestration/test_flight_plan.py`/`test_job_plan.py` and
      `tests/schemas/test_flight_plan_schema.py`/`test_job_plan_schema.py` into the renames
      `git status` and the commit will show). This patch has been APPLIED and RUN by the
      reviewer, twice, in two independent from-scratch disposable worktrees at this round's own
      base commit `bf1b8fc5` (not merely checked) — every numeral in this block's Done-when
      section below is read off those two applied, executed runs, not predicted.

Constraints:
  - Do not touch any file this block's patch does not name.
  - No persisted literal changes: `job.flight_plan` (the attribute/dict key on a job record),
    the schema tag string `"flight_plan_v1"`, the decision type string `"flight_plan_approval"`,
    `FLIGHT_PLAN_SCHEMA_V` and `_MAX_FLIGHT_PLAN_TASKS` (both in
    `packages/orchestration/schemas/models.py`) are UNCHANGED by this patch — if your own read
    of the patch shows any of these touched, STOP and treat it as a block condition, do not
    apply it.
  - No English-prose noun changes: a sentence describing the concept "flight plan" in running
    text, a CLI print statement ("Flight plan approved..."), or a catalog description stays
    exactly as it reads today — only Python identifiers, the module path, and comments/
    docstrings that literally NAME one of the renamed identifiers as a code pointer move.
  - Commit order: C0a (authored carrier) -> C0b (last_block mirror) -> C1 (the two `.agent/`
    fixes, ONE commit) -> C2 (the patch application, ONE commit) -> C3 (handoff). Do not split
    C1 or C2 further; C2 is 145 insertions, far under the 500-line insertion cap.
  - `git status --porcelain` empty before your first commit and after your last.
  - Any disposable worktree you create for verification (including the mutation red-proof
    below) goes under `.remedy-wt/`, inside this checkout — NOT `/tmp` — and you remove it
    yourself as the LAST action of the step that created it, verified by `git worktree list`
    showing only the primary checkout before your handback commit.

Done when (run every command from the repo root, primary checkout):
  G1 TRANSPORT — one digest comparison: `sha256sum .agent/authored/f280-r10.md` equals
     `sha256sum .agent/last_block.md`, and `cmp` each of the three source files under
     `.remedy-wt/` against the corresponding section it produced in the committed target —
     report PASS/FAIL, not a re-typed diff.
  G2 THE RECORD — after C1, over `.agent/live_review.md`:
     `python3 -c "import re; d=open('.agent/live_review.md').read(); print(len(re.findall(r'^Gate: F\d+ R\d+ — ', d, re.M)), len(set(re.findall(r'^- (R-\d{4}) — ', d, re.M))), len(set(re.findall(r'^Done: (R-\d{4}) — ', d, re.M))))"`
     must read exactly `36 136 7` (unchanged open/done counts — this round registers no
     finding). `.agent/plan.md` must be exactly 42 lines with exactly one `## Goal`, one
     `## Current Step`, one `## Next Steps` and one `## Risks`.
  G3 THE PATCH — after C2, `git diff --numstat 49a43950..HEAD -- apps/ packages/ tests/ docs/`
     reads exactly these 28 paths (old/new name where renamed):
       apps/cli/commands/decision.py 4/4
       apps/cli/commands/do_cmd.py 10/10
       apps/cli/commands/job.py 11/11
       apps/cli/commands/job_context_cmd.py 3/3
       docs/system/vocabulary.md 4/4
       packages/orchestration/dag_schedule.py 1/1
       packages/orchestration/decision_inbox.py 1/1
       packages/orchestration/decision_queue.py 1/1
       packages/orchestration/dod_compiler.py 1/1
       packages/orchestration/flight_plan.py => packages/orchestration/job_plan.py 15/15
       packages/orchestration/mission_compiler.py 2/2
       packages/orchestration/orchestrator_loop.py 7/7
       packages/orchestration/ui_server.py 6/6
       tests/cli/test_decision_answers.py 5/5
       tests/cli/test_golden_path.py 6/6
       tests/cli/test_plan_approval.py 23/23
       tests/orchestration/import_reachability_allowlist.txt 1/1
       tests/orchestration/test_bundled_clarification.py 1/1
       tests/orchestration/test_escalation.py 1/1
       tests/orchestration/test_flight_plan.py => tests/orchestration/test_job_plan.py 20/20
       tests/orchestration/test_long_run_executor.py 1/1
       tests/orchestration/test_mission_compiler.py 2/2
       tests/orchestration/test_plan_prompt_golden.py 3/3
       tests/orchestration/test_prompt_cache_prefix.py 2/2
       tests/orchestration/test_prompt_trace.py 8/8
       tests/schemas/test_flight_plan_schema.py => tests/schemas/test_job_plan_schema.py 0/0
       tests/ui_server/test_command_channel.py 4/4
       tests/ui_server/test_command_dispatch.py 2/2
     — 28 files, 145 insertions(+), 145 deletions(-) total.
  G4 THE BOUNDARY — after C2:
     (a) `grep -rln -E "\bFlightPlanResult\b|\bmap_flight_plan_to_tasks\b|\bflight_plan_blocks_execution\b|\bresolve_flight_plan_approval\b|\bauto_approve_flight_plan\b|\bcompose_flight_plan_prompt\b|\bmake_flight_plan_call_recorder\b|\bflight_plan_approval_open\b" apps/ packages/ tests/ scripts/ docs/system/ docs/guides/`
     reads EMPTY (zero files) — every renamed identifier is gone from the swept corpus.
     (b) `grep -rn '"flight_plan_approval"' apps/ packages/ tests/ scripts/ | wc -l` reads `35`
     (unchanged from base — the persisted decision-type literal). `grep -rn "flight_plan_v1"
     apps/ packages/ tests/ scripts/ | wc -l` reads `36` (unchanged). `grep -rn
     "FLIGHT_PLAN_SCHEMA_V\|_MAX_FLIGHT_PLAN_TASKS" apps/ packages/ tests/ scripts/ | wc -l`
     reads `14` (unchanged). Any of these three numbers moving is a block condition — it means
     a persisted literal was touched — stop and report rather than proceeding.
  G5 TARGETED TESTS — after C2:
     `python3 -m pytest tests/orchestration/test_job_plan.py tests/schemas/test_job_plan_schema.py tests/cli/test_plan_approval.py tests/orchestration/test_bundled_clarification.py tests/orchestration/test_escalation.py tests/orchestration/test_mission_compiler.py tests/orchestration/test_plan_prompt_golden.py tests/orchestration/test_prompt_cache_prefix.py tests/orchestration/test_prompt_trace.py tests/orchestration/test_long_run_executor.py tests/ui_server/test_command_channel.py tests/ui_server/test_command_dispatch.py tests/cli/test_decision_answers.py tests/cli/test_golden_path.py tests/cli/test_job_context_cmd.py tests/docs/ -q`
     reads exactly `958 passed`, read by the reviewer off this exact command line, applied and
     executed (not predicted) in a disposable worktree at this round's own base commit
     `bf1b8fc5`.
  G6 FULL SUITE — after C2, in the PRIMARY checkout (never a worktree — this repo's UI
     dependencies are only installed there): `python3 -m pytest -q`. Expect ONLY the
     pre-existing, unrelated `tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`
     to be at risk of failing in an environment missing `node_modules`; in the primary checkout
     it has been observed to pass. Any OTHER failing node id is this round's, not pre-existing —
     treat it as a block condition.
  G7 RUFF — after C2:
     `python3 -m ruff check apps/cli/commands/decision.py apps/cli/commands/do_cmd.py apps/cli/commands/job.py apps/cli/commands/job_context_cmd.py packages/orchestration/dag_schedule.py packages/orchestration/decision_inbox.py packages/orchestration/decision_queue.py packages/orchestration/dod_compiler.py packages/orchestration/job_plan.py packages/orchestration/mission_compiler.py packages/orchestration/orchestrator_loop.py packages/orchestration/ui_server.py tests/cli/test_decision_answers.py tests/cli/test_golden_path.py tests/cli/test_plan_approval.py tests/orchestration/test_bundled_clarification.py tests/orchestration/test_escalation.py tests/orchestration/test_job_plan.py tests/orchestration/test_long_run_executor.py tests/orchestration/test_mission_compiler.py tests/orchestration/test_plan_prompt_golden.py tests/orchestration/test_prompt_cache_prefix.py tests/orchestration/test_prompt_trace.py tests/schemas/test_job_plan_schema.py tests/ui_server/test_command_channel.py tests/ui_server/test_command_dispatch.py`
     reads exactly ONE error — `UP035` in `packages/orchestration/dag_schedule.py:36` (an
     existing `typing.Iterable/Mapping/Sequence` import this round's one-line comment edit does
     not touch; it is part of DECISION F083 D5's ratcheted baseline, pre-existing at this
     round's own base commit `bf1b8fc5` — confirm this yourself with
     `python3 -m ruff check packages/orchestration/dag_schedule.py` BEFORE applying the patch,
     so you have your own base reading). Every OTHER file must read clean; a new error on any
     file besides `dag_schedule.py`, or a second error on `dag_schedule.py`, is this round's.
  G8 MUTATION RED-PROOF (reachability, `task_plan_blocks_execution`) — in a DISPOSABLE git
     worktree under `.remedy-wt/` only, at your own C2 commit: in
     `packages/orchestration/job_plan.py::task_plan_blocks_execution`, change
     `return approval` (the line inside `if approval in ("pending", "rejected"):`) to
     `return None`, then run
     `python3 -m pytest tests/orchestration/test_job_plan.py tests/cli/test_plan_approval.py -q`.
     Expect exactly 4 of the 57 nodes red:
     `TestApprovalGateEnforcement::test_run_refused_while_pending`,
     `TestApprovalGateEnforcement::test_run_refused_while_rejected`,
     `TestApprovalGateEnforcement::test_rejected_cli_exit_3`,
     `TestApprovalGoldenPathCLI::test_full_approval_sequence` (all four in
     `tests/cli/test_plan_approval.py`), with the other 53 green. Revert your mutation, re-run
     the same command, report the second (green, `57 passed`) result. Remove the disposable
     worktree yourself before your handback commit and confirm with `git worktree list`.

Handback: completion report (state block, deviations, next steps) + rewrite
`.agent/handoff.md`. Attribute commits `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`.
Session number: this is SESSION 5 of F280, round 10.
──────────────────────────────────────────────────────────────
