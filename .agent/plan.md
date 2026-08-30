# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 4, round 19.

## Goal
Coming back is calm: a digest endpoint condenses state, cost with its basis, top
ownership entries, open decisions and ONE primary action into a hero card, shown
at job end or on the first UI open after absence — the "what happened while I
was gone" answer in one glance.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the spec decisions D2 to D10 | done | rounds 2-9 |
| T001 the composition, endpoint, goldens | done | rounds 3-5, all PASS |
| T002 the client digest seam through the mount | done | rounds 6-14, all PASS |
| T003 CLI parity + the client end-to-end | done | rounds 15-16, all PASS |
| the integration gate | done | round 17, PASS |
| closure preconditions + Built State | done | round 18, all six CLEAR/NONE |
| closure evidence job + review zip | in progress | this round |
| STATUS line + README sync + PR | open | next, if the zip is READY |

## Next Steps
1. This round builds the closure evidence bundle and the review zip
   (STATUS_closure_protocol.md algorithm steps 1-2) and reports the four
   values a later round needs: evidence job id, package filename,
   SHA-256, accepted HEAD.
2. If the package reads READY_FOR_REVIEW, round 20 authors the STATUS
   line and syncs README in the same final closure commit (R-0154: they
   may never disagree in any committed state), then opens the PR. The PR
   merges at the next feature's Open PR Gate, not this session
   (STATUS_closure_protocol.md algorithm step 6).
3. If the zip build fails or packages BLOCKED_EVIDENCE, that is a closure
   BLOCKER: STOP and hand back with the exact rejection rather than
   repairing it in the same round.
4. Wiring `onOpenDecisions`/`onPrimaryAction` for real needs its own
   resolution design (D5's "in-page action") and is not yet scheduled —
   documented in the Built State section, not a blocker to closure.

## Risks
- R-0570, R-0752 and R-0755 stay OPEN and are routed to the paydown branch;
  none is F040's to fix. R-0753 stays OPEN as this feature's documented risk.
- `browserDigestPort.ts`'s open risk (a real browser refusing a write) is
  still unaddressed and still deferred to whichever round first meets it.
