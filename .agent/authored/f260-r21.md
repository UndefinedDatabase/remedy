# STEP — F260 round 21: book round 20, register the self-use recurrence, repair one landed phrase

Feature F260, session 7, round 21. Base for this round:
`addca04a` — the eight-character prefix the reviewer READ from `git rev-parse`
output; resolve it yourself and report the full object id rather than taking a
long form from this block. It equals `origin/feature/f260-one-world`. Frame
convention: NO runs of repeated characters; slice delimiters are the single lines
`<<<BEGIN name>>>` and `<<<END name>>>`.

## Goal

Three things, and then this SESSION ends with its handoff — the closure's evidence
job, review zip, ledger rotation, STATUS flip and pull request are the NEXT
session's, and the handback says so in full.

1. Book round 20's PASS verdict.
2. Discharge closure precondition 6's registration obligation for the self-use run
   round 20 executed. It ended BLOCKED and its reader returned two strings; those
   are NOT a new finding — the open set already holds `R-0784` describing exactly
   this defect, so the evidence is added there as a RECURRENCE, per §3 item 30.
3. Repair one garbled phrase this reviewer's round-20 slice landed in
   `docs/agents/planner_reviewer_prompt.md`. It is the one KNOWN defect on disk and
   it is not being carried across a session boundary.

## Bundle, in this exact order

- C0a — save this block verbatim to `.agent/authored/f260-r21.md`
- C0b — mirror the same source file to `.agent/last_block.md`
- C1 — `.agent/plan.md`, whole-file replacement from the PLAN slice
- C2 — `.agent/live_review.md` gains GATE_R20 then RECUR784, in that order;
  `.agent/prose_slips.md` gains SLIP26 — ONE commit, live_review first
- C3 — `docs/agents/planner_reviewer_prompt.md`: the FIXPAIR
- C4 — rewrite `.agent/handoff.md` as the handback AND the session handoff

## Change set — no path outside this list may be written

`.agent/authored/f260-r21.md` (C0a) · `.agent/last_block.md` (C0b) ·
`.agent/plan.md` (C1) · `.agent/live_review.md` and `.agent/prose_slips.md` (C2) ·
`docs/agents/planner_reviewer_prompt.md` (C3) · `.agent/handoff.md` (C4)

`docs/roadmap/STATUS.md`, `README.md` and `scripts/self_use_queue.json` are NOT
touched. No evidence job is run, no review zip is built and NO LEDGER ROTATION is
performed this round — all four belong to the next session's closure parts 2 and 3.

## Constraints

1. Apply every slice BYTE FOR BYTE. If a slice or a gate looks wrong, apply it as
   written and DECLARE the problem in the handback. Never adjust a slice, a test
   or a gate to make a reading come out as ordered.
2. TERMINAL BYTES, measured by the reviewer at `addca04a`:
   `.agent/live_review.md` 974830 bytes ending in exactly ONE newline;
   `.agent/prose_slips.md` 125380 bytes ending in exactly ONE newline. Derive each
   recipe from its own target's measured terminal byte and `assert` before writing.
3. C2 appends TWO paragraphs to `.agent/live_review.md` — GATE_R20 FIRST, then
   RECUR784 — and one to `.agent/prose_slips.md`, in ONE commit, live_review
   written first.
4. RECUR784 is a RECURRENCE paragraph against an already-open finding. It mints NO
   new id, and you author no `Done:` and no `Landed:` line. The open set stays at
   298 by distinct id.
5. FIXPAIR is applied with `str.replace(FROM, TO, 1)` after asserting the FROM
   occurs EXACTLY ONCE. The reviewer measured it at 1.
6. `cmp` and the `remedy` binary are denied in this sandbox: use
   `filecmp.cmp(shallow=False)` plus sha256, and `python3 -m apps.cli.grouped`.
   Take exit codes from `subprocess.run(...).returncode`; the bash guard rejects
   `$?`, `$( )`, `cp` and shell loop forms BY FORM and rejects environment
   assignments on the command line — pass `env=`. Scratch under the gitignored
   `.remedy-wt/`, never `git add`ed.
7. `.agent/STOP` did not exist at `addca04a`. If it appears, finish the commit in
   flight, hand off and end. Do not delete it, do not commit it.
8. The handback cannot table its own commit (the R-0149 pattern). Report C4's own
   numbers nowhere. Create no pull request, merge nothing, never force-push,
   never work on `main`.

