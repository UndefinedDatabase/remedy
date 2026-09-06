# STEP — F260 round 20: closure part 1, the self-use item and the checklist consolidation

Feature F260, session 7, round 20. Base for this round:
`a3b89f3c0a3476a6850c87f591d400e7fc70ed28`, read from `git rev-parse` and equal to
`origin/feature/f260-one-world`. Frame convention: NO runs of repeated characters;
slice delimiters are the single lines `<<<BEGIN name>>>` and `<<<END name>>>`.

## Goal

The content half of the closure sequence, so that part 2 can build the review zip
from a clean tree with every content commit already in. Three pieces of work,
none of them bookkeeping:

1. the §3 pre-emission checklist gets its ONE consolidation pass, which operator
   amendment amend0827-process-diet rule 4 mandates exactly once per feature and
   only inside the closure sequence, and which may not lengthen the list;
2. the self-use track's next item is generated and RUN, which is closure
   precondition 6, and every defect its own reader reports is captured;
3. round 19's integration-gate verdict and one reviewer prose slip are booked.

The STATUS flip, the README sync, the ledger rotation, the evidence job, the
review zip and the pull request are all part 2 and part 3. NOTHING here touches
`docs/roadmap/STATUS.md` or `README.md`.

## Bundle, in this exact order

- C0a — save this block verbatim to `.agent/authored/f260-r20.md`
- C0b — mirror the same source file to `.agent/last_block.md`
- C1 — `.agent/plan.md`, whole-file replacement from the PLAN slice
- C2 — `.agent/live_review.md` gains GATE_R19; `.agent/prose_slips.md` gains
  SLIP25 — ONE commit, in that file order
- C3 — `docs/agents/planner_reviewer_prompt.md`: the consolidation, four pairs
- C4 — the self-use item: generate, run, record (see "The self-use item")
- C5 — rewrite `.agent/handoff.md` as the handback

## Change set — no path outside this list may be written

`.agent/authored/f260-r20.md` (C0a) · `.agent/last_block.md` (C0b) ·
`.agent/plan.md` (C1) · `.agent/live_review.md` and `.agent/prose_slips.md` (C2) ·
`docs/agents/planner_reviewer_prompt.md` (C3) · `scripts/self_use_queue.json` and
`.agent/selfuse_f260/` (C4) · `.agent/handoff.md` (C5)

## Constraints

1. Apply every slice BYTE FOR BYTE. If a slice or a gate looks wrong, apply it as
   written and DECLARE the problem in the handback. Never adjust a slice, a test
   or a gate to make a reading come out as ordered.
2. TERMINAL BYTES, measured by the reviewer at `a3b89f3c`:
   `.agent/live_review.md` 969325 bytes ending in exactly ONE newline;
   `.agent/prose_slips.md` 123846 bytes ending in exactly ONE newline. Derive each
   recipe from its own target's measured terminal byte and `assert` before writing.
3. Every pair is applied with `str.replace(FROM, TO, 1)` AFTER asserting the FROM
   occurs EXACTLY ONCE in the file. All four C3 pairs were measured by the
   reviewer at FROM exactly 1.
4. Do NOT author a `Done:` or `Landed:` paragraph, and do NOT mint an R-id. If the
   self-use run reports defects, REPORT THE STRINGS VERBATIM in the handback; the
   reviewer authors the findings and they are registered in the next round's first
   commit. A worker-authored finding is itself a finding.
5. Do NOT set `consumed_by` this round. Closure precondition 6 requires that edit
   in the CLOSURE commit, which is part 3's.
6. `cmp` and the `remedy` binary are denied in this sandbox: use
   `filecmp.cmp(shallow=False)` plus sha256, and `python3 -m apps.cli.grouped`.
   Take exit codes from `subprocess.run(...).returncode`; the bash guard rejects
   `$?`, `$( )`, `cp` and shell loop forms BY FORM and rejects environment
   assignments on the command line — pass `env=`. Scratch lives under the
   gitignored `.remedy-wt/` and is never `git add`ed.
7. `.agent/STOP` does not exist at `a3b89f3c`. If it appears, finish the commit in
   flight, hand off and end. Do not delete it, do not commit it.
8. The handback cannot table its own commit (the R-0149 pattern). Report C5's own
   numbers nowhere. Create no pull request, merge nothing, never force-push,
   never work on `main`.

## The consolidation (C3) — what it does and why in this direction

