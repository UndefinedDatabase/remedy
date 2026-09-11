── STEP T003 / round 50 — F275 ───────────────────────────────
Goal:        Record what the flip dry run measured against a tree whose id shape is now one
             spelling, and rule what it found. The migration DECISIONs F275 D26, D27 and
             D28 performed removed 369 failures and nothing else; the flip still causes
             2557 failures and 106 errors against a control taken at the same commit. Book
             the round 49 PASS verdict and the resolution of `R-0876`.

Bundle:      C0a  save this block verbatim as `.agent/authored/f275-r50.md`
             C0b  mirror it into `.agent/last_block.md` from the committed blob
             C1   slice PLAN50 — whole-file replacement of `.agent/plan.md`
             C2   slices RECORD50, DONE50 and SLIPS50 — the round 49 PASS verdict, the
                  authored resolution of `R-0876`, and one dated reviewer slip
             C3   slice ARTEFACT50 — the new file
                  `.agent/f275_t003_flip_residue_r50.md`, whole-file
             C4   slice DEC50 — DECISION F275 D29, appended to `.agent/decisions.md`
             C5   the handback, rewriting `.agent/handoff.md`

Change:      EXACTLY these paths and nothing else.
             `.agent/authored/f275-r50.md`  (new) · `.agent/last_block.md` ·
             `.agent/plan.md` · `.agent/live_review.md` · `.agent/prose_slips.md` ·
             `.agent/f275_t003_flip_residue_r50.md`  (new) · `.agent/decisions.md` ·
             `.agent/handoff.md`
             NO path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` moves this
             round. `.agent/f275_t003_flip_residue.md` is NOT edited: it records the run at
             `978046fe` and stays as written, per planner_reviewer_prompt.md §3 item 20.

Constraints:
 1. Apply every slice BYTE FOR BYTE; extract each mechanically from the COMMITTED blob of
    `.agent/authored/f275-r50.md` by its `BEGIN-<name> ` / `END-<name> ` marker-line
    PREFIX. Never retype, reflow or edit one. A slice that looks wrong is applied as given
    and DECLARED.
 2. The commit order C0a, C0b, C1, C2, C3, C4, C5 is FIXED — none merged, none reordered.
    C1 precedes C2 because a round that books into the finding ledger advances the plan
    first (planner_reviewer_prompt.md §3 item 23).
 3. EVERY length is `len(<bytes>)` from `read_bytes()` or a `git show` byte stream, never
    `len()` over a decoded `str`.
 4. The four appends — RECORD50, DONE50, SLIPS50, DEC50 — are `old_bytes + slice_bytes` in
    Python. Each owns its leading blank line. All four pre-blobs end in a newline; add none.
 5. This round RESOLVES `R-0876` and registers nothing. DONE50 is the reviewer's authored
    resolution; the `Landed: R-0876` line already in the record is NOT deleted or rewritten
    — an append-only record keeps both, and the `Done:` paragraph is what closes the id.
    The open set goes 87 at the base to 86 at C2.
 6. ARTEFACT50 creates a file that does not exist at the base. Write it as the slice's
    bytes and nothing more: no heading added, no trailing byte added, no reflow. Its fenced
    code block and its indented output block are content.
 7. No mutation red-proof is ordered and none is owed: the change set holds no production
    line, no test line and no import, so there is no code whose colour a mutation could
    establish. That is stated rather than left out, because an absent red proof is normally
    a finding.
 8. Re-read `.agent/STOP` FROM DISK before the first commit and report what you found.

Done when:   the gates below, each run for real as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`,
             one line per gate in the handback, EVERY reading taken at C4 or earlier.
             Report the number of gates YOU ran; this block states none.

 G1  TRANSPORT, at C0b. sha256 over the bytes of `.agent/authored/f275-r50.md` equals the
     digest the delegation message states — this block carries marker lines for its SLICES
     only and no BEGIN marker of its own. `.agent/last_block.md` is written from
     `git cat-file blob <C0a-sha>:<that path>` and never retyped. Report both byte counts
     and both digests, and state the chain the proof walked. Claim nothing about the bytes
     emitted into your prompt.

 G2  THE PLAN, at C1. `.agent/plan.md` BYTE-EQUAL to slice PLAN50: both byte counts, both
     sha256 digests, the line count against the AGENTS.md cap of 50, `^## Goal$` exactly 1x
     and `^## Next Steps$` exactly 1x.

 G3  THE RECORD AND THE SLIPS, at C2. Read every pre and post blob with
     `git show <sha>:<path>` INTO MEMORY — never write a non-current revision over a
     tracked file.
     (i)  `.agent/live_review.md` ← RECORD50 then DONE50, applied in that order inside C2,
          pre at C1 and post at C2, all three readings:
          (a) reader A: pre_bytes + RECORD50 + DONE50 == post_bytes, `identical: True`.
          (b) reader B, structural: N is the number of blank-line-separated paragraphs your
              script COUNTS across the two slices — never a number this block asserts — and
              the LAST N blank-line units of the post blob equal those N paragraphs IN
              ORDER, stripped.
          (c) negative control: flip ONE byte inside the FIRST appended paragraph of the
              IN-MEMORY copy; reader A rejects AND reader B rejects, each re-run against
              the ORIGINAL slices.
     (ii) `.agent/prose_slips.md` ← SLIPS50, pre at C1 and post at C2, reading (a) alone.

 G4  THE ARTEFACT, at C3. `.agent/f275_t003_flip_residue_r50.md` BYTE-EQUAL to slice
     ARTEFACT50: both byte counts, both sha256 digests, and `git show <C2-sha>:<that path>`
     exits non-zero because the path does not exist at C2 — report that exit code, which is
     what makes this an addition rather than a rewrite. Then EXECUTE the artefact's own
     instrument: extract the single fenced `python` block that follows the line
     `<!-- INSTRUMENT -->` from the COMMITTED C3 blob, write it under `.remedy-wt/`, run it
     as `python3 -B <that file> .` from the repository root, and compare its stdout LINE BY
     LINE against the indented block the artefact records after the words
     `complete and untrimmed:` with four leading spaces stripped from each line. Report
     `recorded == actual` and, if False, both blocks in full — never a truncated diff.

 G5  THE DECISION, at C4. `.agent/decisions.md` ← DEC50, pre at C3 and post at C4, the same
     three readings as G3(i): reader A, reader B at N counted from the slice, and the
     negative control on the FIRST appended paragraph. Then report
     `^## DECISION F275 D29 ` counted over the C4 blob, which must be 1, and over the C3
     blob, which must be 0.

 G6  THE SCOPED ROUND GATE AND THE CANARY, in the PRIMARY checkout at C4, with
     `git status --porcelain` read empty immediately before each.
     `python3 -m pytest tests/ui_server/test_dashboard_contract.py
     tests/orchestration/test_development_artifact_boundary.py
     tests/orchestration/test_live_review_rotation.py tests/regression/test_resource_safety.py
     tests/orchestration/test_test_runner.py -q`
     and the canary `python3 -m pytest tests/cli/test_golden_path.py -q`. Report both last
     lines and both exit codes. That selection is the tests that READ the four `.agent/`
     files this round writes — `test_dashboard_contract.py` asserts `## Goal` and a Steps
     heading in `.agent/plan.md` directly — and it is the only claim made for it: it reaches
     the state contracts and no production behaviour, because this round changes none.

 G7  NOTHING ELSE MOVED, at C4.
     (a) `.agent/STOP` re-read from disk: report the literal result. `git status
         --porcelain` == `''`: report the literal string.
     (b) The changed-path set over `020b1d57..C4` equals the paths the Change section
         lists, other than `.agent/handoff.md` which C5 writes. Resolve that expectation
         against the Change section itself, not against a number stated anywhere in this
         block. Report MISSING and EXTRA as lists, and
         report the count of paths in that set under `packages/`, `apps/`, `tests/`,
         `docs/` or `scripts/`, which must be 0.
     (c) THE OPEN SET, BY DISTINCT ID over `.agent/live_review.md`: distinct `^- R-\d+ — `
         minus distinct `^Done: R-\d+ — `, at the base `020b1d57` and at C2. It reads 87 at
         the base and must read 86 at C2. Report the ids registered and the ids resolved
         this round as lists. Report `^Done: R-0876 ` counted at C1 and at C2, which are 0
         and 1, and `^Landed: R-0876 ` at both, which is 1 at both — the landed line
         survives beside its resolution.
     (d) Each of C0a..C4's own insertion count against the F104 D1 cap of 500, derived ONCE
         from `git show --numstat <sha>` and used both here and in the `+/-` column of the
         handback's `## Commits` table. A whole-file rewrite is exactly where a line count
         before and after diverges from what `numstat` reports, and the table is the half a
         later session reads.

