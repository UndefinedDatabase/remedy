# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md, scoped by DECISION F262 D4; the nine
remaining wirings are F267's per DECISION F262 D5).

## Current Step

Round 26, session 9 — closure preconditions 6 and 3. The self-use queue
holds no pending item (eight, all consumed), so
`generate_and_append_if_empty()` appends one (expected SU-009, tier 1,
the oldest open Low/Medium finding), `run_next_self_use_item()` runs it
unflagged to the normal approval gate with the default small budget,
`describe_self_use_run_defects()` is reported verbatim, evidence lands
under `.agent/selfuse_f262/`; then `integrity check --json` via the
`apps.cli.grouped` module route. No `consumed_by` edit, no new R-id.

## Next Steps

- Book round 26 (with the reviewer's defect-registration narration
  against the open set — §3 item 30), then closure algorithm steps 1-2:
  evidence job `f262-closure` (EVIDENCESCRIPT template from
  `.agent/authored/f009-r33.md`), fresh review zip with red control.
- The closure commit (STATUS `[x]`, README sync, `consumed_by=F262` on
  the new item) and the pull request; merge under the operator's
  2026-09-05 authorization once hosted CI reads green.

## Risks

- The self-use run is a real, budget-capped call against local
  `ollama` (`max_cost_usd=0.50`, `max_provider_calls=6`); prior runs of
  the same tier-1 pick ended BLOCKED at the approval gate — the correct
  outcome — and their defect strings were added to the open `R-0784`.
- `append_generated_item` may rewrite `scripts/self_use_queue.json`
  whole (open `R-0785` class); report append vs rewrite, never fix it.