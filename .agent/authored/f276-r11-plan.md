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

Round 11 books the verdicts of rounds 9 and 10, both PASS, records DECISIONs
F276 D11 and D12, and RE-RUNS the integration gate once on the merged tree.
The re-run is D12's subject: the transcript committed at `fd23710f` reads
17659 outcomes while `512ba69c` collects 17740, so the one file closure
precondition 2 reads by name no longer describes the tree being closed. The
new transcript replaces `.agent/authored/f276-closure-suite.txt` in place,
as round 8's already did. `apps/ui` is built before the run.

## Next Steps

1. The evidence round: `remedy integrity check --json`, the evidence job
   through `job_evidence.create_manual_completion_bundle` over the six test
   files this feature created, and a FRESH review package from the clean
   tree at that round's own handback commit, whose `base_commit` is the FORK
   POINT `43d148177efd145f179ba2d9875eaa675b1595b7` — now genuinely
   different from `git merge-base`, which the merge moved to main's tip. Its
   name, SHA-256 and archived path go to the reviewer, per DECISION F276 D11.
2. The closure commit, the LAST on the branch: the STATUS `[x]` line, the
   README capability paragraph and counters in the SAME commit, SU-024's
   `consumed_by` set to f276, and the final `.agent/` state. Then the pull
   request into `main`, which the next feature's Open PR Gate merges.
3. The open findings are carried, not resolved. At `512ba69c` the open set
   is 19 by distinct id: the seventeen round 9's C4 marked
   `Owner: F282 — Findings paydown v2`, plus `R-1008` and `R-1009`, which
   the merge carried in and which default to the same owner.

## Risks

The package is the one step that fails late. An abbreviated `base_commit`, a
node-id list not taken from `--collect-only`, or a directory where a file
path belongs each surface only at zip time; all three are checked before the
build rather than after it.
