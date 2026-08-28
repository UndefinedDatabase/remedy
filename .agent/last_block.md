STEP T002 — F037 Rendered diff viewer — ROUND 15

Goal: start T002. Three rounds of this feature recorded T002 and T003 as BLOCKED
on a refused frontend test runner, and that premise is false: the runner is
reachable through this repository's own pytest gate. This round rules that in a
DECISION, repairs the two shipped comments that assert it and the superseded
read bound, and lands the first half of the rendering core — the PURE view model
the renderer will draw, in the one layer vitest reaches.

Base: the round starts from `0d750765` on branch
`feature/f037-rendered-diff-viewer`. Nothing else is in flight.

Bundle, one commit each, in this order:
- C0a save this block verbatim to `.agent/authored/f037-r15.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 apply PLANF037R15 to `.agent/plan.md`
- C2 append GATER14, FIND0723 and FIND0724 to `.agent/live_review.md`
- C3 append DECISION8 to `.agent/decisions.md` and write SPEC S1 and S2 — the
  two stale-claim repairs — into `packages/orchestration/diff_parser.py` and
  `tests/ui_contracts/test_diff_surface_css.py`
- C4 write SPEC S3 through S9 into a NEW file
  `apps/ui/src/api/diffViewModel.ts`
- C5 write SPEC S10 into a NEW file `apps/ui/src/api/diffViewModel.test.ts`
- C6 write SPEC S11 into a NEW file
  `tests/ui_contracts/test_diff_view_model.py`
- C7 append DONE0723 and DONE0724 to `.agent/live_review.md`
- C8 rewrite `.agent/handoff.md` as the handback

Change set, and nothing outside it: `.agent/authored/f037-r15.md`,
`.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
`.agent/decisions.md`, `.agent/handoff.md`,
`packages/orchestration/diff_parser.py`,
`tests/ui_contracts/test_diff_surface_css.py`,
`apps/ui/src/api/diffViewModel.ts`, `apps/ui/src/api/diffViewModel.test.ts`,
`tests/ui_contracts/test_diff_view_model.py`. Push the branch after C8. Create
no PR, merge nothing.

Constraints:
1. A slice between the markers is applied BYTE FOR BYTE. Never edit a slice,
   never reflow it, never fix a typo in it. If a slice looks wrong, apply it and
   say so in the handback's Deviations.
2. Production code and test code are DESCRIBED by the SPEC below, not sliced.
   Write them yourself, in each language's local idiom. `apps/ui/src/api/` is
   TypeScript with a heavy WHY-comment style and total functions —
   `decisionOrder.ts` and `decisionOrder.test.ts` are the models to follow, down
   to `import { describe, it, expect } from "vitest"`.
3. NO BEHAVIOUR of `packages/orchestration/diff_parser.py` changes. S1 edits
   COMMENT TEXT only: after C3 the file's Python statements are byte-identical
   to `0d750765`, and the handback proves that by comparing the two blobs with
   every `#`-comment line and docstring removed.
4. `packages/orchestration/diff_view_source.py`, `ui_server.py` and every test
   under `tests/orchestration/` are NOT touched.
5. Nothing under `apps/ui/src/components/`, no `.css` file and no existing
   `apps/ui` file is touched. C4, C5 and C6 create three NEW files and change no
   existing one.
6. `apps/ui/src/api/diffViewModel.ts` imports NOTHING — not React, not a `.css`
   module, not another `src/api` module. It is pure data in, pure data out. That
   is what keeps it inside what `apps/ui/vitest.config.ts` reaches, which
   collects `src/**/*.test.ts` in a NODE environment with no DOM.
7. Ruff runs under this repository's own configuration — line length 120, rules
   `E`, `F`, `W`, `I`, `UP`. Never `--isolated`.
8. Every destructive check runs inside a disposable `git worktree` under
   `.remedy-wt/`, never in the primary checkout, which reads
   `git status --porcelain` empty after every commit.
9. C7 runs after C3, C4, C5 and C6. DONE0723 and DONE0724 state what this round
   landed, so the commit order is what makes them true.
10. NO RED-PROOF IS ORDERED FOR THE TYPESCRIPT, and the reason is measured
    rather than assumed — see gate G6. Do not invent one: a colour taken from a
    command that cannot pass is not evidence.

SPEC — the two stale-claim repairs

