# Handoff — F277 Machine contracts: event vocabulary, JSON envelope, exit codes · Round 13

## Session

SESSION 7 of feature F277 · round 13 · rounds so far 13

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE.

**SCOPE REPORT (obliged by amend0827 rule 6 while at the 7-session soft limit).** Unchanged
since round 12 and already executed, so it is restated in brief rather than re-argued.
*Finished:* T001, the event vocabulary, and T002, the JSON envelope with its dispatch error
boundary, are both complete contracts. *Missing:* T003 is applied in part — `fail()` exists
and nine of the twenty-eight CLI modules call it; nineteen modules and the catalog half
remain. T004 is not started. *The proposal, already executed:* DECISION F277 D10 closes F277
on T001 and T002 complete and T003 in part, with the remainder registered as F283 directly
after F277's STATUS line. The operator question it owes is `.agent/operator_questions.md` Q2.
Round 13 adds nothing to this report; it is the closure sequence continuing.

Context self-assessment: the worker read `AGENTS.md`, `docs/agents/handback_template.md`,
`.remedy-wt/f277-r13-block.md` and `docs/roadmap/STATUS_closure_protocol.md` in full before
any edit, plus `docs/roadmap/features/T2_F277.md` around the clause C2 repairs and the four
payloads. Verified the block's own bytes first (R-0954, below), found no `.agent/STOP` on
disk, verified the branch clean at `4f335b03`, then verified all four PAYLOADS entries before
using any of them. Executed the five-commit bundle C1a, C1b, C2, C3, C4 in order and ran all
six gates for real.

## Range

Review of `4f335b03`..`HEAD`.

## Commits

### 649d2873 F277 R13 C1a: copy round 13 payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f277-r13-block.md | +237/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f277-r13-f277-fix.diff | +16/-0 | byte-for-byte copy of f277-fix.diff payload |
| .agent/authored/f277-r13-ledger.md | +2/-0 | byte-for-byte copy of ledger.md payload |
| .agent/authored/f277-r13-plan.md | +49/-0 | byte-for-byte copy of plan.md payload |
| .agent/authored/f277-r13-slips.md | +3/-0 | byte-for-byte copy of slips.md payload |

Measured insertions by `git show --numstat`: **307**. Block's expectation: 70 payload lines
plus this block's own 237 = 307. MATCHES. THE CAP ARITHMETIC THE BLOCK ORDERED, run BEFORE
committing: `500 − 70 − 237 = ` **193**, positive, so the commit was legal to make and no
second oversize declaration was needed. This feature's one permitted declaration stays spent
where round 12 spent it.

### ab081b97 F277 R13 C1b: book round 12's PASS and three reviewer slips, rewrite plan
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | append round 12's PASS entry (ledger.md payload) |
| .agent/plan.md | +28/-25 | rewrite to plan.md payload, byte-identical (sha `0fa5a997…`), 49 lines |
| .agent/prose_slips.md | +3/-0 | append the three prose-slip lines (slips.md payload) |

Measured insertions by `git show --numstat`: **33** (2 + 28 + 3). Block expected **33**, and
named `28 25 .agent/plan.md` as the reviewer's own dry-run numstat. MATCHES on both the total
and the per-file rewrite reading — the DIFF's count, not the payload's 49 lines, which is the
distinction round 12 got wrong and the second prose-slip line now records.

### aca27d4a F277 R13 C2: name both commits in the Built State clause round 12 got wrong
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T2_F277.md | +4/-2 | apply f277-fix.diff: the corrected "WHAT MOVED TO F283" clause, naming `90976846` and `3c3ca820` |

Measured insertions by `git show --numstat`: **4**. Block expected **3**. DECLARED, not
adjusted — see deviation 1. The payload was applied verbatim via `git apply`; its hunk
removes 2 lines and adds 4, so 4 is the reading the gate takes.

### 47116516 F277 R13 C3: generate and run the closure's self-use item
| Path | +/- | Reason |
|---|---|---|
| scripts/self_use_queue.json | +8/-0 | the generator's append of SU-025 and nothing else; `consumed_by` left as the empty string |

Measured insertions by `git show --numstat`: **8**. The diff is one new queue object —
`id`, `title`, `why`, `job_markdown`, `consumed_by`, `provenance` — appended after SU-024.
No existing item was touched.

Self-reference exception (handback template, R-0149 pattern): the commit that writes this
handoff and the trailing commit that fills in its post-push G6 readings share one grouped
table with per-commit attribution, following rounds 9 through 12's identical precedent — a
handback cannot table the commit that writes it.

