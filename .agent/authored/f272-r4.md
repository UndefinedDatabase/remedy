── STEP T001 (repair) — F272 ──────────────────────────────
Goal:        Clear the last 2 red tests by moving the ONE job-keyed run-log
             path that lives outside `tests/`, land DECISION F272 D2 with a
             repository-wide consequence, and book the two owed gate entries.
Bundle:      C0a save the block · C0b mirror the block · C1 the plan ·
             C2 the two gate entries into the record · C3 the smoke-script
             path fix · C4 DECISION F272 D2 into the feature file ·
             C5 the `Landed:` line and the prose slips · C6 the handback.
Change:      EXACTLY these eight paths and nothing else —
             `.agent/authored/f272-r4.md`, `.agent/last_block.md`,
             `.agent/plan.md`, `.agent/live_review.md`,
             `scripts/remedy_runtime_cli_smoke.py`,
             `docs/roadmap/features/T2_F272.md`, `.agent/prose_slips.md`,
             `.agent/handoff.md`.
Handback:    completion report + rewrite `.agent/handoff.md`.
── end header. Per §3 item 37 every run of a repeated character in this block's
frame states its length: line 1 carries a run of 2 U+2500 then a run of 30, and
this line carries one run of 2. Both readings were measured, not recalled.

## Why this round exists

Round 3 PASSED every gate it could reach and its sweep was re-verified by the
reviewer line for line. It did NOT reach green, because the reviewer's own
completeness gate searched `tests/` and the last job-keyed run-log path lives in
`scripts/`. That is the SAME under-scoping finding R-0818 already registers, so
NO NEW ID IS MINTED — per docs/agents/planner_reviewer_prompt.md §3 item 30 the
evidence joins the open finding, and R-0818's own STANDING RULE paragraph is the
rule this round finally applies to itself.

Round 3's C4 was cut short by the `.agent/STOP` sentinel, so DECISION F272 D2 is
still not on disk. Its draft survives verbatim in `.agent/last_block.md`. It is
NOT reused: the round 3 worker's deviation 5 correctly objected that the draft's
CONSEQUENCE paragraph scopes the gate to "all of `tests/`", which is the very
error the decision corrects. The DECISIOND2 slice below is re-authored with a
repository-wide consequence.

## Readings the reviewer took before writing this block

All at `385d3b16`, in the primary checkout, by the reviewer itself.

1. `git status --porcelain` EMPTY. `.agent/STOP` does not exist.
2. The two node ids of gate G4(ii): EXIT 1, both listed under `FAILED`,
   `2 failed in 2.30s`. This is the RED CONTROL and it is real.
3. The same two node ids in a disposable worktree at `385d3b16` with the ONE
   line of the SMOKEFIX pair applied: EXIT 0, `2 passed in 2.37s`. The whole of
   `tests/cli/` in that same worktree: EXIT 0, 1537 passed; in the unmodified
   primary checkout the same selection is EXIT 1, `2 failed, 1535 passed`. The
   worktree was removed, its branch deleted and `git worktree prune` run.
4. `"runs" /` over every tracked `.py` file in the WHOLE repository, enumerated
   from `git ls-files` in Python and never from a shell glob: 1063 files, SEVEN
   matching lines. Exactly one of them is job-keyed. The other six are the
   survivors G6 names.
5. `python3 -m ruff check scripts/remedy_runtime_cli_smoke.py`: EXIT 0,
   `All checks passed!`. Repo-wide `ruff check .` is EXIT 1 at 26 errors at this
   commit and on `main`; that debt is OPEN finding R-0468 and is deliberately
   NOT gated here, because ordering a gate already red at its base is the
   R-0364 class.
6. `python3 -m pytest tests/docs/ tests/orchestration/test_roadmap_index.py`:
   EXIT 0, 333 passed.
