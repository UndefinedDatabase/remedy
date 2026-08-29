### STEP T002 — F257 Self-use track, round 11 (THE PACKAGE, REBUILT AT THE REPAIRED HEAD)

Goal: book the round 10 verdict, record one reviewer-prose slip, and rebuild the
evidence bundle and the review zip at the repaired head. Round 9's package
recorded `506bbab5` as the accepted HEAD; round 10 landed a commit under `tests/`,
so that package no longer covers the head being closed and a fresh one is built
here. This round does NOT close the feature: no `[x]`, no README sync, no
`consumed_by` edit, no pull request.

Base: `260b42c4`, the tip of `feature/f257-self-use-track` and the handback this
round starts from.

Bundle, in commit order:

- C0a save this block verbatim to `.agent/authored/f257-r11.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 advance `.agent/plan.md`
- C2 book the F257 R10 verdict into `.agent/live_review.md`
- C3 append one line to `.agent/prose_slips.md`
- then PUSH, and build the bundle and the zip from the clean tree at C3
- C4 rewrite `.agent/handoff.md`

Change set — these paths and nothing else:

- `.agent/authored/f257-r11.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `.agent/prose_slips.md`
- `.agent/handoff.md`

THE EVIDENCE DIRECTORY IS NEVER COMMITTED and neither is the zip; both are
gitignored, and a committed evidence dir puts evidence files into the review
subject and packages BLOCKED_EVIDENCE. NO file under `packages/`, `apps/`,
`tests/`, `scripts/` or `docs/` is edited. `docs/roadmap/STATUS.md`, `README.md`
and `scripts/self_use_queue.json` are NOT touched.

ACCEPTED HEAD IS C3. The zip is built after C3 is committed and pushed, so the
manifest's `committed_review_subject.head_commit` is C3's full sha. C4 writes only
`.agent/handoff.md` and follows the READY package. Report C3's full sha as the
accepted HEAD; the next round's STATUS line carries it.

THE SUPERSEDED PACKAGE IS LEFT ALONE. `remedy-review-20260829-025133-READY_FOR_REVIEW.zip`
already sits in `/home/decodeux/Repos/remedy-history/zips`. DELETE NOTHING there —
it is the operator's archive, and nothing in this round needs the space. State in
the handback, by exact filename, which package is SUPERSEDED and which is LIVE.

### Constraints

