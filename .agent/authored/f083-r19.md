# F083 R19 — record R18, register two reviewer defects, and MEASURE R-0480

This is a MEASUREMENT round. It writes no production code and rules nothing: it
records the R18 verdict, registers two findings that belong to the reviewer, and
answers with real numbers the question R-0480 left open, so that R20 can rule on
the `ui` stage from data instead of from an anecdote.

Base: `git rev-parse HEAD` MUST print 6ce3c58d before the first commit. If it
does not, stop and report — every gate below is measured against that base.

## Why this round measures instead of fixing

R-0480 says the `ui` stage is RED the first time its suite runs in a fresh
worktree and GREEN on every run after, and attributes that to a cold `npx`
cache. The attribution has a hole in it that this round exists to close: the npx
cache is a per-USER directory, not a per-worktree one, so a new `git worktree`
should NOT produce a cold cache at all. Either the cause is something else, or
the cache was genuinely cold for an unrelated reason at the time. R-0480's
MEASUREMENT stands — four first-run reds and four second-run greens is data —
but its CAUSE is a hypothesis, and ordering a fix on a hypothesis is how a round
spends itself proving the reviewer wrong.

So this round orders a PROBE and never a colour
(docs/agents/planner_reviewer_prompt.md §3, pre-emission item 5). Every question
below has "not reproducible" as an acceptable, honest answer.

## Slice convention

Every slice is delimited by its own `--- BEGIN SLICE <NAME> ---` and
`--- END SLICE <NAME> ---` markers, which are TRANSPORT ONLY and NEVER reach a
target file. A slice's content begins on the line AFTER its BEGIN marker and
ends on the line BEFORE its END marker, newline included. The slices carried
here are named RECORD-R18 and PLAN. A slice with no FROM: line is an EOF-APPEND:
its bytes are appended to the end of the named file and nothing already in that
file is edited. Extract both slices programmatically from the COMMITTED
`.agent/authored/f083-r19.md` by their markers — never by retyping.

--- BEGIN SLICE RECORD-R18 --- (EOF-APPEND to .agent/live_review.md, C1)

