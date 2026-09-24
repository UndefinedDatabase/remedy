-- STEP R10 CI repair -- F015 Interactive plan editing --
Session 2 of F015 · round 10 · base `0cac897c` (branch feature/f015-interactive-plan-editing,
pushed; pull request 274 into `main`, open, not a draft).

Goal: repair pull request 274's hosted CI under AGENTS.md's Open PR Gate exception
(amend0820-gate-autonomy): run `36005167608` on `0cac897c` failed one node on Python 3.10,
`tests/runtimes/test_supervisor_portability.py::TestPersistentLogPumpHealth::test_a_broken_helper_thread_fails_the_regression`,
because the prelude helper `_mark` creates its marker empty and writes the text afterwards.

Read first, completely: AGENTS.md (Commit Gate, Open PR Gate); the payload `ledger.md` (it books
round 9's verdict and registers R-1047 — the finding text is this round's spec).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f015-r10/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md      sha256 55dabba32d51b9cd7d5251d82b3520516e11ab850132ca7aad7b50de10604290
  plan.md        sha256 5bd3271dfd618060edc641029d2799a733b101821d6ce9c92b3ac1e184364908
  test_from.txt  sha256 3db573febeaeeec79ec8903129ea8ad78ef42dcfe135ddee64a329ede593b276
  test_to.txt    sha256 7855cf377007851a93cdc350596fa3d2f7046f25167543df11b3a2af2e3dd518
  probe.py       sha256 d8e104efac7b7f919a3ff39441425591b0dd937bb8ba8e088251495715c9f73c
  block.md       this block (save it in C1 with the others; report its line count and sha256)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of every payload, the block included, as
   `.agent/authored/f015-r10-<name>`; `.agent/live_review.md` := its `0cac897c` bytes + ledger.md;
   `.agent/plan.md` := plan.md.
C2 the repair — in `tests/runtimes/test_supervisor_portability.py` the bytes of test_from.txt
   (exactly 1x at `0cac897c`) replaced by the bytes of test_to.txt. The reviewer's containment
   test on the pair printed `TO contains FROM: False`, so a REWRITE: FROM 1x before and 0x after,
   TO 1x after. The prelude already imports `os`, `threading` and `time`, and it is a
   `str.format` template, which is why test_to.txt holds no brace. Nothing else in the file
   changes; no production file is touched.
C3 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md with every section
   it and AGENTS.md mandate, the item-status table included: Session section
   "SESSION 2 of feature F015 · round 10 · rounds so far 10" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 and C2, compared
   cell by cell against that tool; every gate's real output; open findings by distinct id (the
   script's own reading); `## Next` naming Phase 1 rule 1, then the review of round 10 and the
   Open PR Gate on pull request 274 after its hosted CI, and "Operator questions open: <the count
   you read from the file>". Then `git push origin feature/f015-interactive-plan-editing` (never
   force).

Constraints:
1. Change set: exactly the paths the Bundle names. Every commit < 500 inserted lines.
2. Build every edited file from `git show 0cac897c:<path>` bytes. The shell denies `VAR=x cmd`
   and `cp`; copy and compare bytes with python.
3. Never weaken an assertion or delete a test to pass. A red gate or an ambiguity -> stop, commit
   nothing half-done, write the handoff under AGENTS.md "If Blocked", report.
4. Do not merge, comment on or edit pull request 274; the reviewer does that.
5. Commit messages "F015 R10 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Work in the primary checkout `/home/decodeux/Repos/remedy`; only G4 uses a worktree.

Done when (G1 to G4 at C2, before C3; report literal output and the real exit code):
G1 transport + state: every payload digest matched; a python check prints True that
   `.agent/plan.md` equals plan.md, that `.agent/live_review.md` equals its `0cac897c` bytes +
   ledger.md, and that each `.agent/authored/f015-r10-*` copy equals its payload; and
   `open_finding_ids` of `scripts/rotate_live_review.py` over `.agent/live_review.md` at C1 —
   report the set it prints.
G2 the pair: `tests/runtimes/test_supervisor_portability.py` holds test_from.txt 0x and
   test_to.txt 1x; `git show --numstat` of C2 lists that file alone.
G3 `python3 -m pytest -q -p no:cacheprovider tests/runtimes/test_supervisor_portability.py
   tests/cli/test_golden_path.py` -> summary line, 0 failed (serial, no `-n`), and
   `python3 -m ruff check tests/runtimes/test_supervisor_portability.py` -> "All checks passed!".
G4 red/green probe in ONE disposable worktree `.remedy-wt/f015-r10-g4` at C2
   (`git worktree add --detach .remedy-wt/f015-r10-g4 <C2 sha>`), run from its root:
   `python3 -B /home/decodeux/Repos/remedy/.remedy-wt/f015-r10/probe.py
   /home/decodeux/Repos/remedy/.remedy-wt/f015-r10/`. It prints three readings and whether it
   restored the file: CONTROL must be exit 0; RED (the old `_mark` with the error marker paused
   one second before its write) must be exit 1 failing
   `test_a_broken_helper_thread_fails_the_regression`; GREEN (the new `_mark` with the same
   pause before its rename) must be exit 0. Report all four lines verbatim; then
   `git worktree remove .remedy-wt/f015-r10-g4` and show `git worktree list`.
G5 after the push: `git status --porcelain` empty and the local tip equals
   `origin/feature/f015-interactive-plan-editing` — reported in your final message only, since
   the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput); the hosted CI re-runs it on the push.
-- end of block --
