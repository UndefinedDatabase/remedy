### STEP T002 — F257 Self-use track, round 7 (THE BUILT STATE)

Goal: book the round 6 verdict — the integration gate PASSED — register the
finding that gate round exposed, and bring `docs/roadmap/features/T5_F257.md`
current. That file still carries a REGISTRATION-ONLY banner saying "Nothing in
this file has been implemented", which is false at this tip, and it has no Built
State section at all. Closure precondition 4 requires one, so this round is the
last thing standing between F257 and its closure sequence.

Base: `2bb2db2c`, the tip of `feature/f257-self-use-track` and the handback this
round starts from.

Bundle, in commit order:

- C0a save this block verbatim to `.agent/authored/f257-r7.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 advance `.agent/plan.md`
- C2 book the F257 R6 verdict AND register R-0736 into `.agent/live_review.md`
- C3 bring `docs/roadmap/features/T5_F257.md` current
- C4 rewrite `.agent/handoff.md`

Change set — these paths and nothing else:

- `.agent/authored/f257-r7.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `docs/roadmap/features/T5_F257.md`
- `.agent/handoff.md`

NO file under `packages/`, `apps/`, `tests/` or `scripts/` is edited. In
particular `docs/agents/integration_gate.md` is NOT edited: R-0736 is REGISTERED
here and repaired on a branch of its own, for the same scope reason R-0734 was
left alone — the procedure doc is not F257's surface. `scripts/self_use_queue.json`
is NOT edited: the consumption edit belongs to the closure commit, which is a
later round.

### Constraints

