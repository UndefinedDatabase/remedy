── STEP R8/11 — F082 Self-benchmark (record R7, finish the sweep, pin the threshold) ──
Goal:        Record the R7 gate, register R-0415 and R-0416, persist DECISION
             F082 D4, retire the TWO regions of `.agent/context.md` that the
             R-0414 sweep left standing, and close T002's real coverage gap: the
             regression threshold and the trailing MEDIAN are pinned by nothing.
Bundle:      C0a/C0b save this block · C1 two findings, one decision and the R7
             verdict, persisted FIRST · C2 the state repair · C3 the fourth
             golden and the two tests that pin the rule · C4 handback.
Change:      .agent/live_review.md, .agent/context.md, .agent/plan.md,
             .agent/authored/f082-r8.md, .agent/last_block.md,
             .agent/handoff.md,
             tests/orchestration/fixtures/bench_history/varied.jsonl (NEW),
             tests/orchestration/test_bench_history.py (EDITED, additive).
             NOTHING else. No gauntlet module, no gauntlet test file, no order
             file, no manifest, and NO production module at all — R8 changes no
             file under `packages/`. `bench_history.py` is CORRECT as built; the
             gap is in its tests, so the tests are what change.
Constraints: Findings persist FIRST (planner_reviewer_prompt.md §4 item 4).
             Never write a `Done:` or `Landed:` paragraph of your own. Every
             authored slice is applied disk-to-disk out of the COMMITTED block
             file, never retyped. Push after every commit. Never merge, never
             force-push, never work on main. Create NO pull request: F082 is
             mid-feature and its PR is created at closure, not before.
             ADDITIVE in the test file: the three existing golden tests and the
             five others stay byte-unmodified and only new functions are added.
Done when:   the gates at the end of this block all pass, with their real
             values reported.
Handback:    completion report + rewrite .agent/handoff.md
──────────────────────────────────────────────────────────────────────

── C0 — save the block, in TWO commits ───────────────────────────────
The reviewer's scratchpad original is at `.remedy-wt/f082-r8-scratchpad.md`.
Saving it to both targets in ONE commit costs roughly twice its line count in
insertions and crowds the 500-insertion cap (findings R-0381, R-0399). Split it
unconditionally, and retype neither target:

C0a. Copy the scratchpad byte for byte to `.agent/authored/f082-r8.md`.
     Commit that file ALONE.
     Subject: `chore(f082): save the R8 block verbatim`
C0b. Copy the COMMITTED `.agent/authored/f082-r8.md` — not the scratchpad —
     byte for byte to `.agent/last_block.md`. Commit that file ALONE.
     Subject: `chore(f082): mirror the R8 block into last_block`

── C1 — two findings, one decision, the R7 verdict ───────────────────
ONE commit, the FIRST after C0. `.agent/live_review.md`, APPEND ONLY, in this
order, separated by exactly one blank line: FINDING-R415, FINDING-R416,
DECISION-D4, then GATE-R7. FINDING-R415, FINDING-R416 and GATE-R7 are each
exactly ONE physical line; DECISION-D4 is exactly TWO. Nothing above the append
may move — prove it against the pre-C1 revision over the file's existing 125
lines.
  Subject: `docs(f082): record the R7 verdict, register R-0415 and R-0416`

── C2 — finish the context.md sweep ──────────────────────────────────
ONE commit. TWO REWRITE pairs in `.agent/context.md` and one full replacement of
`.agent/plan.md`. The two FROM slices are disjoint from each other and neither
TO contains its own FROM. Apply CTXSCOPE first, then CTXSTEPS2.
  C2a. Pair CTXSCOPE — the Scope paragraph's "Built so far" list omits
       `bench_dry_run.py` and `bench_history.py`, and its "Still to come" names
       the history append and the regression rules, which landed at R7.
  C2b. Pair CTXSTEPS2 — the Steps map has no ✅ on R6 or R7 and still ends at
       R10. Do NOT touch the `## Steps` heading above it: the dashboard
       contract test asserts that substring.
  C2c. `.agent/plan.md`. FULL REPLACEMENT with the PLAN slice.
  Subject: `docs(f082): complete the context sweep and re-sync plan`

