── STEP R19/21 — F082 Self-benchmark — the acceptance proof for R-0435 ──────

Goal:
  The bench's fixture run PASSES, and the suite asserts what the rows SAY.
  R-0435 records that R17's mission double left `job_links` empty, so
  `gauntlet_runner.py::latest_gate_result` found no verdict, `run_order` wrote
  no `dod_result.json`, `gauntlet_evaluator.py::_check_dod` reported
  `dod_blocking_green` RED, and every bench row carried `passed=False` while
  `tests/orchestration/test_bench_run.py` was green over all of them. This round
  makes the double store a real `GateResult` through the PRODUCT's own
  `dod_gate.py::save_gate_result`, inside the run's isolated root, adds the two
  properties measuring F082's first and third DONE conditions, and repairs
  R-0436's invented numeral. NO PRODUCTION CODE CHANGES — gate 12 measures that
  as a restriction.

Bundle, in commit order:
  C0a  save this block verbatim as `.agent/authored/f082-r19.md`
  C0b  mirror it byte-identically into `.agent/last_block.md`
  C1   `tests/orchestration/test_bench_run.py` — nine slices, R-0435's repair
  C2   `.agent/context.md` — CTXSTEPS-R19
  C3   `.agent/plan.md` — the PLAN slice, whole file, repairs R-0436
  C4   `.agent/live_review.md` — LR-LANDED, appended at EOF
  C5   rewrite `.agent/handoff.md`

BASE: 26dc94d2. Re-derive `git rev-parse HEAD` before the first commit and
report whether it equals 26dc94d2 (R-0428). If it does NOT, stop and hand off.

SLICE CONVENTION (R-0437: a shape asserted without its convention is a coin
flip the worker is left to resolve). Every FROM and TO body below is the lines
between its markers INCLUDING the trailing newline of its last line, and every
shape below is declared UNDER THAT CONVENTION. APPEND-SHAPED, TO contains FROM
verbatim: TBR-JOBLINK, TBR-TESTS. REWRITE, FROM and TO disjoint: the other
eight. Ten FROM/TO pairs, one whole-file replacement (PLAN), one EOF append
(LR-LANDED) — twelve named units, counted by listing them.

Constraints:
  1. Change set: `.agent/authored/f082-r19.md`, `.agent/last_block.md`,
     `.agent/context.md`, `.agent/plan.md`, `.agent/live_review.md`,
     `tests/orchestration/test_bench_run.py`, `.agent/handoff.md`. Nothing else.
     `packages/`, `apps/`, `scripts/`, `docs/` stay EMPTY in the range diff.
  2. The gauntlet's seven test files stay UNMODIFIED (context.md, Out).
  3. Do NOT edit `tests/orchestration/test_bench_never_runs_implicitly.py`. Its
     scan covers `apps/`, `packages/` and `scripts/` only — `tests/` is
     deliberately outside it — so this round cannot add a caller to that pin.
  4. Apply every slice BYTE-VERBATIM, including one you believe is wrong. A
     defect in my text is a declared deviation, never a silent repair.
  5. You write no `Done:` paragraph — `Landed:` only
     (planner_reviewer_prompt §4.4). `Done:` is reviewer-authored text.
  6. The red-proof at gate 8 runs ONLY inside a disposable `git worktree` under
     `.remedy-wt/`, removed and pruned before the handback (G5).

--- BEGIN SLICE TBR-DOC --- (in tests/orchestration/test_bench_run.py, C1 — REWRITE pair)
The doubles below follow the SHAPE of ``tests/orchestration/test_gauntlet_runner``'s
``Recorder``, authored locally rather than imported — a test module is not an
API, and sharing its privates would make either file unable to move.
"""
--- BEGIN SLICE TBR-DOC-TO --- (C1)
The doubles below follow the SHAPE of ``tests/orchestration/test_gauntlet_runner``'s
``Recorder``, authored locally rather than imported — a test module is not an
API, and sharing its privates would make either file unable to move.

The DoD VERDICT is part of the product path these doubles drive, not scenery.
``run_order`` writes ``dod_result.json`` only when ``latest_gate_result`` finds a
stored verdict on the mission's jobs, and the evaluator counts its absence as a
RED blocking criterion. Until R19 the mission double carried no ``job_links`` at
all, so every row this file produced was a FAILURE row and properties 1 to 3
passed over all of them (finding R-0435). The double now stores a real
``GateResult`` through ``dod_gate.py::save_gate_result``, inside the run's own
isolated root, and property 7 asserts what the rows SAY rather than that they
exist.
"""
--- END SLICE TBR-DOC-TO ---

