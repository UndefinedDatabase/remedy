── STEP R39 — F105 ───────────────────────────
Goal:        Half of R-0256, the half that is provable on its own: `run_intake`
             and `plan_job_llm` accept a keyword-only `composed`, one test each
             pins that the provider then sees exactly those bytes, and both are
             red-proofed. Also record the R38 reviewer gate. The three
             `do_cmd.py` call sites follow in R40 — this block would exceed
             DECISION F105 D5's 400-line cap with them in it, and a block over
             the cap cannot be fixed downstream (D8 item 1).
Bundle:      C1 save this block · C2 record the R38 gate · C3 the two
             signatures · C4 the two tests · C5 plan and handoff.
Change:      `.agent/authored/f105-r39-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `packages/orchestration/intake.py`,
             `packages/orchestration/flight_plan.py`,
             `tests/orchestration/test_intake.py`,
             `tests/orchestration/test_flight_plan.py`, `.agent/plan.md`,
             `.agent/handoff.md`. Nothing else. No `apps/` and no `docs/` byte
             changes this round.
Constraints: Do not touch the composers — `compose_intake_prompt` and
             `compose_flight_plan_prompt` keep every byte, which is what makes
             gate H mean anything. Do not move `prompt = ...` in `plan_job_llm`
             inside the `try`: that is R-0262, NOT fixed this round. Do not
             reflow any line you were not given a pair for. Do not touch
             `apps/cli/commands/do_cmd.py` — R40 owns it. Write no `Done:`
             paragraph of your own (§4.4); no TO offers a `Landed:` slot, so
             write none.
Done when:   every gate below is run and its REAL exit code recorded.

C1 — save this block verbatim, TWO commits
  C1a `cp /home/decodeux/Repos/remedy/.remedy-wt/f105-r39-1.block.md`
      `.agent/authored/f105-r39-1.md`. Commit it ALONE.
  C1b `cp` the same bytes to `.agent/last_block.md`. Commit separately.
  `sha256sum` all three plus `cmp`; digest in the handback.

C2 — `.agent/live_review.md`, ONE commit
  Apply PAIR_LR, appended at the END of the file. No next-free-ID bump: this
  round registers no new finding.

C3 — the two signatures, ONE commit
  Apply PAIR_INTAKE to `packages/orchestration/intake.py`, then PAIR_FP and
  PAIR_FP2 to `packages/orchestration/flight_plan.py`.

C4 — the two tests, ONE commit
  Apply PAIR_TI and PAIR_TF, CONTAINS-FROM appends at the END of their files.
  Each adds ONE test, for the `composed` branch only: the default branch is
  already covered by the existing tests in both files, which call these
  functions without it. Then run gate I, in a DISPOSABLE worktree only.

C5 — plan and handoff, ONE commit
  Apply PAIR_P_PLAN to `.agent/plan.md` as a FULL replacement, then rewrite
  `.agent/handoff.md` in your own words per AGENTS.md.

<<<PAIR_LR_FROM>>>
  `LAST_REVIEWED_SHA` advances 25e6326a -> c30b365e.
<<<END_PAIR_LR_FROM>>>

<<<PAIR_LR_TO>>>
  `LAST_REVIEWED_SHA` advances 25e6326a -> c30b365e.
- R38: state round — record the R37 gate, resolve R-0261, register R-0262.
  No production code.
- Reviewer gate on R38 (2026-08-10): PASS. Range `c30b365e..5ca4debd` = four
  commits, five paths, every one under `.agent/`. Insertions per commit 230,
  156, 62 and 70, each far under 500.
  Transport by the PRIMARY shape, not the §4.9 fallback: the scratch original
  `.remedy-wt/f105-r38-1.block.md`, the committed
  `.agent/authored/f105-r38-1.md` and `.agent/last_block.md` all three hash to
  `d746b069f3954dada7f39dbc1b24a15fba7d5911f2cf671f66b828dc160ee46a`
  at 230 lines against D5's cap of 400; both `cmp` runs silent.
  All four pairs re-sliced from the COMMITTED authored file by this reviewer's
  own whole-line marker reader, never retyped: DECLARED equals MEASURED for
  every one, every FROM 1x before its write. PAIR_A REWRITE at FROM 0x / TO 1x
  after; PAIR_B and PAIR_C CONTAINS-FROM at FROM 1x / TO 1x. PAIR_P_PLAN is
  byte-equal to the applied `.agent/plan.md` at 49 lines against the cap of 50.
  C2 reconciles against `+62/-1` with 0 strays in both directions.
  Gates re-run by THIS reviewer, none taken from the handback: `tests/docs/`
  `294 passed in 0.30s`; the dashboard contract `70 passed in 4.06s`; the
  canary `42 passed in 19.81s`; `^<<<` count 0 in all three written targets;
  `^## Steps` exactly 1x in live_review, `## Goal` exactly 1x in plan;
  `grep -c 7335` 0 in both test files, which is the R-0261 resolution this
  round records; `git status --porcelain` empty and `git worktree list` the
  primary alone at this verdict. R-0262 was checked against source rather than
  accepted: `packages/orchestration/flight_plan.py:454` holds
  `prompt = _build_plan_prompt(intake)` directly above the `try:` at 455.
  One deviation, DECLARED and ACCEPTED: the block's gate G named base
  `25e6326a`, one round stale, so its no-drift list spanned R37 too and showed
  two `tests/` paths already gated PASS at R37. Over the round's OWN range the
  list is `.agent/` only, so the gate's intent held. The defect is the
  reviewer's, not the round's: a gate G base must be the CURRENT
  `LAST_REVIEWED_SHA`. A lesson, not a finding — the call R37 made for its own
  reviewer-side defect, and the cost here was likewise nil.
  `LAST_REVIEWED_SHA` advances c30b365e -> 5ca4debd.
