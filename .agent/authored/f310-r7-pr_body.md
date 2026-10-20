## F310 — Budgets that fit the provider, and one stop, one question

### What changed
- **Profiles per provider class (T001).** A job is `local` when every role runs on a model Ollama
  serves on this machine, `paid` otherwise. A run reads its limits as the job's own budgets, then
  the configured `budget.*` values, then its class's profile (`budget.profile.local.*`: 1,500,000
  tokens, 200 calls, 480 minutes; `budget.profile.paid.*`: unset). No profile value is written into
  a job's record. A task plan's suggested budgets are no longer limits (`apply_plan_budgets`
  deleted). `GET /api/v1/execution` and `remedy client execution` name both profiles and each
  provider's class. The registry's budget keys moved to `config_keys_budget.py`.
- **The working wall clock (T002).** `budget_actuals` is version 3.0.0 with `waited_s` and
  `active_until`; every gap between two runs of a job counts as waiting, and the guard, the Pi
  call's time bound and the persisted counters measure work alone.
- **One stop, one question (T003).** The budget decision names the mission's open blocking criteria
  under `blockers`; `extend` without an answer doubles every limit the stop exhausted (the wall
  clock to at least 60 minutes); answers are checked against the limits the run read; over the
  public API the run resumes by itself (`resumed`). The walk's raise of the remainder decision at
  a budget stop is deleted; an `abandon` raises it once, and a cancelled job still lists its
  mission's remainder question.
- **The proof (T004).** The lab stop of 2026-10-20 is rebuilt as a test; the budget page describes
  all of it.

### Why
The operator's lab runs of 2026-10-20 with Pi over a local model: a 9-minute wall clock ended
normal work, the time spent waiting for an answer counted as work, and one budget stop asked two
questions (findings R-1370 and R-1371).

### Key decisions
DECISIONs F310 D1 to D8 in `.agent/decisions.md`. D3: an order's own caps stay the client's, so the
Orb must send the profile's numbers, which the execution offer now names (operator question Q19).
D7: the closure reads the integrity check as met while it fails only on thirteen High findings
F310 does not own; finding R-1375, owned by F307, books them (operator question Q20). D8: the
ledger is not rotated in this closure, because the commit hook's agent-state check refuses a
rotation that moves a record holding a path of this machine (finding R-1376, owned by F307).

### How to review and test
Read `docs/roadmap/features/T12_F310.md` (Built State) and the round entries in
`.agent/live_review.md`. Every round's selection was re-run by the reviewer, and every production
change was mutation-proven in a disposable worktree. The closure's one full suite:
`python3 -m pytest -n auto -q` → `21989 passed, 11 skipped` on `cc9a109e6`
(`.agent/authored/f310-closure-suite.txt`).

### Evidence
- Evidence job `f310r6e1001` (8749 passed, 0 failed); package
  `remedy-review-20261020-215917-READY_FOR_REVIEW.zip`, SHA-256
  `3e9da10ccd0289b57d036534442b6abedcf480b09bc729f1f00f05d91b4db056`, in
  `~/Repos/remedy-history/zips`; accepted head `899850b8dd6867d7d9683fb506bc0574454a7505`.
- Self-use item SU-065 ran to its approval gate through `claude-cli` and was never applied.

### Verdict and findings
Live review PASS_WITH_RISKS. Resolved: R-1370, R-1371, R-1372, R-1373, R-1374. Open: 87 findings
by the ledger's reader, R-1375 and R-1376 among them, both owned by F307.

### Runtime actuals
One session, seven delegated rounds; reviewer Claude Opus 5.5, workers Claude Sonnet 5.5; tokens
and cost of the session: not-measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
