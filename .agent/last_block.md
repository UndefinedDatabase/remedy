STEP T001-B / F259 — Vocabulary & concept model v1 — round 2 of session 1
BRANCH feature/f259-vocabulary, already cut and pushed; its head at the time this
block was written is 85b0e8b5, the round-1 handback commit.

Goal
  Book the reviewer's PASS verdict on round 1, repair one byte the round-1 slice
  cost `.agent/live_review.md`, record two reviewer prose slips, and create
  `docs/system/vocabulary.md` carrying its binding preamble and the DECISION
  amend0905-vocab D1 table — one row per D1 word, with the "code spelling today"
  column taken from `.agent/f259_inventory.md` and from nothing else. The
  do-not-confuse table, the Mermaid diagram and the D2–D10 paragraphs are NOT in
  this round; they are rounds 3 and 4.

Bundle, in this order (one commit each)
  C0a save the block file to .agent/authored/f259-r2.md (copy, never retype)
  C0b mirror it to .agent/last_block.md
  C1  .agent/plan.md ← PLANF259R2 (whole rewrite)
  C2  .agent/live_review.md: the blank-line repair, then GATE_R1 appended at end
      of file; .agent/prose_slips.md: SLIP1 and SLIP2 appended. One commit — all
      three edits are this round's booking of the round-1 verdict.
  C3  docs/system/vocabulary.md (new) ← VOCABPAGE
  then push; run the gates
  C4  rewrite .agent/handoff.md; push again.

  Create NO pull request. F259's pull request belongs to its closure round.

Change set — EXACTLY these paths and nothing else
  .agent/authored/f259-r2.md (C0a) — .agent/last_block.md (C0b) —
  .agent/plan.md (C1) — .agent/live_review.md, .agent/prose_slips.md (C2) —
  docs/system/vocabulary.md (C3) — .agent/handoff.md (C4)

  C0a and C0b are SEPARATE commits this round. Round 1 collapsed them into one
  and that commit carried 908 insertions, over the AGENTS.md Commit Discipline
  cap; split, neither half reaches it. This is the shape every later F259 block
  uses.

Delivery — how this block reaches the repository
  The block is on disk, written by the reviewer, at
      .remedy-wt/f259-r2-block.md
  `.remedy-wt/` is gitignored (`.gitignore` line 235). C0a COPIES that file —
  `shutil.copyfile` or `cp`, never a retype — to .agent/authored/f259-r2.md, and
  C0b copies it to .agent/last_block.md. Every slice you apply is extracted from
  the COMMITTED .agent/authored/f259-r2.md by marker extraction in Python.

The authored slices. Each lies between its own one-line BEGIN and END marker;
the slice is the bytes between the BEGIN marker's newline and the newline before
the END marker, EXCLUDING that final newline. The marker lines themselves are
never applied to any file.

The blank-line repair (C2, first edit)
  Round 1's LRHEAD_TO slice replaced the record's preamble, and the reviewer's
  constraint ordered exactly one newline after it, where the preamble it replaced
  had ended with an empty line. `.agent/live_review.md` therefore reads
  `…the closure sequence.` immediately followed by `## Findings` with no blank
  line between them. Insert exactly one newline byte immediately before the `#`
  of `## Findings`, so the file reads `…the closure sequence.\n\n## Findings\n`.
  Assert first that `\n## Findings\n` occurs EXACTLY ONCE in the file and that
  `\n\n## Findings\n` occurs ZERO times; assert afterwards that the second count
  is 1. Nothing else in the file changes in this edit.

The GATE_R1 append (C2, second edit)
  `.agent/live_review.md` ends with a newline. Append the bytes
      "\n" + GATE_R1 + "\n"
  so the record gains one empty line and then the GATE_R1 line at end of file.
  This is the file's existing convention: records are appended at end of file,
  separated by one empty line.

The prose-slip appends (C2, third edit)
  `.agent/prose_slips.md` does NOT end with a newline (measured by the reviewer
  at 85b0e8b5: 74 550 bytes, final byte `.`). Its entries are separated by one
  empty line. Append the bytes
      "\n\n" + SLIP1 + "\n\n" + SLIP2
  and add NO trailing newline, so the file's convention is preserved. The file
  is append-only and is never rewritten or renumbered (AGENTS.md, prose_slips.md).

