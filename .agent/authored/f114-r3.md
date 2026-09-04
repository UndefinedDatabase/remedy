STEP T001 PART 2 (COMPLETES T001) / ROUND 3 - F114 Cost preview per command
FEATURE F114 - Cost preview per command (Tier 3) - SESSION 1, ROUND 3

Goal
  Book round 2's PASS verdict into the ledger (RECORD2) and complete T001:
  ship packages/orchestration/cost_preview.py (estimate_cost_band,
  CostBandEstimate, ESTIMATE_UNAVAILABLE) and its tests. No production
  caller this round - that is T002, not started yet.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f114-r3.md
  C0b mirror it to .agent/last_block.md
  C1  apply RECORD2 to .agent/live_review.md (append) and PLAN3 to
      .agent/plan.md (whole-file replacement)
  C2  write packages/orchestration/cost_preview.py per MODULE (new file)
      and tests/orchestration/test_cost_preview.py per TESTMODULE (new
      file)
  C3  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f114-r3.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md (C1) - .agent/plan.md (C1) -
  packages/orchestration/cost_preview.py (new, C2) -
  tests/orchestration/test_cost_preview.py (new, C2) -
  .agent/handoff.md (C3)

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by
     delimiter index from the COMMITTED .agent/authored/f114-r3.md -
     marker lines EXCLUDED - and write it with a script, never by
     retyping. If a slice looks wrong, apply it as written and DECLARE it
     in the handback.
  2. C1 is the first substantive commit of the round.
  3. RECORD2 appends to .agent/live_review.md as EXACTLY ONE newline byte
     followed by the slice (the file's own current convention, same as
     round 2's own G2 measurement). PLAN3 REPLACES .agent/plan.md whole.
  4. BOTH new files are WHOLE-FILE writes: write each one's exact bytes
     with the Write tool (a "copyfile", never a text-extraction-and-
     reflow) and verify each by extracting MODULE / TESTMODULE from the
     committed authored file and `cmp` against the written file.
  5. Do NOT wire cost_preview into apps/cli, command_catalog.py, or any
     call site - that is T002. Zero production callers is expected at
     this stage, not a "dead code" defect - G6's red-proof is what
     proves the code is real despite having no caller yet.
  6. Do not touch packages/orchestration/token_economy.py,
     packages/orchestration/budget_guard.py, or
     packages/orchestration/budget_resolution.py - only the two new
     files carry content this round.
  7. ruff is DENIED to this session (measured at the F114 claim and
     again at round 2); gate with `python3 -m py_compile` on both new
     files instead, and ATTEMPT `ruff check` on both, reporting the real
     output or the exact refusal text - never assume either way.
  8. A sentence OUTSIDE the change set that this round makes stale is
     DECLARED in the handback and NOT repaired. Round 2's own
     `.agent/context.md` line 29 declaration stands; do not repeat it.
  9. Read .agent/STOP from disk before the first commit and again before
     C3. If it exists, finish the commit in hand, write the handback,
     and stop.
  10. Self-review loop before every commit (git diff --stat, git diff).
      Push after C3. No pull request, no merge this round.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f114-r3.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE LEDGER APPEND. Base size of .agent/live_review.md immediately
     BEFORE C1 (measure it yourself): report its byte length and whether
     it ends with a trailing newline. RECORD2 has ZERO internal
     newlines - report its own byte length. Report: base + 1 +
     len(RECORD2) and whether that equals the post-C1 file's byte length
     (expected 2355786, from a base of 2351767
     and a RECORD2 of 4018 bytes - recompute both independently).
     Then the SECOND reader: report whether the post-C1 file's bytes from
     `base` to the end equal exactly `"\n" + RECORD2`. Then a NEGATIVE
     CONTROL in a scratch copy ONLY (never the tracked file): flip one
     byte inside RECORD2's own text and report the second reader REJECTS it.
  G3 THE PLAN. Extract PLAN3 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md            -> exit 0
       wc -l .agent/plan.md                      -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G4 THE TWO NEW FILES. Extract MODULE and TESTMODULE from the COMMITTED
     authored file and `cmp` each against
     packages/orchestration/cost_preview.py and
     tests/orchestration/test_cost_preview.py respectively -> exit 0
     each. Report each file's byte length (MODULE expected 3414,
     TESTMODULE expected 4614 - recompute both
     independently).
  G5 COMPILE AND LINT. `python3 -m py_compile` on both new files -> exit
     0 each. Then ATTEMPT `ruff check packages/orchestration/cost_preview.py
     tests/orchestration/test_cost_preview.py` and report the real
     result, success or refusal text, verbatim.
  G6 THE RED-PROOF, INSIDE A DISPOSABLE GIT WORKTREE ONLY (never the
     primary checkout - self_drive_protocol.md guardrail G5). After C2,
     from the round's own HEAD: create a scratch worktree, inside it
     change the final `return CostBandEstimate(min(usd_a, usd_b),
     max(usd_a, usd_b), basis, inputs)` line in cost_preview.py so BOTH
     bounds use `max(usd_a, usd_b)` instead of one using `min`, then run
       python3 -m pytest tests/orchestration/test_cost_preview.py -q
     and report the failure count (must be greater than zero - name
     which test(s) failed). Then revert the edit inside that same
     worktree, re-run the same command and report it fully green again
     (13 passed - the unmutated control). Remove the worktree when done
     (`git worktree remove --force`) - it must not exist at G8's tree
     check.
  G7 THE SUITES, EACH AS ITS OWN INVOCATION, RUN SERIALLY, IN THE PRIMARY
     CHECKOUT:
       python3 -m pytest tests/orchestration/test_cost_preview.py -q
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
     The last is the canary. test_cost_preview.py is expected at 13
     passed (a brand new file); every other count is a moved-count
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
RECORD2, PLAN3, MODULE and TESTMODULE.

