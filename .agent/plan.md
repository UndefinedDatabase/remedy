# Plan — F281 CLI help surface

Branch: feature/f281-cli-help-surface, cut from `main` at
`c617dd74df26b8e677161b265a88d5926f4d78ab`, the merge commit of pull request
253 (F280's closure).

## Goal

Every catalog description, role label and help page reads as the finished
vocabulary of DECISION amend0905-vocab D4 (`docs/roadmap/features/T2_F281.md`).
DONE when T001 and the Acceptance list hold.

## Current Step

ROUND 15. C1 books round 14's PASS. C2 fixes `apps/cli/help_renderer.py`'s
`_box()`: long right-column text now WRAPS across continuation lines instead
of being truncated with an ellipsis (DECISION F281 D4), clearing the
Acceptance line "A 200-character option help renders without `…`." Three new
tests in `tests/test_help_renderer.py` sweep the real catalog (root help,
every group, every command) for zero ellipsis.

## Next Steps

1. Remaining Acceptance items, freshly re-measured this round: the D4 visible
   group order test does not exist yet; `doctor core`'s dead-commands section
   does not exist (design item (c) of DECISION amend0905-vocab D11,
   `T2_F271.md` T002 — check the scope-overlap risk below before authoring);
   R-0805, R-0809, R-0895 and R-0934 are all still OPEN; the README quickstart
   is unchanged. Re-measure fresh at round 16's claim rather than trusting
   this line.
2. Session 2 of F281 is 7 delegated rounds in (rounds 9-15), at the top of
   the 6-to-8 target (amend0905-throughput). End this session after round 15
   on demonstrably sufficient progress, or continue if context comfortably
   suffices.

## Risks

- The `doctor core` dead-commands section appears in BOTH this feature's own
  Acceptance list and F271's (`T2_F271.md` T002, design item (c)) — F271 runs
  AFTER F281 in STATUS order. Read both files fresh before claiming that item;
  do not implement the same mechanism twice.
