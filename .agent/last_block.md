── STEP CLOSURE PART 3 / F040 — ROUND 20 (BRANCH TERMINATOR) ─
Goal:        STATUS_closure_protocol.md algorithm steps 3-5: flip F040's
             STATUS line to `[x]`, sync README (accepted count, tier table,
             capability paragraph) IN THE SAME COMMIT as the STATUS flip
             (R-0154: README and STATUS may never disagree in any
             committed state), record one closure-review candidate this
             round's own README audit surfaced, then open the PR. This is
             the LAST round of F040's build — Rule A4 renders the STATUS
             edit as the final content commit on the branch, with the one
             candidates-only exception DECISION amend0827 D2 permits.

Bundle:      C0a save this block verbatim · C0b mirror it · C1 the plan ·
             C2 the record (the R19 verdict) · C3 THE CLOSURE COMMIT
             (STATUS.md + README.md + `.agent/handoff.md`, one commit,
             per the F033/179d4031 precedent) · C4 the candidates-only
             commit (DECISION amend0827 D2).
Change:      EXACTLY these paths and nothing else, across the round.
               `.agent/authored/f040-r20.md`               (C0a, new)
               `.agent/last_block.md`                       (C0b)
               `.agent/plan.md`                             (C1)
               `.agent/live_review.md`                      (C2)
               `docs/roadmap/STATUS.md`                     (C3)
               `README.md`                                  (C3)
               `.agent/handoff.md`                          (C3 — the
                 handback IS this commit; there is no separate handback
                 commit this round, matching the F033 closure precedent
                 where `.agent/handoff.md`, `README.md` and
                 `docs/roadmap/STATUS.md` landed in one commit)
               `.agent/candidates.md`                       (C4 — its ONLY
                 path, per DECISION amend0827 D2)
             NOTHING UNDER `packages/`, `apps/` or `tests/` IS EDITED.
             `scripts/self_use_queue.json` IS NOT EDITED — precondition 6
             read NONE (queue exhausted) at round 18 and nothing in this
             round changes that reading.

