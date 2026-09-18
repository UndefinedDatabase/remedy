-- STEP R4 T004 (do) -- F270 History apply: one commit per task, merge on demand --
Session 1 of F270 · round 4 · base `8e9c2fad` (branch feature/f270-history-apply, pushed).

Goal: the `do` half of T004 — `remedy do` takes `--commit "<message>"`, `--commit-auto`,
`--commit-with-history` and `--push`, chains its jobs under a commit flag, pushes once per
mission, honours `apply.push_after_mission`, and a push waits only for a red blocking criterion.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F270.md; the payload `decisions.md`
(DECISION F270 D4 — this round's spec; where this block is terser, it rules); DECISIONs F270 D1
to D3 and F268 D12 in `.agent/decisions.md`; `packages/orchestration/do_sequence.py` whole.
REFERENCES, not slices: `.remedy-wt/f270-r4/prototype.diff` and
`.remedy-wt/f270-r4/prototype_test_do_commit_flags.py` are a research helper's prototype at
`8e9c2fad` (it measured 0 failures over this round's do and apply files and every behaviour red
when disabled); it predates D4 (3)'s per-job messages, D4 (6)'s red rule and the `--plan-only`
refusal. Read it, write your own code, and copy nothing blindly.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f270-r4/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md               sha256 21baab005f089e9387c642981c3fdce989247a4dcff5e2ac3f2759624a805e45
  decisions.md            sha256 b37f1937b6ee5fb750ffc6f1bdc02f328c62e922f24464aa70e1279806f5d94e
  plan.md                 sha256 b9fd817321cc57980754871cabe37352c93d3a4777c557e3a593117551aa1c96
  operator_questions.md   sha256 e75ae05136b0d7c8925a61451e17ef476b172bac2dd6a5811a0149d2237ff4f1
  f273_from.txt           sha256 12836298cade1590365a62299e2982ae510e7cc314f1b1c6b9c2b5da0a75e9b7
  f273_to.txt             sha256 493a8b8993b45c4805d573c6d9a2a58d535f6d7f334d6ed1ffdae96f4e9a9aa3
  block.md                this block (save it in C1 with the others; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of EVERY payload above, the block included, as
   `.agent/authored/f270-r4-<name>`; `.agent/live_review.md` := its `8e9c2fad` bytes + ledger.md
   (round 3's verdict, `Done: R-0975`, `Done: R-0976`, R-0977); `.agent/decisions.md` := its
   `8e9c2fad` bytes + decisions.md; `.agent/plan.md` := plan.md; `.agent/operator_questions.md` :=
   operator_questions.md (it merges two low-impact entries into one and adds the entry for D4 (6));
   `docs/roadmap/features/T2_F273.md`: the bytes of f273_from.txt replaced by f273_to.txt
   (reviewer's containment test: `TO contains FROM: True`, an APPEND — FROM 1x before and after,
   and the lines C1's diff adds to that file are exactly the TO-only lines, in order).
C2 the push rule and its reuse — D4 (6) in `packages/orchestration/job_apply.py`: a push refused
   while a blocking criterion of the mission is `unmet`, the `open` ones named in the output and the
   record; the push refusals and the push itself made callable without a `JobApplyResult` so `do`
   reuses them, `job apply`'s behaviour otherwise unchanged. Update the D3 (5) tests in
   `tests/orchestration/test_job_apply_commit.py` whose property D4 (6) changes: an `unmet`
   blocking criterion still refuses; an `open` one pushes and is named. Name each changed test and
   its reason in the handoff.
C3 `do` — D4 (1) to (5) and (7): `apps/cli/commands/do_cmd.py` (the flags, the before-any-step
   refusals with exit 2 and "Nothing was run.", the key's sentence), `do.run`'s ArgDef help in
   `apps/cli/command_catalog.py`, `packages/orchestration/do_sequence.py` (the chaining, the apply
   step's commit flag without push, the one mission push, `--json`'s `landed` and `push`), and
   `docs/guides/do-run-v1.md`. The four not-yet-available tests of
   `tests/cli/test_do_sequence_cli.py` are replaced by tests of the behaviour D4 gives those flags,
   never deleted without a replacement. Split into C3a/C3b if over 500 inserted lines.
C4 tests — a new `tests/cli/test_do_commit_flags.py`, at least: `--commit "Add the contact page"`
   → one commit with that first line and the trailers; `--commit-auto` → one commit passing D3
   (4)'s rule; `--commit-with-history` → a merge commit; a lone `--push`, two commit flags, a commit
   flag with `--plan-only`, a dirty tree and, with `--push`, no upstream → each exit 2 before any
   step, nothing written; `--push` to a bare fixture remote → exactly ONE push per `do` run, a
   fast-forward, recorded by the remote's update hook; `apply.push_after_mission` with `--commit` →
   one push without `--push`; the key with no commit flag → no commit, no push, the sentence on
   stderr; plain `do` and `do --apply`, the key on and off → the operator's `HEAD` unchanged and no
   push; an `unmet` blocking criterion → refused before anything is applied; an `open` one → pushed
   and named in `--json`; a remote refusing the push → the commit stays, exit 1; a two-job walk
   under `--commit` → two linear commits, suffixed `(job 1 of 2)` and `(job 2 of 2)`, the second
   job's worktree cut from the first commit, one push; `apply_job` never receives a push.
C5 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: "SESSION 1 of
   feature F270 · round 4 · rounds so far 4" plus one sentence of context self-assessment;
   per-commit tables with `git show --numstat` counts for C1 to C4; every gate's real output; open
   findings by distinct id; `## Next` naming Phase 1 rule 1 then the review of round 4, and
   "Operator questions open: <the count you read from the file>". Then `git push`.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. Do-not-touch (T2_F270.md): the apply gate's approval semantics, the snapshot guard, the
   worktree lifecycle beyond committing on it. No existing gate is removed or relaxed beyond D4
   (6); nothing force-pushes; nothing runs `git reset` on the operator's branch; without a commit
   flag `do` behaves exactly as at `8e9c2fad`.
3. No test calls a real provider or a network remote; remotes are bare repositories under
   `tmp_path`. The shell denies `VAR=x cmd` and `cp`; use python; set environment in tests with
   `monkeypatch.setenv`.
4. Never weaken an assertion or delete a test to pass. A red gate or an ambiguity D4 does not
   settle → stop, commit nothing half-done, report.
5. Build every edited `.agent/` and `docs/roadmap/` file from `git show 8e9c2fad:<path>` bytes.
6. Commit messages "F270 R4 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.

Done when (G1 to G4 at C4, before C5; report literal output and the real exit code):
G1 transport + state: every payload digest matched; a python check prints True that
   `.agent/plan.md` and `.agent/operator_questions.md` equal their payloads, that
   `.agent/live_review.md` and `.agent/decisions.md` equal their `8e9c2fad` bytes + ledger.md and +
   decisions.md, that T2_F273.md equals its `8e9c2fad` bytes with the pair applied, and that each
   `.agent/authored/f270-r4-*` copy, the block's included, equals its payload.
G2 `python3 -m pytest -q -p no:cacheprovider tests/cli/test_do_commit_flags.py
   tests/cli/test_do_sequence_cli.py tests/cli/test_do_flags.py tests/cli/test_do_cmd_summary.py
   tests/orchestration/test_do_sequence.py tests/orchestration/test_do_run.py
   tests/cli/test_product_spine.py tests/orchestration/test_job_apply_commit.py
   tests/orchestration/test_job_apply_history.py tests/orchestration/test_job_apply.py
   tests/orchestration/test_mission_contract.py tests/orchestration/test_config.py
   tests/cli/test_config_cmd.py tests/test_help_renderer.py tests/cli/test_cli_ux.py
   tests/cli/test_golden_path.py tests/test_command_catalog.py tests/cli/test_advertised_commands.py
   tests/test_subprocess_timeouts.py tests/orchestration/test_import_reachability.py tests/docs/
   tests/orchestration/test_roadmap_index.py tests/ui_server/test_dashboard_contract.py
   tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py` plus any other
   test file this round edited → summary line, 0 failed (serial, no `-n`; the reviewer's base
   reading of this list without the new file, at `8e9c2fad`, was 0 failed).
G3 `python3 -m ruff check` over every .py file C2 to C4 touched → "All checks passed!".
G4 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C4, run from the worktree
   root with `python3 -B -m pytest -p no:cacheprovider tests/cli/test_do_commit_flags.py
   tests/orchestration/test_job_apply_commit.py`, `__pycache__` purged before each run, the
   imported `do_sequence` module path printed first; the UNMUTATED control first (must be exit 0);
   each change below made, reverted before the next: (a) the before-any-step refusals skipped;
   (b) the lone-`--push` refusal disabled; (c) `--plan-only` accepted with a commit flag; (d) the
   key's push with a commit flag disabled; (e) the key made to commit without a commit flag; (f)
   the chaining disabled (jobs after the first wait again); (g) the apply step passes `push` to
   `apply_job`; (h) the `unmet` refusal disabled; (i) `open` made to block again; (j) the walk's
   push attempted after a stopped walk. Report each exit code and the failing ids; a mutation that
   stays green is reported as green, never papered over. Remove the worktree and show
   `git worktree list`.
G5 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
