── STEP R5 — F255 Teacher role ────────────────────────────────
Goal:        Apply DECISION F255 D6 to the handback template, close the hole
             that let a second id be minted for a defect already open, record
             the R4 verdict, and resolve the three findings this round settles.
             R-0602 turns out to duplicate R-0462, open since F083 R8; both are
             retired together and the counter-measure lands as checklist item 30.

Bundle:      C0a save this block · C0b mirror it · C1 register R-0603 · C2 apply
             D6 to the template · C3 add checklist item 30 · C4 record R4 and
             resolve R-0462, R-0602 and R-0603 · C5 the plan · C6 the handback,
             then push.

Change:      Exactly these paths, in this order, one commit each.
             C0a `.agent/authored/f255-r5.md`
             C0b `.agent/last_block.md`
             C1  `.agent/live_review.md`
             C2  `docs/agents/handback_template.md`
             C3  `docs/agents/planner_reviewer_prompt.md`
             C4  `.agent/live_review.md`
             C5  `.agent/plan.md`
             C6  `.agent/handoff.md`
             Nothing else is created, modified, deleted or staged. NO source
             file and NO test changes this round. These paths are PRESENT at the
             base and must stay untouched: `docs/roadmap/features/T5_F255.md`,
             `docs/roadmap/STATUS.md`, `docs/roadmap/ROADMAP.md`,
             `.agent/decisions.md`, `.agent/context.md`,
             `.agent/f255_inventory.md`, `AGENTS.md`.

Constraints:
1. NO SLICE IS EDITED. Every text between `<<<SLICE x` and `<<<END x` is applied
   byte for byte. A slice you believe is wrong is applied anyway and DECLARED in
   the handback; you never repair it silently. Marker lines never reach a target.
2. TRANSPORT. `.remedy-wt/f255-r5.md` is this block on disk. C0a copies that
   FILE to `.agent/authored/f255-r5.md` — copy it, never retype it — and C0b
   copies the same file to `.agent/last_block.md`. Prove all three byte-EQUAL;
   the reviewer stated the expected digest when it delegated, and that digest
   cannot appear in this file because this file is what it digests.
3. TWO PAIRS EXIST AND THEY HAVE DIFFERENT SHAPES. The reviewer ran the
   containment test over both before emission and quotes each result as the test
   printed it. CAPFROM→CAPTO over `docs/agents/handback_template.md`:
   `TO contains FROM: False` — a REWRITE, so G5 orders the FROM-zero count.
   ITEM30FROM→ITEM30TO over `docs/agents/planner_reviewer_prompt.md`:
   `TO contains FROM: True` — APPEND-shaped, so G6 orders FROM exactly 1x and
   each TO-ONLY line exactly 1x AMONG THAT COMMIT'S ADDED LINES, and NEVER a
   FROM-zero count, which that shape cannot reach (§4.9, R-0207).
4. EVERY LEDGER APPEND IS BLANK-SEPARATED. R0603 at C1, and RECORDR4, DONE0462,
   DONE0602 and DONE0603 at C4, are each appended preceded by exactly one blank
   line (R-0578), copied from their extracted slice files and never retyped.
   Nothing already in that file is rewritten, reordered or deleted.
5. THE SETS MOVE BY A KNOWN AMOUNT, MEASURED AT BOTH ENDS. The reviewer measured
   178 registered, 0 resolved, 178 open and 0 line-anchored `Landed:` at the
   base. C1 owes 179 / 0 / 179 / 0. C4 owes 179 / 3 / 176 / 0 — three `Done:`
   paragraphs and no new `- R-` line. G4 and G7 order both readings measured.
6. THE `Done:` TEXTS ARE THE REVIEWER'S AND YOU NEVER AUTHOR ONE YOURSELF. You
   apply DONE0462, DONE0602 and DONE0603 verbatim and write no other `Done:` and
   no `Landed:` line.
7. THE TEMPLATE EDIT REMOVES A RULE THIS PROJECT HAS OUTGROWN, AND YOUR OWN
   HANDBACK IS THE FIRST ARTIFACT IT FREES. After C2 the ≤800-token sentence is
   gone; the LINE cap your commit count earns is the only size bound, and your
   handback must meet it.
8. `.agent/STOP` is read from disk before C0a. If it exists, stop and write the
   handback instead.
