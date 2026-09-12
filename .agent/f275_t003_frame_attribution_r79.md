# F275 T003 — the surviving over-selection frames, carried back to the ruled sites

> Written by the worker of F275 round 79 from its own run, under DECISION F275 D53.
> EVERY INDENTED LINE IN THIS FILE is a line of the instrument's saved output at
> `.remedy-wt/r79_inst.out`, spliced out of it by line range rather than retyped, and in the
> order that output prints it. The only figures outside that output are identifiers —
> feature, decision, finding, round and commit ids, and file names — and no line here
> carries a wall-clock duration.

`R-0880` names two obligations. Round 77 discharged the first: it partitioned the sites
the plain re-derivation drops by the shipped owner check's verdict, which is a property of
the SET. It left the second open, because the surviving over-selection frames are a property
of the RUN and nothing had carried one back to the site that produced it. This round does
that, and it is the whole of the round: no production line moves.

The method is fixed by a measurement rather than by preference. Round 77's transcript was
taken with one location line per failure, and that line names the frame the error was RAISED
in — for the largest class a file inside `pydantic`, outside this repository entirely. So
the attribution here is by the DEEPEST FRAME LYING INSIDE THE BUILT TREE, read off a fresh
capture that carries the whole frame list of every failure.

## 1. The inputs, and what this round left on disk

Four inputs are carried in unchanged: the ruled site set DECISION F275 D51 rules, its owner
verdicts, the guarded transform DECISION F275 D43 landed, and the status site set the
transform's fourth argument takes. Four saved transcripts are carried in as controls: round
77's transform summary and its suite run, plus round 76's unflipped control run and its
collect-only listing, which are what the bad-node arithmetic subtracts against.

  r77_corrected.json               120753 bytes  sha256 765b5ba99f2c92765349c3a013f4074c62ece893cb50b373450927af0290a512  carried in
  r77_corrected_owners.json        121095 bytes  sha256 670c6e952667b7c52b6c5a9ffd832dcc9f096aedfba114b83bc28ca061591b44  carried in
  r69_flip_transform_guarded.py      29032 bytes  sha256 075bc0dcb4b8ea2c3bd9cba47409d90b22f4a7d6a26d5e6799d6a40705ee5ae3  carried in
  r61_status.json                    1438 bytes  sha256 a4c6cd631b6669ea9ef58418e09471258f433a76e46c79e1ae363cf3eaad1e38  carried in
  r77_tf_corr.out                    1285 bytes  sha256 8897d3257d924c97d50642a7d73b47e401f92c7f0be46ae0d39eeda32f14299e  carried in
  r77_suite_corr.out               654679 bytes  sha256 a1405326e856f9b1a88c802e6418f43f7250037c68c1fd510b94968677e9038b  carried in
  r76_suite_ctl.out                 30331 bytes  sha256 020cd6ddab345b95f9cd4a9edf7d72a696133a70a1317c483e430d087119cd51  carried in
  r76_co_r53.out                  1996100 bytes  sha256 638960b440bfbe3dde0d379f482b2d8cb092cec216dfa2ed6af5139fb8c3e1b6  carried in
  r79_tf_corr.out                    1488 bytes  sha256 44cd9350f3e8683e6af1ca486082470dae67fdc3346d4b484b3691e6540e5430  PRODUCED THIS ROUND
  r79_suite_corr.out              4965147 bytes  sha256 0a49fc98bf36a84e0cd28dba7b7bf3acef2aaea1ae7b48549fa3f2ff388fcb22  PRODUCED THIS ROUND
  r79_frames.jsonl                3638751 bytes  sha256 16d876503e3c790cde16943d802116d305b15921268ed05ab43812ce1842bc43  PRODUCED THIS ROUND
  r79_co_corr.out                 1999041 bytes  sha256 7efc6cedf22d8efed27557676f894275f844d0deb28396ffdb19d5b24dc9c4df  PRODUCED THIS ROUND

  THE BUILT TREE THIS ROUND LEFT ON DISK, PINNED BY A DIGEST OVER ITS FILES
  .remedy-wt/r79_tree               57774 files  sha256 37b163e5c7f8870ca4b151e8e9172a50888a92d7e5773e26ace270f5bcaf91fb  PRODUCED THIS ROUND
  the digest is taken over the sorted list of every file in the tree outside .git and
  .pytest_cache, each as its relative path followed by its own sha256, so the reviewer
  can recompute it without the tree's index.

