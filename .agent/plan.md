# Plan — F281 CLI help surface

Branch: feature/f281-cli-help-surface, cut from `main` at
`c617dd74df26b8e677161b265a88d5926f4d78ab`, the merge commit of pull request
253 (F280's closure).

## Goal

Every catalog description, role label and help page reads as the finished
vocabulary of DECISION amend0905-vocab D4 (`docs/roadmap/features/T2_F281.md`).
DONE when T001 and the Acceptance list hold.

## Current Step

ROUND 16. C1 books round 15's PASS, registers and resolves R-0955 (the
default `remedy --help` order did not match D4, and the canary's own pinning
test never caught it), and adds DECISION F281 D5. C2 lands
`VISIBLE_GROUP_ORDER` in `apps/cli/command_catalog.py`, points
`_print_root_help` at it, and replaces the stale canary assertion with one
that pins the full D4 order; two new tests pin the tuple's own content and
completeness. After this round: `remedy --help` prints the sixteen visible
groups in exactly D4's order.

## Next Steps

1. Remaining Acceptance items, freshly re-measured this round: `doctor
   core`'s dead-commands section does not exist yet — it duplicates F271's
   own design item (c) (`T2_F271.md` T002), which also wires it into the
   closure protocol as precondition 7 and adds a fixture-based red-proof
   test; F271 runs AFTER F281. Read `T2_F271.md`'s full Design section before
   the round that claims this item, and scope F281's delivery to exactly its
   own Acceptance wording ("lists dead commands as a section... empty") so
   F271 can layer the closure-precondition wiring and fixture test on top
   without redoing the mechanism. R-0805, R-0809, R-0895 and R-0934 are all
   still OPEN. The README quickstart is unchanged (orchestrator brief:
   last, because it quotes the finished catalog).
2. Session 2 of F281 is 8 delegated rounds in (rounds 9-16), at the top of
   the 6-to-8 target (amend0905-throughput). Continuing is allowed while
   context comfortably suffices; ending here is also a clean stop, not an
   early one.

## Risks

- The `doctor core` dead-commands section needs its own design pass (what
  "referenced by no test and no script" means, mechanically, for a
  command_id) before a round claims it — do not rush a heuristic
  implementation; F271's fuller design (T2_F271.md) is the reference.
