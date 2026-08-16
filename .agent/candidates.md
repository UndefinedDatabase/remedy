# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

The carrier is empty at the time F083's closure block was authored. F083 raised no
closure candidate of its own during its rounds: everything it found was registered
as an R-id in `.agent/live_review.md` while the round that found it was still open,
which is where a finding belongs.

Two open findings are deliberately deferred rather than carried here, because they
are registered findings and not candidates: R-0482, a live `NameError` on the
refusal path of `check_injections_supported`, and R-0487, `docs/README.md` never
being link-checked. Both are code- or test-content fixes that F083's scope
forbids, and both want a paydown branch of their own.

If the reviewer's closure review of this round raises a candidate after this file
is committed, that candidate rides in the round report and in `.agent/handoff.md`,
and the next feature's first reviewed round registers it — the same path F082's
three closure candidates took to become R-0448, R-0449 and R-0450 at F083 R1.
