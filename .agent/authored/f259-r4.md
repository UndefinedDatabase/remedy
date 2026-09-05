STEP T002 / F259 — Vocabulary & concept model v1 — round 4 of session 1
BRANCH feature/f259-vocabulary, head a03d8b6b at the time this block was written.

Goal
  T002. Put the eleven rulings this page is the user-facing home of onto
  `docs/system/vocabulary.md`: DECISION amend0905-vocab D2 through D10, copied
  from `.agent/decisions.md`, and DECISION F259 D1 and D2, copied from
  `docs/roadmap/features/T2_F259.md`. They are EXTRACTED from those two files by
  your own script, never retyped — the only edit any of them receives is the
  demotion of a heading level, so the page nests them under one section. Also
  book the reviewer's PASS verdict on round 3 and one reviewer prose slip, and
  record the T002 measurement of `T2_F263.md`'s heading.

  T2_F263.md needs NO edit. Its T002 obligation reads "updates T2_F263.md's
  header if the H1 still carries a working name", and the reviewer measured that
  H1 at a03d8b6b: it reads `# T2_F263 — Human-change absorption (absorb)`, which
  is already the name DECISION F259 D1 chose. The conditional is false, so the
  file stays out of the change set and gate G5 records the reading that says so.

Bundle, in this order (one commit each)
  C0a save the block file to .agent/authored/f259-r4.md (copy, never retype)
  C0b mirror it to .agent/last_block.md
  C1  .agent/plan.md ← PLANF259R4 (whole rewrite)
  C2  .agent/live_review.md: GATE_R3 appended at end of file;
      .agent/prose_slips.md: SLIP4 appended. One commit — both are this round's
      booking of the round-3 verdict.
  C3  docs/system/vocabulary.md: append RULINGS_INTRO followed by the eleven
      extracted rulings (see "The rulings append" below)
  then push; run the gates
  C4  rewrite .agent/handoff.md; push again.

  Create NO pull request. F259's pull request belongs to its closure round.

Change set — EXACTLY these paths and nothing else
  .agent/authored/f259-r4.md (C0a) — .agent/last_block.md (C0b) —
  .agent/plan.md (C1) — .agent/live_review.md, .agent/prose_slips.md (C2) —
  docs/system/vocabulary.md (C3) — .agent/handoff.md (C4)

Delivery — how this block reaches the repository
  The block is on disk, written by the reviewer, at
      .remedy-wt/f259-r4-block.md
  `.remedy-wt/` is gitignored (`.gitignore` line 235). C0a COPIES that file —
  `shutil.copyfile` or `cp`, never a retype — to .agent/authored/f259-r4.md, and
  C0b copies it to .agent/last_block.md. Every slice you apply is extracted from
  the COMMITTED .agent/authored/f259-r4.md by marker extraction in Python.

The authored slices. Each lies between its own one-line BEGIN and END marker;
the slice is the bytes between the BEGIN marker's newline and the newline before
the END marker, EXCLUDING that final newline. The marker lines themselves are
never applied to any file.

The rulings append (C3)
  Write a script under `.remedy-wt/` (gitignored, never committed) that builds
  the appended text mechanically. It must do exactly this and nothing more.

  A. From `.agent/decisions.md`, take each block that begins with a line matching
     `^## DECISION amend0905-vocab D(2|3|4|5|6|7|8|9|10) ` and runs up to — but
     not including — the next line matching `^#{1,2} `, with trailing newlines
     stripped. There are nine such blocks and they occur in the file in the order
     D2, D3, D4, D5, D6, D7, D8, D9, D10; assert that order rather than assuming
     it, and assert that exactly nine were found.
  B. From `docs/roadmap/features/T2_F259.md`, take each block that begins with a
     line matching `^### DECISION F259 D[12] ` and runs up to — but not
     including — the next line matching `^#{1,3} `, with trailing newlines
     stripped. Assert that exactly two were found, in the order D1, D2.
  C. Demote the FIRST LINE ONLY of each of the nine blocks from A, by replacing
     its leading `## ` with `### `. The two blocks from B are already at `###`
     and are not touched at all. No other byte of any block changes.
  D. Join: RULINGS_INTRO, then the nine demoted blocks in their order, then the
     two F259 blocks in their order, each separated from the next by exactly one
     empty line.
  E. `docs/system/vocabulary.md` ends with a newline (measured by the reviewer at
     a03d8b6b: 14 545 bytes). Append `"\n" + <the joined text> + "\n"`.

  The reviewer measured the eleven blocks at a03d8b6b as 10 023 bytes and 146
  lines in total, before the heading demotion, which adds one byte per demoted
  block. Report your own totals beside those.