Handback:    completion report + rewrite `.agent/handoff.md`. Carry SESSION 20 of F275,
             round 50, the item-status table with every ordered item exactly once, the
             deviations, and one sentence of context self-assessment.
──────────────────────────────────────────────────────────────

WHY THIS ROUND IS A MEASUREMENT AND NOT THE FLIP. The handback you are replacing names the
dry-run re-run as this round's work and says to take it BEFORE authoring anything. The
reviewer took it: two disposable worktrees at `020b1d57`, the transform applied in one and
the other left alone, the full suite run in both, and both removed and pruned before this
block was written. `git worktree list` reads one entry. The readings are in ARTEFACT50 with
the instrument that reproduces the half of them that does not need a twenty-minute run.

WHAT THE REVIEWER ALREADY MEASURED, so that no gate below re-derives it. The scoped
selection in G6 reads `161 passed` at exit 0 and the canary `42 passed` at exit 0, both in
the primary checkout at `020b1d57`. The artefact's embedded instrument, extracted from the
authored bytes and run from the repository root, reproduces its recorded output block line
for line. Every gate reading an authored text must carry was taken at a commit strictly
earlier than the commit that writes it: RECORD50 carries session 19's gates, and ARTEFACT50
and DEC50 carry the reviewer's dry run, which precedes C0a.

