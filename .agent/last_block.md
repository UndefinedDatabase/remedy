── STEP R8/11 — F077 Autonomy watchdog (T002 the action, unwired) ────
Goal:        Build the pause, the deduped decision and the `watchdog_tripped` ledger entry as ONE callable action in `watchdog.py`, exactly as DECISIONS F077 D1-D8 settle them, with no call site in `orchestrator_loop.py`.
Bundle:      C0 save the block (TWO commits) · C1 the R7 verdict, R-0385, Done: R-0384 · C2 the action · C3 its tests · C4 mirrors · C5 handback.
Change:      EXACTLY these nine files — .agent/authored/f077-r8.md (new), .agent/last_block.md, .agent/live_review.md, .agent/plan.md, .agent/context.md, .agent/handoff.md, packages/orchestration/watchdog.py, tests/orchestration/test_watchdog.py, and nothing else.
Constraints: DECISION F077 D8 governs this round: the action ships UNWIRED. Adding any call to it from `packages/orchestration/orchestrator_loop.py` is out of scope and is a scope violation, not a bonus — R9 owns the wiring and the four `test_mission_e2e.py` guards it breaks. Do not edit orchestrator_loop.py, escalation.py, decision_queue.py, mission_state.py, mission_cmd.py or docs/. The watchdog never modifies plans, milestones or dossiers; the ONLY writes it may perform are the mission status, the escalation record on the job it attaches to, and the ledger append. Existing behaviour in watchdog.py is untouched: the three evaluators, their helpers and `watchdog_thresholds_from_config` keep their current signatures and bodies. Never write a `Done:` paragraph of your own — mark a landed fix `Landed: R-XXXX — <one line>` and nothing else.
──────────────────────────────────────────────────────────────────────

── C0 — save the block, in TWO commits ───────────────────────────────
Write the block body verbatim to `.agent/authored/f077-r8.md` and commit that
file ALONE. Then `cp .agent/authored/f077-r8.md .agent/last_block.md` and commit
THAT alone. Two commits by construction, because one commit carrying both files
would double the insertion count against AGENTS.md's 500 cap — the R7 lesson,
now ordered up front instead of left for you to discover (finding R-0385).
Report `cmp` exit 0, the shared sha256 and the line count.

── C1 — the R7 verdict, finding R-0385, and the R-0384 resolution ────
Findings persist FIRST. One commit, `.agent/live_review.md` only, appended at
the very END in THIS order: blank, FINDING-R385, blank, GATE-R7, blank,
DONE-R384. Each slice is ONE physical line — do not re-wrap. Change nothing
above them, and in particular leave the existing `Landed: R-0384` line exactly
where it is: this round APPENDS its resolution rather than rewriting that line,
so the shape is APPEND and the deletion column of this commit's numstat is 0.

>>> FINDING-R385 >>>
- R-0385 — Medium — the reviewer emitted a 445-line block against its own 400-line gate, and the same overrun then ordered a commit AGENTS.md forbids. Two downstream costs, both real, both traceable to one omission. First: gate 2 of the R7 block ordered the worker to report the block's line count and assert it is "at or under 400"; the real value is 445, so the gate was unsatisfiable by construction, and the worker was right to report 445 unadjusted rather than trim an artifact it is required to save verbatim. That is the R-0371 self-referential-gate class recurring — a gate whose expected value the block's own bytes contradict. It also breaks the 240-line ceiling recorded in `.agent/context.md`, whose stated purpose is precisely "so the block-save commit stays inside the 500-insertion cap". Second: C0 of that block ordered the new authored file and its `cp` mirror committed TOGETHER, which at 445 lines measures 886 insertions against AGENTS.md's hard 500-line cap, whose own prescribed remedy is "stop and split before committing". The worker applied that remedy, splitting by file into `8ecf306f` (445 insertions, the authored file) and `8d9ed78e` (441 insertions, the `cp` mirror — itself the AGENTS.md-exempt verbatim rewrite of a single `.agent/**` state file), kept the bytes identical so `cmp` still exits 0, and consumed no oversize exception. That was the correct call and AGENTS.md outranks the block, so it is not a worker defect. The root cause is single: the block was never measured. Pre-emission checklist item 1 (docs/agents/planner_reviewer_prompt.md §3) says to count the block's lines mechanically on the FINAL bytes, after the last edit, before the block leaves the reviewer; the reviewer reasoned about a 240-line budget while drafting, kept adding, and never counted the result. Fix, both halves: the reviewer counts the emitted block with `wc -l` before delegating and cuts to the ceiling if it is over, AND any block expected to exceed roughly 250 lines orders C0 as two commits from the start, as this block does, so the cap is never something the worker has to discover mid-round. OPEN.
<<< FINDING-R385 <<<

