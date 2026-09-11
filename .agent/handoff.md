# Handback — F275 round 47

## Session

SESSION 19 of feature F275 · round 47 · rounds so far 47

Context self-assessment (amend0905-throughput): context is comfortable — this
round read AGENTS.md, the 280-line self-drive protocol and the 105-line handback
template, verified and copied a 31417-byte block, ran a generator plus two hand
fixes over fourteen code paths, and spent the rest on eight gate runs including a
scoped 376-test selection, a 42-test canary and a four-reading mutation red proof
in a disposable worktree, so there is room for at least one more round this
session.

F275 stands at 47 rounds and 19 sessions against the operator's soft limit of 60
rounds and 20 sessions (amend0908-f275-finish rule 1), so no scope report is owed
by THIS session. The NEXT session is the twentieth and owes one.

## THE ONE THING THE REVIEWER MUST READ FIRST

**EIGHT GATES RUN — I RAN EIGHT, G1 THROUGH G8 — ALL GREEN, AND THE PRODUCTION
CHANGE IS PROVEN REACHED: mutation M1 turns `tests/test_task_runner.py` from 45
passed to 40 failed, 5 passed.** `TaskExecutionContext.job_id` and `.task_id` now
read `<class 'str'>` when the shipped class is IMPORTED, all 34 construction
sites pass `str(...)`, and the fourteen-path `git diff --numstat` table matches
the block cell for cell, including `builder_models.py` at 2/3 where FIX A deleted
the now-unused `from uuid import UUID`.

**ONE SLICE FACT DOES NOT REPRODUCE AND IS DECLARED, NOT EDITED.** Slice DECIDE47
states the widen is "34 construction sites across 14 files, 32 insertions". The
34 sites reproduce exactly (17 `job_id` + 17 `task_id`, from the generator's own
counter). The insertion count does NOT: C3 is **34 insertions, 35 deletions**, not
32. 32 is the GENERATOR-ONLY figure — the thirteen files it rewrites sum to 2×10
+ 4×3 = 32 insertions — measured before the two hand fixes the same block orders,
which add `tests/test_task_runner.py` at 2/2 and one further deletion in
`builder_models.py`. "14 files" is likewise the post-fix change-set count, while
the 34 construction sites live in THIRTEEN files; the fourteenth carries only FIX
B's two assertions. Constraint 1 says a slice that looks wrong is applied as given
and declared, so DECIDE47 is committed byte for byte and this paragraph is the
declaration. Nothing on disk is wrong: G6(b)'s table is the post-fix reading and
it matched exactly.

The open set is unchanged at **86 by distinct id** (104 registrations − 18
resolutions), identical at the base `013e5517` and at C4. No id registered, none
resolved. `R-0876` is still UNREGISTERED — `^- R-0876 — ` reads 0 at C1 and 0 at
C4, while the bare token occurs once at C4 inside RECORD47's own prose, exactly
as the block predicted.

## Range

Review of `013e5517`..`HEAD` — C0a through C5. C5 is the commit that writes this
file and cannot table itself.

## Commits

### 3bdaaac1 F275 R47 C0a: save the round 47 step block verbatim.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r47.md` | +372 / -0 | the step block, `shutil.copyfile` from `.remedy-wt/f275-r47.block.md`, never retyped |

### 8a6d6ebb F275 R47 C0b: mirror the round 47 block into last_block.md.

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +310 / -400 | written from `git cat-file blob 3bdaaac1:.agent/authored/f275-r47.md` |

### ffac7c43 F275 R47 C1: the round 47 plan.

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +20 / -23 | whole-file replacement by slice PLAN47 |

### 8d2784b3 F275 R47 C2: book the round 46 PASS verdict and the two round 46 reviewer slips.

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2 / -0 | append of slice RECORD47 — the round 46 PASS verdict |
| `.agent/prose_slips.md` | +4 / -0 | append of slice SLIPS47 — the two dated reviewer slips |

