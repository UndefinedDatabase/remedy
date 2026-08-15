── STEP R11/15 — F083 CI self-check — RECORD R10 PASS, MEASURE EVERY STAGE'S RUNTIME, REGISTER R-0468 AND R-0469 ──

Goal:
  Replace the plan's last remaining guess with data. `.agent/plan.md` states the
  risk in its own words: `fast` rests on a single 391.8 s reading and is inverted
  with respect to cost, so no runtime budget can be written from measured data.
  This round MEASURES every stage — serially and under `-n auto` — records the
  readings in the inventory, and registers the two findings the R10 review turned
  up. It lands NO stage and NO production code on purpose: the budget stage T002
  asks for is written FROM these numbers in R12, never before them.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f083-r11.md`
  C0b  mirror it byte-identically into `.agent/last_block.md`
  C1   `.agent/live_review.md` — RECORD-R10 appended at EOF, ONE commit, one body:
       gate line, blank line, then the two findings.
  C2   `.agent/f083_inventory.md` — the Q5 measurement section appended at EOF,
       ONE commit. Its NUMBERS ARE YOURS, not mine: see the C2 contract below.
  C3   `.agent/plan.md` (PLAN, whole file), ONE commit.
  C4   `.agent/handoff.md`, the handback, alone.

BASE: c6db29fa. Re-derive `git rev-parse HEAD` before the first commit and report
whether it equals c6db29fa. If it does NOT, stop and hand off.

TRANSPORT: this session has no paste relay and therefore no scratchpad file. The
authored original of this block is the byte range your prompt delimits with
`--- BEGIN BLOCK BYTES ---` / `--- END BLOCK BYTES ---`; C0a writes exactly that
range and C0b mirrors it. The proof obligation is unchanged in substance and
reduced in shape: gate 3 proves `.agent/authored/f083-r11.md` and
`.agent/last_block.md` are byte-identical to each other and that the measured
line count equals this block's declared footer, and the reviewer re-reads the
committed file against the text it authored.

SLICE CONVENTION (R-0437): every slice body below is the lines between its
markers INCLUDING the trailing newline of its last line, and every shape is
declared under that convention. The authored units are, listed and NOT counted:
RECORD-R10, PLAN.

SHAPES, stated at authoring time (§4.9): there is no FROM→TO pair in this block.
RECORD-R10 is an APPEND to `.agent/live_review.md` proved by the prefix property
in gate 4. PLAN is a WHOLE FILE proved by byte equality in gate 16. The Q5
section is an APPEND to `.agent/f083_inventory.md` proved by the prefix property
in gate 10 — its heading is prescribed, its numbers are measured.

C2 CONTRACT — WHY THIS ONE SLICE IS NOT AUTHORED. A block may never order a value
that cannot exist at the moment the ordered text is written (R-0371). Every
number in Q5 is produced by gates 5 to 9, which run after this text was written,
so authoring Q5 verbatim would be exactly that defect. You therefore WRITE Q5
yourself, under these binding constraints:
  · It is APPENDED at EOF of `.agent/f083_inventory.md` with exactly one blank
    line between the file's current last line and its first line.
  · Its first line is exactly: `## Q5 — Stage runtime, measured at R11`
  · Every number in it is a value one of gates 5 to 9 actually printed. You may
    not round, extrapolate, average, or carry a number over from Q4 or from any
    earlier reading. A measurement you did not take is written as `not measured`.
  · It states, for each of the five stages: collected count, wall-clock seconds
    for each run you performed, the pass/fail tallies, and the REAL exit code.
  · It states the machine's CPU count (`python3 -c "import os; print(os.cpu_count())"`)
    beside the `-n auto` readings, because `auto` means nothing without it.
  · It names, in one sentence each, the two facts R12 needs: which stage is the
    long pole, and whether the determinism candidate set of gate 9 is already
    wholly inside `standard`.
  · It carries NO recommendation and NO budget number. Choosing the budget is
    R12's job; this section is evidence, not a decision.

