── STEP R13/15 — F083 CI self-check — RECORD R12 PASS, REGISTER R-0474, MEASURE THE SERIAL COST OF `remedy ci` ──

Goal:
  Record the R12 PASS, register the one finding its review produced, and then
  measure what `remedy ci` ACTUALLY costs today: three samples per CI stage,
  taken through the production instrument, at the timeout the runner really
  defaults to. R-0473 binds this round to at least three samples before any
  ceiling is written, so this round takes the samples and writes NO ceiling, NO
  budget number, NO stage and NO production code. The budget stage, the
  determinism stage and the ruling on R-0468 are written in R14 from this data.

WHY SERIAL, AND NOT `-n auto`. `pytest_argv_for_stage` in
`packages/orchestration/ci_stages.py` returns `["-m", <expression>, "-q"]`, and
`stage_command` in `packages/orchestration/ci_run.py` wraps it as
`[sys.executable, <repo_root>/scripts/remedy_pytest_runner.py, "--", *argv]`.
There is no `-n auto` anywhere on that path. Every `-n auto` reading in
`## Q9` therefore measures something `remedy ci` does not do, and `## Q9`
records a SERIAL wall time for exactly one stage — `fast`, 391.9 s — and `not
measured` for `standard`, `ui` and `smoke`. A budget written from Q9 would be a
budget for a command that does not exist. This round takes the readings that
describe the real one.

THE QUESTION THIS ROUND SETTLES BY MEASUREMENT, NOT BY ARGUMENT.
`scripts/remedy_pytest_runner.py` reads `REMEDY_PYTEST_TIMEOUT_SEC` and defaults
it to 600, and returns 124 when it kills the run — the value `ci_run.py` names
`PYTEST_TIMEOUT_EXIT_CODE`. The `standard` stage collects 12579 items and has
never been run serially. Whether today's `remedy ci` completes that stage or
truncates it at 600 seconds is UNKNOWN, and it is the single most consequential
number for the budget. Measure it. Do not predict it. A 124 is not a failure of
this round — it is a reading this round earned, and you record it as one.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f083-r13.md`
  C0b  mirror it byte-identically into `.agent/last_block.md`
  C1   `.agent/live_review.md` — RECORD-R12 appended at EOF, ONE commit, one
       body: the gate line, a blank line, the one finding.
  C2   `.agent/f083_inventory.md` — the `## Q10` section appended, ONE commit.
       You write its BODY from YOUR OWN measurements; the contract below fixes
       its first line, its required content and its honesty rules, nothing else.
  C3   `.agent/plan.md` (PLAN, whole file), ONE commit.
  C4   `.agent/handoff.md`, the handback, alone.

BASE: 6af03d95. Re-derive `git rev-parse HEAD` before the first commit and report
whether it equals 6af03d95. If it does NOT, stop and hand off.

BLOCK SIZE. This block declares NO line count of its own — the reviewer that
wrote it has no scratchpad file and cannot mechanically count its own final
bytes, and the standing rule from R-0470 is count it or state no numeral. Gate 3
asks YOU to measure the count and check it against the 400-line cap
(DECISION F105 D5). A block over the cap is a finding against the reviewer that
you DECLARE, not a defect you repair.

SLICE CONVENTION (R-0437): every slice body below is the lines between its
markers INCLUDING the trailing newline of its last line, and every shape is
declared under that convention. The authored units are, listed and NOT counted:
RECORD-R12, PLAN.

APPEND CONVENTION, one statement governing both appends so no two clauses can
disagree (R-0471): `.agent/live_review.md` and `.agent/f083_inventory.md` BOTH
already end with a newline. An append writes exactly ONE newline and then the
appended text, which puts exactly one blank line between the file's current last
line and the appended text's first line. Every append gate below reads
`post[len(pre):]` and expects it to BEGIN with exactly one `\n`. There is no
other reading in this block.

SHAPES, stated at authoring time (§4.9):
  · RECORD-R12 is an APPEND to `.agent/live_review.md`, proved by the prefix
    property in gate 4 with the tail byte-equal to `b"\n" + RECORD-R12`.
  · The `## Q10` section is an APPEND to `.agent/f083_inventory.md` whose body
    you author from measurements, so gate 5 proves the prefix property and the
    section's FIRST LINE only — a byte-equality gate is impossible here by
    construction and none is ordered.
  · PLAN is a WHOLE FILE, proved by byte equality in gate 10.

