── STEP R2/8 — F083 CI self-check — T001 MARKER INVENTORY ─────────────────────

Goal:
  Record the R1 PASS, register the two defects R1 exposed — both the reviewer's
  own — and produce T001's first deliverable: an inventory of the marker
  landscape the CI stages will select over, written from MEASURED values with a
  file-and-symbol citation behind every claim. It builds no stage runner. The
  feature file's orchestrator brief makes this inventory T001's precondition,
  and the stage split follows this data rather than the other way round.

Bundle, in commit order:
  C0a  copy the reviewer's scratchpad original to `.agent/authored/f083-r2.md`
  C0b  mirror it byte-identically into `.agent/last_block.md`
  C1   `.agent/live_review.md` — GATE-R1 + R-0451 + R-0452, appended at EOF in
       ONE commit. Findings persist FIRST (planner_reviewer_prompt §4.4).
  C2   `.agent/f083_inventory.md` (NEW, worker-authored — see THE INVENTORY),
       `.agent/decisions.md` (DEC-D1 appended at EOF), `.agent/context.md`
       (CTX-R2 pair) and `.agent/plan.md` (PLAN, whole file), ONE commit.
  C3   `.agent/handoff.md`, the handback, alone.

BASE: 928120ab. Re-derive `git rev-parse HEAD` before the first commit and report
whether it equals 928120ab (R-0428). If it does NOT, stop and hand off.

TRANSPORT: the reviewer's scratchpad original of THIS block is on disk at
`.remedy-wt/.cache/f083-r2/f083-r2.md`, which `.gitignore` drops (line 235,
`.remedy-wt/`). C0a is a byte COPY of that file — do not retype it, do not
reflow it, do not strip anything.

SLICE CONVENTION (R-0437): every FROM and TO body below is the lines between its
markers INCLUDING the trailing newline of its last line, and every shape is
declared UNDER THAT CONVENTION. The block's authored units are, listed: two EOF
appends (GATE-R1-BLOCK into `.agent/live_review.md`, DEC-D1 into
`.agent/decisions.md`); one REWRITE pair with FROM and TO disjoint (CTX-R2 in
`.agent/context.md`); and one whole-file replacement (PLAN). No numeral is
stated for that list — the list IS the statement (R-0402, R-0441).

`.agent/f083_inventory.md` is NOT an authored slice. It is the worker's own
prose, written from the worker's own measurements, and no byte of it is dictated
here — only the questions it must answer and the form the answers take.

Constraints:
  1. Change set: `.agent/authored/f083-r2.md`, `.agent/last_block.md`,
     `.agent/live_review.md`, `.agent/f083_inventory.md`, `.agent/decisions.md`,
     `.agent/context.md`, `.agent/plan.md`, `.agent/handoff.md`. Nothing else.
     `packages/`, `apps/`, `scripts/`, `tests/` and `docs/` all stay EMPTY in the
     range diff — this round writes no code, no test and no doc. Gate 9 measures
     that as a restriction.
  2. Apply every slice BYTE-VERBATIM. A defect in my text is a declared deviation
     in the handback, never a silent repair. No slice contains an instruction
     addressed to you about the file it lands in (R-0450).
  3. C1 lands BEFORE C2. Push after C3. Create NO pull request — F083's PR is
     created at closure, not before.
  4. This round adds NO worktree. `git worktree list` is one line throughout.
  5. MEASURE, NEVER ESTIMATE. Every number in the inventory is produced by a
     command you ran in this round, and the inventory records the command next to
     the number. A number you did not measure is written as `not-measured`.
  6. A RED STAGE IS DATA, NOT A BLOCKER — DECISION F083 D1, ruled in this block
     and appended to `.agent/decisions.md` as DEC-D1. If a stage run reports
     failures, record the real exit code, the real counts and the failing node
     ids in the inventory and CONTINUE the round. Rationale: this round's product
     is a description of the repository as it is, and detecting a red main is
     this feature's own job (R-0205, carried into F083 by its feature file). This
     exception is scoped to the stage-runtime measurement in THIS round and to
     nothing else; every gate below still fails the round when it is red.

