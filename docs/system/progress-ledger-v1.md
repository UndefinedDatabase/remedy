# Progress Ledger v1

Structured checklist built from plan, live review, and known risks.

## Generate

```bash
remedy progress checklist --agent [--json]
remedy progress checklist <job_id> [--json]
```

## What it does

Parses `.agent/plan.md`, `.agent/live_review.md`, and `.agent/context.md` into a unified checklist:

- Plan steps become done/planned/skipped items
- Live review findings become resolved/blocked items
- Known risks and pre-existing issues become risk items
- Job artifacts (test failures, proof gaps) become risk items

## Statuses

| Status | Meaning |
|---|---|
| planned | Not started |
| in_progress | Work underway |
| done | Completed |
| resolved | Finding fixed and verified |
| blocked | Open blocker/high severity finding |
| deferred | Postponed |
| risk | Known risk, not yet resolved |
| skipped | Explicitly skipped |

## Overnight checklist experience

After a long Remedy run, the user sees:

1. Checked items with step numbers
2. Open blockers with severity
3. Known risks
4. Latest review verdict
5. Inconsistencies (e.g., PASS verdict with open blocker)

## Sources

| Source | Items |
|---|---|
| `.agent/plan.md` | Checklist steps |
| `.agent/live_review.md` | Findings with Done markers |
| `.agent/context.md` | Known risks, pre-existing issues |
| Job artifacts | Test failures, repair artifacts |
| Job events | Proof gaps |

## JSON output

```json
{
  "version": 1,
  "scope": "Steps 1010-1029: ...",
  "verdict": "PASS — all blockers resolved",
  "done_count": 15,
  "open_count": 2,
  "blocked_count": 0,
  "risk_count": 1,
  "skipped_count": 0,
  "total_count": 18,
  "inconsistencies": [],
  "items": [...]
}
```

## Safety

- No raw file contents in export
- No raw stack traces
- Item titles bounded to 200 chars
- Finding details/evidence not included (only title, severity, area)
