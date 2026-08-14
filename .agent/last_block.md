── STEP R7/10 — F082 Self-benchmark (record R6, then T002 history, trend, regressions) ──
Goal:        Record the R6 gate, register R-0414, retire the LAST superseded
             region of `.agent/context.md`, then build T002: the append-only
             bench history, the trend read back off it, the regression rules,
             and the improving, flat and degrading goldens.
Bundle:      C0a/C0b save this block · C1 the R6 verdict and one finding,
             persisted FIRST · C2 the state repair · C3 the history module, its
             three goldens and its tests · C4 handback.
Change:      .agent/live_review.md, .agent/context.md, .agent/plan.md,
             .agent/authored/f082-r7.md, .agent/last_block.md,
             .agent/handoff.md, packages/orchestration/bench_history.py (NEW),
             tests/orchestration/test_bench_history.py (NEW),
             tests/orchestration/fixtures/bench_history/improving.jsonl (NEW),
             tests/orchestration/fixtures/bench_history/flat.jsonl (NEW),
             tests/orchestration/fixtures/bench_history/degrading.jsonl (NEW).
             NOTHING else. No gauntlet module, no gauntlet test file, no order
             file, no manifest, no existing bench module is edited.
Constraints: Findings persist FIRST (planner_reviewer_prompt.md §4 item 4).
             Never write a `Done:` or `Landed:` paragraph of your own. Every
             authored slice is applied disk-to-disk out of the COMMITTED block
             file, never retyped. Push after every commit. Never merge, never
             force-push, never work on main. Create NO pull request: F082 is
             mid-feature and its PR is created at closure, not before.
             ADDITIVE only (F082 inventory Q11): every bench and data-path
             symbol the new module needs is IMPORTED, none is moved or edited.
             `capability_bench.py` stays PURE — its docstring claims no disk
             read, no network, no clock — so the history reading lives in the
             NEW module, exactly as `bench_dry_run.py` did at R6.
Done when:   the gates at the end of this block all pass, with their real
             values reported.
Handback:    completion report + rewrite .agent/handoff.md
──────────────────────────────────────────────────────────────────────

── C0 — save the block, in TWO commits ───────────────────────────────
The reviewer's scratchpad original is at `.remedy-wt/f082-r7-scratchpad.md`.
Saving it to both targets in ONE commit costs roughly twice its line count in
insertions and crowds the 500-insertion cap (findings R-0381, R-0399). Split it
unconditionally, and retype neither target:

C0a. Copy the scratchpad byte for byte to `.agent/authored/f082-r7.md`.
     Commit that file ALONE.
     Subject: `chore(f082): save the R7 block verbatim`
C0b. Copy the COMMITTED `.agent/authored/f082-r7.md` — not the scratchpad —
     byte for byte to `.agent/last_block.md`. Commit that file ALONE.
     Subject: `chore(f082): mirror the R7 block into last_block`

── C1 — the R6 verdict and one finding ───────────────────────────────
ONE commit, the FIRST after C0. `.agent/live_review.md`, APPEND ONLY, in this
order, separated by exactly one blank line, each exactly ONE physical line:
FINDING-R414, then GATE-R6. Nothing above the append may move — prove it
against the pre-C1 revision over the file's existing 121 lines.
  Subject: `docs(f082): record the R6 verdict and register R-0414`

── C2 — retire the last superseded region of context.md ──────────────
ONE commit. One REWRITE pair in `.agent/context.md` and one full replacement of
`.agent/plan.md`.
  C2a. Pair CTXBUILT — the R2-inventory sentence still says the bench "lands as
       a NEW `packages/orchestration/capability_bench.py`", singular, while
       three bench modules now exist. This is R-0414 and it is the third region
       of the same class in this one file. Its FROM spans five physical lines
       and its wrapping is NOT what a reader would guess — apply it
       disk-to-disk from the committed block, never retyped.
  C2b. `.agent/plan.md`. FULL REPLACEMENT with the PLAN slice.
  Subject: `docs(f082): retire the last superseded context region and re-sync plan`

