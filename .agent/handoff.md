# Handoff — F272 One world completion, round 10

## Session

SESSION 4 of feature F272 · round 10 · rounds so far 10

Context self-assessment (amend0905-throughput): context is comfortable — this round
spent its budget on eight full suite runs rather than on writing, and the reading
volume was small, so a further round in this session is affordable.

ROUND 10 EXECUTED THE BUNDLE IN FULL. C0a through C7 all landed, in the ordered
sequence, with nothing added and nothing reordered. The rename round 9 refused to
guess at is now MEASURED: the ordered command reaches EXIT 0 with the raising probe
installed, and the site set it converged on is 234 sites across 35 files — eighteen
of those files outside the seventeen the block named as its expected core.

## Range

Review of `027bdc2c`..`HEAD` (branch `feature/f272-one-world-completion`).

## Commits

### 31c4ed95 f272: save the round 10 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f272-r10.md` | +400 / -0 | C0a, `shutil.copyfile` of the reviewer's scratch original |

### 33ecf575 f272: mirror the round 10 step block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +307 / -307 | C0b, byte copy of the same original |

### cdab7fbe f272: set the plan to the round 10 measured rename step
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +14 / -14 | C1, replaced by the PLANF272R10 slice |

### 6b679548 f272: book the round 9 PASS verdict and register finding R-0820
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4 / -0 | C2, RECORDR10 appended |

### c1597759 f272: rule the rename set as measured by runtime probe in DECISION F272 D7
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T2_F272.md` | +42 / -0 | C3, DECISIONR10 appended |

### e869aad9 f272: record the measured state rename inventory from the runtime probe
| Path | +/- | Reason |
|---|---|---|
| `.agent/f272_state_rename_inventory.md` | +380 / -0 | C4, the inventory, written from the measurement and not from a prediction |

### f4136d24 f272: rename JobPlan.status to JobPlan.state at every measured site
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/do_cmd.py` | +8 / -8 | C5, 5 probe sites, 1 getattr, 2 annotation |
| `apps/cli/commands/job_stop_cmd.py` | +10 / -10 | C5, 8 probe sites + the `_CoreJobAdapter` stand-in (slot and assignment) |
| `packages/orchestration/job_evidence.py` | +10 / -10 | C5, 7 probe sites, 3 getattr |
| `packages/orchestration/job_promote.py` | +3 / -3 | C5, 3 probe sites |
| `packages/orchestration/pingpong_job.py` | +33 / -33 | C5, the dataclass field + 26 probe sites + 4 constructor keywords + 2 annotation sites = 33 |
| `packages/orchestration/run_manifest.py` | +1 / -1 | C5, 1 getattr site in `_job_is_resumable` |
| `packages/orchestration/self_use_findings.py` | +1 / -1 | C5, the production site round 9 named |
| `packages/orchestration/self_use_runner.py` | +1 / -1 | C5, 1 probe site |
| `packages/orchestration/ui_server.py` | +1 / -1 | C5, `_JobPlanAdapter.__init__`, 2 reads on one line |
| `tests/cli/test_job_rerun_manifest.py` | +8 / -8 | C5, 8 probe sites |
| `tests/cli/test_job_stop.py` | +5 / -5 | C5, 5 probe write sites |
| `tests/orchestration/test_budget_guard.py` | +1 / -1 | C5, 1 constructor keyword |
| `tests/orchestration/test_episode_snapshot_lifecycle.py` | +6 / -6 | C5, 6 probe sites |
| `tests/orchestration/test_f018_authority_integration.py` | +22 / -22 | C5, 17 probe sites, 5 constructor keywords |
| `tests/orchestration/test_f018_package_pipeline_e2e.py` | +4 / -4 | C5, 1 probe site, 3 constructor keywords |
| `tests/orchestration/test_failure_wiring.py` | +2 / -2 | C5, 2 probe sites |
| `tests/orchestration/test_final_audit_evidence.py` | +3 / -3 | C5, three stand-ins — `_FakeJob` and two `FakePlan` classes |
| `tests/orchestration/test_job_evidence.py` | +2 / -2 | C5, 2 probe sites |
| `tests/orchestration/test_job_promote.py` | +23 / -23 | C5, 23 constructor keywords |
| `tests/orchestration/test_job_promote_consistency.py` | +1 / -1 | C5, 1 probe site |
| `tests/orchestration/test_job_stop_integration.py` | +26 / -26 | C5, 25 probe sites + the site inside the generated runner script |
| `tests/orchestration/test_job_task_runner.py` | +26 / -26 | C5, 26 probe sites |
| `tests/orchestration/test_job_worktree_handoff.py` | +7 / -7 | C5, 7 probe sites |
| `tests/orchestration/test_job_worktree_integration.py` | +6 / -6 | C5, 6 probe sites |
| `tests/orchestration/test_job_worktree_integrity.py` | +8 / -8 | C5, 8 probe sites |
| `tests/orchestration/test_pingpong_integration.py` | +2 / -2 | C5, 1 probe site + the `FakeJob` stand-in |
| `tests/orchestration/test_predictive_budget.py` | +5 / -5 | C5, 5 probe sites |
| `tests/orchestration/test_run_manifest_episode_graph.py` | +1 / -1 | C5, the `_J` stand-in |
| `tests/orchestration/test_run_manifest_reference_coverage.py` | +1 / -1 | C5, 1 probe site |
| `tests/orchestration/test_run_manifest_runtime_truth.py` | +1 / -1 | C5, 1 probe site |
| `tests/orchestration/test_run_manifest_terminal_consistency.py` | +1 / -1 | C5, the `_Job` stand-in |
| `tests/orchestration/test_run_manifest_zero_call_expectations.py` | +1 / -1 | C5, 1 probe site |
| `tests/orchestration/test_self_use_findings.py` | +1 / -1 | C5, 1 probe site |
| `tests/orchestration/test_self_use_runner.py` | +2 / -2 | C5, 2 probe sites |
| `tests/test_do_job_flow.py` | +1 / -1 | C5, the `_FakeJob` stand-in, OUTSIDE both ordered suites |

