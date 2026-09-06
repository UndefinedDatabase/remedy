# Handoff — F272 One world completion, round 9

## Session

SESSION 4 of feature F272 · round 9 · rounds so far 9

Context self-assessment (amend0905-throughput): context is comfortable — this
round spent most of its budget on measurement rather than on writing, and a
further round in this session is affordable.

**ROUND 9 STOPPED AT C4 UNDER SELF-DRIVE GUARDRAIL G8.** C0a, C0b, C1, C2 and C3
landed exactly as ordered. C4 and C5 did NOT land: the block's change set cannot
produce a correct rename, and this is proved by measurement below rather than
argued. C6 is this handoff.

## Range

Review of `c1c8f76d`..`HEAD` (branch `feature/f272-one-world-completion`).

## Commits

### 47b3dc51 f272: save the round 9 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f272-r9.md` | +400 / -0 | C0a, `shutil.copyfile` of the reviewer's scratch original |

### 6c347d80 f272: mirror the round 9 step block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +316 / -316 | C0b, byte copy of the same original |

### fc989cd2 f272: set the plan to the round 9 rename step
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +22 / -23 | C1, replaced by the PLANF272R9 slice |

### 1dfb201d f272: book the round 8 gate entry and the D5 site-figure slip
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2 / -0 | C2, RECORDR9 appended |
| `.agent/prose_slips.md` | +2 / -0 | C2, SLIPSR9 appended |

### 7a3c8c44 f272: rule the state collapse as three moves in DECISION F272 D6
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T2_F272.md` | +40 / -0 | C3, DECISIONR9 appended |

### C6 — this handoff
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | self-referential | C6 cannot table the commit that writes it (R-0149 pattern) |

NO COMMIT WAS MADE BEYOND THE BLOCK'S ORDERED SEQUENCE. Two ordered commits, C4
and C5, are absent; the reason is Deviation 1.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | `.agent/authored/f272-r9.md`, byte copy |
| C0b | done | `.agent/last_block.md`, byte copy |
| C1 | done | plan replaced by the slice, byte-equal |
| C2 | done | both appends, every G2 count as ordered |
| C3 | done | DECISION F272 D6 appended |
| C4 | skipped | the block's change set cannot produce a correct rename — measured, Deviation 1 |
| C5 | skipped | C5 pins the field C4 was to rename; without C4 there is nothing to pin |
| C6 | done | this handoff |

## Verification

Raw readings per gate. One line per gate with its REAL exit code, then the
transcripts. "Green" as a word appears nowhere.

| Gate | Exit | Reading |
|---|---|---|
| G1 TRANSPORT | 0 | three artefacts, all 29054 bytes, all sha256 `08eb65d9…b237d27` |
| G2 THE RECORD | 0 | readers (a)(b)(c)(d) all accept; every ordered count matched |
| G3 PLAN + FEATURE FILE | 0 | plan byte-equal at 2143 B / 43 lines; feature file readers accept |
| G4 THE RENAME | NOT REACHED | C4 absent. Base readings re-measured and reproduce the block exactly |
| G5 MUTATION RED-PROOF | NOT RUN | depends on C5, which depends on C4 |
| G6 THE SUITES | 0 where reachable | `tests/docs/` EXIT 0, `tests/cli/test_golden_path.py` EXIT 0 |
| G7 LINT AND INTEGRITY | 0 | no `.py` file changed, so ruff's ordered file set is empty; integrity EXIT 0 |
| G8 THE TREE | 0 | tree empty, `git ls-files .remedy-wt` empty, both probe worktrees removed |

### G1 TRANSPORT — a real three-artefact chain

Per §3 item 37 this covers the saved copy and its mirror, not the bytes emitted
into the prompt.

| Artefact | Bytes | sha256 |
|---|---|---|
| `.remedy-wt/f272-r9-block.md` (reviewer's surviving original) | 29054 | `08eb65d964918f29c3fcd673c46a389895a3ae6f1bb6161e98219c498b237d27` |
| `.agent/authored/f272-r9.md` (C0a) | 29054 | same |
| `.agent/last_block.md` (C0b) | 29054 | same |

All three equal each other and equal the delegation's BLOCK_SHA and BLOCK_LENGTH.
BLOCK_LINES read 400 and matched. Verified BEFORE any other action.

### G2 THE RECORD — exit 0

`.agent/live_review.md`, readers (a) to (d):
- (a) BYTE: pre 1104989 → post 1109691; pre a byte-exact prefix; `post == pre +
  b"\n" + slice` TRUE; pre's terminal byte exactly one `\n` asserted before
  writing; post ends in exactly one `\n`.
- (b) STRUCTURAL, computed independently of (a): N counted by the script from the
  slice's own paragraphs = 1; units 698 → 699, delta 1; the last N units equal
  the slice's paragraphs in order; the units before are an unchanged prefix.
- (c) NEGATIVE CONTROL, in memory on a `bytes` object, never on disk: offset
  1105030 asserted to lie inside the first appended paragraph, one bit flipped —
  reader (a) rejected and reader (b) rejected, BOTH; restored, both accepted, and
  the restored image equalled the disk image.
- (d) COUNTS before → after: registrations 303 → 303, resolutions 247 → 247, open
  set BY DISTINCT ID 56 → 56, `^Gate: ` 30 → 31, `^Gate: F272 R8 ` 0 → 1. Every
  one exactly as ordered; the first three unchanged because this round mints no id.

`.agent/prose_slips.md`, readers (a) and (b): pre 135900 → post 136942; prefix,
append arithmetic and terminal-newline all TRUE; N counted 1, units 173 → 174,
last unit equals the slice paragraph, prefix unchanged.

### G3 THE PLAN at C1, AND THE FEATURE FILE at C3 — exit 0

Plan: `.agent/plan.md` equals the PLANF272R9 slice bytes exactly. Both byte
lengths 2143. 43 lines against the AGENTS.md cap of 50. `## Goal` present,
`## Next Steps` present.