S1. `packages/orchestration/diff_parser.py`, in the comment block above
    `DIFF_VIEW_MAX_FILES`. Its DELIBERATE ABSENCE paragraph currently says that
    `packages/orchestration/diff_view_source.py` "still reads the artifact WHOLE
    before this function is called, and that is where the bound on the INPUT
    belongs". That was true when it was written and is false at `0d750765`.
    Replace that clause so the paragraph says what is now true: the two ceilings
    here bound the OUTPUT this module BUILDS, the INPUT is bounded separately by
    `DIFF_VIEW_MAX_ARTIFACT_BYTES` in `diff_view_source.py` under DECISION F037
    D7, and the two are different resources in different units so neither
    subsumes the other. Change nothing else in that block, and change no
    statement anywhere in the file.

S2. `tests/ui_contracts/test_diff_surface_css.py`, module docstring. It
    currently reads "the frontend test runner cannot be executed in this
    environment, so the conformance of this stylesheet is pinned from Python".
    The first half is false — see DECISION F037 D8 — while the CONCLUSION is
    right for a reason the sentence never gives. Replace the clause with the
    real reason: `apps/ui/vitest.config.ts` collects `src/**/*.test.ts` in a
    NODE environment, so the runner reaches no stylesheet and no markup whatever
    its availability, which is why this conformance is pinned from Python.
    Change nothing else in the file, and change no assertion.

SPEC — `apps/ui/src/api/diffViewModel.ts`, a NEW file

S3. A module comment opening the file, in the style of `decisionOrder.ts`: this
    is the PURE half of F037's rendering core, the endpoint's diff envelope
    turned into the rows a renderer draws; it holds no markup and no fetch
    because DECISION F031 D5 keeps decidable rules in the layer the shipped
    vitest config reaches; and Remedy deliberately does NOT re-sort files or
    hunks here — the server's order is the reading order, and `diff_parser.py`
    preserves input order on purpose.

S4. Exported TypeScript types for what the endpoint sends, named after the
    contract they mirror: a line (`kind`, `oldLn`, `newLn`, `content`,
    `intraline`), a hunk (`id`, `header`, `oldStart`, `newStart`, `lines`), a
    file (`path`, `oldPath`, `status`, `stats` with `added` and `deleted`,
    `note`, `hunks`), and the envelope (`version`, `scope`, `taskId`, `source`,
    `available`, `reason`, `truncated`, `files`, `taskRunIds`). The wire form is
    snake_case and this module's form is camelCase; that translation is
    `readDiffEnvelope`'s job and is the reason it exists.

S5. `export function readDiffEnvelope(raw: unknown): DiffEnvelope`. TOTAL: no
    input makes it throw, and anything it cannot trust becomes the same answer
    an absent artifact gives — `available` false, `files` empty. It reads BOTH
    spellings of every field that has two (`task_run_ids` and `taskRunIds`, and
    so on), the way `remedyApi.ts` already does; a line whose `kind` is not one
    of the three the contract names is DROPPED rather than rendered as
    something; `intraline` defaults to the empty array; `truncated` is true only
    when the wire value is literally true. State in a WHY comment that this is
    where a malformed payload stops, so no function below it has to be
    defensive twice.

S6. `export const DIFF_HUNK_COLLAPSE_THRESHOLD_LINES = 200`, with the WHY the
    feature file's "collapsed by default beyond a size threshold" does not give:
    the binding CSS sets `.diffLine` at `12.5px/1.6`, so a line is twenty
    pixels and two hundred of them is roughly four thousand — several screens of
    one hunk, which is the point at which an open hunk stops being a reading aid
    and becomes a wall to scroll past. Declared once, here, and referenced by
    name everywhere else including the tests.

S7. `export function defaultCollapsedHunkIds(envelope: DiffEnvelope):
    Set<string>` — the ids of every hunk carrying MORE than
    `DIFF_HUNK_COLLAPSE_THRESHOLD_LINES` lines. Exactly the threshold is OPEN;
    the boundary is inclusive the same way both parser ceilings are.
    `export function toggleHunkCollapse(collapsed: ReadonlySet<string>, hunkId:
    string): Set<string>` returns a NEW set and never mutates its argument, for
    the reason `orderDecisionInbox` gives for not sorting in place.

S8. `export function buildDiffRowModels(envelope: DiffEnvelope, collapsed:
    ReadonlySet<string>): DiffRowModel[]` — one FLAT array, in the envelope's
    own order, of rows discriminated by a `kind` field of `"file"`, `"hunkHead"`
    or `"line"`. Every row carries a `key` that is unique across the whole array
    and stable under collapse: derive it from the server's own hunk `id`, which
    `diff_parser.py` assigns as `"<fileIndex>:<hunkIndex>"`. A COLLAPSED hunk
    emits its head row and NONE of its line rows, and its head row says how many
    lines it is hiding so the renderer can label it without a second pass. A
    file with no hunks — a binary marker, a pure rename — still emits its file
    row, because the sidebar and the body must agree on which files exist.
    Note in a comment that hunk ids are PROVISIONAL and F033 replaces them with
    content-hash ids, which is what the envelope's `version` field is for.