0. BEFORE ANYTHING: report `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
   — it was `[]` when this block was written, and if it is not `[]` now, STOP and
   hand back without committing. Report `git rev-parse HEAD`, which must equal
   `2bb2db2c`'s full sha, and `git branch --show-current`, which must be
   `feature/f257-self-use-track`. Create no branch and no pull request. Never
   force-push and never rewrite history.
1. Apply every authored slice BYTE FOR BYTE — no reflow, rewording, retitling,
   correction or shortening. If a slice looks wrong, apply it as written and say
   so in the handback's deviations; the record is repaired by a later append.
2. The delimiter lines `<<<SLICE …` and `<<<END …` are transport only and never
   reach a target file.
3. Extract every slice from the COMMITTED blob with
   `git show <C0a>:.agent/authored/f257-r7.md`, never from this prompt's text.
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
   `len(set(registered ids) - set(resolved ids))`. It reads 254 at `2bb2db2c`.
   This round registers ONE id and resolves none, so it must read 255 at C2.
8. A PAIR IS APPLIED BY EXACT MATCH. The FROM block below occurs EXACTLY ONCE in
   `docs/roadmap/features/T5_F257.md` at `2bb2db2c` — verify that count is 1
   before replacing, and if it is not 1, STOP and hand back. Replace the FROM
   bytes with the TO bytes and change nothing else by that replacement.

### The authored slices

<<<SLICE PLANF257R7
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
| the feature file's Built State | done | this round, precondition 4 |
| the closure sequence | open | next, and it must satisfy precondition 6 |

## Next Steps
1. Satisfy closure precondition 6 for F257 itself: plan the pending self-use item
   through `packages.orchestration.self_use_job` and take it to the approval gate.
   F257 is the FIRST feature that must consume an item at its own close.
2. Build the evidence bundle and the review zip from a clean tree.
3. The closure commit — STATUS, README, `scripts/self_use_queue.json`
   `consumed_by`, and the final `.agent/` state — then the PR.

## Risks
- A job must never mark its own queue item consumed; neither shipped module owns
  a queue writer, and DECISION F257 D2 rules the consumption point.
- `docs/roadmap/STATUS.md` is in `scope_fences.BUILTIN_DENY` and stays there.
- R-0734 and R-0736 are registered and deliberately NOT repaired on this branch;
  both are outside F257's surface.
<<<END PLANF257R7

<<<SLICE GATEF257R6
Gate: F257 R6 — the INTEGRATION-GATE round. THE ROUND PASSED, AND THE INTEGRATION GATE PASSES. The gate verdict is the reviewer's alone under `docs/agents/integration_gate.md` step 5, and it is issued here on evidence the reviewer produced independently, not on the worker's report.

THE BRANCH IS CLEAN ON A FULL RUN, MEASURED TWICE BY TWO ACTORS. The worker's branch run of `python3 -m pytest -n auto -q` at the repository root reported REAL exit 0, `18186 passed, 20 skipped in 112.58s`, with a COMPLETE FAILED list of ZERO ids and the committed `branch_failed.txt` empty at 0 bytes. The reviewer then ran the identical command itself at the same tip and measured REAL exit 0, `18186 passed, 20 skipped in 116.03s` — the same 18186, the same 20, the same zero failures. BRANCH-ONLY FAILURES: NONE, against either base run, so step 4's attribution obligation is discharged with nothing to attribute and no blocker can arise.

THE BASE COMPARISON IS FULLY ATTRIBUTED, WHICH IS THE HARD HALF. Base run 1 at `f17b1d0d` gave 116 base-only ids and base run 2 gave 1; every one is accounted for. 114 belong to a stale-dist ENVIRONMENT class the worker proved rather than asserted: `ui_server.py` is byte-identical at both revisions, `apps/ui` is untouched by the branch, the marker `ERROR: React UI not built.` appears exactly 114 times in the base log and 0 times in the branch log — 1:1 with the ids and none left over — and the decisive control is that completing parity in the SAME worktree at the SAME revision turned all 114 green. The remaining 3 are xdist and port flakes, each serial re-run at the merge base by exact node id and each serial-pass at exit 0. Parity was verified by measuring the EVENT and not the outcome, as R-0444 requires: 4 dist files, mtimes recorded before and after each run against that run's own window, ZERO mtimes inside either window, no content hash offered in place of the reading.

THE STRUCTURAL GATES ALL REPRODUCED. Transport EQUAL at sha256 `0a436adf…c20bc5` over 22016 bytes with one blob id at C0b; the plan byte-equal at 1764 bytes and 37 lines; the record append reconstructing 1393448 → 1396957 with the negative control failing as it must and the two prose-slip lines landing exactly; the ledger UNMOVED at 296 registered and 254 open with `Gate:` 110 → 111; both residues empty; the range holding 12 paths of which ZERO lie under `packages/`, `apps/`, `tests/`, `scripts/` or `docs/`; no evidence file named `\.log$`; the base worktree and its throwaway branch both gone. The evidence is real content and not placeholders — `branch_run.txt` at 20994 bytes, `comparison.txt` at 34436 bytes, `parity.txt` at 4320 bytes, the 116-id list untruncated.

THE ONE OVERSIZE COMMIT IS THE PERMITTED ONE. C3 carries 1328 insertions, declared before review with the inseparability reason AGENTS.md asks for — a gate's evidence is one artifact and a comparison is meaningless apart from the lists it diffs. The reviewer counted every commit on this branch since the merge base: 37 commits, EXACTLY ONE over 500 insertions, and this is it. The exception is spent correctly and is now spent for F257.

THE WORKER FOUND A DEFECT IN THE PROCEDURE ITSELF AND HANDLED IT EXACTLY RIGHT. It did not repair the 114 failures, did not shorten a run, did not subset a suite, and did not issue the verdict; it completed parity in the throwaway worktree only, re-ran the whole suite unmodified, and declared the recipe gap. That gap is registered below as R-0736.
<<<END GATEF257R6

<<<SLICE FINDF257R7
- R-0736 — Medium, THE INTEGRATION GATE'S OWN PARITY RECIPE MANUFACTURES 114 FALSE BASE FAILURES ON EVERY RUN THAT FOLLOWS IT LITERALLY. THE MEASUREMENT, taken at F257 R6 and confirmed independently by the reviewer at `2bb2db2c`: `docs/agents/integration_gate.md` step 3 says to restore build parity by COPYING the primary checkout's `apps/ui/node_modules` and `apps/ui/dist` into the throwaway base worktree. `shutil.copytree` PRESERVES the source mtimes, while `git worktree add` stamps every checked-out source file with the CHECKOUT time. `packages/orchestration/ui_server.py::_frontend_is_stale` returns True when ANY file under `apps/ui/src/` is newer than `apps/ui/dist/index.html` — the reviewer read the function at this tip to confirm the comparison. So the copied dist is byte-correct and mtime-stale, staleness fires, `REMEDY_UI_NO_AUTO_BUILD=1` correctly suppresses the rebuild, the UI is never built, and 114 `tests/ui_server/` ids fail with `ERROR: React UI not built.` — a marker that appeared exactly 114 times in the base log and 0 times in the branch log. THE PROOF IT IS THE RECIPE AND NOT THE REVISION: completing parity in the SAME worktree at the SAME revision and re-running the full suite unmodified turned all 114 green, 18149 passed. WHY MEDIUM: nothing in the product is wrong and no verdict was corrupted here, because the worker attributed all 116 ids and the gate still passed — but step 3 says an UNATTRIBUTED base-only id BLOCKS the gate verdict, so the recipe as written puts 114 ids in the blocking bucket on every future gate run and costs a round to clear each time. It also masks a GENUINE base failure in those same files, which is the failure mode step 3 exists to prevent. THE FIX is one clause in step 3: after copying `apps/ui/dist`, set its mtimes NEWER than the newest file under `apps/ui/src` — the copy restores CONTENT parity but not the mtime relation `_frontend_is_stale` actually reads, and only the second makes the neutralisation real. NOT REPAIRED ON THIS BRANCH: `docs/agents/integration_gate.md` is not F257's surface and AGENTS.md forbids mixing an unrelated fix into a feature branch. Resolved when step 3 carries that clause and one gate run afterwards reports zero stale-dist base failures.
<<<END FINDF257R7

`PLANF257R7` is a WHOLE-FILE replacement of `.agent/plan.md`. `GATEF257R6` and
`FINDF257R7` are TWO SEPARATE APPENDS to `.agent/live_review.md`, in that order,
each under constraint 6 — `GATEF257R6` first. This round registers R-0736 and
resolves nothing.

### The authored pair for C3 — the stale banner

FROM (occurs exactly once in `docs/roadmap/features/T5_F257.md`):

<<<SLICE BANNERFROM
> Registered 2026-08-28 by operator order amend0828-daily-driver, point 5.
> REGISTRATION ONLY — the order says to register it with a feature file and NOT
> to build it. Nothing in this file has been implemented.
<<<END BANNERFROM

TO:

<<<SLICE BANNERTO
> Registered 2026-08-28 by operator order amend0828-daily-driver, point 5, which
> said to register the feature and NOT to build it. That hold was lifted when
> F257 was claimed under Rule A5; the feature is BUILT, and what exists on disk
> is recorded in the Built State section at the foot of this file.
<<<END BANNERTO

### The authored append for C3 — the Built State

`BUILTSTATE` is APPENDED to the END of `docs/roadmap/features/T5_F257.md` under
constraint 6, after the `## Orchestrator brief` section, which is where
`docs/roadmap/features/T5_F256.md` puts the same section.