Constraints
  1. Every slice is applied BYTE FOR BYTE from the committed
     .agent/authored/f259-r2.md by marker extraction in Python. You may not
     improve, rewrap, re-punctuate or shorten a slice, and you may not fix an
     error you find in one: apply it as written and declare the problem in the
     handback's deviations. The reviewer owns this text.
  2. `docs/system/vocabulary.md` is a NEW file. Write it as VOCABPAGE plus
     exactly one trailing newline, and create no other file under `docs/`.
     Registering the page in `docs/README.md` is round 6's work (T004), not
     this round's — do not do it early.
  3. Read `.agent/STOP` from disk before C0a, before C3 and before C4. If it
     exists, finish the commit in hand, write the handback saying so, push, and
     stop.
  4. NEWLINE CONVENTIONS, all four in one place: PLANF259R2 replaces
     `.agent/plan.md` whole and ends with exactly one trailing newline; VOCABPAGE
     creates `docs/system/vocabulary.md` with exactly one trailing newline;
     GATE_R1 is appended as described above and is ONE line containing no
     newline of its own; SLIP1 and SLIP2 are each ONE line and the appended
     region ends with NO newline.
  5. This session's shell guard refuses some command FORMS outright — shell
     loops, `$(...)` substitution, `$?` in a compound command, a `$` anchor
     inside a `grep -c` pattern, brace-with-quote literals in a heredoc. Do not
     fight it: re-express the check in Python (`python3 -c`, or a script under
     the gitignored `.remedy-wt/`) and report the Python you ran beside its
     output, with the refusal quoted verbatim. No gate is dropped or narrowed
     because a form was refused.
  6. Commit subjects are `f259: <what>`. No leading-slash token, no absolute
     path. End every commit message with the trailer
     `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.
  7. AGENTS.md binds you in full: the self-review loop before EVERY commit, the
     Commit Gate, the branch never being `main`, `git push -u origin
     feature/f259-vocabulary`. Never `--force`, never a history rewrite, never
     `gh pr merge`, never a branch deletion.
  8. NO `path:line` citation appears anywhere in VOCABPAGE. The page names
     MODULES and SYMBOLS, because a symbol survives an edit above it and a line
     number does not (AGENTS.md, Code Discoverability Conventions; the same rule
     the §3 checklist states as item 9). `.agent/f259_inventory.md` is where the
     line numbers live, and it is dated and disposable; the page is not.
  9. Do-not-touch, from T2_F259.md: no command is renamed, no module is moved,
     no data shape changes, no catalog description is edited. This round writes
     one new documentation page and four `.agent/` state edits, nothing else.

Done when — the gates. Real exit codes, real output, one line per gate in the
handback. Every gate runs at or before C3, so the handback can quote all of
them; none is ordered after the commit that writes the handback.

  G1 TRANSPORT. `sha256sum .remedy-wt/f259-r2-block.md .agent/authored/f259-r2.md .agent/last_block.md`
     — one digest, three times. Report the digest and all three paths. It is a
     copy chain, not a retype chain, which is why one reading settles it.
  G2 THE THREE APPENDS OF C2, each proved by a PREFIX property rather than by a
     line count. For `.agent/live_review.md`: report the count of `\n## Findings\n`
     and of `\n\n## Findings\n` before the repair (expect 1 and 0) and after
     (expect 0 and 1); then, for the GATE_R1 append, the file's bytes immediately
     before the append are a byte-exact PREFIX of its bytes after, and the
     remainder is exactly `"\n" + GATE_R1 + "\n"` — report both booleans;
     and `grep -c '^Gate: R1 — ' .agent/live_review.md` goes from 0 to 1. For
     `.agent/prose_slips.md`: the pre-append bytes are a byte-exact PREFIX of the
     post-append bytes and the remainder equals `"\n\n" + SLIP1 + "\n\n" + SLIP2`
     exactly — report both booleans — and the file still does not end with a
     newline. Report `git show --numstat <C2>` verbatim beside these readings
     rather than asserting its numbers: the prose-slip file's missing final
     newline makes the diff's line accounting unobvious, and the prefix property
     is the real proof.
  G3 THE PAGE LANDED VERBATIM AND ROWS THE RIGHT WORDS. `docs/system/vocabulary.md`
     equals the extracted VOCABPAGE slice plus one trailing newline, compared with
     `filecmp.cmp(..., shallow=False)` against the extraction written to
     `.remedy-wt/`; report the boolean. Then extract the first cell of every table
     row of the page's word table, in file order, strip the bold markers, and
     report that list. It must equal, in order, the words DECISION amend0905-vocab
     D1 names: Project, Order, Mission, Contract, Job, Plan, Task, Run, Round,
     Worker, Decision, Evidence, Gate, Verdict, Roadmap. Report the length your
     own extraction measured rather than checking it against a number this block
     states.
  G4 EVERY MODULE AND SYMBOL THE PAGE NAMES RESOLVES. Write a checker under
     `.remedy-wt/` (gitignored, never committed) that (a) collects every
     backticked span on the page that CONTAINS A SLASH and ends `.py`, and
     confirms each such file exists — report the count found and the count
     resolved, which must be equal. The slash is what makes this a path rather
     than a filename: the "after F260/F261" column deliberately names
     `job_plan.py`, a module F261 has not created yet, and a bare `.py` appears
     in ordinary prose, so neither is a path and neither is checked. Then (b)
     for every OTHER backticked span on the page that is a bare
     Python identifier or a dotted identifier — no spaces, no `<`, no `-` — that
     the page attributes to a module in the same table cell, confirms the
     identifier occurs in that module's source. Report the count checked, the
     count found, and the full list of any not found. Then run a NEGATIVE
     CONTROL: on a COPY of the page under `.remedy-wt/`, rename one identifier to
     a name that does not exist and confirm the checker reports exactly one
     failure — a checker that cannot fail proves nothing when it passes.
  G5 THE SUITES, RUN SERIALLY, at C3. Each is a real run; report the passed count
     and exit code for each. The expected counts were measured by the reviewer at
     85b0e8b5, this branch's head before this round:
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
  G6 THE PLAN MEETS ITS CONTRACT. `wc -l .agent/plan.md` under 50; the file
     carries one `## Goal` heading and one `## Next Steps` heading (report both
     counts); and it equals the extracted PLANF259R2 slice plus one trailing
     newline under `filecmp.cmp(..., shallow=False)` — report the boolean.
  G7 STRUCTURE. `git status --porcelain` empty immediately before C4 is staged
     and again after the final push; `git ls-files .remedy-wt` returns nothing
     (report the line count); every commit single-parent; and
     `git diff --numstat <parent> <commit>` for EACH commit C0a through C3,
     reported cell by cell so the handback's `## Commits` table carries the same
     numbers this gate printed and is derived from `git diff --numstat` and from
     nothing else. Report each commit's insertion count against the 500 cap; if
     one exceeds it, declare it with its inseparability reason rather than
     splitting a slice. Report the push result and confirm no pull request was
     created.

