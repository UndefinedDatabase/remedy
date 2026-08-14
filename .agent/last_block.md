── STEP R7/9 — F077 Autonomy watchdog (R6 verdict, the eight T002 decisions, R-0384) ──
Goal:        Settle every open question T002 is blocked on as a recorded, reversible DECISION, and repair the three stale docstrings that claim no autonomous status write ever happens.
Bundle:      C0 save the block · C1 the R6 verdict, Done: R-0383, and both mirrors · C2 the eight F077 decisions · C3 the R-0384 repair across all three sites · C4 handback.
Change:      EXACTLY these ten files, nothing else — .agent/authored/f077-r7.md (new), .agent/last_block.md, .agent/live_review.md, .agent/decisions.md, .agent/plan.md, .agent/context.md, .agent/handoff.md, packages/orchestration/mission_state.py, apps/cli/commands/mission_cmd.py, tests/cli/test_mission_cmd.py.
Constraints: NO new behaviour, NO new function, NO new test, NO signature change. C3 is docstring/prose text only — if a diff hunk in C3 touches a line that is not inside a docstring or a comment, you have gone out of scope. The watchdog pause, the decision, the dedup and the ledger entry are R8's work and are NOT built here; this round only decides their shape. Do not touch packages/orchestration/watchdog.py, orchestrator_loop.py, escalation.py, decision_queue.py or docs/. Never write a `Done:` paragraph of your own — that text is reviewer-authored; a fix you land is marked `Landed: R-XXXX — <one line>` and nothing else.
──────────────────────────────────────────────────────────────────────

── C0 — save the block ───────────────────────────────────────────────
Write the block body verbatim to `.agent/authored/f077-r7.md`, `cp` it to
`.agent/last_block.md`, commit both together. Report `cmp` exit, the shared
sha256 and the line count.

── C1 — the R6 verdict, the R-0383 resolution, and both mirrors ──────
Findings persist FIRST. Four files, ONE commit.

(a) `.agent/live_review.md` — TWO edits, in this order.

  (a1) REWRITE pair. The file currently carries one physical line beginning
  `Landed: R-0383 — `. Replace that ENTIRE physical line with the DONE-R383
  slice. FROM and TO are disjoint, so this is a REWRITE: prove
  `grep -c "^Landed: R-0383 — "` goes 1 -> 0 and `grep -c "^Done: R-0383 — "`
  goes 0 -> 1. Change nothing else on that line's neighbours.

  (a2) APPEND. At the very END of the file add one blank line then the
  GATE-R6 slice. It is ONE physical line — do not re-wrap it. Shape: APPEND.

>>> DONE-R383 >>>
Done: R-0383 — the module docstring of `packages/orchestration/watchdog.py` now scopes its purity claim to the three EVALUATORS and their helpers and names `watchdog_thresholds_from_config` as the ONE function that reaches outside, reading config through `get_config()`. Verified at the R6 gate by reading the committed docstring against every function in the module: the narrowed sentence is true of the code as written, and no signature and no behaviour changed to make it true.
<<< DONE-R383 <<<

