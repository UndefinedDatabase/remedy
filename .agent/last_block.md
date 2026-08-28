### STEP T002a — F256 Diff viewer completion, round 6 (THE SERVER-SIDE MEASUREMENT)

Goal: measure the 10k-line fixture through the REAL read endpoint and pin the
result with a guard that survives a slower machine, so F037's Acceptance bullet
"10k-line fixture within the perf budget (recorded)" stops being a claim. This
round measures the SERVER half — artifact on disk, parse, envelope, JSON, HTTP.
The CLIENT half and the recording into the feature file are round 7 and round 8.

Base: `08f6218a`, the tip of `feature/f256-diff-viewer-completion`. Every reading
below was taken there by the reviewer.

Bundle, in commit order:

- C0a save this block verbatim to `.agent/authored/f256-r6.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 advance `.agent/plan.md`
- C2 append the R5 verdict to `.agent/live_review.md` and DECISION F256 D4 to
  `.agent/decisions.md`
- C3 the end-to-end measurement in `tests/ui_server/test_diff_endpoint.py`
- C4 rewrite `.agent/handoff.md`

Change set, these paths and nothing else:

- `.agent/authored/f256-r6.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `.agent/decisions.md`
- `tests/ui_server/test_diff_endpoint.py`
- `.agent/handoff.md`

NO PRODUCTION FILE IS EDITED BY THIS ROUND. `packages/orchestration/diff_parser.py`,
`packages/orchestration/diff_view_source.py`, `packages/orchestration/ui_server.py`,
`docs/roadmap/features/T5_F256.md` and everything under `apps/ui/` are NOT touched
in the primary checkout. The red-proof mutates two of them inside a disposable
worktree and reverts each; that is the only place any of them changes.

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
   `git show <C0a>:.agent/authored/f256-r6.md`, never from this prompt's text.
4. AGENTS.md binds in full: self-review before every commit, one logical step per
   commit, `.agent/plan.md` current before every commit, clean tree, push.
5. Destructive verification runs ONLY inside a disposable `git worktree` under the
   gitignored `.remedy-wt/`. The primary checkout satisfies
   `git status --porcelain` empty at every commit.
6. Shell forms rejected by this session's guard are RE-EXPRESSED as a script file
   under `.remedy-wt/` run with `python3`, never skipped and never weakened.
   Report each one.
7. READ `tests/ui_server/test_diff_endpoint.py` IN FULL BEFORE EDITING IT. Its
   `TestDiffEndpoint` carries a `_setup_job` fixture, a `_start_server` and a
   static `_get`. Your class needs the same three shapes over a DIFFERENT evidence
   body, and `_start_server` reads `self.tmp_path` and `self.job_id` off the
   instance, so it cannot be called from a class that does not have them. Measured
   at `08f6218a`, SEVEN modules under `tests/ui_server/` each carry their own
   `start_ui_server` harness, so a second one inside this module follows the
   package's established shape rather than inventing one. Give your class its own
   fixture and its own start helper; `TestDiffEndpoint._get` is a `@staticmethod`
   and is callable unchanged, so reuse that one. Report which you reused and which
   you re-declared. DO NOT EDIT `TestDiffEndpoint` AND DO NOT SUBCLASS IT — a
   subclass would re-run all of its tests under a new name.
8. NO EXISTING ASSERTION IS WEAKENED, DELETED OR RELAXED, and no existing test in
   that file changes by one byte. If an existing guard genuinely contradicts this
   block, STOP and hand back with the contradiction stated.
9. A MEASURED NUMBER IS NEVER INVENTED AND NEVER COPIED FROM THIS BLOCK. Every
   figure you write into a docstring is one YOUR OWN run produced. The figures
   inside the DECF256D4 slice are the REVIEWER'S, measured at `08f6218a`; they are
   applied as part of that slice byte for byte, and they are never transcribed
   into a test docstring as though this round had measured them.
10. NO CEILING IS RAISED TO MAKE A RUN PASS. The four constants in S2 are ruled by
    DECISION F256 D4 and are applied as given. If a real run cannot meet them,
    that is a finding: STOP and hand back with the full numbers.

### SPEC — the measurement of C3

