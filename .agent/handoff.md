# Handback — F274 round 1 — THE ROUND STOPPED UNDER G8 AT THE CONTROL RUN

F274 is CLAIMED. The branch is cut, both state files are re-pointed, `.agent/live_review.md`
is re-headed with its findings region byte-identical, F272's round 31 verdict is booked, and
the ledger line reads `[~]`. C0a, C0b, C1, C2, C3 and C4 landed in the block's order.

**C5 AND C6 WERE NOT PERFORMED.** The block's probe specification orders an UNMUTATED CONTROL
before any mutated run and states, in its own words: "a control failure OUTSIDE it stops the
round under G8." The control produced failures outside the block's declared environment class.
No `Job.id` probe was installed, no site set was measured, and DECISION F274 D1 — whose text
asserts a measurement recorded in `.agent/f274_id_probe_inventory.md` — was NOT appended,
because appending a ruling whose premise was never measured would land a false claim in the
append-only decisions record. The disposable worktree was removed and pruned. The evidence the
next block needs to re-scope the control is in the Verification section below.

## Session

SESSION 1 of feature F274 · round 1 · rounds so far 1

CONTEXT SELF-ASSESSMENT (amend0905-throughput, one sentence): context is comfortable — this
round read the block, AGENTS.md, the self-drive protocol and the handback template in full,
and handled every large state file (`live_review.md` 493 KB, `decisions.md` 872 KB) by
measurement rather than by reading it.

## Range

Review of `13dfaabd93d7b6452a1d23ca698e29ed47ecf035`..HEAD.

This file is written BEFORE the commit that carries it exists, so C7's own SHA and its own
numstat row cannot appear here — the R-0149 self-reference exception.

## Commits

### 75a7bf17 f274: archive the round 1 step block as the authored original  (C0a)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f274-r1.md | +401 / -0 | `shutil.copyfile` of `.remedy-wt/f274-r1-block.md` per C0a |

### cd1a0222 f274: mirror the round 1 step block into the last block state file  (C0b)
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +383 / -329 | the same `shutil.copyfile`, the mirror |

### e165afe2 f274: re-point the plan and the context onto the F274 branch  (C1)
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | +37 / -42 | byte-equal to CONTEXTF274R1 |
| .agent/plan.md | +23 / -24 | byte-equal to PLANF274R1 |

### 6600442e f274: re-head the live review record at the F274 claim  (C2)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +31 / -35 | head replaced by REHEADTO; the `## Findings` tail is byte-identical |

### 42f63af4 f274: book the F272 round 31 verdict into the review record  (C3)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 / -0 | RECORDR31 appended against C2's post-image |

### f0e953a4 f274: claim F274 in the roadmap ledger  (C4)
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS.md | +1 / -1 | STATUSPAIR, one replacement, `[ ]` → `[~]` |

Per-commit insertions against the DECISION F104 D1 cap of 500: 401, 383, 60, 31, 2, 1. Every
commit is single-parent. No commit is oversize and none needs the declared-oversize exception.

## External actions

| Command | Outcome |
|---|---|
| `gh pr list --state open --json number,headRefName,baseRefName,isDraft` | `[]` — Open PR Gate passes, no open PR |
| `git checkout -b feature/f274-one-world-completion-part-two` | cut from `main` at `13dfaabd93d7b6452a1d23ca698e29ed47ecf035` |
| `git worktree add .remedy-wt/f274-probe 13dfaabd…` | created, detached HEAD at the base SHA; worktree count 14 → 15 |
| `git worktree remove --force .remedy-wt/f274-probe` + `git worktree prune` | removed and pruned; worktree count 15 → 14 |
| `git push -u origin feature/f274-one-world-completion-part-two` | run after this commit |

NO pull request was created and NOTHING was merged, as the block orders.

## Verification

### G1 TRANSPORT — one digest comparison, EXIT n/a (in-process)

    .remedy-wt/f274-r1-block.md   30618 bytes  401 lines
    .agent/authored/f274-r1.md    30618 bytes  401 lines
    .agent/last_block.md          30618 bytes  401 lines
    all three byte-identical: True
    all three sha256: 0a01672609eb7de5034f478647ee324397039562b5321690d626e8938426eccc
    equal to the digest the delegation states: True

Per §3 item 37 this chain covers those three artefacts and claims nothing about emitted bytes.

