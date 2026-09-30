--- STEP T003(b)/3 — F044 ---
ROUND 8. Book round 7 (already verified PASS by this session's reviewer; the
booking text is a records.diff payload below, applied verbatim), fix finding
R-1116 (a wrong DECISION citation in two shipped comments, found at the R7
gate), and land T003's SECOND of three CI performance budgets: first paint
< 1.5s (built bundle, cold), measured over a real HTTP-served fresh
`apps/ui` build with a `first-contentful-paint` reading from headless
Chrome, joining the EXISTING `budgets` CI stage's own
`tests/orchestration/test_ci_budgets.py` — no new stage, no new stage path.
DECISION F044 D9 records the design and defers the 60fps budget and the
`docs/system/ci-self-check-v1.md` fix to the next round. Full design
context: `.agent/decisions.md` DECISION F044 D9 (in the records.diff
payload below) and `docs/roadmap/features/T5_F044.md` T003.

Goal: enforce `apps/ui`'s built shell's first paint against the 1.5-second
budget, in the pattern `packages/orchestration/ci_budgets.py` already uses
for its bundle-size and lint checks, reading the real number from Chrome's
own performance timeline rather than a fixed sleep.

Bundle:
1. Book F044 round 7 into `.agent/live_review.md` (the Gate paragraph AND
   the `R-1116` finding registration, both in the same `records.diff`),
   record DECISION F044 D9 into `.agent/decisions.md`, and rewrite
   `.agent/plan.md` — all from the `records.diff` and `plan.md` payloads
   below, verbatim, no retyping.
2. Apply `code.diff` to `packages/orchestration/ci_budgets.py`: it BOTH
   fixes finding R-1116 (the two `DECISION F044 D7` comments become
   `DECISION F044 D8`) AND adds `FIRST_PAINT_BUDGET_MS` and
   `check_first_paint`.
3. Apply `tests.diff` to `tests/orchestration/test_ci_budgets.py`: four
   pure unit tests plus the one live `@pytest.mark.subprocess` test,
   `test_this_repositorys_shell_paints_within_its_budget`, which imports
   `ChromePipe`, `CHROME_BIN` and `CHROME_STARTUP_TIMEOUT` from
   `tests/ui_server/test_story_export_file_live.py` (an existing, real,
   already-tested class — read it yourself before applying, so you can
   recognise it in the diff rather than trust this sentence) and serves a
   fresh `apps/ui` build with Python's own `http.server.ThreadingHTTPServer`.
4. Prove all four mutations of the `mutations.py` payload turn
   `tests/orchestration/test_ci_budgets.py` red, in a disposable worktree —
   this tool deliberately runs `-k "not shell_paints"`, excluding the one
   live Chrome test (nothing here mutates it; it costs a real browser
   launch per run and the pure tests already cover every line the
   mutations touch).