S9. `export function buildDiffFileSummaries(envelope: DiffEnvelope):
    DiffFileSummary[]` — one entry per file, in the envelope's order, carrying
    the path, the added and deleted counts, the hunk count, the note, and the
    `key` of that file's own row so a sidebar click can find its row without
    recomputing anything. This is the file sidebar T003 renders; it is built
    here because it is decidable and therefore testable.

SPEC — `apps/ui/src/api/diffViewModel.test.ts`, a NEW file

S10. Vitest tests, `describe` per exported name, covering at least: a
    well-formed envelope round-trips through `readDiffEnvelope` with both wire
    spellings; a malformed payload — a string, null, a `files` that is not an
    array, a line with an unknown `kind` — yields the unavailable envelope or
    drops the line rather than throwing; the collapse threshold is exercised on
    BOTH of its sides, at exactly `DIFF_HUNK_COLLAPSE_THRESHOLD_LINES` and at
    one more, referencing the constant by name and never repeating its literal;
    `toggleHunkCollapse` leaves its input set unchanged and returns the opposite
    membership; `buildDiffRowModels` emits every line of an open hunk and none
    of a collapsed one while still emitting its head, keeps every `key` unique
    across a two-file envelope, and emits a file row for a file with no hunks;
    and `buildDiffFileSummaries` reports one entry per file with the stats the
    envelope carries. Each `it` names the property rather than the function.

SPEC — `tests/ui_contracts/test_diff_view_model.py`, a NEW file

S11. A Python guard reading the two new TypeScript files AS TEXT, importing
    nothing from `apps/`, with a module docstring stating what it is for: vitest
    proves the module's BEHAVIOUR, and this proves the two structural facts
    vitest cannot see about itself. Assert, each with a message naming its
    authority: (a) `diffViewModel.ts` contains no `import` statement at all and
    no `.tsx`-only construct, because constraint 6's rule — the module stays in
    the layer the node-environment vitest config reaches — is invisible to
    vitest itself, which passes just as happily on a module it cannot load in a
    browser; (b) every name the module exports appears in `diffViewModel.test.ts`,
    computed by scanning the module for `export function` and `export const` and
    checking each against the test file's text, so a later export cannot ship
    untested; (c) `DIFF_HUNK_COLLAPSE_THRESHOLD_LINES`'s numeric literal occurs
    EXACTLY ONCE across the two files, which is what stops the threshold from
    drifting between the rule and its tests. Derive the export set from the
    module rather than listing it here, so the guard grows with the module.

Slice convention: each authored text sits between a line beginning `<<<SLICE `
and a line beginning `<<<END `, both carrying the slice's name. The marker lines
are NEVER written into any target file. The slices are PLANF037R15, GATER14,
FIND0723, FIND0724, DECISION8, DONE0723 and DONE0724.

<<<SLICE PLANF037R15
# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495` (the
merge of PR #217, which closed F032). `.agent/decisions.md` holds F037 D1 to D8.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the design amendments A1 through A4.

## Current Step
R15 starts T002 and corrects the premise that stopped it. DECISION F037 D8
records that the frontend runner IS reachable here — through
`tests/orchestration/test_test_runner.py`, which runs `npx vitest run` from
pytest — and that the build pattern is this repository's own: decidable rules in
`apps/ui/src/api/` where vitest reaches them, markup and stylesheets pinned from
`tests/ui_contracts/`. The round lands `diffViewModel.ts`, its vitest tests and
a structural guard, and repairs two shipped comments that assert otherwise
(`R-0723`, `R-0724`).

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R14 verdict and two registrations | ordered | record first |
| C3 DECISION F037 D8 and both comment repairs | ordered | the choice beside what it governs |
| C4/C5 the view model and its vitest tests | ordered | the decidable half of the core |
| C6 the structural guard | ordered | what vitest cannot see about itself |
| C7 the resolutions | ordered | written after the repairs are proved |
| C8 the handback | ordered | |

## Next Steps
1. The round after this one renders: the `DiffView` component over these row
   models, the hunk-head and line markup against the binding CSS, and the entry
   point `component_spec.md` names — `onOpenDiff(taskId)` from `DetailPopover`.
   Its behaviour is pinned by `tests/ui_contracts/`, its rules by vitest here.
2. T003 — the sidebar over `buildDiffFileSummaries`, virtual scrolling beyond
   two thousand lines, lazy language bundles, the L3 tab — is the last slice.