<<<SLICE BUILTSTATE
## Built State (F257, 2026-08-29)

What exists on disk at the close of F257, so a later reader need not reconstruct
it from this file's future tense. Written before the closure sequence, as
closure precondition 4 requires.

**The queue.** `scripts/self_use_queue.json` is the shipped, operator-curated
queue: a `schema_version`-stamped object whose `items` each carry exactly five
keys — `id`, `title`, `why`, `job_markdown`, `consumed_by`. It lives beside the
other shipped campaign data rather than under `docs/`, because a data file that
code reads is not a doc. DECISION F257 D2 rules the format and the consumption
point.

**The read side.** `packages/orchestration/self_use_queue.py` loads and validates
it and owns NO writer at all: its public callables are `SelfUseQueueEntry`,
`SelfUseQueueError`, `default_self_use_queue_path`, `load_self_use_queue`,
`next_self_use_item` and `pending_self_use_items`. Every failure raises rather
than degrading to an empty queue, because "the queue is empty" and "I could not
read the queue" are opposite answers; only `next_self_use_item` answers `None`,
and only for exhaustion. Ids must match `^SU-\d{3}$` and be unique. Tests:
`tests/orchestration/test_self_use_queue.py`, 18 of them.

**The job-path seam.** `packages/orchestration/self_use_job.py` renders one item
to `<dest_dir>/<id>.md` and plans it through the parser Remedy already has,
`packages.orchestration.pingpong_job.plan_job_from_file`. The rendered bytes are
the curated bytes — no templating, no substitution — so the text a reviewer read
is the text that runs. It plans only: it never runs a job, never promotes one,
and never marks an item consumed. Two guards protect the destination, and each
answers a different question: `Path(id).name != id` (plus `.` and `..` named
outright) asks "is this id one file name?", and a resolved-parent comparison
asks "does that file land inside the caller's directory?". They repair findings
`R-0733` and `R-0735`, both raised by the reviewer RUNNING the shipped function
rather than reading it. Tests: `tests/orchestration/test_self_use_job.py`, 18 of
them.

