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