### 868ba410 f272: pin the state field, the unchanged stored key and the rendering
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_job_state_field.py` | +90 / -0 | C6, new file, 9 tests |

### C7 — this handoff
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | self-referential | C7 cannot table the commit that writes it (R-0149 pattern) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | `.agent/authored/f272-r10.md`, byte copy, digest verified before any other action |
| C0b | done | `.agent/last_block.md`, byte copy of the same original |
| C1 | done | plan replaced by the PLANF272R10 slice, byte-equal |
| C2 | done | RECORDR10 appended; every ordered count matched exactly |
| C3 | done | DECISION F272 D7 appended; headings read D1..D7 in order |
| C4 | done | the inventory, 234 sites over 35 files, written from the converged measurement |
| C5 | done | one commit, 35 files, 234 insertions |
| C6 | done | `tests/orchestration/test_job_state_field.py`, 9 tests, all five minima covered |
| C7 | done | this handoff |

No commit exists outside this ordered sequence; see the Deviations section.

## Verification

One line per gate with its REAL exit code, then the transcripts. "Green" as a word
appears nowhere; where a gate is red it says so and says why.

| Gate | Exit | Reading |
|---|---|---|
| G1 TRANSPORT | 0 | three artefacts, all 32692 bytes / 400 lines, all sha256 `e0aea48b…d8d2a13` |
| G2 THE RECORD | 0 | readers (a)(b)(c)(d) all accept; all six ordered counts matched |
| G3 PLAN + FEATURE FILE | 0 | plan byte-equal at 2173 B / 43 lines; feature file readers accept; D1..D7 |
| G4 THE RENAME IS COMPLETE | 0 | control EXIT 1 naming exactly the reverted site; residual run EXIT 0; (iii)(iv)(v) all as required |
| G5 MUTATION RED-PROOF | 0 | control EXIT 0; three mutations EXIT 1, 1, 1; three restores byte-identical; three control re-runs EXIT 0 |
| G6 THE SUITES | 0 | five invocations, every one EXIT 0; `tests/orchestration/` rose 12838 → 12847 |
| G7 LINT AND INTEGRITY | **1** and 0 | ruff EXIT 1 on ONE pre-existing `I001`, proven present at `027bdc2c`; integrity EXIT 0 |
| G8 THE TREE | 0 | tree empty, `git ls-files .remedy-wt` empty, both worktrees removed by exact path |

### G1 TRANSPORT — a real three-artefact chain

Per §3 item 37 this covers the saved copy and its mirror, not the bytes emitted into
my prompt.

| Artefact | Bytes | Lines | sha256 |
|---|---|---|---|
| `.remedy-wt/f272-r10-block.md` (reviewer's surviving original) | 32692 | 400 | `e0aea48b27d07b255fa7c18c7ad1abbbd5bfa4893ac04dafd14d7daaad8d2a13` |
| `.agent/authored/f272-r10.md` at HEAD (C0a) | 32692 | 400 | same |
| `.agent/last_block.md` at HEAD (C0b) | 32692 | 400 | same |

All three equal each other and equal the delegation's BLOCK_SHA, BLOCK_LENGTH and
BLOCK_LINES. Verified BEFORE any other action was taken.

### G2 THE RECORD at C2 — exit 0

`.agent/live_review.md`, readers (a) to (d):

- (a) BYTE: pre 1109691 → post 1118077; pre a byte-exact prefix; `post == pre + b"\n" +
  slice` TRUE; pre's terminal byte asserted to be exactly one `\n` BEFORE writing;
  post ends in exactly one `\n`. Slice 8385 bytes, sha256 `2438a28cece5…`.
- (b) STRUCTURAL, computed independently of (a) by splitting the WHOLE image on
  `\n{2,}`: N counted by my script from the slice's own paragraphs = 2; units 699 →
  701, delta 2; the last 2 units equal the slice's paragraphs in order; the units
  before are an unchanged prefix.
- (c) NEGATIVE CONTROL, in memory on a `bytes` object, never on disk: offset 1109732
  asserted to lie inside the FIRST appended paragraph, one bit flipped — reader (a)
  rejected AND reader (b) rejected; restored, both accepted, and the restored image
  equalled the disk image.
- (d) COUNTS before → after C2, every one exactly as ordered:

| reading | ordered | measured |
|---|---|---|
| `^- R-\d{4} — ` distinct ids | 303 → 304 | 303 → 304 |
| `^Done: R-\d{4} — ` distinct | 247 → 247 | 247 → 247 |
| open set BY DISTINCT ID | 56 → 57 | 56 → 57 |
| `^Gate: ` | 31 → 32 | 31 → 32 |
| `^Gate: F272 R9 ` | 0 → 1 | 0 → 1 |
| `^- R-0820 — ` | 0 → 1 | 0 → 1 |

### G3 THE PLAN at C1, AND THE FEATURE FILE at C3 — exit 0

Plan: `.agent/plan.md` equals the PLANF272R10 slice bytes exactly. Both byte lengths
2173. 43 lines against the AGENTS.md cap of 50. `## Goal` present, `## Next Steps`
present.

