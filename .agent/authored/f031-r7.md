── STEP T001/3 — F031 Decision inbox · Runde 7 ───────────────
Goal:        Build T001: derive the inbox view from the decision
             queue, wire the blocked-subtree size that no decision
             reads today, expose it as one read endpoint, and pin it
             with a fixture per PRODUCING type. Record the R6
             verdict on the way. FIRST round to touch production
             code.

Fortschritt: ~20 % (F031 claimed; R1 through R6 landed and gated ·
             the source inventory and the three design rulings are
             on disk · T001 ships this round · T002 and T003 offen)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block ·
             C1 the plan · C2 the R6 gate entry and the R-0471
             recurrence · C3 the module and its tests · C4 the route
             and its test · C5 the handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r7.md                        (C0a)
             .agent/last_block.md                              (C0b)
             .agent/plan.md                                    (C1)
             .agent/live_review.md                             (C2)
             packages/orchestration/decision_inbox.py    (C3, NEW)
             tests/orchestration/test_decision_inbox.py  (C3, NEW)
             packages/orchestration/ui_server.py               (C4)
             tests/ui_server/test_decisions_endpoint.py  (C4, NEW)
             .agent/handoff.md                                 (C5)
             This list bounds the round's WRITES, not its ACTIONS:
             the push named in G11 is ordered explicitly and is not
             a file (R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `e73da3efd3ea0b58d1570beecaa4db34be7f2fc1`, the R6
handback commit and the current tip of `feature/f031-decision-inbox`.
Every SHA-shaped token in this block was passed to `git cat-file -t`
before emission and every one resolves, so G8 orders that sweep with
an EMPTY failure set and this block declares no positive control.
Stay on that branch; create none, never commit to `main`.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md`: `^- R-\d+ — ` 240 all DISTINCT, maximum
  `R-0679`; `^Done: R-\d+ — ` 2; `^Recurrence: R-` 14;
  `^Gate: R\d+ — ` 6, the keys `R19`, `R1`, `R2`, `R3`, `R4`, `R5`.
- The §3 item 10 open set — every `^- R-\d+ — ` paragraph minus
  every `^Done: R-\d+ — ` line — is 240 − 2 = 238 at that commit.
- `.agent/plan.md` 49 lines. `.agent/handoff.md` 77 lines.
- The `handlers` map of `do_GET` in
  `packages/orchestration/ui_server.py` has 13 keys and no
  `decisions` key, and NO test counts that map — so the new entry
  breaks no existing guard (§3 checklist item 7).

── Why this round exists ─────────────────────────────────────
R6 passed on every one of its ten gates under the reviewer's own
execution, in a NEW session, and every value its handback states
reproduced exactly. C2 records that verdict and registers R6's one
real defect as a RECURRENCE of R-0471 rather than a new id (§3 item
30). The design is settled, so T001 builds rather than re-opens it:
D1 rules the queue a derived read view, D3 fixes the acceptance set
at the EIGHT producing types, D2 keeps the badge in T002.

── Constraints ───────────────────────────────────────────────
1. Apply every authored slice BYTE FOR BYTE. Never retype, rewrap,
   reflow or "fix" one. If a slice looks wrong, apply it verbatim
   and DECLARE the disagreement in the handback: a contradiction
   inside this block is the reviewer's defect, not yours.
2. Slice transport. This block is saved verbatim as
   `.agent/authored/f031-r7.md` at C0a and mirrored byte-identically
   into `.agent/last_block.md` at C0b. Extract every slice
   PROGRAMMATICALLY out of the COMMITTED C0a blob by its marker
   LINES — `<<<SLICE <NAME>` opens, `<<<END <NAME>` closes. Marker
   lines never reach a target file.
3. Commit sequence, exactly: C0a, C0b, C1, C2, C3, C4, C5. No extra
   commit, none dropped, no reordering. C1 is the FIRST substantive
   commit because this round touches the finding ledger (§3 item
   23). The push runs after C5. To correct a landed commit, do NOT
   add one outside this sequence — declare it (R-0675).
4. C2 lands BOTH ledger paragraphs — GATE6 then RECUR471 — in that
   ONE commit, or neither. GATE6's text states that the recurrence
   is written in the same commit, and THIS constraint is what makes
   that sentence true (§3 item 20, the R-0524 carve-out).
5. Never amend, rebase, cherry-pick, force-push or rewrite history;
   never delete a branch; never merge; create no pull request.
6. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C5; if
   present, finish the commit in hand, write the handback and stop.
7. The slices this block carries are the whole text PLANF031R7 and
   the ledger paragraphs GATE6 and RECUR471. This paragraph names
   them and states no count; G3 orders you to report the count YOUR
   extractor measured.
8. C2 appends GATE6 then RECUR471 to `.agent/live_review.md`. THE
   APPEND SHAPE IS STATED ONCE, HERE, AND EVERY GATE NAMES THIS
   PARAGRAPH RATHER THAN RESTATING IT — the R-0471 counter-measure
   this round registers, applied to itself. Under the
   newline-INCLUDED convention each slice already ends in a
   newline, so the file at C2 is EXACTLY: the base blob, one
   newline, GATE6, one newline, RECUR471. Nothing follows, and the
   file ends in exactly one newline because RECUR471 carries it.
   THIS BLOCK CARRIES NO FROM/TO PAIR, so no containment reading is
   owed and none is stated.
9. THIS ROUND MINTS NO FINDING ID. `^- R-\d+ — ` must be 240 before
   and 240 after and the maximum must stay `R-0679`; the new record
   is a `Recurrence:` line against an OPEN finding, as §3 item 30
   requires for a defect the open set already holds.
10. Do not touch `.agent/decisions.md`, `.agent/f031_inventory.md`
    or anything under `docs/`. NO `docs/` UPDATE IS OWED AND THIS
    IS A RULING, not an oversight: `docs/` describes what IS, and
    this endpoint has no consumer until T002 ships the cards, so
    the round that makes it reachable documents it. Consequently
    `tests/docs/` and `test_roadmap_index.py` are NOT gated.
11. NO NEW DEPENDENCY, no new event kind, no CSS and no UI source
    file: D2 keeps the badge and the two constant-zero counters in
    T002, so `event_schemas.py` and everything under `apps/ui/` stay
    untouched. This round adds no visual surface, so
    `docs/ui/design_reference/` is not reached and owes no deviation.
12. Destructive verification, both red-proofs included, runs ONLY in
    a disposable `git worktree` under `.remedy-wt/`, removed BY ITS
    EXACT PATH (R-0662) and before the G10 suites. `.remedy-wt/dry`
    is PRE-EXISTING scratch belonging to no round of this feature:
    do not create a worktree there, read it or delete it.

── The production change: DESCRIBED, NOT SLICED ──────────────
C3 and C4 carry NO authored bytes. You write that code yourself, to
the specification below, under AGENTS.md's self-review loop. It
fixes BEHAVIOUR and SEAM, never wording: name things per AGENTS.md
"Code Discoverability Conventions" and put the one-line WHY comment
directly above each new definition.

S1 THE MODULE. New file `packages/orchestration/decision_inbox.py`.
It derives the inbox view and performs NO I/O — DECISION F031 D1
rules the queue a derived read view, so this module adds no storage
and opens no path. Public surface, named in a module docstring
`Public API` block the way `decision_queue.py` names its own:
  `DECISION_INBOX_VERSION` — int, 1
  `build_decision_inbox(job, events, now=None) -> dict[str, Any]`
It returns `{"version": DECISION_INBOX_VERSION, "job_id": <str>,
"decisions": [<card>, ...]}` — the same three key spellings that
`_cmd_decision_list` in `apps/cli/commands/decision.py` prints for
`--json`, so the browser and the CLI describe one thing one way.
The list comes from `list_decisions(job, events)` and nowhere else.

S2 THE CARD. Each card is `export_decision_json(d)` from
`decision_queue.py`, unchanged, plus exactly two ADDITIVE keys:
  `age_seconds` — int when `created_at` parses, else None
  `blocked_count` — int, never None
Nothing else is added, and no existing key is renamed or dropped.

S3 THE AGE. `created_at` is written by `datetime.isoformat()` — the
field `enqueue_task_decision` stores in
`packages/orchestration/escalation.py`. Parse with
`datetime.fromisoformat`; on ValueError, TypeError or the empty
string, `age_seconds` is None. A naive timestamp is read as UTC.
The value is `int((now - created).total_seconds())` CLAMPED AT 0, so
a skewed or future stamp prints 0 and never a negative. `now`
defaults to the current UTC time and is a parameter so a test can
fix it.

S4 THE BLOCKED COUNT. The seed set is `{UUID(payload["task_id"])}`
when that value parses as a UUID, and EMPTY otherwise.
`blocked_count` is `len(blocked_downstream(tasks, seeds))` with
`blocked_downstream` imported from
`packages/orchestration/dag_schedule.py`, and `tasks` read as
`getattr(job, "tasks", None) or ()` because `list_decisions` accepts
a JobPlan too and a JobPlan has no `.tasks`. An empty seed set makes
`blocked_downstream` return the empty set by its own first branch,
so every other type reports 0 with no special case. MEASURED, not
assumed: `.agent/f031_inventory.md` Q3 records that only branch 8 of
`list_decisions` sets `payload["task_id"]`, so `task_decision` is
the only type whose count can be non-zero today — and the WHY
comment says exactly that, because a reader who does not know it
reads the zeros as a bug.

S5 THE HONESTY RULE. No input makes this module raise. An unreadable
`created_at`, a `task_id` that is not a UUID, a job with no tasks, a
decision with an empty payload: each yields the honest value — None
age, 0 blocked — and the card still renders. That is the feature
file's "honest about unreadable entries", and S8 (e) pins it.

S6 THE SCOPE. Scoping is BY JOB and the route already enforces it:
`/api/jobs/<job_id>/decisions` loads exactly one job through
`_load_job`. This module never reads a second job and takes no
project argument. Record that in the module docstring as a
deliberate absence, per AGENTS.md "Code Discoverability
Conventions".

S7 THE ROUTE. In `packages/orchestration/ui_server.py`, add
`_build_decisions_json(job)` beside the other `_build_*_json`
builders — it calls `_load_events(job)` and returns
`build_decision_inbox(job, events)`, the same two-line shape
`_build_task_progress_json` already has — and add the single entry
`"decisions": _build_decisions_json` to the `handlers` map of
`do_GET`. NOTHING ELSE in that file changes: the two constant-zero
counters DECISION F031 D2 names belong to T002.

S8 THE MODULE TESTS. New file
`tests/orchestration/test_decision_inbox.py`, named after the source
it covers per AGENTS.md. The feature file suggests
`tests/ui_contract/…`; no such directory exists (the real one is
`tests/ui_contracts/`) and the module is orchestration, so the
naming convention wins — declared here, not discovered later. Cover:
 (a) A FIXTURE PER PRODUCING TYPE. DECISION F031 D3 fixes the set at
     the EIGHT types a branch of `list_decisions` produces:
     patch_approval, stop_reason, test_failure, repo_dirty,
     token_budget, memory_review, flight_plan_approval and
     task_decision. `worker_approval` and `revert_missing` have no
     producer and get NO fixture. Build each through the real
     upstream state `list_decisions` reads — never construct a
     `HumanDecision` directly and never monkeypatch
     `list_decisions`, because a fixture that bypasses the
     derivation proves nothing about it. Assert per type that a card
     appears with the expected `type` and both S2 keys.
 (b) THE BLOCKED MATH, against the DAG module and never a literal.
     Build a job with a linear task chain and an OPEN escalation
     record on the FIRST task; assert the card's `blocked_count`
     equals `len(blocked_downstream(job.tasks, {first.id}))`
     computed in the test AND that it is greater than 0. The second
     half is what makes the first discriminating: two zeros compare
     equal, so without it the assertion passes on a module that
     always returns 0.
 (c) EVERY OTHER TYPE REPORTS 0, so the pin holds both ways.
 (d) AGE. A fixed `now` and a known `created_at` give the exact
     integer; an empty and a malformed `created_at` each give None;
     a future `created_at` gives 0 and never a negative.
 (e) HONESTY. A `task_id` that is not a UUID, and a job with no
     tasks, each give a card with `blocked_count` 0 and raise
     nothing.
 (f) SHAPE. Assert the card's key set EQUALS the keys of
     `export_decision_json` plus exactly the two of S2, so a later
     field cannot be added silently.

S9 THE ROUTE TEST. New file
`tests/ui_server/test_decisions_endpoint.py`, reaching the route the
way existing `tests/ui_server/` tests reach theirs — read one and
follow it rather than inventing a harness. Assert that
`/api/jobs/<job_id>/decisions` with a valid token answers 200 with
the three S1 keys, that a card carries the two S2 keys, that an
invalid token is refused as the other endpoints refuse it, and that
an unknown job id answers through the same `_load_job` error path
rather than raising.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R7
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the merge
commit of pull request #213 which closed F022. `.agent/live_review.md` is the
source of truth for the record and the finding-id ceiling;
`.agent/f031_inventory.md` is the measured source inventory; `.agent/decisions.md`
carries DECISION F031 D1, D2 and D3, which settle the design.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact. DONE when the inbox lists fixture
decisions of every PRODUCING type with correct blocked-size math, answering from
a card round-trips through the write channel into the same effects the CLI
produces, the badge tracks live, and ordering follows a documented rule over age
and blocked size rather than vibes.

## Current Step
R7 builds T001: the derivation module `packages/orchestration/decision_inbox.py`,
its wiring into the `/api/jobs/<job_id>/decisions` route, and the contract tests
with a fixture per PRODUCING type. It also records the R6 verdict, and is the
first round of this feature to touch production code.

## Next Steps
1. R8 records the R7 verdict and plans T002: the cards, the generic options
   renderer, ordering and filtering, and the badge — where DECISION F031 D2
   binds, so the badge re-derives on refetch over the existing SSE stream.
2. T002 replaces the two constant-zero counters D2 names: the `decision_count`
   local of `_build_dashboard` and the `open_decisions` sum of
   `_build_live_state_json`, both in `packages/orchestration/ui_server.py`. The
   THIRD, in `_build_orchestrator_section`, is fed by `orchestrator_brain` and
   is NOT part of this feature.
3. T003 wires answering through the existing `decision.resolve` write channel,
   adds the clarification forms and deep links, and closes with the end-to-end.

## Risks
- Open findings, stated with the rule and the commit DECISION F009 D10 requires:
  by §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — `
  line — the open set is 238, measured at `e73da3ef`.
- The findings THIS FEATURE MUST STILL ACT ON — a narrower set, named as what it
  is and not called "open" — are R-0403, R-0413, R-0431, R-0445, R-0471, R-0495,
  R-0533, R-0574, R-0601, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677,
  R-0678 and R-0679; R-0495 and R-0574 are the two Highs, from F085 and F086.
- Only the `task_decision` branch of `list_decisions` carries a task id, so it is
  the only type whose blocked count can be non-zero — measured in
  `.agent/f031_inventory.md` Q3, and T001 pins it in both directions.
- The record holds `Gate: R19` from F022 as its seed entry. If F031 reaches its
  own R19 that key collides — the §3 item 26 defect. A round before then renames
  the seed or the scheme; this bullet is the reminder.
<<<END PLANF031R7

<<<SLICE GATE6
Gate: R6 — the F031 R6 entry. R6 PASSED ON EVERY ONE OF ITS TEN GATES, AND THE REVIEWER RE-RAN EVERY ONE OF THEM ITSELF — IN A NEW SESSION, AGAINST THE DISK RATHER THAN AGAINST ANY MEMORY OF HAVING ORDERED THEM — rather than reading the handback's word for any of them; every value that handback states reproduced exactly. TRANSPORT HELD IN ITS STRONGEST FORM AND ACROSS A SESSION BOUNDARY: the reviewer's own scratch original at `.remedy-wt/f031-r6.md` SURVIVED the session that wrote it, and it, the committed C0a blob, the committed C0b blob and `.agent/last_block.md` off disk are ALL sha256 `6db8af9e023718d359a47d5a5505adabcb834a84dbfafdd9fac8432115564c5b` over 25625 bytes and 310 lines, with C0a and C0b resolving to the SAME git blob `6ae136b7` — the primary proof shape §4 item 9 asks for, and taken here by a reviewer that did not author the bytes it was comparing. THE EXTRACTION printed 3 slices across 51 content lines against 310 total over 6 marker lines. `.agent/plan.md` at `c8dbf20e` is 2960 bytes and 49 lines, byte-equal to PLANF031R6 under the newline-INCLUDED convention with the trailing-newline-removed control FALSE at 2959, `^## Goal$` and `^## Next Steps$` once each, strictly under the cap of 50. THE LEDGER APPEND HELD AS AN EQUALITY OVER THE WHOLE FILE: at `f2a1a518` it is EXACTLY the base blob plus one newline plus GATE5 plus one newline plus FIND679, 546250 bytes to 553746 with the delta 7496 equal to 1 plus 4600 plus 1 plus 2894; an independent blank-line split went 279 units to 281 with the LAST TWO equal to GATE5 then FIND679 IN ORDER; and the reviewer flipped its own byte at offset 546450, inside the FIRST appended paragraph, which BOTH readers rejected while BOTH accepted the true file. THE SETS MOVED ONLY WHERE CONSTRAINT 8 ALLOWED: `^- R-\d+ — ` 239 to 240 all DISTINCT, ids ADDED exactly the one id `R-0679`, ids REMOVED the EMPTY SET, maximum `R-0678` to `R-0679`, `^Done: R-` 2 to 2, `^Recurrence: R-` 14 to 14 UNCHANGED, and `^Gate: R\d+ — ` 5 to 6 gaining exactly the key `R5`. MARKERS WERE LINE-ANCHORED 0 in both targets at their own commits; the four-path range holds nothing under `packages/`, `apps/`, `tests/` or `docs/` and neither `.agent/decisions.md` nor `.agent/f031_inventory.md`; the range path set MINUS the change set is EMPTY and the change set MINUS the range is exactly `.agent/handoff.md`; four single-parent commits with insertions 310, 172, 23 and 4, each under the 500 cap; `git ls-files .remedy-wt` 0, the zip glob 0, one worktree, `git status --porcelain` 0. THE BLOCK'S OWN OBJECT IDS WERE SWEPT: 14 occurrences over 11 distinct word-bounded hex tokens, every one resolving under `git cat-file -t` as one blob and ten commits, so the failing set is EMPTY exactly as that block predicted with no positive control available to it. THE FIVE SUITES ARE THE REVIEWER'S OWN, run SERIALLY with never two pytest processes alive, every one REAL exit code 0 at 470, 52, 21, 16 and 42 — cell for cell the readings taken at `49c50d05`, so there is no difference to account for. THE PUSH DISCHARGED, AND THIS SENTENCE IS THE CARRIER FINDING R-0679'S FIX CLAUSE NAMES: measured by the reviewer against `git ls-remote`, the local and remote tips of `feature/f031-decision-inbox` are both `e73da3efd3ea0b58d1570beecaa4db34be7f2fc1`; no pull request exists, and nothing was merged. THE HANDBACK DERIVED ITS OWN CAP rather than quoting one, reading the tier as 60 from the five commits its constraint 3 fixes, landing at 77 lines with a DECISION D15 stated-cause line naming that count and the mandated content behind it, no section dropped and no token cap claimed. THE ROUND'S THREE DECLARED ITEMS ARE ALL THE REVIEWER'S OWN, AND THE WORKER HANDLED EVERY ONE CORRECTLY: the newline contradiction is registered as a recurrence of R-0471 in THIS SAME COMMIT, which constraint 4 of the R7 block fixes; constraint 10 of the R6 block said the worktree is removed "BEFORE the G7 suites" where the suites are G9, and it was removed before both; and the PLANF031R6 Risks bullet calls T001 a ROUND where T001 is a slice and R7 is the round, which `.agent/plan.md` corrects by rewrite in this same round, landed text being corrected by dating and never by editing. THE VERDICT IS PASS.
<<<END GATE6

<<<SLICE RECUR471
Recurrence: R-0471 — TWO CLAUSES OF ONE BLOCK DISAGREED ABOUT A SINGLE NEWLINE. SECOND INSTANCE, at F031 R6, and it is the reviewer's own. NO NEW ID IS MINTED: R-0471 already holds this family — a gate literal quoting an append boundary, read against the convention paragraph of the SAME block — and the open set was searched for the DEFECT before any id was considered (§3 item 30), which is how this arrives as a recurrence rather than as R-0680. THE MEASUREMENT, taken by the reviewer at `f2a1a518`: G5 of the R6 block orders `.agent/live_review.md` to be "the base blob, then one newline, then GATE5, then one newline, then FIND679, then one newline", while constraint 7 of that same block orders exactly one blank line between the appends and the file "ending in exactly one newline". Under the newline-INCLUDED convention the block itself declares, GATE5 and FIND679 each already carry a trailing newline, so G5's literal yields a trailing BLANK LINE and breaks constraint 7, while dropping that last newline is the only shape satisfying both — the two clauses cannot both be obeyed as written. THE WORKER RESOLVED IT THE RIGHT WAY ROUND: it built base plus newline plus GATE5 plus newline plus FIND679, reported the literal variant as MEASURED False rather than as an opinion, and declared the contradiction instead of choosing silently; the reviewer re-derived both readings independently and confirms the applied shape is the one that satisfies constraint 7 and reproduces exactly the arithmetic GATE5 itself quotes. WHAT MAKES IT A RECURRENCE RATHER THAN A NEW CLASS: R-0471's instance was a C2 contract and a gate literal disagreeing about one newline at an append boundary, and this is the same two clause KINDS disagreeing about one newline at an append boundary in a different file — the R-0437 newline family crossed with the clause-versus-clause defect, which is how R-0471's own body already names it. WHY IT RECURRED IS THE PART WORTH RECORDING: R-0471's counter-measure is a mechanical pass in which every gate literal quoting an append boundary is checked against the same block's convention paragraph before emission, and the R6 block ran no such pass — it wrote the equality gate and the constraint in different SECTIONS and never read the two against each other, which is the same sweep failure §3 item 16 records for headings and §3 item 32 for gate adjectives. A counter-measure that requires a reviewer to remember to compare two distant sentences fails exactly where the R-0486 and R-0488 family fails. THE COUNTER-MEASURE IS REPLACED, not merely restated, and binds every block from here: a block that orders a whole-file equality over an append states that equality EXACTLY ONCE, in the same paragraph that declares its newline convention, and every gate touching that boundary NAMES that paragraph instead of restating the formula. A formula written twice is a formula that can disagree with itself, and this is the second round in which it has. Constraint 8 of the F031 R7 block carries that form, which is this counter-measure applied by the block that registers it.
<<<END RECUR471

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output,
and report ONE LINE PER GATE in the handback, transcripts kept out
of it (R-0582). "Green" as a word is a finding. Every gate runs at a
commit STRICTLY EARLIER than C5, which writes the handback (§3 item
31).

G1  Branch and cleanliness. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`. `.agent/STOP` read
    from disk is ABSENT before C0a and again before C5. Report
    `git status --porcelain` line count after each of C0a, C0b, C1,
    C2, C3 and C4; each must be 0.

G2  Transport. Report sha256, byte count and line count for FOUR
    readings: `.remedy-wt/f031-r7.md` before C0a, the committed C0a
    blob, the committed C0b blob, and `.agent/last_block.md` off
    disk after C0b. All four must be EQUAL. Report the git blob id
    of C0a's and C0b's file; they must be the SAME id.

G3  Extraction. Run your extractor over the COMMITTED C0a blob and
    report the slice count, the CONTENT lines inside markers, and
    the TOTAL line count. Report the numbers YOUR extractor printed.

G4  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R7
    under your stated newline convention; report slice length, file
    length and convention. NEGATIVE CONTROL: NOT byte-equal to that
    slice with its trailing newline REMOVED. `^## Goal$` 1,
    `^## Next Steps$` 1, `wc -l` STRICTLY under 50.

G5  The ledger append, as ONE equality over the whole file, in the
    shape constraint 8 states — name that paragraph, do not restate
    its formula. Report the boolean and the byte arithmetic. Report
    a SECOND, INDEPENDENT reading: split the C2 file on blank lines
    and confirm the LAST TWO units equal GATE6 then RECUR471 IN
    ORDER, with the unit count before and after. NEGATIVE CONTROL:
    flip ONE byte inside the FIRST appended paragraph in a
    disposable worktree; BOTH readers must reject the mutant and
    BOTH accept the true file.

G6  The sets, base versus C2 in `.agent/live_review.md`:
    `^- R-\d+ — ` 240 → 240 all DISTINCT, ids ADDED and ids REMOVED
    both the EMPTY SET, maximum `R-0679` → `R-0679`, `^Done: R-`
    2 → 2. `^Recurrence: R-` 14 → 15, the one gained line naming
    `R-0471`. `^Gate: R\d+ — ` 6 → 7, gaining exactly the key `R6`,
    with `R19`, `R1`, `R2`, `R3`, `R4` and `R5` still present.

G7  Markers, paths, structure and hygiene. Line-anchored `^<<<SLICE `
    and `^<<<END ` both count 0 in `.agent/plan.md` at C1, in
    `.agent/live_review.md` at C2 and in each of the four source and
    test files at C3 and C4. Report that
    `git diff --name-only <base>..C4` names NEITHER
    `.agent/decisions.md` NOR `.agent/f031_inventory.md`, and no
    path under `docs/` or `apps/`. Over C0a..C4 report per commit
    that it is single-parent and its INSERTION count — the `+`
    column only, per AGENTS.md DECISION F104 D1 — each under 500.
    Report the range path set MINUS the change set (EMPTY) and the
    change set MINUS the range (exactly `.agent/handoff.md`, which
    C5 writes). Report `git ls-files .remedy-wt` as 0, `git ls-files`
    over `*.zip` as 0, and `git worktree list` as 1 line. FOR THE
    REFLOG, state the SCOPE and the FIELD in the reading itself:
    over THIS ROUND'S entries only, read by the OPERATION PREFIX
    before the first colon of `git reflog --format=%gs`, report
    `amend`, `rebase` and `cherry` each 0, and how many entries you
    scoped to.

G8  The block's own object ids. Extract every SHA-shaped token from
    the COMMITTED C0a blob with the word-bounded pattern
    `[0-9a-f]{7,40}` — whose boundaries do NOT match the 64-char
    sha256 digests this block also carries — and pass each to
    `git cat-file -t`. THE FAILING SET MUST BE EMPTY: this block
    quotes no non-existent id, so it has no positive control.
    Report the token count YOUR extractor measured, the failing
    set, and the type printed for each token.

G9  THE TWO RED-PROOFS, each in a disposable worktree at C4, each
    removed by its exact path afterwards. Both are ordered as
    PROBES: report WHICH test node ids failed and how many; do not
    predict a count. If NOTHING fails under either mutation, say so
    plainly — that is the honest answer, and it means the test is
    not discriminating. Declare it; never repair it silently.
    (a) In `decision_inbox.py`, force the blocked-count seed set
        EMPTY unconditionally, all else intact, then run
        `python3 -m pytest tests/orchestration/test_decision_inbox.py -q`.
        A green run means S8 (b)'s greater-than-zero half is
        missing or its fixture raises no open task decision.
    (b) In `ui_server.py`, rename the `handlers` key `decisions` to
        `decisionz`, the builder itself intact, then run
        `python3 -m pytest tests/ui_server/test_decisions_endpoint.py -q`.

G10 Suites, run SERIALLY, never two pytest processes at once, in
    the PRIMARY checkout at the C4 tree, with `git worktree list`
    reported as 1 line immediately BEFORE the first pytest command.
    All must exit 0; report the real exit code and the counts:
      python3 -m pytest tests/orchestration/test_decision_inbox.py -q
      python3 -m pytest tests/ui_server/test_decisions_endpoint.py -q
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    The reviewer executed the last five at `e73da3ef` and measured,
    in that order, 470, 52, 21, 16 and 42, every one exit 0. The
    `tests/ui_server/` count MUST GROW by exactly the number of
    tests S9 adds, since that file lands in that directory — report
    the new total and that arithmetic, and account for any other
    difference. Also run `python3 -m ruff check` over the four paths
    of the change set under `packages/` and `tests/`, using the
    repository's OWN configuration — no `--isolated`, no hand-passed
    line length (finding R-0463) — and report its real exit code.
    `ui_server.py` already existed, so if it carries pre-existing
    findings, compare the rule-code MULTISET at the base against C4
    and report both rather than demanding exit 0 on that path.

G11 The push. AFTER C5, run
    `git push origin feature/f031-decision-inbox`. No `--force`, no
    `--force-with-lease`, no history rewrite, no branch deletion, no
    pull request. THIS GATE'S OUTCOME IS NOT A VALUE OF ANY FILE
    THIS ROUND WRITES, and its carrier is named here so you inherit
    ONE instruction rather than two: the reviewer measures the
    pushed tips at the next gate and records them in the R7 entry of
    `.agent/live_review.md`. In `## External actions` write the push
    COMMAND and that sentence — which is how this block satisfies
    `docs/agents/handback_template.md` and R-0679's fix clause
    together. Report the real outcome in your final message.

── Handback ──────────────────────────────────────────────────
Rewrite `.agent/handoff.md` at C5 per docs/agents/handback_template.md:
feature and round, branch, base and commit SHAs, a changed-files
table per commit, the item-status table covering C0a, C0b, C1, C2,
C3, C4, C5 and the push, ONE LINE PER GATE with its real result, the
finding counts, and the next expected action. Carry the
`Fortschritt:` block above VERBATIM — count its lines yourself and
carry exactly those; this block states no numeral for them.

THE HANDBACK LINE CAP: this block states no cap and no tier. Resolve
it from AGENTS.md under `### handoff.md` against the commit count
constraint 3 fixes, and report BOTH that count and the tier. If the
MANDATED content genuinely does not fit, exceed it and carry a
DECISION D15 "Deviations, declared" line naming your measured count
and the mandated content behind it. Never drop a section to fit. Do
NOT claim compliance with any token cap: that cap was withdrawn.

Any finding count you state carries the RULE that produced it and
the COMMIT it was measured at, in the same sentence, per DECISION
F009 D10. A narrower set is named "the findings this feature must
still act on" and is never called "open" unqualified.

Your `## Next` section names, in order: Phase 1 rule 1 (re-read
`.agent/STOP` from disk), then that NO pull request exists for this
branch and none should be created yet, then that R8 records the R7
verdict — which by DECISION F085 D9 no artefact of this round can
carry — and plans T002.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────
