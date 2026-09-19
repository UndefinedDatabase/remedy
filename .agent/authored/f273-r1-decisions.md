
## DECISION F273 D1 (2026-09-19, reviewer, round 1) — the suite runs on an isolated data root and fails when the configured root changed; the cockpit walk and the fake builder's single marker
CONTEXT: T2_F273.md T001 builds R-0803 first, "a session-wide isolated data-root fixture in
`tests/conftest.py`, proven by a full run that leaves the operator's data root byte-identical before
and after", and R-0804 and R-0810 as their finding text specifies. Measured by the reviewer at
`80f7c529` in a disposable worktree: `resolve_data_root()` in
`packages/orchestration/data_paths.py` answers `REMEDY_DATA_DIR`, else the configured `data_dir`,
else `<repo>/.data`; `tests/conftest.py` sets no data root; with no fixture,
`tests/test_grouped_cli.py` alone leaves 8 new entries under the default root (`jobs/<id>/job.json`
twice and a `job_logs/<id>/<run>.jsonl`), from `test_brain_graph_json` and
`test_test_discover_json`. R-0804's `_JobPlanTaskAdapter` was deleted at `8601b92e` (F275 R104 C2)
and no test walks the cockpit's read endpoints with a job the current job path created. R-0810 is
live: `_apply_fake_builder_changes` in `packages/orchestration/pingpong_loop.py` appends the task's
marker again in every repair round.
CHOSEN: (1) R-0803. An autouse fixture `_isolated_data_root` in `tests/conftest.py` points
`REMEDY_DATA_DIR` at a fresh `tmp_path_factory` directory for every test unless a wider-scoped
fixture already set it, and removes it after the test; it does not request `monkeypatch`, for the
teardown-order reason `_no_live_ollama_reach` records. `pytest_configure` records, in the xdist
controller only, the configured root and its fingerprint, then drops an inherited
`REMEDY_DATA_DIR`, so a root exported in the operator's shell is the one protected and no test sees
it; `pytest_sessionfinish` re-fingerprints and, on any difference, sets the run's exit status to
failed and prints `R-0803:` with the changed entries. The fingerprint is every entry's relative
path, kind, size and `mtime_ns`: it stands in for "byte-identical" because hashing every file of the
operator's root twice per run costs more than it buys, and a write that alters bytes moves size or
mtime unless it resets them on purpose. `tests/test_data_root_isolation.py` pins the per-test half
(the root is under the pytest temp base and not `<repo>/.data`, starts empty, and a child process
inherits it). R-0803's resolution waits for the closure sequence's one full suite run (operator
amendment amend0917-throughput rule 1), whose transcript must exit 0 with no `R-0803:` line. (2)
R-0804. `tests/ui_server/test_handler_table_walk.py` builds a two-task job with `parse_job_file` and
`run_job` naming the fake provider, derives the endpoint set from `do_GET` in
`packages/orchestration/ui_server.py` with `ast` (the `handlers` dict's string keys and the strings
compared against `endpoint`), and asserts 200 for each, naming every failing endpoint. No
production change. (3) R-0810. `_apply_fake_builder_changes` skips a file that already carries the
task's marker line, with a one-line comment naming the finding, and `TestFakeProviderE2E` in
`tests/orchestration/test_pingpong_cli.py` asserts a two-round fake run leaves exactly one marker.
ALTERNATIVES: a fixture that always overrides the variable, rejected because it sent
`tests/orchestration/test_manual_completion_bundle.py`'s module-built job to the wrong root
(measured); a sentinel file in the root, rejected because it detects only writes to itself; content
hashes, rejected on cost as above; a hand-written endpoint list, rejected because an endpoint added
later would go unwalked; hoisting `handlers` to module level, rejected as a production change made
only for a test.
REVERSE: remove the fixture, the two hooks and `_data_root_fingerprint` from `tests/conftest.py`,
delete `tests/test_data_root_isolation.py` and `tests/ui_server/test_handler_table_walk.py`, remove
the marker guard and its test, and delete this paragraph.
