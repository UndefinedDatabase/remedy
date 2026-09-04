STEP T001 PART 1 / ROUND 2 - F112 Prompt budget per task class
FEATURE F112 - Prompt budget per task class (Tier 3) - SESSION 1, ROUND 2

Goal
  Book round 1's verdict into the ledger and land T001 part 1: the config
  schema and the new module packages/orchestration/prompt_budget.py
  (resolver + floor/vocabulary validator). No tests this round (round 3,
  for the 400-line block cap) and no compiler wiring (T002).

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f112-r2.md
  C0b mirror it to .agent/last_block.md
  C1  apply RECORD1 to .agent/live_review.md (append) and PLAN2 to
      .agent/plan.md (whole-file replacement)
  C2  apply CONFIG PAIR to packages/orchestration/config.py and write
      packages/orchestration/prompt_budget.py per MODULE (new file)
  C3  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f112-r2.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md (C1) - .agent/plan.md (C1) -
  packages/orchestration/config.py (C2) -
  packages/orchestration/prompt_budget.py (new, C2) - .agent/handoff.md (C3)

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by
     delimiter index from the COMMITTED .agent/authored/f112-r2.md -
     marker lines EXCLUDED - and write it with a script, never by
     retyping. If a slice looks wrong, apply it as written and DECLARE it
     in the handback.
  2. C1 is the first substantive commit of the round.
  3. RECORD1 appends to .agent/live_review.md as the single byte newline
     TWICE (two newline bytes) followed by the slice - the file's own
     existing convention (no blank-line separator missing, no extra one).
     PLAN2 REPLACES .agent/plan.md whole.
  4. THE CONFIG PAIR IS A REWRITE, NOT AN APPEND: verify FROM occurs
     EXACTLY ONCE in packages/orchestration/config.py before C2, apply
     str.replace(FROM, TO, 1), and confirm TO does not contain FROM
     (a genuine rewrite, since content is inserted BETWEEN the FROM's
     last two lines rather than after them).
  5. packages/orchestration/prompt_budget.py is a WHOLE NEW FILE: write
     MODULE's exact bytes with the Write tool (a "copyfile", never a
     text-extraction-and-reflow) and verify by extracting MODULE from the
     committed authored file and cmp against the written file.
  6. ruff is DENIED to this session (measured F112 R1's context claim);
     gate with python3 -m py_compile on both touched/created .py files
     instead, and additionally ATTEMPT ruff check yourself, reporting
     either its real output or the exact refusal text - never assume
     either way.
  7. Do NOT wire prompt_budget into context_compiler.py, role_config.py,
     or any call site - that is T002. This round's new module has ZERO
     production callers yet, which is expected and not a "dead code"
     defect at this stage.
  8. A sentence OUTSIDE the change set that this round makes stale is
     DECLARED in the handback and NOT repaired.
  9. Read .agent/STOP from disk before the first commit and again before
     C3. If it exists, finish the commit in hand, write the handback, and
     stop.
  10. Self-review loop before every commit (git diff --stat, git diff).
      Push after C3. No pull request, no merge.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f112-r2.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE LEDGER APPEND. Base size of .agent/live_review.md immediately
     BEFORE C1 (measure it yourself, do not trust a stated number):
     report its byte length and whether it ends with a trailing newline.
     RECORD1 has ZERO internal newlines - report its own byte length via
     UTF-8 encoding. Report: base + 2 + len(RECORD1) and whether that
     equals the post-C1 file's byte length. Then the SECOND, independent
     reader: split the WHOLE post-C1 file on blank-line boundaries and
     report whether the LAST unit equals RECORD1 exactly (N=1, so "last
     unit" and "final paragraph" are the same check). Then a NEGATIVE
     CONTROL in a scratch copy ONLY (never the tracked file): flip one
     byte inside RECORD1's own text and report that the second reader
     REJECTS it.
  G3 THE PLAN. Extract PLAN2 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md            -> exit 0
       wc -l .agent/plan.md                      -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G4 THE CONFIG PAIR. Count FROM in config.py BEFORE C2 (must be 1).
     After C2: FROM count, TO count, and the containment test's own
     output in these words:
       TO contains FROM: false
  G5 THE NEW MODULE. Extract MODULE from the COMMITTED authored file and
     cmp against packages/orchestration/prompt_budget.py -> exit 0.
     Then: python3 -m py_compile on both packages/orchestration/config.py
     and packages/orchestration/prompt_budget.py -> exit 0 each. Then
     ATTEMPT `ruff check packages/orchestration/prompt_budget.py
     packages/orchestration/config.py` and report the real result,
     success or refusal text, verbatim.
  G6 NO REGRESSION. python3 -m pytest tests/orchestration/test_config.py
     -q -> report the pass count; it must be a SUPERSET behavior of the
     pre-round count (no existing test in that file may be broken by the
     two new keys). No test file exists yet for prompt_budget.py itself
     (round 3) - do not invent one and do not order a mutation red-proof
     this round, because no test can yet catch a mutation to it
     (section 3 item 5).
  G7 THE STATE READERS AND THE CANARY, EACH AS ITS OWN INVOCATION:
       python3 -m pytest tests/ui_server/ -q
       python3 -m pytest tests/orchestration/test_test_runner.py -q
       python3 -m pytest tests/regression/test_resource_safety.py -q
       python3 -m pytest tests/orchestration/test_integrity_gate.py -q
       python3 -m pytest tests/cli/test_golden_path.py -q
     Report each pass count. THE FOUR STATE READERS ARE RUN AS FOUR, NOT
     AS THREE. The last is the canary.
  G8 THE TREE, THE COMMITS AND THE SWEEP. Read git status --porcelain
     immediately before C3 is staged, and git ls-files .remedy-wt (no
     output). Then, for C0a, C0b, C1 and C2 - the commits BEFORE the
     handback commit - report each one's insertion count from git show
     --numstat, the '+' column ONLY, and compare it CELL BY CELL against
     the Commits table of the handback you are writing. C3's own numbers
     go to NEITHER a round report NOR this file. Then THE STALENESS
     SWEEP over every file this round touched, one entry per file, stale
     or NOT stale, why.

Handback
  Rewrite .agent/handoff.md per docs/agents/handback_template.md. It
  carries the SESSION NUMBER of the running feature - this is SESSION 1
  of F112 - the state block, the item-status table with every ordered
  item appearing exactly once, the Commits table, one line per gate
  followed by the transcripts, the deviations, and the next steps. It has
  no length cap.

SLICES. Each slice lies between its own one-line BEGIN and END marker.
The marker lines are NEVER part of the slice. The slices carried here are
RECORD1, PLAN2, CONFIG PAIR FROM, CONFIG PAIR TO and MODULE.

<<<BEGIN RECORD1>>>
Gate: F112 R1 — the round 1 entry. VERDICT PASS, over the range `5c28c674..0092939e`. THE ROUND CLAIMED F112 IN THE STATUS LEDGER AND SET `.agent/plan.md` AND `.agent/context.md` FOR THE BRANCH; NO PRODUCTION CODE SHIPPED. TRANSPORT: the reviewer's own scratchpad original at `.remedy-wt/f112_r1_block.md` (gitignored, never committed) is BYTE-IDENTICAL to the committed `.agent/authored/f112-r1.md` — a direct Python byte comparison of both files' contents, not the worker's sha256 alone, confirmed the transport chain end to end. THE PLAN AND CONTEXT ARE BYTE-CORRECT: the reviewer re-extracted PLAN1 and CONTEXT1 from its own pre-emission scratch copies and diffed each against the committed `.agent/plan.md` (48 lines, under 50, exactly one `## Goal` and one `## Next Steps`) and `.agent/context.md` (exactly one `## Active Branch`, one `## Steps`) — both diffs were IDENTICAL. THE STATUS PAIR HELD: `docs/roadmap/STATUS.md` reads `- [~] F112 — Prompt budget per task class`, reproduced directly; a REWRITE, since the TO does not contain the FROM. THE SUITES WERE SPOT-CHECKED BY THE REVIEWER, NOT ONLY READ FROM THE HANDBACK: `tests/docs/` (295 passed), `tests/orchestration/test_roadmap_index.py` (30 passed) and the canary `tests/cli/test_golden_path.py` (42 passed) were RE-RUN independently and matched the worker's reported counts exactly; the round touched no path any of the other four gated suites cover, so their green readings carry no independent risk this round did not already retire. THE TREE HELD: `git status --porcelain` and `git ls-files .remedy-wt` were both re-run by the reviewer and were empty. NO FINDING IS OWED BY THIS ROUND.
<<<END RECORD1>>>

<<<BEGIN PLAN2>>>
# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 2, session 1 — T001 part 1: register `prompt_budget.task_class_caps`
and `prompt_budget.default_cap` in `packages/orchestration/config.py`
(mirroring the `model_routing.*` table-key pattern), and ship the new
module `packages/orchestration/prompt_budget.py` — resolver
`resolve_task_class_cap` (configured class cap > configured global default
> shipped fallback, all basis `class_default`) and floor + vocabulary
validator `validate_prompt_budget_config`, both reusing
`model_routing.TASK_CLASS_TIERS` as the one shared class vocabulary. No
tests land this round (round 3, for the 400-line block cap); no compiler
wiring (T002).

## Next Steps

- Round 3: `tests/orchestration/test_class_prompt_budget.py`, gating
  round 2's module, plus the mutation red-proof item 5 forbids ordering
  before a reachable test exists.
- T002: compiler cap enforcement in `context_compiler.py` — `fit(context,
  cap)`, the `cannot_fit` outcome with tier-1/cap/class arithmetic, and
  oversized/unfittable fixtures.
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
<<<END PLAN2>>>

<<<BEGIN CONFIG PAIR FROM>>>
        value_type=dict,
        entry_type=dict,
        default=None,
    ),
)
<<<END CONFIG PAIR FROM>>>

