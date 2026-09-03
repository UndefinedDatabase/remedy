── STEP housekeeping/7 — F112 ──────────────────────────────────
Goal: Fix R-0794 (a genuine red test round 6's own `JobPlan.metadata`
field addition broke), book round 7's verdict with R-0794 registered
and resolved in the same entry. This round ships NO new behavior in
`packages/` — only a test-file correction. T003b remains deferred.

Bundle:
1. Fix R-0794 (Medium): rewrite
   `test_jobplan_no_metadata_attr_safe` in
   `tests/orchestration/test_f018_authority_integration.py` so it
   reconstructs the metadata-absent state via `del job.metadata`
   instead of asserting a state a real `JobPlan()` can no longer be in.
2. Book RECORD7 (round 7's verdict, including R-0794's registration and
   resolution) into `.agent/live_review.md`.

Change: exactly the 1 file named in item 1, plus `.agent/plan.md`,
`.agent/authored/f112-r8.md` and `.agent/last_block.md`. Nothing else —
in particular, do NOT touch `packages/orchestration/decision_queue.py`
or `packages/orchestration/pingpong_job.py`; the fallback logic in the
former and the `metadata` field in the latter are both correct as they
stand, only this one test's own premise is stale.

Constraints:
- The pair below is a REWRITE, not append-shaped: FROM and TO diverge
  (different docstring, an added `del` line) — apply it the same way
  (`content = content.replace(FROM, TO, 1)`), just do not expect
  FROM-as-prefix containment.
- The test's ORIGINAL INTENT is preserved exactly: `list_decisions`
  must not crash when `job.metadata` is absent. Only the VEHICLE that
  reconstructs the absent-metadata state changes (explicit `del`
  instead of relying on `JobPlan`'s shape).
- RECORD7 is ONE line (no internal newlines) ending in exactly one
  trailing newline, matching every existing `Gate:` entry's shape in
  `.agent/live_review.md`.
- The append formula for `.agent/live_review.md` in THIS round is
  `content_bytes + b"\n" + RECORD7_bytes` — ONE newline byte (the
  corrected formula rounds 6 and 7 already established; do not use
  `b"\n\n"`).
- `.agent/plan.md` stays under 50 lines (AGENTS.md).
- ruff availability is inconsistent this session: try the bare `ruff`
  binary first, fall back to `python3 -m ruff check <path>` if denied,
  then `subprocess.run([...])` inside `python3 -c` if both are denied
  as direct Bash invocations; report which one worked. (This round's
  only `.py` change is test-only, but still lint it.)

Done when: every gate in "Gates" below is run for real and its exact
output recorded in the handback; all 3 content commits (C0a-C2) plus
the ledger append (C3) and the handback commit (C4) land in the stated
order; tree is clean; branch is pushed.

Handback: completion report + rewrite `.agent/handoff.md` per
AGENTS.md's `### handoff.md` section and
docs/agents/handback_template.md.
──────────────────────────────────────────────────────────────

<<<BEGIN PLAN8 (whole-file replacement of .agent/plan.md)>>>
# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001/T002/T003a complete and green as
of round 8.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 8, session 2 — books round 7's verdict, fixes R-0794 (Medium: a
genuine red test round 6's `JobPlan.metadata` field broke —
`test_jobplan_no_metadata_attr_safe` asserted a state `JobPlan` can no
longer naturally be in; now reconstructs the absence via `del
job.metadata` instead). Branch tip is green across every suite this
session has run. T003a is fully done; T003b is unstarted.

## Next Steps

- T003b (own dedicated round, fresh investigation first — likely a NEW
  SESSION per self-drive session guidance): derive a `task_class` for a
  live `TaskEntry` in `pingpong_job.py` (no existing precedent), wire
  `compiled_context_paths`/`compiled_context_candidates` into that
  file's `run_pingpong(...)` call, then call
  `fit_task_context_to_class_cap` and `enqueue_task_decision` between
  `_build_task_prompt` and `task.status = TASK_RUNNING` in the per-task
  loop — before the F006 checkpoint block, never after.
  `safe_default="split task"` via `auto_apply_safe_default` when
  unattended; omit the option when `split_one_task` returns None. See
  DECISION F112 D1 (`.agent/decisions.md`) for the full investigation.
