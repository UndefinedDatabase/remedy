── STEP R31 — F105 ────────────────────────────────────────────
Goal:        Name the mission-plan evidence sink and fix R-0257. `plan_mission`
             owns the traces list and appends them to the mission's evidence
             dir, `remedy mission plan` labels the provider, and composition
             moves back inside the try/except it was lifted out of at R30.
Bundle:      C1 save this block · C2 the R30 gate record and R-0257 · C3 the
             R-0257 fix · C4 the sink and the CLI · C5 the tests · C6 plan and
             handback.
Change:      `.agent/authored/f105-r31-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `packages/orchestration/mission_compiler.py`,
             `apps/cli/commands/mission_cmd.py`,
             `tests/orchestration/test_mission_compiler.py`, `.agent/plan.md`,
             `.agent/handoff.md`. Nothing else.
Constraints: Prompt CONTENT does not change — only composition and evidence.
             Do NOT touch `flight_plan.py`, `intake.py` or `do_cmd.py`: R-0256
             covers those and is its own round. Do not reflow any line you were
             not given a pair for. `git status --porcelain` empty at handback.
             Destructive checks only inside a disposable `git worktree`.
Done when:   every gate below is run and its REAL exit code recorded.

C1 — save this block verbatim, TWO commits
  C1a `cp /home/decodeux/Repos/remedy/.remedy-wt/f105-r31-1.block.md`
      `.agent/authored/f105-r31-1.md`. Commit it ALONE.
  C1b `cp` the same bytes to `.agent/last_block.md`. Commit separately.
  `sha256sum` all three plus `cmp`; digest in the handback.

C2 — the R30 gate record and the new finding (own commit, FIRST)
  Findings persist before any fix (§4.4). Apply PAIR_A (APPEND) and PAIR_B
  (REWRITE, the header's next-free-ID line) to `.agent/live_review.md` in this
  one commit. For PAIR_A prove FROM 1x plus the TO-only ADDED-LINE count over
  this commit's diff and the stray count; for PAIR_B prove FROM 0x after,
  TO 1x. Do NOT use a whole-file count for PAIR_A.

<<<PAIR_A_FROM>>>
  `LAST_REVIEWED_SHA` advances 55550615 -> 0c8932e3.
<<<END_PAIR_A_FROM>>>

<<<PAIR_A_TO>>>
  `LAST_REVIEWED_SHA` advances 55550615 -> 0c8932e3.
- R30: SPLIT round — `compile_mission_plan` composes ONCE and hands that one
  ComposedPrompt to a `mission_plan` recorder, plus the R-0246 docstring fix.
  No sink, no CLI: those are R31.
- Reviewer gate on R30 (2026-08-10): PASS, with R-0257 registered against the
  reviewer's own authored text. Range `0c8932e3..0ba30611` = six commits, read
  as a real diff: seven paths, exactly the ones the block named; insertions per
  commit 399, 349, 27, 64, 64, 57 — each under 500.
  Transport re-proved disk to disk against the reviewer's surviving original:
  `.remedy-wt/f105-r30-1.block.md`, `.agent/authored/f105-r30-1.md` and
  `.agent/last_block.md` all three
  `691c21a6b9717c160379291f63e6f45318e412f0e2714e590afb8ec7f8e14afa`, both
  `cmp` runs silent, 399 lines against DECISION F105 D5's cap of 400. This is
  the primary proof shape, not the §4.9 digest fallback: in-session the
  reviewer's original never left the disk.
  All seven pairs re-sliced from the COMMITTED authored file by the reviewer's
  own whole-line marker reader; declared shape equals measured shape for every
  one. PAIR_A FROM 1x with 27 TO-only lines against 27 ADDED and 0 removed;
  PAIR_G FROM 1x with 63 TO-only against 64 ADDED — the one extra is the
  `    compose_mission_prompt,` import line C4 explicitly ordered, so strays 0;
  PAIR_D FROM 1x with 42 TO-only. PAIR_B, C, E and F all FROM 0x after and
  TO 1x. Across the whole C3 commit (64 added, 3 removed) no ADDED line comes
  from outside a TO and no REMOVED line from outside a FROM. PAIR_H is
  byte-equal to `.agent/plan.md` at 45 lines against the cap of 50.
  Gates re-run by THIS reviewer with real exit codes: `grep -c -E '^<<<'` = 0 in
  all four targets; `test_mission_compiler.py` + `test_mission_prompt_golden.py`
  `121 passed in 0.49s`; the three caller suites `78 passed in 1.42s`;
  `tests/docs/` `294 passed in 0.30s`; the dashboard contract `70 passed in
  4.09s`; the canary `42 passed in 19.47s`; `git status --porcelain` empty and
  `git worktree list` the primary alone at this verdict.
  Red-proof M1 reproduced by the reviewer in a disposable worktree at ccb128f0
  with `PYTHONDONTWRITEBYTECODE=1`: deleting `composed_prompt=composed,` from
  `make_mission_plan_call_recorder` turns exactly the two named tests RED at
  `2 failed, 114 passed in 0.61s`. Reverted, worktree removed and pruned.
- R-0257 (Medium, F105 R30, reviewer-authored defect): the R30 block lifted
  composition OUT of the try/except that turns any failure into the
  deterministic fallback. `compile_mission_plan` used to build its prompt as an
  ARGUMENT to `run_structured_call` inside `try:`, so a raising composer became
  `_fallback(goal, hint=f"provider error: {exc}")`; PAIR_F put
  `composed = compose_mission_prompt(...)` above the `try:`, so it now escapes
  the function. Proved by the reviewer in a disposable worktree with the
  composer monkeypatched to raise: at 39da9b61^ the call returns
  `source="deterministic"` and `error_hint="provider error: composition blew
  up"`; at 39da9b61 the `RuntimeError` propagates out. No test covers it, which
  is exactly why every gate was green — the module docstring's promise that
  "any provider failure, or an unparseable answer" yields the fallback "rather
  than an exception" is what regressed, and `remedy mission plan` would
  traceback where it used to degrade. The realistic trigger is a filesystem
  failure inside `repo_facts_block()`. The R30 worker DECLARED this rather than
  repairing it, which was right: the defect is the reviewer's, and a worker that
  silently fixes authored text hides the mistake instead of pricing it. Fix:
  compose inside the try, pinned by a test that makes the composer raise. OPEN.
  `LAST_REVIEWED_SHA` advances 0c8932e3 -> 0ba30611.