7. `python3 -m apps.cli.grouped integrity check --json`: EXIT 0, `"passed": true`.
8. `.agent/live_review.md` 1066064 bytes, terminal byte exactly one `\n`;
   `.agent/prose_slips.md` 132118 bytes, same; `docs/roadmap/features/T2_F272.md`
   11875 bytes, same. Registrations 302 and resolutions 246 BY DISTINCT ID, open
   set 56, `^Gate: ` 24, `^Gate: F272 R2 ` 0, `^Gate: F272 R3 ` 0,
   `^Landed: R-0818` 0.
9. In `scripts/remedy_runtime_cli_smoke.py`: the SMOKEFIX FROM occurs exactly 1x
   and the token `job_logs` occurs 0x.

## Constraints

1. NO SLICE IS EDITED. Apply every authored text byte for byte between its
   markers. If a slice looks wrong, apply it anyway and say so in the handback.
2. The eight paths of the Change line are the whole change set. Touch nothing
   else. If a fix seems to need a ninth path, REPORT it rather than editing it.
3. Commit order is C0a, C0b, C1, C2, C3, C4, C5, C6 with nothing reordered.
   C1 is the first substantive commit (§3 item 23); only the two block-save
   commits precede it.
4. APPEND CONVENTION, identical for all three appended files: the post-image is
   the pre-image, then one `\n`, then the slice bytes, then one `\n`. The slice
   bytes are the lines BETWEEN the two marker lines, each including its own
   terminating newline, with no leading and no trailing blank line.
5. PLAN CONVENTION, different on purpose: `.agent/plan.md` is REPLACED by
   exactly the PLANF272R4 slice bytes as defined in constraint 4, and by
   nothing else. Do not add a trailing newline beyond the ones the slice
   already carries.
6. The SMOKEFIX pair is a REWRITE. The containment test's own output is
   `TO contains FROM: false`, so the §4.9 REWRITE proof applies and the
   FROM-zero count is ordered. Change that one line and nothing else in that
   file — no import, no comment, no reflow.
7. Mint NO finding id. Write NO `Done:` paragraph — `Done:` is reserved for
   reviewer-authored text (§4 item 4). The `Landed:` line at C5 is the only
   resolution-shaped text this round writes.
8. Destructive verification, if you run any, goes in a disposable `git worktree`
   under the gitignored `.remedy-wt/` and never in the primary checkout
   (self_drive_protocol.md G5). Remove and prune it before the handback.
9. Read `.agent/STOP` with `os.path.exists` three times — before C0a, before C3
   and before C6 — and table all three readings. If it appears, finish only the
   half-written commit, then hand off (G6).
10. `python3 -B` for any run where a stale `__pycache__` could shadow a change.
11. Report each gate's REAL exit code. "Green" as a word is a finding (G4).

## Gate list — DONE WHEN

**G1 TRANSPORT.** sha256 and byte length of the committed
`.agent/authored/f272-r4.md` and of `.agent/last_block.md`. Both equal each
other and both equal the BLOCK_SHA and length the delegation named. Per §3
item 37 this chain covers the saved copy and its mirror and is NOT a claim
about the bytes emitted into your prompt; say so.

**G2 THE RECORD, at C2 and at C5, four readers each.**
(a) BYTE. Pre and post lengths; pre is a byte-exact prefix of post;
`post == pre + b"\n" + slice + b"\n"`; pre's terminal byte asserted to be
exactly one `\n` BEFORE writing; post ends in exactly one `\n`.
(b) STRUCTURAL, computed independently of (a) by splitting the WHOLE image on
`\n{2,}`: units before, units after, delta. N is COUNTED BY YOUR SCRIPT from
the slice's own paragraphs and is never a number this block asserts. The last N
units must equal the slice's N paragraphs IN ORDER, and the units before must be
an unchanged prefix.
(c) NEGATIVE CONTROL, in memory on a `bytes` object, never on disk. Flip one
byte inside the FIRST appended paragraph — assert the offset lies inside it
before flipping — and require reader (a) and reader (b) to BOTH reject. Restore,
require both to accept, and require the restored image to equal the disk image.
(d) COUNTS, before C2 → after C5: distinct `^- R-\d{4} — ` ids 302 → 302;
distinct `^Done: R-\d{4} — ` ids 246 → 246; open set BY DISTINCT ID 56 → 56;
`^Gate: ` 24 → 26; `^Gate: F272 R2 ` 0 → 1; `^Gate: F272 R3 ` 0 → 1;
`^Landed: R-0818` 0 → 1; `^Done:` lines inside either appended region 0.
`.agent/prose_slips.md` gets readers (a) and (b) only.

