# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 545-564: Timeline exact fix and orchestrator loop semantics.

## Canonical Review File
`.agent/live_review.md` — NOT `.data/live_review.md`

## Timeline Failure — Steps 530-544 Did Not Produce Acceptable Timeline
- Done phase icons incorrectly replaced with TaskDoneGlyph checkmarks (icons vanish)
- Timeline event fallback creates fake dots from tasks (implies events that never happened)
- RemedyTimelineEvent type too weak (done: boolean, no state/title/cycle)
- CSS uses overflow: hidden (clips glow effects)
- CSS uses weak flex-centered layout
- Finalized gate too loose (marks done on job state alone, ignores pending/blocked tasks)
- Tests too shallow — allowed wrong visual structure to pass

## What Must Change
- Phase header: always PhaseGlyph, never replace with TaskDoneGlyph
- Done/current/pending = visual classes on icon shell + rail markers, not icon replacement
- Event rail: only real backend events, no task-based fallback
- RemedyTimelineEvent: state-based with title/cycle/timeLabel
- Finalized gate: strict (no pending tasks, no open approvals, no blocked tasks)
- Orchestrator loop: Build/Test/Review repeat, not waterfall
- Proposed tasks: distinct from planned tasks

## Resource Safety
All pytest runs use scripts/remedy_pytest.sh (flock + timeout).
