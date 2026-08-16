── STEP R14-REC — F083 CI self-check — RECORD THE R14 PASS, REGISTER R-0477, CLOSE THE SESSION ──

Goal:
  Put the R14 verdict on disk and end the session cleanly. The reviewer re-ran
  all fifteen R14 gates itself at 94e6c353 and all fifteen reproduce, so R14 is a
  PASS; one Low finding remains and is registered here. This round takes NO
  measurement, runs NO timing sample, writes NO ceiling, NO budget number, NO
  stage and NO production code. R15 does the engineering.

WHY A RECORD ROUND EXISTS AT ALL. In this repository a round's PASS is written by
the NEXT round's C1, so a session that ends right after a verdict would leave
that verdict nowhere but in a chat window. R15's block is the heavy one — a
per-stage timeout, a budget stage, a ruling on R-0468 and a determinism DECISION
— and authoring it well needs a session with its budget ahead of it, not behind
it. So the verdict lands here, on its own, and R15 starts clean.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f083-r14-rec.md`
  C0b  mirror it byte-identically into `.agent/last_block.md`
  C1   `.agent/live_review.md` — RECORD-R14 appended at EOF, ONE commit, one
       body: the gate line, a blank line, the one finding.
  C2   `.agent/plan.md` (PLAN, whole file), ONE commit.
  C3   `.agent/handoff.md`, the session-closing handoff, alone.

BASE: 94e6c353. Re-derive `git rev-parse HEAD` before the first commit and report
whether it equals 94e6c353. If it does NOT, stop and hand off.

BLOCK SIZE. This block declares NO line count of its own — the reviewer that
wrote it has no scratchpad file and cannot mechanically count its own final
bytes, and the standing rule from R-0470 is count it or state no numeral. Gate 3
asks YOU to measure the count and check it against the 400-line cap
(DECISION F105 D5). A block over the cap is a finding against the reviewer that
you DECLARE, not a defect you repair.

SLICE CONVENTION (R-0437): every slice body below is the lines between its
markers INCLUDING the trailing newline of its last line, and every shape is
declared under that convention. The authored units are, listed and NOT counted:
RECORD-R14, PLAN.

APPEND CONVENTION (R-0471): `.agent/live_review.md` already ends with a newline.
The append writes exactly ONE newline and then the appended text, which puts
exactly one blank line between the file's current last line and the appended
text's first line. Gate 4 reads `post[len(pre):]` and expects it to BEGIN with
exactly one `\n`. There is no other reading in this block.

SHAPES, stated at authoring time (§4.9):
  · RECORD-R14 is an APPEND to `.agent/live_review.md`, proved by the prefix
    property in gate 4 with the tail byte-equal to `b"\n" + RECORD-R14`.
  · PLAN is a WHOLE FILE, proved by byte equality in gate 6.
  · `.agent/handoff.md` is written by YOU to the contract below; no slice exists
    for it and no byte-equality gate is ordered or possible.

Constraints:
  1. Change set, exactly: `.agent/authored/f083-r14-rec.md`,
     `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
     `.agent/handoff.md`. Nothing else. `packages/`, `apps/`, `tests/`,
     `scripts/` and `docs/` stay EMPTY in the range diff.
  2. Apply every slice BYTE-VERBATIM. A defect in reviewer text is a declared
     deviation, never a silent repair.
  3. Commit strictly in the C-order above. Push after C3. Create NO pull request.
  4. NO git worktree, NO mutation, NO timing run, NO commit amended.
  5. `.agent/f083_inventory.md` is NOT touched: R14's `## Q11` is the record and
     this round adds nothing to it.

HANDOFF CONTRACT — what `.agent/handoff.md` must contain at C3. Write it
yourself from what you measure; nothing here is a slice.
  · Feature, the round being closed (R14) and the fact that this is a record
    round that ends the session. Branch. The reviewed range a677c3ba..94e6c353
    and the verdict PASS.
  · What R14 delivered, in one short paragraph: `## Q11`'s three uncapped
    `standard` samples and their spread, read from the section, not recalled.
  · The state of the feature in one short paragraph: `remedy ci` cannot complete
    `standard` today, because `scripts/remedy_pytest_runner.py` defaults
    `REMEDY_PYTEST_TIMEOUT_SEC` to 600 and R13 measured three kills at exit 124
    out of three attempts. No timeout fix, no budget stage, no determinism stage
    and no ceiling exist yet.
  · This round's own per-commit changed-files table and every gate value below.
    C3 cannot table its own SHA or insertion count (R-0371, R-0149); say so.
  · The open-finding set as you MEASURE it at C1, with max and next free id.
  · NEXT SESSION — FIRST ACTIONS, in this order and numbered, because the
    self-drive protocol requires a handoff to name Phase 1 rule 1 before rule 2
    (R-0347): first read `.agent/STOP` from disk and end if it exists; then run
    the Open PR Gate; only then start R15 as the plan states it. Report what
    `.agent/STOP` and the open-PR list read at this handoff.
  · The item-status table covering every C-item and every gate.
  · Over a cap, name BOTH caps and the mandated content that caused it (R-0462,
    DECISION D15). Sections are never dropped to meet a cap.
  · The Fortschritt line, verbatim, at the end.

