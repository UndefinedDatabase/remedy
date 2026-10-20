# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q21 — What the insight cannot see (2026-10-21, F311, round 1)

**What needs deciding.** Remedy is getting two new answers for the Orb: one that lists what runs
right now, and one that looks into a single job's worker and says why it hangs. Remedy can only
report what it can measure, so I made four choices. The worker's latest lines and the time of its
last output are recorded only for the local worker that runs your lab model, not yet for the paid
command-line worker, so a job on that worker says plainly that its silence is not measured. Remedy
has no fixed number of worker slots, so the number of free workers reads empty. The local model
server never tells anyone how many requests wait, so that number reads empty too. And the two
commands are named after the other client reads, as "remedy client now" and "remedy client
insight", rather than "remedy now" and "remedy job insight".

**Why it matters.** The Orb will show an empty value or the word for "not measured" in these
places, instead of a number. If the paid worker matters to you in the lab, it needs a later step.

**My recommendation.** Keep all four choices. An honest empty value is better than a guess, and
the local worker is the one your lab runs use.

**What happens if you say nothing.** The recommendation is already executed and stands until you
say otherwise.
