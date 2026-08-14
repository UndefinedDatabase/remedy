── STEP R10/13 — F082 Self-benchmark ─────────────────────────────────────────
Goal:        Record the R9 verdict, split T003 into a read half and a write half
             as DECISION F082 D5, retire the branch's largest stale sentence,
             and build the read half: `remedy stats bench` over the append-only
             history, naming the order and the numbers on every regression.
Bundle:      C0a save this block · C0b mirror it · C1 GATE-R9 + DECISION-D5
             appended to the review record · C2 retire the stale `## Steps` map
             · C3 the bench_cmd module + its catalog entry + its registration
             · C4 tests/cli/test_stats_bench.py · C5 plan and context re-sync
             · C6 handback.
Change:      This list is a CEILING. Nothing outside it.
             - .agent/authored/f082-r10.md   (C0a, new)
             - .agent/last_block.md          (C0b)
             - .agent/live_review.md         (C1 append, C2 pair)
             - apps/cli/commands/bench_cmd.py    (C3, NEW module)
             - apps/cli/commands/__init__.py     (C3, two pairs below)
             - apps/cli/command_catalog.py       (C3, one pair below)
             - tests/cli/test_stats_bench.py     (C4, NEW test file)
             - .agent/plan.md, .agent/context.md (C5)
             - .agent/handoff.md             (C6)
             NOT in scope: packages/** — `git diff --name-only <BASE>..HEAD --
             packages/` must be EMPTY. No gauntlet file, no bench_history.py,
             no capability_bench.py, no bench_orders.py, no bench_dry_run.py.
             This round adds a READER over those modules and changes none.

Constraints:
 1. The read view CHANGES NO WRITE PATH. `stats bench` opens the history for
    reading and never appends, never creates it, never migrates it.
 2. `apps/cli/commands/bench_cmd.py` is a NEW module and not an addition to
    `stats_ledger_cmd.py`: that module's own docstring scopes it to "the
    per-project SQLite ledger", and the bench history is a JSONL file. A
    promise that is true is worth its own file — the same reason
    `bench_dry_run.py` exists rather than a function inside
    `capability_bench.py`. Test file name follows the source (AGENTS.md, Code
    Discoverability): `bench_cmd.py` ↔ `tests/cli/test_stats_bench.py` is the
    ONE exception, matching the existing `stats_ledger_cmd.py` ↔
    `tests/cli/test_stats_cost.py` pairing already in the repo.
 3. NO PRICE IS COMPUTED and NO ABSENCE PRINTS AS A ZERO. `BenchRecord.cost`
    is a token dict or None; `wall_s` is a float or None; `repair_rounds` is
    None at EVERY row by construction (capability_bench.py, the field's own
    comment: `repair_rounds_used` is dropped at the `JobExecution` boundary).
    An unmeasured figure prints a WORD, never `0` and never blank, in BOTH
    output modes — `stats_ledger_cmd.UNMEASURED` is the existing spelling and
    the reason is written in that module's docstring. Reuse the spelling by
    importing it; do not invent a second word for the same absence.
 4. A repair-round column that is None at every row is NOT rendered as a column
    of words. Say once, in a sentence, that no run records repair rounds yet
    and why. A column of identical placeholders is noise, not a measurement.
 5. `bench_regressions` is the ONLY source of warnings. Do not re-derive a
    threshold, do not re-implement the median, do not re-decide a pass.
    `BenchRegression.describe()` already names the order and both numbers,
    which is F082's acceptance criterion — render it, do not rewrite it.
 6. `--series` is OPTIONAL. When it is omitted, use the series of the highest
    `run_seq` in the file and NAME the chosen series in the output. When the
    file holds more than one series, the output also names the others it did
    not read. Never silently pick one of several.
 7. NO TEST-ONLY FLAG. There is no `--history` escape hatch. Tests reach the
    history the way a user does: `REMEDY_DATA_DIR` (tests/conftest.py) or the
    `root=` parameter `bench_history_path_for` already takes. A flag that
    exists only so a test can run is a finding.
 8. A MISSING HISTORY IS NOT AN EMPTY ONE. No file on disk prints a sentence
    saying nothing has been recorded yet, exactly as
    `_render_cost_human` does for an absent ledger. It never prints a table of
    zeros and never exits non-zero — an unrun bench is not an error.
 9. Fewer than two runs of a series yields NO warning; `bench_regressions`
    returns `()` there by construction and the output says why rather than
    printing "no regressions" as if a comparison had happened.
10. `stats.bench` is `action_class="read_only"`, `may_mutate_repo=False`,
    `may_execute_commands=False`, `supports_json=True`. It adds EXACTLY ONE
    handler key, `stats.bench`, and no other.
11. Every commit follows the AGENTS.md self-review loop and the Commit Gate.
    Insertions per commit stay under 500. No commit trailer, matching every
    prior commit on this branch.
12. `.agent/plan.md` stays under 50 lines and keeps `## Goal` and
    `## Next Steps`. `.agent/context.md` keeps `## Active Branch` with its
    `feature/` slug, the substring `Steps`, a roadmap F-id, and `pytest` or
    `resource` — grep every reader before saving (§4 item 11).
13. Apply every slice below DISK-TO-DISK out of the COMMITTED
    `.agent/authored/f082-r10.md`, never by retyping and never from this
    prompt after C0a. No `--- BEGIN SLICE` or `--- END SLICE` marker line may
    reach any target file. No target file gains a trailing-whitespace line.

────────────────────────── AUTHORED SLICES ──────────────────────────

--- BEGIN SLICE GATE-R9 --- (append to .agent/live_review.md, C1, ONE physical line)
Gate: R9 — PASS, with no new finding. Verification tier: round gate plus the state-file contract readers plus the canary; no full-suite claim is made and none is owed. All seventeen ordered gates were re-executed by the reviewer against the disk rather than read out of the handback, and every one reproduces at its reported value. Transport is proven at DIGEST-FALLBACK strength per planner_reviewer_prompt.md §4 item 9: the previous session's scratchpad did not survive into this one, so the proof is `.agent/authored/f082-r9.md` against `.agent/last_block.md`, which are byte-identical at shared sha256 `d2efd799c2de694506c18a0b1dcb23c5eccea322b1c0af30dc57eade5381e7ef`, 22136 bytes and 252 lines, inside the 400-line cap, and that digest is the one the R9 block recorded for itself. The append was proven as a PROPERTY and not by grep: over the committed revisions `7e31aae0^` and `7e31aae0`, `post.startswith(pre)` is TRUE byte-wise, the 134-line pre-C1 file is an exact prefix of the 138-line result, 6747 bytes were added and the C1 numstat is `4 0` with the deletion column zero. The record counts recomputed at HEAD are `^Gate: R8 — PASS` 1, `^- R-0417 — ` 1, `^Landed: ` 0 and `^Done: ` 0, so the worker authored no resolution of its own; the open set derived mechanically from every `^- R-\d+ — ` paragraph minus every `^Done: ` line is exactly FORTY-SEVEN with no duplicate, max R-0417 and next free R-0418. The change set is seven paths, every one inside the block's Change list, and `git diff --name-only 4b0d0db0..HEAD -- packages/` is EMPTY, so the promise that no production module changed holds exactly. The load-bearing gate is 7, and the reviewer checked the CLAIM rather than the replacement: the rewritten module docstring of `tests/orchestration/test_bench_history.py` says three goldens are three runs over the same two order ids while `varied` is four runs over one, and reading the four fixtures directly gives flat, improving and degrading at six rows each with `run_seq` {1,2,3} over `bench-01-cold-start` and `bench-02-repair-loop`, and `varied` at four rows with `run_seq` {1,2,3,4} over `bench-01-cold-start` alone — the sentence R-0417 was raised about is now true of the disk, which is the only thing that retires it. Suites re-run by the reviewer at the branch head: the eleven-file orchestration suite `294 passed`, matching the R8 head exactly since this round adds and removes no test; the canary plus the three contract readers `184 passed`; scoped ruff on the touched test file `All checks passed!`; `integrity check --json` `passed: true`, `fail_count: 0` over 5 checks with `no open blocker/high findings`. Insertions per commit measured by `git show --numstat` are 252, 166, 4, 7, 21 and 142, none over 500, and `gh pr list --state open` is `[]`. The state files hold their contracts: `.agent/plan.md` at 41 lines under the 50-line cap with `## Goal` and `## Next Steps`, `.agent/context.md` at 60 lines carrying `## Active Branch` with the slug `feature/f082-self-benchmark`, the substring `Steps`, the F-ids F077/F082/F105 and both `pytest` and `resource`, and zero trailing-whitespace lines across all seven touched files. Gate 10, the standing staleness sweep R-0417 created, ran for the first time and did the job it was made for: twenty-six sentences re-read, twenty holding and six not, and the handback declares all six rather than hiding them. The reviewer confirms the two that matter — this record's own `## Steps` map still promised five frozen orders and a run ending at R7, and the R9 block's Constraints still said eight test functions where the file has ten — and neither was repaired BECAUSE the block forbade widening, which is the correct behaviour and not a defect of the round. R10 retires the first of those two by ordered pair; the second was a property of a block that has already been superseded. No block condition was hit — no fabricated value, no false live indicator, no missing changed-files table, no unverified completion claim, no silent scope change. R9 is the cleanest round on this branch: it registered nothing new because there was nothing new to register.
--- END SLICE GATE-R9 ---

--- BEGIN SLICE DECISION-D5 --- (append to .agent/live_review.md, C1, after GATE-R9, separated by one blank line)
## DECISION F082 D5 — T003 is built in two halves, not one

Chosen: T003 splits into T003a, the `remedy stats bench` READ view over the
existing history (R10), and T003b, model-context recording plus a
fake-provider bench run end to end (R11). The integration gate moves to R12
and closure to R13.

Why: T003 as written is a CLI, a new recorded field on the write path, and a
run harness — three change sets across `apps/` and `packages/` that share no
file and no test. Reading is complete today: `load_bench_history`,
`bench_regressions` and `bench_history_path_for` all exist and are gated, so
the read half is a renderer over finished code and lands in one bounded
round. The write half needs a field that no `run.json` carries yet, which is
a different risk and deserves its own verdict. Six of the last seven findings
on this branch were reviewer-block defects; a smaller block is the direct
counter-measure, and the planning contract sanctions a shrunken step exactly
when the ground is unknown.

Alternatives considered: (a) T003 in one round — rejected, the change set
crosses `apps/` and `packages/` and would exceed the 500-line commit cap
without an inseparability reason; (b) the read view AFTER the write path —
rejected, the reader is what makes the writer observable, and building it
second means the write half is gated by tests it also authored.

How to reverse: delete this decision, restore the R10 line of the step map in
`.agent/context.md`, and order T003 whole. Nothing built under it is wasted
either way — the read view is required by the feature's Goal & Done sentence
regardless of when it lands.
--- END SLICE DECISION-D5 ---

--- BEGIN SLICE LRSTEPS-FROM --- (in .agent/live_review.md, C2 — REWRITE pair)
frozen orders and the record schema → R4 T002 history append, trend computation
and the regression rules with improving, flat and degrading goldens → R5 T003
the CLI, model-context recording and a fake-provider bench run end to end →
R6 the integration gate → R7 closure.
--- END SLICE LRSTEPS-FROM ---

--- BEGIN SLICE LRSTEPS-TO --- (C2)
frozen orders and the record schema → R4 T002 history append, trend computation
and the regression rules with improving, flat and degrading goldens → R5 to R9
the T002 build-out, its goldens and the verdicts on them → R10 T003a the stats
bench read view → R11 T003b model context and a fake-provider run → R12 the
integration gate → R13 closure. The frozen order set is THREE, not the five
this map first promised: finding R-0411 measured it and DECISION F082 D3 binds
the recovery to a bench-owned fixture. This map is rewritten whenever it stops
matching `.agent/context.md`; the standing gate R-0417 created is what catches
it.
--- END SLICE LRSTEPS-TO ---

--- BEGIN SLICE INIT1-FROM --- (in apps/cli/commands/__init__.py, C3 — REWRITE pair)
    from apps.cli.commands import (
        blocker,
--- END SLICE INIT1-FROM ---

--- BEGIN SLICE INIT1-TO --- (C3)
    from apps.cli.commands import (
        bench_cmd,
        blocker,
--- END SLICE INIT1-TO ---

--- BEGIN SLICE INIT2-FROM --- (in apps/cli/commands/__init__.py, C3 — REWRITE pair, tail of the `for mod in (...)` line)
mission_cmd, loop_cmd):
--- END SLICE INIT2-FROM ---

--- BEGIN SLICE INIT2-TO --- (C3)
mission_cmd, loop_cmd, bench_cmd):
--- END SLICE INIT2-TO ---

--- BEGIN SLICE CATALOG-FROM --- (in apps/cli/command_catalog.py, C3 — APPEND-shaped pair: the TO CONTAINS the FROM verbatim, so the FROM stays 1x after)
    # ── stats — the token ledger (F103) ──────────────────────────────────
--- END SLICE CATALOG-FROM ---

--- BEGIN SLICE CATALOG-TO --- (C3)
    # ── stats — the self-benchmark trend (F082) ──────────────────────────
    CommandEntry(
        command_id="stats.bench",
        group_id="stats",
        subcommand="bench",
        description=(
            "Capability trend from the append-only bench history: the last run, "
            "the series before it, and a regression warning naming the order and "
            "both numbers. Never runs the bench (read-only)."
        ),
        action_class="read_only",
        supports_json=True,
        related=("stats.cost", "stats.report"),
        args=(
            ArgDef("--series", "Which bench series to read (default: the series of the latest run)", required=False, is_option=True),
            ArgDef("--multiplier", "Warn when cost or wall time exceeds the trailing median by this factor (default: 1.5)", required=False, is_option=True),
            _PROJECT_SCOPE_OPT,
            _JSON_OPT,
        ),
        may_mutate_repo=False,
        may_execute_commands=False,
    ),
    # ── stats — the token ledger (F103) ──────────────────────────────────
--- END SLICE CATALOG-TO ---

--- BEGIN SLICE CTXSTEPS-FROM --- (in .agent/context.md, C5 — REWRITE pair)
the regression threshold ✅ → R9 record the R8 verdict and retire the last
stale claim → R10 T003 the stats bench CLI, model context and a fake-provider
run → R11 the integration gate → R12 closure.
--- END SLICE CTXSTEPS-FROM ---

--- BEGIN SLICE CTXSTEPS-TO --- (C5)
the regression threshold ✅ → R9 record the R8 verdict and retire the last
stale claim ✅ → R10 T003a the stats bench read view → R11 T003b model context
and a fake-provider run → R12 the integration gate → R13 closure. T003 split
into two halves at DECISION F082 D5; R10 marks R9 done and never itself.
--- END SLICE CTXSTEPS-TO ---

--- BEGIN SLICE PLAN --- (WHOLE-FILE replacement of .agent/plan.md, C5)
# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0418. Open findings: forty-seven — the thirty-two carried from F077, plus
R-0403 to R-0417 registered on this branch. `.agent/live_review.md` is the
source of truth for that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R10 records the R9 gate, splits T003 in two as DECISION F082 D5, retires this
branch's largest stale sentence, and builds T003a: the `remedy stats bench`
read view over the append-only history, with its catalog entry, its
registration and its own test file. T001 and T002 are built and gated.

## Next Steps
1. R11 — T003b: model-context recording per run and a fake-provider bench run
   end to end. The field no `run.json` carries yet is the risk; begin with an
   inspect-the-shape pass over the gauntlet's run writer before authoring a
   change set.
2. R12 the integration gate, R13 closure.

## Risks
- The delivered order set is three, not the Design's five (R-0411). Closure
  may not quote five, and DECISION F082 D3 binds the recovery to a
  bench-owned fixture rather than an edit to the gauntlet's template.
- The freeze holds against a file-side edit only (R-0410). The Built State
  states that threat model rather than quoting the acceptance criterion whole.
- `repair_rounds` is `None` at every row by construction (R2 Q7). The trend has
  no repair-round series to regress on, and T003a says so in one sentence
  rather than rendering a column of placeholders.
- Six of the last seven findings are reviewer-block defects, not worker
  defects. R-0417's standing staleness gate is the counter-measure; R9 ran it
  for the first time and it caught six stale sentences, so it works.
--- END SLICE PLAN ---

────────────────────────── DONE WHEN ──────────────────────────
Run every gate. Record its REAL output. "Green" as a word is a finding.
BASE is the SHA this round starts from: d08250ed.

 1. `git status --porcelain` EMPTY at handback; `git worktree list` back to
    exactly the primary checkout. Report both verbatim.
 2. TRANSPORT AS A PROPERTY: sha256 and byte length of the reviewer scratchpad
    `.remedy-wt/f082-r10-scratchpad.md`, of `.agent/authored/f082-r10.md` and
    of `.agent/last_block.md`. All three must be EQUAL. Prove byte equality
    itself, not the availability of a tool — `cmp` and `cp` are denied to this
    session class (R-0408); `sha256sum` plus a python3 `read_bytes()` equality
    is the route. Report the shared digest and the line count; it must be
    ≤ 400.
 3. `.agent/STOP` — report its presence at round START and again at handback.
    Absent both times. If it appears, finish the current commit and hand off.
 4. C1 APPEND PROOF: over the COMMITTED revisions `<C1>^` and `<C1>`, report
    whether `post == pre + add` holds BYTE-WISE, where `add` is GATE-R9 and
    DECISION-D5 joined exactly as committed. Report the C1 `--numstat`; its
    DELETION column must be 0.
 5. RECORD COUNTS in `.agent/live_review.md` at HEAD: `^Gate: R9 — PASS` must
    be 1 · `^## DECISION F082 D5` must be 1 · `^Landed: ` must be 0 ·
    `^Done: ` must be 0. Report each real number.
 6. OPEN SET RECOMPUTED MECHANICALLY, never carried forward: every
    `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line. Report the
    count, the max id, the next free id, and any duplicate. R10 registers no
    finding, so the expected count is FORTY-SEVEN and the next free id stays
    R-0418 — report the real numbers whatever they are.
 7. LRSTEPS PAIR AS A PROPERTY: report whether
    `post == pre.replace(LRSTEPS_FROM, LRSTEPS_TO)` holds byte-wise over the
    committed C2. Report LRSTEPS_FROM count before and after (1 then 0) and
    LRSTEPS_TO count after (1). This is a REWRITE and the FROM is gone after.
 8. CATALOG PAIR AS A PROPERTY: report whether
    `post == pre.replace(CATALOG_FROM, CATALOG_TO)` holds byte-wise over the
    committed C3. This pair is APPEND-SHAPED — the TO CONTAINS the FROM — so
    the FROM count is 1 BEFORE and 1 AFTER, and demanding 0 would be
    unmeetable by construction. Report `stats.bench` count in that file: 0
    before, 1 after. Report both INIT pairs the same way; both are REWRITES,
    so each FROM is 1x before and 0x after, and each TO is 1x after.
 9. STATE SLICES AS PROPERTIES, then the contract readers.
    (a) Report whether `post == pre.replace(CTXSTEPS_FROM, CTXSTEPS_TO)` holds
        byte-wise over the committed C5. REWRITE: FROM 1x before, 0x after;
        TO 1x after.
    (b) Report whether `.agent/plan.md` at HEAD BYTE-EQUALS the PLAN slice as a
        WHOLE FILE. Report its sha256 and its `wc -l`; it must be under 50.
    (c) CONTRACT READERS of `.agent/context.md` at HEAD: `## Active Branch`
        present and followed by a `feature/` slug · substring `Steps` present ·
        at least one roadmap F-id present · `pytest` present or `resource`
        present. `.agent/plan.md` keeps `## Goal` and `## Next Steps`. Report
        `wc -l` for `.agent/context.md`.
10. STANDING STALENESS GATE (R-0417, second run). Re-read every sentence in
    the files this round touched that states a COUNT, a module list, a
    round→step map, or a completion claim, and report for each whether it
    still holds at HEAD. Repair ONLY what the ordered pairs above cover; for
    anything else, report it and leave it. A sentence that no longer holds is
    the finding this gate exists to surface a round earlier than a worker's
    declaration would. State the number of sentences you checked.
11. CHANGE SET: `git diff --name-only d08250ed..HEAD` — report every path,
    COUNT them, and state whether you measured before or after C6. The Change
    list is a CEILING: every path reported appears in it. Report
    `git diff --name-only d08250ed..HEAD -- packages/` separately; it must be
    EMPTY.
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
    measured these eleven files at d08250ed today: 294 passed. R10 adds no
    test to them and removes none, so 294 is the expected total. Report the
    real number; any other is a finding, not a rounding.
13. `python3 -m pytest tests/cli/test_golden_path.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_test_runner.py -q` → exit 0. Reviewer baseline
    re-measured at d08250ed today: 184 passed. `test_dashboard_contract.py`
    calls `collect_all_handlers()`, so this bundle is the one that catches a
    broken registration.
14. `python3 -m pytest tests/test_command_catalog.py
    tests/cli/test_command_catalog.py tests/test_grouped_cli.py
    tests/cli/test_stats_cost.py tests/cli/test_cli_ux.py -q` → exit 0.
    Reviewer baseline re-measured at d08250ed today: 634 passed. These are the
    catalog and grouped-CLI contract guards; the new entry must satisfy them
    UNMODIFIED. If any of these five files needs an edit to go green, STOP and
    say so in the handback — that is a finding about the catalog entry, not a
    test to change.
15. `python3 -m pytest tests/cli/test_stats_bench.py -q` → exit 0. Report the
    real count. Then report `remedy stats bench --help` reached through
    `python3 -m apps.cli.main stats bench --help`, exit 0, and paste the real
    output — the command must be reachable through the actual parser, not only
    through its handler (R-0220: a green gate is not a working feature; check
    who calls the new code).
16. `python3 -m ruff check apps/cli/commands/bench_cmd.py
    apps/cli/commands/__init__.py apps/cli/command_catalog.py
    tests/cli/test_stats_bench.py` → exit 0. Repository-wide ruff is RED on
    main and is NOT a gate (R-0364). The reviewer ran this same command over
    the three EXISTING paths at d08250ed today and it printed
    `All checks passed!`.
17. `python3 -m apps.cli.main integrity check --json` → `passed: true`,
    `fail_count: 0`, `check_count: 5`. Report the `handler_import` message.
    The reviewer measured `handlers=336` at d08250ed; this round adds EXACTLY
    ONE handler key, so the expected message is `handlers=337`. Report the
    real value — a different number means more or fewer keys landed than the
    block ordered.
18. RED-PROOF, INSIDE A DISPOSABLE WORKTREE ONLY, never in the primary
    checkout (G5, §4 item 10). Add a worktree at HEAD under `.remedy-wt/`.
    There, replace the body of the branch that renders the regression
    warnings with `raise AssertionError("red-proof")`, run
    `python3 -m pytest tests/cli/test_stats_bench.py -q`, and REPORT WHICH
    tests fail and how many. Do not predict the count — report it. If NOTHING
    fails, say so plainly: that means the warning path is untested and it is
    a finding, not a pass. Remove and prune the worktree; gate 1 must then
    show the primary checkout clean.
19. `gh pr list --state open --json number,headRefName` → report verbatim. It
    must be `[]`: no PR is created for this branch until closure.
20. Report each commit's `git show --numstat <sha>` insertion total. If any
    exceeds 500, declare it in the handback with the inseparability reason
    BEFORE review. C6 cannot state its own numstat; report it in the
    completion report instead.

Handback:    Completion report + rewrite `.agent/handoff.md` per
             docs/agents/handback_template.md: feature and round, branch, the
             per-commit changed-files tables, the real verification values
             above, the item-status table with every C0a–C6 item and every
             gate 1–20 appearing exactly once, open-findings count, and the
             next expected action. Declare every deviation with its cause. The
             handoff repeats the Fortschritt line verbatim. Push after every
             commit. Create NO pull request.
──────────────────────────────────────────────────────────────────────────────
