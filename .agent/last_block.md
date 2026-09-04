STEP T001 PART 1 / ROUND 2 - F114 Cost preview per command
FEATURE F114 - Cost preview per command (Tier 3) - SESSION 1, ROUND 2

Goal
  Book round 1's PASS verdict into the ledger (RECORD1) and extract the
  shared cost-arithmetic helper: a new pure function
  packages/orchestration/token_economy.py:tokens_to_cost_usd() replaces
  the inlined multiply at packages/orchestration/budget_guard.py:482-484
  inside predict_next_task_cost, which is refactored to call it. No
  behavior change - the arithmetic (tokens / 1000 * price_basis) and its
  None-propagation are preserved byte-for-byte as a Python expression, so
  every existing caller's output is unaffected. Round 1's own plan text
  named the wrong regression suite (tests/orchestration/test_budget_guard.py);
  the real coverage of predict_next_task_cost is
  tests/orchestration/test_predictive_budget.py, corrected here.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f114-r2.md
  C0b mirror it to .agent/last_block.md
  C1  apply RECORD1 to .agent/live_review.md (append) and PLAN2 to
      .agent/plan.md (whole-file replacement)
  C2  apply TE PAIR to packages/orchestration/token_economy.py, BG PAIR to
      packages/orchestration/budget_guard.py, and TEST PAIR to
      tests/orchestration/test_token_economy.py
  C3  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f114-r2.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md (C1) - .agent/plan.md (C1) -
  packages/orchestration/token_economy.py (C2) -
  packages/orchestration/budget_guard.py (C2) -
  tests/orchestration/test_token_economy.py (C2) - .agent/handoff.md (C3)

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by
     delimiter index from the COMMITTED .agent/authored/f114-r2.md -
     marker lines EXCLUDED - and write it with a script, never by
     retyping. If a slice looks wrong, apply it as written and DECLARE it
     in the handback.
  2. C1 is the first substantive commit of the round.
  3. RECORD1 appends to .agent/live_review.md as EXACTLY ONE newline byte
     followed by the slice - measured mechanically on the file's own last
     eight "Gate: F" record boundaries before this round (each preceded
     by exactly one `\n`, never a blank line), which is the file's real
     CURRENT convention, not an assumed one. PLAN2 REPLACES .agent/plan.md
     whole.
  4. TE PAIR IS AN APPEND: FROM is the single line `def _now() -> str:`
     (count it in the file before C2 - must be exactly 1); TO is the new
     function's full text ending in that same line verbatim, so TO
     CONTAINS FROM - verify this containment mechanically and report
     "TO contains FROM: true" before applying.
  5. BG PAIR IS A REWRITE: FROM is the three-line block reproduced in the
     BG PAIR FROM slice (count it in the file before C2 - must be exactly
     1); TO does NOT contain FROM - verify "TO contains FROM: false"
     before applying.
  6. TEST PAIR IS AN APPEND spanning the file's OWN trailing newline: FROM
     is the file's last existing test method's five lines PLUS the file's
     own trailing newline byte (so FROM is a true byte-exact SUFFIX of the
     file before C2 - verify this with .endswith() before applying, and
     count FROM exactly 1); TO is FROM with the new test class's text
     appended after it, so TO CONTAINS FROM - verify "TO contains FROM:
     true". This construction reproduces byte-for-byte what a plain
     append (`cat snippet >> file`) would have produced - a fact you may
     verify yourself by comparing the two constructions in scratch before
     applying, but only the FROM/TO replace method may touch the tracked
     file.
  7. Do not touch packages/orchestration/budget_resolution.py,
     packages/orchestration/pingpong_job.py, apps/cli/commands/job.py, or
     any other caller/consumer of predict_next_task_cost or
     PredictiveBudgetConfig - only the two files named in the change set
     carry production-code edits this round.
  8. packages/orchestration/cost_preview.py does NOT exist yet and is NOT
     created this round - that is round 3.
  9. A sentence OUTSIDE the change set that this round makes stale is
     DECLARED in the handback and NOT repaired.
  10. Read .agent/STOP from disk before the first commit and again before
      C3. If it exists, finish the commit in hand, write the handback,
      and stop.
  11. Self-review loop before every commit (git diff --stat, git diff).
      Push after C3. No pull request, no merge.
  12. ruff is DENIED to this session (measured at the F114 claim, round
      1's CONTEXT1); gate with `python3 -m py_compile` on all three
      touched/created .py files instead, and additionally ATTEMPT
      `ruff check` yourself on the two production files, reporting either
      its real output or the exact refusal text - never assume either
      way.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f114-r2.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE LEDGER APPEND. Base size of .agent/live_review.md immediately
     BEFORE C1 (measure it yourself, do not trust a stated number):
     report its byte length and whether it ends with a trailing newline.
     RECORD1 has ZERO internal newlines - report its own byte length via
     UTF-8 encoding. Report: base + 1 + len(RECORD1) and whether that
     equals the post-C1 file's byte length (expected 2351767,
     from a base of 2349237 and a RECORD1 of 2529
     bytes - recompute both independently rather than trusting these
     numbers). Then the SECOND, independent reader: split the WHOLE
     post-C1 file on single-newline boundaries after its LAST "Gate: F"
     marker and report whether that final unit equals RECORD1 exactly.
     Then a NEGATIVE CONTROL in a scratch copy ONLY (never the tracked
     file): flip one byte inside RECORD1's own text and report that the
     second reader REJECTS it.
  G3 THE PLAN. Extract PLAN2 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md            -> exit 0
       wc -l .agent/plan.md                      -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G4 THE THREE CODE PAIRS. For EACH of TE PAIR, BG PAIR and TEST PAIR:
     report the FROM count in its target file immediately BEFORE C2 (must
     be exactly 1 for all three), and after C2 report the containment
     test's own output in these words - "TO contains FROM: true" or
     "TO contains FROM: false" - matching constraints 4/5/6 exactly. Then
     extract each slice from the COMMITTED authored file and cmp the
     target file's actual new content against what str.replace(FROM, TO,
     1) applied to a pre-C2 scratch copy of each target produces - exit 0
     for all three.
  G5 COMPILE AND LINT. `python3 -m py_compile` on
     packages/orchestration/token_economy.py,
     packages/orchestration/budget_guard.py and
     tests/orchestration/test_token_economy.py -> exit 0 each. Then
     ATTEMPT `ruff check packages/orchestration/token_economy.py
     packages/orchestration/budget_guard.py` and report the real result,
     success or refusal text, verbatim.
  G6 THE RED-PROOF, INSIDE A DISPOSABLE GIT WORKTREE ONLY (never the
     primary checkout - self_drive_protocol.md guardrail G5). After C2,
     from the round's own HEAD: create a scratch worktree, inside it
     change tokens_to_cost_usd's own `return tokens / 1000 * ...` line to
     divide by 999 instead of 1000 (a one-character edit), then run
       python3 -m pytest tests/orchestration/test_token_economy.py
         tests/orchestration/test_predictive_budget.py -q
     and report the failure count (must be greater than zero - name which
     tests failed). Then revert the one-character edit inside that same
     worktree, re-run the same command and report it fully green again
     (the unmutated control). Remove the worktree when done
     (`git worktree remove --force`) - it must not exist at G8's tree
     check.
  G7 THE SUITES, EACH AS ITS OWN INVOCATION, RUN SERIALLY, IN THE PRIMARY
     CHECKOUT:
       python3 -m pytest tests/orchestration/test_token_economy.py -q
       python3 -m pytest tests/orchestration/test_predictive_budget.py -q
       python3 -m pytest tests/orchestration/test_budget_guard.py -q
       python3 -m pytest tests/docs/ -q
       python3 -m pytest tests/orchestration/test_roadmap_index.py -q
       python3 -m pytest tests/ui_server/ -q
       python3 -m pytest tests/orchestration/test_test_runner.py -q
       python3 -m pytest tests/regression/test_resource_safety.py -q
       python3 -m pytest tests/orchestration/test_integrity_gate.py -q
       python3 -m pytest tests/cli/test_golden_path.py -q
     Report each pass count. THE FOUR STATE READERS ARE RUN AS FOUR, NOT
     AS THREE. The last is the canary. The first three must show a pass
     count STRICTLY GREATER than their pre-round baseline (new tests
     landed); the other seven are a moved-count check against the
     reviewer's independent base reading.
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
RECORD1, PLAN2, TE PAIR FROM, TE PAIR TO, BG PAIR FROM, BG PAIR TO, TEST
PAIR FROM and TEST PAIR TO.

