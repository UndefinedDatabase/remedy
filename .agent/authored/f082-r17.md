── STEP R17/19 — F082 Self-benchmark ─────────────────────────────────────────
Goal:        Land the fake-provider bench run end to end: the missing entry
             point joining a campaign to a history, its no-network test, the ONE
             allowlist name DECISION F082 D9 promised, and the R-0427 repair.

Bundle:      C0a save this block · C0b mirror it · C1 GATE-R16 + FINDINGS-R429-430
             appended to the review record · C2 the entry point, a NEW production
             module authored from the contract below · C3 its NEW test file, also
             authored from a contract · C4 the allowlist gains one name · C5 the
             R-0427 docstring repair · C6 plan and context re-sync · C7 handback.

Change:      This list is a CEILING. Nothing outside it.
             - .agent/authored/f082-r17.md                          (C0a, new)
             - .agent/last_block.md                                 (C0b)
             - .agent/live_review.md                                (C1 append)
             - packages/orchestration/bench_run.py                  (C2, NEW)
             - tests/orchestration/test_bench_run.py                (C3, NEW)
             - tests/orchestration/test_bench_never_runs_implicitly.py (C4, one pair)
             - packages/orchestration/bench_history.py              (C5, one pair)
             - .agent/plan.md                                       (C6 whole-file)
             - .agent/context.md                                    (C6, three pairs)
             - .agent/handoff.md                                    (C7)
             NOT in scope: `docs/**`, `apps/**`, `scripts/**`, every gauntlet
             module, and every PRE-EXISTING test file except the pin at C4.
             `gauntlet_runner.py` is READ and IMPORTED, never edited (gate 18).

Constraints:
 1. THE FACTORING STAYS ADDITIVE. `bench_run.py` is NEW and only IMPORTS
    `run_campaign`, `RunnerDeps`, `load_bench_order_set`,
    `dry_run_from_order_set` and `append_bench_run`. No gauntlet module is
    edited — the R2 Q11 rule, and DECISION F082 D1's exception does not widen.
 2. NO FAKE PROVIDER IN PRODUCTION CODE. `bench_run.py` holds NO double, stub
    or test-only branch: it takes an injected `RunnerDeps` and an explicit
    history path, and the fake-provider deps live in the TEST file at C3. A
    production module that knows tests exist is a finding.
 3. THE ENTRY POINT CANNOT REACH THE OPERATOR'S ROOT BY DEFAULT — R11 Q6's
    blocker (4). `run_campaign` defaults `real_data_root` to
    `resolve_data_root()` and `bench_history_path_for` resolves through
    `data_paths.projects_dir`, so the entry point takes BOTH its data root and
    its history path as REQUIRED keyword arguments: a caller that forgets one
    gets a TypeError, not a write into the operator's real root. C3 property 5
    pins that.
 4. THE CLOCK IS ACKNOWLEDGED, NOT REMOVED. R11 Q6's blocker (3):
    `gauntlet_runner.py::run_order` calls `time.monotonic()` to fill
    `wall_seconds`, so `wall_s` is clock-derived even though the bench modules
    keep clocks out of themselves. `bench_run.py` adds NO clock and says so in
    one WHY line. Removing the runner's clock would be a gauntlet edit.
 5. THE SEAM SET IS LARGER THAN R11 Q6 NAMED, and this round records it. Q6
    named `plan_call_fn`, `move_call_fn` and `execute_fn`. A no-network run
    ALSO needs `make_project` (its default writes the project registry via
    `save_project`), `materialise` (its default shells out to `git`), and the
    four mission verbs `create_mission`, `plan_mission`, `run_mission`,
    `load_mission` — NINE seams, counted. Follow the shape of
    `tests/orchestration/test_gauntlet_runner.py::Recorder`, which already hands
    over exactly this set. READ IT FIRST.
 6. THE ALLOWLIST GAINS EXACTLY ONE NAME, `packages/orchestration/bench_run.py`,
    and that is the deliberate act DECISION F082 D9 described. Touch no other
    line of the pin file. The pin asserts callers EQUAL the allowlist, so an
    allowlisted module calling nothing ALSO fails — `bench_run.py` calls both
    guarded symbols, which is what makes the one name legitimate.
 7. Apply every REWRITE-PAIR slice DISK-TO-DISK out of the COMMITTED
    `.agent/authored/f082-r17.md`. No `--- BEGIN SLICE` / `--- END SLICE`
    marker line may reach any target file, and no target gains a
    trailing-whitespace line. C2 and C3 are authored by YOU from their
    contracts, not transported.
 8. Apply every slice VERBATIM. If a slice is wrong on arrival, apply it as
    ordered and DECLARE it — never silently repair it (R-0419). Reporting a
    reviewer's error is the behaviour this round rewards; R-0429 below is
    exactly that, found by the previous worker.
 9. Every commit follows the AGENTS.md self-review loop and the Commit Gate.
    Insertions per commit stay under 500. No commit trailer. DECISION F082 D1
    through D9 and every prior gate entry are time-stamped history and ARE NOT
    REWRITTEN; this round appends and supersedes nothing.

