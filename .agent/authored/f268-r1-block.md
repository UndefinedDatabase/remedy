── STEP R1 T001 — F268 remedy do: the one-command start ──
Session 1 of F268 · round 1 · base `8e075bbe` (main, the merge of PR 255).

Goal: claim F268 and land T001 — `remedy do "<order>"` walks one ordered list of
step names (init, study, plan, shape, run, ui, apply) end to end on the fake
provider and stops before apply, with one test per step boundary.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F268.md; the four
DECISIONs in the payload `decisions.md` below (they bind this round's design).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f268-r1/`. Verify
each sha256 before use; any mismatch → stop and report. Apply byte-exact; never retype.
  plan.md              sha256 31b06c4e26ceeea7648b489392398bf72dfc1dfbf3cde13494bcd79cb91ce188
  context.md           sha256 18deda742479fdca0daaef2f1c17dcb12284cada7f5ad6956ddf88d08f2f0d9e
  live_review_head.md  sha256 917f9ff55f9e785c42e44af6142e10785ffb55c562e0a86c52fc6903a7bf1936
  decisions.md         sha256 04cd299a6d593e7ed456e4c2d9436411b9dc3b731e7c9a4247751493d416af58
  status_from.txt      sha256 74cca710aff46175f7b0bae6739be4963c87149463929df16e3e9ce8a00bce6e
  status_to.txt        sha256 02419d148e2ff0b8cf451ba5dccd7bb9f3efaea097c2ab5e5f976732e7025b7a
  block.md             this block (save it; its digest is reported, not pre-stated)

Bundle (commit order):
C1 claim — branch `feature/f268-remedy-do` from `main` at `8e075bbe` (Open PR Gate
   already run by the reviewer: zero open PRs). One commit holding exactly:
   byte copies of every payload file above under `.agent/authored/f268-r1-<name>`;
   `.agent/plan.md` := plan.md; `.agent/context.md` := context.md;
   `.agent/live_review.md` := live_review_head.md bytes + the old file's bytes from
   the line `## Findings` (inclusive) to the end, byte-identical;
   `.agent/decisions.md` := old bytes + decisions.md bytes (append);
   `docs/roadmap/STATUS.md`: the single line equal to status_from.txt replaced by
   status_to.txt.
C2 helpers — (a) move `_ensure_ignore_entry` and `_ignore_entries` out of
   `apps/cli/commands/init_cmd.py` into a new `packages/orchestration/` module (name
   it; public names without the underscore); `init_cmd.py` imports them; `remedy
   init` behaviour byte-unchanged (its tests stay green unedited). (b) DECISION D3's
   single function in `packages/orchestration/study.py` that writes
   `metadata["studied_at"]` and `metadata["studied_head"]` on the project record and
   saves it; `remedy study run` (`apps/cli/commands/study_cmd.py`) calls it after a
   pass completes. Tests for (b) in the existing study test files.
C3 sequence — `packages/orchestration/do_sequence.py` per DECISION D4: `DO_SEQUENCE`,
   the step table, a context object carrying the order, repo root, project, mission
   id, job ids, role/provider choices, flags and per-step results, and ONE walker
   that calls steps only through the table in `DO_SEQUENCE` order. Steps:
   init (D2: `resolve_project`, else `register_project_repo` + the ignore entries);
   study (D3: once, non-empty repo only, `run_study` then the D3 writer);
   plan (create the mission for the order, set its order, `plan_mission` —
   deterministic when no planner provider is available; mirror how
   `mission plan` in `apps/cli/commands/mission_cmd.py` calls it);
   shape (T001: ONE job linked to the mission — move, do not copy, the job-planning
   body of `_cmd_do_mission` in `apps/cli/commands/do_cmd.py` (intake, task plan or
   skeleton, `--yes` auto-approval) into a function this step calls; the job gets
   `repo_path` = repo root and is linked with `link_job_to_mission`);
   run (`pingpong_job.run_job` with the builder/reviewer provider choices; if the
   job's task plan awaits approval and `--yes` was not given, the step stops and
   prints the real approval command with the real job id);
   ui (D4: skipped under `--no-ui`; otherwise prints `remedy ui start <real job id>`);
   apply (always stops before apply in T001). Unit tests in
   `tests/orchestration/test_do_sequence.py`: `DO_SEQUENCE` is exactly the seven
   names in order; the walker calls a spy table in that order and nothing outside it;
   a step that stops ends the walk with later steps not called.
C4 wiring — bare `remedy do "<order>"` (the `_truly_bare` route in
   `apps/cli/grouped.py` → `_cmd_do` → today `_cmd_do_mission`) runs the walker.
   Catalog (`apps/cli/command_catalog.py`, `do.run`): `--builder-provider` becomes
   the run's builder provider (choices fake, claude, claude-cli, ollama; default
   None = role config), add `--reviewer-provider` (same choices) and `--yes`;
   `--fixture-builder` is deleted with its reads (R-0933). Non-bare `do run` with
   `--dry-run` keeps its current path untouched this round. `--json` prints one
   object with at least `mission_id`, `job_ids` (ordered list), `contract` (null,
   D1), `stopped_before_apply` (bool), and `steps` (list of name/status/detail).
   Text output prints one line per step and ends with `Next:` lines carrying real
   ids and paths only. Update every existing test whose pinned behaviour this
   round changes BY DESIGN (e.g. `tests/cli/test_golden_path.py`,
   `tests/cli/test_mission_cmd.py`'s "do leaves no mission behind",
   `tests/cli/test_plan_approval.py` / `tests/cli/test_decision_answers.py` calls
   into `_cmd_do_mission`, `tests/test_cli_execution_loop_closure.py`'s
   `--fixture-builder` cases): each edit keeps the test's own property where it
   still holds and is named in the handoff with its reason. Regenerate the
   import-reachability allowlist with its own generator if the test requires it.
