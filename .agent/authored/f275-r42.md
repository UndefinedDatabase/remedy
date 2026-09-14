── STEP T003 / F275 — ROUND 42 — the unified-store widen the flip needs ──

Goal:
  DECISION F275 D21 rules the classic-to-unified record flip as ONE declared-oversize
  commit and describes it as a migration of consumers onto the unified record. A dry
  run of that commit, applied in a disposable worktree at `77a7d840` and RUN, measured
  three capabilities the classic store has and the unified store does not, so the flip
  as ruled is not executable: it would have to INVENT production API and its tests
  inside the one commit in this feature that cannot be split. This round widens those
  three in first, green by construction, on the precedent DECISION F275 D22 set one
  round ago for `TaskEntry` and DECISION F272 D5, D6 and D7 set for the `state`
  collapse. It records the reason as DECISION F275 D23, books the round 41 PASS
  verdict, and moves no consumer.

Bundle:
  C0a  save this block verbatim as `.agent/authored/f275-r42.md`
  C0b  mirror that file into `.agent/last_block.md`
  C1   the plan — slice PLAN42, whole-file replacement
  C2   the record — slices RECORD42, SLIPS42 and DECISION42, three appends
  C3   the widen — specification S1 to S6, described and not sliced
  C4   the handback

Change: exactly these eight paths and nothing else.
  .agent/authored/f275-r42.md                        (new, C0a)
  .agent/last_block.md                               (C0b)
  .agent/plan.md                                     (C1)
  .agent/live_review.md                              (C2)
  .agent/prose_slips.md                              (C2)
  .agent/decisions.md                                (C2)
  packages/orchestration/data_paths.py               (C3)
  packages/orchestration/pingpong_job.py             (C3)
  tests/orchestration/test_unified_store_parity.py   (new, C3)
  .agent/handoff.md                                  (C4)

WHAT WAS MEASURED, AND WHERE THE NUMBERS COME FROM. Every figure below was taken by
the reviewer at `77a7d840`, by `ast` over the files `git ls-files '*.py'` names, and
each was then confirmed by APPLYING the widen in a disposable worktree and running it.
No figure is a prediction and none is carried from an earlier round.

  W1  THE JOBS-ROOT OVERRIDE. 186 classic-store call sites pass one — 83 by the
      keyword `root=` and 103 as a positional — of which 56 are production. Neither
      `save_job_plan` nor `load_job_plan` accepts such an argument.
      `data_paths.job_record_path(job_id, root=None)` ALREADY accepts it, so the gap
      is a thread-through that was never threaded, not a missing layout.
  W2  CORRUPTION VISIBILITY. `storage.load_job_safe` returns `(job, degraded)` and is
      called at 6 sites, every one production. FOUR consume the flag, in
      `packages/orchestration/mission_state.py`, `packages/orchestration/task_execution.py`
      and `packages/orchestration/proposed_tasks.py` twice, and two discard it, in
      `packages/orchestration/gauntlet_runner.py` and
      `packages/orchestration/handoff.py`. `load_job_plan` returns `None` for a missing record and for an
      unreadable one alike, so a consumer moved onto the unified record would LOSE the
      distinction rather than spell it differently. That is a user-observable loss and
      operator amendment amend0908-f275-finish rule 4 would otherwise force this
      feature to register it against an inheriting feature that does not exist.
  W3  LISTING. `storage.list_jobs` is called at 11 sites and `storage.list_jobs_safe`
      at 6, seventeen together and ten of them production. The unified store has NO
      listing function: a search for `def list_job_plans`, `def iter_job_plans`,
      `def all_job_plans` and `def load_all_job` over `packages/` and `apps/` returns
      nothing at all.

