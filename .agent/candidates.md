# Closure Candidates — carrier of record

> Written per docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate
> findings", disk-vehicle rule, operator ruling 2026-08-01). Read at Window-1
> session bootstrap (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present at
> feature-claim time is a block condition.

- THE SELF-USE RUNNER HANDS `run_job` THE ROLE CONFIG'S PROVIDER NAMES BUT NOT ITS MODEL NAMES. In F275 round 107's run of `SU-014`, recorded under `.agent/selfuse_f275/`, `resolve_role_config` named provider `ollama` and model `muse-glimmer:latest` for both the builder and the reviewer, while the job's `execution_config` records `builder_model=''` and `reviewer_model=''`, each with source `default`; so a closure's self-use run may not run the model its role config names. Raised at the closure review of F275 from the worker's declared observation, not yet searched against the open set under §3 item 30 and not measured beyond that record. · F275 · 2026-09-14

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
