STEP F112 CLAIM / ROUND 1 - F112 Prompt budget per task class
FEATURE F112 - Prompt budget per task class (Tier 3) - SESSION 1, ROUND 1

Goal
  Claim F112 in the STATUS ledger and set .agent/plan.md and
  .agent/context.md for the branch, which the reviewer already cut from
  main at pull request 233's merge commit (5c28c674). No production code
  this round: T001 (config schema, resolver, validation, tests) is split
  across rounds 2 and 3 to respect the 400-line block cap
  (docs/agents/planner_reviewer_prompt.md section 3 item 1).

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f112-r1.md
  C0b mirror it to .agent/last_block.md
  C1  apply PLAN1 to .agent/plan.md (FIRST substantive commit)
  C2  apply PAIR S to docs/roadmap/STATUS.md and CONTEXT1 to .agent/context.md
  C3  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f112-r1.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/plan.md (C1) - docs/roadmap/STATUS.md (C2) - .agent/context.md (C2) -
  .agent/handoff.md (C3)

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by delimiter
     index from the COMMITTED .agent/authored/f112-r1.md - marker lines
     EXCLUDED - and write it with a script, never by retyping. If a slice
     looks wrong, apply it as written and DECLARE it in the handback.
  2. C1 is the first substantive commit of the round, before any other
     content commit.
  3. Newline conventions: this block's own PLAN1 and CONTEXT1 slices both
     end WITH a trailing newline (measured on the scratch originals before
     emission); .agent/plan.md and .agent/context.md must too after C1/C2.
  4. The STATUS edit is str.replace(FROM, TO, 1) on the file's text. No
     JSON or YAML round trip, no reformatting, no reflowing.
  5. PLAN1 and CONTEXT1 REPLACE their whole files.
  6. A sentence OUTSIDE the change set that this round makes stale is
     DECLARED in the handback and NOT repaired.
  7. Read .agent/STOP from disk before the first commit and again before
     C3. If it exists, finish the commit in hand, write the handback, and
     stop.
  8. Self-review loop before every commit (git diff --stat, git diff).
     Push after C3. No pull request, no merge.
  9. This branch was cut and PR #233 was merged directly by the reviewing
     session this session (git plumbing only - no file content was
     authored by that session; every byte in every commit still comes
     from a worker). Do not re-run the Open PR Gate or re-create the
     branch - both already exist. `git rev-parse HEAD` before C0a must
     read `5c28c674...` (report the full SHA).

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f112-r1.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE PLAN. Extract PLAN1 from the COMMITTED authored file to scratch,
     then:
       cmp <extracted> .agent/plan.md            -> exit 0
       wc -l .agent/plan.md                      -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G3 THE STATUS PAIR. Count FROM in docs/roadmap/STATUS.md BEFORE C2; it
     must be exactly 1 before anything is written. After C2 report the
     FROM and TO counts and the containment test's own output, in these
     words:
       TO contains FROM: false
     This pair is a REWRITE and the FROM-zero count is the right proof.
  G4 THE CONTEXT. Extract CONTEXT1 from the COMMITTED authored file and
     cmp against .agent/context.md -> exit 0. Then, on the written
     .agent/context.md, report each reading as a number, not as a word:
       grep -c '^## Active Branch'  -> 1
       grep -c '^## Steps'          -> 1
       count of 'feature/'          -> report the number
       first regex match of F followed by three digits -> report it
       'pytest' in the lowercased text -> report True
  G5 THE SUITES, EACH AS ITS OWN INVOCATION, RUN SERIALLY. This round edits
     no test and no production code, so a MOVED COUNT IS ITSELF THE
     FINDING.
       python3 -m pytest tests/docs/ -q
       python3 -m pytest tests/orchestration/test_roadmap_index.py -q
       python3 -m pytest tests/ui_server/ -q
       python3 -m pytest tests/orchestration/test_test_runner.py -q
       python3 -m pytest tests/regression/test_resource_safety.py -q
       python3 -m pytest tests/orchestration/test_integrity_gate.py -q
       python3 -m pytest tests/cli/test_golden_path.py -q
     Report the pass count of each; the reviewer will diff them against a
     base reading taken independently. THE FOUR STATE READERS ARE RUN AS
     FOUR, NOT AS THREE. The last is the canary every handback owes.
  G6 THE TREE, THE COMMITS AND THE SWEEP. Read git status --porcelain
     immediately before C3 is staged, and git ls-files .remedy-wt (no
     output - nothing under .remedy-wt/ is ever committed). Then, for
     C0a, C0b, C1 and C2 - the commits BEFORE the handback commit - report
     each one's insertion count from git show --numstat, the '+' column
     ONLY, and compare it CELL BY CELL against the Commits table of the
     handback you are writing. C3's own numbers go to NEITHER a round
     report NOR this file - the reviewer measures them at the next gate.
     Then THE STALENESS SWEEP over every file this round touched, one
     entry per file, stale or NOT stale, why.

