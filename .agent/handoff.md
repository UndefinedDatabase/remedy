# Handback — F040 · SESSION 2 · round 6 — T002 PART 1: THE CLIENT'S DIGEST SEAM

> Written by the WORKER in C6, the last commit of the bundle. Every exit code
> below is REAL, taken from `subprocess.run(...).returncode` inside a script
> under the gitignored `.remedy-wt/`; not one was read through a pipe.

## Session

SESSION 2 of feature F040 · round 6 · rounds so far 6.

The soft limit (25 rounds / 7 sessions, amend0827 rule 6) is not approached, so
no scope report is owed. `.agent/STOP` did not exist at any reading this round.

## Range

Review of `4e5e9bf8`..`HEAD` on branch `feature/f040-completion-digest`. The
base is round 5's handback commit and was the tip of the branch when this round
opened. No new branch was cut, no pull request opened, nothing merged, nothing
force-pushed.

**T002's DECIDABLE HALF IS BUILT. NO `.tsx` AND NO CSS LANDED THIS ROUND.** The
browser now has a pure `apps/ui/src/api/jobDigest.ts` that decodes the digest
envelope, names the endpoint's path and turns the cost section into a cost-line
RULE — and nothing else. The hero card component, its CSS conformance guard and
the trigger / dismiss / last-seen rule are all still open, deliberately: a
component with no test harness is exactly what this round was told not to build.
NO PYTHON PRODUCTION CODE CHANGED. `packages/orchestration/job_digest.py` and
`packages/orchestration/ui_server.py` are untouched; the only production edit
outside the new module is the four-line comment and the `export` keyword
PAIRACTUAL adds to `apps/ui/src/api/costMetric.ts`.

## Commits

### b9873fc5 docs(f040): save the round 6 block

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f040-r6.md` | +363 −0 | C0a — the block, copied with `shutil.copyfile` from `.remedy-wt/f040-r6-block.md`, never retyped |

### fc2acc0e docs(f040): mirror the round 6 block

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +272 −230 | C0b — the same bytes, the same `shutil.copyfile` call |

### 3138e75e docs(f040): retarget the plan at the client digest seam

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +19 −18 | C1 — slice PLAN6 applied byte for byte; SESSION 2 / round 6, round 5's row settled to `round 5, PASS`, T002 split into three rows so the trigger rule and the card are visibly still open |

### 14cd19b7 docs(f040): book the round 5 verdict and rule D7

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +6 −0 | C2 — slice RECORD6 appended: the R5 PASS gate line, `Done: R-0754`, DECISION F040 D7. Append-only; the base bytes are a prefix of the result |

### ea6b85a7 feat(f040): add the client digest seam and export the exactness basis

| Path | +/- | Reason |
|------|-----|--------|
| `apps/ui/src/api/costMetric.ts` | +6 −2 | C3 — pair PAIRACTUAL, a REPLACEMENT: `ACTUAL_BASIS` becomes `export const` and its WHY comment says why |
| `apps/ui/src/api/jobDigest.ts` | +217 −0 | C3 — the seam: four envelope types, `JOB_DIGEST_VERSION`, `decodeJobDigest`, `digestCostLine`, `jobDigestPath`, and a header naming the four deliberate absences |

The two halves are ONE commit by block constraint 8: `jobDigest.ts` imports the
symbol the pair exports, so landing the import before the export would be a
module that does not resolve.

### f7bf0469 test(f040): pin the client digest seam in vitest

| Path | +/- | Reason |
|------|-----|--------|
| `apps/ui/src/api/jobDigest.test.ts` | +157 −0 | C4 — 16 vitest cases over the three exports, including the one that reads exactness THROUGH the imported `ACTUAL_BASIS` rather than through a retyped literal |

### ab8d02dc test(f040): guard the digest seam purity and its one-source basis

| Path | +/- | Reason |
|------|-----|--------|
| `tests/ui_contracts/test_job_digest_card_contract.py` | +280 −0 | C5 — 16 Python cases reading the TypeScript as TEXT: the purity, the one-source cost string, the single home across the directory, and the absence of presentation copy — each paired with a positive control |

### (this commit) docs(f040): write the round 6 handback

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | C6 — this file. A handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/g3-negative-control HEAD` | rc 0 — G3's on-disk negative control |
| `git worktree remove --force .remedy-wt/g3-negative-control` | rc 0 — removed by exact path; `git worktree list` no longer holds it |
| `git worktree add --detach .remedy-wt/g6-red-proof HEAD` | rc 0 — G6's two mutations of `jobDigest.ts` |
| `git worktree remove --force .remedy-wt/g6-red-proof` | rc 0 — removed by exact path; `git worktree list` no longer holds it |
| `git push origin feature/f040-completion-digest` | after C6 — see the closing line |