- R39: SPLIT round — record the R38 gate and take the first half of R-0256: a
  keyword-only `composed` on `run_intake` and `plan_job_llm`, one test each,
  both red-proofed. The three `do_cmd.py` call sites are R40's, split out
  because one block carrying both would have broken the D5 cap.
<<<END_PAIR_LR_TO>>>

<<<PAIR_INTAKE_FROM>>>
def run_intake(
    mission: str,
    call_fn: Callable[[str, int], str],
    *,
    on_call: Callable[[int, str, bool, str], None] | None = None,
) -> IntakeResult:
    """LLM-backed intake with heuristic fallback on failure."""
    try:
        outcome: StructuredOutcome = run_structured_call(
            JobIntake,
            _build_intake_prompt(mission),
<<<END_PAIR_INTAKE_FROM>>>

<<<PAIR_INTAKE_TO>>>
def run_intake(
    mission: str,
    call_fn: Callable[[str, int], str],
    *,
    on_call: Callable[[int, str, bool, str], None] | None = None,
    composed: ComposedPrompt | None = None,
) -> IntakeResult:
    """LLM-backed intake with heuristic fallback on failure.

    ``composed`` lets a caller that ALREADY composed this prompt — the CLI, for
    its trace manifest — hand those exact bytes over, so one composition feeds
    both the provider and the evidence row and a manifest can no longer
    describe bytes that were never sent (R-0256). Omitted, this function
    composes for itself as it always has. The expression stays the ARGUMENT
    inside the ``try``: a raising composer becomes the heuristic fallback,
    never an escape (R-0257).
    """
    try:
        outcome: StructuredOutcome = run_structured_call(
            JobIntake,
            composed.text if composed is not None else _build_intake_prompt(mission),
<<<END_PAIR_INTAKE_TO>>>

<<<PAIR_FP_FROM>>>
    on_call: Callable[[int, str, bool, str], None] | None = None,
    granularity: GranularityConfig | None = None,
) -> FlightPlanResult:
    """Generate a FlightPlan from a job's intake via LLM.

    Uses run_structured_call for schema validation + one parse retry.
    Returns a FlightPlanResult; on failure, plan is None and error_hint
    describes the failure class.
<<<END_PAIR_FP_FROM>>>

<<<PAIR_FP_TO>>>
    on_call: Callable[[int, str, bool, str], None] | None = None,
    granularity: GranularityConfig | None = None,
    composed: ComposedPrompt | None = None,
) -> FlightPlanResult:
    """Generate a FlightPlan from a job's intake via LLM.

    Uses run_structured_call for schema validation + one parse retry.
    Returns a FlightPlanResult; on failure, plan is None and error_hint
    describes the failure class.

    ``composed`` lets a caller that ALREADY composed this prompt — the CLI, for
    its trace manifest — hand those exact bytes over, so one composition feeds
    both the provider and the evidence row (R-0256). Omitted, this function
    composes for itself as it always has. The composition deliberately stays
    ABOVE the ``try``: moving it inside is R-0262, which needs this function
    and the CLI's call sites in one round and is NOT fixed here.
<<<END_PAIR_FP_TO>>>

<<<PAIR_FP2_FROM>>>
    prompt = _build_plan_prompt(intake)
<<<END_PAIR_FP2_FROM>>>

<<<PAIR_FP2_TO>>>
    prompt = composed.text if composed is not None else _build_plan_prompt(intake)
<<<END_PAIR_FP2_TO>>>

<<<PAIR_TI_FROM>>>
        fn("test prompt", 0)
        assert captured["chat_kwargs"]["model"] == "intake-test-model"
<<<END_PAIR_TI_FROM>>>

<<<PAIR_TI_TO>>>
        fn("test prompt", 0)
        assert captured["chat_kwargs"]["model"] == "intake-test-model"


class TestRunIntakeAcceptsAComposedPrompt:
    """R-0256: one composition feeds the provider AND the trace manifest."""

    def test_composed_text_is_exactly_what_the_provider_sees(self):
        from packages.orchestration.intake import compose_intake_prompt

        composed = compose_intake_prompt("SENTINEL-INTAKE-MISSION")
        seen: list[str] = []

        def _call(prompt: str, attempt: int) -> str:
            seen.append(prompt)
            return json.dumps(_VALID_INTAKE)

        run_intake("a completely different mission", _call, composed=composed)

        assert seen == [composed.text]
        assert "SENTINEL-INTAKE-MISSION" in seen[0]
        assert "a completely different mission" not in seen[0]
<<<END_PAIR_TI_TO>>>

<<<PAIR_TF_FROM>>>
        with pytest.raises(ReplanRejectedError, match="Cannot replan"):
            replan(fp1.model_dump(), fp2, tmp_path, any_task_completed=True)
<<<END_PAIR_TF_FROM>>>

<<<PAIR_TF_TO>>>
        with pytest.raises(ReplanRejectedError, match="Cannot replan"):
            replan(fp1.model_dump(), fp2, tmp_path, any_task_completed=True)


class TestPlanJobLlmAcceptsAComposedPrompt:
    """R-0256: one composition feeds the provider AND the trace manifest."""

    def test_composed_text_is_exactly_what_the_provider_sees(self):
        from packages.orchestration.flight_plan import compose_flight_plan_prompt

        composed = compose_flight_plan_prompt(
            {"goal": "SENTINEL-PLAN-GOAL"}, project_facts="pinned facts",
        )
        seen: list[str] = []

        def _call(prompt: str, attempt: int) -> str:
            seen.append(prompt)
            return _valid_plan_json(3)

        plan_job_llm(_fake_intake(), _call, composed=composed)

        assert seen == [composed.text]
        assert "SENTINEL-PLAN-GOAL" in seen[0]
        assert "Add a login page" not in seen[0]
<<<END_PAIR_TF_TO>>>

<<<PAIR_P_PLAN>>>
# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245
after PR #188 merged at the Open PR Gate. One-session self-drive, one delegated
worker per round. The next free finding ID lives in `.agent/live_review.md`
line 8 and is deliberately not duplicated here (R-0240's root cause).

## Goal
Prompt assembly stops being ad hoc. Every prompt composes from REGISTERED
SEGMENTS ordered by stability — system and conventions first, task and steering
last — every call records a segment manifest (name, rank, hash) into evidence,
and `remedy stats cache` shows the cache-read share per role from actuals.
Prompt CONTENT does not change; only its composition.

## Current Step
T001 and T002 are DONE and gated. T003's six migration sites are all migrated.
R38 is GATED; `LAST_REVIEWED_SHA` is 5ca4debd. R39 records that gate and takes
the first half of R-0256: `run_intake` and `plan_job_llm` accept a keyword-only
`composed`, one test each, both red-proofed. R-0256 stays OPEN until R40.
Open findings: R-0221, R-0239, R-0247, R-0256, R-0262.
No PR; one is created at CLOSURE.

## Next Steps
- R40 finishes R-0256: pass `composed=` at the three
  `apps/cli/commands/do_cmd.py` sites that already build one — intake,
  flight-plan (whose comment about the second composition goes stale and must
  be replaced) and replan. The new keyword goes on its OWN line: the suite
  counts `on_call=make_flight_plan_call_recorder(` over the WHOLE file
  (tests/orchestration/test_prompt_trace.py, `== 2`).
- Then T004, `remedy stats cache` over actuals: a per-role cache-read share
  from recorded call evidence, not estimates. Quote the flight-plan prompt's
  cacheable-prefix gain — it was the worst-ordered site.
- Then the integration gate (docs/agents/integration_gate.md), then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- R-0262 stays OPEN and out of scope: it needs the composition moved inside the
  `try` in `plan_job_llm` AND at the CLI sites, pinned by a raising composer.
<<<END_PAIR_P_PLAN>>>

GATES — run every one, record the REAL exit code in the handback

A transport
  `sha256sum .remedy-wt/f105-r39-1.block.md .agent/authored/f105-r39-1.md
  .agent/last_block.md` — all three EQUAL; two `cmp` runs, both silent.

B size
  `wc -l .agent/authored/f105-r39-1.md` against the cap of 400 (D5).

C pair shapes, MEASURED not assumed
  Slice every pair from the COMMITTED `.agent/authored/f105-r39-1.md` with a
  whole-line marker reader; never retype. Verify FIRST that every FROM occurs
  exactly 1x in its target before the write, and STOP if one does not. Then:
  PAIR_INTAKE, PAIR_FP and PAIR_FP2 are REWRITEs — FROM 0x, TO 1x after the
  write. PAIR_LR, PAIR_TI and PAIR_TF are CONTAINS-FROM — FROM 1x, TO 1x.
  PAIR_P_PLAN: `cmp` the applied `.agent/plan.md` against the slice, `wc -l`
  against the cap of 50.
  A declared shape that does not equal the measured shape is a STOP.

D added-line reconciliation, per commit
  For C2, C3 and C4 run `git show -U0 <commit> -- <path>`: every ADDED line
  appears in some TO for that file, every REMOVED line is a FROM. Report both
  stray counts per commit — all must be 0.

E marker leakage
  `^<<<` line count is 0 in EVERY written target — the seven paths named in
  "Change" minus the two block copies. Report the numbers, not the word.

F state-file contracts
  `python3 -m pytest tests/docs/ -q` and
  `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q`.
  `.agent/plan.md` keeps `## Goal` and a `Steps` substring;
  `.agent/live_review.md` keeps its `## Steps` heading.

G scoped suite, after C4
  `python3 -m pytest tests/orchestration/test_intake.py
  tests/orchestration/test_flight_plan.py -q`. Report the count: both files
  must be fully green, not only the two new tests.

H prompt CONTENT is unchanged
  BEFORE any edit of C3, and AGAIN after C4, run and record both digests:
  `python3 -c "import hashlib
  from packages.orchestration.intake import compose_intake_prompt as ci
  from packages.orchestration.flight_plan import compose_flight_plan_prompt as cf
  print(hashlib.sha256(ci('a fixed mission').text.encode()).hexdigest())
  print(hashlib.sha256(cf({'goal':'fixed'}, project_facts='pinned').text.encode()).hexdigest())"`
  Both must be EQUAL before and after. A difference is a STOP.

I red-proofs, DISPOSABLE WORKTREE ONLY
  `git worktree add .remedy-wt/r39-red HEAD` after C4. Inside that worktree
  ONLY, one at a time, revert the ternary to the unconditional builder call and
  run the matching test file. Each mutation must make
  `test_composed_text_is_exactly_what_the_provider_sees` FAIL — report the
  actual assertion line, not the word "red". The branch is reachable: that test
  passes `composed=`. Then `git worktree remove --force .remedy-wt/r39-red` and
  `git worktree prune`. The primary checkout is never mutated (G5).

J canary and hygiene
  `python3 -m pytest tests/cli/test_golden_path.py -q`.
  `git status --porcelain` empty at handback; `git worktree list` shows the
  primary ALONE; per-commit insertions each under 500 via `git show --numstat`.
  `git diff --name-only 5ca4debd..HEAD` lists ONLY the seven paths named in
  "Change" — report the list. `apps/cli/commands/do_cmd.py` must NOT appear.

Handback: completion report + rewrite `.agent/handoff.md` (changed-files table,
item-status table for C1a..C5, the gate table with real exit codes, the
transport and pair proofs, the two H digests, the red-proof failure lines,
open-findings count, next action — "gate R39, then run R40"). Then `git push`.
No PR — one is created at CLOSURE.
──────────────────────────────────────────────────────────────