SESSION 20 IS F275's TWENTIETH AND THE SOFT LIMIT amend0908-f275-finish rule 1 names is 20
SESSIONS and 60 ROUNDS. The SCOPE REPORT that rule obliges is owed by the SESSION, not by
this round, and it is written into the handback of the last round of this session. Rule 2
forbids the amend0905-throughput split-and-close default here BY NAME: the session writes
the report and CONTINUES. Do not close F275, do not register a follow-up feature, and do not
touch `docs/roadmap/STATUS.md`.

────────── SLICES ──────────
The authored texts follow, in the order their commits apply them: PLAN50, RECORD50, DONE50,
SLIPS50, ARTEFACT50, DEC50. Each is delimited by its own `BEGIN-`/`END-` marker lines; the
marker lines are NOT part of any slice and never reach a target file. Every rule line in this
block's frame is a run of U+2500 BOX DRAWINGS LIGHT HORIZONTAL, and no rule LENGTH is
load-bearing: markers are matched by PREFIX and the frame carries no appliable bytes.

Slice shapes, mechanically. PLAN50 and ARTEFACT50 are WHOLE-FILE writes, the second of a
path that does not exist at the base. RECORD50, DONE50, SLIPS50 and DEC50 are prose APPENDS
applied as `old_bytes + slice_bytes`, each carrying its own leading blank line. No FROM/TO
pair is authored this round, so no containment test is owed and no FROM-zero count is
ordered.

BEGIN-PLAN50 ─────────────────────────────────────────────────
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

ROUND 50 re-runs the flip dry run against a tree whose id shape is one spelling, and records
what it measured in `.agent/f275_t003_flip_residue_r50.md`. The migration DECISIONs F275 D26,
D27 and D28 performed removed 369 failures and nothing else: measured against a control taken
at the same commit, the flip still causes 2557 failures and 106 errors. Three prerequisites
are diagnosed and ruled in DECISION F275 D29. The round 49 PASS verdict and the resolution of
`R-0876` are booked here.

## Next Steps

1. P1 — replace the transform's receiver-NAME heuristic with the DECISION F272 D7
   raising-property probe that `docs/roadmap/features/T2_F275.md` T002 already orders, and
   measure the real site set.
2. P2 — migrate the surviving `UUID(...)` coercions over a job or task id, one
   assignment-connected component per commit, as DECISION F275 D28 rules for an id widen.
3. P3 — the `**` splat call-graph pass over the test helper factories.
4. Re-run the dry run, then THE FLIP as the one declared-oversize commit AGENTS.md permits
   per feature, declared with its inseparability reason before review.
5. The resolver collapse DECISION F260 D5 places in T003, with the classic store.
6. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- F275 reaches the soft limit amend0908-f275-finish rule 1 names — 20 sessions — in this
  session, at 50 of its 60 rounds. Rule 2 forbids the split-and-close default here BY NAME:
  the session writes the scope report and CONTINUES.
- The three prerequisites are the diagnosed causes of MEASURED classes; nothing establishes
  that a fourth does not appear once they are fixed, and only another dry run settles it.
- The open set is 86 by distinct id once this round books `Done: R-0876`. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END-PLAN50 ───────────────────────────────────────────────────

BEGIN-RECORD50 ───────────────────────────────────────────────

