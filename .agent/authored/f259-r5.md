STEP T003 / F259 — Vocabulary & concept model v1 — round 5 of session 1
BRANCH feature/f259-vocabulary, head 42448906 at the time this block was written.

Goal
  T003. Ship `tests/docs/test_vocabulary.py` in PLANNED mode, written by you to
  the SPEC below — it is production code and no slice is shipped for it — with
  both of the red proofs T2_F259.md's T003 names, run inside a disposable git
  worktree. Add to the page the per-word meaning table the enforced mode reads.
  Record DECISION F259 D3, which settles a gap the feature file's own synonym
  list leaves open. Book the reviewer's PASS verdict on round 4.

Why DECISION F259 D3 exists (docs/agents/planner_reviewer_prompt.md §4 item 7)
  T2_F259.md names seven retired synonyms for the enforced mode to assert absent
  and scopes that mode to the catalog. The reviewer measured all seven against
  the shipped catalog at 42448906 by importing it. Six are reachable there:
  `promote` in three descriptions (`group:do`, `do.promote`, `do.job-flow`) and
  in two command ids; `flight plan` in the description of `do.replan`;
  `overnight` in six descriptions and as a group id; `loop` as a group id;
  `job-file` in two option names (`do.job-plan`, `do.job-flow`); `task-file` in
  two option names (`do.run`, `do.plan`). The seventh, `Worker:` as a role
  label, occurs NOWHERE in the catalog — it lives in report and render code, 78
  occurrences under `packages/` and `apps/`, among them
  `packages/orchestration/pingpong_evidence.py` and
  `apps/cli/commands/do_cmd.py`. A catalog-scoped assertion that `Worker:` is
  absent would therefore pass for every possible repository: it is the
  vacuous-gate shape this record calls R-0438, and shipping it would be worse
  than shipping nothing, because it reads on the page like a guard. The
  DECISION names the scope, names `Worker:` as out of it WITH the reason, and
  routes that check to F261, which owns the renames and touches those
  renderers. The operator's veto is any later relay; nothing waits for an answer.

Bundle, in this order (one commit each)
  C0a save the block file to .agent/authored/f259-r5.md (copy, never retype)
  C0b mirror it to .agent/last_block.md
  C1  .agent/plan.md ← PLANF259R5 (whole rewrite)
  C2  .agent/live_review.md: GATE_R4 appended at end of file;
      .agent/decisions.md: DECISION_D3 appended. One commit.
  C3  docs/system/vocabulary.md: append MEANINGS (see "The page append" below)
  C4  tests/docs/test_vocabulary.py (new) — written by you to the SPEC
  then push; run the gates, including the red proofs
  C5  rewrite .agent/handoff.md; push again.

  Create NO pull request. F259's pull request belongs to its closure round.

Change set — EXACTLY these paths and nothing else
  .agent/authored/f259-r5.md (C0a) — .agent/last_block.md (C0b) —
  .agent/plan.md (C1) — .agent/live_review.md, .agent/decisions.md (C2) —
  docs/system/vocabulary.md (C3) — tests/docs/test_vocabulary.py (C4) —
  .agent/handoff.md (C5)

Delivery — how this block reaches the repository
  The block is on disk, written by the reviewer, at
      .remedy-wt/f259-r5-block.md
  `.remedy-wt/` is gitignored (`.gitignore` line 235). C0a COPIES that file to
  .agent/authored/f259-r5.md and C0b copies it to .agent/last_block.md. Every
  slice is extracted from the COMMITTED .agent/authored/f259-r5.md by marker
  extraction in Python.

The authored slices lie between one-line BEGIN and END markers; the slice is the
bytes between the BEGIN marker's newline and the newline before the END marker,
EXCLUDING that final newline. The marker lines are never applied to any file.

The page append (C3)
  `docs/system/vocabulary.md` ends with a newline (measured by the reviewer at
  42448906: 25 555 bytes). Append `"\n" + MEANINGS + "\n"`.

The record append (C2)
  `.agent/live_review.md` ends with a newline. Append `"\n" + GATE_R4 + "\n"`.