Constraints:
 1. APPLY EVERY AUTHORED SLICE/PAIR BYTE FOR BYTE. If one looks wrong,
    apply it anyway and DECLARE the objection in the handback. Never
    repair one.
 2. THE COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4 and it is fixed.
 3. C1 IS THE FIRST SUBSTANTIVE COMMIT (§3 item 23).
 4. RECORD20 IS APPENDED to `.agent/live_review.md`, never inserted, under
    the same generalized reading round 19's own constraint 3 established
    (read round 19's committed `.agent/last_block.md` — i.e. this round's
    OWN base state, before C0b overwrites it — if the exact wording is
    needed).
 5. THE STATUS LINE IS A REPLACE PAIR, not an append. At this round's
    base, confirm `- [~] F040 — Completion/return digest\n` occurs in
    `docs/roadmap/STATUS.md` EXACTLY ONCE, then replace that exact
    substring with STATUSLINE below (also exactly once, and note
    STATUSLINE's own trailing `\n` — the replacement carries the line's
    own newline, nothing is duplicated or dropped). Report the pre-commit
    occurrence count (must be 1) and the post-commit count of the OLD
    string (must be 0) and of STATUSLINE (must be 1).
 6. README GETS THREE PAIR-REPLACEMENTS, each independently narrow — do
    not touch any other README text:
      (i)   `63 of 257 registered items accepted. Next: the first
             unchecked item in docs/roadmap/STATUS.md.` →
            `64 of 257 registered items accepted. Next: the first
             unchecked item in docs/roadmap/STATUS.md.`
      (ii)  `| 5 | Operator Cockpit | 11 | 31 |` →
            `| 5 | Operator Cockpit | 12 | 31 |`
      (iii) an INSERTION, not a replace — per "insert-after must read what
            follows": the anchor is the exact substring
            `not a gate).\n\nFull per-feature state:` (confirm it occurs
            exactly once at this round's base); insert README_PARAGRAPH
            below, as its own new paragraph, BETWEEN `not a gate).\n\n`
            and `Full per-feature state:` — i.e. the committed text reads
            `not a gate).\n\n` + README_PARAGRAPH + `\n\nFull per-feature
            state:` in that exact order, so the paragraph sits after
            F257's own paragraph and before the "Full per-feature state"
            line, matching the existing per-feature-paragraph convention.
    Confirm each of the three FROM strings occurs exactly once at the
    round's base (the reviewer measured this immediately before authoring
    the block: 1, 1 and 1) and report the same measurement fresh.
 7. `tests/docs/test_docs_consistency.py` MUST BE RUN AFTER C3, in the
    PRIMARY CHECKOUT, and MUST PASS — this is the mechanical proof the
    three README pins (accepted count, tier Done cell, and every README-
    listed accepted feature actually being accepted) all hold together.
    A red here is a STOP condition per constraint 10, not a number to
    silently adjust.
 8. THE CLOSURE-CANDIDATE FINDING (C4). This round's own README audit
    found that `README.md`'s "Accepted in Tier 5 so far:" prose list
    (the paragraphs constraint 6(iii) extends) omits F033's own paragraph
    — F033 IS counted in both the accepted-count pin and the Tier 5 Done
    cell (both pins pass regardless, since neither test reads the prose
    list's completeness — only `test_the_readme_reports_the_accepted_
    foundation_and_no_later_feature` reads it, and only in the direction
    "every NAMED feature is accepted", never the reverse), but a reader
    scanning the prose paragraphs for F033's capability finds nothing.
    This is NOT F040's defect to fix inline (STATUS_closure_protocol.md's
    "Closure-candidate findings": a finding raised DURING a closure review
    is recorded as a CANDIDATE only, no R-id spent, disk vehicle
    `.agent/candidates.md`, in a commit AFTER the closure commit per
    DECISION amend0827 D2). Append ONE entry to `.agent/candidates.md`
    (currently EMPTY — confirm that at this round's base) describing:
    what's missing (F033's capability paragraph in README's Tier 5 list),
    where (README.md, between F257's and F040's paragraphs once this
    round's C3 lands), source feature (F040, discovered during its own
    closure's README audit), and today's date.
 9. RE-READ `.agent/STOP` FROM DISK BEFORE THE FIRST COMMIT AND AGAIN
    BEFORE C3 AND AGAIN BEFORE C4. If it appears, finish the commit in
    hand, write the handback and stop.
10. IF constraint 7's suite goes red, or any pair/insertion in constraints
    5-6 does not measure exactly as stated, STOP after finishing the
    commit in hand — do not repair the underlying text in this round;
    hand back with the exact mismatch.
11. AFTER C3 IS PUSHED, open the PR per the AGENTS.md PR workflow: title
    under 70 characters, body with what/why, key decisions (link
    `docs/roadmap/features/T5_F040.md`'s Amendments/Decisions if any,
    and this feature's D1-D10), how to review, a changed-files table
    covering the WHOLE branch (not just this round), the latest verdict
    (R19's PASS, booked this round as RECORD20), open-findings count
    (unchanged this round), and runtime actuals (rounds, wall clock,
    models/tokens where the ledger has them — `not-measured` beats a
    guess). DO NOT MERGE THE PR (G1 of self_drive_protocol.md: merges
    happen only at the Open PR Gate, never in the session that opened the
    PR). Report the PR URL/number in the handback.

Done when: every gate below is executed, each with its REAL exit code or
REAL measured value.

 G1 TRANSPORT, at C0b. sha256 and byte length of
    `.remedy-wt/f040-r20-block.md`, `.agent/authored/f040-r20.md` and
    `.agent/last_block.md`; all three equal.
 G2 THE PLAN, at C1. `.agent/plan.md` byte-equal to PLAN20; line count
    under 50; holds `## Goal`, `## Next Steps`, `\bF\d{3}\b`.
 G3 THE RECORD APPEND, at C2. Reading (a) and (b) per constraint 4, with
    the negative control inside a disposable worktree.
 G4 THE LEDGER, at C2. Distinct registered/resolved/`DECISION F040 D`
    ADDED and REMOVED (report none of either), `^Gate: F040 R19 — ` lines
    0 before 1 after, open count unchanged.
 G5 THE STATUS AND README PAIRS, at C3. Every occurrence count named in
    constraints 5-6, before and after, exactly as stated; the README
    paragraph's ordering (F257's paragraph, then README_PARAGRAPH, then
    the "Full per-feature state" line) confirmed by direct substring
    search on the committed file.
 G6 `tests/docs/` GREEN, at C3. Real exit code of
    `python3 -m pytest tests/docs/ -q` in the primary checkout at the C3
    commit; must be 0. Report the passed count.
 G7 THE CANDIDATE, at C4. `.agent/candidates.md` was EMPTY at this round's
    base (confirm); the committed file names F033's missing README
    paragraph, F040 as source, and a date; no R-id appears in it.
 G8 THE TREE AND THE PR, at C4/after. `git status --porcelain` empty;
    `git worktree list` one line; branch pushed; the PR exists, targets
    `main` from `feature/f040-completion-digest`, is not a draft, and is
    NOT merged.

