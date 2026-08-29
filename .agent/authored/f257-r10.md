### STEP T002 — F257 Self-use track, round 10 (THE CLOSURE BLOCKER)

Goal: book the round 9 verdict, register R-0737, and REPAIR IT. The reviewer
dry-ran the closure commit's own edits in a throwaway worktree and found that
three tests on F257's own surface go RED the moment F257 closes: they require the
shipped queue to hold a PENDING item, and closure precondition 6 consumes exactly
that item. The feature cannot satisfy its own closure rule without turning its own
suite red. This round makes those three tests state-independent so the closure
commit can land green.

THIS ROUND SUPERSEDES ROUND 9'S PACKAGE. The zip built at `506bbab5` recorded
that commit as the accepted HEAD; a repair under `tests/` is a CONTENT commit, so
the accepted HEAD moves and the package must be rebuilt at the new head. That
rebuild is the NEXT round. Do not close anything here.

Base: `5cb48adc`, the tip of `feature/f257-self-use-track` and the handback this
round starts from.

Bundle, in commit order:

- C0a save this block verbatim to `.agent/authored/f257-r10.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 advance `.agent/plan.md`
- C2 book the F257 R9 verdict AND register R-0737 into `.agent/live_review.md`
- C3 repair `tests/orchestration/test_self_use_job.py`
- C4 rewrite `.agent/handoff.md`

Change set — these paths and nothing else:

- `.agent/authored/f257-r10.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `tests/orchestration/test_self_use_job.py`
- `.agent/handoff.md`

`scripts/self_use_queue.json` IS NOT EDITED IN THE PRIMARY CHECKOUT. The
`consumed_by` edit belongs to the closure commit, and this round only SIMULATES it
inside a disposable worktree to prove the repair. No file under `packages/`,
`apps/`, `docs/` or `scripts/` is edited, and no test is deleted, skipped or
weakened: the three tests keep every assertion they carry and change only WHERE
they get their entry from. `docs/roadmap/STATUS.md` and `README.md` are NOT
touched.

### Constraints