The handback (C4) — rewrite .agent/handoff.md whole
  No length cap. It must carry: the feature, the round and the SESSION NUMBER —
  this is still SESSION 1 of F259, round 2, rounds so far 2; the commit range;
  a `## Commits` table with one row per commit giving the files and the `+/-`
  numbers G7 printed; the item-status table AGENTS.md requires, one row per
  bundle item C0a through C4 with a status of done, skipped or deviated with a
  reason; one line per gate G1 through G7 with its real reading; the deviations
  and assumptions; ONE sentence of context self-assessment (operator amendment
  amend0905-throughput); and the next expected action, which is the reviewer's
  gate of this round and then round 3, the do-not-confuse table and the Mermaid
  diagram. Repeat this line verbatim in its state block:
  `~25 % (T001 inventory ✅ · D1-Tabelle im Review · Diagramm, T002, T003, T004 offen) — Schätzung`

<<<BEGIN PLANF259R2>>>
# Plan — F259 Vocabulary & concept model v1

Branch: feature/f259-vocabulary, cut from `main` at 25961794. Round 1 PASSED the
reviewer's gate; its verdict is booked in `.agent/live_review.md` by round 2's
own C2, which is where a verdict lands under operator amendment
amend0827-process-diet rule 1.

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

Round 2 — create `docs/system/vocabulary.md` with its binding preamble and the
D1 table, every "code spelling today" cell taken from `.agent/f259_inventory.md`
and from nothing else; book the round-1 verdict and two reviewer prose slips;
repair the blank line the round-1 preamble slice cost the review record.