Constraints:
  1. Change set, exactly: `.agent/authored/f083-r13.md`, `.agent/last_block.md`,
     `.agent/live_review.md`, `.agent/f083_inventory.md`, `.agent/plan.md`,
     `.agent/handoff.md`. Nothing else. `packages/`, `apps/`, `tests/`,
     `scripts/` and `docs/` stay EMPTY in the range diff — this round writes no
     code and no test.
  2. Apply every slice BYTE-VERBATIM. A defect in reviewer text is a declared
     deviation, never a silent repair.
  3. Commit strictly in the C-order above. Push after C4. Create NO pull request.
  4. This round adds NO git worktree and performs NO mutation. It DOES perform
     timing runs; they are read-only test executions in the primary checkout and
     they leave the tree clean, which gate 1 re-checks before C4.
  5. `## Q10` does NOT touch any existing section. `## Q5` and `## Q9` are
     unchanged, and no existing heading is renumbered.

MEASUREMENT CONTRACT — how every number in `## Q10` is taken:
  · The instrument is the PRODUCTION code, imported, never retyped:
        from packages.orchestration.ci_stages import CI_STAGES, CiStage
        from packages.orchestration.ci_run import run_ci_stage, stage_command
    Marker expressions are READ from `CI_STAGES`. `run_ci_stage(stage,
    repo_root)` returns `StageResult(stage, ran, exit_code, duration_s, note)`;
    its `exit_code` is the one that process returned (R-0438) and `duration_s`
    is `time.monotonic()` around the call. Report
    `stage_command(stage, repo_root)` verbatim for one stage so the argv is on
    the record.
  · The driver runs from the repository root and passes the repository root as
    `repo_root`. Every sample is its own process.
  · RED CONTROL, run FIRST and recorded in `## Q10`: build
    `CiStage(name="bogus", description="red control",
    marker_expression="no_such_marker_at_all", runs_in_ci=True,
    manual_command="")` and call `run_ci_stage` on it. Report its `exit_code`.
    If it is not 5, the instrument cannot tell an empty selection from a green
    one, every timing below is decoration, and you STOP and hand off.
  · SAMPLES: for each stage in `CI_STAGES` whose `runs_in_ci` is True — `fast`,
    `standard`, `ui`, `smoke` — THREE samples, run one after another, with NO
    environment override, i.e. at the runner's own 600-second default. Record
    every sample's `exit_code` and `duration_s` SEPARATELY. Never average a
    sample away; the spread is the whole point of the round.
  · UNCAPPED PROBE: for each stage whose three samples include an `exit_code` of
    124, run ONE further sample with `REMEDY_PYTEST_TIMEOUT_SEC` set to `5400`
    in the environment, and record it in its own row, labelled as the uncapped
    probe and naming the value you set. This is the ONLY run in the round that
    overrides the default, and `## Q10` says so on its face. If no stage returns
    124, write that no uncapped probe was needed and run none.
  · CONTEXT, measured and not recalled: `os.cpu_count()`; the output of
    `python3 -m pytest --version`; and the ruff baseline from
    `python3 -m ruff check .` run from the repository root with the repository's
    own `pyproject.toml` (which sets `select = ["E", "F", "W", "I", "UP"]` and
    `line-length = 120`) — report its error count and its exit code. That count
    is the baseline R-0468 needs recorded BEFORE any lint ceiling can be
    written, and recording it is the whole of what this round does about R-0468.
  · The `excluded` stage has `runs_in_ci` False, so `run_ci_stage` returns
    `ran=False` without running anything. Record it as not run, with the
    `manual_command` the stage table carries.

`## Q10` CONTRACT — the appended section:
  · Its first line is exactly:
    ## Q10 — Serial stage cost through the production runner, measured at R13
  · It contains, in this order: an instrument paragraph naming the two modules,
    the function, the verbatim argv and the red control's exit code; a
    PER-SAMPLE table with one row per SAMPLE and never one row per stage —
    columns stage, sample, wall seconds, exit code, and pytest's own final
    summary line verbatim; the uncapped-probe rows if any, labelled; one spread
    line per stage giving its min, its max and max-minus-min in seconds; the
    context readings; and a closing sentence stating that the section carries no
    ceiling and no budget number.
  · Honesty rules, binding: a stage you did not run is `not run` with the
    reason, never a blank and never an estimate. A number you did not measure is
    `not measured`. No recommendation, no ceiling and no budget number appears
    anywhere in `## Q10` — choosing them is R14's work, and evidence stays
    separate from the decision it informs, exactly as `## Q9` did.