## 2. How the tree was built, and the transform control

The tree was built at `ef75e213`, the commit round 76 and round 77 both ran at, as an
unregistered copy rather than a registered worktree, so it can be left in place. Its tracked
`.py` files were compared against that commit's blobs before the transform ran. The vector
each step was invoked with is read back out of the step's own transcript below, not restated
from memory.

  Read back out of the saved transcripts rather than restated, so the vector below is
  the vector the run used.
  r79_g4a.txt          COMMAND: python3 -B .remedy-wt/r79_build_tree.py .remedy-wt/r79_tree ef75e213
  r79_g4a.txt          CWD: /home/decodeux/Repos/remedy
  r79_tf_corr.out      COMMAND: python3 -B .remedy-wt/r69_flip_transform_guarded.py .remedy-wt/r79_tree .remedy-wt/r77_corrected.json .remedy-wt/r77_corrected_owners.json .remedy-wt/r61_status.json
  r79_tf_corr.out      CWD: /home/decodeux/Repos/remedy
  r79_suite_corr.out   COMMAND: /usr/bin/python3 -B -m pytest -q --tb=long -p r79_frames_plugin
  r79_suite_corr.out   CWD: /home/decodeux/Repos/remedy/.remedy-wt/r79_tree
  r79_suite_corr.out   PYTHONPATH: /home/decodeux/Repos/remedy/.remedy-wt/r79_plugin
  r79_co_corr.out      COMMAND: /usr/bin/python3 -B -m pytest -q --collect-only
  r79_co_corr.out      CWD: /home/decodeux/Repos/remedy/.remedy-wt/r79_tree
  the build pass's own readings, quoted from its transcript:
    tracked .py in the built tree : 994
    tracked .py at ef75e213         : 994
    the two path lists are EQUAL  : True
    G4(a) .py files compared      : 994
    G4(a) .py files DIFFERING     : 0
    G4(a) .py files MISSING       : 0
    G4A_OK: True

The transform's fourth argument is the one the block did not name. `.remedy-wt/r61_status.json`
is the input that reproduces the control's nine rewrites under `T8 status value read`; it was
found in round 69's own guard-test script rather than guessed, and the reproduction below is
the evidence that it is the right one.

  round 77 summary lines: 36 | round 79 summary lines: 36
  the two summaries are LINE-FOR-LINE EQUAL: True
  differing lines: 0
  per-rule rows: round 77 24 | round 79 24 | EQUAL ROW FOR ROW: True
  CROSS-CHECK the rebuilt rule table against round 77's, by row count: 24 against 24 rows  -> MATCH
  ruled keys         round 77: PRECONDITION: ruled keys 2185 | resolving at this tree 2185 | NOT resolving 0
  ruled keys         round 79: PRECONDITION: ruled keys 2185 | resolving at this tree 2185 | NOT resolving 0
  files rewritten    round 77: files rewritten: 263 | skipped unparsable: 0
  files rewritten    round 79: files rewritten: 263 | skipped unparsable: 0
  total rewrites     round 77: total rewrites: 6078
  total rewrites     round 79: total rewrites: 6078

The summaries are equal line for line, which includes the precondition line, the file
counts, the whole per-rule table and the total. The suite pass was spent only after this
comparison came back empty.

## 3. The suite run's selection, and its bad-node total beside round 77's

