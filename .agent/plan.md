# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 4, round 17.

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
| the integration gate | in progress | this round |
| closure sequence | open | next, if the gate is clean |

## Next Steps
1. This round runs docs/agents/integration_gate.md steps 1-4: branch run,
   base run at the merge base `f5b1e6c5` in a throwaway worktree, the
   `comm` comparison, and per-id attribution for every branch-only failure.
   Evidence lands under `.agent/gate_f040_r17/`. Per the gate's own rule,
   ONLY THE REVIEWER ISSUES THE VERDICT — this round reports raw evidence
   and classifications, and the next round's review carries the verdict.
2. If the gate is clean (or every branch-only id is attributed to the known
   xdist-flake or environment-parity classes), the next round starts the
   closure sequence (STATUS_closure_protocol.md): evidence job, a fresh
   review zip, the STATUS line, the PR.
3. If a branch-only failure is coupled to feature code, that is a BLOCKER
   per the gate's own rule: STOP and hand back rather than repairing it in
   the same round, per docs/agents/integration_gate.md step 4.
4. Wiring `onOpenDecisions`/`onPrimaryAction` for real needs its own
   resolution design (D5's "in-page action") and is not yet scheduled.

## Risks
- R-0570, R-0752 and R-0755 stay OPEN and are routed to the paydown branch;
  none is F040's to fix. R-0753 stays OPEN as this feature's documented risk.
- `browserDigestPort.ts`'s open risk (a real browser refusing a write) is
  still unaddressed and still deferred to whichever round first meets it.
