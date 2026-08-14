── STEP R9/12 — F082 Self-benchmark (record R8, retire the last stale claim, close the session) ──
Goal:        Record the R8 gate, register R-0417, retire the one stale sentence
             R8's own gate 11 forbade it from fixing, re-sync the plan, and
             leave the branch fully gated so the NEXT session starts on a
             reviewed round instead of an open one.
Bundle:      C0a/C0b save this block · C1 the R8 verdict and one finding,
             persisted FIRST · C2 the docstring pair · C3 the plan re-sync ·
             C4 handback.
Change:      .agent/live_review.md, .agent/context.md, .agent/plan.md,
             .agent/authored/f082-r9.md, .agent/last_block.md,
             .agent/handoff.md, tests/orchestration/test_bench_history.py
             (EDITED, one docstring sentence). NOTHING else. No file under
             `packages/` changes. No new test, no new fixture, no order file.
Constraints: Findings persist FIRST (planner_reviewer_prompt.md §4 item 4).
             Never write a `Done:` or `Landed:` paragraph of your own. Every
             authored slice is applied disk-to-disk out of the COMMITTED block
             file, never retyped. Push after every commit. Never merge, never
             force-push, never work on main. Create NO pull request: F082 is
             mid-feature and its PR is created at closure, not before.
             This round DELIBERATELY carries no zero-deletion gate on the test
             file: R8's did, and that is what made the stale sentence
             unfixable (R-0417). The eight test FUNCTIONS stay byte-unmodified;
             only the module docstring changes.
Done when:   the gates at the end of this block all pass, with their real
             values reported.
Handback:    completion report + rewrite .agent/handoff.md
──────────────────────────────────────────────────────────────────────

── C0 — save the block, in TWO commits ───────────────────────────────
The reviewer's scratchpad original is at `.remedy-wt/f082-r9-scratchpad.md`.
Saving it to both targets in ONE commit costs roughly twice its line count in
insertions (findings R-0381, R-0399). Split it unconditionally, and retype
neither target:

C0a. Copy the scratchpad byte for byte to `.agent/authored/f082-r9.md`.
     Commit that file ALONE.
     Subject: `chore(f082): save the R9 block verbatim`
C0b. Copy the COMMITTED `.agent/authored/f082-r9.md` — not the scratchpad —
     byte for byte to `.agent/last_block.md`. Commit that file ALONE.
     Subject: `chore(f082): mirror the R9 block into last_block`

── C1 — the R8 verdict and one finding ───────────────────────────────
ONE commit, the FIRST after C0. `.agent/live_review.md`, APPEND ONLY, in this
order, separated by exactly one blank line, each exactly ONE physical line:
FINDING-R417, then GATE-R8. Nothing above the append may move — prove it
against the pre-C1 revision over the file's existing 134 lines.
  Subject: `docs(f082): record the R8 verdict and register R-0417`

── C2 — retire the stale docstring sentence ──────────────────────────
ONE commit. One REWRITE pair, DOCSTR, in
`tests/orchestration/test_bench_history.py`. Its FROM spans four physical lines
of the module docstring and ends on a real line boundary. The eight test
functions and every helper stay byte-unmodified; this commit touches the
docstring and nothing else.
  Subject: `docs(f082): correct the golden count in the bench history docstring`

── C3 — re-sync the plan and the context step map ────────────────────
ONE commit. `.agent/plan.md` FULL REPLACEMENT with the PLAN slice, and one
REWRITE pair, CTXSTEPS3, in `.agent/context.md`. Do NOT touch the `## Steps`
heading above it: the dashboard contract test asserts that substring.
  Subject: `docs(f082): re-sync the plan and the step map for R10`

