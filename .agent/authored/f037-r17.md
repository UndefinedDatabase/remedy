# STEP T003 (first round) — F037 Rendered diff viewer, round 17

BASE: `44a8493b`. SESSION 5 of feature F037. This block carries no line that is a
run of a single repeated character, so nothing in its frame has a length a reader
must recover by eye.

## Goal

Open T003 at the seam T002 stopped short of: the DOOR the client fetches a diff
envelope through. `apps/ui/src/api/remedyApi.ts` gains a URL builder and a loader
for the two scopes `packages/orchestration/ui_server.py` really routes, every
payload leaves that loader through `readDiffEnvelope`, and a Python guard pins
the client's URL template against the server's own route conditions — the one
agreement vitest cannot see, because it spans two languages. Nothing is mounted
this round.

## Bundle

- C0a save this block verbatim to `.agent/authored/f037-r17.md`.
- C0b mirror the same bytes into `.agent/last_block.md`.
- C1 rewrite `.agent/plan.md` from the PLANF037R17 slice.
- C2 append the GATER16 slice to `.agent/live_review.md`.
- C3 the envelope door and its vitest tests: SPEC S1 through S6 in
  `apps/ui/src/api/remedyApi.ts` and `apps/ui/src/api/remedyApi.test.ts`.
- C4 the cross-language guard: SPEC S7 in the NEW file
  `tests/ui_contracts/test_diff_envelope_door.py`, and SPEC S8 appended to
  `tests/ui_contracts/test_diff_view_render.py`.
- C5 rewrite `.agent/handoff.md` as the handback.

## Change set

Exactly these paths, and nothing outside them:

- `.agent/authored/f037-r17.md` (new)
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `apps/ui/src/api/remedyApi.ts`
- `apps/ui/src/api/remedyApi.test.ts`
- `tests/ui_contracts/test_diff_envelope_door.py` (new)
- `tests/ui_contracts/test_diff_view_render.py`
- `.agent/handoff.md`

Push the branch after C5 with `git push -u origin feature/f037-rendered-diff-viewer`.
Create no PR. Merge nothing. Rewrite no history.

## Constraints

1. Apply every slice BYTE FOR BYTE. Do not edit, reflow, correct or re-wrap a
   slice, and never write a `<<<SLICE` or `<<<END` marker line into a target
   file. If a slice looks wrong, apply it anyway and declare it in the handback.
2. The SPEC items below describe PRODUCTION CODE and are not slices. Write that
   code yourself, in this repository's idiom, satisfying every numbered clause.
   The WHY comments the clauses ask for are yours to word.
3. `apps/ui/src/api/diffViewModel.ts` is NOT edited this round. The door imports
   from it and adds nothing to it. Two guards in
   `tests/ui_contracts/test_diff_view_model.py` bind that file — every export
   must be named by `diffViewModel.test.ts`, and the collapse threshold literal
   must occur exactly once across the module and its tests — and leaving the
   module alone is what keeps both satisfied.
4. Nothing under `packages/` changes. The server routes already exist; this
   round reads them and agrees with them.
5. No new npm dependency, no new config file, no change to
   `apps/ui/vitest.config.ts`.
6. `vi.stubGlobal` and any other global patching is FORBIDDEN in the vitest
   tests. There is no precedent for it in `apps/ui/src` and this round does not
   create one — the door takes its fetcher as an argument precisely so the tests
   need no global at all (SPEC S4).
7. Order the commits exactly C0a, C0b, C1, C2, C3, C4, C5. C1 is the first
   substantive commit, which is what keeps `.agent/plan.md` true before every
   later commit's gate.
8. Every gate below runs at a commit STRICTLY EARLIER than C5, so the handback
   can quote all of them. G1's second STOP reading is the sole exception and is
   taken immediately before C5 is written.
9. Destructive verification runs ONLY inside a disposable worktree under
   `.remedy-wt/`. The primary checkout reads `git status --porcelain` empty
   after every commit.
