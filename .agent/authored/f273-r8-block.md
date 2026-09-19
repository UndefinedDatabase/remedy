-- STEP R8 T013+T011+R-0986 -- F273 Findings paydown v1 --
Session 2 of F273 · round 8 · base `ec4e2e86` (the round 7 handoff, branch
`feature/f273-findings-paydown-v1`).

Goal: book round 7's verdict and its six resolutions, register R-0987, land DECISION F273 D8, and
build T013, T011 and R-0986 with R-0987 exactly as the reviewer's dry run built them.

Read first, completely: AGENTS.md; the payload `decisions.md` (DECISION F273 D8 — this round's
spec; where this block is terser, it rules).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f273-r8/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  plan.md              sha256 b278ebc6683859b216013514824630ec225bd1883954bf10518bd82984d0f81b
  ledger.md            sha256 5ae0725dca2880ccb9634aa3da0df1780c22871e58ab805c813f057561821dc1
  decisions.md         sha256 ba6696affba6bdf30fea78f391e8a74a209b731fea65f27ac27e9d8d6a8619f3
  block.md             this block (save it; report its digest)
CODE — three diffs research helpers built at `ec4e2e86`, which the reviewer applied, ran and
red-proved in its own worktree. Apply with `git apply`; never retype or edit a hunk:
  `.remedy-wt/f273-proto-t013.diff`  sha256 6d502312283334c1c3bd98b5f2689d01c15988c7ab7ea905f5e9e13aebe9d290
  `.remedy-wt/f273-proto-t011.diff`  sha256 c2305f5467882c8b2771343fda07bd7eeb211da6a74bf37488d935b2aa68afb6
  `.remedy-wt/f273-proto-r0986.diff` sha256 6146f97bc3d8fe87b617af193b591061b01975cb2719ef1c8d69d572583d9b73

Bundle (commit order):
C1 bookkeeping — one commit holding exactly: byte copies of every payload above as
   `.agent/authored/f273-r8-<name>`; `.agent/plan.md` := plan.md; `.agent/live_review.md` and
   `.agent/decisions.md` := each one's `ec4e2e86` bytes + ledger.md and decisions.md respectively.
C2 R-0570, R-0665, R-0752, R-0769 — `git apply .remedy-wt/f273-proto-t013.diff`.
C3 R-0666, R-0667, R-0668 — `git apply .remedy-wt/f273-proto-t011.diff`.
C4 R-0986, R-0987 — `git apply .remedy-wt/f273-proto-r0986.diff`.
   Before each code commit run `git status --porcelain` and stage every path the apply touched
   (new files included); nothing may be left untracked or unstaged.
C5 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 2 of feature F273 · round 8 · rounds so far 8" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C4; every gate's
   real output; open findings by distinct id (`count_open_findings`) on the committed ledger; one
   `Landed: R-xxxx` line naming its commit for each of R-0570, R-0665, R-0752, R-0769, R-0666,
   R-0667, R-0668, R-0986 and R-0987, in the handoff only — never a `Done:` line of your own;
   `## Next` naming Phase 1 rule 1 then the review of round 8, and "Operator questions open: <the
   count you read from the file>". Then `git push`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test calls a real provider. The shell denies `VAR=x cmd`, `cp`, loops, `$( )`, `$VAR` and
   `cd` before git; use `git -C <path>` and small python scripts under `.remedy-wt/f273-r8/`
   (prefix yours `wk_`) with an explicit `cwd=`. Never use `git stash`: its stack is shared.
3. Never weaken an assertion or delete a test other than the changes the diffs carry. A red gate or
   an ambiguity D8 does not settle -> stop, commit nothing half-done, report.
4. Build every edited `.agent/` file from `git show ec4e2e86:<path>` bytes.
5. Commit messages "F273 R8 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never list, read or write any `.data/` yourself. Never run `scripts/make_review_zip.sh` for real,
   never run the `remedy` CLI, `run_job` or the self-use runner, and create no branch.

Done when (G1 to G5 at C4, before C5; report literal output and the real exit code):
G1 transport + state + path sets: every payload and diff digest matched; a python check prints
   True that `.agent/plan.md` equals its payload, that `.agent/live_review.md` and
   `.agent/decisions.md` each equal their `ec4e2e86` bytes + ledger.md and decisions.md, that each
   `.agent/authored/f273-r8-*` copy equals its payload, and that `git show --name-only --format=`
   of C2, C3 and C4 each lists exactly the paths `git apply --numstat` reads from its diff.
