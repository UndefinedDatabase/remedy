## F203 — Structured logging & correlation

**What.** Remedy writes what it does to one operations log, `<data root>/logs/remedy.log`, set up
in `packages/orchestration/structured_log.py` on the standard library: one JSON line per record
with `ts`, `level`, `logger`, `message`, `job_id`, `task_id`, `run_id` and, when there is one,
`exception`, every line redacted like evidence, the file owner-only and rotated by size. Its keys
are `logging.level`, `logging.json_lines`, `logging.max_bytes` and `logging.backup_count`. Every
command configures it at dispatch, the error stream is unchanged, and job timeline events are
mirrored into it with their ids. `remedy doctor logs <job> [--run <run id>] [--json]` reads one
job's or run's lines in order, and `GET /api/v1/jobs/{job}/logs` answers the same on the public
API (client operation `doctor.logs`; client interface `1.12`, public API `1.13`). Ruff's `T20` now
reads `packages/`, with every remaining `print` carrying a reasoned mark held by a ratchet. Page:
`docs/system/structured-logging-v1.md`.

**Why.** What Remedy did during a job lived on the terminal and in scattered files; nothing tied a
line to the job, task and run it belonged to, so following one run after the fact meant guessing.

**Key decisions.** DECISIONs F203 D1 to D7 in `.agent/decisions.md`: the setup, the file under the
data root and its keys (D1); the wiring at dispatch, the silent write failure and the timeline
mirror (D2); `T20` over `packages/` with reasoned marks and a structural step of
`continue_from_node` first (D3); the read command (D4); the route and the client operation, with the
cockpit's logs view moved to F303 (D5, confirmed by the operator in D7); and the key
`logging.json_lines`, because a key ending like a file extension escapes the documentation
staleness check (D6).

**How to review.** `docs/roadmap/features/T12_F203.md` (its amendments and Built State), then the
round entries `Gate: F203 R1` to `R9` and the `Done:` paragraphs of R-1272 to R-1274 in
`.agent/live_review_archive.md`; `tests/orchestration/test_structured_log.py` plants secrets in
both line shapes, `tests/cli/test_doctor_logs_cmd.py` reads one job's lines, and
`tests/ui_server/test_public_api.py` drives the logs route.

**Changed files.** Ten rounds over two sessions; each round's block is in its
`.agent/authored/f203-r<N>.md`, and the review package's manifest lists every path.

**Verdict.** Rounds 1 to 9 booked PASS in the ledger; round 10's verdict is the reviewer's and is
booked in the next feature's first commit. Live review PASS_WITH_RISKS: four Low findings carried,
all owned by F306.

**Open findings.** 4 (R-1235, R-1246, R-1251 and R-1252, Low, owned by F306).

**Local evidence (amend1011-manual-hosted-ci).** Interpreter: Python 3.10.12, `/usr/bin/python3`.
- The one full suite, `python3 -m pytest -n auto -q`, at `93ff850ec` after `vite build`:
  `22952 passed, 22 skipped, 1 warning in 363.98s`, exit 0 (`.agent/authored/f203-closure-suite.txt`).
- The evidence job `f203r8e1001`, `python3 .agent/authored/f203-r8-create_f203_evidence.py`, on the
  accepted head `145a9195a771183d1c70a14e6a5a7dd4c14fa2ab`: 4607 passed, 4 skipped, exit 0.
- The closing round's selection over `tests/docs/` and the closure guards, on the final tree:
  recorded in `.agent/handoff.md`.
- Review package `remedy-review-20261013-193251-READY_FOR_REVIEW.zip`, SHA-256 `8ba31f893c4f95b1100b2150f5f71f6052b539b126ee675874e83594f9f69c10`, in `/home/decodeux/Repos/remedy-history/zips`.

**Runtime actuals.** 10 delegated rounds over two sessions; wall clock and model tokens not
measured for the rounds themselves; the closure's self-use run, item `SU-061`, ran to its approval
gate in round 6, made 2 provider calls and was never applied.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
