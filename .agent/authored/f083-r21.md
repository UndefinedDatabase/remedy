# F083 R21 — T003 part 1: the hosted workflow and the guards that keep it thin

SPLIT round: it creates production CI configuration under `.github/` and a test
under `tests/`, so the worker executes and the reviewer gates. It records the R20
verdict and lands the first half of T003.

Base: `git rev-parse HEAD` MUST print 35b80d17 before the first commit. If it
does not, stop and report — every gate below is measured against that base.

## The one design choice in this round

T2_F083's Orchestrator brief says "Keep hosted workflows thin wrappers — reject
workflow logic that isn't in the entrypoint", and its Design says the hosted files
"mirror the same stages by calling the same entrypoint (one source of truth for
what CI means)". The thinnest wrapper that satisfies both is ONE job calling
`remedy ci run` ONCE, with no stage matrix and no stage name in the YAML at all:
`CI_STAGES` already decides what runs, in what order and under which budget, and
`_cmd_ci_run` in `apps/cli/commands/ci_cmd.py` already prints the summary and
exits on `ci_exit_code`. A matrix over stage names would copy the table into YAML
and give CI a second opinion about what CI means — the drift the `ci_stages`
module docstring exists to prevent. Reverse by adding a matrix and a `--stage`
argument in the same commit.

`npm ci --prefix apps/ui` is a STEP OF THE JOB, not a stage of the table, because
DECISION F083 D6 made the toolchain a PRECONDITION of the `ui` stage rather than
part of it: without it `test_typescript_compiles` skips hosted too and the
Acceptance line is met by a skip rather than by a compile. Its position before the
`remedy ci run` step is load-bearing, and C3 pins it.

WHAT THIS ROUND DOES NOT MEASURE, said rather than left blank: hosted wall time.
Every number in `## Q9` through `## Q12` was taken on this 24-CPU machine, and
`standard` needs 935.14 s serially at its slowest sample against the 2100 s
`timeout_sec` the table already carries. A hosted runner with fewer cores may
exceed it. The first hosted run is that measurement; this round neither predicts
it nor tunes a budget to a guess. The job cap is set ABOVE the sum of the stage
budgets — `sum(s.timeout_sec for s in CI_STAGES if s.runs_in_ci)` is 3900 s, i.e.
65 minutes — so a slow stage times out at ITS OWN budget with exit code 124 and a
`timed out` note, instead of the job dying first and naming no stage.

## Slice convention

Every slice is delimited by its own `--- BEGIN SLICE <NAME> ---` and
`--- END SLICE <NAME> ---` markers, which are TRANSPORT ONLY and NEVER reach a
target file. A slice's content begins on the line AFTER its BEGIN marker and ends
on the line BEFORE its END marker, newline included. The slices carried here are
named RECORD-R20 and PLAN. A slice with no FROM: line is an EOF-APPEND: its bytes
are appended to the end of the named file and nothing already in that file is
edited. There is no FROM/TO pair in this block. Extract every slice
programmatically from the COMMITTED `.agent/authored/f083-r21.md` by its markers —
never by retyping.

--- BEGIN SLICE RECORD-R20 --- (EOF-APPEND to .agent/live_review.md, C1)

