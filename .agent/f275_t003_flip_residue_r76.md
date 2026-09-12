# F275 T003 — what the two corrections cost the FLIP, measured in FAILURES: the plain set trades an over-selection for a larger under-selection

> Measured by the reviewer at `ef75e213`, this round's base, in four disposable `git
> worktree`s under the gitignored `.remedy-wt/`, all removed and pruned before this text was
> authored. THIS FILE RECORDS A DRY RUN; IT FLIPS NOTHING. No line under `packages/`,
> `apps/`, `tests/`, `docs/` or `scripts/` moved in the round that wrote it. It replaces
> none of `.agent/f275_t003_flip_residue.md`, `_r50.md`, `_r55.md`, `_r58.md`, `_r59.md`,
> `_r60.md`, `_r61.md`, `_r63.md`, `_r65.md`, `_r67.md` or `_r68.md`, which stay as written.
>
> PROVENANCE, AS A SHAPE AND NOT AS A RANGE. Every INDENTED line below is quoted verbatim
> from the output of the committed instrument `.agent/authored/f275-r76-instrument.py.md`,
> which is what this round's gate runs. Every maximal run of digits in the PROSE — that is,
> on every line that does NOT begin with whitespace — is one of exactly two kinds. Either it
> is A FIGURE THAT ALSO OCCURS as a digit run in that same output, or it is A CITATION: a
> digit run belonging to a feature id, a task slice id, a decision id, a finding id, a round
> number, a commit id or an artefact file name, or a figure this document quotes from a
> named decision in order to discuss it. There is no third kind, and NO FIGURE BELOW IS A
> REVIEWER READING taken outside the instrument — which is the difference between this
> document and the round 67 artefact, whose own clause had to except two pytest summary
> lines. This clause is authoritative over the gate that checks it: where the two differ in
> wording, these words rule.

## 1. Why this reading was owed, and by whom

Three decisions in a row deferred it and each said so by name. DECISION F275 D41's
alternative (iii) deferred re-running the flip's dry run against the plain set because its
reading "is only meaningful once the 54 are ruled". DECISION F275 D42 ruled them and closed
with the observation that "the flip's dry run has still not been re-run against the plain
re-derived set of round 67". DECISION F275 D44's consequence paragraph repeated it for the
corrected inputs of rounds 67 and 69 together. `.agent/plan.md` has carried it as item 1
ever since. This file is that run.

## 2. The design: one variable, and the control that proves the base did not move

Both arms run the SAME guarded transform DECISION F275 D43 landed, at the same commit, over
the same tracked `.py` files, with the same status input. They differ in the RULED SITE SET
alone.

THE BASE HAS NOT MOVED SINCE THE LAST DRY RUN, WHICH IS WHY THESE FIGURES ARE COMPARABLE TO
ROUND 59's AT ALL. The `packages`, `apps`, `tests`, `docs` and `scripts` tree object ids are
identical at `bf692757`, round 59's base, and at `ef75e213`, this round's base, and the 994
tracked `.py` files are identical between them. Two further controls hold. The re-key stage
run here against the round 53 set reproduces `.remedy-wt/r69_rekeyed.json` BYTE FOR BYTE, and
the round 53 arm's transform reproduces round 69's own figures exactly, at 263 files and 6091
rewrites. A rebuild that could not reproduce its predecessor's numbers would be measuring two
things at once; this one reproduces both.

## 3. The two sets

    === 1. THE TWO RULED SITE SETS, IN SITES ===
      round 53 committed set                 : 2198 sites
      round 67 plain re-derivation           : 2138 sites
      PLAIN is a SUBSET of round 53's        : True
      sites round 53 rules and PLAIN drops   : 60 sites
      sites PLAIN rules and round 53 lacks   : 0 sites

THE PLAIN SET IS A STRICT SUBSET. Round 67 measured it as recovering 22 sites the REWRITTEN
re-derivation had dropped, and that reading stands unchanged; what no round had asked is how
the re-derived set compares to the set the transform actually consumes. It is 60 sites
smaller and adds nothing. Where those 60 sit decides everything below:

      of them in production files: 35 sites over 8 files
      of them in test files      : 25 sites over 9 files
      PARTITION production against test: 35 + 25 = 60 against 60 sites  -> MATCH

## 4. What the transform did with each

    === 2. THE TWO TRANSFORM RUNS, IN REWRITES ===
           ruled:  round 53   2198   PLAIN   2138   difference   -60
           files:  round 53    263   PLAIN    263   difference    +0
           total:  round 53   6091   PLAIN   6032   difference   -59
       undecided:  round 53   3084   PLAIN   3143   difference   +59

      the rules whose count MOVED, in rewrites:
          T2 job field                         1786 ->   1754     -32
          T3 task field                         411 ->    384     -27
      CROSS-CHECK the rules that MOVED against the change in the printed total: -59 against -59 rewrites  -> MATCH
      CROSS-CHECK the round 53 arm's rule table against its own printed total: 6091 against 6091 rewrites  -> MATCH
      rules unchanged across the two arms: 22

SIXTY FEWER RULED SITES BUY FIFTY-NINE FEWER RENAMES AND FIFTY-NINE MORE UNDECIDED SITES, and
the missing one is accounted for rather than waved at: the round 53 set carries exactly one
site with no owner verdict, the single `art` receiver round 59's run also reported, and a
site the transform cannot attribute to an owner is left alone whether or not the set holds
it. Every other rule is untouched, so the difference is the two field renames and nothing
else.

## 5. The three suite runs

    === 3. THE THREE SUITE RUNS, IN TEST NODES ===
      node ids collected from the short summaries, in nodes:
        CONTROL  failed     1   errors     0
        R53      failed  1186   errors    42
        PLAIN    failed  1331   errors    31

Those counts are read TWICE, from two places in the same transcript, because a number derived
once cannot be checked against itself:

      CROSS-CHECK PLAIN failed node ids against the tally line: 1331 against 1331 nodes  -> MATCH
      CROSS-CHECK PLAIN error node ids against the tally line: 31 against 31 nodes  -> MATCH

      nodes bad in the CONTROL too, and therefore a worktree artefact and not the flip:
        R53 1   PLAIN 1
          tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes

      CAUSED BY THE FLIP, in nodes:
        R53     1227   = failures  1185 + errors    42
        PLAIN   1361   = failures  1330 + errors    31
        THE PLAIN SET COSTS +134 BAD NODES over the round 53 set.

THE CONTROL REPRODUCES ROUND 59's TO THE UNIT — one failure, and it is the node that needs
the gitignored `apps/ui/node_modules`, absent from any fresh worktree. That single shared
failure is subtracted from both arms rather than argued away.

AND THE ANSWER TO THE QUESTION THIS ROUND EXISTS TO ASK IS THAT THE PLAIN SET IS WORSE. It
does not cost a little; it costs 134 additional bad nodes, which is more than a tenth of the
residue the flip already carries.

## 6. The arm difference, and it moves in both directions

    === 4. THE ARM DIFFERENCE, IN NODES ===
      bad under PLAIN only (the plain set BREAKS) : 172 nodes
      bad under R53 only   (the plain set FIXES)  : 38 nodes
      bad under both                              : 1189 nodes
      PARTITION the PLAIN arm by shared and own: 1189 + 172 = 1361 against 1361 nodes  -> MATCH
      PARTITION the round 53 arm by shared and own: 1189 + 38 = 1227 against 1227 nodes  -> MATCH

The plain set is not uniformly worse, which is the whole reason this reading is worth taking:
it breaks 172 nodes and fixes 38. The two lists attribute themselves.

      the plain set BREAKS, by test file, in nodes (11 files):
            36  tests/test_task_runner.py                                      holds a dropped site: False
            31  tests/orchestration/test_long_run_executor.py                  holds a dropped site: False
            30  tests/test_verifier.py                                         holds a dropped site: False
            25  tests/orchestration/test_self_healing_cycles.py                holds a dropped site: False
            19  tests/orchestration/test_dag_schedule.py                       holds a dropped site: False
            14  tests/test_workspace.py                                        holds a dropped site: False

      the plain set FIXES, by test file, in nodes (9 files):
            11  tests/cli/test_repair_runtime.py                               holds a dropped site: True
             8  tests/orchestration/test_watchdog.py                           holds a dropped site: True
             6  tests/orchestration/test_loop_run.py                           holds a dropped site: False
             3  tests/cli/test_repair_request_cli.py                           holds a dropped site: True

THE TWO LISTS READ IN OPPOSITE DIRECTIONS AND THE COLUMN SAYS WHY. What the plain set BREAKS
is concentrated in the test files of the four production modules that lost the most sites —
`task_runner.py`, `long_run_executor.py`, `verifier.py` and `dag_schedule.py` hold 31 of the
35 dropped production sites between them — and none of those TEST files holds a dropped site
itself. What the plain set FIXES sits mostly in test files that DO hold one. Dropping a site
in a production module breaks the tests of that module; dropping a site inside a test file
stops that test file from being wrongly rewritten. The full lists are in the instrument's own
output; the rows above are its largest, and the bucket sums it prints cover every row.

## 7. THE ATTRIBUTION, AND IT IS THE READING THE ROUND EXISTS FOR

    === 5. THE ATTRIBUTION, IN LOCATION FRAMES ===
      location frames parsed: R53 994   PLAIN 1128

      --- R53 ---
      UNDER-SELECTION, a classic field read left standing on a unified record: 0 frames over 0 kinds
      OVER-SELECTION on a NAMED class, which is what R-0880 reports: 59 frames over 6 kinds
             25  Artifact.job_id
             22  Mission.job_id
              5  BrainNode.task_id
              5  QueueEntry.job_id
              1  BrainNode.job_id
              1  _FakeJob.job_id
      the classes in the OVER-SELECTION bucket: ['Artifact', 'BrainNode', 'Mission', 'QueueEntry', '_FakeJob']
      every one of them is named by R-0880: True

      --- PLAIN ---
      UNDER-SELECTION, a classic field read left standing on a unified record: 231 frames over 2 kinds
            224  TaskEntry.id
              7  JobPlan.id
      OVER-SELECTION on a NAMED class, which is what R-0880 reports: 1 frames over 1 kinds
              1  _FakeJob.job_id
      the classes in the OVER-SELECTION bucket: ['_FakeJob']
      every one of them is named by R-0880: True

      THE TRADE, IN FRAMES: under-selection 0 -> 231 (+231), over-selection on a named class 59 -> 1 (-58), absent receiver 5 -> 5 (+0).

THE PLAIN RE-DERIVATION IS A COMPLETE FIX FOR `R-0880`'s OVER-SELECTION AND AN UNUSABLE INPUT
FOR THE FLIP, AND BOTH HALVES ARE MEASURED HERE. Every production record class `R-0880` names
— `Artifact`, `Mission`, `QueueEntry` and `BrainNode` — disappears from the residue under the
plain set, and what survives is one frame on `_FakeJob`, a test double. That is 59 frames
falling to 1. In the same run the under-selection class goes from NOTHING to 231 frames, all
of them a classic field read left standing on a record whose field the flip has already
renamed: `TaskEntry.id` at 224 and `JobPlan.id` at 7. The round 53 set has no such frame at
all.

THE UNIT MATTERS AND THIS PARAGRAPH STATES IT RATHER THAN LEAVING IT TO BE INFERRED, because
the last two rounds of this feature were spent on exactly that mistake. These are LOCATION
FRAMES of a `--tb=line` report. Finding `R-0880`'s own measurement counts `E <Exc>: <msg>`
lines, which is a DIFFERENT unit, and section 8 of `.agent/f275_t003_flip_residue_r59.md`
already recorded that the two readings do not agree to the unit even within one run. So the
counts above are not comparable figure-for-figure with the ones on `R-0880`'s record, and no
claim is made that they are. What IS comparable, and what the instrument checks
mechanically rather than by eye, is the SET OF CLASSES: every class in the over-selection
bucket of either arm is one `R-0880` names, at both ends.

    === 6. THE FILES WHOSE FRAME COUNT MOVED, IN FRAMES ===
           +133  packages/orchestration/dag_schedule.py                         holds a dropped site: True
            +68  packages/orchestration/task_runner.py                          holds a dropped site: True
            +23  packages/orchestration/verifier.py                             holds a dropped site: True
      CROSS-CHECK the per-file deltas against the change in the frame total: 134 against 134 frames  -> MATCH

The three files whose frame count grows most under the plain set are three of the production
modules that lost sites. The deltas sum to the change in the total, so no file's movement is
unaccounted for.

## 7a. What the checks in this document are worth, stated rather than assumed

    === 8. THE CHECKS THIS OUTPUT CARRIES, COUNTED ===
      CROSS-CHECKS run : 14   holding: 14   FAILING: 0
      PARTITIONS run   : 12   holding: 12   FAILING: 0
      EVERY CHECK HOLDS: True

A PARTITION adds a set's own parts back to the set. It cannot fail, it is printed so a reader
can add up, and it is not evidence that anything was verified. A CROSS-CHECK compares two
numbers reached by different routes — a node-id set against pytest's own tally line, a rule
table against the total the same tool printed beside it, a re-keyed set against the set it was
re-keyed from — and it can fail. The distinction is drawn here because an earlier edition of
this instrument printed only partitions, and a control that deleted one line from a transcript
left every one of them reading MATCH. The cross-checks above found a real defect before this
document was emitted: the rule table was being split at a two-space gap, which three of the
longest rule names do not have, so three rows worth 19 rewrites were silently dropped and only
the comparison against the transform's own printed total saw it.

## 8. What this settles

THE FLIP'S INPUT IS NEITHER OF THESE TWO SETS. The round 53 set over-selects and the plain
re-derivation under-selects, and this run measures both in the same pass over the same tree.
The set the flip needs is the round 53 set MINUS the sites the plain re-derivation identifies
as over-selected — a set strictly between the two — and the plain re-derivation is the first
mechanism this chain has found that locates those sites at all.

DECISION F275 D41's DEFERRAL IS DISCHARGED. It deferred this run on the ground that its
reading would be meaningless until the 54 were ruled; they were ruled by D42, the run has
been taken, and it has a result.

## 9. What this reading does NOT settle, stated as limits rather than as caveats

WHICH OF THE 60 DROPPED SITES ARE CORRECTLY DROPPED IS NOT ESTABLISHED HERE. The evidence
that SOME are is strong — 59 over-selection frames become 1 — but this run does not carry
each over-selected frame back to the ruled site that produced it, and until it does, the
partition of the 60 into "correctly dropped" and "wrongly dropped" is an inference rather
than a measurement. That cross-walk is the next round's work and it needs the transformed
tree's coordinates mapped back through the re-key, which is why it was not folded in here.

THE RESIDUE IS NOT EXHAUSTED AND NEITHER ARM IS CLOSE TO GREEN. 1227 bad nodes under the
better of the two arms is the number to keep in view: the classes section 7 of
`.agent/f275_t003_flip_residue_r59.md` named as unexplained by any rule this chain has
written — `SystemExit` at 337 frames, unchanged across both arms — are untouched by anything
measured here.

THE 31 AND 42 ERRORS ARE STILL NOT DIAGNOSED. They moved, by 11, and this round did not
attribute the movement. An undiagnosed class that moves is reported as undiagnosed, exactly
as round 59 reported it when it did not move.

NOTHING HERE TOUCHES THE id-SHAPE SEAM DECISION F275 D37 routed into T003's resolver collapse,
which is production work no round has started, and `R-0880` stays OPEN.
