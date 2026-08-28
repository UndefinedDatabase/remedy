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
R25 is the INTEGRATION-GATE round, the first of F037's closure sequence. It books
the R24 verdict, resolves `R-0719` — whose counter-measure landed as amendment A4
at `c60a7318`, two commits after the entry that registered it, and was never
written up — and then runs the full suite twice: once on this branch and once in
a throwaway worktree at the merge base `9dde5495`, comparing the two failure sets
and attributing every branch-only id. The raw evidence lands under
`.agent/gate_f037_r25/`. Nothing under `apps/`, `packages/`, `tests/` or `docs/`
is touched.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R24 verdict and one resolution | ordered | record first |
| C3 the integration-gate evidence | ordered | the round's substance |
| C4 the handback | ordered | |

## Next Steps
1. The evidence-and-zip round: the feature file's Built State section, the
   `create_manual_completion_bundle` evidence job, and a FRESH review zip whose
   failure is a closure blocker.
2. The STATUS round: the `[x]` line, the README capability sync in the SAME
   commit, and the closure PR, which this session does not merge.

## Risks
- A6 narrows what F037 ships. Reversing it is one paragraph in each of
  `.agent/decisions.md` and the feature file, both named in D11.
- The base worktree lacks `apps/ui/node_modules` and `apps/ui/dist`. Both are
  restored with symlinks PRESERVED, or the base-only set fills with environment
  failures that mask the real ones.