Gate: F275 R49 — the F275 round 49 entry. VERDICT PASS. Written by the planner and reviewer of session 19, carried in the pushed `.agent/handoff.md` at `020b1d57` as amend0827-process-diet rule 1 permits, and booked here by the first substantive commit of round 50. The range read was `70d6c8e6`..`31e37b27` and EVERY GATE WAS RE-DERIVED INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line below. THE REPAIR IS RIGHT AND BOTH HALVES ARE PROVED SEPARATELY. G1 is the PRIMARY cmp-against-scratchpad proof and not the §4.9 digest fallback: the reviewer's scratch original survived, and the saved copy, its mirror and that original are one blob at 28474 bytes and sha256 `37081bec7b73c5e7d4de0fbf52ac2dc249a2dccc62ace4d6f92f7b37afadb113`. G2: `.agent/plan.md` is byte-identical to slice PLAN49 at 2557 bytes over 45 lines. G3: all four appends reconstruct exactly — `.agent/live_review.md` 892396 to 898518 bytes across RECORD49 and FIND49 together, `.agent/prose_slips.md` 240453 to 241765, and `.agent/live_review.md` again 898518 to 898808 for LANDED49 at C4 — with reader B true at N counted from the slices, N being 2, and the negative control rejected by BOTH readers with the flipped byte inside the FIRST appended paragraph. G4: both pairs are REWRITES on the containment test's own output, FROM reads 1 in each base blob and 0 in each C3 blob, TO reads 1, and the reviewer rebuilt each C3 blob from its base blob by applying that pair alone, byte-identical both times. G5: both guards are CODE APPENDS proved by ordered equality rather than by a multiplicity count — each base blob is a byte-exact PREFIX of its C3 blob, each slice a byte-exact SUFFIX, and base plus slice equals the C3 blob exactly at 25968 plus 861 and 33134 plus 1108. G6: both subtree digests equal the reviewer's own replay of this repair on a clean checkout, `packages` at `1f1a040413f8045a9e53ec8dece733ddb1d0c0ac` and `tests` at `b33e3ac3ed64ebd1d6fa4e0b86c9f8614c4d07ee`, and C3's own diff is exactly the four ordered rows; the reviewer re-ran the scoped selection itself at 175 passed and the canary at 42 passed, both exit 0. G8: the changed-path set matches exactly with MISSING and EXTRA both empty, `.agent/decisions.md` untouched, zero paths under `apps/`, `docs/` or `scripts/`, the open set 86 to 87 with `R-0876` the only id registered and none resolved, and `^Landed: R-0876 ` 0 at C3 and 1 at C4 against `^Done: R-0876 ` 0 at both. G7 IS THE GATE THIS ROUND EXISTS FOR AND THE REVIEWER RE-RAN IT AT THE COMMITTED C3 `9df09805`: the control reads `2 passed` at exit 0, M1 reverting PAIR49A reddens ONLY the `test_do_run.py` guard, M2 reverting PAIR49B reddens ONLY the `test_test_failure_repair.py` guard, and THE TWO NODE-ID SETS ARE DISJOINT — which is why two mutations were ordered rather than one, since neither fix's proof covers the other. Both reverts are byte-exact by sha256, the control is green again, and the primary checkout's porcelain read empty in the same command sequence as every mutation. THE WORKER DECLARED ONE CONTRADICTION AND IT WAS THE REVIEWER'S: G6(b) named the command `git diff --numstat 70d6c8e6..C3` and asserted it "reads exactly four rows", while that range spans C0a through C3 and therefore also carries the five `.agent/` rows those earlier commits wrote, so it reads NINE. The worker reported both readings, measured C3's OWN diff at exactly the four stated rows with exactly the four stated numerals, and edited nothing; it also found and fixed a node-id parser defect in its own throwaway probe before reporting G7, which is the difference between a gate and a number. Nothing on disk is wrong, so the reviewer's range error is a dated line in `.agent/prose_slips.md` and not an id, per amend0827-process-diet rule 2.
END-RECORD50 ─────────────────────────────────────────────────

BEGIN-DONE50 ─────────────────────────────────────────────────

Done: R-0876 — RESOLVED at F275 round 49's C3 `9df09805`. THE DEFECT: round 48's slice WIDEN48 wrapped every construction keyword it rewrote in `str(...)` unconditionally, because `ast` gives a generator no way to know whether an expression is nullable, and at two production sites the wrapped expression could evaluate to `None` — `packages/orchestration/do_run.py` in `_run_build_phase`, where a job with no tasks has no task to attribute its artifact to, and `packages/orchestration/test_failure_artifact.py` in `persist_failure_artifact`, where `TestFailureArtifact.task_id` defaults to the empty string. Both wrote the string `"None"` where `packages/core/models.py` documents an absence in the `Artifact` docstring itself, and `artifact_index.task_artifacts_by_kind` matches that field by equality, so the stored value was a truthy string no lookup could ever match. THE FIX moves the `str(...)` inside each conditional's true branch, so the false branch yields `None` again; it is one line per site and it changes nothing on the populated branch, where `str(UUID)` is what the widened field already required. THE GUARD, and why there are two: each site gained a test that constructs the artifact through the REAL function on the absent branch and asserts `task_id is None`, and the two are red-proved SEPARATELY because one mutation cannot establish two fixes — reverting the `do_run.py` line reddens only `tests/orchestration/test_do_run.py::TestSystemArtifactKeepsTaskIdAbsent`, reverting the `test_failure_artifact.py` line reddens only `tests/orchestration/test_test_failure_repair.py::TestSystemArtifactKeepsTaskIdAbsent`, and the reviewer measured the two FAILED node-id sets DISJOINT in its own disposable worktree at `9df09805`. Both guards fail on `assert 'None' is None`, which states the defect in the assertion's own words. THE RULE THIS LEAVES BEHIND, and it is the reason the finding was worth an id rather than a quiet fix: a mechanical rewrite that wraps an expression states what it assumes about that expression's NULLABILITY, and where the generator cannot know, the BLOCK sweeps for the conditional form before emission. No gate round 48 ordered could see this — the subtree digests matched, the scoped suite read 480 passed and the canary 42 passed — because no test reached either branch, which is exactly the class `.agent/f275_t003_flip_sites.md` section 3 names as invisible to both of the flip's instruments.
END-DONE50 ───────────────────────────────────────────────────