────────────────────────── AUTHORED SLICES ──────────────────────────

--- BEGIN SLICE GATE-R16 --- (append to .agent/live_review.md, C1, ONE physical line)
Gate: R16 — PASS, with two new findings, both of them the reviewer's own, and one of the two found by the worker and declared before the reviewer read the diff. Verification tier: round gate plus the canary; the round wrote NO production code, so the additive claim reduces to a restriction that is measured rather than argued — the range restricted to `docs/`, `apps/`, `packages/` and `scripts/` is EMPTY. All twenty-one ordered gates were re-executed by the REVIEWER against the disk rather than read out of the handback, and every reported value reproduces exactly. Transport is proven at PRIMARY strength: `.agent/authored/f082-r16.md` and `.agent/last_block.md` are byte-identical under python3 `read_bytes()`, sha256 `39cc8d563d1518ea1e7bb72c971f6c531d95f2f80c43077baa6fc96fa65836d8`, 32783 bytes, and the measured line count is 373 — exactly the number the block declared before emission, so R-0420's rule held for a third consecutive round. The C1 append is a PROPERTY: over the committed `da61d992^` to `da61d992` the reviewer re-derived that `post` equals `pre + NL + GATE + NL + FINDINGS + NL + DECISION` byte-wise, TRUE, with `pre` a prefix of `post`, the added region 11670 bytes and the numstat deletion column 0. Record counts at HEAD, line-anchored, are `^Gate: R15 — PASS` 1, `^- R-0427 — ` 1, `^- R-0428 — ` 1, `^## DECISION F082 D9` 1, `^## DECISION F082 D8` 1, `^## DECISION F082 D7` 1, `^Landed: ` 0 and `^Done: ` 0, and the open set recomputed mechanically is FIFTY-EIGHT with no duplicate, max R-0428 and next free R-0429. C6's context edit was proven as ONE composite exactly as R-0422 demands: `pre` with all three replacements applied EQUALS `post`, and each pair shows FROM 1x to 0x, TO 0x to 1x and `FROM in TO` False. `.agent/plan.md` byte-equals the PLAN slice as a whole file at sha256 `94d42d6fa260a72a56d45c57bb4959dd88e657de8ad0dc71b2bd9b273f7e0608`, 48 lines, under the AGENTS.md fifty-line cap, keeping `## Goal` and `## Next Steps`. The change set is seven paths, every one inside the block's Change list, and the range restricted to `tests/` is exactly the one new pin file. Marker lines reaching any target: 0. Trailing-whitespace lines gained in any target: 0. Suites re-run by the reviewer at the branch head: the new pin `6 passed` exit 0; the gauntlet's seven `276 passed` exit 0 and the pre-existing bench five `61 passed` exit 0, both UNCHANGED from their base values; `test_bench_model_context.py` `14 passed` exit 0; the canary plus the three contract readers `184 passed` exit 0; scoped `ruff check` `All checks passed!` exit 0; and `integrity check --json` `passed: true`, `fail_count: 0` over 5 checks with `handler_import` still `handlers=337`. Insertions per commit are 373, 286, 53, 250, 40 and 1, none over 500. `git status --porcelain` is empty, `git worktree list` is the single primary checkout, `.agent/STOP` is absent and `gh pr list --state open` is `[]`. The RED-PROOF was re-run by the reviewer in its own disposable worktree rather than trusted: a scratch module under `packages/` calling `append_bench_run` turned the pin's COLOUR to RED, failing `test_only_allowlisted_modules_call_the_bench_write_entry_points` with a message beginning "The bench gained an implicit caller: packages/orchestration/_reviewer_redproof_caller.py calls append_bench_run", and the worktree was removed with `git worktree list` back to one line. The reviewer then went PAST the ordered gates, because a gate list is a floor and R-0220 is the finding that says a green gate is not a working feature: the pin was probed in all three directions that matter, and it discriminates. A direct `ast.Name` call (`append_bench_run(...)` after a `from … import`) goes RED; an `ast.Attribute` call (`bench_dry_run.dry_run_from_order_set(...)`) ALSO goes RED, which the ordered red-proof alone would not have shown and which matters because R17's own driver uses one of the two forms; and a hostile module that IMPORTS the symbol, BINDS it to a name, mentions it in a docstring and names the other symbol in a string constant — calling neither — stays GREEN at `6 passed`. That last probe is the one a substring grep fails, and it is the difference between a pin and a grep. Both probe runs were confirmed by `pwd` and `git rev-parse --show-toplevel` to have executed inside the worktree, so the import path is proven and a green probe is not a probe of unmutated code (R-0337). The reviewer's own staleness spot-check of `.agent/context.md` initially reported the "240 the preferred target" sentence ABSENT; re-checking with whitespace normalised showed it PRESENT, the first reading having been defeated by a line wrap between "240 the" and "preferred". The worker's gate-21 report was right and the reviewer's first check was wrong, which is recorded here because a reviewer that reports its own near-miss is the only kind whose green means anything. No block condition was hit: no fabricated data, no false live indicator, no missing changed-files table, no unverified completion claim, no silent scope change.
--- END SLICE GATE-R16 ---