## Risks
- Round 15 of a 25-round soft limit with T002 and T003 both unfinished. If the
  component does not land next round, the handback after it carries a scope
  report proposing a split rather than another step.
- The binding CSS defines no intraline treatment while Acceptance requires it,
  so that stays a question for the round that renders spans.
<<<END PLANF037R15

<<<SLICE GATER14
Gate: F037 R14 — the round that closed the remaining half of `R-0721` by bounding the artifact READ. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran all of the load-bearing ones itself at `0d750765`. TRANSPORT IS PROVED FROM A VALUE THE REVIEWER HELD BEFORE DELEGATING: the block was written to the gitignored scratch `.remedy-wt/f037-r14-block.md` and measured there at sha256 `19ac258925457ddf3b82dcd29751ae49e72854b8ba10cdf03c572025df09e6fc` over 32272 bytes and 419 lines, and the committed `.agent/authored/f037-r14.md` is byte-identical to that original, with the saved copy and `.agent/last_block.md` ONE git blob `af7b2387e3c27925a085f7e1737e6b4a77c5d44b`. EXTRACTION REPRODUCES: slices at 49, 1, 75 and 1 content lines, CONTENT 126 against TOTAL 419, PROSE 293, both caps holding. THE PLAN IS BYTE-EQUAL to PLANF037R14 with the trailing-newline control False, at 49 lines. THE RECORD MOVED AS ORDERED: registrations unmoved at 283 and all distinct, `^Done: R-\d+ — ` 31 to 32, `^Landed: R-` unmoved at 1, `^Gate: F\d+ R\d+ — ` 83 to 84, open set unmoved at 252, and `.agent/decisions.md` at 173 headings with `F037 D7` exactly once. THE REPEATED RESOLUTION ID IS DELIBERATE AND MEASURED: 32 resolution lines over 31 distinct ids, the repeat being `R-0721`, which is the second paragraph closing the half F037 R12 left open — the shape the round was ordered to produce and to declare. THE CODE MATCHES THE SPEC WITHOUT DRIFT: the read is `handle.read(DIFF_VIEW_MAX_ARTIFACT_BYTES + 1)` in binary, the cut is to the ceiling and then back through `raw.rfind(b"\n") + 1`, the flag is `parsed["truncated"] or read_truncated`, and the existing `except (OSError, UnicodeDecodeError)` handler and the `DIFF_REASON_ARTIFACT_MISSING` branch are untouched, so an unreadable artifact still arrives as the same named absence. THE TESTS PIN THE HAZARDS RATHER THAN DESCRIBING THEM, which is the part worth recording: the partial-line fixture asserts that the bytes on BOTH sides of the cut point are not newlines, and the multi-byte fixture asserts that the first byte the cut would drop satisfies `0x80 <= byte < 0xC0`, so neither fixture can silently stop exercising its case. THE SUITES AND THE LINT ARE GREEN AT REAL EXIT CODES RE-RUN BY THE REVIEWER: `python3 -m pytest tests/orchestration/test_diff_view_source.py -q` exit 0 at `15 passed in 0.26s` against the base `9 passed in 0.21s`, the whole rise being the one test that writes an eight-megabyte artifact; `python3 -m pytest tests/orchestration/test_diff_parser.py tests/ui_server/test_diff_endpoint.py -q` exit 0 at `49 passed`, UNMOVED, which is what constraints 3 and 4 asked for; and ruff exit 0 at `All checks passed!`. ALL FIVE ORDERED RED-PROOFS REPRODUCE, run by the reviewer in a disposable worktree at `0d750765` with `python3 -B`, each replaced string counted at exactly 1 and the module restored and re-hashed to `35ee01c1c8acf21b1b142cff8a2065ab39db4c4ed4ec51f088d7c7a5e97b6644` after every run: control exit 0 at `15 passed`; `>` to `>=` exit 1 killing exactly the boundary test; dropping the newline cut-back exit 1 killing exactly the two hazard tests; dropping the read source from the flag exit 1 at `4 failed`; dropping the parser source from it exit 1 killing exactly the OR discriminator. THE REVIEWER ADDED A SIXTH THE BLOCK DID NOT ORDER, because the `+ 1` in the read is load-bearing and nothing else pins it: reading exactly `DIFF_VIEW_MAX_ARTIFACT_BYTES` instead of one more is exit 1 at `4 failed, 11 passed`, so the inclusive boundary cannot be broken silently. THE WORKER'S DECLARED DEVIATIONS ARE HONEST AND TWO ARE SUBSTANTIVE: the test module's IMPORT BLOCK had to change, which constraint 6 did not foresee, and the worker proved the nine existing tests byte-identical by showing the base file's tail survives as one contiguous substring rather than asserting it; and the parser appends one trailing EMPTY body line when a cut hunk still has lines outstanding in its header, which the worker reported as pre-existing behaviour and asserted exactly rather than filtering — the reviewer confirmed it at `0d750765` on a four-line hunk header carrying two lines, where the parsed contents are `alpha`, `beta` and the empty string with `truncated` False, so the behaviour is the parser's and not the cut's. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END GATER14

