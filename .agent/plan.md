# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 4, round 16.

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
| T003 CLI parity — `remedy job digest <id>` | done | round 15, PASS |
| T003 the end-to-end (away, reopen, dismiss, re-arm) | done | this round |
| the integration gate | open | next |
| closure sequence | open | after the gate |

## Next Steps
1. This round adds `apps/ui/src/api/digestEndToEnd.test.ts`, chaining
   `decodeJobDigest` to `digestVisibility` to `digestCtaText` over one of the
   frozen golden shapes, proving the feature file's own script on the client:
   finish while away, reopen, correct CTA, dismiss, no re-show, re-arm.
2. The next round is the dedicated integration-gate round
   (docs/agents/integration_gate.md); a regression there is a normal repair
   round.
3. Then the closure sequence (STATUS_closure_protocol.md): evidence job, a
   fresh review zip, the STATUS line, the PR.
4. Wiring `onOpenDecisions`/`onPrimaryAction` for real needs its own
   resolution design (D5's "in-page action") and is not yet scheduled.

## Risks
- R-0570, R-0752 and R-0755 stay OPEN and are routed to the paydown branch;
  none is F040's to fix. R-0753 stays OPEN as this feature's documented risk.
- `browserDigestPort.ts`'s open risk (a real browser refusing a write) is
  still unaddressed and still deferred to whichever round first meets it.