9. `git status --porcelain` is EMPTY after every commit. No worktree is created
   this round, because no destructive check is ordered.
10. YOU DO NOT WAIT ON ANY CI RUN and you report no run's conclusion.

<<<SLICE CAPFROM
> Hard cap: this file stays ≤800 tokens — ≤1600 in the >10-commit
> LARGE case (P4 token thrift).
<<<END CAPFROM

<<<SLICE CAPTO
> That LINE cap is the single operative bound on a handback's size: it
> scales with the commit count, is measured with `wc -l`, and needs no
> tokenizer to agree on. A "≤800 tokens — ≤1600 in the >10-commit LARGE
> case" hard cap stood here until 2026-08-20, when DECISION F255 D6
> withdrew it (findings R-0462 and R-0602): twelve consecutive rounds
> exceeded it, from roughly 1306 to 2983 tokens at a chars/4 estimate,
> while every one of them met the line cap. A cap two readers cannot
> measure identically is not enforceable by either, and a cap no round
> has met in twelve rounds binds nothing. Do not restate a token cap
> here without re-measuring what the mandated sections actually cost.
<<<END CAPTO

<<<SLICE ITEM30FROM
  Why this is on disk and not a habit: item 2 has recurred six times across
<<<END ITEM30FROM

<<<SLICE ITEM30TO
  30. **A new finding id is minted only after the open set is searched for the
      DEFECT.** Finding R-0603. Before writing `- R-XXXX`, grep
      `.agent/live_review.md` for the defect itself — the file it is in, the
      rule it breaks, the symptom a reader would search for — and not merely for
      an id. If an OPEN finding already describes it, add the new evidence to
      that finding's fix rather than minting a second id, because two ids for
      one defect are two things to resolve, two things to carry forward and two
      chances to fix it half-way. Item 10 governs the SHAPE of the open set —
      it recomputes the set mechanically and forbids carrying it forward — and
      is silent on whether a NEW id describes a defect the set already holds,
      which is the gap that let this happen twice: the same class cost F086 R28
      a FAIL, and R-0602 was still minted at F255 R2 for the handback token cap
      that R-0462 had held OPEN since F083 R8. The reviewer had just measured
      twelve handbacks against that cap and never searched the record for the
      defect it was measuring. A duplicate is not harmless: R-0462 carried a fix
      clause the duplicate did not, and had the ruling gone the other way the
      two entries could have been resolved in contradictory directions. When a
      duplicate is discovered, retire the NEWER id as the duplicate, keep the
      older one as the record, and say in both resolutions which is which.
  Why this is on disk and not a habit: item 2 has recurred six times across
<<<END ITEM30TO

<<<SLICE R0603
- R-0603 — Low — A SECOND ID WAS MINTED FOR A DEFECT THE SAME RECORD ALREADY HELD OPEN, BECAUSE NO CHECKLIST ITEM REQUIRES SEARCHING THE OPEN SET FOR THE DEFECT BEFORE MINTING. R-0602, registered at F255 R2 in the commit `b9c0cb64`, states that the handback template's ≤800-token hard cap is exceeded by every round and therefore binds nothing. R-0462, registered at F083 R8 and OPEN at that same commit — 1 registered paragraph and 0 `Done:` lines, measured — states the same defect about the same sentence of the same file: "THE HANDBACK TOKEN CAP IS BINDING, EXCEEDED EVERY ROUND, AND MEASURED BY NOTHING", naming the same two disagreeing caps and offering the same two coherent outcomes. The reviewer minted R-0602 immediately after measuring twelve handbacks against that cap, and never grepped the record for the defect it had just measured. This is a recurrence rather than a first occurrence: the same class cost F086 R28 a FAIL. The cause is a gap in the counter-measure and not in any one round — §3's pre-emission checklist governs the SHAPE of the open set at item 10, recomputing it mechanically and forbidding a carry-forward, and says nothing about whether a NEW id describes a defect the set already holds — so nothing on disk has ever asked the question, and item 10 is satisfied by a duplicate. The duplication is not cosmetic: R-0462 carries a fix clause R-0602 does not, asking that checklist item 3 gain the token cap so it is measured rather than assumed, and DECISION F255 D6 withdraws the cap instead, so a reviewer resolving only the newer id would have left the older one open against a rule that no longer exists. The fix lands this round as checklist item 30, and both ids are retired together: the defect is fixed once, the older id keeps the record, and the newer is retired as the duplicate.
<<<END R0603

