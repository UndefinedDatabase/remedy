-- STEP R7 T009+T012 -- F273 Findings paydown v1 --
Session 1 of F273 · round 7 · base `00b995e7` (the round 6 handoff, branch
`feature/f273-findings-paydown-v1`).

Goal: book round 6's verdict and the resolutions rounds 3 to 6 landed, land DECISION F273 D7, and
build R-0568 and the self-use track's repairs exactly as the reviewer's dry run built them.

Read first, completely: AGENTS.md; the payload `decisions.md` (DECISION F273 D7 — this round's
spec; where this block is terser, it rules).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f273-r7/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  plan.md              sha256 abce1fb2fe9dbf96a08f752ef365ed8c21b58bdae7ff47d53d70717ae7806025
  ledger.md            sha256 ff11886183a71f36de1287f728d48db190a0e5cd69c0c7cc62c977a5f53811eb
  decisions.md         sha256 f306f64c476bc5a2d8451d5a593df4c8389c7104dd493bf779f84de9d4648984
  block.md             this block (save it; report its digest)
CODE — two diffs research helpers built at `00b995e7`, which the reviewer applied, ran and
red-proved in its own worktree. Apply with `git apply`; never retype or edit a hunk:
  `.remedy-wt/f273-proto-r0568.diff` sha256 0872e6170458f15fc975e28b64a5b18a953209ffb07b6b09a52013755070d9cb
  `.remedy-wt/f273-proto-t012.diff` sha256 01175335b3bc51c5fec9e5daa7a7be823b1be3bdd5ae1a44949c92cfd4e4d38d

Bundle (commit order):
C1 bookkeeping — one commit holding exactly: byte copies of every payload above as
   `.agent/authored/f273-r7-<name>`; `.agent/plan.md` := plan.md; `.agent/live_review.md` and
   `.agent/decisions.md` := each one's `00b995e7` bytes + ledger.md and decisions.md respectively.
C2 R-0568 — `git apply .remedy-wt/f273-proto-r0568.diff`.
C3 R-0784, R-0785, R-0786, R-0838, R-0972 — `git apply .remedy-wt/f273-proto-t012.diff`.
   Before each code commit run `git status --porcelain` and stage every path the apply touched;
   nothing may be left untracked or unstaged.
C4 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 1 of feature F273 · round 7 · rounds so far 7" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C3; every gate's
   real output; open findings by distinct id (`count_open_findings`) on the committed ledger; one
   `Landed: R-xxxx` line naming its commit for each of R-0568, R-0784, R-0785, R-0786, R-0838 and
   R-0972, in the handoff only — never a `Done:` line of your own; `## Next` naming Phase 1 rule 1
   then the review of round 7, and "Operator questions open: <the count you read from the file>".
   Then `git push`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test calls a real provider. The shell denies `VAR=x cmd`, `cp`, compound commands and `cd`
   before git; use `git -C <path>` and small python scripts under `.remedy-wt/f273-r7/` (prefix
   yours `wk_`) with an explicit `cwd=`. Never use `git stash`: its stack is shared.
3. Never weaken an assertion or delete a test other than the changes the diffs carry. A red gate or
   an ambiguity D7 does not settle -> stop, commit nothing half-done, report.
4. Build every edited `.agent/` file from `git show 00b995e7:<path>` bytes.
5. Commit messages "F273 R7 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never list, read or write any `.data/` yourself. Never run `scripts/make_review_zip.sh` for real,
   and never run the self-use runner.
7. A reviewer's disposable worktree `.remedy-wt/f273-r7-dry` exists: never run anything in it.

Done when (G1 to G5 at C3, before C4; report literal output and the real exit code):
G1 transport + state + path sets: every payload and diff digest matched; a python check prints
   True that `.agent/plan.md` equals its payload, that `.agent/live_review.md` and
   `.agent/decisions.md` each equal their `00b995e7` bytes + ledger.md and decisions.md, that each
   `.agent/authored/f273-r7-*` copy equals its payload, and that `git show --name-only --format=`
   of C2 and of C3 lists exactly the paths `git apply --numstat` reads from its diff.
