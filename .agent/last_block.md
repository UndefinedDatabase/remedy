# STEP R9/F040 — T002 PART 4: TURNING REPORT MARKUP INTO CARD COPY

Goal: the last decidable half of the hero card. The digest's `primary_action.label`
is written for a MARKDOWN REPORT and the cockpit may not render it raw; this
round rules that collision as DECISION F040 D10 and builds the pure copy rules
that resolve it, so the round that mounts the card has nothing left to decide.
Book the round 8 verdict.

Base: `b2cef8cb`, the round-8 handback commit and the tip of
`feature/f040-completion-digest`. Stay on that branch. Open no pull request.

THE COLLISION, MEASURED AT THE BASE — this is the whole reason for the round.
`docs/ui/design_reference/ux_spec.md` §17 forbids the default UI showing raw
UUIDs or raw JSON, and requires human phrasing. But `primary_action.label` comes
verbatim from `recommended_next_action` in `packages/orchestration/run_report.py`,
which builds it for a Markdown artifact, and TWO of its five rules emit markup or
identifiers:

- `open-decision` (:385-394) emits ``Answer the open decision: `<command>` ``
  where the command is a copy-pasteable CLI line carrying a job-id prefix and a
  `td:` decision id — visible in the R5 golden
  `blocked_with_decisions.json`. It degrades to the bare sentence when no
  command exists, so the id is CONDITIONAL, not guaranteed.
- `blocked-failed` (:403-407) emits `Inspect {target} and repair the blocked
  task`, where `target` is `_link("the postmortem", ref)` and `_link` (:358-363)
  returns `[the postmortem](ref)` — MARKDOWN LINK SYNTAX — whenever an evidence
  ref exists, and the bare label when it does not.

The other three — `stopped-by-operator` (:397-401), `all-green` (:411) and
`indeterminate` (:413) — carry neither. NOTE that the four goldens exercise only
`open-decision`, `blocked-failed`, `all-green` and `indeterminate`: the rule
table has FIVE rules and `stopped-by-operator` is reached by no fixture, so the
goldens are a sample and the RULE TABLE is the vocabulary. Read the table.

THIS IS NOT A DEFECT AND MINTS NO FINDING. The label is CORRECT for the report
and for the CLI, where a copy-pasteable command is the useful thing. The
collision is only at the cockpit's render boundary, and nothing on disk is
wrong-valued, so it is ruled as DECISION F040 D10 in the manner D3 and D5
already handled "the feature file asks for something this surface cannot give" —
not registered as an R-id, per amend0827 rule 2.

TWO TRAPS IN THE EXISTING COPY MODULE, both measured, both of which a builder
would otherwise walk into:
- `apps/ui/src/copy/humanCopy.ts` exports `stateLabel(state)`, and its vocabulary
  is the CHECKLIST's — `done`, `current`, `blocked`, `suggested`, else
  `"Planned"`. `RunState` shares NONE of those spellings, so `stateLabel` answers
  `"Planned"` for `completed`, `paused`, `running` and every other digest state.
  It is the wrong function and must not be used here.
- `scrubUiText(value, fallback)` in the same file rejects a value that is
  ENTIRELY hex-ish (`/^[0-9a-f]{6,}(-[0-9a-f]+)*$/i`), so it cannot see an id
  EMBEDDED in a sentence. It is still the right final screen — it owns §17's
  forbidden-word list — but it is not sufficient alone.

## Bundle, in commit order

