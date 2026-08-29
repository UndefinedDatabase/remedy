# Handback — F040 · SESSION 2 · round 5 — THE ENVELOPE GOLDENS (T001's LAST CLAUSE)

> Written by the WORKER in C5, the last commit of the bundle. Every exit code
> below is REAL, taken from `subprocess.run(...).returncode` inside a script
> under the gitignored `.remedy-wt/`; not one was read through a pipe.

## Session

SESSION 2 of feature F040 · round 5 · rounds so far 5.

The soft limit (25 rounds / 7 sessions, amend0827 rule 6) is not approached, so
no scope report is owed.

## Range

Review of `458e8d51`..`HEAD` on branch `feature/f040-completion-digest`. The
base is round 4's handback commit and was the tip of the branch when this round
opened. No new branch was cut, no pull request opened, nothing merged, nothing
force-pushed.

**T001 IS NOW COMPLETE INCLUDING ITS GOLDENS CLAUSE.** The feature file's
acceptance list opens "Fixture goldens exact"; until this round no golden
existed. Four stored envelope goldens — one per state shape — now sit under
`tests/orchestration/fixtures/job_digest/golden/`, compared WHOLE against the
envelope the same fixture builds, after exactly the three identity
substitutions DECISION F040 D6 names and nothing else. NO PRODUCTION CODE WAS
EDITED: `packages/orchestration/job_digest.py` and
`packages/orchestration/ui_server.py` are untouched by this round, and every
golden matched what the composition already produces on the first generation —
no golden had to be argued into agreement.

## Commits

### 2c7c0109 docs(f040): save the round 5 step block

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f040-r5.md` | +321 −0 | C0a — the block, copied with `shutil.copyfile` from `.remedy-wt/f040-r5-block.md`, never retyped |

### 50bebff7 docs(f040): mirror the round 5 block into last_block

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +229 −165 | C0b — the same bytes, the same `shutil.copyfile` call |

### 8778f11d docs(f040): retarget the plan at the envelope goldens

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +7 −5 | C1 — slice PLAN5 applied byte for byte; SESSION 2 / round 5, T001's goldens row added, round 4's row settled to `round 4, PASS` |

### a65a4a1b docs(f040): book the round 4 verdict, R-0754 and D6

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +6 −0 | C2 — slice RECORD5 appended: the R4 PASS gate line, finding R-0754, DECISION F040 D6. Append-only; the base bytes are a prefix of the result |

### 1f31b4dc test(f040): freeze one envelope golden per state shape

| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/fixtures/job_digest/golden/green.json` | +19 −0 | C3 — the generated `green` envelope, `job_id` normalized |
| `tests/orchestration/fixtures/job_digest/golden/blocked_with_decisions.json` | +19 −0 | C3 — the generated `blocked_with_decisions` envelope; the CTA keeps its words, the job prefix and the `td:` id become placeholders |
| `tests/orchestration/fixtures/job_digest/golden/budget_stopped.json` | +19 −0 | C3 — the generated `budget_stopped` envelope |
| `tests/orchestration/fixtures/job_digest/golden/mid_run.json` | +19 −0 | C3 — the generated `mid_run` envelope |
| `tests/orchestration/test_job_digest.py` | +110 −3 | C3 — the reader: `GOLDEN_DIR`, `_normalize`, the parametrized comparison, the directory-completeness test and the narrowness guard; plus the three imports and the docstring amendment described under Deviations |

### 38dd0117 docs(f040): record amendment A3 on T001 acceptance

| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/features/T5_F040.md` | +11 −0 | C4 — pair PAIRACCEPT, APPEND-shaped: AMENDMENT A3 joins the Acceptance bullet. The clause "Fixture goldens exact" is NOT deleted; the amendment records how it is met |

### (this commit) docs(f040): write the round 5 handback

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | C5 — this file. A handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/wt-f040-r5-g3 HEAD` | rc 0 — G3's on-disk negative control |
| `git worktree remove --force .remedy-wt/wt-f040-r5-g3` | rc 0 — removed; `git worktree list` no longer holds it |
| `git worktree add --detach .remedy-wt/wt-f040-r5-g5 HEAD` | rc 0 — G5's production-code mutation |
| `git worktree remove --force .remedy-wt/wt-f040-r5-g5` | rc 0 — removed; `git worktree list` no longer holds it |
| `git worktree add --detach .remedy-wt/wt-f040-r5-g6 HEAD` | rc 0 — G6's golden perturbation |
| `git worktree remove --force .remedy-wt/wt-f040-r5-g6` | rc 0 — removed; `git worktree list` no longer holds it |
| `git push origin feature/f040-completion-digest` | after C5 — see the closing line |