<<<BEGIN RECORD1>>>
Gate: F114 R1 — the round 1 entry, the STATUS claim and plan/context set, no production code. VERDICT PASS, over the range `a1b5d4bb455550f082da7d6c4c80fd968d6e1a88..fd25323e1b91178299cd9be1320058db88132047` (commits C0a `064c28dd351f7eb157713401fcdd1e3c9b26db9c`, C0b `8534dfa413a6e3220c2dacc199bd3e1e78257441`, C1 `88f6e57f20a3080d58ac9b699c8f5eb54f208e44`, C2 `3f3fc506cdb857039281e731c976cf8d7c21f0d0` — four real content commits — plus handback commit `fd25323e1b91178299cd9be1320058db88132047`), independently re-verified by the reviewer. TRANSPORT HELD: `sha256sum .agent/authored/f114-r1.md .agent/last_block.md` both print `c286ebc3ec985927a7a20018db46e9f98b35808c9e7c9514c76d3d896fca25e4`, reproduced directly. G2 THE PLAN HELD BYTE-EXACT: PLAN1 extracted from the committed authored file `cmp`s exit 0 against `.agent/plan.md` (42 lines, under 50; `## Goal`/`## Next Steps` each exactly once), reproduced independently. G3 THE STATUS PAIR HELD: `docs/roadmap/STATUS.md`'s F114 line read `- [ ] F114 — Cost preview per command` exactly once before C2 and `- [~] F114 — Cost preview per command` exactly once after, TO does not contain FROM (a rewrite), reproduced independently. G4 THE CONTEXT HELD BYTE-EXACT: CONTEXT1 extracted from the committed authored file `cmp`s exit 0 against `.agent/context.md` (`## Active Branch`/`## Steps` each exactly once, one `feature/` occurrence, first `F\d{3}` match `F114`, `pytest` present), reproduced independently. G5 THE SUITES, REPRODUCED INDEPENDENTLY BY THE REVIEWER at this round's own HEAD: `tests/docs/` 295 passed, `tests/orchestration/test_roadmap_index.py` 30 passed, `tests/ui_server/` 515 passed, `tests/orchestration/test_test_runner.py` 52 passed, `tests/regression/test_resource_safety.py` 21 passed, `tests/orchestration/test_integrity_gate.py` 16 passed, `tests/cli/test_golden_path.py` (canary) 42 passed — all seven counts identical to the worker's own reading, nothing moved. G6 THE TREE, THE COMMITS AND THE SWEEP HELD: `git status --porcelain` empty, `git ls-files .remedy-wt` empty, all four pre-handback commits' `+` numstat cells (248/236/30/1/41) matched the handback's own Commits table cell for cell, reproduced independently; the staleness sweep found nothing stale outside the change set. No finding was registered or resolved this round — the registered/Done counts (354/76) are unmoved both sides. Branch `feature/f114-cost-preview-per-command` is pushed and matches `origin` head-for-head; `git status --porcelain` reads empty now.
<<<END RECORD1>>>