**G3 THE PLAN, at C1.** `.agent/plan.md` equals the PLANF272R4 slice bytes
exactly — report the equality and both byte lengths. Line count, which must be
under the AGENTS.md cap of 50. `## Goal` present and `## Next Steps` present.

**G4 THE CODE, at C3 — the pair and the colour.**
(i) In `scripts/remedy_runtime_cli_smoke.py`: FROM occurs 1x at C2 and 0x at C3;
TO occurs 0x at C2 and 1x at C3. `git diff --numstat C2 C3` is exactly one row,
`1 1 scripts/remedy_runtime_cli_smoke.py`, and `git diff --name-only` over C3
lists that one path and nothing else.
(ii) THE COLOUR PAIR, both readings in the primary checkout, no mutation needed
because the file itself changes between them. Command, both times:
`python3 -B -m pytest tests/cli/test_propose_cli_runtime.py::TestProposeRuntimeSmoke::test_propose_flow tests/cli/test_worker_cli_runtime.py::TestWorkerRuntimeSmoke::test_worker_flow -q -p no:randomly`
At C2 it must be EXIT 1 with both node ids listed under `FAILED`. At C3 it must
be EXIT 0. Report both exit codes and both summary lines verbatim.
(iii) `python3 -B -m pytest tests/cli/ -q -p no:randomly` at C3: EXIT 0. Report
the exit code and the passed count you measured; this block states no count for
it on purpose.

**G5 THE FEATURE FILE, at C4.** Reader (a) of G2 over
`docs/roadmap/features/T2_F272.md`. Then `^### DECISION F272 D2` exactly 1,
`^### DECISION F272 D1` still exactly 1, `^## DECISIONs` exactly 1. Then
`python3 -m pytest tests/docs/ tests/orchestration/test_roadmap_index.py -q -p no:randomly`:
EXIT 0. The reviewer's base reading at `385d3b16` was EXIT 0 at 333 passed.

**G6 THE JOB-KEYED SPELLING IS ZERO REPOSITORY-WIDE, at C3.** This is R-0818's
own standing rule applied to itself, so the search is stated and it is wide.
Enumerate every tracked file whose name ends `.py` from `git ls-files` IN PYTHON
— never a shell glob, because `tests/**/*.py` does not match
`tests/test_data_paths.py` — and PRINT IN FULL every line containing the
substring `"runs" /`. The result must be EXACTLY these six lines and no seventh:

    tests/orchestration/test_context_compiler.py:1451
    tests/orchestration/test_failure_postmortem.py:412
    tests/orchestration/test_failure_wiring.py:903
    tests/orchestration/test_gauntlet_runner.py:490
    tests/test_data_paths.py:396
    tests/test_data_paths.py:430

Each of the six is run-keyed, names a fixed filename, or is the assertion that
pins `run_dir`'s own layout; none is keyed by a JOB id. Also report `job_logs`
occurring exactly 1x in `scripts/remedy_runtime_cli_smoke.py`. Non-`.py` matches
are prose quotations in `.agent/` and `docs/` and are deliberately out of scope;
say so rather than counting them.