Gate: R20 — PASS. The reviewer re-ran every one of the round's eighteen ordered gates itself, from the repository root at 35b80d17, and every measured value equals the one the handback reports. TRANSPORT, by digest over the committed files rather than against a scratchpad original, because this is a self-drive session in which the reviewer holds no scratch copy (§4.9 digest fallback, stated so the evidence chain stays honest): `.agent/authored/f083-r20.md` and `.agent/last_block.md` read from HEAD are byte-equal at sha256 8f77255a7c0328c8 over 24374 bytes and 276 lines. C1 and C4 are both pure appends and were proved as such rather than believed: `.agent/live_review.md` goes 263322 B to 269472 B at C1 with the former a prefix of the latter and the 6150-byte tail byte-EQUAL to the RECORD-R19 slice extracted from the committed authored file by its markers at numstat `6 0`, then 269472 B to 271015 B at C4 with the 1543-byte tail byte-EQUAL to the RESOLVE slice at numstat `4 0`; the deletion column is 0 both times, so no committed text was edited. The CHECKLIST pair is APPEND-SHAPED as declared and was checked that way rather than asserted: its TO contains its FROM verbatim, the FROM string occurred exactly 1x in `docs/agents/planner_reviewer_prompt.md` before C2 and exactly 1x after it, all 17 TO-ONLY lines occur exactly 1x each among the 17 lines C2's diff adds, C2 adds no other line, and no marker line and no FROM:/TO: label reached the file. `.agent/plan.md` byte-equals its PLAN slice at sha256 900ce257188f5781, 2149 bytes, 39 lines under the 50-line cap, with `## Goal` and `## Next Steps` present and 0 unchecked-box lines. THE FIX WAS PROVED IN BOTH DIRECTIONS RATHER THAN ON ITS HAPPY PATH, because a skip guard exercised only one way is a guard nobody has tested: in the primary checkout `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q` is 70 passed at exit 0 and `test_typescript_compiles` is PASSED by name, and the compiler it resolved is the project's own — `apps/ui/node_modules/.bin/tsc --version` prints `Version 5.9.3`, which is the whole point of D6 and not the nine-year-old `tsc@2.0.4` stub the old `npx` form was grading. In a disposable worktree at HEAD where `apps/ui/node_modules` is absent by construction the same test is SKIPPED at exit 0 with a message naming the missing directory and the exact command `npm ci --prefix apps/ui`, which is the intended outcome; that worktree was removed and pruned, `git worktree list` is one line and `git status --porcelain` is empty at this verdict. The remaining gates all reproduce: `python3 -m ruff check .` reports `Found 26 errors.` at exit 1 with the breakdown unchanged at 20 I001, 4 F401, 1 F821 and 1 UP035, and the edited test file alone reports `All checks passed!` at exit 0, so the ratchet held; the integrity gate is passed true, fail_count 0, check_count 5; the five CI suites are 46 passed, `tests/docs/` is 295 passed, and the verification set with the canary is 78 passed, every one at exit 0. The range gate holds — `git diff --name-only 59d7d341..HEAD -- packages/ apps/ scripts/` prints nothing — the change set is exactly the nine paths the block names and no more, per-commit insertions are 276, 202, 6, 17, 9, 4, 46, 16 and 106 with none near 500, and the history is linear with no amend, rebase or reset. The open set recomputes mechanically from the record rather than being carried forward: 112 registered, 9 resolved, 0 landed, 103 open, maximum R-0484, next free R-0485, no duplicate id, and every resolved id is a registered id. The `Amended: R-0480` paragraph is correctly NOT counted as a registration, which is the property it was deliberately shaped to have. Three declared deviations, all honest and none a defect, and two of them are the worker correctly refusing to follow reviewer text off a cliff: the ordered "one-line WHY comment" carried about 148 characters of mandated content against a 120-character ruff ceiling, so two lines of 101 characters or fewer is the fewest that carries it without reddening the very lint gate the same block freezes; and the docs gate was run a second time AFTER C5, because C5 is the commit that changes `docs/roadmap/**` and a reading taken before it would not be a reading of the change it exists to gate. That second one is precisely the class of defect pre-emission checklist item 13 describes, applied by the worker in the same round that put item 13 on disk. ONE IMPRECISION IS RECORDED AND IS NOT A FINDING: gate 8 asked for ruff's "final line" expecting `Found 26 errors.`, but ruff's actual final line is its fixable-count hint and `Found 26 errors.` is the line above it. The reviewer's expectation was the imprecise half; the count, the breakdown and the exit code the worker reported are exact and re-measured. No finding is registered against this round.
--- END SLICE RECORD-R20 ---
--- BEGIN SLICE PLAN --- (WHOLE FILE, replaces .agent/plan.md, C4)
# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0485. `.agent/live_review.md` is the source of
truth for the open set; this file repeats no count of it.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R20 is closed PASS and R21 recorded it. R21 landed the first half of T003: the
hosted workflow `.github/workflows/ci.yml`, a thin wrapper that installs the
Python and the UI toolchain and then calls `remedy ci run` once, plus the guard
tests pinning its load-bearing properties — it calls the entrypoint, it selects
no tests of its own, it installs the UI toolchain before the run, and it never
auto-retries.

