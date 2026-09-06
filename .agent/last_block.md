# STEP — F260 round 17: rule the split, and state what F260 actually built

Feature F260 "One world: mission → job → run", session 7, round 17.
Base for this round: `867f34ae0c4632c961ad4a0dc9ef168d595606fc`, the branch tip,
which is the same object as `origin/feature/f260-one-world`.

Frame convention: this block uses NO runs of repeated characters. Slice
delimiters are the single lines `<<<BEGIN name>>>` and `<<<END name>>>`.

## Goal

Session 7 reaches the soft limit of operator amendment amend0905-throughput — 25
rounds or 7 sessions, whichever comes first. This round performs the first half of
the standing default: it RULES the split as a dated DECISION, books round 16's
verdict and the reviewer's own prose slips, and rewrites F260's feature file so it
states the scope F260 actually built and which slices move to the follow-up. The
follow-up's REGISTRATION — its detail file, its STATUS line, the README counters
and the `TOTAL_FEATURES` pin — is the NEXT round's, deliberately: the ruling is
recorded before it is applied.

## Bundle, in this exact order

- C0a — save this block verbatim to `.agent/authored/f260-r17.md`
- C0b — mirror the same source file to `.agent/last_block.md`
- C1 — `.agent/plan.md`, whole-file replacement from the PLAN slice
- C2 — the record: `.agent/live_review.md` gains GATE_R16; `.agent/prose_slips.md`
  gains SLIP21, SLIP22 and SLIP23; `.agent/decisions.md` gains DEC_D8 — ONE commit,
  in that file order
- C3 — `docs/roadmap/features/T2_F260.md`: the BUILTSTATE slice appended, and the
  three pairs applied
- C4 — rewrite `.agent/handoff.md` as the handback

## Change set — no path outside this list may be written

- `.agent/authored/f260-r17.md` (C0a)
- `.agent/last_block.md` (C0b)
- `.agent/plan.md` (C1)
- `.agent/live_review.md`, `.agent/prose_slips.md`, `.agent/decisions.md` (C2)
- `docs/roadmap/features/T2_F260.md` (C3)
- `.agent/handoff.md` (C4)

Nothing under `packages/`, `apps/`, `tests/` or `scripts/` is touched this round,
and `docs/roadmap/STATUS.md` and `README.md` are NOT touched — they move together
with the follow-up's registration in the next round, because the ledger and the
README may never disagree in any committed state.

## Constraints

1. Apply every slice BYTE FOR BYTE. If a slice or a gate looks wrong, apply it as
   written and DECLARE the problem in the handback. Never adjust a slice, a test
   or a gate to make a reading come out as ordered.
2. TERMINAL BYTES, measured by the reviewer at `867f34ae`. They are NOT the same
   for the three record files, and one of them CHANGED last round:
   `.agent/live_review.md` 953191 bytes ending in exactly ONE newline;
   `.agent/prose_slips.md` 119984 bytes ending in exactly ONE newline;
   `.agent/decisions.md` 848037 bytes ending in **ZERO** newlines — the round-16
   merge left that file on `origin/main`'s own convention, which the round-16
   handback declared as its deviation 4. Derive each append recipe from its own
   target's measured terminal byte and `assert` that count before writing, so a
   wrong measurement aborts rather than corrupts. The decisions recipe is
   therefore `pre + b"\n\n" + DEC_D8 + b"\n"`, which restores a trailing newline;
   the other two are `pre + b"\n" + <slice> + b"\n"`.
3. C2 writes its three files in this order: `.agent/live_review.md` FIRST,
   `.agent/prose_slips.md` SECOND, `.agent/decisions.md` THIRD, all in ONE commit.
   The three prose slips go in as SLIP21, then SLIP22, then SLIP23, separated by
   one blank line each, in that order.
4. Do NOT author a `Done:` or `Landed:` paragraph for any finding. GATE_R16 is a
   `Gate:` record and registers nothing; the open set does not move this round.
5. The three pairs of C3 are applied with `str.replace(FROM, TO, 1)` AFTER
   asserting the FROM occurs EXACTLY ONCE in the file. Each pair's shape is stated
   beside it below, as the OUTPUT of a containment test the reviewer ran, not as a
   label. The BUILTSTATE slice is an APPEND to the end of that same file.
