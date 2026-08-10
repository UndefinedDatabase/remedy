── STEP R27 — F105 ────────────────────────────────────────────
Goal:        Record the R26 gate, resolve R-0253 and R-0254, register and fix
             R-0255, then give the flight-plan prompt an `on_call` recorder so
             its segment manifest reaches call evidence at the one site whose
             evidence sink already exists.
Bundle:      C1 save this block · C2 the R26 gate record, the two `Done:` texts
             and R-0255 · C3 fix R-0255 · C4 the flight-plan call recorder and
             its `do_cmd` wiring · C5 plan and handoff.
Change:      `.agent/authored/f105-r27-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `docs/agents/planner_reviewer_prompt.md`,
             `packages/orchestration/flight_plan.py`,
             `apps/cli/commands/do_cmd.py`,
             `tests/orchestration/test_prompt_trace.py`, `.agent/plan.md`,
             `.agent/handoff.md`. Nothing else.
Constraints: SPLIT round (docs/agents/planner_reviewer_prompt.md §3, "Round
             types"): C4 touches production code under `packages/` and `apps/`,
             so you execute and the reviewer gates. Never self-certify it.
             Do NOT touch the replan site `apps/cli/commands/do_cmd.py:2859`.
             `write_trace_jsonl` opens its path with mode `"w"`, so a second
             write for the same job would TRUNCATE the first run's traces; that
             site needs a sink decision and gets its own round.
             Do not touch `make_intake_call_recorder`, the intake composer, or
             any of the other five migration sites. Do not change the signature
             of `plan_job_llm` or `_build_plan_prompt`. Do not reflow any line
             you were not given a pair for.
             A landed fix gets one `Landed: R-XXXX` line and no `Done:` text
             (docs/agents/planner_reviewer_prompt.md §4.4).
Done when:   every gate below is run and its REAL exit code recorded.

C1 — save this block verbatim, TWO commits
  C1a `cp` this block to `.agent/authored/f105-r27-1.md`. Commit it ALONE.
  C1b `cp` the same bytes to `.agent/last_block.md`. Commit separately.
  Both are `cp` of the file on disk — never a retype. `sha256sum` both plus
  `cmp`, and record the digest in the handback.

C2 — the R26 gate record, the two resolutions and R-0255 (own commit)
  Apply PAIR_A, PAIR_B, PAIR_C and PAIR_D to `.agent/live_review.md`.
  PAIR_A is APPEND-shaped (the TO contains the FROM verbatim as its prefix):
  prove FROM exactly 1x, then count the TO-only ADDED LINES IN THIS COMMIT'S
  DIFF (`git show --numstat`) with the stray count. PAIR_B, PAIR_C and PAIR_D
  are REWRITES (the TO does not contain the FROM): prove FROM 0x after and
  TO 1x, each grep SCOPED to `.agent/live_review.md`.

<<<PAIR_A_FROM>>>
  `LAST_REVIEWED_SHA` advances df32f595 -> 0341928d.
<<<END_PAIR_A_FROM>>>

<<<PAIR_A_TO>>>
  `LAST_REVIEWED_SHA` advances df32f595 -> 0341928d.
- R26: SPLIT repair round — record the R25 gate, fix R-0253 (§4.9 scoped to the
  diff's ADDED lines plus a sixth D8 checklist item) and R-0254 (the shared
  boundary helper's builder-only message plus the one assertion that pins it).
- Reviewer gate on R26 (2026-08-10): PASS. Range `0341928d..d0ebba63`, nine
  commits, read as a real diff. Every path the block named and no other:
  `.agent/authored/f105-r26-1.md`, `.agent/last_block.md`,
  `.agent/live_review.md`, `docs/agents/planner_reviewer_prompt.md`,
  `packages/orchestration/pingpong_loop.py`,
  `tests/orchestration/test_builder_prompt_golden.py`, `.agent/plan.md`,
  `.agent/handoff.md`. Insertions per commit 264, 196, 47, 17, 1, 3, 1, 80, 8 —
  each under 500, and the authored save is 264 lines against DECISION F105 D5's
  cap of 400.
  Transport verified under the §4.9 DIGEST FALLBACK: this reviewer session holds
  no scratchpad original, so sha256 was recomputed over the COMMITTED files.
  `.agent/authored/f105-r26-1.md` and `.agent/last_block.md` are both
  `c249919e7e8d111f9cac38d8593b9f0c67d409ae85530256a0367eac4b1b4a0d`, `cmp`
  silent, 264 lines each — the digest the handback declared.
  Application re-measured disk to disk against the COMMITTED authored file with
  the reviewer's own slicer, never a retype: PAIR_A append-shaped with the
  prefix property holding literally, FROM 1x; PAIR_B rewrite, FROM 0x after,
  TO 1x; PAIR_C append-shaped, FROM 1x; PAIR_D rewrite, FROM 0x, TO 1x; PAIR_E
  rewrite, FROM 0x, TO 1x; PAIR_F byte-equal to `.agent/plan.md` at 41 lines
  against the cap of 50. Declared shape equals measured shape for all six.
  R-0253's own new rule was applied for the first time and it holds. `git show
  --numstat 4c53c746` reads `47 0`, and all 47 ADDED lines are PAIR_A's TO-only
  lines at exactly 1x, strays 0. `git show --numstat c6ec5d3e` reads `17 2`;
  PAIR_B's first TO line is diff CONTEXT, so the 17 decompose as 9 (PAIR_B) + 8
  (PAIR_C TO-only), strays 0, extras 0.
  Gates re-run by THIS reviewer with real exit codes: the golden suite `21
  passed`, `tests/docs/` `294 passed`, the dashboard contract `70 passed`, the
  canary `42 passed`, and `tests/orchestration/` `10498 passed, 7 skipped in
  672.30s` — the module regression re-run in full, not accepted on the word.
  Mutation red-proof M1 run by the reviewer in a disposable worktree at
  d0ebba63: restoring the word "builder" turns exactly one test RED,
  `TestDropOneNewlinePerSegmentBoundary::test_a_boundary_with_no_newline_at_all_is_illegal`,
  at `1 failed, 20 passed`. The worktree was removed and pruned; `git status
  --porcelain` empty and `git worktree list` the primary alone at this verdict.
  Gate D's redness is charged to the REVIEWER, not to R26. The R26 block's own
  PAIR_A TO wrote the marker NAMES and a bare `<<<` into `.agent/live_review.md`
  as prose, and then ordered those strings to count 0 in that same file —
  DECISION F105 D8 item 2's sixth recurrence, and precisely the class R26's own
  new item 6 installs. The worker MEASURED it and declared it instead of editing
  prose to force the count down, which is the correct behaviour and costs R26
  nothing. The property the gate exists to protect does hold, independently
  checked: a line-anchored count of marker LINES is 0 in all five targets.
  `LAST_REVIEWED_SHA` advances 0341928d -> d0ebba63.
<<<END_PAIR_A_TO>>>

<<<PAIR_B_FROM>>>
  Landed: R-0253 — §4.9 scoped to diff-added lines and D8 item 6 added, commit c6ec5d3e.
<<<END_PAIR_B_FROM>>>

<<<PAIR_B_TO>>>
  Done: R-0253 (2026-08-10) — RESOLVED. §4.9 now scopes the TO-only count to the
  lines that commit's diff ADDS, names `git show --numstat` as the measurement,
  and D8 carries a sixth item for the whole-file collision. The reviewer
  re-measured the new rule against its own first use: the C2 commit adds 47
  lines, all 47 are PAIR_A TO-only lines at exactly 1x, strays 0 — achievable
  where the whole-file reading was not.
<<<END_PAIR_B_TO>>>

<<<PAIR_C_FROM>>>
  Landed: R-0254 — message is role-neutral and the assertion now anchors it, commit bb7b2cdc.
<<<END_PAIR_C_FROM>>>

<<<PAIR_C_TO>>>
  Done: R-0254 (2026-08-10) — RESOLVED. The message now reads "prompt segment
  boundary carries no newline to drop between segments N and N+1", so a
  reviewer-side boundary fault no longer reports itself as a builder fault, and
  the one assertion that pins it anchors with `^` and `$`. Re-proved by the
  reviewer in a disposable worktree at d0ebba63: putting "builder " back turns
  exactly that test RED, where before R26 the same mutation stayed green.
- R-0255 (Low, F105 R26): DECISION F105 D8's checklist now holds six items, but
  its preamble still reads "Run all four checks" and its closing note still
  reads "item 2 has recurred five times ... R20 hit all four items". Item 5
  landed at R24 and item 6 at R26; neither round updated the two counts. A
  reviewer following the preamble literally runs four of six checks — and the
  two the preamble drops are exactly the two most recently learned. The R26
  worker spotted this and correctly did NOT act: no pair was given for it and
  AGENTS.md Scope Control bars the "while I'm here" edit. Fix: the preamble
  says six, and the closing note says six recurrences and "four of them in one
  block". OPEN.
<<<END_PAIR_C_TO>>>

<<<PAIR_D_FROM>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0255.
<<<END_PAIR_D_FROM>>>

<<<PAIR_D_TO>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0256.
<<<END_PAIR_D_TO>>>

C3 — fix R-0255 (own commit)
  Apply PAIR_E and PAIR_F to `docs/agents/planner_reviewer_prompt.md`. Both are
  REWRITES: prove FROM 0x after and TO 1x, each grep SCOPED to that file.
  Then append ONE line to `.agent/live_review.md`, immediately after the line
  `  block". OPEN.`:
    `  Landed: R-0255 — D8's preamble and closing note now count six, commit <sha>.`
  with `<sha>` the short SHA of this commit. No other text.

