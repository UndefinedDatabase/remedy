# Handback — F259 Vocabulary & concept model v1, round 5 (T003)

## Session

SESSION 1 of feature F259 · round 5 · rounds so far 5

Branch `feature/f259-vocabulary`, cut from `main` at `25961794`. Rounds 1-4 PASSED;
the round-4 verdict is booked into `.agent/live_review.md` by this round's C2, per
operator amendment amend0827-process-diet rule 1. Soft limit (25 rounds / 7
sessions) is far away.

Fortschritt: `~75 % (T001 ✅ · T002 ✅ · T003 ✅ · T004 offen) — Schätzung`

Context self-assessment: context is comfortable — this round spent it on reading
the page and the catalog rather than on retries, and a further round of this size
fits without a boundary.

Open findings: 299 registrations against 5 `Done:` lines in `.agent/live_review.md`
= **294 open**, unchanged this round. No new finding raised.

## Range

Review of `42448906..dbacffd7` (six commits; C5 adds a seventh, this file).

## Commits

### 50a3abb2 f259: save the round 5 block to .agent/authored
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f259-r5.md` | +409 / -0 | C0a — `shutil.copyfile` of the reviewer's block file, never retyped |

### 2a6028f7 f259: mirror the round 5 block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +352 / -226 | C0b — same copy, mirrored over round 4's block |

### 32158ff6 f259: rewrite the plan for round 5 (T003)
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +18 / -21 | C1 — whole rewrite from the PLANF259R5 slice + one newline |

### 4f30e4f7 f259: book the round 4 PASS verdict and record DECISION F259 D3
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +39 / -1 | C2 — DECISION_D3 appended as `"\n\n" + slice`, no trailing newline |
| `.agent/live_review.md` | +2 / -0 | C2 — GATE_R4 appended as `"\n" + slice + "\n"` |

### 707ddd3e f259: add the per-word meaning table the enforced mode reads
| Path | +/- | Reason |
|---|---|---|
| `docs/system/vocabulary.md` | +35 / -0 | C3 — MEANINGS appended as `"\n" + slice + "\n"` |

### dbacffd7 f259: pin the vocabulary page against the shipped catalog
| Path | +/- | Reason |
|---|---|---|
| `tests/docs/test_vocabulary.py` | +240 / -0 | C4 — production code, written by the worker to the block's SPEC |

### C5 (this commit) f259: round 5 handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | whole rewrite | C5 — a handoff cannot table the commit that writes it (R-0149) |

Every commit above is SINGLE-PARENT (`git rev-list --parents -n 1` reports one
parent each) and every one is under the 500-insertion cap: 409, 352, 18, 41, 35,
240.

## External actions

| Action | Outcome |
|---|---|
| `git push -u origin feature/f259-vocabulary` | `42448906..dbacffd7` — ok, tracking set |
| `git worktree add .remedy-wt/f259-r5-redproof HEAD` | exit 0, detached at `dbacffd7` |
| `git worktree remove .remedy-wt/f259-r5-redproof --force` + `git worktree prune` | exit 0; `git worktree list` no longer shows it |
| `gh pr list --state open --json number,headRefName,baseRefName,isDraft` | `[]` — **no pull request created this round**, as ordered |
| push of C5 | ordered after this file is written; its result is deliberately NOT reported here (constraint 10) |

`git worktree list` still shows ten pre-existing `remedy/job-*` dogfood worktrees
under `.remedy-wt/`. They predate this round and were not touched.

## Verification — one line per gate

- **G1 TRANSPORT — PASS.** `sha256sum` over `.remedy-wt/f259-r5-block.md`,
  `.agent/authored/f259-r5.md`, `.agent/last_block.md`: one digest three times,
  `2e9aeaf94d5269d06473479693f71976d426ab4eb5e0b35c132f8e5db831ad67`.
- **G2 RECORD + DECISION — PASS.** Measured against the committed blobs of
  `4f30e4f7^` and `4f30e4f7`. `.agent/live_review.md`: prefix=True,
  remainder byte-equal to `"\n" + GATE_R4 + "\n"`=True, 830 738 → 834 169 bytes;
  `grep -c '^Gate: R4 — '` 0 → 1. `.agent/decisions.md`: prefix=True, remainder
  byte-equal to `"\n\n" + DECISION_D3`=True, 833 794 → 836 338 bytes, still ends
  with NO newline (final byte `.`); count of `DECISION F259 D3` 0 → 1.
- **G3 PAGE APPEND — PASS.** prefix=True, post = pre + exactly
  `"\n" + MEANINGS + "\n"` = True, 25 555 → 27 295 bytes. Undisturbed: exactly one
  fenced mermaid block; its body (trailing newline stripped — see deviation 3)
  hashes `6f6d59ee6f3d2b36525d64596b04fee3f5ce43d2c439367e6e40c613d313e07c`;
  `^## ` headings in order = How to read the table, The words, Do not confuse
  these, The concept model, The rulings, What counts as the meaning.