6. `cmp` and the `remedy` binary are denied in this sandbox. Use
   `filecmp.cmp(shallow=False)` plus sha256, and `python3 -m apps.cli.grouped` for
   the CLI. Take every exit code from a Python `subprocess.run(...).returncode`;
   the bash guard rejects `$?`, `$( )` and shell loop forms BY FORM.
7. Scratch goes under the gitignored `.remedy-wt/`. Never `git add` anything
   there. Remove any worktree you create BY EXACT PATH, never by glob.
8. `.agent/STOP` does not exist at `867f34ae`. If it appears at any point, finish
   the commit in flight, hand off and end. Do not delete it, do not commit it.
9. The handback cannot table its own commit (the R-0149 pattern). Report C4's own
   numbers nowhere; the reviewer measures them at the next gate.
10. Create no pull request. Merge nothing. Never force-push. Never work on `main`.

## The pairs for C3, in `docs/roadmap/features/T2_F260.md`

The reviewer ran the containment test on each pair and reports its OUTPUT here.

PAIR 1 — the header note. `TO contains FROM: true` ⇒ APPEND-shaped.

<<<BEGIN P1_FROM>>>
> Registered 2026-08-31 by operator order amend0831-vocab-registrations.
<<<END P1_FROM>>>

<<<BEGIN P1_TO>>>
> Registered 2026-08-31 by operator order amend0831-vocab-registrations.
> BUILT across rounds 1 to 17 (2026-09-05/06) on branch `feature/f260-one-world`;
> the scope that landed is the Built State section at the end of this file. The
> remainder was split off at the amend0905-throughput soft limit by DECISION F260
> D8 and is carried by the follow-up feature registered directly after this one in
> `docs/roadmap/STATUS.md`.
<<<END P1_TO>>>

PAIR 2 — the "REGISTRATION ONLY" claim, which is no longer true of this file.
`TO contains FROM: false` ⇒ REWRITE.

<<<BEGIN P2_FROM>>>
> REGISTRATION ONLY — nothing in this file has been implemented.
<<<END P2_FROM>>>

<<<BEGIN P2_TO>>>
> PARTLY BUILT — read the Built State section before this file's Goal, T-slice and
> Acceptance sections, which describe the feature AS ORIGINALLY SCOPED and are kept
> unedited on purpose so the follow-up can copy its slices from them unchanged.
<<<END P2_TO>>>

PAIR 3 — the Orchestrator brief's split point, which this feature did not reach.
`TO contains FROM: true` ⇒ APPEND-shaped.

<<<BEGIN P3_FROM>>>
amend0905-throughput split-and-close default applies — if the session must split,
the split point is between T003 and T004, never inside T005.
<<<END P3_FROM>>>

<<<BEGIN P3_TO>>>
amend0905-throughput split-and-close default applies — if the session must split,
the split point is between T003 and T004, never inside T005. THAT SENTENCE WAS
OVERTAKEN BY EVENTS AND IS AMENDED BY DECISION F260 D8: the session limit arrived
during T002, which is earlier than any split point this brief anticipated, so the
split fell inside T002 and the brief is amended rather than obeyed. The prohibition
it carries is untouched and still binds the follow-up: never split inside T005.
<<<END P3_TO>>>

## The slices

<<<BEGIN PLAN>>>
# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, with `origin/main`
merged in at round 16. Rounds 1 to 16 are reviewed and 2 to 16 PASSED.

## Goal

SESSION 7 REACHES THE SOFT LIMIT — 25 rounds or 7 sessions, whichever comes first,
and this is session 7. The obligation is a SCOPE REPORT and then the standing
default of operator amendment amend0905-throughput: SPLIT-AND-CLOSE, executed on
this session's own authority. F260 closes at the scope it has actually built —
T001 whole, and the RUN side of T002 — and the remainder is carried by a follow-up
feature registered directly after F260, per operator order amend0906-split-placement.

## Current Step

Round 17 RULES the split as DECISION F260 D8, books round 16's verdict and the
reviewer's three prose slips, and rewrites this feature's file so it states what
was built and what moved. The follow-up's registration is the next round's, so
that the ruling is recorded before it is applied.

## Next Steps

1. Register the follow-up feature: its detail file, its STATUS line directly after
   F260's inside the same tier heading, the README counters, the TOTAL_FEATURES
   pin and the six downstream "Depends on" lines, in ONE commit.
