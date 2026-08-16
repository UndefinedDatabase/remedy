── STEP R17-REPAIR — T2_F083 CI self-check — REPAIR + RECORD, session-closing ─
Goal:        Record the R16-REC PASS, register the one defect that round left on
             disk, and repair `.agent/plan.md` so the file the next session reads
             second states the right round and the right finding set. This round
             takes no measurement and writes NO production code.
Bundle:      FIVE commits, in this order, with these exact subjects:
  C0a `docs(f083): save the R17 repair block verbatim` — THIS ENTIRE BLOCK,
      byte-verbatim, to `.agent/authored/f083-r17-repair.md`.
  C0b `docs(f083): mirror the R17 repair block into last_block` —
      `.agent/last_block.md` becomes a byte-identical copy of that file.
  C1  `docs(f083): record the R16-REC PASS and register R-0481` — the
      RECORD-R16REC append at EOF of `.agent/live_review.md`, nothing else.
  C2  `docs(f083): repair the plan round number and finding set` —
      `.agent/plan.md` replaced as a WHOLE FILE by the PLAN slice.
  C3  `docs(f083): write the R17 repair handback` — `.agent/handoff.md` alone.
Change:      Exactly five files: `.agent/authored/f083-r17-repair.md`,
             `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
             `.agent/handoff.md`. NO code path is touched by this round.
Constraints:
  1. Apply every slice BYTE-VERBATIM. If a FROM string is not found exactly
     once, STOP, commit nothing further, write the handoff naming the slice and
     what you found instead (G8). Never repair a slice yourself.
  2. Do NOT touch `.agent/f083_inventory.md`, nor anything under `packages/`,
     `apps/`, `tests/`, `scripts/` or `docs/`. This round is state-only.
  3. No `git commit --amend`, `git rebase`, `git reset`, force push or PR
     (R-0477, G2). The subjects above are given so you never choose one.
  4. Do NOT edit any text already committed in `.agent/live_review.md`. The
     superseded sentences stay where they are; the correction lives in the new
     finding (R-0470's principle). Only `.agent/plan.md` is repaired forward,
     because it is live bridge state AGENTS.md orders rewritten, not a record.
Slice convention: every slice is delimited by its own `--- BEGIN SLICE <NAME>
---` and `--- END SLICE <NAME> ---` markers, which are transport only and NEVER
reach a target file. EACH MARKER IS EXACTLY ONE LINE: a slice's content starts
on the line AFTER its BEGIN marker and ends on the line BEFORE its END marker,
and every blank line between those two is part of the content. The named units
are RECORD-R16REC and PLAN. A slice with no FROM: line is an EOF-APPEND:
concatenate its content to the target's bytes EXACTLY as given — its leading
blank line is part of it — and change nothing already in the file.
--- BEGIN SLICE RECORD-R16REC --- (EOF-APPEND to .agent/live_review.md, C1)

Gate: R16-REC — PASS. The reviewer re-ran all sixteen R16-REC gates itself at 0d9c72e0 from the repository root and all sixteen reproduce. TRANSPORT, proved against the reviewer's OWN scratchpad original rather than by digest fallback (§4.9): `.remedy-wt/f083-r16-block.md`, the committed `.agent/authored/f083-r16-rec.md` and the committed `.agent/last_block.md` are all three byte-equal at sha256 ce30a79f6e1bbc61 over 20986 bytes and 171 lines, under the 400-line cap. C1's prefix property holds with the tail byte-equal to the RECORD-R15 slice extracted from the COMMITTED authored file by its markers, 9957 bytes, numstat `8 0`. C2's `.agent/plan.md` byte-equals its PLAN slice at sha256 79411ece7fbca4d4, 39 lines, `## Goal` and `## Next Steps` present, 0 `- [ ]` lines. Both range gates printed NOTHING from the repository root: the scoped diff over `packages/`, `apps/`, `tests/`, `scripts/` and `docs/`, and the diff over `.agent/f083_inventory.md`, whose `^## Q\d` headings still read Q1 through Q11. The measured change set is the five `.agent/` paths. Every gate ran as its own process with the exit code read from that process: the four CI suites at 10, 9, 6 and 10 passed and the verification quartet at 70, 21, 15 and 42 passed, all exit 0; `python3 -m ruff check .` ends `Found 26 errors.` at exit 1, EQUAL to the `## Q10` baseline; the integrity gate reports passed true, fail_count 0, check_count 5, handlers=338; the open set recomputes to 108 registered, 6 `Done:`, 0 `Landed:`, 102 open, max R-0480, next free R-0481, no duplicate id — exactly what the block predicted. Insertions 171, 98, 8 and 13, none over 500. THE ORDERING GATE WAS THE POINT AND IT HELD: the worker took the lint and integrity readings BEFORE any pytest command ran, which is the discipline R-0479 exists to impose, so both are values rather than contaminated samples. The R-0480 exception did not trigger in the primary checkout, whose npx cache is warm, so no second dashboard-contract reading exists and none is claimed. The worker's conduct was correct throughout: both slices applied byte-verbatim, no `Done:` paragraph of its own, the change set exactly the ordered paths, and both deviations declared — including one worth keeping, that it discarded a gate reading it had piped through `tail` because the pipe would have masked the exit code, and re-ran the suite bare. One defect remains and it belongs entirely to the reviewer, registered below.

