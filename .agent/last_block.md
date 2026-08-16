# F083 R22 — T003 part 2: the CI documentation, the budget table, and one rule promotion

SPLIT round: it changes `docs/` and `.agent/` only — no file under `packages/`,
`apps/`, `scripts/` or `tests/` is touched. It records the R21 verdict, registers
one Low finding and lands the second half of T003.

Base: `git rev-parse HEAD` MUST print 8336140e before the first commit. If it does
not, stop and report — every gate below is measured against that base.

## What this round writes down

T003's remaining deliverables are the documentation and the runtime budget. Both
already exist as measurements; this round moves them from `.agent/f083_inventory.md`,
which is task scratch, into `docs/`, which is where the built system is described.

THE BUDGET NUMBERS ARE NOT CHOSEN HERE AND MUST NOT BE RE-DERIVED BY HAND. Every
one was measured and is quoted verbatim below with its source section. The rule
that turns a measurement into a budget is `ceil(2 * measured_max / 300) * 300`,
with the factor 2 and the rounding 300 pinned in
`tests/orchestration/test_ci_stages.py`. The reviewer re-computed all five against
the `timeout_sec` values in `CI_STAGES` before emitting this block and all five
agree; your job is to transcribe, not to recalculate.

| Stage | Measured max, seconds | Source | Budget, seconds |
|---|---|---|---|
| fast | 397.45 | `## Q10`, three samples | 900 |
| standard | 935.14 | `## Q11`, three samples | 2100 |
| ui | 8.09 | `## Q10`, three samples | 300 |
| smoke | 11.07 | `## Q10`, three samples | 300 |
| budgets | 1.32 | `## Q12`, three samples | 300 |
| excluded | not run — `runs_in_ci` is False | `## Q10` | 0 |

Two derived figures, also re-computed by the reviewer: the five CI budgets sum to
3900 s, i.e. 65 minutes, which is why `.github/workflows/ci.yml` caps its job at 90;
and the five measured maxima sum to 1353.07 s, i.e. about 22.6 minutes, which is
what a green serial run actually costs on the machine those samples were taken on.

## Slice convention

Every slice is delimited by its own `--- BEGIN SLICE <NAME> ---` and
`--- END SLICE <NAME> ---` markers, which are TRANSPORT ONLY and NEVER reach a
target file. A slice's content begins on the line AFTER its BEGIN marker and ends
on the line BEFORE its END marker, newline included. The slices carried here are
named RECORD-R21, TEMPLATE, QUICKFIND, SYSTABLE and PLAN. A slice with no FROM:
line is an EOF-APPEND. TEMPLATE, QUICKFIND and SYSTABLE are FROM/TO pairs and all
three are APPEND-SHAPED — each TO contains its FROM verbatim (§4.9), so the proof
obligation for each is FROM exactly 1x in the target file before the edit, and each
TO-ONLY line exactly 1x among the lines that commit's diff ADDS. Extract every
slice programmatically from the COMMITTED `.agent/authored/f083-r22.md` by its
markers — never by retyping.

--- BEGIN SLICE RECORD-R21 --- (EOF-APPEND to .agent/live_review.md, C1)