<<<BEGIN RECORD2>>>
Gate: F114 R2 — the round 2 entry, `tokens_to_cost_usd()` extraction and refactor, no ledger findings. VERDICT PASS, over the range `fd25323e1b91178299cd9be1320058db88132047..80d469c26d927bf16294edd83efd6d058f90f014` (commits C0a `e8f75da1502fbf023087546e7ae93618526c71c4`, C0b `06ce3b8f8481ed1225d1e5f054e568ddeb1ceb25`, C1 `b7eec287e125ccd7384af7dbc5f1e854f945eb74`, C2 `9230a7135d4ec69a9cc29d81e964458d31385f44` — four real content commits — plus handback commit `80d469c26d927bf16294edd83efd6d058f90f014`), independently re-verified by the reviewer. TRANSPORT HELD: `sha256sum .agent/authored/f114-r2.md .agent/last_block.md` both print `1dd16065123b01af3b195cbb7f07934915256273992db5cc1f9c13dde9abfaae`, reproduced directly. G2 THE LEDGER APPEND HELD: `.agent/live_review.md` measured 2351767 bytes after C1, matching `2349237 + 1 + 2529` exactly, reproduced independently by the reviewer with its own byte-length reads on both sides of the append and the tail-slice comparison against RECORD1. G3 THE PLAN HELD BYTE-EXACT: PLAN2 extracted from the committed authored file `cmp`s exit 0 against `.agent/plan.md` (42 lines, under 50; `## Goal`/`## Next Steps` each exactly once), reproduced independently. G4 THE THREE CODE PAIRS HELD: the reviewer independently reconstructed each of `packages/orchestration/token_economy.py`, `packages/orchestration/budget_guard.py` and `tests/orchestration/test_token_economy.py` by applying the block's own FROM/TO pairs to a pre-round scratch copy and found each byte-identical to the real committed file — TE PAIR an append (`TO contains FROM: true`), BG PAIR a rewrite (`TO contains FROM: false`), TEST PAIR an append across the file's own trailing newline. G5 HELD: `python3 -m py_compile` exit 0 on all three files, reproduced; `ruff check` produced the same session-level denial text the handback quoted, reproduced verbatim rather than assumed. G6 THE RED-PROOF HELD, REPRODUCED INDEPENDENTLY IN A SEPARATE DISPOSABLE WORKTREE: the reviewer's own /999 mutation of `tokens_to_cost_usd` produced the identical 8 failing tests the worker reported, spanning both `test_token_economy.py`'s own new unit test and `test_predictive_budget.py`'s downstream coverage of `predict_next_task_cost` — proving the extraction is genuinely reachable, not dead code; the worktree was removed after. G7 THE SUITES, REPRODUCED INDEPENDENTLY BY THE REVIEWER at this round's own HEAD, all ten counts identical to the worker's own reading: `test_token_economy.py` 42, `test_predictive_budget.py` 75, `test_budget_guard.py` 92, `tests/docs/` 295, `test_roadmap_index.py` 30, `tests/ui_server/` 515, `test_test_runner.py` 52, `test_resource_safety.py` 21, `test_integrity_gate.py` 16, `test_golden_path.py` (canary) 42 — nothing moved beyond the five new `TestTokensToCostUsd` tests the change set itself added. G8 HELD: `git status --porcelain` empty, `git ls-files .remedy-wt` empty, no leftover scratch worktree, all four pre-handback commits' numstat `+` cells matched the handback's own Commits table cell for cell, reproduced independently. Two honest deviations were declared and are both correctly handled, not defects: (1) this round's own G7 wording carried an unedited "THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE" sentence copied from round 1's differently-shaped gate list — a reviewer authoring slip in the block, not a worker error, and the worker reported the real measured counts rather than forcing the mismatched wording; a future block will not repeat this copy-paste. (2) `.agent/context.md` line 29 now names removed code (`budget_guard.py:482-484`, replaced by C2) and is correctly declared stale rather than repaired, since `.agent/context.md` is outside this round's change set — it will be corrected the next time context.md itself is rewritten. No finding is registered for either; nothing is wrong on disk. Branch `feature/f114-cost-preview-per-command` is pushed and matches `origin` head-for-head; `git status --porcelain` reads empty now.
<<<END RECORD2>>>

