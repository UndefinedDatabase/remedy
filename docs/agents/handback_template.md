# Handback Template (mandatory)

> Mandatory skeleton of every `.agent/handoff.md` rewrite
> (docs/agents/split_workflow.md round life cycle). All sections required,
> in order. A missing or incomplete section is a Medium finding; the
> second occurrence within one feature is High and blocks until a
> compliant handback exists. (A wholly missing changed-files table remains
> the R-0070 block condition.) Stay within the AGENTS.md handoff cap —
> ≤60 lines, ≤100 when per-commit tables of >5 commits require it — by
> trimming transcripts to command + exit code + decisive lines and by
> summarizing evidence directories — never by dropping a section.
> Hard cap: this file stays ≤800 tokens (P4 token thrift).

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
command + outcome. `None` if none.

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

## Next

The single expected next action.