Operator amendment amend0827-process-diet rule 4: the list is FROZEN while a
feature is open, consolidation happens EXACTLY ONCE per feature inside the closure
sequence, and the list must come out the SAME LENGTH OR SHORTER. It stands at 36
items, running 1 to 31 and 33 to 37 — the reviewer counted them mechanically. This
pass merges ITEM 19 INTO ITEM 31, leaving 35.

They are one rule about two artefacts. Item 19 says an authored SLICE may claim a
gate's result only when the block schedules that gate before the commit writing
the slice; item 31 says the same of the HANDBACK. Same defect, same
counter-measure, same finding family — item 19 cites R-0515 and names "the R-0371
and R-0449 family", and item 31 cites R-0449 and R-0494.

THE DIRECTION IS MEASURED, NOT PREFERRED. A merged number is retired and never
reused, and the survivors are never renumbered, because the append-only record
cross-references these items by number. The reviewer counted those references:
`item 31` occurs 14 times in `.agent/live_review.md`, 12 times in
`.agent/live_review_archive.md` and 5 times in `.agent/prose_slips.md` — 31
references that cannot be corrected — while `item 19` occurs ZERO times in all
three and exactly ONCE in the checklist file itself, inside item 20's neighbour
paragraph, which pair CONS4 updates. Retiring 31 would strand 31 landed
references; retiring 19 strands none. F259's pass merged the higher number into
the lower; this one merges the lower into the higher, for the reason the rule
itself gives.

## The self-use item (C4) — closure precondition 6

`scripts/self_use_queue.json` holds ten items and NO pending one; the reviewer
confirmed `packages.orchestration.self_use_queue.next_self_use_item()` answers
`None`, and separately that
`packages.orchestration.self_use_generator.generate_self_use_item()` — the SEARCH
half, which writes nothing, proved by the queue's sha256 being identical before
and after the call — would offer `SU-011`, "Address ledger finding R-0419", from
its tier-1 ledger scan. Precondition 6 therefore requires
`generate_and_append_if_empty()` FIRST. Run it, report the entry it appended, and
then:

- (i) `packages.orchestration.self_use_runner.run_next_self_use_item(dest_dir=<a
  directory under the gitignored .remedy-wt/>, repo_path='.')` — take its defaults
  for `max_provider_calls`, `max_cost_usd` and `max_tasks`. Report the returned
  entry id, the path, and the JobPlan's id and status. The dest_dir is scratch and
  is NEVER committed.
- (ii) `packages.orchestration.self_use_findings.describe_self_use_run_defects`
  for that run's own `JobPlan`. Report EVERY string it returns, verbatim and
  complete, never truncated. An empty tuple means nothing to register — report the
  empty tuple EXPLICITLY, because "nothing was returned" and "nothing was checked"
  must not look the same.
- (iii) Write the run's record into `.agent/selfuse_f260/`, matching the shape of
  the precedent directory `.agent/selfuse_f259/`: the generated job markdown as
  `<entry id>.md`, and `run.txt` carrying the commands, the JobPlan id and status,
  the defect strings from (ii), and the budgets that were in force.

The self-use RUN is a real job execution with a real budget; let it run to its own
completion rather than interrupting it. If the runner RAISES, commit nothing for
C4, record the full traceback in the handback, and continue to C5 — a failed
self-use run is REPORTED, never hidden, and the reviewer decides what it means.

## The pairs for C3, in `docs/agents/planner_reviewer_prompt.md`

Each was measured at FROM exactly 1, and each reads `TO contains FROM: false`
⇒ REWRITE, so every FROM count after its edit must be 0.

CONS1 — remove item 19. Its FROM ends with item 20's opening line so that the
deletion is anchored on both sides and cannot consume a neighbour.
<<<BEGIN CONS1_FROM>>>
  19. **A claim about a gate's result names the commit that runs the gate.** Finding
      R-0515. An authored slice may state what a gate showed only when the same block
      fixes that the gate runs BEFORE the commit that writes the slice. Otherwise the
      worker must either reorder the round on its own initiative or commit a claim it
      has not verified, and the second puts a false line into the permanent record.
      Item 13 governs the ORDER a block imposes on the worker's runs and item 14 which
      commits a per-commit gate can honestly reach; this one governs a slice's TEXT
      making a claim whose producer the block never scheduled — the R-0371 and R-0449
      family, narrowed from commit SHAs to gate results. The R22 instance: DONE1
      asserted a probe outcome while the block listed its gates after its commits, and
      only the worker's own reordering kept the record true.
  20. **A slice states a fact about a file the same block edits only with the commit
