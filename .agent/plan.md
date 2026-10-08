# Plan — F304 Machine client contract v1.1, part two: what a client can rely on

## Goal
A client's real paths work through the command line and are written down: an order runs in the
repository of the project it names, a refused apply says so, a result can be declined, an order of
several jobs and an order started twice behave, a program sees what changed and what it cost, and
the digest stays small (docs/roadmap/features/T12_F304.md, T002 to T007, carried from F298).

## Current Step
Session 5, round 24, the closing round: book round 23, rotate the finding ledger, flip F304's
STATUS line to accepted with the README sync and the self-use item SU-049's `consumed_by`, and
open the pull request, left unmerged.

## Next Steps
1. The next session: Phase 1 rule 1, then the Open PR Gate merges F304's pull request (a red
   hosted check is read, registered and re-run once first, per amend0929-context-hygiene), then
   the next feature's first commit books round 24's verdict, then Rule A5 claims the next
   unchecked line, F253 — Headless API contract.

## Risks
- A selector that names no single project still fails in the init step instead of before any step
  (DECISION F268 D16 (4), kept by DECISION F304 D2).
- The operator's own data root holds 13,481 open decisions, so its digest stays about 10 MB
  under the window (DECISION F304 D16).
- F304 owns no open finding. R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157,
  R-1158, R-1162, R-1172, R-1176 (Low) stay open, owned by F297.