### G2 THE RE-HEAD (C2) — PASSED, all four readings

    '\n## Findings\n' occurrences: 1 BEFORE, 1 AFTER
    HEAD before: 2501 bytes / 39 lines
    TAIL before: 490724 bytes / 498 lines
      sha256 d7ed620f9242c7929e0d8ae77070ef28b87c063578d8b03acd8cef88fac1cb03
    TAIL after:  490724 bytes / 498 lines
      sha256 d7ed620f9242c7929e0d8ae77070ef28b87c063578d8b03acd8cef88fac1cb03  (UNCHANGED)
    HEAD after:  2534 bytes / 35 lines, BYTE-EQUAL to REHEADTO: True

### G3 THE RECORD APPEND (C3), against C2's post-image — PASSED, (a)(b)(c)(d)

    pre-image  493258 bytes / 533 lines  sha256 c7c2e000bcd84e3529e8f61b84090416e9b00e617384e0c1225ad331426e4a65
    slice      4613 bytes / 2 lines, carries its own leading blank line: True
    post-image 497871 bytes / 535 lines  sha256 799cadf2680c53315f25d3bd174720cd112040e2626d95ef13102cdebf3f5d14
    (a) BYTE   pre is a byte-exact prefix of post: True | post == pre + slice: True
    (b) STRUCT N counted from the slice = 1; the last 1 blank-line-separated units of the
        whole file equal the slice's 1 paragraph in order: True
    (c) CONTROL byte flipped at offset 493269, inside the FIRST appended paragraph (' ' -> NUL)
        byte reader   REJECTS flipped: True | ACCEPTS real: True
        struct reader REJECTS flipped: True | ACCEPTS real: True
        file on disk UNCHANGED by the control: True (sha256 799cadf2… as above)
    (d) COUNTS                          BEFORE   AFTER
        distinct '^- R-\d{4}'               62      62
        distinct '^Done: R-\d{4}'            2       2
        open set BY DISTINCT ID             60      60
        '^Gate: '                           31      32
        '^Gate: F272 R31'                    0       1
        '^- R-0829'                          0       0

### G4 THE TWO STATE FILES (C1) — PASSED

    plan.md BYTE-EQUAL to PLANF274R1: True | 36 lines, under the AGENTS.md cap of 50: True
    plan.md carries '## Goal': True | '## Next Steps': True
    context.md BYTE-EQUAL to CONTEXTF274R1: True
    reader 1  contains the substring 'Steps':                        True
    reader 2  '## Active Branch' followed by a feature/ slug:        True
              -> feature/f274-one-world-completion-part-two
    reader 3  a roadmap F-id present:                                True  (F017, F259, F260, …)
    reader 4  contains the substring 'pytest':                       True

### G5 THE CLAIM (C4) — PASSED

    PAIR CLASSIFICATION re-derived before use: TO CONTAINS FROM = False
      -> label REWRITE, therefore NO append obligation
    FROM count: 1 BEFORE, 0 AFTER      TO count: 0 BEFORE, 1 AFTER
    post == pre with that ONE replacement and nothing else: True
    file 40038 bytes before and after
    '^- \[~\] '      occurs exactly once after: 1
    '^- \[~\] F274 ' occurs exactly once after: 1

### G6 THE MEASUREMENT (C5) — NOT REACHED. The control stopped the round.

(a) THE UNMUTATED CONTROL, run FIRST and before any edit, in the disposable worktree at the
base SHA, exactly as the block spells it:

    python3 -B -m pytest tests/ -q -p no:randomly -n auto
    EXIT 1
    11 failed, 19739 passed, 29 skipped, 1 warning in 206.65s (0:03:26)

Classification of every one of the 11 against the block's declared class — "`tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`
plus `tests/ui_server/` ids":

| Failed id | In the declared class? |
|---|---|
| tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes | YES — named explicitly |
| tests/ui_server/test_command_channel.py::TestCommandChannelDoor — 8 ids | YES — `tests/ui_server/` ids |
| tests/cli/test_job_rerun_workspace_identity.py::TestNoFalseWorkspaceDrift::test_a_mutated_workspace_shows_blocking_drift | **NO** |
| tests/cli/test_review_bundle_runtime.py::TestSubprocessCleanup::test_timeout_raises_with_cleanup | **NO** |

Two control failures fall OUTSIDE the declared class, so the block's own clause applies and
the round stops there. The worker then measured — rather than asserted — what those two are,
so the next block can re-scope the control rather than re-discover this:

