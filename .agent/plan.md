# Plan — Visual Addendum A1-A7

## Goal
Fix timeline visual regressions: event rail + legend always visible, exact CSS shape, rounded buttons, shell height reserve, regression tests.

## Current Step
Complete — all addendum steps done.

## Steps
- [x] A1: PhaseTimeline JSX — event rail + legend always rendered (not gated by hasEvents)
- [x] A2: PhaseTimeline CSS — exact shape from spec (border-radius: 28px, 148px min-height)
- [x] A3: Shell timeline height — clamp(150px, 16vh, 178px)
- [x] A4: Rounded button contract — metric icon shell 11px, tooltip z-index 9999
- [x] A5: PhaseGlyph icons verified — briefcase/calendar/code/clipboard-check/person/flag
- [x] A6: Regression tests — 10 new tests in TestVisualRegressionA6 (34 total in guard)
- [x] A7: Visual QA report