THE GUARD THIS ROUND'S FIRST DRAFT TRIPPED, recorded because it fixes S1's placement
and because a reader would otherwise move the code back. The dry run first put the
`*/job.json` glob inside `pingpong_job.list_job_plans_safe`, and
`tests/test_data_paths.py` went RED with
`packages.orchestration.pingpong_job references data_paths.jobs_dir at lines [510, 512]`:
`pingpong_job` is one of the four modules that test's `_JOB_EVIDENCE_OWNING_MODULES`
binds, and DECISION F260 D1 makes `data_paths` the only module allowed to spell a
job's layout. The glob therefore belongs beside `job_record_path`, which is what S1
orders and why S2 forbids the other placement.

SPECIFICATION — THE PRODUCTION CHANGE IS DESCRIBED, NOT SLICED. Write it under
AGENTS.md's Mandatory Self-Review Loop and its File Editing Safety Rules. Apply the
repository's own naming and comment conventions; where this specification and those
conventions disagree, follow the conventions and declare it.

  S1  `packages/orchestration/data_paths.py` gains ONE public function, placed
      directly above `job_evidence_dir` so it sits beside `job_record_path`, the
      accessor it is the plural of:

        def job_record_paths(root: Path | None = None) -> list[Path]:

      It returns every persisted job record under `root`, sorted by path: built on
      `jobs_dir(root)`, globbing `*/job.json`, and returning `[]` when that directory
      does not exist, so no caller has to decide whether "no jobs" and "no store"
      differ. Its WHY comment carries ONE fact and it is this: the shape of the store
      is a layout fact and DECISION F260 D1 puts every layout fact in this module, so
      a caller that globbed for itself would be the second place a layout change has
      to happen.

  S2  `packages/orchestration/pingpong_job.py` threads the override through the three
      functions that resolve a record path, each keeping its present behaviour when
      the argument is omitted:

        def _persist_job(job: JobPlan, root: Path | None = None) -> Path:
        def save_job_plan(job: JobPlan, root: Path | None = None) -> Path:
        def load_job_plan(job_id: str, root: Path | None = None) -> JobPlan | None:

      Each passes `root` to `job_record_path(..., root)`. NO LINE of this module may
      name `jobs_dir` or glob the store — see the guard above; the listing reaches the
      layout only through S1's accessor.

  S3  `pingpong_job` gains the unified counterpart of `storage.load_job_safe`:

        def load_job_plan_safe(job_id: str, root: Path | None = None) -> tuple[JobPlan | None, bool]:

      `(None, False)` when no record exists, `(None, True)` when one exists and cannot
      be read, `(plan, False)` on success — the contract `load_job_safe` carries for
      the classic record, and the three answers the four production sites named in W2
      act on. It catches `OSError`, `_json.JSONDecodeError`, `KeyError`, `ValueError`
      and `TypeError`: the first three are what `load_job_plan` already catches, and
      the last two are what `_import_job` raises on a record whose JSON parses into
      the wrong shapes. No input makes this function raise.

  S4  `pingpong_job` gains the unified counterpart of `storage.list_jobs_safe`:

        def list_job_plans_safe(root: Path | None = None) -> tuple[list[JobPlan], bool, list[str]]:

      It iterates `job_record_paths(root)`, imports each record, skips one it cannot
      read and names it in the third element BY JOB ID — the record's directory name —
      where the classic counterpart names a file name, because one directory per job
      is what makes the id the honest identifier here. `degraded` is true when
      anything was skipped. The list is sorted by `created_at` DESCENDING, newest
      first, matching the classic function. No input makes this function raise.

  S5  `pingpong_job` gains `def list_job_plans(root: Path | None = None) -> list[JobPlan]:`,
      returning S4's first element and discarding the other two — the plain reader, as
      `storage.list_jobs` is the plain reader over `list_jobs_safe`.

  S6  A NEW FILE `tests/orchestration/test_unified_store_parity.py` pins the three
      capabilities and the backward compatibility that makes the widen green. Its
      module docstring states WHY the file exists: the dry run that measured W1, W2 and
      W3, and the decision that route follows. It covers, at minimum, each of these as
      its own test, and each test name says which property it pins:
        (a) a save under an explicit root writes at `<root>/jobs/<job_id>/job.json`;
        (b) a record written under a root loads back through the same root;
        (c) a record under one root is invisible under another;
        (d) omitting the override resolves where it resolved before;
        (e) a missing record reads `(None, False)`;
        (f) an unreadable record reads `(None, True)`;
        (g) a readable record reads `(plan, False)`;
        (h) the plain reader CANNOT tell missing from unreadable, and the safe reader
            can — the gap this widen closes, written as a test and not as a comment;
        (i) an absent store lists nothing and does not raise;
        (j) every persisted record is listed newest first;
        (k) an unreadable record is skipped and named by its job id;
        (l) the plain listing hides the degraded flag;
        (m) the layout glob lives in `data_paths` and the accessor S1 adds returns the
            records sorted by path, with `[]` for an absent store;
        (n) a record written before this round, carrying none of the new keys, still
            loads.
      Every test isolates through `tmp_path` and the override, never through the
      process data root, so no test can write into the repository's own `.data`.