>>> GATE-R6 >>>
Gate: R6 — PASS. Verification tier: round gate plus canary plus the state-file contract readers; no full-suite claim is made. Every value was re-executed by the reviewer against the disk rather than read out of the handback, and every one reproduces. Transport: `cmp .agent/authored/f077-r6.md .agent/last_block.md` exit 0 at shared sha256 `126d7c10cbe046d670a0bea99dfaa65ff0cb0a1f02a328d3141124483cc89983`, 136 lines, inside the 400-line cap and inside the 240-line ceiling R-0381's counter-measure sets; BOTH slices were re-extracted by the reviewer from the COMMITTED block file at `ca0af789` between their own markers — FINDING-R384 at 2121 bytes, sha256 `58372ae6e245aa6febf03a2aa3c69dd2f5220c5ecbe18434da844734c2f2d6a7`, and GATE-R5 at 4548 bytes, sha256 `6440d42c125339a36108ebbcaa8a4a8f0de081940b2b3af610823dcd100c1405` — and each is byte-equal to a physical line of `.agent/live_review.md`, whose tail is exactly `Landed: R-0383`, blank, FINDING-R384, blank, GATE-R5, in that order. The live_review numstat for `480a639d` is `4 0`, deletion column 0, so nothing above the append moved. The open set recomputed mechanically from the record — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — is exactly nineteen: R-0361, R-0362, R-0363, R-0364, R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378, R-0379, R-0380, R-0381, R-0382, R-0383, R-0384 — with zero `^Done:` lines and exactly one `^Landed:` line, which is what an unreviewed fix is supposed to look like; the worker authored no resolution of its own. Scope held: `git diff --name-only 6e871e6d..HEAD` returns exactly the six files the Change line names, `git diff --stat 6e871e6d..HEAD -- packages/ apps/ tests/ docs/` produces NO OUTPUT AT ALL, and insertions per commit are 246, 36 and 86, none over 500. Suites re-run by the reviewer: the canary `42 passed`, the three state-file contract readers `142 passed`, `tests/orchestration/test_watchdog.py` `13 passed` against its untouched 13 baseline, and `integrity check --json` returns `passed: true`, `fail_count: 0` over 5 checks; `git status --porcelain` is empty, `git worktree list` is one line, `.agent/plan.md` is 49 physical lines under its 50 cap with `wc -l` and `grep -c ""` agreeing, so the file is newline-terminated, and `.agent/context.md` carries every reader string its three test files assert. A trailing-whitespace scan over all six touched files finds none. R-0383 is RESOLVED at this gate on the reviewer's own reading of the committed module rather than on the handback's claim. The handback's declared 126-line overage is correct under DECISION D15 and its stated cause is real: the mandated tables, the fifteen-gate transcript and the nineteen named findings genuinely do not fit in sixty lines, and no section was dropped to pretend otherwise. No block condition was hit — no fabricated value, no false live indicator, no missing changed-files table, no unverified completion claim, no silent scope change. One correction the record must carry, and it is the REVIEWER's undercount rather than the worker's: R-0384's own text says the stale no-autonomous-writes claim is "available in two places", but it is in THREE — the `TestStatusTransitions` class docstring in `tests/cli/test_mission_cmd.py` repeats it as a third time, found by grepping the suite for the sentence rather than by trusting the finding, and R7's repair covers all three sites.
<<< GATE-R6 <<<

(b) `.agent/plan.md` — REWRITE pair, replacing the Current Step section and the
Next Steps list. FROM and TO are disjoint: prove FROM 0x and TO 1x after.

>>> PLAN-FROM >>>
## Current Step
R6 — record the R5 verdict, register R-0384, close the session.
<<< PLAN-FROM <<<

>>> PLAN-TO >>>
## Current Step
R7 — record the R6 verdict, resolve R-0383, settle the eight T002 questions as
DECISIONS F077 D1-D8, and repair R-0384's three stale docstrings.

T002's code is NOT built this round. The eight questions the T002 inventory
left open each had a shape consequence, and building before settling them is
how a round discovers a schema decision halfway through. D1-D8 settle them.
<<< PLAN-TO <<<

Then in the same file replace the whole `## Next Steps` list body with:

>>> PLANNEXT-TO >>>
1. R8 — T002 the code D1-D8 unblock: the pause, the deduped decision, the
   `watchdog_tripped` ledger entry and the unit tests, as a callable action in
   `watchdog.py` NOT yet wired into `run_mission`.
2. R9 — wire the watchdog into the loop's iteration seam, pay the four
   whole-ledger guards in `tests/orchestration/test_mission_e2e.py` that a new
   entry kind breaks, and add the loop-integration test.
3. R10 — T003 the manual CLI including the missing `mission resume` verb (D4)
   and the report surface. R11 — integration gate, then closure.
<<< PLANNEXT-TO <<<

Also update the plan's finding ledger sentence: next free finding id is R-0385
and the open count after this round is EIGHTEEN, because R-0383 resolves here
and R-0384 only LANDS here. Keep `.agent/plan.md` at or under 49 physical lines
and keep its `## Goal` and `## Next Steps` headings — contract tests read them.
Trim the Risks section if you need the room; do not drop a heading.

(c) `.agent/context.md` — REWRITE pair on the Steps line only.

