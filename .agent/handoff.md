# Handback — F275 round 73

## Session

SESSION 26 of feature F275 · round 73 · rounds so far 73

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE

F275 stands past the soft limit amend0908-f275-finish rule 1 names. The SCOPE REPORT that
rule obliges was written in round 51's handback and STANDS; it is not restated here, per the
block's Handback section. Rule 2 forbids the split-and-close default by name, so the session
writes the report reference and continues.

CONTEXT SELF-ASSESSMENT (amend0905-throughput): context is comfortable — this round was one
expensive gate and eleven single-path commits, and the reading budget went almost entirely to
the block and the three carriers rather than to the repository, so a further round in this
session would start from a healthy margin.

THE ROUND'S HEADLINE: every gate ran, ten of the eleven commits landed exactly as ordered, and
G6(b) is RED on its FIRST ordered reading — the control run of the full suite was NOT green.
Per the block's own G6(b) and the delegation's standing instruction, the round STOPPED at that
reading, wrote this handback with the real output, and did not repair the gate by widening the
change set. The red is on a test the round's own artefact names as load-sensitive, and the
detail is in Deviations below. No finding id is registered, resolved or de-registered.

## Range

Review of `f8fbe3b6`..`HEAD`

## Commits

### 86081613 F275 R73 C0a: save the round 73 block as authored text.
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f275-r73.md | +362 / -0 | the block, transported by `shutil.copyfile` from `.remedy-wt/f275-r73.block.md` |

### dbd5ab4f F275 R73 C0b: save the round 73 residual artefact as authored text.
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f275-r73-artefact.md | +189 / -0 | whole text, transported by `shutil.copyfile` |

### 78e5c18c F275 R73 C0c: save the owner-check stage carrier as authored text.
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f275-r73-owner-stage.py.md | +529 / -0 | whole text, transported by `shutil.copyfile`; DECLARED OVERSIZE, see Deviations |

### 18b82f97 F275 R73 C0d: save the owner-widening instrument carrier as authored text.
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f275-r73-instrument.py.md | +179 / -0 | whole text, transported by `shutil.copyfile` |

### 7c73ad68 F275 R73 C0e: save the residual-risk instrument carrier as authored text.
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f275-r73-risk.py.md | +185 / -0 | whole text, transported by `shutil.copyfile` |

### df901dd8 F275 R73 C0f: mirror the round 73 block into the last-block state file.
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +174 / -161 | REPLACEMENT, sourced from the COMMITTED C0a blob via `git cat-file blob` |

### e7783a0d F275 R73 C1: make the plan current for round 73.
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +18 / -20 | whole-file replacement by slice PLAN73 |

### 9149963c F275 R73 C2: book the round 72 reviewer verdict.
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +12 / -0 | append of slice RECORD73 |

### e84567f7 F275 R73 C3: append the round 72 prose slips.
| Path | +/- | Reason |
|---|---|---|
| .agent/prose_slips.md | +6 / -0 | append of slice SLIPS73 |

### 9a2e2965 F275 R73 C4: record DECISION F275 D47, the ruling on the owner check residual.
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +14 / -0 | append of slice DEC73 |

### 5d80f4d3 F275 R73 C5: land the owner-check residual artefact for round 73.
| Path | +/- | Reason |
|---|---|---|
| .agent/f275_t003_owner_residual_r73.md | +189 / -0 | copy of the COMMITTED C0b blob |

### C6 — this handback (self-reference exception, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | measured by the reviewer at the next gate | a handback cannot table the commit that writes it; every gate of this round ran at C5 |

THE INSERTION CELLS ABOVE ARE COMPARED CELL BY CELL AGAINST G4, and every source is
`git show --numstat <sha>` and no other. The column is an insertion and deletion count, never a
file's line count.

| Commit | table insertion cell | G4 insertion reading | AGREE |
|---|---|---|---|
| C0a 86081613 | 362 | 362 | yes |
| C0b dbd5ab4f | 189 | 189 | yes |
| C0c 78e5c18c | 529 | 529 | yes |
| C0d 18b82f97 | 179 | 179 | yes |
| C0e 7c73ad68 | 185 | 185 | yes |
| C0f df901dd8 | 174 | 174 | yes |
| C1 e7783a0d | 18 | 18 | yes |
| C2 9149963c | 12 | 12 | yes |
| C3 e84567f7 | 6 | 6 | yes |
| C4 9a2e2965 | 14 | 14 | yes |
| C5 5d80f4d3 | 189 | 189 | yes |

## External actions

No `gh` command was run. No `remedy` CLI command was run. No pull request was created, edited
or merged. No branch was created. No merge. No force-push. Constraint 6 holds.

