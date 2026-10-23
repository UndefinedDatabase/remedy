## F133 — Provider trust score

**What.** `packages/orchestration/model_trust_score.py` is the one trust home. Read-only on the cost
ledger, the job records and each task run's provider evidence, it measures per model and role inside
a rolling window: the pass quota and the repair need over settled tasks, the format-error rate over
calls (a call followed by a parse retry, or the last call of a role whose task run holds a parse
post-mortem) and the cost per pass with its basis label, each carried with its sample size. A call's
model is the ledger's verified one when present, else its own provider attempt's; a call that joins
to neither is counted as unattributed. Rows below the sample floor are thin and never lead. The
table is cached as `model_trust_snapshot.json` beside the ledger. `remedy stats trust [--role]
[--project] [--json]` shows the matrix with `n` and the window on every figure, the change against
the prior window, and one recommendation line per role; `remedy job plan-show` prints an
informational "Trust suggests otherwise" note when a job's configured model is outranked by a clear
leader, and changes nothing. Three settings: `model_routing.trust_window_days`,
`model_routing.trust_sample_floor`, `model_routing.trust_snapshot_max_age_seconds`.

**Why.** Which model earns which work should be a queryable fact from Remedy's own history, offered
to a person as a recommendation; routing changes stay config plus an ADR.

**Key decisions.** DECISIONs F133 D1 to D4 in `.agent/decisions.md`: the provider-trust pair the
feature file names was deleted at `0242c0a3b` and never measured a model, so the home is a new
module (D1); the model of a call comes from its own provider attempt because the ledger's model
column is empty on every real row, the four metrics and the settled-task rule (D2); the clear leader
leads by at least ten points, the cost basis is read from the ledger, and no per-tier summary,
because `query_tier_outcomes` writes on open and keeps no window (D3); the routing note lives in the
plan view, never in the resolver, and the plan view's JSON is unchanged (D4).

**How to review.** `docs/roadmap/features/T7_F133.md` (slice list and Built State),
`docs/system/model-trust-score-v1.md`, `.agent/f133_inventory.md`, then the round entries
`Gate: F133 R1` to `R6` in `.agent/live_review.md` (moved to the archive by the closing rotation where
the rotation rules say so). Production code: `packages/orchestration/model_trust_score.py`,
`apps/cli/commands/stats_trust_cmd.py`, the note's caller in `apps/cli/commands/job_plan_cmd.py`, the
three settings in `packages/orchestration/config_keys_model_routing.py`, and the registrations in
`apps/cli/command_catalog_stats.py` and `apps/cli/commands/__init__.py`. Tests:
`tests/orchestration/test_model_trust_score.py` (goldens on a constructed history, the one-home
guard), `tests/cli/test_stats_trust_cmd.py`, the trust-note classes in `tests/cli/test_job_plan_cmd.py`
and `tests/regression/test_f133_acceptance.py`. The branch merged nothing in; its fork point is
`11fda065b`.

**Changed files.** Seven rounds in one session; the review package's manifest lists the reviewed
range of 32 commits.

**Verdict.** Round 1 PASS; rounds 2 to 4 FAIL on Low findings the reviewer's mutation runs and
reading found (R-1429 to R-1434), each repaired and resolved in the next round with its red-proof;
rounds 5 and 6 PASS. Round 7's verdict is the reviewer's and is booked in the next feature's first
commit. Live review PASS: every finding F133 raised is resolved, and it owns no open finding.

**Open findings.** 11 (R-1246, R-1281, R-1326, R-1351, R-1353, R-1418, R-1421, R-1425, R-1426,
R-1427 and R-1428), all owned by F314.

**Local evidence (amend1011-manual-hosted-ci).** Interpreter: Python 3.10.12, `/usr/bin/python3`.
- The one full suite, `python3 -m pytest -n auto -q`, on the tree of `fda9e0d89` (the tree that
  ships but for records): `23494 passed, 11 skipped, 1 warning in 369.40s`, exit 0
  (`.agent/authored/f133-closure-suite.txt`); the cost script read 5.0 percent above F074's, within
  the 10 percent limit.
- The evidence job `f133r6e1001`, `python3 .agent/authored/f133-r6-create_f133_evidence.py`, on the
  accepted head `74e60a86c8fcdddc780bf9d172883489e0605ce3`: 12360 passed, 6 skipped, exit 0.
- The closing round's selection over `tests/docs/` and the closure guards, on the final tree:
  recorded in `.agent/handoff.md`.
- Review package `remedy-review-20261023-145010-READY_FOR_REVIEW.zip`, SHA-256
  `eea6f24c275d5f09d8434e4e05c6f64dc5f7c72bf0f7f8c1cbd47c181855a8dc`, in
  `~/Repos/remedy-history/zips`.

**Runtime actuals.** Seven delegated rounds, one session, the branch's commits from 11:45 to the
closing round on 2026-10-23; model tokens of the rounds themselves not measured; the closure's
self-use run used two provider calls and 2724 tokens.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
