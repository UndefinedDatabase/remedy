# F310 round 4 — amendment 1 (reviewer, after the worker's stop before C4)

The worker stopped before C4, correctly: `list_decisions` answers `[]` for every cancelled job
(exec-1017c, "A cancelled job asks nothing"), and an `abandon` cancels the job, while
`raise_contract_remainder_decision` attaches the remainder decision to the mission's latest linked
job, which is that same cancelled job. So the remainder decision DECISION F310 D6 raises at an
`abandon` is written and then hidden from every list a person or a client reads. The same was true
before this feature: a remainder raised at the stop was hidden as soon as the stop was abandoned.
That is finding R-1374, registered by this amendment and owned by F310.

1. A new commit C3b goes between C3 and C4, subject
   `F310 R4 C3b: a cancelled job still asks its mission's remainder question (R-1374)`, paths
   `packages/orchestration/decision_queue.py`, `.agent/live_review.md`, `.agent/decisions.md` and
   `.agent/authored/f310-r4-amend1.md` (a Python byte copy of `.remedy-wt/f310-r4/prep/amend1.md`).
2. In `list_decisions`, the eight lines from the comment line beginning
   `    # THE EMIT GATE (DECISION F032 D1): this derivation point is the one seam` through
   `    return [] if str(getattr(job, "state", "")) == "cancelled" else decisions   # exec-1017c, job_cancel.py`
   become exactly these eight, so the function's length does not change:
   ```
       # THE EMIT GATE (DECISION F032 D1): the one seam every producer funnels through, where an enforced type is
       # refused for arriving without its receipts; it enforces only `TRIPLE_REQUIRED_TYPES`, which holds `token_budget`
       # since the budget stop got a real triple, and each other producer joins in its own upgrade commit.
       enforce_decision_evidence(decisions)
       from packages.orchestration.mission_contract import CONTRACT_REMAINDER_MARKER
       if str(getattr(job, "state", "")) == "cancelled":   # exec-1017c; DECISION F310 D6: only its mission's remainder
           return [d for d in decisions if str(d.payload.get("question", "")).startswith(CONTRACT_REMAINDER_MARKER)]
       return decisions
   ```
3. Append to `.agent/live_review.md` the bytes of `src-r1374.md`, and to `.agent/decisions.md` the
   bytes of `src-d6-addendum.md`, each as they are; nothing else in either file changes.
4. C4 then asserts through `decision list` and `list_decisions` as the block orders, and gains one
   test in `tests/orchestration/test_budget_stop.py`: a cancelled job whose escalations hold an open
   remainder decision and an open decision of another kind lists exactly the remainder decision.
5. Gate 5 then reads 89 (R-1373 and R-1374 open until the reviewer's resolution). `verify.py` now
   checks C3b; its new sha256 is in the reviewer's message. Every other part of the block stands.
