── STEP T002 (part 3) — F260 ─────────────────────────────────
Goal:        Give the PING-PONG store one spelling in `data_paths` and DELETE
             `pingpong_job._jobs_dir`, so finding R-0814's "no module-local
             `_jobs_dir`" clause is discharged and T002's actual record move
             becomes a change to two function bodies instead of forty call sites.
Bundle:      C0a save this block · C0b mirror it · C1 the record (the R7 gate
             entry) · C2 two reviewer slips · C3 the plan · C4 the two new
             accessors, the six production sites, the seventeen test sites and
             the widened guard · C5 the handback
(§3 item 37: the STEP line above is 62 characters ending in a run of U+2500,
 and the rule line below is 62 copies of U+2500 and nothing else)
──────────────────────────────────────────────────────────────

## Where this round starts

Continuing on `feature/f260-one-world` at `072b54ed`, already pushed. Do NOT
create a branch, do NOT merge, do NOT open a pull request.

Round 7 PASSED. The reviewer re-ran all eight gates itself, reproduced the ledger
and slip arithmetic — including the unit count rising 128 to 129, the reading the
round-6 recipe would have failed — re-ran the three mutations in its own
worktree and re-ran all eight suites. BOTH block defects you declared are UPHELD
and are recorded in C2: the change set really is NINE paths and the block said
eight, and "the last blank-line unit equals the slice" really is False unless the
file's terminating newline is stripped first. Your rename of the guard test is
also upheld: a name claiming single-module scope over a parametrized set is the
same defect as a heading that miscounts its body.

## Change set — nothing outside this list

    .agent/authored/f260-r8.md                                (new, C0a)
    .agent/last_block.md                                      (C0b)
    .agent/live_review.md                                     (C1)
    .agent/prose_slips.md                                     (C2)
    .agent/plan.md                                            (C3)
    packages/orchestration/data_paths.py                      (C4)
    packages/orchestration/pingpong_job.py                    (C4)
    packages/orchestration/job_evidence.py                    (C4)
    tests/test_data_paths.py                                  (C4)
    tests/orchestration/test_failure_wiring.py                (C4)
    tests/orchestration/test_job_promote_consistency.py       (C4)
    tests/orchestration/test_job_stop_integration.py          (C4)
    tests/orchestration/test_job_worktree_handoff.py          (C4)
    tests/orchestration/test_job_worktree_integration.py      (C4)
    tests/orchestration/test_job_worktree_integrity.py        (C4)
    tests/orchestration/test_pingpong_integration.py          (C4)
    .agent/handoff.md                                         (C5)

That is SEVENTEEN paths; C5 adds the last of them. `.remedy-wt/` scratch stays
untracked; `git ls-files .remedy-wt` returns nothing.

## C0a / C0b — save and mirror

The block is at `.remedy-wt/f260-r8-block.md`; the delegating prompt states its
sha256 (BLOCK_SHA — a file cannot carry its own digest). COPY it to
`.agent/authored/f260-r8.md` with `shutil.copyfile`, commit alone; copy the same
bytes to `.agent/last_block.md`, commit alone. Do not retype either.

## C1 — the record

APPEND to `.agent/live_review.md`, in one commit of its own, exactly the bytes
`"\n"` + the GATE_R7 slice + `"\n"`. A slice is the bytes between its markers
EXCLUDING the newline that ends its last content line. Measured at `072b54ed`:
893805 bytes, ends with exactly one newline, 425 blank-line units; afterwards one
newline and 426 units.

## C2 — the slips

APPEND to `.agent/prose_slips.md`, in one commit of its own, exactly the bytes
`"\n"` + SLIP7 + `"\n\n"` + SLIP8 + `"\n"`. Measured at `072b54ed`: 94802 bytes,
LAST BYTE is a newline, 129 blank-line units; afterwards 131. Report the terminal
byte you read before appending — round 6 is why.

NOTE THE DOUBLE NEWLINE BETWEEN THE TWO SLIPS, and that it is not a typo. The
round-6 defect was a missing separator BEFORE the first appended slip; the same
defect sits BETWEEN two slips appended together, and the single-newline recipe
that is correct for one slip fuses two. The reviewer's own first draft of this
block had it wrong and its unit-count check caught it before emission: with
single newlines throughout the count reaches 130, not 131.

## C3 — the plan

REPLACE `.agent/plan.md` entirely with the PLANF260R8 slice plus one trailing
newline. Commit alone.

