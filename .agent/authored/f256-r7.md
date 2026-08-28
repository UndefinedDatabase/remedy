### STEP T002b — F256 Diff viewer completion, round 7 (THE CLIENT MEASUREMENT)

Goal: measure the 10k-line fixture through the CLIENT model and pin the property
that actually makes a diff that size viable — that the drawn window stays a small
constant however long the document gets. Round 6 measured the server half. This
round measures the half the server hands to, so that round 8 can write both sets
of numbers into the feature file's Built State.

Base: `dff36f33`, the tip of `feature/f256-diff-viewer-completion`. Every reading
below was taken there by the reviewer.

Bundle, in commit order:

- C0a save this block verbatim to `.agent/authored/f256-r7.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 advance `.agent/plan.md`
- C2 append the R6 verdict to `.agent/live_review.md` and DECISIONS F256 D5 and
  F256 D6 to `.agent/decisions.md`
- C3 the client measurement in `apps/ui/src/api/diffViewModel.test.ts`
- C4 rewrite `.agent/handoff.md`

Change set, these paths and nothing else:

- `.agent/authored/f256-r7.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `.agent/decisions.md`
- `apps/ui/src/api/diffViewModel.test.ts`
- `.agent/handoff.md`

NO PRODUCTION FILE IS EDITED BY THIS ROUND. `apps/ui/src/api/diffViewModel.ts`,
everything else under `apps/ui/src/`, `packages/` and `docs/` are NOT touched in
the primary checkout. The red-proof mutates `diffViewModel.ts` inside a disposable
worktree and reverts it; that is the only place it changes.

### Constraints

0. BEFORE ANYTHING: report `gh pr list --state open --json number,headRefName`.
   Do NOT create or merge a pull request. Stay on
   `feature/f256-diff-viewer-completion`; do not branch, never work on `main`.
1. Apply every authored slice BYTE FOR BYTE — no reflow, rewording, retitling,
   correction or shortening. If a slice looks wrong, apply it as written and say
   so in the handback's deviations.
2. The delimiter lines `<<<SLICE …` and `<<<END …` are transport only and never
   reach a target file.
3. Extract every slice from the COMMITTED blob with
   `git show <C0a>:.agent/authored/f256-r7.md`, never from this prompt's text.
4. AGENTS.md binds in full: self-review before every commit, one logical step per
   commit, `.agent/plan.md` current before every commit, clean tree, push.
5. Destructive verification runs ONLY inside a disposable `git worktree` under the
   gitignored `.remedy-wt/`. The primary checkout satisfies
   `git status --porcelain` empty at every commit. G7 below states the exact
   route by which a vitest red-proof meets this, because vitest CANNOT run inside
   a worktree — see DECISION F256 D6, which you are applying, not deciding.
6. Shell forms rejected by this session's guard are RE-EXPRESSED as a script file
   under `.remedy-wt/` run with `python3`, never skipped and never weakened.
   Report each one.
7. READ `apps/ui/src/api/diffViewModel.test.ts` IN FULL BEFORE EDITING IT. It
   already carries the fixture helpers `wireEnvelope`, `wireFile`, `wireHunk` and
   `envelopeWithHunkOf`, and a `SCALE_ROWS` constant of 10000 used for the window
   tests. REUSE those helpers; do not write a second envelope builder. Report
   which you reused.
8. NO EXISTING ASSERTION IS WEAKENED, DELETED OR RELAXED, and no existing test in
   that file changes by one byte. If an existing guard genuinely contradicts this
   block, STOP and hand back with the contradiction stated.
9. A MEASURED NUMBER IS NEVER INVENTED AND NEVER COPIED FROM THIS BLOCK. Every
   figure you write into a comment or a docstring is one YOUR OWN run produced.
   The figures inside the DECF256D5 slice are the REVIEWER'S, measured at
   `dff36f33`; they are applied as part of that slice byte for byte and are never
   transcribed into a test as though this round had measured them.
10. NO CONSTANT IN `diffViewModel.ts` IS CHANGED to make an assertion pass. If a
    real run cannot meet what S2 fixes, that is a finding: STOP and hand back with
    the full numbers.

