**What changed.** `remedy do run --rehearse "<order>"` plans what you ask exactly as `remedy do`
does and stops before any job runs: it builds no builder or reviewer, applies nothing and writes
nothing into the repository. Beside each job it writes `rehearsal.json` and a readable
`rehearsal.md`: what the planning cost as the job's prompt trace records it, each task's estimate
band from the shared estimator, the plan's risks, the DoD's checks and which were not compiled,
and which files the run could write and which the fences block. Running the rehearsed plan for
real is approving it and running the job; neither plans again, and both warn when the
repository's commit moved since the rehearsal. `remedy status` labels a waiting rehearsed job.

**Defects found and repaired on the way.** `remedy job run` ran a job whose plan still waited for
approval; it now refuses it with `plan_awaiting_approval` (or `plan_rejected`), exit 3 (R-1317).
A definition-of-done check could pass on another check's application when its own died on a
taken port, found by the closure's serial evidence run; it now fails (R-1320). Two counters the
rehearsal's guarantees read at zero now have tests that show them counting (R-1316, R-1318).

**Key decisions.** DECISION F055 D1: rehearsal is `--plan-only` with its own words, refusals and
counters; the catalog's `do` group moves to its own module first, and edits of the listed
functions in `do_cmd.py` are line-neutral. D2: the record and summary, with no dollar figure the
run did not measure. D3: the real run, the warning, the label, and the approval refusal. D4:
R-1320 moved into F055 and repaired before the closure.

**How to review.** `docs/roadmap/features/T3_F055.md` (Built State), `docs/guides/do-run-v1.md`
(sections "--rehearse", "What a rehearsal records" and "Running a rehearsed plan for real"),
then `packages/orchestration/do_rehearsal.py`, `apps/cli/commands/do_rehearsal_refusals.py`,
`apps/cli/commands/job_run_refusals.py`, the two checks in `packages/orchestration/dod_runners.py`,
`tests/cli/test_rehearsal.py` and `tests/orchestration/test_do_rehearsal.py`, and the `Gate: F055
R1` to `R8` entries in `.agent/live_review.md`. The branch merged nothing in; its fork point is
`eea4f5cfe`.

**Verdict.** Rounds 1 to 8 PASS, booked in the ledger; round 9's verdict is the reviewer's and is
booked in the next feature's first commit. Live review PASS: every finding F055 owned is resolved.

**Open findings.** 40, all owned by the rolling paydown F307 (R-1246, R-1276 to R-1313 and R-1319).

**Local evidence (amend1011-manual-hosted-ci).** Interpreter: Python 3.10.12, `/usr/bin/python3`.
- The one full suite, `python3 -m pytest -n auto -q`, on the repaired tree of `c13b99e15`:
  `23069 passed, 22 skipped, 1 warning in 352.31s`, exit 0 (`.agent/authored/f055-closure-suite.txt`).
- The evidence job `f055r5e1001`, `python3 .agent/authored/f055-r5-create_f055_evidence.py`, on the
  accepted head `c3c6ae7bf958d712b77656e60a6ee9e9c33efe2a`: 8330 passed, 9 skipped, exit 0.
- Review package `remedy-review-20261014-200011-READY_FOR_REVIEW.zip`, SHA-256 `7be134c461b533e26dab8ca02d1f28de90a750c6a18197a9fd549f87529611aa`, in `/home/decodeux/Repos/remedy-history/zips`.

**Runtime actuals.** 9 delegated rounds in one session; wall clock and model tokens not measured
for the rounds themselves; the closure's self-use run used two provider calls and 11577 tokens.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
