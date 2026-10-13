## F199 — Self-health & crash reports

**What.** `remedy doctor health [--json]` runs eight checks of Remedy's own health from
`packages/orchestration/self_health.py`: `config`, `ledgers`, `snapshots`, `worktrees`,
`providers`, `staging_copies`, `disk` and `crash_reports`. Each answers PASS, WARN or FAIL with a
detail and a hint that names a command or an edit; nothing is repaired, and the command exits 1 on
a FAIL so a CI step can gate on it. `packages/orchestration/crash_report.py` writes a local
Markdown report with secrets removed under `<data root>/crash/` from the command line's catch-all
and when a thread of the serve supervisor ends on an exception; it is never sent. The public API's
`GET /api/v1/health` answers what `remedy doctor health --json` answers, with HTTP 503 on a FAIL,
and `doctor.health` is a client operation (interface version `1.11`). Page:
`docs/system/self-health-v1.md`.

**Why.** Remedy observed the health of the jobs it runs but not its own: a damaged ledger, a broken
snapshot, a full disk or a crash went unnoticed until something else failed.

**Key decisions.** DECISIONS F199 D1 to D3 in `.agent/decisions.md`: the checks, their order, the
command and the crash report under the data root rather than the home folder, with the worker
isolation half of the adapter check, the F171 corpus and the schema registry left to their own
features (D1); the `providers` check warns only when no provider's prerequisite is present and never
fails, the snapshot check reads the twenty newest snapshots, and the worktree check writes nothing
(D2); `doctor.health` becomes a client operation, and the public API's route table moved to
`packages/orchestration/public_api_routes.py` after the health route took `public_api.py` past
1,000 lines (D3). The command catalog's `doctor` group moved to
`apps/cli/command_catalog_doctor.py` first (structure rule 2).

**How to review.** `docs/roadmap/features/T12_F199.md` (its amendment and Built State), then the
round entries `Gate: F199 R1` to `R8` in `.agent/live_review.md` and the `Done:` paragraphs of
R-1266 to R-1271 in its archive; `tests/orchestration/test_self_health.py` injects one corruption
per check, `tests/orchestration/test_crash_report.py` plants secrets in a crash, and
`tests/ui_server/test_public_api.py::test_the_health_route_answers_the_doctor_health_command`
drives the route over both the socket and the port.

**Changed files.** Nine rounds over two sessions; each round's block is in its
`.agent/authored/f199-r<N>.md`, and the review package's manifest lists every path.

**Verdict.** Rounds 1 to 8 booked in the ledger: round 5 FAIL and repaired by round 6, the rest
PASS; round 9's verdict is the reviewer's and is booked in the next feature's first commit. Live
review PASS_WITH_RISKS: four Low findings carried, all owned by F306.

**Open findings.** 4 (R-1235, R-1246, R-1251 and R-1252, Low, owned by F306).

**Local evidence (amend1011-manual-hosted-ci).** Interpreter: Python 3.10.12, `/usr/bin/python3`.
- The one full suite, `python3 -m pytest -n auto -q`, at `16373f14d` after `vite build`:
  `22899 passed, 22 skipped, 1 warning in 365.99s`, exit 0 (`.agent/authored/f199-closure-suite.txt`).
- The evidence job `f199r8e1001`, `python3 .agent/authored/f199-r8-create_f199_evidence.py`, on the
  accepted head `7c76f21da85ff6e5e73beb549ace319d08025c34`: 4337 passed, 4 skipped, exit 0.
- The closing round's selection over `tests/docs/` and the closure guards, on the final tree:
  recorded in `.agent/handoff.md`.
- Review package `remedy-review-20261013-150526-READY_FOR_REVIEW.zip`, SHA-256
  `d068dfe9167cfbfe646115d3127b6dcbeb5273687fb62bc166d47706ffedbc82`, in
  `/home/decodeux/Repos/remedy-history/zips`.

**Runtime actuals.** 9 delegated rounds over two sessions; wall clock and model tokens not measured
for the rounds themselves; the closure's self-use run, item `SU-060`, ran to its approval gate in
round 7, made 2 provider calls and was never applied.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