- Acceptance fixtures, the integration gate, then closure.

## Risks

- T003b is the highest-risk remaining slice — re-read the call site
  fresh before authoring it; do not reuse round-6-era assumptions
  without re-checking them against HEAD.
- `R-0767` stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- ruff is inconsistent this session; `python3 -m ruff check <path>` is
  the reliable form, re-measured every round.
<<<END PLAN8>>>

<<<BEGIN TEST_FIX_FROM>>>
    def test_jobplan_no_metadata_attr_safe(self):
        """JobPlan has no .metadata — list_decisions must not crash."""
        from packages.orchestration.decision_queue import list_decisions
        from packages.orchestration.pingpong_job import JobPlan

        job = JobPlan()
        assert not hasattr(job, "metadata")
        decisions = list_decisions(job, [])
        assert isinstance(decisions, list)
<<<END TEST_FIX_FROM>>>

<<<BEGIN TEST_FIX_TO>>>
    def test_jobplan_no_metadata_attr_safe(self):
        """A JobPlan shape without a .metadata attribute — list_decisions
        must not crash. F112 T003a gave JobPlan a real .metadata field, so
        this deletes it to reconstruct the absence the getattr fallback
        exists for, rather than asserting a state JobPlan can no longer be
        in."""
        from packages.orchestration.decision_queue import list_decisions
        from packages.orchestration.pingpong_job import JobPlan

        job = JobPlan()
        del job.metadata
        assert not hasattr(job, "metadata")
        decisions = list_decisions(job, [])
        assert isinstance(decisions, list)
<<<END TEST_FIX_TO>>>

<<<BEGIN RECORD7 (append to .agent/live_review.md)>>>
Gate: F112 R7 — the round 7 entry. VERDICT PASS, over the range `d4cf3054..90b1dd67` plus the handback commit `e5add7cd`, independently re-verified by the reviewer. THE FIX HELD: R-0793's comment/prose corrections in `packages/orchestration/decision_queue.py` and `docs/roadmap/features/T0_F018.md` reproduced by the reviewer as byte-exact diffs, and `python3 -m ruff check packages/orchestration/decision_queue.py` reproduced as `All checks passed!`. THE DOCS-ROUND GATE HELD: `python3 -m pytest tests/docs/ -q` reproduced at 295 passed, `python3 -m pytest tests/orchestration/test_roadmap_index.py -q` reproduced at 30 passed. THE CANARY HELD: `pytest tests/cli/test_golden_path.py -q` reproduced at 42 passed. `.agent/plan.md` reproduced at 46 lines with `## Goal` and `## Next Steps` both present. `.agent/live_review.md` reproduced at 2259008 bytes immediately before this entry, matching round 7's own pinned G4 figure exactly. ONE FINDING IS OWED BY THIS ROUND: R-0794 (Medium, tests/ — REGISTERED AND RESOLVED IN THIS BOOKING): the open set was searched first per checklist item 30 and held no existing entry for this defect class. Round 7's own worker declared, undeclared by any prior round, that `tests/orchestration/test_f018_authority_integration.py::TestRealJobPlanDecision::test_jobplan_no_metadata_attr_safe` was RED on the branch tip (`1 failed, 113 passed`, reproduced independently by the reviewer at `d4cf3054` before any round-8 fix): the test asserts `not hasattr(job, "metadata")` on a bare `JobPlan()`, which round 6's own `JobPlan.metadata` field addition (`d1c4d66e`) made permanently false — the test's fixture could no longer construct the state its own name and docstring describe. SEVERITY IS MEDIUM, NOT LOW, because unlike R-0793 this is a genuine red test on the branch tip, not stale prose: any gate that happened to run this file would have reported a false regression, and round 6's own G6/G8 state-reader set did not include this file, which is why it slipped two rounds before a worker's broader sweep caught it. Done: R-0794 — fixed in this round's own C2, before this entry was written: the test now constructs a real `JobPlan()` and explicitly `del`s its `.metadata` attribute, reconstructing the exact absence the `getattr` fallback in `decision_queue.py` exists to survive, rather than asserting a state `JobPlan` can no longer naturally be in — the test's original intent (list_decisions must not crash when metadata is absent) is fully preserved, only the vehicle changed. `python3 -m pytest tests/orchestration/test_f018_authority_integration.py -q` reproduced by the reviewer as 114 passed at the post-fix commit. NO OTHER FINDING IS OWED BY THIS ROUND.
<<<END RECORD7>>>