S1. Add ONE new class to `tests/ui_server/test_diff_endpoint.py`, after the
existing `TestDiffEndpoint` class, covering the 10k-line fixture end to end over
the REAL HTTP route that class already exercises, under the split constraint 7
rules. It does not call `build_diff_view` directly, because the thing under
measurement is the route and everything behind it, not the builder alone.

S2. Four module-level constants, each with a `#:` comment saying what it is for
and naming DECISION F256 D4 as the authority for the two guards:

- the Acceptance fixture's body-line count, `10_000`;
- the LINEAR REFERENCE body-line count, `1_000`, measured through the same route
  so the two figures differ only in size;
- the SCALE RATIO CEILING, `20`, which the measured
  `t(10_000) / t(1_000)` must stay under;
- the HANG NET in seconds, `5.0`, a coarse absolute bound on a single 10k request.

The fixture body-line counts must both be EVEN — the body is written as
alternating deletion/addition pairs — and the large one must be strictly below
`DIFF_VIEW_MAX_BODY_LINES`, asserted directly and not merely implied, so a
re-decided ceiling that truncated the very fixture Acceptance names turns this
file red instead of quietly measuring a truncated parse.

S3. A generator for the fixture, local to this module: one file, `body_line_count`
body lines as alternating `-`/`+` pairs, with a hunk header whose counts follow.
`tests/orchestration/test_diff_parser.py` carries a twin of this generator; a
comment on yours must say so, and say why this module carries its own rather than
importing a private helper across test packages. Do NOT import from that module.

S4. The RECORDING test. Serve the 10k fixture as `workspace.diff` through the job
route, five times, and record the MEDIAN wall clock of the request. Before any
timing assertion, pin the WORK — a budget met by serving nothing is not a budget:
the response status is 200, `available` is True, `truncated` is False, exactly one
file entry, and the body lines summed across its hunks equal the Acceptance
count. Then assert the median is under the hang net. The docstring records, as
figures YOUR run produced: the median, the minimum and the maximum request time,
and the byte length of the serialized JSON response. Date the measurement and name
the machine class the way
`test_the_huge_diff_parses_inside_the_recorded_perf_budget` in
`tests/orchestration/test_diff_parser.py` does — read that docstring first and
follow its shape.

S5. The COMPLEXITY GUARD. Measure the median request time at the linear reference
count and at the Acceptance count, over the same route in the same test, and
assert their ratio is under the ratio ceiling. The docstring states, in its own
words, what the assertion separates: a pipeline linear in body lines answers near
the size ratio itself, a pipeline quadratic in body lines answers near its square,
and because both figures come off the SAME machine in the SAME run the assertion
never becomes a report on machine speed. It must also say which direction the
fixed per-request overhead moves the measured ratio, and that the direction is the
safe one.

S6. Both tests must name, in an assertion message, the measured figures and the
constant they were compared against — a red that prints only `assert False`
tells the next reader nothing about which half moved.

### The authored slices

<<<SLICE PLANF256R6
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
| measure the 10k fixture, server half | done | this round |
| measure the 10k fixture, client half | open | round 7, in vitest |
| record the numbers in the feature file | open | round 8 |

## Next Steps
1. Measure `buildDiffRowModels` and `diffRowWindowForViewport` over a 10k-row
   envelope in vitest, which is the client half of the same fixture.
2. Write all measured numbers into the Built State of
   `docs/roadmap/features/T5_F256.md`, which is what Acceptance asks for.
3. Run the integration gate, then the closure sequence.

## Risks
- A perf assertion that pins an absolute second count on a hosted runner is a
  report on machine speed; DECISION F256 D4 rules the ratio guard instead.
- The 10k measurement must be a real run against a real fixture; a budget is
  re-derived from a re-measured maximum and never raised by hand.
<<<END PLANF256R6

<<<SLICE GATEF256R5
Gate: F256 R5 — the SIDEBAR RULING round, which discharged the deferral `DiffFileSidebar.tsx` had carried in its own header since F037. THE ROUND PASSED on every gate its block ordered, G1 through G9, and the reviewer re-ran each one independently at `08f6218a` rather than reading the handback's figures.