<<<END CONS1_FROM>>>
<<<BEGIN CONS1_TO>>>
  20. **A slice states a fact about a file the same block edits only with the commit
<<<END CONS1_TO>>>

CONS2 — item 31 absorbs item 19's rule, and its heading widens from the handback
to any artefact that quotes a gate.
<<<BEGIN CONS2_FROM>>>
  31. **A gate whose reading the handback must carry runs at a commit STRICTLY
      EARLIER than the handback commit.** Findings R-0449 and R-0494. When a block
<<<END CONS2_FROM>>>
<<<BEGIN CONS2_TO>>>
  31. **A gate whose reading an authored text must carry runs at a commit STRICTLY
      EARLIER than the commit that writes that text.** Findings R-0449, R-0494 and
      R-0515. This item absorbed former item 32-neighbour ITEM 19 at F260's closure
      on 2026-09-06; 19 is RETIRED and never reused. The two were one rule about two
      artefacts, and the merged form states it once: an authored text may claim what
      a gate showed only when the same block fixes that the gate runs BEFORE the
      commit writing that text. THE SLICE HALF, formerly item 19 and finding R-0515:
      an authored slice bound for the permanent record may state a gate's result only
      under that scheduling, because otherwise the worker must either reorder the
      round on its own initiative or commit a claim it has not verified, and the
      second puts a false line into a file nothing can correct. The R22 instance:
      DONE1 asserted a probe outcome while the block listed its gates after its
      commits, and only the worker's own reordering kept the record true. THE
      HANDBACK HALF, formerly the whole of this item. When a block
<<<END CONS2_TO>>>

CONS3 — the preamble records this pass and re-bases the figure the NEXT one
measures against.
<<<BEGIN CONS3_FROM>>>
  Consolidated once, at F259's closure on 2026-09-06: item 32 was merged into item
  16, whose family it belonged to and which its own text named, leaving 36 items.
  A merged item's NUMBER IS RETIRED AND NEVER REUSED, and the survivors are NEVER
  RENUMBERED, so this list now runs 1 to 31 and 33 to 37. The reason is that
  `.agent/live_review.md` is append-only and cross-references these items by
  number from dated entries that cannot be corrected: renumbering would silently
  re-point every one of those references at a different rule, which is a worse
  failure than a gap in the numbering. The next consolidation measures against 36.
<<<END CONS3_FROM>>>
<<<BEGIN CONS3_TO>>>
  Consolidated at F259's closure on 2026-09-06: item 32 was merged into item
  16, whose family it belonged to and which its own text named, leaving 36 items.
  Consolidated again at F260's closure on 2026-09-06: item 19 was merged into item
  31, the same rule about a second artefact, leaving 35 items.
  A merged item's NUMBER IS RETIRED AND NEVER REUSED, and the survivors are NEVER
  RENUMBERED, so this list now runs 1 to 18, 20 to 31 and 33 to 37. The reason is that
  `.agent/live_review.md` is append-only and cross-references these items by
  number from dated entries that cannot be corrected: renumbering would silently
  re-point every one of those references at a different rule, which is a worse
  failure than a gap in the numbering. That reason also fixes the DIRECTION of a
  merge, which F260's pass measured rather than assumed: `item 31` had 31 landed
  references across the record and its archive and the prose slips, and `item 19`
  had none, so 19 was the number that could be retired without stranding one.
  The next consolidation measures against 35.
<<<END CONS3_TO>>>

CONS4 — item 20's neighbour paragraph, the one place in this file that cites the
retired number.
<<<BEGIN CONS4_FROM>>>
      at emission and item 19 governs a claim about a GATE's result; this one governs a
<<<END CONS4_FROM>>>
<<<BEGIN CONS4_TO>>>
      at emission and item 31 governs a claim about a GATE's result; this one governs a
<<<END CONS4_TO>>>

## The slices

<<<BEGIN PLAN>>>
# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, `origin/main` merged in at round 16. Rounds 1 to
19 are reviewed; round 1 FAILED and was repaired, and 2 to 19 PASSED. DECISION
F260 D8 closes this feature at the scope it built; F272 carries the remainder and
was registered in round 18, directly after F260 in the ledger.

