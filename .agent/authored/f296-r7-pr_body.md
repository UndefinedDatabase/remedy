## F296 — Evidence-triggered tier escalation (routing v2)

**What.** A task whose builder keeps failing on a cheaper model tier can now hand its next repair
round to the next tier up, with its reviewer raised alongside, on evidence only: a test run its
execution guard stopped at a limit, two red runs with the same failure (which used to end the
repair), or `model_escalation.after_failures` failing rounds in a row. A provider that cannot be
reached never escalates (that stays F058's failover), a task never steps down, and the run's round,
repair and budget caps still decide whether a round exists. The escalated round's providers are
built fresh and never resume the cheaper model's session. Every escalated call carries its record:
the round entry's `escalation`, the cost booking under the model that served it, the relaunch
session guard, one `remedy run show` line per escalation and the job's `worker.escalated` event. A
run on tier models records its tiers as `tier_ladder`, and the job's evidence export writes
`tier_outcomes.json` per task run, mirrored into the ledger's `tier_outcomes` table, for F133. Off by
default: `model_escalation.enabled` stays `false` until a benchmark shows cheap-first pays (T003's
Amendment, DECISION F296 D5).

**Why.** F110 routes each class to a tier and F058 fails over only on availability; nothing
handed a failing cheap model's work to a stronger one, so it kept failing on the same tier until a
cap ended the job.

**Key decisions.** DECISIONs F296 D1 to D5 in `.agent/decisions.md`: the slice list and
`run_pingpong`'s structural step (1) first (D1); the three keys, the triggers and the loop's two
calls, line-neutral (D2); the record carried on each answer by `EscalatedProvider` (D3); the outcome
per task class and tier as evidence and a ledger table of its own (D4); the default kept off by the
Amendment, because no round of the feature buys thirty paid bench missions (D5).

**How to review.** `docs/roadmap/features/T3_F296.md` (slice list, Amendment and Built State),
`docs/system/tier-escalation-v1.md`, then the round entries `Gate: F296 R1` to `R6` in
`.agent/live_review.md`. The production code is `packages/orchestration/tier_escalation.py`,
`packages/orchestration/tier_outcomes.py` and the line-neutral edits of `pingpong_loop.py`,
`pingpong_job.py`, `job_evidence.py`, `pingpong_call_record.py`, `pingpong_provider_call.py`,
`event_names.py`, `config_keys_model_routing.py` and `apps/cli/commands/run_report_cmd.py`; the
tests are `tests/orchestration/test_tier_escalation.py` and `tests/orchestration/test_tier_outcomes.py`.
The branch merged nothing in; its fork point is `eb7aa432b`.

**Changed files.** Seven rounds in one session; the review package's manifest lists the 47 files
of the reviewed range.

**Verdict.** Rounds 1 to 6 PASS, booked in the ledger, each verified by the reviewer's dry run with
bytes identical and its mutations red; round 7's verdict is the reviewer's and is booked in the
next feature's first commit. Live review PASS_WITH_RISKS: R-1421 carried with an owner.

**Open findings.** 7 (R-1246, R-1326, R-1353, R-1418 and R-1421 Low; R-1281 and R-1351 Medium),
owned by F314.

**Local evidence (amend1011-manual-hosted-ci).** Interpreter: Python 3.10.12, `/usr/bin/python3`.
- The one full suite, `python3 -m pytest -n auto -q`, on the tree of `4e22c749a` (the tree that
  ships but for records and docs): `23248 passed, 11 skipped, 1 warning in 380.20s`, exit 0
  (`.agent/authored/f296-closure-suite.txt`); the cost script read 12.0 percent above F307's,
  registered as R-1421.
- The evidence job `f296r6e1001`, `python3 .agent/authored/f296-r6-create_f296_evidence.py`, on
  the accepted head `0143b9e17e05e2626602830340b25fef55479b04`: 11586 passed, 6 skipped, exit 0.
- The closing round's selection over `tests/docs/` and the closure guards, on the final tree:
  recorded in `.agent/handoff.md`.
- Review package `remedy-review-20261022-085320-READY_FOR_REVIEW.zip`, SHA-256
  `cc616314ffef4d468e3dcfa497b55011ec6b129005fead9927778f05f410fbe5`, in
  `~/Repos/remedy-history/zips`.

**Runtime actuals.** Seven delegated rounds, one session; wall clock and model tokens not measured
for the rounds themselves; the closure's self-use run used two provider calls and 3604 tokens.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
