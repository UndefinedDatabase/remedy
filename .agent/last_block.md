── STEP T002 PART 5A / F040 — ROUND 11 ────────────────────────
Goal:        Build the completion digest's HERO CARD COMPONENT — the first
             `.tsx` of this feature — with the dismissal port bound at its edge
             per DECISION F040 D8, pin it with a pytest text guard that is red
             proved, and repair finding R-0756 in the vitest file that round 9
             shipped blind.
Bundle:      C0a save this block verbatim · C0b mirror it · C1 the plan ·
             C2 the record (the R9 verdict and R-0756) · C3 export the two
             estimate constants · C4 repair R-0756 · C5 the component ·
             C6 the guard · C7 the handback.
Change:      EXACTLY these paths and nothing else.
               `.agent/authored/f040-r11.md`                       (C0a, new)
               `.agent/last_block.md`                              (C0b)
               `.agent/plan.md`                                    (C1)
               `.agent/live_review.md`                             (C2)
               `apps/ui/src/components/metrics/TopMetricsBar.tsx`  (C3)
               `apps/ui/src/api/digestCardCopy.test.ts`            (C4)
               `apps/ui/src/components/digest/DigestHeroCard.tsx`  (C5, new)
               `tests/ui_contracts/test_digest_hero_card.py`       (C6, new)
               `.agent/handoff.md`                                 (C7)
             NOTHING ELSE IS EDITED. `digestCardCopy.ts`, `jobDigest.ts`,
             `digestVisibility.ts`, `DigestHeroCard.module.css`, `humanCopy.ts`,
             `run_report.py`, `job_digest.py`, every file under
             `docs/roadmap/` and every other test file are READ ONLY.

Constraints:
 1. APPLY EVERY AUTHORED SLICE BYTE FOR BYTE. If a slice looks wrong, apply it
    anyway and DECLARE the objection in the handback. Never repair a slice.
 2. THE COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4, C5, C6, C7 and it is fixed.
    Every claim any slice makes about this round's own landed change rests on
    this ordering constraint and on nothing else (§3 item 20, R-0524 carve-out).
 3. C1 IS THE FIRST SUBSTANTIVE COMMIT (§3 item 23): the round moves the finding
    ledger, so `.agent/plan.md` is current before the ledger is touched.
 4. RECORD11 IS APPENDED, never inserted. `.agent/live_review.md` ends with a
    single newline and no trailing blank line at the branch tip this round
    opens on; the append is one newline followed by the slice's bytes.
 5. THE BLOCK ARRIVES AS A FILE, NOT AS TYPED TEXT. It is on disk at
    `.remedy-wt/f040-r11-block.md`, written there by the reviewer. Copy it to
    both destinations with `shutil.copyfile` and never retype it. Because that
    original survives, G1 is a `cmp` against it rather than a chain of the
    worker's own outputs, and the transport proof this round therefore does
    cover the emitted bytes (§3 item 37). Two lines of the frame are runs of the
    single character `─`: the STEP line's trailing run is 24 characters and the
    closing line is 62. Their lengths are stated because a run has none a reader
    recovers by eye; nothing appliable lives in the frame either way.
 6. THE CARD ADDS NO CSS. `DigestHeroCard.module.css` is not in the change set.
    The component uses the three classes the round-8 sheet defines and plain
    semantic elements for everything else. The layout rules belong with the
    mount, where the card is first seen in context, and that is step 2 of the
    plan.
 7. THE CARD READS NO CLOCK EXCEPT AT THE DISMISSAL, AND IT READS NO STORAGE AT
    ALL. `Date.now()` is called in exactly one place — the dismiss handler, which
    is the edge DECISION F040 D8 names — and every persisted read or write goes
    through the injected `DigestVisibilityPort`. `localStorage`,
    `sessionStorage`, `fetch` and `XMLHttpRequest` do not occur in the
    component's executable source.
 8. NO RULE GETS A SECOND HOME. The card imports every decided value and
    restates none: the state phrase from `digestStateLabel`, the call to action
    from `digestCtaText`, the exactness flag from `digestCostLine`, and the two
    estimate constants from `TopMetricsBar.tsx`. None of the seven `RunState`
    phrases, neither `"~"` nor `", estimated"`, and no forbidden-word list may
    appear as a literal in `DigestHeroCard.tsx`.
 9. THE HEADLINE IS RENDERED AS THE SERVER WROTE IT, with no §17 screen, and the
    component says why where a reader would search: `_headline` in
    `packages/orchestration/job_digest.py` composes the digest's OWN prose as one
    plain sentence and never borrows the report's Markdown, so unlike
    `primary_action.label` it carries no markup and no identifier to remove. That
    reading was taken at `5778fccb`.