- C0a save this block verbatim to `.agent/authored/f040-r9.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1  rewrite `.agent/plan.md` from slice PLAN9
- C2  append slice RECORD9 to `.agent/live_review.md`
- C3  add `apps/ui/src/api/digestCardCopy.ts` per the SPEC below
- C4  create `apps/ui/src/api/digestCardCopy.test.ts` per the SPEC below
- C5  create `tests/ui_contracts/test_digest_card_copy.py` per the SPEC below
- C6  rewrite `.agent/handoff.md` — the handback

## Change set — exactly these paths, nothing else

    .agent/authored/f040-r9.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    apps/ui/src/api/digestCardCopy.ts
    apps/ui/src/api/digestCardCopy.test.ts
    tests/ui_contracts/test_digest_card_copy.py
    .agent/handoff.md

NOTHING ELSE IS EDITED. Not `apps/ui/src/copy/humanCopy.ts` — it is imported,
not changed. Not `jobDigest.ts`, not `digestVisibility.ts`, not the stylesheet,
not `run_report.py`: the server's label is RIGHT for the report and this round
does not touch it. No `.tsx`. No Python production code.

## Constraints

1. Apply every slice BYTE FOR BYTE. If one looks wrong, apply it as given and
   DECLARE the problem in the handback's deviations.
2. C0a is a COPY: the block is at `.remedy-wt/f040-r9-block.md`. Use
   `shutil.copyfile` for C0a and again for C0b.
3. C1 is the FIRST substantive commit, ahead of the ledger append.
4. `.agent/live_review.md` is APPEND-ONLY.
5. `.agent/plan.md` stays under 50 lines.
6. Every exit code is REAL, from `subprocess.run(...).returncode` in a script
   under the gitignored `.remedy-wt/`. Never through a pipe.
7. Mutation and red-proof checks run ONLY in a disposable `git worktree`; the
   only red proof available is the PYTHON guard's (constraint 13).
8. THE MODULE IS PURE: no clock, no storage, no socket, nothing minted. Same
   absences the two sibling api modules document in their headers, written down
   the same way.
9. ONE SOURCE FOR THE §17 SCREEN. The forbidden-word list and the whole-value id
   test live in `humanCopy.ts`; this module IMPORTS `scrubUiText` and applies it
   as the FINAL pass. It does not restate that list, does not restate the
   fallback string and does not re-implement the truncation.
10. `stateLabel` FROM `humanCopy.ts` IS NOT USED — it answers the checklist's
    vocabulary, not `RunState`'s. Say so in a comment where a reader would reach
    for it.
11. THE WORDS STAY THE SERVER'S. This module REMOVES markup and identifiers; it
    does not rewrite the sentence, does not add a verb and does not substitute a
    phrase of its own. DECISION F040 D5 keeps the digest's CTA equal to the
    report's recommendation, and a client that reworded it would break that
    equality as surely as a second rule table would.
12. Commit subjects carry no leading-slash token, no absolute path, no
    secret-like string, and no `Co-Authored-By` trailer. Push after C6. No pull
    request, no merge, no force-push. The `remedy` script is DENIED; use
    `python3 -m apps.cli.main ...` if needed and say so.
13. NO TYPESCRIPT COLOUR IS ORDERED (DECISION F040 D7): `npx vitest` is refused
    to this session class and `apps/ui/node_modules` is absent from a worktree,
    so a mutation there is red for every module. Do not attempt one; say in the
    handback that none was run.

## SANDBOX NOTES

- Env-var assignment is DENIED in all three shell forms; set it in-process.
- `cp` is denied; copy with `shutil.copyfile`.
- `$(...)` in a compound, `;`/`&&` chains and process substitution are rejected
  by FORM. One command per call, or a driver script run as one `bash script.sh`.
- A `python3 -c` script containing a newline followed by `#` is rejected; use a
  script FILE for anything carrying comments.
- The Bash tool does not surface non-zero exits; capture
  `subprocess.run(...).returncode`.

## Slices

The authored units are PLAN9 and RECORD9, each between its own BEGIN and END
marker line. The markers are NOT part of the unit; the newline ENDING the last
content line IS.

<<<BEGIN PLAN9
# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 2, round 9.

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
| T002 the card's copy rules and the §17 screen | done | this round |
| T002 the card itself, its mount and wiring | open | next session |
| T003 CLI parity and the end-to-end | open | |

