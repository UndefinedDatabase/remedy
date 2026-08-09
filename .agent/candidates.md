# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

**No open candidates.**

Swept at the F105 R1 candidate sweep — the first reviewed round after the F104
closure. Both entries were RESOLVED rather than carried, because both asked for
the same kind of thing: one process rule written down once in
docs/agents/planner_reviewer_prompt.md.

- Worker-authored `Done:` text preceding the reviewer's · source feature: F104 ·
  date: 2026-08-09 — resolved as §4.4: a worker marks a landed fix
  `Landed: R-XXXX`, never `Done:`, which stays reserved for reviewer-authored
  resolution text. The F104 R7 instance was hedged honestly and was replaced by
  the reviewer's text at R8, so no false Resolved ever reached an accepted state;
  the rule closes the window in which a dead session would have left one.
- The last round of a branch has no on-disk gate entry · source feature: F104 ·
  date: 2026-08-09 — resolved as §4.13: that absence is the terminator, so the
  closing round's verdict lives in `.agent/handoff.md`, the completion report and
  the PR, and no repair round is opened to close it. F104 spent R10 and R11
  discovering this; no branch should have to discover it again.

The two F103 candidates were swept earlier, at the F104 R1 candidate sweep: the
UI auto-build test is registered as R-0221, a documented Low risk routed to the
F252 flake-debt class, and the commit-size counting ambiguity was resolved inline
as DECISION F104 D1 and applied to AGENTS.md Commit Discipline. Neither was
dropped.
