-- STEP R5 do's gate -- F269 Contract & contract templates --
Session 1 of F269 · round 5 · base `09d7641f` (branch feature/f269-contract, pushed).

Goal: whole-mission checks enter a job's DoD as reported checks, the job gate runs inside `run_job`
before the worktree goes, `remedy do`'s jobs carry their contract slice, and `do`'s result names
the blocking criteria that are not met.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F269.md; the payload `decisions.md`
(DECISION F269 D6 — this round's spec; where this block is terser, it rules); DECISIONs F269 D3 and
D4 in `.agent/decisions.md`; `packages/orchestration/mission_contract.py`
(`merge_contract_slice_into_dod`, `record_contract_results`, `contract_blockers`);
`packages/orchestration/dod_gate.py` (`run_job_gate`, `gate_blocker`); in
`packages/orchestration/pingpong_job.py` `run_job` from its `if all_done:` block through its
`finally` and `_finalize_job_workspace`; in `packages/orchestration/do_sequence.py` `_step_shape`
and `_step_run`; in `apps/cli/commands/do_cmd.py` the `--json` body and text output of
`_cmd_do_order`.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f269-r5/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md     sha256 df3872343f97409a65c0d8814c9f501920afdf36764c2147175d8655811deed2
  decisions.md  sha256 e53dc595d4618bf376ad53fec1bab05e8aa9a68130a638b0590387c8f447b31a
  plan.md       sha256 cace050496a66db138cc4e6de34c676ac7266a26dbf1cc344fc9602e587811f9
  block.md      this block (save it; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of the payloads as `.agent/authored/f269-r5-<name>`;
   `.agent/live_review.md` := its `09d7641f` bytes + ledger.md; `.agent/decisions.md` := its
   `09d7641f` bytes + decisions.md; `.agent/plan.md` := plan.md.
C2 the merge — D6 (1) in `merge_contract_slice_into_dod`. Tests: a whole-mission criterion's check
   enters the DoD with `blocking` false even when the criterion is blocking; a milestone-scoped
   blocking criterion's check enters blocking; a job gate whose only red check is a whole-mission
   one releases, while the criterion reads `unmet` afterwards and still holds `evaluate_move`'s
   achieve refusal. Update the round 2 tests this changes by design, keeping their properties.
C3 the gate in `run_job` — D6 (2). Tests over a tmp git repository with the fake providers: a job
   with a stored DoD whose blocking check cannot pass ends blocked with a `dod_blocking_red:`
   reason naming the check, and its worktree is kept; a job whose DoD's only red check is
   non-blocking completes; a job with no stored DoD completes exactly as before and writes no gate
   result; a job linked to a mission with a contract has its slice criteria's statuses and
   `evidence_ref` written after its run.
C4 `do` — D6 (3) and (4). Tests (the fake roles, `--no-llm --no-ui`, a tmp git repository with one
   committed file and no tests): `do --contract cli-tool` merges the whole-mission checks into the
   job's DoD, all non-blocking; the job completes; afterwards the contract's `The test suite
   passes.` criterion reads `unmet` with an `evidence_ref` naming the job, the hygiene criteria
   read `met`, `--json` `unmet_blocking_criteria` lists exactly the blocking criteria not met in
   contract order, and the text output carries the count line naming each with its status; a `do`
   whose order proposes no template carries `unmet_blocking_criteria` naming only criteria not
   met. Update any existing test whose pinned behaviour D6 changes by design, keeping its property,
   named in the handoff with its reason.
C5 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: "SESSION 1 of feature
   F269 · round 5 · rounds so far 5" plus one sentence of context self-assessment; per-commit
   tables with `git show --numstat` counts for C1 to C4; every gate's real output; `## Next` naming
   Phase 1 rule 1 then the review of round 5, and "Operator questions open: <the count you read>".
   Then `git push`.

Constraints:
1. Change set: the paths the Bundle names plus test files C2 to C4 edit, `docs/guides/do-run-v1.md`
   where its `--json` field list must name `unmet_blocking_criteria`, and the regenerated
   import-reachability allowlist if its test requires it. Every commit < 500 inserted lines; split
   code and tests rather than exceed.
2. Do-not-touch: `dod_compiler.py`, `dod_gate.py`, `dod_runners.py`; F061's check kinds and runners,
   F031's inbox contract, F264's channel, F072's renderer.
3. No test calls a real provider. The shell denies `VAR=x cmd`, `cp` and `sed -i`; use python.
4. Never weaken an assertion or delete a test to pass. A red gate or an ambiguity D6 does not
   settle → stop, commit nothing half-done, report.
5. Build every edited `.agent/` file from `git show 09d7641f:<path>` bytes.
6. Commit messages "F269 R5 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.

Done when (G1 to G4 at C4, before C5; report literal output and the real exit code):
G1 transport + state: every payload digest matched; a python check prints True that
   `.agent/plan.md` equals plan.md, and that `.agent/live_review.md` and `.agent/decisions.md` equal
   their `09d7641f` bytes + their slice.
G2 `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_mission_contract.py
   tests/orchestration/test_mission_gate.py tests/orchestration/test_orchestrator_loop.py
   tests/orchestration/test_mission_e2e.py tests/orchestration/test_gauntlet_runner.py
   tests/orchestration/test_job_fulfillment.py tests/orchestration/test_fence_production_e2e.py
   tests/orchestration/test_dod_gate.py tests/orchestration/test_pingpong.py
   tests/orchestration/test_job_worktree_integration.py tests/orchestration/test_run_manifest_recovery.py
   tests/orchestration/test_job_task_runner.py tests/cli/test_do_sequence_cli.py tests/cli/test_do_flags.py
   tests/cli/test_do_cmd_summary.py tests/orchestration/test_do_sequence.py tests/cli/test_golden_path.py
   tests/orchestration/test_import_reachability.py tests/docs/` plus every other test file this
   round created or edited → summary line, 0 failed (the reviewer's base reading of the existing
   files at `09d7641f` was 0 failed).
G3 `python3 -m ruff check` over every .py file C2 to C4 touched → "All checks passed!".
G4 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C4, run from the worktree
   root with `python3 -B -m pytest`, `__pycache__` purged before each run, the imported
   `mission_contract` module path printed first to prove it resolves inside the worktree; the
   UNMUTATED control over the test files holding C2's, C3's and C4's tests first (must be exit 0);
   each mutation reverted before the next: (a) the merge keeps a whole-mission criterion's own
   `blocking` → C2's non-blocking test red; (b) `run_job`'s gate call removed → C3's blocked-job
   test red; (c) `do`'s shape step merges nothing → C4's `--contract cli-tool` test red. Report
   each exit code and the failing ids; remove the worktree and show `git worktree list`.
G5 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
