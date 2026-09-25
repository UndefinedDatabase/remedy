-- STEP R9 CI repair -- F024 Phase timeline with scrubber --
Session 2 of F024 · round 9 · base `953d5715` (branch feature/f024-phase-timeline-scrubber,
pushed; pull request 279 into `main`, open, not a draft).

Goal: repair pull request 279's hosted CI under AGENTS.md's Open PR Gate exception
(amend0820-gate-autonomy): run `36103781836` on `953d5715` failed one node on Python 3.10 and
3.12, `tests/ui_server/test_timeline_scrub_live.py::test_a_live_jobs_ledger_scrubs_to_exactly_each_prefix`,
because vitest colours its summary wherever `CI` is set and the test's pattern reads plain text.

Read first, completely: AGENTS.md (Commit Gate, Open PR Gate); the payload `ledger.md` (it books
round 8's verdict and registers R-1048 — the finding text is this round's spec).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f024-r9/`. Verify each one's
line count, byte count and sha256 before use; any mismatch -> stop and report. Apply byte-exact;
never retype. Lines = newline count.
  ledger.md      lines=4 bytes=3564 sha256=2341d8942c7bee612f367e875a70822dab1403385ca1a4d796a3015774230865
  plan.md        lines=33 bytes=1209 sha256=945048b323acfa52a57d5b785b763e67ad33cf976fd89964276b9fe395696fb6
  test_from.txt  lines=1 bytes=63 sha256=193ba4a7a33c634e0888602138575d2ee8d7a2fc45fcf2b36829b40e090fbbdd
  test_to.txt    lines=2 bytes=183 sha256=a9f2796f998db11a82a33f113957f0a1906a4d4a6701504f8f0ca28a6d3512c5
  probe.py       lines=52 bytes=2153 sha256=982d88bb694f1cc634a7d77379241f818cf5e4ff6520c4b2de46b53cd7e47325
  block.md       this block; your delegation message states its line count and sha256 — measure
                 both, report them beside the given ones, and stop if either differs (R-0954).

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of every payload, the block included, as
   `.agent/authored/f024-r9-<name>`; `.agent/live_review.md` := its `953d5715` bytes + ledger.md;
   `.agent/plan.md` := plan.md. Subject `F024 R9 C1: book round 8, register R-1048, copy the
   round's block and payloads`. Expected by `git show --numstat`, as the reviewer's simulation
   printed it: this block's line count plus 110, that is the block copy's own lines and 4/0
   `.agent/authored/f024-r9-ledger.md`, 33/0 `.agent/authored/f024-r9-plan.md`, 52/0
   `.agent/authored/f024-r9-probe.py`, 1/0 `.agent/authored/f024-r9-test_from.txt`, 2/0
   `.agent/authored/f024-r9-test_to.txt`, 4/0 `.agent/live_review.md`, 14/9 `.agent/plan.md`.
C2 the repair — in `tests/ui_server/test_timeline_scrub_live.py` the bytes of test_from.txt
   (exactly 1x at `953d5715`) replaced by the bytes of test_to.txt. The reviewer's containment
   test on the pair printed `TO contains FROM: False`, so a REWRITE: FROM 1x before and 0x after,
   TO 1x after. The file already imports `re`. Nothing else in the file changes; no production
   file is touched. Subject `F024 R9 C2: strip vitest's colour escapes before reading its
   summary (R-1048)`. Expected by `git show --numstat`: 2/1, that file alone.