2. The integration gate: the full suite at the branch head and at the merge base.
3. Closure part 1: the self-use item, the evidence job and the review zip.
4. Closure part 2: the verdict bookings and the ledger rotation.
5. Closure part 3: the STATUS accepted flip, the README sync, the handback and the
   pull request, which is left UNMERGED as the operator's review window.

## Risks

- README.md and docs/roadmap/STATUS.md may never disagree in any committed state,
  so the registration counters and the closure flip each land in one commit, and
  neither file is touched by any other commit of this session.
- `tests/docs/test_docs_consistency.py` pins the feature count, the id contiguity
  and the filename tier against STATUS.md, so the registration's STATUS line, its
  detail file and the TOTAL_FEATURES pin are one commit or the suite goes red.
<<<END PLAN>>>

<<<BEGIN GATE_R16>>>
Gate: R16 — the F260 R16 entry. R16 BROUGHT `origin/main` ONTO THE BRANCH AND BOOKED ROUND 15'S VERDICT INTO THE RECORD. VERDICT PASS. Range `08dca210b4b70153c35e419044dc4de6f4a188cd`..`867f34ae0c4632c961ad4a0dc9ef168d595606fc`, six commits in exactly the bundle's ordered sequence C0a, C0b, C1, C2, C3, C4, with nothing added, dropped or reordered; five are single-parent and C1 is the merge commit, whose two parents are the round's own C0b `aa6a76a5` and `f957c4c6`, the tip of `origin/main`. The reviewer re-ran every gate itself rather than reading the handback's numbers. TRANSPORT: the reviewer's scratchpad original `.remedy-wt/f260-r16-block.md`, the committed `.agent/authored/f260-r16.md` and `.agent/last_block.md` are all 20342 bytes and all hash to `4de9eb8b3979428b359f0e81bf6856023267875542449b32c03486c52b65acfc`; per §3 item 37 that chain covers the reviewer's scratch file, the worker's saved copy and the mirror, it is a COPY chain in which nothing is retyped, and it is not a claim about the bytes emitted into a prompt. THE MERGE, which was the point of the round: `.agent/decisions.md` at the merge commit is 848037 bytes with sha256 `e161a74832cc6452f6fc2755d09de4bbd1fd8e3d223ec25b6410904e5cfef463`, exactly the value the block ordered, and the reviewer reproduced the three-segment equality independently — its first 836338 bytes equal the file at `b5cd6c20`, the next 8734 equal this branch's own appended tail carrying DECISION F260 D5, D6 and D7, and the remaining 2965 equal the tail `origin/main` appended carrying the operator's amend0906-split-placement DECISION. Nothing was dropped from either side and nothing was invented: lines opening or closing a git conflict marker and lines equal to a run of seven equals signs each count ZERO in the merged file, and the reviewer measured those same three counts at zero in all three inputs, so the gate is not satisfied by its own absence of subject matter. Over the merge's own change set the seven paths other than `.agent/decisions.md` are byte-identical to their blobs on `origin/main`. THE SLICES, extracted by the reviewer from the COMMITTED authored copy and never from a retype: `.agent/plan.md` equals the PLAN slice plus exactly one newline at 2245 bytes and 43 lines, under the 50-line cap, carrying `## Goal` and `## Next Steps`; `.agent/live_review.md` equals its pre-image plus a newline plus GATE_R15 plus a newline, 947109 to 953191 bytes, blank-line units 437 to 438; `.agent/prose_slips.md` the same shape for SLIP20, 119984 bytes after, units 150 to 151. Both appended regions were checked by an independent structural reader over the whole appended region with N counted from the slice, and by an in-memory negative control that flipped one byte inside the first appended paragraph and was REJECTED by both readers, then restored and accepted by both. CENSUS at the round's last content commit: `^Gate: ` 25 with `^Gate: R15 — ` at exactly 1, registrations 301 over 301 DISTINCT ids, `^Done: ` 5 lines over THREE distinct ids, OPEN SET 298 BY DISTINCT ID — unchanged, which is correct because this round registered and resolved nothing. Zero lines beginning with a block marker prefix reached either record file. SUITES re-run by the reviewer in the primary checkout, serially: `tests/docs/` exit 0 at 303 passed, the canary `tests/cli/test_golden_path.py` exit 0 at 42 passed, and the three-file run-log selection exit 0 at 140 passed, with zero `FAILED` and zero `ERROR` lines in each; `python3 -m apps.cli.grouped integrity check --json` exit 0 with `"passed": true` and `"fail_count": 0` over five checks. `tests/docs/` is the suite that matters here because the merge carried `docs/` changes, and the reviewer had additionally dry-run it against the merge result BEFORE emitting the block, together with a red control that broke the README accepted-count on purpose inside a disposable worktree and confirmed the suite really goes red — exit 1 at 1 failed and 302 passed — then restored the file byte-identically and re-read exit 0 at 303 passed. `git status --porcelain` is EMPTY in the primary checkout and `git ls-files .remedy-wt` is EMPTY. THREE DEVIATIONS WERE DECLARED AND ALL THREE ARE UPHELD, and all three are defects of the REVIEWER's own block rather than of the work; the worker applied the block as written, declared each gap, adjusted nothing, and was right to do so in every case. First, the block named a full base SHA that does not exist as an object — the reviewer had measured only the eight-character prefix and wrote out a full-length value it never read — while the prefix every gate actually used resolves uniquely to the real tip. Second, the block's merge gate ordered the merge commit's FIRST parent to be that base, which its own bundle makes impossible, because the bundle places the two block-save commits before the merge and the first parent is therefore necessarily the second of them. Third, the same gate ordered a path comparison over a range that also contains those two block-save commits, one of which writes a file that does not exist on `origin/main` at all; the worker ran both the ordered form and the corrected form scoped to the merge's own change set, and the property the gate exists to protect holds at seven of seven. None of the three left anything wrong under `packages/`, `apps/`, `tests/` or `docs/`, so per operator amendment amend0827-process-diet rule 2 none spends an id and each is one dated line in `.agent/prose_slips.md`. The worker additionally reported, unprompted and correctly, that the merge left `.agent/decisions.md` ending in ZERO newlines where this branch's own convention had been one, and warned that the next round's append recipe for that file must be derived from that measurement rather than copied from a prior round; the reviewer confirms the terminal-byte count at zero and the round-17 block carries the corrected recipe.
<<<END GATE_R16>>>

