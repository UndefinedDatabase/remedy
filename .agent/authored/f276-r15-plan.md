# Plan — F276 Data-root hygiene & disk budget

Branch: feature/f276-data-root-hygiene, cut from `main` at `43d14817`. The
operator merged `origin/main` back into it at `512ba69c`. Pull request 262
is OPEN and unmerged over it.

## Goal

Every directory class under the data root has a named owner and a reclaim
rule, an operator reclaims scratch through one preview-first command, and a
job refuses to start below a disk floor
(`docs/roadmap/features/T2_F276.md`).

## Current Step

Round 15 repairs what round 14's closure commit left red. It books round
14's verdict, registers `R-1011` — `README.md`'s accepted counter and its
Tier 2 Done cell still carried the pre-closure numbers, so the ledger
cross-check `tests/docs/` went red at `b07a2eda` — repairs both cells,
resolves the finding, and empties `.agent/candidates.md` of the entry round
14 filed. Commits on this branch are the work order that operator amendment
amend0820-gate-autonomy names when a check over an open pull request is red.

## Next Steps

1. The pull request is NOT merged this session. The next feature's Open PR
   Gate merges it, which is the operator's manual-review window.
2. The next session claims the next feature by Rule A5 and books this
   feature's closing verdict in its first round.
3. The open findings are carried, not resolved — 19 by distinct id, 12
   Medium and 7 Low, none High, every one naming `Owner: F282`. R-1010 and
   R-1011 were both raised and repaired inside this feature and are not
   among them.

## Risks

The hosted CI column on pull request 262 is the last unmeasured surface:
this branch carries main's own amend0920 work through the operator's merge,
and the pull request's first run is the first time that combination is
exercised on a hosted runner rather than here.