## C4 — what to build

Rounds 6 and 7 gave `data_paths` the one spelling of DECISION F260 D1's TARGET
layout. The store that actually holds ping-pong records TODAY —
`<data_root>/task_jobs/<16hex>/` — is still spelled through a module-local helper
in `pingpong_job`, which is the shadowing finding R-0814 names. This round gives
that store one spelling too, so T002's real move becomes a change to two function
bodies in `data_paths` rather than a sweep of every caller.

ADD to `packages/orchestration/data_paths.py`, immediately after `task_jobs_dir`
and built on it, mirroring `job_dir` / `job_record_path` exactly:

    task_job_dir(job_id, root=None)          -> task_jobs_dir(root) / job_id
    task_job_record_path(job_id, root=None)  -> task_job_dir(...) / "job.json"

Extend the module docstring's `Public API::` block with both names. Say in the
group comment that these NAME THE STORE AS IT IS TODAY and that DECISION F260 D1
collapses them into `job_dir` / `job_record_path` in T002 — the pair exists so
that collapse is one edit.

THEN DELETE `pingpong_job._jobs_dir` ENTIRELY and point its six users at the new
accessors. What the reviewer read at `072b54ed`, so you are not reading it cold —
re-grep each before editing, because these numbers are pre-edit:

    pingpong_job.py:379  the `_jobs_dir` def itself                → DELETE
    pingpong_job.py:387  `_persist_job`, builds the job dir then `/ "job.json"`
                                                                   → task_job_record_path
    pingpong_job.py:400  `load_job_plan`, reads that same file      → task_job_record_path
    pingpong_job.py:976  `_jobs_dir().parent`, i.e. the DATA ROOT   → resolve_data_root()
    pingpong_job.py:1184 `_jobs_dir() / job.job_id`                 → task_job_dir
    pingpong_job.py:2696 `_fjr_dir = _jobs_dir() / job.job_id`      → task_job_dir
    pingpong_job.py:2877 inside a compound `and` expression         → task_job_dir

EVERY ONE OF THOSE SIX SITES NEEDS ITS OWN FUNCTION-SCOPED IMPORT. `pingpong_job`
imports `data_paths` only inside function bodies — that is the module's existing
style and this round does not change it — so a name imported in one function is
NOT available in another. The reviewer's own dry run got this wrong at exactly one
site and it is the one to watch: `pingpong_job.py:2877` sits inside a multi-line
boolean `and` expression, where the edit does not look like a statement and the
missing import produced

    NameError: name 'task_job_dir' is not defined

at runtime, caught only by two integration tests in
`tests/orchestration/test_job_worktree_handoff.py` and by nothing else. Add the
import to the ENCLOSING FUNCTION of that expression, and after editing, grep the
module for every use of each new name and confirm each has an import in scope.

ALSO in `packages/orchestration/job_evidence.py`: it imports `_jobs_dir` FROM
`pingpong_job` — a cross-module reach into another module's private helper, and
the last external dependency on the name being deleted. Point it at
`data_paths.task_job_dir` instead. That is a two-line change and it is why the
delete is possible at all.

THEN THE SEVENTEEN TEST SITES across seven files, all of one shape —
`_jobs_dir() / <id> / <tail>` or `PJ._jobs_dir() / <id> / <tail>`, plus two
`_jobs_dir().parent` data-root readings in `test_job_stop_integration.py`. They
become `task_job_dir(<id>) / <tail>` and `resolve_data_root()`. The files are the
seven `tests/orchestration/` paths in the change set above. Two of them import
`_jobs_dir` by name in a from-import list; those imports move to `data_paths`.
Place every added import where that file's existing imports live, in isort order
— see the ruff note in G5, which is why this matters.

DO NOT TOUCH `packages/orchestration/storage.py`. Its `_resolve_jobs_dir` is a
DIFFERENT symbol that merely contains the same substring, and it names the
CLASSIC store, deleted in T004. Do not touch `task_jobs_dir` itself either: the
new accessors are built on it and `data_paths._task_job_id_matches` still uses it.

