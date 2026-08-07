Target: docs/README.md
Operation: two independent replacements. Each FROM occurs exactly 1x
(verify both before editing).

PAIR 1 — quick-find table

FROM
<<<FROM
| split workflow | [split_workflow.md](agents/split_workflow.md) | agents |
FROM>>>

TO
<<<TO
| split workflow | [split_workflow.md](agents/split_workflow.md) | agents |
| self-drive | [self_drive_protocol.md](agents/self_drive_protocol.md) | agents |
TO>>>

PAIR 2 — Agent Conventions table

FROM
<<<FROM
| [orchestrator_protocol.md](agents/orchestrator_protocol.md) | F070 orchestrator role contract — the source of the loop's system prompt |
FROM>>>

TO
<<<TO
| [orchestrator_protocol.md](agents/orchestrator_protocol.md) | F070 orchestrator role contract — the source of the loop's system prompt |
| [self_drive_protocol.md](agents/self_drive_protocol.md) | One-session build discipline: roles, state probe, round loop, guardrails |
TO>>>
