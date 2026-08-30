# Plan — F258 Self-use track v2

Branch: feature/f258-self-use-v2, cut from `main` at `18ae7129`, the merge
commit of pull request 225. SESSION 3, round 11.

## Goal
"Remedy is used on Remedy" keeps running with zero operator input: a generator
replenishes the self-use queue with exactly one dated, provenanced item
whenever it is empty at close, the consumed item is actually RUN through the
real job path under a small budget and stopped at the normal approval gate
rather than only planned, and any defect the run surfaces flows back into the
standard finding ledger.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001/T002/T003, integration gate | done | rounds 2-7 |
| all six closure preconditions | done | rounds 8-10 |
| the evidence bundle and the review zip | done | this round, closure steps 1-2 |
| the closure commit and the PR | open | next, and it is the last round |

## Next Steps
1. The closure commit, in ONE commit: the `[x]` flip on F258's line of
   `docs/roadmap/STATUS.md`, the README capability sync that may never
   disagree with it, the `scripts/self_use_queue.json` `consumed_by` edit
   that marks SU-002 consumed by F258, and the final `.agent/` state.
2. Open the pull request. It is NOT merged in this session — the gap is
   the operator's manual-review window, and the next feature's Open PR
   Gate merges it.

## Risks
- R-0570 (Low), R-0736 (Medium), R-0757 (Medium): all OPEN, all
  documented, none block a PASS WITH RISKS closure.
- `docs/roadmap/STATUS.md` is in `scope_fences.BUILTIN_DENY` and stays
  there.
- A job must never mark its own queue item consumed; DECISION F257 D2
  rules the consumption point stays the closure commit's edit.