### SPEC — the measurement of C3

S1. Add ONE new `describe` block to `apps/ui/src/api/diffViewModel.test.ts`,
after the existing ones, covering the Acceptance fixture through the client model.
It builds its envelope with the file's OWN helpers and asserts on
`buildDiffRowModels`, `defaultCollapsedHunkIds` and `diffRowWindowForViewport`.

S2. THE TRAP THIS BLOCK EXISTS TO AVOID, and the reason S3 is written the way it
is. Measured by the reviewer at `dff36f33`: `defaultCollapsedHunkIds` collapses a
single hunk of 10,000 lines AND a single hunk of 1,000 lines — its returned set
has size 1 in both cases — and a collapsed hunk emits NO line rows, so
`buildDiffRowModels(envelope, defaultCollapsedHunkIds(envelope))` returns just TWO
rows for the Acceptance fixture. A benchmark written that way measures two rows
however large the fixture is. Every measurement below therefore passes an EMPTY
collapsed set, and one test pins the collapse fact itself so the trap is recorded
rather than merely avoided.

S3. THE RECORDING TEST. Over an envelope of one file and one hunk of 10,000 body
lines, with an EMPTY collapsed set, build the row models several times and record
the MEDIAN, MINIMUM and MAXIMUM wall clock in a comment, dated and attributed to
a machine class the way `test_the_huge_diff_parses_inside_the_recorded_perf_budget`
in `tests/orchestration/test_diff_parser.py` does. Pin the WORK first — a
measurement of an empty answer is not a measurement: the row count is exactly the
body-line count plus one file row plus one hunk-head row, and that arithmetic is
written as an expression over the constants, never as a bare literal.

S4. THE GUARD, and it is EXACT rather than timed. Build the window over the
Acceptance row count and over a row count TEN TIMES larger, and assert that
`diffRowWindowForViewport` reports `virtualized` true for both and that
`rowsInWindow` is IDENTICAL for the two — the drawn row count does not grow when
the document does. That constant is what makes a 10k-line diff viable at all, it
is decided by `DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS` and
`DIFF_VIRTUAL_OVERSCAN_ROWS` rather than by the document, and unlike a duration it
is the same number on every machine. Assert also that `rowsInWindow` is far below
the total row count, expressed as a comparison against the row count and not as a
literal.

S5. THE COLLAPSE FACT. One test pinning what S2 records: over the Acceptance
fixture, `defaultCollapsedHunkIds` returns a set of size 1, and building with THAT
set yields exactly two rows while building with an empty set yields the full
count. Its comment states plainly that this is the viewer's FIRST PAINT of a
10k-line diff — the hunk arrives collapsed — and that the expanded number is what
S3 measures.

S6. Every assertion names, in its failure message or through `expect`'s own
output, the measured figure and what it was compared against. Print the recorded
figures with `console.log` in the shape round 6 used in
`tests/ui_server/test_diff_endpoint.py`, so a run reports what the comments carry.

### The authored slices

<<<SLICE PLANF256R7
# Plan — F256 Diff viewer completion

Branch: feature/f256-diff-viewer-completion, cut from `main` at `0e8ab5b4`.
F256 was claimed by Rule A5 as the first unchecked line of Package 1 in
`docs/roadmap/STATUS.md`.

## Goal
Finish the rendered diff viewer F037 shipped: highlighting actually rendered
rather than only modelled, the 10k-line budget measured and recorded, and the
file sidebar's visual treatment ruled by a named authority.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the per-line highlight model | done | `apps/ui/src/api/diffHighlight.ts` |
| the DiffView wiring and the derived palette | done | `678bc698` |
| make the lazy load real, repairing `R-0732` | done | `8bcff3db` |
| rule on the sidebar's treatment | done | `1b70fb02`, DECISION F256 D3 |
| measure the 10k fixture, server half | done | `4aea7ba2`, DECISION F256 D4 |
| measure the 10k fixture, client half | done | this round |
| record the numbers in the feature file | open | next round |

## Next Steps
1. Write both halves' measured numbers into the Built State of
   `docs/roadmap/features/T5_F256.md`, which is what Acceptance asks for: a
   recorded measurement rather than a claim.