<<<SLICE FIND0723
- R-0723 — Low, A SHIPPED COMMENT IN THE PARSER TELLS A READER THE OPPOSITE OF WHAT THE CODE DOES, AND IT SITS ON THE CONSTANT IT IS WRONG ABOUT. Raised by the reviewer at the F037 R14 gate; the worker found it first, declared it under its own Deviations, and correctly minted no id because constraint 3 of the R14 block forbade the edit. The DELIBERATE ABSENCE paragraph above `DIFF_VIEW_MAX_FILES` in `packages/orchestration/diff_parser.py` reads, at `0d750765`, that `packages/orchestration/diff_view_source.py` "still reads the artifact WHOLE before this function is called, and that is where the bound on the INPUT belongs". THAT SENTENCE WAS TRUE WHEN F037 R13 WROTE IT AND F037 R14 FALSIFIED IT ONE ROUND LATER: `build_diff_view` now reads under `DIFF_VIEW_MAX_ARTIFACT_BYTES` per DECISION F037 D7, so the artifact is not read whole and the bound the comment says belongs elsewhere is already there. LOW AND NOT MEDIUM because no behaviour is wrong, no suite is red, and the paragraph's CONCLUSION — that the input bound belongs in the other module — is exactly what landed; what is false is the present-tense claim about the other module's state. NOT a slip under operator amendment amend0827 rule 2: the wrong state is on disk under `packages/`, in shipped production code, which is the first clause of what rule 2 reserves an id for, and it is the class the checklist's own item 20 exists to prevent — a slice stating a present-tense fact about a file a later commit of the same branch falsifies. THIS IS NOT `R-0724`, which is a false claim about this environment's test runner in a test module's docstring; this one is a false claim about a sibling module's code, in production code. COUNTER-MEASURE: replace the clause with what is now true — the two ceilings here bound the OUTPUT this module builds, the INPUT is bounded by `DIFF_VIEW_MAX_ARTIFACT_BYTES` under DECISION F037 D7, and neither subsumes the other because they are different resources in different units — changing no statement in the file, which the round proves by comparing the comment-stripped blobs. OPEN.
<<<END FIND0723

<<<SLICE FIND0724
- R-0724 — Low, A TEST MODULE'S DOCSTRING STATES AS FACT THE PREMISE THAT STOPPED TWO THIRDS OF THIS FEATURE, AND THE PREMISE IS FALSE. Raised by the reviewer at the F037 R14 gate while probing whether T002 is really blocked; no round was ordered to look for it. `tests/ui_contracts/test_diff_surface_css.py` opens, at `0d750765`, with "the frontend test runner cannot be executed in this environment, so the conformance of this stylesheet is pinned from Python". MEASURED BY THE REVIEWER at `0d750765`: `tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes` runs `npx vitest run` with `cwd` at `apps/ui` and asserts its return code is 0, and that node is REAL EXIT CODE 0 in 0.92 s in this environment — so the runner executes here, through this repository's own gate, and CI runs the same node. What is refused is a DIRECT `npx vitest` invocation from the session's own shell, which is a permission on one caller and not a property of the environment. THE COST IS THE REASON THIS EARNS AN ID RATHER THAN A SLIP: this sentence, and the same claim repeated in `.agent/plan.md` and in three handbacks, is why F037 R8 through R14 recorded T002 and T003 as BLOCKED and built only server-side work, and wrong state under `tests/` is the first clause of what operator amendment amend0827 rule 2 reserves an id for. LOW AND NOT HIGHER because the sentence's CONCLUSION is right for a reason it never gives — `apps/ui/vitest.config.ts` collects `src/**/*.test.ts` in a NODE environment, so the runner reaches no stylesheet and no markup whatever its availability, and pinning this conformance from Python is correct either way — so no guard is weaker than it looks and nothing on the CSS side needs rebuilding. THIS IS NOT `R-0723`, a stale bound clause in the parser's own comment. COUNTER-MEASURE: replace the false half with the real reason, and rule the general question in a DECISION rather than in a docstring, since it governs the whole remaining scope of this feature — DECISION F037 D8 does that, and records what a red-proof of TypeScript can and cannot be here. OPEN.
<<<END FIND0724