**The consumption point — the part that makes the track a track.**
`docs/roadmap/STATUS_closure_protocol.md` gained precondition 6: exactly one
self-use item is consumed by each feature close, and the closure commit's path
set gained `scripts/self_use_queue.json` for that one `consumed_by` edit. An
EXHAUSTED queue never blocks a feature — the close records
`self-use NONE (queue exhausted)` and proceeds. This is what turns "Remedy is
used on Remedy" from an intention into a step that cannot be skipped, which is
this file's Goal & Done clause in as many words.

**Where a reader looks.** `docs/system/self-use-track-v1.md` documents both
formats and the consumption rule, registered in `docs/README.md` twice — the
quick-find row and the system table.

**Acceptance, item by item.** (1) The queue file exists with a curated item and
its format is documented where a reader would look — DONE. (2) One feature close
consumes exactly one item and leaves the queue shorter — the MECHANISM is in
place as precondition 6; F257's own close is the first to exercise it. (3) The
run reaches the normal approval gate and nothing is promoted without it — the
shipped module plans only, and promotion stays behind the `--approve` barrier in
`packages/orchestration/job_promote.py`, which never auto-promotes. (4) A defect
the run exposes lands as an operator finding in the owning feature file — the
route is open and unexercised; the defects this feature's own rounds exposed were
registered in `.agent/live_review.md` as `R-0733`, `R-0734`, `R-0735` and
`R-0736`, of which `R-0734` and `R-0736` are deliberately left for branches of
their own.

**The integration gate.** Full suite at `2bb2db2c`: `18186 passed, 20 skipped`,
exit 0, ZERO failures, measured independently by worker and reviewer. Zero
branch-only failures against the merge base `f17b1d0d`. Evidence:
`.agent/gate_f257_r6/`.
<<<END BUILTSTATE

### Done when

G1 HYGIENE. Read `.agent/STOP` from disk with `os.path.exists` before C0a and
again before C3; report both answers. If it exists at either reading, finish the
commit in hand, write the handback and stop. Report constraint 0's three
readings and `git status --porcelain | wc -l` after each of C0a, C0b, C1, C2
and C3.

G2 TRANSPORT. One digest comparison. Report sha256 and the byte length of the
committed blob `git show <C0a>:.agent/authored/f257-r7.md` and of the reviewer's
own original at `.remedy-wt/f257-r7-block.md`, and whether they are EQUAL. That
original was written before this worker existed, so the reading covers more than
self-consistency; it covers no emission, because this workflow has none — say
both in the handback. Then report that
`git rev-parse <C0b>:.agent/authored/f257-r7.md` and
`git rev-parse <C0b>:.agent/last_block.md` print ONE blob id.

G3 THE PLAN AT C1. `.agent/plan.md` at C1 equals PLANF257R7 including the
trailing newline — report `True` or `False`, with the byte length of each side.
Report `wc -l`, under 50, and the count of lines exactly `## Goal` and exactly
`## Next Steps`.

G4 THE RECORD APPENDS AT C2. Reconstruct the C2 blob of `.agent/live_review.md`
from the `2bb2db2c` blob plus GATEF257R6 plus FINDF257R7, applied IN THAT ORDER
each under constraint 6, and report `True` or `False` with all three lengths.
NEGATIVE CONTROL: flip one byte at an offset your script confirms lies INSIDE
the FIRST appended paragraph, recompute, and report the equality is now `False`.
Report that the pre-round blob is a byte PREFIX, with both lengths, and that the
C2 blob ends in exactly ONE newline.