--- BEGIN SLICE FINDINGS-R429-430 --- (append to .agent/live_review.md, C1, after GATE-R16, one blank line between the gate and this slice)
- R-0429 — Low, REVIEWER-BLOCK DEFECT, CLAUSE-VS-CLAUSE, found by the WORKER while applying the R16 block and declared in the handback before the reviewer read the diff. The R16 block's Constraint 2 said "Properties 1 and 5 of the contract exist only to make a vacuous pass impossible", but the block's OWN contract list two hundred lines below made property 1 ANTI-VACUOUS, SYMBOLS and property 2 ANTI-VACUOUS, SCAN, with property 5 the import-time side effect. Both clauses were written by the reviewer, in one file, and they disagreed. The worker followed the CONTRACT — the correct choice, since the contract is the constructive text — but copied the constraint's wrong numbering into the new file's module docstring, and then caught it under the standing staleness gate and spent an extra commit, `3a0b1d77`, correcting one word. Low, because the shipped code is right and the cost was one line in one commit. It is registered because the CLASS is the expensive one: R-0331, R-0334, R-0353 and R-0356 are the same defect, the planner_reviewer_prompt §3 pre-emission checklist items 9 and 10 exist to catch it, and it still arrived. What those items miss is the case here — the two clauses are far apart, agree in TOPIC, and disagree only in an ORDINAL, which reads as correct on a linear pass and is only caught by resolving each numeral against the list it indexes. Standing rule from here, binding the reviewer: a block clause that cites a numbered item of its own contract by ORDINAL is checked by counting into the contract list and reading back what that ordinal actually names, in the same pass that measures the block. An ordinal is a cross-reference, and an unresolved cross-reference is the one error a careful linear read cannot see.