--- BEGIN SLICE FINDING-R415 ---
- R-0415 — Medium — T002's regression rule is built correctly and pinned by nothing: BOTH mechanisms that make it a rule rather than a comparison survive deletion with the whole suite green. The reviewer proved it by mutation in a disposable worktree at `20f101b0`, twice, each time reverting the previous mutation first. Replacing `if latest <= baseline * multiplier:` with `if latest <= baseline:` in `bench_history._threshold_regression` — deleting the threshold multiplier outright — leaves `8 passed`. Replacing the body of `bench_history._median` with `return float(sum(values)) / float(len(values))` — the mean instead of the median, the exact choice whose one-line WHY comment says "one catastrophic run must not raise the bar every later run is compared against" — also leaves `8 passed`. The cause is in the FIXTURES rather than in the assertions: all three goldens carry IDENTICAL trailing values, `flat.jsonl` and `degrading.jsonl` both at cost totals 1200 and 1200 with walls 40.0 and 40.0 across runs 1 and 2, and over identical values the median equals the mean and every positive multiplier ranks the same way, so no assertion written against those files can see either mechanism. The tests are not weak — they read their expected numbers off the goldens rather than restating them, which is exactly right — they are blind, and blind in a way only a mutation finds. This is the REVIEWER's defect: the R7 block ordered three goldens and named their shapes precisely, and every shape it named was a flat trailing series. It matters now rather than later because R9 wires `stats bench` to a CONFIG multiplier: a config knob whose value changes no test outcome is a knob that can drift to any number, including 1.0, without one gate going red, and the F082 acceptance criterion "cost/wall exceed the trailing median by a config multiplier" would then be satisfied in name only. The counter-measure, binding from R8 on: a block that orders a threshold rule also orders at least one fixture whose trailing values are NOT all equal and at least one assertion on the BASELINE the rule computed, not only on whether a warning appeared — a warn/no-warn boundary tests the fixture, a baseline value tests the rule. R8 closes it with a fourth golden and two tests, and re-runs both mutations to prove they now die. OPEN.
--- END SLICE FINDING-R415 ---

--- BEGIN SLICE FINDING-R416 ---
- R-0416 — Low — the closing sentence of R-0414 was false on disk in the same commit that wrote it. FINDING-R414 ends "R7 retires this one and the sweep is stated as complete for `.agent/context.md`", and after R7's C2 that file still carried two regions of R-0414's own class: the Scope paragraph's "Built so far" list, which names `capability_bench.py` and `bench_orders.py` and omits R6's `bench_dry_run.py`, followed by a "Still to come" clause naming the history append and the regression rules that R7's own C3 landed one commit later; and the Steps map, which awards ✅ to R1 through R5 and none to the landed R6. This is the third round running that a worker has declared a stale region its block did not order, and the second running that the declaration was correct — the R7 worker reported both under gate 7 and refused to repair them outside its ordered pair, which is the R-0406 conduct this repository asks for. The defect is entirely the reviewer's and it is a compound of two already-registered classes: R-0409 forbids an authored state slice from stating an outcome that a later step in the SAME block could falsify, and R-0413 registered the first time a counter-measure was violated by the very block that introduced it; R-0414's own counter-measure says to re-read the whole target file at emission and list every region naming the claim's subject, and the block that carried it re-read the file for the SENTENCE it was replacing instead. The claim also cost nothing to make and could not be checked by any gate, which is why it survived: gate 7 asked the worker to REPORT other stale regions, and reporting them does not retract a sentence already written. The counter-measure, binding from R8 on and additive to R-0414's: an authored finding never states that a sweep, a migration or a retirement is COMPLETE. It states what the round retires, by name, and leaves completeness to be measured by the next round's gate against the file. A completeness claim is a prediction about bytes the same block has not yet written, which is the R-0371 class in prose form. R8 retires both named regions and asserts nothing about what remains. OPEN.
--- END SLICE FINDING-R416 ---

