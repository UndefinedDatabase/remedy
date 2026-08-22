── STEP LEDGER-CLEAR — F009 ──
Goal:        Clear the block condition this session inherited. The R31 verdict
             is recorded, the two reviewer-block defects the carrier held are
             registered as R-0646 and R-0647, and `.agent/candidates.md` is
             emptied in the same round — which is what
             docs/roadmap/STATUS_closure_protocol.md's disk-vehicle rule and
             docs/agents/planner_reviewer_prompt.md §1 item 4 require of the
             FIRST reviewed round of a session that starts with a non-empty
             carrier. No closure work happens here; closure is the next round.

Fortschritt: ~99 % (T001 gebaut · T002 gebaut · T003 gebaut und verifiziert ·
             Integrations-Gate BESTANDEN; offen bleiben nur die zwei
             Closure-Runden: Evidenz und Zip, dann STATUS-Zeile und PR) —
             Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the two finding
             registrations · C3 the R31 verdict · C4 empty the carrier ·
             C5 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f009-r32.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2 and
             C3) · `.agent/candidates.md` (C4) · `.agent/handoff.md` (C5).
             NOTHING under `packages/`, `apps/`, `docs/` or `tests/` is touched.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4, C5 and is not negotiable. C1
    precedes the ledger commits because the plan must be current before them
    (checklist item 23). C2 precedes C3 because findings persist FIRST
    (docs/agents/planner_reviewer_prompt.md §4.4). C4 follows C3 because the
    carrier may only be emptied once the ids that replace it are on disk.
 3. THIS ROUND MINTS EXACTLY TWO IDS, R-0646 and R-0647, both inside the
    FINDINGS slice, and RESOLVES NOTHING. It writes no `Done:` line and no
    `Landed:` line. The next free id when the round ends is R-0648.
 4. TWO APPENDS AND TWO WHOLE-FILE REPLACEMENTS. PLANF009R32 replaces
    `.agent/plan.md` at C1 in full. FINDINGS appends to `.agent/live_review.md`
    at C2 BASED ON THE ROUND BASE. LEDGER32 appends to `.agent/live_review.md`
    at C3 BASED ON C2, never on the round base — a round-base comparison for
    the second append is wrong by one whole slice, which is the reading F009
    R30 got right and recorded. CANDIDATES32 replaces `.agent/candidates.md` at
    C4 in full. There is NO FROM/TO pair in this round; order no containment
    reading and no FROM count anywhere.
 5. The reviewer measured the targets at the round base
    `5ad780198cc7bceaff3b4664a2d1500e45b24336`: `.agent/live_review.md` is
    576883 bytes over 1138 lines and ends in exactly ONE newline;
    `.agent/candidates.md` is 3300 bytes over 48 lines; `.agent/plan.md` is
    2142 bytes over 40 lines. So each append is one newline followed by its
    slice.
 6. FINDINGS carries its entries separated by a blank line, in the shape
    `.agent/live_review.md` already uses: every entry in that file is ONE
    physical line and entries are blank-line separated. Count FINDINGS'
    paragraphs and LEDGER32's paragraphs with your script rather than from any
    sentence in this block.
 7. The `Fortschritt:` line above is relayed deliberately (finding R-0418); the
    handback's state block repeats it VERBATIM across all FOUR of its lines.
    Four is the reviewer's own count of this block's bytes.
 8. EVERY reading at a revision other than the one your shell is on is taken
    with `git show <sha>:<path>` into memory or into a scratch file under the
    gitignored `.remedy-wt/`. NEVER write a base blob over a tracked file and
    restore it afterwards: docs/agents/self_drive_protocol.md guardrail G5
    forbids mutating the primary checkout, and checklist item 29 exists because
    a round did exactly that (finding R-0594).
 9. SIZE, measured at emission by reading it back out of the assembled bytes
    and computing PROSE as TOTAL minus the slices' CONTENT lines, with marker
    lines counted as prose per DECISION F085 D5: this block is 250 lines
    TOTAL against DECISION F085 D6's 490 cap, 195 of them PROSE against
    D5's 400. Re-measure both from the committed C0a blob; a disagreement is a
    finding.