THE GUARD — extend `TestJobAndRunLayout` in `tests/test_data_paths.py`:

  * `task_job_record_path(j)` is `task_job_dir(j) / "job.json"` and
    `task_job_dir(j)` is `task_jobs_dir() / j`, with the `root` override honoured
    by both — the same readings the D1 pair already has;
  * `pingpong_job` has NO attribute `_jobs_dir` — the name is gone, not merely
    unused. Assert it by `hasattr`, which reads the imported module rather than
    its text;
  * no module in the migrated set NAMES `_jobs_dir` at all, by the same AST
    reference reading the round-7 guard uses, over `pingpong_job.py` and
    `job_evidence.py`. State in the docstring that `storage.py`'s
    `_resolve_jobs_dir` is a different symbol and out of scope.

Keep every existing test in that class. Give the new tests the same non-vacuity
discipline the class already has.

## Constraints

1. Apply every authored slice BYTE FOR BYTE. If a slice looks wrong, apply it
   anyway and say so in the handback's deviations — do not repair it.
2. Nothing outside the change set above is created, edited or deleted.
3. Commit order is C0a, C0b, C1, C2, C3, C4, C5, each its own commit. C4 is ONE
   commit and touches ELEVEN files: deleting `_jobs_dir` breaks every caller at
   once, so a production-only or test-only commit would be red on its own, and
   AGENTS.md's own "keep commits small" yields here to "never commit a red tree".
   Declare its insertion count in the handback.
4. Every mutation of G6 runs ONLY inside a disposable `git worktree` under
   `.remedy-wt/` (self_drive_protocol.md G5), removed with
   `git worktree remove --force` before C5. Choose a worktree name that does not
   already exist there and delete nothing you did not create.
5. Purge `__pycache__` or run `python3 -B` for every mutation run.
6. Gates G1 through G8 all run AT C4, before C5 is written (§3 item 31).
7. `git status --porcelain` is empty at C5. Re-read `.agent/STOP` from disk before
   C4; if it exists, finish the commit in hand, write the handback and stop.
8. Push after C5: `git push origin feature/f260-one-world`. Never force-push.

## Done when — eight gates, each run and its real exit code recorded

G1 TRANSPORT (one digest). `sha256sum` over `.remedy-wt/f260-r8-block.md`,
   `.agent/authored/f260-r8.md` and `.agent/last_block.md` returns ONE value equal
   to BLOCK_SHA. Report the digest.

G2 THE RECORD. At C1: report `.agent/live_review.md` before and after and that the
   growth equals the appended byte count exactly. Prove (a) the 893805-byte
   pre-image is a byte-exact PREFIX; (b) the remainder is exactly `"\n"` + the
   GATE_R7 slice + `"\n"`; (c) the file's LAST blank-line unit, WITH THE FILE'S
   TERMINATING NEWLINE STRIPPED, equals the GATE_R7 slice — the convention your
   deviation 2 correctly said was missing last round. Two negative controls, one
   per region: a byte flipped inside the appended paragraph must make (c) reject,
   a byte flipped inside the pre-image region must make (a) reject. Report the
   unit count before and after — 425 then 426 — that the file ends with exactly
   one newline, that `^- R-[0-9]{4} — ` still matches 299 and
   `^Done: R-[0-9]{4} — ` still matches 4, the `^Gate: ` header count, and that
   they are all distinct.

G3 THE PROSE FILES. At C2: report `.agent/prose_slips.md`'s terminal byte before
   the append, its length before and after, that the pre-image is a byte-exact
   prefix, that the remainder is exactly `"\n"` + SLIP7 + `"\n\n"` + SLIP8 +
   `"\n"`, and its blank-line unit count before and after, which must rise from
   129 to 131 — a rise of exactly two, one per slip, which is the reading that
   catches a fused pair. At C3, `.agent/plan.md` equals the
   PLANF260R8 slice plus exactly one trailing newline; report its line count,
   which must be under 50.

G4 THE NAME IS GONE, AND THE PATHS ARE UNCHANGED. At C4:
   (a) `hasattr(pingpong_job, "_jobs_dir")` is False;
   (b) by AST, references resolving to exactly `_jobs_dir` number 0 in
       `pingpong_job.py` and 0 in `job_evidence.py`, and NON-ZERO in
       `storage.py` — report all three, the third being the non-vacuity reading
       that proves the search can find the name at all;
   (c) with `REMEDY_DATA_DIR` set to a temporary directory, report the actual
       paths and show `task_job_record_path(j) == task_jobs_dir() / j /
       "job.json"` and `task_job_dir(j) == task_jobs_dir() / j`. This is the
       VALUE-PRESERVATION property: the store has not moved this round, only its
       spelling.