- R-0481 — Medium, A LATE INSERTION WAS SWEPT THROUGH A BLOCK'S ARITHMETIC BUT NOT THROUGH ITS PROSE, AND THE PLAN ON DISK NOW UNDERSTATES ITS OWN ROUND. The R16-REC block was authored with two findings and finished with three: R-0480 was written after the rest of the block existed, once the reviewer had chased a one-off dashboard-contract reading to its cause. The insertion sweep updated everything that could be COUNTED — gate 13's expectation moved to 108 / 6 / 0 with max R-0480, C1's subject became "register three findings", the PLAN's next-free id became R-0481, and a new Risks bullet named R-0480 — and it updated nothing that was merely WRITTEN. Three clauses are wrong on disk as a result, all inside the PLAN slice applied at C2 and all verified by the reviewer at 0d9c72e0: `## Current Step` says "This record round wrote that verdict and the two findings it produced" where the round registered THREE; `## Next Steps` says the next round "must honour R-0478 and R-0479 when it writes its gates", silently dropping R-0480, which is the only one of the three that names a stage the next round has to design around; and `## Current Step` closes "R16 has not started" while C2's own commit subject reads "point the plan at the R17 budget stage", so the commit message and the file it commits name different rounds. Nothing is fabricated and no gate value is affected — the worker applied the slice byte-verbatim and correctly, every number the block gated on was right, and the reviewer's arithmetic reproduced at every gate. What broke is that `.agent/plan.md` is the file AGENTS.md's Session Resume orders read SECOND, before any doc and before the diff, and a session resuming from it is told to honour two findings when three are open and is given two different names for the round it should start. Medium for that reason and no other: it costs the next session a reconciliation it should not have to perform, in the one file that exists to prevent exactly that. This is the R-0474 and R-0475 shape a third time, with the trigger named at last — not a moved referent and not a stale status claim, but a LATE ADDITION whose sweep stopped at the numerals. Standing rule, binding the reviewer: when a finding, item or slice is added to a block that is already drafted, the re-sweep covers the block's PROSE as well as its counts — every sentence that enumerates the finding set, names the next round, or lists what the next round must honour is re-read against the block's FINAL bytes, and the pre-emission checklist's mechanical items are re-run on those bytes rather than on the draft they were first run on. ROUND NUMBERING, ruled here because two clauses on disk disagree and neither may be rewritten: the record round committed as `f083-r16-rec.md` has SPENT the number 16, the repair round carrying this finding is R17, and the next ENGINEERING round — the budgets stage, the R-0468 ruling and the determinism shape — is R18. The PLAN slice of this block states that and nothing else; the superseded "R16" and "R17 budget stage" clauses are left standing where they are, per R-0470. OPEN.
--- END SLICE RECORD-R16REC ---
--- BEGIN SLICE PLAN --- (WHOLE FILE, replaces .agent/plan.md, C2)
# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0482. `.agent/live_review.md` is the source of
truth for the open set; this file repeats no count of it.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
None in flight. R15 is closed PASS: every stage carries a measured `timeout_sec`,
the runner is handed that budget per call, and `standard` is no longer killed at
the runner's 600-second default. R16-REC is closed PASS and recorded it. This
repair round, R17, registered R-0481 and rewrote this file; it ends the session.
Round numbering, ruled at R-0481: 16 is spent by the record round and 17 by this
one, so the next engineering round is R18. R18 has not started.