TRANSPORT COVERS THE EMISSION AND NOT MERELY THE WORKER'S SELF-CONSISTENCY: the reviewer's own scratch original `.remedy-wt/f256-r5-block.md` predates the worker, and the committed `.agent/authored/f256-r5.md` blob at `212af2ca` is BYTE EQUAL to it at 22380 bytes, sha256 `f69b68d7635072d23d862d8aa3134c2bf1ebf159e5a2c64ac7608c332b0429b9`. At `d3ee4aac` the authored path and `.agent/last_block.md` are ONE blob id, `6289fa93296611c447ae08f42849477cf27a2a44`.

THE RECORD AND THE LEDGER MOVED EXACTLY AS A ROUND THAT REGISTERS AND RESOLVES NOTHING SHOULD. Both appends at `4afe74f9` reconstruct byte for byte from the `78e71b3c` blob plus a newline plus their slice, each pre-round blob is a byte PREFIX, and in each a byte the reviewer's own script confirmed lies inside the FIRST appended paragraph is REJECTED. Registrations stay at 293 and all DISTINCT, `^Done: R-\d+ — ` at 43, `^Landed: R-` at 11, the OPEN SET computed AS A SET at 252, and `^Gate: F\d+ R\d+ — ` rises by exactly one to 101. `Gate: F256 R4` occurs exactly once and `R-0732` still carries no `Done:` and no `Landed:` line.

THE RULING REACHED THE SCREEN RATHER THAN ONLY THE PROSE, which is the failure a CSS module makes silent by answering `undefined` for a name with no rule. At `1b70fb02` the four classes the component names are exactly `fileMeta`, `filePath`, `statAdd`, `statDel` and every one of them is a SUBSET of the fourteen `DiffView.module.css` defines; the four custom properties the new rules name are each already defined in `apps/ui/src/styles/tokens.css`, which is BYTE UNCHANGED, so no new hue and no new property entered the product. The markup was dressed and not grown: `<span` is 6 before and 6 after, `<strong` 1 and 1, `aria-hidden` 0, every spelling `TestTheSidebarDerivesNothing` forbids is 0 both before and after, and all eight summary fields are still read.

THE RED-PROOF IS REAL, AND THE REVIEWER ADDED A THIRD MUTATION THE BLOCK DID NOT ORDER. In a disposable worktree at `d75eb339`: the unmutated control passed 16, deleting the `.statAdd` rule while the component still named the class turned the subset assertion red at exit 1, removing the `.filePath` class from the path element turned the ruled-classes assertion red at exit 1, and the control passed 16 again. The reviewer's own third mutation cut ALL FOUR rules while KEEPING the D3 comment that names all four selectors in prose — the one shape that would make the stylesheet scanner blind — and the file still went red, so `strip_css_comments` is load-bearing rather than decorative.

RE-RUN IN THE PRIMARY CHECKOUT, one pytest process at a time, each exit 0 and each equal to the handback's figure: `tests/ui_contracts/` 664 passed with 4 skipped, `tests/orchestration/test_test_runner.py` 52 passed, `tests/ui_server/` 495 passed, `tests/regression/test_resource_safety.py` 21 passed, `tests/orchestration/test_integrity_gate.py` 16 passed, the canary `tests/cli/test_golden_path.py` 42 passed, and `npx tsc --noEmit` exit 0. `apps/ui/dist` was NOT stale at review time. The branch tip equals `origin/feature/f256-diff-viewer-completion`, the primary checkout reads `git status --porcelain` empty, `git worktree list` shows the primary alone, `git ls-files .remedy-wt` is 0, and `gh pr list --state open` is `[]`.

THE ONE DEVIATION WORTH RECORDING IS ACCEPTED AND IS NOT A WEAKENING. S1 asked for the mono family with `font-feature-settings` declared AFTER any `font` shorthand; the worker used `font-family` and no shorthand at all, because a shorthand would have obliged it to invent a size and a line height for a sidebar no authority in this repository fixes, which the CANONICAL DESIGN REFERENCE banner forbids. The literal fallback stack it names is the same `ui-monospace, monospace` the rules above it use, and with no shorthand present there is nothing for `font-feature-settings` to be reset by, so the ordering clause is satisfied vacuously and the ligature rule still holds. The reviewer confirms the reasoning on the file's own bytes.
<<<END GATEF256R5