G5 RUFF, OVER THE CHANGED FILES ONLY. Run `python3 -m ruff check` naming the ELEVEN
   files C4 touches, and nothing wider. Measured by the reviewer at `072b54ed`:
   over those eleven files ruff exits 0, but `ruff check packages/` exits 1 with 2
   errors and `ruff check tests/orchestration/` exits 1 with 11 errors, all
   PRE-EXISTING and none of them this round's. A directory-scoped gate here would
   be red whatever you did, so it is not ordered — do not widen it, and if you run
   a wider check out of curiosity, report it as context and not as this gate.

G6 THE MUTATION RED-PROOF (production code — mandatory in full). In a disposable
   worktree at C4, run the UNMUTATED CONTROL FIRST over
   `tests/test_data_paths.py` and report its exit code and pass count; then break
   these three PROPERTIES one at a time, restoring between each, and report each
   run's exit code and every failing node id:
   (i) the record path is `job.json` under the job's own directory — break it by
       returning `task_jobs_dir(root) / job_id / "job.json"` re-spelled as
       `task_jobs_dir(root) / "job.json" / job_id`;
   (ii) the `root` override is honoured — break it by ignoring `root` in
        `task_job_dir`;
   (iii) the deleted name stays deleted — break it by adding a `_jobs_dir`
         function back to `pingpong_job.py`, which must fail BOTH the `hasattr`
         reading and the AST reading, and report both node ids.
   The control must be GREEN before and after each.
   THEN, separately, prove the six production swaps are load-bearing: in the same
   worktree remove the function-scoped import from the site at the compound `and`
   expression and report that
   `tests/orchestration/test_job_worktree_handoff.py` goes RED with a `NameError`.
   That is the exact failure the reviewer's own dry run hit, and it is the reason
   this block names that site. Restore it and report the suite green again. Report
   `git worktree list` after the removal.

G7 THE SUITES, run SERIALLY in the primary checkout at C4, each exit code recorded
   separately — never through a pipe. All seven migrated test files:
   `test_failure_wiring.py`, `test_job_promote_consistency.py`,
   `test_job_stop_integration.py`, `test_job_worktree_handoff.py`,
   `test_job_worktree_integration.py`, `test_job_worktree_integrity.py`,
   `test_pingpong_integration.py` (all under `tests/orchestration/`), plus
   `tests/test_data_paths.py`, `tests/orchestration/test_job_evidence.py`,
   `tests/test_do_job_flow.py` and the canary `tests/cli/test_golden_path.py`.
   Report each suite's count and exit code.

G8 THE TREE AND THE CHANGE SET. At C4: `git status --porcelain` empty,
   `git ls-files .remedy-wt` empty, `.agent/STOP` absent, and `git worktree list`
   holds no worktree this round created. `git diff --name-only 072b54ed..C4` lists
   exactly the change-set paths above other than `.agent/handoff.md`, which C5
   adds; report the list as the command printed it, and report how many paths it
   printed rather than checking it against a numeral in this block. Report
   `python3 -m apps.cli.grouped integrity check --json` with its `passed` and
   `fail_count`.

## Handback

Rewrite `.agent/handoff.md` in C5 per docs/agents/handback_template.md: feature
and round, `SESSION 2 of feature F260`, branch, the per-commit SHAs with each
commit's insertion count from `git diff --numstat` (the `+` column), the
changed-files table, ONE LINE PER GATE G1 to G8 with its real exit code, the
open-findings count, the item-status table, and the next expected action. It has
no length cap. Declare every deviation, including any place this block is wrong.

<<<BEGIN PLANF260R8>>>
# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 to 7 are reviewed; 2 through 7 PASSED. T001 is
CLOSED. T002 is open: `data_paths` holds the one spelling of DECISION F260 D1's
target layout, every evidence path is built from it, and DECISION F260 D4 records
why the resolver waits for the store.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store `<data_root>/task_jobs/<16hex>/job.json` become one record with
one id shape minted by one function per kind; a Run becomes the evidence case a
Job points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

Give the PING-PONG store one spelling too. `data_paths` gains `task_job_dir` and
`task_job_record_path`, mirroring the D1 pair; `pingpong_job._jobs_dir` is
DELETED and its six users, `job_evidence`'s cross-module import of it, and
seventeen test call sites across seven files all move onto the accessors. The
store does not move: only its spelling changes, so the record move that follows
is a change to two function bodies rather than a sweep of every caller.