## Next Steps
1. T003's second half: the CI documentation under `docs/`, registered in the
   `docs/README.md` index, carrying the runtime-budget table from the measured
   data in `.agent/f083_inventory.md` `## Q9` through `## Q12` and saying plainly
   that hosted wall time is NOT measured — only the local samples are.
2. Then the integration-gate round, then closure per
   docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Hosted wall time is unmeasured. `standard` needs 935.14 s at its slowest local
  sample against a 2100 s budget, and a hosted runner with fewer cores may exceed
  it. The first hosted run is the measurement; raising `timeout_sec` before that
  evidence exists would be a guess wearing a budget's name.
- The lint ceiling is a RATCHET. Raising it to make a round green converts the
  one honest lint signal in this repository into decoration.
- R-0482 is a live `NameError` on a guard's refusal path, frozen under that
  ceiling rather than fixed, and belongs to a branch of its own.
--- END SLICE PLAN ---

## Change — exactly these paths, nothing beyond them

**C0a** saves this block verbatim to `.agent/authored/f083-r21.md`. **C0b**
mirrors the committed copy over `.agent/last_block.md`. **C1** applies RECORD-R20.

**C2 — the hosted workflow, the new file `.github/workflows/ci.yml`, the only
file in this commit.** Write a workflow that:
- is named `CI`, triggers on `push` to `main` and on `pull_request` targeting
  `main`, and carries a `concurrency` group keyed on the ref with
  `cancel-in-progress: true`;
- has exactly ONE job, id `ci`, on `ubuntu-latest`, with `timeout-minutes: 90`;
- whose steps are exactly these, in this order: `actions/checkout@v4`;
  `actions/setup-python@v5` with python-version `'3.10'` and `cache: pip`;
  `actions/setup-node@v4` with node-version `'20'`, `cache: npm` and
  `cache-dependency-path: apps/ui/package-lock.json`; a step running
  `python3 -m pip install -e ".[dev]"`; a step running `npm ci --prefix apps/ui`;
  and a final step running `remedy ci run`;
- carries a comment directly above the `npm ci` step naming DECISION F083 D6 and
  stating that without this install the `ui` stage's tsc check skips hosted too;
- carries a comment naming T2_F083's no-retry rule and why the job caps at 90
  minutes while the stage budgets sum to 65;
- contains NO `continue-on-error`, no retry action, no `--stage`, no `pytest`
  invocation of its own, and no stage `marker_expression` from `CI_STAGES`.
Python `'3.10'` is not a preference: it is this repository's `requires-python`
floor in `pyproject.toml` and the version every measurement in
`.agent/f083_inventory.md` was taken on. `[dev]` is the extra that carries pytest.

**C3 — the guards, the new file `tests/orchestration/test_ci_workflow.py`, the
only file in this commit.** The module resolves the workflow from its own
location, reads it as TEXT, and asserts. It MUST NOT use `yaml.safe_load`: PyYAML
is in neither `dependencies` nor the `dev` extra in `pyproject.toml`, so a
YAML-parsing guard would raise ImportError on exactly the clean checkout it exists
to protect. Tests, each with a one-line docstring giving its reason:
1. the workflow file EXISTS at `.github/workflows/ci.yml`;
2. the text contains `remedy ci run`;
3. it selects no tests of its own: for every stage in `CI_STAGES`, imported from
   `packages.orchestration.ci_stages` and never retyped, that stage's
   `marker_expression` does not occur in the text, and neither `--stage` nor
   `pytest` occurs. Assert on the marker EXPRESSION and never on the stage NAME —
   `ui` is a substring of `apps/ui`, so a name-based assertion is red by
   construction. Do NOT assert on the token `-m `: the pip step legitimately
   contains `python3 -m pip`.