10. NO TYPESCRIPT MUTATION RED-PROOF IS ORDERED, and this round does not retry
    the route. The reviewer measured every variant at `44a8493b` and the result
    is recorded in the GATER16 slice: a worktree vitest run given the PRIMARY
    checkout's config path runs green but reads the PRIMARY tree, staying green
    under a worktree mutation, and every invocation that really roots at the
    worktree dies with `ERR_MODULE_NOT_FOUND`. The `.ts` door is covered by
    vitest in the primary checkout; the Python guard is red-proved in full.

## SPEC — the envelope door (C3)

All of S1 through S5 land in `apps/ui/src/api/remedyApi.ts`.

S1. A new exported interface `DiffEnvelopeRequest` with fields `jobId: string`,
`token: string`, `baseUrl?: string` and `taskId?: string | null`. It is an
object rather than positional arguments because three of its four fields are
strings and a swap between them would type-check silently — the rule AGENTS.md
states under "Code Discoverability Conventions".

S2. A new exported type
`DiffEnvelopeFetcher = (path: string) => Promise<unknown>`.

S3. A new exported PURE function `diffEnvelopePath(request: DiffEnvelopeRequest): string`.
Its value is `${base}/api/jobs/${job}/diff?${q}` when the request names no task
run, and `${base}/api/jobs/${job}/task-runs/${task}/diff?${q}` when it does,
where `base` is `request.baseUrl` or the empty string and `q` is
`token=` followed by the percent-encoded token. `job` and `task` are
percent-encoded too — unlike `loadRemedyDashboard` above, which interpolates its
job id raw; say in the WHY comment that a task id is a path SEGMENT here, so an
unencoded slash in it would silently address a different route. A `taskId` that
is `undefined`, `null`, empty, or whitespace only selects the job scope.

S4. A new exported function
`loadDiffEnvelope(request: DiffEnvelopeRequest, fetchPayload?: DiffEnvelopeFetcher): Promise<DiffEnvelope>`.
It awaits `fetchPayload(diffEnvelopePath(request))` and returns
`readDiffEnvelope` of the result; on ANY rejection it returns
`readDiffEnvelope(null)` instead. `fetchPayload` DEFAULTS to the module's
existing private `fetchJson`, so callers pass nothing and the tests pass a fake.
The WHY comment states the property: this door never throws and never returns a
shape a caller must branch on — a 403, a dead socket and a junk body all arrive
as the same total `DiffEnvelope` with `available` false, which is the reason
`readDiffEnvelope` exists.

S5. The imports S3 and S4 need, from `./diffViewModel`: the value
`readDiffEnvelope`, and the TYPE `DiffEnvelope` as a `type` import.

S6. A new `describe` block in `apps/ui/src/api/remedyApi.test.ts`, added at the
end and changing no existing test. It imports the three new exports beside the
four it already imports, and covers, one `it` per clause:
(a) the job-scope path is the exact expected string for a plain request;
(b) the task-run path is the exact expected string for the same request plus a
    task id;
(c) a token containing `&` and a task id containing `/` are percent-encoded, so
    neither can add a query parameter nor a path segment;
(d) a request carrying `baseUrl` prefixes it, and one without it yields a
    relative path beginning `/api/`;
(e) `taskId` of `null`, of `""` and of `"   "` each select the job scope;
(f) `loadDiffEnvelope` with a fake fetcher returns the parsed envelope, and the
    fetcher was called exactly once with the value `diffEnvelopePath` returns
    for the same request;
(g) a fetcher that REJECTS yields `available` false and does not throw;
(h) a fetcher resolving a junk body — a string, and an array — yields
    `available` false with an empty `files`.

## SPEC — the guards (C4)

S7. A NEW file `tests/ui_contracts/test_diff_envelope_door.py`. It reads
`apps/ui/src/api/remedyApi.ts`, `apps/ui/src/api/remedyApi.test.ts` and
`packages/orchestration/ui_server.py` AS TEXT and imports nothing from `apps/`,
exactly as `tests/ui_contracts/test_diff_view_render.py` does. Reuse that file's
`strip_ts_comments` shape; every assertion over the client runs on
COMMENT-STRIPPED source, because the door's own WHY comments name the symbols
asserted below. Assertions:
(a) the client's job-scope route agrees with the server's: the stripped client
    carries the literal `/diff?`, and `ui_server.py` carries `"diff":` as a key
    of the handler dictionary its five-segment job route dispatches on;