--- BEGIN SLICE DECISION-D4 ---
## DECISION F082 D4 — R8 is inserted for the sweep and the threshold pin; T003 moves to R9
Chosen 2026-08-14 by the reviewer under planner_reviewer_prompt.md §4 item 7, which routes a wrong plan into the current block as a loud, persisted, reversible decision rather than a question. R-0415 (the regression threshold and the trailing median are pinned by no test) and R-0416 (two regions of context.md left stale by the R-0414 sweep) both land between T002 and T003, and both are small. The alternative considered and rejected was folding them into R9 alongside T003 — the `stats bench` CLI, model-context recording and a fake-provider run end to end — which is already the largest remaining slice and would have made a red gate there ambiguous between a CLI defect and a fixture defect; the second alternative, deferring the threshold pin to closure, was rejected because R9 wires a CONFIG multiplier into exactly the mechanism no test can currently see, so the pin must precede the knob. The plan therefore reads R8 sweep-and-pin, R9 T003, R10 the integration gate, R11 closure, and the round denominator moves from ten to eleven in `.agent/plan.md`, `.agent/context.md` and every later block header, which is the R-0413 counter-measure applied rather than the drift it was registered against. Reverse this decision by deleting this paragraph and merging R8's bundle into R9; nothing in it is load-bearing for T003's design, only for its evidence.
--- END SLICE DECISION-D4 ---

