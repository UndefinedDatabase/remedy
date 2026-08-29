# Handback — F040 · SESSION 2 · round 9 — T002 PART 4: REPORT MARKUP INTO CARD COPY

> Written by the WORKER in C6, the last commit of the bundle. Every exit code
> below is REAL, taken from `subprocess.run(...).returncode` inside a script
> under the gitignored `.remedy-wt/`; not one was read through a pipe or from
> `$?`. The runner is `.remedy-wt/run.py`, which inherits the child's streams and
> prints the `CompletedProcess.returncode` it gets back.

## Session

SESSION 2 of feature F040 · round 9 · rounds so far 9.

The soft limit (25 rounds / 7 sessions, amend0827 rule 6) is not approached, so
no scope report is owed. `.agent/STOP` did not exist at any reading this round —
checked by listing `.agent/` before the first commit and again before this one.

## Range

Review of `b2cef8cb`..`HEAD` on branch `feature/f040-completion-digest`. The
base is round 8's handback commit and was the tip of the branch when this round
opened. No new branch was cut, no pull request opened, nothing merged, nothing
force-pushed, and no commit touched `main`.

## What this round did and did NOT do

DID: ruled the copy collision as DECISION F040 D10 and built the two pure rules
that resolve it, at `apps/ui/src/api/digestCardCopy.ts` —
`digestStateLabel` for the digest's own `RunState` vocabulary, `digestCtaText`
for a `primary_action.label` that `run_report.py` composed for a Markdown
artifact, and `DIGEST_CTA_RULE_IDS` as the closed rule set. Graded the sentences
in `apps/ui/src/api/digestCardCopy.test.ts` and pinned the module's SHAPE in
`tests/ui_contracts/test_digest_card_copy.py`, red-proved with four mutations,
each shown to reach a declaration before its colour was read. Booked the round 8
verdict and D10 into the record.

DID NOT: no card, no mount, no markup. No `.tsx` entered the change set, nothing
under `apps/ui/src/components/` was touched, and `run_report.py` was read but not
edited — the server's label is RIGHT for the report and for the CLI, and D10
turns that down as a repair route explicitly. `humanCopy.ts` was imported and not
changed; `jobDigest.ts`, `digestVisibility.ts` and
`DigestHeroCard.module.css` were not touched at all.

EVERY DECIDABLE RULE OF THE HERO CARD IS NOW BUILT AND PINNED. The envelope
(round 6), the trigger (round 7), the stylesheet (round 8) and the copy (this
round) are four separate pure modules with four separate guards. What is left for
the card round is wiring and nothing else, which is why the plan now says so.

## Commits

### 37740fb8 docs(f040): save the round 9 block verbatim
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f040-r9.md` | +327/-0 | C0a — the block copied verbatim with `shutil.copyfile`, before any slice was applied |

### 77d8a502 chore(f040): mirror the round 9 block into last block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +232/-219 | C0b — the same bytes in the location the resume protocol reads, again by `shutil.copyfile` |

### 9017f391 docs(f040): retarget the plan at the card copy rules
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +15/-15 | C1 — PLAN9 applied byte for byte; the copy collision moves from an open risk to a ruled decision |

### 129c86d7 docs(f040): book the round 8 verdict and decision D10
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4/-0 | C2 — RECORD9 appended: the R8 PASS and DECISION F040 D10. No finding registered, by design |

### 53d2a91c feat(f040): add the hero card copy rules
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/digestCardCopy.ts` | +155/-0 | C3 — the module: `digestStateLabel`, `digestCtaText`, `DIGEST_CTA_RULE_IDS` |