Gate: R21 — PASS. The reviewer re-ran every one of the round's eighteen ordered gates itself, from the repository root at 8336140e, and every measured value equals the one the handback reports. TRANSPORT, by digest over the committed files (§4.9 digest fallback, this being a self-drive session in which the reviewer holds no scratch copy): `.agent/authored/f083-r22.md`'s predecessor `.agent/authored/f083-r21.md` and `.agent/last_block.md` are byte-equal at sha256 f0524ec4a2eae48a over 20628 bytes and 252 lines, and 252 is under the 400-line block cap. C1 is a pure append and was proved so: `.agent/live_review.md` goes 271015 B to 275871 B, the former prefixes the latter, the 4856-byte tail byte-EQUALS the RECORD-R20 slice extracted from the committed authored file by its markers, numstat is `2 0`, and the marker count in the file is 4 both at base and at HEAD, so no transport marker leaked. `.agent/plan.md` byte-equals its PLAN slice at sha256 3e06a8df6d276e06, 2174 bytes, 39 lines under the cap, `## Goal` and `## Next Steps` present, 0 unchecked-box lines. THE GUARDS WERE PROVED LIVE IN THREE DIRECTIONS RATHER THAN ONE, because a guard exercised only on its happy path is a guard nobody has tested and the block ordered only the first of these: in a disposable worktree at HEAD the reviewer moved the `npm ci --prefix apps/ui` step after the `remedy ci run` step and got exit 1 with `1 failed, 4 passed`, the single failure being `test_hosted_workflow_installs_the_ui_toolchain_before_the_run`; added `continue-on-error: true` on a non-comment line and got exit 1 with the single failure `test_hosted_workflow_never_auto_retries`; and appended a real stage marker expression to the run step and got exit 1 with the single failure `test_hosted_workflow_selects_no_tests_of_its_own`. Each mutation reddened its OWN guard and only its own, and restoring the file returned `5 passed` at exit 0. The worktree was removed and pruned; `git worktree list` is one line and `git status --porcelain` is empty at this verdict. A GAP THE ROUND DID NOT COVER WAS CLOSED BY THE REVIEWER RATHER THAN LEFT OPEN: the guards deliberately read the workflow as TEXT and never parse it, which is the right call because PyYAML is in neither `dependencies` nor the `dev` extra, but it means nothing in the round proved the file is well-formed YAML — and a malformed workflow is a hosted CI that silently never runs. The reviewer parsed it with PyYAML as a spot-check: it loads, the job `ci` carries `runs-on: ubuntu-latest` and `timeout-minutes: 90`, `concurrency` is the ref-keyed group with `cancel-in-progress`, the triggers are `push` and `pull_request` both on `main`, and the six steps are in exactly the ordered sequence — checkout, setup-python 3.10 with the pip cache, setup-node 20 with the npm cache keyed on `apps/ui/package-lock.json`, the editable dev install, the UI toolchain install, and `remedy ci run` last. The YAML 1.1 quirk that parses the `on:` key as boolean true is present and is not a defect: GitHub's own parser reads it as the trigger key, as it does in every workflow file. The remaining gates all reproduce: ruff reports `Found 26 errors.` at exit 1 with the breakdown unchanged at 20 I001, 4 F401, 1 F821 and 1 UP035 and the new test file alone `All checks passed!` at exit 0, so the ratchet held across a round that added a file; the new guards are 5 passed; the escape guard is 9 passed, which is the reading that matters most this round because C3 added a test file and a file that escaped every marker-selected stage would be a test CI never runs; the five CI suites are 46 passed, the two budget-stage guard suites 18 passed, and the verification set with the canary 78 passed, every one at exit 0. The range gate holds — `git diff --name-only 35b80d17..HEAD -- packages/ apps/ scripts/` prints nothing — the change set is exactly the seven paths the handback lists, insertions are 252, 180, 2, 52, 56, 14, 63 and 3 with none near 500, the history is linear with no amend, rebase or reset, and the open set recomputes to 112 registered, 9 resolved, 0 landed, 103 open, max R-0484, no duplicate id and no unregistered resolution. The design is right and worth naming: one job calling one `remedy ci run`, with no stage matrix and no marker expression anywhere in the YAML, is the thinnest wrapper that can satisfy the Orchestrator brief, and the guards pin exactly that rather than pinning a shape. Two of the block's own gates were removed before emission because the code contradicted them — a `-m ` absence gate that the legitimate `python3 -m pip` step would have reddened, and a stage-NAME gate that `ui` being a substring of `apps/ui` would have reddened — so this round's guards assert on marker EXPRESSIONS, which is why they are satisfiable and meaningful at the same time. One Low finding is registered against this round, R-0485, and it concerns where a deviation was written down rather than anything that landed wrong.