## Next Steps

- Add the do-not-confuse table, the Mermaid diagram and its short
  REMEDY_EINSTIEG-grade description; that completes T001.
- Write D2–D10 and F259 D1/D2 onto the page and check `T2_F263.md`'s heading for
  a working name (T002).
- Write `tests/docs/test_vocabulary.py` in planned mode with both of the red
  proofs T2_F259.md's T003 names.
- Put the Mermaid block into `README.md` and register the page in
  `docs/README.md` (T004).
- Run the integration gate, then the closure sequence.

## Risks

- The page's middle two columns say different things ON PURPOSE — today's
  spelling and the spelling after F260/F261 — and a reader who conflates them
  will think the page is wrong. The preamble says so before the table.
- `README.md` has a guarded region: its `Accepted in Tier 2 so far:` block is
  scanned for feature ids, and putting an unaccepted id there is what R-0797
  was. Round 6 writes into that file and must add no id token.
<<<END PLANF259R2>>>

<<<BEGIN GATE_R1>>>
Gate: R1 — the F259 R1 entry. R1 WAS THE CLAIM AND THE T001 SOURCE INVENTORY. VERDICT PASS. Range 25961794..85b0e8b5, seven commits, all single-parent, pushed to `origin/feature/f259-vocabulary`, no pull request created. The reviewer re-ran every gate itself rather than reading the handback's numbers. TRANSPORT: `sha256sum` over `.remedy-wt/f259-r1-block.md`, `.agent/authored/f259-r1.md` and `.agent/last_block.md` returns the single digest `6b0cd1746c917224a52cfd71d07b9497729b6ea2f8441ffb85702911add499cf`, equal to the digest the reviewer computed over its own scratch file before emission; per §3 item 37 that chain covers the reviewer's scratch file, the worker's saved copy and the mirror — it is a COPY chain under docs/agents/self_drive_protocol.md, where nothing is retyped, and it is not a claim about bytes emitted into a prompt. SLICES: the reviewer extracted each slice from the COMMITTED `.agent/authored/f259-r1.md` and compared it against disk — `LRHEAD_TO` is an exact byte prefix of `.agent/live_review.md` at ddf1e9b3 with `## Findings` beginning immediately after it; `.agent/plan.md` and `.agent/context.md` at 951134e8 each equal their slice plus one trailing newline exactly; the `DONE0797` slice occurs exactly once at 6efb510b in the shape Landed-line, empty line, Done-line, empty line, `- R-0798` line, with the `Landed: R-0797` line surviving byte for byte as §4 item 4 requires. RECORD CARRIED FORWARD: the bytes from `## Findings` to end of file are byte-IDENTICAL across the re-head at ddf1e9b3, 815 223 bytes, sha256 `c9a028823fc3a8018ca85e6d90bcbdc4049e4fa2ab976ac025f6595efdb4db9e` before and after, equal to the value the reviewer measured at 25961794 before the block was emitted. LEDGER: `docs/roadmap/STATUS.md` at 67598164 differs from its parent in exactly the F259 line and in nothing else — the reviewer reconstructed the parent by the single substitution and compared byte-for-byte — leaving one `[~]` line and 72 `[x]` lines. OPEN SET, recomputed mechanically per §3 item 10: 299 `^- R-\d{4} — ` registrations against 5 `^Done: R-\d{4} — ` lines, 294 open, down one from the 295 measured at the branch point because this round closed R-0797. SUITES, re-run by the reviewer serially and all exact: `tests/docs/` 295, `tests/orchestration/test_roadmap_index.py` 30, `tests/ui_server/` 515, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16, `tests/cli/test_golden_path.py` 42. INVENTORY: the reviewer wrote its OWN citation checker rather than trusting the worker's and measured 471 citations, 471 resolving to an existing file and line, 0 whose quoted text differs from the source, with a negative control perturbing one quotation and correctly reporting exactly 1 mismatch; `len(GROUPS)` 60, `len(CATALOG)` 342 and 17 user-facing groups were re-derived by IMPORTING `apps.cli.command_catalog`, and all three equal the values DECISION amend0905-vocab D4 measured independently at `b2ee0a84`. TWO COMMITS EXCEED THE 500-INSERTION CAP AND BOTH WERE DECLARED BY THE WORKER BEFORE REVIEW, which is the honest route AGENTS.md Commit Discipline names: C4 `c2f74bd1` at 615 insertions is ONE new file holding one indivisible measurement and is ACCEPTED as this feature's single stated-cause overage, and it is not a precedent; C0 `686dde44` at 908 was the reviewer's own authoring error, because the block collapsed the authored save and the `.agent/last_block.md` mirror into one commit where the precedent block of amend0905-throughput had split them into C0a and C0b for exactly this reason, and split they are 463 and 445, both under the cap. BINDING ON EVERY LATER F259 BLOCK: the block save is TWO commits. Neither overage is a finding with product effect under operator amendment amend0827-process-diet rule 2 — nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong and no gate over production code is blind — so no R-id is spent and the two reviewer-side lessons are recorded in `.agent/prose_slips.md` by the same commit that appends this entry.
<<<END GATE_R1>>>