--- BEGIN SLICE TBR-IMPORT --- (in tests/orchestration/test_bench_run.py, C1 — REWRITE pair)
from packages.orchestration.bench_history import load_bench_history
--- BEGIN SLICE TBR-IMPORT-TO --- (C1)
from packages.orchestration.bench_history import (
    REGRESSION_PASS_DROP,
    bench_regressions,
    load_bench_history,
)
--- END SLICE TBR-IMPORT-TO ---

--- BEGIN SLICE TBR-JOBLINK --- (in tests/orchestration/test_bench_run.py, C1 — APPEND-shaped pair; the TO adds ABOVE the FROM and contains the FROM verbatim)
@dataclass
class FakeMission:
    id: str = "m-1"
    job_links: tuple = ()
--- BEGIN SLICE TBR-JOBLINK-TO --- (C1)
@dataclass
class FakeJobLink:
    """The one attribute ``gauntlet_runner.latest_gate_result`` reads."""

    job_id: str


@dataclass
class FakeMission:
    id: str = "m-1"
    job_links: tuple = ()
--- END SLICE TBR-JOBLINK-TO ---

--- BEGIN SLICE TBR-FIELDS --- (in tests/orchestration/test_bench_run.py, C1 — REWRITE pair)
    roots_written: list[Path] = field(default_factory=list)

    def deps(self) -> RunnerDeps:
--- BEGIN SLICE TBR-FIELDS-TO --- (C1)
    roots_written: list[Path] = field(default_factory=list)
    #: Order ids whose DoD verdict is deliberately HELD, so their rows FAIL.
    #: Empty by default: a plain run degrades nothing.
    held_orders: frozenset[str] = frozenset()
    #: The order currently running, recorded by ``_make_project`` off the slug
    #: ``run_order`` hands it. A campaign runs its orders one at a time.
    order_id: str = ""

    def deps(self) -> RunnerDeps:
--- END SLICE TBR-FIELDS-TO ---

--- BEGIN SLICE TBR-DEPS --- (in tests/orchestration/test_bench_run.py, C1 — REWRITE pair)
            load_mission=lambda project_id, mission_id: FakeMission(id=mission_id),
--- BEGIN SLICE TBR-DEPS-TO --- (C1)
            load_mission=self._load_mission,
--- END SLICE TBR-DEPS-TO ---

--- BEGIN SLICE TBR-METHODS --- (in tests/orchestration/test_bench_run.py, C1 — REWRITE pair)
    def _make_project(self, name: str, slug: str, repo_path: Path | None = None) -> str:
        return "p-1"
--- BEGIN SLICE TBR-METHODS-TO --- (C1)
    def _make_project(self, name: str, slug: str, repo_path: Path | None = None) -> str:
        self.order_id = slug
        return "p-1"

    def _job_id(self) -> str:
        """One job id per order, so a HELD order holds only its own row."""
        return f"job-{self.order_id}"

    def _load_mission(self, project_id: str, mission_id: str) -> FakeMission:
        """The reloaded mission ``run_order`` reads its gate verdict off."""
        return FakeMission(id=mission_id,
                           job_links=(FakeJobLink(job_id=self._job_id()),))
--- END SLICE TBR-METHODS-TO ---

--- BEGIN SLICE TBR-GATE --- (in tests/orchestration/test_bench_run.py, C1 — REWRITE pair)
        (root / "missions" / "ledger.jsonl").write_text("{}\n", encoding="utf-8")
        return FakeResult()
--- BEGIN SLICE TBR-GATE-TO --- (C1)
        (root / "missions" / "ledger.jsonl").write_text("{}\n", encoding="utf-8")
        self._store_gate_verdict()
        return FakeResult()

    def _store_gate_verdict(self) -> None:
        """Write a real gate verdict through the PRODUCT's own writer.

        Called from inside ``run_order``'s isolated environment, so
        ``dod_gate.result_path`` resolves under the run's own root and nothing
        reaches the operator's. A HELD order gets ``released=False`` with a named
        blocking check, because a red gate is what a failing bench order IS;
        writing no verdict at all would instead reproduce R-0435.
        """
        from packages.orchestration.dod_gate import GateResult, save_gate_result

        held = self.order_id in self.held_orders
        save_gate_result(self._job_id(), GateResult(
            released=not held,
            blocking_red=("tests-green",) if held else (),
        ))
