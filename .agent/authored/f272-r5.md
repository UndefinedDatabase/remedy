── STEP T001 (move two, production half) — F272 ──────────
Goal:        Move every PRODUCTION caller off `pingpong_run_dir` and
             `pingpong_runs_dir` onto `run_dir` and `runs_dir`, choosing the
             call shape by whether the caller's own scope binds a local of
             that name. The two functions are NOT deleted this round.
Bundle:      C0a save the block · C0b mirror the block · C1 the plan ·
             C2 the record: `Done: R-0818`, the round 4 gate entry and the
             prose slips · C3 DECISION F272 D3 into the feature file ·
             C4 `pingpong_loop.py` · C5 `job_evidence.py` · C6 the five
             remaining production files · C7 the handback.
Change:      EXACTLY these fourteen paths and nothing else —
             `.agent/authored/f272-r5.md`, `.agent/last_block.md`,
             `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/prose_slips.md`, `docs/roadmap/features/T2_F272.md`,
             `packages/orchestration/pingpong_loop.py`,
             `packages/orchestration/job_evidence.py`,
             `packages/orchestration/pingpong_promote.py`,
             `packages/orchestration/worktree_resume.py`,
             `packages/orchestration/pingpong_evidence.py`,
             `packages/orchestration/repair_attest.py`,
             `apps/cli/commands/do_cmd.py`, `.agent/handoff.md`.
Handback:    completion report + rewrite `.agent/handoff.md`.
── end header. Per §3 item 37 every run of a repeated character in this block's
frame states its length: line 1 carries a run of 2 U+2500 then a run of 10, and
this line carries one run of 2. Both readings were measured, not recalled.

## What this round is, and what it is not

DECISION F272 D1's "move two" deletes `pingpong_runs_dir` and `pingpong_run_dir`
in favour of `runs_dir` and `run_dir` at every call site — no alias, no attic,
per AGENTS.md "Replacing is deleting". Measured by the reviewer at `78457a98`
over every tracked `.py` file, that is 178 occurrences in 34 files, split 41
production / 132 test / 5 inside `data_paths.py` itself.

THIS ROUND MOVES THE PRODUCTION HALF ONLY, and the two functions stay on disk.
Round 6 moves the 132 test-side occurrences and deletes the two bodies in its
last commit. The split is deliberate: the production half is a SPLIT round by
the §3 Round-types rule and carries a real mutation red-proof, while the test
half is a mechanical sweep whose proof is the suite. Landing both in one round
would put the deletion in the same commit range as a 34-file rename and leave no
reviewable diff for either.

DO NOT delete `pingpong_runs_dir` or `pingpong_run_dir` this round. DO NOT touch
any file under `tests/`. Both are round 6's, and gate G5 measures that they are
still present and still correct.

## The two call shapes, and how to choose between them

A plain token swap is WRONG at 7 of this round's 41 sites, and in
`pingpong_loop.py` it does not merely read badly — it raises. Those sites assign
`run_dir = pingpong_run_dir(...)`, so after a token swap the name `run_dir` is
bound locally in that function and the call on the right-hand side resolves to
the local rather than to the import, which is `UnboundLocalError` at runtime.

**SHAPE A — the plain token swap.** Use it wherever the enclosing scope does NOT
bind a local named `run_dir` or `runs_dir`. Replace `pingpong_run_dir` with
`run_dir` and `pingpong_runs_dir` with `runs_dir`, in the import line and at the
call, and change nothing else on those lines.

**SHAPE B — reach the function through its module.** Use it at every site whose
enclosing scope DOES bind such a local. Import
`from packages.orchestration import data_paths` and call `data_paths.run_dir(...)`
or `data_paths.runs_dir(...)`. THE LOCAL VARIABLE KEEPS ITS NAME. Do not rename
it: AGENTS.md forbids mass renames as their own activity. Do not write
`import run_dir as _run_dir` or any other alias: AGENTS.md's discoverability
section forbids local rename-imports of a core concept.

`packages/orchestration/pingpong_loop.py` takes SHAPE B AT ALL THIRTEEN OF ITS
SITES, not only at its four shadowing ones, so that one file has one shape. Its
module-level `from packages.orchestration.data_paths import (...)` block loses
`pingpong_run_dir` and `pingpong_runs_dir` and keeps `mint_run_id`; the module
import is added beside it. The reviewer confirmed at `78457a98` that neither
`pingpong_loop.py` nor `job_evidence.py` already imports `data_paths` as a
module, so the import you add is new in both.