<<<BEGIN SLIP21>>>
2026-09-06 · F260 R16 (reviewer) · The round-16 block stated its base as a full forty-character SHA that does not exist as an object in this repository: the reviewer had only ever measured the eight-character prefix `08dca210`, and wrote out a full-length value it never read, inventing the remaining thirty-two characters. Nothing broke, because every gate in the block quoted the prefix rather than the long form and the prefix resolves uniquely to the real tip, so the worker executed against the right commit and declared the discrepancy. THE LESSON is that a SHA is a measurement like any other and is never completed from memory or from the shape of the thing: write the prefix that was actually read, or run `git rev-parse` and paste what it returns. A base SHA is the one value in a block that every later gate resolves against, so a fabricated one is the cheapest possible way to make an entire round unverifiable.
<<<END SLIP21>>>

<<<BEGIN SLIP22>>>
2026-09-06 · F260 R16 (reviewer) · Gate G2(f) of the round-16 block ordered the merge commit's two parents to be the round's BASE and the tip of `origin/main`, while the same block's own Bundle places the two block-save commits C0a and C0b BEFORE the merge — so the merge's first parent is necessarily C0b and the ordered reading was unmeetable by construction, for every possible execution of that bundle. THE LESSON is checklist item 13 arriving through a gate about PARENTAGE rather than about a reading's timing: a clause naming which commit another commit descends from is a claim about the block's OWN commit sequence, and it is checked by walking that sequence on the page before emission. The safe form names the position — "C1's first parent is the commit immediately before it in this bundle" — rather than a SHA that was true only before the bundle added commits ahead of it.
<<<END SLIP22>>>

<<<BEGIN SLIP23>>>
2026-09-06 · F260 R16 (reviewer) · Gate G2(e) of the round-16 block ordered every path in the range BASE to the merge commit, other than the resolved one, to be byte-identical to its blob on `origin/main` — but that range also contains the block's own two save commits, and one of the paths they write, `.agent/authored/f260-r16.md`, does not exist on `origin/main` at all, so a literal reading of the gate cannot even produce a value for it. THE LESSON is that a gate comparing a merge against what it merged must be scoped to the MERGE's own change set, which is the diff against its first parent, and not to a range whose endpoints the block itself chose for other reasons; the worker ran both forms and the corrected one holds at seven of seven, which is the reading the gate was written to take. Item 22's shape — a sentence quantifying across commits measured over the wrong range — reaching a gate's path set instead of a count.
<<<END SLIP23>>>

