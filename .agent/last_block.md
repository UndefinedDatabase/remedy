── STEP RECORD AND HAND OFF — F021 ──
Goal:        Record R36, which PASSED, and close this SESSION cleanly. F021's
             BUILD is complete — every item of T001, T002 and T003 is on disk —
             and the next session opens the closure sequence. This round writes
             no product code: it exists because a verdict that is never written
             down did not happen, and because a session that ends without a
             handoff did not happen either. ONE correction is appended naming
             OPEN finding R-0629; it mints no id and it is the REVIEWER's own
             defect in the R36 block.

Fortschritt: 100 % der Bauarbeit, 0 % des Abschlusses (Integrations-Gate,
             Evidenz-Runde und STATUS-Runde stehen noch aus)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R36 verdict
             and the one correction · C3 the session handoff.

Change:      Exactly these paths. I counted this list mechanically: it holds
             FIVE entries, of which FOUR are not the handoff.
             `.agent/authored/f021-r37.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `.agent/handoff.md` (C3). NO file under `apps/`, `packages/`,
             `tests/` or `docs/` is touched. Report the counts YOU measure.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3 and is not negotiable. ROUND BASE is
    `dc9e72bf` — resolve its full form with `git rev-parse`.
 3. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. Before it: 224 registered
    under `^- R-\d+ — `, maximum R-0661, `Done: R-` 1. After C2: still 224,
    still all DISTINCT, still maximum R-0661, `Done: R-` still 1.
    `^- R-0629 — ` stays at exactly 1 across C2.
 4. NO PARAGRAPH OF RECORD37 BEGINS WITH THE BYTES `- R-`. One opens
    `Recurrence: ` and the verdict opens `Gate: R37 — `, and the two are
    separated by EXACTLY ONE BLANK LINE.
 5. THE APPEND CONVENTION for `.agent/live_review.md` at C2: the slice is
    quoted WITHOUT a trailing newline; add EXACTLY ONE newline, then RECORD37,
    then one terminator, so the join carries EXACTLY ONE BLANK LINE. A
    WHOLE-FILE write (PLANF021R37) is the slice PLUS one terminator.
 6. THE LEDGER IS APPEND-ONLY. No landed paragraph, `Gate:` or `Recurrence:`
    entry is edited.
 7. EVERY LEDGER COUNT NAMES ITS PATTERN, ANCHORED. No unanchored count is
    ordered over `.agent/live_review.md`, which quotes the tokens a gate might
    count (R-0629's sibling R-0630).
 8. Run no formatter or linter that rewrites a file in place. `npm run lint` is
    RED tree-wide under R-0622 and is NOT a gate — do not run it. Create and
    merge NO pull request. Push the branch after C3. Create NO worktree: this
    round changes no control flow, so no red-proof is owed and none is ordered.
 9. C3 IS A SESSION HANDOFF AND NOT ONLY A ROUND HANDBACK. Besides the usual
    contents it states, in its own words: that F021's build is COMPLETE; that
    the next action is the INTEGRATION-GATE round, followed by the evidence
    round and then the STATUS-commit round; that the branch carries NO pull
    request and opens one only at closure; and that the next session's FIRST
    action is Phase 1 rule 1 of docs/agents/self_drive_protocol.md — re-reading
    `.agent/STOP` from disk — BEFORE rule 2. It also carries R37's own two
    unnameable readings as owed to the next round: C3's SHA and its insertions.
10. Block size, measured on these final bytes AFTER the last edit: TOTAL 168
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice
    CONTENT lines — 121 against DECISION F085 D5's 400. Markers count as prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C3; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain`
     prints 0 lines after each of C0a, C0b, C1 and C2. C3's own reading is
     ordered NOWHERE — §3 item 31 leaves it to the next session.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r37.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you read, and over my
     emitted copy at `.remedy-wt/f021-r37.md` are all equal. Write C0b FROM the
     committed C0a blob. Report the digest, bytes and lines. Then extract the
     slices from the COMMITTED C0a blob by their marker LINES, `<<<SLICE ` and
     `<<<END `, and report how many whole texts and how many CONTENT lines your
     extractor printed — numbers YOU measured — re-measuring constraint 10's
     two numerals from that same blob against their caps.
 G3  `.agent/plan.md` at C1 equals PLANF021R37 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0, with a NEGATIVE CONTROL against the bare slice that must
     exit 1. Report both exit codes, that the last byte is a newline,
     `^## Goal$` 1 and `^## Next Steps$` 1, and the `wc -l` YOU measure against
     AGENTS.md's "keep it short (<50 lines)". If that count is 50 or more, STOP
     and report — do NOT trim the file to reach it (R-0654).
 G4  THE LEDGER, at C2, every count naming its anchored pattern, base then C2:
     canonical `^- R-\d+ — ` 224 then 224, ALL DISTINCT at both, maximum
     R-0661 at both; loose `^- R-` 225 then 225, gap 1 at both; `^Done: R-` 1
     then 1; `^Gate: R` 35 then 36, DISTINCT at both; `^Gate: R37` 0 then 1;
     `^Recurrence: ` 13 then 14; `^Recurrence: R-0629 — ` 1 then 2 — NOT a
     zero-then-one, because one already landed at F021 R32; `^- R-0629 — ` 1
     then 1. Report that the number of RECORD37 paragraphs opening with the
     bytes `- R-` is 0, that the base blob is a byte-exact PREFIX of the C2
     blob, and that the remainder is EXACTLY one newline plus RECORD37 plus one
     newline.
 G5  THE SUITES, SERIAL, in the PRIMARY checkout, never two at once. This round
     rewrites `.agent/` state and touches nothing else, so it gates ALL FOUR
     state readers and the canary and NOTHING MORE — no `tsc`, no vitest, no
     `ruff`, because no file those read is touched, and R-0364 forbids ordering
     a gate whose subject this round does not change.
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py
     tests/orchestration/test_integrity_gate.py -q -rf` — I measured 528 at the
     round base. `python3 -m pytest tests/cli/test_golden_path.py -q -rf` — 42
     at the base. Report both numbers YOU measure.
 G6  STRUCTURE. `git diff --name-only dc9e72bf..HEAD` at C2 EQUALS the FOUR
     non-handoff paths of the `Change:` list, and at C3 those plus
     `.agent/handoff.md` for FIVE; report the count YOU measure at each and
     both set differences, which must be EMPTY at both. 5 commits, every one
     single-parent; `git show --numstat` and `git diff --numstat` agree cell by
     cell; every commit's insertions under 500, each number reported — and note
     that `--stat` may print a larger figure than `--numstat` for a whole-file
     rewrite under rename detection, which `.agent/last_block.md` is. Marker
     sweep, LINE-ANCHORED, 0 for each of `<<<SLICE ` and `<<<END ` over
     `.agent/plan.md` and `.agent/live_review.md`. No unanchored `<<<` count is
     ordered over either (R-0630). Reflog read BY OPERATION: every one of this
     round's rows is `commit`, with `amend`, `rebase` and `cherry` 0 each in
     that field. `gh pr list --state open` reported verbatim; it must print
     `[]`, and NEITHER `gh pr create` NOR `gh pr merge` is run this round.

<<<SLICE PLANF021R37
# Plan — F021 Live activity feed + now-card

Branch: feature/f021-live-activity-feed, cut from `main` at `4548995d`, the merge
commit of pull request #210. `.agent/live_review.md` is the source of truth for
the open set, the round map and the finding-id ceiling.

## Goal
The raw SSE event stream becomes a story a human can follow: a humanization
catalog maps event kinds to plain lines, a NowCard shows the newest ACTION-class
event with a recency dot, and feed rows carry their seq and click-jump to their
node. DONE when the catalog covers the kind set DECISION F021 D3 rules and an
unknown kind renders an honest generic line rather than vanishing, the feed
renders fixture streams per the binding CSS, jump-to-node focuses the right
node, and the steering input renders DISABLED with its tooltip until F030.

## Current Step
R37 records R36 and ends the session. THE BUILD IS COMPLETE: T001's catalog and
its derived coverage contract, T002's ring, feed, NowCard, recency dot and
scroll discipline, and T003's envelope linkage, row resolver, click-jump and
disabled steering input are all on disk and gated. Nothing of the feature's
change set remains unwritten. One correction is appended against OPEN finding
R-0629, minting no id.

## Next Steps
1. The INTEGRATION-GATE round: the whole suite at the branch tip, and the
   feature file's Goal & Done read clause by clause against what is on disk —
   the round that may only confirm, never build.
2. The evidence round, then the STATUS-commit round
   (docs/roadmap/STATUS_closure_protocol.md; the two are never one round).
3. The pull request, opened at closure and merged only at the Open PR Gate.

## Risks
- The build being complete is a claim about the CHANGE SET, not about the
  acceptance criteria. Only the integration-gate round can read Goal & Done
  clause by clause, and it may find a clause nothing on disk satisfies.
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK.
- Nothing here renders CSS. R-0661's pin proves the unresolved-property SET has
  not grown; it cannot prove any rule's computed value.
- `npm run lint` is RED tree-wide under R-0622, still open.
- No code defect of F021 is open. R-0364, R-0369, R-0402, R-0403, R-0419,
  R-0439, R-0587, R-0607 through R-0609, R-0611, R-0613, R-0618, R-0622,
  R-0629, R-0630, R-0644, R-0651, R-0653 through R-0659 and R-0661 stay routed
  to a paydown branch.
<<<END PLANF021R37

<<<SLICE RECORD37
Recurrence: R-0629 — A DESTRUCTIVE CONTROL NAMED A TARGET WHOSE TWO UNIQUENESS READINGS DISAGREE, AND THE BLOCK NEVER MEASURED EITHER. Second instance, in the reviewer's own F021 R36 block; found by the WORKER, which refused its own first applier rather than guess. NO NEW ID IS MINTED: R-0629 already rules that a destructive control MEASURES the uniqueness it asserts, whole-line AND indent-agnostic, and ships only if the two AGREE (§3 checklist item 25). THE INSTANCE: G6 ordered the mutation by quoting, inside a code span, the line `      <ChatInput disabled reason={STEERING_DISABLED_REASON} />` at its six-space fallback-branch indentation. Measured by the reviewer at `dc9e72bf` over the committed card: as a WHOLE LINE that six-space form occurs exactly ONCE, but as a SUBSTRING it occurs TWICE and INDENT-AGNOSTIC it occurs TWICE, because the live branch's copy is the same text at eight spaces and therefore contains the six-space form. The two readings disagree, which is precisely the condition R-0629 exists to forbid. NOTHING WENT WRONG, and the reason is the worker rather than the block: its applier asserted a count of 1 before deleting, got 2 under a substring reading, refused, switched to a whole-line index, and then verified BOTH that the following line was `    </section>` and that the live branch's copy survived. THE FIX IS THE ONE R-0629 ALREADY NAMES and the R36 block did not follow: a destructive target is quoted with the reading it is unique under stated beside it, and both readings are printed by the block's own script before emission. The prose identified the line unambiguously — "immediately above the `</section>` of the PRE-STREAM FALLBACK branch" — which is why this cost the round nothing, but prose is not a count and a gate is not satisfied by being understandable.

Gate: R37 — the R36 entry. R36 PASSED ON EVERY GATE WHOSE SUBJECT IS THE WORK, EACH RE-MEASURED INDEPENDENTLY BY THE REVIEWER RATHER THAN READ BACK FROM THE HANDBACK, AND ITS ONE SUBSTANTIVE DEVIATION IS THE REVIEWER'S OWN BLOCK DEFECT, RECORDED ABOVE. R36 IS THE ROUND THAT FINISHED F021'S BUILD: `apps/ui/src/components/panels/ChatInput.tsx` — 47 lines, NEW, the path component_spec.md names — renders the steering input VISIBLE and DISABLED in BOTH branches of the activity card, with the reason announced through `aria-describedby` and not only through a `title` a keyboard reader never sees, and with `onSend` declared but deliberately not destructured because a disabled input holds no state to send. DECISION F021 D11, landed at C3 BEFORE the code that cites it, settles a real conflict the reviewer found rather than papered over: `ux_spec.md` §11.3 and `T5_F021.md` give this one tooltip two different texts, and `.agent/context.md` makes the design reference binding for a visual surface, so the reference's sentence ships. THE REVIEWER TRACED THAT SENTENCE TO ITS SOURCE rather than to the block: it is present in `ux_spec.md` line-wrapped, present unwrapped in the card, and equal to the contract's own `REASON` constant, so the three cannot drift apart silently. RE-MEASURED GATES: `tests/ui_contracts/` 495 passed and 4 skipped against 490 and 4 at the base, the difference being the contract's five tests; `npm run test:unit` 16 files and 218 tests, UNCHANGED, as a round adding no `.test.ts` must be; `npx tsc --noEmit` exit 0 with EMPTY output; all four state readers 528; the canary 42. `.agent/decisions.md` went 117 to 118 `^## DECISION ` headings with D11 the only addition, and BOTH appended files are byte-exact prefixes of their successors with a remainder of exactly one newline plus the slice plus one newline. `ChatInput.tsx` on disk is BYTE-IDENTICAL to its slice plus one terminating newline. THE RED-PROOF WAS REAL AND SUBTLE BY DESIGN: deleting the input from the PRE-STREAM FALLBACK branch alone — the branch a reader sees before any job runs, and the one a reviewer watching a running cockpit would never notice — printed `1 failed, 66 passed` with the sole failure being the test that counts both render sites. THE LEDGER held at 224 under `^- R-\d+ — `, all distinct, maximum R-0661. STRUCTURE: eight commits, every one single-parent, insertions 448, 377, 16, 6, 10, 69, 47 and 93, each under 500. C6's own three readings are `dc9e72bf`, +93/-83, and 137 lines, over the 100-line tier with the cause declared. ONE DECLARED DEVIATION IS ACCEPTED AND WORTH KEEPING: the worker added a SECOND worktree, which constraint 9 did not allow, in order to re-measure the base figure G7 merely asserted — it printed 62 against 67 and confirmed the +5 independently. That is the constraint being too tight rather than the worker being out of scope, and a round that verifies a number I gave it instead of trusting me is the behaviour this protocol exists to produce.
<<<END RECORD37
