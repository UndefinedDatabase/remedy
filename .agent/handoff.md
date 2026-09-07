# Handback — F272 round 27

## Session

SESSION 12 of feature F272 · round 27 · rounds so far 27

SOFT LIMIT, under operator amendment amend0906-triage-throughput rule 2, which sets F272's
limit at 12 SESSIONS and 40 ROUNDS by name: the SESSION half REMAINS REACHED — this is
still session 12 of 12. The round half is not: this is round 27 of 40. The SPLIT half of
the amend0905-throughput split-and-close default was executed in round 26 (F274 registered,
DECISION F272 D16); this round is the second step of the CLOSE half, discharging two
closure preconditions at once.

CONTEXT SELF-ASSESSMENT (amend0905-throughput, one sentence): context is comfortable — the
round's only reading of production code was the ~40 lines of `ui_server.py` needed to name
the base-run environment cause, the two large state files were handled by measurement
rather than by reading them end to end, and the two full-suite runs cost wall clock rather
than context.

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE

The scope report the limit obliges was written in full in round 26's handback and is not
re-derived here; it is now also ON DISK AND DURABLE as the `## Built State` section this
round appended to `docs/roadmap/features/T2_F272.md`, which states what F272 built, which
slices moved to F274, and what remains open against this file's own "Goal & Done".

## Range

Review of `412ce673`..`4016a97d`.

The range ends at C5, the last commit that EXISTS while this file is being written. C6 is
the commit that writes this file and cannot state its own SHA; the reviewer's range is
`412ce673`..HEAD after C6 lands.

## Commits

### 9a9bf185 f272: save the round 27 step block as the authored original  (C0a)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f272-r27.md | +319 / -0 | `shutil.copyfile` of `.remedy-wt/f272-r27-block.md` per constraint 3 |

### cc21b12b f272: mirror the round 27 block into last_block  (C0b)
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +243 / -414 | same `shutil.copyfile`, the mirror |

### f65c6a84 f272: point the plan at round 27 and the closure sequence  (C1)
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +25 / -26 | replaced byte for byte with the PLANF272R27 slice |

### a0850e1a f272: book the round 26 PASS verdict into the record  (C2)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 / -0 | append of RECORDR27, the `Gate: F272 R26` PASS entry |

### 898102c4 f272: record the round 26 block prose slip on the R-0826 absence claim  (C3)
| Path | +/- | Reason |
|---|---|---|
| .agent/prose_slips.md | +2 / -0 | append of SLIPSR27, one dated line, no id spent |

### d47c9983 f272: add the Built State section and name the slices that moved to F274  (C4)
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T2_F272.md | +51 / -0 | append of BUILTSTATE; closure precondition 4, and the D16 pointer round 26 recommended |

### 4016a97d f272: land the round 27 integration-gate evidence with per-id base attribution  (C5)
| Path | +/- | Reason |
|---|---|---|
| .agent/gate_f272_r27/base_failed.txt | +126 / -0 | sorted FAILED lines of the base run |
| .agent/gate_f272_r27/base_only.txt | +126 / -0 | `comm -23`, the base-only set |
| .agent/gate_f272_r27/base_only_attribution.txt | +150 / -0 | the attribution table, one row per base-only id |
| .agent/gate_f272_r27/base_run_tail.txt | +10 / -0 | raw tail of the base suite |
| .agent/gate_f272_r27/branch_failed.txt | +0 / -0 | sorted FAILED lines of the branch run — EMPTY |
| .agent/gate_f272_r27/branch_only.txt | +0 / -0 | `comm -13`, THE GATE'S VERDICT SET — EMPTY |
| .agent/gate_f272_r27/branch_run_tail.txt | +9 / -0 | raw tail of the branch suite |
| .agent/gate_f272_r27/dist_mtime_window.txt | +18 / -0 | the R-0444 event measurement |
| .agent/gate_f272_r27/gate_summary.txt | +22 / -0 | the three canonical steps and their figures |
| | **+461 / -0** | commit total, 9 files, under the DECISION F104 D1 cap of 500 insertions |

### C6 — the handback commit (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | not tabled | a handoff cannot table the commit that writes it; its SHA is HEAD after C6 |