4. the UI toolchain is installed BEFORE the run: `npm ci --prefix apps/ui` occurs
   exactly once, `remedy ci run` occurs exactly once, and the index of the former
   is less than the index of the latter. Docstring names DECISION F083 D6.
5. the workflow never auto-retries: none of `continue-on-error`, `retry`,
   `max_attempts` occurs — checked over the NON-COMMENT lines only, i.e. lines
   whose first non-space character is not `#`, so the workflow may explain its own
   no-retry rule without tripping the guard that enforces it. The docstring says
   that in one line and cites T2_F083's "retries hide rot".
The file must be ruff-clean under this repository's own configuration.

**C4** applies PLAN. **C5** rewrites `.agent/handoff.md`.

## Constraints

1. Never work on `main`; never force-push; never amend, rebase or reset. No PR is
   created and none is merged.
2. `.agent/live_review.md` is APPENDED to once, at C1. No committed text in it is
   edited. Write no resolution or `Landed:` line of your own — RECORD-R20 resolves
   nothing and registers nothing, and that is deliberate.
3. No marker line reaches a target file. Every slice is extracted from the
   COMMITTED `.agent/authored/f083-r21.md` by its markers.
4. Exactly two files are created and no existing file outside the paths named
   above is touched. `packages/`, `apps/` and `scripts/` are not modified at all;
   gate 6 proves it.
5. The 26 ruff errors are NOT fixed and the lint ceiling is NOT raised. The new
   test file must be ruff-clean, so the repo-wide count stays 26.
6. Every disposable worktree is removed and pruned before the handback.
7. If any gate is red, stop at that gate, record its real output verbatim, and
   hand back. Do not widen the change set to route around it.

## Done when — every command run from /home/decodeux/Repos/remedy, each its own
## unpiped process, each exit code read from that process

1. `pwd` printed FIRST. `git status --porcelain` EMPTY before the first commit and
   before C5. `git worktree list` ONE line at round start and at handback.
   `.agent/STOP` ABSENT at both.
2. `git rev-parse HEAD` at round start EQUALS 35b80d17.
3. `.agent/authored/f083-r21.md` and `.agent/last_block.md` byte-equal; report
   their sha256, byte count and line count.
4. `.agent/live_review.md` at C1: the pre content PREFIXES the post content, the
   tail byte-EQUALS the RECORD-R20 slice as extracted from the committed authored
   file by its markers, and `git show --numstat` has deletion column 0.
5. `.agent/plan.md` byte-equals the PLAN slice; report its sha256, line count
   (under 50), that `## Goal` and `## Next Steps` are present, and its count of
   unchecked-box lines.
6. `git diff --name-only 35b80d17..HEAD -- packages/ apps/ scripts/` prints
   NOTHING. Report that it printed nothing.
7. `python3 -m ruff check .` — report the `Found N errors.` line, ruff's actual
   final line, and the exit code. Expected 26 errors at exit 1, unchanged. Take
   this reading AT C3, the last commit that can change it, and report the commit
   you took it at rather than the word "before".
8. `python3 -m ruff check tests/orchestration/test_ci_workflow.py` — report its
   output and exit code. Expected `All checks passed!` at exit 0.
9. `python3 -m pytest tests/orchestration/test_ci_workflow.py -q` — report the
   passed count and exit code. All of its tests must pass.
