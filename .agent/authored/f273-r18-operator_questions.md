# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q1 — two small command-line rulings (2026-09-17 and 2026-09-18, F281 round 14 and F268 round 8)

This entry joins two earlier, lower-impact entries so the file stays within its limit of five; both rulings are unchanged and each can be overturned on its own.

First ruling. What needs deciding: two pieces of command-line help text carry the word "loop", a word otherwise retired because it conflicts with the binding term "Mission". One sits in the description of a command whose name another feature already settled, so rewording it would rename a command people already type; the other describes a value a flag accepts, which several tests and the published documentation name, so rewording it would change what the command accepts. Why it matters: the rule against retired words in help text can only be switched on with these two named exceptions, or not at all for now. My recommendation: keep the rule on with the two exceptions, recorded plainly in the code so nobody removes them by accident.

Second ruling. What needs deciding: the one-command start was designed with a flag choosing which service does the planning, beside the flags for the builder and the reviewer. Today the planner can only use the local model server, so that flag would accept exactly one value, and the session created only the flag that picks the planning model. Why it matters: a flag with one possible value suggests a choice that does not exist, but leaving it out makes the flag list differ from the design by one flag. My recommendation: add that flag in the same change that adds a second planning service.

What happens if you say nothing: both recommendations are already executed and stand until you say otherwise.

### Q2 — apply the evidence skill update (2026-09-18, F268, round 7)

What needs deciding: the helper page that tells coding assistants how Remedy's job evidence is built is out of date, and the automated session is not allowed to write to that page. A corrected version of the page has been prepared and checked, but only you can put it in place, either by copying the prepared text over the page yourself or by allowing the session to write there.

Why it matters: the page still names a piece of code that was deleted and a field that the evidence no longer carries. An assistant that reads the page to inspect or explain a job's evidence will look for things that do not exist and may describe the evidence wrongly.

My recommendation: apply the prepared text as it is. It changes only the lines about the deleted code and field, and nothing else on the page. The session cannot carry this out itself, because the write is refused on its side; the round's handoff names the prepared file and its checksum.

What happens if you say nothing: the skill page keeps describing the deleted writer, and the finding it belongs to stays open until someone applies the text.

### Q4 — two mission-contract rulings (2026-09-18, F269 round 2 and F270 round 4)

This entry joins two earlier entries about how a mission's contract holds work back, so the file stays within its limit of five; both rulings are unchanged and each can be overturned on its own.

First ruling, the manual achieve command. What needs deciding: a mission now carries a contract, a list of acceptance criteria that each have a check. When the automatic run tries to declare a mission achieved while a blocking criterion is not yet met, it is refused and told which criteria are open. The manual command a person types to mark a mission achieved is not refused in that case. It prints which blocking criteria are still unmet and then marks the mission achieved anyway, because that command has always been described as the operator's own explicit judgement.

Why it matters: if the manual command also refused, a person could never close a mission whose contract they consider wrong or no longer relevant without first changing the contract. If it does not refuse, a mission can be marked achieved with a criterion unmet, although the command says so plainly.

My recommendation: keep the manual command as the operator's override, with the unmet criteria printed every time, and let only the automatic run be held by the contract.

Second ruling, pushes and unchecked criteria. What needs deciding: Remedy can now push a mission's committed work to the branch's remote when you ask it to, and the design says a push happens only when no blocking acceptance criterion of the mission is "red". A criterion can be met, failed, or not yet checked. The session first ruled that a criterion not yet checked also holds the push back. It then found that under the one-command start, the planner's per-milestone criteria are never checked at all, because that command's jobs serve no single milestone, so no real run could ever push. The session changed the rule: only a failed blocking criterion holds a push back, and every blocking criterion not yet checked is named in the push's output and its record.

Why it matters: with the stricter rule the push feature never works outside test fixtures. With the new rule a push can publish work whose planner-written criteria no check has confirmed, although every failed criterion still stops it and the unchecked ones are listed each time.

My recommendation: keep the new rule, which is the design's own word, and fix separately the gap that leaves the planner's criteria unchecked under the one-command start.

Third ruling, added 2026-09-19 (F273, round 18), the gap closed. What needs deciding: the session has now fixed the gap the second recommendation named. Each job of the one-command start records the milestone it serves, and the planner's criterion for that milestone is checked when the job finishes and marked met or failed. The check never stops the job itself. But a failed blocking criterion holds a push back, as the second ruling says, and the planner's usual criterion is that the project's tests pass. So in a project with no tests, or with failing tests, asking the one-command start to push is now refused: the work is still committed, and the refusal names the failed criteria. Before this change such a push went through, because the criterion was never checked. Why it matters: a person who uses the one-command start on a project without tests can no longer have it push. My recommendation: keep it. A push is refused only when the check the planner wrote has actually failed, which is exactly what the second ruling allows, and the commit is still made so nothing is lost.

What happens if you say nothing: all three recommendations are already executed and stand until you say otherwise.

### Q5 — contract jobs are granted automatically (2026-09-18, F269, round 6)

What needs deciding: until now a person had to grant a job, one command at a time, the right to run the repository's tests, to write a generated patch into the repository, and to revert such a write, and had to attach the repository to the job by hand. Those two commands are now removed. Instead, every job that belongs to a mission with a contract is attached to its repository and given those three rights automatically when it is created, because the contract is the order the operator accepted for that repository.

Why it matters: it removes a manual safety step. A job of a planned mission can now run tests, write generated patches and revert them without a separate grant. A job of a mission that was never planned has no way to receive these rights at all.

My recommendation: keep the automatic grants for contract jobs. The three rights are exactly what the remaining test, patch and self-run commands check, and the manual step only ever granted the same three.

What happens if you say nothing: the recommendation is already executed and stands until you say otherwise.

### Q7 — four behaviour changes, one session (2026-09-19, F273, rounds 8 to 11)

What needs deciding: while repairing registered defects, the session changed four things a person using Remedy can notice. First, a job's spending and token limits now count the calls of the run that is happening, so a job can be stopped partway through a run once it passes its limit; before, the money limit only saw earlier runs and the token limit saw nothing at all, so neither stopped anything mid-run. Second, the event list of a job now shows the newest events first and its limit keeps the newest ones, like every other list; before, it showed the oldest fifty. Third, the command that sets a single field of a job's budget now refuses the token and runtime fields when the job already carries its own token or time limit, and names the flag that sets that limit; before, the value was accepted and then quietly put back the next time the job ran. Fourth, the automatic mission loop can now continue a paused job, or one that ran out of cycles, as the same job, behind the same checks the manual resume command applies; before, it could only start a new job.

Why it matters: the first and third change what a limit does, the second changes what a list shows, and the fourth lets the loop continue work without a person typing a command, although it grants nothing the loop could not already start.

My recommendation: keep all four. Each repairs a behaviour that did not do what its own description promised, and each is covered by a test that fails if it is undone.

What happens if you say nothing: the recommendation is already executed and stands until you say otherwise.