THE SEVEN SHADOWING SITES, read by the reviewer at `78457a98` and enumerated
rather than described, so you can check your own coverage:

    packages/orchestration/job_evidence.py:2432
    packages/orchestration/job_evidence.py:2715
    packages/orchestration/pingpong_loop.py:2017
    packages/orchestration/pingpong_loop.py:2759
    packages/orchestration/pingpong_loop.py:4076
    packages/orchestration/pingpong_loop.py:4236
    packages/orchestration/pingpong_promote.py:400

Line numbers move as you edit; resolve each by its assignment text
`run_dir = pingpong_run_dir(`, not by the number. Determine the shape for EVERY
site by reading its enclosing scope yourself — the list above is the reviewer's
reading and a cross-check, never a substitute for yours. If you find an eighth,
apply SHAPE B to it and say so in the handback.

## The per-file site counts the reviewer measured at `78457a98`

`pingpong_loop.py` 13 · `job_evidence.py` 14 · `pingpong_promote.py` 4 ·
`worktree_resume.py` 4 · `pingpong_evidence.py` 2 · `repair_attest.py` 2 ·
`do_cmd.py` 2. Total 41. Report your own count per file beside each; where yours
differs from the reviewer's, yours is the measurement and the difference is a
declared deviation.

One site is worth naming because it looks like an alias and is not:
`worktree_resume.py:78` defines `def _run_dir(run_id)` whose whole body returns
`pingpong_run_dir(run_id)`. Under SHAPE A it becomes a one-line wrapper around
`run_dir`. The wrapper has other callers in that file, so it is NOT deleted here
and its name does not collide with the imported one. Leave it a wrapper.

## Constraints

1. NO SLICE IS EDITED. Apply every authored text byte for byte between its
   markers. If a slice looks wrong, apply it anyway and say so in the handback.
2. The fourteen paths of the Change line are the whole change set. Nothing under
   `tests/`, and no ninth production file. If a change seems to need one, REPORT
   it rather than making it.
3. Commit order is C0a, C0b, C1, C2, C3, C4, C5, C6, C7, nothing reordered.
   C1 is the first substantive commit (§3 item 23); only the block-save commits
   precede it.
4. APPEND CONVENTION for `.agent/live_review.md`, `.agent/prose_slips.md` and
   `docs/roadmap/features/T2_F272.md`: `post == pre + b"\n" + slice`, where the
   slice is the lines between the markers each carrying its own terminating
   newline, and the post-image ends in exactly one `\n`. This is round 4's
   measured on-disk convention and it supersedes the trailing-`\n` wording round
   4's block carried, which the round 4 worker correctly showed to be
   self-contradictory.
5. PLAN CONVENTION: `.agent/plan.md` is REPLACED by exactly the PLANF272R5 slice
   bytes and nothing else.
6. The only behaviour permitted to change this round is NONE. Every edit is a
   rename or a re-route of the same call to the same function body. If any edit
   would change what a function returns, stop and report.
7. Mint NO finding id. The `Done: R-0818` slice is reviewer-authored and is the
   only resolution text; write no `Done:` paragraph of your own.
8. Destructive verification goes in a disposable `git worktree` under the
   gitignored `.remedy-wt/`, never in the primary checkout (G5). Remove and
   prune it before the handback.
9. Read `.agent/STOP` with `os.path.exists` three times — before C0a, before C4
   and before C7 — and table all three. If it appears, finish only the
   half-written commit, then hand off (G6).
10. `python3 -B` for every run, and purge `__pycache__` inside any worktree
    before a mutation run.
11. Report each gate's REAL exit code. "Green" as a word is a finding (G4).

## Gate list — DONE WHEN

**G1 TRANSPORT.** sha256 and byte length of the committed
`.agent/authored/f272-r5.md` and `.agent/last_block.md`; both equal each other
and the BLOCK_SHA and length the delegation named. Per §3 item 37 this covers
the saved copy and its mirror and is NOT a claim about the bytes emitted into
your prompt; say so.

