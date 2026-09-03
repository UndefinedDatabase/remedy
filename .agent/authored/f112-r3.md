STEP T001 PART 2 (REPAIR + TESTS) / ROUND 3 - F112 Prompt budget per task class
FEATURE F112 - Prompt budget per task class (Tier 3) - SESSION 1, ROUND 3

Goal
  Fix R-0791 (two ruff-confirmed defects the round 2 block's own MODULE
  slice shipped into packages/orchestration/prompt_budget.py), book round
  2's verdict, and land T001's test file, completing T001. Still no
  compiler wiring - that is T002.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f112-r3.md
  C0b mirror it to .agent/last_block.md
  C1  apply PLAN3 to .agent/plan.md (whole-file replacement, FIRST
      substantive commit per section 3 item 23, since this round
      registers/resolves a finding)
  C2  THE FIX: apply QUOTE PAIR to
      packages/orchestration/prompt_budget.py, then append exactly one
      newline byte (0x0a) at the very end of that same file
  C3  apply RECORD2 to .agent/live_review.md (append) and SLIP1 to
      .agent/prose_slips.md (append) - AFTER the fix, so the resolution
      claim is true when written
  C4  write tests/orchestration/test_class_prompt_budget.py per TEST_FILE
      (new file)
  C5  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f112-r3.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/plan.md (C1) - packages/orchestration/prompt_budget.py (C2) -
  .agent/live_review.md (C3) - .agent/prose_slips.md (C3) -
  tests/orchestration/test_class_prompt_budget.py (new, C4) -
  .agent/handoff.md (C5)

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by
     delimiter index from the COMMITTED .agent/authored/f112-r3.md -
     marker lines EXCLUDED - and write it with a script, never by
     retyping. If a slice looks wrong, apply it as written and DECLARE it
     in the handback.
  2. TRAILING NEWLINE HANDLING, STATED EXPLICITLY BECAUSE ROUND 2 GOT
     THIS WRONG (declared there as a prose slip, not repeated here): each
     slice's content INCLUDES the newline byte that terminates its OWN
     final content line - i.e. everything from immediately after the
     BEGIN marker's own line-ending up to and INCLUDING the newline
     immediately before the END marker line, but EXCLUDING the marker
     lines themselves. Verify this per slice with a byte length check
     against what this block states below, not by eye.
  3. THE FIX (C2) is TWO separate byte-level edits to the SAME file, in
     this order: (a) str.replace(FROM, TO, 1) using QUOTE PAIR FROM/TO -
     verify FROM occurs exactly once before, TO does not contain FROM
     (a genuine rewrite); (b) the file must NOT end with a newline before
     this edit (verify) and MUST end with exactly one newline byte after
     - append it, do not rewrite the whole file.
  4. RECORD2 appends to .agent/live_review.md as two newline bytes then
     the slice, per the file's existing convention. SLIP1 appends to
     .agent/prose_slips.md the same way. Both slices, as given below,
     already include their own trailing content correctly per
     constraint 2 - do not add or drop bytes at either boundary.
  5. TEST_FILE is a WHOLE NEW FILE: write its exact bytes with the Write
     tool (a "copyfile", never a text-extraction-and-reflow), ending with
     exactly one trailing newline per constraint 2.
  6. ruff availability is UNRELIABLE this session (round 2 found
     `python3 -m ruff` resolves even though the bare `ruff` binary does
     not) - use the MODULE form, and re-measure rather than assuming
     either way.
  7. Do NOT wire prompt_budget into context_compiler.py, role_config.py,
     or any call site - that is T002.
  8. A sentence OUTSIDE the change set that this round makes stale is
     DECLARED in the handback and NOT repaired.
  9. Read .agent/STOP from disk before the first commit and again before
     C5. If it exists, finish the commit in hand, write the handback, and
     stop.
  10. Self-review loop before every commit (git diff --stat, git diff).
      Push after C5. No pull request, no merge.
  11. THE MUTATION RED-PROOF (G6) RUNS ONLY INSIDE A DISPOSABLE git
      worktree created under .remedy-wt/, NEVER in the primary checkout,
      and the primary checkout's git status --porcelain must read EMPTY
      immediately after the mutation step, proving nothing leaked. Do not
      `cd` into the worktree for the pytest run - use an absolute path or
      `subprocess.run(cwd=...)`; verify which checkout you touched by
      printing the imported module's `__file__` before trusting a
      red/green reading.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f112-r3.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE PLAN. Extract PLAN3 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md            -> exit 0
       wc -l .agent/plan.md                      -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G3 THE FIX. Before C2: count of QUOTE PAIR FROM in
     packages/orchestration/prompt_budget.py -> must be 1; file's last
     byte -> report it, must NOT be a newline. After C2: FROM count (0),
     TO count (1), "TO contains FROM: false"; file's last byte -> must be
     a newline; byte length before/after the append differs by exactly 1.
     Then `python3 -m ruff check packages/orchestration/prompt_budget.py`
     -> report the real result; it must read "All checks passed!".
  G4 THE LEDGER AND SLIP APPENDS.
     (a) .agent/live_review.md gets the FULL arithmetic amend0827 rule 5
         reserves for the record: base size immediately BEFORE C3
         (measure it, do not trust a stated number) + 2 + RECORD2's own
         byte length (report it; RECORD2 has ZERO internal newlines) =
         the post-C3 size. Then the second, independent reader: split the
         WHOLE post-C3 file on blank-line boundaries and report whether
         the LAST unit equals RECORD2 exactly. Then a NEGATIVE CONTROL in
         a scratch copy ONLY: flip one byte inside RECORD2's text and
         report that the second reader REJECTS it.
     (b) .agent/prose_slips.md gets a BYTE-EQUALITY CHECK ONLY (amend0827
         rule 5's ceiling for a .agent/ prose file): report whether the
         file's final bytes equal the extracted SLIP1 slice exactly.
  G5 THE TEST FILE. Extract TEST_FILE from the COMMITTED authored file
     and cmp against tests/orchestration/test_class_prompt_budget.py ->
     exit 0. Then:
       python3 -m pytest tests/orchestration/test_class_prompt_budget.py -q
     Report the pass count; expect 24 passed.
  G6 THE MUTATION RED-PROOF, INSIDE A DISPOSABLE WORKTREE ONLY (see
     constraint 11). In the worktree copy of
     packages/orchestration/prompt_budget.py, swap the ORDER of the two
     `if` blocks inside resolve_task_class_cap so the DEFAULT_CAP_CONFIG_KEY
     check runs BEFORE the TASK_CLASS_CAPS_CONFIG_KEY check (i.e. a
     configured global default would now win over a configured per-class
     cap). Run
       python3 -m pytest <worktree>/tests/orchestration/test_class_prompt_budget.py -q
     via an absolute path (no cd) and report: it must show exactly 1
     failed, naming
     TestResolutionPrecedence::test_a_configured_class_cap_wins_over_the_global_default,
     with every other test still passing. Then confirm the UNMUTATED
     control in the SAME worktree (revert the swap) returns to 24 passed.
     Report `git status --porcelain` on the PRIMARY checkout immediately
     after the mutation step and again after cleanup - both must read
     EMPTY. Remove the worktree before C5.
  G7 THE STATE READERS AND THE CANARY, EACH AS ITS OWN INVOCATION:
       python3 -m pytest tests/ui_server/ -q
       python3 -m pytest tests/orchestration/test_test_runner.py -q
       python3 -m pytest tests/regression/test_resource_safety.py -q
       python3 -m pytest tests/orchestration/test_integrity_gate.py -q
       python3 -m pytest tests/cli/test_golden_path.py -q
     Report each pass count. THE FOUR STATE READERS ARE RUN AS FOUR, NOT
     AS THREE. The last is the canary.
  G8 THE TREE, THE COMMITS AND THE SWEEP. Read git status --porcelain
     immediately before C5 is staged, and git ls-files .remedy-wt (no
     output). Then, for C0a through C4 - the commits BEFORE the handback
     commit - report each one's insertion count from git show --numstat,
     the '+' column ONLY, and compare it CELL BY CELL against the
     Commits table of the handback you are writing. C5's own numbers go
     to NEITHER a round report NOR this file. Then THE STALENESS SWEEP
     over every file this round touched, one entry per file, stale or
     NOT stale, why.

Handback
  Rewrite .agent/handoff.md per docs/agents/handback_template.md. It
  carries the SESSION NUMBER of the running feature - this is SESSION 1
  of F112 - the state block, the item-status table with every ordered
  item appearing exactly once, the Commits table, one line per gate
  followed by the transcripts, the deviations, and the next steps. It has
  no length cap.

SLICES. Each slice lies between its own one-line BEGIN and END marker.
The marker lines are NEVER part of the slice. The slices carried here are
PLAN3, QUOTE PAIR FROM, QUOTE PAIR TO, RECORD2, SLIP1 and TEST_FILE.

<<<BEGIN PLAN3>>>
# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001 part 1 landed round 2.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 3, session 1 — fix `R-0791` (two ruff-confirmed defects in
`packages/orchestration/prompt_budget.py`: a redundant-quotes type hint
and a missing trailing newline), then ship
`tests/orchestration/test_class_prompt_budget.py`, completing T001. Still
no compiler wiring — T002.