The decisions append (C2)
  `.agent/decisions.md` does NOT end with a newline (measured at 42448906:
  833 794 bytes, final byte `.`). Append `"\n\n" + DECISION_D3` and add NO
  trailing newline — that is this file's existing convention between entries.

Constraints
  1. Every slice is applied BYTE FOR BYTE from the committed
     .agent/authored/f259-r5.md by marker extraction in Python. You may not
     improve, rewrap, re-punctuate or shorten a slice, and you may not fix an
     error you find in one: apply it verbatim and declare the problem in the
     handback's deviations.
  2. `tests/docs/test_vocabulary.py` IS PRODUCTION CODE AND IS YOURS TO WRITE.
     No slice is shipped for it. Write it to the SPEC below in the idiom of
     `tests/docs/test_docs_consistency.py`, which sits beside it — same import
     style, same `REPO = Path(__file__).resolve().parents[2]` root resolution,
     same plain-assert style. Match that file's conventions rather than
     inventing new ones.
  3. Read `.agent/STOP` from disk before C0a, before C4 and before C5.
  4. NEWLINE CONVENTIONS: PLANF259R5 replaces `.agent/plan.md` whole with
     exactly one trailing newline; the page and record appends are as described
     above; the DECISION_D3 append ends with NO newline;
     `tests/docs/test_vocabulary.py` ends with exactly one trailing newline.
  5. DESTRUCTIVE VERIFICATION IS ISOLATED. Both red proofs run ONLY inside a
     disposable `git worktree` created from this branch's head, never in the
     primary checkout, which must satisfy `git status --porcelain` empty at
     every commit and at the end. Remove the worktree and prune it when done and
     show `git worktree list` afterwards. Before each proof run, delete any
     `__pycache__` under the worktree and invoke pytest as `python3 -B -m pytest`
     so a stale bytecode cache cannot mask a mutation.
  6. THE WORKTREE MUST BE PROVED TO BE READING ITSELF. In every proof run, have
     the run also print `apps.cli.command_catalog.__file__` and
     `tests/docs/test_vocabulary.py`'s resolved `REPO`, and report both: a
     worktree that imports the PRIMARY checkout's modules is measuring the wrong
     tree, and that failure is silent. Run pytest with the worktree as the
     working directory (`subprocess.run(..., cwd=<worktree>)`).
  7. This session's shell guard refuses some command FORMS outright — shell
     loops, `$(...)` substitution, `$?` in a compound command, a `$` anchor
     inside a `grep -c` pattern, brace-with-quote literals in a heredoc, a
     non-ASCII character in a Python bytes literal, and `${PIPESTATUS[0]}`.
     Re-express in Python and report the Python you ran beside its output, with
     any refusal quoted verbatim. No gate is dropped or narrowed for a refused
     form.
  8. `ruff check tests/docs/test_vocabulary.py` is DENIED to the reviewer. You
     attempt it and report either its exact output or the exact refusal;
     `python3 -m py_compile tests/docs/test_vocabulary.py` is run either way.
  9. Commit subjects are `f259: <what>`. No leading-slash token, no absolute
     path. End every commit message with the trailer
     `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.
 10. AGENTS.md binds you in full. Never `--force`, never a history rewrite,
     never `gh pr merge`, never a branch deletion. C5 is ONE commit and reports
     no reading that only exists after it is pushed.
 11. Do-not-touch: no command is renamed, no module is moved, no data shape
     changes, NO CATALOG DESCRIPTION IS EDITED. The test measures the catalog;
     it never repairs it. `README.md` and `docs/README.md` are round 6's.

SPEC — tests/docs/test_vocabulary.py (production code, written by you)

  Purpose: pin `docs/system/vocabulary.md` against the SHIPPED command catalog,
  in a mode F261 flips from planned to enforced.

  Module level:
  - A module docstring saying what the file pins and that it reads only
    checked-in files and the imported catalog — no network, no provider call.
  - `VOCABULARY_MODE = "planned"` — a plain module constant with a comment
    naming F261 as the feature that flips it to `"enforced"`. It is NEVER a
    skip marker and no test in this file is decorated with `skipif`.
  - `REPO = Path(__file__).resolve().parents[2]`, `PAGE = REPO / "docs" /
    "system" / "vocabulary.md"`, and the feature file path for the diagram
    comparison.
  - `BINDING_WORDS` — the fifteen words, in DECISION amend0905-vocab D1's order:
    Project, Order, Mission, Contract, Job, Plan, Task, Run, Round, Worker,
    Decision, Evidence, Gate, Verdict, Roadmap.
  - `RETIRED_SYNONYMS` — the six the reviewer measured as reachable in the
    catalog: `promote`, `flight plan`, `job-file`, `task-file`, `loop`,
    `overnight`. A comment beside it names `Worker:` as deliberately EXCLUDED
    and cites DECISION F259 D3 for the reason, so the next reader does not
    "restore" a clause that cannot fail.
  - The catalog is reached by `from apps.cli.command_catalog import CATALOG,
    GROUPS` at module import. Never by running a command, never from a captured
    `--help` transcript.

  Helpers, small and named:
  - `_page()` returns the page text.
  - `_word_rows()` returns the first cell of every row of the page's word table,
    in file order, bold markers stripped.
  - `_confusion_rows()` returns the first cell of every row of the
    do-not-confuse table, in file order.
  - `_meaning_fragments()` parses the page's `## What counts as the meaning`
    table into a mapping word -> list of fragments, taking the fragments from
    the backticked spans of the second cell.
  - `_mermaid_body(text)` returns the body of the single fenced mermaid block.
  - `_catalog_surfaces()` yields `(where, text)` pairs covering the whole
    catalog surface a description can hide in: for every group, its `id`,
    `label` and `description`; for every catalog entry, its `command_id` and
    `description`, and for each of its args the arg's `name` and `description`.
    This is the scope DECISION F259 D3 fixes, and the helper is where that scope
    lives so it is stated once.
  - `_synonym_offenders()` returns the sorted list of `(where, synonym)` pairs
    for every surface whose text contains a retired synonym, case-insensitively.

  Tests that hold in BOTH modes (they read the page):
  1. the word table's first cells equal `BINDING_WORDS`, in order;
  2. the do-not-confuse table carries exactly the eight pairs, in the order
     `Job / Run`, `Plan / Roadmap`, `Order / Job`, `Task / Round`,
     `Contract / permissions`, `Mission / schedule`, `Worker / role`,
     `template / order file`;
  3. the page holds exactly one fenced mermaid block and its body is BYTE-EQUAL
     to the body of the single fenced mermaid block in
     `docs/roadmap/features/T2_F259.md`;
  4. the page carries a `### DECISION` heading for each of amend0905-vocab D2
     through D10 and for F259 D1 and D2, in that order;
  5. `_meaning_fragments()` has a non-empty fragment list for every word in
     `BINDING_WORDS`, and no word outside it.

  The two mode-dependent tests. NEITHER is skipped in planned mode: each runs in
  both modes and asserts the OPPOSITE thing, so the planned mode is a live
  measurement of the debt rather than a switched-off test, and the test turns
  red by itself on the day F261 finishes the renames and forgets to flip the
  constant.
  6. `test_no_retired_synonym_reaches_the_catalog` — compute
     `_synonym_offenders()`. In `"enforced"` mode assert it is EMPTY, naming the
     offenders in the assertion message. In `"planned"` mode assert it is
     NON-EMPTY, with a message saying that an empty set means the renames have
     landed and `VOCABULARY_MODE` should now be `"enforced"`.
  7. `test_every_binding_word_in_a_description_carries_the_pages_meaning` — for
     each surface that is a DESCRIPTION (not an id, not a label, not an arg
     name) and each binding word occurring in it as a whole word,
     case-insensitively, the description must also contain at least one of that
     word's fragments, case-insensitively; collect the violations. In
     `"enforced"` mode assert there are none; in `"planned"` mode assert there
     is at least one, with the same "flip the constant" message.

  Nothing in this file writes, and nothing in it edits the catalog.