**G2 THE RECORD, at C2.** Four readers over `.agent/live_review.md`, and readers
(a) and (b) over `.agent/prose_slips.md`.
(a) BYTE: pre and post lengths; pre a byte-exact prefix; `post == pre + b"\n" +
slice`; pre's terminal byte asserted to be exactly one `\n` BEFORE writing; post
ends in exactly one `\n`.
(b) STRUCTURAL, computed independently of (a) by splitting the WHOLE image on
`\n{2,}`: units before, after, delta, with N COUNTED BY YOUR SCRIPT from the
slice's own paragraphs and never taken from this block. Last N units equal the
slice's paragraphs IN ORDER; the units before are an unchanged prefix.
(c) NEGATIVE CONTROL, in memory on a `bytes` object, never on disk: flip one
byte inside the FIRST appended paragraph, asserting the offset lies inside it
before flipping, and require readers (a) and (b) to BOTH reject; restore and
require both to accept and the restored image to equal the disk image.
(d) COUNTS, before C2 → after C2: distinct `^- R-\d{4} — ` ids 302 → 302;
distinct `^Done: R-\d{4} — ` ids 246 → 247; open set BY DISTINCT ID 56 → 55;
`^Done: R-0818 — ` 0 → 1; `^Landed: R-0818` 1 → 1 — THE `Landed:` LINE IS NOT
DELETED, because the record is append-only and the `Done:` paragraph is what
supersedes it; `^Gate: ` 26 → 27; `^Gate: F272 R4 ` 0 → 1.

**G3 THE PLAN, at C1.** `.agent/plan.md` equals the PLANF272R5 slice bytes
exactly; report the equality and both byte lengths. Line count under the
AGENTS.md cap of 50. `## Goal` and `## Next Steps` both present.

**G4 THE FEATURE FILE, at C3.** Reader (a) of G2 over
`docs/roadmap/features/T2_F272.md`, then `^### DECISION F272 D3` exactly 1,
`^### DECISION F272 D2` still exactly 1, `^### DECISION F272 D1` still exactly 1.
Then `python3 -m pytest tests/docs/ tests/orchestration/test_roadmap_index.py -q -p no:randomly`:
EXIT 0. The reviewer's base reading at `78457a98` was EXIT 0 at 333 passed.

**G5 THE PRODUCTION SWEEP IS COMPLETE AND SCOPED, at C6.** Enumerate every
tracked `.py` file from `git ls-files` IN PYTHON — never a shell glob, because
`tests/**/*.py` does not match `tests/test_data_paths.py`.
(i) `\bpingpong_runs?_dir\b` occurs ZERO times in every tracked `.py` file under
`packages/` and `apps/` EXCEPT `packages/orchestration/data_paths.py`, where it
must still occur exactly 5 times — the two defs, the two module-docstring lines
and the one internal call. Print any non-zero file with its lines.
(ii) The test side is UNTOUCHED: `\bpingpong_runs?_dir\b` still occurs 132 times
under `tests/`, and `git diff --name-only` over the whole round lists no path
beginning `tests/`.
(iii) NO SHADOW SURVIVES: no line in the seven changed code files matches
`^\s*(run_dir|runs_dir)\s*=\s*(run_dir|runs_dir)\s*\(`. Print the count, which
must be 0.
(iv) Report, per changed file, how many sites you moved and under which shape,
and the total, against the reviewer's 41.

**G6 THE MUTATION RED-PROOF, with its control, in a disposable worktree at C6.**
A pure rename cannot be proved by mutating the accessor — moving one body moves
reader and writer in lockstep and no observer can see it, which is the defect
the F260 R12 gate entry records. The proof here is a BEFORE/AFTER pair over a
selection that cannot mention the old name, and the reviewer has already
measured the BEFORE half.

SELECTION RULE, recomputed by your script and never hard-coded: every
`tests/**/test_*.py` whose own source contains ZERO matches of
`\bpingpong_runs?_dir\b` AND names at least one of `pingpong_loop`,
`job_evidence`, `pingpong_promote`, `worktree_resume`, `pingpong_evidence`,
`repair_attest`. The reviewer measured 88 files at `78457a98`; report your own
number.

MUTATION: in the worktree only, replace the BODY of `data_paths.pingpong_run_dir`
— the single line `    return pingpong_runs_dir(root) / run_id`, which the
reviewer counted exactly 1x in that file at `78457a98` — with
`    raise AssertionError("R5 PROBE: a caller still reaches pingpong_run_dir")`.

REQUIRED READINGS, both from the same worktree, `python3 -B`, `__pycache__`
purged first:
- UNMUTATED CONTROL over the selection: EXIT 0. At `78457a98` the reviewer
  measured EXIT 0 at 3562 passed, so a non-zero control means your worktree is
  broken, not that the round is.
