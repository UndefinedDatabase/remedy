# Handoff — F277 Machine contracts: event vocabulary, JSON envelope, exit codes · Round 12

## Session

SESSION 7 of feature F277 · round 12 · rounds so far 12

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE.

**SCOPE REPORT (obliged by amend0827 rule 6 at the 7-session soft limit).**
*What is finished.* T001, the event vocabulary, is a complete contract:
`packages/orchestration/event_names.py` declares 84 names plus 2 retirements, the AST test
asserts read ⊆ declared and written ⊆ declared and is red-proved, and DECISION F277 D5
disposed of all six names found read-and-never-written. T002, the JSON envelope and the
dispatch error boundary, is a complete contract: `apps/cli/json_envelope.py` carries one
shape behind `build_ok`/`build_error`/`emit_ok`/`emit_error`/`fail`, and `grouped.py`'s
catch-all boundary means no traceback reaches an operator.
*What is missing.* T003 is APPLIED IN PART — the `fail()` helper exists and nine of the
twenty-eight CLI modules call it; nineteen modules and the catalog half (the read-only
commands not declaring `supports_json`, plus the two false declarations on `init run` and
`dev status`) remain. T004 is NOT STARTED: no exit code has a documented meaning and
`tests/cli/test_json_contract.py` does not exist.
*The proposal, and it is already executed.* DECISION F277 D10 takes the standing
split-and-close default of amend0905-throughput: F277 closes on T001 and T002 complete and
T003 in part, and the remainder is registered as F283 — Machine contracts, part two — placed
directly after F277's own STATUS line under amend0906-split-placement. The operator question
this owes is `.agent/operator_questions.md` Q2, which states the reading the operator may
overturn: the limit fired on SESSIONS at round 11 of 25, not on rounds.

THE SESSION NUMBER, CORRECTED THIS ROUND. The `Gate:` entries in `.agent/live_review.md` for
rounds 1 to 10 label their reviewing sessions FIRST, SECOND and THIRD; the handoff chain
across the eleven handback commits that carry the mandated field runs SESSION 1 through
SESSION 6 continuously. AGENTS.md makes the handback field the carrier of record, so the
handoff chain is right and the ledger labels undercount by three. Round 12's ledger entry and
the second prose-slip line record that reconciliation; no landed entry was edited.

Context self-assessment: the worker read `AGENTS.md`, `docs/agents/handback_template.md`,
`.remedy-wt/f277-r12-block.md` and `docs/roadmap/features/T2_F277.md` in full before any
edit, verified the block's own bytes first (R-0954, below), found no `.agent/STOP` on disk,
verified the branch clean at `67b0972d`, then verified all eleven PAYLOADS entries against
the block's table before using any of them. Executed the five-commit bundle C1a, C1b, C2, C3,
C4 in order and ran all six gates for real.

## Range

Review of `67b0972d`..`HEAD`.

## Commits

### 548d773f F277 R12 C1a: copy round 12 payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f277-r12-block.md | +229/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f277-r12-context.md | +49/-0 | byte-for-byte copy of context.md payload |
| .agent/authored/f277-r12-decisions.md | +65/-0 | byte-for-byte copy of decisions.md payload |
| .agent/authored/f277-r12-f277-file.diff | +92/-0 | byte-for-byte copy of f277-file.diff payload |
| .agent/authored/f277-r12-f283.md | +90/-0 | byte-for-byte copy of f283.md payload |
| .agent/authored/f277-r12-ledger.md | +2/-0 | byte-for-byte copy of ledger.md payload |
| .agent/authored/f277-r12-pin.diff | +17/-0 | byte-for-byte copy of pin.diff payload |
| .agent/authored/f277-r12-plan.md | +46/-0 | byte-for-byte copy of plan.md payload |
| .agent/authored/f277-r12-questions.md | +39/-0 | byte-for-byte copy of questions.md payload |
| .agent/authored/f277-r12-readme.diff | +19/-0 | byte-for-byte copy of readme.diff payload |
| .agent/authored/f277-r12-slips.md | +2/-0 | byte-for-byte copy of slips.md payload |
| .agent/authored/f277-r12-status.diff | +11/-0 | byte-for-byte copy of status.diff payload |

Measured insertions by `git show --numstat`: **661**. Block's formula: its own line count
(229, measured) plus 432 = 661. The eleven payload copies sum to 432, measured. MATCHES.

