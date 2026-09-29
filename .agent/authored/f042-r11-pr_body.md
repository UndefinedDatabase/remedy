## What

F042 — Multi-project cockpit. The daily multi-repo reality gets a home in the cockpit:

- T001: `packages/orchestration/project_cockpit.py` is pure composition over readers that already
  exist. `projects_view` lists every registered project by slug with its folder checked when read,
  a moved folder carrying a fix-it that names `remedy project attach`, the default project by the
  resolution precedence, and the jobs no card can show, counted as unscoped or orphaned;
  `project_summary` answers one card from `scoped_jobs`: active jobs, the newest job's digest, open
  decisions with their peak urgency, and cost today with its exactness basis.
  `/api/projects`, `/api/projects/<uuid-or-slug>/summary` and `/api/jobs/<id>/project` serve them.
- T002: `apps/ui/src/api/projectScope.ts` is the pure client seam (decoders, paths, the active
  project by address, then the opened job, then the server default, and a switch gate under which
  only the latest switch applies); `cockpitAddress.ts` reads the address into four faces;
  `RemedyApp.tsx` is its one reader and writer, Back and Forward re-read it, and the shell mounts
  under the project and the job, so nothing survives a switch. The switcher is a native select in
  the brand rail's kicker, shown only with more than one project.
- T003: an address with only a token opens `HomeGrid.tsx`, a card per project, twelve to a page;
  one project skips the grid; deep links restore project, job and zoom focus; the dashboard's
  project line counts the same jobs as the card. `tests/ui_server/test_multi_project_live.py` holds
  every card number to `remedy status` over the real CLI and a real UI server.

## Why

T5_F042.md asks for one place to see every project at a glance, switch between them without stale
data, and share a link that restores the same project and view.

## Key decisions (in `.agent/decisions.md`)

- F042 D1 — the project list and card are one composition module over existing readers.
- F042 D2 — the client's project seam is one pure module with its doors in `remedyApi.ts`.
- F042 D3 — the seam is mounted: one address reader and writer, the shell keyed by project and job.
- F042 D4 — the home grid, twelve cards to a page; one project skips it.
- F042 D5 — deep links keep the project; the dashboard reads the job's own project first.
- F042 D6 — the end-to-end run is a CI test over the real CLI and UI server, beside a live browser run.
- F042 D7 — the closure's self-use item SU-036 landed as its job's own diff plus one assertion.

## How to review

Server: `packages/orchestration/project_cockpit.py` and the three routes in `ui_server.py`.
Cockpit: `apps/ui/src/api/projectScope.ts`, `cockpitAddress.ts`, `homeGrid.ts`,
`components/shell/ProjectProvider.tsx`, `ProjectSwitcher.tsx`, `components/home/HomeGrid.tsx` and
`RemedyApp.tsx`. The Built State of `docs/roadmap/features/T5_F042.md` walks every slice; each
round's mutation tool is under `.agent/authored/f042-r*-mutations.py`. The branch also carries two
operator amendments merged from `main` (context hygiene and the reclaim default), already reviewed
in their own pull requests.

## Verification

- The one full suite, on the tree that ships: `20945 passed, 20 skipped` at exit 0, no bad node
  (`.agent/authored/f042-closure-suite.txt`). Its first two runs found two defects this feature
  made, both repaired: a parametrize id drawn from `uuid4()` that stopped xdist at collection
  (R-1112, now also guarded by `tests/test_parametrize_ids_stable.py`), and a blind exception
  handler that raised the BLE001 ratchet (R-1113).
- Evidence job `f042r10e1001` against the fork point `4e643440`: 823 selected tests passed at exit 0.
- Review package `remedy-review-20260929-202000-READY_FOR_REVIEW.zip`, SHA-256
  `44ad4a56316cdecd648fee40d4351c172b88283b2f3efe6b6d34b5d92cbe5672`, READY_FOR_REVIEW.
- A live headless Chrome run over the real stack read seven checks of seven
  (`.agent/authored/f042-r6-live_*`).
- The closure's self-use item SU-036 ran as job `6dad54d0e18348c4` and its diff, the repair of
  R-1107, landed with one added assertion.

## Findings and notes

Latest verdict PASS; accepted PASS. Seven findings were resolved inside the feature, R-1107 to
R-1113. Open findings after this feature: none.

## Runtime actuals

Eleven rounds in two sessions, from the branch's first commit at 13:02 on 2026-09-29 to the
accepted head `cf4d59b7` at 20:14 the same day (UTC+2); reviewer and workers ran as Claude
Opus 5.5; tokens not measured. Remedy itself made two provider calls, in the self-use item, on
`claude-cli` with `claude-sonnet-4-6`, measured at $1.11.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