2. Run the integration gate.
3. Run the closure sequence, which needs two rounds — evidence and zip, then the
   STATUS commit.

## Risks
- A collapsed hunk emits no line rows, so a client benchmark built with the
  DEFAULT collapsed set measures two rows however large the fixture is.
- The client model costs about a millisecond with a threefold run-to-run spread,
  so a timing assertion there would measure the JIT; DECISION F256 D5 rules the
  exact bounded-window property instead.
<<<END PLANF256R7

<<<SLICE GATEF256R6
Gate: F256 R6 — the SERVER-SIDE MEASUREMENT round, which measured the Acceptance fixture through the real read endpoint and guarded its shape by a ratio rather than a second count. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran each one independently at `dff36f33`.

TRANSPORT COVERS THE EMISSION: the reviewer's own scratch original `.remedy-wt/f256-r6-block.md` predates the worker, and the committed `.agent/authored/f256-r6.md` blob at `250529ba` is BYTE EQUAL to it at 27077 bytes, sha256 `9c873ffb6f5d31498d0305f4e7ebe10412a3d7e739ff59516882e5fc65516b67`. At `b402da84` the authored path and `.agent/last_block.md` are ONE blob id, `2fd3a32f39c5b70ca4dd0d9257a2c03c411f0df6`. `.agent/plan.md` at `221c1dd2` is byte-equal to its slice at 35 lines, both appends at `1962f8ef` reconstruct byte for byte from the `08f6218a` blob plus a newline plus their slice with each pre-round blob a byte PREFIX, and in each a byte flipped inside the FIRST appended paragraph is REJECTED. The ledger moved as a round that registers and resolves nothing should: registrations 293 and all DISTINCT, `^Done:` 43, `^Landed:` 11, the OPEN SET as a set 252, and `^Gate: F\d+ R\d+ — ` alone rising by one to 102, with `Gate: F256 R5` occurring exactly once.

THE MEASUREMENT IS REAL AND THE REVIEWER RE-TOOK IT RATHER THAN READING IT. Running the new class alone at `dff36f33` the reviewer measured a median of 0.1343 s over five GETs at 10,000 body lines, minimum 0.1292 s, maximum 0.1408 s, for a response of 1,045,960 bytes — against the 0.1331 s, 0.1282 s, 0.1489 s and 1,045,960 bytes the docstring records. The byte figure is EXACT and the three durations sit inside ordinary run-to-run spread, so the recorded numbers are this machine's numbers. The route served `available` True, `truncated` False, one file and exactly 10,000 summed body lines, so the budget is not being met by serving nothing, and `DIFF_VIEW_MAX_BODY_LINES` is 20,000 with the fixture asserted strictly below it.

THE RESPONSE-SIZE FIGURE IS RECONSTRUCTED, AND THE RECONSTRUCTION IS FAITHFUL. `_get` hands back a decoded body, so the test reports `len(json.dumps(body, default=str).encode())`; the reviewer read `_send_json` in `packages/orchestration/ui_server.py` and it writes exactly `json.dumps(data, default=str).encode()`, so the two are the same bytes rather than an estimate of them. A six-byte difference against the reviewer's own earlier probe is fully explained by that probe's fixture carrying a `task_runs/T001` directory, which puts one more entry in `task_run_ids`.

THE RED-PROOF IS REAL, AND THE REVIEWER RAN THREE MUTATIONS WHERE THE BLOCK ORDERED TWO. In a disposable worktree at `4aea7ba2`: control 8 passed; lowering `DIFF_VIEW_MAX_BODY_LINES` from 20_000 to 5_000 turned the file RED with 2 failed; the reviewer's own dry-run spelling `diff_text.count(stripped[:1])` in the parser's per-line path turned the ratio test RED; the shipped spelling `diff_text.replace("body", "BODY")` turned the ratio test RED; and the control passed 8 again, with worktree porcelain empty after every revert.

