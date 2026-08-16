# F083 R20 — rule on R-0480 with the Q13 data, promote the R-0483 rule, resolve three

SPLIT round: it changes a test under `tests/`, so the worker executes and the
reviewer gates. It records the R19 verdict, corrects R-0480's CAUSE from the
`## Q13` measurement, lands the fix that correction implies, and performs the
checklist promotion R-0483 said R20 would perform.

Base: `git rev-parse HEAD` MUST print 59d7d341 before the first commit. If it
does not, stop and report — every gate below is measured against that base.

## What Q13 changed

R-0480 blamed a cold `npx` cache. `## Q13` measured that and falsified it: the
cache is warm and has been since 2026-06-02, and the cold-cache run is GREEN.
The real variable is `apps/ui/node_modules`, gitignored at `.gitignore:221` and
therefore absent from every fresh checkout and every new worktree. With it
absent, `npx tsc` does not fail to find TypeScript — it silently resolves the
deprecated `tsc@2.0.4` stub out of the user cache, whose bin sets
`process.exitCode = 1`. With it present, `npx` resolves the LOCAL TypeScript and
the check is real. The run-1-red / run-2-green flip is intra-module ordering:
`test_typescript_compiles` sits above `test_auto_build_runs_by_default`, which
calls `_auto_build_frontend` and really does run `npm install`, so the first run
creates the `node_modules` the second run benefits from.

That is a worse defect than the one R-0480 named, and it is worth stating
plainly: the check has been resolving a nine-year-old stub instead of the
project's own compiler whenever the toolchain was missing, and reporting the
stub's exit code as a TypeScript verdict.

## DECISION F083 D6 — the tsc check resolves the LOCAL compiler or it skips

Chosen: `test_typescript_compiles` resolves `apps/ui/node_modules/.bin/tsc`
explicitly and, when that binary is absent, SKIPS with the install command in the
message. This is not a new policy — it is T2_F083's own documented edge case,
"UI toolchain absent locally: the ui stage reports skipped with the install hint
locally but is REQUIRED hosted — local convenience, hosted rigor, both honest" —
finally implemented. Alternatives considered and rejected: `npx --yes` (Q13
measured it: it changes nothing, because the stub resolves either way); having
the test run `npm ci` itself (a test that installs a toolchain is a build step
wearing a test's name, and it would put a network install inside the `fast`
stage); leaving it and amending Acceptance (keeps a green that is a stub's exit
code). Reverse by restoring the `npx` invocation.

CONSEQUENCE FOR T003, recorded so it cannot be forgotten: hosted rigor is now
load-bearing. The hosted workflow MUST run `npm ci --prefix apps/ui` before the
`ui` stage, or the check will skip hosted as well and the Acceptance line will be
met by a skip rather than by a compile. T003 owns that step.

## Slice convention

Every slice is delimited by its own `--- BEGIN SLICE <NAME> ---` and
`--- END SLICE <NAME> ---` markers, which are TRANSPORT ONLY and NEVER reach a
target file. A slice's content begins on the line AFTER its BEGIN marker and
ends on the line BEFORE its END marker, newline included. The slices carried
here are named RECORD-R19, CHECKLIST, RESOLVE and PLAN. A slice with no FROM:
line is an EOF-APPEND: its bytes are appended to the end of the named file and
nothing already in that file is edited. CHECKLIST is a FROM→TO pair and is
APPEND-SHAPED — its TO CONTAINS its FROM verbatim (§4.9), so the proof
obligation is FROM exactly 1x in the file before the edit, and each TO-ONLY line
exactly 1x among the lines that commit's diff ADDS. Extract every slice
programmatically from the COMMITTED `.agent/authored/f083-r20.md` by its
markers — never by retyping.

--- BEGIN SLICE RECORD-R19 --- (EOF-APPEND to .agent/live_review.md, C1)

