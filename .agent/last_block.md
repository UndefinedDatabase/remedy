── STEP R16-REC — T2_F083 CI self-check — RECORD ROUND, session-closing ──────
Goal:        Write the R15 verdict and its two findings to disk, point the plan
             at R17, and end the session. This round takes no measurement, runs
             no timing sample, writes no ceiling, no budget stage and NO
             production code.

Bundle:      FIVE commits, in this order, with these exact subjects:
  C0a `docs(f083): save the R16 record block verbatim` — THIS ENTIRE BLOCK,
      byte-verbatim, to `.agent/authored/f083-r16-rec.md`.
  C0b `docs(f083): mirror the R16 record block into last_block` —
      `.agent/last_block.md` becomes a byte-identical copy of that file.
  C1  `docs(f083): record the R15 PASS and register three findings` — the
      RECORD-R15 append at EOF of `.agent/live_review.md`, nothing else.
  C2  `docs(f083): point the plan at the R17 budget stage` — `.agent/plan.md`
      replaced as a WHOLE FILE by the PLAN slice.
  C3  `docs(f083): write the R16 record handback` — `.agent/handoff.md` alone.
Change:      Exactly five files: `.agent/authored/f083-r16-rec.md`,
             `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
             `.agent/handoff.md`. NO code path is touched by this round.
Constraints:
  1. Apply every slice BYTE-VERBATIM. If a FROM string is not found exactly
     once, STOP, commit nothing further, write the handoff naming the slice and
     what you found instead (G8). Never repair a slice yourself.
  2. Do NOT touch `.agent/f083_inventory.md`, any file under `packages/`,
     `apps/`, `tests/`, `scripts/` or `docs/`. This round is state-only.
  3. No `git commit --amend`, `git rebase`, `git reset`, force push or PR
     (R-0477, G2). The subjects above are given so you never choose one.
Slice convention: every slice is delimited by its own `--- BEGIN SLICE <NAME>
---` and `--- END SLICE <NAME> ---` markers, which are transport only and NEVER
reach a target file. EACH MARKER IS EXACTLY ONE LINE: a slice's content starts
on the line AFTER its BEGIN marker and ends on the line BEFORE its END marker,
and every blank line between those two is part of the content. The named units
are RECORD-R15 and PLAN. A slice with no FROM: line is an EOF-APPEND:
concatenate its content to the target's bytes EXACTLY as given — its leading
blank line is part of it — and change nothing already in the file.
--- BEGIN SLICE RECORD-R15 --- (EOF-APPEND to .agent/live_review.md, C1)

Gate: R15 — PASS. The reviewer re-ran all fifteen R15 gates itself at 2c1240ce from the repository root and all fifteen reproduce. TRANSPORT, proved against the reviewer's OWN scratchpad original rather than by digest fallback (§4.9): `.remedy-wt/f083-r15-block.md`, the committed `.agent/authored/f083-r15.md` and the committed `.agent/last_block.md` are all three byte-equal at sha256 ed21a4676a8fb162 over 23399 bytes and 400 lines, and 400 is AT the 400-line cap. C1's prefix property holds with the tail byte-equal to the RECORD-R14REC slice extracted from the COMMITTED authored file by its markers, 3603 bytes, numstat `4 0`. C2's change set is EXACTLY the four ordered code paths and `scripts/remedy_pytest_runner.py` is not among them. C3's `.agent/plan.md` byte-equals its PLAN slice at sha256 890c56124e010f31, 33 lines, `## Goal` and `## Next Steps` present, 0 `- [ ]` lines. `.agent/f083_inventory.md` is untouched across the range and its `^## Q\d` headings still read Q1 through Q11. THE CODE WAS RE-DERIVED RATHER THAN READ: the reviewer applied its own block's twenty slices to a clean worktree at 54d83919 and byte-compared the result against every committed file — `ci_stages.py`, `ci_run.py`, `test_ci_run.py`, `test_ci_stages.py`, `.agent/live_review.md` and `.agent/plan.md` are all six byte-identical to the reviewer's independent derivation, which is what proves the worker's two aborted applier passes left no residue. Every gate ran as its own process with the exit code read from that process: the four CI suites at 10, 9, 6 and 10 passed and the verification quartet at 70, 21, 15 and 42 passed, all exit 0; `python3 -m ruff check .` from the repository root against the repository's own `pyproject.toml` ends `Found 26 errors.` at exit 1, EQUAL to the `## Q10` baseline, so the round added no lint error; the integrity gate reports passed true, fail_count 0, check_count 5, handlers=338; the open set recomputes to 105 registered, 6 `Done:`, 0 `Landed:`, 99 open, max R-0477, no duplicate id, unchanged as the block predicted. Insertions 400, 368, 4, 95 and 16, none over 500. THE RED CONTROL WAS RE-RUN BY THE REVIEWER, not accepted from the report: setting `timeout_sec=2100` to `600` inside a disposable worktree at HEAD turns `test_ci_stages.py` red at exit 1 with exactly `test_each_budget_is_the_documented_multiple_of_the_measured_maximum` and `test_the_standard_budget_clears_the_runners_default_that_killed_it` failing, so the budget guards can fail and their green is worth something. The worker's conduct was correct throughout: every slice applied byte-verbatim with none repaired, no `Done:` paragraph of its own, the change set exactly the ordered paths, both aborted passes restored with `git show` rather than the `git reset` constraint 3 forbids, and all three deviations declared. What R15 delivered is what it promised and no more: each stage carries a budget derived by the published rule from the published maxima, the budget reaches the runner process as its environment variable, and `standard` at 2100 s clears the 935.14 s it was measured at. Two defects remain and BOTH belong to the reviewer, registered below.

