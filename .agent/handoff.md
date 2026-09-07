# Handback — F272 round 28

## Session

SESSION 12 of feature F272 · round 28 · rounds so far 28

SOFT LIMIT, under operator amendment amend0906-triage-throughput rule 2, which sets F272's
limit at 12 SESSIONS and 40 ROUNDS by name: the SESSION half REMAINS REACHED — this is
still session 12 of 12. The round half is not: this is round 28 of 40. The SPLIT half of
the amend0905-throughput split-and-close default was executed in round 26 (F274 registered,
DECISION F272 D16); this round is the third step of the CLOSE half, discharging closure
precondition 6.

CONTEXT SELF-ASSESSMENT (amend0905-throughput, one sentence): context is comfortable — the
round read four small production modules end to end (`self_use_runner.py`,
`self_use_findings.py`, `self_use_generator.py`, `self_use_queue.py`, 845 lines together),
handled the two large state files by measurement rather than by reading them, and spent its
wall clock rather than its context on the 251.76-second real-provider run.

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE

The scope report the limit obliges was written in full in round 26's handback and is on
disk and durable as the `## Built State` section of `docs/roadmap/features/T2_F272.md`,
which states what F272 built, which slices moved to F274, and what remains open. It is not
re-derived here. What is finished as of this round: T001, T002 and T003 complete; closure
preconditions 2 (round 27's integration gate), 4 (Built State) and 6 (this round) all
discharged. What is missing: preconditions 1, 3 and 5 — the verdict booking for this round,
`remedy integrity check --json`, and the evidence job, review zip, ledger rotation and
closure commit. The proposal is unchanged from round 26 and already executed: close F272 at
DECISION F272 D16's scope, with F274 carrying T004's remainder and T005.

## Range

Review of `b865f001`..`fd19b113`.

The range ends at C5, the last commit that EXISTS while this file is being written. C6 is
the commit that writes this file and cannot state its own SHA; the reviewer's range is
`b865f001`..HEAD once C6 lands.

## Commits

### e8bd5dd2 f272: save the round 28 step block as authored text  (C0a)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f272-r28.md | +281 / -0 | `shutil.copyfile` of `.remedy-wt/f272-r28-block.md` per constraint 3 |

### a33eed0a f272: mirror the round 28 block into last_block  (C0b)
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +188 / -226 | the same `shutil.copyfile`, the mirror |

### 6d226f61 f272: point the plan at round 28 and the self-use precondition  (C1)
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +16 / -15 | replaced byte for byte with the PLANF272R28 slice |

### 4ab2f054 f272: book the round 27 PASS verdict into the record  (C2)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 / -0 | append of RECORDR28, the `Gate: F272 R27` PASS entry |

### 98a2bf5c f272: record the round 27 block prose slip on the ledger entry span  (C3)
| Path | +/- | Reason |
|---|---|---|
| .agent/prose_slips.md | +2 / -0 | append of SLIPSR28, one dated line, no id spent |

### 4d5edd71 f272: let the shipped generator append self-use item SU-012  (C4)
| Path | +/- | Reason |
|---|---|---|
| scripts/self_use_queue.json | +8 / -0 | written by `generate_and_append_if_empty()` and by no hand; pure append, zero deletions, so the generator reformatted nothing |

### fd19b113 f272: record the SU-012 self-use run evidence  (C5)
| Path | +/- | Reason |
|---|---|---|
| .agent/selfuse_f272_r28/g5a_entry_and_job_file.txt | +8 / -0 | G5(a) |
| .agent/selfuse_f272_r28/g5b_result_state.txt | +5 / -0 | G5(b) |
| .agent/selfuse_f272_r28/g5c_execution_config.txt | +2 / -0 | G5(c) |
| .agent/selfuse_f272_r28/g5d_timing.txt | +2 / -0 | G5(d) |
| .agent/selfuse_f272_r28/g5e_run_defects.txt | +3 / -0 | G5(e) |
| .agent/selfuse_f272_r28/g5f_jobplan.txt | +3 / -0 | ADDITION — the full `JobPlan` repr, which carries the stop reason and the run-manifest error; see deviation 3 |
| .agent/selfuse_f272_r28/g5g_stop_and_manifest.txt | +29 / -0 | ADDITION — the same facts re-read through the shipped `load_job_plan`; see deviation 3 |
| .agent/selfuse_f272_r28/g5_full_transcript.txt | +28 / -0 | ADDITION — the run script's own transcript |
| .agent/selfuse_f272_r28/job/SU-012.md | +7 / -0 | the job file `plan_next_self_use_item` rendered, 2494 bytes, sha256 `950747cd1b75dc45c1f177c881471ab672a57f56a6bb8b13f20213e115c2ef66` |

### C6 f272: hand back round 28
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | (self-referential) | this file; a handoff cannot table the commit that writes it (R-0149 pattern) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a  | done | `.agent/authored/f272-r28.md`, copyfile, digest-identical |
| C0b  | done | `.agent/last_block.md`, copyfile, digest-identical |
| C1   | done | `.agent/plan.md` byte-equal to PLANF272R28 |
| C2   | done | RECORDR28 appended, `POST_EQUALS_PRE_NL_SLICE` true |
| C3   | done | SLIPSR28 appended, `POST_EQUALS_PRE_NL_SLICE` true |
| C4   | done | SU-012 appended BY THE SHIPPED FUNCTION, `consumed_by` empty |
| C5   | done | evidence directory, 9 files, no `.log` member |
| C6   | done | this handback |

## External actions

| Action | Command | Outcome |
|---|---|---|
| push (after C5) | `git push -u origin feature/f272-one-world-completion` | `b865f001..fd19b113`, exit 0, upstream set |
| push (after C6) | `git push` | see the reviewer's own `git log origin/...`; a second push is expected per the round's transport note |
| worktree add | NONE BY ME. The PRODUCT created `/home/decodeux/Repos/remedy/.remedy-wt/job-020c1ef366af4f07` on branch `remedy/job-020c1ef366af4f07` | RETAINED per constraint 8; `worktree_cleanup_status='retained'` |
| worktree remove | none | constraint 8 forbids removing it or any of the twelve pre-existing ones |
| PR create / merge | none | the block orders none, and the closure PR is a later round |

## Verification

Every gate was run as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, with no pipe between the
command and the echo.

**G1 TRANSPORT — PASS.** One digest comparison over three artefacts; all three identical and
all three equal to the reviewer's stamp.

    .remedy-wt/f272-r28-block.md (as delivered, on disk) bytes=22575 lines=281 sha256=79c944de68ea99589234068b62c33aa4591f32efaa1f2364bd7c3e343258685c
    .agent/authored/f272-r28.md (committed, HEAD)        bytes=22575 lines=281 sha256=79c944de68ea99589234068b62c33aa4591f32efaa1f2364bd7c3e343258685c
    .agent/last_block.md (committed, HEAD)               bytes=22575 lines=281 sha256=79c944de68ea99589234068b62c33aa4591f32efaa1f2364bd7c3e343258685c
    ALL_THREE_IDENTICAL: True
    ALL_THREE_MATCH_REVIEWER_STAMP(22575/281/79c944de...): True
    REAL_EXIT=0

The three measurements were also taken BEFORE the block was opened, against the reviewer's
stated 22575 / 281 / `79c944de68ea99589234068b62c33aa4591f32efaa1f2364bd7c3e343258685c`, and
all three agreed.

**G2 THE FINDING RECORD — PASS.** Every count landed on the block's stated figure; none was
adjusted to agree.

    === G2(a) BYTE ===
    pre_len=1220698 pre_sha256=0f2924505f470394ace8f1e55a372a03713c722943ef227edfe74b25a8ea8bc6 pre_term12=b'for either.\n' pre_trailing_nl_run=1
    post_len=1225920 post_sha256=495c5cea046dfe0a7211dc89d18123b4ac64e903b6f152b19bb8790b3f0dfde0 post_term12=b'tion round.\n' post_trailing_nl_run=1
    slice_len=5221 slice_sha256=c165f21cac14eddf6612de01165d6852b31e1989815bebadb8fde08c99b35a94
    PRE_IS_BYTE_EXACT_PREFIX_OF_POST: True
    POST_EQUALS_PRE_NL_SLICE: True
    === G2(b) STRUCTURAL ===
    N (counted from slice) = 1
    units_before=733 units_after=734
    LAST_N_UNITS_EQUAL_SLICE_PARAGRAPHS_IN_ORDER: True
    EVERYTHING_BEFORE_UNCHANGED: True
    === G2(c) NEGATIVE CONTROL (in memory only) ===
    first_appended_paragraph_offset=1220699 flipped_byte_index=1220709
    mutated_differs_from_post: True
    BYTE_READER_REJECTS_MUTANT: True
    STRUCTURAL_READER_REJECTS_MUTANT: True
    DISK_UNCHANGED_BYTE_IDENTICAL_TO_REAL_POST: True sha256=495c5cea046dfe0a7211dc89d18123b4ac64e903b6f152b19bb8790b3f0dfde0
    BOTH_READERS_ACCEPT_REAL_POST: True
    === G2(d) COUNTS ===
      ^- R-dddd distinct             309 ->   309
      ^Done: R-dddd distinct         252 ->   252
      open set BY DISTINCT ID         57 ->    57
      ^Gate:                          50 ->    51
      ^Gate: F272 R27                  0 ->     1
      ^- R-0826                        0 ->     0
      OPEN FINDINGS BY DISTINCT ID arithmetic: pre 309 registered - 252 resolved-among-registered = 57 ; post 309 - 252 = 57
      triple_newline_occurrences pre=0 post=0
    REAL_EXIT=0

The pre-image was 1220698 bytes at 2135 lines with sha256 beginning `0f2924505f470394`,
exactly as the block stated. `^- R-0826 ` is 0 at the base AND 0 at the end, so constraint 9
holds: no finding id was minted this round.

**G3 THE TWO PROSE FILES — PASS.**

`.agent/plan.md`:

    C1 plan.md bytes=2075 lines=40 sha256=f0cc0d5dedca4b0147ddeda92f897b6ddfac5a5960b72d03ea20dba1cd23ab93
    C1 BYTE_EQUAL_TO_SLICE: True
    REAL_EXIT=0

40 lines against the AGENTS.md cap of 50. `## Goal` present (line 8) and `## Next Steps`
present (line 22), both confirmed by re-reading the file after the write.

`.agent/prose_slips.md`:

    pre_len=151498 pre_lines=565 pre_sha256=1428aac1c72606436168be2f998609bda6c07643c841be8ffec12fecc99dd981 pre_term12=b's not have.\n' pre_trailing_nl_run=1
    post_len=152214 post_lines=567 post_sha256=e52d1332646895a89914fc9077aedfe710555332dee718f040f653904376b690 post_term12=b' exist yet.\n' post_trailing_nl_run=1
    slice_len=715 slice_sha256=539cda532989c157108d2992d81f9cc012e513c6ec1192e1a6deb8db13ef40b8
    PRE_IS_BYTE_EXACT_PREFIX_OF_POST: True
    POST_EQUALS_PRE_NL_SLICE: True
    triple_newline pre=1 post=1
    REAL_EXIT=0

pre_len 151498 and pre_lines 565 are the block's own figures. The single pre-existing
triple-newline at offset 39213 is still 1 after the append: not load-bearing, not repaired.

**G4 THE QUEUE — PASS, and the reviewer's probe is confirmed exactly.** Every reading below
comes from the SHIPPED readers (`load_self_use_queue`, `pending_self_use_items`,
`next_self_use_item`) except `schema_version`, for which no shipped reader is exported.

    STOP_READING_2_before_C4: False
    PRE  queue bytes=33722 lines=94 sha256=78f87b368bb2b721154cf0567ff27f6edde96d427ed5de5c96c7b9767feee2c0
    PRE  load_self_use_queue() item count: 11
    PRE  pending_self_use_items() length: 0
    PRE  next_self_use_item(): None
    PRE  body['schema_version']: 2
    PRE  every item has non-empty consumed_by: True
    --- generate_and_append_if_empty() returned ---
    returned is None: False
    entry.id: SU-012
    entry.title: Address ledger finding R-0445
    entry.provenance: generated (self-use-generator tier 1, ledger scan, R-0445)
    entry.consumed_by: ''
    entry.consumed_by IS EMPTY STRING: True
    entry.job_markdown length (chars): 2486
    entry.why length (chars): 2255
    POST queue bytes=38741 lines=102 sha256=d04d856c0f4b3eef20a1d21f20e53ba4bc6590c9ce121179942d9ddcb2f84ec4
    POST load_self_use_queue() item count: 12
    POST pending_self_use_items() length: 1
    POST next_self_use_item().id: SU-012
    POST next_self_use_item() ANSWERS THE APPENDED ID: True
    POST body['schema_version']: 2
    POST ids: ['SU-001', 'SU-002', 'SU-003', 'SU-004', 'SU-005', 'SU-006', 'SU-007', 'SU-008', 'SU-009', 'SU-010', 'SU-011', 'SU-012']
    POST appended item consumed_by from shipped loader: ''
    REAL_EXIT=0

Against the block's ordered readings: item count 11 -> 12; appended id `SU-012`; title
`Address ledger finding R-0445`; provenance
`generated (self-use-generator tier 1, ledger scan, R-0445)`; `consumed_by` the EMPTY
STRING; `next_self_use_item()` answers `SU-012`; `pending_self_use_items()` 0 -> 1;
`schema_version` 2 before and 2 after. The id is the one the reviewer's probe named, so
there is NO deviation to declare here. The 2486-character `job_markdown` also matches the
probe's figure exactly.

The queue diff is +8 / -0 — a pure append. The generator rewrites the whole file through
`json.dumps(..., indent=2)`, so a zero-deletion diff is the proof it reformatted nothing.

**G5 THE RUN — PASS as a gate; see the reading itself, which is the round's whole point.**
Command was the block's, verbatim, with no `builder_name` and no `reviewer_name`:

    from packages.orchestration.self_use_runner import run_next_self_use_item
    entry, job_file_path, result = run_next_self_use_item(dest_dir, repo_path=".")

`dest_dir` was `/home/decodeux/Repos/remedy/.agent/selfuse_f272_r28/job` — see assumption 1.

    REAL_EXIT=0

Provider resolution was probed read-only at C4's HEAD before the call, and it matched the
reviewer's measurement exactly:

    resolve_role_config('builder'): provider='ollama' model='muse-glimmer:latest'
    resolve_role_config('reviewer'): provider='ollama' model='muse-glimmer:latest'
    ollama /api/tags: 8 models
       names: ['muse-glimmer:latest', 'qwen2.5-coder:32b', 'qwen3.5:9b', 'qwen3-coder-next:latest', 'mistral:7b-instruct', 'qwen2.5:32b-instruct-q4_K_M', 'nomic-embed-text:latest', 'Openhermes:latest']
       muse-glimmer:latest present: True
    REAL_EXIT=0

*(a) entry and job file*

    entry.id: SU-012
    entry.title: Address ledger finding R-0445
    entry.provenance: generated (self-use-generator tier 1, ledger scan, R-0445)
    entry.consumed_by: ''
    job_file_path: /home/decodeux/Repos/remedy/.agent/selfuse_f272_r28/job/SU-012.md
    job_file bytes: 2494
    job_file lines: 7
    job_file sha256: 950747cd1b75dc45c1f177c881471ab672a57f56a6bb8b13f20213e115c2ef66

*(b) result state*

    result.state (literal): <RunState.RUNNING: 'running'>
    result.job_id: '020c1ef366af4f07'
    result.error: ''
    number of tasks: 1
      task_id='T001' status='pending' error=''

READ THAT LITERAL VALUE CAREFULLY. `result.state` is `RunState.RUNNING`, which is NEITHER
`JOB_COMPLETED` NOR `JOB_BLOCKED` — the two outcomes the block's constraint 7 names as the
legitimate ones. `finished_at` is the empty string. The job did not reach the approval gate;
it was STOPPED by its own budget. Re-read through the shipped `load_job_plan`, the persisted
record says:

    state:                 <RunState.RUNNING: 'running'>
    finished_at:           ''
    error:                 ''
    stop_reason:           'budget_exhausted:max_provider_calls'
    stop_source:           'budget'
    stop_request_id:       'budget_a0b7276e530e4e0c'
    stopped_at:            '2026-09-07T15:03:52.142876+00:00'
    stop_error:            ''
    budgets:               {'max_total_tokens': None, 'max_provider_calls': 6, 'max_wall_clock_minutes': None, 'max_cost_usd': 0.5, 'deadline': None}
    budget_actuals:        {'schema_version': '1.0.0', 'provider_call_count': 6, 'actual_call_count': 0, 'total_tokens': 0, 'started_at': '2026-09-07T14:59:40.633887+00:00', 'actual_sources': [], 'unmeasured_call_count': 6}
    repair_rounds_allowed: 2
    isolation_mode:        'worktree'
    worktree_branch:       'remedy/job-020c1ef366af4f07'
    worktree_path:         '.remedy-wt/job-020c1ef366af4f07'
    worktree_cleanup_status: 'retained'
    result_diff_size_bytes:  0
    root_changed_files:      []
    task T001: status='pending' final_status='stopped' error='' repair_rounds_used=2 task_attempt_state='active' reviewer_verdict='' test_passed=None
    REAL_EXIT=0

The 6 of `max_provider_calls: 6` is `run_next_self_use_item`'s OWN default, not a value this
round chose: the block ordered the call with no budget arguments, and the signature defaults
to `max_provider_calls=6, max_cost_usd=0.50, max_tasks=1`. The run made exactly 6 provider
calls, used both of its 2 allowed repair rounds, and was then cut off with T001 still
`pending`.

The persisted record ALSO carries a non-empty `run_manifest_error`, which is a real failure
the run recorded about itself:

    run_manifest_path:     ''
    run_manifest_error:
    run_manifest_write_failed: ManifestError: invalid run manifest (write (bound)): a published stopped reference manifest must have complete call coverage; incomplete coverage is manifest corruption (task T001: call lineage is invalid: call calls/builder/round-01/attempt prepared_input.mode 'ollama-legacy' is not a supported transport mode; task T001: call lineage is invalid: stored sequence 2 != )

*(c) execution config — WHICH PROVIDER ACTUALLY RAN*

    ExecutionConfig(builder='ollama', builder_source='cli', reviewer='ollama', reviewer_source='cli', builder_model='', builder_model_source='default', builder_effort='', builder_effort_source='default', reviewer_model='', reviewer_model_source='default', reviewer_effort='', reviewer_effort_source='default', repair_provider='', repair_provider_source='default', repair_model='', repair_model_source='default', repair_effort='', repair_effort_source='default', max_rounds=3, max_rounds_source='default', repair_rounds_allowed=2, repair_rounds_source='default', test_command='', test_command_source='default', claude_cli_write_mode='none', claude_cli_write_mode_source='default', context_strategy='task_bounded_sequential_job', timeout_sec=120, timeout_sec_source='default', timeout_profile='', timeout_profile_source='default', max_output_chars=50000, max_output_chars_source='default', stream_evidence=False, stream_evidence_source='default', max_tasks=1, max_tasks_source='invocation')
    FAKE_APPEARS_IN_EXECUTION_CONFIG: False

THE PROVIDER THAT ACTUALLY RAN WAS `ollama`, for BOTH roles. The word `fake` appears nowhere
in the execution config, so constraint 6's STOP condition did not fire. Independent
corroboration from the run's own input snapshot, which records the daemon it talked to:

    'provider_versions': {'ollama': 'ollama version is 0.32.9'}
    'models': {'builder': 'ollama', 'reviewer': 'ollama'}
    'ollama.model' -> 'muse-glimmer:latest' (source: default)
    'ollama.host'  -> 'http://localhost:11434' (source: default)

*(d) wall clock and provider calls*

    wall_clock_seconds: 251.76
    result.budgets = {'max_total_tokens': None, 'max_provider_calls': 6, 'max_wall_clock_minutes': None, 'max_cost_usd': 0.5, 'deadline': None}
    budget_actuals.provider_call_count = 6
    budget_actuals.actual_call_count   = 0
    budget_actuals.total_tokens        = 0
    budget_actuals.unmeasured_call_count = 6

The result DOES carry a provider-call count: 6, all six of them `unmeasured` for tokens
(`actual_call_count: 0`, `total_tokens: 0`, `actual_sources: []`).

*(e) `describe_self_use_run_defects(result)` — THE OUTPUT THIS ROUND EXISTS FOR*

    TUPLE LENGTH: 0
    THE TUPLE IS EMPTY: ()

**THE TUPLE IS EMPTY. Its length is 0 and its value is `()`.** There is no defect string to
quote, because there is none to quote — not because one was dropped, truncated or
summarised. The same call against the plan RE-READ from disk through the shipped
`load_job_plan` answers identically:

    describe_self_use_run_defects(reloaded_plan) length: 0
    value: ()

WHY IT IS EMPTY, stated so the next round can rule on it rather than infer it.
`describe_self_use_run_defects` reads exactly two things (`self_use_findings.py` lines
49-55): `result.error`, and each `task.error`. Both are the empty string on this run —
`result.error == ''` and `T001.error == ''`. Everything the run actually surfaced about
itself lives in fields that function does not read: `stop_reason`
(`budget_exhausted:max_provider_calls`), `state` (`RunState.RUNNING` rather than
`JOB_COMPLETED`/`JOB_BLOCKED`), `T001.final_status` (`stopped`) and `run_manifest_error`
(the `ManifestError` quoted under (b)). So the honest reading of `()` here is "the two error
fields are blank", NOT "the run went well" — and closure precondition 6's own words, "an
empty tuple means nothing to register, not that nothing was checked", are being satisfied by
a run that was cut off before it could finish. That judgement is the reviewer's to make, and
this handback deliberately makes none: it mints no id and writes no `- R-XXXX` line, per the
block's Goal and constraint 9.

**G6 THE SUITES — PASS, both, run serially in the primary checkout at C5.**

    $ python3 -B -m pytest tests/orchestration/test_self_use_queue.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_job.py tests/orchestration/test_self_use_runner.py -q -p no:randomly
    ........................................................................ [100%]
    72 passed in 4.45s
    REAL_EXIT=0

    $ python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
    .......................................... [100%]
    42 passed in 20.80s
    REAL_EXIT=0

72 passed at exit 0 reproduces the reviewer's disposable-worktree measurement cell for cell,
and the canary's 42 reproduces the `b865f001` figure. No red-proof was ordered or possible:
no production line moved this round.

**G7 THE TREE — PASS.**

    git status --porcelain output: ''  (EMPTY=True)
    git ls-files .remedy-wt output: ''  (EMPTY=True)
    git worktree list entries AFTER the run: 14
      /home/decodeux/Repos/remedy/.remedy-wt/job-020c1ef366af4f07  4d5edd71 [remedy/job-020c1ef366af4f07]
    REAL_EXIT=0

`git status --porcelain` was read at EVERY commit boundary and was EMPTY every time — after
C0a, C0b, C1, C2, C3, C4 and C5. The one non-empty reading in the whole round was between
C4 and C5, `?? .agent/selfuse_f272_r28/`, which is the C5 change-set entry itself sitting
untracked before its own commit; it is not a commit boundary and not the run's doing. The
run wrote nothing into the tracked tree: `root_changed_files: []` and
`result_diff_size_bytes: 0`.

Worktrees: 13 before the run, 14 after. The 13 before were the primary plus twelve
pre-existing `remedy/job-*`, exactly as the block stated. The one new entry is the PRODUCT's
own, `/home/decodeux/Repos/remedy/.remedy-wt/job-020c1ef366af4f07` on branch
`remedy/job-020c1ef366af4f07`, and it is NOT removed, per constraint 8; the plan itself
records `worktree_cleanup_status='retained'`. I created no worktree of my own.

Per-commit insertions, `git diff --numstat <parent> <commit>`, C0a through C5 (C6 excluded):

    C0a  e8bd5dd2  insertions=281  deletions=0     under_500=True
    C0b  a33eed0a  insertions=188  deletions=226   under_500=True
    C1   6d226f61  insertions=16   deletions=15    under_500=True
    C2   4ab2f054  insertions=2    deletions=0     under_500=True
    C3   98a2bf5c  insertions=2    deletions=0     under_500=True
    C4   4d5edd71  insertions=8    deletions=0     under_500=True
    C5   fd19b113  insertions=87   deletions=0     under_500=True
    REAL_EXIT=0

Every one is under the DECISION F104 D1 cap of 500 insertions. These figures are the ones in
the per-commit tables above, compared cell for cell.

The three `.agent/STOP` readings, all by `os.path.exists`:

    STOP_READING_1_before_C0a: False
    STOP_READING_2_before_C4:  False
    STOP_READING_3_before_C6:  False

## Authored-text proofs

All three slices were extracted PROGRAMMATICALLY from the COMMITTED
`.agent/authored/f272-r28.md`, between `<<<BEGIN NAME ...>>>` and `<<<END NAME>>>`, exclusive
of both marker lines and inclusive of the newline ending the last content line. Nothing was
retyped and nothing was taken from the delegating message. The extractor asserts exactly one
BEGIN and exactly one END marker per name.

| Slice | Bytes | sha256 | Proof |
|---|---|---|---|
| PLANF272R28 | 2075 | `f0cc0d5dedca4b0147ddeda92f897b6ddfac5a5960b72d03ea20dba1cd23ab93` | `.agent/plan.md` is byte-equal to the slice: `BYTE_EQUAL_TO_SLICE: True` |
| RECORDR28 | 5221 | `c165f21cac14eddf6612de01165d6852b31e1989815bebadb8fde08c99b35a94` | `POST_EQUALS_PRE_NL_SLICE: True` on `.agent/live_review.md`, plus the structural and negative-control readers |
| SLIPSR28 | 715 | `539cda532989c157108d2992d81f9cc012e513c6ec1192e1a6deb8db13ef40b8` | `POST_EQUALS_PRE_NL_SLICE: True` on `.agent/prose_slips.md` |

This round carried no FROM/TO pair, as constraint 2 states.

## Deviations & assumptions

The block's ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5, C6 was followed exactly:
no extra commit, no dropped commit, no reordering.

**1. ASSUMPTION — where `dest_dir` points.** G5 says "`dest_dir` inside
`.agent/selfuse_f272_r28/`" and then "Write (a) through (e) into `.agent/selfuse_f272_r28/`
as `.txt` files at C5, together with the job file itself." I read "inside" strictly and used
`/home/decodeux/Repos/remedy/.agent/selfuse_f272_r28/job` as `dest_dir`, so the job file
landed at `.agent/selfuse_f272_r28/job/SU-012.md` — a subdirectory of the evidence directory
rather than its root. Both clauses are satisfied: `dest_dir` is inside the evidence
directory, and the job file is committed with the evidence. If the reviewer meant
`dest_dir` to BE `.agent/selfuse_f272_r28/`, the only difference is one path segment.

**2. DECLARED DISAGREEMENT WITH CONSTRAINT 7, applied as written and not silently
corrected.** Constraint 7 says "`JOB_COMPLETED` and `JOB_BLOCKED` are both legitimate
outcomes and neither is a failure of this round." The run produced NEITHER: `result.state` is
`RunState.RUNNING` with `finished_at=''`, because the run was cut short by
`stop_reason='budget_exhausted:max_provider_calls'` after exactly the 6 calls
`run_next_self_use_item`'s own default budget allows. I did not stop the round over this,
because constraint 7 does not make a third state a stop and G5 orders me to report
`result.state` — the literal value — rather than to require a particular one; the only STOP
conditions the block states are a `fake` provider, a red gate and a dirty tree, and none
fired. But the block's premise that the run "GOES TO THE APPROVAL GATE" is not what
happened, and a reviewer who reads constraint 7 as an exhaustive list of outcomes would
mis-read this round. Naming it here rather than correcting it.

**3. ADDITION — three evidence files beyond the ordered (a) through (e).**
`g5f_jobplan.txt` (the full `JobPlan` repr), `g5g_stop_and_manifest.txt` (the same fields
re-read through the shipped `load_job_plan`) and `g5_full_transcript.txt` (the run script's
own output). All three sit inside
`.agent/selfuse_f272_r28/`, which the change set declares, and all three are `.txt`. They
exist because the material the next round most needs — the stop reason and the
`run_manifest_error` — is NOT in (a) through (e), since (b) and (e) read only the fields
`describe_self_use_run_defects` reads, and a fact that reaches no committed file does not
reach the round that must rule on it.

**4. OBSERVATION, not a deviation — `remedy_dirty: True` inside the run's input snapshot.**
The run's own `input_snapshot` records `'remedy_dirty': True` at 14:59:41. That is my
untracked `.agent/selfuse_f272_r28/` directory, created moments earlier as C5's change-set
entry; the tracked tree was clean and the run changed nothing in it
(`root_changed_files: []`, `result_diff_size_bytes: 0`). Recording it so nobody later reads
that flag as the product having dirtied the checkout.

**5. TOOLING — scratch scripts under `.remedy-wt/`.** This session's bash guard rejects
heredocs, loops and `$( )` by shape, so every multi-step measurement was written to a file
under the gitignored `.remedy-wt/` and run with `python3 -B`. The TWELVE files were
`.remedy-wt/r28_pre.py`, `r28_c0a.py`, `r28_c0b.py`, `r28_slice.py`, `r28_c1.py`, `r28_c2.py`,
`r28_c3.py`, `r28_c4.py`, `r28_probe.py`, `r28_g5.py`, `r28_g5g.py` and `r28_g1g7.py`, and
each was deleted BY ITS EXACT PATH after the round's gates were taken — never by a glob.
`.remedy-wt/f272-r28-block.md` was NOT deleted: it is G1's first link. `git ls-files
.remedy-wt` is empty, so none of this ever touched the review subject.

**6. NOT DONE, deliberately, per the Goal and constraint 9.** No R-id was minted, no
`- R-XXXX` line and no `Done:` paragraph was written. `^- R-0826 ` reads 0 in the committed
ledger at HEAD, so `R-0826` is still the next free id. No `consumed_by` was set on SU-012;
that edit belongs to the closure commit in a later round, per constraint 5.

## Next

The reviewer reviews `b865f001`..HEAD and rules on closure precondition 6. The substantive
question this round hands over is not "which strings do I register" — the tuple is `()` —
but whether a self-use run that was cut off at `budget_exhausted:max_provider_calls` with
`RunState.RUNNING`, a `pending` task and a `run_manifest_write_failed` error CONSUMES the
item, and whether `describe_self_use_run_defects`'s blindness to `stop_reason`,
`final_status` and `run_manifest_error` is itself a finding worth `R-0826`. Both are
reviewer-authored calls; this handback makes neither.
