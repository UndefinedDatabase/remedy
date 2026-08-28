# F037 R12 — the parse ceiling, repairing R-0721

## Goal

Give the parser a bound it enforces itself, and make the contract's `truncated`
flag mean something F037 actually decides rather than something an upstream
producer once wrote into an artifact.

`R-0721` is registered OPEN against exactly this: `parse_unified_diff_to_view`
appends one dict per body line with no ceiling, `build_diff_view` copies the
result onto an envelope the endpoint serialises whole, and the only thing that
ever sets `truncated` True today is the `[DIFF TRUNCATED]` sentinel some other
producer emitted. This round closes the parser half. The endpoint half — the
artifact is read whole into memory before the parser ever sees it — is R13.

## Base

Base commit `f676f41981d83613ab4b216b75e372151881bd83`, branch
`feature/f037-rendered-diff-viewer`. This is the SHA of the R11 handback this
round starts from; every range reading below is against it.

## Bundle — seven commits

| Commit | Subject | Paths |
|--------|---------|-------|
| C0a | docs(agent): save the F037 R12 step block | `.agent/authored/f037-r12.md` |
| C0b | docs(agent): mirror the F037 R12 block into last_block | `.agent/last_block.md` |
| C1 | docs(agent): point the plan at the F037 R12 ceiling round | `.agent/plan.md` |
| C2 | docs(agent): book the R11 gate verdict and the timing slip | `.agent/live_review.md`, `.agent/prose_slips.md` |
| C3 | feat(orchestration): bound the parsed diff with DECISION F037 D5 | `.agent/decisions.md`, `packages/orchestration/diff_parser.py` |
| C4 | test(orchestration): pin the parse ceiling and its exact boundary | `tests/orchestration/test_diff_parser.py` |
| C5 | docs(agent): resolve R-0721 | `.agent/live_review.md` |
| C6 | docs(agent): hand back F037 R12 | `.agent/handoff.md` |

## Exact change set

Nothing outside these eight paths is written, created or deleted:

    .agent/authored/f037-r12.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    .agent/decisions.md
    packages/orchestration/diff_parser.py
    tests/orchestration/test_diff_parser.py
    .agent/handoff.md

Plus the push of `feature/f037-rendered-diff-viewer` after C6, which is ordered
explicitly here and sits outside every gate below.

## Constraints

1. A slice between its marker lines is applied BYTE FOR BYTE and is never edited,
   retyped, reflowed or trimmed — not to make a numeral in this block come true,
   and not to satisfy a cap. A slice's text already carries exactly one trailing
   newline. If a slice and a gate disagree, apply the slice, report the
   measurement, and declare the contradiction under Deviations.
2. Production code is DESCRIBED by the SPEC below, never sliced. The worker writes
   that code itself, in the idiom of the file it is editing, and reads the whole
   file before touching it.
3. `packages/orchestration/diff_view_source.py` IS NOT TOUCHED. Its unbounded
   `read_text` is the OTHER half of `R-0721` and belongs to R13; changing it here
   would leave this round's red-proofs unable to say which half they proved.
   `packages/orchestration/ui_server.py` is not touched either.
4. `docs/`, `docs/roadmap/` and `apps/` are NOT touched. No `.ts`, `.tsx` or React
   code is written: the frontend test runner is refused in this environment and
   code neither role can execute must not be certified.
5. NO EXISTING TEST IS WEAKENED, DELETED, RENAMED OR REORDERED, and no existing
   fixture constant, helper or import changes. In particular the four tests R11
   added stay exactly as they are: they are this round's regression guard, and the
   ceiling is chosen so that all four still pass untouched. C4 ADDS.
6. `.agent/live_review.md` is append-only. Nothing already in it is edited,
   renumbered or deleted. No id is registered this round; exactly `R-0721` is
   resolved.
7. No PR is created and nothing is merged. The Open PR Gate is READ and reported.
8. Every destructive check runs inside a disposable `git worktree` under
   `.remedy-wt/`, never in the primary checkout, and the worktree is removed and
   pruned afterwards.
9. THE CEILING MUST NOT BITE ON THE FIXTURE ACCEPTANCE NAMES. `T5_F037.md`
   requires a 10k-line fixture to render within budget; a bound that truncated it
   would satisfy this block and break the feature. The value in SPEC S1 is twice
   that fixture for exactly this reason, and G6 mutation (d) is the proof.