--- BEGIN SLICE FINDING-R414 ---
- R-0414 — Low — `.agent/context.md` carried a THIRD superseded region of exactly the class R-0412 registered one round earlier, and the R6 block that registered R-0412 left it standing. The Scope paragraph's R2-inventory sentence still reads "the factoring is ADDITIVE, so the bench lands as a NEW `packages/orchestration/capability_bench.py` with `tests/orchestration/test_capability_bench.py`" — singular, one module — while three bench modules now exist on this branch: `capability_bench.py` from R3, `bench_orders.py` from R4 and `bench_dry_run.py` from R6, each with its own test file. Nothing on disk contradicts it outright, which is why it survived two sweeps: it is an incomplete statement rather than a false one, and a grep for a contradiction does not return it. R-0412's counter-measure says to "grep that WHOLE file for the claim being changed and retire every instance in the same pair set"; the R6 block ordered two pairs against the two regions R-0412's own text named and never re-read the file for a third, so the counter-measure was applied to the instances already known instead of to the file. That is the REVIEWER's defect and not the worker's: the R6 worker found this region while executing gate 7, reported it in the handback as "one residual, NOT repaired (outside the ordered pairs)", and correctly refused to repair it outside its ordered slices, which is the R-0406 conduct this repository asks for and the second round running that the worker has declared a region the block did not order. The counter-measure, additive to R-0412's and binding from R7 on: a block that retires a superseded claim in an `.agent/**` state file greps that file for the claim's SUBJECT — here, which modules this feature builds — rather than for the sentence being replaced, and the reviewer re-reads the whole target file at emission and lists every region naming that subject, so the sweep ends at the file rather than at the findings that happened to name a region. R7 retires this one and the sweep is stated as complete for `.agent/context.md`. OPEN.
--- END SLICE FINDING-R414 ---