No pull request created, none edited, none merged. No `gh` command run. No
force-push. The `remedy` console script was never invoked (block constraint
11); nothing this round needed it.

## Verification

Eight gates, eight REAL exit codes. Every gate ran at a commit strictly earlier
than C5.

    G1 TRANSPORT, at C0b (50bebff7)                              REAL EXIT 0
    G2 THE PLAN, at C1 (8778f11d)                                REAL EXIT 0
    G3 THE RECORD APPEND, at C2 (a65a4a1b)                       REAL EXIT 0
    G4 THE LEDGER, at C2 (a65a4a1b)                              REAL EXIT 0
    G5 THE GOLDENS BITE, at C3 (1f31b4dc)                        REAL EXIT 0
    G6 NO SELF-BLESSING, NARROW NORMALIZATION, at C3 (1f31b4dc)  REAL EXIT 0
    G7 THE FEATURE FILE, at C4 (38dd0117)                        REAL EXIT 0
    G8 THE SUITES AND THE TREE, at C4 (38dd0117)                 REAL EXIT 0

### G1 TRANSPORT — REAL EXIT 0

One sha256 over three files, all three EQUAL. The block states no expected
digest, so this is a measurement and not a match against a number I was given.

    4e3bcefd476e46e33540e3d1216b31360cefcb84f69b7468bd3eee55cd07821c  27067 bytes  .remedy-wt/f040-r5-block.md
    4e3bcefd476e46e33540e3d1216b31360cefcb84f69b7468bd3eee55cd07821c  27067 bytes  .agent/authored/f040-r5.md
    4e3bcefd476e46e33540e3d1216b31360cefcb84f69b7468bd3eee55cd07821c  27067 bytes  .agent/last_block.md
    ALL THREE EQUAL: True

The two `.agent/` copies were also read back out of git (`git show HEAD:<path>`)
and both COMMITTED blobs hash to the same digest at the same 27067 bytes.

### G2 THE PLAN — REAL EXIT 0

    PLAN5 slice     sha256 28553ded2f6a3b868853c6ca42699e800f446396314dece78070c4e48746892c  1910 bytes
    committed plan  sha256 28553ded2f6a3b868853c6ca42699e800f446396314dece78070c4e48746892c  1910 bytes
    BYTE-EQUAL: True
    line count: 40 (< 50: True )
    holds '## Goal': True  holds '## Next Steps': True