<<<BEGIN DEC_D8>>>
### DECISION F260 D8 (2026-09-06, F260 round 17, session 7) — F260 closes at the job record and the one id shape; the run re-key, the consumers and the deletions are split off as a follow-up feature placed directly after it
CONTEXT. Operator amendment amend0905-throughput sets the soft limit at 25 ROUNDS or 7 SESSIONS per feature, whichever comes first, and makes SPLIT-AND-CLOSE the standing default on reaching it, executed on the session's own authority rather than referred to the operator as a question. This is session 7 of F260 at round 17, so the SESSION half of the limit is the binding one; the round half is not close, which is worth recording because it means the constraint that ended this feature was WALL CLOCK, not scope creep and not repair churn. Every round from 2 to 16 PASSED, one round FAILED and was repaired, and no round was spent on rework of its own earlier work. MEASURED SCOPE, from the ledger entries `Gate: R1` through `Gate: R16` and the feature file's own task list. BUILT: T001 whole — the inventory in `.agent/f260_inventory.md`, DECISION F260 D1 ruling the record layout and D2 ruling the 16-hex id shape with one minting function per kind, and those minting functions at their call sites; and the RUN side of T002 — the ping-pong job record moved under the one jobs root beside its own evidence, both resolvers returning `str`, the ping-pong run store and the job-keyed run-log store each given one spelling in `data_paths` across the whole production side, and, at round 15, a run made an INVOCATION rather than an event, which DECISION F260 D7 rules and finding R-0816 measured on disk before and after. NOT BUILT: the rest of T002 — `Job.run_refs`, the re-key of the run directory onto a RUN id, the unified record's eleven administrative fields and the Mission extension; T003 whole, the eleven named consumers; T004 whole, the classic cycle runner and the resolver collapse DECISION F260 D5 placed there; and T005 whole, the reachability test and the prototype cluster deletion, measured in the feature file at 24527 lines under `packages/orchestration/` plus 4731 lines of `apps/cli/commands/*_cmd.py`. CHOSEN. F260 closes at the scope it built, and the remainder is registered as ONE new follow-up feature placed IMMEDIATELY AFTER F260's line inside the same tier heading, per operator order amend0906-split-placement, so that Rule A5 proposes it before any other unchecked feature. The follow-up's file copies its T-slices and its Acceptance items from F260's file rather than re-planning them, which is why this decision does not restate them; F260's own file keeps its Goal, T-slice and Acceptance sections UNEDITED for exactly that reason, and gains a Built State section stating what landed and what moved. THE DEPARTURE THIS DECISION IS MOST RESPONSIBLE FOR RECORDING: F260's Orchestrator brief says that if the session must split, "the split point is between T003 and T004, never inside T005". The session limit arrived during T002, which is EARLIER than any split point that brief anticipated, so the split falls inside T002 and the brief is amended rather than obeyed. The prohibition the same sentence carries — never split inside T005 — is untouched and binds the follow-up, because T005 is the deletion round and a half-performed deletion is the one state this feature must never leave behind. This is a wrong-spec finding routed to planning under docs/agents/planner_reviewer_prompt.md §4 item 7: the ruling is authored, recorded and proceeded under, and the operator's veto is any later relay. ALTERNATIVES CONSIDERED. Run session 7 past the limit to reach the brief's own split point between T003 and T004 — rejected: T003 is eleven consumers each owed a test against a ping-pong-created job, and T004 is a forty-call-site resolver collapse, which is several sessions of work rather than several rounds, so this option does not reach the brief's split point either, it merely reaches the limit later and with the same split still owed. Close F260 at its full scope by narrowing what the Acceptance list demands — rejected outright: the Acceptance items are the feature's reason for existing and none of them holds today, so this is the failure mode AGENTS.md names as the one unforgivable one. Stop and ask the operator which of the two to take — rejected because amend0905-throughput exists precisely to remove that question, having been written after F262's round 23 wrote a correct scope report and then waited a whole session for a ruling the default already supplied. Split the remaining scope into TWO follow-up features, one for the records and one for the deletions — rejected as premature: the follow-up inherits a coherent single narrative, and if it in turn reaches its own limit the same default applies to it with better information than this session has. CONSEQUENCE. F260's STATUS line will read as complete for the slices it built and will name the follow-up; it will not claim T002 through T005. The vocabulary page F259 made binding is unaffected, since F260 changed what a job IS and never what it is CALLED. No production behaviour is reverted by this decision and nothing on disk is deleted by it; it moves the boundary of a ledger line and nothing else. REVERSE by deleting this paragraph, deleting the follow-up feature's STATUS line and its detail file, restoring the `TOTAL_FEATURES` pin and the README counters to their pre-registration values, removing the follow-up from the six downstream "Depends on" lines, and returning F260's STATUS line to `[~]`; the feature then stands unsplit at the scope its Goal section describes, with its Orchestrator brief's split point binding again unamended.
<<<END DEC_D8>>>

