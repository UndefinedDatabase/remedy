-- STEP R7 T004 amendments -- F269 Contract & contract templates --
Session 1 of F269 · round 7 · base `c4bd55c1` (branch feature/f269-contract, pushed).

Goal: T004 — an amendment's shape and rules, the function that amends a mission's contract from a
message with the round it applies from, the acknowledgement the orchestrator loop writes into the
mission's ledger, and the renderers listing amendments.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F269.md (T004, Acceptance); the
payload `decisions.md` (DECISION F269 D8 — this round's spec; where this block is terser, it
rules); DECISIONs F269 D2, D4 and D6 in `.agent/decisions.md`; `packages/orchestration/mission_contract.py`;
in `packages/orchestration/orchestrator_loop.py` `LedgerEntry`, `append_ledger_entry`,
`read_ledger`, `next_iteration_index`, `render_ledger` and `run_mission`'s iteration loop; every
other reader of the mission ledger: `apps/cli/commands/mission_cmd.py`,
`packages/orchestration/mission_dossier.py`, `self_use_generator.py`, `token_ledger.py` and
`watchdog.py`.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f269-r7/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md     sha256 49ca94ddcedb9fc2c8c951a8317e4d4100873bf5efe9f8a6adc9007bbd003426
  decisions.md  sha256 629519b91562c1c6a3782f741189d36f28840b5d9489d5ae9622b5378086a839
  plan.md       sha256 e8a9920ba4db1dcd5962fe5bbf9df17bc3f43fe12ab363ef8c6fcf6eb06c360c
  block.md      this block (save it; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of the payloads as `.agent/authored/f269-r7-<name>`;
   `.agent/live_review.md` := its `c4bd55c1` bytes + ledger.md; `.agent/decisions.md` := its
   `c4bd55c1` bytes + decisions.md; `.agent/plan.md` := plan.md.
C2 shape + amend — D8 (1) and (2) in `mission_contract.py`, and D8 (5) in the one renderer. Tests:
   every D8 (1) rule refused on write and on read of a body stored raw (parametrized); amending a
   mission with no contract creates one; the amendment's criterion is origin `amendment`, compiled,
   with the next free id; `applies_from` equals the mission's next round, read from a ledger
   holding two rounds; a second amendment gets `A002`; an existing criterion and entry are left
   byte-identical; a re-plan (`write_planner_criteria`) keeps the amendment criterion and entry;
   `mission contract` text and `--json` show the amendment.
C3 the loop — D8 (3) and (4) in `run_mission`. THE ACCEPTANCE TEST, over a planned mission with a
   contract and fake dispatch and execute seams: round 1 dispatches a job; then an amendment whose
   text names a test path no existing check selects (for example "tests/test_login.py passes") is
   applied, with `applies_from` 2; round 2's ledger holds, before its move entry, one
   `acknowledge_amendment` entry whose detail names what was understood and "applies from round
   2", and the amendment reads `acknowledged_in` 2; the job dispatched in round 2 carries the
   amendment's check in its DoD while round 1's job does not; a third round writes no second
   acknowledgement. Every reader of the ledger named above keeps its reading correct for an entry
   of this kind (for example it is no progress for the watchdog and no cost for the token ledger);
   read each, change only what an acknowledgement entry would break, and test each change.
C4 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: "SESSION 1 of feature
   F269 · round 7 · rounds so far 7" plus one sentence of context self-assessment; per-commit
   tables with `git show --numstat` counts for C1 to C3; every gate's real output; `## Next` naming
   Phase 1 rule 1 then the review of round 7, and "Operator questions open: <the count you read>".
   Then `git push`.

Constraints:
1. Change set: the paths the Bundle names plus test files C2 and C3 edit. Every commit < 500
   inserted lines; split code and tests rather than exceed.
2. Do-not-touch: F264's channel (no command sends an amendment); `dod_compiler.py`, `dod_gate.py`,
   `dod_runners.py`; the ledger stays append-only — no entry is ever rewritten.
3. No test calls a real provider. The shell denies `VAR=x cmd`, `cp` and `sed -i`; use python.
4. Never weaken an assertion or delete a test to pass. A red gate or an ambiguity D8 does not
   settle → stop, commit nothing half-done, report.
5. Build every edited `.agent/` file from `git show c4bd55c1:<path>` bytes.
6. Commit messages "F269 R7 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.

Done when (G1 to G4 at C3, before C4; report literal output and the real exit code):
G1 transport + state: every payload digest matched; a python check prints True that
   `.agent/plan.md` equals plan.md, and that `.agent/live_review.md` and `.agent/decisions.md` equal
   their `c4bd55c1` bytes + their slice.
G2 `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_mission_contract.py
   tests/cli/test_contract_cmd.py tests/orchestration/test_orchestrator_loop.py
   tests/orchestration/test_mission_gate.py tests/orchestration/test_mission_e2e.py
   tests/orchestration/test_watchdog.py tests/orchestration/test_gauntlet_runner.py
   tests/orchestration/test_gauntlet_evidence.py tests/orchestration/test_gauntlet_matrix.py
   tests/orchestration/test_bench_run.py tests/orchestration/test_mission_dossier.py
   tests/orchestration/test_token_ledger.py tests/orchestration/test_self_use_generator.py
   tests/cli/test_mission_cmd.py tests/orchestration/test_mission_state.py
   tests/cli/test_golden_path.py tests/orchestration/test_import_reachability.py tests/docs/` plus
   every other test file this round created or edited → summary line, 0 failed.
G3 `python3 -m ruff check` over every .py file C2 and C3 touched → "All checks passed!".
G4 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C3, run from the worktree
   root with `python3 -B -m pytest`, `__pycache__` purged before each run, the imported
   `mission_contract` module path printed first to prove it resolves inside the worktree; the
   UNMUTATED control over the test files holding C2's and C3's tests first (must be exit 0); each
   mutation reverted before the next: (a) `applies_from` set to the current round instead of the
   next → C2's round-of-effect test red; (b) the loop's acknowledgement not written → the acceptance
   test red; (c) an already acknowledged amendment acknowledged again → the third-round test red.
   Report each exit code and the failing ids; remove the worktree and show `git worktree list`.
G5 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
