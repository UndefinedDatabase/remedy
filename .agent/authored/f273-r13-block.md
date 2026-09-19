-- STEP R13 mission surfaces and event coupling -- F273 Findings paydown v1 --
Session 2 of F273 · round 13 · base `b3baf7d5` (the round 12 handoff, branch
`feature/f273-findings-paydown-v1`).

Goal: book round 12's verdict and nine resolutions, register R-0989, land DECISION F273 D13, and
build R-0930, R-0929, R-0904, R-0970, R-0915, R-0919, R-0920, R-0905 and R-0907 exactly as the
reviewer's dry run built them.

Read first, completely: AGENTS.md; the payload `decisions.md` (DECISION F273 D13 — this round's
spec; where this block is terser, it rules).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f273-r13/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  plan.md              sha256 54ca2b388528d9722b12154fb4a8594bcc8cc4cdf87c6ddca8dd6312e390cfe4
  ledger.md            sha256 f0759ac4a18760721bafca0e3eb754e2755df6ff8d7b60460382b18c4e75f9d1
  decisions.md         sha256 aa19154f8ee09dfff6d8a021c5379d1249877e9d38193e077256796e464d1855
  block.md             this block (save it; report its digest)
CODE — diffs research helpers built, which the reviewer applied in this order at `b3baf7d5`, ran
and red-proved in its own worktree. Apply with `git apply`; never edit a hunk:
  `.remedy-wt/f273-proto-g3.diff` sha256 f354aa37b70bb4e94aa3cbf227c29a83462f95b7a715f34b14d7ef95173c5312
  `.remedy-wt/f273-proto-g4.diff` sha256 5c1f5f3bf5c62cf89be0710054981e77eca32748f32953417fcf1ee43906b73d

Bundle (commit order):
C1 bookkeeping — one commit holding exactly: byte copies of every payload above as
   `.agent/authored/f273-r13-<name>`; `.agent/plan.md` := plan.md; `.agent/live_review.md` and
   `.agent/decisions.md` := each one's `b3baf7d5` bytes + ledger.md and decisions.md respectively.
C2 R-0930, R-0929, R-0904, R-0970, R-0915 — `git apply` g3.diff.
C3 R-0919, R-0920, R-0905, R-0907 — `git apply` g4.diff.
   Before each code commit run `git status --porcelain` and stage every path the apply touched,
   deletions included; nothing may be left untracked or unstaged.
C4 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 2 of feature F273 · round 13 · rounds so far 13" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C3; every gate's
   real output; open findings by distinct id (`count_open_findings`) on the committed ledger; one
   `Landed: R-xxxx` line naming its commit for each of R-0930, R-0929, R-0904, R-0970, R-0915,
   R-0919, R-0920, R-0905 and R-0907, in the handoff only — never a `Done:` line of your own;
   `## Next` naming Phase 1 rule 1 then the review of round 13, and "Operator questions open: <the
   count you read from the file>". Then `git push`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test calls a real provider or model. The shell denies `VAR=x cmd`, `cp`, loops, `$( )`,
   `$VAR` (including `$?`) and `cd` before git; use `git -C <path>` and small python scripts under
   `.remedy-wt/f273-r13/` (prefix yours `wk_`) with an explicit `cwd=`. Never use `git stash`.
3. Never weaken an assertion or delete a test other than the changes the diffs carry. A red gate or
   an ambiguity D13 does not settle -> stop, commit nothing half-done, report.
4. Build every edited `.agent/` file from `git show b3baf7d5:<path>` bytes.
5. Commit messages "F273 R13 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never list, read or write any `.data/` yourself. Never run `scripts/remedy_smoke.sh` or
   `scripts/make_review_zip.sh` for real, never run the `remedy` CLI, `run_job` against this
   repository, `npm install` or the self-use runner, and create no branch. Research helpers may
   hold worktrees under `.remedy-wt/f273-h-*`; never touch them.

Done when (G1 to G5 at C3, before C4; report literal output and the real exit code):
G1 transport + state + path sets: every payload and diff digest matched; a python check prints
   True that `.agent/plan.md` equals its payload, that `.agent/live_review.md` and
   `.agent/decisions.md` each equal their `b3baf7d5` bytes + ledger.md and decisions.md, that each
   `.agent/authored/f273-r13-*` copy equals its payload, and that `git show --name-only --format=`
   of C2 and of C3 each lists exactly the paths `git apply --numstat` reads from its diff.