--- BEGIN SLICE GATE-R6 ---
Gate: R6 — PASS, with one new finding, the reviewer's. Verification tier: round gate plus the state-file contract readers plus the canary; no full-suite claim is made and none is owed. All eighteen ordered gates were re-executed by the reviewer against the disk rather than read out of the handback, and every one reproduces at its reported value. Transport is proven at the PRIMARY strength rather than the R-0207 digest fallback: the reviewer's scratchpad `.remedy-wt/f082-r6-scratchpad.md` still exists and hashes to `7969531a3551f295d65449f1ea158aec15cff8c31dea7dcfd41a66775c9b149e`, byte-identical to both `.agent/authored/f082-r6.md` and `.agent/last_block.md` at 28701 bytes and 325 lines, inside the 400-line cap. The append was proven as `post == pre + add` and not by grep: the reviewer re-extracted FINDING-R412, FINDING-R413 and GATE-R5 from the COMMITTED block file, joined them with the blank-line separator the block ordered, and the result is byte-identical to the region C1 added, at sha256 `dd7e655df70edad090853460c9928ef4454c040d3664003ad9c09ea6e47f74af` over 8476 bytes, with the whole 115-line pre-C1 file an exact prefix of the 121-line result and the C1 numstat `6 0`, deletion column zero. Each slice's own digest reproduces the handback's table exactly — `ba1e5953…` 2384 bytes, `b10519d7…` 1594 bytes, `da638a3e…` 4495 bytes — and each is one physical line occurring once. The record counts re-measured are `^Gate: R5 — PASS` 1, `^- R-0412 — ` 1, `^- R-0413 — ` 1, `^## Steps` 1, `^Landed: ` 0 and `^Done: ` 0, so the worker authored no resolution of its own; the open set recomputed mechanically from the record is exactly FORTY-THREE with no duplicate, max id R-0413 and next free R-0414. Both context pairs are REWRITES and each measures FROM 1x before and 0x after with its TO 0x before and 1x after — the newline-inclusive reading the handback corrected the block's own note to, and the one that discriminates — with `.agent/context.md` at 55 lines, `.agent/plan.md` byte-equal to the PLAN slice as a whole file at 35 lines under the 50-line cap, zero BEGIN/END marker lines in all six non-block files, zero trailing-whitespace lines in any of them and every one ending in a newline. The change set is eight paths, every one inside the block's Change list and none outside it, the eighth being the handoff added by the commit that writes it (R-0149); the only path under `tests/orchestration/` is the new test file, so the gauntlet's own test files are byte-unmodified. Suites re-run by the reviewer at the branch head: the ten-file orchestration suite `284 passed`, and the arithmetic is closed independently — the same nine files WITHOUT the new one give `279 passed` at this head, so 279 + 5 new tests = 284 and no pre-existing test was lost; the canary plus the three contract readers `184 passed`; scoped ruff over the two new files `All checks passed!`; `python3 -m apps.cli.main integrity check --json` `passed: true`, `fail_count: 0` over 5 checks with `high_blockers_open` reporting no open blocker/high findings. The reviewer ran its OWN red-proof rather than accepting the handback's, in a disposable worktree at HEAD, and made it stronger than the ordered one: replacing `for order_id in order_ids` with `for order_id in sorted(order_ids)` in `dry_run_rows` turned TWO tests red, `test_rows_follow_order_ids_not_the_directory_sort` at the reported assertion `At index 0 diff: 'fx-01-pure-code-change' != 'fx-02-operator-command'` plus `test_unreadable_evidence_never_raises_and_takes_the_missing_row`, so the ordering guarantee is genuinely pinned and not merely asserted; the worktree was removed and pruned and `git worktree list` reads one line with `git status --porcelain` empty. Insertions per commit are 325, 257, 6, 16, 263 and 94, none over 500. `gh pr list --state open` is `[]`: no PR exists for this branch and none is created before closure. The code itself was read rather than trusted: `bench_dry_run.py` imports every gauntlet and bench symbol it uses and edits none, keeps `capability_bench.py`'s purity promise true by living in its own file, never re-decides a pass — each row's `passed` is the evaluator's own `flawless`, which the wiring test proves against a deliberately mixed recorded set rather than against a restated table — and documents its one deliberate absence, that a recorded run matching no requested id produces no row, where a reader would search for it. Two deviations, both declared and both accepted: the handback is 129 lines against the 60-line cap carrying its DECISION D15 stated cause with no section dropped, and the commit messages carry no trailer, matching this repository's history. One new finding, R-0414, and it charges the reviewer rather than the worker: a third superseded region of R-0412's own class stood in `.agent/context.md` after a block whose job was to retire that class, and the worker declared it in gate 7 instead of repairing it outside its ordered slices. No block condition was hit — no fabricated value, no false live indicator, no missing changed-files table, no unverified completion claim, no silent scope change.
--- END SLICE GATE-R6 ---

--- BEGIN SLICE CTXBUILT-FROM ---
R2's inventory settled the shape: the factoring is ADDITIVE, so the bench lands
as a NEW
`packages/orchestration/capability_bench.py` with
`tests/orchestration/test_capability_bench.py`, and no symbol moves out of any
gauntlet module. R3 additionally owns
--- END SLICE CTXBUILT-FROM ---

--- BEGIN SLICE CTXBUILT-TO ---
R2's inventory settled the shape: the factoring is ADDITIVE, so every bench
module is NEW and no symbol moves out of any gauntlet module — R3's
`capability_bench.py`, R4's `bench_orders.py`, R6's `bench_dry_run.py` and R7's
`bench_history.py`, each with its own test file under `tests/orchestration/`.
R3 additionally owns
--- END SLICE CTXBUILT-TO ---

--- BEGIN SLICE PLAN ---
# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0415. Open findings: forty-four — the thirty-two carried from F077, plus
R-0403 to R-0414 registered on this branch. `.agent/live_review.md` is the
source of truth for that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R7 records the R6 gate, registers R-0414, retires the last superseded region of
`.agent/context.md`, and builds T002 — the append-only history under the data
root's project area, the trend read back off it, the regression rules, and the
improving, flat and degrading goldens.

## Next Steps
1. R8 — T003: the `stats bench` CLI, model-context recording, and a
   fake-provider bench run end to end.
2. R9 the integration gate, R10 closure.

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

── C3 — T002: the history, the trend, the regression rules ───────────
ONE commit, all five files together — the module, its three goldens and its
tests are one logical step and none is meaningful alone.
  Subject: `feat(f082): add the append-only bench history and regression rules`