G2 code transport: `git rev-parse <C3>:tests <C3>:packages <C3>:scripts <C3>:docs` prints exactly
   f93cf09ef075d7c30bc7efbe56f14eed55194221, a7de87d1c4ce4abf3ce2a07838fec2508c37df73,
   b3754f08c41d508ebcdf0d2bedb15073e9a2dbb6 and 02a05b9351d90dff4a68a0468b421365d39d6ae5 (the
   reviewer's dry-run subtrees).
G3 in the primary checkout, serial (no `-n`): `python3 -m pytest -q -p no:cacheprovider
   tests/orchestration/test_applicator_fences.py tests/orchestration/test_budget_stop_integration.py
   tests/orchestration/test_builder_bridge.py tests/orchestration/test_ci_run.py
   tests/orchestration/test_development_artifact_boundary.py tests/orchestration/test_exec_guard.py
   tests/orchestration/test_failure_postmortem.py tests/orchestration/test_failure_wiring.py
   tests/orchestration/test_gauntlet_evaluator.py tests/orchestration/test_import_reachability.py
   tests/orchestration/test_integrity_gate.py tests/orchestration/test_job_apply.py
   tests/orchestration/test_mission_state.py tests/orchestration/test_pingpong.py
   tests/orchestration/test_self_healing_cycles.py tests/orchestration/test_self_use_findings.py
   tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_job.py
   tests/orchestration/test_self_use_queue.py tests/orchestration/test_self_use_runner.py
   tests/orchestration/test_test_runner.py tests/orchestration/test_worktree_cleanup_paths.py
   tests/test_command_discovery.py tests/test_no_orphan_modules.py tests/test_test_runner.py
   tests/orchestration/test_pingpong_cli.py tests/orchestration/test_job_evidence.py tests/docs/
   tests/orchestration/test_roadmap_index.py tests/cli/test_golden_path.py` -> summary line,
   0 failed, exit 0, no `R-0803:` line.
G4 `python3 -m ruff check . --output-format concise` from the primary checkout's root ->
   "All checks passed!", exit 0.
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C3, run from its root
   with `python3 -B -m pytest -q -p no:cacheprovider`, `__pycache__` purged before each run, the
   imported `packages.orchestration.failure_postmortem` path printed first to prove it resolves
   inside the worktree. The UNMUTATED control first over the test files named below (exit 0). Then,
   each reverted before the next, counting the mutated bytes in the named file first (each must be
   1), naming the failing ids:
   (a) `packages/orchestration/failure_postmortem.py`: the six lines from
   `    tripped = (signals.tripped_limit or "").strip()` through
   `        return Classification(FailureClass.RESOURCE_LIMIT, SIGNAL_GUARD_TRIP, reason)` deleted ->
   `tests/orchestration/test_failure_postmortem.py` fails;
   (b) `packages/orchestration/pingpong_job.py`: the line
   `                task.tripped_limit = last_round.test_tripped_limit` deleted ->
   `tests/orchestration/test_failure_wiring.py` fails;
   (c) `packages/orchestration/self_use_generator.py`: `, ensure_ascii=False` removed from the one
   `json.dumps(body, indent=2, ensure_ascii=False)` -> `tests/orchestration/test_self_use_generator.py`
   fails;
   (d) the same file: `        if r_id in done_ids or r_id in exclude:` ->
   `        if r_id in done_ids:` -> `tests/orchestration/test_self_use_generator.py` fails;
   (e) `packages/orchestration/self_use_findings.py`: `    if result.state == JOB_STOPPED:` ->
   `    if False:` -> `tests/orchestration/test_self_use_findings.py` fails;
   (f) `scripts/self_use_queue.json` replaced by its `00b995e7` bytes ->
   `tests/orchestration/test_self_use_queue.py` fails.
   Report exit codes and failing ids, and a mutation that stays green as green. Remove the worktree
   and show `git worktree list`.
G6 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