A bad node is a node the flipped tree fails or errors and the unflipped control of round 76
does not. Both arms are counted that way, off their own transcripts.

  the unflipped CONTROL run of round 76: failed 1  errors 0
  round 77: failed 1174  errors 31  passed 17175  skipped 29  BAD NODES CAUSED BY THE FLIP 1204
  CROSS-CHECK round 77 failed node ids against its own tally line: 1174 against 1174 nodes  -> MATCH
  CROSS-CHECK round 77 error node ids against its own tally line: 31 against 31 nodes  -> MATCH
  PARTITION the round 77 arm: 1173 + 31 = 1204 against 1204 nodes  -> MATCH
  round 79: failed 1177  errors 31  passed 17202  skipped 29  BAD NODES CAUSED BY THE FLIP 1207
  CROSS-CHECK round 79 failed node ids against its own tally line: 1177 against 1177 nodes  -> MATCH
  CROSS-CHECK round 79 error node ids against its own tally line: 31 against 31 nodes  -> MATCH
  PARTITION the round 79 arm: 1176 + 31 = 1207 against 1207 nodes  -> MATCH
  BAD NODE TOTAL round 77: 1204 | round 79: 1207 | DIFFERENCE +3 which is 0.25 per cent of round 77's
  bad nodes round 79 holds that round 77 lacks: 3
  bad nodes round 77 holds that round 79 lacks: 0
      ONLY IN ROUND 79  tests/orchestration/test_autonomy.py::TestGitStatusReader::test_read_current_repo
      ONLY IN ROUND 79  tests/orchestration/test_event_name_coupling.py::TestEventNameCouplingRatchet::test_no_declared_entry_is_stale
      ONLY IN ROUND 79  tests/orchestration/test_event_name_coupling.py::TestEventNameCouplingRatchet::test_the_instrument_sees_the_deleted_modules_at_all

The difference is three nodes, which is well inside the five per cent the round's gate
treats as unremarkable, and it is one-directional: round 79 holds every bad node round 77
held. Two further differences are real and are stated here rather than left as unexplained
numerals.

THE FIRST IS THE SELECTED SET. Round 76 and round 77 ran pytest against `tests` alone. This
round ran it against the tree's root, which additionally collects the vendored sample
project under `scripts/`. Thirty nodes are selected that the earlier arms never selected,
every one of them passed, and none of them is a bad node, so the comparison above is
unaffected.

  nodes the run REPORTED round 77: 18409 | round 79: 18439 | DIFFERENCE +30
  collect-only node ids: round 76's arm 18409 | round 79 18439
    only in round 79: 30 | only in round 76: 0
    round 76's arm by top directory: tests 18409
    round 79 by top directory: scripts 30  tests 18409
    the nodes only round 79 selected, by test file:
         3  scripts/gauntlet_sample_project/tests/test_cli.py
         9  scripts/gauntlet_sample_project/tests/test_config.py
         4  scripts/gauntlet_sample_project/tests/test_importer.py
         6  scripts/gauntlet_sample_project/tests/test_parsing.py
         4  scripts/gauntlet_sample_project/tests/test_report.py
         4  scripts/gauntlet_sample_project/tests/test_retry.py
  PARTITION the extra selection by test file: 9 + 6 + 4 + 4 + 4 + 3 = 30 against 30 nodes  -> MATCH
    every extra node lies under scripts/: True
    every extra node PASSED, so none of them is a bad node: True

THE SECOND IS THE THREE EXTRA BAD NODES. All three read the repository's own git history,
and the tree this round built is a fresh `git init` over an extracted archive with no commit
in it, so a head sha reads empty and the deleted-module instrument sees nothing. That is a
property of how this round built the tree, not of the ruled site set. None of the three is
an `AttributeError` on a unified attribute, so none of them enters the attribution.

  THE THREE BAD NODES ONLY ROUND 79 HOLDS, BY THEIR OWN EXCEPTION
    AssertionError  tests/orchestration/test_autonomy.py::TestGitStatusReader::test_read_current_repo
      assert 0 > 0
    AssertionError  tests/orchestration/test_event_name_coupling.py::TestEventNameCouplingRatchet::test_no_declared_entry_is_stale
      these are no longer dead couplings and must leave the list: ['context_budget_optimized']
    AssertionError  tests/orchestration/test_event_name_coupling.py::TestEventNameCouplingRatchet::test_the_instrument_sees_the_deleted_modules_at_all
      assert 0 >= 40
    none of the three is an AttributeError naming a unified attribute: True

