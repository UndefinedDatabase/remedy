── STEP R3 T003 + R-0964/R-0966/R-0811 — F268 remedy do: the one-command start ──
Session 1 of F268 · round 3 · base `57ca6293` (branch feature/f268-remedy-do, pushed).

Goal: book round 2's verdict; repair R-0964's residue, R-0966 and R-0811's
`job show` half; land T003 — `--step-by-step` and `--plan-only` — and list
every job's tasks in `do`'s output.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F268.md (Design,
T003, Acceptance); `packages/orchestration/do_sequence.py`;
`packages/orchestration/safe_points.py` (`request_stop`); payload `ledger.md`
(the R2 gate record names R-0964's residue; R-0966's fix clause) and payload
`decisions.md` (DECISION F268 D8 binds T003's design).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f268-r3/`. Verify
each sha256 before use; any mismatch → stop and report. Apply byte-exact.
  ledger.md     sha256 007ae5a776560c8e84e0861f7654bdf6df468bda9932cbc8846cb3a83dbb9e77
  decisions.md  sha256 1a18778fbfbe848721d73ffd0958e57902131fbf5549d6d8fdb73aca70d499b4
  plan.md       sha256 dc90d095784d3ef04a8ba234aa70d50149450f901d442e79a57c1feb2b6df03e
  block.md      this block (save it; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of the payloads as
   `.agent/authored/f268-r3-<name>`; `.agent/live_review.md` := `git show
   57ca6293:.agent/live_review.md` bytes + ledger.md; `.agent/decisions.md` :=
   `git show 57ca6293:.agent/decisions.md` bytes + decisions.md;
   `.agent/plan.md` := plan.md.
C2 repairs —
   R-0964 residue: `docs/system/first-perfect-job-demo-v0.md` shows only
   invocations the current parser accepts (its two `--fixture-builder true`
   uses); the comment in `packages/orchestration/autorun.py` stops naming the
   deleted flag; the `dev` hint in `apps/cli/commands/dev.py` stops calling
   bare `do` a repair E2E (describe what it does, or drop the line).
   R-0966: per its fix clause, in `packages/orchestration/task_deliverables.py`
   with tests in `tests/orchestration/test_task_deliverables.py`.
   R-0811's `job show` half: the two tips that print
   `remedy job attach-repo <job_id> <path>` — `stop_reasons.py` (the
   `sr:derived_no_repo` next action) and `autonomy_readiness.py` (the
   `attached_repo` check) — print the real job id; for the path, the job's
   project's `canonical_repo_path` when the job has a project with one, else a
   sentence naming what to pass, never an angle-bracket placeholder. Read each
   call site's inputs first; a test per tip asserting no `<[a-z_]+>` survives in
   the rendered text and the real job id appears.
C3 T003 — DECISION F268 D8 in `do_sequence.py`: the halt function (reads through
   a line-reader the context carries; the CLI supplies `input`), halts after each
   step that did work and before each job in the run step, `q` or EOF stops the
   walk and calls `safe_points.request_stop(job_id, reason=..., source="do")` for
   every job of the walk; `--plan-only` ends the walk after shape with the run
   step reporting stopped, reason `--plan-only`, no job run. CLI: `--step-by-step`
   and `--plan-only` on `do.run` (catalog with descriptions the vocabulary guard
   accepts, the bare-route allow-list in `apps/cli/grouped.py`, `_cmd_do_order`).
   Output: after the shape step, text output lists every job's tasks, one line
   each with its deliverable; `--json` adds `jobs`: a list of
   `{job_id, tasks: [{title, deliverable}]}` in job order, and `mission_plan_path`.
C4 tests — `tests/cli/test_do_sequence_cli.py`, same fixture style as rounds 1–2
   (fake providers, `--no-ui`, `--no-llm`, `REMEDY_DATA_DIR` via monkeypatch, the
   model-call tripwire): (1) `--step-by-step` with a reader answering empty lines
   halts at least three times and completes like a plain run; (2) a reader that
   records a provider-call counter on entry and exit of every wait proves no
   provider call happens while a halt waits (count the fake provider's calls —
   read how `FakeProvider` counts builds and reviews); (3) `q` at the first halt
   after shape stops the walk, no job is run, and `safe_points` shows a stop
   request for every job of the walk; (4) `--plan-only` writes the mission plan
   (its path exists), plans the jobs, starts no run (no job has a run), and
   `--json` carries `contract` null and `jobs` with tasks and deliverables;
   (5) text output lists each task's deliverable.
C5 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md:
   "SESSION 1 of feature F268 · round 3 · rounds so far 3"; per-commit tables with
   `git show --numstat` counts for C1–C4; every gate's real output; `Landed:`
   lines in the HANDOFF only (never `Done:`, never in the ledger) for R-0964,
   R-0966 and R-0811. Then `git push`.

Constraints:
1. Change set: only paths the Bundle names plus test files C2–C4 edit. Every
   commit < 500 changed lines; split rather than exceed.
2. Do-not-touch (T2_F268.md): planner internals (`mission_compiler`,
   `mission_plan_schema`, `schemas/models.py`, `job_plan`, `task_granularity`,
   `job_runner`), `pingpong_job.run_job`'s own stop check (D8's alternative
   rejected), the contract's shape, the apply gate's semantics, the cockpit's
   content.
3. No test calls a real provider or reads real stdin; env vars only via
   `monkeypatch.setenv`; the shell denies `VAR=x cmd` and `cp`.
4. Never weaken an assertion or delete a test to pass. A red gate you can repair
   inside this change set without touching a DECISION: repair it in its own
   commit and name it in the handoff. Anything else: stop and report.
5. Build every appended file from `git show 57ca6293:<path>` bytes plus the
   payload — never from a file you are writing.
6. Commit messages "F268 R3 C<n>: <summary>", blank line,
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.

Done when (run each at C4, before C5; report literal output + real exit code):
G1 transport + state: payload digests matched; python byte checks print True for
   both appends against their `57ca6293` bytes, and `cmp .agent/plan.md
   .remedy-wt/f268-r3/plan.md` exit 0.
G2 `python3 -m pytest -q -p no:cacheprovider tests/cli/test_do_sequence_cli.py
   tests/orchestration/test_do_sequence.py tests/orchestration/test_task_deliverables.py
   tests/cli/test_golden_path.py tests/cli/test_plan_approval.py tests/cli/test_mission_cmd.py
   tests/cli/test_job_commands.py tests/test_cli_execution_loop_closure.py
   tests/test_command_catalog.py tests/orchestration/test_import_reachability.py
   tests/orchestration/test_safe_points.py` plus every test file this round edited and the
   existing test files of `stop_reasons.py` and `autonomy_readiness.py` → 0 failed.
G3 `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_roadmap_index.py
   tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py` → 0 failed.
G4 `python3 -m ruff check` over every .py file C2–C4 touched → "All checks passed!".
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C4, run from
   the worktree root with `python3 -B -m pytest`, `__pycache__` purged before each run,
   the imported module path printed first; unmutated control first (exit 0); each
   mutation reverted before the next: (a) the halt function returns without reading →
   C4 test (1) red; (b) the `q` branch skips `request_stop` → C4 test (3) red;
   (c) `--plan-only` read as False → C4 test (4) red. Report exit codes and failing
   ids; remove the worktree; show `git worktree list` and the `remedy/job-*` branch
   count before and after.
G6 `git status --porcelain` empty and HEAD equals origin after the push.
Full suite: NOT run (amend0917-throughput).
── end of block ──