--- BEGIN SLICE RECORD-R14 --- (APPEND to .agent/live_review.md, C1. The blank line INSIDE this slice, between the gate line and the finding, is part of it.)
Gate: R14 — PASS. The reviewer re-ran all fifteen gates itself at 94e6c353 from the repository root and all fifteen reproduce. TRANSPORT: `.agent/authored/f083-r14.md` and `.agent/last_block.md` are byte-equal at sha256 9ece6420fe5f8eba over 27455 bytes and 301 lines, each equal to its committed blob at C0a and C0b, and 301 is under the 400-line cap. C1's prefix property holds with the tail byte-equal to `b"\n" + RECORD-R13` extracted from the COMMITTED authored file by its markers, numstat `6 0`. C2's prefix property holds, its tail begins with exactly one newline and the ordered `## Q11` heading, numstat `76 0`; the file's `^## Q\d` headings read Q1 through Q11, each exactly once, the `## Q5`, `## Q9` and `## Q10` heading lines each still count 1, and C2 added exactly one `^## ` line. C3's `.agent/plan.md` byte-equals its PLAN slice at sha256 fcacccfc3a49961f, 40 lines, `## Goal` and `## Next Steps` present, 0 `- [ ]` lines. Both range gates printed nothing from the repository root: the scoped `a677c3ba..HEAD` diff over `packages/`, `apps/`, `tests/`, `scripts/` and `docs/`, and the provenance `fb9ddf12..HEAD` diff over `packages/` and `scripts/`. Every gate ran as its own process with the exit code read from that process: the four CI suites at 7, 9, 6 and 8 passed and the verification quartet at 70, 21, 15 and 42 passed, all exit 0; the integrity gate reports passed true, fail_count 0, check_count 5, handlers=338; the open set recomputes to 104 registered, 6 `Done:`, 0 `Landed:`, 98 open, max R-0476, next free R-0477, no duplicate id. Insertions 301, 147, 6, 76, 18 and 117, none over 500. THE EVIDENCE WAS CHECKED AGAINST ITS SOURCE RATHER THAN READ: the two R14 sample logs under `.remedy-wt/f083-r14/logs/` end with exactly the summary lines `## Q11` quotes, at 14062 bytes each against the runner's 512 KiB cap; the red control's whole output is the single line `17045 deselected in 3.47s` at exit 5, taken before either sample; and the raw `duration_s` values in `samples.jsonl`, 935.1410913239997 and 916.3571064700009, round to the published 935.14 and 916.36. The finding R14 was ordered to answer is answered in the strict form R-0473 demanded: `standard`'s serial cost now rests on THREE uncapped samples rather than one, 927.72, 935.14 and 916.36 seconds, all exit 0, all reporting the identical `12578 passed, 1 skipped, 4466 deselected`, so the readings time one selection and not three. R-0476's rule was obeyed rather than merely quoted — the published spread of min 916.36, max 935.14 and max−min 18.78 reproduces exactly by subtracting the published bounds, which is what `## Q10`'s `standard` row could not do. R-0475 is RESOLVED: the PLAN applied at C3 names no figure its own C2 could move and points at `## Q11` instead of repeating it. The worker's conduct was correct throughout: the red control ran first, no `run_command=` injection replaced the instrument, every sample went through the production `_run_via_subprocess`, both slices were applied byte-verbatim with no repair, the change set is exactly the six ordered paths, and the 162-line handback declares both caps with the mandated content named as the cause. One defect remains, registered below, and it concerns an action rather than a text.