### b77d989f F277 R12 C1b: book round 11's PASS, DECISION D10 and the split scope report
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | +13/-6 | rewrite to context.md payload, byte-identical (sha `c40f9910…`), 49 lines |
| .agent/decisions.md | +65/-0 | append DECISION F277 D10 (decisions.md payload) |
| .agent/live_review.md | +2/-0 | append round 11's PASS entry (ledger.md payload) |
| .agent/operator_questions.md | +39/-0 | append operator question Q2 (questions.md payload) |
| .agent/plan.md | +27/-30 | rewrite to plan.md payload, byte-identical (sha `ce8fe437…`), 46 lines |
| .agent/prose_slips.md | +2/-0 | append two prose-slip lines (slips.md payload) |

Measured insertions by `git show --numstat`: **148** (13+65+2+39+27+2). The block EXPECTED
**203** (2+2+65+39+46+49). The difference is entirely in the two REWRITES and is a
diff-algorithm reading, not a content difference: the block's 46 and 49 assume a whole-file
replacement, while git computes a minimal diff and charges `.agent/plan.md` +27/-30 and
`.agent/context.md` +13/-6. The four APPENDS land at exactly their payload line counts
(2, 65, 2, 39 = 108, as predicted). No payload was adjusted to reach 203, per the block's own
instruction. Both rewritten files are byte-identical to their payloads — see G1(d).
`git commit`'s own terminal summary printed a third pair, `167 insertions(+), 55 deletions(-)`
with `rewrite .agent/plan.md (81%)`, because it applies rewrite detection; the numstat reading
is the one DECISION F104 D1 fixes and 148 is far under the 500 cap.

### 90976846 F277 R12 C2: register F283 — machine contracts part two: feature file, STATUS line, pin 283, README counters
| Path | +/- | Reason |
|---|---|---|
| README.md | +2/-2 | apply readme.diff: ledger total 282→283, Tier 2 cell 35→36 |
| docs/roadmap/STATUS.md | +1/-0 | apply status.diff: the F283 line, directly after F277's |
| docs/roadmap/features/T2_F283.md | +90/-0 | new file from f283.md payload, byte-identical (sha `2b6ff2b3…`), explicitly `git add`ed |
| tests/docs/test_docs_consistency.py | +6/-1 | apply pin.diff: `TOTAL_FEATURES` 282→283 and its five-line registration comment |

Measured insertions by `git show --numstat`: **99** (2+1+90+6). Block expected **99**. MATCHES.
All four edits are in this one commit — see G2.

### 3c3ca820 F277 R12 C3: strike the moved Acceptance bullets and write F277's Built State
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T2_F277.md | +71/-5 | apply f277-file.diff: strike the three moved Acceptance bullets with a struck-here paragraph, add the Built State section |

Measured insertions by `git show --numstat`: **71**. Block expected **71**. MATCHES.

Self-reference exception (handback template, R-0149 pattern): the commit that writes this
handoff and the trailing commit that fills in its post-push G6 readings share one grouped
table with per-commit attribution, following rounds 9, 10 and 11's identical precedent — a
handback cannot table the commit that writes it.

### (this commit) F277 R12 C4: rewrite handoff for round 12
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, first and only write; G6's push/status/worktree readings are not knowable before the push C4 performs |

### (trailing) F277 R12 C4-fix: record the actual push outcome in the handoff
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | this edit | fill in the real `git push` / `git status --porcelain` / `git worktree list` output for G6, only knowable after C4 was pushed |

## External actions