## Next Steps
1. This round rules DECISION F040 D10 and builds `digestCardCopy.ts`: the state
   label the digest needs, and the rule turning the report's markup into copy
   the cockpit may show, with `scrubUiText` as the final §17 screen.
2. The next round mounts the card — the `.tsx`, the trigger wiring onto
   `digestVisibility`, the dismissal port bound at the edge per D8, and the
   stylesheet from round 8. Every rule it needs is now built and pinned.
3. Then T003's `remedy job digest`, the end-to-end, the integration gate and
   closure.

## Risks
- R-0570, R-0752 and R-0755 stay OPEN and are routed to the paydown branch; none
  is F040's to fix. R-0753 stays OPEN as this feature's documented risk.
- The card round is the first this feature cannot red-prove: a `.tsx` has no
  pure logic left to test and this repository renders no component. Every
  decidable rule has been pushed out of it on purpose, so what remains is
  wiring, pinned as TEXT by a guard.
<<<END PLAN9

<<<BEGIN RECORD9
Gate: F040 R8 — T002 PART 3, THE HERO CARD'S STYLESHEET. VERDICT PASS. Reviewed by re-running every gate in the reviewer's own driver. TRANSPORT is REAL at sha256 `faa78f87e238e94ca7aea52c2a009d155dcfed083ab5e3ac70550deed30d321c` over 26546 bytes, equal on all three copies. THE PLAN is byte-equal to PLAN8 at 1969 bytes and 41 lines. THE RECORD APPEND reconstructs whole at 1694456 + 1 + 9514 = 1703971, N counted as 3, order holding, base a prefix. THE LEDGER moved as ordered — registered ADDED `['R-0755']` and REMOVED `[]`, resolved ADDED `[]`, `DECISION F040` ADDED `['D9']`, one `^Gate: F040 R7 — ` line, open count 261 to 262. THE TRANSCRIPTION IS FAITHFUL, parsed rather than eyeballed: all SIXTEEN binding values of the three rules are present, the seven `--remedy-*` tokens the sheet names are all defined in `apps/ui/src/styles/tokens.css`, `#fff` occurs exactly once, every other hex and every `rgb(`/`rgba(` occurs zero times, and `animation`, `transition`, `transform` and `@media` are each zero — so `ux_spec.md` §16 is satisfied by carrying no motion at all rather than by a motion block nobody checked. Nothing under `docs/ui/design_reference/` was touched and no `.tsx` entered the change set, so the round did not edit its own authority. THE REVIEWER RED-PROVED THE GUARD IN ITS OWN WORKTREE WITH FIVE MUTATIONS, control first in each: `max-width` 720px to 640px killed the card rule's binding-value test; an UNDEFINED token killed both the CTA's binding-value test and the token sweep; a second raw colour killed the single-literal pin; a `transition` killed the no-motion pin; and a FIFTH the block did not order — swapping the CTA's `color:#fff` for `var(--remedy-ink)`, which is precisely the alternative DECISION F040 D9 REJECTED — killed the CTA binding test and the single-literal pin together. That fifth matters because it proves the guard can tell D9's chosen option from the option D9 turned down, which is the property that makes a decision enforceable rather than merely recorded. A NOTE ON THAT MUTATION, recorded because the reviewer got it wrong first and the lesson is general: the initial spelling replaced the FIRST `color: #fff;` in the file, which is inside the header comment quoting the sibling stylesheet, so the declaration was untouched and the guard stayed green — a green that looked like a gate blind spot and was in fact a mutation that never reached the code. It was caught by checking that the mutated text differed from the original in the DECLARATION rather than merely differing, and re-run against the declaration it reddened immediately. A mutation must be shown to reach the thing under test before its colour means anything. FIVE SUITES all REAL exit 0: `tests/ui_contracts/` 728 to 735, a rise of exactly the SEVEN tests C4 adds with the four pre-existing skips unmoved, plus 515, 295 and the canary 42; both frontend nodes PASSED rather than skipped and are unmoved at 4 and 1, as a round adding no TypeScript requires. Tree clean, zero untracked, seven commits at insertions 314, 219, 18, 6, 60, 256 and 402, every one under 500. THE WORKER'S DEVIATIONS WERE ALL CORRECTLY DECLARED and one is worth keeping: it reports that `git commit` printed 314 insertions for C0b while `git diff --numstat` reads 219 for the same commit, a rewrite-detection difference, and it tabled the `--numstat` figure — which is the right choice, since AGENTS.md's counting rule names the `+` column of the diff and both readings are far under the cap either way.

