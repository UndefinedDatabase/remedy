# F275 T003 — the flip's residue at `bd2a75d5`, round 87

WHAT THIS ROUND DID AND DID NOT DO. No production line moved: round 87 changes nothing under
`packages/`, `apps/`, `tests/`, `docs/` or `scripts/`. The worker ran no test suite. The three
full-suite transcripts classified below are the reviewer's, taken at `bd2a75d5` before the round
was authored, and are pinned by digest: `suite_ctl.out` sha256
`5b0883648f5a96b760194861ae0d3d9919a880b6a05f589f5d3856a316659463`, `suite_flip.out` sha256
`33d2cdaecb8d1ae86b306be999babf44311442df399c43920d0a807b9f32faa7` and `suite_flip_short.out` sha256
`8f79bcdba6702f237b520c42f0319d870495bfe0e8ed1dae2ed63f3b023df96e`. What the worker did run is the
committed generator over four plain-directory trees, the committed guarded transform over one
detached worktree at `bd2a75d5` that was restored, removed and pruned before C4, an `ast` census
over `packages/` at `bd2a75d5`, and the instrument committed at C4 over the pinned transcripts.

## The generator readings of G4, as measured

The four instruments were extracted from their committed carriers at `bd2a75d5`, one fence each and
the transform's two fences concatenated part 1 then part 2:

| Instrument | Carrier | Bytes | sha256 |
|---|---|---|---|
| re-key | `.agent/authored/f275-r59-rekey.py.md` | 5186 | `f56394e9ac2582d5655a64a135fbf95b2930c24d14e791a23a2eb2630742a721` |
| owner check | `.agent/authored/f275-r73-owner-stage.py.md` | 24253 | `7be3437450d1f183d241e8a5161a6ae182652d0aecd674ea10e8f870407eddb8` |
| generator | `.agent/authored/f275-r82-input.py.md` | 10580 | `c50da9738864bbfe3714d1042a0484cc800ee4c3afbdba8866d6221f4bc9d1f8` |
| transform | `.agent/authored/f275-r69-transform-guarded.part1.py.md` + `.part2.py.md` | 29032 | `075bc0dcb4b8ea2c3bd9cba47409d90b22f4a7d6a26d5e6799d6a40705ee5ae3` |

The trees: BASE from `git archive ef75e213`, TIP from `git archive bd2a75d5`, each followed by
`git init -q` and `git add -A -f .`; SHIFT and DELETE copies of TIP by `shutil.copytree(..., symlinks=True)`,
SHIFT with three empty lines inserted after line 1 of `packages/orchestration/brain_detail.py`, DELETE
with that file's one line `    job_id_str = str(job.id)` removed (its count in the file read 1, at
line 142), each re-indexed. The generator ran as its carrier's Usage line orders over the four trees,
`r77_corrected.json` and `r77_corrected_owners.json`, exit 0.

| Reading | Measured | Reviewer |
|---|---|---|
| paths under `packages/`, `apps/` or `tests/` differing between BASE and TIP | 21 | 21 |
| ruled sites after the subtraction | 2183 | 2183 |
| recovered by the scope key at TIP / SHIFT / DELETE | 2183 / 2183 / 2183 | 2183 each |
| UNRESOLVED at TIP / SHIFT / DELETE | 0 / 0 / 0 | 0 |
| line-key control at TIP / SHIFT / DELETE | 2157 / 2148 / 2148 | 2157 / 2148 / 2148 |
| owner check at TIP: CONFIRMED / REFUSED / CONTRADICTED | 1908 / 275 / 0 | 1908 / 275 / 0 |

## The transform readings of G4, as measured

The guarded transform ran over a worktree made by `git worktree add --detach` at `bd2a75d5`, with the
TIP re-keyed set, its owners file and `r61_status.json`, exit 0.

| Reading | Measured | Reviewer |
|---|---|---|
| PRECONDITION: keys resolving / not resolving | 2183 / 0 | 2183 / 0 |
| files rewritten | 264 | 264 |
| total rewrites | 6097 | 6097 |
| files the edit would have broken | 0 | 0 |
| `git diff --numstat`: files | 264 | 264 |
| insertions / deletions | 5252 / 5079 | 5252 / 5079 |
| insertions under `tests/` / elsewhere | 4177 / 1075 | 4177 / 1075 |
| largest single-file insertion count | 141, `tests/orchestration/test_job_fulfillment.py` | 141 |

The census by `ast` over the 269 `.py` files under `packages/` at `bd2a75d5`: a `UUID(...)` call is a call
whose callee is the bare name `UUID`; each is counted by the callee name, bare or attribute, of the
call it is a positional argument of. Import aliases are NOT followed. The attribute form
`<x>.UUID(...)` occurs 0 times, so it hides nothing.

| Reading | Measured | Reviewer |
|---|---|---|
| `UUID(...)` calls | 55 | 55 |
| a positional argument of `load_job` | 29 | 29 |
| a positional argument of `load_job_safe` | 4 | 4 |
| a positional argument of no call | 13 | not stated |
| of `str` / `load_project` | 3 / 2 | not stated |
| of `_lj` / `_mii` / `add` / `make_intent_id` | 1 each | not stated |

## The instrument's stdout, verbatim