0. BEFORE ANYTHING: report `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
   — it was `[]` when this block was written, and if it is not `[]` now, STOP and
   hand back without committing. Report `git rev-parse HEAD`, which must equal
   `260b42c4`'s full sha, and `git branch --show-current`, which must be
   `feature/f257-self-use-track`. Create no branch and no pull request. Never
   force-push and never rewrite history.
1. Apply every authored slice BYTE FOR BYTE — no reflow, rewording, retitling,
   correction or shortening. If a slice looks wrong, apply it as written and say
   so in the handback's deviations; the record is repaired by a later append.
2. The delimiter lines `<<<SLICE …` and `<<<END …` are transport only and never
   reach a target file.
3. Extract every slice from the COMMITTED blob with
   `git show <C0a>:.agent/authored/f257-r11.md`, never from this prompt's text.
4. AGENTS.md binds in full: the self-review loop before every commit, one
   logical step per commit, `.agent/plan.md` current before every commit, a
   clean tree, and the push. AGENTS.md also requires that EVERY artifact-build
   attempt — bundle, zip, and the deliberate red control below — appears in the
   handback with its status, failed attempts included with the blocking reason.
5. Shell forms rejected by this session's guard are RE-EXPRESSED, never skipped
   and never weakened. Loops, `$( )`, `${arr[0]}`, `cp`, brace literals
   containing quotes, and every form of environment-variable assignment are
   rejected by FORM; route such work through a scratch script under the
   gitignored `.remedy-wt/`, and copy with `shutil.copyfile` or, for a directory,
   `shutil.copytree`. Capture real exit codes with
   `bash -c '<cmd>; echo "REAL_EXIT=$?"'` or from `subprocess`. This Python is
   3.10: an f-string expression may not contain a backslash, so hoist any regex
   into a named variable. Report every re-expression.
6. THE APPEND CONVENTION: an appended slice is separated from the text before it
   by exactly ONE BLANK LINE and the file ends with exactly one trailing
   newline. Concretely, for a target whose last byte is already a newline, write
   one newline then the slice, the slice carrying its own single terminator.
   This constraint is the authority on separators; if a gate formula below
   disagrees, follow this constraint and declare the disagreement.
7. THE OPEN SET IS COUNTED BY DISTINCT ID, as
   `len(set(registered ids) - set(resolved ids))`. It reads 256 at `260b42c4`.
   THIS ROUND REGISTERS NO ID AND RESOLVES NONE, so it must still read 256 at C2
   and the registered count must be UNMOVED at 298. A `Gate:` paragraph is not a
   registration, and `.agent/prose_slips.md` never carries an id at all.
8. EXIT CODE 0 IS NEVER THE READING FOR THE ZIP. `scripts/make_review_zip.sh`
   exits 0 for a BLOCKED_EVIDENCE package as readily as for a READY one. The
   reading is `PACKAGE_STATUS` in the printed output and `package_status` in
   `.review_zip_manifest.json`. A handback that reports the zip green on an exit
   code is a finding.

### The authored slices

<<<SLICE PLANF257R11
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
| plan SU-001 and stop at the approval gate | done | round 8, precondition 6 |
| three tests survive their own feature's close | done | round 10, R-0737 |
| the evidence bundle and the review zip | done | this round, at the repaired head |
| the closure commit and the PR | open | next, and it is the last round |

## Next Steps
1. The closure commit, in ONE commit: the `[x]` flip on `docs/roadmap/STATUS.md`,
   the README accepted count, its `Next:` clause, the tier-5 Done cell, the README
   capability paragraph, the `scripts/self_use_queue.json` `consumed_by` edit and
   the final `.agent/` state.
2. Open the pull request. It is NOT merged in this session — the gap is the
   operator's manual-review window, and the next feature's Open PR Gate merges it.

## Risks
- A job must never mark its own queue item consumed; neither shipped module owns
  a queue writer, and DECISION F257 D2 rules the consumption point.
- `docs/roadmap/STATUS.md` is in `scope_fences.BUILTIN_DENY` and stays there.
- R-0734 and R-0736 are registered and deliberately NOT repaired on this branch;
  both are outside F257's surface.
- The queue holds ONE item, so F257's own close EXHAUSTS it. The next feature's
  close records `self-use NONE (queue exhausted)` until an operator curates more.
<<<END PLANF257R11

<<<SLICE GATEF257R10
Gate: F257 R10 — THE CLOSURE BLOCKER, found by dry-running the closure commit before authoring it. THE ROUND PASSED AND R-0737 IS REPAIRED. THE RED-PROOF WAS REPRODUCED BY THE REVIEWER IN ITS OWN DISPOSABLE WORKTREE, not read out of the handback, and it is the reading this round turns on: `python3 -B -m pytest tests/orchestration/test_self_use_queue.py tests/orchestration/test_self_use_job.py -q`, the same command against the same two suites, four times — (A) at `5cb48adc` with the queue PENDING, REAL exit 0, `36 passed`; (B) at `5cb48adc` with SU-001's `consumed_by` set to `F257` in the WORKTREE ONLY, REAL exit 1, `3 failed, 33 passed`, the three being `TestPlanSelfUseItem::test_the_shipped_item_plans_with_its_title_and_tasks`, `TestPlanSelfUseItem::test_the_shipped_item_plans_to_exactly_one_task_with_acceptance` and `TestPlanNextSelfUseItem::test_it_returns_the_shipped_pending_item`; (C) at C3 `ceac0e3a` with the queue PENDING, REAL exit 0, `36 passed`; (D) at C3 with the queue EXHAUSTED, REAL exit 0, `36 passed`. The ONLY difference between (B) and (D) is the commit. A gate that cannot show the red proves nothing, and this one showed it.

THE REPAIR WAS READ AS A DIFF, LINE BY LINE, AND IT REMOVES NOTHING. `load_self_use_queue` was added to the existing import block in alphabetical position. The first two tests take `load_self_use_queue()[0]` — the shipped queue's first item in file order, which `consumed_by` does not affect — and keep every assertion they carried: `path.exists()`, `plan.error == ""`, the job title, the task count, the task id `T001` and the non-empty acceptance. The one assertion whose MESSAGE changed is the one the block ordered changed, from "the shipped queue has no pending item" to an emptiness claim, because the test no longer asks about pending-ness. The third test is renamed to `test_it_plans_the_pending_item_or_raises_when_the_queue_is_exhausted` and asserts the invariant in BOTH directions — an exhausted queue must RAISE `SelfUseJobError` rather than answer `None`, and a pending queue plans that exact item under all four of its original assertions. No test was deleted, skipped or weakened, no `xfail` was added, and the file collects 18 tests before and after.

THE STRUCTURE REPRODUCED EXACTLY. Transport EQUAL at sha256 `a46995eb…797640` over 23379 bytes with ONE blob id at C0b; the plan byte-equal at 2559 bytes over 47 lines; the record reconstructing 1409456 → 1415933 from GATEF257R9 then FINDF257R10 applied in that order, the negative control failing as it must and the pre-round blob a byte PREFIX; the ledger registered 297 → 298 all DISTINCT, `Done:` 44 over 42 and `Landed:` 11 UNMOVED, `Gate:` 114 → 115, the open set 255 → 256 — exactly the one id this round registers; both residues empty over five SINGLE-PARENT commits of 305, 195, 13, 14 and 15 insertions; `.remedy-wt` untracked at 0; and `scripts/self_use_queue.json`, `docs/roadmap/STATUS.md`, `README.md` and `packages/orchestration/self_use_job.py` all ABSENT from the range — in particular the queue file, whose edit belongs to the closure commit and which the red-proof touched only inside a worktree that was removed by exact path.

THE SUITES AND THE LINTER WERE RUN BY THE REVIEWER IN THE PRIMARY CHECKOUT: `test_self_use_job.py` 18 passed, `test_self_use_queue.py` 18 passed, `test_docs_consistency.py` 295 passed, the canary `test_golden_path.py` 42 passed, and `python3 -m ruff check` on the repaired file printed `All checks passed!` — every REAL exit 0, one process at a time.

THE WORKER FOUND A CONTRADICTION IN THE BLOCK'S OWN CLAUSES AND HANDLED IT CORRECTLY. G6(D) asked for the three failing ids "among the passing ones" while C3 step 3 ordered the third of them renamed; both could not hold literally. It reported the id under its post-rename name and declared the disagreement instead of silently picking one. That is the reviewer's slip, not the worker's, and it is recorded in `.agent/prose_slips.md` this round under amend0827 rule 2 — no id is spent on it, because nothing on disk is wrong.
<<<END GATEF257R10

<<<SLICE SLIPF257R11
2026-08-29 · F257 R10 · The block's G6(D) asked for the three ids from the negative control to appear "among the passing ones" while its own C3 step 3 ordered the third of those tests renamed, so the two clauses could not both hold literally; the worker reported that id under its post-rename name and declared the disagreement, which is the required behaviour.
<<<END SLIPF257R11

`PLANF257R11` is a WHOLE-FILE replacement of `.agent/plan.md`. `GATEF257R10` is a
SINGLE APPEND to `.agent/live_review.md` at C2 under constraint 6. `SLIPF257R11`
is a SINGLE APPEND to `.agent/prose_slips.md` at C3 under constraint 6. This round
registers nothing and resolves nothing.

### The evidence script — ADAPTED FROM THE COMMITTED TEMPLATE, NOT WRITTEN FRESH

Extract the slice named `EVIDENCESCRIPT` from the COMMITTED blob
`git show HEAD:.agent/authored/f009-r33.md` by its `<<<SLICE EVIDENCESCRIPT` and
`<<<END EVIDENCESCRIPT` marker lines, save it to `.remedy-wt/f257_evidence_r11.py`,
and change ONLY the values below. Every other line stays BYTE FOR BYTE — the
double path scrub in `_tail`, node ids from `--collect-only`, the
`len(node_ids) == selected` assert, the sorted `test_files`, the `_unsafe_text`
pre-scan with its red control and the `OUTPUT_HASH` re-derivation are all
load-bearing, each paid for by a closure that was blocked without it.

- `EVIDENCE_DIR` → `<REPO>/.remedy-wt/f257_closure_evidence_r11/remedy-job-evidence-f257-closure`.
  It is a FRESH directory, deliberately not round 9's, so no stale artifact from
  the superseded bundle can be packaged.
- `BASE` → `f17b1d0d03e4042df8452b2019b719cbe4704b21`, the merge base with `main`,
  unchanged from round 9 and 40 characters, which the template asserts.
- the `runs = [...]` list → exactly these four, in this order, no `-k` and no
  deselection:
  - `mkrun("vr-0001", "tests/orchestration/test_self_use_queue.py", 18)`
  - `mkrun("vr-0002", "tests/orchestration/test_self_use_job.py", 18)`
  - `mkrun("vr-0003", "tests/docs/test_docs_consistency.py", 295)`
  - `mkrun("vr-0004", "tests/cli/test_golden_path.py", 42)`
- the `create_manual_completion_bundle(...)` keyword arguments:
  `job_id="f257-closure"`, `job_title="F257 Self-use track - closure"`,
  `step_range="T001-T002"`, `prior_job_ids=["f256-closure"]`, `num_tasks=2`,
  `note_prefix="operator-attested manual completion - F257 closure"`,
  `review_feature_id="f257"`.

`HEAD` is computed by the template at run time and must come out as C3's full sha;
report it. A verification record may NEVER carry a full-suite node-id list —
`len(node_ids) == selected` forbids filtering and the metadata scan rejects this
repository's redaction-torture ids by design (the F080 R4 lesson). The full-suite
proof rides in `.agent/gate_f257_r6/` and the reviewer's own re-runs.

### The zip, the red control and the archive

1. Confirm the tree is clean and the branch is pushed, then build with
   `bash scripts/make_review_zip.sh --evidence-dir <the EVIDENCE_DIR above>`.
   Report `PACKAGE_STATUS`, the zip filename and its SHA-256, computed by you over
   the file on disk and not merely copied from the script's output.
2. THE RED CONTROL. Copy the evidence directory to a SECOND directory under
   `.remedy-wt/`, append ONE node id containing an absolute path to the first run
   of that copy's `verification_tests.json`, and build a zip from the COPY. It
   must report `PACKAGE_STATUS=BLOCKED_EVIDENCE` at REAL exit code 0 — report the
   exit code beside the status to make the point that the status is the reading,
   and report the `ready_gate_matrix.blocking_reasons` list from the control's
   manifest, untruncated. Declare this attempt in the handback as a DELIBERATE
   CONTROL. The real bundle is not touched by it.
3. The script writes into `/home/decodeux/Repos/remedy-history/zips` directly. If
   the READY zip is already there when the build finishes, no move is needed — say
   so; if it is not, move it there with `shutil.move`. Either way report the
   absolute path the live package occupies and confirm the file exists there.
4. DELETE NOTHING in that archive directory. Name, by exact filename, the
   SUPERSEDED package from round 9 and the LIVE package from this round.

### Done when

G1 HYGIENE. Read `.agent/STOP` from disk with `os.path.exists` before C0a and
again before the zip build; report both answers. If it exists at either reading,
finish the commit in hand, write the handback and stop. Report constraint 0's
three readings and `git status --porcelain | wc -l` after each of C0a, C0b, C1, C2
and C3, and again immediately BEFORE the zip build, where it must be 0.

G2 TRANSPORT. One digest comparison. Report sha256 and the byte length of the
committed blob `git show <C0a>:.agent/authored/f257-r11.md` and of the reviewer's
own original at `.remedy-wt/f257-r11-block.md`, and whether they are EQUAL. That
original was written before this worker existed, so the reading covers more than
self-consistency; it covers no emission, because this workflow has none — say
both in the handback. Then report that
`git rev-parse <C0b>:.agent/authored/f257-r11.md` and
`git rev-parse <C0b>:.agent/last_block.md` print ONE blob id.

G3 THE PLAN AT C1. `.agent/plan.md` at C1 equals PLANF257R11 including the
trailing newline — report `True` or `False`, with the byte length of each side.
Report `wc -l`, under 50, and the count of lines exactly `## Goal` and exactly
`## Next Steps`.