## 4. The frames `R-0880` names, in the fresh capture

The capture is a reporting-only pytest plugin loaded from outside the tree. It writes one
record per failing or erroring node carrying the node id, the exception class, the message
and the full raw frame list. It changed no file inside the tree and it raised nothing: the
count of its own error records is zero.

  traceback records captured: 1237   plugin_error records: 0
  distinct node ids among them: 1237
  CROSS-CHECK the captured node ids against the transcript's bad-and-control node ids: 1208 against 1208 nodes  -> MATCH
  AttributeError records naming a UNIFIED attribute: 30
     on a NAMED receiver class, which is what R-0880 reports: 25
     on NoneType, an absent receiver and a different cause   : 5
  PARTITION the unified-attribute records by receiver class: 25 + 5 = 30 against 30 records  -> MATCH
  the NAMED-class records against round 77's own failing node ids:
     of the 25 nodes, failing in round 77 as well: 25
     of the 25 nodes, NOT failing in round 77     : 0
  PARTITION the named-class records by whether round 77 failed the same node: 25 + 0 = 25 against 25 records  -> MATCH
     round 77's own reading of this class, taken off a --tb=line transcript, was 19
     frames on a named class and 5 on NoneType, over 24 location frames in total;
     the fresh capture reads the SAME NoneType count and 6 more named-class nodes,
     every one of which round 77 also failed, so the difference is what the earlier
     transcript could show and not a different population of failures.

The earlier transcript's own frames, re-read here with round 77's own regular expression, are
what fixes the method. They resolve to eight locations, and the one carrying half of them is
a file inside `pydantic` — the frame the error was RAISED in, not the site that reached it.

  ROUND 77's OWN LOCATION FRAMES, RE-READ HERE WITH ITS OWN REGEX
     location frames naming a unified attribute: 24
     distinct locations among them: 8
         12  /home/decodeux/.local/lib/python3.10/site-packages/pydantic/main.py:1042   a path inside this repository: False
          4  /home/decodeux/Repos/remedy/.remedy-wt/r77_corr/packages/orchestration/brain_detail.py:345   a path inside this repository: True
          2  /home/decodeux/Repos/remedy/.remedy-wt/r77_corr/apps/cli/commands/job.py:1459   a path inside this repository: True
          2  /home/decodeux/Repos/remedy/.remedy-wt/r77_corr/apps/cli/commands/job.py:1849   a path inside this repository: True
          1  /home/decodeux/Repos/remedy/.remedy-wt/r77_corr/apps/cli/commands/job.py:994   a path inside this repository: True
          1  /home/decodeux/Repos/remedy/.remedy-wt/r77_corr/packages/orchestration/project_registry.py:856   a path inside this repository: True
          1  /home/decodeux/Repos/remedy/.remedy-wt/r77_corr/tests/test_project_brain.py:263   a path inside this repository: True
          1  /home/decodeux/Repos/remedy/.remedy-wt/r77_corr/tests/test_project_brain.py:298   a path inside this repository: True
  PARTITION round 77's location frames by location: 12 + 4 + 2 + 2 + 1 + 1 + 1 + 1 = 24 against 24 frames  -> MATCH

The named-class count read here is larger than the one round 77 recorded, and the reason is
the instrument rather than the population: every node in this round's set also failed in
round 77, and the NoneType count is identical. The earlier transcript could not show six of
them as a parseable location frame, which is the same limitation that sent the largest group
of the frames it did show to a library file.

## 5. The attribution, by the deepest frame inside the built tree

