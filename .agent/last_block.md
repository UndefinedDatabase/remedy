── STEP R9/11 — F077 Autonomy watchdog (R8 verdict, session close) ───
Goal:        Put the R8 verdict and one reviewer finding on the record, then close the session with a handoff the next session can start from cold.
Bundle:      C0 save the block · C1 the R8 verdict, R-0386, and both mirrors · C2 the session-closing handoff.
Change:      EXACTLY five files — .agent/authored/f077-r9.md (new), .agent/last_block.md, .agent/live_review.md, .agent/plan.md, .agent/context.md, .agent/handoff.md. No production file, no test, no doc.
Constraints: No code this round. T002's wiring is R10's work and is NOT started here. Never write a `Done:` paragraph of your own.
──────────────────────────────────────────────────────────────────────

── C0 — save the block ───────────────────────────────────────────────
Write the block body verbatim to `.agent/authored/f077-r9.md` and commit it
ALONE; then `cp` it to `.agent/last_block.md` and commit that alone. Two commits,
per finding R-0385. Report `cmp` exit 0, the shared sha256 and the line count.

── C1 — the R8 verdict, finding R-0386, and both mirrors ─────────────
Findings persist FIRST. Append to the END of `.agent/live_review.md` in THIS
order: blank, FINDING-R386, blank, GATE-R8. Each slice is ONE physical line —
do not re-wrap. Change nothing above them. Shape: APPEND, deletion column 0.

>>> FINDING-R386 >>>
- R-0386 — Low — the reviewer stated two expected values in the R8 block and both were wrong, in the same block, on values it could have computed from the record it had already read. The open-finding count: the block's C4 told the worker to record SEVENTEEN after the round, when the arithmetic on its own numbers is eighteen open minus R-0384 resolved plus R-0385 registered, which is eighteen; the worker recomputed the set mechanically, got eighteen, reported it unadjusted and mirrored eighteen into `.agent/plan.md`. Gate 7: the block predicted that `grep -rn "watchdog" packages/orchestration/orchestrator_loop.py` would return "one pre-existing hit … a prose comment mentioning escalation", when the real answer is ZERO hits — the reviewer had grepped that file earlier in the session, saw a line matching a DIFFERENT pattern in the same combined command, and carried the misreading into the block instead of re-running the single grep it was about to order. Neither cost the round anything, and that is the load-bearing part of this finding rather than a mitigation of it: both gates were written in the probe form finding R-0327 prescribes — "report YOUR count", "report every hit", "do not adjust it to match this line" — so the worker's mechanical answer beat the reviewer's prediction by construction, exactly as designed. This is the sixth and seventh instance of the reviewer-arithmetic class (R-0327, R-0328, R-0336, R-0367 and now these two), and the pattern across all of them is identical: the reviewer states a number it could have measured. Fix, and it is narrower than "be careful": a block may state an expected value ONLY when the reviewer executed the exact command that produces it, at the commit the block starts from, immediately before emission. An expectation the reviewer did not run is not an expectation, it is a guess, and it goes into the block as a bare probe with no number attached. OPEN.
<<< FINDING-R386 <<<