--- BEGIN SLICE FINDING-R417 ---
- R-0417 — Low — R8's gate 11 ordered the DELETION column of `tests/orchestration/test_bench_history.py` to be 0, to protect the eight existing tests from being edited while two were added, and that gate made a sentence the same round falsified impossible to repair. The module docstring opens "The three goldens under ``fixtures/bench_history/`` are three runs over the same two order ids"; R8's C3 added `varied.jsonl`, a FOURTH golden of FOUR runs over ONE order id, so both halves of the sentence became wrong in the commit that added the file, and correcting it needs exactly one deleted line, which the gate forbade. The worker took the ordered constraint, declared the residual in the handback, and repaired nothing outside its slices — the fourth consecutive round in which a worker has declared a stale claim its block did not order and the fourth in which the declaration was correct (R-0412, R-0414, R-0416 and this one). The defect is the REVIEWER's twice over: once for a zero-deletion gate that could not coexist with the round's own change, and once for the class itself, because this is the same stale-claim class those three earlier findings already registered and the counter-measures they carry are aimed at `.agent/**` state files rather than at every file a round makes stale. Registering a fifth finding for a fifth instance would be the wrong answer; the class needs a GATE, not another paragraph. The counter-measure, binding from R10 on and REPLACING the file-scoped halves of R-0412, R-0414 and R-0416 rather than adding to them: (1) a zero-deletion gate may only be ordered over regions the round does not make stale, and where a round changes what a file's prose asserts, the block orders the prose pair in the SAME commit; (2) every block's gate list carries one standing staleness gate — for each file the round touched, re-read it end to end and report every sentence that states a count, a list of modules, a round map or a completion, together with whether it still holds — so the class is measured every round instead of discovered by a worker and registered by the reviewer one round later. R9 retires this sentence and adds that gate. OPEN.
--- END SLICE FINDING-R417 ---