For each record the deepest frame whose path lies inside the built tree is selected; frames
in `site-packages`, in the standard library and in pytest's own machinery are skipped. That
frame's path is reduced to a path relative to the tree root and paired with its line number,
the corrected set is asked whether it holds a ruled site at exactly that pair, and the source
line is read from `ef75e213` — the text the ruled site was keyed against, before the flip.

  the built tree's root is /home/decodeux/Repos/remedy/.remedy-wt/r79_tree
  ruled sites in the corrected set: 2185 over 2080 distinct (path, line) pairs
  records attributed to an in-tree frame: 30
  records with NO frame inside the tree, reported UNATTRIBUTABLE: 0
  PARTITION the unified-attribute records by attributability: 30 + 0 = 30 against 30 records  -> MATCH

  THE READING THIS ROUND EXISTS TO PRODUCE:
    frames landing ON a ruled site the corrected set holds : 17
    frames landing NOWHERE in the corrected set            : 13
  PARTITION the attributed frames by whether the corrected set holds the site: 17 + 13 = 30 against 30 frames  -> MATCH

THIS IS THE READING THE ROUND EXISTS TO PRODUCE. Seventeen of the thirty frames land on a
ruled site the corrected set holds, and those name sites the flip's input could drop.
Thirteen land nowhere in the set, and those are a different defect: the rewrite that produced
them did not come from a held site, so dropping sites cannot remove them.