- R-0477 — Low, A COMMIT WAS AMENDED AND THE REWRITE SURVIVES ONLY IN A CHANNEL THE REPOSITORY DOES NOT KEEP. R14's worker created C4 with the subject `docs(f083): write the R13 handback`, noticed that the convention names the PRODUCING round rather than the round being handed back, and amended the message to `docs(f083): write the R14 handback` before pushing. The correction is right: the file's own content said R14 throughout, and `6af03d95 write the R12 handback` sets the precedent the amended subject follows. Nothing published was rewritten either — `git reflog show refs/remotes/origin/feature/f083-ci-self-check` records the remote moving 6af03d95 to a677c3ba to 94e6c353, each an ancestor of the next, so the only commit the remote ever saw was the amended one and no force was used. Two things nevertheless went wrong. First, guardrail G2 of docs/agents/self_drive_protocol.md reads "Never force-push. No `--force`, no `--force-with-lease`, no history rewrite, no branch deletion" — and `git commit --amend` IS a history rewrite by git's own definition, so a worker meeting a typo in an unpushed subject has a rule that forbids the obvious repair and no stated exception, which is a gap in the rule rather than a lapse by the worker. Second, and this is the part that costs something: the amend is absent from `.agent/handoff.md`. It was reported to the reviewer in the round's final message, alongside the four values the block genuinely routes there — C4's own SHA, C4's own insertion count, the push result and the open-PR list — but those four are routed there because they CANNOT exist inside C4, whereas an amend is an action taken on the repository that a later commit could have recorded. The handback's Deviations section instead reads "Assumptions: none. No slice was repaired; no defect in reviewer text was found", which is true of every clause it makes and still leaves a reader of the repository alone unable to learn that a commit message on this branch was rewritten. Low, not Medium: the rewrite touched an unpublished commit only, the resulting subject is more correct than the one it replaced, the reviewer was told, and no evidence, gate value or measurement is affected. Two standing rules follow. Binding the WORKER: G2's prohibition is read as absolute on PUBLISHED history and as permitting exactly one exception — the message, never the content, of a commit that has not yet been pushed — and any such amend is declared in the next artifact that CAN carry it, which is the next round's record when C4 itself is the amended commit. Binding the REVIEWER: a block that orders a commit whose subject follows a convention NAMES that subject in the bundle, the way this block's own C-items are named, so the worker never has to choose it and never has to repair it. OPEN.
--- END SLICE RECORD-R14 ---

--- BEGIN SLICE PLAN --- (WHOLE FILE replacement of .agent/plan.md, C2)
# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0478. Open findings: the seventy-five carried out
of the F082 record plus R-0448 to R-0477 registered on this branch, of which
R-0456 to R-0459, R-0467, R-0472 and R-0475 are resolved. `.agent/live_review.md`
is the source of truth.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
None in flight. R14 is closed: the reviewer re-ran all fifteen gates at 94e6c353,
issued PASS, resolved R-0475 and registered R-0477. This record round writes that
verdict to disk and ends the session. R15 has not started.

## Next Steps
1. R15 carries a per-stage timeout in the stage table and writes the budget stage
   from the `## Q11` spread, because today's `remedy ci` kills `standard` at the
   runner's 600-second default. R15 also rules on R-0468 from the 26-error ruff
   baseline `## Q10` records, and settles the determinism stage's shape as a
   DECISION. It is the first round of this feature to touch production code
   since fb9ddf12, so it is a SPLIT round and self-certification is forbidden.

## Risks
- `remedy ci` cannot complete `standard` today: `scripts/remedy_pytest_runner.py`
  defaults `REMEDY_PYTEST_TIMEOUT_SEC` to 600 and the stage needs far longer
  serially. Raising that default repo-wide would change every other caller of the
  runner, so R15 carries the timeout on the stage instead. The figures are in
  `## Q11`; this file repeats none of them.
- The determinism suite is already wholly inside `standard` — 850 ids, 0 outside,
  measured at R11 — so a determinism stage would duplicate work unless
  `standard`'s expression is narrowed in the same change.
- 26 ruff errors stand repo-wide (R-0468) and no stage lints. A lint ceiling
  arrives red unless the baseline is recorded first, which `## Q10` does.
- Changing the stage timeout changes what `tests/orchestration/test_ci_run.py`
  and `tests/cli/test_ci_cmd.py` pin. R15 lands the guard and the change in the
  same commit rather than leaving either side unpinned for a round.
--- END SLICE PLAN ---

