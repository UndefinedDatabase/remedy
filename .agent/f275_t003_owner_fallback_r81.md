# F275 T003 — the seventeen attributed frames blame a FALLBACK, and the class it can reach

Round 80 corrected round 79's selection and handed forward a reading its own round did not act
on: of the twenty-four records whose exception is an `AttributeError` naming a unified
attribute, seventeen land on a ruled site the corrected set holds, at three sites carrying five
ruled columns between them. This round reads those five columns against the SHIPPED owner check
of DECISION F275 D47, measures the class they belong to across the whole corrected set, and
rules which of them come out of the flip's input. No production line moved, no suite ran and no
transform was executed.

THE HEADLINE IS THAT THE OWNER CHECK IS WRONG NOWHERE HERE. Every column the frames blame is a
column the check DECLINES to decide, and the transform renames it anyway, on the fallback its
P1 rule describes. That is a different defect from the one a reader of round 80's table would
reach for, and it sends the next round somewhere else entirely.

The five inputs are pinned by digest and none of them was regenerated:

    f275-r73-owner-stage.py         24253 bytes  7be3437450d1f183d241e8a5161a6ae182652d0aecd674ea10e8f870407eddb8  MATCH
    r77_corrected.json             120753 bytes  765b5ba99f2c92765349c3a013f4074c62ece893cb50b373450927af0290a512  MATCH
    r77_corrected_owners.json      121095 bytes  670c6e952667b7c52b6c5a9ffd832dcc9f096aedfba114b83bc28ca061591b44  MATCH
    r77_stage_corrected.out           447 bytes  86ecf97aa7c6a522427e2f137782594546a2f330d7a87f2242ec37bee2e56fc6  MATCH
    r79_frames.jsonl              3638751 bytes  16d876503e3c790cde16943d802116d305b15921268ed05ab43812ce1842bc43  MATCH
    every pinned input matches its digest and its byte count: True

## 1. What round 80 handed this round, re-derived rather than quoted

Round 80's figures are not copied out of its artefact. They are re-derived here from the same
pinned capture, with the same two rules — the record's exception CLASS is `AttributeError` and
its message names one of the four unified attributes — and the same attribution rule, the
deepest frame whose path lies inside the built tree reduced to a tree-relative path and line.
The six figures that result are then CROSS-CHECKED against the ones round 80 published, which
nothing in this round produced, so a disagreement between the two readings would show as a
difference rather than hide inside a quotation.

    JSON lines in the capture                                  : 1238
    of them per-node records, the population the rules run over: 1237
    of them session-level records                              : 1
    records the MESSAGE rule admits, as round 79 selected them : 30
    records the CLASS rule admits, round 80's correction       : 24
    records the CLASS rule REJECTS                             : 6
  PARTITION the message-rule records by exception class: 24 + 6 = 30 against 30 records  -> MATCH
    of the corrected set, on a NAMED receiver class            : 19
    of the corrected set, on NoneType                          : 5
  PARTITION the corrected set by receiver class: 19 + 5 = 24 against 24 records  -> MATCH
    frames landing ON a ruled site the corrected set holds     : 17
    frames landing NOWHERE in the corrected set                : 7
  PARTITION the attributed frames by whether the corrected set holds the site: 17 + 7 = 24 against 24 frames  -> MATCH
    distinct held (path, line) pairs the frames reach          : 3
       4 frames  packages/orchestration/brain_detail.py:345
       1 frames  packages/orchestration/project_registry.py:856
      12 frames  tests/cli/test_repair_runtime.py:68
    the six figures above are now compared against the ones round 80 PUBLISHED,
    which nothing in this round produced
  CROSS-CHECK class-rule records: 24 against 24 records  -> MATCH
  CROSS-CHECK on a named receiver class: 19 against 19 records  -> MATCH
  CROSS-CHECK on NoneType: 5 against 5 records  -> MATCH
  CROSS-CHECK frames on a held ruled site: 17 against 17 records  -> MATCH
  CROSS-CHECK frames landing nowhere: 7 against 7 records  -> MATCH
  CROSS-CHECK distinct held sites reached: 3 against 3 records  -> MATCH
    every re-derived figure reproduces round 80's              : True

The capture holds 1238 JSON lines and 1237 of them are per-node records; the rules run over the
per-node population and the session-level line is not one of them. Every figure reproduces.

## 2. The control over the rebuilt base tree, and the negative control on the recipe