Done when — the gates. Real exit codes, real output, one line per gate in the
handback. Every gate runs at or before C4; none is ordered after the commit that
writes the handback.

  G1 TRANSPORT. `sha256sum .remedy-wt/f259-r5-block.md .agent/authored/f259-r5.md .agent/last_block.md`
     — one digest, three times. Report it and all three paths.
  G2 THE RECORD AND THE DECISION. For `.agent/live_review.md`: the pre-append
     bytes are a byte-exact PREFIX of the post-append bytes and the remainder
     equals exactly `"\n" + GATE_R4 + "\n"` — report both booleans — and
     `grep -c '^Gate: R4 — ' .agent/live_review.md` goes from 0 to 1. For
     `.agent/decisions.md`: the same prefix property, the remainder equal to
     `"\n\n" + DECISION_D3`, the file still ending with no newline, and the count
     of the string `DECISION F259 D3` going from 0 to 1. Report byte lengths
     before and after for both.
  G3 THE PAGE APPEND. Report both booleans: prefix property; and post equals pre
     plus exactly `"\n" + MEANINGS + "\n"`. Report byte length before and after.
     Then confirm this round did NOT disturb what earlier rounds landed: the page
     still holds exactly one fenced mermaid block whose body's sha256 is
     6f6d59ee6f3d2b36525d64596b04fee3f5ce43d2c439367e6e40c613d313e07c, and its
     `^## ` headings are, in order, How to read the table, The words, Do not
     confuse these, The concept model, The rulings, What counts as the meaning.
  G4 THE TEST IS GREEN IN PLANNED MODE, AND THE WHOLE DOCS SUITE WITH IT.
     `python3 -m pytest tests/docs/test_vocabulary.py -q` — report the passed
     count and exit code. `python3 -m pytest tests/docs/ -q` — report the passed
     count and exit code; it was 295 at 42448906, so the new number is 295 plus
     the count the first command reported, and you state that arithmetic
     explicitly rather than a number this block guesses.
  G5 THE TWO RED PROOFS, IN A DISPOSABLE WORKTREE, EACH WITH AN UNMUTATED
     CONTROL. Constraints 5 and 6 govern how. Report, for each of the four runs,
     the exit code, the passed/failed counts and the failing node ids:
       (control) unmutated worktree, `python3 -B -m pytest tests/docs/test_vocabulary.py -q`
                 — must be exit 0. A colour with no baseline is not evidence.
       (a) delete ONE binding word's row from the worktree's
           `docs/system/vocabulary.md` word table — name which word and quote the
           removed line — and re-run: the word-table test must FAIL.
       (b) restore, then set `VOCABULARY_MODE = "enforced"` in the worktree's
           test file and re-run: `test_no_retired_synonym_reaches_the_catalog`
           must FAIL, and its message must name a real offender. Quote the
           offenders it names.
       (control again) restore both, re-run, exit 0.
     Report `apps.cli.command_catalog.__file__` and the resolved `REPO` from
     inside the worktree runs, per constraint 6. Finish with `git worktree list`
     showing the scratch worktree gone, and `git status --porcelain` empty in the
     primary checkout.
  G6 THE TEST READS THE SHIPPED CATALOG, NOT A TRANSCRIPT. Report: the file
     imports `CATALOG` and `GROUPS` from `apps.cli.command_catalog` (quote the
     import line); the file contains no occurrence of the strings `--help`,
     `subprocess` or `capsys`; `VOCABULARY_MODE` occurs as a module-level
     assignment exactly once and the file contains no `skipif` and no
     `pytest.mark.skip`. Then `python3 -m py_compile tests/docs/test_vocabulary.py`
     (report exit code) and the `ruff check` attempt of constraint 8.
  G7 THE SUITES, RUN SERIALLY, at C4. Report the passed count and exit code for
     each. Expected counts re-measured by the reviewer at 42448906:
       python3 -m pytest tests/orchestration/test_roadmap_index.py -q   expect 30
       python3 -m pytest tests/ui_server/ -q                            expect 515
       python3 -m pytest tests/orchestration/test_test_runner.py -q     expect 52
       python3 -m pytest tests/regression/test_resource_safety.py -q    expect 21
       python3 -m pytest tests/orchestration/test_integrity_gate.py -q  expect 16
       python3 -m pytest tests/cli/test_golden_path.py -q               expect 42
     `tests/docs/` is covered by G4 and is not repeated here. The four state
     readers are run as four. A different count is reported as the number it is,
     with failing node ids verbatim.
  G8 THE PLAN AND THE STRUCTURE. `wc -l .agent/plan.md` under 50; one `## Goal`
     and one `## Next Steps` (report both counts); `filecmp.cmp(..., shallow=False)`
     True against the slice plus one newline. Then `git status --porcelain` empty
     immediately before C5 is staged; `git ls-files .remedy-wt` returns nothing;
     every commit single-parent; `git diff --numstat <parent> <commit>` for EACH
     commit C0a through C4 reported cell by cell, so the handback's `## Commits`
     table carries the same numbers; each commit's insertion count against the
     500 cap; the push result; and confirmation that no pull request was created.

