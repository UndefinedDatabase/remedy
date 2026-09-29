# Plan — F042 Multi-project cockpit

Branch: feature/f042-multi-project-cockpit, cut from `main` at
`4e643440`, the merge commit of pull request 295 (F041 Artifact preview).

## Goal

Give the daily multi-repo reality a home in the cockpit: a grid of project
cards, a project switcher in the header, and deep links that carry
`?project=` (`docs/roadmap/features/T5_F042.md`, DECISION F042 D1).

## Current Step

ROUND 6 is reviewed PASS at `19ccafd4c`. ROUND 7, the integration gate,
was delegated (book round 6 with R-1111's resolution and DECISION F042
D7, land the closure's self-use item SU-036, complete the Built State,
prove the repair red, build `apps/ui`, run the one full suite) but its
worker found `.agent/STOP` present at BEFORE ANYTHING ELSE step 1 and
stopped immediately, per the block's own instruction and
`docs/agents/self_drive_protocol.md` Phase 1 rule 1. No payload was
applied, no commit beyond this handoff/plan pair was made. Round 7's
work is entirely undone and remains queued as originally specified.

## Next Steps

1. Phase 1 rule 1: re-read `.agent/STOP` from disk before anything else.
2. Once cleared, re-delegate round 7 as specified: book round 6, land
   SU-036's diff, complete the Built State, build the cockpit and run
   the one full suite.
3. The evidence round: the evidence bundle and the review package.
4. The closing round: the rotation, the STATUS line, the README and the
   pull request.

## Risks

Open findings: 2 (R-1107 owned by F290; R-1111 owned by F042, its test
landed this round).
