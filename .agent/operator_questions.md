# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q11 — Four real order texts needed (2026-10-11, F297, round 1)

**What needs deciding.** On 11 October you asked for tests that use the texts of four real
orders, the ones named luna-tugwqu, luna-t9qzgu, luna-tfdvf5 and luna-t5twkd. Those texts are
kept in Remedy's data folder, and the loop's sessions are not allowed to read that folder, so the
tests were written with texts made up from your description instead. Someone who may read the
data folder has to copy the four order files into the folder that was prepared for them among the
test data of the orchestration tests, the one named after your change of that day.

**Why it matters.** The tests are meant to prove that the planner's repair works on the orders
that really failed. With made-up texts they prove it only on texts that look like those orders,
so a difference in the real texts could go unnoticed.

**My recommendation.** Copy the four files yourself, or tell the loop that it may read those four
files once. Until then the loop keeps the item open, carries it on to the next findings paydown
when this one closes, and changes nothing else.

**What happens if you say nothing.** The recommendation is already in effect and stands until you
say otherwise: the item stays open, moves to the next findings paydown, and the tests keep their
made-up texts.

### Q12 — Mission card moved to cockpit feature (2026-10-11, F297, round 1)

**What needs deciding.** Your change of 11 October recorded that the cockpit has no card for a
mission, the lasting record that each repository now has, and asked for one card per repository
with its orders and jobs. The loop judged that this is two to three rounds of work on the
cockpit's screens with a test in a real browser, which is too large for the findings paydown,
whose items must each fit one round. It moved the item to the feature that is already planned to
show missions in the cockpit: the band that shows which repository each job of a mission works
in. That feature comes right after this paydown in the list.

**Why it matters.** It decides when the mission card is built: together with that cockpit
feature, straight after this paydown, instead of inside the paydown now.

**My recommendation.** Keep the move. The cockpit feature needs the mission card to draw its band
on, so building the two together is less work than building the card first and changing it
again.

**What happens if you say nothing.** The recommendation is already carried out and stands until
you say otherwise.
