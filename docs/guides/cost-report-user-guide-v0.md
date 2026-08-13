# Cost report — user guide (v0)

`remedy stats report` answers one question about a project: where did the tokens
go, and what did they cost. It reads that project's token ledger and writes
nothing. Every number it prints comes from a ledger row — nothing is
interpolated, and nothing is priced that a provider did not price.

For the estimates Remedy makes BEFORE a task runs, see
[token-economy-user-guide-v0.md](token-economy-user-guide-v0.md). This guide is
about actuals, after the fact.

## The command

```
remedy stats report [--since <ts>] [--until <ts>] [--job <id>]
                    [--by role|model|day] [--label <name>]
                    [--project <id>] [--json]
```

- `--since` / `--until` bound the period as ISO-8601 timestamps (`2026-08-01`,
  or `2026-08-01T12:00:00+00:00`; a trailing `Z` is read as `+00:00`). The
  period is HALF-OPEN: a call at exactly `--since` is IN, a call at exactly
  `--until` is OUT. Two adjacent periods therefore never double-count a call.
- `--job` narrows to one job — in this period AND in the period it is compared
  against, so the comparison stays one question rather than two.
- `--by` groups the cost table by `role`, `model` or `day`. Without it you get
  the grand total only.
- `--label` names the scope in the report's header. The default is
  `(unlabelled)`.
- `--project` picks the project whose ledger is read. Exactly one, and there is
  deliberately NO `--all-projects`: cost folds across projects but the segment
  breakdown does not, so an all-projects report would publish one project's
  breakdown under a multi-project total.
- `--json` prints the same facts as a machine-readable payload.

All timestamps are UTC, and the report says so in its own header.

## What it looks like

This is the report the suite pins against a fixture ledger, copied verbatim
from `tests/orchestration/fixtures/cost_report/golden/cost_report.md`:

```text
# Cost report — f115-golden

Filters: since=-  until=-  job=-  by=day · all timestamps UTC

## Cost

| bucket | calls | tokens in | tokens out | cache read | cache write | cost usd | basis |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-08-01 | 1 | 1000 | 200 | unmeasured | unmeasured | unmeasured | 0/1 measured |
| 2026-08-05 | 1 | 1000 | 200 | unmeasured | unmeasured | unmeasured | 0/1 measured |
| 2026-08-09 | 2 | 2000 | 400 | 64 | 32 | 0.2500 | 1/2 measured |
| TOTAL | 4 | 4000 | 800 | 64 | 32 | 0.2500 | 1/4 measured |

PARTLY UNMEASURED: these figures cover only the 1 call(s) whose provider reported them; the 3 unmeasured call(s) contribute nothing to any figure above.
No price is computed: a cost appears only where a provider reported one.

## Where the tokens went

| segment | calls | segments | chars | tokens est. | share |
| --- | --- | --- | --- | --- | --- |
| diff | 1 | 1 | 400 | 100 | 43.5% |
| schema_tail | 1 | 1 | 60 | 100 | 43.5% |
| task_brief | 1 | 1 | 120 | 30 | 13.0% |
| TOTAL | - | 3 | 580 | 230 | 100.0% |

Attribution: 2 call(s) carry a segment manifest, 2 do not. An unattributed call is one whose prompt was never traced; it is counted here and given no share of any segment kind.

## Compared to the previous period

No previous period: this report has no start or no end, and an open-ended period has no length to mirror.
```

## Reading the numbers

Three sections, always in this order.

**`## Cost`** — one row per bucket plus a `TOTAL` row: calls, tokens in and
out, cache read and write, cost in USD, and the row's basis as `N/M measured`.
A figure no provider reported prints the word `unmeasured`, never `0`: a reader
has to be able to tell "nobody reported this" from "it was zero", and in a
column of numbers only a word does that. A total that is only partly measured
says so in its own sentence. No price is ever computed — there is no price
table, so an unpriced call stays unpriced instead of being multiplied into a
plausible figure.

**`## Where the tokens went`** — the input share per prompt-segment kind, taken
from the segment manifest each traced call records. The `Attribution:` line
names how many calls carry a manifest and how many do not. An unattributed call
is one whose prompt was never traced: it is counted, and given no share of any
segment kind, rather than being guessed into a bucket.

**`## Compared to the previous period`** — the equal-length window immediately
before this one, queried under the same `--job` filter. It needs BOTH bounds:
an open-ended period has no length to mirror, and the report prints that reason
instead of a table. A previous window that exists but held no calls gets a
different sentence, because "there was no window to look at" and "we looked and
found nothing" are two different facts about the same empty space. Where there
IS a table, the line under it names the window that was compared against, so
the baseline is never anonymous.

## Two breakdowns this report does not have yet

The roadmap asks for a per-role and a per-task-class breakdown. Remedy
deliberately does not fake either one:

- `--by role` has ONE bucket today, because a task run's `role` is recorded as
  `"builder"` for the whole run. The existing `remedy stats cost` view already
  prints that limit in its own output.
- There is no per-task-class breakdown at all: no ledger row carries a task
  class, so there is nothing to aggregate. The report stays silent rather than
  inventing a bucket.

Both limits belong to their own features. This report shows what exists and
says nothing about what does not.

## When there is no ledger

A project whose ledger was never written is not a project that cost nothing, so
the report refuses to print a table of zeros and says this instead:

```
No ledger on disk for this scope — nothing has been recorded yet. Run 'remedy stats backfill-ledger <evidence-dir>' to mirror existing evidence.
```

`remedy stats backfill-ledger <evidence-dir>` mirrors finalized task runs from
an evidence directory into the ledger. It writes the ledger and never the
evidence, and it is idempotent: the same evidence always yields the same rows.
Run it, then run the report again.

## The json payload

`--json` prints `report_version: 3` and these top-level keys:

`buckets`, `comparison`, `filters`, `label`, `ledger_exists`, `note`,
`report_version`, `segments`, `total`, `unmeasured_notation`

In json an unmeasured figure is `null`, not the word — and
`unmeasured_notation` states that convention inside the payload itself, so a
consumer cannot read a missing measurement as a zero.
