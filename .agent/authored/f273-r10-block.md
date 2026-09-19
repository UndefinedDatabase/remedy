-- STEP R10 T007+T006 -- F273 Findings paydown v1 --
Session 2 of F273 · round 10 · base `6871f1cd` (the round 9 handoff, branch
`feature/f273-findings-paydown-v1`).

Goal: book round 9's verdict and three resolutions, land DECISION F273 D10, and build R-0762 and
T006's R-0661 and R-0755 exactly as the reviewer's dry run built them.

Read first, completely: AGENTS.md; the payload `decisions.md` (DECISION F273 D10 — this round's
spec; where this block is terser, it rules).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f273-r10/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  plan.md              sha256 2121dfd90ad0b356f4d2c2a5433cb3f5baf9dc9d33d4db0a815ed5a3144d86fc
  ledger.md            sha256 eadb310b9e474a7a45fa39cfb7548085232d2b29003908944e8bd35ac57e12aa
  decisions.md         sha256 f13bb22eae2f1facf3b05d2c2d15ac8b6dd8cac3ec3e36bc291c838e846dd4e4
  block.md             this block (save it; report its digest)
CODE — diffs research helpers built, which the reviewer applied in this order at `6871f1cd`, ran
and red-proved in its own worktree. Apply with `git apply`; never edit a hunk:
  `.remedy-wt/f273-proto-r0762.diff` sha256 581a43d351d884eecaa1ea3ae64df803d0d15a84bdba7b6449bb2668eaaa7bf4
  `.remedy-wt/f273-proto-t006.diff`  sha256 78abae17e7168dd81810bc48209abed4901a1fe0985a8c107d51c99cad189c68

Bundle (commit order):
C1 bookkeeping — one commit holding exactly: byte copies of every payload above as
   `.agent/authored/f273-r10-<name>`; `.agent/plan.md` := plan.md; `.agent/live_review.md` and
   `.agent/decisions.md` := each one's `6871f1cd` bytes + ledger.md and decisions.md respectively.
C2 R-0762 — `git apply` r0762.diff.
C3 R-0661, R-0755 — `git apply` t006.diff.
   Before each code commit run `git status --porcelain` and stage every path the apply touched
   (new files included); nothing may be left untracked or unstaged.
C4 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 2 of feature F273 · round 10 · rounds so far 10" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C3; every gate's
   real output; open findings by distinct id (`count_open_findings`) on the committed ledger; one
   `Landed: R-xxxx` line naming its commit for each of R-0762, R-0661 and R-0755, in the handoff
   only — never a `Done:` line of your own; a line stating that R-0622 is carried per DECISION
   F273 D10 (4); `## Next` naming Phase 1 rule 1 then the review of round 10, and "Operator
   questions open: <the count you read from the file>". Then `git push`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test calls a real provider. The shell denies `VAR=x cmd`, `cp`, loops, `$( )`, `$VAR` and
   `cd` before git; use `git -C <path>` and small python scripts under `.remedy-wt/f273-r10/`
   (prefix yours `wk_`) with an explicit `cwd=`. Never use `git stash`: its stack is shared.
3. Never weaken an assertion or delete a test other than the changes the diffs carry. A red gate or
   an ambiguity D10 does not settle -> stop, commit nothing half-done, report.
4. Build every edited `.agent/` file from `git show 6871f1cd:<path>` bytes.
5. Commit messages "F273 R10 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never list, read or write any `.data/` yourself. Never run `scripts/make_review_zip.sh` for real,
   never run the `remedy` CLI, the orchestrator loop against a real mission, `run_job`, `npm
   install` or the self-use runner, and create no branch. Research helpers may hold worktrees under
   `.remedy-wt/f273-h-*`; never touch them.

Done when (G1 to G5 at C3, before C4; report literal output and the real exit code):
G1 transport + state + path sets: every payload and diff digest matched; a python check prints
   True that `.agent/plan.md` equals its payload, that `.agent/live_review.md` and
   `.agent/decisions.md` each equal their `6871f1cd` bytes + ledger.md and decisions.md, that each
   `.agent/authored/f273-r10-*` copy equals its payload, and that `git show --name-only --format=`
   of C2 and of C3 each lists exactly the paths `git apply --numstat` reads from its diff.