--- BEGIN SLICE GATE-R7 ---
Gate: R7 — PASS, with two new findings, both the reviewer's, and neither charging the worker. Verification tier: round gate plus the state-file contract readers plus the canary; no full-suite claim is made and none is owed. All eighteen ordered gates were re-executed by the reviewer against the disk rather than read out of the handback, and every one reproduces at its reported value. Transport is proven at PRIMARY strength rather than the digest fallback: the scratchpad `.remedy-wt/f082-r7-scratchpad.md`, `.agent/authored/f082-r7.md` and `.agent/last_block.md` are byte-identical at shared sha256 `e0517f102c34ad9373f3ca8b9cb98701991d5c4b81737e78c873620b15801a56`, 28357 bytes and 334 lines, inside the 400-line cap. The append was proven as `post == pre + add` and not by grep: the reviewer re-extracted FINDING-R414 and GATE-R6 from the COMMITTED block file, joined them with the blank-line separator the block ordered, and the result is byte-identical to the region C1 added, with the whole 121-line pre-C1 file an exact prefix of the 125-line result and the C1 numstat `4 0`, deletion column zero. Every slice digest reproduces the reviewer's own pre-emission measurement exactly — FINDING-R414 `11026fe6…`, GATE-R6 `defbd10f…`, CTXBUILT-FROM `355436a9…`, CTXBUILT-TO `276be55e…`, PLAN `7865656a…` — and the CTXBUILT pair was gated as a PROPERTY rather than a count for the reason R6 taught: `pre.replace(FROM, TO) == post` holds byte-wise, with FROM 1x before and 0x after and TO 0x before and 1x after. `.agent/plan.md` is byte-equal to the PLAN slice as a whole file at 36 lines under the 50-line cap, `.agent/context.md` is 55 lines and keeps every contract reader, and the record counts are `^Gate: R6 — PASS` 1, `^- R-0414 — ` 1, `^## Steps` 1, `^Landed: ` 0 and `^Done: ` 0, so the worker authored no resolution of its own; the open set recomputed mechanically is exactly FORTY-FOUR with no duplicate, max R-0414 and next free R-0415. The change set is eleven paths, every one inside the block's Change list and none outside it; the four under `tests/orchestration/` are the new test file and the three new goldens, so no gauntlet or existing bench test file was touched. Suites re-run by the reviewer at the branch head: the eleven-file orchestration suite `292 passed`, and the arithmetic closes against the reviewer's own pre-round measurement of 284 for the same files without the new one, so 284 + 8 new tests = 292 and no pre-existing test was lost; the canary plus the three contract readers `184 passed`; scoped ruff over the two new Python files `All checks passed!`; `integrity check --json` `passed: true`, `fail_count: 0` over 5 checks with no open blocker/high findings. Insertions per commit are 334, 227, 4, 16, 467 and 157, none over 500. `gh pr list --state open` is `[]`. The reviewer ran its own red-proof in a disposable worktree and the ordered mutation reproduces: `append_bench_run` opening its file `"w"` instead of `"a"` fails exactly `test_a_rerun_appends_and_never_rewrites_the_bytes_already_there` at `assert after_second.startswith(after_first)`, and the failure output shows run 1's bytes genuinely gone, which also proves the mutated module was the one imported rather than the primary checkout's (R-0337). The goldens were read rather than trusted and they are not vacuous: all three carry the series the tests query, so the flat and improving files return no warning because the RULE returns none, not because the filter emptied them, and the degrading file's run 3 puts one order at cost total 2400 against a trailing median of 1200 and wall 90.0 against 40.0 while the other order is untouched, so it warns about exactly one order. `bench_history.py` itself imports `BenchRecord` and `projects_dir` and edits neither, keeps `capability_bench.py`'s purity promise true by living in its own file, mirrors `token_ledger.token_ledger_path_for` including its registry-UUID-is-not-the-repo-hash warning, nests the row under its own key so no future field can collide with an envelope field, never raises on a read, and documents its deliberate absence of a clock where a reader would search for it. Two deviations, both declared and both accepted: the handback is 180 lines against the 60-line cap carrying its DECISION D15 stated cause with no section dropped, and the commit messages carry no trailer. One observation costs no id: the worker's per-slice byte lengths exceed the reviewer's by the number of multi-byte characters in each slice, because the worker measured UTF-8 BYTES where the reviewer measured characters; the digests agree exactly, which is the load-bearing proof, and this is the same measurement-convention difference already noted at R1 and R5. The two new findings are R-0415, that the regression threshold multiplier and the trailing median are pinned by no test because all three goldens carry identical trailing values — proven by two mutations that each leave `8 passed` — and R-0416, that R-0414's own closing sentence claimed the context.md sweep was complete while two regions of its class still stood. No block condition was hit — no fabricated value, no false live indicator, no missing changed-files table, no unverified completion claim by the worker, no silent scope change.
--- END SLICE GATE-R7 ---

--- BEGIN SLICE CTXSCOPE-FROM ---
In: the capability bench built on the gauntlet harness. Built so far:
`capability_bench.py` with the pure record builder, `bench_orders.py` with the
version-bound freeze, and THREE frozen orders under `scripts/bench_orders/` —
three and not five, because the shared sample project has no HTTP surface and
no web asset (R-0411), and the missing two wait on a bench-owned fixture per
DECISION F082 D3 rather than an edit to the gauntlet's template. Still to come:
the history append, the trend and regression rules, and the `stats bench` CLI.
--- END SLICE CTXSCOPE-FROM ---

--- BEGIN SLICE CTXSCOPE-TO ---
In: the capability bench built on the gauntlet harness. Built so far:
`capability_bench.py` with the pure record builder, `bench_orders.py` with the
version-bound freeze, THREE frozen orders under `scripts/bench_orders/` — three
and not five, because the shared sample project has no HTTP surface and no web
asset (R-0411), and the missing two wait on a bench-owned fixture per DECISION
F082 D3 rather than an edit to the gauntlet's template — `bench_dry_run.py`
with the join from an order file to a row over recorded evidence, and
`bench_history.py` with the append-only history, the trend and the regression
rules. Still to come, both T003: the `stats bench` CLI surface and the
model-context recording.
--- END SLICE CTXSCOPE-TO ---

