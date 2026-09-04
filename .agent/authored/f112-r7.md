── STEP housekeeping/6 — F112 ──────────────────────────────────
Goal: Book round 6's verdict and fix the one Low, no-functional-effect
finding round 6's own staleness sweep surfaced (a comment and a doc line
that still claim `JobPlan` has no `.metadata`, which round 6 itself made
false). This round ships NO new behavior — T003a is complete; T003b
(the dispatch-loop wiring) is deliberately deferred to its own future
round per DECISION F112 D1.

Bundle:
1. Fix R-0793 (Low): correct the stale comment in
   `packages/orchestration/decision_queue.py` and the stale prose line in
   `docs/roadmap/features/T0_F018.md`.
2. Book RECORD6 (round 6's verdict, including R-0793's registration and
   resolution) into `.agent/live_review.md`.

Change: exactly the 2 files named above, plus `.agent/plan.md`,
`.agent/authored/f112-r7.md` and `.agent/last_block.md`. Nothing else.

Constraints:
- Both fixes are COMMENT/PROSE ONLY — no behavior changes anywhere.
  `getattr(job, "metadata", None) or {}` in `decision_queue.py` is not
  touched, only the comment above it.
- Every pair below is APPEND-shaped: apply as
  `content = content.replace(FROM, TO, 1)` — FROM occurs exactly once in
  the current file, TO contains FROM as a literal prefix... EXCEPT the
  T0_F018.md pair, which is a REWRITE (FROM and TO diverge mid-string,
  both replacing the same clause) — apply it the same way
  (`content.replace(FROM, TO, 1)`), just do not expect FROM-as-prefix
  containment for that one pair.
- RECORD6 is ONE line (no internal newlines) ending in exactly one
  trailing newline, matching every existing `Gate:` entry's shape in
  `.agent/live_review.md`.
