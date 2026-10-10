# F302 T003 — the fixed question and one real task, before the cut and after it

> Written by `.agent/authored/f302-r4-measure.py render` from `.agent/f302_after.jsonl` and
> `.agent/f302_attribution.jsonl` alone; every figure below is computed, none typed.

Provider calls: 4 for the question and 4 read from the two jobs' run records, of at most 12 (DECISION F302 D2 (4)). "Before" is the command line
before F302, with both keys true; "after" is the lean start, with neither set. Context is input
plus cache creation plus cache read: what the call's requests read, however much was cached.

## The fixed question

| Place | Start | Switches | Exit | Turns | Input | Output | Cache creation | Cache read | Context |
|---|---|---|---|---|---|---|---|---|---|
| scratch | before | none | 0 | 1 | 3 | 5 | 21,530 | 0 | 21,533 |
| scratch | after | `--safe-mode` `--tools` `Read,Glob,Grep,Edit,Write,MultiEdit` | 0 | 1 | 3 | 5 | 1,689 | 5,359 | 7,051 |
| remedy | before | none | 0 | 1 | 3 | 5 | 15,192 | 12,861 | 28,056 |
| remedy | after | `--safe-mode` `--tools` `Read,Glob,Grep,Edit,Write,MultiEdit` | 0 | 1 | 3 | 5 | 1,207 | 6,197 | 7,407 |

In the scratch place the context fell from 21,533 to 7,051, by 14,482; T002's two baselines there read 21,533, 21,533.
In the remedy place the context fell from 28,056 to 7,407, by 20,649; T002's two baselines there read 28,035, 28,035.

## One real task as a job

A job's call works through many turns of its own tool loop, and each turn reads the context
again, so a job call's context below counts every turn's reading.

- before: `SU-054`, "Narrow the excused handler at apps/cli/commands/job.py:1818", job `288b02c4836542ca` ended `completed` (T001 applied_to_job_workspace, verdict pass, staged_review_passed); 2 calls; input 29, output 16,674, cache creation 74,354, cache read 935,023.

- after: `SU-054`, "Narrow the excused handler at apps/cli/commands/job.py:1818", job `7ce423fd67604240` ended `completed` (T001 applied_to_job_workspace, verdict pass, staged_review_passed); 2 calls; input 32, output 18,192, cache creation 46,224, cache read 504,279.

| Start | Run | Seq | Round | Role | Input | Output | Cache creation | Cache read | Context |
|---|---|---|---|---|---|---|---|---|---|
| before | `da017de615ce4821` | 1 | 1 | builder | 19 | 9,366 | 34,695 | 690,944 | 725,658 |
| before | `da017de615ce4821` | 2 | 1 | reviewer | 10 | 7,308 | 39,659 | 244,079 | 283,748 |
| after | `1c9c87f3a3794fb9` | 1 | 1 | builder | 21 | 11,854 | 28,855 | 406,307 | 435,183 |
| after | `1c9c87f3a3794fb9` | 2 | 1 | reviewer | 11 | 6,338 | 17,369 | 97,972 | 115,352 |

The builder's first call read 725,658 before and 435,183 after.