No pull request created, none edited, none merged. No `gh` command run. No
force-push. The `remedy` console script was never invoked (block constraint 11)
and nothing this round needed it, so no `python3 -m apps.cli.main` substitute
was needed either.

## Verification

Eight gates, eight REAL exit codes. Every gate ran at a commit strictly earlier
than C6, which writes this file.

    G1 TRANSPORT, at C0b (fc2acc0e)                        REAL EXIT 0
    G2 THE PLAN, at C1 (3138e75e)                          REAL EXIT 0
    G3 THE RECORD APPEND, at C2 (14cd19b7)                 REAL EXIT 0
    G4 THE LEDGER, at C2 (14cd19b7)                        REAL EXIT 0
    G5 THE PAIR AND THE SINGLE HOME, at C3 (ea6b85a7)      REAL EXIT 0
    G6 THE GUARD AND ITS RED PROOF, at C5 (ab8d02dc)       REAL EXIT 0
    G7 VITEST AND THE TYPECHECK, at C5 (ab8d02dc)          REAL EXIT 0 (both nodes)
    G8 THE SUITES AND THE TREE, at C5 (ab8d02dc)           REAL EXIT 0

### G1 TRANSPORT — REAL EXIT 0

One sha256 over three files, all three EQUAL. The block states no expected
digest, so this is a measurement and not a match against a number I was handed.

    274cd28a08ab7231cf84fbe606bfb2b089d32947f0c20acf60351cf16172d928  29186 bytes  .remedy-wt/f040-r6-block.md
    274cd28a08ab7231cf84fbe606bfb2b089d32947f0c20acf60351cf16172d928  29186 bytes  .agent/authored/f040-r6.md
    274cd28a08ab7231cf84fbe606bfb2b089d32947f0c20acf60351cf16172d928  29186 bytes  .agent/last_block.md
    ALL THREE EQUAL: True
    committed last_block sha256 274cd28a…172d928 29186   (git show, rc 0)
    committed authored  sha256 274cd28a…172d928 29186   (git show, rc 0)

The two `.agent/` copies were also read back OUT of git and both COMMITTED blobs
hash to the same digest at the same 29186 bytes.

### G2 THE PLAN — REAL EXIT 0

    PLAN6 slice    sha256 c53180516ca54edb9480ffb9dc549f9b731f9b252a12d02100e36c049968acaa  2052 bytes
    .agent/plan.md sha256 c53180516ca54edb9480ffb9dc549f9b731f9b252a12d02100e36c049968acaa  2052 bytes
    BYTE-EQUAL: True
    line count: 41 (< 50: True )
    holds '## Goal': True   holds '## Next Steps': True

### G3 THE RECORD APPEND — REAL EXIT 0