<<<BEGIN PLAN3>>>
# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 3 books round 2's PASS verdict (RECORD2) and completes T001: the
new module `packages/orchestration/cost_preview.py` (`estimate_cost_band`,
`CostBandEstimate`, `ESTIMATE_UNAVAILABLE`) computes a real USD band —
never a fabricated point — from two `TokenBand` values, a repeat count
and a `PredictiveBudgetConfig`, reusing round 2's
`token_economy.tokens_to_cost_usd()`. Its tests land in
`tests/orchestration/test_cost_preview.py`. Neither file has any
production caller yet — that is T002, next.

## Next Steps

- T002: CLI helper (`apps/cli`) — threshold confirm, tty/non-tty
  semantics (pipe never hangs), `--yes` audited, reusing
  `loop_cmd.py`'s `_confirm_materialization`/`_stdin_is_a_tty` pattern,
  calling `cost_preview.estimate_cost_band()` for the shown numbers.
- T003: mark expensive commands in `apps/cli/command_catalog.py`,
  goldens for preview lines, docs.
- Acceptance fixtures, the integration gate, then the closure sequence.

## Risks

- No expensive-command registry exists yet — T003 is greenfield.
- `estimate_cost_band`'s two-band-plus-repeat-count shape is this
  feature's own design choice (feature file gives a suggested shape
  only); T002 is where it meets real CLI call sites and may need a
  small adjustment, not a rewrite.
<<<END PLAN3>>>