## Next Steps

- T002: compiler cap enforcement in `context_compiler.py` — `fit(context,
  cap)` over the existing demotion order, the `cannot_fit` outcome with
  tier-1/cap/class arithmetic, and oversized/unfittable fixtures.
- T003: decision wiring (`escalation.enqueue_task_decision`, type
  `task_decision`), unattended default split, granularity-machinery seam.
- Acceptance fixtures, the integration gate, then the closure sequence.

## Risks

- `task_granularity.py`'s split helpers are module-private and built for
  plan-time normalization, not a live dispatched task; T003 may need a
  small public seam addition, never a fork of the heuristics themselves
  (feature file "Do not touch").
- `R-0767` stays OPEN on the model-routing seam this feature's config
  registration pattern borrows from; unrelated to F112, not absorbed.
- ruff availability is INCONSISTENT within this session: the bare `ruff`
  binary is denied but `python3 -m ruff` resolves (measured R2); use the
  module form and re-measure each round rather than trusting a prior
  round's claim.
<<<END PLAN3>>>

<<<BEGIN QUOTE PAIR FROM>>>
def validate_prompt_budget_config(config: "RemedyConfig") -> list[str]:
<<<END QUOTE PAIR FROM>>>

<<<BEGIN QUOTE PAIR TO>>>
def validate_prompt_budget_config(config: RemedyConfig) -> list[str]:
<<<END QUOTE PAIR TO>>>