## Goal

Session 7 performs SPLIT-AND-CLOSE at the amend0905-throughput soft limit of 7
sessions. The split is ruled and registered, and round 19's integration gate was
GREEN on both sides with both comparison sets empty, which satisfies closure
precondition 2. What remains is the closure sequence itself.

## Current Step

Round 20 is CLOSURE PART 1, the content half: the §3 checklist's one mandated
consolidation pass, the self-use item generated and run for closure precondition
6, and round 19's verdict booked. It touches neither `docs/roadmap/STATUS.md` nor
`README.md`.

## Next Steps

1. Closure part 2: any findings the self-use run reported are registered first;
   then the evidence job, the review zip, and the ledger rotation.
2. Closure part 3: the STATUS accepted flip, the README sync, `consumed_by` set on
   the self-use item, the handback, and the pull request — left UNMERGED as the
   operator's review window.

## Risks

- The self-use run is a real job execution against a real budget. If it raises,
  that is reported with its full traceback and the reviewer rules on it; it is
  never hidden and never retried into silence.
- The consolidation may not lengthen the list. It merges two items into one and
  re-bases the figure the next pass measures against, in the same commit.
<<<END PLAN>>>
<<<BEGIN GATE_R19>>>
Gate: R19 — the F260 R19 entry, THE INTEGRATION GATE (docs/agents/integration_gate.md). VERDICT PASS, AND THE GATE IS GREEN ON BOTH SIDES WITH BOTH COMPARISON SETS EMPTY. Range `d4f1a55c1aa4e6315e1b52d573f1847308832d90`..`a3b89f3c`, six commits, every one single-parent, in exactly the bundle's ordered sequence C0a, C0b, C1, C2, C3, C4; insertion counts 236, 163, 19, 2 and 46 for the five before the handback. THE REVIEWER RAN BOTH SIDES OF THIS GATE ITSELF, which is what closure precondition 2 asks for, and the numbers below are the reviewer's own except where they are named as the worker's. BRANCH RUN, `python3 -m pytest -n auto -q` in the primary checkout: the reviewer measured exit 0, 19731 passed, 23 skipped, 158.5 seconds, ZERO lines beginning `FAILED`; the worker independently measured exit 0, 19731 passed, 23 skipped, 129.4 seconds, zero `FAILED`. The pass and skip counts are IDENTICAL across two independent runs on the same commit. Before that run the dist precondition was asserted rather than assumed, because a cold or stale `apps/ui/dist` reddens this suite for a reason that has nothing to do with the branch: `apps/ui/dist/index.html` exists and its mtime exceeds that of every one of the 142 files under `apps/ui/src`, the newest being `RemedyShell.tsx`. BASE RUN at the merge base `f957c4c6dede34e9ba9d3653ae01cc16157b96fc`, which is also the tip of `origin/main` because round 16 merged it in: the reviewer built its own disposable worktree ON A BRANCH — never detached, because the self-dogfood guard refuses a detached checkout by design — restored parity, and measured exit 0, 19694 passed, 23 skipped, 182.9 seconds, ZERO `FAILED`; the worker measured exit 0, 19694 passed, 23 skipped, 150.2 seconds, zero `FAILED`. Again identical counts from two independent runs. The base collects 37 fewer tests than the branch, which is the shape F260's own added tests predict. PARITY WAS RESTORED IN THREE STEPS, ALL THREE MEASURED, and two of them are not in the canonical procedure at all. `shutil.copytree` was called with `symlinks=True` for both `apps/ui/node_modules` and `apps/ui/dist`; the reviewer counted 23 symlinks under `.bin` in the primary and 23 in the copy, so finding R-0591's dereferencing class did not recur. The copied `dist` mtimes were then advanced past every file under that worktree's own `apps/ui/src`, and the staleness was REAL before the advance rather than hypothetical — the reviewer measured the copied build as stale against the fresh checkout, and the worker measured the gap at 632357.8 seconds — which is finding R-0736 confirmed live at this merge base for the third time. The repair was then proved by IMPORTING AND CALLING the real `_frontend_is_stale` from the BASE worktree's own `ui_server.py`, with its `__file__` confirmed to resolve inside that worktree, and it answered False before the run started. THE COMPARISON, which is what the gate exists to produce: `comm -13` and `comm -23` over the two sorted failure lists are BOTH EMPTY — zero branch-only ids and zero base-only ids — so no id was owed an attribution and none was invented. Both committed evidence files are 0 bytes and both captured tails are committed beside them under `.agent/gate_f260_r19/`, all named `.txt` and never `.log`. Only the round's own worktree existed and it was removed by exact path and pruned, its temporary branch deleted, leaving 12 `git worktree list` rows — the primary and the eleven pre-existing `remedy/job-*` — and no `tmp/*` branch; the reviewer's own worktree was likewise removed by exact path and its branch deleted. `git status --porcelain` EMPTY and `git ls-files .remedy-wt` EMPTY at the verdict. CENSUS: `^Gate: ` 28 with `^Gate: R18 — ` at exactly 1; registrations 301 over 301 DISTINCT ids; `^Done: ` 5 lines over THREE distinct ids; OPEN SET 298 BY DISTINCT ID, unchanged. EIGHT ITEMS WERE DECLARED AND ALL EIGHT ARE UPHELD, and ONE OF THEM IS A REAL DEFECT THE ROUND FOUND IN THE REVIEWER'S OWN PARITY RECIPE, which the reviewer then reproduced independently. The recipe stamps the copied `dist` to the base worktree's newest source mtime plus sixty seconds; because that source stamp is itself the fresh checkout time, the stamped value lands INSIDE the wall-clock window of the run that follows, and the R-0444 clause of the canonical procedure — "ANY mtime falling inside the run window voids the parity claim" — therefore trips on every gate that applies the repair correctly. The worker supplied the discriminator that separates the two readings, and the reviewer measured the same thing in its own worktree: all four `dist` files have before-mtime EQUAL to after-mtime, so ZERO files changed during either run, while all four VALUES fall inside the window. Nothing rebuilt; the check is reading the repair rather than a rebuild. The parity claim is reported VOID as the procedure literally requires, and it changed no verdict, because both comparison sets are empty and no attribution depended on it. This is fresh evidence for the OPEN finding R-0736 rather than a new id, per §3 item 30: R-0736 already owns the gap between what `docs/agents/integration_gate.md` step 3 says and what `_frontend_is_stale` actually reads, and its resolution must now also narrow the void-check from "a value falling inside the window" to "a value that CHANGED between the before and after censuses" — otherwise fixing R-0736 by adding the mtime advance to the doc would guarantee the void on every future gate.
<<<END GATE_R19>>>
<<<BEGIN SLIP25>>>
2026-09-06 · F260 R19 (reviewer) · The round-19 block ordered the integration gate's parity repair as "raise `dist/index.html`'s mtime above every file under THAT WORKTREE's `apps/ui/src`" and, in the same gate, ordered the canonical R-0444 check that "ANY mtime falling inside the run window VOIDS the parity claim". Those two clauses cannot both be satisfied: the worktree's newest source stamp IS the fresh checkout time, so a repair anchored on it necessarily produces a dist mtime seconds away from "now", which then falls inside the window of the run that follows. The worker declared it and supplied the discriminator; the reviewer reproduced it independently, measuring zero of four dist files CHANGED across the run while all four VALUES sat inside the window. THE LESSON is checklist item 18's shape — a recipe and the property it is ordered to establish must be read against each other — reaching a case where the recipe is correct, the check is correct, and only their COMPOSITION is unsatisfiable: whenever a block orders both a repair and a check over the same observable, it composes them on the page before emitting, and prefers a discriminator that measures the EVENT (did this value change?) over one that measures a COINCIDENCE (is this value near now?). Nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result and the gate's verdict did not depend on it, so no id is spent (amend0827-process-diet rule 2); the durable half is recorded as fresh evidence against the open finding R-0736.
<<<END SLIP25>>>