Feature file: readers (a) and (b), no negative control (gate budget). Pre 24461 →
post 27130; prefix, append arithmetic, terminal newline all TRUE; N counted 7,
units 50 → 57, last 7 units equal the slice's paragraphs in order. Lines matching
`^### DECISION F272 D\d+ ` counted by this worker: 5 before, 6 after, naming in
order D1 D2 D3 D4 D5 D6.

### G4 — base readings reproduce the block exactly; the post-C4 half is unreachable

Measured by importing the shipped module, `__file__` =
`/home/decodeux/Repos/remedy/packages/orchestration/pingpong_job.py`, and by
`ast` over the 1065 tracked `.py` files from `git ls-files`.

(i) THE FIELD, at this tree: `"state" in JobPlan.__dataclass_fields__` FALSE,
`"status" in …` TRUE — exactly the block's stated base at `c1c8f76d`.

(ii) THE SWEEP, the four scoped counts:

| reading | block's base at `c1c8f76d` | measured now at `7a3c8c44` | required after C4 | actual after C4 |
|---|---|---|---|---|
| INSIDE the twenty, `.status` | 86 | **86** | 0 | not reached |
| INSIDE the twenty, `.state` | 11 | **11** | 97 | not reached |
| OUTSIDE them, `.status` | 4 | **4** | 4 | not reached |
| OUTSIDE them, `.state` | 125 | **125** | 125 | not reached |

Every base reading reproduces. The per-file `<job>.status` counts also reproduce
the block's twenty-row table cell for cell, and the `JobPlan(...)` `status=`
keyword total reproduces at 36 across the 5 named files (28/9/7/6/5/4/4/4/3/3/3/
3/2/2/1/1/1/0/0/0 summing to 86; kwargs 4+1+5+3+23 = 36; 86 + 36 = 122).

The four OUTSIDE `.status` survivors, BY PATH AND LINE, and what each receiver
actually is — every one verified by reading its source, and the block's
classification of all four is CORRECT:

| site | receiver's real type |
|---|---|
| `tests/orchestration/test_autonomy.py:978` | `StopReason` (`get_stop_reason`) |
| `tests/orchestration/test_dogfood_run.py:164` | `DogfoodRun` (`load_dogfood_run`) |
| `tests/orchestration/test_dogfood_run.py:373` | `DogfoodRun` (`load_dogfood_run`) |
| `tests/orchestration/test_self_repair_proposal.py:414` | `SelfRepairProposal` |

(iii) THE STORED KEY, at this tree: `_export_job` on a job whose lifecycle value
is `JOB_BLOCKED` has key `"status"` with value `'blocked'` and has no key
`"state"`; `_import_job({'job_id':…, 'status':'blocked'})` returns that value.

(iv) NOTHING WAS RETYPED, at this tree: `type(...).__name__` is `str`,
`isinstance(..., RunState)` is FALSE, default `'planned'` == `JOB_PLANNED`.

### G5 — NOT RUN

G5 mutates the file C5 creates. C5 did not land, so there is nothing to mutate
and no exit code to report. Reporting a colour here would be a fabrication.

