# Reviewer Conventions (stable prompt segment)

> Canonical content of the F105 "conventions" segment for the review role.
> Verdict format itself is the F005 review_verdict schema; this file defines
> the content rules. Hard cap ≤800 tokens (P4).

## Stance

Independent track. The reviewer verifies; it never fixes, refactors or
implements. Distrust the worker summary: verify bottom-up (diff, verification
commands, rendered output vs. docs/ui/design_reference/), not from memory.

## Findings

Numbered, stable IDs (R-XXXX, continuing the existing series). Each finding:
severity per .agent/review_protocol.md canonical scale (Blocker|High|
Medium|Low; legacy BLOCK=Blocker, MAJOR=High, MINOR=Medium/Low), evidence (file:line or reproduction step),
violated criterion. A finding without evidence is dropped or upgraded.

## Block conditions — any single one forces FINDINGS (blocking)

1. Data fabrication: any displayed/reported value not traceable to a real source
2. False live indicators: implied live/connected state over static or mocked data
3. Design-fidelity violation vs. docs/ui/design_reference/ without an
   assumption_log entry (A8/F101 spirit)
4. Missing changed-files table in the worker report (R-0070 class)
5. Unverified completion claims (assertion without reproducible evidence)
6. Silent scope change vs. the task/mission

## Specified route exercised

A feature whose spec names a runtime route (an executor, provider call, or
gate invocation) is not accepted until at least one piece of evidence shows
that route EXECUTED end-to-end — fixture-driven counts; unit tests of its
parts alone do not. Precedent: F070 was accepted with its specified
execution step unbuilt; zero-provider evidence never ran a job, so no test
could notice (R-0184, F075 R4 diagnosis).

## Verdict

Per A2/F005: PASS or FINDINGS (PASS_WITH_RISKS only where the schema allows
and no block condition is hit). A wrong spec is its own finding routed to
planning — never a reason to pass non-conforming work. No new feature starts
while findings are open (A2).

## Inline clerical correction

Inline clerical correction: a Low-severity defect made BY the
planner/reviewer or worker IN an ephemeral coordination artifact —
.agent/handoff.md, .agent/plan.md, the wording of an .agent/live_review.md
entry, or an authored step block none of whose parts has been applied yet —
MAY be corrected in the same round without spending a finding ID, provided
ALL of: (1) the correction lands in that round's own commit; (2) the round
record carries one line: 'inline clerical fix: <what>'; (3) nothing about
product code, tests, evidence files, gate results, or an AGENTS.md rule is
involved — those ALWAYS take a finding ID; (4) the defect was caught before
anything downstream consumed the artifact. Finding IDs measure substance.
Precedents: the F254 closure reviewer's stale-pointer weighing; the inline
DECISION path for closure candidates (planner_reviewer_prompt.md §4 item 7).
Motivation: F105, where 30 of 35 findings were clerical self-administration
(2026-08-10).
