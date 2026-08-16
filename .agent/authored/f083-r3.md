── STEP R3/8 — F083 CI self-check — RECORD R2, RULE THE STAGE SET ─────────────

Goal:
  Record the R2 PASS, register the two defects R2 exposed — both the reviewer's
  own — repair the finding-count sentence one of them put on disk, and rule
  DECISION F083 D2: the four stage-set questions R2's inventory left open that
  its own measurements plus the feature file's Do-not-touch list already decide.
  It builds no stage runner and writes no code. R4 builds T001 over this ruling.

Bundle, in commit order:
  C0a  copy the reviewer's scratchpad original to `.agent/authored/f083-r3.md`
  C0b  mirror it byte-identically into `.agent/last_block.md`
  C1   `.agent/live_review.md` — GATE-R2 + R-0453 + R-0454, appended at EOF in
       ONE commit. Findings persist FIRST (planner_reviewer_prompt §4.4).
  C2   `.agent/decisions.md` (DEC-D2 appended at EOF) and `.agent/plan.md`
       (PLAN, whole file — this is R-0453's repair), ONE commit.
  C3   `.agent/handoff.md`, the handback, alone.

BASE: 290e52ee. Re-derive `git rev-parse HEAD` before the first commit and report
whether it equals 290e52ee (R-0428). If it does NOT, stop and hand off.

TRANSPORT: the reviewer's scratchpad original of THIS block is on disk at
`.remedy-wt/.cache/f083-r3/f083-r3.md`, which `.gitignore` drops (line 235,
`.remedy-wt/`). C0a is a byte COPY of that file — do not retype it, do not
reflow it, do not strip anything.

SLICE CONVENTION (R-0437): every FROM and TO body below is the lines between its
markers INCLUDING the trailing newline of its last line, and every shape is
declared UNDER THAT CONVENTION. The block's authored units are, listed: two EOF
appends (GATE-R2-BLOCK into `.agent/live_review.md`, DEC-D2 into
`.agent/decisions.md`) and one whole-file replacement (PLAN). No numeral is
stated for that list — the list IS the statement (R-0402, R-0441).

Constraints:
  1. Change set: `.agent/authored/f083-r3.md`, `.agent/last_block.md`,
     `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
     `.agent/handoff.md`. Nothing else. `packages/`, `apps/`, `scripts/`,
     `tests/` and `docs/` all stay EMPTY in the range diff. Gate 8 measures that.
  2. Apply every slice BYTE-VERBATIM. A defect in my text is a declared deviation
     in the handback, never a silent repair. No slice contains an instruction
     addressed to you about the file it lands in (R-0450).
  3. C1 lands BEFORE C2. Push after C3. Create NO pull request.
  4. This round adds NO worktree. `git worktree list` is one line throughout.
  5. `.agent/f083_inventory.md` is NOT edited. It is R2's measured record and it
     stays as it was written; D2 rules OVER it, in `.agent/decisions.md`, and
     does not rewrite the measurements it rules over.

--- BEGIN SLICE GATE-R2-BLOCK --- (APPEND to .agent/live_review.md, C1, with exactly one blank line between the file's current last line and the first line of this slice)
Gate: R2 — PASS. Verification tier: the docs gate, the two live-state readers and the canary, all four re-run by the reviewer at the round's head, plus an independent re-derivation of the inventory's load-bearing arithmetic and a spot-check of two of its six timed stage runs; no full-suite claim is made, because this round changed no code and no test. All twelve ordered gates reproduce against the committed tree. TRANSPORT held: scratchpad, `.agent/authored/f083-r2.md` and `.agent/last_block.md` are all sha256 6521fd1cbe019c44cb0093c5af9c62427c5c7179ce31eced251bed45cd41002a, 23836 bytes, 277 lines, byte-equal, declared footer 277 equal to measured 277. C1's prefix property is True with a `6 0` numstat. C2's three applied units each hold against the slice extracted from the COMMITTED authored file: `.agent/decisions.md` is a pure append equal to `b"\n" + DEC-D1`, the `.agent/context.md` pair is 1/0/1 with `FROM in TO` False and the composite True, and `.agent/plan.md` byte-equals PLAN at 41 lines with no `- [ ]` line. The open set at HEAD is 80 registered, 0 resolved, max R-0452, next free R-0453, no duplicate id. The change set is 7 paths before the handback and 8 after, EMPTY under `packages/`, `apps/`, `scripts/`, `tests/` AND `docs/` — this round wrote no code, no test and no doc, as ordered. Insertions 277 · 212 · 6 · 382 · 152, none over 500. The inventory itself is the round's product and it was checked as such rather than read: the reviewer re-collected the five stage selections at HEAD and got union 17007 against a suite of 17007, uncovered 0, and exactly one non-empty pairwise overlap, `standard ∩ smoke` = 8, every id in `tests/cli/test_pytest_runner.py` — reproducing Q4 exactly, and reproducing the value the reviewer had measured independently BEFORE the block was emitted, which is R-0364 holding on both sides of the round. Two of the six timed stages were re-run: `architecture` 71 passed exit 0 and `ui` 393 passed 4 skipped exit 0 in 6.92 s, against the inventory's recorded 71/0 and 393/4 at 6.92 s pytest time — equal, including the inventory's distinction between driver time and pytest time, which is a precision the round was not asked for and volunteered. The inventory's most consequential result is a negative one and it is stated plainly: `fast` costs 391.8 s serially for 3970 items while `standard` costs 134.1 s under `-n auto` for 12546, so the split the feature file suggests is inverted with respect to cost. That number is why R4 does not pin a parallelism setting from this data, and DECISION F083 D2 below says so. Q3 is the round's other real catch — the feature file's `ui-contract` and `live-provider` do not exist under those spellings, and the inventory names `ui_contract` and `real_ollama` as what does exist rather than resolving the disagreement silently, which is exactly what the question asked for. TWO findings are registered below and both are defects of the reviewer's own block text; the worker declared both, with the disk evidence, before the reviewer read the diff, which is the eighth consecutive round.

- R-0453 — Low, A SENTENCE COUNTED A SET THE SAME SLICE HAD ALREADY ENUMERATED, AND THE TWO DISAGREE ON DISK. Found by the WORKER while applying the R2 PLAN slice. That slice's opening paragraph enumerates the branch's findings as "R-0448 to R-0452" — five — and its Risks section then reads "Five of the six findings registered on this branch are defects in the reviewer's own block text". The reviewer confirmed both sentences are in `.agent/plan.md` at d2282fca, lines 5 and 35, and that gate 10 measured max R-0452 with 80 registered against 75 carried, which makes the branch's own count five. The numeral is wrong twice over: there is no sixth finding, and the qualifier "five of" implies an exception that does not exist — all five ARE reviewer-block defects. Nothing downstream consumed the number, and `.agent/live_review.md` remains the source of truth the plan says it mirrors, so the damage is a reader's confusion at one file. Low for that reason. This is the R-0402 / R-0404 / R-0436 family in its plainest form: a numeral written next to an enumeration that already stated the count. The standing rule from those findings — count it mechanically or state no numeral, and prefer writing the range alone — was in force and was broken anyway, in a slice whose own first paragraph carried the correct enumeration two dozen lines above. Repaired in this round's PLAN slice by removing the numeral and letting the range stand. OPEN until the repair is reviewed.

- R-0454 — Low, A GATE ORDERED A MEASUREMENT OF SUBJECTS THE BLOCK NEVER DEFINED, SO THE WORKER HAD TO CHOOSE THEM. Found by the WORKER, which declared it as its second deviation. R2's Q4 defines five stage selections by name and expression — fast, standard, ui, smoke, excluded — and Q5 then orders "Run fast, ui, smoke, safety and architecture serially". `safety` and `architecture` are not among the five and no expression is given for either anywhere in the block. The worker inferred `-m "safety and not real_ollama"` and `-m "architecture and not real_ollama"` by analogy with the `ui` and `smoke` forms, recorded both exact commands in the inventory, and declared the inference rather than presenting it as ordered. The reviewer re-ran `architecture` and reproduces 71 passed, so the inference was the right one — which is the problem, not the mitigation: a worker that guesses correctly is still a worker that guessed, and the protocol's whole point is that it must never have to. This is R-0438's family, an unrunnable-as-written gate, reached from the other side: R-0438 was a path that did not resolve on disk, this is a subject that does not resolve in the block. Low, because the inference was declared, mechanically checkable and correct. Standing rule from here, binding the reviewer: every noun a Done-when gate orders measured is either defined in the same block or resolvable to a single value on disk, and the pre-emission checklist resolves each one before emission — the same walk R-0452 added for gate values, extended to gate subjects. OPEN.
--- END SLICE GATE-R2-BLOCK ---

--- BEGIN SLICE DEC-D2 --- (APPEND to .agent/decisions.md, C2, with exactly one blank line between the file's current last line and the first line of this slice)
## DECISION F083 D2 — the stage set, ruled from R2's measurements (2026-08-15)

R2's inventory closed with six open questions. Four of them are already decided
by its own measured data plus the feature file's Do-not-touch list, and leaving
them open would make R4 guess. They are ruled here. Two are NOT ruled, and the
reason each is deferred is stated.

RULED.

D2.1 — The stage set is exactly the five selections Q4 defines: `fast`,
`standard`, `ui`, `smoke` and `excluded`. Reason: measured, they cover the suite
(union 17007 against a suite of 17007, uncovered 0), and no sixth selection is
needed to reach any test.

D2.2 — `safety` and `architecture` do NOT become stages of their own. Reason:
Q4's open question 2 measured them as set intersections over the same node ids —
`architecture`'s 71 items all sit inside `fast`, and `safety`'s 33 split 21 into
`fast` and 12 into `standard`. Promoting either would introduce overlaps the
five-stage set does not have, and `safety` would straddle two stages. They stay
markers, usable for ad-hoc selection, and the stage runner does not name them.

D2.3 — The `standard ∩ smoke` overlap of 8 is ACCEPTED and documented, not
removed. Reason: every one of the 8 ids is in `tests/cli/test_pytest_runner.py`,
which the conftest lists in both `SUBPROCESS_FILES` and `SMOKE_FILES`; removing
the overlap means editing marker semantics, which the F083 feature file's
Do-not-touch list forbids. The stage runner therefore MAY run those 8 twice and
the summary table says so — a documented double-run beats a silent marker edit.

D2.4 — The `determinism` and `budgets` stages the feature file names are NOT
marker selections. Reason: Q8 recorded that neither name exists among the nine
declared markers, so making them selections requires declaring new markers and
assigning them across the tree, which is the same marker-semantics change D2.3
refuses. They are script invocations the stage runner calls and whose exit code
it folds into the summary, exactly as the feature file's own design paragraph
describes the budgets stage.

DEFERRED, with the reason.

D2.5 — Per-stage parallelism is NOT pinned here. Q5 measured `fast` at 391.8 s
serial for 3970 items and `standard` at 134.1 s under `-n auto` for 12546, so the
cost is dominated by serialization rather than by selection — but that single
reading does not say what `-n auto` does to `fast`, and the three small stages
may lose more to worker startup than they gain. R4 measures each of the five both
ways, once, and pins the setting per stage from that measurement. Pinning it now
would be a guess dressed as a decision.

D2.6 — The feature file's `ui-contract` and `live-provider` spellings are NOT
corrected now. Reason: `docs/roadmap/features/T2_F083.md` is edited in the round
that brings its Built State current before closure; correcting prose in a round
that writes no other doc would be scope drift, and the inventory already records
what exists under which name. Q3's record is the interim answer.

Reverse any part of this decision by deleting its numbered paragraph.
--- END SLICE DEC-D2 ---

--- BEGIN SLICE PLAN --- (WHOLE FILE replacement of .agent/plan.md, C2 — this is R-0453's repair)
# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0455. Open findings: the seventy-five carried out
of the F082 record plus R-0448 to R-0454 registered on this branch.
`.agent/live_review.md` is the source of truth; this file mirrors it.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure in
each stage fails the right stage with a readable summary, and total runtime
stays within a documented budget.

## Current Step
R3 records the R2 PASS, registers R-0453 and R-0454, repairs the finding-count
sentence R-0453 reports, and rules DECISION F083 D2 — the stage set is Q4's five
selections; `safety` and `architecture` do not become stages; the eight-item
`standard`/`smoke` overlap is accepted and documented; `determinism` and
`budgets` are script invocations rather than marker selections. Per-stage
parallelism and the feature file's marker spellings are deferred, each with its
reason. It writes no code.

## Next Steps
1. R4 builds T001 over D2: the stage runner, the five marker selections, the
   summary table and its tests, plus the one measurement D2.5 defers — each
   stage timed with and without `-n auto`, and the per-stage setting pinned from
   that reading.
2. The CLI seam is the one Q8 names; the stage runner reuses the existing pytest
   subprocess runner rather than reimplementing it.

## Risks
- Every finding registered on this branch so far is a defect in the reviewer's
  own block text, and R-0452 records that a counter-measure written as finding
  prose does not bind the next block. R-0453 and R-0454 are the evidence that it
  still does not: both were registered one round after their own family's rule.
- `fast` costs 391.8 s, measured once on one machine with an unrelated stale
  process present. The documented runtime budget the Goal requires cannot rest
  on a single reading, and no hosted runner exists yet to give a second one.
- D2.3 accepts a double-run of eight tests to avoid editing marker semantics.
  If the summary table does not state it, the acceptance becomes a silent defect.
--- END SLICE PLAN ---

Done when — run every gate and record its REAL value; a gate you cannot run is
reported as not run, never as green:

 1. `git status --porcelain` EMPTY before the first commit and before C3.
    `git worktree list` ONE line throughout. `.agent/STOP` ABSENT at round start
    and again at handback (R-0347).
 2. BASE: `git rev-parse HEAD` before the first commit; report it and whether it
    equals 290e52ee.
 3. TRANSPORT, bytes read in Python: report sha256, byte count and line count of
    `.remedy-wt/.cache/f083-r3/f083-r3.md`, `.agent/authored/f083-r3.md` and
    `.agent/last_block.md`, whether all three byte strings are EQUAL, and whether
    the measured line count equals this block's declared footer count.
 4. C1 PREFIX PROPERTY over `<C1>^..<C1>`: `pre` is a prefix of `post`, and
    `post[len(pre):]` equals `b"\n" + GATE-R2-BLOCK` byte-for-byte, the slice
    extracted from the COMMITTED `.agent/authored/f083-r3.md` by its markers.
    Report the numstat and confirm its deletion column is 0.
 5. C2 APPLIED TEXT, each proven against the slice extracted from the committed
    authored file: (a) `.agent/decisions.md` — `pre` is a prefix of `post` and
    `post[len(pre):]` equals `b"\n" + DEC-D2`; (b) `.agent/plan.md` byte-equals
    PLAN as a whole file — report sha256 and line count, under 50, with `## Goal`
    and `## Next Steps` present and no `- [ ]` line.
 6. R-0453 IS REPAIRED, measured on `.agent/plan.md` at HEAD as literals: the
    string `six findings` 0x, the string `Five of the six` 0x, and the string
    `R-0448 to R-0454` 1x. Report all three.
 7. `.agent/f083_inventory.md` is UNCHANGED by this round (Constraint 5): report
    `git diff --name-only 290e52ee..HEAD -- .agent/f083_inventory.md` and confirm
    it is empty.
 8. CHANGE SET, measured BEFORE the handoff is written into C3, so it lists five
    paths and `.agent/handoff.md` is the sixth and last:
    `git diff --name-only 290e52ee..HEAD`. Report the full list and its count.
    Restricted to `packages/`, `apps/`, `scripts/`, `tests/` and `docs/` it must
    be EMPTY. Report that restriction as a measured list.
 9. VERIFICATION, each command run separately with its exit code read from the
    process, never from a pipe (R-0438). Report collected count and real exit
    code for EACH: `python3 -m pytest tests/docs/ -q`, which the reviewer
    measured at 295 collected, 295 passed, exit 0 at BASE; `python3 -m pytest
    tests/regression/test_resource_safety.py -q`, 21 passed, exit 0 at BASE;
    `python3 -m pytest tests/orchestration/test_integrity_gate.py -q`, 15 passed,
    exit 0 at BASE; and the canary `python3 -m pytest
    tests/cli/test_golden_path.py -q`, 42 collected, 42 passed, exit 0 at BASE.
10. OPEN SET at HEAD: count `^- R-\d+ — ` paragraphs, count `^Done: R-\d+ — `
    lines, report both, their difference, the max id, the next free id and any
    duplicate id. Report what you MEASURE.
11. INTEGRITY GATE, in Python because the `remedy` CLI is denied in this session
    class (R-0408): `python3 -c "from packages.orchestration.integrity_gate
    import run_integrity_checks, export_integrity_json; import json;
    print(json.dumps(export_integrity_json(run_integrity_checks())))"` — report
    `passed`, `fail_count`, `check_count` and every named check's status.
12. Insertions (`+` column only) for C0a, C0b, C1 and C2 — report each; none over
    500. C0b is a verbatim single-`.agent/`-file rewrite and is exempt by the
    AGENTS.md counting rule; report its number anyway. C3's own insertion count
    cannot exist inside C3 (R-0149): report it in your final message instead.

The push and its result, the post-C3 clean-tree reading and the open-PR list all
come into existence AFTER C3 writes the handback, so per R-0449 and R-0452 they
are NOT ordered into that file: run `git push -u origin feature/f083-ci-self-check`
after C3, create no pull request, and report all three in your final message.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md, as
C3 — feature and round, branch, per-commit changed-files tables, every gate value
above, the item-status table covering every C-item and every gate, open findings
with max and next free id, and the next expected action, which is R4 building
T001 over DECISION F083 D2. C3 cannot table its own SHA (R-0371, R-0149); say so
rather than inventing one. Repeat this line verbatim as the Fortschritt line:

Fortschritt: 8 % (F083 beansprucht · R1 und R2 PASS · Marker-Inventar gemessen · Stage-Set per DECISION F083 D2 entschieden · R-0453 und R-0454 registriert · noch kein Stage-Runner, kein Code) — gemessen, nicht geschätzt

If any gate is RED, or anything here contradicts what you find on disk: finish
the commit you are in, write the handoff naming the exact blocker, and end. Do
not widen scope to route around it (G8).

BLOCK SIZE, measured on these final bytes: 230 lines (cap 400, DECISION F105 D5).
──────────────────────────────────────────────────────────────────────────────