10. NO TYPESCRIPT MUTATION OF THE COMPONENT. `apps/ui/vitest.config.ts` at
    `5778fccb` sets `environment: "node"` and `include: ["src/**/*.test.ts"]`,
    and `apps/ui/package.json` ships no jsdom, happy-dom or testing library — so
    a `.tsx` is neither collected by the runner nor renderable by it. The
    component's colour is the pytest guard of C6, which IS red proved, plus
    `tsc`. G7's vitest colour is ordered over `digestCardCopy.test.ts`, a `.ts`
    file the runner does collect, and over nothing else.
11. DESTRUCTIVE VERIFICATION ONLY INSIDE A DISPOSABLE `git worktree`, removed
    before the handback, with `git worktree list` showing one line. The primary
    checkout satisfies `git status --porcelain` empty at every commit.
12. RE-READ `.agent/STOP` FROM DISK BEFORE THE FIRST COMMIT AND AGAIN BEFORE
    C7. If it appears, finish the commit in hand, write the handback and stop.
13. THE FIX FOR R-0756 IS EXACTLY THE PROBE VALUE AND ITS DISCRIMINATOR. C4
    touches no other test in that file and changes no production code: the module
    is already correct and this round proves that the guard over it now bites.
14. THIS BLOCK IS A VERBATIM RENUMBERING OF ROUND 10's BLOCK, dated
    2026-08-29, decided by the reviewer per the round-10 handback's own
    deferral. Round 10 already completed one full delegate-review cycle — it
    hit `.agent/STOP` before its first commit and closed with a stop-handback
    at commit `19ff6482` — so this re-dispatch of the identical, never-executed
    bundle is round 11, not a continuation of round 10, per the F031 R10
    precedent the round-10 handback cites twice. No other content changed:
    every constraint, gate, spec and pair below is identical in substance to
    round 10's block, with only the round number, the two slice labels
    (PLAN10→PLAN11, RECORD10→RECORD11) and the `f040-r10.md`→`f040-r11.md`
    filename updated for consistency. Declare this renumbering in the handback
    as a reviewer decision, not a worker deviation.

