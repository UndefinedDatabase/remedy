# F275 T003 — the flip's input set, CONSTRUCTED: the partition of the 60, and a third arm that is strictly better than the set the transform consumes today

> Measured by the reviewer at `ef75e213`, round 76's base and the commit all three arms of
> this comparison were taken at, in disposable `git worktree`s under the gitignored
> `.remedy-wt/`, all removed and pruned before this text was authored. THIS FILE RECORDS A DRY
> RUN; IT FLIPS NOTHING. No line under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/`
> moved in the round that wrote it. It replaces `.agent/f275_t003_flip_residue_r76.md` in no
> respect and extends it: the round 53 and PLAIN arms quoted below are that round's own runs,
> re-read from the same transcripts.
>
> PROVENANCE, AS A SHAPE AND NOT AS A RANGE. Every INDENTED line below is quoted verbatim from
> the output of the committed instrument `.agent/authored/f275-r77-instrument.py.md`, which is
> what this round's gate runs. Every maximal run of digits in the PROSE — that is, on every
> line that does NOT begin with whitespace — is one of exactly two kinds. Either it is A FIGURE
> THAT ALSO OCCURS as a digit run in that same output, or it is A CITATION: a digit run
> belonging to a feature id, a task slice id, a decision id, a finding id, a round number, a
> commit id or an artefact file name, or a figure this document quotes from a named decision in
> order to discuss it. There is no third kind, and NO FIGURE BELOW IS A REVIEWER READING taken
> outside the instrument. This clause is authoritative over the gate that checks it: where the
> two differ in wording, these words rule.

## 1. What DECISION F275 D50 left open, and in its own terms

D50 ruled that the flip's input is the round 53 set MINUS the sites the plain re-derivation
identifies as over-selected, and it was careful to call that an inference: its own section 9
says the partition of the 60 into correctly and wrongly dropped "is an inference rather than a
measurement" because nothing had carried an over-selected frame back to the ruled site that
produced it. This round takes that measurement, and then does the thing that turns a partition
into a decision — it builds the resulting set and runs it.

## 2. The partition, and the instrument that makes it does not need the frames at all

The route D50 imagined was to carry each over-selection frame back through the re-key into the
ruled set's coordinates. That route works — it was probed, and all thirteen distinct frames in
this repository resolve to a base line carrying a ruled site — but it is not the route taken,
because a better one was already on disk. THE SHIPPED OWNER CHECK ALREADY NAMES THE SITES. The
Rule H stage DECISION F275 D47 landed reads each ruled site's receiver against the live record
classes and reports the ones the code contradicts, by path, line, column and attribute, with no
suite run and no coordinate arithmetic anywhere.

    === 1. THE THREE RULED SITE SETS, IN SITES ===
      round 53 committed, re-keyed           : 2198 sites
      round 67 plain re-derivation, re-keyed : 2138 sites
      THE CORRECTED SET                      : 2185 sites
      the CORRECTED set is a SUBSET of round 53's : True
      the PLAIN set is a SUBSET of the CORRECTED one : True

The three sets nest, which is worth stating because it makes the comparison a line rather than
a triangle: the plain set is inside the corrected set is inside the round 53 set. How the
middle one was built is the rest of this section.

    === 2. THE PARTITION OF THE DROPPED SITES ===
      the SHIPPED owner check over the round 53 set: ruled 2198, decided 1921, refused 277, CONTRADICTED 13
      CROSS-CHECK the CONTRADICTED rows parsed against the count the stage prints: 13 against 13 sites  -> MATCH
      the receiver classes it names, in sites:
            9  Mission
            3  Artifact
            1  QueueEntry

      CONTRADICTED and dropped by the plain set : 13 sites
      CONTRADICTED but KEPT by the plain set     : 0 sites
      dropped but NOT contradicted               : 47 sites
      PARTITION the dropped sites, by whether the owner check contradicts them: 13 + 47 = 60 against 60 sites  -> MATCH
      EVERY SITE THE OWNER CHECK CONTRADICTS IS ONE THE PLAIN SET DROPS: True
      CROSS-CHECK the corrected set against the round 53 set minus the contradicted sites: 2185 against 2185 sites  -> MATCH

THIRTEEN AND FORTY-SEVEN, AND THE THIRTEEN ARE A SUBSET OF THE SIXTY WITH NOTHING LEFT OVER.
Every site the owner check contradicts is one the plain re-derivation drops, which is the
containment D50 inferred, now measured. The other 47 are the wrongly dropped ones: the plain
set was removing them for a reason that has nothing to do with the receiver's record, and they
are what cost round 76's plain arm its 231 under-selection frames.

## 3. The guard fires, and then it passes

    === 3. THE GUARD FIRES, AND THEN PASSES ===
      over the round 53 set   : CONTRADICTED 13
      over the CORRECTED set  : CONTRADICTED 0
      CROSS-CHECK the corrected run's contradicted count against zero: 0 against 0 sites  -> MATCH
      THE BLIND SPOT IS UNCHANGED AND IS STATED: refused 277 over the round 53 set and 277 over the corrected one — the corrected set removes what the check DECIDES against, never what it refuses to decide.

THE SAME GUARD, THE SAME COMMIT, TWO SETS, TWO ANSWERS. A guard seen only to pass is not
evidence and a guard that can only fail is the same defect from the other side; both readings
are here and they differ in the set alone. The refusal count does not move, and that is the
honest half: the corrected set removes the sites the check DECIDES are wrong, and the 277 it
declines to decide about are untouched. DECISION F275 D45 ruled that blind spot acceptable and
DECISION F275 D48, as corrected by D49, discharged its precondition on a witness measurement;
nothing here reopens either.

## 4. The third arm

    === 4. THE THREE TRANSFORM RUNS, IN REWRITES ===
      round 53   ruled  2198  files  263  total  6091  undecided  3084
      PLAIN      ruled  2138  files  263  total  6032  undecided  3143
      CORRECTED  ruled  2185  files  263  total  6078  undecided  3097

    === 5. THE THREE SUITE RUNS BESIDE THEIR CONTROL, IN TEST NODES ===
      CONTROL    failed     1   errors     0
      round 53   failed  1186   errors    42   CAUSED BY THE FLIP  1227
      PLAIN      failed  1331   errors    31   CAUSED BY THE FLIP  1361
      CORRECTED  failed  1174   errors    31   CAUSED BY THE FLIP  1204

All three arms run the same guarded transform of DECISION F275 D43 at `ef75e213` against the
same control, and differ in the ruled site set alone.

## 5. AND IT IS STRICTLY BETTER, WHICH IS A STRONGER STATEMENT THAN BEING SMALLER

    === 6. THE CORRECTED ARM AGAINST THE OTHER TWO, IN NODES ===
      CORRECTED against round 53 : FIXES   23 nodes, BREAKS    0 nodes, net   -23
      CORRECTED against PLAIN    : FIXES  174 nodes, BREAKS   17 nodes, net  -157

      the 23 nodes the corrected set fixes over the round 53 set, by test file:
             8  tests/orchestration/test_watchdog.py
             6  tests/orchestration/test_loop_run.py
             3  tests/cli/test_repair_request_cli.py
             2  tests/cli/test_repair_v1_cli.py
             2  tests/orchestration/test_mission_state.py
             2  tests/orchestration/test_queue_executor_binding.py
      PARTITION those nodes by file: 8 + 6 + 3 + 2 + 2 + 2 = 23 against 23 nodes  -> MATCH

BREAKS ZERO IS THE READING THAT MATTERS AND IT IS A SET DIFFERENCE, NOT A COUNT. Against the
set the transform consumes today the corrected set fixes 23 test nodes and breaks not one:
every node bad under the corrected arm is also bad under the round 53 arm. A smaller total
could hide a trade; an empty BREAKS set cannot. The six test files the 23 sit in are the tests
of the records the owner check named — the watchdog and loop-run and mission-state tests read a
`Mission`, the repair tests an `Artifact`, and the queue-executor binding a `QueueEntry`.

## 6. The attribution, across all three arms

    === 7. THE ATTRIBUTION ACROSS THE THREE ARMS, IN LOCATION FRAMES ===

      --- round 53 ---   location frames parsed: 994
      UNDER-SELECTION, a classic field read left on a unified record: 0 frames over 0 kinds
      OVER-SELECTION on a NAMED class, which is what R-0880 reports: 59 frames over 6 kinds
             25  Artifact.job_id
             22  Mission.job_id
              5  BrainNode.task_id
              5  QueueEntry.job_id
              1  BrainNode.job_id
              1  _FakeJob.job_id

      --- CORRECTED ---   location frames parsed: 969
      UNDER-SELECTION, a classic field read left on a unified record: 0 frames over 0 kinds
      OVER-SELECTION on a NAMED class, which is what R-0880 reports: 19 frames over 4 kinds
             12  Artifact.job_id
              5  BrainNode.task_id
              1  BrainNode.job_id
              1  _FakeJob.job_id

      THE TRADE, IN FRAMES. under-selection: round 53 0, PLAIN 231, CORRECTED 0. over-selection on a named class: round 53 59, PLAIN 1, CORRECTED 19.

`Mission.job_id` GOES FROM 22 FRAMES TO NONE AND `QueueEntry.job_id` FROM 5 TO NONE. Those two
classes are gone from the residue entirely. `Artifact.job_id` falls from 25 to 12, so the owner
check catches some of that class and not all of it, and `BrainNode` and the `_FakeJob` test
double do not move at all. That is the 277-site blind spot showing through, exactly where
DECISION F275 D45 said it would, and it is the residue the next round owns.

## 7. What this settles

THE FLIP HAS AN INPUT SET AND IT IS ON DISK. It is the round 53 re-keyed set minus the 13 sites
the shipped owner check contradicts, it passes that check at zero, and against the set the
transform consumes today it fixes 23 test nodes and breaks none. DECISION F275 D50's inference
is now a construction.

`R-0880` IS NOT RESOLVED BY THIS AND THE REASON IS THE 19. The finding's first obligation is
discharged twice over — statically by DECISION F275 D44's bound and behaviourally here — but
its second asks the transform to REFUSE a site whose owner verdict cannot be confirmed, and 19
over-selection frames survive the corrected set on classes the check does not decide. A finding
whose defect is still reachable is open.

## 8. What this reading does NOT settle

THE 19 SURVIVING OVER-SELECTION FRAMES ARE NOT ATTRIBUTED TO SITES. This round partitioned the
60 by the owner check's verdict, which is a property of the SET; it did not carry the 19 back to
the ruled sites that produced them, which is a property of the RUN and is the same cross-walk
D50 described. The probe that would do it was written and works, and it was not spent here
because the owner check answered the question this round asked without it.

WHETHER THE 47 ARE ALL CORRECT IS NOT ESTABLISHED. They are not contradicted by the owner check,
which is a weaker statement than being right: 277 sites are refused rather than confirmed, and a
site can sit in that refusal set and still be wrong.

THE RESIDUE IS NOT EXHAUSTED AND THE CORRECTED ARM IS NOT GREEN. 1204 bad nodes is the best
reading this chain has taken and it is not close to zero. The classes section 8 of
`.agent/f275_t003_flip_residue_r59.md` named as unexplained by any rule this chain has written
are untouched by anything measured here, and the errors stand at 31 under both the plain and the
corrected arms with no round having diagnosed them.

NOTHING HERE TOUCHES THE id-SHAPE SEAM DECISION F275 D37 routed into T003's resolver collapse,
which is production work no round has started, and no production line moved in the round that
recorded this.
