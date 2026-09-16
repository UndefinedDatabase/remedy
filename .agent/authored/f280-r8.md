── STEP R8/n — F280 ────────────────────────────────────────
Goal: book round 7's independently-reviewed PASS, fix R-0939 (missing trailing newline in
four .agent/ files), and rename the `job run` CLI flag `--max-tasks` to `--tasks`
(DECISION amend0905-vocab D4).

Bundle:
  1. Copy this block to `.agent/authored/f280-r8.md` and mirror to `.agent/last_block.md`.
  2. Fix the trailing newline on `.agent/decisions.md` and `.agent/operator_questions.md`,
     append the Gate:F280 R7 + R-0939 register/resolve text to `.agent/live_review.md`
     (which also fixes its own trailing newline as part of the same append), and replace
     `.agent/plan.md` with the new full content — all four pre-built and pre-verified by
     the reviewer in a disposable worktree.
  3. Apply the pre-built `--tasks` rename patch.
  4. Run the done-when gates, run the canary, write the handoff, commit, push.

Change — exact files, exact source:
  All five source files below live under `/home/decodeux/Repos/remedy/.remedy-wt/` (repo-root
  scratch, NOT a git ref — plain files on disk in the primary checkout's own working tree).
  Copy each BYTE-FOR-BYTE with `shutil.copyfile` or equivalent; do not retype.

  (a) `.agent/decisions.md` — append exactly one `\n` byte at end of file (it currently has
      none). Do NOT touch any other byte.
  (b) `.agent/operator_questions.md` — append exactly one `\n` byte at end of file (it
      currently has none). Do NOT touch any other byte.
  (c) `.agent/live_review.md` — append, IN THIS ORDER, to the end of the current file
      (which currently has NO trailing `\n`):
        1. one `\n` byte (restores the file's own missing trailing newline — this is
           R-0939's fourth file)
        2. one more `\n` byte (the blank-line paragraph separator this ledger's own
           convention uses between entries)
        3. the exact bytes of `.remedy-wt/gate_r7_entry.txt` (sha256
           `a347f1766a12d01280f25059b9aff6bbd95bdc0bd1b2cb75ee7c337992f941c1`, 5625 bytes,
           already ends in its own single `\n`)
        4. one `\n` byte (blank-line separator)
        5. the exact bytes of `.remedy-wt/reg_r0939.txt` (sha256
           `a53a3d6c87394ad430b7e5acd8badb9d2c8b4eeca96c15d4e6d81347ec87d3a0`, 1372 bytes,
           already ends in its own single `\n`)
        6. one `\n` byte (blank-line separator)
        7. the exact bytes of `.remedy-wt/done_r0939.txt` (sha256
           `c3edbab8964da14a12a752094f24fdbf0f750a1feca5e5a366b0f4da0727e485`, 512 bytes,
           already ends in its own single `\n`)
      i.e. `new_bytes = old_bytes + b"\n\n" + gate_r7_entry + b"\n" + reg_r0939 + b"\n" + done_r0939`.
  (d) `.agent/plan.md` — REPLACE THE WHOLE FILE with the exact bytes of
      `.remedy-wt/f280-r8-plan.md` (sha256 `3e9d02077c7519ab16934e1ea6a72f9c8d7b53f87ce85f18446be0f6edbcfc05`,
      2990 bytes, 49 lines). This is a rewrite per AGENTS.md `.agent/plan.md` convention, not
      an append.
  (e) Apply `.remedy-wt/f280-r8-tasks.patch` (sha256
      `66f782d340e80cf74c1747da2fa36f1a16ae13a997abb1d09ef2fb97b581bc16`, 5818 bytes, 94
      lines) with `git apply --check` then `git apply` from the repo root. It touches exactly:
      `apps/cli/command_catalog.py` (1 line: `ArgDef("--max-tasks", ...)` → `ArgDef("--tasks", ...)`,
      same help text, same `default=None`), `apps/cli/grouped.py` (the `elif arg.name ==
      "--max-tasks":` branch and its `parser.add_argument("--max-tasks", ...)` call both become
      `"--tasks"`; `dest="max_tasks"` is UNCHANGED — only the CLI-facing flag string moves,
      never the internal field name), `tests/cli/test_job_run_invocation_truth.py` (one CLI
      invocation literal), `tests/orchestration/test_job_task_runner.py` (four docstring/comment
      strings), `tests/test_command_catalog.py` (adds `("job.run", "--max-tasks")` to
      `TestDeletedFlags.DELETED`, alphabetically between `"--builder"` and `"--reviewer"`).

Constraints:
  - Do not touch any file this block does not name. Do not touch the internal `max_tasks`
    Python identifier anywhere outside the two catalog/grouped.py CLI-wiring lines the patch
    already covers — every other `max_tasks` occurrence in the repo (RunInvocation,
    ExecutionConfig, run_job kwargs, etc.) is an internal name D4 does not govern and stays
    exactly as it is.
  - `docs/roadmap/features/T0_F012.md` mentions `--max-tasks` in prose; it is an accepted
    `[x]` history file (`docs/roadmap/STATUS.md` line naming F012 accepted 2026-07-20) and is
    EXEMPT from this sweep, same rule DECISION F280 D5 already applied to T1_F014/F016/F080/F252 —
    do not edit it.
  - Commit order: C0a (authored carrier) → C0b (last_block mirror) → C1 (the four `.agent/`
    fixes, ONE commit) → C2 (the patch application, ONE commit) → C3 (handoff). Do not split
    C1 or C2 further; both are far under the 500-line insertion cap.
  - `git status --porcelain` empty before your first commit and after your last.

Done when (run every command from the repo root, primary checkout):
  G1 TRANSPORT — one digest comparison: `sha256sum .agent/authored/f280-r8.md` equals
     `sha256sum .agent/last_block.md`, and `cmp` each of the five source files under
     `.remedy-wt/` against the corresponding section it produced in the committed target —
     report PASS/FAIL, not a re-typed diff.
  G2 THE RECORD — after C1, over `.agent/live_review.md`:
     `python3 -c "import re; d=open('.agent/live_review.md').read(); print(len(re.findall(r'^Gate: F\d+ R\d+ — ', d, re.M)), len(set(re.findall(r'^- (R-\d{4}) — ', d, re.M))), len(set(re.findall(r'^Done: (R-\d{4}) — ', d, re.M))))"`
     must read exactly `34 135 7`. `.agent/plan.md` must be exactly 49 lines with exactly one
     `## Goal`, one `## Current Step`, one `## Next Steps`, one `## Risks`.
  G3 THE NEWLINE FIX — after C1, for each of `.agent/plan.md`, `.agent/live_review.md`,
     `.agent/decisions.md`, `.agent/operator_questions.md`:
     `python3 -c "print(open('<path>','rb').read().endswith(b'\n'))"` reads `True`.
  G4 THE PATCH — after C2, `git diff --numstat 4a0da00a..HEAD -- apps/ tests/` reads exactly
     five files: `apps/cli/command_catalog.py` 1/1, `apps/cli/grouped.py` 2/2,
     `tests/cli/test_job_run_invocation_truth.py` 1/1, `tests/orchestration/test_job_task_runner.py`
     4/4, `tests/test_command_catalog.py` 1/0.
  G5 THE SWEEP — after C2, `grep -rn -- '--max-tasks' apps/ packages/ tests/ docs/ scripts/`
     reads exactly one line, `tests/test_command_catalog.py`'s new `DELETED` row, and nothing
     under `docs/roadmap/features/T0_F012.md` (excluded from this grep root by design — it is
     the accepted-history exemption above, verify separately that it is untouched with
     `git diff --stat 4a0da00a..HEAD -- docs/roadmap/features/T0_F012.md` reading empty).
  G6 TARGETED TESTS — after C2:
     `python3 -m pytest tests/test_command_catalog.py tests/cli/test_job_run_invocation_truth.py tests/orchestration/test_job_task_runner.py tests/cli/test_golden_path.py tests/docs/ -q`
     reads `620 passed`.
  G7 RUFF — after C2, `python3 -m ruff check apps/cli/command_catalog.py apps/cli/grouped.py tests/cli/test_job_run_invocation_truth.py tests/orchestration/test_job_task_runner.py tests/test_command_catalog.py`
     reads `All checks passed!`.
  G8 MUTATION RED-PROOF (reachability of the new DELETED-flag guard) — in a DISPOSABLE git
     worktree only (never the primary checkout), at your own C2 commit: revert ONLY the
     `apps/cli/command_catalog.py` line back to `ArgDef("--max-tasks", ...)` (put the flag
     back, leave `grouped.py` and the test files exactly as C2 left them), then run
     `python3 -m pytest tests/test_command_catalog.py::TestDeletedFlags -q`. Report the exact
     failing node id (expect
     `TestDeletedFlags::test_no_deleted_flag_is_declared_by_its_command` to fail, since the
     catalog now declares the "deleted" flag again). Revert your mutation, re-run the same
     command, report the second (green) result. Remove the disposable worktree after.

Handback: completion report (state block, deviations, next steps) + rewrite
`.agent/handoff.md`. Attribute commits `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`.
Session number: this is SESSION 4 of F280, round 8.
──────────────────────────────────────────────────────────────