- R-0430 — Low, HANDOFF DEFERRED ITS OWN MEASURED LENGTH TO A CHANNEL THAT LEAVES NO DISK ARTIFACT, found by the reviewer while checking the R16 handback against AGENTS.md D15. The R16 handoff correctly declared a stated-cause overage of the 60-line cap and correctly named the mandated content that caused it — seven per-commit tables, twenty-one gate values and the item-status table, no section dropped — but where D15 requires the declaring line to name "its actual line count", the handoff instead said "Real measured length is recorded in the round's completion report". Under the split workflow that would be recoverable: the completion report is the text the worker hands to Window 1. Under `docs/agents/self_drive_protocol.md` there is no relay, the worker is a subagent whose report ends with the round, and the handoff is stated by that same protocol to be "the only return channel" — so the deferred number reached NO durable artifact and the real count, 132 lines, had to be re-measured by the reviewer from the file. Low, because the overage itself is legitimate, every mandated section is present, and the number is trivially recoverable by `wc -l`. It is registered because the CAUSE is the self-drive shape rather than carelessness: a rule written for a two-window workflow named a channel that the one-session protocol deleted, and the worker followed the rule as written. Standing rule from here: a handoff declaring a D15 overage states its own measured line count as a NUMERAL in the declaring line, and never forwards it to a completion report, a transcript or any channel that does not survive the session. Adding the numeral does not change the count, because it is written into a line that already exists.
--- END SLICE FINDINGS-R429-430 ---

--- BEGIN SLICE CTXSCOPE-R17 --- (in .agent/context.md, C6 — REWRITE pair)
Still to come,
the fake-provider bench run end to end, inventoried at R11 before it is built.
--- END SLICE CTXSCOPE-R17 ---

--- BEGIN SLICE CTXSCOPE-R17-TO --- (C6)
R17 landed the run itself as
`packages/orchestration/bench_run.py`, a NEW module joining the frozen order set
to a campaign, the campaign's evidence to bench rows, and the rows to a history
file — the entry point R11's Q6 found missing. It carries no fake and no clock:
the no-network deps are the test's, and `wall_s` stays clock-derived from the
runner. Its data root and history path are REQUIRED arguments, which closes Q6's
fourth blocker — history resolving through `data_paths.projects_dir` to the
operator's real root. It is the one name in the D9 allowlist.
--- END SLICE CTXSCOPE-R17-TO ---

--- BEGIN SLICE CTXIMPLICIT-R17 --- (in .agent/context.md, C6 — REWRITE pair)
R17. Adding to it is a deliberate act, not a repair.
--- END SLICE CTXIMPLICIT-R17 ---

--- BEGIN SLICE CTXIMPLICIT-R17-TO --- (C6)
R17, which spent it on `packages/orchestration/bench_run.py`. Adding to it is a
deliberate act, not a repair.
--- END SLICE CTXIMPLICIT-R17-TO ---

--- BEGIN SLICE CTXSTEPS-R17 --- (in .agent/context.md, C6 — REWRITE pair)
→ R16 record the R15 verdict, register R-0427 and R-0428 and pin the Q7
criterion → R17 the fake-provider run → R18 the integration gate → R19 closure.
--- END SLICE CTXSTEPS-R17 ---

--- BEGIN SLICE CTXSTEPS-R17-TO --- (C6)
→ R16 record the R15 verdict, register R-0427 and R-0428 and pin the Q7
criterion ✅ → R17 record the R16 verdict, register R-0429 and R-0430 and land
the fake-provider run → R18 the integration gate → R19 closure.
--- END SLICE CTXSTEPS-R17-TO ---

--- BEGIN SLICE R0427FIX --- (in packages/orchestration/bench_history.py, C5 — REWRITE pair, repairs R-0427)
ADDITIVE by construction (F082 inventory Q11): :class:`BenchRecord` and
:func:`projects_dir` are IMPORTED. No symbol moves out of a bench or gauntlet
module and none is edited.
--- END SLICE R0427FIX ---

--- BEGIN SLICE R0427FIX-TO --- (C5)
ADDITIVE by construction (F082 inventory Q11): :class:`BenchRecord` and
:func:`projects_dir` are IMPORTED. No symbol moves out of a GAUNTLET module and
no gauntlet module is edited. That is the invariant Q11 ruled on and the one
every round on this branch has enforced; it is NOT a promise that bench symbols
never change, because R15 added the `models` field to :class:`BenchRecord`
(R-0427).
--- END SLICE R0427FIX-TO ---