--- BEGIN SLICE CTXSTEPS2-FROM ---
R1 claim F082, reset the record carrying the F077 open set forward, register
R-0403 ✅ → R2 the T001 gauntlet-harness inventory ✅ → R3 T001 the pure record
builder and the R-0407 token repair ✅ → R4 T001 the frozen order set and its
version freeze ✅ → R5 record the R4 verdict, register R-0409 to R-0411 and
DECISION F082 D3 ✅ → R6 record the R5 verdict, retire the superseded context
regions and close T001 with the dry run against recorded evidence → R7 T002
history, trend and regression rules → R8 T003 the stats bench CLI, model context
and a fake-provider run → R9 the integration gate → R10 closure.
--- END SLICE CTXSTEPS2-FROM ---

--- BEGIN SLICE CTXSTEPS2-TO ---
R1 claim F082, reset the record carrying the F077 open set forward, register
R-0403 ✅ → R2 the T001 gauntlet-harness inventory ✅ → R3 T001 the pure record
builder and the R-0407 token repair ✅ → R4 T001 the frozen order set and its
version freeze ✅ → R5 record the R4 verdict, register R-0409 to R-0411 and
DECISION F082 D3 ✅ → R6 record the R5 verdict, retire two superseded context
regions and close T001 with the dry run ✅ → R7 T002 the append-only history,
the trend and the regression rules ✅ → R8 record the R7 verdict, complete this
sweep and pin the regression threshold → R9 T003 the stats bench CLI, model
context and a fake-provider run → R10 the integration gate → R11 closure.
--- END SLICE CTXSTEPS2-TO ---

--- BEGIN SLICE PLAN ---
# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0417. Open findings: forty-six — the thirty-two carried from F077, plus
R-0403 to R-0416 registered on this branch. `.agent/live_review.md` is the
source of truth for that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R8 records the R7 gate, registers R-0415 and R-0416, persists DECISION F082 D4,
retires the two regions of `.agent/context.md` the R-0414 sweep left standing,
and pins T002's regression threshold and trailing median with a fourth golden
whose trailing values are not all equal.

## Next Steps
1. R9 — T003: the `stats bench` CLI, model-context recording, and a
   fake-provider bench run end to end.
2. R10 the integration gate, R11 closure.

## Risks
- The delivered order set is three, not the Design's five (R-0411). Closure
  may not quote five, and DECISION F082 D3 binds the recovery to a
  bench-owned fixture rather than an edit to the gauntlet's template.
- The freeze holds against a file-side edit only (R-0410). The Built State
  states that threat model rather than quoting the acceptance criterion whole.
- `repair_rounds` is `None` at every row by construction (R2 Q7). The trend
  therefore has no repair-round series to regress on, and T003's report says so
  rather than printing a zero.
--- END SLICE PLAN ---

── C3 — pin the threshold and the median ─────────────────────────────
ONE commit, both files together.
  Subject: `test(f082): pin the regression threshold and the trailing median`

Write `tests/orchestration/fixtures/bench_history/varied.jsonl`, NEW. FOUR runs
of ONE order id `bench-01-cold-start`, series `f082-bench`, every row
`"passed": true`, `"repair_rounds": null`, `"postmortem_classes": []`, written
in exactly the line shape `BenchHistoryEntry.to_json()` produces — generate it
with that method rather than hand-typing the JSON, so it cannot drift from the
shape the loader expects:
  run 1  cost `{"in": 800, "out": 200}`   wall_s 10.0
  run 2  cost `{"in": 800, "out": 200}`   wall_s 10.0
  run 3  cost `{"in": 3200, "out": 800}`  wall_s 100.0
  run 4  cost `{"in": 1600, "out": 400}`  wall_s 25.0
Run 3 is the one catastrophic run the `_median` docstring exists for. The
trailing cost totals are 1000, 1000 and 4000, whose median is 1000 and whose
mean is 2000; the trailing walls are 10.0, 10.0 and 100.0, median 10.0 and mean
40.0. The latest run sits at 2000 and 25.0 — above 1.5x each median and below
1.5x each mean, and below 3.0x each median. That is what makes the fixture
discriminate; nothing else in it matters.

