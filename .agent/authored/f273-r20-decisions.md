
## DECISION F273 D20 (2026-09-19, reviewer, round 20) — T015 is built: the direct-API provider keeps its usage and caches its prefix, one test proves every collected test runs in some CI stage, and the vitest ceiling is measured
CONTEXT: T015 of `docs/roadmap/features/T2_F273.md` mints one id per item at the start of the round that
takes it, and no round had taken it; its three items are registered as R-0994, R-0995 and R-0996 in this
round's first commit. A research helper prototyped them on the tree of `fdece9ab` and the reviewer
re-ran them in its own dry run.
CHOSEN: (1) R-0994. `ClaudeProvider._call` returns the CLI provider's shape: its usage is read through
`token_actuals`' envelope reader into `usage_actuals`, so `build` and `review` stop stamping
`provider_actuals_unavailable` when the SDK reported usage, and `tokens_used` is input plus output as on
the CLI path. `ComposedPrompt.stable_prefix()` is the leading run of segments ranked before `TASK`; the
loop offers it to a provider that takes one, and the direct-API provider sends it as a `system` block
with `cache_control` when the prompt starts with it, so the two parts concatenate to the prompt byte for
byte. Failures map most-specific-first to a kind with the HTTP status and a redacted, capped message.
`pyproject.toml` gains an `anthropic` extra that the ImportError text names. (2) R-0995. The partition
T015 (b) asks for does not hold by construction, because the `budgets` and `smoke` stages select by path
nodes the marker stages also select; the defect the item describes is a test no CI stage runs, so the
guard asserts coverage: one collection, each stage's selection evaluated in-process with pytest's own
expression reader, and every node selected by a CI stage or by the stage CI deliberately excludes. It
runs in the `budgets` stage, whose budget rule still yields 300 s. This amends T015 (b) (§4 item 7), and
T015 records it. (3) R-0996. Three runs of the vitest suite measured 1.01 s to 1.09 s on this machine; the
30 s ceiling is more than twice that and stays, and the test's docstring records the numbers, the machine
and the rule.
ALTERNATIVES: a keyword on every provider's `build` for the prefix, rejected because it breaks every fake
provider; one collection per stage, rejected at about 93 s; raising the vitest ceiling, rejected without
a measurement.
REVERSE: restore the touched files from `fdece9ab`, and delete this paragraph.