## SPEC — C3, the bound in `packages/orchestration/diff_parser.py`

Read the whole module first. It is 652 lines at the base and it is PURE and TOTAL
by contract: it touches no filesystem and never raises. Both properties survive
this change.

**S1 — the constant.** Add ONE module-level constant beside the existing tuning
constant `DIFF_INTRALINE_MIN_RATIO`, in the same `#:` comment idiom the file uses
for every other constant, named `DIFF_VIEW_MAX_BODY_LINES`, with the value
`20_000`. Its comment names DECISION F037 D5 and states in one sentence that the
value is twice the 10,000-line fixture the feature file's Acceptance names, so
that fixture renders in full.

**S2 — the counter.** Add ONE local counter beside the existing `truncated = False`
initialisation in `parse_unified_diff_to_view`, counting body lines appended
ACROSS THE WHOLE DIFF rather than per file or per hunk. The total is what the
payload costs, and a per-file ceiling would leave a diff of many small files
unbounded — which is the case G6 mutation (c) exercises.

**S3 — the guard.** In the hunk-body branch, at the point where a classified line
is about to be appended, refuse the append once the counter has REACHED the
ceiling: set `truncated` True and stop walking the input. Increment the counter
once per appended line. The boundary is INCLUSIVE of the ceiling — a diff of
exactly `DIFF_VIEW_MAX_BODY_LINES` body lines parses in full and is NOT marked
truncated; the flag and the stop appear only for input that exceeds it.

**S4 — the WHY comment.** The guard carries the one-line WHY comment this
repository's discoverability conventions put directly above a definition, and it
states what the reader most needs: the flag is the contract's own field, the stop
is deliberate rather than an error, and the last file in a truncated view may hold
a partial hunk or none at all.

**S5 — the deliberate absence, documented where a reader would search for it.**
State in the module — in the guard's comment or the constant's — that Remedy
deliberately does NOT bound the artifact READ here, because this module touches no
filesystem, and name `diff_view_source.py` as where that bound belongs. Text
search cannot find code that does not exist, and the next reader will look here
first.

**S6 — nothing else changes.** No existing function signature, docstring,
constant, regex or branch is altered. `parse_unified_diff_to_view` still never
raises and still returns the empty-files shape for empty input, non-diff text and
a non-string argument.

## SPEC — C4, the tests in `tests/orchestration/test_diff_parser.py`

Add a new section at the END of the file, in the same banner-comment idiom, using
the `_generated_huge_single_file_diff` and `_generated_many_file_diff` builders
R11 already added. Import `DIFF_VIEW_MAX_BODY_LINES` by adding it to the existing
import block in alphabetical order. Every size below is expressed in terms of that
constant, never as a transcribed literal, so the tests follow the ceiling if it is
ever re-decided.

**S7 — above the ceiling, the bound bites.** A diff generated well above the
ceiling parses to exactly `DIFF_VIEW_MAX_BODY_LINES` body lines in total across
all files, and `truncated` is True.

**S8 — the exact boundary, both sides.** A diff of exactly
`DIFF_VIEW_MAX_BODY_LINES` body lines parses in FULL with `truncated` False, and a
diff of exactly two more parses to exactly the ceiling with `truncated` True. Both
halves in the assertions, because an off-by-one in the comparison moves the
boundary by one and only a test that pins both sides can see it.

**S9 — the many-files dimension is bounded by the same counter.** A diff of
several thousand one-line files, whose TOTAL body lines exceed the ceiling, is
truncated at the same total. This is the case a per-file ceiling would miss.

**S10 — the Acceptance fixture is NOT truncated.** The 10,000-line fixture R11
added parses in full with `truncated` False, asserted against
`HUGE_DIFF_BODY_LINE_COUNT` and `DIFF_VIEW_MAX_BODY_LINES` rather than against
literals, together with the relationship the two constants must keep — the ceiling
is strictly greater than the fixture. This is constraint 9 written as a test.

**S11 — stats stay honest under truncation.** For the truncated view, each file's
`stats` still equal a recount of that file's OWN parsed lines, the way
`test_every_file_stats_equal_a_recount_of_its_own_parsed_lines` asserts it for the
untruncated corpus. A bound that left stats describing lines that are not in the
payload would be worse than no bound.

