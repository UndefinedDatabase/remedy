── STEP R4 T004 + R-0967/R-0811 — F268 remedy do: the one-command start ──
Session 1 of F268 · round 4 · base `f831d374` (branch feature/f268-remedy-do, pushed).

Goal: book round 3's verdict; repair R-0967 and the rest of R-0811's
placeholder tips; land T004 — the detached cockpit, `--apply`, and the
F269/F270 flags refusing as not yet available.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F268.md (Design,
T004, Acceptance); `packages/orchestration/do_sequence.py`; `apps/cli/commands/ui.py`
(`_cmd_ui_start`, `--info-file`, `ui stop`); `packages/orchestration/job_apply.py`
(`apply_job`); payload `ledger.md` (R-0967's fix clause; the R-0811 remainder
named in the R3 gate record) and payload `decisions.md` (DECISION F268 D9 binds
T004's design).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f268-r4/`. Verify
each sha256 before use; any mismatch → stop and report. Apply byte-exact.
  ledger.md     sha256 8d4d502300c701ec7777215d6afd3e9478c570e9e391def9483d5071501d6158
  decisions.md  sha256 72663c2731e709875667bd427c787b8919b1cc400b0a81ebfd3e8d1c5196f2a8
  plan.md       sha256 f9b1bf555a029f4b6132eea351b35762f92eed81b1f13415f87fd2afcfc60abf
  block.md      this block (save it; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of the payloads as
   `.agent/authored/f268-r4-<name>`; `.agent/live_review.md` := `git show
   f831d374:.agent/live_review.md` bytes + ledger.md; `.agent/decisions.md` :=
   `git show f831d374:.agent/decisions.md` bytes + decisions.md;
   `.agent/plan.md` := plan.md.
C2 repairs —
   R-0967: per its fix clause.
   R-0811 remainder: every tip in `packages/orchestration/stop_reasons.py` and
   `packages/orchestration/autonomy_readiness.py` that prints an angle-bracket
   placeholder or `"<goal>"` prints the real job id (and the real intent id
   where the caller has it) — read each call site's inputs first; where a value
   is genuinely unknown to the function, the tip names it in words, never in
   angle brackets. `remedy do run "<goal>"` in the `tasks_defined` check becomes
   a real `remedy do "<order>"`-free sentence or a real command. One test per
   module asserting that the full rendered readiness summary and every
   stop-reason next action for a job carry no `<[a-z_]+>` match and do carry the
   real job id; widen the round 3 tests that checked only the `attach-repo` line.
C3 T004 — DECISION F268 D9 in `do_sequence.py` and the CLI:
   (1) the ui step's detached launch through a launcher on the walk's context
   (the CLI's default launcher spawns `sys.executable -m apps.cli.grouped ui
   start <job id> --port 0 --info-file <path>` with `start_new_session=True`,
   stdout/stderr to a log file under the data root; bounded wait for the info
   file; reports URL and `remedy ui stop`; a timeout reports `skipped` with the
   reason and the manual command);
   (2) `--apply`: the apply step applies every job in order via
   `apply_job(<job id>, <repo root>, approve=True)`, stops at the first not
   applied naming why (status `failed`), `stopped_before_apply` false on success;
   (3) `--contract <template>`, `--commit <message>`, `--commit-auto`,
   `--commit-with-history`, `--push` on `do.run`: while F269 / F270 are `[ ]`,
   each exits 2 before any step with "not yet available" and the feature that
   brings it; `--with-history` is never created. Catalog descriptions pass the
   vocabulary guard; the bare-route allow-list in `apps/cli/grouped.py` carries
   every new flag (valued ones in its valued set).
C4 tests — `tests/cli/test_do_sequence_cli.py`, same fixture style as rounds 1–3:
   (1) without `--no-ui`, a fake launcher records it was called once with the
   last job id and the ui step reports the URL it returned; a launcher that
   times out yields `skipped` and the walk still ends at apply; (2) `--apply`
   applies every job (single-job and `--force-mission`), the target repository's
   tracked content changes, `stopped_before_apply` is false; (3) an apply that
   is refused (make the target dirty the way `job_apply`'s baseline check
   refuses — read it first) ends the walk `failed` naming the job; (4) each of
   the five refusing flags exits 2 with "not yet available", no project is
   registered and no mission created; (5) the default launcher builds the argv
   named in C3 (test the argv builder, never spawn).
C5 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md:
   "SESSION 1 of feature F268 · round 4 · rounds so far 4"; per-commit tables with
   `git show --numstat` counts for C1–C4; every gate's real output; `Landed:`
   lines in the HANDOFF only (never `Done:`, never in the ledger) for R-0967 and
   R-0811. Then `git push`.

Constraints:
1. Change set: only paths the Bundle names plus test files C2–C4 edit. Every
   commit < 500 changed lines; split rather than exceed.
2. Do-not-touch (T2_F268.md): planner internals, the contract's shape, the apply
   gate's semantics (`job_apply.py` is read, never edited), the cockpit's content
   (`ui.py` and `ui_server.py` are read, never edited this round).
3. No test starts a real UI server, opens a browser, calls a real provider or
   reads real stdin; env vars only via `monkeypatch.setenv`; the shell denies
   `VAR=x cmd` and `cp`.
4. Never weaken an assertion or delete a test to pass. A red gate you can repair
   inside this change set without touching a DECISION: repair it in its own
   commit and name it in the handoff. Anything else: stop and report.
5. Build every appended file from `git show f831d374:<path>` bytes plus the
   payload — never from a file you are writing.
6. Commit messages "F268 R4 C<n>: <summary>", blank line,
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.

Done when (run each at C4, before C5; report literal output + real exit code):
G1 transport + state: payload digests matched; python byte checks print True for
   both appends against their `f831d374` bytes, and `cmp .agent/plan.md
   .remedy-wt/f268-r4/plan.md` exit 0.
G2 `python3 -m pytest -q -p no:cacheprovider tests/cli/test_do_sequence_cli.py
   tests/orchestration/test_do_sequence.py tests/cli/test_golden_path.py
   tests/orchestration/test_stop_reasons.py tests/test_autonomy_readiness.py
   tests/cli/test_open_decisions_view.py tests/regression/test_named_bugs.py
   tests/orchestration/test_autonomy.py tests/orchestration/test_job_apply.py
   tests/test_cli_execution_loop_closure.py tests/test_command_catalog.py
   tests/orchestration/test_import_reachability.py tests/cli/test_job_commands.py`
   plus every test file this round edited → 0 failed.
G3 `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_roadmap_index.py
   tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py` → 0 failed.
G4 `python3 -m ruff check` over every .py file C2–C4 touched → "All checks passed!".
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C4, run from
   the worktree root with `python3 -B -m pytest`, `__pycache__` purged before each run,
   the imported module path printed first; unmutated control first (exit 0); each
   mutation reverted before the next: (a) the EOFError branch of the halt reads as an
   empty answer → the R-0967 test red; (b) `--apply` read as False in the apply step →
   C4 test (2) red; (c) the refusal of `--push` removed → C4 test (4) red. Report exit
   codes and failing ids; remove the worktree; show `git worktree list` and the
   `remedy/job-*` branch count before and after.
G6 `git status --porcelain` empty and HEAD equals origin after the push.
Full suite: NOT run (amend0917-throughput).
── end of block ──
