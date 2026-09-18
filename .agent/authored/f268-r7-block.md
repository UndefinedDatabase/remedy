-- STEP R7 T005 + R-0892 docs half -- F268 remedy do: the one-command start --
Session 2 of F268 · round 7 · base `8746b21e` (branch feature/f268-remedy-do, pushed).

Goal: book round 6's verdict; record DECISION F268 D15 (amends D14); land T005 — five
real quick-start lines in `remedy --help` and the README, with a test that runs them —
and R-0892's documentation half in `.claude/skills/remedy-evidence-review/SKILL.md`.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F268.md (T005, Acceptance);
payload `decisions.md` (DECISION F268 D15 binds this round); `apps/cli/grouped.py`
(`_QUICK_START`, `_print_root_help`); `tests/cli/test_cli_ux.py` (`TestHappyPath`,
`TestQuickStart`); `tests/test_cli_execution_loop_closure.py` (`test_quick_start_updated`,
`test_no_auto_commit_in_docs`); `tests/cli/test_do_sequence_cli.py` (its `repo` fixture and
the `no_model_call` tripwire — reuse the pattern); README.md `## Quickstart`.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f268-r7/`. Verify each
sha256 before use; any mismatch -> stop and report. Apply byte-exact.
  ledger.md          sha256 5cd7b3ded3156fe25a7c0ab43c586b382359cb4a371094ba099518424fac28ff
  decisions.md       sha256 d2d0b9a8300ef075a3e363673b95f7cd504e6df195cec3a07ec9545d6e7c722b
  plan.md            sha256 39084c4711f70950a327797b158bf1ab6821c4eaaeca439631dc69c9c4252c45
  quickstart_to.txt  sha256 782821135e1589d235deda909787456b08c65d1b4923d1b5a58333a756062186
  readme_to.txt      sha256 2ce89dbc5b88067583b4748defa268e232193f4c8a594cb4104f37517875455e
  skill.md           sha256 4a6bf8da8b59f9dac84ae9e183205fbfb08d84fbf0d9e8274da4d4d59494ccc8
  block.md           this block (save it as `.agent/authored/f268-r7-block.md`; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of every payload above as
   `.agent/authored/f268-r7-<name>`; `.agent/live_review.md` := `git show
   8746b21e:.agent/live_review.md` bytes + ledger.md; `.agent/decisions.md` :=
   `git show 8746b21e:.agent/decisions.md` bytes + decisions.md; `.agent/plan.md` := plan.md.
C2 T005 — production and pins, one commit:
   (a) in `apps/cli/grouped.py`, replace the whole `_QUICK_START = """\` assignment (from
       that line through the line ending `remedy --all-commands"""`) with the bytes of
       quickstart_to.txt; nothing else in the file changes.
   (b) in README.md, replace the fenced ```bash block directly under `## Quickstart` (its
       opening fence line through its closing fence line) with the bytes of readme_to.txt;
       nothing else in the file changes.
   (c) the pins this change turns red BY DESIGN — measured by the reviewer's dry run at
       `8746b21e` with (a) and (b) applied: `TestHappyPath::test_happy_path_in_help`,
       `TestQuickStart::test_quick_start_has_auto_job_id`,
       `TestQuickStart::test_quick_start_no_manual_job_id` (tests/cli/test_cli_ux.py) and
       `TestDocsHelpReviewMemoryCommands::test_quick_start_updated`
       (tests/test_cli_execution_loop_closure.py). Rewrite each to assert the NEW content
       (e.g. `remedy do "Write a CONTRIBUTING.md"` and `remedy job list` in the help; no
       `<...>` placeholder at all in `_QUICK_START`), never to assert less than before
       about what it pinned. `TestQuickStart::test_quick_start_has_tee` and
       `test_quick_start_flags_are_declared_by_their_commands` stay green by accident
       (the latter counts two `group sub` lines and never reads a `remedy do` line):
       replace `test_quick_start_has_tee` with a test that the quick start has exactly five
       numbered lines, and rewrite the flags test so it resolves EVERY numbered line to a
       catalog entry — a group word not followed by one of its subcommands resolves
       through `apps.cli.grouped._DEFAULT_COMMAND` (so `remedy do "Write …"` is
       `("do", "run")` and `remedy init` is `("init", "run")`) — and checks every flag on
       it is declared.
