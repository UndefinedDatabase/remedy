# F275 T003 — the owner check's residual, measured by WITNESS, and DECISION F275 D47 corrected

> Measured by the reviewer at `0d47205d`, this round's base. The coverage reading runs in the
> PRIMARY CHECKOUT and writes no tracked file; the mutations run in a disposable `git worktree`
> under the gitignored `.remedy-wt/` that the instrument itself creates and removes. Its last
> banner reads `git worktree list` and `git status --porcelain` back afterwards.
> THIS FILE RECORDS A MEASUREMENT; IT FLIPS NOTHING. No line under `packages/`, `apps/`,
> `tests/`, `docs/` or `scripts/` moved in the round that wrote it.
>
> PROVENANCE, STATED AS A SHAPE. EVERY INDENTED LINE IN THIS FILE is a verbatim excerpt of the
> output of the committed instrument `.agent/authored/f275-r74-witness.py.md`, which is what
> this round's gate runs. Every figure in the PROSE that the instrument does not print is one
> of exactly two kinds, and each names its own source in the sentence that uses it: a CITATION
> of a named decision, finding, round, section, commit or source line; or a READING THE
> REVIEWER TOOK OUTSIDE THIS INSTRUMENT — the re-run of round 73's own instrument, and a
> discarded draft of this one — which is named as such where it is used. This clause was
> checked by running this round's figure sweep against it before emission, and one figure in it
> resolves against the instrument only by coincidence: the `23` of "23 UNEXECUTED" below is
> round 73's re-run, and the instrument separately prints `23 skipped`.
> NO LINE CARRYING A WALL-CLOCK DURATION IS QUOTED ANYWHERE IN THIS FILE, because such a line
> cannot reproduce in any run — one of the three defects that made round 73 a FAIL.

## 1. What round 73 got wrong

ROUND 73 ASKED WHETHER THE SITES THE OWNER CHECK REFUSES ARE EXECUTED BY THE SUITE, ran the
suite inside a fresh `git worktree`, read 176 of 176 executed with an empty risk set, and
DECISION F275 D47 discharged DECISION F275 D45's precondition on that reading. Re-run by the
reviewer at this round's base, the same instrument in the same kind of worktree read 23
UNEXECUTED and 126 control failures. A worktree carries no `apps/ui/node_modules` and no built
dist, so the `ui_server` suite fails there and never reaches the `ui_server` lines; round 73's
worktree happened to have been warmed by an earlier invocation and the next one was not.

A MEASUREMENT THAT MOVES WITH THE WEATHER CANNOT DISCHARGE A PRECONDITION. That is the
substance of the round 73 FAIL, and this round is its repair. Two further defects of the same
round are recorded in `.agent/prose_slips.md` and are not restated here.

## 2. The guard this file is about, out of its own committed carrier

          carrier 78e5c18c:.agent/authored/f275-r73-owner-stage.py.md
          extracted 24253 bytes  sha256 7be3437450d1f183d241e8a5161a6ae182652d0aecd674ea10e8f870407eddb8
          REFUSED, the stated blind spot: 277
          refused sites                                    : 277
          of them, in test files                           : 102
          of them, in production files                     : 175
          distinct production files                        : 29

THE SHIPPED GUARD IS THE RULE H STAGE ROUND 73 LANDED, and the instrument derives its refusal
set by running that stage out of its own committed carrier rather than by reading a map an
earlier round left in scratch. A draft of this instrument read round 72's map instead, whose
refusal set of 324 is a SUPERSET of Rule H's — conservative, and therefore not wrong, but it
measures a guard that is no longer in use, and a document about the shipped guard should name
the shipped guard's own set.

## 3. The suite, where it actually runs

          THE BIAS OF A FAILING TEST RUNS THE SAFE WAY, which is why no colour is
          THE TREE IS UNTOUCHED BY THIS RUN, which is what makes it legal here:
          git status --porcelain -> ''

NO COUNT FROM THAT RUN IS QUOTED HERE AND THAT IS DELIBERATE. Its pass, fail and skip numbers
move between invocations with the environment-sensitive tests named below, so quoting one
would make this document unreproducible in exactly the way round 73's was. The instrument
prints them in full; what this file takes from the run are the two lines above, which do not
move, and the witness counts of the sections that follow, which are properties of the coverage
data rather than of the run's colour.

