--- STEP Closure C1 — F044 ---
ROUND 11. The closure sequence's first round (docs/roadmap/
STATUS_closure_protocol.md; amend0827-process-diet rule 1 permits
pure-bookkeeping rounds here and only here). Book round 10, record
DECISION F044 D12, write the feature file's Built State for T001
through T003, state the checklist-consolidation pass's own finding
(nothing to add), and run the closure's mandatory self-use item
(precondition 6) to its approval gate. This round does NOT land the
self-use item's diff and does NOT mark it `consumed_by` — both happen
later in the closure sequence, exactly as F043's own closure split them
(R6 ran the item, R7 landed it; the `consumed_by` edit itself waits for
the FINAL closure commit, confirmed by reading F043's own git history:
`scripts/self_use_queue.json` was touched only at R6, the run, and R9
C4, the closure commit — never at R7, the landing round). Full design
context: `.agent/decisions.md` DECISION F044 D12 (in the records.diff
payload below).

Goal: close out F044's own findings-and-documentation debt before the
integration gate, and produce the self-use run's own evidence for a
later round to land.

Bundle:
1. Book F044 round 10 into `.agent/live_review.md` (the `Gate: F044
   R10 —` paragraph) and record DECISION F044 D12 into
   `.agent/decisions.md`, both from the `records.diff` payload below,
   verbatim, no retyping; rewrite `.agent/plan.md` from the `plan.md`
   payload.
2. Apply `builtstate.diff` to `docs/roadmap/features/T5_F044.md`:
   appends the `## Built State (F044, 2026-09-30)` section, T001
   through T003, ending at T003's own paragraph (no self-use paragraph
   yet — that lands with the self-use item itself).
