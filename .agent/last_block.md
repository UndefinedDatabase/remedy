### STEP T002 — F257 Self-use track, round 8 (CLOSURE PRECONDITION 6)

Goal: book the round 7 verdict — the built-state round PASSED — and then satisfy
closure precondition 6 for F257 itself. The first pending self-use item, SU-001,
is planned through `packages.orchestration.self_use_job` against THIS repository
and stops at the normal approval gate, with the real transcript committed as
evidence. F257 is the first feature ever required to consume a self-use item at
its own close, so this round is the one that proves the track rather than
describing it.

Base: `ba28d224`, the tip of `feature/f257-self-use-track` and the handback this
round starts from.

Bundle, in commit order:

- C0a save this block verbatim to `.agent/authored/f257-r8.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 advance `.agent/plan.md`
- C2 book the F257 R7 verdict into `.agent/live_review.md`
- C3 run the self-use item and commit the evidence under `.agent/selfuse_f257/`
- C4 rewrite `.agent/handoff.md`

Change set — these paths and nothing else:

- `.agent/authored/f257-r8.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `.agent/selfuse_f257/SU-001.md`
- `.agent/selfuse_f257/run.txt`
- `.agent/handoff.md`

NO file under `packages/`, `apps/`, `tests/` or `scripts/` is edited. In
particular `scripts/self_use_queue.json` is NOT edited: the `consumed_by` edit
belongs to the closure commit, and an item that could be marked consumed by its
own run would not be a gate — DECISION F257 D2 rules exactly this. NEITHER
`docs/roadmap/STATUS.md` NOR `README.md` is edited: the `[x]` flip and the README
capability sync are the closure commit's, a later round. `docs/` is not touched at
all this round. R-0734 and R-0736 stay registered and unrepaired on this branch.

WHAT THIS ROUND DOES NOT DO, AND WHY, because a reader will ask. It does NOT RUN
the job and does NOT write the documentation page SU-001 asks for. Precondition 6
requires the item to be "planned through `packages.orchestration.self_use_job`,
taken to the normal approval gate like any other job". The shipped module plans
only — its own docstring says "REMEDY DELIBERATELY DOES NOT RUN A JOB HERE" and
"Remedy deliberately does not PROMOTE a job here" — so planning to the gate and
stopping IS the whole of what the shipped code offers, and running the job would
also drop an unrelated docs page onto a feature branch, which AGENTS.md forbids.
The approval gate is the OPERATOR'S: the plan reaches it and waits. Say this
plainly in the handback rather than implying the page was written.

### Constraints