## The repair (C3)

Round 20's CONS2 slice landed the phrase "former item 32-neighbour ITEM 19" in the
§3 checklist. It is wrong and it is the reviewer's error: item 19 sat between 18
and 20, and 32 is the number F259's consolidation retired, so the phrase welds two
unrelated facts into a description of neither. The worker applied it byte for byte
as constraint 1 required and declared it, which was correct. `planner_reviewer_prompt.md`
is a LIVING document, not the append-only record, so this is repaired in place
rather than corrected by a later dated sentence — the rule against rewriting
landed text binds `.agent/live_review.md` and its archive, and does not reach here.

FIXPAIR — `TO contains FROM: false` ⇒ REWRITE, so the FROM count after must be 0.
<<<BEGIN FIXPAIR_FROM>>>
      R-0515. This item absorbed former item 32-neighbour ITEM 19 at F260's closure
      on 2026-09-06; 19 is RETIRED and never reused.
<<<END FIXPAIR_FROM>>>
<<<BEGIN FIXPAIR_TO>>>
      R-0515. This item absorbed ITEM 19 at F260's closure on 2026-09-06, and the
      number 19 is RETIRED and never reused.
<<<END FIXPAIR_TO>>>

## The slices

<<<BEGIN PLAN>>>
# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, `origin/main` merged in at round 16. Rounds 1 to
20 are reviewed; round 1 FAILED and was repaired, and 2 to 20 PASSED. DECISION
F260 D8 closes this feature at the scope it built; F272 carries the remainder and
was registered in round 18, directly after F260 in the ledger.

## Goal

Session 7 performs SPLIT-AND-CLOSE at the amend0905-throughput soft limit of 7
sessions. The split is RULED and REGISTERED, the integration gate was GREEN on both
sides with both comparison sets empty, the §3 checklist has had its one mandated
consolidation pass, and closure precondition 6's self-use item has been generated
and run. What remains is the closure's evidence half.

## Current Step

Round 21 books round 20, registers the self-use run's outcome as a RECURRENCE of
the open finding R-0784 rather than a new id, and repairs one garbled phrase the
reviewer's round-20 slice landed in the §3 checklist. THIS SESSION ENDS AFTER IT.

## Next Steps

1. CLOSURE PART 2, first commit: book round 21's verdict. Then the evidence job
   (`create_manual_completion_bundle(review_feature_id='f260', ...)`), the review
   zip from a clean tree, and `python3 scripts/rotate_live_review.py` as its OWN
   commit — after the bookings and before the STATUS flip.
2. CLOSURE PART 3: the STATUS `[x]` flip and the README sync in ONE commit, with
   `consumed_by` set to `F260` on SU-011 in that same commit, then the handback,
   then the pull request — left UNMERGED as the operator's review window.

## Risks

- The self-use queue's SU-011 is PENDING and must be marked consumed in the
  closure commit, not before. Nothing else may set it.
- The ledger rotation re-bases every byte baseline, so the block after it measures
  its own terminal bytes rather than reusing any number from this session.
