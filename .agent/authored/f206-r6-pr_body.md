## F206 — Repo dependency catalog

**What.** A catalog the operator writes by hand at `<data root>/org/catalog.toml` names which
registered repository depends on which (`[[repo]]` tables with `pid`, `depends_on`, and optionally
`name`, `root`, `owner`, `publishes`, `consumes`). `packages/orchestration/repo_catalog.py` parses
and validates it — a cycle is refused with its path shown, `a -> b -> a` — and orders an order's
repositories so that each comes after every repository it depends on. An order over several
projects (`remedy do` with several `project:` lines) now plans its jobs in that order when the
catalog exists, and the init step's detail and every job's order text cite each edge, as "app
depends on toolbox through brain". `packages/orchestration/repo_catalog_plausibility.py` warns,
naming the lockfile as proof, when a repository's `package-lock.json`, `uv.lock`, `poetry.lock` or
`Cargo.lock` names a package another repository publishes while the catalog lacks the edge. Two
commands: `remedy project catalog-check` and `remedy project catalog-show`. User page:
`docs/guides/repo-catalog-user-guide-v1.md`.

**Why.** F205 left the order of an order's jobs over several repositories to this feature: a
library's job must run before the job of a repository that consumes it.

**Key decisions.** DECISIONS F206 D1 to D4 in `.agent/decisions.md`: the catalog is a durable class
of the data root, not a file under the home folder (D1); the walk's own project stays the one the
order names first, so the machine client's reading of the mission does not move, and an invalid
catalog plans nothing (D2); lockfiles are read only at a repository's root, names compared
normalized, and a warning never edits the catalog (D3); the commands live in the `project` group,
whose entries first moved unchanged to `apps/cli/command_catalog_project.py`, because the command
catalog's file may not grow (D4).

**How to review.** `docs/roadmap/features/T13_F206.md` (its amendments and Built State), then the
round entries `Gate: F206 R1` to `R5` and the `Done:` paragraphs of R-1253 to R-1256 in
`.agent/live_review.md` and its archive; `tests/cli/test_do_repo_catalog_order.py` for a real walk
over two repositories in the catalog's order.

**Changed files.** Six rounds in one session; each round's prepared files and numstats are in its
`.agent/authored/f206-r<N>.md`, and the review package's manifest lists every path.

**Verdict.** Rounds 1 to 5 PASS, booked in the ledger; round 6's verdict is the reviewer's and is
booked in the next feature's first commit. Live review PASS_WITH_RISKS: four Low findings carried,
all owned by F306.

**Open findings.** 4 (R-1235, R-1246, R-1251 and R-1252, Low, owned by F306).

**Local evidence (amend1011-manual-hosted-ci).** Interpreter: Python 3.10.12, `/usr/bin/python3`.
- The one full suite, `python3 -m pytest -n auto -q`, on `6f664d777` after `vite build`:
  `22726 passed, 22 skipped, 1 warning in 385.64s`, exit 0 (`.agent/authored/f206-closure-suite.txt`).
- The evidence job `f206r5e1001`, `python3 .agent/authored/f206-r5-create_f206_evidence.py`, on the
  accepted head `eda6c6bb329a10c0893c821da9c84c32d5fdc7f9`: 4553 passed, 4 skipped, exit 0.
- The closing round's selection over `tests/docs/` and the closure guards, on the final tree:
  recorded in `.agent/handoff.md`.
- Review package `remedy-review-20261012-063624-READY_FOR_REVIEW.zip`, SHA-256
  `27903864ff926408ffd660ab35a342e686a3352ac8fee54bce305d3c29d1c5fe`, in
  `/home/decodeux/Repos/remedy-history/zips`.

**Runtime actuals.** 6 delegated rounds, one session; wall clock and model tokens not measured for
the rounds themselves; the closure's self-use run used two provider calls and 11512 tokens over
181.9 seconds.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