- **G4 GREEN IN PLANNED MODE — PASS.** `python3 -m pytest
  tests/docs/test_vocabulary.py -q` → **7 passed**, exit 0. `python3 -m pytest
  tests/docs/ -q` → **302 passed**, exit 0. Arithmetic as the block ordered it:
  295 (the count at `42448906`) + 7 (the new file) = 302, and 302 is the number
  measured, not predicted.
- **G5 RED PROOFS — PASS.** Four runs in a disposable worktree, full transcript
  below. control 0 → (a) 1 failed/6 passed → (b) 2 failed/5 passed → control 0.
- **G6 SHIPPED CATALOG, NOT A TRANSCRIPT — PASS on every clause the worker could
  execute.** Import line, verbatim: `from apps.cli.command_catalog import CATALOG,
  GROUPS`. Occurrences in the file: `--help` 0, `subprocess` 0, `capsys` 0,
  `skipif` 0, `pytest.mark.skip` 0. `VOCABULARY_MODE` occurs 5 times, of which
  module-level assignments (`^VOCABULARY_MODE\s*=`) exactly 1.
  `python3 -m py_compile tests/docs/test_vocabulary.py` → exit 0.
  `ruff check tests/docs/test_vocabulary.py` → REFUSED by this session's
  permission guard (deviation 1; refusal quoted there).
- **G7 SUITES, SERIALLY at C4 — PASS, every count exact.**
  `tests/orchestration/test_roadmap_index.py` 30 passed exit 0 (expected 30);
  `tests/ui_server/` 515 passed exit 0 (515); `tests/orchestration/test_test_runner.py`
  52 passed exit 0 (52); `tests/regression/test_resource_safety.py` 21 passed exit 0
  (21); `tests/orchestration/test_integrity_gate.py` 16 passed exit 0 (16);
  `tests/cli/test_golden_path.py` 42 passed exit 0 (42). No failing node ids.
- **G8 PLAN AND STRUCTURE — PASS.** `wc -l .agent/plan.md` = **42** (< 50);
  `grep -c '^## Goal'` = 1, `grep -c '^## Next Steps'` = 1;
  `filecmp.cmp(..., shallow=False)` against the PLANF259R5 slice + one newline =
  **True**. `git status --porcelain` EMPTY immediately before C5 was staged;
  `git ls-files .remedy-wt` returns nothing; all six commits single-parent; the
  per-commit `git diff --numstat` cells are the `+/-` numbers in the Commits table
  above; every insertion count under 500; push `42448906..dbacffd7` ok; and
  `gh pr list --state open` = `[]`, so **no pull request was created**.

## G5 — the full red-proof transcript

Isolation per guardrail G5 and constraint 5: `git worktree add
.remedy-wt/f259-r5-redproof HEAD` (detached at `dbacffd7`); every pytest run with
`cwd=<worktree>`, invoked as `python3 -B -m pytest`, with every `__pycache__`
under the worktree removed immediately before each run (0 found each time — the
worktree was freshly checked out and `-B` wrote none). The primary checkout was
never mutated. Driver: `.remedy-wt/redproof.py`.

