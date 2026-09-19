-- STEP R6 R-0753+T008+T014 -- F273 Findings paydown v1 --
Session 1 of F273 · round 6 · base `6c87c133` (the round 5 handoff, branch
`feature/f273-findings-paydown-v1`).

Goal: book round 5's verdict and R-0374's resolution, register R-0986, land DECISION F273 D6, and
build R-0753, R-0745, R-0685 and R-0378 exactly as the reviewer's dry run built them.

Read first, completely: AGENTS.md; the payload `decisions.md` (DECISION F273 D6 — this round's
spec; where this block is terser, it rules).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f273-r6/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  plan.md              sha256 91f55d2eeb0f910ea786cc9724a5ef9203132d308ad66bb87e894a2c04d122b8
  ledger.md            sha256 1a2abc2c53be19e83e59d95008fa787e07dcfc253469a4533ef4757a6333efc1
  decisions.md         sha256 738b6cb328274d571316ff99c1ca572b8c50587200b564823130e3168b4231f7
  block.md             this block (save it; report its digest)
CODE — two diffs research helpers built at `6c87c133`, which the reviewer applied, ran and
red-proved in its own worktree. Apply with `git apply`; never retype or edit a hunk:
  `.remedy-wt/f273-proto-r0753.diff` sha256 140fcbd19c3e140acd6bc806254beeb60a08445db3917b0363b9449598b51bff
  `.remedy-wt/f273-proto-t008.diff` sha256 d4ffc18b49f27a03903558768f7e8b444747bf79670b837b8834a27c2685543a

Bundle (commit order):
C1 bookkeeping — one commit holding exactly: byte copies of every payload above as
   `.agent/authored/f273-r6-<name>`; `.agent/plan.md` := plan.md; `.agent/live_review.md` and
   `.agent/decisions.md` := each one's `6c87c133` bytes + ledger.md and decisions.md respectively.
C2 R-0753 — `git apply .remedy-wt/f273-proto-r0753.diff`.
C3 R-0745, R-0685, R-0378 — `git apply .remedy-wt/f273-proto-t008.diff`.
   Before each code commit run `git status --porcelain` and stage every path the apply touched;
   nothing may be left untracked or unstaged.
C4 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 1 of feature F273 · round 6 · rounds so far 6" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C3; every gate's
   real output; open findings by distinct id (`count_open_findings`) on the committed ledger; one
   `Landed: R-xxxx` line naming its commit for each of R-0753, R-0745, R-0685 and R-0378, in the
   handoff only — never a `Done:` line anywhere; `## Next` naming Phase 1 rule 1 then the review of
   round 6, and "Operator questions open: <the count you read from the file>". Then `git push`.
   Open no pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test calls a real provider. The shell denies `VAR=x cmd`, `cp`, compound commands and `cd`
   before git; use `git -C <path>` and small python scripts under `.remedy-wt/f273-r6/` (prefix
   yours `wk_`) with an explicit `cwd=`. Never use `git stash`: its stack is shared.
3. Never weaken an assertion or delete a test other than the replacements the diffs carry. A red
   gate or an ambiguity D6 does not settle -> stop, commit nothing half-done, report.
4. Build every edited `.agent/` file from `git show 6c87c133:<path>` bytes.
5. Commit messages "F273 R6 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never list, read or write any `.data/` yourself. Never run `scripts/make_review_zip.sh` for real.
7. A reviewer's disposable worktree `.remedy-wt/f273-r6-dry` exists: never run anything in it.

Done when (G1 to G5 at C3, before C4; report literal output and the real exit code):
G1 transport + state + path sets: every payload and diff digest matched; a python check prints
   True that `.agent/plan.md` equals its payload, that `.agent/live_review.md` and
   `.agent/decisions.md` each equal their `6c87c133` bytes + ledger.md and decisions.md, that each
   `.agent/authored/f273-r6-*` copy equals its payload, and that `git show --name-only --format=`
   of C2 and of C3 lists exactly the paths `git apply --numstat` reads from its diff.