The handback (C5) — rewrite .agent/handoff.md whole
  No length cap. Carry: feature, round, SESSION NUMBER — still SESSION 1 of
  F259, round 5, rounds so far 5; the commit range; a `## Commits` table with the
  `+/-` numbers G8 printed; the AGENTS.md item-status table, one row per bundle
  item C0a through C5; one line per gate G1 through G8 with its real reading; the
  full red-proof transcript of G5; the deviations; ONE sentence of context
  self-assessment; and the next expected action — the reviewer's gate, then round
  6, T004. Repeat this line verbatim in its state block:
  `~75 % (T001 ✅ · T002 ✅ · T003 ✅ · T004 offen) — Schätzung`

<<<BEGIN PLANF259R5>>>
# Plan — F259 Vocabulary & concept model v1

Branch: feature/f259-vocabulary, cut from `main` at 25961794. Rounds 1 to 4
PASSED the reviewer's gate; the round-4 verdict is booked in
`.agent/live_review.md` by round 5's own C2, which is where a verdict lands
under operator amendment amend0827-process-diet rule 1.

## Goal

Write `docs/system/vocabulary.md` as the BINDING vocabulary page: the DECISION
amend0905-vocab D1 table, the do-not-confuse table, the Mermaid concept diagram,
and D2–D10 and F259 D1/D2 as dated DECISION paragraphs. Pin the page with
`tests/docs/test_vocabulary.py` in planned mode against the shipped
`apps/cli/command_catalog.py`, put the same Mermaid block into `README.md`, and
register the page in `docs/README.md`. Explicitly no other code: F259 decides
words, F260 and F261 spend them.