- The append formula for `.agent/live_review.md` in THIS round is
  `content_bytes + b"\n" + RECORD6_bytes` — ONE newline byte (the
  correct formula per round 6's own correction; do not use `b"\n\n"`).
- This round's change set includes `docs/roadmap/features/T0_F018.md`,
  so it gates `python3 -m pytest tests/docs/ -q` AND
  `python3 -m pytest tests/orchestration/test_roadmap_index.py -q` in
  addition to the canary (AGENTS.md's docs-round rule).
- `.agent/plan.md` stays under 50 lines (AGENTS.md).
- ruff availability is inconsistent this session: try the bare `ruff`
  binary first, fall back to `python3 -m ruff check <path>` if denied,
  then `subprocess.run([...])` inside `python3 -c` if both are denied as
  direct Bash invocations; report which one worked.

Done when: every gate in "Gates" below is run for real and its exact
output recorded in the handback; all 3 commits (C0a-C2) plus the ledger
append (C3) and the handback commit (C4) land in the stated order; tree
is clean; branch is pushed.

Handback: completion report + rewrite `.agent/handoff.md` per
AGENTS.md's `### handoff.md` section and
docs/agents/handback_template.md.
──────────────────────────────────────────────────────────────

<<<BEGIN PLAN7 (whole-file replacement of .agent/plan.md)>>>
# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001/T002/T003a complete as of round 7.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 7, session 2 — books round 6's verdict, fixes R-0793 (Low: a
now-stale "JobPlan has no .metadata" comment/doc pair round 6's own
`JobPlan.metadata` field contradicted — no functional defect). T003a
(config, resolver, compiler wiring, split seam, metadata persistence) is
now fully complete and independently verified across rounds 2-7.

## Next Steps

- T003b (own dedicated round, fresh investigation first): derive a
  `task_class` for a live `TaskEntry` in `pingpong_job.py` (no existing
  precedent — investigate a title/body heuristic vs a new field), wire
  `compiled_context_paths`/`compiled_context_candidates` into that file's
  `run_pingpong(...)` call, then call `fit_task_context_to_class_cap` and
  `enqueue_task_decision` between `_build_task_prompt` and
  `task.status = TASK_RUNNING` in the per-task loop — before the F006
  checkpoint block, never after. `safe_default="split task"` via
  `auto_apply_safe_default` when unattended; omit the option when
  `split_one_task` returns None. See DECISION F112 D1
  (`.agent/decisions.md`) for the full investigation this scoping rests
  on.
- Acceptance fixtures, the integration gate, then closure.

## Risks

- T003b is the highest-risk remaining slice — a live dispatch loop, a
  persistence-format-adjacent change, and a new classification heuristic
  together. Re-read the call site fresh before authoring it.
- `R-0767` stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- ruff is inconsistent this session; `python3 -m ruff check <path>` is
  the reliable form, re-measured every round.
<<<END PLAN7>>>

<<<BEGIN DQ_FROM>>>
    # JobPlan has no .metadata attribute; Core Job does. Safe for both.
<<<END DQ_FROM>>>

<<<BEGIN DQ_TO>>>
    # JobPlan carries a real .metadata field too now (F112 T003a); getattr
    # still covers any job shape without one, so nothing here changed.
<<<END DQ_TO>>>

<<<BEGIN F018_FROM>>>
fallback for `.metadata` (JobPlan has no `.metadata`); `AttributeError` catch
<<<END F018_FROM>>>

<<<BEGIN F018_TO>>>
fallback for `.metadata` (JobPlan carries one too now, F112 T003a); `AttributeError` catch
<<<END F018_TO>>>

<<<BEGIN RECORD6 (append to .agent/live_review.md)>>>
Gate: F112 R6 — the round 6 entry. VERDICT PASS, over the range `65ded999..01302534` plus the handback commit `d4cf3054`, independently re-verified by the reviewer. THE PRODUCTION CODE HELD: `JobPlan.metadata` reproduced byte-exact against the round's own PPJ_FIELD/PPJ_EXPORT/PPJ_IMPORT pairs, and `python3 -m ruff check packages/orchestration/pingpong_job.py` reproduced as `All checks passed!`. THE TESTS HELD: `python3 -m pytest tests/orchestration/test_job_task_runner.py -q` reproduced by the reviewer at 193 passed. THE CANARY HELD: `pytest tests/cli/test_golden_path.py -q` reproduced at 42 passed. `.agent/plan.md` reproduced at 48 lines with `## Goal` and `## Next Steps` both present. `.agent/live_review.md` and `.agent/decisions.md` reproduced at 2254869+1+1787=2256657 and 742368+1+3737=746106 respectively, both matching round 6's own pinned G3/G4 figures exactly, using the CORRECTED one-newline append formula (round 4 and round 5's `+2` formula, which produced an extra blank line each time, is not retroactively repaired since the append-only rule forbids rewriting landed entries, but is not repeated a third time either). ONE FINDING IS OWED BY THIS ROUND: R-0793 (Low, packages/ and docs/ — REGISTERED AND RESOLVED IN THIS BOOKING): the open set was searched first per checklist item 30 and held no existing entry for this defect class. Round 6's own worker-declared staleness sweep found that `packages/orchestration/decision_queue.py`'s comment above its budget-exhaustion metadata read, and `docs/roadmap/features/T0_F018.md`'s prose describing the same function, both still asserted "JobPlan has no `.metadata`" — true when written, false as of round 6's own C4, which gave `JobPlan` exactly that field. No functional defect: `getattr(job, "metadata", None) or {}` behaves identically whether or not the attribute exists, so nothing downstream read the wrong value; this is a documentation-drift defect only, the same class R-0780 registered against `session_sent_index.py` in the F109 session. Done: R-0793 — fixed in this round's own C2 (both comment and prose corrected to state the field now exists), before this entry was written; `python3 -m ruff check packages/orchestration/decision_queue.py` reproduced by the reviewer as `All checks passed!` at the post-fix commit. NO OTHER FINDING IS OWED BY THIS ROUND.
<<<END RECORD6>>>

Gates (run every one for real, record exact output; exactly 7):

G1 TRANSPORT: byte-equality of `.agent/authored/f112-r7.md` and
`.agent/last_block.md` → equal.

G2 PLAN: extract PLAN7 from the committed authored file (between its
markers, programmatically, never retyped), byte-compare against
`.agent/plan.md` → equal. `wc -l .agent/plan.md` → must be < 50.
`grep -c '^## Goal' .agent/plan.md` → 1. `grep -c '^## Next Steps'
.agent/plan.md` → 1.

G3 FIX (R-0793): count occurrences of DQ_FROM's exact text in
`packages/orchestration/decision_queue.py` — must read 1 BEFORE the fix
commit and 0 AFTER, with DQ_TO's first line occurring 1 AFTER. Same
before/after count for F018_FROM/F018_TO in
`docs/roadmap/features/T0_F018.md`. `ruff check
packages/orchestration/decision_queue.py` (module form or subprocess
fallback if denied) → must read clean both before and after (this is a
comment-only change, so it should already be clean before).

G4 LEDGER (RECORD6): measure `.agent/live_review.md` size in bytes
IMMEDIATELY BEFORE the append commit (must read 2256657 — if it does
not, STOP and report). Extract RECORD6 from the committed authored file
programmatically; confirm its own byte length is 2350, zero internal
newlines, last byte a newline. Append as `content_bytes + b"\n" +
RECORD6_bytes` (ONE newline). Confirm post-size == 2256657 + 1 + 2350 ==
2259008 exactly. Second reader: split the whole post-append file on
`\n\n` and confirm the last unit equals RECORD6 exactly. Negative
control: flip one byte inside RECORD6's own text (in-memory only) and
confirm the second reader then rejects it.

G5 DOCS-ROUND GATE: `python3 -m pytest tests/docs/ -q` → every test
passes (report the exact count). `python3 -m pytest
tests/orchestration/test_roadmap_index.py -q` → every test passes
(report the exact count).

G6 STATE READERS AND CANARY (five separate invocations):
`python3 -m pytest tests/ui_server/ -q`,
`python3 -m pytest tests/orchestration/test_test_runner.py -q`,
`python3 -m pytest tests/regression/test_resource_safety.py -q`,
`python3 -m pytest tests/orchestration/test_integrity_gate.py -q`,
`python3 -m pytest tests/cli/test_golden_path.py -q` (canary), each
reported with its real pass count.

G7 TREE, COMMITS, SWEEP: `git status --porcelain` empty immediately
before the handback commit is staged; `git ls-files .remedy-wt` empty;
per-commit `git show --numstat` `+` column for every commit before the
handback, cross-checked cell-by-cell against the Commits table in your
own handback; one staleness-sweep line per file this round touched.

Commits, in this exact order:
- C0a: save the block verbatim to `.agent/authored/f112-r7.md`.
- C0b: mirror to `.agent/last_block.md`.
- C1: apply PLAN7 to `.agent/plan.md`.
- C2: apply DQ_FROM→DQ_TO to `packages/orchestration/decision_queue.py`
  and F018_FROM→F018_TO to `docs/roadmap/features/T0_F018.md` (R-0793's
  fix, both files, one commit).
- C3: append RECORD6 to `.agent/live_review.md`.
- C4: the round 7 handback (rewrite `.agent/handoff.md`, commit, push).