**S12 — the docstrings say what the truncated view IS.** At least one of the new
tests states in its docstring that the last file of a truncated view may carry a
partial hunk or an empty one, so a reader meeting that shape does not file it as a
defect.

## Slices

<<<SLICE PLANF037R12
# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495`, the
merge commit of pull request #217 which closed F032.
`.agent/decisions.md` carries the DECISION series, F037 D1 through D5.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the design amendments A1 through A4.

## Current Step
R12 repairs `R-0721`: the parser bounds its own output at
`DIFF_VIEW_MAX_BODY_LINES` and sets the contract's `truncated` flag when the bound
bites, so that flag becomes something F037 decides rather than only a relay of an
upstream sentinel. The ceiling is twice the 10k fixture Acceptance names, so that
fixture still renders in full. DECISION F037 D5 records the value and how to
reverse it.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R11 verdict and the timing slip | ordered | record first |
| C3 DECISION F037 D5 and the ceiling | ordered | the choice beside what it governs |
| C4 the boundary tests | ordered | both sides of the ceiling, or an off-by-one hides |
| C5 the resolution | ordered | written after the repair is proved |
| C6 the handback | ordered | |

## Next Steps
1. R13 carries the other half of `R-0721`: `diff_view_source.py` reads the whole
   artifact with `read_text` before the parser ever sees it, so the input is
   still unbounded even once the output is not.
2. T002's rendering core and all of T003 stay BLOCKED. `npx vitest`, the `npm`
   script and the direct binary were each refused again while planning R10, for
   the reviewer, as they were for both roles at R8.

## Risks
- A ceiling is a behaviour change on a shipped read path. The four tests R11 added
  are the regression guard and constraint 5 forbids touching them; if one of them
  moves, the ceiling was chosen wrong rather than the test being stale.
- The binding CSS defines no intraline treatment while Acceptance requires
  intraline emphasis. Inventing a colour early would breach the feature file's
  own banner, so it stays a question for the round that renders spans.
<<<END PLANF037R12