- MUTATED over the same selection: EXIT 0, with ZERO failures and ZERO errors.
  At `78457a98` the reviewer measured EXIT 1 at `330 failed, 3215 passed,
  17 errors`, which is the control proving production really reached that
  function. Any failure that survives at C6 NAMES a production caller this round
  missed; report its node id and its file rather than adjusting the selection.
Restore the mutated file, confirm the worktree diff is empty, remove and prune.

**G7 LINT AND INTEGRITY, at C6.** `python3 -m ruff check` over exactly the seven
changed code files in ONE invocation: EXIT 0. The reviewer measured
`All checks passed!` over all seven at `78457a98`, so the gate is meetable and a
red reading is this round's own. A repo-wide `ruff check .` is NOT ordered: it is
EXIT 1 at 26 errors at the base and on `main` under OPEN finding R-0468.
`python3 -m apps.cli.grouped integrity check --json`: EXIT 0, `"passed": true`,
`"fail_count": 0`.

**G8 THE TREE.** `git status --porcelain` EMPTY when C7 is staged.
`git ls-files .remedy-wt` EMPTY. `git worktree list` naming the worktree you
created for G6 and confirming its removal; the twelve pre-existing
`remedy/job-*` entries predate this round and stay. Per commit for C0a through
C6 — NOT C7, which cannot count its own insertions (§3 item 14) — the insertion
count from `git diff --numstat <parent> <commit>`, each under the DECISION F104
D1 cap of 500, each single-parent. Marker sweep: zero lines beginning
`<<<BEGIN ` or `<<<END ` in each of the twelve written non-block files. The
three `.agent/STOP` readings of constraint 9, as a table.

## The slices

<<<BEGIN PLANF272R5>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1, 3 and 4 PASSED; round 2
FAILED on a premise DECISION F272 D2 has now corrected. The run re-key is
finished and the tip is green: the 25-file observer set is 1125 passed.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the plural
run list and the run re-key, T002 the rest of the unified record, T003 the
eleven consumers, T004 the classic runner, T005 the reachability test and the
cluster deletion, which is never split.

## Current Step

Round 5 is the production half of DECISION F272 D1's "move two": all 41
production callers of `pingpong_run_dir` and `pingpong_runs_dir` move onto
`run_dir` and `runs_dir`. Seven of them assign a local of that very name, so
those reach the function through `data_paths` instead of importing it, which
DECISION F272 D3 rules and explains. The two functions are NOT deleted yet and
nothing under `tests/` is touched.

## Next Steps

1. The test half of the same move — 132 occurrences in 27 files — and then the
   deletion of `pingpong_runs_dir` and `pingpong_run_dir` from `data_paths.py`
   in that round's last commit, with the alias test that pins them deleted
   alongside, its four properties already being pinned for the real names at
   `tests/test_data_paths.py` lines 79, 102, 376 and 396.
2. The rest of the unified record: the eleven administrative fields and the
   Mission extension (T002).
3. The eleven consumers named under Design in `T2_F260.md`, one per commit where
   the diff allows (T003).

## Risks

- A token swap shadows the imported function wherever a local is already called
  `run_dir`, and in `pingpong_loop.py` that is `UnboundLocalError` rather than a
  style problem. The shape rule exists for that and the gate counts the shadows
  to zero.
- A rename cannot be proved by mutating the accessor, because reader and writer
  move together. The proof is a before/after pair over tests that never name the
  old spelling.
<<<END PLANF272R5>>>

