── STEP R13/16 — F082 Self-benchmark ─────────────────────────────────────────
Goal:        Record the R12 verdict, rule at DECISION F082 D8 on the two things
             D7 left open — the module D7 did not name, and the size of T003b —
             and build the WRITE half of T003b: every gauntlet run records which
             model served which role, and an unobserved role is recorded as
             absent rather than as a default name.

Bundle:      C0a save this block · C0b mirror it · C1 GATE-R12 + DECISION-D8
             appended to the review record · C2 the code · C3 the new test file
             · C4 plan and step-map re-sync · C5 handback.

Change:      This list is a CEILING. Nothing outside it.
             - .agent/authored/f082-r13.md                     (C0a, new)
             - .agent/last_block.md                            (C0b)
             - .agent/live_review.md                           (C1 append)
             - packages/orchestration/intake.py                (C2, INTAKE pair)
             - packages/orchestration/gauntlet_runner.py       (C2, six pairs)
             - tests/orchestration/test_bench_model_context.py (C3, NEW file)
             - .agent/plan.md, .agent/context.md               (C4)
             - .agent/handoff.md                               (C5)
             NOT in scope: `docs/**`, `apps/**`, `scripts/**`, and EVERY
             existing test file. No existing test file is edited for any
             reason: if one must change, the change is not additive and the
             round STOPS and hands off.

Constraints:
 1. DECISION F082 D7's three conditions bind this round. ADDITIVE: no existing
    key of the evidence body changes name, type or meaning. The gauntlet's
    seven test files stay green UNMODIFIED. An absent binding is recorded as
    absent — never as a default model name, never as a re-resolution from
    config. A configured model is not the model that ran; that is why the value
    is read off the instance that serves the calls.
 2. The builder role is NOT observable from the runner —
    `orchestrator_loop.py::execute_dispatched_job` constructs `OllamaBuilder()`
    itself. It is recorded as an absence, with the WHY comment saying so. Do
    NOT reach into `orchestrator_loop.py` to make it observable; that is R14.
 3. `_minimal_body` deliberately does NOT gain the key. It is the crash-of-crash
    fallback and is already a declared SUBSET of the evidence body; widening it
    is out of scope. Do not touch it.
 4. `.agent/plan.md` stays under 50 lines and keeps `## Goal` and
    `## Next Steps`. `.agent/context.md` keeps `## Active Branch` with its
    `feature/` slug, the substring `Steps`, a roadmap F-id, and `pytest` or
    `resource`.
 5. Apply every slice DISK-TO-DISK out of the COMMITTED
    `.agent/authored/f082-r13.md`. No `--- BEGIN SLICE` / `--- END SLICE`
    marker line may reach any target file. No target file gains a
    trailing-whitespace line.
 6. Every commit follows the AGENTS.md self-review loop and the Commit Gate.
    Insertions per commit stay under 500. No commit trailer.
 7. Apply every slice VERBATIM. If a slice is wrong on arrival, apply it as
    ordered and DECLARE it in the handback — do not silently repair it. A
    "fixed" slice breaks the byte-equality gates that make transport provable
    and the repair becomes invisible (finding R-0419).

────────────────────────── AUTHORED SLICES ──────────────────────────

