── STEP R6/n — F115 Prompt breakdown & cost report · Round 6 ─────────
Goal:        Wire the PLANNER call site, the last unwired `build_trace_entry`
             site: build `compose_planner_prompt`, hand the composition down to
             `_record_plan_call`, and prove the sent bytes did not change.
Bundle:      C1a save block · C1b mirror · C2 register R-0324 · C3 DECISION D3 ·
             C4 composer + hook · C5 composer tests · C6 CLI wiring ·
             C7 CLI trace guard · C8 plan + handback
Change:      EXACTLY these paths:
               .remedy-wt/f115-r6-1.md      (source, gitignored, NOT committed)
               .agent/authored/f115-r6-1.md (new, C1a)
               .agent/last_block.md         (rewrite, C1b)
               .agent/live_review.md        (C2: append)
               .agent/decisions.md          (C3: append)
               packages/orchestration/llm_planner.py              (C4)
               tests/test_llm_planner.py                          (C5)
               apps/cli/commands/job.py                           (C6)
               tests/orchestration/test_structured_planner_cli.py (C7)
               .agent/plan.md               (C8: full replace)
               .agent/handoff.md            (C8: rewrite)
Constraints:
  - TEXT-A … TEXT-K are AUTHORED text: apply byte for byte, no rewording,
    rewrapping or re-punctuation, and no slots to substitute.
  - THE SENT BYTES MAY NOT CHANGE. `compose_planner_prompt` describes the prompt
    this module already builds; it does not improve it. If gate (b) is red, STOP
    and hand back — never adjust a text, a rank or a delimiter to make it green.
  - Do NOT write a `Done:` paragraph and do NOT mark R-0324 resolved
    (docs/agents/planner_reviewer_prompt.md §4.4); a fix landing before the
    reviewer's resolution is marked `Landed:` and nothing else.
  - Do NOT fix R-0320 or R-0322. Both predate this branch and neither is an
    F115 defect; AGENTS.md bars mixing an unrelated fix into a feature branch.
  - Do NOT touch `structured_planner.py`, `structured_outputs.py`,
    `prompt_segments.py` or `prompt_trace.py`. The schema tail stays outside the
    registry (DECISION F105 D9): the manifest covers the composed base prompt
    only, and that gap is recorded, not repaired here.
  - Never force-push. Never commit on main. Push after EVERY commit (R-0289).
  - Do NOT create a pull request this round.
Done when: every command RUN for real, its TRUE output recorded — a guessed,
           expected or remembered value is a finding.
  a. `cmp .agent/authored/f115-r6-1.md .agent/last_block.md` exits 0; record
     `sha256sum` of both and `wc -lc` of the authored file.
  b. IDENTITY GATE, RUN FIRST after C5 and before C6:
     `python3 -m pytest tests/test_llm_planner.py -q` — measured baseline `34
     passed`, TEXT-H adds FOUR tests, so 38 is expected. Record the real tail
     and exit code. A red identity test ends the round.
  c. After C2 and C3, over `.agent/live_review.md`: `grep -c '^- R-0324'` = 1 ·
     `grep -c '^- R-0'` = 5 (was 4) · `grep -c '^Done:'` = 1 (unchanged) ·
     `grep -c '^## Steps'` = 1; and
     `grep -c '^## DECISION F115 D3' .agent/decisions.md` = 1.
  d. After C7: `python3 -m pytest tests/orchestration/test_structured_planner_cli.py -q`
     — measured baseline `15 passed`; TEXT-J adds TWO tests, so 17 is expected.
  e. Neighbours, one command:
     `python3 -m pytest tests/test_llm_planner.py tests/orchestration/test_structured_planner_cli.py tests/orchestration/test_memory_planning.py tests/orchestration/test_prompt_trace.py tests/orchestration/test_prompt_segments.py -q`
     — measured baseline `128 passed`; with the six new tests, 134 is expected.
  f. Canary `python3 -m pytest tests/cli/test_golden_path.py -q` — measured baseline `42 passed`, must not move.
  g. `wc -l .agent/plan.md` prints a number BELOW 50 — record the real one.
  h. `git status --porcelain` empty; `git diff --name-only 0d6c97aa..HEAD | wc -l`
     — the EIGHTEEN paths present after R5 plus this round's FIVE new ones
     (`.agent/authored/f115-r6-1.md`, `packages/orchestration/llm_planner.py`,
     `tests/test_llm_planner.py`, `apps/cli/commands/job.py`,
     `tests/orchestration/test_structured_planner_cli.py`), none of them in the
     R5 list, so 23 is expected. If it is not 23, report the real number and the
     actual list and change nothing; `.remedy-wt/**` must NOT appear. Finally
     `git rev-list --left-right --count origin/feature/f115-prompt-cost-report...HEAD`
     prints 0 and 0.