## Next Steps
1. R18 takes the three items DECISION F083 D3 deferred: the `budgets` STAGE
   T2_F083's Design asks for, which checks documented ceilings and runs the guard
   tests and does not yet exist; a ruling on R-0468 from the 26-error ruff
   baseline `## Q10` records; and the determinism stage's shape settled as a
   DECISION. It is a SPLIT round — the budgets stage is production code — and its
   gates must honour R-0478, R-0479 and R-0480.

## Risks
- A per-stage `timeout_sec` is a kill threshold, NOT the budgets stage; reading
  R15 as the stage would close F083 with a Design item unbuilt.
- The determinism suite is already wholly inside `standard` (850 ids, 0 outside,
  measured at R11), so a determinism stage duplicates work unless `standard`'s
  expression is narrowed in the same change.
- A budgets stage that runs the integrity gate or a repo-wide lint count while
  other stages execute against the same checkout will read a clean repository as
  dirty (R-0479). Sequence it, or it reports a failure that is not there.
- The `ui` stage is RED on a clean checkout with a cold npx cache (R-0480), so
  the Acceptance line "clean checkout: green" is not met today. R18 rules on it.
--- END SLICE PLAN ---

Done when — run every gate, record its REAL value; a gate you cannot run is
reported as not run, never as green (G4). EVERY PATH BELOW IS COMPLETE AND
RESOLVES ON DISK AS WRITTEN — run it exactly as given (R-0478):

 1. `pwd` printed FIRST and equal to `/home/decodeux/Repos/remedy`. `git status
    --porcelain` EMPTY before C0a and before C3. `git worktree list` ONE line at
    round start and at handback. `.agent/STOP` ABSENT at both (R-0347).
 2. BASE: `git rev-parse HEAD` before C0a; report it and whether it equals
    0d9c72e0.
 3. TRANSPORT AND SIZE, bytes read in Python: sha256, byte count and line count
    of `.agent/authored/f083-r17-repair.md` and `.agent/last_block.md`, and
    whether the two are EQUAL. This block declares no count of its own, so
    report the measured line count as a value — yours is the only measurement.
 4. C1 PREFIX PROPERTY over `<C1>^..<C1>`: `pre` prefixes `post`, and
    `post[len(pre):]` EQUALS the RECORD-R16REC slice extracted from the COMMITTED
    `.agent/authored/f083-r17-repair.md` by its markers. Report numstat; the
    deletion column must be 0.
 5. NO CODE MOVED: `git diff --name-only 0d9c72e0..HEAD -- packages/ apps/
    tests/ scripts/ docs/` must print NOTHING. Report it as a measured list and
    confirm you ran it from `/home/decodeux/Repos/remedy`.
 6. `.agent/f083_inventory.md` UNTOUCHED: `git diff --name-only 0d9c72e0..HEAD
    -- .agent/f083_inventory.md` prints NOTHING, and its `^## Q\d` count is 11.
 7. C2 PLAN byte-equals the PLAN slice as a whole file — report sha256, line
    count (under 50), `## Goal` and `## Next Steps` present, no `- [ ]` line.
 8. GATE — THE REPAIR IS A REPAIR, not merely a diff. At HEAD, `.agent/plan.md`
    must contain the string `R18 has not started`, must contain
    `R-0478, R-0479 and R-0480`, and must contain NEITHER `the two findings it
    produced` NOR `R16 has not started`. Report all four readings separately.
 9. GATE — ORDERING (R-0479): run gates 10 and 11 BEFORE any pytest command in
    this round, and say in the handoff that you did.
10. GATE — LINT: `python3 -m ruff check .` from `/home/decodeux/Repos/remedy` —
    report its final `Found N errors.` line and exit code. [BASE: 26, exit 1.]
