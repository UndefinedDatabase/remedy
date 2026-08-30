# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 4, round 18.

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
| closure sequence | in progress | this round: Built State + preconditions |

## Next Steps
1. This round appends the R17 verdict to the ledger, writes F040's missing
   Built State section into its feature file, and declares the status of
   all six STATUS_closure_protocol.md preconditions against a fresh
   measurement.
2. If every precondition reads clear, round 19 builds the closure evidence
   job and the review zip (algorithm steps 1-2), reporting the four values
   (job id, package filename, SHA-256, accepted HEAD) a later round needs
   to author the STATUS line — never in the same round that authors it
   (R-0371: a value cannot be quoted before the tool that produces it
   runs).
3. Round 20 (or later) authors the STATUS line and README sync in the
   final closure commit, then opens the PR. The PR is not merged this
   session (G1 of self_drive_protocol.md; STATUS_closure_protocol.md
   algorithm step 6 defers the merge to the next feature's Open PR Gate).
4. Wiring `onOpenDecisions`/`onPrimaryAction` for real needs its own
   resolution design (D5's "in-page action") and is not yet scheduled —
   this is documented in the Built State section this round adds, not a
   blocker to closure.

## Risks
- R-0570, R-0752 and R-0755 stay OPEN and are routed to the paydown branch;
  none is F040's to fix. R-0753 stays OPEN as this feature's documented risk.
- `browserDigestPort.ts`'s open risk (a real browser refusing a write) is
  still unaddressed and still deferred to whichever round first meets it.