3. Copy `selfuse.py` to `.agent/authored/f044-r11-selfuse.py` and run
   it from the primary checkout: `python3 .agent/authored/f044-r11-
   selfuse.py`. It generates the queue's next item if empty, plans and
   RUNS it to the approval gate (spending real provider budget — at
   most the `self_use` role's own default, 8 provider calls / $6.00),
   NEVER applies it, and writes every reading under
   `.agent/selfuse_f044/`. Commit that whole directory as this step's
   own commit. Report EVERY file it prints, verbatim.
4. Read `.agent/selfuse_f044/run_defects.txt`. If it reads `NONE`,
   state that plainly in the handback and do nothing further this
   round — precondition 6's finding-registration clause has nothing to
   register. If it lists ANY defect, quote every one of them VERBATIM
   in the handback's own text (do not summarise, do not paraphrase,
   do not register an R-id yourself — the reviewer mints the id and
   the finding's own prose next round, from your verbatim quote).

Change: exactly `.agent/live_review.md`, `.agent/decisions.md`,
`.agent/plan.md`, `docs/roadmap/features/T5_F044.md`, `.agent/authored/
f044-r11-selfuse.py` and everything `.agent/selfuse_f044/` — the files
Bundle items 1-3 name. Nothing under `apps/` or `packages/` (the
self-use item's own diff, if the run produces one, is NOT applied this
round — it lives only on the job's own branch, `remedy/job-<id>`, until
a later round lands it).

Constraints:
- Never retype a payload. Copy every one of the four below into
  `.agent/authored/f044-r11-<name>` with `shutil.copyfile`, verbatim,
  before using it; measure each saved copy's line count, byte count and
  sha256 and compare against the table below before applying it.
- `records.diff` and `builtstate.diff` are unified diffs: run `git
  apply --check <path-to-authored-copy>` from the repo root before the
  real `git apply`, in this order — `records.diff` first (it is the
  round's bookkeeping and AGENTS.md's Commit Gate item 1 requires
  `.agent/plan.md` current before every commit that follows it), then
  `builtstate.diff`. `plan.md` is a REWRITE of `.agent/plan.md`
  (AGENTS.md: rewrite, never append) — copy the authored `plan.md`
  payload over `.agent/plan.md` with `shutil.copyfile` in the SAME
  commit as `records.diff`'s apply.
- `selfuse.py` is a REVIEWER-AUTHORED SCRIPT, copied verbatim like
  every other payload, never edited — if it errors, report the real
  traceback rather than patching the script yourself; that is an
  ambiguity this block does not resolve (G8, self_drive_protocol.md).
- The self-use run resolves the `self_use` role's configured frontier
  provider (never the local model by accident, DECISION amend0920-
  selfuse-real D2) and spends real money; this is expected and
  budgeted, not a deviation to flag.
- No disposable worktree is needed for Bundle items 1-2 (documentation
  and bookkeeping only). The self-use script itself creates and removes
  its OWN temporary worktree internally if the job's result needs
  reading from its branch (see the script's own `_stale_lines`
  machinery) — this is the script's business, not yours; do not
  duplicate it.
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
   `393d558b6`. Report all three.
3. Report `git worktree list | wc -l` as found (expect 11).

PAYLOADS — the reviewer-authored originals already exist on disk,
untouched by you, at `.remedy-wt/f044-r11-payloads/<file>` (this
session's in-session digest-fallback transport,
docs/agents/self_drive_protocol.md: "in-session there is no transport,
so the hash-stamp ritual is replaced by a cmp of the applied file
against the authored original"). Copy each with `shutil.copyfile` (never
open-and-retype, never an editor) to `.agent/authored/f044-r11-<file>`.
Verify every one's line count, byte count and sha256 BEFORE using it and
report every reading; never retype, never edit.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 69 | 13850 | 2cced28560b9e747db071a9c738308886f4a8f467487bc35affbec9c8a194b00 |
| builtstate.diff | 83 | 5197 | 1d5559641600d1f7b1561fcc09be354f001c94b7eb23f5e58ac56a4d7733e63c |
| selfuse.py | 122 | 6450 | 524bedce37697045f5344b7300d848363184c4a0b9caeb9b00b1bb8c22df7a8d |
| plan.md | 40 | 1690 | 3d78e1cd62a888fe25108a42250fb19b8bd884050f50c69fba849fc309658361 |

`records.diff` touches `.agent/live_review.md` (appends the `Gate:
F044 R10 —` entry) and `.agent/decisions.md` (appends DECISION F044
D12); both edits are pure appends, verified as `git apply --check`
succeeding cleanly against the current tracked files. `plan.md` is the
full replacement text for `.agent/plan.md` (40 lines, under the 50-line
cap). `builtstate.diff` appends ONE new section to
`docs/roadmap/features/T5_F044.md`, ending after T003's own paragraph.

Suggested commit sequence (small, self-reviewed, each ends with the
trailer):
C1 — copy `block.md` (this text, saved by you as you received it),
  `plan.md` and `selfuse.py` into `.agent/authored/`.
C2 — copy `records.diff` and `builtstate.diff` into `.agent/authored/`.
C3 — `git apply` the authored `records.diff`; copy the authored
  `plan.md` over `.agent/plan.md`. First substantive commit of the round
  (AGENTS.md Commit Gate item 1; §3 pre-emission item 23).
C4 — `git apply` the authored `builtstate.diff`.
C5 — run `.agent/authored/f044-r11-selfuse.py`; commit its own output
  directory, `.agent/selfuse_f044/`.
C6 — handback: rewrite `.agent/handoff.md`, push.

Done when (run every command yourself; report the real exit code and the
literal output, never the word "green"):

G1 TRANSPORT — for each of the four payloads, report the line count,
byte count and sha256 you measured of the file you saved under
`.agent/authored/f044-r11-<name>`, beside the table above; all four must
match exactly. Also report the line count, byte count and sha256 of
your own saved `.agent/authored/f044-r11-block.md` (the text of this
step, saved as you received it): the reviewer holds its own reading of
the same text and compares it at review time (R-0954: this is the one
payload whose digest cannot be checked against a table inside itself).

G2 RECORDS AND PLAN — `git apply --check .agent/authored/f044-r11-
records.diff` then the real apply, both exit 0; `.agent/plan.md` read
back and compared byte-for-byte against `.agent/authored/f044-r11-
plan.md` (must be identical). Report `.agent/decisions.md` and
`.agent/live_review.md`'s byte length (`len(path.read_bytes())`) at
your own C2 commit's tree (before applying `records.diff`), and again
after C3, and confirm each post-apply length equals the pre-apply
length plus that file's own appended slice length from the table's
`records.diff` accounting (live_review.md gains the `Gate: F044 R10 —`
paragraph alone; decisions.md gains DECISION D12 alone) — state both
readings and the arithmetic explicitly.

G3 BUILT STATE AND DOCS — `git apply --check .agent/authored/f044-r11-
builtstate.diff` then the real apply, both exit 0; `python3 -m pytest
-q -p no:cacheprovider tests/docs/` reads `327 passed` at exit 0
(same count as round 10 — confirms no docs-consistency guard reads the
new Built State text in a way that breaks it).

G4 SELF-USE RUN — the script's own stdout (report it in full); all TEN
files it writes under `.agent/selfuse_f044/` exist and are non-empty:
`<entry-id>.md`, `entry_and_job_file.txt`, `execution_config.txt`,
`result_state.txt`, `timing.txt`, `changed_paths.txt`,
`full_transcript.txt`, `staleness_after.txt`, `job_diff.txt` and
`run_defects.txt`. `plan.state` (from `result_state.txt`) is either
`JOB_COMPLETED` or `JOB_BLOCKED`; report which, and if `JOB_BLOCKED`,
quote `plan.stop_reason` verbatim — a blocked run before any task ran
is a curation defect per `self_use_runner`'s own docstring, not a
failure of this round, and is reported rather than treated as a gate
failure.

G5 INTEGRITY — run in the primary checkout: `python3 -m apps.cli.main
integrity check --json` reads `"fail_count": 0` and `"ok": true`.

G6 CANARY — `python3 -m pytest tests/cli/test_golden_path.py -q` passes
at exit 0 (AGENTS.md / §3 verification tiers, every handback).

Handback: completion report (changed-files table with +/- per commit,
verification results with real output, item-status table for Bundle
items 1-4, the self-use run's own summary — entry id, title, job id,
provider/model, provider-call count, cost, final task status, and the
`run_defects.txt` contents verbatim) + rewrite `.agent/handoff.md`
naming SESSION 4, round 11, the next step (landing the self-use item's
diff with reviewer-authored tests, mirroring F043's R6→R7 split), and
any deviation.
--- END STEP ---
