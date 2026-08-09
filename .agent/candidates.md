# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

- Worker-authored `Done:` resolution text preceded the reviewer's. In F104 R7 the
  worker wrote its own `Done: R-0227` paragraph into `.agent/live_review.md`
  (commit 103a854d) although the round's block explicitly deferred that text to
  the reviewer. It was hedged honestly — it ended "Awaiting reviewer verification"
  and the handback said the Resolved text was the reviewer's to author — and the
  F104 R8 closure replaced it with the reviewer's authored text, so no false
  Resolved reached the accepted state. The residual risk is what the disk would
  have carried had the session died between R7 and R8: a worker-authored `Done:`
  paragraph that a later reader could mistake for a reviewer resolution, which is
  the R-0223 class one level up. Candidate for a rule sharpening in
  docs/agents/planner_reviewer_prompt.md §4.4 — e.g. workers mark a fix landed
  with a distinct token that is not `Done:` — rather than for a code fix.
  · source feature: F104 · date: 2026-08-09

The two F103 candidates were swept at the F104 R1 candidate sweep, which is
the first reviewed round after the F103 closure: the UI auto-build test is
registered as R-0221 in `.agent/live_review.md` as a documented Low risk
routed to the F252 flake-debt class, and the commit-size counting ambiguity
is resolved inline as DECISION F104 D1 and applied to AGENTS.md Commit
Discipline. Neither was dropped.

> Recorded AFTER the F104 closure commit, which deviates from Rule A4 (the STATUS
> edit is normally the last commit on the branch). The reviewer chose the deviation
> deliberately: the candidate surfaced while reviewing the closure commit itself,
> and the disk-vehicle rule exists because a brief-only candidate gets lost. The
> accepted HEAD (68a7412019e92232a880625b7fce4e48c7198744) and the review package
> both predate this commit and are unaffected.