The static check needs the UNFLIPPED tree, and it enumerates the files it will parse with
`git ls-files`. A plain archive extraction therefore hands it nothing, so the tree is built as
an archive of `ef75e213` extracted into a scratch directory and then given an index with
`git init` and `git add -A -f`. The control is that the shipped stage's summary over that tree
reproduces the pinned `.remedy-wt/r77_stage_corrected.out` line for line.

    the argument vector the control ran, verbatim
      python3 -B /home/decodeux/Repos/remedy/.remedy-wt/f275-r73-owner-stage.py /home/decodeux/Repos/remedy/.remedy-wt/r81_base_worker /home/decodeux/Repos/remedy/.remedy-wt/r77_corrected.json /home/decodeux/Repos/remedy/.remedy-wt/r77_corrected_owners.json --dump /home/decodeux/Repos/remedy/.remedy-wt/r81_decided.json
    the stage's own exit code                                  : 0
    per-line diff of the pinned summary against the measured one, the only line
    this harness adds to either side being none — it writes the REAL_EXIT trailer
    into both or into neither, and here into neither
      (no differing line)
    differing lines between the two summaries                  : 0
    the control reproduces the pinned summary                  : True
      ruled sites                 : 2185
      live record classes         : 71
         1908  CONFIRMED: the owner verdict matches the receiver's record
          107  REFUSED to decide: receiver's class not statically bound
          104  REFUSED to decide: annotation carries no class identity
           66  REFUSED to decide: receiver expression does not resolve
      DECIDED                     : 1908
      REFUSED, the stated blind spot: 277
      CONTRADICTED                : 0
      REAL_EXIT=0

THE CONTROL ONLY MEANS SOMETHING IF IT COULD HAVE FAILED, so the same extraction was run
WITHOUT the index. It decides nothing at all, and it does so quietly: the stage reports every
one of the 2185 ruled sites as sitting in a file it cannot read, finds zero live record
classes, and still exits zero. A gate that cannot fail wearing the face of a gate that cannot
pass is exactly the shape this control exists to rule out.

    python files ON DISK in the no-index tree                  : 994
    a .git directory exists in the no-index tree               : False
    git ls-files '*.py' there: exit 0, files 0
    what the stage decides over that tree, its own words
      ruled sites                 : 2185
      live record classes         : 0
         2185  file unreadable at this tree
      DECIDED                     : 0
      REFUSED, the stated blind spot: 0
      CONTRADICTED                : 0
      REAL_EXIT=0
    the negative control reproduces the pinned summary         : False
    so the control of G4(b) is a comparison that CAN fail      : True

The 994 Python files are on disk in both trees. Only the indexed one is visible to the stage.
The decided set the control dumped is what section 3 reads each column's verdict out of:

    ruled sites in the decided set the control dumped          : 1908
    ruled sites absent from it, the stated blind spot          : 277
  PARTITION the ruled set by whether the shipped check decided it: 1908 + 277 = 2185 against 2185 sites  -> MATCH

## 3. The five ruled columns at the three sites, with their verdicts

An `ast` column is a BYTE OFFSET into its line and the receiver identifier STARTS at that
offset. Reading backwards from the column finds nothing, and a class read that way reports as
empty when it is not; the receivers below are read forward from the offset, in bytes.

    the receiver is the identifier STARTING at the byte offset, per constraint 4
    tests/cli/test_repair_runtime.py:68 col 19 .id
      receiver read at that byte offset : job
      the shipped owner check says      : CONFIRMED
      the owners file names             : Job
      the ruled set holds this column   : True
      source at ef75e213                : return str(job.id), str(art.id), str(data_dir)
    tests/cli/test_repair_runtime.py:68 col 32 .id
      receiver read at that byte offset : art
      the shipped owner check says      : REFUSED
      the owners file names             : Job
      the ruled set holds this column   : True
      source at ef75e213                : return str(job.id), str(art.id), str(data_dir)
    packages/orchestration/brain_detail.py:345 col 45 .id
      receiver read at that byte offset : t
      the shipped owner check says      : CONFIRMED
      the owners file names             : Task
      the ruled set holds this column   : True
      source at ef75e213                : task = next((t for t in job.tasks if str(t.id) == node.id), None)
    packages/orchestration/brain_detail.py:345 col 54 .id
      receiver read at that byte offset : node
      the shipped owner check says      : REFUSED
      the owners file names             : Task
      the ruled set holds this column   : True
      source at ef75e213                : task = next((t for t in job.tasks if str(t.id) == node.id), None)
    packages/orchestration/project_registry.py:856 col 19 .id
      receiver read at that byte offset : j
      the shipped owner check says      : REFUSED
      the owners file names             : Job
      the ruled set holds this column   : True
      source at ef75e213                : job_map = {str(j.id): j for j in jobs}
    of the five, CONFIRMED by the shipped owner check          : 2
    of the five, REFUSED, absent from the decided set          : 3
  PARTITION the five ruled columns by the shipped check's verdict: 2 + 3 = 5 against 5 columns  -> MATCH

