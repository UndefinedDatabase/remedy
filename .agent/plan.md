# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 3, round 14.

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
| T002 the client digest seam and its guard | done | round 6, PASS |
| T002 the trigger, dismiss and last-seen rule | done | round 7, PASS |
| T002 the hero card stylesheet and its guard | done | round 8, PASS |
| T002 the card's copy rules and the §17 screen | done | round 9, PASS |
| T002 the card component and its guard | done | round 11, PASS |
| T002 the storage edge (dismissal + last-seen) | done | round 12, PASS |
| T002 the fetch loader `loadJobDigest` | done | round 13, PASS |
| T002 the mount into `RemedyShell.tsx` | done | this round |
| T003 CLI parity and the end-to-end | open | next |

## Next Steps
1. This round mounts the card for real: the load, the storage edge bound to
   `window.localStorage`, last-seen and dismissal wiring, and placement as
   a sibling of the shell div — `<main>` stays at exactly four children.
   `onOpenDecisions`/`onPrimaryAction` stay unwired.
2. The next round is T003: `remedy job digest <id>` CLI parity, then the
   end-to-end (finish a fake job while the UI is "away", reopen, hero shows
   the right CTA, dismiss, no re-show), the integration gate and closure.
3. Wiring `onOpenDecisions`/`onPrimaryAction` for real needs its own
   resolution design (D5's "in-page action") and is not yet scheduled.

## Risks
- R-0570, R-0752 and R-0755 stay OPEN and are routed to the paydown branch;
  none is F040's to fix. R-0753 stays OPEN as this feature's documented risk.
- `browserDigestPort.ts`'s open risk (a real browser refusing a write) is
  still unaddressed and still deferred to whichever round first meets it.