Gate: R18 — PASS. The reviewer re-ran every gate itself at 6ce3c58d from the repository root, and the two colours the block ordered were re-proved independently rather than accepted from the handback. TRANSPORT, proved against the reviewer's OWN scratchpad original and not by digest fallback (§4.9): `.remedy-wt/f083-r18-block.md`, the committed `.agent/authored/f083-r18.md` and the committed `.agent/last_block.md` are all three byte-equal at sha256 272806846bd4e204 over 23774 bytes and 290 lines, under the 400-line cap. C1's prefix property holds — `.agent/live_review.md` goes 249551 B to 255203 B, the former prefixes the latter, and the 5652-byte tail is byte-EQUAL to the RECORD-R17 slice extracted from the COMMITTED authored file by its markers, numstat `4 0`. C6's `.agent/plan.md` byte-equals its PLAN slice, 42 lines under the 50-line cap, `## Goal` and `## Next Steps` present, 0 `- [ ]` lines, and 0 `--- BEGIN SLICE` occurrences, so no marker line leaked. The change set is exactly the thirteen paths the block named and nothing else, and per-commit insertions read from `git log --numstat` are 290, 270, 4, 178, 56, 103, 24 and 114 — none near 500. Gates taken BEFORE any pytest command, honouring R-0479: `python3 -m ruff check .` ends `Found 26 errors.` at exit 1 with the breakdown UNCHANGED at 20 I001, 4 F401, 1 F821 and 1 UP035, so the four new Python files this round added contribute zero errors and DECISION F083 D5's ceiling is honest; the integrity gate reports passed true, fail_count 0, check_count 5, handlers=338, all five checks pass. Then the suites, each unpiped with its exit read from its own process: the budgets suite and the four CI suites together 46 passed exit 0, `tests/docs/` 295 passed exit 0, and the verification quartet with the canary 148 passed exit 0. The open set recomputes mechanically to 110 registered, 6 `Done:`, 0 `Landed:`, 104 open, max R-0482, no duplicate id, and `.agent/f083_inventory.md` carries twelve `## Q` headings reading Q1 through Q12 — every value the block predicted. THE TWO RED CONTROLS WERE RE-RUN BY THE REVIEWER, in a disposable worktree created at HEAD and removed before this verdict, with `git worktree list` one line and `git status --porcelain` empty afterwards: pointing one `budgets` test path at a file that does not exist turns `test_every_test_path_a_stage_names_resolves_on_disk` RED, and the assertion message resolves `REPO_ROOT` to the WORKTREE copy, which is the proof that the mutated code is what ran (R-0337 class); lowering `LINT_ERROR_CEILING` to 0 turns `test_this_repository_really_is_at_or_below_the_lint_ceiling` RED with ruff's real reading of 26 in the message. Both gates can fail, so both mean something when they pass. THE WORK ITSELF IS SOUND: `timeout_sec=300` for `budgets` is exactly `ceil(2 * 1.32 / 300) * 300` under the table's own documented rule against the `## Q12` measured maximum, so the new budget was derived and not chosen; `pytest_argv_for_stage` appends `*stage.test_paths` and both argv shapes are pinned; and the D4 deliberate-absence paragraph landed in the `ci_stages` docstring in the repository's own idiom, with the feature file amended to match and `docs/roadmap/ROADMAP.md` untouched. THE WORKER'S CONDUCT WAS BETTER THAN THE BLOCK IT WAS GIVEN, and that is the substance of this gate: it caught two defects in the reviewer's own instructions, implemented the correct thing, and declared both rather than quietly complying. Both are registered below as reviewer defects. No finding is registered against the worker, and its remaining four declared deviations are all honest and none is a defect: a pre-commit suite run, two shell forms this session class denies which produced no reading, an extra `--statistics` ruff view, and a 154-line handoff carrying its DECISION D15 stated cause.

- R-0483 — Low, THE BLOCK ORDERED A GATE ORDERING ITS OWN COMMIT SEQUENCE MADE UNMEETABLE, AND THE WORKER HAD TO SPEND A DEVIATION PROVING IT. The R18 block's constraint 7 read "the lint reading and the integrity gate are taken BEFORE any pytest command runs this round", which exists to serve R-0479: a repo-wide lint count or an integrity reading taken while a suite is executing against the same checkout reads a clean repository as dirty. But the SAME block ordered C3 as a wall-clock MEASUREMENT of the budgets selection — three pytest runs — and then ordered C4's `timeout_sec` to be derived from that measurement. A pytest command therefore had to run in the middle of the round by construction, so a reading taken "before any pytest command" could only ever describe the base commit, never HEAD. The worker resolved it in the only honest way available: it took both readings TWICE, once genuinely before any pytest ran and once at HEAD before the gate suites, reported that the values are identical, and declared the deviation — and it recorded that the first integrity reading was RED on `relevant_untracked` because C2's two files were not yet committed, rather than quietly reporting the green one. Low and not Medium: no gate produced a wrong value, no evidence was lost, and the contamination R-0479 guards against did not occur. It is registered because the cost is real and recurring — the round paid a declared deviation to demonstrate a contradiction internal to the reviewer's own text, which docs/agents/planner_reviewer_prompt.md §3 item 5 names as the outcome worse than the mistake. THE RULE THIS PRODUCES, stated here and NOT yet binding: an ordering constraint over "any pytest command" is checked against the block's OWN commit sequence before emission, and when that sequence contains a measuring pytest run, the constraint names the COMMIT the reading is taken at instead of using the word "before". It binds nothing while it lives in this paragraph — a rule written as finding prose is an unpersisted lesson (R-0452, R-0454) — and R20 is the round that promotes it into docs/agents/planner_reviewer_prompt.md §3's pre-emission checklist, in the same block that carries the edit. Until that edit lands, this finding stays OPEN for that reason and not for any other. OPEN.