<<<BEGIN RECORD2>>>
Gate: F112 R2 — the round 2 entry. VERDICT PASS, over the range `0092939e..e33a6161`. THE ROUND BOOKED ROUND 1'S VERDICT AND LANDED T001 PART 1: the config schema (`prompt_budget.task_class_caps`, `prompt_budget.default_cap`) and the new module `packages/orchestration/prompt_budget.py`. TRANSPORT: the reviewer's own scratchpad original at `.remedy-wt/f112_r2_block.md` matches the committed `.agent/authored/f112-r2.md` for the ENTIRE slice content of every marked region; the two files differ by exactly one byte, a trailing newline AFTER the final `<<<END MODULE>>>` marker line, outside every slice boundary and therefore of no product effect — recorded in `.agent/prose_slips.md` this round, not as a finding. THE LEDGER ARITHMETIC HELD: base 2246582 bytes plus 2 plus RECORD1's 1663 bytes equals 2248247, reproduced directly against the file on disk, tail matching RECORD1 verbatim. THE CONFIG PAIR WAS A GENUINE REWRITE: FROM occurred once before, zero after; the new keys resolve via `get_key_spec`. THE SUITES HELD: `tests/orchestration/test_config.py` unchanged at 81 passed, the canary and the four state readers all green, reproduced by the reviewer directly for `test_config.py`, the canary and `test_integrity_gate.py`. FINDING R-0791 (Low, packages/, REGISTERED AND RESOLVED IN THIS ROUND): the open set was searched first per §3 item 30 and held no existing entry for this defect class. `python3 -m ruff check packages/orchestration/prompt_budget.py`, run independently by the reviewer at `e33a6161` (contrary to the F112 R1 context claim that ruff was denied this session — `python3 -m ruff` resolves even though the bare `ruff` binary does not, and the R1 claim is corrected here rather than silently), found two real defects the round's own MODULE slice shipped: `UP037` (redundant quotes on the `TYPE_CHECKING`-guarded `"RemedyConfig"` annotation, which `from __future__ import annotations` already stringifies) and `W292` (the file has no trailing newline, because the reviewer's own MODULE slice omitted one before its END marker). Root cause is the reviewing session's authored slice, not the worker's application of it — the worker correctly declared both rather than silently repairing a slice it was ordered to apply byte for byte, which would have broken the round's own `cmp` gate. Done: R-0791 — fixed in this round's own C2, before this entry was written, `python3 -m ruff check packages/orchestration/prompt_budget.py` reproduced by the reviewer as `All checks passed!` at the post-fix commit. NO OTHER FINDING IS OWED BY THIS ROUND.
<<<END RECORD2>>>

<<<BEGIN SLIP1>>>
2026-09-03 · F112 R2 · The reviewer's own PLAN2 slice left its END marker boundary ambiguous, and the worker's marker-delimited extraction dropped `.agent/plan.md`'s final trailing newline as a result (45 lines, content otherwise byte-identical to the reviewer's scratch copy); the same ambiguity dropped the trailing newline of the whole committed `.agent/authored/f112-r2.md` file after its last marker line, with zero effect on any slice's content. Neither is wrong on disk under `packages/`, `apps/`, `tests/` or `docs/`; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIP1>>>

