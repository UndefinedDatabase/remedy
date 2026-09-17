── STEP R12/n — F280 ────────────────────────────────────
Goal: book round 11's independently-reviewed PASS (Gate: F280 R11, one prose slip, no new
R-id), author DECISION F280 D7 (corrects D6's numeral, widens D6's item 1 to the prompt-trace
role, names further persisted spellings as owed to a future round), and land DECISION F280
D6 (as corrected and widened by D7) as ONE mechanical, reviewer-dry-run-verified rename patch.

Bundle:
  1. Copy this block to `.agent/authored/f280-r12.md` and mirror to `.agent/last_block.md`.
  2. Append the Gate:F280 R11 entry to `.agent/live_review.md`, append the prose-slip line to
     `.agent/prose_slips.md`, append DECISION F280 D7 to `.agent/decisions.md`, insert the
     feature-file amendment into `docs/roadmap/features/T2_F280.md`, and replace `.agent/plan.md`
     — all five pre-built and pre-verified by the reviewer.
  3. Apply the reviewer's pre-built, pre-tested rename patch (`.remedy-wt/f280-r12-rename.patch`)
     with `git apply`, verbatim, in ONE commit.
  4. Run the done-when gates, write the handoff, commit, push.

Change — exact files, exact source:
  All source files below live under `/home/decodeux/Repos/remedy/.remedy-wt/` (repo-root
  scratch, NOT a git ref — plain files on disk in the primary checkout's own working tree).
  Copy each BYTE-FOR-BYTE with `shutil.copyfile` or equivalent; do not retype.

  (a) `.agent/live_review.md` — append, IN THIS ORDER, to the end of the current file (which
      currently ends in exactly one `\n`):
        1. one `\n` byte (blank-line paragraph separator)
        2. the exact bytes of `.remedy-wt/gate_r11_entry.txt` (sha256
           `2964241b6cfca85c875e8b9ead96ee1c00257cbef9cbbbdde8e9165f3edb7f15`, 4251 bytes,
           already ends in its own single `\n`)
      i.e. `new_bytes = old_bytes + b"\n" + gate_r11_entry`. There is no new R-id to register.
  (b) `.agent/prose_slips.md` — append, IN THIS ORDER, to the end of the current file (which
      currently ends in exactly one `\n`):
        1. one `\n` byte (blank-line paragraph separator)
        2. the exact bytes of `.remedy-wt/prose_slip_r11.txt` (sha256
           `942f319e056e3827da07c8391eb04a7268cae5ae1e5bfc7fdfe3bc0532862798`, 853 bytes,
           already ends in its own single `\n`)
  (c) `.agent/decisions.md` — append, IN THIS ORDER, to the end of the current file (which
      currently ends in exactly one `\n`):
        1. one `\n` byte (blank-line paragraph separator)
        2. the exact bytes of `.remedy-wt/decision_f280_d7.txt` (sha256
           `e658d81b749ffaadc3cbb339c5d1c5b516977d9d7049a46fd16239e83b6e6598`, 6701 bytes,
           already ends in its own single `\n`)
  (d) `docs/roadmap/features/T2_F280.md` — INSERT the exact bytes of
      `.remedy-wt/t2_f280_amendment_d7.txt` (sha256
      `4d35018d88d14859a782dd0f49cdab6676a1f05a4329440a07b92883f6bbbdf8`, 821 bytes, starts with
      its own leading `\n` and ends in its own single trailing `\n`) immediately after the byte
      sequence ending `...D6 explicitly does not reach either.\n` (the end of DECISION F280 D6's
      amendment paragraph) and immediately before the pre-existing blank line that precedes the
      `## T002` heading. Locate the exact splice point yourself by reading the file — do not
      guess a line number; the insertion is `prefix + amendment_bytes + suffix` where `prefix`
      ends in `does not reach either.\n` and `suffix` begins with the existing blank line then
      `## T002 — Descriptions, role labels, help wrapping, tests`.
  (e) `.agent/plan.md` — REPLACE THE WHOLE FILE with the exact bytes of
      `.remedy-wt/f280-r12-plan.md` (sha256
      `512d742bc87934f93e9b4845647dbcba19bd001df5dd1a28bb9eea2fbead94ea`, 2499 bytes, 43 lines).
  (f) The rename itself — apply `.remedy-wt/f280-r12-rename.patch` (sha256
      `b3586932a1a570dfa26381c411c57bf747650ee5d401f463e47cf00a88be9911`, 82509 bytes, 47 files,
      192 insertions, 192 deletions) with `git apply --check` then `git apply`, from the repo
      root, against the primary checkout. This is the reviewer's own patch, already applied and
      fully tested (compile-checked, full suite, ruff, one mutation red-proof) TWICE in two
      independent from-scratch disposable worktrees before this round was authored — the
      committed diff must be the same bytes, not merely equivalent to what was reviewed.

Constraints:
  - Do not touch any file this block does not name. In particular: no file outside the 47 paths
    the patch names, and no file under `.data/` — if your own diff shows one, STOP, that is a
    block condition.
  - Do not edit DECISION F280 D6's own paragraph, or any other existing paragraph in
    `.agent/decisions.md` or `T2_F280.md` — this round only APPENDS/INSERTS beside them.
  - Commit order: C0a (authored carrier) -> C0b (last_block mirror) -> C1 (all five
    appends/inserts (a)-(e), ONE commit) -> C2 (apply the rename patch (f), ONE commit) -> C3
    (handoff). Do not split C2 further — this is a mechanical, single-substitution-rule rename
    across 47 files, the same size class AGENTS.md's mechanical-rename exception already covered
    for round 10's 28-path patch.
  - `git status --porcelain` empty before your first commit and after your last.
  - The mutation red-proof (G8 below) runs ONLY inside a disposable `git worktree`, never in the
    primary checkout (self-drive protocol G5); remove the worktree after and confirm with
    `git worktree list` in the handoff.

Done when (run every command from the repo root, primary checkout unless a gate says worktree):
  G1 TRANSPORT — `sha256sum .agent/authored/f280-r12.md` equals `sha256sum .agent/last_block.md`;
     `cmp` each of the six source files under `.remedy-wt/` against the corresponding section it
     produced in the committed target (for (d), `cmp` the inserted span, not the whole file; for
     (f), `cmp` the committed diff against the patch file itself via `git diff --numstat` path
     agreement, detailed in G4). Report PASS/FAIL, not a re-typed diff.
  G2 THE RECORD — after C1:
     `python3 -c "import re; d=open('.agent/live_review.md').read(); print(len(re.findall(r'^Gate: F\d+ R\d+ — ', d, re.M)), len(set(re.findall(r'^- (R-\d{4}) — ', d, re.M))), len(set(re.findall(r'^Done: (R-\d{4}) — ', d, re.M))))"`
     must read exactly `38 136 7` (unchanged open/done — no new finding). `grep -c "^## DECISION F280 D" .agent/decisions.md` must read `7`. `wc -l .agent/prose_slips.md` must read exactly `1027` (1025 at base plus the blank separator and the slip's own single line — the slip is written as ONE paragraph line, so the append is two lines, not one). `.agent/plan.md` must be exactly 43 lines with exactly one `## Goal`, one `## Current Step`, one `## Next Steps` and one `## Risks`.
  G3 THE SPLICE — after C1, `git diff --numstat HEAD~1..HEAD -- docs/` reads exactly
     `docs/roadmap/features/T2_F280.md` with `10` insertions and `0` deletions (a pure insert);
     `git diff HEAD~1..HEAD -- docs/roadmap/features/T2_F280.md` shows the new paragraph landing
     between D6's amendment and the `## T002` heading, with every other line of the file
     unchanged.
  G4 THE PATCH — after C2 (which immediately follows C1, so `HEAD~1` at this point IS C1),
     `git diff --numstat HEAD~1..HEAD -- apps/ packages/ tests/ scripts/ docs/system/ docs/guides/`
     reads exactly the 47 paths the patch names, 192 insertions / 192 deletions total, and is
     BYTE-IDENTICAL (`diff` over the two texts, zero output) to `.remedy-wt/f280-r12-rename.patch`.
  G5 THE BOUNDARY — after C2: `git diff --stat HEAD~1..HEAD` touches only the 47 named paths,
     none under `.data/`; a sweep for `\bflight_plan\b(?!\.py\b)` (bare token, excluding the
     module-filename citations) over `apps/ packages/ tests/ scripts/ docs/system/ docs/guides/`
     reads ZERO; `"flight_plan_v1"`, `FLIGHT_PLAN_SCHEMA_V`, `_MAX_FLIGHT_PLAN_TASKS` and
     `"flight_plan_approval"` each read ZERO over the same six directories; a count of
     `flight-plan` (hyphenated) over the same six directories reads exactly `56`, and a count of
     `"flight"]` / `get("flight"` over the same six directories reads exactly `25` — both equal
     to the reviewer's own pre-C2 measurement at `52f5fc49` (D7's deferred items, untouched
     by design).
  G6 TARGETED TESTS + LINT — `python3 -m pytest tests/cli/test_plan_approval.py tests/cli/test_decision_answers.py tests/orchestration/test_decision_evidence.py tests/orchestration/test_decision_inbox.py tests/orchestration/test_job_plan.py tests/orchestration/test_prompt_trace.py tests/schemas/test_job_plan_schema.py tests/ui_server/test_command_channel.py tests/ui_server/test_command_dispatch.py tests/cli/test_golden_path.py -q` reads all green; `python3 -m ruff check $(git diff --name-only HEAD~1..HEAD -- '*.py')` over the 38 touched Python files (resolved from the commit's own diff, not hand-listed) reads clean (zero errors).
  G7 FULL SUITE — `python3 -m pytest -q` (serial, no `-n auto`; the F275 xdist/UI-build race is
     a known class, D48-adjacent) over the WHOLE primary checkout reads `17654 passed, 23
     skipped` — the same totals round 10's own full-suite reading and the reviewer's own two
     pre-authoring dry runs both read.
  G8 THE RED-PROOF — in a disposable worktree under `.remedy-wt/r12-review-g8` (removed after,
     confirmed by `git worktree list`), mutate `task_plan_blocks_execution`'s
     `return approval` (the one inside the `if approval in ("pending", "rejected")` branch) to
     `return None`; the four nodes `test_run_refused_while_pending`,
     `test_run_refused_while_rejected`, `test_rejected_cli_exit_3`,
     `test_full_approval_sequence` in `tests/cli/test_plan_approval.py` go red and no other node
     in that file does; reverting restores `27 passed`.

Handback: completion report (state block, deviations, next steps) + rewrite
`.agent/handoff.md`. Attribute commits `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`.
Session number: this is SESSION 6 of F280, round 12.
──────────────────────────────────────────────────────────
