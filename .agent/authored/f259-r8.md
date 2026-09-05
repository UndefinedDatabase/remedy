STEP CLOSURE PART 1 / F259 — Vocabulary & concept model v1 — round 8 of session 1
BRANCH feature/f259-vocabulary, head e10cbc30 at the time this block was written.

Goal
  The content half of the closure sequence, so that part 2 can build the review
  zip from a clean tree with every content commit already in. Four pieces of
  work, none of them bookkeeping:
  (1) the feature file gains its Built State section and loses its
      REGISTRATION-ONLY banner (closure precondition 4);
  (2) the §3 pre-emission checklist gets its ONE consolidation pass, which
      operator amendment amend0827-process-diet rule 4 mandates exactly once per
      feature and only inside the closure sequence;
  (3) the self-use track's next item is generated and RUN (closure precondition
      6), and every defect its own reader reports is captured;
  (4) the round-7 integration-gate verdict and one reviewer prose slip are booked.

  The STATUS flip, the README sync, the ledger rotation, the evidence job, the
  review zip and the pull request are all part 2. Nothing here touches
  `docs/roadmap/STATUS.md` or `README.md`.

Bundle, in this order (one commit each)
  C0a save the block file to .agent/authored/f259-r8.md (copy, never retype)
  C0b mirror it to .agent/last_block.md
  C1  .agent/plan.md ← PLANF259R8 (whole rewrite)
  C2  .agent/live_review.md: GATE_R7 appended; .agent/prose_slips.md: SLIP8
      appended. One commit.
  C3  docs/roadmap/features/T2_F259.md: apply the REGBANNER pair, then append
      BUILTSTATE (see "The feature file" below)
  C4  docs/agents/planner_reviewer_prompt.md: the consolidation (see "The
      consolidation pass" below)
  C5  the self-use item: generate, run, and record (see "The self-use item")
  then push; run the gates
  C6  rewrite .agent/handoff.md; push again.

  Create NO pull request. It belongs to part 2.

Change set — EXACTLY these paths and nothing else
  .agent/authored/f259-r8.md (C0a) — .agent/last_block.md (C0b) —
  .agent/plan.md (C1) — .agent/live_review.md, .agent/prose_slips.md (C2) —
  docs/roadmap/features/T2_F259.md (C3) —
  docs/agents/planner_reviewer_prompt.md (C4) —
  scripts/self_use_queue.json, .agent/selfuse_f259/** (C5) —
  .agent/handoff.md (C6)

Delivery
  The block is at `.remedy-wt/f259-r8-block.md`, gitignored scratch. C0a COPIES
  it to .agent/authored/f259-r8.md, C0b to .agent/last_block.md. Slices are
  extracted from the COMMITTED authored file by marker extraction in Python.

The record append (C2)
  `.agent/live_review.md` ends with a newline. Append `"\n" + GATE_R7 + "\n"`.
  `.agent/prose_slips.md` does NOT end with a newline. Append `"\n\n" + SLIP8`
  and add NO trailing newline.

The feature file (C3)
  Two edits to `docs/roadmap/features/T2_F259.md`, in this order.
  (a) The REGBANNER pair, applied with `str.replace(FROM, TO, 1)` after
      confirming FROM occurs EXACTLY ONCE. The reviewer ran the containment test
      on it before emission and it printed `TO contains FROM: false`, so it is a
      REWRITE and the obligation is FROM 0x and TO 1x afterwards.
  (b) The file ends with a newline. Append `"\n" + BUILTSTATE + "\n"`.

The consolidation pass (C4)
  Operator amendment amend0827-process-diet rule 4 freezes the §3 checklist while
  a feature is open and mandates ONE consolidation inside the closure sequence,
  from which the list must emerge the SAME LENGTH OR SHORTER. Merging two items
  into one is the intended move; growing the list is forbidden. The reviewer
  measured the list at e10cbc30: 37 items, numbered 1 to 37 with no gaps, which
  is the figure the frozen paragraph names.

  THE MERGE: item 32 into item 16. They are one rule — a numeral a block states
  about its OWN parts is hand-counted, drifts the moment the block is edited, and
  is the half nobody re-reads. Item 32's own text says so: "Items 11 and 16 are
  the same family". Item 32 was chosen because it is referenced BY NUMBER nowhere
  in the governing documents — the reviewer counted references to every item
  number across `docs/agents/planner_reviewer_prompt.md`,
  `docs/agents/self_drive_protocol.md`, `AGENTS.md`,
  `docs/roadmap/STATUS_closure_protocol.md`, `docs/agents/integration_gate.md`,
  `docs/agents/split_workflow.md` and `docs/agents/handback_template.md`, and item
  32 has zero.

  THE SURVIVORS ARE NOT RENUMBERED. Item 32's number is RETIRED. `.agent/live_review.md`
  is append-only and cross-references these items by number from dated entries
  that cannot be corrected; renumbering would silently re-point every one of them
  at a different rule. The list therefore runs 1 to 31 and 33 to 37 — 36 items,
  shorter than 37, with one retired number and every existing cross-reference
  still resolving to the rule it was written about.

  Three edits, in this order:
  (a) ITEM16 pair — append the merged paragraph to item 16. The FROM is item 16's
      last line, which the reviewer confirmed occurs EXACTLY ONCE in the file, and
      the containment test printed `TO contains FROM: true`, so it is an APPEND
      and the obligation is FROM exactly 1x afterwards plus each new line once
      among the lines that commit's diff ADDS — never a FROM-zero count.
  (b) DELETE ITEM 32 BY DIGEST, not by retyping it. Item 32 is the block of lines
      from the one matching `^  32\. \*\*` up to but NOT including the next line
      matching `^  \d+\. \*\*`, joined by newlines WITHOUT a trailing one. At
      e10cbc30 that block is 23 lines and 1703 bytes and its sha256 is
          695759114c327d494d21e548170eeefd74e9263db04881dd9baa8de814d8000b
      Recompute that digest and REFUSE if it differs; the block is identified by
      its digest, not by a line number. DELETE THE BLOCK TOGETHER WITH THE
      NEWLINE THAT TERMINATES ITS LAST LINE — that is, replace `block + "\n"`
      with the empty string, exactly once. Deleting the block alone leaves that
      newline behind as a second blank line, which changes item 31's trailing
      bytes; the reviewer's dry run hit precisely that and G4's per-item digest
      sweep is what catches it. Item 32's own last line is blank — the separator
      before item 33 — so the correct deletion leaves item 31's own trailing
      blank line followed directly by item 33's first line.
  (c) FROZEN pair — add the retired-numbering sentences to the frozen paragraph.
      The FROM is a two-line anchor the reviewer confirmed occurs EXACTLY ONCE.
      The reviewer ran the containment test on this pair before emission and it
      printed `TO contains FROM: false`, so it is a REWRITE, not an append: the
      new text goes BETWEEN the anchor's two lines, so the TO does not contain
      the FROM contiguously. The obligation is therefore FROM 0x and TO 1x
      afterwards — not the append obligation of (a).

The self-use item (C5) — closure precondition 6
  `scripts/self_use_queue.json` holds nine items and NO pending one; the reviewer
  confirmed `packages.orchestration.self_use_queue.next_self_use_item()` answers
  `None` at e10cbc30. Precondition 6 therefore requires
  `packages.orchestration.self_use_generator.generate_and_append_if_empty()` FIRST.
  Run it, report the entry it appended, and then:
    (i)   `packages.orchestration.self_use_runner.run_next_self_use_item(
          dest_dir=<a directory under the gitignored .remedy-wt/>, repo_path='.')`
          — take its defaults for `max_provider_calls`, `max_cost_usd` and
          `max_tasks`. Report the returned entry id, the path and the JobPlan's
          id and status. The dest_dir is scratch and is NEVER committed.
    (ii)  `packages.orchestration.self_use_findings.describe_self_use_run_defects`
          for that run's own `JobPlan`. Report EVERY string it returns, verbatim
          and complete. An empty tuple means nothing to register — report the
          empty tuple explicitly, because "nothing was returned" and "nothing was
          checked" must not look the same.
    (iii) Write the run's record into `.agent/selfuse_f259/`, matching the shape
          of the precedent directory `.agent/selfuse_f262/`: the generated job
          markdown as `<entry id>.md`, and `run.txt` carrying the commands, the
          JobPlan id and status, the defect strings from (ii), and the budgets
          that were in force.
  DO NOT set `consumed_by` this round. Precondition 6 requires that edit in the
  CLOSURE commit, which is part 2's. If the runner raises, commit nothing for C5,
  record the full traceback in `run.txt` and in the handback, and continue with
  C6 — a failed self-use run is reported, never hidden, and the reviewer decides
  what it means.

Constraints
  1. Slices are applied BYTE FOR BYTE from the committed authored file by marker
     extraction in Python. Apply a slice you believe wrong verbatim and declare
     it in the handback.
  2. NOTHING in this round touches `docs/roadmap/STATUS.md` or `README.md`. The
     STATUS flip and the README capability sync must land in the SAME commit as
     each other (R-0154), and that commit is part 2's.
  3. Read `.agent/STOP` from disk before C0a, before C5 and before C6.
  4. NEWLINE CONVENTIONS: PLANF259R8 replaces `.agent/plan.md` whole with exactly
     one trailing newline; the record and slip appends are as described above;
     `docs/roadmap/features/T2_F259.md` and
     `docs/agents/planner_reviewer_prompt.md` each still end with exactly one
     newline after their edits.
  5. This session's shell guard refuses some command FORMS outright — shell
     loops, `$(...)` substitution, `$?` in a compound command, `${PIPESTATUS[0]}`,
     a `$` anchor inside a `grep -c` pattern, brace-with-quote literals in a
     heredoc, and a non-ASCII character in a Python bytes literal. Re-express in
     Python and report the Python you ran beside its output, with any refusal
     quoted verbatim. `ruff check` and the built `remedy` CLI are denied to this
     session; where a `remedy` subcommand is needed, use
     `python3 -m apps.cli.grouped <...>` and report which route was used.
  6. Commit subjects are `f259: <what>`. No leading-slash token, no absolute
     path. End every commit message with the trailer
     `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.
  7. AGENTS.md binds you in full. Never `--force`, never a history rewrite, never
     `gh pr merge`, never a branch deletion. C6 is ONE commit and reports no
     reading that only exists after it is pushed.
  8. The self-use RUN is a real job execution with a real budget. Let it run to
     the approval gate and no further; never approve, never apply, never promote
     its result. Precondition 6 says "to the normal approval gate like any other
     job — never applied".

Done when — the gates. Real exit codes, real output, one line per gate in the
handback. Every gate runs at or before C5.

  G1 TRANSPORT. `sha256sum .remedy-wt/f259-r8-block.md .agent/authored/f259-r8.md .agent/last_block.md`
     — one digest, three times.
  G2 THE RECORD AND THE SLIP. For `.agent/live_review.md`: pre-append bytes are a
     byte-exact PREFIX of the post-append bytes, remainder exactly
     `"\n" + GATE_R7 + "\n"`, and `grep -c '^Gate: R7 — '` 0 → 1. For
     `.agent/prose_slips.md`: same prefix property, remainder exactly
     `"\n\n" + SLIP8`, still no trailing newline. Byte lengths before and after
     for both.
  G3 THE FEATURE FILE. REGBANNER: FROM count 1 before, 0 after; TO count 1 after;
     the printed containment reading. BUILTSTATE: the post-commit bytes equal the
     pre-commit bytes with the pair applied plus exactly `"\n" + BUILTSTATE + "\n"`
     — report the boolean and the byte lengths. Then report the file's `^## `
     headings in order, and confirm `Built State` is among them and
     `REGISTRATION ONLY` occurs 0 times.
  G4 THE CONSOLIDATION, MEASURED BEFORE AND AFTER. Report: the item count and the
     full list of item numbers BEFORE the edit (expect 37, 1..37) and AFTER
     (expect 36, 1..31 and 33..37); the recomputed sha256 of the item-32 block
     before deletion, which must equal the value stated above; the ITEM16 and
     FROZEN containment readings, each printed; and the boolean that the
     post-commit file equals the pre-commit file with exactly those three edits
     applied and nothing else. Then confirm no OTHER item's text changed, by
     reporting the sha256 of every surviving item's block before and after and
     the count that differ — which must be exactly 1, item 16.
  G5 THE SELF-USE ITEM. Report, in order: `next_self_use_item()` before the
     generator (expect `None`); the entry `generate_and_append_if_empty()`
     appended, with its id, title and provenance; the runner's returned entry id,
     path, JobPlan id and status; the COMPLETE tuple from
     `describe_self_use_run_defects`; the files written under
     `.agent/selfuse_f259/` with their byte sizes; and the confirmation that
     `consumed_by` is still empty for the new entry — this round does not consume
     it. Also report `git status --porcelain` naming nothing under the runner's
     dest_dir.
  G6 THE SUITES. Run serially at C5, each a real run with its passed count and
     exit code. Expected counts re-measured by the reviewer at e10cbc30:
       python3 -m pytest tests/docs/ -q                                 expect 303
       python3 -m pytest tests/orchestration/test_roadmap_index.py -q   expect 30
       python3 -m pytest tests/ui_server/ -q                            expect 515
       python3 -m pytest tests/orchestration/test_test_runner.py -q     expect 52
       python3 -m pytest tests/regression/test_resource_safety.py -q    expect 21
       python3 -m pytest tests/orchestration/test_integrity_gate.py -q  expect 16
       python3 -m pytest tests/cli/test_golden_path.py -q               expect 42
       python3 -m pytest tests/test_agent_tooling.py -q                 report the number
     The last is added because this round edits `docs/agents/`. The four state
     readers are run as four. A different count is reported as the number it is,
     with failing node ids verbatim.
  G7 THE INTEGRITY GATE — closure precondition 3.
     `python3 -m apps.cli.grouped integrity check --json`. Report the full JSON,
     including `passed` and `fail_count`, and the exact command you ran. Also
     report `git status --porcelain` and confirm there are no relevant untracked
     files — listing any untracked path you see, with whether it is gitignored.
  G8 THE PLAN AND THE STRUCTURE. `wc -l .agent/plan.md` under 50; one `## Goal`
     and one `## Next Steps` (report both counts); `filecmp.cmp(..., shallow=False)`
     True against the slice plus one newline. Then `git status --porcelain` empty
     immediately before C6 is staged; `git ls-files .remedy-wt` returns nothing;
     every commit single-parent; `git diff --numstat <parent> <commit>` for EACH
     commit C0a through C5 reported cell by cell; each commit's insertion count
     against the 500 cap; the push result; and confirmation that no pull request
     was created.

The handback (C6) — rewrite .agent/handoff.md whole
  No length cap. Carry: feature, round and SESSION NUMBER — still SESSION 1 of
  F259, round 8, rounds so far 8; the commit range; a `## Commits` table with the
  `+/-` numbers G8 printed; the AGENTS.md item-status table, one row per bundle
  item C0a through C6; one line per gate G1 through G8 with its real reading; the
  complete self-use transcript of G5; the deviations; ONE sentence of context
  self-assessment; and the next expected action — the reviewer's gate, then
  CLOSURE PART 2: the ledger rotation, the evidence job, the review zip, the
  STATUS/README closure commit and the pull request. Repeat this line verbatim in
  its state block:
  `~97 % (T001–T004 ✅ · Integration Gate ✅ · Closure Teil 1 im Review · Teil 2 offen) — Schätzung`

<<<BEGIN PLANF259R8>>>
# Plan — F259 Vocabulary & concept model v1

Branch: feature/f259-vocabulary, cut from `main` at 25961794. Rounds 1 to 7
PASSED the reviewer's gate, the last of them the INTEGRATION GATE: the full
suite is green on the branch and at the merge base, with zero branch-only and
zero base-only failures. The round-7 verdict is booked by round 8's own C2.

## Goal

`docs/system/vocabulary.md` is the BINDING vocabulary page: the DECISION
amend0905-vocab D1 table, the do-not-confuse table, the Mermaid concept diagram,
the per-word meaning table, and D2–D10 plus F259 D1/D2 as dated DECISION
paragraphs. `tests/docs/test_vocabulary.py` pins it in planned mode against the
shipped `apps/cli/command_catalog.py`; the same diagram stands in `README.md`,
byte-equal and pinned; the page is registered in `docs/README.md`. No other
code: F259 decides words, F260 and F261 spend them.

## Current Step

Round 8 is CLOSURE PART 1, the content half: the feature file gains its Built
State and loses its registration-only banner; the §3 checklist takes its one
mandated consolidation pass, merging item 32 into item 16 and retiring the
number rather than renumbering, because the append-only review record
cross-references these items by number; the self-use queue is replenished and
its item is run to the approval gate; and the integration-gate verdict is booked.

## Next Steps

- CLOSURE PART 2: the ledger rotation as its own commit; the evidence job; the
  FRESH review zip, whose failure would be a closure blocker; the STATUS `[x]`
  line and the README capability sync in ONE commit with the self-use
  `consumed_by` edit; then the pull request, which is NOT merged in this session
  but at the next feature's Open PR Gate.

## Risks

- The self-use run is a real job execution. If it raises, that is reported and
  the reviewer decides what it means; it is never hidden and never retried into
  silence.
- The consolidation edits the document that governs the reviewer's own work. Its
  gate therefore measures every surviving item's digest, so a merge cannot
  quietly alter a rule it was only supposed to move.
<<<END PLANF259R8>>>

<<<BEGIN GATE_R7>>>
Gate: R7 — the F259 R7 entry, the INTEGRATION GATE (docs/agents/integration_gate.md steps 1 to 4) before closure. VERDICT PASS. THE FULL SUITE IS GREEN ON BOTH SIDES AND THE BRANCH INTRODUCES NO FAILURE: branch run 19694 passed, 23 skipped, 0 failed, exit 0, 134.50s; base run at the merge base 25961794 in a throwaway worktree 19686 passed, 23 skipped, 0 failed, exit 0, 161.68s; `comm -13` (branch-only) EMPTY and `comm -23` (base-only) EMPTY, both stated as empty rather than sampled, so there was nothing to attribute and no blocker. The difference of 8 is exactly the eight tests of `tests/docs/test_vocabulary.py`, which does not exist at the base. THE REVIEWER RE-RAN THE BRANCH SUITE ITSELF rather than reading the worker's number: `python3 -m pytest -n auto -q` in the primary checkout returned 19694 passed, 23 skipped, 1 warning in 141.61s — the same 19694, independently measured. This is the only entry in this record entitled to the "full suite" claim, per §3 verification tier 3. Range 6e6e73ae..e10cbc30, six commits, all single-parent, pushed, no pull request; largest commit 291 insertions. TRANSPORT: one digest `a8c08ea7d75b5c051a25a3e3c4ba347f80e38f8fb4e23bd07d2acb88cab09f39` across `.remedy-wt/f259-r7-block.md`, `.agent/authored/f259-r7.md` and `.agent/last_block.md`, equal to the reviewer's own pre-emission digest; a COPY chain per §3 item 37. The record append was proved by reconstruction: `.agent/live_review.md` equals its parent plus exactly `"\n" + GATE_R6 + "\n"` (839 318 to 843 886 bytes). THE PARITY RECIPE OBEYED THE TWO OPEN FINDINGS THE BLOCK NAMED, and the round produced fresh evidence for one of them. R-0591's clause: the copy was made with `symlinks=True`, and `apps/ui/node_modules/.bin` holds 23 symlinks in the primary checkout and 23 in the base worktree with equal name sets, so npm's shims were not dereferenced. R-0736's clause: the defect was reproduced directly before it was fixed — the worktree's newest source file `apps/ui/src/types/react-force-graph-2d.d.ts` stamped 1788645445.45 against a copied `apps/ui/dist/index.html` stamped 1788057215.85, so `_frontend_is_stale` read True and the base run would have manufactured its ~114 false failures; setting the dist mtimes to 1788645565.45 cleared it to False. R-0736 remains OPEN and `docs/agents/integration_gate.md` was correctly left unedited, because it is not F259's surface; the finding now carries a second independent measurement for whoever repairs it. THE WORKER FOUND A DEGENERACY IN THE REVIEWER'S OWN PARITY GATE AND ANSWERED IT PROPERLY. G4 ordered the dist mtimes stamped into the future AND ordered a test that no dist mtime fall inside the run's time window — and a synthetic stamp of newest_src plus 120 seconds necessarily lands inside a window the run then takes 162 seconds to open, so the ordered test reads "void" by construction rather than by evidence. The worker declared it and measured the EVENT a second, independent way, which is what R-0444 asks for: every dist file's ctime is 1788645468.32, 18.4 seconds BEFORE the run started, and every inode is unchanged, so no write and no replacement occurred; the mtimes are also identical before and after. No rebuild happened, the neutralisation was real, and the empty base-only list is the corroboration. The reviewer's gate error is recorded in `.agent/prose_slips.md` by the same commit that appends this entry. THE R-0176 DISCLOSURE the block required: writing run logs under `~` was refused by the sandbox, so the worker fell back to the gitignored `.remedy-wt/` and reported it; of the two node ids that finding names, neither exists in the suite at this tip, and the surviving `tests/orchestration/test_run_manifest_logical_identity.py` collects 11 ids, all passing in both runs. EVIDENCE, verified by the reviewer on disk: `.agent/gate_f259_r7/` holds all eight ordered files, no name ends in `.log`, and `branch_failed.txt`, `base_failed.txt`, `comm_13.txt` and `comm_23.txt` are each 0 bytes and 0 lines. TEARDOWN, verified by the reviewer: `git worktree list` shows the primary checkout and the ten pre-existing `remedy/job-*` worktrees and nothing else, no `tmp/*` branch survives, `git status --porcelain` is empty and `gh pr list --state open` returns `[]`. OPEN SET, recomputed mechanically per §3 item 10: 299 registrations against 5 `Done:` lines, 294 open, unchanged by this round.
<<<END GATE_R7>>>

<<<BEGIN SLIP8>>>
2026-09-05 · F259 R7 (reviewer) · The round-7 block's gate G4 ordered two things that cannot both be informative: step (ii) stamped every `apps/ui/dist` mtime into the FUTURE, at newest_src plus 120 seconds, to clear the staleness relation R-0736 names; step (iii) then ordered the parity claim VOID if any dist mtime fell inside the run's time window. A synthetic future stamp lands inside its own window whenever the run outlasts the offset, and the run took 162 seconds against a 120-second offset, so the test read "void" by construction and not by evidence. The worker declared the degeneracy and measured the event a second, independent way — ctime and inode, both of which any rebuild would change — finding every dist ctime 18.4 seconds BEFORE the run started and every inode unchanged, which establishes what the window test was written to establish. THE LESSON: §3 item 18 asks whether an ordered recipe and the property it must establish agree, and this pair fails that reading in a way neither half shows alone — when a gate MUTATES the very attribute a later clause measures, the later clause must read a DIFFERENT attribute, not the mutated one. Order ctime or inode where the mtime is the thing being set, or offset the stamp beyond the expected run duration and say why. Reviewer-authored gate degeneracy; the worker's substitute measurement is sound and the base-only failure list came back empty, so nothing on disk under `packages/`, `apps/`, `tests/` or `docs/` is wrong; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIP8>>>

<<<BEGIN REGBANNER_FROM>>>
> REGISTRATION ONLY — nothing in this file has been implemented.
<<<END REGBANNER_FROM>>>

<<<BEGIN REGBANNER_TO>>>
> BUILT 2026-09-06 on branch `feature/f259-vocabulary`; see Built State below.
<<<END REGBANNER_TO>>>

<<<BEGIN BUILTSTATE>>>
## Built State
Built 2026-09-06 on `feature/f259-vocabulary`, cut from `main` at 25961794.
Seven delegated rounds, every one PASSED by the reviewer; the seventh was the
integration gate.

What exists now:

- `docs/system/vocabulary.md` — the BINDING page. It carries, in order: a
  binding preamble; a "How to read the table" section explaining why the code
  spelling today and the code spelling after F260/F261 differ on purpose; the
  DECISION amend0905-vocab D1 table with one row per word for all fifteen words
  (Project, Order, Mission, Contract, Job, Plan, Task, Run, Round, Worker,
  Decision, Evidence, Gate, Verdict, Roadmap), each with its meaning, its code
  spelling today, its code spelling after F260/F261, its CLI spelling and what
  it is NOT; the do-not-confuse table with the eight pairs T2_F259.md's Goal &
  Done names; the concept model as a Mermaid `flowchart TD`; the rulings —
  DECISION amend0905-vocab D2 through D10 copied byte-verbatim from
  `.agent/decisions.md` and DECISION F259 D1 and D2 copied byte-verbatim from
  this file, edited only by one heading level; and the per-word meaning-fragment
  table the test's enforced mode reads.
- The "code spelling today" column was READ, not remembered. `.agent/f259_inventory.md`
  holds the measurement it was taken from: 471 `path:line` citations across the
  seven modules T001 names, each quoting its source line verbatim, every one
  re-verified by the reviewer against disk.
- `tests/docs/test_vocabulary.py` — eight tests, reading the SHIPPED catalog by
  importing `CATALOG` and `GROUPS` from `apps/cli/command_catalog.py`, never a
  transcript. `VOCABULARY_MODE = "planned"` is a plain module constant that F261
  flips to `"enforced"`; nothing in the file is skipped. The two mode-dependent
  tests assert the OPPOSITE thing in each mode, so planned mode measures the
  outstanding debt rather than switching a test off, and the file turns red by
  itself when F261 finishes the renames without flipping the constant. Measured
  at the close: 64 retired-synonym occurrences and 664 meaning violations remain
  in the catalog — F261's work, recorded rather than hidden.
- `README.md` carries the same Mermaid block under the one-sentence description,
  byte-equal to the page's; the eighth test pins the two together, and the page's
  block is in turn pinned byte-equal to the one in this file.
- `docs/system/vocabulary.md` is registered in `docs/README.md`'s Quick-Find
  table and its System Documentation table.
- DECISION F259 D3 (in `.agent/decisions.md`) scopes the enforced-mode synonym
  scan to the catalog surface and names `Worker:` as deliberately outside it,
  because that string occurs nowhere in the catalog and asserting its absence
  there would forbid nothing. That check belongs to F261.

Deliberate absences: F259 renames no command, moves no module, changes no data
shape and edits no catalog description. It decides the words; F260 and F261
spend them.
<<<END BUILTSTATE>>>

<<<BEGIN ITEM16_FROM>>>
      NAMES, wherever in the block that list lives, and prefer naming it over counting it.
<<<END ITEM16_FROM>>>

<<<BEGIN ITEM16_TO>>>
      NAMES, wherever in the block that list lives, and prefer naming it over counting it.
      Finding R-0656 brings this item to a GATE's or a CONSTRAINT's OWN WORDING, which
      neither this item as first written nor item 11 reached: item 11 forbids the numeral
      in a CONVENTION PARAGRAPH and this one forbade it in a HEADING or a quantifying
      sentence, while a gate's own text is neither. A gate or a constraint that names a
      CATEGORY of the block's own slices — the whole texts, the marker prefixes, the pairs
      — names that category and gives NO numeral for it, because the numeral is
      hand-counted while the extraction standing beside it is measured, so the two drift
      the moment the block is edited and the hand-counted half is the one nobody re-reads.
      Where a count is genuinely owed, the block orders the WORKER to report the number IT
      measured rather than naming one itself. R22's G3 ordered the extraction "for the two
      whole texts" over a block carrying three, and R23's G10 bound the marker sweep to
      "every one of the four marker prefixes" over the six that block's G3 names, as the
      recurrence paragraph committed at `bdc242b4` records; in each the block's arithmetic
      was right and only the adjective was wrong, which is why no gate the block ordered
      could see it and the WORKER caught each. Consolidated into this item at F259's
      closure on 2026-09-06 from what was item 32; that number is RETIRED, not reused.
<<<END ITEM16_TO>>>

<<<BEGIN FROZEN_FROM>>>
  round, and it grew fastest exactly where it was already being skimmed.
  Reverse by deleting this paragraph.
<<<END FROZEN_FROM>>>

<<<BEGIN FROZEN_TO>>>
  round, and it grew fastest exactly where it was already being skimmed.
  Consolidated once, at F259's closure on 2026-09-06: item 32 was merged into item
  16, whose family it belonged to and which its own text named, leaving 36 items.
  A merged item's NUMBER IS RETIRED AND NEVER REUSED, and the survivors are NEVER
  RENUMBERED, so this list now runs 1 to 31 and 33 to 37. The reason is that
  `.agent/live_review.md` is append-only and cross-references these items by
  number from dated entries that cannot be corrected: renumbering would silently
  re-point every one of those references at a different rule, which is a worse
  failure than a gap in the numbering. The next consolidation measures against 36.
  Reverse by deleting this paragraph.
<<<END FROZEN_TO>>>
