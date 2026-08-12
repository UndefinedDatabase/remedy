# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0298. R19 reviewed PASS at 65723390; R20 and R21 are
gated on their committed items, each having stopped short on an environment
wall rather than route around one.

## Goal
The context compiler selects fenced-path files, their direct import neighbors,
and only SIGNATURES of distant dependencies, under a total context token budget
with tier demotion — and writes an omissions record naming everything it left
out and why. DONE when a fixture repo's task context shrinks measurably versus
whole-files with the fixture task still solvable by the fake provider, and the
omissions record explains every exclusion
(docs/roadmap/features/T2_F107.md).

## Current Step
R22 — the package, finally built. R-0297 records that R21's block named an
unreachable path; DECISION F107 D3a moves the archive inside the repository to
`.remedy-wt/.cache/f107-archive/`, which is gitignored and which the packager
prunes, so the 1834 unsafe members never reach the zip. The evidence bundle and
the package are rebuilt at this round's head and the package is verified by
opening it. Preconditions 1-5 otherwise hold: 22 open findings, none above
Medium, full suite re-confirmed twice, integrity check passed, Built State
current, tree clean and pushed.

## Next Steps
1. R23 — the closure commit: the reviewer-authored STATUS `[x]` line, the
   README capability sync in the SAME commit (R-0154), the final `.agent/`
   state, then the PR. Verdict PASS_WITH_RISKS for the five pre-existing
   R-0286 `[reviewer]` failures plus the R-0296 flake.
2. The closure PR is never merged in the session that creates it; it merges at
   the next feature's start via the AGENTS.md Open PR Gate.
