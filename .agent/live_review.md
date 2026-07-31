# Live Review — Paydown micro-round 2026-07-31 (F052→F053 boundary)

Branch: feature/paydown-0731
Scope: codify the digest fallback for transport proofs and the
practice-requires-pointer rule (planner_reviewer_prompt.md); resolve
the carried VT run_id closure candidate (STATUS_closure_protocol.md);
fix R-0159 (worktree-safe dogfood branch guard) + gate-doc cleanup.
Same-session merge on PASS (standing operator approval, 2026-07-31).

## Steps
- R1: Open PR Gate (#167) → Items 1–3 + candidate pass → gates
  (tests/docs + canary + touched test files) → handback.

## Findings
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

## Verdicts
- R1: PASS (reviewer, 2026-07-31). Range b63f9665..168f9890. All 9
  authored texts cmp 0 disk-to-disk against the reviewer scratchpad
  originals; every payload verified exactly once at its anchor in
  the committed files (python count proof). Reviewer's own gate
  runs: tests/docs 293, canary 42, touched test files 30 (24 unit +
  6 CLI). R-0159 repro killed in a throwaway linked worktree at
  HEAD on a branch (.git gitfile → 6/6 CLI ids green); negative
  control: a DETACHED worktree still fails the 2 guard-dependent
  ids — the guard refuses detached HEAD as before, so the fix is
  additive and default-preserving. Worktree removed + pruned.
  Ledger: R-0159 Resolved (23a06611 + 21aa8e88), VT run_id
  candidate resolved inline as DECISION D1 (408c89c9), no ID spent,
  next free ID R-0160. Merge same-session per standing operator
  approval (2026-07-31). LAST_REVIEWED_SHA = 168f9890.
