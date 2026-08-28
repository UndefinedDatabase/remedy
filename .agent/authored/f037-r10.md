# F037 R10 — book the R9 verdict, repair R-0720

## Goal

Session 3 opens. R9's verdict is booked, the defect the reviewer measured in R9's
own conformance guard is registered as `R-0720`, and the guard is repaired so the
drift its own failure message names is actually caught.

`R-0720` is not a wording complaint. The guard
`tests/ui_contracts/test_diff_surface_css.py` tells a reader, in the message of
`test_ligatures_are_off_in_the_diff_line_rule`, that "the `font` shorthand resets
this property, so the declaration must follow it", and the stylesheet's own header
comment says reordering the two "silently turns ligatures back on". Neither
sentence is enforced. The reviewer measured it at `5cba4674`, inside a disposable
worktree: moving `font-feature-settings: "liga" 0` ABOVE the `font` shorthand in
the `.diffLine` rule, changing nothing else, leaves the file at exit 0 with
`7 passed`. That is a gate over production code shown to be blind, so it earns an
id under operator amendment amend0827 rule 2, and the product effect is the one
`assets_spec.md` section 2 and amendment A4 forbid: a `!=` or a `->` in a diff
rendering as one composed glyph.

## Base

Base commit `c777fe83818ab7d4aa7c8150b2f387e562450483`, branch
`feature/f037-rendered-diff-viewer`. This is the SHA of the R9 handback this round
starts from; every range reading below is against it.

## Bundle — six commits

| Commit | Subject | Paths |
|--------|---------|-------|
| C0a | docs(agent): save the F037 R10 step block | `.agent/authored/f037-r10.md` |
| C0b | docs(agent): mirror the F037 R10 block into last_block | `.agent/last_block.md` |
| C1 | docs(agent): point the plan at the F037 R10 repair round | `.agent/plan.md` |
| C2 | docs(agent): book the R9 gate verdict and register R-0720 | `.agent/live_review.md` |
| C3 | test(ui-contracts): catch a font shorthand that resets the ligature setting | `tests/ui_contracts/test_diff_surface_css.py` |
| C4 | docs(agent): resolve R-0720 | `.agent/live_review.md` |
| C5 | docs(agent): hand back F037 R10 | `.agent/handoff.md` |

## Exact change set

Nothing outside these seven paths is written, created or deleted:

    .agent/authored/f037-r10.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    tests/ui_contracts/test_diff_surface_css.py
    .agent/handoff.md

Plus the push of `feature/f037-rendered-diff-viewer` after C5, which is ordered
explicitly here and sits outside every gate below.

## Constraints

1. A slice between its marker lines is applied BYTE FOR BYTE and is never
   edited, retyped, reflowed or trimmed — not to make a numeral in this block
   come true, and not to satisfy a cap. A slice's text already carries exactly
   one trailing newline. If a slice and a gate in this block disagree, apply the
   slice, report the measurement, and declare the contradiction under
   Deviations. A worker that edits a slice to make a number green destroys the
   only evidence that the file on disk is the reviewer's text.
2. Production code is DESCRIBED by the SPEC below, never sliced. The worker
   writes that code itself, in the idiom of the file it is editing, and reads the
   whole file before touching it.
3. No `.ts`, `.tsx`, `.jsx` or React component is written this round. The
   frontend test runner is refused in this environment and code neither role can
   execute must not be certified.
4. `docs/`, `packages/`, `apps/` and `docs/roadmap/` are NOT touched. The
   stylesheet `apps/ui/src/components/diff/DiffView.module.css` is READ by C3 and
   is not modified: the sheet on disk is already correct, and the defect is in the
   guard.
5. No existing assertion in `tests/ui_contracts/test_diff_surface_css.py` is
   weakened, deleted or renamed. C3 ADDS; the seven tests already there keep
   their names and their bodies.
6. `.agent/live_review.md` is append-only. Nothing already in it is edited,
   renumbered or deleted, and no id other than `R-0720` is registered or
   resolved.