Handback:  completion report + rewrite `.agent/handoff.md`: item-status table
           (C1a, C1b, C2, C3, C4, C5, C6, C7, C8 — each exactly once), commit
           table with real SHAs and insertions, changed-files table, every
           result a-h as a REAL value, the Fortschritt line verbatim. Over 60
           lines ⇒ a "Deviations, declared" line naming the count and the
           mandated content that caused it (AGENTS.md DECISION D15).
──────────────────────────────────────────────────────────────────────

PROCEDURE

C1a `chore(f115): save the R6 step block verbatim` — copy the reviewer's
    scratchpad original `.remedy-wt/f115-r6-1.md` to
    `.agent/authored/f115-r6-1.md`. Copy the FILE; do not retype it.
C1b `chore(f115): mirror the R6 block into last_block` — copy that same file to
    `.agent/last_block.md`. Run gate (a).

C2 `chore(f115): register R-0324 for the D2 rank assignment`
    Append TEXT-A to the END of `.agent/live_review.md`.

C3 `docs(f115): correct the planner segment ranks as DECISION D3`
    Append TEXT-B to the END of `.agent/decisions.md`. Run gate (c).

C4 `feat(f115): compose the planner prompt from ranked segments`
    Apply TEXT-C, TEXT-D, TEXT-E, TEXT-F to `packages/orchestration/llm_planner.py`.

C5 `test(f115): pin the planner composition against the sent bytes`
    Apply TEXT-G, and TEXT-H at the END of `tests/test_llm_planner.py`. Run gate
    (b) NOW — before C6 exists. If it is red, stop and hand back.

C6 `feat(f115): give the planner trace entry its segment manifest`
    Apply TEXT-I1, TEXT-I2 and TEXT-I3 to `apps/cli/commands/job.py`.

C7 `test(f115): pin the planner trace manifest and its wiring`
    Apply TEXT-J at the END of `tests/orchestration/test_structured_planner_cli.py`.
    Run gates (d) and (e).

C8 `chore(f115): refresh the plan and write the R6 handoff`
    `.agent/plan.md` ← TEXT-K in full, then rewrite `.agent/handoff.md`.
    Run gates (f), (g) and (h).

TEXT-A — append to the END of .agent/live_review.md

- R-0324 — Low — reviewer spec arithmetic, self-registered, caught before the
  round it would have broken. DECISION F115 D2 (R5) fixed the planner segment
  ranks as "the job prompt at TASK rank, the recalled memory section at
  JOB_CONTEXT rank". Composition sorts by rank ASCENDING
  (`compose_prompt_segments`, `prompt_segments.py:182-188`) and JOB_CONTEXT is 3
  against TASK's 4, so that assignment composes the MEMORY SECTION FIRST, while
  the code it must reproduce concatenates the other way round —
  `prompt = f"{prompt}\n\n{memory_section}"`, `llm_planner.py:107-109`. D2's own
  byte-identity gate, the one it calls the round's first gate, was therefore
  unmeetable by construction — reading the rank names as semantic labels rather
  than as the sort key they are is what produced the slip. Corrected before
  emission as DECISION F115 D3, by checklist item 8
  (`docs/agents/planner_reviewer_prompt.md`) — compute a gate's expected value
  from the code that PRODUCES it. Fourth of the reviewer-arithmetic class after
  R-0282, R-0321 and R-0323, and the first caught before a worker paid. OPEN.