<<<SLICE DECF256D4
## DECISION F256 D4 (2026-08-28, F256 R6) — the end-to-end diff budget is guarded by a scale RATIO measured on one machine in one run, not by an absolute second count

CONTEXT. F037's Acceptance names a "10k-line fixture within the perf budget
(recorded)" and amendment A6 records that bullet as UNMET, which is why F256
carries T002. One half of the budget already exists:
`test_the_huge_diff_parses_inside_the_recorded_perf_budget` in
`tests/orchestration/test_diff_parser.py` measures the PARSER alone against an
absolute ceiling of 0.5 s, and its own docstring states the rule that ceiling was
chosen by — it must sit BETWEEN the measured linear case and where a quadratic
parser would land, or it records nothing. What has never been measured is the
whole server path: artifact on disk, parse, envelope, JSON serialisation and the
HTTP response the client actually receives.

WHAT THE REVIEWER MEASURED AT `08f6218a`, on the machine this feature is being
built on, as the median of nine runs at each size. The whole envelope path —
artifact read, parse, envelope assembly — costs 12.5 ms at 1,000 body lines,
24.5 ms at 2,000 and 123.5 ms at 10,000, while the PARSER ALONE costs 12.1 ms and
121.8 ms at the two ends of that range. Serialising the envelope adds 0.9 ms and
10.0 ms, and the serialised JSON is 102,954 and 1,045,960 bytes against artifacts
of 18,903 and 197,905. The parser is therefore about ninety-two per cent of the
whole server-side cost, and everything composed around it is the remaining eight.

THE ABSOLUTE CEILING IS ALREADY SPENT, AND SPENDING IT AGAIN GUARDS NOTHING NEW.
`HUGE_DIFF_PARSE_CEILING_SECONDS` bounds the parser at 0.5 s and its own docstring
records the rule it was chosen by. A second absolute ceiling over the endpoint
would bound that same ninety-two per cent a second time and more loosely, and its
red would be as likely to mean the runner was busy as that the code changed:
AGENTS.md already names "a stage budget too small for a slower hosted runner" as
one of the three classes of CI failure, and a bound that goes red for that reason
teaches a future session to raise it, which is the one repair this repository
forbids. What is genuinely UNGUARDED is the composition — nothing on disk today
fails if the envelope layer, the serialiser or the route stops being linear in
body lines.

CHOSEN. The end-to-end guard is a RATIO. The same route is measured at 1,000 and
at 10,000 body lines, in the same test, in the same run, on the same machine, and
the assertion is that the second median divided by the first stays under 20. A
pipeline linear in body lines answers near 10, the size ratio itself; a pipeline
quadratic in body lines answers near 100. Because both figures come off one
machine in one run, every constant factor a machine contributes — clock speed,
load, interpreter version — divides out, and the assertion cannot become a report
on machine speed however slow the runner is. A coarse absolute HANG NET of 5.0 s
on a single 10,000-line request sits beside it to catch a pipeline that stopped
answering at all rather than one that got slower; at more than forty times the
115.7 ms the route itself costs at that size it is not a budget and is not
described as one.

THE FIXED PER-REQUEST OVERHEAD MOVES THE RATIO THE SAFE WAY, and this is the
reason the ratio is sound rather than merely convenient. Server dispatch, socket
setup and JSON decoding cost the same at both sizes, so they inflate the SMALLER
median proportionally more than the larger one and the measured ratio comes out
BELOW the true algorithmic ratio. The error therefore makes the guard more
permissive and never falsely red — it can miss a mild regression, it cannot
manufacture one — which is the only direction a bound in a suite that must stay
green is allowed to err in.

BOTH DIRECTIONS WERE MEASURED BEFORE THE CEILING WAS FIXED, so 20 is a derived
number and not a taste. Over the real route at `08f6218a` the linear ratio is
7.42 — a median of 15.6 ms at 1,000 body lines against 115.7 ms at 10,000, for a
1,045,966 byte response — which sits BELOW the algorithmic 10 exactly as the
paragraph above predicts, and leaves the ceiling 2.7 times of headroom. In the
other direction, inserting one statement into the parser's per-line path that
scans the whole input on every iteration moves the PARSER's own ratio from 10.07
to 39.51 while the parse still returns 10,000 body lines and `truncated` False —
a regression that changes no answer and only costs time, which is precisely the
class of defect this guard exists for. Damped by the same fixed overhead, that
mutation reaches the route at roughly 31, so the ceiling separates the two cases
with margin on both sides. At 25 the mutated margin would have been 1.2 times,
and that is why the ceiling is 20.

