# Plan — F015 Interactive plan editing

Branch: feature/f015-interactive-plan-editing, cut from `main` at
`fce49ce0`, the merge commit of pull request 273 (F267 List commands v2
completion).

## Goal

The human reshapes a job's task plan before approving it: six edit
commands, valid only while the plan's approval is open, each revalidated
and logged, reachable through the write channel and `remedy job plan-*`,
and execution follows the edited plan exactly, proven by hash
(`docs/roadmap/features/T5_F015.md`). Open findings: 4, all owned by F284.

## Current Step

ROUND 4: book round 3's PASS and land T003 under DECISION F015 D4 — the
approval's plan hash and its check at every job start, edits that keep
each task after the tasks it waits for, the `## Edits` section of an
edited revision with its goldens, and the end-to-end run of an edited
plan.

## Next Steps

1. The closure sequence's first half: the feature file's Built State,
   the checklist consolidation, the self-use track and the one full
   suite.
2. The closure sequence's evidence half and its closing round.

## Risks

None open inside this feature.