TEXT-B — append to the END of .agent/decisions.md

## DECISION F115 D3 (2026-08-13) — the planner segments rank so composition reproduces the sent order

Supersedes the RANK ASSIGNMENT in DECISION F115 D2 and nothing else in it: the
composer, the optional hook, the untouched `on_call` contract and the
byte-identity-first gate all stand as D2 recorded them.

Context: `compose_prompt_segments` sorts by `(int(rank), registration index)`
ascending, and `SegmentStabilityRank.JOB_CONTEXT` is 3 against TASK's 4, so D2's
ranks compose the memory section BEFORE the job prompt. The sent bytes are the
other order: `llm_planner.py:107-109` builds `prompt` from `job.user_prompt or
job.name`, then appends `f"\n\n{memory_section}"`. D2's ranks and D2's identity
gate contradict each other; the gate is the load-bearing half.

Chosen: `planner_job_prompt` at `SegmentStabilityRank.TASK` and
`planner_memory_context` at `SegmentStabilityRank.STEERING` — the only pair of
DISTINCT ranks that reproduces the existing order. The scale's declared meaning
is cache stability, "stable prefixes first, volatile tails last"
(`prompt_segments.py:52`), and a per-job memory recall already sitting in the
prompt's tail belongs there on both readings.

Alternatives: (a) both segments at TASK rank, letting the registration-index
tie-break carry the order — rejected, it makes a tie-break load-bearing where a
rank states the same thing explicitly; (b) memory at DOSSIER or CONVENTIONS —
rejected, both are below TASK and reverse the order as JOB_CONTEXT does;
(c) keep D2's ranks and let the sent bytes change — rejected outright, F115 D1
is that the manifest describes what was sent, and a telemetry feature may not
edit the prompt it measures.

Reverse by deleting this entry and restoring D2's ranks — which also means
accepting a changed planner prompt, so the two are one decision.

TEXT-C — APPEND-shaped pair for packages/orchestration/llm_planner.py

FROM:
from packages.orchestration.planner_models import PlannerOutput, ProposedTask
TO:
from packages.orchestration.planner_models import PlannerOutput, ProposedTask
from packages.orchestration.prompt_segments import (
    ComposedPrompt,
    PromptSegmentRegistry,
    SegmentStabilityRank,
    compose_prompt_segments,
)

TEXT-D — REWRITE pair for packages/orchestration/llm_planner.py

FROM:
def plan_job_with_llm(
    job: Job,
    call_planner: Callable[[str], PlannerOutput],
) -> PlanJobResult:
TO:
# Named segments for the planner prompt, so a ledger row can say WHERE its
# tokens went. Ranks are the composition sort key, not a semantic label: TASK
# before STEERING is what reproduces the byte order already sent (DECISION D3).
def compose_planner_prompt(job_prompt: str, memory_section: str = "") -> ComposedPrompt:
    """Compose the planner prompt from registered segments, with its manifest.

    Byte identity with the pre-F115 concatenation is the whole contract: the
    join string is `PROMPT_SEGMENT_DELIMITER`, which IS the `\n\n` this module
    used by hand, and an absent memory section registers NO segment rather than
    an empty one — so a one-segment composition is the bare job prompt.
    """
    registry = PromptSegmentRegistry()
    registry.register("planner_job_prompt", SegmentStabilityRank.TASK, job_prompt)
    if memory_section:
        registry.register(
            "planner_memory_context", SegmentStabilityRank.STEERING, memory_section
        )
    return compose_prompt_segments(registry.registered_segments())


