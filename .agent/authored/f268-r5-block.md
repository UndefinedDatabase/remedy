── STEP R5 R-0968/R-0969/R-0807 — F268 remedy do: the one-command start ──
Session 1 of F268 · round 5 · base `994f045a` (branch feature/f268-remedy-do, pushed).

Goal: book round 4's verdict and three findings; repair R-0968 (a follow-up job
runs on its predecessor's applied output) and R-0969; land R-0807's F268 half
(`do` prints measured tokens per role and cost; the builder's context size per
round reaches `context_strategy.json`).

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F268.md (Acceptance);
`packages/orchestration/do_sequence.py`; `packages/orchestration/job_evidence.py`
(`mirror_job_run_into_ledger`, the `context_strategy.json` writer);
`packages/orchestration/token_ledger.py` (`query_cost`); how `_cmd_job_run` in
`apps/cli/commands/do_cmd.py` mirrors cost; payload `ledger.md` (R-0968, R-0969,
R-0970) and payload `decisions.md` (DECISIONs F268 D10 and D11 bind this round).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f268-r5/`. Verify
each sha256 before use; any mismatch → stop and report. Apply byte-exact.
  ledger.md     sha256 226e35c47fbbb4122569894613a9cbd1fbaa5f9db145408f827e5599ac68b35b
  decisions.md  sha256 8d5f46c03ffbdfc58e268da1f4c033bad535d02560bac9a3069d4b1d9c6fecf0
  plan.md       sha256 f7090b5335da4e9aab155afb827770f73d96ca2e3a1033ceafac2b6191952d2d
  f273_line.md  sha256 f854c524e1d4d8bbf105a9f29ede438f7d235424fc92560eedb1990f67f6a2ec
  block.md      this block (save it; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of the payloads as
   `.agent/authored/f268-r5-<name>`; `.agent/live_review.md` := `git show
   994f045a:.agent/live_review.md` bytes + ledger.md; `.agent/decisions.md` :=
   `git show 994f045a:.agent/decisions.md` bytes + decisions.md;
   `.agent/plan.md` := plan.md; `docs/roadmap/features/T2_F273.md`: f273_line.md's
   bytes inserted immediately after the line that reads exactly
   `  text, run before the commit that saves it.` (the end of the R-0954 Acceptance
   item; that line occurs once in the file — check), nothing else in the file changes
   (amend0911-feedback rule A: R-0970's owner line lands with its registration).
C2 R-0968 + R-0969 — DECISION F268 D10 in `do_sequence.py`; R-0969 per its fix
   clause (`apps/cli/command_catalog.py` `do.run` `may_mutate_repo=True`; the pinned
   test in `tests/orchestration/test_do_run.py` renamed to what it asserts). Update
   the existing multi-job tests in `tests/cli/test_do_sequence_cli.py` whose pinned
   behaviour D10 changes BY DESIGN, each named in the handoff; add: (1) without
   `--apply`, `--force-mission` runs job 1 only, reports `stopped` with the apply
   command for job 1 and the `remedy job run` command for job 2 (real ids), job 2
   has no run; (2) with `--apply`, `--force-mission` on the stock fake provider
   (every build writes the same file — the case R-0968 measured) applies every job
   and exits 0, and job 2's workspace held job 1's applied output when it ran
   (assert on the target or on job 2's recorded base, whichever the code exposes —
   read it first).
C3 R-0807's F268 half — DECISION F268 D11: the run step mirrors each completed job
   (the same call `_cmd_job_run` makes); `do` prints one line per role with measured
   input, output and cache-read tokens and one cost line, read through
   `token_ledger.query_cost(..., job_id=<id>, by="role")` summed over the walk's
   jobs; `--json` adds `cost` with the same numbers and the ids of any job whose
   mirror failed; `context_strategy.json` gains the builder's reported input and
   cache-read tokens per task and round from the run's own evidence (read where
   `job_evidence` / `token_ledger.call_record_from_evidence` already find a call's
   usage — do not invent a second reader). Tests: in
   `tests/cli/test_do_sequence_cli.py`, a fake run's `--json` `cost` has a row per
   role that ran with the ledger's own numbers (compare against `query_cost` in the
   test); a failed mirror is named, not zero; in the nearest `job_evidence` test
   file, `context_strategy.json` for a fake job carries one builder entry per
   task-round with the usage the fake provider reported.
C4 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md:
   "SESSION 1 of feature F268 · round 5 · rounds so far 5"; per-commit tables with
   `git show --numstat` counts for C1–C3; every gate's real output; `Landed:` lines
   in the HANDOFF only (never `Done:`, never in the ledger) for R-0968, R-0969 and
   R-0807's F268 half. Then `git push`.

Constraints:
1. Change set: only paths the Bundle names plus test files C2–C3 edit. Every
   commit < 500 changed lines; split rather than exceed.
2. Do-not-touch (T2_F268.md): planner internals, the contract's shape, the apply
   gate's semantics (`job_apply.py` read only), the cockpit's content,
   `pingpong_job.run_job` (D10's alternative rejected), `token_ledger.py`'s
   recording and aggregation (read only).
3. No test calls a real provider, starts a UI server or reads real stdin; env vars
   only via `monkeypatch.setenv`; the shell denies `VAR=x cmd` and `cp`.
4. Never weaken an assertion or delete a test to pass. A red gate you can repair
   inside this change set without touching a DECISION: repair it in its own commit
   and name it in the handoff. Anything else: stop and report.
5. Build every appended file from `git show 994f045a:<path>` bytes plus the payload
   — never from a file you are writing.
6. Commit messages "F268 R5 C<n>: <summary>", blank line,
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.

Done when (run each at C3, before C4; report literal output + real exit code):
G1 transport + state: payload digests matched; python byte checks print True for
   both appends against their `994f045a` bytes and for `T2_F273.md` = its
   `994f045a` bytes with f273_line.md inserted after that one line; `cmp
   .agent/plan.md .remedy-wt/f268-r5/plan.md` exit 0.
G2 `python3 -m pytest -q -p no:cacheprovider tests/cli/test_do_sequence_cli.py
   tests/orchestration/test_do_sequence.py tests/cli/test_golden_path.py
   tests/orchestration/test_do_run.py tests/test_command_catalog.py
   tests/orchestration/test_job_apply.py tests/orchestration/test_job_evidence.py
   tests/orchestration/test_token_ledger.py tests/orchestration/test_import_reachability.py`
   plus every test file this round edited → 0 failed.
G3 `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_roadmap_index.py
   tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py` → 0 failed.
G4 `python3 -m ruff check` over every .py file C2–C3 touched → "All checks passed!".
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C3, run from
   the worktree root with `python3 -B -m pytest`, `__pycache__` purged before each run,
   the imported module path printed first; unmutated control first (exit 0); each
   mutation reverted before the next: (a) the run step runs every job without the
   per-job apply under `--apply` → C2 test (2) red; (b) the run step's mirror call
   removed → the C3 cost test red; (c) the builder-context field left empty → the
   `context_strategy.json` test red. Report exit codes and failing ids; remove the
   worktree; show `git worktree list` and the `remedy/job-*` branch count before and
   after.
G6 `git status --porcelain` empty and HEAD equals origin after the push.
Full suite: NOT run (amend0917-throughput).
── end of block ──
