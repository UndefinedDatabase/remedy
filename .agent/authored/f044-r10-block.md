--- STEP T003 doc sync — F044 ---
ROUND 10. Book round 9 (already verified PASS by this session's reviewer,
who independently re-derived the transport, re-ran every test, ruff,
integrity, canary and mutation red-proofs; the booking text is a
records.diff payload below, applied verbatim), record DECISION F044
D11, and sync `docs/system/ci-self-check-v1.md`'s stage and budget
tables to the `budgets` CI stage's real, current selection. This is a
DOCUMENTATION AND DATA-ACCURACY round: no production behaviour changes,
`packages/orchestration/ci_stages.py` is untouched, and `timeout_sec`
for the `budgets` stage stays `300`. Full design context:
`.agent/decisions.md` DECISION F044 D11 (in the records.diff payload
below).

Goal: make `docs/system/ci-self-check-v1.md` and
`tests/orchestration/test_ci_stages.py` agree with each other and with
`packages/orchestration/ci_stages.py`'s real `budgets` stage — currently
SEVEN named test paths, not four — backed by a fresh three-sample
wall-clock measurement in the primary checkout.

Bundle:
1. Book F044 round 9 into `.agent/live_review.md` (the `Gate: F044 R9 —`
   paragraph) and record DECISION F044 D11 into `.agent/decisions.md`,
   both from the `records.diff` payload below, verbatim, no retyping;
   rewrite `.agent/plan.md` from the `plan.md` payload.
2. Apply `inventory.diff` to `.agent/f083_inventory.md`: appends `## Q14`,
   a fresh three-sample measurement of the `budgets` stage's current
   seven-path selection, taken in the PRIMARY checkout (never a
   worktree).
