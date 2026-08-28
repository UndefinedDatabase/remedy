### STEP T006 — F256 Diff viewer completion, round 10 (THE CLOSURE)

Goal: resolve `R-0732`, book the round 9 verdict, and CLOSE F256 — the STATUS
line flipped to `[x]` with the README capability sync in the SAME commit, then the
pull request. The package, its SHA-256, its archived path and the accepted HEAD
were all measured in round 9 and are carried below; nothing here re-derives them.

Base: `64c3774f`, the tip of `feature/f256-diff-viewer-completion`. Every reading
below was taken there by the reviewer.

Bundle, in commit order:

- C0a save this block verbatim to `.agent/authored/f256-r10.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 advance `.agent/plan.md`
- C2 append the `R-0732` resolution and the round 9 verdict to
  `.agent/live_review.md`
- C3 THE CLOSURE COMMIT: `docs/roadmap/STATUS.md`, `README.md` and
  `.agent/handoff.md` in ONE commit, the LAST on this branch
- then `gh pr create`, which is NOT a commit and does NOT merge

Change set, these paths and nothing else:

- `.agent/authored/f256-r10.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `docs/roadmap/STATUS.md`
- `README.md`
- `.agent/handoff.md`

RULE A4 BINDS: C3 is the LAST commit on this branch. The STATUS edit and the
README sync travel in it TOGETHER — the reviewer measured that flipping STATUS
while leaving README alone turns `tests/docs/` RED with exactly two failures, so
this is a proven pin and not a convention. The single permitted successor is
DECISION amend0827 D2's `.agent/candidates.md`-only commit, and only if the
closure gate raises a candidate.

### Constraints

