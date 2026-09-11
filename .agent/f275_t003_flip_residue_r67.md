# F275 T003 — the plain run recovers all 22, and the re-derived set has no unruled drop left

> Measured by the reviewer at `39647827`, this round's base, in one disposable `git
> worktree` under the gitignored `.remedy-wt/`, removed and pruned before this text was
> authored. THIS FILE RECORDS A RE-DERIVATION; IT FLIPS NOTHING. No line under `packages/`,
> `apps/`, `tests/`, `docs/` or `scripts/` moved in the round that wrote it.
>
> PROVENANCE, AS A LIST. Every figure in sections 2 through 6 is re-derived by the committed
> instrument `.agent/authored/f275-r67-plain.py.md`, which is what this round's gate runs.
> TWO readings are the reviewer's own and are not in that instrument's output: the two
> pytest summary lines of section 2, which live in the run logs rather than in the probe
> JSON, and the sha256 of the probe binary quoted in section 1. Nothing else in this
> document is a reviewer reading.

## 1. What this round spent, and what it did not change

DECISION F275 D40 ruled that pytest's assertion rewriting caused 22 of the 52 drops the
round 65 re-derivation made, and that `--assert=plain` was the route. This round spends it.
THE PROBE IS NOT MODIFIED: the file run here is byte-identical to the one committed at
round 65, sha256 `f06450611120e9c2…`, and the only change is that the pytest invocation
gains `--assert=plain`. That matters because a re-derivation that also changed the
instrument would be a two-variable comparison, which is the mistake round 65's own control
was added to catch.

## 2. The two plain runs

| Run | pytest summary | probe rows |
|---|---|---|
| 1 | `2 failed, 18408 passed, 29 skipped, 1 warning in 1259.73s (0:20:59)` | 2195 |
| 2 | `1 failed, 18415 passed, 23 skipped, 1 warning in 1279.75s (0:21:19)` | 2195 |

    as the ROUND 53 key: run1 2145  run2 2145  symmetric difference 0
    as the ROUND 65 key: run1 2195  run2 2195  symmetric difference 0

Set-equal under both keys, and at the same row counts as the rewritten runs. The two
summary lines are not gated on, for the reason `.agent/f275_t003_descriptor_sites.md`
already gives about a cold worktree and `apps/ui/node_modules`.

## 3. The synthetic names are gone, against a control that had them

    CONTROL, the rewritten run: 24 rows on 24 lines
    the PLAIN run             : 0 rows

TWENTY-FOUR TO ZERO. The control is the rewritten run's own figure rather than an assertion
that the number used to be higher, because a run that had none to begin with would prove
nothing by having none now.

## 4. What that cost, and what it bought

    rewritten: rows 2195  RESOLVED 2082  REFUSED 113
    plain    : rows 2195  RESOLVED 2058  REFUSED 137

    the lines the rewritten run resolved to a synthetic name, as the plain run sees them:
      REFUSED: 24
      resolved: 4

The plain run resolves 24 FEWER receivers and refuses 24 more, which is the whole of the
difference and is the direction DECISION F275 D40 predicted: a wrong name became an honest
absence. On the 24 lines that carried a synthetic name, the plain run refuses 24 rows and
resolves 4 — those four being other reads on the same lines whose receivers really are
bare names.

## 5. The rebuild, under the same control as round 65

    CONTROL: round 53 probe under the LINE join -> 2198   SET-EQUAL to round 53's R: True
    rewritten probe: LINE 2168  RECEIVER 2116  drops 52
    plain probe    : LINE 2168  RECEIVER 2138  drops 30
    the two LINE joins agree: True
    sites the PLAIN receiver join keeps that the REWRITTEN one dropped: 22
    sites the PLAIN receiver join drops that the REWRITTEN one kept: 0

THE TWO NUMBERS THAT MATTER ARE 22 AND 0. Twenty-two sites come back — exactly the count
DECISION F275 D40 attributed to the rewriting, arriving from the other direction — and NOT
ONE site is newly dropped, so the plain run is strictly better rather than differently
wrong. The LINE joins agreeing at 2168 is the control on that claim: the line join reads no
receiver at all, so it must not move when the receivers change, and it does not.

## 6. Is every drop justified?

    dropped total                                   : 30
    on one of the 39 at-risk lines D36 bounded      : 27
    the sweep recorded NO receiver for it at all    : 4
    both of the above                               : 3
    on a line still carrying a SYNTHETIC receiver   : 0
    NEITHER, so justified by nothing stated so far  : 2
      packages/orchestration/long_run_executor.py:505 col 30 .id  sweep receiver 'entry'
      tests/orchestration/test_repair_loop_v1.py:56 col 28 .id  sweep receiver 'art'

BOTH SURVIVORS WERE ALREADY RULED, BY DECISION F275 D40, ONE ROUND AGO. `:505` is the site
that reads `RULED False` against round 53's committed set and whose recorded column and
receiver both disagree with the source — D40 section three of the round 66 artefact ruled it
not a drop but a sweep defect. `test_repair_loop_v1.py:56` at column 28 is `art.id`, an
Artifact's id ruled only by sharing a line with `job.id` and `task.id`, which D40 ruled a
CORRECT drop. The third site D39 held the write shut on,
`tests/orchestration/test_loop_run.py:285`, is NOT in this list: it is one of the 22 the
plain run recovered, which is what D40 predicted for it by name.

SO THE PLAIN RE-DERIVED SET HAS NO UNRULED DROP. Every one of its 30 drops is either inside
the class DECISION F275 D36 bounded, or a site the sweep gave no receiver, or one of the two
DECISION F275 D40 already ruled.

## 7. What this settles, and what it does not

SETTLED: the route DECISION F275 D40 chose works and its predicted figure is met exactly.
The set re-derived from the plain run drops 30 rather than 52, recovers 22, drops nothing
new, and carries no drop that some decision has not ruled. The half of D40's condition that
named the rewriting is DISCHARGED.

NOT SETTLED, and it is the whole of what remains on that condition. THE 54 RULED KEYS THAT
RESOLVE TO NO `ast` NODE are untouched by this round: DECISION F275 D40 part three measured
them and nothing since has ruled them or asked whether the transform's own consumption
already loses them. The write stays shut on that alone. Beyond it, `R-0880`'s SECOND
obligation is still unbuilt, the flip's dry run has not been re-run against any re-derived
set, and the id-SHAPE seam DECISION F275 D37 routed into T003 is still production work no
round has started.
