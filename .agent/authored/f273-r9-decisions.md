
## DECISION F273 D9 (2026-09-19, reviewer, round 9) — the bench gets its two missing orders on its own fixture and its evidence names the world it ran in; F273 wires the four list commands and F267 keeps its tests
CONTEXT: T010's R-0411 and T007's R-0796 each needed a ruling taken in the round that lands the
patch (amend0917-throughput rule 3). Measured by research helpers and re-measured by the reviewer's
dry run at `db9a05cc`: the frozen bench set loads three orders; `run_order` in
`packages/orchestration/gauntlet_runner.py` records `template_digest` of the gauntlet's default
template whatever `materialise` copied, so a run on any other fixture would name the wrong world;
of the nine list commands R-0796 kept in scope, F275 deleted five and `test.list`, `mission.list`,
`change.list` and `event.list` survive unwired; and `T2_F267.md` names R-0796 "owned here" while
the 2026-09-06 triage routed it to this feature's T007.
CHOSEN: (1) R-0411, per DECISION F082 D3. `scripts/bench_sample_project/` is a stdlib-only fixture
(a WSGI item service and a static widget); an order file may name it with `bench_template`, absent
meaning the gauntlet's; the bench manifest freezes the fixture by `bench_template_digest`; and two
orders against it, `b04-api-create-endpoint` and `b05-widget-count-badge`, each state a premise a
test checks by behaviour. `BENCH_ORDER_SET_VERSION` goes to 2, which resets nothing because no count
or series is keyed on it. (2) THE GAUNTLET EDIT, a reviewer ruling beyond DECISION F082 D1, which
covers only R-0407. `RunnerDeps` gains `template_dir_fn`, default `None`, and `_evidence_body`
digests the template it names; a gauntlet run passes `None` throughout, so its evidence bytes, the
gauntlet manifest, its template digest and `GAUNTLET_ORDER_SET_VERSION` are unchanged. The bench
hands one template choice to both the copy and the digest, read off the `run-NN-<order id>` name
`run_order` gives each run directory, and fails closed when no single order matches. (3) b05's
script is judged at the HTTP level only, as F082's Design's "no browser dependency" requires. (4)
R-0796 AND F267. F273 lands F267's T001 — the four wirings, each with tests for an unknown sort
field, the limit and the time window — and resolves R-0796, because the later routing and a built,
red-proved patch both point here; F267 stays registered with T002 and T003, and its file says so
in the same commit. `event.list` now returns the newest events first like every wired list, and
`change.list` dates a change by its patch intent's `created_at`, so a change whose intent carries no
date sorts last and drops out of a time window, as `patch list` already does. (5) R-0762 stays in
T007 and is the next round's.
ALTERNATIVES: editing the gauntlet's sample project, rejected by DECISION F082 D3; a bench run that
records the gauntlet's digest as a known absence, rejected because evidence that names the wrong
world is the defect R-0189 exists to prevent; leaving R-0796 to F267, rejected because the patch
is built and the triage routed it here; a date field added to every patch-intent writer, rejected
as outside both findings.
REVERSE: restore `packages/orchestration/bench_orders.py`, `bench_run.py`, `gauntlet_runner.py`,
`pyproject.toml`, `scripts/bench_orders/`, `docs/roadmap/features/T2_F082.md`,
`docs/roadmap/features/T2_F267.md`, the four command modules and `apps/cli/command_catalog.py` from
`db9a05cc`, delete `scripts/bench_sample_project/`, drop the tests this round added or changed,
and delete this paragraph.
