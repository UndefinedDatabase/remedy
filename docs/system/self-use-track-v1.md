# The self-use track (v1)

> **Status (2026-08-29):** built by F257. The queue, its loader, the job-path
> seam and the closure-protocol precondition are in place; consumption happens
> at feature close.

Remedy is used on Remedy on a schedule that cannot be skipped. This page is
where to look for the two file formats involved and for the rule that makes the
track run.

## Why it exists

"Dogfooding" rots the moment it depends on someone remembering to do it. The
self-use track replaces the intention with a mechanism: a curated queue of small
maintenance jobs, exactly ONE of which is consumed per feature close, planned
through the job path Remedy already has and taken to the normal approval gate.

## The queue file

`scripts/self_use_queue.json` — shipped, operator-curated INPUT, kept beside the
other shipped campaign data rather than under `docs/`, because a data file that
code reads is not a doc.

    {
      "schema_version": 1,
      "description": "<what this queue is for>",
      "items": [
        {
          "id": "SU-001",
          "title": "<one line>",
          "why": "<why this job is worth a feature close>",
          "job_markdown": "# Job: ...\n\n## Task 1\n...\n\nAcceptance:\n- ...\n",
          "consumed_by": ""
        }
      ]
    }

Rules the loader enforces, every one of them a refusal rather than a guess:

| Rule | Detail |
|------|--------|
| `schema_version` | must equal 1; a file from the future is refused, not half-read |
| item keys | exactly the five above — no more, no fewer |
| `id` | must match `^SU-\d{3}$`, and must be unique across the file |
| `title`, `why`, `job_markdown` | non-empty strings |
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

## The two modules

| Module | Role |
|--------|------|
| `packages/orchestration/self_use_queue.py` | the READ side — loads, validates, answers the next pending item. Owns no writer. |
| `packages/orchestration/self_use_job.py` | renders one item to `<dest_dir>/<id>.md` and plans it via `plan_job_from_file`. Plans only; never runs, never promotes. |

## Consumption — exactly one per feature close

Precondition 6 of the closure protocol
([STATUS_closure_protocol.md](../roadmap/STATUS_closure_protocol.md)) requires
that exactly one self-use item is consumed by each close: the first pending item
is planned, taken to the approval gate, and its `consumed_by` set to the
feature's id in the closure commit. An EXHAUSTED queue never blocks a feature —
the close records `self-use NONE (queue exhausted)` and proceeds, which is the
track asking for curation rather than stopping work.

## Deliberate absences

Remedy deliberately does not let a job mark its own queue item consumed. Neither
module owns a queue writer, and consumption is an edit the closure round makes.
A run that can check itself off is not a gate — the same reason
`docs/roadmap/STATUS.md` sits in `packages.orchestration.scope_fences`'s
built-in deny list.

Remedy deliberately does not discover, generate or infer queue items. The list
is operator-curated data; curation is where this feature's risk sits, and the
queue is exactly as useful as the human who wrote it.