<<<SLICE GATER11
Gate: F037 R11 — the corpus round that closed T001's last named shape and recorded Acceptance's perf figure. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran all of them itself at `f676f419`. TRANSPORT IS PROVED FROM A VALUE THE REVIEWER HELD BEFORE DELEGATING: the block was written to the gitignored scratch `.remedy-wt/f037-r11-block.md` and measured there at sha256 `d44846216a9cf57accbb7575308622452d020fe1244838c50ad4b59ac9b1a242` over 26435 bytes and 326 lines, and the committed `.agent/authored/f037-r11.md` is byte-identical to that original, with the saved copy and `.agent/last_block.md` ONE git blob `9cf846287e22e52a6596f23d92b5630a07712626`. EXTRACTION REPRODUCES: 3 slices at 46, 1 and 1 content lines, CONTENT 48 against TOTAL 326, PROSE 278, both caps holding. THE PLAN IS BYTE-EQUAL to PLANF037R11 with the trailing-newline control `False`, at 46 lines. BOTH APPENDS ARE PROVED BY BYTE IDENTITY re-read from disk with the negative control `False`, and the pre-round blob is a byte PREFIX of the result. THE RECORD MOVED AS ORDERED AND ONLY AS ORDERED: `^- R-\d+ — ` 281 to 282, `^Done: R-\d+ — ` unmoved at 29, `^Landed: R-` unmoved at 1, `^Gate: F\d+ R\d+ — ` 80 to 81, the single id added being `R-0721`, NOTHING resolved as constraint 6 required, every id distinct, and the open set 252 to 253. CONSTRAINT 3 IS PROVED RATHER THAN ASSERTED: the restricted `git diff --stat` over `packages/` between the base and C3 is EMPTY, so the parser this round pins was not touched while being pinned. THE SUITES AND THE LINT ARE GREEN AT REAL EXIT CODES RE-RUN BY THE REVIEWER: `python3 -m pytest tests/orchestration/test_diff_parser.py tests/orchestration/test_diff_view_source.py -q` exit 0 at `41 passed`, `python3 -m ruff check tests/orchestration/test_diff_parser.py` exit 0 at `All checks passed!`, and the canary exit 0 at `42 passed`, matching the base figure. BOTH RED-PROOFS REPRODUCE EXACTLY, run by the reviewer in a disposable worktree at the C3 tree with `__pycache__` purged and `python3 -B` used and each restore verified byte-identical: unmutated control exit 0 at `32 passed`; a cap of 100 parsed body lines is exit 1 at `3 failed, 29 passed`, killing all three of the huge-file tests; and a cap of 10 file regions is exit 1 at `1 failed, 31 passed`, killing the many-files test. THE DISCRIMINATOR IS THE POINT AND IT HOLDS: the reviewer measured both mutations against the corpus AS IT STOOD AT THE BASE and both came back exit 0 at `28 passed`, so neither is visible to the twenty-eight tests that existed before this round — C3's four tests are the only thing that can see a silent truncation, which is precisely what `R-0721` says the corpus was blind to. THE REVIEWER ADDED A VACUOUSNESS CONTROL THE BLOCK DID NOT ORDER, because a timing assertion is the easiest thing in a suite to satisfy by doing nothing: making the parser return the empty shape immediately is exit 1 at `29 failed, 3 passed`, and the budget test is among the failures — it pins the parsed-line count before it looks at the clock, so it cannot be met by parsing nothing. THE TIMING ASSERTION IS NOT FLAKY AND THE REVIEWER MEASURED THAT RATHER THAN TRUSTING IT: twenty consecutive parses of the committed fixture ran from 0.0998 s to 0.1052 s, so the 0.5 s ceiling holds 4.8 times the WORST sample, which clears the block's own constraint 9 requirement of surviving a three-times-slower runner. THE ROUND'S TWO SUBSTANTIVE DEVIATIONS ARE BOTH CORRECT AND THE SECOND IS THE REVIEWER'S ERROR, NOT THE WORKER'S. First, the worker set the ceiling at five times the measurement rather than the "roughly an order of magnitude" SPEC S5 asked for, because ten times would land at 1.0 s, which is exactly where the quadratic case lands — a ten-times ceiling would have passed both the linear and the quadratic parser and recorded nothing. That is the SPEC's purpose clause defeating its own adjective, the worker read the purpose, chose the value that separates the two cases, and wrote both figures into the docstring. Second, the worker could not reproduce the 0.363 s figure FIND0721 states and measured 0.105 s. The worker is right and the finding's numeral is the reviewer's measurement artifact: that figure was taken with `tracemalloc` active, and the reviewer has since measured the same fixture at 0.101 s clean against 0.262 s with `tracemalloc` running — 2.6 times slower — with the remainder explained by the different generated content the reviewer's probe used. The finding's SUBSTANCE is unaffected and was re-confirmed: the cost is linear and the output is unbounded, which is what `R-0721` is about. The inaccurate numeral is a reviewer-prose slip with no product effect, so under operator amendment amend0827 rule 2 it spends no id, and under the same rule's fourth bullet it earns no correction round; it is recorded in `.agent/prose_slips.md` by this round's C2. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END GATER11

<<<SLICE SLIPR12
- 2026-08-28 · F037 R11 · Finding `R-0721` states a parse cost of 0.363 s for a
  10k-line diff, and the figure is an artifact of the reviewer's own probe rather
  than a property of the parser: it was measured with `tracemalloc` active around
  the call. Measured clean afterwards, the same fixture parses in 0.101 s and the
  same fixture with `tracemalloc` running takes 0.262 s, so the instrumentation
  accounted for a factor of 2.6 and the different generated content of the probe
  for the rest. The R11 worker measured 0.105 s, reported the disagreement instead
  of transcribing the finding, and was right to. The finding's substance — linear
  cost, no ceiling — is unaffected and was re-confirmed. A timing figure that will
  be written into the append-only record is measured by the SAME instrument the
  round will use to check it, never through a profiler that is switched on for the
  memory reading beside it; a measurement's harness is part of the measurement.
<<<END SLIPR12

<<<SLICE DECISION5
## DECISION F037 D5 — the parsed diff is bounded at 20,000 body lines, and `truncated` becomes something F037 decides

**Date:** 2026-08-28 · **Round:** F037 R12 · **Finding:** `R-0721`

