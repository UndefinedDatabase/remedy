## What and why

F290 is the sixth rolling findings paydown (operator amendment amend0911-feedback rule B). It took
the seven review findings open at its claim and repaired each by the repair its own text names, one
slice per finding (DECISION F290 D1). The record only stays readable while it also shrinks.

- **R-1117, the one with product effect.** A task inside a job that changed no file is now blocked
  by the job's completion gate with the reason `no_file_changed`, whatever its reviewer answered.
  Three of Remedy's own self-repair runs had recorded such a task as passed. Four test files whose
  fake builders named a file without writing it now write it (DECISION F290 D2; the operator
  confirmed the behaviour change by delegation when answering question Q4, DECISION F290 D5).
- **R-1129.** The cockpit words a refused task edit by the reason the server gave, and says "this
  task changed since you opened it" only when no reason came.
- **R-1128.** The preview end-to-end test draws its command nonce from hexadecimal digits, so it no
  longer fails at random about one run in thirty-two.
- **R-1127.** A test watches the interpreter's own audit events while the test data-root allocator
  makes two roots, and accepts exactly two `os.mkdir` calls and nothing else.
- **R-1125 and R-1133.** Two documentation guards: every README tier row equals the STATUS lines of
  its tier, and every page under `docs/system/` and `docs/guides/` is linked from `docs/README.md`.
- **R-1137.** The eleven test modules F200 added or changed were measured at 39.18 CPU seconds and
  recorded as the price of F200; the rest of that rise was left to this closure's own reading
  (DECISION F290 D3).
- **The closure's self-use item, `SU-044`.** Unlike the three before it, the job changed files: it
  narrowed the excused error handler of the live-UI probe in `remedy dev status` and lowered the
  BLE001 ratchet. It landed as the job wrote it, with two tests through the command line
  (DECISION F290 D4).

## Key decisions

- D1: seven findings, seven slices; R-1127 closed by the interpreter's audit events.
- D2: a job task that changed no file is blocked, whatever its reviewer answered.
- D3: the CPU cost of F200's serve tests is recorded, not cut; the unattributed rest goes to this
  closure's reading.
- D4: `SU-044` lands as its job wrote it, with two command-line tests.
- D6 and D7: main's amendment amend1006-luna-control-plane gave the numbers F295 and F296 to two
  new features while this branch was open, and this branch's closing round had given F295 to the
  seventh findings paydown. On the operator's delegated answer to question Q5, main keeps both
  numbers; this branch merged main and renumbered the paydown F297, placed by the rolling rule in
  main's new order (directly after F199).
- The hardening stage (SLOW MODE): a fresh auditor who saw only the feature file audited nine
  statements and found no gap; six were proved by breaking the code, one of them through a real
  `remedy job run` whose task changed nothing (`.agent/f290_acceptance_audit.md`).

## How to review

1. `docs/roadmap/features/T2_F290.md`, its Task slicing and Built State sections.
2. `packages/orchestration/pingpong_job.py` (`validate_job_task_result`) and
   `tests/orchestration/test_job_task_runner.py` (`TestCompletionGate`).
3. `apps/ui/src/api/taskEditSend.ts` and its test; `apps/cli/commands/dev.py` and the `live_ui`
   tests in `tests/regression/test_named_bugs.py`.
4. The guards in `tests/docs/test_docs_consistency.py` and `tests/test_data_root_isolation.py`.
5. The review record: `.agent/live_review.md` (one `Gate: F290 R<n>` entry per round),
   `.agent/f290_acceptance_audit.md`, `.agent/authored/f290-r5-cpu.txt` and
   `.agent/authored/f290-closure-suite.txt`.
6. The merge of main, `F290 R12 C2`: against `main`, it changes only F290's STATUS line, the
   paydown's line and heading after F199, `docs/roadmap/features/T2_F297.md`, the
   `TOTAL_FEATURES` pin and the README counters.

## Changed files outside `.agent/` (fork point `31542dbfd` to the accepted head)

| Path | +/- |
|---|---|
| `apps/cli/commands/dev.py` | +1/-1 |
| `apps/ui/src/api/taskEditSend.test.ts` | +17/-0 |
| `apps/ui/src/api/taskEditSend.ts` | +15/-11 |
| `docs/agents/planner_reviewer_prompt.md` | +8/-0 |
| `docs/roadmap/STATUS.md` | +1/-1 |
| `docs/roadmap/features/T2_F290.md` | +74/-0 |
| `packages/orchestration/pingpong_job.py` | +8/-1 |
| `scripts/self_use_queue.json` | +8/-0 |
| `tests/docs/test_docs_consistency.py` | +42/-0 |
| `tests/orchestration/test_job_task_runner.py` | +26/-3 |
| `tests/orchestration/test_job_worktree_integration.py` | +7/-4 |
| `tests/orchestration/test_predictive_budget.py` | +8/-9 |
| `tests/orchestration/test_task_injection_runner.py` | +4/-1 |
| `tests/orchestration/test_task_veto_runner.py` | +8/-2 |
| `tests/regression/test_named_bugs.py` | +64/-0 |
| `tests/test_ble001_ratchet.py` | +1/-1 |
| `tests/test_data_root_isolation.py` | +27/-0 |
| `tests/ui_server/test_preview_end_to_end.py` | +1/-1 |

After the accepted head, the closing round registers the next findings paydown (its feature file,
its STATUS line under its own Tier 2 heading, the `TOTAL_FEATURES` pin and the README counters),
then flips F290's STATUS line, syncs `README.md` and sets `SU-044`'s `consumed_by`. Round 12 then
merges `main` and renumbers that paydown F297; everything else after it is under `.agent/`.

## Verdict and evidence

- Latest live review verdict: PASS (round 12, the merge of main; round 13's own verdict is booked in
  the next feature's first commit). The STATUS line reads PASS_WITH_RISKS because two Low findings
  this feature raised stay open with F297.
- The one full suite, run again on the merged tree because the branch moved after its first run
  (amend0921-operator-feedback rule 1): `21311 passed, 22 skipped, 1 warning in 402.78s (0:06:42)`,
  exit 0, no bad node, no leftover process. It used 1048.65 CPU seconds
  (`.agent/authored/f290-closure-suite.txt`); the first run, before the merge, used 1196.01, 21.8
  percent more than F200's 981.70, which finding R-1139 records.
- Evidence job `f290r10e1001`: 997 tests passed. Package
  `remedy-review-20261006-194554-READY_FOR_REVIEW.zip`, SHA-256
  `dd2feaf4fbd473023e119dabf9cd48d4403be4cbb722d4196e10677e8fdea15a`, archived in
  `/home/decodeux/Repos/remedy-history/zips`, accepted head
  `555d8144802f1c3e908862b0d4f16542108ed47e`.
- Open findings: 2, both Low and owned by F297: R-1138 (the reviewer of a run whose builder changed
  nothing is told the code was confirmed correct) and R-1139 (the closure suite's CPU rise).
- Operator questions open: 0 (Q4 and Q5 were answered by the operator by delegation).

## Runtime actuals

- 13 delegated rounds in 6 sessions, from 2026-10-01 to 2026-10-06.
- Planner and reviewer: Claude Opus 5.5; workers: one subagent per round; the hardening auditor:
  one fresh subagent. Tokens and cost of the sessions themselves: not measured.
- The self-use run: 6 provider calls, $1.89, 424 seconds.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