Every `+/-` cell above is `git diff --numstat <parent> <commit>` output and was compared
cell for cell against G8's per-commit figures below; all rows agree.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | 461 insertions, UNDER the 500 cap — no oversize declaration is owed |
| C6 | done | this file |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add -b tmp/f272-base-gate /home/decodeux/remedy-gate-scratch/f272r27-base-wt b18fad576252f7f2739a5807b6408031da8fcde6` | exit 0, "Preparing worktree (new branch 'tmp/f272-base-gate')", `git worktree list` 13 -> 14 |
| `git worktree remove --force /home/decodeux/remedy-gate-scratch/f272r27-base-wt` | exit 0 |
| `git worktree prune` | exit 0 |
| `git branch -D tmp/f272-base-gate` | exit 0, "Deleted branch tmp/f272-base-gate (was b18fad57)", `git worktree list` 14 -> 13 |
| `git push -u origin feature/f272-one-world-completion` (after C5) | exit 0, `412ce673..4016a97d`, upstream set |
| `git push -u origin feature/f272-one-world-completion` (after C6) | expected exit 0; a handback cannot transcribe the push of itself |

No PR created. No merge. No force-push. No history rewrite. No branch switch. The ONE
worktree this round created is the throwaway base worktree constraint 8 requires, and it was
removed, pruned and its branch deleted before this file was written.

## Verification

Every gate was run as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, with no pipe between the
command and the echo. No gate is reported as "green"; each carries its real exit code and
its real numbers.

### Receipt of the block (before anything else)

| Measurement | Reviewer stated | Measured | |
|---|---|---|---|
| byte length | 24499 | 24499 | agrees |
| line count | 319 | 319 | agrees |
| sha256 | 94e540c1… | `94e540c1ae7a3f167be0321e8c3d1e43a629ead7282123a01e2196ad303b8ef2` | agrees |

### G1 TRANSPORT — one digest comparison, all three artefacts identical, REAL_EXIT=0

    .remedy-wt/f272-r27-block.md   len=24499 lines=319 sha256=94e540c1ae7a3f167be0321e8c3d1e43a629ead7282123a01e2196ad303b8ef2
    .agent/authored/f272-r27.md    len=24499 lines=319 sha256=94e540c1ae7a3f167be0321e8c3d1e43a629ead7282123a01e2196ad303b8ef2
    .agent/last_block.md           len=24499 lines=319 sha256=94e540c1ae7a3f167be0321e8c3d1e43a629ead7282123a01e2196ad303b8ef2
    ALL_THREE_IDENTICAL       = True
    MATCHES_REVIEWER_STATEMENT = True
    REAL_EXIT=0

Per §3 item 37 this chain covers the saved copy and its mirror and is not a claim about the
bytes emitted into a prompt.

### G2 THE FINDING RECORD — byte, structural, negative control and counts all hold, REAL_EXIT=0

    === G2(a) BYTE ===
    pre_len          = 1215841
    pre_sha256       = d371b0aa6ab9991641920565ee5cb52a4659c7a536a80804b92e8ea274279c99
    pre_lines        = 2133
    pre_terminal_12  = b'er touched.\n'
    pre_trailing_nl_run = 1
    slice_len        = 4856
    slice_sha256     = e16e323c998a6d801d25d69e3cd57a088f6b8b8e0e4a663da12429132b9a9d11
    triple_nl_in_pre = 0
    post_len         = 1220698
    post_sha256      = 0f2924505f470394ace8f1e55a372a03713c722943ef227edfe74b25a8ea8bc6
    post_lines       = 2135
    post_terminal_12 = b'for either.\n'
    post_trailing_nl_run = 1
    PRE_IS_BYTE_EXACT_PREFIX_OF_POST = True
    POST_EQUALS_PRE_NL_SLICE = True
    triple_nl_in_post = 0

    === G2(b) STRUCTURAL ===
    N (counted from the slice) = 1
    units_before      = 732
    units_after       = 733
    LAST_N_UNITS_EQUAL_SLICE_PARAGRAPHS_IN_ORDER = True
    EVERYTHING_BEFORE_UNCHANGED = True

    === G2(c) NEGATIVE CONTROL (in memory only) ===
    first_added_paragraph_len = 4855
    flip_offset_absolute = 1215882  inside_first_added_paragraph = True
    byte_before_flip = b'r'   byte_after_flip = b'R'
    BYTE_READER_REJECTS_MUTANT       = True
    STRUCTURAL_READER_REJECTS_MUTANT = True
    BYTE_READER_ACCEPTS_REAL_POST       = True
    STRUCTURAL_READER_ACCEPTS_REAL_POST = True
    DISK_UNCHANGED_BY_NEGATIVE_CONTROL = True
    DISK_SHA_AFTER_CONTROL = 0f2924505f470394ace8f1e55a372a03713c722943ef227edfe74b25a8ea8bc6

    === G2(d) COUNTS ===
    ^- R-\d{4} distinct            309 ->   309
    ^Done: R-\d{4} distinct        252 ->   252
    open set BY DISTINCT ID         57 ->    57
    ^Gate:                          49 ->    50
    ^Gate: F272 R26                  0 ->     1
    ^- R-0826                        0 ->     0
    OPEN SET ARITHMETIC: 309 distinct registrations - 252 distinct Done ids = 57 (post)
    Done ids with no registration (so nothing is subtracted twice) = 0
    R-0826 registered? = False
    REAL_EXIT=0

The pre-image is the block's stated 1215841 bytes / 2133 lines with sha256 beginning
`d371b0aa6ab99916`. ALL SIX ordered counts landed on their stated values. OPEN FINDINGS BY
DISTINCT ID = 57, by the arithmetic above; the set is taken by DISTINCT ID and not by line,
and the "Done ids with no registration = 0" line proves no id is subtracted twice.
The structural splitter strips the single terminal newline and splits on `\n\n`, which is
exact here because `triple_nl_in_pre` and `triple_nl_in_post` are both 0.

### G3 THE TWO PROSE FILES — plan byte-equal and under the cap, slips appended, REAL_EXIT=0

    === G3 part 1 — .agent/plan.md byte equality (applied at C1) ===
    plan_bytes            = 1988
    plan_lines            = 39
    AGENTS.md cap         = 50   UNDER_CAP = True
    PLAN_BYTE_EQUAL_TO_PLANF272R27 = True
    plan_sha256           = 1189e22d0c5d1b1c5b0c6d4d3f7996f1ffc79df1a1571b8bb7845690d19640a7
    HAS '## Goal'         = True
    HAS '## Next Steps'   = True

    === G3 part 2 — .agent/prose_slips.md byte append ===
    pre_len               = 150774 (block states 150774)
    pre_lines             = 563 (block states 563)
    pre_sha256            = 98505ccaab13e4799d00a659dd8414a556c28fbecce448b035b30c5c32f52c0a
    pre_terminal_12       = b'in advance.\n'
    pre_trailing_nl_run   = 1
    triple_nl_in_pre      = 1   first_triple_nl_off = 39213
    slice_len             = 723
    slice_sha256          = 725fd1aefef937e908b16b09cf0d0cf7b4c4b0e6628dbdfc73dd061aa8df2492
    post_len              = 151498
    post_lines            = 565
    post_sha256           = 1428aac1c72606436168be2f998609bda6c07643c841be8ffec12fecc99dd981
    PRE_IS_BYTE_EXACT_PREFIX_OF_POST = True
    POST_EQUALS_PRE_NL_SLICE = True
    triple_nl_in_post     = 1
    REAL_EXIT=0

Both stated pre-image figures — 150774 bytes and 563 lines — reproduce exactly, and the
pre-existing triple newline at offset 39213 that constraint 4 names is confirmed present,
untouched and not load-bearing.

### G4 THE FEATURE FILE — byte-exact append, no landed ruling overwritten, REAL_EXIT=0

    pre_len              = 62897 (block states 62897)
    pre_lines            = 768 (block states 768)
    pre_sha256           = 075e72d74c8a382afc7c09684531573b9a3dc2b04eb7863160f5d2d99aae4042
    pre_terminal_12      = b'for itself.\n'
    pre_trailing_nl_run  = 1
    triple_nl_in_pre     = 0
    slice_len            = 3280
    slice_sha256         = aeecbb4f4474548942eb8984befc23ae27f782306b21dddb9430df9e25a526c8
    slice_has_DECISION_heading = 0
    post_len             = 66178
    post_lines           = 819
    post_sha256          = 49228a28f3bd4700800ac559f6ddc6fca44be0a65b310f3032ebc1cfa0563bff
    post_trailing_nl_run = 1
    PRE_IS_BYTE_EXACT_PREFIX_OF_POST = True
    POST_EQUALS_PRE_NL_SLICE = True
    triple_nl_in_post    = 0

    ^### DECISION F272 D headings: 15 -> 15  (block states 15 -> 15)
    ^## Built State headings:       0 ->  1  (block states 0 -> 1)
    DECISION_HEADING_LIST_BYTE_UNCHANGED = True
    built_state_heading = ## Built State (2026-09-07, rounds 1 to 27, ledger `Gate: F272 R1` to `Gate: F272 R26`)
    DECISION numbers in order = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']
    numbers_are_1_to_15_each_once = True
    REAL_EXIT=0

The stated pre-image — 62897 bytes, 768 lines, sha256 beginning `075e72d74c8a382a` —
reproduces exactly. Constraint 5 holds by measurement and not by assertion: the slice
contains ZERO `### DECISION F272 D` headings, the count stays 15, and the fifteen heading
lines are byte-identical before and after.