## Current Step

Round 5 is T003 — `tests/docs/test_vocabulary.py` in planned mode, written to
spec against the imported catalog, with both red proofs run inside a disposable
worktree; the page gains the per-word meaning table the enforced mode reads; and
DECISION F259 D3 records why the enforced synonym scan omits `Worker:`, which is
not a catalog token and whose absence there no repository could ever violate.

## Next Steps

- Put the Mermaid block into `README.md`, byte-equal to the page's, and register
  the page in `docs/README.md` (T004).
- Run the integration gate per docs/agents/integration_gate.md.
- Run the closure sequence per docs/roadmap/STATUS_closure_protocol.md.

## Risks

- The Mermaid block exists in two places and T004 makes it three; only the
  byte-comparison test keeps them equal.
- `README.md` has a guarded region: its `Accepted in Tier 2 so far:` block is
  scanned for feature ids, and putting an unaccepted id there is what R-0797
  was. The T004 round writes into that file and must add no id token; its gates
  read the guarded block's tokens, not only the pin's direction.
- The enforced mode is written but not switched on. If F261 lands the renames
  and forgets the constant, test 6 turns red by itself — that is deliberate.
<<<END PLANF259R5>>>

<<<BEGIN GATE_R4>>>
Gate: R4 — the F259 R4 entry. R4 WAS T002: THE ELEVEN RULINGS ONTO THE PAGE. VERDICT PASS. Range a03d8b6b..42448906, six commits, all single-parent, pushed, no pull request; largest commit 283 insertions. Constraint 8 of the R4 block held and C4 was ONE commit, where R3 had needed two — the §3 item 31 defect that block introduced did not recur. TRANSPORT: one digest `7b58ea8e5d5d8990dc545a1f949ec05aba23d90887d8868f1c95ab9724ec2aa5` across `.remedy-wt/f259-r4-block.md`, `.agent/authored/f259-r4.md` and `.agent/last_block.md`, equal to the digest the reviewer computed over its own scratch file before emission; per §3 item 37 that is a COPY chain covering scratch, saved copy and mirror. THE REVIEWER DID NOT TRUST THE WORKER'S EXTRACTION SCRIPT: it re-implemented the block's steps A through E independently — grabbing the nine `## DECISION amend0905-vocab D2..D10` blocks from `.agent/decisions.md` and the two `### DECISION F259 D1..D2` blocks from `docs/roadmap/features/T2_F259.md`, each running to the next heading of level at most its own, demoting only the first line of the nine — and the page committed at 36eaa893 is byte-EQUAL to its parent plus exactly `"\n" + that independently rebuilt text + "\n"` (14 545 to 25 555 bytes). Every one of the ELEVEN rulings on the page, with its heading level restored, hashes identically to the block extracted from its source file, so nothing was reworded, rewrapped or tidied in the copy; the worker's own negative control altering one word inside D6's body reported exactly one unequal, so the comparison can fail. `.agent/live_review.md` and `.agent/decisions.md`'s neighbour `.agent/prose_slips.md` were likewise proved by total reconstruction: the record equals its parent plus exactly `"\n" + GATE_R3 + "\n"` (827 079 to 830 738) and the slip file equals its parent plus exactly `"\n\n" + SLIP4`, still ending with no newline (77 778 to 79 043). `.agent/plan.md` equals its slice plus one newline at 45 lines. THE EARLIER ROUNDS' WORK WAS NOT DISTURBED: the page's `^## ` headings are How to read the table, The words, Do not confuse these, The concept model, The rulings, and its single fenced mermaid body still hashes `6f6d59ee6f3d2b36525d64596b04fee3f5ce43d2c439367e6e40c613d313e07c`. THE T002 CONDITIONAL WAS MEASURED, NOT ASSUMED: `docs/roadmap/features/T2_F263.md`'s first line reads `# T2_F263 — Human-change absorption (absorb)`, already the name DECISION F259 D1 chose, so the conditional "update the header if the H1 still carries a working name" is FALSE, the file is untouched, and `git diff --name-only a03d8b6b..42448906` names it nowhere. OPEN SET, recomputed mechanically per §3 item 10: 299 registrations against 5 `Done:` lines, 294 open, unchanged. SUITES, re-run by the reviewer serially and all exact: `tests/docs/` 295, `tests/orchestration/test_roadmap_index.py` 30, `tests/ui_server/` 515, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16, `tests/cli/test_golden_path.py` 42. THE POST-PUSH READINGS THE HANDBACK CORRECTLY DOES NOT CARRY, taken here per §3 item 31: after 42448906 was pushed the reviewer found `git status --porcelain` EMPTY in the primary checkout, `git ls-files .remedy-wt` empty, `origin/feature/f259-vocabulary` at 42448906, and `gh pr list --state open` returning `[]`. No finding; no reviewer prose slip this round.
<<<END GATE_R4>>>