## Done when — the gates. Report ONE LINE PER GATE with its REAL exit code.

**G1 TRANSPORT.** Before staging C0a, sha256 over the delegation's source file,
`.agent/authored/f260-r20.md` and `.agent/last_block.md`; all three equal the
digest the delegation names. Both writes `shutil.copyfile`, each proved with
`filecmp.cmp(shallow=False)`.

**G2 THE RECORD, at C2.** For `.agent/live_review.md`: (a) exact image —
`post == pre + b"\n" + GATE_R19 + b"\n"` True and `post[:len(pre)] == pre` True,
both byte counts reported; (b) structural, independent of (a) — split the WHOLE
file on a blank line and compare the last N units against the slice's N
paragraphs IN ORDER, N counted by your script from the slice; (c) negative
control IN MEMORY on a `bytes` object, flipping one byte inside the FIRST
appended paragraph: both readers REJECT, then both ACCEPT after restore, with the
restored image equal to the disk image. For `.agent/prose_slips.md`, byte
equality is enough: `post == pre + b"\n" + SLIP25 + b"\n"` True, with byte counts
and unit counts before and after.

**G3 THE PLAN, at C1.** `.agent/plan.md` equals the PLAN slice plus exactly one
trailing newline. Report byte count and line count; under the 50-line cap, and
carrying `## Goal` and `## Next Steps`.

