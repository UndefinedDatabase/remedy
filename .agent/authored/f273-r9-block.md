-- STEP R9 T010+T007 -- F273 Findings paydown v1 --
Session 2 of F273 · round 9 · base `db9a05cc` (the round 8 handoff, branch
`feature/f273-findings-paydown-v1`).

Goal: book round 8's verdict and its nine resolutions, land DECISION F273 D9, and build T010
(R-0411) and T007's R-0796 with F267's amendment exactly as the reviewer's dry run built them.

Read first, completely: AGENTS.md; the payload `decisions.md` (DECISION F273 D9 — this round's
spec; where this block is terser, it rules).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f273-r9/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  plan.md              sha256 a0b702a9aae1c9e5c517dce3c5d2b46d03ca8ced005022ee3ae98d7e15235979
  ledger.md            sha256 2cb978843d76739fb417d65dd9abc83a6e47d84d5d62be4be74145e298a3d557
  decisions.md         sha256 b2a8ca183122dd3bf4d202409db5a7d753f89e7797de0df38412518556a130a9
  block.md             this block (save it; report its digest)
CODE — diffs built at `ec4e2e86` and `db9a05cc`, which the reviewer applied in this order at
`db9a05cc`, ran and red-proved in its own worktree. Apply with `git apply`; never edit a hunk:
  `.remedy-wt/f273-proto-t010a.diff` sha256 9409ae31de1b25f05140c2c437e4a25b936363e8be0a4f1d27cc9c87d619aa68
  `.remedy-wt/f273-proto-t010b.diff` sha256 7a2d412d8b20881a087b434ca65c4f9898586b84e9e44402cb2135c73e66e77b
  `.remedy-wt/f273-proto-t007.diff`  sha256 772c7029707c25005ce386762678d1a496d3e5cfffdfe0fcdf5b31a3a952e9b3
  `.remedy-wt/f273-r9/f267.diff`     sha256 b15556c286d3ccbe6b8a02fdbb3902463aadc5b22471aea582687dc43b958b58

Bundle (commit order):
C1 bookkeeping — one commit holding exactly: byte copies of every payload above as
   `.agent/authored/f273-r9-<name>`; `.agent/plan.md` := plan.md; `.agent/live_review.md` and
   `.agent/decisions.md` := each one's `db9a05cc` bytes + ledger.md and decisions.md respectively.
C2 R-0411 part 1 (fixture, bench template wiring, evidence digest) — `git apply` t010a.diff.
C3 R-0411 part 2 (the two orders) — `git apply` t010b.diff.
C4 R-0796 — `git apply` t007.diff, then `git apply` f267.diff, one commit.
   Before each code commit run `git status --porcelain` and stage every path the apply touched
   (new files included); nothing may be left untracked or unstaged.
C5 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 2 of feature F273 · round 9 · rounds so far 9" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C4; every gate's
   real output; open findings by distinct id (`count_open_findings`) on the committed ledger; one
   `Landed: R-xxxx` line naming its commit for each of R-0411 (C2 and C3) and R-0796, in the
   handoff only — never a `Done:` line of your own; `## Next` naming Phase 1 rule 1 then the
   review of round 9, and "Operator questions open: <the count you read from the file>". Then
   `git push`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test calls a real provider. The shell denies `VAR=x cmd`, `cp`, loops, `$( )`, `$VAR` and
   `cd` before git; use `git -C <path>` and small python scripts under `.remedy-wt/f273-r9/`
   (prefix yours `wk_`) with an explicit `cwd=`. Never use `git stash`: its stack is shared.
3. Never weaken an assertion or delete a test other than the changes the diffs carry. A red gate or
   an ambiguity D9 does not settle -> stop, commit nothing half-done, report.
4. Build every edited `.agent/` file from `git show db9a05cc:<path>` bytes.
5. Commit messages "F273 R9 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never list, read or write any `.data/` yourself. Never run `scripts/make_review_zip.sh` for real,
   never run the `remedy` CLI, a bench or gauntlet campaign, `run_job` or the self-use runner, and
   create no branch.

Done when (G1 to G5 at C4, before C5; report literal output and the real exit code):
G1 transport + state + path sets: every payload and diff digest matched; a python check prints
   True that `.agent/plan.md` equals its payload, that `.agent/live_review.md` and
   `.agent/decisions.md` each equal their `db9a05cc` bytes + ledger.md and decisions.md, that each
   `.agent/authored/f273-r9-*` copy equals its payload, and that `git show --name-only --format=`
   of C2 and of C3 each lists exactly the paths `git apply --numstat` reads from its diff, and of
   C4 exactly the union of the paths of t007.diff and f267.diff.