The record append (C2)
  `.agent/live_review.md` ends with a newline. Append `"\n" + GATE_R3 + "\n"`.

The prose-slip append (C2)
  `.agent/prose_slips.md` does NOT end with a newline (measured at a03d8b6b:
  77 778 bytes, final byte `.`). Append `"\n\n" + SLIP4` and add NO trailing
  newline.

Constraints
  1. Every slice is applied BYTE FOR BYTE from the committed
     .agent/authored/f259-r4.md by marker extraction in Python. You may not
     improve, rewrap, re-punctuate or shorten a slice, and you may not fix an
     error you find in one: apply it as written and declare the problem in the
     handback's deviations. The reviewer owns this text.
  2. THE ELEVEN RULINGS ARE COPIES AND NOTHING ELSE. You may not reword,
     rewrap, re-punctuate, shorten, summarise, modernise or "fix" any of them,
     including anything in them you believe to be wrong or out of date. The one
     permitted edit is the heading demotion of step C. A ruling is a record of
     what the operator decided on a date; editing it in the copy would make the
     page disagree with the ledger, which is the exact failure this page exists
     to prevent.
  3. Read `.agent/STOP` from disk before C0a, before C3 and before C4. If it
     exists, finish the commit in hand, write the handback saying so, push, and
     stop.
  4. NEWLINE CONVENTIONS: PLANF259R4 replaces `.agent/plan.md` whole and ends
     with exactly one trailing newline; the page and record appends are as
     described above; SLIP4 is ONE line and the appended region ends with NO
     newline.
  5. This session's shell guard refuses some command FORMS outright — shell
     loops, `$(...)` substitution, `$?` in a compound command, a `$` anchor
     inside a `grep -c` pattern, brace-with-quote literals in a heredoc, and a
     non-ASCII character inside a Python bytes literal. Re-express the check in
     Python and report the Python you ran beside its output, with the refusal
     quoted verbatim. No gate is dropped or narrowed because a form was refused.
  6. Commit subjects are `f259: <what>`. No leading-slash token, no absolute
     path. End every commit message with the trailer
     `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.
  7. AGENTS.md binds you in full: the self-review loop before EVERY commit, the
     Commit Gate, the branch never being `main`, `git push -u origin
     feature/f259-vocabulary`. Never `--force`, never a history rewrite, never
     `gh pr merge`, never a branch deletion.
  8. C4 IS ONE COMMIT AND IT DOES NOT REPORT ITS OWN POST-PUSH STATE. No gate
     below asks the handback for a reading that only exists after the handback
     is pushed; the reviewer takes those readings itself at the next gate and
     records them in the next round's ledger entry, which is what
     docs/agents/planner_reviewer_prompt.md §3 item 31 requires. Round 3 spent an
     extra commit because the previous block got this wrong.
  9. Do-not-touch, from T2_F259.md: no command is renamed, no module is moved,
     no data shape changes, no catalog description is edited. `T2_F263.md`,
     `docs/README.md` and `README.md` are all OUTSIDE this round's change set.

Done when — the gates. Real exit codes, real output, one line per gate in the
handback. Every gate runs at or before C3; none is ordered after the commit that
writes the handback.

  G1 TRANSPORT. `sha256sum .remedy-wt/f259-r4-block.md .agent/authored/f259-r4.md .agent/last_block.md`
     — one digest, three times. Report the digest and all three paths.
  G2 THE PAGE APPEND, proved by reconstruction. Report both booleans: the
     pre-append bytes of `docs/system/vocabulary.md` are a byte-exact PREFIX of
     the post-append bytes; and the post-append bytes equal the pre-append bytes
     plus exactly `"\n" + <the joined text your script built> + "\n"`. Report the
     file's byte length before and after, and the byte length of the joined text.
  G3 EVERY RULING ON THE PAGE IS ITS SOURCE, UNEDITED. For each of the eleven,
     extract the block from the PAGE, restore its heading level — for the nine
     amend0905 rulings replace the leading `### ` of the first line with `## `,
     for the two F259 rulings change nothing — and compare the result to the
     block extracted from its source file by sha256. Report one line per ruling:
     its heading, the source digest, the page digest, and whether they are equal.
     All eleven must be equal. Then run a NEGATIVE CONTROL on a copy under
     `.remedy-wt/`: change one word inside one ruling and confirm exactly one of
     the eleven comparisons then reports unequal.
  G4 THE PAGE'S SECTIONS AND THE ORDER OF THE RULINGS. Report, in file order,
     every `^## ` heading of `docs/system/vocabulary.md` and every `^### `
     heading. The `###` list must be, in order, the nine amend0905-vocab rulings
     D2 to D10 followed by DECISION F259 D1 and DECISION F259 D2. Report the
     length your own extraction measured. Confirm also that the page still holds
     exactly one fenced ```mermaid block and that its body's sha256 is still
     6f6d59ee6f3d2b36525d64596b04fee3f5ce43d2c439367e6e40c613d313e07c — this
     round must not disturb it.
  G5 THE T002 CONDITIONAL, MEASURED RATHER THAN ASSUMED. Report the first line of
     `docs/roadmap/features/T2_F263.md` verbatim, and report whether the string
     `absorb` occurs in it. The block asserts the H1 already carries the final
     name and that the file therefore needs no edit; if your reading contradicts
     that, do NOT edit the file — report the contradiction and stop, because the
     change set does not contain it. Confirm `git status --porcelain` names
     `docs/roadmap/features/T2_F263.md` nowhere at any point this round.
  G6 THE RECORD AND THE SLIP APPENDS. For `.agent/live_review.md`: the
     pre-append bytes are a byte-exact PREFIX of the post-append bytes and the
     remainder equals exactly `"\n" + GATE_R3 + "\n"` — report both booleans —
     and `grep -c '^Gate: R3 — ' .agent/live_review.md` goes from 0 to 1. For
     `.agent/prose_slips.md`: the same prefix property, the remainder equal to
     `"\n\n" + SLIP4`, and the file still does not end with a newline. Report the
     byte length of each file before and after.
  G7 THE SUITES, RUN SERIALLY, at C3. Each is a real run; report the passed count
     and exit code for each. The expected counts were re-measured by the reviewer
     at a03d8b6b, this branch's head before this round:
       python3 -m pytest tests/docs/ -q                                 expect 295
       python3 -m pytest tests/orchestration/test_roadmap_index.py -q   expect 30
       python3 -m pytest tests/ui_server/ -q                            expect 515
       python3 -m pytest tests/orchestration/test_test_runner.py -q     expect 52
       python3 -m pytest tests/regression/test_resource_safety.py -q    expect 21
       python3 -m pytest tests/orchestration/test_integrity_gate.py -q  expect 16
       python3 -m pytest tests/cli/test_golden_path.py -q               expect 42
     The four state readers are run as four, not as three. A count that comes
     back different is not rounded off or explained away: report the number and
     the failing node ids verbatim.
  G8 THE PLAN AND THE STRUCTURE. `wc -l .agent/plan.md` under 50; one `## Goal`
     heading and one `## Next Steps` heading (report both counts); the file
     equals the extracted PLANF259R4 slice plus one trailing newline under
     `filecmp.cmp(..., shallow=False)` — report the boolean. Then:
     `git status --porcelain` empty immediately before C4 is staged;
     `git ls-files .remedy-wt` returns nothing (report the line count); every
     commit single-parent; and `git diff --numstat <parent> <commit>` for EACH
     commit C0a through C3, reported cell by cell so the handback's `## Commits`
     table carries the same numbers this gate printed. Report each commit's
     insertion count against the 500 cap, the push result, and confirm no pull
     request was created.

