# F306 round 2 — amendment 1 (the reviewer's repair of its own block, after gate 3 read red)

Your C1 `accb73a87` and C2 `013656215` stand; nothing is rewritten, nothing was pushed. Gate 3
read two red nodes of `tests/test_structure_ratchet.py`, both caused by the block: its step 1
ordered a re-export from `packages/runtimes/dev_server.py`, a file on the structure ledger that may
not grow, and its step 2 put the new branch inline in `_run_app_once`, which then passed 100 lines.
Your stop was correct. Continue the round with ONE more product commit, then the gates, C3, push.

## C2b — `F306 R2 C2b: the ownership check lives beside the runner, and a denied read is unproven, not foreign (R-1251)`
Paths: `packages/runtimes/dev_server.py`, `packages/runtimes/dev_server_ports.py`,
`packages/orchestration/dod_runners.py`, `tests/orchestration/test_dod_runners.py`,
`tests/runtimes/test_dev_server_ports.py`.
1. `dev_server.py`: restore it byte for byte to its content at `58a280f34`
   (`git -C ... show 58a280f34:packages/runtimes/dev_server.py`); afterwards
   `git diff 58a280f34 -- packages/runtimes/dev_server.py` prints nothing. The new function is not
   re-exported: no existing import path names it.
2. `dod_runners.py`: import `port_listener_in_session` from
   `packages.runtimes.dev_server_ports`, not from `dev_server`. Move the new branch into a module
   function `_confirm_app_owns_port(port: int, proc: Any, health_path: str, log: list[str]) ->
   tuple[str, str]` directly above `_run_app_once`, with this WHY comment directly above it:
   `# R-1251: two checks can be given one port, so a health answer proves readiness only when a`
   `# process of the app's own session holds the port.` It passes `proc.pid` as the session id
   (the app was started with `start_new_session=True`, so its group id is its pid, and no call
   can raise on an app that has just exited). It returns `("", "")` to go on and
   `(REASON_APP_START_FAILED, detail)` to refuse, logging exactly the two sentences step 2 of the
   block names. `_run_app_once` calls it after `ready on ...` and runs `body` only when the
   returned reason is empty. `_run_app_once` must end at most 100 lines long.
3. `dev_server_ports.py`, `port_listener_in_session`: a process whose group id cannot be read is
   skipped (it vanished, or it is not ours to read). A process IN the session whose connections
   cannot be read — `psutil.NoSuchProcess` is skipped, any other `psutil.Error` or `OSError`
   (access denied, zombie) — marks the answer unproven: the function returns True as soon as a
   listener is found, otherwise None when any session member was unreadable, otherwise False. The
   docstring says so. A denied read must never read as proof that the port is foreign.
4. `tests/runtimes/test_dev_server_ports.py`: add a test — an idle child in its own session, with
   the connections read of `psutil.Process` monkeypatched to raise `psutil.AccessDenied` (patch
   `connections`, and `net_connections` too where the installed psutil has it) — reads None.
5. `tests/orchestration/test_dod_runners.py`, the two-racers test: delete the assertion that at
   least one check did not pass, and put one comment line in its place saying the two checks may
   not overlap in time, so only the property every interleaving keeps is asserted; the squatter
   test is the deterministic proof.
6. Self-review over `git diff --cached`.

## Then
Run gates 1 to 5 of the block once each, in order, exactly as written (gate 1's `verify.py` reads
C1 only and stays valid). In C3, ALSO copy this file to `.agent/authored/f306-r2-amend1.md`
(`cmp` prints nothing; report `wc -l` and `sha256sum`), so C3's paths are `.agent/handoff.md` and
that file. The handback's commits table has a row for C2b; its Verification section reports the
first gate-3 reading (2 failed, 3753 passed, 3 skipped) as well as the new one; its item-status
table adds rows for this amendment's steps 1 to 5. Everything else in the block stands.