Feature file: readers (a) and (b), no negative control (gate budget). Pre 27130 →
post 30008; prefix, append arithmetic and terminal newline all TRUE; N counted 6,
units 57 → 63, last 6 units equal the slice's paragraphs in order. Lines matching
`^### DECISION F272 D\d+ ` counted by me: 6 before, 7 after, naming in order
D1 D2 D3 D4 D5 D6 D7.

### G4 THE RENAME IS COMPLETE — a gate that CAN fail, and was shown to fail

All of G4 ran in the disposable worktree `.remedy-wt/f272-r10-gate` at commit
`868ba410`, the commit C6 creates.

**(ii) THE NON-VACUITY CONTROL, run FIRST.** One inventory site was reverted to
`.status` — `packages/orchestration/self_use_findings.py:51`, a PRODUCTION site,
sha256 `2dc0caee…51c6fb` → `a6cc5f50…3b60e2`. Then the ordered command:

    python3 -B -m pytest tests/orchestration/ tests/cli/ -q -p no:randomly
    EXIT = 1 — 2 failed, 14382 passed, 10 skipped in 999.86s

The site log named the reverted site and nothing else that is not the instrument
itself:

| logged site | times | what it is |
|---|---|---|
| `packages/orchestration/self_use_findings.py:51` `[describe_self_use_run_defects]` | 2 | the reverted site, named exactly |
| `tests/orchestration/test_job_state_field.py:45` | 1 | C6's own absence assertion — see Deviation 6 |