Write `packages/orchestration/bench_history.py`, NEW. It owns T002: "history
append + trend computation + regression rules". It reads and writes ONE file
and computes over what it reads; it runs no order and starts no clock.

Design, and the reasons, which belong in the module docstring in your own words:
  * A NEW module for the same reason R6 gave: `capability_bench.py` promises
    "no disk read, no network, no clock" and this one reads and writes a file.
  * ADDITIVE: import `BenchRecord` from
    `packages.orchestration.capability_bench` and `projects_dir` from
    `packages.orchestration.data_paths`. Move nothing, edit neither.
  * NO CLOCK, deliberately, and say so where a reader would search for it. Runs
    are grouped by an integer `run_seq` derived from the file itself, not by a
    timestamp, so a golden fixture is comparable byte for byte and a trend does
    not depend on when it was computed.
  * Unmeasured is `None` and `None` NEVER warns. A row whose `cost` or `wall_s`
    is absent is not a regression, it is an unmeasured field — the R-0178 and
    R-0407 discipline, applied to the comparison instead of to the row.

Public surface, named per the AGENTS.md discoverability conventions:
  * `BENCH_HISTORY_FILENAME = "bench_history.jsonl"`, `BENCH_HISTORY_VERSION = 1`,
    `REGRESSION_MULTIPLIER_DEFAULT = 1.5`, and one constant per warning kind:
    `REGRESSION_PASS_DROP = "pass_drop"`, `REGRESSION_COST = "cost_regression"`,
    `REGRESSION_WALL = "wall_regression"`. One spelling per concept, defined once.
  * `bench_history_path_for(project_id, root=None) -> Path` returning
    `projects_dir(root) / str(project_id) / BENCH_HISTORY_FILENAME`. Mirror
    `token_ledger.token_ledger_path_for` — read it first — including its warning
    in your own words: `project_id` is the registry UUID
    (`project_registry.RemyProject.id`), NOT the sha256 repo-path hash
    `worktrees.project_id` uses, and the two must never be swapped. This module
    never reads the data-root environment variable itself.
  * `BenchHistoryEntry` frozen dataclass: `run_seq: int` and `record: BenchRecord`.
    `to_json()` returns `{"bench_history_version": BENCH_HISTORY_VERSION,
    "run_seq": self.run_seq, "row": self.record.to_json()}` — the row NESTED
    under its own key, never flattened, so no future row field can collide with
    an envelope field.
  * `next_run_seq(path) -> int` — one more than the highest `run_seq` the file
    holds; `1` for a missing or empty file.
  * `append_bench_run(records, *, path) -> int` — assigns ONE `run_seq` to the
    whole batch, appends one JSON line per record in the order given, creates
    parent directories, and returns the assigned seq. It opens the file for
    APPEND and never for write: a rerun adds rows and never rewrites one, which
    is the feature file's acceptance criterion "History is append-only (rerun
    never rewrites old rows)". An empty `records` writes nothing and returns 0.
  * `load_bench_history(path) -> tuple[BenchHistoryEntry, ...]` — in file order.
    Reading NEVER raises, the same promise `bench_dry_run` makes and for the
    same reason: a missing file is `()`, and a line that is not JSON, not an
    object, or carries no usable `row` is SKIPPED, so one corrupt line costs one
    row instead of the whole history.
  * `BenchRegression` frozen dataclass: `kind: str`, `order_id: str`,
    `series: str`, `latest: float`, `baseline: float`,
    `multiplier: float | None` (`None` for a pass drop, which has no multiplier),
    plus `describe() -> str` naming the ORDER and both NUMBERS — the acceptance
    criterion is "warns with order and numbers", so a warning that names only
    the order does not meet it.
  * `bench_regressions(entries, *, series, multiplier=REGRESSION_MULTIPLIER_DEFAULT)
    -> tuple[BenchRegression, ...]` — compare the LATEST run of that series
    against the TRAILING median of every earlier run of it. Rules, and nothing
    beyond them:
      - Entries of other series are ignored entirely. Fewer than two runs in the
        series → `()`: a first run has nothing to regress against.
      - Per order id present in the latest run, in that run's row order, emit at
        most one of each kind in the fixed order pass, cost, wall.
      - `REGRESSION_PASS_DROP` when the latest row's `passed` is `False` and the
        order's trailing pass rate is above 0. `latest` is 0.0, `baseline` is
        that trailing rate. `passed is None` never warns.
      - `REGRESSION_COST` when the latest row's cost total — `sum` of its
        values — exceeds `multiplier` times the median of the order's trailing
        cost totals. Rows with `cost is None` are excluded from both sides; no
        trailing cost means no warning.
      - `REGRESSION_WALL`, identically, over `wall_s`.
  * A private `_median` over a non-empty sorted sequence, mean of the middle two
    on an even count. Say in one line why it is the median and not the mean: one
    catastrophic run must not raise the bar it is later compared against.

