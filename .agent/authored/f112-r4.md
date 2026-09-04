── STEP T002/3 — F112 ────────────────────────────────────────
Goal: Wire T001's per-class cap resolver onto the context compiler's
existing demotion cascade (T002), with the two required fixtures
(oversized→demoted-and-fits, unfittable→cannot_fit-with-arithmetic),
and book round 3's already-independently-reviewed PASS verdict into
the ledger in this round's first substantive commit (amend0827 rule 1
— a verdict never buys a round of its own).

Bundle:
1. Book RECORD3 (round 3's verdict) into `.agent/live_review.md`.
2. Add `ClassBudgetFit` + `fit_task_context_to_class_cap` to
   `packages/orchestration/context_compiler.py`.
3. Add 4 tests to `tests/orchestration/test_context_compiler.py`
   covering: fits-under-cap-with-demotion, cannot_fit-arithmetic,
   vocabulary refusal, and real-config wiring (no mock of the
   resolver in the last two).

Change: exactly the 6 files named in the Commits section below.
Nothing else.

Constraints:
- Do NOT touch the demotion cascade itself, calibration (F074), or
  granularity heuristics — docs/roadmap/features/T3_F112.md
  "Do not touch". `fit_task_context_to_class_cap` calls
  `compile_task_context` unchanged; it adds no selection logic.
- Every pair below is APPEND-shaped: apply as
  `content = content.replace(FROM, TO, 1)` — FROM occurs exactly
  once in the current file (verified below at BASE_SHA), TO
  contains FROM as a literal prefix, and the file text after FROM's
  original span is untouched by construction.
- `packages/orchestration/prompt_budget.py` is NOT touched this
  round — only imported from.
- ruff availability is inconsistent this session: try the bare
  `ruff` binary first, fall back to `python3 -m ruff check <path>`
  if denied; report which one worked.
- RECORD3 is ONE line (no internal newlines) ending in exactly one
  trailing newline, matching every existing `Gate:` entry's shape in
  `.agent/live_review.md` — do not reflow it.
- `.agent/plan.md` stays under 50 lines (AGENTS.md).

Done when: every gate in "Gates" below is run for real and its exact
output recorded in the handback; all 6 commits land in the stated
order; tree is clean; branch is pushed.

Handback: completion report + rewrite `.agent/handoff.md` per
AGENTS.md's `### handoff.md` section and
docs/agents/handback_template.md.
──────────────────────────────────────────────────────────────

<<<BEGIN PLAN4 (whole-file replacement of .agent/plan.md)>>>
# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001 complete as of round 3.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 4, session 2 — T002: `ClassBudgetFit` + `fit_task_context_to_class_cap`
in `packages/orchestration/context_compiler.py`, wiring T001's
`resolve_task_class_cap` onto the existing `compile_task_context` demotion
cascade with no change to that cascade itself. Two fixtures: an oversized
context demoted under its cap (`fits=True`), and an unfittable one
reporting `cannot_fit` arithmetic (`fits=False`, `tier1_tokens` carried).

## Next Steps

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
  binary is denied but `python3 -m ruff` resolves (measured every round so
  far); use the module form and re-measure rather than trusting a prior
  round's claim.
<<<END PLAN4>>>

<<<BEGIN RECORD3 (append to .agent/live_review.md)>>>
Gate: F112 R3 — the round 3 entry. VERDICT PASS, over the range `e33a6161..72779afb` plus the handback commit `3eae460d`, independently re-verified by the reviewer at the start of round 4 rather than at round 3's own end (session 1 closed before the review step ran; session 2 opened by re-reading this same range from disk, per docs/agents/self_drive_protocol.md Phase 0 and Phase 1 rule 4). THE FIX HELD: `python3 -m ruff check packages/orchestration/prompt_budget.py` reproduced by the reviewer as `All checks passed!`, and the file's last byte reads a newline (`od -c` tail), closing R-0791's two defects (UP037 redundant quotes, W292 missing trailing newline) that RECORD2 already registered and resolved. THE TEST FILE HELD: `python3 -m pytest tests/orchestration/test_class_prompt_budget.py -q` reproduced by the reviewer at 24 passed. THE LEDGER APPEND HELD: this file's own tail, read directly off disk immediately before this entry was appended, ends at byte offset 2250826 exactly as round 3's own handback stated, and the R-0791 text RECORD2 carries is internally consistent with the independently reproduced ruff reading. THE PROSE SLIP HELD: `.agent/prose_slips.md` measured at 66618 bytes, matching the handback's own arithmetic exactly. THE CANARY HELD: `pytest tests/cli/test_golden_path.py -q` reproduced by the reviewer at 42 passed. T001 (config schema, module, resolver, floor and vocabulary validation, 24 tests with a real mutation red-proof run in round 3's own disposable worktree) IS COMPLETE. NO FINDING IS OWED BY THIS BOOKING: it is a record of round 3's already-true verdict, carried forward into round 4's first substantive commit per amend0827-process-diet rule 1 rather than spending a round of its own.
<<<END RECORD3>>>

<<<BEGIN CC_IMPORT_FROM>>>
from packages.orchestration.prompt_segments import (
<<<END CC_IMPORT_FROM>>>

<<<BEGIN CC_IMPORT_TO>>>
from packages.orchestration.prompt_budget import resolve_task_class_cap
from packages.orchestration.prompt_segments import (
<<<END CC_IMPORT_TO>>>

<<<BEGIN CC_MODULE_FROM>>>
        over_budget=total_tokens > token_budget,
        line_cap=line_cap,
    )


<<<END CC_MODULE_FROM>>>

<<<BEGIN CC_MODULE_TO>>>
        over_budget=total_tokens > token_budget,
        line_cap=line_cap,
    )


@dataclass(frozen=True)
class ClassBudgetFit:
    """Whether ``task_class``'s compiled context fits its resolved cap (F112 T002).

    ``fits`` is False exactly for the ``cannot_fit`` outcome
    (docs/roadmap/features/T3_F112.md Design): tier-1 content alone still
    exceeds ``cap_tokens`` after the existing demotion cascade has demoted or
    dropped every tier-2 and tier-3 candidate, which is also why
    ``tier1_tokens`` equals ``compiled.estimated_tokens`` in that case.
    """

    compiled: CompiledContext
    task_class: str
    cap_tokens: int
    cap_source: str
    fits: bool
    tier1_tokens: int


def fit_task_context_to_class_cap(
    root: Path,
    fenced_paths: Iterable[str],
    repo_paths: Iterable[str],
    task_class: str,
    *,
    inline_cap_bytes: int = DEFAULT_INLINE_SIZE_CAP_BYTES,
    line_cap: int = DEFAULT_SIGNATURE_LINE_CAP,
) -> ClassBudgetFit:
    """Compile ``task_class``'s context under its resolved per-class cap.

    Resolves the cap via
    :func:`packages.orchestration.prompt_budget.resolve_task_class_cap`
    (F112 T001), then runs ``compile_task_context`` unchanged at that
    budget — no new selection or demotion logic, only the class-specific
    number the existing cascade enforces
    (docs/roadmap/features/T3_F112.md Design). ``fits`` is False exactly
    when tier-1 content alone still exceeds the cap after every tier-2 and
    tier-3 candidate has been demoted or dropped, carrying the arithmetic
    (``tier1_tokens``, ``cap_tokens``, ``task_class``) the ``cannot_fit``
    task-split decision needs (T003).
    """
    resolution = resolve_task_class_cap(task_class)
    compiled = compile_task_context(
        root,
        fenced_paths,
        repo_paths,
        token_budget=resolution.cap_tokens,
        inline_cap_bytes=inline_cap_bytes,
        line_cap=line_cap,
    )
    tier1_tokens = sum(
        selected.estimated_tokens
        for selected in compiled.included
        if selected.tier == TIER_FENCED
    )
    return ClassBudgetFit(
        compiled=compiled,
        task_class=task_class,
        cap_tokens=resolution.cap_tokens,
        cap_source=resolution.source,
        fits=not compiled.over_budget,
        tier1_tokens=tier1_tokens,
    )


<<<END CC_MODULE_TO>>>

<<<BEGIN TEST_P1_FROM>>>
    OMITTED_CONTEXT_FILENAME,
<<<END TEST_P1_FROM>>>

<<<BEGIN TEST_P1_TO>>>
    OMITTED_CONTEXT_FILENAME,
    ClassBudgetFit,
<<<END TEST_P1_TO>>>

<<<BEGIN TEST_P2_FROM>>>
    extract_file_signatures,
<<<END TEST_P2_FROM>>>

<<<BEGIN TEST_P2_TO>>>
    extract_file_signatures,
    fit_task_context_to_class_cap,
<<<END TEST_P2_TO>>>

<<<BEGIN TEST_P3_FROM>>>
from packages.orchestration.context_compiler import (
<<<END TEST_P3_FROM>>>

<<<BEGIN TEST_P3_TO>>>
from packages.orchestration.config import load_config
from packages.orchestration.context_compiler import (
<<<END TEST_P3_TO>>>

<<<BEGIN TEST_P4_FROM>>>
from packages.orchestration.prompt_segments import (
<<<END TEST_P4_FROM>>>

<<<BEGIN TEST_P4_TO>>>
from packages.orchestration.prompt_budget import TaskClassCapResolution
from packages.orchestration.prompt_segments import (
<<<END TEST_P4_TO>>>

<<<BEGIN TEST_P5_FROM>>>
    assert _tiering(compiled) == (("app.py", 1, "full"),)
    assert compiled.budget_tokens == 1
    assert compiled.over_budget is True


<<<END TEST_P5_FROM>>>

<<<BEGIN TEST_P5_TO>>>
    assert _tiering(compiled) == (("app.py", 1, "full"),)
    assert compiled.budget_tokens == 1
    assert compiled.over_budget is True


def test_an_oversized_context_fits_under_its_class_cap_with_the_demotion_recorded(
    monkeypatch, tmp_path: Path
) -> None:
    """The cap comes from the resolver (T001); everything past that is the
    existing compiler unchanged — a cap one token under the unconstrained
    total still forces the same tier-2 demotion phase A already proves, and
    ``fits`` reports the result as fitting."""
    _selector_tree(tmp_path)
    unconstrained = compile_task_context(tmp_path, ["app.py"], _SELECTOR_REPO_PATHS)
    cap = unconstrained.estimated_tokens - 1
    monkeypatch.setattr(
        "packages.orchestration.context_compiler.resolve_task_class_cap",
        lambda task_class: TaskClassCapResolution(
            task_class=task_class,
            cap_tokens=cap,
            source="configured_class",
            estimate_basis="class_default",
        ),
    )

    result = fit_task_context_to_class_cap(
        tmp_path, ["app.py"], _SELECTOR_REPO_PATHS, "format"
    )

    assert result.fits is True
    assert result.cap_tokens == cap
    assert result.cap_source == "configured_class"
    assert result.tier1_tokens == _full_tokens(tmp_path, "app.py")
    assert (
        OmissionRecord("lib_big.py", 2, "budget", "signatures")
        in result.compiled.omissions
    )


def test_an_unfittable_context_reports_cannot_fit_with_the_tier1_arithmetic(
    monkeypatch, tmp_path: Path
) -> None:
    """Tier 1 alone still exceeds a cap of 1: ``fits`` is False and
    ``tier1_tokens`` carries the exact arithmetic a task-split decision
    needs (T003), equal to the compiled context's own total in this case."""
    _selector_tree(tmp_path)
    monkeypatch.setattr(
        "packages.orchestration.context_compiler.resolve_task_class_cap",
        lambda task_class: TaskClassCapResolution(
            task_class=task_class,
            cap_tokens=1,
            source="configured_class",
            estimate_basis="class_default",
        ),
    )

    result = fit_task_context_to_class_cap(
        tmp_path, ["app.py"], _SELECTOR_REPO_PATHS, "format"
    )

    assert result.fits is False
    assert result.cap_tokens == 1
    assert result.tier1_tokens == _full_tokens(tmp_path, "app.py")
    assert result.tier1_tokens == result.compiled.estimated_tokens
    assert result.compiled.over_budget is True


def test_a_class_outside_the_shared_vocabulary_is_refused(tmp_path: Path) -> None:
    """No mock here: the real resolver's vocabulary check (T001) refuses the
    class before any file under root is even read."""
    _selector_tree(tmp_path)

    with pytest.raises(ValueError, match="shared vocabulary"):
        fit_task_context_to_class_cap(
            tmp_path, ["app.py"], _SELECTOR_REPO_PATHS, "not_a_real_class"
        )


def test_the_cap_comes_from_the_real_resolver_when_config_sets_one(
    monkeypatch, tmp_path: Path
) -> None:
    """No mock of resolve_task_class_cap here either: a real config
    default_cap reaches the compiler exactly the way T001 designed it to."""
    _selector_tree(tmp_path)
    default_cap = _full_tokens(tmp_path, "app.py")
    config_dir = tmp_path / "_config"
    config_dir.mkdir()
    toml_file = config_dir / "remedy.toml"
    toml_file.write_text(
        f"[remedy.prompt_budget]\ndefault_cap = {default_cap}\n", encoding="utf-8"
    )
    loaded = load_config(
        project_path=toml_file, user_path=Path("/nonexistent/user.toml")
    )
    monkeypatch.setattr("packages.orchestration.config.get_config", lambda: loaded)

    result = fit_task_context_to_class_cap(
        tmp_path, ["app.py"], _SELECTOR_REPO_PATHS, "format"
    )

    assert result.cap_tokens == default_cap
    assert result.cap_source == "configured_default"
    assert result.fits is True


<<<END TEST_P5_TO>>>

Gates (run every one for real, record exact output; at most 8, this
round uses all 8):

G1 TRANSPORT: `cmp .agent/authored/f112-r4.md .agent/last_block.md` → exit 0.

G2 PLAN: extract PLAN4 from the committed `.agent/authored/f112-r4.md`
(between its markers, programmatically, never retyped) to a scratch file
under `.remedy-wt/`, then `cmp` it against `.agent/plan.md` → exit 0.
`wc -l .agent/plan.md` → must be < 50. `grep -c '^## Goal' .agent/plan.md`
→ 1. `grep -c '^## Next Steps' .agent/plan.md` → 1.

G3 LEDGER: measure `.agent/live_review.md` size in bytes IMMEDIATELY
BEFORE the append commit (must read 2250826 — if it does not, STOP and
report the discrepancy rather than proceeding). Extract RECORD3 from the
committed authored file programmatically; compute its own byte length
(must be 1739, zero internal newlines, last byte a newline). Append it as
`content_bytes + b"\n\n" + RECORD3_bytes` (two newline bytes plus the
slice, matching round 3's own convention) and write back. Confirm
post-size == 2250826 + 2 + 1739 == 2252567 exactly. Second reader: split
the whole post-append file on `\n\n` boundaries and confirm the last unit
equals RECORD3 exactly. Negative control (in-memory only, never written):
flip one byte inside RECORD3's own text and confirm the second reader then
rejects it.

G4 PRODUCTION CODE: `git show 3eae460d55a68f292c7a04e76011639b748033ca:packages/orchestration/context_compiler.py`
into scratch, apply CC_IMPORT_FROM→CC_IMPORT_TO then CC_MODULE_FROM→CC_MODULE_TO
via `content.replace(FROM, TO, 1)` in that order, `cmp` the result against
the committed `packages/orchestration/context_compiler.py` → exit 0. Then
`ruff check packages/orchestration/context_compiler.py` (or
`python3 -m ruff check` if the bare binary is denied) → must read clean.

G5 TEST FILE: same reconstruction technique as G4 — base blob of
`tests/orchestration/test_context_compiler.py` at the same SHA, apply
TEST_P1 through TEST_P5 in that exact order via `content.replace(FROM, TO, 1)`,
`cmp` against the committed file → exit 0. Then
`python3 -m pytest tests/orchestration/test_context_compiler.py -q` → every
test passes (report the exact count), and confirm by name that all 4 new
tests ran and passed.

G6 MUTATION RED-PROOF (disposable git worktree only, never the primary
checkout — print the worktree's own `__file__` path before trusting any
reading): inside the worktree, change
`if selected.tier == TIER_FENCED` to `if selected.tier != TIER_FENCED`
in `fit_task_context_to_class_cap`'s `tier1_tokens` computation (the only
occurrence of that exact line inside that function — confirm count is 1
in that function's body before editing). Run
`python3 -m pytest <worktree>/tests/orchestration/test_context_compiler.py -q`
and confirm the two tests
`test_an_oversized_context_fits_under_its_class_cap_with_the_demotion_recorded`
and `test_an_unfittable_context_reports_cannot_fit_with_the_tier1_arithmetic`
are named among the failures (both assert `tier1_tokens` against
`_full_tokens`, which the mutation makes wrong). Revert the mutation in the
worktree, `cmp` the reverted file against the primary checkout's copy to
confirm exact match, re-run and confirm full green again. Remove the
worktree. `git status --porcelain` on the PRIMARY checkout must read empty
immediately after the mutation step and again after cleanup.

G7 STATE READERS AND CANARY (five separate invocations, run as five, not
three): `python3 -m pytest tests/ui_server/ -q`,
`python3 -m pytest tests/orchestration/test_test_runner.py -q`,
`python3 -m pytest tests/regression/test_resource_safety.py -q`,
`python3 -m pytest tests/orchestration/test_integrity_gate.py -q`,
`python3 -m pytest tests/cli/test_golden_path.py -q` (canary). Report each
pass count.

G8 TREE, COMMITS, SWEEP: `git status --porcelain` empty immediately before
the handback commit is staged. `git ls-files .remedy-wt` empty. Per-commit
`git show --numstat` `+` column for every commit before the handback,
cross-checked cell-by-cell against the Commits table in your own handback.
One staleness-sweep line per file this round touched, in the handback.

Commits, in this exact order:
- C0a: save the block verbatim to `.agent/authored/f112-r4.md`.
- C0b: mirror to `.agent/last_block.md`.
- C1: apply PLAN4 to `.agent/plan.md` (whole-file replacement).
- C2: append RECORD3 to `.agent/live_review.md` per G3's procedure.
- C3: apply CC_IMPORT and CC_MODULE pairs to
  `packages/orchestration/context_compiler.py`.
- C4: apply TEST_P1 through TEST_P5 to
  `tests/orchestration/test_context_compiler.py`.
- C5: the round 4 handback (rewrite `.agent/handoff.md`, commit, push).