>>> CTX-FROM >>>
R4 T001 the three evaluators, their config keys and their tests ✅ → R5 record
the R4 verdict, repair R-0383 and inventory T002 ✅ → R6 record the R5 verdict,
register R-0384 and close the session → R7 T002 pause, decision, dedup and
ledger entry, which first settles the eight open questions in
`.agent/f077_t002_inventory.md` and repairs R-0384 → R8 T003 CLI and report →
R9 integration gate then closure.
<<< CTX-FROM <<<

>>> CTX-TO >>>
R4 T001 the three evaluators, their config keys and their tests ✅ → R5 record
the R4 verdict, repair R-0383 and inventory T002 ✅ → R6 record the R5 verdict
and register R-0384 ✅ → R7 record the R6 verdict, settle the eight T002
questions as DECISIONS F077 D1-D8 and repair R-0384 → R8 T002 the pause, the
deduped decision and the ledger entry as an unwired action → R9 wire it into
the loop and pay the four e2e ledger guards → R10 T003 CLI, `mission resume`
and report → R11 integration gate then closure.
<<< CTX-TO <<<

`.agent/context.md` must still contain, after the edit: `## Active Branch` 1x,
`feature/f077-autonomy-watchdog` at least 1x, `Steps`, an `F077` token,
`resource` and `pytest`. Three separate test files assert those.

── C2 — the eight decisions T002 is blocked on ───────────────────────
Append the DECISIONS-F077 slice to the END of `.agent/decisions.md`, preceded
by one blank line. Shape: APPEND. Extract it disk-to-disk; do not retype it.
Own commit.

>>> DECISIONS-F077 >>>
## DECISION F077 D1 (2026-08-14) — a trip always pauses; only the decision degrades on a jobless mission

CONTEXT. `enqueue_task_decision` (`packages/orchestration/escalation.py`) is
task-scoped and has no jobless guard, and no decision path in the repository
attaches to a MISSION — every producer branch of `list_decisions` is job- or
global-scoped. `evaluate_no_progress` and `evaluate_goal_drift` fire only off
`dispatched_entries`, which requires a non-empty `outcome.job_id`, so only
`burn_anomaly` can trip with no job to attach to.

CHOSEN. The pause is unconditional; the decision is best-effort. The watchdog
attaches through `mission.latest_link()` and the job's first task, exactly as
`escalate_repeated_refusal` (`packages/orchestration/orchestrator_loop.py`)
already does, and on a jobless or taskless mission it still writes `paused` and
still writes the ledger entry, recording the attachment failure as prose in the
entry's `outcome.detail` — the same shape `escalate_repeated_refusal` uses for
its three guard returns.

ALTERNATIVES CONSIDERED. Refusing to trip on a jobless mission (inventory §1
option c) is cheaper, but it trades a SAFETY stop for a reporting convenience:
a burn anomaly on a jobless mission is exactly the runaway the feature exists to
stop. A mission-anchored decision store (option b) needs a new `DECISION_TYPES`
member, a ninth `list_decisions` branch and a mission entry point for the three
`remedy decision` verbs — a schema change T002 should not carry.

HOW TO REVERSE. Make the attachment failure an early return before the pause.
The D1 test named for the jobless path fails immediately, which is the point.

## DECISION F077 D2 (2026-08-14) — F077's dedup wins, implemented in the watchdog and not in escalation.py

CONTEXT. `packages/orchestration/escalation.py`'s module docstring declines
dedup as policy — "Two tasks raising the same question produce TWO records
(deduplication is a human call, feature-file A9)" — while F077 requires one
decision per trip class, deduped within a mission until resolved. All three
existing writers enqueue unconditionally, and `enqueue_task_decision` builds a
fixed key set with no extras argument, so there is nowhere on the stored record
to hang a typed dedup key.

CHOSEN. F077's requirement wins, and the dedup lives at the WATCHDOG's layer.
`escalation.py` is not touched and keeps enqueuing whatever it is asked to; the
watchdog asks only when it should. Before enqueuing, it reads
`open_mission_decisions(mission)` — which returns the stored record dicts, each
carrying a `question`, filtered to `ESCALATION_STATUS_OPEN` across every linked
job — and skips the enqueue when a record's `question` already starts with the
marker `[watchdog:<kind>]`. The marker is a literal prefix on the question text
because that is the one caller-controlled field on the record.