Handback
  Rewrite .agent/handoff.md per docs/agents/handback_template.md. It
  carries the SESSION NUMBER of the running feature - this is SESSION 1
  of F112 - the state block, the item-status table with every ordered
  item appearing exactly once, the Commits table, one line per gate
  followed by the transcripts, the deviations, and the next steps. It has
  no length cap.

SLICES. Each slice lies between its own one-line BEGIN and END marker. The
marker lines are NEVER part of the slice. The slices carried here are
PLAN1, CONTEXT1, PAIR S FROM and PAIR S TO.

<<<BEGIN PLAN1>>>
# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, cut from `main` after
pull request 233 was merged at the Open PR Gate.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 1, session 1 — claim F112 in the STATUS ledger and set this file and
`.agent/context.md`. Branch already cut. T001 lands over the next two
rounds, split for the 400-line block cap (section 3 item 1): round 2 ships
the config schema (`prompt_budget.task_class_caps` +
`prompt_budget.default_cap`) and the new module
`packages/orchestration/prompt_budget.py` (resolver
`resolve_task_class_cap`, validator `validate_prompt_budget_config`,
reusing `model_routing.TASK_CLASS_TIERS` as the one shared class
vocabulary); round 3 ships that module's tests. No compiler wiring yet —
that is T002.

## Next Steps

- Round 2: `prompt_budget.py` + its config registration.
- Round 3: `tests/orchestration/test_class_prompt_budget.py`, gating
  round 2's module.
- T002: compiler cap enforcement in `context_compiler.py` — `fit(context,
  cap)` over the existing demotion order, plus the `cannot_fit` outcome
  with the tier-1-size/cap/class arithmetic, and oversized/unfittable
  fixtures.
- T003: the decision wiring (`escalation.enqueue_task_decision`, type
  `task_decision`) for "task context exceeds its class cap", unattended
  default split, and the granularity-machinery seam (see Risks).
- Acceptance fixtures, the integration gate, then the closure sequence.

## Risks

- `task_granularity.py`'s split helpers are module-private and built for
  plan-time normalization, not a live dispatched task; T003 may need a
  small public seam addition, never a fork of the heuristics themselves
  (feature file "Do not touch").
- `R-0767` stays OPEN on the model-routing seam this feature's config
  registration pattern borrows from; unrelated to F112, not absorbed.
<<<END PLAN1>>>

<<<BEGIN CONTEXT1>>>
# Context — F112 Prompt budget per task class

## Active Branch
feature/f112-prompt-budget-per-task-class, cut from `main` at the merge
commit of pull request 233.

## Scope
F112 (Tier 3, depends on F103 — done): every task class carries an
input-token cap; the context compiler fits under it via its documented
demotion cascade (distant signatures drop first) with full omission
disclosure; a context that CANNOT fit raises a task-split decision instead
of a truncated prayer. Task slicing: T001 config + validation + the
shared class vocabulary assertion + tests; T002 compiler cap enforcement
+ cannot_fit arithmetic + fixture; T003 the decision wiring + unattended
default (split) + an end-to-end where the split resolves the fit + tests.

## Do not touch
Calibration (F074), the demotion order itself, granularity heuristics
(reused, not modified) — all explicitly out of scope per
`docs/roadmap/features/T3_F112.md` Do not touch. Mid-file truncation stays
forbidden; enforcement lives inside the compiler, never as an outer
truncation.

## Assumptions
- `packages/orchestration/model_routing.TASK_CLASS_TIERS` is the ONE task
  class vocabulary; F112 reuses it rather than declaring a second one, and
  a cap for a class outside it is refused, not silently guessed.
- `packages/orchestration/context_compiler.py` already owns tiered
  selection, budget demotion (`compile_task_context`,
  `DEFAULT_CONTEXT_TOKEN_BUDGET = 24000`) and the omissions record
  (`OmissionRecord`, `write_omitted_context_json`); F112 gives it PER-CLASS
  caps and the hard-floor behavior, T002's job.

## Constraints
The bullets in this first group are STANDING project constraints, carried
forward from the context this file replaced.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree,
  never in the primary checkout, which satisfies `git status --porcelain`
  empty at every verdict.
- THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE.
- `ruff check` is DENIED to this session's reviewer, measured at the F112
  claim (`ruff check <path>` answers "This command requires approval").
  F110's opposite constraint was measured for a DIFFERENT session and does
  NOT carry forward. A round of F112 that ships a `.py` file gates
  `python3 -m py_compile <path>` instead, and the worker attempts `ruff
  check` itself, reporting success or the exact refusal.

This round is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`, which AGENTS.md's "Completion Report — Item-Status
Table" section requires of every completion report. This file deliberately
does not restate it.
<<<END CONTEXT1>>>

<<<BEGIN PAIR S FROM>>>
- [ ] F112 — Prompt budget per task class
<<<END PAIR S FROM>>>

<<<BEGIN PAIR S TO>>>
- [~] F112 — Prompt budget per task class
<<<END PAIR S TO>>>
