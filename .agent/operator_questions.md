# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q9 — Client contract feature split early (2026-10-08, F298, round 21)

**What needs deciding.** The feature that makes Remedy's promises to a program true and written
down had seven parts. The first part is finished: Remedy now describes itself to a program from its
own code, with every command, option, answer field, state word, refusal word and exit code, and the
page a person reads ends with that same description, written by Remedy and checked by tests. The
other six parts are still open: an order runs in the repository of the project it names, a refused
apply says so, a result can be declined, an order of several jobs and an order started twice
behave, a program sees what changed and what it cost, and the overview stays small. The feature
has used twenty of its twenty-five working rounds. I split it now: this feature closes with the
first part, and the six open parts move unchanged into a new feature placed directly after it and
before the feature that serves Remedy over HTTP.

**Why it matters.** At the slow pace you asked for, the first part alone took twenty rounds, and
closing a feature now needs a careful audit and several rounds of its own. Starting the second part
would have run past the limit in the middle of that part, with nothing finished to close. The six
open parts are still the next work: the new feature comes before the HTTP feature, so nothing
starts ahead of them. The program you are building as Remedy's first client still cannot rely on
those six parts until the new feature is done.

**My recommendation.** Keep the split. The first part is finished and tested, so it is a clean point
to close, and the new feature carries the rest word for word, so nothing is lost or re-planned.

**What happens if you say nothing.** The recommendation is already executed and stands until you
say otherwise: this feature goes through its audit and closure with the first part, and then the
new feature starts with the second part.