### 73182b9f test(f040): grade the hero card copy rules
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/digestCardCopy.test.ts` | +233/-0 | C4 — the vitest grade over every label shape the five rules emit, both forms of the two that have two |

### 6ab1377f test(f040): pin the card copy module shape
| Path | +/- | Reason |
|---|---|---|
| `tests/ui_contracts/test_digest_card_copy.py` | +454/-0 | C5 — the text guard: purity, the one-source rule for the §17 screen, the `stateLabel` trap, the five rule ids and the seven run states |

### C6 — this commit (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this file | C6 — a handoff cannot table the commit that writes it |

Every commit's insertion count is under 500: 327, 232, 15, 4, 155, 233, 454.

## External actions

| Command | Outcome |
|---|---|
| `git worktree add .remedy-wt/wt-g3 HEAD --detach` | created at `129c86d7` for G3's negative control |
| `git worktree remove .remedy-wt/wt-g3 --force` | removed, exit 0 |
| `git worktree add .remedy-wt/wt-g6 HEAD --detach` | created at `6ab1377f` for G6's four mutations |
| `git worktree remove .remedy-wt/wt-g6 --force` | removed, exit 0 |
| `git worktree list` | one line only, the primary checkout — neither worktree remains |
| `git push -u origin feature/f040-completion-digest` | run after C6 |

No pull request created, edited or merged. No `gh` command run. No force-push, no
history rewrite, no branch deleted. The `remedy` script was not invoked; nothing
this round needed it.

## Verification

All eight gates, each with its REAL exit code. Every gate ran at a commit
strictly earlier than C6.

### G1 TRANSPORT, at C0b (`77d8a502`) — REAL EXIT CODE 0

    + python3 -B .remedy-wt/g1.py
    fcfd0b131dec41599c12e9b67453c14a2170b0d541a3a79aec545ca1b40cc723   24159  .remedy-wt/f040-r9-block.md
    fcfd0b131dec41599c12e9b67453c14a2170b0d541a3a79aec545ca1b40cc723   24159  .agent/authored/f040-r9.md
    fcfd0b131dec41599c12e9b67453c14a2170b0d541a3a79aec545ca1b40cc723   24159  .agent/last_block.md
    ALL THREE EQUAL: True
    REAL EXIT CODE: 0

### G2 THE PLAN, at C1 (`9017f391`) — REAL EXIT CODE 0

    + python3 -B .remedy-wt/g2.py
    PLAN9 slice   sha256 257ed7df0420f852d9aa23d880db1c6c227f5db45fa0a448a6d770899de30adb 2034 bytes
    plan.md       sha256 257ed7df0420f852d9aa23d880db1c6c227f5db45fa0a448a6d770899de30adb 2034 bytes
    line count: 41
      byte-equal to PLAN9: True
      under 50 lines: True
      holds '## Goal': True
      holds '## Next Steps': True
    REAL EXIT CODE: 0

### G3 THE RECORD APPEND, at C2 (`129c86d7`) — REAL EXIT CODE 0

The pre-commit length was re-measured here, not taken from the block; it reads
1703971 at `b2cef8cb`, which is what the reviewer read.

    + python3 -B .remedy-wt/g3.py .remedy-wt/wt-g3
    pre-commit base length re-measured: 1703971 sha256 0a14f7fcd04cd5cce45f5edf663df3dc01086e29cc369f9920b2e3e1c3cda6f0
    RECORD9 length: 6230 sha256 24e9d7050f9ffd1f871b21ffdd4920637c4168c4f80d46b346dca8edddb9d791
    committed length: 1710202
    ARITHMETIC: 1703971 + 1 + 6230 = 1710202
    READING (a) WHOLE RECONSTRUCTION: True
    READING (b) PARAGRAPH ORDER: True | N counted: 2
    BASE BYTES ARE A PREFIX of the committed file: True
    worktree copy equals the primary checkout before the flip: True
    negative control: byte 1704012 b'C' -> b'c', inside paragraph 1 of 2; written in .remedy-wt/wt-g3
    the flip really changed the bytes on disk: True
    mutated bytes REJECTED by reading (a): True
    mutated bytes REJECTED by reading (b): True
    unflipped bytes ACCEPTED by reading (a): True
    unflipped bytes ACCEPTED by reading (b): True
    REAL EXIT CODE: 0

N was COUNTED by the script, not asserted: RECORD9 is two blank-line-separated
paragraphs, the R8 gate line and DECISION F040 D10. The negative control was
written to disk inside the disposable worktree only; the primary checkout was
read and never written, which is why `git status --porcelain` is still empty.

### G4 THE LEDGER, at C2 (`129c86d7`) — REAL EXIT CODE 0

    + python3 -B .remedy-wt/g4.py
    registered  ^- R-\d+ — : distinct 316 -> 316 | ADDED [] | REMOVED []
    resolved    ^Done: R-\d+: distinct 54 -> 54 | ADDED [] | REMOVED []
    decisions   DECISION F040 D\d+: distinct 9 -> 10 | ADDED ['D10'] | REMOVED []
    ^Gate: F040 R8 —  lines: 1
    OPEN COUNT: 262 -> 262 (UNCHANGED: True)
    REAL EXIT CODE: 0

The sets are computed by DIFFERENCE between the pre-commit base and the committed
file, never by reading the slice, so a claim about what moved is a measurement of
the record rather than a restatement of the block.

### G5 THE MODULE'S SHAPE, at C3 (`53d2a91c`) — REAL EXIT CODE 0

    + python3 -B .remedy-wt/g5.py
    EXPORTED NAMES, parsed: ['digestStateLabel', 'digestCtaText', 'DIGEST_CTA_RULE_IDS']
    imports scrubUiText from ../copy/humanCopy: True
    uses scrubUiText in executable source: True
    imports stateLabel (must be False): False
    RunState values parsed from packages/core/models.py (7): ['pending', 'planned', 'running', 'paused', 'completed', 'failed', 'cancelled']
    states missing from digestCardCopy.ts: []
    NextAction rule ids parsed from run_report.py (5): ['indeterminate', 'open-decision', 'stopped-by-operator', 'blocked-failed', 'all-green']
    DIGEST_CTA_RULE_IDS as written: ['open-decision', 'stopped-by-operator', 'blocked-failed', 'all-green', 'indeterminate']
    rule ids absent from the tuple: []
    tuple entries no rule emits: []
    FORBIDDEN-CAPABILITY SWEEP, each with a salted positive control:
      'fetch': occurrences 0 | scan sees a salted one: True
      'Date.now': occurrences 0 | scan sees a salted one: True
      'new Date': occurrences 0 | scan sees a salted one: True
      'localStorage': occurrences 0 | scan sees a salted one: True
      'sessionStorage': occurrences 0 | scan sees a salted one: True
      'crypto': occurrences 0 | scan sees a salted one: True
      'XMLHttpRequest': occurrences 0 | scan sees a salted one: True
    REAL EXIT CODE: 0

Both Python sets are read with `ast` rather than by grep: `NextAction(` is called
across two lines for `stopped-by-operator`, so a line-oriented reader would have
found four of five and called the set complete.

### G6 THE GUARD AND ITS RED PROOF, at C5 (`6ab1377f`) — REAL EXIT CODE 0 and 0

First the guard itself in the primary checkout:

    + python3 -m pytest tests/ui_contracts/test_digest_card_copy.py -q
    23 passed in 0.22s
    REAL EXIT CODE: 0

Then the red proof inside `.remedy-wt/wt-g6`, control FIRST, each mutation
reverted before the next, and each shown to REACH A DECLARATION before its colour
was read — the R8 lesson, where a mutation landed in a header comment and the
green that followed meant nothing. The proof of reach is that the change survives
comment stripping:

    + python3 -B .remedy-wt/g6.py .remedy-wt/wt-g6
    CONTROL, unmutated, inside the worktree:
      [control] REAL EXIT CODE: 0 | 23 passed in 0.22s

    MUTATION (a) a consumed Date.now()
      bytes on disk differ from the original: True
      the DECLARATION differs after comment stripping: True
      replaced: 'const key = String(state ?? "").trim().toLowerCase();'
      with:     'const key = Date.now() > 0 ? String(state ?? "").trim().toLowerCase() : "";'
      [mutated] REAL EXIT CODE: 1 | 1 failed, 22 passed in 0.22s
      TESTS THAT DIED (1):
        test_digest_card_copy.py::TestTheCopyRulesArePure::test_the_module_names_none_of_the_forbidden_capabilities

    MUTATION (b) scrubUiText import removed, call replaced by the raw string
      bytes on disk differ from the original: True
      the DECLARATION differs after comment stripping: True
      replaced: 'return scrubUiText(uncommanded, CTA_FALLBACK);'
      with:     'return uncommanded || CTA_FALLBACK;'
      [mutated] REAL EXIT CODE: 1 | 5 failed, 18 passed in 0.22s
      TESTS THAT DIED (5):
        test_digest_card_copy.py::TestTheStrippersReallyStrip::test_the_literal_blanker_empties_a_literal_the_module_really_carries
        test_digest_card_copy.py::TestTheStrippersReallyStrip::test_the_literal_reader_finds_the_literals_the_blanker_erases
        test_digest_card_copy.py::TestTheScreenHasOneHome::test_the_module_imports_the_screen_from_its_one_home
        test_digest_card_copy.py::TestTheWrongStateLabelIsNotReachedFor::test_the_checklist_state_label_is_not_imported
        test_digest_card_copy.py::TestTheWrongStateLabelIsNotReachedFor::test_the_import_reader_would_see_it_if_it_were_reached_for

    MUTATION (c) one rule id deleted from DIGEST_CTA_RULE_IDS
      bytes on disk differ from the original: True
      the DECLARATION differs after comment stripping: True
      replaced: '"stopped-by-operator",'
      with:     ''
      [mutated] REAL EXIT CODE: 1 | 2 failed, 21 passed in 0.22s
      TESTS THAT DIED (2):
        test_digest_card_copy.py::TestEveryRuleIdIsAccountedFor::test_every_reported_rule_id_appears_in_the_closed_tuple
        test_digest_card_copy.py::TestEveryRuleIdIsAccountedFor::test_the_rule_id_reader_would_notice_a_missing_entry

    MUTATION (d) one RunState value dropped from digestStateLabel
      bytes on disk differ from the original: True
      the DECLARATION differs after comment stripping: True
      replaced: '"paused": "Paused",'
      with:     ''
      [mutated] REAL EXIT CODE: 1 | 1 failed, 22 passed in 0.22s
      TESTS THAT DIED (1):
        test_digest_card_copy.py::TestEveryRunStateIsAccountedFor::test_all_seven_run_states_are_named_by_the_label_map

    RESTORED:
      byte-equal to the committed module: True
      [restored] REAL EXIT CODE: 0 | 23 passed in 0.22s
    REAL EXIT CODE: 0

Node ids are abbreviated above to the file's basename; the full ids all begin
`tests/ui_contracts/`. Mutation (c) kills the discriminator test as well as the
comparison it discriminates for, which is correct: that test asserts what a
dropped id looks like against the FULL tuple, so a tuple that is already short
has nothing left to drop.

    + git worktree remove .remedy-wt/wt-g6 --force
    + git worktree list
    /home/decodeux/Repos/remedy  6ab1377f [feature/f040-completion-digest]

### G7 VITEST AND THE TYPECHECK, at C5 (`6ab1377f`) — REAL EXIT CODES 0 and 0

    + python3 -m pytest "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" -q -rs
    4 passed in 1.24s
    REAL EXIT CODE: 0

    + python3 -m pytest tests/ui_server/test_dashboard_contract.py -k typescript -q -rs
    1 passed, 73 deselected in 2.04s
    REAL EXIT CODE: 0

BOTH PASSED, NEITHER SKIPPED, and both are unmoved at 4 and 1 — the numbers the
reviewer measured at the base. Per constraint 13 NO TYPESCRIPT COLOUR WAS RUN:
`npx vitest` is refused to this session class and `apps/ui/node_modules` is absent
from a worktree, so a mutation there would be red for every module and would
prove nothing. No vitest mutation was attempted.

### G8 THE SUITES AND THE TREE, at C5 (`6ab1377f`) — REAL EXIT CODES 0, 0, 0, 0, 0

    + python3 -m pytest tests/ui_contracts/ -q
    758 passed, 4 skipped in 5.80s
    REAL EXIT CODE: 0

    + python3 -m pytest tests/ui_server/ -q
    515 passed in 33.73s
    REAL EXIT CODE: 0

    + python3 -m pytest tests/docs/ -q
    295 passed in 0.44s
    REAL EXIT CODE: 0

    + python3 -m pytest tests/cli/test_golden_path.py -q
    42 passed in 20.65s
    REAL EXIT CODE: 0

`tests/ui_contracts/` rose 735 → 758, a DIFFERENCE OF 23, which is exactly the
number of tests C5 adds (`test_digest_card_copy.py` alone reports 23 passed). The
four pre-existing skips are unmoved. `tests/ui_server/`, `tests/docs/` and the
canary are unmoved at 515, 295 and 42.

    + python3 -B .remedy-wt/g8_tree.py
    git status --porcelain (exit 0): 'EMPTY'
    git ls-files --others --exclude-standard (exit 0): count 0

    PER-COMMIT INSERTIONS (the + column of git diff --numstat):
      C0a  37740fb8  +327   under 500: True
      C0b  77d8a502  +232   under 500: True
      C1   9017f391  +15    under 500: True
      C2   129c86d7  +4     under 500: True
      C3   53d2a91c  +155   under 500: True
      C4   73182b9f  +233   under 500: True
      C5   6ab1377f  +454   under 500: True
    REAL EXIT CODE: 0

## Authored-text proofs

| Unit | Applied to | Result |
|---|---|---|
| the whole block | `.agent/authored/f040-r9.md` | `shutil.copyfile`; sha256 equal to the source at 24159 bytes (G1) |
| the whole block | `.agent/last_block.md` | `shutil.copyfile`; same sha256, same 24159 bytes (G1) |
| PLAN9 | `.agent/plan.md` | extracted mechanically by `.remedy-wt/extract_r9.py`, 2034 bytes, sha256 `257ed7df…`; disk-to-disk equal (G2) |
| RECORD9 | `.agent/live_review.md` | extracted mechanically, 6230 bytes, sha256 `24e9d705…`; reconstructs the committed tail byte for byte (G3) |

Both slices were cut by script between their `<<<BEGIN`/`<<<END` marker lines,
with the marker lines excluded and the newline ending each last content line
included. Neither was retyped.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block to `.agent/authored/f040-r9.md` | done | |
| C0b mirror the same bytes into `.agent/last_block.md` | done | |
| C1 rewrite `.agent/plan.md` from PLAN9 | done | |
| C2 append RECORD9 to `.agent/live_review.md` | done | |
| C3 add `apps/ui/src/api/digestCardCopy.ts` | done | |
| C4 create `apps/ui/src/api/digestCardCopy.test.ts` | done | |
| C5 create `tests/ui_contracts/test_digest_card_copy.py` | done | |
| C6 rewrite `.agent/handoff.md` | done | this file |
| G1 transport | done | REAL exit 0 |
| G2 the plan | done | REAL exit 0 |
| G3 the record append | done | REAL exit 0 |
| G4 the ledger | done | REAL exit 0 |
| G5 the module's shape | done | REAL exit 0 |
| G6 the guard and its red proof | done | REAL exit 0 (guard) and 0 (driver); four mutations each red |
| G7 vitest and the typecheck | done | REAL exit 0 and 0, both PASSED not skipped |
| G8 the suites and the tree | done | REAL exit 0 ×4 plus the tree script at 0 |

## Decisions taken inside the module, which the block delegated

DECIDED — THE EMPTY CTA CASE. The block ordered the empty case decided and
documented, and required `scrubUiText`'s OWN fallback parameter rather than a
second mechanism. `digestCtaText` passes `CTA_FALLBACK = "No recommendation
recorded"`. It is a MISSING-VALUE MARKER and deliberately not a call to action:
it names no target, asks for nothing and adds no instruction, because inventing
one is exactly what constraint 11 and DECISION F040 D5 forbid. The wording is the
repository's own missing-value voice — `NOT_RECORDED = "not recorded"` in
`run_report.py`. Passing it through `scrubUiText`'s fallback gives the module ONE
empty-case path covering all three of that function's refusals (empty string,
forbidden word, whole-value identifier) rather than a hand-rolled check beside a
library one. This is stated here because it is a wording choice a reviewer may
want to overrule, and it is one string in one constant to change.