**The choice.** `packages/orchestration/diff_parser.py` gains a module constant
`DIFF_VIEW_MAX_BODY_LINES = 20_000` and refuses to append a body line once the
count of appended lines ACROSS THE WHOLE DIFF has reached it, setting the
contract's existing top-level `truncated` flag True and stopping the walk. A diff
of exactly the ceiling parses in full and is not marked truncated; the flag and
the stop appear only above it.

**Why a bound exists at all.** `R-0721` measured the absence: the parser appended
one dict per body line with no ceiling, `build_diff_view` copied the result onto
the envelope, and the endpoint serialised the whole thing into one response.
`workspace.diff` is a job's ENTIRE workspace diff and no code in this repository
constrains its size, so a job that vendored a dependency or rewrote a lockfile
would have the server build tens of megabytes of JSON on a request the viewer
makes automatically. The cost is linear — the reviewer measured 1k through 20k
lines and the per-line cost is flat — but a linear function with no bound is still
unbounded, and the client half that would otherwise defend itself, T003's virtual
scrolling, cannot be built while the frontend test runner is refused here.

**Why 20,000.** The feature file's Acceptance names a 10,000-line fixture that
must render within budget. A ceiling at or below that would truncate the very
fixture the feature is accepted against, so the value is twice it: the Acceptance
case renders in full with room to spare, and the worst-case payload is bounded at
roughly 2.6 MB of JSON rather than growing with whatever a job happened to touch.

**Why a TOTAL rather than a per-file ceiling.** The payload is the sum. A per-file
bound leaves a diff of fifteen thousand one-line files completely unbounded, which
is a realistic `workspace.diff` shape, so the counter spans the whole diff and the
tests exercise that case directly.

**Why truncation rather than a refusal.** `truncated` already exists in the
contract v1 and has until now only ever relayed an upstream `[DIFF TRUNCATED]`
sentinel. The viewer's whole design, stated in `diff_view_source.py`'s own module
docstring, is that every absence is NAMED in the data rather than raised: a viewer
that 500s on a large job is worse than one that says, in the data, that it is
showing the first part. This makes the existing field mean what its name says.

**What a truncated view looks like, plainly.** The walk stops mid-input, so the
LAST file in the list may carry a partial hunk or a hunk holding no lines at all,
and files after it do not appear. Each file's `stats` still equal a recount of
that file's own parsed lines, so nothing in the payload describes content the
payload does not carry. `truncated` True is the client's signal that the list is a
prefix and not the whole diff.

**Alternatives rejected.** (1) Leave it unbounded — this is the status quo
`R-0721` registers, and it makes the server's memory a function of an
unconstrained artifact. (2) Bound the artifact READ instead — that is a real and
complementary bound, it belongs in `diff_view_source.py` where the filesystem is
touched, and F037 R13 carries it; it is not an alternative to this one, because
0.4 MB of input still expands to over 1 MB of JSON. (3) A byte ceiling on the
input text rather than a line ceiling on the output — rejected because the
contract's unit is a line, the cost is per line object, and a byte cut lands
mid-hunk at an offset no field of the contract can express. (4) Refuse above the
ceiling with an error — rejected for the reason above.

**How to reverse.** Delete `DIFF_VIEW_MAX_BODY_LINES` and the guard that reads it
in `parse_unified_diff_to_view`, and delete the tests F037 R12 added in the final
section of `tests/orchestration/test_diff_parser.py`. Nothing else depends on the
constant; the `truncated` field returns to relaying the upstream sentinel alone.
<<<END DECISION5

<<<SLICE DONE0721
Done: R-0721 — RESOLVED IN PART at F037 R12, and the remaining part is named rather than left implied. `packages/orchestration/diff_parser.py` now carries `DIFF_VIEW_MAX_BODY_LINES` and refuses to append a body line once that many have been appended across the whole diff, setting the contract's `truncated` flag and stopping the walk — so the flag is now something F037 DECIDES, where before it only ever relayed an upstream `[DIFF TRUNCATED]` sentinel, which is the specific inertness the finding registered. DECISION F037 D5 records the value, why it is twice the 10,000-line fixture Acceptance names, why the counter spans the whole diff rather than each file, and how to reverse the whole thing. The repair is proved in both colours rather than asserted, and the boundary is pinned on BOTH sides so an off-by-one in the comparison cannot hide: a diff of exactly the ceiling parses in full and is not marked truncated, a diff of two more parses to exactly the ceiling and is. The many-files dimension is covered by the same counter and the same tests, which is the case a per-file ceiling would have missed. THE PART THAT IS NOT REPAIRED, STATED PLAINLY: `packages/orchestration/diff_view_source.py` still reads the artifact whole with `read_text` before the parser ever sees it, so the INPUT is still unbounded even though the OUTPUT no longer is; constraint 3 of the R12 block deliberately kept that module out of this round so these red-proofs could say which half they proved, and F037 R13 carries it. The four tests F037 R11 added are untouched and still pass, which is what proves the ceiling was chosen high enough not to truncate the fixture the feature is accepted against.
<<<END DONE0721

