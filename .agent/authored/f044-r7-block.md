--- STEP T003(a)/3 — F044 ---
ROUND 7. Book round 6 (already verified PASS by this session's reviewer; the
booking text is a records.diff payload below, applied verbatim). Land T003's
FIRST of three CI performance budgets: the bundle-size cap, baseline plus 10%
(docs/ui/design_reference/acceptance_criteria.md §5), joining the EXISTING
`budgets` CI stage's own `tests/orchestration/test_ci_budgets.py` — no new
stage, no new stage path. DECISION F044 D8 records the design and defers the
first-paint and 60fps budgets, and the docs fix `docs/system/ci-self-check-v1.md`
needs, to the next two rounds. Full design context: `.agent/decisions.md`
DECISION F044 D8 (in the records.diff payload below) and
`docs/roadmap/features/T5_F044.md` T003.

Goal: enforce `apps/ui`'s built bundle against its own baseline plus 10%, in
the pattern `packages/orchestration/ci_budgets.py` already uses for its lint
check, with a breach naming every chunk that grew.

Bundle:
1. Book F044 round 6 into `.agent/live_review.md`, record DECISION F044 D8
   into `.agent/decisions.md`, and rewrite `.agent/plan.md` — all from the
   `records.diff` and `plan.md` payloads below, verbatim, no retyping.
2. Add `normalize_chunk_name`, `BundleReport`, `bundle_report`,
   `BUNDLE_BASELINE_CHUNKS`, `BUNDLE_SIZE_CAP_FACTOR` and `check_bundle_size`
   to `packages/orchestration/ci_budgets.py`, from the `code.diff` payload.
3. Add the pure unit tests and the one live `@pytest.mark.subprocess` test to
   `tests/orchestration/test_ci_budgets.py`, from the `tests.diff` payload.
4. Prove all five mutations of the `mutations.py` payload turn
   `tests/orchestration/test_ci_budgets.py` red, in a disposable worktree.

Change: exactly `.agent/live_review.md`, `.agent/decisions.md`,
`.agent/plan.md`, `packages/orchestration/ci_budgets.py` and
`tests/orchestration/test_ci_budgets.py` — the files Bundle items 1-3 name.
Nothing under `packages/orchestration/ci_stages.py`, `apps/ui/vite.config.ts`,
`docs/system/ci-self-check-v1.md` or any GitHub Actions workflow. No new
dependency, in `apps/ui/package.json` or anywhere else.

Constraints:
- Never retype a payload. Copy every one of the eight below into
  `.agent/authored/f044-r7-<name>` with `shutil.copyfile`, verbatim, before
  using it; measure each saved copy's line count, byte count and sha256 and
  compare against the table below before applying it.
- `records.diff`, `code.diff` and `tests.diff` are unified diffs: run
  `git apply --check <path-to-authored-copy>` from the repo root before the
  real `git apply`, in this order — `records.diff` first (it is the round's
  bookkeeping and AGENTS.md's Commit Gate item 1 requires `.agent/plan.md`
  current before every commit that follows it), then `code.diff`, then
  `tests.diff`. `plan.md` is a REWRITE of `.agent/plan.md`
  (AGENTS.md: rewrite, never append) — copy the authored `plan.md` payload
  over `.agent/plan.md` with `shutil.copyfile` in the SAME commit as
  `records.diff`'s apply.
- `mutations.py` is copied to `.agent/authored/f044-r7-mutations.py` and run
  from there against a disposable `git worktree` under `.remedy-wt/`
  (self_drive_protocol.md G5) — never against the primary checkout. The tool
  runs the WHOLE of `tests/orchestration/test_ci_budgets.py` (control and
  every mutation alike), whose one live test needs `apps/ui/node_modules`
  present — symlink that worktree's `apps/ui/node_modules` to the primary's
  before running the tool, and `os.unlink` the symlink (never delete through
  it) before removing the worktree. Remove the worktree and `git worktree
  prune` as this step's last action; report `git worktree list | wc -l`
  before creating it and after removing it — the two readings must match.
- Never build into the shared `apps/ui/dist` (DECISION F039 D9); the live
  test already builds into `tmp_path`.
