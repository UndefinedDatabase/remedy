## F305 — Multi-repo missions: the cockpit's chain band

**What.** The cockpit's missions panel. The right panel's Missions button opens one card per
mission of the project the cockpit shows (one per repository since amend1011b); opening a card
reads that mission's newest orders, each with the model calls and tokens its jobs used and its
chain band: one chip per job of the order in every repository the order reached. A click on a chip
opens that job in its own project's cockpit (`?project=<slug>&job=<job id>`), and Back returns.
Server side, `packages/orchestration/mission_cockpit.py` answers the two new read routes
`/api/projects/<selector>/missions` and `/api/projects/<selector>/missions/<mission id>/orders`
through `packages/orchestration/cockpit_project_routes.py`. Resolves R-1248.

**Why.** F205 split this band off at its closure; and since amend1011b an order over several
repositories is one batch in each repository's own mission, so the cockpit had no view that showed
where one order's jobs went.

**Key decisions.** DECISIONs F305 D1 to D3 in `.agent/decisions.md`: an order's chain is its own
batch plus every batch sharing its correlation id, read across projects, and the feature file
gains an amendment saying so (D1); every route below a project goes through one door, the
structural step that keeps `_RemedyHandler.do_GET` from growing (D2); the panel is an overlay the
right panel opens, its doors a module of their own because `remedyApi.ts` may not grow, and a chip
opens its job through the project context's switch gate (D3). Usage is counted in calls and tokens,
never in dollars (DECISION amend1007b D7). A chip carries references and titles only.

**How to review.** `docs/roadmap/features/T13_F305.md` (its amendment and Built State), then the
round entries `Gate: F305 R1` to `R4` and the `Done: R-1248` paragraph in `.agent/live_review.md`
and its archive; `docs/guides/missions-panel-user-guide-v1.md` for the person's view;
`tests/ui_server/test_mission_chain_live.py` for the browser proof.

**Changed files.** Five rounds in one session; each round's prepared files and numstats are in its
`.agent/authored/f305-r<N>.md`, and the review package's manifest lists every path.

**Verdict.** Rounds 1 to 4 PASS, booked in the ledger; round 5's verdict is the reviewer's and is
booked in the next feature's first commit. Live review PASS_WITH_RISKS: four Low findings carried,
all owned by F306.

**Open findings.** 4 (R-1235, R-1246, R-1251 and R-1252, Low, owned by F306).

**Local evidence (amend1011-manual-hosted-ci).** Interpreter: Python 3.10.12, `/usr/bin/python3`.
- The one full suite, `python3 -m pytest -n auto -q`, on `2506d3f3a` after `vite build`:
  `22641 passed, 22 skipped, 1 warning in 436.71s`, exit 0 (`.agent/authored/f305-closure-suite.txt`).
- The evidence job `f305r4e1001`, `python3 .agent/authored/f305-r4-create_f305_evidence.py`, on the
  accepted head `5132e487355b06bca05fc27a1aabafec1b0835d9`: 4461 passed, 4 skipped, exit 0.
- The closing round's selection over `tests/docs/` and the closure guards, on the final tree:
  recorded in `.agent/handoff.md`.
- Review package `remedy-review-20261012-035421-READY_FOR_REVIEW.zip`, SHA-256
  `485bba5edc512dce18320e9c52b8a01afc827c0b439d595b4f5adb6a60804e13`, in
  `/home/decodeux/Repos/remedy-history/zips`.

**Runtime actuals.** 5 delegated rounds, one session; wall clock and model tokens not measured for
the rounds themselves; the closure's self-use run used two provider calls and 6284 tokens over
105.6 seconds.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