## Gates — every command is RUN and its REAL exit code recorded

Eight gates. "Green" as a word is a finding; a gate that was not executed is
reported as not executed.

**G1 hygiene.** Read `.agent/STOP` from disk BEFORE C0a and again before C6, and
report the literal reading both times. Report `git rev-parse HEAD` before C0a and
state whether it equals the base above, and `git branch --show-current`. Report the
LINE COUNT of `git status --porcelain` after each of C0a, C0b, C1, C2, C3, C4 and
C5.

**G2 transport, ONE digest comparison.** After C0b, report `git rev-parse` of both
`HEAD:.agent/authored/f037-r12.md` and `HEAD:.agent/last_block.md` and state
whether they are the same blob hash. Report the sha256, byte count and line count
of the working copy of `.agent/authored/f037-r12.md`. State plainly what the chain
covers: the saved copy and its mirror.

**G3 extraction and caps.** Extract every slice from the COMMITTED C0a blob by its
marker lines, in Python, and report each slice's line count, the CONTENT total, the
TOTAL line count of the blob and PROSE = TOTAL − CONTENT. State whether TOTAL is at
most 490 and PROSE at most 400. Measure the blob; carry no figure from this block's
prose into that table.

**G4 the plan at C1.** Report whether `.agent/plan.md` is byte-equal to the
PLANF037R12 slice, newline included, and a NEGATIVE CONTROL against the same slice
minus its trailing newline, which must read False. Report the count of lines
exactly matching `## Goal` and of lines exactly matching `## Next Steps`. Report
`wc -l` and state whether it is STRICTLY under 50. The binding clause is the strict
inequality; the measurement wins over any figure elsewhere and disagreement is
declared.

**G5 the record at C2, C3 and C5.** For each of the four appends — GATER11 into
`.agent/live_review.md` and SLIPR12 into `.agent/prose_slips.md` at C2, DECISION5
into `.agent/decisions.md` at C3, DONE0721 into `.agent/live_review.md` at C5 —
report the file's byte size before and after and TWO independent readers. Reader (a)
is the BYTE IDENTITY `result == before + b"\n" + slice`, re-read from disk. Reader
(b) counts the N blank-line-separated units in the slice and compares the LAST N
units of the file against the slice's N units IN ORDER. Report a NEGATIVE CONTROL
per append flipping ONE byte INSIDE the first appended paragraph; BOTH readers must
come back False. Report whether the pre-round blob of each file is a byte PREFIX of
its result.
Then report these counts over `.agent/live_review.md` after C5, line-anchored:
`^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-`, `^Gate: F\d+ R\d+ — `, the size of
the open set, whether every id is distinct, whether `R-0721` occurs ZERO times as a
new registration this round and exactly once as a resolution. Report `^## DECISION `
over `.agent/decisions.md` and the count of `F037 D5`, which must be exactly 1.

**G6 the red-proofs of the ceiling.** All of this runs inside a disposable
`git worktree` under `.remedy-wt/`, at the C4 tree, never in the primary checkout;
purge `__pycache__` and use `python3 -B` before EVERY run; restore the mutated file
between runs and verify each restore is byte-identical.

Report the UNMUTATED CONTROL first: `python3 -B -m pytest
tests/orchestration/test_diff_parser.py -q`, its REAL exit code and verbatim summary
line.

Then FOUR mutations of `packages/orchestration/diff_parser.py`, each applied alone
and reverted before the next. For each report the exact string replaced, the count
of its occurrences BEFORE the edit, the REAL exit code, the verbatim summary line,
and WHICH node ids fail as measured. THE ORDERED PROPERTY IS THE COLOUR: each must
be RED. Do not treat any predicted name or count as the gate.

