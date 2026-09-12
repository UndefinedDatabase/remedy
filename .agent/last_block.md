# STEP T003 — F275 ROUND 78 — restore the operator amendment this branch lost in a merge

## Goal

The operator's merge of `main` into this branch resolved the conflict in
`docs/agents/self_drive_protocol.md` by taking the branch side, so all four paragraphs of
operator amendment amend0911-feedback are absent from the document that governs this loop,
while the eleven other files that amendment touched came across intact and every one of them
still cites it. Restore the four paragraphs, derived from two committed blobs rather than
authored, in their chronological place after the amend0908 paragraph this branch added. Book
the round 77 PASS verdict and its two prose slips. Register the loss as `R-0881` and resolve
it in the same round. NO PRODUCTION LINE MOVES.

## Bundle — the ordered commit sequence

The sequence is EXACTLY this. Nothing is added, dropped or reordered. Each commit stages
exactly ONE path.

- C0a save the block as authored text — `.agent/authored/f275-r78.md`
- C0b mirror the block into the last-block state file — `.agent/last_block.md`
- C1 make the plan current for round 78 — `.agent/plan.md` — THE FIRST SUBSTANTIVE COMMIT
- C2 book the round 77 verdict and register `R-0881` — `.agent/live_review.md`
- C3 append the round 77 prose slips — `.agent/prose_slips.md`
- C4 restore the amendment — `docs/agents/self_drive_protocol.md` — THE ROUND'S SUBSTANCE
- C5 record DECISION F275 D52 — `.agent/decisions.md`
- C6 resolve `R-0881` — `.agent/live_review.md`
- C7 the round 78 handback — `.agent/handoff.md`

## Change — the exact path set

These paths and NOTHING ELSE:

    .agent/authored/f275-r78.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    docs/agents/self_drive_protocol.md
    .agent/decisions.md
    .agent/handoff.md

`.agent/live_review.md` is staged twice, at C2 and at C6, because the registration of a finding
and the resolution of that finding cannot honestly sit in one commit — the resolution states
that C4 landed, and C4 is between them. Every other path is staged once.

NOTHING under `packages/`, `apps/` or `tests/` is touched. `.agent/STOP` is NOT created, staged,
deleted or read for its contents beyond the existence check constraint 7 orders.

## What this round is, stated before the recipe

THE DEFECT IS A LOST OPERATOR ORDER, NOT A STALE DOCUMENT. Commit `e262f420`, the operator's
merge of `main` into this branch, has parents `b916c1a1` (this branch) and `d0aa833b` (`main`,
the merge of pull request 248, amendment amend0911-feedback). That amendment changed twelve
files. Eleven of them arrived on this branch: `.agent/decisions.md`, `.agent/operator_questions.md`,
`docs/roadmap/STATUS_closure_protocol.md`, five feature files under `docs/roadmap/features/`,
`docs/system/vocabulary.md` among them. The twelfth, `docs/agents/self_drive_protocol.md`, did
not: `git diff --name-only b916c1a1 e262f420` lists the eleven and not it, and the file's blob
at `e262f420` is byte-identical to its blob at `b916c1a1`. The merge took the branch side whole.

WHAT THE FOUR PARAGRAPHS SAY, because the loss is not cosmetic. Rule A binds every open finding
to exactly one owning feature and forbids losing one at a closure. Rule B installs the rolling
findings-paydown feature, one per five features. Rule C creates `.agent/operator_questions.md`
and states what a session must write there and what its handback's `## Next` must say about it.
The fourth paragraph, amend0911-f275-to-scope, LIFTS F275's soft limit of 20 sessions and 60
rounds without a replacement number, so that no scope report, no session-limit banner and no
limit line is owed by this feature any more. All four bind by `.agent/decisions.md` DECISION
amend0911-feedback D8 and D9, which are on this branch and which name the protocol file as the
place the rules live. So the branch carries decisions that point at text the branch does not have.

WHY IT IS NOT MERELY THIS BRANCH'S PROBLEM, and this is the reason the round is spent now rather
than at closure. The merge base of this branch and `main` now INCLUDES `d0aa833b`. A later merge
of this branch into `main` therefore resolves that path in favour of this branch's version, and
`main` loses the four paragraphs. The defect propagates in the direction of the operator's own
document, silently, through an ordinary merge nobody would look at twice.

