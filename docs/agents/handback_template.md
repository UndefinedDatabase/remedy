# Handback Template (mandatory)

> Mandatory skeleton of every `.agent/handoff.md` rewrite
> (docs/agents/split_workflow.md round life cycle). All sections required,
> in order. A missing or incomplete section is a Medium finding; the
> second occurrence within one feature is High and blocks until a
> compliant handback exists. (A wholly missing changed-files table remains
> the R-0070 block condition.) Keep transcripts trimmed to command, exit
> code and decisive lines, and summarize evidence directories — never drop
> a section.
>
> Operator amendment amend0827-process-diet (2026-08-27), rule 3 — A
> HANDBACK HAS NO SIZE CAP OF ANY KIND. The three LINE tiers stated here
> until this date — ≤60, ≤100 when per-commit tables of >5 commits require
> it, ≤160 for a LARGE bundle's >10 commits (DECISION 2026-08-03, F070 R1
> precedent) — are WITHDRAWN, together with the AGENTS.md DECISION D15
> stated-cause overage ceremony they fed. A handback is VALID when it
> carries its mandated sections; its length is not measured, not declared
> and never the subject of a finding. Reason: the tiers stopped bounding
> anything and started generating work — measured across F031, 63 of 75
> handbacks exceeded the 60-line base tier and 12 exceeded 100, at a median
> of 93 lines and a maximum of 198, every one of them through the
> declared-overage route, so the ceremony cost a paragraph per handback and
> bought no brevity. Note for anyone reading finding R-0700,
> which calls the ≤160 tier one "AGENTS.md does not define": the tier was
> real and was defined HERE, in this file, and only here.
>
> A "≤800 tokens — ≤1600 in the >10-commit LARGE case" hard cap also stood
> here until 2026-08-20, when DECISION F255 D6 withdrew it (findings
> R-0462 and R-0602). Do not restate a cap of either kind without
> re-measuring what the mandated sections actually cost.
>
> Write-once rule (PH v3), which SURVIVES this amendment: write and commit
> `.agent/handoff.md` ONCE per handback. Trim commits against a handback
> are a smell, not a workflow (F251 lesson: 116→91→110→103→100); with no
> cap left to trim against there is even less reason for a second write.
>
> Reverse the amendment by restoring the tier paragraph from git history
> at `f4eae1d4`, here and in the three other files that carried it.

## Session

One line, MANDATORY from 2026-08-27 (operator amendment
amend0827-process-diet, rule 6):
`SESSION <n> of feature <Fxxx> · round <r> · rounds so far <total>`.
`<n>` counts loop sessions on this feature, read from the previous handback
and incremented at session start; `<total>` counts delegated rounds across
the whole feature. Both counts exist so the 25-round / 7-session soft limit
is visible WHILE it is being approached rather than after. At or past the
limit this section additionally carries the scope report the limit obliges —
what is finished, what is missing, and the proposal — and the session output
carries the line `SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER
ÜBERGABE`. Reverse by deleting this section.

## Range

One line: `Review of <LAST_REVIEWED_SHA>..<HEAD>`.

## Commits

One changed-files table PER COMMIT, for EVERY commit in the range —
including state-file and bookkeeping commits:

    ### <short-sha> <subject>
    | Path | +/- | Reason |

Evidence-dir file lists may be summarized as "<n> files under <dir>".
Exception (self-reference): the final handoff commit and any trailing
bookkeeping commits that only trim it may share ONE grouped table with
per-commit attribution in the Reason column — a handoff cannot table
the commit that writes it (R-0149 pattern).

## External actions

Every push, PR create/edit/merge, gh command, worktree add/remove —
command + outcome. PR create entries include the resulting PR
number (DECISION 2026-08-01 — the F056 closure handoff omitted it).
`None` if none.

## Verification

Raw transcripts — command, exit code, real trimmed output — for every
gate the round's paste block ordered. Never a summarized "green".

## Authored-text proofs

For every reviewer-authored text applied this round: the disk-to-disk
comparison result against the committed `.agent/authored/` file, per the
fidelity protocol in docs/agents/split_workflow.md. `None applied` if
none.

## Deviations & assumptions

Each with justification / assumption_log pointer. `None` if none.

ANY DEPARTURE FROM THE BLOCK'S ORDERED COMMIT SEQUENCE BELONGS HERE, not only in
the commit table: an extra commit, a dropped one, or a reordering is a deviation
even when it is correct and even when the commit table already shows it (finding
R-0485). A round report dies with its session and this file does not, so a reader
auditing whether a round followed its block reads this section and nothing else.

## Next

The single expected next action.