- R-0478 — Medium, A GATE NAMED FOUR TEST PATHS THAT DO NOT RESOLVE ON DISK, AND BUYING BLOCK-CAP HEADROOM IS WHY. The R15 block's gate 9 ordered `test_dashboard_contract.py`, `test_resource_safety.py` and `test_integrity_gate.py` as bare basenames and closed with the sentence "Paths as gate 8 names them". Gate 8 names four paths and not one of them is any of these three, so the pointer resolves to nothing and the ordered command line is a basename with no directory. The worker ran `pytest tests/cli/test_dashboard_contract.py`, got EXIT 4 and the message that the file or directory was not found, recognised it as the vacuous-gate class, globbed the real paths and re-ran them green — the honest response, and the reason this cost the round nothing. It could have cost the round everything: `pytest <missing path>` exits 4 and reports NO failure, so a worker reading exit codes less carefully would have recorded a gate that never executed a test as an unremarkable non-zero, which is precisely finding R-0438 and precisely what a self-check feature exists to prevent. Medium, not Low, because the gate whose paths evaporated is the VERIFICATION quartet, the one that stands between a scoped round and a broken repository. The cause is nameable and is the part worth keeping: the paths were full and correct in the draft, and they were shortened to basenames in the final trimming pass that brought the block from 403 lines down to the 400-line cap of docs/agents/planner_reviewer_prompt.md §3 item 1. Standing rule, binding the reviewer: a gate's PATHS, commands and flags are never the material cut to meet the block cap — they are the load-bearing bytes of the only thing a round is verified by. When a block is over cap, cut prose, cut a FROM/TO to its changed lines, or split the round; and a block that has been trimmed at all re-reads every gate's paths afterwards and resolves each one on disk before emission, because the trimming pass is exactly when they die. OPEN.

- R-0479 — Low, A GENERATED TEST FILE APPEARS UNTRACKED IN THE WORKING TREE WHILE THE SUITE RUNS, AND TWO GATES READ THE REPOSITORY AS DIRTY WHILE IT IS THERE. Measured, not inferred: while `tests/regression/test_resource_safety.py` was running in this repository, the reviewer ran the integrity gate and `ruff` against the primary checkout and read `relevant_untracked` FAIL with the message `1 relevant untracked: tests/regression/test_wrapper_slow_1014301_ijaza9_1.py`, together with `Found 27 errors.` from ruff. Both readings were taken again after that suite finished and both returned to their true values — `relevant_untracked` pass with `untracked=0, relevant=0`, and `Found 26 errors.` — and `git status --porcelain` was EMPTY before the suite, empty after it, and the named file is absent from the tree now. Nothing in R15 caused it and no committed artefact is affected; the contaminated readings were the reviewer's own, taken concurrently, and they are corrected in the gate paragraph above rather than left standing. Low because it corrupts no commit and survives no suite run. Not Nil, because two of this repository's own health checks — the integrity gate's untracked check and any lint ceiling counting errors repo-wide — report a clean repository as dirty for as long as a suite is in flight, and F083 exists to give this repository a CI whose green means something. A CI that runs its own integrity gate concurrently with its test stages would read that failure as real. Standing rule, binding every role: a gate that reads WORKING-TREE state — `git status --porcelain`, the integrity gate's untracked check, a repo-wide lint count — is run when no test suite is executing against the same checkout, and a reading taken concurrently with one is reported as contaminated rather than as a value. Whether the generator should clean up after itself, and whether `relevant_untracked` should ignore this name class, is a question for the budgets stage that will have to run these checks in a real sequence; it is NOT ruled here and no fix is ordered. OPEN.

