# Context — operator amendment amend0929-context-hygiene

## Active Branch
feature/amend0929-context-hygiene, cut from `main` at `4e643440`.

## Scope
The operator amendment amend0929-context-hygiene, Parts A to G: the ledger
diet, the red-CI rule, stale staging copies, checkout hygiene, Q6 and the
F291 registration.

## Do not touch
F042's product code on `feature/f042-multi-project-cockpit`; its handoff,
plan and ledger records are carried, never rewritten.

## Active assumptions
- A staging copy under `.data` is derived scratch, never a record.
- Finding ids continue from R-1112 (the F042 branch holds R-1111).