>>> GATE-R7 >>>
Gate: R7 — PASS. Verification tier: round gate plus canary plus the state-file contract readers; no full-suite claim is made. Every value was re-executed by the reviewer against the disk rather than read out of the handback, and every one reproduces. Transport: `cmp .agent/authored/f077-r7.md .agent/last_block.md` exit 0 at shared sha256 `bbac8ab687f6d0002d2cf6384c5576a7004c0266f0e6086b095e440fad83bae5`, 445 lines — OVER the 400-line cap the block set for itself, which is the reviewer's defect and is registered above as R-0385, not the worker's. All nine authored slices were re-extracted by the reviewer from the COMMITTED block file at `8ecf306f` between their own markers and each is present in its target EXACTLY ONCE, byte for byte: DONE-R383 482 bytes, GATE-R6 3444, LANDED-R384 420, DECISIONS-F077 12273, PLANNEXT-TO 561, CTX-TO 526, MS-TO 621, MC-TO 419, TC-TO 247; and all five FROM anchors — PLAN, CTX, MS, MC, TC — count 0 in their files afterwards, so every rewrite pair completed rather than double-applied. The record's line-anchored counts are `^Gate: R6 — PASS` 1, `^Done: R-0383 — ` 1, `^Landed: R-0383 — ` 0, `^Landed: R-0384 — ` 1, `^## Steps` 1, and the open set recomputed mechanically from the record — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — is exactly EIGHTEEN: R-0361, R-0362, R-0363, R-0364, R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378, R-0379, R-0380, R-0381, R-0382, R-0384. Scope held exactly: `git diff --name-only 55159180..HEAD` returns the ten Change-line files and no others, `git diff --stat 55159180..HEAD -- packages/ apps/ tests/` lists exactly `mission_cmd.py`, `mission_state.py` and `test_mission_cmd.py` at 19 insertions against 3 deletions, and over `docs/` it produces no output at all. The C3 diff was read hunk by hunk rather than trusted: all three hunks sit wholly inside a docstring, no executable line moved, and each new text names ONLY the callers that exist at this commit — the three human verbs and the loop's two terminal moves — with no mention of the watchdog, which is DECISION F077 D7 applied correctly and is the difference between repairing a false claim and replacing it with a different one. The T002 inventory's own §5 proposed amendment would have made that mistake, and declining it is the right call. Suites re-run by the reviewer: `tests/cli/test_mission_cmd.py` with `tests/orchestration/test_mission_state.py` `164 passed` against the 164 baseline the reviewer measured BEFORE authoring, the canary `42 passed`, the three state-file contract readers `142 passed`, `tests/orchestration/test_watchdog.py` `13 passed` untouched, `ruff check` over the three changed files `All checks passed!`, and `integrity check --json` `passed: true`, `fail_count: 0` over 5 checks; `git status --porcelain` is empty, `git worktree list` is one line, `.agent/plan.md` is 42 physical lines with `wc -l` and `grep -c ""` agreeing, and `.agent/context.md` carries every reader string its three test files assert. The C0 split into two commits is a correct deviation and is credited to the worker rather than charged to it: AGENTS.md outranks the block, the combined commit would have been 886 insertions, and the split kept the bytes identical. The worker's refusal to trim the oversize block to satisfy a gate about the block itself is likewise correct — an artifact it must save verbatim is not its to edit — and its report of 445 unadjusted is exactly the honesty the evidence rule asks for. R-0384 is RESOLVED at this gate, on the reviewer's own reading of all three repaired sites. The eight decisions are the round's real product and they were spot-checked rather than accepted: D2's mechanism was verified reachable before it was ordered — `open_mission_decisions` in `orchestrator_loop.py` returns the STORED record dicts, each carrying a `question`, filtered to `ESCALATION_STATUS_OPEN` across every linked job — and D5's central claim was verified against the reader rather than assumed, since `render_ledger` prints `move.get("kind", "unknown")` and then every key of `move["payload"]` in sorted order, so the evidence triple reaches the human ledger with no renderer change. No block condition was hit — no fabricated value, no false live indicator, no missing changed-files table, no unverified completion claim, no silent scope change.
<<< GATE-R7 <<<

