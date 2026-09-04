STEP F114 CLAIM / ROUND 1 - F114 Cost preview per command
FEATURE F114 - Cost preview per command (Tier 3) - SESSION 1, ROUND 1

Goal
  Claim F114 in the STATUS ledger and set .agent/plan.md and
  .agent/context.md for the branch, which the reviewer already cut from
  main at pull request 234's merge commit (a1b5d4bb). No production code
  this round: T001 (shared estimator extraction + band computation +
  basis labels + unit tests) lands over rounds 2 and 3.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f114-r1.md
  C0b mirror it to .agent/last_block.md
  C1  apply PLAN1 to .agent/plan.md (FIRST substantive commit)
  C2  apply PAIR S to docs/roadmap/STATUS.md and CONTEXT1 to .agent/context.md
  C3  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f114-r1.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/plan.md (C1) - docs/roadmap/STATUS.md (C2) - .agent/context.md (C2) -
  .agent/handoff.md (C3)

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by delimiter
     index from the COMMITTED .agent/authored/f114-r1.md - marker lines
     EXCLUDED - and write it with a script, never by retyping. If a slice
     looks wrong, apply it as written and DECLARE it in the handback.
  2. C1 is the first substantive commit of the round, before any other
     content commit.
  3. Newline conventions, measured on the scratch originals before
     emission and re-measured on the committed file after C1/C2: PLAN1
     and CONTEXT1 both end WITHOUT a trailing newline (the last byte of
     each slice, between its own END marker's preceding newline and the
     marker line, is not itself a newline) - .agent/plan.md and
     .agent/context.md must match, byte for byte, after C1/C2
     respectively. Report `tail -c 1 <path> | od -An -tx1` for both
     written files; neither may print `0a`.
  4. The STATUS edit is str.replace(FROM, TO, 1) on the file's text. No
     JSON or YAML round trip, no reformatting, no reflowing.
  5. PLAN1 and CONTEXT1 REPLACE their whole files.
  6. A sentence OUTSIDE the change set that this round makes stale is
     DECLARED in the handback and NOT repaired.
  7. Read .agent/STOP from disk before the first commit and again before
     C3. If it exists, finish the commit in hand, write the handback, and
     stop.
  8. Self-review loop before every commit (git diff --stat, git diff).
     Push after C3 (git push -u origin feature/f114-cost-preview-per-command).
     No pull request, no merge.
  9. This branch was cut directly by the reviewing session (git plumbing
     only - no file content was authored by that session; every byte in
     every commit still comes from a worker). PR #234, the PREVIOUS
     feature's PR, was already merged by the reviewer in an earlier
     session - do not touch it, do not run the Open PR Gate, do not
     re-create the branch. `git rev-parse HEAD` before C0a must read
     `a1b5d4bb455550f082da7d6c4c80fd968d6e1a88` (report the full SHA);
     `git branch --show-current` must read
     `feature/f114-cost-preview-per-command`.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f114-r1.md .agent/last_block.md
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
  of F114 - the state block, the item-status table with every ordered
  item appearing exactly once, the Commits table, one line per gate
  followed by the transcripts, the deviations, and the next steps. It has
  no length cap.

SLICES. Each slice lies between its own one-line BEGIN and END marker. The
marker lines are NEVER part of the slice. The slices carried here are
PLAN1, CONTEXT1, PAIR S FROM and PAIR S TO.

<<<BEGIN PLAN1>>>
# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 1, session 1 — claim F114 in the STATUS ledger and set this file
and `.agent/context.md`. Branch already cut. Round 2 extracts the shared
cost-arithmetic helper (`packages/orchestration/budget_guard.py:482-484`,
today inlined inside `predict_next_task_cost`) into
`packages/orchestration/token_economy.py` as `tokens_to_cost_usd()`, with
`predict_next_task_cost` refactored to call it (no behavior change).
Round 3 ships the new module `packages/orchestration/cost_preview.py`
(band estimator + basis labels) and its tests, completing T001.