Done when — run every gate and record its REAL exit code and output:
 G1  Before C0a and again before C5: `.agent/STOP` is ABSENT,
     `git rev-parse --abbrev-ref HEAD` prints
     `feature/f009-single-write-channel`, and `git status --porcelain` prints 0
     lines after each of C0a, C0b, C1, C2, C3 and C4. Report the round base SHA
     you read at step 0.
 G2  TRANSPORT: `.agent/authored/f009-r32.md` at C0a and `.agent/last_block.md`
     at C0b are byte-equal to each other and to the block you received; report
     sha256, bytes and lines for all three. C0b is written FROM the committed
     C0a blob, never from the scratch copy again.
 G3  SLICES: extract every slice from the COMMITTED C0a blob by its `<<<SLICE `
     and `<<<END ` marker lines with a script and apply them programmatically.
     Report each slice's sha256, bytes and lines plus the aggregate count your
     script printed. State no slice count you did not count. Re-measure
     constraint 9's two numbers from that same blob — TOTAL, and PROSE as TOTAL
     minus the summed slice-CONTENT lines — and report both.
 G4  `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R32 and
     `.agent/candidates.md` at C4 is BYTE-EQUAL to CANDIDATES32 — report `cmp`
     exit and both sha256 for EACH, each with a negative control against
     another file exiting non-zero. Report `wc -l` for the plan against the
     50-line cap of AGENTS.md. Line-anchored in the plan, `^## Goal$` and
     `^## Next Steps$` each read 1. Over `.agent/candidates.md`, all six of
     these, every one LINE-ANCHORED at line start: a leading `- ` reads 2 at
     the round base and 0 at C4; `^NON-EMPTY\.` reads 1 at the round base and 0
     at C4; `^EMPTY\.` reads 0 at the round base and 1 at C4. Anchoring is not
     decoration here — the reviewer's dry run found that an UNANCHORED count of
     `EMPTY.` reads 1 at BOTH points, because `NON-EMPTY.` contains it, so the
     substring form is the vacuous clause R-0646 registers, arriving in the
     round that registers it. Report all six numbers.
 G5  THE TWO APPENDS, each under TWO independent readers, each with a negative
     control on the FIRST appended paragraph (finding R-0631). For FINDINGS at
     C2 based on the round base, and then for LEDGER32 at C3 BASED ON C2:
     (a) the base blob is a byte-exact PREFIX and the remainder equals a
     newline plus that slice — report its sha256, bytes and lines; (b) N is
     counted BY YOUR SCRIPT and the last N blank-line-separated units equal the
     slice's N paragraphs IN ORDER. Then, for each append separately, flip one
     printable byte in the FIRST appended paragraph at equal length and report
     that BOTH readers REJECT the flip while both ACCEPT the true file. Report
     before/after bytes and lines for each append.
 G6  Line-anchored at line START over `.agent/live_review.md` at the round
     base, at C2 and at C3: a leading `- R-` id with every captured id DISTINCT
     at each point; a leading `Done: R-` id; a leading `Landed: `; a leading
     `Gate: R` key over that many DISTINCT keys; and the `Gate: R32` key.
     Report EVERY one of those five readings at EVERY one of the three points
     — none of them belongs in a round report, because a reading routed there
     dies with the session (finding R-0494). The reviewer's base readings,
     which yours must reproduce: entries 211, `Done:` 3, `Landed: ` 0,
     `Gate: R` keys 31 over 31 DISTINCT, `Gate: R32` 0. Constraint 3 fixes that
     entries read 213 all DISTINCT at C2 and at C3, and that `Gate: R32` reads
     0 at C2 and 1 at C3.
 G7  THE ANCHORING CONTROL, ordered as a DIFFERENCE and never as a maximum,
     because the anchored and unanchored maxima coincide whenever the round's
     own new id is the file's ceiling — which is exactly the defect R-0647
     registers, applied in the round that registers it. Over
     `.agent/live_review.md` at the round base and again at C3, report all four
     populations: leading `- R-` ids, DISTINCT `R-\d{4}` strings anywhere in
     the file, how many of those distinct strings were NEVER registered as a
     leading id, and leading `Gate: R` keys against unanchored occurrences of
     `Gate: R`. The reviewer's base readings, which yours must reproduce: 211
     anchored ids, 271 distinct unanchored strings, 60 never registered, 31
     anchored `Gate: R` keys against 81 unanchored occurrences. Report the C3
     numbers as MEASURED — this block predicts none of them, because the slices
     it ships quote ids in prose and the reviewer will not order a number it
     did not compute.
 G8  Report the max REGISTERED id, read line-anchored, and the open count by
     DECISION F009 D10's rule at the round base and at C3. This reading exists
     to fix the next round's id ceiling and NOT as an anchoring control; G7 is
     the control. The reviewer's base readings: max REGISTERED id R-0645, open
     208. Constraint 3 fixes max R-0647 and open 210 at C3.
 G9  RANGE: the range from the round base to C4 lists EXACTLY the declared
     paths other than `.agent/handoff.md`, the set difference EMPTY in both
     directions, and 0 paths beginning `packages/`, `apps/`, `docs/` or
     `tests/`. Each commit has ONE parent; `git show --numstat` and
     `git diff --numstat` AGREE on every cell — invoke `git show` WITHOUT a
     `--` before the SHA, which turns it into a pathspec and prints nothing;
     every cell equals the `+/-` column of the handback's `## Commits` table
     (checklist item 28), compared cell by cell. Report each pre-handback
     commit's insertions against the 500 cap; the handback commit's own numbers
     belong in the round report (item 14). Leading `<<<SLICE ` and `<<<END `
     read 0 LINES in every file a slice lands in, which are `.agent/plan.md`,
     `.agent/live_review.md` and `.agent/candidates.md` — read that count
     LINE-ANCHORED and not as a substring, because LEDGER32 legitimately QUOTES
     both marker strings mid-line in its own range sentence. `git ls-files
     .remedy-wt` reads 0. Classify THIS ROUND's reflog rows by the operation
     before the first `:` and report `amend`, `rebase` and `cherry` each 0;
     assert no total over the whole reflog (R-0601).
 G10 CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q -rf` in the
     PRIMARY checkout, serially, with no other pytest process alive (finding
     R-0518). Report its REAL exit code and the count IT printed. No docs gate
     is owed: this round's change set holds no `docs/` path. The reviewer ran
     the canary at the round base before ordering it — it exits 0 at 42 passed,
     so it can fail honestly (R-0364).
 G11 The handback carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each of C0a, C0b,
     C1, C2, C3, C4 and C5, the round base SHA, one line per gate, and this
     block's `Fortschritt:` line VERBATIM across all four of its lines. Where a
     gate ordered a reading AT SEVERAL POINTS, every point's value appears in
     the file and not only the first — G6 and G7 are that shape, and a gate
     line that reports one point of three is the R-0494 incompleteness this
     round's own verdict slice records. Report its `wc -l` against the 100-line
     cap AGENTS.md allows for a per-commit table of more than five commits,
     which the commit sequence constraint 2 fixes is; if the mandated content
     does not fit, carry a DECISION D15 "Deviations, declared" line naming the
     actual count and the mandated content that caused it, and NEVER drop a
     section to fit. Its `## Next` section states that the next round is
     closure round one — the evidence job and a FRESH review zip — and that
     `.agent/candidates.md` is EMPTY as of C4.