DECISION F040 D10 — THE CARD SHOWS THE SERVER'S WORDS WITH THE REPORT'S MARKUP TAKEN OUT, AND REWRITES NOTHING. THE PROBLEM: `docs/ui/design_reference/ux_spec.md` §17 forbids the default UI showing raw UUIDs or raw JSON and requires human phrasing, while `primary_action.label` is carried verbatim from `recommended_next_action` in `packages/orchestration/run_report.py`, which composes it for a MARKDOWN artifact. MEASURED at `b2cef8cb` over the rule table rather than over the fixtures, because the four goldens reach only four of its five rules: `open-decision` (:385-394) emits a backticked, copy-pasteable CLI command carrying a job-id prefix and a `td:` decision id whenever a blocked item has an answer command, and degrades to the bare sentence when none does; `blocked-failed` (:403-407) builds its target through `_link` (:358-363), which returns MARKDOWN LINK SYNTAX `[the postmortem](ref)` whenever an evidence ref exists; `stopped-by-operator`, `all-green` and `indeterminate` carry neither, and `stopped-by-operator` is reached by no golden at all. So the label is report markup, and rendering it raw in the cockpit would show both a URL-ish ref in brackets and a command containing identifiers. CHOSEN: the CLIENT strips MARKUP AND IDENTIFIERS from the server's label and changes nothing else — a markdown link becomes its own link text, a trailing backticked command is dropped, and the result goes through `scrubUiText` from `humanCopy.ts`, which owns §17's forbidden-word list, as the final screen. The words that survive are the server's own, so DECISION F040 D5's equality between the digest's CTA and the report's recommendation is preserved; what is removed is exactly what the Markdown surface added. ALTERNATIVES CONSIDERED: (a) change `run_report.py` so the label carries no markup — rejected, the label is RIGHT for the report and for the CLI, where a copy-pasteable command is the useful artifact, and F040 may not degrade two shipped surfaces to suit a third; (b) have the client compose its own phrasing per `rule_id` — rejected, it is a second home for the CTA's wording and the digest could then drift from the report, which is the drift D2 spent a round preventing for the urgency formula; (c) render the label raw and accept the ids — rejected, §17 is binding and an id in a hero card is precisely the overclaiming-by-noise this feature exists to remove. HOW TO REVERSE: delete the copy module and render `label` directly; nothing else depends on it. WHAT IT COSTS TO BE WRONG: the card shows a slightly shorter sentence than the report does, and the in-page affordance that replaces the dropped command is what `rule_id` was kept for in the first place, per D5.
<<<END RECORD9

## SPEC for C3 — `apps/ui/src/api/digestCardCopy.ts`

Read `apps/ui/src/copy/humanCopy.ts` in full, then `apps/ui/src/api/jobDigest.ts`
for this feature's header voice. Open with the house header: what the module is,
and the DELIBERATE ABSENCES (no clock, no storage, no socket, nothing minted).

Export, each with a one-line WHY comment:

- `digestStateLabel(state: string): string` — the digest's own state vocabulary
  rendered for a human. It covers the SEVEN `RunState` values in
  `packages/core/models.py` and answers a safe phrase for anything else. Put a
  comment where a reader would reach for `humanCopy.stateLabel` saying why that
  one is wrong here: its vocabulary is the checklist's and it would answer
  "Planned" for every digest state.