7. No PR is created and nothing is merged. The Open PR Gate is READ and reported.
8. Every destructive check — every mutation — runs inside a disposable
   `git worktree` under `.remedy-wt/`, never in the primary checkout, and the
   worktree is removed and pruned afterwards.

## SPEC — C3, the ordering assertion

Read the whole of `tests/ui_contracts/test_diff_surface_css.py` first. It is 131
lines at the base and defines one class, `TestDiffSurfaceStylesheet`, holding
seven tests, above which sit four module-level helpers: `_strip_comments`,
`_rule_body`, `_declaration` and `_normalise`.

**S1.** Add ONE module-level helper, after the existing helpers and before the
class, named `_declaration_offset`. It takes a rule body and a property name and
returns the character offset at which that property's declaration begins, or `-1`
when the property is absent. It finds the property with the same left-boundary
guard the existing `_declaration` uses — a negative lookbehind for `[-\w]` — so
that a search for `font` does not match inside `font-size` or
`font-feature-settings`. It carries a one-line docstring in the file's own voice.

**S2.** Add ONE further module-level helper beside it, named
`_font_shorthand_after`. It takes a rule body and a character offset and returns
`True` when a `font` SHORTHAND declaration begins after that offset in that body.
It uses the same left-boundary guard. Its docstring states the WHY in one or two
sentences: the `font` shorthand resets `font-feature-settings` to its initial
value, so a `liga 0` declaration sitting ABOVE a shorthand is dead and the rule
composes ligatures anyway.

**S3.** Add ONE test method to `TestDiffSurfaceStylesheet`, after the two existing
ligature tests, named
`test_no_font_shorthand_follows_the_ligature_declaration`. For EACH of the two
selectors `.diffLine` and `.hunkHead` it takes the normalised rule body, asserts
that a `font-feature-settings` declaration is present at all, and asserts that no
`font` shorthand follows it. Both assertion messages NAME THE SELECTOR they are
about, so a failure says which rule drifted rather than only that one did.

**S4.** The second message states the consequence in the file's own register, not
merely the rule: ligatures return to the diff surface, so a `!=` or a `->` renders
as one composed glyph instead of the characters really in the file, and it cites
`assets_spec.md` section 2 the way the two existing ligature messages do.

**S5.** Nothing else changes. The module docstring, `ROOT`, the five binding
constants, the four existing helpers and the seven existing tests are untouched.

## Slices

<<<SLICE PLANF037R10
# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495`, the
merge commit of pull request #217 which closed F032.
`.agent/decisions.md` carries the DECISION series, F037 D1 through D4.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the design amendments A1 through A4.

## Current Step
R10 opens session 3. It books the R9 verdict and repairs `R-0720`, a blindness
the reviewer measured in R9's own conformance guard: the guard's failure message
names declaration ORDER as what keeps ligatures off, and the guard never checks
it, so moving `font-feature-settings` above the `font` shorthand leaves the suite
green while the diff surface composes glyphs.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R9 verdict and R-0720 | ordered | record first, before the repair |
| C3 the ordering assertion | ordered | must go red on the reorder alone |
| C4 the resolution | ordered | written after the repair is proved |
| C5 the handback | ordered | |

## Next Steps
1. R11 closes T001's last named corpus shape, the huge diff. The task slicing
   lists "huge file chunking" and no test in the corpus names one; the parser
   carries no size bound of its own, since `truncated` is only relayed from an
   upstream sentinel.
2. R12 records the same budget where the JSON is actually serialised, at the
   read endpoint.
3. T002's rendering core and all of T003 stay BLOCKED. `npx vitest`, the `npm`
   script and the direct binary were refused again while planning R10, for the
   reviewer, as they were for both roles at R8.

## Risks
- The binding CSS defines no intraline treatment while Acceptance requires
  intraline emphasis. Inventing a colour early would breach the feature file's
  own banner, so it stays a question for the round that renders spans.