TWO OF THE FIVE ARE CONFIRMED AND THREE ARE REFUSED, and the refusals are not errors. `art`,
`node` and `j` are simply absent from the set the shipped check decided — it declined them,
for the reasons its own banner counts — while the ruled set holds all five, so the transform
renames all five.

THE FALLBACK IS WHERE THE RENAME COMES FROM. The transform's P1 rule takes the owner from the
static verdict where there is one, else from the probe's line, else from the receiver name. On
line 68 of `tests/cli/test_repair_runtime.py` the line carries one owner verdict, `Job`, and
both columns take it, so `art` — an Artifact — is renamed as a Job. On line 345 of
`packages/orchestration/brain_detail.py` the line carries `Task`, and `node` — a BrainNode —
is renamed as a Task. Those two renames are what the sixteen frames on those two lines report
at runtime, and calling them an owner-check error would send the next round to repair a
component that is behaving exactly as specified.

THE THIRD SITE IS NOT THAT SHAPE AND MUST NOT BE SWEPT IN WITH THE OTHER TWO. At
`packages/orchestration/project_registry.py:856` the receiver `j` iterates `jobs`, so the
rename is right for the production record; the single frame comes from a `_FakeJob` double in
the test that lacks the unified field. A site whose rename is correct and whose test double is
stale is a test to update with the flip, not a site to drop from its input.

## 4. The class, with its partition

The population the fallback can reach is not these three sites. It is every line carrying more
than one ruled site on which a single shared owner verdict spans sites whose receiver
identifiers DIFFER — because that is precisely the configuration in which a refused column
inherits the verdict of the column beside it and the two receivers are not the same thing. The
multi-site lines are partitioned by whether their sites' verdicts agree, and the agreeing part
is partitioned again by whether the receiver names differ. Both partitions are closed sums and
neither can fail; they are labelled as partitions for that reason.

    ruled sites in the corrected set                           : 2185
    distinct (path, line) pairs they sit on                    : 2080
    lines carrying MORE THAN ONE ruled site                    : 91
    of those, one SHARED verdict over DIFFERING receivers      : 26
    of those, one SHARED verdict over the SAME receiver name   : 32
    of those, owner verdicts that DISAGREE across the line     : 33
    sites on a multi-site line whose receiver would not read   : 0
  PARTITION the multi-site lines by whether their sites' verdicts agree: 58 + 33 = 91 against 91 lines  -> MATCH
  PARTITION the agreeing lines by whether their receiver names differ: 26 + 32 = 58 against 58 lines  -> MATCH
    THE CLASS ITSELF, ENUMERATED, one line per member, sorted
      packages/orchestration/brain_detail.py:345  verdict Task  receivers t node
      tests/cli/test_repair_runtime.py:68  verdict Job  receivers job art
      tests/cli/test_self_dogfood_execution_cli.py:38  verdict Job  receivers job tasks
      tests/orchestration/test_dag_schedule.py:153  verdict Task  receivers mid c
      tests/orchestration/test_dag_schedule.py:161  verdict Task  receivers legacy independent
      tests/orchestration/test_loop_run.py:340  verdict Job  receivers last_run_for_loop newer
      tests/orchestration/test_loop_run.py:354  verdict Job  receivers found mine
      tests/orchestration/test_loop_run.py:384  verdict Job  receivers found outcome
      tests/orchestration/test_loop_run.py:396  verdict Job  receivers found outcome
      tests/orchestration/test_mission_state.py:837  verdict Job  receivers job_one job_two
      tests/orchestration/test_repair_request_builder.py:69  verdict Job  receivers load_job job
      tests/orchestration/test_repair_request_builder.py:76  verdict Job  receivers load_job job
      tests/orchestration/test_self_dogfood_execution.py:71  verdict Job  receivers pt job
      tests/orchestration/test_self_dogfood_execution.py:83  verdict Job  receivers unapproved job
      tests/orchestration/test_self_dogfood_execution.py:89  verdict Job  receivers pt job
      tests/orchestration/test_self_dogfood_execution.py:95  verdict Job  receivers pt job
      tests/orchestration/test_self_dogfood_execution.py:109  verdict Job  receivers pt job
      tests/orchestration/test_self_dogfood_execution.py:121  verdict Job  receivers pt job
      tests/orchestration/test_self_dogfood_execution.py:128  verdict Job  receivers pt job
      tests/orchestration/test_self_dogfood_execution.py:129  verdict Job  receivers pt job
      tests/orchestration/test_self_dogfood_execution.py:136  verdict Job  receivers pt job
      tests/orchestration/test_self_dogfood_execution.py:213  verdict Job  receivers pt job
      tests/test_cli_main.py:500  verdict Task  receivers t task
      tests/test_project_brain.py:262  verdict Job  receivers job_nodes job
      tests/test_project_brain.py:297  verdict Task  receivers task_nodes task
      tests/test_runner.py:133  verdict Task  receivers result existing_task