G2 code transport: `git rev-parse <C3>:tests <C3>:packages <C3>:apps <C3>:docs <C3>:scripts` prints
   exactly 2beafcb1ee267504ea8f3e134c5635eda7cca657, 9f0255aa1385c7770163b1590b87847691a50cda,
   0e7f11cb7c7a4f81ad5ace8ffac6a881a16be6cc, dc2df26a7ece692e469ce4b7707a1799b082d6bb and
   9638c2c911dee4ee8993a79a582aa2dc721f738d (the reviewer's dry-run objects).
G3 in the primary checkout, serial (no `-n`): `python3 -m pytest -q -p no:cacheprovider
   tests/cli/test_mission_cmd.py tests/orchestration/test_orchestrator_loop.py tests/test_timeline.py
   tests/test_trust_report.py tests/orchestration/test_job_plan.py tests/cli/test_plan_approval.py
   tests/cli/test_command_catalog.py tests/test_command_catalog.py tests/cli/test_advertised_commands.py
   tests/docs/ tests/orchestration/test_mission_compiler.py tests/orchestration/test_mission_state.py
   tests/orchestration/test_prompt_trace.py tests/orchestration/test_event_name_coupling.py
   tests/orchestration/test_approval_queue.py tests/orchestration/test_autonomy.py
   tests/orchestration/test_decision_evidence.py tests/orchestration/test_decision_inbox.py
   tests/orchestration/test_event_ledger.py tests/orchestration/test_run_contract.py
   tests/orchestration/test_stop_reasons.py tests/storage/test_persistence.py
   tests/test_autonomy_readiness.py tests/test_run_contract.py tests/test_token_policy.py
   tests/cli/test_blocker_cmd.py tests/test_remedy_smoke_script.py tests/test_execution_foundation.py
   tests/ui_server/test_cockpit_contract.py tests/ui_server/test_dashboard_cockpit_truth.py
   tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py
   tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py
   tests/cli/test_golden_path.py` -> summary line, 0 failed, exit 0, no `R-0803:` line.
G4 `python3 -m ruff check . --output-format concise` from the primary checkout's root ->
   "All checks passed!", exit 0.
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C3, run from its root
   with `python3 -B -m pytest -q -p no:cacheprovider` and an env carrying
   `REMEDY_OLLAMA_HOST=http://127.0.0.1:9` and `OLLAMA_HOST=http://127.0.0.1:9` (through the
   script's `env=`), `__pycache__` purged before each run, the imported
   `packages.orchestration.trust_report` path printed first to prove it resolves inside the
   worktree. The UNMUTATED control first over the test files named below (exit 0). Then, each
   reverted from its saved bytes before the next, counting each FROM line (with its newline) in
   the named file first (each must be 1), naming the failing ids. M = tests/cli/test_mission_cmd.py;
   K = tests/orchestration/test_event_name_coupling.py.
   (a) `packages/orchestration/orchestrator_loop.py`:
   `                            recorded_at=_utc_now_iso(now))` -> `                            recorded_at="")`
   -> M fails;
   (b) `apps/cli/commands/mission_cmd.py`: `        print(render_ledger(ledger))` ->
   `        print(render_ledger(ledger[-1:]))` -> M fails;
   (c) the same file: `        mission_job_state_label(link.job_id) in _NOT_STARTED_JOB_STATES` ->
   the same line with `_NOT_STARTED_JOB_STATES` replaced by `(*_NOT_STARTED_JOB_STATES, "completed")`
   -> M fails;
   (d) `packages/orchestration/trust_report.py`: in the one line starting
   `    return [f"      remedy patch approve {job.job_id} ` replace `{i['intent_id']}` by
   `<intent_id>` -> tests/test_trust_report.py fails;
   (e) `apps/cli/commands/job.py`: `            f"  {REJECTED_PLAN_NEXT_STEP}")` -> `            "")`
   -> tests/cli/test_plan_approval.py fails;
   (f) K itself: `            for a in node.args` -> `            for a in node.args[:1]` -> K fails;
   (g) K itself: `            helpers.add(fdef.name)` -> `            pass` -> K fails;
   (h) `packages/orchestration/autonomy_readiness.py`: after the line
   `        _check("agent_loop", f"remedy dev agent-loop {job_id}")` insert the line
   `        _check("run_contract")` -> tests/test_autonomy_readiness.py fails.
   Report exit codes and failing ids, and a mutation that stays green as green. Remove the worktree
   and show `git worktree list`.
G6 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