0. BEFORE ANYTHING: report `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
   — it was `[]` when this block was written, and if it is not `[]` now, STOP and
   hand back without committing. Report `git rev-parse HEAD`, which must equal
   `5cb48adc`'s full sha, and `git branch --show-current`, which must be
   `feature/f257-self-use-track`. Create no branch and no pull request. Never
   force-push and never rewrite history.
1. Apply every authored slice BYTE FOR BYTE — no reflow, rewording, retitling,
   correction or shortening. If a slice looks wrong, apply it as written and say
   so in the handback's deviations; the record is repaired by a later append.
2. The delimiter lines `<<<SLICE …` and `<<<END …` are transport only and never
   reach a target file.
3. Extract every slice from the COMMITTED blob with
   `git show <C0a>:.agent/authored/f257-r10.md`, never from this prompt's text.
4. AGENTS.md binds in full: the self-review loop before every commit, one
   logical step per commit, `.agent/plan.md` current before every commit, a
   clean tree, and the push.
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
   `len(set(registered ids) - set(resolved ids))`. It reads 255 at `5cb48adc`.
   This round registers ONE id and resolves none, so it must read 256 at C2 and
   the registered count must read 298.
8. DESTRUCTIVE VERIFICATION IS ISOLATED. Every measurement that needs the queue
   EXHAUSTED happens inside a `git worktree add --detach` worktree under
   `.remedy-wt/`, never in the primary checkout, which satisfies
   `git status --porcelain` empty at every commit. Remove that worktree by its
   EXACT PATH when done — never by glob — and report `git worktree list`
   afterwards.

### The authored slices

<<<SLICE PLANF257R10
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
| the evidence bundle and the review zip | superseded | round 9; the head moves |
| three tests survive their own feature's close | done | this round, R-0737 |
| rebuild the bundle and the zip at the new head | open | next |
| the closure commit and the PR | open | after the rebuilt zip |

## Next Steps
1. Rebuild the evidence bundle and the review zip at the repaired head; the
   package from round 9 recorded `506bbab5` as the accepted HEAD and a content
   commit has landed since, so it no longer covers the head being closed.
2. The closure commit, in ONE commit: the `[x]` flip on `docs/roadmap/STATUS.md`,
   the README accepted count, its `Next:` clause, the tier-5 Done cell, the README
   capability paragraph, the `scripts/self_use_queue.json` `consumed_by` edit and
   the final `.agent/` state. Then the PR, unmerged.

## Risks
- A job must never mark its own queue item consumed; neither shipped module owns
  a queue writer, and DECISION F257 D2 rules the consumption point.
- `docs/roadmap/STATUS.md` is in `scope_fences.BUILTIN_DENY` and stays there.
- R-0734 and R-0736 are registered and deliberately NOT repaired on this branch;
  both are outside F257's surface.
- The queue holds ONE item, so F257's own close EXHAUSTS it. The next feature's
  close records `self-use NONE (queue exhausted)` until an operator curates more.
<<<END PLANF257R10

<<<SLICE GATEF257R9
Gate: F257 R9 — THE PACKAGE ROUND, closure-protocol algorithm steps 1 and 2. THE ROUND PASSED AND THE PACKAGE BUILT READY_FOR_REVIEW. Every gate was re-executed by the reviewer at `5cb48adc` from a script of its own. Transport EQUAL at sha256 `4d995a0a…8e9d133` over 22597 bytes with ONE blob id `3305242c…6562` at C0b; the plan byte-equal at 2177 bytes over 42 lines; the record reconstructing 1405901 → 1409456 from GATEF257R8 alone, the negative control failing at an offset proved inside the appended text; the ledger registered UNMOVED at 297 all DISTINCT, `Done:` 44 over 42 and `Landed:` 11 UNMOVED, `Gate:` 113 → 114, the open set UNMOVED at 255; both residues empty over four SINGLE-PARENT commits of 331, 198, 9 and 10 insertions; delimiters 0 and 0 in both targets against a 2/2 control; `.remedy-wt` untracked at 0; `git ls-files` carrying ZERO `remedy-job-evidence` paths, so the evidence directory really is uncommitted; and STATUS.md, README.md, the queue file and the feature file all ABSENT from the range.

THE BUNDLE WAS READ OFF DISK, NOT OFF THE HANDBACK. All eight closed-schema gate documents are present in the evidence directory — `final_verifier_report`, `fresh_evidence`, `artifact_contract`, `change_provenance`, `manifest_integrity`, `postmortem_integrity`, `commit_execution` and `runtime_integration`. All four verification runs satisfy `len(node_ids) == selected` at 18, 18, 295 and 42 with zero failed and zero skipped, every `test_files` list SORTED — the unsorted-list trap that packaged BLOCKED_EVIDENCE at F082 — and every `output_hash` equal to sha256 of its `stdout_summary` exactly, which is the preimage rule that blocked the F083 closure. The adapted evidence script differs from the committed `EVIDENCESCRIPT` template in ONLY the values the block named: `EVIDENCE_DIR`, `BASE`, the four `mkrun` rows and the seven producer keyword arguments. Nothing load-bearing was touched.

THE PACKAGE WAS VERIFIED BY THE REVIEWER'S OWN HASH OVER THE ARCHIVED FILE. `remedy-review-20260829-025133-READY_FOR_REVIEW.zip` at `/home/decodeux/Repos/remedy-history/zips`, 18146705 bytes, sha256 `c2cf586f…a078fc` recomputed independently and identical to the reported value; 3349 members; `package_status` `READY_FOR_REVIEW`; `ready_gate_matrix.ok` True with `blocking_reasons` `[]`; `committed_review_subject.head_commit` `506bbab5d719974f69593087f8d4fa31f45edfb1`, EQUAL to C2's full sha; `base_commit` `f17b1d0d03e4042df8452b2019b719cbe4704b21`, the merge base with `main`. The worker's two deviations were both correct and both verified: the zip is written straight into the archive directory by the script, so no move was needed, and `blocking_reasons` genuinely has no top-level key — it lives under `ready_gate_matrix` and was reported from where it actually lives.

THE RED CONTROL IS THE READING THAT MAKES THE GREEN ONE MEAN ANYTHING. The tampered copy built `remedy-review-20260829-025231-BLOCKED_EVIDENCE.zip`, and the reviewer opened it: `package_status` `BLOCKED_EVIDENCE`, `ready_gate_matrix.ok` False, and three specific blocking reasons — the injected node id carrying a local absolute path, the resulting `node_ids` count of 19 against `selected` 18, and the unconfirmable VerificationTests total. Both builds exited 0. The exit code did not distinguish them; the status did, which is exactly why this block forbade reading the zip by its exit code.

PRECONDITIONS 2 AND 3 RE-CONFIRMED. `run_integrity_checks()` answers `passed=True`, `fail_count=0`. The full-suite proof still covers this tip and the reviewer measured why rather than assuming it: `git diff --name-only 2bb2db2c..HEAD` — from the integration-gate tip to here — lists TEN paths, of which ZERO lie under `packages/`, `apps/`, `tests/` or `scripts/`, so nothing the round 6 gate ran over has moved.

THE PACKAGE IS NEVERTHELESS SUPERSEDED, AND THIS IS NOT A FAULT OF THE ROUND. Round 10's repair of R-0737 lands a commit under `tests/`, which moves the head being closed away from `506bbab5`. A package records the head it covers, so a new one is built at the repaired head before the closure commit. Round 9 is accepted as executed correctly; its artifact is simply about to be out of date.
<<<END GATEF257R9

<<<SLICE FINDF257R10
- R-0737 — Medium, THREE TESTS ON F257'S OWN SURFACE GO RED THE MOMENT F257 CLOSES, BECAUSE THEY READ THE SHIPPED QUEUE'S PENDING STATE INSTEAD OF ITS CONTENTS. THE MEASUREMENT, taken by the reviewer at `5cb48adc` by applying the closure commit's own edits in a throwaway worktree and running the suite there: with SU-001's `consumed_by` set to `F257`, `python3 -m pytest tests/orchestration/test_self_use_queue.py tests/orchestration/test_self_use_job.py -q` reports `3 failed, 33 passed`, against `36 passed` in the pending state at the same commit. The three are `TestPlanSelfUseItem::test_the_shipped_item_plans_with_its_title_and_tasks`, `TestPlanSelfUseItem::test_the_shipped_item_plans_to_exactly_one_task_with_acceptance` and `TestPlanNextSelfUseItem::test_it_returns_the_shipped_pending_item`. The first two call `next_self_use_item()` and plan whatever it answers; the third calls `plan_next_self_use_item` against the shipped queue. All three therefore require the shipped queue to hold a PENDING item, and closure precondition 6 removes exactly that by setting `consumed_by` on the first pending item — which, for a one-item queue, exhausts it. WHY THIS IS THE FEATURE'S OWN DEFECT RATHER THAN THE PROTOCOL'S: F257 wrote both the precondition and these tests, and the two contradict each other, so the feature cannot satisfy its own closure rule without turning its own suite red. WHY MEDIUM AND NOT HIGH: no shipped behaviour is wrong — `plan_self_use_item` plans a consumed entry perfectly well, `plan_next_self_use_item` raises on exhaustion exactly as designed, and that exhaustion path already has its own state-independent test in `test_exhausted_queue_raises_rather_than_answering_none`. What is wrong is that three gates are coupled to a state the product is designed to leave behind. THE FIX is to make all three read the shipped queue's CONTENTS rather than its pending-ness: the first two take the first entry of `load_self_use_queue()`, which `consumed_by` does not affect, and the third asserts the invariant in BOTH directions — a pending item is planned, an exhausted queue raises. Resolved when that suite is green at one commit in BOTH ledger states, measured with the queue pending and again with it exhausted.
<<<END FINDF257R10

`PLANF257R10` is a WHOLE-FILE replacement of `.agent/plan.md`. `GATEF257R9` and
`FINDF257R10` are TWO SEPARATE APPENDS to `.agent/live_review.md`, in that order,
each under constraint 6 — `GATEF257R9` first. This round registers R-0737 and
resolves nothing.

### C3 — the repair, DESCRIBED rather than pasted

This is production code, so the block specifies the CHANGE and you write it. Read
`tests/orchestration/test_self_use_job.py` in full first. Change only what is
listed; keep every existing assertion; delete no test; skip no test; weaken no
assertion; add no `xfail`.

1. Add `load_self_use_queue` to the existing import block from
   `packages.orchestration.self_use_queue`, keeping that block alphabetically
   ordered as it already is. `load_self_use_queue(path=None)` answers a
   `tuple[SelfUseQueueEntry, ...]` and is unaffected by `consumed_by`.
2. In `TestPlanSelfUseItem.test_the_shipped_item_plans_with_its_title_and_tasks`
   and `TestPlanSelfUseItem.test_the_shipped_item_plans_to_exactly_one_task_with_acceptance`,
   replace the `next_self_use_item()` call that obtains `entry` with the FIRST
   entry of `load_self_use_queue()` — the shipped queue's first item in file
   order, which is the curated order. In the first test, the existing
   `assert entry is not None, "the shipped queue has no pending item"` becomes an
   assertion that the shipped queue is NOT EMPTY, with a message saying so; the
   remaining assertions in both tests stay exactly as they are.
3. Rewrite `TestPlanNextSelfUseItem.test_it_returns_the_shipped_pending_item` so
   it holds in BOTH ledger states, and rename it to say so — a name containing
   `pending` alone will read false once the queue is exhausted. It reads
   `next_self_use_item()` once. If that answers `None`, the whole-track call
   `plan_next_self_use_item` must RAISE `SelfUseJobError` and the test asserts
   that and returns. Otherwise it keeps the four assertions it has today: the
   planned entry's id equals the pending id, the entry is pending, the file is
   named `<id>.md`, and `plan.error` is empty.
4. Above the two changed classes, put a one-line WHY comment in the repo's idiom,
   naming R-0737 and saying that these tests read the shipped queue's CONTENTS
   because closure precondition 6 is designed to exhaust its PENDING state. That
   comment is what stops the next reader re-coupling them.
5. Update the module docstring's list of load-bearing tests if and only if it
   names a test you renamed; leave it otherwise untouched.

### Done when

G1 HYGIENE. Read `.agent/STOP` from disk with `os.path.exists` before C0a and
again before C3; report both answers. If it exists at either reading, finish the
commit in hand, write the handback and stop. Report constraint 0's three readings
and `git status --porcelain | wc -l` after each of C0a, C0b, C1, C2 and C3.

G2 TRANSPORT. One digest comparison. Report sha256 and the byte length of the
committed blob `git show <C0a>:.agent/authored/f257-r10.md` and of the reviewer's
own original at `.remedy-wt/f257-r10-block.md`, and whether they are EQUAL. That
original was written before this worker existed, so the reading covers more than
self-consistency; it covers no emission, because this workflow has none — say
both in the handback. Then report that
`git rev-parse <C0b>:.agent/authored/f257-r10.md` and
`git rev-parse <C0b>:.agent/last_block.md` print ONE blob id.

G3 THE PLAN AT C1. `.agent/plan.md` at C1 equals PLANF257R10 including the
trailing newline — report `True` or `False`, with the byte length of each side.
Report `wc -l`, under 50, and the count of lines exactly `## Goal` and exactly
`## Next Steps`.

