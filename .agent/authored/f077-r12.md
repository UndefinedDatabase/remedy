── STEP T002-repair/2 — F077 Autonomy watchdog · R12 ─────────────

Goal:        Repair the one red test to the invariant this codebase actually
             holds, retire the reviewer's wrong diagnosis on the record, and
             leave the branch green.

Bundle:
  C0a  save this block verbatim to `.agent/authored/f077-r12.md`
  C0b  `cp` it to `.agent/last_block.md`
  C1   FINDINGS FIRST, own commit: append the authored FINDING-R391 slice, then
       the authored GATE-R11 slice, then the authored DONE-R388 slice, then
       REPLACE the `Landed: R-0390` line with the authored DONE-R390 slice —
       all in `.agent/live_review.md`, in that order
  C2   append the authored DECISION-D11 slice to `.agent/decisions.md`
  C3   the repair: pair LEDGER-TEST in `tests/orchestration/test_orchestrator_loop.py`
  C4   mirror the round into `.agent/plan.md` and `.agent/context.md`
  C5   handback: rewrite `.agent/handoff.md` — this is the session's LAST round

Change:      EXACTLY these files, and nothing beyond them:
             `.agent/authored/f077-r12.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/decisions.md`,
             `tests/orchestration/test_orchestrator_loop.py`,
             `.agent/plan.md`, `.agent/context.md`, `.agent/handoff.md`.
             Eight files. NO production file is touched this round. If you find
             yourself editing `orchestrator_loop.py` or `watchdog.py`, stop —
             the block is wrong and you should report that instead.

Why the reviewer reversed itself, so you can check it rather than trust it:
finding R-0388 claimed a duplicated iteration number broke the invariant "one
entry per iteration, numbered once". That invariant does not exist. `_record`
has ELEVEN call sites in `run_mission`, and two of them fire in the SAME
iteration on a path that has been green and shipped since F075 R-0190: the
executed move's entry, and then the blocked-completion escalation's entry
directly below it, both carrying the same `iteration`. The shipped test
`TestTheSecondBlockedCompletionEscalates::test_two_blocked_completions_in_a_row_escalate`
drives exactly that shape. So an entry's `iteration` says which iteration it
BELONGS to; it was never a unique key. Verify both claims yourself — grep
`_record(iteration` in `packages/orchestration/orchestrator_loop.py` and report
the count, and read the R-0190 escalation path — before you apply C3. If the
two same-iteration `_record` calls are NOT both reachable in one pass, stop and
report it, because then this repair is wrong too.

Constraints:
  - AGENTS.md Commit Gate before EVERY commit. 500-INSERTION cap per commit.
  - `.agent/plan.md` stays UNDER 50 lines. It is 45 now; keep it there.
  - You never author a `Done:` paragraph. The two below are the reviewer's text
    and you apply them verbatim. Write no `Landed:` line this round.
  - Do NOT change any threshold default, any config key, `act_on_trips`,
    `watchdog_pass`, `evaluate_ledger`, or the `run_mission` call site.
  - Repair ONLY the one named test. Every other test in
    `tests/orchestration/test_orchestrator_loop.py` is correct and untouched —
    in particular `test_every_entry_carries_a_context_digest_and_cost` directly
    below it runs `max_iterations=2`, which is under the no_progress threshold
    of 3, so it does not trip and needs nothing.
  - `.agent/STOP`: re-check from disk before you start and again at handback.
  - Any destructive check runs ONLY in a disposable `git worktree` under
    `.remedy-wt/`, never in the primary checkout.