- R-0484 — Medium, A SCOPING CLAUSE THE BLOCK ORDERED WOULD HAVE TURNED A GREEN PROPERTY TEST RED FOR A REASON THE BLOCK DID NOT INTEND, AND ONLY THE WORKER'S REFUSAL KEPT IT GREEN. The R18 block's C4 ordered four selection tests scoped to stages with `runs_in_ci and not stage.test_paths`. For three of them that is right. For `test_no_test_in_this_repository_escapes_all_five_stages` it is wrong, and demonstrably so: that test asserts the COMPLEMENT of the union of the stage marker expressions collects nothing, and `excluded` carries `runs_in_ci=False`, so the ordered clause would have dropped `real_ollama` — the only term in the union that accounts for the live-provider tests — out of the union entirely. The complement would then have collected all 79 `real_ollama` items measured at `## Q2`, the subprocess call would have returned 0 instead of the asserted 5, and the gate would have gone red reporting every live-provider test as a test no stage runs. The reviewer's intent was to exclude PATH-bearing stages from a MARKER union, and `runs_in_ci` had no business in that predicate at all. The worker scoped it to `not stage.test_paths` alone, keeping `excluded` in, renamed the test to `test_no_test_in_this_repository_escapes_the_marker_selected_stages`, wrote the reason into the docstring, and declared the deviation. Medium and not Low, and not because anything landed wrong — nothing did: had the worker complied literally, the round would have ended on a red gate whose cause is a one-word predicate error in the reviewer's text, and the repair round would have been spent rediscovering it. This is the pre-emission checklist's item 8 exactly — a gate whose expected VALUE the code contradicts, ordered without reading the code that produces it — and the reviewer had read that very test file in the same turn it authored the clause. The remedy is not a new rule: item 8 already covers it, and it was not run against this clause. OPEN.
--- END SLICE RECORD-R18 ---
--- BEGIN SLICE PLAN --- (WHOLE FILE, replaces .agent/plan.md, C3)
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
R18 is closed PASS: the `budgets` stage, path-based stage selection, the
ratcheted lint ceiling, DECISION F083 D4 (no determinism stage) and DECISION
F083 D5 (the 26 ruff errors frozen, not fixed) are all on disk. R19 recorded
that verdict, registered R-0483 and R-0484 — both reviewer defects the worker
caught — and MEASURED the R-0480 question as `## Q13` of the inventory. R19
rules nothing.

## Next Steps
1. R20 rules on R-0480 from the `## Q13` data. If the cold-cache cause is
   confirmed, the options are warming the toolchain inside the stage, moving
   `test_typescript_compiles` behind the "UI toolchain absent locally" edge case
   the feature file already documents, or amending Acceptance. If Q13 shows the
   cause is something else, or is not reproducible, R-0480 is amended to say so
   before any fix is ordered. SPLIT round — the fix is production code.
2. T003 then remains: hosted workflow files calling the same entrypoint, the
   docs, and the runtime-budget documentation from the measured data.

## Risks
- R-0480's cause is a HYPOTHESIS, not a measurement. The npx cache is a per-user
  directory, so a fresh `git worktree` alone should not produce a cold one.
  Ordering a fix before Q13 answers this would spend a round proving the
  reviewer wrong.
- The lint ceiling is a RATCHET. Raising it to make a round green converts the
  one honest lint signal in this repository into decoration.
- R-0482 is a live `NameError` on a guard's refusal path, frozen under that
  ceiling rather than fixed, and belongs to a branch of its own.
--- END SLICE PLAN ---

## Change — exactly these paths, nothing beyond them

**C0a** saves this block to `.agent/authored/f083-r19.md`. **C0b** mirrors the
committed copy over `.agent/last_block.md`. **C1** applies the RECORD-R18 slice.