G4 THE RECORD APPENDS AT C2. Reconstruct the C2 blob of `.agent/live_review.md`
from the `5cb48adc` blob plus GATEF257R9 plus FINDF257R10, applied IN THAT ORDER
each under constraint 6, and report `True` or `False` with all lengths. NEGATIVE
CONTROL: flip one byte at an offset your script CONFIRMS lies inside the FIRST
appended paragraph, recompute, and report the equality is now `False`. Report that
the pre-round blob is a byte PREFIX, with both lengths, and that the C2 blob ends
in exactly ONE newline.

G5 THE LEDGER AT C2, counted under constraint 7. Report over
`.agent/live_review.md` at `5cb48adc` and again at C2: the count of lines matching
`^- R-\d+ — ` and whether all are DISTINCT; the count of `^Done: R-\d+ — ` lines
AND the count of DISTINCT ids among them, as two separate numbers; the count of
`^Landed: R-`; the count of `^Gate: F\d+ R\d+ — `; and the OPEN SET as
`len(set(registered) - set(resolved))`. Expected: registered 297 → 298 all
distinct, the `Done:` numbers and `Landed:` UNMOVED, `Gate:` 114 → 115, and the
open set 255 → 256. Report the count of `^Gate: F257 R9 — ` at C2, which must be
1, and of `^- R-0737 — `, which must be 1.