BEGIN-SLIPS50 ────────────────────────────────────────────────

2026-09-11 · F275 R49 · The round 49 block's G6(b) named the command `git diff --numstat 70d6c8e6..C3` and asserted that it "reads exactly four rows". That range spans C0a, C0b, C1, C2 AND C3, so it necessarily also carries the five `.agent/` state rows those earlier commits wrote, and it reads NINE. The four production rows and all four of their numerals are correct — they are C3's OWN diff, which the worker measured at `9df09805^..9df09805` and reported beside the nine-row reading, editing nothing. This is §3 item 22's class, a sentence quantifying across COMMITS that was written against the commit it meant rather than the range it named, and it is the second range-versus-commit slip of this session after round 46's G8. THE RULE THAT FOLLOWS: a gate that means ONE commit's diff names that commit's own range as `<sha>^..<sha>`, and a gate that means the round's cumulative change says so and states the row count it expects for the whole of it.
END-SLIPS50 ──────────────────────────────────────────────────

BEGIN-ARTEFACT50 ─────────────────────────────────────────────
# F275 T003 — the FLIP RE-RUN against the migrated id shape: what still blocks it

> Measured by the reviewer at `020b1d57`, this round's base, in two disposable `git worktree`s
> under the gitignored `.remedy-wt/`, both removed and pruned before the block was authored.
> THIS FILE RECORDS A DRY RUN; IT FLIPS NOTHING. No line under `packages/`, `apps/`,
> `tests/`, `docs/` or `scripts/` moved in the round that wrote it. It does not replace
> `.agent/f275_t003_flip_residue.md`, which records the run at `978046fe` and stays as written.

## 1. Why this reading was owed

DECISION F275 D26 ruled the flip NOT the next commit because a dry run of it at `978046fe`
left 2714 failing tests, and named the ID SHAPE as the largest unruled class. D27 and D28
migrated that shape one assignment-connected component at a time. The question those three
decisions leave is a measurement and not a prediction: with the shape migrated, does the flip
converge?

## 2. THE CONTROL, WHICH THE R46 RUN DID NOT HAVE

R46 reported 2714 failures against no baseline, so it could not tell a flip-caused failure
from a worktree artifact. This run takes both readings at the SAME commit, in two fresh
worktrees, with the same selection and the same flags.

    $ python3 -B -m pytest tests/ -q --tb=line -p no:randomly -p no:cacheprovider
    UNFLIPPED  1 failed, 18366 passed, 29 skipped, 1 warning in 1316.51s       REAL_EXIT=1
    FLIPPED    2558 failed, 15703 passed, 29 skipped, 1 warning,
               106 errors in 1248.09s                                          REAL_EXIT=1

The control's ONE failure is
`tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`,
which needs the gitignored `apps/ui/node_modules`, absent from every fresh worktree. It is
the only node id failing in BOTH runs. Differencing the two node-id sets gives 2557 failures
and all 106 errors CAUSED by the flip, against 1 shared failure and 0 errors in the control.
So the honest comparison with R46 is 2714 UNATTRIBUTED against 2557 ATTRIBUTED, and the
migration D26, D27 and D28 performed bought 157 of them.

## 3. What the applied transform did

`.remedy-wt/r46_flip_transform.py` unchanged — the same surgical `ast`-span text edits in
bytes, the same six rules, the same five exclusions. It rewrote 282 files and broke none;
`git diff --shortstat` reads 5390 insertions and 5232 deletions over those 282, of which 110
are under `packages/` or `apps/` and 172 under `tests/`; `pytest tests/ -q --co` then
collected 18396 tests at exit 0 with zero collection errors. Rewrites by rule, as the
instrument counted them: import moved 518, import split 218, T1 type name 1237, T2 job field
1896, T3 task field 532, T4 `description` 247, T4 `id` 107, T4 `name` 540, T5 seam 779, T6
isoformat 6 — 6080 in all.

## 4. The residue by class, the two runs beside each other

Both columns bucket the `E   <Exception>: <message>` lines of a `--tb=line` run by exception
type and by a message with quoted spans and digits normalised. R46's column is quoted from
`.agent/f275_t003_flip_residue.md` section 5; this run matched 2387 such lines.

| R46 | R50 | class |
|---:|---:|---|
| 867 | 867 | `TypeError: JobPlan.__init__() got an unexpected keyword argument 'X'` |
| 493 | 517 | `AttributeError: 'X' object has no attribute 'X'` |
| 271 | 368 | `TypeError: unsupported operand type(s) for /: 'X' and 'X'` |
| 256 | 269 | `ValueError: badly formed hexadecimal UUID string` |
| 241 | 0 | `pydantic ValidationError: N validation error for Artifact` |
| 128 | 0 | `pydantic ValidationError: N validation errors for TaskExecutionContext` |
| 14 | 14 | `TypeError: TaskEntry.__init__() got an unexpected keyword argument 'X'` |