G2 code transport: `git rev-parse <C3>:tests <C3>:packages <C3>:docs <C3>:apps` prints exactly
   296f59a949538214b6dee1f79c498352adfb5060, 0f9bb487445c4481fd6508545e7e45b502b9d573,
   f03cba02ffa51d99ebdc33a569c64d2f9682e7f8 and a2a14cc74fa5d096918d96dbbbd59fa1a46f2c79 (the
   reviewer's dry-run objects).
G3 in the primary checkout, serial (no `-n`): `python3 -m pytest -q -p no:cacheprovider
   tests/orchestration/test_checkpoints.py tests/orchestration/test_decision_evidence.py
   tests/orchestration/test_escalation.py tests/orchestration/test_handoff.py
   tests/orchestration/test_job_worktree_handoff.py tests/orchestration/test_long_run_executor.py
   tests/orchestration/test_mission_contract.py tests/orchestration/test_mission_dossier.py
   tests/orchestration/test_mission_e2e.py tests/orchestration/test_mission_gate.py
   tests/orchestration/test_orchestrator_loop.py tests/orchestration/test_orchestrator_prompt_golden.py
   tests/orchestration/test_prompt_cache_prefix.py tests/orchestration/test_resume_cli.py
   tests/orchestration/test_resume_kill.py tests/orchestration/test_watchdog.py
   tests/orchestration/test_worktree_resume_cli.py tests/orchestration/test_era_integrity.py
   tests/orchestration/test_import_reachability.py tests/orchestration/test_test_runner.py
   tests/cli/test_mission_cmd.py tests/test_agent_loop.py tests/test_cockpit.py tests/test_timeline.py
   tests/test_trust_report.py tests/ui_contracts/ tests/docs/ tests/ui_server/test_dashboard_contract.py
   tests/cli/test_golden_path.py` -> summary line, 0 failed, exit 0, no `R-0803:` line.
G4 `python3 -m ruff check . --output-format concise` from the primary checkout's root ->
   "All checks passed!", exit 0.
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C3, run from its root
   with `python3 -B -m pytest -q -p no:cacheprovider`, `__pycache__` purged before each run, the
   imported `packages.orchestration.orchestrator_loop` path printed first to prove it resolves
   inside the worktree. The UNMUTATED control first over the test files named below (exit 0).
   Then, each reverted from its saved bytes before the next, counting each FROM (with its
   newlines) in the named file first (each must be 1), naming the failing ids. R =
   tests/orchestration/test_orchestrator_loop.py and tests/orchestration/test_resume_cli.py; U =
   tests/ui_contracts/test_design_drift.py and tests/ui_contracts/test_raw_colour_ratchet.py.
   (a) `packages/orchestration/orchestrator_move_schema.py`: `    "resume_job",` ->
   `    # "resume_job",` -> R fails;
   (b) `packages/orchestration/orchestrator_loop.py`: the two lines
   `    if kind == MOVE_RESUME_JOB:` and `        return resume_milestone_job(` -> the first becomes
   `    if False:` -> R fails;
   (c) the same file: `    if not _resumable(ev):` -> `    if False:` -> R fails;
   (d) the same file: `    if decision.action != RESUME_PROCEED:` -> `    if False:` -> R fails;
   (e) `packages/orchestration/checkpoints.py`: `    if stop_requested(jid) is not None:` ->
   `    if False:` -> R fails;
   (f) `apps/ui/src/styles/tokens.css`: the line `  --remedy-warning-fg: #664d03;` replaced by an
   empty line -> U fails;
   (g) `apps/ui/src/components/shell/DegradedBanner.module.css`: `  font-size: 0.8125rem;` ->
   `  font-size: 0.8125rem; outline-color: #ff0000;` -> U fails.
   Report exit codes and failing ids, and a mutation that stays green as green. Remove the worktree
   and show `git worktree list`.
G6 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
