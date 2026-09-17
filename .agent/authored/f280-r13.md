── STEP R13/n — F280 ────────────────────────────────────
Goal: book round 12's independently-reviewed PASS (Gate: F280 R12, one prose slip, no new
R-id), author DECISION F280 D8, and land the first of DECISION F280 D7's two deferred items:
the prompt-trace `kind` values `"flight-plan"`/`"flight-plan-retry"` become
`"task-plan"`/`"task-plan-retry"`.

Bundle:
  1. Copy this block to `.agent/authored/f280-r13.md` and mirror to `.agent/last_block.md`.
  2. Append the Gate:F280 R12 entry to `.agent/live_review.md`, append the prose-slip line to
     `.agent/prose_slips.md`, append DECISION F280 D8 to `.agent/decisions.md`, insert the
     feature-file amendment into `docs/roadmap/features/T2_F280.md`, and replace `.agent/plan.md`
     — all five pre-built and pre-verified by the reviewer.
  3. Apply the reviewer's pre-built, pre-tested rename patch (`.remedy-wt/f280-r13-rename.patch`)
     with `git apply`, verbatim, in ONE commit.
  4. Run the done-when gates, write the handoff, commit, push.

Change — exact files, exact source:
  All source files below live under `/home/decodeux/Repos/remedy/.remedy-wt/` (repo-root
  scratch, NOT a git ref — plain files on disk in the primary checkout's own working tree).
  Copy each BYTE-FOR-BYTE with `shutil.copyfile` or equivalent; do not retype.

  (a) `.agent/live_review.md` — append, IN THIS ORDER, to the end of the current file (which
      currently ends in exactly one `\n`):
        1. one `\n` byte (blank-line paragraph separator)
        2. the exact bytes of `.remedy-wt/gate_r12_entry.txt` (sha256
           `868e6a1babfcc8428e740b37d64fe60e4bee8dccfa8e432e20da61cefaab1354`, 5170 bytes,
           already ends in its own single `\n`)
      i.e. `new_bytes = old_bytes + b"\n" + gate_r12_entry`. There is no new R-id to register.
  (b) `.agent/prose_slips.md` — append, IN THIS ORDER, to the end of the current file (which
      currently ends in exactly one `\n`):
        1. one `\n` byte (blank-line paragraph separator)
        2. the exact bytes of `.remedy-wt/prose_slip_r12.txt` (sha256
           `db3c0de1694de892e9b8fce1bc3df86107ef0587c1a2ad1cc5d7f40c5bc3b069`, 604 bytes,
           already ends in its own single `\n`)
  (c) `.agent/decisions.md` — append, IN THIS ORDER, to the end of the current file (which
      currently ends in exactly one `\n`):
        1. one `\n` byte (blank-line paragraph separator)
        2. the exact bytes of `.remedy-wt/decision_f280_d8.txt` (sha256
           `5e34015f7d657656161d6c08ab2d5d7b9c611e332e3238d2a29896a75c9f6f70`, 3096 bytes,
           already ends in its own single `\n`)
  (d) `docs/roadmap/features/T2_F280.md` — INSERT the exact bytes of
      `.remedy-wt/t2_f280_amendment_d8.txt` (sha256
      `bf6e122be4b8aaca2ced4793514c747f94b0a86c7953f914ca5b63e9d408b88d`, 667 bytes, starts with
      its own leading `\n` and ends in its own single trailing `\n`) immediately after the byte
      sequence ending `...mechanical rename can reach it safely.\n` (the end of DECISION F280
      D7's amendment paragraph) and immediately before the pre-existing blank line that precedes
      the `## T002` heading. Locate the exact splice point yourself by reading the file — do not
      guess a line number; the insertion is `prefix + amendment_bytes + suffix` where `prefix`
      ends in `mechanical rename can reach it safely.\n` and `suffix` begins with the existing
      blank line then `## T002 — Descriptions, role labels, help wrapping, tests`.
  (e) `.agent/plan.md` — REPLACE THE WHOLE FILE with the exact bytes of
      `.remedy-wt/f280-r13-plan.md` (sha256
      `448c886309f8f56fb046bc89a4d8e5546142d7499a67bd4b331152d0909a9a9a`, 2525 bytes, 44 lines).
  (f) The rename itself — apply `.remedy-wt/f280-r13-rename.patch` (sha256
      `b2666a35bfe7923f5b77703bf06f63968c9d5af35833de832a079def181d54d0`, 1234 bytes, 2 files,
      2 insertions, 2 deletions) with `git apply --check` then `git apply`, from the repo root,
      against the primary checkout. This is the reviewer's own patch, already applied and fully
      tested (targeted test, ruff, full suite) in a disposable worktree before this round was
      authored — the committed diff must be the same bytes, not merely equivalent to what was
      reviewed.

Constraints:
  - Do not touch any file this block does not name. In particular: only
    `packages/orchestration/job_plan.py` and `tests/orchestration/test_prompt_trace.py` change
    under `apps/`, `packages/`, `tests/` or `scripts/` this round — if your own diff shows
    anything else, STOP, that is a block condition.
  - Do not edit DECISION F280 D7's own paragraph, or any other existing paragraph in
    `.agent/decisions.md` or `T2_F280.md` — this round only APPENDS/INSERTS beside them.
  - Commit order: C0a (authored carrier) -> C0b (last_block mirror) -> C1 (all five
    appends/inserts (a)-(e), ONE commit) -> C2 (apply the rename patch (f), ONE commit) -> C3
    (handoff).
  - `git status --porcelain` empty before your first commit and after your last.
  - The mutation red-proof (G6 below) runs ONLY inside a disposable `git worktree`, never in the
    primary checkout (self-drive protocol G5); remove the worktree after and confirm with
    `git worktree list` in the handoff. Run pytest FROM WITHIN the worktree directory (a plain
    `cd` first), never by pointing a pytest invocation in the primary checkout at a worktree
    path — that silently tests the primary checkout's own unmutated code instead (round 12's
    reviewer caught this exact mistake mid-review).

Done when (run every command from the repo root, primary checkout unless a gate says worktree):
  G1 TRANSPORT — `sha256sum .agent/authored/f280-r13.md` equals `sha256sum .agent/last_block.md`;
     `cmp` each of the six source files under `.remedy-wt/` against the corresponding section it
     produced in the committed target (for (d), `cmp` the inserted span, not the whole file; for
     (f), byte-identity is checked in G3 below). Report PASS/FAIL, not a re-typed diff.
  G2 THE RECORD — after C1:
     `python3 -c "import re; d=open('.agent/live_review.md').read(); print(len(re.findall(r'^Gate: F\d+ R\d+ — ', d, re.M)), len(set(re.findall(r'^- (R-\d{4}) — ', d, re.M))), len(set(re.findall(r'^Done: (R-\d{4}) — ', d, re.M))))"`
     must read exactly `39 136 7` (unchanged open/done — no new finding). `grep -c "^## DECISION F280 D" .agent/decisions.md` must read `8`. `wc -l .agent/prose_slips.md` must read exactly `1029` (1027 at base plus the blank separator and the slip's own single line). `.agent/plan.md` must be exactly 44 lines with exactly one `## Goal`, one `## Current Step`, one `## Next Steps` and one `## Risks`. `git diff --numstat HEAD~1..HEAD -- docs/` (after C1) reads exactly `docs/roadmap/features/T2_F280.md` with `9` insertions and `0` deletions, landing between D7's amendment and the `## T002` heading with every other line unchanged.
  G3 THE PATCH — after C2 (which immediately follows C1, so `HEAD~1` at this point IS C1),
     `git diff --numstat HEAD~1..HEAD -- apps/ packages/ tests/ scripts/ docs/system/ docs/guides/`
     reads exactly two paths — `packages/orchestration/job_plan.py`,
     `tests/orchestration/test_prompt_trace.py` — 2 insertions / 2 deletions total, and is
     BYTE-IDENTICAL (`diff` over the two texts, zero output) to
     `.remedy-wt/f280-r13-rename.patch`. `git diff --stat HEAD~1..HEAD` shows no other path.
  G4 THE BOUNDARY — after C2: a count of `"flight-plan"`/`"flight-plan-retry"` (quoted, exact)
     over `apps/ packages/ tests/ scripts/ docs/system/ docs/guides/` reads ZERO; a count of the
     bare hyphenated word `flight-plan` (unquoted, prose) over the same six directories reads
     exactly `54` (D5's third owed item, untouched by design); `"task-plan"`/`"task-plan-retry"`
     (quoted, exact) reads exactly `2`.
  G5 TARGETED TESTS + LINT — `python3 -m pytest tests/orchestration/test_prompt_trace.py
     tests/cli/test_golden_path.py -q` reads all green; `python3 -m ruff check
     packages/orchestration/job_plan.py tests/orchestration/test_prompt_trace.py` reads clean.
  G6 FULL SUITE + RED-PROOF — `python3 -m pytest -q` (serial, no `-n auto`) over the WHOLE
     primary checkout reads `17654 passed, 23 skipped` (same totals as round 12). Then, in a
     disposable worktree under `.remedy-wt/r13-review-g6` (removed after, confirmed by
     `git worktree list`), edit `packages/orchestration/job_plan.py:181` to revert ONLY the
     non-retry value — `kind = "task-plan-retry" if is_parse_retry else "flight-plan"` (leaving
     the retry arm alone; this simulates a rename applied to the test but missed on one branch
     of the production code) — and, running from WITHIN the worktree, confirm
     `pytest tests/orchestration/test_prompt_trace.py -q` shows exactly one failure,
     `TestSegmentManifest::test_the_cli_flight_plan_recorder_passes_the_composed_prompt`, with
     every other node in the file green; reverting the edit restores `43 passed`.

Handback: completion report (state block, deviations, next steps) + rewrite
`.agent/handoff.md`. Attribute commits `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`.
Session number: this is SESSION 6 of F280, round 13.
──────────────────────────────────────────────────────────
