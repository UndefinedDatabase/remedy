-- STEP R2 T002 -- F269 Contract & contract templates --
Session 1 of F269 · round 2 · base `17edb194` (branch feature/f269-contract, pushed).

Goal: T002 — the contract compiled by F061's compiler, planner criteria written when a mission is
planned, each dispatched job's DoD carrying its contract slice, criterion statuses read back from
that job's gate, and the orchestrator's achieve move held while a blocking criterion is not met.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F269.md; the payload `decisions.md`
(DECISION F269 D4 — this round's spec; where this block is terser, it rules); DECISIONs F269 D2
and D3 in `.agent/decisions.md`; `packages/orchestration/mission_contract.py`,
`dod_compiler.py`, `dod_gate.py`, and in `orchestrator_loop.py` `execute_move`, `evaluate_move`
and `run_gate_for_job`.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f269-r2/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md     sha256 8c98f23e6e572e57c3ae0d0f1798527de1830ad8c0d2ae41f4a4187f653b6b04
  decisions.md  sha256 d38c6e684ff9ac99e6e6ca323ed34e7f56eb331be79bacd7ab4b0138a2e4add4
  plan.md       sha256 7e10a17cabb6c458bd39a68934d40defdc7acff62ab3d59ad9877179d5a7ce69
  opq.md        sha256 3f2aeda2f041845f1049cc0127fb25016646cf310aab1a07ad1c0811f5b33ade
  block.md      this block (save it; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of the payloads as `.agent/authored/f269-r2-<name>`;
   `.agent/live_review.md` := its `17edb194` bytes + ledger.md; `.agent/decisions.md` := its
   `17edb194` bytes + decisions.md; `.agent/plan.md` := plan.md; and in
   `tests/orchestration/test_mission_state.py` only the docstring of
   `test_the_contract_round_trips_through_disk`, reworded so it no longer calls the field reserved
   or empty and names `packages/orchestration/mission_contract.py` as the shape's owner.
C2 compile + planner criteria — D4 (1) and (2): the compiler function and the planner-criteria
   writer in `mission_contract.py`; `plan_mission` in `packages/orchestration/mission_compiler.py`
   calls the writer after the milestone DoDs are attached. Tests: compile gives every criterion a
   check with id `ctr-<id>`, refs [`<id>:0`] and the criterion's own `blocking` (a non-blocking
   criterion stays non-blocking); a criterion text naming a test path compiles to that selector;
   a planned mission carries one planner criterion per milestone, scoped to it; a re-plan keeps a
   non-planner criterion with its id and replaces the planner ones.
C3 the job's DoD and its results — D4 (3) and (4): the merge function and the results function
   in `mission_contract.py`, both called from `execute_move`'s dispatch branch in
   `orchestrator_loop.py` (merge after `attach_milestone_dod`, results after the job executed).
   Tests: a slice check whose kind and spec equal an existing DoD check is not added a second time;
   a job with no DoD gets one holding its slice checks; a job for M1 gets no M2-scoped check;
   statuses and `evidence_ref` follow a stored gate result; no gate result changes nothing.
C4 the gate and the surfaces — D4 (5) and (6): the blockers function; `evaluate_move`'s refusal;
   `remedy mission achieve`'s notice line and `unmet_blocking_criteria` JSON key (its handler in
   `apps/cli/commands/mission_cmd.py`); `remedy do --json`'s `contract` (`apps/cli/commands/do_cmd.py`
   and whatever `do_sequence.py` must hand it). THE ACCEPTANCE TEST, in
   `tests/orchestration/test_orchestrator_loop.py` or a new `tests/orchestration/test_mission_gate.py`:
   a planned mission with a three-criterion contract whose checks are decided by files in a tmp
   directory (two pass, one cannot), one job dispatched through `execute_move` with an `execute`
   seam that runs the REAL `dod_gate.run_job_gate` in that directory; afterwards the contract
   reads two `met` and one `unmet`, and `evaluate_move` refuses `declare_mission_achieved` with a
   reason naming that criterion's id; with that check made passable and the job re-run, the refusal
   is gone. Also: `mission achieve` on such a mission exits 0, prints the unmet ids and sets the
   status; `do --json` carries the contract body. Every existing test whose pinned behaviour D4
   changes by design (for example `data["contract"] is None` in `tests/cli/test_golden_path.py` and
   `tests/cli/test_do_sequence_cli.py`) is updated to the new behaviour with the test's own property
   kept, and named in the handoff with its reason.