<<<BEGIN MODULE>>>
"""F114 T001 — the shared cost-band estimator.

Computes an upfront USD cost BAND (never a point) from the class-default
token counts and price basis ``resolve_predictive_budget_config``
resolves (budget_resolution.py) — one estimator, shared with
``predict_next_task_cost`` (budget_guard.py) via
``token_economy.tokens_to_cost_usd``. Pure: no reads/writes/clock/prompt
(scanned by tests/test_no_interactive_guard.py). CLI confirmation is
built in a later round, entirely inside apps/cli.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from packages.orchestration.budget_resolution import PredictiveBudgetConfig
from packages.orchestration.token_economy import TokenBand, tokens_to_cost_usd

#: The estimate could not be computed - an unrecognised class, an unpriced
#: config, or an invalid repeat count. Never a fabricated number (P6).
ESTIMATE_UNAVAILABLE = "estimate_unavailable"

_VALID_BANDS = (TokenBand.LOW, TokenBand.MEDIUM, TokenBand.HIGH)


@dataclass(frozen=True)
class CostBandEstimate:
    """A USD cost estimate - always a band, never a point.

    ``band_usd_low``/``band_usd_high`` are None together, never separately:
    an unrecognised class or an unset price basis makes the WHOLE estimate
    unavailable rather than half of it fabricated. ``band_usd_low ==
    band_usd_high`` is a real duplicate (caller named one class twice),
    not evidence of missing math.
    """

    band_usd_low: float | None
    band_usd_high: float | None
    basis: str
    inputs: dict[str, Any] = field(default_factory=dict)


def estimate_cost_band(
    band_a: str,
    band_b: str,
    *,
    repeat_count: int = 1,
    config: PredictiveBudgetConfig,
) -> CostBandEstimate:
    """Estimate a USD cost band spanning ``band_a`` and ``band_b``.

    Both are ``TokenBand`` values (LOW/MEDIUM/HIGH); pass the same value
    twice for a single confidently-known class (an honest degenerate
    band, not a fabricated spread). ``repeat_count`` scales a single
    unit's cost. Argument order does not matter - the lower resulting
    USD figure is always ``band_usd_low``.

    Returns UNAVAILABLE (both bounds None) rather than a guess when:
    either band is unrecognised or has no configured class default,
    ``repeat_count`` is negative, or ``config`` has no price basis
    (A9: unknown is treated as expensive, never guessed here).
    """
    inputs: dict[str, Any] = {
        "band_a": band_a,
        "band_b": band_b,
        "repeat_count": repeat_count,
    }
    class_defaults = config.class_default_tokens
    if (
        band_a not in _VALID_BANDS
        or band_b not in _VALID_BANDS
        or band_a not in class_defaults
        or band_b not in class_defaults
        or repeat_count < 0
    ):
        return CostBandEstimate(None, None, ESTIMATE_UNAVAILABLE, inputs)

    price_basis = config.price_basis_usd_per_1k_tokens
    usd_a = tokens_to_cost_usd(class_defaults[band_a] * repeat_count, price_basis)
    usd_b = tokens_to_cost_usd(class_defaults[band_b] * repeat_count, price_basis)
    if usd_a is None or usd_b is None:
        return CostBandEstimate(None, None, ESTIMATE_UNAVAILABLE, inputs)

    basis = (
        f"class defaults ({band_a}/{band_b} token bands) x "
        f"price_basis_usd_per_1k_tokens={price_basis}"
    )
    return CostBandEstimate(min(usd_a, usd_b), max(usd_a, usd_b), basis, inputs)
<<<END MODULE>>>

<<<BEGIN TESTMODULE>>>
"""F114 T001 — tests for the shared cost-band estimator.

