# Plan — F276 Data-root hygiene & disk budget

Branch: feature/f276-data-root-hygiene, cut from `main` at `43d14817` (the
merge commit of pull request 260, F273's closure). The operator merged
`origin/main` back into it at `512ba69c`.

## Goal

Every directory class under the data root has a named owner and a reclaim
rule, an operator reclaims scratch through one preview-first command, and a
job refuses to start below a disk floor
(`docs/roadmap/features/T2_F276.md`).

## Current Step

Round 14 CLOSES F276. It books round 13's verdict PASS, then lands the
closure commit — the LAST on this branch — carrying the STATUS `[x]` line,
the README Tier 2 entry in the SAME commit so the two can never disagree,
SU-024's `consumed_by` set to `f276`, and the final `.agent/` state. Then it
opens the pull request into `main`. Every precondition is met: T001 to T004
built, the integration gate green on the merged tree at `3359296e`, the
integrity check passing, the self-use item consumed, the ledger rotated, the
checklist consolidated, `R-1010` repaired and resolved, and the package
built and archived with its base at the fork point.

## Next Steps

1. The pull request is NOT merged this session. The next feature's Open PR
   Gate merges it, which is the operator's manual-review window.
2. The next session claims the next feature by Rule A5 and books this
   feature's closing verdict in its first round.
3. The nineteen open findings are carried, not resolved — 12 Medium and 7
   Low, none High, every one naming `Owner: F282 — Findings paydown v2`.
   R-0984's hosted-CI reading is answered by the first CI run of this pull
   request.

## Risks

None left inside this feature's scope. The one risk that remains is the
hosted CI column on the pull request: this branch carries main's own
amend0920 work through the operator's merge, and the first CI run is the
first time that combination is exercised on a hosted runner rather than
here.
