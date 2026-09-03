## Authored texts

The block below (from "===AUTHORED BLOCK START===" to "===AUTHORED BLOCK END===") is what you save verbatim to `.agent/authored/f112-r13.md` in commit C0a.

===AUTHORED BLOCK START===

RECORD12 (append to .agent/live_review.md, one-newline formula — `content_bytes + b"\n" + RECORD12_bytes`, 1331 bytes):

Gate: F112 R12 — the round 12 entry. VERDICT PASS, over the range `2ef8c4dd..afb90730` (commits C0a through C5 — this round had six commits total, ending at C5, not eight), independently reviewed by the reviewer at the start of session 4's round 13. THE T3_F112.md AMENDMENT HELD: `git show 17ed4d52` reproduced the exact T003c bullet C4 describes, landing immediately after T003's own line. THE LEDGER APPENDS HELD BYTE-IDENTICAL: `.agent/authored/f112-r12.md` and `.agent/last_block.md` compare equal (10485 bytes both); `.agent/plan.md` measured at 2163 bytes / 47 content lines (46 newlines, no trailing newline), matching PLAN12 exactly; `.agent/decisions.md`'s tail matches DECISION F112 D5 exactly; `.agent/live_review.md`'s tail matches RECORD11 exactly. THE DOCS GATE HELD: `python3 -m pytest tests/docs/ -q` reproduced at 295 passed. THE CANARY HELD: `pytest tests/cli/test_golden_path.py -q` reproduced at 42 passed. THE NO-CODE CONSTRAINT HELD: `git show --stat 2ef8c4dd..afb90730` touches only `.agent/**` and `docs/roadmap/features/T3_F112.md` — no `packages/` or `tests/` path in the range, confirming the round's own declared scope. `git status --porcelain` read empty throughout. THE `cmp`-DENIAL SUBSTITUTION WAS REASONABLE AGAIN: the same documented, recurring sandbox property as round 11, not a shortcut.

<<<END RECORD12>>>

PLAN13 (whole-file replacement of .agent/plan.md, no trailing newline, 2049 bytes):

# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001/T002/T003a/T003b1/T003b2a/
T003b2b1 complete and green as of round 11; round 12 added T003c to
T3_F112.md's Task slicing (no code) as T003b2b2's prerequisite.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 13, session 4 — builds T003c per DECISION F112 D5's CHOSEN clause:
job task markdown gains a "Files:" inline marker (mirrors "Acceptance:"),
parsed into a new TaskEntry.files_hint: list[str] field, exported/
imported like inputs/task_class. task_entry_to_planned_task now passes
task.files_hint through instead of hardcoding [] (T003b2a's own
docstring updated to match).

## Next Steps

- T003b2b2 (own round(s), now unblocked): fit_task_context_to_class_cap
  + run_pingpong wiring at the dispatch site, using a task's real
  files_hint as compiled_context_paths (still [] and falling through to
  build_repo_context for a task with no Files: section — an honest,
  unchanged default, not a regression) + the cannot_fit decision call.
- Acceptance fixtures, the integration gate, then closure.

## Risks

- T003b2b2 remains the highest-risk remaining slice; re-read the call
  site fresh before authoring, same standing instruction as D2-D5.
- A task with no Files: section still cannot engage the capped path
  (use_compiled_context needs both lists non-empty) — worth flagging
  in T003b2b2's own investigation rather than assuming it's solved.
- R-0767 stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- ruff is inconsistent this session; python3 -m ruff check <path> is the
  reliable form, re-measured every round.

<<<END PLAN13>>>

===AUTHORED BLOCK END===