--- BEGIN SLICE GATE-R1-BLOCK --- (APPEND to .agent/live_review.md, C1, with exactly one blank line between the file's current last line and the first line of this slice)
Gate: R1 — PASS. Verification tier: the docs gate, the two live-state readers and the canary, all four re-run by the reviewer at the round's head; no full-suite claim is made or needed, because this round changed no code and no test. All twelve ordered gates reproduce against the committed tree. TRANSPORT held: scratchpad, `.agent/authored/f083-r1.md` and `.agent/last_block.md` are all sha256 df5447bb084a6874d2d2c59916f026c8366c07b0f984e3eba06e81be2c42b902, 24035 bytes, 313 lines, byte-equal, and the declared footer 313 equals the measured 313. C1 is the round's structurally interesting proof and it is the shape worth reusing: the reset was not reviewed by reading it but RECONSTRUCTED — the reviewer extracted LIVEREVIEW-HEAD from the committed authored file by its markers, rebuilt the carried set out of the BASE record by the block's own rule, applied the byte formula and got equality with the committed file, so the carry is proven mechanically rather than trusted. 75 paragraphs carried, none retyped; the rebuilt record measures 78 registered, 0 resolved, 0 `Landed:`, 0 `Gate:`, max R-0450, next free R-0451, no duplicate id. The formula itself was validated BEFORE emission against commit e978262b, the F082 reset, where it reproduced that file byte-for-byte over its 33 paragraphs — an ordered rule checked against the corpus it would run on, which is R-0446's standing rule holding for the first time in the round after it was written. The three whole-file slices byte-equal their sources, `.agent/plan.md` at 40 lines with `## Goal` and `## Next Steps` present and no `- [ ]` line to trip `plan_consistency`. The STATUS pair is 1/0/1 with `FROM in TO` False and the composite True; at HEAD the unclaimed F083 line is gone, exactly one `[~]` line exists in the whole ledger, and the 49 `[x]` lines are unchanged. `tests/docs/` 295 passed, `tests/regression/test_resource_safety.py` 21 passed, `tests/orchestration/test_integrity_gate.py` 15 passed and the canary 42 passed, every one exit 0 and every one equal to the value the reviewer measured at BASE before ordering it (R-0364). The integrity gate passes all five checks, `fail_count` 0, with `live_review_verdict` now quoting the F083 record and `plan_consistency` reporting `context_complete=False`. The change set is 8 paths, EMPTY under `packages/`, `apps/`, `scripts/` and `tests/`, and exactly one file under `docs/`. Insertions 313 · 260 · 28 · 65 · 119, none over 500. No PR was created, as ordered. TWO findings are registered below and both are defects of the reviewer's own block text; the worker declared both, with the disk evidence, before the reviewer read the diff, which is the seventh consecutive round.

- R-0451 — Low, A BLOCK ASSERTED THAT ITS OWN SLICE SAID SOMETHING THE SLICE DOES NOT SAY, SO A DOCUMENTED DROP WENT UNDOCUMENTED. Found by the WORKER while executing the R1 carry. The R1 block's prose reads "`Gate:`, `Done:` and `Landed:` lines are NOT carried, and the head slice says so in prose, so nothing is silently dropped" — but LIVEREVIEW-HEAD, the slice that actually lands on disk, names ONLY the four `Landed:` lines. The reviewer confirmed the arithmetic at the BASE record: it held 22 `^Gate: ` lines, 2 `^Done: ` lines and 4 `^Landed: ` lines, so 24 lines were dropped that the committed record does not account for, against 4 that it does. Nothing is lost in the strong sense — the pre-reset record is intact in git history at f3fd96d7 and the reconstruction gate proves the carry was exactly the open set — but the reset's own prose is the only place a reader resuming from disk would look, and it under-reports what the reset removed. Low for that reason, and because the drop itself is correct and matches the F082 reset's shape. This is the block-clause family: R-0331 and its successors say two clauses of a block must agree with each other, and this one extends it by one step — a clause that makes a claim ABOUT a slice is checked against the slice's bytes, not against the intent, because only the slice survives the round. Standing rule from here, binding the reviewer: when block prose asserts that an applied slice states something, the pre-emission checklist greps the slice body for it; an unfound assertion is either deleted from the prose or added to the slice before the block is emitted. OPEN.

- R-0452 — Low, THE BLOCK THAT REGISTERED R-0449 BROKE R-0449'S OWN RULE IN THE SAME BREATH. Found by the WORKER, which declared it as its first deviation. R-0449, registered by the R1 block, states the rule "before ordering any value INTO an artifact, name the commit that writes the artifact and the step that produces the value; if the producer is not strictly earlier than the writer, the block orders the value reported in the round's final message and orders the artifact to say so". That same block's gate 12 ordered the push result and the `gh pr list` reading into the handback, and its gate 1 ordered the post-C3 `git status --porcelain` there too — while C3 IS the handback and the push necessarily follows it. The worker reported all three in its final message and said so, which is exactly the accommodation R-0449 prescribes, so nothing false was written; the reviewer independently confirmed the clean tree, the pushed head and the empty PR list after the fact. Low for that reason. The lesson is not that the rule was wrong but that a rule stated as prose inside a finding does not bind the next block, because nothing reads it at emission time: R-0449 and R-0451 both die at the same point, the moment between authoring and emitting where no mechanical check runs. Standing rule from here, binding the reviewer: the §3 pre-emission checklist gains one item that walks every gate in the Done-when list, names the commit or step that produces its value, and rejects any gate whose producer is not strictly earlier than the artifact ordered to carry it. A counter-measure that lives only in a finding paragraph has already failed once by the time it is read. OPEN.
--- END SLICE GATE-R1-BLOCK ---

--- BEGIN SLICE DEC-D1 --- (APPEND to .agent/decisions.md, C2, with exactly one blank line between the file's current last line and the first line of this slice)
## DECISION F083 D1 — a red stage is inventory data, not a round blocker (2026-08-15)

Scope: the stage-runtime measurement of F083 R2, and nothing else.

R2 measures the wall time of each candidate CI stage by running it. If a stage
run reports failures, the worker records the real exit code, the real counts and
the failing node ids in `.agent/f083_inventory.md` and CONTINUES the round,
rather than treating the red as the G8 "any red gate ends the round" case.

Why: this round's product is a DESCRIPTION of the repository as it is. A red
stage is a fact about the repository and therefore part of the description —
suppressing it would make the inventory less true, and stopping on it would make
F083 unable to inventory the very condition it exists to detect. R-0205, carried
into F083 by its own feature file, records that live-state contract tests turn
red for reasons unrelated to the change under review; an inventory that cannot
survive that is an inventory that cannot be taken on this repository.

Limits: this exception covers the stage-runtime measurement only. Every ordered
gate in the R2 block still ends the round when it is red, and no later round
inherits this exception without ruling it again. Reverse this decision by
deleting this section.
--- END SLICE DEC-D1 ---

--- BEGIN SLICE CTX-R2 --- (in .agent/context.md, C2 — REWRITE pair, FROM and TO disjoint)
In: Remedy's own CI as one entrypoint plus thin hosted wrappers. Nothing is built
yet — this round only opens the record. The feature file T2_F083.md sets the
--- BEGIN SLICE CTX-R2-TO --- (C2)
In: Remedy's own CI as one entrypoint plus thin hosted wrappers. No stage runner
exists yet; R2 inventoried the marker landscape the stages select over and
`.agent/f083_inventory.md` is that record. The feature file T2_F083.md sets the
--- END SLICE CTX-R2-TO ---

--- BEGIN SLICE PLAN --- (WHOLE FILE replacement of .agent/plan.md, C2)
# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0453. Open findings: eighty — the seventy-five
carried out of the F082 record, plus R-0448 to R-0452 registered on this branch.
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
R2 is the T001 MARKER INVENTORY: it records the R1 PASS, registers R-0451 and
R-0452, rules DECISION F083 D1, and writes `.agent/f083_inventory.md` — which
markers exist and who assigns them, the collected count per marker, whether the
candidate stage selections cover the suite without overlapping, the measured
wall time per stage, and what the repository already provides that the stage
runner must reuse rather than copy. It builds no stage runner.

## Next Steps
1. R3 builds T001 — the stage runner, the marker selections and the summary
   table — over the shape R2's inventory settles, and no earlier.
2. The stage split is chosen from R2's measured data, not from the feature
   file's suggested shape, wherever the two disagree.

## Risks
- The feature file names a `live-provider` marker; the reviewer's own grep of
  `pyproject.toml` found the live-provider role carried by `real_ollama` and no
  marker of that name. R2 settles the naming in writing before R3 depends on it.
- Five of the six findings registered on this branch are defects in the
  reviewer's own block text, and R-0452 records that a counter-measure written
  as finding prose does not bind the next block. Whether the pre-emission
  checklist change holds is measurable only in later rounds.
- Measuring stage wall time means running most of the suite. DECISION F083 D1
  rules that a red stage is data for the inventory rather than a round blocker,
  so the round can complete over a repository that is red for unrelated reasons.
--- END SLICE PLAN ---

THE INVENTORY — `.agent/f083_inventory.md`, new file, your own prose. Answer
every question below with a MEASURED value and, where the question asks for one,
a file-and-symbol citation. Record the exact command next to each number. Where a
question has no answer, write the absence and the command that proves it — a
repository-wide absence is asserted only from a grep you ran (R-0419, DECISION
F082 D7).

 Q1. Which test markers exist, and who assigns them? Give the declaration site
     and every declared marker with its description. Then split them: which are
     assigned AUTOMATICALLY at collection, and by which function, versus which
     reach a test only through an explicit decorator. Cite file and symbol.
 Q2. The collected count for each marker declared in Q1, and the total collected
     count for the whole suite, each with the command that produced it.
 Q3. The feature file `docs/roadmap/features/T2_F083.md` names its markers as
     "integration, subprocess, ui-contract, live-provider, smoke". For EACH of
     those five names, state whether a marker of that name exists on disk, and
     where. Name the marker that actually carries the live-provider role. This
     question exists because the feature file and the code may disagree; if they
     do, the inventory records the disagreement rather than resolving it silently.
 Q4. Take these five candidate stage selections verbatim:
       fast          not integration and not subprocess and not real_ollama and not ui_contract and not smoke and not slow
       standard      (integration or subprocess) and not real_ollama
       ui            ui_contract and not real_ollama
       smoke         smoke and not real_ollama
       excluded      real_ollama
     Report each one's collected count. Then answer two questions mechanically,
     over collected NODE IDS and not over counts: do the five COVER the suite
     (report the union size and the list of uncovered node ids), and are they
     DISJOINT (report every pairwise overlap with its size and its node ids)?
 Q5. The measured wall time and outcome of each stage. Run fast, ui, smoke,
     safety and architecture serially; run standard with `-n auto`. For each,
     record the exact command, the real exit code, collected/passed/failed/
     skipped and the duration. Do NOT run the excluded stage: record that it was
     not run, why, and the exact command an operator would use to run it. If a
     stage is red, DECISION F083 D1 applies — record it and continue.
 Q6. Does a `ci` command already exist anywhere under `apps/`, `packages/`,
     `scripts/` or `tests/`? Answer from a grep you ran and quote the command.
 Q7. Do hosted workflow files exist? Give the path you checked and what you found.
 Q8. What does the repository ALREADY provide that a stage runner must reuse
     rather than reimplement — the module that runs pytest as a subprocess today,
     the CLI command-registration seam a new `ci` command would attach to, and
     the parallel-execution plugin with its version. Cite file and symbol for
     each, and name anything you looked for and did not find.

Close the inventory with a short OPEN QUESTIONS section: what R3 cannot decide
from this data. Do not answer them and do not design the stage runner here.

Done when — run every gate and record its REAL value; a gate you cannot run is
reported as not run, never as green:

 1. `git status --porcelain` EMPTY before the first commit and before C3.
    `git worktree list` ONE line throughout. `.agent/STOP` ABSENT at round start
    and again at handback (R-0347).
 2. BASE: `git rev-parse HEAD` before the first commit; report it and whether it
    equals 928120ab.
 3. TRANSPORT, bytes read in Python: report sha256, byte count and line count of
    `.remedy-wt/.cache/f083-r2/f083-r2.md`, `.agent/authored/f083-r2.md` and
    `.agent/last_block.md`, whether all three byte strings are EQUAL, and whether
    the measured line count equals this block's declared footer count.
 4. C1 PREFIX PROPERTY over `<C1>^..<C1>`: `pre` is a prefix of `post`, and
    `post[len(pre):]` equals `b"\n" + GATE-R1-BLOCK` byte-for-byte, the slice
    extracted from the COMMITTED `.agent/authored/f083-r2.md` by its markers.
    Report the numstat and confirm its deletion column is 0.
 5. C2 APPLIED TEXT, each proven against the slice extracted from the committed
    authored file: (a) `.agent/decisions.md` — `pre` is a prefix of `post` and
    `post[len(pre):]` equals `b"\n" + DEC-D1`; (b) `.agent/context.md` — report
    the FROM count in `pre`, the FROM count in `post`, the TO count in `post`,
    `FROM in TO`, and `pre.replace(FROM,TO) == post`; (c) `.agent/plan.md` byte-
    equals PLAN as a whole file — report sha256 and line count, under 50, with
    `## Goal` and `## Next Steps` present and no `- [ ]` line.
 6. THE INVENTORY EXISTS AND ANSWERS EVERY QUESTION: report `.agent/
    f083_inventory.md`'s line count, and for each of Q1 to Q8 the answer's
    one-line summary. Report the count of questions answered and the count asked.
 7. THE INVENTORY'S ARITHMETIC IS INTERNALLY CONSISTENT, re-derived by you at
    HEAD rather than restated from Q4: report the union size of the five stage
    selections, the uncovered count, and every pairwise overlap with its size.
    The reviewer measured this at emission and will compare; report what you
    MEASURE, and if it differs say so rather than reconciling it.
 8. VERIFICATION, each command run separately with its exit code read from the
    process, never from a pipe (R-0438). Report collected count and real exit
    code for EACH: `python3 -m pytest tests/docs/ -q`, which the reviewer
    measured at 295 collected, 295 passed, exit 0 at BASE; `python3 -m pytest
    tests/regression/test_resource_safety.py -q`, 21 passed, exit 0 at BASE;
    `python3 -m pytest tests/orchestration/test_integrity_gate.py -q`, 15 passed,
    exit 0 at BASE; and the canary `python3 -m pytest
    tests/cli/test_golden_path.py -q`, 42 collected, 42 passed, exit 0 at BASE.
    These four are gates and DECISION F083 D1 does NOT cover them: a red one ends
    the round.
 9. CHANGE SET, measured BEFORE the handoff is written into C3, so it lists seven
    paths and `.agent/handoff.md` is the eighth and last:
    `git diff --name-only 928120ab..HEAD`. Report the full list and its count.
    Restricted to `packages/`, `apps/`, `scripts/`, `tests/` and `docs/` it must
    be EMPTY. Report that restriction as a measured list.
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
above, the item-status table covering every C-item, every gate and every
inventory question, open findings with max and next free id, and the next
expected action. C3 cannot table its own SHA (R-0371, R-0149); say so rather than
inventing one. Repeat this line verbatim as the Fortschritt line:

Fortschritt: 5 % (F083 beansprucht · R1 PASS · R-0451 und R-0452 registriert · T001-Marker-Inventar gemessen und geschrieben · noch kein Stage-Runner, kein Code) — gemessen, nicht geschätzt

If any gate is RED, or anything here contradicts what you find on disk: finish
the commit you are in, write the handoff naming the exact blocker, and end. Do
not widen scope to route around it (G8). DECISION F083 D1 is the single scoped
exception and it covers Q5's stage runs only.

BLOCK SIZE, measured on these final bytes: 277 lines (cap 400, DECISION F105 D5).
──────────────────────────────────────────────────────────────────────────────