ALTERNATIVES CONSIDERED. (a) A second absolute ceiling, matching the parser
test's idiom. Rejected for the reason above: it re-guards the parser's own cost
and its red is machine-shaped. For the record, a quadratic pipeline matching
today's cost at 1,000 body lines lands near 1.3 s at 10,000, so such a ceiling
would have to sit under that to separate the two cases at all. The idiom is right
for a function whose cost is nearly all algorithm and wrong for a path whose cost
includes a server. (b) An absolute ceiling above the quadratic case. Rejected
because it separates nothing and would record a number while guarding no
property. (c) Measure the parser again through the endpoint and assert nothing.
Rejected because Acceptance asks for a budget, not only a figure.

CONSEQUENCE. The recorded numbers and the guarded property become two different
things, deliberately: the docstring of the recording test carries the real
medians, the real spread and the real serialised byte size, dated and attributed
to a machine class, and the Built State of `docs/roadmap/features/T5_F256.md` will
carry them too, while the ASSERTIONS pin only what survives a change of machine.
A reader who wants to know how fast the viewer is reads the numbers; a runner that
is merely slow does not turn the suite red.

REVERSE by deleting this decision and replacing the ratio assertion with an
absolute ceiling under the quadratic figure named above, accepting that the bound
then tracks the machine. The recorded numbers are unaffected either way, because
they are a measurement and not a bound.
<<<END DECF256D4

`PLANF256R6` is a WHOLE-FILE replacement of `.agent/plan.md`. `GATEF256R5` and
`DECF256D4` are APPENDS to `.agent/live_review.md` and `.agent/decisions.md`. For
each, append exactly what gate G4 measures — the pre-round blob, one newline, then
the slice — whatever blank lines that file already ends with.

### Done when

G1 HYGIENE AND STRUCTURE. Read `.agent/STOP` with `os.path.exists` before C0a and
again before C3; report both, and stop after the commit in hand if it exists.
Report `git rev-parse HEAD` before C0a — it must equal `08f6218a` —
`git branch --show-current`, and `git status --porcelain | wc -l` after each of
C0a, C0b, C1, C2 and C3. Then, over `08f6218a..<C3>` — the range ending BEFORE the
handback commit, so `.agent/handoff.md` is expected in the change set but not in
this range — report `git diff --name-only` and both residues against the change
set with `.agent/handoff.md` set aside, printed in both directions and both
expected empty. Report each commit's insertions from `git diff --numstat`, each
under 500, and that each of C0a, C0b, C1, C2 and C3 is single-parent. Report the
counts of lines beginning `<<<SLICE ` and `<<<END ` in every target other than
`.agent/authored/f256-r6.md` and `.agent/last_block.md` — each expected 0 — beside
those two as the non-zero control. Report `git ls-files .remedy-wt | wc -l`,
expected 0, and `git worktree list` after the red-proof worktree is removed.

G2 TRANSPORT. One digest comparison: sha256 of
`git show <C0a>:.agent/authored/f256-r6.md` against the reviewer's own original at
`.remedy-wt/f256-r6-block.md`, reporting both digests, the byte length and
equality; that original predates this worker, so say the reading covers more than
self-consistency. Report that `<C0b>:.agent/authored/f256-r6.md` and
`<C0b>:.agent/last_block.md` are ONE blob id.

G3 THE PLAN AT C1. `.agent/plan.md` at C1 equals PLANF256R6 including the trailing
newline — report `True` or `False` — with `wc -l` under 50 and the counts of lines
exactly `## Goal` and exactly `## Next Steps`.

