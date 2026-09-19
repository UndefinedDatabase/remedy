-- STEP R4 closure: integration gate -- F271 No more legacy: ownership, reachability, replace-is-delete --
Session 1 of F271 · round 4 · base `25c231b9` (branch `feature/f271-no-more-legacy`, pushed).

Goal: book round 3's verdict; give T2_F273.md the Acceptance lines round 2's owner assignment
owed; append the feature file's Built State; run the full suite ONCE and commit its transcript
(closure precondition 2, operator amendment amend0917-throughput (1)).

Read first, completely: AGENTS.md; docs/roadmap/STATUS_closure_protocol.md (Preconditions);
docs/agents/integration_gate.md; docs/agents/self_drive_protocol.md amendments amend0911-feedback
rule A and amend0917-throughput; `docs/roadmap/features/T2_F271.md`;
`.agent/authored/f270-closure-suite.txt` (the transcript's shape).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f271-r4/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md       sha256 4ca80d7ca0d517fab4eeeb93f99e1a1a193fdfe8979ab7860fd74a1f734320f6
  plan.md         sha256 4b9698a09d1c2f9f2ea855d09cf8eae23f6e78a856395317a9eab2a29996c1a3
  built_state.md  sha256 22586b8b3d73f36ed46060d60a6f441bf58f53c047b184bce32dff7254147acc
  f273_from.txt   sha256 37ca623591237771ae315f2f9ef445193e17356d428fbc5e79991c6057a7b404
  f273_to.txt     sha256 625baeeef1e3c35924a9e9ece5a0589880801e04dd1344a6f7773300c982d6e6
  block.md        this block (save it in C1 with the others; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of EVERY payload above, the block included, as
   `.agent/authored/f271-r4-<name>`; `.agent/live_review.md` := its `25c231b9` bytes + ledger.md;
   `.agent/plan.md` := plan.md; `docs/roadmap/features/T2_F273.md`: the bytes of f273_from.txt
   replaced by f273_to.txt (reviewer's containment test: `TO contains FROM: True`, an APPEND —
   FROM 1x before and after, and the lines C1's diff adds to that file are exactly the TO-only
   lines, in order; no FROM-zero count is owed).
C2 Built State — one commit: `docs/roadmap/features/T2_F271.md` := its `25c231b9` bytes +
   built_state.md (an append; nothing else in the file changes).
C3 the integration gate — ONE run of `python3 -m pytest -n auto -q` in the PRIMARY checkout (never
   a worktree), after C2, with nothing else running; then one commit adding
   `.agent/authored/f271-closure-suite.txt` holding the run's final summary line exactly as pytest
   printed it and, below it, every failed or errored node id, one per line, sorted (none -> the
   summary line alone). Do NOT repair anything after this run in this round and do not run the
   full suite a second time; a red run is the next round's input.
C4 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: "SESSION 1 of
   feature F271 · round 4 · rounds so far 4" plus one sentence of context self-assessment;
   per-commit tables with `git show --numstat` counts for every commit before C4; every gate's real
   output; the closure suite's summary line and bad-node list verbatim; `## Next` naming Phase 1
   rule 1, then the review of round 4, then the closure steps, and "Operator questions open: <the
   count you read>". Then `git push`.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test calls a real provider or starts a UI server; env vars only via `monkeypatch.setenv` or
   in-process `os.environ`; the shell denies `VAR=x cmd`, `cp` and `sed -i` — use python.
3. Never weaken an assertion or delete a test. A red in G1 or G2: stop, commit nothing half-done,
   report.
4. Build every edited file from `git show 25c231b9:<path>` bytes plus its payload.
5. Commit messages "F271 R4 C<n>: <summary>", blank line,
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Touch no line of `T2_F271.md` above the append; no `.claude/**`; no production code.

Done when (G1 and G2 after C2 and before C3; G3 is C3 itself; report literal output + real exit code):
G1 transport + state: payload digests matched; a python check prints True that
   `.agent/live_review.md` and `T2_F271.md` equal their `25c231b9` bytes + their payload, that
   `.agent/plan.md` equals plan.md, that `T2_F273.md` equals its `25c231b9` bytes with the pair
   applied (FROM counted 1 before), and that each `.agent/authored/f271-r4-*` copy equals its
   payload.
G2 `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_roadmap_index.py
   tests/cli/test_advertised_commands.py tests/cli/test_golden_path.py` -> summary line, 0 failed.
G3 the C3 run: its exit code, its summary line, the bad-node count, and the committed transcript's
   sha256.
G4 after the push: `git status --porcelain` empty and the local tip equals origin; `git worktree
   list` one row; the `remedy/job-*` branch count before C3 and after it — in your final message.
-- end of block --
