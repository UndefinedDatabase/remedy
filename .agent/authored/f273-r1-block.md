-- STEP R1 T001 -- F273 Findings paydown v1 --
Session 1 of F273 · round 1 · base `80f7c529` (main, the merge of pull request 259).

Goal: claim F273, book F271 round 6's verdict, land DECISION F273 D1, and build R-0803, R-0804 and
R-0810 of T001 exactly as the reviewer's dry run built them.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F273.md; the payload `decisions.md`
(DECISION F273 D1 — this round's spec; where this block is terser, it rules).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f273-r1/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  plan.md              sha256 fffaa530fe3684cdfa72d87b6a69e0002decce5b02d9df31d707d2df3cdba2d0
  context.md           sha256 efd3d12df8c5eb4a41e3c04cc69a0898738edc0db35882f26d1f9d70d4b51c41
  live_review_head.md  sha256 b5e350a7f8c652f3e12455fa5fe2318bd8fa3b67c7ebb565794de66a6946e1d0
  ledger.md            sha256 40687b55c52b0efc61b58e9dbee85b245282056c160aac07148a6058733bad28
  decisions.md         sha256 8a89bedc2f645c4f274585a1c748d283870c980acdd542e09b32656ba9eef8b8
  status_from.txt      sha256 1d697c44cb046b2f1f07b3824214bca92ce75f81e609d88c34d40ba953fe5da7
  status_to.txt        sha256 80b01c2bba19fb1422220b928352738595cf8f11e0d0a111dfd52fe6dd0f8f86
  block.md             this block (save it; report its digest)
CODE — two diffs a research helper built at `80f7c529`, which the reviewer re-applied, ran and
red-proved in its own worktree. Apply them with `git apply`; do not retype or edit a hunk:
  `.remedy-wt/f273-proto-r0803.diff` sha256 0ce6d6238085ab730ff8560bb3e1055211de1cca902970744fa7e8e5995315fd
  `.remedy-wt/f273-proto-t001b.diff` sha256 6c46caa8923c8e560c94232ed5e4347e06b1e959c1e46ca062b8895adb2e16e8

Bundle (commit order):
C1 claim — branch `feature/f273-findings-paydown-v1` from `main` at `80f7c529` (the reviewer
   already ran the Open PR Gate: it merged pull request 259; zero pull requests are open). One
   commit holding exactly: byte copies of every payload above as `.agent/authored/f273-r1-<name>`;
   `.agent/plan.md` := plan.md; `.agent/context.md` := context.md; `.agent/live_review.md` :=
   live_review_head.md bytes + the old file's bytes from the line `## Findings` (inclusive) to the
   end + ledger.md bytes (it books F271 round 6's verdict); `.agent/decisions.md` := old bytes +
   decisions.md bytes; `docs/roadmap/STATUS.md`: the line equal to status_from.txt replaced by
   status_to.txt (reviewer's containment test: `TO contains FROM: False`, a REWRITE — FROM 1x
   before, 0x after, TO 1x after).
C2 R-0803 — `git apply .remedy-wt/f273-proto-r0803.diff` (`tests/conftest.py`,
   `tests/test_data_root_isolation.py`).
C3 R-0804 — `git apply --include=tests/ui_server/test_handler_table_walk.py
   .remedy-wt/f273-proto-t001b.diff`.
C4 R-0810 — `git apply --include=packages/orchestration/pingpong_loop.py
   --include=tests/orchestration/test_pingpong_cli.py .remedy-wt/f273-proto-t001b.diff`.
C5 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 1 of feature F273 · round 1 · rounds so far 1" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C4; every gate's
   real output; open findings by distinct id AND by the canonical line formula
   (`scripts/rotate_live_review.py::count_open_findings`), measured on the committed ledger; a
   line `Landed: R-0803`, `Landed: R-0804` and `Landed: R-0810` each naming its commit (in the
   handoff only — never a `Done:` line anywhere); `## Next` naming Phase 1 rule 1 then the review
   of round 1, and "Operator questions open: <the count you read from the file>". Then
   `git push -u origin feature/f273-findings-paydown-v1`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test calls a real provider. The shell denies `VAR=x cmd`, `cp` and compound commands; copy
   bytes and read exit codes with small python scripts under `.remedy-wt/f273-r1/`.
3. Never weaken an assertion or delete a test. A red gate or an ambiguity D1 does not settle ->
   stop, commit nothing half-done, report.
4. Build every edited `.agent/` and `docs/` file from `git show 80f7c529:<path>` bytes.
5. Commit messages "F273 R1 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never list, read or write `.data/` yourself. From C2 on, a pytest run in the primary checkout
   fingerprints the configured data root at start and end by D1 (1); that is the guard working.

Done when (G1 to G5 at C4, before C5; report literal output and the real exit code):
G1 transport + state: every payload and diff digest matched; a python check prints True that
   `.agent/plan.md` and `.agent/context.md` equal their payloads, that `.agent/live_review.md`
   equals head + the `80f7c529` bytes from `## Findings` + ledger.md, that `.agent/decisions.md`
   equals its `80f7c529` bytes + decisions.md, that STATUS equals its `80f7c529` bytes with the
   pair applied, and that each `.agent/authored/f273-r1-*` copy equals its payload.
G2 code transport: `git rev-parse <C4>:tests <C4>:packages` prints exactly
   d2b0f3a9544b4b9feee226c28db82bb60f2bc0da and e8c063e321a50f8990c9da4f9c673e8a6c33ee1b (the
   reviewer's dry-run subtrees), and `git diff --stat 80f7c529 <C4> -- tests packages` names
   exactly the paths C2 to C4 name.
G3 `python3 -m pytest -q -p no:cacheprovider tests/test_data_root_isolation.py
   tests/ui_server/test_handler_table_walk.py tests/orchestration/test_pingpong_cli.py
   tests/test_data_paths.py tests/test_grouped_cli.py
   tests/orchestration/test_manual_completion_bundle.py tests/ui_server/test_cockpit_contract.py
   tests/cli/test_golden_path.py tests/docs/ tests/orchestration/test_roadmap_index.py` in the
   primary checkout, serial (no `-n`) -> summary line, 0 failed, exit 0, no `R-0803:` line.
G4 `python3 -m ruff check tests/conftest.py tests/test_data_root_isolation.py
   tests/ui_server/test_handler_table_walk.py tests/orchestration/test_pingpong_cli.py
   packages/orchestration/pingpong_loop.py` -> "All checks passed!".
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C4, run from the worktree
   root with `python3 -B -m pytest -q -p no:cacheprovider`, `__pycache__` purged before each run,
   the imported `tests.conftest` and `packages.orchestration.pingpong_loop` paths printed first to
   prove they resolve inside the worktree. The UNMUTATED control first over the test files named
   below (exit 0). Then, each reverted before the next, counting the mutated bytes in the named
   file first (each must be 1): (a) in `tests/conftest.py` the line
   `    os.environ["REMEDY_DATA_DIR"] = str(tmp_path_factory.mktemp("remedy-data"))` replaced by
   `    pass` -> `tests/test_data_root_isolation.py` must fail, and `tests/test_grouped_cli.py` run
   alone must exit 1 printing an `R-0803:` line; (b) in `packages/orchestration/pingpong_loop.py`
   the two lines `if f"<!-- Remedy: {goal} -->" in content.splitlines():` and its `continue`
   deleted -> `tests/orchestration/test_pingpong_cli.py` must fail; (c) in
   `packages/orchestration/project_brain.py` `task.inputs` replaced by `task.inputz` ->
   `tests/ui_server/test_handler_table_walk.py` must fail. Report exit codes and failing ids, and
   a mutation that stays green as green. Remove the worktree and show `git worktree list`.
G6 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