>>> GATE-R8 >>>
Gate: R8 — PASS. Verification tier: round gate plus canary plus the state-file contract readers; no full-suite claim is made. Every value was re-executed by the reviewer against the disk rather than read out of the handback, and every one reproduces. Transport: `cmp .agent/authored/f077-r8.md .agent/last_block.md` exit 0 at shared sha256 `ed8c458f5cda183e7aa36d63a693ba982a01530176d40e6d58bcaf7e0bfecdca`, 224 lines — inside the 400-line cap and inside the 240-line ceiling, which is R-0385's fix working on its first outing after a 445-line block, and the ordered two-commit C0 meant the worker never had to discover the insertion cap mid-round. The record's line-anchored counts are `^Gate: R7 — PASS` 1, `^- R-0385 — ` 1, `^Done: R-0384 — ` 1, `^Landed: R-0384 — ` 1 (the Landed line correctly stays, because this round appended its resolution rather than rewriting it) and `^## Steps` 1; the C1 numstat is `6 0` with deletion column 0. The open set recomputed mechanically by the reviewer from the record is EIGHTEEN — R-0361, R-0362, R-0363, R-0364, R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378, R-0379, R-0380, R-0381, R-0382, R-0385 — from twenty registered minus two resolved, R-0383 and R-0384. That is the worker's number and NOT the block's seventeen: the worker recomputed rather than complied, which is what the probe form is for, and the reviewer's error is registered above as R-0386. DECISION F077 D8 was verified as the property it is rather than taken on trust: `grep -rn "watchdog" packages/orchestration/orchestrator_loop.py` returns ZERO hits, so `act_on_trips` genuinely has no call site, and `git diff --stat 7649a86b..HEAD -- docs/ apps/` produces no output at all. Scope held: `git diff --name-only 7649a86b..HEAD` returns exactly eight files, the seven the Change line names plus the handoff. The action was read line by line rather than inferred from its gate colour, and it implements D1 through D6 as written: the status write is guarded to `active` → `paused` so a terminal mission is never overwritten and an already-paused one is not rewritten; `open_mission_decisions` is read ONCE and the new record is appended to that in-memory list, which is what makes two trips of one class in a SINGLE call collapse to one decision rather than only across calls; the three attachment guards mirror `escalate_repeated_refusal` and each degrades to a note instead of raising, so the pause and the ledger entry survive a jobless mission; `safe_default` is empty, which matters more than it looks, because `escalation.auto_apply_safe_default` would otherwise let the automation the watchdog just stopped answer its own alarm; the entry carries `move={"kind": "watchdog_tripped", "payload": trip.to_json()}` with `context_digest=""` and the precedent zero cost; and the iteration number is the caller's when supplied and re-resolved per append when not, so a manual multi-trip audit numbers consecutively. The heavy imports sit inside the function body, `python3 -c "import packages.orchestration.watchdog"` exits 0, and no module-level edge to the loop was created. The twelve new tests were spot-read rather than counted: `test_answering_the_decision_lifts_the_suppression` round-trips the whole D3 claim — enqueue, assert suppressed, answer through `answer_task_decision`, save the job, then assert a THIRD call is unsuppressed and carries a DIFFERENT decision id — and `test_a_watchdog_entry_is_inert_to_a_later_watchdog_pass` asserts the positive control `verdict_without is not None` BEFORE asserting the with-and-without verdicts are equal, so it cannot pass vacuously on a tripwire that never fired. `test_the_rendered_ledger_shows_the_evidence_triple` asserts the literal rendered strings `kind:`, `what:`, `since_iteration:` and `numbers:`, which is D5's central claim proved against the renderer instead of restated. Suites re-run by the reviewer: `tests/orchestration/test_watchdog.py` `25 passed` against the 13 baseline, with `grep -c "def test_"` also 25 so no test is collected twice or skipped silently; `test_orchestrator_loop.py` with `test_mission_e2e.py` and `test_escalation.py` `286 passed`, identical to the worker's pre-C2 measurement of the same three files, which is the attributable proof that an unwired action changed nothing; the canary `42 passed`; `ruff check` over the two changed files `All checks passed!`; `git status --porcelain` empty and `git worktree list` one line. The worker's five declared deviations are all correct and three of them are catches rather than concessions: the open-count correction, the zero-hits correction, and the module docstring sentence "Deciding what to DO about a trip … is deliberately NOT here; that is F077 T002", which `act_on_trips` falsified the moment it landed in that same file — the worker repaired it in the same commit, which is exactly the R-0384 lesson applied without being told. Its refusal to write D7's watchdog clause into `mission_state.py` is also right: D7 says R8 adds that clause, the block's Change line forbids that file, and a worker that resolves a block-versus-decision conflict by widening its own scope is a worker that cannot be gated — flagging it was the correct move and the clause moves to the wiring round, where the caller it describes will actually exist. No block condition was hit — no fabricated value, no false live indicator, no missing changed-files table, no unverified completion claim, no silent scope change. What this gate does NOT say, per DECISION F077 D8 and stated here so no later reader mistakes a green round for a finished slice: `act_on_trips` has no caller, so nothing in a running mission reaches it, and this PASS is a statement about the action in isolation and about nothing else.
<<< GATE-R8 <<<

Then, in the SAME commit, update `.agent/plan.md` and `.agent/context.md`:
- Current Step becomes R9 — record the R8 verdict, register R-0386, close the
  session. Open findings: NINETEEN (the eighteen above plus R-0386). Next free
  id R-0387. Recompute that set yourself from `.agent/live_review.md` and report
  YOUR number; if it is not nineteen, report what you got and do not adjust it.