**C2 — the measurement, appended to `.agent/f083_inventory.md` as `## Q13`**, in
the shape `## Q10`, `## Q11` and `## Q12` already use: every number next to the
command that produced it, exit codes read from the `CompletedProcess` object and
never from a pipe, and `not-measured` written out wherever a value was not taken.
Answer these, in order:

1. WHERE THE NPX CACHE LIVES. Report `npm config get cache` and `npx --version`.
   Report whether the cache directory exists and whether it already contains a
   `typescript` or `tsc` entry, measured with a directory listing, not guessed.
   This is the fact that decides whether "fresh worktree" and "cold cache" are
   the same condition at all.
2. WHAT THE TEST ACTUALLY RUNS. Quote the `subprocess` argv and the `cwd` from
   `TestJobSummaryCommandContract::test_typescript_compiles` in
   `tests/ui_server/test_dashboard_contract.py`, read from the file, and report
   whether the argv carries `--yes`, `--no-install` or neither.
3. THE WARM READING. In a DISPOSABLE worktree at HEAD, run
   `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q` twice in a
   row with the ambient cache untouched. Report both exit codes and both summary
   lines. If the first run is GREEN, say so plainly — that is the result which
   falsifies R-0480's per-worktree reading, and it is exactly as valuable as a
   red one.
4. THE GENUINELY COLD READING. Run the same suite in that worktree once more
   with the environment variable `npm_config_cache` pointed at a NEW empty
   directory under `.remedy-wt/`, so npm resolves a cache that is empty by
   construction. Report the exit code, the summary line, and — if it failed —
   the failing test id and the captured stdout of the `npx` call verbatim.
   NEVER delete, move or modify the user's real npm cache directory; the env var
   is the whole mechanism, and a round that touches the real cache is a failed
   round regardless of what it measures.
5. WHETHER `--yes` CHANGES THE COLOUR. Repeat question 4's cold-cache run, once,
   with the test's `npx` invocation given `--yes` — do this by running the argv
   from question 2 DIRECTLY with `subprocess.run`, not by editing the test.
   Report the exit code and stdout of both forms, with and without `--yes`, in
   the same empty-cache environment.
6. THE HONEST CONCLUSION. State in two or three sentences what the numbers show
   and what they do NOT show. If the cold-cache cause is not reproducible, write
   that. This section carries NO recommendation and orders no fix — R20 rules.

**C3** applies the PLAN slice. **C4** rewrites `.agent/handoff.md`.

## Constraints

1. No production code. `packages/`, `apps/`, `tests/` and `scripts/` are NOT
   modified by this round; the range gate below proves it.
2. Never work on `main`; never force-push; never amend, rebase or reset. No PR
   is created or merged.
3. `.agent/live_review.md` is APPENDED to only. No committed text in it is
   edited, and no `Done:` paragraph is written.
4. No marker line reaches a target file. Both slices are extracted from the
   COMMITTED `.agent/authored/f083-r19.md` by their markers.
5. The user's real npm/npx cache is never deleted, moved or modified. Cold-cache
   conditions are produced ONLY by pointing `npm_config_cache` at a new empty
   directory under `.remedy-wt/`.
6. Every disposable worktree is removed and pruned before the handback, so
   `git status --porcelain` is empty and `git worktree list` is one line.
7. A question that cannot be answered is answered `not-measured` WITH the reason.
   Do not infer a number, and do not widen the change set to route around a
   blocker.

## Done when — every command run from /home/decodeux/Repos/remedy, each its own
## unpiped process, each exit code read from that process

1. `pwd` printed FIRST. `git status --porcelain` EMPTY before the first commit
   and before C4. `git worktree list` ONE line at round start and at handback.
   `.agent/STOP` ABSENT at both.
2. `git rev-parse HEAD` at round start EQUALS 6ce3c58d.
3. `.agent/authored/f083-r19.md` and `.agent/last_block.md` byte-equal; report
   their sha256, byte count and line count.