0. BEFORE ANYTHING: report `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
   with its real output. Expected `[]`. Stay on
   `feature/f256-diff-viewer-completion`; do not branch, never work on `main`.
1. Apply every authored slice and every FROM/TO pair BYTE FOR BYTE. A slice you
   believe is wrong is applied as written and the problem is declared in the
   handback's deviations.
2. The delimiter lines `<<<SLICE …` and `<<<END …` are transport only and never
   reach a target file.
3. Extract every slice from the COMMITTED blob with
   `git show <C0a>:.agent/authored/f256-r10.md`, never from this prompt's text.
4. AGENTS.md binds in full: self-review before every commit, one logical step per
   commit, `.agent/plan.md` current before every commit, clean tree, push.
5. NO FILE UNDER `apps/`, `packages/`, `tests/` OR `docs/roadmap/features/`
   CHANGES BY A BYTE, and neither does `docs/roadmap/ROADMAP.md`. The feature
   file's Built State is already current from `f6d5d064`.
6. Shell forms rejected by this session's guard are RE-EXPRESSED as a script file
   under `.remedy-wt/` run with `python3`, never skipped and never weakened.
   Report each one.
7. EACH FROM STRING BELOW OCCURS EXACTLY ONCE in its target, measured by the
   reviewer at `64c3774f`. Assert that count is 1 BEFORE replacing, and report
   each measured count. If any is not 1, STOP and hand back — a replacement over
   a count you did not verify is how the wrong line gets edited.
8. DO NOT MERGE THE PULL REQUEST. It merges at the NEXT feature's start via the
   Open PR Gate; the gap is the operator's manual-review window. Never
   force-push, never rewrite history, never delete a branch.

### The closure edits of C3

Apply these three FROM/TO pairs and one APPEND. Nothing else in either file
changes: no other line is edited, reordered or deleted.

EVERY FROM AND TO BELOW IS DISPLAYED INDENTED BY FOUR SPACES so it renders as a
block; THAT INDENTATION IS NOT PART OF THE STRING. Strip exactly four leading
spaces from each displayed line before matching or writing it. The F256 R7
handback records this same presentation catching a worker out, which is why it is
stated here: constraint 7's "count must be 1" check will fail loudly if you match
the indented form, and that failure is the intended guard rather than a licence
to guess.

PAIR S1, in `docs/roadmap/STATUS.md`.

FROM (one line):

    - [~] F256 — Diff viewer completion (highlighting wiring, 10k-line perf measurement, sidebar ruling; split off F037 by DECISION F037 D11 / amendment A6)

TO (one line):

    - [x] F256 — Diff viewer completion (T001–T003 complete; accepted 2026-08-28 · live review PASS — ACCEPTED · Evidence job f256-closure · package remedy-review-20260828-233819-READY_FOR_REVIEW.zip · SHA-256 5f18d7acdeab790b0f79181c7179023535b389ce0b76ec427f2765b20cda4ad5 · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD c6775b3c41f1d1fa4b0f4bb7907307573855a61b)

The dash in `T001–T003` is an EN DASH, matching every accepted line above it.

PAIR S2, in `README.md`.

FROM (one line):

    60 of 257 registered items accepted. Next: F256 (Diff viewer completion).

TO (one line):

    61 of 257 registered items accepted. Next: F257 (Self-use track).

`F257` is the next unchecked STATUS line after F256, which the reviewer confirmed
at `64c3774f`.

PAIR S3, in `README.md`.

FROM (one line):

    | 5 | Operator Cockpit | 8 | 31 |

TO (one line):

    | 5 | Operator Cockpit | 9 | 31 |

APPEND S4, in `README.md`. The CAPABILITY slice below is inserted immediately
after the line

    modelled and deliberately not wired, per this feature's amendment A6).

and before the blank line that precedes `Full per-feature state:`. It is an
insertion; the F037 paragraph above it is not edited.

### The authored slices

<<<SLICE PLANF256R10
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
| T001 wire the highlighting | done | DECISIONS F256 D1 and D2 |
| T002 measure and record both halves | done | D4, D5, D6, Built State |
| T003 rule on the sidebar's treatment | done | DECISION F256 D3 |
| the integration gate and the package | done | READY_FOR_REVIEW at `c6775b3c` |
| resolve `R-0732` | done | this round |
| the STATUS closure and the PR | done | this round |

## Next Steps
1. The closure PR is NOT merged this session; it merges at the next feature's
   start through the Open PR Gate, which is the operator's review window.
2. The next feature by Rule A5 is F257 — Self-use track, the first unchecked
   STATUS line after F256.
3. `.agent/candidates.md` stays empty unless the closure gate raised one.

## Risks
- None open against F256. `R-0732` is resolved this round; the wider ledger's
  251 open findings belong to earlier features.
<<<END PLANF256R10

<<<SLICE DONER0732
Done: R-0732 — RESOLVED at F256 R4 by that round's refactor, and verified by the reviewer at `78e71b3c` by RUNNING the bundler rather than reading the handback. The finding was that `apps/ui/src/components/diff/DiffView.tsx` imported `apps/ui/src/api/diffHighlight` both STATICALLY and DYNAMICALLY, so the module was not code-split at all and DECISION F256 D1's stated benefit of no main-chunk weight went unmet. THE FIX IS ON DISK AND MEASURED: the grammar tables moved to their own module `apps/ui/src/api/diffHighlightGrammars.ts`, and at `78e71b3c` `npx vite build` exits 0 with ZERO output lines carrying both `dynamically imported` and `statically imported`, against exactly 1 at `e23dad09`; the build emits a real separate chunk, `dist/assets/diffHighlightGrammars-o9XqnLhb.js` at 1.70 kB, so the tables genuinely left the main bundle rather than being re-described as having left it. THE REFACTOR CHANGED NO VALUE, and the reviewer proved that by EXECUTING both grammar tables in two disposable worktrees and comparing them field by field: 11 language ids on both sides, no id's comment openers, string delimiters or keyword set differing, and 271 keywords in total on each — a refactor that quietly drops a keyword is the one failure that comparison exists to catch, and it did not happen. It stayed OPEN for the rest of the feature because only a reviewer may author a resolution and the repair had already landed inside the round that registered it; it is resolved here, in the closure round, so F256 closes with no open finding of its own. THE LESSON: a module imported both statically and dynamically by the SAME file is not split, and the bundler says so in a warning that exits 0 — a build whose exit code is the only thing read will report success for a lazy load that never happened.
<<<END DONER0732

<<<SLICE GATEF256R9
Gate: F256 R9 — the INTEGRATION GATE AND PACKAGE round, which satisfied closure preconditions 2, 3 and 5 and produced the review package F256 closes against. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran each one independently at `64c3774f`.

TRANSPORT COVERS THE EMISSION: the reviewer's own scratch original `.remedy-wt/f256-r9-block.md` predates the worker, and the committed `.agent/authored/f256-r9.md` blob at `c46042a9` is BYTE EQUAL to it at 23804 bytes, sha256 `8237c1e4fdcde6ab70e6a0a2a3abc79c559ee3e8d7f5e75d206f819f73d559db`. `.agent/plan.md` at `c47ad2ea` is byte-equal to its slice at 34 lines. At `c6775b3c` the append reconstructs byte for byte from the `f69bff0d` blob plus a newline plus GATEF256R8, the pre-round blob is a byte PREFIX, the negative control is REJECTED, and the last 6 blank-line units match the slice's paragraphs in order. The ledger moved as a round that registers and resolves nothing should: registrations 293 all DISTINCT, `^Done:` 43, `^Landed:` 11, the OPEN SET as a set 252, and `^Gate: F\d+ R\d+ — ` alone rising by one to 105. No file under `apps/`, `packages/`, `tests/` or `docs/` changed by a byte, and `git ls-files` over the build-output globs is empty.

THE INTEGRATION GATE IS GREEN AND THREE INDEPENDENT RUNS AGREE ON ITS COUNTS. The reviewer ran the full suite at `f69bff0d` before the round and again at `64c3774f` after it, and the worker ran it at `c6775b3c`: `python3 -B -m pytest -n auto -q` returned REAL exit 0 with 18150 passed and 20 skipped every time, at 104.3 s, 145.6 s and 160.0 s of wall clock. The wall clock differs by more than half; the COUNTS do not differ at all, which is the reading that matters. `apps/ui/dist` was verified not stale before each run. The integrity gate, reached through `packages.orchestration.integrity_gate.run_integrity_checks` because the `remedy` CLI is denied in this session, returned `passed=True` and `fail_count=0` with all five checks PASS.

THE PACKAGE IS READY AND THE REVIEWER READ IT OUT OF THE ZIP RATHER THAN OFF THE HANDBACK. Opening `remedy-review-20260828-233819-READY_FOR_REVIEW.zip` at its archived path, the manifest inside reports `package_status` READY_FOR_REVIEW, `committed_review_subject.base_commit` `0e8ab5b4f780b5265a6aa604ee89067399046b1e` — the branch point — and `head_commit` `c6775b3c41f1d1fa4b0f4bb7907307573855a61b`, which is C2 and therefore the accepted HEAD. `evidence_authoritative` reads True at `current_evidence.evidence_freshness`. The reviewer computed the file's SHA-256 independently over the 18076792 bytes on disk and got `5f18d7acdeab790b0f79181c7179023535b389ce0b76ec427f2765b20cda4ad5`, equal to the worker's figure. The nine verification runs each carry `selected` equal to their node-id count with one test file apiece, the packaging scan rejected zero strings with its red control reading True, and all nine `OUTPUT_HASH` lines read True.

THE WORKER'S SIX DECLARED DEVIATIONS ARE ALL ACCEPTED, AND TWO OF THEM CORRECT THE BLOCK. It reported that step (m)'s move was a NO-OP because the packaging pipeline already writes into the archive directory, so the package was never moved and the recorded path is where it was built — the reviewer confirmed the file is there. It reported that the manifest carries no top-level `evidence_authoritative` key where the block's wording implied one, and named the real location; the reviewer read it at that location and agrees. It flagged `review_subject_evidence_alignment.dirty_file_count_total` of 1 without letting it pass unremarked: the reviewer checked, and `review_subject.dirty_file_count_total` is 0 with `dirty_files` empty and `git_status_snapshot.status` OK, so the reviewed subject is clean and the 1 belongs to the alignment view, which lists no source or test file. It also declined to delete a stale zip left in the repository root by an earlier session, correctly, because it is untracked, gitignored and not this round's artifact.
<<<END GATEF256R9

<<<SLICE CAPABILITY
F256 diff viewer completion (the highlighting F037 only modelled is now rendered,
with the grammar tables split into their own lazily imported chunk so they leave
the main bundle; the 10k-line fixture measured end to end and its numbers
recorded — the route answers a 1,045,960-byte envelope in 0.1331 s, and the
client draws 48 rows of 10,002 however far the document grows — and the file
sidebar's visual treatment ruled by a named design authority and applied).
<<<END CAPABILITY

<<<SLICE PRBODY
## What changed

F256 finishes the rendered diff viewer F037 shipped, in the three pieces the
feature file scopes: T001 the highlighting actually rendered, T002 the 10k-line
budget measured end to end and recorded, T003 the file sidebar's visual treatment
ruled by a named authority.

## Why

F037 closed with three clauses of its own Goal and Acceptance UNMET, recorded
honestly in its amendment A6 rather than quietly dropped. F256 is the operator's
execution of that split, and it exists to close exactly those three.

## Key decisions

- **F256 D1** — Remedy writes its own lazy syntax bundles rather than adding a
  third-party highlighter.
- **F256 D2** — the syntax palette is four custom properties the shipped token
  sheet already defines; no new hue enters the product. `plain` is deliberately
  given no rule.
- **F256 D3** — the sidebar takes its treatment from the diff body's own
  vocabulary, and Remedy draws NO proportional stats bar; the two counts carry
  the magnitude exactly.
- **F256 D4** — the end-to-end server budget is guarded by a scale RATIO measured
  on one machine in one run, not by an absolute second count that would report
  machine speed on a hosted runner.
- **F256 D5** — the client half is guarded by an EXACT bounded-window invariant
  rather than by a duration, because a millisecond of JavaScript is mostly the
  JIT; the durations are recorded beside it.
- **F256 D6** — a vitest red-proof runs the worktree's mutated sources against
  the primary checkout's `node_modules`, because vitest cannot run inside a
  worktree; this satisfies guardrail G5 rather than waiving it.

## The measurement, recorded

Written into the Built State of `docs/roadmap/features/T5_F256.md`, and pinned by
a cross-check that every recorded number is present in the file that produced it:
the parser at a median of 0.105 s for 10,000 body lines; the whole server path at
0.1331 s for a 1,045,960-byte JSON envelope, with a scale ratio of 4.97 against a
ceiling of 20; the client model at 0.678 ms building 10,002 rows, of which the
virtual window draws 48 — and the same 48 at 100,020 rows.

## How to review

Start with the Built State section of `docs/roadmap/features/T5_F256.md`, which
states what exists and what was measured. The two measurement tests are
`tests/ui_server/test_diff_endpoint.py::TestDiffEndpointPerfBudget` and the
`the ten-thousand-line diff through the client model` block of
`apps/ui/src/api/diffViewModel.test.ts`. The sidebar ruling is enforced by
`tests/ui_contracts/test_diff_file_sidebar.py::TestTheSidebarWearsTheRuledTreatment`.

Full suite: `python3 -m pytest -n auto -q` → 18150 passed, 20 skipped, exit 0.
Frontend: `npx vitest run` in `apps/ui` → 631 passed in 33 files; `npx tsc
--noEmit` → exit 0.

## Verdict and findings

Latest live review verdict: PASS. Findings registered by F256: one, `R-0732`,
registered and repaired in the same round and RESOLVED in the closure round. No
finding is left open against this feature.

## Runtime actuals

Rounds 1–10 across 2 sessions. Wall clock, models, tokens and cost:
not-measured — the ledger does not carry them for this feature, and a guess would
be worse than the absence.
<<<END PRBODY

`PLANF256R10` is a WHOLE-FILE replacement of `.agent/plan.md`. `DONER0732` and
`GATEF256R9` are APPENDS to `.agent/live_review.md`, in that order — the pre-round
blob, one newline, then `DONER0732`, one newline, then `GATEF256R9`. `CAPABILITY`
is the S4 insertion into `README.md`. `PRBODY` is the pull request's body and
reaches no tracked file.

### Done when

G1 HYGIENE AND STRUCTURE. Read `.agent/STOP` with `os.path.exists` before C0a and
again before C3; report both, and stop after the commit in hand if it exists.
Report `git rev-parse HEAD` before C0a — it must equal `64c3774f` —
`git branch --show-current`, and `git status --porcelain | wc -l` after each of
C0a, C0b, C1, C2 and C3. Over `64c3774f..<C3>` report `git diff --name-only` and
both residues against the change set, printed in both directions and both
expected empty. Report `git diff --stat 64c3774f..<C3>` restricted to `apps/`, to
`packages/`, to `tests/` and to `docs/roadmap/features/` — all four expected to
print NOTHING. Report each commit's insertions from `git diff --numstat`, each
under 500, and that C0a, C0b, C1, C2 and C3 are single-parent. Report the counts
of lines beginning `<<<SLICE ` and `<<<END ` in `.agent/plan.md`,
`.agent/live_review.md`, `docs/roadmap/STATUS.md` and `README.md` — each expected
0 — beside `.agent/authored/f256-r10.md` as the non-zero control. Report
`git ls-files .remedy-wt | wc -l`, expected 0.

G2 TRANSPORT. One digest comparison: sha256 of
`git show <C0a>:.agent/authored/f256-r10.md` against the reviewer's own original
at `.remedy-wt/f256-r10-block.md`, reporting both digests, the byte length and
equality; that original predates this worker. Report that
`<C0b>:.agent/authored/f256-r10.md` and `<C0b>:.agent/last_block.md` are ONE blob
id.

G3 THE PLAN AT C1. `.agent/plan.md` at C1 equals PLANF256R10 including the
trailing newline — report `True` or `False` — with `wc -l` under 50 and the counts
of lines exactly `## Goal` and exactly `## Next Steps`.

