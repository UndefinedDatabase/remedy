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

ROUND 2. C1 books round 1's PASS, records DECISION F281 D2 (two of the six
retired-"loop"-synonym offenders — `dev.agent-loop`'s command_id and
`--fixture-builder`'s `repair-loop` value — are structurally unreachable by
this feature; the F259 enforced flip is bounded by them, not by zero), and
re-points `.agent/plan.md`. C2 rewrites 18 catalog text fields in
`apps/cli/command_catalog.py`: the full Contract/Roadmap/Plan/Worker
meaning-violation buckets (13 descriptions/help strings, 19 violations —
several descriptions carried more than one binding-word violation once
checked against every word, not only the one first measured) and the 4 of 6
"loop"-synonym offenders that are pure prose.

## Next Steps

1. `tests/docs/test_vocabulary.py` now measures 275 meaning-violations (was
   294) and 2 synonym-offenders (was 6, floor per DECISION F281 D2). The
   remaining 275 break down by binding word: Job 125 (or fewer — some Job
   violations may already have cleared as a side effect of a shared
   description; re-measure at the start of the next round rather than
   trusting this figure), Project ~65, Run, Mission, Order, Evidence, Task,
   Decision, Plan (any left outside this round's 4), Contract (any left
   outside this round's 1) — re-run `_meaning_violations()` grouped by word at
   the start of round 3 and take the next-smallest remaining bucket, the same
   pattern this round used (smallest buckets first, to build the rewrite
   pattern before the two large ones).
2. Help wrap, the `doctor core` dead-commands section (D11d), the D11a
   catalog group-reach test, the visible-order data-pinned test, the F259
   enforced flip itself (once the description buckets are clear and DECISION
   F281 D2's two-item floor is either accepted as the flip's final state or
   separately resolved), and the README quickstart's R-0895 line remain
   entirely undone.

## Risks

- Every catalog description edit is verified by re-running
  `tests/docs/test_vocabulary.py`'s own `_meaning_violations()` and
  `_synonym_offenders()` functions against the modified catalog BEFORE
  authoring, and by a full literal-string sweep for the two synonym floor
  items to confirm no round accidentally "fixes" them by editing text that
  isn't the command_id or the ArgDef value itself.
- A description rewrite that adds a binding word's own fragment can
  accidentally introduce a DIFFERENT binding word without ITS fragment (round
  2 caught this on `worker.list`/`worker.show`/`worker.doctor`/`group:worker`,
  where a first-draft rewrite added a bare "run" verb, tripping the `Run`
  check it hadn't tripped before); every rewrite in this feature is checked
  against the FULL violation diff (fixed vs. introduced), never just the one
  word it targeted.