THE REPAIR IS DERIVED, NOT AUTHORED, which is why this block ships no slice for it. Retyping
sixty-five lines of operator text into a block and back out again is the one transport this
workflow cannot prove, per item 37 of `docs/agents/planner_reviewer_prompt.md` §3. The bytes
instead come out of two committed git objects, and the gate that checks them is a pair of
round-trip identities rather than a digest of something a reviewer typed.

## The derivation C4 performs

Let `M` be `git show d0aa833b:docs/agents/self_drive_protocol.md` and `B` be the same path at
this round's base. Compute `p`, the number of leading lines on which `M` and `B` agree, and `s`,
the number of trailing lines on which they agree. Then `M[p : len(M)-s]` is the block of text
`main` has and this branch lacks, and `B[p : len(B)-s]` is the block this branch has and `main`
lacks. Measured by the reviewer at `e262f420`: `p` is 246, `s` is 13, the first block is 65
lines and is the four amend0911 paragraphs, the second is 20 lines and is the amend0908
paragraph this branch added.

The restored file is `B` with a single blank line followed by those 65 lines inserted
immediately after line `p + 20` — that is, directly after the amend0908 paragraph's last line,
``amend0908 paragraphs in `docs/roadmap/features/T2_F275.md`.`` — and nothing else changed. The
inserted region is 66 lines. The result is 345 lines.

PLACEMENT IS CHRONOLOGICAL AND IT IS A CHOICE, so it is stated rather than assumed. On `main`
the four paragraphs sit where the amend0908 paragraph sits here, because DECISION
amend0911-feedback D10 records that amend0908 did not exist at `main` at the time and the new
text was inserted after the amend0906 paragraph instead. Here amend0908 exists, and the
amend0911-f275-to-scope paragraph overrides amend0908 rule 1 by name, so the overriding text
must read AFTER the text it overrides. Both paragraphs survive; neither is edited.

## Constraints

1. EVERY SLICE IS APPLIED BYTE FOR BYTE. A slice is never edited, reflowed, re-wrapped or
   corrected, not even where it is wrong. A discrepancy is DECLARED in the handback with the
   measurement that shows it, and the slice still lands as written.
2. C4 WRITES NO AUTHORED TEXT. Its bytes are computed from `d0aa833b` and from the base blob by
   the derivation above. If the computed insertion is not exactly 66 lines, or the base file is
   not 279 lines, STOP and declare it — do not proceed on an adjusted recipe.
3. THE TWO PROSE-SLIP LINES ARE EXTRACTED, NOT TYPED. They are the two non-blank lines between
   the heading that begins `## Authored text for round 78 to book` in
   `git show b916c1a1:.agent/handoff.md` and the next line beginning `## `. That heading occurs
   exactly once in that blob and the region holds exactly two non-blank lines; if either reading
   differs, STOP and declare it.
4. C1 IS THE FIRST SUBSTANTIVE COMMIT. Item 23 of §3 binds it: this round touches the finding
   ledger, so the plan advances before the ledger does, and only the two block-save commits
   precede it.
5. NO COMMIT EXCEEDS 500 INSERTIONS. Measured per commit with `git show --numstat`.
6. NO `gh` COMMAND AND NO `remedy` CLI COMMAND IS RUN. No pull request is created, edited or
   merged. No branch is created or deleted. No merge. No force-push. No history rewrite.
7. READ `.agent/STOP` BEFORE C0a AND AGAIN BEFORE C7. It does not exist at this round's base.
   If it appears, finish the commit in hand, write the handback recording both readings with
   their timestamps, push, and stop — do not stage it, do not delete it.
8. THE BLOCK'S OWN SIZE: this block is 347 lines TOTAL and 275 of them are PROSE, against the
   caps DECISION F085 D6 and D5 set at 490 and 400. Report both numbers as measured.
