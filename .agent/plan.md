# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 7 books round 6's PASS and deletes the SECOND module group, `worker_recommend` — the
module, its handler, its two catalog entries, the two smoke-script steps that drove them and
the guards asserting those steps, the surviving test call sites, and one stale sentence in an
ist-doc. DECISION F275 D3 rules that the recorded order is a valid topological order rather
than a mandated sequence, which is why this group is taken before `review_bundle`.

## Next Steps

1. `context_pack`, which this round's regeneration makes the order file's first line.
2. `review_bundle`, deferred by DECISION F275 D3 and needing a session of its own: 2254 lines,
   sixteen surviving test importers, eight `docs/system/` pages, `pyproject.toml` and a script.
3. The remaining components in the recorded order, the multi-module ones as single commits
   because their members import each other.
4. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831
   and R-0840 named among the ideas deleted rather than inherited.
5. T002, the atomic record flip, alone, because every later commit's size depends on its ruling.

## Risks

- 66 findings are open by distinct id, four of them High — R-0803, R-0804, R-0806 and R-0807 —
  all F273's rather than this feature's, per DECISION F272 D12.
- R-0832 records that the map measures IMPORT edges only. Rounds 6 and 7 both measured that
  gap for real: a UI catalog pinned to the Python emitters, and a smoke script plus its guards
  that drive a command by STRING. An AST importer sweep is necessary and not sufficient.
- The full suite is run SERIALLY. Under `pytest -n auto` the `ui_server` command-channel tests
  race for a server port and the vitest node needs `apps/ui/node_modules`; round 7 measured 12
  such failures in parallel and 0 in the same worktree run serially.