<<<BEGIN PLAN2>>>
# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 2 books round 1's PASS verdict (RECORD1) and extracts the shared
cost-arithmetic helper: `token_economy.tokens_to_cost_usd()` (new, pure,
None-propagating) replaces the inlined multiply at
`budget_guard.py:482-484` inside `predict_next_task_cost`, which now
calls it. Round 1's plan text named the wrong regression suite
(`test_budget_guard.py`); the real coverage of `predict_next_task_cost`
is `tests/orchestration/test_predictive_budget.py`, and the new
function's own unit tests land in
`tests/orchestration/test_token_economy.py` (both suites, plus
`test_budget_guard.py` itself, gate this round).

## Next Steps

- Round 3: `packages/orchestration/cost_preview.py` (`estimate_cost_band`,
  band computation from `PredictiveBudgetConfig`'s per-`TokenBand` class
  defaults, basis labels, "estimate unavailable" when no price basis) +
  `tests/orchestration/test_cost_preview.py` — completes T001.
- T002: CLI helper (`apps/cli`) — threshold confirm, tty/non-tty
  semantics (pipe never hangs), `--yes` audited, reusing
  `loop_cmd.py`'s `_confirm_materialization`/`_stdin_is_a_tty` pattern.
- T003: mark expensive commands in `apps/cli/command_catalog.py`,
  goldens for preview lines, docs.