G4 THE RECORD AT C2. The `64c3774f` blob of `.agent/live_review.md` plus a newline
plus DONER0732 plus a newline plus GATEF256R9 equals the C2 blob — report `True`
or `False` — the pre-round blob is a byte PREFIX, and a NEGATIVE CONTROL flipping
one byte at an offset your script confirms lies INSIDE THE FIRST appended
paragraph reports the equality now `False`. Let N be the appended text's paragraph
count, COUNTED BY YOUR SCRIPT, ignoring an empty trailing unit; report N and that
the LAST N blank-line units match those paragraphs IN ORDER. Report that
`Done: R-0732 — ` occurs exactly once and that `Gate: F256 R9` occurs exactly once.

G5 THE LEDGER AT C2. Over the C2 blob and the `64c3774f` blob beside it, report
`^- R-\d+ — ` and whether all DISTINCT, `^Done: R-\d+ — `, `^Landed: R-`,
`^Gate: F\d+ R\d+ — `, and the OPEN SET as a set. This round RESOLVES ONE finding
and registers none, so: registrations UNMOVED at 293, `^Landed: R-` UNMOVED,
`^Done: R-\d+ — ` rises by exactly ONE, `^Gate: F\d+ R\d+ — ` rises by exactly
ONE, and the OPEN SET FALLS BY EXACTLY ONE, from 252 to 251. Report that `R-0732`
is NOT in the open set at C2 and WAS in it at `64c3774f`.

