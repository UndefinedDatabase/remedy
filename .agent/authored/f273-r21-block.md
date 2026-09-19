-- STEP R21 closure: integration gate -- F273 Findings paydown v1 --
Session 3 of F273 · round 21 · base `c8b91d87` (the round 20 handoff, branch
`feature/f273-findings-paydown-v1`).

Goal: book round 20's verdict and three resolutions, append the feature file's Built State, and run
the full suite ONCE, committing its transcript (closure precondition 2, operator amendment
amend0917-throughput (1)).

Read first, completely: AGENTS.md; docs/roadmap/STATUS_closure_protocol.md (Preconditions);
docs/agents/integration_gate.md; docs/agents/self_drive_protocol.md amendment amend0917-throughput;
`.agent/authored/f271-closure-suite.txt` (the transcript's shape).

PAYLOADS: reviewer-authored, gitignored scratch in `.remedy-wt/f273-r21/`. Verify each sha256 before
use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md       sha256 cf2428f4cfad30db51677cf1cabfbb4eea347220e52b94f0c02d104a61fcf157
  plan.md         sha256 9862db7cd0b0e251e14b625509b2f9eb62e2f28bb446e0f147322798a2ac48df
  built_state.md  sha256 5d94312ae39224892169414df4b9082fd9c0386edf70c5ee70b59e9ba9e918b5
  next.md         sha256 10b87fc5f32b326dea0a939072d449b7eba751a10a56798cf99be95ce00042c6
  block.md        this block (save it; report its sha256 and line count)

Bundle (commit order):
C1 bookkeeping, one commit: byte copies of ledger.md, plan.md, built_state.md and block.md as
   `.agent/authored/f273-r21-<name>`; `.agent/live_review.md` := its `c8b91d87` bytes + ledger.md;
   `.agent/plan.md` := plan.md. Before this commit, compare the saved block copy's line count and
   sha256 with the block text you were given, and report both.
C2 Built State, one commit: `docs/roadmap/features/T2_F273.md` := its `c8b91d87` bytes +
   built_state.md (an append; nothing else in the file changes).
C3 the integration gate: ONE run of `python3 -m pytest -n auto -q` in the PRIMARY checkout (never a
   worktree), after C2, with nothing else running, through a script whose `env=` drops
   `REMEDY_OLLAMA_HOST` and `OLLAMA_HOST`. Then one commit adding
   `.agent/authored/f273-closure-suite.txt`, holding the run's final summary line exactly as pytest
   printed it and, below it, every failed or errored node id, one per line, sorted (none -> the
   summary line alone), and after them the count of output lines starting `R-0803:` as the line
   `R-0803 lines: <n>`. Do NOT repair anything after this run in this round, and do not run the full
   suite a second time; a red run is the next round's input.
C4 handoff: rewrite `.agent/handoff.md` per docs/agents/handback_template.md. Its Session section
   reads "SESSION 3 of feature F273 · round 21 · rounds so far 21", plus one sentence of context
   self-assessment. Include per-commit tables with `git show --numstat` counts for C1 to C3, every
   gate's real output, the closure suite's transcript verbatim, and open findings by distinct id
   (`count_open_findings`) on the committed ledger. Record under External actions that the branch
   `remedy/job-81ec65896729405c` still exists; a research helper's probe created it before round 16,
   and nobody may delete it without the operator. End with a `## Next` section whose body is next.md
   byte for byte, followed by the line "Operator questions open: <the count you read from the
   file>". Then `git push`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test may call a real provider or start a UI server of its own accord beyond what the suite does.
   The shell denies `VAR=x cmd`, `cp`, loops, `$( )`, `$VAR` (including `$?`), heredocs and `cd`
   before git. Use `git -C <path>` and small python scripts under `.remedy-wt/f273-r21/`, with names
   prefixed `wk_` and an explicit `cwd=`. Never use `git stash`.
3. Never weaken an assertion or delete a test. A red in G1 or G2: stop, commit nothing half-done,
   and report.
4. Build every edited file from `git show c8b91d87:<path>` bytes plus its payload.
5. Commit messages read "F273 R21 C<n>: <summary>", then a blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Touch no line of `T2_F273.md` above the append; no `.claude/**`; no production code. Never list,
   read or write any `.data/`. Never run the `remedy` CLI, `scripts/remedy_smoke.sh`,
   `scripts/make_review_zip.sh` or the self-use runner. Create no branch and delete no branch.

Done when (G1 and G2 after C2 and before C3; G3 is C3 itself; report literal output and the real
exit code):
G1 transport + state: payload digests matched. A python check prints True that
   `.agent/live_review.md` and `T2_F273.md` equal their `c8b91d87` bytes + their payload, that
   `.agent/plan.md` equals plan.md, that each `.agent/authored/f273-r21-*` copy equals its payload,
   and that `git rev-parse <C2>:docs` prints 6f24191f3f591dc5acf1a2f5c88f057d83514371 (the
   reviewer's dry-run object).
G2 `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_roadmap_index.py
   tests/cli/test_golden_path.py` -> summary line, 0 failed.
G3 the C3 run: its exit code, its summary line, the bad-node count, the `R-0803:` line count, and
   the committed transcript's sha256.
G4 after the push: `git status --porcelain` is empty, the local tip equals origin, `git worktree list`
   shows the primary checkout and no worktree of yours, and `git branch --list "remedy/job-*"` counts
   37 before C3 and after it. Report this in your final message only.
-- end of block --