0. BEFORE ANYTHING: report `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
   — it was `[]` when this block was written, and if it is not `[]` now, STOP and
   hand back without committing. Report `git rev-parse HEAD`, which must equal
   `ba28d224`'s full sha, and `git branch --show-current`, which must be
   `feature/f257-self-use-track`. Create no branch and no pull request. Never
   force-push and never rewrite history.
1. Apply every authored slice BYTE FOR BYTE — no reflow, rewording, retitling,
   correction or shortening. If a slice looks wrong, apply it as written and say
   so in the handback's deviations; the record is repaired by a later append.
2. The delimiter lines `<<<SLICE …` and `<<<END …` are transport only and never
   reach a target file.
3. Extract every slice from the COMMITTED blob with
   `git show <C0a>:.agent/authored/f257-r8.md`, never from this prompt's text.
4. AGENTS.md binds in full: the self-review loop before every commit, one
   logical step per commit, `.agent/plan.md` current before every commit, a
   clean tree, and the push.
5. Shell forms rejected by this session's guard are RE-EXPRESSED, never skipped
   and never weakened. Loops, `$( )`, `${arr[0]}`, `cp`, brace literals
   containing quotes, and every form of environment-variable assignment are
   rejected by FORM; route such work through a scratch script under the
   gitignored `.remedy-wt/`, and copy with `shutil.copyfile`. Capture real exit
   codes with `bash -c '<cmd>; echo "REAL_EXIT=$?"'` or from `subprocess`. This
   Python is 3.10: an f-string expression may not contain a backslash, so hoist
   any regex into a named variable. Report every re-expression.
6. THE APPEND CONVENTION: an appended slice is separated from the text before it
   by exactly ONE BLANK LINE and the file ends with exactly one trailing
   newline. Concretely, for a target whose last byte is already a newline, write
   one newline then the slice, the slice carrying its own single terminator.
   This constraint is the authority on separators; if a gate formula below
   disagrees, follow this constraint and declare the disagreement.
7. THE OPEN SET IS COUNTED BY DISTINCT ID, as
   `len(set(registered ids) - set(resolved ids))`. It reads 255 at `ba28d224`.
   THIS ROUND REGISTERS NO ID AND RESOLVES NONE, so it must still read 255 at C2
   and the registered count must be UNMOVED at 297. A `Gate:` paragraph is not a
   registration.

### The authored slices

<<<SLICE PLANF257R8
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
| the queue file and its read-only loader | done | round 2, 18 tests |
| render a queue item and plan it on the real job path | done | round 3 |
| refuse a job file written outside its destination | done | round 4, R-0733 |
| consume exactly one item per feature close | done | round 4, precondition 6 |
| refuse an id that is not one file name | done | round 5, R-0735 |
| document the format where a reader looks | done | round 5 |
| the integration gate | done | round 6, PASSED, 18186 passed 0 failed |
| the feature file's Built State | done | round 7, precondition 4 |
| plan SU-001 and stop at the approval gate | done | this round, precondition 6 |
| the evidence bundle and the review zip | open | next |
| the closure commit and the PR | open | after the zip |

## Next Steps
1. Build the evidence bundle with
   `job_evidence.create_manual_completion_bundle(review_feature_id="f257")` and
   the review zip from a clean tree; record package, SHA-256 and archived path.
2. The closure commit — STATUS, README, the `scripts/self_use_queue.json`
   `consumed_by` edit that marks SU-001 consumed by F257, and the final `.agent/`
   state — then the PR. It is NOT merged in this session.

## Risks
- A job must never mark its own queue item consumed; neither shipped module owns
  a queue writer, and DECISION F257 D2 rules the consumption point.
- `docs/roadmap/STATUS.md` is in `scope_fences.BUILTIN_DENY` and stays there.
- R-0734 and R-0736 are registered and deliberately NOT repaired on this branch;
  both are outside F257's surface.
<<<END PLANF257R8

<<<SLICE GATEF257R7
Gate: F257 R7 — the BUILT-STATE round. THE ROUND PASSED. All eight gates were re-run by the reviewer at `ba28d224` from a script of its own, and every structural number reproduced exactly: transport EQUAL at sha256 `9b4e8f7f…508cad` over 23769 bytes with ONE blob id `165a8857…5741c` at C0b; the plan byte-equal at 2019 bytes over 40 lines with one `## Goal` and one `## Next Steps`; the record reconstructing 1396957 → 1402722 from GATEF257R6 (3502 bytes) then FINDF257R7 (2261 bytes), with the negative control failing at an offset the script proved lay inside the first appended paragraph and the pre-round blob a byte PREFIX of the result; the ledger registered 296 → 297 all DISTINCT, `Done:` 44 lines over 42 distinct ids and `Landed:` 11 both UNMOVED, `Gate:` 111 → 112, the open set 254 → 255; the feature file reconstructing 3156 → 7265 with BANNERFROM 1 → 0, BANNERTO 1, one Built State heading and it the LAST heading in the file; both residues empty over five SINGLE-PARENT commits of 340, 228, 11, 14 and 70 insertions; delimiters 0 and 0 in all three targets against a 6/6 control; `.remedy-wt` untracked at 0; and all four named paths ABSENT from the range.

THE SUITES WERE RE-RUN, NOT READ. `tests/docs/test_docs_consistency.py` 295 passed, `tests/orchestration/test_self_use_job.py` 18 passed, `tests/orchestration/test_self_use_queue.py` 18 passed, and the canary `tests/cli/test_golden_path.py` 42 passed — one pytest process at a time, every REAL exit 0, and the same four numbers the worker reported.

THE PROSE WAS GATED AS WELL AS THE SHAPE, WHICH IS THE HALF A RECONSTRUCTION CANNOT REACH. A byte-exact append proves that text LANDED, never that it is TRUE, so the Built State's claims were checked against disk one by one. `self_use_queue.py`'s public top-level definitions are EXACTLY the six the section names — read by AST rather than by grep, beside one private `_require` — and that module contains ZERO occurrences of `open(`, `write_text`, `json.dump` or any write mode, so "owns NO writer at all" is measured and not asserted; `^SU-\d{3}$` really is the id rule in it. `self_use_job.py` imports `plan_job_from_file` and carries both guards the section distinguishes. `docs/system/self-use-track-v1.md` exists, and `docs/README.md` carries it on exactly TWO rows — line 19 in the quick-find table and line 136 in the system table — which is the "twice" the section claims, though the raw string occurs four times because each row names it as link text and again as target. `scripts/self_use_queue.json` holds ONE item whose keys are exactly the five listed. Precondition 6 and the literal `self-use NONE (queue exhausted)` are both present in `docs/roadmap/STATUS_closure_protocol.md`. `job_promote.py` does keep promotion behind `--approve` and never auto-promotes. NO CLAIM IN THE SECTION WAS FOUND FALSE.

