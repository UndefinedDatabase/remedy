# Plan — F276 Data-root hygiene & disk budget

Branch: feature/f276-data-root-hygiene, cut from `main` at `43d14817` (the
merge commit of pull request 260, F273's closure). The operator merged
`origin/main` back into it at `512ba69c`, which is why `git merge-base` no
longer answers the fork point and closure pitfall (e) is live here.

## Goal

Every directory class under the data root has a named owner and a reclaim
rule, an operator reclaims scratch through one preview-first command, and a
job refuses to start below a disk floor
(`docs/roadmap/features/T2_F276.md`).

## Current Step

Round 12 books round 11's verdict PASS, corrects one false clause the round
10 entry left in the ledger, and BUILDS THE CLOSURE EVIDENCE: the integrity
check, the evidence job through
`job_evidence.create_manual_completion_bundle` over the six test files this
feature created, and a FRESH review package from the clean tree at this
round's own handback commit. The package's name, SHA-256 and archived path
go to the reviewer, who authors the STATUS line from them per DECISION
F276 D11. Every closure precondition but the STATUS line itself is met:
T001 to T004 built, the integration gate re-run green on the merged tree at
`c6a519d1` at 17720 passed and 20 skipped, the self-use item consumed, the
ledger rotated, the checklist consolidated, and all 19 open findings
explicitly owned by F282.

## Next Steps

1. The closure commit, the LAST on the branch: the reviewer-authored STATUS
   `[x]` line, the README capability paragraph and counters in the SAME
   commit, SU-024's `consumed_by` set to f276, and the final `.agent/`
   state including the handoff rewrite that records the package.
2. The pull request into `main`, carrying what changed, why, the key
   decisions, the changed-files table, the latest verdict, the
   open-findings count and the runtime actuals. It is NOT merged this
   session; the next feature's Open PR Gate merges it.
3. The open findings are carried, not resolved — 19 by distinct id, each
   naming F282. R-0984's hosted-CI reading is answered by the first CI run
   of this pull request.

## Risks

The package is the one step that fails late. An abbreviated `base_commit`,
a node-id list not taken from `--collect-only`, or a directory where a file
path belongs each surface only at zip time; all three are checked before
the build rather than after it.