Handback:    completion report + rewrite `.agent/handoff.md`. Push after C5.
             Create NO pull request: F009 opens one at its own closure.
─────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF009R32
# Plan — F009 The single write channel

Branch: feature/f009-single-write-channel, cut from `main` at `ce49348b`, the
merge commit of pull request #209. `.agent/live_review.md` is the source of truth
for the open set, the round map and the finding-id ceiling.

## Goal
Exactly ONE door for UI-initiated change: POST /api/jobs/{jid}/commands validates
against the UI-exposed catalog subset, authenticates with a bearer token plus an
X-Remedy-CSRF double-submit, rate-limits per token and job, deduplicates by
client nonce, and ENQUEUES into the existing decision, approval and control
machinery without touching files, jobs or shells directly. Every other POST, PUT
and DELETE answers 405. DONE when the exposed commands round-trip through their
effects on fixtures, replayed nonces are idempotent, unauthenticated and
cross-site attempts fail closed and are audited as rejected, and a route-walking
test plus an import guard prove no other mutating route exists.

## Current Step
R32 clears the block condition this session inherited. It records the R31
verdict, registers as R-0646 and R-0647 the two reviewer-block defects the
closure-candidate carrier held, and empties that carrier in the same round. The
build and its integration gate are done; what remains is closure.

## Next Steps
1. Closure round one: the evidence job and a FRESH review zip, whose values the
   STATUS line quotes.
2. Closure round two: the authored STATUS line, the README capability sync in
   the SAME commit, and the pull request.

