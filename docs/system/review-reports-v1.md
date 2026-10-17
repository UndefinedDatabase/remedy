# Review reports v1

> Status (operator order exec-1017, 2026-10-17): built. DECISION exec-1017 D5 in
> `.agent/decisions.md`.

A review report is one JSON file per `remedy do` walk that asked for it. It holds what a reviewer
needs to judge the run without recording a job id or running an export: the effective order and
configuration, the lane and why, the planning calls, every job and task with its runs, phase times,
measured usage, each Pi call's model turns and tool calls, the verification, changed files, review
verdicts, errors and the outcome. These are Remedy's own review evidence; they have nothing to do
with Universe's Improve tasks or Luna's reports.

## Asking for one

| Where | How |
|---|---|
| Command line | `remedy do run "<order>" --capture-review` (also with an order file) |
| HTTP | `POST /api/v1/orders` with `"capture_review": true`; it passes `--capture-review` to the walk the supervisor starts |

The `do` answer's `review_report` names it: `{report_id, status, file}`, `file` relative to the
data root; null without the flag. Every job the walk plans and runs is in the report, including the
jobs of an HTTP order. A job left waiting and run later by `remedy job run` is not: that run is not
part of the walk.

## Where it lives

`<data root>/review_reports/<report id>.json`, the data root being the one Remedy resolves
(`REMEDY_DATA_DIR`, the configured `data_dir`, else the checkout's `.data/`, which `.gitignore`
ignores). The id is `rr-<UTC start time>-<8 hex>`; it sorts by start time. Reports are kept: no
retention rule removes them.

## How it is written

Atomically, twice, under the same id: when the walk starts (`outcome.status` `running`) and when it
ends, whatever ended it. The outcome is `completed`, `failed`, `stopped`, `budget_exhausted`,
`cancelled` (Ctrl-C, SIGTERM, or the order's cancel request, whose reason and step the outcome
names) or `crashed` (an unexpected error; the walk's own error still ends the command). A process
killed outright leaves the `running` write, which says it never finished. `order` names the
supervisor's order id (`supervisor_order_id`) and its cancel request (`cancel`) for a walk the
serve supervisor started. Every job of the walk keeps the report's id, so a job run later (a waiting
job, a resumed one) rewrites its entry under `jobs` and adds itself to `continued`; the walk's own
outcome stays what the walk ended with.
A report that cannot be built is written `incomplete` with the reason. `not_measured` names what
the walk cannot know: queue time before its process started, inference time apart from tool time
inside one Pi call, planner tokens.

Every string is redacted by `stream_evidence.redact_json_value` and the home directory is written
`~`. No whole model prompt is copied; the run records keep only prompt sizes and hashes.

## In the review ZIP

`scripts/make_review_zip.sh`, with no argument, packages the newest ten reports (by start time,
then id; failed and cancelled runs included) under `review_reports/`, with `index.json` and
`INDEX.md`. With none, the index says that none exists and lists none. The copies are redacted a
second time. The ZIP's timestamps are fixed, so the same reports give the same bytes.
`--evidence-dir` and `--job-id` keep working as before.

## Code

`packages/orchestration/review_reports.py` (the report and its writes),
`scripts/stage_review_reports.py` (the ZIP's selection), `do_sequence.walk_do_sequence` (the one
place the report is opened and finished).