**G7 LINT AND INTEGRITY, at C3 and C4.**
`python3 -m ruff check scripts/remedy_runtime_cli_smoke.py`: EXIT 0. The
reviewer measured `All checks passed!` at `385d3b16`, so this gate is meetable.
`python3 -m apps.cli.grouped integrity check --json`: EXIT 0 with
`"passed": true` and `"fail_count": 0`. A repo-wide `ruff check .` is NOT
ordered: it is EXIT 1 at 26 errors at the base and on `main`, and that debt is
OPEN finding R-0468.

**G8 THE TREE.** `git status --porcelain` EMPTY when C6 is staged.
`git ls-files .remedy-wt` EMPTY. `git worktree list` naming any worktree you
created and confirming its removal. Per commit for C0a through C5 — NOT C6,
which cannot count its own insertions (§3 item 14) — the insertion count from
`git diff --numstat <parent> <commit>`, each under the DECISION F104 D1 cap of
500, each single-parent. Marker sweep: zero lines beginning `<<<BEGIN ` or
`<<<END ` in each of the six written non-block files. The three `.agent/STOP`
readings of constraint 9, as a table.

## The slices

<<<BEGIN PLANF272R4>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 PASSED. Round 2 FAILED
its gate: its production change was right, but DECISION F272 D1 sized the change
set from a three-file search and 24 test files observed the move. Round 3 swept
those 24 and took the tip from 207 failures to 2. Round 4 clears the last 2.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the plural
run list and the run re-key, T002 the rest of the unified record, T003 the
eleven consumers, T004 the classic runner, T005 the reachability test and the
cluster deletion, which is never split.

## Current Step

Round 4 finishes T001's re-key. It books the round 2 and round 3 verdicts, moves
the ONE job-keyed run-log path that lives outside `tests/` —
`scripts/remedy_runtime_cli_smoke.py`, which both CLI runtime smoke tests shell
out to — and lands DECISION F272 D2, whose consequence is stated over the whole
repository rather than over `tests/`, because scoping it to `tests/` is the
error D2 exists to correct. No finding id is minted: the second instance belongs
to R-0818, which stays open until its fix is reviewed.

## Next Steps

1. The name collapse DECISION F272 D1 places next: `pingpong_runs_dir` and
   `pingpong_run_dir` are DELETED in favour of `runs_dir` and `run_dir` at every
   call site, with no alias and no attic, per AGENTS.md "Replacing is deleting".
   Measured at `385d3b16`: about 170 sites across roughly 35 files, so it is
   split by module group across several commits.
2. The rest of the unified record: the eleven administrative fields and the
   Mission extension (T002).
3. The eleven consumers named under Design in `T2_F260.md`, one per commit where
   the diff allows (T003).

## Risks

- The name collapse is a pure rename: `pingpong_run_dir` and `run_dir` return
  the same path today, which `tests/test_data_paths.py` pins. A rename that
  large still needs a red-proof pair rather than a mutation, because moving one
  accessor moves reader and writer in lockstep and no observer can see it.
<<<END PLANF272R4>>>

