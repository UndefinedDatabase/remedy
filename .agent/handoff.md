# Handback — F260 round 8

## Session

`SESSION 2 of feature F260 · round 8 · rounds so far 8`

## Range

Review of `072b54ed..b92d096f`.

Branch `feature/f260-one-world`. No branch created, no merge, no pull request
created or touched.

## Commits

Six commits, all single-parent, in the block's ordered sequence C0a → C4.
Insertion counts are the `+` column of `git diff --numstat`.

### 76dc7a47 f260: save the round 8 step block as authored text — C0a, +349

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f260-r8.md` | +349 / -0 | `shutil.copyfile` of `.remedy-wt/f260-r8-block.md`; not retyped |

### 3037d75b f260: mirror the round 8 block into the last block slot — C0b, +251

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +251 / -196 | same bytes copied over the round-7 block |

### ec1defd0 f260: book the round 7 gate record into the live review ledger — C1, +2

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +2 / -0 | append of `"\n"` + GATE_R7 (5010 bytes) + `"\n"` |

### 5a910981 f260: append the two round 7 reviewer prose slips — C2, +4

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/prose_slips.md` | +4 / -0 | append of `"\n"` + SLIP7 + `"\n\n"` + SLIP8 + `"\n"` |

### c333d06d f260: point the plan at the one spelling for the ping-pong store — C3, +21

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +21 / -19 | whole-file replacement by the PLANF260R8 slice + one newline |

### b92d096f f260: give the ping-pong store one spelling and delete the module-local jobs dir helper — C4, +257

One commit, eleven files, 257 insertions / 42 deletions — under the AGENTS.md
500-insertion cap, so no oversize declaration is owed. Deleting `_jobs_dir`
breaks every caller at once, so a production-only or test-only split would have
been red on its own.

| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/data_paths.py` | +28 / -0 | `task_job_dir`, `task_job_record_path`, the group comment, the `Public API::` lines |
| `packages/orchestration/pingpong_job.py` | +22 / -15 | `_jobs_dir` DELETED; its six users moved, each with its own function-scoped import |
| `packages/orchestration/job_evidence.py` | +2 / -2 | cross-module reach into `pingpong_job._jobs_dir` replaced by `data_paths.task_job_dir` |
| `tests/test_data_paths.py` | +183 / -8 | the guard: layout, root override, `hasattr`, the AST absence, the non-vacuity readings |
| `tests/orchestration/test_failure_wiring.py` | +2 / -1 | 1 call site + local import |
| `tests/orchestration/test_job_promote_consistency.py` | +3 / -2 | 1 call site + function-scoped from-import list |
| `tests/orchestration/test_job_stop_integration.py` | +3 / -3 | 2 `.parent` data-root readings + module-level from-import list |
| `tests/orchestration/test_job_worktree_handoff.py` | +6 / -5 | 5 call sites + module-level import |
| `tests/orchestration/test_job_worktree_integration.py` | +2 / -1 | 1 call site + module-level import |
| `tests/orchestration/test_job_worktree_integrity.py` | +2 / -1 | 1 call site + module-level import |
| `tests/orchestration/test_pingpong_integration.py` | +4 / -4 | 3 call sites + module-level from-import list |

Seventeen test sites, counted mechanically: 12 of shape `_jobs_dir() / <id> /
<tail>`, 2 `_jobs_dir().parent` data-root readings, 3 from-import lists.

C5 rewrites `.agent/handoff.md` (this file) and is not tabled above — a handoff
cannot table the commit that writes it (R-0149 pattern).

## External actions

| Command | Outcome |
|---------|---------|
| `git worktree add --detach .remedy-wt/f260-r8-mut 86750459` | created (first C4) |
| `git worktree remove --force .remedy-wt/f260-r8-mut` | removed after the G6(iii) gap was measured |
| `git worktree add --detach .remedy-wt/f260-r8-mut b92d096f` | re-created at the amended C4; full G6 re-run there |
| `git worktree remove --force .remedy-wt/f260-r8-mut` | removed before C5; `git worktree list` = 12 entries, all pre-existing `job-*` plus the primary |
| `git push origin feature/f260-one-world` | run after C5 — see below |

No PR created, edited or merged. No `gh` command run.

## Verification — G1..G8, real exit codes

| Gate | Result | Exit |
|------|--------|------|
| G1 TRANSPORT | `sha256sum` over the scratch block, `.agent/authored/f260-r8.md` and `.agent/last_block.md` returns ONE value `f362c984379e56fb99a3d1d6f58fb62cff55d7f02ebef6d26f4d15bf56209ed1`, equal to BLOCK_SHA | 0 |
| G2 THE RECORD | 893805 → 898817, growth 5012 = 1 + 5010 + 1; prefix exact; remainder exact; last unit STRIPPED equals the slice; units 425 → 426; one terminating newline; 299 / 4 / 17 `Gate:` headers all distinct; both negative controls reject in their own region only | 0 |
| G3 THE PROSE FILES | terminal byte before append `b'\n'`; 94802 → 97989 (+3187); prefix exact; remainder exact; units 129 → 131, a rise of exactly two. `.agent/plan.md` == PLANF260R8 + one newline, 48 lines (< 50) | 0 |
| G4 THE NAME IS GONE | (a) `hasattr(pingpong_job, "_jobs_dir")` = False. (b) `_jobs_dir` AST refs: `pingpong_job.py` 0, `job_evidence.py` 0, `storage.py` 0 — see deviation 1. (c) value preservation holds under a temp `REMEDY_DATA_DIR` | 0 |
| G5 RUFF | `python3 -m ruff check` over exactly the eleven C4 files: "All checks passed!" — not widened | 0 |
| G6 MUTATION RED-PROOF | control 46 passed; (i) 2 failed; (ii) 1 failed; (iii) 2 failed; import-removal proof RED with the predicted `NameError`; control green after every restore | see below |
| G7 THE SUITES | eleven suites serially, never through a pipe: 58, 34, 26, 26, 13, 24, 10, 46, 93, 178, 42 = 550 passed | 0 each |
| G8 THE TREE | `git status --porcelain` empty; `git ls-files .remedy-wt` empty; `.agent/STOP` absent; no worktree this round created survives; `git diff --name-only 072b54ed..b92d096f` printed 16 paths; `integrity check --json` `"passed": true`, `"fail_count": 0`, 5 checks, handlers=342 | 0 |

### G4(b), reported as measured

    packages/orchestration/pingpong_job.py: 0   lines=[]
    packages/orchestration/job_evidence.py: 0   lines=[]
    packages/orchestration/storage.py:      0   lines=[]

The third is ZERO, not non-zero. See deviation 1. Substitute non-vacuity
readings, supplied because the ordered one measures nothing:

* the same AST reading over `storage.py` for `_resolve_jobs_dir` returns 3 — the
  reader can find an underscore-prefixed private helper;
* the same reading for `_jobs_dir` at `072b54ed`, before any edit, returned 6 in
  `pingpong_job.py` and 2 in `job_evidence.py` — it can find *this* name when it
  is there. Both are now 0 because the name was deleted.

### G6 transcript, in a disposable worktree at `b92d096f`

Module resolution confirmed to come from the worktree
(`.remedy-wt/f260-r8-mut/packages/orchestration/data_paths.py`), not an editable
install. Every run used `python3 -B`.

| Run | Exit | Result |
|-----|------|--------|
| unmutated control | 0 | 46 passed |
| (i) record path re-spelled `task_jobs_dir(root) / "job.json" / job_id` | 1 | 2 failed, 44 passed |
| control after restore | 0 | 46 passed |
| (ii) `task_job_dir` ignores `root` | 1 | 1 failed, 45 passed |
| control after restore | 0 | 46 passed |
| (iii) `_jobs_dir` added back to `pingpong_job.py` | 1 | 2 failed, 44 passed |
| control after restore | 0 | 46 passed |
| import removed at the compound-`and` site, `test_job_worktree_handoff.py` | 1 | 2 failed, 24 passed |
| same suite after restore | 0 | 26 passed |

Failing node ids:

* (i) `tests/test_data_paths.py::TestJobAndRunLayout::test_the_task_job_record_is_job_json_under_the_task_job_dir`
  and `::TestJobAndRunLayout::test_the_root_override_is_honoured_by_both_task_job_helpers`
* (ii) `tests/test_data_paths.py::TestJobAndRunLayout::test_the_root_override_is_honoured_by_both_task_job_helpers`
* (iii) BOTH readings, as G6(iii) requires:
  `tests/test_data_paths.py::TestJobAndRunLayout::test_pingpong_job_has_no_jobs_dir_attribute_at_all` (the `hasattr` reading)
  and `tests/test_data_paths.py::TestJobAndRunLayout::test_no_migrated_module_names_the_deleted_jobs_dir_helper[packages.orchestration.pingpong_job]` (the AST reading).
  Only the `pingpong_job` parametrization failed — the `job_evidence` case stayed
  green, so the parametrization is genuinely per-module and not one assertion
  wearing two names.
* import-removal proof:
  `tests/orchestration/test_job_worktree_handoff.py::TestJobPlanResumeCli::test_the_cli_resumes_a_16_char_jobplan_id`
  and `::TestEndToEndJobFlow::test_plan_run_report_evidence_promote_dry_run`,
  both with `NameError: name 'task_job_dir' is not defined` at
  `packages/orchestration/pingpong_job.py:2878` — exactly the failure the block
  predicted, in exactly the two tests it predicted, and in no other suite.

### G7, per suite

| Suite | Passed | Exit |
|-------|--------|------|
| `tests/orchestration/test_failure_wiring.py` | 58 | 0 |
| `tests/orchestration/test_job_promote_consistency.py` | 34 | 0 |
| `tests/orchestration/test_job_stop_integration.py` | 26 | 0 |
| `tests/orchestration/test_job_worktree_handoff.py` | 26 | 0 |
| `tests/orchestration/test_job_worktree_integration.py` | 13 | 0 |
| `tests/orchestration/test_job_worktree_integrity.py` | 24 | 0 |
| `tests/orchestration/test_pingpong_integration.py` | 10 | 0 |
| `tests/test_data_paths.py` | 46 | 0 |
| `tests/orchestration/test_job_evidence.py` | 93 | 0 |
| `tests/test_do_job_flow.py` | 178 | 0 |
| `tests/cli/test_golden_path.py` (canary) | 42 | 0 |

### G8, the path list as the command printed it

    .agent/authored/f260-r8.md
    .agent/last_block.md
    .agent/live_review.md
    .agent/plan.md
    .agent/prose_slips.md
    packages/orchestration/data_paths.py
    packages/orchestration/job_evidence.py
    packages/orchestration/pingpong_job.py
    tests/orchestration/test_failure_wiring.py
    tests/orchestration/test_job_promote_consistency.py
    tests/orchestration/test_job_stop_integration.py
    tests/orchestration/test_job_worktree_handoff.py
    tests/orchestration/test_job_worktree_integration.py
    tests/orchestration/test_job_worktree_integrity.py
    tests/orchestration/test_pingpong_integration.py
    tests/test_data_paths.py

`wc -l` on that output: **16**. Reported as the command printed it, not checked
against a numeral this block asserts (SLIP7's lesson, applied).

## Authored-text proofs

| Slice | Target | Result |
|-------|--------|--------|
| whole block | `.agent/authored/f260-r8.md`, `.agent/last_block.md` | sha256 identical to the scratch original and to BLOCK_SHA |
| GATE_R7 (5010 B) | `.agent/live_review.md` | appended remainder byte-identical to `"\n"` + slice + `"\n"`; last blank-line unit, newline stripped, equals the slice |
| SLIP7 (1581 B), SLIP8 (1602 B) | `.agent/prose_slips.md` | appended remainder byte-identical to `"\n"` + SLIP7 + `"\n\n"` + SLIP8 + `"\n"` |
| PLANF260R8 (2623 B) | `.agent/plan.md` | file equals slice + exactly one trailing newline |

The block's warning about the double newline was reproduced before applying it:
the ordered recipe yields 131 units, the single-newline recipe yields 130.

## Deviations & assumptions

**1. Gate G4(b)'s non-vacuity clause is unmeetable as written — block defect,
measured.** G4(b) orders references resolving to exactly `_jobs_dir` to be
"NON-ZERO in `storage.py` — the third being the non-vacuity reading that proves
the search can find the name at all". Measured with the exact AST reading the
gate names: `storage.py` has **0** such references — and had 0 at `072b54ed`,
before this round touched anything. `storage.py` names `_resolve_jobs_dir`, a
DIFFERENT symbol, which is what the block's own "DO NOT TOUCH" paragraph says
fifty lines earlier ("a DIFFERENT symbol that merely contains the same
substring") and what the round-7 guard's docstring calls "correctly invisible".
So the clause contradicts the block's own reading of the same file, and as
ordered it proves nothing. The gate was applied exactly as ordered and 0/0/0 is
reported above; two substitute non-vacuity readings that DO discriminate are
reported beside it, not in place of it. Nothing on disk is wrong as a result.

**2. Gate G6(iii) cannot fail BOTH readings against the guard the block
specifies — block defect, measured, and the guard was changed to satisfy the
gate.** The guard paragraph orders the absence to be read "by the same AST
reference reading the round-7 guard uses". G6(iii) then requires that reviving
`_jobs_dir` as a function in `pingpong_job.py` "must fail BOTH the `hasattr`
reading and the AST reading". These two clauses are inconsistent: a reference
reading matches `ast.Name` / `ast.Attribute` / `ast.alias`, and a `def` is an
`ast.FunctionDef`, so an uncalled revived helper is invisible to it. Measured at
the first C4 (`86750459`): under mutation (iii) both parametrized AST cases
PASSED and only `hasattr` failed — 1 failed, 45 passed.

Resolution: `_names_of` was added beside `_references_to`. It is the round-7
reference reading PLUS the binding forms (`FunctionDef`, `AsyncFunctionDef`,
`ClassDef`) whose `.name` equals the target, and the new absence guard uses it.
The round-7 helper and the round-7 guard are untouched, so nothing that shipped
last round changed behaviour. Re-measured at `b92d096f`: mutation (iii) now
fails both readings, which is what G6(iii) ordered. A discriminator test pins the
definition arm as live (`len(_names_of(...)) > len(_references_to(...))` on
`storage._resolve_jobs_dir`), so the widening cannot silently collapse back.

This is a deliberate departure from the guard paragraph's "same AST reference
reading" phrasing. It was chosen because G6(iii) is the binding gate, and
because the guard's own claim — "no module in the migrated set NAMES `_jobs_dir`
at all" — is what a definition-inclusive reading measures and a reference-only
reading does not. Flagging it explicitly for the reviewer to overrule if the
phrasing was meant to bind instead.

**3. C4 was amended once — a departure from the ordered commit sequence in
mechanism, not in shape.** The first C4 was `86750459`. After deviation 2 was
measured, the guard fix was folded into C4 with `git commit --amend` rather than
added as a twelfth commit, so the block's ordered sequence C0a, C0b, C1, C2, C3,
C4, C5 stays exactly as ordered and the change set is unchanged. Nothing had
been pushed at that point, so this is not a force-push and G2 of
self_drive_protocol.md is not engaged. Final C4 = `b92d096f`. Every gate was
re-run at `b92d096f`, and G6 was re-run from the control in a FRESHLY created
worktree at that commit — the earlier worktree was removed first.

**4. The block says "Two of them import `_jobs_dir` by name in a from-import
list"; there are THREE.** Measured: `test_pingpong_integration.py:17` and
`test_job_stop_integration.py:31` (module level) and
`test_job_promote_consistency.py:351` (function-scoped). All three moved to
`data_paths`. The block's count of SEVENTEEN test sites is correct and already
includes all three: 12 call sites of shape `_jobs_dir() / <id> / <tail>`, 2
`_jobs_dir().parent` data-root readings, 3 from-import lists. Only the adjective
"two" is wrong; the set is complete.

**5. Two added test imports are function-scoped, not module-level.** In
`test_failure_wiring.py` and `test_job_promote_consistency.py` the `_jobs_dir`
use sits inside a function whose own imports are function-local, so the added
import went into that local block in isort order — that is "where that file's
existing imports live" for those two sites. ruff is clean over both.

**6. Two of the seventeen test sites have `job.json` as their tail** —
`test_failure_wiring.py` and `test_job_worktree_handoff.py:170`. They were
written as `task_job_dir(<id>) / "job.json"`, exactly the transformation the
block states, even though `task_job_record_path(<id>)` would give the same value
without a test re-spelling the record layout by hand — the practice
`TestJobAndRunLayout`'s own docstring warns against. Applied as ordered rather
than repaired, per constraint 1; noted here for the reviewer to rule on.

**7. Open-findings arithmetic, both readings.** 299 registration paragraphs, 4
`Done:` lines over 2 distinct ids (R-0721 and R-0725 each carry two). By the
ledger's stated arithmetic — paragraphs minus `Done:` lines — **295 open**. By
distinct id, 297. Reporting the stated convention as the headline, and the other
because the two disagree.

No other deviation. No `docs/` change was needed: this round moves no behaviour
and adds no user-visible surface, only a spelling. `.agent/context.md` and
`.agent/decisions.md` were not touched — DECISION F260 D1 and D2 already record
the layout and id rules this round builds on, and no new decision was made.

## Item-status table

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block | done | |
| C0b mirror the block | done | |
| C1 the R7 gate record | done | |
| C2 the two prose slips | done | |
| C3 the plan | done | |
| C4 accessors + 6 production + 17 test sites + guard | deviated | guard reading widened to satisfy G6(iii); commit amended once — deviations 2 and 3 |
| C5 the handback | done | this file |
| G1 transport | done | one digest, equals BLOCK_SHA |
| G2 the record | done | |
| G3 the prose files | done | |
| G4 the name is gone | deviated | (b)'s `storage.py` non-vacuity clause unmeetable; applied as ordered, substitutes supplied — deviation 1 |
| G5 ruff | done | eleven files only, not widened |
| G6 mutation red-proof | done | all four proofs red, controls green throughout — after deviation 2's fix |
| G7 the suites | done | 11 suites, 550 passed, all exit 0 |
| G8 the tree and change set | done | 16 paths printed; integrity `passed: true` |

## Open findings

**295** open by the ledger's stated arithmetic (299 registrations − 4 `Done:`
lines); 297 by distinct id. No blocker or high finding is open —
`integrity check` reports `high_blockers_open: pass`.

## Next

Reviewer verdict on round 8, then T002's actual record move: collapse
`task_job_dir` / `task_job_record_path` into `job_dir` / `job_record_path` so
`<data_root>/task_jobs/<16hex>/job.json` becomes
`<data_root>/jobs/<16hex>/job.json`, moving `data_paths._task_job_id_matches` in
the SAME commit or every ping-pong job becomes unresolvable. Finding R-0814
resolves there, against the fix clause it carries.