- R-0485 — Low, A DEVIATION THE WORKER NAMED IN ITS ROUND REPORT REACHED THE HANDOFF ONLY AS A TABLE-CELL ASIDE, AND THE HANDOFF IS THE ONLY RETURN CHANNEL. R21's block ordered the commit sequence C0a through C5, which is seven commits; the round produced eight. The eighth, 8336140e, corrects items 16 and 17 of the handback to their post-C5 readings, because those two were measured at C4 and so omitted `.agent/handoff.md`, the path C5 itself adds to the change set. The commit is right, its reason is right, and refusing to amend was right — constraint 1 forbids it, and this is the R-0149 self-reference the handback template already contemplates. What is wrong is only where the departure is recorded. On disk it appears inside the C5 table's Reason cell and in a trailing sentence of item 17, while the handoff's `## Deviations & assumptions` section lists two other deviations and not this one; the worker's round report to the reviewer, by contrast, listed it first. A round report dies with its session and the handoff does not, so a later reader auditing whether R21 followed its block reads the Deviations section and learns nothing about the extra commit. Low and not Medium because the fact IS on disk, nothing is misstated and no reading is wrong — but R20's handoff declared a strictly smaller procedural departure, a gate run twice, as a numbered deviation, which is the standard this one misses. The fix is not a repair of R21, whose commits are all correct and must not be rewritten: it is the rule promotion C2 of this block performs, adding to `docs/agents/handback_template.md` the requirement that any departure from the block's ordered commit sequence appears in the Deviations section even when the commit table already shows it. A standing rule written only as finding prose binds nothing, which is why this finding names the file it changes and the commit that changes it.
--- END SLICE RECORD-R21 ---
--- BEGIN SLICE TEMPLATE --- (FROM/TO pair, APPEND-SHAPED, docs/agents/handback_template.md, C2)
FROM:
## Deviations & assumptions

Each with justification / assumption_log pointer. `None` if none.
TO:
## Deviations & assumptions

Each with justification / assumption_log pointer. `None` if none.