- `git push -u origin feature/f277-machine-contracts` — outcome under Verification / G6 below
  (the round's final act). No worktree was added or removed this round: the block orders no
  destructive verification, and constraint 6 states why.
- No `gh` command, no PR created, edited or merged.

## Verification

### Pre-flight

- `ls .agent/STOP` → `No such file or directory`, real exit code **2**. No STOP on disk.
- `git status --porcelain` → empty.
- `git branch --show-current` → `feature/f277-machine-contracts`.
- `git rev-parse HEAD` → `67b0972df78ab0ce5023471fc0be182cf59bd9fa`, matching the block's
  stated tip `67b0972d`.
- Block self-verification (R-0954), `.remedy-wt/f277-r12-block.md`:

| reading | measured | given in the delegation message | equal |
|---|---|---|---|
| line count | 229 | 229 | True |
| sha256 | `de2eadea7766f4d0876f54b97ae6bf472760d41c5f5e57f6831cbccb8411acca` | `de2eadea7766f4d0876f54b97ae6bf472760d41c5f5e57f6831cbccb8411acca` | True |

### G1(a) — PAYLOADS transport, all eleven files, 33 readings

| file | lines measured / given | bytes measured / given | sha256 measured (given identical) | equal |
|---|---|---|---|---|
| context.md | 49 / 49 | 2621 / 2621 | `c40f9910340ca109fa07c7963e0fe9dd58a71c0c6054b218cc182c200b96c69e` | True |
| decisions.md | 65 / 65 | 4708 / 4708 | `ce012695e0bebf539b6c9db2a9e8fcf00734d6288d4611e4901ac54a6d494a17` | True |
| f277-file.diff | 92 / 92 | 6665 / 6665 | `99c570b0f69a313e9c792d5d9a007c7d444af33eb6d048fc8ed1b1c5e4fa43b2` | True |
| f283.md | 90 / 90 | 5472 / 5472 | `2b6ff2b34cf82b9452be409ef6cf4da7c63ec379e42431edc2f43c76777fee39` | True |
| ledger.md | 2 / 2 | 7273 / 7273 | `0c34a0770d977a17a9ed56c9f23a126f235a0ac506bf72da8deda48208d729fd` | True |
| pin.diff | 17 / 17 | 836 / 836 | `37241db16f88a34a44c367d775313bbd764a66f2972b683e22268b648b1d39b6` | True |
| plan.md | 46 / 46 | 2425 / 2425 | `ce8fe437a82fb00cc24fcfc5a50ded844cfc4605aa579e9a0d562704a5d46396` | True |
| questions.md | 39 / 39 | 2789 / 2789 | `ade37891181ba543edeaa808c17ba4ea7fe6a477b0db5fedda9694305d99a97c` | True |
| readme.diff | 19 / 19 | 655 / 655 | `e207d8e0fce50336115a14f66a1901d01cb5f8f87e8325803da0b1de0f4fdbaa` | True |
| slips.md | 2 / 2 | 2365 / 2365 | `0ea03bac3f8c11ccb03e4c1f7b7156c87d59f469d486d09c01a620d37990b604` | True |
| status.diff | 11 / 11 | 1371 / 1371 | `5881978ca6ec288ff1677ad1416c581509b873ff886e838fb7e20bb228e63b2a` | True |

Script printed `READINGS_EQUAL 33 of 33`, real exit code 0. The payload directory holds
exactly these eleven files and no twelfth.

`git apply --check` on each of the four diffs, run before any real apply — all real exit
code 0:

```
=== f277-file.diff ===  REAL_EXIT=0
=== pin.diff ===        REAL_EXIT=0
=== readme.diff ===     REAL_EXIT=0
=== status.diff ===     REAL_EXIT=0
```

`f277-file.diff` was re-checked immediately before its own apply at C3: `CHECK_EXIT=0`,
`APPLY_EXIT=0`.

### G1(b) — the twelve `.agent/authored/f277-r12-*` copies vs. their sources

Each copy read back from disk and compared byte-for-byte with its source under
`.remedy-wt/f277-r12-payloads/` (the block copy against `.remedy-wt/f277-r12-block.md`):

| copy | bytes | lines | IDENTICAL_TO_SOURCE |
|---|---|---|---|
| f277-r12-block.md | 15466 | 229 | True |
| f277-r12-context.md | 2621 | 49 | True |
| f277-r12-decisions.md | 4708 | 65 | True |
| f277-r12-f277-file.diff | 6665 | 92 | True |
| f277-r12-f283.md | 5472 | 90 | True |
| f277-r12-ledger.md | 7273 | 2 | True |
| f277-r12-pin.diff | 836 | 17 | True |
| f277-r12-plan.md | 2425 | 46 | True |
| f277-r12-questions.md | 2789 | 39 | True |
| f277-r12-readme.diff | 655 | 19 | True |
| f277-r12-slips.md | 2365 | 2 | True |
| f277-r12-status.diff | 1371 | 11 | True |

Twelve readings, all True. Real exit code 0.

### G1(c) — the four appends at C1b, measured from the COMMITTED blobs

Pre read with `git show 67b0972d:<path>`, post with `git show b77d989f:<path>`; neither off
the working tree.

| file | pre measured | pre, reviewer's | equal | payload | post | post−pre | pre+payload=post |
|---|---|---|---|---|---|---|---|
| .agent/live_review.md | 439654 | 439654 | True | 7273 | 446927 | 7273 | True |
| .agent/prose_slips.md | 342200 | 342200 | True | 2365 | 344565 | 2365 | True |
| .agent/decisions.md | 1787112 | 1787112 | True | 4708 | 1791820 | 4708 | True |
| .agent/operator_questions.md | 2572 | 2572 | True | 2789 | 5361 | 2789 | True |

Four readings, all True; all four pre values equal the reviewer's. Each post additionally
verified as pre-prefixed and payload-suffixed.

NEGATIVE CONTROL, on `.agent/live_review.md` only. One bit flipped at absolute offset 443290,
inside the appended region `[439654, 446927)` — byte 120 → 121, length unchanged:

```
prefix check pre == mutated[:len(pre)]      : True
suffix check mutated[len(pre):] == payload  : False      <- the control
UNMUTATED suffix check, for comparison      : True
```

The reading returns False under a single flipped bit and True without it, so the comparison
can fail. Real exit code 0.

### G1(d) — the two rewrites at C1b

| file | payload sha256 | committed sha256 at b77d989f | EQUAL | lines |
|---|---|---|---|---|
| .agent/plan.md | `ce8fe437a82fb00cc24fcfc5a50ded844cfc4605aa579e9a0d562704a5d46396` | `ce8fe437a82fb00cc24fcfc5a50ded844cfc4605aa579e9a0d562704a5d46396` | True | 46 |
| .agent/context.md | `c40f9910340ca109fa07c7963e0fe9dd58a71c0c6054b218cc182c200b96c69e` | `c40f9910340ca109fa07c7963e0fe9dd58a71c0c6054b218cc182c200b96c69e` | True | 49 |

`.agent/plan.md` reads 46 lines, satisfying constraint 5 and the AGENTS.md under-50 rule.

### G1(e) — open set by distinct id in `.agent/live_review.md`

| rev | ids matching `^- R-\d+ — ` | ids matching `^Done: R-\d+ — ` | OPEN |
|---|---|---|---|
| 67b0972d | 27 | 7 | **20** |
| b77d989f (C1b) | 27 | 7 | **20** |

Both numbers measured, not asserted equal. Round 12 registered and resolved nothing.

### G2 — the registration is ledger-atomic

`git diff --name-only b77d989f 90976846`:

```
README.md
docs/roadmap/STATUS.md
docs/roadmap/features/T2_F283.md
tests/docs/test_docs_consistency.py
```

LENGTH **4**; set equals the four expected paths exactly, no fifth.
`docs/roadmap/features/T2_F283.md` IS present, so the explicit `git add` of the new file was
not omitted. Real exit code 0.

From the tree at C2 (`90976846`):

- `TOTAL_FEATURES = 283`
- README: `87 of 283 registered items accepted. Next: the first unchecked item in docs/roadmap/STATUS.md.`
- README Tier 2 row: `| 2 | Minimal Self-Build Runtime | 29 | 36 |`
- STATUS line 46: `- [~] F277 — Machine contracts: event vocabulary, JSON envelope, exit codes`
- STATUS line 47: `- [ ] F283 — Machine contracts, part two: the refusal sweep, the JSON gap and the exit-code taxonomy`
- F283_IMMEDIATELY_AFTER_F277: **True** (46 → 47, adjacent)
- Enclosing heading for BOTH lines: `## Tier 2 — Easy Start & Contract Block (operator order amend0905)`; SAME_TIER2_HEADING **True**

### G3 — the docs and state-contract gate, primary checkout, at C3

```
$ python3 -m pytest -q -p no:cacheprovider tests/docs/ \
  tests/orchestration/test_roadmap_index.py tests/orchestration/test_test_runner.py \
  tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py
481 passed in 105.33s (0:01:45)
```
Real exit code **0**.

Against the reviewer's dry run of `479 passed, 2 skipped` at exit 0: the COLLECTED TOTAL is
the same number, 481, and the exit code is the same, but here nothing skipped. The two tests
the reviewer's disposable worktree skipped ran and passed in the primary checkout — the
fresh-worktree-first-run difference. Reported as measured, not reconciled away. A targeted
re-run of `tests/ui_server/test_dashboard_contract.py -rs` read `67 passed` at exit 0 with no
skip reasons, so the two skips were not in that file. `git status --porcelain` immediately
after the gate: empty. The full suite was NOT run, per amend0917 rule 1.

### G4 — lint and canary

```
$ python3 -m ruff check tests/docs/test_docs_consistency.py
All checks passed!
```
Real exit code **0**.

```
$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 130.98s (0:02:10)
```
Real exit code **0**.

### G5 — the round's whole path set

`git diff --name-only 67b0972d 3c3ca820`, with the commit that introduced each entry:

| # | commit | path |
|---|---|---|
| 1 | C1a | .agent/authored/f277-r12-block.md |
| 2 | C1a | .agent/authored/f277-r12-context.md |
| 3 | C1a | .agent/authored/f277-r12-decisions.md |
| 4 | C1a | .agent/authored/f277-r12-f277-file.diff |
| 5 | C1a | .agent/authored/f277-r12-f283.md |
| 6 | C1a | .agent/authored/f277-r12-ledger.md |
| 7 | C1a | .agent/authored/f277-r12-pin.diff |
| 8 | C1a | .agent/authored/f277-r12-plan.md |
| 9 | C1a | .agent/authored/f277-r12-questions.md |
| 10 | C1a | .agent/authored/f277-r12-readme.diff |
| 11 | C1a | .agent/authored/f277-r12-slips.md |
| 12 | C1a | .agent/authored/f277-r12-status.diff |
| 13 | C1b | .agent/context.md |
| 14 | C1b | .agent/decisions.md |
| 15 | C1b | .agent/live_review.md |
| 16 | C1b | .agent/operator_questions.md |
| 17 | C1b | .agent/plan.md |
| 18 | C1b | .agent/prose_slips.md |
| 19 | C2 | README.md |
| 20 | C2 | docs/roadmap/STATUS.md |
| 21 | C2 | docs/roadmap/features/T2_F283.md |
| 22 | C2 | tests/docs/test_docs_consistency.py |
| 23 | C3 | docs/roadmap/features/T2_F277.md |

LENGTH **23** — the eleven paths the block names plus the twelve C1a copies. The set equals
exactly that union (`SET_IS_EXACTLY_EXPECTED_PLUS_AUTHORED True`). Paths under `packages/` or
`apps/`: **count 0**, empty list — a measured count, not an assertion. Real exit code 0.
Constraint 3 therefore holds: no production file, no test file other than
`tests/docs/test_docs_consistency.py`, no command-group migration.

### G6 — push and tree, after C4

C4 commits this handoff and THEN pushes, so the three readings below did not exist at the
moment C4 was written. They are recorded verbatim by the trailing C4-fix commit, which
touches nothing else (deviation 3).

- `git push -u origin feature/f277-machine-contracts`, real exit code **0**:
```
To github.com:UndefinedDatabase/remedy.git
   67b0972d..805387e0  feature/f277-machine-contracts -> feature/f277-machine-contracts
Branch 'feature/f277-machine-contracts' set up to track remote branch 'feature/f277-machine-contracts' from 'origin'.
```
  Succeeded. The remote tip of the branch is `805387e0`, which is C4.
- `git status --porcelain` after the push: **empty** (no output), exit code 0.
- `git worktree list` after the push, exit code 0:
```
/home/decodeux/Repos/remedy                                  805387e0 [feature/f277-machine-contracts]
/home/decodeux/Repos/remedy/.remedy-wt/job-468c8e62a2cc4fac  1b9ae606 [remedy/job-468c8e62a2cc4fac]
/home/decodeux/Repos/remedy/.remedy-wt/job-c1dba9c3d7874968  fd23710f [remedy/job-c1dba9c3d7874968]
```
  Three entries: the primary checkout and the two pre-existing `remedy/job-*` worktrees,
  nothing else. No worktree was added or removed this round.

C4-fix, the commit carrying this paragraph, is itself pushed immediately after it; its own
push outcome is reported in the session output rather than recursively here.

## Authored-text proofs

Every reviewer-authored text applied this round was compared disk-to-disk against its
committed `.agent/authored/f277-r12-*` copy, per the fidelity protocol:

- The twelve copies at C1a vs. their originals under `.remedy-wt/f277-r12-payloads/` (block
  copy vs. `.remedy-wt/f277-r12-block.md`): twelve readings, all True — see G1(b).
- The two REWRITE payloads vs. the committed files at C1b: `.agent/plan.md` and
  `.agent/context.md`, both sha256-equal to their payloads — see G1(d).
- The four APPEND payloads vs. the committed files at C1b: each committed file is its
  `67b0972d` bytes as an exact prefix plus its payload as an exact suffix — see G1(c), with
  a negative control proving the comparison can return False.
- The WHOLE NEW FILE payload vs. the committed file at C2: `docs/roadmap/features/T2_F283.md`
  read back at 5472 bytes / 90 lines / sha256 `2b6ff2b34cf82b9452be409ef6cf4da7c63ec379e42431edc2f43c76777fee39`,
  `IDENTICAL_TO_PAYLOAD True`.
- The four `.diff` payloads were never retyped and never edited: each went on with
  `git apply` after its own `git apply --check` at exit 0, and their committed copies are
  byte-identical to the originals (G1(b)).

## Deviations & assumptions

1. **C1b's measured insertions are 148, not the block's expected 203.** Declared here as the
   block instructed. The four appends landed at exactly their payload line counts; the gap is
   entirely git's minimal diff over the two REWRITES (`.agent/plan.md` +27/-30 rather than
   +46/-49, `.agent/context.md` +13/-6 rather than +49/-42). No payload was touched to reach
   203, and G1(d) shows both rewritten files byte-identical to their payloads, so the content
   is exactly what the block ordered and only the counting convention differs. A third
   reading exists and is not the governing one: `git commit`'s terminal summary printed
   `167 insertions(+), 55 deletions(-)` under rewrite detection.