<<<BEGIN DECISION_D3>>>
## DECISION F259 D3 (2026-09-05, reviewer, docs/agents/planner_reviewer_prompt.md §4 item 7) — the enforced synonym scan is scoped to the catalog, and `Worker:` is named out of it

T2_F259.md lists seven retired synonyms for the vocabulary test's enforced mode
to assert absent — `promote`, `flight plan`, `job-file`, `task-file`, `loop` as
a group, `overnight`, and `Worker:` as a role label — and scopes that mode to
`apps/cli/command_catalog.py`. Measured at 42448906 by importing the catalog,
six of the seven are reachable there: `promote` in the descriptions of the `do`
group, `do.promote` and `do.job-flow` and in the command ids `do.promote` and
`do.job-promote`; `flight plan` in the description of `do.replan`; `overnight`
in six descriptions and as a group id; `loop` as a group id; `job-file` in the
option names of `do.job-plan` and `do.job-flow`; `task-file` in the option names
of `do.run` and `do.plan`.

`Worker:` is not there at all. It occurs 78 times under `packages/` and `apps/`
— in report and render code such as `packages/orchestration/pingpong_evidence.py`
and `apps/cli/commands/do_cmd.py` — and zero times anywhere in the catalog. An
assertion that the catalog does not contain `Worker:` would therefore hold for
every possible state of this repository: it would forbid nothing while reading
on the page exactly like a guard, which is the vacuous-gate failure recorded as
R-0438.