### G6 — the reachable suites, run serially, each its own invocation

| suite | exit | summary |
|---|---|---|
| `tests/docs/` | 0 | `303 passed in 0.49s` — the block's measured 303, unchanged |
| `tests/cli/test_golden_path.py` (canary) | 0 | `42 passed in 22.42s` — the block's measured 42, unchanged |

`tests/orchestration/` and `tests/cli/` are ordered by the block AT C5. No `.py`
file changed in this round's landed commits, so neither suite is reachable as a
gate on the landed tree; both WERE run against the block-as-written tree in a
disposable worktree, and that measurement is Deviation 1's evidence below.

### G7 — exit 0

`python3 -m ruff check` over exactly the `.py` files this round changed: this
round changed ZERO `.py` files, so the ordered one-invocation file set is empty
and there is nothing to lint. Stated rather than dressed up as a pass. The
repo-wide `ruff check .` was correctly NOT run (EXIT 1 on base under open R-0468).

`python3 -m apps.cli.grouped integrity check --json`: EXIT 0, `"passed": true`,
`"fail_count": 0`, over 5 checks.

### G8 THE TREE — exit 0

- `git status --porcelain` EMPTY when C6 is staged.
- `git ls-files .remedy-wt` EMPTY.
- `git worktree list`: two worktrees were created and both removed BY EXACT PATH
  and pruned — `/home/decodeux/Repos/remedy/.remedy-wt/f272-r9-probe` and
  `/home/decodeux/Repos/remedy/.remedy-wt/f272-r9-probe2`. Never by glob. Only
  the twelve pre-existing `remedy/job-*` entries remain, exactly as before.
- Per-commit insertions from `git diff --numstat <parent> <commit>`, each
  single-parent, each under the DECISION F104 D1 cap of 500, and each matching
  the `## Commits` table above cell for cell:

| commit | parents | `+` | `-` | ≤500 | matches `## Commits` |
|---|---|---|---|---|---|
| `47b3dc51` C0a | 1 | 400 | 0 | yes | yes |
| `6c347d80` C0b | 1 | 316 | 316 | yes | yes |
| `fc989cd2` C1 | 1 | 22 | 23 | yes | yes |
| `1dfb201d` C2 | 1 | 4 | 0 | yes | yes (2 + 2) |
| `7a3c8c44` C3 | 1 | 40 | 0 | yes | yes |

C4 and C5 have no row because they do not exist. C6 is excluded by §3 item 14.

- Marker sweep, counted by this worker, lines beginning `<<<BEGIN ` or `<<<END `
  in every written non-block file: `.agent/plan.md` 0, `.agent/live_review.md` 0,
  `.agent/prose_slips.md` 0, `docs/roadmap/features/T2_F272.md` 0.

- The three `.agent/STOP` readings of constraint 9, each by `os.path.exists`:

| when | `.agent/STOP` exists |
|---|---|
| before C0a | False |
| before C4 | False |
| before C6 | False |

## External actions