G4 THE TWO RECORD APPENDS, each reconstructed separately and each with its own
negative control. (a) Reconstruct the C2 blob of `.agent/live_review.md` from the
`260b42c4` blob plus GATEF257R10 under constraint 6 — report `True` or `False`
with all three lengths, flip one byte at an offset your script CONFIRMS lies
inside the appended text and report the equality is now `False`, and report that
the pre-round blob is a byte PREFIX and that the C2 blob ends in exactly ONE
newline. (b) Do the same for `.agent/prose_slips.md` at C3 against its `260b42c4`
blob plus SLIPF257R11. Report the count of lines in the C3 blob of
`.agent/prose_slips.md` matching `^2026-\d\d-\d\d · F257 R10 · `, which must be 1,
and the count matching `^- R-`, which must be 0 — that file never carries an id.

G5 THE LEDGER AT C2, counted under constraint 7. Report over
`.agent/live_review.md` at `260b42c4` and again at C2: the count of lines matching
`^- R-\d+ — ` and whether all are DISTINCT; the count of `^Done: R-\d+ — ` lines
AND the count of DISTINCT ids among them, as two separate numbers; the count of
`^Landed: R-`; the count of `^Gate: F\d+ R\d+ — `; and the OPEN SET as
`len(set(registered) - set(resolved))`. Expected: registered UNMOVED at 298 and
all distinct, the `Done:` numbers and `Landed:` UNMOVED, `Gate:` 115 → 116, and
the open set UNMOVED at 256. Report the count of `^Gate: F257 R10 — ` at C2, which
must be 1.