- A parse budget is a number from one host. R11 must record it as a measurement
  naming its machine, never as a portable ceiling, or the suite turns flaky on a
  slower runner.
<<<END PLANF037R10

<<<SLICE GATER9
Gate: F037 R9 — the diff surface round, T002 part one, and the last round of session 2. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran all of them itself at `c777fe83` before writing this line. TRANSPORT REPRODUCES: the committed `.agent/authored/f037-r9.md` and `.agent/last_block.md` are ONE git blob `131e48d9907ca9b2e9e764d8f0c873799c04ed8a`, 25955 bytes and 383 lines at sha256 `c7face0455a87e074563b640f8837c9cc61c617e958605a4f4bc914ecf520d3a`; that chain covers the saved copy and its mirror and claims nothing about any prompt's bytes, which the handback states plainly rather than overclaiming. EXTRACTION REPRODUCES THE BLOCK'S ARITHMETIC EXACTLY: 4 slices at 49, 1, 9 and 36 content lines, CONTENT 95 against TOTAL 383, so PROSE is 288 and both caps hold. THE PLAN IS BYTE-EQUAL to PLANF037R9 with the trailing-newline negative control `False`, at 49 lines with one `## Goal` and one `## Next Steps`. ALL THREE APPENDS ARE PROVED BY BYTE IDENTITY, `result == before + b"\n" + slice`, each with its negative control `False`, and every base size the block named was measured rather than assumed: `.agent/live_review.md` 1173234, `.agent/prose_slips.md` 8992 and `.agent/decisions.md` 657352, all three exact. THE RECORD MOVED AS ORDERED AND ONLY AS ORDERED: `^- R-\d+ — ` unmoved at 280, `^Done: R-\d+ — ` unmoved at 28, `^Landed: R-` unmoved at 1, `^Gate: F\d+ R\d+ — ` at 79, `^## DECISION ` at 170 with `F037 D4` occurring exactly once, no id minted, the open set unmoved at 252, `R-0719` still in it and every id distinct. THE SUITES AND THE LINT ARE GREEN AT REAL EXIT CODES RE-RUN BY THE REVIEWER: `python3 -m pytest tests/ui_contracts/ -q` exit 0 at `587 passed, 4 skipped`, `python3 -m ruff check tests/ui_contracts/test_diff_surface_css.py` exit 0 at `All checks passed!`, and the canary `python3 -m pytest tests/cli/test_golden_path.py -q` exit 0 at `42 passed`, matching the base figure. ALL THREE RED-PROOFS REPRODUCE EXACTLY AS REPORTED, run by the reviewer in a disposable worktree at the C4 tree with `__pycache__` purged and `python3 -B` used before every run and the sheet restored and re-verified between mutations: unmutated control exit 0 at `7 passed`; the track list narrowed to two columns exit 1; the ligature declaration deleted from the `.diffLine` line alone exit 1; and the `.ln` colour token renamed to one that is not defined exit 1. THE SECOND OF THOSE IS THE ONE THAT MATTERS AND IT LANDS: exactly ONE of the two ligature tests fired while the `.hunkHead` test stayed green, so the assertion is genuinely PER RULE and not a count over the file that the surviving declaration could have masked. THE ROUND'S ONE DECLARED DEVIATION IS THE REVIEWER'S AND IT IS CORRECTLY HANDLED: the PLANF037R9 slice measures 49 lines where the block predicted 48 twice, the worker applied the slice byte for byte and reported the measurement instead of trimming a slice constraint 1 forbids it to edit, and the LOAD-BEARING clause — `.agent/plan.md` strictly under 50 — is met, so the R8 defect is genuinely repaired from 50 to 49. That is a reviewer-prose inaccuracy with no product effect, it spends no id under operator amendment amend0827 rule 2, and it earns no correction round under the same rule's fourth bullet. THE HANDBACK'S FOUR OTHER DECLARATIONS ARE ALL HONEST AND THE REVIEWER MEASURED THE LOAD-BEARING ONE: deviation 3 states in as many words that an unimported CSS module is INERT and ships in no bundle, rather than letting a committed file read as a rendered feature, and G8's reading of 0 imports across `apps/ui/src` is reproduced; deviation 4 states the guard's reach honestly by naming six properties it does NOT pin, and the reviewer CONFIRMED that claim by mutation rather than accepting it — `.ln`'s `text-align` and `padding-right` and `.hunkHead`'s `font-size` and `letter-spacing` were each drifted in the worktree and each left the file at exit 0 with `7 passed`, exactly as declared. ONE DEFECT THE ROUND HAD NO WAY TO SEE IS REGISTERED BELOW AS `R-0720`, found by the reviewer while probing that same declared reach: the guard is blind to declaration ORDER, which its own failure message names as the property that keeps ligatures off. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END GATER9