Handback:    the handback IS C3 (per the Change set above) — this round
             has no separate final handback commit the way earlier rounds
             did; C4 (the candidates-only commit) follows it and is
             declared as such, exactly as constraint 8 and the F033
             precedent (`179d4031` then `4829e697`) both show. C3's
             `.agent/handoff.md` still carries every mandated section:
             SESSION 4, round 20, the range, one line per gate, the item-
             status table, the PR reference (added once C3 is pushed and
             the PR opened — if the handback text must be finalized before
             the PR exists, name the PR in a short PS-style addendum
             consistent with R-0371's own resolution: never fabricate a
             number before its tool runs), deviations, and the
             feature-done banner (STATUS_closure_protocol.md algorithm
             step 7: "End Window 1 with the feature-done banner").
──────────────────────────────────────────────────────────────

<<<BEGIN PLAN20
# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 4, round 20 — CLOSURE.

## Goal
Coming back is calm: a digest endpoint condenses state, cost with its basis, top
ownership entries, open decisions and ONE primary action into a hero card, shown
at job end or on the first UI open after absence — the "what happened while I
was gone" answer in one glance.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the spec decisions D2 to D10 | done | rounds 2-9 |
| T001 the composition, endpoint, goldens | done | rounds 3-5, all PASS |
| T002 the client digest seam through the mount | done | rounds 6-14, all PASS |
| T003 CLI parity + the client end-to-end | done | rounds 15-16, all PASS |
| the integration gate | done | round 17, PASS |
| closure preconditions + Built State | done | round 18, all six CLEAR/NONE |
| closure evidence job + review zip | done | round 19, READY_FOR_REVIEW |
| STATUS line + README sync + PR | in progress | this round |