--- BEGIN SLICE GATE-R12 --- (append to .agent/live_review.md, C1, ONE physical line)
Gate: R12 — PASS, with no new finding; the first clean round on this branch in some time. Verification tier: round gate plus the canary; no full-suite claim is made and none is owed. All sixteen ordered gates were re-executed by the reviewer against the disk rather than read out of the handback, and every one reproduces at its reported value. Transport is proven at PRIMARY strength: `.remedy-wt/f082-r12-scratchpad.md`, `.agent/authored/f082-r12.md` and `.agent/last_block.md` are byte-identical at shared sha256 `debf254122da4712916bde4baa4f0f712fa315f51c61dcfa1ec92ac967721574`, 22603 bytes and 266 lines, and python3 `read_bytes()` equality holds across all three. The C1 append is a PROPERTY and was proven as one: over the committed `9fdc6d8e^`→`9fdc6d8e`, `post.startswith(pre)` is TRUE, the appended region is 8806 bytes, and the reviewer additionally extracted GATE-R11, FINDING-R419 and DECISION-D7 from the committed authored file and confirmed `add == newline + GATE-R11 + blank + FINDING-R419 + blank + DECISION-D7 + newline` byte-for-byte — so the append is not merely an append, it is exactly the three ordered slices and nothing else, with zero marker lines reaching the record and the numstat deletion column at 0. The record counts are `^Gate: R11 — PASS` 1, `^- R-0419 — ` 1, `^## DECISION F082 D7` 1, `^## DECISION F082 D6` 1 still standing unrewritten, `^Landed: ` 0 and `^Done: ` 0; the open set recomputed mechanically is FORTY-NINE with no duplicate, max R-0419 and next free R-0420. Gate 9 is the round's point and it lands: `only one role is bound to a model` is 0 in the mirror and `found exactly one role bound to a model` is exactly 2 in the record, one inside DECISION F082 D6 where Constraint 1 forbids rewriting it and one inside FINDING-R419 which quotes it on purpose. The CTXSTEPS3 pair holds as a property — `post == pre.replace(FROM, TO)` TRUE over the committed `04a24aba`, FROM 1x to 0x, TO 0x to 1x, `FROM in TO` False — and `.agent/plan.md` byte-equals the PLAN slice as a whole file at sha256 `cbdae4c19e7ac621d5d9442d84fb013fd90b3732a62232f6710e9c2e8e04fa31`, 49 lines, both required headings present, with `.agent/context.md` at 68 lines keeping every contract reader. The change set is six paths, every one inside the block's Change list, and `git diff --name-only e6c18d89..HEAD -- apps/ packages/ tests/ docs/` is EMPTY, which is the promise a verdict round exists to keep. Suites re-run by the reviewer at the branch head: the canary plus the three contract readers `184 passed`, `tests/cli/test_stats_bench.py` `25 passed`, and `integrity check --json` `passed: true`, `fail_count: 0` over 5 checks with `handlers=337` unchanged. Insertions per commit are 266, 174, 49 and 31, none over 500, `git status --porcelain` is empty, `git worktree list` is the single primary checkout, `.agent/STOP` is absent, and `gh pr list --state open` is `[]`. The reviewer also went past the gates and spot-checked the round's substance, because R-0419 is precisely the finding that says a claim nobody re-ran is not evidence: R-0419's own charge is upheld against the code — `packages/providers/ollama_planner/provider.py::_resolve_model:54` and `packages/providers/ollama_builder/provider.py::_resolve_model:175` both exist and each binds a further role to a model, so the R11 block's "exactly one role" was indeed false — and DECISION-D7's premise was re-read line by line at `gauntlet_runner.py::_evidence_body`, where the dict literal carries FIFTEEN keys and exactly one of `tokens` or `tokens_source` is then added unconditionally, so every EMITTED body carries sixteen and none of them is a model. The worker's qualified hold on that numeral was therefore accurate, and declaring it rather than quietly correcting the slice was the right call twice over. One thing the reviewer found that the round did not owe and R13 does: `::_evidence_body` is not the only writer of a run body — `::_minimal_body` writes a thirteen-key subset on the crash-of-crash path — so the count-the-writers rule that produced R-0419 applies to D7's own key, and the R13 block binds both writers explicitly rather than leaving the second one to be discovered later. No block condition was hit: no fabricated data, no false live indicator, no missing changed-files table, no unverified completion claim, no silent scope change.
--- END SLICE GATE-R12 ---

--- BEGIN SLICE DECISION-D8 --- (append to .agent/live_review.md, C1, after GATE-R12, blank line between)
## DECISION F082 D8 — the module D7 did not name, and the size of T003b

This decision EXTENDS DECISION F082 D7 (it does not supersede it; D7's three
conditions stand unchanged and bind R13) and settles two things D7 left open.

**Part one — `intake.py` is inside the exception.** D7 granted the additive
`models` key to `gauntlet_runner.py::_evidence_body` and named no other module.
But the honest value for the planner and orchestrator roles does not live in
`gauntlet_runner.py`. `packages/orchestration/intake.py::make_structured_call_fn`
constructs the `OllamaPlanner` that will actually serve every call and then
returns only the closure, discarding the one thing worth recording:
`planner.model`, the model that instance resolved. So T003b MAY add ONE
assignment plus its WHY comment to that factory, attaching the resolved model
to the callable it already returns.

