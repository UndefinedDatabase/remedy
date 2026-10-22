## F113 — Local models for side roles

**What.** An operator can name local Ollama servers in `local_routing.endpoints` and map side roles
to them in `local_routing.side_roles`. Only the cheap-tier roles — summary, teacher and study — may
be mapped; a table mapping a core role is refused whole with F058's rule
`core_role_on_local_provider` named. A mapped role runs on its endpoint while the endpoint answers
its probe (one per process, held 300 seconds) and no failed spot check stands against it; otherwise
it runs on its own path exactly as before. The summary role's three call sites (the diff summary,
the result tour, the chat answer) follow the route, and a summary records it with the cost basis
`local_zero` or `unknown`. A job's evidence export writes the routed summaries as
`side_role_calls.json` and mirrors them into the ledger's own `side_role_calls` table. A frozen
spot-check set of seeded facts, run with `remedy doctor side-roles --check`, moves a failing role
back to its own model for that endpoint and model; only a passing check an hour later moves it
back. `remedy status` shows where each mapped role runs and why. A project that maps no role sees
no change.

**Why.** Chores such as summaries cost API tokens although a local model can write them; the
existing Ollama paths had no per-role routing, no quality gate and no honest cost basis.

**Key decisions.** DECISIONs F113 D1 to D3 in `.agent/decisions.md`: the endpoint and side-role
tables, `local_never_core` as F058's existing rule, the planner's client as the adapter, and the
four statements of the feature file that were no longer true (D1); the evidence file and a ledger
table of its own, because `token_ledger.py` is held at its row and its `calls` table admits no
`local_zero` (D2); the frozen set, the flip per endpoint and model under the data root, the one-hour
dwell, and the explicit check (D3).

**How to review.** `docs/roadmap/features/T3_F113.md` (slice list and Built State),
`docs/system/local-side-roles-v1.md`, then the round entries `Gate: F113 R1` to `R5` in
`.agent/live_review.md`. The production code is `packages/orchestration/local_endpoints.py`,
`side_role_routing.py`, `side_role_calls.py`, `side_role_quality.py` and
`apps/cli/commands/doctor_side_roles_cmd.py`, with small edits of `artifact_summary.py`,
`result_tour.py` (line-neutral), `chat_answer.py`, `job_evidence.py` (line-neutral),
`config_keys_model_routing.py`, `data_paths.py`, `status_cmd.py`, `apps/cli/commands/__init__.py`
and `apps/cli/command_catalog_doctor.py`. The tests are `tests/orchestration/test_local_endpoints.py`,
`test_side_role_routing.py`, `test_side_role_calls.py`, `test_side_role_quality.py`,
`tests/cli/test_doctor_side_roles_cmd.py` and `tests/regression/test_f113_acceptance.py`. The branch
merged nothing in; its fork point is `3af211790`.

**Changed files.** Six rounds in one session; the review package's manifest lists the 51 files of
the reviewed range.

**Verdict.** Rounds 1 to 5 PASS, booked in the ledger, each verified by the reviewer's dry run with
bytes identical and its mutations red; round 6's verdict is the reviewer's and is booked in the next
feature's first commit. Live review PASS: F113 raised no finding and owns none.

**Open findings.** 7 (R-1246, R-1326, R-1353, R-1418 and R-1421 Low; R-1281 and R-1351 Medium),
owned by F314.

**Local evidence (amend1011-manual-hosted-ci).** Interpreter: Python 3.10.12, `/usr/bin/python3`.
- The one full suite, `python3 -m pytest -n auto -q`, on the tree of `908d30689` (the tree that
  ships but for records): `23353 passed, 11 skipped, 1 warning in 361.64s`, exit 0
  (`.agent/authored/f113-closure-suite.txt`); the cost script read 1.6 percent below F296's.
- The evidence job `f113r5e1001`, `python3 .agent/authored/f113-r5-create_f113_evidence.py`, on the
  accepted head `a61bcfe1b43e0f6069976fbe997eb15578a90cc4`: 11814 passed, 6 skipped, exit 0.
- The closing round's selection over `tests/docs/` and the closure guards, on the final tree:
  recorded in `.agent/handoff.md`.
- Review package `remedy-review-20261022-104538-READY_FOR_REVIEW.zip`, SHA-256
  `402704bec2c9610387f01c056f892a8e1c40aadd045d5a4ef37779bcea5e5104`, in
  `~/Repos/remedy-history/zips`.

**Runtime actuals.** Six delegated rounds, one session; wall clock and model tokens not measured for
the rounds themselves; the closure's self-use run used two provider calls and 3320 tokens.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