2. **The operator question landed in C1b, not in the handback commit.** Declared per the
   block's own "WHY THE OPERATOR QUESTION IS HERE AND NOT IN THE HANDBACK COMMIT" paragraph:
   amend0911-feedback rule C's obligation is that the WORKER writes the file and the reviewer
   stays read-only, which C1b satisfies, and amend0917-throughput rule 4 puts a round's
   DECISION in the one bookkeeping commit — Q2 is this round's DECISION in question form.
   Chosen, not missed.
3. **A trailing C4-fix commit beyond the block's five, for G6's post-push readings.** C4
   writes this handoff and then pushes, so the `git push` / `git status` / `git worktree list`
   outcomes cannot exist when C4 is committed. C4-fix records the real readings and touches
   nothing else. This is the handback template's explicit trailing-bookkeeping exception
   (R-0149 pattern) and follows rounds 9, 10 and 11's identical, reviewed precedent. Apart
   from it, the five-commit bundle ran in the block's exact order — none dropped, none
   reordered, none added.
4. **G3's skip count differs from the reviewer's dry run and the pass count therefore also
   differs**: `481 passed, 0 skipped` here against `479 passed, 2 skipped` in the reviewer's
   disposable worktree, same collected total of 481 and same exit code 0. Not reconciled,
   reported as measured.