3. Apply `docs_and_test.diff`: edits BOTH
   `docs/system/ci-self-check-v1.md` (the stage table's `budgets` row —
   "four" becomes "seven" named paths — and the runtime-budget table's
   `budgets` row and its two derived sum figures) AND
   `tests/orchestration/test_ci_stages.py` (`MEASURED_MAX_WALL_S
   ["budgets"]` moves from `24.40` to `28.08`, with its comment
   rewritten to name the reading's full history). These two files land
   in ONE commit because the doc's own number and the test's own number
   must never disagree, even for one commit.

Change: exactly `.agent/live_review.md`, `.agent/decisions.md`,
`.agent/plan.md`, `.agent/f083_inventory.md`,
`docs/system/ci-self-check-v1.md` and
`tests/orchestration/test_ci_stages.py` — the files Bundle items 1-3
name. Nothing under `packages/orchestration/ci_stages.py` (its
`timeout_sec` values are UNCHANGED this round — the whole point of the
re-measurement is confirming they still hold) or any other production
path.

Constraints:
- Never retype a payload. Copy every one of the four below into
  `.agent/authored/f044-r10-<name>` with `shutil.copyfile`, verbatim,
  before using it; measure each saved copy's line count, byte count and
  sha256 and compare against the table below before applying it.
- `records.diff`, `inventory.diff` and `docs_and_test.diff` are unified
  diffs: run `git apply --check <path-to-authored-copy>` from the repo
  root before the real `git apply`, in this order — `records.diff`
  first (it is the round's bookkeeping and AGENTS.md's Commit Gate item
  1 requires `.agent/plan.md` current before every commit that
  follows it), then `inventory.diff`, then `docs_and_test.diff`.
  `plan.md` is a REWRITE of `.agent/plan.md` (AGENTS.md: rewrite, never
  append) — copy the authored `plan.md` payload over `.agent/plan.md`
  with `shutil.copyfile` in the SAME commit as `records.diff`'s apply.
- No disposable worktree is needed this round (no production code and
  no new test changed behaviour — `test_each_budget_is_the_documented_
  multiple_of_the_measured_maximum` already exercises the changed
  dict value directly), so G5 of the self-drive protocol does not
  apply; do not create one.
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
   `1318d15ca`. Report all three.
3. Report `git worktree list | wc -l` as found (expect 11 — unchanged
   by this round).

PAYLOADS — the reviewer-authored originals already exist on disk,
untouched by you, at `.remedy-wt/f044-r10-payloads/<file>` (this
session's in-session digest-fallback transport,
docs/agents/self_drive_protocol.md: "in-session there is no transport,
so the hash-stamp ritual is replaced by a cmp of the applied file
against the authored original"). Copy each with `shutil.copyfile` (never
open-and-retype, never an editor) to `.agent/authored/f044-r10-<file>`.
Verify every one's line count, byte count and sha256 BEFORE using it and
report every reading; never retype, never edit.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 68 | 12750 | 1cba7329c438b3e4d2f12cd2d24aec3925b8f29608024ed4eb07b0338bfae12e |
| inventory.diff | 71 | 4521 | 7f913911bf63ea29a6f01d5a36237613fda490765b2f32195fdb3cf7b8a8c2b5 |
| docs_and_test.diff | 52 | 3993 | 0e4c169b90bc558bf5ca65c321a7645dc9bde2547ac23ccc04862fdc869b91d4 |
| plan.md | 35 | 1345 | 4d40f07c5791beeb5450077711b3dc10930ee23063621ef35366411e7353b743 |

`records.diff` touches `.agent/live_review.md` (appends the
`Gate: F044 R9 —` entry) and `.agent/decisions.md` (appends DECISION
F044 D11); both edits are pure appends, verified as `git apply --check`
succeeding cleanly against the current tracked files. `plan.md` is the
full replacement text for `.agent/plan.md` (35 lines, under the 50-line
cap). `inventory.diff` appends ONE new section, `## Q14`, to
`.agent/f083_inventory.md`. `docs_and_test.diff` edits TWO files: three
lines of `docs/system/ci-self-check-v1.md` (one table cell in the stage
table, one table cell plus two derived numbers in the runtime-budget
table) and `tests/orchestration/test_ci_stages.py` (one comment
rewritten, one dict value changed).

Suggested commit sequence (small, self-reviewed, each ends with the
trailer):
C1 — copy `block.md` (this text, saved by you as you received it) and
  `plan.md` into `.agent/authored/`.
C2 — copy `records.diff`, `inventory.diff` and `docs_and_test.diff`
  into `.agent/authored/`.
C3 — `git apply` the authored `records.diff`; copy the authored
  `plan.md` over `.agent/plan.md`. First substantive commit of the round
  (AGENTS.md Commit Gate item 1; §3 pre-emission item 23).
C4 — `git apply` the authored `inventory.diff`.
C5 — `git apply` the authored `docs_and_test.diff`.
C6 — handback: rewrite `.agent/handoff.md`, push.

Done when (run every command yourself; report the real exit code and the
literal output, never the word "green"):

G1 TRANSPORT — for each of the four payloads, report the line count,
byte count and sha256 you measured of the file you saved under
`.agent/authored/f044-r10-<name>`, beside the table above; all four must
match exactly. Also report the line count, byte count and sha256 of
your own saved `.agent/authored/f044-r10-block.md` (the text of this
step, saved as you received it): the reviewer holds its own reading of
the same text and compares it at review time (R-0954: this is the one
payload whose digest cannot be checked against a table inside itself).

G2 RECORDS AND PLAN — `git apply --check .agent/authored/f044-r10-
records.diff` then the real apply, both exit 0; `.agent/plan.md` read
back and compared byte-for-byte against `.agent/authored/f044-r10-
plan.md` (must be identical). Report `.agent/decisions.md` and
`.agent/live_review.md`'s byte length (`len(path.read_bytes())`) at
your own C2 commit's tree (before applying `records.diff`), and again
after C3, and confirm each post-apply length equals the pre-apply
length plus that file's own appended slice length from the table's
`records.diff` accounting (live_review.md gains the `Gate: F044 R9 —`
paragraph alone; decisions.md gains DECISION D11 alone) — state both
readings and the arithmetic explicitly.

G3 DOCS, INVENTORY AND TEST — `git apply --check` for `inventory.diff`
and `docs_and_test.diff` both exit 0 before the real applies; `python3
-m ruff check tests/orchestration/test_ci_stages.py` reads `All checks
passed!`, exit 0; `python3 -m pytest -q -p no:cacheprovider
tests/orchestration/test_ci_stages.py tests/orchestration/
test_ci_stage_coverage.py` reads `12 passed` at exit 0 (same count as
before this round — only a dict value and a comment changed, no test
added or removed); `python3 -m pytest -q -p no:cacheprovider
tests/docs/` reads `327 passed` at exit 0, confirming no docs-consistency
guard reads the numbers this round changed.

G4 INTEGRITY — run in the primary checkout: `python3 -m apps.cli.main
integrity check --json` reads `"fail_count": 0` and `"ok": true`.

G5 CANARY — `python3 -m pytest tests/cli/test_golden_path.py -q` passes
at exit 0 (AGENTS.md / §3 verification tiers, every handback).

Handback: completion report (changed-files table with +/- per commit,
verification results with real output, item-status table for Bundle
items 1-3) + rewrite `.agent/handoff.md` naming SESSION 4, round 10, the
next step (the closure sequence, docs/roadmap/STATUS_closure_protocol.md),
and any deviation.
--- END STEP ---