THE WORKER'S DECLARED DEVIATION 1 IS TRUE, AND IT IS THE MOST VALUABLE LINE IN THE HANDBACK. It reported that its first mutation, `diff_text.count(stripped)`, was a genuine whole-input scan that nevertheless did NOT redden the file, and that it therefore switched spellings rather than touching a constant or an assertion. The reviewer ran that exact spelling and confirms it: exit 0, 8 passed. So the ratio ceiling of 20 is NOT tripped by every whole-input scan — only by one costly enough to move the median — which is a real limit on the guard's reach, and the worker recorded it instead of quietly shipping a mutation that happened to work.

RE-RUN IN THE PRIMARY CHECKOUT, one pytest process at a time, each exit 0 and each equal to the handback's figure: `tests/ui_server/` 497 passed in 30.42 s against 495 at the base, `tests/orchestration/test_diff_parser.py` 43 passed, `tests/orchestration/test_diff_view_source.py` 15 passed, `tests/ui_contracts/` 664 passed with 4 skipped, `tests/orchestration/test_integrity_gate.py` 16 passed, and the canary `tests/cli/test_golden_path.py` 42 passed. `ruff check` on the changed test file reports "All checks passed!". The change set is six paths with both residues empty, every commit single-parent and under 500 insertions, and NO file under `packages/`, `apps/` or `docs/` moved by a byte. The branch tip equals `origin/feature/f256-diff-viewer-completion`, the primary checkout reads `git status --porcelain` empty, and `gh pr list --state open` is `[]`.
<<<END GATEF256R6

<<<SLICE DECF256D5
## DECISION F256 D5 (2026-08-28, F256 R7) — the client half of the 10k budget is guarded by the EXACT bounded-window property, not by a duration, and the numbers are recorded beside it

CONTEXT. DECISION F256 D4 ruled the SERVER half of F037's Acceptance budget and
guarded it with a scale ratio taken on one machine in one run. The CLIENT half —
`readDiffEnvelope`, `buildDiffRowModels` and `diffRowWindowForViewport` in
`apps/ui/src/api/diffViewModel.ts` — is what turns that envelope into the rows a
renderer draws, and it has never been measured at the Acceptance size.

WHAT THE REVIEWER MEASURED AT `dff36f33`, over an envelope of one file and one
hunk, with the collapsed set EMPTY, as the median of seven builds: 0.469 ms at
1,000 body lines producing 1,002 rows, and 1.688 ms at 10,000 body lines producing
10,002 rows. The spread is the point: 0.122 ms to 0.918 ms at the small size and
0.943 ms to 3.043 ms at the large one, a factor of three or more between the
fastest and slowest sample in the same run, because a millisecond of JavaScript is
mostly the JIT deciding whether to compile. The measured ratio was 3.60, nowhere
near the algorithmic 10, for the same reason.

CHOSEN. The client half records its durations and asserts on something else
entirely: that `diffRowWindowForViewport` reports `virtualized` true at the
Acceptance row count and that its `rowsInWindow` is IDENTICAL at ten times that
row count. Measured at `dff36f33`, 10,002 rows draw 48. That number is decided by
`DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS` and `DIFF_VIRTUAL_OVERSCAN_ROWS` and not by
the document, so it is the same integer on every machine, in every run, forever —
and it is the property that actually makes a 10,000-line diff viable, because what
would make the viewer unusable is drawing ten thousand rows, not spending two
milliseconds building a list. An exact invariant is a better guard than a noisy
duration, and here one is available.

THE COLLAPSE TRAP IS RECORDED BECAUSE IT MAKES THE OBVIOUS BENCHMARK VACUOUS.
`defaultCollapsedHunkIds` returns a set of size 1 for a single hunk of 10,000
lines and ALSO for one of 1,000, and a collapsed hunk emits no line rows at all,
so the natural spelling — build the default collapsed set, then build the rows —
returns TWO rows however large the fixture is, and times nothing. The reviewer hit
this on the first probe. Every client measurement therefore passes an EMPTY
collapsed set, and a test pins the collapse fact itself so that the next reader
meets it as an assertion rather than as a surprise. It is also a real product
fact worth recording: the viewer's FIRST PAINT of a 10,000-line diff is two rows,
and the ten thousand arrive only when the reader expands the hunk.