The four counts are then CROSS-CHECKED against the figures the round 81 block states, which
were measured by the reviewer before this round was authored and which nothing in this run
produced. That comparison CAN fail, and is labelled as a cross-check rather than as a
partition for that reason.

  CROSS-CHECK ruled sites: 2185 against 2185 sites  -> MATCH
  CROSS-CHECK distinct lines: 2080 against 2080 lines  -> MATCH
  CROSS-CHECK multi-site lines: 91 against 91 lines  -> MATCH
  CROSS-CHECK shared verdict over differing receivers: 26 against 26 lines  -> MATCH
    every class figure reproduces the block's                  : True

TWENTY-SIX IS AN UPPER BOUND AND NOT A DEFECT COUNT. A shared verdict over differing receivers
can be right for both: `job_one` and `job_two` on one line of `test_mission_state.py` are both
Jobs, and the members the enumeration above draws from one self-dogfood test module pair `pt`
with `job` over and over, where the same reading may well hold. What the class is, is the set
of lines where the fallback has room
to be wrong, measured; which of them it is actually wrong on is not settled here and no site is
dropped on membership alone.

## 5. The ruling, and which sites it names

Both lines behind the behavioural evidence are in the class, and the third site is not even a
multi-site line — it carries one ruled column, so no shared verdict reaches it:

    packages/orchestration/brain_detail.py:345 is in the class: True
    tests/cli/test_repair_runtime.py:68 is in the class: True
  CROSS-CHECK the two lines behind the frames for membership in the class: 2 against 2 lines  -> MATCH
    the third site packages/orchestration/project_registry.py:856 carries 1 ruled site, so it is not a multi-site line at all
    frames on the class's two lines                            : 16 of 17
    frames on the third site, which the class does not reach   : 1
  PARTITION the on-site frames by whether their line is in the class: 16 + 1 = 17 against 17 frames  -> MATCH

DECISION F275 D55 is recorded on this reading. TWO SITES COME OUT OF THE FLIP'S INPUT BY NAME —
`tests/cli/test_repair_runtime.py` line 68 column 32 attribute `id`, and
`packages/orchestration/brain_detail.py` line 345 column 54 attribute `id`. Both carry
behavioural evidence: a rename at each produces failing nodes whose exception is an
`AttributeError` naming a unified attribute on a receiver of another record. The alternative of
dropping every site the check refuses — all 277 of them — is rejected, because refusal is not
evidence of error and DECISION F275 D45 already weighed and accepted that set; dropping it
wholesale would trade a measured defect for an unmeasured one.

THE THIRD SITE STAYS AND ITS TEST DOUBLE MOVES INSTEAD. `packages/orchestration/project_registry.py`
line 856 column 19 keeps its place in the flip's input and the `_FakeJob` double is updated in
the flip's own commit, per the rule that a rename never leaves a stub behind it: the test
follows the record, not the other way round.

## 6. What this reading does NOT settle

`R-0880` REMAINS OPEN. Its second obligation asks the transform to REFUSE a site whose owner
verdict cannot be confirmed, and this round neither builds that refusal nor closes the case for
it. What it adds is the first behavioural measurement of what the fallback costs and two sites
removed by name; the finding's own subject — a transform that renames on a verdict it does not
have — is untouched.

ONLY WHAT A TEST EXERCISES PRODUCED A FRAME. The seventeen frames come from nodes that ran and
failed; the fallback reaches sites no test reaches, and those are invisible to every reading
this chain has taken. The class of twenty-six bounds where it can reach, not where it did.

NOTHING HERE MEASURES THE 277 REFUSALS AS A WHOLE. Three of them were read; the other 274 were
counted and not examined, and DECISION F275 D45's acceptance of that set stands unrevisited.

The gate-bearing comparisons of the instrument behind this artefact, in one place:

    G4(a) the pinned inputs match their digests                : True
    G4(b) the control reproduces round 77's summary            : True
    G4(c) the no-index tree decides something else             : True
    G4(d) the five columns split CONFIRMED 2, REFUSED 3        : True
    G4(e) the class has 26 members over 91 multi-site lines     : True
    G4(f) every cross-checked figure reproduces                : True

Every figure above was produced by one run of one instrument over the pinned inputs and the
rebuilt base tree. Where a figure the round 81 block states differs from one measured here,
this file carries the measured one; no such difference was found.
