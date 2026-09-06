# Handback — F272 round 6

## Session

SESSION 2 of feature F272 · round 6 · rounds so far 6

Context self-assessment (amend0905-throughput): context is comfortable — this
round spent most of its wall clock inside two multi-minute suites rather than
inside reading, and there is ample room for further rounds this session.

## Range

Review of `61c4bd2e`..`HEAD` (10 commits, C0a through C8).

## Commits

### a4063692 f272: save the round 6 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f272-r6.md` | +331/-0 | C0a, `shutil.copyfile` of the reviewer's scratch block |

### 0808ddc3 f272: mirror the round 6 step block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +280/-333 | C0b, same source, byte-identical mirror |

### f95245d3 f272: set the plan to round 6, the test half and the deletion
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +22/-25 | C1, REPLACED by the PLANF272R6 slice bytes |

### b26c010d f272: book the round 5 gate entry and the scope-rule prose slip
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-0 | C2, RECORDR6 appended |
| `.agent/prose_slips.md` | +2/-0 | C2, SLIPSR6 appended |

### 252b0d95 f272: move the seventeen unshadowed test files onto run_dir and runs_dir
| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_task_input.py` | +4/-4 | C3, shape A |
| `tests/orchestration/test_failure_postmortem.py` | +2/-2 | C3, shape A |
| `tests/orchestration/test_job_stop_integration.py` | +3/-3 | C3, shape A |
| `tests/orchestration/test_job_worktree_handoff.py` | +2/-2 | C3, shape A |
| `tests/orchestration/test_job_worktree_integration.py` | +3/-3 | C3, shape A |
| `tests/orchestration/test_job_worktree_integrity.py` | +2/-2 | C3, shape A |
| `tests/orchestration/test_persisted_call_episode_membership.py` | +2/-2 | C3, shape A |
| `tests/orchestration/test_persisted_call_ownership.py` | +2/-2 | C3, shape A |
| `tests/orchestration/test_persisted_run_call_schema.py` | +2/-2 | C3, shape A |
| `tests/orchestration/test_pingpong_cli.py` | +5/-5 | C3, shape A |
| `tests/orchestration/test_run_manifest_ledger_semantics.py` | +2/-2 | C3, shape A |
| `tests/orchestration/test_run_manifest_task_lifecycle_binding.py` | +2/-2 | C3, shape A |
| `tests/orchestration/test_run_manifest_zero_call_expectations.py` | +2/-2 | C3, shape A |
| `tests/orchestration/test_stream_export_e2e.py` | +2/-2 | C3, shape A |
| `tests/orchestration/test_worktree_isolation.py` | +3/-3 | C3, shape A |
| `tests/orchestration/test_worktree_persistence.py` | +2/-2 | C3, shape A |
| `tests/orchestration/test_worktree_safety.py` | +4/-4 | C3, shape A |

### 6af5d04a f272: move test_pingpong_promote onto data_paths.run_dir at its twenty-three shadowing scopes
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_pingpong_promote.py` | +46/-46 | C4, shape B at all 23 scopes |

### 815f3a8d f272: move the seven mixed-shape test files, shape B at their eleven shadowing scopes
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_evidence_bundle.py` | +3/-3 | C5, shape B x3 |
| `tests/orchestration/test_failure_wiring.py` | +8/-8 | C5, shape A x7 + shape B x2 |
| `tests/orchestration/test_job_evidence.py` | +8/-8 | C5, shape B x8 |
| `tests/orchestration/test_manual_completion_bundle.py` | +2/-2 | C5, shape B x2 |
| `tests/orchestration/test_repair_loop.py` | +2/-2 | C5, shape B x2 |
| `tests/orchestration/test_worktree_lifecycle.py` | +2/-3 | C5, shape B x2, imports combined by ruff I001 |
| `tests/orchestration/test_worktree_resume_cli.py` | +2/-3 | C5, shape B x2, imports combined by ruff I001 |

### 98ab08b6 f272: delete the alias pin test and retarget the two stale failure messages
| Path | +/- | Reason |
|---|---|---|
| `tests/test_data_paths.py` | +2/-37 | C6, alias test deleted whole; two failure MESSAGES retargeted |

### d7ec5a68 f272: delete pingpong_runs_dir and pingpong_run_dir from data_paths
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/data_paths.py` | +0/-25 | C7, the two defs, the explanatory comment block, two module-docstring lines |

