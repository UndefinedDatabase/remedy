# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q1 — narrow vocabulary check's synonym scope (2026-09-17, F281, round 14)

Two pieces of command-line help text carry the word "loop" — a word otherwise retired from the vocabulary because it conflicts with the binding term "Mission." One appears in the description of a command that is itself named as a result of another feature's renaming work, so renaming this piece of text would rename a command people already type. The other describes what a command-line flag accepts, and that accepted value is asserted as a literal in multiple test files and named by published documentation — renaming it would change observable behavior. The feature's vocabulary checker can either narrow its scope to exempt these two surfaces by name, or the rule cannot be enforced yet.

Turning on the project's "no retired words in help text" rule for real means choosing: either live with these two specific exceptions because they represent real constraints, or reverse the rule and stay in planned mode until those constraints can be resolved. The first option is the recommendation — keep the rule on, keep these two named exceptions, and record the exception plainly in the code so it is not removed by accident later.

The recommendation is already executed and stands until you say otherwise.

### Q2 — apply the evidence skill update (2026-09-18, F268, round 7)

What needs deciding: the helper page that tells coding assistants how Remedy's job evidence is built is out of date, and the automated session is not allowed to write to that page. A corrected version of the page has been prepared and checked, but only you can put it in place, either by copying the prepared text over the page yourself or by allowing the session to write there.

Why it matters: the page still names a piece of code that was deleted and a field that the evidence no longer carries. An assistant that reads the page to inspect or explain a job's evidence will look for things that do not exist and may describe the evidence wrongly.

My recommendation: apply the prepared text as it is. It changes only the lines about the deleted code and field, and nothing else on the page. The session cannot carry this out itself, because the write is refused on its side; the round's handoff names the prepared file and its checksum.

What happens if you say nothing: the skill page keeps describing the deleted writer, and the finding it belongs to stays open until someone applies the text.

### Q3 — no planner provider flag (2026-09-18, F268, round 8)

What needs deciding: the one-command start was designed with a flag to choose which service does the planning, beside the flags that choose the builder and the reviewer. Today the planner can only use the local model server, so that flag would accept exactly one value. The session decided not to create it, and to create only the flag that picks which planning model to use.

Why it matters: a flag that accepts one value tells a user there is a choice when there is none, and it would have to be changed again the day a second planning service exists. Leaving it out keeps the help text honest, but it means the command's flag list differs from the design by one flag.

My recommendation: leave the flag out until a second planning service exists, and add it in the same change that adds that service.

What happens if you say nothing: the recommendation is already executed and stands until you say otherwise.

### Q4 — manual achieve ignores the contract (2026-09-18, F269, round 2)

What needs deciding: a mission now carries a contract, a list of acceptance criteria that each have a check. When the automatic run tries to declare a mission achieved while a blocking criterion is not yet met, it is refused and told which criteria are open. The manual command a person types to mark a mission achieved is not refused in that case. It prints which blocking criteria are still unmet and then marks the mission achieved anyway, because that command has always been described as the operator's own explicit judgement.

Why it matters: if the manual command also refused, a person could never close a mission whose contract they consider wrong or no longer relevant without first changing the contract. If it does not refuse, a mission can be marked achieved with a criterion unmet, although the command says so plainly.

My recommendation: keep the manual command as the operator's override, with the unmet criteria printed every time, and let only the automatic run be held by the contract.

What happens if you say nothing: the recommendation is already executed and stands until you say otherwise.