1. BOTH PASS IN ISOLATION.

        python3 -B -m pytest \
          "tests/cli/test_job_rerun_workspace_identity.py::TestNoFalseWorkspaceDrift::test_a_mutated_workspace_shows_blocking_drift" \
          "tests/cli/test_review_bundle_runtime.py::TestSubprocessCleanup::test_timeout_raises_with_cleanup" \
          -q -p no:randomly
        EXIT 0
        2 passed in 1.94s

2. A SECOND UNMUTATED CONTROL, same command, same worktree, no edit in between:

        python3 -B -m pytest tests/ -q -p no:randomly -n auto
        EXIT 1
        1 failed, 19755 passed, 23 skipped, 1 warning in 137.55s (0:02:17)
        FAILED tests/cli/test_review_bundle_runtime.py::TestSubprocessCleanup::test_timeout_raises_with_cleanup

   The vitest id and all eight `tests/ui_server/` ids WENT GREEN on the second run, and so did
   the workspace-drift id. The cause is on disk: the first run's auto-build populated
   `apps/ui/node_modules` and `apps/ui/dist` INSIDE the worktree (both directories exist there
   now; the run-1 output carries the "cd apps/ui && npm install && npm run build" hint and the
   `REMEDY_UI_NO_AUTO_BUILD=1` escape). So the block's environment class is TRANSIENT — it
   exists on the FIRST full-suite run in a fresh worktree and is self-healing afterwards.

3. THE TWO OUT-OF-CLASS IDS, DIAGNOSED FROM THEIR REAL OUTPUT:

   - `test_a_mutated_workspace_shows_blocking_drift` failed on
     `assert diff_manifests(ref, clean)["blocking"] == []` with a single blocking entry whose
     `field` is `remedy_worktree_digest`. It compares a digest of the remedy worktree while the
     UI auto-build of run 1 was writing `node_modules` and `dist` into that same worktree. This
     failure has the SAME ROOT CAUSE the block names — a fresh worktree without node_modules or
     dist — but is NOT in the block's ENUMERATED id list, and it disappeared in run 2.
   - `test_timeout_raises_with_cleanup` failed on
     `assert result.returncode != 0, "Orphan process found after timeout cleanup"` where
     `pgrep -f "apps.cli.grouped.*--help"` returned PID 2115172. The assertion is a HOST-WIDE
     pgrep with no worker scoping, so under `-n auto` it sees a SIBLING xdist worker's
     subprocess. It is the one id that failed in BOTH control runs and it passes serially.

(b) THE MUTATED PROBE RUN — NOT RUN. No edit was made to
`packages/core/models.py` in the worktree or anywhere else. No per-PID site files exist, no
site set was aggregated, and `.agent/f274_id_probe_inventory.md` DOES NOT EXIST.

THE LOAD-BEARING PROPERTY G6 ASKS FOR — the distinct site count and the boolean `sites > 500` —
IS THEREFORE UNMEASURED BY THIS ROUND. It is not reported, not estimated, and not carried over
from the reviewer's figure of 1978. The persisted-key demonstration was likewise NOT run, so no
exit code and no pair of UUIDs is reported for it.

### G7 THE DECISION APPEND (C6) — NOT REACHED, deliberately

`.agent/decisions.md` is UNTOUCHED by this round: 872485 bytes / 10897 lines, sha256
`6db4150fe9437cc702fcbd1199be58a5342e80678183f05944f14ba6a5e73993`, identical to the base
reading the block asserts. `^## DECISION F274 D` occurs 0 times, and D1SLICE is NOT applied.

### G8 THE GATES AND THE TREE — every gate EXIT 0, run serially in the primary checkout

| Command | Exit | Tail |
|---|---|---|
| `python3 -B -m pytest tests/docs/ -q -p no:randomly` | 0 | `303 passed in 0.65s` |
| `python3 -B -m pytest tests/orchestration/test_roadmap_index.py -q -p no:randomly` | 0 | `30 passed in 0.37s` |
| `python3 -B -m pytest tests/ui_server/ -q -p no:randomly` | 0 | `515 passed in 35.23s` |
| `python3 -B -m pytest tests/orchestration/test_test_runner.py -q -p no:randomly` | 0 | `52 passed in 5.74s` |
| `python3 -B -m pytest tests/regression/test_resource_safety.py -q -p no:randomly` | 0 | `21 passed in 11.51s` |
| `python3 -B -m pytest tests/orchestration/test_integrity_gate.py -q -p no:randomly` | 0 | `16 passed in 0.28s` |
| `python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly` | 0 | `42 passed in 20.79s` |