THE COVERAGE READING MOVES TO THE PRIMARY CHECKOUT. That is not a guardrail violation:
`docs/agents/self_drive_protocol.md` G5 isolates DESTRUCTIVE verification, and a coverage run
writes no tracked file — `.coverage` is gitignored, and the instrument reports
`git status --porcelain` afterwards to show it. The MUTATIONS of section 6 still happen only
inside a disposable worktree, which is what G5 is about.

AND THIS RUN'S COLOUR IS NOT A READING OF THE GATE, which is the other half of the repair.
Several tests here are environment-sensitive under coverage on a parallel runner: a wall-clock
perf budget and a workspace-identity pair have each been observed red in one invocation and
green in the next, and passing in isolation. A gate demanding this run be green fails at
random — the gate that cannot reliably pass, which is what round 73's G6(b) was and why it
went red on a worker who had done nothing wrong. No colour is needed, because a failing test
can only execute FEWER lines than it otherwise would, so it can only UNDERSTATE a site's
witness count, which makes the sets below too large rather than too small.

## 4. How many tests witness each refused site

          witnessed by zero         :     0
          witnessed by one          :    11
          witnessed by two to nine  :    58
          witnessed by ten or more  :    97
          median witnesses per site                        : 17
          total (site, test) witness pairs                 : 6966

"IS THE LINE EXECUTED" IS THE WEAK VERSION OF THE QUESTION, and round 73 could only say so as
an unquantified caveat after spot-checking two sites. One test reaching a site and forty tests
reaching it are not the same protection. Coverage records WHICH test executed each line, so
this asks how many distinct tests witness each refused site, for every site at once. The
answer is a distribution rather than a yes: the median site has seventeen witnesses, and the
whole residual is held up by 6966 site-and-test pairs.

## 5. The risk set

          the risk set holds                               : 0

NO REFUSED PRODUCTION SITE IS WITNESSED BY NOTHING. This is the same conclusion round 73
reached and it is now reached by a reading that reproduces, in the checkout where the suite
runs, under a measurement whose bias is stated and runs the safe way.

## 6. The thin set, and every one of it red-proved

          the thin set holds                               : 11

ELEVEN SITES ARE HELD BY EXACTLY ONE TEST EACH, and those are the real exposure: not because
they are unguarded, but because they are one test deletion from unguarded. Round 73 named that
risk as a limitation it could not measure. Here each of the eleven is RED-PROVED individually
— its single witness run unmutated in a worktree, then run again with the flip's own rename
applied to that exact site — and all eleven witnesses really catch it, every control green and
every mutation red, with each file reverted byte-identically.

          packages/orchestration/verifier.py:209 col 75 .id
            witness            : tests/test_verifier.py::test_verify_fails_when_artifact_task_id_does_not_match
            unmutated control  : exit 0 ; passed 1, failed 0, skipped 0
            against the rename : exit 1 ; passed 0, failed 1, skipped 0
            control green and mutation red: True ; reverted byte-identically: True
          thin sites whose single witness really catches the rename: 11 of 11

THAT SITE IS QUOTED BECAUSE IT IS THE ONE THE PROBE GOT WRONG FIRST. A draft of this
instrument mutated by replacing the first textual `.id` on the ruled line. At
`packages/orchestration/verifier.py` that text sits inside an f-string's LITERAL, so the
replace edited a message rather than an attribute access, the witness stayed green, and the
site read as the one unguarded member of the thin set. The flip renames an ATTRIBUTE NODE, so
the probe now mutates exactly that node, located by the line, the byte column and the
attribute name the ruled set already records. The reading went from 10 of 11 to 11 of 11, and
the 10 was the instrument's defect rather than the repository's.

## 7. What this settles, and what DECISION F275 D48 rules

SETTLED. The residual the owner check refuses is 277 sites, of which 102 are in test files that
break themselves and 175 are production lines. Every one of the 175 is witnessed by at least
one test; the median is seventeen; eleven are witnessed by exactly one, and each of those
eleven witnesses is demonstrated to catch the rename rather than assumed to. This is the
reading D47 needed and did not have.

NOT SETTLED. `R-0880` STAYS OPEN: the guard is still silent on 277 sites under Rule H, and a
residual that the suite catches is not a residual that the guard decides. The eleven thin sites
are carried into DECISION F275 D48 as a named obligation on the flip round rather than as a
caveat, because a witness set of one is a fact about today's suite and not a property of the
code. And nothing here touches the id-SHAPE seam DECISION F275 D37 routed into T003's resolver
collapse, which is production work no round has started.
