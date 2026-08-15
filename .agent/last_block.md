── STEP R18/21 — F082 Self-benchmark ─────────────────────────────────────────
BASE:        b2ccafea. RE-DERIVE it: run `git rev-parse HEAD` before your first
             commit and report the value. If it is not b2ccafea, STOP and report
             — do not adapt (R-0428).

Goal:        Put the round's two new findings on disk, re-plan the remaining map
             as DECISION F082 D10, and repair four prose-and-typing defects:
             R-0431's self-contradicting context bullet, the four stale pin
             sentences of R-0432 and R-0434, and R-0433's `Any` annotations. This
             round lands NO capability and writes no test — R-0435, the missing
             acceptance proof it registers, is R19's deliverable and stays OPEN.

Bundle:      C0a save this block · C0b mirror it · C1 FINDINGS-R434-435 +
             DECISION-D10 appended to the review record · C2 the R-0433 type
             repair · C3 the R-0432 + R-0434 pin-prose repair, four pairs · C4
             the R-0431 context-bullet repair · C5 four LANDED lines · C6 plan
             and context re-sync · C7 handback.

Change:      This list is a CEILING. Nothing outside it.
             - .agent/authored/f082-r18.md                          (C0a, new)
             - .agent/last_block.md                                 (C0b)
             - .agent/live_review.md                                (C1, C5 appends)
             - packages/orchestration/bench_run.py                  (C2, two pairs)
             - tests/orchestration/test_bench_never_runs_implicitly.py (C3, four pairs)
             - .agent/context.md                                    (C4 one pair, C6 two pairs)
             - .agent/plan.md                                       (C6 whole-file)
             - .agent/handoff.md                                    (C7)
             NOT in scope: `docs/**`, `apps/**`, `scripts/**`, every gauntlet
             module, every other product module, and EVERY test file except the
             pin at C3. `tests/orchestration/test_bench_run.py` is RUN but NOT
             EDITED this round — editing it is R19's job (gate 15).

Constraints:
 1. THE FACTORING STAYS ADDITIVE and no gauntlet module is edited — the R2 Q11
    rule; DECISION F082 D1's exception does not widen. C2 ADDS two imports to
    `bench_run.py`: importing a type for a signature is NOT a call, which is the
    R-0433 correction itself. The verbs `bench_run.py` CALLS stay four, counted —
    `load_bench_order_set`, `run_campaign`, `dry_run_from_order_set`,
    `append_bench_run` — and C2 adds none.
 2. C2 CHANGES NO BEHAVIOUR: no new argument, no new branch. Because
    `bench_run.py` carries `from __future__ import annotations`, its annotations
    are STRINGS never evaluated at import, so a wrong type import would NOT
    surface as an ImportError — gate 10 therefore RESOLVES them.
 3. THE PIN FILE'S PROSE ONLY. C3 changes four comment/docstring regions and no
    executable line: `EXPLICIT_BENCH_CALLERS` keeps its one name, the floors in
    `MIN_SCANNED_FILES` are untouched, and its comment "measured at R16 …
    packages 256" is DELIBERATELY LEFT — time-stamped to R16, therefore true as
    history (R-0432 ruled on it explicitly).
 4. NO RED-PROOF IS ORDERED, deliberately, and the handback says so. Every change
    here is a comment, a docstring, an annotation or an `.agent` state file, so
    no behavioural branch exists for a mutation to turn red, and an ordered
    mutation whose green outcome is the honest one costs the round a declared
    deviation (R-0252, DECISION F105 D10). R19 carries two red-proofs.
 5. Apply every pair slice DISK-TO-DISK out of the COMMITTED
    `.agent/authored/f082-r18.md`. No `--- BEGIN SLICE` / `--- END SLICE` marker
    line may reach any target, and no target gains a trailing-whitespace line.
 6. Apply every slice VERBATIM. A slice that is wrong on arrival is applied as
    ordered and DECLARED, never silently repaired: three of R17's findings
    arrived that way, and R-0434 below is the reviewer catching its own miscount.
 7. R-0435 IS NOT REPAIRED HERE and MUST NOT be marked `Landed:`. It is
    registered at C1 and stays in the open set at handback. A round that
    registered a finding and marked it resolved without a test would be the
    exact overclaim the finding is about.
 8. Every commit follows the AGENTS.md self-review loop and the Commit Gate.
    Insertions per commit stay under 500. No commit trailer. DECISION F082 D1–D9
    and every prior gate entry are history and ARE NOT REWRITTEN.

