-- STEP R9 R-0971 repair -- F269 Contract & contract templates --
Session 1 of F269 · round 9 · base `f7775533` (branch feature/f269-contract, pushed).

Goal: repair R-0971 — a follow-up mission carries its remainder as one amendment (DECISION F269
D10), so planning it keeps every carried criterion.

Read first, completely: AGENTS.md; the payload `ledger.md` (round 8's gate entry and finding
R-0971 with its fix clause); the payload `decisions.md` (DECISION F269 D10 — this round's spec);
DECISIONs F269 D8 and D9 in `.agent/decisions.md`; in `packages/orchestration/mission_contract.py`
`start_remainder_follow_up_mission`, `write_planner_criteria` and the amendment entry rules;
the reviewer's probe `.remedy-wt/f269-r8/probe_replan.py`.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f269-r9/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md     sha256 431819ae828b1afd33fed9b613fa803a4fbd0c71dc8a7cae4987c5ea5d8d40f3
  decisions.md  sha256 be0c9a3fa77a99539c5419cf0412d2923eab39d7e1c86c60edeb7fb9771aa0b7
  plan.md       sha256 b151547a40a1dc54c4a8a6b3f8486cb1a7ae334cbdf5de1805a5cffd0ead9df4
  block.md      this block (save it; report its digest)

Bundle (commit order):
C1 the finding first — one commit: byte copies of the payloads as `.agent/authored/f269-r9-<name>`;
   `.agent/live_review.md` := its `f7775533` bytes + ledger.md; `.agent/decisions.md` := its
   `f7775533` bytes + decisions.md; `.agent/plan.md` := plan.md.
C2 the repair — D10 in `start_remainder_follow_up_mission`. Tests: THE R-0971 TEST — a follow-up
   started from a mission whose unmet blocker has origin `planner` is planned with `plan_mission`
   (no provider), and afterwards every carried criterion is still present with its id and text,
   origin `amendment`, with the planner's own criteria after it; the follow-up's contract holds one
   amendment entry `A001` whose `criteria` are every carried id and whose `understood` names the
   old and new ids; update the round 8 tests that pinned the kept origin, keeping their properties.
C3 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: "SESSION 1 of feature
   F269 · round 9 · rounds so far 9" plus one sentence of context self-assessment; per-commit
   tables with `git show --numstat` counts for C1 and C2; every gate's real output; one line
   `Landed: R-0971 — <what changed, which commit>` in the handoff only (never a `Done:`, never in
   the ledger); `## Next` naming Phase 1 rule 1, then the review of round 9, then the closure
   sequence, and "Operator questions open: <the count you read>". Then `git push`.

Constraints:
1. Change set: the paths the Bundle names plus the test files C2 edits. Every commit < 500 inserted
   lines.
2. Do-not-touch: `write_planner_criteria`'s rule that a re-plan replaces the planner's own
   criteria; F031's inbox contract; `dod_compiler.py`, `dod_gate.py`, `dod_runners.py`.
3. No test calls a real provider. The shell denies `VAR=x cmd`, `cp` and `sed -i`; use python.
4. Never weaken an assertion or delete a test to pass. A red gate or an ambiguity D10 does not
   settle → stop, commit nothing half-done, report.
5. Build every edited `.agent/` file from `git show f7775533:<path>` bytes.
6. Commit messages "F269 R9 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.

Done when (G1 to G4 at C2, before C3; report literal output and the real exit code):
G1 transport + state: every payload digest matched; a python check prints True that
   `.agent/plan.md` equals plan.md, and that `.agent/live_review.md` and `.agent/decisions.md` equal
   their `f7775533` bytes + their slice.
G2 `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_mission_contract.py
   tests/orchestration/test_mission_gate.py tests/orchestration/test_orchestrator_loop.py
   tests/cli/test_decision_cmd.py tests/cli/test_decision_answers.py
   tests/ui_server/test_command_channel.py tests/cli/test_contract_cmd.py
   tests/cli/test_do_sequence_cli.py tests/cli/test_golden_path.py tests/docs/` plus every other
   test file this round edited → summary line, 0 failed.
G3 `python3 -m ruff check` over every .py file C2 touched → "All checks passed!".
G4 mutation red-proof in ONE disposable worktree under `.remedy-wt/` at C2, run from the worktree
   root with `python3 -B -m pytest`, `__pycache__` purged before each run, the imported
   `mission_contract` module path printed first to prove it resolves inside the worktree; the
   UNMUTATED control over the test file holding the R-0971 test first (must be exit 0); then the
   carried criteria given back each blocker's own origin → the R-0971 test red. Report both exit
   codes and the failing ids; remove the worktree and show `git worktree list`.
G5 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