The handback (C4) — rewrite .agent/handoff.md whole
  No length cap. It must carry: the feature, the round and the SESSION NUMBER —
  still SESSION 1 of F259, round 4, rounds so far 4; the commit range; a
  `## Commits` table with one row per commit giving the files and the `+/-`
  numbers G8 printed; the item-status table AGENTS.md requires, one row per
  bundle item C0a through C4; one line per gate G1 through G8 with its real
  reading; the deviations and assumptions; ONE sentence of context
  self-assessment (operator amendment amend0905-throughput); and the next
  expected action, which is the reviewer's gate of this round and then round 5,
  T003 — `tests/docs/test_vocabulary.py` in planned mode with both red proofs.
  Repeat this line verbatim in its state block:
  `~55 % (T001 ✅ · T002 ✅ · T003, T004 offen) — Schätzung`

<<<BEGIN PLANF259R4>>>
# Plan — F259 Vocabulary & concept model v1

Branch: feature/f259-vocabulary, cut from `main` at 25961794. Rounds 1 to 3
PASSED the reviewer's gate; the round-3 verdict is booked in
`.agent/live_review.md` by round 4's own C2, which is where a verdict lands
under operator amendment amend0827-process-diet rule 1.

## Goal

Write `docs/system/vocabulary.md` as the BINDING vocabulary page: the DECISION
amend0905-vocab D1 table — one row per word, with its meaning, its code spelling
today, its code spelling after F260/F261, its CLI spelling and what it is NOT —
plus the do-not-confuse table, the Mermaid concept diagram, and D2–D10 and F259
D1/D2 as dated DECISION paragraphs. Pin the page with
`tests/docs/test_vocabulary.py` in planned mode against the shipped
`apps/cli/command_catalog.py`, put the same Mermaid block into `README.md`, and
register the page in `docs/README.md`. Explicitly no other code: F259 decides
words, F260 and F261 spend them.