Constraints:
  1. EVERY SLICE IS APPLIED BYTE FOR BYTE. Extract each one MECHANICALLY by its
     `BEGIN-`/`END-` marker lines from the COMMITTED `.agent/authored/f275-r42.md`,
     read with `git cat-file blob`, and apply it with file writes or byte
     concatenation in Python. Never retype a slice, never reflow one, and never
     edit one even where you believe it wrong — declare it instead. A marker line is
     never part of a slice's content.
  2. AN EOF-APPEND IS PURE CONCATENATION. Each append slice's content already begins
     with the blank line that separates it from what precedes it, so the operation is
     exactly `old_bytes + slice_bytes` with nothing inserted between them. Every
     target named in C2 ends with a newline at this round's base; do not add one.
  3. THE PRODUCTION CHANGE IS DESCRIBED, NOT SLICED. S1 to S6 fix behaviour, seam and
     public surface; you write the code.
  4. THE COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4 and nothing is reordered, merged or
     added. C1 comes before C2 because the plan must be current before the round
     touches the finding ledger (planner_reviewer_prompt.md §3 item 23).
  5. THE CHANGE SET IS EXACTLY THE EIGHT PATHS the Change list names plus the two new
     files it marks `(new, …)`. No path under `apps/`, `docs/` or `scripts/` moves.
     Nothing else is touched, created or deleted.
  6. THIS ROUND REGISTERS NO FINDING AND RESOLVES NONE. The open set is 86 by distinct
     id at this base and is 86 at C3. Do not mint an id; the next free one is R-0875
     and it stays free.
  7. NEVER `cd` INTO A WORKTREE, for any purpose. If a gate needs a disposable
     worktree, address its files by ABSOLUTE path and run commands there with
     `subprocess.run([...], cwd=<abs worktree>)`. Run `git status --porcelain` in the
     PRIMARY checkout in the SAME command sequence as any mutation, before reading the
     mutation's result, and revert with a sha256 re-read. Remove and prune the
     worktree before the handback.
  8. RUN `python3 -m pytest`, never bare `pytest`. The `remedy` console script is
     sandbox-blocked in these sessions; if a CLI reading is needed use
     `python3 -m apps.cli.grouped <group> <cmd>` and say which form you ran.
  9. THIS BLOCK IS CAPPED AT 490 LINES TOTAL AND 400 LINES OF PROSE, where PROSE is
     TOTAL minus the summed content lines of every slice and the marker lines count as
     prose (DECISION F085 D6 and D5). Measure BOTH from the committed
     `.agent/authored/f275-r42.md` blob, report both in the handback, and say plainly
     if either is exceeded. Do not fix an overage — declare it.
 10. READ `.agent/STOP` FROM DISK before the first commit and again before C3. If it
     exists, finish the commit in hand, write the handback and stop.

