### STEP T001b — F257 Self-use track, round 2 (THE QUEUE)

Goal: book the round 1 verdict into the record, and build the curated queue
file, its read-only loader and its tests exactly as DECISION F257 D2 rules.

Base: `cbf081eb`, the tip of `feature/f257-self-use-track`. Every reading stated
below was taken there by the reviewer.

Bundle, in commit order:

- C0a save this block verbatim to `.agent/authored/f257-r2.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 advance `.agent/plan.md`
- C2 book the F257 R1 verdict into `.agent/live_review.md` and append the two
  reviewer-prose slips to `.agent/prose_slips.md`
- C3 the queue file, its loader and its tests
- C4 rewrite `.agent/handoff.md`

Change set — these paths and nothing else:

- `.agent/authored/f257-r2.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `.agent/prose_slips.md`
- `scripts/self_use_queue.json`
- `packages/orchestration/self_use_queue.py`
- `tests/orchestration/test_self_use_queue.py`
- `.agent/handoff.md`

### Constraints

0. BEFORE ANYTHING: report `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
   — it was `[]` when this block was written, and if it is not `[]` now, STOP and
   hand back without committing. Report `git rev-parse HEAD`, which must equal
   `cbf081eb2ea9d2d6572891ee8185f66f56041c0c`, and `git branch --show-current`,
   which must be `feature/f257-self-use-track`. Create no branch and no pull
   request this round. Never force-push and never rewrite history.
1. Apply every authored slice BYTE FOR BYTE — no reflow, rewording, retitling,
   correction or shortening. If a slice looks wrong, apply it as written and say
   so in the handback's deviations; the record is repaired by a later append.
2. The delimiter lines `<<<SLICE …` and `<<<END …` are transport only and never
   reach a target file.
3. Extract every slice from the COMMITTED blob with
   `git show <C0a>:.agent/authored/f257-r2.md`, never from this prompt's text.
4. AGENTS.md binds in full: the self-review loop before every commit, one
   logical step per commit, `.agent/plan.md` current before every commit, a
   clean tree, and the push.
5. Destructive verification runs ONLY inside a disposable `git worktree` under
   the gitignored `.remedy-wt/`. The primary checkout satisfies
   `git status --porcelain` empty at every commit.
6. Shell forms rejected by this session's guard are RE-EXPRESSED, never skipped
   and never weakened. Loops, `$( )`, `${arr[0]}`, `cp`, brace literals
   containing quotes, and every form of environment-variable assignment
   (`VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`) are rejected by FORM;
   route such work through `python3 - <<'PY'`, set variables in-process with
   `os.environ[...]`, and copy with `shutil.copyfile`. Capture real exit codes
   with `bash -c '<cmd>; echo "REAL_EXIT=$?"'` or from `subprocess` in Python —
   the tool does not surface a non-zero exit on its own. Report every
   re-expression in the handback.
7. THE GUARDS THAT SWEEP EVERY NEW `packages/orchestration/*.py`, measured by
   the reviewer at `cbf081eb` and named here so they are satisfied by
   construction rather than discovered from a red:
   `tests/test_data_paths.py::TestSingleReaderInvariant` forbids the literal
   `os.environ.get("REMEDY_DATA_DIR")` in any file under `packages/` but
   `data_paths.py`;
   `tests/test_path_utils.py::TestSingleImplementationInvariant` forbids the
   regex `[^a-zA-Z0-9_-]` and the name `_MAX_PATH_COMPONENT_LENGTH` outside
   `path_utils.py`;
   `tests/regression/test_named_bugs.py::TestNoSilentSwallow` forbids a bare
   `except: pass`; and
   `tests/ui_server/test_dashboard_contract.py::TestLiveReviewAndAgentStateRefs`
   forbids a product module referencing `.agent/live_review.md`. The new module
   contains none of those.
8. THE APPEND CONVENTION, and it governs every append this round. Each appended
   slice is separated from the text that precedes it by exactly ONE BLANK LINE,
   and the file ends with exactly one trailing newline. Concretely, for a file
   whose last byte is already a newline, the bytes written are: one newline,
   then the slice, then one newline. Where two slices append to the SAME file in
   one commit, the second is separated from the first by one blank line in the
   same way. This constraint, not any arithmetic sentence in a gate below, is
   the authority on separators; if a gate's formula and this constraint
   disagree, follow this constraint and declare the disagreement.

### SPEC — the production code of C3

Production code is DESCRIBED here, not sliced: write it in this repository's
idiom, with the one-line WHY comment above each definition that AGENTS.md's
discoverability conventions ask for. Follow
`packages/orchestration/dead_model_list.py` and `scripts/dead_models.json` as
the shape precedent — the reviewer read both at `cbf081eb` — including the
module docstring's "Public API" and "Deliberate absences" sections.

S1. New file `scripts/self_use_queue.json`, a JSON object with exactly the keys
`schema_version` (integer 1), `description` (one prose string stating that the
queue is operator-curated DATA, that exactly one item is consumed per feature
close, and that an item is marked consumed by the closure round and NEVER by a
job) and `items` (array).

S2. Each item is an object with exactly the keys `id`, `title`, `why`,
`job_markdown` and `consumed_by`. `id` matches `^SU-\d{3}$` and is unique.
`job_markdown` is the literal text of a job file in the format
`packages/orchestration/pingpong_job.py:parse_job_file` accepts — a `# Job: …`
H1 and at least one `## Task N` heading, each task carrying an `Acceptance:`
line. `consumed_by` is the empty string while the item is pending, and otherwise
the feature id that consumed it.

S3. Ship EXACTLY ONE item, `SU-001`, with `consumed_by` empty. Its subject is
the documentation gap the reviewer measured at `cbf081eb`: no page under `docs/`
states the job-file format `parse_job_file` accepts, which is written down only
in `scripts/remedy_self_job_flow.sh` and in the argument help in
`apps/cli/command_catalog.py`. Its `job_markdown` asks for one new page under
`docs/` describing that format and registering it in the `docs/README.md` index
as AGENTS.md requires, with an `Acceptance:` line naming both obligations.
Curated is the load-bearing word: the item is small, bounded, genuinely useful,
and touches no path the scope fences deny.

S4. New module `packages/orchestration/self_use_queue.py`. Public API, exactly:
`SELF_USE_QUEUE_SCHEMA_VERSION` (1); `SELF_USE_QUEUE_FILENAME`
(`"self_use_queue.json"`); `SelfUseQueueError(RuntimeError)`; a frozen dataclass
`SelfUseQueueEntry` carrying the five fields S2 names;
`default_self_use_queue_path(repo_root: Path | None = None) -> Path`, resolving
`repo_root or Path(__file__).resolve().parents[2]` then `scripts/` then the
filename, the way `gauntlet_orders.default_orders_dir` does;
`load_self_use_queue(path: Path | None = None) -> tuple[SelfUseQueueEntry, ...]`;
`pending_self_use_items(path=None) -> tuple[SelfUseQueueEntry, ...]`; and
`next_self_use_item(path=None) -> SelfUseQueueEntry | None`.

S5. `load_self_use_queue` RAISES `SelfUseQueueError` on a missing file, on
unparseable JSON, on a `schema_version` other than 1, on a missing or
wrongly-typed key, on a duplicate id, and on an id not matching the pattern. It
NEVER returns an empty tuple to stand for a failure: "the queue is empty" and
"I could not read the queue" are opposite answers and must never look alike.
Record that as a Deliberate absence in the docstring.

S6. `next_self_use_item` answers the FIRST item in file order whose
`consumed_by` is empty, and `None` when every item is consumed. `None` means the
track is exhausted and a human must curate more; it never means an error,
because S5 raises for those.

S7. THE MODULE IS READ-ONLY AND OWNS NO WRITER. It opens the queue file for
reading only and exports no function that marks an item consumed. Record the
deliberate absence where a reader will search for it: Remedy deliberately does
not let a job mark its own queue item consumed, for the same reason
`docs/roadmap/STATUS.md` sits in `scope_fences.BUILTIN_DENY` — a run that can
check itself off is not a gate. Consumption is an edit the closure round makes,
which DECISION F257 D2 rules.

S8. New file `tests/orchestration/test_self_use_queue.py`, named after the
module it covers, pinning each of these as its own test: the SHIPPED file loads,
carries `schema_version` 1 and at least one item, with unique ids all matching
the pattern; EVERY shipped item's `job_markdown` really parses through
`parse_job_file` and yields at least one task carrying a title — this is the
invariant that keeps the queue and the job parser from drifting apart, and it is
why the queue stores job TEXT rather than a second task format; the loader
RAISES rather than returning empty for each failure S5 names, driven from
fixtures written into `tmp_path`; `next_self_use_item` returns the first pending
item, skips a consumed one, and returns `None` for an all-consumed fixture; and
`load_self_use_queue` leaves the queue file's bytes unchanged, read before and
after the call.

### The authored slices

<<<SLICE PLANF257R2
# Plan — F257 Self-use track

Branch: feature/f257-self-use-track, cut from `main` at the merge commit of pull
request #220. F257 was claimed by Rule A5 as the first unchecked line in
`docs/roadmap/STATUS.md` after F256.

## Goal
Remedy is used on Remedy on a schedule that cannot be skipped: a curated queue
of small maintenance jobs, exactly one consumed per feature close, run through
`do job-plan` and `do job-run` against this repository and taken to the normal
approval gate.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| claim F257 and retarget the state | done | round 1 |
| rule the queue format and the consumption point | done | DECISIONS F257 D1 and D2 |
| the queue file and its read-only loader | done | this round, against D2 |
| render a queue item into a job file and plan it | open | needs the loader first |
| consume exactly one item per feature close | open | the closure-protocol edit |
| document the format where a reader looks | open | acceptance item 1 |

## Next Steps
1. Render a pending queue item into a job file and plan it through
   `plan_job_from_file`, so the queue reaches the real job path.
2. Wire the consumption point into the closure sequence, so exactly one item is
   consumed per feature close and the track cannot rot.
3. Document the queue format and the job-file format where a reader would look,
   and register the page in `docs/README.md`.

## Risks
- A job must never mark its own queue item consumed; the loader ships no writer
  and DECISION F257 D2 rules the consumption point.
- `docs/roadmap/STATUS.md` is in `scope_fences.BUILTIN_DENY` and stays there.
<<<END PLANF257R2

<<<SLICE GATEF257R1
Gate: F257 R1 — the CLAIM round, which merged the F256 closure pull request at the Open PR Gate, claimed F257 and ruled the two questions this feature's shape depends on. THE ROUND PASSED on every gate its block ordered, G1 through G7, and the reviewer re-ran each one independently at `cbf081eb`.

THE OPEN PR GATE WAS EXECUTED, NOT ASSERTED. Pull request #220 merged as a real two-parent commit, `f17b1d0d` with parents `0e8ab5b4` and `c9c54d27`, so the bytes that reached `main` are exactly the F256 closure commit the reviewer had gated. `gh pr list --state open` reads `[]` afterwards and no pull request was created this round. The branch `feature/f257-self-use-track` carries five single-parent commits with insertions 373, 332, 131, 1 and 187, each under the 500-line cap, and `docs/roadmap/STATUS.md` now reads `[x]` for F256 and `[~]` for F257 with the accepted count UNMOVED at 61.

THE APPEND WAS VERIFIED AGAINST THE BYTES RATHER THAN AGAINST THE GATE'S WORDING, AND THE TWO DISAGREED. `.agent/decisions.md` at C1 reconstructs byte for byte as the base blob plus one newline, plus DECF257D1, plus a BLANK LINE, plus DECF257D2, plus a trailing newline — 710498 bytes to 715877 — with the pre-round blob a byte PREFIX, a negative control flipped inside the FIRST appended paragraph REJECTED, and the last 12 blank-line units matching the two slices' paragraphs in order. The block's own G4 sentence spelled that reconstruction with a single newline between the two slices and no trailing newline, which is false of the correct file; the worker applied the block's separator convention, which is the authority, and the disk is right. The reviewer's arithmetic was wrong, not the round's, and it is recorded in `.agent/prose_slips.md` rather than as a finding, because nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong on disk.

TRANSPORT IS REPORTED FOR WHAT IT COVERS AND NOT MORE. The block was carried to the worker as a file under the gitignored `.remedy-wt/` and copied into `.agent/authored/f257-r1.md` with `shutil.copyfile` rather than retyped, so the chain the proof walks is the reviewer's own original, the committed blob and its mirror: 20338 bytes and sha256 `5854eb042b5cc4916d1f01808e696df0bef1894d4b9e5f74ae4642621036a2aa` on both sides, EQUAL, with C0b's two paths one blob id `b358ea1b`. That original predates the worker, so the reading covers more than self-consistency; it does not and cannot cover an emission, because under this workflow there is none.

THE SUITES WERE RE-RUN BY THE REVIEWER, SERIALLY, IN THE PRIMARY CHECKOUT, and every count reproduced: `tests/docs/` 295 passed, the four state readers 119 passed together, `tests/ui_server/` 497 passed and the canary `tests/cli/test_golden_path.py` 42 passed, all at REAL exit 0. THE ONE DECLARED DEVIATION IS ACCEPTED AND IS THE REVIEWER'S OWN DEFECT: G7's residue over `BASE..C2` is non-empty at `.agent/handoff.md`, because that gate's range ends one commit before the commit that writes the handback while its change set names the file, so the clause was unmeetable by construction. The worker declared it instead of quietly dropping the path, which is the correct move.
<<<END GATEF257R1

<<<SLICE SLIPSF257R1
2026-08-28 · F257 R1 · The block's G4 reconstruction formula read "base + newline + DECF257D1 + newline + DECF257D2" while the same block's slice-convention paragraph required one BLANK LINE before each appended slice and a trailing newline; the two clauses disagreed, the worker followed the convention, and `.agent/decisions.md` is byte-correct on disk.

2026-08-28 · F257 R1 · The block's G7 structure gate ran over a range ending at C2 while its change set named `.agent/handoff.md`, which C3 writes, so the changeset-minus-range residue could never be empty; the worker reported the residue and declared it rather than dropping the path.
<<<END SLIPSF257R1

`PLANF257R2` is a WHOLE-FILE replacement of `.agent/plan.md`. `GATEF257R1` is an
APPEND to `.agent/live_review.md` and `SLIPSF257R1` an APPEND to
`.agent/prose_slips.md`, each under constraint 8. This round mints no finding id
and resolves none: the two entries above are reviewer-prose slips, which
operator amendment amend0827 rule 2 routes to `.agent/prose_slips.md` with no id,
no severity and no correction round.

### Done when

G1 HYGIENE. Read `.agent/STOP` from disk with `os.path.exists` before C0a and
again before C3; report both answers. If it exists at either reading, finish the
commit in hand, write the handback and stop. Report constraint 0's three
readings, and `git status --porcelain | wc -l` after each of C0a, C0b, C1, C2
and C3.

G2 TRANSPORT. One digest comparison, per the gate budget. Report sha256 and the
byte length of the committed blob `git show <C0a>:.agent/authored/f257-r2.md`
and of the reviewer's own original at `.remedy-wt/f257-r2-block.md`, and whether
they are EQUAL. That original was written before this worker existed, so the
reading covers more than self-consistency; it covers no emission, because this
workflow has none — say both things in the handback. Then report that
`git rev-parse <C0b>:.agent/authored/f257-r2.md` and
`git rev-parse <C0b>:.agent/last_block.md` print ONE blob id.

G3 THE PLAN AT C1. Byte equality only, per the gate budget: `.agent/plan.md` at
C1 equals PLANF257R2 including the trailing newline — report `True` or `False`.
Report `wc -l`, which must be under 50 (AGENTS.md), and the count of lines
exactly `## Goal` and exactly `## Next Steps`.

G4 THE RECORD APPEND AT C2, two readers, over `.agent/live_review.md`. (a)
Reconstruct the C2 blob from the `cbf081eb` blob and GATEF257R1 under constraint
8, and report `True` or `False`. NEGATIVE CONTROL: flip one byte at an offset
your script confirms lies INSIDE THE FIRST appended paragraph, recompute, and
report the equality is now `False`. (b) Split the C2 blob on blank lines; let N
be the number of paragraphs GATEF257R1 holds, COUNTED BY YOUR SCRIPT from the
slice itself and never taken from this block; report N, and report that the LAST
N units match those paragraphs IN ORDER, unit by unit. Report that the pre-round
blob is a byte PREFIX, with both byte lengths. Report separately that
`.agent/prose_slips.md` at C2 reconstructs from its `cbf081eb` blob and
SLIPSF257R1 under constraint 8, `True` or `False`.

G5 THE LEDGER AT C2. Report over `.agent/live_review.md`, at `cbf081eb` and
again at C2: the count of lines matching `^- R-\d+ — ` and whether they are all
DISTINCT; the count of `^Done: R-\d+ — `; the count of `^Landed: R-`; the count
of `^Gate: F\d+ R\d+ — `; and the size of the OPEN SET computed as the
registrations minus the resolutions. The first three and the open set must be
UNMOVED, and only the `Gate:` count may rise, by exactly one. Report the count
of lines matching `^Gate: F257 R1 — ` at C2, which must be 1.

G6 THE LOADER RED-PROOF AT C3, in a disposable worktree added at C3 under
`.remedy-wt/`, never in the primary checkout. Report the UNMUTATED CONTROL
FIRST, in that same worktree — a colour with no baseline is not evidence —
running `python3 -m pytest tests/orchestration/test_self_use_queue.py -q` and
reporting its REAL exit code and passed count. THE MUTATIONS, each applied alone
and reverted before the next, each in
`packages/orchestration/self_use_queue.py` inside the worktree, and each of
which must turn that file RED: (i) break S5 by making `load_self_use_queue`
return an empty tuple instead of raising when the file is missing; (ii) break S6
by making `next_self_use_item` answer the first item regardless of its
`consumed_by`. Report the exit code and the passed/failed counts for every run.
Then report the control again, green, with the module restored byte-clean, and
report `git worktree list` and `git status --porcelain | wc -l` in the primary
checkout after removal.

G7 THE SUITES AT C3. One pytest process at a time, from the repository root, in
the PRIMARY checkout, each with its REAL exit code and its own passed/failed
line: `tests/orchestration/test_self_use_queue.py`; the guards constraint 7
names, `tests/test_data_paths.py`, `tests/test_path_utils.py`,
`tests/regression/test_named_bugs.py` and
`tests/orchestration/test_development_artifact_boundary.py`; the state readers
`tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
`tests/regression/test_resource_safety.py` and
`tests/orchestration/test_integrity_gate.py`; the job-path neighbours
`tests/orchestration/test_job_promote.py` and
`tests/orchestration/test_fences.py`; and the canary
`tests/cli/test_golden_path.py`. Every one must be exit 0. If any is red, STOP
and write the handback with the full untruncated failure list.

G8 STRUCTURE, over `cbf081eb..<C3>` — the range that ends BEFORE the handback
commit, because C4's own numbers cannot exist while C4 is being written. The
change set above lists `.agent/handoff.md`, which C4 writes, so compute the
changeset-minus-range residue over the change set WITHOUT that path and report
which path you excluded; the range-minus-changeset residue is computed against
the full change set and must be empty. Report each commit's insertions from
`git diff --numstat`, each under 500, and that each of C0a, C0b, C1, C2 and C3
is single-parent. Report, counted affirmatively over each file's C3 content, the
number of lines beginning `<<<SLICE ` and `<<<END ` in `.agent/plan.md`,
`.agent/live_review.md`, `.agent/prose_slips.md`,
`scripts/self_use_queue.json`, `packages/orchestration/self_use_queue.py` and
`tests/orchestration/test_self_use_queue.py` — each expected 0 — beside the same
counts over `.agent/authored/f257-r2.md` as the non-zero control. Report
`git ls-files .remedy-wt | wc -l`, expected 0.

### Handback

Rewrite `.agent/handoff.md` in C4 per docs/agents/handback_template.md. It
carries: `SESSION 1 of feature F257 · round 2`; the range `cbf081eb..HEAD`; a
per-commit changed-files table whose `+/-` cells are taken from
`git diff --numstat` and compared cell by cell against the figures G8 reports;
ONE LINE PER GATE G1 through G8 with its real result; the deviations, including
every guard re-expression constraint 6 required; the item-status table with
every C-item and every gate appearing exactly once; and the next expected
action.

Do not write a `Done:` or `Gate:` paragraph of your own anywhere — GATEF257R1 is
reviewer-authored text you apply verbatim, and any OTHER such paragraph is a
finding however hedged.

After C4: push with `git push origin feature/f257-self-use-track` and report the
outcome. Do NOT create a pull request and do NOT merge anything.