G6 THE CLOSURE EDIT AT C3. For each of S1, S2 and S3 report the count of the FROM
string in its target at `64c3774f` — each must be 1 — and the count of the TO
string at C3, each also 1, with the FROM count at C3 now 0. For S4 report that the
CAPABILITY text occurs exactly once at C3 and that the F037 paragraph above it is
byte-unchanged. Report `git diff --numstat 64c3774f..<C3> -- docs/roadmap/STATUS.md`
— expected exactly 1 insertion and 1 deletion — and confirm that the count of
lines matching `^- \[x\] F\d{3} — ` in `docs/roadmap/STATUS.md` at C3 EQUALS the
number the README's `N of 257` line states. Report both numbers.

G7 THE DOCS GATE AND THE SUITES, at C3, in the PRIMARY checkout, one pytest
process at a time, each with its exit code and its own passed/failed line:
`tests/docs/` in full; `tests/ui_contracts/`; `tests/ui_server/`; and the canary
`tests/cli/test_golden_path.py`. Every one must be exit 0. The reviewer measured,
in a disposable worktree at `64c3774f`, that applying S1 ALONE — the STATUS flip
with `README.md` untouched — turns `tests/docs/` RED at 2 failed and 293 passed,
naming `test_the_readme_accepted_count_equals_the_status_count` and
`test_the_readme_tier_table_done_column_matches_the_ledger`; you do not need to
reproduce that, but state in the handback that the four edits travel in ONE commit
for that measured reason. If any suite is red, STOP and hand back with the FULL
untruncated failure list.