| action | outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f272-r9-probe HEAD` | created at `7a3c8c44` |
| `git worktree remove --force .remedy-wt/f272-r9-probe` | removed by exact path |
| `git worktree add --detach .remedy-wt/f272-r9-probe2 HEAD` | created at `7a3c8c44` |
| `git worktree remove --force .remedy-wt/f272-r9-probe2` | removed by exact path |
| `git worktree prune` | run after each removal |
| `git push -u origin feature/f272-one-world-completion` | see below |

No PR created, none merged, nothing force-pushed, no branch deleted.

## Authored-text proofs

Disk-to-disk against the committed `.agent/authored/f272-r9.md`:

| slice | target | bytes | mode | result |
|---|---|---|---|---|
| PLANF272R9 | `.agent/plan.md` | 2143 | replace | IDENTICAL, sha256 `a8586da3…3c64afb` |
| RECORDR9 | `.agent/live_review.md` | 4701 | append | IDENTICAL, sha256 `8046732a…670dfdc1` |
| SLIPSR9 | `.agent/prose_slips.md` | 1041 | append | IDENTICAL, sha256 `d4644f26…600c04164e` |
| DECISIONR9 | `docs/roadmap/features/T2_F272.md` | 2668 | append | IDENTICAL, sha256 `b898f444…5fcc809e5` |

Every slice was applied byte for byte, none was edited, and no `<<<BEGIN`/`<<<END`
marker line reached any target file. C4 and C5 were a SPEC and not a slice, so
they carry no authored text.

## Deviations & assumptions

### Deviation 1 — C4 AND C5 DID NOT LAND. The block's change set cannot produce a correct rename.

This is the round's whole substance, so it is stated with both readings.

**The block's rule.** C4 identifies the rename set as 122 sites in twenty files:
86 `<job>.status` attribute sites whose receiver is a bare `Name` in
(`job`, `plan`, `job_plan`, `jp`, `loaded`, `reloaded`, `j`, `resumed`), plus 36
`status=` keyword arguments in `JobPlan(...)` calls. Constraint 2 makes those
twenty paths "the whole change set".

**What I measured.** That receiver-Name rule is not a classification of what the
receiver IS; it is a classification by NAME, which is the thing the delegation
told me never to do. It is wrong in both directions:

- IT MISSES REAL `JobPlan.status` SITES. A receiver-TYPE pass — a name is
  JobPlan-bound when it is annotated `JobPlan` or assigned from a JobPlan
  producer (`JobPlan(…)`, `load_job_plan`, `_import_job`, `parse_job_file`,
  `plan_job_from_file`, `run_job`, `resume_job_plan`, `_stop_job`) — finds at
  least 94 further sites the Name set does not reach, including in PRODUCTION
  code outside the twenty. The clearest single example, read from source:
  `packages/orchestration/self_use_findings.py:51`, inside
  `def describe_self_use_run_defects(result: JobPlan)`, is `result.status`. The
  parameter is annotated `JobPlan`. That file is not in the twenty.
- IT ALSO MIS-CLASSIFIES AT LEAST ONE SITE IT DOES CLAIM.
  `apps/cli/commands/do_cmd.py:1892` is `job.status == "completed"`, a genuine
  production `JobPlan` read, but its test double `FakeJob` — declared at
  `tests/orchestration/test_pingpong_integration.py:237-239` with a `status: str`
  field — is structural and lives outside the twenty, so renaming the production
  read without the double raises `'FakeJob' object has no attribute 'state'`.

**The proof, not the argument.** I applied C4 EXACTLY as the block scopes it — the
twenty files, the block's own receiver set, the 36 kwargs, the dataclass field
`status: str = JOB_PLANNED` → `state: str = JOB_PLANNED`, annotation and default
untouched — in a disposable worktree at `7a3c8c44`, with `__pycache__` purged and
the module confirmed resolving from inside it
(`…/.remedy-wt/f272-r9-probe2/packages/orchestration/pingpong_job.py`). Then I ran
the suites the block's G6 orders:

    python3 -B -m pytest tests/orchestration/ tests/cli/ -q -p no:randomly
    EXIT 1 — 153 failed, 14222 passed, 10 skipped in 1029.00s

Against G6's requirement of EXIT 0 with `tests/orchestration/` at 12838 passed and
`tests/cli/` at 1537. An earlier `tests/orchestration/`-only run of the same tree
read EXIT 1, `137 failed, 12701 passed, 10 skipped in 749.95s`. Exactly one of
the 153 is unrelated to the rename: `test_test_runner.py::…::test_vitest_passes`
fails with `ERR_MODULE_NOT_FOUND`, the known "a worktree has no `node_modules`"
artifact. So 152 failures are caused by the rename as the block scopes it.

The 23 distinct failing files, with failure counts — this is the list round 10
needs, because it IS the correction to the change set:

| file | fails | in the block's twenty? |
|---|---|---|
| `tests/orchestration/test_job_promote_consistency.py` | 34 | NO |
| `tests/orchestration/test_job_task_runner.py` | 21 | yes |
| `tests/orchestration/test_job_stop_integration.py` | 20 | yes |
| `tests/orchestration/test_final_audit_evidence.py` | 14 | NO |
| `tests/orchestration/test_f018_authority_integration.py` | 13 | yes |
| `tests/cli/test_job_rerun_manifest.py` | 12 | yes |
| `tests/orchestration/test_job_worktree_integrity.py` | 5 | yes |
| `tests/orchestration/test_predictive_budget.py` | 5 | NO |
| `tests/cli/test_golden_path.py` (THE CANARY) | 4 | NO |
| `tests/orchestration/test_episode_snapshot_lifecycle.py` | 4 | yes |
| `tests/orchestration/test_job_worktree_handoff.py` | 4 | yes |
| `tests/orchestration/test_failure_wiring.py` | 2 | yes |
| `tests/orchestration/test_job_worktree_integration.py` | 2 | yes |
| `tests/orchestration/test_pingpong_integration.py` | 2 | NO |
| `tests/orchestration/test_self_use_findings.py` | 2 | NO |
| `tests/orchestration/test_self_use_runner.py` | 2 | NO |
| `tests/orchestration/test_f018_package_pipeline_e2e.py` | 1 | yes |
| `tests/orchestration/test_job_evidence.py` | 1 | NO |
| `tests/orchestration/test_run_manifest.py` | 1 | NO |
| `tests/orchestration/test_run_manifest_reference_coverage.py` | 1 | NO |
| `tests/orchestration/test_run_manifest_runtime_truth.py` | 1 | NO |
| `tests/orchestration/test_run_manifest_zero_call_expectations.py` | 1 | NO |
| `tests/orchestration/test_test_runner.py` | 1 | NO — `node_modules` artifact, not the rename |

Ten of the twenty files the block DOES name still fail after the rename it
specifies, so the receiver-Name rule is incomplete even inside its own file list.
Eleven further files, plus the production module
`packages/orchestration/self_use_findings.py`, are outside it entirely.

**Why I stopped instead of widening.** Constraint 2 says the listed paths are the
whole change set and the delegation says "C4 is ONE commit covering all twenty
files". A correct rename needs roughly 180 attribute sites across about 28 files —
not "a site this block does not name", which is what C4's escape clause covers,
but a re-scoping of the round, and re-scoping is the reviewer's to do, not mine.
Self-drive guardrail G8 says a contradiction ends the round with a clean handoff,
and AGENTS.md forbids "while I'm here" widening. The alternative was to commit a
tree I had already measured as 152 tests red, which no honest gate could pass.
I did not change any code to make any gate go green.

**The part that most needs the reviewer's attention.** On that same 152-red tree,
the block's own G4 reads FULLY GREEN. Measured in the probe worktree:

| G4(ii) reading | required after C4 | actually read on the broken tree |
|---|---|---|
| INSIDE the twenty, `.status` | 0 | **0** |
| INSIDE the twenty, `.state` | 11 → 97 | **97** |
| OUTSIDE them, `.status` | 4 | **4** |
| OUTSIDE them, `.state` | 125 | **125** |

and the four OUTSIDE survivors print as exactly the four named paths and lines.
G4(i), (iii) and (iv) pass there too. G4 counts only receivers in the same Name
set that defined the change set, so it cannot see any site that set missed: the
gate and the edit share one blind spot, and four of the block's eight gates
certify a tree with 152 failing tests. Only G6 catches it. I mint no finding id
and write no `Done:` paragraph — registering this is the reviewer's call.

### Deviation 2 — `.agent/plan.md` still describes the rename as this round's work.

Constraint 5 replaces the plan with exactly the PLANF272R9 slice, and G3 pins it
byte-for-byte; the slice says round 9 "renames `JobPlan.status` … at all 122 sites
in one commit". After Deviation 1 that sentence describes work that did not land.
AGENTS.md "If Blocked" would have me write the blocker into `.agent/plan.md`, but
editing it would break the G3 equality the block orders. I kept the slice byte-
exact and put the blocker here, in the handoff, which the protocol names as the
end-of-round carrier and which Phase 0 reads. Round 10's plan slice should
correct it. Flagged rather than silently resolved either way.

### Deviation 3 — G6's `tests/orchestration/` and `tests/cli/` were not run on the landed tree.

The block orders them at C5. C5 does not exist and no `.py` file changed, so they
gate nothing here. They were run on the block-as-written tree instead, which is
Deviation 1's evidence. `tests/docs/` and the canary WERE run on the landed tree
and are EXIT 0.

### Deviation 4 — G7's ruff invocation had an empty file set.

It is ordered over "exactly the `.py` files this round changed". That set is
empty, so the invocation was not made. Reported as an empty set rather than as a
pass.

### Assumption

`test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes` is
treated as a worktree artifact, not a rename effect. Basis: it fails with
`ERR_MODULE_NOT_FOUND` from `npx vitest run`, and a fresh `git worktree` has no
`node_modules`. It is excluded from the 152.

## Next

The reviewer re-runs these gates, rules on Deviation 1, and issues round 10's
block with a CORRECTED C4 change set — derived by receiver TYPE rather than by
receiver name, covering the roughly 28 files above including the production module
`packages/orchestration/self_use_findings.py` and the `FakeJob` double at
`tests/orchestration/test_pingpong_integration.py:237-239` — together with a G4
sweep that can actually fail when the rename is incomplete. Phase 1 rule 1
(`.agent/STOP`) is checked before Phase 1 rule 2, as always.