Done when: ten gates. Run each as `bash -c '<cmd>; echo "REAL_EXIT=$?"'` and record the
real exit code and the real numbers — one line per gate in the handback. A gate's
reading is taken at the commit named beside it, which is always EARLIER than C4, the
commit that writes the handback.

  G1  TRANSPORT, at C0b. `.agent/authored/f275-r42.md` and `.agent/last_block.md` have
      the SAME sha256 and the same byte count, and `.agent/last_block.md` was written
      from `git cat-file blob <C0a>:.agent/authored/f275-r42.md` rather than retyped.
      Report both digests and the byte count. This covers the two committed artefacts
      and claims nothing about the bytes emitted into your prompt
      (planner_reviewer_prompt.md §3 item 37).
  G2  THE PLAN, at C1. `.agent/plan.md` is BYTE-EQUAL to the PLAN42 slice as
      extracted; report its byte count, its sha256 and its line count against the
      AGENTS.md cap of 50, and the count of `^## Goal$` and `^## Next Steps$`, each of
      which must read exactly 1.
  G3  THE RECORD, at C2, for EACH of the three appends, against COMMITTED blobs only —
      pre at C1 and post at C2, read with `git show <rev>:<path>`.
      (a) Reader A, bytes: the post blob EQUALS the pre blob followed by the slice,
          exactly, with nothing between them. Report pre bytes, slice bytes, post
          bytes and whether the reconstruction is identical.
      (b) Reader B, structural: count N as the number of blank-line-separated
          paragraphs IN THE SLICE — count it, do not take a number from this block —
          then compare the LAST N such paragraphs of the post blob against the
          slice's N paragraphs IN ORDER.
      (c) A negative control per append: flip ONE byte inside the FIRST appended
          paragraph and confirm that BOTH readers REJECT it. Report four outcomes per
          append: A and B on the true bytes, A and B on the control.
      (d) `^Gate: F275 R41 ` reads 0 at C1 and exactly 1 at C2;
          `^## DECISION F275 D23 ` reads 0 at C1 and exactly 1 at C2.
      Where a formula in this block and the ORDERED OPERATION disagree, the operation
      wins and you declare the disagreement.
  G4  THE OPEN SET, at C3. By DISTINCT ID: the count of distinct ids matching
      `^- R-\d+ — ` minus the count of distinct ids matching `^Done: R-\d+ — `, read
      from `git show <rev>:.agent/live_review.md` into memory and never by writing over
      the tracked file. Report the three numbers at this round's base `77a7d840` and
      again at C3, plus the list of ids registered this round and the list resolved.
      Both lists must be empty and both readings must be 86.
  G5  THE WIDEN IS GREEN, at C3. Run, and report each separately:
        python3 -m pytest tests/orchestration/test_unified_store_parity.py -q
        python3 -m pytest tests/test_data_paths.py tests/storage/test_persistence.py -q
        python3 -m pytest tests/cli/test_golden_path.py -q
        python3 -m ruff check packages/orchestration/data_paths.py packages/orchestration/pingpong_job.py tests/orchestration/test_unified_store_parity.py
      Then prove the surface through the SHIPPED functions rather than by grep, in one
      `python3 -c` run: import `pingpong_job` and `data_paths`, print
      `inspect.signature` of `job_record_paths`, `save_job_plan`, `load_job_plan`,
      `load_job_plan_safe`, `list_job_plans` and `list_job_plans_safe`, and print the
      file each module was imported FROM so no installed copy can be mistaken for the
      work tree.
  G6  THE WIDEN BITES — MUTATION RED PROOF, at C3, in a DISPOSABLE worktree detached
      at C3 under constraint 7, with `__pycache__` purged before every run and every
      run under `python3 -B`, the selection scoped to
      `tests/orchestration/test_unified_store_parity.py`. Print the imported module's
      file path before believing any result. Run the UNMUTATED control FIRST, then
      each mutation below, then the control again after every revert. For each
      mutation report the anchor's count BEFORE it is applied (it must read 1), the
      real exit code, and WHICH NODE IDS FAILED — read from the `FAILED ` lines, where
      the node id is the token after the FIRST space, and never inferred from the exit
      code. DO NOT REPORT A PREDICTED COUNT; report what ran. A mutation that stays
      GREEN is the honest answer to declare, not to paper over: it means the test
      ordered for it does not reach the line, and declaring that is the round working.
        M1  in `load_job_plan`, drop `root` from the `job_record_path` call so the read
            ignores the override.
        M2  in `load_job_plan_safe`, make the except branch return `(None, False)`
            instead of `(None, True)`.
        M3  in `list_job_plans_safe`, delete the `sort` line so the listing loses its
            newest-first order.
        M4  in `data_paths.job_record_paths`, change the glob from `*/job.json` to
            `*.json`, the CLASSIC store's shape.
      Report each revert's sha256 against the pristine digest, and state that both
      touched files equal their pristine digests after the last revert.
  G7  THE LAYOUT GUARD, at C3. `python3 -m pytest tests/test_data_paths.py -q` is
      green, AND an `ast` reading of `packages/orchestration/pingpong_job.py` at C3
      reports ZERO references to the name `jobs_dir` — the guard whose red reading is
      quoted above, re-measured rather than assumed.
  G8  NOTHING ELSE MOVED, at C3. `.agent/STOP` read FROM DISK is ABSENT.
      `git status --porcelain` is EMPTY. `git worktree list` reads exactly ONE entry.
      `git diff --name-only 77a7d840..<C3>` is an EXACT SET MATCH against the Change
      list minus `.agent/handoff.md`: report the MISSING set and the EXTRA set, both of
      which must be empty. Report ZERO paths under `apps/`, `docs/` or `scripts/`.
      Report each commit's INSERTION count for C0a, C0b, C1, C2 and C3 against the
      AGENTS.md DECISION F104 D1 cap of 500 insertions; C4's own numbers are not
      ordered here, because its text cannot count itself.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md, carrying