- `digestCtaText(label: string): string` — the label with the REPORT'S MARKUP
  removed and nothing rewritten (constraint 11). It must, in this order:
  unwrap a markdown link `[text](ref)` to its `text`; drop a trailing backticked
  command together with the `: ` that introduces it, leaving the human sentence
  that precedes it; then hand the result to `scrubUiText` IMPORTED from
  `../copy/humanCopy` as the final §17 screen. A label with neither markup nor a
  command passes through unchanged except for that screen.
  DECIDE AND DOCUMENT the empty case: what a label that reduces to nothing
  becomes. `scrubUiText` already takes a fallback — use it rather than inventing
  a second one, and say in the comment which fallback you passed and why.
- `DIGEST_CTA_RULE_IDS` — the five `rule_id` values `recommended_next_action` can
  return, as a closed readonly tuple, with a comment naming the file and the
  function they come from. This is what lets the guard notice a sixth rule.

## SPEC for C4 — `apps/ui/src/api/digestCardCopy.test.ts`

Read `apps/ui/src/api/recency.test.ts` for conventions. Cover: all seven
`RunState` values through `digestStateLabel`, written as a table, plus an
unknown string; `digestCtaText` over each of the FIVE rules' real label shapes,
built from the shapes `run_report.py` actually emits and not invented ones —
including the `open-decision` label BOTH with and without a command, and the
`blocked-failed` label BOTH with and without an evidence ref, since each of
those two rules has two forms; and the assertion that matters most, that no
output of `digestCtaText` contains a backtick, a `[`, a `](` or a `td:` id.

## SPEC for C5 — `tests/ui_contracts/test_digest_card_copy.py`

Read `tests/ui_contracts/test_job_digest_card_contract.py` for the stripper and
positive-control conventions this repository now uses, and follow them; strip
comments and string literals before every absence assertion, and pair every zero
with a salted positive control.

Pin, over `apps/ui/src/api/digestCardCopy.ts`:

- THE PURITY: the forbidden capabilities occur zero times, each with a salted
  control.
- THE ONE SOURCE FOR THE §17 SCREEN: the module IMPORTS `scrubUiText` from
  `../copy/humanCopy`, and it does NOT restate that list — assert that no more
  than one of `humanCopy`'s forbidden words appears as a literal here, and that
  the module does not define its own array of them.
- `stateLabel` IS NOT IMPORTED from `humanCopy` — the wrong-vocabulary trap,
  asserted so a later edit cannot quietly reach for it.
- THE FIVE RULE IDS ARE ALL ACCOUNTED FOR, parsed from the SOURCE rather than
  retyped: read every `NextAction("<id>"` literal out of
  `packages/orchestration/run_report.py` and assert each id appears in
  `DIGEST_CTA_RULE_IDS`. A sixth rule added to the report reddens this test,
  which is the point — this is the same mechanism the seven-state assertion uses
  for `RunState`, and it is the reason that assertion was worth writing.
- THE SEVEN RUN STATES ARE ALL ACCOUNTED FOR in `digestStateLabel`, parsed from
  `packages/core/models.py` exactly as the sibling guard does.

## Done when — the gates

Report ONE line per gate with its REAL exit code. Every gate runs at a commit
STRICTLY EARLIER than C6.

G1 TRANSPORT, at C0b. One sha256 over `.remedy-wt/f040-r9-block.md`, the
   committed `.agent/authored/f040-r9.md` and `.agent/last_block.md`, with byte
   lengths, all three EQUAL. This block states no expected digest.

G2 THE PLAN, at C1. `.agent/plan.md` byte-EQUAL to PLAN9 (report both sha256),
   under 50 lines, holding `## Goal` and `## Next Steps`.

G3 THE RECORD APPEND, at C2. Re-measure the pre-commit length yourself; the
   reviewer read 1703971 at `b2cef8cb`. Base + one separator newline + RECORD9
   equals the committed length. TWO readings: (a) WHOLE RECONSTRUCTION; (b)
   PARAGRAPH ORDER, N COUNTED by your script. Report that the base bytes are a
   PREFIX. NEGATIVE CONTROL in a disposable worktree: flip one byte inside the
   FIRST appended paragraph, report that BOTH readings reject it and accept the
   unflipped bytes.