<<<END PLAN>>>
<<<BEGIN GATE_R20>>>
Gate: R20 — the F260 R20 entry, CLOSURE PART 1. VERDICT PASS. Range `a3b89f3c0a3476a6850c87f591d400e7fc70ed28`..`addca04a`, seven commits, every one single-parent, in exactly the bundle's ordered sequence C0a, C0b, C1, C2, C3, C4, C5 with nothing added, dropped or reordered; insertion counts 346, 285, 20, 4, 24 and 133 for the six before the handback, every one far under the 500 cap. The reviewer re-ran every gate itself. TRANSPORT: the reviewer's scratchpad original, the committed `.agent/authored/f260-r20.md` and `.agent/last_block.md` are all 26833 bytes and all hash to `e83dbaad265b6fe1a130f2c9b6e692d35ff3c87ae495d891f6b90273721a06c6`; per §3 item 37 that chain covers the scratch file, the saved copy and the mirror, and is not a claim about the bytes emitted into a prompt. THE RECORD: `.agent/live_review.md` 969325 to 974830 bytes and `.agent/prose_slips.md` 123846 to 125380 bytes, each equal to its pre-image plus its own recipe exactly and each with the pre-image a byte-exact prefix; `.agent/plan.md` equals its slice plus one newline at 1666 bytes and 36 lines. THE CONSOLIDATION, which operator amendment amend0827-process-diet rule 4 mandates exactly once per feature and only inside the closure sequence, IS DONE AND IS SHORTER: `docs/agents/planner_reviewer_prompt.md` went 92039 to 92539 bytes under four pairs, each measured FROM exactly 1 before and 0 after with `TO contains FROM: false`, and the reviewer reconstructed the whole file INDEPENDENTLY from its pre-edit bytes with only those four applied and found it byte-equal to the committed result. Counted mechanically on the COMMITTED file, the list now holds 35 items with gaps at exactly 19 and 32, and no line matching a numbered item 19 survives anywhere. ITEM 19 WAS MERGED INTO ITEM 31 and 19 is retired. The direction was MEASURED rather than preferred, which is the part worth recording: a merged number is retired and never reused because the append-only record cross-references these items by number, and the reviewer counted those references before choosing — `item 31` occurs 14 times in `.agent/live_review.md`, 12 in `.agent/live_review_archive.md` and 5 in `.agent/prose_slips.md`, 31 landed references that cannot be corrected, while `item 19` occurs ZERO times in all three and exactly once in the checklist file itself, which the fourth pair updated. Retiring 31 would have stranded 31 references; retiring 19 stranded none. Three `item 19` mentions survive in the file by design and were reported as such — two in the consolidation preamble and one inside item 31's absorbed text — and they are PROVENANCE for a retired number, not live cross-references. CLOSURE PRECONDITION 6: `next_self_use_item()` answered `None` beforehand over ten entries with none pending, so the generator ran first and appended `SU-011`, "Address ledger finding R-0419", provenance `generated (self-use-generator tier 1, ledger scan, R-0419)`, with an empty `consumed_by`; the queue went 10 entries to 11 and its empty-`consumed_by` count 0 to 1, and `consumed_by` was correctly NOT set this round, which is the closure commit's edit. The run itself is recorded under `.agent/selfuse_f260/` as `SU-011.md` and `run.txt`. IT ENDED BLOCKED, WHICH IS REPORTED AND NOT HIDDEN: JobPlan `101fad068c0741f4`, status `blocked`, T001 `repair_exhausted` with a failing reviewer verdict after both repair rounds and a zero-byte result diff, in 96.5 seconds against the ollama roles. The runner did not raise; `blocked` is its documented normal-gate outcome, which is why the round committed its record. The two strings its reader returned are registered as a RECURRENCE of the open finding `R-0784` in the paragraph that follows this one, not as a new id. SUITES re-run by the reviewer: `tests/docs/` exit 0 at 303 passed, `tests/orchestration/test_self_use_generator.py` exit 0 at 20 passed, the canary exit 0 at 42 passed, and the integrity check exit 0 with `"passed": true` and `"fail_count": 0`. The reviewer had additionally simulated all four consolidation pairs before emitting the block and measured the resulting list at 35 with gaps 19 and 32, and had verified separately that the generator's SEARCH half writes nothing, by comparing the queue's sha256 before and after calling it. CENSUS: `^Gate: ` 29 with `^Gate: R19 — ` at exactly 1; registrations 301 over 301 DISTINCT ids; OPEN SET 298 BY DISTINCT ID, unchanged. SEVEN ITEMS WERE DECLARED AND ALL SEVEN ARE UPHELD, and two of them are the round doing better than the block asked. The worker found that its own draft of `run.txt` had inherited a job-record path from the F259 precedent directory that NO LONGER EXISTS — `.data/task_jobs/<id>/job.json`, which this very feature moved — and repaired it by calling the product resolver `data_paths.job_record_path` before staging, rather than copying a dead path forward; the stale path still stands in `.agent/selfuse_f259/run.txt`, which is outside this round's change set and is left alone. And the worker rejected its own first structural reader rather than the file, when that reader read False because it had not stripped the units' surrounding newlines: it fixed the READER, re-ran against the on-disk image, and the negative control still rejected. ONE DEFECT LANDED, AND IT IS THE REVIEWER'S. The CONS2 slice carried the phrase "former item 32-neighbour ITEM 19", which is wrong twice over — item 19 sat between 18 and 20, and 32 is the number F259 retired — so the phrase welds two unrelated facts into a description of neither. The worker applied it byte for byte as constraint 1 requires and declared it, which is exactly right. It is repaired in place by round 21, because `docs/agents/planner_reviewer_prompt.md` is a living document and the rule against rewriting landed text binds the append-only record and does not reach it.
<<<END GATE_R20>>>
<<<BEGIN RECUR784>>>
Recurrence: R-0784 — the same defect, at F260's closure, and this instance REFUTES the prediction the F259 instance closed with. Closure precondition 6 requires every string `packages.orchestration.self_use_findings.describe_self_use_run_defects` returns for the closing run to be registered before the close, and F260 R20's run of `SU-011` returned two: `job 101fad068c0741f4 (blocked): task_T001_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail` and `T001 (blocked): completion_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail`. These are the SAME defect `R-0784` already holds open — the job-level and task-level views of one gate failure in a self-use run that exhausted its repair rounds — differing from the entries above only in the job id and the queue item. NO NEW ID IS MINTED, per §3 item 30: the reviewer searched the open set for the DEFECT before writing, found `R-0784` describing it in as many words, and `R-0784`'s own text already rules that the two strings are one defect and take one id. WHAT IS NEW, AND IT MATTERS MORE THAN THE REPEAT. The F259 instance recorded that six consecutive closures had drawn the same tier-1 item because the generator takes the OLDEST open Low or Medium ledger finding and that finding had been `R-0418` since F110; it then paid `R-0418` off by demonstrated compliance and predicted that "the generator's tier 1 will offer a DIFFERENT finding at the next closure". THE PREDICTION HELD AND THE LOOP DID NOT BREAK. Tier 1 did offer a different finding — this closure drew `R-0419` rather than `R-0418`, which the reviewer confirmed by calling the generator's write-free search half before the round and reading the entry it proposed — and the run blocked anyway, in the same way, for the same reason: `R-0419` is ALSO a REVIEWER-BLOCK DEFECT, a finding whose fix is a rule about what a block must contain, and no builder can perform it. Paying off the head of the queue moved the queue forward by exactly one item and changed nothing, because the ledger's oldest open Low and Medium findings are DENSELY populated with reviewer-practice entries. That is the measurement `R-0784`'s fix clause was missing: the remedy is not to retire findings one at a time until a code-shaped one surfaces, but the TIER-1 FILTER that clause already names as its first option — the generator must skip a finding whose fix binds the reviewer rather than the code, or must state that blocking on such an item is the intended outcome. Until it does, every closure will spend a real provider budget on a job that cannot succeed; this one spent 96.5 seconds and two repair rounds to produce a zero-byte diff. `R-0784` stays OPEN and its resolution condition is unchanged.
<<<END RECUR784>>>
<<<BEGIN SLIP26>>>
2026-09-06 · F260 R20 (reviewer) · The round-20 CONS2 slice described the checklist consolidation as absorbing "former item 32-neighbour ITEM 19", which is wrong twice over: item 19 sat between items 18 and 20 and was neighbour to neither 32 nor anything else numbered 32, and 32 is the number F259's OWN consolidation retired a feature earlier. The phrase welds two unrelated true facts into a description of neither, and it LANDED — the worker applied it byte for byte as constraint 1 requires and declared it, which was correct, and round 21 repaired it in place because `docs/agents/planner_reviewer_prompt.md` is a living document rather than the append-only record. THE LESSON is narrower than "check your prose": it is that a slice describing a change to a NUMBERED structure states the numbers it actually measured and nothing else. The reviewer had measured three real numbers for this pass — 19, 31 and 35 — and then reached for 32 from the paragraph immediately above, which belonged to a different feature's consolidation, because the two paragraphs sit adjacent and read alike. When two records of the same KIND sit side by side, the one being copied from is the likelier source of a wrong numeral than the one being written about; extract every numeral in such a slice back to the measurement that produced it before emitting.
<<<END SLIP26>>>