G2 code transport: `git rev-parse <C4>:tests <C4>:packages <C4>:scripts <C4>:docs <C4>:README.md`
   prints exactly 1623bf8dd892d1b2fa14d5ec2195daa62ff6adfc, cd0bde167f2a16a4fcdf3e259320437c55d493a3,
   5ccac4ccb4a128d21034b1fb7325fb393a7a1863, 1eb23a428f17ba8ddfaecfd6b7be63fd67b7ddc9 and
   7a30c8641b2a36f9f9a702556d73291846cc03a3 (the reviewer's dry-run objects).
G3 in the primary checkout, serial (no `-n`): `python3 -m pytest -q -p no:cacheprovider tests/docs/
   tests/orchestration/test_review_package_status.py
   tests/orchestration/test_review_manual_completion_shapes.py
   tests/orchestration/test_review_authoritative_e2e.py
   tests/orchestration/test_review_manifest_archive_same_snapshot.py
   tests/orchestration/test_manual_completion_bundle.py tests/orchestration/test_job_evidence.py
   tests/orchestration/test_fresh_evidence_gate.py tests/orchestration/test_artifact_contract_gate.py
   tests/orchestration/test_job_digest.py tests/orchestration/test_f018_authority_integration.py
   tests/orchestration/test_budget_guard.py tests/orchestration/test_job_budgets.py
   tests/orchestration/test_budget_stop_integration.py tests/orchestration/test_token_ledger.py
   tests/orchestration/test_import_reachability.py tests/ui_server/test_budget_tick_envelope.py
   tests/ui_server/test_dashboard_contract.py tests/cli/test_job_digest_cli.py
   tests/cli/test_quick_start.py tests/test_agent_tooling.py tests/test_no_orphan_modules.py
   tests/cli/test_golden_path.py` -> summary line, 0 failed, exit 0, no `R-0803:` line.
G4 `python3 -m ruff check . --output-format concise` from the primary checkout's root ->
   "All checks passed!", exit 0.
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C4, run from its root
   with `python3 -B -m pytest -q -p no:cacheprovider`, `__pycache__` purged before each run, the
   imported `packages.orchestration.pingpong_job` path printed first to prove it resolves inside the
   worktree. The UNMUTATED control first over the test files named below (exit 0). Then, each
   reverted from its saved bytes before the next, counting each FROM line (with its newline) in the
   named file first (each must be 1), naming the failing ids. D = tests/docs/test_docs_consistency.py;
   M = tests/orchestration/test_review_package_status.py and
   tests/orchestration/test_review_manual_completion_shapes.py; J =
   tests/orchestration/test_job_digest.py, tests/orchestration/test_f018_authority_integration.py and
   tests/orchestration/test_budget_guard.py.
   (a) `README.md`: the line `F115 prompt breakdown & cost report,` deleted -> D fails;
   (b) `README.md`: after the line `ledger as a normal finding).` insert a blank line and the line
   `F106 session resume: a misplaced second entry.` -> D fails;
   (c) `docs/ui/design_reference/assumption_log.md` deleted -> D fails;
   (d) `docs/roadmap/features/T4_F119.md`: in the line
   `the shell itself. Suggested tests: tests/ui_contracts/test_memory_api.py` replace
   `ui_contracts` by `ui_contract` -> D fails;
   (e) `scripts/build_review_manifest.py`:
   `        alignment = _build_alignment(review_subject["dirty_files"], evidence_view)` ->
   `        alignment = _build_alignment(dirty, evidence_view)` -> M fails;
   (f) the same file: the line
   `        "commit_execution_arbitration": commit_execution_arbitration(gate_matrix),` deleted -> M fails;
   (g) `packages/orchestration/job_evidence.py`: insert the line `    _w("job_report.json", "")`
   directly above the one line starting `    _w("job_timeline.json", {"job_id": job_id,` -> M fails;
   (h) `packages/orchestration/pingpong_job.py`:
   `            _own_cost_usd = (_own_cost_usd or 0.0) + _cost` -> `            pass` -> J fails;
   (i) the same file: the line `                **_money_kwargs(),` deleted -> J fails;
   (j) the same file: `                int(ua.get("input_tokens", 0) or 0) +` ->
   `                getattr(ua, "input_tokens", 0) +` -> J fails.
   Report exit codes and failing ids, and a mutation that stays green as green. Remove the worktree
   and show `git worktree list`.
G6 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
