# Plan — F288 Event stream completeness & prompt nodes in the live graph

Branch: feature/f288-event-stream-completeness, cut from `main` at
`db691093`, the merge commit of pull request 285 (F289 Self-use sources).

## Goal

Every builder, review, check, test and repair event the browser receives
carries the attempt id, the task id and the result; a plan-approved event
exists; and the live graph draws test-run, repair and prompt nodes
(`docs/roadmap/features/T5_F288.md`).

## Current Step

ROUND 5: book round 4's PASS and R-1075's resolution, record DECISION
F288 D5, and land the first half of T003 — prompts as `synapse` nodes of
the live model, children of their task, drawn at graph_spec's synapse
radius, and a click on one selecting the prompt itself.

## Next Steps

1. The second half of T003: the keyboard's parallel list of the live
   picture's prompt nodes, and a rendered proof in a headless browser.
2. The closure sequence.

## Risks

The simple view must not change, and a scrubbed timeline must draw no
prompt. Open findings: 0.