<<<END_PAIR_A_TO>>>

<<<PAIR_B_FROM>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0257.
<<<END_PAIR_B_FROM>>>

<<<PAIR_B_TO>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0258.
<<<END_PAIR_B_TO>>>

C3 — the R-0257 fix (own commit)
  Apply PAIR_C to `packages/orchestration/mission_compiler.py`. REWRITE: prove
  FROM 0x after and TO 1x. After the commit, append the line
  `  Landed: R-0257 — composition moved back inside the try at C3 of R31.`
  directly under R-0257's `OPEN.` line in `.agent/live_review.md`, in this same
  commit. That is the ONLY text you author into that file; `Done:` is
  reviewer-only (§4.4).

<<<PAIR_C_FROM>>>
    composed = compose_mission_prompt(goal, project_facts=project_facts,
                                      max_milestones=max_milestones)
    if traces is not None:
        # The sink wins over a caller-supplied ``on_call``: only code INSIDE
        # this function holds the ComposedPrompt that was actually sent.
        on_call = make_mission_plan_call_recorder(
            traces, composed, provider=provider, provider_kind=provider_kind)
    try:
        outcome: StructuredOutcome = run_structured_call(
<<<END_PAIR_C_FROM>>>

<<<PAIR_C_TO>>>
    try:
        # Composition sits INSIDE the try because it CAN fail —
        # ``repo_facts_block`` reads the filesystem — and this function's
        # contract is that a failure degrades to the deterministic fallback
        # rather than raising into the caller (R-0257).
        composed = compose_mission_prompt(goal, project_facts=project_facts,
                                          max_milestones=max_milestones)
        if traces is not None:
            # The sink wins over a caller-supplied ``on_call``: only code
            # INSIDE this function holds the ComposedPrompt actually sent.
            on_call = make_mission_plan_call_recorder(
                traces, composed, provider=provider,
                provider_kind=provider_kind)
        outcome: StructuredOutcome = run_structured_call(
<<<END_PAIR_C_TO>>>

C4 — the sink and the CLI (own commit)
  PAIR_D and PAIR_E against `packages/orchestration/mission_compiler.py`,
  PAIR_F against `apps/cli/commands/mission_cmd.py`. All three REWRITE: prove
  FROM 0x after and TO 1x, each scoped to its own file.

<<<PAIR_D_FROM>>>
    root: Path | None = None,
    on_call: Callable[[int, str, bool, str], None] | None = None,
    max_milestones: int | None = None,
) -> MissionPlanOutcome:
<<<END_PAIR_D_FROM>>>

<<<PAIR_D_TO>>>
    root: Path | None = None,
    provider: str = "",
    provider_kind: str = "",
    max_milestones: int | None = None,
) -> MissionPlanOutcome:
<<<END_PAIR_D_TO>>>

