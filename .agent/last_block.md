STEP T003 PART 1 (MARKING ONLY) / ROUND 6 - F114 Cost preview per command
FEATURE F114 - Cost preview per command (Tier 3) - SESSION 2, ROUND 6

Goal
  Book round 5's PASS verdict into the ledger (RECORD5) and start T003's
  first slice: mark which commands are expensive. Add `is_expensive:
  bool = False` to `CommandEntry` (apps/cli/command_catalog.py) and mark
  `job.run` as the first and only expensive command so far. Catalog
  tests confirm the field's type and that exactly job.run carries it.
  Wiring `confirm_cost_preview()` into a real command's execution path,
  goldens, and docs are NOT this round - see constraint 6.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f114-r6.md
  C0b mirror it to .agent/last_block.md
  C1  apply RECORD5 to .agent/live_review.md (append) and PLAN6 to
      .agent/plan.md (whole-file replacement)
  C2  apply FIELD PAIR and MARK PAIR to apps/cli/command_catalog.py, and
      TEST PAIR to tests/test_command_catalog.py
  C3  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f114-r6.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md (C1) - .agent/plan.md (C1) -
  apps/cli/command_catalog.py (C2) -
  tests/test_command_catalog.py (C2) - .agent/handoff.md (C3)

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by
     delimiter index from the COMMITTED .agent/authored/f114-r6.md -
     marker lines EXCLUDED - and write it with a script, never by
     retyping. If a slice looks wrong, apply it as written and DECLARE it
     in the handback.
  2. C1 is the first substantive commit of the round.
  3. RECORD5 appends to .agent/live_review.md as EXACTLY ONE newline byte
     followed by the slice (the file's own current convention, same as
     every prior round's own G2 measurement). PLAN6 REPLACES
     .agent/plan.md whole.
  4. NEWLINE CONVENTION, STATED EXPLICITLY: RECORD5 and PLAN6 carry NO
     trailing newline of their own (matching this round's own scratch
     originals and .agent/plan.md's pre-round convention). FIELD PAIR
     FROM/TO and MARK PAIR FROM/TO each carry their OWN trailing newline
     as the true last byte of the matched line group - a byte-exact
     structural suffix of the file, not marker-line formatting (same
     class as round 4's own CONFIG PAIR). TEST PAIR FROM/TO likewise
     each carry their own trailing newline as their real last byte.
  5. FIELD PAIR IS A REWRITE (the new field line is inserted BETWEEN
     `may_execute_commands: bool = False,` and `related: tuple[str,
     ...] = (),` - same shape as F114 R4's own IMPORT PAIR): verify FROM
     count is exactly 1 in command_catalog.py before C2, apply
     str.replace(FROM, TO, 1), confirm "TO contains FROM: false". MARK
     PAIR IS ALSO A REWRITE, same reasoning (the new `is_expensive=True,`
     line is inserted between two existing lines of job.run's own
     CommandEntry call): confirm "TO contains FROM: false" for it too.
     TEST PAIR IS ALSO A REWRITE, same reasoning (the new class is
     inserted BETWEEN TestCatalogClassification's own last method and
     `class TestCatalogSensitivity:`, so FROM's own trailing anchor line
     is not a prefix of TO): confirm "TO contains FROM: false" for it
     too.
  6. Do NOT wire confirm_cost_preview() into job.py or any command's
     real execution path, and do NOT touch
     apps/cli/commands/job.py, packages/orchestration/cost_preview.py,
     apps/cli/cost_preview_confirm.py, or tests/cli/test_cost_preview.py
     (which does not exist yet) - that is T003's next slice, gated on
     designing how job.run gathers task-count/class data for a real
     CostBandEstimate, which is separate, larger work. A command marked
     is_expensive with zero confirm-path callers yet is expected at this
     stage, not a "dead code" defect - G6's red-proof is what proves the
     flag is real despite having no caller yet.
  7. Apply FIELD PAIR before MARK PAIR to command_catalog.py, as TWO
     SEPARATE str.replace calls on the same file (FIELD PAIR's FROM is
     nearer the top of the file and unaffected by MARK PAIR's own edit
     further down).
  8. ruff is DENIED to this session (measured at every round since
     F114's claim); gate with `python3 -m py_compile` on
     apps/cli/command_catalog.py and tests/test_command_catalog.py
     instead, and ATTEMPT `ruff check` on both, reporting the real
     output or the exact refusal text - never assume either way.
  9. A sentence OUTSIDE the change set that this round makes stale is
     DECLARED in the handback and NOT repaired. Rounds 2 and 3's own
     `.agent/context.md` declarations (lines 29 and 36) stand; do not
     repeat them.
  10. Read .agent/STOP from disk before the first commit and again
      before C3. If it exists, finish the commit in hand, write the
      handback, and stop.
  11. Self-review loop before every commit (git diff --stat, git diff).
      Push after C3. No pull request, no merge this round - T003 having
      only its first slice land does not by itself trigger the Open PR
      Gate; that waits for T003's full scope and the acceptance
      fixtures.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f114-r6.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE LEDGER APPEND. Base size of .agent/live_review.md immediately
     BEFORE C1 (measure it yourself): report its byte length and whether
     it ends with a trailing newline. RECORD5 has ZERO internal
     newlines - report its own byte length. Report: base + 1 +
     len(RECORD5) and whether that equals the post-C1 file's byte length
     (expected 2367783, from a base of 2364059
     and a RECORD5 of 3723 bytes - recompute both independently).
     Then the SECOND reader: report whether the post-C1 file's bytes from
     `base` to the end equal exactly `"\n" + RECORD5`. Then a NEGATIVE
     CONTROL in a scratch copy ONLY (never the tracked file): flip one
     byte inside RECORD5's own text and report the second reader REJECTS it.
  G3 THE PLAN. Extract PLAN6 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md            -> exit 0
       wc -l .agent/plan.md                      -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G4 THE THREE CATALOG PAIRS. For EACH of FIELD PAIR, MARK PAIR and TEST
     PAIR: report the FROM count in its target file immediately BEFORE
     C2 (must be exactly 1 for all three - FIELD PAIR and MARK PAIR both
     target command_catalog.py, so re-count FIELD PAIR's FROM in the file
     BEFORE MARK PAIR is applied, per constraint 7's ordering), and after
     C2 report the containment test's own output in these words - "TO
     contains FROM: true" or "TO contains FROM: false" - matching
     constraint 5 exactly (all three pairs are REWRITES this round, so
     all three report "false"). Then extract each slice from the COMMITTED
     authored file and cmp the target file's actual new content against
     what applying str.replace in the constraint-7 order to a pre-C2
     scratch copy of each target produces - exit 0 for both target files
     (command_catalog.py takes two pairs, test_command_catalog.py takes
     one).
  G5 COMPILE AND LINT. `python3 -m py_compile` on
     apps/cli/command_catalog.py and tests/test_command_catalog.py ->
     exit 0 each. Then ATTEMPT `ruff check apps/cli/command_catalog.py
     tests/test_command_catalog.py` and report the real result, success
     or refusal text, verbatim.
  G6 THE RED-PROOF, INSIDE A DISPOSABLE GIT WORKTREE ONLY (never the
     primary checkout - self_drive_protocol.md guardrail G5). After C2,
     from the round's own HEAD: create a scratch worktree, inside it
     remove the `is_expensive=True,` line from job.run's own
     CommandEntry (reverting it to the field's default False - a
     one-line removal), then run
       python3 -m pytest tests/test_command_catalog.py -q
     and report the failure count (must be greater than zero - name
     which tests failed; expect exactly 2:
     TestCatalogExpensive::test_exactly_job_run_is_marked_expensive_so_far
     and TestCatalogExpensive::test_job_run_is_expensive). Then restore
     the line inside that same worktree, re-run the same command and
     report it fully green again (21 passed - the unmutated control).
     Remove the worktree when done (`git worktree remove --force`) - it
     must not exist at G8's tree check.
  G7 THE SUITES, EACH AS ITS OWN INVOCATION, RUN SERIALLY, IN THE PRIMARY
     CHECKOUT:
       python3 -m pytest tests/test_command_catalog.py -q
       python3 -m pytest tests/cli/test_command_catalog.py -q
       python3 -m pytest tests/orchestration/test_job_task_runner.py -q
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
     The last is the canary. test_command_catalog.py is expected at 21
     passed (18 existing + 3 new); tests/cli/test_command_catalog.py and
     tests/orchestration/test_job_task_runner.py are moved-count checks
     against the reviewer's own independent base reading of 23 and 214
     respectively - report what you actually measured, not what you
     expect; every other count is likewise a moved-count check.
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
RECORD5, PLAN6, FIELD PAIR FROM/TO, MARK PAIR FROM/TO and TEST PAIR
FROM/TO.

<<<BEGIN RECORD5>>>
Gate: F114 R5 — the round 5 entry, ships apps/cli/cost_preview_confirm.py (render_estimate_line, confirm_cost_preview, EXIT_USAGE) and tests/cli/test_cost_preview_confirm.py (T002 complete), no ledger findings. VERDICT PASS, over the range `99157a070a2d7291332c16071246e8960cfffc34..2e7e0090715562a7794b22a6b5ded313c3227c65` (commits C0a `487a8ac8271a95630b3eb65f715fae3affcdd6a7`, C0b `3f70577458ad70ab950a1103772cd6935e9b568e`, C1 `67a4a73c897934b1128b72a2a39ff987f1a60267`, C2 `27c3acc4da827e52d23e618a8587cbfef0f8dc5f` — four real content commits — plus handback commit `2e7e0090715562a7794b22a6b5ded313c3227c65`), independently re-verified by the reviewer. TRANSPORT HELD: `sha256sum .agent/authored/f114-r5.md .agent/last_block.md` both print `c029bef2dc53322be7602053545274fccf93df1905b0ba12bb496d4a461438a5`, reproduced directly. G2 THE LEDGER APPEND HELD: base 2360277 bytes (no trailing newline), RECORD4 3781 bytes, base + 1 + 3781 = 2364059, matching the post-C1 file's measured length exactly; the second reader's tail slice equalled `\n` + RECORD4 byte for byte, and a one-byte-flipped negative control was correctly rejected — all reproduced independently. G3 THE PLAN HELD BYTE-EXACT: PLAN5 extracted from the committed authored file `cmp`s exit 0 against `.agent/plan.md` (37 lines, under 50; `## Goal`/`## Next Steps` each exactly once), reproduced independently. G4 THE TWO NEW FILES HELD: MODULE and TESTMODULE extracted from the committed authored file `cmp` exit 0 against `apps/cli/cost_preview_confirm.py` (2541 bytes) and `tests/cli/test_cost_preview_confirm.py` (4744 bytes) respectively, reproduced independently. G5 HELD: `python3 -m py_compile` exit 0 on both new files, reproduced; `ruff check` was denied to this session, same refusal text as every prior round. G6 THE RED-PROOF HELD, REPRODUCED INDEPENDENTLY IN A SEPARATE DISPOSABLE WORKTREE: the reviewer's own `>` to `<` mutation on `confirm_cost_preview`'s comparison produced the identical six failing tests the worker reported (`TestUnderThreshold::test_under_threshold_proceeds_without_any_prompt`, `TestUnderThreshold::test_under_threshold_never_touches_stdin`, `TestOverThresholdWithYes::test_yes_skips_the_prompt_and_proceeds`, `TestOverThresholdNonTty::test_non_tty_exits_with_usage_code_never_hangs`, `TestOverThresholdNonTty::test_non_tty_never_calls_input`, `TestOverThresholdTty::test_tty_declining_returns_false_without_raising`), proving `is_expensive`'s comparison is real, reachable code; reverted, 12 passed again; worktree removed after. G7 THE SUITES, REPRODUCED INDEPENDENTLY BY THE REVIEWER at this round's own HEAD, all twelve counts identical to the worker's own reading: `test_cost_preview_confirm.py` 12, `test_loop_cmd.py` 14, `test_no_interactive_guard.py` 6, `test_cost_preview.py` 19, `test_config.py` 81, `tests/docs/` 295, `test_roadmap_index.py` 30, `tests/ui_server/` 515, `test_test_runner.py` 52, `test_resource_safety.py` 21, `test_integrity_gate.py` 16, `test_golden_path.py` (canary) 42 — nothing moved outside this round's own six new tests. G8 HELD: `git status --porcelain` empty, `git ls-files .remedy-wt` empty, no leftover scratch worktree, all four pre-handback commits' numstat `+` cells matched the handback's own Commits table cell for cell, reproduced independently. ZERO DEVIATIONS WERE DECLARED by the worker and the reviewer found none either. No finding is registered; nothing is wrong on disk. Both `cost_preview_confirm.py` functions have zero CLI callers yet, exactly as expected at this stage of T002 — T003 wires a real command next. Branch `feature/f114-cost-preview-per-command` is pushed and matches `origin` head-for-head; `git status --porcelain` reads empty now.
<<<END RECORD5>>>

<<<BEGIN PLAN6>>>
# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 6 books round 5's PASS verdict (RECORD5) and starts T003's first
slice: marking which commands are expensive. Adds `is_expensive: bool =
False` to `CommandEntry` (apps/cli/command_catalog.py) and marks
`job.run` (the feature doc's "mission runs" case) as the first and only
expensive command so far. Catalog tests in tests/test_command_catalog.py
assert the field's type, that exactly `job.run` is marked, and that
`job.run.is_expensive` is True. This round does NOT wire
`confirm_cost_preview()` into `job.run`'s real execution path yet -
`_cmd_job_run_cycles` (apps/cli/commands/job.py) has no task-count/class
data to build a `CostBandEstimate` from today, and that data-gathering
design is separate, larger work.

## Next Steps

- T003 continuation: gather real task-count/class data for `job.run`
  (see `packages/orchestration/token_economy.py`'s `TokenBand`
  classification and `budget_guard.py`'s `predict_next_task_cost` for
  the existing analogous consumer pattern), then wire
  `confirm_cost_preview()` into `_cmd_job_run_cycles`
  (apps/cli/commands/job.py).
- T003 continuation: goldens for the preview line, docs
  (docs/roadmap/features/T3_F114.md's "Suggested tests:
  tests/cli/test_cost_preview.py" path does not exist yet).
- Acceptance fixtures, the integration gate, then the closure sequence.
- Session note: this is round 6, session 2 of F114 (session 1 closed at
  round 5 per amend0827 rule 6's 4-5 default).

## Risks

- `job.run` is marked expensive but still has zero confirm-path callers
  after this round - same "proven live only by mutation red-proof, not a
  real caller yet" shape as T001/T002's modules, now also true of the
  catalog flag itself until the next round wires it.
- Only one command is marked so far; the feature doc's "rerunning
  subtrees" and "long explanations" cases still need their own fixture
  commands identified before they can be marked too.
<<<END PLAN6>>>

<<<BEGIN FIELD PAIR FROM>>>
    action_class: ActionClass
    args: tuple[ArgDef, ...] = ()
    supports_json: bool = False
    requires_permission: bool = False
    may_mutate_repo: bool = False
    may_execute_commands: bool = False
    related: tuple[str, ...] = ()
<<<END FIELD PAIR FROM>>>

<<<BEGIN FIELD PAIR TO>>>
    action_class: ActionClass
    args: tuple[ArgDef, ...] = ()
    supports_json: bool = False
    requires_permission: bool = False
    may_mutate_repo: bool = False
    may_execute_commands: bool = False
    #: True marks a command whose real-money spend requires an upfront
    #: estimate and, above a configured threshold, operator confirmation
    #: before it runs (F114). Explicit and reviewable per command - never
    #: derived from another flag such as may_execute_commands.
    is_expensive: bool = False
    related: tuple[str, ...] = ()
<<<END FIELD PAIR TO>>>

<<<BEGIN MARK PAIR FROM>>>
        supports_json=True,
        may_execute_commands=True,
        related=("job.run-next", "job.plan", "decision.list"),
    ),
<<<END MARK PAIR FROM>>>

<<<BEGIN MARK PAIR TO>>>
        supports_json=True,
        may_execute_commands=True,
        is_expensive=True,
        related=("job.run-next", "job.plan", "decision.list"),
    ),
<<<END MARK PAIR TO>>>

<<<BEGIN TEST PAIR FROM>>>
    def test_mutating_commands_flagged(self) -> None:
        """Commands that may_mutate_repo or may_execute_commands must not be read_only."""
        for cmd in CATALOG:
            if cmd.may_mutate_repo or cmd.may_execute_commands:
                assert cmd.action_class != "read_only", (
                    f"{cmd.command_id} mutates/executes but is classified as read_only"
                )


class TestCatalogSensitivity:
<<<END TEST PAIR FROM>>>

<<<BEGIN TEST PAIR TO>>>
    def test_mutating_commands_flagged(self) -> None:
        """Commands that may_mutate_repo or may_execute_commands must not be read_only."""
        for cmd in CATALOG:
            if cmd.may_mutate_repo or cmd.may_execute_commands:
                assert cmd.action_class != "read_only", (
                    f"{cmd.command_id} mutates/executes but is classified as read_only"
                )


class TestCatalogExpensive:
    """F114 T003 - is_expensive is explicit and reviewable, never inferred."""

    def test_is_expensive_is_a_bool_on_every_entry(self) -> None:
        for cmd in CATALOG:
            assert isinstance(cmd.is_expensive, bool), (
                f"{cmd.command_id}.is_expensive must be a bool"
            )

    def test_exactly_job_run_is_marked_expensive_so_far(self) -> None:
        marked = sorted(cmd.command_id for cmd in CATALOG if cmd.is_expensive)
        assert marked == ["job.run"], (
            f"F114 T003 has only marked job.run so far; found {marked}"
        )

    def test_job_run_is_expensive(self) -> None:
        assert get_command("job.run").is_expensive is True


class TestCatalogSensitivity:
<<<END TEST PAIR TO>>>