<<<SLICE FIND0720
- R-0720 — Medium, THE LIGATURE GUARD IS BLIND TO THE ONE DRIFT ITS OWN FAILURE MESSAGE NAMES. Raised by the reviewer at the F037 R9 gate while probing the reach that round declared for itself; no round was ordered to look for it. `tests/ui_contracts/test_diff_surface_css.py` asserts that `.diffLine` and `.hunkHead` each CONTAIN the declaration `font-feature-settings: "liga" 0`, by substring over the normalised rule body, and the message of the `.diffLine` test closes with "Note the `font` shorthand resets this property, so the declaration must follow it." The stylesheet's own header comment says the same thing harder: `font-feature-settings` is declared after the `font` shorthand "because the shorthand resets it; reordering the two silently turns ligatures back on." NEITHER SENTENCE IS ENFORCED, AND THE REVIEWER MEASURED THAT RATHER THAN INFERRING IT: inside a disposable worktree at the C4 tree `5cba4674`, with `__pycache__` purged and `python3 -B` used, the `.diffLine` rule was rewritten to place `font-feature-settings: "liga" 0` BEFORE the `font` shorthand and nothing else was changed — every declaration, every value and every byte of the other four rules identical — and `python3 -B -m pytest tests/ui_contracts/test_diff_surface_css.py -q` came back REAL EXIT CODE 0 at `7 passed in 0.17s`. A substring test cannot see order, and order is the whole property here. THE PRODUCT EFFECT IS THE ONE THE AUTHORITY FORBIDS: per the CSS Fonts specification the `font` shorthand resets `font-feature-settings` to `normal`, so the reordered rule composes ligatures, and a `!=` or a `->` in a diff would draw as one glyph where the source holds two characters — a reader judging a change against type that does not match the bytes. `docs/ui/design_reference/assets_spec.md:92-95` requires ligatures OFF on diff surfaces and amendment A4 of `docs/roadmap/features/T5_F037.md` names that file as one of the three binding authorities for this surface. MEDIUM AND NOT HIGH because the stylesheet on disk is CORRECT today — the reviewer confirmed the shipped order is shorthand first, ligature declaration second, in both rules — so nothing renders wrong now and no suite is red; the defect is that the guard would not stop the regression it exists to stop. NOT LOW because this is the only guard over that stylesheet, the frontend test runner is refused in this environment so no second reader exists, and a reordering is exactly the kind of edit a later formatter, minifier or well-meaning tidy-up performs without a human looking at it. THIS IS NOT `R-0719`, which is a pointer in the feature file to a design-reference section that does not exist, and it is not the six unpinned properties R9 declared under its own deviation 4: those are absences the round STATED, and the reviewer reproduced all four it could mutate, whereas this one is a property the file's own text claims to hold and does not. COUNTER-MEASURE: the guard asserts the ORDER, for both rules, by offset rather than by substring — no `font` shorthand may begin after the `font-feature-settings` declaration in the same rule body — and the assertion is red-proved against the pure reorder above, which leaves the existing substring assertions satisfied and therefore fires only on the new one. F037 R10 carries the repair. OPEN.
<<<END FIND0720

