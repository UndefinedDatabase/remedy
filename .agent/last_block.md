── STEP R41 — F105 ───────────────────────────────────────────
Goal:        Persist the R40 reviewer gate, register R-0264 (the §4.13
             session-versus-branch misreading that left R40's four commits
             ungated), land R39's two tests in their CORRECTED form so R-0263
             is fixed, and finish R-0256 by handing the composition down at all
             three `apps/cli/commands/do_cmd.py` call sites.
Bundle:      C1 save this block · C2 every `.agent/live_review.md` gate edit ·
             C3 the two orchestration tests · C4 the three CLI call sites plus
             their wiring guard · C5 the two `Landed:` lines, plan and handoff.
Change:      `.agent/authored/f105-r41-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `tests/orchestration/test_intake.py`,
             `tests/orchestration/test_flight_plan.py`,
             `apps/cli/commands/do_cmd.py`,
             `tests/orchestration/test_prompt_trace.py`, `.agent/plan.md`,
             `.agent/handoff.md`. Nothing else — no `docs/`, no `packages/`.
Constraints: `.agent/STOP` is ABSENT and stays that way; do not create it. The
             three CLI keywords go on their OWN line each: the suite counts
             `on_call=make_flight_plan_call_recorder(` over the WHOLE of
             `do_cmd.py` and that count must stay 2. Write no `Done:` paragraph
             of your own — `Landed:` only (§4.4). Every red-proof runs ONLY
             inside a disposable `git worktree`; the primary checkout is
             `git status --porcelain` EMPTY at the handback.
Done when:   every gate below is run and its REAL exit code recorded.

C1 — save this block verbatim, TWO commits
  C1a `cp /home/decodeux/Repos/remedy/.remedy-wt/f105-r41-1.block.md`
      `.agent/authored/f105-r41-1.md`. Commit it ALONE.
  C1b `cp` the same bytes to `.agent/last_block.md`. Commit separately.
  `sha256sum` all three plus `cmp`; digest in the handback.

C2 — `.agent/live_review.md`, ONE commit
  Apply PAIR_ID (REWRITE, the header's next-free-ID line), PAIR_F
  (CONTAINS-FROM, R-0264 appended at the end of `## Findings`) and PAIR_S
  (CONTAINS-FROM, the R40 gate record plus the R41 step line at the END of the
  file). All three share ONE path in ONE commit: reconcile them TOGETHER
  against that commit's `git show -U0`.

C3 — the two tests, ONE commit
  Apply PAIR_TI and PAIR_TF, CONTAINS-FROM appends at the END of their files.
  These are R39's C4 items in the form R-0263 proved correct: the assertion is
  `startswith`, not equality, because `run_structured_call` hands `call_fn` the
  schema-decorated prompt and not `base_prompt` itself.

C4 — the three CLI call sites plus their guard, ONE commit
  Apply PAIR_DO1, PAIR_DO2 and PAIR_DO3 to `apps/cli/commands/do_cmd.py`
  (REWRITEs — each inserts one keyword line INSIDE its FROM, so the FROM string
  no longer occurs afterwards) and PAIR_GUARD to
  `tests/orchestration/test_prompt_trace.py` (CONTAINS-FROM). PAIR_DO2 also
  replaces the comment that describes the second composition, which this commit
  makes false.

C5 — markers, plan and handoff, ONE commit
  In `.agent/live_review.md`, directly BELOW the last line of the R-0263 entry
  and directly BELOW the last line of the R-0256 entry, append ONE line each in
  YOUR OWN words, of the form `  Landed: R-XXXX — <what changed, which commit>`.
  Two lines total, nothing more; no `Done:` paragraph (§4.4). Then apply
  PAIR_P_PLAN to `.agent/plan.md` as a FULL replacement and rewrite
  `.agent/handoff.md` in your own words per AGENTS.md.

<<<PAIR_ID_FROM>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0264.
<<<END_PAIR_ID_FROM>>>

<<<PAIR_ID_TO>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0265.
<<<END_PAIR_ID_TO>>>

<<<PAIR_F_FROM>>>
  own test. Whoever runs R40 lands that corrected form. OPEN.
<<<END_PAIR_F_FROM>>>

<<<PAIR_F_TO>>>
  own test. Whoever runs R40 lands that corrected form. OPEN.

- R-0264 (Low, F105 R40, reviewer-authored defect): the R40 step line applies
  §4.13 — "the LAST round of a BRANCH has no on-disk gate entry" — to the last
  round of a SESSION. The two are not the same boundary. A session that ends
  mid-branch against `.agent/STOP` leaves a round that the NEXT session can and
  must gate, and R40 left four commits (4149021f, 0dd0b104, 7f3b0ba5, 7f622b7f)
  carrying a line that tells the next reader no gate entry is coming. The next
  session nearly skipped them on exactly that reading. §4.13's terminator
  applies once per BRANCH, at closure, where no later round exists to write the
  record; every other unreviewed round is an ordinary handback. Cost so far:
  nil — this round gates R40 — but the line would have cost a real gate on any
  branch resumed by a reader who trusted it. Fix: the R40 line says the session
  closed with its own round ungated and awaiting the next session, and the
  gate below supplies it. OPEN.
<<<END_PAIR_F_TO>>>

<<<PAIR_S_FROM>>>
  lives in `.agent/handoff.md` and the session's completion report.
<<<END_PAIR_S_FROM>>>

<<<PAIR_S_TO>>>
  lives in `.agent/handoff.md` and the session's completion report.
  That reading was wrong and is registered as R-0264: R40 ended a SESSION, not
  the BRANCH, so the round stayed gateable and the next session gated it below.
- Reviewer gate on R40 (2026-08-10, by the session that resumed the branch):
  PASS. Range `c44a582c..7f622b7f` = four commits, five paths, every one under
  `.agent/`; nothing under `packages/`, `apps/`, `tests/` or `docs/`.
  Insertions per commit 220, 145, 59 and 82, each far under 500.
  Transport by the PRIMARY shape: `.remedy-wt/f105-r40-1.block.md`, the
  committed `.agent/authored/f105-r40-1.md` and `.agent/last_block.md` all
  three hash to
  `dd655c7b424259199977a4b402e2a52ea40e2ca4dd78f31f083c554e6995376e`
  at 220 lines against D5's cap of 400; the `cmp` run is silent.
  Content re-read against the applied file, not the handback: the ID line
  reads R-0264, the R-0263 entry is present and OPEN, and the R39 step line
  carries its correction. The commit removes exactly four lines, all of them
  FROM text, so both stray counts are 0.
  Gates re-run by THIS reviewer, none taken from the handback: `tests/docs/`
  `294 passed in 0.26s`; `test_dashboard_contract.py` `70 passed in 4.44s`;
  the canary `42 passed in 19.86s`. `.agent/plan.md` is 41 lines against the
  cap of 50 and keeps `## Goal` and a `Steps` substring; `.agent/live_review.md`
  keeps exactly one `## Steps` heading; `^<<<` is 0 in live_review, plan and
  handoff. `.agent/handoff.md` is 97 lines and carries its DECISION D15
  stated-cause line, so the overage is declared, not silent.
  `LAST_REVIEWED_SHA` advances c44a582c -> 7f622b7f.
- R41: SPLIT round — record the R40 gate, register R-0264, and land BOTH halves
  of the work R39 and R40 left open: the two corrected tests that fix R-0263,
  and the three `do_cmd.py` call sites plus a wiring guard that fix R-0256.
  Both changes were red-proofed by the reviewer in disposable worktrees at
  7f622b7f before this block was authored.
<<<END_PAIR_S_TO>>>

<<<PAIR_TI_FROM>>>
        fn("test prompt", 0)
        assert captured["chat_kwargs"]["model"] == "intake-test-model"
<<<END_PAIR_TI_FROM>>>

<<<PAIR_TI_TO>>>
        fn("test prompt", 0)
        assert captured["chat_kwargs"]["model"] == "intake-test-model"


class TestRunIntakeAcceptsAComposedPrompt:
    """R-0256: one composition feeds the provider AND the trace manifest."""

    def test_composed_text_is_the_prefix_the_provider_sees(self):
        from packages.orchestration.intake import compose_intake_prompt

        composed = compose_intake_prompt("SENTINEL-INTAKE-MISSION")
        seen: list[str] = []

        def _call(prompt: str, attempt: int) -> str:
            seen.append(prompt)
            return json.dumps(_VALID_INTAKE)

        run_intake("a completely different mission", _call, composed=composed)

        assert len(seen) == 1
        assert seen[0].startswith(composed.text)
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

    def test_composed_text_is_the_prefix_the_provider_sees(self):
        from packages.orchestration.flight_plan import compose_flight_plan_prompt

        composed = compose_flight_plan_prompt(
            {"goal": "SENTINEL-PLAN-GOAL"}, project_facts="pinned facts",
        )
        seen: list[str] = []

        def _call(prompt: str, attempt: int) -> str:
            seen.append(prompt)
            return _valid_plan_json(3)

        plan_job_llm(_fake_intake(), _call, composed=composed)

        assert len(seen) == 1
        assert seen[0].startswith(composed.text)
        assert "SENTINEL-PLAN-GOAL" in seen[0]
        assert "Add a login page" not in seen[0]
<<<END_PAIR_TF_TO>>>

<<<PAIR_DO1_FROM>>>
            intake_result = run_intake(
                mission,
                call_fn,
                on_call=make_intake_call_recorder(
<<<END_PAIR_DO1_FROM>>>

<<<PAIR_DO1_TO>>>
            intake_result = run_intake(
                mission,
                call_fn,
                composed=intake_composed,
                on_call=make_intake_call_recorder(
<<<END_PAIR_DO1_TO>>>

<<<PAIR_DO2_FROM>>>
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
<<<END_PAIR_DO2_FROM>>>

<<<PAIR_DO2_TO>>>
        # Composed exactly ONCE here and handed to `plan_job_llm`, so the bytes
        # the provider receives and the manifest the trace records come from the
        # same composition — `prompt_chars` and `segment_manifest_chars` can no
        # longer describe two different prompts (R-0256).
        plan_composed = compose_flight_plan_prompt(plan_intake_dict)
        fp_result = plan_job_llm(
            plan_intake_dict,
            plan_call_fn,
            composed=plan_composed,
            on_call=make_flight_plan_call_recorder(
<<<END_PAIR_DO2_TO>>>

<<<PAIR_DO3_FROM>>>
    fp_result = plan_job_llm(
        intake,
        call_fn,
        on_call=make_flight_plan_call_recorder(
<<<END_PAIR_DO3_FROM>>>

<<<PAIR_DO3_TO>>>
    fp_result = plan_job_llm(
        intake,
        call_fn,
        composed=replan_composed,
        on_call=make_flight_plan_call_recorder(
<<<END_PAIR_DO3_TO>>>

<<<PAIR_GUARD_FROM>>>
        assert source.count("on_call=make_flight_plan_call_recorder(") == 2
<<<END_PAIR_GUARD_FROM>>>

<<<PAIR_GUARD_TO>>>
        assert source.count("on_call=make_flight_plan_call_recorder(") == 2

    def test_every_cli_call_site_hands_its_composition_down(self):
        """R-0256 wiring guard: a site that composes twice fails HERE."""
        import apps.cli.commands.do_cmd as do_cmd

        source = inspect.getsource(do_cmd)
        assert "composed=intake_composed," in source
        assert "composed=plan_composed," in source
        assert "composed=replan_composed," in source
<<<END_PAIR_GUARD_TO>>>

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
R41 landed. T001 and T002 are DONE and gated; T003's six migration sites are
all migrated. R40 is GATED PASS; `LAST_REVIEWED_SHA` is 7f622b7f. R-0256 and
R-0263 are FIXED and marked `Landed:`, awaiting the reviewer's `Done:` text at
the R41 gate: one composition now feeds both the provider and the trace at all
three CLI sites, pinned by two orchestration tests and one wiring guard.
Open findings: R-0221, R-0239, R-0247, R-0262, R-0264.
No PR; one is created at CLOSURE.

## Next Steps
- Await the R41 gate, which resolves R-0256, R-0263 and R-0264.
- Then T004: `remedy stats cache` over actuals — the cache-read share per role
  read from recorded calls, not from an estimate.
- Then the integration gate (docs/agents/integration_gate.md); R-0221 will
  attribute phantom base-only failures there and that is expected, not new.
- Then closure (docs/roadmap/STATUS_closure_protocol.md), where the evidence
  job, the FRESH review zip, the STATUS line and the PR all land.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- R-0262 stays OPEN and out of scope: it needs the composition moved inside the
  `try` in `plan_job_llm` AND at the CLI sites, pinned by a raising composer.
<<<END_PAIR_P_PLAN>>>

GATES — run every one, record the REAL exit code in the handback

A transport
  `sha256sum .remedy-wt/f105-r41-1.block.md .agent/authored/f105-r41-1.md
  .agent/last_block.md` — all three EQUAL; two `cmp` runs, both silent.

B size
  `wc -l .agent/authored/f105-r41-1.md` against the cap of 400 (D5).

C pair shapes, MEASURED not assumed
  Slice every pair from the COMMITTED `.agent/authored/f105-r41-1.md` with a
  whole-line marker reader; never retype. Verify FIRST that every FROM occurs
  exactly 1x in its target before its write, and STOP if one does not. Then:
  PAIR_ID, PAIR_DO1, PAIR_DO2 and PAIR_DO3 are REWRITEs — FROM 0x, TO 1x after
  the write. PAIR_F, PAIR_S, PAIR_TI, PAIR_TF and PAIR_GUARD are CONTAINS-FROM
  — FROM 1x, TO 1x. PAIR_P_PLAN: `cmp` the applied `.agent/plan.md` against the
  slice, `wc -l` against the cap of 50.
  A declared shape that does not equal the measured shape is a STOP.

D added-line reconciliation for C2, C3 and C4
  For each of those three commits run `git show -U0 <commit>`: every ADDED line
  appears in some TO of that commit, every REMOVED line is a FROM. Both stray
  counts must be 0 for all three.

E marker leakage
  `^<<<` line count is 0 in `.agent/live_review.md`, `.agent/plan.md`,
  `.agent/handoff.md`, `apps/cli/commands/do_cmd.py` and all three touched test
  files. Report the numbers, not the word.

F state-file contracts
  `python3 -m pytest tests/docs/ -q` and
  `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q`.
  `.agent/plan.md` keeps `## Goal` and a `Steps` substring;
  `.agent/live_review.md` keeps exactly one `## Steps` heading.

G scope
  `git diff --name-only 7f622b7f..HEAD` lists EXACTLY these nine paths and no
  others: the two `.agent/authored`/`last_block` saves, `.agent/live_review.md`,
  `.agent/plan.md`, `.agent/handoff.md`, `tests/orchestration/test_intake.py`,
  `tests/orchestration/test_flight_plan.py`,
  `tests/orchestration/test_prompt_trace.py`, `apps/cli/commands/do_cmd.py`.
  Report the list. Nothing under `packages/` or `docs/`.

H scoped suite, after C4
  `python3 -m pytest tests/orchestration/test_intake.py
  tests/orchestration/test_flight_plan.py tests/orchestration/test_prompt_trace.py
  tests/cli/test_do_cmd_cli_path.py -q`. Report the count and the time.

I canary
  `python3 -m pytest tests/cli/test_golden_path.py -q`.

J red-proofs, THREE of them, in a DISPOSABLE worktree only
  `git worktree add .remedy-wt/r41-red HEAD` after C4. Inside that worktree,
  one at a time and reverting between them, report the FAILED test name each
  time — three separate runs of the scoped pair
  `tests/orchestration/test_intake.py tests/orchestration/test_flight_plan.py`
  or `tests/orchestration/test_prompt_trace.py` as appropriate:
  J1 in `packages/orchestration/intake.py`, replace
     `composed.text if composed is not None else _build_intake_prompt(mission),`
     with `_build_intake_prompt(mission),` — expect the new intake test RED.
  J2 in `packages/orchestration/flight_plan.py`, replace
     `prompt = composed.text if composed is not None else _build_plan_prompt(intake)`
     with `prompt = _build_plan_prompt(intake)` — expect the new flight-plan
     test RED.
  J3 in `apps/cli/commands/do_cmd.py`, DELETE the line `composed=plan_composed,`
     — expect `test_every_cli_call_site_hands_its_composition_down` RED.
  Then `git worktree remove .remedy-wt/r41-red --force` and `git worktree prune`.
  If any of the three comes back GREEN, that is a STOP and a declared
  deviation, not something to fix by editing the test.

K hygiene
  `git status --porcelain` EMPTY — `.agent/STOP` is gone and must not return.
  `git worktree list` shows the primary ALONE. Per-commit insertions each under
  500 via `git show --numstat`.

Handback: completion report + rewrite `.agent/handoff.md` (changed-files table,
item-status table for C1a/C1b/C2/C3/C4/C5, the gate table with real exit codes,
the transport and pair proofs, the three red-proof results, open-findings count,
and the next expected action). Then `git push`. Do NOT create a PR — the PR is
created at CLOSURE only.
──────────────────────────────────────────────────────────────