Write the three goldens under `tests/orchestration/fixtures/bench_history/`,
each a `.jsonl` file of THREE runs over the SAME two order ids, written in the
exact line shape `BenchHistoryEntry.to_json()` produces:
  * `flat.jsonl` — identical numbers in all three runs, both orders passing.
  * `improving.jsonl` — cost and wall falling run over run, both orders passing.
  * `degrading.jsonl` — runs 1 and 2 match `flat.jsonl`'s numbers; in run 3 ONE
    named order flips `passed` to `false` AND carries a cost total and a
    `wall_s` above 1.5x its own trailing median, while the OTHER order is
    unchanged. So the degrading file must warn about exactly one order and the
    flat file about nothing.

Write `tests/orchestration/test_bench_history.py`, NEW. Cover at least:
  1. Append-only, proven as bytes: append run 1 to a `tmp_path` file, read the
     file's bytes, append run 2, and assert the new bytes START WITH the old
     bytes. Assert the two returned seqs are 1 then 2. Do not prove this with a
     line count.
  2. `bench_history_path_for("some-id", root=tmp_path)` equals
     `tmp_path / "projects" / "some-id" / "bench_history.jsonl"`.
  3. A file whose second line is `{not json` loads the surrounding rows and
     raises nothing; a path that does not exist loads as `()`.
  4. `flat.jsonl` → `bench_regressions(...) == ()`.
  5. `improving.jsonl` → `()`.
  6. `degrading.jsonl` → non-empty; every returned regression names the ONE
     degraded order and no other; the kinds returned include the pass drop, the
     cost and the wall; and one `describe()` string CONTAINS that order id and
     the string form of its latest number. Read the expected numbers off the
     golden inside the test rather than restating them as literals.
  7. A history holding only run 1 returns `()`.

If any of this cannot be built as described — a symbol is not where this block
says, a signature differs — STOP, commit what is green, and report the exact
blocker in the handback. Do not invent a different design and do not edit any
gauntlet or existing bench file to make it fit.

── C4 — handback ─────────────────────────────────────────────────────
Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. Name, as the
FIRST action of the next session, `docs/agents/self_drive_protocol.md` Phase 1
rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2's Open PR Gate. State
that F082 is MID-FEATURE, that no PR exists for this branch and none is created
until closure, and that the next round is R8. Under 60 lines, or carry a
DECISION D15 stated-cause line naming the real count and the mandated content
that caused it. Commit and push.
  Subject: `chore(f082): handback R7`

── Gates — run every one, report the REAL value ──────────────────────
1.  `git status --porcelain` → EMPTY at handback. `git worktree list` → 1 line,
    as it reads AT HANDBACK.
2.  Transport, as a PROPERTY (R-0408): prove the scratchpad,
    `.agent/authored/f082-r7.md` and `.agent/last_block.md` are byte-identical
    and report the shared sha256 and the line count, which must be at or under
    400. Any means; report the digest.
3.  `.agent/STOP` — ABSENT or PRESENT, at round start AND at handback.
4.  Append proof: the first 121 lines of the new `.agent/live_review.md` equal
    the pre-C1 file, proven as `post == pre + add` byte-wise and not by grep.
    Report the C1 numstat for that path; DELETION column 0. Report the physical
    line count of FINDING-R414 and GATE-R6; each must be exactly 1.