C3 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md with every section
   it and AGENTS.md mandate, the item-status table included: Session section
   "SESSION 2 of feature F024 · round 9 · rounds so far 9" plus one sentence of context
   self-assessment; per-commit tables for C1 and C2 whose `+/-` cells are the
   `git show --numstat` readings, compared cell by cell against that tool; every gate's real
   output; open findings by distinct id (the script's own reading); `## Next` naming Phase 1
   rule 1, then the review of round 9 and the Open PR Gate on pull request 279 after its hosted
   CI, and "Operator questions open: <the count you read from the file>". Subject `F024 R9 C3:
   rewrite handoff for round 9`. Then `git push origin feature/f024-phase-timeline-scrubber`
   (never force).

Constraints:
1. Change set: exactly the paths the Bundle names. Every commit < 500 inserted lines.
2. Build every edited file from `git show 953d5715:<path>` bytes. The shell denies `VAR=x cmd`,
   `cp` and `cd <dir> && git ...`; copy and compare bytes with python (`shutil.copyfile`), and
   use `git -C <path>`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`.
3. Never weaken an assertion or delete a test to pass. A red gate or an ambiguity -> stop, commit
   nothing half-done, write the handoff under AGENTS.md "If Blocked", report.
4. Do not merge, comment on or edit pull request 279; the reviewer does that.
5. Commit messages as the Bundle states, blank line, then
   `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Work in the primary checkout `/home/decodeux/Repos/remedy`; only G4 uses a worktree. Leave
   every existing worktree (the reviewer's `.remedy-wt/f024-r9-sim` and the older `f015-*`,
   `f020-*`, `f023-*`, `f024-*`, `f284-*` and `job-*` ones) and every stash alone.
7. Do NOT run the full suite (amend0917-throughput); the hosted CI re-runs it on the push.

Done when (G1 to G4 at C2, before C3; report literal output and the real exit code):
G1 transport + state: every payload reading matched; a python check prints True that
   `.agent/plan.md` equals plan.md, that `.agent/live_review.md` equals its `953d5715` bytes +
   ledger.md, and that each `.agent/authored/f024-r9-*` copy equals its payload (the block copy
   against `.remedy-wt/f024-r9/block.md`); and `open_finding_ids` of
   `scripts/rotate_live_review.py` over `.agent/live_review.md`'s text at C1 — the reviewer's
   simulation read `['R-1008', 'R-1048']`; report the set you read.
G2 the pair: at C2 `tests/ui_server/test_timeline_scrub_live.py` holds test_from.txt 0x and
   test_to.txt 1x, and reads bytes=3637 sha256=7a8287268b0af80542069274bfd8554fa7b21a5574eb20e1973389497c63cddc;
   `git show --numstat` of C2 lists that file alone.
G3 in the primary checkout at C2, serially:
   `python3 -m pytest -q -p no:cacheprovider -rs tests/ui_server/test_timeline_scrub_live.py
   tests/cli/test_golden_path.py tests/orchestration/test_live_review_rotation.py
   tests/orchestration/test_integrity_gate.py` -> summary line, 0 failed. The reviewer's sim
   worktree read `86 passed, 1 skipped`, the skip being the live scrub node for want of
   `apps/ui/node_modules`; in the primary checkout that node must PASS, not skip, so expect
   87 passed and report every SKIPPED line. Then
   `python3 -m ruff check tests/ui_server/test_timeline_scrub_live.py` -> "All checks passed!",
   and `python3 -m apps.cli.main integrity check --json` -> all six checks `pass`, `fail_count` 0.
G4 red/green probe in ONE disposable worktree `.remedy-wt/f024-r9-g4` at C2
   (`git worktree add --detach .remedy-wt/f024-r9-g4 <C2 sha>`), with that worktree as the
   working directory: `python3 -B /home/decodeux/Repos/remedy/.remedy-wt/f024-r9/probe.py
   /home/decodeux/Repos/remedy/.remedy-wt/f024-r9/` (a python wrapper under
   `.remedy-wt/f024-r9-worker/` passing `cwd=` is fine; never `cd` your own shell there). It links the primary `apps/ui/node_modules` in, prints three readings,
   restores the file and removes the link. The reviewer read, against its sim tree: CONTROL
   (the C2 file, `CI` unset) exit 0, 1 passed; RED (the old line, `CI=true`) exit 1, 1 failed,
   the failing node the hosted run's; GREEN (the C2 file, `CI=true`) exit 0, 1 passed;
   `restored byte-identical: True`; `link removed: True`. Report every line verbatim; then
   `git worktree remove .remedy-wt/f024-r9-g4` and show `git worktree list`.
G5 after C3 and the push: `git status --porcelain` empty, the local tip equals
   `origin/feature/f024-phase-timeline-scrubber`, and `git log --oneline -n 4` shows C3, C2, C1
   and `953d5715` — reported in your final message only, since the handoff commit precedes it.
-- end of block --