<<<SLICE DECISION8
## DECISION F037 D8 — T002 and T003 are NOT blocked; the client is built in the layer vitest reaches, and no TypeScript colour is ordered because none can be run

**Date:** 2026-08-28 · **Round:** F037 R15 · **Findings:** `R-0724`, `R-0723`

**The choice.** F037's remaining scope is built with this repository's existing
frontend pattern rather than waiting for a runner. Decidable rules go in
`apps/ui/src/api/*.ts` with `*.test.ts` beside them, which
`apps/ui/vitest.config.ts` collects in a NODE environment; markup, stylesheets
and wiring are pinned from `tests/ui_contracts/` in Python. That is what
DECISION F031 D5 already ruled for the decision inbox, and F037 follows it.

**Why the blocked premise was wrong.** Measured at `0d750765`:
`tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`
runs `npx vitest run` from pytest with `cwd` at `apps/ui` and asserts a return
code of 0, and it is exit 0 here in 0.92 s. CI runs the same node. What is
refused is a DIRECT `npx vitest` from the session's own shell — a permission on
one caller, not a property of the environment. Reading that refusal as "the
runner cannot be executed" is what recorded T002 and T003 as blocked from R8
through R14, and it is registered as `R-0724`.

**What a red-proof of TypeScript can be here, and what it cannot.** It cannot be
a mutation. Guardrail G5 of `docs/agents/self_drive_protocol.md` confines every
destructive check to a disposable `git worktree`, `apps/ui/node_modules` is
gitignored and therefore absent from any fresh worktree, and the reviewer
measured the consequence at `0d750765`: the vitest node run with its `cwd` in a
worktree fails at STARTUP with `Cannot find package 'vitest'` before any test is
loaded, so it is red for every possible module under test. A colour from a
command that cannot pass proves nothing — that is finding `R-0703`'s rule and
this decision does not break it. What IS ordered instead, and what makes the
TypeScript honest: the vitest suite runs GREEN through the pytest node in the
primary checkout, where it is a real gate that a broken module turns red; and a
Python guard under `tests/ui_contracts/` pins the structural facts vitest cannot
see about itself, and THAT guard is mutated and red-proved normally, because it
is Python and needs no `node_modules`.

**What this costs, stated plainly.** A defect that a vitest test would catch is
caught only when the whole vitest suite is run, and never by a mutation aimed at
one function. The mitigation is the shape of the code rather than more gates:
the more of the client's behaviour that lives in `src/api/` as total functions
over plain data, the more of it a green suite actually covers. That is the
reason the view model is built before the component and carries the collapse
rule, the row keys and the sidebar, rather than leaving them in markup where
nothing here can reach them at all.

**Why the feature file is not amended.** Its Task slicing already names T002 as
the rendering core and T003 as the sidebar and virtual scrolling, and neither
mentions a runner. The blocked premise never lived in
`docs/roadmap/features/T5_F037.md` — it lived in a test docstring, in
`.agent/plan.md` and in handbacks. Amendment A4 stands unchanged.

**Alternatives rejected.** (1) Keep waiting for a direct runner — rejected: it
is a session permission that has already varied between sessions, and a feature
cannot be paced by it. (2) Copy `apps/ui/node_modules` into the worktree to
enable mutations — rejected: it is hundreds of megabytes per proof, and
`shutil.copytree` defaults to dereferencing the bin shims, which is exactly the
mechanism finding `R-0591` records as having CAUSED failures it was meant to
prevent. (3) Build the component first and the model after — rejected: it puts
the collapse rule and the row keys in markup no gate here can reach, which is
the arrangement DECISION F031 D5 exists to prevent.

**How to reverse.** Delete this decision and the three files F037 R15 added —
`apps/ui/src/api/diffViewModel.ts`, `apps/ui/src/api/diffViewModel.test.ts` and
`tests/ui_contracts/test_diff_view_model.py`. Nothing else imports them; no
existing module changes as part of this decision, and the two comment repairs it
carries stand on their own findings rather than on this ruling.
<<<END DECISION8

<<<SLICE DONE0723
Done: R-0723 — RESOLVED at F037 R15 by the round's C3, in the commit order constraint 9 of the R15 block fixes. The DELIBERATE ABSENCE paragraph above `DIFF_VIEW_MAX_FILES` in `packages/orchestration/diff_parser.py` no longer claims that `diff_view_source.py` reads the artifact whole: it now says that the two ceilings here bound the OUTPUT this module builds, that the INPUT is bounded by `DIFF_VIEW_MAX_ARTIFACT_BYTES` under DECISION F037 D7, and that neither subsumes the other because they are different resources in different units. THE REPAIR CHANGED NO CODE AND THE ROUND PROVED THAT RATHER THAN ASSERTING IT: the commit's blob and the base blob are byte-identical once every `#`-comment line and docstring is removed, which is a stronger reading than a green suite, because a suite cannot tell a comment edit from an equivalent statement edit. The counter-measure is the one the finding named — correct the clause, change nothing else — and not a rewrite of the paragraph, because the paragraph's conclusion was right all along.
<<<END DONE0723