<<<PAIR_E_FROM>>>
  four checks mechanically, on the FINAL bytes, after the last edit, before any
<<<END_PAIR_E_FROM>>>

<<<PAIR_E_TO>>>
  six checks mechanically, on the FINAL bytes, after the last edit, before any
<<<END_PAIR_E_TO>>>

<<<PAIR_F_FROM>>>
  Why this is on disk and not a habit: item 2 has recurred five times across
  F104 and F105, and R20 hit all four items in one block. A check that lives
<<<END_PAIR_F_FROM>>>

<<<PAIR_F_TO>>>
  Why this is on disk and not a habit: item 2 has recurred six times across
  F104 and F105, and R20 hit four of them in one block. A check that lives
<<<END_PAIR_F_TO>>>

C4 — the flight-plan call recorder and its wiring (own commit)
  Apply PAIR_G and PAIR_H to `packages/orchestration/flight_plan.py`, then
  PAIR_I, PAIR_J, PAIR_K and PAIR_L to `apps/cli/commands/do_cmd.py`, then
  PAIR_M to `tests/orchestration/test_prompt_trace.py`. All in ONE commit: the
  recorder, its only caller and the test that fails when the wiring is removed
  are one unit, and splitting them lands a commit whose guard test is red.
  PAIR_G is APPEND-shaped (the TO contains the FROM verbatim as its SUFFIX).
  PAIR_H and PAIR_M are APPEND-shaped (TO contains FROM as its PREFIX).
  PAIR_I, PAIR_J, PAIR_K and PAIR_L are REWRITES.
  For every APPEND pair prove FROM exactly 1x plus the TO-only ADDED-LINE count
  from this commit's diff with the stray count; for every REWRITE prove FROM 0x
  after and TO 1x. Every grep is SCOPED to the one file the pair targets.
  `provider="ollama"` mirrors the intake call site in the same function, which
  hardcodes the same value for the same reason: `make_provider_call_fn()` is
  the ollama provider.