The table below is one row per frame group, where a group is one receiver class, attribute,
relative path and line. Each row carries the site, whether the corrected set holds it and
with which columns and attributes, the pre-flip source line, and one example node.

  THE ATTRIBUTION TABLE, ONE ROW PER FRAME GROUP
  A group is one (receiver class, attribute, relative path, line) and its size is the
  number of failing nodes whose deepest in-tree frame is that location.
  distinct frame groups: 14
    GROUP size  12  Artifact.job_id
      site      tests/cli/test_repair_runtime.py:68  in _setup_job_with_failure
      RULED     the corrected set HOLDS this (path, line): (col 19, .id), (col 32, .id)
      source    ef75e213  return str(job.id), str(art.id), str(data_dir)
      example   tests/cli/test_repair_runtime.py::TestRepairStartRuntime::test_exit_zero_json
    GROUP size   4  BrainNode.task_id
      site      packages/orchestration/brain_detail.py:345  in <genexpr>
      RULED     the corrected set HOLDS this (path, line): (col 45, .id), (col 54, .id)
      source    ef75e213  task = next((t for t in job.tasks if str(t.id) == node.id), None)
      example   tests/orchestration/test_project_brain.py::TestBrainDetailRegistry::test_brain_detail_builds_for_all_node_types
    GROUP size   2  NoneType.job_id
      site      apps/cli/commands/job.py:1459  in _extract_job_truth
      RULED     the corrected set holds NO site at this (path, line)
      source    ef75e213  ev_data = ev if isinstance(ev, dict) else (ev.data if hasattr(ev, 'data') else {})
      example   tests/cli/test_product_spine.py::TestJobFacadeNoAgent::test_job_status_handler_no_agent
    GROUP size   2  NoneType.job_id
      site      apps/cli/commands/job.py:1849  in _cmd_job_digest
      RULED     the corrected set holds NO site at this (path, line)
      source    ef75e213  from packages.orchestration.job_digest import build_job_digest
      example   tests/cli/test_job_digest_cli.py::TestUnknownJobId::test_bare_mode_exits_1_with_a_clean_stderr_message
    GROUP size   1  BrainNode.job_id
      site      tests/test_project_brain.py:263  in test_empty_job_has_job_node
      RULED     the corrected set holds NO site at this (path, line)
      source    ef75e213  assert job_nodes[0].status == "pending"
      example   tests/test_project_brain.py::TestBuildProjectBrain::test_empty_job_has_job_node
    GROUP size   1  BrainNode.task_id
      site      tests/test_project_brain.py:298  in test_task_nodes_and_edges
      RULED     the corrected set holds NO site at this (path, line)
      source    ef75e213  assert task_nodes[0].status == "pending"
      example   tests/test_project_brain.py::TestBuildProjectBrain::test_task_nodes_and_edges
    GROUP size   1  NoneType.job_id
      site      apps/cli/commands/job.py:994  in _cmd_job_resume
      RULED     the corrected set holds NO site at this (path, line)
      source    ef75e213  try:
      example   tests/orchestration/test_resume_cli.py::TestDegradations::test_an_unknown_job_exits_one
    GROUP size   1  _FakeJob.job_id
      site      packages/orchestration/project_registry.py:856  in <dictcomp>
      RULED     the corrected set HOLDS this (path, line): (col 19, .id)
      source    ef75e213  job_map = {str(j.id): j for j in jobs}
      example   tests/test_project_registry.py::TestExportProjectJson::test_jobs_list_structure
    GROUP size   1  _FakeJob.job_id
      site      tests/orchestration/test_orchestrator_loop.py:1513  in test_what_execution_produced_is_on_the_ledger
      RULED     the corrected set holds NO site at this (path, line)
      source    ef75e213  assert "executed: terminal=all_green" in detail
      example   tests/orchestration/test_orchestrator_loop.py::TestTheLoopExecutesWhatItDispatches::test_what_execution_produced_is_on_the_ledger
    GROUP size   1  _FakeJob.job_id
      site      tests/orchestration/test_orchestrator_loop.py:1524  in test_a_stop_reason_from_the_executor_is_recorded
      RULED     the corrected set holds NO site at this (path, line)
      source    ef75e213  assert "stop=budget" in detail
      example   tests/orchestration/test_orchestrator_loop.py::TestTheLoopExecutesWhatItDispatches::test_a_stop_reason_from_the_executor_is_recorded
    GROUP size   1  _FakeJob.job_id
      site      tests/orchestration/test_orchestrator_loop.py:1765  in test_the_execution_outcome_reports_the_gate
      RULED     the corrected set holds NO site at this (path, line)
      source    ef75e213  assert "gate=released" in detail
      example   tests/orchestration/test_orchestrator_loop.py::TestAReleasedGateMakesTheMilestoneClaimable::test_the_execution_outcome_reports_the_gate
    GROUP size   1  _FakeJob.job_id
      site      tests/orchestration/test_orchestrator_loop.py:1776  in test_an_ungated_job_says_so_rather_than_implying_green
      RULED     the corrected set holds NO site at this (path, line)
      source    ef75e213  assert "gate=not-run" in detail
      example   tests/orchestration/test_orchestrator_loop.py::TestAReleasedGateMakesTheMilestoneClaimable::test_an_ungated_job_says_so_rather_than_implying_green
    GROUP size   1  _FakeJob.job_id
      site      tests/orchestration/test_orchestrator_loop.py:1825  in test_the_escalation_names_both_blockers
      RULED     the corrected set holds NO site at this (path, line)
      source    ef75e213  assert result.detail.count("acc-001") == 2
      example   tests/orchestration/test_orchestrator_loop.py::TestTheSecondBlockedCompletionEscalates::test_the_escalation_names_both_blockers
    GROUP size   1  _FakeJob.job_id
      site      tests/orchestration/test_orchestrator_loop.py:1833  in test_the_escalation_says_what_budget_it_saved
      RULED     the corrected set holds NO site at this (path, line)
      source    ef75e213  assert "more iteration(s) of this run's budget" in result.detail
      example   tests/orchestration/test_orchestrator_loop.py::TestTheSecondBlockedCompletionEscalates::test_the_escalation_says_what_budget_it_saved
  PARTITION the frame groups against the attributed records: 2 + 2 + 12 + 1 + 1 + 1 + 1 + 1 + 1 + 4 + 1 + 1 + 1 + 1 = 30 against 30 records  -> MATCH

Grouped by receiver class and attribute instead, with the sizes as measured:

  BY RECEIVER CLASS AND ATTRIBUTE, THE GROUP SIZES MEASURED
      12  Artifact.job_id   of them on a held ruled site: 12
       7  _FakeJob.job_id   of them on a held ruled site: 1
       5  BrainNode.task_id   of them on a held ruled site: 4
       5  NoneType.job_id   of them on a held ruled site: 0
       1  BrainNode.job_id   of them on a held ruled site: 0
  PARTITION the receiver-class groups against the attributed records: 12 + 7 + 5 + 5 + 1 = 30 against 30 records  -> MATCH

