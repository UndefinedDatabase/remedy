# F275 T003 — the surviving over-selection frames, re-classified by the exception

> Written by the worker of F275 round 80 from its own run. It CORRECTS
> `.agent/f275_t003_frame_attribution_r79.md`, which is not edited and stays on disk as it
> landed, and it is read beside DECISION F275 D54, which corrects DECISION F275 D53 by
> appending to it rather than by rewriting it.
> EVERY INDENTED LINE IN THIS FILE is a line of the corrected instrument's saved output at
> `.remedy-wt/r80_inst.out`, spliced out of it by anchor rather than retyped, and in the order
> that output prints it. The only figures outside that output are identifiers — feature,
> decision, finding, round and commit ids, file names and line numbers inside them — and no
> line here carries a wall-clock duration.

## 1. What round 79 published, and what was wrong with it

Round 79 selected the frames `R-0880` names by searching each captured record's MESSAGE for
the text an attribute error carries, and it never asked what the record's exception CLASS
was. A pytest record for a failing assertion carries the whole assertion text as its message,
so a test asserting over an object that itself raised an attribute error quotes that error
inside the assertion's own text. Six such records were admitted to a set the round then
described as the class `R-0880` names.

THE DEFECT IS ONE MISSING CONDITION IN A PREDICATE, not a bad capture and not a bad
attribution rule. The capture is sound and is not re-taken; the built tree is not rebuilt;
the transform is not re-run. This round re-analyses the same pinned bytes with the class
condition added, and everything downstream of the selection is round 79's, unchanged.

WHAT THE CORRECTION COSTS ROUND 79's PUBLISHED SENTENCE. That round's artefact and DECISION
F275 D53 both explained a named-class count larger than round 77's by reasoning about the
instrument that produced the EARLIER number — that a location-line transcript could not show
six further nodes, and that the difference was the instrument and not a different population
of failures. Corrected, the named-class count is the same as the one round 77 recorded, kind
for kind, so round 77's reading never needed explaining away and that sentence is false in
both halves. DECISION F275 D54 withdraws it. The landed text stays where it landed.

## 2. The inputs, by digest

Every input is pinned and none is regenerated. The four this round's block pins by digest —
the capture, round 79's instrument, the corrected site set and round 79's own saved output —
were compared against their pinned digests before anything ran. The tag `PRODUCED THIS
ROUND` below belongs to round 79's own list of inputs, carried into this instrument
unchanged; the four it marks were produced by round 79 and are read here, not re-made.

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

## 3. The corrected selection, and the set it now excludes

A record enters the working set when BOTH hold: its exception CLASS is `AttributeError`, and
its message names one of the four unified attributes. The instrument reports both rules, so
the difference between them is a measurement rather than a claim, and it enumerates every
record the class rule rejects — a repair that silently drops records is indistinguishable
from a repair that loses them.

  THE TWO RULES, THE SECOND OF WHICH IS ROUND 80's CORRECTION
  records the MESSAGE rule admits, as round 79 selected them : 30
  records the CLASS rule admits, the corrected set           : 24
  records the CLASS rule REJECTS                             : 6
  PARTITION the message-rule records by exception class: 24 + 6 = 30 against 30 records  -> MATCH
  THE REJECTED SET, ENUMERATED, because a repair that silently drops records is
  indistinguishable from a repair that loses them
    exception AssertionError   names _FakeJob.job_id
      node tests/orchestration/test_orchestrator_loop.py::TestAReleasedGateMakesTheMilestoneClaimable::test_an_ungated_job_says_so_rather_than_implying_green
    exception AssertionError   names _FakeJob.job_id
      node tests/orchestration/test_orchestrator_loop.py::TestAReleasedGateMakesTheMilestoneClaimable::test_the_execution_outcome_reports_the_gate
    exception AssertionError   names _FakeJob.job_id
      node tests/orchestration/test_orchestrator_loop.py::TestTheLoopExecutesWhatItDispatches::test_a_stop_reason_from_the_executor_is_recorded
    exception AssertionError   names _FakeJob.job_id
      node tests/orchestration/test_orchestrator_loop.py::TestTheLoopExecutesWhatItDispatches::test_what_execution_produced_is_on_the_ledger
    exception AssertionError   names _FakeJob.job_id
      node tests/orchestration/test_orchestrator_loop.py::TestTheSecondBlockedCompletionEscalates::test_the_escalation_names_both_blockers
    exception AssertionError   names _FakeJob.job_id
      node tests/orchestration/test_orchestrator_loop.py::TestTheSecondBlockedCompletionEscalates::test_the_escalation_says_what_budget_it_saved
    the rejected records by exception class: AssertionError 6
    the rejected records by test file: tests/orchestration/test_orchestrator_loop.py 6
  AttributeError records naming a UNIFIED attribute: 24
     on a NAMED receiver class, which is what R-0880 reports: 19
     on NoneType, an absent receiver and a different cause   : 5
  PARTITION the unified-attribute records by receiver class: 19 + 5 = 24 against 24 records  -> MATCH
  the NAMED-class records against round 77's own failing node ids:
     of the 19 nodes, failing in round 77 as well: 19
     of the 19 nodes, NOT failing in round 77     : 0
  PARTITION the named-class records by whether round 77 failed the same node: 19 + 0 = 19 against 19 records  -> MATCH