<<<BEGIN RECORDGATES>>>
Gate: F272 R2 — the F272 round 2 entry, BOOKED LATE. VERDICT FAIL, and the failure is the reviewer's and not the worker's. Range `5a93878c`..`b189a03f`, seven commits, every one single-parent, in the bundle's ordered sequence, insertion counts 379, 322, 20, 2, 62, 67 and 383 read by the reviewer from `git diff --numstat <parent> <commit>` at `385d3b16`, every one under the AGENTS.md DECISION F104 D1 cap of 500. THE PRODUCTION CHANGE AT `1d24b4a7` IS CORRECT AND WAS NOT REVERTED: `data_paths.run_log_dir` moved the job-keyed run log to `<data_root>/job_logs/<job_id>/` and the ping-pong run store arrived at `<data_root>/runs/<run_id>/`, one function body each, and the reviewer confirms at `385d3b16` that `job_logs_dir` returns `<root>/job_logs` and `run_log_dir` returns `job_logs_dir(root) / str(job_id)`. THE ROUND FAILED ON ITS OWN TIP COLOUR. DECISION F272 D1, committed at `43d91cda`, asserted that "the only code that observes the change is the three test files that hand-spell the layout"; 24 test files did, the tip went red at 207 tests and the canary fell from 42 passed to 41 passed and 1 failed. That sentence is the whole of the failure, it was written by the reviewer from a three-file grep, and it is registered as finding R-0818. THE WORKER BEHAVED CORRECTLY THROUGHOUT: it applied the block as written, measured the red itself, attributed it by demonstration in a worktree rather than by assumption, declined to widen the sweep on its own authority under self_drive_protocol.md G8, declined to revert so the reviewer could reproduce the numbers, and reported all of it. This entry is written in round 4 rather than in round 3 because operator amendment amend0827-process-diet rule 1 makes the pushed handoff the durable carrier and forbids a round whose whole change set is bookkeeping; round 3's own change set was the repair sweep and carried no room for it, which is a scheduling fact and not an excuse — the verdict existed on disk in `.agent/handoff.md` at `b189a03f` throughout.

Gate: F272 R3 — the F272 round 3 entry. VERDICT FAIL ON THE TIP COLOUR, AND EVERY GATE THE ROUND COULD REACH IS GREEN AND WAS RE-RUN BY THE REVIEWER ITSELF. Range `b189a03f`..`9ed39cea`, six commits, every one single-parent, in the bundle's ordered sequence C0a, C0b, C1, C2, C3 and then the handback, with C4 dropped; insertion counts 355, 279, 23, 2, 61 and 305. The verdict is FAIL for one reason only, and it is the reviewer's again: `python3 -m pytest` over the 25-file observer set is EXIT 1 at `2 failed, 1123 passed`, re-measured by the reviewer at `385d3b16`, and this repository does not certify a red tip however blameless the round. Against `b189a03f`'s 207 failures over the same observers that is 205 failures removed. THE SWEEP IS CORRECT LINE FOR LINE. The reviewer read the whole of `git diff 20737a16 aaa55053`: 24 files, +61/-61, 56 job-keyed path components moved from `"runs"` to `"job_logs"` and 5 prose lines corrected beside them, and every one of the 56 is keyed by a JOB id — `job.id`, `job_id`, `job.job_id`, `jid`, `str(job.id)` or `str(job_id)` — with no run-keyed or filename-keyed site touched. The survivor inventory reproduces exactly: `"runs" /` over all of `tests/` returns the same six non-job-keyed lines the handback enumerated, no seventh. TRANSPORT: `.agent/authored/f272-r3.md` and `.agent/last_block.md` are both 24241 bytes and both hash to `428de848e99a4e2cc45e3b9fa6dab16936949819a634c6e17ccceba0280e4fea`, recomputed by the reviewer and equal to the digest the delegation carried; per §3 item 37 that covers the saved copy and its mirror and claims nothing about the emitted bytes. THE PLAN at `c778a8b7`: `.agent/plan.md` is 2098 bytes, 43 lines against the cap of 50, carries `## Goal` and `## Next Steps`, and the reviewer extracted the PLANF272R3 slice from the committed authored original by exact-position marker matching and found the file byte-equal to it. THE RECORD at `20737a16`: `.agent/live_review.md` gained exactly the R-0818 paragraph and nothing else, +2/-0, with no id resolved and no `Gate:` paragraph disturbed. THE CANARY `tests/cli/test_golden_path.py` is EXIT 0 at 42 passed, round 1's reading, re-run by the reviewer. `python3 -m apps.cli.grouped integrity check --json` is EXIT 0 with `"passed": true` and `"fail_count": 0`. THE TWO SURVIVING FAILURES ARE A SECOND INSTANCE OF R-0818 AND SPEND NO NEW ID, per §3 item 30. They are `tests/cli/test_propose_cli_runtime.py::TestProposeRuntimeSmoke::test_propose_flow` and `tests/cli/test_worker_cli_runtime.py::TestWorkerRuntimeSmoke::test_worker_flow`, and the block's explanation of them was factually wrong: it said both reach the path through `tests/cli/runtime_helpers.py`, and neither imports it — both `subprocess`-launch `scripts/remedy_runtime_cli_smoke.py`, which hand-spells `root / "runs" / jid` at line 168. Because that file is outside `tests/`, the block's own completeness gate could not see it, which is precisely the under-scoped search R-0818 registers, arriving a second time inside the round that was repairing the first. The reviewer confirmed the attribution in its own disposable worktree at `385d3b16`: with that one line changed to `root / "job_logs" / jid` the two node ids go from EXIT 1 at `2 failed` to EXIT 0 at `2 passed`, and the whole of `tests/cli/` goes from EXIT 1 at `2 failed, 1535 passed` to EXIT 0 at 1537 passed; the worktree was removed and pruned. THE WORKER WAS RIGHT NOT TO TOUCH IT — the block ordered it reported rather than edited, and self_drive_protocol.md G8 forbids widening scope to route around a block. R-0818's fix is therefore WIDENED here rather than duplicated: the job-keyed spelling is counted to zero over every tracked `.py` file in the WHOLE REPOSITORY, not over `tests/`, and round 4 both performs that count and lands the one-line move it demands. TEN DEVIATIONS WERE DECLARED AND ALL TEN ARE UPHELD, including the two that are the reviewer's own and are recorded here rather than charged to the round: the block's false sentence about `runtime_helpers.py`, and its lint gate, which listed `tests/test_project_context_coverage.py` while that file carries two pre-existing `F401`s present at `b18fad57` on `main` and inside the 26-error repository-wide baseline that OPEN finding R-0468 already holds — a gate red at its own base, which is the R-0364 class and which R-0364's standing rule exists to prevent. Round 3's C4 was not executed because `.agent/STOP` appeared mid-round; G6 permits finishing only the half-written commit, the worker finished C3 and stopped, and DECISION F272 D2 is carried into round 4 with the CONSEQUENCE paragraph re-authored, exactly as the worker's deviation 5 objected it must be.
<<<END RECORDGATES>>>

