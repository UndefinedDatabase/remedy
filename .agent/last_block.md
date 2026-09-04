STEP T003 PART 4 (ACCEPTANCE TESTS, REAL GATE) / ROUND 9 - F114 Cost preview per command
FEATURE F114 - Cost preview per command (Tier 3) - SESSION 2, ROUND 9

Goal
  Book round 8's PASS verdict into the ledger (RECORD8) and add
  tests/cli/test_cost_preview.py - the feature doc's own suggested
  acceptance-test path, empty until now. Five tests exercise the REAL
  confirm_cost_preview end to end through job.run (not mocked, unlike
  round 8's own gate tests): a non-tty pipe without --yes exits with
  code 2 and names job.run in its hint, --yes and --unattended both
  proceed through the real gate without a tty, and the printed line
  always carries its basis label. No production code changes this round.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f114-r9.md
  C0b mirror it to .agent/last_block.md
  C1  apply RECORD8 to .agent/live_review.md (append) and PLAN9 to
      .agent/plan.md (whole-file replacement)
  C2  write tests/cli/test_cost_preview.py per TESTMODULE (new file)
  C3  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f114-r9.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md (C1) - .agent/plan.md (C1) -
  tests/cli/test_cost_preview.py (new, C2) - .agent/handoff.md (C3)

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by
     delimiter index from the COMMITTED .agent/authored/f114-r9.md -
     marker lines EXCLUDED - and write it with a script, never by
     retyping. If a slice looks wrong, apply it as written and DECLARE it
     in the handback.
  2. C1 is the first substantive commit of the round.
  3. RECORD8 appends to .agent/live_review.md as EXACTLY ONE newline byte
     followed by the slice (the file's own current convention, same as
     every prior round's own G2 measurement). PLAN9 REPLACES
     .agent/plan.md whole.
  4. NEWLINE CONVENTION, STATED EXPLICITLY: RECORD8 and PLAN9 carry NO
     trailing newline of their own. TESTMODULE is a real Python source
     file whose OWN trailing newline is its true last byte - a
     byte-exact structural suffix of the file, not marker-line
     formatting (same class as round 5's own MODULE/TESTMODULE).
  5. TESTMODULE IS A WHOLE-FILE WRITE: write its exact bytes with the
     Write tool (a "copyfile", never a text-extraction-and-reflow) and
     verify by extracting TESTMODULE from the committed authored file
     and `cmp` against the written file.
  6. This round does NOT touch apps/cli/commands/job.py,
     packages/orchestration/cost_preview.py, apps/cli/cost_preview_confirm.py,
     apps/cli/command_catalog.py, tests/orchestration/test_long_run_executor.py,
     or tests/orchestration/test_escalation.py - all six already carry
     what this round's new tests exercise, unmodified, from rounds 5-8.
  7. ruff is DENIED to this session (measured at every round since
     F114's claim); gate with `python3 -m py_compile` on the new file
     instead, and ATTEMPT `ruff check` on it, reporting the real output
     or the exact refusal text - never assume either way.
  8. A sentence OUTSIDE the change set that this round makes stale is
     DECLARED in the handback and NOT repaired. Rounds 2 and 3's own
     `.agent/context.md` declarations (lines 29 and 36) stand; do not
     repeat them.
  9. Read .agent/STOP from disk before the first commit and again
     before C3. If it exists, finish the commit in hand, write the
     handback, and stop.
  10. Self-review loop before every commit (git diff --stat, git diff).
      Push after C3. No pull request, no merge this round - a new
      acceptance-test file does not by itself trigger the Open PR Gate;
      that waits for docs and the remaining acceptance items.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f114-r9.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE LEDGER APPEND. Base size of .agent/live_review.md immediately
     BEFORE C1 (measure it yourself): report its byte length and whether
     it ends with a trailing newline. RECORD8 has ZERO internal
     newlines - report its own byte length. Report: base + 1 +
     len(RECORD8) and whether that equals the post-C1 file's byte length
     (expected 2379181, from a base of 2375218
     and a RECORD8 of 3962 bytes - recompute both independently).
     Then the SECOND reader: report whether the post-C1 file's bytes from
     `base` to the end equal exactly `"\n" + RECORD8`. Then a NEGATIVE
     CONTROL in a scratch copy ONLY (never the tracked file): flip one
     byte inside RECORD8's own text and report the second reader REJECTS it.
  G3 THE PLAN. Extract PLAN9 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md            -> exit 0
       wc -l .agent/plan.md                      -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G4 THE NEW FILE. Extract TESTMODULE from the COMMITTED authored file
     and `cmp` against tests/cli/test_cost_preview.py -> exit 0. Report
     the file's byte length (expected 2965 - recompute independently).
  G5 COMPILE AND LINT. `python3 -m py_compile` on
     tests/cli/test_cost_preview.py -> exit 0. Then ATTEMPT `ruff check
     tests/cli/test_cost_preview.py` and report the real result, success
     or refusal text, verbatim.
  G6 THE RED-PROOF, INSIDE A DISPOSABLE GIT WORKTREE ONLY (never the
     primary checkout - self_drive_protocol.md guardrail G5). After C2,
     from the round's own HEAD: create a scratch worktree, inside it
     invert _cmd_job_run_cycles's own `if not confirm_cost_preview(` to
     `if confirm_cost_preview(` (a one-word removal, flips decline/
     approve - the same mutation round 8's own G6 used), then run
       python3 -m pytest tests/cli/test_cost_preview.py -q
     and report the failure count (must be greater than zero - name
     which tests failed; expect exactly 2:
     test_yes_flag_proceeds_through_the_real_gate_without_a_tty and
     test_unattended_proceeds_through_the_real_gate_without_a_tty).
     Then revert the edit inside that same worktree, re-run the same
     command and report it fully green again (5 passed - the unmutated
     control). Remove the worktree when done (`git worktree remove
     --force`) - it must not exist at G8's tree check.
  G7 THE SUITES, EACH AS ITS OWN INVOCATION, RUN SERIALLY, IN THE PRIMARY
     CHECKOUT:
       python3 -m pytest tests/cli/test_cost_preview.py -q
       python3 -m pytest tests/orchestration/test_long_run_executor.py -q
       python3 -m pytest tests/orchestration/test_escalation.py -q
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
     The last is the canary. test_cost_preview.py is expected at 5
     passed (a brand new file); every other count is a moved-count check
     against round 8's own G7 figures - report what you actually
     measured, not what you expect (no production code changed this
     round, so every other count should be IDENTICAL to round 8's own).
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
RECORD8, PLAN9 and TESTMODULE.

<<<BEGIN RECORD8>>>
Gate: F114 R8 — the round 8 entry, wires the real confirm_cost_preview() call into _cmd_job_run_cycles, repairs six existing test call sites, adds two gate tests, no ledger findings. VERDICT PASS, over the range `1f9797ab92bcbceea5c54450154edb5ffdb5d4ae..64de02a69288b65265766c548c8a86f0cbd6bfd5` (commits C0a `296cf38e8a79c8320771253996f00825a7d21b87`, C0b `76e8b85dec101f6bf03d701ff0dae59246907b59`, C1 `400704f0082d1358bcd6bab9d7344b22ddc08fa9`, C2 `bcf70fa4a0d84d108991a890cac6002d180f4dce` — four real content commits — plus handback commit `64de02a69288b65265766c548c8a86f0cbd6bfd5`), independently re-verified by the reviewer. TRANSPORT HELD: `sha256sum .agent/authored/f114-r8.md .agent/last_block.md` both print `0cf4d30469d4f0510c2184d6f5fef916845d63f3427aa780b42e6a7a4162f960`, reproduced directly. G2 THE LEDGER APPEND HELD: base 2371519 bytes (no trailing newline), RECORD7 3698 bytes, base + 1 + 3698 = 2375218, matching the post-C1 file's measured length exactly; the second reader's tail slice equalled `\n` + RECORD7 byte for byte, and a one-byte-flipped negative control was correctly rejected — all reproduced independently. G3 THE PLAN HELD BYTE-EXACT: PLAN8 extracted from the committed authored file `cmp`s exit 0 against `.agent/plan.md` (46 lines, under 50; `## Goal`/`## Next Steps` each exactly once), reproduced independently. G4 THE TEN PAIRS HELD: the reviewer independently reconstructed apps/cli/commands/job.py, tests/orchestration/test_long_run_executor.py and tests/orchestration/test_escalation.py by applying all ten pairs in the block's own stated order to pre-C2 scratch copies, and found all three byte-identical to the real committed files — nine pairs correctly classified as rewrites and NEWTESTS correctly classified as an append, all matching constraint 5 exactly. G5 HELD: `python3 -m py_compile` exit 0 on all three files, reproduced; `ruff check` produced the same session-level denial text every prior round has quoted, reproduced verbatim. G6 THE RED-PROOF HELD, REPRODUCED INDEPENDENTLY IN A SEPARATE DISPOSABLE WORKTREE: inverting `if not confirm_cost_preview(` to `if confirm_cost_preview(` produced the identical four failing tests the worker reported (two pre-existing tests whose call sites now rely on the run proceeding, plus both of NEWTESTS' own two new tests), proving the gate is real, load-bearing code; reverted, 76 passed again; worktree removed after. G7 THE SUITES, REPRODUCED INDEPENDENTLY BY THE REVIEWER at this round's own HEAD, all twelve counts identical to the worker's own reading: `test_long_run_executor.py` 76, `test_escalation.py` 68, `test_resume_kill.py`+`test_resume_cli.py` 42, `test_no_interactive_guard.py` 6, `test_command_catalog.py`+`test_command_catalog.py` (cli) 45, `tests/docs/` 295, `test_roadmap_index.py` 30, `tests/ui_server/` 515, `test_test_runner.py` 52, `test_resource_safety.py` 21, `test_integrity_gate.py` 16, `test_golden_path.py` (canary) 42 — nothing moved outside this round's own declared changes. G8 HELD: `git status --porcelain` empty, `git ls-files .remedy-wt` empty, no leftover scratch worktree, all four pre-handback commits' numstat `+`/`-` cells matched the handback's own Commits table cell for cell, reproduced independently. ZERO DEVIATIONS WERE DECLARED by the worker and the reviewer found none either. No finding is registered; nothing is wrong on disk. `job.run` now genuinely confirms before spending, gated on an honest unavailable estimate, with real production callers and real red-proof coverage — this is the first round where confirm_cost_preview() has a live, non-test caller. The reviewer's own pre-authoring investigation (done before round 8 was even drafted) is what surfaced the six test call sites that needed repair, avoiding a red G7 the round would otherwise have produced. Branch `feature/f114-cost-preview-per-command` is pushed and matches `origin` head-for-head; `git status --porcelain` reads empty now.
<<<END RECORD8>>>

<<<BEGIN PLAN9>>>
# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 9 books round 8's PASS verdict (RECORD8) and adds
`tests/cli/test_cost_preview.py` - the feature doc's own suggested
acceptance-test path, still empty until now. Unlike round 8's own gate
tests (which mock `confirm_cost_preview` itself to isolate the wiring),
these five tests exercise the REAL `confirm_cost_preview` end to end
through `job.run`: a non-tty pipe without `--yes` exits with code 2 and
names `job.run` in its hint, `--yes` and `--unattended` both proceed
through the real gate without a tty, and the printed line always carries
its basis label (A9). This closes the "exits-with-hint on a pipe" /
"proceeds audited with --yes" acceptance criteria that round 8's mocked
tests did not reach.

## Next Steps

- T003 continuation: docs for `--yes` and the cost-preview behavior
  (no dedicated CLI reference doc file exists yet for job commands;
  needs its own investigation of docs/ structure rules before writing).
- T003 continuation: consider marking other "rerunning subtrees" /
  "long explanations" commands `is_expensive` - only `job.run` so far.
- Real cost bands for `job.run` still do not exist - a future round
  needs real task-class data to replace the unavailable estimate.
- Acceptance fixtures continue; the integration gate, then the closure
  sequence (PR, Open PR Gate). No PR exists yet.
- Session note: round 9, session 2 - 4 delegated rounds this session
  (6, 7, 8, 9), at the 4-5 default.

## Risks

- No new production code lands this round - test-only, lower risk than
  round 8, by design (round 8 was unusually large for one round).
- Docs remain the one named acceptance item with no owner yet; a future
  round should investigate docs/README.md's structure rules before
  writing anything, per this repo's own docs-ops conventions.
<<<END PLAN9>>>

<<<BEGIN TESTMODULE>>>
"""F114 T003 — acceptance tests for job.run's cost-preview behavior.

Unlike tests/orchestration/test_long_run_executor.py's own gate tests
(which mock confirm_cost_preview itself to isolate the wiring), these
exercise the REAL confirm_cost_preview end to end through job.run, per
docs/roadmap/features/T3_F114.md's acceptance section: a pipe exits with
the --yes hint, --yes proceeds audited, and every printed estimate
carries its basis label.
"""
from __future__ import annotations

import pytest


class TestJobRunCostPreviewAcceptance:
    def test_non_tty_without_yes_exits_with_the_job_run_hint(self, monkeypatch):
        from apps.cli.commands import job as job_cmd

        monkeypatch.setattr("apps.cli.cost_preview_confirm._stdin_is_a_tty", lambda: False)
        ran: list[str] = []
        monkeypatch.setattr(job_cmd, "_cmd_run_next_task_local", ran.append)

        with pytest.raises(SystemExit) as exc:
            job_cmd._cmd_job_run_cycles("abc12345")

        assert exc.value.code == 2
        assert ran == []

    def test_non_tty_without_yes_names_job_run_in_the_hint(self, monkeypatch, capsys):
        from apps.cli.commands import job as job_cmd

        monkeypatch.setattr("apps.cli.cost_preview_confirm._stdin_is_a_tty", lambda: False)
        monkeypatch.setattr(job_cmd, "_cmd_run_next_task_local", lambda _: None)

        with pytest.raises(SystemExit):
            job_cmd._cmd_job_run_cycles("abc12345")

        err = capsys.readouterr().err
        assert "--yes" in err
        assert "job.run" in err

    def test_yes_flag_proceeds_through_the_real_gate_without_a_tty(self, monkeypatch):
        from apps.cli.commands import job as job_cmd

        monkeypatch.setattr("apps.cli.cost_preview_confirm._stdin_is_a_tty", lambda: False)
        ran: list[str] = []
        monkeypatch.setattr(job_cmd, "_cmd_run_next_task_local", ran.append)

        job_cmd._cmd_job_run_cycles("abc12345", yes=True)

        assert ran == ["abc12345"]

    def test_unattended_proceeds_through_the_real_gate_without_a_tty(self, monkeypatch):
        from apps.cli.commands import job as job_cmd

        monkeypatch.setattr("apps.cli.cost_preview_confirm._stdin_is_a_tty", lambda: False)
        ran: list[str] = []
        monkeypatch.setattr(job_cmd, "_cmd_run_next_task_local", ran.append)

        job_cmd._cmd_job_run_cycles("abc12345", unattended=True)

        assert ran == ["abc12345"]

    def test_the_printed_preview_line_carries_its_basis_label(self, monkeypatch, capsys):
        # A9: every shown number carries its basis label - job.run's own
        # printed line is no exception, even in the unavailable case.
        from apps.cli.commands import job as job_cmd

        monkeypatch.setattr(job_cmd, "_cmd_run_next_task_local", lambda _: None)

        job_cmd._cmd_job_run_cycles("abc12345", yes=True)

        out = capsys.readouterr().out
        assert "basis:" in out
        assert "estimate_unavailable" in out
<<<END TESTMODULE>>>
