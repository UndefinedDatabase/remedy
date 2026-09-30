--- STEP Closure C2 — F044 ---
ROUND 12. The closure sequence's second round: book round 11, register
finding `R-1117` (the self-use item's own reviewer approved a task
that changed nothing — `describe_self_use_run_defects` caught it, as
designed), owned by F290, and add the self-use item's own paragraph to
the feature file's Built State. This round is a pure bookkeeping round
(amend0827-process-diet rule 1's closure-sequence exception): nothing
under `apps/` or `packages/` changes, because `SU-039`'s job branch
holds no diff to land.

Goal: close out precondition 6 (docs/roadmap/STATUS_closure_protocol.md)
honestly — the self-use item ran, produced nothing, and that nothing is
itself a real, registered finding, not a silently-skipped step.

Bundle:
1. Book F044 round 11 into `.agent/live_review.md` — the `Gate: F044
   R11 —` paragraph AND the `R-1117` finding registration, both from
   the `records.diff` payload below, verbatim, no retyping; rewrite
   `.agent/plan.md` from the `plan.md` payload.
2. Apply `builtstate.diff` to `docs/roadmap/features/T5_F044.md`:
   appends the self-use item's own Built State paragraph, naming
   `SU-039`, its job id, its empty diff and `R-1117`.

Change: exactly `.agent/live_review.md`, `.agent/plan.md` and
`docs/roadmap/features/T5_F044.md` — the files Bundle items 1-2 name.
Nothing under `apps/`, `packages/` or `scripts/self_use_queue.json`
(the `consumed_by` edit precondition 6 asks for lands in the FINAL
closure commit, not here — confirmed by this session's reviewer
reading F043's own git history: `scripts/self_use_queue.json` was
touched only at the round that RAN the item and the round that FLIPPED
STATUS, never at the round in between).

Constraints:
- Never retype a payload. Copy every one of the three below into
  `.agent/authored/f044-r12-<name>` with `shutil.copyfile`, verbatim,
  before using it; measure each saved copy's line count, byte count and
  sha256 and compare against the table below before applying it.
- `records.diff` and `builtstate.diff` are unified diffs: run `git
  apply --check <path-to-authored-copy>` from the repo root before the
  real `git apply`, `records.diff` first (it is the round's bookkeeping
  and AGENTS.md's Commit Gate item 1 requires `.agent/plan.md` current
  before every commit that follows it), then `builtstate.diff`.
  `plan.md` is a REWRITE of `.agent/plan.md` (AGENTS.md: rewrite, never
  append) — copy the authored `plan.md` payload over `.agent/plan.md`
  with `shutil.copyfile` in the SAME commit as `records.diff`'s apply.
- No disposable worktree is needed this round: no production code
  changed, nothing is mutated, this is pure record-keeping.
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
   `65fc51728`. Report all three.
3. Report `git worktree list | wc -l` as found (expect 11 — unchanged
   by this round).

PAYLOADS — the reviewer-authored originals already exist on disk,
untouched by you, at `.remedy-wt/f044-r12-payloads/<file>` (this
session's in-session digest-fallback transport,
docs/agents/self_drive_protocol.md: "in-session there is no transport,
so the hash-stamp ritual is replaced by a cmp of the applied file
against the authored original"). Copy each with `shutil.copyfile` (never
open-and-retype, never an editor) to `.agent/authored/f044-r12-<file>`.
Verify every one's line count, byte count and sha256 BEFORE using it and
report every reading; never retype, never edit.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 12 | 11122 | cf8cc1ac294bd179a78642c0ed90851baf12d3d84b7063014e6a02dd206299a3 |
| builtstate.diff | 20 | 1288 | be86839f4d9db54e1bac40d6cc47ff30086f6e44cc0766c8440eccc596e4ab51 |
| plan.md | 38 | 1547 | fa43ecdc383a33df06fe70168d9049b5351eda7f6c70f888dffd4cde05b01464 |

`records.diff` touches `.agent/live_review.md` only: the `Gate: F044
R11 —` paragraph AND the `R-1117` finding registration, appended
together as one pure-append hunk. `builtstate.diff` appends ONE
paragraph to `docs/roadmap/features/T5_F044.md`, directly after the
existing T003 paragraph.

Suggested commit sequence (small, self-reviewed, each ends with the
trailer):
C1 — copy `block.md` (this text, saved by you as you received it) and
  `plan.md` into `.agent/authored/`.
C2 — copy `records.diff` and `builtstate.diff` into `.agent/authored/`.
C3 — `git apply` the authored `records.diff`; copy the authored
  `plan.md` over `.agent/plan.md`. First substantive commit of the round
  (AGENTS.md Commit Gate item 1; §3 pre-emission item 23).
C4 — `git apply` the authored `builtstate.diff`.
C5 — handback: rewrite `.agent/handoff.md`, push.

Done when (run every command yourself; report the real exit code and the
literal output, never the word "green"):

G1 TRANSPORT — for each of the three payloads, report the line count,
byte count and sha256 you measured of the file you saved under
`.agent/authored/f044-r12-<name>`, beside the table above; all three
must match exactly. Also report the line count, byte count and sha256
of your own saved `.agent/authored/f044-r12-block.md` (the text of this
step, saved as you received it): the reviewer holds its own reading of
the same text and compares it at review time (R-0954).

G2 RECORDS AND PLAN — `git apply --check .agent/authored/f044-r12-
records.diff` then the real apply, both exit 0; `.agent/plan.md` read
back and compared byte-for-byte against `.agent/authored/f044-r12-
plan.md` (must be identical). Report `.agent/live_review.md`'s byte
length (`len(path.read_bytes())`) at your own C2 commit's tree (before
applying `records.diff`), and again after C3, and confirm the
post-apply length equals the pre-apply length plus the appended slice
length (the Gate: F044 R11 paragraph AND the R-1117 finding, together)
from the table's `records.diff` accounting — state both readings and
the arithmetic explicitly.

G3 BUILT STATE — `git apply --check .agent/authored/f044-r12-
builtstate.diff` then the real apply, both exit 0; `python3 -m pytest
-q -p no:cacheprovider tests/docs/` reads `327 passed` at exit 0 (same
count as round 11 — confirms no docs-consistency guard reads the new
paragraph in a way that breaks it).

G4 INTEGRITY — run in the primary checkout: `python3 -m apps.cli.main
integrity check --json` reads `"fail_count": 0` and `"ok": true` — the
new `R-1117` is Medium, so `high_blockers_open` still reads pass; if it
does not, stop and report the real reading rather than proceeding.

G5 CANARY — `python3 -m pytest tests/cli/test_golden_path.py -q` passes
at exit 0 (AGENTS.md / §3 verification tiers, every handback).

Handback: completion report (changed-files table with +/- per commit,
verification results with real output, item-status table for Bundle
items 1-2) + rewrite `.agent/handoff.md` naming SESSION 4, round 12, the
next step (the integration gate — the feature's one full suite run),
and any deviation.
--- END STEP ---