--- BEGIN SLICE ALLOWLIST --- (in tests/orchestration/test_bench_never_runs_implicitly.py, C4 — REWRITE pair)
EXPLICIT_BENCH_CALLERS: frozenset[str] = frozenset()
--- END SLICE ALLOWLIST ---

--- BEGIN SLICE ALLOWLIST-TO --- (C4)
EXPLICIT_BENCH_CALLERS: frozenset[str] = frozenset({
    # R17: the fake-provider bench run's entry point. It calls BOTH guarded
    # symbols on purpose — that is what an explicit caller is — and DECISION
    # F082 D9 predicted this exact one name before it existed.
    "packages/orchestration/bench_run.py",
})
--- END SLICE ALLOWLIST-TO ---

--- BEGIN SLICE FORTSCHRITT --- (the Fortschritt line; the handoff repeats it VERBATIM, R-0418)
Fortschritt: ~94 % (T001 ✅ · T002 ✅ · T003a ✅ · T003b ✅ · Q7-Kriterium gepinnt · Fake-Provider-Lauf gelandet · Integrationsgate + Closure offen) — Schätzung
--- END SLICE FORTSCHRITT ---

--- BEGIN SLICE PLAN --- (WHOLE-FILE replacement of .agent/plan.md, C6)
# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0431. Open findings: sixty — the thirty-two carried from F077, plus R-0403
to R-0430 registered on this branch. `.agent/live_review.md` is the source of
truth for that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R17 records the R16 gate, registers R-0429 and R-0430, and lands the
fake-provider bench run: a new `packages/orchestration/bench_run.py` joining the
frozen order set to a campaign, its evidence to rows, and the rows to a history
file, with both roots required rather than defaulted. It spends the D9
allowlist's one name and repairs R-0427.

## Next Steps
1. R18 the integration gate: the bench green on fixtures across two runs with
   history surviving, and a deliberately degraded run raising the regression
   warning — the Goal's three DONE conditions, measured together.
2. R19 closure: STATUS line, Built State, closure candidates, the PR.

## Risks
- The delivered order set is three, not the Design's five (R-0411). Closure may
  not quote five, and DECISION F082 D3 binds the recovery to a bench-owned
  fixture rather than an edit to the gauntlet's template.
- The freeze holds against a file-side edit only (R-0410). The Built State
  states that threat model rather than quoting the criterion whole.
- The builder's model stays unobservable: making it visible means reaching into
  `orchestrator_loop.py::execute_dispatched_job`. Closure states that absence
  rather than implying three roles were recorded.
- `wall_s` is clock-derived from `gauntlet_runner.py::run_order`, not a bench
  clock. Closure states that rather than implying the bench measures time.
- Reviewer defects remain the dominant finding class. Thirteen standing
  counter-measures now bind every block: R-0417 staleness, R-0418 Fortschritt,
  R-0419 grep-every-writer, R-0420 measure-the-block, R-0421 count-the-list,
  R-0422 composite-property, R-0423 measure-the-slice, R-0424
  count-your-own-contribution, R-0425 read-back-the-line-number, R-0427
  name-the-quantified-set, R-0428 re-derive-the-base-at-delegation, R-0429
  resolve-your-own-ordinals, R-0430 state-the-numeral-in-the-handoff.
--- END SLICE PLAN ---

────────────────── C2 — THE ENTRY POINT, BY CONTRACT ──────────────────
CREATE `packages/orchestration/bench_run.py`. NEW file. Read
`packages/orchestration/bench_dry_run.py` first and follow its module-docstring
and import style; this module is its sibling.

Module docstring: what the module is for (the on-demand bench run, R11 Q6's
missing entry point), that it holds NO clock and NO fake — `wall_s` is
clock-derived from `gauntlet_runner.py::run_order`, the no-network deps are the
caller's — and that both roots are required so no default reaches the
operator's real data root.

Define ONE public function. Name it `run_bench_campaign`. Keyword-only, and
these six parameters, with NO default on the first four:

    campaign_root: Path        — where the campaign writes its runs
    data_root: Path            — passed to run_campaign as real_data_root
    history_path: Path         — where the rows are appended
    series: str                — the history series label
    orders_dir: Path | None = None
    deps: RunnerDeps | None = None