Done when: every gate below is executed, each with its REAL exit code taken from
`subprocess.run(...).returncode`. All of them run at commits strictly earlier
than C7 (§3 item 31), and the commit each runs at is named below.

 G1 TRANSPORT, at C0b. ONE comparison, disk to disk, against the reviewer's own
    surviving original: report the sha256 and byte length of
    `.remedy-wt/f040-r11-block.md`, of `.agent/authored/f040-r11.md` and of
    `.agent/last_block.md`, and that all three are equal. Report the digest you
    MEASURED; this block asserts no digest of itself, which it could not do.
 G2 THE PLAN, at C1. `.agent/plan.md` byte-equal to the PLAN11 slice; report its
    line count and that it is under 50; report that it holds `## Goal`,
    `## Next Steps` and a string matching `\bF\d{3}\b`.
 G3 THE RECORD APPEND, at C2. Re-measure the pre-commit length rather than
    taking it from this block. Reading (a): the base blob is a byte PREFIX of the
    committed file and base + one newline + slice reconstructs it whole.
    Reading (b), independent and structural: split the slice on blank lines,
    COUNT the paragraphs into N, and compare the committed file's LAST N
    blank-line units against those N paragraphs IN ORDER. Negative control:
    inside the disposable worktree, flip one byte in the FIRST appended
    paragraph and report that both readings REJECT it and both ACCEPT the
    unflipped bytes. N is counted by the script and never asserted.
 G4 THE LEDGER, at C2. Compute by DIFFERENCE between the pre-commit base and the
    committed file, never by reading the slice: the distinct ids matching
    `^- R-\d+ — `, those matching `^Done: R-\d+`, those matching
    `DECISION F040 D\d+`, and the count of lines matching `^Gate: F040 R9 — `.
    Report ADDED and REMOVED for each set and the open count before and after.
 G5 THE COMPONENT'S SHAPE, at C5. Over `DigestHeroCard.tsx` with comments
    stripped and quoted literals blanked for the absence half:
      - the exported names, parsed from the source;
      - every module it imports from, and the names taken from each;
      - every `styles.<name>` it references, and that each such name is a class
        the round-8 sheet declares — parse the class names out of
        `DigestHeroCard.module.css` rather than retyping them;
      - occurrences of `localStorage`, `sessionStorage`, `fetch` and
        `XMLHttpRequest`, each of which must be 0, and each paired with a salted
        positive control proving the scan can see it when it is there;
      - occurrences of `Date.now`, which must be exactly 1;
      - that none of the seven `RunState` phrases of `DIGEST_STATE_LABELS`, and
        neither `~` nor `, estimated`, occurs as a quoted literal in the card —
        parse those phrases out of `digestCardCopy.ts` and out of
        `TopMetricsBar.tsx` rather than retyping them;
      - and that `TopMetricsBar.tsx` still contains the byte strings
        `const ESTIMATE_MARK = "~";` and `const ESTIMATE_PHRASE = ", estimated";`,
        which `tests/ui_contracts/test_job_digest_card_contract.py` and
        `tests/ui_contracts/test_cost_metric_render.py` assert at `5778fccb` —
        BOTH of them, measured at emission — so C3's export cannot falsify a
        guard this round does not own.
 G6 THE GUARD AND ITS RED PROOF, at C6. First
    `python3 -m pytest tests/ui_contracts/test_digest_hero_card.py -q` in the
    primary checkout. Then, inside a disposable worktree at that commit, the
    UNMUTATED CONTROL first and each mutation reverted before the next, run the
    same node id and report the REAL exit code and the node ids that DIED for
    each of these four mutations of `DigestHeroCard.tsx`:
      (a) render `digest.primary_action.label` where `digestCtaText(...)` stands;
      (b) restate one `RunState` phrase as a literal in the card;
      (c) replace the port's `writeDismissal` call with `localStorage.setItem`;
      (d) delete the emptiness guard in front of the ownership section.
    Assert each anchor is UNIQUE in the file before replacing it, and report the
    count. For each, report that the bytes on disk differ from the original AND
    that the DECLARATION differs after comment stripping — a mutation that lands
    in a comment proves nothing, which is the R8 lesson. Restore and report byte
    equality to the committed file and the control's colour again.
 G7 R-0756 REPAIRED, AND PROVED, at C4. By the worktree route DECISION F256 D6
    fixes: put the mutation in the worktree, run vitest from the PRIMARY
    `apps/ui` so resolution finds the primary's `node_modules`, and name the
    worktree's test file by ABSOLUTE path in a scratch config under
    `.remedy-wt/` whose `cacheDir` also points inside `.remedy-wt/` so the
    primary checkout stays clean. The config must export a PLAIN OBJECT.
    Report, in this order: the UNMUTATED CONTROL's real exit code and test
    count; then, with the own-property guard in `digestStateLabel` replaced by
    `return DIGEST_STATE_LABELS[key] ?? UNREADABLE_STATE_LABEL;` in the
    WORKTREE'S COPY OF `digestCardCopy.ts`, the real exit code and the node ids
    that died — which must be non-zero, and that is the whole point of the
    repair; then the restored control. The production module is NOT edited in
    the primary checkout at any point.
 G8 THE SUITES, THE TOOLCHAIN AND THE TREE, at C6:
      python3 -m pytest tests/ui_contracts/ -q
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/docs/ -q
      python3 -m pytest tests/cli/test_golden_path.py -q
      python3 -m pytest "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" -q -rs
      python3 -m pytest tests/ui_server/test_dashboard_contract.py -k typescript -q -rs
    Report each REAL exit code, and for the last two report PASSED or SKIPPED
    explicitly — a skip is not a type check and is not vitest. Then report
    `git status --porcelain`, the count from
    `git ls-files --others --exclude-standard`, `git worktree list`, and the `+`
    column of `git diff --numstat` for each commit from C0a through C6. C7's own
    insertion count is not orderable here and is not ordered (§3 item 14).
    Those insertion numbers are ALSO required by
    docs/agents/handback_template.md in the `+/-` column of the handback's
    `## Commits` table, which makes C7 their second writer: when you write that
    table, take every cell from THIS gate's `git diff --numstat` output and from
    nothing else, and say in the handback that you did (§3 item 28). A full-file
    rewrite is where the two readings diverge — `git commit`'s own summary and
    the file's before/after line counts are neither of them the `+` column
    AGENTS.md's counting rule names.