### C8 — the handback (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | — | C8, this file; a handoff cannot table the commit that writes it |

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1  | done | |
| C2  | done | |
| C3  | done | |
| C4  | done | |
| C5  | done | |
| C6  | done | (c) was vacuous — see deviations |
| C7  | done | |
| C8  | done | |

## External actions

| Action | Outcome |
|---|---|
| `git worktree add .remedy-wt/f272r6-base 61c4bd2e --detach` | created, for the read-only base measurement of G4(iii) |
| `git worktree remove .remedy-wt/f272r6-base` + `git worktree prune` | removed; `git worktree list` now shows only the primary checkout and the twelve pre-existing `remedy/job-*` entries |
| `git push -u origin feature/f272-one-world-completion` | pushed, 10 commits |
| PR create / merge | None. No PR created, none merged. |

## Verification

**G1 TRANSPORT — PASS.** Covers the SAVED COPY and its MIRROR, not the bytes
emitted into the prompt (§3 item 37).

    source  .remedy-wt/f272-r6-block.md   26278 bytes  5d1e0e2a62e049e9cf87f613f3be9b20f92c39a7b09d428c2fb59efc6b903c13
    saved   .agent/authored/f272-r6.md    26278 bytes  5d1e0e2a62e049e9cf87f613f3be9b20f92c39a7b09d428c2fb59efc6b903c13
    mirror  .agent/last_block.md          26278 bytes  5d1e0e2a62e049e9cf87f613f3be9b20f92c39a7b09d428c2fb59efc6b903c13
    filecmp.cmp(source, saved,  shallow=False) -> True
    filecmp.cmp(saved,  mirror, shallow=False) -> True

All three equal each other and the BLOCK_SHA and length the delegation named.

**G2 THE RECORD, at C2 — PASS.** Four readers over `.agent/live_review.md`,
readers (a) and (b) over `.agent/prose_slips.md`.

    live_review.md  pre 1081516  slice 7033  post 1088550
      pre terminal byte is exactly one NL           : True
      (a) pre is byte-exact prefix                  : True
      (a) post == pre + NL + slice                  : True
      (a) post ends in exactly one NL               : True
      (b) N counted by the script from the slice    : 1
      (b) units before / after / delta              : 693 / 694 / 1
      (b) last N units == slice paragraphs IN ORDER : True
      (b) prefix units unchanged                    : True
      (c) first appended paragraph [1081517,1088549), flip at 1085033 -> inside: True
      (c) mutated rejected by (a) / by (b)          : True / True
      (c) restored accepted by (a) / by (b)         : True / True
      (c) restored == disk image                    : True
      (d) distinct registrations                    : 302 -> 302
      (d) distinct Done ids                         : 247 -> 247
      (d) open set BY DISTINCT ID                   : 55 -> 55
      (d) ^Gate:                                    : 27 -> 28
      (d) ^Gate: F272 R5                            : 0 -> 1

    prose_slips.md  pre 134136  slice 679  post 134816
      pre terminal byte is exactly one NL           : True
      (a) VERDICT                                   : True
      (b) N 1, units 170 -> 171, delta 1, order OK  : True
      (c) flip at 134476 inside [134137,134815); both readers reject, both accept on restore, restored == disk

Every (d) count matches the block's expectation exactly.

**G3 THE PLAN, at C1 — PASS.**

    slice bytes 2126, on-disk bytes 2126, equal: True
    sha256 both 6145935d2ce57a5e95be0cba6f9e69eb80f960e03854cc6413bc2655e7e86af1
    line count 42, AGENTS.md cap 50 -> under: True
    "## Goal" present: True   "## Next Steps" present: True

**G4 THE COLLAPSE IS TOTAL, at C7.**

(i) PASS.

    tracked .py files enumerated from git ls-files (in Python): 1063
    packages/orchestration/data_paths.py present in enumeration : True
    tests/test_data_paths.py present in enumeration             : True
    occurrences of \bpingpong_runs?_dir\b                       : 0
    surviving files                                             : none

(ii) PASS, read from the SHIPPED module.

    module resolved from : /home/decodeux/Repos/remedy/packages/orchestration/data_paths.py
    hasattr pingpong_run_dir  : False
    hasattr pingpong_runs_dir : False
    NON-VACUITY hasattr run_dir  : True
    NON-VACUITY hasattr runs_dir : True

