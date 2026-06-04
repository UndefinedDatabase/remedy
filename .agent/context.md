# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 530-544: Timeline visual rebuild to match target screenshot.

## Timeline Failure Acknowledgement
Timeline is still visually wrong after Steps 515-529.
Current timeline does not match target screenshot.
Specific failures: wrong icons (build=triangle, review=document), labels not beside icons in all states, journey line missing borders on dots, pending items not dashed-outline, legend uses colored dots instead of proper icons, backend missing job+finalized phases, no cycle semantics.

## What Is Changing
- New `RemedyTimelineEvent` type + `timelineEvents` on dashboard
- Backend `timeline_events` derived from event ledger
- PhaseTimeline.tsx full rewrite (phaseHeader + rail + eventRail + legend)
- PhaseTimeline.module.css full rewrite
- PhaseGlyph icon paths fixed (build=code, review=person)
- Shell height lock for timeline stability
- Timeline product tests

## Resource Safety
All pytest runs use scripts/remedy_pytest.sh (flock + timeout).
