- Resolved: R-0159 (process, Low) 2026-07-31: the dogfood branch
  guard now resolves HEAD for both repo forms — a `.git` directory
  and a linked worktree's gitfile pointer (stdlib-only, still no
  subprocess); the worktree form is pinned by
  TestCurrentBranchRepoForms (throwaway worktree in the test), and
  integration_gate.md no longer carries a non-restorable
  `.git`-directory class.
  Done: R-0159 (commit 23a06611 — fix + tests; gate-doc cleanup
  21aa8e88).
- DECISION D1 (2026-07-31, closure-candidate rule of
  STATUS_closure_protocol.md, reviewer): the carried VT run_id
  candidate is resolved inline, no ID spent — the producer-pitfall
  list now names the `^vr-\d{4,}$` run_id shape and the
  vt_passed = None failure mode (commit 408c89c9). Alternative
  considered: register as R-0160 (rejected: the doc line IS the
  entire fix; an ID would be born resolved). Reversal: any later
  relay may register the class if it recurs.
- Next free ID: R-0160.