G6 THE EVIDENCE BUNDLE. (a) Report the unified diff between the template slice
`EVIDENCESCRIPT` and your adapted `.remedy-wt/f257_evidence_r11.py`, and the count
of changed lines: ONLY the values the section above lists may differ, and the
handback names each changed line. (b) Report, per verification run, `run_id`,
`selected`, `len(node_ids)`, whether `len(node_ids) == selected`, `passed`,
`failed`, `skipped`, `deselected`, and `test_files` with whether that list is
SORTED. Expected passes: 18, 18, 295, 42, with failed, skipped and deselected 0
everywhere. (c) Report the `_unsafe_text` pre-scan result over every node id and
every command — expected 0 rejected — BESIDE its red control on a fabricated
absolute-path id, which must read True. (d) Report the full list of files the
producer wrote into the evidence directory and confirm all eight closed-schema
gates are present: `final_verifier_report`, `fresh_evidence`, `artifact_contract`,
`change_provenance`, `manifest_integrity`, `postmortem_integrity`,
`commit_execution` and `runtime_integration`. (e) Report, per run, whether
`output_hash` equals sha256 of `stdout_summary` EXACTLY. (f) Report the `HEAD` the
template computed and confirm it equals C3's full sha.

G7 THE REVIEW ZIP, read under constraint 8. (a) Report the zip filename, its
SHA-256 computed by you over the file on disk, the REAL exit code of the build,
and `PACKAGE_STATUS`, which must be `READY_FOR_REVIEW`. (b) From
`.review_zip_manifest.json` INSIDE the zip report `package_status`,
`ready_gate_matrix.ok`, `ready_gate_matrix.blocking_reasons` — expected empty —
`committed_review_subject.head_commit`, which must equal C3's FULL sha, and
`committed_review_subject.base_commit`, which must equal
`f17b1d0d03e4042df8452b2019b719cbe4704b21`; report C3's full sha beside it.
(c) THE RED CONTROL: report the control build's `PACKAGE_STATUS`, which must be
`BLOCKED_EVIDENCE`, its REAL exit code, expected 0, and its untruncated
`ready_gate_matrix.blocking_reasons` — then state plainly that the exit code did
not distinguish the two builds and the status did. (d) Report the absolute path
the LIVE package occupies, that the file exists there, its size in bytes, and the
exact filename of the SUPERSEDED round 9 package, which is left in place.
(e) Report `git status --porcelain | wc -l` after all of it, which must be 0.