G5 THE LEDGER AT C2, counted under constraint 7. Report over
`.agent/live_review.md` at `2bb2db2c` and again at C2: the count of lines
matching `^- R-\d+ — ` and whether all are DISTINCT; the count of
`^Done: R-\d+ — ` lines AND the count of DISTINCT ids among them, as two
separate numbers; the count of `^Landed: R-`; the count of
`^Gate: F\d+ R\d+ — `; and the OPEN SET as
`len(set(registered) - set(resolved))`. Expected: registered 296 → 297, the
`Done:` numbers and `Landed:` UNMOVED, `Gate:` 111 → 112, and the open set
254 → 255. Report the count of `^Gate: F257 R6 — ` at C2, which must be 1, and
the count of `^- R-0736 — `, which must be 1.

G6 THE FEATURE FILE AT C3, over `docs/roadmap/features/T5_F257.md`. Report:
(a) the count of BANNERFROM in the `2bb2db2c` blob, which must be 1, and the
count in the C3 blob, which must be 0; (b) the count of BANNERTO in the C3 blob,
which must be 1; (c) that the C3 blob equals the `2bb2db2c` blob with BANNERFROM
replaced by BANNERTO and then BUILTSTATE appended under constraint 6 — report
`True` or `False` and all three byte lengths; (d) the count of lines exactly
`## Built State (F257, 2026-08-29)`, which must be 1, and that it is the LAST
heading in the file; (e) that the file ends in exactly ONE newline; (f) that the
string `Nothing in this file has been implemented` appears ZERO times in the C3
blob; (g) that every relative markdown link in the C3 blob resolves — extract
each `[text](target)`, drop `http://`, `https://` and `mailto:` targets, and
report each remaining target with whether it exists relative to
`docs/roadmap/features/`; report the empty list if the file carries none.

G7 THE SUITES AT C3. One pytest process at a time, from the repository root, in
the PRIMARY checkout, each with its REAL exit code and its own passed/failed
line. CONFIRM FIRST that every path below resolves on disk and report the empty
list, because `pytest <missing path>` exits 4 and says almost nothing:
`tests/docs/test_docs_consistency.py` — the one that counts and cross-checks the
feature files and is the gate this round's edit could plausibly break;
`tests/orchestration/test_self_use_job.py`;
`tests/orchestration/test_self_use_queue.py`; and the canary
`tests/cli/test_golden_path.py`. Every one must be exit 0. If any is red, STOP
and write the handback with the full untruncated failure list.

G8 STRUCTURE, over `2bb2db2c..<C3>` — the range that ends BEFORE the handback
commit, because C4's own numbers cannot exist while C4 is being written. The
change set lists `.agent/handoff.md`, which C4 writes, so compute the
changeset-minus-range residue over the change set WITHOUT that path and name the
path you excluded; the range-minus-changeset residue is computed against the
full change set and must be empty. Report each commit's insertions from
`git diff --numstat`, each under 500, and that each of C0a, C0b, C1, C2 and C3
is single-parent. Report, counted affirmatively over each file's C3 content, the
number of lines beginning `<<<SLICE ` and `<<<END ` in `.agent/plan.md`,
`.agent/live_review.md` and `docs/roadmap/features/T5_F257.md` — each expected 0
— beside the same counts over `.agent/authored/f257-r7.md` as the non-zero
control. Report `git ls-files .remedy-wt | wc -l`, expected 0. Report the
`git diff --numstat` line for `docs/agents/integration_gate.md`,
`scripts/self_use_queue.json`, `packages/orchestration/self_use_job.py` and
`tests/ui_server/test_command_channel.py` over the range, all four expected
ABSENT.

### Handback

Rewrite `.agent/handoff.md` in C4 per docs/agents/handback_template.md. It
carries: `SESSION 2 of feature F257 · round 7`; the range `2bb2db2c..HEAD`; a
per-commit changed-files table whose `+/-` cells are taken from
`git diff --numstat`; ONE LINE PER GATE G1 through G8 with its real result; the
deviations, including every guard re-expression constraint 5 required; the
item-status table with every C-item and every gate appearing exactly once; the
open-findings count, which must be 255; and the next expected action, which is
the closure sequence — and NAME its first step: satisfying closure precondition 6
for F257 itself, the first feature ever required to consume a self-use item at
its own close.

Do not write a `Done:` or `Gate:` paragraph of your own anywhere — GATEF257R6
and FINDF257R7 are reviewer-authored text you apply verbatim, and any OTHER such
paragraph is a finding however hedged.

After C4: push with `git push origin feature/f257-self-use-track` and report the
outcome. Do NOT create a pull request and do NOT merge anything.