ALTERNATIVES CONSIDERED. (a) A ratio guard mirroring D4. Rejected: at a
millisecond, with a threefold spread inside one run, the measured ratio would
sometimes be 3 and sometimes 12, so the assertion would report the JIT rather than
the code. (b) An absolute millisecond ceiling. Rejected for the same noise, and
because it would be the flakiest assertion in a suite of 628 that currently
finishes in under a second. (c) Measure nothing on the client and rely on the
server figure. Rejected because Acceptance says "end to end", and the row model is
the half a reader actually looks at.

CONSEQUENCE. What is ASSERTED on the client is exact and machine-independent; what
is RECORDED is the real duration, in a comment and in the Built State of
`docs/roadmap/features/T5_F256.md`, dated and attributed to a machine class. A
reader who wants to know how fast the client model is reads the numbers; a runner
that is merely slow, or merely cold, does not turn the suite red.

REVERSE by deleting this decision and replacing the bounded-window assertions with
a duration bound, accepting the flakiness the paragraphs above measure. The
recorded numbers are unaffected either way, because they are a measurement and not
a bound.
<<<END DECF256D5

<<<SLICE DECF256D6
## DECISION F256 D6 (2026-08-28, F256 R7) — a vitest red-proof runs the WORKTREE's mutated sources against the PRIMARY checkout's node_modules, because vitest cannot run inside a worktree

CONTEXT. Guardrail G5 of docs/agents/self_drive_protocol.md requires destructive
verification — mutation and red-proof checks — to run only inside a disposable
`git worktree`, never in the primary checkout, so that `git status --porcelain` is
empty at every verdict. Every red-proof in this feature so far has been a pytest
run, which needs nothing but the repository. A vitest red-proof does not have that
property, and F256 R7 is the first round in this feature whose new test is a
vitest test.

THE OBSTACLE, measured by the reviewer at `dff36f33`. A `git worktree` contains no
`node_modules`, symlinking one in is denied in this environment, and installing
one inside a throwaway worktree is neither fast nor guaranteed to have a network.
Running `npx vitest run` from inside a worktree's `apps/ui` fails at startup with
`Cannot find package 'vitest'`, because the only `node_modules` above it is the
repository root's, which does not carry vitest. So the literal reading of G5 makes
a vitest red-proof impossible, and the tempting repair — mutate the primary
checkout and revert afterwards — is exactly what G5 exists to forbid.

CHOSEN, and it satisfies G5 rather than excusing it. The mutation is applied to
the WORKTREE's copy of the source, and vitest is invoked with its working
directory set to the PRIMARY `apps/ui`, so module resolution finds the primary's
`node_modules`, while the FILES under test are named by absolute path inside the
worktree. Concretely: a scratch config under `.remedy-wt/` exports a plain object —
it must NOT `import` from `vitest/config`, because a config outside the package
cannot resolve that specifier — setting `root` to the primary `apps/ui`, `cacheDir`
to a path under `.remedy-wt/`, and `test.include` to the absolute path of the
worktree's test file. The primary checkout's sources are never written to.

THE ROUTE WAS PROVED, NOT ASSUMED, and the proof is the part worth keeping. Simply
observing that the suite runs would not show WHICH copy of the source it ran: the
reviewer first mutated the worktree's `DIFF_HUNK_COLLAPSE_THRESHOLD_LINES` and saw
90 tests still pass, which is consistent both with the route being a lie and with
those particular tests deriving their expectation from the constant they import.
The question was settled by gutting `buildDiffRowModels` in the WORKTREE copy so
that it returns an empty array: 8 of the 90 tests went red, and reverting restored
all 90. The worktree's source is therefore genuinely the one under test.

`cacheDir` IS LOAD-BEARING AND NOT TIDINESS. Without it, running vitest with the
primary as root writes an untracked `.vite/` directory into the repository root,
which is not gitignored, so the red-proof would leave the primary checkout DIRTY —
the precise condition G5 exists to prevent. With `cacheDir` pointed inside the
gitignored `.remedy-wt/`, the reviewer measured `git status --porcelain` empty in
the primary after a full run.