EVERY REJECTED RECORD IS AN `AssertionError`, AND EVERY ONE SITS IN ONE TEST MODULE, against
a local `_FakeJob` double. The partition above adds the corrected set and the rejected set
back to the set the message rule admitted and cannot fail; the comparison below is a
CROSS-CHECK between two numbers reached by different routes and can.

THE CROSS-CHECK IS AGAINST A NUMBER NOTHING IN THIS ROUND PRODUCED: the figure
`.agent/f275_t003_flip_residue_r77.md` records for this class, read out of that file's
CORRECTED arm through its own marker so the larger figure the round 53 arm carries on
identical wording cannot be read by mistake.

     AGAINST ROUND 77's OWN RECORDED READING, WHICH NOTHING IN THIS ROUND PRODUCED.
     the arm read is the CORRECTED one, reached through its own '--- CORRECTED ---'
     marker, so the round 53 arm's larger figure on the same wording cannot be read
     by mistake
     the figure .agent/f275_t003_flip_residue_r77.md records for this class: 19 frames over 4 kinds
  CROSS-CHECK the CORRECTED named-class count against round 77's recorded figure: 19 against 19 frames  -> MATCH
     the corrected per-kind counts against round 77's, kind by kind:
       Artifact.job_id          round 77  12   corrected  12   MATCH
       BrainNode.job_id         round 77   1   corrected   1   MATCH
       BrainNode.task_id        round 77   5   corrected   5   MATCH
       _FakeJob.job_id          round 77   1   corrected   1   MATCH
  CROSS-CHECK the corrected per-kind breakdown against round 77's, as a mapping: {'Artifact.job_id': 12, 'BrainNode.task_id': 5, 'BrainNode.job_id': 1, '_FakeJob.job_id': 1} against {'Artifact.job_id': 12, 'BrainNode.task_id': 5, 'BrainNode.job_id': 1, '_FakeJob.job_id': 1} kinds  -> MATCH
     ROUND 79 PRINTED FIVE HARD-CODED LINES HERE, saying the fresh capture read six
     more named-class nodes than round 77 and that the gap was what the earlier
     transcript could show rather than a different population. The added class
     condition falsifies that sentence and DECISION F275 D54 withdraws it; the lines
     above are measured in its place.

The corrected count equals round 77's, and so does every per-kind count. Two readings taken
by different instruments over different captures agree exactly, which is what round 79's
explanation of its own larger number denied was possible.

## 4. The corrected attribution table

The attribution rule is round 79's and is untouched: the deepest frame whose path lies inside
the built tree, reduced to a tree-relative path and line, asked of the corrected site set, and
read back against the pre-flip source line at `ef75e213`. Only the set it runs over changed.

  the built tree's root is /home/decodeux/Repos/remedy/.remedy-wt/r79_tree
  ruled sites in the corrected set: 2185 over 2080 distinct (path, line) pairs
  records attributed to an in-tree frame: 24
  records with NO frame inside the tree, reported UNATTRIBUTABLE: 0
  PARTITION the unified-attribute records by attributability: 24 + 0 = 24 against 24 records  -> MATCH

  THE READING THIS ROUND EXISTS TO PRODUCE:
    frames landing ON a ruled site the corrected set holds : 17
    frames landing NOWHERE in the corrected set            : 7
  PARTITION the attributed frames by whether the corrected set holds the site: 17 + 7 = 24 against 24 frames  -> MATCH