(iii) MEASURED BY AST OVER SCOPES. Two readings are reported because the gate's
literal wording is RED ON BASE — see deviation 2.

    reading                       base 61c4bd2e    HEAD
    LITERAL (the block's words)             21       36
    HAZARD  (the D3 defect)                  0        0

The HAZARD reading — a bare-Name call of `run_dir`/`runs_dir` that executes
BEFORE its scope's first binding of that name, which is exactly `run_dir =
run_dir(...)` and exactly round 5's three sites above their shadowing
assignment — is 0 over all 1063 tracked `.py` files, at base and at HEAD.

(iv) PER-FILE SITE COUNTS AND SHAPES. "sites" counts occurrences of
`\bpingpong_runs?_dir\b`; "shadowed" counts CALL sites whose callee is a bare
`Name` inside a scope binding that identifier — the definition that reproduces
the reviewer's table.

    commit file                                                      sites   A    B  shadowed
    C3   tests/cli/test_task_input.py                                    4   4    0     0
    C3   tests/orchestration/test_pingpong_cli.py                        6   6    0     0
    C3   tests/orchestration/test_worktree_safety.py                     4   4    0     0
    C3   tests/orchestration/test_job_stop_integration.py                3   3    0     0
    C3   tests/orchestration/test_job_worktree_integration.py            3   3    0     0
    C3   tests/orchestration/test_worktree_isolation.py                  3   3    0     0
    C3   tests/orchestration/test_failure_postmortem.py                  2   2    0     0
    C3   tests/orchestration/test_job_worktree_handoff.py                2   2    0     0
    C3   tests/orchestration/test_job_worktree_integrity.py              2   2    0     0
    C3   tests/orchestration/test_persisted_call_episode_membership.py   2   2    0     0
    C3   tests/orchestration/test_persisted_call_ownership.py            2   2    0     0
    C3   tests/orchestration/test_persisted_run_call_schema.py           2   2    0     0
    C3   tests/orchestration/test_run_manifest_ledger_semantics.py       2   2    0     0
    C3   tests/orchestration/test_run_manifest_task_lifecycle_binding.py 2   2    0     0
    C3   tests/orchestration/test_run_manifest_zero_call_expectations.py 2   2    0     0
    C3   tests/orchestration/test_stream_export_e2e.py                   2   2    0     0
    C3   tests/orchestration/test_worktree_persistence.py                2   2    0     0
    C4   tests/orchestration/test_pingpong_promote.py                   46   0   46    23
    C5   tests/orchestration/test_failure_wiring.py                      9   7    2     1
    C5   tests/orchestration/test_job_evidence.py                        8   0    8     4
    C5   tests/orchestration/test_evidence_bundle.py                     3   0    3     2
    C5   tests/orchestration/test_manual_completion_bundle.py            2   0    2     1
    C5   tests/orchestration/test_repair_loop.py                         2   0    2     1
    C5   tests/orchestration/test_worktree_lifecycle.py                  2   0    2     1
    C5   tests/orchestration/test_worktree_resume_cli.py                 2   0    2     1
    C6   tests/test_data_paths.py                                       13   0    0     0
    ------------------------------------------------------------------------------------
         TOTAL, 26 files                                               132  52   67    34

`tests/test_data_paths.py`'s 13 are neither shape: 10 were AST sites inside the
alias test C6 deletes whole, and 3 are the two failure-message strings C6
retargets. My independent AST measurement reproduces the reviewer's
132 sites / 34 shadowed / 8 files, and its per-file shadowed split
(46/23, 9/1, 8/4, 3/2, 2/1, 2/1, 2/1, 2/1) matches the block's table exactly.

**G5 THE DELETION IS OBSERVABLE, AND NO COVERAGE IS LOST — PASS.**

The control was NOT re-run, per the block: the reviewer already measured, at
`61c4bd2e` in a disposable worktree, that deleting both bodies with the test
callers UNMOVED is EXIT 1 across `tests/test_data_paths.py` (1 failed, 50
passed), `tests/orchestration/test_pingpong_promote.py` (23 failed, 48 passed)
and `tests/orchestration/test_job_evidence.py` (4 failed, 89 passed). The
REASONING that makes this round's run a red-proof rather than a green word: a
caller this round missed cannot survive C7 silently, because the name it would
still reference no longer exists on the module — it is a hard `ImportError` or
`AttributeError`, which the measured control shows those three suites do
observe. Those same three suites going green AFTER C7, with the deletion in
place, is therefore the discriminating reading.

    COVERAGE  tests/test_data_paths.py collected before C6 : 51
              tests/test_data_paths.py collected after  C6 : 50
              difference: exactly the deleted alias test
    test_the_pingpong_run_dir_is_the_run_id_under_the_pingpong_runs_dir

The four surviving pins, FULL NODE IDS obtained from `--collect-only`:

    tests/test_data_paths.py::TestDirectoryHelpers::test_runs_dir_default
    tests/test_data_paths.py::TestDirectoryHelpers::test_runs_dir_explicit_root
    tests/test_data_paths.py::TestJobAndRunLayout::test_a_run_hangs_under_runs_dir_and_never_under_jobs_dir
    tests/test_data_paths.py::TestJobAndRunLayout::test_the_root_override_is_honoured_by_all_four

    $ python3 -B -m pytest -q -p no:randomly <the four node ids>
    EXIT 0 — 4 passed in 0.21s

**G6 THE SUITES, at C7, run SERIALLY, one invocation each — PASS.**

    $ python3 -B -m pytest tests/test_data_paths.py -q -p no:randomly
    EXIT 0 — 50 passed in 0.76s

    $ python3 -B -m pytest tests/orchestration/ -q -p no:randomly
    EXIT 0 — 12809 passed, 10 skipped, 1 warning in 713.55s (0:11:53)

    $ python3 -B -m pytest tests/cli/ -q -p no:randomly
    EXIT 0 — 1537 passed in 298.02s (0:04:58)

    $ python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
    EXIT 0 — 42 passed in 20.97s

Both pinned counts hit exactly: `tests/cli/` 1537, canary 42.

**G7 LINT AND INTEGRITY, at C7 — PASS.**

    $ python3 -m ruff check <the 27 changed .py files, ONE invocation>
    EXIT 0 — All checks passed!

    $ python3 -m apps.cli.grouped integrity check --json
    EXIT 0 — "passed": true, "fail_count": 0

The repo-wide `ruff check .` was NOT run: it is not ordered, and it is EXIT 1
at 26 errors on base and on `main` under open finding R-0468.

**G8 THE TREE — PASS.**

    $ git status --porcelain      -> EMPTY (with C8 staged)
    $ git ls-files .remedy-wt     -> EMPTY
    $ git worktree list           -> the primary checkout + the twelve
                                     pre-existing remedy/job-* entries only;
                                     .remedy-wt/f272r6-base created and removed

Per-commit insertions from `git diff --numstat <parent> <commit>`, C0a..C7
(C8 excluded — it cannot count its own insertions, §3 item 14). Every commit
single-parent, every count under the DECISION F104 D1 cap of 500:

    C0a a4063692  parents 1  insertions 331
    C0b 0808ddc3  parents 1  insertions 280
    C1  f95245d3  parents 1  insertions  22
    C2  b26c010d  parents 1  insertions   4
    C3  252b0d95  parents 1  insertions  44
    C4  6af5d04a  parents 1  insertions  46
    C5  815f3a8d  parents 1  insertions  27
    C6  98ab08b6  parents 1  insertions   2
    C7  d7ec5a68  parents 1  insertions   0

Marker sweep: 0 lines beginning `<<<BEGIN ` or `<<<END ` across every written
non-block file (the two block copies are excluded by construction).

`.agent/STOP` readings (constraint 10):

    | Reading | When | os.path.exists |
    |---|---|---|
    | 1 | before C0a | False |
    | 2 | before C7  | False |
    | 3 | before C8  | False |

## Authored-text proofs

| Slice | Target | Result |
|---|---|---|
| PLANF272R6 | `.agent/plan.md` | disk image == slice bytes, 2126 == 2126, sha256 equal |
| RECORDR6 | `.agent/live_review.md` | `post == pre + b"\n" + slice`, byte-exact prefix, negative control rejects and restores |
| SLIPSR6 | `.agent/prose_slips.md` | same convention, same result |
| whole block | `.agent/authored/f272-r6.md`, `.agent/last_block.md` | `filecmp.cmp(shallow=False)` True against the source and each other; identical sha256 and length |

Every slice was extracted as the lines strictly BETWEEN its two marker lines,
each keeping its own terminating newline, with exactly one BEGIN and one END
asserted per name. No slice was edited (constraint 1).

## Deviations & assumptions

1. **The block's change-set count is 29; its own enumeration is 33 paths.**
   17 (C3) + 1 (C4) + 7 (C5) + 1 (C6) + 1 (C7) + 6 (`.agent/` files) = 33. I
   applied the ENUMERATION, which is the change set, and touched exactly those
   33 paths and no others. A prose numeral, no product effect.

2. **G4(iii) as literally worded is RED ON BASE and cannot reach 0.** The gate
   says "zero function scopes that BOTH bind a local named `run_dir` or
   `runs_dir` AND contain a call whose callee is a bare `Name` of that same
   identifier". A function-local `from packages.orchestration.data_paths import
   run_dir` followed by `run_dir(...)` satisfies that wording exactly, and it
   is the repository's correct and pervasive idiom. Measured in a disposable
   worktree at `61c4bd2e`, BEFORE this round wrote anything: the literal
   reading is **21**, of which 11 are production sites
   (`apps/cli/commands/do_cmd.py`, `packages/orchestration/job_evidence.py` x4,
   `pingpong_evidence.py`, `pingpong_promote.py`, `repair_attest.py`,
   `worktree_resume.py` x2) and 10 are in `tests/test_data_paths.py`. At HEAD
   it is 36, the rise being the shape-A files whose function-local import now
   spells the new name. I therefore report BOTH readings and treat the
   discriminating one as the gate: a bare-Name call executing BEFORE its
   scope's first binding of that name — the actual `UnboundLocalError` that
   DECISION F272 D3 describes and that round 5's three sites above their
   shadowing assignment exhibit. That reading is **0 at base and 0 at HEAD**.
   Recommend the gate's wording be corrected before it is reused.

3. **C6(c) was vacuous.** The block anticipated "the remaining sites in that
   file take SHAPE A or B by the scope test like any other". Measured: there
   are none. All 10 AST sites in `tests/test_data_paths.py` sat inside the
   alias test that (a) deletes whole; the file's other 3 regex occurrences are
   the two failure-message strings that (b) retargets. No shape-A or shape-B
   rewrite was performed in that file.

4. **Ruff `I001` forced two import lines to be combined.** In
   `test_worktree_lifecycle.py` and `test_worktree_resume_cli.py` the new
   `from packages.orchestration import data_paths` had to merge into the
   existing `from packages.orchestration import event_replay` line, giving
   `from packages.orchestration import data_paths, event_replay`. Applied with
   `python3 -m ruff check --fix --select I001` on exactly those two files. This
   is a consequence of the ordered G7 gate, not a choice; it is the same
   `I001` consequence round 5 recorded for `pingpong_loop.py`.

5. **The reviewer's "34 shadowed" is a count of CALL sites, not of
   occurrences.** Counting every occurrence in a shadowed scope — which
   includes the function-local import feeding the call — gives 63, exactly
   double for the uniform files. Under the call-site definition my numbers
   reproduce the reviewer's table cell for cell. Stated so the two figures are
   not read as a disagreement.

6. **C0a and C0b precede C1**, so `.agent/plan.md` did not yet describe round 6
   at those two commits. That is the block's own ordered sequence (constraint 3,
   §3 item 23), not a departure from it.

No finding id was minted and no `Done:` paragraph was written (constraint 8).
Behaviour changes: NONE beyond `pingpong_runs_dir` and `pingpong_run_dir`
ceasing to exist (constraint 7) — `pingpong_runs_dir(root)` was `runs_dir(root)`
and `pingpong_run_dir(run_id, root)` was `runs_dir(root) / run_id`, which is
`run_dir`'s own body, so every moved call reaches the same body as before.
Thirteen scratch drivers under `.remedy-wt/` were removed BY EXACT PATH, never
by glob; no `__pycache__` existed under `.remedy-wt/`, which is positive
evidence that `python3 -B` held for every run of the round.

## Next

Review round 6 and, on PASS, open T002 — the rest of the unified record: the
eleven administrative fields, eight of which have no counterpart in `JobPlan`,
and the Mission extension. T001 is complete: the run re-key, the repository-wide
spelling sweep and the name collapse have all landed, and neither ping-pong
spelling exists anywhere in the tree.