THE MIGRATION DID EXACTLY WHAT IT WAS PERFORMED TO DO AND NOTHING MORE. The two pydantic
classes are gone in full — 369 E-lines to 0 — and the whole run now holds TWO
`ValidationError` lines, `1 validation error for Job` and `1 validation error for Task`, both
against the classic record the flip excludes. Every other class held or GREW, which is why
the total moved by 157 and not by 369: the classes below were never the id shape.

## 5. THE THREE PREREQUISITES THE FLIP STILL HAS, each measured

**P1 — THE FIELD RENAME IS DECIDED BY A RECEIVER-NAME HEURISTIC, and that is the
`AttributeError` class.** The transform renames `.id`, `.name` and `.description` whenever
the receiver's NAME contains `job`, `plan`, `record` or `task`, and never by resolving the
receiver's TYPE. Restricted to the run's `E ` lines, attribute misses total 551 over 22
distinct receiver-and-attribute pairs, and the largest are every one of them a receiver whose
name matched while its type is not `Job` or `Task`:

    191 PlannedTask.task_id · 99 TaskEntry.id · 48 ProposedTask.title ·
    42 TaskOutcome.title · 29 ProposedTask.task_id · 28 _FakeJob.job_id ·
    20 Mission.job_id · 11 _Job.job_id · 7 RemyProject.job_id · 6 PosixPath.job_title

`PosixPath.job_title` is the shape to recognise: a local named `job_dir` or `plan_path` holds
a `Path`, and its `.name` was renamed to `.job_title`. `TaskEntry.id` is the same heuristic
failing from the other side — a receiver the rename SHOULD have reached and did not, because
its name carries no target word. The 551 here and the 517 in section 4 are the same class
read two ways: section 4 splits the `Did you mean:` suffix into its own bucket.

This is not a new discovery. `docs/roadmap/features/T2_F275.md` T002 ALREADY ORDERS the
remedy — the DECISION F272 D7 raising-property probe over every candidate receiver, "giving
the real site set rather than the bound", because `.id` is polymorphic here exactly as
`.status` was. Every dry run of this chain has used the heuristic instead.

**P2 — THE SURVIVING `UUID(...)` COERCIONS, which are the `unsupported operand` and
hexadecimal-UUID classes and are NOT a rename.** The unified record spells a job id as a
16-hex string. `packages/orchestration/timeline.py` normalises with
`jid = job_id if isinstance(job_id, UUID) else UUID(str(job_id))`, which rejects that string,
and `job_dir` in `packages/orchestration/data_paths.py` returns `jobs_dir(root) / job_id`,
joining a `Path` with whatever it is handed — line 200 at `020b1d57`. Of the 368
`unsupported operand` E-lines the traceback attributes 331 to that one line, and of
the 269 hexadecimal-UUID E-lines it attributes 239 to `uuid.py:177`. Resolved by `ast` at
`020b1d57`, over the transform's own file set: `UUID(<job/task argument>)` at 169 sites in 65
files of which 39 are production, `uuid4()` at 637 sites in 144 files of which 34 are
production, and `UUID(<other argument>)` at 49 sites in 21 files of which 14 are production.
No rule of the transform touches a call, so these sites survive the flip verbatim and then
reject the value it produces.

**P3 — THE SPLAT CLASS, unchanged at 867.** Rule I4 of
`.agent/f275_t003_flip_residue.md` section 3. The 881 constructor-keyword E-lines name their
keywords: 778 `JobPlan.name`, 89 `JobPlan.id`, 13 `TaskEntry.acceptance_checks`, 1
`TaskEntry.description`. A keyword arriving through `**defaults` is not a `keyword.arg`, so
no rewrite of `keyword.arg` reaches it; the fix is a call-graph pass over the helper
factories, and `TaskEntry.acceptance_checks` shows those dict literals carry keys the
construction mapping never ruled.

## 6. The instrument, so that this artefact is reproducible from itself

Run from the repository root with `python3 -B`. It resolves every site by `ast` over the
files `git ls-files '*.py'` names, never by grep, and it writes nothing. Its T2 and T3 totals
are the transform's own `T2 job field` and `T3 task field` counts, which is what makes the
heuristic's reach measurable without applying the flip.