--- BEGIN SLICE GATE-R8 ---
Gate: R8 — PASS, with one new finding, the reviewer's. Verification tier: round gate plus the state-file contract readers plus the canary; no full-suite claim is made and none is owed. All eighteen ordered gates were re-executed by the reviewer against the disk rather than read out of the handback, and every one reproduces at its reported value. Transport is proven at PRIMARY strength: the scratchpad `.remedy-wt/f082-r8-scratchpad.md`, `.agent/authored/f082-r8.md` and `.agent/last_block.md` are byte-identical at shared sha256 `9435c875acdf6ea2671efea0931afc66d61d3bbb61750fc517980c284bee5dd0`, 30466 bytes and 312 lines, inside the 400-line cap. The append was proven as `post == pre + add` and not by grep: the reviewer re-extracted FINDING-R415, FINDING-R416, DECISION-D4 and GATE-R7 from the COMMITTED block file, joined them with the blank-line separator the block ordered, and the result is byte-identical to the region C1 added at sha256 `2b19ac8680bd0ddd9afe59542f3ffb49eea64105aef386380eb62d530be10482`, with the whole 125-line pre-C1 file an exact prefix of the 134-line result and the C1 numstat `9 0`, deletion column zero. Both context pairs were gated as a PROPERTY: `pre.replace(SCOPE_FROM, SCOPE_TO).replace(STEPS_FROM, STEPS_TO) == post` holds byte-wise with each FROM 1x before and 0x after, `.agent/context.md` at 59 lines keeping every contract reader, and `.agent/plan.md` byte-equal to the PLAN slice as a whole file at 36 lines. The record counts are `^Gate: R7 — PASS` 1, `^- R-0415 — ` 1, `^- R-0416 — ` 1, `^## DECISION F082 D4` 1, `^Landed: ` 0 and `^Done: ` 0, so the worker authored no resolution of its own; the open set recomputed mechanically is exactly FORTY-SIX with no duplicate, max R-0416 and next free R-0417. The change set is eight paths, every one inside the block's Change list, and `git diff --name-only 20f101b0..HEAD -- packages/` is EMPTY, so the promise that no production module changed holds exactly. Suites re-run by the reviewer at the branch head: the eleven-file orchestration suite `294 passed`, closing against the reviewer's own pre-round measurement of 292 for the same files, so 292 + 2 = 294 and no pre-existing test was lost; the canary plus the three contract readers `184 passed`; scoped ruff `All checks passed!`; `integrity check --json` `passed: true`, `fail_count: 0` over 5 checks. Insertions per commit are 312, 203, 9, 21, 44 and 152, none over 500, and `gh pr list --state open` is `[]`. The load-bearing gate is 15 and the reviewer ran BOTH mutations itself in a disposable worktree at `4b0d0db0` rather than accepting the handback, reverting the first before applying the second: deleting the threshold multiplier fails `test_a_larger_multiplier_silences_the_same_history` with `1 failed, 9 passed`, and replacing `_median`'s body with the mean fails BOTH that test and `test_the_trailing_median_ignores_one_catastrophic_run` with `2 failed, 8 passed`. Each of those mutations left `8 passed` before this round, so R-0415's blindness is genuinely closed and not merely asserted; the worktree was removed and pruned and the primary checkout is clean. The new fixture is what does the work and it was read rather than trusted: `varied.jsonl` carries trailing cost totals 1000, 1000 and 4000 whose median is 1000 and whose mean is 2000, and the test asserts the two DIFFER before asserting which one the rule used, so a later edit that flattens the fixture fails loudly instead of going blind again — that non-vacuity guard is the part worth keeping. One observation costs no id: the worker reported gate 10 as seven paths where the reviewer measures eight, because the worker counted before C4 wrote the handoff, which a handoff cannot table for itself (R-0149); the per-commit table names all eight, nothing is hidden, and the difference is a reporting moment rather than a scope change. Three deviations, all declared and all accepted: the handback is 190 lines against the 60-line cap carrying its DECISION D15 stated cause with no section dropped, the commit messages carry no trailer, and the denied-command routes were named per R-0408. The fourth declaration is the new finding R-0417 and it charges the reviewer, not the worker: R8's own gate 11 froze the deletion column of the test file, which made the module docstring's "three goldens" unrepairable in the round that made it wrong. No block condition was hit — no fabricated value, no false live indicator, no missing changed-files table, no unverified completion claim by the worker, no silent scope change.
--- END SLICE GATE-R8 ---

--- BEGIN SLICE DOCSTR-FROM ---
The three goldens under ``fixtures/bench_history/`` are three runs over the same
two order ids, written in exactly the line shape ``BenchHistoryEntry.to_json()``
produces. They carry no timestamp, so they are comparable byte for byte and
these tests do not depend on when they run.
--- END SLICE DOCSTR-FROM ---

--- BEGIN SLICE DOCSTR-TO ---
The goldens under ``fixtures/bench_history/`` are written in exactly the line
shape ``BenchHistoryEntry.to_json()`` produces. Three of them — ``flat``,
``improving`` and ``degrading`` — are three runs over the same two order ids;
``varied`` is four runs over one order id and is the only one whose trailing
values are not all equal, which is what lets a test see the trailing MEDIAN and
the threshold multiplier at all (R-0415). None carries a timestamp, so they are
comparable byte for byte and these tests do not depend on when they run.
--- END SLICE DOCSTR-TO ---

--- BEGIN SLICE CTXSTEPS3-FROM ---
regions and close T001 with the dry run ✅ → R7 T002 the append-only history,
the trend and the regression rules ✅ → R8 record the R7 verdict, complete this
sweep and pin the regression threshold → R9 T003 the stats bench CLI, model
context and a fake-provider run → R10 the integration gate → R11 closure.
--- END SLICE CTXSTEPS3-FROM ---

--- BEGIN SLICE CTXSTEPS3-TO ---
regions and close T001 with the dry run ✅ → R7 T002 the append-only history,
the trend and the regression rules ✅ → R8 complete the context sweep and pin
the regression threshold ✅ → R9 record the R8 verdict and retire the last
stale claim → R10 T003 the stats bench CLI, model context and a fake-provider
run → R11 the integration gate → R12 closure.
--- END SLICE CTXSTEPS3-TO ---