The scope of this exception is deliberately tiny and is stated so it cannot
creep: no signature changes, no return type changes, no behaviour changes, and
no caller is affected. `make_structured_call_fn` has six call sites — one
inside `intake.py` itself, two in `gauntlet_runner.py`, two in
`apps/cli/commands/mission_cmd.py` and two in `apps/cli/commands/do_cmd.py` —
and every one of them keeps receiving exactly the callable it receives today.
The count was taken with a repository-wide grep before this decision was
written, which is the standing rule R-0419 imposed.

Alternatives considered: (a) re-resolve the model inside the runner by calling
`ollama_planner/provider.py::_resolve_model` — REJECTED, and this is the whole
reason the decision exists. That re-derives a CONFIGURED value and writes it
into evidence as though it were observed, which is exactly what
`gauntlet_runner.py::run_order`'s own comment refuses to do (DECISION F105 D13)
and exactly what `token_ledger.py::call_record_from_evidence` refuses for its
own `model` column. It would also be silently WRONG whenever the factory
returned None because Ollama was unreachable: the evidence would name a model
for a call that never happened. (b) Record nothing for those two roles —
REJECTED; it leaves the Design bullet unbuilt while the observed value is one
attribute away.

**Part two — T003b is split in half.** As planned, R13 carried the model-context
write path, the read path into the bench record, AND a fake-provider bench run
whose four blockers R11's Q6 names. That is three separable deliverables in one
round, and the middle one needs `gauntlet_evidence.py::RunEvidence` — a THIRD
gauntlet module that neither D7 nor part one of this decision names. Chosen:
R13 builds the WRITE half only — the models reach `run.json` and are pinned by
tests. R14 builds the READ half (`RunEvidence` to `BenchRecord`, which needs its
own additive ruling) together with the fake-provider run and the Q7 pin for
"the bench never runs implicitly". R15 is the integration gate and R16 closure.

Why split rather than push: a round that cannot be gated as one thing cannot be
reviewed as one thing. The write half has a crisp falsifiable gate — the models
appear in the emitted body, absences stay absent, and the gauntlet's seven test
files stay green unmodified — and that gate is worth having on its own before
anything reads the value.

How to reverse: delete part one and the planner/orchestrator models are
unobservable, so T003b records three absences and the Design bullet closes
unbuilt with an assumption_log entry. Delete part two and R13 reverts to the
three-deliverable round, at the review cost stated above.
--- END SLICE DECISION-D8 ---

--- BEGIN SLICE INTAKE-FROM --- (in packages/orchestration/intake.py, C2 — REWRITE pair)
    schema = to_json_schema(model_cls)

    def _call(prompt: str, attempt: int) -> str:
        return planner.raw_call(prompt, schema=schema)

    return _call
--- END SLICE INTAKE-FROM ---

--- BEGIN SLICE INTAKE-TO --- (C2)
    schema = to_json_schema(model_cls)

    def _call(prompt: str, attempt: int) -> str:
        return planner.raw_call(prompt, schema=schema)

    # F082 T003b (DECISION F082 D8): the model this call_fn will ACTUALLY serve
    # with, read off the instance that serves it rather than re-resolved from
    # config — a configured model is not the model that ran, the same rule
    # `token_ledger.py::call_record_from_evidence` keeps for its own column.
    # Readers use `getattr(fn, "resolved_model", None)`, so an unlabelled
    # call_fn reads as an absence and never as a default name.
    _call.resolved_model = planner.model  # type: ignore[attr-defined]
    return _call
--- END SLICE INTAKE-TO ---

--- BEGIN SLICE RUNNERINIT-FROM --- (in packages/orchestration/gauntlet_runner.py, C2 — REWRITE pair)
    body: dict[str, Any] = _minimal_body(order, before)

    try:
--- END SLICE RUNNERINIT-FROM ---