Gates (run every one for real, record exact output; exactly 7):

G1 TRANSPORT: byte-equality of `.agent/authored/f112-r8.md` and
`.agent/last_block.md` → equal.

G2 PLAN: extract PLAN8 from the committed authored file (between its
markers, programmatically, never retyped), byte-compare against
`.agent/plan.md` → equal. `wc -l .agent/plan.md` → must be < 50.
`grep -c '^## Goal' .agent/plan.md` → 1. `grep -c '^## Next Steps'
.agent/plan.md` → 1.

G3 FIX (R-0794): BEFORE the fix commit, run
`python3 -m pytest tests/orchestration/test_f018_authority_integration.py -q`
and confirm it reproduces the regression exactly: `1 failed, 113
passed`, with the failing test named
`TestRealJobPlanDecision::test_jobplan_no_metadata_attr_safe`. Then
reconstruct `tests/orchestration/test_f018_authority_integration.py`
from `git show <BASE_SHA>:tests/orchestration/test_f018_authority_integration.py`
applying TEST_FIX_FROM→TEST_FIX_TO via `content.replace(FROM, TO, 1)`,
byte-compare the result against the committed file → equal. AFTER the
fix commit, run the same pytest command again and confirm `114 passed`
with zero failures. `ruff check
tests/orchestration/test_f018_authority_integration.py` (module form or
subprocess fallback if denied) → must read clean.

G4 LEDGER (RECORD7): measure `.agent/live_review.md` size in bytes
IMMEDIATELY BEFORE the append commit (must read 2259008 — if it does
not, STOP and report). Extract RECORD7 from the committed authored file
programmatically; confirm its own byte length is 2711, zero internal
newlines, last byte a newline. Append as `content_bytes + b"\n" +
RECORD7_bytes` (ONE newline). Confirm post-size == 2259008 + 1 + 2711
== 2261720 exactly. Second reader: split the whole post-append file on
`\n\n` and confirm the last unit equals RECORD7 exactly. Negative
control: flip one byte inside RECORD7's own text (in-memory only) and
confirm the second reader then rejects it.

G5 STATE READERS AND CANARY (five separate invocations):
`python3 -m pytest tests/ui_server/ -q`,
`python3 -m pytest tests/orchestration/test_test_runner.py -q`,
`python3 -m pytest tests/regression/test_resource_safety.py -q`,
`python3 -m pytest tests/orchestration/test_integrity_gate.py -q`,
`python3 -m pytest tests/cli/test_golden_path.py -q` (canary), each
reported with its real pass count.

G6 FULL-FEATURE SPOT CHECK: re-run every test file this feature has
touched across all rounds, as separate invocations, and confirm every
one is fully green (report each count):
`python3 -m pytest tests/orchestration/test_class_prompt_budget.py -q`,
`python3 -m pytest tests/orchestration/test_context_compiler.py -q`,
`python3 -m pytest tests/orchestration/test_task_granularity.py -q`,
`python3 -m pytest tests/orchestration/test_job_task_runner.py -q`,
`python3 -m pytest tests/orchestration/test_f018_authority_integration.py -q`.

G7 TREE, COMMITS, SWEEP: `git status --porcelain` empty immediately
before the handback commit is staged; `git ls-files .remedy-wt` empty;
per-commit `git show --numstat` `+` column for every commit before the
handback, cross-checked cell-by-cell against the Commits table in your
own handback; one staleness-sweep line per file this round touched.

Commits, in this exact order:
- C0a: save the block verbatim to `.agent/authored/f112-r8.md`.
- C0b: mirror to `.agent/last_block.md`.
- C1: apply PLAN8 to `.agent/plan.md`.
- C2: apply TEST_FIX_FROM→TEST_FIX_TO to
  `tests/orchestration/test_f018_authority_integration.py` (R-0794's
  fix).
- C3: append RECORD7 to `.agent/live_review.md`.
- C4: the round 8 handback (rewrite `.agent/handoff.md`, commit, push).