- Next Steps become: R10 wire `act_on_trips` into `run_mission`'s iteration seam
  and pay the four whole-ledger guards in `tests/orchestration/test_mission_e2e.py`
  plus D7's watchdog docstring clause; R11 T003 the manual CLI including the
  missing `mission resume` verb and the report surface; R12 integration gate
  then closure.
- `.agent/plan.md` stays at or under 49 physical lines with `## Goal` and
  `## Next Steps` intact. `.agent/context.md` keeps `## Active Branch` 1x,
  `feature/f077-autonomy-watchdog`, `Steps`, `F077`, `resource`, `pytest`, and
  its Steps line is extended through R9 with R10-R12 as above.

── C2 — the session-closing handoff ──────────────────────────────────
Rewrite `.agent/handoff.md` for a COLD start: the next session reads this file
and nothing else from this one. It carries the feature and round, the branch,
the R7/R8/R9 commit SHAs, the per-commit changed-files table for THIS round,
the real gate transcript below, the item-status table for C0-C2, the open count
and the next expected action. DECISION D15 applies if the mandated content does
not fit in 60 lines; name the real count and the cause, drop no section.

The Next section must say, in this order:
 1. Phase 1 rule 1 of `docs/agents/self_drive_protocol.md` is the next session's
    FIRST action: re-read `.agent/STOP` from disk BEFORE rule 2's Open PR Gate.
 2. Then rule 2. There is NO open PR for this branch; one is created at closure,
    not before. Nothing was merged this session.
 3. The next reviewed round is R10: wire `act_on_trips` into `run_mission` and
    pay the four `test_mission_e2e.py` guards.
 4. Name those four guards explicitly so the next session does not re-derive
    them, and name the fifth risk with them: the `move={}` KeyError subscript in
    `test_the_ledger_records_the_moves_in_the_order_they_happened` does NOT
    break on a watchdog entry, because DECISION F077 D5 gives that entry a real
    `move.kind` — but the list-equality in the same test and the
    `numbers == [1..7]` equality both still break on the extra entry, the
    universally-quantified `context_digest`/`cost` assertion breaks on the
    zero-cost shape, and `len(e2e["open_at_pause"]) == 1` breaks if the wired
    watchdog raises a decision during the scripted e2e run.
 5. R10 also writes DECISION F077 D7's watchdog clause into the
    `set_mission_status` and `_cmd_mission_set_status` docstrings, in the same
    commit as the call site, because only then is the claim true.
 6. Nineteen findings are open and none is a blocker; `integrity check` reports
    no open blocker/high findings.

── Gates — run every one, report the REAL value ──────────────────────
 1. `git status --porcelain` -> EMPTY; `git worktree list` -> 1 line.
 2. `cmp .agent/authored/f077-r9.md .agent/last_block.md` -> exit 0; report the
    shared sha256 and the line count.
 3. On `.agent/live_review.md`: `grep -c "^Gate: R8 — PASS"` -> 1,
    `grep -c "^- R-0386 — "` -> 1, `grep -c "^## Steps"` -> 1.
 4. Recompute the open set mechanically; name every id; report YOUR count.
 5. `git show --numstat <C1-sha> -- .agent/live_review.md` -> report both
    columns; the deletion column is 0.
 6. `git diff --stat <base>..HEAD -- packages/ apps/ tests/ docs/` -> EMPTY, no
    output at all, where <base> is `c4be17e8`.
 7. `git diff --name-only c4be17e8..HEAD` -> exactly the five Change-line files
    plus `.agent/handoff.md`.
 8. `wc -l .agent/plan.md` -> at or under 49 and equal to `grep -c ""`;
    `^## Goal` 1, `^## Next Steps` 1; the six `.agent/context.md` reader strings.
 9. `python3 -m pytest tests/cli/test_golden_path.py -q` -> baseline `42 passed`.
10. `python3 -m pytest tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py -q`
    -> baseline `142 passed`.
11. `python3 -m pytest tests/orchestration/test_watchdog.py -q` -> baseline
    `25 passed`; untouched this round.
12. `python3 -m apps.cli.main integrity check --json` -> report `passed`,
    `fail_count`, `check_count`.
13. Insertions per commit; none over 500.
14. Trailing-whitespace scan over every touched file -> none.
15. `test -e .agent/STOP` -> report absent or present, checked before you start
    and again at handback.
16. `git push -u origin feature/f077-autonomy-watchdog`. No `gh`, no PR.

Handback: completion report + rewrite `.agent/handoff.md`.