CLOSURE PRECONDITION 4 IS SATISFIED: the feature file's Built State is current, and the stale REGISTRATION-ONLY banner is gone at ZERO occurrences of "Nothing in this file has been implemented". What stands between F257 and its closure sequence is precondition 6 — the one no feature has ever had to meet.
<<<END GATEF257R7

`PLANF257R8` is a WHOLE-FILE replacement of `.agent/plan.md`. `GATEF257R7` is a
SINGLE APPEND to `.agent/live_review.md` under constraint 6. This round registers
nothing and resolves nothing.

### C3 — the self-use run

Do this in a scratch script under `.remedy-wt/`, not in the shell.

1. Read the queue through the SHIPPED loader, never by parsing the JSON yourself:
   `packages.orchestration.self_use_queue.default_self_use_queue_path`,
   `pending_self_use_items` and `next_self_use_item`. Record the ids BEFORE the
   run.
2. Call
   `packages.orchestration.self_use_job.plan_next_self_use_item(dest_dir, repo_path=<repo root>)`
   with `dest_dir` under the gitignored `.remedy-wt/` — NOT inside `.agent/`, so
   the run itself cannot dirty the tracked tree.
3. Copy the rendered job file to `.agent/selfuse_f257/SU-001.md` with
   `shutil.copyfile`.
4. Write `.agent/selfuse_f257/run.txt`: the FULL untruncated transcript of what
   you measured — every reading G6 asks for, the plan's `job_id` and `created_at`
   among them, plus a closing paragraph in your own words stating that the run
   stopped at the approval gate, that nothing was promoted, and that SU-001 is
   still PENDING. EVERY PATH IN THAT FILE IS WRITTEN RELATIVE TO THE REPOSITORY
   ROOT, never absolute: absolute paths in committed evidence are what the
   packaging metadata scanner rejects at zip time, and the zip is two rounds away.
5. Do NOT import or call `packages.orchestration.job_promote`. Do NOT call
   `do job-run`. Do NOT edit `scripts/self_use_queue.json`.

### Done when

G1 HYGIENE. Read `.agent/STOP` from disk with `os.path.exists` before C0a and
again before C3; report both answers. If it exists at either reading, finish the
commit in hand, write the handback and stop. Report constraint 0's three readings
and `git status --porcelain | wc -l` after each of C0a, C0b, C1, C2 and C3.

G2 TRANSPORT. One digest comparison. Report sha256 and the byte length of the
committed blob `git show <C0a>:.agent/authored/f257-r8.md` and of the reviewer's
own original at `.remedy-wt/f257-r8-block.md`, and whether they are EQUAL. That
original was written before this worker existed, so the reading covers more than
self-consistency; it covers no emission, because this workflow has none — say
both in the handback. Then report that
`git rev-parse <C0b>:.agent/authored/f257-r8.md` and
`git rev-parse <C0b>:.agent/last_block.md` print ONE blob id.

G3 THE PLAN AT C1. `.agent/plan.md` at C1 equals PLANF257R8 including the
trailing newline — report `True` or `False`, with the byte length of each side.
Report `wc -l`, under 50, and the count of lines exactly `## Goal` and exactly
`## Next Steps`.

G4 THE RECORD APPEND AT C2. Reconstruct the C2 blob of `.agent/live_review.md`
from the `ba28d224` blob plus GATEF257R7 under constraint 6, and report `True` or
`False` with all three lengths. NEGATIVE CONTROL: flip one byte at an offset your
script CONFIRMS lies inside the appended text, recompute, and report the equality
is now `False`. Report that the pre-round blob is a byte PREFIX, with both
lengths, and that the C2 blob ends in exactly ONE newline.

G5 THE LEDGER AT C2, counted under constraint 7. Report over
`.agent/live_review.md` at `ba28d224` and again at C2: the count of lines matching
`^- R-\d+ — ` and whether all are DISTINCT; the count of `^Done: R-\d+ — ` lines
AND the count of DISTINCT ids among them, as two separate numbers; the count of
`^Landed: R-`; the count of `^Gate: F\d+ R\d+ — `; and the OPEN SET as
`len(set(registered) - set(resolved))`. Expected: registered UNMOVED at 297 and
all distinct, the `Done:` numbers and `Landed:` UNMOVED, `Gate:` 112 → 113, and
the open set UNMOVED at 255. Report the count of `^Gate: F257 R7 — ` at C2, which
must be 1.