The table below is round 79's own row format, one row per frame group, where a group is one
receiver class, attribute, relative path and line. Each row carries the site, whether the
corrected set holds it and with which columns and attributes, the pre-flip source line, and
one example node.

  THE ATTRIBUTION TABLE, ONE ROW PER FRAME GROUP
  A group is one (receiver class, attribute, relative path, line) and its size is the
  number of failing nodes whose deepest in-tree frame is that location.
  distinct frame groups: 8
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
  PARTITION the frame groups against the attributed records: 2 + 2 + 12 + 4 + 1 + 1 + 1 + 1 = 24 against 24 records  -> MATCH

Grouped by receiver class and attribute instead, with the sizes as measured:

  BY RECEIVER CLASS AND ATTRIBUTE, THE GROUP SIZES MEASURED
      12  Artifact.job_id   of them on a held ruled site: 12
       5  BrainNode.task_id   of them on a held ruled site: 4
       5  NoneType.job_id   of them on a held ruled site: 0
       1  BrainNode.job_id   of them on a held ruled site: 0
       1  _FakeJob.job_id   of them on a held ruled site: 1
  PARTITION the receiver-class groups against the attributed records: 12 + 5 + 5 + 1 + 1 = 24 against 24 records  -> MATCH

The `_FakeJob.job_id` class is where the correction lands. Round 79's own by-class table read
it as the second largest class in the set and as almost entirely unheld; corrected, it is a
single frame, and that frame is on a held site. The same result read by site rather than by
class:

  THE DISTINCT RULED SITES THE FRAMES REACH
    distinct held (path, line) pairs reached: 3
         4 frames  packages/orchestration/brain_detail.py:345  (col 45, .id), (col 54, .id)
         1 frames  packages/orchestration/project_registry.py:856  (col 19, .id)
        12 frames  tests/cli/test_repair_runtime.py:68  (col 19, .id), (col 32, .id)
    distinct UNHELD (path, line) pairs reached: 5
         1 frames  apps/cli/commands/job.py:994  NOT in the corrected set
         2 frames  apps/cli/commands/job.py:1459  NOT in the corrected set
         2 frames  apps/cli/commands/job.py:1849  NOT in the corrected set
         1 frames  tests/test_project_brain.py:263  NOT in the corrected set
         1 frames  tests/test_project_brain.py:298  NOT in the corrected set

THE THREE HELD SITES ARE THE ACTIONABLE RESULT AND THEY DID NOT MOVE. They are the same three
sites, with the same frame counts and the same ruled columns, as round 79 published. A
traceback with no frame inside the built tree would be reported as unattributable rather than
forced onto a site; that set is empty here, as it was in round 79:

  count: 0

## 5. The two splits side by side, and the rows that moved