<<<SLICE RECORDR4
Gate: R5 — the R4 entry. R4 PASSED with NO finding against its work and none against its block. Every gate the R4 block ordered was RE-EXECUTED by the reviewer over `a0b8e542..b40c0616` rather than read from the handback, and every one holds. THE TRANSPORT HELD IN THE PRIMARY FORM: `.remedy-wt/f255-r4.md`, the committed `.agent/authored/f255-r4.md` at `abb8b7ea` and the committed `.agent/last_block.md` at `bbbf37ca` are byte-EQUAL at sha256 0c6e610c210d7e03349d4ef076bdaf28d5f2c08bc3ccfc8b985da5b0e3ac4d62 over 24010 B and 337 lines, the digest stated at delegation. THE FEATURE FILE WAS AMENDED WITHOUT LOSING A BYTE, WHICH WAS THE ROUND'S CENTRAL RISK: the base blob at `a0b8e542` — 2730 B over 47 lines, a BYTE count, which differs from its 2713 CHARACTERS because the file carries multi-byte UTF-8, a distinction the reviewer's own first gate text got wrong and corrected before emission — is a byte-exact PREFIX of the C2 blob at `d5ffa2e3`, 9737 B over 175 lines; the remainder equals a blank line followed by AMEND255 byte for byte; the C2 diff carries ZERO deletion lines and a numstat of 128/0, so the amendment is a pure append. Line 1 and lines 2-4, which `packages/orchestration/roadmap_index.py` parses, are IDENTICAL at both ends, and the `## Scope (registered verbatim, plan0806 2026-08-06)` block — the operator's registration record — is byte-identical between its heading and `## Non-goals`. The file now carries ten `## ` headings, the original three followed by Amendment status, Design, Task slicing, Acceptance, Edge cases, Orchestrator brief and Do not touch. THE PARSER AND THE DOCS SUITE BOTH STILL ACCEPT IT: the reviewer re-ran `tests/orchestration/test_roadmap_index.py` at exit 0 with 30 passed and `tests/docs/` at exit 0 with 295 passed, separately so that a regression in either would be visible alone, and 30 plus 295 equals the 325 the reviewer had measured with AMEND255 pre-applied inside a disposable worktree BEFORE the block was emitted. THE VERDICT ENTRY LANDED AS AN APPEND AND THE SETS DID NOT MOVE: the pre-C1 blob is a byte-exact PREFIX of the post-C1 blob at `4e1df902`, the 2-line remainder is a blank line followed by RECORDR3 with the separator PRESENT, an independent paragraph split yields RECORDR3 as its LAST unit under both newline conventions, registered 178 / resolved 0 / open 178 / line-anchored `Landed:` 0 at BOTH ends, and `Gate: R4 — the R3 entry.` occurs 1x, sits last, with all four header keys distinct. THE PLAN IS BYTE-EXACT at 40 lines, under the 50-line cap. THE ROUND GATE WAS RE-RUN SERIALLY BY THE REVIEWER IN THE PRIMARY CHECKOUT: the four-file state-reader selection exited 0 at `160 passed` and the canary exited 0 at `42 passed`. NOTHING WAS BUILT: `git diff --name-only a0b8e542..b40c0616` scoped to `apps/ packages/ tests/ scripts/` is EMPTY, all eight paths named untouched are PRESENT at the base and ABSENT from the range, every commit has one parent, the maximum insertion column is 337 under the 500 cap, zero marker lines reached any written file, and the handback is 99 lines inside the ≤100 its six-commit table earns. THE REFLOG CONTROL DISCRIMINATED FOR THE FIRST TIME, WHICH IS THE POINT OF R-0601 AND IS WORTH RECORDING: read by OPERATION PREFIX the round has six `commit` entries and ZERO rewrite entries, but read as a WHOLE LINE — the form R-0601 retired — it reports ONE, because C2's own subject is "docs(roadmap): amend the F255 feature file with the R3 rulings" and contains the word `amend`. The reviewer re-measured both readings itself: the retired form would have reported a history rewrite that never happened, on a round whose history is provably linear. R3's worker had reported honestly that the same control did not discriminate in its round; one round later it does.
<<<END RECORDR4