<<<BEGIN BUILTSTATE>>>
## Built State (2026-09-06, rounds 1 to 17, ledger `Gate: R1` to `Gate: R16`)

Scope per DECISION F260 D8, which closed this feature at the soft limit of operator
amendment amend0905-throughput and split the remainder off as the follow-up feature
registered directly after this one in `docs/roadmap/STATUS.md`. The Goal & Done,
T001 to T005 and Acceptance sections above are kept UNEDITED and describe the
feature as originally scoped, so that the follow-up copies its slices from them
unchanged; this section is the one that describes what is on disk.

- T001 (rounds 1 to 6), COMPLETE. `.agent/f260_inventory.md` measured both writers,
  the three id shapes actually minted, and the four kinds of thing the 16-hex shape
  already named. DECISION F260 D1 rules the record layout and the three areas;
  DECISION F260 D2 rules the one id shape as 16-hex with a SEPARATE minting function
  per kind, in `packages/orchestration/data_paths.py`, because one shape naming four
  kinds is not one function. DECISION F260 D4 records why the one RESOLVER could not
  land in T001, and moves it to the store that makes it true.
- T002 (rounds 7 to 15), PARTIAL — the RUN side only. The ping-pong job record moved
  under the one jobs root beside its own evidence; both resolvers return `str`; the
  ping-pong run store and the job-keyed run-log store each have ONE spelling in
  `data_paths` across the whole production side; `RunLogWriter` takes a data root;
  and a RUN is now an INVOCATION rather than an event — `packages/orchestration/
  timeline.py` holds one run id for the life of the process, which is what
  `RunLogWriter`'s docstring had always promised. DECISION F260 D7 rules that
  cardinality and finding R-0816 records it, measured on disk at five files for one
  five-event resume before the fix and one file after. DECISION F260 D5 records why
  the resolver COLLAPSE belongs in T004 rather than here. DECISION F260 D6 records
  why the TEST-side spelling sweep was declined rather than forgotten.
- MOVED TO THE FOLLOW-UP FEATURE by DECISION F260 D8, not abandoned: the rest of
  T002 — `Job.run_refs`, the re-key of the run directory onto a RUN id, the unified
  record's eleven administrative fields, and the Mission extension; T003 whole, the
  eleven consumers named under Design; T004 whole, the classic cycle runner and the
  resolver collapse; and T005 whole, the reachability test, the two carry-overs,
  DECISION F260 D3 and the prototype cluster deletion. Every Acceptance item of this
  file moves with them, because none of them holds at this close.
- Findings: R-0814 resolved; R-0816 open at this close and owned by the follow-up,
  which is where the re-key it is a prerequisite for now lives.
<<<END BUILTSTATE>>>

## Done when — the gates. Report ONE LINE PER GATE with its REAL exit code.

**G1 TRANSPORT — one comparison.** Before staging C0a, sha256 over the
delegation's source file, `.agent/authored/f260-r17.md` and
`.agent/last_block.md`. All three must equal the digest the delegation names.
Both writes are `shutil.copyfile` from the source path, each proved with
`filecmp.cmp(shallow=False)` = True.

**G2 THE RECORD, at C2.** For `.agent/live_review.md` and for
`.agent/decisions.md`, three readings each:
(a) exact image — `post == pre + <this file's recipe from constraint 2>` is True,
and `post[:len(pre)] == pre` is True. Report both byte counts;
(b) structural, independent of (a) — split the WHOLE file on a blank line and
compare the last N units against the slice's N paragraphs IN ORDER, where N is a
number your script COUNTS from the slice and never one this block asserts. Report
the unit count before and after;
(c) negative control, run IN MEMORY on a `bytes` object so the primary checkout
never holds known-bad bytes: flip one byte inside the FIRST appended paragraph;
both readers must REJECT. Restore; both must ACCEPT and the restored image must
equal the disk image.
For `.agent/prose_slips.md` a byte-equality reading is enough: `post == pre +
b"\n" + SLIP21 + b"\n\n" + SLIP22 + b"\n\n" + SLIP23 + b"\n"` is True. Report both
byte counts and the blank-line unit count before and after, and confirm the last
three units are SLIP21, SLIP22, SLIP23 in that order.