<<<BEGIN SLIP1>>>
2026-09-05 · F259 R1 (reviewer) · The round-1 block ordered the authored save and the `.agent/last_block.md` mirror as ONE commit (C0), which landed 908 insertions against the 500-insertion cap of AGENTS.md Commit Discipline, while the amend0905-throughput block the reviewer had read while writing it split exactly that work into C0a and C0b — 463 and 445 apart, both under the cap. The reviewer copied the precedent's slice conventions and not its commit split. THE LESSON: the block-save commit costs roughly twice the block's own length, because the authored file is a full insert and the mirror is a full rewrite, so a block over about 250 lines must split the save or it orders an overage by arithmetic alone. Reviewer-authored ordering slip; the worker declared it correctly before review and nothing on disk under `packages/`, `apps/`, `tests/` or `docs/` is wrong; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIP1>>>

<<<BEGIN SLIP2>>>
2026-09-05 · F259 R1 (reviewer) · The round-1 block's constraint 4 ordered the `LRHEAD_TO` preamble slice "followed by exactly one newline, so `## Findings` still begins its own line", and the preamble it replaced had ended with an EMPTY line, so the applied file reads `…the closure sequence.` immediately followed by `## Findings` with no blank line between them. The constraint reasoned about what the heading needs to PARSE and not about what the region it replaced actually ended with; the worker applied the slice verbatim as constraint 1 required and flagged the gap rather than silently fixing it. THE LESSON: a whole-region replacement's newline convention is derived from the BYTES of the region being replaced, which the block already had to measure to identify the region at all, not from what the following construct needs in order to render. Reviewer-authored newline slip in an `.agent/` prose file, repaired by round 2's C2; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIP2>>>

<<<BEGIN VOCABPAGE>>>
# Vocabulary — the words Remedy uses

> **BINDING.** These are the words. Every feature, every command description in
> `apps/cli/command_catalog.py` and every document under `docs/` uses them with
> the meaning given here, and uses no synonym for a word that already has one.
> The operator decided them on 2026-09-05 in order amend0905-vocab-rebuild,
> DECISION amend0905-vocab D1; F259 wrote them down. To change a word, change
> this page first.

## How to read the table

Two of the columns disagree on purpose. **Code spelling today** is what the
source really says right now — it was read out of the code, not remembered, and
`.agent/f259_inventory.md` holds the per-symbol citations it was taken from,
measured at commit `67598164`. **Code spelling after F260/F261** is a PLAN:
F260 rebuilds the data model and F261 performs the renames, and until they land
the two columns differ wherever the current code carries a word this page
retires. A reader who conflates them will think the page is wrong about the
code; it is not, it is about both the code and the decision.

The last column is the one that does the work. Most of the confusion this page
exists to end was not people failing to define a word — it was two words for one
thing, or one word for two things.

## The words