Both failures were the two tests that read that line. Restored: sha256 back to
`2dc0caee…51c6fb`, byte-identical, and `git status --porcelain` for that path empty.

**(i) THE RESIDUAL PROBE.** Same worktree, same probe, nothing reverted:

    python3 -B -m pytest tests/orchestration/ tests/cli/ -q -p no:randomly
    EXIT = 0 — 14384 passed, 10 skipped in 1053.97s

Site log: ONE entry, `tests/orchestration/test_job_state_field.py:45`, C6's own
assertion that the old name is gone. No production site and no other test site
appears. Both readings are reported because an empty log with a red run proves
nothing: here the log is free of every site that is not the instrument observing
itself, AND the run is EXIT 0.

**(iii) THE FIELD.** `packages.orchestration.pingpong_job.__file__` printed first and
read `/home/decodeux/Repos/remedy/.remedy-wt/f272-r10-gate/packages/orchestration/pingpong_job.py`.
Then `"state" in JobPlan.__dataclass_fields__` TRUE, `"status" in …` FALSE. The base
at `027bdc2c` is the exact inverse, measured by parsing the base blob out of git:
`status` present TRUE, `state` present FALSE.

**(iv) THE STORED KEY DID NOT MOVE.** For `JobPlan(job_id="g1", state=JOB_BLOCKED)`,
`_export_job` has key `"status"` valued `'blocked'` and NO key `"state"`.
`_import_job({"job_id": "g1", "status": "blocked"})`, a dict with no `"state"` key,
returns a JobPlan whose `state` is `'blocked'`.

**(v) NOTHING WAS RETYPED.** `type(JobPlan().state).__name__` is `str`;
`isinstance(JobPlan().state, RunState)` is FALSE.

### G5 MUTATION RED-PROOF — exit codes, one per mutation

Same worktree at `868ba410`, probe removed, `__pycache__` purged before every run,
`pingpong_job` confirmed resolving from inside the worktree. Target sha256
`a5227241…c04fc653`.

    UNMUTATED CONTROL   EXIT = 0 | 9 passed in 0.29s

| mutation | occurrences of the byte string in the target | mutated EXIT | restored byte-identical | control re-run EXIT |
|---|---|---|---|---|
| 1 the dataclass field `state` goes back to `status` | 1 | 1 (`9 failed`) | yes | 0 (`9 passed`) |
| 2 the exporter writes the key `"state"` instead of `"status"` | 1 | 1 (`3 failed, 6 passed`) | yes | 0 (`9 passed`) |
| 3 the importer reads `data.get("state", …)`, the old-record path | 1 | 1 (`2 failed, 7 passed`) | yes | 0 (`9 passed`) |

Mutation 2 needed a three-line anchor because `"status": job.state,` occurs TWICE in
`pingpong_job.py` (the exporter at 667 and a report builder at 2968) and §3 item 25
requires the mutated byte string to be unique; the anchor used carries the preceding
`"job_workspace_path"` and `"job_title"` lines and occurs exactly once.

### G6 THE SUITES at C6 — run SERIALLY, each its own invocation

Run in the gate worktree at `868ba410` (Deviation 9), `__pycache__` purged before each.

| invocation | exit | summary line |
|---|---|---|
| `tests/orchestration/test_job_state_field.py` | 0 | `9 passed in 0.24s` |
| `tests/orchestration/` | 0 | `12847 passed, 10 skipped, 1 warning in 750.73s (0:12:30)` |
| `tests/docs/` | 0 | `303 passed in 0.66s` |
| `tests/cli/` | 0 | `1537 passed in 293.41s (0:04:53)` |
| `tests/cli/test_golden_path.py` (THE CANARY) | 0 | `42 passed in 21.20s` |