Done when: every gate below has been RUN by you and its REAL value recorded.
"Green" as a word is a finding. The round's base commit is `28c50487`.

  1.  `git status --porcelain` → EMPTY. `git worktree list` → exactly 1 line.
  2.  `cmp .agent/authored/f077-r12.md .agent/last_block.md` → exit 0. Report
      the shared sha256 and the line count.
  3.  `grep -c '^Gate: R11 — ' .agent/live_review.md` → 1.
      `grep -c '^- R-0391 — ' .agent/live_review.md` → 1.
      `grep -c '^Done: R-0388 — ' .agent/live_review.md` → 1.
      `grep -c '^Done: R-0390 — ' .agent/live_review.md` → 1.
      `grep -c '^Landed: ' .agent/live_review.md` → 0.
      `grep -c '^## Steps' .agent/live_review.md` → 1.
      `grep -c '^## DECISION F077 D11 ' .agent/decisions.md` → 1.
  4.  Recompute the open-finding set MECHANICALLY — every `^- R-\d+ — `
      paragraph minus every `^Done: R-\d+ — ` line — and report the count and
      the names. Report what you measure, unadjusted.
  5.  `grep -c '_record(iteration' packages/orchestration/orchestrator_loop.py`
      → report the number, and name the two line numbers that fire in one pass.
  6.  `grep -c 'test_one_entry_per_iteration_numbered_from_one' tests/ -r`
      → run BEFORE C3 and report it, so the rename in pair LEDGER-TEST is known
      to break no other reference. If it is anything other than 1, STOP.
  7.  THE GATE THIS ROUND EXISTS FOR:
      `python3 -m pytest tests/orchestration/test_orchestrator_loop.py -q`
      → base `28c50487` FIRST, then your HEAD. Report BOTH real numbers.
  8.  `python3 -m pytest tests/orchestration/test_watchdog.py tests/orchestration/test_mission_e2e.py -q`
      → report the number. It was 52 in one invocation at base; this round must
      not move it.
  9.  `ruff check` over ONLY the files this round changed → exact output. Note
      that `tests/orchestration/test_orchestrator_loop.py` carries a
      PRE-EXISTING `I001`; report it as pre-existing and do NOT fix it, that is
      outside this round's change.
  10. Canary: `python3 -m pytest tests/cli/test_golden_path.py -q` → number.
  11. `python3 -m pytest tests/ -q -k "dashboard_contract or resource_safety or test_runner"`
      → number. Before authoring either state edit, grep every test that reads
      that path and validate the draft against ALL of it (R-0162).
  12. `python3 -c "import sys; sys.argv=['remedy','integrity','check','--json']; from apps.cli.grouped import main; sys.exit(main())"`
      → report `passed`, `fail_count`, `check_count`, `high_blockers_open`.
  13. `wc -l .agent/plan.md` → under 50.
  14. Insertions per commit via `git show --numstat`, per commit. None over 500.
  15. `test -e .agent/STOP` → ABSENT or PRESENT, before the round and at handback.
  16. `git push -u origin feature/f077-autonomy-watchdog`. No `gh`, no PR.
  17. Trailing-whitespace scan over every touched file → none; all
      newline-terminated.

Handback:    completion report + rewrite `.agent/handoff.md`, item-status table
             covering C0a C0b C1 C2 C3 C4 C5, and this Fortschritt line verbatim:
             `~75 % (T001 ✅ · T002 ✅ verdrahtet und grün · T003 offen) — Schätzung`
             ≤60 lines, or a "Deviations, declared" line naming the real count
             and the mandated content (DECISION D15). Never drop a section.
             This is the session's LAST round, so the handoff's Next section
             must name, in this order: (1) Phase 1 rule 1 of
             docs/agents/self_drive_protocol.md — re-read `.agent/STOP` from
             disk BEFORE rule 2's Open PR Gate; (2) rule 2, noting there is NO
             open PR for this branch and one is created at closure, not before;
             (3) that the next reviewed round is R13, T003's manual CLI
             including the missing `mission resume` verb (DECISION F077 D4) and
             the report surface; (4) that R14 is the integration gate then
             closure; (5) the open-finding count and names you measured at gate
             4 and the next free id; and (6) that R12's own verdict is not on
             disk by construction (planner_reviewer_prompt.md §4.13 — the last
             round of a session cannot record the gate on itself) and will be
             written by R13's first commit.

── AUTHORED SLICES — apply byte for byte ─────────────────────────

Each of the four live_review slices is ONE physical line, separated from its
neighbour by one blank line, matching the file's existing shape. DONE-R390
REPLACES the existing `Landed: R-0390` line; the other three are appends.

