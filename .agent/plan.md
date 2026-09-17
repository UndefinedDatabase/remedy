# Plan — F281 CLI help surface

Branch: feature/f281-cli-help-surface, cut from `main` at
`c617dd74df26b8e677161b265a88d5926f4d78ab`, the merge commit of pull request 253
(F280's closure).

## Goal

Every catalog description, role label and help page reads as the finished
vocabulary of DECISION amend0905-vocab D4 once F280 has pruned and renamed the
command tree (`docs/roadmap/features/T2_F281.md`). DONE when T001 and the
Acceptance list hold.

## Current Step

ROUND 1. C1 books F280 round 26's PASS (its last, unbooked round), registers
R-0954 (the block-save transport gap F280 round 26 raised as a closure
candidate) with Owner F273, empties `.agent/candidates.md`, and records DECISION
F281 D1 (the scope boundary for the `Worker:` → role-label rename — which of the
several "Worker" sites this feature's T001 touches and which it does not). C2
claims F281 on the STATUS line and re-points the context file. C3 lands the
first slice of T001, "role labels" (the orchestrator brief's own first item):
`Worker:` → `Builder:` at the three production report-renderer sites DECISION
F281 D1 names, with their two test assertions.

## Next Steps

1. The remaining slices of T001, in the orchestrator brief's order: descriptions
   (175 catalog strings; 294 measured `_meaning_violations()` plus 6
   `_synonym_offenders()` per `tests/docs/test_vocabulary.py`), help wrap, the
   `doctor core` dead-commands section (D11d, unbuilt), the D11a catalog
   group-reach test (unbuilt — `GroupDef` has no `feature`/`reach` field today),
   the visible-order data-pinned test (D4/amend0911-feedback D1's eighteen-slot
   order — no test pins it today), the F259 `VOCABULARY_MODE` flip to
   `enforced`, and the README quickstart's one surviving broken line (R-0895's
   `job create --plan plan.yaml`).
2. One open scope question the next round should read before touching
   descriptions: D11a's catalog test (per DECISION amend0905-vocab D11) and the
   F259 enforced-mode scan (per DECISION F259 D3) both read a command's
   `command_id`, and `dev.agent-loop`'s own command_id contains the retired
   word "loop" — but `docs/roadmap/features/T2_F281.md`'s Do-not-touch clause
   forbids this feature changing any command id. The `enforced` flip may not be
   reachable without either a DECISION narrowing the synonym scan's fields or a
   ruling that `dev.agent-loop` is out of scope for that check specifically.

## Risks

- The Worker→Builder rename does not change any gate's pass/fail on its own:
  DECISION F259 D3 scopes the vocabulary test's enforced-mode scan away from
  `Worker:` entirely (comment at `tests/docs/test_vocabulary.py:44-50`), so this
  slice is verified by its own targeted tests and mutation red-proof, not by
  that suite.