It performs exactly four steps, in this order, and nothing else:
 1. `load_bench_order_set(orders_dir)` — the freeze runs FIRST, so a tampered
    set refuses before any run happens.
 2. `run_campaign(tuple(b.order for b in orders), campaign_root, deps=deps,
    real_data_root=data_root)` — `BenchOrder.order` IS a real `GauntletOrder`,
    so nothing is converted or copied.
 3. `dry_run_from_order_set(evidence_dir=campaign_root, series=series,
    orders_dir=orders_dir)` — the campaign root IS the evidence dir:
    `run_campaign` writes one `run.json` per run under it and
    `bench_dry_run._recorded_bodies` keys on the body's own `order_id`.
 4. `append_bench_run(rows, path=history_path)`.

Return a small frozen dataclass — name it `BenchRunResult` — carrying the
outcomes from step 2, the rows from step 3 and the `run_seq` from step 4, so a
caller need not re-read the disk. One WHY line above the function explains that
the freeze runs before the campaign. No `if TYPE_CHECKING` gymnastics, no
logging setup, no CLI entry, no `__main__` block. Keep it under 90 lines.

────────────────── C3 — THE FAKE-PROVIDER RUN, BY CONTRACT ──────────────────
CREATE `tests/orchestration/test_bench_run.py`. NEW file. FIRST read
`tests/orchestration/test_gauntlet_runner.py` lines 50-160 and reuse its
`Recorder`/`FakeMission`/`FakeExecution` SHAPE; author the doubles locally,
importing no private name from that module.

Build a `RunnerDeps` with ALL NINE seams doubled so the run touches no network,
no `git` and no project registry: `make_project`, `create_mission`,
`plan_mission`, `run_mission`, `load_mission`, `execute_fn`, `materialise`,
`plan_call_fn`, `move_call_fn`. Count them in the test's own docstring.

Use the REAL frozen bench order set — `default_bench_orders_dir()` — not a
fixture copy, so the run exercises the shipped freeze. Every path the run
touches is under `tmp_path`.

Pin exactly these six properties:

 1. THE RUN PRODUCES ONE ROW PER FROZEN ORDER, in the order set's own order.
    Assert the row ids equal the loaded order ids as a SEQUENCE, not a set.
 2. THE HISTORY FILE IS WRITTEN AND SURVIVES A SECOND RUN. Run twice into the
    same history path; assert `load_bench_history` reads back both runs and that
    the second `run_seq` is the first plus one.
 3. NO ROW IS AN `evidence_missing` ROW — assert against
    `bench_dry_run.EVIDENCE_MISSING_CLASS`. This separates an end-to-end run
    from a dry run over an empty directory: without it, properties 1 and 2 both
    pass over three missing rows.
 4. NOTHING IS WRITTEN OUTSIDE `tmp_path`. Pass a `data_root` under `tmp_path`;
    assert `campaign_root` and `history_path` are both relative to `tmp_path`
    after the run. Do NOT call `resolve_data_root()` in the test.
 5. THE SIGNATURE REFUSES A MISSING ROOT. `run_bench_campaign` called without
    `data_root`, and again without `history_path`, raises `TypeError` — R11
    Q6's blocker (4) pinned as a property rather than trusted to review.
 6. THE FREEZE RUNS BEFORE THE CAMPAIGN. Point `orders_dir` at a copied order
    set with one file's bytes changed and its version left alone; assert
    `BenchOrderSetError` is raised AND that `campaign_root` contains no run
    directory afterwards — the refusal happened before anything ran.

Reuse existing `tests/orchestration/` helpers; keep assertion messages actionable.