--- BEGIN SLICE RECORD-R12 --- (APPEND to .agent/live_review.md, C1. The blank line INSIDE this slice, between the gate line and the finding, is part of it.)
Gate: R12 — PASS. The reviewer re-ran all fifteen gates itself at the round's head from the repository root and all fifteen reproduce. TRANSPORT: `.agent/authored/f083-r12.md` and `.agent/last_block.md` are byte-equal at sha256 3821ad67c09d over 21247 bytes and 200 lines, each equal to its committed blob at C0a and C0b, and 200 is at and under the 400-line cap. C1's prefix property holds with the tail byte-equal to `b"\n" + RECORD-R11` extracted from the COMMITTED authored file by its markers, numstat `8 0`. C2's REWRITE pair measures FROM 1x before and 0x after, TO 0x before and 1x after, numstat `1 1`; the file's `^## Q\d` headings now read Q1 through Q9, each exactly once, and the two body sentences citing Q5 still count 1 each. C3's `.agent/plan.md` byte-equals its PLAN slice at sha256 fc8565d17cd3, 32 lines, `## Goal` and `## Next Steps` present, 0 `- [ ]` lines. The scoped range diff over `packages/`, `apps/`, `tests/` and `docs/` printed nothing from the repository root, so a round that promised no code delivered none. Every gate ran as its own process with the exit code read from that process: the four CI suites at 7, 9, 6 and 8 passed and the verification quartet at 70, 21, 15 and 42 passed, all exit 0; the integrity gate reports passed true, fail_count 0, check_count 5, handlers=338; the open set recomputes to 101 registered, 6 `Done:`, 0 `Landed:`, 95 open, max R-0473, next free R-0474, no duplicate id. Insertions 200, 117, 8, 1, 15 and 114, none over 500. The REPAIR was checked as a repair and not merely as a diff: the two sentences citing "Q5" sit in `## Q8` and in `## OPEN QUESTIONS`, both predate the R11 append, and the original `## Q5` does record that only `standard` used `-n auto` and does time `safety` and `architecture` as separate rows — so the rename restores their true referent rather than merely deleting a duplicate heading. The findings were checked against their subjects rather than read: R11's authored block measures 241 lines at 22819 bytes against the "246 lines" its own footer declares, so R-0470 holds; that block's C2 contract says "exactly one blank line" while its own gate 10 orders a tail of `b"\n\n## Q5 — …"`, so R-0471 holds; it ordered `## Q5 — Stage runtime, measured at R11` into a file already carrying `## Q5 — Measured wall time and outcome per stage` and already running to Q8, so R-0472 holds and C2 resolves it; and `## Q9` does record one wall-clock reading each for `standard`, `ui` and `smoke` and two for `fast`, with `standard` at 138.8 s and the summary `12578 passed, 1 skipped`, so R-0473's data holds. The worker's conduct was correct throughout: every slice applied byte-verbatim, the handback's 150 lines declared against BOTH caps with the mandated content named as the cause, and no `Done:` paragraph of its own. One defect remains and it belongs to the reviewer, registered below.

- R-0474 — Medium, A FINDING'S EVIDENCE POINTER WAS INVALIDATED BY ITS OWN BLOCK, IN THE SAME ROUND THAT WROTE IT. R12's C1 wrote R-0473 into this file with three present-tense citations of `Q5` — "Q5 records exactly one wall-clock reading for each of `standard`, `ui` and `smoke`, and two for `fast`", "the 138.8 s Q5 records", and "Q5 is not wrong" — every one of them meaning the section R11 had appended. C2 of that same block then renamed that section to `## Q9 —`, so by the end of the round all three pointers resolve to `## Q5 — Measured wall time and outcome per stage`, a different section with different numbers: it carries one reading for each of SIX stages, it puts `standard` at 134.1 s rather than 138.8 s, and it holds no second `fast` reading at all. The measured CONTENT of R-0473 is correct and was verified against `## Q9` at this gate, so nothing is fabricated and no number is wrong; what broke is the address, not the data. Medium because R-0473 is the finding that BINDS the next round, and a binding instruction naming the wrong evidence section sends the round that must obey it to the wrong table — the same consequence R-0472 was rated Medium for, with the arrow reversed: R-0472 was a heading prescribed for a file the reviewer had not read, and this is a citation left pointing at a heading the same block moved. The block was aware of the rename everywhere else — its constraint 5 reasons explicitly about which references the rename disambiguates, and the PLAN slice it applied at C3 already reads "from the `## Q9` readings" — so the omission is confined to the finding text, which makes it an emission-sweep failure rather than a misunderstanding. R-0473's text is deliberately NOT edited to close this gap: R-0470 established one round ago that closing the distance between a claim and the bytes by editing the bytes is how a record stops being one, and that principle does not weaken when the stale half is the reviewer's own. The correction lives here instead, in the finding that reports it, and it is stated once and plainly: every `Q5` in R-0473 means the section now titled `## Q9 — Stage runtime, measured at R11`. Refinement, binding the reviewer: when one block both WRITES a citation and MOVES its referent, the citation is authored in the POST-move form, and the block's pre-emission sweep re-reads every heading, section number and quoted name that any later slice of the SAME block rewrites — the sweep §3 item 9 already performs for `file:line` citations, widened to the section names this repository actually navigates by. OPEN.
--- END SLICE RECORD-R12 ---