- R-0480 — Medium, THE `ui` STAGE IS RED ON A GENUINELY CLEAN CHECKOUT, WHICH IS THE ONE CONDITION THIS FEATURE'S ACCEPTANCE NAMES. Measured, four times, each in a DISPOSABLE worktree created at 2c1240ce and each the FIRST run of that suite in that worktree: `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q` exits 1 with `1 failed, 69 passed`, and the failure is always the same id — `TestJobSummaryCommandContract::test_typescript_compiles`. Its assertion is `assert 1 == 0` over `CompletedProcess(args=['npx', 'tsc', '--noEmit'], returncode=1)`, and the captured stdout is npx's own interactive install notice, the one that warns about running code from un-installed packages. The SECOND run in the SAME worktree exits 0 with `70 passed`, every time. In the primary checkout the suite has been green at every reading this session, because its npx cache is already warm. So the test does not depend on the repository's state at all: it depends on whether `tsc` has already been fetched into the npx cache on that machine, and it pays for the fetch on first use. T2_F083's Acceptance section reads "Clean checkout: `remedy ci` green locally and hosted with the same stage results", and `test_typescript_compiles` carries the `ui_contract` marker, so it is selected by the `ui` stage — which means the stage table this feature has spent fifteen rounds building selects, today, a stage that is RED the first time anyone runs it on a clean machine and GREEN forever after. Medium and deliberately not High or Blocker: no committed artefact is wrong, the production code R15 landed is unaffected, and the condition is invisible on any machine that has run the suite once. Not Low, because it falsifies the feature's own acceptance criterion, because a hosted runner is a clean checkout with a cold cache BY CONSTRUCTION and would meet it on every single run, and because the failure mode is the worst kind for a self-check feature — green on the developer's machine, red in CI, with the difference living in a cache nobody names. This finding RESOLVES the anecdote R-0479 left open: the one-off 69/70 reading observed while authoring R15 was this, not the untracked-file class, and it is recorded here rather than folded into R-0479 because the two have different subjects and only one of them is now named. No fix is ordered here and the diagnosis stops at the measurement: whether the `ui` stage should install the toolchain before it selects, whether `test_typescript_compiles` belongs behind the "UI toolchain absent locally" edge case T2_F083 already documents, or whether the stage should warm the cache and say so, is a design question the budgets-and-stages round owns. OPEN.
--- END SLICE RECORD-R15 ---
--- BEGIN SLICE PLAN --- (WHOLE FILE, replaces .agent/plan.md, C2)
# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0481. `.agent/live_review.md` is the source of
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
the runner's 600-second default. This record round wrote that verdict and the two
findings it produced, and ends the session. R16 has not started.

## Next Steps
1. R16 takes the three items DECISION F083 D3 deferred: the `budgets` STAGE
   T2_F083's Design asks for, which checks documented ceilings and runs the guard
   tests and does not yet exist; a ruling on R-0468 from the 26-error ruff
   baseline `## Q10` records; and the determinism stage's shape settled as a
   DECISION. It is a SPLIT round — the budgets stage is production code — and it
   must honour R-0478 and R-0479 when it writes its gates.

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
  the Acceptance line "clean checkout: green" is not met today. R16 rules on it.
--- END SLICE PLAN ---

Done when — run every gate, record its REAL value; a gate you cannot run is
reported as not run, never as green (G4). EVERY PATH BELOW IS COMPLETE AND
RESOLVES ON DISK AS WRITTEN — run it exactly as given (R-0478):

 1. `pwd` printed FIRST and equal to `/home/decodeux/Repos/remedy`. `git status
    --porcelain` EMPTY before C0a and before C3. `git worktree list` ONE line at
    round start and at handback. `.agent/STOP` ABSENT at both (R-0347).
 2. BASE: `git rev-parse HEAD` before C0a; report it and whether it equals
    2c1240ce.
 3. TRANSPORT AND SIZE, bytes read in Python: sha256, byte count and line count
    of `.agent/authored/f083-r16-rec.md` and `.agent/last_block.md`, and whether
    the two are EQUAL. This block declares no count of its own, so report the
    measured line count as a value — yours is the only measurement.
 4. C1 PREFIX PROPERTY over `<C1>^..<C1>`: `pre` prefixes `post`, and
    `post[len(pre):]` EQUALS the RECORD-R15 slice extracted from the COMMITTED
    `.agent/authored/f083-r16-rec.md` by its markers. Report numstat; the
    deletion column must be 0.
 5. NO CODE MOVED: `git diff --name-only 2c1240ce..HEAD -- packages/ apps/
    tests/ scripts/ docs/` must print NOTHING. Report it as a measured list and
    confirm you ran it from `/home/decodeux/Repos/remedy` — at the wrong root it
    is vacuous.
 6. `.agent/f083_inventory.md` UNTOUCHED: `git diff --name-only 2c1240ce..HEAD
    -- .agent/f083_inventory.md` prints NOTHING, and its `^## Q\d` count is 11.
 7. C2 PLAN byte-equals the PLAN slice as a whole file — report sha256, line
    count (under 50), `## Goal` and `## Next Steps` present, no `- [ ]` line.
 8. GATE — no suite may run against this checkout while gates 9 and 10 are
    taken (R-0479). Run gates 9 and 10 FIRST, before any pytest command in this
    round, and say in the handoff that you did.
 9. GATE — LINT: `python3 -m ruff check .` from `/home/decodeux/Repos/remedy` —
    report its final `Found N errors.` line and exit code. [BASE: 26, exit 1.]