ALTERNATIVES CONSIDERED. Adding dedup inside `enqueue_task_decision` reverses a
documented policy for every caller to serve one of them. A new stored key needs
`enqueue_task_decision` to accept extras — a signature change on a shared writer
for a single feature's benefit.

HOW TO REVERSE. Delete the marker scan in the watchdog. Escalation is untouched,
so nothing else in the repository changes behaviour.

## DECISION F077 D3 (2026-08-14) — the decision's own open/answered state IS the dedup state

CONTEXT. "Deduped until resolved" needs a notion of resolved. Inventory §3 lists
four candidates and all four are unbuilt.

CHOSEN. Option (a): no new state at all. Suppression means "an open decision
carrying this trip's marker exists". Answering it through
`answer_task_decision` flips the record to `ESCALATION_STATUS_ANSWERED`, which
removes it from `open_task_decisions` and therefore from
`open_mission_decisions`, and the suppression lifts on the next evaluation with
no bookkeeping. `remedy decision resolve` already reaches it, because
`_cmd_decision_resolve` (`apps/cli/commands/decision.py`) dispatches on the
`td:` prefix the escalation writer produces.

ALTERNATIVES CONSIDERED. A key on the mission record touches `Mission`'s
serialization. A file under `mission_evidence_dir` is a second source of truth
beside the queue, which `decision_queue.py`'s own docstring rules out. Deriving
it from the ledger is append-only and elegant but has no notion of "answered",
which is precisely the notion the requirement is about.

HOW TO REVERSE. Introduce an explicit dedup store and read it instead. The
marker scan is one function and it is the only reader.

## DECISION F077 D4 (2026-08-14) — the missing `mission resume` verb is T003's, not T002's

CONTEXT. `_status_for_verb` (`apps/cli/commands/mission_cmd.py`) maps exactly
`achieve`, `abandon` and `pause`; `apps/cli/command_catalog.py` registers the
matching three, and a search for `mission.resume` or `mission.activate` across
`apps/` and `packages/` returns nothing. A paused mission has NO supported path
back to active, so a watchdog pause is terminal for the run in practice.

CHOSEN. T002 ships the pause and the deduped decision without a resume verb, and
T003 — the slice that owns the manual CLI — adds `mission resume` alongside the
watchdog command. The feature file is NOT amended: its acceptance sentence
"resume clears exactly that trip's dedup" stays true across T002 and T003
together, because D3 makes the clearing a consequence of answering the decision
rather than of the verb, and the verb only restores `active`.

ALTERNATIVES CONSIDERED. Adding the verb inside T002 widens a pause-and-decide
slice into CLI and catalog work. Shipping the pause with no route out at all,
and not writing the gap down, is how a session rediscovers it in the round that
can least afford the detour.

HOW TO REVERSE. Move the verb into T002's change set. It is one `_status_for_verb`
entry, one catalog registration and its test.

## DECISION F077 D5 (2026-08-14) — the evidence triple rides in `move.payload`, and the renderer prints it for free

CONTEXT. `MoveOutcome.to_json` emits only `status`, `detail` and — when set —
`job_id`, so the triple has no home there. Inventory §4 offers prose in
`detail`, a raw dict bypassing `MoveOutcome`, or a new `MoveOutcome` field that
`render_ledger` would not print. Five loop precedents pass `move={}` for entries
with no model move behind them.

CHOSEN. The `watchdog_tripped` entry takes
`move={"kind": "watchdog_tripped", "payload": trip.to_json()}`, a real
`MoveOutcome` for the outcome, `context_digest=""`, and the precedent zero cost
`{"calls": 0, "usage": None, "usage_source": USAGE_UNMEASURED}`. This was
checked against the reader rather than assumed: `render_ledger` prints
`move.get("kind", "unknown")` and then every key of `move["payload"]` in
`sorted` order, so `kind`, `what`, `since_iteration` and `numbers` appear in the
human ledger with NO change to the renderer. It also keeps `move["kind"]` a
total lookup for the existing bare-subscript reader in the suite.