G2 code transport: `git rev-parse <C4>:tests <C4>:packages <C4>:scripts <C4>:docs <C4>:apps
   <C4>:pyproject.toml` prints exactly e3f1e31676ef32f3b2c2dfedd7a3af6ff1d5fdad,
   2d5e2ac415e5fa1047098f60943ca49dacab4766, be7597b0b73946138a69c98d427fbd1c5873c51c,
   1d9ff5b4eaa1462d91d455153cfeba2b831af225, a067589349e82f806957e9fef44aca6ee642fed2 and
   93acca6ef06eaa797e65333658003f3c11289e97 (the reviewer's dry-run objects).
G3 in the primary checkout, serial (no `-n`): `python3 -m pytest -q -p no:cacheprovider
   tests/orchestration/test_bench_dry_run.py tests/orchestration/test_bench_history.py
   tests/orchestration/test_bench_model_context.py tests/orchestration/test_bench_never_runs_implicitly.py
   tests/orchestration/test_bench_orders.py tests/orchestration/test_bench_run.py
   tests/orchestration/test_bench_sample_project.py tests/orchestration/test_capability_bench.py
   tests/orchestration/test_gauntlet_evaluator.py tests/orchestration/test_gauntlet_evidence.py
   tests/orchestration/test_gauntlet_injection.py tests/orchestration/test_gauntlet_matrix.py
   tests/orchestration/test_gauntlet_orders.py tests/orchestration/test_gauntlet_runner.py
   tests/orchestration/test_self_run_gauntlet.py tests/cli/test_event_list_cmd.py
   tests/cli/test_change_proof_cli.py tests/cli/test_mission_cmd.py
   tests/cli/test_real_test_execution_cli.py tests/docs/ tests/test_no_orphan_modules.py
   tests/cli/test_advertised_commands.py tests/cli/test_cli_ux.py tests/cli/test_command_catalog.py
   tests/cli/test_scoped_listings.py tests/test_command_catalog.py tests/test_command_discovery.py
   tests/test_grouped_cli.py tests/orchestration/test_list_options.py
   tests/orchestration/test_import_reachability.py tests/ui_server/test_dashboard_contract.py
   tests/cli/test_golden_path.py` -> summary line, 0 failed, exit 0, no `R-0803:` line.
G4 `python3 -m ruff check . --output-format concise` from the primary checkout's root ->
   "All checks passed!", exit 0.
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C4, run from its root
   with `python3 -B -m pytest -q -p no:cacheprovider`, `__pycache__` purged before each run, the
   imported `packages.orchestration.bench_run` path printed first to prove it resolves inside the
   worktree. The UNMUTATED control first over the test files named below (exit 0). Then, each
   reverted from its saved bytes before the next, counting each FROM line (with its newline) in the
   named file first (each must be 1), naming the failing ids. B = the eight `test_bench_*` and
   `test_capability_bench.py` files of G3; N = `(lambda rows, **_: rows)(`.
   (a) `packages/orchestration/bench_run.py`:
   `        return materialise_sample_project(run_dir, template_dir=template_dir(run_dir))` ->
   `        return materialise_sample_project(run_dir)` -> B fails;
   (b) `packages/orchestration/gauntlet_runner.py`:
   `        "template_digest": _template_digest(template_dir),` ->
   `        "template_digest": _template_digest(),` -> B fails;
   (c) `scripts/bench_sample_project/benchproj/api.py`: `        if method != "GET":` ->
   `        if method not in ("GET", "POST"):` -> tests/orchestration/test_bench_sample_project.py fails;
   (d) `packages/orchestration/bench_orders.py`: `    _require(declared == actual_template,` ->
   `    _require(True,` -> B fails;
   (e) `apps/cli/commands/event.py`: `        result = apply_list_options(` -> `        result = N`
   -> tests/cli/test_event_list_cmd.py fails;
   (f) `apps/cli/commands/change.py`: `        changes = apply_list_options(` ->
   `        changes = N` -> tests/cli/test_change_proof_cli.py fails;
   (g) `apps/cli/commands/real_test_execution_cmd.py`: `        runs = apply_list_options(` ->
   `        runs = N` -> tests/cli/test_real_test_execution_cli.py fails;
   (h) `apps/cli/commands/mission_cmd.py`: `        rows = apply_list_options(` -> `        rows = N`
   -> tests/cli/test_mission_cmd.py fails.
   Report exit codes and failing ids, and a mutation that stays green as green. Remove the worktree
   and show `git worktree list`.
G6 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
