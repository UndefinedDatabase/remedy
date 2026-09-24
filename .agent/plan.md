# Plan — F267 List commands v2 completion

Branch: feature/f267-list-commands-v2-completion, cut from `main` at
`9f06c509`, the merge commit of pull request 272 (F265 Teacher learning
UI v1).

## Goal

Every list command's handler honours `--sort`, `--desc`, `--since`,
`--until` and `--limit`, proved over the whole catalog rather than a
sample, and the ten-second demo is a test
(`docs/roadmap/features/T2_F267.md`). T001, the wirings, landed in F273.
Open findings: 4, all owned by F284.

## Current Step

ROUND 1: claim F267, re-head the live review record with F265's closing
verdict, record DECISION F267 D1, and land T002 and T003 as
`tests/cli/test_list_commands_everywhere.py`.

## Next Steps

1. The closure sequence's first half: the Built State, the checklist
   consolidation, the self-use track and the one full suite.
2. The evidence bundle and the fresh review package.
3. The closing round: the verdict bookings, the ledger rotation, the
   STATUS flip and the pull request.

## Risks

None open inside this feature.