<<<BEGIN FINDING-R391>>>
- R-0391 — Medium — the reviewer raised R-0388 and decided DECISION F077 D10 on an invariant that does not exist, and it took a worker's refusal to apply the resulting order to expose it. R-0388 asserted that "one entry per iteration, numbered once" was load-bearing, citing two tests that assert it and `next_iteration_index`, which reads one past the highest recorded value. What the reviewer never did was read the code that WRITES the field it was reasoning about: `_record` has eleven call sites inside `run_mission`, and two of them — the executed move's entry and the blocked-completion escalation's entry directly below it — fire in the SAME pass with the same `iteration`, a shape that has been green and shipped since F075 R-0190 and that `TestTheSecondBlockedCompletionEscalates::test_two_blocked_completions_in_a_row_escalate` drives on purpose. The invariant was inferred from two test names and never checked against the eleven writers. This is pre-emission checklist item 8 — read the code that PRODUCES the value a gate asserts — applied to the watchdog's own number and to nothing else, and it is the second item-8-class miss on this branch after R-0387's narrow item-7 grep, which is why it is Medium and not Low. The compounding cost is on the record and is the point of the finding: the wrong diagnosis produced DECISION F077 D10, D10 ordered a code change to production behaviour that was already correct, and D10's safety premise was ALSO false — the worker measured a scripted stop-after-trip run at `[1, 2, 3, 4, 4]` with the ordered repair against `[1, 2, 3, 3, 4]` without it, because `run_mission`'s safe point calls `_record` BEFORE the top-of-loop status check that was supposed to make the collision impossible. Two independent errors in one diagnosis, and the only thing that stopped either from landing was that the block made its own premise a checkable precondition and the worker checked it. From here, a finding that asserts an invariant names every writer of the field it constrains, counted mechanically, before the finding is authored — not after a repair is ordered against it.
<<<END FINDING-R391>>>

