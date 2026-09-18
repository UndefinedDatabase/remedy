-- STEP R5 closure: integration gate -- F270 History apply: one commit per task, merge on demand --
Session 1 of F270 · round 5 · base `6ca5c361` (branch feature/f270-history-apply, pushed).

Goal: book round 4's verdict; append the feature file's Built State; run the full suite ONCE and
commit its transcript (closure precondition 2, operator amendment amend0917-throughput (1)).

Read first, completely: AGENTS.md; docs/roadmap/STATUS_closure_protocol.md (Preconditions);
docs/agents/integration_gate.md; docs/agents/self_drive_protocol.md amendment
amend0917-throughput; `docs/roadmap/features/T2_F270.md`; `.agent/authored/f269-closure-suite.txt`
(the transcript's shape).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f270-r5/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md       sha256 1481d3c7cc6a1d9c13dd8859d3234756f360daddc0ba8b79a4f5b75c35020432
  plan.md         sha256 1818311fc1c236b2014538f2194e41588c5afb0ea466cfad3be89edcb46fb3c5
  built_state.md  sha256 2faa356fcab8c7518071d4f9971a0ac8b0d96e09adddbd217c307aa9cdd139c4
  block.md        this block (save it in C1 with the others; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of EVERY payload above, the block included, as
   `.agent/authored/f270-r5-<name>`; `.agent/live_review.md` := its `6ca5c361` bytes + ledger.md;
   `.agent/plan.md` := plan.md.
C2 Built State — one commit: `docs/roadmap/features/T2_F270.md` := its `6ca5c361` bytes +
   built_state.md (an append; nothing else in the file changes).
C3 the integration gate — ONE run of `python3 -m pytest -n auto -q` in the PRIMARY checkout (never
   a worktree), after C2, with nothing else running; then one commit adding
   `.agent/authored/f270-closure-suite.txt` holding the run's final summary line exactly as pytest
   printed it and, below it, every failed or errored node id, one per line, sorted (none -> the
   summary line alone). Do NOT repair anything after this run in this round and do not run the
   full suite a second time; a red run is the next round's input.
C4 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: "SESSION 1 of
   feature F270 · round 5 · rounds so far 5" plus one sentence of context self-assessment;
   per-commit tables with `git show --numstat` counts for every commit before C4; every gate's real
   output; the closure suite's summary line and bad-node list verbatim; `## Next` naming Phase 1
   rule 1, then the review of round 5, then the closure steps, and "Operator questions open: <the
   count you read>". Then `git push`.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test calls a real provider or starts a UI server; env vars only via `monkeypatch.setenv` or
   in-process `os.environ`; the shell denies `VAR=x cmd`, `cp` and `sed -i` — use python.
3. Never weaken an assertion or delete a test. A red in G1 or G2: stop, commit nothing half-done,
   report.
4. Build every appended file from `git show 6ca5c361:<path>` bytes plus the payload.
5. Commit messages "F270 R5 C<n>: <summary>", blank line,
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Touch no line of `T2_F270.md` above the append; no `.claude/**`; no production code.

Done when (G1 and G2 after C2 and before C3; G3 is C3 itself; report literal output + real exit code):
G1 transport + state: payload digests matched; a python check prints True that
   `.agent/live_review.md` and `T2_F270.md` equal their `6ca5c361` bytes + their payload, that
   `.agent/plan.md` equals plan.md, and that each `.agent/authored/f270-r5-*` copy equals its
   payload.
G2 `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_roadmap_index.py
   tests/cli/test_advertised_commands.py tests/cli/test_golden_path.py` -> summary line, 0 failed.
G3 the C3 run: its exit code, its summary line, the bad-node count, and the committed transcript's
   sha256.
G4 after the push: `git status --porcelain` empty and the local tip equals origin; `git worktree
   list` one row; the `remedy/job-*` branch count before C3 and after it — in your final message.
-- end of block --