C5 handoff — `.agent/operator_questions.md` := its `17edb194` bytes + opq.md, and rewrite
   `.agent/handoff.md` per docs/agents/handback_template.md: "SESSION 1 of feature F269 · round
   2 · rounds so far 2" plus one sentence of context self-assessment; per-commit tables with `git
   show --numstat` counts for C1 to C4; every gate's real output; `## Next` naming Phase 1 rule 1
   then the review of round 2, and "Operator questions open: <the count you read after the
   append>". Then `git push`.

Constraints:
1. Change set: the paths the Bundle names plus test files C2 to C4 edit and the regenerated
   import-reachability allowlist if its test requires it. Every commit < 500 inserted lines; split
   a commit into code and tests (C2a/C2b) rather than exceed.
2. Do-not-touch: `dod_compiler.py`, `dod_gate.py` and `dod_runners.py` are called, never edited;
   F061's check kinds and runners, F031's inbox contract, F264's channel, F072's renderer.
3. No test calls a real provider. The shell denies `VAR=x cmd` and `cp`; copy bytes with python.
4. Never weaken an assertion or delete a test to pass. A red gate or an ambiguity D4 does not
   settle → stop, commit nothing half-done, report.
5. Build every edited `.agent/` file from `git show 17edb194:<path>` bytes.
6. Commit messages "F269 R2 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.

Done when (G1 to G4 at C4, before C5; report literal output and the real exit code):
G1 transport + state: every payload digest matched; a python check prints True that
   `.agent/plan.md` equals plan.md, that `.agent/live_review.md` equals its `17edb194` bytes +
   ledger.md, and that `.agent/decisions.md` equals its `17edb194` bytes + decisions.md.
G2 `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_mission_contract.py
   tests/cli/test_contract_cmd.py tests/orchestration/test_orchestrator_loop.py
   tests/orchestration/test_mission_e2e.py tests/orchestration/test_mission_compiler.py
   tests/orchestration/test_mission_state.py tests/cli/test_mission_cmd.py
   tests/orchestration/test_dod_gate.py tests/orchestration/test_dod_compiler.py
   tests/orchestration/test_watchdog.py tests/orchestration/test_gauntlet_runner.py
   tests/orchestration/test_gauntlet_injection.py tests/cli/test_do_sequence_cli.py
   tests/cli/test_do_flags.py tests/cli/test_do_cmd_summary.py tests/orchestration/test_do_sequence.py
   tests/cli/test_golden_path.py tests/orchestration/test_import_reachability.py
   tests/test_command_catalog.py tests/docs/` plus every other test file this round created or
   edited → summary line, 0 failed (the reviewer's base reading of the existing files at
   `17edb194` was 0 failed).
G3 `python3 -m ruff check` over every .py file C1 to C4 touched → "All checks passed!".
G4 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C4, run from the worktree
   root with `python3 -B -m pytest`, `__pycache__` purged before each run, the imported
   `mission_contract` module path printed first to prove it resolves inside the worktree; the
   UNMUTATED control over the test files named below first (must be exit 0); each mutation
   reverted before the next: (a) the compiler sets every check blocking regardless of the
   criterion → C2's non-blocking test red; (b) the merge adds a check even when an equal kind and
   spec is present → C3's no-duplicate test red; (c) the results function sets `met` whatever the
   evidence says → the acceptance test red; (d) `evaluate_move`'s contract refusal removed → the
   acceptance test red. Test files: `tests/orchestration/test_mission_contract.py`, the file
   holding the acceptance test, and `tests/orchestration/test_orchestrator_loop.py`. Report each
   exit code and the failing ids; remove the worktree and show `git worktree list`.
G5 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