The four state readers were run as FOUR, not three. Each command was run on its own, with its
exit code captured by a Python runner rather than through a pipe, because this session's shell
guard refuses `$?` inside a compound command.

THE TREE:

    git status --porcelain  — EMPTY immediately before every one of the six commits and now
    git ls-files .remedy-wt — 0 entries (the directory is gitignored at .gitignore:235)
    git worktree list       — 14 at the start of the round, 15 with the probe worktree, 14 now

### THE THREE `.agent/STOP` READINGS, by `os.path.exists`

| Reading | When | Result |
|---|---|---|
| 1 | before C0a | False |
| 2 | before C5 | False |
| 3 | before C7 | False |

The round did not stop on the sentinel. It stopped on the block's own control clause.

## Authored-text proofs

Every authored text was extracted PROGRAMMATICALLY from `.agent/authored/f274-r1.md` by
matching the marker lines the block's Conventions section defines, with an assertion that each
name matches exactly one BEGIN and one END line. None was retyped.

| Name | Bytes | Lines | sha256 of the extracted text | Applied? |
|---|---|---|---|---|
| PLANF274R1 | 1909 | 36 | 69231b29f7a71fc56914cf7bd54b301787f11353427006e8c47c83db5e791f26 | yes — `.agent/plan.md` byte-equal |
| CONTEXTF274R1 | 3475 | 60 | 19f3ae628a709c7a366a948b2cd5ceddf36b601203be3e2ff5e1e770206bc4f7 | yes — `.agent/context.md` byte-equal |
| REHEADTO | 2534 | 35 | 4b300a4042a0480154111da39b9ac15e46be97583eb5ed496078d9a7b37c422a | yes — the new head is byte-equal |
| RECORDR31 | 4613 | 2 | a80e6d5da7d7f873ade72b79216daad1b767582c1d39b63aa17ba1c26b8ef1fa | yes — appended verbatim |
| STATUSPAIR_FROM | 97 | 0 | 43256980ef8a9c6fb8198f4edd51de1f9b7a8f2ef689c70f8936325ba1b6ad87 | yes — matched once, replaced once |
| STATUSPAIR_TO | 97 | 0 | e76c1b1887853b191d1401c8c70e59606f20da587a809f0714a28eeacf65ed05 | yes — present once after |
| D1SLICE | 3939 | 51 | da8fc271c9734f15b72e0f91457b90852d8b4904e75d4e8d38ae83af33f506f1 | **NO — C6 not reached** |

The transport chain's first link was verified before anything was written:
`.remedy-wt/f274-r1-block.md` measured 30618 bytes, 401 lines and sha256
`0a01672609eb7de5034f478647ee324397039562b5321690d626e8938426eccc`, matching all three values
the delegation stated.

The block's five asserted base measurements were CONFIRMED ON DISK before use, with no
divergence: `.agent/live_review.md` 493225 bytes / 537 lines sha256 `9b104c3c…1438`;
`.agent/decisions.md` 872485 bytes / 10897 lines sha256 `6db4150f…3993`; `.agent/plan.md` 1838
bytes; `.agent/context.md` 3366 bytes; `docs/roadmap/STATUS.md` 40038 bytes.

## Deviations & assumptions

1. **C5 AND C6 WERE NOT PERFORMED — the block's ordered commit sequence is incomplete.** The
   sequence executed was C0a, C0b, C1, C2, C3, C4, C7. Nothing was reordered and nothing extra
   was added; two ordered items are absent. The trigger is the block's own probe specification:
   "Report your control's failures and state whether each is in that class; a control failure
   OUTSIDE it stops the round under G8." Two of the control's eleven failures are outside the
   declared class, so the clause fired. The worker did NOT widen the class on its own
   authority, did not install the probe, and did not append a DECISION asserting a measurement
   that was never taken.