<<<BEGIN SMOKEFIX_FROM>>>
    runs_dir = root / "runs" / jid
<<<END SMOKEFIX_FROM>>>

<<<BEGIN SMOKEFIX_TO>>>
    runs_dir = root / "job_logs" / jid
<<<END SMOKEFIX_TO>>>

<<<BEGIN DECISIOND2>>>
### DECISION F272 D2 (2026-09-06, F272 round 4) — correction to D1's premise: the observer set is the repository, not the three files the search read
DECISION F272 D1 is CORRECT IN ITS RULING and is not withdrawn: the run log keeps
its job key, the two directories move one function body each, the name collapse
follows in its own round, and the merge of the log into the per-run directory
stays deferred to T003. This decision corrects one FALSE SENTENCE in it, by
appending rather than by rewriting, which is how this repository corrects a
landed decision — the precedent is "DECISION F085 D6 — correction to the ruled
figure" in `.agent/decisions.md`.

THE FALSE SENTENCE. D1 says "the only code that observes the change is the three
test files that hand-spell the layout". Measured at `b189a03f`, after D1's move
had landed: `python3 -m pytest -n auto -q -p no:randomly` gives 207 failed,
19528 passed, 23 skipped, across 24 test files, and the job-keyed run-log
directory is hand-spelled at 56 lines in those 24 files. The three files D1
named are the three `docs/roadmap/features/T2_F272.md` T001 happens to list;
they are the files the reviewer searched, not the files that exist. Registered
as finding R-0818.