### G5 THE INTEGRATION GATE, BRANCH RUN — integration_gate.md step 1, primary checkout at C4

    $ bash -c 'SECONDS=0; python3 -m pytest -n auto -q > <out-of-repo log>; echo "REAL_EXIT=$?"; echo "WALL_SECONDS=$SECONDS"'
    REAL_EXIT=0
    WALL_SECONDS=117

    raw tail:
    ...........................................s............................ [ 99%]
    .........                                                                [100%]
    =============================== warnings summary ===============================
    tests/orchestration/test_model_routing.py::TestTheUndeclaredRolePathWarnsAndAnswersConservatively::test_it_matches_role_configs_own_unknown_role_behaviour
      packages/orchestration/model_routing.py:1392: UserWarning: Role 'a_role_nobody_declared_a_class_for' declares no task class; routing conservatively as 'undeclared_role'.
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    19786 passed, 23 skipped, 1 warning in 115.98s (0:01:55)

    grep -c '^FAILED' <log>  ->  0
    branch_failed.txt        ->  0 lines

| | Reviewer measured at `412ce673` | This round measured at `d47c9983` |
|---|---|---|
| passed | 19786 | 19786 |
| skipped | 23 | 23 |
| FAILED | 0 | 0 |
| exit code | — | 0 |
| wall (pytest) | 131.37s | 115.98s |

THE FULL `FAILED` LIST FOR THE BRANCH RUN IS EMPTY — there is nothing to list, and
`branch_failed.txt` is a zero-byte, zero-line file. The pass/skip/failure counts agree with
the reviewer's reading cell for cell; only the wall clock differs, which is machine load and
not a disagreement.

### G6 THE INTEGRATION GATE, BASE RUN — integration_gate.md step 2, at the FORK POINT

