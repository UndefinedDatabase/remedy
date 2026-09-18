-- STEP R8 T005 remainder -- F269 Contract & contract templates --
Session 1 of F269 · round 8 · base `5fac20d6` (branch feature/f269-contract, pushed).

Goal: T005 — the remainder decision raised at the loop's budget end and at a `do` job's budget stop
while blocking criteria are open, and a one-word "yes" at either answer door starting the follow-up
mission with the prefilled order and contract.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F269.md (T005, Acceptance); the
payload `decisions.md` (DECISION F269 D9 — this round's spec; where this block is terser, it
rules); DECISIONs F269 D4 and D6 in `.agent/decisions.md`; `packages/orchestration/escalation.py`
(`enqueue_task_decision`, `answer_task_decision`); in `orchestrator_loop.py`
`escalate_repeated_refusal`, `open_mission_decisions` and `run_mission`'s `iteration_limit` exit;
`packages/orchestration/watchdog.py`'s marker dedupe; in `apps/cli/commands/decision.py`
`_cmd_decision_resolve` (its `td:` branch and the `plan:` branch's `--as-mission`); in
`packages/orchestration/ui_server.py` `_dispatch_decision_resolve`; `TestCommandDoorImportGuard`
in `tests/ui_server/test_command_channel.py`; in `do_sequence.py` `_step_run` and its Next lines.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f269-r8/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md     sha256 186352ad2b5b5e64856e33cf686c38962b7f671c378289616e8aefbddf65c7a9
  decisions.md  sha256 34e706fd4eae03c6b76b52eed83838a7232f44d01488c9b4eb495af99262bec6
  plan.md       sha256 9be4d9bae5398ea28b8537d0b948ee5d264382c051e66a7d5d87405776e772d2
  block.md      this block (save it; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of the payloads as `.agent/authored/f269-r8-<name>`;
   `.agent/live_review.md` := its `5fac20d6` bytes + ledger.md; `.agent/decisions.md` := its
   `5fac20d6` bytes + decisions.md; `.agent/plan.md` := plan.md.
C2 raise + act — D9 (1) and (3)'s two functions in `mission_contract.py`. Tests: a mission with
   two blockers gets one decision on its latest job's first task whose question starts with the
   marker and names both ids and texts, options `yes`/`no`, empty safe default, `impact` the
   prefilled order; a second raise while it is open returns None; no blockers, or no job, returns
   None; answering `yes` creates a follow-up mission whose order is the prefilled order and whose
   contract holds exactly the blockers, renumbered, `open`; `no`, or another answer, or a
   non-remainder decision, creates nothing.
C3 the call sites — D9 (2) in `run_mission` and in `do`, and D9 (3) in both answer doors, with the
   one `ALLOWED_IMPORTS` entry D9 rules. THE ACCEPTANCE TEST: a planned mission with a
   three-criterion contract, one criterion's check unable to pass, run by `run_mission` with the
   real job gate in a tmp directory (as `tests/orchestration/test_mission_gate.py` does) and a
   small `max_iterations`, ends `iteration_limit`; the achieve move is refused naming that
   criterion; one open remainder decision names it; `remedy decision resolve <job> <id> --reason
   yes` exits 0, prints the follow-up mission's id and `remedy mission plan <id>`, and that mission's
   contract holds exactly the unmet criterion. Also: the cockpit door answering `yes` to a remainder
   decision creates the follow-up; a `do` walk whose job is stopped by its budget with blockers
   raises the decision and its Next lines name the answer command. Every existing test whose pinned
   behaviour D9 changes by design is updated with its property kept, named in the handoff.
C4 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: "SESSION 1 of feature
   F269 · round 8 · rounds so far 8" plus one sentence of context self-assessment; per-commit
   tables with `git show --numstat` counts for C1 to C3; every gate's real output; `## Next` naming
   Phase 1 rule 1, then the review of round 8, then the closure sequence, and "Operator questions
   open: <the count you read>". Then `git push`.

Constraints:
1. Change set: the paths the Bundle names plus test files C2 and C3 edit, and the regenerated
   import-reachability allowlist if its test requires it. Every commit < 500 inserted lines; split
   code and tests rather than exceed.
2. Do-not-touch: F031's inbox contract — no new decision type, no change to `decision_queue.py`'s
   type sets, `escalation.py` or the record shape; F009's door gains only the one import D9 rules;
   `dod_compiler.py`, `dod_gate.py`, `dod_runners.py`.
3. No test calls a real provider. The shell denies `VAR=x cmd`, `cp` and `sed -i`; use python.
4. Never weaken an assertion or delete a test to pass. A red gate or an ambiguity D9 does not
   settle → stop, commit nothing half-done, report.
5. Build every edited `.agent/` file from `git show 5fac20d6:<path>` bytes.
6. Commit messages "F269 R8 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.

Done when (G1 to G4 at C3, before C4; report literal output and the real exit code):
G1 transport + state: every payload digest matched; a python check prints True that
   `.agent/plan.md` equals plan.md, and that `.agent/live_review.md` and `.agent/decisions.md` equal
   their `5fac20d6` bytes + their slice.
G2 `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_mission_contract.py
   tests/orchestration/test_mission_gate.py tests/orchestration/test_orchestrator_loop.py
   tests/orchestration/test_mission_e2e.py tests/orchestration/test_watchdog.py
   tests/cli/test_decision_answers.py tests/cli/test_decision_cmd.py tests/cli/test_plan_approval.py
   tests/cli/test_open_decisions_view.py tests/orchestration/test_decision_inbox.py
   tests/orchestration/test_decision_evidence.py tests/orchestration/test_escalation.py
   tests/orchestration/test_approval_queue.py tests/orchestration/test_proposal_decision.py
   tests/orchestration/test_budget_stop_integration.py tests/ui_contracts/test_decision_answer_wiring.py
   tests/ui_contracts/test_decision_urgency_parity.py tests/ui_server/test_command_channel.py
   tests/cli/test_do_sequence_cli.py tests/cli/test_do_cmd_cli_path.py tests/cli/test_do_cmd_summary.py
   tests/orchestration/test_do_sequence.py tests/cli/test_golden_path.py
   tests/orchestration/test_import_reachability.py tests/docs/` plus every other test file this
   round created or edited → summary line, 0 failed (the reviewer's base reading of the existing
   files at `5fac20d6` was 0 failed).
G3 `python3 -m ruff check` over every .py file C2 and C3 touched → "All checks passed!".
G4 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C3, run from the worktree
   root with `python3 -B -m pytest`, `__pycache__` purged before each run, the imported
   `mission_contract` module path printed first to prove it resolves inside the worktree; the
   UNMUTATED control over the test files holding C2's and C3's tests first (must be exit 0); each
   mutation reverted before the next: (a) the raise ignores an open remainder decision → C2's
   dedupe test red; (b) the actor acts on any answer, not only `yes` → C2's `no` test red; (c)
   `run_mission` raises nothing at `iteration_limit` → the acceptance test red. Report each exit
   code and the failing ids; remove the worktree and show `git worktree list`.
G5 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
