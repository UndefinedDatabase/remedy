-- STEP R22 closure repair 1: the corpus guard -- F273 Findings paydown v1 --
Session 3 of F273 · round 22 · base `7e717bc4` (the round 21 handoff, branch
`feature/f273-findings-paydown-v1`).

Goal: book round 21's verdict, register R-0997, land DECISION F273 D21, repair the closure suite's one
bad node exactly as the reviewer's dry run did, and run the full suite ONCE more, committing its
transcript (operator amendment amend0917-throughput (2), the shrinking rule).

Read first, completely: AGENTS.md; the payload `decisions.md` (DECISION F273 D21); the amend0917-throughput
paragraph of docs/agents/self_drive_protocol.md; `.agent/authored/f273-closure-suite.txt` at `7e717bc4`.

PAYLOADS: reviewer-authored, gitignored scratch. Verify each sha256 before use; any mismatch -> stop
and report. Apply byte-exact; never retype.
  `.remedy-wt/f273-r22/ledger.md`     sha256 4b5f2ef973344035ee2e5d68d1b7cdf09f974bc43df62948a8ac90a82ef49346
  `.remedy-wt/f273-r22/plan.md`       sha256 dd98ce0f4d8c6593ca2862511e268e1910bae42780b50dd338db6aa33c317d99
  `.remedy-wt/f273-r22/decisions.md`  sha256 5c4f4fa5b49db9885d06f0d8dfee28dde744360bf4177936ce17c790fd81774d
  `.remedy-wt/f273-r22/next.md`       sha256 17e4830cda59de05010585ad8d68ddfff4aa68f708bf2ffc82efee7f6086523e
  `.remedy-wt/f273-s3/r22_fix.diff`   sha256 091184c81efb0c782065b49e709b78212f412c54bd3e07cdbe06f12a7e931be9
  `.remedy-wt/f273-r22/block.md`      this block (save it; report its sha256 and line count)

Bundle (commit order):
C1 bookkeeping, one commit: byte copies of ledger.md, plan.md, decisions.md and block.md as
   `.agent/authored/f273-r22-<name>`; `.agent/live_review.md` and `.agent/decisions.md` := each one's
   `7e717bc4` bytes + ledger.md and decisions.md; `.agent/plan.md` := plan.md. Before this commit,
   compare the saved block copy's line count and sha256 with the block text you were given, and
   report both.
C2 R-0997: `git apply` r22_fix.diff (one test file).
C3 the full suite, once: ONE run of `python3 -m pytest -n auto -q` in the PRIMARY checkout (never a
   worktree), after C2, with nothing else running, through a script whose `env=` drops
   `REMEDY_OLLAMA_HOST` and `OLLAMA_HOST`. Then one commit adding
   `.agent/authored/f273-closure-suite-r22.txt` in the shape of `.agent/authored/f273-closure-suite.txt`:
   the run's final summary line exactly as pytest printed it; below it every failed or errored node
   id, one per line, sorted (none -> nothing); then the line `R-0803 lines: <n>` counting output lines
   that start `R-0803:`. Leave `.agent/authored/f273-closure-suite.txt` untouched. Repair nothing
   after this run, and do not run the full suite a second time.
C4 handoff: rewrite `.agent/handoff.md` per docs/agents/handback_template.md. Its Session section
   reads "SESSION 3 of feature F273 · round 22 · rounds so far 22", plus one sentence of context
   self-assessment. Include per-commit tables with `git show --numstat` counts for C1 to C3, every
   gate's real output, the new transcript verbatim, the SHRINKING READING (the previous bad set, the
   new bad set, whether the new set is a strict subset, and any node newly bad), open findings by
   distinct id (`count_open_findings`) on the committed ledger, and one `Landed: R-0997` line naming
   C2, in the handoff only; never write a `Done:` line of your own. Record under External actions that
   the branch `remedy/job-81ec65896729405c` still exists; nobody may delete it without the operator.
   End with a `## Next` section whose body is next.md byte for byte, followed by the line "Operator
   questions open: <the count you read from the file>". Then `git push`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. The shell denies `VAR=x cmd`, `cp`, loops, `$( )`, `$VAR` (including `$?`), heredocs and `cd`
   before git. Use `git -C <path>` and small python scripts under `.remedy-wt/f273-r22/`, with names
   prefixed `wk_` and an explicit `cwd=`. Never use `git stash`.
3. Never weaken an assertion or delete a test. A red in G1 or G2: stop, commit nothing half-done, and
   report.
4. Build every edited `.agent/` file from `git show 7e717bc4:<path>` bytes plus its payload.
5. Commit messages read "F273 R22 C<n>: <summary>", then a blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. No `.claude/**`, no production code. Never list, read or write any `.data/`. Never run the `remedy`
   CLI, `scripts/remedy_smoke.sh`, `scripts/make_review_zip.sh` or the self-use runner. Create no
   branch and delete no branch.

Done when (G1 and G2 after C2 and before C3; G3 is C3 itself; report literal output and the real
exit code):
G1 transport + state: payload digests matched. A python check prints True that
   `.agent/live_review.md` and `.agent/decisions.md` equal their `7e717bc4` bytes + their payload,
   that `.agent/plan.md` equals plan.md, that each `.agent/authored/f273-r22-*` copy equals its
   payload, that `git show --name-only --format=` of C2 lists exactly the path `git apply --numstat`
   reads from the diff, and that `git rev-parse <C2>:tests` prints
   395d7718d05267dcfb2c9b1fa6ef48d62dd5fcfd (the reviewer's dry-run object).
G2 `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_job_plan_state_reads.py
   tests/docs/ tests/cli/test_golden_path.py` -> summary line, 0 failed; and
   `python3 -m ruff check . --output-format concise` -> "All checks passed!".
G3 the C3 run: its exit code, its summary line, the bad-node list, the `R-0803:` line count, the
   committed transcript's sha256, and the shrinking reading.
G4 after the push: `git status --porcelain` is empty, the local tip equals origin, `git worktree list`
   shows the primary checkout alone, and `git branch --list "remedy/job-*"` counts 37 before C3 and
   after it. Report this in your final message only.
-- end of block --
