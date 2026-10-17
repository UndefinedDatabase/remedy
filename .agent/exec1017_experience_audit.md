# exec-1017 Phase 6 — does earlier experience reach a new job? (audit, 2026-10-17)

Read-only audit of the code on branch feature/execution-quality and of the operator's data root
(through `remedy stats failures --json` and `remedy memory list --json`; `.data/**` not read raw).

## What a new job's model calls are shown

| Call | Context it receives | Earlier experience in it |
|---|---|---|
| Planner: mission plan, intake, task plan | the order, the target repository's top-level listing (exec-1017 D1), fixed rules | none |
| Builder (Pi) | task body = the order's own words, previous tasks of the same job, goal/file tree/README | only the same job's earlier tasks |
| Reviewer (Pi) | task body and acceptance, staged diff, test result | none |
| Repair | the reviewer's findings of this run | only this run |

## Where experience is stored, and who reads it

| Store | Written by | Read by a model call? | Operator data root, 2026-10-17 |
|---|---|---|---|
| Memory cards (`packages/memory`, `memory_learn`) | `remedy memory learn` (manual) | no | 0 entries |
| Post-mortems (`failure_postmortem`) | every terminal failure | no (`remedy stats failures` counts them) | 0 (3 jobs scanned) |
| Project brain / study | `remedy study`, the do study step | no (viewer, brain detail, study staleness) | — |
| `.agent/decisions.md`, regression tests | sessions | no; they act as CODE (guards, tests) | — |

## The small set of earlier failures, checked

| Failure | Would retrieval have helped? | What prevented the repeat |
|---|---|---|
| 2026-10-16 README order: checksum, comparison and report tasks (R-1336) | The planner ignored explicit rules in its own prompt (amend1016p) | `order_scope` constraints, `_without_checking_tasks`, `work_milestones` |
| 2026-10-17 README order: `test_command.txt`, 28-turn builder | No: the planner's error came from wrong repo facts, not missing lessons | exec-1017 D1, D2, D4 |
| Scale audit planner invents files (amend1014 D6) | No | `order_scope_violations` guard |

## Result

Earlier experience reaching a model call: 0 of 3 failures, context overhead 0 tokens. Every
repeat that was prevented was prevented by turning the lesson into deterministic code with a
regression test. No memory rewrite, and no injection of history into prompts: with a local model
that ignored explicit rules, more prompt text has no demonstrated benefit and costs tokens on
every turn of every Pi loop (exec-1017 D4 shows an agent loop resends its prompt every turn).
Next useful step, not built: when a job fails, list its post-mortem class beside a re-run's order
so the operator sees it, without putting it in a prompt.