5. After `code.diff` lands (step 2's commit), append ONE line to
   `.agent/live_review.md`, directly after the `- R-1116` paragraph
   `records.diff` added in step 1, with no blank line removed or added
   elsewhere: `Landed: R-1116 — the two DECISION F044 D7 comments in
   packages/orchestration/ci_budgets.py became DECISION F044 D8 at
   <your C4 commit's short SHA>.` Fill in your own commit's SHA; do not
   guess it, read it back with `git rev-parse --short HEAD` right after
   making that commit. This is YOUR OWN prose (per
   docs/agents/planner_reviewer_prompt.md §4 item 4, only reviewer-authored
   text may say `Done:`; a worker names a landed fix `Landed:` and nothing
   else) — write it as a `git apply`-free direct edit: read the file,
   locate the R-1116 paragraph's end (it ends in "... OPEN.\n"), insert your
   one line immediately after it, on its own line, nothing else changed.

Change: exactly `.agent/live_review.md`, `.agent/decisions.md`,
`.agent/plan.md`, `packages/orchestration/ci_budgets.py` and
`tests/orchestration/test_ci_budgets.py` — the files Bundle items 1-3 and 5
name. Nothing under `packages/orchestration/ci_stages.py`,
`apps/ui/vite.config.ts`, `docs/system/ci-self-check-v1.md` or any GitHub
Actions workflow. No new dependency, in `apps/ui/package.json` or
anywhere else — `ChromePipe` and `http.server` are both already in the
tree.

Constraints:
- Never retype a payload. Copy every one of the five below into
  `.agent/authored/f044-r8-<name>` with `shutil.copyfile`, verbatim, before
  using it; measure each saved copy's line count, byte count and sha256 and
  compare against the table below before applying it.
- `records.diff`, `code.diff` and `tests.diff` are unified diffs: run
  `git apply --check <path-to-authored-copy>` from the repo root before the
  real `git apply`, in this order — `records.diff` first (it is the
  round's bookkeeping and AGENTS.md's Commit Gate item 1 requires
  `.agent/plan.md` current before every commit that follows it), then
  `code.diff`, then `tests.diff`. `plan.md` is a REWRITE of `.agent/plan.md`
  (AGENTS.md: rewrite, never append) — copy the authored `plan.md` payload
  over `.agent/plan.md` with `shutil.copyfile` in the SAME commit as
  `records.diff`'s apply.
- `mutations.py` is copied to `.agent/authored/f044-r8-mutations.py` and run
  from there against a disposable `git worktree` under `.remedy-wt/`
  (self_drive_protocol.md G5) — never against the primary checkout. Remove
  the worktree and `git worktree prune` as this step's last action; report
  `git worktree list | wc -l` before creating it and after removing it —
  the two readings must match.
- Never build into the shared `apps/ui/dist` (DECISION F039 D9); the live
  test already builds into `tmp_path`.
- Never run `npm` or `npx`: call `apps/ui/node_modules/.bin/vite` by path,
  exactly as `tests.diff`'s live test does.
- The live test launches a real headless Chrome (`google-chrome` or
  `chromium` on PATH) via `ChromePipe`; if neither binary is on PATH the
  test itself skips (do not treat that as a failure to fix — report which
  branch happened).
- Commit subjects: no leading-slash tokens, no absolute paths.
- Self-review loop (AGENTS.md) before every commit: `git diff --stat` then
  `git diff`, read what changed, confirm it matches this step, only then
  commit.
- COMMIT TRAILER — every commit of this round ends with exactly this line,
  verbatim: `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the
   reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`;
   report `pwd`. `git status --porcelain` must be empty, `git branch
   --show-current` must read `feature/f044-command-palette`, and `git log
   --oneline -1` must read `c65583711`. Report all three.
3. Report `git worktree list | wc -l` as found (expect 11).

PAYLOADS — the reviewer-authored originals already exist on disk, untouched
by you, at `.remedy-wt/f044-r8-payloads/<file>` (this session's in-session
digest-fallback transport, self_drive_protocol.md: "in-session there is no
transport, so the hash-stamp ritual is replaced by a cmp of the applied
file against the authored original"). Copy each with `shutil.copyfile`
(never open-and-retype, never an editor) to `.agent/authored/f044-r8-<file>`.
Verify every one's line count, byte count and sha256 BEFORE using it and
report every reading; never retype, never edit.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 30 | 14876 | 7a5b463b1e9cb957d809601eb7c676195ea43e90f0c38e158eeb9496a7f67644 |
| code.diff | 44 | 2130 | 5a9b6d316e8a0dabfda32b271f8ce8bc9e7105db7f153d55776ea7222c9b0390 |
| tests.diff | 126 | 4888 | 57db58e8871b34838acf1ac0bdf892584841b88d9b4f5c46b68c583a37815b71 |
| plan.md | 33 | 1181 | 3640bbfb47591c415bd9f95eddbcdc05fd99d886a69868bf85c4554a3594873a |
| mutations.py | 121 | 4117 | bfc75cd1eb4a02fb2f220d868addcdb5e576e06b609c2745a71acec2959968fd |

`records.diff` touches `.agent/live_review.md` (appends the `Gate: F044 R7 —`
entry AND the `- R-1116` finding registration, one paragraph each) and
`.agent/decisions.md` (appends DECISION F044 D9); both edits are pure
appends, verified as `git apply --check` succeeding cleanly against the
current tracked files. `plan.md` is the full replacement text for
`.agent/plan.md` (33 lines, under the 50-line cap). `code.diff` edits
`packages/orchestration/ci_budgets.py` only: two one-word comment fixes
(`D7` to `D8`) and one append of a constant plus one function at the end of
the file. `tests.diff` edits `tests/orchestration/test_ci_budgets.py` only:
six new stdlib imports, the `from packages.orchestration.ci_budgets import
(...)` tuple widened (a REWRITE — the closing `)` moves), one new import
line for `ChromePipe`/`CHROME_BIN`/`CHROME_STARTUP_TIMEOUT`, and an append
of four pure tests, one private poll helper and one live subprocess test.

Suggested commit sequence (small, self-reviewed, each ends with the trailer):
C1 — copy `block.md` (this text, saved by you as you received it) and
  `plan.md` into `.agent/authored/`.
C2 — copy `records.diff`, `code.diff`, `tests.diff` and `mutations.py` into
  `.agent/authored/`.
C3 — `git apply` the authored `records.diff`; copy the authored `plan.md`
  over `.agent/plan.md`. First substantive commit of the round (AGENTS.md
  Commit Gate item 1; §3 pre-emission item 23).
C4 — `git apply` the authored `code.diff`; note your commit's short SHA.
C5 — apply your OWN `Landed: R-1116 —` line to `.agent/live_review.md`
  per Bundle item 5, naming C4's SHA.
C6 — `git apply` the authored `tests.diff`.
C7 — handback: rewrite `.agent/handoff.md`, push.

Done when (run every command yourself; report the real exit code and the
literal output, never the word "green"):

G1 TRANSPORT — for each of the five payloads, report the line count, byte
count and sha256 you measured of the file you saved under
`.agent/authored/f044-r8-<name>`, beside the table above; all five must
match exactly. Also report the line count, byte count and sha256 of your
own saved `.agent/authored/f044-r8-block.md` (the text of this step, saved
as you received it): the reviewer holds its own reading of the same text
and compares it at review time (R-0954: this is the one payload whose
digest cannot be checked against a table inside itself).

G2 RECORDS AND PLAN — `git apply --check .agent/authored/f044-r8-records.diff`
then the real apply, both exit 0; `.agent/plan.md` read back and compared
byte-for-byte against `.agent/authored/f044-r8-plan.md` (must be identical).
Report `.agent/decisions.md` and `.agent/live_review.md`'s byte length
(`len(path.read_bytes())`) at your own C2 commit's tree (before applying
`records.diff`), and again after C3, and confirm each post-apply length
equals the pre-apply length plus that file's own appended slice length from
the table's `records.diff` accounting (live_review.md gains the Gate
paragraph plus the finding paragraph together; decisions.md gains DECISION
D9 alone) — state both readings and the arithmetic explicitly.