## Risks
- Closure needs TWO rounds, not one: ending right after a verdict strands it
  (DECISION F085 D9).
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- The closure zip's known blockers are on disk, not in memory: sorted
  `verification_runs[].test_files`, an `output_hash` that is sha256 of
  `stdout_summary` exactly, node ids from `--collect-only`, and no full-suite
  node-id list (STATUS_closure_protocol.md, algorithm step 1).
<<<END PLANF009R32

<<<SLICE FINDINGS
- R-0646 — Low — A GATE COUNTED A MARKDOWN CONSTRUCT ITS NAMED TARGET DOES NOT CONTAIN, SO THE CLAUSE COULD NOT HAVE FAILED FOR ANY ROUND. Found and declared by the WORKER of F009 R30 and confirmed by that round's reviewer against the named file; carried across the session boundary in `.agent/candidates.md` at `896f0312` and registered here by the first reviewed round of the next session, which is what the disk-vehicle rule of docs/roadmap/STATUS_closure_protocol.md exists to make happen. The R30 block's G8 ordered the line-anchored `^## ` heading count of `docs/agents/integration_gate.md` to read the same at the round base and at C4. Measured at `002e0e83`, that file carries ONE `# ` title and ZERO `^## ` headings, so both readings are 0 and "the same count" is true of every possible round. This is the R-0438 vacuous-gate class arriving through a document's STRUCTURE rather than through a missing path, which is why R-0438's own clause does not reach it: the path resolves and only the heading level is absent. Checklist item 24 makes a reviewer resolve every PATH a gate names and nothing yet makes it resolve the CONSTRUCT a gate counts. Fix: promote into docs/agents/planner_reviewer_prompt.md §3 the rule that before ordering a count of a markup construct the reviewer reads that construct's count in the target at the base, and where the base count is 0 either drops the clause or counts the construct the file actually uses — a count that is 0 on both sides discriminates nothing, exactly as a clause naming a path that does not exist forbids nothing.

- R-0647 — Low — A CONTROL ORDERED TO SHOW THAT AN ANCHORING MATTERS WAS ORDERED AS A MAXIMUM, AND THE TWO MAXIMA COINCIDE PRECISELY WHEN THE ROUND'S OWN NEW ID IS THE CEILING. Found and declared by the WORKER of F009 R30 and confirmed by that round's reviewer; carried in `.agent/candidates.md` at `896f0312` and registered here alongside R-0646. The R30 block's G6 ordered the max REGISTERED id read line-anchored and cited R-0630, whose warning is that an unanchored scan reports a maximum that was never registered. R-0645 was minted by that same round and is the file's highest id, so the anchored and the unanchored maxima are both R-0645 and the reading demonstrates nothing at all. The discriminating readings existed and the worker reported them unprompted. Measured at `5ad78019`: 211 anchored ids against 271 DISTINCT unanchored `R-` strings of which 60 were never registered as a leading id, and 31 anchored `Gate: R` keys against 81 unanchored occurrences of that same string. Fix: promote into docs/agents/planner_reviewer_prompt.md §3 the rule that a control existing to show an anchoring matters is ordered as the DIFFERENCE between the anchored and the unanchored population and never as a maximum over either, because the two coincide whenever the newest id is the reviewer's own — the shape R-0630's own counter-measure did not name. The block registering this finding applies it: its own anchoring control is ordered as that difference, and its maximum is ordered separately and only to fix the next round's id ceiling.
<<<END FINDINGS