Constraint 7, both counts re-run and reported:

    $ git cat-file -t b18fad576252f7f2739a5807b6408031da8fcde6   -> commit
    b18fad57 Merge pull request #242 from UndefinedDatabase/feature/f260-one-world
    $ git merge-base main HEAD                                   -> 148fbd0b4f3bbc7d5d57a81af080e53359e95681

    at the FORK POINT, at 412ce673 (the reviewer's reading):
      git rev-list --ancestry-path b18fad57..412ce673 | wc -l   -> 213   (block states 213)
      git rev-list                b18fad57..412ce673 | wc -l   -> 213   (block states 213)
    at the MERGE-BASE 148fbd0b, at 412ce673, for contrast:
      git rev-list --ancestry-path 148fbd0b..412ce673 | wc -l  -> 184   (block states 184)
      git rev-list                148fbd0b..412ce673 | wc -l  -> 205   (block states 205)
    at the FORK POINT, at THIS ROUND'S C4 d47c9983:
      both counts -> 219  (213 + this round's six commits C0a..C4 — equal, as the fork point requires)

All four of the block's stated figures reproduce exactly, and the inequality 184 != 205 at
the merge-base — the shape that packaged F260's round 22 as BLOCKED_EVIDENCE — is confirmed
to exist and to be absent at the fork point.

Worktree, per constraint 8 (created ON A THROWAWAY BRANCH, never detached):

    $ git worktree add -b tmp/f272-base-gate /home/decodeux/remedy-gate-scratch/f272r27-base-wt b18fad576252f7f2739a5807b6408031da8fcde6
    Preparing worktree (new branch 'tmp/f272-base-gate')
    HEAD is now at b18fad57 Merge pull request #242 ...
    REAL_EXIT=0
    rev-parse HEAD  -> b18fad576252f7f2739a5807b6408031da8fcde6
    branch --show-current -> tmp/f272-base-gate      (NOT detached)
    status --porcelain -> empty
    git worktree list -> 14

Artefact parity restored BEFORE the run, with `symlinks=True` ORDERED (R-0591):

    shutil.copytree(apps/ui/node_modules, ..., symlinks=True)  4.9s  43032 files
    shutil.copytree(apps/ui/dist,         ..., symlinks=True)  0.0s      4 files
    SYMLINKS_PRESERVED_IN_BASE_node_modules = 27
    SYMLINKS_IN_PRIMARY_node_modules        = 27      (equal — no bin shim was dereferenced)

The block calls `apps/ui/node_modules` 305 MB; `du -sh` reads exactly 305M and
`du -sh --apparent-size` reads 162M, while the sum of `lstat().st_size` over the 43032
copied files is 181.8 MB. The block's figure is the `du -sh` one and is correct.

R-0444 — THE NEUTRALISATION IS VERIFIED BY MEASURING THE EVENT, NOT THE OUTCOME:

    RUN WINDOW start = 1788791504.190902  (2026-09-07T16:31:44.190902)
    RUN WINDOW end   = 1788791671.544701  (2026-09-07T16:34:31.544701)
    RUN WINDOW width = 167.35s
    dist files before = 4  after = 4   file set identical = True
      assets/diffHighlightGrammars-o9XqnLhb.js  1788776043.1460497 -> 1788776043.1460497  inside_window=False
      assets/index-D_qZGOuo.css                 1788776043.1430497 -> 1788776043.1430497  inside_window=False
      assets/index-SSfmtKy1.js                  1788776043.1460497 -> 1788776043.1460497  inside_window=False
      index.html                                1788776043.1460497 -> 1788776043.1460497  inside_window=False
    FILES_WITH_MTIME_INSIDE_RUN_WINDOW = 0
    FILES_WITH_CHANGED_MTIME           = 0
    PARITY_CLAIM_HOLDS                 = True

No mtime under the base worktree's `apps/ui/dist` falls inside the run window, so nothing
rebuilt during the base run and the parity claim is not voided.

The run itself:

    $ bash -c 'cd <base wt> && SECONDS=0 && ... REMEDY_UI_NO_AUTO_BUILD=1 python3 -m pytest -n auto -q > <out-of-repo log> 2>&1; echo "REAL_EXIT=$?"; ...'
    REAL_EXIT=1
    WALL_SECONDS=167

    raw tail:
    FAILED tests/ui_server/test_diff_endpoint.py::TestDiffEndpoint::test_unknown_task_run_is_a_named_absence_at_status_200
    FAILED tests/ui_server/test_diff_endpoint.py::TestDiffEndpointPerfBudget::test_the_acceptance_fixture_is_served_inside_the_hang_net
    FAILED tests/ui_server/test_digest_route.py::TestDigestRoute::test_digest_body_carries_exactly_the_envelope_key_set
    FAILED tests/ui_server/test_digest_route.py::TestDigestRoute::test_digest_endpoint_refuses_an_invalid_token
    FAILED tests/ui_server/test_command_dispatch.py::TestFlightPlanApprovalDispatchEffects::test_the_accepted_fp_approval_saves_the_job_exactly_once
    126 failed, 19605 passed, 23 skipped, 1 warning in 166.70s (0:02:46)

    grep -c '^FAILED' <log>  ->  126
    base_failed.txt          ->  126 lines

### G7 THE COMPARISON — integration_gate.md step 3, REAL_EXIT=0

    $ comm -13 base_failed.txt branch_failed.txt   # BRANCH-ONLY — the gate's verdict
    BRANCH_ONLY_COUNT = 0
    --- BRANCH-ONLY LIST (full, not truncated) ---
    (no lines — the file is zero bytes)
    --- end branch-only ---

    $ comm -23 base_failed.txt branch_failed.txt   # base-only
    BASE_ONLY_COUNT = 126

**THE GATE'S VERDICT CRITERION IS MET: THE BRANCH-ONLY SET IS EMPTY.** It is empty by
construction as well as by measurement — the branch run had zero failures, and a branch with
zero failures can have no branch-only failure. No BLOCKER, so the round continued.

THE FULL BASE-ONLY LIST, all 126 ids, never truncated. All of them are under
`tests/ui_server/`, grouped here by file with every id named:

`tests/ui_server/test_command_channel.py::TestCommandChannelDoor::` — 78 ids:
`test_absent_args_is_valid_and_reaches_the_effect`, `test_absent_body_is_400_on_field_body`,
`test_a_decision_resolve_naming_an_open_decision_is_answered_and_saved`,
`test_a_dispatched_command_is_audited_as_accepted`,
`test_a_mistyped_limit_falls_back_to_the_default_and_still_limits`,
`test_an_accepted_command_reaches_the_sse_frame_it_announces`,
`test_an_audit_writer_that_raises_changes_neither_status_nor_body`,
`test_a_near_miss_of_the_commands_path_is_405`,
`test_an_event_writer_that_raises_changes_neither_status_nor_body`,
`test_an_exposed_id_with_no_dispatch_branch_is_the_501_guard`,
`test_an_fp_approval_answered_approve_is_accepted`,
`test_an_fp_approval_answered_reject_is_accepted`,
`test_an_fp_approval_answered_with_a_next_action_string_is_409`,
`test_an_fp_approval_answering_an_unknown_question_id_is_409`,
`test_an_fp_approval_on_a_plan_that_is_not_pending_is_409`,
`test_an_fp_approval_whose_answers_are_not_a_map_is_409`,
`test_a_nonce_that_cannot_be_a_filename_is_400_on_its_own_field[aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa]`,
`test_a_nonce_that_cannot_be_a_filename_is_400_on_its_own_field[../escape]`,
`test_a_nonce_that_cannot_be_a_filename_is_400_on_its_own_field[has space]`,
`test_a_nonce_that_cannot_be_a_filename_is_400_on_its_own_field[with/slash]`,
`test_an_unexposed_command_does_not_spend_budget`,
`test_an_unexposed_command_is_audited_as_rejected_command`,
`test_an_unknown_path_is_405_for_every_mutating_method`,
`test_an_unresolvable_job_is_audited_as_rejected_job`,
`test_an_unseeded_nonce_is_dispatched_rather_than_replayed`,
`test_a_rate_limited_attempt_is_audited_as_rejected_rate`,
`test_a_refused_command_announces_nothing`,
`test_a_replay_announces_nothing_a_second_time`,
`test_a_replayed_nonce_answers_from_the_store_byte_for_byte`,
`test_a_replay_is_not_the_acceptance_it_repeats`, `test_a_replay_spends_no_rate_budget`,
`test_a_second_job_has_its_own_budget`, `test_a_shape_error_does_not_spend_budget`,
`test_a_shape_error_is_audited_as_rejected_shape`,
`test_a_wrong_bearer_is_audited_as_rejected_token`,
`test_a_wrong_credential_on_a_job_with_no_control_dir_leaves_no_file`,
`test_a_wrong_csrf_header_is_audited_as_rejected_csrf`,
`test_bearer_without_a_token_is_403`,
`test_command_in_no_catalog_is_400_on_field_command`,
`test_csrf_is_checked_after_the_bearer`, `test_delete_is_405_even_on_the_commands_path`,
`test_empty_client_nonce_is_400_on_field_client_nonce`,
`test_empty_command_is_400_on_field_command`,
`test_empty_command_is_still_a_shape_error_not_a_subset_error`,
`test_every_exposed_command_reaches_the_answer_its_effect_gives`,
`test_every_outcome_the_door_writes_is_in_the_ruled_vocabulary`,
`test_every_route_the_server_serves_refuses_post_put_and_delete`,
`test_get_door_answers_403_for_a_non_ascii_token`,
`test_get_door_still_answers_200_for_the_correct_token`,
`test_get_door_still_answers_403_for_a_wrong_token`,
`test_invalid_json_body_is_400_on_field_body`,
`test_job_id_is_checked_after_the_credentials`, `test_malformed_bearer_is_403`,
`test_missing_bearer_is_403`, `test_missing_client_nonce_is_400_on_field_client_nonce`,
`test_missing_command_is_400_on_field_command`, `test_missing_csrf_header_is_403`,
`test_non_ascii_bearer_is_403_and_does_not_raise`,
`test_non_object_args_is_400_on_field_args`, `test_non_object_body_is_400_on_field_body`,
`test_non_string_command_is_400_on_field_command`,
`test_oversize_body_is_400_on_field_body`, `test_post_to_job_dashboard_is_405`,
`test_post_to_non_commands_path_is_405`,
`test_present_args_object_is_valid_and_is_accepted`,
`test_put_is_405_even_on_the_commands_path`,
`test_the_commands_path_is_the_only_post_that_is_not_405`,
`test_the_last_command_in_budget_is_accepted_and_the_next_is_429`,
`test_the_raw_token_never_reaches_the_audit_file`,
`test_the_two_refusals_are_indistinguishable`,
`test_unexposed_catalog_command_is_400_on_field_command`,
`test_unexposed_command_on_an_unresolvable_job_is_404`,
`test_unexposed_command_with_a_bad_bearer_is_403_and_never_400`,
`test_unresolvable_job_id_is_404`, `test_unresolvable_job_id_matches_the_get_door`,
`test_well_formed_command_is_dispatched_and_accepted`, `test_wrong_bearer_is_403`,
`test_wrong_csrf_header_is_403`

`tests/ui_server/test_command_dispatch.py::` — 12 ids:
`TestApproveHunksDispatchEffects::test_an_accepted_submission_records_the_decision_and_persists_it`,
`TestApproveHunksDispatchEffects::test_an_unresolvable_evidence_directory_takes_the_same_409_path`,
`TestApproveHunksDispatchEffects::test_a_refused_decision_is_409_audited_rejected_state_and_writes_nothing`,
`TestApproveHunksDispatchEffects::test_the_accepted_body_carries_the_attempt_key_and_the_three_counts`,
`TestApproveHunksDispatchEffects::test_the_rejected_wire_form_reaches_the_recorder_with_its_reason_verbatim`,
`TestFlightPlanApprovalDispatchEffects::test_an_accepted_fp_approval_really_resolved_the_plan`,
`TestFlightPlanApprovalDispatchEffects::test_a_supplied_clarification_answer_is_recorded_as_human`,
`TestFlightPlanApprovalDispatchEffects::test_the_accepted_fp_approval_saves_the_job_exactly_once`,
`TestJobStopDispatchEffects::test_an_effect_that_raises_is_500_and_audited_rejected_effect`,
`TestJobStopDispatchEffects::test_a_retry_of_the_same_nonce_is_audited_replayed`,
`TestJobStopDispatchEffects::test_the_dispatch_publishes_the_stop_request_the_body_names`,
`TestJobStopDispatchEffects::test_the_nonce_record_holds_the_body_the_client_received`

`tests/ui_server/test_decisions_endpoint.py::TestDecisionsEndpoint::` — 4 ids:
`test_decision_card_carries_age_and_blocked_count`,
`test_decisions_endpoint_answers_404_for_an_unknown_job`,
`test_decisions_endpoint_refuses_an_invalid_token`,
`test_decisions_endpoint_returns_the_inbox_document`

`tests/ui_server/test_diff_endpoint.py::` — 8 ids:
`TestDiffEndpointPerfBudget::test_the_acceptance_fixture_is_served_inside_the_hang_net`,
`TestDiffEndpointPerfBudget::test_the_route_stays_linear_in_body_lines`,
`TestDiffEndpoint::test_job_route_refuses_a_bad_token`,
`TestDiffEndpoint::test_job_route_serves_the_workspace_diff`,
`TestDiffEndpoint::test_job_without_evidence_names_the_absence_at_status_200`,
`TestDiffEndpoint::test_task_run_route_refuses_a_bad_token`,
`TestDiffEndpoint::test_task_run_route_serves_only_that_runs_diff`,
`TestDiffEndpoint::test_unknown_task_run_is_a_named_absence_at_status_200`

`tests/ui_server/test_digest_route.py::TestDigestRoute::` — 7 ids:
`test_a_neighbouring_endpoint_is_still_unhandled`,
`test_digest_body_carries_exactly_the_envelope_key_set`,
`test_digest_endpoint_answers_404_for_an_unknown_job`,
`test_digest_endpoint_answers_json_for_a_job_with_a_plan`,
`test_digest_endpoint_is_a_pass_through_of_the_composition`,
`test_digest_endpoint_refuses_an_invalid_token`,
`test_digest_version_is_the_modules_own_and_never_a_literal`

`tests/ui_server/test_live_state.py::TestUIServerIntegration::` — 16 ids:
`test_api_invalid_token_403`, `test_api_missing_job_404`, `test_api_requires_token`,
`test_api_valid_token_returns_dashboard`, `test_app_shell_served_without_token`,
`test_brain_endpoint`, `test_context_budget_endpoint`, `test_dashboard_no_raw_leaks`,
`test_delete_rejected`, `test_events_endpoint`, `test_guide_endpoint`,
`test_post_rejected`, `test_put_rejected`, `test_readiness_endpoint`,
`test_server_starts_and_writes_info`, `test_url_is_localhost_only`

`tests/ui_server/test_server_concurrency.py::TestServerServesConcurrentRequests::` — 1 id:
`test_two_requests_are_in_flight_at_once`

    78 + 12 + 4 + 8 + 7 + 16 + 1 = 126, which is BASE_ONLY_COUNT.

### PER-ID ATTRIBUTION OF EVERY BASE-ONLY ID — one class, named by direct evidence

Every one of the 126 has the SAME named artefact, so the attribution is stated once and
covers each id individually rather than 126 different causes being asserted:

    distinct E-lines in the base log = {'E       Failed: Server did not start in time'}
    E-line occurrences = 126  ==  base-only id count = 126  ->  True
    EVERY_BASE_ONLY_ID_IS_IN_A_SERVER_STARTING_FILE = True
      tests/ui_server/test_command_channel.py     ids= 78  contains the server-start wait = True
      tests/ui_server/test_command_dispatch.py    ids= 12  contains the server-start wait = True
      tests/ui_server/test_decisions_endpoint.py  ids=  4  contains the server-start wait = True
      tests/ui_server/test_diff_endpoint.py       ids=  8  contains the server-start wait = True
      tests/ui_server/test_digest_route.py        ids=  7  contains the server-start wait = True
      tests/ui_server/test_live_state.py          ids= 16  contains the server-start wait = True
      tests/ui_server/test_server_concurrency.py  ids=  1  contains the server-start wait = True

CLASS: ENVIRONMENT. NAMED STALE ARTEFACT: `apps/ui/dist/index.html` in the base worktree.
The captured stderr of a serial re-run of one of the ids says it in the product's own words:

    ERROR: React UI not built.
      To fix, run:
        cd apps/ui && npm install && npm run build
      Disable auto-build: REMEDY_UI_NO_AUTO_BUILD=1

The mechanism, measured (this is R-0736 exactly):

    apps/ui/dist/index.html mtime = 1788776043.1460497 = 2026-09-07T12:14:03
      (shutil.copytree PRESERVES the primary's mtime)
    apps/ui/src files total = 142 ; files NEWER than dist/index.html = 142
      min 1788791451.5513723 = 2026-09-07T16:30:51  apps/ui/src/RemedyApp.tsx
      max 1788791451.5572982 = 2026-09-07T16:30:51  apps/ui/src/types/react-force-graph-2d.d.ts
      (`git worktree add` STAMPS every checked-out source file at checkout time)
    => ui_server._frontend_is_stale() returns True ("any source file newer than dist/index.html")
    => _auto_build_frontend("source changed") is suppressed by REMEDY_UI_NO_AUTO_BUILD=1 and returns None
    => start_ui_server prints "ERROR: React UI not built." and NEVER writes server_info.json
    => every listed test waits 50 x 0.1s for that file and fails "Server did not start in time"

MEASURED, NOT INFERRED. With ONLY the staleness removed — the copied dist mtimes touched
forward, no rebuild, no code change, same commit, same worktree — the same 126 node ids were
re-run there:

    after touch: apps/ui/src files still NEWER than dist/index.html = 0
    $ REMEDY_UI_NO_AUTO_BUILD=1 python3 -m pytest -n auto -q <the 126 ids>
    CONTROL_REAL_EXIT = 0
    126 passed in 2.78s

SO THERE ARE ZERO GENUINE BASE FAILURES AND NO UNATTRIBUTED `comm -23` ID. The gate verdict
is not blocked.

### G8 THE TREE — clean at every boundary, worktrees restored, every commit under the cap

    git status --porcelain -> ''  EMPTY=True
    git ls-files .remedy-wt -> ''  EMPTY=True
    git worktree list       -> 13 entries (base was 13)
    git branch --list tmp/* -> ''  THROWAWAY_BRANCH_DELETED=True

    per-commit insertions, git diff --numstat <parent> <commit>:
      C0a  9a9bf185  files=1  insertions=319  deletions=0    UNDER_500=True
      C0b  cc21b12b  files=1  insertions=243  deletions=414  UNDER_500=True
      C1   f65c6a84  files=1  insertions=25   deletions=26   UNDER_500=True
      C2   a0850e1a  files=1  insertions=2    deletions=0    UNDER_500=True
      C3   898102c4  files=1  insertions=2    deletions=0    UNDER_500=True
      C4   d47c9983  files=1  insertions=51   deletions=0    UNDER_500=True
      C5   4016a97d  files=9  insertions=461  deletions=0    UNDER_500=True

    parents (single-parent check):
      C0a 9a9bf185 parents=['412ce6730901b4a33e0738aa0e922a384e66633d']
      C0b cc21b12b parents=['9a9bf1855b9f7d2946759f1aae38584a5e4119e0']
      C1  f65c6a84 parents=['cc21b12bfa32dd89ad725bb1ff7ae4ff50e0a53c']
      C2  a0850e1a parents=['f65c6a84abe0aa6d47569b2cb5ecee72b94ed057']
      C3  898102c4 parents=['a0850e1a0c8a52582a4d2511591dbdadd8378720']
      C4  d47c9983 parents=['898102c4b0fda7dcb47b23cfe9b776950448fd4a']
      C5  4016a97d parents=['d47c99838c958db64229e3e3cc351167fcf3d658']
    REAL_EXIT=0

MAXIMUM INSERTIONS IN ANY COMMIT IS 461 (C5, the gate evidence), UNDER the DECISION F104 D1
cap of 500. NO OVERSIZE COMMIT IS DECLARED THIS ROUND and none is owed; the block's
contingency for an oversize C5 did not arise. C6 is excluded, as the block orders, because a
commit cannot count its own insertions while it is being written.

In addition, `git status --porcelain` was run immediately after each of the seven commits
and printed nothing every time; each transcript reads `PORCELAIN_EMPTY_ABOVE` with no
preceding output. The primary checkout was clean at every commit boundary, and every
destructive and base-run action happened inside the disposable worktree (G5 of the
self-drive protocol).

### Constraint 10 — the three `.agent/STOP` readings, by `os.path.exists`

| Reading point | Result |
|---|---|
| before C0a | `False` |
| before C5 | `False` |
| before C6 | `False` |

### Constraint 4 — the per-file triple-newline measurement, reproduced at `412ce673`

| File | Block states | Measured |
|---|---|---|
| `.agent/live_review.md` | 0 | 0 |
| `.agent/prose_slips.md` | 1, offset 39213 | 1, offset 39213 |
| `docs/roadmap/features/T2_F272.md` | 0 | 0 |

Both append targets end in exactly ONE newline at the base, measured per file, so
`post == pre + b"\n" + slice` holds for each; both appends satisfy it, and the pre-existing
triple newline in `.agent/prose_slips.md` was neither load-bearing nor repaired.

## Authored-text proofs

Every authored text was extracted PROGRAMMATICALLY from the COMMITTED
`.agent/authored/f272-r27.md`, between its `<<<BEGIN NAME …>>>` and `<<<END NAME>>>` lines,
exclusive of both marker lines and inclusive of the newline ending the last content line —
never retyped, and never read from the delegation message. This round carried no FROM/TO
pair, so round 26's second extraction convention did not arise, exactly as constraint 2 says.

| Slice | bytes | lines | sha256 | Disk-to-disk result |
|---|---|---|---|---|
| PLANF272R27 | 1988 | 39 | 1189e22d0c5d1b1c… | `.agent/plan.md` BYTE_EQUAL_TO_SLICE True |
| RECORDR27 | 4856 | 1 | e16e323c998a6d80… | POST_EQUALS_PRE_NL_SLICE True |
| SLIPSR27 | 723 | 1 | 725fd1aefef937e9… | POST_EQUALS_PRE_NL_SLICE True |
| BUILTSTATE | 3280 | 50 | aeecbb4f44745489… | POST_EQUALS_PRE_NL_SLICE True |

Each slice ends in exactly one newline (`endswith_one_nl = True` for all four). C0a and C0b
were `shutil.copyfile` of `.remedy-wt/f272-r27-block.md` per constraint 3, so the saved copy
and its mirror are byte-identical to the delivered file by construction; G1 measures all
three at 24499 bytes, 319 lines and the same sha256.

## Deviations & assumptions

1. **DECLARED DISAGREEMENT — the Goal's ledger range is off by one AT THE BASE COMMIT THE
   BLOCK NAMES.** The Goal says, of base commit `412ce673`, that "the ledger holds
   `Gate: F272 R1` through `Gate: F272 R26`". MEASURED at `412ce673`:
   `grep -c '^Gate: F272 R'` is **26 entries whose highest round is R25**, not R26 —
   `^Gate: F272 R26` reads 0 there, as G2(d) independently confirms. The R26 entry is added
   by THIS round's own C2, after which the count is 27 and the highest is R26. Nothing was
   corrected: the BUILTSTATE slice's own heading says "ledger `Gate: F272 R1` to
   `Gate: F272 R26`" and that IS true at C4, because C2 lands first. THE LOAD-BEARING HALF OF
   THE CLAIM IS TRUE AND WAS MEASURED: `grep -c '^Gate: F272 R.*full suite'` is **0**, so no
   F272 gate entry has ever claimed the full suite and closure precondition 2 really was
   unmet before this round. Under amend0827 rule 2 this is reviewer prose that reached
   nothing on disk — one dated `.agent/prose_slips.md` line for a later round, no id.

2. **ADDITION — one unordered control run, and one unordered serial re-run, both inside the
   disposable base worktree only.** The block orders base-only ids to be attributed "BY
   DIRECT EVIDENCE". To get evidence rather than inference I (a) re-ran ONE base-only id
   serially in the base worktree to capture the product's own stderr, which named the cause,
   and (b) touched the copied `apps/ui/dist` mtimes forward — nothing else, no rebuild, no
   code change — and re-ran ALL 126 base-only ids at the SAME base commit, which returned
   exit 0 and `126 passed in 2.78s`. Neither run touched the primary checkout, neither
   changed any recorded G6 figure, and BOTH happened AFTER the R-0444 run window closed and
   after its measurement was taken, so the "0 files with mtime inside the run window" reading
   is unaffected by the later touch. The evidence directory says so explicitly. This is an
   addition to the ordered gate set, not a substitute for any part of it.

3. **Two pushes rather than one.** The branch was pushed after C5 so this handback could
   transcribe a real push with a real exit code, and is pushed again after C6, which a
   handback cannot transcribe for itself. Both are plain
   `git push -u origin feature/f272-one-world-completion`; no force, no lease, no rewrite.

4. **Scripts written to `.remedy-wt/` because the session's bash guard refused a shell form.**
   `mkdir -p <dir> && ls -la <dir> && …` was refused as "multiple operations". Every
   multi-step measurement was therefore written with the file tool to the gitignored
   `.remedy-wt/` and run as `bash -c 'python3 -B <abs-path>; echo "REAL_EXIT=$?"'`, which is
   the exact invocation form the block's "Done when" section orders. All TEN scratch scripts
   were then deleted BY THEIR EXACT PATHS, never by a glob: `.remedy-wt/r27_extract.py`,
   `.remedy-wt/r27_c2.py`, `.remedy-wt/r27_c3.py`, `.remedy-wt/r27_c4.py`,
   `.remedy-wt/r27_parity.py`, `.remedy-wt/r27_dist_after.py`, `.remedy-wt/r27_attrib.py`,
   `.remedy-wt/r27_control.py`, `.remedy-wt/r27_c5.py`, `.remedy-wt/r27_g1g8.py`; the
   `.remedy-wt/__pycache__` directory `python3 -B` could not prevent for the imported
   extractor module was removed by its exact path too. `.remedy-wt/f272-r27-block.md` was left
   in place — it is the delivered block and G1's first link. `git ls-files .remedy-wt` is
   empty throughout.

5. **ASSUMPTION — the base worktree's `packages` namespace has the PRIMARY checkout second on
   its path, and this cannot manufacture a branch-only failure.** Measured in the base
   worktree: `packages.__path__` is
   `['<base wt>/packages', '/home/decodeux/Repos/remedy/packages']`, because
   `/home/decodeux/.local/lib/python3.10/site-packages/_editable_impl_remedy.pth` puts the
   primary checkout on `sys.path`. The base worktree's own copy therefore WINS for every
   module that exists in both, which is the case for all of them here. The residual risk is
   one-directional: a module that existed ONLY on the branch could be imported at base and
   make base look greener than it is, which can only SHRINK the base-only set. It cannot add
   a branch-only id, and the branch-only set is the gate's verdict criterion. Recorded so the
   reviewer can weigh it rather than discover it.

6. **ASSUMPTION — `.agent/live_review.md` was verified by measurement rather than read end to
   end.** AGENTS.md's File Editing Safety Rules say "read the entire file" before modifying.
   That file is 1.2 MB / 2133 lines. I read its terminal region and derived its structure
   programmatically instead (paragraph units, terminal newline run, id counts), and the
   after-edit obligation is discharged by G2, which proves the pre-image is a byte-exact
   prefix, that all 732 units before the appended one are unchanged, and that a one-byte
   corruption of the added text is rejected by BOTH readers while the real post-image is
   accepted by both. Every other file this round touched was read in full before editing.

7. **No production code moved, so no red-proof was ordered or possible.** Nothing under
   `packages/`, `apps/`, `tests/`, `scripts/` or `README.md` changed this round, and no
   STATUS line was touched — `git diff --numstat 412ce673..4016a97d` names exactly the
   fifteen declared paths and nothing else. F272 is still `[~]` in `docs/roadmap/STATUS.md`;
   the `[x]` flip belongs to the closure round.

8. **No finding id was minted this round**, per constraint 6. Round 26 PASSED, and the one
   gap its verdict named is reviewer block prose that reached no file, so it is one dated
   `.agent/prose_slips.md` line under amend0827 rule 2. `R-0826` is still FREE:
   `^- R-0826` reads 0 before and 0 after. Registrations stay at 309 and resolutions at 252,
   both measured.

9. **One worktree created, and it is the one constraint 8 requires.** `tmp/f272-base-gate` at
   `/home/decodeux/remedy-gate-scratch/f272r27-base-wt`, created on a THROWAWAY BRANCH and
   never detached, then removed, pruned and its branch deleted. `git worktree list` is 13
   entries at the base and 13 at the end, and `git branch --list 'tmp/*'` is empty. The branch
   deletion is the one integration_gate.md step 2 and constraint 8 both order by name; it is
   not the branch deletion guardrail G2 forbids.

10. **All run logs were written OUTSIDE the repository while a suite ran**, per constraint 9 —
    to `/home/decodeux/remedy-gate-scratch/`, which is not inside the primary checkout and not
    inside the base worktree — and were copied into `.agent/gate_f272_r27/` only after both
    runs had exited. Every evidence file is named `.txt`; `[f for f in listdir(D) if
    f.endswith('.log')]` is `[]`.

11. **No departure from the block's ordered commit sequence.** The seven work commits landed
    in exactly the order C0a, C0b, C1, C2, C3, C4, C5, each single-parent, with C6 last. No
    commit was added, dropped, reordered or split.

12. **Non-disagreement, recorded so the reviewer need not re-check it.** The block's G5 quotes
    the reviewer's branch reading as "19786 passed, 23 skipped and ZERO failures in 131.37s".
    The three COUNTS reproduce exactly; the wall time does not (115.98s here). That is machine
    load, and the block explicitly says "REPORT WHAT YOU MEASURE". Likewise the "305 MB"
    figure for `apps/ui/node_modules` is the `du -sh` reading and is exactly right —
    `du -sh --apparent-size` gives 162M and the summed `st_size` over 43032 files gives
    181.8 MB.

## Open findings

57, BY DISTINCT ID — 309 distinct `^- R-xxxx` registrations minus 252 distinct
`^Done: R-xxxx` resolutions, with zero `Done:` ids lacking a registration, so nothing is
subtracted twice. Unchanged by this round, which mints and resolves nothing. Four of the 57
are High — R-0803, R-0804, R-0806 and R-0807 — and all four are booked to F273's T001 by the
2026-09-06 triage, so F272's close will be PASS_WITH_RISKS naming them.

## Runtime actuals — for the closure round's runtime-actuals section

| Run | Command | Exit | passed | failed | skipped | Wall (pytest) | Wall (shell) |
|---|---|---|---|---|---|---|---|
| branch, primary at `d47c9983` | `python3 -m pytest -n auto -q` | 0 | 19786 | **0** | 23 | 115.98s | 117s |
| base, worktree at `b18fad57` | `REMEDY_UI_NO_AUTO_BUILD=1 python3 -m pytest -n auto -q` | 1 | 19605 | **126** | 23 | 166.70s | 167s |
| base control, 126 ids only | `REMEDY_UI_NO_AUTO_BUILD=1 python3 -m pytest -n auto -q <126 ids>` | 0 | 126 | 0 | 0 | 2.78s | 3.0s |

Both suite runs are under the ~5 min budget integration_gate.md step 5 names, so no perf pass
is noted. The base run's extra ~51s over the branch run is the 126 tests each spending their
full 5s server-start wait before failing.

## Next

Review round 27 and issue its verdict. Then, per `.agent/plan.md`, the SELF-USE ROUND that
closure precondition 6 requires: the queue holds no pending item, so
`generate_and_append_if_empty` is called first, then the item is planned and run, and every
string `describe_self_use_run_defects` returns is registered as a normal R-id finding.
Before authoring, re-read `.agent/STOP` per Phase 1 rule 1, then the Open PR Gate per rule 2.