The fence of `.agent/authored/f275-r87-residue.py.md` as committed at C4, extracted at 5468 bytes,
sha256 `d42fbd3c8b8c3048c31f877bef4f9ddc898a19c0522b4171745424fc94907317`, ran twice as
`python3 -B <fence> suite_ctl.out suite_flip.out suite_flip_short.out <prefix>`, the prefix being the
flipped tree's path inside the transcripts, `/home/decodeux/Repos/remedy/.remedy-wt/r87/wt_flip`. Both runs
exited 0 with no stderr, and the two stdouts are byte-identical at 5266 bytes, sha256
`3752f7a117bfd3aaafad4afd953a2fadfc6111fdda21fae11798b6e298775a53`. Every stdout line follows in order, indented by one space; the
stdout's empty lines stay empty rather than carrying a lone space.

 I1  THE TALLIES AND THE BAD NODES
     control        tally: 1 failed, 18429 passed, 29 skipped, 1 warning
     control        distinct FAILED/ERROR node ids: 1
     flipped        tally: 796 failed, 17603 passed, 29 skipped, 1 warning, 31 errors
     flipped        distinct FAILED/ERROR node ids: 827
     flipped short  tally: 795 failed, 17610 passed, 23 skipped, 1 warning, 31 errors
     flipped short  distinct FAILED/ERROR node ids: 826

 I2  THE SETS
     flip-only (flipped minus control): 826
     control-only (control minus flipped): 0
     symmetric difference of the two flipped transcripts: 1
         tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes  (only in flipped)

 I3  THE SECTIONS OF THE SHORT-TRACEBACK FLIPPED TRANSCRIPT
     sections: 826

 I4  THE CLASSIFICATION
     by exception class, count descending then name:
          233  AssertionError
          142  TypeError
          114  AttributeError
           85  ValueError
           80  http.client.RemoteDisconnected
           74  <none>
           25  KeyError
           23  IndexError
           15  FileNotFoundError
           13  json.decoder.JSONDecodeError
            8  packages.orchestration.mission_state.MissionError
            6  packages.orchestration.data_paths.JobIdNotFound
            3  Failed
            3  NameError
            2  pydantic_core._pydantic_core.ValidationError
     by (deepest in-tree frame, exception class), pairs of count 3 or more:
           80  packages/orchestration/data_paths.py::job_dir  TypeError
           56  tests/ui_server/test_command_channel.py::_request  http.client.RemoteDisconnected
           46  packages/orchestration/job_fulfillment.py::run_job_fulfill  ValueError
           31  packages/orchestration/pingpong_job.py::_persist_job  TypeError
           24  tests/orchestration/test_mission_e2e.py::e2e  KeyError
           13  packages/orchestration/mission_state.py::build_verify_first_task  TypeError
           12  packages/orchestration/flight_plan.py::map_flight_plan_to_tasks  TypeError
           10  tests/cli/test_context_inspect_runtime.py::_create_temp_job  AttributeError
            9  tests/orchestration/test_self_dogfood_execution.py::_approved_task  IndexError
            8  packages/orchestration/mission_state.py::continue_mission  packages.orchestration.mission_state.MissionError
            8  tests/cli/test_mission_cmd.py::_run  AssertionError
            8  tests/ui_server/test_command_dispatch.py::_approve  http.client.RemoteDisconnected
            7  tests/cli/test_loop_cmd.py::_stored_jobs  AttributeError
            7  tests/orchestration/test_resume_kill.py::_wait_for  AttributeError
            6  packages/orchestration/data_paths.py::lookup_job_id  packages.orchestration.data_paths.JobIdNotFound
            6  tests/test_data_paths.py::test_a_loading_handler_hands_load_job_the_id_a_short_prefix_resolves_to  AssertionError
            6  tests/ui_server/test_diff_endpoint.py::_get  http.client.RemoteDisconnected
            5  packages/orchestration/worker_queue.py::_run_via_task_execution  AttributeError
            5  tests/cli/test_job_report.py::test_every_reported_terminal_is_allowed  AssertionError
            5  tests/cli/test_mission_cmd.py::_run_in  AssertionError
            5  tests/cli/test_self_dogfood_execution_cli.py::_approved_task  IndexError
            5  tests/orchestration/test_run_report_hook.py::test_each_terminal_writes_exactly_one_report  AssertionError
            5  tests/orchestration/test_run_report_hook.py::test_the_report_names_the_terminal_it_was_written_for  FileNotFoundError
            4  packages/orchestration/worker_queue.py::_run_via_legacy_autorun  TypeError
            4  tests/orchestration/test_job_digest.py::test_the_envelope_names_the_job_and_its_state  AssertionError
            4  tests/orchestration/test_test_execution_service.py::_run_with_candidates  AttributeError
            4  tests/ui_server/test_command_dispatch.py::_post  http.client.RemoteDisconnected
            3  tests/orchestration/test_job_digest.py::test_the_normalized_envelope_equals_its_stored_golden  AssertionError
     by production frame path, count descending then path:
           86  packages/orchestration/data_paths.py
           46  packages/orchestration/job_fulfillment.py
           31  packages/orchestration/pingpong_job.py
           21  packages/orchestration/mission_state.py
           12  packages/orchestration/flight_plan.py
           10  apps/cli/commands/job.py
            9  packages/orchestration/worker_queue.py
            7  apps/cli/commands/brain.py
            2  apps/cli/commands/review_cmd.py
            2  packages/orchestration/patch_apply.py
            2  packages/orchestration/run_contract.py
            2  packages/orchestration/task_execution.py
            1  apps/cli/commands/project.py
            1  apps/cli/commands/repo.py
            1  packages/orchestration/agent_loop.py
            1  packages/orchestration/approval_queue.py
            1  packages/orchestration/autonomy_readiness.py
            1  packages/orchestration/project_registry.py
            1  packages/orchestration/reviewer.py
     deepest frames: production 237, test 589, unattributable 0
     CROSS-CHECK 237 + 589 + 0 = 826 sections: True
