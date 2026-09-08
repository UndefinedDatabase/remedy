# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 8 books round 7's PASS, registers R-0841 and R-0842, and deletes the THIRD module group,
`context_pack` — the module, its handler, its catalog entry, the brain-graph node that read its
event by NAME rather than by import, that node's detail renderer and its viewer, theme, copy and
edge-humanization entries, two dead `ui_server.py` readers, three smoke-script sections with
their guards, the surviving test call sites, one ist-doc section and its map lines. DECISION
F275 D4 rules that an event-coupled consumer dies in the same commit as the emitter that fed it.

## Next Steps

1. `review_bundle`, which this round's regeneration makes the order file's first line: 2254
   lines, sixteen surviving test importers, eight `docs/system/` pages, a `pyproject.toml`
   per-file ignore and list entry, and `scripts/remedy_test_runtime.sh`. It needs a session
   that can carry it whole, and DECISION F275 D3 keeps it deferred until one can.
2. The remaining components in the recorded order, the multi-module ones as single commits
   because their members import each other.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831,
   R-0840 and R-0842 named among the ideas deleted rather than inherited.
4. T002, the atomic record flip, alone, because every later commit's size depends on its ruling.

## Risks

- The open set is 66 by distinct id at this round's base `65409e64`; the ledger commit this
  block fixes as C2 registers R-0841 and R-0842 and takes it to 68. Four are High — R-0803,
  R-0804, R-0806 and R-0807 — all F273's rather than this feature's, per DECISION F272 D12.
- R-0832 records that the map measures IMPORT edges only. This is the first group whose
  surviving readers are coupled ONLY by event name, and an AST importer sweep saw none of
  them; they were found by reading the emitter's event string back out of the tree.
- The full suite is run SERIALLY. Under `pytest -n auto` the `ui_server` command-channel tests
  race for a server port and the vitest node needs `apps/ui/node_modules`.
