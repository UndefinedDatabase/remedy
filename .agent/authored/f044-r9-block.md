--- STEP T003(c)/3 — F044 ---
ROUND 9. Book round 8 (already verified PASS by this session's reviewer,
who re-ran its tests, ruff, integrity, canary and mutation red-proofs
independently; the booking text is a records.diff payload below, applied
verbatim), record DECISION F044 D10, and land T003's THIRD and LAST CI
performance budget: 60fps p95 at 200 nodes, measured as the p95 gap
between consecutive REAL, presented compositor frames — Chrome's own
`PipelineReporter` trace events, filtered to `state: "STATE_PRESENTED_ALL"`
— across the fixture's mount-and-settle window, joining the EXISTING
`budgets` CI stage's own `tests/orchestration/test_ci_budgets.py` — no new
stage, no new stage path. A new COMMITTED harness, `apps/ui/perf/`, mounts
the real `ForceBrainGraph` over the committed 200-node fixture
(`brainPerfFixture.ts`, DECISION F019 D6) so the trace has something real
to measure. Full design context: `.agent/decisions.md` DECISION F044 D10
(in the records.diff payload below) and `docs/roadmap/features/T5_F044.md`
T003.

Goal: enforce the graph's frame-delivery rate at 200 nodes against the
60fps p95 budget, in the pattern `packages/orchestration/ci_budgets.py`
already uses for its other two budgets, reading the real number from
Chrome's own compositor trace rather than a JS-side timer that cannot see
dropped frames.

Bundle:
1. Book F044 round 8 into `.agent/live_review.md` (the `Gate: F044 R8 —`
   paragraph) and record DECISION F044 D10 into `.agent/decisions.md`,
   both from the `records.diff` payload below, verbatim, no retyping;
   rewrite `.agent/plan.md` from the `plan.md` payload.
2. Apply `code.diff` to `packages/orchestration/ci_budgets.py`: widens
   `BudgetCheck.observed` from `int` to `int | float`, and adds
   `FRAME_PIPELINE_P95_BUDGET_MS = 17.0` and `check_frame_pipeline`.
3. Apply `harness.diff`: THREE NEW FILES under `apps/ui/perf/`
   (`index.html`, `main.tsx`, `vite.config.mjs`). This is a `git apply`
   of a diff that CREATES files — `git apply --check` then the real apply
   work exactly as for an edit; do not hand-create these files. Read
   `main.tsx` yourself before applying so you recognise it in the diff:
   it mounts `ForceBrainGraph` at the root zoom level (`ZOOM_HOME`,
   `zoomEmphasis`), with no vetoes, and imports
   `../src/styles/globals.css` — WITHOUT that import the page crashes on
   its first paint (`CanvasGradient.addColorStop` on an empty-string
   color, because the node painter's design tokens never resolve), which
   is exactly what this round's reviewer found and DECISION F044 D10
   records; do not remove that import.
4. Apply `tests.diff` to `tests/orchestration/test_ci_budgets.py`: four
   pure unit tests, one private helper
   (`_p95_presented_frame_interval_ms`), and one live
   `@pytest.mark.subprocess` test,
   `test_this_repositorys_shell_sustains_60fps_at_200_nodes`, which
   builds `apps/ui/perf/` fresh (never `apps/ui`'s own build, a
   DIFFERENT vite config) and drives it exactly as the existing
   `test_this_repositorys_shell_paints_within_its_budget` drives
   `apps/ui` itself — read that existing test first, so you recognise
   the pattern in the diff.
5. Prove all four mutations of the `mutations.py` payload turn
   `tests/orchestration/test_ci_budgets.py` red, in a disposable
   worktree (self_drive_protocol.md G5) — this tool excludes BOTH live
   Chrome tests (`-k "not shell_sustains and not shell_paints"`);
   nothing here mutates either of them and each costs a real browser
   launch per run.

Change: exactly `.agent/live_review.md`, `.agent/decisions.md`,
`.agent/plan.md`, `packages/orchestration/ci_budgets.py`,
`tests/orchestration/test_ci_budgets.py`, `apps/ui/perf/index.html`
(new), `apps/ui/perf/main.tsx` (new) and `apps/ui/perf/vite.config.mjs`
(new) — the files Bundle items 1-4 name. Nothing under
`packages/orchestration/ci_stages.py` (this round's own wall-clock
re-measurement, done by this round's reviewer at 44.2s against the
existing 300s timeout, needs no change — DECISION F044 D10 records the
reading), `apps/ui/vite.config.ts`, `docs/system/ci-self-check-v1.md`,
`apps/ui/tsconfig.json`, `apps/ui/eslint.config.js` or any GitHub Actions
workflow. No new dependency, in `apps/ui/package.json` or anywhere else
— `ChromePipe`, `Tracing.start`/`Tracing.end` and `http.server` are all
already available.

Constraints:
- Never retype a payload. Copy every one of the six below into
  `.agent/authored/f044-r9-<name>` with `shutil.copyfile`, verbatim,
  before using it; measure each saved copy's line count, byte count and
  sha256 and compare against the table below before applying it.
- `records.diff`, `code.diff`, `tests.diff` and `harness.diff` are
  unified diffs: run `git apply --check <path-to-authored-copy>` from
  the repo root before the real `git apply`, in this order —
  `records.diff` first (it is the round's bookkeeping and AGENTS.md's
  Commit Gate item 1 requires `.agent/plan.md` current before every
  commit that follows it), then `code.diff`, then `harness.diff`, then
  `tests.diff`. `plan.md` is a REWRITE of `.agent/plan.md` (AGENTS.md:
  rewrite, never append) — copy the authored `plan.md` payload over
  `.agent/plan.md` with `shutil.copyfile` in the SAME commit as
  `records.diff`'s apply.
- `mutations.py` is copied to `.agent/authored/f044-r9-mutations.py` and
  run from there against a disposable `git worktree` under
  `.remedy-wt/` (self_drive_protocol.md G5) — never against the primary
  checkout. BEFORE running it, symlink that worktree's
  `apps/ui/node_modules` to the PRIMARY checkout's own (the same
  technique R7's and R8's own blocks named): the mutation tool's `-k`
  filter excludes the two live Chrome tests by name, but it does NOT
  exclude the existing bundle-size live test
  (`test_this_repositorys_ui_bundle_is_within_its_size_cap`), which
  needs `apps/ui/node_modules` and has no marker of its own to filter
  on — R8's own handback records exactly this gap. `os.unlink` the
  symlink (never delete through it) before removing the worktree.
  Remove the worktree and `git worktree prune` as this step's last
  action; report `git worktree list | wc -l` before creating it and
  after removing it — the two readings must match.