Add to `tests/orchestration/test_bench_history.py`, ADDITIVE — the eight
existing test functions and every helper stay byte-unmodified:
  1. `test_the_trailing_median_ignores_one_catastrophic_run` — load `varied.jsonl`,
     compute the trailing cost totals and walls INSIDE the test by reading the
     entries whose `run_seq` is below the highest, and assert first that the
     median and the mean of those trailing totals DIFFER (so a later edit that
     flattens the fixture fails here rather than silently going blind again),
     then that the cost warning's `baseline` equals the median and does NOT
     equal the mean, and the same for the wall warning. Assert the BASELINE the
     rule computed, not only that a warning appeared: a warn/no-warn boundary
     tests the fixture, a baseline value tests the rule (R-0415).
  2. `test_a_larger_multiplier_silences_the_same_history` — the SAME entries
     return warnings at the default multiplier and exactly `()` at
     `multiplier=3.0`. This is what fails if `* multiplier` is ever dropped.
  Import `statistics` if you want its `median` and `mean`; do not hand-roll them
  in the test, and do not import the module's own `_median` — a test that reuses
  the implementation it is checking proves nothing.

If either test passes against a deliberately broken rule, say so in the handback
rather than adjusting the test until it looks right.

── C4 — handback ─────────────────────────────────────────────────────
Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. Name, as the
FIRST action of the next session, `docs/agents/self_drive_protocol.md` Phase 1
rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2's Open PR Gate. State
that F082 is MID-FEATURE, that no PR exists for this branch and none is created
until closure, and that the next round is R9 — T003. Under 60 lines, or carry a
DECISION D15 stated-cause line naming the real count and the mandated content
that caused it. Commit and push.
  Subject: `chore(f082): handback R8`

── Gates — run every one, report the REAL value ──────────────────────
1.  `git status --porcelain` → EMPTY at handback. `git worktree list` → 1 line,
    as it reads AT HANDBACK.
2.  Transport, as a PROPERTY (R-0408): prove the scratchpad,
    `.agent/authored/f082-r8.md` and `.agent/last_block.md` are byte-identical
    and report the shared sha256 and the line count, which must be at or under
    400. Any means; report the digest.
3.  `.agent/STOP` — ABSENT or PRESENT, at round start AND at handback.
4.  Append proof: the first 125 lines of the new `.agent/live_review.md` equal
    the pre-C1 file, proven as `post == pre + add` byte-wise and not by grep.
    Report the C1 numstat for that path; DELETION column 0. Report the physical
    line count of FINDING-R415, FINDING-R416, DECISION-D4 and GATE-R7 — 1, 1, 2
    and 1 respectively.
5.  `grep -c "^Gate: R7 — PASS" .agent/live_review.md` → 1; `^- R-0415 — ` → 1;
    `^- R-0416 — ` → 1; `^## DECISION F082 D4` → 1; `^## Steps` → 1;
    `^Landed: ` → 0; `^Done: ` → 0.
6.  Open set recomputed mechanically — `^- R-[0-9]\+ — ` paragraphs minus
    `^Done: R-[0-9]\+ — ` lines. Expect FORTY-SIX; name every id; report
    duplicates as none or name them; report max and next free.
7.  Both context pairs, gated as a PROPERTY because counts alone are brittle
    here: prove `post == pre.replace(SCOPE_FROM, SCOPE_TO).replace(STEPS_FROM,
    STEPS_TO)` byte-wise over `.agent/context.md`, and report each FROM 1x
    before and 0x after and each TO 0x before and 1x after, measured WITH the
    terminating newline. Report `wc -l .agent/context.md`. Then re-read the file
    end to end and report every region, if any, that still names which modules
    this feature builds, which round did what, or how many rounds remain, and
    whether each agrees with `.agent/plan.md`. Report them; repair nothing
    outside these two pairs.