Gate: R19 — PASS. The reviewer re-ran every gate itself at 59d7d341 from the repository root. TRANSPORT, against the reviewer's OWN scratchpad original and not by digest fallback (§4.9): `.remedy-wt/f083-r19-block.md`, the committed `.agent/authored/f083-r19.md` and the committed `.agent/last_block.md` are all three byte-equal at sha256 64d578db137f2167 over 20868 bytes and 215 lines. C1's prefix property holds — `.agent/live_review.md` goes 255203 B to 263322 B, the former prefixes the latter, the 8119-byte tail is byte-EQUAL to the RECORD-R18 slice extracted from the COMMITTED authored file by its markers, and numstat is `6 0`. C3's `.agent/plan.md` byte-equals its PLAN slice, 41 lines under the cap, `## Goal` and `## Next Steps` present, 0 `- [ ]` lines, 0 `--- BEGIN SLICE` occurrences. THE ROUND'S OWN CONSTRAINT HELD AND WAS RE-PROVED: `git diff --name-only 6ce3c58d..HEAD -- packages/ apps/ tests/ scripts/` printed NOTHING, so a measurement round measured and wrote no production code; the change set is exactly the six `.agent/` paths, and per-commit insertions are 215, 134, 6, 178, 21 and 92, none near 500. Lint and integrity taken before any pytest command: `Found 26 errors.` at exit 1 with the breakdown UNCHANGED at 20 I001, 4 F401, 1 F821, 1 UP035, and the integrity gate passed true, fail_count 0, check_count 5, handlers=338. The five CI suites and the canary together are 88 passed, exit 0. The open set recomputes to 112 registered, 6 `Done:`, 0 `Landed:`, 106 open, max R-0484, no duplicate id, and the inventory carries thirteen `## Q` headings reading Q1 through Q13 — every value the block predicted. THE MEASUREMENT WAS SPOT-CHECKED RATHER THAN BELIEVED, because a measurement round's whole value is its numbers: the reviewer read `test_typescript_compiles` in `tests/ui_server/test_dashboard_contract.py` and confirms its argv is exactly `["npx", "tsc", "--noEmit"]` with `cwd` at `REPO_ROOT / "apps" / "ui"` and neither `--yes` nor `--no-install`, exactly as Q13 reports; `.gitignore` line 221 is `node_modules/`; and `apps/ui/node_modules` exists in the primary checkout, which is the condition Q13 identifies as the real variable. The round exceeded its brief in the way a measurement round should: ordered to answer six questions in one disposable worktree, it created two MORE worktrees to separate the two candidate causes from each other, and declared the addition rather than folding it into the answer. All three were removed and pruned; `git worktree list` is one line and `git status --porcelain` is empty at this verdict. The user's real npm cache was never deleted, moved or modified — every cold-cache condition came from `npm_config_cache` pointed at a new empty directory under `.remedy-wt/`, which is the mechanism the block required and the only one used. Its five declared deviations are all honest and none is a defect, including the one worth naming: the worker caught and corrected its OWN handoff line count before committing, rather than shipping a self-report that disagreed with the file it described. No finding is registered against this round.

Amended: R-0480 — CAUSE CORRECTED at R20 from the `## Q13` measurement, per R-0470. This paragraph deliberately does NOT begin with the `- R-XXXX — ` registration form, because R-0480 is already registered and a second such line would count as a duplicate registration in every open-set recomputation this record supports. the text above is left standing and this paragraph supersedes only its cause. The OBSERVATION reproduces exactly and is not in question — first run red, second run green, four times. The stated CAUSE, a cold `npx` cache, is FALSIFIED. Measured at R19 and recorded as `## Q13`: the npx cache is the per-user directory `/home/decodeux/.npm`, it is WARM and has held a `tsc` entry under `_npx/1d6e82a4126006c4` since 2026-06-02, and the deliberately COLD run — the same suite with `npm_config_cache` pointed at an empty directory — is GREEN at `70 passed`, exit 0. A cold cache does not produce the failure; a warm one does. The real variable is `apps/ui/node_modules`, which `.gitignore` line 221 excludes as `node_modules/` and which is therefore absent from every fresh clone and every new `git worktree` by construction. With it ABSENT the suite is RED on BOTH runs, measured — so "first run red, second green" was never about the run count at all. What actually happens is worse than a cache miss: `npx tsc` with no local TypeScript resolves the deprecated `tsc@2.0.4` stub from the user cache, whose bin ends in `process.exitCode = 1`, so the assertion `result.returncode == 0` has been reading a nine-year-old stub's exit code and reporting it as a TypeScript verdict. The run-1/run-2 flip is intra-module ORDERING: `test_typescript_compiles` sits above `TestAutoBuildBehavior::test_auto_build_runs_by_default`, which calls `_auto_build_frontend` and performs a real `npm install`, so the first run of the module CREATES the `node_modules` that makes the second run green — measured directly at R19 in a third worktree by running that one test and watching the directory appear. The severity stays Medium and the finding stays this feature's business for the reason it always was: T2_F083's Acceptance line says "Clean checkout: `remedy ci` green locally and hosted", the `ui` stage selects this test by its `ui_contract` marker, and a hosted runner is a clean checkout by construction. DECISION F083 D6, ruled in this same block, is the fix.