9. GATES RUN AT C6, STRICTLY BEFORE C7, so the handback can quote every one of them. Each gate
   writes its transcript to a file under `.remedy-wt/` and the handback reports the REAL exit
   code read back out of that file, one line per gate.
10. THE NEGATIVE CONTROLS OF G4 MUTATE A BYTE STRING IN MEMORY AND WRITE NO FILE. No worktree is
    created for them and the primary checkout is never modified, so guardrail G5 of
    `docs/agents/self_drive_protocol.md` is not engaged by this round at all.
11. `R-0881` IS REGISTERED AT C2 AND RESOLVED AT C6, and the resolution names constraint 4 and
    this constraint as the ordering that makes its claim true, never a SHA — item 20's R-0524
    carve-out, because the commit it describes does not exist when the slice is authored.

## Done when — the gates

### G1 — transport, the block budget, the insertion cap

(a) `.agent/authored/f275-r78.md` at C0a is byte-identical to the reviewer's scratch original at
`.remedy-wt/r78_block.md`, by `cmp`. This is the PRIMARY proof and not the §4.9 digest fallback.
(b) `.agent/last_block.md` at C0b is byte-identical to the COMMITTED C0a blob, not to any
working copy.
(c) Each of the three authored slices below matches the sha256 stamped on its own BEGIN marker,
computed over the bytes strictly between the BEGIN line and the END line with the trailing
newline kept.
(d) The block re-measures at the TOTAL and PROSE line counts constraint 8 states, where PROSE is
TOTAL minus the lines lying between BEGIN and END markers.
(e) No line of the block outside a slice is a run of a single repeated character.

### G2 — the plan

`.agent/plan.md` at C1 is byte-identical to slice PLAN78; it is at most 50 lines; it carries
exactly one `## Goal` and exactly one `## Next Steps`.

### G3 — the record, with full forensics

For each of the three appends — RECORD78 at C2, DEC78 at C5, DONE78 at C6:
(i) READER A, bytes: the pre-commit blob of that path is a byte-exact PREFIX of the post-commit
file, and the slice is a byte-exact SUFFIX of it.
(ii) READER B, structure: the LAST N blank-line-separated units of the post-commit file equal
the slice's N paragraphs IN ORDER, where N is COUNTED by the script from the slice and is never
a number this block asserts.
(iii) NEGATIVE CONTROL: flip one byte inside the FIRST appended paragraph, in the ASCII letter
range `A`-`Z` or `a`-`z` so the flip cannot land inside a multi-byte sequence, and require BOTH
readers to REJECT. Not the last paragraph — a control there leaves reader B unexercised.
(iv) The DELETION column of each of the three commits is ZERO, so no landed paragraph is
rewritten.
(v) RECORD78's `Gate:` header is compared as a pattern against the headers already in
`.agent/live_review.md` and must match their repeating shape and duplicate none of them.

### G4 — the restore, and this is the gate the round exists for

All readings are taken over the file as committed at C4.
(i) `git show --numstat` for C4 reads exactly 66 insertions and 0 deletions for the path.
(ii) SLICE IDENTITY: the 66 inserted lines are byte-identical to a blank line followed by
`M[p : len(M)-s]` as computed in the derivation above.
(iii) ROUND TRIP A: the committed file with those 66 lines removed is byte-identical to the
path's blob at this round's BASE. Nothing this branch had was lost.
(iv) ROUND TRIP B: the committed file with the amend0908 paragraph's own lines TOGETHER WITH the
single blank line following them removed — 21 lines in all, beginning at line `p` — is
byte-identical to `d0aa833b:docs/agents/self_drive_protocol.md`. Nothing `main` had was lost.
(v) The committed file is 345 lines, ends with a newline, and holds exactly four lines beginning
`Operator amendment amend0911`. Every line beginning `Operator amendment` is preceded by a blank
line, so no two paragraphs ran together.
(vi) NEGATIVE CONTROLS, each a mutation of the committed bytes IN MEMORY per constraint 10, and
each required to be REJECTED by the CONJUNCTION of (ii), (iii) and (iv). The mutations are:
flip one ASCII letter inside the first inserted paragraph; delete one line from the inserted
region; delete one line of the amend0908 paragraph; delete one line of the shared tail. Report
the three booleans for EVERY mutation listed and for the unmutated control, and report the
number of mutations run. NO SINGLE READING CATCHES THEM ALL — the reviewer measured that the
letter-flip leaves (iii) TRUE and the shared-tail deletion leaves (ii) TRUE — so the gate is
the conjunction, and the handback states it as the conjunction rather than as three passes.