The departure from the `move={}` precedent is deliberate and narrow: those five
entries are ones where a model move was EXPECTED and absent, whereas a watchdog
trip is an action of its own with a name. An empty move would be a claim that
nothing happened.

Re-entrancy, checked against the evaluators rather than assumed: the entry is
inert to a later watchdog pass. `dispatched_entries` skips it because its kind
is not `dispatch_job`; `evaluate_no_progress` neither counts nor clears on it
because it is neither a dispatch nor a `declare_milestone_done`; and
`measured_tokens` returns `None` for it because the cost carries no `usage`
dict, so it cannot drag a burn baseline. R8 pins each of those three with a
test.

ALTERNATIVES CONSIDERED. Prose in `detail` loses the numbers to string parsing.
A raw outcome dict bypassing `MoveOutcome` gives the entry a shape no other
entry has. A new `MoveOutcome` field is invisible to the renderer, which is the
one surface a human reads.

HOW TO REVERSE. Move the payload into `outcome`. `render_ledger` stops printing
the triple, which is the visible cost and the reason not to.

## DECISION F077 D6 (2026-08-14) — the iteration number is a parameter, defaulted, never guessed

CONTEXT. `run_mission` computes `base = next_iteration_index(...)` ONCE before
the loop and then uses `iteration = base + step - 1`, while
`next_iteration_index` re-reads the file and returns one past the highest
recorded. An external append mid-run therefore takes a number the loop is
already going to reuse, and the ledger ends up with a duplicate.

CHOSEN. The T002 action takes `iteration: int | None = None` and falls back to
`next_iteration_index(...)` only when the caller passes nothing. A manual
out-of-band audit gets a correct number; the loop, when R9 wires it in, passes
its OWN current number and no collision is possible. The hazard is closed at the
API boundary in the round that creates the boundary, rather than left for the
wiring round to discover.

ALTERNATIVES CONSIDERED. Always calling `next_iteration_index` guarantees the
collision the inventory warns about. Always requiring the caller to pass one
makes the manual CLI path carry loop bookkeeping it has no business knowing.

HOW TO REVERSE. Drop the parameter. The R9 wiring is the only caller that
passes it.

## DECISION F077 D7 (2026-08-14) — the stale docstrings are repaired to what is true TODAY, not to what T002 will make true

CONTEXT. Finding R-0384. Three sites claim no autonomous status write happens:
`set_mission_status` (`packages/orchestration/mission_state.py`),
`_cmd_mission_set_status` (`apps/cli/commands/mission_cmd.py`), and — found by
grepping the suite rather than by trusting the finding's own count — the
`TestStatusTransitions` class docstring in `tests/cli/test_mission_cmd.py`. All
three have been false since `mission_achieved` and `execute_move` landed.

CHOSEN. All three are repaired in R7, and each new text names ONLY the callers
that exist at R7: the three human verbs and the loop's two terminal moves. The
watchdog sentence is deliberately NOT written yet. The T002 inventory §5
proposes an amendment reading "and — since F077 — the autonomy watchdog, which
writes `paused`"; applying that in R7 would replace a false claim with a
different false claim, because no such caller exists until R8. R8 adds the
watchdog clause in the same commit as the watchdog.

ALTERNATIVES CONSIDERED. Repairing all three in R8 alongside the writer keeps
one commit, but leaves a known-false docstring on disk across a round for no
gain. Repairing only the two the finding named leaves the third to be found
again by whoever greps next.

HOW TO REVERSE. Restore the sentences from git history. Nothing reads them
programmatically — no test asserts any of the three, which is why they went
stale unnoticed.

## DECISION F077 D8 (2026-08-14) — T002's action ships UNWIRED, and the four e2e ledger guards are R9's declared bill

CONTEXT. Inventory §7 names four whole-ledger guards in
`tests/orchestration/test_mission_e2e.py` that a new entry kind breaks: a
`numbers == [1, 2, 3, 4, 5, 6, 7]` list equality, a seven-kind move list that
also subscripts `e["move"]["kind"]` bare, a universally quantified
`context_digest`/`cost` assertion that a zero-cost entry fails, and
`len(e2e["open_at_pause"]) == 1` over the whole mission queue. None of them
breaks while the watchdog is not called by `run_mission`.

