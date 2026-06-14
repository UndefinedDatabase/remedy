# Self-Dogfood Readiness + Self-Improvement Planner v0

Remedy can inspect its **own** evidence — live review verdict, handoff state, missing
evidence, failed tests, repair/provider chains, roadmap position — and produce
structured improvement items + a plan + **ProposedTasks**. It is a **planning rail**,
not autonomous self-modification.

    remedy self inspect [--job-id <id>] [--json]
    remedy self plan    [--job-id <id>] [--json]
    remedy self propose <job_id> [--item-id <id>] [--top N] [--json]
    remedy self report  [--job-id <id>] [--markdown] [--json]

## Flow

    project evidence
      → SelfDogfoodInspection (read-only)
      → SelfImprovementItems (classified, deduped by fingerprint)
      → SelfImprovementPlan (grouped, top 3)
      → remedy self propose → ProposedTasks
      → human evaluate / approve / materialize (EXISTING flow) → do continue

## Does NOT

- Edit code. Apply patches. Approve tasks. Insert `Job.tasks` directly.
- Create PRs, do git operations, or mutate `main`.
- Run a provider / network / subprocess / browser, or run in the background.

`self inspect` / `self plan` / `self report` are **read-only**. `self propose` is
**metadata-only** — it creates ProposedTasks (origin self-dogfood) that still require
the normal human evaluation/approval and materialize → do continue flow.

## What it inspects

- **Live review** verdict + open finding counts (reused parser). PENDING/FAIL or an
  open blocker/high becomes a self-improvement **blocker**.
- **Stale handoff**: plan marked done with open steps; PASS handoff missing a
  changed-files table or test count.
- **Evidence gaps** (job-scoped): unresolved failure with no repair attempt; repair
  attempt with no pending intent; accepted provider candidate not materialized.
- **Roadmap**: deterministic rules that cite a module as evidence (e.g. trust gate +
  request builder present → "Provider Trust Verification v1").
- **Quality debt**: registry-only checks (e.g. missing docs page). No arbitrary code
  scanning in v0.

## Items

Each item has a stable fingerprint, a type (`bug`, `safety_gap`, `evidence_gap`,
`test_gap`, `docs_gap`, `ux_gap`, `architecture_gap`, `roadmap_next`, `cleanup`,
`security_hardening`), a priority (`blocker`/`high`/`medium`/`low`), and a confidence.
All text is scrubbed — no raw findings, source, diffs, logs, secrets, or paths.

## Idempotency

`self propose` dedupes by item fingerprint (stored as the ProposedTask
`origin_recommendation_id`); re-proposing the same item creates no duplicate. With
multiple high-priority items it requires `--item-id` or `--top N`.

## Why this is separate

Self-improvement planning is deliberately decoupled from product execution: Remedy
proposes, a human disposes. A future **Self-Dogfood Execution v0** could add a guarded
execution rail — still behind approval, never self-merging.

## See also

- [repair-loop-v1.md](repair-loop-v1.md), [do-continue-v1.md](do-continue-v1.md)
- [provider-trust-gate-v0.md](provider-trust-gate-v0.md), [repair-request-builder-v0.md](repair-request-builder-v0.md)