(b) the client's task-run route agrees with the server's: the stripped client
    carries the literal `task-runs`, and `ui_server.py` carries both
    `parts[4] == "task-runs"` and `parts[6] == "diff"`;
(c) the client sends the token on the diff route — the stripped client's
    `diffEnvelopePath` body carries `token=`, which is what
    `ui_server.py` requires of every `/api/` path before dispatch;
(d) the door normalizes through the single door: `readDiffEnvelope` occurs in
    the stripped client, and `loadDiffEnvelope` contains a `catch`, so the
    degradation path is in the CODE and not only in the comment;
(e) every name the door exports is named by `remedyApi.test.ts`, the same reach
    `tests/ui_contracts/test_diff_view_model.py` gives the model module;
(f) a NOT-VACUOUS class, above the others, in the shape
    `TestTheStripperIsNotVacuous` of `test_diff_view_render.py`: the stripper
    really removes both comment forms, the client source really loses text to
    it, and the server scan really finds more than zero route literals. Without
    it every assertion above is satisfiable by prose.

S8. One test appended to `tests/ui_contracts/test_diff_view_render.py`, inside
the existing `TestTheHunkHeadIsAControl` class, using the existing
`hunk_head_tag` helper. It asserts that the tag binds `aria-expanded` to the
NEGATION of the row's collapse flag: `aria-expanded={!row.collapsed}` is in the
tag, and `aria-expanded={row.collapsed}` is not. Change no existing test. The
reviewer measured at `774cf732` that inverting that expression leaves the whole
guard green at 12 passed, so the guard pins the attribute's PRESENCE — which is
all the R16 block ordered — and not its polarity; a viewer that reports every
open hunk as closed is exactly what a screen reader would then announce.

## Slice convention

Each slice below sits between a `<<<SLICE <NAME>` line and a `<<<END <NAME>`
line. Neither marker line is part of the slice, and neither is ever written into
a target file. The slices this block carries are PLANF037R17 and GATER16.
PLANF037R17 is a FULL REWRITE of `.agent/plan.md`. GATER16 is an APPEND to
`.agent/live_review.md`: join it to the existing bytes with exactly one newline
between the file's current content and the slice's first line.

<<<SLICE PLANF037R17
# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495` (the
merge of PR #217, which closed F032). `.agent/decisions.md` holds F037 D1 to D9.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the design amendments A1 through A5.

## Current Step
R17 opens T003 at the seam T002 stopped short of: the DOOR the client fetches a
diff envelope through. `remedyApi.ts` gains a URL builder and a loader for the
two scopes `packages/orchestration/ui_server.py` really routes — a job's diff
and one task run's — and every payload leaves that loader through
`readDiffEnvelope`, so a 403, a dead socket and a junk body all degrade to the
same total envelope rather than three shapes the viewer would have to know
about. A Python guard pins the client's URL template against the server's own
route conditions, which is the agreement vitest cannot see. Nothing is mounted.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R16 verdict | ordered | record first |
| C3 the envelope door and its vitest tests | ordered | the fetch seam |
| C4 the cross-language guard and the polarity test | ordered | vitest sees no routes |
| C5 the handback | ordered | |

## Next Steps
1. Mount the viewer: the "Open diff" button `component_spec.md:113-116` puts in
   `DetailPopover`, the state holding the opened task, and `DiffView` behind it.
2. The file sidebar over `buildDiffFileSummaries`, then virtual scrolling beyond
   two thousand lines, the lazy language bundles and the perf fixture.

## Risks
- Round 17 of a 25-round soft limit, session 5 of 7. The named pieces of T003
  still open are the mount, the sidebar, the virtual scrolling, the lazy
  language bundles, the perf fixture and the L3 tab integration, so a round
  closing none of them is the one to stop and re-scope after.
- No TypeScript mutation red-proof is orderable anywhere here. The `.ts` layer
  is covered by vitest in the primary checkout and by text guards; the `.tsx`
  layer by `tsc --noEmit` and text guards, and by nothing else.
<<<END PLANF037R17