the mandated sections — the state block with the SESSION NUMBER of this feature, the
range, a per-commit changed-files table with a reason per path, external actions,
one line per gate with its REAL exit code and real numbers, the item-status table, the
open-findings count, and your deviations. This is SESSION 18 of F275 and round 42;
F275 stands at 42 rounds against the operator's soft limit of 60 rounds and 20
sessions (amend0908-f275-finish rule 1), so no scope report is owed. Add the one
sentence of context self-assessment amend0905-throughput requires. State the measured
TOTAL and PROSE line counts constraint 9 orders. Then push the branch. Create no pull
request, merge nothing, force-push nothing and rewrite no history.

--- BEGIN SLICE PLAN42 ---
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, and the classic runner's whole
command surface is gone as of round 34.

## Current Step

ROUND 42 widens the UNIFIED STORE with the three capabilities the classic store has and it
lacked, measured by applying the flip in a disposable worktree and running it: a jobs-root
override, which 186 classic call sites pass and `data_paths.job_record_path` already
accepted; corruption visibility, which four production sites read off
`storage.load_job_safe`; and listing, which seventeen call sites use and the unified store
did not offer at all. DECISION F275 D23 records why this precedes the flip rather than
riding inside it. Green by construction — no consumer moves.

## Next Steps

1. The flip itself, now that its target API exists: applied from the round 36 site
   enumeration and the round 38 seam list, as the one declared-oversize commit AGENTS.md
   permits per feature, with the inseparability reason AND the real size stated in the
   handback BEFORE review. The `Job` type sites DECISION F275 D21 counts as part (c) and
   the `Task` type sites DECISION F275 D22 counts have no committed per-site enumeration,
   so that round either enumerates them first or states that it applied them from a
   measurement taken in its own worktree.