### 3295d184 F275 R47 C3: widen TaskExecutionContext job_id and task_id to str at every construction site.

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/autorun.py` | +2 / -2 | generator: two construction sites take `str(...)` |
| `packages/orchestration/builder_models.py` | +2 / -3 | generator: the two annotations become `str`; FIX A deletes `from uuid import UUID` |
| `packages/orchestration/long_run_executor.py` | +2 / -2 | generator: two construction sites |
| `packages/orchestration/task_runner.py` | +2 / -2 | generator: two construction sites in `_build_execution_context` |
| `tests/orchestration/test_builder_bridge_smoke.py` | +2 / -2 | generator: two construction sites |
| `tests/orchestration/test_builder_eval.py` | +2 / -2 | generator: two construction sites |
| `tests/orchestration/test_builder_prompt_quality.py` | +2 / -2 | generator: four construction sites on two lines |
| `tests/orchestration/test_escalation.py` | +2 / -2 | generator: four construction sites on two lines |
| `tests/orchestration/test_long_run_executor.py` | +4 / -4 | generator: four construction sites |
| `tests/orchestration/test_loop_run.py` | +2 / -2 | generator: two construction sites |
| `tests/orchestration/test_real_ollama_smoke.py` | +4 / -4 | generator: four construction sites |
| `tests/orchestration/test_self_healing_cycles.py` | +2 / -2 | generator: two construction sites |
| `tests/test_ollama_builder.py` | +4 / -4 | generator: four construction sites |
| `tests/test_task_runner.py` | +2 / -2 | FIX B: both assertions compare against `str(...)` |

Commit total: +34 / -35. The generator itself was written to the gitignored
`.remedy-wt/widen47.py`, run once from the repository root, and is NOT committed.

### a1f948e7 F275 R47 C4: record DECISION F275 D27, the id shape migrates one model at a time.

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +14 / -0 | append of slice DECIDE47 — DECISION F275 D27 |

### C5 (this commit) F275 R47 C5: the round 47 handback.

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback (R-0149 self-reference exception) |

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a save the block verbatim | done | `shutil.copyfile`, digest re-verified on the destination |
| C0b mirror into last_block.md | done | from the committed blob of C0a |
| C1 slice PLAN47 | done | whole-file replacement, byte-equal |
| C2 slices RECORD47 + SLIPS47 | done | two appends, `old_bytes + slice_bytes` |
| C3 THE WIDEN (WIDEN47 + FIX A + FIX B) | done | generator run once; both hand fixes applied |
| C4 slice DECIDE47 | done | append, three readings green |
| C5 the handback | done | this file |
| G1 transport | done | PASS |
| G2 the plan | done | PASS |
| G3 the record and the slips | done | PASS |
| G4 the decisions | done | PASS |
| G5 the open set | done | PASS |
| G6 the widen is exactly what was ordered | done | PASS |
| G7 the red proof | done | PASS — M1 went red |
| G8 nothing else moved | done | PASS |
| FIX A delete `from uuid import UUID` | done | 0 occurrences at C3 |
| FIX B the two `test_task_runner.py` assertions | done | both sides one spelling |
| Constraint 8 re-read `.agent/STOP` from disk | done | ABSENT — `ls` exits 2, `Path.exists()` False |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach /home/decodeux/Repos/remedy/.remedy-wt/g7-r47 3295d184` | exit 0, worktree HEAD `3295d18413cd373b9cf6d786b2a1389a3b2924a2` |
| `git worktree remove --force .remedy-wt/g7-r47` then `git worktree prune` | exit 0; `git worktree list` reads ONE entry |
| `git push -u origin feature/f275-one-world-completion-part-three` | exit 0, `013e5517..a1f948e7` |
| `gh pr list --state open --json number,headRefName,baseRefName,isDraft` | `[]` — no open PR; none created, edited or merged this round |

No pull request was created, edited or merged. No force-push, no history rewrite,
no branch deletion.

## Verification

Eight gates, each run for real as `bash -c '<cmd>; echo "REAL_EXIT=$?"'` or as a
Python driver whose own exit code was echoed the same way. I ran EIGHT gates.

**G1 TRANSPORT, at C0b — PASS.** The chain the proof walked: the scratch order
`.remedy-wt/f275-r47.block.md` → the saved copy `.agent/authored/f275-r47.md`
(`shutil.copyfile`, never retyped) → its committed blob at C0a → the mirror
`.agent/last_block.md` (`git cat-file blob 3bdaaac1:.agent/authored/f275-r47.md`,
never retyped) → the working copy on disk. All four readings:

    committed blob    31417 bytes  def622533158a25f4002b15cc7e8ee4ecc4a31c7ab812e48e9e972f17dcc7f31
    last_block.md     31417 bytes  def622533158a25f4002b15cc7e8ee4ecc4a31c7ab812e48e9e972f17dcc7f31
    authored (disk)   31417 bytes  def622533158a25f4002b15cc7e8ee4ecc4a31c7ab812e48e9e972f17dcc7f31
    scratch order     31417 bytes  def622533158a25f4002b15cc7e8ee4ecc4a31c7ab812e48e9e972f17dcc7f31
    ORDERED DIGEST                 def622533158a25f4002b15cc7e8ee4ecc4a31c7ab812e48e9e972f17dcc7f31
    all four equal: True

