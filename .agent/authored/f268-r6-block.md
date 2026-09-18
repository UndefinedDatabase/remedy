── STEP R6 R-0892 + T005 — F268 remedy do: the one-command start ──
Session 1 of F268 · round 6 · base `68cf6a13` (branch feature/f268-remedy-do, pushed).

Goal: book round 5's verdict; land R-0892 — a `do` job's evidence export passes
`scripts/build_review_manifest.py`'s required-artifact check with honest
artifacts — and T005 — five real quick-start lines in `remedy --help`.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F268.md (T005,
Acceptance); R-0892's full text in `.agent/live_review.md`;
`scripts/build_review_manifest.py` (`REQUIRED_ROOT_ARTIFACTS`,
`REQUIRED_TASK_ARTIFACTS`, `validate_evidence_candidate`, `_job_flow_shape_problems`);
`packages/orchestration/job_evidence.py` (`export_job_evidence`);
`packages/orchestration/agent_run_trace.py`; the deleted writers at
`git show 70c78773^:apps/cli/commands/do_cmd.py`; `apps/cli/grouped.py`
(`_QUICK_START`, `_print_root_help`) and its pinning tests
(`tests/cli/test_cli_ux.py` `TestQuickStart`, `tests/test_cli_execution_loop_closure.py`
quick-start assertions, `tests/cli/test_advertised_commands.py`); `README.md`'s
Quickstart; payload `decisions.md` (DECISIONs F268 D13 and D14 bind this round).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f268-r6/`. Verify
each sha256 before use; any mismatch → stop and report. Apply byte-exact.
  ledger.md     sha256 12b5edbeb448a483838f926f8d110bc1291d64aa40cf86ad693097eb5ffa2e8c
  decisions.md  sha256 ffcd3f6e315a0a01e79648fcfd28de0f6d5f686374e5cd4400e5b7f0019418ea
  plan.md       sha256 dfdfa7023ceea5bdaff88fc274dbf7164bfe5bcd594195acf27ea63c3450bdc4
  block.md      this block (save it; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of the payloads as
   `.agent/authored/f268-r6-<name>`; `.agent/live_review.md` := `git show
   68cf6a13:.agent/live_review.md` bytes + ledger.md; `.agent/decisions.md` :=
   `git show 68cf6a13:.agent/decisions.md` bytes + decisions.md;
   `.agent/plan.md` := plan.md.
C2 R-0892 — DECISION F268 D13 in `job_evidence.py`. First measure: export a
   completed fake-provider `do` job (in a test, `REMEDY_DATA_DIR` via monkeypatch)
   and run `validate_evidence_candidate` on it; record which root AND per-task
   artifacts are missing. Then write the four root artifacts per D13. If
   per-task artifacts are also missing for a fake run, write each from the task's
   own run records in the same honest way (never invented values); if a per-task
   artifact has no source at all, stop and report which. Update
   `.claude/skills/remedy-evidence-review/SKILL.md`'s pointer to the deleted
   `do_cmd.py _build_final_audit()` so it names the heir (R-0892's fix clause).
   Test (in `tests/orchestration/test_job_evidence.py` or a new
   `tests/cli/test_do_evidence_package.py`): a fake-provider `remedy do` job,
   exported, validates with `is_valid_current_run` True and no
   `missing root artifact` / `task_runs/…: missing` error; `job_flow.json`'s
   `final_audit.status` equals the export's own verifier verdict.
C3 T005 — DECISION F268 D14: `_QUICK_START` five numbered lines (confirm every
   group/sub/flag exists in the catalog; `remedy job list` and `remedy doctor core`
   exist); `README.md` Quickstart mirrors them; update the pinning tests BY DESIGN,
   each named in the handoff (the `JOB_ID`/`tee`/`<goal>`/"do run" assertions);
   a test that runs the five lines in order, as printed, on a fixture git
   repository with the fake builder and reviewer selected through that
   repository's own `remedy.toml` role configuration (read `role_config.py` for
   the keys), `REMEDY_DATA_DIR` via monkeypatch, each exiting 0.
C4 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md:
   "SESSION 1 of feature F268 · round 6 · rounds so far 6"; per-commit tables with
   `git show --numstat` counts for C1–C3; every gate's real output; `Landed:` lines
   in the HANDOFF only (never `Done:`, never in the ledger) for R-0892. Then `git push`.

Constraints:
1. Change set: only paths the Bundle names plus test files C2–C3 edit. Every
   commit < 500 changed lines; split rather than exceed.
2. `scripts/build_review_manifest.py` and `scripts/make_review_zip.sh` are read
   only: the check is unchanged (D13). Do-not-touch of T2_F268.md stands.
3. No test calls a real provider, starts a UI server or reads real stdin; env vars
   only via `monkeypatch.setenv`; the shell denies `VAR=x cmd` and `cp`.
4. Never weaken an assertion or delete a test to pass. A red gate you can repair
   inside this change set without touching a DECISION: repair it in its own commit
   and name it in the handoff. Anything else: stop and report.
5. Build every appended file from `git show 68cf6a13:<path>` bytes plus the payload.
6. Commit messages "F268 R6 C<n>: <summary>", blank line,
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.

Done when (run each at C3, before C4; report literal output + real exit code):
G1 transport + state: payload digests matched; python byte checks print True for
   both appends against their `68cf6a13` bytes; `cmp .agent/plan.md
   .remedy-wt/f268-r6/plan.md` exit 0.
G2 `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_job_evidence.py
   tests/cli/test_do_sequence_cli.py tests/cli/test_cli_ux.py
   tests/test_cli_execution_loop_closure.py tests/cli/test_advertised_commands.py
   tests/cli/test_golden_path.py tests/orchestration/test_stream_export_e2e.py
   tests/orchestration/test_evidence_index.py tests/orchestration/test_final_verifier.py`
   plus every test file this round edited or added → 0 failed (drop a named file only
   if it does not exist, and say so).
G3 `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_roadmap_index.py
   tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py` → 0 failed.
G4 `python3 -m ruff check` over every .py file C2–C3 touched → "All checks passed!".
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C3, run from
   the worktree root with `python3 -B -m pytest`, `__pycache__` purged before each run,
   the imported module path printed first; unmutated control first (exit 0); each
   mutation reverted before the next: (a) the `job_flow.json` write skipped → the C2
   validity test red; (b) `final_audit.status` hard-coded to a constant → the C2
   status-equality test red; (c) one quick-start line changed to a flag the catalog
   does not declare → a C3 test red. Report exit codes and failing ids; remove the
   worktree; show `git worktree list` and the `remedy/job-*` branch count before and
   after.
G6 `git status --porcelain` empty and HEAD equals origin after the push.
Full suite: NOT run (amend0917-throughput).
── end of block ──
