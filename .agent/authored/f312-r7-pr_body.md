## F312 — The scope guard knows orders without file names

### What changed
- **Three kinds of order (T001).** `do_scope.order_scope_kind` reads an order's kind from its text
  alone: `names_files` (it spells a file path), `fenced` (a fence of `order_scope`'s one vocabulary,
  no path), or `open` (neither). The task-plan guard answers as before for the first two kinds; for
  an open order it leaves out only a task that makes nothing but a checking artifact, so the
  planner's files are the delivery. `plan_order_job` takes the person's order as `scope_order`, and
  the walk's shape step passes it for every job: a milestone's job outline still shapes its job's
  work but never fences it. Structure step (2) of `plan_order_job` (`_first_pass_task_plan`) came
  first; `plan_order_job` fell from 249 to 165 lines.
- **The question after two refusals (T002).** An open order whose task plan is refused gets one
  more planner call with the same prompt; a second refusal saves the job stopped (`scope_question`)
  with its prompt traces, raises one task decision asking which files the order means, with the
  planner's proposed files as options and no safe default, and ends the walk's shape step `stopped`
  with the answering command as its next line (`packages/orchestration/scope_question.py`). An
  answer naming files makes them the job's tasks and the job `planned`, so `remedy job resume` runs
  it with no planner call. `do_job_task_listing` moved to `do_summary.py` to keep `do_sequence.py`
  under the file limit.
- **The proof (T003).** `tests/regression/test_lab_orders_20261020.py` holds the three lab orders
  of 2026-10-20 and walks the second through the real `remedy do` with fake providers and the
  `milestones` shape. `docs/guides/do-run-v1.md` describes the kinds, the question and its answer.

### Why
The operator's second lab order of 2026-10-20, "Super, jetzt mach ein schickes design", failed after
five planner calls and 226 seconds without a single job: the task-plan guard read a
planner-written milestone outline as the order and refused its files (finding R-1369).

### Key decisions
DECISIONs F312 D1 to D5 in `.agent/decisions.md`. D1: the kind is read from the order's text, not
the repository. D2: an outline narrows a job's work and never draws a fence. D3: two refusals, then
one question, and the inspection-plan test of F268 D6 now gives an order that names a file (the D3
addendum). D4: an answer naming files becomes the job's tasks; an answer naming no usable file
changes nothing. D5: the ledger is not rotated in this closure, for the reason of DECISION F310 D8
(finding R-1376, owned by F307). The closure reads the integrity check as F310's did (DECISION F310
D7): it fails only on thirteen High findings F312 does not own.

### How to review and test
Read `docs/roadmap/features/T2_F312.md` (Built State) and the round entries in
`.agent/live_review.md`. Every round's selection was re-run by the reviewer, and every production
change was mutation-proven in a disposable worktree. The closure's one full suite:
`python3 -m pytest -n auto -q` → `22015 passed, 11 skipped` on `e04884674`
(`.agent/authored/f312-closure-suite.txt`).

### Evidence
- Evidence job `f312r6e1001` (9064 passed, 0 failed); package
  `remedy-review-20261021-011120-READY_FOR_REVIEW.zip`, SHA-256
  `6794d8c3eea4f31999f98681d9a1b080fd8b48ce427fcc101fbcff54fddcf3ac`, in
  `~/Repos/remedy-history/zips`; accepted head `a667ae7c44fad44d84224d946b325d2fd168859e`.
- Self-use item SU-066, the toolchain refresh, ran to its approval gate through `claude-cli` and was
  never applied; it ended blocked at its third task (finding R-1381, owned by F307).

### Verdict and findings
Live review PASS_WITH_RISKS. Resolved: R-1369, R-1377, R-1378, R-1379, R-1380, R-1382. Open: 88
findings by the ledger's reader, R-1381 among them, owned by F307. One commit, `a667ae7c4`, is over
the 500-insertion cap and was not declared before review (R-1382, recorded; no history rewrite).

### Runtime actuals
One session, seven delegated rounds; reviewer Claude Opus 5.5, workers Claude Sonnet; tokens and
cost of the session: not-measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
