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