G6 THE REPAIR PROVED IN BOTH LEDGER STATES — the red-proof, and the reason this
round exists. Under constraint 8, in a `git worktree add --detach` worktree under
`.remedy-wt/`, run `python3 -B -m pytest tests/orchestration/test_self_use_queue.py
tests/orchestration/test_self_use_job.py -q` FOUR times and report all four with
their REAL exit codes and full counts:
  (A) at `5cb48adc`, queue PENDING (untouched) — expected all passed;
  (B) at `5cb48adc`, queue EXHAUSTED (SU-001's `consumed_by` set to `F257` in the
      WORKTREE ONLY) — expected exactly 3 failed, and report the three failing
      node ids IN FULL and untruncated. THIS IS THE NEGATIVE CONTROL: it is the
      defect reproduced, and a gate that cannot show the red proves nothing;
  (C) at C3, queue PENDING — expected all passed;
  (D) at C3, queue EXHAUSTED — expected all passed, and the three ids from (B)
      among the passing ones.
Report that the ONLY difference between (B) and (D) is the commit, and that the
queue edit was made in the worktree and never in the primary checkout — show
`git status --porcelain` EMPTY in the primary checkout at the same moment. Then
remove the worktree BY ITS EXACT PATH and report `git worktree list`.

G7 THE SUITES AT C3, in the PRIMARY checkout, one pytest process at a time, each
with its REAL exit code and its own passed/failed line. CONFIRM FIRST that every
path resolves on disk and report the empty list:
`tests/orchestration/test_self_use_job.py` — expected 18 passed;
`tests/orchestration/test_self_use_queue.py` — expected 18;
`tests/docs/test_docs_consistency.py` — expected 295; and the canary
`tests/cli/test_golden_path.py` — expected 42. Every one must be exit 0. If any is
red, STOP and write the handback with the full untruncated failure list.

