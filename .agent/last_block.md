STEP T003 PART 3 (WIRE THE REAL CONFIRM CALL) / ROUND 8 - F114 Cost preview per command
FEATURE F114 - Cost preview per command (Tier 3) - SESSION 2, ROUND 8

Goal
  Book round 7's PASS verdict into the ledger (RECORD7) and wire the real
  confirm_cost_preview() call into _cmd_job_run_cycles
  (apps/cli/commands/job.py), gating both the single-cycle short-circuit
  and the full run_cycles path with an honest "estimate unavailable"
  CostBandEstimate. Repair the existing _cmd_job_run_cycles call sites in
  tests/orchestration/test_long_run_executor.py and
  tests/orchestration/test_escalation.py that would otherwise trip the
  new gate under pytest's non-tty stdin, and add two new tests for the
  gate itself.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f114-r8.md
  C0b mirror it to .agent/last_block.md
  C1  apply RECORD7 to .agent/live_review.md (append) and PLAN8 to
      .agent/plan.md (whole-file replacement)
  C2  apply SIG PAIR, GATE PAIR and HANDLER PAIR to
      apps/cli/commands/job.py; TLRE1, TLRE2, TLRE3, TLRE4 and NEWTESTS
      PAIRs to tests/orchestration/test_long_run_executor.py; ESC1 and
      ESC2 PAIRs to tests/orchestration/test_escalation.py
  C3  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f114-r8.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md (C1) - .agent/plan.md (C1) -
  apps/cli/commands/job.py (C2) -
  tests/orchestration/test_long_run_executor.py (C2) -
  tests/orchestration/test_escalation.py (C2) - .agent/handoff.md (C3)

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by
     delimiter index from the COMMITTED .agent/authored/f114-r8.md -
     marker lines EXCLUDED - and write it with a script, never by
     retyping. If a slice looks wrong, apply it as written and DECLARE it
     in the handback.
  2. C1 is the first substantive commit of the round.
  3. RECORD7 appends to .agent/live_review.md as EXACTLY ONE newline byte
     followed by the slice (the file's own current convention, same as
     every prior round's own G2 measurement). PLAN8 REPLACES
     .agent/plan.md whole.
  4. NEWLINE CONVENTION, STATED EXPLICITLY: RECORD7 and PLAN8 carry NO
     trailing newline of their own. Every one of the ten pairs' FROM/TO
     text (SIG, GATE, HANDLER, TLRE1-4, NEWTESTS, ESC1-2) carries its OWN
     trailing newline as the true last byte of the matched line group - a
     byte-exact structural suffix of the file, not marker-line
     formatting (same class as every prior round's own code pairs).
  5. ALL TEN PAIRS ARE REWRITES except NEWTESTS, which IS AN APPEND (its
     TO begins with its FROM verbatim, then continues with two new test
     methods). For EACH pair: verify FROM count is exactly 1 in its
     target file before C2, apply str.replace(FROM, TO, 1), and confirm
     "TO contains FROM: true" for NEWTESTS and "TO contains FROM: false"
     for the other nine - do not assume either way, recheck mechanically
     (a prior round's own draft-time self-check on a superficially
     similar insert-between shape got this wrong via a comparison typo;
     this block's own classification was verified with the real target
     files before being written).
  6. Apply to apps/cli/commands/job.py in this order: SIG PAIR, then GATE
     PAIR, then HANDLER PAIR - SIG PAIR's FROM is the function signature
     (nearest the top of the three), GATE PAIR's FROM sits inside the
     function body below it, and HANDLER PAIR's FROM is the
     COMMAND_HANDLERS dict entry far below both; none of the three FROMs
     overlaps another's TO, so this order is for readability of the
     round's own narrative, not correctness, but follow it as written.
     Apply to tests/orchestration/test_long_run_executor.py in this
     order: TLRE1, TLRE2, TLRE3, TLRE4, then NEWTESTS (NEWTESTS's own
     FROM sits after all four TLRE call sites in the file and is
     unaffected by their edits, since none of the four touches the lines
     NEWTESTS anchors to). Apply ESC1 then ESC2 to
     tests/orchestration/test_escalation.py.
  7. GATE PAIR inserts the confirm call BEFORE `if resolved.max_cycles <=
     1:` so BOTH the single-cycle short-circuit and the full run_cycles
     path are gated by the same one confirmation - the feature spends
     money either way. The estimate is deliberately
     CostBandEstimate(None, None, ESTIMATE_UNAVAILABLE, {}): job.run has
     no per-task class data before it starts (investigated and confirmed
     absent this round's own predecessor round), so an honest "unavailable"
     label is correct per A9 rather than a fabricated band. `yes=(yes or
     unattended)` maps --unattended to skip-prompt because the feature
     doc requires unattended runs to never prompt and rely on budgets
     instead - this is not a workaround, it is the feature's own stated
     design.
  8. TLRE1-4 and ESC1-2 each add `, yes=True` to an EXISTING call site of
     _cmd_job_run_cycles that tests unrelated behavior (capping,
     multi-cycle looping, escalation blocking) and does not already pass
     unattended=True - found by the reviewer's own investigation BEFORE
     this block was authored: under pytest, stdin is not a tty, so
     without yes/unattended these calls would hit the new gate's
     EXIT_USAGE exit instead of reaching the behavior they actually
     test. Every other pre-existing call site in both files either
     already passes unattended=True or is fully monkeypatched
     (_cmd_job_run_cycles itself replaced with a stub) and is UNTOUCHED
     by this round - do not edit any call site not named by a pair
     above.
  9. NEWTESTS adds exactly two methods to TestJobRunCommand
     (tests/orchestration/test_long_run_executor.py): one proving a
     decline (confirm_cost_preview monkeypatched to return False) returns
     without calling _cmd_run_next_task_local and prints "Cancelled.
     Nothing was run.", one proving the gate is called with an
     unavailable estimate and yes=True when unattended=True. Do not add
     these tests anywhere else or duplicate them.
  10. Do NOT touch apps/cli/command_catalog.py, packages/orchestration/
      cost_preview.py, or apps/cli/cost_preview_confirm.py this round -
      all three already carry what this round needs (is_expensive,
      --yes, resolve_confirm_above_usd, ESTIMATE_UNAVAILABLE,
      CostBandEstimate, confirm_cost_preview) from rounds 5-7. Do NOT
      touch tests/orchestration/test_resume_kill.py or
      tests/orchestration/test_resume_cli.py - both fully monkeypatch
      _cmd_job_run_cycles and are unaffected by this round (confirmed by
      the reviewer's own investigation).
  11. ruff is DENIED to this session (measured at every round since
      F114's claim); gate with `python3 -m py_compile` on all three
      touched .py files instead, and ATTEMPT `ruff check` on
      apps/cli/commands/job.py, reporting the real output or the exact
      refusal text - never assume either way.
  12. A sentence OUTSIDE the change set that this round makes stale is
      DECLARED in the handback and NOT repaired. Rounds 2 and 3's own
      `.agent/context.md` declarations (lines 29 and 36) stand; do not
      repeat them.
  13. Read .agent/STOP from disk before the first commit and again
      before C3. If it exists, finish the commit in hand, write the
      handback, and stop.
  14. Self-review loop before every commit (git diff --stat, git diff).
      Push after C3. No pull request, no merge this round - the real
      confirm wiring landing does not by itself trigger the Open PR
      Gate; that waits for goldens, docs and the acceptance fixtures.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f114-r8.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE LEDGER APPEND. Base size of .agent/live_review.md immediately
     BEFORE C1 (measure it yourself): report its byte length and whether
     it ends with a trailing newline. RECORD7 has ZERO internal
     newlines - report its own byte length. Report: base + 1 +
     len(RECORD7) and whether that equals the post-C1 file's byte length
     (expected 2375218, from a base of 2371519
     and a RECORD7 of 3698 bytes - recompute both independently).
     Then the SECOND reader: report whether the post-C1 file's bytes from
     `base` to the end equal exactly `"\n" + RECORD7`. Then a NEGATIVE
     CONTROL in a scratch copy ONLY (never the tracked file): flip one
     byte inside RECORD7's own text and report the second reader REJECTS it.
  G3 THE PLAN. Extract PLAN8 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md            -> exit 0
       wc -l .agent/plan.md                      -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G4 THE TEN PAIRS. For EACH pair (SIG, GATE, HANDLER, TLRE1, TLRE2,
     TLRE3, TLRE4, NEWTESTS, ESC1, ESC2): report the FROM count in its
     target file immediately BEFORE C2 (must be exactly 1 for all ten -
     for the three pairs sharing apps/cli/commands/job.py, re-count each
     remaining pair's FROM AFTER the previous pair in constraint 6's
     order is applied; same for the five pairs sharing
     test_long_run_executor.py), and after C2 report the containment
     test's own output in these words - "TO contains FROM: true" or "TO
     contains FROM: false" - matching constraint 5 exactly (NEWTESTS
     reports "true"; the other nine report "false"). Then extract each
     slice from the COMMITTED authored file and cmp each target file's
     actual new content against what applying its pairs' str.replace
     calls, in constraint 6's order, to a pre-C2 scratch copy of that
     target produces - exit 0 for all three target files.
  G5 COMPILE AND LINT. `python3 -m py_compile` on
     apps/cli/commands/job.py, tests/orchestration/test_long_run_executor.py
     and tests/orchestration/test_escalation.py -> exit 0 each. Then
     ATTEMPT `ruff check apps/cli/commands/job.py` and report the real
     result, success or refusal text, verbatim.
  G6 THE RED-PROOF, INSIDE A DISPOSABLE GIT WORKTREE ONLY (never the
     primary checkout - self_drive_protocol.md guardrail G5). After C2,
     from the round's own HEAD: create a scratch worktree, inside it
     invert GATE PAIR's own new `if not confirm_cost_preview(` to `if
     confirm_cost_preview(` (a one-word removal, flips decline/approve),
     then run
       python3 -m pytest tests/orchestration/test_long_run_executor.py -q
     and report the failure count (must be greater than zero - name
     which tests failed; expect at least the two new NEWTESTS methods
     plus any pre-existing test whose call site now passes yes=True and
     relies on the run actually proceeding). Then revert the edit inside
     that same worktree, re-run the same command and report it fully
     green again (76 passed - the unmutated control: 74 pre-existing +
     2 new). Remove the worktree when done (`git worktree remove
     --force`) - it must not exist at G8's tree check.
  G7 THE SUITES, EACH AS ITS OWN INVOCATION, RUN SERIALLY, IN THE PRIMARY
     CHECKOUT:
       python3 -m pytest tests/orchestration/test_long_run_executor.py -q
       python3 -m pytest tests/orchestration/test_escalation.py -q
       python3 -m pytest tests/orchestration/test_resume_kill.py tests/orchestration/test_resume_cli.py -q
       python3 -m pytest tests/test_no_interactive_guard.py -q
       python3 -m pytest tests/test_command_catalog.py tests/cli/test_command_catalog.py -q
       python3 -m pytest tests/docs/ -q
       python3 -m pytest tests/orchestration/test_roadmap_index.py -q
       python3 -m pytest tests/ui_server/ -q
       python3 -m pytest tests/orchestration/test_test_runner.py -q
       python3 -m pytest tests/regression/test_resource_safety.py -q
       python3 -m pytest tests/orchestration/test_integrity_gate.py -q
       python3 -m pytest tests/cli/test_golden_path.py -q
     Report each pass count. THE STATE READERS
     (tests/ui_server/, test_test_runner.py, test_resource_safety.py,
     test_integrity_gate.py) ARE RUN AS ALL FOUR NAMED HERE, NOT FEWER.
     The last is the canary. test_long_run_executor.py is expected at 76
     passed (74 existing + 2 new); test_escalation.py is expected at 68
     passed (unchanged count, only yes=True added to two call sites);
     test_resume_kill.py + test_resume_cli.py together are expected at
     42 passed (both fully monkeypatch _cmd_job_run_cycles or bypass it
     entirely via a child subprocess calling run_cycles directly, per
     constraint 10 - unaffected); test_no_interactive_guard.py is
     expected at 6 (apps/cli stays outside its scan scope); every other
     count is a moved-count check against the reviewer's own independent
     base reading - report what you actually measured, not what you
     expect.
  G8 THE TREE, THE COMMITS AND THE SWEEP. Read git status --porcelain
     immediately before C3 is staged, and git ls-files .remedy-wt (no
     output). Confirm `git worktree list` shows no leftover scratch
     worktree from G6. Then, for C0a, C0b, C1 and C2 - the commits BEFORE
     the handback commit - report each one's insertion count from git
     show --numstat, the '+' column ONLY, and compare it CELL BY CELL
     against the Commits table of the handback you are writing. C3's own
     numbers go to NEITHER a round report NOR this file. Then THE
     STALENESS SWEEP over every file this round touched, one entry per
     file, stale or NOT stale, why.

Handback
  Rewrite .agent/handoff.md per docs/agents/handback_template.md. It
  carries the SESSION NUMBER of the running feature - this is SESSION 2
  of F114 - the state block, the item-status table with every ordered
  item appearing exactly once, the Commits table, one line per gate
  followed by the transcripts, the deviations, and the next steps. It has
  no length cap.

SLICES. Each slice lies between its own one-line BEGIN and END marker.
The marker lines are NEVER part of the slice. The slices carried here are
RECORD7, PLAN8, SIG PAIR FROM/TO, GATE PAIR FROM/TO, HANDLER PAIR
FROM/TO, TLRE1-4 PAIR FROM/TO, NEWTESTS PAIR FROM/TO and ESC1-2 PAIR
FROM/TO.

<<<BEGIN RECORD7>>>
Gate: F114 R7 — the round 7 entry, adds a --yes ArgDef to job.run's own CommandEntry and its catalog test (T003 continued), no ledger findings. VERDICT PASS, over the range `a886072b844566fb40757c036f8750e3a4f39090..1f9797ab92bcbceea5c54450154edb5ffdb5d4ae` (commits C0a `e83309b1fce6177a6b97955987e17b07a640a0c3`, C0b `20a613598f54224a38176181e49eaa5de1315d8b`, C1 `3d37b1b952fbd9441b718429b3b05b518fc0372d`, C2 `7c25fe18e7dae52d5b6229aab25906b5facdc5ad` — four real content commits — plus handback commit `1f9797ab92bcbceea5c54450154edb5ffdb5d4ae`), independently re-verified by the reviewer. TRANSPORT HELD: `sha256sum .agent/authored/f114-r7.md .agent/last_block.md` both print `69c8767c2530932c17d8c432ff47487cc0868e13dade4c0986a2891ed3ff0b94`, reproduced directly. G2 THE LEDGER APPEND HELD: base 2367783 bytes (no trailing newline), RECORD6 3735 bytes, base + 1 + 3735 = 2371519, matching the post-C1 file's measured length exactly; the second reader's tail slice equalled `\n` + RECORD6 byte for byte, and a one-byte-flipped negative control was correctly rejected — all reproduced independently. G3 THE PLAN HELD BYTE-EXACT: PLAN7 extracted from the committed authored file `cmp`s exit 0 against `.agent/plan.md` (49 lines, under 50; `## Goal`/`## Next Steps` each exactly once), reproduced independently. G4 THE TWO PAIRS HELD: the reviewer independently reconstructed `apps/cli/command_catalog.py` and `tests/test_command_catalog.py` by applying YES_ARG PAIR and YES_TEST PAIR respectively to pre-C2 scratch copies, and found both byte-identical to the real committed files — both pairs correctly classified as rewrites (`TO contains FROM: false` for both). G5 HELD: `python3 -m py_compile` exit 0 on both files, reproduced; `ruff check` produced the same session-level denial text every prior round has quoted, reproduced verbatim. G6 THE RED-PROOF HELD, REPRODUCED INDEPENDENTLY IN A SEPARATE DISPOSABLE WORKTREE: removing the new `--yes` ArgDef from job.run's own args tuple produced the identical single failing test the worker reported (`TestCatalogExpensive::test_job_run_has_a_yes_flag_to_skip_the_cost_confirmation`), proving the arg is real catalog data; reverted, 22 passed again; worktree removed after. G7 THE SUITES, REPRODUCED INDEPENDENTLY BY THE REVIEWER at this round's own HEAD, all ten counts identical to the worker's own reading: `test_command_catalog.py` 22, `test_command_catalog.py` (cli) 23, `test_job_task_runner.py` 214, `tests/docs/` 295, `test_roadmap_index.py` 30, `tests/ui_server/` 515, `test_test_runner.py` 52, `test_resource_safety.py` 21, `test_integrity_gate.py` 16, `test_golden_path.py` (canary) 42 — nothing moved outside this round's own one new test. G8 HELD: `git status --porcelain` empty, `git ls-files .remedy-wt` empty, no leftover scratch worktree, all four pre-handback commits' numstat `+` cells matched the handback's own Commits table cell for cell, reproduced independently. ZERO DEVIATIONS WERE DECLARED by the worker and the reviewer found none either. No finding is registered; nothing is wrong on disk. `job.run`'s `--yes` arg exists with zero runtime readers yet, exactly as expected at this stage — the next slice wires the real `confirm_cost_preview()` call, and the reviewer's own pre-authoring investigation already found and will need to repair several existing test call sites of `_cmd_job_run_cycles` that do not pass `yes`/`unattended` and would otherwise break under the new gate (tests/orchestration/test_long_run_executor.py and tests/orchestration/test_escalation.py). Branch `feature/f114-cost-preview-per-command` is pushed and matches `origin` head-for-head; `git status --porcelain` reads empty now.
<<<END RECORD7>>>

<<<BEGIN PLAN8>>>
# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 8 books round 7's PASS verdict (RECORD7) and wires the real
`confirm_cost_preview()` call into `_cmd_job_run_cycles`
(`apps/cli/commands/job.py`), gating both the single-cycle short-circuit
and the full `run_cycles` path. The estimate is `CostBandEstimate(None,
None, ESTIMATE_UNAVAILABLE, {})` - honest, since `job.run` has no
per-task class data before it starts - which A9 treats as expensive, so
every call now confirms unless `--yes` or `--unattended` (mapped to
skip-prompt, per the feature doc's unattended-never-prompts rule). This
round also repairs existing `_cmd_job_run_cycles` call sites in
tests/orchestration/test_long_run_executor.py and
tests/orchestration/test_escalation.py that would otherwise trip the new
gate under pytest's non-tty stdin, and adds two new tests for the gate
itself.

## Next Steps

- T003 continuation: goldens for the preview line, docs for `--yes` and
  the cost-preview behavior.
- T003 continuation: consider marking other "rerunning subtrees" /
  "long explanations" commands `is_expensive` - only `job.run` so far.
- Acceptance fixtures, the integration gate, then the closure sequence
  (PR, Open PR Gate). No PR exists yet.
- Session note: round 8, session 2 - 3 delegated rounds this session
  (6, 7, 8), within the 4-5 default.

## Risks

- Every non-interactive `job.run` call now needs `--yes` or
  `--unattended` or it exits with EXIT_USAGE - by design (A9), but a
  real behavior change for existing automation, worth flagging to the
  operator as breaking, not additive.
- Real cost bands for `job.run` still do not exist - a future round
  needs real task-class data to replace the unavailable estimate.
<<<END PLAN8>>>

<<<BEGIN SIG PAIR FROM>>>
def _cmd_job_run_cycles(
    job_id_str: str,
    *,
    cycles: int | None = None,
    unattended: bool = False,
    json_output: bool = False,
) -> None:
<<<END SIG PAIR FROM>>>

<<<BEGIN SIG PAIR TO>>>
def _cmd_job_run_cycles(
    job_id_str: str,
    *,
    cycles: int | None = None,
    unattended: bool = False,
    yes: bool = False,
    json_output: bool = False,
) -> None:
<<<END SIG PAIR TO>>>

<<<BEGIN GATE PAIR FROM>>>
    if resolved.capped:
        origin = "--cycles" if resolved.source == "flag" else "cycles.max_cycles"
        print(
            f"Note: {origin} {resolved.requested} capped to {resolved.max_cycles} "
            f"by the F046 rollout default (raised by the F075 milestone gate).",
            file=sys.stderr,
        )

    if resolved.max_cycles <= 1:
<<<END GATE PAIR FROM>>>

<<<BEGIN GATE PAIR TO>>>
    if resolved.capped:
        origin = "--cycles" if resolved.source == "flag" else "cycles.max_cycles"
        print(
            f"Note: {origin} {resolved.requested} capped to {resolved.max_cycles} "
            f"by the F046 rollout default (raised by the F075 milestone gate).",
            file=sys.stderr,
        )

    from apps.cli.cost_preview_confirm import confirm_cost_preview
    from packages.orchestration.cost_preview import (
        ESTIMATE_UNAVAILABLE,
        CostBandEstimate,
        resolve_confirm_above_usd,
    )

    estimate = CostBandEstimate(None, None, ESTIMATE_UNAVAILABLE, {})
    if not confirm_cost_preview(
        estimate,
        confirm_above_usd=resolve_confirm_above_usd(),
        yes=(yes or unattended),
        command_name="job.run",
    ):
        print("Cancelled. Nothing was run.")
        return

    if resolved.max_cycles <= 1:
<<<END GATE PAIR TO>>>

<<<BEGIN HANDLER PAIR FROM>>>
    "job.run": lambda args: _cmd_job_run_cycles(
        args.job_id,
        cycles=(int(args.cycles) if getattr(args, "cycles", None) else None),
        unattended=getattr(args, "unattended", False),
        json_output=getattr(args, "json", False),
    ),
<<<END HANDLER PAIR FROM>>>

<<<BEGIN HANDLER PAIR TO>>>
    "job.run": lambda args: _cmd_job_run_cycles(
        args.job_id,
        cycles=(int(args.cycles) if getattr(args, "cycles", None) else None),
        unattended=getattr(args, "unattended", False),
        yes=getattr(args, "yes", False),
        json_output=getattr(args, "json", False),
    ),
<<<END HANDLER PAIR TO>>>

<<<BEGIN TLRE1 PAIR FROM>>>
        job_cmd._cmd_job_run_cycles("abc12345")
<<<END TLRE1 PAIR FROM>>>

<<<BEGIN TLRE1 PAIR TO>>>
        job_cmd._cmd_job_run_cycles("abc12345", yes=True)
<<<END TLRE1 PAIR TO>>>

<<<BEGIN TLRE2 PAIR FROM>>>
        job_cmd._cmd_job_run_cycles(str(job.id), cycles=99)
<<<END TLRE2 PAIR FROM>>>

<<<BEGIN TLRE2 PAIR TO>>>
        job_cmd._cmd_job_run_cycles(str(job.id), cycles=99, yes=True)
<<<END TLRE2 PAIR TO>>>

<<<BEGIN TLRE3 PAIR FROM>>>
        job_cmd._cmd_job_run_cycles(str(job.id), cycles=3)
<<<END TLRE3 PAIR FROM>>>

<<<BEGIN TLRE3 PAIR TO>>>
        job_cmd._cmd_job_run_cycles(str(job.id), cycles=3, yes=True)
<<<END TLRE3 PAIR TO>>>

<<<BEGIN TLRE4 PAIR FROM>>>
            job_cmd._cmd_job_run_cycles(str(job.id))
<<<END TLRE4 PAIR FROM>>>

<<<BEGIN TLRE4 PAIR TO>>>
            job_cmd._cmd_job_run_cycles(str(job.id), yes=True)
<<<END TLRE4 PAIR TO>>>

<<<BEGIN NEWTESTS PAIR FROM>>>
        err = capsys.readouterr().err
        assert "cycles.max_cycles 20 capped to 8" in err
<<<END NEWTESTS PAIR FROM>>>

<<<BEGIN NEWTESTS PAIR TO>>>
        err = capsys.readouterr().err
        assert "cycles.max_cycles 20 capped to 8" in err

    def test_declining_the_cost_preview_returns_without_running(self, monkeypatch, capsys):
        from apps.cli.commands import job as job_cmd

        monkeypatch.setattr(
            "apps.cli.cost_preview_confirm.confirm_cost_preview", lambda *a, **k: False)
        ran: list[str] = []
        monkeypatch.setattr(job_cmd, "_cmd_run_next_task_local", ran.append)
        job_cmd._cmd_job_run_cycles("abc12345")
        assert ran == []
        assert "Cancelled" in capsys.readouterr().out

    def test_the_gate_sees_an_unavailable_estimate_and_yes_or_unattended(self, monkeypatch):
        from apps.cli.commands import job as job_cmd

        seen: dict = {}

        def fake_confirm(estimate, *, confirm_above_usd, yes, command_name):
            seen["estimate"] = estimate
            seen["yes"] = yes
            seen["command_name"] = command_name
            return True

        monkeypatch.setattr("apps.cli.cost_preview_confirm.confirm_cost_preview", fake_confirm)
        ran: list[str] = []
        monkeypatch.setattr(job_cmd, "_cmd_run_next_task_local", ran.append)
        job_cmd._cmd_job_run_cycles("abc12345", unattended=True)
        assert seen["estimate"].band_usd_high is None
        assert seen["yes"] is True
        assert seen["command_name"] == "job.run"
        assert ran == ["abc12345"]
<<<END NEWTESTS PAIR TO>>>

<<<BEGIN ESC1 PAIR FROM>>>
            job_cmd._cmd_job_run_cycles(str(cli_job.id), cycles=3)
<<<END ESC1 PAIR FROM>>>

<<<BEGIN ESC1 PAIR TO>>>
            job_cmd._cmd_job_run_cycles(str(cli_job.id), cycles=3, yes=True)
<<<END ESC1 PAIR TO>>>

<<<BEGIN ESC2 PAIR FROM>>>
        job_cmd._cmd_job_run_cycles("abc12345")
<<<END ESC2 PAIR FROM>>>

<<<BEGIN ESC2 PAIR TO>>>
        job_cmd._cmd_job_run_cycles("abc12345", yes=True)
<<<END ESC2 PAIR TO>>>