Handback:    rewrite `.agent/handoff.md` per docs/agents/handback_template.md.
             Carry the SESSION NUMBER — this is SESSION 3 of F040 — the round
             (11), the range, the per-commit table with the `+/-` column from
             `git diff --numstat`, one line per gate with its REAL exit code,
             the item-status table, the deviations (including the round-10→11
             renumbering, cited as constraint 14), and the open-findings count.
             Then `git push -u origin feature/f040-completion-digest`. Create no
             pull request, merge nothing, force-push nothing, touch no branch.
──────────────────────────────────────────────────────────────

<<<BEGIN PLAN11
# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 3, round 11.

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
| T002 the client digest seam and its guard | done | round 6, PASS |
| T002 the trigger, dismiss and last-seen rule | done | round 7, PASS |
| T002 the hero card stylesheet and its guard | done | round 8, PASS |
| T002 the card's copy rules and the §17 screen | done | round 9, PASS |
| T002 the card component and its guard | done | this round |
| T002 the mount, the data load and the layout CSS | open | next |
| T003 CLI parity and the end-to-end | open | |

## Next Steps
1. This round builds `DigestHeroCard.tsx` with the dismissal port bound at its
   edge, pins it with a pytest text guard, and repairs R-0756 — the prototype
   test round 9 shipped blind.
2. The next round MOUNTS the card: the shell placement, the digest load through
   `jobDigestPath`, the last-seen clock, and the layout CSS this round
   deliberately did not write.
3. Then T003's `remedy job digest`, the end-to-end, the integration gate and
   closure.

## Risks
- R-0570, R-0752 and R-0755 stay OPEN and are routed to the paydown branch; none
  is F040's to fix. R-0753 stays OPEN as this feature's documented risk.
- The card gets no vitest colour at all, and the reason is the runner rather than
  the session: `apps/ui/vitest.config.ts` sets `environment: "node"` and includes
  `src/**/*.test.ts` only, and the package ships no DOM library, so a `.tsx` is
  neither collected nor renderable. Its colour is a pytest text guard, which IS
  red proved, plus `tsc`.
<<<END PLAN11

