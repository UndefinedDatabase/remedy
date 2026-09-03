## Authored texts

The block below (from "===AUTHORED BLOCK START===" to "===AUTHORED BLOCK END===") is what you save verbatim to `.agent/authored/f112-r12.md` in commit C0a.

===AUTHORED BLOCK START===

RECORD11 (append to .agent/live_review.md, one-newline formula — `content_bytes + b"\n" + RECORD11_bytes`, 2195 bytes):

Gate: F112 R11 — the round 11 entry. VERDICT PASS, over the range `0ec9d2b9..2ef8c4dd` (commits C0a through C6), independently reviewed by the reviewer at the start of session 4's round 12. THE FIELD ADDITION HELD: `git show 21d79aa2 -- packages/orchestration/pingpong_job.py` reproduced the exact Pairs E/F/G (all REWRITE) C4 describes — the TaskEntry.inputs field plus its export/import round-trip; `git show 21d79aa2 -- tests/orchestration/test_job_task_runner.py` reproduced the exact two new TestPersistence tests. THE ESCALATION FIX HELD: `git show 01c87498 -- packages/orchestration/escalation.py` reproduced the exact Pair I (REWRITE) C5 describes — the dual-shape task-identifier lookup; `git show 01c87498 -- tests/orchestration/test_escalation.py` reproduced the exact TestJobPlanCompatibility class (2 tests). THE LEDGER APPENDS HELD BYTE-IDENTICAL: `.agent/authored/f112-r11.md` and `.agent/last_block.md` compare equal (10133 bytes both); `.agent/plan.md` (49 lines) matches PLAN11 exactly; `.agent/decisions.md`'s tail matches DECISION F112 D4 exactly; `.agent/live_review.md`'s tail matches RECORD10 exactly. THE TESTS HELD: `python3 -m pytest tests/orchestration/test_job_task_runner.py tests/orchestration/test_escalation.py -q` reproduced at 270 passed. THE LINT HELD: `python3 -m ruff check packages/orchestration/pingpong_job.py packages/orchestration/escalation.py tests/orchestration/test_job_task_runner.py tests/orchestration/test_escalation.py` read "All checks passed!". THE CANARY HELD: `pytest tests/cli/test_golden_path.py -q` reproduced at 42 passed. THE MUTATION CLEANUP HELD: `git worktree list` showed neither `f112-r11-mutation-c4` nor `f112-r11-mutation-c5`, and `git status --porcelain` read empty throughout — the mutation runs themselves were not re-executed by the reviewer this round, corroborated by the handback's own detailed before/after transcripts and the clean worktree list. THE DENIED-`cmp`-SUBSTITUTION DEVIATION WAS REASONABLE: the handback's own Python byte-equality read (`a == b` True, 10133 bytes both) is an equivalent proof to `cmp`'s exit code, and the sandbox denial is a documented, recurring session property, not a shortcut.

<<<END RECORD11>>>

PLAN12 (whole-file replacement of .agent/plan.md, no trailing newline, 2163 bytes):

# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001/T002/T003a/T003b1/T003b2a/
T003b2b1 complete and green as of round 11.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 12, session 4 — investigation of T003b2b2's call site found
run_pingpong's `use_compiled_context = bool(compiled_context_paths) and
bool(compiled_context_candidates)` requires BOTH lists non-empty, and
job-dispatch TaskEntry has no files_hint source — fenced_paths=[] (the
only value available today) makes the whole wiring a silent no-op,
always falling through to the uncapped build_repo_context path
(DECISION F112 D5). Stronger than D3/D4: not just cannot_fit
unreachable, the capped path never activates at all. T3_F112.md gains
T003c (a "## Files" job-markdown section feeding TaskEntry.files_hint)
as T003b2b2's prerequisite. This round is decision + plan + feature-file
only — no production code, since T003c must land first.

## Next Steps

- T003c (own round(s)): parse "## Files" in job task markdown (mirrors
  the existing "Acceptance:" inline-marker pattern) into a new
  TaskEntry.files_hint: list[str] field, exported/imported like
  inputs/task_class; update task_entry_to_planned_task's mapping.
- T003b2b2 (after T003c): fit_task_context_to_class_cap +
  run_pingpong wiring (now with real fenced_paths) + the cannot_fit
  decision call, now actually reachable.
- Acceptance fixtures, the integration gate, then closure.

## Risks

- T003b2b2 depends on T003c landing first; re-read both call sites
  fresh before authoring either.
- R-0767 stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- ruff is inconsistent this session; python3 -m ruff check <path> is the
  reliable form, re-measured every round.

<<<END PLAN12>>>

DECISION F112 D5 (append to .agent/decisions.md, one-newline formula, 5548 bytes):

## DECISION F112 D5 (2026-09-03, F112 R12) — run_pingpong's use_compiled_context gate requires BOTH fenced and candidate path lists non-empty; job-dispatch TaskEntry has no fenced-scope source, so T003b2b2's live wiring cannot activate the compiler at all until T003c adds one

CONTEXT. DECISION F112 D4 (F112 R11) left T003b2b2 as three pieces: the fit_task_context_to_class_cap call, the run_pingpong parameter wiring, and the cannot_fit -> enqueue_task_decision -> auto_apply_safe_default chain. Fresh investigation this round (reviewer, read-only, over packages/orchestration/pingpong_loop.py's run_pingpong, and pingpong_job.py's TaskEntry/task_entry_to_planned_task) re-checked the call site before authoring, per D2/D3/D4's own standing instruction, and found the plan as D3/D4 left it cannot work at all: run_pingpong's use_compiled_context gate (pingpong_loop.py:3115) is `bool(compiled_context_paths) and bool(compiled_context_candidates)` — BOTH lists must be non-empty, by the comment directly above it ("one list alone is a caller mistake and must not silently half-compile"). Job-dispatch TaskEntry carries no files_hint or any other fenced-scope declaration (confirmed again: TaskEntry's full field list, pingpong_job.py:119-146, has none), so the only value available for compiled_context_paths at this call site is `[]` — and `bool([])` is False. Wiring the three pieces as planned would silently keep use_compiled_context False forever, falling through to the untouched build_repo_context default path on every call: the class cap, the compiler, and the whole T003b2b2 round's work would exist in the code and never run once, for any task, ever. This is a stronger finding than D4's: D4 found one branch (cannot_fit) unreachable; this finds the ENTIRE compiled/capped path unreachable.

MEASURED. task_entry_to_planned_task (T003b2a, pingpong_job.py:150-176) deliberately sets files_hint=[] on the PlannedTask it returns, but that adapter feeds split_one_task's clustering (a DIFFERENT call, DECISION F112 D2's concern) — its empty files_hint has no bearing on what compiled_context_paths should be for run_pingpong, and D2/D3 never claimed it did. No existing job task markdown syntax declares a file scope: parse_job_file (pingpong_job.py:788-840) recognizes only a `## Task N` heading and an inline `Acceptance:` marker: two states (body, acceptance), no third. T3_F112.md's own "How it fits" section says "class comes from the same declaration routing uses" but says nothing about where FENCED SCOPE comes from for a job-dispatch task specifically — the Design section's "fit(context, cap)" sentence assumes a caller that already has fenced_paths, which is true for F107's other future callers (FlightPlan-derived tasks carry PlannedTask.files_hint natively) but not for this one.

CHOSEN. Add T003c to T3_F112.md's Task slicing: a job task markdown "## Files" section (a list of repo-relative paths, one per line), parsed by parse_job_file the same way "Acceptance:" already is (a third parser state, files_lines, joined into a new TaskEntry.files_hint: list[str] field, exported/imported like inputs and task_class), feeding compiled_context_paths at the T003b2b2 call site directly. T003b2b2 itself is NOT built this round: with no fenced-scope source, there is nothing correct to wire yet, and a block that ships plumbing between two points neither of which can be exercised would violate the reachable-red-proof rule (docs/agents/planner_reviewer_prompt.md §3 item 5) at the level of the WHOLE round, not one branch of it. This round's change set is DECISION F112 D5, the T3_F112.md amendment, and .agent/plan.md — no packages/ or tests/ path, an exception amend0827 rule 1 permits because a DECISION plus a feature-file amendment is planning content (the §4 item 7 "wrong spec is a finding routed to planning" shape), not a verdict, registration or correction.

ALTERNATIVE CONSIDERED AND REJECTED. Widen run_pingpong's use_compiled_context gate to accept a non-empty compiled_context_candidates alone (fenced_paths optionally empty), so job-dispatch tasks could engage the capped path today with an all-tier-2/3/4 compiled context and no tier-1 floor. Rejected: this changes F107's own already-shipped, already-tested activation contract for EVERY caller, not only this one, and the comment guarding it names the exact failure this would reintroduce ("must not silently half-compile") — the gate is deliberate design, not an oversight, and F112 has no standing to relax a different feature's safety rail to route around its own missing prerequisite. Building the missing prerequisite (T003c) is smaller, safer, and fixes the actual gap.

CONSEQUENCE. docs/roadmap/features/T3_F112.md's Task slicing gains T003c between T002 and T003, described as this round's own prerequisite finding, not an alternative design. `.agent/plan.md` Next Steps names T003c before T003b2b2. Task slicing's existing T003 one-line description ("the decision wiring + unattended default (split) + an end-to-end where the split resolves the fit + tests") is left as written: it remains true at the escalation-chain level (tests/orchestration/test_escalation.py's TestJobPlanCompatibility, T003b2b1) even though the live-dispatch-loop half of "end-to-end" now explicitly waits on T003c.

REVERSE by deleting this DECISION, reverting the T3_F112.md Task-slicing amendment, and treating T003b2b2 as D4 left it (buildable today) — which a fresh read of run_pingpong's use_compiled_context gate would immediately re-discover false.

<<<END D5>>>

===AUTHORED BLOCK END===
