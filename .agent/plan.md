# Plan — F281 CLI help surface

Branch: feature/f281-cli-help-surface, cut from `main` at
`c617dd74df26b8e677161b265a88d5926f4d78ab`, the merge commit of pull request
253 (F280's closure).

## Goal

Every catalog description, role label and help page reads as the finished
vocabulary of DECISION amend0905-vocab D4 (`docs/roadmap/features/T2_F281.md`).
DONE when T001 and the Acceptance list hold.

## Current Step

ROUND 14. C1 books round 13's PASS and adds DECISION F281 D3 (exempts the
two structurally-unreachable synonym offenders by name; flips
`VOCABULARY_MODE` to `"enforced"`). C2 rewords `stats.bench`'s description
and lands the `SYNONYM_EXEMPTIONS` mechanism plus the mode flip in
`tests/docs/test_vocabulary.py`. After this round:
`_meaning_violations() == []`, `_synonym_offenders() == []`, both
mode-dependent tests assert the enforced-mode branch and pass.

## Next Steps

1. T001's remaining Acceptance items (group order, `doctor core`'s
   dead-commands section, the 200-char help wrap, the README quickstart,
   R-0805, R-0809, R-0934) are UNVERIFIED by this round — a quick grep found
   nothing conclusive either way. Re-read `docs/roadmap/features/T2_F281.md`'s
   Acceptance list fresh at round 15's claim; do not assume any one item is
   done or not from this note.
2. Session 2 of F281 is 6 delegated rounds in (rounds 9-14) after this round,
   at the low end of the 6-to-8 target (amend0905-throughput). A further
   round or two stays in scope; end the session on demonstrably exhausted
   context, not at a nice seam.

## Risks

- Each remaining Acceptance item is its own measurement against the real
  catalog/CLI output; do not batch more than one per round without a fresh
  dry run, per the discipline DECISION F281 D3 followed.