## Current Step

Round 4 is T002 — the eleven rulings the page is the user-facing home of are
EXTRACTED from `.agent/decisions.md` and `docs/roadmap/features/T2_F259.md` and
appended to the page, unedited apart from a heading demotion, so the page cannot
disagree with the ledger. `T2_F263.md` needs no edit: its H1 already carries the
final name `absorb`, which the round measures rather than assumes.

## Next Steps

- Write `tests/docs/test_vocabulary.py` in planned mode, with the two red proofs
  T2_F259.md's T003 names: removing a binding word from the page must fail the
  page assertion, and flipping the mode constant to enforced against today's
  catalog must fail the synonym assertion.
- Put the Mermaid block into `README.md`, byte-equal to the page's, and register
  the page in `docs/README.md` (T004).
- Run the integration gate, then the closure sequence.

## Risks

- The Mermaid block will exist in three places once T004 lands; only a
  byte-comparison gate keeps them equal, and every round touching any of the
  three re-runs it.
- `README.md` has a guarded region: its `Accepted in Tier 2 so far:` block is
  scanned for feature ids, and putting an unaccepted id there is what R-0797
  was. The T004 round writes into that file and must add no id token.
<<<END PLANF259R4>>>

<<<BEGIN GATE_R3>>>
Gate: R3 — the F259 R3 entry. R3 COMPLETED T001: THE DO-NOT-CONFUSE TABLE AND THE CONCEPT MODEL. VERDICT PASS. Range e726832e..a03d8b6b, seven commits, all single-parent, pushed, no pull request; largest commit 275 insertions, so no commit approached the AGENTS.md 500-insertion cap. TRANSPORT: one digest `7c12b38cdc9b9f921b3fd768861898e6fdd1664f840e747a40a1fe50a88f74a2` across `.remedy-wt/f259-r3-block.md`, `.agent/authored/f259-r3.md` and `.agent/last_block.md`, equal to the digest the reviewer computed over its own scratch file before emission; per §3 item 37 that is a COPY chain covering scratch, saved copy and mirror, and is not a claim about bytes emitted into a prompt. EVERY EDIT WAS PROVED BY TOTAL RECONSTRUCTION, the form this record's R2 entry made binding after the counting gate that preceded it failed: `.agent/live_review.md` at c6999268 is byte-EQUAL to its parent plus exactly `"\n" + GATE_R2 + "\n"` (823 241 to 827 079 bytes); `.agent/prose_slips.md` is byte-EQUAL to its parent plus exactly `"\n\n" + SLIP3`, still ends with no newline (76 469 to 77 778); `docs/system/vocabulary.md` at 8de6d3e6 is byte-EQUAL to its parent plus exactly `"\n" + PAGE2 + "\n"` (10 608 to 14 545); and `.agent/plan.md` equals its slice plus one newline at 44 lines. Each reconstruction establishes both that the ordered text landed and that nothing else in the target moved, which no count can do. THE DIAGRAM CANNOT DRIFT: the fenced mermaid body of `docs/system/vocabulary.md` and that of `docs/roadmap/features/T2_F259.md` both hash to `6f6d59ee6f3d2b36525d64596b04fee3f5ce43d2c439367e6e40c613d313e07c` at 309 bytes, the reviewer confirmed U+00B7 MIDDLE DOT survived into the landed page, and the worker's negative control replacing it with a hyphen produced a differing digest, so the comparison can fail. THE TABLE: the do-not-confuse rows are, in file order, Job / Run, Plan / Roadmap, Order / Job, Task / Round, Contract / permissions, Mission / schedule, Worker / role, template / order file — exactly the pairs T2_F259.md's Goal & Done names, in that order — and every row splits into the header's cell count. OPEN SET, recomputed mechanically per §3 item 10: 299 registrations against 5 `Done:` lines, 294 open, unchanged by this round. SUITES, re-run by the reviewer serially and all exact: `tests/docs/` 295, `tests/orchestration/test_roadmap_index.py` 30, `tests/ui_server/` 515, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16, `tests/cli/test_golden_path.py` 42. THE ROUND'S ONE DEVIATION IS THE REVIEWER'S DEFECT, NOT THE WORKER'S: the block's G7 ordered `git status --porcelain` read "after the final push" while the same block required one line per gate in the handback, and the handback is written by the commit that is then pushed — the §3 item 31 shape exactly, an artefact ordered to quote a reading that does not exist when it is written. The worker declined to point at absent evidence and spent one follow-up commit, a03d8b6b, carrying the real post-push transcript. THE READING THAT COMMIT COULD NOT HAVE HELD IS TAKEN HERE INSTEAD, which is what item 31 prescribes: the reviewer ran `git status --porcelain` in the primary checkout after a03d8b6b was pushed and it returned EMPTY, `git ls-files .remedy-wt` returns nothing, and `origin/feature/f259-vocabulary` is at a03d8b6b with no pull request open. The reviewer's ordering error is recorded in `.agent/prose_slips.md` by the same commit that appends this entry; it has no product effect under operator amendment amend0827-process-diet rule 2 and no R-id is spent.
<<<END GATE_R3>>>