C5 boundary tests — `tests/cli/test_do_sequence_cli.py`, in-process, a tmp git repo
   with one committed file, `REMEDY_DATA_DIR` via `monkeypatch.setenv`, fake
   builder and reviewer, `--no-ui`, no model call anywhere (planner/intake forced
   deterministic): (1) init→study: an unregistered repo is registered and studied,
   `studied_at`/`studied_head` written; a second `do` skips study; (2) study→plan: a
   mission exists carrying the order, and `--json` `mission_id` names it; (3)
   plan→shape: exactly one job, linked to that mission, `repo_path` = repo root;
   (4) shape→run: the fake run completes and the job records it; (5) run→stop:
   `git status --porcelain` in the target is byte-identical before and after `do`,
   `stopped_before_apply` is true; (6) R-0897: `job_apply.apply_job(<job id>,
   <repo>, approve=True)` then accepts the job `do` ran.
C6 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md,
   Session section "SESSION 1 of feature F268 · round 1 · rounds so far 1", per-commit
   changed-files tables with `git show --numstat` counts for C1–C5, every gate's real
   output, the owned findings this round touched (R-0897, R-0933, R-0811) as
   `Landed: R-XXXX — <what, which commit>` lines in the HANDOFF only (never a `Done:`,
   never in the ledger). Then `git push -u origin feature/f268-remedy-do`.

Constraints:
1. Change set: only the paths the Bundle names plus test files the round edits
   under C4/C5 and the regenerated allowlist. Every commit < 500 changed lines
   excluding pure moves; split a commit rather than exceed.
2. Do-not-touch (T2_F268.md): planner internals, the contract's shape (F269), the
   apply gate's semantics, the cockpit's content.
3. No test calls a real provider. Env vars only via `monkeypatch.setenv` or
   in-process `os.environ`; the shell denies `VAR=x cmd` and `cp`.
4. Never weaken an assertion or delete a test to pass; if a pinned behaviour
   conflicts with a DECISION and the fix is unclear, stop and report.
5. Any red gate or ambiguity the DECISIONs do not settle → stop, commit nothing
   half-done, report.
6. Commit messages "F268 R1 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.

Done when (run each at C5, before C6; report literal output + real exit code):
G1 transport + state: every payload digest matched; `cmp` of `.agent/plan.md` and
   `.agent/context.md` against their payloads exit 0; python byte checks print True
   for the live_review re-head (head + old bytes from `## Findings`) and the
   decisions append (old + slice), both against `git show 8e075bbe:<path>`.
G2 `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_do_sequence.py
   tests/cli/test_do_sequence_cli.py tests/cli/test_init_cmd.py tests/cli/test_study_cmd.py
   tests/orchestration/test_study.py tests/cli/test_golden_path.py tests/cli/test_mission_cmd.py
   tests/cli/test_plan_approval.py tests/cli/test_decision_answers.py tests/cli/test_job_commands.py
   tests/test_cli_execution_loop_closure.py tests/cli/test_do_runtime.py
   tests/orchestration/test_do_run.py tests/orchestration/test_import_reachability.py
   tests/cli/test_scoped_listings.py tests/orchestration/test_mission_compiler.py` plus every
   other test file this round edited → summary line, 0 failed.
G3 `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_roadmap_index.py
   tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py` → 0 failed.
G4 `python3 -m ruff check` over every .py file C2–C5 touched → "All checks passed!".
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C5, run
   from the worktree root with `python3 -B -m pytest`, `__pycache__` purged before
   each run, the module path printed first to prove it resolves inside the
   worktree; the UNMUTATED control run first (must be exit 0), each mutation
   reverted before the next: (a) the walker iterates `DO_SEQUENCE` reversed →
   `tests/orchestration/test_do_sequence.py` red; (b) the shape step omits
   `repo_path` → test (6) of C5 red; (c) the D3 writer returns without writing →
   test (1) of C5 red. Report each exit code and failing ids; remove the worktree
   and show `git worktree list`.
G6 `git status --porcelain` empty and HEAD equals origin after the push.
Full suite: NOT run (amend0917-throughput).
── end of block ──