CHOSEN. R8 builds the pause, the decision and the ledger entry as a callable
action with unit tests and adds NO call site in `orchestrator_loop.py`. R9 adds
the call site and pays all four guards in that same round. The split is recorded
here so that R8's green gate is not read as a working feature: a passing R8
proves the action is correct in isolation and proves NOTHING about the loop,
and the handback and brief for R8 must say exactly that.

ALTERNATIVES CONSIDERED. Building and wiring in one round puts a new entry
shape, a new decision writer, a dedup rule and four rewritten whole-file
assertions in one diff, where a failure in any one of them is ambiguous between
the action and the wiring.

HOW TO REVERSE. Merge R8 and R9 into one round. The guard repairs are the same
work either way; only the diagnosis cost changes.
<<< DECISIONS-F077 <<<

── C3 — the R-0384 repair, all three sites ───────────────────────────
Three REWRITE pairs, ONE commit. Docstring prose only. For each pair prove the
FROM string is 0x and the TO string is 1x in its file afterwards. Each FROM was
verified by the reviewer to occur EXACTLY ONCE in its file at `55159180`.

(a) `packages/orchestration/mission_state.py`, in `set_mission_status`:

>>> MS-FROM >>>
    """Set a mission's status.  Only ever called by an explicit human command.

    Deliberately absent: any rule that moves a mission to ``achieved`` because
<<< MS-FROM <<<

>>> MS-TO >>>
    """Set a mission's status.

    Two kinds of caller write here.  The explicit human verbs — ``remedy
    mission achieve|abandon|pause``, through
    ``apps.cli.commands.mission_cmd._cmd_mission_set_status`` — and the loop's
    own terminal moves: ``mission_achieved`` writes ``achieved`` for
    ``declare_mission_achieved``, and ``execute_move`` writes ``abandoned``
    for ``abort_with_reason``, both in
    ``packages.orchestration.orchestrator_loop``.  A status on disk is
    therefore NOT evidence that a human put it there.

    Deliberately absent: any rule that moves a mission to ``achieved`` because
<<< MS-TO <<<

(b) `apps/cli/commands/mission_cmd.py`, in `_cmd_mission_set_status`:

>>> MC-FROM >>>
    human typing the command is the authority on what the mission's state is.
    Nothing in Remedy moves a mission between statuses on its own (F056).
    """
<<< MC-FROM <<<

>>> MC-TO >>>
    human typing the command is the authority on what the mission's state is.

    This surface is not the only writer, though.  The orchestrator loop's own
    terminal moves write ``achieved`` and ``abandoned`` with no human in the
    loop — see ``mission_state.set_mission_status`` for the full caller list —
    so F056's "nothing moves on its own" holds for this COMMAND, not for the
    status field.
    """
<<< MC-TO <<<

(c) `tests/cli/test_mission_cmd.py`, the `TestStatusTransitions` class docstring:

>>> TC-FROM >>>
    status may follow any other, because the human typing the command is
    the authority. Nothing in Remedy moves a mission's status on its own.
    """
<<< TC-FROM <<<

>>> TC-TO >>>
    status may follow any other, because the human typing the command is
    the authority. This surface is not the only writer, though: the
    orchestrator loop's terminal moves write achieved and abandoned with
    no human in the loop.
    """
<<< TC-TO <<<

Then append to `.agent/live_review.md`, as its new last physical line preceded
by one blank line, the LANDED-R384 slice. Same commit as the three pairs.

>>> LANDED-R384 >>>
Landed: R-0384 — repaired the stale no-autonomous-status-write claim at all THREE sites (set_mission_status in packages/orchestration/mission_state.py, _cmd_mission_set_status in apps/cli/commands/mission_cmd.py, and the TestStatusTransitions class docstring in tests/cli/test_mission_cmd.py); each new text names only the callers that exist at this commit and none of them mentions the watchdog, per DECISION F077 D7.
<<< LANDED-R384 <<<