5. **One command beyond the ordered gates**: `python3 -m pytest -q -p no:cacheprovider -rs
   tests/ui_server/test_dashboard_contract.py` (`67 passed`, exit 0), run only to locate
   deviation 4's two skips rather than speculate about them. Read-only, no tree effect —
   `git status --porcelain` empty afterwards.
6. **An inaccuracy inside an applied payload, left unrepaired because constraint 1 forbids
   editing a payload.** `f277-file.diff`'s "WHAT MOVED TO F283" paragraph, now at
   `docs/roadmap/features/T2_F277.md`, reads "registered in the same commit that struck them
   from the Acceptance list above". The block orders the registration as C2 (`90976846`) and
   the strike as C3 (`3c3ca820`) — two commits, one round. The prose is wrong about the commit
   boundary and right about everything else; nothing on disk is inconsistent. Flagged for the
   reviewer's disposition, not touched by the worker.
7. No mutation red-proof was run, per constraint 6 — the round's change set holds no
   production code. No disposable worktree was created or removed, for the same reason.
8. **C1a breaches constraint 2 and the AGENTS.md 500-insertion cap at 661 insertions, and is
   declared oversize.** The block's own C1a paragraph both predicts the number ("this block's
   own line count plus 432") and misreads it ("far under 500 either way"); 229 + 432 = 661.
   The inseparability reason and the measured proof that it is the ONLY such commit in F277
   — one of 69 commits from the fork point `f2494c02` — are in the note under the item-status
   table. Recorded there rather than only here because the exception AGENTS.md grants
   requires the declaration to carry its reason before review.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a copy block + 11 payloads | done | 661 insertions, matching the block's formula |