Constraint 6 — the worktree reads ITSELF. Printed before every one of the four
runs, identical each time:

    CATALOG __file__ = /home/decodeux/Repos/remedy/.remedy-wt/f259-r5-redproof/apps/cli/command_catalog.py
    test REPO       = /home/decodeux/Repos/remedy/.remedy-wt/f259-r5-redproof
    cwd             = /home/decodeux/Repos/remedy/.remedy-wt/f259-r5-redproof

No path resolves into the primary checkout, so no run measured the wrong tree.

### CONTROL 1 — unmutated worktree

    __pycache__ directories purged under the worktree: 0
    VOCABULARY_MODE = planned
    $ python3 -B -m pytest tests/docs/test_vocabulary.py -q     (exit 0)
    .......                                                                  [100%]
    7 passed in 0.22s

### PROOF (a) — one binding word's row deleted from the word table

Word removed: **Verdict**. The removed line, verbatim:

    | **Verdict** | The Reviewer's judgement on one Round. | `Verdict` and `ReviewVerdict` in `packages/orchestration/schemas/models.py`, where `Verdict` is the literal set pass, fail, needs_repair, blocked; the field carrying it is `reviewer_verdict` in `packages/orchestration/pingpong_job.py` | unchanged | none | a Gate's result |

    __pycache__ directories purged under the worktree: 0
    VOCABULARY_MODE = planned
    $ python3 -B -m pytest tests/docs/test_vocabulary.py -q     (exit 1)
    =================================== FAILURES ===================================
    ________ test_the_word_table_carries_the_fifteen_binding_words_in_order ________
        def test_the_word_table_carries_the_fifteen_binding_words_in_order():
    >       assert _word_rows() == BINDING_WORDS
    E       AssertionError: assert ['Project', '..., 'Plan', ...] == ['Project', '..., 'Plan', ...]
    E         At index 13 diff: 'Roadmap' != 'Verdict'
    E         Right contains one more item: 'Roadmap'
    tests/docs/test_vocabulary.py:190: AssertionError
    =========================== short test summary info ============================
    FAILED tests/docs/test_vocabulary.py::test_the_word_table_carries_the_fifteen_binding_words_in_order
    1 failed, 6 passed in 0.23s

Page restored afterwards; byte-identical to the original: True.