10. GATE — INTEGRITY, in Python because the `remedy` CLI is denied here
    (R-0408): `python3 -c "from packages.orchestration.integrity_gate import
    run_integrity_checks, export_integrity_json; import json;
    print(json.dumps(export_integrity_json(run_integrity_checks())))"` — report
    `passed`, `fail_count`, `check_count`, each check's status and the
    `handler_import` message [BASE: handlers=338; no handler is added here].
11. GATE — THE CI SUITES ARE UNDISTURBED, each its own process, REAL exit code
    read from that process, each `python3 -m pytest <path> -q`:
    `tests/orchestration/test_ci_stages.py` [10, 0];
    `tests/orchestration/test_ci_stage_selection.py` [9, 0];
    `tests/cli/test_ci_cmd.py` [6, 0]; `tests/orchestration/test_ci_run.py`
    [10, 0]. Report the counts you MEASURE.
12. GATE — VERIFICATION, each separately, same form as gate 11:
    `tests/ui_server/test_dashboard_contract.py` [70, 0];
    `tests/regression/test_resource_safety.py` [21, 0];
    `tests/orchestration/test_integrity_gate.py` [15, 0]; canary
    `tests/cli/test_golden_path.py` [42, 0]. On any red, report the FAILED ids
    VERBATIM before you stop — and if the ONLY failure is
    `TestJobSummaryCommandContract::test_typescript_compiles`, that is the known
    R-0480 cold-npx-cache defect: run that ONE suite a second time and report
    BOTH readings with their exit codes, then continue.
13. OPEN SET at HEAD: count `^- R-\d+ — ` paragraphs, `^Done: R-\d+ — ` and
    `^Landed: R-\d+ — ` lines; report all three, registered-minus-done, max id,
    next free id, any duplicate. [BASE: 105 / 6 / 0, open 99, max R-0477.] This
    block registers R-0478, R-0479 and R-0480, so expect 108 / 6 / 0, open 102,
    max R-0480, next free R-0481. Report what you MEASURE.
14. CHANGE SET at C2 — FOUR paths, `.agent/handoff.md` being written by C3 and
    so absent from any measurement preceding it: `git diff --name-only
    2c1240ce..HEAD`. Report the list and count; name `.agent/handoff.md` the
    fifth path C3 adds.
15. Insertions (`+` column only) for C0a through C2 — report each; none over
    500. C0b is a verbatim single-`.agent/`-file rewrite and AGENTS.md-exempt;
    report it anyway. C3's own count cannot exist inside C3 (R-0149).
16. NO COMMIT WAS AMENDED (R-0477): confirm in one sentence that you ran no
    `git commit --amend`, no `git rebase` and no `git reset` this round.

The push, the post-C3 clean-tree reading and the open-PR list postdate C2, so
per R-0449 they are NOT ordered into the handoff: run `git push -u origin
feature/f083-ci-self-check` after C3, create no PR, and report all three in your
final message with C3's own SHA and insertion count.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
feature and round, branch, per-commit changed-files tables, an item-status table
covering C0a through C3 and every gate above, the real verification values, the
open-findings count, and the next expected action, which is R16 as the PLAN
slice states it. Declare any cap overage with its mandated cause (DECISION D15).
End the handoff with this line verbatim:

Fortschritt: 52 % (F083 beansprucht · R1 bis R7 und R9 bis R15 PASS, R8 FAIL auf einem roten ruff-Gate und in R9 repariert · Stage-Tabelle, Stage-Runner, die `remedy ci` CLI-Naht und die Selektionstests als Code gelandet · seit R15 trägt jede Stage ihr gemessenes Wall-Clock-Budget und `standard` wird nicht mehr nach 600 Sekunden abgeschnitten · noch keine budgets-Stage, keine Determinismus-Stage, kein Lint-Ceiling, keine hosted workflows) — Rundenzahl gemessen, Prozentwert geschätzt

If a GATE is RED, or anything here contradicts what you find on disk: finish the
commit you are in, write the handoff naming the exact blocker, end. Do not widen
scope to route around it (G8).
──────────────────────────────────────────────────────────────────────────────