### G5 — the prose slips

(a) The extraction of constraint 3 returns exactly two non-blank lines, each beginning
`2026-09-12 · F275 R77 · `, neither carrying trailing whitespace.
(b) The bytes appended at C3 are a blank line, the first extracted line, a blank line, and the
second extracted line, and the post-commit file equals the pre-commit blob followed by exactly
those bytes.
(c) `git show --numstat` for C3 reads exactly 4 insertions and 0 deletions.

### G6 — the guards on the target and the colours

Every command runs in the PRIMARY checkout, never a worktree.
(a) `python3 -B -m pytest tests/test_agent_tooling.py -q` at this round's BASE and again at C4.
The reviewer measured 10 passed and 1 skipped at the base. This file holds the only two tests in
the suite that read the restored document, and both are substring-presence pins, so a pure
insertion cannot redden them — the gate exists to prove that claim rather than to assume it.
(b) `python3 -B -m pytest tests/docs/ -q` at C4. The reviewer measured 306 passed at the base.
(c) THE CANARY: `python3 -B -m pytest tests/cli/test_golden_path.py -q` at C6. The reviewer
measured 42 passed at the base.
(d) `ruff check .` at C6 reports 26 rows against the frozen ceiling of 26. The round adds no
Python, so any movement here is a finding.

### G7 — the tree, the path set and the open set

(a) `git status --porcelain` is the EMPTY STRING at C6.
(b) `git worktree list` shows the primary checkout alone.
(c) The changed-path set of the whole range equals the eight paths of the Change section, with
MISSING and EXTRA both empty; the count of changed paths under `packages/`, `apps/` or `tests/`
is ZERO.
(d) The open set BY DISTINCT ID — registered `- R-xxxx — ` ids minus ids carrying at least one
`Done: R-xxxx — ` line — reads 87 at the base, 88 at C2, and 87 at C6. `R-0880` is OPEN at all
three readings. Report the membership difference between the base and C6 readings, which must be
empty.

### G8 — the per-commit insertion counts

`git show --numstat` for each of C0a through C6, reported one line per commit, each under 500.
The handback commit C7 is NOT covered: its own numbers cannot exist while its text is written
(item 14), and under self-drive they are not routed to a round report either — the reviewer
measures them at the next gate and records them in that round's ledger entry (item 31).

## Handback

Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`: the state block with the
SESSION NUMBER, which is 28, and the round, which is 78; the range; the per-commit table whose
`+/-` cells are read from `git show --numstat` and compared CELL BY CELL against G8's numbers,
with the comparison printed; external actions; one line per gate with the REAL exit code read
back out of its transcript file; the item-status table; deviations; next steps.

NO SCOPE REPORT AND NO SESSION-LIMIT BANNER IS OWED. The amend0911-f275-to-scope paragraph this
round restores lifts F275's limit without a replacement number, and DECISION amend0911-feedback
D8 binds it on this branch already. State that in one sentence and do not print the banner.

STATE THE OPERATOR-QUESTIONS COUNT. Restored rule C requires the handback's `## Next` to carry
`Operator questions open: <n>`, read from `.agent/operator_questions.md`, which currently reads
`EMPTY — nothing is waiting on the operator.` and therefore gives 0. This round writes nothing
to that file: the ruling it records is not reversible by the operator in the sense rule C means,
because it restores the operator's own text rather than deciding anything on the operator's
behalf. Say so in one sentence.

## SLICE PLAN78 — replaces `.agent/plan.md` at C1

BEGIN PLAN78 sha256=f6dbfa9bdd9ce81a0e1ccbe655680c3a81fe28de6b1b0fb09f3e183fd122dd74
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, and the classic runner's whole
command surface is gone as of round 34.

## Current Step