5.  `grep -c "^Gate: R6 — PASS" .agent/live_review.md` → 1; `^- R-0414 — ` → 1;
    `^## Steps` → 1; `^Landed: ` → 0; `^Done: ` → 0.
6.  Open set recomputed mechanically — `^- R-[0-9]\+ — ` paragraphs minus
    `^Done: R-[0-9]\+ — ` lines. Expect FORTY-FOUR; name every id; report
    duplicates as none or name them; report max and next free.
7.  The CTXBUILT pair, gated as a PROPERTY because a count alone is brittle
    here: prove `post == pre.replace(FROM, TO)` byte-wise over
    `.agent/context.md`, and report CTXBUILT-FROM 1x before and 0x after and
    CTXBUILT-TO 0x before and 1x after, each measured WITH the terminating
    newline. Report `wc -l .agent/context.md`. Then re-read the file end to end
    and report whether ANY other sentence still names which modules this feature
    builds, or still says five orders are owed, or maps a round to another
    round's work — if one does, report it, do not repair it outside this pair.
8.  `wc -l .agent/plan.md` → under 50. Report it.
9.  The `.agent/context.md` contract readers: it must still carry
    `## Active Branch` with a `feature/` slug, the substring `Steps`, a roadmap
    F-id and the word `pytest` or `resource`. Report each.
10. `git diff --name-only 18bc4945..HEAD` → report every path and COUNT them
    mechanically, stating the count. The Change list is a CEILING: every path
    reported appears in it. Name any path present that it does not contain —
    there must be none.
11. `git diff --name-only 18bc4945..HEAD -- tests/orchestration/` → report every
    path. Each one must be either `tests/orchestration/test_bench_history.py` or
    under `tests/orchestration/fixtures/bench_history/`. No existing gauntlet or
    bench test file may appear; report the property, not just the count.
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
    measured those files WITHOUT the new one at `18bc4945` today: 284 passed.
    Report the real total and the arithmetic — it must be 284 plus the number of
    tests you wrote, and no pre-existing test may be lost.
13. `python3 -m pytest tests/cli/test_golden_path.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_test_runner.py -q` → exit 0. Reviewer baselines
    re-measured at `18bc4945` today: 42 for the canary and 142 for the three
    readers, so 184.
14. `python3 -m ruff check packages/orchestration/bench_history.py
    tests/orchestration/test_bench_history.py` → exit 0. Repository-wide ruff is
    RED on main and is NOT a gate (R-0364); this is scoped to the two Python
    files R7 owns. The reviewer ran the same command over the two R6 files at
    `18bc4945` today and it printed `All checks passed!`.
15. Red-proof, in a DISPOSABLE worktree under `.remedy-wt/` only (G5, §4 item
    10), never in the primary checkout: make `append_bench_run` open its file
    with mode `"w"` instead of `"a"` and report which test fails and its
    assertion. Order the PROPERTY, not a colour: if NO test fails, say so
    plainly — that is a real finding about test 1 and the reviewer wants it, not
    a green word. Remove and prune the worktree; `git worktree list` must read
    one line afterwards.
16. `python3 -m apps.cli.main integrity check --json` → `passed: true`,
    `fail_count: 0`, `check_count: 5`. Report the `high_blockers_open` message.
17. `gh pr list --state open --json number,headRefName` → report it verbatim.
    It must be `[]`: no PR is created for this branch until closure.
18. Report each commit's `git show --numstat <sha>` insertion total. If any
    exceeds 500, declare it in the handback with the reason.

Transport proof: state, for each of FINDING-R414, GATE-R6, CTXBUILT-FROM,
CTXBUILT-TO and PLAN, that it was extracted from the COMMITTED
`.agent/authored/f082-r7.md` and applied disk-to-disk, with its sha256 and byte
length, and the proof that the applied region equals it. CTXBUILT is a REWRITE:
its TO does not contain its FROM. Confirm no BEGIN/END marker line reached any
target file. Scan every file you touched for trailing whitespace and report the
result.