**G3 THE PLAN, at C1.** `.agent/plan.md` equals the PLAN slice plus exactly one
trailing newline. Report its byte count and line count; it must be under the
50-line cap AGENTS.md sets and must carry `## Goal` and `## Next Steps`.

**G4 THE THREE PAIRS, at C3.** For each of P1, P2, P3 report FOUR numbers: the
FROM count BEFORE the edit, which must be 1; the containment reading `TO contains
FROM` printed as the words `true` or `false`; the FROM count AFTER; and the TO
count AFTER, which must be 1. For P1 and P3 the containment reading is `true`, so
the FROM count after is NOT ordered to be 0 and must not be reported as a
failure when it is 1 — those are append-shaped pairs and the FROM survives inside
the TO. For P2 the reading is `false`, so the FROM count after must be 0.

**G5 THE APPEND AND THE WHOLE-FILE RECONSTRUCTION, at C3.**
`docs/roadmap/features/T2_F260.md` after C3 must equal its pre-edit bytes with
ONLY the three pair replacements applied AND the BUILTSTATE slice appended by the
recipe your script derives from the file's own measured terminal byte — recomputed
independently from the pre-edit text, reported as ONE boolean. Report the file's
byte count before and after, and that it ends with exactly one newline. Also
report that the file contains ZERO lines beginning `<<<BEGIN ` or `<<<END `.

**G6 THE CENSUS, after C2.** Over `.agent/live_review.md`: `^Gate: ` must read 26;
`^Gate: R16 — ` must read exactly 1; registrations `^- R-\d{4} — ` must read 301
over 301 DISTINCT ids; `^Done: R-\d{4} — ` must read 5 lines over 3 distinct ids;
and the OPEN SET BY DISTINCT ID must read 298 — unchanged, because this round
registers and resolves nothing. Report that `.agent/live_review.md`,
`.agent/prose_slips.md` and `.agent/decisions.md` each contain ZERO lines
beginning `<<<BEGIN ` or `<<<END `.

**G7 THE SUITES, run SERIALLY, in the PRIMARY checkout, after C3.** Report each
one's real exit code and its pass count:

    python3 -m pytest tests/docs/ -q -p no:randomly
    python3 -m pytest tests/orchestration/test_roadmap_index.py -q -p no:randomly
    python3 -m pytest tests/cli/test_golden_path.py -q -p no:randomly
    python3 -m apps.cli.grouped integrity check --json

`tests/docs/` and `test_roadmap_index.py` are in this list because C3 changes a
file under `docs/roadmap/`. The integrity check must report `"passed": true` with
`"fail_count": 0`. Report any `^FAILED` or `^ERROR` lines; there must be none.

**G8 TREE AND STRUCTURE.** `git status --porcelain` is EMPTY; `git ls-files
.remedy-wt` is EMPTY. Every commit C0a through C3 is single-parent — report each
one's parent count. Every commit's INSERTION count — the `+` column of `git diff
--numstat`, never insertions plus deletions — is reported for C0a through C3 and
is under 500. Count the `.py` files in `git diff --name-only 867f34ae..C3`
yourself; if there are none, report this gate's lint half as not applicable rather
than inventing a target, and if there are any, run `python3 -m ruff check` over
exactly those and report the names and the exit code.

## Handback

Rewrite `.agent/handoff.md`. Mandated sections: the Session block naming SESSION 7
of F260, round 17, and rounds so far 17; a one-sentence context self-assessment;
the Range; the per-commit table with `+/-` taken from `git log --numstat` and
never re-derived by eye; External actions; Verification, one line per gate with
its real exit code; the Authored-text proofs; Deviations and assumptions; the
Item-status table with every bundle item and every gate appearing exactly once as
`done`, `skipped` or `deviated` with a reason; Open findings; and Next.

Then `git push -u origin feature/f260-one-world`. Create NO pull request. Merge
nothing. Never force-push.