The digest was verified over the file's bytes BEFORE the block was read for
content. I claim nothing about the bytes emitted into my prompt; nothing here can
measure those. Every slice was extracted from the COMMITTED blob by marker-line
PREFIX (`.remedy-wt/r47_slice.py`), with an assertion that each `BEGIN-`/`END-`
prefix matches exactly one line.

**G2 THE PLAN, at C1 — PASS.**

    slice PLAN47       2586 bytes  sha256 41bbe0fbac63acb1738bdfff1135f7dc7393e9410e1f5395c81c4ddaadea2dc2
    .agent/plan.md     2586 bytes  sha256 41bbe0fbac63acb1738bdfff1135f7dc7393e9410e1f5395c81c4ddaadea2dc2
    byte-equal: True
    line count: 44   AGENTS.md cap 50 -> OK
    ^## Goal$        count: 1
    ^## Next Steps$  count: 1

**G3 THE RECORD AND THE SLIPS, at C2 — PASS.** Every pre and post blob read with
`git show <sha>:<path>` INTO MEMORY; no non-current revision was written over a
tracked file. Pre blobs asserted equal to the C1 revision.

    --- RECORD47 -> .agent/live_review.md
        pre bytes 884856  slice bytes 3879  post bytes 888735
        pre sha 28dfab14d56a6b0a  post sha ff40e48db81641ee
        (a) reader A pre+slice == post -> identical: True
        (b) reader B: N counted in slice = 1; last 1 units equal, in order: True
        (c) control: flipped byte at offset 886795, inside the FIRST appended
            paragraph of the in-memory copy
            reader A rejects: True
            reader B rejects: True  (N still 1, yardstick = ORIGINAL slice)
    --- SLIPS47 -> .agent/prose_slips.md
        pre bytes 237582  slice bytes 1689  post bytes 239271
        pre sha 727b5780d01f56c8  post sha ac877bba9352f7f0
        (a) reader A pre+slice == post -> identical: True

N is counted by the script from the slice, never asserted by the block. Both
controls flip one byte in the IN-MEMORY copy only and are re-run against the
ORIGINAL slice, so the yardstick stays clean.

**G4 THE DECISIONS, at C4 — PASS.** Pre blob asserted equal to the C3 revision.

    --- DECIDE47 -> .agent/decisions.md
        pre bytes 1076187  slice bytes 4122  post bytes 1080309
        pre sha 4e1f89ae51d0ffbb  post sha 7e88e49ade1ce2ca
        (a) reader A pre+slice == post -> identical: True
        (b) reader B: N counted in slice = 7; last 7 units equal, in order: True
        (c) control: flipped byte at offset 1076304, inside the FIRST appended
            paragraph of the in-memory copy
            reader A rejects: True
            reader B rejects: True  (N still 7, yardstick = ORIGINAL slice)

**G5 THE OPEN SET, at C4, BY DISTINCT ID — PASS.**

    distinct registrations: 104   distinct resolutions: 18
    open set = 104 - 18 = 86          (ordered: 104 - 18 = 86)
    at base 013e5517: 104 - 18 = 86
    ids REGISTERED this round: []
    ids RESOLVED   this round: []
      '^Gate: F275 R46 ' at C1: 0        at C4: 1
      '^- R-0876 — '    at C1: 0        at C4: 0
      bare token 'R-0876' anywhere: 0 at C1, 1 at C4

The bare-token line is reported only to show why the gate is anchored on the
REGISTRATION form: the one occurrence at C4 is RECORD47's own quotation.

**G6 THE WIDEN IS EXACTLY WHAT WAS ORDERED, at C3 — PASS.**

(a) By IMPORTING the shipped class, not by reading its source; the import path is
printed so nothing is believed on faith:

    module: packages.orchestration.builder_models
    file  : /home/decodeux/Repos/remedy/packages/orchestration/builder_models.py
    job_id annotation : <class 'str'>
    task_id annotation: <class 'str'>
    REAL_EXIT=0