Constraints:
  1. Change set, exactly: `.agent/authored/f083-r11.md`, `.agent/last_block.md`,
     `.agent/live_review.md`, `.agent/f083_inventory.md`, `.agent/plan.md`,
     `.agent/handoff.md`. Nothing else. `packages/`, `apps/`, `tests/` and
     `docs/` stay EMPTY in the range diff — this round writes no code.
  2. Apply RECORD-R10 and PLAN BYTE-VERBATIM. A defect in my text is a declared
     deviation in the handback, never a silent repair.
  3. Commit strictly in the C-order above. Push after C4. Create NO pull request.
  4. This round adds NO git worktree and performs NO mutation. Every measurement
     is a read-only test run in the primary checkout, so `git status --porcelain`
     stays empty throughout except for the files you are committing.
  5. MEASUREMENTS ARE NOT GATES. Gates 5 to 9 record a COLOUR and an exit code as
     data. A red stage there is a RESULT to write down, not a failure to repair
     and not a reason to stop — detecting a red repository is precisely what this
     feature exists to do. Do not fix a red test this round. Gates 11 to 15 ARE
     gates in the ordinary sense: if one of those is red, finish the commit you
     are in, write the handoff naming the exact blocker, and end (G8).
  6. Timing runs use `python3 -m pytest` DIRECTLY and NOT
     `scripts/remedy_pytest_runner.py`. The runner defaults to a 600 s timeout
     (`REMEDY_PYTEST_TIMEOUT_SEC`, runner line 60) and env assignment is denied
     here, so routing a timing run through it would truncate the very reading
     being taken. The reviewer proved at emission that the runner passes these
     arguments through unchanged — `python3 scripts/remedy_pytest_runner.py -- -n
     auto --collect-only -q -m <fast expression>` collected 3975/17045 at exit 0
     — so nothing about the seam is in doubt; only its timeout is unhelpful here.
  7. Measure marker expressions by READING them from the table, never by
     retyping them: import `CI_STAGES` / `ci_stage_by_name` from
     `packages.orchestration.ci_stages` in your measuring script. A retyped
     expression measures a stage that does not exist.