--- BEGIN SLICE PLAN --- (WHOLE FILE replacement of .agent/plan.md, C3)
# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0475. Open findings: the seventy-five carried out
of the F082 record plus R-0448 to R-0474 registered on this branch, of which
R-0456 to R-0459, R-0467 and R-0472 are resolved. `.agent/live_review.md` is the
source of truth.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R13 records the R12 PASS, registers R-0474, and measures the SERIAL cost of every
CI stage three times through the production `run_ci_stage` instrument, because
`remedy ci` passes no `-n auto` and every reading in `## Q9` therefore describes a
run the command does not perform. It writes no ceiling and no production code.

## Next Steps
1. R14 writes the budget and determinism stages from the `## Q10` samples, never
   from the `-n auto` readings in `## Q9`. R-0473 binds the ceiling to the
   observed spread with its headroom stated, or to a budget that says on its face
   how many samples it rests on. R14 also rules on R-0468 from the ruff baseline
   `## Q10` records, and settles the determinism stage's shape as a DECISION.

## Risks
- The determinism suite is already wholly inside `standard` — 850 ids, 0 outside,
  measured at R11 — so a determinism stage would duplicate work unless
  `standard`'s expression is narrowed in the same change.
- `scripts/remedy_pytest_runner.py` defaults `REMEDY_PYTEST_TIMEOUT_SEC` to 600
  and returns 124 on a kill. `standard` collects 12579 items and has never been
  run serially, so today's `remedy ci` may already truncate its largest stage.
  R13 measures it; until then the outcome is unknown, not assumed.
- 26 ruff errors stand repo-wide (R-0468) and no stage lints. A lint ceiling
  arrives red unless the baseline is recorded first, which `## Q10` does.
--- END SLICE PLAN ---

Done when — run every gate, record its REAL value; a gate you cannot run is reported as not run, never as green:

 1. `pwd` printed FIRST and equal to the repository root. `git status --porcelain`
    EMPTY before the first commit and before C4. `git worktree list` ONE line at
    round start and at handback. `.agent/STOP` ABSENT at both (R-0347).
 2. BASE: `git rev-parse HEAD` before the first commit; report it and whether it
    equals 6af03d95.
 3. TRANSPORT AND SIZE, bytes read in Python: sha256, byte count and line count of
    `.agent/authored/f083-r13.md` and `.agent/last_block.md`; whether the two are
    EQUAL. Report the measured line count and whether it is at or under the
    400-line cap. This block declares no count of its own; yours is the only
    measurement, so report it as a value and not as a comparison.
 4. C1 PREFIX PROPERTY over `<C1>^..<C1>`: `pre` prefixes `post`, and
    `post[len(pre):]` equals `b"\n" + RECORD-R12`, that slice extracted from the
    COMMITTED `.agent/authored/f083-r13.md` by its markers. Report the numstat;
    its deletion column must be 0.
 5. C2 PREFIX AND FIRST LINE over `<C2>^..<C2>`: `pre` prefixes `post`, and
    `post[len(pre):]` BEGINS with exactly
    `b"\n## Q10 — Serial stage cost through the production runner, measured at R13\n"`.
    Report the numstat; its deletion column must be 0. No byte-equality is
    ordered for this slice and none is possible — you authored its body.
 6. C2 STRUCTURE, at C2, over `.agent/f083_inventory.md`: report the count of
    lines matching `^## Q\d` and the full ORDERED list of those heading lines.
    The sequence must read Q1 through Q10 with no number repeated, and the lines
    `## Q5 — Measured wall time and outcome per stage` and
    `## Q9 — Stage runtime, measured at R11` must each still count exactly 1.
 7. C2 CONTENT: report, from the committed `## Q10`, the number of SAMPLE rows
    and how many belong to each of `fast`, `standard`, `ui` and `smoke`; the red
    control's exit code; every sample's exit code; how many uncapped probes you
    ran and why; and the counts of the strings `not measured` and `not run` you
    wrote. State plainly whether `## Q10` contains any ceiling, budget number or
    recommendation — it must contain none, and this is your declaration, not a
    count.
 8. GATE — THE CI SUITES ARE UNDISTURBED, each its own process, REAL exit code
    from the process (R-0438), each via `python3 -m pytest <path> -q`:
    `tests/orchestration/test_ci_stages.py` [7, 0];
    `tests/orchestration/test_ci_stage_selection.py` [9, 0];
    `tests/cli/test_ci_cmd.py` [6, 0]; `tests/orchestration/test_ci_run.py` [8, 0].
 9. GATE — VERIFICATION, each run separately, REAL exit code from the process:
    `tests/ui_server/test_dashboard_contract.py` [70, 0];
    `tests/regression/test_resource_safety.py` [21, 0];
    `tests/orchestration/test_integrity_gate.py` [15, 0]; canary
    `tests/cli/test_golden_path.py` [42, 0].