G6 THE SELF-USE RUN AT C3. This is the round's substance; report every reading.
(a) THE RENDERED BYTES ARE THE CURATED BYTES: `.agent/selfuse_f257/SU-001.md` at
C3 is byte-identical to the SU-001 `job_markdown` of `scripts/self_use_queue.json`
at `ba28d224` encoded UTF-8 — report `True` or `False`, both byte lengths, and
the sha256 of each side. (b) Report the plan's own `job_file_sha256` and whether
it EQUALS that same digest; this is the reading that proves nothing was templated
between the queue and the plan. (c) Report `plan.status`, which must be `planned`;
`plan.job_title`, which must be `Document the Markdown job-file format`; the list
`[t.task_id for t in plan.tasks]`, which must be exactly `['T001']`; and
`plan.repo_path`, which must resolve to this repository's root. (d) Report the
plan's `job_id` and `created_at` — NO EXPECTED VALUE IS STATED FOR EITHER, because
both are freshly minted per run and a block that ordered them would be ordering
something it cannot know. (e) THE RUN DID NOT CONSUME ITS OWN ITEM: report
`next_self_use_item().id` and the ids from `pending_self_use_items()` BOTH BEFORE
and AFTER the run — `SU-001` and `['SU-001']` at both readings — and report
`git status --porcelain scripts/self_use_queue.json`, which must be EMPTY.
(f) NOTHING WAS PROMOTED: report the count of the string `job_promote` in your own
run script, expected 0, beside `plan.status` again, which is `planned` and never
`promoted`. (g) Report `git status --porcelain | wc -l` immediately after the run
and BEFORE C3 stages anything, expected 0 — the run wrote only into the gitignored
`.remedy-wt/`. (h) Report the byte length of `.agent/selfuse_f257/run.txt` and the
count of occurrences of the string `/home/` in it, which must be 0.

G7 THE SUITES AT C3. One pytest process at a time, from the repository root, in
the PRIMARY checkout, each with its REAL exit code and its own passed/failed line.
CONFIRM FIRST that every path below resolves on disk and report the empty list,
because `pytest <missing path>` exits 4 and says almost nothing:
`tests/orchestration/test_self_use_job.py`;
`tests/orchestration/test_self_use_queue.py`;
`tests/docs/test_docs_consistency.py`; and the canary
`tests/cli/test_golden_path.py`. Every one must be exit 0. If any is red, STOP and
write the handback with the full untruncated failure list.

G8 STRUCTURE, over `ba28d224..<C3>` — the range that ends BEFORE the handback
commit, because C4's own numbers cannot exist while C4 is being written. The
change set lists `.agent/handoff.md`, which C4 writes, so compute the
changeset-minus-range residue over the change set WITHOUT that path and name the
path you excluded; the range-minus-changeset residue is computed against the full
change set and must be empty. Report each commit's insertions from
`git diff --numstat`, each under 500, and that each of C0a, C0b, C1, C2 and C3 is
single-parent. Report, counted affirmatively over each file's C3 content, the
number of lines beginning `<<<SLICE ` and `<<<END ` in `.agent/plan.md`,
`.agent/live_review.md`, `.agent/selfuse_f257/SU-001.md` and
`.agent/selfuse_f257/run.txt` — each expected 0 — beside the same counts over
`.agent/authored/f257-r8.md` as the non-zero control. Report
`git ls-files .remedy-wt | wc -l`, expected 0. Report the `git diff --numstat`
line for `scripts/self_use_queue.json`, `docs/roadmap/STATUS.md`, `README.md`,
`packages/orchestration/self_use_job.py` and `docs/system/self-use-track-v1.md`
over the range, all five expected ABSENT.

### Handback

Rewrite `.agent/handoff.md` in C4 per docs/agents/handback_template.md. It
carries: `SESSION 3 of feature F257 · round 8`; the roster of this session's
rounds, this round included; the range `ba28d224..HEAD`; a per-commit
changed-files table whose `+/-` cells are taken from `git diff --numstat`; ONE
LINE PER GATE G1 through G8 with its real result; the deviations, including every
guard re-expression constraint 5 required; the item-status table with every
C-item and every gate appearing exactly once; the open-findings count, which must
be 255; and the next expected action — the evidence bundle and the review zip,
built from a clean tree, then the closure commit and the PR.

State plainly in the deviations that the job was PLANNED and NOT RUN, that the
documentation page SU-001 asks for was NOT written, and why: the shipped module
plans only and the approval gate is the operator's. A handback that lets a reader
believe the page exists is a finding however hedged.

Do not write a `Done:` or `Gate:` paragraph of your own anywhere — GATEF257R7 is
reviewer-authored text you apply verbatim, and any OTHER such paragraph is a
finding however hedged.

After C4: push with `git push origin feature/f257-self-use-track` and report the
outcome. Do NOT create a pull request and do NOT merge anything.