<<<BEGIN RECORDR5>>>
Done: R-0818 — RESOLVED at `0df30d70`, and the resolution is wider than the defect that raised it. The finding registered a DECISION ruled from a three-file grep that asserted a property of the whole test suite: DECISION F272 D1 said "the only code that observes the change is the three test files that hand-spell the layout", 24 test files did, and the branch tip went red at 207 tests. Round 3 swept those 24 files, moving 56 job-keyed path components from `"runs"` to `"job_logs"` and taking the tip from 207 failures to 2. The last 2 were a SECOND instance of this same finding rather than a new one, and per docs/agents/planner_reviewer_prompt.md §3 item 30 no second id was minted for them: the two CLI runtime smoke tests do not hand-spell anything themselves, they `subprocess`-launch `scripts/remedy_runtime_cli_smoke.py`, which spelled the job-keyed run log at line 168 — outside `tests/`, and therefore invisible to round 3's own completeness gate, which searched `tests/` because this finding's registration text told it to. Round 4 changed that one line to `root / "job_logs" / jid` at `0df30d70`. THE REVIEWER VERIFIED THE FIX RATHER THAN READING IT: the two node ids `tests/cli/test_propose_cli_runtime.py::TestProposeRuntimeSmoke::test_propose_flow` and `tests/cli/test_worker_cli_runtime.py::TestWorkerRuntimeSmoke::test_worker_flow` are EXIT 1 at `2 failed` at `385d3b16` and EXIT 0 at `2 passed` at the round 4 tip; the whole of `tests/cli/` goes from EXIT 1 at `2 failed, 1535 passed` to EXIT 0 at 1537 passed; and the 25-file observer set that this finding measured at 207 failures is now EXIT 0 at 1125 passed, every reading taken by the reviewer itself. THE STANDING RULE THIS FINDING CARRIED IS NOW ON DISK RATHER THAN IN A FINDING BODY, which is the R-0548 class it would otherwise have joined: DECISION F272 D2, committed at `95a21cc8` in `docs/roadmap/features/T2_F272.md`, rules in its CONSEQUENCE paragraph that the completeness count is taken over every tracked `.py` file in the whole repository, enumerated from `git ls-files` and never from a shell glob, and names the scoping of that count to `tests/` as the error the decision exists to correct. The count was then performed at that scope and returned six surviving `"runs" /` components, all of them run-keyed or filename-keyed and none job-keyed, reproduced independently by the reviewer over 1063 tracked `.py` files. The `Landed:` line above this paragraph is superseded rather than removed, because this record is append-only.