<<<PAIR_E_FROM>>>
    result = compile_mission_plan(mission, call_fn, on_call=on_call,
                                  max_milestones=max_milestones)
    evidence_dir = mission_evidence_dir(project_id, mission.id, root)
<<<END_PAIR_E_FROM>>>

<<<PAIR_E_TO>>>
    prompt_traces: list[Any] = []
    result = compile_mission_plan(mission, call_fn, traces=prompt_traces,
                                  provider=provider,
                                  provider_kind=provider_kind,
                                  max_milestones=max_milestones)
    evidence_dir = mission_evidence_dir(project_id, mission.id, root)
    if prompt_traces:
        # APPEND, never write: the trace file is per MISSION and a recompile is
        # a SECOND command against the same mission, so a write would destroy
        # the first compile's evidence. Same reasoning as the F105 R28 replan.
        from packages.orchestration.prompt_trace import append_trace_jsonl
        append_trace_jsonl(prompt_traces, evidence_dir / "prompt_trace.jsonl")
<<<END_PAIR_E_TO>>>

<<<PAIR_F_FROM>>>
        outcome = plan_mission(project_id, mission.id, call_fn)
<<<END_PAIR_F_FROM>>>

<<<PAIR_F_TO>>>
        # `make_structured_call_fn` is Ollama-backed, so the provider is named
        # here exactly as the flight-plan site names it in `do_cmd.py`. Under
        # `--no-llm` there is no call and therefore no trace to carry a label.
        outcome = plan_mission(project_id, mission.id, call_fn,
                               provider="ollama", provider_kind="ollama")
<<<END_PAIR_F_TO>>>

C5 — the tests (own commit)
  Apply PAIR_G to `tests/orchestration/test_mission_compiler.py`. APPEND-shaped:
  the TO opens with the FROM verbatim, which is the current LAST test in the
  file. Prove FROM 1x plus the TO-only ADDED-LINE count over this commit's diff
  and the stray count. Also add `from packages.orchestration import
  mission_compiler` to the file's import block, on its own line, immediately
  ABOVE the existing `from packages.orchestration.data_paths import jobs_dir`
  line, and change nothing else in that block.

<<<PAIR_G_FROM>>>
    def test_no_provider_records_no_call(self, planned_mission):
        """The deterministic fallback contacts nobody, so it traces nobody."""
        mission, _call_fn = planned_mission
        traces: list = []

        result = compile_mission_plan(mission.goal, None, traces=traces)

        assert result.source == "deterministic"
        assert traces == []
<<<END_PAIR_G_FROM>>>