### (this commit) F277 R13 C4: rewrite handoff for round 13
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, first and only write; G6's push and status readings are not knowable before the push C4 performs |

### (trailing) F277 R13 C4-fix: record the actual push outcome in the handoff
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | this edit | fill in the real `git push` / `git status --porcelain` output for G6, only knowable after C4 was pushed |

## External actions

- `git push -u origin feature/f277-machine-contracts` — outcome under Verification / G6 below
  (the round's final act).
- No `gh` command, no PR created, edited or merged.
- NO WORKTREE WAS ADDED OR REMOVED BY THE WORKER. One worktree appeared during C3 and it is
  the self-use RUN's own: `.remedy-wt/job-86f628f5e4fb4e0c` on branch
  `remedy/job-86f628f5e4fb4e0c`, whose job id is the run's job id. Constraint 5 names this as
  expected. It is left in place, exactly as the two pre-existing job worktrees were.

## Verification

### Pre-flight

- `ls .agent/STOP` → `No such file or directory`, real exit code **2**. No STOP on disk.
- `git status --porcelain` → empty (no output).
- `git branch --show-current` → `feature/f277-machine-contracts`.
- `git rev-parse HEAD` → `4f335b0320bef61bc2bbed5f01c71752ee9a6ede`, matching the block's
  stated tip `4f335b03`.
- Block self-verification (R-0954), `.remedy-wt/f277-r13-block.md`:

| reading | measured | given in the delegation message | equal |
|---|---|---|---|
| line count | 237 | 237 | True |
| sha256 | `b81bf9fad4bbb52d131067d7616847dcd61bd54f285d914b0476eb64532cdbe4` | `b81bf9fad4bbb52d131067d7616847dcd61bd54f285d914b0476eb64532cdbe4` | True |

Real exit code 0. Neither differs, so the round proceeded.

### G1(a) — PAYLOADS transport, all four files, twelve readings

| file | lines measured / given | bytes measured / given | sha256 measured (given identical) | equal |
|---|---|---|---|---|
| f277-fix.diff | 16 / 16 | 1088 / 1088 | `932b7f5bb90880a6df7b7b256e2faa9635d7d719ae1705c01efda5b168a517e5` | True |
| ledger.md | 2 / 2 | 7938 / 7938 | `179d9ace9be680b32048f70d0e24d3aec1074a5b4bcba1bf1d7ca3e072e12bb2` | True |
| plan.md | 49 / 49 | 2578 / 2578 | `0fa5a9978e86dd44f61bee44d403eed7490d8f2212d7d7d5ecfcfec499011b55` | True |
| slips.md | 3 / 3 | 3493 / 3493 | `cf7071e6bd0d81bd77b1b10d9c6e3b1b50cf02730a1036499a5fae79822d3692` | True |

Script printed `twelve readings all equal: True`, real exit code **0**. The two separator
shapes the block declared were verified on disk rather than assumed: `ledger.md` begins with
a leading newline (`leading newline: True`), `slips.md` and `plan.md` do not
(`leading newline: False`). The payload directory holds exactly these four files.

`git apply --check .remedy-wt/f277-r13-payloads/f277-fix.diff` → `CHECK_REAL_EXIT=0`, run
before the real apply, which read `APPLY_REAL_EXIT=0` (constraint 1).

### G1(b) — the five `.agent/authored/f277-r13-*` copies vs. their sources

Each copy read back from disk and compared byte-for-byte with its source under
`.remedy-wt/f277-r13-payloads/` (the block copy against `.remedy-wt/f277-r13-block.md`):

| copy | bytes | IDENTICAL_TO_SOURCE |
|---|---|---|
| f277-r13-block.md | 16096 | True |
| f277-r13-f277-fix.diff | 1088 | True |
| f277-r13-ledger.md | 7938 | True |
| f277-r13-plan.md | 2578 | True |
| f277-r13-slips.md | 3493 | True |

Five readings, all True (`all five True: True`). Real exit code **0**. Copying was done with
`shutil.copyfile`; no payload was retyped.

### G1(c) — the two appends at C1b

| file | pre measured | pre, reviewer's | equal | payload | post | post−pre | pre+payload=post |
|---|---|---|---|---|---|---|---|
| .agent/live_review.md | 446927 | 446927 | True | 7938 | 454865 | 7938 | True |
| .agent/prose_slips.md | 344565 | 344565 | True | 3493 | 348058 | 3493 | True |

Both pre values equal the reviewer's exactly. Each post was additionally verified as
pre-prefixed AND payload-suffixed (`pre is exact prefix: True`,
`payload is exact suffix: True` for both). Real exit code **0**.

NEGATIVE CONTROL, on `.agent/live_review.md` only. One bit flipped at absolute offset 447127
— offset 200 into the appended region, inside the FIRST appended paragraph — turning `r` into
`s`, length unchanged at 454865 bytes:

```
baseline suffix-equals-payload : True
MUTATED  suffix-equals-payload : False      <- the control
RESTORED suffix-equals-payload : True
restored equals baseline       : True
```

sha256 moved `cc03a5e7…` → `4dfc9b24…` → `cc03a5e7…`. The byte COUNT was unchanged by the
flip, so a length check alone would not have caught it and the comparison is doing real work.
The file was restored to its exact baseline bytes before staging; the committed blob is the
unmutated one. Real exit code **0**.

### G1(d) — the plan rewrite at C1b

| reading | value |
|---|---|
| payload sha256 | `0fa5a9978e86dd44f61bee44d403eed7490d8f2212d7d7d5ecfcfec499011b55` |
| on-disk sha256 | `0fa5a9978e86dd44f61bee44d403eed7490d8f2212d7d7d5ecfcfec499011b55` |
| equal byte-for-byte | True |
| line count | 49 |

49 lines, under the AGENTS.md sub-50 rule.

### G1(e) — open set by distinct id in `.agent/live_review.md`

| rev | ids matching `^- R-\d+ — ` | ids matching `^Done: R-\d+ — ` | OPEN |
|---|---|---|---|
| 4f335b03 | 27 | 7 | **20** |
| ab081b97 (C1b) | 27 | 7 | **20** |

Both numbers measured, not asserted equal. Round 13 registered and resolved nothing: the two
self-use defect strings are REPORTED below for the reviewer, never registered by the worker.

### G2 — the Built State clause

The corrected paragraph's first four lines, read verbatim from
`docs/roadmap/features/T2_F277.md` at lines 219–222 after C2:

```
**WHAT MOVED TO F283** (`docs/roadmap/features/T2_F283.md`, registered at `90976846` and
struck from the Acceptance list above at `3c3ca820`, the two adjacent commits of round 12;
this clause read "in the same commit" until round 13 corrected it): T003's remainder —
the nineteen unmigrated
```

Count of the string `registered in the same commit` in that file: **0**.

`git diff --name-only ab081b97 aca27d4a`:

```
docs/roadmap/features/T2_F277.md
```

LENGTH **1** — exactly the one expected path, nothing else. Real exit code **0**.

### G3 — the docs and state-contract gate, primary checkout, at C2

```
$ python3 -m pytest -q -p no:cacheprovider tests/docs/ \
  tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py \
  tests/regression/test_resource_safety.py
451 passed in 105.39s (0:01:45)
```
Real exit code **0**.

Against the reviewer's dry run of `449 passed, 2 skipped` at exit 0 in a disposable worktree:
the COLLECTED TOTAL is the same number, **451**, and the exit code is the same, but here
nothing skipped. That is exactly the primary-checkout shape the block predicted — the two
tests a fresh worktree skips ran and passed here. Reported as measured, not reconciled away.
The full suite was NOT run, per constraint 6 and amend0917 rule 1.

### G4 — THE SELF-USE PRECONDITION (closure precondition 6)

The run HAPPENED, under the real configured provider, and every reading C3 items (i) to (v)
name is below. Driver: `.remedy-wt/f277-r13-scratch/c3_selfuse.py`, full log at
`.remedy-wt/f277-r13-scratch/c3_selfuse.log` (gitignored). Real exit code **0**.

| reading | value | reviewer's dry run |
|---|---|---|
| (i) `len(pending_self_use_items())` BEFORE | **0** | 0 at `4f335b03` — matches |
| (ii) generated entry `id` | `SU-025` | `SU-025` — matches |
| (ii) generated entry `title` | `Address ledger finding R-0820` | same — matches |
| (ii) generated entry `provenance` | `generated (self-use-generator tier 1, ledger scan, R-0820)` | tier 1 ledger scan — matches |
| (iii) role config | `RoleConfig(role='self_use', provider='claude-cli', model='claude-sonnet-4-6', effort='medium', routed_call={'task_class': 'standard_build', 'tier': 'mid', 'reason': 'seed_mapping', 'promoted_by': None})` | provider `claude-cli`, model `claude-sonnet-4-6`, effort `medium` — matches |
| (iv) job id | `86f628f5e4fb4e0c` | — |
| (iv) `JobPlan.state` | **`blocked`** (`JOB_BLOCKED`) | — |
| (iv) provider that ACTUALLY ran | builder `claude-cli` (source `cli`), reviewer `claude-cli` (source `cli`), both at model `claude-sonnet-4-6`, effort `medium` | — |
| (iv) wall clock | **513.84 s** (01:11:47 → 01:20:00 local) | — |
| (v) defect tuple length | **2** | — |
| pending count AFTER the run | **1** | — |
| new item's `consumed_by` | `''` — the empty string, both in memory and on disk in `scripts/self_use_queue.json` | required empty |

No `builder_name` / `reviewer_name` was passed, so the run resolved the configured provider
itself; `execution_config` confirms `claude-cli` on both sides with source `cli`, never
`fake` and never the local model.

`JOB_BLOCKED` is one of the two outcomes the block names as legitimate, so this is a RUN
OUTCOME and not a red gate (constraint 4's explicit carve-out). Nothing raised — no
`SelfUseRunError` and no other exception. The job's own fields:

```
plan.error              = 'task_T001_gate_failed: final_status=provider_unavailable; missing_reviewer_output'
plan.stop_reason        = ''
plan.stop_source        = ''
plan.run_manifest_error = ''
task count: 1
    task T001 status='blocked' final_status='provider_unavailable'
               error='completion_gate_failed: final_status=provider_unavailable; missing_reviewer_output'
```

**THE TWO DEFECT STRINGS `describe_self_use_run_defects(plan)` RETURNED, VERBATIM AND IN
ORDER.** These are REPORTED for the reviewer to register next round as R-id findings; the
worker registered nothing, per the block and precondition 6.

1. (113 chars)
```
job 86f628f5e4fb4e0c (blocked): task_T001_gate_failed: final_status=provider_unavailable; missing_reviewer_output
```
2. (98 chars)
```
T001 (blocked): completion_gate_failed: final_status=provider_unavailable; missing_reviewer_output
```

Tuple length **2** — this is NOT an empty tuple, so there IS something to register.

### G5 — canary and tree hygiene

```
$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 130.71s (0:02:10)
```
Real exit code **0**, matching the reviewer's own 42.

`git worktree list` BEFORE C3 — **3** entries, exit code 0:
```
/home/decodeux/Repos/remedy                                  aca27d4a [feature/f277-machine-contracts]
/home/decodeux/Repos/remedy/.remedy-wt/job-468c8e62a2cc4fac  1b9ae606 [remedy/job-468c8e62a2cc4fac]
/home/decodeux/Repos/remedy/.remedy-wt/job-c1dba9c3d7874968  fd23710f [remedy/job-c1dba9c3d7874968]
```
Two `remedy/job-*` worktrees, matching the reviewer's measurement at `4f335b03`.
`git branch --list 'remedy/job-*'` BEFORE C3: **39** branches.

`git worktree list` AFTER C3 — **4** entries, exit code 0:
```
/home/decodeux/Repos/remedy                                  aca27d4a [feature/f277-machine-contracts]
/home/decodeux/Repos/remedy/.remedy-wt/job-468c8e62a2cc4fac  1b9ae606 [remedy/job-468c8e62a2cc4fac]
/home/decodeux/Repos/remedy/.remedy-wt/job-86f628f5e4fb4e0c  aca27d4a [remedy/job-86f628f5e4fb4e0c]
/home/decodeux/Repos/remedy/.remedy-wt/job-c1dba9c3d7874968  fd23710f [remedy/job-c1dba9c3d7874968]
```
`git branch --list 'remedy/job-*'` AFTER C3: **40** branches.

THE THIRD JOB WORKTREE IS EXPLAINED AND ITS ID MATCHES. Exactly one worktree and one branch
appeared (3→4, 39→40), both named `job-86f628f5e4fb4e0c` / `remedy/job-86f628f5e4fb4e0c`, and
`86f628f5e4fb4e0c` IS the job id the self-use run reported in G4. There is no unexplained new
worktree and no unexplained new branch.

### The round's whole path set (constraint 3)

`git diff --name-only 4f335b03 47116516` — LENGTH **10**:

| # | commit | path |
|---|---|---|
| 1 | C1a | .agent/authored/f277-r13-block.md |
| 2 | C1a | .agent/authored/f277-r13-f277-fix.diff |
| 3 | C1a | .agent/authored/f277-r13-ledger.md |
| 4 | C1a | .agent/authored/f277-r13-plan.md |
| 5 | C1a | .agent/authored/f277-r13-slips.md |
| 6 | C1b | .agent/live_review.md |
| 7 | C1b | .agent/plan.md |
| 8 | C1b | .agent/prose_slips.md |
| 9 | C2 | docs/roadmap/features/T2_F277.md |
| 10 | C3 | scripts/self_use_queue.json |

Paths under `packages/`, `apps/` or `tests/`: **count 0**, empty list — a measured count, not
an assertion. With `.agent/handoff.md` from C4 this is exactly the ten-path set the block
names, none added. `.agent/decisions.md` and `.agent/operator_questions.md` were not touched.

Commit trailers, checked one commit at a time over `4f335b03..47116516`
(`git log --format='%h TRAILER=[%(trailers:key=Co-Authored-By,valueonly)]'`): all four read
`Claude Opus 5 <noreply@anthropic.com>`.

### G6 — push and tree, after C4

C4 commits this handoff and THEN pushes, so the readings below did not exist at the moment C4
was written. They are recorded verbatim by the trailing C4-fix commit, which touches nothing
else (deviation 2).

- `git push -u origin feature/f277-machine-contracts`, real exit code **0**:
```
To github.com:UndefinedDatabase/remedy.git
   4f335b03..8ffc7bba  feature/f277-machine-contracts -> feature/f277-machine-contracts
Branch 'feature/f277-machine-contracts' set up to track remote branch 'feature/f277-machine-contracts' from 'origin'.
```
  SUCCEEDED. The remote tip of the branch is `8ffc7bba`, which is C4. At the moment C4 was
  committed this section read "PENDING AT THIS COMMIT" rather than a predicted SHA — no push
  reading was written before the push happened.
- `git status --porcelain` after the push: **empty** (no output), real exit code **0**.
  Constraint 5 holds: no tracked file is left dirty, despite the run writing under `.data/`,
  under its own job worktree and under the gitignored scratch directory.

C4-fix, the commit carrying this paragraph, is pushed immediately after it; its own push
outcome is reported in the session output rather than recursively here.

## Authored-text proofs

Every reviewer-authored text applied this round was compared disk-to-disk against its
committed `.agent/authored/f277-r13-*` copy, per the fidelity protocol:

- The five copies at C1a vs. their originals under `.remedy-wt/f277-r13-payloads/` (block copy
  vs. `.remedy-wt/f277-r13-block.md`): five readings, all True — see G1(b).
- The REWRITE payload vs. the committed file at C1b: `.agent/plan.md`, sha256-equal to its
  payload at 49 lines — see G1(d).
- The two APPEND payloads vs. the committed files at C1b: each committed file is its
  `4f335b03` bytes as an exact prefix plus its payload as an exact suffix — see G1(c), with a
  negative control proving the comparison can return False.
- The `.diff` payload was never retyped and never edited: `f277-fix.diff` went on with
  `git apply` after its own `git apply --check` at exit 0, and its committed copy is
  byte-identical to the original (G1(b)).
- `scripts/self_use_queue.json`'s C3 change is NOT reviewer-authored text: it is the
  generator's own output, written by `generate_and_append_if_empty()` and committed unedited.

## Deviations & assumptions

1. **C2's measured insertions are 4, not the block's expected 3.** The payload was applied
   verbatim and NOT adjusted to reach 3. `f277-fix.diff`'s single hunk removes two lines and
   adds four (`+4/-2` by `git show --numstat`), so 4 is the reading DECISION F104 D1 fixes.
   The block's "Expected insertions: 3" appears to have counted the added lines that carry
   new prose while overlooking the fourth, `the nineteen unmigrated`, which the rewrap
   produced. Nothing on disk is wrong — G2 shows the corrected clause and a zero count of the
   stale string — and this is the same class as round 12's second prose slip: a block numeral
   that did not survive measurement. Declared here for the reviewer's disposition; the worker
   authored no finding.
2. **A trailing C4-fix commit beyond the block's five, for G6's post-push readings.** C4
   writes this handoff and then pushes, so the `git push` and `git status` outcomes cannot
   exist when C4 is committed. C4-fix records the real readings and touches nothing else.
   This is the handback template's explicit trailing-bookkeeping exception (R-0149 pattern)
   and follows rounds 9 through 12's identical, reviewed precedent — round 12's own ledger
   entry books the trailing commit as part of an unbroken sequence. Apart from it, the
   five-commit bundle ran in the block's exact order — none dropped, none reordered.
3. **The self-use run ended `JOB_BLOCKED` with `provider_unavailable`, and this is reported
   as an outcome rather than treated as a gate failure.** The block and constraint 4 both name
   `JOB_BLOCKED` as a legitimate result; the gate is that the run HAPPENED and was reported,
   which G4 does in full. The worker did NOT retry the run, did not pass a fake provider, and
   did not investigate or repair the `provider_unavailable` cause: the two defect strings are
   exactly what the closure protocol asks be surfaced for registration, and diagnosing them
   would be the worker authoring a finding, which the block forbids.
4. **`.agent/plan.md` was rewritten at C1b, one commit AFTER C1a.** The AGENTS.md Commit Gate
   asks that the plan match the work before every commit, and at C1a it still described round
   12. This is the block's own ordered bundle (C1a mirrors the payloads, C1b books and
   rewrites) and the established shape of every round of this feature, so it is noted rather
   than argued; from C1b onward the plan describes round 13.
5. No mutation red-proof was run and no disposable worktree was created by the worker, per
   constraint 6 — the round's change set holds no file under `packages/` or `apps/`, measured
   at 0 above. The full suite was not run; it is round 14's integration gate.
6. **One command beyond the ordered gates**, read-only: `git log --format=…%(trailers)…` over
   the round's range, to verify the commit trailer on each commit rather than assume it. No
   tree effect.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a copy block + 4 payloads | done | 307 insertions, matching the block's 70+237; cap headroom 193 |
| C1b book PASS + three slips, rewrite plan | done | 33 insertions, matching the block's expected 33 exactly |
| C2 repair the Built State clause | deviated | applied verbatim; measured 4 insertions vs the block's expected 3 — see deviation 1 |
| C3 generate and run the self-use item | done | SU-025 generated and RUN under `claude-cli`; `JOB_BLOCKED`, 2 defect strings, `consumed_by` left empty |
| C4 rewrite handoff and push | done | this commit plus the declared C4-fix |
| G1 transport and state (a–e) | done | 12/12 payload readings, 5/5 copies, 2/2 appends + negative control, plan rewrite identical at 49 lines, open set 20 and 20 |
| G2 the Built State clause | done | corrected paragraph quoted; stale string count 0; path list length 1 |
| G3 docs and state-contract | done | `451 passed in 105.39s`, exit 0 |
| G4 the self-use precondition | done | every reading (i)–(v) reported; run happened, 513.84 s, `JOB_BLOCKED`, 2 defects verbatim |
| G5 canary and tree hygiene | done | `42 passed` exit 0; worktrees 3→4 and branches 39→40, the one new pair matching job id `86f628f5e4fb4e0c` |
| G6 push and tree | done | readings recorded by the trailing C4-fix commit; push exit 0, porcelain empty |
| Constraint 1 no payload edited or retyped | done | `git apply --check` exit 0 before the apply; copies via `shutil.copyfile`, all byte-identical |
| Constraint 2 every commit under 500 insertions | done | 307, 33, 4, 8 — the largest is 307, and the cap arithmetic was run BEFORE committing C1a |
| Constraint 3 no file the block does not name | done | 10 paths, exactly the block's set; 0 under `packages/`, `apps/` or `tests/` |
| Constraint 4 stop on a red gate | done | no gate went red; `JOB_BLOCKED` is the named carve-out, not a red gate |
| Constraint 5 tree clean, run's own artefacts not a leak | done | porcelain empty at C4; the one new worktree/branch is the run's own, id-matched |
| Constraint 6 no mutation red-proof, no full suite | done | none ordered, none run; see deviation 5 |
| DO NOT set `consumed_by` | done | measured `''` in memory and on disk after the run |
| DO NOT register a finding | done | open set 20 at `4f335b03` and 20 at C1b; both defect strings reported here only |

## Next

Phase 1 rule 1 first: read `.agent/STOP` from disk. Then the review of round 13 — C1a, C1b,
C2, C3, C4 and the declared C4-fix, all six gates. Then round 14: the reviewer registers each
of the TWO self-use defect strings reported in G4 as an R-id finding in `.agent/live_review.md`
under the standard rules, then `remedy integrity check --json` at PASS, then the integration
gate running the full suite ONCE, by the worker, in the primary checkout, with its transcript
committed as `.agent/authored/f277-closure-suite.txt`.

Open findings count: **20**. Operator-questions count: **2**.
