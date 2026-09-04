STEP T003 PART 2 (--yes ARG ONLY) / ROUND 7 - F114 Cost preview per command
FEATURE F114 - Cost preview per command (Tier 3) - SESSION 2, ROUND 7

Goal
  Book round 6's PASS verdict into the ledger (RECORD6) and continue
  T003: add a `--yes` arg to job.run's own CommandEntry
  (apps/cli/command_catalog.py), mirroring loop.run's own --yes shape,
  so the future confirm call has a real flag to skip its prompt. A
  catalog test confirms the arg exists and is a flag. Wiring
  confirm_cost_preview() into _cmd_job_run_cycles itself is NOT this
  round - see constraint 6.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f114-r7.md
  C0b mirror it to .agent/last_block.md
  C1  apply RECORD6 to .agent/live_review.md (append) and PLAN7 to
      .agent/plan.md (whole-file replacement)
  C2  apply YES_ARG PAIR to apps/cli/command_catalog.py and YES_TEST
      PAIR to tests/test_command_catalog.py
  C3  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f114-r7.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md (C1) - .agent/plan.md (C1) -
  apps/cli/command_catalog.py (C2) -
  tests/test_command_catalog.py (C2) - .agent/handoff.md (C3)

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by
     delimiter index from the COMMITTED .agent/authored/f114-r7.md -
     marker lines EXCLUDED - and write it with a script, never by
     retyping. If a slice looks wrong, apply it as written and DECLARE it
     in the handback.
  2. C1 is the first substantive commit of the round.
  3. RECORD6 appends to .agent/live_review.md as EXACTLY ONE newline byte
     followed by the slice (the file's own current convention, same as
     every prior round's own G2 measurement). PLAN7 REPLACES
     .agent/plan.md whole.
  4. NEWLINE CONVENTION, STATED EXPLICITLY: RECORD6 and PLAN7 carry NO
     trailing newline of their own (matching this round's own scratch
     originals and .agent/plan.md's pre-round convention). YES_ARG PAIR
     FROM/TO and YES_TEST PAIR FROM/TO each carry their OWN trailing
     newline as the true last byte of the matched line group - a
     byte-exact structural suffix of the file, not marker-line
     formatting (same class as round 6's own FIELD/MARK/TEST pairs).
  5. BOTH PAIRS ARE REWRITES this round (verified mechanically before
     this block was authored - do not assume, recheck): YES_ARG PAIR
     inserts a new ArgDef BETWEEN the existing --unattended ArgDef and
     _JSON_OPT in job.run's own args tuple; YES_TEST PAIR inserts a new
     test method BETWEEN test_job_run_is_expensive and
     `class TestCatalogSensitivity:`. For EACH pair: verify FROM count is
     exactly 1 in its target file before C2, apply
     str.replace(FROM, TO, 1), confirm "TO contains FROM: false".
  6. Do NOT touch apps/cli/commands/job.py,
     packages/orchestration/cost_preview.py, or
     apps/cli/cost_preview_confirm.py this round - wiring the real
     confirm_cost_preview() call into _cmd_job_run_cycles is round 8,
     once this round's --yes arg exists for it to read. A --yes arg with
     no caller reading it yet is expected at this stage, not a "dead
     code" defect - G6's red-proof is what proves the arg is real
     catalog data despite having no runtime reader yet.
  7. ruff is DENIED to this session (measured at every round since
     F114's claim); gate with `python3 -m py_compile` on
     apps/cli/command_catalog.py and tests/test_command_catalog.py
     instead, and ATTEMPT `ruff check` on both, reporting the real
     output or the exact refusal text - never assume either way.
  8. A sentence OUTSIDE the change set that this round makes stale is
     DECLARED in the handback and NOT repaired. Rounds 2 and 3's own
     `.agent/context.md` declarations (lines 29 and 36) stand; do not
     repeat them.
  9. Read .agent/STOP from disk before the first commit and again
     before C3. If it exists, finish the commit in hand, write the
     handback, and stop.
  10. Self-review loop before every commit (git diff --stat, git diff).
      Push after C3. No pull request, no merge this round - a schema-only
      --yes arg does not by itself trigger the Open PR Gate; that waits
      for T003's full scope and the acceptance fixtures.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f114-r7.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE LEDGER APPEND. Base size of .agent/live_review.md immediately
     BEFORE C1 (measure it yourself): report its byte length and whether
     it ends with a trailing newline. RECORD6 has ZERO internal
     newlines - report its own byte length. Report: base + 1 +
     len(RECORD6) and whether that equals the post-C1 file's byte length
     (expected 2371519, from a base of 2367783
     and a RECORD6 of 3735 bytes - recompute both independently).
     Then the SECOND reader: report whether the post-C1 file's bytes from
     `base` to the end equal exactly `"\n" + RECORD6`. Then a NEGATIVE
     CONTROL in a scratch copy ONLY (never the tracked file): flip one
     byte inside RECORD6's own text and report the second reader REJECTS it.
  G3 THE PLAN. Extract PLAN7 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md            -> exit 0
       wc -l .agent/plan.md                      -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G4 THE TWO PAIRS. For EACH of YES_ARG PAIR and YES_TEST PAIR: report
     the FROM count in its target file immediately BEFORE C2 (must be
     exactly 1 for both), and after C2 report the containment test's own
     output in these words - "TO contains FROM: true" or "TO contains
     FROM: false" - matching constraint 5 exactly (both report "false").
     Then extract each slice from the COMMITTED authored file and cmp
     the target file's actual new content against what applying
     str.replace to a pre-C2 scratch copy of each target produces - exit
     0 for both target files.
  G5 COMPILE AND LINT. `python3 -m py_compile` on
     apps/cli/command_catalog.py and tests/test_command_catalog.py ->
     exit 0 each. Then ATTEMPT `ruff check apps/cli/command_catalog.py
     tests/test_command_catalog.py` and report the real result, success
     or refusal text, verbatim.
  G6 THE RED-PROOF, INSIDE A DISPOSABLE GIT WORKTREE ONLY (never the
     primary checkout - self_drive_protocol.md guardrail G5). After C2,
     from the round's own HEAD: create a scratch worktree, inside it
     remove the new `--yes` ArgDef line group from job.run's own args
     tuple (reverting it to round 6's shape), then run
       python3 -m pytest tests/test_command_catalog.py -q
     and report the failure count (must be greater than zero - name
     which test failed; expect exactly 1:
     TestCatalogExpensive::test_job_run_has_a_yes_flag_to_skip_the_cost_confirmation).
     Then restore the ArgDef inside that same worktree, re-run the same
     command and report it fully green again (22 passed - the unmutated
     control). Remove the worktree when done (`git worktree remove
     --force`) - it must not exist at G8's tree check.
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
     The last is the canary. test_command_catalog.py is expected at 22
     passed (21 existing + 1 new); every other count is a moved-count
     check against the reviewer's own independent base reading of round
     6's own G7 figures - report what you actually measured, not what
     you expect.
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
RECORD6, PLAN7, YES_ARG PAIR FROM/TO and YES_TEST PAIR FROM/TO.

<<<BEGIN RECORD6>>>
Gate: F114 R6 — the round 6 entry, adds is_expensive field to CommandEntry and marks job.run (T003 first slice), no ledger findings. VERDICT PASS, over the range `2e7e0090715562a7794b22a6b5ded313c3227c65..a886072b844566fb40757c036f8750e3a4f39090` (commits C0a `6b415998d1d0023ef09a9112ff77527261cb9798`, C0b `b025ca6ed343a35e3ceb809a54aa34bd0d1c5a3d`, C1 `8f79f31b9c6b6ae86cfe6c6985401c1404c7b9b5`, C2 `10c7b3240e87920c470c9c45829d0ba6ec21265e` — four real content commits — plus handback commit `a886072b844566fb40757c036f8750e3a4f39090`), independently re-verified by the reviewer. TRANSPORT HELD: `sha256sum .agent/authored/f114-r6.md .agent/last_block.md` both print `fabe2098d8505810ffc1cfbddbd9516acc284db32d0f76bd8db92e6fc87d318a`, reproduced directly. G2 THE LEDGER APPEND HELD: base 2364059 bytes (no trailing newline), RECORD5 3723 bytes, base + 1 + 3723 = 2367783, matching the post-C1 file's measured length exactly; the second reader's tail slice equalled `\n` + RECORD5 byte for byte, and a one-byte-flipped negative control was correctly rejected — all reproduced independently. G3 THE PLAN HELD BYTE-EXACT: PLAN6 extracted from the committed authored file `cmp`s exit 0 against `.agent/plan.md` (49 lines, under 50; `## Goal`/`## Next Steps` each exactly once), reproduced independently. G4 THE THREE CATALOG PAIRS HELD: the reviewer independently reconstructed `apps/cli/command_catalog.py` and `tests/test_command_catalog.py` by applying FIELD PAIR then MARK PAIR, and TEST PAIR respectively, to pre-C2 scratch copies, and found both byte-identical to the real committed files — all three pairs correctly classified as rewrites (`TO contains FROM: false` for all three; the worker's own draft-time self-check that misclassified TEST PAIR as an append due to a `TEST_FROM in TEST_FROM` typo was caught and corrected by the reviewer BEFORE the block was authored, so the shipped block's constraint 5 and G4 wording were already right). G5 HELD: `python3 -m py_compile` exit 0 on both files, reproduced; `ruff check` produced the same session-level denial text every prior round has quoted, reproduced verbatim. G6 THE RED-PROOF HELD, REPRODUCED INDEPENDENTLY IN A SEPARATE DISPOSABLE WORKTREE: removing `is_expensive=True,` from job.run's own entry produced the identical two failing tests the worker reported (`TestCatalogExpensive::test_exactly_job_run_is_marked_expensive_so_far`, `TestCatalogExpensive::test_job_run_is_expensive`), proving the mark is real, reachable data; reverted, 21 passed again; worktree removed after. G7 THE SUITES, REPRODUCED INDEPENDENTLY BY THE REVIEWER at this round's own HEAD, all ten counts identical to the worker's own reading: `test_command_catalog.py` 21, `test_command_catalog.py` (cli) 23, `test_job_task_runner.py` 214, `tests/docs/` 295, `test_roadmap_index.py` 30, `tests/ui_server/` 515, `test_test_runner.py` 52, `test_resource_safety.py` 21, `test_integrity_gate.py` 16, `test_golden_path.py` (canary) 42 — nothing moved outside this round's own three new tests. G8 HELD: `git status --porcelain` empty, `git ls-files .remedy-wt` empty, no leftover scratch worktree, all four pre-handback commits' numstat `+` cells matched the handback's own Commits table cell for cell, reproduced independently. ZERO DEVIATIONS WERE DECLARED by the worker and the reviewer found none either. No finding is registered; nothing is wrong on disk. `job.run` is marked is_expensive with zero confirm-path callers yet, exactly as expected at this stage of T003's first slice — the next slice adds a `--yes` arg and wires the real confirm call. Branch `feature/f114-cost-preview-per-command` is pushed and matches `origin` head-for-head; `git status --porcelain` reads empty now.
<<<END RECORD6>>>

<<<BEGIN PLAN7>>>
# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 7 books round 6's PASS verdict (RECORD6) and continues T003:
`job.run` gets a new `--yes` arg (`apps/cli/command_catalog.py`),
mirroring `loop.run`'s own `--yes` shape, to skip the cost-preview
confirmation prompt. A catalog test confirms it exists and is a flag.
This round still does NOT call `confirm_cost_preview()` from
`_cmd_job_run_cycles` - investigation found `job.run` has no per-task
class data before it starts (no `TokenBand` classification happens until
a task is pulled), so the real estimate `job.run` can honestly build is
"unavailable" (`band_usd_high=None`), which A9 already treats as
expensive - always confirm unless `--yes` or `--unattended`. Wiring that
call is round 8, once `--yes` exists for it to reference.

## Next Steps

- T003 continuation (round 8): import `confirm_cost_preview` and
  `CostBandEstimate` into `apps/cli/commands/job.py`; call it once near
  the top of `_cmd_job_run_cycles`, before either the single-cycle
  short-circuit (`_cmd_run_next_task_local`) or the full `run_cycles`
  path, with `basis="estimate_unavailable"` and
  `yes=(yes_flag or unattended)` - `--unattended` maps to skip-prompt
  because the feature doc requires unattended runs to never prompt and
  rely on budgets instead (T3_F114.md's own explicit rule).
- T003 continuation: goldens for the preview line, docs.
- Acceptance fixtures, the integration gate, then the closure sequence.
- Session note: round 7, session 2 of F114.

## Risks

- `job.run`'s `--yes` arg exists after this round but has zero real
  effect until round 8 wires the confirm call - same "schema before
  behavior" shape as round 6's own `is_expensive` mark.
- The "estimate unavailable" design means job.run will ALWAYS show the
  cost-preview prompt (or need --yes/--unattended) once wired, never a
  real dollar band, until a future round teaches it to classify pending
  tasks before running. This is honest (A9: unknown is expensive), not a
  shortcut, but it is a real UX gap worth flagging to the operator.
<<<END PLAN7>>>

<<<BEGIN YES_ARG PAIR FROM>>>
            ArgDef("--unattended",
                   "Run without a human present: a task decision that carries a safe "
                   "default is auto-answered from it and recorded in the escalation "
                   "assumption log. A question with no safe default still waits.",
                   required=False, is_option=True, is_flag=True),
            _JSON_OPT,
<<<END YES_ARG PAIR FROM>>>

<<<BEGIN YES_ARG PAIR TO>>>
            ArgDef("--unattended",
                   "Run without a human present: a task decision that carries a safe "
                   "default is auto-answered from it and recorded in the escalation "
                   "assumption log. A question with no safe default still waits.",
                   required=False, is_option=True, is_flag=True),
            ArgDef("--yes", "Skip the cost-preview confirmation prompt above the "
                            "configured threshold (F114). Never bypasses budget "
                            "limits or the escalation log.",
                   required=False, is_option=True, is_flag=True),
            _JSON_OPT,
<<<END YES_ARG PAIR TO>>>

<<<BEGIN YES_TEST PAIR FROM>>>
    def test_job_run_is_expensive(self) -> None:
        assert get_command("job.run").is_expensive is True


class TestCatalogSensitivity:
<<<END YES_TEST PAIR FROM>>>

<<<BEGIN YES_TEST PAIR TO>>>
    def test_job_run_is_expensive(self) -> None:
        assert get_command("job.run").is_expensive is True

    def test_job_run_has_a_yes_flag_to_skip_the_cost_confirmation(self) -> None:
        args = get_command("job.run").args
        yes_args = [a for a in args if a.name == "--yes"]
        assert len(yes_args) == 1, "job.run must declare exactly one --yes arg"
        assert yes_args[0].is_flag is True, "job.run's --yes must be a flag, not a valued option"


class TestCatalogSensitivity:
<<<END YES_TEST PAIR TO>>>
