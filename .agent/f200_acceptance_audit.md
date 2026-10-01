# F200 (daemon mode, `remedy serve`) — Acceptance Audit (amend0930b-slow-cap hardening stage)

## What was read, what was not, and how this was run

Read in full: `docs/roadmap/features/T12_F200.md` (original Design/Task slicing/Acceptance, "Amendment — DECISION F200 D1", and the later D4/D5/D7/D8 amendment paragraphs — the amendment governs wherever it disagrees with earlier text, as the file itself says); the F200 line of `docs/roadmap/ROADMAP.md` (Tier 12 — the only Goal & Done text; there is no separate Done bullet list for F200); the amend0930b-slow-cap paragraph of `docs/agents/self_drive_protocol.md`; `AGENTS.md`; `git log --oneline 959b88a85..HEAD` and `git diff --stat 959b88a85..HEAD -- packages apps tests scripts docs/system`; and the production/test files: `packages/orchestration/serve_daemon.py`, `serve_paths.py`, `serve_runs.py`, `pause_control.py`, `ui_server.py` (socket handler, nonce, command-exposure call sites), `apps/cli/serve_client.py`, `apps/cli/commands/{serve_cmd,job_stop_cmd,job_pause_cmd,do_cmd}.py`, `scripts/serve/remedy-serve.service`, `scripts/serve/container-entrypoint.sh`, `packages/orchestration/safe_points.py`, `packages/orchestration/command_nonce.py`, and every `tests/orchestration/test_serve_*.py` / `tests/cli/test_serve_*.py`. Not read, per instructions: `.agent/handoff.md`, `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`, `.agent/decisions.md`, `.agent/prose_slips.md`, anything under `.agent/authored/`, any `.remedy-wt/f200-*` directory other than this audit's own scratch.

Worktree: `git -C /home/decodeux/Repos/remedy worktree add --detach .../f200-audit-wt HEAD`, at commit `c820db28a` (tip of `feature/f200-daemon-mode`), with `apps/ui/dist` copied in. Every test/mutation ran with cwd = that worktree; the primary checkout's `git status --porcelain` was empty before and after. The first test run passed immediately (no "UI not built" retry needed). Every pytest call used `python3 -B -m pytest <selection> -q -n auto -p no:cacheprovider`, one selection at a time, never the full suite. Every mutation was applied inside the disposable worktree only, shown red, then restored byte-identical and shown green. No production code or test was modified in either the primary checkout or left behind in the worktree (now removed).

**Total claims audited: 20. Proven at once: 17. Gaps: 3.**

### Claim 1 — "`remedy serve start` creates the socket and the token file readable by their owner only ... and writes the process id file"
Code: `serve_daemon.run_supervisor` → `_write_private` (0600) for token/pid files, `os.chmod(paths.socket, 0o600)`, `paths.root` at 0700. Test: `tests/orchestration/test_serve_daemon.py::test_its_directory_socket_and_token_are_readable_by_their_owner_only`. Mutation: `os.fchmod(fd, 0o600)` → `0o644`. Red: `assert _mode(paths.token_file) == 0o600` → `420 == 384`, 1 failed in 1.30s. Restored byte-identical; green: 1 passed in 1.26s. **PROVEN.**

### Claim 2 — "`remedy serve status` reports whether it runs"
Code: `supervisor_state` / `_cmd_serve_status`. Test (real CLI subprocess, `python3 -m apps.cli.main serve start/status --json` under `REMEDY_DATA_DIR`): `tests/cli/test_serve_cmd.py::test_start_status_stop_runs_one_supervisor_and_cleans_up_after_it`. Mutation: `running = socket_answers(paths.socket)` → `running = False`. Red: `(False, None) == (True, 968676)`, 1 failed, 2 passed in 1.03s. Restored byte-identical; green: 3 passed in 1.33s. **PROVEN (command-line proof).**

### Claim 3 — "`remedy serve stop` stops it and removes the socket and the process id file"
Same test as Claim 2. Mutation: dropped `paths.pid_file` from the cleanup tuple. Red: `assert not paths.pid_file.exists()` failed, 1 failed in 1.35s. Restored byte-identical; green: 1 passed in 1.32s. **PROVEN (command-line proof).**