<<<BEGIN GATE-R11>>>
Gate: R11 — PASS, for a round that deliberately did NOT complete its ordered change set. Verification tier: round gate plus canary plus the state-file contract readers plus `integrity check`; no full-suite claim is made. The block made its own safety premise a checkable precondition — "if you find a path where the loop DOES record after a trip, stop and report it, because then this whole repair is wrong" — and the worker found one, measured it, and halted at C3 with C0a, C0b, C1, C2, C4 and C5 landed. That is the block's stop clause working exactly as written, so the incomplete change set is compliance and not a deviation, and the round PASSES on it. The reviewer verified the refutation independently rather than accepting it: `run_mission`'s safe point calls `_record(iteration, "", {}, outcome, ...)` inside `if signal is not None:` and RETURNS from there, all of it above the `load_mission` and `if mission.status != MISSION_STATUS_ACTIVE:` check that DECISION F077 D10 assumed would stop the run first — so a stop requested in the window after a trip does write an entry, at the number the trip just took. The worker's measurement of `[1, 2, 3, 4, 4]` with the ordered repair against `[1, 2, 3, 3, 4]` without it is therefore sound, and D10 would have moved a duplicate rather than removed one. Reading the same code to check that refutation surfaced the larger error underneath it: `grep -c '_record(iteration'` returns eleven call sites, of which the executed move's and the blocked-completion escalation's fire in one pass at one number, which means R-0388's invariant never existed and R10's wiring was correct as committed. That is registered as R-0391 against the reviewer, R-0388 is resolved as a misdiagnosis, and DECISION F077 D11 supersedes D10 without any production change. Everything else in R11 was re-run by the reviewer at this HEAD rather than read: `tests/orchestration/test_orchestrator_loop.py` `1 failed, 195 passed` — unchanged from its base, which is correct for a round that changed no code — `tests/orchestration/test_watchdog.py` `28 passed`, `tests/orchestration/test_mission_e2e.py` `24 passed`, the canary `42 passed`, `wc -l .agent/plan.md` `45`, the tree clean and `git worktree list` one line. Two things the round did that are worth recording because a less careful round would have done neither: it transcribed DECISION F077 D10 verbatim into `.agent/decisions.md` while refusing to implement it, correctly treating C2 as a transcription duty rather than an endorsement, so the reviewer's reasoning is on the record next to its own refutation instead of being quietly dropped; and it refused to write `.agent/context.md`'s ordered claim that the ledger numbering was "repaired", because at that HEAD it was not, which is a worker declining to author a false state file it was explicitly told to author. What this gate does NOT say: the branch is still red at this commit — `test_one_entry_per_iteration_numbered_from_one` fails — and R12 is the round that clears it, by repairing the test rather than the loop.
<<<END GATE-R11>>>

<<<BEGIN DONE-R388>>>
Done: R-0388 — resolved as a MISDIAGNOSIS, with no production change. The finding asserted that the watchdog's ledger entry sharing its observing iteration's number broke a "one entry per iteration, numbered once" invariant. That invariant does not exist and never did: `run_mission` writes two entries under one iteration number on the blocked-completion escalation path, shipped and green since F075 R-0190. An entry's `iteration` field says which iteration it belongs to, not which row it is, and the watchdog's entry saying "iteration 3" is the same true statement the escalation entry makes on its own path. The R10 wiring is correct as committed, DECISION F077 D6 stands, DECISION F077 D10 is superseded by D11 without ever being implemented, and the only real defect was the test that encoded the imagined invariant — repaired in R12. The reviewer's own error here is registered separately as R-0391 rather than folded into this resolution, so the record shows a wrong finding being withdrawn AND the reason it was raised, instead of a quiet deletion.
<<<END DONE-R388>>>

<<<BEGIN DONE-R390>>>
Done: R-0390 — `.agent/plan.md` measures 45 lines, under the "<50" AGENTS.md bound it violated at exactly 50, with every mandated section intact: `## Goal`, `## Current Step`, `## Next Steps` and `## Risks` all survive the cut, which came out of prose and not out of structure. The reviewer confirmed the count independently. The underlying cause is fixed too, not just its symptom: the R10 block delegated plan.md's content to the worker as a description with no line bound attached, so neither role ever computed a number against the cap; the R11 and R12 blocks both state the bound explicitly in their Constraints, which is where a worker will actually read it.
<<<END DONE-R390>>>

<<<BEGIN DECISION-D11>>>
## DECISION F077 D11 (2026-08-14) — the ledger's `iteration` is not a unique key, and D10 is withdrawn unimplemented

CONTEXT. Findings R-0388 and R-0391. DECISION F077 D10 ordered `run_mission` to
stop passing its own iteration number to `watchdog_pass`, so a trip would be
numbered one past the entry that caused it. It rested on two premises and both
are false. The first, that the ledger holds one entry per iteration number:
`_record` has eleven call sites in `run_mission`, and the executed move's entry
and the blocked-completion escalation's entry fire in the same pass at the same
number, shipped and green since F075 R-0190. The second, that a trip always
ends the run before another entry can be written: `run_mission`'s safe point
calls `_record` and returns BEFORE the top-of-loop status check, so a stop
requested after a trip writes an entry at exactly the number D10 hands the trip.
The worker measured it — `[1, 2, 3, 4, 4]` with the repair against
`[1, 2, 3, 3, 4]` without it — and halted rather than applying it.

CHOSEN. D10 is withdrawn without ever being implemented. DECISION F077 D6 stands
unchanged: `run_mission` passes its own iteration number, and a trip is recorded
as belonging to the iteration that produced the evidence for it. The `iteration`
field is documented, here, as an ATTRIBUTION and not a key — it answers "which
iteration does this entry belong to", a question with more than one correct
answer per number, and the ledger's ordering is its file order. The only change
this round makes is to the one test that encoded the imagined invariant.

ALTERNATIVES CONSIDERED. Making `iteration` genuinely unique would mean giving
every one of the eleven `_record` call sites its own number, retiring the
attribution meaning that the R-0190 escalation entry and the F077 trip entry
both depend on, and rewriting the guards that currently read the field as an
iteration count — a large change to a shipped audit format, bought to satisfy a
property nothing needs. Adding a separate sequence field beside `iteration`
gives the ledger two numbers where readers cope with one, and the F077 entry is
not the reason to introduce it; if a real need for row identity appears, it
arrives with its own feature and its own migration of the record shape.

HOW TO REVERSE. Re-apply D10 by restoring the `iteration=iteration` argument's
removal at the `run_mission` call site — which was never removed, so reversing
this decision is a change, not a revert. Any such attempt must first answer the
safe-point path this decision names, because that path is what made D10 unsafe
independently of whether its invariant existed.
<<<END DECISION-D11>>>

<<<BEGIN PAIR LEDGER-TEST — REWRITE, file tests/orchestration/test_orchestrator_loop.py>>>
FROM:
    def test_one_entry_per_iteration_numbered_from_one(self, tmp_path, mission,
                                                       dispatched):
        run_mission(
            mission.id, LoopLimits(max_iterations=3), project_id=PROJECT,
            call_fn=_scripted(_move_json("dispatch_job", milestone_id="M001",
                                         step="work")),
            root=tmp_path, dispatch=dispatched, execute=_executed,
            control_root_path=tmp_path / "control")
        entries = read_ledger(PROJECT, mission.id, tmp_path)
        assert [e["iteration"] for e in entries] == [1, 2, 3]
        assert all(e["move"]["kind"] == "dispatch_job" for e in entries)
TO:
    def test_iterations_are_numbered_in_sequence_from_one(self, tmp_path,
                                                          mission, dispatched):
        """Four entries for three iterations, and the fourth is not a bug.

        An entry's ``iteration`` is an ATTRIBUTION — which iteration it belongs
        to — and NOT a unique key (DECISION F077 D11). The loop has recorded
        twice under one number since F075 R-0190, where a blocked completion's
        escalation entry follows its own move entry; see
        ``TestTheSecondBlockedCompletionEscalates``. Here the extra entry is the
        autonomy watchdog: three identical M001 dispatches with no milestone
        declared done between them IS the ``no_progress`` pattern at the default
        threshold of 3, so iteration 3 both moves and trips.
        """
        run_mission(
            mission.id, LoopLimits(max_iterations=3), project_id=PROJECT,
            call_fn=_scripted(_move_json("dispatch_job", milestone_id="M001",
                                         step="work")),
            root=tmp_path, dispatch=dispatched, execute=_executed,
            control_root_path=tmp_path / "control")
        entries = read_ledger(PROJECT, mission.id, tmp_path)
        assert [e["iteration"] for e in entries] == [1, 2, 3, 3]
        assert [e["move"]["kind"] for e in entries] == [
            "dispatch_job", "dispatch_job", "dispatch_job", "watchdog_tripped"]
<<<END PAIR LEDGER-TEST>>>

This pair is a REWRITE: the TO does not contain the FROM verbatim. The proof is
the FROM string exactly 0x in the file afterwards and the TO string exactly 1x.
Zero marker lines (`<<<BEGIN`, `<<<END`, `FROM:`, `TO:`) may reach any target
file.

── STATE MIRROR — C4 ─────────────────────────────────────────────

`.agent/plan.md` (UNDER 50 lines, keeps `## Goal` and `## Next Steps`): Current
Step R12 as this repair; Next Steps R13 (T003 CLI, `mission resume`, report
surface) and R14 (integration gate, then closure); the open-findings sentence
carries the count and names YOU measured at gate 4. Keep the post-resume
re-trip risk. Drop the R11 blocker line — it is resolved.

`.agent/context.md` (keeps `## Active Branch` with the `feature/` slug, the
substring `Steps`, an F-id, and `resource` or `pytest`): the Scope paragraph
describes the watchdog as wired and the branch as green, with the `iteration`
field named as an attribution per D11; the `## Steps` line gains R12 and
renumbers what follows. Also correct the block-ceiling constraint line per
R-0389: it now reads that the reviewer MEASURES the block mechanically before
emission and keeps it under 400 (DECISION F105 D5), with 240 named as the
preferred target rather than a ceiling nobody counted. Change nothing else.

── HANDBACK ──────────────────────────────────────────────────────

Report every gate's REAL value. Declare every deviation with its reason. If a
gate cannot run, say so with the exact command and the exact error rather than
routing around it. If anything in this block contradicts AGENTS.md or the code
you find on disk, STOP, write the contradiction into the handback, and end the
round — do not widen your own scope to resolve it, and do not guess.
──────────────────────────────────────────────────────────────────