## Done when — the gates. Report ONE LINE PER GATE with its REAL exit code.

**G1 TRANSPORT.** Before staging C0a, sha256 over the delegation's source file,
`.agent/authored/f260-r21.md` and `.agent/last_block.md`; all three equal the
digest the delegation names. Both writes `shutil.copyfile`, each proved with
`filecmp.cmp(shallow=False)`. Also report the FULL object id the base prefix
`addca04a` resolves to.

**G2 THE RECORD, at C2.** For `.agent/live_review.md`, three readings:
(a) exact image — `post == pre + b"\n" + GATE_R20 + b"\n\n" + RECUR784 + b"\n"`
True and `post[:len(pre)] == pre` True; report both byte counts;
(b) structural, independent of (a) — split the WHOLE file on a blank line and
compare the last N units against the two slices' N paragraphs IN ORDER, where N is
counted by your script from the slices and is never a number this block asserts;
report units before and after, and that the last-but-one unit is GATE_R20 and the
last is RECUR784;
(c) negative control IN MEMORY on a `bytes` object, flipping one byte inside the
FIRST appended paragraph — that is GATE_R20, not RECUR784: both readers must
REJECT, then both ACCEPT after restore with the restored image equal to disk.
For `.agent/prose_slips.md`, byte equality is enough: `post == pre + b"\n" +
SLIP26 + b"\n"` True, with byte counts and unit counts before and after.