Done when — run every gate, record its REAL value; a gate you cannot run is reported as not run, never as green:

 1. `pwd` printed FIRST and equal to the repository root. `git status --porcelain`
    EMPTY before the first commit and before C3. `git worktree list` ONE line at
    round start and at handback. `.agent/STOP` ABSENT at both (R-0347).
 2. BASE: `git rev-parse HEAD` before the first commit; report it and whether it
    equals 94e6c353.
 3. TRANSPORT AND SIZE, bytes read in Python: sha256, byte count and line count of
    `.agent/authored/f083-r14-rec.md` and `.agent/last_block.md`; whether the two
    are EQUAL. Report the measured line count and whether it is at or under the
    400-line cap. This block declares no count of its own; yours is the only
    measurement, so report it as a value and not as a comparison.
 4. C1 PREFIX PROPERTY over `<C1>^..<C1>`: `pre` prefixes `post`, and
    `post[len(pre):]` equals `b"\n" + RECORD-R14`, that slice extracted from the
    COMMITTED `.agent/authored/f083-r14-rec.md` by its markers. Report the
    numstat; its deletion column must be 0.
 5. GATE — `.agent/f083_inventory.md` IS UNTOUCHED: `git diff --name-only
    94e6c353..HEAD -- .agent/f083_inventory.md` must print NOTHING, and the
    file's `^## Q\d` heading count must still be 11, ordered Q1 through Q11.
 6. C2 PLAN byte-equals the PLAN slice as a whole file — report sha256, line count
    (under 50), `## Goal` and `## Next Steps` present, no `- [ ]` line, and the
    count of numbered items under `## Next Steps`.
 7. GATE — THE CI SUITES ARE UNDISTURBED, each its own process, REAL exit code
    from the process (R-0438), each via `python3 -m pytest <path> -q`:
    `tests/orchestration/test_ci_stages.py` [7, 0];
    `tests/orchestration/test_ci_stage_selection.py` [9, 0];
    `tests/cli/test_ci_cmd.py` [6, 0]; `tests/orchestration/test_ci_run.py` [8, 0].
 8. GATE — VERIFICATION, each run separately, REAL exit code from the process:
    `tests/ui_server/test_dashboard_contract.py` [70, 0];
    `tests/regression/test_resource_safety.py` [21, 0];
    `tests/orchestration/test_integrity_gate.py` [15, 0]; canary
    `tests/cli/test_golden_path.py` [42, 0].
 9. GATE — NOTHING ELSE MOVED: `git diff --name-only 94e6c353..HEAD -- packages/
    apps/ tests/ scripts/ docs/` must print NOTHING. Report it as a measured
    list, and confirm you ran it from the repository root — at the wrong root it
    is vacuous.
10. GATE — INTEGRITY, in Python because the `remedy` CLI is denied here (R-0408):
    `python3 -c "from packages.orchestration.integrity_gate import
    run_integrity_checks, export_integrity_json; import json;
    print(json.dumps(export_integrity_json(run_integrity_checks())))"` — report
    `passed`, `fail_count`, `check_count`, every check's status, and the
    `handler_import` message [BASE: handlers=338; this round adds no handler].
11. GATE — OPEN SET at HEAD: count `^- R-\d+ — ` paragraphs, `^Done: R-\d+ — `
    and `^Landed: R-\d+ — ` lines; report all three, registered-minus-done, max
    id, next free id, any duplicate. Reviewer measured 104 / 6 / 0, open 98, max
    R-0476 at BASE and expects 105 / 6 / 0, open 99, max R-0477, next free
    R-0478. Report what you MEASURE.
12. CHANGE SET at C2 — FOUR paths, `.agent/handoff.md` being written by C3 and so
    absent from any measurement preceding it: `git diff --name-only
    94e6c353..HEAD`. Report the list and count; name `.agent/handoff.md` the
    fifth path C3 adds.
13. GATE — NO COMMIT WAS AMENDED (R-0477): report `git reflog show
    refs/remotes/origin/feature/f083-ci-self-check` limited to its newest few
    entries after the push, and confirm every entry is an ancestor of the one
    above it. Confirm in one sentence that you ran no `git commit --amend`, no
    `git rebase` and no `git reset` this round.
14. Insertions (`+` column only) for C0a through C2 — report each; none over 500.
    C0b is a verbatim single-`.agent/`-file rewrite, AGENTS.md-exempt; report it
    anyway. C3's own count cannot exist inside C3 (R-0149): final message.

The push result, post-C3 clean-tree reading and open-PR list postdate C2, so per
R-0449 and R-0452 they are NOT ordered into the handoff: run `git push -u origin
feature/f083-ci-self-check` after C3, create no PR, report all three in the final
message.

Fortschritt, verbatim, for the end of the handoff:

Fortschritt: 48 % (F083 beansprucht · R1 bis R7 und R9 bis R14 PASS, R8 FAIL auf einem roten ruff-Gate und in R9 repariert · Stage-Tabelle, Stage-Runner, die `remedy ci` CLI-Naht und die Selektionstests samt Live-Wächter als Code gelandet · die serielle Kosten von `standard` stehen jetzt mit drei Samples fest, und damit ist gemessen statt vermutet, dass `remedy ci` seine grösste Stage heute nach 600 Sekunden abschneidet · noch keine Determinismus- oder Budget-Stage, kein Ceiling, kein Timeout-Fix, keine hosted workflows) — Rundenzahl gemessen, Prozentwert geschätzt

If a GATE is RED, or anything here contradicts what you find on disk: finish the
commit you are in, write the handoff naming the exact blocker, end. Do not widen
scope to route around it (G8).
──────────────────────────────────────────────────────────────────────────────