G2 code transport: `git rev-parse <C3>:tests <C3>:packages <C3>:apps` prints exactly
   da75aa8947139820ff8ba0fab14168c97770c287, eebe84de0d6e63ca6728cfe21128b654201304da and
   8ff8341b020ac0170a8957f4af715dd0c7f67a76 (the reviewer's dry-run subtrees).
G3 in the primary checkout, serial (no `-n`): `python3 -m pytest -q -p no:cacheprovider
   tests/orchestration/test_budget_guard.py tests/orchestration/test_job_digest.py
   tests/orchestration/test_f018_authority_integration.py tests/orchestration/test_job_budgets.py
   tests/orchestration/test_predictive_budget.py tests/orchestration/test_run_report.py
   tests/orchestration/test_run_report_hook.py tests/orchestration/test_long_run_executor.py
   tests/orchestration/test_token_ledger.py tests/orchestration/test_self_healing_cycles.py
   tests/orchestration/test_resume_kill.py tests/orchestration/test_job_evidence.py
   tests/ui_server/test_digest_route.py tests/ui_contracts/test_digest_mount.py
   tests/ui_contracts/test_digest_card_copy.py tests/cli/test_job_digest_cli.py
   tests/cli/test_stats_report.py tests/cli/test_cost_preview.py
   tests/orchestration/test_cost_preview.py tests/ui_server/test_command_channel.py
   tests/orchestration/test_escalation.py tests/cli/test_decision_answers.py
   tests/ui_contracts/test_decision_answer_wiring.py tests/orchestration/test_provider_retry.py
   tests/orchestration/test_evidence_index.py tests/orchestration/test_import_reachability.py
   tests/orchestration/test_rate_governor.py tests/cli/test_job_budget_set.py
   tests/cli/test_golden_path.py` -> summary line, 0 failed, exit 0, no `R-0803:` line.
G4 `python3 -m ruff check . --output-format concise` from the primary checkout's root ->
   "All checks passed!", exit 0; and `tests/orchestration/test_test_runner.py -k vitest` in the
   primary checkout -> passed, exit 0 (vitest over `apps/ui`, whose two `src/api` files C3 edits).
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C3, run from its root
   with `python3 -B -m pytest -q -p no:cacheprovider`, `__pycache__` purged before each run, the
   imported `packages.orchestration.budget_guard` path printed first to prove it resolves inside the
   worktree. The UNMUTATED control first over the test files named below (exit 0). Then, each
   reverted before the next, counting the mutated bytes in the named file first (each must be 1),
   naming the failing ids:
   (a) `packages/orchestration/pingpong_job.py`: the line
   `            "measured_cost_usd": _money.measured_cost_usd if _money is not None else None,` ->
   `            "measured_cost_usd": None,` -> `tests/orchestration/test_job_digest.py` fails;
   (b) `packages/orchestration/budget_guard.py`: the line
   `    PERSISTED_ACTUALS_SCHEMA_V2: _PERSISTED_ACTUALS_FIELDS | _PERSISTED_MONEY_FIELDS,` deleted
   -> `tests/orchestration/test_budget_guard.py` fails;
   (c) `packages/orchestration/evidence_index.py`: the line `import subprocess` inserted between
   `import json` and `from datetime import datetime, timezone` ->
   `tests/ui_server/test_command_channel.py` fails;
   (d) `packages/orchestration/ui_server.py`: the three lines starting
   `        if (command == DECISION_RESOLVE_COMMAND_ID and isinstance(answer, str)` deleted ->
   `tests/ui_server/test_command_channel.py` fails;
   (e) `packages/orchestration/escalation.py`: the two lines `    if not str(answer).strip():` and
   `        return None` deleted -> `tests/orchestration/test_escalation.py` fails;
   (f) `packages/orchestration/pingpong_loop.py`: the line
   `            and not out.error.startswith("provider_error:")` deleted ->
   `tests/orchestration/test_provider_retry.py` fails.
   Report exit codes and failing ids, and a mutation that stays green as green. Remove the worktree
   and show `git worktree list`.
G6 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