def plan_job_with_llm(
    job: Job,
    call_planner: Callable[[str], PlannerOutput],
    *,
    on_prompt_composed: Callable[[ComposedPrompt], None] | None = None,
) -> PlanJobResult:

TEXT-E — APPEND-shaped pair for packages/orchestration/llm_planner.py

FROM:
      - injecting approved project memory context when available
TO:
      - injecting approved project memory context when available
      - handing the composed prompt to ``on_prompt_composed``, when given,
        immediately before the provider call, so a caller can trace the
        segment manifest of the bytes it is about to send

TEXT-F — REWRITE pair for packages/orchestration/llm_planner.py

FROM:
    prompt = job.user_prompt or job.name
    if memory_section:
        prompt = f"{prompt}\n\n{memory_section}"

    output: PlannerOutput = call_planner(prompt)
TO:
    # F115 D1/D3: compose instead of concatenating, so the caller's trace entry
    # carries a real segment manifest. The sent bytes are unchanged — the
    # composer joins with the same delimiter this concatenation used.
    composed = compose_planner_prompt(job.user_prompt or job.name, memory_section)
    prompt = composed.text
    if on_prompt_composed is not None:
        on_prompt_composed(composed)

    output: PlannerOutput = call_planner(prompt)

TEXT-G — REWRITE pair for tests/test_llm_planner.py

FROM:
from packages.orchestration.llm_planner import annotate_planning_result, plan_job_with_llm
TO:
from packages.orchestration.llm_planner import (
    annotate_planning_result,
    compose_planner_prompt,
    plan_job_with_llm,
)
from packages.orchestration.prompt_segments import (
    PROMPT_SEGMENT_DELIMITER,
    SegmentStabilityRank,
)

TEXT-H — append to the END of tests/test_llm_planner.py

# F115 — the planner prompt is composed, and composing it changes no byte.

_MEMORY_SECTION = "## Project Memory\n- prefer small commits"


def test_compose_planner_prompt_without_memory_is_the_bare_job_prompt():
    """One segment composes to itself: no delimiter, no header, no marker."""
    composed = compose_planner_prompt("Fix the bug")
    assert composed.text == "Fix the bug"
    assert [e.name for e in composed.manifest] == ["planner_job_prompt"]
    assert [e.rank for e in composed.manifest] == [int(SegmentStabilityRank.TASK)]


def test_compose_planner_prompt_with_memory_keeps_the_legacy_byte_order():
    """The pre-F115 concatenation, byte for byte: job prompt first, memory last."""
    composed = compose_planner_prompt("Fix the bug", _MEMORY_SECTION)
    assert composed.text == f"Fix the bug{PROMPT_SEGMENT_DELIMITER}{_MEMORY_SECTION}"
    assert [e.name for e in composed.manifest] == [
        "planner_job_prompt",
        "planner_memory_context",
    ]
    assert [e.rank for e in composed.manifest] == [
        int(SegmentStabilityRank.TASK),
        int(SegmentStabilityRank.STEERING),
    ]


def test_compose_planner_prompt_manifest_accounts_for_every_character():
    """Row chars plus one delimiter per join is the composed length, exactly."""
    composed = compose_planner_prompt("Fix the bug", _MEMORY_SECTION)
    rows = composed.manifest
    joined = sum(e.chars for e in rows) + len(PROMPT_SEGMENT_DELIMITER) * (len(rows) - 1)
    assert joined == len(composed.text)


def test_plan_job_with_llm_hands_down_the_composition_it_sends():
    """The hook sees the ComposedPrompt whose `.text` is the prompt sent."""
    seen: list = []
    sent: list = []

    def _capture(prompt: str) -> PlannerOutput:
        sent.append(prompt)
        return _make_output()

    job = Job(name="test-job", user_prompt="Fix the bug")
    plan_job_with_llm(job, _capture, on_prompt_composed=seen.append)
    assert len(seen) == 1
    assert sent == [seen[0].text]
    assert seen[0].manifest[0].name == "planner_job_prompt"