Done: R-0484 — the defect was the reviewer's and the correct code is already on disk. The R18 worker declined the clause, scoped the union to `not stage.test_paths` alone so `excluded` stays in the union, renamed the test to `test_no_test_in_this_repository_escapes_the_marker_selected_stages`, and put the reason in the docstring; the reviewer re-ran that test at 6ce3c58d and it is green. No rule is added for it, and none is needed: pre-emission checklist item 8 already governs a gate whose expected value the code contradicts, and this instance was a failure to RUN item 8, not a gap in it. Resolved as a defect that never reached disk.
--- END SLICE RECORD-R19 ---
--- BEGIN SLICE CHECKLIST --- (FROM→TO pair, APPEND-SHAPED, docs/agents/planner_reviewer_prompt.md, C2)
FROM:
  Why this is on disk and not a habit: item 2 has recurred six times across
TO:
  13. **An ordering constraint is checked against the block's OWN commit sequence.**
      Finding R-0483. A constraint of the form "take reading X before any pytest
      command runs this round" is read back against the commits the SAME block
      orders. When that sequence contains a measuring pytest run — a wall-clock
      sample, a collection count, anything whose number a later commit consumes —
      the constraint is unmeetable as written, because a reading taken before any
      pytest command can only ever describe the BASE commit and never HEAD. Name
      the COMMIT the reading is taken at instead of using the word "before". The
      F083 R18 instance: constraint 7 demanded the lint and integrity readings
      before any pytest command while the same block ordered a three-sample
      pytest measurement mid-round and derived a later commit's `timeout_sec`
      from it, so the worker had to take both readings twice and spend a declared
      deviation demonstrating a contradiction internal to the reviewer's own
      text. Item 12 governs the reviewer's own PRE-EMISSION runs; this one
      governs the ORDER the block imposes on the worker's runs, which no dry run
      can surface because it is a property of the commit sequence rather than of
      any command in it.
  Why this is on disk and not a habit: item 2 has recurred six times across
--- END SLICE CHECKLIST ---
--- BEGIN SLICE RESOLVE --- (EOF-APPEND to .agent/live_review.md, C4)

Done: R-0483 — promoted, not merely restated. The rule now stands as item 13 of the pre-emission block checklist in docs/agents/planner_reviewer_prompt.md §3, added by C2 of this same block, which is the condition item 11 of that list imposes on a finding that claims its own promotion. The paragraph that registered it said explicitly that it bound nothing while it lived in finding prose and named R20 as the round that would move it; this is that round, and the move is the resolution.

Done: R-0480 — cause corrected and fixed. The correction is the amendment paragraph appended at C1 of this block, which supersedes the cold-cache attribution with the `## Q13` measurement; the fix is C3, ruled as DECISION F083 D6: `test_typescript_compiles` now resolves `apps/ui/node_modules/.bin/tsc` explicitly instead of letting `npx` fall back to a cached `tsc@2.0.4` stub, and SKIPS with the install command when that binary is absent — which is T2_F083's own "UI toolchain absent locally" edge case implemented rather than merely documented. The `ui` stage is therefore no longer RED on a clean checkout, and the silent-stub reading that made it green for the wrong reason is gone too. What is NOT resolved and is deliberately left to T003: hosted rigor now depends on the workflow running `npm ci --prefix apps/ui` before the `ui` stage, or the check skips hosted as well and Acceptance is met by a skip rather than by a compile. That obligation is recorded in the feature file by C5 of this block, which is where T003 will look for it.
--- END SLICE RESOLVE ---
--- BEGIN SLICE PLAN --- (WHOLE FILE, replaces .agent/plan.md, C6)
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
R19 is closed PASS and R20 recorded it. R20 corrected R-0480's cause from the
`## Q13` measurement — the variable is a missing `apps/ui/node_modules`, not a
cold npx cache — and ruled DECISION F083 D6: the tsc check resolves the LOCAL
compiler or skips with an install hint, instead of silently grading a cached
`tsc@2.0.4` stub. R-0480, R-0483 and R-0484 are resolved. T001 and T002 are
complete.

## Next Steps
1. T003, the last slice: hosted workflow files that call the same `remedy ci`
   entrypoint, the docs, and the runtime-budget documentation from the measured
   data in `## Q9` through `## Q12`. The workflow MUST run
   `npm ci --prefix apps/ui` before the `ui` stage — DECISION F083 D6 makes that
   step load-bearing, because without it the tsc check skips hosted too.
2. Then the integration-gate round, then closure per
   docs/roadmap/STATUS_closure_protocol.md.

## Risks
- If T003's workflow omits the `npm ci` step, the `ui` stage goes GREEN hosted by
  skipping, and the Acceptance line is met by a skip rather than a compile. That
  is the same false green D6 removed, wearing a different hat.
