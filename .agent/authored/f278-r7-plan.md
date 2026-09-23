# Plan — F278 Durable writes & loud failures

Branch: feature/f278-durable-writes-loud-failures, cut from `main` at
`9817a927`, the merge commit of pull request 265 (F283's closure).

## Goal

One durable write in this repository, used everywhere, and no artifact that is
silently incomplete (`docs/roadmap/features/T2_F278.md`).

## Current Step

ROUND 7 books round 6's PASS, registers R-1036, R-1037 and R-1038 with
DECISION F278 D6, repairs R-1036 so a lost final job review is recorded as a
blocking one, and marks the second group of blind handlers: the job,
pingpong, apply, command-line, runtime and snapshot modules.

## Next Steps

1. The last marking round: repair R-1037 and R-1038 first, mark the third
   group, then turn BLE001 on in `pyproject.toml` with the ratchet test that
   freezes the count of excused handlers.
2. The closure sequence.

## Risks

Three open findings are this feature's own until they are repaired; the
closure cannot run while any of them is open.
