# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495` (the
merge of PR #217, which closed F032). `.agent/decisions.md` holds F037 D1 to D11.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse and
virtual scrolling. `docs/roadmap/features/T5_F037.md` holds Goal & Done, the task
slicing, the binding CSS and the design amendments A1 through A6, the last of
which records what this feature deliberately no longer ships.

## Current Step
R24 is the SCOPE REPORT round. F037 has reached session 7 of a seven-session soft
limit, so operator amendment amend0827-process-diet rule 6 makes a report the
next obligation rather than more work. This round books the R23 verdict, resolves
`R-0731`, records DECISION F037 D11 splitting the three unbuilt pieces out of the
feature, amends the feature file to say so, and writes the report into the
handback. Nothing under `apps/`, `packages/` or `tests/` is touched.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R23 verdict and one resolution | ordered | record first |
| C3 DECISION F037 D11 | ordered | the ruling, not a question |
| C4 the feature-file amendment A6 | ordered | after the decision it cites |
| C5 the handback carrying the scope report | ordered | |

## Next Steps
1. The closure sequence for F037 as amended by A6: the integration-gate round,
   then the evidence-and-zip round, then the STATUS round.
2. The split-off scope — wiring `loadDiffLanguageBundle` into `DiffView`, the
   10k-line perf measurement, and the sidebar visual ruling — wants its own
   STATUS line. That is a PROPOSAL to the operator and is not executed here.

## Risks
- A6 narrows what F037 ships. Reversing it is one paragraph in each of
  `.agent/decisions.md` and the feature file, both named in D11.
- `loadDiffLanguageBundle` has NO production caller at `82d3d584`, measured by
  the reviewer with `git grep -l`: the lazy-bundle model is complete and unwired,
  and A6 exists so that gap is stated rather than silent.