<<<BEGIN RECORD11
Gate: F040 R9 — T002 PART 4, THE HERO CARD'S COPY RULES. VERDICT PASS. Reviewed by re-running every gate in the reviewer's own drivers under the gitignored `.remedy-wt/`, and by running colours the block did not order. TRANSPORT: `.agent/authored/f040-r9.md` and `.agent/last_block.md` are equal at sha256 `fcfd0b131dec41599c12e9b67453c14a2170b0d541a3a79aec545ca1b40cc723` over 24159 bytes; per §3 item 37 that chain walks the worker's own two outputs, no scratchpad original of the R9 block survived its session, and the EMITTED bytes are therefore NOT covered and are not claimed. THE PLAN is byte-equal to PLAN9 at sha256 `257ed7df0420f852d9aa23d880db1c6c227f5db45fa0a448a6d770899de30adb`, 2034 bytes, 41 lines, carrying `## Goal`, `## Next Steps` and the feature id. THE RECORD APPEND reconstructs whole at 1703971 + 1 + 6230 = 1710202, the base a byte PREFIX, N COUNTED at 2 rather than asserted, paragraph order holding over the WHOLE appended region, and a negative control flipped at byte 1704031 INSIDE the FIRST appended paragraph rejected by both readings while the unflipped bytes are accepted by both. THE LEDGER moved exactly as ordered, computed by DIFFERENCE against the base and never from the slice: registered 316 to 316 with ADDED `[]` and REMOVED `[]`, resolved 54 to 54, `DECISION F040` ADDED `['D10']`, one `^Gate: F040 R8 — ` line, open count 262 to 262. THE MODULE READS CORRECTLY AGAINST ALL FOUR OF ITS SOURCES, each parsed rather than grepped: the seven `RunState` members of `packages/core/models.py` are all keys of `DIGEST_STATE_LABELS`; the five `NextAction` ids of `recommended_next_action` are `DIGEST_CTA_RULE_IDS` in that function's own first-match order and the tuple invents none; `scrubUiText` is imported from `../copy/humanCopy` and used, `stateLabel` is not imported, and the empty case is carried by `scrubUiText`'s OWN `fallback` parameter rather than by a second mechanism. FIVE SUITES REPRODUCED TO THE TEST, all REAL exit 0: `tests/ui_contracts/` 758 passed and 4 skipped, the rise of 23 over the base being exactly the tests C5 adds; `tests/ui_server/` 515; `tests/docs/` 295; the canary 42; and both frontend nodes PASSED rather than skipped, unmoved at 4 and 1. Seven commits at insertions 327, 232, 15, 4, 155, 233 and 454 by `git diff --numstat`, every one under 500, with the handback commit at 404. Tree clean, zero untracked, `git worktree list` one line. THE REVIEWER RAN THE TYPESCRIPT COLOUR THE BLOCK FORBADE, AND TWO SENTENCES THE HANDBACK CARRIES ABOUT THAT PROHIBITION ARE FALSE ON DISK. FIRST, deviation 4 states that `apps/ui/src/api/digestCardCopy.test.ts` "has never been executed by a test runner in this round" and that the G7 nodes report only that the foundation is in place. Measured at `5778fccb`: `test_vitest_passes` in `tests/orchestration/test_test_runner.py` runs `npx vitest run` with `cwd` at `apps/ui` and NO scope, so it collects that file with every other — the run reports 36 test files and 717 tests at REAL exit 0, and 38 of its verbose lines name `digestCardCopy.test.ts`. The file WAS executed and WAS green, so the worker understated its own evidence. SECOND, the "Next" section grounds its prohibition partly on "`npx vitest` is refused to this session class", and that is the R-0724 confusion: the direct shell spelling is refused, a `subprocess.run` from a Python driver is not, and a refusal binds the CALLER rather than the environment. Neither sentence damaged anything on disk, so under amend0827 rule 2 they spend no id and buy no correction round; they are dated lines in `.agent/prose_slips.md` at the next round that writes one. THE OTHER TWO GROUNDS OF THAT PROHIBITION ARE TRUE, AND ITS CONCLUSION SURVIVES INTACT: every decidable rule really has been pushed out of the component, this repository really renders no component in any test, and the card round really does get no vitest colour — for a reason about the RUNNER rather than about the session, which is the version the next block must carry. At `5778fccb` `apps/ui/vitest.config.ts` sets `environment: "node"` and `include: ["src/**/*.test.ts"]`, and `apps/ui/package.json` names no jsdom, no happy-dom and no testing library, so a `.tsx` is neither collected by that glob nor renderable in that environment. THE REVIEWER THEREFORE RED-PROVED THE R9 MODULE ITSELF, by the worktree route DECISION F256 D6 fixes, with the unmutated control first and each mutation reverted before the next: control REAL exit 0 at 38 passed; removing the markdown-link unwrap exit 1 at 3 failed; removing the trailing-command strip exit 1 at 5 failed; bypassing `scrubUiText` exit 1 at 2 failed; changing one `RunState` phrase exit 1 at 1 failed; and the restored module exit 0 at 38 passed again, byte-equal to the committed blob. Four of five mutations are red and the module's rules are real. THE FIFTH CAME BACK GREEN AND IS REGISTERED BELOW AS R-0756. The round PASSES: every ordered command is green under the reviewer's own hand, the diff is clean, no block condition of §4 item 5 is met, and the one defect found is a blind test rather than a wrong value — the production module is correct today and the guard over one of its properties is not.