<<<BEGIN TEST_FILE>>>
"""Tests for packages.orchestration.prompt_budget (F112 T001).

Config-backed tests use the REAL ``load_config`` against a pytest
``tmp_path`` TOML file, patched at
``packages.orchestration.config.get_config`` — the idiom
``tests/orchestration/test_role_config.py`` established for
``resolve_effective_task_class_tiers``, which ``resolve_task_class_cap``
mirrors.
"""

from __future__ import annotations

import pathlib

import pytest

from packages.orchestration.config import get_key_spec, load_config
from packages.orchestration.model_routing import TASK_CLASS_TIERS
from packages.orchestration.prompt_budget import (
    DEFAULT_CAP_CONFIG_KEY,
    DEFAULT_FALLBACK_CAP_TOKENS,
    MIN_TASK_CLASS_CAP_TOKENS,
    PROMPT_BUDGET_ESTIMATE_BASIS_CLASS_DEFAULT,
    TASK_CLASS_CAPS_CONFIG_KEY,
    resolve_task_class_cap,
    validate_prompt_budget_config,
)


def _configure_prompt_budget(
    monkeypatch, tmp_path, *, task_class_caps=None, default_cap=None
):
    """Make prompt_budget's config keys answer given values via REAL TOML.

    Nothing is written to the repository root: a ``remedy.toml`` there
    would change how every test in the suite resolves configuration.
    """
    lines: list[str] = []
    if default_cap is not None:
        lines.append("[remedy.prompt_budget]")
        lines.append(f"default_cap = {default_cap}")
    if task_class_caps:
        lines.append(f"[remedy.{TASK_CLASS_CAPS_CONFIG_KEY}]")
        lines += [f"{task_class} = {cap}" for task_class, cap in task_class_caps.items()]
    toml_file = tmp_path / "remedy.toml"
    toml_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    loaded = load_config(
        project_path=toml_file, user_path=pathlib.Path("/nonexistent/user.toml")
    )
    monkeypatch.setattr("packages.orchestration.config.get_config", lambda: loaded)
    return loaded


class TestSharedVocabulary:
    def test_every_task_class_tiers_member_resolves_a_cap(self, monkeypatch, tmp_path):
        _configure_prompt_budget(monkeypatch, tmp_path)
        for task_class in TASK_CLASS_TIERS:
            resolution = resolve_task_class_cap(task_class)
            assert resolution.task_class == task_class

    def test_a_class_outside_task_class_tiers_is_refused(self, monkeypatch, tmp_path):
        _configure_prompt_budget(monkeypatch, tmp_path)
        with pytest.raises(ValueError, match="shared vocabulary"):
            resolve_task_class_cap("not_a_real_class")


