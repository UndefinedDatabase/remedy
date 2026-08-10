── STEP R28 — F105 ────────────────────────────────────────────
Goal:        Record the R27 gate, resolve R-0255, register R-0256, and close
             the last do_cmd evidence gap: give the trace writer an APPEND
             sibling and wire the replan site with it, so a replan records its
             flight-plan manifest without truncating the traces the job's first
             run wrote.
Bundle:      C1 save this block · C2 the R27 gate record, the `Done:` text and
             R-0256 · C3 `append_trace_jsonl` and its tests · C4 the replan
             wiring and its guard · C5 plan and handoff.
Change:      `.agent/authored/f105-r28-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `packages/orchestration/prompt_trace.py`,
             `apps/cli/commands/do_cmd.py`,
             `tests/orchestration/test_prompt_trace.py`, `.agent/plan.md`,
             `.agent/handoff.md`. Nothing else.
Constraints: SPLIT round (docs/agents/planner_reviewer_prompt.md §3, "Round
             types"): C3 and C4 touch production code under `packages/` and
             `apps/`, so you execute and the reviewer gates. Never self-certify.
             Do NOT change `write_trace_jsonl` — its mode "w" is correct for the
             command that creates the job, and every existing caller depends on
             it. `append_trace_jsonl` is a new function beside it, not a
             replacement and not a parameter on the old one.
             Do not touch the first `plan_job_llm` call site wired at R27, do
             not touch `make_intake_call_recorder`, and do not reflow any line
             you were not given a pair for.
             A landed fix gets one `Landed: R-XXXX` line and no `Done:` text
             (§4.4).
Done when:   every gate below is run and its REAL exit code recorded.

C1 — save this block verbatim, TWO commits
  C1a `cp` this block to `.agent/authored/f105-r28-1.md`. Commit it ALONE.
  C1b `cp` the same bytes to `.agent/last_block.md`. Commit separately.
  Both are `cp` of the file on disk. `sha256sum` both plus `cmp`; digest in the
  handback.

C2 — the R27 gate record, the resolution and R-0256 (own commit)
  Apply PAIR_A, PAIR_B and PAIR_C to `.agent/live_review.md`. PAIR_A is
  APPEND-shaped (TO contains FROM verbatim as its prefix): prove FROM exactly
  1x plus the TO-only ADDED-LINE count from this commit's diff and the stray
  count. PAIR_B and PAIR_C are REWRITES: prove FROM 0x after and TO 1x, each
  grep SCOPED to `.agent/live_review.md`.

<<<PAIR_A_FROM>>>
  `LAST_REVIEWED_SHA` advances 0341928d -> d0ebba63.
<<<END_PAIR_A_FROM>>>

<<<PAIR_A_TO>>>
  `LAST_REVIEWED_SHA` advances 0341928d -> d0ebba63.
- R27: SPLIT round — record the R26 gate, resolve R-0253 and R-0254, register
  and fix R-0255, and wire `on_call` for the flight-plan prompt at the one
  `do_cmd` site whose evidence sink already exists.
- Reviewer gate on R27 (2026-08-10): PASS. Range `d0ebba63..73259d7a`, eight
  commits, read as a real diff: only the nine paths the block named, and the
  replan site the block forbade is untouched. Insertions per commit 457, 371,
  69, 3, 1, 95, 77, 1 — each under 500.
  Transport under the §4.9 digest fallback: `.agent/authored/f105-r28-1.md`'s
  predecessor `.agent/authored/f105-r27-1.md` and `.agent/last_block.md` both
  recompute to `efef62a6c61e08b33682175f034b9ba1441cac7245b6dceca5e05093199fb71a`,
  `cmp` silent, 457 lines each — the digest the handback declared.
  All 13 pairs re-sliced from the COMMITTED authored file by the reviewer's own
  marker-LINE reader and measured disk to disk: declared shape equals measured
  shape for every one, appends at FROM 1x, rewrites at FROM 0x after and TO 1x,
  and PAIR_N byte-equal to `.agent/plan.md` at 42 lines against the cap of 50.
  Diff-scoped accounting per §4.9: `.agent/live_review.md` ADDED 69, fully
  decomposed, strays 0; `docs/agents/planner_reviewer_prompt.md` ADDED 3,
  strays 0; `packages/orchestration/flight_plan.py` ADDED 44, strays 0;
  `tests/orchestration/test_prompt_trace.py` ADDED 25, strays 0;
  `apps/cli/commands/do_cmd.py` ADDED 26, strays 0. No ADDED line in any file
  came from outside a TO slice.
  Gates re-run by THIS reviewer with real exit codes: `tests/orchestration/`
  `10499 passed, 7 skipped in 627.56s` — one more test than R26's 10499-minus-one
  baseline, the new guard; `tests/cli/` `1329 passed in 260.89s`;
  `test_prompt_trace.py` `38 passed`; `tests/docs/` `294 passed`; the dashboard
  contract `70 passed`; the canary `42 passed`. Mutation red-proof M1 run by the
  reviewer in a disposable worktree at 73259d7a: removing BOTH the `on_call=`
  argument and the `make_flight_plan_call_recorder,` import turns exactly one
  test RED, `TestSegmentManifest::test_the_cli_flight_plan_recorder_passes_the_composed_prompt`,
  at `1 failed, 37 passed`. Worktree removed and pruned; `git status
  --porcelain` empty and `git worktree list` the primary alone at this verdict.
  The 457-line block is charged to the REVIEWER, not to R27. DECISION F105 D5
  caps a block at 400 and D8 item 1 says to COUNT it on the final bytes; the
  reviewer estimated instead of counting, and a block must be saved verbatim, so
  the worker was right to declare the overage rather than trim it. First
  recurrence of item 1 in this feature. The remedy is mechanical counting before
  emission, which is what item 1 already prescribes.
  `LAST_REVIEWED_SHA` advances d0ebba63 -> 73259d7a.
<<<END_PAIR_A_TO>>>

<<<PAIR_B_FROM>>>
  Landed: R-0255 — D8's preamble and closing note now count six, commit f5752809.
<<<END_PAIR_B_FROM>>>

<<<PAIR_B_TO>>>
  Done: R-0255 (2026-08-10) — RESOLVED. The preamble reads "Run all six checks"
  and the closing note reads "recurred six times ... R20 hit four of them in one
  block", so the count a reviewer follows now matches the list they must run.
  Verified by the reviewer against the applied file, not the diff alone.
- R-0256 (Low, F105 R27): the segment manifest a flight-plan trace carries is
  composed a SECOND time at the call site. `apps/cli/commands/do_cmd.py` calls
  `compose_flight_plan_prompt(plan_intake_dict)` for the manifest while
  `plan_job_llm` composes the bytes it actually sends, and both reach
  `repo_facts_block()` independently. The trace's `prompt_text` is the effective
  prompt but its `segment_manifest` describes the reviewer-composed twin, so an
  audit row can describe bytes that were never sent if the two compositions
  differ. `make_intake_call_recorder` has the same shape, so the finding covers
  both sites. Cost today is bounded and visible: `prompt_chars` and
  `segment_manifest_chars` are both recorded, so a divergence shows up as a
  mismatch rather than a silent lie. Fix: compose ONCE — have the builder return
  or accept its `ComposedPrompt` so exactly one composition feeds both the
  provider and the trace. Needs a signature change on `plan_job_llm` and
  `run_intake`, so it is its own round. OPEN.
<<<END_PAIR_B_TO>>>

<<<PAIR_C_FROM>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0256.
<<<END_PAIR_C_FROM>>>

<<<PAIR_C_TO>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0257.
<<<END_PAIR_C_TO>>>

C3 — `append_trace_jsonl` and its tests (own commit)
  Apply PAIR_D to `packages/orchestration/prompt_trace.py` and PAIR_E to
  `tests/orchestration/test_prompt_trace.py`. Both are APPEND-shaped (TO
  contains FROM verbatim as its prefix): prove FROM exactly 1x plus the TO-only
  ADDED-LINE count from this commit's diff and the stray count, each grep
  SCOPED to its own file.

<<<PAIR_D_FROM>>>
def write_trace_jsonl(entries: list[PromptTraceEntry], path: Path) -> None:
    """Write prompt trace entries as JSONL (one JSON object per line)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for entry in entries:
            f.write(json.dumps(trace_entry_to_dict(entry)) + "\n")
<<<END_PAIR_D_FROM>>>

<<<PAIR_D_TO>>>
def write_trace_jsonl(entries: list[PromptTraceEntry], path: Path) -> None:
    """Write prompt trace entries as JSONL (one JSON object per line)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for entry in entries:
            f.write(json.dumps(trace_entry_to_dict(entry)) + "\n")


# Two writers, because the trace file is per JOB and not per run:
# `RunLogWriter.path.parent` is `<runs_root>/<job_id>/`, so a second command
# against the same job would truncate the first command's traces if it used
# `write_trace_jsonl`. The command that CREATES a job writes; a command that
# adds traces to a job that already has some appends (F105 R28).
def append_trace_jsonl(entries: list[PromptTraceEntry], path: Path) -> None:
    """Append prompt trace entries to a JSONL file, creating it if absent."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        for entry in entries:
            f.write(json.dumps(trace_entry_to_dict(entry)) + "\n")
<<<END_PAIR_D_TO>>>

<<<PAIR_E_FROM>>>
        assert "prompt_traces" in source
<<<END_PAIR_E_FROM>>>

<<<PAIR_E_TO>>>
        assert "prompt_traces" in source

    def test_appending_traces_keeps_the_earlier_ones(self, tmp_path):
        """A replan must not truncate the traces its job's first run wrote."""
        from packages.orchestration.prompt_trace import append_trace_jsonl

        composed = compose_intake_prompt("demo mission")
        first = build_trace_entry(
            prompt_text=composed.text, role="intake", composed_prompt=composed,
        )
        second = build_trace_entry(
            prompt_text=composed.text, role="flight_plan", composed_prompt=composed,
        )
        path = tmp_path / "prompt_trace.jsonl"
        write_trace_jsonl([first], path)
        append_trace_jsonl([second], path)
        lines = path.read_text().strip().split("\n")
        assert len(lines) == 2
        assert [json.loads(x)["role"] for x in lines] == ["intake", "flight_plan"]

    def test_appending_to_a_missing_file_creates_it(self, tmp_path):
        from packages.orchestration.prompt_trace import append_trace_jsonl

        composed = compose_intake_prompt("demo mission")
        entry = build_trace_entry(
            prompt_text=composed.text, role="flight_plan", composed_prompt=composed,
        )
        path = tmp_path / "nested" / "prompt_trace.jsonl"
        append_trace_jsonl([entry], path)
        assert len(path.read_text().strip().split("\n")) == 1

    def test_the_replan_path_records_and_appends_its_traces(self):
        """Wiring guard: an unwired or truncating replan fails HERE (F105 R28)."""
        import apps.cli.commands.do_cmd as do_cmd

        source = inspect.getsource(do_cmd)
        assert "replan_traces" in source
        assert "append_trace_jsonl" in source
        assert source.count("on_call=make_flight_plan_call_recorder(") == 2
<<<END_PAIR_E_TO>>>

C4 — the replan wiring (own commit)
  Apply PAIR_F and PAIR_G to `apps/cli/commands/do_cmd.py`. PAIR_F is a
  REWRITE: prove FROM 0x after and TO 1x. PAIR_G is APPEND-shaped: prove FROM
  exactly 1x plus the TO-only ADDED-LINE count and the stray count. Both greps
  SCOPED to `apps/cli/commands/do_cmd.py`.
  `provider="ollama"` mirrors the two call sites already in this file for the
  same reason: `make_structured_call_fn` is the ollama provider.

<<<PAIR_F_FROM>>>
    from packages.orchestration.flight_plan import (
        ReplanRejectedError,
        map_flight_plan_to_tasks,
        plan_job_llm,
        replan,
    )

    fp_result = plan_job_llm(intake, call_fn)
<<<END_PAIR_F_FROM>>>

<<<PAIR_F_TO>>>
    from packages.orchestration.flight_plan import (
        ReplanRejectedError,
        compose_flight_plan_prompt,
        make_flight_plan_call_recorder,
        map_flight_plan_to_tasks,
        plan_job_llm,
        replan,
    )

    replan_traces: list = []
    replan_composed = compose_flight_plan_prompt(intake)
    fp_result = plan_job_llm(
        intake,
        call_fn,
        on_call=make_flight_plan_call_recorder(
            replan_traces,
            replan_composed,
            provider="ollama",
            provider_kind="ollama",
        ),
    )
<<<END_PAIR_F_TO>>>

<<<PAIR_G_FROM>>>
    new_fp_dict["_normalization"] = fp_result.transformations
    job.flight_plan = new_fp_dict
    job.tasks = map_flight_plan_to_tasks(fp_result.plan)
    save_job(job)
<<<END_PAIR_G_FROM>>>

<<<PAIR_G_TO>>>
    new_fp_dict["_normalization"] = fp_result.transformations
    job.flight_plan = new_fp_dict
    job.tasks = map_flight_plan_to_tasks(fp_result.plan)
    save_job(job)

    # APPEND, never write: this job's first run already left its intake and
    # flight-plan traces in the same per-job file (F105 R28).
    if replan_traces:
        from packages.orchestration.prompt_trace import append_trace_jsonl
        from packages.orchestration.run_log import RunLogWriter
        log = RunLogWriter(job_id=job.id)
        try:
            append_trace_jsonl(replan_traces, log.path.parent / "prompt_trace.jsonl")
        except OSError:
            pass
<<<END_PAIR_G_TO>>>

C5 — plan and handoff (own commit)
  Apply PAIR_H to `.agent/plan.md` as a FULL replacement, then rewrite
  `.agent/handoff.md`.

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
T001 and T002 are DONE and gated. T003's six migration sites are all migrated,
each under its own golden. R27 is GATED; `LAST_REVIEWED_SHA` is 73259d7a.
R28 is a SPLIT round: it records the R27 gate, resolves R-0255, registers
R-0256, and closes the last `do_cmd` evidence gap by adding
`append_trace_jsonl` beside `write_trace_jsonl` and wiring the replan site with
it — the per-job trace file must not be truncated by a second command.
Open findings: R-0221, R-0239, R-0246, R-0247, R-0256.
No PR; one is created at CLOSURE.

## Next Steps
- `on_call` for the mission and orchestrator prompts — `mission_cmd.py:187`,
  `mission_cmd.py:362`, `gauntlet_runner.py:505`. None has an evidence sink
  today, so each needs its sink named before it is wired.
- Fix R-0246 in the round that next touches `mission_compiler.py`.
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
  A transport: `sha256sum` on `.agent/authored/f105-r28-1.md` and
    `.agent/last_block.md`; `cmp` them. Digest in the handback.
  B size: `wc -l .agent/authored/f105-r28-1.md`. Report the number even if it
    is under the cap.
  C application, each grep SCOPED to the named file:
    REWRITES, prove FROM 0x after and TO 1x — PAIR_B, PAIR_C in
    `.agent/live_review.md`; PAIR_F in `apps/cli/commands/do_cmd.py`.
    APPENDS, prove FROM exactly 1x plus the TO-only ADDED-LINE count from
    `git show --numstat <commit> -- <path>` and the stray count — PAIR_A in
    `.agent/live_review.md`; PAIR_D in `packages/orchestration/prompt_trace.py`;
    PAIR_E in `tests/orchestration/test_prompt_trace.py`; PAIR_G in
    `apps/cli/commands/do_cmd.py`. Do NOT use whole-file counts for an append.
    PAIR_H: `cmp` the applied `.agent/plan.md` against the sliced PAIR_H;
    `wc -l .agent/plan.md` must be under 50.
  D marker leakage, LINE-anchored: `grep -c -E '^<<<'` in
    `.agent/live_review.md`, `.agent/plan.md`,
    `packages/orchestration/prompt_trace.py`, `apps/cli/commands/do_cmd.py` and
    `tests/orchestration/test_prompt_trace.py` — each count must be 0. The count
    is over marker LINES on purpose: pair bodies quote marker names in prose and
    a substring count would be counting this block's own text (D8 item 2).
  E the touched suite: `python3 -m pytest tests/orchestration/test_prompt_trace.py -q`.
  F red-proof M1, in a DISPOSABLE `git worktree` at HEAD and nowhere else:
    change `append_trace_jsonl`'s `path.open("a")` to `path.open("w")` and run
    `python3 -m pytest tests/orchestration/test_prompt_trace.py -q`. It MUST go
    RED on `test_appending_traces_keeps_the_earlier_ones`.
  G red-proof M2, in the SAME disposable worktree, after reverting M1: delete
    the `on_call=make_flight_plan_call_recorder(...)` argument from the REPLAN
    call only, leaving the R27 site untouched, and re-run the same file. It MUST
    go RED on `test_the_replan_path_records_and_appends_its_traces`. Then remove
    and prune the worktree. For either red-proof, if it comes out GREEN do NOT
    edit anything to force a red — report the green as a declared deviation.
  H module regression: `python3 -m pytest tests/orchestration/ -q` and
    `python3 -m pytest tests/cli/ -q`.
  I contract tests and canary: `python3 -m pytest tests/docs/ -q`,
    `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q`, and
    `python3 -m pytest tests/cli/test_golden_path.py -q`.
  J hygiene: `git status --porcelain` empty; `git worktree list` the primary
    alone; `git log --numstat 73259d7a..HEAD` with the `+` column per commit.
Handback:    completion report + rewrite `.agent/handoff.md` (changed-files
             table one row per path, item-status table over
             C1a/C1b/C2/C3/C4/C5, the gate table with REAL exit codes and REAL
             output, transport and pair proofs, both red-proof results,
             open-findings count, next action). Keep it under 60 lines, or carry
             a DECISION D15 "Deviations, declared" line naming the real count
             and the mandated content that caused the overage. Then push. Do NOT
             create a PR.
──────────────────────────────────────────────────────────────