Gate: F272 R4 — the F272 round 4 entry. VERDICT PASS, AND THE TIP IS GREEN FOR THE FIRST TIME SINCE ROUND 2. Range `385d3b16`..`78457a98`, eight commits, every one single-parent, in exactly the bundle's ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6 with nothing added, dropped or reordered; insertion counts 319, 272, 17, 4, 1, 44 and 8 for the seven before the handback, every one far under the AGENTS.md DECISION F104 D1 cap of 500. `git diff --numstat 385d3b16..78457a98` lists exactly the eight paths of the change set and nothing more. THE REVIEWER RE-RAN EVERY GATE ITSELF AND EVERY NUMBER BELOW IS ITS OWN. TRANSPORT: the reviewer's scratch original `.remedy-wt/f272-r4-block.md`, the committed `.agent/authored/f272-r4.md` and the committed `.agent/last_block.md` are all 26458 bytes and all hash to `283e2a54ea9260765acbf000191191884ded42c06a21671df2dbf56f8170514c`, the digest the delegation named before the round began; per §3 item 37 that chain covers those three artefacts and is not a claim about the bytes emitted into a prompt. THE PRODUCTION CHANGE IS ONE LINE AND THE REVIEWER READ THE WHOLE DIFF: `git diff 7861b027 0df30d70` is exactly `1 1 scripts/remedy_runtime_cli_smoke.py`, changing `runs_dir = root / "runs" / jid` to `runs_dir = root / "job_logs" / jid` inside `read_events`, with no import, comment or reflow beside it. THE COLOUR PAIR IS REAL AND WAS REPRODUCED: the two runtime node ids are EXIT 1 at `2 failed in 2.30s` at `385d3b16` and EXIT 0 at `2 passed in 2.31s` at the tip, the whole of `tests/cli/` is EXIT 0 at 1537 passed against `2 failed, 1535 passed` before, the canary `tests/cli/test_golden_path.py` is EXIT 0 at 42 passed, and the 25-file observer set of round 3 is EXIT 0 at `1125 passed in 68.40s` where round 3 left it at `2 failed, 1123 passed`. THE RECORD, at C2, re-verified at the commit itself rather than at the tip: `.agent/live_review.md` 1066064 to 1072790 bytes with the pre-image a byte-exact prefix, `post == pre + NL + slice` TRUE, blank-line units 688 to 690 with N counted from the slice as 2 and the last two units equal to the slice's two paragraphs in order; at C5 the same reader gives 1072790 to 1073333 with `post == pre + NL + slice` TRUE, and `.agent/prose_slips.md` 132118 to 133530 likewise. Registrations 302 and resolutions 246 BY DISTINCT ID with the open set at 56, all three unchanged across the round; `^Gate: ` 24 to 26; `^Gate: F272 R2 ` and `^Gate: F272 R3 ` each 0 to 1; `^Landed: R-0818` 0 to 1; zero ids minted and no `Done:` paragraph written by the worker, which is exactly what §4 item 4 asks of it. THE PLAN, at C1: 2243 bytes byte-equal to the PLANF272R5 slice's predecessor PLANF272R4, 44 lines against the cap of 50, carrying `## Goal` and `## Next Steps`. THE FEATURE FILE, at C4: 11875 to 14790 bytes by the same append reader, `### DECISION F272 D2` exactly 1 beside `D1` exactly 1 and `## DECISIONs` exactly 1, and `tests/docs/` with `tests/orchestration/test_roadmap_index.py` EXIT 0 at 333 passed. THE COMPLETENESS COUNT AT ITS NEW SCOPE, reproduced by the reviewer over 1063 tracked `.py` files enumerated from `git ls-files` in Python: exactly six lines still carry a `"runs" /` component, at `tests/orchestration/test_context_compiler.py:1451`, `tests/orchestration/test_failure_postmortem.py:412`, `tests/orchestration/test_failure_wiring.py:903`, `tests/orchestration/test_gauntlet_runner.py:490`, `tests/test_data_paths.py:396` and `tests/test_data_paths.py:430`, none of them keyed by a job id, and no seventh. `python3 -m ruff check scripts/remedy_runtime_cli_smoke.py` is EXIT 0 at `All checks passed!` and `python3 -m apps.cli.grouped integrity check --json` is EXIT 0 with `"passed": true` and `"fail_count": 0`. `git status --porcelain` EMPTY, `git ls-files .remedy-wt` empty, zero marker lines in any of the six written files, and the `.agent/STOP` sentinel absent at all three ordered readings. SEVEN DEVIATIONS WERE DECLARED AND ALL SEVEN ARE UPHELD. THE FIRST IS THE REVIEWER'S AND IS CHARGED TO THE REVIEWER: constraint 4 and gate G2(a) of the round 4 block ordered `post == pre + b"\n" + slice + b"\n"` while defining the slice as lines each carrying their own terminating newline, which contradicts the same gate's "post ends in exactly one `\n`" clause and would have left a trailing blank unit that reader (b) could not match. The worker resolved it by MEASURING round 3's landed convention — `git show 20737a16^` at 961527 bytes against `git show 20737a16` at 965104, a delta of 3577 for a 3576-byte paragraph — rather than by preference, applied `post = pre + b"\n" + slice`, and declared it; the reviewer reproduced both readings and confirms the landed bytes are correct under the only self-consistent reading of its own text. That is a reviewer-prose defect that left nothing wrong on disk, so per operator amendment amend0827-process-diet rule 2 it spends no id and is one dated line in `.agent/prose_slips.md`. THE THIRD IS AN OBJECTION THE REVIEWER UPHOLDS AND DECLINES TO ACT ON: the moved line leaves its local variable named `runs_dir` while it now holds a `job_logs` path. That is true, and it is true identically at all 24 files round 3 swept, where round 3's own deviation 8 recorded the same reasoning — the local names the run-log directory generically rather than a path spelling, and AGENTS.md forbids mass renames as their own activity. The remaining five record that no worktree was created because gate G4(ii) needed none, that the repo-wide lint was correctly not widened, that eight scratch drivers under `.remedy-wt/` were removed by exact path and never by glob, and that no ninth path was touched.
<<<END RECORDR5>>>

<<<BEGIN SLIPSR5>>>
2026-09-06 · F272 R4 block (reviewer) · Constraint 4 and gate G2(a) ordered `post == pre + b"\n" + slice + b"\n"` while defining the slice as the lines between the markers each carrying its own terminating newline, which contradicts the same gate's "post ends in exactly one `\n`" clause and would have broken reader (b) on a trailing empty unit. The worker resolved it by measuring round 3's landed convention rather than by preference and declared it; the landed bytes are correct and nothing on disk was wrong, so it spends no id. The convention is stated once, correctly, in round 5's constraint 4.
<<<END SLIPSR5>>>

<<<BEGIN DECISIOND3>>>
### DECISION F272 D3 (2026-09-06, F272 round 5) — the name collapse takes two call shapes, chosen by whether the caller already binds the new name
DECISION F272 D1's "move two" deletes `pingpong_runs_dir` and `pingpong_run_dir`
in favour of `runs_dir` and `run_dir` at every call site. D1 described that as a
nineteen-site rename. It is not, and this decision records the real shape before
the sweep rather than after it.