## Next Steps

- The record move itself: `task_job_dir` and `task_job_record_path` collapse into
  `job_dir` and `job_record_path`, so `<data_root>/task_jobs/<16hex>/job.json`
  becomes `<data_root>/jobs/<16hex>/job.json`. `data_paths._task_job_id_matches`
  moves with it, in the same commit, or every ping-pong job becomes unresolvable.
  Finding R-0814 is resolved there, against the fix clause it carries.
- The ONE resolver, in the same round group as that move, because 40 of the 42
  job-taking call sites take a `UUID` today (DECISION F260 D4).
- Then `runs/<run_id>/` keyed by run id, T003 consumer by consumer, T004 the
  classic runner, T005 the reachability test and the cluster deletion.

## Risks

- D1 changes what `<data_root>/runs/` is keyed by, from job id to run id. Every
  reader of the old shape must move in the same commit as its writer.
- `pingpong_job` imports `data_paths` only inside function bodies, so each call
  site carries its own import; one such site sits inside a compound boolean and
  is easy to miss.
- The T005 cluster deletion is large and reversible in one direction only. It
  runs last, behind a reachability test green BEFORE the first `git rm`.
<<<END PLANF260R8>>>

<<<BEGIN GATE_R7>>>
Gate: R7 — the F260 R7 entry. R7 PUT THE FOUR REMAINING HAND-BUILT EVIDENCE PATHS ONTO `data_paths.job_evidence_dir` AND WIDENED THE GUARD FROM ONE MODULE TO THE SET THAT OWNS A JOB'S EVIDENCE. VERDICT PASS. Range 99ca6406..072b54ed, seven commits, all single-parent, pushed to `origin/feature/f260-one-world`, no pull request created; the largest commit is 294 insertions and is a single `.agent/**` state write, the largest code commit 96, both under the AGENTS.md 500-insertion cap. THE REVIEWER RE-RAN ALL EIGHT GATES ITSELF. TRANSPORT: one digest `dcc306d01cc944bf8b03993c76882ff8ccb30881909cd2855160c573e66de8c0` across the reviewer's scratch original, the worker's saved copy at `.agent/authored/f260-r7.md` and the mirror at `.agent/last_block.md`; per §3 item 37 that chain covers those three artefacts and is NOT a claim about the bytes emitted into the worker's prompt. THE RECORD: `.agent/live_review.md` went 893805 from 887129, growth 6676 equal to `"\n"` plus a 6674-byte slice plus `"\n"`, the pre-image a byte-exact PREFIX, the two negative controls each rejecting in its OWN region and only there, blank-line units 424 to 425, registrations 299, `Done:` 4, sixteen `Gate:` headers all distinct. THE SLIP FILE IS THE ROUND'S REAL RESULT: `.agent/prose_slips.md` went 92673 to 94802 and its blank-line unit count rose 128 to 129 — a rise of exactly one, which is the reading round 6's recipe failed and this block gated. The counter-measure the round-6 defect earned was ordered, run, and came back green, and the reviewer reproduced the terminal-byte reading and the unit arithmetic independently. THE SHIPPED CODE WAS RUN, NOT READ: with `REMEDY_DATA_DIR` pointed at a scratch directory the reviewer confirmed all four migrated expressions equal their hand-built forms exactly, which is the value-preservation property the swaps rest on, and by AST that references resolving to exactly `jobs_dir` number ZERO in each of `pingpong_job.py`, `job_evidence.py`, `repair_attest.py` and `do_cmd.py` and TWO in each of `checkpoints.py` and `storage.py` — the second half being the non-vacuity reading, because a guard returning zero everywhere would be measuring nothing, and the excluded pair legitimately still names the CLASSIC store that T004 deletes. `ruff check` over the three changed production files exits 0. THE MUTATION RED-PROOF REPRODUCES INDEPENDENTLY: in a disposable worktree at `246efbb9`, module resolving from that worktree, the unmutated control is exit 0 at 40 passed; restoring the hand-built expression in `job_evidence.py` fails ONLY `test_no_module_that_owns_job_evidence_spells_the_path_itself[packages.orchestration.job_evidence]`, the same in `repair_attest.py` fails ONLY that guard's `repair_attest` case — so the parametrization is genuinely per-module and not one assertion wearing several names — and breaking the LAYOUT itself reddens the round-6 value tests instead, which proves the widened guard did not quietly replace the readings it was added beside. The control is green after each restore. THE SUITES, re-run serially by the reviewer, all exit 0 at 40, 93, 37, 7, 33, 178, 173 and 42, and `integrity check --json` returned `"passed": true` with `"fail_count": 0` over 5 checks at handlers=342. THE WORKER CORRECTED THE REVIEWER TWICE MORE AND BOTH ARE UPHELD. Its deviation 1 caught gate G8 saying the change set holds EIGHT paths other than `.agent/handoff.md` when the block's own list holds nine and `git diff --name-only` prints nine; the SET was complete and correct and only the numeral was wrong, which is §3 item 16 reaching a gate's own wording — the reviewer's pre-emission script measured the block's line count, its slice lengths and its append arithmetic, and never resolved that numeral against the list beside it. Its deviation 2 caught that gate G2(c) as worded is FALSE on a correct file: the last blank-line unit carries the file's terminating newline, so it is 6675 bytes against a 6674-byte slice, and the comparison passes only when that byte is stripped first — the reviewer's own verification script had been stripping it since round 5 without ever saying so, which is exactly how an unstated convention survives four rounds of green gates. Both are reviewer-prose defects over `.agent/` files with nothing wrong on disk, so under operator amendment amend0827-process-diet rule 2 each is a dated line in `.agent/prose_slips.md` and neither spends an R-id; the round-8 block states the newline convention inside G2(c) and asks the worker to REPORT the path count rather than check it against a numeral the block asserts. Its deviation 3 renamed the guard from `test_pingpong_job_no_longer_spells_the_evidence_path_itself` to `test_no_module_that_owns_job_evidence_spells_the_path_itself` because the old name claimed single-module scope over a now-parametrized set; that is the same defect class as a heading that miscounts its body, the worker checked that no code depends on the old node id, and the rename is upheld.
<<<END GATE_R7>>>