2. **THE WORKER DISAGREES WITH THE CLAUSE'S SCOPE AND SAYS SO RATHER THAN ACTING ON IT.** The
   measurements in G6 above show the declared class is under-drawn in two different ways: it is
   drawn by ENUMERATED ID where its own stated CAUSE (no `node_modules`, no `dist`) reaches at
   least one further id, `test_a_mutated_workspace_shows_blocking_drift`; and it does not cover
   `test_timeout_raises_with_cleanup`, a host-wide `pgrep` assertion that cannot be stable under
   `-n auto` because it matches sibling workers. A control that runs the full suite in a fresh
   worktree under `-n auto` therefore cannot be all-green on its first pass by construction.
   That is a reviewer decision to take, not the worker's, and the round ended instead of
   absorbing it.

3. **A SPEC GAP THE NEXT BLOCK SHOULD CLOSE BEFORE THE PROBE IS RE-ORDERED.** The block
   specifies a `property` named `id` with a getter only. `job.id = uuid4()` is a live
   assignment pattern in the suite — `tests/ui_server/test_live_state.py:40` and `:51`,
   `tests/ui_server/test_brain_view_model.py:150`, `:256`, `:280`,
   `tests/regression/test_named_bugs.py:69`, `tests/orchestration/test_approval_queue.py:99`,
   `tests/orchestration/test_autorun.py:19`, `tests/orchestration/test_source_apply.py:50` and
   `:61` among others. A getter-only property makes every one of those raise on WRITE, which
   both contradicts the block's "do NOT raise `AttributeError` anywhere in this probe" and
   truncates those tests before they reach their reads — the exact UNDER-COUNTING the
   specification exists to prevent. The probe needs a setter that writes `self.job_id` and
   records nothing. This was NOT applied; it is reported so the ruling is the reviewer's.

4. **AN ENVIRONMENT FACT THAT AFFECTS THE PROBE'S VALIDITY, MEASURED NOT ASSUMED.** `remedy`
   0.1.0 is installed EDITABLE at `/home/decodeux/Repos/remedy`, so `packages` is a namespace
   package whose `__path__` inside the worktree is
   `['…/.remedy-wt/f274-probe/packages', '/home/decodeux/Repos/remedy/packages']`. The worktree
   entry is FIRST, and `packages.core.models.__file__` resolved to the worktree copy, so a
   mutation there IS the one the suite imports. Confirmed before the control ran.

5. C0a and C0b precede C1, so the first two commits land while `.agent/plan.md` still names
   F272. This is the block's explicit ordering and its stated reason (§3 item 23); it is noted
   here only because AGENTS.md's Commit Gate item 1 reads on every commit.

6. The block's control assertion of "13 failed and 19737 passed" was not reproduced: this
   worker measured 11 failed / 19739 passed on the cold run and 1 failed / 19755 passed on the
   warm run, over the same 19779 collected. The divergence is declared rather than absorbed.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a | done | `.agent/authored/f274-r1.md` by `shutil.copyfile` |
| C0b | done | `.agent/last_block.md` by `shutil.copyfile` |
| C1 | done | both state files byte-equal to their slices |
| C2 | done | re-head applied, findings tail digest unchanged |
| C3 | done | RECORDR31 appended against C2's post-image |
| C4 | done | STATUSPAIR applied, one replacement |
| C5 | skipped | the block's control clause stopped the round under G8; no probe installed, no inventory written |
| C6 | skipped | D1SLICE asserts a measurement C5 never took; appending it would land a false claim in an append-only record |
| C7 | done | this file |
| G1 | done | three artefacts byte-identical at the delegation's digest |
| G2 | done | all four readings reported; tail digest unchanged |
| G3 | done | (a) (b) (c) (d) all reported and all pass |
| G4 | done | both files byte-equal; all four context readers reported as booleans |
| G5 | done | pair re-classified as a REWRITE; counts 1→0 and 0→1 |
| G6 | skipped | the measurement was not taken; the control and its diagnosis are reported in full instead |
| G7 | skipped | C6 was not performed; `.agent/decisions.md` is proven untouched at its base digest |
| G8 | done | seven gate commands, every one EXIT 0; tree, worktree counts and per-commit insertions reported |

## Next

Phase 1 rule 1 first: re-read `.agent/STOP`. Then the reviewer rules the control's scope — either
widen the declared environment class to cover the auto-build's transient reach and the
`-n auto` `pgrep` interference, or order the control as a WARM second run, or order the probe
run serially — and re-issues T001's probe as F274 round 2, with the getter/setter gap of
deviation 3 closed. `.agent/f274_id_probe_inventory.md` and DECISION F274 D1 are still owed.
No pull request exists for this branch and none is owed yet.