DECIDED — THE UNREADABLE STATE. `digestStateLabel` answers
`UNREADABLE_STATE_LABEL = "State not recorded"` for anything outside the seven
`RunState` values, rather than passing the string through. §17 forbids showing a
raw value, and a state string is a value the server chose; the same "not
recorded" voice is used, for the same reason.

DECIDED — THE TRAILING-COMMAND REGEX MAKES THE COLON OPTIONAL.
`/\s*:?\s*`[^`]*`\s*$/` drops a trailing backticked run whether or not a `: `
introduces it. The block ordered "the `: ` that introduces it"; the optional
colon is a superset that costs nothing on the five shipped shapes and closes the
case where a label ends in a bare backticked command, which would otherwise leave
a backtick on screen. `digestCardCopy.test.ts` grades that case explicitly.

## Deviations & assumptions

1. NO DEPARTURE FROM THE ORDERED COMMIT SEQUENCE. The bundle ran C0a, C0b, C1,
   C2, C3, C4, C5, C6 in exactly that order — seven commits before this one, no
   extra commit, none dropped, none reordered, and C1 is the first substantive
   commit as constraint 3 requires.
2. NO SLICE LOOKED WRONG. PLAN9 and RECORD9 were applied byte for byte and
   neither raised a question, so constraint 1's declare-it clause is not
   exercised.
3. AN EXTRA SELF-REVIEW STEP THE BLOCK DID NOT ORDER, DECLARED BECAUSE IT RAN.
   Before committing C3 I executed the two copy rules once under `node` from
   `.remedy-wt/sanity_cta.mjs`, a scratch file that mechanically strips the type
   annotations off `humanCopy.ts` and `digestCardCopy.ts` and calls the shipped
   functions over the label shapes `run_report.py` emits. It is NOT a gate, is
   NOT counted as TypeScript colour, and nothing in the verification section
   rests on it; it is AGENTS.md's self-review loop applied to a regex, and it did
   catch that the rules behave as their comments claim before the commit landed.
   It lives under the gitignored `.remedy-wt/` and is not in the change set. Also
   removed a dead capture group from `MARKDOWN_LINK` during that review, before
   the commit.
4. CONSTRAINT 13 HONOURED: NO TYPESCRIPT MUTATION WAS ATTEMPTED and no vitest
   colour is claimed. `apps/ui/src/api/digestCardCopy.test.ts` has never been
   executed by a test runner in this round — the two pytest nodes of G7 report
   only that the vitest FOUNDATION and the typecheck node are in place, which is
   what the block ordered and all it ordered.
5. THE `+232/-219` READING FOR C0b IS FROM `git diff --numstat`, the `+` column
   AGENTS.md's counting rule names. `git commit` printed a different figure for
   the same commit, a rewrite-detection difference; the same divergence was
   declared in round 8 and the reviewer endorsed tabling the `--numstat` reading.
   Both are far under the cap either way.
6. THE CHANGE SET IS EXACTLY THE EIGHT PATHS THE BLOCK NAMES and nothing else.
   `git status --porcelain` is empty and `git ls-files --others
   --exclude-standard` counts 0, so no scratch file leaked into the tree; the
   drivers, the extracted slices and the two worktrees all lived under the
   gitignored `.remedy-wt/`.
7. THE `remedy` SCRIPT WAS NOT INVOKED. It is denied to this session class;
   nothing this round needed it, so no `python3 -m apps.cli.main` substitute was
   used either.
8. `.agent/context.md` AND `.agent/decisions.md` WERE NOT TOUCHED, and the commit
   gate's item 7 was answered rather than skipped: this round's only meaningful
   decision is DECISION F040 D10, which is written into `.agent/live_review.md`
   at C2 as the durable record, and the three sub-decisions the block delegated
   are stated in this handback under "Decisions taken inside the module". Neither
   file is in the block's change set, and constraint "NOTHING ELSE IS EDITED"
   binds. Scope and constraints are unchanged from round 8, so `context.md` has
   nothing new to carry either.
9. NO DOCUMENTATION UNDER `docs/` WAS UPDATED, which is the commit gate's item 8
   answered rather than skipped: this round ships no user-visible behaviour and
   no new surface — three exported functions on a client seam that nothing mounts
   yet. `docs/` describes the BUILT system, and the card is not built. The
   feature's own file `docs/roadmap/features/T5_F040.md` is authority, not
   output, and F040 may not edit it (DECISION F040 D9's reasoning).

## Open findings

262, UNCHANGED — this round registers none, by design, and DECISION F040 D10
states why: the collision it resolves is a render-boundary mismatch, not a
wrong value on disk, so per amend0827 rule 2 it is a decision and not an R-id.

- R-0570 — OPEN, routed to the paydown branch. Not F040's to fix.
- R-0752 — OPEN, routed to the paydown branch. Not F040's to fix.
- R-0755 — OPEN, routed to the paydown branch. Not F040's to fix.
- R-0753 — OPEN, carried as this feature's documented risk.

## Next

T002 PART 5 — THE CARD ITSELF: `DigestHeroCard.tsx`, its mount, the trigger
wiring onto `digestVisibility`, and the dismissal port bound at the edge per
DECISION F040 D8, using the stylesheet from round 8 and the copy rules from this
one. SCOPE IT ACCORDINGLY: it is the first round of this feature that CANNOT be
red-proved. Every decidable rule has been pushed out of the component on purpose,
this repository renders no component in any test, and `npx vitest` is refused to
this session class — so what is left is wiring, and the only honest gate over it
is a TEXT guard that pins the mount, the bindings and the absence of a second
home for any rule. Do not order a mutation red-proof of a `.tsx` and do not
accept one.

The next session's first action is Phase 1 rule 1: re-read `.agent/STOP` from
disk before anything else, then rule 2, the Open PR Gate.
