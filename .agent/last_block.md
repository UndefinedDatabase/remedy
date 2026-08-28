STEP T002 part one, the diff surface — F037 R9

Goal: the diff surface's binding CSS becomes a real stylesheet in the package,
and a Python guard makes it impossible to drift without a red. The rendering
core stays unwritten: R8 measured the frontend test runner as refused for both
roles, and code neither role can execute must not be certified.

Base: `98b4495d`. Branch: `feature/f037-rendered-diff-viewer`. SESSION 2 of
feature F037, round 9, rounds so far 8. THIS IS THE LAST ROUND OF THE SESSION.

Bundle, one commit each, in this order:
C0a  save this block verbatim to `.agent/authored/f037-r9.md`
C0b  mirror the C0a blob into `.agent/last_block.md`
C1   `.agent/plan.md` from slice PLANF037R9
C2   `.agent/live_review.md` append GATER8; `.agent/prose_slips.md` append SLIPR9
C3   `.agent/decisions.md` append DECISION4;
     `apps/ui/src/components/diff/DiffView.module.css`, new, per SPEC S1 to S4
C4   `tests/ui_contracts/test_diff_surface_css.py`, new, per SPEC S5 to S11
C5   `.agent/handoff.md`, the handback

Change set — these paths and no others:
  .agent/authored/f037-r9.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/prose_slips.md
  .agent/decisions.md
  apps/ui/src/components/diff/DiffView.module.css
  tests/ui_contracts/test_diff_surface_css.py
  .agent/handoff.md
Run `git push origin feature/f037-rendered-diff-viewer` AFTER C5. Create no pull
request and merge nothing: the Open PR Gate returned `[]` when this block was
authored.

Slice convention: the authored texts in this block are PLANF037R9, GATER8,
SLIPR9 and DECISION4. Each is delimited by a line `<<<SLICE <NAME>` and a line
`<<<END <NAME>`; the marker lines are never part of the text.

Constraints:
1. Apply every slice byte for byte, extracted from the COMMITTED C0a blob by its
   marker LINES in Python. Never retype a slice, never edit a slice.
2. `.agent/plan.md` is a WHOLE-FILE replacement by PLANF037R9. That slice is 48
   lines as authored, which repairs the 50-line file R8 left behind: AGENTS.md
   requires this file strictly under 50 and R8's slice was exactly 50, a
   reviewer authoring error already recorded.
3. GATER8 appends at EOF of `.agent/live_review.md`, SLIPR9 at EOF of
   `.agent/prose_slips.md`, DECISION4 at EOF of `.agent/decisions.md`. Every
   append uses the file's existing convention: a single separator newline, then
   the slice bytes.
4. No finding id is minted this round. R8 PASSED; its one deviation was a
   reviewer authoring error with no product effect, which goes to SLIPR9 with no
   id per operator amendment amend0827 rule 2.