2. The resolver collapse DECISION F260 D5 places in T003 — `resolve_any_job_id`, the "TWO
   job stores" paragraph, every which-store branch and the absence test — with the classic
   store, which is the same commit range by that decision's own terms.
3. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- Step 1 is the largest single commit this repository will take, and every round that
  measures it has found it larger: DECISION F275 D17 sized it at 1766 changed lines, D21 at
  3771 across 263 files, D22 added a type pair worth 427 more, and D23 found that three
  pieces of its target API did not exist.
- The open set is 86 by distinct id at this round's base `77a7d840`. This round registers
  none and resolves none. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's,
  per DECISION F272 D12.
--- END SLICE PLAN42 ---

--- BEGIN SLICE RECORD42 ---

Gate: F275 R41 — the F275 round 41 entry. VERDICT PASS, written by the planner and reviewer of session 17 after reading the committed range `bbede92f`..`17be0eb4` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs, and booked here by round 42 rather than by a round of its own, under operator amendment amend0827-process-diet rule 1, whose durable carrier was the round 41 handback committed at `a75d72d1` with the verdict appended at `77a7d840`. Six single-parent commits C0a `addded9d`, C0b `f0894ab7`, C1 `83904d14`, C2 `82d36d9d`, C3 `17be0eb4` and C4 `a75d72d1`, per-commit insertions 421, 356, 15, 6 and 98 for the five before the handback, every one far under the AGENTS.md DECISION F104 D1 cap of 500. G1 TRANSPORT covers the chain this workflow can walk, per §3 item 37, and not the emitted bytes: the delegation source was written AND HASHED BEFORE delegation at `0c3a56c2fee41894378b9fa042dd6493d6962641652d876783f9e818539419d4`, and both committed copies are 26383 bytes at that digest as ONE shared git blob `1aa34ec1874015a6eefeedca2a4ace269b3d5f9d`. G2: `.agent/plan.md` byte-identical to PLAN41 at 2441 bytes, 42 lines against the cap of 50, both mandated headings exactly once. G3: `.agent/live_review.md` 851931 to 855619 and `.agent/prose_slips.md` 233188 to 234601, each post-blob equal to its pre-blob then ONE newline then the slice, both joining bytes read back as newlines, both structural readers true with N counted FROM THE SLICE, all four negative controls REJECTED by both readers with the flipped byte inside the FIRST appended paragraph, and `^Gate: F275 R40 ` exactly 1. G4: the open set is 86 BY DISTINCT ID at the base and at C3, over 103 registrations against 17 resolutions, with no id registered and none resolved. G5 IS THE GATE THIS ROUND TURNED ON and it holds as ONE CHAINED RECONSTRUCTION PER FILE, committed blob to committed blob: `packages/orchestration/pingpong_job.py` rebuilds from 164734 bytes to the committed 165637 by applying pairs H, I and J in the constraint-5 order, byte-identical at sha256 `8aadab4b…`, and all three are APPEND-SHAPED re-measured rather than assumed — each `TO contains FROM` reads true, so a FROM-zero count is unattainable by construction and none was ordered or taken, per §4.9 and §3 item 15; `tests/orchestration/test_job_administrative_fields.py` rebuilds from 8785 to 12481 by applying pair L and then appending K, with the post-L state a byte-exact PREFIX of the committed blob and K an exact SUFFIX, which is the ORDERED EQUALITY that binds a CODE append and never the per-line count that binds prose, per finding R-0531. `ruff` printed `All checks passed!` on both files, re-run by the reviewer. G6: the widen was built and red-proved by the reviewer BEFORE delegation and the worker's readings reproduce it in all four runs — control `12 passed` at exit 0, M1 deleting the export line and M2 deleting the import line each exit 1 at `2 failed, 10 passed` naming the SAME two assertions, `test_both_survive_the_round_trip_through_json` and `test_both_survive_the_real_job_record_file`, read from the `FAILED` lines rather than inferred from the exit code, both reverts byte-exact by sha256 against the pristine `8aadab4b…`, and the control green again. The reviewer additionally ran the whole orchestration suite with the widen applied and read `11879 passed, 10 skipped` with one failure, `tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`, then measured that same node id failing IDENTICALLY at the unmodified base in the same worktree — the known fresh-worktree artefact, not this change. G7: the scoped gate plus the canary read `54 passed` at exit 0, and the shipped-function probe reads `dataclasses.fields(TaskEntry)` at 25 fields with both `output_artifact_ids` and `budget` present, a bare `TaskEntry(task_id="x")` reading `[]` and `None` for them, and `_export_job`'s task dict carrying both over 25 keys. G8: the change set is an EXACT set match with MISSING and EXTRA both empty, ZERO paths under `apps/`, `docs/` or `scripts/`, porcelain EMPTY, ONE worktree, `.agent/STOP` absent. THE WORKER DECLARED NO DEVIATION AND THE REVIEWER FOUND NONE. It stated two ABSENCES explicitly rather than leaving them to be read as omissions — no FROM-zero count for the three append-shaped pairs, and no per-line count for the code append — and it CHECKED a claim the block made rather than believing it, confirming against the source that `JobPlan.budgets` really is a serialized dict on the same record and that it is a DISTINCT field from the administrative `budget` DECISION F272 T002 added. That is the round auditing the block. NO FINDING IS REGISTERED BY THIS GATE AND NONE IS RESOLVED.
--- END SLICE RECORD42 ---

