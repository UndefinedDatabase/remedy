### STEP T001a — F256 Diff viewer completion, round 1 (THE CLAIM)

Goal: claim F256, retarget the `.agent/` state onto it, record the two rulings
the feature's shape depends on, and ship the per-line highlight MODEL that
T001's wiring will later call.

Base: `0e8ab5b4`, the tip of `main`. Every reading below was taken there.

Bundle, in commit order:

- C0a save this block verbatim to `.agent/authored/f256-r1.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 retarget `.agent/plan.md` and `.agent/context.md`, and append DECISION
  F256 D1 to `.agent/decisions.md`
- C2 the STATUS claim
- C3 the highlight model and its vitest suite
- C4 rewrite `.agent/handoff.md`

Change set — these paths and nothing else:

- `.agent/authored/f256-r1.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/context.md`
- `.agent/decisions.md`
- `docs/roadmap/STATUS.md`
- `apps/ui/src/api/diffHighlight.ts`
- `apps/ui/src/api/diffHighlight.test.ts`
- `.agent/handoff.md`

`.agent/live_review.md` is NOT edited: F037 R27 was the last round of its
branch, and docs/agents/planner_reviewer_prompt.md §4 item 13 rules that such a
round has no on-disk gate entry, so nothing is owed to the ledger this round.

### Constraints

0. BEFORE ANYTHING: run the Open PR Gate (AGENTS.md) and report its output. It
   was `[]` when this block was written; if it is not `[]` now, STOP and hand
   back without committing. Then, from `main` at `0e8ab5b4`, create and switch
   to `feature/f256-diff-viewer-completion`; every commit lands there.

1. Apply every authored slice BYTE FOR BYTE — no reflow, rewording, retitling,
   correction or shortening. If a slice looks wrong, apply it as written and say
   so in the handback's deviations; the record is repaired by a later append.
2. The delimiter lines `<<<SLICE …` and `<<<END …` are transport only and never
   reach a target file.
3. Extract every slice from the COMMITTED blob with
   `git show <C0a>:.agent/authored/f256-r1.md`, never from this prompt's text.
4. AGENTS.md binds in full: the self-review loop before every commit, one
   logical step per commit, `.agent/plan.md` current before every commit, a
   clean tree, and the push.
5. Destructive verification runs ONLY inside a disposable `git worktree` under
   the gitignored `.remedy-wt/`. The primary checkout satisfies
   `git status --porcelain` empty at every commit.
6. Shell forms rejected by this session's guard are RE-EXPRESSED, never skipped
   and never weakened. Loops, `$( )`, `${arr[0]}` and brace literals containing
   quotes are rejected by form; route such work through `python3 - <<'PY'`.
   Report every re-expression in the handback.
7. `apps/ui/src/api/diffHighlight.ts` is swept by repo-wide guards that name no
   diff path and would still fail on it. Measured at `0e8ab5b4`:
   `tests/ui_contracts/test_brain_stream_ring.py` forbids `EventSource` and
   counts `useBrainStream(` across every non-test `.ts`/`.tsx` under
   `apps/ui/src`; `tests/ui_contracts/test_ux_quality.py` forbids the substring
   `scanline`; `tests/ui_contracts/test_cost_metric_render.py` requires that no
   file but `apps/ui/src/api/costMetric.ts` contains `spent_usd`,
   `spent_tokens`, `limit_usd` or `limit_tokens`. The new module contains none
   of those strings.
8. This round adds NO CSS and edits NO component: `DiffView.tsx`,
   `DiffView.module.css` and `DiffFileSidebar.tsx` are untouched.

### SPEC — the production code of C3

Production code is DESCRIBED here, not sliced: write it in this repository's
idiom, with the one-line WHY comment above each definition that AGENTS.md's
discoverability conventions ask for.

S1. New file `apps/ui/src/api/diffHighlight.ts`. It imports nothing at runtime
and holds no module state.

S2. Export `DIFF_HIGHLIGHT_TOKEN_KINDS`, a frozen tuple naming the closed token
set: `comment`, `string`, `number`, `keyword`, `plain`. Export the union type
`DiffHighlightTokenKind` derived from it. The set is closed and small on
purpose: every kind must eventually map to a custom property already defined
under `apps/ui/src`, and a larger set invents distinctions no palette here can
honour.

S3. Export `interface DiffHighlightSegment { text: string; kind:
DiffHighlightTokenKind }`.

S4. Export `DIFF_HIGHLIGHT_GRAMMARS`, a frozen mapping built on
`Object.create(null)`, keyed by the language ids that are the VALUES of
`DIFF_SUPPORTED_LANGUAGES` in `apps/ui/src/api/diffViewModel.ts`. Each grammar
carries `lineComment: readonly string[]`, `stringDelimiters: readonly string[]`
and `keywords: ReadonlySet<string>`. Read it through
`Object.prototype.hasOwnProperty.call`, never by comparing the read value to
`undefined`. Both halves are load-bearing for the reason `diffViewModel.ts`
gives at `0e8ab5b4` above `DIFF_SUPPORTED_LANGUAGES`: the language id
originates in a diff path from a repository this viewer does not control.

S5. Export `tokenizeDiffLine(text: string, language: string | null): readonly
DiffHighlightSegment[]`.

S6. TOTAL. No input throws, for any string and any language id.

S7. THE LOAD-BEARING INVARIANT: for every input, joining the returned segments'
`text` in order reproduces `text` exactly. A highlighter that drops or
duplicates a character is worse than none, because the operator is reading the
line to judge a change.

S8. A `null` language, or one the grammar mapping does not OWN, yields a single
`plain` segment carrying the whole text. Empty text yields an empty array.

S9. Scanning is left to right and first match wins: a line-comment opener makes
the REST of the line one `comment` segment; a string delimiter opens a `string`
segment running to the next unescaped occurrence of that same delimiter or to
the end of the line; a run of digits is `number`; a run of identifier characters
is `keyword` when the grammar's set owns it and `plain` otherwise; anything else
is `plain`.

S10. Adjacent `plain` segments are MERGED, so no two consecutive segments both
carry `plain`.

S11. The module's own WHY comment records the per-line ruling and the deliberate
absence it creates, because a reader will search here for it: highlighting is
decided per LINE and never across lines. A diff omits the lines between hunks,
so block-comment and multi-line-string state cannot be carried honestly — a
viewer that tried would mark the wrong runs with confidence. Remedy deliberately
does not track cross-line highlight state.

S12. New file `apps/ui/src/api/diffHighlight.test.ts`, vitest, node
environment, named after the source it covers. It pins, each as its own test:
the S7 concatenation invariant over a table of lines covering every grammar AND
over an unknown language; that `constructor` and `__proto__` as language ids
answer a single `plain` segment rather than reaching an inherited value; that
each of the token kinds S2 names is produced by at least one input; the S10
merge rule; that an unterminated string ends at the line end; and totality over
the empty string, a whitespace-only line and a lone delimiter.

### The authored slices

<<<SLICE PLANF256R1
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
| claim F256 and retarget the state | done | this round |
| the per-line highlight model | done | `apps/ui/src/api/diffHighlight.ts` |
| compose the token cut with the intraline cut | open | model layer, not yet begun |
| lazy bundles, DiffView wiring, the palette | open | needs the composition first |
| rule on the sidebar's treatment | open | a ruling to record, not code |
| measure the 10k-line fixture | open | needs a real fixture and a real run |

## Next Steps
1. Compose the token cut with the intraline cut in the model layer, so one line
   carries both without either losing characters.
2. Ship the lazy per-language bundles and wire `loadDiffLanguageBundle` into
   `DiffView`, with a palette derived from custom properties already defined
   under `apps/ui/src` rather than invented.
3. Rule on the file sidebar's visual treatment and record the authority.
4. Measure the 10k-line fixture end to end and record the numbers in the
   feature file's Built State.

## Risks
- The palette may name only custom properties defined under `apps/ui/src`;
  `tests/ui_contracts/test_design_drift.py` fails any that is not.
- `npx vitest run` is gated under a 30-second timeout in
  `tests/orchestration/test_test_runner.py`.
<<<END PLANF256R1

<<<SLICE CTXF256R1
# Context — F256 Diff viewer completion

## Active Branch
feature/f256-diff-viewer-completion, cut from `main` at `0e8ab5b4`, the merge
commit of pull request #219.

## Scope
Feature F256, `docs/roadmap/features/T5_F256.md` — the scope DECISION F037 D11
split off F037 and operator order amend0828-daily-driver registered.
The pieces: wire the highlighting, measure the 10k-line fixture end to end and
record it, rule on the file sidebar's visual treatment.

## Do not touch
The diff JSON schema, the read endpoint, hunk-id stability (that is F033's
contract) and apply mechanics. Nothing F037 built is removed — DECISION F037
D11 says so in as many words. `docs/roadmap/ROADMAP.md` is not edited. The
server-side diff source under `packages/` is outside this feature.

## Assumptions
- No third-party syntax highlighter is reachable from this build environment,
  so DECISION F256 D1 rules that Remedy writes its own lazy bundles.
- No file under `docs/ui/design_reference/` contains the word "syntax", so no
  authority rules a token palette. The round that ships the stylesheet rules
  it, deriving it from custom properties already defined under `apps/ui/src`;
  `tests/ui_contracts/test_design_drift.py` fails any that is not.

## Constraints
The bullets in this first group are STANDING project constraints, carried
forward from the context this file replaced. They are not this feature's, and
deleting them with the rest of a rewrite is what cost an earlier round a red
CI run.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout, which satisfies
  `git status --porcelain` empty at every verdict.
- THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE. The full contract those
  readers hold over the three state files, so a rewrite is checked against it
  directly rather than rediscovered from a red: this file carries
  `## Active Branch`, a `feature/` branch name, a roadmap feature id matching
  `\bF\d{3}\b` and the word `Steps`; `.agent/plan.md` carries `## Goal`,
  `## Next Steps` and a feature id; `.agent/live_review.md` carries `Steps`.

- A `.ts` mutation red-proof follows DECISION F037 D10: vitest is spawned from
  the primary checkout so it resolves its own package there, `--root` points
  discovery at the worktree, and both flags are load-bearing.

## Steps
The item-status table for this feature lives in the `## Current Step` section
of `.agent/plan.md`. This file deliberately does not restate it — a second copy
of the map is what fell out of step and cost F022 a finding.
<<<END CTXF256R1

<<<SLICE DECF256R1
## DECISION F256 D1 (2026-08-28, F256 R1) — Remedy writes its OWN lazy syntax bundles for the diff surface rather than adding a third-party highlighter

CONTEXT. F256 T001 must wire `loadDiffLanguageBundle` into `DiffView` so a diff
of a supported language really renders highlighted. That function takes its
`importBundle` as a REQUIRED argument and names no highlighter, deliberately, so
the wiring round has to decide what the bundles ARE. Measured at `0e8ab5b4`:
`apps/ui/package.json` declares no highlighter among its dependencies or
devDependencies, and `apps/ui/node_modules` holds no shiki, prism, highlight.js
or lowlight. A registry query for a candidate package was refused by this
session class, so a new dependency can be neither installed nor verified here.

CHOSEN. The bundles are Remedy's own modules under `apps/ui/src/api/`, loaded
through the dynamic `import()` the existing importer type already describes. A
bundle is a pure tokenizer: a function from a line of text and a language id to
a list of typed segments. This keeps every decidable rule in the layer
`apps/ui/vitest.config.ts` really executes, which is DECISION F031 D5, and it
adds no dependency, no main-chunk weight and no build step.

ALTERNATIVES CONSIDERED. (a) Add shiki or prismjs. Rejected on independent
grounds: the registry is unreachable from this environment, so the change could
not be verified where it is made; and a third-party tokenizer's rules would sit
outside what any runner in this repository executes, which is the same blindness
DECISION F031 D5 exists to prevent. (b) Ship no highlighting and close F256 on
the other two pieces. Rejected because it abandons the Goal & Done clause A6
already recorded as UNMET, and a second deferral of the same clause is how a
promise stops being one.

CONSEQUENCE, stated plainly because it is a real narrowing. Remedy's
highlighting is COARSER than a full grammar — a closed token set and no semantic
analysis — which is the honest ceiling of a per-line tokenizer and enough for
helping a reader see structure in a changed line.

REVERSE by deleting this decision and the modules it authorises, and adding a
highlighter dependency once registry access exists; `loadDiffLanguageBundle`
needs no change either way, because the importer is its argument.

<<<END DECF256R1

<<<SLICE CLAIMFROM
- [ ] F256 — Diff viewer completion (highlighting wiring, 10k-line perf measurement, sidebar ruling; split off F037 by DECISION F037 D11 / amendment A6)
<<<END CLAIMFROM

<<<SLICE CLAIMTO
- [~] F256 — Diff viewer completion (highlighting wiring, 10k-line perf measurement, sidebar ruling; split off F037 by DECISION F037 D11 / amendment A6)
<<<END CLAIMTO

The CLAIM pair is a REWRITE — containment test, run before emission: `TO
contains FROM: false` — so its gate is a FROM-zero / TO-one count and never an
append obligation. `PLANF256R1` and `CTXF256R1` are WHOLE-FILE replacements.
`DECF256R1` is an APPEND to `.agent/decisions.md`, separated from the existing
final line by exactly one blank line.

### Done when

G1 HYGIENE. Read `.agent/STOP` from disk with `os.path.exists` before C0a and
again before C3; report both answers. If it exists at either reading, finish the
commit in hand, write the handback and stop. Report `git rev-parse HEAD` before
C0a — it must equal `0e8ab5b4` — `git branch --show-current`, and
`git status --porcelain | wc -l` after each of C0a, C0b, C1, C2 and C3.

G2 TRANSPORT. One digest comparison, per the gate budget. Compute sha256 of the
committed blob `git show <C0a>:.agent/authored/f256-r1.md` and of the reviewer's
own original at `.remedy-wt/f256-r1-block.md`, and report both digests, the byte
length and whether they are equal. That original was written before this worker
existed and is not the worker's output, so the reading covers more than
self-consistency; say so. Then report that
`git rev-parse <C0b>:.agent/authored/f256-r1.md` and
`git rev-parse <C0b>:.agent/last_block.md` print ONE blob id.

G3 THE STATE SLICES AT C1. Byte-equality only, per the gate budget:
`.agent/plan.md` at C1 equals PLANF256R1 including the trailing newline, and
`.agent/context.md` at C1 equals CTXF256R1 including it. Report both as `True`
or `False`, and report `wc -l` of `.agent/plan.md`, which must be under 50
(AGENTS.md). Report the count of lines exactly `## Goal` and exactly
`## Next Steps` in `.agent/plan.md`, and of lines exactly `## Active Branch` in
`.agent/context.md`.

G4 THE DECISIONS APPEND AT C1, two readers. (a) The `0e8ab5b4` blob of
`.agent/decisions.md`, plus a newline, plus DECF256R1 equals the C1 blob —
report `True` or `False`. NEGATIVE CONTROL: flip one byte at an offset your
script confirms lies INSIDE THE FIRST appended paragraph, recompute, and report
that the equality is now `False`. (b) Split the C1 blob on blank lines; let N be
the number of paragraphs in DECF256R1, COUNTED BY YOUR SCRIPT from the slice
itself and never taken from this block; report N, and report that the LAST N
units of the file match those paragraphs IN ORDER, unit by unit. Report that the
pre-round blob is a byte PREFIX of the C1 blob, with both byte lengths.

G5 THE CLAIM AT C2. Report, over `docs/roadmap/STATUS.md` at C2: the count of
CLAIMFROM (must be 0) and of CLAIMTO (must be 1); that CLAIMTO's text is present
as a WHOLE LINE and how many times; and the count of lines matching
`^- \[~\] F\d{3} — `, which `tests/docs/test_docs_consistency.py` requires to be
at most 1. Report the count of lines matching `^- \[x\] F\d{3} — ` before and
after C2 — it must be unmoved.

G6 THE MODEL RED-PROOF AT C3, in a disposable worktree, following DECISION F037
D10, never in the primary checkout. Add a worktree at C3 under `.remedy-wt/`.
Report the UNMUTATED CONTROL FIRST, in that same worktree — a control with no
baseline is not evidence — then each mutation, reporting exit code and the
passed/failed counts for every run. Drive it from `python3`, with

    ["npx", "vitest", "run", "--root", f"{WT}/apps/ui",
     "--config", f"{PRIMARY}/apps/ui/vitest.config.ts",
     "src/api/", "--reporter=basic"], cwd=f"{PRIMARY}/apps/ui"

Both flags are load-bearing and the run is SCOPED to `src/api/`; the reviewer
measured this exact recipe at `0e8ab5b4` and got control exit 0 at 588 passed
against a mutation exit 1 at 1 failed. THE MUTATIONS, each applied alone and
reverted before the next, each in `apps/ui/src/api/diffHighlight.ts` inside the
worktree, and each of which must turn the suite RED: (i) break S7 by making the
scanner drop a character it consumed; (ii) break S10 by returning adjacent
`plain` segments unmerged. Report the control again, green, with every file
restored. Report `git worktree list` and `git status --porcelain | wc -l` in the
primary after removal.

G7 THE SUITES AT C3. One pytest process at a time, from the repository root, in
the PRIMARY checkout, each with its exit code and its own passed/failed line.
`tests/orchestration/test_test_runner.py` (it spawns `npx vitest run` under a
30-second timeout, so report the wall clock too); `tests/docs/` and
`tests/orchestration/test_roadmap_index.py`, which this round's
`docs/roadmap/**` path requires; the remaining state readers `tests/ui_server/`,
`tests/regression/test_resource_safety.py` and
`tests/orchestration/test_integrity_gate.py`; the sweeps constraint 7 names,
`tests/ui_contracts/test_brain_stream_ring.py`,
`tests/ui_contracts/test_cost_metric_render.py` and
`tests/ui_contracts/test_ux_quality.py`; the diff contracts
`tests/ui_contracts/test_diff_view_model.py` and
`tests/ui_contracts/test_diff_view_render.py`; and the canary
`tests/cli/test_golden_path.py`. Every one must be exit 0. If any is red, STOP
and write the handback with the full untruncated failure list.

G8 STRUCTURE, over `0e8ab5b4..<C3>` — the range that ends BEFORE the handback
commit, because C4's own numbers cannot exist while C4 is being written. Report
`git diff --name-only` and both residues against the change set above, printed
in both directions and both expected empty. Report each commit's insertions from
`git diff --numstat`, each under 500, and report that each of C0a, C0b, C1, C2
and C3 is single-parent. Report, counted affirmatively over each file's C3
content rather than inferred from a silent grep, the number of lines beginning
`<<<SLICE ` and `<<<END ` in `.agent/plan.md`, `.agent/context.md`,
`.agent/decisions.md`, `docs/roadmap/STATUS.md`,
`apps/ui/src/api/diffHighlight.ts` and `apps/ui/src/api/diffHighlight.test.ts` —
each expected 0 — beside the same counts over `.agent/authored/f256-r1.md` as
the non-zero control. Report `git ls-files .remedy-wt | wc -l`, expected 0.

### Handback

Rewrite `.agent/handoff.md` in C4 per docs/agents/handback_template.md. It
carries: `SESSION 1 of feature F256 · round 1`; the range `0e8ab5b4..HEAD`; a
per-commit changed-files table with the `+/-` cells taken from
`git diff --numstat` and compared cell by cell against the figures G8 reports;
ONE LINE PER GATE G1 through G8 with its real result; the deviations, including
every guard re-expression constraint 6 required; the item-status table with
every C-item and every gate appearing exactly once; and the next expected
action.

Do not write a `Done:` or `Gate:` paragraph anywhere — only reviewer-authored
text sets those, and a worker-authored one is a finding however hedged.

After C4: push with `git push -u origin feature/f256-diff-viewer-completion` and
report the outcome. Do NOT create a pull request and do NOT merge anything.