<<<SLICE LEDGER32
Gate: R32 — the R31 entry. R31 PASSED. Every gate was RE-EXECUTED by the reviewer off disk rather than read back out of the handback, and every value reproduced. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f009-r31.md` at `a4d92d41`, `.agent/last_block.md` at `192f3dc2` and the bytes the reviewer EMITTED, still on disk at `.remedy-wt/f009-r31.md`, are all sha256 55e0ca46a24cda5cc3b26488547b9991e852495a6988ed55904be33f5ac33d1e over 20989 bytes and 242 lines, and that digest is the one the block itself named before the round began. The reviewer's own extraction out of the committed C0a blob prints an aggregate of 3 slices over 89 CONTENT lines, and constraint 7's numerals re-measure as 242 TOTAL and 153 PROSE, both under DECISION F085 D6's 490 and D5's 400. `.agent/plan.md` at `b4149410` is BYTE-EQUAL to that round's PLANF009R31 slice, 40 lines against the 50-line cap, with `^## Goal$` and `^## Next Steps$` each reading 1, and `.agent/candidates.md` at `896f0312` is BYTE-EQUAL to its CANDIDATES slice; each negative control differs. THE APPEND HOLDS UNDER THE REVIEWER'S OWN TWO READERS: LEDGER31 at `6cae6a53` is based on the round base, the base blob a byte-exact PREFIX and the remainder exactly one newline plus the slice, 571277 to 576883 bytes and 1136 to 1138 lines, N counted at 1; a single equal-length printable-byte flip inside the FIRST appended paragraph is REJECTED by both readers while both ACCEPT the true file. THE SETS HELD line-anchored at line start: at the round base entries 211 all DISTINCT, `Done:` 3, `Landed: ` 0, `Gate: R` keys 30 over 30 DISTINCT, `Gate: R31` 0, max REGISTERED id R-0645, 208 open; at `6cae6a53` the entries are UNCHANGED at 211 all DISTINCT with max still R-0645 and 208 open, which is the reading that shows the round minted nothing, while `Gate: R` reaches 31 over 31 DISTINCT with `Gate: R31` at 1. THE RANGE HELD: base→`896f0312` lists exactly the five declared paths, set difference EMPTY in both directions, and 0 paths beginning `packages/`, `apps/`, `docs/` or `tests/`; every one of the round's six commits has ONE parent; `git show --numstat` and `git diff --numstat` agree on every cell and every cell equals the `+/-` column of the handback's own table, at 242/0, 179/240, 12/12, 2/0, 46/10 and 65/65; pre-handback insertions 242, 179, 12, 2 and 46, each under the 500 cap, and the handback commit's own 65 is under it as well; zero leading `<<<SLICE ` and `<<<END ` LINES in all three slice targets; `git ls-files .remedy-wt` 0; the round's six reflog rows all classify as `commit`, with `amend`, `rebase` and `cherry` each 0 and no total asserted over the whole reflog. THE CANARY IS THE REVIEWER'S OWN, re-run serially in the primary checkout: it exits 0 at 42 passed. THE VERDICT SLICE THAT ROUND APPLIED WAS ALSO CHECKED AGAINST THE ROUND IT DESCRIBES rather than only against its bytes: R30's per-commit cells 303/0, 204/172, 12/11, 2/0, 2/0, 8/3 and 59/0 reproduce over `bcf295f9`→`d8d48b7f`, R30's base ledger reads 210 entries with max R-0644 and 207 open, `docs/agents/integration_gate.md` at `002e0e83` carries ONE `# ` title and ZERO `^## ` headings, and `docs/roadmap/features/T5_F009.md` at `d8d48b7f` opens its `## Built State` at line 94 with one blank line above it — every numeral true. THE HANDBACK IS 100 LINES against the 100 AGENTS.md allows a per-commit table of more than five commits, carries every mandated section and an item-status row for each of C0a, C0b, C1, C2, C3 and C4, and repeats its block's four-line `Fortschritt:` VERBATIM. ONE INCOMPLETENESS, AND IT IS AN INSTANCE OF OPEN R-0494 RATHER THAN A NEW ID: that block's G6 ordered its readings at BOTH the round base and C2, and the handback's one-line G6 entry gives `Done:`, `Landed: ` and the `Gate: R` key count at the base only, routing the C2 half of those three to a round report that dies with the session. All three reproduce true at `6cae6a53` — 3, 0, and 31 over 31 DISTINCT — so nothing false landed, and per checklist item 30 the evidence is added to R-0494 here rather than minted as a second id. The tension is the block's own: its G6 ordered fourteen readings across two points while its G9 ordered one line per gate under a 100-line cap, so the worker had to choose which readings survived, and it chose the discriminating ones.
<<<END LEDGER32

<<<SLICE CANDIDATES32
# Closure Candidates — carrier of record

> Written per docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate
> findings", disk-vehicle rule, operator ruling 2026-08-01). Read at Window-1
> session bootstrap (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present at
> feature-claim time is a block condition.

EMPTY. The two entries this file carried — a gate that counted a markdown
construct its named target does not contain, and an anchoring control ordered as
a maximum that coincides whenever the round's own new id is the ceiling — are
registered as R-0646 and R-0647 in this branch's review record, by the same round
that empties this file.
<<<END CANDIDATES32