--- BEGIN SLICE RUNNERINIT-TO --- (C2)
    body: dict[str, Any] = _minimal_body(order, before)
    # F082 T003b: which model served which role, filled in as each call_fn is
    # built and read back out into the evidence body. Bound BEFORE the try for
    # the same R-0180 reason as `body`, so the crash path still records what
    # was resolved before the crash. A role this seam cannot observe stays
    # None: an invented model is the exact class of lie F082 exists to prevent,
    # and the same honesty that keeps `repair_rounds` None rather than 0.
    # The builder is never observable here — `orchestrator_loop.py::
    # execute_dispatched_job` constructs `OllamaBuilder()` itself, so no value
    # reaches this seam at all. It is recorded as an absence on purpose.
    models: dict[str, str | None] = {
        "planner": None, "orchestrator": None, "builder": None,
    }

    try:
--- END SLICE RUNNERINIT-TO ---

--- BEGIN SLICE RUNNERCALLS-FROM --- (in packages/orchestration/gauntlet_runner.py, C2 — REWRITE pair)
            deps.plan_mission(project_id, mission.id, deps.plan_call_fn(),
                              max_milestones=len(order.milestones) + 1)
            seams = build_injectors(
                order.injections,
                call_fn=deps.move_call_fn(),
--- END SLICE RUNNERCALLS-FROM ---

--- BEGIN SLICE RUNNERCALLS-TO --- (C2)
            plan_call = deps.plan_call_fn()
            models["planner"] = getattr(plan_call, "resolved_model", None)
            deps.plan_mission(project_id, mission.id, plan_call,
                              max_milestones=len(order.milestones) + 1)
            move_call = deps.move_call_fn()
            models["orchestrator"] = getattr(move_call, "resolved_model", None)
            seams = build_injectors(
                order.injections,
                call_fn=move_call,
--- END SLICE RUNNERCALLS-TO ---

--- BEGIN SLICE RUNNERBODY1-FROM --- (in packages/orchestration/gauntlet_runner.py, C2 — REWRITE pair, the SUCCESS path; the `gate =` line disambiguates it from the crash path)
            body = _evidence_body(order, terminal, time.monotonic() - started,
                                  entries, mission, injectors, before, data_root)
            gate = latest_gate_result(mission)
--- END SLICE RUNNERBODY1-FROM ---

--- BEGIN SLICE RUNNERBODY1-TO --- (C2)
            body = _evidence_body(order, terminal, time.monotonic() - started,
                                  entries, mission, injectors, before,
                                  data_root, models)
            gate = latest_gate_result(mission)
--- END SLICE RUNNERBODY1-TO ---

--- BEGIN SLICE RUNNERBODY2-FROM --- (in packages/orchestration/gauntlet_runner.py, C2 — REWRITE pair, the CRASH path; note the deeper indentation)
                body = _evidence_body(order, terminal, time.monotonic() - started,
                                      entries, mission, injectors, before, data_root)
--- END SLICE RUNNERBODY2-FROM ---

--- BEGIN SLICE RUNNERBODY2-TO --- (C2)
                body = _evidence_body(order, terminal,
                                      time.monotonic() - started,
                                      entries, mission, injectors, before,
                                      data_root, models)
--- END SLICE RUNNERBODY2-TO ---

--- BEGIN SLICE RUNNERSIG-FROM --- (in packages/orchestration/gauntlet_runner.py, C2 — REWRITE pair)
def _evidence_body(order: GauntletOrder, terminal: str, wall: float,
                   entries: list[Any], mission: Any, injectors: list[Any],
                   before: str, data_root: Path) -> dict[str, Any]:
--- END SLICE RUNNERSIG-FROM ---

--- BEGIN SLICE RUNNERSIG-TO --- (C2)
def _evidence_body(order: GauntletOrder, terminal: str, wall: float,
                   entries: list[Any], mission: Any, injectors: list[Any],
                   before: str, data_root: Path,
                   models: dict[str, str | None] | None = None,
                   ) -> dict[str, Any]:
--- END SLICE RUNNERSIG-TO ---

--- BEGIN SLICE RUNNERKEY-FROM --- (in packages/orchestration/gauntlet_runner.py, C2 — REWRITE pair)
        "template_digest": _template_digest(),
    }
--- END SLICE RUNNERKEY-FROM ---

--- BEGIN SLICE RUNNERKEY-TO --- (C2)
        "template_digest": _template_digest(),
        # F082 T003b (DECISION F082 D7 and D8): which model served which role.
        # An unobserved role is None, never a default name. The dict is copied
        # so a later mutation of the caller's own map cannot rewrite evidence
        # that has already been recorded.
        "models": dict(models) if models else {
            "planner": None, "orchestrator": None, "builder": None},
    }
