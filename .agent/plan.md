# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 3, round 12.

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
| T002 the storage edge (dismissal + last-seen) | done | this round |
| T002 the mount, the data load and the layout | open | next |
| T003 CLI parity and the end-to-end | open | |

## Next Steps
1. This round extends `DigestVisibilityPort` (DECISION F040 D8) with the two
   last-seen methods D8 already names but no round had yet added, and builds
   the browser-local storage edge implementing all four — dismissal and
   last-seen, both keyed per job — pinned by a real vitest guard with a
   worktree mutation red-proof (the F256 D6 route R11 already used).
2. The next round MOUNTS the card into `RemedyShell.tsx`: `loadJobDigest`
   (paired with `jobDigestPath`, following `loadDiffEnvelope`'s shape in
   `remedyApi.ts` — `jobDigest.ts` itself may keep no fetch, per its own
   header), `latestActivityMs` read from the brain stream's `recent` ring
   buffer via `newestActionRow(...).receivedAtMs`, a real `window`-bound
   instance of this round's storage edge, and the card mounted as a sibling
   of the shell div rather than inside `<main>`, which
   `tests/ui_contracts/test_main_layout_guard.py` pins to exactly four
   children. `onOpenDecisions` and `onPrimaryAction` render but stay inert
   that round too: `JobDigestPrimaryAction` carries only `label` and
   `rule_id`, no task or decision id to focus, so wiring DECISION F040 D5's
   "in-page action using the focus mechanism F021 shipped for feed rows"
   needs its own resolution design and its own round.
3. Then T003's `remedy job digest`, the end-to-end, the integration gate and
   closure.

## Risks
- R-0570, R-0752 and R-0755 stay OPEN and are routed to the paydown branch;
  none is F040's to fix. R-0753 stays OPEN as this feature's documented risk.
- R-0756 is RESOLVED this round (RECORD12): R11 built and proved the fix,
  and this round's append is where the append-only ledger records it.
- `browserDigestPort.ts` is this repository's first localStorage-backed
  module; a real browser can refuse a write (private mode, quota) and this
  round does not guard that case — no shipped sibling establishes how this
  codebase wants a storage failure to degrade, so it is left to whichever
  round first meets it in practice rather than guessed here.