ROUND 78 RESTORES AN OPERATOR AMENDMENT THIS BRANCH LOST IN A MERGE. The operator's merge of
`main` into this branch resolved `docs/agents/self_drive_protocol.md` by taking the branch side,
so all four paragraphs of amendment amend0911-feedback — finding ownership, rolling paydown, the
operator questions file, and the lifting of this feature's own session and round limit — are
absent from the document governing this loop, while the eleven other files that amendment
touched arrived intact and every one of them cites it. The restored bytes are derived from two
committed blobs rather than authored. The loss is registered as `R-0881` and resolved in the
same round. The round 77 verdict and its two prose slips are booked.

## Next Steps

1. Carry the 19 surviving over-selection frames back to the ruled sites that produce them,
   which the corrected set does not remove because the owner check REFUSES rather than decides
   on their receivers. That is the residue `R-0880`'s second obligation still names.
2. The resolver collapse DECISION F260 D5 places in T003, which DECISION F275 D37 names as the
   home of the id-SHAPE seam behind the three largest residue classes. Production code, so a
   SPLIT round with mutation red-proofs.
3. THE FLIP, on the corrected set DECISION F275 D51 rules, carrying DECISION F275 D48's
   obligations: the full suite is the backstop, and the thin set is re-derived before the flip
   with any site fallen to zero witnesses treated as a stop.
4. Then the classic store, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20 sessions
  and 60 rounds without a replacement, so this feature closes only at full scope and owes no
  scope report. Until C4 of this round lands, the document on this branch still states the
  withdrawn numbers, which is the defect `R-0881` names.
- THE CORRECTED SET IS BETTER, NOT RIGHT. 19 over-selection frames survive it on classes the
  owner check refuses to decide, and 1204 bad nodes is the best reading this chain has taken and
  is not near green.
- The open set is 87 by distinct id at this round's base, with `R-0880` open. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN78

## SLICE RECORD78 — appended to `.agent/live_review.md` at C2

BEGIN RECORD78 sha256=980607cc050f27c1fd12f2a477393492ad35edf5c6b45e0bfdc118916ade98f7

Gate: F275 R77 — the F275 round 77 entry. VERDICT PASS. Written by the planner and reviewer of session 27 after reading the committed range `75cc221e`..`8b02f1e8` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs, and carried in `.agent/handoff.md` at `b916c1a1` as the durable carrier operator amendment amend0827-process-diet rule 1 names. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 78, per that same rule. The round turned DECISION F275 D50's inference into a construction: the shipped owner check of DECISION F275 D47 contradicts 13 of the round 53 re-keyed set's 2198 sites, every one of the 13 is among the 60 the plain re-derivation drops, and the corrected set — that set minus exactly those 13, at 2185 sites — is that difference AS A SET rather than merely at that count. The same check exits at 13 contradictions over the round 53 set and at ZERO over the corrected one, which is the discriminator a guard needs at both ends. Run as a third arm at `ef75e213` against the same control it FIXES 23 test nodes and BREAKS 0, and `Mission.job_id` and `QueueEntry.job_id` leave the residue entirely. All three authored blobs were byte-identical to the reviewer's originals, the block re-measured at 397 lines TOTAL and 316 PROSE, all nine per-commit insertion cells agreed with `git show --numstat`, and the open set was 87 by distinct id at the base, at C5 and at the tip with `R-0880` open at each. DECISION F275 D51 rules the corrected set the flip's input, and `R-0880` stays OPEN because 19 over-selection frames survive it on classes the owner check refuses rather than decides.

THE VERDICT'S OWN LIMIT, RECORDED WITH IT. Session 27's transport proof walked the reviewer's scratch original, the committed `.agent/authored/` blob and the working copy — three artefacts of which two are the worker's own output — and it therefore established that the worker was SELF-CONSISTENT and nothing about the bytes the worker RECEIVED, which is the obligation item 37 of `docs/agents/planner_reviewer_prompt.md` §3 places on a verdict under this workflow. That limit is stated here because the record, not the session, is what a later reader has.