| C1b book PASS, slips, D10, Q2, plan, context | done | 148 insertions measured vs 203 expected; see deviation 1 |
| C2 register F283, ledger-atomically | done | 99 insertions, four paths in one commit |
| C3 strike bullets, write Built State | done | 71 insertions |
| C4 rewrite handoff and push | done | this commit plus the declared C4-fix |
| G1 transport and state (a–e) | done | 33/33 payload readings, 12/12 copies, 4/4 appends + negative control, 2/2 rewrites, open set 20 and 20 |
| G2 registration is ledger-atomic | done | 4 paths exactly; pin 283, README 283 / Tier 2 36, STATUS 46→47 adjacent under one Tier 2 heading |
| G3 docs and state-contract gate | done | `481 passed in 105.33s`, exit 0; see deviation 4 |
| G4 lint and canary | done | ruff `All checks passed!` exit 0; golden path `42 passed` exit 0 |
| G5 whole path set | done | 23 paths, exactly the expected union, 0 under `packages/` or `apps/` |
| G6 push and tree | done | readings recorded by the trailing C4-fix commit; see G6 |
| Constraint 1 no payload edited/retyped | done | every diff via `git apply` after `--check` at exit 0 |
| Constraint 2 every commit under 500 insertions | deviated | C1a measured 661; declared oversize with its reason in the note below |