--- END SLICE RUNNERKEY-TO ---

--- BEGIN SLICE CTXSTEPS4-FROM --- (in .agent/context.md, C4 — REWRITE pair)
gauntlet key at D7 → R13 T003b model context and a fake-provider run → R14 the
integration gate → R15 closure. T003 split at DECISION F082 D5, its second half
inventoried at D6 and unblocked at D7; each round marks the PREVIOUS one done
and never itself.
--- END SLICE CTXSTEPS4-FROM ---

--- BEGIN SLICE CTXSTEPS4-TO --- (C4)
gauntlet key at D7 ✅ → R13 T003b the write half, every run recording which model
served which role → R14 T003b the read half and the fake-provider run → R15 the
integration gate → R16 closure. T003 split at DECISION F082 D5, its second half
inventoried at D6, unblocked at D7 and split in two at D8; each round marks the
PREVIOUS one done and never itself.
--- END SLICE CTXSTEPS4-TO ---

--- BEGIN SLICE FORTSCHRITT --- (the Fortschritt line; the handoff repeats it VERBATIM, R-0418)
Fortschritt: ~82 % (T001 ✅ · T002 ✅ · T003a ✅ · T003b Schreibhälfte gebaut · Lesehälfte und Fake-Provider-Lauf offen) — Schätzung
--- END SLICE FORTSCHRITT ---

--- BEGIN SLICE PLAN --- (WHOLE-FILE replacement of .agent/plan.md, C4)
# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0420. Open findings: forty-nine — the thirty-two carried from F077, plus
R-0403 to R-0419 registered on this branch. `.agent/live_review.md` is the
source of truth for that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R13 records the R12 gate, rules at DECISION F082 D8 that `intake.py` is inside
D7's exception and that T003b splits in two, and builds the WRITE half: a
gauntlet run records which model served which role in its own `run.json`, and a
role the runner cannot observe is recorded as absent rather than guessed.

## Next Steps
1. R14 — T003b the read half and the run: carry the models from
   `gauntlet_evidence.py::RunEvidence` into the bench record, which needs its
   own additive ruling; then the fake-provider bench run, clearing R11's Q6
   four blockers — no entry point, local-Ollama reach, a `time.monotonic()`
   call in `::run_order`, and history resolving to the real data root; and the
   Q7 pin for "the bench never runs implicitly".
2. R15 the integration gate, R16 closure.

## Risks
- "The bench never runs implicitly" is an ACCEPTANCE criterion that NO test
  pins (R11 Q7). It holds today only by absence: `append_bench_run` and
  `dry_run_from_order_set` have no caller under `apps/`, `packages/` or
  `scripts/`. An unpinned criterion found at closure is a closure blocker, so
  R14 pins it.
- The builder's model stays unobservable after R13, because making it visible
  means reaching into `orchestrator_loop.py::execute_dispatched_job`. Closure
  states that absence rather than implying three roles were recorded.
- The delivered order set is three, not the Design's five (R-0411). Closure
  may not quote five, and DECISION F082 D3 binds the recovery to a
  bench-owned fixture rather than an edit to the gauntlet's template.
- The freeze holds against a file-side edit only (R-0410). The Built State
  states that threat model rather than quoting the acceptance criterion whole.
- Reviewer-block defects, not worker defects, are the dominant finding class on
  this branch. No count is stated here because none has been taken; R-0417's
  staleness gate, R-0418's Fortschritt rule and R-0419's grep-every-writer
  rule are the counter-measures, and all three bind every block from here.
--- END SLICE PLAN ---