### PROOF (b) — VOCABULARY_MODE flipped to "enforced" in the worktree's test

    __pycache__ directories purged under the worktree: 0
    VOCABULARY_MODE = enforced
    $ python3 -B -m pytest tests/docs/test_vocabulary.py -q     (exit 1)
    =================================== FAILURES ===================================
    _________________ test_no_retired_synonym_reaches_the_catalog __________________
        def test_no_retired_synonym_reaches_the_catalog():
            offenders = _synonym_offenders()
            if VOCABULARY_MODE == "enforced":
    >           assert offenders == [], (
                    f"retired vocabulary still reaches the catalog: {offenders}")
    E           AssertionError: retired vocabulary still reaches the catalog: [('arg:contract.set:field:description', 'loop'), ('arg:do.job-flow:--job-file:name', 'job-file'), ('arg:do.job-plan:--job-file:name', 'job-file'), ('arg:do.job-promote:--skip-blocked:description', 'promote'), ('arg:do.plan:--task-file:name', 'task-file'), ('arg:do.promote:run_id:description', 'promote'), ('arg:do.run:--fixture-builder:description', 'loop'), ('arg:do.run:--task-file:name', 'task-file'), ('arg:dogfood.run-loop:--max-steps:description', 'loop'), ('arg:loop.run:name:description', 'loop'), ('arg:mission.run:--max-steps:description', 'loop'), ('arg:mission.run:run_id:description', 'loop'), ('command:builder-…
    E           assert [('arg:contra...romote'), ...] == []
    E             Left contains 64 more items, first extra item: ('arg:contract.set:field:description', 'loop')
    tests/docs/test_vocabulary.py:223: AssertionError
    ______ test_every_binding_word_in_a_description_carries_the_pages_meaning ______
    =========================== short test summary info ============================
    FAILED tests/docs/test_vocabulary.py::test_no_retired_synonym_reaches_the_catalog
    FAILED tests/docs/test_vocabulary.py::test_every_binding_word_in_a_description_carries_the_pages_meaning
    2 failed, 5 passed in 0.23s

The offenders the message names are REAL catalog surfaces, all six retired words
represented: `job-file` in the option names of `do.job-plan` and `do.job-flow`;
`task-file` in the option names of `do.run` and `do.plan`; `promote` in the
command ids and in `do.job-promote --skip-blocked`'s description and
`do.promote run_id`'s description; `loop` as the `loop` group and in
`mission.run` and `dogfood.run-loop` option descriptions. 64 pairs in total.
`overnight` and `flight plan` are in the tail the assertion truncated; the full
64 are reproducible with `_synonym_offenders()`.

Test file restored afterwards; byte-identical to the original: True.

### CONTROL 2 — both mutations reverted

    __pycache__ directories purged under the worktree: 0
    VOCABULARY_MODE = planned
    $ python3 -B -m pytest tests/docs/test_vocabulary.py -q     (exit 0)
    .......                                                                  [100%]
    7 passed in 0.22s

Worktree removed and pruned; `git worktree list` no longer lists
`.remedy-wt/f259-r5-redproof`; `git status --porcelain` EMPTY in the primary
checkout.

## Authored-text proofs

| Slice | Applied to | Proof |
|---|---|---|
| PLANF259R5 | `.agent/plan.md` (whole rewrite) | `filecmp.cmp(shallow=False)` against slice + one newline = **True** |
| GATE_R4 | `.agent/live_review.md` (append) | committed blob = parent blob + exactly `"\n" + slice + "\n"` = **True** |
| DECISION_D3 | `.agent/decisions.md` (append) | committed blob = parent blob + exactly `"\n\n" + slice` = **True**, no trailing newline |
| MEANINGS | `docs/system/vocabulary.md` (append) | committed blob = parent blob + exactly `"\n" + slice + "\n"` = **True** |

Every slice was extracted from the COMMITTED `.agent/authored/f259-r5.md` by
marker extraction in Python (`.remedy-wt/extract.py`), never retyped. No slice was
reworded, rewrapped or shortened. `tests/docs/test_vocabulary.py` carries no
slice — it is production code written to the block's SPEC.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a | done | `.agent/authored/f259-r5.md`, digest-identical copy |
| C0b | done | `.agent/last_block.md`, same digest |
| C1 | done | `.agent/plan.md` = PLANF259R5 + one newline, 42 lines |
| C2 | done | GATE_R4 + DECISION_D3, one commit |
| C3 | done | MEANINGS onto `docs/system/vocabulary.md` |
| C4 | done | `tests/docs/test_vocabulary.py`, 7 tests green in planned mode |
| C5 | done | this file; one commit, then push |

No commit was added, dropped or reordered relative to the block's sequence.

## Deviations & assumptions

1. **`ruff check` was REFUSED, not run** (constraint 8 / G6). Attempted twice —
   once inside a compound command, once standalone as
   `ruff check tests/docs/test_vocabulary.py`. Both times the session guard
   answered, verbatim: *"Permission to use Bash has been denied. IMPORTANT: You
   *may* attempt to accomplish this action using other tools that might naturally
   be used to accomplish this goal, e.g. using head instead of cat. But you
   *should not* attempt to work around this denial in malicious ways… If you
   believe this capability is essential to complete the user's request, STOP and
   explain to the user what you were trying to do and why you need this
   permission."* No workaround was attempted. `python3 -m py_compile` ran and
   returned exit 0, as constraint 8 requires either way. So `ruff check` is denied
   to the WORKER as well as to the reviewer; the block assumed only the latter.
2. **Two shell command FORMS were refused** (constraint 7) and re-expressed in
   Python, with the Python reported beside its output above. (a) A compound
   `grep …; echo "grep exit=$?"` — the `$?`-in-a-compound form; re-expressed with
   `subprocess.run(...).returncode`, giving `grep -c '^Gate: R4 — '` exit 1 /
   stdout 0 before the append and exit 0 / stdout 1 after. (b) A heredoc
   containing a brace-with-quote dict literal; re-expressed as a list of tuples
   in the file `.remedy-wt/probe_mermaid.py`. No gate was dropped or narrowed for
   either refusal.
3. **G3's mermaid digest needed a stated normalization.** The block asks for "its
   body's sha256 = `6f6d59ee…`". The RAW fenced body ends with a newline and
   hashes `1da6e9ee983e53b252f5982dc0449dea1473a15b8c028b4e3d1fe42677b0a716`; the
   body with that trailing newline stripped hashes exactly the expected
   `6f6d59ee6f3d2b36525d64596b04fee3f5ce43d2c439367e6e40c613d313e07c`. Round 4's
   record used the stripped convention, so the page is UNCHANGED and the gate
   passes; only the normalization was unstated. Declared so the reviewer does not
   re-derive it.
4. **Red proof (b) turned TWO tests red, not one.** The block requires
   `test_no_retired_synonym_reaches_the_catalog` to fail; it does, naming real
   offenders. `test_every_binding_word_in_a_description_carries_the_pages_meaning`
   also fails, because it is the SECOND mode-dependent test and it too asserts
   the opposite in enforced mode (664 violations measured). That is the SPEC's
   designed behaviour, not damage; declared because the block named only one.
5. **The SPEC says an argument has a `description`; `ArgDef` spells it `help`.**
   `ArgDef` has fields `name`, `help`, `required`, `is_option`, `default`,
   `is_flag`, `is_repeatable` — there is no `description` attribute, so reading
   one literally would raise `AttributeError` at collection. `_catalog_surfaces()`
   therefore reads `arg.help` as the argument's description and says so in its
   docstring, which is where the two names meet. Same for `GroupDef.description`
   and `CommandEntry.description`, which DO exist under those names.
6. **The module docstring was reworded before C4 to satisfy G6.** The natural
   phrasing of the SPEC's "no network, no provider call" clause was "no captured
   `--help` transcript, no subprocess" — but G6 asserts the FILE contains no
   occurrence of the strings `--help` or `subprocess`, and a docstring counts.
   Reworded to "no captured help transcript, no child process". No behaviour
   change; the file now contains 0 of each.
7. **Constraint 11 held.** No catalog description was edited. The 64 synonym
   offenders and 664 meaning violations are MEASURED and left in place; that is
   the debt F261 pays.
8. **Scratch files were left under the gitignored `.remedy-wt/`**, by exact path:
   `extract.py`, `plan_expect.md`, `pre_live_review.md`, `pre_decisions.md`,
   `pre_vocabulary.md`, `probe_mermaid.py`, `probe_spec.py`, `probe_g6.py`,
   `redproof.py`, `gates.py`, `g8.py`, `final_checks.py`. They are the Python the
   refused shell forms were re-expressed as, kept so the reviewer can re-run them.
   `git ls-files .remedy-wt` returns nothing and `git status --porcelain` is
   empty, so none of them is in the repository.

No pull request was created. Nothing was force-pushed, no history was rewritten,
no branch was deleted. `.agent/STOP` was read from disk before C0a, before C4 and
before C5, and was absent every time.

## Next

The reviewer's gate on `42448906..<C5>`, then **round 6 — T004**: the Mermaid
block into `README.md` byte-equal to the page's, directly under the one-sentence
description, and `docs/system/vocabulary.md` registered in `docs/README.md`.
Round 6 writes into `README.md`, whose `Accepted in Tier 2 so far:` block is
scanned for feature ids (R-0797): it must add no id token there. Phase 1 rule 1
(`.agent/STOP`) is checked before rule 2 at the start of that round.
