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

### Q4 — Whether `propose` may stay a real command (2026-09-16, F280, round 7)

What needs deciding. The vocabulary cleanup's master list marks the command group that lets an operator review and approve a suggested next task for deletion. Looking at the actual code, I found that deleting it would leave two other features stuck with no way forward: the self-drive execution command would permanently refuse to run any task it hasn't been told is approved, and a job's build and finalize steps would stay stuck at pending forever once even one suggestion exists for it, because nothing else in the running system ever marks a suggestion resolved. A job accumulates one of these suggestions automatically every time a task finishes successfully, so this is not a rare edge case.

Why it matters. If I delete the group to satisfy the cleanup list, every job that finishes a task afterward gets permanently stuck unable to reach done, with no command-line way out. If I instead keep the whole group alive to avoid that, the vocabulary cleanup's own finish line — every word on its retirement list is actually gone — stays unmet, and two already-written acceptance criteria for this feature go permanently unsatisfiable without a further change to them.

My recommendation. Keep the review-and-approve part of the group alive under a different name attached to an existing surviving word, rather than deleting it outright or leaving it exactly as it is. That satisfies both concerns: the old top-level word disappears as the cleanup intends, and the two stuck safety gates keep a real, reachable way to be resolved. Building that replacement command and choosing its exact name is more design work than a naming decision, so I have not built it without your sign-off.

What happens if you say nothing. I will leave the group exactly as it is today, unresolved, and move on to other work this session can still finish; the two acceptance criteria that assume its deletion stay open, and the next session picks this back up.