Covers ``estimate_cost_band`` / ``CostBandEstimate`` in
``packages.orchestration.cost_preview`` — one estimator, shared with
``budget_guard.predict_next_task_cost`` via
``token_economy.tokens_to_cost_usd``, per T3_F114.md.
"""
from __future__ import annotations

import pytest

from packages.orchestration.budget_resolution import PredictiveBudgetConfig
from packages.orchestration.cost_preview import ESTIMATE_UNAVAILABLE, estimate_cost_band
from packages.orchestration.token_economy import TokenBand

CLASS_DEFAULTS = {TokenBand.LOW: 8000, TokenBand.MEDIUM: 32000, TokenBand.HIGH: 120000}


def _config(price_basis, defaults=None):
    return PredictiveBudgetConfig(
        price_basis_usd_per_1k_tokens=price_basis,
        class_default_tokens=dict(CLASS_DEFAULTS if defaults is None else defaults),
    )


class TestSingleConfidentBand:
    def test_same_band_twice_gives_a_degenerate_band(self):
        # 8000 tokens x $0.02/1k = $0.16, both bounds identical.
        e = estimate_cost_band(TokenBand.LOW, TokenBand.LOW, config=_config(0.02))
        assert e.band_usd_low == 0.16
        assert e.band_usd_high == 0.16
        assert e.basis != ESTIMATE_UNAVAILABLE

    def test_repeat_count_scales_both_bounds(self):
        e = estimate_cost_band(TokenBand.LOW, TokenBand.LOW, repeat_count=3, config=_config(0.02))
        assert e.band_usd_low == pytest.approx(0.48)
        assert e.band_usd_high == pytest.approx(0.48)

    def test_zero_repeat_count_is_a_measured_zero(self):
        e = estimate_cost_band(TokenBand.HIGH, TokenBand.HIGH, repeat_count=0, config=_config(0.02))
        assert e.band_usd_low == 0.0
        assert e.band_usd_high == 0.0


class TestSpanningBand:
    def test_low_and_high_span_produces_a_real_range(self):
        # LOW=8000 tok -> $0.16 ; HIGH=120000 tok -> $2.40, at $0.02/1k.
        e = estimate_cost_band(TokenBand.LOW, TokenBand.HIGH, config=_config(0.02))
        assert e.band_usd_low == pytest.approx(0.16)
        assert e.band_usd_high == pytest.approx(2.40)

    def test_argument_order_does_not_matter(self):
        a = estimate_cost_band(TokenBand.LOW, TokenBand.HIGH, config=_config(0.02))
        b = estimate_cost_band(TokenBand.HIGH, TokenBand.LOW, config=_config(0.02))
        assert (a.band_usd_low, a.band_usd_high) == (b.band_usd_low, b.band_usd_high)


class TestBasisLabel:
    def test_basis_names_both_bands_and_the_price(self):
        e = estimate_cost_band(TokenBand.LOW, TokenBand.MEDIUM, config=_config(0.02))
        assert TokenBand.LOW in e.basis
        assert TokenBand.MEDIUM in e.basis
        assert "0.02" in e.basis

    def test_every_available_estimate_carries_a_non_unavailable_basis(self):
        for band_a in (TokenBand.LOW, TokenBand.MEDIUM, TokenBand.HIGH):
            for band_b in (TokenBand.LOW, TokenBand.MEDIUM, TokenBand.HIGH):
                e = estimate_cost_band(band_a, band_b, config=_config(0.02))
                assert e.basis != ESTIMATE_UNAVAILABLE
                assert e.band_usd_low is not None
                assert e.band_usd_high is not None


class TestUnavailable:
    def test_unknown_band_is_unavailable_not_guessed(self):
        e = estimate_cost_band(TokenBand.UNKNOWN, TokenBand.LOW, config=_config(0.02))
        assert e.band_usd_low is None
        assert e.band_usd_high is None
        assert e.basis == ESTIMATE_UNAVAILABLE

    def test_nonsense_band_is_unavailable(self):
        e = estimate_cost_band("nonsense", TokenBand.LOW, config=_config(0.02))
        assert e.basis == ESTIMATE_UNAVAILABLE

    def test_missing_price_basis_is_unavailable(self):
        e = estimate_cost_band(TokenBand.LOW, TokenBand.LOW, config=_config(None))
        assert e.band_usd_low is None
        assert e.band_usd_high is None
        assert e.basis == ESTIMATE_UNAVAILABLE

    def test_negative_repeat_count_is_unavailable(self):
        e = estimate_cost_band(TokenBand.LOW, TokenBand.LOW, repeat_count=-1, config=_config(0.02))
        assert e.basis == ESTIMATE_UNAVAILABLE

    def test_class_missing_from_config_is_unavailable(self):
        partial = {TokenBand.LOW: 8000}
        e = estimate_cost_band(TokenBand.LOW, TokenBand.HIGH, config=_config(0.02, defaults=partial))
        assert e.basis == ESTIMATE_UNAVAILABLE


class TestInputsRecordWhatWasAsked:
    def test_inputs_carry_the_raw_request(self):
        e = estimate_cost_band(TokenBand.MEDIUM, TokenBand.HIGH, repeat_count=2, config=_config(0.02))
        assert e.inputs == {"band_a": TokenBand.MEDIUM, "band_b": TokenBand.HIGH, "repeat_count": 2}
<<<END TESTMODULE>>>