NOTE ON CONSTRAINT 2 — A DECLARED OVERSIZE COMMIT, and the round's one substantive finding
against its own block. C1a's measured 661 insertions EXCEED the 500-insertion cap DECISION
F104 D1 fixes, so constraint 2 as written was not met and is booked as `deviated` rather
than `done`. Declared under the AGENTS.md Commit Discipline exception, with both of its
conditions addressed:

(a) THE INSEPARABILITY REASON. C1a is the verbatim transport of the reviewer's own twelve
authored artefacts into `.agent/authored/`, ordered by the block as ONE commit. The fidelity
protocol reads that commit as the single provenance record for the round's payloads;
splitting it would leave two partial transport records and break the disk-to-disk comparison
G1(b) performs against it. Nothing in it is product code — it is twelve byte-for-byte copies,
every one proved identical to its source.

(b) IT IS THE ONLY ONE IN THIS FEATURE, MEASURED RATHER THAN ASSERTED. Insertions were summed
per commit with `git log --numstat` over all 69 commits from the fork point `f2494c02` to
HEAD: exactly one exceeds 500, and it is `548d773f` at 661. The next largest is `7c9fdade` at
458 (R1 C1a), then 367, 361, 354 and 346 — all R-series payload copies, all under the cap.

WHERE THE BLOCK WAS WRONG. C1a's paragraph predicts the count correctly as "this block's own
line count plus 432" and then asserts "it is far under 500 either way". 229 + 432 = 661, so
the arithmetic the block supplies contradicts the reassurance it attaches. That is the one
number in this block that did not survive measurement; the payload set was not adjustable by
the worker, and constraint 4 orders a stop only for a RED GATE, which this is not — no gate
of the six covers commit size. The worker therefore executed the block as ordered and
declared the overage here, which is the route AGENTS.md provides.

| Item | Status | Reason |
|---|---|---|
| Constraint 3 no file the block does not name | done | G5: 0 paths under `packages/` or `apps/`, no other test file |
| Constraint 4 stop on a red gate | done | no gate went red; nothing to stop for |
| Constraint 5 `.agent/plan.md` reads 46 lines | done | measured 46 at C1b |
| Constraint 6 no mutation red-proof | done | none ordered, none run; see deviation 7 |

## Next

Phase 1 rule 1 first: read `.agent/STOP` from disk. Then the review of round 12 — C1a, C1b,
C2, C3, C4 and the declared C4-fix, all six gates. Then the closure sequence of
`docs/roadmap/STATUS_closure_protocol.md`, in its order: precondition 6's self-use item
planned and run to the approval gate with its defect strings registered; `integrity check`;
then the integration-gate round running the full suite ONCE in the primary checkout with its
transcript committed as `.agent/authored/f277-closure-suite.txt`.

Open findings count: **20**. Operator-questions count: **2**.