<<<SLICE DONE0462
Done: R-0462 — RESOLVED, and it is the id of record for this defect. The ruling the finding asked for exists: DECISION F255 D6 in `.agent/decisions.md` settles the handback token cap, and this round removes the sentence "Hard cap: this file stays ≤800 tokens — ≤1600 in the >10-commit LARGE case (P4 token thrift)" from `docs/agents/handback_template.md` and states in its place that the LINE cap is the single operative bound. The finding offered two coherent outcomes — raise the cap to match the mandated content, or shrink the mandated content — and the ruling takes a third that the finding did not consider and that its own evidence supports better: WITHDRAW a cap no round has met in at least twelve rounds, and keep the cap every round does meet, which scales with commit count and is measured with `wc -l` rather than with an estimator two readers would disagree about. Two of the finding's clauses expire with the ruling and are deliberately NOT implemented, which is stated here so no later reader reads their absence as an oversight: "a handback that declares a D15 stated-cause overage names BOTH caps it exceeds" has no second cap to name, and "item 3 gains the token cap so the number is measured instead of assumed" would have checklist item 3 measure a cap that no longer exists — item 3 measures caps that exist, and this one does not. The finding's diagnosis was right on every point and stood open for twelve rounds because its fix was routed to a paydown round that never came.
<<<END DONE0462

<<<SLICE DONE0602
Done: R-0602 — RESOLVED as a DUPLICATE of R-0462, which is the id of record. Both describe the same defect in the same sentence of the same file — the handback template's ≤800-token hard cap, exceeded by every round and measured by nothing — and R-0462 was already OPEN when R-0602 was minted at F255 R2, with 1 registered paragraph and 0 `Done:` lines in the same record the new id was written into. The underlying defect is fixed ONCE, by DECISION F255 D6 and the template edit this round lands; nothing in R-0602 required a fix that R-0462 did not already ask for, and its measurement — twelve consecutive handbacks between roughly 1306 and 2983 tokens at a chars/4 estimate — is evidence the older finding lacked and is preserved in the ruling and in the template's replacement text. The duplication itself is registered separately as R-0603 rather than being quietly absorbed here, because the process gap that produced it outlives this pair.
<<<END DONE0602

<<<SLICE DONE0603
Done: R-0603 — RESOLVED by checklist item 30 of docs/agents/planner_reviewer_prompt.md, which this round adds: a new finding id is minted only after the open set has been searched for the DEFECT — the file, the rule, the symptom — and not merely for an id, and where an OPEN finding already describes it the new evidence joins that finding instead of a second id. The item states the two instances that earned it, the F086 R28 FAIL and the R-0462/R-0602 pair, and the rule for retiring a duplicate: the NEWER id is retired, the older keeps the record, and both resolutions say which is which. That is exactly how this round retires R-0602 against R-0462, so the rule and its first application land together rather than the rule arriving as prose nobody has yet followed.
<<<END DONE0603

<<<SLICE PLAN255R5
# Plan — F255 Teacher role

Branch: feature/f255-teacher-role, cut from `main` at b35d350b, the merge commit
of pull request #207. No pull request is open for this branch; on this project
the PR is created by the closure round.
`.agent/live_review.md` is the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