- The lint ceiling is a RATCHET. Raising it to make a round green converts the
  one honest lint signal in this repository into decoration.
- R-0482 is a live `NameError` on a guard's refusal path, frozen under that
  ceiling rather than fixed, and belongs to a branch of its own.
--- END SLICE PLAN ---

## Change — exactly these paths, nothing beyond them

**C0a** saves this block to `.agent/authored/f083-r20.md`. **C0b** mirrors the
committed copy over `.agent/last_block.md`. **C1** applies RECORD-R19.
**C2** applies CHECKLIST.

**C3 — the fix, `tests/ui_server/test_dashboard_contract.py`, method
`TestJobSummaryCommandContract::test_typescript_compiles` and nothing else in
that file.** Rewrite that method so it:
- resolves `REPO_ROOT / "apps" / "ui" / "node_modules" / ".bin" / "tsc"` and,
  when that path is not a file, calls `pytest.skip` with a message naming the
  absent directory and the exact install command `npm ci --prefix apps/ui`
  (the module already imports `pytest` at top level — do not add an import);
- otherwise runs `[str(local_tsc), "--noEmit"]` with `cwd` unchanged at
  `str(REPO_ROOT / "apps" / "ui")`, `capture_output=True` and the existing
  `timeout=30`, and keeps the existing assertion and its `result.stderr.decode()`
  message;
- carries a one-line WHY comment directly above the skip, naming finding R-0480
  and DECISION F083 D6 and stating that `npx` resolves a cached `tsc@2.0.4` stub
  when no local TypeScript exists, so the old form graded the stub's exit code.
Change no other method, no import, and no other file.

**C4** applies RESOLVE. **C5 — the rulings on disk**: append DECISION F083 D6 to
`.agent/decisions.md` in the file's existing entry shape, and amend
`docs/roadmap/features/T2_F083.md` — the "Edge cases & assumption defaults (A9)"
bullet about the absent UI toolchain gains a sentence recording that D6
implements it and that T003's hosted workflow must run `npm ci --prefix apps/ui`
before the `ui` stage. Change nothing else in that file; `docs/roadmap/ROADMAP.md`
is not touched. **C6** applies PLAN. **C7** rewrites `.agent/handoff.md`.

## Constraints

1. Never work on `main`; never force-push; never amend, rebase or reset. No PR
   is created or merged.
2. `.agent/live_review.md` is APPENDED to only, at C1 and again at C4. No
   committed text in it is edited. Both `Done:` paragraphs are reviewer-authored
   text applied verbatim; write no `Done:` or `Landed:` line of your own.
3. No marker line reaches a target file. Every slice is extracted from the
   COMMITTED `.agent/authored/f083-r20.md` by its markers.
4. The CHECKLIST pair is APPEND-SHAPED. Verify the FROM string occurs exactly
   ONCE in `docs/agents/planner_reviewer_prompt.md` before applying it, and
   apply it as a single replacement of that one occurrence.
5. Only the one test METHOD changes under `tests/`. `packages/`, `apps/` and
   `scripts/` are not modified at all; the range gate below proves it.
6. The 26 ruff errors are NOT fixed and the lint ceiling is NOT raised. The
   edited test must be ruff-clean, so the repo-wide count stays 26.
7. Every disposable worktree is removed and pruned before the handback.
8. If any gate is red, stop at that gate, record its real output verbatim, and
   hand back. Do not widen the change set to route around it.

## Done when — every command run from /home/decodeux/Repos/remedy, each its own
## unpiped process, each exit code read from that process

1. `pwd` printed FIRST. `git status --porcelain` EMPTY before the first commit
   and before C7. `git worktree list` ONE line at round start and at handback.
   `.agent/STOP` ABSENT at both.
2. `git rev-parse HEAD` at round start EQUALS 59d7d341.
3. `.agent/authored/f083-r20.md` and `.agent/last_block.md` byte-equal; report
   their sha256, byte count and line count.
4. `.agent/live_review.md` at C1 and again at C4: the pre content PREFIXES the
   post content, each tail byte-EQUALS the RECORD-R19 and RESOLVE slice
   respectively as extracted from the committed authored file by their markers,
   and each commit's `git show --numstat` has deletion column 0.
5. CHECKLIST pair proof: the FROM string occurred exactly 1x in
   `docs/agents/planner_reviewer_prompt.md` before C2, and each TO-ONLY line
   occurs exactly 1x among the lines C2's diff ADDS. Report both counts.
