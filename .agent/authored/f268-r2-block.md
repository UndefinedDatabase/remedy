── STEP R2 T002 + R-0963/R-0964/R-0965 — F268 remedy do: the one-command start ──
Session 1 of F268 · round 2 · base `f0210593` (branch feature/f268-remedy-do, pushed).

Goal: book round 1's verdict and three findings, repair them, and land T002 —
the shape read from the mission plan, `--force-job` / `--force-mission`, and
tasks bounded by deliverables with one validator.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F268.md (Design,
T002, Acceptance); `packages/orchestration/do_sequence.py`; the three findings
in payload `ledger.md` and the three DECISIONs in payload `decisions.md` — they
bind this round's design.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f268-r2/`. Verify
each sha256 before use; any mismatch → stop and report. Apply byte-exact.
  ledger.md     sha256 d4ba52076db37b82737303fc4d6566c8b157806f1fc92ee8babe7273b7b685b0
  decisions.md  sha256 b660d7780fd39f3e653dc8223c69f4c0ba5b60dd301b5d1fcfcf0e3d22585866
  plan.md       sha256 ba5e2512ca9352bca704a49e76b9cdb46d523de576a9358066983fcbb3be29d3
  block.md      this block (save it; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of the payloads as
   `.agent/authored/f268-r2-<name>`; `.agent/live_review.md` := old bytes +
   ledger.md (append); `.agent/decisions.md` := old bytes + decisions.md (append);
   `.agent/plan.md` := plan.md.
C2 repairs —
   R-0963: a test in `tests/cli/test_do_sequence_cli.py`: after `do` on an
   unregistered repo, `<repo>/.git/info/exclude` holds every entry
   `repo_ignore.ignore_entries(<repo root>)` returns.
   R-0964 per DECISION D7: `scripts/remedy_smoke.sh` section 12ao drops
   `--fixture-builder repair-loop` (nothing else in the section changes; confirm
   with `bash -n scripts/remedy_smoke.sh`); `apps/cli/commands/dev.py`'s hint drops
   it; `_pipeline_next_command` in `packages/orchestration/ui_server.py` returns
   `remedy job show <job id> --full --json` for `provider_output_prose_only` and
   `provider_output_malformed`, with a test (find the existing tests of that
   function first and extend them); `docs/guides/autocoder-usage.md` and
   `docs/system/repair-loop-v1.md` describe only flags the current parser
   accepts and say `--fixture-builder` was deleted by F268.
   R-0965: the `do.run` catalog entry declares `may_execute_commands=True`
   (matching `job.run`); `tests/orchestration/test_do_run.py`'s pinned
   `test_do_run_no_command_execution` moves with it, renamed to what it now
   asserts; any other catalog guard this trips is read and satisfied, not
   weakened.
C3 deliverables — `packages/orchestration/task_deliverables.py` per DECISION D6
   (extractor, deterministic job plan, validator; the inspection verbs are a
   named tuple constant) with unit tests in
   `tests/orchestration/test_task_deliverables.py`: one-sentence order without a
   path → 1 task; an order naming ten distinct files → ten tasks in order, each
   `inputs["deliverable"]` the file; duplicates collapse; 26 files → two jobs'
   worth of tasks, none dropped; the validator rejects a task with no deliverable
   and a task titled with each inspection verb, and accepts a clean plan; every
   deterministic task carries at most `planning.granularity.max_acceptance`
   acceptance items.
C4 shape — `do_sequence.py` per DECISION D5: the plan step stores the plan on the
   context; the shape function; `plan_order_job` uses the D6 deterministic plan in
   place of `job_runner.plan_job` and runs the D6 validator on every plan (LLM
   included, deliverable from `files_hint[0]` else the first acceptance line);
   the multi-job branch with `initial` / `follow_up` links and `repo_path` on
   every job; the run step runs every job in order and stops at the first that
   does not complete; the apply step prints one real apply command per job.
   CLI: `--force-job` and `--force-mission` on `do.run` (catalog, the bare-route
   allow-list in `apps/cli/grouped.py`, `_cmd_do_order`), both together exit 2;
   `--json` adds `shape` and `shape_source`. Update every existing test whose
   pinned behaviour this changes BY DESIGN (the golden path's "3 task(s)" and
   "deterministic skeleton" readings, `tests/cli/test_plan_approval.py`'s plan
   label, …), each edit named in the handoff with its reason.
C5 acceptance tests — in `tests/cli/test_do_sequence_cli.py`, same fixture style
   as round 1 (fake providers, `--no-ui`, `--no-llm`, `REMEDY_DATA_DIR` via
   monkeypatch, the model-call tripwire): (1) `do "Write a CONTRIBUTING.md"`
   plans ONE job, `shape` "one job", `shape_source` "planner", ≤3 tasks;
   (2) the same order with `--force-mission` yields ≥2 jobs, all linked to the one
   mission (first `initial`, rest `follow_up`), every job run, every `repo_path`
   the repo root, `git status --porcelain` unchanged; (3) `--force-job` on an
   order naming ten files yields one job of ten tasks; (4) `--force-job
   --force-mission` exits 2; (5) a unit test of the shape function over a plan
   with two outlines reads "milestones" and over one reads "one job".
C6 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md:
   "SESSION 1 of feature F268 · round 2 · rounds so far 2"; per-commit tables with
   `git show --numstat` counts for C1–C5; every gate's real output; `Landed:`
   lines in the HANDOFF only (never `Done:`, never in the ledger) for R-0963,
   R-0964, R-0965 and, for what this round reaches of it, R-0808. Then `git push`.

Constraints:
1. Change set: only paths the Bundle names plus test files C2–C5 edit. Every
   commit < 500 changed lines; split rather than exceed (C4a/C4b is fine).
2. Do-not-touch (T2_F268.md): planner internals — `mission_compiler`,
   `mission_plan_schema`, `schemas/models.py`, `job_plan.plan_job_llm`,
   `task_granularity`, `job_runner` stay unedited — the contract's shape, the
   apply gate's semantics, the cockpit's content (the one `ui_server.py` string
   R-0964 names is a hint, not content).
3. No test calls a real provider; env vars only via `monkeypatch.setenv`; the
   shell denies `VAR=x cmd` and `cp` (use `python3 -c "import shutil; ..."`).
4. Never weaken an assertion or delete a test to pass; a conflict the DECISIONs
   do not settle → stop and report, nothing half-committed.
5. Commit messages "F268 R2 C<n>: <summary>", blank line,
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.

Done when (run each at C5, before C6; report literal output + real exit code):
G1 transport + state: payload digests matched; python byte checks print True for
   `.agent/live_review.md` = `git show f0210593:.agent/live_review.md` + ledger.md,
   `.agent/decisions.md` = `git show f0210593:.agent/decisions.md` + decisions.md,
   and `cmp .agent/plan.md .remedy-wt/f268-r2/plan.md` exit 0.
G2 `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_task_deliverables.py
   tests/orchestration/test_do_sequence.py tests/cli/test_do_sequence_cli.py
   tests/cli/test_golden_path.py tests/cli/test_plan_approval.py tests/cli/test_decision_answers.py
   tests/cli/test_mission_cmd.py tests/cli/test_scoped_listings.py tests/orchestration/test_do_run.py
   tests/test_command_catalog.py tests/orchestration/test_import_reachability.py
   tests/orchestration/test_job_apply.py tests/test_runner.py` plus every test file this round
   edited and the existing test file(s) of `_pipeline_next_command` → 0 failed.
G3 `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_roadmap_index.py
   tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py` → 0 failed;
   `bash -n scripts/remedy_smoke.sh` exit 0.
G4 `python3 -m ruff check` over every .py file C2–C5 touched → "All checks passed!".
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C5, run from
   the worktree root with `python3 -B -m pytest`, `__pycache__` purged before each run,
   the imported module path printed first; unmutated control first (exit 0); each
   mutation reverted before the next: (a) the validator's inspection-verb check
   disabled → `tests/orchestration/test_task_deliverables.py` red; (b) `--force-mission`
   read as False inside the shape step → C5 test (2) red; (c) the ignore-entry loop in
   `_step_init` iterates an empty slice → the R-0963 test red. Report exit codes and
   failing ids; remove the worktree; show `git worktree list` and the `remedy/job-*`
   branch count before and after.
G6 `git status --porcelain` empty and HEAD equals origin after the push.
Full suite: NOT run (amend0917-throughput).
── end of block ──