────────────────────── C3 — THE NEW TEST FILE, BY CONTRACT ──────────────────
`tests/orchestration/test_bench_model_context.py`, a NEW bench-owned file. It
is a new file and not an addition to `tests/orchestration/test_gauntlet_runner.py`
because that file is one of the gauntlet's seven and Constraint 1 freezes it;
declare that naming deviation from the `test_x.py` ↔ `x.py` convention in the
handback with this reason. Drive `run_order` through `RunnerDeps` doubles — read
`tests/orchestration/test_gauntlet_runner.py` for the established double
pattern, do not modify it — and pin exactly these five properties:

 1. A run whose `plan_call_fn` and `move_call_fn` return callables carrying
    `resolved_model` records those two names under `run.json`'s `models`.
 2. A run whose call_fns return callables with NO `resolved_model` attribute
    records `None` for those roles — an absence, not a default.
 3. A run whose call_fns return None (the unreachable-Ollama case, which
    `make_structured_call_fn` really does return) records `None`, and does not
    raise.
 4. `models["builder"]` is `None` in every case above.
 5. The EXACT key set of the emitted body. Assert it equals the sixteen keys
    that exist at BASE plus `models` — name them in the assertion so a future
    rename is caught. The base sixteen are `gauntlet_run_version`, `order_id`,
    `kind`, `terminal_status`, `wall_seconds`, `operator_interventions`,
    `data_root_hash_before`, `postmortems`, `open_decisions`, `era_defects`,
    `injections`, `evidence_links`, `cycles_budget`, `cycles_resolved`,
    `template_digest`, and exactly one of `tokens` or `tokens_source`.

Property 5 is the additivity proof for DECISION F082 D7's first condition, so
it must assert the whole set rather than the presence of `models` alone.

────────────────────────── DONE WHEN ──────────────────────────
Run every gate. Record its REAL output. "Green" as a word is a finding. Order
the COLOUR of a red proof, never its count. BASE is b0ea45c9.

 1. `git status --porcelain` EMPTY at handback; `git worktree list` back to
    exactly the primary checkout. Report both verbatim.
 2. TRANSPORT AS A PROPERTY: sha256 and byte length of
    `.agent/authored/f082-r13.md` and `.agent/last_block.md`. EQUAL, proven by
    python3 `read_bytes()` equality as well as by digest. Report the shared
    digest and the line count; ≤ 400.
 3. `.agent/STOP` — report presence at round START and at handback. Absent
    both times. If it appears, finish the current commit and hand off.
 4. C1 APPEND PROOF: over the COMMITTED `<C1>^` and `<C1>`, report whether
    `post == pre + add` holds BYTE-WISE, where `add` is GATE-R12 and
    DECISION-D8 joined exactly as committed. Report the C1 `--numstat`; its
    DELETION column must be 0.
 5. RECORD COUNTS in `.agent/live_review.md` at HEAD: `^Gate: R12 — PASS` 1 ·
    `^## DECISION F082 D8` 1 · `^## DECISION F082 D7` 1 (still there — D7 is
    history and is NOT rewritten) · `^Landed: ` 0 · `^Done: ` 0. Report each
    real number.
 6. OPEN SET RECOMPUTED MECHANICALLY: every `^- R-\d+ — ` paragraph minus
    every `^Done: R-\d+ — ` line. Report the count, the max id, the next free
    id, and any duplicate. R13 registers NO finding, so the expected count is
    FORTY-NINE and the next free id stays R-0420 — report the real numbers
    whatever they are.
 7. EVERY SLICE PAIR AS A PROPERTY, over its own COMMITTED revision: for each
    of INTAKE, RUNNERINIT, RUNNERCALLS, RUNNERBODY1, RUNNERBODY2, RUNNERSIG,
    RUNNERKEY and CTXSTEPS4, report whether
    `post == pre.replace(FROM, TO)` holds byte-wise, and report FROM going 1x
    to 0x and TO going 0x to 1x. Report `FROM in TO` for each; where it is
    True the pair is APPEND-shaped and the FROM legitimately stays 1x after —
    say which pairs those are rather than asserting a uniform shape.
 8. `.agent/plan.md` at HEAD BYTE-EQUALS the PLAN slice as a WHOLE FILE.
    Report its sha256 and `wc -l`; under 50. Report `wc -l` for
    `.agent/context.md`. Contract readers of `.agent/context.md`:
    `## Active Branch` followed by a `feature/` slug · substring `Steps` ·
    a roadmap F-id · `pytest` or `resource`. Plan keeps `## Goal` and
    `## Next Steps`.
 9. THE GAUNTLET SEVEN STAY GREEN, UNMODIFIED — DECISION F082 D7's second
    condition, and the round's stop condition.
    (a) `python3 -m pytest tests/orchestration/test_gauntlet_runner.py
        tests/orchestration/test_gauntlet_evaluator.py
        tests/orchestration/test_gauntlet_evidence.py
        tests/orchestration/test_gauntlet_injection.py
        tests/orchestration/test_gauntlet_matrix.py
        tests/orchestration/test_gauntlet_orders.py
        tests/orchestration/test_self_run_gauntlet.py -q` → exit 0. The
        reviewer measured 276 passed at BASE. Report the real number.
    (b) `git diff --name-only b0ea45c9..HEAD -- <those same seven paths>` must
        be EMPTY. Report it. A non-empty result means the change was not
        additive: STOP and hand off rather than editing a test to fit.