>>> DONE-R384 >>>
Done: R-0384 — the stale "no autonomous status write" claim is repaired at all THREE sites: `set_mission_status` in `packages/orchestration/mission_state.py` now names the two kinds of caller and states that a status on disk is not evidence a human put it there; `_cmd_mission_set_status` in `apps/cli/commands/mission_cmd.py` now scopes F056's "nothing moves on its own" to the COMMAND rather than to the status field; and the `TestStatusTransitions` class docstring in `tests/cli/test_mission_cmd.py` — the third site, which the finding itself undercounted — carries the same correction. Verified at the R7 gate by reading each hunk against the callers that actually exist at that commit: `mission_achieved` and `execute_move` in `orchestrator_loop.py` are named, the watchdog deliberately is NOT, because it does not write a status until R8 lands, and a docstring naming a caller that does not exist yet would be the same defect in the other direction (DECISION F077 D7).
<<< DONE-R384 <<<

── C2 — the action ───────────────────────────────────────────────────
Own commit. `packages/orchestration/watchdog.py` only. Append a new section
BELOW the existing evaluators; change no existing function. Heavy imports go
INSIDE the function body, following this module's own precedent in
`watchdog_thresholds_from_config` and `orchestrator_loop.open_mission_decisions`
— a module-level import of the loop would create the cycle R9's wiring needs to
not exist.

Add, in this order:

1. Constants, each with the one-line WHY comment this repo puts directly above
   a definition: `MOVE_WATCHDOG_TRIPPED = "watchdog_tripped"` (the ledger
   entry's `move.kind`), `OUTCOME_WATCHDOG_TRIPPED = "watchdog_tripped"` (its
   `MoveOutcome.status`), `DECISION_OPTION_RESUME = "resume"` and
   `DECISION_OPTION_ABORT = "abort"` (the two options the feature file names).

2. `def watchdog_decision_marker(kind: str) -> str` returning
   `f"[watchdog:{kind}]"`. This prefix on the decision's QUESTION is the whole
   dedup key (DECISION F077 D2): `enqueue_task_decision` writes a fixed key set
   and takes no extras, so the question text is the one caller-controlled field.

3. A frozen dataclass `TripAction` with `trip: Trip`, `decision_id: str = ""`,
   `suppressed: bool = False`, `note: str = ""`. `decision_id` is `""` whenever
   no record was written, and `note` then says why in one human sentence.

