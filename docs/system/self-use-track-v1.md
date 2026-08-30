# The self-use track (v1)

> **Status (2026-08-29):** built by F257. The queue, its loader, the job-path
> seam and the closure-protocol precondition are in place; consumption happens
> at feature close. **Update (2026-08-30, F258 rounds 2-3):** the queue's
> schema moved to v2, adding a required `provenance` field naming each item's
> source, and `packages/orchestration/self_use_generator.py` now supplies one
> when the queue is empty (Tier 1: the oldest open Low/Medium finding; Tiers
> 2-3 are documented placeholders, DECISION F258 D2). This page's "Deliberate
> absences" below is corrected accordingly — the LOADER stays read-only, but
> the track as a whole is no longer discovery-free. **Update (2026-08-30,
> F258 round 5):** `packages/orchestration/self_use_runner.py` now RUNS a
> planned item through the real job path (builder/reviewer loop, isolated
> worktree) under a small budget, stopping at the normal approval gate
> (T002); this page's job-path and consumption sections are updated to
> match.

Remedy is used on Remedy on a schedule that cannot be skipped. This page is
where to look for the two file formats involved and for the rule that makes the
track run.

## Why it exists

"Dogfooding" rots the moment it depends on someone remembering to do it. The
self-use track replaces the intention with a mechanism: a curated queue of small
maintenance jobs, exactly ONE of which is consumed per feature close, planned
through the job path Remedy already has and RUN through it — builder/reviewer
loop, isolated worktree, small budget — to the normal approval gate (F258
T002).

## The queue file

`scripts/self_use_queue.json` — shipped, operator-curated INPUT, kept beside the
other shipped campaign data rather than under `docs/`, because a data file that
code reads is not a doc.

    {
      "schema_version": 2,
      "description": "<what this queue is for>",
      "items": [
        {
          "id": "SU-001",
          "title": "<one line>",
          "why": "<why this job is worth a feature close>",
          "job_markdown": "# Job: ...\n\n## Task 1\n...\n\nAcceptance:\n- ...\n",
          "consumed_by": "",
          "provenance": "<what found this item — a human curator, or a generator source>"
        }
      ]
    }

Rules the loader enforces, every one of them a refusal rather than a guess:

| Rule | Detail |
|------|--------|
| `schema_version` | must equal 2 (v1 files, without `provenance`, are refused, not half-read) |
| item keys | exactly the six above — no more, no fewer |
| `id` | must match `^SU-\d{3}$`, and must be unique across the file |
| `title`, `why`, `job_markdown`, `provenance` | non-empty strings |
| `consumed_by` | a string; empty means the item is still PENDING |

An item is PENDING while `consumed_by` is blank. `next_self_use_item` answers
the FIRST pending item in file order, which is the curation order.

## The job-file format

`job_markdown` holds the LITERAL text of a job file in the format
`packages.orchestration.pingpong_job.parse_job_file` already accepts: a
`# Job: <title>` H1, then one or more `## Task N` headings, each carrying an
`Acceptance:` line. The queue deliberately stores job-file TEXT rather than a
richer schema of its own, so there is never a second task format to keep in step
with the first.

The rendered bytes are the curated bytes: `write_self_use_job_file` performs no
templating and no substitution, so the text an operator reviewed is exactly the
text that runs.

## The self-use modules

| Module | Role |
|--------|------|
| `packages/orchestration/self_use_queue.py` | the READ side — loads, validates, answers the next pending item. Owns no writer. |
| `packages/orchestration/self_use_job.py` | renders one item to `<dest_dir>/<id>.md` and plans it via `plan_job_from_file`. Plans only; never runs, never promotes. |
| `packages/orchestration/self_use_runner.py` | runs the planned item via `run_job` under a small budget, in the isolated worktree the target repo gives it. Stops at the approval gate; never promotes, never marks consumed (F258 T002). |

## Consumption — exactly one per feature close

Precondition 6 of the closure protocol
([STATUS_closure_protocol.md](../roadmap/STATUS_closure_protocol.md)) requires
that exactly one self-use item is consumed by each close: the first pending item
is planned, RUN through
`packages.orchestration.self_use_runner.run_next_self_use_item` (F258 T002) to
the approval gate, and its `consumed_by` set to the feature's id in the
closure commit. An EXHAUSTED queue never blocks a feature —
the close records `self-use NONE (queue exhausted)` and proceeds, which is the
track asking for curation rather than stopping work.

## Deliberate absences

Remedy deliberately does not let a job mark its own queue item consumed. Neither
module owns a queue writer, and consumption is an edit the closure round makes.
A run that can check itself off is not a gate — the same reason
`docs/roadmap/STATUS.md` sits in `packages.orchestration.scope_fences`'s
built-in deny list.

Remedy deliberately does not discover, generate or infer queue items IN THE
LOADER ABOVE — that module stays read-only by construction (DECISION F257
D2). `packages/orchestration/self_use_generator.py` (F258, built round 3) is
the separate module that now does: it searches, in a fixed priority order,
for a source to append as a new PENDING item when the queue is empty, and
never marks anything consumed. The list a human curates and the list a
generator can extend now share one file and one loader; only the WRITER
changed, and it is still not this module.