--- BEGIN SLICE SLIPS42 ---

2026-09-10 · F275 R42 · The round 41 handback and `.agent/plan.md` both say the flip is applied from THREE COMMITTED LISTS, and two of the three are enumerations while the third is not: `.agent/f275_t003_task_pair.md` section 4 gives the `Task` type sites as three COUNTS over 427 changed lines in 111 files and names no path or line, and DECISION F275 D21's part (c) — the `Job` type sites, 1294 lines in 201 files — says in its own words that it was "re-derived here because no committed file enumerates them". So roughly 1721 of the 3771 declared lines have no per-site list to apply, and the flip round owes either an enumeration or a declaration that it applied them from a measurement taken in its own worktree. Nothing on disk under `packages/`, `apps/`, `tests/` or `docs/` is wrong, so this is a dated line and not an id, per operator amendment amend0827-process-diet rule 2.
--- END SLICE SLIPS42 ---

--- BEGIN SLICE DECISION42 ---

## DECISION F275 D23 (2026-09-10, F275 round 42) — the flip's target API did not exist: the unified store lacked three capabilities the classic store has, and they are widened in BEFORE the flip

WHAT THIS AMENDS AND WHAT IT LEAVES ALONE. DECISION F275 D21 rules the classic-to-unified record flip as F275's ONE declared-oversize commit and measures its floor at 3771 changed lines across 263 files. That ROUTE is unchanged here and this decision does not reopen it. What D21 describes, and what this decision corrects, is the KIND of change that commit contains: D21 and DECISION F275 D17 before it both read the flip as a migration of consumers from one record onto another, and a dry run of exactly that commit establishes that three parts of the record it migrates ONTO did not exist. D21's and D17's landed text is NOT rewritten, per planner_reviewer_prompt.md §3 item 20; this paragraph is their dated extension. DECISION F275 D22 is the precedent rather than the thing amended: it found a second type pair one round ago and ruled that the pair is landed by WIDENING `TaskEntry` first, in its own commit, before the flip. This is the same move over the store instead of the record.

