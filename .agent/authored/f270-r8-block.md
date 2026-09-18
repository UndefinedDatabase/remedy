-- STEP R8 CI repair -- F270 History apply: one commit per task, merge on demand --
Session 1 of F270 · round 8 · base `b91fb1ec` (branch feature/f270-history-apply, pushed; pull
request 258 into `main`, open).

Goal: repair pull request 258's hosted CI under AGENTS.md's Open PR Gate exception
(amend0820-gate-autonomy): run `35401706742` on `b91fb1ec` failed one node,
`tests/runtimes/test_dev_server.py::TestReadiness::test_delayed_readiness`, because the test's
clock starts after the server it times was launched.

Read first, completely: AGENTS.md (Commit Gate, Open PR Gate); the payload `ledger.md` (it books
round 7's verdict and registers R-0979 — the finding text is this round's spec).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f270-r8/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md      sha256 025805f5ae22432965e1ef54c91a392e5f91e4e25880cfd7741f26a36aec19e3
  plan.md        sha256 33e4f71225e6f8cec1247dffaf17c6af166a78b1c561bdb175d272a611177dc9
  test_from.txt  sha256 7a6383054565c780aba87f2c4f85c60ddd9971675d9d2679eee5ef7f6bf718a2
  test_to.txt    sha256 a9c01472ac64b903048265dcfe608f70d3ba18b1f856966c476958160b33bbc4
  block.md       this block (save it in C1 with the others; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of every payload, the block included, as
   `.agent/authored/f270-r8-<name>`; `.agent/live_review.md` := its `b91fb1ec` bytes + ledger.md;
   `.agent/plan.md` := plan.md.
C2 the repair — in `tests/runtimes/test_dev_server.py` the bytes of test_from.txt (exactly 1x at
   `b91fb1ec`) replaced by the bytes of test_to.txt. The reviewer's containment test on the pair
   printed `TO contains FROM: False`, so a REWRITE: FROM 1x before and 0x after, TO 1x after. The
   file already imports `time`. Nothing else in the file changes; no production file is touched.
C3 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 1 of feature F270 · round 8 · rounds so far 8" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 and C2; every gate's
   real output; open findings by distinct id; `## Next` naming Phase 1 rule 1, then the review of
   round 8 and the Open PR Gate on pull request 258 after its hosted CI, and "Operator questions
   open: <the count you read from the file>". Then `git push` (never force).

Constraints:
1. Change set: exactly the paths the Bundle names. Every commit < 500 inserted lines.
2. Build every edited file from `git show b91fb1ec:<path>` bytes. The shell denies `VAR=x cmd` and
   `cp`; copy and compare bytes with python.
3. Never weaken an assertion or delete a test to pass. A red gate or an ambiguity → stop, commit
   nothing half-done, report.
4. Do not merge, comment on or edit pull request 258; the reviewer does that.
5. Commit messages "F270 R8 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.

Done when (G1 to G4 at C2, before C3; report literal output and the real exit code):
G1 transport + state: every payload digest matched; a python check prints True that
   `.agent/plan.md` equals plan.md, that `.agent/live_review.md` equals its `b91fb1ec` bytes +
   ledger.md, and that each `.agent/authored/f270-r8-*` copy equals its payload.
G2 the pair: `tests/runtimes/test_dev_server.py` holds test_from.txt 0x and test_to.txt 1x;
   `git show --numstat` of C2 lists that file alone.
G3 `python3 -m pytest -q -p no:cacheprovider tests/runtimes/test_dev_server.py
   tests/cli/test_golden_path.py tests/ui_server/test_dashboard_contract.py
   tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py` → summary
   line, 0 failed (serial, no `-n`), and `python3 -m ruff check tests/runtimes/test_dev_server.py`
   → "All checks passed!".
G4 mutation red-proof in ONE disposable worktree under `.remedy-wt/` at C2, run from its root with
   `python3 -B -m pytest -q -p no:cacheprovider tests/runtimes/test_dev_server.py::TestReadiness`,
   `__pycache__` purged first: the UNMUTATED control (must be exit 0); then in
   `packages/runtimes/dev_server.py` `wait_ready`, the line
   `            if READY_STATUS_MIN <= status <= READY_STATUS_MAX:` (exactly 1x there) made
   `            if True:` → `test_delayed_readiness` red. Report both exit codes and the failing
   ids; remove the worktree and show `git worktree list`.
G5 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput); the hosted CI re-runs it on the push.
-- end of block --