────────────────────────── AUTHORED SLICES ──────────────────────────

--- BEGIN SLICE FINDINGS-R434-435 --- (append to .agent/live_review.md, C1, one blank line between the file's current last line and the first line of this slice)
- R-0434 — Low, MY OWN ENUMERATION WAS SHORT BY ONE, found by the reviewer while authoring R18 against the file R-0432 describes. R-0432 says the pin file "now carries three sentences that were true when R16 wrote them and are false at HEAD" and names three: the module docstring's "which is empty today and gains exactly one name at R17", the allowlist constant's "EMPTY today, which is a measured fact and not an assumption", and the section header "callers equal the allowlist, which is empty today". There are FOUR. The fourth is the allowlist constant's other comment, "R17 adds EXACTLY ONE name, the fake-provider run's entry point", which is future tense over a name already sitting two lines below it. Low, because it is the same prose class R-0432 already registered and R18 repairs all four in one commit. It is registered separately because the CAUSE is a different mistake: R-0432's list was derived by matching one PHRASE, "empty today", and the fourth sentence is stale without containing that phrase. That is R-0402 and R-0404's class in its other form — those two counted their own list wrongly, this one counted correctly and claimed coverage the count never had. Standing rule from here, binding the reviewer: an enumeration of stale claims in a file either STATES the query it was derived from, so a later reader knows what it cannot have found, or it is derived by reading every claim-bearing sentence in the file. A grep for the symptom is not a read of the claim.

- R-0435 — Medium, THE ROUND'S OWN SUITE WAS GREEN OVER THREE FAILURE ROWS, so F082's FIRST DONE CONDITION WAS NEVER MEASURED. Found by the reviewer while authoring R18, by running R17's own `_run` helper in a scratch probe and printing what the rows SAY rather than that they exist. `tests/orchestration/test_bench_run.py` passes 7/7 at HEAD, and every bench row it produces carries `passed=False`. Exactly ONE pass criterion fails, and the evaluator names it itself: `dod_blocking_green`, detail "no dod_result.json: the DoD gate never produced a verdict". The chain is mechanical — the `load_mission` double returns a `FakeMission` whose `job_links` is empty, so `gauntlet_runner.py::latest_gate_result` finds no stored verdict, so `::run_order` writes no `dod_result.json`, so `gauntlet_evaluator.py::_check_dod` reports a red blocking criterion, so `capability_bench.py::_passed_of` reads `flawless=False`. The R17 block's property 3 asked only that no row carry `bench_dry_run.EVIDENCE_MISSING_CLASS`, which is strictly weaker: a row can be present, correctly joined, and FAILED. Two consequences reach closure. F082's Goal condition "the bench runs green on fixtures" was not measured by the round that landed the run; and the third condition, "a deliberately degraded fixture run triggers the regression warning", is UNREACHABLE from a real run while nothing ever passes, because `bench_history.py::bench_regressions` emits `pass_drop` only when the trailing pass rate is above zero — a bench that always fails cannot regress. Medium, not Low, because a DONE condition went unmeasured one round before closure; not High, because no shipped behaviour is wrong: the product path is correct end to end and only the test's double is incomplete, and the repair changes no production logic. The CAUSE is mine and precise: the contract I authored for R17's C3 enumerated six properties about SHAPE — row order, row count, absence of missing rows, path containment, required arguments, freeze ordering — and not one about the VERDICT the rows carry. This is R-0220's class at its own root, and the aggravating detail is that the same round probed the pin in three directions past its ordered gates and still never asked the run what its output said. Standing rule from here, binding the reviewer: a contract for a test that drives a product path to a RECORD asserts what the record SAYS, not merely that a record exists. For a bench row that is `passed`; for any evaluated artifact it is the verdict field, named explicitly in the contract. R19 repairs this and is the round that measures the Goal's three DONE conditions together.
--- END SLICE FINDINGS-R434-435 ---

--- BEGIN SLICE DECISION-D10 --- (append to .agent/live_review.md, C1, after FINDINGS-R434-435, one blank line between the two slices)
## DECISION F082 D10 — the acceptance proof gets its own round, ahead of the integration gate

Chosen 2026-08-15 by the reviewer under docs/agents/planner_reviewer_prompt.md
§4 item 7, which routes a wrong plan into the current block as a loud, persisted,
reversible decision rather than a question. `.agent/plan.md` and
`.agent/context.md` both said R18 is the integration gate and R19 the closure.
R-0435 makes that map unsafe, and the reason is ordering rather than taste: the
gate's whole job is to run the full suite over the code that CLOSES the feature,
and that code does not exist yet, because the Goal's first DONE condition is
unmeasured and its third is unreachable from a real run.

Chosen instead, a four-round tail: R18 records the findings and repairs the four
prose-and-typing defects; R19 lands the acceptance proof — the DoD verdict the
doubles never stored, plus the properties that read what the rows SAY; R20 is the
integration gate; R21 is closure. The denominator moves from 19 to 21 in
`.agent/plan.md`, `.agent/context.md` and every later block header.

Three alternatives were rejected. Bundling the proof into the gate round was
rejected because a commit landing after the branch run invalidates the gate's own
evidence: `branch_failed.txt` is a claim about a tree, and a later commit makes it
a claim about a tree that no longer exists. Running the gate first and adding the
proof at closure was rejected for the reason R11's Q7 established and D9 applied
once — moving a blocker closer to the closure it blocks is not a plan, and it
would put the proof AFTER the only run permitted to say "full suite green".
Bundling the proof WITH these four repairs was rejected mechanically rather than
by preference: the block ordering both measured 482 lines against the 400-line
ceiling of DECISION F105 D5, and a block the worker must save verbatim cannot be
trimmed downstream.

How to reverse: delete this decision, fold R19's proof into the closure round and
restore the R18-gate/R19-closure map. Nothing else depends on it.
--- END SLICE DECISION-D10 ---

--- BEGIN SLICE BR-IMPORTS --- (in packages/orchestration/bench_run.py, C2 — REWRITE pair)
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from packages.orchestration.bench_dry_run import dry_run_from_order_set
from packages.orchestration.bench_history import append_bench_run
from packages.orchestration.bench_orders import load_bench_order_set
from packages.orchestration.gauntlet_runner import RunnerDeps, run_campaign
--- BEGIN SLICE BR-IMPORTS-TO --- (C2)
from dataclasses import dataclass
from pathlib import Path

from packages.orchestration.bench_dry_run import dry_run_from_order_set
from packages.orchestration.bench_history import append_bench_run
from packages.orchestration.bench_orders import load_bench_order_set
from packages.orchestration.capability_bench import BenchRecord
from packages.orchestration.gauntlet_runner import OrderOutcome, RunnerDeps, run_campaign
--- END SLICE BR-IMPORTS-TO ---

--- BEGIN SLICE BR-FIELDS --- (in packages/orchestration/bench_run.py, C2 — REWRITE pair)
    #: One outcome per order, exactly as ``run_campaign`` returned them; each is
    #: a ``gauntlet_runner.OrderOutcome``.
    outcomes: tuple[Any, ...]
    #: One bench row per frozen order, in the order set's own order; each is a
    #: ``capability_bench.BenchRecord``.
    rows: tuple[Any, ...]
--- BEGIN SLICE BR-FIELDS-TO --- (C2)
    #: One outcome per order, exactly as ``run_campaign`` returned them.
    outcomes: tuple[OrderOutcome, ...]
    #: One bench row per frozen order, in the order set's own order.
    rows: tuple[BenchRecord, ...]
--- END SLICE BR-FIELDS-TO ---

--- BEGIN SLICE PIN-DOC --- (in tests/orchestration/test_bench_never_runs_implicitly.py, C3 — REWRITE pair)
entry point EQUALS :data:`EXPLICIT_BENCH_CALLERS`, which is empty today and gains
exactly one name at R17. "Never implicitly" was never a claim that nothing calls
the bench; it is a claim that nothing calls it as a SIDE EFFECT, and an
enumerated caller is the opposite of an implicit one.
--- BEGIN SLICE PIN-DOC-TO --- (C3)
entry point EQUALS :data:`EXPLICIT_BENCH_CALLERS`, which R17 spent on exactly one
name — the bench run's own entry point. "Never implicitly" was never a claim that
nothing calls the bench; it is a claim that nothing calls it as a SIDE EFFECT,
and an enumerated caller is the opposite of an implicit one.
--- END SLICE PIN-DOC-TO ---

--- BEGIN SLICE PIN-CONST --- (in tests/orchestration/test_bench_never_runs_implicitly.py, C3 — REWRITE pair)
#: THE ALLOWLIST — repo-relative module paths permitted to call a guarded entry
#: point. EMPTY today, which is a measured fact and not an assumption.
--- BEGIN SLICE PIN-CONST-TO --- (C3)
#: THE ALLOWLIST — repo-relative module paths permitted to call a guarded entry
#: point. ONE name today, R17's, which is a measured fact and not an assumption.
--- END SLICE PIN-CONST-TO ---

--- BEGIN SLICE PIN-ADDS --- (in tests/orchestration/test_bench_never_runs_implicitly.py, C3 — REWRITE pair, repairs R-0434)
#: R17 adds EXACTLY ONE name, the fake-provider run's entry point. Adding to this
#: set is a DELIBERATE ACT that says the bench gained an explicit caller, never a
#: repair to make a red test green. A name appearing here without a round that
#: meant to put it here is the failure this pin exists to surface.
--- BEGIN SLICE PIN-ADDS-TO --- (C3)
#: R17 ADDED that one name, the bench run's entry point. Adding to this set is a
#: DELIBERATE ACT that says the bench gained an explicit caller, never a repair
#: to make a red test green. A name appearing here without a round that meant to
#: put it here is the failure this pin exists to surface.
--- END SLICE PIN-ADDS-TO ---

--- BEGIN SLICE PIN-HEADER --- (in tests/orchestration/test_bench_never_runs_implicitly.py, C3 — REWRITE pair, ONE physical line)
# 3. THE CRITERION — callers equal the allowlist, which is empty today
--- BEGIN SLICE PIN-HEADER-TO --- (C3, ONE physical line)
# 3. THE CRITERION — callers equal the allowlist, exactly
--- END SLICE PIN-HEADER-TO ---

--- BEGIN SLICE CTXIMPLICIT-R18 --- (in .agent/context.md, C4 — REWRITE pair, repairs R-0431; the FROM's LAST line is deliberately unindented, which is the defect being repaired)
- The bench never runs implicitly — on demand only, an F082 acceptance rule,
  pinned at R16 by `tests/orchestration/test_bench_never_runs_implicitly.py` as
  an allowlist of modules permitted to call the bench's write entry points
  (DECISION F082 D9). The allowlist is EMPTY today and gains exactly one name at
  R17, which spent it on `packages/orchestration/bench_run.py`. Adding to it is a
deliberate act, not a repair.
--- BEGIN SLICE CTXIMPLICIT-R18-TO --- (C4)
- The bench never runs implicitly — on demand only, an F082 acceptance rule,
  pinned at R16 by `tests/orchestration/test_bench_never_runs_implicitly.py` as
  an allowlist of modules permitted to call the bench's write entry points
  (DECISION F082 D9). The allowlist holds EXACTLY ONE name, R17's
  `packages/orchestration/bench_run.py`. Adding to it is a deliberate act, not a
  repair.
--- END SLICE CTXIMPLICIT-R18-TO ---

--- BEGIN SLICE LANDED-R18 --- (append to .agent/live_review.md, C5, one blank line before the first line; replace each <sha of Cn> with the REAL short SHA of that commit, so this slice is applied AFTER C4. FOUR lines: R-0435 is NOT among them, per Constraint 7)
Landed: R-0431 — the context bullet was rewritten whole, so the "EMPTY today" head no longer contradicts the "spent it on bench_run.py" tail, and the dedented continuation line is back inside its bullet, in <sha of C4>.
Landed: R-0432 — three of the pin file's stale prose regions repaired, in <sha of C3>.
Landed: R-0433 — `BenchRunResult.outcomes` and `.rows` carry their concrete types `OrderOutcome` and `BenchRecord`, and `typing.Any` is gone from the module, in <sha of C2>.
Landed: R-0434 — the fourth stale pin sentence, the allowlist constant's "R17 adds EXACTLY ONE name", repaired in the same commit as the other three, <sha of C3>.
--- END SLICE LANDED-R18 ---

--- BEGIN SLICE CTXSCOPE-R18 --- (in .agent/context.md, C6 — APPEND-SHAPED pair: the TO CONTAINS the FROM verbatim and adds sentences after it, so gate 8 proves it as an append, never as FROM 0x)
operator's real root. It is the one name in the D9 allowlist.
--- BEGIN SLICE CTXSCOPE-R18-TO --- (C6)
operator's real root. It is the one name in the D9 allowlist. R18 registered
R-0434 and R-0435 and repaired four prose-and-typing defects, landing no
capability: R-0435 records that R17's doubles left `job_links` empty, so no
`dod_result.json` was ever written, every row the run produced was a FAILURE row,
and the suite was green over it. R19 owns that repair — a stored `GateResult`
through `dod_gate.py::save_gate_result` inside the isolated root, plus the
properties that assert what the rows SAY — and is the round that measures the
Goal's three DONE conditions together (DECISION F082 D10).
--- END SLICE CTXSCOPE-R18-TO ---

--- BEGIN SLICE CTXSTEPS-R18 --- (in .agent/context.md, C6 — REWRITE pair)
criterion ✅ → R17 record the R16 verdict, register R-0429 and R-0430 and land
the fake-provider run → R18 the integration gate → R19 closure.
--- BEGIN SLICE CTXSTEPS-R18-TO --- (C6)
criterion ✅ → R17 record the R16 verdict, register R-0429 and R-0430 and land
the fake-provider run ✅ → R18 register R-0434 and R-0435, rule at D10 and repair
R-0431 to R-0434 → R19 the acceptance proof for R-0435 → R20 the integration
gate → R21 closure, per DECISION F082 D10.
--- END SLICE CTXSTEPS-R18-TO ---

--- BEGIN SLICE FORTSCHRITT --- (the Fortschritt line; the handoff repeats it VERBATIM, R-0418)
Fortschritt: ~94 % (T001 ✅ · T002 ✅ · T003a ✅ · T003b ✅ · Q7-Kriterium gepinnt · Fake-Provider-Lauf gelandet · DONE-Bedingungen noch UNBEWIESEN, R-0435 offen · Akzeptanzbeweis + Integrationsgate + Closure offen) — Schätzung
--- END SLICE FORTSCHRITT ---

--- BEGIN SLICE PLAN --- (WHOLE-FILE replacement of .agent/plan.md, C6)
# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0436. Open findings: sixty-five — the thirty-two carried from F077, plus
R-0403 to R-0435 registered on this branch. `.agent/live_review.md` is the
source of truth for that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R18 registers R-0434 and R-0435, rules the remaining round map at DECISION F082
D10, and repairs four defects: R-0431's self-contradicting context bullet, the
four stale pin sentences of R-0432 and R-0434, and R-0433's `Any` annotations. It
lands no capability and writes no test.

## Next Steps
1. R19 the acceptance proof for R-0435: the doubles store a DoD verdict, so a
   bench row can PASS, and three properties measure the Goal's three DONE
   conditions over real runs.
2. R20 the integration gate, per docs/agents/integration_gate.md.
3. R21 closure: STATUS line, Built State, closure candidates, the PR.

## Risks
- R-0435 is the closure blocker of record: until R19 lands, NO round may claim
  the bench runs green on fixtures or that a degraded run warns.
- The delivered order set is three, not the Design's five (R-0411), the freeze
  holds against a file-side edit only (R-0410), and the builder's model stays
  unobservable — closure states all three absences rather than implying five
  orders and three recorded roles.
- `wall_s` is clock-derived from `gauntlet_runner.py::run_order` and every row's
  `cost` is `None` under doubles, so pass rate is the only trend a real run can
  prove; cost and wall warnings stay golden-pinned.
- Reviewer defects remain the dominant finding class: fifteen standing
  counter-measures now bind every block, R-0417 through R-0435.
--- END SLICE PLAN ---

────────────────────────────── DONE WHEN ──────────────────────────────
Run every command yourself and report the REAL output and exit code. "Green" as a
word is a finding (G4). Report a number you measured, never one you expected.

 1. `git status --porcelain` EMPTY before your first commit and after your last;
    `git worktree list` ONE line at handback. `.agent/STOP` — report absent or
    present at round START and again at handback (R-0347). Present at any point:
    finish the commit in hand, write the handoff, stop.
 2. TRANSPORT: after C0b, compare `.agent/authored/f082-r18.md` and
    `.agent/last_block.md` with python3 `Path(...).read_bytes()` equality. Report
    True/False, the sha256 and byte count of both, and the real `wc -l`. This
    block declares its own length as 399 lines (R-0420): report the real count
    and say whether it matches.
 3. BASE re-derived: report `git rev-parse HEAD` from before your first commit
    and whether it equals b2ccafea (R-0428).
 4. C1 IS AN APPEND, proven as a PROPERTY over `<C1>^..<C1>`: read `pre` and
    `post` as bytes; report whether `pre` is a PREFIX of `post` and whether
    `post[len(pre):]` decodes to exactly the two slices as ordered. Report the
    added byte count and the `git show --numstat` DELETION column, which MUST
    be 0. Do NOT predict the insertion count.
 5. Line-anchored counts in `.agent/live_review.md` at HEAD, after C5:
    `^- R-0434 — ` 1 · `^- R-0435 — ` 1 · `^## DECISION F082 D10` 1 ·
    `^Landed: ` 4 · `^Landed: R-0435` 0 · `^Done: ` 0 · `^Gate: R18` 0. The last
    is not an omission: the round that writes a gate cannot record the gate on
    itself (planner_reviewer_prompt.md §4.13).
 6. OPEN SET recomputed mechanically from `.agent/live_review.md`, never carried
    forward: every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line.
    Report the count, that no id is registered twice, the maximum id and the next
    free id. Reviewer's expectation: 65 open, max R-0435, next free R-0436 — a
    `Landed:` line does NOT close a finding (§4.4), so all four repaired ones
    remain in this count.
 7. C3's FOUR PAIRS over `<C3>^..<C3>`: for EACH of PIN-DOC, PIN-CONST, PIN-ADDS
    and PIN-HEADER report FROM count in `pre` (1) and in `post` (0), TO count in
    `post` (1), and `FROM in TO` (False — all four are REWRITES). Then the
    COMPOSITE: `pre` with all four replacements applied EQUALS `post` byte-wise
    (R-0422). Also report that `EXPLICIT_BENCH_CALLERS` still holds exactly one
    entry, that the `MIN_SCANNED_FILES` comment line is byte-unchanged
    (Constraint 3), and that `empty today` occurs 0 times in the file.
 8. THE CONTEXT PAIRS, TWO COMMITS, TWO SHAPES — do not conflate them. C4 over
    `<C4>^..<C4>`: CTXIMPLICIT-R18 is a REWRITE — FROM 1x→0x, TO 1x,
    `FROM in TO` False, `pre.replace(FROM, TO) == post` — plus: no line of
    `.agent/context.md` at HEAD begins with `deliberate act` at column 0. C6 over
    `<C6>^..<C6>`: CTXSTEPS-R18 is a REWRITE, same four values; CTXSCOPE-R18 is
    APPEND-SHAPED, its TO CONTAINS its FROM, so FROM stays 1x in `post` BY
    CONSTRUCTION and a FROM-0x gate is unmeetable (§4.9, R-0207) — prove FROM 1x
    in `pre`, TO 1x in `post`, and the composite with BOTH pairs EQUALS `post`.
 9. C2's TWO PAIRS over `<C2>^..<C2>` as ONE composite: `pre` with both
    replacements EQUALS `post`; each FROM 1x→0x; and at HEAD the count of `Any`
    in `bench_run.py` is 0, of `OrderOutcome` 2 and of `BenchRecord` 2.
10. THE ANNOTATIONS RESOLVE, not merely parse (Constraint 2). Run:
    `python3 -c "import typing; from packages.orchestration.bench_run import
    BenchRunResult; print(typing.get_type_hints(BenchRunResult))"` → exit 0.
    Report the printed mapping: `outcomes` and `rows` must resolve to tuples of
    `OrderOutcome` and `BenchRecord`, with `Any` nowhere in it. An unresolvable
    name passes a plain import and fails only here.
11. `python3 -m pytest tests/orchestration/test_bench_run.py -q` → exit 0.
    Reviewer's BASE measurement `7 passed`. NOT edited this round, so it is the
    importer that breaks if C2 got an import wrong; report the real number and
    confirm the file is absent from the change set.
12. THE PIN STILL PASSES AFTER A PROSE-ONLY EDIT:
    `python3 -m pytest tests/orchestration/test_bench_never_runs_implicitly.py -q`
    → exit 0. Reviewer's BASE measurement `6 passed`. C3 changes comments only,
    so a different number means C3 touched an executable line.
13. STILL GREEN, each set run together: the gauntlet seven — reviewer's BASE
    measurement `276 passed` — and the pre-existing bench five — BASE
    `61 passed`. Report both real numbers and exit codes.
14. `python3 -m pytest tests/cli/test_golden_path.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_test_runner.py -q` → exit 0. Reviewer's BASE
    measurement 184 passed. Canary plus the three `.agent`-state contract
    readers, and C4 and C6 both write `.agent/context.md`.
15. `python3 -m ruff check packages/orchestration/bench_run.py
    tests/orchestration/test_bench_never_runs_implicitly.py` → exit 0.
    Reviewer's BASE measurement `All checks passed!`, so red here is THIS round's
    doing. Repo-wide ruff is red on main and NOT gated (R-0364).
16. `python3 -m apps.cli.main integrity check --json` → `passed: true`,
    `fail_count: 0`, `check_count: 5`. Report the `handler_import` message: it
    must still be `handlers=337`, because this round adds NO CLI handler key.
17. NO PRODUCT MODULE BUT `bench_run.py` WAS EDITED, AND NO TEST BUT THE PIN.
    Report `git diff --name-only <BASE>..HEAD` restricted to these ten paths —
    MUST be EMPTY: `packages/orchestration/` `gauntlet_runner.py`,
    `gauntlet_orders.py`, `gauntlet_evidence.py`, `gauntlet_evaluator.py`,
    `gauntlet_matrix.py`, `dod_gate.py`, `capability_bench.py`,
    `bench_history.py`, `bench_dry_run.py`, and
    `tests/orchestration/test_bench_run.py`. Measures Constraint 1 and the ceiling.
18. CHANGE SET: `git diff --name-only <BASE>..HEAD` — report every path, COUNT
    them, and state whether you measured before or after C7. The Change list is
    a CEILING. Restricted to `docs/`, `apps/` and `scripts/` it MUST be EMPTY.
19. `gh pr list --state open --json number,headRefName` → verbatim. Must be
    `[]`. Create NO pull request; the closure round R21 creates it.
20. Report each commit's `git show --numstat <sha>` insertion total. If any
    exceeds 500, declare it with the inseparability reason BEFORE review.
21. STANDING STALENESS GATE (R-0417, tenth run). Re-read every sentence in the
    files this round touched that states a COUNT, a module list, a round-to-step
    map, or a completion claim, and report whether each still holds at HEAD.
    Report the number CHECKED and the number that HOLD. Repair only what an
    ordered slice covers; REPORT anything else and leave it. In scope:
    `bench_run.py`, the pin file, `.agent/context.md`, `.agent/plan.md`, plus
    `test_bench_run.py`'s docstring, which is NOT edited here — a stale claim
    there is REPORTED and left for R19. Verbatim transport and the append-only
    record are OUT of scope by construction. R-0434 exists because the previous
    run of this gate matched a phrase instead of reading the claims.
22. `.agent/plan.md` byte-equals the PLAN slice as a WHOLE FILE — report the
    equality, its sha256, its `wc -l` (must be under 50, AGENTS.md), and that
    `## Goal` and `## Next Steps` are both present. Report `.agent/context.md`'s
    line count too.

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md:
             feature and round (R18/21), branch, the per-commit changed-files
             table, all 22 gate values REAL and trimmed, the item-status table
             covering C0a–C7 and gates 1–22 with `done`/`skipped`/`deviated` and
             a reason for each non-done row, the open-findings count, and the
             next expected action. Repeat the FORTSCHRITT slice VERBATIM
             (R-0418). State plainly that this round landed NO capability and that
             R-0435 is OPEN. If the 60-line cap is exceeded, carry a "Deviations,
             declared" line naming your OWN MEASURED line count as a NUMERAL and
             the mandated content that caused it (AGENTS.md D15, R-0430) — never
             defer the number to a channel that does not survive the session.
             Declare every deviation, including any slice that arrived wrong and
             was applied verbatim anyway. Next action for the next session:
             self_drive_protocol.md Phase 1 rule 1, re-read `.agent/STOP` from
             disk, BEFORE rule 2's Open PR Gate.
──────────────────────────────────────────────────────────────────────────────
