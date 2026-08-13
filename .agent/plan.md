# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after PR
#194 merged. Last reviewed SHA: 7bc57cd1. R21's verdict is PASS; the
integration gate is green. Next free finding ID: R-0343 (still unspent). Open
findings: 14 — R-0320, R-0322/23/24, R-0327/28, R-0331, R-0333/34, R-0336/37,
R-0339, R-0341/42 — all Medium/Low. No PR exists.

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE tokens go
— by segment kind, by role, by task class — plus a cost curve and a
prior-period comparison, as markdown and json, every number traceable to a
ledger row, missing data reported as missing (docs/roadmap/features/T2_F115.md).

## Current Step
R25 landed the Built State: ITEM B verified claim by claim (30 claims, all
TRUE) and committed at 0fc9c051, byte-identical to the authored text. Closure
precondition 4 is now met.

R25 HALTED at ITEM A on stop-on-false-claim. R-0343's text says: "R24's block
ordered `git stash list` non-empty as a closure gate". FALSE. That block
(.agent/authored/f115-r24-1.md) already carries the CORRECTED gate, at its
amendment 2 and its done-when (e). The block that ordered the unfailable one is
R23's (f115-r23-1.md:131, "git stash list non-empty"), inherited from R22's
ITEM 5 step 2; the R23 worker found it and the reviewer fixed it in R24 — which
is what R-0343's own R24 draft says ("it is fixed in R24").

ITEMs 3-7 blocked as a consequence: ITEM 6 (c) must write "open findings 15 …
R-0343 … next free ID R-0344", and closure precondition 1 requires every
R-XXXX to be registered. With R-0343 unregistered both would be false, and the
closure commit must be the LAST commit — so it cannot precede ITEM A.

## Next Steps
1. Reviewer re-authors R-0343 with the stash-gate attribution corrected (R22/
   R23 ordered it, the R23 worker found it, R24 fixed it), and re-orders the
   closure from ITEM A. ITEM B is DONE — do not re-order it.
2. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, a FRESH
   review zip, the authored STATUS line committed last, then the PR.

## Risks
- The work tree carries ` M scripts/make_review_zip.sh`, made by no agent of
  this session. DECISION F115 D7 leaves it untouched until closure stashes it.
- The repo already carries five unrelated stashes, so a "stash list non-empty"
  gate cannot fail; the closure gate must match the new entry's message.
- Four rounds now lost to reviewer-authored claims the disk refutes. The
  narrowed inventory shape fixed ITEM B; ITEM A still carries prose about
  which ROUND did what, and that is the coordinate class all over again.

Fortschritt: 99 % (T001 ✅ · T002 ✅ · T003 ✅ · Integration-Gate ✅ · Built State ✅ — Closure offen) — gemessen