### G3 THE RECORD APPEND — REAL EXIT 0

    RECORD5 paragraph count N counted by this script: 3
    pre-commit length re-measured at 458e8d51: 1668053
    arithmetic: 1668053 + 1 + 10079 = 1678133
    committed length:                              1678133
    lengths agree: True
    (a) WHOLE RECONSTRUCTION: True
    (b) PARAGRAPH ORDER (last 3 units equal RECORD5's, in order): True
    base bytes are a PREFIX of the committed file: True
    worktree add wt-f040-r5-g3: rc=0 HEAD is now at a65a4a1b docs(f040): book the round 4 verdict, R-0754 and D6
    NEGATIVE CONTROL in wt-f040-r5-g3: byte 1668059 (offset 5 into RECORD5, inside appended paragraph 1) ' ' -> '\x00'
      flipped on disk: (a)=False  (b)=False   BOTH REJECT: True
      restored on disk: (a)=True  (b)=True  bytes equal the committed file: True
    git worktree list still holds wt-f040-r5-g3: False

The pre-commit length was RE-MEASURED here from `git show 458e8d51:...`, not
taken from the block; it agrees with the 1668053 the reviewer read. N was
counted by the script (3 blank-line units: the gate line, R-0754, D6), not
asserted. The negative control was performed ON DISK inside the disposable
worktree and both readings rejected the flipped bytes.

### G4 THE LEDGER — REAL EXIT 0

    distinct registered ids  before 314  after 315
      registered ADDED   ['R-0754']
      registered REMOVED []
    distinct resolved ids    before 53  after 53
      resolved ADDED     []
      resolved REMOVED   []
    DECISION F040 ids        before ['D1', 'D2', 'D3', 'D4', 'D5']  after ['D1', 'D2', 'D3', 'D4', 'D5', 'D6']
      DECISION ADDED     ['D6']
    '^Gate: F040 R4 — ' lines in the committed file: 1
    '^Done: R-0753' count: 0   '^Done: R-0754' count: 0
    OPEN COUNT (registered minus resolved): 262

Patterns recorded so the count can be reproduced: registered ids by
`(?m)^- (R-\d+) — `, resolved by `(?m)^Done: (R-\d+)`, decisions by
`DECISION F040 (D\d+)`. OPEN FINDINGS: **262**.

### G5 THE GOLDENS BITE — REAL EXIT 0

Control FIRST in both checkouts, then a PRODUCTION-CODE mutation inside a
disposable worktree. The mutated line is `run_report.recommended_next_action`'s
`all-green` arm — the rule `primary_action.rule_id` names for the `green` shape.
`__pycache__` was purged before every run and every run used `python3 -B`.

    [primary, unmutated] REAL EXIT 0   46 passed in 0.43s
    worktree add wt-f040-r5-g5: rc=0 HEAD is now at 1f31b4dc test(f040): freeze one envelope golden per state shape
    [wt-f040-r5-g5, CONTROL unmutated] REAL EXIT 0   46 passed in 0.41s
    MUTATION in wt-f040-r5-g5/packages/orchestration/run_report.py: "Review and merge the branch" -> "Review and land the branch"
    [wt-f040-r5-g5, MUTATED] REAL EXIT 1   1 failed, 45 passed in 0.44s
       died: tests/orchestration/test_job_digest.py::test_the_normalized_envelope_equals_its_stored_golden[green]
    the `green` golden test died: True
    the one-source CTA test died with it: False   (reported honestly either way)
    [wt-f040-r5-g5, RESTORED] REAL EXIT 0   46 passed in 0.41s
    restored bytes equal the original: True
    git worktree list still holds wt-f040-r5-g5: False

THE RISE: `tests/orchestration/test_job_digest.py` collected and passed **40**
at the base `458e8d51` (the reviewer's figure, and the figure this file's own
G8 row carried last round) and passes **46** at C3 — a rise of exactly **6**,
which is the four parametrized golden comparisons plus the directory-completeness
test plus the narrowness guard.

THE HONEST ANSWER THE GATE ASKED FOR, and it is the interesting result of this
round: the one-source CTA test did **NOT** die with the golden. That is not a
weakness in it — it is structural, and it is precisely the argument DECISION
F040 D6 makes. `test_the_primary_action_is_the_reports_own_recommendation`
asserts the digest's label against `recommended_next_action`'s OWN return value
for the same job, so when the rule table's text moves BOTH SIDES MOVE TOGETHER
and the assertion stays true. Only a STORED copy of the text notices. So the
mutation demonstrates, in one run, both that the goldens pin CONTENT rather than
shape and that they catch a class the pre-existing field-wise assertions
structurally cannot. Nothing was repaired to make this read better.

### G6 NO SELF-BLESSING, NARROW NORMALIZATION — REAL EXIT 0

(a) `ast` over the COMMITTED bytes of `tests/orchestration/test_job_digest.py`
(`git show HEAD:...`), quoting the mechanism rather than claiming a result. The
golden section is every top-level statement from the `GOLDEN_DIR` assignment
(line 519) to the end of the module (599 lines). The 29-call list below is the
gate's own single-column output re-flowed into two columns to fit; nothing else
about it is changed:

    GOLDEN_DIR assignment-target line numbers: [519]
    GOLDEN_DIR appears in exactly ONE assignment target (its own definition): True
    every Call in the golden section, as the parser resolves it (29 total):
        line  519  Path                      line  569  json.loads
        line  534  re.compile                line  569  read_text
        line  549  getattr                   line  572  pytest.mark.parametrize
        line  549  str                       line  575  Subscript
        line  553  isinstance                line  576  _normalize
        line  554  value.replace             line  576  _read_golden
        line  556  text.replace              line  576  build_job_digest
        line  557  DECISION_ID_PATTERN.sub   line  581  GOLDEN_DIR.iterdir
        line  558  isinstance                line  581  sorted
        line  559  _replace                  line  582  len
        line  559  value.items               line  582  len
        line  560  isinstance                line  583  sorted
        line  561  _replace                  line  595  Subscript
        line  564  _replace                  line  596  _normalize
                                             line  596  build_job_digest
    calls whose final attribute is a write verb ['dump', 'mkdir', 'touch', 'unlink', 'write_bytes', 'write_text']: []
    calls to `open` with a write mode in the section: []
    same write verbs over the WHOLE module: []
    (a) VERDICT: PASS

The only filesystem verbs the section reaches are `read_text` and `iterdir`,
both reads. The write-verb sweep was widened past the four the gate named
(`open`-with-write-mode, `write_text`, `write_bytes`, `json.dump`) to include
`mkdir`, `touch` and `unlink`, and run over the WHOLE module as well as the
section; all three readings are empty. There is no regenerate flag and no
environment switch: `GOLDEN_DIR` is bound exactly once and never reassigned.

(b) One byte of one stored golden perturbed on disk in a disposable worktree —
the `peak_urgency` digit, a value `_normalize` is forbidden to touch:

    worktree add wt-f040-r5-g6: rc=0 HEAD is now at 1f31b4dc test(f040): freeze one envelope golden per state shape
    [wt-f040-r5-g6, CONTROL] REAL EXIT 0   46 passed in 0.41s
    PERTURBATION in wt-f040-r5-g6/tests/orchestration/fixtures/job_digest/golden/blocked_with_decisions.json: byte 279 '2' -> '3'  (peak_urgency 2400 -> 3400)
    [wt-f040-r5-g6, PERTURBED] REAL EXIT 1   1 failed, 45 passed in 0.43s
    [wt-f040-r5-g6, RESTORED] REAL EXIT 0   46 passed in 0.41s
    restored bytes equal the original: True
    git worktree list still holds wt-f040-r5-g6: False

### G7 THE FEATURE FILE — REAL EXIT 0

    TO contains FROM (the pair is APPEND-shaped): True
    FROM occurs in the committed file exactly 1x: 1 occurrence(s)
    C4's diff adds 11 line(s) and removes 0
    TO-only lines: 11; each must occur exactly 1x among the added lines:
        1x    AMENDMENT A3 (DECISION F040 D6, 2026-08-29): "fixture goldens
        1x    exact" is met by ENVELOPE goldens — one stored JSON per state
        1x    shape under `tests/orchestration/fixtures/job_digest/golden/`,
        1x    compared WHOLE against the envelope the same fixture builds.
        1x    Exactly three identities are normalized first, because they
        1x    differ on every build: the job's UUID, the job's first-eight
        1x    prefix, and each `td:` decision id, each replaced by a fixed
        1x    placeholder everywhere it occurs including inside strings.
        1x    Nothing else is normalized — headlines, labels, rule ids, counts
        1x    and urgencies are compared as they are — and the test never
        1x    writes a golden.
    'AMENDMENT A3' occurs 1x   'AMENDMENT A1' 1x   'AMENDMENT A2' 1x
    T001's Task-slicing entry, UNCHANGED by this round: True
        - **T001** the endpoint composition + rule-table import + fixtures
          per state shape (green, blocked-with-decisions, budget-stopped,
          mid-run) + goldens.
    the acceptance CLAUSE itself still stands: True

Per block constraint 14 the obligation was read as APPEND-shaped: FROM at
exactly 1x and each TO-only line at exactly 1x among the ADDED lines, never a
FROM-zero count. C4's diff adds 11 lines and removes none, and the 11 added
lines are exactly the 11 TO-only lines.

### G8 THE SUITES AND THE TREE — REAL EXIT 0

Six suites, run SERIALLY, each with its own REAL exit code:

    REAL EXIT 0  tests/orchestration/test_job_digest.py           46 passed in 0.43s
    REAL EXIT 0  tests/ui_server/                                 515 passed in 32.79s
    REAL EXIT 0  tests/ui_contracts/                              699 passed, 4 skipped in 6.01s
    REAL EXIT 0  tests/docs/                                      295 passed in 0.61s
    REAL EXIT 0  tests/orchestration/test_integrity_gate.py       16 passed in 0.30s
    REAL EXIT 0  tests/cli/test_golden_path.py                    42 passed in 20.74s

    git status --porcelain EMPTY: True   ''
    git ls-files --others --exclude-standard count: 0

    per-commit insertion counts, C0a through C4:
        2c7c0109  +321   -0     1 path(s)  under 500: True
        50bebff7  +229   -165   1 path(s)  under 500: True
        8778f11d  +7     -5     1 path(s)  under 500: True
        a65a4a1b  +6     -0     1 path(s)  under 500: True
        1f31b4dc  +186   -3     5 path(s)  under 500: True
        38dd0117  +11    -0     1 path(s)  under 500: True

Against the base figures: `test_job_digest.py` 40 → 46 (+6, this round's
tests); `tests/ui_server/` 515 → 515, `tests/ui_contracts/` 699+4s → 699+4s,
`test_integrity_gate.py` 16 → 16 and `test_golden_path.py` 42 → 42, all
unmoved, which is what a round that edits no production code should produce.
`tests/docs/` was NOT measured at the base by the reviewer, so no rise can be
stated for it; it is **295 passed at REAL EXIT 0**, green — reported, not
repaired, and it reads the feature file C4 edited.

Also run, though no gate ordered it:
`python3 -m ruff check tests/orchestration/test_job_digest.py` — REAL EXIT 0,
"All checks passed!".

## Authored-text proofs

Every reviewer-authored unit was extracted MECHANICALLY from
`.remedy-wt/f040-r5-block.md` by a script that slices between the `<<<BEGIN
NAME` / `<<<END NAME` marker lines (markers excluded, the newline ending the
last content line included) and writes each to
`.remedy-wt/f040r5_units/<NAME>.txt`. Nothing was retyped.

| Unit | Bytes | sha256 | Applied to | Proof |
|---|---|---|---|---|
| the block itself | 27067 | `4e3bcefd…c07821c` | `.agent/authored/f040-r5.md`, `.agent/last_block.md` | G1 — three-way disk-to-disk equality, plus both committed blobs re-hashed from `git show` |
| PLAN5 | 1910 | `28553ded…46892c` | `.agent/plan.md` | G2 — byte-equality against the COMMITTED file |
| RECORD5 | 10079 | `14a6ba4d…52df9f` | `.agent/live_review.md` | G3 — whole reconstruction + paragraph order + prefix, with an on-disk negative control |
| PAIRACCEPT-FROM | 335 | `e4910ef9…bbf363` | `docs/roadmap/features/T5_F040.md` | G7 — the FROM anchor survives at exactly 1x |
| PAIRACCEPT-TO | 994 | `c8007eb0…f7e8b` | `docs/roadmap/features/T5_F040.md` | G7 — each of the 11 TO-only lines occurs exactly 1x among C4's added lines |

## Deviations & assumptions

1. **THE THREE NEW IMPORTS SIT AT THE TOP OF THE MODULE, NOT IN THE APPENDED
   SECTION.** The C3 SPEC says the reader is "appended as a new section at the
   END" of `tests/orchestration/test_job_digest.py`. The section itself is
   appended verbatim to the end; `import json`, `import re` and
   `from pathlib import Path` were added to the module's existing top import
   block instead, because a module-level import after code is `ruff` E402 and
   the file would not lint. Declared rather than silently done.
2. **THE MODULE DOCSTRING WAS AMENDED — 3 lines removed, 6 added — AND THE
   BLOCK DID NOT ORDER IT.** The sentence at the old line 12 read "A golden
   would keep passing while the digest and the report drifted apart, which is
   precisely the failure F040 is built to prevent." Left standing it would
   argue against the section now sitting some 500 lines below it. It now reads "A
   golden ALONE would keep passing … so the golden section at the bottom stands
   BESIDE that assertion and never in place of it (DECISION F040 D6, finding
   R-0754)", which is D6's own reasoning and R-0754's own answer to that
   sentence. The file is in the change set; the edit is in scope by path but
   not by instruction, so it is declared here.
3. **THE GOLDENS ARE SERIALIZED WITH `ensure_ascii=False`.** `indent=2` and the
   trailing newline follow `test_cost_report.py`'s convention exactly. The
   default `ensure_ascii=True` would store the `indeterminate` CTA's em dash as
   the six-character escape `—`; the SPEC asks for goldens "pretty-printed
   with a trailing newline so a diff is readable", and an escaped dash is not.
   No other serialization choice differs from the sibling.
4. **GENERATION RAN FROM A THROWAWAY SCRIPT, NEVER FROM THE TEST.**
   `.remedy-wt/f040r5_generate.py` (gitignored, uncommitted) replicates ONLY
   the module's two autouse fixtures — the isolated `REMEDY_DATA_DIR` and the
   frozen `decision_inbox` clock — and imports `_normalize` FROM the committed
   test module, so the bytes written are the bytes the shipped reader compares
   against. The committed test has no write path of any kind (G6a). The
   generated files were then read back and checked by eye against each shape
   fixture before committing: `green` is COMPLETED + `all_green` with both
   tasks completed and nothing open, `blocked_with_decisions` is PAUSED +
   `blocked` with `open_count` 2 and `peak_urgency` (3+1)×600 = 2400,
   `budget_stopped` is PAUSED + `budget_exhausted` reaching `blocked-failed`,
   and `mid_run` is RUNNING with no terminal status and the `indeterminate`
   rule. All four agree with the two-build stability probe.
5. **NO PRODUCTION CODE CHANGED, AND NONE NEEDED TO.** Every golden matched the
   composition's real output on the first generation. The block's STOP clause
   for "a golden that cannot be made to match without editing production code"
   was never reached.
6. **G5's ONE-SOURCE RESULT IS REPORTED, NOT REPAIRED.** The mutation killed
   the `green` golden and did not kill the one-source CTA test. See the G5
   transcript above for why that is structural and expected rather than a gap.
7. **C0a AND C0B PRECEDE C1, SO TWO COMMITS LAND WHILE `.agent/plan.md` STILL
   NAMES ROUND 4.** This is the block's own bundle order together with its
   constraint 3 ("C1 is the FIRST substantive commit"), not a departure from
   it, and it is the established shape of every round of this feature. Noted so
   a reader auditing the AGENTS.md commit gate against the first two commits
   does not have to reconstruct why.
8. **THE `remedy` CONSOLE SCRIPT WAS NEVER INVOKED** (block constraint 11). No
   step of this round needed it, so no `python3 -m apps.cli.main` substitute
   was needed either.
9. No commit subject carries a leading-slash token, an absolute path, a
   secret-like string or a `Co-Authored-By` trailer (block constraint 12);
   every commit's insertion count is under 500 (G8), so no oversize-commit
   declaration is owed.
10. All three disposable worktrees were removed by exact path
    (`.remedy-wt/wt-f040-r5-g3`, `-g5`, `-g6`), never by glob, and
    `git worktree list` was re-read after each removal.

## Item status

| Item | Status | Reason |
|--------|----------|------------------------------|
| C0a save the block to `.agent/authored/f040-r5.md` | done | `shutil.copyfile`; 2c7c0109 |
| C0b mirror into `.agent/last_block.md` | done | `shutil.copyfile`; 50bebff7 |
| C1 rewrite `.agent/plan.md` from PLAN5 | done | byte-equal; 8778f11d |
| C2 append RECORD5 to `.agent/live_review.md` | done | append-only; a65a4a1b |
| C3 the four goldens and their reader | done | one commit, both halves; 1f31b4dc |
| C4 apply PAIRACCEPT to `docs/roadmap/features/T5_F040.md` | done | append-shaped; 38dd0117 |
| C5 rewrite `.agent/handoff.md` | done | this commit |
| G1 TRANSPORT | done | REAL EXIT 0 |
| G2 THE PLAN | done | REAL EXIT 0 |
| G3 THE RECORD APPEND | done | REAL EXIT 0 |
| G4 THE LEDGER | done | REAL EXIT 0; open count 262 |
| G5 THE GOLDENS BITE | done | REAL EXIT 0; 40 → 46, rise 6 |
| G6 NO SELF-BLESSING / NARROWNESS | done | REAL EXIT 0 |
| G7 THE FEATURE FILE | done | REAL EXIT 0 |
| G8 THE SUITES AND THE TREE | done | REAL EXIT 0; six suites, clean tree |

## Findings state

| Id | State |
|---|---|
| R-0570 | OPEN — routed to the paydown branch |
| R-0752 | OPEN — routed to the paydown branch |
| R-0753 | OPEN — a documented risk this feature carries: the persisted actuals record has no money field for the digest's cost basis to read |
| R-0754 | REGISTERED AND FIXED IN THIS SAME ROUND — registered by C2, discharged by DECISION F040 D6, the four goldens and their reader in C3, and AMENDMENT A3 in C4. Not marked `Done:` in the ledger; that booking belongs to the round that gates this one |

Open findings after C2: **262**.

## Next

**T002 — the hero card.** Build it against the canonical design reference in
`docs/ui/design_reference/` per the binding CSS in the feature file, wire the
trigger / dismiss / last-seen mechanics, and retire the TypeScript urgency copy
per DECISION F040 D2 so the urgency formula has ONE home instead of the two
`tests/ui_contracts/test_decision_urgency_parity.py` currently pins equal.
Before authoring it, re-read `.agent/STOP` from disk (Phase 1 rule 1, ahead of
rule 2) — it did not exist at any reading this round.

Branch `feature/f040-completion-digest` pushed after C5. No pull request opened,
nothing merged, nothing force-pushed.