- R-0756 — Medium, A VITEST TEST NAMES THE PROTOTYPE-CHAIN HAZARD AND CANNOT SEE IT, SO A GUARD OVER PRODUCTION CODE IS BLIND WHILE READING ON THE PAGE EXACTLY LIKE A GUARD. Raised by the reviewer at the F040 R9 gate, from a mutation the R9 block did not order. THE TEST, at `apps/ui/src/api/digestCardCopy.test.ts` in the `digestStateLabel` describe block: `it("does not read a state off the prototype chain")` asserts `digestStateLabel("toString")` is `"State not recorded"`, under a comment reading "`DIGEST_STATE_LABELS` is a plain object, so an unguarded index would answer a FUNCTION here rather than a sentence". THE DEFECT: `digestStateLabel` folds its key — `String(state ?? "").trim().toLowerCase()` — so `"toString"` becomes `"tostring"`, which `Object.prototype` does not carry, and the lookup misses the prototype entirely and reaches the fallback for the wrong reason. MEASURED at `5778fccb`, inside a disposable worktree, by the F256 D6 route: replacing the whole `Object.prototype.hasOwnProperty.call(DIGEST_STATE_LABELS, key) ? DIGEST_STATE_LABELS[key] : UNREADABLE_STATE_LABEL` expression with `DIGEST_STATE_LABELS[key] ?? UNREADABLE_STATE_LABEL` leaves ALL 38 vitest tests GREEN at REAL exit 0, and all 23 tests of `tests/ui_contracts/test_digest_card_copy.py` green as well, so nothing anywhere would notice the guard being deleted. The mutation was shown to reach a declaration rather than a comment, its bytes differing after comment stripping. THE DISCRIMINATOR THAT DOES WORK, measured by the same route with a probe spec written into the worktree only: `"constructor"` is already lowercase, so it survives the fold, and with the guard present `digestStateLabel("constructor")` answers `"State not recorded"` while with the guard removed it answers `"function Object() { [native code] }"` — a raw JavaScript function, rendered into a hero card, which is the most literal `ux_spec.md` §17 violation this feature could produce. SHIPPED BEHAVIOUR IS CORRECT TODAY and this is not a wrong value on screen; what is wrong is that the property is unpinned, and the natural simplification of that expression to `??` is exactly the edit no test would catch. THE OPEN SET WAS SEARCHED FOR THE DEFECT BEFORE THIS ID WAS MINTED, per §3 item 30: `hasOwnProperty` occurs five times in `.agent/live_review.md` and `toLowerCase` zero times, and no OPEN finding concerns a blind prototype test. The nearest neighbour is `R-0731`, which is the same hazard SHIPPED in `diffViewModel.ts` and RESOLVED at F037 R23 — a different module and a different fault, since there the behaviour was wrong and here only the gate is, so this takes its own id rather than reopening that one. R-0731's resolution is nonetheless the precedent that makes this Medium rather than Low: it landed BOTH halves of its fix on purpose, "because either one alone is undone silently by a later refactor", and this repository has therefore already paid once for exactly the class of drift an unpinned own-property guard invites. FIX, binding on F040 round 10: change the probe value in that test to `"constructor"`, and keep `"toString"` beside it in a SECOND test that states in its own words that the key is folded and that `"toString"` alone would therefore prove nothing — a probe and its discriminator, the shape the rest of that file already uses. Prove the repair by re-running the guard-removal mutation and showing it now goes RED, naming the node ids that died. Touch no production code: the module needs no change, and a fix that edited it would be repairing the wrong half.
<<<END RECORD11

SPEC — `apps/ui/src/components/digest/DigestHeroCard.tsx` (C5, new file)

Write the component; this is a description, not a slice, and the words are
yours. It must satisfy every constraint above and the guard of C6.

EXPORT one function component, `DigestHeroCard`.

PROPS, one object, every one of them a VALUE or a callback so the component
binds nothing it is not the edge for:
  digest: JobDigest                      — from `../../api/jobDigest`
  visibility: DigestVisibility           — from `../../api/digestVisibility`
  port: DigestVisibilityPort             — from `../../api/digestVisibility`
  onDismissed?: () => void
  onOpenDecisions?: () => void
  onPrimaryAction?: (ruleId: string) => void

BEHAVIOUR:
  - When `visibility.show` is false the component renders `null`. The RULE is
    `digestVisibility`'s and this component re-derives none of it; it is handed
    the answer and branches on it.
  - The dismiss control calls `port.writeDismissal(digest.job_id, Date.now())`
    and then `onDismissed?.()`. That `Date.now()` is the ONE clock read in the
    file and it is here because this is the edge — the same split
    `AgentNowCard.tsx` makes for `recency.ts`.

MARKUP, inside `<section className={styles.heroCard} data-state={digest.state}>`:
  - the headline in `<h2 className={styles.heroHeadline}>`, rendered as the
    server wrote it, with the constraint-9 reason in a WHY comment above it;
  - the state phrase from `digestStateLabel(digest.state)`;
  - the cost line: `digestCostLine(digest.cost)` gives `{ value, estimated }`,
    and when `estimated` is true the line carries `ESTIMATE_MARK` before the
    value and `ESTIMATE_PHRASE` after it, the treatment `TopMetricsBar.tsx`
    already uses;
  - the ownership sentences ONLY when `digest.ownership.length > 0` — DECISION
    F040 D3 rules that an empty list is OMITTED rather than rendered empty, and
    the guard reads that emptiness check;
  - the decisions control ONLY when `digest.decisions.open_count > 0`, calling
    `onOpenDecisions`, naming the count and the peak urgency;
  - the single call to action in `<button className={styles.heroCta}>` whose
    text is `digestCtaText(digest.primary_action.label)` — never the raw label —
    calling `onPrimaryAction?.(digest.primary_action.rule_id)`.

