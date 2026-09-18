-- STEP R8 the do flag list (R-0933) -- F268 remedy do: the one-command start --
Session 2 of F268 · round 8 · base `3c18ade2` (branch feature/f268-remedy-do, pushed).

Goal: book round 7's verdict; record DECISION F268 D16; make every `remedy do` walk the
sequence with exactly T2_F268.md's flag list as D16 rules it, which resolves R-0933.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F268.md (Design "Flags,
complete", Acceptance); payload `decisions.md` (DECISION F268 D16 binds this round, clause by
clause); R-0933 in `.agent/live_review.md` (grep `^- R-0933`); `apps/cli/grouped.py` (the
`do` parser args, `_DEFAULT_COMMAND` injection, the truly-bare detection and its bare-flag
lists); `apps/cli/commands/do_cmd.py` (`_cmd_do_order`, `_cmd_do`, `_cmd_job_run`'s budget and
role handling, `COMMAND_HANDLERS["do.run"]`); the `do.run` entry in
`apps/cli/command_catalog.py`; `packages/orchestration/do_sequence.py` (`DoContext`,
`_step_init`, `_step_plan`, `_step_shape`, `plan_order_job`, `_step_run`, `_provider_flags`);
`tests/cli/test_do_sequence_cli.py` (fixture and tripwire pattern).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f268-r8/`. Verify each
sha256 before use; any mismatch -> stop and report. Apply byte-exact.
  ledger.md     sha256 d33becb67901bd72ec5a3cb8443bb96960fdcd59fd74ffe74d25817248b45207
  decisions.md  sha256 ed8c331e2890e0106a3c7afc87eca4c9f78e49847f7cc5b97c1dc8875e7c4cf9
  plan.md       sha256 b8b046bd9c823c718a88e65fc2fc382bf32591a5a02b7984f17a3061bcda10cd
  opq.md        sha256 04536a0fd56f880c51f62f4ad6edb59295bb42052a3f822df6fd4c2914b511b1
  block.md      this block (save it as `.agent/authored/f268-r8-block.md`; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of every payload above as
   `.agent/authored/f268-r8-<name>`; `.agent/live_review.md` := `git show
   3c18ade2:.agent/live_review.md` bytes + ledger.md; `.agent/decisions.md` := `git show
   3c18ade2:.agent/decisions.md` bytes + decisions.md; `.agent/operator_questions.md` :=
   `git show 3c18ade2:.agent/operator_questions.md` bytes + opq.md; `.agent/plan.md` := plan.md.
C2 D16 clauses (4) to (7) — production + tests (split production and tests into two commits
   if one would exceed 500 insertions). SPEC, in D16's words: `DoContext` carries the
   `--project` selector, the resolved budgets (only when a budget flag was given), and the
   builder, reviewer and planner models; `_cmd_do_order` validates the two role models with
   `_validate_role_override` and resolves the budget flags with `resolve_job_budgets(cli_…,
   project_root=repo)` BEFORE `walk_do_sequence` (an error exits 2, nothing registered or
   run); `_step_init` with a selector uses `select_project(selector, repo)`, and on
   `ProjectNotFoundError` returns DO_STEP_FAILED naming the selector; `_step_run` passes
   `budgets=`, `builder_model=`, `reviewer_model=` to `run_job`; `_provider_flags` (or its
   successor) adds `--builder-model`/`--reviewer-model` to every `remedy job run` Next line;
   `--planner-model` reaches `model=` of every `make_structured_call_fn` the plan and shape
   steps build (`plan_order_job`'s intake and task-plan calls included — read how they build
   theirs). Add `--builder-model`, `--reviewer-model`, `--planner-model` to the `do.run`
   catalog entry and the `do` parser. Tests in a NEW `tests/cli/test_do_flags.py` (fixture
   pattern of test_do_sequence_cli.py, `--no-ui` always, fake providers): `--project <slug>`
   of a project `remedy init` registered walks and the job's project is it; an unknown
   `--project` exits 1 with the init step failed and no mission created;
   `--max-total-tokens 100000` is the job's recorded `max_total_tokens`; an invalid budget
   value exits 2 and leaves the repository unregistered; `--builder-model m1
   --reviewer-model m2` are the job's recorded `execution_config` models with source `cli`
   and appear on the `--plan-only` Next line; `--planner-model p1` WITHOUT `--no-llm`, with
   `intake.make_structured_call_fn` monkeypatched to a recorder that returns None and
   `study.study_call_fn` monkeypatched to return None (the study role has its own model),
   reaches every recorded call as `model="p1"` (and at least one call is recorded).
C3 D16 clauses (1) to (3) and R-0933 — one commit (or production and tests split as C2):
   delete the truly-bare detection in `grouped.py` and the autorun branch of `_cmd_do` (the
   `dry_run`, `run_do`, `select_project`/`attach_job` tail) so `do.run` always calls the
   sequence; remove `--autonomy-level`, `--max-cycles`, `--ui`, `--dry-run` from the catalog
   entry, the parser, the handler and the dispatch lambda; keep `--no-llm`. Do NOT delete
   `run_do`, `export_do_run_json`, `summarize_do_run`, `dry_run_autorun` or their modules —
   the next round does. Tests pinning the deleted routing or flags are deleted or rewritten
   BY DESIGN; the reviewer's research helper found them at `8746b21e`: the whole of
   `tests/cli/test_do_runtime.py`; in `tests/cli/test_job_commands.py`
   `test_dry_run_no_side_effects`, `test_dry_run_phases_by_autonomy`, `test_do_direct_dry_run`,
   `test_do_run_alias_still_works`, `test_do_with_all_flags`; in `tests/cli/test_golden_path.py`
   `test_explicit_do_run_skips_golden_path`, `test_budget_flag_skips_golden_path`,
   `test_explicit_default_flag_skips_golden_path` (rewrite each to assert the NEW routing —
   the sequence runs); in `tests/test_cli_execution_loop_closure.py` the three
   `TestUiBooleanFlagParsing` tests and the `truly_bare` assertion near line 73. Verify each
   against its body before deleting; list every deleted or rewritten test in the handoff with
   its reason. Add to `tests/cli/test_do_flags.py`: an explicit `remedy do run "<order>"
   --builder-provider fake --reviewer-provider fake --no-llm --no-ui` walks the sequence and
   the job's recorded builder is `fake` with source `cli` (R-0933); each removed flag given
   to `remedy do "<order>"` exits 2. Docs: every line under README.md, docs/guides/,
   docs/system/ and scripts/ that shows a `remedy do` invocation with a removed flag is
   rewritten to the sequence's flags or removed (read `tests/cli/test_do_cmd_summary.py`
   `test_docs_do_commands_valid`, which checks `docs/guides/autocoder-usage.md`).
C4 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md:
   "SESSION 2 of feature F268 · round 8 · rounds so far 8"; per-commit tables with
   `git show --numstat` counts for every commit before C4; every gate's real output;
   `Landed:` lines in the HANDOFF only (never `Done:`) for R-0933. Then `git push`.

Constraints:
1. Change set: the paths the Bundle names, the test files it names, and the docs lines C3
   rewrites. Every commit < 500 inserted lines.
2. No test calls a real provider, starts a UI server or reads real stdin; env vars only via
   `monkeypatch.setenv`; the shell denies `VAR=x cmd` and `cp` — copy bytes with python.
3. Never weaken an assertion or delete a test to pass, beyond the by-design deletions and
   rewrites C3 names. A red gate you can repair inside this change set without touching a
   DECISION: repair it in its own commit and name it in the handoff. A red that contradicts a
   clause of D16, or a test outside C3's list that only the deleted routing could satisfy:
   stop and report.
4. Build every appended file from `git show 3c18ade2:<path>` bytes plus the payload.
5. Commit messages "F268 R8 C<n>: <summary>", blank line,
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Do not touch docs/roadmap/**, `role_config.py`, `.claude/**`, or `do_run.py`/`autorun.py`.

Done when (run each after the last code commit, before C4; report literal output + real exit code):
G1 transport + state: every payload digest matched; python byte checks print True for the
   three appends against their `3c18ade2` bytes; `.agent/plan.md` byte-equal to plan.md.
G2 `python3 -m pytest -q -p no:cacheprovider tests/cli/test_do_flags.py
   tests/cli/test_do_sequence_cli.py tests/cli/test_golden_path.py tests/cli/test_job_commands.py
   tests/test_cli_execution_loop_closure.py tests/cli/test_cli_ux.py tests/cli/test_quick_start.py
   tests/cli/test_advertised_commands.py tests/cli/test_do_cmd_summary.py
   tests/test_command_catalog.py tests/orchestration/test_do_run.py
   tests/cli/test_do_evidence_package.py tests/orchestration/test_import_reachability.py
   tests/docs/` plus every other test file this round edited -> 0 failed.
G3 absence, measured at `3c18ade2` AND at your last code commit, printing both counts:
   python regex over tracked files under apps/ packages/ tests/ for
   `truly_bare|_BARE_ALLOWED|_injected_default`; and over tracked README.md, docs/guides/,
   docs/system/, scripts/ lines containing `remedy do` for
   `--autonomy-level|--max-cycles|--dry-run|(?<![\w-])--ui\b`. The second reading must be 0.
G4 `python3 -m ruff check` over every .py file the round touched -> "All checks passed!".
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at the last code commit,
   `python3 -B -m pytest -q -p no:cacheprovider tests/cli/test_do_flags.py` from the worktree
   root, `__pycache__` purged before each run, the imported `do_sequence.py` path printed
   first; unmutated control first (exit 0); each mutation one unique byte string you quote
   with its file, reverted before the next: (a) `budgets=` not passed to `run_job` -> the
   budget test red; (b) `_step_init` ignores the selector -> an `--project` test red;
   (c) `builder_model=` not passed -> the model test red; (d) `--planner-model` not passed to
   `model=` -> the planner-model test red. (No mutation drops the builder provider: its
   default is a real Ollama provider, which constraint 2 forbids a test run to reach.)
   Remove the worktree; show `git worktree list` and the `remedy/job-*`
   branch count before and after.
G6 `git status --porcelain` empty and the local tip equals origin after the push.
Full suite: NOT run (amend0917-throughput).
-- end of block --
