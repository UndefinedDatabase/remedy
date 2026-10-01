## What and why

F200 gives Remedy a long-lived supervisor, `remedy serve`, so that one process per data root can
own the jobs it runs, answer the command line while it runs, and run its jobs again after a crash
or a restart. Before this feature every command line call was its own short process and nothing
outlived it. Running without a supervisor stays fully supported: with no supervisor answering,
every command runs directly, exactly as before.

- **The supervisor.** `remedy serve start` runs it in the foreground; `remedy serve status` reports
  whether it runs and `remedy serve stop` stops it. Its socket, process id file, token file and run
  registry live in a new data-root class, `serve`, readable by their owner only. The socket is
  answered by the cockpit's own request handler, so every command sent over it passes the same
  checks as one sent from the cockpit and is recorded with the source `cli` (DECISIONs F200 D1, D2).
- **Client mode.** While a supervisor answers, `remedy job stop`, `remedy job pause` and
  `remedy job unpause` send their one write to it and print what they print without it, and a plain
  `remedy job run <job>` hands the job to the supervisor and follows its output to the end. Every
  other command runs directly in both modes (D3, D4, D5).
- **Restart.** On every start the supervisor settles the runs its registry still holds: a run whose
  process still runs is adopted, a job whose record still reads `running` is run again, and any
  other run is recorded as ended. A test kills a real supervisor and its run with SIGKILL, starts a
  new one, and finds every task run exactly once (D7).
- **Shipping.** `scripts/serve/remedy-serve.service` is a systemd user unit and
  `scripts/serve/container-entrypoint.sh` a container entrypoint; `docs/system/serve-daemon-v1.md`
  describes the built supervisor (D8).
- **Not built, by D1.** A scheduler that runs several jobs from a waiting line, a cockpit inside the
  supervisor, notification and audit-export workers, and a client channel over a network port.

## Key decisions

- D1 to D5 and D7 to D8 build the feature; D6 records that the operator, asked, confirmed the
  smaller design.
- D9 records the hardening stage (SLOW MODE): a fresh auditor tried to break each of twenty
  statements of the feature file; seventeen had a test that turned red at once, and the three gaps,
  a STOP request for a supervised run, the advice to run the container with an init process, and
  the limit of client mode to its four commands, each got a test that a second auditor proved.
- D10: the closure's self-use item, `SU-043`, ran to its approval gate, but Remedy's builder changed
  no file and its reviewer still passed the task. That is the defect finding R-1117 already records,
  so it was booked as R-1117's recurrence, nothing of the item was landed, and the item is consumed
  by F200.

## How to review

1. `docs/roadmap/features/T12_F200.md`, its Amendment and Built State sections first, and
   `docs/system/serve-daemon-v1.md`.
2. The supervisor: `packages/orchestration/serve_paths.py`, `packages/orchestration/serve_daemon.py`
   and `packages/orchestration/serve_runs.py`, and the handler change in
   `packages/orchestration/ui_server.py`.
3. The command line: `apps/cli/commands/serve_cmd.py`, `apps/cli/serve_client.py`, and the client
   paths in `apps/cli/commands/job_stop_cmd.py`, `apps/cli/commands/job_pause_cmd.py` and
   `apps/cli/commands/do_cmd.py`.
4. The tests: `tests/cli/test_serve_client_parity.py` (every forwarded command in both modes),
   `tests/orchestration/test_serve_restart_kill.py` (the SIGKILL restart) and
   `tests/orchestration/test_serve_stop_file.py`.
5. The review record: `.agent/live_review.md` (one `Gate: F200 R<n>` entry per round),
   `.agent/f200_acceptance_audit.md`, `.agent/f200_acceptance_reaudit1.md` and
   `.agent/authored/f200-closure-suite.txt`.

## Changed files outside `.agent/` (fork point `959b88a85` to the accepted head)