## Risks

- No `cost_preview.py` or expensive-command registry exists yet — T003
  is greenfield, not a rename.
- The estimator commits to `token_economy.TokenBand`, distinct from
  `model_routing.TASK_CLASS_TIERS` (round 3 states which and why).
<<<END PLAN2>>>

<<<BEGIN TE PAIR FROM>>>
def _now() -> str:
<<<END TE PAIR FROM>>>

<<<BEGIN TE PAIR TO>>>
def tokens_to_cost_usd(tokens: int | None, price_basis_usd_per_1k_tokens: float | None) -> float | None:
    """Convert a token count to a USD cost at a given per-1k-token price.

    ``None`` propagates rather than becoming a fabricated 0.0: an unmeasured
    token count or an unset price basis (P6, the hard rule this module states
    at its top — no invented pricing) both mean no cost can be computed.
    """
    if tokens is None or price_basis_usd_per_1k_tokens is None:
        return None
    return tokens / 1000 * price_basis_usd_per_1k_tokens


def _now() -> str:
<<<END TE PAIR TO>>>

<<<BEGIN BG PAIR FROM>>>
    expected_cost_usd: float | None = None
    if expected_tokens is not None and price_basis is not None:
        expected_cost_usd = expected_tokens / 1000 * price_basis
<<<END BG PAIR FROM>>>

<<<BEGIN BG PAIR TO>>>
    expected_cost_usd = token_economy.tokens_to_cost_usd(expected_tokens, price_basis)
<<<END BG PAIR TO>>>

<<<BEGIN TEST PAIR FROM>>>
    def test_no_execution_or_apply(self):
        src = self._src()
        for bad in ("os.system", "Popen", "check_output", "do_continue(", "apply_patch(",
                    ".approve(", "os.fork", "eval(", "exec("):
            assert bad not in src, bad
<<<END TEST PAIR FROM>>>

<<<BEGIN TEST PAIR TO>>>
    def test_no_execution_or_apply(self):
        src = self._src()
        for bad in ("os.system", "Popen", "check_output", "do_continue(", "apply_patch(",
                    ".approve(", "os.fork", "eval(", "exec("):
            assert bad not in src, bad


# ---------------------------------------------------------------------------
# tokens_to_cost_usd (F114 T001 — extracted from budget_guard.predict_next_task_cost)
# ---------------------------------------------------------------------------


class TestTokensToCostUsd:
    def test_ordinary_multiply(self):
        # 8000 tokens x $0.02/1k = $0.16 — the exact figure
        # test_predictive_budget.py's TestBreachBoundary pins for the same inputs.
        assert te.tokens_to_cost_usd(8000, 0.02) == 0.16

    def test_zero_tokens_is_a_measured_zero_not_none(self):
        assert te.tokens_to_cost_usd(0, 0.02) == 0.0

    def test_none_tokens_propagates_none(self):
        assert te.tokens_to_cost_usd(None, 0.02) is None

    def test_none_price_basis_propagates_none(self):
        assert te.tokens_to_cost_usd(8000, None) is None

    def test_both_none_propagates_none(self):
        assert te.tokens_to_cost_usd(None, None) is None
<<<END TEST PAIR TO>>>