<<<BEGIN CONFIG PAIR TO>>>
        value_type=dict,
        entry_type=dict,
        default=None,
    ),
    # F112's per-class input-token cap table and its global fallback scalar.
    # Reuses the shared task-class vocabulary TASK_CLASS_TIERS declares
    # (packages/orchestration/model_routing.py) — the floor and vocabulary
    # checks specific to this feature live in
    # packages/orchestration/prompt_budget.py, not here (DECISION F110 D5
    # precedent: policy-level validation stays out of config.py).
    ConfigKeySpec(
        key="prompt_budget.task_class_caps",
        env_var="REMEDY_PROMPT_BUDGET_TASK_CLASS_CAPS",
        description=(
            "Per-task-class input token cap overrides (F112). Each entry's "
            "basis is class_default until F074 calibration ships measured "
            "caps. Configured in TOML only — an env var cannot carry a "
            "table."
        ),
        value_type=dict,
        entry_type=int,
        default=None,
    ),
    ConfigKeySpec(
        key="prompt_budget.default_cap",
        env_var="REMEDY_PROMPT_BUDGET_DEFAULT_CAP",
        description=(
            "Global fallback input token cap (F112) for a task class "
            "carrying no configured per-class cap. Falls back further to "
            "packages.orchestration.prompt_budget.DEFAULT_FALLBACK_CAP_TOKENS "
            "when unset."
        ),
        value_type=int,
        default=None,
    ),
)
<<<END CONFIG PAIR TO>>>