`data-state` carries the raw state for a LATER round to colour the headline
from, which is why the state phrase and the attribute are separate: the sheet
gains its state colours with the mount, and the component needs no edit then.

Write the header comment the way the three sibling digest modules write theirs:
what the file is, why it exists, and its deliberate absences named where a
reader would search for them.

SPEC — `tests/ui_contracts/test_digest_hero_card.py` (C6, new file)

Follow the shape of `tests/ui_contracts/test_digest_card_copy.py` at `5778fccb`
— comment stripping, literal blanking, a salted positive control beside every
absence, and a `TestTheStrippersReallyStrip` class proving the strippers strip.
Import nothing from that file; the helpers are short and a shared import would
couple two guards. Pin, each with its own discriminator:

  1. THE COMPONENT IS THE EDGE AND NOTHING MORE. `localStorage`,
     `sessionStorage`, `fetch` and `XMLHttpRequest` occur zero times in the
     executable source; `Date.now` occurs exactly once; `writeDismissal` occurs.
  2. NO RULE HAS A SECOND HOME. None of the seven `RunState` phrases — parsed
     out of `DIGEST_STATE_LABELS` in `digestCardCopy.ts`, not retyped — occurs
     as a quoted literal here, and neither does `~` nor `, estimated`, both
     parsed out of `TopMetricsBar.tsx`.
  3. EVERY DECIDED VALUE IS IMPORTED: `digestStateLabel` and `digestCtaText`
     from the copy module, `digestCostLine` from the envelope module,
     `ESTIMATE_MARK` and `ESTIMATE_PHRASE` from `TopMetricsBar`.
  4. THE CTA GOES THROUGH THE RULE. `digestCtaText(` occurs in the source and
     the raw `primary_action.label` is never placed in markup — assert on the
     shape you can actually read, and say in the test's own docstring what the
     reader can and cannot see.
  5. DECISION F040 D3 IS ON DISK: the ownership section sits behind an
     emptiness check on `ownership`.
  6. EVERY `styles.<name>` the component names is a class
     `DigestHeroCard.module.css` declares — parse the class names out of the
     sheet rather than retyping them, so a renamed class fails here.

PAIR TMB-1 — `apps/ui/src/components/metrics/TopMetricsBar.tsx` (C3)
TO contains FROM: true — this is an APPEND-shaped pair, so the obligation is
the §4.9 ordered-equality reading and NEVER a FROM-zero count.
FROM:
const ESTIMATE_MARK = "~";
TO:
export const ESTIMATE_MARK = "~";

PAIR TMB-2 — same file (C3)
TO contains FROM: true — APPEND-shaped, same obligation.
FROM:
const ESTIMATE_PHRASE = ", estimated";
TO:
export const ESTIMATE_PHRASE = ", estimated";

WHY THESE TWO PAIRS EXIST: `tests/ui_contracts/test_job_digest_card_contract.py`
asserts at `5778fccb` that those two byte strings are present in that file and
that `jobDigest.ts` contains neither — the "one home" property. The hero card
needs the same two words, and importing them keeps that home single, where
retyping them would give the phrase the second home the guard exists to
prevent. Prefixing `export ` leaves both asserted substrings intact, which G5
re-measures rather than assumes.

SPEC — `apps/ui/src/api/digestCardCopy.test.ts` (C4, the R-0756 repair)

In the `digestStateLabel` describe block, replace the existing
`"does not read a state off the prototype chain"` test with two:

  - the same name, now probing `"constructor"`, whose comment states that
    `"constructor"` is already lowercase and therefore survives the key fold and
    really reaches `Object.prototype`, and that without the own-property guard
    it answers the `Object` constructor function;
  - a second test stating that the key is FOLDED, probing `"toString"` and
    `"TOSTRING"`, whose comment says these fold to `"tostring"`, which
    `Object.prototype` does not carry, so they would answer the fallback with or
    without the guard — which is why the probe above uses `"constructor"`.

Change nothing else in that file. The production module is correct and is not
edited.
