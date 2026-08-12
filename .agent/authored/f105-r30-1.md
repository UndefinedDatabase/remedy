── STEP R30 — F105 ────────────────────────────────────────────
Goal:        `compile_mission_plan` composes its prompt ONCE, and that one
             composition feeds both the bytes the provider gets and the segment
             manifest a trace records. The evidence SINK and the CLI wiring are
             R31; this round pins the manifest where the composition happens.
Bundle:      C1 save this block · C2 the R29 gate record · C3 the compiler
             change and the R-0246 fix · C4 the tests · C5 plan and handback.
Change:      `.agent/authored/f105-r30-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `packages/orchestration/mission_compiler.py`,
             `tests/orchestration/test_mission_compiler.py`, `.agent/plan.md`,
             `.agent/handoff.md`. Nothing else.
Constraints: Prompt CONTENT does not change — only composition and evidence.
             Do NOT touch `apps/`, `flight_plan.py`, `intake.py`, `do_cmd.py`
             or `plan_mission`: the sink is R31. Do not reflow any line you were
             not given a pair for. `git status --porcelain` empty at handback.
             Destructive checks only inside a disposable `git worktree`.
Done when:   every gate below is run and its REAL exit code recorded.

C1 — save this block verbatim, TWO commits
  C1a `cp /home/decodeux/Repos/remedy/.remedy-wt/f105-r30-1.block.md`
      `.agent/authored/f105-r30-1.md`. Commit it ALONE.
  C1b `cp` the same bytes to `.agent/last_block.md`. Commit separately.
  `sha256sum` all three plus `cmp`; digest in the handback. The reviewer's
  original stays on disk this session, so the transport proof is a real
  disk-to-disk `cmp`, not a recomputation (self_drive_protocol.md Phase 2.1).

C2 — the R29 gate record (own commit)
  Apply PAIR_A to `.agent/live_review.md`. It is APPEND-shaped (the TO contains
  the FROM verbatim as its prefix): prove FROM exactly 1x, plus the TO-only
  ADDED-LINE count from this commit's diff and the stray count. Do NOT use a
  whole-file count. The header's `Next free ID` line is NOT touched: this round
  registers nothing new, so R-0257 stays free.

<<<PAIR_A_FROM>>>
  `LAST_REVIEWED_SHA` advances 73259d7a -> 55550615.
<<<END_PAIR_A_FROM>>>

<<<PAIR_A_TO>>>
  `LAST_REVIEWED_SHA` advances 73259d7a -> 55550615.
- R29: session-close round — record the R28 gate, sync the plan, write the
  session-ending handoff. State files only.
- Reviewer gate on R29 (2026-08-10): PASS. Range `55550615..HEAD` = five commits
  (9e497810, aa056f36, 0b431989, 9d7511e5, 0c8932e3) read as a real diff: five
  paths, every one under `.agent/`; insertions 165, 109, 48, 49, 9 — each under
  500. C4 (0c8932e3) is a declared deviation, not in the block: gate rows G and H
  can only carry real post-C3 numbers once C3 exists (the R28 C5 precedent), and
  the handoff declares it. Transport re-proved disk to disk —
  `.agent/authored/f105-r29-1.md` and `.agent/last_block.md` both recompute to
  `fdf4d7f6f05273c26b055f436675144954f241330b26a7d6f2414c2a5d04c179`, `cmp`
  silent, 165 lines each against DECISION F105 D5's cap of 400. Both pairs
  re-sliced from the COMMITTED authored file by the reviewer's own whole-line
  marker reader: PAIR_A is APPEND-shaped as declared — the TO's first line IS
  the FROM — at FROM 1x, and 0b431989 ADDS exactly 48 lines against 48 TO-only
  lines, in order, 0 removals and 0 strays; PAIR_B is byte-equal to
  `.agent/plan.md` at 43 lines against the cap of 50.
  Gates re-run by THIS reviewer, real exit codes: `grep -c -E '^<<<'` = 0 in
  `.agent/live_review.md` and `.agent/plan.md`; `tests/docs/` `294 passed in
  0.27s`; dashboard contract `70 passed in 4.16s`; canary `42 passed in 19.52s`;
  `git status --porcelain` empty; `git worktree list` the primary alone. Open
  findings recounted from the file rather than from the handoff: R-0221, R-0239,
  R-0246, R-0247, R-0256 — five, as declared. No mutation red-proof: the diff
  names nothing executable, so there is no branch to mutate (D10, D8 item 5).
  `remedy plan status` and `remedy plan next` were NOT run — the command sits
  outside this session's command allowlist and every attempt was denied;
  `docs/roadmap/STATUS.md` was read directly and carries exactly one `[~]`, F105.
  `LAST_REVIEWED_SHA` advances 55550615 -> 0c8932e3.
<<<END_PAIR_A_TO>>>

C3 — compose once and record the manifest (own commit)
  Five pairs, all against `packages/orchestration/mission_compiler.py`. PAIR_D
  is APPEND-shaped — prove FROM 1x plus the TO-only ADDED-LINE count over this
  commit's diff and the stray count. PAIR_B, C, E and F are REWRITE — prove
  FROM 0x after and TO 1x, scoped to that file.

  PAIR_B — the import. REWRITE.

<<<PAIR_B_FROM>>>
)
from packages.orchestration.schemas.models import FLIGHT_PLAN_SCHEMA_V, FlightPlan
<<<END_PAIR_B_FROM>>>

<<<PAIR_B_TO>>>
)
from packages.orchestration.prompt_trace import build_trace_entry
from packages.orchestration.schemas.models import FLIGHT_PLAN_SCHEMA_V, FlightPlan
<<<END_PAIR_B_TO>>>

  PAIR_C — the R-0246 fix, `build_mission_prompt`'s docstring. REWRITE.

<<<PAIR_C_FROM>>>
    ``max_milestones`` (R-0197) lowers the milestone ceiling the prompt states.
    ``None`` reproduces today's prompt byte for byte.
    """
<<<END_PAIR_C_FROM>>>

<<<PAIR_C_TO>>>
    ``max_milestones`` (R-0197) lowers the milestone ceiling the prompt states.
    ``None`` reproduces the pre-R-0197 milestone CEILING — not the pre-migration
    byte SEQUENCE. F105 T003 reordered these segments while leaving their bytes
    unchanged, so the composed order differs from the old template at every
    value of ``max_milestones``, ``None`` included (R-0246).
    """
<<<END_PAIR_C_TO>>>

  PAIR_D — the recorder, directly after `compose_mission_prompt`'s `return`.
  APPEND-shaped: the TO opens with the FROM verbatim.

<<<PAIR_D_FROM>>>
    return compose_prompt_segments(registry.registered_segments())
<<<END_PAIR_D_FROM>>>

<<<PAIR_D_TO>>>
    return compose_prompt_segments(registry.registered_segments())


# The recorder lives beside the composer, in this module, so the manifest and
# the prompt it describes cannot drift apart — the same reason
# `make_flight_plan_call_recorder` sits in `flight_plan.py` and
# `make_intake_call_recorder` in `intake.py` (F105 T003 site 2).
def make_mission_plan_call_recorder(
    traces: list[Any],
    composed: ComposedPrompt,
    *,
    provider: str = "",
    provider_kind: str = "",
) -> Callable[[int, str, bool, str], None]:
    """Build the ``on_call`` recorder ``compile_mission_plan`` wires.

    Every provider invocation appends one prompt trace entry to ``traces``,
    carrying ``composed``'s segment manifest so call evidence records which
    named segments produced the prompt.

    The role is ``mission_plan``, deliberately NOT ``mission``: the mission
    DOSSIER compression in ``mission_dossier.py`` is a different prompt against
    the same mission, and one spelling per concept is what keeps a per-role
    cache report from summing two prompts into one row.
    """
    def _record(
        attempt: int, schema_v: str, is_parse_retry: bool, effective_prompt: str,
    ) -> None:
        kind = "mission-plan-retry" if is_parse_retry else "mission-plan"
        traces.append(build_trace_entry(
            prompt_text=effective_prompt,
            role="mission_plan",
            provider=provider,
            provider_kind=provider_kind,
            prompt_kind=kind,
            schema_v=schema_v,
            phase=kind,
            transport_attempt=attempt,
            is_transport_retry=False,
            composed_prompt=composed,
        ))

    return _record
<<<END_PAIR_D_TO>>>

  PAIR_E — `compile_mission_plan`'s signature. REWRITE, purely ADDITIVE:
  ``on_call`` stays. Nothing passes it today, but removing it would ripple into
  `plan_mission`, which is R31's change set, and this round stops at that line.

<<<PAIR_E_FROM>>>
    on_call: Callable[[int, str, bool, str], None] | None = None,
    project_facts: str = "",
    max_milestones: int | None = None,
) -> MissionCompileResult:
<<<END_PAIR_E_FROM>>>

<<<PAIR_E_TO>>>
    on_call: Callable[[int, str, bool, str], None] | None = None,
    traces: list[Any] | None = None,
    provider: str = "",
    provider_kind: str = "",
    project_facts: str = "",
    max_milestones: int | None = None,
) -> MissionCompileResult:
<<<END_PAIR_E_TO>>>

  PAIR_F — the call itself. REWRITE.

<<<PAIR_F_FROM>>>
    try:
        outcome: StructuredOutcome = run_structured_call(
            MissionPlanDraft if max_milestones is None
            else _capped_draft_model(resolve_milestone_cap(max_milestones)),
            build_mission_prompt(goal, project_facts=project_facts,
                                 max_milestones=max_milestones),
            call_fn,
            on_call=on_call,
            allow_parse_retry=True,
        )
<<<END_PAIR_F_FROM>>>

<<<PAIR_F_TO>>>
    # Composed ONCE. The same ComposedPrompt supplies the bytes that go to the
    # provider and the manifest the trace records, so an audit row can never
    # describe a twin composition the provider never saw. That failure mode is
    # real and open elsewhere — R-0256, the flight-plan and intake sites, where
    # the caller composes a second time because it has to build the recorder
    # before the builder runs. It is not reproduced here.
    composed = compose_mission_prompt(goal, project_facts=project_facts,
                                      max_milestones=max_milestones)
    if traces is not None:
        # The sink wins over a caller-supplied ``on_call``: only code INSIDE
        # this function holds the ComposedPrompt that was actually sent.
        on_call = make_mission_plan_call_recorder(
            traces, composed, provider=provider, provider_kind=provider_kind)
    try:
        outcome: StructuredOutcome = run_structured_call(
            MissionPlanDraft if max_milestones is None
            else _capped_draft_model(resolve_milestone_cap(max_milestones)),
            composed.text,
            call_fn,
            on_call=on_call,
            allow_parse_retry=True,
        )
<<<END_PAIR_F_TO>>>

C4 — the tests (own commit)
  Apply PAIR_G to `tests/orchestration/test_mission_compiler.py`. APPEND-shaped:
  the TO opens with the FROM verbatim, which is the current LAST function in the
  file. Prove FROM 1x plus the TO-only ADDED-LINE count over this commit's diff.
  Also add `compose_mission_prompt` to the existing
  `from packages.orchestration.mission_compiler import (...)` block, on its own
  line, and change nothing else in that block.

<<<PAIR_G_FROM>>>
def test_the_cap_never_loosens_the_dag_discipline() -> None:
    """A cycle is still a cycle, capped or not."""
    body = draft_body(milestone("M001", depends_on=["M002"]),
                      milestone("M002", depends_on=["M001"]))
    result = compile_mission_plan("ship it", replaying(body), max_milestones=2)
    assert result.source == "deterministic"
<<<END_PAIR_G_FROM>>>

<<<PAIR_G_TO>>>
def test_the_cap_never_loosens_the_dag_discipline() -> None:
    """A cycle is still a cycle, capped or not."""
    body = draft_body(milestone("M001", depends_on=["M002"]),
                      milestone("M002", depends_on=["M001"]))
    result = compile_mission_plan("ship it", replaying(body), max_milestones=2)
    assert result.source == "deterministic"


# ---------------------------------------------------------------------------
# F105 T003 — the mission-plan prompt's segment manifest, composed once
# ---------------------------------------------------------------------------


class TestMissionPlanCallEvidence:
    """One composition feeds both the provider bytes and the trace manifest."""

    def test_the_manifest_describes_the_bytes_that_were_sent(
            self, planned_mission):
        """Compose-once, proved from the prompt the provider actually got."""
        mission, replay = planned_mission
        traces: list = []
        sent: list[str] = []

        def call_fn(prompt: str, attempt: int) -> str:
            sent.append(prompt)
            return replay(prompt, attempt)

        compile_mission_plan(mission.goal, call_fn, traces=traces,
                             provider="ollama", provider_kind="ollama",
                             project_facts="FACTS")

        composed = compose_mission_prompt(mission.goal, project_facts="FACTS")
        assert len(traces) == 1
        entry = traces[0]
        assert entry.role == "mission_plan"
        assert entry.provider == "ollama"
        assert entry.prompt_kind == "mission-plan"
        # The manifest covers the composed text, and that text is a PREFIX of
        # what was sent. Any remainder is the schema tail `run_structured_call`
        # appends outside every builder, which F105 does not register
        # (DECISION F105 D3) — recording both numbers keeps that gap visible.
        assert entry.segment_manifest_chars == len(composed.text)
        assert sent[0].startswith(composed.text)
        assert [row["name"] for row in entry.segment_manifest] == [
            "mission_system", "mission_rules", "mission_repo_facts",
            "mission_goal", "mission_schema_directive"]

    def test_a_manifest_row_carries_its_rank_and_hash(self, planned_mission):
        """A name alone would not let an auditor re-derive the ordering."""
        mission, call_fn = planned_mission
        traces: list = []

        compile_mission_plan(mission.goal, call_fn, traces=traces,
                             project_facts="FACTS")

        row = traces[0].segment_manifest[0]
        assert row["name"] == "mission_system"
        assert row["rank"] == 0
        assert len(row["sha256"]) == 64

    def test_no_provider_records_no_call(self, planned_mission):
        """The deterministic fallback contacts nobody, so it traces nobody."""
        mission, _call_fn = planned_mission
        traces: list = []

        result = compile_mission_plan(mission.goal, None, traces=traces)

        assert result.source == "deterministic"
        assert traces == []
<<<END_PAIR_G_TO>>>

C5 — plan and handback (own commit)
  Apply PAIR_H to `.agent/plan.md` as a FULL replacement, then rewrite
  `.agent/handoff.md` per AGENTS.md: feature and round, branch, this round's
  commit SHAs, a changed-files table with one row per path, the item-status
  table over C1a/C1b/C2/C3/C4/C5, the gate table with REAL exit codes and REAL
  output, the open-findings count with IDs, and the next expected action.
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
Call evidence reaches both `do_cmd` flight-plan sites — the first through
`write_trace_jsonl`, the replan through `append_trace_jsonl`.
R29 is GATED; `LAST_REVIEWED_SHA` is 0c8932e3. R30 is in review: it makes
`compile_mission_plan` compose ONCE and hands that one composition to a
`mission_plan` recorder, so the mission manifest exists at the layer that owns
the bytes. R30 names no sink and touches no CLI — that is R31.
Open findings: R-0221, R-0239, R-0247, R-0256. R-0246 lands with R30.
No PR; one is created at CLOSURE.

## Next Steps
- R31: name the mission-plan sink. `plan_mission` owns the evidence dir, so it
  owns the traces list and appends to `<evidence_dir>/prompt_trace.jsonl`
  (APPEND, because a recompile is a second command against the same mission);
  `mission_cmd.py:187` passes the provider label; evidence tests plus the CLI
  wiring guard.
- Then the orchestrator prompt — `mission_cmd.py:362` into `run_mission`, then
  `gauntlet_runner.py:505`. Neither has a sink today either.
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
    `.agent/authored/f105-r30-1.md` and `.agent/last_block.md`; `cmp` all three.
  B size: `wc -l .agent/authored/f105-r30-1.md`. Cap 400 (DECISION F105 D5).
  C application, per pair, scoped to the named file: PAIR_A, PAIR_D and PAIR_G
    are APPEND — FROM exactly 1x, plus the TO-only ADDED-LINE count from
    `git show --numstat <commit> -- <path>` and the stray count. PAIR_B, C, E
    and F are REWRITE — FROM 0x after and TO 1x. PAIR_H: `cmp` the applied
    `.agent/plan.md` against the sliced text; `wc -l` must be under 50.
  D marker leakage, LINE-anchored: `grep -c -E '^<<<'` in `.agent/live_review.md`,
    `packages/orchestration/mission_compiler.py`,
    `tests/orchestration/test_mission_compiler.py` and `.agent/plan.md` — 0 each.
    The count is over marker LINES on purpose (D8 item 2).
  E touched suite: `python3 -m pytest tests/orchestration/test_mission_compiler.py
    tests/orchestration/test_mission_prompt_golden.py -q`.
  F callers of the changed function: `python3 -m pytest
    tests/orchestration/test_mission_e2e.py
    tests/orchestration/test_overnight_mission.py
    tests/orchestration/test_feature_mission_adapter.py -q`.
  G red-proof M1, in a disposable `git worktree` at the C4 commit, with
    `PYTHONDONTWRITEBYTECODE=1` (the F105 R28 lesson: a same-length revert in
    the same clock second can be served from a stale `.pyc`): delete the line
    `            composed_prompt=composed,` from `make_mission_plan_call_recorder`.
    `test_the_manifest_describes_the_bytes_that_were_sent` and
    `test_a_manifest_row_carries_its_rank_and_hash` must go RED. Report the
    exact failed/passed counts, then remove and prune the worktree.
  H state-file contract tests: `python3 -m pytest tests/docs/ -q` and
    `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q`.
  I canary: `python3 -m pytest tests/cli/test_golden_path.py -q`.
  J hygiene: `git status --porcelain` empty; `git worktree list` the primary
    alone; `git log --numstat 0c8932e3..HEAD` with the `+` column per commit,
    each under 500.
Handback:    completion report + the rewritten `.agent/handoff.md` described in
             C5. Then push. Do NOT create a PR.
──────────────────────────────────────────────────────────────
