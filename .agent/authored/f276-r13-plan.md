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

Round 13 books round 12's verdict PASS, registers and REPAIRS `R-1010`, and
then builds the closure evidence round 12 could not. R-1010 is the reason
round 12's evidence job raised: `parse_safe_diff_paths` could not read back
a hunkless diff entry, so the empty `claude_planner/__init__.py` the merge
carried in made the producer's own path-set equality unsatisfiable and no
review package could be built. The repair widens that one reader — which
serves the bundle writer and the manifest validator alike — to take a path
from its entry's header, with a deleted entry still excluded. Then the
integrity check, the evidence job, and a FRESH package from the clean tree
at this round's own handback commit, whose `base_commit` is the FORK POINT
`43d148177efd145f179ba2d9875eaa675b1595b7`.

## Next Steps

1. The closure commit, the LAST on the branch: the reviewer-authored STATUS
   `[x]` line, the README capability paragraph and counters in the SAME
   commit, SU-024's `consumed_by` set to f276, and the final `.agent/`
   state including the handoff rewrite that records the package.
2. The pull request into `main`, carrying what changed, why, the key
   decisions, the changed-files table, the latest verdict, the
   open-findings count and the runtime actuals. It is NOT merged this
   session; the next feature's Open PR Gate merges it.
3. The open findings are carried, not resolved — 19 by distinct id at
   `b8ecbb7a`, each naming F282, and R-1010 resolved by this round rather
   than carried. R-0984's hosted-CI reading is answered by the first CI run
   of this pull request.

## Risks

The package is the one step that fails late, and round 12 proved it. The
producer's own path-set equality, an abbreviated `base_commit`, a node-id
list not taken from `--collect-only`, or a directory where a file path
belongs each surface only at build time.