Round 79's split is not quoted from its artefact. It is RECOMPUTED here from the same pinned
records, with the same attribution rules, over the set its message rule selected, and is then
cross-checked against the figures round 79 itself printed into its saved output — so a reader
of both artefacts can see which rows moved and which did not without re-running anything.

  Round 79's split is RECOMPUTED here from the same pinned records with the same
  attribution rules, over the set its MESSAGE rule selected, and is then cross-checked
  against the figures round 79 itself printed into r79_inst.out.
  CROSS-CHECK the recomputed round 79 ON-site count against the figure round 79 published: 17 against 17 frames  -> MATCH
  CROSS-CHECK the recomputed round 79 OFF-site count against the figure round 79 published: 13 against 13 frames  -> MATCH
  THE SPLIT, ROUND 79 BESIDE ROUND 80
    selected records                      round 79   30   round 80   24
    attributed to an in-tree frame        round 79   30   round 80   24
    unattributable                        round 79    0   round 80    0
    landing ON a ruled site held          round 79   17   round 80   17
    landing NOWHERE in the corrected set  round 79   13   round 80    7
  PARTITION the round 79 attributed frames: 17 + 13 = 30 against 30 frames  -> MATCH
    the ON-site half moved by +0 frames and the OFF-site half by -6
  distinct frame groups   round 79 14   round 80 8
  CROSS-CHECK the recomputed round 79 group count against the figure round 79 published: 14 against 14 groups  -> MATCH
  THE ROWS THAT MOVED, NAMED INDIVIDUALLY: 6
    ROW _FakeJob.job_id  at tests/orchestration/test_orchestrator_loop.py:1513
      size round 79 1  ->  size round 80 0   change -1
      the corrected set holds this (path, line): False
    ROW _FakeJob.job_id  at tests/orchestration/test_orchestrator_loop.py:1524
      size round 79 1  ->  size round 80 0   change -1
      the corrected set holds this (path, line): False
    ROW _FakeJob.job_id  at tests/orchestration/test_orchestrator_loop.py:1765
      size round 79 1  ->  size round 80 0   change -1
      the corrected set holds this (path, line): False
    ROW _FakeJob.job_id  at tests/orchestration/test_orchestrator_loop.py:1776
      size round 79 1  ->  size round 80 0   change -1
      the corrected set holds this (path, line): False
    ROW _FakeJob.job_id  at tests/orchestration/test_orchestrator_loop.py:1825
      size round 79 1  ->  size round 80 0   change -1
      the corrected set holds this (path, line): False
    ROW _FakeJob.job_id  at tests/orchestration/test_orchestrator_loop.py:1833
      size round 79 1  ->  size round 80 0   change -1
      the corrected set holds this (path, line): False
  rows identical in both tables: 8
  PARTITION the round 79 rows by whether they moved: 8 + 6 = 14 against 14 rows  -> MATCH
  EVERY MOVED ROW LIES IN THE OFF-SITE HALF: True

THE HALF THE ROUND EXISTED FOR SURVIVES INTACT. The on-site half does not move at all: the
same frames land on the same three held sites. The whole of the change falls in the other
half, and every moved row is a row the corrected set holds no site for, so no held site loses
a witness and none gains one. The rows that moved are six rows of one frame each, all of them
`_FakeJob.job_id` on assertion lines in one test module.

The instrument's own checks, over the whole pass, after the correction:

  CROSS-CHECKS run 11  all MATCH: True
  PARTITIONS  run 13   all MATCH: True

## 6. What this corrected reading does NOT settle

IT DOES NOT RESOLVE `R-0880`. THE FINDING REMAINS OPEN. Its second obligation asked for the
attribution and now has a corrected one behind it; whether the transform gains a refusal for
a site whose owner verdict cannot be confirmed is not decided here, and nothing in this round
resolves the finding or proposes to.

IT DOES NOT CHANGE THE FLIP'S INPUT SET. DECISION F275 D51 rules that set and neither this
round nor DECISION F275 D54 changes it. Whether the held sites the attribution names are
dropped is a later decision taken with this table in front of it, and dropping them is not
obviously right — most of the frames are one site in a test helper, and a site that produces
an over-selection frame may still be a site the flip must rewrite.

IT DOES NOT RE-VERIFY ROUND 79's CAPTURE OR ITS TREE. The capture, the built tree and the
transform control are read as pinned bytes. If the capture itself were wrong, this round
would not see it; what this round measured is the predicate applied to that capture.

IT DOES NOT EXPLAIN THE UNHELD FRAMES THAT REMAIN. They are reported as a separate class and
what rewrote those lines is not measured here.

IT SAYS NOTHING ABOUT THE OTHER RESIDUE. The run carries more than a thousand bad nodes and
this reading covers the ones whose message names a unified attribute and whose exception is
an attribute error. The id-SHAPE seam DECISION F275 D37 routed into T003's resolver collapse
is untouched.

IT IS NOT A GREEN SUITE AND WAS NEVER MEANT TO BE. No suite ran this round at all; the round
re-analysed saved bytes, and no gate of round 80 turns on a run's colour.

The tree and every transcript stay on disk under `.remedy-wt/`, pinned by the digests above,
so the next round re-analyses these bytes instead of re-taking the pass.