### Claim 4 — "An envelope sent to the socket passes the cockpit door's checks and applies the same effect, recorded with source `cli`"
Test: `test_a_stop_envelope_on_the_socket_is_recorded_with_the_command_lines_source`. Mutation: `effect_source = SOCKET_EFFECT_SOURCE` → `"wrong"`. Red: `'wrong' == 'cli'` failed, 1 failed in 1.19s. Restored byte-identical; green: 1 passed in 1.20s. **PROVEN.**

### Claim 5 — "a command the socket does not accept is refused as the door refuses"
Test: `test_a_command_the_door_does_not_expose_is_refused_as_the_door_refuses_it`. Mutation: `_command_is_ui_exposed`'s fallback → `return True`. Red: expected 400, got 501, 1 failed in 1.18s. Restored byte-identical; green: 1 passed in 1.19s. **PROVEN.**

### Claim 6 — "every forwarded command prints the same output, exits with the same code and leaves the same effect on disk as in direct mode; one test module runs each of them in both modes"
Test module: `tests/cli/test_serve_client_parity.py` (10 stop/pause/unpause scenarios + 2 job-run scenarios, each run direct and client). Mutation: `job_stop_cmd.py`'s forwarded `reason` replaced with `"mutated"`. Red: exactly the 4 scenarios that call `job stop` failed, 23 others stayed green — `4 failed, 23 passed in 6.00s`. Restored byte-identical; green: 27 passed in 4.29s. **PROVEN.**

### Claim 7 — "Without a socket every command runs direct, exactly as before" (= ROADMAP's "direct mode staying first-class")
Test: `test_the_direct_variable_keeps_a_command_direct_while_a_supervisor_answers`. Mutation: disabled the `DIRECT_ENV` early-return. Red: `['accepted'] == []` failed, 1 failed in 1.24s. Restored byte-identical; green: 1 passed in 1.17s. **PROVEN.**

### Claim 8 — "two distinct nonces apply once each"
Test: parity's `stop-twice` scenario. Mutation: `secrets.token_hex(8)` → fixed string, colliding two distinct requests onto one nonce. Red: second request answered `"replayed"` instead of `"accepted"`, 1 failed in 1.34s. Restored byte-identical; green: 1 passed in 1.32s. **PROVEN.**

### Claim 9 — "a repeated nonce is refused as a replay"
Test: `test_a_repeated_run_nonce_answers_the_first_run_and_starts_no_second`. Mutation: `_replayed_command_result` → `return None`. Red: second identical `job.run` now re-executed and hit `409` instead of being answered from cache, 1 failed, 1 passed in 1.23s. Restored byte-identical; green: 2 passed in 1.23s. **Caveat**: the sibling `job.stop` test (`test_a_repeated_nonce_is_answered_from_the_record...`) stayed **green** under this same mutation, because `safe_points.request_stop`'s own independent create-only dedup (F011) reproduces the same idempotency regardless of the nonce store — it doesn't isolate the nonce mechanism for `job.stop`. The claim is still **PROVEN** via the `job.run` node id.

### Claim 10 — "a second `job run` of a job the supervisor runs is refused"
Test: `test_a_second_run_of_a_job_still_running_is_refused_with_its_reason`. Mutation: disabled `RunLauncher.start`'s running-child guard. Red: `409` expected, got `200`, 1 failed in 1.19s. Restored byte-identical; green: 1 passed in 1.19s. **PROVEN.**

### Claim 11 — SIGKILL restart resumes every registered running job, each task executed once, all green
Test: `tests/orchestration/test_serve_restart_kill.py::test_restart_after_sigkill_resumes_the_job_with_each_task_executed_exactly_once` — two real processes (supervisor + its spawned run) are SIGKILLed, a second supervisor restarts and resumes, cycle-evidence files on disk are checked. Mutation: disabled the `resume_registered` restart branch. Red: timed out waiting for the resumed run's end, 1 failed in 31.03s. Restored byte-identical; green: 1 passed in 1.41s. **PROVEN** (genuine multi-process scenario).

### Claim 12 — "A STOP file (F011) stops a run the supervisor started, exactly as it stops a direct run"
**GAP — no test.** F011's STOP file is `safe_points.py`'s `stop.json`; a supervisor-started run is `remedy job run <job>` as a child process running the identical `pingpong_job.run_job`/`long_run_executor.run_cycles`/`stop_requested()` loop a direct run uses, so by code reading the product likely meets this. But no test anywhere starts a real, long-running job through the supervisor and then sends it a stop (direct or forwarded) to confirm it actually halts at a safe point and the job persists `stopped`. Searched every test touching `RunLauncher`/`run_supervisor`/`post_command` for any "stop" reference (`test_serve_daemon.py`, `test_serve_restart_kill.py`, `tests/ui_server/test_command_channel.py`) — none combines a real running supervised job with an actual stop. The existing socket-stop test only checks the control file's bytes, never a consuming process; the restart-kill test uses SIGKILL, a different mechanism entirely. No mutation could be run against a nonexistent test.