class TestResolutionPrecedence:
    def test_no_config_falls_back_to_the_shipped_default(self, monkeypatch, tmp_path):
        _configure_prompt_budget(monkeypatch, tmp_path)
        resolution = resolve_task_class_cap("format")
        assert resolution.cap_tokens == DEFAULT_FALLBACK_CAP_TOKENS
        assert resolution.source == "shipped_default"

    def test_a_configured_global_default_overrides_the_shipped_one(
        self, monkeypatch, tmp_path
    ):
        _configure_prompt_budget(monkeypatch, tmp_path, default_cap=9000)
        resolution = resolve_task_class_cap("format")
        assert resolution.cap_tokens == 9000
        assert resolution.source == "configured_default"

    def test_a_configured_class_cap_wins_over_the_global_default(
        self, monkeypatch, tmp_path
    ):
        _configure_prompt_budget(
            monkeypatch, tmp_path, default_cap=9000, task_class_caps={"format": 5000}
        )
        resolution = resolve_task_class_cap("format")
        assert resolution.cap_tokens == 5000
        assert resolution.source == "configured_class"

    def test_a_class_cap_for_a_different_class_does_not_leak(self, monkeypatch, tmp_path):
        _configure_prompt_budget(
            monkeypatch, tmp_path, task_class_caps={"architecture": 40000}
        )
        resolution = resolve_task_class_cap("format")
        assert resolution.source == "shipped_default"

    @pytest.mark.parametrize("task_class", sorted(TASK_CLASS_TIERS))
    def test_every_resolution_carries_the_class_default_basis(
        self, monkeypatch, tmp_path, task_class
    ):
        _configure_prompt_budget(monkeypatch, tmp_path)
        resolution = resolve_task_class_cap(task_class)
        assert resolution.estimate_basis == PROMPT_BUDGET_ESTIMATE_BASIS_CLASS_DEFAULT


class TestFloorValidation:
    def test_a_clean_config_has_no_errors(self, monkeypatch, tmp_path):
        loaded = _configure_prompt_budget(
            monkeypatch, tmp_path, default_cap=24000, task_class_caps={"format": 4000}
        )
        assert validate_prompt_budget_config(loaded) == []

    def test_no_prompt_budget_table_at_all_has_no_errors(self, monkeypatch, tmp_path):
        loaded = _configure_prompt_budget(monkeypatch, tmp_path)
        assert validate_prompt_budget_config(loaded) == []

    def test_a_class_cap_below_the_floor_is_an_error(self, monkeypatch, tmp_path):
        loaded = _configure_prompt_budget(
            monkeypatch, tmp_path, task_class_caps={"format": 100}
        )
        errors = validate_prompt_budget_config(loaded)
        assert len(errors) == 1
        assert "format" in errors[0]
        assert str(MIN_TASK_CLASS_CAP_TOKENS) in errors[0]

    def test_a_default_cap_below_the_floor_is_an_error(self, monkeypatch, tmp_path):
        loaded = _configure_prompt_budget(monkeypatch, tmp_path, default_cap=1)
        errors = validate_prompt_budget_config(loaded)
        assert len(errors) == 1
        assert DEFAULT_CAP_CONFIG_KEY in errors[0]

    def test_an_unknown_task_class_is_an_error(self, monkeypatch, tmp_path):
        loaded = _configure_prompt_budget(
            monkeypatch, tmp_path, task_class_caps={"not_a_real_class": 5000}
        )
        errors = validate_prompt_budget_config(loaded)
        assert len(errors) == 1
        assert "not_a_real_class" in errors[0]

    def test_both_kinds_of_violation_are_both_reported(self, monkeypatch, tmp_path):
        loaded = _configure_prompt_budget(
            monkeypatch,
            tmp_path,
            default_cap=1,
            task_class_caps={"not_a_real_class": 5000, "format": 100},
        )
        errors = validate_prompt_budget_config(loaded)
        assert len(errors) == 3


class TestConfigRegistration:
    def test_task_class_caps_key_is_a_table_of_ints(self):
        spec = get_key_spec(TASK_CLASS_CAPS_CONFIG_KEY)
        assert spec is not None
        assert spec.value_type is dict
        assert spec.entry_type is int
        assert spec.default is None

    def test_default_cap_key_is_a_scalar_int(self):
        spec = get_key_spec(DEFAULT_CAP_CONFIG_KEY)
        assert spec is not None
        assert spec.value_type is int
        assert spec.default is None
<<<END TEST_FILE>>>
