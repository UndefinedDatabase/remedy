STEP T002 PART 2 (COMPLETES T002) / ROUND 5 - F114 Cost preview per command
FEATURE F114 - Cost preview per command (Tier 3) - SESSION 1, ROUND 5

Goal
  Book round 4's PASS verdict into the ledger (RECORD4) and complete T002:
  ship apps/cli/cost_preview_confirm.py (render_estimate_line,
  confirm_cost_preview, EXIT_USAGE) and its tests. No real command calls
  it this round - that is T003, not started yet.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f114-r5.md
  C0b mirror it to .agent/last_block.md
  C1  apply RECORD4 to .agent/live_review.md (append) and PLAN5 to
      .agent/plan.md (whole-file replacement)
  C2  write apps/cli/cost_preview_confirm.py per MODULE (new file) and
      tests/cli/test_cost_preview_confirm.py per TESTMODULE (new file)
  C3  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f114-r5.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md (C1) - .agent/plan.md (C1) -
  apps/cli/cost_preview_confirm.py (new, C2) -
  tests/cli/test_cost_preview_confirm.py (new, C2) - .agent/handoff.md (C3)

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by
     delimiter index from the COMMITTED .agent/authored/f114-r5.md -
     marker lines EXCLUDED - and write it with a script, never by
     retyping. If a slice looks wrong, apply it as written and DECLARE it
     in the handback.
  2. C1 is the first substantive commit of the round.
  3. RECORD4 appends to .agent/live_review.md as EXACTLY ONE newline byte
     followed by the slice (the file's own current convention, same as
     every prior round's own G2 measurement). PLAN5 REPLACES
     .agent/plan.md whole.
  4. NEWLINE CONVENTION, STATED EXPLICITLY: RECORD4 and PLAN5 carry NO
     trailing newline of their own (matching this round's own scratch
     originals and .agent/plan.md's pre-round convention). MODULE and
     TESTMODULE are both real Python source files whose OWN trailing
     newline is their true last byte - each is a byte-exact structural
     suffix ending in `\n`, and that `\n` is part of the slice, not
     marker-line formatting (same class as round 3's own MODULE/
     TESTMODULE, and round 4's own APPEND/TEST PAIRs).
  5. BOTH new files are WHOLE-FILE writes: write each one's exact bytes
     with the Write tool (a "copyfile", never a text-extraction-and-
     reflow) and verify each by extracting MODULE / TESTMODULE from the
     committed authored file and `cmp` against the written file.
  6. Do NOT wire cost_preview_confirm into any command file or
     command_catalog.py - that is T003. Zero production callers is
     expected at this stage, not a "dead code" defect - G6's red-proof
     is what proves the code is real despite having no caller yet.
  7. Do not touch packages/orchestration/cost_preview.py,
     packages/orchestration/config.py, or apps/cli/commands/loop_cmd.py -
     only the two new files carry content this round.
  8. ruff is DENIED to this session (measured at the F114 claim and at
     every round since); gate with `python3 -m py_compile` on both new
     files instead, and ATTEMPT `ruff check` on both, reporting the real
     output or the exact refusal text - never assume either way.
  9. A sentence OUTSIDE the change set that this round makes stale is
     DECLARED in the handback and NOT repaired. Rounds 2 and 3's own
     `.agent/context.md` declarations (lines 29 and 36) stand; do not
     repeat them.
  10. Read .agent/STOP from disk before the first commit and again
      before C3. If it exists, finish the commit in hand, write the
      handback, and stop.
  11. Self-review loop before every commit (git diff --stat, git diff).
      Push after C3. No pull request, no merge this round - T002
      completing does not by itself trigger the Open PR Gate; that
      waits for T003 and the acceptance fixtures.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f114-r5.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE LEDGER APPEND. Base size of .agent/live_review.md immediately
     BEFORE C1 (measure it yourself): report its byte length and whether
     it ends with a trailing newline. RECORD4 has ZERO internal
     newlines - report its own byte length. Report: base + 1 +
     len(RECORD4) and whether that equals the post-C1 file's byte length
     (expected 2364059, from a base of 2360277
     and a RECORD4 of 3781 bytes - recompute both independently).
     Then the SECOND reader: report whether the post-C1 file's bytes from
     `base` to the end equal exactly `"\n" + RECORD4`. Then a NEGATIVE
     CONTROL in a scratch copy ONLY (never the tracked file): flip one
     byte inside RECORD4's own text and report the second reader REJECTS it.
  G3 THE PLAN. Extract PLAN5 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md            -> exit 0
       wc -l .agent/plan.md                      -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G4 THE TWO NEW FILES. Extract MODULE and TESTMODULE from the COMMITTED
     authored file and `cmp` each against apps/cli/cost_preview_confirm.py
     and tests/cli/test_cost_preview_confirm.py respectively -> exit 0
     each. Report each file's byte length (MODULE expected 2541,
     TESTMODULE expected 4744 - recompute both independently).
  G5 COMPILE AND LINT. `python3 -m py_compile` on both new files -> exit
     0 each. Then ATTEMPT `ruff check apps/cli/cost_preview_confirm.py
     tests/cli/test_cost_preview_confirm.py` and report the real result,
     success or refusal text, verbatim.
  G6 THE RED-PROOF, INSIDE A DISPOSABLE GIT WORKTREE ONLY (never the
     primary checkout - self_drive_protocol.md guardrail G5). After C2,
     from the round's own HEAD: create a scratch worktree, inside it
     change `confirm_cost_preview`'s own comparison
     `estimate.band_usd_high > confirm_above_usd` to use `<` instead of
     `>` (a one-character edit), then run
       python3 -m pytest tests/cli/test_cost_preview_confirm.py -q
     and report the failure count (must be greater than zero - name
     which tests failed). Then revert the edit inside that same
     worktree, re-run the same command and report it fully green again
     (12 passed - the unmutated control). Remove the worktree when done
     (`git worktree remove --force`) - it must not exist at G8's tree
     check.
  G7 THE SUITES, EACH AS ITS OWN INVOCATION, RUN SERIALLY, IN THE PRIMARY
     CHECKOUT:
       python3 -m pytest tests/cli/test_cost_preview_confirm.py -q
       python3 -m pytest tests/cli/test_loop_cmd.py -q
       python3 -m pytest tests/test_no_interactive_guard.py -q
       python3 -m pytest tests/orchestration/test_cost_preview.py -q
       python3 -m pytest tests/orchestration/test_config.py -q
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
     The last is the canary. test_cost_preview_confirm.py is expected at
     12 passed (a brand new file); test_no_interactive_guard.py's own
     count is worth a specific note in the handback - apps/cli is OUTSIDE
     its _GUARDED_PACKAGES scan scope, so this round's new file must NOT
     change that suite's pass count at all; every other count is a
     moved-count check against the reviewer's own independent base
     reading - report what you actually measured, not what you expect.
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
  carries the SESSION NUMBER of the running feature - this is SESSION 1
  of F114 - the state block, the item-status table with every ordered
  item appearing exactly once, the Commits table, one line per gate
  followed by the transcripts, the deviations, and the next steps. It has
  no length cap.

SLICES. Each slice lies between its own one-line BEGIN and END marker.
The marker lines are NEVER part of the slice. The slices carried here are
RECORD4, PLAN5, MODULE and TESTMODULE.

<<<BEGIN RECORD4>>>
Gate: F114 R4 — the round 4 entry, cost_preview.confirm_above_usd config key + resolve_confirm_above_usd(), no ledger findings. VERDICT PASS, over the range `8b296131eff88cbdbe13bd47b839c95f5c4490d6..99157a070a2d7291332c16071246e8960cfffc34` (commits C0a `8bb227b8f18a8ebcc4247e515429255987f86dc8`, C0b `db8c8e7321fc6487cf45505bc23847d928b56476`, C1 `4d46e2935222b6dc349c6921967b16338c4e213d`, C2 `6978e949ece539b59e635ed899b23d557422fa3c` — four real content commits — plus handback commit `99157a070a2d7291332c16071246e8960cfffc34`), independently re-verified by the reviewer. TRANSPORT HELD: `sha256sum .agent/authored/f114-r4.md .agent/last_block.md` both print `c0b99055ee4cb5f5b7c65d83240ba2339c829dfb12e5fd22c2d2a18713957b5b`, reproduced directly. G2 THE LEDGER APPEND HELD: `.agent/live_review.md` measured 2360277 bytes after C1, matching `2355786 + 1 + 4490` exactly, reproduced independently. G3 THE PLAN HELD BYTE-EXACT: PLAN4 extracted from the committed authored file `cmp`s exit 0 against `.agent/plan.md` (39 lines, under 50; `## Goal`/`## Next Steps` each exactly once), reproduced independently. G4 THE FOUR CODE PAIRS HELD: the reviewer independently reconstructed `packages/orchestration/cost_preview.py`, `packages/orchestration/config.py` and `tests/orchestration/test_cost_preview.py` by applying the block's own four FROM/TO pairs, in constraint-7 order, to pre-round scratch copies, and found all three byte-identical to the real committed files — IMPORT PAIR a rewrite (`TO contains FROM: false`), APPEND/CONFIG/TEST PAIRS all appends (`TO contains FROM: true`). This round's own constraint 4 stated each slice's newline convention EXPLICITLY (round 3's own lesson, applied), and the round reproduced every stated number exactly with zero deviations declared — a genuine improvement over round 3's implicit-convention gap, confirmed by its own outcome rather than assumed. G5 HELD: `python3 -m py_compile` exit 0 on all three files, reproduced; `ruff check` produced the same session-level denial text the handback quoted, reproduced verbatim. G6 THE RED-PROOF HELD, REPRODUCED INDEPENDENTLY IN A SEPARATE DISPOSABLE WORKTREE: the reviewer's own `value > 0` to `value >= 0` mutation produced the identical single failing test the worker reported (`TestResolveConfirmAboveUsd::test_zero_configured_value_falls_back_to_default`, 1 failed, 18 passed), proving the validation fallback is real, reachable code; the worktree was removed after. G7 THE SUITES, REPRODUCED INDEPENDENTLY BY THE REVIEWER at this round's own HEAD, all thirteen counts identical to the worker's own reading: `test_cost_preview.py` 19, `test_config.py` 81, `test_no_interactive_guard.py` 6, `test_predictive_budget.py` 75, `test_budget_guard.py` 92, `test_token_economy.py` 42, `tests/docs/` 295, `test_roadmap_index.py` 30, `tests/ui_server/` 515, `test_test_runner.py` 52, `test_resource_safety.py` 21, `test_integrity_gate.py` 16, `test_golden_path.py` (canary) 42 — nothing moved outside this round's own six new tests. G8 HELD: `git status --porcelain` empty, `git ls-files .remedy-wt` empty, no leftover scratch worktree, all four pre-handback commits' numstat `+` cells matched the handback's own Commits table cell for cell, reproduced independently. ZERO DEVIATIONS WERE DECLARED, a first for this feature's rounds so far — the handback states this explicitly and credits it to constraint 4's explicit newline-convention statement. No finding is registered; nothing is wrong on disk. `resolve_confirm_above_usd()` has zero CLI callers yet, exactly as expected at this stage of T002 (the confirm helper itself lands next round). Branch `feature/f114-cost-preview-per-command` is pushed and matches `origin` head-for-head; `git status --porcelain` reads empty now.
<<<END RECORD4>>>

<<<BEGIN PLAN5>>>
# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 5 books round 4's PASS verdict (RECORD4) and completes T002: the
new shared module `apps/cli/cost_preview_confirm.py`
(`render_estimate_line`, `confirm_cost_preview`, `EXIT_USAGE`) reuses
`loop_cmd.py`'s tty/prompt shape, calling round 4's
`resolve_confirm_above_usd()` and T001's `estimate_cost_band()`. Its
tests land in `tests/cli/test_cost_preview_confirm.py`. No real command
calls it yet - that is T003, a separate future round.

## Next Steps

- T003: mark expensive commands in `apps/cli/command_catalog.py`, wire
  them to `confirm_cost_preview()`, goldens for the preview lines, docs.
- Acceptance fixtures, the integration gate, then the closure sequence.
- Session note: this is round 5 of the 4-5 default; the next round is a
  natural point to consider a fresh session per amend0827 rule 6, unless
  context remains ample.

## Risks

- No expensive-command registry exists yet - T003 is greenfield.
- T003 will be the first round with a REAL production caller; until
  then, both `cost_preview.py` and `cost_preview_confirm.py` are
  fully-tested but uncalled code, proven live only by their own
  mutation red-proofs.
<<<END PLAN5>>>

<<<BEGIN MODULE>>>
"""F114 T002 — the shared cost-preview confirmation helper.

Renders an upfront USD estimate band and confirms before an expensive
command runs. A SHARED module (unlike loop_cmd.py's own local
`_confirm_materialization`/`_stdin_is_a_tty` copy) so a future expensive
command reuses this rather than growing a third copy of the same shape.
No command calls this yet - wiring a real command to it is T003.
"""
from __future__ import annotations

import sys

from packages.orchestration.cost_preview import CostBandEstimate

EXIT_USAGE = 2


def _stdin_is_a_tty() -> bool:
    """Whether there is an operator on the other end who could answer a prompt."""
    return sys.stdin.isatty()


def render_estimate_line(estimate: CostBandEstimate) -> str:
    """The one-line preview text - always carries its basis (A9)."""
    if estimate.band_usd_low is None or estimate.band_usd_high is None:
        return f"estimated cost unavailable (basis: {estimate.basis})"
    return (
        f"estimated ${estimate.band_usd_low:.4f}-${estimate.band_usd_high:.4f} "
        f"(basis: {estimate.basis})"
    )


def confirm_cost_preview(
    estimate: CostBandEstimate,
    *,
    confirm_above_usd: float,
    yes: bool,
    command_name: str,
) -> bool:
    """Show the estimate and decide whether the command may proceed.

    Returns True to proceed, False if the operator declined. An
    UNAVAILABLE estimate (``band_usd_high`` is None) is treated as
    expensive (A9) - it always requires confirmation, same as a real
    high estimate over the threshold.

    ``yes`` skips the prompt and proceeds, printing an audited line so
    the skip is visible in evidence. A non-tty stdin never blocks: it
    exits with the estimate and the --yes hint rather than hanging on a
    pipe. Below the threshold, no prompt either way - cheap commands
    never interrupt.
    """
    line = render_estimate_line(estimate)
    is_expensive = estimate.band_usd_high is None or estimate.band_usd_high > confirm_above_usd
    if not is_expensive:
        print(line)
        return True

    if yes:
        print(f"{line} - proceeding without prompt (--yes)")
        return True

    if not _stdin_is_a_tty():
        print(
            f"Error: {line}. stdin is not a terminal, so there is nobody to "
            f"confirm. Pass --yes to run '{command_name}' without a prompt.",
            file=sys.stderr,
        )
        sys.exit(EXIT_USAGE)

    print(line)
    return input(f"Continue running '{command_name}'? [y/N] ").strip().lower() in ("y", "yes")
<<<END MODULE>>>

<<<BEGIN TESTMODULE>>>
"""F114 T002 — tests for the shared cost-preview confirmation helper.

Covers `render_estimate_line` / `confirm_cost_preview` in
`apps.cli.cost_preview_confirm`, reusing the tty-mocking shape
`tests/cli/test_loop_cmd.py` already established for
`loop_cmd._stdin_is_a_tty` / `builtins.input`.
"""
from __future__ import annotations

import pytest

from apps.cli import cost_preview_confirm as cpc
from packages.orchestration.cost_preview import CostBandEstimate

AVAILABLE = CostBandEstimate(0.16, 2.40, "class defaults (low/high) x price=0.02", {})
UNAVAILABLE = CostBandEstimate(None, None, "estimate_unavailable", {})


class TestRenderEstimateLine:
    def test_available_estimate_shows_the_band_and_basis(self):
        line = cpc.render_estimate_line(AVAILABLE)
        assert "$0.1600" in line
        assert "$2.4000" in line
        assert "class defaults (low/high) x price=0.02" in line

    def test_unavailable_estimate_says_so_and_still_carries_a_basis(self):
        line = cpc.render_estimate_line(UNAVAILABLE)
        assert "unavailable" in line
        assert "estimate_unavailable" in line


class TestUnderThreshold:
    def test_under_threshold_proceeds_without_any_prompt(self, capsys):
        result = cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=10.0, yes=False, command_name="do")
        assert result is True
        assert "estimated" in capsys.readouterr().out

    def test_under_threshold_never_touches_stdin(self, monkeypatch, capsys):
        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: (_ for _ in ()).throw(
            AssertionError("must not be called when under threshold")))
        cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=10.0, yes=False, command_name="do")