- Never build into the shared `apps/ui/dist` (DECISION F039 D9); the
  live test already builds into `tmp_path`, using `apps/ui/perf/`'s OWN
  `vite.config.mjs`, never the app's own `apps/ui/vite.config.ts`.
- Never run `npm` or `npx`: call `apps/ui/node_modules/.bin/vite` by
  path, exactly as the existing live test does.
- The live test launches a real headless Chrome (`google-chrome` or
  `chromium` on PATH) via `ChromePipe`; if neither binary is on PATH the
  test itself skips (do not treat that as a failure to fix — report
  which branch happened, and note that `test_this_repositorys_shell_
  paints_within_its_budget` will skip for the identical reason in the
  same run).
- Commit subjects: no leading-slash tokens, no absolute paths.
- Self-review loop (AGENTS.md) before every commit: `git diff --stat`
  then `git diff`, read what changed, confirm it matches this step,
  only then commit.
- COMMIT TRAILER — every commit of this round ends with exactly this
  line, verbatim: `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report
   the reading.
2. Your shell must be in the primary checkout,
   `/home/decodeux/Repos/remedy`; report `pwd`. `git status --porcelain`
   must be empty, `git branch --show-current` must read
   `feature/f044-command-palette`, and `git log --oneline -1` must read
   `4b34a5a0e`. Report all three.
3. Report `git worktree list | wc -l` as found (expect 11).

PAYLOADS — the reviewer-authored originals already exist on disk,
untouched by you, at `.remedy-wt/f044-r9-payloads/<file>` (this
session's in-session digest-fallback transport,
docs/agents/self_drive_protocol.md: "in-session there is no transport,
so the hash-stamp ritual is replaced by a cmp of the applied file
against the authored original"). Copy each with `shutil.copyfile` (never
open-and-retype, never an editor) to `.agent/authored/f044-r9-<file>`.
Verify every one's line count, byte count and sha256 BEFORE using it and
report every reading; never retype, never edit.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 28 | 14562 | d8ccf761e6da94e2827925977fc9cbcbf3ead541122f233e7ca53d126ca08690 |
| code.diff | 42 | 2220 | b34af210497c3448fb4de996d58c394631fb4b5c8146de2d55a3c22867ea893a |
| harness.diff | 115 | 4861 | 9008917b17ff44a76a59ccb98afeb2d43def3b903adb151ee77a67e2612be975 |
| tests.diff | 160 | 7182 | 04320aaf78c6822de245dc94f97fa59f0d415fa005c72942e1f4c174379a1419 |
| plan.md | 34 | 1280 | c9372c12e4b9dc5ad54080762018d6f7a326fe2ad9d15c5e4ee821aab0a8316b |
| mutations.py | 122 | 4270 | df0043398be054a1ea7579c29346a812901114b9913c9d3de44e0a57a5223fdf |

`records.diff` touches `.agent/live_review.md` (appends the
`Gate: F044 R8 —` entry) and `.agent/decisions.md` (appends DECISION
F044 D10); both edits are pure appends, verified as `git apply --check`
succeeding cleanly against the current tracked files. `plan.md` is the
full replacement text for `.agent/plan.md` (34 lines, under the 50-line
cap). `code.diff` edits `packages/orchestration/ci_budgets.py` only: one
field-type widening and one append of a constant plus one function at
the end of the file. `harness.diff` CREATES three new files under
`apps/ui/perf/`. `tests.diff` edits
`tests/orchestration/test_ci_budgets.py` only: two new imports widened
into the existing tuple, one new module constant, and an append of four
pure tests, one private helper and one live subprocess test.

Suggested commit sequence (small, self-reviewed, each ends with the
trailer):
C1 — copy `block.md` (this text, saved by you as you received it) and
  `plan.md` into `.agent/authored/`.
C2 — copy `records.diff`, `code.diff`, `harness.diff`, `tests.diff` and
  `mutations.py` into `.agent/authored/`.
C3 — `git apply` the authored `records.diff`; copy the authored
  `plan.md` over `.agent/plan.md`. First substantive commit of the round
  (AGENTS.md Commit Gate item 1; §3 pre-emission item 23).
C4 — `git apply` the authored `code.diff`.
C5 — `git apply` the authored `harness.diff` (three new files).
C6 — `git apply` the authored `tests.diff`.
C7 — handback: rewrite `.agent/handoff.md`, push.

Done when (run every command yourself; report the real exit code and the
literal output, never the word "green"):

G1 TRANSPORT — for each of the six payloads, report the line count,
byte count and sha256 you measured of the file you saved under
`.agent/authored/f044-r9-<name>`, beside the table above; all six must
match exactly. Also report the line count, byte count and sha256 of
your own saved `.agent/authored/f044-r9-block.md` (the text of this
step, saved as you received it): the reviewer holds its own reading of
the same text and compares it at review time (R-0954: this is the one
payload whose digest cannot be checked against a table inside itself).

G2 RECORDS AND PLAN — `git apply --check .agent/authored/f044-r9-
records.diff` then the real apply, both exit 0; `.agent/plan.md` read
back and compared byte-for-byte against `.agent/authored/f044-r9-
plan.md` (must be identical). Report `.agent/decisions.md` and
`.agent/live_review.md`'s byte length (`len(path.read_bytes())`) at
your own C2 commit's tree (before applying `records.diff`), and again
after C3, and confirm each post-apply length equals the pre-apply
length plus that file's own appended slice length from the table's
`records.diff` accounting (live_review.md gains the `Gate: F044 R8 —`
paragraph alone; decisions.md gains DECISION D10 alone) — state both
readings and the arithmetic explicitly.

G3 CODE, HARNESS AND TESTS — `git apply --check` for `code.diff`,
`harness.diff` and `tests.diff` all exit 0 before the real applies;
`python3 -m ruff check packages/orchestration/ci_budgets.py
tests/orchestration/test_ci_budgets.py` reads `All checks passed!`,
exit 0 (note: `apps/ui/perf/*.tsx` is outside `apps/ui/tsconfig.json`'s
`include` and `apps/ui/eslint.config.js`'s `files` glob, so neither
`tsc` nor `eslint` touches it — this is by design, DECISION F044 D10,
and is not a gap to fix); `python3 -m pytest -q -p no:cacheprovider
tests/orchestration/test_ci_budgets.py` reads `27 passed` at exit 0 (or,
ONLY if neither `google-chrome` nor `chromium` is on PATH,
`25 passed, 2 skipped` — report which and why); `python3 -m pytest -q -p
no:cacheprovider tests/orchestration/test_ci_stages.py
tests/orchestration/test_ci_stage_coverage.py` reads `12 passed` at exit
0 (unchanged baseline — confirms this round left the stage table and
its coverage guard alone).

G4 RED PROOFS — run `.agent/authored/f044-r9-mutations.py` against a
disposable `git worktree` built at your own C6 (per the Constraints
above, with the `apps/ui/node_modules` symlink in place before running
it); its last line reads `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY:
True` at exit 0, every one of its four mutations shows `restored
byte-identical: True`, and both controls (before and after) read
`exit=0 failed=0`.

G5 INTEGRITY — run in the primary checkout, AFTER the mutation
worktree of G4 is fully removed and pruned (a leftover worktree symlink
reads as a false "relevant untracked" red): `python3 -m apps.cli.main
integrity check --json` reads `"fail_count": 0` and `"ok": true`.

G6 CANARY — `python3 -m pytest tests/cli/test_golden_path.py -q` passes
at exit 0 (AGENTS.md / §3 verification tiers, every handback).

Handback: completion report (changed-files table with +/- per commit,
verification results with real output, item-status table for Bundle
items 1-5) + rewrite `.agent/handoff.md` naming SESSION 4, round 9, the
next step (`docs/system/ci-self-check-v1.md`'s stage and budget tables,
then the closure sequence), and any deviation.
--- END STEP ---