<!-- INSTRUMENT -->
```python
"""F275 R50 — the two classes the R46 dry run left undiagnosed, resolved to their sites."""
import ast, collections, subprocess, sys

BASE = sys.argv[1] if len(sys.argv) > 1 else "."
JOB_FIELD, TASK_FIELD = {"id", "name"}, {"id", "description"}
JOBISH, TASKISH = ("job", "plan", "record"), ("task",)
EXCLUDE = {"packages/core/models.py", "packages/orchestration/pingpong_job.py",
           "packages/orchestration/storage.py", "tests/test_storage.py",
           "tests/test_models.py"}
recv_name = lambda n: str(getattr(n, "id", None) or getattr(n, "attr", "") or "")
is_jobish = lambda s: s.lower() in ("j", "stored") or any(t in s.lower() for t in JOBISH)
is_taskish = lambda s: s.lower() in ("t", "tk") or any(t in s.lower() for t in TASKISH)

paths = [p for p in subprocess.run(["git", "ls-files", "*.py"], capture_output=True,
                                   text=True, cwd=BASE).stdout.split() if p]
scanned = [p for p in paths if p not in EXCLUDE]
t2, t3 = collections.Counter(), collections.Counter()
uuid_sites, uuid_files = collections.Counter(), collections.defaultdict(set)
for rel in scanned:
    try:
        tree = ast.parse(open(f"{BASE}/{rel}", "rb").read(), filename=rel)
    except (SyntaxError, OSError):
        continue
    for n in ast.walk(tree):
        if isinstance(n, ast.Attribute):
            recv = recv_name(n.value)
            if n.attr in JOB_FIELD and is_jobish(recv):
                t2[recv] += 1
            elif n.attr in TASK_FIELD and is_taskish(recv):
                t3[recv] += 1
        elif isinstance(n, ast.Call):
            f = n.func
            called = f.id if isinstance(f, ast.Name) else (
                f.attr if isinstance(f, ast.Attribute) else None)
            if called not in ("UUID", "uuid4", "uuid5", "uuid3"):
                continue
            arg = " ".join(ast.dump(a) for a in n.args).lower() if n.args else ""
            key = called if called != "UUID" else (
                "UUID(job/task arg)" if ("job" in arg or "task" in arg) else "UUID(other arg)")
            uuid_sites[key] += 1
            uuid_files[key].add(rel)

print(f"tracked .py: {len(paths)} | scanned after the transform's exclusions: {len(scanned)}")
print(f"D1 T2 JOB-FIELD edits: {sum(t2.values())} over {len(t2)} distinct receiver names")
for r, c in t2.most_common(10):
    print(f"    {c:>5}  {r or '(expr)'}")
print(f"D1 T3 TASK-FIELD edits: {sum(t3.values())} over {len(t3)} distinct receiver names")
for r, c in t3.most_common(10):
    print(f"    {c:>5}  {r or '(expr)'}")
for k, c in uuid_sites.most_common():
    files = uuid_files[k]
    prod = len([f for f in files if not f.startswith("tests/")])
    print(f"D2 {c:>5}  {k:22s} in {len(files)} files, production {prod}")
```

Its recorded output at `020b1d57`, complete and untrimmed:

    tracked .py: 993 | scanned after the transform's exclusions: 989
    D1 T2 JOB-FIELD edits: 1896 over 19 distinct receiver names
         1802  job
           33  j
            6  parent_job
            6  job_one
            6  plan_less
            5  job_node
            5  _Job
            4  job_stub
            4  cli_job
            4  job_two
    D1 T3 TASK-FIELD edits: 532 over 11 distinct receiver names
          272  task
          235  t
            8  fix_task
            6  pending_task
            3  repair_task
            3  task_node
            1  verify_task
            1  real_task
            1  ptask
            1  awaiting_task
    D2   637  uuid4                  in 144 files, production 34
    D2   169  UUID(job/task arg)     in 65 files, production 39
    D2    49  UUID(other arg)        in 21 files, production 14

## 7. What this reading does NOT settle

THE RESIDUE IS CLASSIFIED, NOT EXHAUSTED. The classes in section 4 account for 2035 of the
2387 matched E-lines, and 2387 is itself smaller than 2557 flip-caused failures plus 106
errors, because a failure whose line the pattern did not match is not counted. That remainder
is given NO numeral beyond the two totals, because none was measured.

THE 106 ERRORS ARE NOT DIAGNOSED HERE. They fall in nine files, the largest being
`tests/orchestration/test_mission_e2e.py` at 24,
`tests/orchestration/test_worktree_resume_cli.py` at 16,
`tests/orchestration/test_feature_mission_adapter.py` at 15 and
`tests/ui_server/test_live_state.py` at 15. They are consistent with a fixture raising before
its test body runs, and that reading was not taken, so it is not stated.

WHETHER P1, P2 AND P3 EXHAUST THE PREREQUISITES IS NOT ESTABLISHED. Each is the diagnosed
cause of a class this run MEASURED; nothing here proves a fourth class does not appear once
they are fixed, and the honest test of that is another dry run.
END-ARTEFACT50 ───────────────────────────────────────────────

BEGIN-DEC50 ──────────────────────────────────────────────────