Against the block's base at `027bdc2c` — `tests/orchestration/` 12838 and 10 skipped,
`tests/docs/` 303, `tests/cli/` 1537, canary 42. No count is lower anywhere, and
`tests/orchestration/` ROSE by exactly 9, which is C6's test count.

### G7 LINT AND INTEGRITY at C6 — ruff EXIT 1, integrity EXIT 0

`python3 -m ruff check` over exactly the 36 `.py` files this round changed, in ONE
invocation:

    EXIT = 1
    I001 [*] Import block is un-sorted or un-formatted
        --> tests/orchestration/test_predictive_budget.py:1127:9
    Found 1 error.

THIS IS PRE-EXISTING AND NOT THIS ROUND'S, proven rather than asserted: the base blob
`027bdc2c:tests/orchestration/test_predictive_budget.py` was written to a scratch path
and linted on its own, and reads the same `I001` at the same import block, `Found 1
error.`, EXIT 1. This round's five edits in that file are at lines 744, 766, 785, 801
and 909; the finding is at 1127. I fixed nothing: the repair is unrelated to the
change set and AGENTS.md forbids the "while I'm here" edit. The scratch path
`/home/decodeux/Repos/remedy/.remedy-wt/base_lint_probe` was removed BY EXACT PATH
afterwards. The repo-wide `ruff check .` was correctly NOT run (EXIT 1 on base under
open R-0468).

`python3 -m apps.cli.grouped integrity check --json`: EXIT 0, `"passed": true`,
`"fail_count": 0`, over 5 checks.

### G8 THE TREE — exit 0

- `git status --porcelain` EMPTY when C7 is staged.
- `git ls-files .remedy-wt` EMPTY.
- `git worktree list`: two worktrees were created and both removed BY EXACT PATH and
  pruned — `/home/decodeux/Repos/remedy/.remedy-wt/f272-r10-probe` and
  `/home/decodeux/Repos/remedy/.remedy-wt/f272-r10-gate`. Never by glob. Only the
  twelve pre-existing `remedy/job-*` entries remain, exactly as before.
- Per-commit insertions from `git diff --numstat <parent> <commit>`, each
  single-parent, each under the DECISION F104 D1 cap of 500, each matching the
  `## Commits` table above cell for cell:

| commit | item | parents | `+` | `-` | ≤500 | matches `## Commits` |
|---|---|---|---|---|---|---|
| `31c4ed95` | C0a | 1 | 400 | 0 | yes | yes |
| `33ecf575` | C0b | 1 | 307 | 307 | yes | yes |
| `cdab7fbe` | C1 | 1 | 14 | 14 | yes | yes |
| `6b679548` | C2 | 1 | 4 | 0 | yes | yes |
| `c1597759` | C3 | 1 | 42 | 0 | yes | yes |
| `e869aad9` | C4 | 1 | 380 | 0 | yes | yes |
| `f4136d24` | C5 | 1 | 234 | 234 | yes | yes (35 rows) |
| `868ba410` | C6 | 1 | 90 | 0 | yes | yes |

C7 is excluded by §3 item 14: it cannot count its own insertions.

- Marker sweep, counted by me, lines beginning `<<<BEGIN ` or `<<<END ` in every
  written non-block file: `.agent/plan.md` 0, `.agent/live_review.md` 0,
  `docs/roadmap/features/T2_F272.md` 0, `.agent/f272_state_rename_inventory.md` 0,
  `tests/orchestration/test_job_state_field.py` 0.

- The three `.agent/STOP` readings of constraint 8, each by `os.path.exists`:

| when | `.agent/STOP` exists |
|---|---|
| before C0a | False |
| before C5 | False |
| before C7 | False |

### C5's change set beyond the seventeen the block named

All seventeen named files were changed. EIGHTEEN more were, each with the evidence
that put it there. Per the block, a file the probe named is INSIDE the change set.