CHOSEN: the enforced mode scans the whole catalog surface — every group's `id`,
`label` and `description`, and every command's `command_id`, `description` and
each of its arguments' `name` and `description` — for the SIX synonyms that live
there, and `tests/docs/test_vocabulary.py` names `Worker:` in a comment as
deliberately excluded, citing this decision, so no later reader restores a
clause that cannot fail. The role-label check belongs to F261, which owns the
renames and edits those renderers; its own round asserts that the report prints
the ROLE, per DECISION amend0905-vocab D1.

ALTERNATIVES CONSIDERED: (a) widen the vocabulary test to scan `packages/` and
`apps/` for `Worker:` — rejected, because F259 explicitly ships no check over
production code and the string occurs in HTML and JavaScript fragments where an
absence rule needs a parser, not a grep; (b) ship the clause anyway and note the
vacuity in prose — rejected, because a passing gate that forbids nothing is the
exact failure this project keeps paying for. Reverse by deleting this paragraph
and adding `Worker:` to `RETIRED_SYNONYMS`.
<<<END DECISION_D3>>>

<<<BEGIN MEANINGS>>>
## What counts as the meaning

The enforced mode of `tests/docs/test_vocabulary.py` has to decide, mechanically,
whether a command description uses a word in the sense this page gives it. It
cannot read English, so this table gives it something it can check: per word, the
fragments that mark the page's meaning. A description that uses a binding word
must also contain at least one of that word's fragments.

This is a floor, not a definition — it catches a description that uses a word
while saying nothing that fits its meaning. The definitions are in the table
above; these are the handles a test can grip.

| Word | Fragments that count as its meaning |
|---|---|
| **Project** | `repo`, `mission` |
| **Order** | `order file`, `what you ask`, `text or` |
| **Mission** | `order`, `job`, `contract` |
| **Contract** | `acceptance`, `definition of done`, `criteria` |
| **Job** | `mission`, `budget`, `fence`, `task` |
| **Plan** | `task`, `milestone`, `step` |
| **Task** | `job plan`, `step`, `run` |
| **Run** | `task`, `evidence` |
| **Round** | `build`, `review`, `repair` |
| **Worker** | `role`, `builder`, `reviewer`, `planner`, `teacher`, `model` |
| **Decision** | `answer`, `question`, `resolve`, `blocker` |
| **Evidence** | `run`, `folder`, `bundle`, `proof` |
| **Gate** | `check`, `pass`, `block` |
| **Verdict** | `review`, `round` |
| **Roadmap** | `build plan`, `docs/roadmap`, `remedy's own` |

Until F261 rewrites the descriptions, this check runs in planned mode, where it
asserts the OPPOSITE — that violations still exist. That is deliberate: a test
switched off records nothing, while a test that measures the debt turns red by
itself on the day the debt is paid and the mode constant has not been flipped.
<<<END MEANINGS>>>