--- END SLICE TBR-GATE-TO ---

--- BEGIN SLICE TBR-HELPER --- (in tests/orchestration/test_bench_run.py, C1 — REWRITE pair)
         orders_dir: Path | None = None):
    return run_bench_campaign(
        campaign_root=tmp_path / campaign,
        data_root=data_root,
        history_path=tmp_path / "history" / "bench_history.jsonl",
        series=SERIES,
        orders_dir=orders_dir,
        deps=NoNetworkRun().deps(),
    )
--- BEGIN SLICE TBR-HELPER-TO --- (C1)
         orders_dir: Path | None = None, runner: NoNetworkRun | None = None):
    return run_bench_campaign(
        campaign_root=tmp_path / campaign,
        data_root=data_root,
        history_path=tmp_path / "history" / "bench_history.jsonl",
        series=SERIES,
        orders_dir=orders_dir,
        deps=(runner or NoNetworkRun()).deps(),
    )
--- END SLICE TBR-HELPER-TO ---

--- BEGIN SLICE TBR-TESTS --- (in tests/orchestration/test_bench_run.py, C1 — APPEND-shaped pair; the FROM is the file's current LAST line)
    assert not (tmp_path / "history" / "bench_history.jsonl").exists()
--- BEGIN SLICE TBR-TESTS-TO --- (C1)
    assert not (tmp_path / "history" / "bench_history.jsonl").exists()


# ---------------------------------------------------------------------------
# 7. EVERY ROW CARRIES A PASS — the Goal's "the bench runs green on fixtures"
# ---------------------------------------------------------------------------

def test_every_row_passes_on_a_clean_fixture_run(
        tmp_path: Path, data_root: Path) -> None:
    """What the rows SAY, not merely that they exist (finding R-0435).

    Properties 1 to 3 all passed over three ``passed=False`` rows: the run was
    joined, ordered and complete, and every order had FAILED on
    ``dod_blocking_green``. A bench whose fixture run is red measures nothing and
    cannot regress either — ``bench_regressions`` emits ``pass_drop`` only
    against a trailing pass rate above zero, so a bench that never passes never
    warns and property 8 below would be unreachable.
    """
    result = _run(tmp_path, data_root)
    not_passed = [(row.order_id, row.passed) for row in result.rows
                  if row.passed is not True]
    assert not not_passed, (
        f"Bench rows {not_passed} did not pass on a clean fixture run. F082's "
        "first DONE condition is that the bench runs GREEN on fixtures; a row "
        "that exists but failed satisfies properties 1-3 and not this one.")


# ---------------------------------------------------------------------------
# 8. A DEGRADED RUN WARNS — the Goal's "a degraded run triggers the warning"
# ---------------------------------------------------------------------------

def test_a_deliberately_degraded_run_triggers_the_pass_drop_warning(
        tmp_path: Path, data_root: Path) -> None:
    """The degradation is a HELD DoD verdict — what a real failure actually is.

    No history row is edited and no warning is constructed here: the second
    campaign really runs, the gate really refuses to release ONE order, and the
    warning is read back off the file both runs appended to.

    Only ``pass_drop`` is asserted. ``wall_s`` is clock-derived from
    ``gauntlet_runner.run_order``, so a second fixture run that happens to take
    over 1.5x the first legitimately adds a ``wall_regression`` — asserting the
    whole warning tuple would pin this property to a stopwatch.
    """
    held = load_bench_order_set()[0].id
    _run(tmp_path, data_root, campaign="campaign-green")
    degraded = _run(tmp_path, data_root, campaign="campaign-degraded",
                    runner=NoNetworkRun(held_orders=frozenset({held})))

    verdicts = {row.order_id: row.passed for row in degraded.rows}
    assert verdicts.get(held) is False, (
        f"The held order {held} reported {verdicts.get(held)}; the degradation "
        "never reached the row, so the warning below would prove nothing")
    still_green = [order_id for order_id, passed in verdicts.items()
                   if order_id != held and passed is not True]
    assert not still_green, (
        f"Orders {still_green} also stopped passing — the degradation was not "
        f"confined to {held}, so a warning about it is not attributable")

    entries = load_bench_history(tmp_path / "history" / "bench_history.jsonl")
    drops = [(w.kind, w.order_id) for w in bench_regressions(entries, series=SERIES)
             if w.kind == REGRESSION_PASS_DROP]
    assert drops == [(REGRESSION_PASS_DROP, held)], (
        f"Expected exactly one {REGRESSION_PASS_DROP} warning, for {held}, and "
        f"got {drops}. F082's third DONE condition is that a deliberately "
        "degraded fixture run triggers the regression warning.")
--- END SLICE TBR-TESTS-TO ---

--- BEGIN SLICE CTXSTEPS-R19 --- (in .agent/context.md, C2 — REWRITE pair)
R-0431 to R-0434 → R19 the acceptance proof for R-0435 → R20 the integration
--- BEGIN SLICE CTXSTEPS-R19-TO --- (C2)
R-0431 to R-0434 ✅ → R19 the acceptance proof for R-0435 → R20 the integration
--- END SLICE CTXSTEPS-R19-TO ---

--- BEGIN SLICE PLAN --- (WHOLE FILE replacement of .agent/plan.md, C3)
# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0438. Open findings: sixty-seven — the thirty-two carried from F077, plus
R-0403 to R-0437 registered on this branch. `.agent/live_review.md` is the
source of truth for that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R19 repairs R-0435: the mission double stores a real `GateResult` through
`dod_gate.py::save_gate_result` inside the run's isolated root, so a bench row
can PASS, and two new properties assert what the rows SAY — every row passes on
a clean fixture run, and a run with one order's verdict HELD produces exactly
one `pass_drop` warning. It also repairs R-0436's numeral here. It changes no
production code.

## Next Steps
1. R20 the integration gate, per docs/agents/integration_gate.md.
2. R21 closure: STATUS line, Built State, closure candidates, the PR.

## Risks
- Until R19 is GATED, no round may claim the bench runs green on fixtures: the
  claim is what R-0435 is about, and a worker's green is not a verdict.
- The delivered order set is three, not the Design's five (R-0411), the freeze
  holds against a file-side edit only (R-0410), and the builder's model stays
  unobservable — closure states all three absences rather than implying five
  orders and three recorded roles.
- `wall_s` is clock-derived from `gauntlet_runner.py::run_order` and every row's
  `cost` is `None` under doubles, so pass rate is the only trend a real run can
  prove; cost and wall warnings stay golden-pinned.
- Reviewer defects remain the dominant finding class: the standing
  counter-measures binding every block are R-0417 through R-0437, stated as a
  range and deliberately WITHOUT a count (R-0436).
--- END SLICE PLAN ---

--- BEGIN SLICE LR-LANDED --- (APPEND to .agent/live_review.md, C4, with exactly one blank line between the file's current last line and the first line of this slice)
Landed: R-0435 — the mission double stores a real `GateResult` through `dod_gate.py::save_gate_result` inside the run's isolated root, so `latest_gate_result` finds a verdict and `run_order` writes `dod_result.json`; every bench row now reports `passed=True` on a clean fixture run, and two new properties (`test_every_row_passes_on_a_clean_fixture_run`, `test_a_deliberately_degraded_run_triggers_the_pass_drop_warning`) assert what the rows SAY. No production code changed.
Landed: R-0436 — `.agent/plan.md`'s counter-measure risk now states the range R-0417 through R-0437 alone, with no numeral, which is the form R-0436's standing rule prescribes.
--- END SLICE LR-LANDED ---

Done when — run every gate and record its REAL value; a gate you cannot run is
reported as not run, never as green:

 1. `git status --porcelain` EMPTY before the first commit and after the last.
    `git worktree list` ONE line at the handback. `.agent/STOP` ABSENT at round
    start and again at handback (R-0347).
 2. TRANSPORT: `Path.read_bytes()` equality of `.agent/authored/f082-r19.md`
    and `.agent/last_block.md`; report sha256, byte count and real `wc -l` of
    both. The block DECLARES its own line count in the footer below — report
    whether the measured count equals it (R-0420).
 3. BASE: `git rev-parse HEAD` before the first commit; report it and whether
    it equals 26dc94d2.
 4. C1 PAIRS. For each of the EIGHT rewrite pairs — TBR-DOC, TBR-IMPORT,
    TBR-FIELDS, TBR-DEPS, TBR-METHODS, TBR-GATE, TBR-HELPER, CTXSTEPS-R19 —
    report over that commit's `pre` and `post`: FROM count in `pre`, FROM count
    in `post`, TO count in `post`, and `FROM in TO`. For the TWO append-shaped
    pairs — TBR-JOBLINK, TBR-TESTS — report FROM count in `pre`, FROM count in
    `post`, `FROM in TO`, and the per-line count of each TO-ONLY line among the
    lines that commit's diff ADDS (§4.9). Then the COMPOSITE for each file:
    `pre` with all of that file's replacements applied equals `post`, byte-wise.
 5. `python3 -m pytest tests/orchestration/test_bench_run.py -q` — report the
    count and exit code. Report also the `-v` names of the two new tests.
 6. THE VALUE, not just the colour. In a disposable worktree at HEAD, run a
    probe that calls the module's own `_run` helper and PRINTS
    `[(row.order_id, row.passed) for row in result.rows]`. Report that list
    verbatim, and report the probe's `test_bench_run.__file__` so the import
    path is proven to be the worktree's and not the primary checkout's
    (R-0337). At BASE the same probe prints three `False` values; report what
    it prints at HEAD.
 7. `python3 -m pytest tests/orchestration/test_bench_never_runs_implicitly.py
    -q` — report count and exit code; the file is NOT edited this round, so
    report it as ABSENT from the change set at gate 12.
 8. RED-PROOF, disposable worktree only. Delete the single line
    `        self._store_gate_verdict()` from the worktree copy of
    `tests/orchestration/test_bench_run.py`, then run that file. The run must
    be RED. Report the exit code and the NAMES of every test that fails — do
    not report a predicted count, report what failed. Then remove and prune the
    worktree and re-report `git worktree list`.
 9. `python3 -m ruff check tests/orchestration/test_bench_run.py` — run it at
    BASE before any commit AND at HEAD; report both (R-0364).
10. CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q`, plus the
    `.agent`-state contract readers `tests/dashboard`, `tests/test_test_runner.py`
    and `tests/regression/test_resource_safety.py` — report counts and exit
    codes.
11. `python3 -m apps.cli.main integrity check --json` — report `passed`,
    `fail_count`, `check_count`.
12. CHANGE SET, measured BEFORE C5: `git diff --name-only 26dc94d2..HEAD`.
    Report the full list and its count. Restricted to `packages/`, `apps/`,
    `scripts/` and `docs/` it must be EMPTY — that is this round's additive
    claim, measured as a restriction. Restricted to the gauntlet's seven test
    files it must also be EMPTY.
13. Insertions (`+` column only) per commit — report each; none over 500.
14. OPEN SET recomputed mechanically from `.agent/live_review.md` at HEAD:
    count `^- R-\d+ — ` paragraphs, count `^Done: R-\d+ — ` lines, report both
    and their difference, the max id and the next free id. `^Done: ` must be 0.
    Report the count of `^Landed: ` lines.
15. `.agent/plan.md` byte-equals the PLAN slice as a WHOLE FILE; report sha256
    and `wc -l` (must be under 50), and that `## Goal` and `## Next Steps` are
    both present.
16. STALENESS GATE, standing since R-0417. READ — do not grep — every
    claim-bearing sentence in `test_bench_run.py`, `.agent/context.md`,
    `.agent/plan.md` and `packages/orchestration/bench_run.py`. Report the
    number READ, the number that HOLD at HEAD, and name separately those that
    do NOT hold and those this round's gates never measured (R18 conflated the
    two). Repair nothing outside Constraint 1; report it for R20.
17. `gh pr list --state open --json number,headRefName` — report it. Create NO
    PR: F082's PR is created at closure (R21), not before.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
feature and round, branch, per-commit changed-files tables, the seventeen gate
values above, the item-status table covering every C-item and every gate, open
findings count with max and next free id, and the next expected action. Repeat
this line verbatim as the Fortschritt line:

Fortschritt: ~96 % (T001 ✅ · T002 ✅ · T003a ✅ · T003b ✅ · Q7-Kriterium gepinnt · Fake-Provider-Lauf gelandet · R-0435 repariert, DONE-Bedingungen 1 und 3 erstmals gemessen · Integrationsgate + Closure offen) — Schätzung

If any gate is RED, or anything in this block contradicts what you find on
disk: finish the commit you are in, write the handoff naming the exact blocker,
and end. Do not widen scope to route around it (G8).

BLOCK SIZE, measured on these final bytes: 398 lines (cap 400, DECISION F105 D5).
──────────────────────────────────────────────────────────────────────────────