| Path | +/- |
|---|---|
| `apps/cli/command_catalog.py` | +35/-0 |
| `apps/cli/commands/__init__.py` | +2/-1 |
| `apps/cli/commands/do_cmd.py` | +20/-0 |
| `apps/cli/commands/job_pause_cmd.py` | +30/-5 |
| `apps/cli/commands/job_stop_cmd.py` | +34/-7 |
| `apps/cli/commands/serve_cmd.py` | +71/-0 |
| `apps/cli/serve_client.py` | +135/-0 |
| `docs/README.md` | +2/-0 |
| `docs/agents/planner_reviewer_prompt.md` | +14/-0 |
| `docs/guides/environment.md` | +2/-0 |
| `docs/roadmap/STATUS.md` | +1/-1 |
| `docs/roadmap/features/T12_F200.md` | +125/-0 |
| `docs/system/serve-daemon-v1.md` | +191/-0 |
| `packages/orchestration/config.py` | +24/-0 |
| `packages/orchestration/data_paths.py` | +3/-0 |
| `packages/orchestration/pause_control.py` | +27/-19 |
| `packages/orchestration/serve_daemon.py` | +285/-0 |
| `packages/orchestration/serve_paths.py` | +62/-0 |
| `packages/orchestration/serve_runs.py` | +313/-0 |
| `packages/orchestration/ui_server.py` | +40/-3 |
| `scripts/self_use_queue.json` | +8/-0 |
| `scripts/serve/container-entrypoint.sh` | +29/-0 |
| `scripts/serve/remedy-serve.service` | +42/-0 |
| `tests/cli/test_cli_ux.py` | +4/-4 |
| `tests/cli/test_exit_codes.py` | +8/-0 |
| `tests/cli/test_serve_client_parity.py` | +401/-0 |
| `tests/cli/test_serve_client_scope.py` | +110/-0 |
| `tests/cli/test_serve_cmd.py` | +91/-0 |
| `tests/orchestration/import_reachability_allowlist.txt` | +5/-0 |
| `tests/orchestration/test_serve_artifacts.py` | +190/-0 |
| `tests/orchestration/test_serve_daemon.py` | +287/-0 |
| `tests/orchestration/test_serve_paths.py` | +63/-0 |
| `tests/orchestration/test_serve_restart_kill.py` | +245/-0 |
| `tests/orchestration/test_serve_runs.py` | +348/-0 |
| `tests/orchestration/test_serve_stop_file.py` | +360/-0 |

After the accepted head, the closing commit flips F200's STATUS line, syncs `README.md` and sets
`SU-043`'s `consumed_by`; everything else after it is under `.agent/`.

## Verdict and evidence

- Latest live review verdict: PASS (round 13, the evidence round; the closing round's own verdict is
  booked in the next feature's first commit). The STATUS line reads PASS_WITH_RISKS because two
  findings F200 raised stay open with the next findings paydown.
- The one full suite: `21303 passed, 22 skipped`, exit 0, no bad node and no leftover process,
  981.70 CPU seconds, 13.8 percent more than F292's; finding R-1137 records that cost
  (`.agent/authored/f200-closure-suite.txt`).
- Evidence job `f200r13e1001`: 1537 tests passed. Package
  `remedy-review-20261001-153207-READY_FOR_REVIEW.zip`, SHA-256
  `97fa32a252c2e4476e49cf958a37c98e68108e30f180805c681ae4f297b29bda`, archived in
  `/home/decodeux/Repos/remedy-history/zips`, accepted head
  `f96507e803f7295f1e7727905b3ddd99f2669788`.
- Open findings: 7, none owned by F200: R-1117 (Medium), R-1125, R-1127, R-1128, R-1129, R-1133 and
  R-1137 (Low), all owned by F290, the next findings paydown.

## Runtime actuals

- 14 delegated rounds in 3 sessions, all on 2026-10-01, from 10:48 to about 15:45 local time.
- Planner and reviewer: Claude Opus 5.5; workers: one subagent per round. Tokens and cost of the
  sessions themselves: not measured.
- The self-use run: 4 provider calls, $0.80, 111 seconds.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