G3 CODE AND TESTS — `git apply --check .agent/authored/f044-r8-code.diff`
and `git apply --check .agent/authored/f044-r8-tests.diff` both exit 0
before the real applies; `python3 -m ruff check
packages/orchestration/ci_budgets.py tests/orchestration/test_ci_budgets.py`
reads `All checks passed!`, exit 0; `python3 -m pytest -q -p no:cacheprovider
tests/orchestration/test_ci_budgets.py` reads `22 passed` at exit 0 (or, ONLY
if neither `google-chrome` nor `chromium` is on PATH,
`21 passed, 1 skipped` — report which and why); `python3 -m pytest -q -p
no:cacheprovider tests/orchestration/test_ci_stages.py
tests/orchestration/test_ci_stage_coverage.py` reads `12 passed` at exit 0
(unchanged baseline — confirms this round left the stage table and its
coverage guard alone).

G4 RED PROOFS — run `.agent/authored/f044-r8-mutations.py` against a
disposable `git worktree` built at your own C6 (per the Constraints above);
its last line reads `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True` at
exit 0, every one of its four mutations shows `restored byte-identical:
True`, and both controls (before and after) read `exit=0 failed=0`.

G5 INTEGRITY — run in the primary checkout, AFTER the mutation worktree of
G4 is fully removed and pruned (a leftover worktree symlink reads as a
false "relevant untracked" red): `python3 -m apps.cli.main integrity check
--json` reads `"fail_count": 0` and `"ok": true`.

G6 CANARY — `python3 -m pytest tests/cli/test_golden_path.py -q` passes at
exit 0 (AGENTS.md / §3 verification tiers, every handback).

Handback: completion report (changed-files table with +/- per commit,
verification results with real output, item-status table for Bundle items
1-5, the `Landed: R-1116` line's own text quoted verbatim) + rewrite
`.agent/handoff.md` naming SESSION 3, round 8, the next step (T003(c):
the 60fps budget and the `budgets` stage wall-clock re-measurement), and
any deviation.
--- END STEP ---