G8 STRUCTURE, over `5cb48adc..<C3>` — the range that ends BEFORE the handback
commit. The change set lists `.agent/handoff.md`, which C4 writes, so compute the
changeset-minus-range residue over the change set WITHOUT that ONE path and name
the path you excluded; the range-minus-changeset residue is computed against the
FULL change set and must be empty. Report each commit's insertions from
`git diff --numstat`, each under 500, and that each of C0a, C0b, C1, C2 and C3 is
single-parent. Report the number of lines beginning `<<<SLICE ` and `<<<END ` in
`.agent/plan.md`, `.agent/live_review.md` and
`tests/orchestration/test_self_use_job.py` at C3 — each expected 0 — beside the
same counts over `.agent/authored/f257-r10.md` as the non-zero control. Report
`git ls-files .remedy-wt | wc -l`, expected 0. Report the `git diff --numstat`
line over the range for `scripts/self_use_queue.json`, `docs/roadmap/STATUS.md`,
`README.md` and `packages/orchestration/self_use_job.py`, all four expected
ABSENT — in particular the queue file, whose edit belongs to the closure commit.
Finally report `python3 -m ruff check tests/orchestration/test_self_use_job.py`
with its REAL exit code, or, if ruff is unavailable, `python3 -m py_compile` on
the same file with its real exit code; say which one you ran.

### Handback

Rewrite `.agent/handoff.md` in C4 per docs/agents/handback_template.md. It
carries: `SESSION 3 of feature F257 · round 10`; the roster of this session's
rounds, this round included; the range `5cb48adc..HEAD`; a per-commit
changed-files table whose `+/-` cells are taken from `git diff --numstat`; ONE
LINE PER GATE G1 through G8 with its real result; the deviations, including every
guard re-expression constraint 5 required; the item-status table with every
C-item and every gate appearing exactly once; the open-findings count, which must
be 256; and the next expected action — rebuild the evidence bundle and the review
zip at the repaired head, then the closure commit and the PR.

Quote in the handback the FULL final text of each of the three repaired tests, so
the reviewer can read what landed without reconstructing it from a diff, and state
plainly that no assertion was removed.

Do not write a `Done:` or `Gate:` paragraph of your own anywhere — GATEF257R9 and
FINDF257R10 are reviewer-authored text you apply verbatim, and any OTHER such
paragraph is a finding however hedged. Do not flip any checkbox to `[x]`. Do not
edit `scripts/self_use_queue.json` in the primary checkout. Do not create a pull
request and do not merge anything.

After C4: push with `git push origin feature/f257-self-use-track` and report the
outcome.