4. `.agent/live_review.md`: the pre-C1 content PREFIXES the post-C1 content, the
   tail byte-EQUALS the RECORD-R18 slice extracted from the committed authored
   file by its markers, and `git show --numstat` for that commit has deletion
   column 0.
5. `.agent/plan.md` byte-equals the PLAN slice; report its sha256, its line
   count (under 50), that `## Goal` and `## Next Steps` are present, and its
   count of `- [ ]` lines.
6. `git diff --name-only 6ce3c58d..HEAD -- packages/ apps/ tests/ scripts/`
   prints NOTHING. Report that it printed nothing.
7. `python3 -m ruff check .` — report its final line and exit code. Expected
   `Found 26 errors.` at exit 1, unchanged: this round writes no Python.
8. The integrity gate: `python3 -c "from packages.orchestration.integrity_gate
   import run_integrity_checks, export_integrity_json; import json;
   print(json.dumps(export_integrity_json(run_integrity_checks())))"` — report
   `passed`, `fail_count` and `check_count`.
9. `python3 -m pytest tests/orchestration/test_ci_budgets.py
   tests/orchestration/test_ci_stages.py
   tests/orchestration/test_ci_stage_selection.py tests/cli/test_ci_cmd.py
   tests/orchestration/test_ci_run.py -q` — report the passed count and exit
   code. All five paths exist today; report any that does not rather than
   accepting exit 4 as a pass.
10. `python3 -m pytest tests/cli/test_golden_path.py -q` — the canary. Report
    the passed count and exit code.
11. The open set, recomputed from `.agent/live_review.md` at HEAD: count every
    `^- R-\d+ — ` paragraph, every `^Done: R-\d+ — ` line, every
    `^Landed: R-\d+ — ` line; report registered, done, landed, open, the maximum
    id, the next free id, and whether any id repeats. Expected after C1: 112
    registered, 6 done, 0 landed, 106 open, max R-0484, next free R-0485.
12. `## Q\d` headings in `.agent/f083_inventory.md` at HEAD — report the count
    and the range. Expected Q1 through Q13.
13. `git diff --name-only 6ce3c58d..HEAD` — report the full path list. Nothing
    outside the paths this block names may appear.
14. `git log --numstat` over the round — report the insertion count of every
    commit. None may exceed 500.
15. Confirm in one sentence that no `git commit --amend`, `git rebase` or
    `git reset` was run this round, and that the real npm cache directory
    reported in `## Q13` question 1 was neither deleted nor modified.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, branch, every commit SHA, a changed-files table per commit, the real
measured value of every gate above in an item-status table where each ordered
item appears exactly once with `done`, `skipped` or `deviated`, the open-findings
count, declared deviations with their causes, and the next expected action. If
the file exceeds 60 lines, carry a "Deviations, declared" line naming its line
count and the mandated content that caused the overage (DECISION D15). Repeat
this Fortschritt line verbatim as the handoff's last line:

Fortschritt: 62 % (F083 beansprucht · R1 bis R7 und R9 bis R18 PASS, R8 FAIL auf einem roten ruff-Gate und in R9 repariert · Stage-Tabelle, Stage-Runner, die `remedy ci` CLI-Naht, die Selektionstests, die gemessenen Stage-Budgets und die budgets-Stage mit geratschter Lint-Decke als Code gelandet · D4 schliesst eine eigene Determinismus-Stage aus, D5 friert die 26 ruff-Fehler ein · R19 misst nur: die Ursache hinter R-0480 wird als Q13 gemessen, bevor R20 darüber entscheidet · noch offen: T003 mit den hosted workflows) — Rundenzahl gemessen, Prozentwert geschätzt

Then `git push -u origin feature/f083-ci-self-check` and report its result, the
post-push `git status --porcelain` and the open-PR list in the round report.