- **(a) the bound removed.** Delete the guard so the parser is unbounded again —
  the state `R-0721` registers. This is the proof the repair is load-bearing.
- **(b) the flag not set.** Keep the stop but do not set `truncated` True. This
  separates "stopped" from "said it stopped"; a bound that truncates silently is
  worse than none, because the client cannot tell a short diff from a cut one.
- **(c) the counter scoped to one hunk instead of the whole diff.** Change the
  guard to compare the CURRENT HUNK's own line count against the ceiling rather
  than the whole-diff counter. This is the realistic wrong-scope mistake and it is
  the mutation S9 exists for; report what actually fires.
  A NOTE ON WHY THIS SPELLING AND NOT ANOTHER: resetting the counter inside
  `open_region` instead looks equivalent and is NOT — that function is a closure
  and would bind a fresh local rather than the enclosing counter unless a
  `nonlocal` is added, so the edit is inert and the mutation comes back green for
  a reason that has nothing to do with the tests. The reviewer measured that dead
  end; do not substitute it.
- **(d) the ceiling lowered below the Acceptance fixture.** Set the constant to a
  value under 10,000. THIS MUTATION IS CONSTRAINT 9 WRITTEN AS A PROOF: it must
  turn the R11 tests red, showing that those four tests really do guard the
  fixture the feature is accepted against against a ceiling chosen too low.

If a mutation comes back GREEN, STOP: report it, diagnose WHY the assertions could
not see it, and declare it rather than substituting a different mutation.

Afterwards report `git worktree remove`, `git worktree prune`, the line count of
`git worktree list` and the line count of `git status --porcelain` in the primary
checkout.

**G7 suite, lint and canary at C4.** ONE pytest process at a time; never two in
parallel. Report the REAL exit code and verbatim summary of each:

- `python3 -m pytest tests/orchestration/ -q` — THE WHOLE DIRECTORY, not a
  selection, because C3 changes shipped production code that other suites import —
  and the count of lines matching `^FAILED`. Report an EXTRACTOR-BLINDNESS CONTROL:
  the same counter over a control string that does begin with `FAILED`, returning a
  non-zero count.
- `python3 -m pytest tests/ui_server/test_diff_endpoint.py -q`, which exercises the
  endpoint that serves this parser's output.
- `python3 -m ruff check packages/orchestration/diff_parser.py tests/orchestration/test_diff_parser.py`
  under the repository's own configuration, with NO `--isolated`.
- The canary `python3 -m pytest tests/cli/test_golden_path.py -q`. The base figure
  is `42 passed`; report the measured figure beside it and name any difference.
- Report the parser suite's verbatim `in <n>s` figure at the base `f676f419` and at
  C4, and state the difference.

**G8 structure, artifacts and the Open PR Gate at C5.** Report
`git diff --name-only f676f419..<C5>` and both RESIDUES against the change set above
minus `.agent/handoff.md`: actual minus expected, and expected minus actual. Report
`git diff --stat` restricted to `docs/` and `apps/` — each must be EMPTY — and to
`packages/`, which MUST HOLD ONLY `packages/orchestration/diff_parser.py`; that last
reading is what proves constraint 3. Report per-commit insertions from
`git diff --numstat` for C0a through C5, each commit's parent count, and whether each
insertion count is under 500. Report a marker sweep of `^<<<SLICE ` and `^<<<END `
over `.agent/plan.md` at C1, `.agent/live_review.md` at C5,
`packages/orchestration/diff_parser.py` at C3 and
`tests/orchestration/test_diff_parser.py` at C4, and the SAME counter over the C0a
blob, whose figures must be greater than zero so the zeros are a measurement. Report
`git ls-files .remedy-wt` line count. Report the Open PR Gate verbatim:
`gh pr list --state open --json number,headRefName,baseRefName,isDraft`.

## Done when

C0a, C0b, C1, C2, C3, C4, C5 and C6 are committed in that order, one commit each,
the branch is pushed, `.agent/handoff.md` is rewritten per
`docs/agents/handback_template.md` carrying the state block, the deviations, the
item-status table and the next steps, and every gate above is reported with its REAL
exit code. The handback names SESSION 3 of feature F037 and round 12.

A gate that could not be run is reported as NOT RUN with the literal refusal or
error text — never as a pass, and never worked around.