4. `def act_on_trips(project_id: str, mission_id: str, trips: Sequence[Trip],
   *, root: Any = None, iteration: int | None = None, now: Any = None) ->
   list[TripAction]`, doing exactly this and nothing more:

   (a) `if not trips: return []` — no pause, no entry, no decision. A watchdog
       that writes on a clean ledger is a watchdog nobody leaves switched on.
   (b) Load the mission. Write `MISSION_STATUS_PAUSED` through
       `set_mission_status` ONLY when the current status is
       `MISSION_STATUS_ACTIVE`. An `achieved` or `abandoned` mission is
       terminal and the watchdog must not overwrite it; an already-`paused` one
       needs no write. One status write per call, never one per trip.
   (c) Read the open decisions ONCE via
       `orchestrator_loop.open_mission_decisions(mission)`.
   (d) For each trip, in the order given: compute its marker; if any open
       record's `question` (coerced with `str(...)`, defaulting to `""`) starts
       with that marker, produce `TripAction(trip, suppressed=True,
       note=...)` and enqueue NOTHING. Otherwise attach exactly as
       `escalate_repeated_refusal` does (DECISION F077 D1) — `mission
       .latest_link()`, then `load_job(_as_uuid(link.job_id))` inside a
       `try/except Exception`, then the job's first task — and on each of those
       three guards produce a `TripAction` with `decision_id=""` and a note
       naming the specific gap, never a raise. On the happy path call
       `enqueue_task_decision(job, task_id=<first task's id>,
       question=f"{marker} {trip.what}",
       options=(DECISION_OPTION_RESUME, DECISION_OPTION_ABORT),
       safe_default="", impact=<one sentence naming the paused mission>,
       now=<the stamp>)`, then `save_job(job)`, and take `decision_id` from the
       returned record. `safe_default` is deliberately EMPTY: it is the value
       `escalation.auto_apply_safe_default` would apply unattended, and a
       watchdog whose trip can be auto-answered by the same automation it just
       stopped is not a tripwire. Append the new record to the in-memory open
       list so a second trip of the same class in the SAME call cannot
       double-enqueue.
   (e) For each trip, append ONE ledger entry, whatever the decision outcome
       was — the pause and the record of it must not depend on whether a
       decision could be attached. Shape, fixed by DECISION F077 D5:
       `move={"kind": MOVE_WATCHDOG_TRIPPED, "payload": trip.to_json()}`,
       `outcome=MoveOutcome(status=OUTCOME_WATCHDOG_TRIPPED, detail=<see
       below>, terminal=False).to_json()`, `context_digest=""`, and the
       precedent zero cost `{"calls": 0, "usage": None, "usage_source":
       USAGE_UNMEASURED}`. `detail` is `trip.what`, followed by `"; "` and the
       note whenever a note exists. Use `append_ledger_entry(project_id,
       mission_id, entry, root, now=<the stamp>)`.
   (f) Iteration numbering, per DECISION F077 D6: when `iteration` is not None
       every entry of this call carries it — simultaneous trips genuinely
       happened in one iteration — and when it is None, call
       `next_iteration_index(project_id, mission_id, root)` freshly before EACH
       append, so a manual multi-trip audit numbers its entries consecutively.
   (g) Return the `TripAction` list in trip order, one per trip, always.

   Give `act_on_trips` a docstring that states what it writes (mission status,
   one escalation record per unsuppressed trip, one ledger entry per trip) and
   what it never touches (plans, milestones, jobs beyond that record, dossiers).
   Then add ONE paragraph to the MODULE docstring saying that this section is
   the action half and is deliberately NOT pure, so the existing purity sentence
   keeps meaning only what it says. Describe only what exists at this commit:
   the action has NO caller in `orchestrator_loop.py` and the docstring must not
   imply one (the D7 discipline).

── C3 — the tests ────────────────────────────────────────────────────
Own commit. `tests/orchestration/test_watchdog.py` only; the 13 existing tests
keep passing untouched. The file is currently fixture-free and pure, so add what
you need at the bottom: borrow the mission/job fixture shapes from
`tests/orchestration/test_orchestrator_loop.py` (its `mission` fixture, `PROJECT`
and `_plan`) and from `tests/orchestration/test_escalation.py` for a job with
tasks. Every test passes `root=tmp_path`. Name each test after the property it
pins, in this file's existing sentence style. Cover, at minimum:

 1. An empty trip list writes NOTHING: status unchanged, ledger file absent or
    unchanged, no decision, return value `[]`.
 2. One trip on an ACTIVE mission leaves it `paused`.
 3. A mission already `achieved` is NOT overwritten by a trip.
 4. The ledger entry's `move["kind"]` is `watchdog_tripped` and its
    `move["payload"]` equals `trip.to_json()` exactly — assert the DICTS are
    equal, not their rendered length.
 5. `render_ledger` over the read-back ledger contains the trip's `kind`, its
    `what`, and the `since_iteration` and `numbers` keys — the D5 claim that the
    evidence triple reaches the human ledger with no renderer change.
 6. Dedup: acting twice on the same trip CLASS writes exactly ONE escalation
    record; the second call returns `suppressed=True` and `decision_id == ""`.
 7. Two trips of DIFFERENT classes in one call produce TWO decisions — dedup is
    per class, not per mission.
 8. Answering the decision through `escalation.answer_task_decision` and saving
    the job lifts the suppression: a third call enqueues again (DECISION D3).
 9. A mission with no linked job still pauses and still writes its ledger entry;
    the returned `TripAction` has `decision_id == ""` and a note naming the
    missing job, and nothing raises (DECISION D1).
10. Re-entrancy (the D5 inertness claim, verified rather than asserted): build a
    ledger that already contains a `watchdog_tripped` entry and show that
    `dispatched_entries` ignores it, that `measured_tokens` returns `None` for
    it, and that `evaluate_no_progress` reaches the same verdict with and
    without it present.
11. A caller-supplied `iteration` is the number the entry carries.

Report the real test count for the file afterwards; do not adjust it to a
number this block predicts.