G8 STRUCTURE AND THE REMAINING PRECONDITIONS, over `260b42c4..<C3>`. The change
set lists `.agent/handoff.md`, which C4 writes, so compute the
changeset-minus-range residue over the change set WITHOUT that ONE path and name
the path you excluded; the range-minus-changeset residue is computed against the
FULL change set and must be empty. Report each commit's insertions from
`git diff --numstat`, each under 500, and that each of C0a, C0b, C1, C2 and C3 is
single-parent. Report the number of lines beginning `<<<SLICE ` and `<<<END ` in
`.agent/plan.md`, `.agent/live_review.md` and `.agent/prose_slips.md` at C3 — each
expected 0 — beside the same counts over `.agent/authored/f257-r11.md` as the
non-zero control. Report `git ls-files .remedy-wt | wc -l`, expected 0, and the
count of tracked paths matching `remedy-job-evidence`, expected 0. Report the
`git diff --numstat` line over the range for `docs/roadmap/STATUS.md`,
`README.md`, `scripts/self_use_queue.json` and
`tests/orchestration/test_self_use_job.py`, all four expected ABSENT. Finally,
PRECONDITION 3: run
`from packages.orchestration.integrity_gate import run_integrity_checks` and
report `result.passed` and `result.fail_count` — it answers an
`IntegrityGateResult` OBJECT with attributes, not a dict, so `.get(...)` raises.

