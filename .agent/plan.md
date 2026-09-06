# Plan — amend0906-triage-throughput

Branch: feature/amend0906-triage-throughput, cut from main at `b18fad57`. Planning,
ledger and protocol text only; no product code and no test code except the
`TOTAL_FEATURES` pin.

## Goal

Triage every open finding into fixed / deletion-bound / process-only / product,
register the product remainder as F273, and land the three throughput rules for the
rebuild block. Then carry main into the open F272 branch so that branch can see all
of it.

## Current Step

Parts 0, A and B are complete and committed in six commits: the triage table, the
ledger resolutions, the prose_slips classes, the deletion-bound tag with the F272
and F261 sentences, the F273 registration with its pins, and the protocol paragraph
with DECISION amend0906-triage-throughput. The handoff is the sixth. Next is the
push, the pull request and its merge, then Part C.

## Next Steps

1. Push, open the PR, wait for hosted CI, merge on green, verify main.
2. Part C: merge `origin/main` into `feature/f272-one-world-completion` with
   `--no-ff`, keeping BOTH sides of every append-only conflict (main's block first),
   re-run `tests/docs/` and the canary on the merged branch, push, and append the
   merge record to that branch's `.agent/handoff.md` as one commit.
3. The operator runs `remedy-resume` and restarts the loop; F272 continues on its
   own branch at 12 sessions / 40 rounds.

## Risks

- `.agent/STOP` is present and untouched; this branch never starts the loop.
- The F272 branch has unpushed rounds of its own. Part C merges main INTO it and
  never rebases or force-pushes it.