10. THE ABSENCE IS REAL (D7's third condition). From the run in property 2 or
    3 of the new test file, report that the emitted `models` values are Python
    `None` — and report the result of searching that run's `run.json` bytes for
    the string `llama`, case-insensitive. It must be 0. A default model name
    reaching evidence is the failure this condition exists to prevent.
11. RED-PROOF, in a DISPOSABLE WORKTREE under `.remedy-wt/` and never in the
    primary checkout (G5). Check BASE out there, copy ONLY the new test file
    in, and run it. Report the COLOUR and the assertion text of the first
    failure. It MUST be RED — the models key does not exist at BASE. Do not
    report or predict a pass/fail COUNT; the colour is the claim. Remove the
    worktree afterwards and prove gate 1 again.
12. `python3 -m pytest tests/orchestration/test_bench_model_context.py -q` →
    exit 0 at HEAD. Report the real number.
13. `python3 -m pytest tests/orchestration/test_intake.py
    tests/orchestration/test_intake_prompt_golden.py -q` → exit 0. The
    reviewer measured 43 passed at BASE. Report the real number. The INTAKE
    pair changes a factory these tests cover.
14. `python3 -m pytest tests/cli/test_golden_path.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_test_runner.py -q` → exit 0. Reviewer baseline at
    BASE: 184 passed. Report the real number; if it moved, report that as a
    finding rather than adjusting anything.
15. `python3 -m pytest tests/cli/test_stats_bench.py -q` → exit 0, 25 passed
    at BASE. Report the real number.
16. `python3 -m ruff check packages/orchestration/intake.py
    packages/orchestration/gauntlet_runner.py
    tests/orchestration/test_bench_model_context.py` → report the real exit
    code and output. The reviewer measured `All checks passed!` on the first
    two at BASE, so this gate can fail honestly. Repository-wide `ruff check`
    is RED on main and is NOT a gate (R-0364).
17. `python3 -m apps.cli.main integrity check --json` → `passed: true`,
    `fail_count: 0`, `check_count: 5`. Report the `handler_import` message; it
    must still be `handlers=337`.
18. CHANGE SET: `git diff --name-only b0ea45c9..HEAD` — report every path,
    COUNT them, and state whether you measured before or after C5. The Change
    list is a CEILING. Report
    `git diff --name-only b0ea45c9..HEAD -- docs/ apps/ scripts/`
    separately; it MUST be EMPTY.
19. `gh pr list --state open --json number,headRefName` → report verbatim.
    Must be `[]`.
20. Report each commit's `git show --numstat <sha>` insertion total. If any
    exceeds 500, declare it with the inseparability reason BEFORE review. C5
    cannot state its own numstat; report it in the completion report.
21. STANDING STALENESS GATE (R-0417, fifth run). Re-read every sentence in the
    files this round touched that states a COUNT, a module list, a round→step
    map, or a completion claim, and report for each whether it still holds at
    HEAD. Repair ONLY what the ordered slices cover; report everything else and
    leave it. State how many sentences you checked.

Handback:    Completion report + rewrite `.agent/handoff.md` per
             docs/agents/handback_template.md: feature and round, branch, the
             per-commit changed-files tables, the real verification values
             above, the item-status table with every C0a–C5 item and every
             gate 1–21 appearing exactly once, open-findings count, and the
             next expected action. Declare every deviation with its cause.
             The handoff repeats the FORTSCHRITT slice above VERBATIM (R-0418).
             Push after every commit. Create NO pull request.

             THE NEXT SESSION'S FIRST ACTION is self_drive_protocol.md Phase 1
             rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2's Open PR
             Gate. Say so in the handoff's Next section. F082 is MID-FEATURE
             and no PR exists.
──────────────────────────────────────────────────────────────────────────────