### Claim 13 (D5) — job-run forwarding rules: plain/`--json` forwards; other option/unknown-job runs direct; follows to the end and exits with its code
Four sub-mutations against `tests/cli/test_serve_client_parity.py`, each red then green-restored:
- `_plain` forced False → `test_a_plain_job_run_prints_and_exits_as_it_does_direct[text]`/`[json]`: 2 failed in 2.42s → 2 passed in 3.06s.
- `max_rounds` dropped from the "no options" check → `test_a_job_run_with_an_option_runs_direct_while_a_supervisor_answers`: 1 failed in 3.29s → 1 passed in 2.79s.
- `_recorded is not None` check dropped → `test_a_job_run_of_a_job_this_root_does_not_hold_runs_direct`: 1 failed in 1.37s → 1 passed in 1.29s.
- `sys.exit(code)` disabled → `test_the_followed_runs_exit_code_is_the_commands_own`: 1 failed in 2.12s → 1 passed in 1.84s.
All restores byte-identical. **PROVEN** (all four sub-clauses).

### Claim 14 (D7) — adopt/restart/lost reconciliation at supervisor start
Tests: `test_resume_registered_adopts_a_still_running_process_and_refuses_a_second_start`, `test_resume_registered_restarts_a_job_whose_own_record_still_reads_running`. Two mutations (disabling the adopt condition, then the restart condition) each degraded the outcome to `"lost"`; both 1 failed → 1 passed, byte-identical restores. **PROVEN** (also end-to-end under real SIGKILL via Claim 11).

### Claim 15 (D8, systemd) — user unit, restarts on failure, stops only the supervisor
Tests: `tests/orchestration/test_serve_artifacts.py`. Mutations: `KillMode=process`→`control-group` (1 failed, 10 passed in 0.70s → 11 passed in 0.70s), `Restart=on-failure`→`no` (1 failed in 0.65s → 1 passed in 0.64s). Both byte-identical restores. **PROVEN.**

### Claim 16 (D8, container) — entrypoint execs the supervisor in place of its shell, requires `REMEDY_DATA_DIR`
Mutations: disabled the `REMEDY_DATA_DIR` guard (1 failed in 0.67s → 1 passed in 0.65s), dropped `exec` (pid mismatch, 1 failed in 0.65s → 1 passed in 0.65s). Both byte-identical restores. **PROVEN.**

### Claim 17 (D8) — "expects the container to run with an init process"
**GAP — no test**, and not realistically one this harness could provide; it's a documented operational expectation (a code comment), not an observable product behavior inside a single-container test.

### Claim 18 (D4) — only `job.stop`/`job.pause`/`job.unpause`/`job.run` are forwarded; everything else runs direct always
Verified by code reading: `grep -rl "supervisor_answers" apps/cli/` returns exactly `serve_client.py` plus `job_stop_cmd.py`, `job_pause_cmd.py`, `do_cmd.py` — no other command module can forward. **GAP — no test** for the structural invariant itself (nothing would catch a future command wrongly gaining a forward call); true today by inspection, not by a red/green mutation pair.

### Claim 19 (Goal & Done) — daemon mode `remedy serve` exists and works
Rollup of Claims 1–16, all proven; command-line proof via Claim 2/3's real subprocess test plus Claim 11's two-real-process SIGKILL scenario. **PROVEN.**

### Claim 20 (Goal & Done) — direct mode stays first-class
Covered by Claim 7. **PROVEN.**

## Gap summary
1. **Claim 12** — no test proves a STOP file halts a run the supervisor actually started (code reading suggests it works; unverified).
2. **Claim 17** — "expects an init process" is a documented expectation, not testable in this harness.
3. **Claim 18** — "only four commands forward" is true by code inspection but has no regression-catching test.

## Cleanup
Worktree `.remedy-wt/f200-audit-wt` removed via `git worktree remove --force`; `git worktree list` no longer shows it. The primary checkout's `git status --porcelain` was empty throughout.