<<<PAIR_G_TO>>>
    def test_no_provider_records_no_call(self, planned_mission):
        """The deterministic fallback contacts nobody, so it traces nobody."""
        mission, _call_fn = planned_mission
        traces: list = []

        result = compile_mission_plan(mission.goal, None, traces=traces)

        assert result.source == "deterministic"
        assert traces == []

    def test_a_failing_composer_still_yields_the_fallback(
            self, planned_mission, monkeypatch):
        """R-0257: composition failure degrades, it does not reach the CLI."""
        mission, call_fn = planned_mission

        def boom(*_a, **_k):
            raise RuntimeError("composition blew up")

        monkeypatch.setattr(mission_compiler, "compose_mission_prompt", boom)

        result = compile_mission_plan(mission.goal, call_fn)

        assert result.source == "deterministic"
        assert "composition blew up" in result.error_hint


class TestMissionPlanEvidenceSink:
    """`plan_mission` owns the evidence dir, so it owns the trace file."""

    def test_planning_writes_the_trace_into_the_evidence_dir(
            self, planned_mission):
        mission, call_fn = planned_mission

        outcome = plan_mission("proj", mission.id, call_fn,
                               provider="ollama", provider_kind="ollama")

        rows = [json.loads(line) for line
                in (outcome.evidence_dir / "prompt_trace.jsonl")
                .read_text().splitlines() if line]
        assert len(rows) == 1
        assert rows[0]["role"] == "mission_plan"
        assert rows[0]["provider"] == "ollama"
        assert rows[0]["segment_manifest"]

    def test_a_recompile_appends_rather_than_truncating(self, planned_mission):
        """A second `remedy mission plan` must not erase the first's evidence."""
        mission, call_fn = planned_mission

        plan_mission("proj", mission.id, call_fn)
        outcome = plan_mission("proj", mission.id, call_fn)

        rows = [line for line
                in (outcome.evidence_dir / "prompt_trace.jsonl")
                .read_text().splitlines() if line]
        assert len(rows) == 2

    def test_no_provider_leaves_no_trace_file(self, planned_mission):
        """Nothing was sent, so there is no evidence file pretending it was."""
        mission, _call_fn = planned_mission

        outcome = plan_mission("proj", mission.id, None)

        assert not (outcome.evidence_dir / "prompt_trace.jsonl").exists()

    def test_the_cli_names_the_provider_it_planned_with(self):
        """A source guard, because an unwired CLI leaves every gate green.

        The tests above drive `plan_mission` directly, so they stay green even
        if `remedy mission plan` stops passing the provider. This pins the one
        line they cannot reach. Formatting-sensitive by nature — the F105 R28
        `on_call=` guard precedent, and the same trade-off.
        """
        source = (Path(__file__).resolve().parents[2]
                  / "apps" / "cli" / "commands" / "mission_cmd.py").read_text()
        assert source.count('provider_kind="ollama"') == 1
<<<END_PAIR_G_TO>>>

C6 — plan and handback (own commit)
  Apply PAIR_H to `.agent/plan.md` as a FULL replacement, then rewrite
  `.agent/handoff.md` per AGENTS.md: feature and round, branch, this round's
  commit SHAs, a changed-files table with one row per path, the item-status
  table over C1a/C1b/C2/C3/C4/C5/C6, the gate table with REAL exit codes and
  REAL output, the open-findings count with IDs, and the next expected action.
  Under 60 lines, or carry a DECISION D15 "Deviations, declared" line naming
  the real count and the mandated content that caused it. Then push. No PR.

<<<PAIR_H_PLAN>>>
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
Call evidence now reaches three prompts: both `do_cmd` flight-plan sites — the
first through `write_trace_jsonl`, the replan through `append_trace_jsonl` — and
`remedy mission plan`, whose manifest is composed ONCE inside
`compile_mission_plan` and appended to the mission's evidence dir.
R30 is GATED; `LAST_REVIEWED_SHA` is 0ba30611. R31 is in review: the sink, the
CLI wiring and the R-0257 fix.
Open findings: R-0221, R-0239, R-0247, R-0256, plus R-0257 landed and awaiting
the reviewer's `Done:`. R-0246 landed at R30, same state.
No PR; one is created at CLOSURE.

