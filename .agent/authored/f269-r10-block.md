-- STEP R10 closure: integration gate -- F269 Contract & contract templates --
Session 2 of F269 · round 10 · base `6d10133e` (branch feature/f269-contract, pushed).

Goal: book round 9's verdict and R-0971's resolution; pin Acceptance bullet 3's first half
exactly; append the feature file's Built State; run the full suite ONCE and commit its
transcript (closure precondition 2, amend0917-throughput (1)).

Read first, completely: AGENTS.md; docs/roadmap/STATUS_closure_protocol.md (Preconditions);
docs/agents/integration_gate.md; docs/agents/self_drive_protocol.md amendment
amend0917-throughput; `docs/roadmap/features/T2_F269.md` (Acceptance);
`tests/cli/test_do_sequence_cli.py` from its line `# ── F269 T003` to the next test after
`test_contract_website_with_an_extra_requirement_adds_planner_criteria_and_drops_none`.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f269-r10/`. Verify each
sha256 before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md       sha256 79c3a8c83f56a3fd2578ea51f5841886592a1ca90d7b21bfd57d646684faa0e6
  plan.md         sha256 f8ebf09778cf26db94a9b707072cb658ce999cf0d5e92444ea52f936fa4aa24f
  built_state.md  sha256 d1facc3e17fdd8420991bf3a4df6eefc2e0a6f3ae08a2202dbf1ad2a5538ac77
  block.md        this block (save it as `.agent/authored/f269-r10-block.md`; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of the payloads as `.agent/authored/f269-r10-<name>`;
   `.agent/live_review.md` := `git show 6d10133e:.agent/live_review.md` bytes + ledger.md;
   `.agent/plan.md` := plan.md.
C2 the acceptance pin — one commit, test only: in `tests/cli/test_do_sequence_cli.py`, the test
   `test_contract_website_with_an_extra_requirement_adds_planner_criteria_and_drops_none` is
   renamed `test_contract_website_with_an_extra_requirement_adds_one_planner_criterion_naming_it`,
   and its last line `assert len(_contract_by_origin(data, "planner")) >= 1` becomes exactly
   two lines: `[planner] = _contract_by_origin(data, "planner")` and
   `assert "lists the release checklist" in planner["text"]`. Nothing else in the file changes.
   (T2_F269.md Acceptance bullet 3 says "PLUS one criterion with origin: planner"; the reviewer's
   dry run at `6d10133e` read exactly one planner criterion, whose text carries the whole order.)
C3 Built State — one commit: `docs/roadmap/features/T2_F269.md` := `git show
   6d10133e:docs/roadmap/features/T2_F269.md` bytes + built_state.md (an append; nothing else in
   the file changes).
C4 the integration gate — ONE run of `python3 -m pytest -n auto -q` in the PRIMARY checkout
   (never a worktree), serially after C3, with nothing else running; then one commit adding
   `.agent/authored/f269-closure-suite.txt` holding the run's final summary line exactly as
   pytest printed it and, below it, every failed or errored node id, one per line, sorted
   (none -> the summary line alone). Do NOT repair anything after this run in this round, and
   do not run the full suite a second time; a red run is the next round's input.
C5 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md:
   "SESSION 2 of feature F269 · round 10 · rounds so far 10" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for every commit before
   C5; every gate's real output; the closure suite's summary line and bad-node list verbatim;
   `## Next` naming Phase 1 rule 1, then the review of round 10, then the closure steps, and
   "Operator questions open: <the count you read>". Then `git push`.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test calls a real provider or starts a UI server; env vars only via `monkeypatch.setenv`
   or in-process `os.environ`; the shell denies `VAR=x cmd`, `cp` and `sed -i` — use python.
3. Never weaken an assertion or delete a test. A red in G1 to G3: stop, commit nothing half-done,
   report.
4. Build every appended file from `git show 6d10133e:<path>` bytes plus the payload.
5. Commit messages "F269 R10 C<n>: <summary>", blank line,
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Touch no line of `T2_F269.md` above the append; no `.claude/**`; no production code.

Done when (G1 to G3 after C3 and before C4; G4 is C4 itself; report literal output + real exit code):
G1 transport + state: payload digests matched; a python check prints True that
   `.agent/live_review.md` and `T2_F269.md` equal their `6d10133e` bytes + their payload, and that
   `.agent/plan.md` equals plan.md.
G2 `python3 -m pytest -q -p no:cacheprovider tests/cli/test_do_sequence_cli.py
   tests/cli/test_golden_path.py tests/docs/` -> summary line, 0 failed.
G3 `python3 -m ruff check tests/cli/test_do_sequence_cli.py` -> "All checks passed!".
G4 the C4 run: its exit code, its summary line, the bad-node count, and the committed transcript's
   sha256.
G5 after the push: `git status --porcelain` empty and the local tip equals origin; `git worktree
   list` one row; the `remedy/job-*` branch count before C4 and after it — in your final message.
-- end of block --
