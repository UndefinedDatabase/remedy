# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 5, round 22 — OPEN PR GATE CONFLICT
RESOLUTION.

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
| STATUS line + README sync + PR | done | round 20, PR #225 opened |
| PR #225 vs main drift (F258 landed via #223/#224) | resolved | round 22, merge commit `f69f1785` |

F040's build is DONE. Nothing in this feature's own content changed this
round — round 22 only resolved a merge conflict caused by F258's
registration (PRs #223/#224) landing on `main` after PR #225 opened,
touching the same shared count lines in README.md and
docs/roadmap/STATUS.md.

## Next Steps
1. PR #225 is still OPEN and UNMERGED. It must be merged at the next
   session's Open PR Gate (self_drive_protocol.md G1) before any new
   feature work is claimed on this repo — never in the same
   round/session that touches this branch.
2. No further edits to this branch are expected before that merge. If
   `main` drifts again before the merge, re-run this same conflict
   resolution process against the newly conflicting lines only.
3. Wiring `onOpenDecisions`/`onPrimaryAction` for real needs its own
   resolution design (D5's "in-page action") and is not yet scheduled —
   documented in the Built State section, carried forward as a known
   post-closure item, not a blocker.

## Risks
- R-0570, R-0752 and R-0755 stay OPEN and are routed to the paydown branch;
  none is F040's to fix. R-0753 stays OPEN as this feature's documented risk.
- `browserDigestPort.ts`'s open risk (a real browser refusing a write) is
  still unaddressed and still deferred to whichever round first meets it.