## Goal
A fourth configured role, `teacher`, that narrates a running mission and answers
operator questions about the operator's own code, and never influences the run.
DONE when passive narration keyed to an enumerated set of ledger events (Stage 1,
deterministic templates, zero tokens) and on-demand Q&A (Stage 2, through the
teacher role's own model) both work, the three grounding sources are never mixed
silently, teacher spend is reported as its own role in the F103 ledger, and the
read-only invariant is proven behaviourally.

## Current Step
R5: apply DECISION F255 D6 to `docs/agents/handback_template.md`, add checklist
item 30 so a duplicate id cannot be minted again, record the R4 verdict, and
resolve R-0462, R-0602 and R-0603. The feature file is not touched and no code
is written.

## Next Steps
1. R6 BUILDS T001 — the role vocabularies. `teacher` joins `KNOWN_ROLES` and
   `ConventionsRole`, with the renamed seven-to-eight pin in the SAME commit as
   the tuple it guards, plus a `teacher.model` config key modelled on
   `orchestrator.model`. This is the first round of this feature to touch source.
2. R7 BUILDS T002 AND T003 TOGETHER — Stage 1 narration and the behavioural
   read-only proof — because a read-only feature whose read-only-ness is
   unproven is this feature's likeliest failure.
3. T004, Stage 2 Q&A, comes last and only once the grounding-source labelling
   of T002 is real.

## Risks
- R6 IS THE FIRST SOURCE-TOUCHING ROUND OF THIS FEATURE. Its gate must include
  the tests that read the role vocabulary, not only the state-reader four, and
  the seven-to-eight pin is a deliberate tripwire rather than an accident.
- STAGE 1 MUST STAY ZERO-TOKEN TO BE WORTH HAVING. If narration quietly starts
  calling a model, the feature loses both its cost story and its offline story.
- THE AMENDMENT IS NOW THE SPEC. A T-slice that drifts from it is a finding
  rather than a preference, which is why it was written down before any build.
<<<END PLAN255R5

Done when:
G1 HYGIENE. `.agent/STOP` read from disk before C0a and reported absent or
   present; branch is feature/f255-teacher-role; `git status --porcelain` EMPTY
   after every commit and at the handback; `git worktree list` reports the
   primary checkout alone. No reading is taken by overwriting a file in the
   primary checkout — use `git show <sha>:<path>`.
G2 TRANSPORT. Report the sha256 and the byte and line counts of
   `.remedy-wt/f255-r5.md`, of `.agent/authored/f255-r5.md` at C0a and of
   `.agent/last_block.md` at C0b, and state whether all three are EQUAL.
G3 SLICES EXTRACTED, NEVER RETYPED. Report the extraction command and the
   sha256, byte count AND line count of each of the nine slices, naming the
   newline convention used (R-0600).
G4 R-0603 REGISTERED. C1 appends R0603 preceded by exactly one blank line.
   Report the PREFIX property, the remainder's sha256, byte and line counts, and
   that the separator is present. Report registered, resolved, open and
   line-anchored `Landed:` at the base and at C1: the reviewer measured
   178 / 0 / 178 / 0 at `b40c0616`, and C1 owes 179 / 0 / 179 / 0. Report that
   `- R-0603 — ` occurs exactly 1x.
G5 THE TEMPLATE EDIT, A REWRITE PAIR. In `docs/agents/handback_template.md`
   report CAPFROM's count at the base and at C2, and CAPTO's at both ends. The
   reviewer measured CAPFROM present exactly 1x and CAPTO 0x at the base; the
   rewrite shape owes CAPFROM 0x and CAPTO 1x after C2. Report `git diff
   --numstat` for that file at C2. Report that the LINE-cap sentence the
   template already carried — the one naming ≤60, ≤100 and ≤160 — is still
   present exactly once and was NOT edited.
G6 THE CHECKLIST INSERTION, AN APPEND-SHAPED PAIR. In
   `docs/agents/planner_reviewer_prompt.md` the pair is APPEND-shaped, so do NOT
   report a FROM-zero count: that count is unreachable by construction and
   demanding it invites a fabricated number (§4.9, R-0207). Report instead that
   ITEM30FROM occurs exactly 1x at the base AND exactly 1x at C3, and that each
   line of ITEM30TO that is not in ITEM30FROM occurs exactly 1x AMONG THE LINES
   C3's diff ADDS. Report `git diff --numstat` for that file at C3, that
   `^  30. ` occurs exactly 1x at C3 and 0x at the base, and that no item number
   is duplicated. SCOPE THAT LAST COUNT TO THE CHECKLIST BLOCK, which runs from
   the line beginning `- **Pre-emission block checklist` to the line beginning
   `  Why this is on disk`: inside that span the lines matching `^  \d+\. \*\*`
   must number exactly 1..30 with no gap and no repeat. Measured unscoped the
   same regex reads 34 at C3, because the Verification-tiers list below the
   checklist shares its shape — the reviewer measured that before ordering this
   gate, and a gate demanding 30 unscoped would be unmeetable by construction.
G7 THE VERDICT AND THE THREE RESOLUTIONS. C4 appends RECORDR4, DONE0462,
   DONE0602 and DONE0603, in that order, each preceded by exactly one blank
   line. Report the PREFIX property and that the remainder equals those four
   slices with their separators, byte for byte. Report a SECOND, independent
   paragraph-level split of the C4 blob and that its last FOUR units are those
   four slices in order. Run a negative control — one character of the expected
   remainder mutated — and report that BOTH readings reject it. Report
   registered, resolved, open and line-anchored `Landed:` at C1 and at C4: C4
   owes 179 / 3 / 176 / 0. Report that `Done: R-0462 — `, `Done: R-0602 — ` and
   `Done: R-0603 — ` each occur exactly 1x, and that `Gate: R5 — the R4 entry.`
   occurs 1x, is the LAST line beginning `Gate: R`, with no header key repeated.
G8 THE PLAN. `.agent/plan.md` at C5 byte-equals PLAN255R5; report its sha256,
   byte and line counts, that the line count is under 50, and that `## Goal`,
   `## Next Steps` and a roadmap F-id all occur in it.
G9 THE ROUND GATE, serially in the PRIMARY checkout, never two pytest processes
   at once. Report the exact command, exit code and tail of each:
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/docs/ -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
   The reviewer measured exit 0 at 160 passed, exit 0 at 295 passed and exit 0
   at 42 passed, all three at `b40c0616` in the primary checkout.
   `tests/docs/` runs as a REGRESSION check only, and its green is NOT evidence
   about C2 or C3: the reviewer replaced the whole of
   `docs/agents/handback_template.md` with the single word BROKEN inside a
   disposable worktree and `tests/docs/` still exited 0 at 295 passed, so that
   suite is blind to `docs/agents/**`. The proof for this round's two edits is
   G5 and G6, which read the files themselves. Report the docs run, and do not
   describe it as confirming the edits.
G10 CHANGE SET, HISTORY AND CAPS. Report `git diff --name-only b40c0616..HEAD`
   and state that it equals the Change list with no path on either side alone.
   Report that the SAME command scoped to `apps/ packages/ tests/ scripts/` is
   EMPTY. Report that each of the seven paths the Change section names as
   untouched is PRESENT at the base and absent from the range; that every commit
   in the range has one parent; and each commit's insertion column from
   `git diff --numstat`, every one under 500, with the same `+/-` cells
   appearing byte-identically in the handback's `## Commits` table. C6's own
   cell and the complete change set belong to the round report.
   THE REFLOG IS REPORTED AS TWO MEASURED CLAIMS, NOT ONE UNIVERSAL (R-0601):
   the count of this round's reflog entries that PRODUCED a commit and read
   `commit`, which must equal the number of commits the round makes; and the
   count whose OPERATION PREFIX — the text before the first colon of
   `git reflog --format=%gs` — contains `amend`, `reset`, `rebase` or `cherry`,
   which must be 0. Read the prefix, never the whole line. Report ALSO what the
   retired whole-line reading would have returned this round, as a control.
G11 NO MARKER LEAKED. Report the count of LINES beginning `<<<SLICE ` or
   `<<<END ` in `.agent/live_review.md` at C4,
   `docs/agents/handback_template.md` at C2,
   `docs/agents/planner_reviewer_prompt.md` at C3, `.agent/plan.md` at C5 and
   `.agent/handoff.md` at C6. Every count must be 0.
G12 THE PUSH. After C6, `git push` and report its real output. Do NOT create a
   pull request and do NOT wait on the CI run the push starts (constraint 10).

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             all seven mandated headings in the template's order, the
             item-status table for the C0a..C6 bundle, the `## Commits` table
             G10 pins, and one LINE per gate rather than its transcript
             (R-0582). The ≤800-token cap is GONE from the template as of your
             own C2, so make no claim about it either way; the LINE cap your
             commit count earns is the bound, and your handback meets it. Its
             `## Next` section names the next session's FIRST action as Phase 1
             rule 1, the `.agent/STOP` re-read, and its SECOND as R6, the first
             source-touching round of this feature, building T001 — in that
             order — and states that R5 awaits review. There is no open pull
             request. The full transcripts go in the round report you return,
             never in the file. The handback also carries this Fortschritt line
             verbatim, because with no relay you never see the operator brief
             that would otherwise state it (R-0418):
             Fortschritt: ~15 % (F086 merged · F255 claimed · ground measured ·
             six DECISIONs ruled · the feature file carries its spec · the
             process holes closed · T001 builds next) — Schätzung
──────────────────────────────────────────────────────────────