<<<SLICE DONE0724
Done: R-0724 — RESOLVED at F037 R15 by the round's C3, in the commit order constraint 9 of the R15 block fixes. `tests/ui_contracts/test_diff_surface_css.py`'s docstring no longer says that the frontend test runner cannot be executed in this environment. It now gives the REAL reason that guard is written in Python, which the false clause was standing in for: `apps/ui/vitest.config.ts` collects `src/**/*.test.ts` in a NODE environment, so the runner reaches no stylesheet and no markup whatever its availability. No assertion in that file changed and none needed to — the finding is explicit that the guard was never weaker than it looked. THE GENERAL QUESTION IS RULED WHERE IT BELONGS: DECISION F037 D8 records that T002 and T003 are not blocked, that the build pattern is decidable rules in `apps/ui/src/api/` with markup pinned from `tests/ui_contracts/`, and — the part a docstring could not have carried — that no mutation red-proof of TypeScript is orderable here, because `apps/ui/node_modules` is gitignored and the vitest node run with its `cwd` in a disposable worktree fails at startup for every possible module under test. WHAT THIS RESOLUTION DOES NOT CLAIM: that the runner is available to every caller. A direct `npx vitest` from the session's own shell is still refused, and the finding is about the difference between that permission and a property of the environment.
<<<END DONE0724

Done when — the gates below, every one executed with its REAL exit code
recorded, one line per gate in the handback. G1 through G8 run at the commits
named; none of them runs after C8, so the handback can quote every one of them.

G1 HYGIENE. Read `.agent/STOP` from disk before C0a and again before C8 and
report both readings. Report `git rev-parse HEAD` before C0a and state whether
it equals `0d750765`, `git branch --show-current`, and the `git status
--porcelain` line count after each of C0a through C7.

G2 TRANSPORT, ONE DIGEST COMPARISON. Report sha256, byte count and line count of
the committed `.agent/authored/f037-r15.md` blob, and state whether they equal
the reviewer's scratch original at `.remedy-wt/f037-r15-block.md` — compare the
two files directly, disk to disk. Report `git rev-parse <C0b>:.agent/authored/f037-r15.md`
and `git rev-parse <C0b>:.agent/last_block.md` and whether they are the same
blob. State what the chain covers and what it does not.

G3 EXTRACTION AND CAPS, measured on the COMMITTED C0a blob and never on the
prose. For each slice report its content line count; report TOTAL lines of the
blob, CONTENT as their sum, PROSE as TOTAL minus CONTENT, and whether TOTAL is
at most 490 and PROSE at most 400.

G4 THE PLAN AT C1, AND THE COMMENT-ONLY PROOF AT C3. Report whether
`.agent/plan.md` is byte-equal to the PLANF037R15 slice extracted from the
committed C0a blob, including the trailing newline, plus the negative control
against that slice minus its trailing newline; the count of lines exactly
`## Goal` and exactly `## Next Steps`; and `wc -l` with whether it is strictly
under 50. Then, for `packages/orchestration/diff_parser.py`, report whether the
C3 blob and the `0d750765` blob are byte-identical after removing every line
whose first non-space character is `#` and every triple-quoted docstring — and
report the same comparison WITHOUT that removal, which must be False, so the
first reading is shown not to be a comparison that cannot fail.

G5 THE RECORD AT C2 AND C7. For each of the five appends — GATER14, FIND0723 and
FIND0724 into `.agent/live_review.md`, DECISION8 into `.agent/decisions.md`,
DONE0723 and DONE0724 into `.agent/live_review.md` — report reader (a),
`result == before + b"\n" + slice` re-read from disk; reader (b), which COUNTS
the blank-line-separated units of the slice and compares the LAST that many
units of the file against them IN ORDER, reporting the count it measured; and a
negative control for both readers that flips one byte inside the FIRST appended
paragraph. Report whether each file's pre-round blob is a byte PREFIX of the
result, reading that blob with `git show 0d750765:<path>` into memory and never
over the tracked file. Then report, line-anchored over `.agent/live_review.md`
after C7 with the base figure beside each: `^- R-\d+ — `, `^Done: R-\d+ — `,
`^Landed: R-`, `^Gate: F\d+ R\d+ — `, the open-set size, whether every
REGISTERED id is distinct, and the number of resolution lines against the number
of distinct ids among them. Over `.agent/decisions.md`, report `^## DECISION `
and the count of `F037 D8`.