### Handback

Rewrite `.agent/handoff.md` in C4 per docs/agents/handback_template.md. It
carries: `SESSION 3 of feature F257 · round 11`; the roster of this session's
rounds, this round included; the range `260b42c4..HEAD`; a per-commit
changed-files table whose `+/-` cells are taken from `git diff --numstat`; ONE
LINE PER GATE G1 through G8 with its real result; the deviations, including every
guard re-expression constraint 5 required; the item-status table with every
C-item and every gate appearing exactly once; the open-findings count, which must
be 256; and the next expected action — the closure commit and the pull request.

It ALSO carries, as the values the next round needs and cannot re-derive, written
as a short labelled list: `Evidence job f257-closure`, the LIVE package filename,
its SHA-256, the absolute archived path, the ACCEPTED HEAD which is C3's full sha,
and the exact filename of the SUPERSEDED round 9 package. The next round's STATUS
line is authored from those values and `.agent/handoff.md` is the only carrier
between the two rounds.

Do not write a `Done:` or `Gate:` paragraph of your own anywhere — GATEF257R10 is
reviewer-authored text you apply verbatim, and any OTHER such paragraph is a
finding however hedged. Do not flip any checkbox to `[x]`. Do not create a pull
request and do not merge anything.

After C4: push with `git push origin feature/f257-self-use-track` and report the
outcome.
