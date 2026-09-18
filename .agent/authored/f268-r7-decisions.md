
## DECISION F268 D15 (2026-09-18, reviewer, round 7) — the quick start's five lines and how a test runs them, amending D14
CONTEXT: D14 had the quick-start test choose the fake builder and reviewer through the fixture
repository's own `remedy.toml`; the round 6 worker measured at `68cf6a13` that no such route exists
(`pingpong_job.default_role_provider_name` reads no configuration file). The reviewer's scratch
probe at `8746b21e`, in-process through `apps.cli.grouped.main` on a fresh git repository with
`REMEDY_DATA_DIR` set: the five lines below, with the suffix below added to each `remedy do` line,
each exited 0, and `git status --porcelain` in the target listed only the untracked `.remedy/` and
`remedy.toml` that `init` writes.
CHOSEN: `_QUICK_START` is these five numbered lines, printed exactly so and copyable as printed:
`remedy init`, `remedy doctor core`, `remedy do "Write a CONTRIBUTING.md" --plan-only`,
`remedy do "Write a CONTRIBUTING.md"`, `remedy job list`. Line five lists the jobs rather than
applying one: `job apply` takes a job id a printed line cannot know, a second `do --apply` would
plan a new mission, and line four's run already ends with a `Next:` line carrying the real apply
command. The README Quickstart carries the same five lines. The test reads the lines from the
rendered `remedy --help` output, runs them in order on a fixture repository, appends exactly
`--builder-provider fake --reviewer-provider fake --no-llm --no-ui` to each `remedy do` line and
nothing to any other line, and asserts each exits 0 and that the target's `git status --porcelain`
after the fifth line equals its reading after the first, so nothing the run produced reached the
target (the same probe with `--apply` on line four added an untracked `docs/`). D14's other
clauses stand. ALTERNATIVES: add a `remedy.toml`
route for role providers, rejected because it widens `role_config` for a help-text test.
REVERSE: restore `_QUICK_START` and the README section from git history; delete this paragraph.