Two readings stand out of that grouping. The twelve `Artifact.job_id` frames all land on ONE
held site, a two-column line in a test helper, so a single site accounts for forty per cent
of the whole set. And the seven `_FakeJob.job_id` frames are almost all UNHELD: six of them
land on assertion lines in one test module, where the receiver is a local double rather than
a record the ruled set ever keyed.

The same result read by site rather than by class:

  THE DISTINCT RULED SITES THE FRAMES REACH
    distinct held (path, line) pairs reached: 3
         4 frames  packages/orchestration/brain_detail.py:345  (col 45, .id), (col 54, .id)
         1 frames  packages/orchestration/project_registry.py:856  (col 19, .id)
        12 frames  tests/cli/test_repair_runtime.py:68  (col 19, .id), (col 32, .id)
    distinct UNHELD (path, line) pairs reached: 11
         1 frames  apps/cli/commands/job.py:994  NOT in the corrected set
         2 frames  apps/cli/commands/job.py:1459  NOT in the corrected set
         2 frames  apps/cli/commands/job.py:1849  NOT in the corrected set
         1 frames  tests/orchestration/test_orchestrator_loop.py:1513  NOT in the corrected set
         1 frames  tests/orchestration/test_orchestrator_loop.py:1524  NOT in the corrected set
         1 frames  tests/orchestration/test_orchestrator_loop.py:1765  NOT in the corrected set
         1 frames  tests/orchestration/test_orchestrator_loop.py:1776  NOT in the corrected set
         1 frames  tests/orchestration/test_orchestrator_loop.py:1825  NOT in the corrected set
         1 frames  tests/orchestration/test_orchestrator_loop.py:1833  NOT in the corrected set
         1 frames  tests/test_project_brain.py:263  NOT in the corrected set
         1 frames  tests/test_project_brain.py:298  NOT in the corrected set

## 6. The unattributable set

A traceback with no frame inside the tree is reported as unattributable with its class and
its raising frame rather than forced onto a site. The rule was written expecting that set to
be non-empty, because round 77's reading put twelve frames inside `pydantic`. It is empty:
every one of the thirty tracebacks has at least one frame inside the built tree, which is
exactly the thing the deepest-in-tree rule recovers and the raised-frame reading loses.

=== 6. THE UNATTRIBUTABLE SET ===
  count: 0

The instrument's own checks, over the whole pass:

=== 7. THE CHECKS ===
  CROSS-CHECKS run 6  all MATCH: True
  PARTITIONS  run 10   all MATCH: True

## 7. What this reading does NOT settle

IT DOES NOT CHANGE THE FLIP'S INPUT SET. DECISION F275 D51 rules that set and this round
rules nothing about it; whether the seventeen held sites are dropped is a later decision
taken with this table in front of it, and dropping them is not obviously right — twelve of
them are one site in a test helper, and a site that produces an over-selection frame may
still be a site the flip must rewrite.

IT DOES NOT RESOLVE `R-0880`. The finding's second obligation asked for the attribution, not
for a repair, and whether the transform gains a refusal for a site whose owner verdict cannot
be confirmed is not decided here.

IT DOES NOT EXPLAIN THE THIRTEEN UNHELD FRAMES. They are reported as a separate class, and
what rewrote those lines is not measured by this round. Six of them sit in one test module
against a local double, which is a hypothesis and not a measurement.

IT SAYS NOTHING ABOUT THE OTHER RESIDUE. The run carries more than a thousand bad nodes and
this reading covers thirty of them — the ones whose message names a unified attribute. The
id-SHAPE seam DECISION F275 D37 routed into T003's resolver collapse is untouched.

IT IS NOT A GREEN SUITE AND WAS NEVER MEANT TO BE. The round reads tracebacks out of a
failing run; no gate of round 79 turns on the run's colour.

The tree and every transcript are pinned above and left on disk under `.remedy-wt/`, so the
next round re-analyses these bytes instead of re-taking the pass.