G8 THE PULL REQUEST. After C3 is committed and pushed, create the PR with
`gh pr create`, title `F256 — Diff viewer completion`, body exactly the PRBODY
slice, base `main`, head `feature/f256-diff-viewer-completion`. Report the PR
NUMBER and URL, and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
afterwards. DO NOT MERGE IT. Report that C3 is the last commit on the branch by
printing `git log --oneline -n 1` and confirming it is the closure commit.

### Handback

Rewrite `.agent/handoff.md` INSIDE C3 — it is part of the closure commit's path
set — per docs/agents/handback_template.md. It carries: `SESSION 2 of feature
F256 · round 10 · THE CLOSURE`; the range `64c3774f..HEAD`; a per-commit
changed-files table with `+/-` from `git diff --numstat`; ONE LINE PER GATE G1
through G8 with its real result, with G8's PR number filled in after the fact
being impossible — so state instead that the PR is created after C3 and record its
number in your final message; the deviations; and the item-status table with every
C-item and every gate appearing exactly once.

It also carries, as its own labelled section, the CLOSURE RECORD: evidence job
`f256-closure`, the package filename, its SHA-256, the archived path, and the
accepted HEAD `c6775b3c41f1d1fa4b0f4bb7907307573855a61b`.

Include the grep proof the closure protocol's step 5 requires: that every piece of
reviewer-authored applied text — the STATUS line, the README pins, the CAPABILITY
paragraph and the two `.agent/live_review.md` appends — is byte-identical to the
authored slice or pair it came from.

State that the next expected action is the Open PR Gate at the NEXT feature's
start, that this PR is deliberately unmerged, and that Rule A5's next feature is
F257 — Self-use track.

Do not write a `Done:`, `Gate:` or `Landed:` paragraph of your own anywhere —
DONER0732 and GATEF256R9 are the reviewer's text and are the only things entering
`.agent/live_review.md`.
