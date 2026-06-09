# Parallel Review Protocol

## Finding Format

Each finding is a numbered entry in `.agent/live_review.md`:

```
### R-XXXX: <short summary>
- **Status**: Open | Resolved | Won't Fix
- **Severity**: Blocker | High | Medium | Low
- **Area**: <module or file>
- **Details**: <what is wrong>
- **Evidence**: <test output, code reference, or diff>
- **Expected fix**: <what the builder should do>
```

## Builder Fix Marker

When the builder fixes a finding, they add this line to the finding or to
their commit/response:

```
Done: R-XXXX - <brief summary of what was done>
```

## Reviewer Resolution

After verifying the fix, the reviewer updates the finding:

```
- **Status**: Resolved
```

Only the reviewer may mark a finding Resolved.

## Final Verdict Rules

| Verdict | Condition |
|---|---|
| **PASS** | No open Blocker or High findings |
| **PASS WITH RISKS** | Only Medium/Low remain and are documented as known risks |
| **FAIL** | Any Blocker or High finding remains open |

## Process Rules

1. Reviewer writes findings as soon as discovered — do not batch.
2. Builder reads `.agent/live_review.md` before every final response.
3. Builder must not claim merge-ready PASS while latest verdict is PENDING or FAIL.
4. Every open finding must have either a `Done: R-XXXX` marker or be listed as remaining risk.
5. Reviewer findings beat builder self-report on disputed facts.
6. Builder final handoff must reference the latest review verdict.

## Final Handoff: Changed Files Table

Every implementer final report MUST include a changed files table:

| File | What changed | Why |
|---|---|---|
| `path/to/file.py` | Added X | Needed for Y |

This table is required for merge readiness. Omitting it blocks the handoff.

## Progress Ledger

After long runs, agents should generate/check:
- `remedy progress checklist --agent --json`
- `remedy feature plan --agent --json`

The progress ledger unifies plan.md, live_review.md, and known risks into a structured checklist.

## Integrity Gate

Before claiming PASS, run:
- `remedy integrity check --json`

PASS not allowed if:
- integrity check fails
- latest live_review verdict is PENDING/FAIL
- relevant untracked files exist
- review zip import check fails (if review zip generated)

Final handoff must include:
- `remedy integrity check --json` status or explain why not run
- review zip generated with `scripts/make_review_zip.sh`
- changed files table
- latest live_review verdict
- open findings count
- known risks

## Review Bundle

Reviewers may request `remedy review bundle <job_id>` for a safe state package.
The bundle contains only safe summaries — no raw content, no secrets, no caches.
The bundle does NOT replace the live_review ledger. Findings still go to `.agent/live_review.md`.