- Never run `npm` or `npx`: call `apps/ui/node_modules/.bin/vite` by path,
  exactly as `tests.diff`'s live test does.
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
   --oneline -1` must read `87f81d7fc`. Report all three.
3. Report `git worktree list | wc -l` as found (expect 11).

PAYLOADS — each is saved to `.agent/authored/f044-r7-<file>`. Verify every
one's line count, byte count and sha256 BEFORE using it and report every
reading; never retype, never edit.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 28 | 11759 | b0bf9f27d66adaac75031bdfff02997d9be22db1d4e8843361276ccc2f47feff |
| code.diff | 88 | 3616 | 154025cfe0f59150acf945cb796a58c78dd04fac878237160bf4dda910f3f6dc |
| tests.diff | 105 | 4121 | b8820731a14d3908e33bbb2bea38eddb46fe19c69e4b22bad0c933f65cfe29de |
| plan.md | 31 | 1108 | ac454ccd9824a0adaefb685985b3bb726ef032bfb2776c86267b75e092c07e0a |
| mutations.py | 121 | 4075 | d7813df1969b232b25bf9fedd4ab6c134f06e3520448f486fd5dc66b666859fe |
| verify_append.py | 80 | 3650 | d53798a20d1ecc29b4d44a9b9c3ea46a91460ac1bc9e80fc1452ede058a62377 |
| decision_d8.md | 10 | 4913 | f32a750379db96ae95cc45b4b34b5ce5f56109b0556043c7e3d4eb687402d19f |
| gate_r6.md | 2 | 2452 | 68198580c3282ea9f817052c05641b217f26b371716d0f54eccc532e1f1174b6 |

`records.diff` touches `.agent/decisions.md` (appends DECISION F044 D8) and
`.agent/live_review.md` (appends the `Gate: F044 R6 —` entry); both edits are
pure appends, verified as `git apply --check` succeeding cleanly against the
current tracked files. `plan.md` is the full replacement text for
`.agent/plan.md` (31 lines, under the 50-line cap). `code.diff` edits
`packages/orchestration/ci_budgets.py` only: one `import math` line and one
append of six new names at the end of the file. `tests.diff` edits
`tests/orchestration/test_ci_budgets.py` only: one `import math` line, the
`from packages.orchestration.ci_budgets import (...)` tuple widened (a
REWRITE — the closing `)` moves), and an append of eight new test functions.

Suggested commit sequence (small, self-reviewed, each ends with the trailer):
C1 — copy `block.md` (this text, saved by you as you received it) and
  `plan.md` into `.agent/authored/`.
C2 — copy `records.diff`, `code.diff`, `tests.diff`, `mutations.py`,
  `verify_append.py`, `decision_d8.md` and `gate_r6.md` into `.agent/authored/`.
C3 — `git apply` the authored `records.diff`; copy the authored `plan.md`
  over `.agent/plan.md`. First substantive commit of the round (AGENTS.md
  Commit Gate item 1; §3 pre-emission item 23).
C4 — `git apply` the authored `code.diff`.
C5 — `git apply` the authored `tests.diff`.
C6 — handback: rewrite `.agent/handoff.md`, push.

Done when (run every command yourself; report the real exit code and the
literal output, never the word "green"):

G1 TRANSPORT — for each of the eight payloads, report the line count, byte
count and sha256 you measured of the file you saved under
`.agent/authored/f044-r7-<name>`, beside the table above; all eight must match
exactly. Also report the line count, byte count and sha256 of your own saved
`.agent/authored/f044-r7-block.md` (the text of this step, saved as you
received it): the reviewer holds its own reading of the same text and
compares it at review time (R-0954: this is the one payload whose digest
cannot be checked against a table inside itself).

G2 RECORDS AND PLAN — `git apply --check .agent/authored/f044-r7-records.diff`
then the real apply, both exit 0; `.agent/plan.md` read back and compared
byte-for-byte against `.agent/authored/f044-r7-plan.md` (must be identical).
Full append forensics on the two record files this round appends to (§3 item
36, gate-budget rule) — `verify_append.py` takes the PRE-APPLY BYTE LENGTH,
never a duplicate copy of either multi-megabyte file, because `git apply`'s
own success already proves the untouched prefix; report each file's byte
length (`len(path.read_bytes())`) BEFORE applying `records.diff`, at your own
C2 commit's tree. After applying, run `python3
.agent/authored/f044-r7-verify_append.py <pre-decisions-length>
.agent/decisions.md .agent/authored/f044-r7-decision_d8.md` and `python3
.agent/authored/f044-r7-verify_append.py <pre-live_review-length>
.agent/live_review.md .agent/authored/f044-r7-gate_r6.md`, using the two
lengths you just reported. Both must print `ALL READINGS OK: True` at exit 0.

G3 CODE AND TESTS — `git apply --check .agent/authored/f044-r7-code.diff` and
`git apply --check .agent/authored/f044-r7-tests.diff` both exit 0 before the
real applies; `python3 -m ruff check packages/orchestration/ci_budgets.py
tests/orchestration/test_ci_budgets.py` reads `All checks passed!`, exit 0;
`python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_ci_budgets.py`
reads `17 passed` at exit 0; `python3 -m pytest -q -p no:cacheprovider
tests/orchestration/test_ci_stages.py tests/orchestration/test_ci_stage_coverage.py`
reads `12 passed` at exit 0 (unchanged baseline — confirms this round left
the stage table and its coverage guard alone).

G4 RED PROOFS — run `.agent/authored/f044-r7-mutations.py` against a
disposable `git worktree` built at your own C5 (per the Constraints above);
its last line reads `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True` at
exit 0, every one of its five mutations shows `restored byte-identical: True`,
and both controls (before and after) read `exit=0 failed=0`.

G5 INTEGRITY — run in the primary checkout, AFTER the mutation worktree of G4
is fully removed and pruned (a leftover worktree symlink reads as a false
"relevant untracked" red): `python3 -m apps.cli.main integrity check --json`
reads `"fail_count": 0` and `"ok": true`.

G6 CANARY — `python3 -m pytest tests/cli/test_golden_path.py -q` passes at
exit 0 (AGENTS.md / §3 verification tiers, every handback).

Handback: completion report (changed-files table with +/- per commit,
verification results with real output, item-status table for Bundle items
1-4) + rewrite `.agent/handoff.md` naming SESSION 2, round 7, the next step
(T003(b): first-paint budget), and any deviation.
--- END STEP ---