MEASURED at `78457a98`, over every tracked `.py` file enumerated from
`git ls-files`: the two names occur 178 times in 34 files — 41 under `packages/`
and `apps/`, 132 under `tests/`, and 5 inside `data_paths.py` itself. D1's
nineteen was a reading of the call sites of one of the two names, taken before
the run store had been given one spelling, and it is superseded here by the
measurement rather than by an estimate.

THE HAZARD A PLAIN RENAME CARRIES, and the reason this is a decision rather than
a sweep. At 41 of those 178 sites the calling scope already binds a local named
`run_dir`, in the form `run_dir = pingpong_run_dir(...)`. A token swap turns
that into `run_dir = run_dir(...)`, which binds `run_dir` as a local for the
whole function, so the call on the right-hand side no longer resolves to the
import. Where the import is function-local and the assignment is the only use,
that reads badly and survives; where the import is module-level and the
assignment sits inside a function, as in the four such sites in
`packages/orchestration/pingpong_loop.py`, it is `UnboundLocalError` at runtime.
A rename whose failure mode is an exception in the live ping-pong path is not a
rename that should be performed by substitution.

CHOSEN — two shapes, and the choice is made by reading the enclosing scope:

- **Shape A, the plain token swap**, wherever the scope binds no local of that
  name. `pingpong_run_dir` becomes `run_dir` and `pingpong_runs_dir` becomes
  `runs_dir`, in the import and at the call, with nothing else on the line
  touched. This is the majority shape.
- **Shape B, the call through the module**, at every site whose scope does bind
  one. `from packages.orchestration import data_paths`, then
  `data_paths.run_dir(...)`. THE LOCAL KEEPS ITS NAME. The two rejected
  alternatives are rejected by AGENTS.md and not by taste: renaming the locals
  is a mass rename as its own activity, which the Scope Control section forbids,
  and importing the function under an alias is a local rename-import of a core
  concept, which the Code Discoverability section forbids by name.
- **`pingpong_loop.py` takes shape B at all thirteen of its sites**, not only at
  its four shadowing ones, so that one file has one shape and no later reader
  has to work out which of two idioms a given line is using.

THE COLLAPSE IS SPLIT ACROSS TWO ROUNDS, and the two functions survive the
first. Round 5 moves the 41 production sites; round 6 moves the 132 test sites
and deletes both bodies in its last commit, together with the one test that
exists only to pin them — `tests/test_data_paths.py`'s
`test_the_pingpong_run_dir_is_the_run_id_under_the_pingpong_runs_dir`, every
property of which is already pinned for the real names at lines 79, 102, 376 and
396 of that same file, so the deletion loses no coverage and the round says so
with those citations. Splitting is not deferral: it keeps a 34-file rename out
of the same commit range as a deletion, and it lets the production half carry a
real red-proof that the test half cannot.

THAT RED-PROOF IS WHY THE FUNCTIONS SURVIVE ROUND 5. A pure rename cannot be
proved by mutating the accessor, because moving one body moves reader and writer
in lockstep and no observer inside the system can see it — the defect the F260
R12 gate entry records against a gate that could not fail. While both spellings
still exist, a real discriminator does: make `pingpong_run_dir` raise, and run
only those test files that never name it themselves. Measured by the reviewer at
`78457a98` over the 88 files that rule selects, the unmutated control is EXIT 0
at 3562 passed and the mutated run is EXIT 1 at 330 failed with 17 errors. After
round 5 the same mutation over the same selection must be EXIT 0, and any
failure that survives names a production caller the round missed.

NOT CHANGED BY THIS RULING: D1's layout, D1's staging, and D2's
repository-wide completeness scope, which this sweep is measured against.

REVERSE by deleting this section, at which point the collapse returns to D1's
one-shape description and its nineteen-site estimate.
<<<END DECISIOND3>>>

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md:
`SESSION 2 of feature F272 · round 5`, the one-sentence context self-assessment
amend0905-throughput requires, branch, the range, a per-commit changed-files
table with real `+/-` from `git diff --numstat`, the item-status table covering
C0a through C7 with every item present exactly once, one line per gate G1 to G8
with its real exit code, the per-file site counts and shapes of G5(iv), the
authored-text proof table, deviations and assumptions, and the next expected
action. There is no length cap.