────────────────────────── DONE WHEN ──────────────────────────
Run every gate. Record its REAL output. "Green" as a word is a finding. BASE is
c044cb18 — re-derive it from HEAD before you start and say whether it still
equals this value (R-0428).

 1. `git status --porcelain` EMPTY at handback; `git worktree list` back to
    exactly the primary checkout. Report both verbatim.
 2. TRANSPORT AS A PROPERTY: python3 `read_bytes()` equality of
    `.agent/authored/f082-r17.md` and `.agent/last_block.md`, plus the shared
    sha256 and byte length. The reviewer measured this block at 399 lines before
    emission (R-0420). Report the REAL count and say whether it matches; a
    mismatch is the reviewer's defect to own, not yours to fix.
 3. `.agent/STOP` — report presence at round START and at handback.
 4. C1 APPEND PROOF over the COMMITTED `<C1>^` to `<C1>`: report whether `post`
    equals `pre + NL + GATE-R16 + NL + FINDINGS-R429-430` BYTE-WISE, using the
    join convention R15 and R16 proved — each extracted slice already carries
    its own trailing newline. State the exact expression you evaluated, and the
    C1 `--numstat`; its DELETION column must be 0.
 5. RECORD COUNTS in `.agent/live_review.md` at HEAD, LINE-ANCHORED only:
    `^Gate: R16 — PASS` 1 · `^- R-0429 — ` 1 · `^- R-0430 — ` 1 ·
    `^## DECISION F082 D9` 1 · `^Landed: ` 0 · `^Done: ` 0. Report each real
    number. No unanchored substring count is ordered this round (R-0424).
 6. OPEN SET RECOMPUTED MECHANICALLY: every `^- R-\d+ — ` paragraph minus every
    `^Done: R-\d+ — ` line. Report count, max id, next free id and any
    duplicate. R17 registers two, so expect SIXTY and next free R-0431 — report
    the real numbers regardless.
 7. C6 CONTEXT AS ONE COMPOSITE over the COMMITTED `<C6>^` to `<C6>` (R-0422:
    three pairs share `.agent/context.md`). Report `pre` with ALL THREE
    replacements applied `== post`; per pair report FROM 1x in `pre`, 0x in
    `post`, and `FROM in TO`. The reviewer measured all three FROMs at 1x
    against the disk before emission; report the real values. SAME COMMIT,
    SEPARATE PROPERTY: `.agent/plan.md` at HEAD BYTE-EQUALS the PLAN slice as a
    WHOLE FILE — report its sha256 and `wc -l`, which must be UNDER 50 (the
    reviewer measured the slice at 47 lines) and keep `## Goal` and
    `## Next Steps`. Report `wc -l` for `.agent/context.md` too.
 8. C4 AND C5 ARE ONE PAIR EACH, proven the same way on their own commits:
    report `pre.replace(FROM, TO) == post`, FROM 1x in `pre` and 0x in `post`,
    and each file's `--numstat`. Both FROMs were measured at 1x before emission.
 9. C2 AND C3 ARE NEW FILES. Report `git diff --name-only c044cb18..HEAD`
    restricted to `packages/` and to `tests/`: under `packages/` exactly
    `bench_run.py` and `bench_history.py`, under `tests/` exactly
    `test_bench_run.py` and `test_bench_never_runs_implicitly.py`. Report the
    `--numstat` DELETION column for each NEW file — both must be 0 — plus
    `^def test_` for the new test file and `wc -l` for `bench_run.py`.
10. `python3 -m pytest tests/orchestration/test_bench_run.py -q` → exit 0. New
    file, so no BASE exists: report the real number, predict nothing (R-0336).
11. THE PIN STILL PASSES WITH ITS ONE NEW NAME:
    `python3 -m pytest tests/orchestration/test_bench_never_runs_implicitly.py -q`
    → exit 0. Reviewer's BASE measurement `6 passed` with an EMPTY allowlist;
    C4 adds a name and no test. Report the real number, and the pin's observed
    per-tree file counts — the reviewer measured apps 73, packages 256,
    scripts 29 at BASE, and `packages/` gains exactly one file this round.
12. RED-PROOF, ISOLATED (G5), OF THE ALLOWLIST ITSELF. In a DISPOSABLE `git
    worktree` under `.remedy-wt/` — never the primary checkout — REMOVE the one
    name from `EXPLICIT_BENCH_CALLERS`, leaving `bench_run.py` in place, and run
    the pin there. Report the COLOUR: it MUST fail; name the test function and
    the first line of its assertion message, never a passed/failed COUNT
    (R-0327). Remove the worktree and show `git worktree list` back to one line.
    An allowlist whose entry deletes with nothing going red is not one.
