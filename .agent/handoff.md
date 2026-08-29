# Handback — F040 · SESSION 2 · round 7 — T002 PART 2: WHEN THE HERO CARD APPEARS

> Written by the WORKER in C6, the last commit of the bundle. Every exit code
> below is REAL, taken from `subprocess.run(...).returncode` inside a script
> under the gitignored `.remedy-wt/`; not one was read through a pipe or from
> `$?`.

## Session

SESSION 2 of feature F040 · round 7 · rounds so far 7.

The soft limit (25 rounds / 7 sessions, amend0827 rule 6) is not approached, so
no scope report is owed. `.agent/STOP` did not exist at any reading this round —
checked before the first commit and again before this one.

## Range

Review of `3d609e02`..`HEAD` on branch `feature/f040-completion-digest`. The
base is round 6's handback commit and was the tip of the branch when this round
opened. No new branch was cut, no pull request opened, nothing merged, nothing
force-pushed.

**T002's TRIGGER IS BUILT AND ITS RULE HALF IS COMPLETE. THE COPY HALF IS NOT
DISCHARGED.** The acceptance clauses this round answers are
`docs/roadmap/features/T5_F040.md`'s "Dismissal persists; new activity re-arms"
and the trigger rules at :68-71 — a terminal event while the UI is open shows the
hero, dismissible and remembered per job; a first open with activity since
last-seen shows the hero. Those are now ONE comparison each in
`apps/ui/src/api/digestVisibility.ts`. The Acceptance's OTHER clause — "Absence
detection never claims more than last-seen truth (copy audit: 'since you were
last here' not 'while you slept')" — is **NOT** met by this round, deliberately
and by the block's own instruction: the sentences are the card's, the card is the
next round, and this module is guarded to contain no user-facing sentence at all.
Do not read this handback as discharging the copy audit.

NO `.tsx` AND NO CSS LANDED. NO PYTHON PRODUCTION CODE CHANGED.
`apps/ui/src/api/jobDigest.ts` was not edited and is byte-identical to its base
blob (G5).

## Commits

### c88c2919 docs(f040): save the round 7 block

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f040-r7.md` | +389 −0 | C0a — the block, copied with `shutil.copyfile` from `.remedy-wt/f040-r7-block.md`, never retyped |

### 5cf664e5 docs(f040): mirror the round 7 block

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +293 −267 | C0b — the same bytes, the same `shutil.copyfile` call |

### 7076565e docs(f040): retarget the plan at the trigger rule

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +15 −17 | C1 — slice PLAN7 applied byte for byte; SESSION 2 / round 7, T001's three rows collapsed to one settled row, the trigger row settled to `this round`, the card row now `next` |

### c096a4a3 docs(f040): book the round 6 verdict and rule D8

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +4 −0 | C2 — slice RECORD7 appended: the R6 PASS gate line and DECISION F040 D8. Append-only; the base bytes are a prefix of the result |

### 81f769cd feat(f040): add the digest trigger rule as a pure total function

| Path | +/- | Reason |
|------|-----|--------|
| `apps/ui/src/api/digestVisibility.ts` | +185 −0 | C3 — the trigger: `DigestDismissal`, the `DigestVisibilityPort` type, the closed `DigestVisibilityReason` union, `DigestVisibility`, `DigestVisibilityInput` and the total rule `digestVisibility`, over a THREE-WAY partition of `RunState` |

### 65b14a79 test(f040): pin the digest trigger rule in vitest

| Path | +/- | Reason |
|------|-----|--------|
| `apps/ui/src/api/digestVisibility.test.ts` | +268 −0 | C4 — 30 vitest cases: the seven-state table, both boundaries (activity EQUAL to the dismissal, activity EQUAL to last-seen), a null `lastSeenMs`, a null digest, a future stamp, and the `reason` asserted alongside every boolean |

### 3ce80035 test(f040): guard the trigger rule purity, its port and the seven states

| Path | +/- | Reason |
|------|-----|--------|
| `tests/ui_contracts/test_job_digest_card_contract.py` | +265 −0 | C5 — one APPENDED class, 13 Python cases: the purity, the port-is-a-type count, the two audited phrases, the no-sentence reader, the closed reason union, and the seven states read out of `packages/core/models.py` |

### (this commit) docs(f040): write the round 7 handback

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | C6 — this file. A handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/g3-negative-control HEAD` | rc 0 — G3's on-disk negative control |
| `git worktree remove --force .remedy-wt/g3-negative-control` | rc 0 — removed by exact path; `git worktree list` no longer holds it |
| `git worktree add --detach .remedy-wt/g6-red-proof HEAD` | rc 0 — G6's four mutations of `digestVisibility.ts` |
| `git worktree remove --force .remedy-wt/g6-red-proof` | rc 0 — removed by exact path; `git worktree list` no longer holds it |
| `git push origin feature/f040-completion-digest` | after C6 — see the closing line |

No pull request created, none edited, none merged. No `gh` command run. No
force-push. The `remedy` console script was never invoked (block constraint 11)
and nothing this round needed it, so no `python3 -m apps.cli.main` substitute was
needed either.

## Verification

Eight gates, eight REAL exit codes. Every gate ran at a commit strictly earlier
than C6, which writes this file.

    G1 TRANSPORT, at C0b (5cf664e5)                        REAL EXIT 0
    G2 THE PLAN, at C1 (7076565e)                          REAL EXIT 0
    G3 THE RECORD APPEND, at C2 (c096a4a3)                 REAL EXIT 0
    G4 THE LEDGER, at C2 (c096a4a3)                        REAL EXIT 0
    G5 THE RULE'S SHAPE, at C3 (81f769cd)                  REAL EXIT 0
    G6 THE GUARD, ITS APPEND AND ITS RED PROOF, at C5 (3ce80035)  REAL EXIT 0
    G7 VITEST AND THE TYPECHECK, at C5 (3ce80035)          REAL EXIT 0 (both nodes)
    G8 THE SUITES AND THE TREE, at C5 (3ce80035)           REAL EXIT 0

### G1 TRANSPORT — REAL EXIT 0

One sha256 over three files with the byte length, all three EQUAL. The block
states no expected digest, so this is a measurement and not a match against a
number I was handed.

    12384650aeeec89da2c801535aaf7038df0670ead010e2dfb22baaaff7bf3e9a  29484 bytes  .remedy-wt/f040-r7-block.md
    12384650aeeec89da2c801535aaf7038df0670ead010e2dfb22baaaff7bf3e9a  29484 bytes  .agent/authored/f040-r7.md
    12384650aeeec89da2c801535aaf7038df0670ead010e2dfb22baaaff7bf3e9a  29484 bytes  .agent/last_block.md
    ALL THREE EQUAL: True
    committed .agent/authored/f040-r7.md: sha256 12384650…7bf3e9a 29484   (git show rc 0)
    committed .agent/last_block.md:       sha256 12384650…7bf3e9a 29484   (git show rc 0)
    G1 PASS: True

Both `.agent/` copies were read back OUT of git and both COMMITTED blobs hash to
the same digest at the same 29484 bytes.

### G2 THE PLAN — REAL EXIT 0

    PLAN7 slice    sha256 2006f529043694568589540e0d789392e5c95bf9b07517ed7587f9c8bfbdb409  1882 bytes
    .agent/plan.md sha256 2006f529043694568589540e0d789392e5c95bf9b07517ed7587f9c8bfbdb409  1882 bytes
    BYTE-EQUAL: True
    committed blob sha256 2006f529043694568589540e0d789392e5c95bf9b07517ed7587f9c8bfbdb409  1882 bytes   (git show rc 0)
    line count: 39 (< 50: True)
    holds '## Goal': True   holds '## Next Steps': True

### G3 THE RECORD APPEND — REAL EXIT 0

The pre-commit length was RE-MEASURED here rather than taken from the block; it
agrees with the 1687401 the reviewer read at `3d609e02`. Both the base and the
committed file are read from git BLOBS (`HEAD~1` and `HEAD`), so the arithmetic
is over stored bytes. N was COUNTED by the script — RECORD7 is TWO paragraphs,
the R6 gate line and DECISION F040 D8 — and never asserted.

    BASE      1687401 bytes  sha256 0af1aa9a30a15e637395007653fa5b9ec3edc134025d5b1324675bf2f69a9364
    RECORD7   7054 bytes  sha256 3b15a559be0f4fa3cf904329c04ad9964458355d77d4dcf86a119153def6cfba
    COMMITTED 1694456 bytes  sha256 3d8223c4a2a0b91e471f3fa17d73bcf7f6281546e2828c203eae4fc17d786364
    ARITHMETIC 1687401 + 1 + 7054 = 1694456  vs committed 1694456  match True
    N (paragraphs of RECORD7, counted by this script): 2
    (a) WHOLE RECONSTRUCTION: True
    (b) PARAGRAPH ORDER (last 2 units equal RECORD7's 2, in order): True
    BASE BYTES ARE A PREFIX OF THE COMMITTED FILE: True

    worktree add -> 0
      CONTROL (unflipped, read from the worktree): (a) WHOLE: True  (b) ORDER: True
      FLIPPED byte at offset 1689587 (b'n' -> b'\x00'), inside appended paragraph 1 (spans 1687402..1691772)
      flipped: (a) WHOLE: False  (b) ORDER: False  (both must be False)
    worktree remove -> 0
    git worktree list still holds it: False
    /home/decodeux/Repos/remedy  c096a4a3 [feature/f040-completion-digest]

The negative control was performed ON DISK inside the disposable worktree, the
unflipped control read FIRST; both readings rejected the flipped bytes and both
accepted the unflipped ones.

### G4 THE LEDGER — REAL EXIT 0

    REGISTERED '^- R-\d+ — ': before 315 distinct, after 315 distinct, ADDED [], REMOVED []
    RESOLVED   '^Done: R-\d+': before 54 distinct, after 54 distinct, ADDED [], REMOVED []
    DECISION F040 D\d+: before 7 distinct, after 8 distinct, ADDED ['D8'], REMOVED []
    '^Gate: F040 R6 — ' lines: 1 (must be exactly 1)
    OPEN COUNT: before 261, after 261, delta 0 (must be 0, and 261)
    patterns: registered (?m)^- (R-\d+) — ; resolved (?m)^Done: (R-\d+); decisions DECISION F040 (D\d+)

The patterns are recorded so the count is reproducible. This round registers NO
new finding and resolves none, as ordered, so the open count is UNCHANGED. OPEN
FINDINGS: **261**.

### G5 THE RULE'S SHAPE — REAL EXIT 0

The exported names are found by PARSING the declarations
(`(?m)^export\s+(function|const|let|interface|type|class|enum)\s+([A-Za-z_$][\w$]*)`)
rather than by eye. The strippers are the guard module's own, IMPORTED by this
gate rather than copied, so the gate and the committed test cannot drift apart.

    EXPORTED NAMES (6), parsed from the declarations:
      type      DigestDismissal
      interface DigestVisibilityPort
      type      DigestVisibilityReason
      interface DigestVisibility
      interface DigestVisibilityInput
      function  digestVisibility
    `DigestVisibilityPort` is DECLARED (as an interface): True
    required export 'DigestDismissal': True
    required export 'DigestVisibility': True
    required export 'DigestVisibilityPort': True
    required export 'digestVisibility': True
    PURITY over comment- and literal-stripped source:
      Date.now        occurrences 0   salted control sees it: True
      new Date        occurrences 0   salted control sees it: True
      localStorage    occurrences 0   salted control sees it: True
      sessionStorage  occurrences 0   salted control sees it: True
      fetch           occurrences 0   salted control sees it: True
      crypto          occurrences 0   salted control sees it: True
      XMLHttpRequest  occurrences 0   salted control sees it: True
    RunState VALUES parsed out of packages/core/models.py: ['pending', 'planned', 'running', 'paused', 'completed', 'failed', 'cancelled']
      pending    occurs in digestVisibility.ts (comment-stripped): True  (as a literal, 1x)
      planned    occurs in digestVisibility.ts (comment-stripped): True  (as a literal, 1x)
      running    occurs in digestVisibility.ts (comment-stripped): True  (as a literal, 1x)
      paused     occurs in digestVisibility.ts (comment-stripped): True  (as a literal, 1x)
      completed  occurs in digestVisibility.ts (comment-stripped): True  (as a literal, 1x)
      failed     occurs in digestVisibility.ts (comment-stripped): True  (as a literal, 1x)
      cancelled  occurs in digestVisibility.ts (comment-stripped): True  (as a literal, 1x)
    jobDigest.ts base blob 10400 bytes, HEAD blob 10400 bytes
    jobDigest.ts BYTE-IDENTICAL to its base blob at 3d609e02: True

THE SEVEN NAMES THIS GATE ACTUALLY FOUND are the seven printed above, and they
were read out of `packages/core/models.py` with `ast` rather than retyped — the
same reading the committed guard performs at test time, which is what makes the
three-way partition a pinned property rather than a paragraph. Each was found as
a real code LITERAL in comment-stripped source, so the module's prose cannot
stand in for its code.

### G6 THE GUARD, ITS APPEND AND ITS RED PROOF — REAL EXIT 0

Control FIRST in both checkouts. `__pycache__` was purged before every run and
every run used `python3 -B`. All four mutations edit `digestVisibility.ts` inside
the disposable worktree and each was reverted before the next; each mutation's
anchor was asserted UNIQUE in the source before it was applied.

    STEP 1 — the append and the base's own tests
      base blob 12094 bytes sha256 ea1d03bc25126934a8afb8ee707ac65fa3affe625c8c9e2f3859bd4389580fd7
      HEAD blob 25035 bytes sha256 fc4592717489d4b23f014d15d987490f808877a06cefebe589b98af02cb6bbc1
      BASE BYTES ARE A PREFIX OF THE COMMITTED GUARD: True
      the base file's four classes, re-run at HEAD by node id: REAL EXIT CODE 0  ['16 passed in 0.23s']

    STEP 2 — the guard at C5, in the primary checkout
      [primary] REAL EXIT CODE: 0   ['29 passed in 0.24s']
      rise from 16: 29 - 16 = 13, the number of tests C5 adds

    STEP 3 — worktree add .remedy-wt/g6-red-proof -> 0
      original apps/ui/src/api/digestVisibility.ts  9820 bytes  sha256 9a7be542b69f7a95f24f6a3a4ba69019373f8304774496fcab1ab42330a914a9

    STEP 4 — the UNMUTATED CONTROL, inside the worktree, FIRST
      [control] REAL EXIT CODE: 0   ['29 passed in 0.23s']

    STEP 5 — MUTATION M1 a consumed Date.now() inside the rule's body
      mutated file 9873 bytes  sha256 70b07c22c4038e25a77e5d04436f6117590d6fa69b5c7298dfa4bd26618882a5
      [M1] REAL EXIT CODE: 1   ['1 failed, 28 passed in 0.25s']
          DEAD: tests/ui_contracts/test_job_digest_card_contract.py::TestTheTriggerRuleIsPureAndPortless::test_the_rule_names_none_of_the_forbidden_capabilities
      REVERTED by exact path .remedy-wt/g6-red-proof/apps/ui/src/api/digestVisibility.ts; bytes equal the original: True

    STEP 5 — MUTATION M2 a real implementation bound to the port
      mutated file 9929 bytes  sha256 fb34fedf8bafe017fcb95bd8a791287f1b52e2c000ac407123357d646998e379
      [M2] REAL EXIT CODE: 1   ['2 failed, 27 passed in 0.25s']
          DEAD: tests/ui_contracts/test_job_digest_card_contract.py::TestTheTriggerRuleIsPureAndPortless::test_the_port_is_declared_and_never_implemented
          DEAD: tests/ui_contracts/test_job_digest_card_contract.py::TestTheTriggerRuleIsPureAndPortless::test_the_port_scan_can_see_an_implementation
      REVERTED by exact path .remedy-wt/g6-red-proof/apps/ui/src/api/digestVisibility.ts; bytes equal the original: True

    STEP 5 — MUTATION M3 the audited phrase placed in the module
      mutated file 9869 bytes  sha256 daa013e6cf441d3d476a4e9aa1d93180ed0bdd3159f00d4bf2484c75aca561ef
      [M3] REAL EXIT CODE: 1   ['2 failed, 27 passed in 0.25s']
          DEAD: tests/ui_contracts/test_job_digest_card_contract.py::TestTheTriggerRuleIsPureAndPortless::test_the_rule_carries_neither_audited_phrase
          DEAD: tests/ui_contracts/test_job_digest_card_contract.py::TestTheTriggerRuleIsPureAndPortless::test_the_rule_carries_no_user_facing_sentence_at_all
      REVERTED by exact path .remedy-wt/g6-red-proof/apps/ui/src/api/digestVisibility.ts; bytes equal the original: True

    STEP 5 — MUTATION M4 the string `pending` deleted from the state handling
      mutated file 9809 bytes  sha256 656ec3e016fbcb9d5790ed81eab24c18d467a90756839ae3608ac676e320c0f2
      [M4] REAL EXIT CODE: 1   ['1 failed, 28 passed in 0.25s']
          DEAD: tests/ui_contracts/test_job_digest_card_contract.py::TestTheTriggerRuleIsPureAndPortless::test_all_seven_run_states_are_accounted_for_in_the_rule
      REVERTED by exact path .remedy-wt/g6-red-proof/apps/ui/src/api/digestVisibility.ts; bytes equal the original: True

    STEP 6 — RESTORED, re-run
      [restored] REAL EXIT CODE: 0   ['29 passed in 0.23s']
      restored bytes equal the original: True  sha256 9a7be542b69f7a95f24f6a3a4ba69019373f8304774496fcab1ab42330a914a9

    STEP 7 — removing the worktree BY EXACT PATH
      worktree remove -> 0
      git worktree list still holds g6-red-proof: False
      /home/decodeux/Repos/remedy  3ce80035 [feature/f040-completion-digest]

WHAT EACH MUTATION PROVES, and each is a REAL construct rather than a bare token
in dead code. M1's `Date.now()` is CONSUMED — `const seenAtMs = Date.now();` then
`seenAtMs > 0 ? input.latestActivityMs : null` — so a guard that merely greps a
word out of an unreachable line could not have killed it; it killed the purity
assertion alone, which is the narrow answer a purity guard should give. M2 binds
a working in-memory implementation to the port and killed BOTH port assertions:
the one-occurrence count AND its own discriminator, which is the correct pair —
the discriminator salts the file with a second occurrence and the mutated file
already has one, so it reads three and refuses. M2 was written WITHOUT reaching
for storage on purpose, so the kill is attributable to the port rule and not to
the purity rule standing in for it. M3 killed the named-phrase assertion AND the
no-sentence reader, which is the right pair for a copy leak. M4 killed the
seven-state assertion alone, which is exactly the assertion G5 orders and the one
that makes the three-way partition a pinned property.

NOTE FOR HONESTY, ORDERED BY THE BLOCK: **the vitest cases that pin the PARTITION
ITSELF got no colour this round, and none was attempted.** Running the vitest
node with its cwd in a worktree fails at startup for want of `node_modules` — red
for every possible mutation, the vacuous probe R-0703 records — and running it in
the primary checkout would test the primary's unmutated files, so neither
spelling proves anything. The partition is pinned STATICALLY by G5's seven-state
reading, which IS red-proved above (M4), and dynamically only by the suite being
green. The vitest suite is NOT red-proved and must not be described as such.

### G7 VITEST AND THE TYPECHECK — REAL EXIT 0 for both nodes

Reached through the pytest nodes, never through a direct `npx` call, which is
refused to this session class.

    $ python3 -m pytest "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" -q -rs
    4 passed in 1.22s
    REAL EXIT CODE: 0        NODE STATUS: PASSED — not skipped, no skip report emitted under -rs

    $ python3 -m pytest tests/ui_server/test_dashboard_contract.py -k typescript -q -rs
    1 passed, 73 deselected in 2.08s
    REAL EXIT CODE: 0        NODE STATUS: PASSED — not skipped, no skip report emitted under -rs

Both match the reviewer's base measurement of 4 passed and 1 passed, neither
skipped. `test_typescript_compiles` SKIPS when `apps/ui/node_modules/.bin/tsc` is
absent and otherwise runs that local binary with `--noEmit`; it did not take its
skip branch, so `tsc --noEmit` really compiled the two new `.ts` files under
`strict`, `noUnusedLocals` and `noUnusedParameters`. The COVERAGE claim for the
vitest node was confirmed statically rather than taken:
`apps/ui/vitest.config.ts` sets `include: ["src/**/*.test.ts"]`, a probe listed
the 35 files that pattern collects and `src/api/digestVisibility.test.ts` is
among them, and the node asserts the whole run's returncode is 0 — so a failing
case in the new file reddens that node by construction.

NO TYPESCRIPT COLOUR WAS RUN AND NONE WAS ORDERED (block constraint 15, DECISION
F040 D7). A permission boundary was reported, never routed around.

### G8 THE SUITES AND THE TREE — REAL EXIT 0

Five suites, run SERIALLY, each with its own REAL exit code:

    $ python3 -m pytest tests/ui_contracts/ -q
       728 passed, 4 skipped in 6.38s
       REAL EXIT CODE: 0   base 715 -> now 728   difference +13
    $ python3 -m pytest tests/orchestration/test_job_digest.py -q
       46 passed in 0.43s
       REAL EXIT CODE: 0   base 46 -> now 46   difference +0
    $ python3 -m pytest tests/ui_server/ -q
       515 passed in 34.94s
       REAL EXIT CODE: 0   base 515 -> now 515   difference +0
    $ python3 -m pytest tests/docs/ -q
       295 passed in 0.60s
       REAL EXIT CODE: 0   base 295 -> now 295   difference +0
    $ python3 -m pytest tests/cli/test_golden_path.py -q
       42 passed in 30.63s
       REAL EXIT CODE: 0   base 42 -> now 42   difference +0

    --- the tree ---
    $ git status --porcelain  -> exit 0, 0 lines, EMPTY: True
    $ git ls-files --others --exclude-standard -> count 0

    --- per-commit insertions, C0a through C5 ---
       c88c2919  +389   -0     under 500   docs(f040): save the round 7 block
       5cf664e5  +293   -267   under 500   docs(f040): mirror the round 7 block
       7076565e  +15    -17    under 500   docs(f040): retarget the plan at the trigger rule
       c096a4a3  +4     -0     under 500   docs(f040): book the round 6 verdict and rule D8
       81f769cd  +185   -0     under 500   feat(f040): add the digest trigger rule as a pure total function
       65b14a79  +268   -0     under 500   test(f040): pin the digest trigger rule in vitest
       3ce80035  +265   -0     under 500   test(f040): guard the trigger rule purity, its port and the seven states

THE RISE THE GATE ASKED FOR: `tests/ui_contracts/` was **715 passed with 4
skipped** at the base and is **728 passed with 4 skipped** at C5 — a difference of
**+13**, which is exactly the number of tests C5 adds (the appended class
collects 13 and all 13 pass; the base file's own 16 still collect and still pass,
re-run by node id in G6 step 1). The four skips are pre-existing and unmoved. The
other four suites are unchanged, which is what a round that touches no Python
production code should produce.

Also run, though no gate ordered it:
`python3 -m ruff check tests/ui_contracts/test_job_digest_card_contract.py` —
REAL EXIT 0, "All checks passed!".

## Authored-text proofs

Both reviewer-authored units were extracted MECHANICALLY from
`.remedy-wt/f040-r7-block.md` by `.remedy-wt/r7_extract.py`, which verifies the
block's own digest first, then slices between the `<<<BEGIN NAME` / `<<<END NAME`
marker lines (markers excluded, the newline ending the last content line
included) and writes each to `.remedy-wt/r7units/<NAME>.txt`. Nothing was
retyped; every application was a `shutil.copyfile` or a binary append of those
bytes.

| Unit | Bytes | sha256 | Applied to | Proof |
|---|---|---|---|---|
| the block itself | 29484 | `12384650…7bf3e9a` | `.agent/authored/f040-r7.md`, `.agent/last_block.md` | G1 — three-way disk-to-disk equality, plus both committed blobs re-hashed from `git show` |
| PLAN7 | 1882 | `2006f529…bfbdb409` | `.agent/plan.md` | G2 — byte-equality against the file and against the committed blob |
| RECORD7 | 7054 | `3b15a559…def6cfba` | `.agent/live_review.md` | G3 — whole reconstruction + paragraph order + prefix, with an on-disk negative control |

The three SPECs (C3's module, C4's vitest suite, C5's appended guard class) are
DESCRIBED production code, not slices, so they carry no byte-equality proof; they
are graded by G5, G6, G7 and G8 instead.

## Deviations & assumptions

1. **THE ORDERED COMMIT SEQUENCE WAS FOLLOWED EXACTLY.** Seven commits, in the
   block's order, C0a → C0b → C1 → C2 → C3 → C4 → C5, and this handback as C6.
   No extra commit, none dropped, none reordered, no amend. The change set is
   exactly the eight paths the block names and nothing else.
2. **THE NEW `Path` SITS AT THE TOP OF THE APPENDED REGION, NOT BESIDE THE
   EXISTING ONES.** The C5 SPEC says "Add a module-level `Path` for the new file
   beside the existing ones", and constraint 14 says the committed file's first
   bytes are EXACTLY the base file's. Those two cannot both be met literally:
   `DIGEST`, `METRIC` and `BAR` are at lines 32-34 and inserting a fourth there
   would move every byte after it. Constraint 14 is the hard one and the block
   says the block wins on conflict, so `VISIBILITY = API_DIR / "digestVisibility.ts"`
   is declared at module scope in the appended region — "beside" read as "in the
   same module scope and the same style", not as "physically adjacent". A comment
   above it records why. The file was never read-and-rewritten: it was opened in
   binary APPEND mode, so the base bytes are physically untouched.
3. **`import ast` IS A FUNCTION-LOCAL IMPORT IN THE APPENDED GUARD.** For the
   same reason: the base file's import block is above the appended region and may
   not be edited. `run_state_values()` imports `ast` in its body and says so in
   its docstring. `ruff check` passes over the whole file.
4. **THE RULE TAKES `nowMs` AND NO BRANCH READS IT.** The C3 SPEC anticipates
   this and asks it be declared here rather than papered over with an invented
   use: `nowMs` is a field of `DigestVisibilityInput` and `digestVisibility` never
   consumes it. Every comparison in the rule is between two stamps the same host
   took — activity against the dismissal, activity against last-seen — which is
   precisely why a stamp in the FUTURE relative to `nowMs` is still activity and
   still shows the card. That is the posture `recency.ts` takes at its own skew
   comment, and the module's header says so where a reader will look. The
   parameter is kept because it is the card's one place to bind a clock and
   because a later branch (an expiry, say) would need it; `noUnusedParameters`
   does not fire because the object parameter itself IS used. A vitest case
   (`answers the same for any nowMs, because no branch reads it`) pins the
   invariance rather than leaving it as a claim.
5. **NOT-YET-STARTED IS A VETO, NOT MERELY A FAILED SETTLED TEST.** The C3 SPEC
   distinguishes its three groups with deliberately different force: `running`
   "does not show on settled grounds" (leaving the absence route open) while
   `pending` and `planned` "must NOT show" flatly, and the C4 SPEC repeats
   "assert explicitly that `pending` and `planned` do NOT show". I read that
   asymmetry as intended and implemented it: a not-yet-started state returns
   `{show: false}` BEFORE the absence rule is reached, so a pending job does not
   show even when there is activity after last-seen. Two vitest cases pin exactly
   that ("never shows a pending job, not even with activity since last-seen", and
   the same for `planned`). Declared because it is the one place the rule is
   stronger than a literal reading of the absence bullet alone would make it, and
   it is the difference the two-way/three-way warning is about.
6. **THE REASON SET HAS SIX MEMBERS, TWO MORE THAN THE FOUR THE SPEC NAMES.** The
   SPEC says "Cover at least" the four; the union also carries `no-digest` (a
   `null` digest is a distinct answer, not "nothing new") and `not-yet-started`
   (deviation 5's veto, which the card may want to distinguish from a quiet run).
   Both are additive and both are asserted in the tests.
7. **TWO EXPORTS BEYOND THE FOUR THE C3 SPEC LISTS.**
   `DigestVisibilityReason` is exported because the C5 SPEC assertion is written
   over "the exported reason type", which requires a named exported type;
   `DigestVisibilityInput` names the single named-argument object rather than
   leaving it an inline literal, which is what AGENTS.md's discoverability rules
   and DECISION F040 D2's own reasoning ask for. G5 reports all six exports.
   Neither adds behaviour.
8. **`DigestDismissal` IS A TYPE ALIAS FOR `number | null`, NOT AN INTERFACE.**
   The SPEC describes it as "the instant a dismissal was made, or `null` for
   never dismissed" and asks that it be a named type "even though it is small".
   An alias is the smallest thing that satisfies that; wrapping the instant in an
   object would change every call site for no gain.
9. **THE `no-user-facing-sentence` GUARD IS A HEURISTIC AND ITS REACH IS WRITTEN
   INTO ITS OWN DOCSTRING.** It reads every quoted literal of the
   comment-stripped source and asserts none contains a space. It cannot see a
   sentence assembled from spaceless fragments, nor a template literal (which
   `executable_of_text` deliberately leaves intact). Stated as a limit rather
   than hidden, and paired with a salted control that proves the reader does see
   a plain sentence when one is present.
10. **THE PORT COUNT CANNOT SEE A STRUCTURAL TWIN.** TypeScript is structurally
    typed, so an object literal carrying `readDismissal` and `writeDismissal`
    would satisfy the port without naming it, and the one-occurrence count would
    not notice. The docstring says so, and closes the hole from the other side:
    such a twin could not reach real storage without naming `localStorage` or
    `sessionStorage`, both pinned at zero by the purity assertion, so it would be
    inert. Declared because an unstated blind spot is the finding, not the blind
    spot itself.
11. **C0a AND C0b PRECEDE C1, SO TWO COMMITS LAND WHILE `.agent/plan.md` STILL
    NAMES ROUND 6.** This is the block's own bundle order together with its
    constraint 3 ("C1 is the FIRST substantive commit"), not a departure from it,
    and it is the established shape of every round of this feature. Noted so a
    reader auditing the AGENTS.md commit gate against the first two commits does
    not have to reconstruct why.
12. **`.agent/context.md` AND `.agent/decisions.md` WERE NOT TOUCHED.** The
    commit gate's step 7 was considered at every commit. DECISION F040 D8 is a
    durable decision, and the block routes it into `.agent/live_review.md` via
    RECORD7 — where every other F040 decision from D1 to D7 already lives — while
    the change set names exactly eight paths and forbids widening. Recorded so
    the absence is visibly a decision rather than an omission.
13. **NO TYPESCRIPT COLOUR WAS RUN** — see G6's closing note and G7 for the
    measured reason. None was ordered. The vitest suite's 30 cases are green but
    NOT red-proved, and this handback does not claim otherwise.
14. **THE COPY AUDIT IS NOT DISCHARGED.** Stated again here because it is the
    easiest thing for a reader to assume from a green round: this round meets the
    RULE half of the Acceptance clauses named at the top of the block and NOT the
    copy half. "since you were last here" is not written anywhere yet, and the
    guard actively forbids it in this module.
15. No commit subject carries a leading-slash token, an absolute path, a
    secret-like string or a `Co-Authored-By` trailer (block constraint 12); every
    commit's insertion count is under 500 (G8), so no oversize-commit declaration
    is owed.
16. Both disposable worktrees were removed BY EXACT PATH
    (`.remedy-wt/g3-negative-control`, `.remedy-wt/g6-red-proof`), never by glob,
    and `git worktree list` was re-read after each removal. All scratch scripts
    live under the gitignored `.remedy-wt/` and none is committed —
    `git ls-files --others --exclude-standard` counts 0.

## Item status

| Item | Status | Reason |
|--------|----------|------------------------------|
| C0a save the block to `.agent/authored/f040-r7.md` | done | `shutil.copyfile`; c88c2919 |
| C0b mirror into `.agent/last_block.md` | done | `shutil.copyfile`; 5cf664e5 |
| C1 rewrite `.agent/plan.md` from PLAN7 | done | byte-equal; 7076565e |
| C2 append RECORD7 to `.agent/live_review.md` | done | append-only; c096a4a3 |
| C3 add `apps/ui/src/api/digestVisibility.ts` | done | per SPEC; 81f769cd |
| C4 create `apps/ui/src/api/digestVisibility.test.ts` | done | 30 vitest cases; 65b14a79 |
| C5 append a class to `tests/ui_contracts/test_job_digest_card_contract.py` | done | 13 cases, base bytes a prefix; 3ce80035 |
| C6 rewrite `.agent/handoff.md` | done | this commit |
| G1 TRANSPORT | done | REAL EXIT 0 |
| G2 THE PLAN | done | REAL EXIT 0 |
| G3 THE RECORD APPEND | done | REAL EXIT 0; N counted as 2 |
| G4 THE LEDGER | done | REAL EXIT 0; open count unchanged at 261 |
| G5 THE RULE'S SHAPE | done | REAL EXIT 0; six exports, seven zeros with controls, seven states |
| G6 THE GUARD, ITS APPEND AND ITS RED PROOF | done | REAL EXIT 0; four mutations, all red at exit 1 |
| G7 VITEST AND THE TYPECHECK | done | REAL EXIT 0 and 0; both nodes PASSED, neither skipped |
| G8 THE SUITES AND THE TREE | done | REAL EXIT 0 ×5; clean tree; ui_contracts 715 → 728 |

## Findings state

| Id | State |
|---|---|
| R-0570 | OPEN — routed to the paydown branch |
| R-0752 | OPEN — routed to the paydown branch |
| R-0753 | OPEN — this feature's documented risk: the persisted actuals record has no money field, so the digest's cost basis can only answer `absent` in production |

This round registered NO new finding and resolved none, as ordered. Open
findings after C2: **261**, unchanged.

## Next

**T002 PART 3 — the hero card itself.** The `.tsx` that binds the clock and the
storage port at the edge (the shape `AgentNowCard.tsx` establishes for the clock
and DECISION F040 D8 rules for the port), the binding CSS from
`docs/roadmap/features/T5_F040.md`, **the copy audit that Acceptance names —
"since you were last here", never "while you slept"** — and the CSS conformance
guard. That round is where the copy half of the Acceptance is discharged; it is
not discharged now.

Before authoring it, re-read `.agent/STOP` from disk (Phase 1 rule 1, ahead of
rule 2) — it did not exist at any reading this round.

Branch `feature/f040-completion-digest` pushed after C6. No pull request opened,
nothing merged, nothing force-pushed.
