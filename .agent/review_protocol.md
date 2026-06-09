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

## Review Bundle

Reviewers may request `remedy review bundle <job_id>` for a safe state package.
The bundle contains only safe summaries — no raw content, no secrets, no caches.
The bundle does NOT replace the live_review ledger. Findings still go to `.agent/live_review.md`.