G4 THE RECORD AT C2, two readers per appended file. (a) The `08f6218a` blob plus a
newline plus the slice equals the C2 blob, reported separately for
`.agent/live_review.md` with GATEF256R5 and `.agent/decisions.md` with DECF256D4;
NEGATIVE CONTROL for each, flipping one byte at an offset your script confirms
lies INSIDE THE FIRST appended paragraph and reporting the equality now `False`.
(b) Let N be each slice's paragraph count, COUNTED BY YOUR SCRIPT from the slice
and never taken from this block, ignoring an empty trailing unit; report N and
that the LAST N blank-line units of each file match those paragraphs IN ORDER.
Report each pre-round blob is a byte PREFIX.

G5 THE LEDGER AT C2. Over the C2 blob and the `08f6218a` blob beside it, report
`^- R-\d+ — ` and whether all DISTINCT, `^Done: R-\d+ — `, `^Landed: R-`,
`^Gate: F\d+ R\d+ — `, and the OPEN SET as a set. This round registers and
resolves nothing, so every figure is UNMOVED except `^Gate: F\d+ R\d+ — `, which
rises by exactly ONE. Report that `Gate: F256 R5` occurs exactly 1 time.

G6 THE MEASUREMENT AT C3, the numbers this round exists to produce. Run the new
class alone and report, from that run: the median, minimum and maximum request
time at the Acceptance count and at the linear reference count; their RATIO; the
byte length of the serialised JSON response at the Acceptance count; and the four
pinned readings `status`, `available`, `truncated` and the summed body-line count.
State whether each figure you wrote into a docstring is the figure this run
produced. Report the value of `DIFF_VIEW_MAX_BODY_LINES` you read and that the
Acceptance count is strictly below it.

G7 THE RED-PROOF AT C3, in a disposable worktree, never in the primary checkout.
Report the UNMUTATED CONTROL FIRST, then each mutation, with exit code and
passed/failed counts, using

    ["python3", "-B", "-m", "pytest", "tests/ui_server/test_diff_endpoint.py", "-q"]

with `cwd` set to the WORKTREE. THE MUTATIONS, each applied ALONE and reverted
before the next, each of which must turn that file RED:
(i) in `packages/orchestration/diff_parser.py`, change the assignment
`DIFF_VIEW_MAX_BODY_LINES = 20_000` to `DIFF_VIEW_MAX_BODY_LINES = 5_000`, so the
Acceptance fixture truncates;
(ii) in the same file, immediately after the line `        stripped = line.strip()`
inside `parse_unified_diff_to_view`, insert one line that makes the per-line work
proportional to the WHOLE input — a scan of `diff_text` on every iteration — so
the pipeline becomes quadratic in body lines while still returning the same
answer. Report the exact line you inserted, the ratio the mutated run measured,
and WHICH assertion went red. Purge `__pycache__` in the worktree before each run.
Report the control again, green, and `git status --porcelain` inside the worktree
after the last revert.

G8 THE SUITES AT C3. One pytest process at a time, from the repository root, in
the PRIMARY checkout, each with its exit code and its own passed/failed line:
`tests/ui_server/` in full; `tests/orchestration/test_diff_parser.py`;
`tests/orchestration/test_diff_view_source.py`; `tests/ui_contracts/`;
`tests/orchestration/test_integrity_gate.py`; and the canary
`tests/cli/test_golden_path.py`. Report the WALL CLOCK of `tests/ui_server/`
beside its figure at `08f6218a`, which the reviewer measured as 495 passed in
about 30 seconds, so the cost this round adds to that suite is visible. Every one
must be exit 0. If any is red, STOP and write the handback with the FULL
untruncated failure list.

### Handback

Rewrite `.agent/handoff.md` in C4 per docs/agents/handback_template.md. It
carries: `SESSION 2 of feature F256 · round 6`; the range `08f6218a..HEAD`; a
per-commit changed-files table with `+/-` from `git diff --numstat` compared cell
by cell against G1's figures; ONE LINE PER GATE G1 through G8 with its real
result; the deviations, including every guard re-expression constraint 6 required;
the item-status table with every C-item and every gate appearing exactly once; and
the next expected action, which is the CLIENT half of the same measurement in
vitest.

Do not write a `Done:` or `Gate:` paragraph of your own anywhere — only
reviewer-authored text sets those. GATEF256R5 above is reviewer-authored and
applied as a slice, which is not the same thing.

After C4: push with `git push -u origin feature/f256-diff-viewer-completion` and
report the outcome. Do NOT create a pull request and do NOT merge anything.