THE MEASUREMENT, taken by the reviewer at `77a7d840` by `ast` over the files `git ls-files '*.py'` names, and then CONFIRMED by applying the widen in a disposable worktree and running it rather than by reading the result off the counts. FIRST, the jobs-root override: 186 classic-store call sites pass one, 83 by the keyword `root=` and 103 as a positional, 56 of them production, and neither `save_job_plan` nor `load_job_plan` accepted such an argument — while `data_paths.job_record_path(job_id, root=None)` already did, so the gap was a thread-through nobody had threaded. SECOND, corruption visibility: `storage.load_job_safe` returns `(job, degraded)` at 6 production call sites and FOUR of them act on the flag, in `packages/orchestration/mission_state.py`, `packages/orchestration/task_execution.py` and `packages/orchestration/proposed_tasks.py` twice, while `load_job_plan` returns `None` for a missing record and an unreadable one alike. THIRD, listing: `storage.list_jobs` and `storage.list_jobs_safe` are called at 17 sites, 10 of them production, and the unified store had no listing function of any spelling.

WHY THAT MAKES THE FLIP AS RULED UNEXECUTABLE, stated as the consequence rather than as a complaint. Moving a consumer onto an API that lacks the parameter it passes is not a migration, it is the invention of that API, and the one commit this feature is permitted to declare oversize would then carry NEW production functions together with the tests that pin them. AGENTS.md's Commit Discipline forbids mixing new features with refactoring in one commit, and that commit is by construction the one commit in F275 that cannot be split to repair the mixture. The second cost is a reading nobody could take: a reviewer cannot tell a migration that dropped a capability from one that never had it, so the `degraded` flag four production sites read would have been lost silently, which operator amendment amend0908-f275-finish rule 4 exists to prevent and which no gate over a rename could see.

CHOSEN: THE THREE CAPABILITIES ARE WIDENED IN FIRST, IN THEIR OWN COMMIT, BEFORE THE FLIP. `data_paths` gains `job_record_paths`, the plural of `job_record_path` and the one place the store's `*/job.json` shape is spelled; `pingpong_job` threads an optional `root` through `_persist_job`, `save_job_plan` and `load_job_plan`, and gains `load_job_plan_safe`, `list_job_plans_safe` and `list_job_plans`. Every parameter is optional with the present default and every function is an addition no existing caller reaches, so the commit is GREEN BY CONSTRUCTION and it shrinks the atomic commit that follows by everything it carries. A widen is not the compatibility reader AGENTS.md's Scope Control forbids: the classic store still dies in the flip, and nothing is left alive beside its replacement. The glob's PLACEMENT is ruled rather than left to taste, because the dry run measured it: the first draft put it in `pingpong_job` and `tests/test_data_paths.py` went red, since that module is one of the four `_JOB_EVIDENCE_OWNING_MODULES` bind and DECISION F260 D1 makes `data_paths` the only module allowed to spell a job's layout.

ALTERNATIVES CONSIDERED, each rejected on a measurement rather than a preference. (i) Carry the three inside the one oversize flip commit — rejected on the two costs above, and on arithmetic: it adds production API and a test file to a commit D21 already measures at 7.5 times the per-commit cap. (ii) Drop the three capabilities and register findings for what is lost — rejected for the override, which 186 call sites pass and which therefore makes the flip uncompilable rather than merely poorer, and rejected for `degraded` on its four production consumers; there is no inheriting feature that owns "the job store reports corruption", so rule 4's registration would name nothing. (iii) Rewrite the 186 override sites onto the unified store's existing isolation route, the `data_dir` configuration key — rejected because it replaces a parameter pass with a process-wide monkeypatch at 130 test sites, inside the one commit that cannot be split, and because it changes what those tests isolate rather than where they isolate it. (iv) Give the unified store a `root` parameter only, and leave listing and corruption visibility to the flip — rejected because it splits one measured gap across two commits for no gain, and the flip commit would still be the one inventing API.

HOW TO REVERSE: delete this decision and revert the widen commit. DECISION F275 D21's route stands either way; what is lost by reversing is the flip's target API, and the flip would then have to invent it inside the one commit in this feature that cannot be split.
--- END SLICE DECISION42 ---