10. C3 PLAN byte-equals the PLAN slice as a whole file — report sha256, line count
    (under 50), `## Goal` and `## Next Steps` present, no `- [ ]` line, and the
    count of numbered items under `## Next Steps`.
11. GATE — NOTHING ELSE MOVED: `git diff --name-only 6af03d95..HEAD -- packages/
    apps/ tests/ scripts/ docs/` must print NOTHING. Report it as a measured
    list, and confirm you ran it from the repository root — at the wrong root it
    is vacuous.
12. GATE — INTEGRITY, in Python because the `remedy` CLI is denied here (R-0408):
    `python3 -c "from packages.orchestration.integrity_gate import
    run_integrity_checks, export_integrity_json; import json;
    print(json.dumps(export_integrity_json(run_integrity_checks())))"` — report
    `passed`, `fail_count`, `check_count`, every check's status, and the
    `handler_import` message [BASE: handlers=338; this round adds no handler].
13. GATE — OPEN SET at HEAD: count `^- R-\d+ — ` paragraphs, `^Done: R-\d+ — `
    and `^Landed: R-\d+ — ` lines; report all three, registered-minus-done, max
    id, next free id, any duplicate. Reviewer measured 101 / 6 / 0, open 95, max
    R-0473 at BASE and expects 102 / 6 / 0, open 96, max R-0474, next free
    R-0475. Report what you MEASURE.
14. CHANGE SET at C3 — FIVE paths, `.agent/handoff.md` being written by C4 and so
    absent from any measurement preceding it: `git diff --name-only
    6af03d95..HEAD`. Report the list and count; name `.agent/handoff.md` the
    sixth path C4 adds.
15. Insertions (`+` column only) for C0a through C3 — report each; none over 500.
    C0b is a verbatim single-`.agent/`-file rewrite, AGENTS.md-exempt; report it
    anyway. C4's own count cannot exist inside C4 (R-0149): final message.

The push result, post-C4 clean-tree reading and open-PR list postdate C3, so per
R-0449 and R-0452 they are NOT ordered into that file: run `git push -u origin
feature/f083-ci-self-check` after C4, create no PR, report all three in the final
message.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md, as C4
— feature and round, branch, per-commit changed-files tables, every gate value
above, the item-status table covering every C-item and every gate, open findings
with max and next free id, and next action R14 as the plan states it. C4 cannot
table its own SHA (R-0371, R-0149); say so. Over a cap, name BOTH caps (R-0462).
Fortschritt, verbatim:

Fortschritt: 45 % (F083 beansprucht · R1 bis R7 und R9 bis R12 PASS, R8 FAIL auf einem roten ruff-Gate und in R9 repariert · Stage-Tabelle, Stage-Runner, die `remedy ci` CLI-Naht und die Selektionstests samt Live-Wächter als Code gelandet · R13 misst zum ersten Mal, was `remedy ci` seriell wirklich kostet, denn jede bisherige `-n auto`-Messung beschreibt einen Lauf, den das Kommando gar nicht ausführt · noch keine Determinismus- oder Budget-Stage, kein Ceiling, keine hosted workflows) — Rundenzahl gemessen, Prozentwert geschätzt

If a GATE is RED, or anything here contradicts what you find on disk: finish the
commit you are in, write the handoff naming the exact blocker, end. Do not widen
scope to route around it (G8).
──────────────────────────────────────────────────────────────────────────────