<<<SLICE DONE0720
Done: R-0720 — RESOLVED at F037 R10 by the round's C3. `tests/ui_contracts/test_diff_surface_css.py` now carries `test_no_font_shorthand_follows_the_ligature_declaration`, which reads the normalised body of `.diffLine` and of `.hunkHead`, locates each rule's `font-feature-settings` declaration by OFFSET rather than by substring, and refuses any `font` shorthand beginning after it — the property the two existing ligature messages and the stylesheet's own header comment both assert and neither enforced. Both selectors are covered because a shorthand could be introduced into either, and each assertion message names the selector it is about so a failure says which rule drifted. The repair is proved in both colours, not asserted: the pure reorder that returned exit 0 at `7 passed` when the defect was registered now returns a real exit 1, while the unmutated tree is green — so the new assertion is what fires, and the existing substring assertions, which the reorder leaves satisfied, are not doing the work. The guard's reach is unchanged in every other respect: the six properties F037 R9 declared unpinned under its deviation 4 are still unpinned, and this resolution claims nothing about them.
<<<END DONE0720

## Gates — every command is RUN and its REAL exit code recorded

Eight gates. "Green" as a word is a finding; a gate that was not executed is
reported as not executed.

**G1 hygiene.** Read `.agent/STOP` from disk BEFORE C0a and again before C5, and
report the literal reading both times — the sentinel can appear mid-session and is
otherwise invisible. Report `git rev-parse HEAD` before C0a and state whether it
equals the base above, and `git branch --show-current`. Report the LINE COUNT of
`git status --porcelain` after each of C0a, C0b, C1, C2, C3 and C4.

**G2 transport, ONE digest comparison.** After C0b, report `git rev-parse` of both
`HEAD:.agent/authored/f037-r10.md` and `HEAD:.agent/last_block.md` and state
whether they are the same blob hash. Report the sha256, byte count and line count
of the working copy of `.agent/authored/f037-r10.md`. State plainly what the chain
does and does not cover: it covers the saved copy and its mirror, and it asserts
nothing about the bytes of any prompt.

**G3 extraction and caps.** Extract every slice from the COMMITTED C0a blob by its
marker lines, in Python, and report each slice's line count, the CONTENT total,
the TOTAL line count of the blob and PROSE = TOTAL − CONTENT. State whether TOTAL
is at most 490 and PROSE at most 400. Do not carry any figure from this block's
prose into that table: measure the blob.

**G4 the plan at C1.** Report whether `.agent/plan.md` is byte-equal to the
PLANF037R10 slice, newline included, and report a NEGATIVE CONTROL comparing it
against the same slice minus its trailing newline, which must read False. Report
the count of lines exactly matching `## Goal` and of lines exactly matching
`## Next Steps`. Report `wc -l` and state whether it is STRICTLY under 50. The
binding clause is the strict inequality; if the measured count and any figure
elsewhere in this block disagree, the measurement wins and the disagreement is
declared.

**G5 the record at C2 and C4.** For each of the three appends — GATER9 and
FIND0720 at C2, DONE0720 at C4 — report the file's byte size before and after,
and TWO independent readers. Reader (a) is the BYTE IDENTITY
`result == before + b"\n" + slice`, re-read from disk. Reader (b) counts the N
blank-line-separated units in the slice and compares the LAST N units of the file
against the slice's N units IN ORDER. Report a NEGATIVE CONTROL for each append
that flips ONE byte INSIDE the first appended paragraph; BOTH readers must come
back False. `.agent/live_review.md` measures 1176292 bytes at the base — report
the measured figure beside that one and declare any disagreement.
Then report these counts over `.agent/live_review.md` after C4, line-anchored:
`^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-`, `^Gate: F\d+ R\d+ — `, the size
of the open set, whether every id is distinct, and whether `R-0720` occurs exactly
once as a registration and exactly once as a resolution.