CONSEQUENCE. A vitest test in this repository can now be red-proved to the same
standard as a pytest one, and G5 is met literally rather than waived. The residual
limit is stated plainly: the run borrows the primary's INSTALLED PACKAGES, so this
route proves things about mutated SOURCE and never about a change to
`package.json` or to a dependency version, which it cannot see.

REVERSE by deleting this decision; a later session that finds `node_modules`
reachable from inside a worktree should prefer the plain route and delete the
scratch config with it.
<<<END DECF256D6

`PLANF256R7` is a WHOLE-FILE replacement of `.agent/plan.md`. `GATEF256R6` is an
APPEND to `.agent/live_review.md`. `DECF256D5` and `DECF256D6` are APPENDS to
`.agent/decisions.md`, in that order, D5 before D6. For each append add exactly
what gate G4 measures — the pre-round blob, one newline, then the slice —
whatever blank lines that file already ends with; and when both decision slices go
into one file, append D5 first and then D6 the same way, so the file ends with D6.

### Done when

G1 HYGIENE AND STRUCTURE. Read `.agent/STOP` with `os.path.exists` before C0a and
again before C3; report both, and stop after the commit in hand if it exists.
Report `git rev-parse HEAD` before C0a — it must equal `dff36f33` —
`git branch --show-current`, and `git status --porcelain | wc -l` after each of
C0a, C0b, C1, C2 and C3. Then, over `dff36f33..<C3>` — the range ending BEFORE the
handback commit, so `.agent/handoff.md` is expected in the change set but not in
this range — report `git diff --name-only` and both residues against the change
set with `.agent/handoff.md` set aside, printed in both directions and both
expected empty. Report each commit's insertions from `git diff --numstat`, each
under 500, and that each of C0a, C0b, C1, C2 and C3 is single-parent. Report the
counts of lines beginning `<<<SLICE ` and `<<<END ` in every target other than
`.agent/authored/f256-r7.md` and `.agent/last_block.md` — each expected 0 — beside
those two as the non-zero control. Report `git ls-files .remedy-wt | wc -l`,
expected 0, and `git worktree list` after the red-proof worktree is removed.

G2 TRANSPORT. One digest comparison: sha256 of
`git show <C0a>:.agent/authored/f256-r7.md` against the reviewer's own original at
`.remedy-wt/f256-r7-block.md`, reporting both digests, the byte length and
equality; that original predates this worker, so say the reading covers more than
self-consistency. Report that `<C0b>:.agent/authored/f256-r7.md` and
`<C0b>:.agent/last_block.md` are ONE blob id.

G3 THE PLAN AT C1. `.agent/plan.md` at C1 equals PLANF256R7 including the trailing
newline — report `True` or `False` — with `wc -l` under 50 and the counts of lines
exactly `## Goal` and exactly `## Next Steps`.

G4 THE RECORD AT C2. (a) For `.agent/live_review.md`, the `dff36f33` blob plus a
newline plus GATEF256R6 equals the C2 blob; for `.agent/decisions.md`, the
`dff36f33` blob plus a newline plus DECF256D5 plus a newline plus DECF256D6 equals
the C2 blob. Report each as `True` or `False`, and report each pre-round blob is a
byte PREFIX. NEGATIVE CONTROL for each file, flipping one byte at an offset your
script confirms lies INSIDE THE FIRST appended paragraph and reporting the
equality now `False`. (b) Let N be the paragraph count of the appended text for
each file, COUNTED BY YOUR SCRIPT and never taken from this block, ignoring an
empty trailing unit; report N and that the LAST N blank-line units of each file
match those paragraphs IN ORDER. Report that `## DECISION F256 D5` and
`## DECISION F256 D6` each occur exactly once in the C2 blob, and that D5's offset
is smaller than D6's.

G5 THE LEDGER AT C2. Over the C2 blob and the `dff36f33` blob beside it, report
`^- R-\d+ — ` and whether all DISTINCT, `^Done: R-\d+ — `, `^Landed: R-`,
`^Gate: F\d+ R\d+ — `, and the OPEN SET as a set. This round registers and
resolves nothing, so every figure is UNMOVED except `^Gate: F\d+ R\d+ — `, which
rises by exactly ONE. Report that `Gate: F256 R6` occurs exactly 1 time.