G6 THE RED-PROOFS, WHICH ARE OF THE PYTHON GUARD AND OF NOTHING ELSE. FIRST
report the measurement that says why: in a disposable worktree at the C6 tree,
run `python3 -B -m pytest tests/orchestration/test_test_runner.py -q -k vitest`
with the worktree as the working directory and report its REAL exit code and the
reason text — it is expected to FAIL at startup because `apps/ui/node_modules`
is gitignored and absent there, which is what makes a TypeScript mutation
unmeasurable under guardrail G5. Then, in that same worktree and with
`__pycache__` purged and `python3 -B` for every run, red-prove
`tests/ui_contracts/test_diff_view_model.py` — the file restored between runs and
each restore verified byte-identical by sha256. Report the UNMUTATED CONTROL's
exit code and summary line first, then for each mutation the occurrences of the
replaced string BEFORE the edit, which must be 1, the REAL exit code, the
summary line and the failing node ids:
(a) add a line `import { foo } from "./bar";` at the top of
`apps/ui/src/api/diffViewModel.ts`. Expect RED.
(b) rename one exported function in `apps/ui/src/api/diffViewModel.ts` so the
test file no longer names it. Expect RED.
(c) replace the reference to `DIFF_HUNK_COLLAPSE_THRESHOLD_LINES` in
`apps/ui/src/api/diffViewModel.test.ts` with its numeric literal. Expect RED.
The ordered property is the COLOUR: report the names and counts you measure
rather than any this block predicts.

G7 SUITES, LINT AND CANARY AT C6, IN THE PRIMARY CHECKOUT. One pytest process at
a time; never two at once. Report the REAL exit code and the full summary line
of each: `python3 -m pytest tests/orchestration/test_test_runner.py -q`, which
is the gate that RUNS vitest and whose base figure at `0d750765` is
`52 passed`; `python3 -m pytest tests/ui_contracts/ -q`;
`python3 -m pytest tests/orchestration/test_diff_parser.py
tests/orchestration/test_diff_view_source.py -q`, whose base figure is
`58 passed` and which must be UNMOVED because constraints 3 and 4 forbid
touching either side of it; `python3 -m ruff check
tests/ui_contracts/test_diff_view_model.py
tests/ui_contracts/test_diff_surface_css.py
packages/orchestration/diff_parser.py` under this repository's own
configuration; and the canary `python3 -m pytest tests/cli/test_golden_path.py
-q`, whose base figure is `42 passed`. For the first of these, ALSO report the
`in <n>s` figure and state how many vitest tests the run covers, taking that
count from a separate run of `npx vitest run` you make yourself in the primary
checkout if your permissions allow it and reporting the refusal verbatim if they
do not.

G8 STRUCTURE, ARTIFACTS AND THE OPEN PR GATE AT C7. Report `git diff
--name-only 0d750765..<C7>` and both residues against the change set above —
actual minus expected and expected minus actual, with `.agent/handoff.md`
expected to be the only member of the second because C8 writes it. Report `git
diff --stat` restricted to `docs/`, to `packages/`, and to `apps/`; the second
must hold `packages/orchestration/diff_parser.py` alone and the third must hold
`apps/ui/src/api/diffViewModel.ts` and `apps/ui/src/api/diffViewModel.test.ts`
alone, which is what proves constraints 4 and 5. Report each commit's insertion
count from `git show --numstat` for C0a through C7 and whether each is under
500, and check those figures cell by cell against the `+/-` column of the
handback's own `## Commits` table. Report the count of lines matching
`^<<<SLICE ` and `^<<<END ` in `.agent/plan.md`, `.agent/live_review.md`,
`apps/ui/src/api/diffViewModel.ts` and
`tests/ui_contracts/test_diff_view_model.py`, and the same counts over the C0a
blob as the control that the counter is not blind. Report
`git ls-files .remedy-wt` line count. Run `gh pr list --state open --json
number,headRefName,baseRefName,isDraft` verbatim and report its exit code and
stdout.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It
carries the SESSION NUMBER of this feature — session 4 — the round, the range
`0d750765..<C8>`, a per-commit changed-files table with the `+/-` column, one
line per gate G1 through G8 with its real result, the authored-text proofs, the
deviations, the item-status table covering C0a through C8 and G1 through G8 and
`R-0723` and `R-0724`, and the next expected action. Derive any cap it must
respect from AGENTS.md yourself; this block states none. Then push the branch.