| file | the evidence that put it there |
|---|---|
| `packages/orchestration/run_manifest.py` | probe named `:6509`, `getattr(job, "status", "")` in `_job_is_resumable`, 39 hits |
| `packages/orchestration/self_use_runner.py` | probe named `:127`, `plan.status` in `run_next_self_use_item`, 10 hits |
| `tests/cli/test_job_stop.py` | probe named 5 WRITE sites — 91, 105, 142, 152, 197 |
| `tests/orchestration/test_budget_guard.py` | probe named the constructor at `:779`, keyword at `:781`, 6 hits |
| `tests/orchestration/test_episode_snapshot_lifecycle.py` | probe named 6 sites — 85, 86, 91, 119, 143, 164 |
| `tests/orchestration/test_final_audit_evidence.py` | 14 tests here went RED with an EMPTY probe log after the first application of C5 — the signature of an unfound STAND-IN; three were found by reading: `_FakeJob` and two `FakePlan` classes |
| `tests/orchestration/test_job_promote_consistency.py` | probe named `:89`, 34 hits |
| `tests/orchestration/test_job_stop_integration.py` | probe named 25 sites, plus `/tmp/…/runner.py:31` — a GENERATED script whose source template is `:457` |
| `tests/orchestration/test_job_worktree_integration.py` | probe named 6 sites — 124, 140, 161, 232, 261, 270 |
| `tests/orchestration/test_job_worktree_integrity.py` | probe named 8 sites, two of them writes |
| `tests/orchestration/test_pingpong_integration.py` | probe named `:145`; the `FakeJob` stand-in at 237-239 is the double for `do_cmd.py:1892` |
| `tests/orchestration/test_predictive_budget.py` | probe named 5 sites — 744, 766, 785, 801, 909 |
| `tests/orchestration/test_run_manifest_episode_graph.py` | the `_J` stand-in at `:219`, the double this file passes to `_crosscheck_job_episodes_vs_index`, whose `getattr` this round renamed |
| `tests/orchestration/test_run_manifest_reference_coverage.py` | probe named `:145` |
| `tests/orchestration/test_run_manifest_terminal_consistency.py` | the `_Job` stand-in at `:17`, the double this file passes to `_crosscheck_terminal_jobplan_manifest` |
| `tests/orchestration/test_run_manifest_zero_call_expectations.py` | probe named `:213` |
| `tests/orchestration/test_self_use_runner.py` | probe named `:99` and `:281` |
| `tests/test_do_job_flow.py` | the `_FakeJob` stand-in at `:1198`, the double for `_build_final_audit`. It lives OUTSIDE BOTH ordered suites and was found only by running the probe over the REST of `tests/` (Deviation 3) |

## External actions

| action | outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f272-r10-probe 027bdc2c` | created at `027bdc2c` |
| `git worktree remove --force .remedy-wt/f272-r10-probe` | removed by exact path |
| `git worktree add --detach .remedy-wt/f272-r10-gate 868ba410` | created at `868ba410` |
| `git worktree remove --force .remedy-wt/f272-r10-gate` | removed by exact path |
| `git worktree prune` | run after the removals |
| `git push -u origin feature/f272-one-world-completion` | see below |

No PR created, none merged, nothing force-pushed, no branch deleted.

## Authored-text proofs

Disk-to-disk against the committed `.agent/authored/f272-r10.md`:

| slice | target | bytes | mode | result | sha256 |
|---|---|---|---|---|---|
| PLANF272R10 | `.agent/plan.md` | 2173 | replace | IDENTICAL | `a99735caf764…` |
| RECORDR10 | `.agent/live_review.md` | 8385 | append | IDENTICAL | `2438a28cece5…` |
| DECISIONR10 | `docs/roadmap/features/T2_F272.md` | 2877 | append | IDENTICAL | `7198c0f95720…` |

Every slice was applied byte for byte, none was edited, and no `<<<BEGIN`/`<<<END`
marker LINE reached any target file. (`.agent/live_review.md` contains one INLINE
`<<<BEGIN ` occurrence mid-line; it is in the pre-image at `HEAD~`, is not a marker
line, and the line-anchored count is 0 before and after.) C4, C5 and C6 were a SPEC
and not a slice, so they carry no authored text.

## Deviations & assumptions

NO COMMIT WAS MADE BEYOND THE BLOCK'S ORDERED SEQUENCE. The fix clause OPEN in the
record and binding on this handback — that any commit beyond the ordered sequence
receives its OWN `## Commits` row and its OWN item-status row, and the Deviations
section says so in those same words — is discharged with nothing owed: the range
`027bdc2c..HEAD` holds exactly eight commits before this handoff, they are C0a, C0b,
C1, C2, C3, C4, C5 and C6 in that order, and no row beside this one says otherwise.