── C4 — the handback ─────────────────────────────────────────────────
Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It carries the
per-commit changed-files tables, the REAL gate transcript below, the item-status
table for C0-C4, the open-findings count and the next expected action. If the
mandated content genuinely does not fit in 60 lines, exceed the cap and carry a
"Deviations, declared" line naming the real line count and the specific mandated
content that caused it (DECISION D15). Never drop a section to meet the cap.

── Gates — run every one, report the REAL value, never the word "green" ──
Report the actual output of each. A gate you did not run is a finding.
 1. `git status --porcelain` -> EMPTY, and `git worktree list` -> 1 line.
 2. `cmp .agent/authored/f077-r7.md .agent/last_block.md` -> exit 0. Report the
    shared sha256 and the line count; must be at or under 400.
 3. On `.agent/live_review.md`: `grep -c "^Gate: R6 — PASS"` -> 1,
    `grep -c "^Done: R-0383 — "` -> 1, `grep -c "^Landed: R-0383 — "` -> 0,
    `grep -c "^Landed: R-0384 — "` -> 1, `grep -c "^## Steps"` -> 1.
 4. Recompute the open set MECHANICALLY from `.agent/live_review.md` — every
    `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — and list the
    ids. Expected: 19 registered, 1 resolved, EIGHTEEN open. Name all eighteen.
    If your count differs from eighteen, report YOUR number and do not adjust
    it to match this line.
 5. `git show --numstat <C1-sha> -- .agent/live_review.md` and the same for the
    C3 commit: report both columns. C1's deletion column is 1 (the Landed line
    it rewrites); C3's deletion column is 0.
 6. For all eight FROM/TO pairs (PLAN, PLANNEXT, CTX, MS, MC, TC): report
    `grep -c` for the FROM and for a distinctive line of the TO in the target
    file after the edit. Every FROM -> 0, every TO -> 1. PLANNEXT and the
    live_review appends are APPEND-shaped; count their added lines within
    `git show --numstat` for that commit instead of over the whole file.
 7. `wc -l .agent/plan.md` -> at or under 49, and `grep -c ""` on it must equal
    `wc -l` (newline-terminated). `grep -c "^## Goal"` -> 1,
    `grep -c "^## Next Steps"` -> 1. On `.agent/context.md`:
    `grep -c "^## Active Branch"` -> 1, and `feature/f077-autonomy-watchdog`,
    `Steps`, `F077`, `resource`, `pytest` each at least 1.
 8. `git diff --stat 55159180..HEAD -- packages/ apps/ tests/` must list
    EXACTLY three files: mission_state.py, mission_cmd.py, test_mission_cmd.py.
    `git diff --stat 55159180..HEAD -- docs/` must be EMPTY.
 9. `git diff --name-only 55159180..HEAD` -> exactly the ten Change-line files.
10. Read the C3 diff hunks yourself and confirm every changed line sits inside a
    docstring. Report the three hunks' `+/-` counts.
11. `python3 -m pytest tests/cli/test_mission_cmd.py tests/orchestration/test_mission_state.py -q` ->
    baseline `164 passed`. Report the real number.
12. `python3 -m pytest tests/cli/test_golden_path.py -q` -> baseline
    `42 passed` (canary).
13. `python3 -m pytest tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py -q` ->
    baseline `142 passed`.
14. `python3 -m pytest tests/orchestration/test_watchdog.py -q` -> baseline
    `13 passed`; this round does not touch it.
15. `python3 -m ruff check packages/orchestration/mission_state.py apps/cli/commands/mission_cmd.py tests/cli/test_mission_cmd.py`
    -> exit 0. Repo-wide `ruff check` is RED on main (R-0364) and is NOT a gate.
16. `python3 -m apps.cli.main integrity check --json` -> report `passed`,
    `fail_count`, `check_count`.
17. Insertions per commit from `git show --numstat`; none over 500.
18. Trailing-whitespace scan over every touched file -> none.
19. `test -e .agent/STOP` -> report absent or present. Check it BEFORE you start
    and AGAIN at handback. If it appears, finish the current commit, write the
    handoff and STOP.
20. `git push -u origin feature/f077-autonomy-watchdog`. No `gh` command, no PR.

Handback: completion report + rewrite `.agent/handoff.md`.