10. THE PROBE, not a colour, in a disposable worktree at HEAD: move the
    `npm ci --prefix apps/ui` step to AFTER the `remedy ci run` step in that
    worktree's copy of the workflow, re-run
    `python3 -m pytest tests/orchestration/test_ci_workflow.py -q` there, and
    report the exit code and summary line. Report which tests failed by name. The
    ordering guard is expected to go RED and the others to stay green; any other
    outcome is the finding, and a run in which nothing fails means the guard does
    not guard. Then remove and prune the worktree and report `git worktree list`.
11. `python3 -m pytest tests/orchestration/test_ci_stage_selection.py -q` — the
    escape guard, because C3 adds a test file. Report the passed count and exit
    code.
12. `python3 -m pytest tests/orchestration/test_ci_budgets.py
    tests/orchestration/test_ci_stages.py
    tests/orchestration/test_ci_stage_selection.py tests/cli/test_ci_cmd.py
    tests/orchestration/test_ci_run.py -q` — report the passed count and exit code.
13. `python3 -m pytest tests/test_test_categories.py
    tests/test_no_interactive_guard.py -q` — the guard suites the `budgets` stage
    selects, because C2 adds a repository file they could scan. Report the passed
    count and exit code.
14. `python3 -m pytest tests/regression/test_resource_safety.py
    tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q` —
    the verification set and the canary. Report the passed count and exit code.
15. The open set, recomputed from `.agent/live_review.md` at HEAD: count every
    registration paragraph, every resolution line and every `Landed:` line; report
    registered, resolved, landed, open, the maximum id, the next free id, and
    whether any id repeats. Expected: 112 registered, 9 resolved, 0 landed, 103
    open, max R-0484, next free R-0485 — UNCHANGED by this round, because
    RECORD-R20 registers nothing and resolves nothing.
16. `git diff --name-only 35b80d17..HEAD` — report the full path list. Nothing
    outside the paths this block names may appear.
17. `git log --numstat` over the round — report the insertion count of every
    commit. None may exceed 500.
18. Confirm in one sentence that no `git commit --amend`, `git rebase` or
    `git reset` was run this round.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, branch, every commit SHA, a changed-files table per commit, the real
measured value of every gate above in an item-status table where each ordered item
appears exactly once with `done`, `skipped` or `deviated`, the open-findings
count, declared deviations with their causes, and the next expected action. If the
file exceeds 60 lines, carry a "Deviations, declared" line naming its line count
and the mandated content that caused the overage (DECISION D15).

THE NEXT ACTION THIS HANDOFF NAMES, in this order: (1) read `.agent/STOP` from
disk, self-drive Phase 1 rule 1, before anything else; (2) run the Open PR Gate,
`gh pr list --state open --json number,headRefName,baseRefName,isDraft`; (3) then
T003's second half — the CI documentation under `docs/`, its registration in the
`docs/README.md` index, and the runtime-budget table from `## Q9` through `## Q12`
— whose round also records THIS round's verdict, which lives only in the round
report until it does. Repeat this Fortschritt line verbatim as the handoff's last
line:

Fortschritt: 85 % (F083 beansprucht · R1 bis R7 und R9 bis R20 PASS, R8 FAIL auf einem roten ruff-Gate und in R9 repariert · T001 und T002 fertig · T003 zur Hälfte: die gehostete Workflow-Datei ruft denselben `remedy ci run` Entrypoint einmal auf, ohne Stage-Matrix und ohne Marker-Ausdruck im YAML, installiert die UI-Toolchain davor — D6 macht das tragend — und wiederholt nichts; Guards pinnen genau diese Eigenschaften · offen: die CI-Doku mit der Laufzeit-Budget-Tabelle aus den gemessenen Daten, danach Integration Gate und Closure) — Rundenzahl gemessen, Prozentwert geschätzt

Then `git push -u origin feature/f083-ci-self-check` and report its result, the
post-push `git status --porcelain` and the open-PR list in the round report.
