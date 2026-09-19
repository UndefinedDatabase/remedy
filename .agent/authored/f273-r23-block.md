-- STEP R23 closure round A, first half: bookings and the self-use run -- F273 Findings paydown v1 --
Session 4 of F273 · round 23 · base `83ee29bb` (the round 22 handoff, branch
`feature/f273-findings-paydown-v1`, pushed).

Goal: book round 22's verdict, the resolutions of R-0997 and R-0803 and the registration of R-0998;
then run the closure's one self-use item (closure precondition 6) to its approval gate, mirror that
run into the token ledger, and record the ledger's rows against the run's provider calls, which is
the reading R-0807's resolution needs.

Read first, completely: AGENTS.md; docs/roadmap/STATUS_closure_protocol.md, Precondition 6; F271's
self-use convention, commit `5781a607` and `.agent/selfuse_f271/` (the evidence file shapes the
payload `run_selfuse.py` reproduces).

PAYLOADS: reviewer-authored, gitignored scratch in `.remedy-wt/f273-r23/`. Verify each sha256 before
use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md            sha256 49132af94114670e210726bbabbc9f4f2ee97a12f21fecf5059c394ecef0d44d
  plan.md              sha256 3e86993db9c123ac8ac8eaf4e743ec35277a6fcffe8800ebd24b666e0ff64b81
  next.md              sha256 11f8fbe59139e6fb07d8773efe219240255554c0dbbf6eff6d8fba9eb4598f36
  run_selfuse.py       sha256 cf502769c3478fa8ebc2ca069bce4f42606d5cc5581e185fec8abc3db4ce5668
  integrity_probe.py   sha256 0eecbaf425881e7bdff138d10c9db14c9804f4a43a40b62b14e30f0f82a45544
  block.md             this block (save it; report its sha256 and line count)

Bundle (commit order):
C1 bookkeeping, one commit: byte copies of ledger.md, plan.md, run_selfuse.py and block.md as
   `.agent/authored/f273-r23-<name>`; `.agent/live_review.md` := its `83ee29bb` bytes + ledger.md;
   `.agent/plan.md` := plan.md. Before this commit, compare the saved block copy's line count and
   sha256 with the block text you were given, and report both.
C2 self-use item, one commit: from the primary checkout's root, run
   `python3 -B .remedy-wt/f273-r23/run_selfuse.py` once, with no environment change. It calls the
   generator, runs the item to the approval gate (never applied), mirrors the job into the ledger
   and writes `.agent/selfuse_f273/`. Commit that directory with the change the generator wrote to
   `scripts/self_use_queue.json`, and nothing else. Do NOT set `consumed_by`; round B's closure
   commit does. Do NOT write any finding: quote the files verbatim in the handoff; the reviewer
   registers what they show. If the script raises, commit nothing for C2 and report the traceback.
C3 handoff: rewrite `.agent/handoff.md` per docs/agents/handback_template.md. Its Session section
   reads "SESSION 4 of feature F273 · round 23 · rounds so far 23", plus one sentence of context
   self-assessment. Include per-commit tables with `git show --numstat` counts for C1 and C2, every
   gate's real output, and VERBATIM: the script's stdout, `ledger_rows.txt`, `run_defects.txt`,
   `result_state.txt` and `execution_config.txt`. Open findings by distinct id
   (`count_open_findings`) on the ledger at C1. Under External actions: the `remedy/job-*` branch
   count before and after C2 and the name of every branch C2 created; that
   `remedy/job-81ec65896729405c` still exists; nobody may delete a branch without the operator. End
   with a `## Next` section whose body is next.md byte for byte, then the line "Operator questions
   open: <the count you read from the file>". Then `git push`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. The shell denies `VAR=x cmd`, `cp`, loops, `$( )`, `$VAR` (including `$?`), heredocs and `cd`
   before git. Use `git -C <path>` and small python scripts under `.remedy-wt/f273-r23/`, named
   `wk_*.py`, with an explicit `cwd=`. Never use `git stash`.
3. Never weaken an assertion or delete a test. A red in G1 or G2: stop, commit nothing half-done,
   and report.
4. Build every edited `.agent/` file from `git show 83ee29bb:<path>` bytes plus its payload.
5. Commit messages read "F273 R23 C<n>: <summary>", then a blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. No `.claude/**`, no production code, no README.md, no `docs/`. The data root is touched only by
   the functions `run_selfuse.py` calls; never list, read or write it yourself. Never run the
   `remedy` CLI, `scripts/remedy_smoke.sh` or `scripts/make_review_zip.sh`. Create no branch
   yourself and delete none. Do not run the full suite (amend0917-throughput (1)).

Done when (report literal output and the real exit code):
G1 after C1: payload digests matched; a python check prints True that `.agent/live_review.md`
   equals its `83ee29bb` bytes + ledger.md, that `.agent/plan.md` equals plan.md, and that each
   `.agent/authored/f273-r23-*` copy equals its payload.
G2 after C2: `python3 -m pytest -q -p no:cacheprovider tests/docs/
   tests/orchestration/test_roadmap_index.py tests/cli/test_golden_path.py
   tests/orchestration/test_self_use_queue.py tests/orchestration/test_self_use_generator.py
   tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py`
   -> summary line, 0 failed.
G3 C2's run: the script's exit code and stdout; `git show --name-only --format=` of C2 lists only
   paths under `.agent/selfuse_f273/` and `scripts/self_use_queue.json`; `git worktree list` after
   the run.
G4 after C2: `python3 -B .remedy-wt/f273-r23/integrity_probe.py` -> its output. A FAIL there is
   the expected reading while R-0807 is open and stops nothing; report it.
G5 after the push: `git status --porcelain` is empty, the local tip equals origin, `git worktree
   list` shows the primary checkout alone, and the `remedy/job-*` branch count. Report this in your
   final message only.
-- end of block --