<<<SLICE GATER16
Gate: F037 R16 — the round that finished T002 by drawing the rows and ruling the intraline emphasis. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran it independently at `44a8493b` rather than reading the handback's numbers. RE-MEASURED, NOT ACCEPTED. `git log --numstat` over `68680786..44a8493b` reproduces the `+/-` column of the handback's `## Commits` table cell for cell, every per-commit insertion count under five hundred. The committed C0a blob `git show 8368a4c5:.agent/authored/f037-r16.md` is 33024 bytes, 471 lines, sha256 `fda049537c12a805285830bac86f023690bae4570ffcc6d923f9aa1f16c4612e`, and is byte equal to the reviewer's own scratch original `.remedy-wt/f037-r16-block.md` — which under docs/agents/self_drive_protocol.md IS the artifact the worker read from disk, so this chain covers the emission itself and not only the worker's self-consistency; `git rev-parse 81fb30c5:.agent/authored/f037-r16.md` and `git rev-parse 81fb30c5:.agent/last_block.md` are one blob `9185d96ca9d9323aa05f2b55dbf8124c28b45891`. Every slice was re-extracted from that blob and re-applied by the reviewer: `.agent/plan.md` at `0042f710` is byte equal to PLANF037R16 including its trailing newline, with the newline-stripped negative control False, 49 lines, one `## Goal` and one `## Next Steps`; the four appends GATER15, SLIPR16, DECISION9 and AMENDA5 each satisfy the byte reader and the ordered-unit reader over 1, 1, 9 and 2 units, each with its negative control False and its base blob a byte prefix. RE-RUN SUITES, primary checkout, one process at a time, every one exit 0: `tests/ui_contracts/` 603 passed 4 skipped, `tests/orchestration/test_test_runner.py` 52 passed, `tests/docs/` 295 passed, `tests/ui_server/test_dashboard_contract.py -k typescript` 1 passed 73 deselected, `tests/cli/test_golden_path.py` 42 passed. SPOT-CHECKS THE BLOCK DID NOT ORDER were added because the round touched `docs/roadmap/**` and rewrote `.agent/` state while gating neither reader set in full: `tests/orchestration/test_roadmap_index.py` 30 passed, and `tests/ui_server/` with `tests/regression/test_resource_safety.py` and `tests/orchestration/test_integrity_gate.py` together 532 passed, all exit 0. AN INDEPENDENT RED-PROOF ran in a disposable worktree at `774cf732`: the unmutated guard is exit 0 at 12 passed before and after, the handback's mutation (d) reproduces at exit 1 with `1 failed, 11 passed` failing exactly `TestEveryClassTheComponentNamesIsReal::test_every_class_the_component_names_has_a_rule_in_the_stylesheet`, and the file was restored to its pre-mutation sha256.

TWO MEASUREMENTS THIS GATE ADDS TO THE RECORD, both taken by the reviewer and neither ordered by the R16 block. FIRST, THE GUARD'S REACH. Inverting `aria-expanded={!row.collapsed}` to `aria-expanded={row.collapsed}` in `apps/ui/src/components/diff/DiffView.tsx` at `774cf732`, in the same disposable worktree, leaves the guard GREEN at 12 passed. The guard therefore pins the attribute's PRESENCE, which is exactly what that block's SPEC item S10 (c) ordered, and not its POLARITY. The component's polarity is correct as shipped and nothing on disk is wrong, so no id is spent under operator amendment amend0827-process-diet rule 2; the missing assertion is ordered in this same round's C4 instead, appended to the existing hunk-head class. SECOND, WHY NO TYPESCRIPT COLOUR IS ORDERABLE, which DECISION F037 D8 rules and which this gate now measures by a route D8 never tried. Checklist item 33 of docs/agents/planner_reviewer_prompt.md says a worktree vitest run needs the PRIMARY checkout's config path, since `apps/ui/node_modules` is gitignored and absent from any fresh worktree. Measured at `44a8493b` in a disposable worktree: given `--config <primary>/apps/ui/vitest.config.ts` and scoped to `src/api/`, the run is exit 0 at 29 files and 533 tests — with and without `--root .` — and it stays exit 0 at 533 passed when `DIFF_HUNK_COLLAPSE_THRESHOLD_LINES` is changed from 200 to 3 IN THE WORKTREE, so that green is reading the PRIMARY tree and is blind by construction. Every invocation that really roots at the worktree — its own config, no config, or `--dir` — exits 1 with `ERR_MODULE_NOT_FOUND` before loading a test. The dichotomy is exact and general: whichever tree vitest roots at is the tree it needs `node_modules` in, and a worktree never has one. A later round that reads item 33 and reaches for the config flag would ship a gate that cannot fail; it is written here so that it does not.
<<<END GATER16

