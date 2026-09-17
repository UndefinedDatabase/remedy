# Closure Candidates — carrier of record

> Written per docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate
> findings", disk-vehicle rule, operator ruling 2026-08-01). Read at Window-1
> session bootstrap (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present at
> feature-claim time is a block condition.

CANDIDATE (2026-09-17, F280 round 26 C1) — `.agent/authored/f280-r26.md`, the block-save copy round 26's own C1 made of the paste block this round applied, is 211 bytes shorter than the reviewer's own authored original: it is missing the block's final closing separator line (the `──...──` rule this repository's convention puts at the end of every paste block), confirmed by direct byte comparison against the reviewer's own scratch copy of the block. `.agent/last_block.md` is byte-identical to the truncated `.agent/authored/f280-r26.md`, so both carriers share the same gap. Every PAYLOAD the block ordered (RECORD26, FINDING953, PLAN26, DONE953, TEST26) is independently verified byte-for-byte correct — against the reviewer's own originals and against the files each was applied to — so this gap is confined to the closing decorative line of the saved block copy itself, which carries no constraint, gate or payload text of its own; nothing the round certified is wrong. Source feature: F280. Suggested repair: the next round that saves a block under `.agent/authored/` on any feature registers this as an R-id and checks whether the worker's block-save step is silently dropping trailing content in general, which would be worth catching before it ever drops something load-bearing rather than decorative.

The entry F275's closure gate recorded on 2026-09-14 — the self-use runner hands `run_job`
the role config's provider names but not its model names — was registered in F261 round 1 as
finding `R-0890` in `.agent/live_review.md`; the measurement and the routing are on that
record.

The entries F109's closure gate recorded on 2026-09-03 were discharged in F110
round 1 without spending an R-id, which is what operator amendment
amend0827-process-diet rule 2 requires of a reviewer-prose inaccuracy that left
nothing wrong on disk. The entry naming the §3 checklist consolidation pass F109
owed and never performed is resolved inline as DECISION F110 D1 in
`.agent/decisions.md`, which carries that pass into F110's own closure sequence
against the ceiling amend0827 rule 4 names. The remaining entries — the lessons
rounds 8 through 21 promised `.agent/prose_slips.md` and never wrote, the round
21 block's closure path set naming a file it left nothing to write, and that
block's vacuous U+2014 gate clause — are appended to `.agent/prose_slips.md` as
dated lines in that same round. The on-disk defect underlying the vacuous clause
was already registered as `R-0785`, and no second id was minted for it, per
docs/agents/planner_reviewer_prompt.md §3 item 30.

The entry F108's closure round recorded on 2026-09-02 — `README.md` carries
F106's capability paragraph twice, the second copy misplaced under "Accepted
in Tier 5 so far" — was registered in F109 round 1 as finding `R-0769` in
`.agent/live_review.md`; the reason, the measurement and the routing are on
that record. The entry recorded after F106's closure (job/mission
resume-from-persisted-state, DECISION F106 D2) was registered in F108 round 1
as finding `R-0762` on the same record.