--- BEGIN SLICE PLAN ---
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
R9 records the R8 gate, registers R-0417, retires the stale golden-count
sentence in the bench-history test docstring, and re-syncs the plan. T001 and
T002 are built and gated; T003 is the only slice left.

## Next Steps
1. R10 — T003: the `stats bench` CLI, model-context recording, and a
   fake-provider bench run end to end. Begin with an inspect-the-shape pass over
   `apps/cli/commands/stats_ledger_cmd.py` and the CLI registration path before
   authoring the change set — the ground is unknown and the planning contract
   sanctions a shrunken step for exactly that.
2. R11 the integration gate, R12 closure.

## Risks
- The delivered order set is three, not the Design's five (R-0411). Closure
  may not quote five, and DECISION F082 D3 binds the recovery to a
  bench-owned fixture rather than an edit to the gauntlet's template.
- The freeze holds against a file-side edit only (R-0410). The Built State
  states that threat model rather than quoting the acceptance criterion whole.
- `repair_rounds` is `None` at every row by construction (R2 Q7). The trend has
  no repair-round series to regress on, and T003's report says so rather than
  printing a zero.
- Six of the last seven findings are reviewer-block defects, not worker
  defects. R-0417's standing staleness gate is the counter-measure; if R10 also
  registers one of this class, the block format itself needs re-planning.
--- END SLICE PLAN ---

── C4 — handback, and the session ends here ──────────────────────────
Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. This is the
LAST round of this session, so the handoff is the only return channel and the
next session starts from it. It must state:
  * The FIRST action of the next session is
    `docs/agents/self_drive_protocol.md` Phase 1 rule 1 — re-read `.agent/STOP`
    from disk — BEFORE rule 2's Open PR Gate.
  * F082 is MID-FEATURE. No PR exists for `feature/f082-self-benchmark` and
    none is created until closure; gate 16 proves `gh pr list --state open` is
    `[]`.
  * T001 and T002 are built AND gated; R8's verdict is on disk at
    `^Gate: R8 — PASS`. The next round is R10 — T003, and it begins with an
    inspect-the-shape pass, not with a change set.
  * R9's OWN verdict has no on-disk gate entry by construction
    (planner_reviewer_prompt.md §4 item 13): the round that records a verdict
    cannot record the gate on itself, so R9's verdict lives in this handoff and
    in the reviewer's completion report. That absence is the TERMINATOR, not a
    missing gate — do not open a repair round to close it.
Under 60 lines, or carry a DECISION D15 stated-cause line naming the real count
and the mandated content that caused it. Commit and push.
  Subject: `chore(f082): handback R9`

── Gates — run every one, report the REAL value ──────────────────────
1.  `git status --porcelain` → EMPTY at handback. `git worktree list` → 1 line,
    as it reads AT HANDBACK.
2.  Transport, as a PROPERTY (R-0408): prove the scratchpad,
    `.agent/authored/f082-r9.md` and `.agent/last_block.md` are byte-identical
    and report the shared sha256 and the line count, which must be at or under
    400. Any means; report the digest.
3.  `.agent/STOP` — ABSENT or PRESENT, at round start AND at handback.
4.  Append proof: the first 134 lines of the new `.agent/live_review.md` equal
    the pre-C1 file, proven as `post == pre + add` byte-wise and not by grep.
    Report the C1 numstat for that path; DELETION column 0. Report the physical
    line count of FINDING-R417 and GATE-R8; each must be exactly 1.
5.  `grep -c "^Gate: R8 — PASS" .agent/live_review.md` → 1; `^- R-0417 — ` → 1;
    `^## Steps` → 1; `^Landed: ` → 0; `^Done: ` → 0.
