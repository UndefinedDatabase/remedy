# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

The carrier is empty. F255's closure review produced NO candidate: every defect
this feature surfaced was registered as a numbered finding during the round that
found it, which is what the closure-candidate mechanism exists to avoid needing.
Four of those findings are OPEN at closure and none is a code defect — R-0607,
R-0608, R-0609 and R-0611 are all defects in the reviewer's own block text, and
their fixes edit `docs/agents/planner_reviewer_prompt.md` or
`docs/roadmap/STATUS_closure_protocol.md`, paths the closure commit's R-0154 path
set cannot reach. They route to a paydown branch and are named in the pull
request rather than carried here, because they are registered findings and not
candidates.