8.  `wc -l .agent/plan.md` → under 50. Report it.
9.  The `.agent/context.md` contract readers: `## Active Branch` with a
    `feature/` slug, the substring `Steps`, a roadmap F-id, and `pytest` or
    `resource`. Report each.
10. `git diff --name-only 20f101b0..HEAD` → report every path and COUNT them
    mechanically, stating the count. The Change list is a CEILING: every path
    reported appears in it. Name any path present that it does not contain —
    there must be none. Report `git diff --name-only 20f101b0..HEAD --
    packages/` separately; it must be EMPTY.
11. `git diff --numstat 20f101b0..HEAD -- tests/orchestration/test_bench_history.py`
    → report it. The DELETION column must be 0: the edit is purely additive and
    no existing test or helper line is touched.
12. `python3 -m pytest tests/orchestration/test_bench_history.py
    tests/orchestration/test_bench_dry_run.py
    tests/orchestration/test_capability_bench.py
    tests/orchestration/test_bench_orders.py
    tests/orchestration/test_gauntlet_runner.py
    tests/orchestration/test_gauntlet_evaluator.py
    tests/orchestration/test_gauntlet_evidence.py
    tests/orchestration/test_gauntlet_matrix.py
    tests/orchestration/test_gauntlet_injection.py
    tests/orchestration/test_self_run_gauntlet.py
    tests/orchestration/test_verification_matrix.py -q` → exit 0. The reviewer
    measured those eleven files at `20f101b0` today: 292 passed. Report the real
    total and the arithmetic — it must be 292 plus the number of tests you added,
    and no pre-existing test may be lost.
13. `python3 -m pytest tests/cli/test_golden_path.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_test_runner.py -q` → exit 0. Reviewer baselines
    re-measured at `20f101b0` today: 42 for the canary and 142 for the three
    readers, so 184.
14. `python3 -m ruff check tests/orchestration/test_bench_history.py` → exit 0.
    Repository-wide ruff is RED on main and is NOT a gate (R-0364); this is
    scoped to the one Python file R8 touches. The reviewer ran the same command
    over that file at `20f101b0` today and it printed `All checks passed!`.
15. Red-proof, in a DISPOSABLE worktree under `.remedy-wt/` only (G5, §4 item
    10), never in the primary checkout. Run BOTH of R-0415's mutations against
    `packages/orchestration/bench_history.py`, reverting the first before
    applying the second, and report the real result of each:
      (a) replace `if latest <= baseline * multiplier:` with
          `if latest <= baseline:` in `_threshold_regression`;
      (b) replace the body of `_median` with
          `return float(sum(values)) / float(len(values))`.
    At `20f101b0` each of these left `8 passed` — that is R-0415. Order the
    PROPERTY, not a colour: report which tests fail under each mutation and the
    assertion text, and if EITHER mutation still leaves the suite green, say so
    plainly — that is a real finding about C3 and the reviewer wants it, not a
    green word. Remove and prune the worktree; `git worktree list` must read one
    line afterwards.
16. `python3 -m apps.cli.main integrity check --json` → `passed: true`,
    `fail_count: 0`, `check_count: 5`. Report the `high_blockers_open` message.
17. `gh pr list --state open --json number,headRefName` → report it verbatim.
    It must be `[]`: no PR is created for this branch until closure.
18. Report each commit's `git show --numstat <sha>` insertion total. If any
    exceeds 500, declare it in the handback with the reason.

Transport proof: state, for each of FINDING-R415, FINDING-R416, DECISION-D4,
GATE-R7, CTXSCOPE-FROM, CTXSCOPE-TO, CTXSTEPS2-FROM, CTXSTEPS2-TO and PLAN, that
it was extracted from the COMMITTED `.agent/authored/f082-r8.md` and applied
disk-to-disk, with its sha256 and byte length, and the proof that the applied
region equals it. Both context pairs are REWRITES: neither TO contains its own
FROM, and the two FROMs are disjoint. Confirm no BEGIN/END marker line reached
any target file. Scan every file you touched for trailing whitespace and report
the result.