6.  Open set recomputed mechanically — `^- R-[0-9]\+ — ` paragraphs minus
    `^Done: R-[0-9]\+ — ` lines. Expect FORTY-SEVEN; name every id; report
    duplicates as none or name them; report max and next free.
7.  The DOCSTR pair, as a PROPERTY: prove
    `post == pre.replace(DOCSTR_FROM, DOCSTR_TO)` byte-wise over
    `tests/orchestration/test_bench_history.py`, and report FROM 1x before and
    0x after, TO 0x before and 1x after, measured WITH the terminating newline.
    Then report `git diff --numstat` for that path across THIS commit alone: the
    deletion column is EXPECTED to be non-zero here, which is the whole point of
    R-0417 — report the real number, do not treat it as a failure.
8.  The CTXSTEPS3 pair, as a PROPERTY: prove
    `post == pre.replace(CTXSTEPS3_FROM, CTXSTEPS3_TO)` byte-wise over
    `.agent/context.md` with the same before/after counts. Report
    `wc -l .agent/context.md` and `wc -l .agent/plan.md` (under 50).
9.  The `.agent/context.md` contract readers: `## Active Branch` with a
    `feature/` slug, the substring `Steps`, a roadmap F-id, and `pytest` or
    `resource`. Report each.
10. STANDING STALENESS GATE (R-0417, and this is its first run). For EVERY file
    this round touched, re-read it end to end and report every sentence that
    states a count, a list of modules, a round map, or a completion — and
    whether each still holds after this round's own commits. Name each one and
    its file. Report them all; repair nothing outside the ordered pairs. If one
    no longer holds, say so plainly: that is the finding this gate exists to
    surface a round earlier than a worker's declaration would.
11. `git diff --name-only 4b0d0db0..HEAD` → report every path and COUNT them
    mechanically, stating the count and the MOMENT you measured it (before or
    after C4). The Change list is a CEILING: every path reported appears in it.
    Report `git diff --name-only 4b0d0db0..HEAD -- packages/` separately; it
    must be EMPTY.
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
    measured those eleven files at `4b0d0db0` today: 294 passed. This round adds
    no test and removes none, so the expected total is 294 exactly. Report the
    real total; any other number is a finding, not a rounding.
13. `python3 -m pytest tests/cli/test_golden_path.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_test_runner.py -q` → exit 0. Reviewer baselines
    re-measured at `4b0d0db0` today: 42 for the canary and 142 for the three
    readers, so 184.
14. `python3 -m ruff check tests/orchestration/test_bench_history.py` → exit 0.
    Repository-wide ruff is RED on main and is NOT a gate (R-0364). The reviewer
    ran this same command over that file at `4b0d0db0` today and it printed
    `All checks passed!`.
15. `python3 -m apps.cli.main integrity check --json` → `passed: true`,
    `fail_count: 0`, `check_count: 5`. Report the `high_blockers_open` message.
16. `gh pr list --state open --json number,headRefName` → report it verbatim.
    It must be `[]`: no PR is created for this branch until closure.
17. Report each commit's `git show --numstat <sha>` insertion total. If any
    exceeds 500, declare it in the handback with the reason.
No mutation red-proof is ordered this round and none is owed: R9 changes no
executable line. Ordering one would be ordering a colour over unchanged code,
which R-0364 and R-0252 both forbid.

Transport proof: state, for each of FINDING-R417, GATE-R8, DOCSTR-FROM,
DOCSTR-TO, CTXSTEPS3-FROM, CTXSTEPS3-TO and PLAN, that it was extracted from the
COMMITTED `.agent/authored/f082-r9.md` and applied disk-to-disk, with its sha256
and byte length, and the proof that the applied region equals it. DOCSTR and
CTXSTEPS3 are both REWRITES: neither TO contains its own FROM. Confirm no
BEGIN/END marker line reached any target file. Scan every file you touched for
trailing whitespace and report the result.
