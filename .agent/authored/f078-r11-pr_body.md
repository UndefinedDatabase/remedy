## F078 — Autonomy levels

### What changed
- **The level and its one check (T001).** `packages/orchestration/autonomy_gate.py` holds the
  levels `L2` to `L5`, the sixteen-cell `AUTONOMY_START_MATRIX` over the origins `manual`,
  `orchestrator`, `order-file` and `idea`, and `autonomy_may_start`. `load_autonomy_policy` reads
  `autonomy.level`, `autonomy.gauntlet_evidence` and `autonomy.change_adr` from `remedy.toml` only,
  refuses `L3` and higher without a gauntlet matrix that passed and every change of level without
  its decision record, and records each accepted change.
- **The seams (T002).** `remedy mission run` grants one manual start, and `dispatch_milestone_job`
  asks the check before any job exists: at the default `L2` a run starts one job and ends
  `deferred_by_autonomy`, each waiting start recorded until the next run takes it; from `L3` the
  loop runs as before. The operator's own commands do not ask: every level allows them.
- **Showing the level and the caps of L5 (T003).** `remedy status` ends with the level and any start
  that waits and answers `autonomy`; `remedy mission run` prints and answers its level.
  `claim_idea_start` asks the matrix and the three caps of `L5` for the idea engine to come.
- **Proof.** `tests/orchestration/test_autonomy_levels.py` loads each level from a real
  `remedy.toml` and drives both seams, and re-runs the tests of the watchdog's pause, the iteration
  limit, the operator's stop, the escalation after two blocked completions and the audited approval
  of a waiting plan inside a start scope at `L5`, each still firing.
- **Contract 1.23.** The status answer's new key `autonomy` makes both versions `1.23`, with its
  entry in the release matrix.
- **Structure.** `config.py`'s watchdog keys moved to `config_keys_autonomy.py` (step 7) and
  `_cmd_status`'s text lines to `_print_status_text` (step 3), each row and pin lowered.
- **Repairs found on the way.** The autonomy records' names joined the event vocabulary (R-1393);
  the review package now reads a merge commit against its first parent, so a branch that merges
  work from before its base can be packaged at all (R-1394,
  `packages/orchestration/review_subject.py`).

### Why
Autonomy becomes one auditable dial instead of scattered flags: a configured level states who may
START work on Remedy's own initiative, while every approval, fence, budget and watchdog applies
unchanged at every level (`docs/roadmap/features/T3_F078.md`).

### Key decisions
DECISIONs F078 D1 to D9 in `.agent/decisions.md`. D1 to D3: the keys and the matrix, the mission
loop's starts, the level shown and the caps of `L5`. D4: session 1's branch fell behind `main` and
the commit hook's agent-state check refused merging `main` into it, so this branch is made from
`main` and its first commit merges the first one, with this machine's paths removed from that
branch's three block copies and its handoff; two numbers that collided are told apart (F078's
R-1321, and its open question renumbered Q22). D5: the proof per level and at `L5`. D6: contract
1.23. D7: the three record names declared. D8: the review package reads a merge against its first
parent. D9: no ledger rotation in this closure (R-1376, owned by F307). The first branch
`feature/f078-autonomy-levels` stays on the remote; it may be deleted.

### How to review and test
Read `docs/roadmap/features/T3_F078.md` (Built State), `docs/system/autonomy-levels-v1.md` and the
round entries in `.agent/live_review.md`. Every file of session 2's rounds was prepared by the
reviewer in a disposable worktree and applied byte for byte, and every production change was
mutation-proven there. The closure's one full suite: `python3 -m pytest -n auto -q` →
`22190 passed, 11 skipped` on `25f0a4135` (`.agent/authored/f078-closure-suite.txt`), 1.8 percent
more CPU time than F313's, within its limit.

### Evidence
- Evidence job `f078r10e1001` (10064 passed, 0 failed); package
  `remedy-review-20261021-080416-READY_FOR_REVIEW.zip`, SHA-256
  `954c7dd0df514ddb72e534dd85b5f893fa1e5a0c762850f1e30b630c8459a6da`, in
  `~/Repos/remedy-history/zips`; accepted head `a1f56d46701274ccda6a8b2431967a9160417f48`.
- Self-use item SU-069, narrowing an excused error handler of the worker facade command, ran to its
  approval gate through the `self_use` role's provider, passed review and was never applied.

### Verdict and findings
Live review PASS_WITH_RISKS: the integrity check fails only on twelve High findings F078 does not
own (DECISION F310 D7). Resolved inside the feature: R-1321 (F078), R-1391, R-1392, R-1393 and
R-1394. Open: 87 findings by the ledger's reader; F078 owns none. One operator question is F078's,
Q22, already answered with the session's recommendation.

### Runtime actuals
Two sessions: three delegated rounds on 2026-10-14 and eight on 2026-10-21; reviewer Claude Opus
5.5, workers Claude Sonnet; tokens and cost of the sessions: not-measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
