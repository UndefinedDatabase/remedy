── STEP R12/15 — F083 CI self-check — RECORD R11 PASS, REGISTER R-0470 TO R-0473, REPAIR THE HEADING COLLISION ──

Goal:
  Close the R11 round honestly. Its execution was clean, but three of its
  deviations were defects in the reviewer's block and one of them put a real
  fault on disk: `.agent/f083_inventory.md` now carries TWO sections opening
  `## Q5 —`, because a heading was prescribed for a file the reviewer never
  read. This round records the PASS, registers the four findings the review
  produced, and repairs that heading. It lands NO stage and NO production code:
  the budget stage T002 asks for is written in R13 from the Q5 data, by a
  session with the context to do it justice.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f083-r12.md`
  C0b  mirror it byte-identically into `.agent/last_block.md`
  C1   `.agent/live_review.md` — RECORD-R11 appended at EOF, ONE commit, one
       body: gate line, blank line, the four findings, the one `Done:` line.
  C2   `.agent/f083_inventory.md` — the HEADING pair, ONE commit.
  C3   `.agent/plan.md` (PLAN, whole file), ONE commit.
  C4   `.agent/handoff.md`, the handback, alone.

BASE: 7130ed76. Re-derive `git rev-parse HEAD` before the first commit and report
whether it equals 7130ed76. If it does NOT, stop and hand off.

TRANSPORT: no paste relay and no scratchpad file this session. The authored
original of this block is the byte range your prompt delimits with
`--- BEGIN BLOCK BYTES ---` / `--- END BLOCK BYTES ---`; C0a writes exactly that
range and C0b mirrors it.

BLOCK SIZE — READ THIS, IT IS THE POINT OF R-0470. This block declares NO line
count of its own. R11's footer declared 246 lines against 241 measured, because
the reviewer wrote a numeral it had not measured; the standing rule is count it
or state no numeral. Gate 3 therefore asks YOU to measure the count and to check
it against the 400-line cap (DECISION F105 D5), and a block over the cap is a
finding against the reviewer that you declare, not a defect you repair.

SLICE CONVENTION (R-0437): every slice body below is the lines between its
markers INCLUDING the trailing newline of its last line, and every shape is
declared under that convention. The authored units are, listed and NOT counted:
RECORD-R11, HEADING-FROM, HEADING-TO, PLAN.

SHAPES, stated at authoring time (§4.9):
  · RECORD-R11 is an APPEND to `.agent/live_review.md`, proved by the prefix
    property in gate 4. The correct tail is `b"\n" + RECORD-R11` — ONE newline,
    because the file already ends with one. R11's gate 10 got this wrong in the
    other direction and you were right to apply the contract over the literal.
  · HEADING is a REWRITE — the TO does not contain the FROM — proved by
    FROM 0x and TO 1x over the whole file at C2.
  · PLAN is a WHOLE FILE, proved by byte equality in gate 10.

Constraints:
  1. Change set, exactly: `.agent/authored/f083-r12.md`, `.agent/last_block.md`,
     `.agent/live_review.md`, `.agent/f083_inventory.md`, `.agent/plan.md`,
     `.agent/handoff.md`. Nothing else. `packages/`, `apps/`, `tests/` and
     `docs/` stay EMPTY in the range diff — this round writes no code.
  2. Apply every slice BYTE-VERBATIM. A defect in reviewer text is a declared
     deviation, never a silent repair.
  3. Commit strictly in the C-order above. Push after C4. Create NO pull request.
  4. This round adds NO git worktree and performs NO mutation and NO timing run.
  5. The HEADING pair renames the section R11 appended, from `## Q5 —` to
     `## Q9 —`. It does NOT touch the ORIGINAL `## Q5 — Measured wall time and
     outcome per stage` at the top of the file, and it does NOT touch the two
     body sentences that cite "Q5" meaning that original — those two references
     become UNAMBIGUOUS as a result of this rename, which is the repair working,
     not a side effect to correct. Change nothing else in that file.