ANY DEPARTURE FROM THE BLOCK'S ORDERED COMMIT SEQUENCE BELONGS HERE, not only in
the commit table: an extra commit, a dropped one, or a reordering is a deviation
even when it is correct and even when the commit table already shows it (finding
R-0485). A round report dies with its session and this file does not, so a reader
auditing whether a round followed its block reads this section and nothing else.
--- END SLICE TEMPLATE ---
--- BEGIN SLICE QUICKFIND --- (FROM/TO pair, APPEND-SHAPED, docs/README.md, C4)
FROM:
| candidate eval | [candidate-quality-evaluation-v1.md](system/candidate-quality-evaluation-v1.md) | system |
TO:
| candidate eval | [candidate-quality-evaluation-v1.md](system/candidate-quality-evaluation-v1.md) | system |
| CI self-check | [ci-self-check-v1.md](system/ci-self-check-v1.md) | system |
--- END SLICE QUICKFIND ---
--- BEGIN SLICE SYSTABLE --- (FROM/TO pair, APPEND-SHAPED, docs/README.md, C4)
FROM:
| [candidate-quality-evaluation-v1.md](system/candidate-quality-evaluation-v1.md) | Scoring and evaluation of candidate patches |
TO:
| [candidate-quality-evaluation-v1.md](system/candidate-quality-evaluation-v1.md) | Scoring and evaluation of candidate patches |
| [ci-self-check-v1.md](system/ci-self-check-v1.md) | Remedy's own CI: the stage table, the measured runtime budgets, the hosted workflow, and what CI deliberately never runs |
--- END SLICE SYSTABLE ---
--- BEGIN SLICE PLAN --- (WHOLE FILE, replaces .agent/plan.md, C5)
# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0486. `.agent/live_review.md` is the source of
truth for the open set; this file repeats no count of it.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R21 is closed PASS and R22 recorded it. R22 registered R-0485 (Low, a deviation
recorded outside the handoff's Deviations section) and fixed it by rule, not by
rewriting R21: the handback template now requires any departure from the block's
commit sequence to appear there. T003 is COMPLETE — the workflow and its guards
landed at R21, the documentation and the measured runtime budgets at R22.

## Next Steps
1. The integration-gate round: the full suite exactly once, per
   docs/agents/integration_gate.md. It is also the round that records R22's
   verdict and resolves R-0485.
2. Then closure per docs/roadmap/STATUS_closure_protocol.md — evidence job plus a
   FRESH review zip, both mandatory, then the authored STATUS line and the PR.

## Risks
- Hosted wall time is still unmeasured, and the first hosted run is that
  measurement. `standard` needs 935.14 s at its slowest local sample against a
  2100 s budget; a runner with fewer cores may exceed it. Raising `timeout_sec`
  before that evidence exists would be a guess wearing a budget's name.
- The lint ceiling is a RATCHET. Raising it to make a round green converts the
  one honest lint signal in this repository into decoration.
- R-0482 is a live `NameError` on a guard's refusal path, frozen under that
  ceiling rather than fixed, and belongs to a branch of its own.
--- END SLICE PLAN ---

## Change — exactly these paths, nothing beyond them

**C0a** saves this block verbatim to `.agent/authored/f083-r22.md`. **C0b** mirrors
the committed copy over `.agent/last_block.md`. **C1** applies RECORD-R21.
**C2** applies TEMPLATE.

**C3 — the documentation, the new file `docs/system/ci-self-check-v1.md`, the only
file in this commit.** An ist-doc describing what is BUILT, in this repository's
existing `docs/system/` voice — see `docs/system/real-test-execution-v1.md` for the
register. It must contain, in whatever prose you judge clearest:
- a title and a one-paragraph overview: Remedy's own CI is one stage TABLE
  (`packages/orchestration/ci_stages.py`), one RUNNER
  (`packages/orchestration/ci_run.py`), one local command (`remedy ci run`, whose
  seam is `apps/cli/commands/ci_cmd.py`) and one hosted workflow
  (`.github/workflows/ci.yml`) that calls that same command exactly once. The table
  is the single source of truth for what CI means, and the workflow names no stage
  and selects no tests of its own;
- the stage list with what each selects and why it exists, taken from `CI_STAGES`;
- THE RUNTIME BUDGET TABLE, transcribed from the table in this block's "What this
  round writes down" section — every stage, its measured maximum in seconds, its
  source section, and its budget in seconds — plus the rule
  `ceil(2 * measured_max / 300) * 300` and the note that the factor and the
  rounding are pinned in `tests/orchestration/test_ci_stages.py`. State that the
  five CI budgets sum to 3900 s (65 minutes) and that the hosted job caps at 90
  minutes for that reason, and that the five measured maxima sum to 1353.07 s
  (about 22.6 minutes), which is what a green serial run costs on the machine the
  samples came from;
- the exclusions, honestly: `excluded` carries `runs_in_ci=False`, is REPORTED as
  skipped rather than dropped, and its manual command is
  `python3 -m pytest -m real_ollama -q  # needs a running Ollama server`. The
  benchmark stays out of CI on cost grounds;
- the no-retry rule and why: a flaky test is quarantined only by an explicit
  marker change in a reviewed diff, because retries hide rot;
- DECISION F083 D6's consequence: the hosted workflow runs `npm ci --prefix
  apps/ui` before the CI run, because without it the `ui` stage's TypeScript check
  skips hosted and the Acceptance line would be met by a skip rather than a
  compile;
- a section saying WHAT IS NOT MEASURED, rather than leaving it blank: hosted wall
  time. Every number in the budget table was taken on a 24-CPU developer machine
  under pytest 9.0.3; no hosted run has happened yet, and the first one is that
  measurement.
Two constraints on the file. Any relative markdown link it contains must resolve
on disk — check each one. And it must not state a count of roadmap features or of
anything in `docs/roadmap/`; `tests/docs/` pins several such counts and this
document has no business repeating them.

**C4** applies QUICKFIND and SYSTABLE, both to `docs/README.md`, in one commit.
C3 lands BEFORE C4 deliberately: `tests/docs/` asserts that every relative link in
`docs/README.md` resolves, so the index may not point at a file that does not yet
exist.

**C5** applies PLAN. **C6** rewrites `.agent/handoff.md`.

## Constraints

1. Never work on `main`; never force-push; never amend, rebase or reset. No PR is
   created and none is merged.
2. `.agent/live_review.md` is APPENDED to once, at C1. No committed text in it is
   edited. Both the verdict paragraph and the R-0485 registration are
   reviewer-authored text applied verbatim; write no resolution or `Landed:` line
   of your own.
3. No marker line and no `FROM:`/`TO:` label reaches a target file. Every slice is
   extracted from the COMMITTED `.agent/authored/f083-r22.md` by its markers.
4. Nothing under `packages/`, `apps/`, `scripts/` or `tests/` is modified at all —
   this round is `docs/` and `.agent/` only, and gate 8 proves it.
5. The 26 ruff errors are NOT fixed and the lint ceiling is NOT raised.
6. Every disposable worktree is removed and pruned before the handback.
7. If any gate is red, stop at that gate, record its real output verbatim, and hand
   back. Do not widen the change set to route around it.

## Done when — every command run from /home/decodeux/Repos/remedy, each its own
## unpiped process, each exit code read from that process

1. `pwd` printed FIRST. `git status --porcelain` EMPTY before the first commit and
   before C6. `git worktree list` ONE line at round start and at handback.
   `.agent/STOP` ABSENT at both.
2. `git rev-parse HEAD` at round start EQUALS 8336140e.
3. `.agent/authored/f083-r22.md` and `.agent/last_block.md` byte-equal; report
   their sha256, byte count and line count.
4. `.agent/live_review.md` at C1: the pre content PREFIXES the post content, the
   tail byte-EQUALS the RECORD-R21 slice as extracted from the committed authored
   file by its markers, and `git show --numstat` has deletion column 0. Also report
   the count of `--- BEGIN SLICE` in the file at base and at HEAD; they must be
   equal, which is the proof no transport marker leaked.
5. TEMPLATE pair proof at C2: the FROM string occurred exactly 1x in
   `docs/agents/handback_template.md` before C2, and each TO-ONLY line occurs
   exactly 1x among the lines C2's diff ADDS. Report both counts.
6. QUICKFIND and SYSTABLE pair proofs at C4, separately: each FROM occurred exactly
   1x in `docs/README.md` before C4, and each pair's TO-ONLY line occurs exactly 1x
   among the lines C4's diff ADDS. Report all four counts.
7. `.agent/plan.md` byte-equals the PLAN slice; report its sha256, line count
   (under 50), that `## Goal` and `## Next Steps` are present, and its count of
   unchecked-box lines.
8. `git diff --name-only 8336140e..HEAD -- packages/ apps/ scripts/ tests/` prints
   NOTHING. Report that it printed nothing.
9. `python3 -m ruff check .` — report the `Found N errors.` line and the exit code.
   Expected 26 errors at exit 1, unchanged. Take this reading AT C6 and report the
   commit you took it at rather than the word "before"; no commit in this round
   touches a Python file, so C6 is simply the last commit available.
10. `python3 -m pytest tests/docs/ -q` — the docs-round gate. Report the passed
    count and exit code. Take this reading AFTER C4, the commit that changes
    `docs/README.md`, and say which commit you took it at: a reading taken earlier
    would not be a reading of the change it exists to gate.
11. Every relative markdown link in the new `docs/system/ci-self-check-v1.md`
    resolves on disk. Report the list of link targets you checked and that none was
    missing; if the file contains no relative link, report that explicitly rather
    than reporting a vacuous pass.
12. `python3 -m pytest tests/orchestration/test_ci_workflow.py -q` — the R21 guards,
    still green. Report the passed count and exit code.
13. `python3 -m pytest tests/orchestration/test_ci_budgets.py
    tests/orchestration/test_ci_stages.py
    tests/orchestration/test_ci_stage_selection.py tests/cli/test_ci_cmd.py
    tests/orchestration/test_ci_run.py -q` — report the passed count and exit code.
14. `python3 -m pytest tests/regression/test_resource_safety.py
    tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q` —
    the verification set and the canary. Report the passed count and exit code.
15. The budget table in `docs/system/ci-self-check-v1.md` agrees with the code.
    Import `CI_STAGES` from `packages.orchestration.ci_stages`, and for every stage
    with `runs_in_ci` True confirm that the budget the document states for it
    equals that stage's `timeout_sec`. Report each stage name with the two numbers
    and whether they agree. Read the numbers OUT of the document text; do not
    retype them from this block.
16. The open set, recomputed from `.agent/live_review.md` at HEAD: count every
    registration paragraph, every resolution line and every `Landed:` line; report
    registered, resolved, landed, open, the maximum id, the next free id, and
    whether any id repeats. Expected: 113 registered, 9 resolved, 0 landed, 104
    open, max R-0485, next free R-0486 — one MORE registration than the round
    started with, because RECORD-R21 registers R-0485 and resolves nothing.
17. `git diff --name-only 8336140e..HEAD` — report the full path list. Nothing
    outside the paths this block names may appear.
18. `git log --numstat` over the round — report the insertion count of every commit.
    None may exceed 500. Report the total number of commits the round produced.
19. Confirm in one sentence that no `git commit --amend`, `git rebase` or
    `git reset` was run this round.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, branch, every commit SHA, a changed-files table per commit, the real
measured value of every gate above in an item-status table where each ordered item
appears exactly once with `done`, `skipped` or `deviated`, the open-findings count,
declared deviations with their causes, and the next expected action. Apply the rule
C2 of this very block adds to that template: if this round departs from the ordered
commit sequence C0a..C6 in any way — an extra commit, a dropped one, a reordering —
that departure is named in the `## Deviations & assumptions` section and not only
in the commit table. If the file exceeds 60 lines, carry a "Deviations, declared"
line naming its line count and the mandated content that caused the overage
(DECISION D15).

THE NEXT ACTION THIS HANDOFF NAMES, in this order: (1) read `.agent/STOP` from
disk, self-drive Phase 1 rule 1, before anything else; (2) run the Open PR Gate,
`gh pr list --state open --json number,headRefName,baseRefName,isDraft`; (3) then
the integration-gate round per docs/agents/integration_gate.md — the full suite
exactly once — which is also the round that records THIS round's verdict, which
lives only in the round report until it does, and that resolves R-0485. Repeat this
Fortschritt line verbatim as the handoff's last line:

Fortschritt: 90 % (F083 beansprucht · R1 bis R7 und R9 bis R21 PASS, R8 FAIL auf einem roten ruff-Gate und in R9 repariert · T001, T002 und T003 fertig: Stage-Tabelle, Stage-Runner, die `remedy ci` CLI-Naht, die gemessenen Stage-Budgets, die gehostete Workflow-Datei als dünner Wrapper mit ihren Guards, und jetzt die Doku samt Laufzeit-Budget-Tabelle · D4 schliesst eine eigene Determinismus-Stage aus, D5 friert die 26 ruff-Fehler ein, D6 macht den lokalen tsc-Compiler tragend · offen sind nur noch das Integration Gate und die Closure · gehostete Laufzeit ist weiterhin NICHT gemessen) — Rundenzahl gemessen, Prozentwert geschätzt

Then `git push -u origin feature/f083-ci-self-check` and report its result, the
post-push `git status --porcelain` and the open-PR list in the round report.