| Action | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/r73_g3_wt 5d80f4d3` | exit 0 — G3's negative control |
| `git worktree remove --force .remedy-wt/r73_g3_wt` | exit 0 |
| `git worktree prune` (after G3) | exit 0 |
| `git worktree add --detach .remedy-wt/r73_i_wt f8fbe3b6` | exit 0 — created and removed by instrument A itself, four times (one run plus the determinism triple) |
| `git worktree remove --force .remedy-wt/r73_i_wt` + prune | exit 0 each time; instrument A section 6 reports the list back |
| `git worktree add --detach .remedy-wt/r73_risk_wt f8fbe3b6` | exit 0 — created and removed by instrument B itself |
| `git worktree remove --force .remedy-wt/r73_risk_wt` + prune | exit 0; instrument B section 6 reports the list back |
| `git push -u origin feature/f275-one-world-completion-part-three` | after C6 — result recorded in the round report |

Every worktree lived under the gitignored `.remedy-wt/` and was removed and pruned by the
instrument that made it. `git worktree list` after G6 and again at G8 holds exactly ONE entry,
the primary checkout.

## Verification

Every gate was run as `bash -c '<cmd> > <out> 2>&1; echo "REAL_EXIT=$?" >> <out>'` and the exit
code below is the number read back out of the transcript file, per constraint 11. Transcripts
are under `.remedy-wt/r73_g*.txt`.

ORDERING, per constraint 13: G5 RAN BEFORE G6. Instrument A wrote `.remedy-wt/r73_map72.json`,
the per-site decision map of the shipped round 72 stage (144180 bytes, produced at 05:26), and
instrument B then read that file to know which sites are refused. The order was not accidental:
instrument B fails without that file, and G6's section 1 figures are derived from it.

STOP READINGS, per constraint 7. Before the first commit: `os.path.exists('.agent/STOP') =
False`, `glob.glob('.agent/STOP') = []`. Again before C6: `os.path.exists('.agent/STOP') =
False`, `glob.glob('.agent/STOP') = []`.

### G1 TRANSPORT AND THE BLOCK BUDGET — REAL_EXIT=0

    C0a .agent/authored/f275-r73.md  committed 36880 bytes 1d644d76…0bef45 | scratch 36880 bytes 1d644d76…0bef45 | EQUAL
    C0b .agent/authored/f275-r73-artefact.md  committed 12291 bytes f91e6c7a…c99fe72 | scratch 12291 f91e6c7a…c99fe72 | EQUAL
    C0c .agent/authored/f275-r73-owner-stage.py.md  committed 24929 bytes 23a4d972…851068 | scratch 24929 23a4d972…851068 | EQUAL
    C0d .agent/authored/f275-r73-instrument.py.md  committed 8095 bytes 37fb5020…2ede84 | scratch 8095 37fb5020…2ede84 | EQUAL
    C0e .agent/authored/f275-r73-risk.py.md  committed 8661 bytes dd04e076…b11dd0 | scratch 8661 dd04e076…b11dd0 | EQUAL
    C0f .agent/last_block.md  committed 36880 bytes 1d644d76…0bef45 | COMMITTED C0a blob 36880 1d644d76…0bef45 | EQUAL

    SLICE CARDINALITY MEASURED: 4
       PLAN73    bytes  2837 | lines  47 | MATCHES ITS BEGIN MARKER: True
       RECORD73  bytes  6087 | lines  11 | MATCHES ITS BEGIN MARKER: True
       SLIPS73   bytes  2970 | lines   5 | MATCHES ITS BEGIN MARKER: True
       DEC73     bytes  5715 | lines  13 | MATCHES ITS BEGIN MARKER: True

    TOTAL lines measured : 362 | constraint 8 states 362 | EQUAL: True
    slice body lines     : 76 (8 BEGIN/END marker lines counted as PROSE)
    PROSE lines measured : 286 | constraint 8 states 286 | EQUAL: True

    lines of length >= 2, all characters identical : 0 | constraint 15 fixes this at 0 | EQUAL: True
    wider reading, length >= 1, all identical      : 0

    C0c owner-stage carrier : ```python fences 1, bare ``` 1, source 24253 bytes 7be34374…07eddb8, RE-WRAPPED == COMMITTED BLOB BYTE FOR BYTE: True
    C0d instrument carrier  : ```python fences 1, bare ``` 1, source  7409 bytes c7639899…417468,  RE-WRAPPED == COMMITTED BLOB BYTE FOR BYTE: True
    C0e risk carrier        : ```python fences 1, bare ``` 1, source  7985 bytes 048e46b5…723c23e, RE-WRAPPED == COMMITTED BLOB BYTE FOR BYTE: True

The slice cardinality is the number this worker MEASURED; the block states no numeral for it.

### G2 THE PLAN — REAL_EXIT=0

    .agent/plan.md at C1 e7783a0d : 2837 bytes 066674ceb976a34c83aac0b3465db174357b97b46c9c09c9c7ae92d8bc7c0320
    slice PLAN73                  : 2837 bytes 066674ceb976a34c83aac0b3465db174357b97b46c9c09c9c7ae92d8bc7c0320
    BYTE-IDENTICAL                : True
    line count                    : 47 | AGENTS.md cap 50 | WITHIN CAP: True
    lines matching ^## Goal$        : 1 (line 6)  | must be 1 | True
    lines matching ^## Next Steps$  : 1 (line 24) | must be 1 | True

### G3 THE RECORD — REAL_EXIT=0

(i) READER A, the byte stream:

    C2 .agent/live_review.md    pre 1051368 | post 1057456 | delta 6088 | body 6087 | expected 6088 | ACCEPT
    C3 .agent/prose_slips.md    pre  268101 | post  271072 | delta 2971 | body 2970 | expected 2971 | ACCEPT
    C4 .agent/decisions.md      pre 1186351 | post 1192067 | delta 5716 | body 5715 | expected 5716 | ACCEPT

(ii) READER B, structural, over the WHOLE appended region, N COUNTED from the slice:

    C2 .agent/live_review.md    N = 6 | post units 488  | ACCEPT
    C3 .agent/prose_slips.md    N = 3 | post units 365  | ACCEPT
    C4 .agent/decisions.md      N = 7 | post units 2407 | ACCEPT

(iii) NEGATIVE CONTROL, inside a disposable worktree at 5d80f4d3, one ASCII letter flipped
inside the FIRST appended paragraph of each file:

    git worktree add -> exit 0
    C2 .agent/live_review.md  byte offset 1051369 | letter 'G' -> 'g' | READER A REJECT | READER B (N=6) REJECT
    C2 .agent/live_review.md  UNMUTATED restored 1057456 bytes identical | READER A ACCEPT | READER B ACCEPT
    C3 .agent/prose_slips.md  byte offset  268116 | letter 'F' -> 'f' | READER A REJECT | READER B (N=3) REJECT
    C3 .agent/prose_slips.md  UNMUTATED restored  271072 bytes identical | READER A ACCEPT | READER B ACCEPT
    C4 .agent/decisions.md    byte offset 1186355 | letter 'D' -> 'd' | READER A REJECT | READER B (N=7) REJECT
    C4 .agent/decisions.md    UNMUTATED restored 1192067 bytes identical | READER A ACCEPT | READER B ACCEPT
    git worktree remove -> exit 0 ; git worktree prune -> exit 0

Both readers REJECTED all three mutations and ACCEPTED all three unmutated regions.

(iv) Over RECORD73:

    RECORD73 line count : 11
    lines AFTER THE FIRST carrying a reserved prefix (- R-, Done: R-, Landed: R-, Gate: ) : 0 | must be 0 | True
    lines C2 ADDS matching ^- R-     : 0 | must be 0 | True
    lines C2 ADDS matching ^Done: R- : 0 | must be 0 | True

(v) RECORD73's first line against its neighbours, mechanically:

    lines at the base matching ^Gate: F275 R\d+ — the F275 round \d+ entry\. : 71
    the new first line matches that same pattern                            : True
    duplicates any of them                                                  : False (duplicate count 0)

(vi) Over DEC73:

    DEC73 begins '## DECISION F275 D47 '                : True
    lines at the base matching ^## DECISION F275 D47    : 0 | must be 0 | True
    highest existing ^## DECISION F275 D<n> at the base : 46 (46 distinct ids)

(vii) Over SLIPS73:

    paragraphs SLIPS73 adds                                    : 3
    of those beginning '2026-09-12 · F275 R72 · '              : 3
    lines at the base already beginning with that exact prefix : 0

### G4 THE ARTEFACT — REAL_EXIT=0

    .agent/f275_t003_owner_residual_r73.md at C5 : 12291 bytes f91e6c7a336baf0925e60e9d422ad04dad38c7b4afaa354b2c62abaf4c99fe72
    the COMMITTED C0b blob                       : 12291 bytes f91e6c7a336baf0925e60e9d422ad04dad38c7b4afaa354b2c62abaf4c99fe72
    BYTE-IDENTICAL                               : True

    git show f8fbe3b6:.agent/f275_t003_owner_residual_r73.md
       exit code : 128 | NON-ZERO AS EXPECTED: True
       stderr    : fatal: path '.agent/f275_t003_owner_residual_r73.md' exists on disk, but not in 'f8fbe3b6'

    PER-COMMIT INSERTIONS — the quantity DECISION F104 D1 caps at 500
       C0a 86081613  insertions  362 | deletions   0 | paths staged 1 | under 500: True
       C0b dbd5ab4f  insertions  189 | deletions   0 | paths staged 1 | under 500: True
       C0c 78e5c18c  insertions  529 | deletions   0 | paths staged 1 | under 500: FALSE
       C0d 18b82f97  insertions  179 | deletions   0 | paths staged 1 | under 500: True
       C0e 7c73ad68  insertions  185 | deletions   0 | paths staged 1 | under 500: True
       C0f df901dd8  insertions  174 | deletions 161 | paths staged 1 | under 500: True
       C1  e7783a0d  insertions   18 | deletions  20 | paths staged 1 | under 500: True
       C2  9149963c  insertions   12 | deletions   0 | paths staged 1 | under 500: True
       C3  e84567f7  insertions    6 | deletions   0 | paths staged 1 | under 500: True
       C4  9a2e2965  insertions   14 | deletions   0 | paths staged 1 | under 500: True
       C5  5d80f4d3  insertions  189 | deletions   0 | paths staged 1 | under 500: True

EVERY COMMIT STAGES EXACTLY ONE PATH. C0c at 529 is over the cap and is declared below.

### G5 INSTRUMENT A — THE WIDENING — REAL_EXIT=0 (run), REAL_EXIT=0 (determinism triple)

(a) Extractions from the COMMITTED carriers:

    EXTRACTED 78e5c18c:.agent/authored/f275-r73-owner-stage.py.md -> .remedy-wt/f275-r73-owner-stage.py 24253 bytes 7be3437450d1f183d241e8a5161a6ae182652d0aecd674ea10e8f870407eddb8
    EXTRACTED 18b82f97:.agent/authored/f275-r73-instrument.py.md  -> .remedy-wt/f275-r73-instrument.py   7409 bytes c763989971b92f512aaf581704346e05c52ac6b24355a3a53f911161cd417468

(b) `python3 -B .remedy-wt/f275-r73-instrument.py . f8fbe3b6` — EVERY LINE OF EVERY BANNER:

    === 1. THE ANCHOR — both stages come out of git, not out of scratch ===
          the COMMITTED round 72 carrier : 19931 bytes, fences 1/1
          its extracted source           : sha256 b0108e5e316af922e411a8ca7be16c892f69e15de8e6b9623ca0078da8e18676
          the round 73 stage under test  : sha256 7be3437450d1f183d241e8a5161a6ae182652d0aecd674ea10e8f870407eddb8

    === 2. `--narrow` STILL REPRODUCES THE ROUND 71 READER ===
                                                           round 71   --narrow
          CONFIRMED: the owner verdict matches the recei       1195       1195
          CONTRADICTED: the receiver holds another recor          4          4
          REFUSED to decide: receiver's class not static        787        787
          REFUSED to decide: receiver is not a bare name        113        113
          REFUSED to decide: annotation carries no class         99         99
          DECIDED                                              1199       1199
          REFUSED, the stated blind spot                        999        999
          every class EQUAL to the round 71 figures      : True

    === 3. THE SHIPPED STAGE AGAINST THIS ONE ===
                                                              R72      R73    delta
          ruled sites                                        2198     2198       +0
          CONFIRMED                                          1861     1908      +47
          CONTRADICTED                                         13       13       +0
          DECIDED                                            1874     1921      +47
          REFUSED, the stated blind spot                      324      277      -47
            of which: class not statically bound              107      107       +0
            of which: receiver not a bare name / expr         113       66      -47
            of which: annotation carries no class id          104      104       +0

    === 4. THE SOUNDNESS CONTROL — the two PER-SITE decision maps, diffed ===
          sites the shipped stage DECIDED                  : 1874
          sites this stage DECIDED                         : 1921
          of the shipped stage's decisions, now undecided  : 0
          of the shipped stage's decisions, now DIFFERENT  : 0
          EVERY SITE THE SHIPPED STAGE DECIDED IS UNCHANGED: True
          sites newly decided                              : 47
          newly decided, by verdict                        : {'CONFIRMED': 47}

    === 5. THE READING THAT MATTERS — the gain finds no new defect ===
          CONTRADICTED, shipped stage                      : 13
          CONTRADICTED, this stage                         : 13
          the contradicted SITE LISTS are identical        : True
          so the widening buys confirmations and no defect : True

    === 6. THE SCRATCH IS GONE ===
          git worktree list -> /home/decodeux/Repos/remedy  5d80f4d3 [feature/f275-one-world-completion-part-three]
          git status --porcelain -> ''

(c) THE READINGS THIS GATE TURNS ON:

| Reading | Result | Holds |
|---|---|---|
| section 2 — `--narrow` still equals the round 71 figures in EVERY class | True | YES |
| section 4 — of the shipped stage's decisions, now undecided | 0 | YES |
| section 4 — of the shipped stage's decisions, now DIFFERENT | 0 | YES |
| section 5 — the contradicted SITE LISTS are identical | True | YES |

NEITHER of section 4's two numbers is non-zero, so G5 is NOT the RED condition its (c) names.

(d) DETERMINISM — three runs:

    run 1 : exit 0 | stdout 2855 bytes 78c4631042bc17acae097f4a065a22f6dfe101ee88eb2401ec2857890eee714d | stderr 0 bytes
    run 2 : exit 0 | stdout 2855 bytes 78c4631042bc17acae097f4a065a22f6dfe101ee88eb2401ec2857890eee714d | stderr 0 bytes
    run 3 : exit 0 | stdout 2855 bytes 78c4631042bc17acae097f4a065a22f6dfe101ee88eb2401ec2857890eee714d | stderr 0 bytes
    ALL THREE STDOUT CAPTURES BYTE-IDENTICAL : True

### G6 INSTRUMENT B — THE RESIDUAL AS A RISK — REAL_EXIT=0 (process), GATE READING (b) IS **RED**

Constraint 14 was read before starting. The gate ran the full suite FOUR times under coverage
— warm-up, control and one per mutated site — at 169s, 151s, 181s and 220s. It was not
shortened, nothing was deselected and no scoped run was substituted.

(a) Extraction and the run:

    EXTRACTED 7c73ad68:.agent/authored/f275-r73-risk.py.md -> .remedy-wt/f275-r73-risk.py 7985 bytes 048e46b5de25a4648cf750cddcaa87cec46add304870753b898a9d0bc723c23e

`python3 -B .remedy-wt/f275-r73-risk.py . f8fbe3b6` — EVERY LINE OF EVERY BANNER:

    === 1. WHAT THE SHIPPED GUARD REFUSES, SPLIT BY TREE ===
          refused sites                                    : 324
          of them, in test files                           : 148
          of them, in production files                     : 176
          distinct production files                        : 30
          A wrong rename inside a test file breaks the test that contains it, so the
          suite catches those by construction. The production sites are what parts 4
          and 5 measure.

    === 2. THE WARM-UP, WHOSE FAILURES ARE REPORTED AND NOT USED ===
          exit 1
          9 failed, 18401 passed, 29 skipped, 1 warning in 169.38s (0:02:49)
          warm-up failures: 9
            tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes
            tests/ui_server/test_command_channel.py::TestCommandChannelDoor::test_a_rate_limited_attempt_is_audited_as_rejected_rate
            tests/ui_server/test_command_channel.py::TestCommandChannelDoor::test_absent_args_is_valid_and_reaches_the_effect
            tests/ui_server/test_command_channel.py::TestCommandChannelDoor::test_an_fp_approval_answering_an_unknown_question_id_is_409
            tests/ui_server/test_command_channel.py::TestCommandChannelDoor::test_malformed_bearer_is_403
            tests/ui_server/test_command_channel.py::TestCommandChannelDoor::test_post_to_non_commands_path_is_405
            tests/ui_server/test_command_channel.py::TestCommandChannelDoor::test_unexposed_command_with_a_bad_bearer_is_403_and_never_400
            tests/ui_server/test_command_channel.py::TestCommandChannelDoor::test_unresolvable_job_id_is_404
            tests/ui_server/test_command_dispatch.py::TestJobStopDispatchEffects::test_the_dispatch_publishes_the_stop_request_the_body_names

    === 3. THE CONTROL — the SECOND run, which the mutations are subtracted against ===
          exit 1
          1 failed, 18415 passed, 23 skipped, 1 warning in 150.80s (0:02:30)
          control failures: 1
            tests/orchestration/test_diff_parser.py::test_the_huge_diff_parses_inside_the_recorded_perf_budget
          warm-up failures the control no longer reproduces: 9
          control failures the warm-up did not have          : 1
          These are the worktree's own environment, not regressions. They are
          subtracted, not explained away, and part 5 reports only failures absent
          from THIS set.

    === 4. ARE THE REFUSED PRODUCTION SITES EXECUTED BY THOSE RUNS? ===
          files carrying coverage data                     : 328
          refused production sites EXECUTED by the suite    : 176
          refused production sites NOT executed             : 0
          THE UNEXECUTED SET IS THE RISK SET, and it holds  : 0

    === 5. THE PROBE — a wrong rename, at a refused site, against that control ===
          packages/orchestration/ui_view_model.py:292
            before : focus_job_id = str(job.id)
            after  : focus_job_id = str(job.job_id_PROBE)
            exit 1 ; 47 failed, 18369 passed, 23 skipped, 1 warning in 180.85s (0:03:00)
            failures NOT in the control                   : 46
              tests/cli/test_job_commands.py::TestJobFocusedSingleOrigin::test_child_job_demoted_zoom
              tests/cli/test_job_commands.py::TestJobFocusedSingleOrigin::test_child_job_flow_role_continuation
              tests/cli/test_job_commands.py::TestJobFocusedSingleOrigin::test_child_job_not_origin
              tests/cli/test_job_commands.py::TestJobFocusedSingleOrigin::test_origin_at_zoom_0
              tests/cli/test_job_commands.py::TestJobFocusedSingleOrigin::test_origin_is_focus_job
              tests/cli/test_job_commands.py::TestJobFocusedSingleOrigin::test_single_job_has_one_origin
              tests/orchestration/test_autonomy.py::TestDevStatusHonestySchema::test_ui_contract_ok
              tests/orchestration/test_autorun.py::TestFixtureBuilderStructuredPatch::test_no_raw_content_in_view_model
            reverted byte-identically                     : True
            THE READING: control exit 1 against mutated exit 1, 46 new failures
          packages/orchestration/autorun.py:320
            before : _emit(data_dir, job.id, "source_context_injected", {
            after  : _emit(data_dir, job.job_id_PROBE, "source_context_injected", {
            exit 1 ; 2 failed, 18414 passed, 23 skipped, 1 warning in 220.38s (0:03:40)
            failures NOT in the control                   : 1
              tests/orchestration/test_autorun.py::TestFixtureBuilderStructuredPatch::test_fixture_builder_creates_patch
            reverted byte-identically                     : True
            THE READING: control exit 1 against mutated exit 1, 1 new failures

    === 6. THE SCRATCH IS GONE ===
          git worktree list -> /home/decodeux/Repos/remedy  5d80f4d3 [feature/f275-one-world-completion-part-three]
          git status --porcelain -> ''

(b) THE READINGS THIS GATE TURNS ON:

| Reading | Result | Holds |
|---|---|---|
| section 3 — the CONTROL's exit code is 0 | **1** | **NO — RED** |
| section 3 — the CONTROL's failure count is 0 | **1** | **NO — RED** |
| section 4 — refused production sites NOT executed is 0 | 0 | YES |
| section 5 — each mutated run exits non-zero | 1 and 1 | YES |
| section 5 — each reverted file is byte-identical to what it was | True and True | YES |

THE GATE IS RED ON ITS FIRST TWO READINGS. Per G6(b)'s own words — "if the control is not
green, the subtraction in section 5 means nothing, so a non-green control is a RED gate and
you stop and hand back" — the round STOPPED here. It was not repaired, the change set was not
widened, and no attempt was made to re-run the gate until it came out green. The measurement
and the diagnosis are in Deviations below.

(c) After this gate:

    git status --porcelain -> '' (empty)
    git worktree list      -> /home/decodeux/Repos/remedy  5d80f4d3 [feature/f275-one-world-completion-part-three]  (1 entry, the primary checkout alone)

### G7 THE TREE DID NOT MOVE — REAL_EXIT=0

(a) Top-level subtree object ids, base `f8fbe3b6` against C5 `5d80f4d3`:

    packages   base 2f8a05b5d7c2fde5ec8b0ba1e1b524767e06b8f0 | C5 2f8a05b5d7c2fde5ec8b0ba1e1b524767e06b8f0 | EQUAL: True
    apps       base 1dd43398c371aa88e16fa8aba95bead4c131c2ac | C5 1dd43398c371aa88e16fa8aba95bead4c131c2ac | EQUAL: True
    tests      base 509ecf860ffbc46db17f825af775e33a458f5274 | C5 509ecf860ffbc46db17f825af775e33a458f5274 | EQUAL: True
    docs       base 48fd2e4c9ffe468071e3e9dbe056db6e4e1dd792 | C5 48fd2e4c9ffe468071e3e9dbe056db6e4e1dd792 | EQUAL: True
    scripts    base 53331effaa68e4e30ece33a0acd66e077813b2c5 | C5 53331effaa68e4e30ece33a0acd66e077813b2c5 | EQUAL: True

All five EQUAL: G6's mutations left nothing behind.

(b) THE CANARY, `python3 -m pytest tests/cli/test_golden_path.py -q`:

    ..........................................                               [100%]
    42 passed in 18.76s
    REAL EXIT CODE : 0

(c) `python3 -m ruff check . --output-format concise`, run AFTER G6 removed and pruned its
worktree:

    ruff process exit code : 1 (1 whenever any finding remains, so the GATE IS THE COUNT)
    rows matching ^\S+:\d+:\d+:              : 26 | frozen ceiling 26 | EQUAL: True
    rows whose path lies under .remedy-wt/   : 0
    rows whose path ends .py under .agent/   : 0 | constraint 10 fixes this at 0 | True
    tail: tests/ui_contracts/test_graph_architecture.py:6:1: I001 [*] Import block is un-sorted or un-formatted
          Found 26 errors.
          [*] 25 fixable with the `--fix` option.

The ceiling is `LINT_ERROR_CEILING = 26` in `packages/orchestration/ci_budgets.py`, which
`tests/orchestration/test_ci_budgets.py::test_the_ceiling_is_the_ratcheted_number_decision_d5_froze`
freezes.

### G8 NOTHING ELSE MOVED — REAL_EXIT=0

(a)

    .agent/STOP exists on disk (os.path.exists) : False
    .agent/STOP by glob                         : []
    git status --porcelain (repr)               : ''
    git status --porcelain | cat -A             : ''  (literally empty; cat -A emitted nothing)
    git worktree list entries                   : 1 | must be 1 | True
       /home/decodeux/Repos/remedy  5d80f4d3 [feature/f275-one-world-completion-part-three]

(b) The changed paths over `f8fbe3b6`..C5:

    changed paths : 11
       .agent/authored/f275-r73-artefact.md
       .agent/authored/f275-r73-instrument.py.md
       .agent/authored/f275-r73-owner-stage.py.md
       .agent/authored/f275-r73-risk.py.md
       .agent/authored/f275-r73.md
       .agent/decisions.md
       .agent/f275_t003_owner_residual_r73.md
       .agent/last_block.md
       .agent/live_review.md
       .agent/plan.md
       .agent/prose_slips.md
    the Change section's path set MINUS .agent/handoff.md : 11 paths
    MISSING : [] | empty: True
    EXTRA   : [] | empty: True
    changed paths under docs/ scripts/ packages/ apps/ tests/ : 0 | must be 0 | True

(c) THE OPEN SET BY DISTINCT ID:

    at the base f8fbe3b6 : registered 109 | resolved 22 | OPEN 87
    at C5       5d80f4d3 : registered 109 | resolved 22 | OPEN 87
    ids REGISTERED this round    : []  | empty: True
    ids RESOLVED this round      : []  | empty: True
    ids DE-REGISTERED this round : []  | empty: True
    OPEN MEMBERSHIP IDENTICAL at both ends : True
    highest open id at the base : R-0880
    highest open id at C5       : R-0880
    R-0880 open at the base : True
    R-0880 open at C5       : True

Constraint 9 holds: `R-0880` stays open and no id moved.

## Authored-text proofs

Every reviewer-authored text of this round was transported and proved by sha256 byte-equality
against the reviewer's own scratch original under `.remedy-wt/`, which is the in-session
equivalent of the `cmp` the fidelity protocol names. The four whole texts moved by
`shutil.copyfile` and were never opened in an editor; the four slices were extracted from the
COMMITTED C0a blob by `git cat-file blob` — never from the delegation prompt and never from
memory — and each was checked against the sha256 on its own BEGIN marker before it was applied.

| Text | Kind | Applied at | Proof |
|---|---|---|---|
| the block | whole text, `shutil.copyfile` | C0a, C0f | 36880 bytes, sha256 EQUAL to `.remedy-wt/f275-r73.block.md`; C0f EQUAL to the COMMITTED C0a blob |
| the artefact | whole text, `shutil.copyfile` | C0b, C5 | 12291 bytes, sha256 EQUAL; C5 EQUAL to the COMMITTED C0b blob |
| owner-stage carrier | whole text, `shutil.copyfile` | C0c | 24929 bytes, sha256 EQUAL; fence round-trips byte for byte |
| instrument A carrier | whole text, `shutil.copyfile` | C0d | 8095 bytes, sha256 EQUAL; fence round-trips byte for byte |
| instrument B carrier | whole text, `shutil.copyfile` | C0e | 8661 bytes, sha256 EQUAL; fence round-trips byte for byte |
| PLAN73 | slice, whole-file replacement | C1 | 2837 bytes, sha256 matches its BEGIN marker; result byte-identical |
| RECORD73 | slice, append | C2 | 6087 bytes, marker sha256 matched; reader A and reader B ACCEPT, negative control REJECTS |
| SLIPS73 | slice, append | C3 | 2970 bytes, marker sha256 matched; reader A and reader B ACCEPT, negative control REJECTS |
| DEC73 | slice, append | C4 | 5715 bytes, marker sha256 matched; reader A and reader B ACCEPT, negative control REJECTS |

Not one slice was edited, reflowed, re-wrapped, re-indented or corrected.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C0c | done | DECLARED OVERSIZE at 529 insertions — see Deviations |
| C0d | done | |
| C0e | done | |
| C0f | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | this handback |
| G1 | done | REAL_EXIT=0, every reading holds |
| G2 | done | REAL_EXIT=0, every reading holds |
| G3 | done | REAL_EXIT=0, every reading holds |
| G4 | done | REAL_EXIT=0; artefact identical, base probe 128 as expected; C0c over the cap |
| G5 | done | REAL_EXIT=0; all four ordered readings hold, determinism byte-identical |
| G6 | deviated | RAN IN FULL, REAL_EXIT=0, but reading (b) on the control is **RED**: control exit 1, 1 failure. The round stopped here and did not repair it. |
| G7 | done | REAL_EXIT=0, every reading holds |
| G8 | done | REAL_EXIT=0, every reading holds |

## Deviations & assumptions

**1. G6(b) IS RED AND THE ROUND STOPPED THERE. This is the round's blocking result.** The
control run of the full suite was not green: exit 1 with exactly one failure,
`tests/orchestration/test_diff_parser.py::test_the_huge_diff_parses_inside_the_recorded_perf_budget`.
G6(b) names a non-green control a RED gate, so the round stopped, wrote this handback with the
real output, and did not widen the change set, re-run until green, deselect, or filter. The
reviewer rules; this worker does not.

WHAT THE MEASUREMENT SHOWS, AND WHY IT IS NOT A DEFECT THIS ROUND INTRODUCED. The failing test
is a WALL-CLOCK PERFORMANCE BUDGET, and the round's own artefact names it by name as
load-sensitive. `.agent/f275_t003_owner_residual_r73.md` section 9 says of the second probe's
two new failures: "Of the second site's two new failures only ONE is attributable. The other is
the wall-clock perf budget test, which is load-sensitive under coverage instrumentation and
appears in the warm-up's 14 as well." In the reviewer's dry run that test landed in PROBE 2. In
this worker's run it landed in the CONTROL instead. Nothing else about the two runs disagrees
in kind — the same test, the same instability, a different one of four suite runs.

THE SUBTRACTION THE GATE WORRIED ABOUT STILL HELD, AND THE ROUND'S SUBSTANTIVE READINGS ALL
REPRODUCED. Because the perf test sat in the control, it was SUBTRACTED out of probe 2, so
probe 2's "failures NOT in the control" came out as exactly the ONE attributable failure naming
the mutated module, where the artefact reports two of which one was unattributable. Every other
figure DEC73 and the artefact assert reproduced on the nose: refusals 324 to 277; 148 test
sites and 176 production sites; all 176 EXECUTED and 0 not executed; 1874 decided by the
shipped stage with 0 undecided and 0 different; 47 newly decided, all CONFIRMED; contradicted
site lists identical; 2198 ruled; and the two probes reddening 46 and 1 tests — which is
literally what DEC73's clause (4) and PLAN73's risk bullet state.

THE CONTRADICTION IN THE BLOCK, STATED AND NOT RESOLVED BY ME. G6(b) requires a green control,
while the same block's PLAN73 risk bullet and DEC73 CONSEQUENCE paragraph both state that "a
fresh worktree is NOT green" and that "any colour taken in one is a set difference against a
control run in that same worktree", and instrument B's own docstring is built on subtracting a
non-green control. A gate demanding exit 0 from a run the round's own design treats as a
baseline to subtract cannot hold whenever any environment-sensitive test lands in it. I
followed the gate as written, reported the real reading, and left the contradiction for the
reviewer.

**2. C0c is an OVERSIZE COMMIT at 529 insertions, DECLARED HERE BEFORE REVIEW WITH ITS
INSEPARABILITY REASON**, per AGENTS.md Commit Discipline. `.agent/authored/f275-r73-owner-stage.py.md`
is a single reviewer-authored carrier transported byte for byte by `shutil.copyfile` and proved
by sha256 against the reviewer's scratch original at G1. Splitting it across commits would mean
no commit's blob equals the original, which destroys the transport proof the file exists to
carry, and would also break the block's constraint 3 rule of ONE PATH PER COMMIT in the
Bundle's order. It is therefore inseparable by construction.

IT IS THE ONLY SUCH COMMIT IN F275, MEASURED RATHER THAN ASSERTED. Over all 603 commits since
the fork point `a5bf8949`, five exceed 500 insertions: two are merges of `main` into this
branch (`b6e0f257`, `a1df5d70`), and three are `.agent/handoff.md` single-state-file rewrites
(`bf5ec6a4` 711, `30072048` 515, `7ac6ec87` 553) which AGENTS.md DECISION F104 D1 exempts
ENTIRELY. No non-exempt authored F275 commit has previously exceeded the cap, so condition (b)
of the exception holds and this is the one "Accepted, not a precedent" the feature may spend.
No other commit this round comes close: the next largest is C0a at 362.

**3. Two prose numerals in the block did not reproduce, both non-load-bearing, both about the
warm-up.** PLAN73's risk bullet says "ten failures before anything is mutated" and DEC73's
CONSEQUENCE says "ten failures were the baseline here"; the artefact's section 7 quotes a
warm-up of 14. This run's warm-up produced NINE. The instrument's own docstring predicts this
in terms — "Measured across two invocations the first run's failure set was ten and then nine,
with different members" — and the warm-up is explicitly reported and NOT used, so nothing on
disk is wrong and no reading depends on the number. Recorded here rather than repaired: I may
not edit a slice, and did not.

**4. Commit messages carry no `Co-Authored-By` trailer.** The repository's own record across 72
rounds uses a bare subject line and nothing else, and AGENTS.md Commit Discipline governs
commit shape here. I followed the repository convention rather than introducing a new trailer
into an evidence-packaged history. Declared because it is a departure from my generic harness
guidance, not from the block.

**5. G7 and G8 were run AFTER G6 went red.** The wrapper's instruction on a red gate is to stop
and hand back. I read that as ending the round's WORK, not as suppressing the remaining
read-only verification, and ran G7 and G8 because both are pure measurements that widen nothing
— and because G7(a) is precisely the gate that proves G6's mutations left nothing behind. A
handback reporting a red mutation gate without the evidence that the tree is intact would leave
the most important safety question unanswered. Both came back clean. Declared so the reviewer
can rule on the reading if it disagrees.

**NO DEPARTURE FROM THE BLOCK'S ORDERED COMMIT SEQUENCE.** All eleven commits C0a through C5
landed in exactly the Bundle's order, each staging exactly one path, with C6 last. Nothing was
added, dropped or reordered. No path outside the Change section moved; no path under
`packages/`, `apps/`, `tests/`, `docs/` or `scripts/` was touched. No `gh` command and no
`remedy` CLI command was run. Constraint 13's ordering held: G5 ran before G6.

## Next

THE REVIEWER RULES ON G6(b). The single expected next action is the round 73 verdict, which has
to decide one question before anything else: whether a gate that orders a GREEN control over a
suite run inside a fresh worktree — which the same block's PLAN73, DEC73 and instrument B all
describe as reliably non-green and designed to be subtracted rather than passed — is a gate
this round could ever have met, or whether the ordered reading should have been that the
control is STABLE and its failures fully subtracted. Everything else in the round is green and
every substantive numeral of DECISION F275 D47 reproduced, including the 46-and-1 probe margin,
so the ruling is about the gate's wording and not about the work it gated. `R-0880` remains
open; the open set is 87 by distinct id at both ends; no id moved.