5. Do NOT touch the `Landed: R-0711` line or any existing `Done:` paragraph.
6. NO `.ts`, `.tsx` and no React component is written this round, and nothing
   under `apps/ui/src` other than the ONE new `.module.css` file. The reason is
   R8's G7: `npx vitest run --root apps/ui`, `npm --prefix apps/ui run
   test:unit` and `apps/ui/node_modules/.bin/vitest run --root apps/ui` were all
   REFUSED by the environment for both the reviewer and the worker, so no
   TypeScript can be executed, red-proved or certified here.
7. Do NOT touch `packages/`, `docs/`, `apps/ui/src/styles/tokens.css`, or any
   existing file under `tests/` other than by adding the one new file.
8. Do NOT import the new stylesheet from any component. Nothing consumes it yet;
   the component that will is blocked by constraint 6, and an unimported CSS
   module is inert — Vite bundles only imported ones. Say so in the handback
   rather than wiring it to something to look finished.

SPEC — apps/ui/src/components/diff/DiffView.module.css, new file

S1. A header comment stating, in your own words, that these declarations are
    BINDING and are transcribed from the binding CSS block in the Design section
    of `docs/roadmap/features/T5_F037.md`, that amendment A4 of that file names
    the authorities, and that class names are camelCase per this package's
    CSS-module convention while the binding block's kebab-case names map
    one-for-one. Name in that comment WHY ligatures are disabled: a `!=` or a
    `->` in a diff must render as the characters that are really in the file,
    not as a single composed glyph, which is `assets_spec.md` section 2's rule
    for diff surfaces.

S2. Match this package's existing CSS-module idiom, which you must read first —
    `apps/ui/src/components/detail/DetailPopover.module.css` is a good example:
    camelCase class names, one rule per line with the body on the same line, and
    custom properties referenced as `var(--remedy-x, <fallback>)`.

S3. The rules, with these EXACT values. Every numeric and colour value below is
    transcribed from the feature file's binding CSS and must not be adjusted:
      `.diffLine`   — `display: grid`; `grid-template-columns: 56px 56px 1fr`;
                      a font shorthand giving size `12.5px` and line-height
                      `1.6` over `var(--remedy-font-mono, ui-monospace,
                      monospace)`; and `font-feature-settings: "liga" 0`.
      `.diffLine.add` — `background: rgba(56,217,169,.12)`.
      `.diffLine.del` — `background: rgba(247,103,7,.10)`.
      `.diffLine .ln` — `color: var(--remedy-ink-soft, #6f82a8)`;
                      `text-align: right`; `padding-right: 10px`;
                      `user-select: none`.
      `.hunkHead`   — `background: var(--remedy-bg-2, #f8fbff)`;
                      `color: var(--remedy-ink-soft, #6f82a8)`;
                      `padding: 4px 12px`; `font-size: 11px`;
                      `letter-spacing: .08em`; and
                      `font-feature-settings: "liga" 0`.

S4. Define NO other class. In particular define NO intraline treatment: the
    binding CSS gives none, and the feature file's banner forbids inventing a
    visual language, so that is a design question for the round that renders
    spans and not a colour to guess at now. Write that as a closing comment in
    the file, so a reader who searches for the missing rule finds the reason —
    the "deliberate absence" convention of AGENTS.md's discoverability section.

SPEC — tests/ui_contracts/test_diff_surface_css.py, new file

S5. Follow the idiom of `tests/ui_contracts/test_main_layout_guard.py`, which
    you must read first: a module docstring saying what the guard prevents,
    `from __future__ import annotations`, `ROOT = Path(__file__).resolve()
    .parent.parent.parent`, module-level path constants, and plain assertions
    inside a class. Import nothing from `apps/`.
S6. Assert the stylesheet exists at
    `apps/ui/src/components/diff/DiffView.module.css`.
S7. `.diffLine` declares `display: grid` and the exact three-column track list
    `56px 56px 1fr`. Assert the track list as its own value, not merely that the
    string appears somewhere in the file.
S8. The line rule's font is 12.5px over line-height 1.6, and it names
    `--remedy-font-mono`.
S9. The two changed-line backgrounds are exactly `rgba(56,217,169,.12)` for
    `add` and `rgba(247,103,7,.10)` for `del`. Assert both, and assert they are
    DIFFERENT from each other, so a copy-paste that gives both sides one colour
    is a red.
S10. LIGATURES ARE OFF ON EVERY DIFF SURFACE: assert `font-feature-settings:
     "liga" 0` appears in BOTH the `.diffLine` rule and the `.hunkHead` rule.
     Write the assertion per rule rather than as a count over the file, so
     moving the declaration out of one rule cannot be hidden by the other.
     Normalise whitespace around the colon before matching, so the guard pins
     the DECLARATION and not one particular spacing of it.
S11. THE CROSS-FILE GUARD, and it is the one worth the most: every
     `--remedy-*` custom property this stylesheet REFERENCES is really DEFINED
     in `apps/ui/src/styles/tokens.css`. Collect the referenced names from the
     sheet with a regular expression rather than a hand-written list, so a token
     added later is covered without editing the test, and assert the set of
     referenced names is a subset of the defined ones. Report the offending
     names in the assertion message. This is the guard that would catch a
     stylesheet built on a token that does not exist, which no visual review
     reliably catches.

Done when — eight gates. Run every one, record its REAL exit code and its
verbatim summary line, and put one line per gate in the handback.

G1 hygiene. Read `.agent/STOP` from disk before C0a and again before C5; report
   ABSENT or PRESENT at both points, and if PRESENT stop after the current
   commit and hand off. Report `git rev-parse HEAD` before C0a — it must equal
   the base above — and `git branch --show-current`. Report the
   `git status --porcelain` LINE COUNT after each of C0a, C0b, C1, C2, C3 and
   C4; each must be 0.

G2 transport, ONE digest comparison. After C0a report the sha256, byte count and
   line count of `.agent/authored/f037-r9.md`. After C0b report that
   `git rev-parse HEAD:.agent/authored/f037-r9.md` and
   `git rev-parse HEAD:.agent/last_block.md` are the SAME blob hash. State
   plainly that this chain covers the saved copy, its mirror and the working
   copy, and claims nothing about the bytes of any prompt.

G3 extraction and caps. Extract every slice from the COMMITTED C0a blob by its
   marker lines and print each slice's NAME and line count. Print TOTAL, CONTENT
   and PROSE = TOTAL − CONTENT, all as measured. PROSE at most 400, TOTAL at
   most 490.

G4 the plan at C1. `.agent/plan.md` byte-equal to PLANF037R9 under the
   newline-included convention: report True or False. Report the NEGATIVE
   CONTROL against the slice minus its trailing newline; it must be False.
   Report `^## Goal$` 1, `^## Next Steps$` 1, and `wc -l`, which must be
   STRICTLY UNDER 50 and is expected to read 48. If it does not read strictly
   under 50, say so plainly — that is the exact defect this slice exists to
   repair and it must not be reported as met.

G5 the record at C2 and the decision at C3. The base sizes are
   `.agent/live_review.md` 1173234, `.agent/prose_slips.md` 8992 and
   `.agent/decisions.md` 657352; report each measured value beside its figure.
   For EACH of the three appends report reader (a) as the BYTE IDENTITY
   `result == before + b"\n" + slice`, re-read from disk and stated as an
   identity — not a length sum with a prefix check, which cannot reject a byte
   flipped inside the appended region. Report reader (b) independently: have
   your script COUNT N, the number of blank-line units in the slice, and compare
   the LAST N units of the file against the slice's N units IN ORDER. NEGATIVE
   CONTROL per append: flip one byte inside the FIRST appended paragraph and
   report that reader (a) and reader (b) BOTH come back False.
   COUNTS after C3, line-anchored, each reported as measured:
     `^- R-\d+ — ` 280, unchanged — no id is minted this round
     `^Done: R-\d+ — ` 28, unchanged
     `^Landed: R-` 1, unchanged
     `^Gate: F\d+ R\d+ — ` 79
     `^## DECISION ` in `.agent/decisions.md` 170, with `F037 D4` occurring
     exactly once
   Report the size of the open set and confirm `R-0719` is still in it.

G6 the red-proofs for the conformance guard, run ONLY inside a disposable
   `git worktree` at the C4 tree and never in the primary checkout. Purge
   `__pycache__` and use `python3 -B` before EVERY run, and restore the
   stylesheet between mutations. Report the UNMUTATED CONTROL first —
   `python3 -B -m pytest tests/ui_contracts/test_diff_surface_css.py -q` — with
   its real exit code and verbatim summary; a colour with no baseline is not
   evidence. Then three mutations of
   `apps/ui/src/components/diff/DiffView.module.css`, each quoted exactly FROM
   and TO with the count of that string's occurrences before the edit, and for
   each the real exit code, verbatim summary and every failing node id in full:
     (a) change the track list `56px 56px 1fr` to `56px 1fr`.
     (b) delete the `font-feature-settings: "liga" 0` declaration from the
         `.diffLine` rule only, leaving the one in `.hunkHead` in place — this
         is the mutation that proves S10's per-rule assertion is really per
         rule and not a count over the file.
     (c) change `var(--remedy-ink-soft, #6f82a8)` to
         `var(--remedy-ink-nonexistent, #6f82a8)` in the `.ln` rule — this
         proves the S11 cross-file token guard bites.
   If any mutation comes back GREEN, report the green plainly and diagnose WHY
   the assertion did not fire. Do NOT substitute a different mutation and do NOT
   change a test to make it red. Remove and prune the worktree afterwards and
   report `git worktree list` line count and `git status --porcelain` line count
   in the primary checkout.

G7 suite, lint and canary at C4, in the primary checkout, ONE pytest process at
   a time and never two in parallel.
   Run `python3 -m pytest tests/ui_contracts/ -q`; report the real exit code,
   the verbatim summary line and the count of lines matching `^FAILED`. Add the
   extractor-blindness control: run the SAME counter over a control string
   containing
   `FAILED tests/ui_contracts/test_diff_surface_css.py::test_control_string`
   and report that it returns 1, so a 0 above is a measurement and not a blind
   spot. Report the whole-directory figure as measured; if it is red, report the
   failures rather than narrowing the selection until it is green.
   Report the node-id inventory of the new file from
   `python3 -m pytest tests/ui_contracts/test_diff_surface_css.py --collect-only -q`
   — the count and the ids. Never derive node ids by regexing `-v` output.
   Run `python3 -m ruff check tests/ui_contracts/test_diff_surface_css.py` with
   the repository's own configuration and NO `--isolated`; report the real exit
   code and the verbatim output.
   Run the canary `python3 -m pytest tests/cli/test_golden_path.py -q`, measured
   GREEN at the base at `42 passed`; report the real exit code and verbatim
   summary, and report any difference rather than explaining it away.

G8 structure, artifacts and the Open PR Gate, measured at C4.
   Report `git diff --name-only <base>..<C4>` against the change set above minus
   `.agent/handoff.md`, and report BOTH residues — actual minus expected and
   expected minus actual — each of which must be empty.
   Report a restricted `git diff --stat`: `packages/` and `docs/` EMPTY;
   `apps/` holding only `apps/ui/src/components/diff/DiffView.module.css`;
   `tests/` holding only `tests/ui_contracts/test_diff_surface_css.py`.
   Report the per-commit INSERTION count from `git diff --numstat` for C0a, C0b,
   C1, C2, C3 and C4 — not for C5, whose own count cannot exist while its text
   is being written — and confirm each commit is single-parent and each
   insertion count is under 500.
   Report the line-anchored counts of `^<<<SLICE ` and `^<<<END ` in
   `.agent/plan.md` at C1 and `.agent/live_review.md` at C2; both must be 0.
   Then run the SAME counter over the C0a blob and report the number it
   measures, which must be greater than zero, so the sweep is not blind.
   Report the count of `import` statements naming the new stylesheet across
   `apps/ui/src`, which must be 0 — constraint 8 forbids wiring it, and this is
   the reading that proves the constraint was kept rather than asserted.
   Report `git ls-files .remedy-wt` line count, which must be 0.
   Report the Open PR Gate verbatim:
   `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
   The PUSH is ordered after C5 and is deliberately NOT part of any gate: C5
   writes the handback, so the handback cannot report a value that does not
   exist when it is written. Run the push, and do not name its result in
   `.agent/handoff.md`; the reviewer reads the remote tip itself.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It
carries the Session block naming SESSION 2 of feature F037 and round 9, and
states plainly that THE SESSION ENDS HERE and why — R9 was ordered as the last
round of the session. Include the range and base SHA, a per-commit changed-files
table with a `+/-` column taken from `git diff --numstat` itself and agreeing
cell for cell with the per-commit reading G8 orders, the external actions, one
line per gate G1 through G8 with its real result, the item-status table covering
every C-item, every S-item and every gate with `done`, `skipped` or `deviated`
plus a reason, the Deviations, and the Next section. It has NO length cap.
In the Next section, FIRST and unmissably, state that the frontend test runner
is refused in this environment for both roles, that R8's G7 measured all three
routes, and that T002's rendering core and all of T003 are BLOCKED on the
operator permitting one of them — that is the single thing the next session most
needs to know. Then state that the first action of the next round is to re-read
`.agent/STOP` from disk, then the Open PR Gate.

<<<SLICE PLANF037R9
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
R9 lands the half of T002 this environment can actually verify: the diff surface
stylesheet, transcribed from the feature file's binding CSS, and a Python
conformance guard over it in `tests/ui_contracts/`, which is how this repository
already pins frontend CSS. The rendering core stays unwritten because the
frontend test runner is REFUSED here for both roles, measured at R8 — code that
neither role can execute must not be certified.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit, repairs its own cap |
| C2 the R8 gate and the slip | ordered | record first |
| C3 DECISION F037 D4 and the stylesheet | ordered | the choice beside what it governs |
| C4 the conformance guard | ordered | must go red when the sheet drifts |
| C5 the handback | ordered | last round of the session |

## Next Steps
1. UNBLOCK THE RUNNER. `npx vitest run --root apps/ui`, `npm --prefix apps/ui
   run test:unit` and the direct binary were all refused at R8. Until one is
   permitted, no `.ts`, `.tsx` or React component of T002 can be verified, and
   none is ordered.
2. T002's rendering core as a pure `.ts` view-model beside its `.test.ts`, the
   only shape this package tests: `apps/ui/vitest.config.ts` sets
   `environment: "node"` and there is no jsdom and no testing library.
3. T003 sidebar, virtual scrolling, lazy languages and the L3 tab.

## Risks
- The binding CSS defines no intraline treatment, and Acceptance requires
  intraline emphasis. That is a design question for the round that renders
  spans; inventing a colour early would breach the feature file's own banner.
- `R-0711` carries a `Landed:` line and no `Done:` text because F032's branch
  ended first. It is the terminator case, not a gap for F037 to close.
- No bundle-size budget exists in `tests/` or `apps/ui/vite.config.ts`, so T003
  would be creating that ceiling rather than satisfying one.
<<<END PLANF037R9

<<<SLICE GATER8
Gate: F037 R8 — the preparation round, and the round whose most valuable output is a REFUSAL it was ordered to measure rather than to work around. THE ROUND PASSED on the seven gates that could be met and DECLARED the one that could not, and the reviewer re-ran the load-bearing ones itself at `98b4495d`. THE PROBE IS THE HEADLINE: `npx vitest run --root apps/ui`, `npm --prefix apps/ui run test:unit` and `apps/ui/node_modules/.bin/vitest run --root apps/ui` were each attempted and each REFUSED before execution with `This command requires approval`, so no exit code exists for any of them and none was claimed. That reproduces the reviewer's own three refusals exactly, which is what makes the reading a property of the ENVIRONMENT rather than of one role's permissions, and it is why no TypeScript was ordered this round or the next: code that neither the worker nor the reviewer can execute cannot be red-proved, and certifying it would be the unverified-completion-claim block condition rather than a shortcut. THE DOCS GATE AND THE CANARY BOTH RAN AND BOTH MATCH THE BASE: `python3 -m pytest tests/docs/ -q` exit 0 at `295 passed` and `python3 -m pytest tests/cli/test_golden_path.py -q` exit 0 at `42 passed`. THE SPEC REPAIR IS REAL AND THE REVIEWER RE-MEASURED ITS PREMISE RATHER THAN TRUSTING IT: `docs/ui/design_reference/ux_spec.md` contains the string `diff` ZERO times, case-insensitively, at `98b4495d`, so the feature file's banner really did send every UI builder of this feature to a section that does not exist; amendment A4 now names the three authorities that do — the feature file's own binding CSS, `component_spec.md:113-116` and `assets_spec.md:92-95` — and DECISION F037 D3 records the choice, the three alternatives and how to reverse it. THE RECORD MOVED AS ORDERED: `^- R-\d+ — ` 279 to 280, `^Done: R-\d+ — ` 27 to 28, `^Landed: R-` 2 to 1, `^Gate: F\d+ R\d+ — ` 77 to 78, `^## DECISION ` 168 to 169 with `F037 D3` occurring exactly once, the single id added being `R-0719`, exactly `R-0715` resolved, all ids distinct and the open set unmoved at 252. ONE DEVIATION IS DECLARED AND IT IS THE REVIEWER'S: G4 ordered `.agent/plan.md` strictly under 50 lines while the PLANF037R8 slice was authored at exactly 50, so the two clauses could not both be met; the worker kept byte-equality with the authored text, reported the count as measured and refused to trim a slice constraint 1 forbids it to edit — which is the correct precedence, because a worker that edits a slice to make a number green destroys the only evidence that the file on disk is the reviewer's text. The file was left one line over AGENTS.md's rule for the length of one round and is repaired by the R9 slice, and the authoring failure is recorded in `.agent/prose_slips.md` with no id: `.agent/plan.md` is not one of the paths operator amendment amend0827 rule 2 reserves an id for. NO BLOCK CONDITION AROSE: nothing fabricated, no false live indicator, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END GATER8

<<<SLICE SLIPR9
- 2026-08-28 · F037 R8 · The PLANF037R8 slice was authored at exactly 50 lines
  while the same block's G4 ordered `.agent/plan.md` strictly under 50, so the
  block contained two clauses no worker could satisfy together and the file sat
  one line over AGENTS.md's rule for a round. Checklist item 3 requires every
  authored full-replacement text to be counted against its own file's cap BEFORE
  emission; the count was carried over from an earlier round's slice instead of
  being re-measured after the last edit, which is the staleness shape the
  checklist already names. A cap is re-measured on the FINAL bytes of the slice
  that will land, never inherited from the slice it was adapted from.
<<<END SLIPR9

<<<SLICE DECISION4
## DECISION F037 D4 — the diff surface takes its mono family from `--remedy-font-mono`, keeping the binding CSS's stack as the fallback (2026-08-28, F037 R9)

CONTEXT. Two authorities named by amendment A4 speak to the diff surface's font
and they do not say the same thing. The binding CSS block in
`docs/roadmap/features/T5_F037.md` writes the shorthand
`font:12.5px/1.6 ui-monospace,monospace`, naming a literal family stack.
`docs/ui/design_reference/assets_spec.md:90-93` defines `--remedy-font-mono` as
the canonical mono token and names the diff viewer as one of its usages. Every
other stylesheet in `apps/ui/src/components/` references families and colours
through `var(--remedy-*, <fallback>)` rather than through literals.

CHOSEN. Write the shorthand as
`font: 12.5px/1.6 var(--remedy-font-mono, ui-monospace, monospace)`. The size
`12.5px` and the line-height `1.6` are taken from the binding CSS unchanged;
the family resolves to the design reference's token when it is defined, and
falls back to exactly the stack the binding CSS names when it is not. Both
authorities are then satisfied by one declaration and neither is contradicted.
This is not treated as a visual deviation requiring an assumption-log entry:
the token's own stack is monospace throughout, and the size, line-height and
weight the binding CSS fixes are untouched — what changes is the mechanism by
which the family is named, not the type that renders.

ALTERNATIVES CONSIDERED. (a) Transcribe `ui-monospace, monospace` literally.
Rejected: it pins the diff surface to a different family from every other mono
surface in the package the moment the token changes, which is the synonym drift
AGENTS.md's discoverability section forbids, and it ignores an authority A4
itself names. (b) Use `var(--remedy-font-mono)` with no fallback. Rejected: a
stylesheet that renders proportional text when one token is missing fails in
the worst direction for a diff, where column alignment carries meaning.
(c) Add a diff-specific font token. Rejected: a second spelling for one concept,
and `assets_spec.md` is the operator's artifact and already answers the question.

REVERSE by replacing the `font` declaration in
`apps/ui/src/components/diff/DiffView.module.css` with the binding CSS's literal
shorthand, deleting this decision, and relaxing the corresponding assertion in
`tests/ui_contracts/test_diff_surface_css.py`.
<<<END DECISION4