(b) `git diff --numstat 013e5517..3295d184 -- <the fourteen code paths>`,
REAL_EXIT=0. Every row equals the ordered table, cell for cell; no row differs:

    2  2  packages/orchestration/autorun.py
    2  3  packages/orchestration/builder_models.py
    2  2  packages/orchestration/long_run_executor.py
    2  2  packages/orchestration/task_runner.py
    2  2  tests/orchestration/test_builder_bridge_smoke.py
    2  2  tests/orchestration/test_builder_eval.py
    2  2  tests/orchestration/test_builder_prompt_quality.py
    2  2  tests/orchestration/test_escalation.py
    4  4  tests/orchestration/test_long_run_executor.py
    2  2  tests/orchestration/test_loop_run.py
    4  4  tests/orchestration/test_real_ollama_smoke.py
    2  2  tests/orchestration/test_self_healing_cycles.py
    4  4  tests/test_ollama_builder.py
    2  2  tests/test_task_runner.py

(c) `git show 3295d184:packages/orchestration/builder_models.py | grep -c "from
uuid import UUID"` prints `0`, REAL_EXIT=1 (grep's zero-match exit). FIX A landed.

(d) The SCOPED round gate, in the primary checkout at C3:

    python3 -m pytest tests/orchestration/test_builder_bridge_smoke.py \
      tests/orchestration/test_builder_eval.py \
      tests/orchestration/test_builder_prompt_quality.py \
      tests/orchestration/test_escalation.py \
      tests/orchestration/test_long_run_executor.py \
      tests/orchestration/test_loop_run.py \
      tests/orchestration/test_self_healing_cycles.py tests/test_ollama_builder.py \
      tests/test_task_runner.py tests/orchestration/test_ci_budgets.py -q
    376 passed, 2 skipped in 2.10s
    REAL_EXIT=0

    python3 -m pytest tests/cli/test_golden_path.py -q
    42 passed in 18.89s
    REAL_EXIT=0

`tests/orchestration/test_ci_budgets.py` is inside that selection and passes, so
the ruff ceiling of 26 that FIX A exists for is measured, not assumed.

**G7 THE RED PROOF, at C3 — PASS, M1 GOES RED.** A disposable worktree at
`.remedy-wt/g7-r47`, detached at `3295d184`, never `cd`-ed into: every command ran
as `subprocess.run([...], cwd=<abs worktree>)` under `python3 -B`, with
`__pycache__` purged before every run. The imported module's path was printed
BEFORE any result was believed, and asserted to start with the worktree path, so
no editable install could shadow it. Four readings, in order:

    import path: /home/decodeux/Repos/remedy/.remedy-wt/g7-r47/packages/orchestration/task_runner.py  exit 0
    pristine sha256: b89977a0ee8f76788c9de197ee2f336b16c01d04c86b753e49780fd0c1019297

    1. CONTROL, unmutated, tests/test_task_runner.py
       REAL_EXIT=0   last line: 45 passed in 0.24s

    2. MUTATION M1 — count of 'job_id=str(job.id),' in
       packages/orchestration/task_runner.py: 1  (required 1 before applying)
       reverted that ONE occurrence to 'job_id=job.id,'
       REAL_EXIT=1   last line: 40 failed, 5 passed in 0.64s
       FAILED node ids (40), the token after the FIRST space of each FAILED line:
         tests/test_task_runner.py::test_run_next_task_changed_true
         tests/test_task_runner.py::test_run_next_task_executes_first_pending
         tests/test_task_runner.py::test_run_next_task_skips_non_pending
         tests/test_task_runner.py::test_provider_receives_task_execution_context
         tests/test_task_runner.py::test_context_fields_populated_correctly
         tests/test_task_runner.py::test_context_includes_prior_task_summaries
         tests/test_task_runner.py::test_context_no_planning_summary_when_absent
         tests/test_task_runner.py::test_context_planning_summary_from_explicit_kind
         tests/test_task_runner.py::test_context_planning_summary_from_legacy_artifact
         tests/test_task_runner.py::test_artifact_task_id_matches_executed_task
         tests/test_task_runner.py::test_output_artifact_ids_updated
         tests/test_task_runner.py::test_artifact_name_contains_task_type
         tests/test_task_runner.py::test_artifact_content_contains_summary
         tests/test_task_runner.py::test_artifact_metadata_has_no_legacy_builder_key
         tests/test_task_runner.py::test_artifact_metadata_has_task_type_and_summary
         tests/test_task_runner.py::test_task_running_after_run_next_task
         tests/test_task_runner.py::test_job_running_while_tasks_remain
         tests/test_task_runner.py::test_job_not_completed_until_finalize_task_called
         tests/test_task_runner.py::test_sequential_execution_advances_through_tasks
         tests/test_task_runner.py::test_builder_failure_rolls_task_back_to_pending
         tests/test_task_runner.py::test_builder_failure_restores_job_state
         tests/test_task_runner.py::test_builder_failure_on_partially_executed_job_preserves_running
         tests/test_task_runner.py::test_builder_error_propagates
         tests/test_task_runner.py::test_annotate_task_result_adds_metadata
         tests/test_task_runner.py::test_annotate_task_result_raises_if_changed_but_no_artifact
         tests/test_task_runner.py::test_annotate_task_result_finds_by_task_id_not_index
         tests/test_task_runner.py::test_finalize_task_marks_completed_when_verified
         tests/test_task_runner.py::test_finalize_task_advances_job_to_completed
         tests/test_task_runner.py::test_finalize_task_does_not_complete_job_while_tasks_remain
         tests/test_task_runner.py::test_finalize_task_rolls_back_to_pending_on_failure
         tests/test_task_runner.py::test_finalize_task_clears_output_artifact_ids_on_failure
         tests/test_task_runner.py::test_finalize_task_failed_artifact_remains_in_job_artifacts
         tests/test_task_runner.py::test_finalize_task_records_failure_in_artifact_metadata
         tests/test_task_runner.py::test_retry_after_failure_uses_new_artifact_not_stale
         tests/test_task_runner.py::test_consecutive_failures_annotate_each_artifact_separately
         tests/test_task_runner.py::test_consecutive_failures_each_clear_output_artifact_ids
         tests/test_task_runner.py::test_consecutive_failures_both_artifacts_preserved_in_job
         tests/test_task_runner.py::test_finalize_task_raises_if_task_not_in_job
         tests/test_task_runner.py::test_finalize_task_raises_if_no_output_artifact_ids_on_failure
         tests/test_task_runner.py::test_finalize_task_raises_if_artifact_not_found_in_job_artifacts

    3. REVERT, proved by sha256:
       post-revert sha256: b89977a0ee8f76788c9de197ee2f336b16c01d04c86b753e49780fd0c1019297
       equals pristine: True

    4. CONTROL again
       REAL_EXIT=0   last line: 45 passed in 0.24s

Then `git worktree remove --force` + `git worktree prune`, REAL_EXIT=0, and
`git worktree list` reads ONE entry:

    /home/decodeux/Repos/remedy  3295d184 [feature/f275-one-world-completion-part-three]

Reading the result: the mutation reaches far more than the one assertion FIX B
edits, because `TaskExecutionContext` is now a pydantic model whose `job_id` is
`str` — feeding it a `uuid.UUID` raises a validation error inside
`_build_execution_context`, so every test that runs a task fails. That is a
strictly stronger reachability claim than the two assertions alone would give.

**G8 NOTHING ELSE MOVED, at C4 — PASS.**

    STOP exists on disk (re-read, not remembered): False
    git status --porcelain literal: ''   exit 0
    changed paths 013e5517..a1f948e7: 20
    MISSING (vs Change list MINUS .agent/handoff.md): []
    EXTRA   (vs Change list MINUS .agent/handoff.md): []
    paths under apps/, docs/, scripts/: []

Insertions per commit against the F104 D1 cap of 500, derived ONCE from
`git show --numstat <sha>` and reused in the `## Commits` tables above:

    C0a 3bdaaac1: +372  -0     OK
    C0b 8a6d6ebb: +310  -400   OK
    C1  ffac7c43: +20   -23    OK
    C2  8d2784b3: +6    -0     OK
    C3  3295d184: +34   -35    OK
    C4  a1f948e7: +14   -0     OK

No commit is oversize; no declaration under the AGENTS.md oversize exception is
needed or made.

**Generator transcript (C3), for the record.** `.remedy-wt/widen47.py`, 4032
bytes, sha256 `9a17ee4f78f97f74e632111016ced556a0f77081f87ad420d6a272bf9da86fcc`,
extracted from the committed blob, confirmed ignored by
`git check-ignore -v` (`.gitignore:235:.remedy-wt/`), run ONCE from the repository
root:

    files rewritten: 13
      decl TaskExecutionContext.job_id       1
      decl TaskExecutionContext.task_id      1
      writer TaskExecutionContext.job_id     17
      writer TaskExecutionContext.task_id    17
    total edits: 36

No `writer SKIPPED multiline` line appeared and no `BROKE` line appeared, so every
site was single-line and every rewritten file re-parsed.

## Authored-text proofs

Every slice was extracted mechanically from the COMMITTED blob of
`.agent/authored/f275-r47.md` by `BEGIN-<name> ` / `END-<name> ` marker-line
PREFIX. None was retyped, reflowed or edited.

| Slice | Target | Proof | Result |
|---|---|---|---|
| PLAN47 | `.agent/plan.md` | whole-file byte equality, both sha256 | identical, 2586 bytes |
| RECORD47 | `.agent/live_review.md` | reader A + reader B + negative control | identical: True |
| SLIPS47 | `.agent/prose_slips.md` | reader A | identical: True |
| WIDEN47 | `.remedy-wt/widen47.py` (scratch, never committed) | extracted from the C2 blob, sha256 recorded, `git check-ignore` confirms | run once, exit 0 |
| DECIDE47 | `.agent/decisions.md` | reader A + reader B + negative control | identical: True |

`.agent/authored/f275-r47.md` itself is byte-identical to the delegation order's
stated digest (G1).

## Deviations & assumptions

1. **DECLARED SLICE FACT THAT DOES NOT REPRODUCE — DECIDE47's "32 insertions".**
   Slice DECIDE47 says the widen "is 34 construction sites across 14 files, 32
   insertions". The measured C3 commit is **34 insertions / 35 deletions**. 32 is
   the generator-only figure (thirteen files, 2×10 + 4×3); the two hand fixes the
   same block orders add `tests/test_task_runner.py` at +2/-2 and one further
   deletion in `builder_models.py`. Likewise the 34 construction sites live in
   THIRTEEN files, not fourteen — the fourteenth path carries only FIX B's
   assertions. Under Constraint 1 the slice was applied byte for byte and is
   declared here rather than edited. G6(b)'s fourteen-row table is the correct
   post-fix reading and matched exactly, so nothing on disk is wrong.
2. **No departure from the ordered commit sequence.** C0a, C0b, C1, C2, C3, C4,
   C5 ran in exactly that order; none merged, none reordered, none added, none
   dropped. Seven commits, seven ordered items.
3. **`.agent/plan.md` at C0a and C0b.** The block fixes the plan slice at C1, so
   C0a and C0b were committed while `.agent/plan.md` still described round 46.
   This is the block's own ordered sequence (Constraint 2), not a choice of mine;
   noting it because the AGENTS.md Commit Gate asks for a current plan before
   EVERY commit and the two block-transport commits are the standing exception
   this feature has used in every round.
4. **G6(c)'s exit code.** The absence check is `grep -c`, which exits 1 when it
   matches nothing. REAL_EXIT=1 is the PASSING reading for that gate and is
   reported as measured rather than smoothed into a 0.
5. **No finding registered, none resolved**, as Constraint 5 requires. The open
   set reads 86 by distinct id at the base and 86 at C4.
6. **Constraint 8**: `.agent/STOP` was re-read from disk before the first commit
   — `ls` exited 2 ("No such file or directory") and `pathlib.Path(...).exists()`
   returned False. It was re-read again at G8 with the same result.
7. Scratch drivers `r47_slice.py`, `r47_append.py`, `r47_c2.py`, `r47_c4.py`,
   `r47_g5g8.py`, `r47_g7.py` and `widen47.py` all live under the gitignored
   `.remedy-wt/` and none is committed. The G7 worktree was removed and pruned.
8. No path under `apps/`, `docs/` or `scripts/` moved. No `.py` file outside the
   block's fourteen named code paths was committed.

## Next

The planner/reviewer re-derives all eight gates from the committed range
`013e5517`..`HEAD` and issues the round 47 verdict. On PASS, the next round is
the DIAGNOSIS of `PatchIntentSet.task_id` — the four `tests/test_grouped_cli.py`
tests that fail `Error: Job not found` only under full-suite ordering — before
that field is widened; Phase 1 rule 1 (`.agent/STOP`) is checked before rule 2.
