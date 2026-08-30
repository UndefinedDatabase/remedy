# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 4, round 20 — CLOSURE.

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
| closure evidence job + review zip | done | round 19, READY_FOR_REVIEW |
| STATUS line + README sync + PR | in progress | this round |

## Next Steps
1. This round flips F040 to `[x]` in STATUS.md, syncs README (accepted
   count, Tier 5 Done cell, F040's capability paragraph) in the SAME
   commit, records one closure-candidate finding (F033's own missing
   README paragraph, found during this round's audit — not F040's to
   fix), and opens the PR.
2. The PR is NOT merged this session (self_drive_protocol.md G1;
   STATUS_closure_protocol.md algorithm step 6) — it merges at the next
   feature's Open PR Gate, or the operator merges it manually at any time.
3. End Window 1 with the feature-done banner once the PR is open and the
   handback is written.
4. Wiring `onOpenDecisions`/`onPrimaryAction` for real needs its own
   resolution design (D5's "in-page action") and is not yet scheduled —
   documented in the Built State section, carried forward as a known
   post-closure item, not a blocker.

## Risks
- R-0570, R-0752 and R-0755 stay OPEN and are routed to the paydown branch;
  none is F040's to fix. R-0753 stays OPEN as this feature's documented risk.
- `browserDigestPort.ts`'s open risk (a real browser refusing a write) is
  still unaddressed and still deferred to whichever round first meets it.