<<<PAIR_G_FROM>>>
from packages.orchestration.schemas.models import (
<<<END_PAIR_G_FROM>>>

<<<PAIR_G_TO>>>
from packages.orchestration.prompt_trace import build_trace_entry
from packages.orchestration.schemas.models import (
<<<END_PAIR_G_TO>>>

<<<PAIR_H_FROM>>>
    return compose_flight_plan_prompt(intake_dict, project_facts=project_facts).text
<<<END_PAIR_H_FROM>>>

<<<PAIR_H_TO>>>
    return compose_flight_plan_prompt(intake_dict, project_facts=project_facts).text


# The recorder lives beside the composer, in this module, so the manifest and
# the prompt it describes cannot drift apart: whoever changes flight-plan
# composition sees the evidence writer in the same file (F105 T003 site 5, the
# same reason `make_intake_call_recorder` sits in `intake.py`).
def make_flight_plan_call_recorder(
    traces: list[Any],
    composed: ComposedPrompt,
    *,
    provider: str = "",
    provider_kind: str = "",
) -> Callable[[int, str, bool, str], None]:
    """Build the ``on_call`` recorder ``plan_job_llm`` expects.

    Every provider invocation appends one prompt trace entry to ``traces``,
    carrying ``composed``'s segment manifest so call evidence records which
    named segments produced the prompt.

    The role is ``flight_plan``, deliberately NOT ``planner``: the ``planner``
    traces belong to the OTHER planner path
    (``packages/orchestration/structured_planner.py`` over ``PlannerPlan``), and
    one spelling per concept is what keeps a per-role cache report from summing
    two different prompts into one row.
    """
    def _record(
        attempt: int, schema_v: str, is_parse_retry: bool, effective_prompt: str,
    ) -> None:
        kind = "flight-plan-retry" if is_parse_retry else "flight-plan"
        traces.append(build_trace_entry(
            prompt_text=effective_prompt,
            role="flight_plan",
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
<<<END_PAIR_H_TO>>>

<<<PAIR_I_FROM>>>
    intake_traces: list = []
<<<END_PAIR_I_FROM>>>

<<<PAIR_I_TO>>>
    # One list, one write: it carries every prompt trace this command produces,
    # intake and flight plan alike, because `write_trace_jsonl` opens its path
    # with mode "w" and a second write would truncate the first.
    prompt_traces: list = []
<<<END_PAIR_I_TO>>>

<<<PAIR_J_FROM>>>
                on_call=make_intake_call_recorder(
                    intake_traces,
<<<END_PAIR_J_FROM>>>

<<<PAIR_J_TO>>>
                on_call=make_intake_call_recorder(
                    prompt_traces,
<<<END_PAIR_J_TO>>>

<<<PAIR_K_FROM>>>
    if intake_traces:
        from packages.orchestration.prompt_trace import write_trace_jsonl
        from packages.orchestration.run_log import RunLogWriter
        log = RunLogWriter(job_id=job.id)
        try:
            write_trace_jsonl(intake_traces, log.path.parent / "prompt_trace.jsonl")
<<<END_PAIR_K_FROM>>>

<<<PAIR_K_TO>>>
    if prompt_traces:
        from packages.orchestration.prompt_trace import write_trace_jsonl
        from packages.orchestration.run_log import RunLogWriter
        log = RunLogWriter(job_id=job.id)
        try:
            write_trace_jsonl(prompt_traces, log.path.parent / "prompt_trace.jsonl")
<<<END_PAIR_K_TO>>>

<<<PAIR_L_FROM>>>
        from packages.orchestration.flight_plan import (
            apply_plan_budgets,
            apply_plan_fences,
            map_flight_plan_to_tasks,
            plan_job_llm,
            write_plan_md,
        )
        fp_result = plan_job_llm(intake_result.value.model_dump(), plan_call_fn)
<<<END_PAIR_L_FROM>>>

<<<PAIR_L_TO>>>
        from packages.orchestration.flight_plan import (
            apply_plan_budgets,
            apply_plan_fences,
            compose_flight_plan_prompt,
            make_flight_plan_call_recorder,
            map_flight_plan_to_tasks,
            plan_job_llm,
            write_plan_md,
        )
        plan_intake_dict = intake_result.value.model_dump()
        # The manifest is composed here and the bytes are built again inside
        # `plan_job_llm`; both go through `compose_flight_plan_prompt`, so the
        # trace carries `prompt_chars` from the effective prompt and
        # `segment_manifest_chars` from this composition and a divergence stays
        # visible rather than silent.
        plan_composed = compose_flight_plan_prompt(plan_intake_dict)
        fp_result = plan_job_llm(
            plan_intake_dict,
            plan_call_fn,
            on_call=make_flight_plan_call_recorder(
                prompt_traces,
                plan_composed,
                provider="ollama",
                provider_kind="ollama",
            ),
        )
<<<END_PAIR_L_TO>>>

<<<PAIR_M_FROM>>>
        assert "make_intake_call_recorder" in inspect.getsource(do_cmd)
<<<END_PAIR_M_FROM>>>

<<<PAIR_M_TO>>>
        assert "make_intake_call_recorder" in inspect.getsource(do_cmd)

    def test_the_cli_flight_plan_recorder_passes_the_composed_prompt(self):
        """Wiring guard: an unwired flight-plan manifest fails HERE (F105 R27)."""
        import apps.cli.commands.do_cmd as do_cmd
        from packages.orchestration.flight_plan import (
            compose_flight_plan_prompt,
            make_flight_plan_call_recorder,
        )

        traces: list = []
        composed = compose_flight_plan_prompt(
            {"goal": "demo"}, project_facts="pinned facts"
        )
        recorder = make_flight_plan_call_recorder(
            traces, composed, provider="ollama", provider_kind="ollama"
        )
        recorder(1, "fp1", False, composed.text)
        assert len(traces) == 1
        assert traces[0].role == "flight_plan"
        assert traces[0].prompt_kind == "flight-plan"
        assert len(traces[0].segment_manifest) == 5

        source = inspect.getsource(do_cmd)
        assert "make_flight_plan_call_recorder" in source
        assert "prompt_traces" in source
<<<END_PAIR_M_TO>>>

C5 — plan and handoff (own commit)
  Apply PAIR_N to `.agent/plan.md` as a FULL replacement, then rewrite
  `.agent/handoff.md`.

<<<PAIR_N_PLAN>>>
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
T001 and T002 are DONE and gated. T003's six migration sites are all migrated,
each under its own golden. R26 is GATED; `LAST_REVIEWED_SHA` is d0ebba63.
R27 is a SPLIT round: it records the R26 gate, resolves R-0253 and R-0254,
registers and fixes R-0255 (D8's preamble counts four checks over a six-item
list), and wires `on_call` for the flight-plan prompt at
`apps/cli/commands/do_cmd.py` — the one evidence gap whose sink already exists.
Open findings: R-0221, R-0239, R-0246, R-0247, R-0255.
No PR; one is created at CLOSURE.

## Next Steps
- The replan site `apps/cli/commands/do_cmd.py:2859` needs a sink DECISION
  first: `write_trace_jsonl` opens with mode `"w"`, so a second write for the
  same job truncates the first run's traces.
- Then `on_call` for the mission and orchestrator prompts —
  `mission_cmd.py:187`, `mission_cmd.py:362`, `gauntlet_runner.py:505` — none
  of which has an evidence sink today.
- Fix R-0246 in the round that next touches `mission_compiler.py`.
- Then T004, `remedy stats cache` over actuals; then the integration gate
  (docs/agents/integration_gate.md); then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- The reviewer prompt was the worst-ordered of the six sites and 1824 of 2048
  measured renders reorder, so T004's before/after number should quote its
  cacheable-prefix gain specifically.
<<<END_PAIR_N_PLAN>>>

GATES — run every one, record the REAL exit code and the REAL output
  A transport: `sha256sum` on `.agent/authored/f105-r27-1.md` and
    `.agent/last_block.md`; `cmp` them. Digest in the handback.
  B size: `wc -l .agent/authored/f105-r27-1.md`.
  C application, each grep SCOPED to the named file:
    REWRITES, prove FROM 0x after and TO 1x — PAIR_B, PAIR_C, PAIR_D in
    `.agent/live_review.md`; PAIR_E, PAIR_F in
    `docs/agents/planner_reviewer_prompt.md`; PAIR_I, PAIR_J, PAIR_K, PAIR_L in
    `apps/cli/commands/do_cmd.py`.
    APPENDS, prove FROM exactly 1x — PAIR_A in `.agent/live_review.md`;
    PAIR_G, PAIR_H in `packages/orchestration/flight_plan.py`; PAIR_M in
    `tests/orchestration/test_prompt_trace.py`.
    For EVERY append pair also give the TO-only ADDED-LINE count from
    `git show --numstat <commit> -- <path>` plus the stray count, per §4.9 as
    R26 amended it. Do NOT use whole-file counts for an append pair.
    PAIR_N: `cmp` the applied `.agent/plan.md` against the sliced PAIR_N;
    `wc -l .agent/plan.md` must be under 50.
  D marker leakage, LINE-anchored: `grep -c -E '^<<<'` in
    `.agent/live_review.md`, `.agent/plan.md`,
    `docs/agents/planner_reviewer_prompt.md`,
    `packages/orchestration/flight_plan.py`, `apps/cli/commands/do_cmd.py` and
    `tests/orchestration/test_prompt_trace.py` — each count must be 0. The
    count is over marker LINES on purpose: pair bodies in this block quote
    marker names and a bare `<<<` in prose, and a substring count over those
    files would be counting this block's own text (DECISION F105 D8 item 2).
  E the touched suite: `python3 -m pytest tests/orchestration/test_prompt_trace.py -q`.
  F red-proof M1, in a DISPOSABLE `git worktree` at HEAD and nowhere else:
    in `apps/cli/commands/do_cmd.py` delete BOTH the
    `on_call=make_flight_plan_call_recorder(...)` argument (restoring the bare
    two-argument `plan_job_llm` call) AND the `make_flight_plan_call_recorder,`
    import line, then run
    `python3 -m pytest tests/orchestration/test_prompt_trace.py -q`. It MUST go
    RED. Report the exit code and the failing test NAME. Then remove and prune
    the worktree. If it comes out GREEN, do NOT edit anything to force a red —
    report the green as a declared deviation, because a green there means the
    guard does not pin the wiring and the reviewer needs to know that, not a
    repaired number.
  G module regression: `python3 -m pytest tests/orchestration/ -q` and
    `python3 -m pytest tests/cli/ -q`. Production code changed in both trees.
  H contract tests: `python3 -m pytest tests/docs/ -q` and
    `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q`.
  I canary: `python3 -m pytest tests/cli/test_golden_path.py -q`.
  J hygiene: `git status --porcelain` empty; `git worktree list` the primary
    alone; `git log --numstat d0ebba63..HEAD` with the `+` column per commit.
Handback:    completion report + rewrite `.agent/handoff.md` (changed-files
             table one row per path, item-status table over
             C1a/C1b/C2/C3/C4/C5, the gate table with REAL exit codes and REAL
             output, transport and pair proofs, the red-proof result,
             open-findings count, next action). Keep it under 60 lines, or
             carry a DECISION D15 "Deviations, declared" line naming the real
             count and the mandated content that caused the overage. Then push.
             Do NOT create a PR.
──────────────────────────────────────────────────────────────