TEXT-I1 — APPEND-shaped pair for apps/cli/commands/job.py

FROM:
    _plan_traces: list = []
TO:
    _plan_traces: list = []
    # F115: `plan_job_with_llm` appends the ComposedPrompt it is about to send,
    # so the recorder below can name the segments of the exact prompt it traces
    # instead of rebuilding a second composition that could drift from it.
    _plan_compositions: list = []

TEXT-I2 — REWRITE pair for apps/cli/commands/job.py

FROM:
            transport_attempt=attempt,
            is_transport_retry=False,
        ))
TO:
            transport_attempt=attempt,
            is_transport_retry=False,
            composed_prompt=_plan_compositions[-1] if _plan_compositions else None,
        ))

TEXT-I3 — REWRITE pair for apps/cli/commands/job.py

FROM:
        result: PlanJobResult = plan_job_with_llm(job, call_planner)
TO:
        result: PlanJobResult = plan_job_with_llm(
            job, call_planner, on_prompt_composed=_plan_compositions.append,
        )

TEXT-J — append to the END of tests/orchestration/test_structured_planner_cli.py


class TestPlannerTraceCarriesItsSegmentManifest:
    """F115 wiring guard: a planner trace with an empty manifest fails HERE."""

    def test_every_plan_trace_names_the_segments_it_sent(self, tmp_path, monkeypatch):
        from packages.orchestration.prompt_segments import SegmentStabilityRank

        job = _make_job(tmp_path, monkeypatch)
        planner = _FakePlanner(["bad", VALID_PLAN])
        with _patch_planner(planner):
            _run(job.id)
        traces = _plan_traces(tmp_path, job.id)
        assert len(traces) == 2
        for trace in traces:
            assert trace["segment_manifest"], "planner trace carries no manifest"
            first = trace["segment_manifest"][0]
            assert first["name"] == "planner_job_prompt"
            assert first["rank"] == int(SegmentStabilityRank.TASK)
            # The schema tail sits outside the registry (DECISION F105 D9): the
            # manifest covers a strict prefix of the prompt actually sent.
            assert 0 < trace["segment_manifest_chars"] < trace["prompt_chars"]

    def test_the_cli_hands_the_planner_composition_down(self):
        import inspect

        import apps.cli.commands.job as job_cmd

        source = inspect.getsource(job_cmd)
        assert "on_prompt_composed=_plan_compositions.append" in source
        assert "composed_prompt=_plan_compositions[-1]" in source

TEXT-K — the complete new .agent/plan.md

# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged. Last reviewed SHA: 1422b01f (R5 PASS). Next free finding
ID: R-0325. Open findings: 4 — R-0320 (Low, from F111), R-0322 (Medium,
inherited suite red), R-0323 + R-0324 (Low, reviewer arithmetic).

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
R6 wired the PLANNER call site per DECISION F115 D3: composed from two
ranked segments, handed to the trace entry through an optional hook,
sent bytes pinned unchanged. All three call sites are now wired.

## Next Steps
1. T001 proper — persist the manifest, or a reference to it, alongside
   the ledger row, additively, with backfill tolerance: old rows render
   as "unattributed", never guessed.
2. T002 — aggregation queries plus the pure renderer, with goldens;
   follow `gauntlet_matrix.py` and `tests/cli/test_stats_cost.py:49-128`.
3. T003 — CLI, prior-period comparison, json schema.
4. Integration gate (docs/agents/integration_gate.md), then closure.

## Risks
- Per-role has one bucket until `role` stops being hardcoded, and
  per-task-class has no source at all: report "no data", never a bucket.
- R-0322 will meet F115's integration gate as five pre-existing reds.

Fortschritt: 40 % (R1 ✅ · T001a ✅ · alle drei Call-Sites ✅ · T001 · T002 · T003 offen) — Schätzung