--- BEGIN SLICE RECORD-R11 --- (APPEND to .agent/live_review.md, C1, with exactly one blank line between the file's current last line and the first line of this slice. The blank line INSIDE this slice, between the gate line and the first finding, is part of it.)
Gate: R11 — PASS. The reviewer re-ran the round at its head from the repository root and reproduced it: the authored file and `.agent/last_block.md` are byte-equal at sha256 45b35ecfd0c0 over 22819 bytes and 241 lines; the C1 prefix property holds with the tail byte-equal to `b"\n" + RECORD-R10` and a deletion column of 0; the C2 prefix property holds with the tail opening on a single newline and the Q5 heading; `.agent/plan.md` byte-equals its PLAN slice at 29 lines; the change set at C3 is exactly the five declared paths with `.agent/handoff.md` the sixth added by C4; and the scoped range diff over `packages/`, `apps/`, `tests/` and `docs/` printed nothing, so a round that promised no code delivered none. Every gate was re-run as its own process with the exit code read from that process: the four CI suites at 7, 9, 6 and 8 passed and the verification quartet at 70, 21, 15 and 42 passed, all exit 0; the integrity gate reports passed true, fail_count 0, check_count 5, handlers=338; the open set recomputes to 97 registered, 5 `Done:`, 0 `Landed:`, 92 open, max R-0469, next free R-0470, no duplicate id. The MEASUREMENTS were re-taken rather than read: the reviewer's own collect reproduces fast 3975, standard 12579, ui 397, smoke 23 and excluded 79 against a suite total of 17045, the bogus-marker control exits 5 with `no tests collected` so an empty selection cannot pass for a green one, `fast` under `-n auto` re-reads 55.1 s at exit 0 with the identical `3968 passed, 7 skipped` summary, and the determinism candidate set re-measures as 45 files and 850 ids with set containment in `standard` True and 0 ids outside. The Q5 section itself is the conduct this repository wants: it records `not measured` where nothing was run, it declines to state a serial time for the three stages that were only run in parallel, it names the CPU count beside every `-n auto` reading, and it carries no recommendation and no budget number — evidence, kept separate from the decision it will inform. The worker's conduct was correct throughout: it applied every slice byte-verbatim, it refused to invent its own commit SHA, and it declared three deviations rather than silently repairing reviewer text. All three of those deviations are defects in the reviewer's block and none is a defect in the work, and they are charged to the reviewer as R-0470, R-0471 and R-0472 below. The fourth finding is not a deviation at all: it is what the reviewer found by re-running a measurement instead of reading it.

- R-0470 — Low, A BLOCK DECLARED A SIZE IT HAD NOT MEASURED. The R11 footer reads "BLOCK SIZE, measured on these final bytes: 246 lines", and the transported bytes measure 241 lines at 22819 bytes in both `.agent/authored/f083-r11.md` and `.agent/last_block.md`, which are byte-equal to each other. The word "measured" was false: no count was taken, a number was recalled. The worker did exactly the right thing — it reported the mismatch, declared it, and changed nothing to close the gap, because closing a gap between a claim and the bytes by editing the bytes is how a record stops being one. Low because nothing downstream consumed the numeral and the cap was never in danger at either value. This is the R-0402 / R-0404 / R-0436 family, whose standing rule is count it or state NO numeral, and §3 item 1 already orders the count to be taken mechanically on the FINAL bytes after the last edit; the rule was not missing, it was skipped. Refinement, binding the reviewer and already applied by the block that carries this text: a block whose reviewer cannot mechanically count its own final bytes — which is every block in a session with no scratchpad file, because the bytes exist only in the prompt — declares NO line count and orders the WORKER to measure it against the cap instead. A number the author cannot verify is not a declaration, it is a guess wearing a declaration's clothes. OPEN.
- R-0471 — Low, TWO CLAUSES OF ONE BLOCK DISAGREED ABOUT A SINGLE NEWLINE. R11's C2 contract required "exactly one blank line between the file's current last line and its first line", while gate 10 of the same block ordered the appended tail to begin `b"\n\n## Q5 — …"`. Because `.agent/f083_inventory.md` already ended with a newline, the contract yields a tail of `b"\n## Q5 — …"` and the gate's literal would have produced two blank lines: the two clauses cannot both be satisfied. Gate 4 of that same block had the newline right for the live_review append, so the block contradicted not only itself but its own neighbouring gate. The worker applied the contract, reported the gate as measured, and declared the difference, which is the correct order of precedence and the correct disclosure. Low because the disagreement was visible on inspection and cost no rework beyond the declaration. This is the R-0437 newline family crossed with the clause-versus-clause defect: the fix is not more prose about newlines but a mechanical pass in which every gate literal that quotes an append boundary is checked against the convention paragraph of the SAME block before emission, in the same sweep §3 item 9 uses to re-grep citations. OPEN.
- R-0472 — Medium, A HEADING WAS PRESCRIBED FOR A FILE THE REVIEWER NEVER OPENED. R11's C2 contract fixed the appended section's first line as `## Q5 — Stage runtime, measured at R11`. `.agent/f083_inventory.md` already carried `## Q5 — Measured wall time and outcome per stage` from R2, and its sections already ran Q1 through Q8, so the ordered heading both duplicated an existing one and restarted the numbering after Q8. The worker applied the ordered bytes and declared the collision, which is right — reviewer text is not the worker's to edit — and the result is that the file on disk now holds two sections opening `## Q5 —` with the second sitting after Q8. Medium and not Low because this one did not stop at a false claim: it put a real fault into a document that two of its own body sentences already cite by Q-number, so a later reader following "the reviewer's `-n auto` reading in Q5" has two candidate sections and no way to choose. It is the §3 item 6 failure class in its plainest form — the block that writes into a file must be checked against what that file ALREADY contains — and the check was not skipped so much as never reached, because the reviewer prescribed a heading for a file it had not opened. Refinement, binding the reviewer: any block ordering an append to a file it has not read in the CURRENT session reads that file first and, for a structured file, greps the sibling headings before naming a new one. RESOLVED by this round's C2, which renames the appended section to `## Q9 —`, restoring a single monotonic sequence and disambiguating the two existing citations as a side effect.
- R-0473 — Medium, A BUDGET IS ABOUT TO BE WRITTEN FROM ONE READING PER STAGE, WHICH IS THE MISTAKE THE PLAN'S OWN RISK NAMES. Q5 records exactly one wall-clock reading for each of `standard`, `ui` and `smoke`, and two for `fast`. The reviewer re-ran `standard` under `-n auto` on the SAME machine at the SAME commit with the expression read from `CI_STAGES`, and measured 170.1 s against the 138.8 s Q5 records — a spread of about 22 % — while the pass and skip counts were identical at 12578 and 1, and the exit code was 0 both times. Nothing was fabricated and Q5 is not wrong: a single reading honestly reported as a single reading is exactly what it claims to be, and the section carries no budget number precisely because choosing one was left to a later round. The finding is about what happens NEXT. `.agent/plan.md` has carried, for several rounds, the risk that `fast` rested on a single 391.8 s reading and that no runtime budget could be written from it; R11 replaced that with two readings for `fast` and one for every other stage, so for three of the five stages the risk is unchanged in kind and merely newer. A ceiling set at or just above a single sample fails the first time ordinary variance exceeds it, and a CI that fails for variance teaches its readers to ignore it — which is worse than having no budget, because it spends the credibility the budget existed to build. Medium because the budget stage is the very next piece of work and would bake the error in. Binding R13: before any ceiling is written, each stage that will carry one is measured at least three times and the ceiling is set from the observed SPREAD with its headroom stated, or the budget is documented as provisional and says on its face how many samples it rests on. Remedy does not need a tight budget; it needs an honest one. OPEN.
Done: R-0472 — the appended section is renamed to `## Q9 —`; see C2 of R12.
--- END SLICE RECORD-R11 ---

--- BEGIN SLICE HEADING-FROM --- (the REWRITE pair's FROM, C2; one whole line occurring exactly once in .agent/f083_inventory.md — the heading R11 appended, NOT the original Q5 near the top of the file)
## Q5 — Stage runtime, measured at R11
--- END SLICE HEADING-FROM ---

--- BEGIN SLICE HEADING-TO --- (the REWRITE pair's TO, C2; replaces HEADING-FROM in place, one whole line)
## Q9 — Stage runtime, measured at R11
--- END SLICE HEADING-TO ---

--- BEGIN SLICE PLAN --- (WHOLE FILE replacement of .agent/plan.md, C3)
# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0474. Open findings: the seventy-five carried out
of the F082 record plus R-0448 to R-0473 registered on this branch, of which
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
R12 records the R11 PASS, registers R-0470 to R-0473, and repairs the heading
collision R11 introduced by renaming the appended inventory section to `## Q9`.
It lands no stage and no production code.

## Next Steps
1. R13 writes the determinism and budget stages from the `## Q9` readings, under
   R-0473: at least three samples per stage that carries a ceiling, or a budget
   that states on its face how many samples it rests on. It also rules on R-0468.

## Risks
- The determinism suite is already wholly inside `standard` — 850 ids, 0 outside,
  measured at R11 — so a determinism stage would duplicate work unless
  `standard`'s expression is narrowed in the same change. Decide it as a DECISION.
- 26 ruff errors stand repo-wide (R-0468) and no stage lints. A lint ceiling in
  the budget stage arrives red unless the baseline is recorded first.
--- END SLICE PLAN ---

Done when — run every gate, record its REAL value; a gate you cannot run is reported as not run, never as green:

 1. `pwd` printed FIRST and equal to the repository root. `git status --porcelain`
    EMPTY before the first commit and before C4. `git worktree list` ONE line at
    round start and at handback. `.agent/STOP` ABSENT at both (R-0347).
 2. BASE: `git rev-parse HEAD` before the first commit; report it and whether it
    equals 7130ed76.
 3. TRANSPORT AND SIZE, bytes read in Python: sha256, byte count and line count of
    `.agent/authored/f083-r12.md` and `.agent/last_block.md`; whether the two are
    EQUAL. Report the measured line count and whether it is at or under the
    400-line cap. This block declares no count of its own (R-0470); yours is the
    only measurement, so report it as a value and not as a comparison.
 4. C1 PREFIX PROPERTY over `<C1>^..<C1>`: `pre` prefixes `post`, and
    `post[len(pre):]` equals `b"\n" + RECORD-R11`, that slice extracted from the
    COMMITTED `.agent/authored/f083-r12.md` by its markers. Report the numstat;
    its deletion column must be 0.
 5. C2 PAIR over the whole `.agent/f083_inventory.md` at C2, a REWRITE:
    HEADING-FROM 1x BEFORE and 0x AFTER; HEADING-TO 0x before and 1x after.
    Report all four counts and the numstat, whose insertion and deletion columns
    must both be 1.
 6. C2 STRUCTURE, at C2, over the same file: report the count of lines matching
    `^## Q\d` and the full ORDERED list of those heading lines. There must be
    exactly one line beginning `## Q5 —` and exactly one beginning `## Q9 —`, and
    the sequence must read Q1 through Q9 with no number repeated.
 7. C2 DID NOT TOUCH THE REST: `git show --numstat <C2> -- .agent/f083_inventory.md`
    is `1 1`, and the two body sentences that cite Q5 are unchanged — report the
    count of the exact strings `` `-n auto` is what `standard` used in Q5.`` and
    `Q5 timed them as separate` over the file at C2; both must read 1.
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
11. GATE — NOTHING ELSE MOVED: `git diff --name-only 7130ed76..HEAD -- packages/
    apps/ tests/ docs/` must print NOTHING. Report it as a measured list, and
    confirm you ran it from the repository root — at the wrong root it is vacuous.
12. GATE — INTEGRITY, in Python because the `remedy` CLI is denied here (R-0408):
    `python3 -c "from packages.orchestration.integrity_gate import
    run_integrity_checks, export_integrity_json; import json;
    print(json.dumps(export_integrity_json(run_integrity_checks())))"` — report
    `passed`, `fail_count`, `check_count`, every check's status, and the
    `handler_import` message [BASE: handlers=338; this round adds no handler].
13. GATE — OPEN SET at HEAD: count `^- R-\d+ — ` paragraphs, `^Done: R-\d+ — `
    and `^Landed: R-\d+ — ` lines; report all three, registered-minus-done, max
    id, next free id, any duplicate. Reviewer measured 97 / 5 / 0, open 92, max
    R-0469 at BASE and expects 101 / 6 / 0, open 95, max R-0473, next free
    R-0474. Report what you MEASURE.
14. CHANGE SET at C3 — FIVE paths, `.agent/handoff.md` being written by C4 and so
    absent from any measurement preceding it: `git diff --name-only
    7130ed76..HEAD`. Report the list and count; name `.agent/handoff.md` the
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
with max and next free id, and next action R13 as the plan states it. C4 cannot
table its own SHA (R-0371, R-0149); say so. Over a cap, name BOTH caps (R-0462).
Fortschritt, verbatim:

Fortschritt: 42 % (F083 beansprucht · R1 bis R7 und R9 bis R11 PASS, R8 FAIL auf einem roten ruff-Gate und in R9 repariert · Stage-Tabelle, Stage-Runner, die `remedy ci` CLI-Naht und die Selektionstests samt Live-Wächter als Code gelandet · die Laufzeit jeder Stage ist jetzt gemessen statt geschätzt, und R12 räumt die Heading-Kollision auf, die R11 hinterlassen hat · noch keine Determinismus- oder Budget-Stage, keine hosted workflows) — gemessen, nicht geschätzt

If a GATE is RED, or anything here contradicts what you find on disk: finish the
commit you are in, write the handoff naming the exact blocker, end. Do not widen
scope to route around it (G8).
──────────────────────────────────────────────────────────────────────────────
