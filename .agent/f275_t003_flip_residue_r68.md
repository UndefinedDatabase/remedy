# F275 T003 — the transform does NOT lose the 54, and DECISION F275 D40 part three named the wrong mechanism

> Measured by the reviewer at `1f48b99a`, this round's base, with two disposable `git
> worktree`s under the gitignored `.remedy-wt/` that the instrument itself creates, uses and
> removes; `git worktree list` and `git status --porcelain` are read back at the end of its
> own output. THIS FILE RECORDS A MEASUREMENT; IT FLIPS NOTHING. No line under `packages/`,
> `apps/`, `tests/`, `docs/` or `scripts/` moved in the round that wrote it.
>
> PROVENANCE, AS A LIST. Every figure in sections 2 through 7 is re-derived by the committed
> instrument `.agent/authored/f275-r68-instrument.py.md`, which is what this round's gate
> runs, and every indented block below is a verbatim excerpt of that instrument's output.
> NOTHING in this document is a reviewer reading taken outside it. The two commits it names,
> `a25fef5d` and `1f48b99a`, are arguments the gate passes in rather than values the
> instrument chooses.

## 1. The question, and why it was the last one open

DECISION F275 D41 shut the flip's write on one condition: rule the 54 ruled keys that
resolve to no `ast` node at their recorded position, and ANSWER FIRST whether the
transform's own consumption already loses them. That ordering is the whole of the question.
If the transform loses them, every dry run this chain has taken silently edited 54 fewer
sites than it reported, and the residue readings of rounds 58 through 67 are all measured
against an under-selection. If it does not, the 54 are a stale artefact on disk and nothing
more.

THE ANSWER IS NO. The transform does not lose them, because it does not consume the set the
54 were measured over. What follows is that answer in the order it has to be read: the set
those keys belong to, the commit at which it was exact, the set the transform actually
consumes, and finally the two transform runs that settle it by behaviour rather than by
reading source.

## 2. The round 53 committed set was exact when it was written

    at the sweep commit a25fef5d: resolve 2198  do NOT resolve 0
    at the tip 1f48b99a         : resolve 2144  do NOT resolve 54
         21  packages/orchestration/long_run_executor.py
         12  packages/orchestration/task_runner.py
         11  packages/orchestration/agent_loop.py
          7  packages/orchestration/dag_schedule.py
          3  packages/orchestration/verifier.py

TWO THOUSAND ONE HUNDRED AND NINETY-EIGHT OF 2198 RESOLVE AT THE COMMIT THAT LANDED THE
SET. That is the control this reading needed and did not have before: a set that failed at
both commits would be a sweep defect, and a set that is perfect at one and short at the
other is a set that went stale. The five files are the same five, at the same counts, that
finding `R-0879` recorded when it was registered.

    commits that moved those files between the two:
        5d9d80d6 F275 R57 C8: retype AgentLoopState.job_id to str.
        816eb6c4 F275 R57 C7: retype TaskNode.task_id to str, with the module signatures it threads.
        c82092d0 F275 R57 C6: retype RunTaskResult.task_id to str and make its short-id read shape-agnostic.
        a1858c30 F275 R57 C5: retype TaskAttempt.task_id to str, with the ids it threads.
        b72b9fe1 F275 R57 C4: retype VerificationResult.task_id to str.

Every commit that touched those five files between the two is a round 57 retype commit, and
round 57 is this branch's own. Nothing outside this feature moved them.

## 3. The shape is one line, in one direction, with the receiver intact

    54  node line - recorded line = -1
    the sweep's recorded receiver agrees at the shifted node: 53   disagrees: 1
    shifted node is ITSELF a round 53 ruled key             : 0
    every one of the 54 is in the static sweep's own `sites`: True

ALL 54 ARE OFF BY EXACTLY ONE LINE AND NOT ONE COLUMN. The column and the attribute are
right in every case and the receiver the static sweep recorded still matches the receiver at
the shifted node in 53 of the 54, which is what fixes these as the SAME sites one line
earlier rather than as 54 different reads. That a run of deletions above them moved them by
one line each is exactly what round 57 did.

The third line is the one that would have mattered had the answer gone the other way: NOT
ONE of the 54 shifted nodes is itself a key of the round 53 set, so under that set the
transform would reach none of them by another route.

## 4. The transform consumes a different set, and that set is whole

    round 61 set at the tip: resolve 2198  do NOT resolve 0
    53-only keys 54   61-only keys 54   shared 2144
    every 53-only key's one-line-earlier node is in the 61 set: True
    owner verdicts disagreeing on the 2143 shared owner keys: 0

THIS IS THE ANSWER. The set the transform has consumed since round 61 is
`.remedy-wt/r61_ruled.json`, the OUTPUT of the re-key stage `.remedy-wt/r59_rekey.py` that
DECISION F275 D34 part two ordered as the fix for `R-0879`, and it resolves 2198 of 2198 at
the tip with nothing short. The two sets differ by exactly 54 keys on each side, the 54 that
the round 53 set holds one line late are precisely the 54 the round 61 set holds at the
right line, and the owner verdict is identical on every key the two share. The re-key stage
did its work three rounds before D41 asked whether it had.

## 5. The behavioural pair, which is what settles it

Reading the transform's source establishes that its P1 branch keys by the node it is
standing on, so a key at a position no node occupies can never be produced. That is a
property of the code. What it COSTS is a property of the run, so both runs were taken: the
same transform, at the same commit, in two fresh worktrees, differing in the ruled set alone.

    TREATMENT, round 61 set    T2 1786  T3 411  total 6091  undecided 3084  exit 0
    CONTROL,   round 53 set    T2 1759  T3 384  total 6037  undecided 3138  exit 0
    difference                 T2 +27  T3 +27  total +54  undecided -54

FIFTY-FOUR RENAMES, TWENTY-SEVEN JOB AND TWENTY-SEVEN TASK, AND FIFTY-FOUR FEWER UNDECIDED
SITES. The control is the round 53 set run through the live transform, which is the run
DECISION F275 D41 feared; it is 54 renames short, and the treatment is not. One variable
separates the two runs and the difference is the size of the set difference exactly.

## 6. The 54 renames land where the 54 keys say and nowhere else

      9 differing lines  packages/orchestration/agent_loop.py   (11 fixed keys)
      7 differing lines  packages/orchestration/dag_schedule.py   (7 fixed keys)
     18 differing lines  packages/orchestration/long_run_executor.py   (21 fixed keys)
     12 differing lines  packages/orchestration/task_runner.py   (12 fixed keys)
      3 differing lines  packages/orchestration/verifier.py   (3 fixed keys)
    files compared 994   files differing 5   differing lines 49
    differing lines NOT within 2 lines of a fixed key: 0

FIVE FILES OUT OF 994, AND ZERO UNEXPLAINED LINES. Fifty-four keys over forty-nine lines,
because some lines carry more than one ruled read — `agent_loop.py` holds three `.name`
reads on one line — and the two transformed trees are byte-identical everywhere else. A
count that differed by 54 would not on its own have shown that the 54 are the difference;
this does.

    packages/orchestration/agent_loop.py:137  treatment 'job_id=job.job_id,'
                                               control   'job_id=job.id,'

ONE CAVEAT, REPORTED AND NOT SMOOTHED. The `long_run_executor.py:504` treatment line reads
`entry_id=entry.job_id, job_id=str(queued_job.job_id))`, and `entry` is a `QueueEntry`
rather than a job record, so the first of those two renames is wrong. That is finding
`R-0880`'s over-selection class, which names `QueueEntry.job_id` among its measured
instances, and it is the OTHER open defect of this same set. It is noted here because the
pair run surfaced it; no new id is minted for it.

## 7. What DECISION F275 D40 part three said, and what the source says

    at a25fef5d:
        504:           entry_id=entry.id, job_id=str(queued_job.id))
        node line 504 col 19 .id  receiver 'entry'
        node line 504 col 40 .id  receiver 'queued_job'
        round 53 keys there: [(504, 19, 'id'), (504, 40, 'id'), (506, 32, 'id')]

D40 part three read `long_run_executor.py:504` as TWO SITES AT COLUMNS 19 AND 40 OVER ONE
NODE AT COLUMN 30, and concluded from it that the sweep's own columns were wrong. At the
commit the sweep ran on, line 504 carries exactly two `.id` nodes, at columns 19 and 40,
with receivers `entry` and `queued_job` — and the round 53 set records exactly those two.
The sweep was right. The node at column 30 belongs to the NEXT statement, and it is at line
504 only at the tip, where that source line has become 503.

    at 1f48b99a:
        503:           entry_id=entry.id, job_id=str(queued_job.id))
        node line 504 col 30 .id  receiver 'entry'
        round 53 keys there: [(502, 35, 'id'), (504, 19, 'id'), (504, 40, 'id')]

At the tip that same source line is 503, a node at column 30 stands at line 504, and the
round 53 keys that fall in the window have scattered across three source lines. The round 61
keys read the same at both blocks of the instrument's output, because they are expressed at
the tip in both.

SO D40 PART THREE COMPARED THE ROUND 53 KEYS AGAINST THE TIP'S SOURCE AND ATTRIBUTED THE
MISMATCH TO THE INSTRUMENT THAT PRODUCED THE KEYS. It is the same class it was diagnosing —
a position read against the wrong tree — one level up, and it minted a second explanation
for a defect the record already held under `R-0879` with the identical five-file breakdown.

## 8. What this settles, and what it does not

SETTLED, and this is the whole of DECISION F275 D41's remaining condition. The transform's
consumption does NOT lose the 54: it consumes the re-keyed set, which is whole at the tip,
and the paired run shows the cost of the stale set as exactly the 54 renames the stale set
cannot reach. The 54 are a STALE ARTEFACT on disk — `.agent/f275_t003_descriptor_sites.md`,
whose committed set is correct only at `a25fef5d` — and they are `R-0879`, already open,
already measured, and already fixed in the pipeline by the stage D34 part two ordered. NO
NEW FINDING ID IS MINTED, per item 30 of `docs/agents/planner_reviewer_prompt.md` §3.

NOT SETTLED. `R-0879` stays OPEN and should: the re-key stage lives in scratch and the
COMMITTED artefact still carries the stale set, so a reader who takes the set from disk
rather than from the pipeline gets the short one. `R-0880`'s two obligations are both still
unbuilt, and section 6 above surfaced one more instance of its class. The id-SHAPE seam
DECISION F275 D37 routed into T003's resolver collapse is production work no round has
started, and the flip's dry run has still not been re-run against the plain re-derived set
of round 67.