── C4 — the mirrors ──────────────────────────────────────────────────
Own commit. Update `.agent/plan.md` (Current Step and the Next Steps list) and
`.agent/context.md` (the Scope and Steps lines) to the state after R8. Keep
`.agent/plan.md` at or under 49 physical lines with its `## Goal` and
`## Next Steps` headings intact, and keep in `.agent/context.md`:
`## Active Branch` 1x, `feature/f077-autonomy-watchdog`, `Steps`, `F077`,
`resource`, `pytest`. Record in both that the open count is SEVENTEEN after this
round — eighteen minus R-0384, plus R-0385 — and that the next free id is
R-0386. Recompute that set from `.agent/live_review.md` yourself and report your
own number; if it is not seventeen, report what you got and do not adjust it.

── C5 — the handback ─────────────────────────────────────────────────
Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: per-commit
changed-files tables, the REAL gate transcript, the item-status table for C0-C5,
the open-findings count and the next expected action. Exceeding 60 lines is
allowed only with a DECISION D15 "Deviations, declared" line naming the real
count and the mandated content that caused it. Never drop a section.

State plainly in the handback that this round's green gate proves the ACTION is
correct in isolation and proves NOTHING about the loop, because `act_on_trips`
has no call site yet (DECISION F077 D8). R9 adds the call site and pays the four
whole-ledger guards in `tests/orchestration/test_mission_e2e.py`.

── Gates — run every one, report the REAL value, never the word "green" ──
 1. `git status --porcelain` -> EMPTY; `git worktree list` -> 1 line.
 2. `cmp .agent/authored/f077-r8.md .agent/last_block.md` -> exit 0; report the
    shared sha256 and the line count.
 3. On `.agent/live_review.md`: `grep -c "^Gate: R7 — PASS"` -> 1,
    `grep -c "^- R-0385 — "` -> 1, `grep -c "^Done: R-0384 — "` -> 1,
    `grep -c "^Landed: R-0384 — "` -> 1 (the Landed line STAYS),
    `grep -c "^## Steps"` -> 1.
 4. Recompute the open set mechanically from `.agent/live_review.md` and name
    every id. Report YOUR count.
 5. `git show --numstat <C1-sha> -- .agent/live_review.md`: report both columns;
    the deletion column is 0.
 6. `git diff --name-only 7649a86b..HEAD` -> exactly the nine Change-line files.
    `git diff --stat 7649a86b..HEAD -- docs/ apps/` -> EMPTY.
 7. `grep -rn "watchdog" packages/orchestration/orchestrator_loop.py` -> report
    every hit. There must be NO import of and NO call into `watchdog` (D8); the
    one pre-existing hit is a prose comment mentioning escalation, not an import.
 8. `python3 -m pytest tests/orchestration/test_watchdog.py -q` -> report the
    real count; the 13 pre-existing tests must all still pass. Also report
    `grep -c "def test_" tests/orchestration/test_watchdog.py`.
 9. `python3 -m pytest tests/orchestration/test_orchestrator_loop.py tests/orchestration/test_mission_e2e.py tests/orchestration/test_escalation.py -q`
    -> run it and report the REAL result. Measure this BEFORE you start C2 as
    well and report BOTH numbers, so a regression is attributable.
10. `python3 -m pytest tests/cli/test_golden_path.py -q` -> baseline `42 passed`.
11. `python3 -m pytest tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py -q`
    -> baseline `142 passed`.
12. `python3 -m ruff check packages/orchestration/watchdog.py tests/orchestration/test_watchdog.py`
    -> exit 0. Repo-wide `ruff check` is RED on main (R-0364) and is NOT a gate.
13. `python3 -c "import packages.orchestration.watchdog"` -> exit 0, proving no
    import cycle was introduced.
14. `python3 -m apps.cli.main integrity check --json` -> report `passed`,
    `fail_count`, `check_count`.
15. `wc -l .agent/plan.md` -> at or under 49 and equal to `grep -c ""` on it;
    `^## Goal` 1, `^## Next Steps` 1; the six `.agent/context.md` reader
    strings all present.
16. Insertions per commit from `git show --numstat`; none over 500. If any
    commit would exceed it, SPLIT before committing and say so.
17. Trailing-whitespace scan over every touched file -> none.
18. `test -e .agent/STOP` -> report absent or present, checked BEFORE you start
    and AGAIN at handback. If it appears: finish the current commit, write the
    handoff, STOP.
19. `git push -u origin feature/f077-autonomy-watchdog`. No `gh`, no PR.

Handback: completion report + rewrite `.agent/handoff.md`.
