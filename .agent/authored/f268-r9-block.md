-- STEP R9 D16 (1) to (3), R-0933 -- F268 remedy do: the one-command start --
Session 2 of F268 · round 9 · base `5243e0a6` (branch feature/f268-remedy-do, pushed).

Goal: book round 8's verdict; record DECISION F268 D17; land round 8's C3 — every
`remedy do` walks the sequence, the autorun branch and the four flags leave — which
resolves R-0933.

Read first, completely: AGENTS.md; `.agent/handoff.md` at `5243e0a6` (round 8's measured C3
dry run — you are that round's continuation); payload `decisions.md` (DECISION F268 D17) and
DECISION F268 D16 in `.agent/decisions.md`; the files round 8's block C3 named
(`.agent/authored/f268-r8-block.md`, its C3 item); `scripts/remedy_smoke.sh` sections `12ao`,
`12aq` and the UX smoke gate that reads `${REPAIR_JOB_ID}`.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f268-r9/`. Verify each
sha256 before use; any mismatch -> stop and report. Apply byte-exact.
  ledger.md     sha256 4431cb8a4d782e662ac52cc4d2636014c26aea1914deea1c0e17f84a0c4825ac
  decisions.md  sha256 5d4ace053210bf2a63480b6ea3c9fd626b593feb1d7239b216982b6a375e9708
  plan.md       sha256 c858f18499085caf9344fdd48b81f4bc91c9a93b9bc7c31ac9c07656bcc90906
  block.md      this block (save it as `.agent/authored/f268-r9-block.md`; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of every payload above as
   `.agent/authored/f268-r9-<name>`; `.agent/live_review.md` := `git show
   5243e0a6:.agent/live_review.md` bytes + ledger.md; `.agent/decisions.md` := `git show
   5243e0a6:.agent/decisions.md` bytes + decisions.md; `.agent/plan.md` := plan.md.
C2 production — D16 (1) and (2), one commit. You may start from round 8's worker patch
   `.remedy-wt/f268-r8/c3_production_dryrun.patch` (sha256
   813ff65ac6ca806022d214e3ed18daa1cb5ab2716b1cb85cf7339b258f8539a8; it applies with
   `git apply -3` at `5243e0a6`), which deletes the truly-bare detection and `_did_inject`'s
   use for it in `grouped.py`, the three parser branches only `do` used, the four ArgDefs,
   and `_cmd_do`'s autorun branch and parameters. Two changes to it: `--no-ui`'s help must
   not contain the word `job` (the reviewer's dry run showed
   `tests/docs/test_vocabulary.py::test_every_binding_word_in_a_description_carries_the_pages_meaning`
   red on "for the job that ran"; "Do not open the cockpit" is enough), and `--project`'s
   help ("Project ID to use or create (its repo)") becomes what D16 (4) does: select a
   registered project by slug or id instead of the repository's own.
C3 tests and smoke — one commit (split if over 500 insertions):
   (a) deleted BY DESIGN, each checked against its body first: the whole of
   `tests/cli/test_do_runtime.py`; `tests/cli/test_job_commands.py`
   `TestDoDirectGoalCommandRewrite::test_do_direct_dry_run`, `::test_do_run_alias_still_works`,
   `::test_do_with_all_flags`; `tests/test_cli_execution_loop_closure.py` the three
   `TestUiBooleanFlagParsing` tests; `tests/orchestration/test_autorun.py`
   `TestCalcFixtureBuilderWithProof::test_no_ui_suppresses_ui` (D17 (1)).
   (b) rewritten BY DESIGN to the new routing, never asserting less: `tests/cli/test_golden_path.py`
   `TestDoMission::test_explicit_do_run_skips_golden_path` and
   `::test_explicit_default_flag_skips_golden_path` (the sequence runs);
   `tests/test_cli_execution_loop_closure.py` `TestDoProviderCliParsing::test_default_command_rewrite`
   (drop only its `truly_bare` assertion); `tests/cli/test_job_commands.py`
   `TestRemedyDo::test_do_command_in_catalog` asserts `may_mutate_repo is True` (D17 (3));
   `test_smoke_has_repair_loop_section` becomes a pin of the new `12ao` (its `remedy do`
   line carries `--no-llm`, and `--autonomy-level` appears nowhere in the script).
   (c) `scripts/remedy_smoke.sh` section `12ao` per D17 (2): `git init` a fixture with one
   commit under `${TMP_REPAIR}` (rename the variable if you like), the `remedy do "Make tests
   pass" --repo <fixture> --builder-provider fake --reviewer-provider fake --no-llm --no-ui
   --json` line, the checks D17 (2) names; `REPAIR_JOB_ID` becomes `DO_JOB_ID` at every use.
   (d) docs: `docs/guides/autocoder-usage.md` lines 22, 47 and 97 and `docs/guides/do-run-v1.md`
   line 19 at `5243e0a6` (round 8's G3 docs hits) show only flags `do` still has; read
   `tests/cli/test_do_cmd_summary.py` `test_docs_do_commands_valid` first.
   (e) add to `tests/cli/test_do_flags.py`: an explicit `remedy do run "<order>"
   --builder-provider fake --reviewer-provider fake --no-llm --no-ui --json` walks the
   sequence (its JSON has `mission_id` and a `steps` list) and the job's recorded
   `execution_config` builder is `fake` with source `cli` (R-0933); each of `--autonomy-level
   1`, `--max-cycles 1`, `--ui`, `--dry-run` given to `remedy do "<order>"` exits 2 (parametrize).
C4 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md:
   "SESSION 2 of feature F268 · round 9 · rounds so far 9"; per-commit tables with
   `git show --numstat` counts for every commit before C4; every deleted or rewritten test
   named with its reason; every gate's real output; a `Landed:` line in the HANDOFF only
   (never `Done:`) for R-0933. Then `git push`.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test calls a real provider, starts a UI server or reads real stdin; env vars only via
   `monkeypatch.setenv`; the shell denies `VAR=x cmd` and `cp` — copy bytes with python.
3. Never weaken an assertion or delete a test to pass beyond C3 (a) and (b). A red you can
   repair inside this change set without touching a DECISION: repair it in its own commit and
   name it. Any other red, or a test outside C3's lists that only the deleted routing could
   satisfy: stop and report.
4. Build every appended file from `git show 5243e0a6:<path>` bytes plus the payload.
5. Commit messages "F268 R9 C<n>: <summary>", blank line,
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Do not touch docs/roadmap/**, `.claude/**`, `do_run.py`, `autorun.py`, `do_sequence.py`.

Done when (run each after the last code commit, before C4; report literal output + real exit code):
G1 transport + state: every payload digest matched; python byte checks print True for both
   appends against their `5243e0a6` bytes; `.agent/plan.md` byte-equal to plan.md.
G2 `python3 -m pytest -q -p no:cacheprovider tests/cli/test_do_flags.py
   tests/cli/test_do_sequence_cli.py tests/cli/test_golden_path.py tests/cli/test_job_commands.py
   tests/test_cli_execution_loop_closure.py tests/cli/test_cli_ux.py tests/cli/test_quick_start.py
   tests/cli/test_advertised_commands.py tests/cli/test_do_cmd_summary.py
   tests/test_command_catalog.py tests/orchestration/test_do_run.py
   tests/orchestration/test_autorun.py tests/cli/test_do_evidence_package.py
   tests/cli/test_mission_cmd.py tests/cli/test_plan_approval.py tests/cli/test_scoped_listings.py
   tests/test_install_smoke.py tests/test_remedy_smoke_script.py
   tests/orchestration/test_import_reachability.py tests/docs/` -> 0 failed.
G3 absence at `5243e0a6` AND at your last code commit, both counts printed: the regex of round
   8's G3 (`.remedy-wt/f268-r8/g3.py`, code reading and docs reading) — the second commit's
   code reading and docs reading must both be 0 — and `REPAIR_JOB_ID` in
   `scripts/remedy_smoke.sh` (0 at the second).
G4 `python3 -m ruff check` over every .py file the round touched -> "All checks passed!".
G5 (a) the smoke replacement, run for real: a scratch python script that builds a fixture git
   repository, sets `REMEDY_DATA_DIR` in its own `os.environ`, and runs the new `12ao`
   `remedy do` command and the `12aq` `remedy memory candidates` command as argv lists through
   `[sys.executable, "-m", "apps.cli.grouped", ...]` (the entry point `remedy` maps to), and
   the UX smoke gate's checker through `[sys.executable, "-c", ...]`, each extracted from the
   committed script text with its variable substituted — report each exit code (all 0) and
   the checker's printed line. (b) mutation red-proof in ONE
   disposable worktree under `.remedy-wt/` at the last code commit, `python3 -B -m pytest -q
   -p no:cacheprovider tests/cli/test_do_flags.py` from its root, `__pycache__` purged, the
   imported `do_cmd.py` printed; control first (exit 0); then re-add
   `ArgDef("--dry-run", …)` to the `do.run` entry and its parser handling so `--dry-run` parses
   -> the parametrized removed-flag test red for `--dry-run`. Remove the worktree; show
   `git worktree list` and the `remedy/job-*` branch count before and after.
G6 `git status --porcelain` empty and the local tip equals origin after the push.
Full suite: NOT run (amend0917-throughput).
-- end of block --
