## F311 — The insight: what runs now, what the worker does, why it hangs

### What changed
- **The worker pulse and the reader (T001).** `packages/orchestration/worker_pulse.py` keeps
  `worker_pulse.json` in a job's folder: the running call's role, provider, model, round and kind,
  the time of the worker's last output, and its last 200 stream entries, redacted and cut to 200
  characters. Every run of a job starts a fresh pulse (`pi_provider.bind_job_clock`); every Pi call
  records its start and end and feeds each parsed stream record through `PiLoopWatch`'s new
  `on_record`, writing at most once per two seconds. `packages/orchestration/job_insight.py` builds
  both answers from the job record, the pulse, the budget actuals and limits, the order and the open
  decision; `client_story.job_story_open_decision` and `budget_stop.budget_work_seconds` became
  public for it.
- **The stall reading (T002).** `phase`, `stalled`, `stall_reason` and `advice` in closed words; the
  threshold `insight.stall_seconds` (default 300, `REMEDY_INSIGHT_STALL_SECONDS`); one Ollama probe
  per answer through `/api/tags` and `/api/ps`.
- **The routes and twins (T003).** `GET /api/v1/now` (`remedy client now --json`) and
  `GET /api/v1/jobs/{job}/insight` (`remedy client insight <job> --json --lines <n>`); a client
  token reads `now` filtered to its projects and is refused another project's insight with 403. The
  interface gains one key, `insight`, with every word. `DIGEST_KEY_TREE` moved to
  `apps/cli/client_interface_digest.py` to keep `client_interface.py` under the file limit. The
  guide `docs/guides/http-clients.md` has a section on both routes.
- **The proof (T004).** `test_worker_pulse.py`, `test_job_insight.py`, `test_client_insight_cmd.py`,
  and the route tests in `test_public_api.py` and `test_public_api_client_scope.py`.

### Why
In the operator's third lab run of 2026-10-20 the Orb saw a stop and two notifications but not that
the builder was in its twelfth model turn with 78,696 tokens spent: nothing in Remedy's HTTP API
said what runs now or why it hangs.

### Key decisions
DECISIONs F311 D1 to D7 in `.agent/decisions.md`. D1: one job-entry shape for both answers, and the
twins live in the `client` group beside the story. D2: the pulse is a file of its own, written by
Pi calls only; other providers read `unknown` and `unmeasured`. D3 and its two addenda: the phase,
the stall reasons in order, the advice; `apply_wait` is read from the job's own result. D4: the
model server's `queue` and the free workers read null, because nothing can say them. D5: one
interface key `insight`. D6: the routes are listed `since 1.21` until F313 raises the version. D7:
no ledger rotation in this closure (R-1376, owned by F307). Operator question Q21 records D1, D2 and
D4's visible choices, with the recommendation already executed.

### How to review and test
Read `docs/roadmap/features/T12_F311.md` (Built State) and the round entries in
`.agent/live_review.md`. Every round's selection was re-run by the reviewer, and every production
change was mutation-proven in a disposable worktree. The closure's one full suite:
`python3 -m pytest -n auto -q` → `22092 passed, 11 skipped` on `8e0b5c5da`
(`.agent/authored/f311-closure-suite.txt`), 1.2 percent more CPU time than F312's.

### Evidence
- Evidence job `f311r6e1001` (9539 passed, 0 failed); package
  `remedy-review-20261021-041253-READY_FOR_REVIEW.zip`, SHA-256
  `ce16ffda6c47e2f361c8efc2fe012a46c7f167a2f05fe26feafc5757d2871d57`, in
  `~/Repos/remedy-history/zips`; accepted head `a71cb79ac8bad33355a0e5862c9a07dbc2e48b25`.
- Self-use item SU-067, narrowing an excused error handler of `remedy status`, ran to its approval
  gate through `claude-cli`, passed review and was never applied.

### Verdict and findings
Live review PASS_WITH_RISKS: the integrity check fails only on twelve High findings F311 does not
own (DECISION F310 D7). Resolved inside the feature: R-1383 to R-1389. Open: 87 findings by the
ledger's reader; F311 owns none.

### Runtime actuals
One session, seven delegated rounds; reviewer Claude Opus 5.5, workers Claude Sonnet 5; tokens and
cost of the session: not-measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