G4 THE LEDGER, at C2. Distinct `^- R-\d+ — ` ids with ADDED `[]` and REMOVED
   `[]` — this round registers NO finding, by design, and D10 explains why.
   Distinct `^Done: R-\d+` with ADDED `[]`. Distinct `DECISION F040 D\d+` with
   ADDED exactly `['D10']`. Exactly one `^Gate: F040 R8 — ` line. Report the open
   count, UNCHANGED at 262.

G5 THE MODULE'S SHAPE, at C3. Report the exported names by parsing; that
   `scrubUiText` is imported from `../copy/humanCopy` and `stateLabel` is NOT;
   the seven `RunState` values and the five `NextAction` rule ids your script
   PARSES from the Python sources, and that each appears where the SPEC requires;
   and the forbidden-capability sweep with a salted control per token.

G6 THE GUARD AND ITS RED PROOF, at C5. First
   `python3 -m pytest tests/ui_contracts/test_digest_card_copy.py -q` — REAL exit
   0 with the passed count. Then, INSIDE A DISPOSABLE WORKTREE, the UNMUTATED
   control FIRST, then FOUR mutations of `digestCardCopy.ts`, each reverted
   before the next: (a) a consumed `Date.now()`; (b) `scrubUiText`'s import
   removed and the call replaced by the raw string; (c) one rule id deleted from
   `DIGEST_CTA_RULE_IDS`; (d) one `RunState` value dropped from
   `digestStateLabel`. EACH must redden, and report WHICH tests died by node id,
   never only a count. BEFORE reporting any colour, prove each mutation REACHED
   THE CODE: show that the changed bytes are in a declaration and not in a
   comment — the R8 lesson, where a mutation landed in a header comment and the
   green that followed meant nothing. Restore, re-run, report the restored exit
   code and byte equality. Name the worktree, remove it, report `git worktree
   list` no longer holds it.

G7 VITEST AND THE TYPECHECK, at C5, through the pytest nodes and NOT a direct
   `npx` call:
   `python3 -m pytest "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" -q -rs`
   and `python3 -m pytest tests/ui_server/test_dashboard_contract.py -k typescript -q -rs`.
   Report the REAL exit code AND passed-or-SKIPPED for each; the reviewer
   measured 4 passed and 1 passed at the base, neither skipped. Per constraint 13
   no TypeScript colour is ordered.

G8 THE SUITES AND THE TREE, at C5. Each its own REAL exit code:
   `python3 -m pytest tests/ui_contracts/ -q`,
   `python3 -m pytest tests/ui_server/ -q`,
   `python3 -m pytest tests/docs/ -q`, and the canary
   `python3 -m pytest tests/cli/test_golden_path.py -q`. The reviewer measured
   735 passed with 4 skipped, 515, 295 and 42 at the base; `tests/ui_contracts/`
   MUST rise by the number of tests C5 adds — report both numbers and the
   difference. Then `git status --porcelain` EMPTY, `git ls-files --others
   --exclude-standard` count 0, and the per-commit insertion counts for C0a
   through C5, every one under 500.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: the state
block, the `## Commits` table with a `+/-` column from `git diff --numstat`, the
deviations, the item-status table with every bundle item and every gate
appearing exactly once, and the next steps. State `SESSION 2` of F040 and round
9. No length cap. Record that every DECIDABLE rule of the hero card is now built
and pinned and that NO card, NO mount and NO markup landed; name R-0570, R-0752
and R-0755 as OPEN and routed to paydown and R-0753 as OPEN and carried; and
name the next action as T002 part 5 — the `.tsx`, its mount, the trigger wiring
and the dismissal port bound at the edge, which is the first round of this
feature that cannot be red-proved and should be scoped accordingly.