## Next Steps

- Round 2: extract `tokens_to_cost_usd()`, refactor
  `predict_next_task_cost` to use it, regression-prove
  `tests/orchestration/test_budget_guard.py` unchanged.
- Round 3: `cost_preview.py` (`estimate_cost_band`) +
  `tests/orchestration/test_cost_preview.py` — completes T001.
- T002: CLI helper (`apps/cli`) — threshold confirm, tty/non-tty
  semantics (pipe never hangs), `--yes` audited, reusing
  `loop_cmd.py`'s `_confirm_materialization`/`_stdin_is_a_tty` pattern.
- T003: mark expensive commands in `apps/cli/command_catalog.py`,
  goldens for preview lines, docs.

## Risks

- No `cost_preview.py` or expensive-command registry exists yet — T003
  is greenfield, not a rename.
- Two class vocabularies exist (`model_routing.TASK_CLASS_TIERS` vs
  `token_economy.TokenBand`); the estimator commits to `TokenBand`
  (round 3 states which and why).
<<<END PLAN1>>>

<<<BEGIN CONTEXT1>>>
# Context — F114 Cost preview per command

## Active Branch
feature/f114-cost-preview-per-command, cut from `main` at the merge
commit of pull request 234.

## Scope
F114 (Tier 3, depends on F103 — done; enhanced by F074 calibration, not
yet built): commands that will spend real money show an upfront estimate
band with its basis and require confirmation above a configured
threshold in attended mode; unattended runs rely on budgets, not
prompts. Task slicing: T001 the shared estimator extraction + band
computation + basis labels + unit tests; T002 the CLI helper + threshold
+ tty/non-tty semantics + tests; T003 marking the expensive commands +
goldens for their preview lines + docs.

## Do not touch
The interactive guard's package boundary
(`tests/test_no_interactive_guard.py`, `_GUARDED_PACKAGES` / empty
`_ALLOWLIST`), budget enforcement, calibration (F074) — all explicitly
out of scope per `docs/roadmap/features/T3_F114.md` Do not touch.
Confirmation prompts live in `apps/cli` ONLY, never inside a guarded
package.

## Assumptions
- `packages/orchestration/budget_resolution.PredictiveBudgetConfig` /
  `resolve_predictive_budget_config()` already supply the reusable
  inputs (price basis + per-`TokenBand` class-default tokens); only the
  one-line multiply at `budget_guard.py:482-484` needs extracting, not a
  new config layer.
- `apps/cli/commands/loop_cmd.py` already has the reusable confirm
  pattern: `_confirm_materialization` (an `input()` y/N prompt),
  `_stdin_is_a_tty`, and the `--yes` flag
  (`apps/cli/command_catalog.py:653`) — T002 reuses this shape rather
  than inventing a second one.
- No `cost_preview.py` or expensive-command registry exists today
  (confirmed by search); T001/T003 are new files, not refactors of
  existing ones.
- The estimator commits to `token_economy.TokenBand` (LOW/MEDIUM/HIGH)
  as its class vocabulary, distinct from `model_routing.TASK_CLASS_TIERS`
  (a cost TIER, not a token-size band) — round 3 states this explicitly
  in `cost_preview.py`'s own docstring.

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
- `ruff check` is DENIED to this session's reviewer, measured at the
  F114 claim (`ruff check packages/orchestration/budget_guard.py`
  answers "This command requires approval"). A round of F114 that ships
  a `.py` file gates `python3 -m py_compile <path>` instead, and the
  worker attempts `ruff check` itself, reporting success or the exact
  refusal.

This round is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`, which AGENTS.md's "Completion Report — Item-Status
Table" section requires of every completion report. This file deliberately
does not restate it.
<<<END CONTEXT1>>>

<<<BEGIN PAIR S FROM>>>
- [ ] F114 — Cost preview per command
<<<END PAIR S FROM>>>

<<<BEGIN PAIR S TO>>>
- [~] F114 — Cost preview per command
<<<END PAIR S TO>>>
