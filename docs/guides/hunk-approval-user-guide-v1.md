# Hunk-level diff approval — user guide (v1)

`remedy patch approve-hunks` records an operator's decision over the individual hunks of
a job's diff: which are approved, which are rejected, and why. It RECORDS and never
applies — no file in your repository is modified by it — and the reason you give for a
rejected hunk is quoted VERBATIM into the next builder prompt, which is what turns a
rejection into a repair instruction.

```
remedy patch approve-hunks <job-id> [--task-run <task-id>]
                           [--approve-hunk <hunk-id>]...
                           [--reject-hunk <hunk-id>=<reason>]...
                           [--json]
```

`<job-id>` may be any prefix a job id resolves by, the same as the other `remedy patch`
commands. Both hunk options are repeatable: give one occurrence per hunk.

## Where hunk ids come from

A hunk id is 16 lowercase hex characters. You do not invent one — read it from the diff
view, either in the UI's diff viewer or from the HTTP API:

    GET /api/jobs/<job-id>/diff                             the job-level diff
    GET /api/jobs/<job-id>/task-runs/<task-id>/diff         one task run's diff

Each file entry of that view carries a `hunks` list, and each hunk carries its `id`.

The id is CONTENT-DERIVED and carries no position. It is computed over the file's path,
the hunk's OLD side — its context and deleted lines, never its added lines — and the
hunk's occurrence rank among byte-identical old sides within the same file. The property
you may rely on: a hunk KEEPS its id when other hunks in its file move, grow or vanish,
and when its OWN added lines change, because a second proposed fix for the same original
text is the same hunk. It changes only when the path changes or when the hunk's own old
side does. A decision you record therefore survives the builder rewriting its answer.

## Choosing the scope

Omit `--task-run` to decide over the JOB-level diff. Pass it to decide over one task
run's diff, named exactly as that run appears under `task_runs/` in the job's evidence.

The scope you choose is the scope the decision is recorded under, and the two do not
mix: a decision recorded at job scope is deliberately NOT quoted into any single task's
next prompt, because it was never attributed to one.

## What a recorded decision holds

Every hunk of the chosen diff appears in the record on two independent axes.

STATE is what you decided: `approved`, `rejected` or `pending`. A hunk you named in
neither option is `pending`, and that is a legitimate answer rather than an error — a
hunk appearing for the first time in a later round inherits no decision.

LANDING is what became of the bytes: `landed`, `not_landed` or `unattempted`. Recording
a decision never runs an apply, so every entry this command writes lands `unattempted`.
That is not a synonym for `not_landed`: the first means no apply has run, the second
means one ran and these bytes did not reach the branch.

Deciding the same scope twice REPLACES the earlier record rather than adding a second,
so you may revise freely while the landing is still `unattempted`.

## Output

Without `--json`, four lines:

    Recorded: <task-id>:<attempt>
      approved: 2
      rejected: 1
      pending: 5
    Note: the decision is metadata only — no files have been modified.

With `--json`, the record itself is printed with sorted keys — `task_id`, `attempt`,
`decided_at` and `hunks` — where each row of `hunks` carries exactly `id`, `state`,
`reason` and `landing`, and nothing derived.

## When the command refuses

A refusal exits 1 and writes NOTHING to the job: a refused decision is not a
half-recorded one. Without `--json` the message goes to stderr, with the offending ids
on a following `hunks:` line; with `--json` the refusal is printed as `code`, `message`
and `hunk_ids`. The codes, in the order they are checked:

    no_diff_available   the attempt has no diff to decide over at all
    untrustworthy_view  the diff was truncated, so which hunks it omits is unknown
    empty_decision      you approved nothing and rejected nothing
    duplicate_hunk      an id repeats within --approve-hunk, or within --reject-hunk
    overlapping_sets    an id appears in both
    unknown_hunk        an id is not among the hunks this diff carries
    missing_reason      a rejection carries no reason, or only whitespace

The FIRST code that trips is the one you see, and `hunk_ids` names every offending id at
once rather than one per round-trip.

## Reasons are held byte for byte

`--reject-hunk <id>=<reason>` splits on the FIRST `=`, so a reason may itself contain an
`=` and survives whole. The reason is stored exactly as typed — surrounding whitespace,
interior blank lines and tabs included — and reaches the next builder prompt unchanged:

    remedy patch approve-hunks 4f2a \
        --approve-hunk 1c9e0b77a4d3f215 \
        --reject-hunk 8b31c04ef7a9d260="renames a public name; keep the old spelling"

Remedy deliberately does not reformat, wrap, truncate or normalise a rejection reason.
They are the operator's own words, and the next round is told to act on them.
