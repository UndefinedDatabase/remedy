
## DECISION F273 D4 (2026-09-19, reviewer, round 4) — T002: eight guards and harness waits repaired, three found already repaired, R-0499 and R-0662 carried with their reasons
CONTEXT: T2_F273.md T002 names thirteen findings, each found by a mutation or a measured colour and
each owed "a mutation that now dies". Measured by two research helpers and re-measured by the
reviewer at `4862e71a`: R-0671, R-0689 and R-0690 were already repaired by `bcd4dd07` and
`05bdeae1` and never booked; R-0499 is a one-in-twenty red of an eight-file sweep in a fresh
worktree whose failing id was never captured; R-0662's fix binds the reviewer's block wording, not
a file; the other eight are live.
CHOSEN: (1) R-0518: `test_vitest_passes` in `tests/orchestration/test_test_runner.py` is skipped,
naming the reason, when `apps/ui/node_modules` is absent — the finding's own fix; CI installs it,
so there the node still runs. (2) R-0569: `write_runtime_config` in
`tests/orchestration/test_product_smoke.py` defaults to `worker_port(2)` of `tests/ports.py`
instead of the literal 5273, with a test that two workers get two ports. (3) R-0649: the emitter
walk of `tests/ui_contracts/test_humanize_catalog.py` skips any path with `node_modules` among its
parts, with a test whose red control proves the plain walk reaches a vendored file. (4) R-0664: two
source guards in `tests/ui_contracts/test_brain_stream_ring.py`, one that the feed card prints each
row's `#{row.seq}`, one that the shell hands the graph stage and the panel the same
`onSelectNode`. (5) R-0691: the two assertions are renamed to what they hold and the class
docstring states the residual a source guard cannot see — the finding's own fix. (6) R-0734 and
R-0708: `tests/ui_server/server_start.py` holds one wait, used by every server-start site of
`tests/ui_server/`: an absent, empty or half-written info file is "not started yet", the wait
lasts as long as the server thread is alive and fails at once when it has exited, and a 120-second
backstop exists only so a hung start cannot hang the suite. That backstop is NOT a raised ceiling:
the operative bound is the thread's liveness, which R-0708's "adaptive" names, and the old flat
five seconds is gone. R-0734 named the copy in `test_command_channel.py` and R-0708 the one in
`test_live_state.py`; the six other copies of the same loop are the same race and are switched in
the same round (amend0917-throughput rule 3). (7) R-0815: the guarded read in
`tests/orchestration/test_job_stop_integration.py` addressed `runs/<run_id>.json`, a path the
store never writes, so its assertion never ran; it now reads through `load_run`, fails when the
record is absent, and asserts unconditionally. (8) R-0671, R-0689 and R-0690 are resolved by the
commits that repaired them, each with the reviewer's own mutation. (9) R-0499 stays open: a research
helper ran the sweep 21 times at `4862e71a` with no red, so there is still no id to capture, and
its fix clause (order the sweep as a probe with `-rf`) stands for the next time it runs. (10)
R-0662 stays open for the closure sequence's single consolidation pass of the §3 checklist, which
may fold "a gate ordering node ids names both runners' mechanisms" into item 33; the list is frozen
while a feature is open (amend0827 rule 4).
ALTERNATIVES: polling to a longer flat deadline for R-0708, rejected because it is a raised ceiling;
repairing R-0734's one named copy only, rejected because six identical copies would keep the same
intermittent red; a test that installs `node_modules` for R-0518, rejected because a test must not
install a toolchain.
REVERSE: restore every test file this round modified from `4862e71a`, delete
`tests/ui_server/server_start.py` and `tests/ui_server/test_server_start.py`, and delete this
paragraph.