| Word | Meaning | Code spelling today | Code spelling after F260/F261 | CLI spelling | Is NOT |
|---|---|---|---|---|---|
| **Project** | The frame: one or more repos and every mission inside them. | `project_id` in `packages/core/models.py` and in `packages/orchestration/mission_state.py`, which also defines `mission_dir_for_project` and `project_ids_with_missions`; the store path is `projects_dir` in `packages/orchestration/data_paths.py` | unchanged | the `project` group: `create`, `list`, `show`, `attach-repo`, `attach-job`, `brain`, `context`, `summary`, `current`, `adopt` | — |
| **Order** | Everything the human gives Remedy: the initial text or file behind `remedy do`, and every later message during a run. | no symbol spells it; the same thing is carried under two other names — `parse_job_file`, `plan_job_from_file` and `job_file_sha256` in `packages/orchestration/pingpong_job.py`, and the `--job-file` and `--task-file` options in `apps/cli/command_catalog.py` | `order`; both option spellings are deleted and the argument becomes the positional `<order>`, text or a `.md` path (DECISION F259 D2) | none today; `do <order>` after F261 | the Job — the Order is the input, the Job is Remedy's response |
| **Mission** | What every Order becomes: one persistent record holding the Order, the Contract, the mission Plan and an ordered list of 1..n Jobs. | `Mission`, `MissionJobLink`, the `MISSION_STATUS_` and `MISSION_ROLE_` constants and the `Mission*Error` family, all in `packages/orchestration/mission_state.py` | unchanged as a type; a mission is created for EVERY order, which reverses F056's "a mission is never created automatically" (DECISION amend0905-vocab D2) | the `mission` group: `list`, `show`, `plan`, `contract`, `run`, `continue`, `pause`, `resume`, `achieve`, `abandon`, `start` | a schedule; a job |
| **Contract** | The acceptance criteria of a Mission, compiled to machine-checkable checks — its Definition of Done. One per mission; a job's contract is the derived slice for that job. | nothing in the seven sources spells this concept; its two halves are `PlannedTask.acceptance` in `packages/orchestration/schemas/models.py` and `packages/orchestration/dod_compiler.py`. The catalog's `contract` group today is a DIFFERENT concept wearing the word: the run-permission object, as `contract.inspect`, `contract.check` and `contract.set` | `contract` names the acceptance criteria and nothing else; the run-permission group is deleted and its idea folded into permissions and fences (DECISION amend0905-vocab D4) | `mission contract <id>` and `job contract <id>` after F261 | the run-permission object once called the "run contract" |
| **Job** | The administrative unit under a mission: identity, budget, fences, permissions, decisions, the job Plan with its Tasks, and references to its Runs. | the record and its parts are `Job`, `JobBudgets` and `JobFences` in `packages/core/models.py`; the plan and the state constants are `JobPlan`, `JOB_PLANNED`, `JOB_RUNNING`, `JOB_BLOCKED`, `JOB_COMPLETED`, `JOB_PAUSED` and `JOB_STOPPED` in `packages/orchestration/pingpong_job.py`. Two id shapes are minted from two stores, which `packages/orchestration/data_paths.py` documents in as many words: "Remedy has TWO job stores and they are shaped differently" | one store and one id shape (F260) | the `job` group | the Run |
| **Plan** | The ordered "what will be done" of a level: the mission plan lists the milestones, each of which becomes a job; the job plan lists the tasks. | two dialects side by side. `packages/orchestration/schemas/models.py` defines `FlightPlan`, `FlightPlanClarification`, `PlannerPlan`, `PlannedTask` and `FLIGHT_PLAN_SCHEMA_V`; `packages/orchestration/flight_plan.py` defines `FlightPlanResult` and `map_flight_plan_to_tasks`; and `packages/orchestration/pingpong_job.py` carries `JobPlan` beside them | `flight_plan.py` becomes `job_plan.py` and the noun "flight plan" is deleted from code, catalog, docs and feature files (DECISION amend0905-vocab D6) | `job plan` and `mission plan` are the only two plan commands; today's `plan status` and `plan next` become the hidden group `roadmap` | the Roadmap |
| **Task** | One step in a job plan; the planner chooses how many, bounded by configured maxima that are ceilings, not targets. | four spellings for one idea: `Task` in `packages/core/models.py`; `TaskEntry` in `packages/orchestration/pingpong_job.py`, alongside the `TASK_PENDING` to `TASK_SPLIT` state constants, `max_tasks` and the converters `task_entry_to_planned_task` and `planned_task_to_task_entry`; and `PlannedTask` and `ProposedTask` in `packages/orchestration/schemas/models.py` | one task type (F260) | no group of its own; it appears as `job run <id> --tasks n` and `job context <id> --task <t>` | a Round |
| **Run** | One execution of the ping-pong loop for exactly one Task, owning exactly one evidence folder. | `RunState` in `packages/core/models.py`; `run_id`, `run_job` and the `run_manifest_path`, `run_manifest_created_at` and `run_manifest_episodes` fields in `packages/orchestration/pingpong_job.py`; `runs_dir` in `packages/orchestration/data_paths.py`. The word also names a provider call in one place and a whole execution in another | `run` means the per-task execution and nothing else | `run show <id>` and `run list` after F261; today the verb is scattered across `job run`, `do run`, `mission run`, `loop run` and more | the verb; a dogfood run; the run manifest |
| **Round** | One pass inside a run: build, then tests, then review. Round 2 and later are repairs. | `max_rounds`, `max_rounds_source`, `repair_rounds_allowed`, `repair_rounds_used` and `repair_rounds_source` in `packages/orchestration/pingpong_job.py` | unchanged | none | a Task — a task can take several rounds |
| **Worker** | A model in a role. The roles are Builder, Reviewer, Planner and Teacher, and the list is extensible. | nothing spells the concept itself; the roles appear as the `builder_model` and `reviewer_model` fields in `packages/orchestration/pingpong_job.py` | unchanged as a type, but the report names the ROLE and never says "Worker: fake" for a builder (DECISION amend0905-vocab D1) | the `worker` group: `list`, `show`, `resources`, `unload`, `status`, `doctor` after F261 | — |
| **Decision** | A question Remedy cannot answer for itself, put to the human and answered with one command. | `HumanDecision` in `packages/orchestration/decision_queue.py`; the flight-plan approval path spells the same idea as `flight_plan_approval_open` and `resolve_flight_plan_approval` in `packages/orchestration/flight_plan.py` | the approval stays a Decision; the retired noun leaves its name with DECISION amend0905-vocab D6 | the `decision` group: `list`, `show`, `resolve`, `explain` | a DECISION paragraph in `.agent/decisions.md`, which is Remedy's own build record and not a user concept |
| **Evidence** | What one Run leaves behind: exactly one folder per task run, holding the inputs, the outputs and the proofs. | `build_evidence_bundle` in `packages/orchestration/pingpong_evidence.py`; `stream_evidence` and `job_evidence_dir` in `packages/orchestration/pingpong_job.py`; `mission_evidence_dir` in `packages/orchestration/mission_state.py`; `evidence_exports_dir` in `packages/orchestration/data_paths.py` | unchanged | `job evidence <id>` after F261; today `do evidence` and `do job-evidence` | the run manifest, which is one file inside the folder |
| **Gate** | A check that must pass before the work may proceed; it decides, and it records what it decided from. | `GateResult` in `packages/orchestration/dod_gate.py`, the only type under `packages/` named for the concept itself rather than for one particular gate; nothing in the seven sources spells it | unchanged | none | a Verdict — the gate is the check, the verdict is the Reviewer's judgement |
| **Verdict** | The Reviewer's judgement on one Round. | `Verdict` and `ReviewVerdict` in `packages/orchestration/schemas/models.py`, where `Verdict` is the literal set pass, fail, needs_repair, blocked; the field carrying it is `reviewer_verdict` in `packages/orchestration/pingpong_job.py` | unchanged | none | a Gate's result |
| **Roadmap** | Remedy's own build plan under `docs/roadmap/`; a developer tool, never a user concept. | nothing in the seven sources spells it; the ledger is the file `docs/roadmap/STATUS.md` | unchanged | today's `plan status` and `plan next` become the hidden group `roadmap` (DECISION amend0905-vocab D6) | a mission plan |

The seven sources the "code spelling today" column was read from are
`packages/core/models.py`, `packages/orchestration/pingpong_job.py`,
`packages/orchestration/schemas/models.py`,
`packages/orchestration/flight_plan.py`,
`packages/orchestration/mission_state.py`,
`packages/orchestration/data_paths.py` and `apps/cli/command_catalog.py`.
Where a cell names a module outside that list —
`packages/orchestration/decision_queue.py`,
`packages/orchestration/pingpong_evidence.py`,
`packages/orchestration/dod_gate.py` and
`packages/orchestration/dod_compiler.py` — it is because DECISION
amend0905-vocab D1 gave that word no table row and told F259 to write one from
the feature that owns the concept; they were found by searching every `.py`
file under `packages/` and under `apps/`.
<<<END VOCABPAGE>>>
