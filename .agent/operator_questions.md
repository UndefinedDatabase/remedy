# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q3 — Command-name cleanup split in two (2026-09-16, F261, round 25)

What needs deciding. The feature that renames and prunes Remedy's commands reached its limit of twenty-five rounds before it was finished. Under your standing default I split it: this feature now closes with what it reached, and the rest is registered as a new follow-up feature placed directly after it on the roadmap, so it is the next thing the loop picks up once this one is closed. What moved is the removal of three command families that other working commands still depend on, the changes to how the run command chooses its builder and reviewer, the rename of the plan module, and the whole final pass over help texts, role labels and the visible order of command groups. Seven open review findings go with it.

Why it matters. The command tree is not yet the one the vocabulary decision describes: some words it retires still exist, because deleting them today would break commands that stay. The roadmap now has one more feature, and it sits ahead of every other unfinished feature.

My recommendation. Keep the split. Everything the first feature did is complete and tested, nothing is half-done, and the follow-up starts from a clean state with each blocked deletion named together with the reason it waits.

What happens if you say nothing. The first feature goes through its normal closing steps, and the loop then starts the follow-up feature.