## Done when — the gates

Run every gate yourself and record its REAL exit code and its REAL summary line.
"Green" as a word is a finding. One line per gate in the handback.

G1 HYGIENE. Read `.agent/STOP` from disk before C0a and again immediately before
C5; report ABSENT or PRESENT each time, and on PRESENT stop after finishing the
commit in hand and hand off. `git rev-parse` before C0a must equal `44a8493b`.
Report `git branch --show-current`. Report the `git status --porcelain` line
count after each of C0a through C4; each must be 0.

G2 TRANSPORT, one digest comparison. Report the byte count, line count and
sha256 of the committed C0a blob (`git show <C0a>:.agent/authored/f037-r17.md`)
and compare all three against the three readings the delegation named. Then
report whether `git rev-parse <C0b>:.agent/authored/f037-r17.md` and
`git rev-parse <C0b>:.agent/last_block.md` are the same blob.

G3 EXTRACTION AND CAPS, measured on the committed C0a blob. Report the content
line count of PLANF037R17 and of GATER16, their sum as CONTENT, the blob's line
count as TOTAL, and TOTAL minus CONTENT as PROSE. Report TOTAL <= 490 and
PROSE <= 400.

G4 THE PLAN AT C1. Extract PLANF037R17 from the committed C0a blob
programmatically — never retype it — and report whether `git show <C1>:.agent/plan.md`
is byte equal to it INCLUDING the trailing newline. Report the negative control
against that slice minus its trailing newline; it must be False. Report the
file's `wc -l` and that it is strictly under 50, and the count of lines exactly
`## Goal` and exactly `## Next Steps`; each must be 1.

G5 THE RECORD AT C2. Extract GATER16 from the committed C0a blob. Report reader
(a): the pre-round blob `git show 44a8493b:.agent/live_review.md` plus one
newline plus the slice equals `git show <C2>:.agent/live_review.md`. Report
reader (b): the last N blank-line-separated units of the committed file equal
the slice's N units IN ORDER, where N is a number your script COUNTS. Report a
negative control for each reader, flipping one byte inside the FIRST appended
paragraph; both must be False. Report that the pre-round blob is a byte PREFIX
of the committed one. Then report, line-anchored over the committed file, with
the figure at `44a8493b` beside each: lines matching `^- R-\d+ — ` (285 at base),
`^Done: R-\d+ — ` (34), `^Landed: R-` (1), `^Gate: F\d+ R\d+ — ` (86), the open
set (252), and whether every registered id is distinct.

G6 THE RED-PROOFS OF THE PYTHON GUARDS. All runs in a disposable worktree at the
C4 tree, `__pycache__` purged before every run, `python3 -B` throughout. Report
the UNMUTATED control for
`tests/ui_contracts/test_diff_envelope_door.py tests/ui_contracts/test_diff_view_render.py`
before any mutation and again after the last restore; both must be exit 0. Then,
one at a time, each mutation restored byte-identically to its pre-mutation
sha256 before the next, reporting for each the REAL exit code, the summary line
and the failing node ids.

UNIQUENESS, PER FINDING `R-0629`, WHICH IS OPEN AND BINDING ON ANY BLOCK THAT
ORDERS A DESTRUCTIVE CONTROL. That finding requires the REVIEWER's own script to
count a control's target in the named file at the SHA the control runs at, and
the block to carry that script's output. Mutation (d) targets a file that exists
at the base, so the reviewer measured it and the numbers are stated here.
MEASURED AT `44a8493b` over `apps/ui/src/components/diff/DiffView.tsx`, which is
173 lines: the literal `aria-expanded={!row.collapsed}` is 30 characters, holds
no backtick, and occurs as a SUBSTRING exactly 1 time, on physical line 130 at 14
leading spaces; that physical line read WHOLE and anchored at both ends occurs 1
time, and read indentation-agnostically also 1 time — the two readings agree. The
replacement `aria-expanded={row.collapsed}` occurs 0 times before the edit.