13. STILL GREEN, run each set together: the gauntlet seven — reviewer's BASE
    measurement `276 passed` — and the pre-existing bench five — BASE
    `61 passed`. Report both real numbers and exit codes. C5 edits
    `bench_history.py`, covered by the bench five: a broken import surfaces here.
14. `python3 -m pytest tests/orchestration/test_bench_model_context.py -q` →
    exit 0. Reviewer's BASE measurement `14 passed`.
15. `python3 -m pytest tests/cli/test_golden_path.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_test_runner.py -q` → exit 0. Reviewer's BASE
    measurement: 184 passed.
16. `python3 -m ruff check packages/orchestration/bench_run.py
    packages/orchestration/bench_history.py
    tests/orchestration/test_bench_run.py
    tests/orchestration/test_bench_never_runs_implicitly.py` → exit 0. Scoped
    ruff over the pin file was `All checks passed!` at BASE, so red here is THIS
    round's doing. Repo-wide ruff is red on main, NOT gated (R-0364).
17. `python3 -m apps.cli.main integrity check --json` → `passed: true`,
    `fail_count: 0`, `check_count: 5`. Report the `handler_import` message: it
    must still be `handlers=337`, because this round adds NO CLI handler key.
18. NO GAUNTLET MODULE WAS EDITED. Report `git diff --name-only c044cb18..HEAD`
    restricted to `packages/orchestration/gauntlet_runner.py`,
    `gauntlet_orders.py`, `gauntlet_evidence.py`, `gauntlet_evaluator.py` and
    `gauntlet_matrix.py` — MUST be EMPTY. This measures Constraint 1.
19. CHANGE SET: `git diff --name-only c044cb18..HEAD` — report every path, COUNT
    them, and state whether you measured before or after C7. The Change list is
    a CEILING. The range restricted to `docs/` and `apps/` MUST be EMPTY.
20. `gh pr list --state open --json number,headRefName` → verbatim. Must be
    `[]`. Create NO pull request.
21. Report each commit's `git show --numstat <sha>` insertion total. If any
    exceeds 500, declare it with the inseparability reason BEFORE review.
22. STANDING STALENESS GATE (R-0417, ninth run). Re-read every sentence in the
    files this round touched that states a COUNT, a module list, a
    round-to-step map, or a completion claim, and report whether each still
    holds at HEAD. Repair ONLY what the ordered slices cover; report everything
    else and leave it. State how many sentences you checked. Re-check but do NOT
    repair: `.agent/context.md` still names 240 as the preferred block target.
    The R-0427 sentence IS repaired this round, by C5.
The docs-round gate does NOT bind; gate 19 proves `docs/**` is untouched.
BLOCK-SIZE DECLARATION (R-0420): 399 lines — under the 400 cap (DECISION F105
D5), over the 240 preference because two build contracts, four rewrite pairs and
a whole-file plan need the room. C0a's insertions stay inside the 500 limit.

Handback:    Completion report + rewrite `.agent/handoff.md` per
             docs/agents/handback_template.md: feature and round, branch,
             per-commit changed-files tables, the real verification values
             above, an item-status table with every C0a–C7 item and every gate
             1–22 exactly once, open-findings count, next expected action.
             Declare every deviation with its cause. Repeat the FORTSCHRITT
             slice VERBATIM (R-0418). If the handoff exceeds 60 lines, declare
             the stated-cause overage AND NAME ITS ACTUAL LINE COUNT AS A
             NUMERAL in that same line — never defer it to the completion
             report (R-0430). Push after every commit. Create NO PR. THE NEXT
             SESSION'S FIRST ACTION is self_drive_protocol.md Phase 1 rule 1 —
             re-read `.agent/STOP` from disk — BEFORE rule 2's Open PR Gate.
             F082 is MID-FEATURE and no PR exists. Next round: R18, the
             integration gate.
──────────────────────────────────────────────────────────────────────────────