--- BEGIN SLICE RECORD-R10 --- (APPEND to .agent/live_review.md, C1, with exactly one blank line between the file's current last line and the first line of this slice. The blank line INSIDE this slice, between the gate line and the first finding, is part of it.)
Gate: R10 — PASS. All nineteen gates were re-run by the reviewer at the round's head, from the repository root with `pwd` confirmed before every reading, and every value the handback reported was reproduced exactly, with no deviation of any kind found in the worker's execution. TRANSPORT is three-way byte-equal — the scratchpad original at `.remedy-wt/.cache/f083-r10/f083-r10.md`, `.agent/authored/f083-r10.md` and `.agent/last_block.md` all read sha256 ebfb3238fb9e18a3374805ba0adb3e9c2c51d22eb1e88566db69a2285f2d9880 at 31090 bytes and 399 lines, equal to the block's declared footer. All nine authored slices were re-extracted BY MARKER from the committed authored file and every one matched the digest, byte count and line count the handback printed: RECORD-R9 ccd35335 7067 6, TESTFILE fbffda72 6138 131, DOCSTRING-FROM fb339e4e 80 1, DOCSTRING-TO 72c494c0 93 1, OPENER-FROM 4d09ad4c 82 1, OPENER-TO 63b7c487 82 1, ITEM12-FROM f3a49657 76 1, ITEM12-TO 8a530ad2 1618 21, PLAN 0518bf2d 1463 29. The C1 prefix property holds with the tail byte-equal to `b"\n" + RECORD-R9` and a deletion column of 0; the C2 test file byte-equals TESTFILE and carries the declared digest; the DOCSTRING rewrite reads FROM 1x/TO 0x before and FROM 0x/TO 1x after; the ITEM12 append reads FROM 1x before AND after with TO 0x before and 1x after; and all five item-12 numerals agree at C3 as ordered. Every executable gate was run by the reviewer as its own process, and the real exit code was read from that process rather than from a shell: ruff `All checks passed!` at 0, the new selection suite 9 passed at 0, `test_ci_stages.py` 7 passed at 0, `test_ci_cmd.py` 6 passed at 0, the catalog quartet 601 passed at 0 and unmoved from BASE, and the verification quartet 70, 21, 15 and 42 passed at 0 each. The scoped range diff over `packages/`, `apps/` and `docs/roadmap/` printed nothing from the repository root; the integrity gate reports passed true, fail_count 0, check_count 5 and handlers=338; the open set recomputes to 95 registered, 5 `Done:`, 0 `Landed:`, 90 open, max R-0467, next free R-0468, no duplicate id; the change set at C4 is exactly the seven declared paths with `.agent/handoff.md` the eighth added by C5; and no commit's insertion column exceeds 500. Gate 8, the one gate that can only be believed by being reproduced, was reproduced: in a disposable worktree at HEAD — never the primary checkout — a single test marked only `slow` under `tests/cli/` turned the union guard RED at exit 1, naming `tests/cli/test_redproof_slow_only.py::test_case` at `1/17046 tests collected (17045 deselected)`, and the worktree was removed with `git worktree list` back to one line and the primary tree clean. That colour matters more than any green in this record: the guard C2 landed can actually fail, so its passing state is evidence rather than decoration. The worker's arithmetic cross-check is independently confirmed — 17046 = 17036 + 9 + 1 — because the reviewer's own collect at HEAD without the probe reads 17045 tests, which is 17036 + the 9 tests C2 added. The single declared deviation, a 184-line handback against both the AGENTS.md cap and the handback-template cap, is measured as declared at exactly 184 lines, names both caps as DECISION D15 and R-0462 require, drops no mandated section and pads no prose; it is accepted and is not a finding. The two findings below are NOT charges against this round, whose execution was clean throughout — they are conditions of the repository that the reviewer's own spot-check turned up while gating it, and they are registered here because F083 is the feature that owns them.

- R-0468 — Low, THE REPOSITORY THIS FEATURE WILL GATE IS TWENTY-SIX RUFF ERRORS RED, AND NOT ONE CI STAGE RUNS RUFF. Measured by the reviewer at c6db29fa from the repository root, with the repo's own `pyproject.toml` and no substituted flag: `python3 -m ruff check . --statistics` reports 26 errors — 20 I001 unsorted-imports, 4 F401 unused-import, 1 UP035 deprecated-import and 1 F821 undefined-name — of which 25 are auto-fixable. None of them belongs to this branch: `python3 -m ruff check tests/orchestration/test_ci_stage_selection.py tests/orchestration/test_ci_stages.py` prints `All checks passed!` at exit 0, so R10 added no debt and all 26 predate this feature. It is registered against F083 rather than left alone because of the feature's own Acceptance line, "Clean checkout: `remedy ci` green locally and hosted with the same stage results": all five entries in `CI_STAGES` are pytest marker selections and none of them invokes a linter, so `remedy ci` is green today while `ruff check .` is red, and the day T003's hosted workflow adds a lint step it arrives red with 26 errors nobody scheduled. Low and not Medium because no false GREEN exists on disk right now — no stage claims to lint and none does — and because the remedy is bounded and mechanical rather than a redesign. Routed to T002, whose brief already names "no forbidden patterns" as budget-stage work: a lint ceiling belongs to the budget stage, and the choice between clearing the 26 first or landing the stage against a recorded baseline is R12's to make and to record as a DECISION. OPEN.
- R-0469 — Low, A NAME THAT EXISTS NOWHERE IS INTERPOLATED INTO AN ERROR MESSAGE IN PRODUCTION CODE. `check_injections_supported` in `packages/orchestration/gauntlet_injection.py` raises `MissingSeamError(f"{name} cannot be injected at {BLOCKED_INJECTIONS[name]}: " f"{MISSING_SEAM}")`, and `MISSING_SEAM` is defined nowhere at all: `grep -rn "MISSING_SEAM" --include=*.py .` returns exactly one hit in the whole repository and it is that use site. Evaluating that f-string would raise `NameError: name 'MISSING_SEAM' is not defined` instead of the `MissingSeamError` the function exists to raise, so the refusal path fails in a way none of its own tests describe. Low, and the reason is reachability, checked rather than assumed as §3 item 5 requires: `BLOCKED_INJECTIONS: dict[str, str] = {}` is an empty literal and nothing anywhere writes into it, so `name in BLOCKED_INJECTIONS` is False for every input and the branch is dead today. This is a landmine rather than a live defect, and it detonates on the first commit that registers a blocked injection class. It is registered under F083 rather than routed elsewhere because it is the concrete proof of R-0468 and inseparable from it: ruff has flagged this exact line as F821 for as long as the line has existed, and the only reason nobody noticed is that no stage of Remedy's CI runs ruff. A linter finding nobody reads is indistinguishable from having no linter. Fix and finding travel to T002 together with R-0468. OPEN.
--- END SLICE RECORD-R10 ---

--- BEGIN SLICE PLAN --- (WHOLE FILE replacement of .agent/plan.md, C3)
# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0470. Open findings: the seventy-five carried out
of the F082 record plus R-0448 to R-0469 registered on this branch, of which
R-0456 to R-0459 and R-0467 are resolved. `.agent/live_review.md` is the source
of truth.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R11 records the R10 PASS, registers R-0468 and R-0469, and measures every stage
serially and under `-n auto` into `.agent/f083_inventory.md` Q5, so the budget
stage can be written from data. It lands no stage and no production code.

## Next Steps
1. R12 writes the determinism and budget stages from the Q5 readings, decides
   the determinism stage's shape as a recorded DECISION, and rules on R-0468.

## Risks
- The determinism stage has no marker of its own and the run-manifest suite is
  auto-marked `integration`, so it may already sit wholly inside `standard`.
  Q5 gate 9 measures that; until it is measured, no stage shape is chosen.
--- END SLICE PLAN ---

Done when — run every gate, record its REAL value; a gate you cannot run is reported as not run, never as green:

 1. `pwd` printed FIRST and equal to the repository root. `git status --porcelain`
    EMPTY before the first commit and before C4. `git worktree list` ONE line at
    round start and at handback. `.agent/STOP` ABSENT at both (R-0347).
 2. BASE: `git rev-parse HEAD` before the first commit; report it and whether it
    equals c6db29fa.
 3. TRANSPORT, bytes read in Python: sha256, byte count and line count of
    `.agent/authored/f083-r11.md` and `.agent/last_block.md`; whether the two are
    EQUAL; whether the measured line count equals this block's declared footer.
 4. C1 PREFIX PROPERTY over `<C1>^..<C1>`: `pre` prefixes `post`, and
    `post[len(pre):]` equals `b"\n" + RECORD-R10`, that slice extracted from the
    COMMITTED `.agent/authored/f083-r11.md` by its markers. Report the numstat;
    its deletion column must be 0.
 5. MEASUREMENT — COLLECTED COUNT PER STAGE. For each of the five stages, reading
    its expression from `CI_STAGES` (constraint 7):
    `python3 -m pytest --collect-only -q -p no:cacheprovider -m "<expression>"`.
    Report stage name, collected count, total, and REAL exit code for each.
    [Reviewer measured at c6db29fa: fast 3975, standard 12579, ui 397, smoke 23,
    excluded 79, total 17045, each exit 0. Report what YOU measure.]
 6. MEASUREMENT — THE INSTRUMENT CAN GO RED. A collect that selects nothing must
    be distinguishable from a green one, or every timing below is worthless:
    `python3 -m pytest --collect-only -q -p no:cacheprovider -m "no_such_marker_at_all"`
    — report the REAL exit code and the last output line. [Reviewer measured exit
    5 and `no tests collected`. An empty selection is exit 5, never exit 0.]
 7. MEASUREMENT — THE LONG POLE, BOTH WAYS. The `fast` stage, twice, timed with
    `time.monotonic()` around each `subprocess.run`, direct pytest per constraint 6:
    (a) `python3 -m pytest -q -m "<fast expression>"`
    (b) `python3 -m pytest -n auto -q -m "<fast expression>"`
    Report for each: wall-clock seconds, REAL exit code, and the final summary
    line verbatim (passed/failed/skipped counts). Also report `os.cpu_count()`.
    The plan's standing risk is that (a) was once 391.8 s; this gate replaces
    that single reading with two taken together on one machine.
 8. MEASUREMENT — THE OTHER STAGES UNDER `-n auto`, each timed the same way,
    each its own process: `standard`, `ui`, `smoke`. Report wall-clock seconds,
    REAL exit code and the final summary line for each. `standard` is the large
    one — the reviewer's collect read 12579 tests — so expect it to dominate.
    Do NOT run `excluded`: it selects `real_ollama` and needs a live server.
    Report `excluded` as not run, with the stage's own `manual_command`.
 9. MEASUREMENT — THE DETERMINISM CANDIDATE SET, the question R12 needs settled.
    Report: how many files match `tests/orchestration/test_run_manifest_*.py`;
    how many tests they collect
    (`python3 -m pytest --collect-only -q -p no:cacheprovider tests/orchestration/test_run_manifest_*.py`);
    and whether EVERY one of those test ids also appears in the `standard`
    selection — measure it, by collecting `standard` with `--collect-only -q` and
    testing set containment in Python, never by reasoning about markers. Report
    the containment as True/False plus the count of any ids outside `standard`.
10. C2 PREFIX PROPERTY over `<C2>^..<C2>` for `.agent/f083_inventory.md`: `pre`
    prefixes `post`, the tail begins with `b"\n\n## Q5 — Stage runtime, measured at R11"`,
    and the numstat deletion column is 0. Then confirm, and say so explicitly,
    that every numeral in the Q5 section appears in the gate 5 to 9 output above.
11. GATE — THE CI SUITES ARE UNDISTURBED, each its own process, REAL exit code
    from the process (R-0438), each via `python3 -m pytest <path> -q`:
    `tests/orchestration/test_ci_stages.py` [7, 0];
    `tests/orchestration/test_ci_stage_selection.py` [9, 0];
    `tests/cli/test_ci_cmd.py` [6, 0]; `tests/orchestration/test_ci_run.py` [8, 0].
12. GATE — VERIFICATION, each run separately, REAL exit code from the process:
    `tests/ui_server/test_dashboard_contract.py` [70, 0];
    `tests/regression/test_resource_safety.py` [21, 0];
    `tests/orchestration/test_integrity_gate.py` [15, 0]; canary
    `tests/cli/test_golden_path.py` [42, 0].
13. GATE — NOTHING ELSE MOVED: `git diff --name-only c6db29fa..HEAD -- packages/
    apps/ tests/ docs/` must print NOTHING. Report it as a measured list, and
    confirm you ran it from the repository root — at the wrong root it is vacuous.
14. GATE — INTEGRITY, in Python because the `remedy` CLI is denied here (R-0408):
    `python3 -c "from packages.orchestration.integrity_gate import
    run_integrity_checks, export_integrity_json; import json;
    print(json.dumps(export_integrity_json(run_integrity_checks())))"` — report
    `passed`, `fail_count`, `check_count`, every check's status, and the
    `handler_import` message [BASE: handlers=338; this round adds no handler].
15. GATE — OPEN SET at HEAD: count `^- R-\d+ — ` paragraphs, `^Done: R-\d+ — `
    and `^Landed: R-\d+ — ` lines; report all three, registered-minus-done, max
    id, next free id, any duplicate. Reviewer measured 95 / 5 / 0, open 90, max
    R-0467 at BASE and expects 97 / 5 / 0, open 92, max R-0469, next free R-0470.
    Report what you MEASURE.
16. C3 PLAN byte-equals the PLAN slice as a whole file — report sha256, line count
    (under 50), `## Goal` and `## Next Steps` present, no `- [ ]` line, and the
    count of numbered items under `## Next Steps`.
17. CHANGE SET at C3 — FIVE paths, `.agent/handoff.md` being written by C4 and so
    absent from any measurement preceding it: `git diff --name-only
    c6db29fa..HEAD`. Report the list and count; name `.agent/handoff.md` the
    sixth path C4 adds.
18. Insertions (`+` column only) for C0a through C3 — report each; none over 500.
    C0b is a verbatim single-`.agent/`-file rewrite, AGENTS.md-exempt; report it
    anyway. C4's own count cannot exist inside C4 (R-0149): final message.

The push result, post-C4 clean-tree reading and open-PR list postdate C3, so per
R-0449 and R-0452 they are NOT ordered into that file: run `git push -u origin
feature/f083-ci-self-check` after C4, create no PR, report all three in the final
message.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md, as C4
— feature and round, branch, per-commit changed-files tables, every gate value
above, the item-status table covering every C-item and every gate, open findings
with max and next free id, and next action R12 as the plan states it. C4 cannot
table its own SHA (R-0371, R-0149); say so. Over a cap, name BOTH caps (R-0462).
Fortschritt, verbatim:

Fortschritt: 40 % (F083 beansprucht · R1 bis R7, R9 und R10 PASS, R8 FAIL auf einem roten ruff-Gate und in R9 repariert · Stage-Tabelle, Stage-Runner, die `remedy ci` CLI-Naht und die Selektionstests samt Live-Wächter als Code gelandet · R11 misst jede Stage seriell und unter `-n auto`, damit das Laufzeit-Budget aus Daten statt aus einer Schätzung entsteht · noch keine Determinismus- oder Budget-Stage, keine hosted workflows) — gemessen, nicht geschätzt

If a GATE (11 to 15) is RED, or anything here contradicts what you find on disk:
finish the commit you are in, write the handoff naming the exact blocker, end. Do
not widen scope to route around it (G8). A red MEASUREMENT (gates 5 to 9) is data:
write it down and carry on, per constraint 5.

BLOCK SIZE, measured on these final bytes: 246 lines (cap 400, DECISION F105 D5).
──────────────────────────────────────────────────────────────────────────────