## Next Steps
- The orchestrator prompt — `mission_cmd.py:362` into `run_mission`, then
  `gauntlet_runner.py:505`. Neither has an evidence sink today; the mission-plan
  rounds are the shape to copy.
- R-0256 (compose once, not twice) needs a signature change on `plan_job_llm`
  and `run_intake`, so it is its own round.
- Then T004, `remedy stats cache` over actuals; then the integration gate
  (docs/agents/integration_gate.md); then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- The reviewer prompt was the worst-ordered of the six sites and 1824 of 2048
  measured renders reorder, so T004's before/after number should quote its
  cacheable-prefix gain specifically.
<<<END_PAIR_H_PLAN>>>

GATES — run every one, record the REAL exit code and the REAL output
  A transport: `sha256sum` on the reviewer original in `.remedy-wt/`,
    `.agent/authored/f105-r31-1.md` and `.agent/last_block.md`; `cmp` all three.
  B size: `wc -l .agent/authored/f105-r31-1.md`. Cap 400 (DECISION F105 D5).
  C application, per pair, scoped to the named file: PAIR_A and PAIR_G are
    APPEND — FROM exactly 1x, plus the TO-only ADDED-LINE count from
    `git show --numstat <commit> -- <path>` and the stray count. PAIR_B, C, D,
    E and F are REWRITE — FROM 0x after and TO 1x. PAIR_H: `cmp` the applied
    `.agent/plan.md` against the sliced text; `wc -l` must be under 50. The
    `Landed: R-0257` line and the test-import line are the only two additions
    outside a TO in this whole round; name them both.
  D marker leakage, LINE-anchored: `grep -c -E '^<<<'` in `.agent/live_review.md`,
    `packages/orchestration/mission_compiler.py`, `apps/cli/commands/mission_cmd.py`,
    `tests/orchestration/test_mission_compiler.py` and `.agent/plan.md` — 0 each.
  E touched suite: `python3 -m pytest tests/orchestration/test_mission_compiler.py
    tests/orchestration/test_mission_prompt_golden.py -q`.
  F callers: `python3 -m pytest tests/orchestration/test_mission_e2e.py
    tests/orchestration/test_overnight_mission.py
    tests/orchestration/test_feature_mission_adapter.py -q`, then
    `python3 -m pytest tests/cli/ -q`.
  G red-proof M1, in a disposable `git worktree` at the C5 commit, with
    `PYTHONDONTWRITEBYTECODE=1` (the F105 R28 lesson: a same-length revert in
    the same clock second can be served from a stale `.pyc`): in `plan_mission`,
    change `append_trace_jsonl` to `write_trace_jsonl` in BOTH its import line
    and its call. `test_a_recompile_appends_rather_than_truncating` must go RED.
    Report the exact failed/passed counts.
  H red-proof M2, same worktree, M1 REVERTED first and `git diff --stat` shown
    to prove the revert: delete `traces=prompt_traces,` from `plan_mission`'s
    `compile_mission_plan` call. `test_planning_writes_the_trace_into_the_evidence_dir`
    and `test_a_recompile_appends_rather_than_truncating` must go RED. Report
    the exact counts, then remove and prune the worktree.
  I state-file contract tests: `python3 -m pytest tests/docs/ -q` and
    `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q`.
  J canary: `python3 -m pytest tests/cli/test_golden_path.py -q`.
  K hygiene: `git status --porcelain` empty; `git worktree list` the primary
    alone; `git log --numstat 0ba30611..HEAD` with the `+` column per commit,
    each under 500.
Handback:    completion report + the rewritten `.agent/handoff.md` described in
             C6. Then push. Do NOT create a PR.
──────────────────────────────────────────────────────────────