**G6 the red-proof of the ordering assertion.** All of this runs inside a
disposable `git worktree` under `.remedy-wt/`, at the C3 tree, never in the
primary checkout; purge `__pycache__` and use `python3 -B` before EVERY run;
restore the mutated file between runs and verify the restore is byte-identical.

Report the UNMUTATED CONTROL first: `python3 -B -m pytest
tests/ui_contracts/test_diff_surface_css.py -q`, its REAL exit code and its
verbatim summary line.

Then the MUTATION, which is a PURE REORDER of the `.diffLine` rule in
`apps/ui/src/components/diff/DiffView.module.css`: the `font-feature-settings:
"liga" 0` declaration is moved to sit BEFORE the `font` shorthand within that same
rule, with every declaration, every value and every other rule byte-identical.
Report the two rule texts before and after so the reorder is visible, and report
the REAL exit code and the verbatim summary line. REPORT which node ids fail, as
measured — do not treat any predicted name or count as the gate. THE ORDERED
PROPERTY IS THE COLOUR: this mutation must be RED.

Then run the SAME mutation against the file as it stands at the BASE commit
`c777fe83` — the guard before C3 — and report its REAL exit code. This is the
negative control that proves the new assertion is what fires: at the base the
reorder is expected to be green, and if it is not, stop and declare it, because
then the defect was never real.

Afterwards report `git worktree remove`, `git worktree prune`, the line count of
`git worktree list` and the line count of `git status --porcelain` in the primary
checkout.

**G7 suite, lint and canary at C3.** ONE pytest process at a time; never two in
parallel. Report the REAL exit code and verbatim summary of each:

- `python3 -m pytest tests/ui_contracts/ -q`, and the count of lines matching
  `^FAILED`. Report an EXTRACTOR-BLINDNESS CONTROL: run the same counter over a
  control string that does begin with `FAILED` and report that it returns a
  non-zero count, so a zero above is a measurement rather than a blind spot.
- `python3 -m pytest tests/ui_contracts/test_diff_surface_css.py --collect-only -q`
  and the full node-id inventory it lists. Never derive node ids by regexing `-v`
  output.
- `python3 -m ruff check tests/ui_contracts/test_diff_surface_css.py` under the
  repository's own configuration, with NO `--isolated`.
- The canary `python3 -m pytest tests/cli/test_golden_path.py -q`. The base figure
  is `42 passed`; report the measured figure beside it and name any difference.

**G8 structure, artifacts and the Open PR Gate at C4.** Report
`git diff --name-only c777fe83..<C4>` and both RESIDUES against the change set
above minus `.agent/handoff.md`: actual minus expected, and expected minus actual.
Report `git diff --stat` restricted to `packages/`, `docs/` and `apps/` — each
must be EMPTY — and to `tests/`, which must hold only
`tests/ui_contracts/test_diff_surface_css.py`. Report per-commit insertions from
`git diff --numstat` for C0a through C4, each commit's parent count, and whether
each insertion count is under 500. Report a marker sweep of `^<<<SLICE ` and
`^<<<END ` over `.agent/plan.md` at C1 and `.agent/live_review.md` at C4, and the
SAME counter over the C0a blob, whose figures must be greater than zero so the
zeros are a measurement. Report `git ls-files .remedy-wt` line count. Report the
Open PR Gate verbatim:
`gh pr list --state open --json number,headRefName,baseRefName,isDraft`.

## Done when

C0a, C0b, C1, C2, C3, C4 and C5 are committed in that order, one commit each, the
branch is pushed, `.agent/handoff.md` is rewritten per
`docs/agents/handback_template.md` carrying the state block, the deviations, the
item-status table and the next steps, and every gate above is reported with its
REAL exit code. The handback names SESSION 3 of feature F037 and round 10.

A gate that could not be run is reported as NOT RUN with the literal refusal or
error text — never as a pass, and never worked around.