class TestOverThresholdWithYes:
    def test_yes_skips_the_prompt_and_proceeds(self, capsys):
        result = cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=0.5, yes=True, command_name="do")
        assert result is True
        out = capsys.readouterr().out
        assert "--yes" in out

    def test_yes_never_touches_stdin(self, monkeypatch):
        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: (_ for _ in ()).throw(
            AssertionError("must not be called when --yes")))
        cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=0.5, yes=True, command_name="do")


class TestOverThresholdNonTty:
    def test_non_tty_exits_with_usage_code_never_hangs(self, monkeypatch, capsys):
        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: False)
        with pytest.raises(SystemExit) as exc:
            cpc.confirm_cost_preview(
                AVAILABLE, confirm_above_usd=0.5, yes=False, command_name="do")
        assert exc.value.code == cpc.EXIT_USAGE
        assert exc.value.code != 0
        err = capsys.readouterr().err
        assert "--yes" in err
        assert "do" in err

    def test_non_tty_never_calls_input(self, monkeypatch):
        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: False)
        monkeypatch.setattr("builtins.input", lambda prompt="": (_ for _ in ()).throw(
            AssertionError("must not prompt on non-tty")))
        with pytest.raises(SystemExit):
            cpc.confirm_cost_preview(
                AVAILABLE, confirm_above_usd=0.5, yes=False, command_name="do")


class TestOverThresholdTty:
    def test_tty_answering_yes_proceeds(self, monkeypatch):
        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: True)
        monkeypatch.setattr("builtins.input", lambda prompt="": "y")
        result = cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=0.5, yes=False, command_name="do")
        assert result is True

    def test_tty_declining_returns_false_without_raising(self, monkeypatch):
        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: True)
        monkeypatch.setattr("builtins.input", lambda prompt="": "n")
        result = cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=0.5, yes=False, command_name="do")
        assert result is False


class TestUnavailableIsTreatedAsExpensive:
    def test_unavailable_estimate_requires_confirmation_even_at_a_huge_threshold(
            self, monkeypatch):
        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: False)
        with pytest.raises(SystemExit) as exc:
            cpc.confirm_cost_preview(
                UNAVAILABLE, confirm_above_usd=999999.0, yes=False, command_name="do")
        assert exc.value.code == cpc.EXIT_USAGE

    def test_unavailable_estimate_with_yes_still_proceeds(self):
        result = cpc.confirm_cost_preview(
            UNAVAILABLE, confirm_above_usd=999999.0, yes=True, command_name="do")
        assert result is True
<<<END TESTMODULE>>>