Mutations (a), (b) and (c) target code THIS ROUND CREATES, so no such count can
exist while this block is written and the reviewer states none. For those three
only, YOU take the reading: count the replaced string in the named file before
editing and report the count. If it is not 1 — `token=` is already in
`loadRemedyDashboard`, and a WHY comment may well name `task-runs` — EXTEND the
string with the characters around it until it reads 1 in that file, report the
extended string and its count, and mutate that. Replacing a string that occurs
twice changes a site the mutation does not name, and the red then proves nothing.

The mutations:
(a) in `remedyApi.ts`, change the task-run segment literal `task-runs` to
    `task-run`;
(b) in `remedyApi.ts`, delete the `catch` clause of `loadDiffEnvelope` so a
    rejection propagates;
(c) in `remedyApi.ts`, drop `token=` from the diff path;
(d) in `DiffView.tsx`, invert `aria-expanded={!row.collapsed}` to
    `aria-expanded={row.collapsed}`.
Each must be exit 1. If any mutation is GREEN, say so plainly and do not adjust
the test to suit it — a green mutation is a finding about the guard and the
reviewer wants the true reading.

G7 SUITES, TYPES, LINT AND CANARY AT C4, primary checkout, ONE pytest process at
a time. Report exit code and summary line for each, with the base figure beside
it where one is given: `python3 -m pytest tests/ui_contracts/ -q` (603 passed, 4
skipped at base), `python3 -m pytest tests/orchestration/test_test_runner.py -q`
(52 passed), `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q -k typescript`
(1 passed, 73 deselected), `python3 -m pytest tests/docs/ -q` (295 passed),
`python3 -m ruff check tests/ui_contracts/test_diff_envelope_door.py tests/ui_contracts/test_diff_view_render.py`,
and the canary `python3 -m pytest tests/cli/test_golden_path.py -q` (42 passed).
State explicitly whether the typescript node PASSED or SKIPPED — it skips only
when `apps/ui/node_modules/.bin/tsc` is absent, and a skip means the new door was
never type-checked. `tests/orchestration/test_test_runner.py` is the node that
runs `npx vitest run`, so state that the new `describe` really EXECUTED.

G8 STRUCTURE, ARTIFACTS AND THE OPEN PR GATE AT C4. Report
`git diff --name-only 44a8493b..<C4>` and set-difference it BOTH ways against
the Change set above; ACTUAL MINUS EXPECTED must be empty and EXPECTED MINUS
ACTUAL must be `.agent/handoff.md` alone. Report `git diff --stat` restricted to
`packages/`, which must be EMPTY. Report each commit's insertion count from
`git show --numstat`, each under 500, and confirm each matches the `+/-` column
of your own `## Commits` table cell by cell. Report the count of lines matching
`^<<<SLICE ` and `^<<<END ` in `.agent/plan.md`, `.agent/live_review.md`,
`apps/ui/src/api/remedyApi.ts` and `tests/ui_contracts/test_diff_envelope_door.py`
— each must be 0 — with a CONTROL count over the C0a blob, which must be
non-zero, so the counter is shown not to be blind. Report
`git ls-files .remedy-wt | wc -l`, which must be 0. Report
`gh pr list --state open --json number,headRefName,baseRefName,isDraft`.

## Handback

Rewrite `.agent/handoff.md` at C5 per docs/agents/handback_template.md. It has no
length cap. It must carry: the Session line naming SESSION 5 of F037 and round
17; the review range; a `## Commits` section with one `+/-` table per commit; the
external actions; one Verification line per gate G1 through G8 with real exit
codes; the authored-text proofs; the deviations and assumptions; the item-status
table covering every C and every G exactly once; and the next expected action.
Derive the handback's own tier from AGENTS.md rather than from any number here.