<<<BEGIN SLIP7>>>
2026-09-06 · F260 R7 (reviewer) · Gate G8 of the round-7 block ordered `git diff --name-only` to list "exactly the eight paths of the change set above other than `.agent/handoff.md`". The block's own change-set list holds TEN entries, so the count other than the handback is NINE, and the command prints nine. The set named was complete and correct in every member; only the adjective was wrong. The worker counted mechanically, reported nine, applied the gate as ordered and declared the discrepancy. THE LESSON: §3 item 16 was widened by finding R-0656 to reach a GATE's or a CONSTRAINT's own wording — a gate that names a CATEGORY of the block's own slices or paths names it and gives NO numeral, because the numeral is hand-counted while the extraction beside it is measured, so the two drift the moment the change set is edited and the hand-counted half is the one nobody re-reads. This block's change set grew by one path late in authoring and the gate's numeral did not follow it. The reviewer's pre-emission script measured the block's line count, every slice length and the whole append arithmetic, and never resolved that numeral against the list fifty lines above it — a mechanical check existed for everything except the one class the checklist names twice. The round-8 block orders the worker to REPORT the number the command printed instead of checking it against a numeral the block asserts. Reviewer-authored stale numeral in a gate; nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIP7>>>

<<<BEGIN SLIP8>>>
2026-09-06 · F260 R7 (reviewer) · Gate G2(c) of the round-7 block — and of the three blocks before it — ordered the reviewer's structural reading as "the file's LAST blank-line unit equals the GATE slice", and that sentence is FALSE of a correct file. Splitting the file on a blank line leaves the final unit carrying the file's own terminating newline, so it measures 6675 bytes against a 6674-byte slice and the comparison succeeds only when that byte is stripped first. The worker evaluated it with the byte stripped, said so, and warned that a reviewer running the naive comparison would get False on a correct file. The reviewer's own verification script had been stripping that newline since round 5 — `.rstrip("\n")` on the last unit — and never stated the convention anywhere the worker could read it, so four rounds of green gates rested on an agreement that existed only in the reviewer's code. THE LESSON: a gate is a sentence a second party must be able to execute, and a comparison whose operands need normalising states the normalisation or orders a property that needs none. This is §3 item 11's class arriving through an omission rather than a false claim: what was written was not measured against what was run, because the two lived in different artefacts and only one of them was ever read aloud. The round-8 block writes the stripping into G2(c) itself. Reviewer-authored unstated convention in a gate; every affected reading was in fact correct, nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIP8>>>