C3 T005 test — new `tests/cli/test_quick_start.py`, one commit: per DECISION F268 D15, on a
   fixture git repository (one committed file, `REMEDY_DATA_DIR` via monkeypatch, chdir via
   monkeypatch, the `no_model_call` tripwire), read the numbered lines from the output of
   `apps.cli.grouped.main([])`, run each in order in-process through `main` with
   `shlex.split(line)[1:]`, appending exactly `--builder-provider fake --reviewer-provider
   fake --no-llm --no-ui` to each line whose first word after `remedy` is `do` and nothing
   to any other; assert every line exits 0 (SystemExit code 0 or None counts as 0) and
   that the target's `git status --porcelain` after line five equals its reading after
   line one. A second test asserts the executed argv of each line equals its printed words
   plus that suffix for `do` lines and nothing else.
C4 R-0892 docs half: replace `.claude/skills/remedy-evidence-review/SKILL.md` with the
   bytes of skill.md, one commit. Try the Edit or Write tool. If the permission system
   refuses the write, do NOT route around it by any shell command: skip C4, and in C5 add
   an entry to `.agent/operator_questions.md` per docs/agents/self_drive_protocol.md
   amendment amend0911-feedback rule C, kind (A), asking the operator to apply the payload
   (quote its path under `.agent/authored/` and its sha256 in your handoff, NOT in the
   entry body, which carries no file paths); the entry's "What happens if you say
   nothing" says the skill page keeps describing the deleted writer.
C5 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md:
   "SESSION 2 of feature F268 · round 7 · rounds so far 7"; per-commit tables with
   `git show --numstat` counts for C1–C4; every gate's real output; `Landed:` lines in the
   HANDOFF only (never `Done:`, never in the ledger) for T005 and, if C4 landed, R-0892.
   Then `git push` (never force).

Constraints:
1. Change set: only the paths the Bundle names (plus `.agent/operator_questions.md` only in
   the C4-refused case). Every commit < 500 changed lines.
2. No test calls a real provider, starts a UI server or reads real stdin; env vars only via
   `monkeypatch.setenv`; the shell denies `VAR=x cmd` and `cp` — copy bytes with python.
3. Never weaken an assertion or delete a test to pass, beyond the by-design rewrites C2(c)
   names. A red gate you can repair inside this change set without touching a DECISION:
   repair it in its own commit and name it in the handoff. Anything else: stop and report.
4. Build every appended file from `git show 8746b21e:<path>` bytes plus the payload.
5. Commit messages "F268 R7 C<n>: <summary>", blank line,
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Do not touch docs/roadmap/features/T2_F268.md, `role_config.py` or `pingpong_job.py`.

Done when (run each after C4, before C5; report literal output + real exit code):
G1 transport + state: every payload digest matched; python byte checks print True for both
   appends against their `8746b21e` bytes; `.agent/plan.md` byte-equal to plan.md; grouped.py
   contains quickstart_to.txt's bytes exactly once and README.md contains readme_to.txt's
   bytes exactly once; `git diff --numstat 8746b21e -- apps/cli/grouped.py README.md`.
G2 `python3 -m pytest -q -p no:cacheprovider tests/cli/test_quick_start.py
   tests/cli/test_cli_ux.py tests/test_cli_execution_loop_closure.py
   tests/cli/test_advertised_commands.py tests/cli/test_do_sequence_cli.py
   tests/cli/test_golden_path.py tests/docs/` -> 0 failed.
G3 `python3 -m ruff check apps/cli/grouped.py tests/cli/test_quick_start.py
   tests/cli/test_cli_ux.py tests/test_cli_execution_loop_closure.py` -> "All checks passed!".
G4 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at the C4 commit (or
   C3's if C4 was skipped), run from the worktree root with `python3 -B -m pytest -q
   -p no:cacheprovider tests/cli/test_quick_start.py tests/cli/test_cli_ux.py`,
   `__pycache__` purged before each run, the imported `apps/cli/grouped.py` path printed
   first; unmutated control first (exit 0); each mutation in `apps/cli/grouped.py` only,
   reverted before the next: (a) `  5. remedy job list` -> `  5. remedy job lst` -> a
   test_quick_start.py test red; (b) `CONTRIBUTING.md" --plan-only` ->
   `CONTRIBUTING.md" --plan-everything` (NOT the `"--plan-only",` entry of the bare-flag list,
   which this string does not match) -> at least the flags test red; (c) `  4. remedy do "Write a CONTRIBUTING.md"\n` -> the same line with ` --apply`
   before its newline -> the git-status test red. Report exit codes and failing ids; remove
   the worktree; show `git worktree list` and the `remedy/job-*` branch count before and after.
G5 `git status --porcelain` empty and the local tip equals origin after the push.
Full suite: NOT run (amend0917-throughput).
-- end of block --
