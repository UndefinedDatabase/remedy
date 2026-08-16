# Handback Template (mandatory)

> Mandatory skeleton of every `.agent/handoff.md` rewrite
> (docs/agents/split_workflow.md round life cycle). All sections required,
> in order. A missing or incomplete section is a Medium finding; the
> second occurrence within one feature is High and blocks until a
> compliant handback exists. (A wholly missing changed-files table remains
> the R-0070 block condition.) Stay within the AGENTS.md handoff cap —
> ≤60 lines, ≤100 when per-commit tables of >5 commits require it,
> ≤160 when a LARGE bundle's >10-commit tables require it
> (DECISION 2026-08-03, F070 R1 precedent: 16 commits) — by
> trimming transcripts to command + exit code + decisive lines and by
> summarizing evidence directories — never by dropping a section.
> Hard cap: this file stays ≤800 tokens — ≤1600 in the >10-commit
> LARGE case (P4 token thrift).
> Write-once rule (PH v3): draft the handback in the session
> scratchpad, measure it there (`wc -l`) against the cap, then write
> and commit `.agent/handoff.md` ONCE — trim commits against the cap
> are a smell, not a workflow (F251 lesson: 116→91→110→103→100).

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
