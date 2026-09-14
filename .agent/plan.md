# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246. F275 closed
at `76283e69`, and pull request 250 carries the branch into `main`.

## Goal

Turn pull request 250's hosted CI green so that the Open PR Gate can merge it. Its only hosted
run, `34901124355` on `76283e69`, failed two tests of the event-name coupling ratchet: the
workflow checks out a single commit, and the ratchet reads the modules this branch deleted out
of git history. That defect is finding R-0889.

## Current Step

REPAIR ROUND 110 on the open pull request, by operator amendment amend0820-gate-autonomy. Its
bookkeeping commit books round 109's PASS and registers R-0889. Its fix commit makes the hosted
workflow's checkout fetch the full history and adds a guard that pins it. The worker then runs
the full suite once, commits the transcript, and hands back.

## Next Steps

1. The reviewer gives round 110 its verdict and watches the hosted CI run on the pushed tip.
2. With that run green, the Open PR Gate merges pull request 250.
3. The first reviewed round after the merge books round 110's verdict and the resolution of
   R-0889, and registers or resolves the closure candidate in `.agent/candidates.md`.

## Risks

- The hosted job now fetches the whole history: `git count-objects -vH` in the primary
  checkout at `76283e69` reads 74.10 MiB of packs, against a job cap of 90 minutes.
- The closure candidate stays in `.agent/candidates.md` through this round, because the
  Open PR Gate precedes the candidates rule in Phase 1 of the self-drive protocol.