- R-0881 — High, THIS BRANCH LOST FOUR PARAGRAPHS OF A BINDING OPERATOR AMENDMENT IN A MERGE, AND THE LOSS PROPAGATES TOWARDS `main`. Raised by the planner and reviewer of session 28 during the Phase 0 state probe, before any round was planned. Commit `e262f420`, the operator's merge of `main` into this branch, has parents `b916c1a1` and `d0aa833b`; `d0aa833b` is the merge of pull request 248, operator amendment amend0911-feedback, which changed twelve files. Eleven arrived — `git diff --name-only b916c1a1 e262f420` lists exactly those eleven — and the twelfth, `docs/agents/self_drive_protocol.md`, did not: its blob at `e262f420` is `cb2f3cb5`, identical to its blob at `b916c1a1`, where `main` carries `c54ee2c3`. The conflict was resolved by taking the branch side whole, and the 65 lines `main` added are absent. THE MISSING TEXT IS FOUR RULES, not a note: rule A binds every open finding to one owning feature, rule B installs the rolling findings-paydown feature, rule C creates `.agent/operator_questions.md` and states what every handback must report about it, and the amend0911-f275-to-scope paragraph LIFTS F275's soft limit of 20 sessions and 60 rounds without a replacement number. All four bind this branch already, by DECISIONs amend0911-feedback D8 and D9 in `.agent/decisions.md`, which arrived with the other eleven files and which name this very document as where the rules live — so the branch holds decisions pointing at text the branch does not have. WHY HIGH RATHER THAN MEDIUM: the merge base of this branch and `main` now includes `d0aa833b`, so a later merge of this branch into `main` resolves that path in favour of this branch and DELETES the four paragraphs from `main`. An operator order is reversed repo-wide by an ordinary merge that no reader would examine. THE GUARD THAT EXISTS DID NOT SEE IT: `tests/test_agent_tooling.py::test_self_drive_protocol_states_its_guardrails` pins six substrings of this document — the Open PR Gate, never force-push, the STOP file, the worker subagent, the worktree and the handoff — and every one of them survived the drop, because the test pins the GUARDRAILS and no amendment. A presence pin over a document that grows by amendment cannot see an amendment that never arrived. FIX: restore the four paragraphs, byte-derived from `d0aa833b` rather than retyped, in their chronological place after the amend0908 paragraph this branch added, so that the paragraph overriding amend0908 rule 1 reads after the text it overrides; prove the restoration by the two round-trip identities that nothing of either side was lost. Owner: F275.
END RECORD78

## SLICE DEC78 — appended to `.agent/decisions.md` at C5

BEGIN DEC78 sha256=ed5a8464dd110782696949f51096ceef1e293667c0a658503c130aea58928ad9

## DECISION F275 D52 (2026-09-12, F275 round 78) — the amend0911-feedback paragraphs are restored to `docs/agents/self_drive_protocol.md` by DERIVATION from two committed blobs, and placed after the amend0908 paragraph rather than where `main` has them

CONTEXT. The operator's merge `e262f420` brought eleven of amendment amend0911-feedback's twelve files onto this branch and resolved the twelfth, `docs/agents/self_drive_protocol.md`, in favour of the branch, dropping the four paragraphs `main` added at `d0aa833b`. Finding `R-0881` records the measurement. The branch therefore carried DECISIONs amend0911-feedback D8 and D9, which bind rules A, B and C and name that document as their home, while the document itself said nothing about them; and the amend0911-f275-to-scope paragraph lifting this feature's session and round limit was absent while `.agent/plan.md` and the round 77 handback were still printing the withdrawn numbers and the session-limit banner.

CHOSEN, FIRST: THE BYTES ARE DERIVED AND NOT AUTHORED. The restored text is computed as `M[p : len(M)-s]` where `M` is the path's blob at `d0aa833b`, `B` is its blob at this round's base, `p` is the count of leading lines on which `M` and `B` agree and `s` the count of trailing lines. Measured at `e262f420`, `p` is 246 and `s` is 13, so that expression is 65 lines and is exactly the four paragraphs. ALTERNATIVE: ship the 65 lines as an authored slice in the block, rejected under item 37 of `docs/agents/planner_reviewer_prompt.md` §3 — under this workflow a block travels inside the worker's prompt and is retyped into `.agent/authored/`, so an authored slice is the one link no gate in this repository can prove, and a git object is a link that needs no proving.