WHAT REMAINS TRUE, re-verified at `385d3b16`: no production caller moved. All 74
`timeline.load_run_events` readers and 35 `run_log.RunLogWriter` writers resolve
through `data_paths.run_log_dir`, and `run_log_dir` returns
`job_logs_dir(root) / str(job_id)` while `runs_dir` returns `<root>/runs`, which
is exactly the layout D1 rules. The staging D1 chose is therefore the right
staging; only its estimate of the observer set was wrong, and an estimate is
what it should never have been.

CONSEQUENCE, STATED OVER THE REPOSITORY AND NOT OVER `tests/`. The test-side
spelling sweep that this file's T001 inherits from DECISION F260 D6 is larger
than that file's own sentence suggests, and it is performed in full across
rounds 3 and 4: 24 files under `tests/` in round 3, and in round 4 the one
remaining job-keyed site, `scripts/remedy_runtime_cli_smoke.py`, which both CLI
runtime smoke tests shell out to and which no search of `tests/` can reach. Each
site was read before it was changed, because `"runs"` remains the correct
spelling of the RUN store that round 2 moved INTO `<data_root>/runs/<run_id>/`.
THE GATE IS THE JOB-KEYED SPELLING COUNTED TO ZERO OVER EVERY TRACKED `.py` FILE
IN THE WHOLE REPOSITORY — enumerated from `git ls-files`, never from a shell
glob — and never the word counted anywhere. Scoping that count to `tests/` is
the error this decision exists to correct, and round 3 reproduced it one round
after registering it, which is why the scope is written into the ruling rather
than left to the next block to remember.

REVERSE by deleting this section, at which point D1's premise sentence stands
uncorrected while the sweep it under-counted remains on disk.
<<<END DECISIOND2>>>

<<<BEGIN LANDED818>>>
Landed: R-0818 — the second instance is fixed. `scripts/remedy_runtime_cli_smoke.py` line 168 now spells the job-keyed run log `root / "job_logs" / jid`, committed at C3 of F272 round 4, and the two CLI runtime smoke tests that shell out to it go from EXIT 1 to EXIT 0. The completeness count is now taken over every tracked `.py` file in the whole repository rather than over `tests/`, which is the widened form of this finding's own standing rule; DECISION F272 D2 writes that scope into the ruling. Awaiting the reviewer's `Done:` text.
<<<END LANDED818>>>

<<<BEGIN SLIPS>>>
2026-09-06 · F272 R3 block (reviewer) · The block explained the two CLI runtime smoke tests as reaching the run-log path through `tests/cli/runtime_helpers.py`; neither file imports it, both shell out to `scripts/remedy_runtime_cli_smoke.py`, and the worker measured and declared the error. Nothing on disk was wrong because of it — the block ordered those two files reported rather than edited — so it spends no id.

2026-09-06 · F272 R3 block (reviewer) · The block's lint gate listed `tests/test_project_context_coverage.py`, which carries two pre-existing `F401`s present on `main` at `b18fad57` and counted inside the 26-error repository-wide baseline that OPEN finding R-0468 already holds, so the gate was unmeetable at every commit on the branch and at its own base. That is the R-0364 class and R-0364's standing rule already forbids it; the worker declined to remove two unrelated imports and was right to.

2026-09-06 · F272 R3 handback (worker) · The handback reported the PLANF272R3 slice at 2097 bytes "plus exactly one trailing newline" while the reviewer's own marker extraction gives the slice at 2098 bytes including its terminal newline and the plan byte-equal to it. Both readings describe the same 2098 bytes on disk and differ only in which side of the marker the final newline is attributed to; the load-bearing property, that the plan is exactly the slice, holds under either.
<<<END SLIPS>>>

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, `SESSION 2 of feature F272 · round 4`, the one-sentence context
self-assessment amend0905-throughput requires, branch, the range, a per-commit
changed-files table with real `+/-` from `git diff --numstat`, the item-status
table covering C0a through C6 with every item present exactly once, one line per
gate G1 to G8 with its real exit code, the authored-text proof table, deviations
and assumptions, and the next expected action. There is no length cap.
