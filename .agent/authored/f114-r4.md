STEP T002 PART 1 / ROUND 4 - F114 Cost preview per command
FEATURE F114 - Cost preview per command (Tier 3) - SESSION 1, ROUND 4

Goal
  Book round 3's PASS verdict into the ledger (RECORD3) and start T002:
  register config key cost_preview.confirm_above_usd (default 0.5) and
  add resolver resolve_confirm_above_usd() to cost_preview.py. No CLI
  file touched this round - that lands in round 5.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f114-r4.md
  C0b mirror it to .agent/last_block.md
  C1  apply RECORD3 to .agent/live_review.md (append) and PLAN4 to
      .agent/plan.md (whole-file replacement)
  C2  apply IMPORT PAIR and APPEND PAIR to
      packages/orchestration/cost_preview.py, CONFIG PAIR to
      packages/orchestration/config.py, and TEST PAIR to
      tests/orchestration/test_cost_preview.py
  C3  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f114-r4.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md (C1) - .agent/plan.md (C1) -
  packages/orchestration/cost_preview.py (C2) -
  packages/orchestration/config.py (C2) -
  tests/orchestration/test_cost_preview.py (C2) - .agent/handoff.md (C3)

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by
     delimiter index from the COMMITTED .agent/authored/f114-r4.md -
     marker lines EXCLUDED - and write it with a script, never by
     retyping. If a slice looks wrong, apply it as written and DECLARE it
     in the handback.
  2. C1 is the first substantive commit of the round.
  3. RECORD3 appends to .agent/live_review.md as EXACTLY ONE newline byte
     followed by the slice (the file's own current convention, same as
     rounds 2 and 3's own G2 measurement). PLAN4 REPLACES .agent/plan.md
     whole.
  4. NEWLINE CONVENTION PER SLICE, STATED EXPLICITLY (round 3's own
     lesson - this is not left implicit this time): IMPORT PAIR FROM/TO
     carry NO trailing newline in either (both are bare 2-3 line
     snippets, not full-file tails). APPEND PAIR FROM is
     `packages/orchestration/cost_preview.py`'s OWN real trailing
     newline (the file's true current last byte) - a byte-exact SUFFIX
     of the file, confirmed with `.endswith()` before applying. CONFIG
     PAIR FROM is a mid-file entry with NO trailing newline of its own
     (the entry's closing `),` is immediately followed by the next
     entry's `ConfigKeySpec(` on the following line - the block between
     them has no blank line to lose or gain). TEST PAIR FROM is
     `tests/orchestration/test_cost_preview.py`'s OWN real trailing
     newline, same reasoning as APPEND PAIR - both are real source-file
     tails, confirmed with `.endswith()` before applying.
  5. IMPORT PAIR IS A REWRITE (content inserted BETWEEN the FROM's two
     lines, same shape as F112 R2's own CONFIG PAIR precedent): verify
     FROM count is exactly 1 in cost_preview.py before C2, apply
     str.replace(FROM, TO, 1), confirm "TO contains FROM: false".
  6. APPEND PAIR, CONFIG PAIR and TEST PAIR ARE ALL APPENDS: for each,
     verify its own FROM count is exactly 1 in its target file before
     C2, and confirm "TO contains FROM: true" for each before applying.
  7. Apply IMPORT PAIR and APPEND PAIR to cost_preview.py as TWO
     SEPARATE str.replace calls on the same file, IMPORT PAIR first (its
     FROM is nearer the top and unaffected by APPEND PAIR's own edit at
     the file's tail).
  8. Do NOT touch apps/cli/ or any command file - that is round 5's
     T002 completion. resolve_confirm_above_usd() having zero CLI
     callers yet is expected at this stage, not a "dead code" defect -
     G6's red-proof is what proves the code is real despite having no
     caller yet.
  9. ruff is DENIED to this session (measured at the F114 claim and
     again at rounds 2 and 3); gate with `python3 -m py_compile` on all
     three touched/created `.py` files instead, and ATTEMPT `ruff check`
     on the two production files, reporting the real output or the
     exact refusal text - never assume either way.
  10. A sentence OUTSIDE the change set that this round makes stale is
      DECLARED in the handback and NOT repaired. Rounds 2 and 3's own
      `.agent/context.md` declarations (lines 29 and 36) stand; do not
      repeat them.
  11. Read .agent/STOP from disk before the first commit and again
      before C3. If it exists, finish the commit in hand, write the
      handback, and stop.
  12. Self-review loop before every commit (git diff --stat, git diff).
      Push after C3. No pull request, no merge this round.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f114-r4.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE LEDGER APPEND. Base size of .agent/live_review.md immediately
     BEFORE C1 (measure it yourself): report its byte length and whether
     it ends with a trailing newline. RECORD3 has ZERO internal
     newlines - report its own byte length. Report: base + 1 +
     len(RECORD3) and whether that equals the post-C1 file's byte length
     (expected 2360277, from a base of 2355786
     and a RECORD3 of 4490 bytes - recompute both independently).
     Then the SECOND reader: report whether the post-C1 file's bytes from
     `base` to the end equal exactly `"\n" + RECORD3`. Then a NEGATIVE
     CONTROL in a scratch copy ONLY (never the tracked file): flip one
     byte inside RECORD3's own text and report the second reader REJECTS it.
  G3 THE PLAN. Extract PLAN4 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md            -> exit 0
       wc -l .agent/plan.md                      -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G4 THE FOUR CODE PAIRS. For EACH of IMPORT PAIR, APPEND PAIR, CONFIG
     PAIR and TEST PAIR: report the FROM count in its target file
     immediately BEFORE C2 (must be exactly 1 for all four - IMPORT PAIR
     and APPEND PAIR both target cost_preview.py, so re-count IMPORT
     PAIR's FROM in the file BEFORE APPEND PAIR is applied, per
     constraint 7's ordering), and after C2 report the containment
     test's own output in these words - "TO contains FROM: true" or
     "TO contains FROM: false" - matching constraints 5/6 exactly. Then
     extract each slice from the COMMITTED authored file and cmp the
     target file's actual new content against what applying str.replace
     in the constraint-7 order to a pre-C2 scratch copy of each target
     produces - exit 0 for all three target files (cost_preview.py takes
     two pairs, config.py and test_cost_preview.py take one each).
  G5 COMPILE AND LINT. `python3 -m py_compile` on
     packages/orchestration/cost_preview.py,
     packages/orchestration/config.py and
     tests/orchestration/test_cost_preview.py -> exit 0 each. Then
     ATTEMPT `ruff check packages/orchestration/cost_preview.py
     packages/orchestration/config.py` and report the real result,
     success or refusal text, verbatim.
  G6 THE RED-PROOF, INSIDE A DISPOSABLE GIT WORKTREE ONLY (never the
     primary checkout - self_drive_protocol.md guardrail G5). After C2,
     from the round's own HEAD: create a scratch worktree, inside it
     change `resolve_confirm_above_usd`'s own `if value > 0:` line to
     `if value >= 0:` (a one-character edit, allows a configured zero
     through instead of falling back), then run
       python3 -m pytest tests/orchestration/test_cost_preview.py -q
     and report the failure count (must be greater than zero - name
     which test failed). Then revert the edit inside that same worktree,
     re-run the same command and report it fully green again (19 passed
     - the unmutated control). Remove the worktree when done
     (`git worktree remove --force`) - it must not exist at G8's tree
     check.
  G7 THE SUITES, EACH AS ITS OWN INVOCATION, RUN SERIALLY, IN THE PRIMARY
     CHECKOUT:
       python3 -m pytest tests/orchestration/test_cost_preview.py -q
       python3 -m pytest tests/orchestration/test_config.py -q
       python3 -m pytest tests/test_no_interactive_guard.py -q
       python3 -m pytest tests/orchestration/test_predictive_budget.py -q
       python3 -m pytest tests/orchestration/test_budget_guard.py -q
       python3 -m pytest tests/orchestration/test_token_economy.py -q
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
     The last is the canary. test_cost_preview.py is expected at 19
     passed (13 existing + 6 new); every other count is a moved-count
     check against the reviewer's own independent base reading - report
     what you actually measured, not what you expect.
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
RECORD3, PLAN4, IMPORT PAIR FROM/TO, APPEND PAIR FROM/TO, CONFIG PAIR
FROM/TO and TEST PAIR FROM/TO.

<<<BEGIN RECORD3>>>
Gate: F114 R3 — the round 3 entry, `cost_preview.py` ships (T001 complete), no ledger findings. VERDICT PASS, over the range `80d469c26d927bf16294edd83efd6d058f90f014..8b296131eff88cbdbe13bd47b839c95f5c4490d6` (commits C0a `6b7d394cb6864bda7059a3e7923050d6d8034d81`, C0b `1fb5c49a8566b3caedaa7938337cd07048784e45`, C1 `6362270591b47339e49ecb7cc388fb7c8182cabe`, C2 `539b291dc4e4edff683608843133483233e7a865` — four real content commits — plus handback commit `8b296131eff88cbdbe13bd47b839c95f5c4490d6`), independently re-verified by the reviewer. TRANSPORT HELD: `sha256sum .agent/authored/f114-r3.md .agent/last_block.md` both print `8fee890a26670158becee84733669803e416a781f7e21273fa12d19a337cc740`, reproduced directly. G2 THE LEDGER APPEND HELD: `.agent/live_review.md` measured 2355786 bytes after C1, matching `2351767 + 1 + 4018` exactly, reproduced independently. G3 THE PLAN HELD BYTE-EXACT: PLAN3 extracted from the committed authored file `cmp`s exit 0 against `.agent/plan.md` (39 lines, under 50; `## Goal`/`## Next Steps` each exactly once), reproduced independently. G4 THE TWO NEW FILES HELD BYTE-EXACT: the reviewer independently `cmp`d the committed `packages/orchestration/cost_preview.py` (3414 bytes) and `tests/orchestration/test_cost_preview.py` (4614 bytes) directly against its own pre-round scratch originals — byte-for-byte identical, including each file's trailing newline; the worker's handback correctly identified and declared a one-byte-per-file extraction subtlety (the block's markers placed each new file's own real trailing newline immediately before its END marker with no separator, unlike RECORD2/PLAN3 which have no trailing newline of their own) and reconstructed both files correctly rather than assuming a uniform rule — a reviewer authoring imprecision, not a worker error, and the landed bytes are exactly right regardless. G5 HELD: `python3 -m py_compile` exit 0 on both files, reproduced; `ruff check` produced the same session-level denial text the handback quoted, reproduced verbatim rather than assumed. G6 THE RED-PROOF HELD, REPRODUCED INDEPENDENTLY IN A SEPARATE DISPOSABLE WORKTREE: the reviewer's own min-to-max mutation of the final `CostBandEstimate(...)` line produced the identical single failing test the worker reported (`TestSpanningBand::test_low_and_high_span_produces_a_real_range`, 1 failed, 12 passed), proving the low/high computation is real, reachable code; the worktree was removed after. G7 THE SUITES, REPRODUCED INDEPENDENTLY BY THE REVIEWER at this round's own HEAD, all twelve counts identical to the worker's own reading: `test_cost_preview.py` 13 (new), `test_no_interactive_guard.py` 6, `test_predictive_budget.py` 75, `test_budget_guard.py` 92, `test_token_economy.py` 42, `tests/docs/` 295, `test_roadmap_index.py` 30, `tests/ui_server/` 515, `test_test_runner.py` 52, `test_resource_safety.py` 21, `test_integrity_gate.py` 16, `test_golden_path.py` (canary) 42 — nothing moved outside this round's own new file. G8 HELD: `git status --porcelain` empty, `git ls-files .remedy-wt` empty, no leftover scratch worktree, all four pre-handback commits' numstat `+` cells matched the handback's own Commits table cell for cell, reproduced independently. Two honest deviations were declared and are both correctly handled, not defects: (1) the MODULE/TESTMODULE trailing-newline extraction subtlety already described above — resolved correctly, landed bytes verified exact by the reviewer independently, no finding registered; a future block will state each slice's newline convention explicitly rather than leaving it implicit. (2) `.agent/context.md` line 36 now names cost_preview.py as nonexistent, which C2 makes false; correctly declared stale rather than repaired, since `.agent/context.md` is outside this round's change set — it will be corrected the next time context.md itself is rewritten, alongside round 2's still-open line-29 declaration. No finding is registered for either; nothing is wrong on disk. T001 IS NOW COMPLETE: the shared cost-band estimator exists, is tested, and is honest about its own design deviation from the feature file's suggested shape (a two-band-plus-repeat-count signature rather than a bare `estimate(command_context)`, declared in PLAN3's own Risks section at round 3's own authoring time, not discovered after the fact). Branch `feature/f114-cost-preview-per-command` is pushed and matches `origin` head-for-head; `git status --porcelain` reads empty now.
<<<END RECORD3>>>

<<<BEGIN PLAN4>>>
# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 4 books round 3's PASS verdict (RECORD3) and starts T002 (the CLI
helper): a new config key `cost_preview.confirm_above_usd` (default 0.5,
F114 Design: "around half a dollar") registers in
`packages/orchestration/config.py`, and a new resolver
`resolve_confirm_above_usd()` lands in `cost_preview.py` itself, same
env>TOML>default authority as `resolve_predictive_budget_config`. Round 5
completes T002: the actual CLI confirm helper in `apps/cli`, reusing
`loop_cmd.py`'s `_confirm_materialization`/`_stdin_is_a_tty` shape,
calling this round's resolver and `estimate_cost_band`. No CLI file is
touched this round.

## Next Steps

- Round 5: `apps/cli/cost_preview_confirm.py` (new shared module) — the
  render+confirm helper, tty/non-tty semantics (pipe never hangs),
  `--yes` audited — completing T002. Its own tests land in
  `tests/cli/test_cost_preview_confirm.py`.
- T003: mark expensive commands in `apps/cli/command_catalog.py`,
  goldens for preview lines, docs.
- Acceptance fixtures, the integration gate, then the closure sequence.

## Risks

- No expensive-command registry exists yet — T003 is greenfield.
- `apps/cli/` has no existing shared confirm/exit-code module; round 5
  creates the first one rather than extending something that exists.
<<<END PLAN4>>>

<<<BEGIN IMPORT PAIR FROM>>>
from dataclasses import dataclass, field
from typing import Any
<<<END IMPORT PAIR FROM>>>

<<<BEGIN IMPORT PAIR TO>>>
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
<<<END IMPORT PAIR TO>>>

<<<BEGIN APPEND PAIR FROM>>>
    return CostBandEstimate(min(usd_a, usd_b), max(usd_a, usd_b), basis, inputs)
<<<END APPEND PAIR FROM>>>

<<<BEGIN APPEND PAIR TO>>>
    return CostBandEstimate(min(usd_a, usd_b), max(usd_a, usd_b), basis, inputs)


#: Default confirm-above threshold (F114 Design: "around half a dollar").
#: Config source of truth is cost_preview.confirm_above_usd; this is only
#: the fallback when nothing is configured (same non-invention posture as
#: token_economy - a real number, not a magic default hidden in the CLI).
DEFAULT_CONFIRM_ABOVE_USD = 0.5


def resolve_confirm_above_usd(
    *,
    config_path: str | None = None,
    project_root: str | None = None,
) -> float:
    """Resolve the F114 confirm-above-USD threshold: env > TOML > default.

    Same config authority as ``resolve_predictive_budget_config``. A
    malformed or non-positive configured value falls back to
    ``DEFAULT_CONFIRM_ABOVE_USD`` rather than raising - this threshold is
    a UX policy, not a budget limit, so a bad config value degrades to
    the safe default instead of blocking every command.
    """
    from packages.orchestration.config import ConfigSource, load_config

    if config_path:
        cfg = load_config(project_path=Path(config_path))
    elif project_root:
        cfg = load_config(project_path=Path(project_root) / "remedy.toml")
    else:
        cfg = load_config()

    cv = cfg.get_value("cost_preview.confirm_above_usd")
    if cv is not None and cv.source != ConfigSource.DEFAULT and cv.value is not None:
        try:
            value = float(cv.value)
        except (TypeError, ValueError):
            return DEFAULT_CONFIRM_ABOVE_USD
        if value > 0:
            return value
    return DEFAULT_CONFIRM_ABOVE_USD
<<<END APPEND PAIR TO>>>

<<<BEGIN CONFIG PAIR FROM>>>
    ConfigKeySpec(
        key="budget.class_default_tokens_high",
        env_var="REMEDY_BUDGET_CLASS_DEFAULT_TOKENS_HIGH",
        description=(
            "Expected tokens for a high-band task "
            "(F104; provisional until calibration)"
        ),
        value_type=int,
        default=120000,
    ),
<<<END CONFIG PAIR FROM>>>

<<<BEGIN CONFIG PAIR TO>>>
    ConfigKeySpec(
        key="budget.class_default_tokens_high",
        env_var="REMEDY_BUDGET_CLASS_DEFAULT_TOKENS_HIGH",
        description=(
            "Expected tokens for a high-band task "
            "(F104; provisional until calibration)"
        ),
        value_type=int,
        default=120000,
    ),
    ConfigKeySpec(
        key="cost_preview.confirm_above_usd",
        env_var="REMEDY_COST_PREVIEW_CONFIRM_ABOVE_USD",
        description=(
            "USD threshold above which an expensive command's cost preview "
            "requires operator confirmation before it runs (F114)"
        ),
        value_type=float,
        default=0.5,
    ),
<<<END CONFIG PAIR TO>>>

<<<BEGIN TEST PAIR FROM>>>
class TestInputsRecordWhatWasAsked:
    def test_inputs_carry_the_raw_request(self):
        e = estimate_cost_band(TokenBand.MEDIUM, TokenBand.HIGH, repeat_count=2, config=_config(0.02))
        assert e.inputs == {"band_a": TokenBand.MEDIUM, "band_b": TokenBand.HIGH, "repeat_count": 2}
<<<END TEST PAIR FROM>>>

<<<BEGIN TEST PAIR TO>>>
class TestInputsRecordWhatWasAsked:
    def test_inputs_carry_the_raw_request(self):
        e = estimate_cost_band(TokenBand.MEDIUM, TokenBand.HIGH, repeat_count=2, config=_config(0.02))
        assert e.inputs == {"band_a": TokenBand.MEDIUM, "band_b": TokenBand.HIGH, "repeat_count": 2}


# ---------------------------------------------------------------------------
# resolve_confirm_above_usd (F114 T002 — the CLI confirm threshold)
# ---------------------------------------------------------------------------


class TestResolveConfirmAboveUsd:
    def test_documented_default_when_nothing_is_configured(self):
        from packages.orchestration.cost_preview import (
            DEFAULT_CONFIRM_ABOVE_USD,
            resolve_confirm_above_usd,
        )
        assert resolve_confirm_above_usd() == DEFAULT_CONFIRM_ABOVE_USD == 0.5

    def test_toml_sets_the_threshold(self, tmp_path):
        from packages.orchestration.cost_preview import resolve_confirm_above_usd
        toml = tmp_path / "remedy.toml"
        toml.write_text("[remedy.cost_preview]\nconfirm_above_usd = 2.5\n")
        assert resolve_confirm_above_usd(config_path=str(toml)) == 2.5

    def test_env_sets_the_threshold(self, monkeypatch):
        from packages.orchestration.cost_preview import resolve_confirm_above_usd
        monkeypatch.setenv("REMEDY_COST_PREVIEW_CONFIRM_ABOVE_USD", "1.25")
        assert resolve_confirm_above_usd() == 1.25

    def test_negative_configured_value_falls_back_to_default(self, tmp_path):
        from packages.orchestration.cost_preview import (
            DEFAULT_CONFIRM_ABOVE_USD,
            resolve_confirm_above_usd,
        )
        toml = tmp_path / "remedy.toml"
        toml.write_text("[remedy.cost_preview]\nconfirm_above_usd = -1.0\n")
        assert resolve_confirm_above_usd(config_path=str(toml)) == DEFAULT_CONFIRM_ABOVE_USD

    def test_zero_configured_value_falls_back_to_default(self, tmp_path):
        from packages.orchestration.cost_preview import (
            DEFAULT_CONFIRM_ABOVE_USD,
            resolve_confirm_above_usd,
        )
        toml = tmp_path / "remedy.toml"
        toml.write_text("[remedy.cost_preview]\nconfirm_above_usd = 0\n")
        assert resolve_confirm_above_usd(config_path=str(toml)) == DEFAULT_CONFIRM_ABOVE_USD

    def test_project_root_form_reads_the_same_file(self, tmp_path):
        from packages.orchestration.cost_preview import resolve_confirm_above_usd
        (tmp_path / "remedy.toml").write_text(
            "[remedy.cost_preview]\nconfirm_above_usd = 3.0\n")
        assert resolve_confirm_above_usd(project_root=str(tmp_path)) == 3.0
<<<END TEST PAIR TO>>>