# Context — F311 The insight: what runs now, what the worker does, why it hangs

## Active Branch
`feature/f311-insight` from `main` at `321f130f0` (the merge commit of pull request 370).

## Scope
F311's four slices T001 to T004 as `.agent/plan.md` orders them. F311 owns no open finding at its
claim. Steps outside the feature file's slices are out of scope.

## Assumptions
- The worker pulse is written only by Pi calls; jobs of other providers answer with null worker
  fields and the stall reason `unmeasured` (DECISIONs F311 D2 and D3).
- The public API's version stays `1.21`; F313 raises it.

## Constraints
- One full pytest suite per feature, in the closure's integration-gate round; every round runs
  its own selection once (operator amendments amend0917-throughput and amend0930-test-load).
- The structure ratchet: no listed function or file grows; new logic goes into new modules.
- Do not touch: the redaction of `stream_evidence.py`, the story's five steps and their words,
  and the public API's version.