### Deviation 1 — the probe got a second MODE the block did not order

C4 step 2 orders a `status` property that logs the caller and RAISES. I built that,
and I also gave it a `forward` mode that logs and then forwards to `state`. Reason,
measured rather than assumed: under the raising probe alone, `_export_job:667` fires
on nearly every job in the suite, so each test dies at its FIRST site and the rest of
that test's sites stay invisible — the first raising pass logged 40 distinct sites
against 766 failures. One forwarding pass logged 218. The forwarding pass is an
ACCELERATOR only; every claim in this round rests on the RAISING probe, which is what
G4 re-ran and what had to reach EXIT 0.

### Deviation 2 — the probe also instruments the CONSTRUCTOR

A property cannot see `JobPlan(status=...)`: after the field is renamed that path
raises `TypeError` from the generated `__init__` and never reaches a descriptor. I
wrapped `JobPlan.__init__` so a `status=` keyword is logged with its caller and then
raises (or, in forward mode, is forwarded). Without this the 36 constructor sites
would have had to be inferred statically, which is the thing D7 forbids. All 36 were
in fact named by the running probe.

### Deviation 3 — the probe was ALSO run over the rest of `tests/`

The block orders `tests/orchestration/ tests/cli/`. I additionally ran
`tests/ --ignore=tests/orchestration --ignore=tests/cli` under the probe, twice. It
named one further site — `apps/cli/commands/do_cmd.py:2885` — and, once C5 was
applied, it is what exposed the `_FakeJob` stand-in in `tests/test_do_job_flow.py`,
which no ordered suite reaches. Had I run only the two ordered suites, this round
would have landed a file that is silently wrong and gated it EXIT 0.

### Deviation 4 — `node_modules` was symlinked into both worktrees

Round 9 recorded `test_test_runner.py::…::test_vitest_passes` as an unavoidable
worktree artifact (`ERR_MODULE_NOT_FOUND`, a fresh worktree has no `node_modules`)
and excluded it from its count. That exclusion is not necessary: the primary checkout
has `node_modules` and `apps/ui/node_modules`, and symlinking both into the worktree
makes the test pass there — verified before any edit, `52 passed in 4.05s` for that
file. This is environment provisioning, not a source change, and it is what makes an
honest EXIT 0 reachable inside a worktree at all.

### Deviation 5 — the scaffolding was made lint-clean so it stops tripping a test

With the site set fully applied, the ordered command still read EXIT 1 on exactly one
test: `test_ci_budgets.py::test_this_repository_really_is_at_or_below_the_lint_ceiling`.
`python3 -m ruff check` on the worktree's `pingpong_job.py` showed the cause was the
SCAFFOLDING — two `E402` and one `UP031` from my own probe block, three errors over a
ceiling of 26. I rewrote the scaffolding (imports inside functions, an f-string
instead of `%`) until `ruff` read `All checks passed!` on that file, and the same
ordered command then read EXIT 0. No test was changed, no assertion weakened and no
ceiling raised; the instrument was fixed, not the measurement. The scaffolding never
reaches a commit — the diff C5 landed was produced from a tree with the probe removed.

### Deviation 6 — G4's site log is NOT empty, and cannot be

