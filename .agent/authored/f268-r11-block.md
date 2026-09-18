-- STEP R11 closure: integration gate -- F268 remedy do: the one-command start --
Session 2 of F268 · round 11 · base `a70e66a8` (branch feature/f268-remedy-do, pushed).

Goal: book round 10's verdict and a prose slip; rewrite the three product-spine pins of the
old quick start; append the feature file's Built State; run the full suite ONCE and commit its
transcript (closure precondition 2, amend0917-throughput (1)).

Read first, completely: AGENTS.md; docs/roadmap/STATUS_closure_protocol.md (Preconditions);
docs/agents/integration_gate.md; docs/agents/self_drive_protocol.md amendment
amend0917-throughput; `tests/cli/test_product_spine.py` (`TestJobFirstHappyPath`,
`TestDoRunHelpAlignment`); `apps/cli/grouped.py` `_QUICK_START`; DECISION F268 D15 in
`.agent/decisions.md`.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f268-r11/`. Verify each
sha256 before use; any mismatch -> stop and report. Apply byte-exact.
  ledger.md       sha256 e8b876c75915abd982c3fae3c9985472244edf710dc88773c1ca14e523136c60
  slips.md        sha256 0f6b9da4528f06e5852917e83f92a902216e47cdc0b9ed2ce392e905e02c0539
  plan.md         sha256 55394aac841dc74ef2e58276596a8e00fd8ab90150a67bde4e8c8a9694e53674
  built_state.md  sha256 394e69eec481caa8256759801bd97c5df923b47e366f9ff04b85df99db9bc89c
  block.md        this block (save it as `.agent/authored/f268-r11-block.md`; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of the payloads as `.agent/authored/f268-r11-<name>`;
   `.agent/live_review.md` := `git show a70e66a8:.agent/live_review.md` bytes + ledger.md;
   `.agent/prose_slips.md` := `git show a70e66a8:.agent/prose_slips.md` bytes + slips.md;
   `.agent/plan.md` := plan.md.
C2 pins — one commit, BY DESIGN under DECISION F268 D15, never asserting less than before about
   what each pinned: in `tests/cli/test_product_spine.py`
   `TestJobFirstHappyPath::test_happy_path_starts_with_do` asserts the first numbered line that
   runs work is a `remedy do` line (lines one and two register and check health, D15);
   `::test_happy_path_has_job_show` asserts the quick start lists the jobs (`remedy job list`,
   D15 line five) — rename it to say so; `TestDoRunHelpAlignment::test_happy_path_uses_do_run`
   asserts a numbered `remedy do` line exists. The reviewer's untruncated sweep at `a70e66a8`
   (`git grep -c _QUICK_START`) found it in `apps/cli/grouped.py`, `tests/cli/test_cli_ux.py`,
   `tests/cli/test_product_spine.py` and `tests/test_cli_execution_loop_closure.py` only.
C3 Built State — one commit: `docs/roadmap/features/T2_F268.md` := `git show
   a70e66a8:docs/roadmap/features/T2_F268.md` bytes + built_state.md (an append; nothing else in
   the file changes).
C4 the integration gate — ONE run of `python3 -m pytest -n auto -q` in the PRIMARY checkout
   (never a worktree), serially after C3, with nothing else running; then one commit adding
   `.agent/authored/f268-closure-suite.txt` holding the run's final summary line exactly as
   pytest printed it and, below it, every failed or errored node id, one per line, sorted
   (none -> the summary line alone). Do NOT repair anything after this run in this round, and
   do not run the full suite a second time; a red run is the next round's input.
C5 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md:
   "SESSION 2 of feature F268 · round 11 · rounds so far 11"; per-commit tables with
   `git show --numstat` counts for every commit before C5; every gate's real output; the
   closure suite's summary line and bad-node list verbatim. Then `git push`.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test calls a real provider or starts a UI server; env vars only via `monkeypatch.setenv`;
   the shell denies `VAR=x cmd` and `cp` — copy bytes with python.
3. Never weaken an assertion or delete a test to pass beyond C2. A red in G1 to G3 you can repair
   inside this change set without touching a DECISION: repair it in its own commit before C4 and
   name it. Any other red before C4: stop and report.
4. Build every appended file from `git show a70e66a8:<path>` bytes plus the payload.
5. Commit messages "F268 R11 C<n>: <summary>", blank line,
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Touch no line of `T2_F268.md` above the append; no `.claude/**`; no production code.

Done when (G1 to G3 after C3 and before C4; G4 is C4 itself; report literal output + real exit code):
G1 transport + state: payload digests matched; python byte checks print True for the three
   appends against their `a70e66a8` bytes; `.agent/plan.md` byte-equal to plan.md.
G2 `python3 -m pytest -q -p no:cacheprovider tests/cli/test_product_spine.py
   tests/cli/test_cli_ux.py tests/test_cli_execution_loop_closure.py tests/cli/test_quick_start.py
   tests/cli/test_golden_path.py tests/docs/` -> 0 failed.
G3 `python3 -m ruff check tests/cli/test_product_spine.py` -> "All checks passed!".
G4 the C4 run: its exit code, its summary line, the bad-node count, and the committed transcript's
   sha256.
G5 `git status --porcelain` empty and the local tip equals origin after the push; `git worktree
   list` one row; the `remedy/job-*` branch count before C4 and after it.
-- end of block --