6. `.agent/plan.md` byte-equals the PLAN slice; report its sha256, line count
   (under 50), that `## Goal` and `## Next Steps` are present, and its count of
   `- [ ]` lines.
7. `git diff --name-only 59d7d341..HEAD -- packages/ apps/ scripts/` prints
   NOTHING. Report that it printed nothing.
8. `python3 -m ruff check .` — report its final line and exit code. Expected
   `Found 26 errors.` at exit 1, unchanged. Run BEFORE any pytest command.
9. The integrity gate, BEFORE any pytest command:
   `python3 -c "from packages.orchestration.integrity_gate import
   run_integrity_checks, export_integrity_json; import json;
   print(json.dumps(export_integrity_json(run_integrity_checks())))"` — report
   `passed`, `fail_count` and `check_count`.
10. `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q` in the
    PRIMARY checkout, where `apps/ui/node_modules` exists. Report the summary
    line and exit code, and state explicitly whether `test_typescript_compiles`
    PASSED or SKIPPED — it must PASS here, because the local compiler is present
    and really runs.
11. THE PROBE, not a colour, in a disposable worktree at HEAD where
    `apps/ui/node_modules` is absent by construction: run
    `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q -k typescript_compiles`
    and report the exit code and the summary line. Report which of PASSED,
    SKIPPED or FAILED occurred; a skip is the intended outcome, and any other
    result is the finding. Then remove the worktree and report
    `git worktree list`.
12. `python3 -m pytest tests/orchestration/test_ci_budgets.py
    tests/orchestration/test_ci_stages.py
    tests/orchestration/test_ci_stage_selection.py tests/cli/test_ci_cmd.py
    tests/orchestration/test_ci_run.py -q` — report the passed count and exit
    code.
13. `python3 -m pytest tests/docs/ -q` — the docs-round gate, because C5 changes
    `docs/roadmap/**`. Report the passed count and exit code.
14. `python3 -m pytest tests/regression/test_resource_safety.py
    tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q`
    — the verification set and the canary. Report the passed count and exit code.
15. The open set, recomputed from `.agent/live_review.md` at HEAD: count every
    `^- R-\d+ — ` paragraph, every `^Done: R-\d+ — ` line, every
    `^Landed: R-\d+ — ` line; report registered, done, landed, open, the maximum
    id, the next free id, and whether any id repeats. Expected: 112 registered,
    9 done, 0 landed, 103 open, max R-0484, next free R-0485.
16. `git diff --name-only 59d7d341..HEAD` — report the full path list. Nothing
    outside the paths this block names may appear.
17. `git log --numstat` over the round — report the insertion count of every
    commit. None may exceed 500.
18. Confirm in one sentence that no `git commit --amend`, `git rebase` or
    `git reset` was run this round.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, branch, every commit SHA, a changed-files table per commit, the real
measured value of every gate above in an item-status table where each ordered
item appears exactly once with `done`, `skipped` or `deviated`, the open-findings
count, declared deviations with their causes, and the next expected action. If
the file exceeds 60 lines, carry a "Deviations, declared" line naming its line
count and the mandated content that caused the overage (DECISION D15).

THE NEXT ACTION THIS HANDOFF NAMES, in this order: (1) read `.agent/STOP` from
disk, self-drive Phase 1 rule 1, before anything else; (2) run the Open PR Gate,
`gh pr list --state open --json number,headRefName,baseRefName,isDraft`; (3)
then T003 — the hosted workflow files calling the same entrypoint, the docs, and
the runtime-budget documentation — whose first reviewed round also records this
round's verdict, which lives only in the round report until it does. Repeat this
Fortschritt line verbatim as the handoff's last line:

Fortschritt: 78 % (F083 beansprucht · R1 bis R7 und R9 bis R19 PASS, R8 FAIL auf einem roten ruff-Gate und in R9 repariert · T001 und T002 fertig: Stage-Tabelle, Stage-Runner, die `remedy ci` CLI-Naht, die Selektionstests, die gemessenen Stage-Budgets und die budgets-Stage mit geratschter Lint-Decke · D4 schliesst eine eigene Determinismus-Stage aus, D5 friert die 26 ruff-Fehler ein, D6 lässt den tsc-Check den LOKALEN Compiler auflösen statt einen gecachten tsc@2.0.4-Stub zu benoten · offen ist nur noch T003: hosted workflows, Docs und das Laufzeit-Budget, danach Integration Gate und Closure) — Rundenzahl gemessen, Prozentwert geschätzt

Then `git push -u origin feature/f083-ci-self-check` and report its result, the
post-push `git status --porcelain` and the open-PR list in the round report.