G4(i) requires an EMPTY site log. The log carries exactly one entry:
`tests/orchestration/test_job_state_field.py:45`, which is C6's own assertion
`assert not hasattr(JobPlan(), "status")` — the assertion that makes the rename a
REPLACEMENT rather than an alias. Under the probe an artificial `status` property
exists, so that assertion reads it and is logged; it still PASSES, because the getter
raises `AttributeError` and `hasattr` is therefore False. This is not a site C5
missed: it is the gate's own instrument being observed by the test whose subject is
the instrument's absence. I could not formulate the assertion to satisfy both: any
INSTANCE-level check logs, and any CLASS-level check (`"status" in dir(JobPlan)`,
`JobPlan.__dict__`, `getattr(JobPlan, "status", None)`) FAILS under the probe, which
would redden G4 instead. I applied the block as written and report the log verbatim
rather than trimming it, excluding it by name, or deleting the assertion. The
reviewer may prefer the assertion dropped; that is a ruling, not my call.

### Deviation 7 — G7's ruff is EXIT 1 on a pre-existing finding

Reported above with its base proof. Not fixed: out of the change set's substance and
untouched by any of this round's edits.

### Deviation 8 — two tests are RED AT BASE, outside every ordered suite

`tests/ui_contracts/test_digest_card_copy.py::TestEveryRunStateIsAccountedFor::test_all_seven_run_states_are_named_by_the_label_map`
and
`tests/ui_contracts/test_job_digest_card_contract.py::TestTheTriggerRuleIsPureAndPortless::test_all_seven_run_states_are_accounted_for_in_the_rule`
fail at `027bdc2c`. I reproduced both RED in the UNMODIFIED primary checkout before
any edit of this round, so they are not a rename effect. Both concern "all seven run
states", which is what round 8 widened. They lie outside `tests/orchestration/`,
`tests/cli/`, `tests/docs/` and the canary, so no gate this round orders can see
them. I mint no id; registering this is the reviewer's call.

### Deviation 9 — G4, G5 and G6 ran in the gate worktree, not the primary checkout

The block places G4 and G5 in a disposable worktree at the commit C6 creates. I ran
G6 there too, at that same commit `868ba410`, so that no suite run could leave an
artifact in the primary checkout and put G8's `git status --porcelain` at risk. The
worktree's content is the committed tree; `pingpong_job.__file__` was printed and
resolves from inside it. G7 and G8 ran in the primary checkout.

### Deviation 10 — the inventory uses a fourth classification

C4 step 6 names `probe`, `annotation` and `stand-in`. The inventory carries a fourth,
`field`, used once, for the dataclass field itself — it is neither a call site nor a
double, and calling it any of the three would have been a small lie in the one row
that anchors all the others. `probe` covers 219 sites, `annotation` 5, `stand-in` 9.

### Deviation 11 — two stand-ins keep their `status` KEYWORD

`_Job` in `test_run_manifest_terminal_consistency.py` and `_J` in
`test_run_manifest_episode_graph.py` build their attribute from a keyword their own
callers pass. I renamed the ATTRIBUTE (`self.state = kw.get("status", …)`) and left
the keyword, because the keyword is the double's own local API and renaming it would
have pulled unrelated call sites into a rename commit that must stay atomic.

### Assumption

The forwarding pass and the raising pass see the same site set. Basis rather than
belief: after applying everything the forwarding pass named, the RAISING pass over
the same suites reached EXIT 0 with no production site logged, and the non-vacuity
control proves that same instrument does fire when a site is put back.

## Next

The reviewer re-runs these gates and rules on round 10. The three readings that most
need an independent re-run are G4's control/residual pair (the gate R-0820 exists to
replace), G6's `tests/orchestration/` count of 12847 against the base 12838, and
G7's ruff, which is EXIT 1 for a reason this round did not create. Then move THREE of
DECISION F272 D6: retype `JobPlan.state` to `RunState`, make the six `JOB_*`
constants `RunState` members, and put `.value` at every boundary leaving the record —
`tests/orchestration/test_job_state_field.py::TestTheRenderingIsUnchanged` is the
guard that move must keep green, and `.agent/f272_state_rename_inventory.md` is the
site list it inherits. Phase 1 rule 1 (`.agent/STOP`) is checked before Phase 1
rule 2, as always.