**G3 THE PLAN, at C1.** `.agent/plan.md` equals the PLAN slice plus exactly one
trailing newline. Report byte count and line count; under the 50-line cap, and
carrying `## Goal` and `## Next Steps`.

**G4 THE REPAIR, at C3.** Report FROM count before (1), the containment reading as
the word `true` or `false`, FROM count after (0) and TO count after (1). Then
reconstruct `docs/agents/planner_reviewer_prompt.md` independently from its
pre-edit bytes with only that pair applied and report the boolean, the byte count
before and after, and that it still ends with exactly one newline. Report that the
string `former item 32-neighbour` occurs ZERO times in the file afterwards — the
reviewer measured it at exactly 1 before — and that the checklist still counts 35
items with gaps at exactly 19 and 32, which the repair must not disturb.

**G5 THE OPEN SET DID NOT MOVE.** After C2, over `.agent/live_review.md`:
`^Gate: ` must read 30 and `^Gate: R20 — ` exactly 1; registrations
`^- R-\d{4} — ` must read 301 over 301 DISTINCT ids; `^Done: R-\d{4} — ` 5 lines
over 3 distinct ids; the OPEN SET BY DISTINCT ID must read 298. Also report that
`^Recurrence: R-0784` counts 2 — one from F259's closure and this round's — and
that the highest registered id is still `R-0816`, which is the proof that no new
id was minted.

**G6 THE SUITES, run SERIALLY in the PRIMARY checkout, after C3.** Report each
real exit code and pass count:

    python3 -m pytest tests/docs/ -q -p no:randomly
    python3 -m pytest tests/cli/test_golden_path.py -q -p no:randomly
    python3 -m apps.cli.grouped integrity check --json

The integrity check must report `"passed": true` with `"fail_count": 0`. Report
any `^FAILED` or `^ERROR` lines; there must be none.

**G7 TREE AND STRUCTURE.** `git status --porcelain` EMPTY; `git ls-files
.remedy-wt` EMPTY; every commit C0a through C3 single-parent with its parent count
reported; each of their INSERTION counts — the `+` column of `git diff --numstat`,
never insertions plus deletions — reported and under 500. Count the `.py` files in
`git diff --name-only addca04a..C3` yourself; if there are none, report the lint
half as not applicable rather than inventing a target.

**G8 THE SESSION HANDOFF IS COMPLETE.** This is the LAST round of session 7, so the
handback is also the session handoff and is gated as one. Report that
`.agent/handoff.md` after C4 contains, as literal text: the line
`SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE`; a section naming the
next session's FIRST action as re-reading `.agent/STOP` from disk (Phase 1 rule 1)
BEFORE the Open PR Gate (rule 2); the sentence that there is NO open pull request
for this branch and none may be created without an instruction; and the two
remaining closure parts named in order. Report the presence of each as a boolean.

## Handback — and the session handoff

Rewrite `.agent/handoff.md`. It carries the usual mandated sections: the Session
block naming SESSION 7 of F260, round 21, rounds so far 21; a one-sentence context
self-assessment; the Range; the per-commit table with `+/-` from
`git log --numstat`, never re-derived by eye; External actions; Verification, one
line per gate with its real exit code; the Authored-text proofs; Deviations and
assumptions; the Item-status table; Open findings; and Next.

Because this is the session's last round it ALSO carries the SCOPE REPORT operator
amendment amend0905-throughput requires at the soft limit: what F260 built, what
moved to F272, that the split was executed on the session's own authority under
DECISION F260 D8, and exactly what the closure still owes — parts 2 and 3 as the
PLAN slice's Next Steps name them. Include the banner line and the next-session
rule order that gate G8 measures.

Then `git push -u origin feature/f260-one-world`. Create NO pull request. Merge
nothing. Never force-push.