<<<BEGIN SLIP4>>>
2026-09-05 · F259 R3 (reviewer) · The round-3 block's gate G7 ordered `git status --porcelain` to be read "again after the final push" while the same block required one line per gate in `.agent/handoff.md` — and the handback is written by the commit that the final push then pushes, so the ordered reading cannot exist when the artefact quoting it is authored. This is docs/agents/planner_reviewer_prompt.md §3 item 31, which states the counter-measure the block failed to apply: under self-drive there is no second window, the "round report" channel item 14 offers does not survive the session, and the handback commit's own post-push numbers therefore belong in the REVIEWER's next ledger entry, not in the handback. The worker refused to write a pointer at absent evidence and spent one extra commit carrying the real transcript instead — the honest response to an unmeetable order. THE LESSON: before ordering any reading into the handback, name the commit that produces it and check it is strictly earlier than the commit that writes the handback; a reading about the push belongs to the reviewer. Reviewer-authored ordering slip; nothing on disk under `packages/`, `apps/`, `tests/` or `docs/` is wrong; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIP4>>>

<<<BEGIN RULINGS_INTRO>>>
## The rulings

The words on this page were not derived; they were decided. The eleven rulings
below are the decisions themselves, copied here unedited so that a reader of the
page never has to go looking for the reasoning — each one names its date, the
operator order it came from, and how to reverse it.

They are copies, and the copy is not the original. DECISION amend0905-vocab D2
through D10 live in `.agent/decisions.md`; DECISION F259 D1 and D2 live in
`docs/roadmap/features/T2_F259.md`. Those files are where the rulings were made
and where a reversal is performed — deleting a paragraph here would change
nothing. Because they are verbatim copies of Remedy's own build record, some of
them talk about Remedy's internals — feature ids, finding ids, module paths — in
a way the rest of this page does not; that is the price of not paraphrasing a
decision, and it is worth paying, because a paraphrased ruling is a second
source of truth.
<<<END RULINGS_INTRO>>>