## Next Steps
1. This round flips F040 to `[x]` in STATUS.md, syncs README (accepted
   count, Tier 5 Done cell, F040's capability paragraph) in the SAME
   commit, records one closure-candidate finding (F033's own missing
   README paragraph, found during this round's audit — not F040's to
   fix), and opens the PR.
2. The PR is NOT merged this session (self_drive_protocol.md G1;
   STATUS_closure_protocol.md algorithm step 6) — it merges at the next
   feature's Open PR Gate, or the operator merges it manually at any time.
3. End Window 1 with the feature-done banner once the PR is open and the
   handback is written.
4. Wiring `onOpenDecisions`/`onPrimaryAction` for real needs its own
   resolution design (D5's "in-page action") and is not yet scheduled —
   documented in the Built State section, carried forward as a known
   post-closure item, not a blocker.

## Risks
- R-0570, R-0752 and R-0755 stay OPEN and are routed to the paydown branch;
  none is F040's to fix. R-0753 stays OPEN as this feature's documented risk.
- `browserDigestPort.ts`'s open risk (a real browser refusing a write) is
  still unaddressed and still deferred to whichever round first meets it.
<<<END PLAN20

<<<BEGIN RECORD20
Gate: F040 R19 — THE CLOSURE EVIDENCE JOB AND REVIEW ZIP (STATUS_closure_protocol.md algorithm steps 1-2). VERDICT PASS. THE REVIEWER RE-RAN THE ROUND'S OWN VERIFICATION INDEPENDENTLY RATHER THAN TAKING THE HANDBACK'S NUMBERS, reading the diff `4db6c088..bdf78bb7` in full. THE TRANSPORT: `.remedy-wt/f040-r19-block.md`, `.agent/authored/f040-r19.md` and `.agent/last_block.md` sha256-equal at `73b416a8224fe6cd519242037268d90c108e6cc7fc238a8f9fc8af6c63f07f80`, 16502 bytes, all three, against the reviewer's own scratch original. THE PLAN: byte-equal to PLAN19, 2350 bytes, 46 lines. THE RECORD APPEND: base 1745755 bytes trailing-newline-terminated; `base + "\n" + RECORD19` equals the committed 1749253-byte file exactly. THE LEDGER, recomputed by difference: registered/resolved ADDED `[]` REMOVED `[]` (317/55 distinct both sides), `Gate: F040 R18 —` lines 0 before → 1 after. THE NINE VERIFICATION RUNS: the reviewer independently re-ran three of the nine (`test_job_digest.py`, `test_job_digest_cli.py`, and the vitest-foundation node) as a spot check: REAL EXIT 0, 56 passed (46+9+1), 0 failed, 0 skipped — matching the block's own stated expectations for those three exactly; the handback's own per-run table for the remaining six is internally consistent with the total the bundle records. THE ZIP WAS VERIFIED FROM THE PACKAGE ITSELF, not from a printed claim: the reviewer independently recomputed the sha256 of `/home/decodeux/Repos/remedy-history/zips/remedy-review-20260830-033225-READY_FOR_REVIEW.zip` — `26bacc72356bea20d765736996cb353033d087c328e7af0156548a533d164be1`, matching exactly — then opened it and read `.review_zip_manifest.json` directly: `committed_review_subject.head_commit` = `5281987a142b97f222256c987d36c009ae7ab3ae`, exactly this round's own C2 commit SHA; `package_status` = `READY_FOR_REVIEW`; `ready_gate_matrix.ok` = True; `review_subject_evidence_alignment.verdict` = `PASS` with zero issues. THE ROUND PASSES: every path in the change set matches the block's fixed order (C3 wrote no tracked path, exactly as specified — its outputs are gitignored), the tree is clean and pushed, no `tmp/*` branch or extra worktree survives. F040 is CLEAR to close: STATUS_closure_protocol.md preconditions 1-6 all read CLEAR/NONE as of round 18, and this round's own evidence job and zip satisfy the remaining algorithm steps 1-2. No new finding is raised by this review.
<<<END RECORD20

<<<BEGIN STATUSLINE
- [x] F040 — Completion/return digest (T001–T003 complete; accepted 2026-08-30 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f040-closure · package remedy-review-20260830-033225-READY_FOR_REVIEW.zip · SHA-256 26bacc72356bea20d765736996cb353033d087c328e7af0156548a533d164be1 · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD 5281987a142b97f222256c987d36c009ae7ab3ae)
<<<END STATUSLINE

<<<BEGIN README_PARAGRAPH
F040 completion/return digest (a hero card condensing state, cost with its
basis, open decisions and one recommended action into a single glance, shown
at job end or on the first UI open after an absence; the same envelope is
served to `remedy job digest <id>` so the CLI and the route can never
disagree; a dismissal persists per job and new activity re-arms it).
<<<END README_PARAGRAPH
──────────────────────────────────────────────────────────────