G6 THE MEASUREMENT AT C3. Run the new tests and report, from that run: the median,
minimum and maximum build time at the Acceptance size; the row count built with an
EMPTY collapsed set and the row count built with the DEFAULT collapsed set; the
size of the set `defaultCollapsedHunkIds` returns; `virtualized` and `rowsInWindow`
at the Acceptance row count and at ten times it, with confirmation that the two
`rowsInWindow` values are EQUAL. State whether every figure you wrote into a
comment is the figure this run produced. Run the WHOLE vitest suite too and report
its exit code and totals.

G7 THE RED-PROOF AT C3, applying DECISION F256 D6's route exactly. Create a
disposable worktree under `.remedy-wt/` at the C3 commit. Write a scratch vitest
config under `.remedy-wt/` that exports a PLAIN OBJECT — it must not `import` from
`vitest/config` — with `root` set to the PRIMARY `apps/ui`, `cacheDir` set to a
path under `.remedy-wt/`, and `test.include` set to the absolute path of the
WORKTREE's `apps/ui/src/api/diffViewModel.test.ts`. Invoke

    ["npx", "vitest", "run", "--config", "<that config>"]

with `cwd` set to the PRIMARY `apps/ui`. Report the UNMUTATED CONTROL FIRST, then
each mutation with its exit code and passed/failed totals. THE MUTATIONS, each
applied ALONE to the WORKTREE's `apps/ui/src/api/diffViewModel.ts` and reverted
before the next, each of which must turn the file RED:
(i) make `buildDiffRowModels` return an empty array as its first statement, so the
row-count pins have nothing to count;
(ii) in `diffRowWindowForViewport`, make the unmeasured-viewport fallback grow
with the document by changing the line

        ? DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS

to read `        ? totalRows` instead, so `visibleRowCount` tracks the document
and the bounded-window assertion of S4 no longer holds. The reviewer measured
this anchor as occurring exactly once in that file at `dff36f33`. Report the
exact edit you made, WHICH assertions went red, and note that this mutation is
expected to redden existing window tests as well as the new one — that is
correct, not a scope problem.
Report the control again, green. Then report `git status --porcelain` in the
PRIMARY — it must be EMPTY, which is what `cacheDir` is for — and confirm the
worktree was removed.

G8 THE SUITES AT C3. In the PRIMARY checkout: the whole vitest suite via `npx
vitest run` in `apps/ui` with its real exit code and totals; `npx tsc --noEmit` in
`apps/ui` with its real exit code; then, one pytest process at a time from the
repository root, `tests/orchestration/test_test_runner.py` — it spawns `npx vitest
run` under a 30-second timeout, so report its WALL CLOCK beside the reviewer's
measurement at `dff36f33` of 628 tests in 33 files finishing in about 1.0 second —
`tests/ui_contracts/`, `tests/ui_server/`, and the canary
`tests/cli/test_golden_path.py`. Every one must be exit 0. If any is red, STOP and
write the handback with the FULL untruncated failure list.

### Handback

Rewrite `.agent/handoff.md` in C4 per docs/agents/handback_template.md. It
carries: `SESSION 2 of feature F256 · round 7`; the range `dff36f33..HEAD`; a
per-commit changed-files table with `+/-` from `git diff --numstat` compared cell
by cell against G1's figures; ONE LINE PER GATE G1 through G8 with its real
result; the deviations, including every guard re-expression constraint 6 required;
the item-status table with every C-item and every gate appearing exactly once; and
the next expected action, which is writing both halves' numbers into the Built
State of `docs/roadmap/features/T5_F256.md`.

Do not write a `Done:` or `Gate:` paragraph of your own anywhere — only
reviewer-authored text sets those. GATEF256R6 above is reviewer-authored and
applied as a slice, which is not the same thing.

After C4: push with `git push -u origin feature/f256-diff-viewer-completion` and
report the outcome. Do NOT create a pull request and do NOT merge anything.