<<<BEGIN MODULE>>>
"""Per-task-class input token budget resolution and floor validation (F112).

Reuses the task-class vocabulary ``TASK_CLASS_TIERS`` declares
(packages/orchestration/model_routing.py) rather than inventing a second
one — a cap for a class routing does not recognize is refused outright.
Compiler wiring and the ``cannot_fit`` outcome are T002; this module ships
the config schema's reader, the resolver and the floor validation only.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING

from packages.orchestration.model_routing import TASK_CLASS_TIERS

if TYPE_CHECKING:
    from packages.orchestration.config import RemedyConfig

#: The only estimate basis this module can honestly claim until F074 ships
#: measured caps: every cap below, whichever layer resolved it, originates
#: from a config default rather than from a benchmark.
PROMPT_BUDGET_ESTIMATE_BASIS_CLASS_DEFAULT = "class_default"

#: Global fallback input-token cap, used when a task class carries neither
#: an operator-configured per-class cap nor an operator-configured global
#: override. Matches context_compiler.DEFAULT_CONTEXT_TOKEN_BUDGET (F107):
#: the compiler's existing whole-context budget, unchanged as the floor a
#: class falls back to until it earns a narrower one.
DEFAULT_FALLBACK_CAP_TOKENS = 24000

#: A cap below this is refused outright, regardless of what the fenced set
#: at compile time actually contains: tier-1 content is never demoted
#: (docs/roadmap/features/T3_F112.md Design), so a cap this small could not
#: hold even a single minimal fenced file's full text and is a
#: misconfiguration by construction, not a runtime condition to detect.
MIN_TASK_CLASS_CAP_TOKENS = 2000

TASK_CLASS_CAPS_CONFIG_KEY = "prompt_budget.task_class_caps"
DEFAULT_CAP_CONFIG_KEY = "prompt_budget.default_cap"


@dataclass(frozen=True)
class TaskClassCapResolution:
    """The resolved cap for one task class, with its provenance."""

    task_class: str
    cap_tokens: int
    source: str  # "configured_class" | "configured_default" | "shipped_default"
    estimate_basis: str


def resolve_task_class_cap(task_class: str) -> TaskClassCapResolution:
    """Resolve the input-token cap for ``task_class`` against live config.

    Raises ``ValueError`` for a class outside ``TASK_CLASS_TIERS`` — the one
    class vocabulary this feature and routing share
    (docs/roadmap/features/T3_F112.md "How it fits"). A per-class configured
    cap wins over a configured global default, which wins over the shipped
    fallback; every resolution carries basis ``class_default`` until F074
    ships measured caps.

    ``get_config`` is imported inside the body, mirroring
    :func:`packages.orchestration.role_config.resolve_effective_task_class_tiers`:
    this module has no module-level import of config.
    """
    if task_class not in TASK_CLASS_TIERS:
        raise ValueError(
            f"task class {task_class!r} is not part of the shared vocabulary "
            "in packages.orchestration.model_routing.TASK_CLASS_TIERS"
        )
    from packages.orchestration.config import get_config

    config = get_config()
    class_caps = config.get(TASK_CLASS_CAPS_CONFIG_KEY)
    if isinstance(class_caps, Mapping) and task_class in class_caps:
        return TaskClassCapResolution(
            task_class=task_class,
            cap_tokens=int(class_caps[task_class]),
            source="configured_class",
            estimate_basis=PROMPT_BUDGET_ESTIMATE_BASIS_CLASS_DEFAULT,
        )
    default_cap = config.get(DEFAULT_CAP_CONFIG_KEY)
    if isinstance(default_cap, int):
        return TaskClassCapResolution(
            task_class=task_class,
            cap_tokens=default_cap,
            source="configured_default",
            estimate_basis=PROMPT_BUDGET_ESTIMATE_BASIS_CLASS_DEFAULT,
        )
    return TaskClassCapResolution(
        task_class=task_class,
        cap_tokens=DEFAULT_FALLBACK_CAP_TOKENS,
        source="shipped_default",
        estimate_basis=PROMPT_BUDGET_ESTIMATE_BASIS_CLASS_DEFAULT,
    )


def validate_prompt_budget_config(config: "RemedyConfig") -> list[str]:
    """Return floor and vocabulary violations in ``config``'s prompt_budget keys.

    Empty list means the configured table (if any, or its absence) is
    valid. The generic per-entry TYPE check
    (:func:`packages.orchestration.config.validate_config`) is not
    duplicated here; this checks only what that function cannot know: the
    floor value and the shared vocabulary.
    """
    errors: list[str] = []
    class_caps = config.get(TASK_CLASS_CAPS_CONFIG_KEY)
    if isinstance(class_caps, Mapping):
        for task_class, cap in class_caps.items():
            if task_class not in TASK_CLASS_TIERS:
                errors.append(
                    f"{TASK_CLASS_CAPS_CONFIG_KEY} names unknown task class "
                    f"{task_class!r}; must be one of "
                    f"{sorted(TASK_CLASS_TIERS)}"
                )
                continue
            if isinstance(cap, int) and cap < MIN_TASK_CLASS_CAP_TOKENS:
                errors.append(
                    f"{TASK_CLASS_CAPS_CONFIG_KEY}.{task_class} is {cap}, "
                    f"below the floor of {MIN_TASK_CLASS_CAP_TOKENS} tokens "
                    "— too small to ever hold a single tier-1 fenced file"
                )
    default_cap = config.get(DEFAULT_CAP_CONFIG_KEY)
    if isinstance(default_cap, int) and default_cap < MIN_TASK_CLASS_CAP_TOKENS:
        errors.append(
            f"{DEFAULT_CAP_CONFIG_KEY} is {default_cap}, below the floor of "
            f"{MIN_TASK_CLASS_CAP_TOKENS} tokens — too small to ever hold a "
            "single tier-1 fenced file"
        )
    return errors
<<<END MODULE>>>