11. GATE — INTEGRITY, in Python because the `remedy` CLI is denied here
    (R-0408): `python3 -c "from packages.orchestration.integrity_gate import
    run_integrity_checks, export_integrity_json; import json;
    print(json.dumps(export_integrity_json(run_integrity_checks())))"` — report
    `passed`, `fail_count`, `check_count`, each check's status and the
    `handler_import` message [BASE: handlers=338; no handler is added here].
12. GATE — THE CI SUITES ARE UNDISTURBED, each its own process, REAL exit code
    read from that process, each `python3 -m pytest <path> -q`, UNPIPED so the
    exit code is the suite's own: `tests/orchestration/test_ci_stages.py` [10, 0];
    `tests/orchestration/test_ci_stage_selection.py` [9, 0];
    `tests/cli/test_ci_cmd.py` [6, 0]; `tests/orchestration/test_ci_run.py`
    [10, 0]. Report the counts you MEASURE.
13. GATE — VERIFICATION, each separately, same form as gate 12:
    `tests/ui_server/test_dashboard_contract.py` [70, 0];
    `tests/regression/test_resource_safety.py` [21, 0];
    `tests/orchestration/test_integrity_gate.py` [15, 0]; canary
    `tests/cli/test_golden_path.py` [42, 0]. On any red, report the FAILED ids
    VERBATIM before you stop — and if the ONLY failure is
    `TestJobSummaryCommandContract::test_typescript_compiles`, that is the known
    R-0480 cold-npx-cache defect: run that ONE suite a second time, report BOTH
    readings with their exit codes, then continue.
14. OPEN SET at HEAD: count `^- R-\d+ — ` paragraphs, `^Done: R-\d+ — ` and
    `^Landed: R-\d+ — ` lines; report all three, registered-minus-done, max id,
    next free id, any duplicate. [BASE: 108 / 6 / 0, open 102, max R-0480.] This
    block registers R-0481, so expect 109 / 6 / 0, open 103, max R-0481, next
    free R-0482. Report what you MEASURE.
15. CHANGE SET at C2 — FOUR paths, `.agent/handoff.md` being written by C3 and
    so absent from any measurement preceding it: `git diff --name-only
    0d9c72e0..HEAD`. Report the list and count; name `.agent/handoff.md` the
    fifth path C3 adds.
16. Insertions (`+` column only) for C0a through C2 — report each; none over
    500. C0b is a verbatim single-`.agent/`-file rewrite and AGENTS.md-exempt;
    report it anyway. C3's own count cannot exist inside C3 (R-0149).
17. NO COMMIT WAS AMENDED (R-0477): confirm in one sentence that you ran no
    `git commit --amend`, no `git rebase` and no `git reset` this round.

The push, the post-C3 clean-tree reading and the open-PR list postdate C2, so
per R-0449 they are NOT ordered into the handoff: run `git push -u origin
feature/f083-ci-self-check` after C3, create no PR, and report all three in your
final message with C3's own SHA and insertion count.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
feature and round, branch, per-commit changed-files tables, an item-status table
covering C0a through C3 and every gate above, the real verification values, the
open-findings count, and the next expected action, which is R18 as the PLAN
slice states it. This is the SESSION-CLOSING round: the handoff's first two
numbered next actions are to read `.agent/STOP` from disk and then run the Open
PR Gate, in that order, before anything else. Declare any cap overage with its
mandated cause (DECISION D15). End the handoff with this line verbatim:

Fortschritt: 52 % (F083 beansprucht · R1 bis R7 und R9 bis R15 PASS, R8 FAIL auf einem roten ruff-Gate und in R9 repariert · Stage-Tabelle, Stage-Runner, die `remedy ci` CLI-Naht und die Selektionstests als Code gelandet · seit R15 trägt jede Stage ihr gemessenes Wall-Clock-Budget und `standard` wird nicht mehr nach 600 Sekunden abgeschnitten · noch keine budgets-Stage, keine Determinismus-Stage, kein Lint-Ceiling, keine hosted workflows · neu gemessen: die ui-Stage ist auf einem frischen Checkout rot, solange der npx-Cache kalt ist) — Rundenzahl gemessen, Prozentwert geschätzt

If a GATE is RED, or anything here contradicts what you find on disk: finish the
commit you are in, write the handoff naming the exact blocker, end. Do not widen
scope to route around it (G8).
──────────────────────────────────────────────────────────────────────────────