The pre-commit length was RE-MEASURED here rather than taken from the block; it
agrees with the 1678133 the reviewer read at `4e5e9bf8`. N was COUNTED by the
script (3 blank-line units: the gate line, `Done: R-0754`, DECISION F040 D7),
never asserted.

    BASE      1678133 bytes  sha256 370f82580e5a5bc31e0f1e0930753e6d8559312a922da935a76050e206c38e06
    RECORD6   9267 bytes  sha256 13a130ea5bb17b30b8380ff9c97e2118521f0a7d8b07e0549e93e4e0ed785f37
    COMMITTED 1687401 bytes  sha256 0af1aa9a30a15e637395007653fa5b9ec3edc134025d5b1324675bf2f69a9364
    ARITHMETIC 1678133 + 1 + 9267 = 1687401  vs committed 1687401  match True
    N (paragraphs of RECORD6, counted by this script): 3
    (a) WHOLE RECONSTRUCTION: True
    (b) PARAGRAPH ORDER (last 3 units equal RECORD6's 3, in order): True
    BASE BYTES ARE A PREFIX OF THE COMMITTED FILE: True

    worktree add -> 0
      CONTROL (unflipped, read from the worktree): (a) WHOLE: True  (b) ORDER: True
      FLIPPED byte at offset 1678174 (b' ' -> b'\x00'), inside appended paragraph 1
      flipped: (a) WHOLE: False  (b) ORDER: False  (both must be False)
    worktree remove -> 0
    git worktree list still holds it: False
    /home/decodeux/Repos/remedy  14cd19b7 [feature/f040-completion-digest]

The negative control was performed ON DISK inside the disposable worktree, with
the unflipped control read first; both readings rejected the flipped bytes and
both accepted the unflipped ones.

### G4 THE LEDGER — REAL EXIT 0

    REGISTERED '^- R-\d+ — ': before 315 distinct, after 315 distinct, ADDED [], REMOVED []
    RESOLVED   '^Done: R-\d+': before 53 distinct, after 54 distinct, ADDED ['R-0754'], REMOVED []
    DECISION F040 D\d+: before 6 distinct, after 7 distinct, ADDED ['D7'], REMOVED []
    '^Gate: F040 R5 — ' lines: 1 (must be exactly 1)
    OPEN COUNT: before 262, after 261, fall from 262 -> 261 (delta -1)
       newly closed this round: ['R-0754']

Patterns recorded so the count can be reproduced: registered ids by
`(?m)^- (R-\d+) — `, resolved by `(?m)^Done: (R-\d+)`, decisions by
`DECISION F040 (D\d+)`. This round registers NO new finding, as ordered. OPEN
FINDINGS: **261**, down one from 262 because R-0754 is now booked `Done:`.

### G5 THE PAIR AND THE SINGLE HOME — REAL EXIT 0

"Before" is read from the HEAD~1 BLOB, so the reading is over real stored bytes
rather than over memory.

    TO contains FROM: False  (constraint 14: a REPLACEMENT)
    BEFORE (HEAD~1 blob, 9184 bytes): FROM 1x, TO 0x
    AFTER  (HEAD blob,   9482 bytes): FROM 0x, TO 1x
    PAIR: PASS

    SWEEP: 35 non-test .ts sources under apps/ui/src/api/ , comment-stripped:
      0  actionClass.ts            0  decisionFilter.ts
      0  brainStream.ts            0  decisionFocus.ts
      0  brainStreamDeps.ts        0  decisionNonce.ts
      0  brainStreamDriver.ts      0  decisionOrder.ts
      0  brainStreamHost.ts        0  decisionOutcome.ts
      0  brainStreamRunner.ts      0  decisionSend.ts
      0  brainStreamSession.ts     0  decisionSubmit.ts
      0  budgetTick.ts             0  diffHighlight.ts
      1  costMetric.ts             0  diffHighlightGrammars.ts
      0  costReconciliation.ts     0  diffViewModel.ts
      0  costTicker.ts             0  feedFocus.ts
      0  decisionAnswer.ts         0  feedRow.ts
      0  decisionAnswerFlow.ts     0  feedScroll.ts
      0  decisionCard.ts           0  humanize.ts
      0  decisionClarificationForm.ts  0  humanizeCatalog.ts
                                   0  jobDigest.ts
                                   0  recency.ts
                                   0  remedyApi.ts
                                   0  types.ts
                                   0  useBrainStream.ts
    FILES NAMING THE LITERAL: [('costMetric.ts', 1)]
    total occurrences 1; exactly ONE and in costMetric.ts: True
    jobDigest.ts contains "ACTUAL_BASIS": True; imports it from "./costMetric": True

THE SWEEP'S REACH IS THE ABSENCE'S WIDTH, so the files are named rather than
counted: **35** non-test `.ts` sources under `apps/ui/src/api/`, every one read
and comment-stripped, every one's hit count printed. The gate's own output is a
single column; it is re-flowed into two columns here to fit and nothing else
about it is changed. The one occurrence is `costMetric.ts:62`,
`export const ACTUAL_BASIS = "actual";` — the pair's own line.

### G6 THE GUARD AND ITS RED PROOF — REAL EXIT 0

Control FIRST in both checkouts. `__pycache__` was purged before every run and
every run used `python3 -B`. Both mutations edit `jobDigest.ts` inside the
disposable worktree and each was reverted before the next.

    STEP 1 — the guard at C5, in the primary checkout
      [primary] REAL EXIT CODE: 0   ['16 passed in 0.23s']

    STEP 2 — worktree add g6-red-proof -> 0
      original apps/ui/src/api/jobDigest.ts  10400 bytes  sha256 2df117e09ea156871144a2e424177d704611ea417bf2bc91ae1a046acad38074

    STEP 3 — the UNMUTATED CONTROL, inside the worktree, FIRST
      [control] REAL EXIT CODE: 0   ['16 passed in 0.21s']

    STEP 4 — MUTATION M1 a real Date.now() call inside digestCostLine's body
      mutated file 10459 bytes  sha256 411c88b98a0e7feefc6bc7be7661eae97f65f98a8cf14a8282e0a94a56d0f5cb
      [M1] REAL EXIT CODE: 1   ['1 failed, 15 passed in 0.22s']
      [M1] DEAD TESTS (1):
          tests/ui_contracts/test_job_digest_card_contract.py::TestTheDigestSeamIsPure::test_the_module_names_none_of_the_forbidden_capabilities
      REVERTED by exact path .remedy-wt/g6-red-proof/apps/ui/src/api/jobDigest.ts; bytes equal the original: True

    STEP 4 — MUTATION M2 the imported ACTUAL_BASIS comparison replaced by the literal
      mutated file 10396 bytes  sha256 011134bfc260c1aaefca8607e219d9fc309d9457f6873ae443da09ee85bc7aa9
      [M2] REAL EXIT CODE: 1   ['2 failed, 14 passed in 0.22s']
      [M2] DEAD TESTS (2):
          tests/ui_contracts/test_job_digest_card_contract.py::TestTheExactnessStringHasOneHome::test_the_digest_seam_never_restates_the_literal
          tests/ui_contracts/test_job_digest_card_contract.py::TestTheExactnessStringHasOneHome::test_the_literal_has_exactly_one_home_in_the_whole_api_directory
      REVERTED by exact path .remedy-wt/g6-red-proof/apps/ui/src/api/jobDigest.ts; bytes equal the original: True

    STEP 5 — RESTORED, re-run
      [restored] REAL EXIT CODE: 0   ['16 passed in 0.20s']
      restored bytes equal the original: True  sha256 2df117e09ea156871144a2e424177d704611ea417bf2bc91ae1a046acad38074

    STEP 6 — removing worktree .remedy-wt/g6-red-proof
      worktree remove -> 0
      git worktree list still holds g6-red-proof: False
      /home/decodeux/Repos/remedy  ab8d02dc [feature/f040-completion-digest]

M1 killed the purity assertion and nothing else, which is the narrow answer a
purity guard should give. M2 killed TWO — the module's own zero AND the
directory-wide single-home count — which is the right pair: the literal reappears
in `jobDigest.ts` and the directory therefore has two homes for it at once. M1
was written as a REAL call whose value is consumed
(`const seenAtMs = Date.now(); … seenAtMs > 0 ? cost.value : cost.value`) rather
than as a bare token, so it could not be killed by a guard that merely greps a
word out of dead code.

### G7 VITEST AND THE TYPECHECK — REAL EXIT 0 for both nodes

Reached through the pytest nodes, never through a direct `npx` call, which is
refused to this session class.

    $ python3 -m pytest "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" -q -rs
    4 passed in 1.23s
    REAL EXIT CODE: 0        NODE STATUS: PASSED — not skipped, no skip report emitted under -rs

    $ python3 -m pytest tests/ui_server/test_dashboard_contract.py -k typescript -q -rs
    1 passed, 73 deselected in 2.06s
    REAL EXIT CODE: 0        NODE STATUS: PASSED — not skipped, no skip report emitted under -rs

Both match the reviewer's base measurement of 4 passed and 1 passed, neither
skipped. WHAT THOSE TWO NODES ACTUALLY DO, read from their source rather than
assumed: `test_vitest_passes` (`tests/orchestration/test_test_runner.py:403-411`)
spawns `npx vitest run` in `apps/ui` and asserts its returncode is 0;
`test_typescript_compiles` (`tests/ui_server/test_dashboard_contract.py:463-479`)
SKIPS when `apps/ui/node_modules/.bin/tsc` is absent and otherwise runs that
local binary with `--noEmit`. Both toolchains are present here — vitest 2.1.9 and
the local `tsc` — so neither took its skip branch, and `tsc --noEmit` really
compiled the two new `.ts` files. The vitest config's `include` is
`src/**/*.test.ts`; a probe listed the 34 files that pattern collects and
`apps/ui/src/api/jobDigest.test.ts` is among them, so the new suite is inside the
run whose exit code that node grades. The 1.2s wall time is the warm
`apps/ui/node_modules/.vite` cache, which is present.

NO TYPESCRIPT MUTATION COLOUR WAS RUN, and none was ordered. The reason is the
block's and it is a measured one, not a convenience: direct `npx vitest` and
`npm run test:unit` are REFUSED to this session class before execution, and
`apps/ui/node_modules` is gitignored and therefore absent from any disposable
worktree, so a mutation there would be red for every possible module and would
prove nothing. The colour this round DOES carry is G6's, over the Python guard,
which needs no `node_modules` and was red-proved twice. A permission boundary was
treated as a finding to report, never as an obstacle to route around.

### G8 THE SUITES AND THE TREE — REAL EXIT 0

Five suites, run SERIALLY, each with its own REAL exit code:

    $ python3 -m pytest tests/ui_contracts/ -q
       715 passed, 4 skipped in 6.43s
       REAL EXIT CODE: 0   base 699 -> now 715   difference +16
    $ python3 -m pytest tests/orchestration/test_job_digest.py -q
       46 passed in 0.42s
       REAL EXIT CODE: 0   base 46 -> now 46   difference +0
    $ python3 -m pytest tests/ui_server/ -q
       515 passed in 34.22s
       REAL EXIT CODE: 0   base 515 -> now 515   difference +0
    $ python3 -m pytest tests/docs/ -q
       295 passed in 0.60s
       REAL EXIT CODE: 0   base 295 -> now 295   difference +0
    $ python3 -m pytest tests/cli/test_golden_path.py -q
       42 passed in 20.84s
       REAL EXIT CODE: 0   base 42 -> now 42   difference +0

    --- the tree ---
    $ git status --porcelain  -> exit 0, 0 lines, EMPTY: True
    $ git ls-files --others --exclude-standard -> count 0

    --- per-commit insertions, C0a through C5 ---
       b9873fc5  +363   -0     under 500   docs(f040): save the round 6 block
       fc2acc0e  +272   -230   under 500   docs(f040): mirror the round 6 block
       3138e75e  +19    -18    under 500   docs(f040): retarget the plan at the client digest seam
       14cd19b7  +6     -0     under 500   docs(f040): book the round 5 verdict and rule D7
       ea6b85a7  +223   -2     under 500   feat(f040): add the client digest seam and export the exactness basis
       f7bf0469  +157   -0     under 500   test(f040): pin the client digest seam in vitest
       ab8d02dc  +280   -0     under 500   test(f040): guard the digest seam purity and its one-source basis

THE RISE THE GATE ASKED FOR: `tests/ui_contracts/` was **699 passed with 4
skipped** at the base and is **715 passed with 4 skipped** at C5 — a difference
of **+16**, which is exactly the number of tests C5 adds
(`test_job_digest_card_contract.py` collects 16 and all 16 pass). The four skips
are pre-existing and unmoved. The other four suites are unchanged, which is what
a round that touches no Python production code should produce.

Also run, though no gate ordered it:
`python3 -m ruff check tests/ui_contracts/test_job_digest_card_contract.py` —
REAL EXIT 0, "All checks passed!".

## Authored-text proofs

Every reviewer-authored unit was extracted MECHANICALLY from
`.remedy-wt/f040-r6-block.md` by `.remedy-wt/r6_extract.py`, which slices
between the `<<<BEGIN NAME` / `<<<END NAME` marker lines (markers excluded, the
newline ending the last content line included) and writes each to
`.remedy-wt/r6units/<NAME>.txt`. Nothing was retyped.

| Unit | Bytes | sha256 | Applied to | Proof |
|---|---|---|---|---|
| the block itself | 29186 | `274cd28a…172d928` | `.agent/authored/f040-r6.md`, `.agent/last_block.md` | G1 — three-way disk-to-disk equality, plus both committed blobs re-hashed from `git show` |
| PLAN6 | 2052 | `c5318051…968acaa` | `.agent/plan.md` | G2 — byte-equality against the committed file |
| RECORD6 | 9267 | `13a130ea…d785f37` | `.agent/live_review.md` | G3 — whole reconstruction + paragraph order + prefix, with an on-disk negative control |
| PAIRACTUAL-FROM | 102 | `fcc7a50e…fc276a2b` | `apps/ui/src/api/costMetric.ts` | G5 — 1x in the HEAD~1 blob, 0x in the HEAD blob |
| PAIRACTUAL-TO | 400 | `16bc4a45…2c5e44b4b` | `apps/ui/src/api/costMetric.ts` | G5 — 0x before, exactly 1x after |

The three SPECs (C3's module, C4's vitest suite, C5's Python guard) are
DESCRIBED production code, not slices, so they carry no byte-equality proof;
they are graded by G5, G6, G7 and G8 instead.

## Deviations & assumptions

1. **`jobDigestPath` TAKES THE SPEC'S LITERAL INLINE PARAMETER TYPE, NOT A NAMED
   `JobDigestRequest` INTERFACE.** The C3 SPEC writes the signature as
   `jobDigestPath(request: { jobId: string; token: string; baseUrl?: string })`
   and I applied it as written. The pattern it also points at,
   `diffEnvelopePath`, uses a named `DiffEnvelopeRequest` interface and argues in
   its own comment that naming the fields is the cheapest guard against an
   argument swap. Both readings were available; the block wins, so the inline
   shape shipped. Structurally the two are identical to every caller, and a later
   round can name it without changing a call site. Declared because it is a
   visible departure from the sibling this SPEC told me to follow.
2. **`ownership` IS TYPED `string[]`, WHICH THE GOLDENS DO NOT DETERMINE.** The
   SPEC says to read a stored golden for the exact shape rather than infer it.
   Every one of the four goldens stores `"ownership": []`, so the ELEMENT type is
   not observable there. It was taken from the two places that do state it:
   `docs/roadmap/features/T5_F040.md:41` ("top ownership sentences (≤3)") and
   DECISION F040 D3 in `job_digest.py`, which names F035 as the producer of the
   ownership SENTENCES. `decodeJobDigest` reads it defensively — a non-array
   becomes `[]` and a non-string entry is dropped — so a server that later ships
   a richer shape degrades to no sentences rather than to a wrong render.
3. **`decodeJobDigest` ACCEPTS AN EMPTY `job_id` RATHER THAN REFUSING IT.** The
   SPEC's refusals are "a missing or non-string `job_id`", and an empty string is
   neither. It is also a shape the server really emits:
   `build_job_digest` writes `str(sources.job_id or "")`, so a job whose id was
   never recorded produces `""`. Refusing it would turn a legitimate envelope
   into "no digest at all" and hide exactly the state the digest exists to
   report. The choice is written into the function's own comment so the next
   reader does not have to rediscover it.
4. **`jobDigest.ts` CARRIES ITS OWN PRIVATE `objectOf`.** `costMetric.ts` and
   `budgetTick.ts` each already carry a private copy of this three-line total
   reader; this is the third, and it is deliberate rather than an oversight in a
   round whose whole theme is single homes. A defensive `unknown`-to-object
   reader is not a RULE — it encodes no decision that two modules could disagree
   about — whereas the exactness string is, which is why that one is imported and
   this one is not. Extracting a shared helper would also be an unordered edit to
   two files outside this round's change set.
5. **THE GUARD CARRIES ONE TEST THE SPEC DID NOT ORDER:**
   `TestTheDigestSeamIsPure::test_the_module_promises_those_absences_in_prose_as_well`.
   The SPEC ordered the stripping and ordered the docstring to explain why the
   stripping makes the guard honest, both of which are done. This extra case
   asserts the header still NAMES `Date.now`, `localStorage`, `fetch` and
   `crypto` as deliberate absences — AGENTS.md's "deliberate absences are
   documented where a reader would search for them" — so the prose the stripping
   removes cannot silently disappear along with it. It is additive and pins no
   behaviour the SPEC forbade.
6. **C0a AND C0b PRECEDE C1, SO TWO COMMITS LAND WHILE `.agent/plan.md` STILL
   NAMES ROUND 5.** This is the block's own bundle order together with its
   constraint 3 ("C1 is the FIRST substantive commit"), not a departure from it,
   and it is the established shape of every round of this feature. Noted so a
   reader auditing the AGENTS.md commit gate against the first two commits does
   not have to reconstruct why.
7. **THE ORDERED COMMIT SEQUENCE WAS FOLLOWED EXACTLY.** Seven commits, in the
   block's order, C0a → C0b → C1 → C2 → C3 → C4 → C5, and this handback as C6.
   No extra commit, none dropped, none reordered, and no amend.
8. **NO TYPESCRIPT MUTATION COLOUR WAS RUN** — see G7 for the measured reason.
   None was ordered, and the absence is stated here as well as there so a reader
   auditing the round's colour does not have to infer it from a missing gate.
9. No commit subject carries a leading-slash token, an absolute path, a
   secret-like string or a `Co-Authored-By` trailer (block constraint 12); every
   commit's insertion count is under 500 (G8), so no oversize-commit declaration
   is owed.
10. Both disposable worktrees were removed BY EXACT PATH
    (`.remedy-wt/g3-negative-control`, `.remedy-wt/g6-red-proof`), never by
    glob, and `git worktree list` was re-read after each removal. All scratch
    scripts live under the gitignored `.remedy-wt/` and none is committed —
    `git ls-files --others --exclude-standard` counts 0.

## Item status

| Item | Status | Reason |
|--------|----------|------------------------------|
| C0a save the block to `.agent/authored/f040-r6.md` | done | `shutil.copyfile`; b9873fc5 |
| C0b mirror into `.agent/last_block.md` | done | `shutil.copyfile`; fc2acc0e |
| C1 rewrite `.agent/plan.md` from PLAN6 | done | byte-equal; 3138e75e |
| C2 append RECORD6 to `.agent/live_review.md` | done | append-only; 14cd19b7 |
| C3 pair PAIRACTUAL + `apps/ui/src/api/jobDigest.ts` | done | one commit, both halves (constraint 8); ea6b85a7 |
| C4 create `apps/ui/src/api/jobDigest.test.ts` | done | 16 vitest cases; f7bf0469 |
| C5 create `tests/ui_contracts/test_job_digest_card_contract.py` | done | 16 cases, all passing; ab8d02dc |
| C6 rewrite `.agent/handoff.md` | done | this commit |
| G1 TRANSPORT | done | REAL EXIT 0 |
| G2 THE PLAN | done | REAL EXIT 0 |
| G3 THE RECORD APPEND | done | REAL EXIT 0 |
| G4 THE LEDGER | done | REAL EXIT 0; open count 262 → 261 |
| G5 THE PAIR AND THE SINGLE HOME | done | REAL EXIT 0; 35 files swept, 1 home |
| G6 THE GUARD AND ITS RED PROOF | done | REAL EXIT 0; two mutations, both red at exit 1 |
| G7 VITEST AND THE TYPECHECK | done | REAL EXIT 0 and 0; both nodes PASSED, neither skipped |
| G8 THE SUITES AND THE TREE | done | REAL EXIT 0 ×5; clean tree; ui_contracts 699 → 715 |

## Findings state

| Id | State |
|---|---|
| R-0570 | OPEN — routed to the paydown branch |
| R-0752 | OPEN — routed to the paydown branch |
| R-0753 | OPEN — this feature's documented risk: the persisted actuals record has no money field, so the digest's cost basis can only answer `absent` in production |
| R-0754 | RESOLVED — booked `Done: R-0754` by C2 (14cd19b7), discharged in round 5 by the four envelope goldens, their reader and AMENDMENT A3 |

This round registered NO new finding, as ordered. Open findings after C2:
**261**.

## Next

**T002 PART 2 — the trigger, dismiss and last-seen rule**, as a PURE function
over an INJECTED seam, the shape `decisionNonce.ts` established for randomness
and `recency.ts` established for the clock: `nowMs` arrives as a parameter and
the storage the rule needs arrives as an argument, so the rule stays testable
without waiting and without patching a global. It needs a DECISION FIRST, and
that decision is where a dismissal PERSISTS — `localStorage` in the browser, a
server-side last-seen stamp, or per-tab session state — because that choice
decides whether "no re-show" survives a new tab, a new browser and a second
operator, and the feature file's acceptance clause "Dismissal persists; new
activity re-arms" cannot be graded until it is settled.

Before authoring that round, re-read `.agent/STOP` from disk (Phase 1 rule 1,
ahead of rule 2) — it did not exist at any reading this round.

Branch `feature/f040-completion-digest` pushed after C6. No pull request opened,
nothing merged, nothing force-pushed.