## DECISION F275 D29 (2026-09-11, F275 round 50) — the id-shape migration did exactly what it was performed to do, and the flip still does not converge: three prerequisites, each the diagnosed cause of a measured class

WHAT THIS SETTLES. DECISION F275 D26 ruled the flip NOT the next commit on a dry run at `978046fe` that left 2714 failures, and named the ID SHAPE as its largest unruled class. D27 and D28 migrated that shape. This decision reads the re-run, taken by the reviewer at `020b1d57` and recorded with its instrument in `.agent/f275_t003_flip_residue_r50.md`. The migration succeeded completely and narrowly: the two pydantic classes vanished in full, 369 exception lines to 0, and the whole flipped run now carries two `ValidationError` lines, both against the classic record the flip excludes. It bought 157 failures, not 625, because every other class was never the id shape.

THE MEASUREMENT THIS ROUND ADDS THAT R46 COULD NOT MAKE IS THE CONTROL. R46 reported a total against no baseline. This run takes the unflipped reading at the SAME commit in a second fresh worktree, with the same selection and flags: `1 failed, 18366 passed, 29 skipped` against the flip's `2558 failed, 15703 passed, 29 skipped, 106 errors`. The one control failure is the vitest foundation test, which needs the gitignored `apps/ui/node_modules`, and it is the only node id failing in both. Differencing the node-id sets attributes 2557 failures and all 106 errors TO THE FLIP, with nothing left to guess at.

CHOSEN: THREE PREREQUISITES ARE OWED BEFORE THE FLIP, IN THIS ORDER, AND EACH IS THE DIAGNOSED CAUSE OF A CLASS THAT WAS MEASURED RATHER THAN A SUSPICION. P1, THE FIELD RENAME MUST BE TYPE-RESOLVED. The transform decides `.id`, `.name` and `.description` by whether the RECEIVER'S NAME contains `job`, `plan`, `record` or `task`, never by resolving its TYPE, and that heuristic is the `AttributeError` class: 551 exception lines over 22 receiver-and-attribute pairs, led by 191 `PlannedTask.task_id`, 48 `ProposedTask.title`, 42 `TaskOutcome.title`, 7 `RemyProject.job_id` and 6 `PosixPath.job_title` — every one a receiver whose NAME matched while its TYPE is not `Job` or `Task` — and by 99 `TaskEntry.id`, the same heuristic failing from the other side. `docs/roadmap/features/T2_F275.md` T002 ALREADY ORDERS the remedy, the DECISION F272 D7 raising-property probe over every candidate receiver, and every dry run of this chain has used the heuristic instead. P2, THE SURVIVING `UUID(...)` COERCIONS MOVE, AND THEY ARE NOT A RENAME. The unified record spells a job id as a 16-hex string; `packages/orchestration/timeline.py` normalises with `UUID(str(job_id))`, which rejects it, and `packages/orchestration/data_paths.py` joins a `Path` with whatever it is handed. Resolved by `ast` at `020b1d57`: `UUID(<job/task argument>)` at 169 sites in 65 files of which 39 are production, and `uuid4()` at 637 sites in 144 files of which 34 are production. No rule of the transform touches a call, so these sites survive the flip verbatim and then reject the value it produces. P3, THE `**` SPLAT CLASS, unchanged at 867 and already recorded as rule I4: a keyword arriving through `**defaults` is not a `keyword.arg`, so a call-graph pass over the helper factories is owed, and the 13 `TaskEntry.acceptance_checks` lines show those dict literals carry keys the construction mapping never ruled.

CONSEQUENCE FOR THE PLAN. The flip is no longer the next production commit and is no longer the second step: P1, P2 and P3 precede it, and the dry run is re-run after them, because the honest test of whether three fixes exhaust the prerequisites is another measurement and not this paragraph. P2 is landed the way D28 rules an id widen — one assignment-connected component per commit — since it is the same class of change one level out from the model fields D27 and D28 moved.

ALTERNATIVES CONSIDERED. (i) Flip now and repair the residue inside the flip commit — rejected on arithmetic: 2557 failures cannot be repaired inside a commit whose oversize allowance AGENTS.md grants once per feature, and a flip that lands red is not atomic, it is broken. (ii) Widen the heuristic by adding receiver names until the `AttributeError` class shrinks — rejected because it is the same instrument that produced `PosixPath.job_title`, and because T002 already ordered the type-resolved probe; adding names trades a measurable defect for an unmeasurable one. (iii) Accept the `UUID()` sites as flip-scope and rewrite them inside the transform — rejected because a call rewrite over 169 sites in 39 production files is a second transform with its own residue, and bundling it into the flip makes the one oversize commit carry two unproved mechanisms.

HOW TO REVERSE: delete this decision. D26, D27 and D28 stand either way; what is lost is the control reading and the attribution it makes possible, and the next session would re-derive them from a twenty-minute run apiece.
END-DEC50 ────────────────────────────────────────────────────