**G4 THE CONSOLIDATION, at C3.** For CONS1 to CONS4 report FOUR numbers each:
FROM count BEFORE (1); the containment reading printed as `true` or `false`; FROM
count AFTER (0 for all four); TO count AFTER (1). Then reconstruct
`docs/agents/planner_reviewer_prompt.md` INDEPENDENTLY from its pre-edit bytes
with only those four pairs applied, and report the boolean, the byte count before
and after, and that the file still ends with exactly one newline.

**G5 THE LIST IS SHORTER, AND ITS NUMBERING IS WHAT THE PREAMBLE SAYS.** After C3,
count the checklist items MECHANICALLY — the lines matching `^  \d+\. \*\*` between
the line beginning `  1. **Size.**` and the line beginning
`  Why this is on disk and not a habit` — and report the sorted list of their
numbers, the count, and the sorted gaps in `range(1, 38)`. The count must be 35,
and the gaps must be EXACTLY `[19, 32]`.

The string `item 19` does NOT go to zero and must not be gated at zero: the
consolidation deliberately keeps PROVENANCE references to the retired number.
Report the count and the containing line of each. The reviewer simulated the four
pairs before emitting and measured THREE — two in the consolidation preamble and
one inside item 31's absorbed text, each naming 19 as a retired predecessor. What
must be ZERO is a LIVE cross-reference: report that no line matching `^  19\. \*\*`
survives anywhere in the file, which is the item itself being gone.

**G6 THE SELF-USE ITEM, at C4.** Report, in this order: `next_self_use_item()`
BEFORE the generator, which must be `None`; the entry
`generate_and_append_if_empty()` appended, with its id, title and `provenance`,
and that its `consumed_by` is the empty string; the queue's entry count before and
after, and that the count of entries with an empty `consumed_by` goes 0 to 1; the
runner's returned entry id, the dest path, and the JobPlan's id and status; EVERY
string `describe_self_use_run_defects` returns, verbatim, complete and never
truncated, or the EXPLICIT empty tuple; and the listing of `.agent/selfuse_f260/`
with byte counts. If the runner raised, report the full traceback instead and say
so plainly.

**G7 THE SUITES, run SERIALLY in the PRIMARY checkout, after C4.** Report each
real exit code and pass count:

    python3 -m pytest tests/docs/ -q -p no:randomly
    python3 -m pytest tests/orchestration/test_self_use_generator.py -q -p no:randomly
    python3 -m pytest tests/cli/test_golden_path.py -q -p no:randomly
    python3 -m apps.cli.grouped integrity check --json

The integrity check must report `"passed": true` with `"fail_count": 0`. Report
any `^FAILED` or `^ERROR` lines; there must be none.

**G8 TREE AND STRUCTURE.** `git status --porcelain` EMPTY; `git ls-files
.remedy-wt` EMPTY; every commit C0a through C4 single-parent with its parent count
reported; each of their INSERTION counts — the `+` column of `git diff --numstat`,
never insertions plus deletions — reported and under 500. Count the `.py` files in
`git diff --name-only a3b89f3c..C4` yourself; if there are none, report the lint
half as not applicable rather than inventing a target.

## Handback

Rewrite `.agent/handoff.md`. Mandated sections: the Session block naming SESSION 7
of F260, round 20, rounds so far 20; a one-sentence context self-assessment; the
Range; the per-commit table with `+/-` from `git log --numstat`, never re-derived
by eye; External actions; Verification, one line per gate with its real exit code;
the COMPLETE self-use transcript of G6; the Authored-text proofs; Deviations and
assumptions; the Item-status table with every bundle item and every gate appearing
exactly once as `done`, `skipped` or `deviated` with a reason; Open findings; and
Next. Then `git push -u origin feature/f260-one-world`.