CHOSEN, SECOND: THE PLACEMENT IS CHRONOLOGICAL, WHICH IS NOT WHERE `main` HAS IT. On `main` the four paragraphs sit directly after the amend0906-triage-throughput paragraph, and DECISION amend0911-feedback D10 records why: the amend0908-f275-finish paragraph does not exist at `main` and "was absent and needed insertion rather than being skipped". On this branch it does exist, in exactly that position, and the amend0911-f275-to-scope paragraph overrides amend0908 rule 1 BY NAME. Text that overrides must read after the text it overrides, so the insertion goes after the amend0908 paragraph. ALTERNATIVE: match `main`'s byte position exactly, rejected because it puts the override before its target and because no property of the merge requires it — the two blocks are disjoint and their order is a readability choice, recorded here so a later reader does not read the difference as a second loss.

CHOSEN, THIRD: THE PROOF IS TWO ROUND-TRIP IDENTITIES, not a digest. The committed file with the 66 inserted lines removed must equal the base blob byte for byte, which proves nothing of this branch's was lost; and the committed file with the amend0908 paragraph and its following blank line removed must equal `d0aa833b`'s blob byte for byte, which proves nothing of `main`'s was lost. The reviewer measured that neither identity is sufficient alone: a byte flipped inside the inserted region leaves the first identity TRUE, and a line deleted from the shared tail leaves the slice-identity reading TRUE, so the gate is the conjunction of three readings and four mutations were run against it before it was ordered.

CONSEQUENCE. Rules A, B and C and the limit lift are readable on this branch at the place their own DECISIONs name, and a later merge of this branch into `main` no longer deletes them. F275 owes no scope report and no session-limit banner from this round forward. Every finding this feature registers from now on carries an `Owner:` line under rule A, and every handback carries `Operator questions open: <n>` under rule C. Nothing about the flip, the ruled site set or `R-0880` is touched, and no production line moved.

WHAT THIS DOES NOT FIX, stated because the finding names it. `tests/test_agent_tooling.py` pins six substrings of this document and would not have seen the drop, because it pins the guardrails and no amendment; it will not see the next one either. Widening it is not this round's work and is not smuggled into it — the block's change set holds no path under `tests/` — and the gap is recorded here and in `R-0881` rather than in a new id, per item 30 of §3, because it is the same defect seen from the guard's side.

HOW TO REVERSE. Delete the 66 inserted lines from `docs/agents/self_drive_protocol.md`, which restores the file to its blob at this round's base byte for byte, and delete this paragraph block. Rules A, B and C and the limit lift then bind by `.agent/decisions.md` alone, as they did between `e262f420` and this round.
END DEC78

## SLICE DONE78 — appended to `.agent/live_review.md` at C6

BEGIN DONE78 sha256=e5a8dfba620fcc17af153f6c00234eacc9e7e33694db07cfd0d525c5b1bf152a

Done: R-0881 — RESOLVED in the round that registered it. The four amend0911-feedback paragraphs are back in `docs/agents/self_drive_protocol.md`, derived from the path's blob at `d0aa833b` rather than retyped, and placed after the amend0908 paragraph so that the text overriding amend0908 rule 1 reads after it. The commit carrying them is the one constraint 11 of this round's block fixes between the registration at C2 and this resolution at C6, and it is named by that ordering rather than by a SHA because it did not exist when this paragraph was authored — item 20's R-0524 carve-out. The proof is the conjunction of three readings, each measured against four deliberate mutations: the inserted region is byte-identical to the derived slice, the committed file with that region removed is byte-identical to this round's base blob, and the committed file with the amend0908 paragraph and its trailing blank removed is byte-identical to `d0aa833b`'s blob. DECISION F275 D52 records the derivation, the placement and the reason the proof is two round trips rather than a digest. The guard blind spot the finding names — a substring pin that cannot see a missing amendment — is NOT fixed by this round and is not claimed to be; it stays recorded in the finding and in D52 with no second id, per item 30.
END DONE78
