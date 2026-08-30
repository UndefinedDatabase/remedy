# STEP R7/F040 — T002 PART 2: WHEN THE HERO CARD APPEARS

Goal: the trigger. One pure rule deciding whether the digest shows, whether a
dismissal still holds and when new activity re-arms it — plus the DECISION that
rules WHERE a dismissal persists, which this feature has deliberately not
answered until now. Book the round 6 verdict.

Base: `3d609e02`, the round-6 handback commit and the tip of
`feature/f040-completion-digest`. Stay on that branch. Open no pull request.

THE ACCEPTANCE CLAUSES THIS ROUND ANSWERS, stated here because a T-slice is
complete against its acceptance text and never against a plan row — the
counter-measure finding R-0754 left behind, and this is its second exercise.
`docs/roadmap/features/T5_F040.md` Acceptance says "Dismissal persists; new
activity re-arms" and "Absence detection never claims more than last-seen truth
(copy audit: 'since you were last here' not 'while you slept')". Its trigger
rules at :68-71 say a terminal event while the UI is open shows the hero,
dismissible and remembered per job, and that a first open with activity since
last-seen shows the hero for the most significant job. THIS ROUND MEETS THE
RULE HALF of those clauses and NOT the copy half: the sentences are the card's
and the card is the next round. Say so in the handback rather than implying the
copy audit is discharged.

WHAT IS ALREADY MEASURED, so no gate rests on a guess. There is NO last-seen and
NO dismiss mechanism anywhere in `apps/ui/src/` — the reviewer swept the tree and
`localStorage` occurs exactly once in the whole client, as a COMMENT in
`decisionNonce.ts` saying there is none. This round is greenfield, and the house
answer to greenfield state is visible in two shipped files: `recency.ts` is a
pure function of two numbers whose header says it "never reads a clock itself",
and `AgentNowCard.tsx` binds the clock at the component edge in `useRecencyNowMs`
with the comment "The clock, bound HERE because this is the edge that has one."
The activity instant the rule needs already exists and is already the right one:
`FeedRow.receivedAtMs` is the host's own arrival stamp, and `feedRow.ts:9`
records that it is deliberately NOT the envelope's server-clock string.
`newestActionRow(recent)` in `actionClass.ts` returns the newest ACTION row with
bookkeeping excluded, which is the instant "new activity" means.

## Bundle, in commit order

- C0a save this block verbatim to `.agent/authored/f040-r7.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1  rewrite `.agent/plan.md` from slice PLAN7
- C2  append slice RECORD7 to `.agent/live_review.md`
- C3  add `apps/ui/src/api/digestVisibility.ts` per the SPEC below
- C4  create `apps/ui/src/api/digestVisibility.test.ts` per the SPEC below
- C5  APPEND a new class to
      `tests/ui_contracts/test_job_digest_card_contract.py` per the SPEC
- C6  rewrite `.agent/handoff.md` — the handback

## Change set — exactly these paths, nothing else

    .agent/authored/f040-r7.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    apps/ui/src/api/digestVisibility.ts
    apps/ui/src/api/digestVisibility.test.ts
    tests/ui_contracts/test_job_digest_card_contract.py
    .agent/handoff.md

`apps/ui/src/api/jobDigest.ts` is NOT edited — round 6 built it and the guard
pins it; the trigger is a separate concern and gets a separate module, the way
`recency.ts`, `actionClass.ts` and `feedFocus.ts` each own one. NO `.tsx` and NO
CSS this round. No Python production code changes.

## Constraints

1. Apply every slice BYTE FOR BYTE. If one looks wrong, apply it as given and
   DECLARE the problem in the handback's deviations.
2. C0a is a COPY: the block is at `.remedy-wt/f040-r7-block.md`. Use
   `shutil.copyfile` for C0a and again for C0b.
3. C1 is the FIRST substantive commit, ahead of the ledger append.
4. `.agent/live_review.md` is APPEND-ONLY.
5. `.agent/plan.md` stays under 50 lines.
6. Every exit code is REAL, from `subprocess.run(...).returncode` in a script
   under the gitignored `.remedy-wt/`. Never through a pipe.
7. Mutation and red-proof checks run ONLY in a disposable `git worktree`. As in
   round 6 the ONLY red proof is the PYTHON guard's; see constraint 15.
8. THE RULE READS NO CLOCK AND TOUCHES NO STORAGE. `digestVisibility.ts` takes
   `nowMs` as a parameter and takes the stored state as VALUES. It contains no
   `Date.now`, no `new Date`, no `localStorage`, no `sessionStorage`, no
   `fetch`, no `crypto` and no `XMLHttpRequest`. It DECLARES the storage port as
   a TypeScript type and IMPLEMENTS none: binding a port to real storage is the
   card's job, at the edge, exactly as `AgentNowCard.tsx` binds the clock.
9. THE RULE IS TOTAL AND NEVER THROWS. Every input combination answers, absences
   included; a missing stamp is a state, not an error.
10. NO PRESENTATION COPY, the round-6 rule extended to this module: no
    user-facing sentence, and in particular neither "since you were last here"
    nor "while you slept". The copy audit belongs to the card.
11. The `remedy` console script is DENIED to this session; use
    `python3 -m apps.cli.main ...` if needed and say so.
12. Commit subjects carry no leading-slash token, no absolute path, no
    secret-like string, and no `Co-Authored-By` trailer.
13. Push after C6. No pull request, no merge, no force-push.
14. C5 is an APPEND: the committed file's first bytes are EXACTLY the base
    file's bytes, and the new class follows. Nothing already in that file is
    edited, reordered or deleted — its strippers and its constants are REUSED by
    import within the same module, never copied.
15. NO TYPESCRIPT COLOUR IS ORDERED, for the reason DECISION F040 D7 records and
    the reviewer re-probed at this base: `npx vitest` is refused to this session
    class before execution, and `apps/ui/node_modules` is gitignored so it is
    absent from any disposable worktree, making a mutation there red for every
    possible module. Order none, and say in the handback that none was run.

## SANDBOX NOTES — read before writing a script

- Env-var assignment is DENIED in all three shell forms. Set it in-process with
  `os.environ[...]` or `monkeypatch.setenv`.
- `cp` is denied; copy with `shutil.copyfile`.
- `$(...)` inside a compound, `;`/`&&` chains and process substitution are
  rejected by FORM. One command per call, or a driver script run as a single
  `bash script.sh`, or `python3 - <<'PY'`.
- The Bash tool does not surface non-zero exits; capture
  `subprocess.run(...).returncode`.
- `npx vitest` and `npm run test:unit` are REFUSED. Reach vitest and tsc through
  the pytest nodes named in G7.

## Slices

The authored units are PLAN7 and RECORD7, each between its own BEGIN and END
marker line. The markers are NOT part of the unit; the newline ENDING the last
content line IS.

<<<BEGIN PLAN7
# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 2, round 7.

## Goal
Coming back is calm: a digest endpoint condenses state, cost with its basis, top
ownership entries, open decisions and ONE primary action into a hero card, shown
at job end or on the first UI open after absence — the "what happened while I
was gone" answer in one glance.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the F040 claim and the seam inventory | done | round 1, PASS |
| the spec decisions D2 to D7 | done | rounds 2, 3, 5 and 6 |
| T001 the composition, endpoint, goldens | done | rounds 3-5, all PASS |
| T002 the client digest seam and its guard | done | round 6, PASS |
| T002 the trigger, dismiss and last-seen rule | done | this round |
| T002 the hero card and its CSS conformance | open | next |
| T003 CLI parity and the end-to-end | open | |

## Next Steps
1. This round rules where a dismissal persists (DECISION F040 D8) and builds
   `digestVisibility.ts` as a pure total rule over injected values — no clock,
   no storage, no copy.
2. The next round builds the hero card itself: the `.tsx` that binds the clock
   and the storage port at the edge, the binding CSS from the feature file, the
   copy audit its Acceptance names, and the CSS conformance guard.
3. Then T003's `remedy job digest`, the end-to-end, the integration gate and
   closure.

## Risks
- R-0570 and R-0752 stay OPEN, routed to the paydown branch. R-0753 stays OPEN
  as this feature's documented risk: the persisted actuals record has no money
  field, so the digest's cost basis can only answer `absent` in production.
- The urgency formula still has two homes until the TypeScript copy is retired,
  pinned equal by `tests/ui_contracts/test_decision_urgency_parity.py`.
<<<END PLAN7

<<<BEGIN RECORD7
Gate: F040 R6 — T002 PART 1, THE CLIENT DIGEST SEAM. VERDICT PASS. Reviewed by re-running every gate in the reviewer's own driver; every figure reproduced. TRANSPORT is REAL at sha256 `274cd28a08ab7231cf84fbe606bfb2b089d32947f0c20acf60351cf16172d928` over 29186 bytes, equal on all three copies. THE PLAN is byte-equal to PLAN6 at 2052 bytes and 41 lines. THE RECORD APPEND reconstructs whole at 1678133 + 1 + 9267 = 1687401, N counted as 3, order holding, base a prefix. THE LEDGER moved exactly as a round that registers nothing should: registered ADDED `[]` and REMOVED `[]`, resolved ADDED `['R-0754']`, `DECISION F040` ADDED `['D7']`, one `^Gate: F040 R5 — ` line, and the open count FELL 262 to 261 — the first fall this feature has recorded. THE PAIR IS A TRUE REPLACEMENT, measured on both blobs: `PAIRACTUAL-FROM` occurs once in the base blob of `costMetric.ts` and ZERO times at HEAD, with the TO exactly once, so the export replaced the private const rather than shadowing it. THE SINGLE HOME HOLDS AND THE SWEEP IS AS WIDE AS THE CLAIM: over comment-stripped, non-test `.ts` sources under `apps/ui/src/api/` — THIRTY-FIVE files, counted, not asserted — the literal `"actual"` occurs exactly ONCE and it is in `costMetric.ts`; `jobDigest.ts` restates it zero times and imports `ACTUAL_BASIS` from `./costMetric`. The presentation copy stayed where it belongs: `jobDigest.ts` carries the phrase `, estimated` zero times and the `~` marker zero times, so the api layer decides the RULE and `TopMetricsBar.tsx` keeps the WORDS. THE PYTHON GUARD IS THE ROUND'S REAL GATE AND THE REVIEWER RED-PROVED IT IN ITS OWN WORKTREE, control first in all three cases, each mutation reverted before the next: a consumed `Date.now()` gave REAL exit 1 killing the purity assertion alone; the literal `"actual"` substituted for the imported constant gave REAL exit 1 killing BOTH one-source assertions; and copying the phrase `, estimated` down into the module gave REAL exit 1 killing `TestTheSeamWritesNoPresentationCopy::test_the_seam_contains_neither_the_phrase_nor_the_marker` — which matters because that assertion was added to the block LATE, after the reviewer's own dry run found the SPEC about to plant a second home for the copy, and an untested late addition is exactly the decoration this record has registered findings about before. Each restored run returned to 16 passed at REAL exit 0 with bytes identical to the original. THE GUARD IS HONEST ABOUT ITS OWN STRIPPING, which is the property that makes a text guard worth anything: it proves the comment stripper removes a promise the module really carries AND leaves the surrounding code intact, proves the literal blanker empties a real import specifier, and salts a copy of the source with each forbidden token in turn to prove the scan can SEE a capability when one is there — the vacuous-absence trap answered by construction rather than by assertion. VITEST AND THE TYPECHECK BOTH RAN AND BOTH PASSED RATHER THAN SKIPPED — 4 passed and 1 passed, REAL exit 0 each — and the reviewer confirmed the coverage claim statically rather than taking it: `apps/ui/vitest.config.ts` includes `src/**/*.test.ts`, which `src/api/jobDigest.test.ts` matches, and the node runs the whole suite asserting returncode 0, so a failing case in the new file reddens the node by construction. NO TYPESCRIPT COLOUR WAS RUN AND NONE WAS ORDERED, for the reason D7 states and the reviewer re-probed. FIVE SUITES all REAL exit 0 — `tests/ui_contracts/` 699 to 715, a rise of exactly the SIXTEEN tests C5 adds with the four pre-existing skips unmoved, plus 46, 515, 295 and the canary 42 — tree clean, zero untracked, eight commits at insertions 363, 272, 19, 6, 223, 157, 280 and 376, every one under 500. THE WORKER'S TEN DEVIATIONS WERE ALL CORRECTLY DECLARED and the sharpest was checked at its source: its `decodeJobDigest` accepts an EMPTY `job_id`, justified in the shipped docstring by the claim that `build_job_digest` really emits one. That claim is TRUE and the reviewer verified it rather than accepting it — `packages/orchestration/job_digest.py:142` is literally `str(getattr(job, "id", "") or "")` and :222 is `str(sources.job_id or "")`, both deliberately defending against a falsy id — so a justification that would have been a false statement in production source is instead an accurate one.

DECISION F040 D8 — A DISMISSAL PERSISTS IN THE BROWSER, BEHIND AN INJECTED PORT, AND THE RULE THAT READS IT NEVER REACHES FOR STORAGE. THE PROBLEM: `docs/roadmap/features/T5_F040.md` Acceptance requires "Dismissal persists; new activity re-arms" and its trigger rules require the hero be "dismissible, remembered per job", and F040 has carried that question unanswered since the claim. MEASURED by the reviewer at `3d609e02`: there is NO last-seen and NO dismiss mechanism anywhere under `apps/ui/src/`, and `localStorage` occurs exactly ONCE in the entire client — as a comment in `decisionNonce.ts` stating that module keeps none. So nothing is being extended here and the choice is genuinely open. CHOSEN: the dismissal and the last-seen instant persist in BROWSER-LOCAL storage, keyed per job, reached ONLY through a port that `digestVisibility.ts` declares as a TYPE and does not implement; the pure rule takes the stored values as arguments and answers a decision, and the card binds the port to real storage at the edge. This is not a new pattern but the repository's own, stated twice in shipped source: `recency.ts` is a pure function of two numbers whose header records that it "never reads a clock itself", and `AgentNowCard.tsx` binds the clock in `useRecencyNowMs` under the comment "The clock, bound HERE because this is the edge that has one." ALTERNATIVES CONSIDERED: (a) persist the dismissal SERVER-side so it follows the operator between browsers — rejected on scope and on posture, because the digest route is `read_only` and a write door in this repository is a deliberate, guarded construction (F009's command door and F033's approval door each cost their own feature), and F040 may not grow one as a side effect of a card; (b) keep the dismissal in React state only — rejected outright, it does not survive a reload and the Acceptance word is "persists"; (c) put the storage call directly in `digestVisibility.ts` — rejected because it would make the rule untestable without faking a global, and no test under `apps/ui/src` patches one today, which is a property worth keeping. WHAT THE CHOICE HONESTLY COSTS, stated because the Acceptance copy audit is about not overclaiming: a browser-local dismissal is per-browser and per-profile, so the same operator on a second machine sees the hero again. That is a real limit and the card's copy may not imply otherwise — "since you were last here" is already the honest phrasing for a client-side last-seen, and it is the phrasing the feature file requires. HOW TO REVERSE: the port is one type; a server-backed implementation binds the same port when a write door exists, and the rule does not change.
<<<END RECORD7

## SPEC for C3 — `apps/ui/src/api/digestVisibility.ts`

Read `apps/ui/src/api/recency.ts` end to end first — it is the closest relative
and this module is written in its voice — then
`apps/ui/src/components/panels/AgentNowCard.tsx:14-40` for how the edge binds a
clock, and `apps/ui/src/api/jobDigest.ts` for the header shape this feature now
uses. Follow all three.

Open with the house header: what the module is, and the DELIBERATE ABSENCES
written where a reader will search for them — no clock, no storage, no socket,
no copy — naming `Date.now`, `localStorage` and `fetch` in the prose so a reader
grepping for them finds the explanation.

Export, each with a one-line WHY comment above it:

- `DigestDismissal` — the per-job remembered state: the instant a dismissal was
  made, or `null` for never dismissed. Keep it a named type even though it is
  small; a bare `number | null` at three call sites is the kind of argument
  DECISION F040 D2's own reasoning objects to.
- `DigestVisibilityPort` — the STORAGE PORT AS A TYPE ONLY, with the two
  operations the card will bind: read the remembered dismissal for a job, and
  write one. DECLARE it; implement nothing. State in its comment that the
  implementation is bound at the edge per DECISION F040 D8, and that a module
  that reached for `localStorage` here could not be tested without faking a
  global.
- `DigestVisibility` — what the rule answers: whether to show, and a `reason`
  from a SMALL CLOSED SET of string literals naming WHY. A closed union, not a
  free string: the card will branch on it and a typo must be a type error.
  Cover at least — the run reached a terminal state; there is activity since
  last-seen; a dismissal is still in force; there is nothing new to report.
- `digestVisibility(input): DigestVisibility` — the rule, TOTAL and pure, taking
  a single named-argument object holding: the decoded `JobDigest` (or `null`
  when none has loaded), `lastSeenMs`, `dismissedAtMs`, `latestActivityMs` and
  `nowMs`, every instant `number | null` where absence is meaningful.

THE RULE ITSELF, and these are the propositions the tests pin:

- A dismissal HOLDS until something newer than it happens: if `dismissedAtMs` is
  set and `latestActivityMs` is not strictly greater, the answer is not to show.
  NEW ACTIVITY RE-ARMS — activity strictly after the dismissal shows the card
  again, which is the Acceptance clause in one comparison.
- A SETTLED run shows the card when no dismissal is in force, and the partition
  is over the WHOLE state vocabulary rather than over the four the goldens
  happen to exercise. `packages/core/models.py:38-47` defines `RunState` with
  SEVEN values and the digest carries the value string: `pending`, `planned`,
  `running`, `paused`, `completed`, `failed`, `cancelled`. The goldens cover
  only `completed`, `paused` and `running`, so do NOT derive the rule from them.
  THE PARTITION IS THREE-WAY, not two-way, and getting it wrong in either
  direction is a real defect: `pending` and `planned` are NOT-YET-STARTED and
  must NOT show — nothing happened while the operator was away, and a hero card
  announcing a job that has not begun is the overclaiming the Acceptance's copy
  audit exists to prevent; `running` is IN FLIGHT and does not show on settled
  grounds; and `paused`, `completed`, `failed` and `cancelled` are SETTLED and
  do show. Treating "terminal" as merely "not running" collapses the first group
  into the third and is the specific mistake to avoid. An UNKNOWN state string —
  one this client has never heard of — does NOT show on settled grounds, because
  claiming a run finished on the strength of a word you cannot read is exactly
  the false claim this feature refuses elsewhere; say so in a comment.
- ABSENCE: with no dismissal, activity strictly after `lastSeenMs` shows the
  card. A `lastSeenMs` of `null` means never seen, which SHOWS on any activity.
- NOTHING NEW answers not-to-show, and it is the default rather than a fallback
  a reader has to infer.
- A `null` digest never shows, whatever the instants say.
- CLOCK SKEW IS ANSWERED DELIBERATELY, the way `recency.ts` answers it at its
  own comment: state in a comment what a stamp in the future means here and why
  the choice is the honest one. `nowMs` is taken so the rule is total and
  testable; if the rule does not in fact need it for any branch you write, say
  so in the handback rather than adding a use to justify the parameter.

## SPEC for C4 — `apps/ui/src/api/digestVisibility.test.ts`

Read `apps/ui/src/api/recency.test.ts` and follow its conventions. Cover every
proposition above, each as its own named case, plus the boundaries: activity
EQUAL to the dismissal instant (not newer, so the dismissal holds), activity
equal to `lastSeenMs`, a `null` `lastSeenMs`, a `null` digest, and a future
stamp. Assert the `reason` as well as the boolean — a rule that shows for the
wrong reason is a rule the card will branch on wrongly.

COVER ALL SEVEN `RunState` VALUES BY NAME, and an UNKNOWN state string besides.
Write the seven as a table in the test so a state added to `RunState` later has
an obvious place to land, and assert explicitly that `pending` and `planned` do
NOT show: that pair is the whole point of the three-way partition, and a rule
written two-way passes every other case in this file.

## SPEC for C5 — appending to the guard

APPEND one new class to `tests/ui_contracts/test_job_digest_card_contract.py`,
per constraint 14, REUSING that module's existing strippers, its
`FORBIDDEN_CAPABILITIES` tuple and its positive-control habit rather than
copying any of them. Add a module-level `Path` for the new file beside the
existing ones. Pin, over `apps/ui/src/api/digestVisibility.ts`:

- THE PURITY, over comment- and literal-stripped source: every token in
  `FORBIDDEN_CAPABILITIES` occurs ZERO times, with the same salted positive
  control the existing class uses so a zero is not a blind search.
- THE PORT IS A TYPE AND NOTHING MORE: the module declares
  `DigestVisibilityPort` and contains NO implementation of it — no object
  literal assigned to it, no class, no function returning one. Choose a
  mechanism that reads the CODE rather than the prose and say in the test's
  docstring what the mechanism can and cannot see.
- NO PRESENTATION COPY: neither "since you were last here" nor "while you slept"
  nor any other user-facing sentence appears. Assert the two audited phrases by
  name, since the Acceptance names them.
- THE REASON SET IS CLOSED: the exported reason type is a union of string
  literals rather than `string`.
- THE SEVEN STATES ARE ALL ACCOUNTED FOR: read the `RunState` members out of
  `packages/core/models.py` at test time — parse them, do not retype them — and
  assert every value string appears in `digestVisibility.ts`. This is the
  assertion that makes the three-way partition a pinned property rather than a
  paragraph, and it fails LOUDLY the day someone adds a state to the enum, which
  is exactly when this module needs to be revisited.

## Done when — the gates

Report ONE line per gate with its REAL exit code. Every gate runs at a commit
STRICTLY EARLIER than C6, which writes the handback.

G1 TRANSPORT, at C0b. One sha256 over three files — `.remedy-wt/f040-r7-block.md`,
   the committed `.agent/authored/f040-r7.md` and `.agent/last_block.md` — with
   the byte length, all three EQUAL. This block states no expected digest.

G2 THE PLAN, at C1. `.agent/plan.md` byte-EQUAL to PLAN7 (report both sha256),
   under 50 lines, holding `## Goal` and `## Next Steps`.

G3 THE RECORD APPEND, at C2. Re-measure the pre-commit length yourself; the
   reviewer read 1687401 at `3d609e02`. Base + one separator newline + RECORD7
   equals the committed length. TWO readings: (a) WHOLE RECONSTRUCTION against
   the entire committed file; (b) PARAGRAPH ORDER — the last N blank-line units
   equal RECORD7's N paragraphs IN ORDER, N COUNTED by your script. Report that
   the base bytes are a PREFIX. NEGATIVE CONTROL in a disposable worktree: flip
   one byte inside the FIRST appended paragraph and report that BOTH readings
   reject it and accept the unflipped bytes.

G4 THE LEDGER, at C2. Distinct `^- R-\d+ — ` ids with ADDED `[]` and REMOVED
   `[]`; distinct `^Done: R-\d+` with ADDED `[]`; distinct
   `DECISION F040 D\d+` with ADDED exactly `['D8']`; exactly one
   `^Gate: F040 R6 — ` line. Report the open count, which should be UNCHANGED at
   261 — this round neither registers nor resolves a finding.

G5 THE RULE'S SHAPE, at C3. Over `apps/ui/src/api/digestVisibility.ts`: report
   the exported names your script finds by parsing rather than by eye; that
   `DigestVisibilityPort` is declared; and, over comment- and literal-stripped
   source, that each of `Date.now`, `new Date`, `localStorage`, `sessionStorage`,
   `fetch`, `crypto` and `XMLHttpRequest` occurs ZERO times, each paired with a
   salted positive control proving the scan can see it.

   THE SEVEN-STATE READING, which the guard also asserts as a test so it is
   pinned and not merely reported here: every one of the seven `RunState` values
   — `pending`, `planned`, `running`, `paused`, `completed`, `failed`,
   `cancelled` — occurs in `digestVisibility.ts`, and the list is read FROM
   `packages/core/models.py` at test time rather than retyped, so a state added
   to the enum makes the guard fail until this module accounts for it. Report
   the seven names your script actually found.

   Then confirm `apps/ui/src/api/jobDigest.ts` is byte-IDENTICAL to its base
   blob — this round does not touch it.

G6 THE GUARD, ITS APPEND AND ITS RED PROOF, at C5. First report that the
   committed `test_job_digest_card_contract.py` has the base file's bytes as a
   PREFIX and that the base's own test count still passes. Then
   `python3 -m pytest tests/ui_contracts/test_job_digest_card_contract.py -q` —
   REAL exit 0 with the passed count and the rise from 16. Then, INSIDE A
   DISPOSABLE WORKTREE, the UNMUTATED control FIRST, then THREE mutations of
   `digestVisibility.ts`, each reverted before the next: (a) a consumed
   `Date.now()` — the purity assertion must die; (b) a real implementation
   assigned to the port — the port-is-a-type assertion must die; (c) the phrase
   `since you were last here` placed in the module — the no-copy assertion must
   die. Report each REAL exit code and WHICH tests died by node id, never only a
   count. Restore, re-run, report the restored exit code and byte equality. Name
   the worktree, remove it, report `git worktree list` no longer holds it.

   THEN A FOURTH MUTATION, in the SAME worktree and still against the PYTHON
   guard, because it is the only red proof available here: DELETE the string
   `pending` from `digestVisibility.ts`'s state handling — the seven-state
   assertion G5 orders must die. Report the control first and the mutated REAL
   exit code with the node ids that died.

   Note for honesty rather than for work: the vitest cases that pin the
   PARTITION ITSELF get no colour this round, and no attempt to give them one is
   ordered. Running the vitest node with its cwd in a worktree fails at startup
   for want of `node_modules` — red for every possible mutation, the vacuous
   probe R-0703 records — and running it in the primary checkout would test the
   primary's unmutated files, so neither spelling proves anything. The partition
   is therefore pinned STATICALLY by G5's seven-state reading, which IS
   red-proved above, and dynamically only by the suite being green. Say exactly
   that in the handback; do not describe the vitest suite as red-proved.

G7 VITEST AND THE TYPECHECK, at C5, through the pytest nodes and NOT a direct
   `npx` call:
   `python3 -m pytest "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" -q -rs`
   and `python3 -m pytest tests/ui_server/test_dashboard_contract.py -k typescript -q -rs`.
   For EACH report the REAL exit code AND whether it PASSED or SKIPPED — a skip
   is not a type check. The reviewer measured 4 passed and 1 passed at the base,
   neither skipped. Per constraint 15, no TypeScript colour is ordered.

G8 THE SUITES AND THE TREE, at C5. Each its own REAL exit code:
   `python3 -m pytest tests/ui_contracts/ -q`,
   `python3 -m pytest tests/orchestration/test_job_digest.py -q`,
   `python3 -m pytest tests/ui_server/ -q`,
   `python3 -m pytest tests/docs/ -q`, and the canary
   `python3 -m pytest tests/cli/test_golden_path.py -q`. The reviewer measured
   715 passed with 4 skipped, 46, 515, 295 and 42 at the base;
   `tests/ui_contracts/` MUST rise by the number of tests C5 adds, so report both
   numbers and the difference. Then `git status --porcelain` EMPTY,
   `git ls-files --others --exclude-standard` count 0, and the per-commit
   insertion counts for C0a through C5, every one under 500.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: the state
block, the `## Commits` table with a `+/-` column from `git diff --numstat`, the
deviations, the item-status table with every bundle item and every gate
appearing exactly once, and the next steps. State `SESSION 2` of F040 and round
7. No length cap. Record that T002's RULE half is complete and that the COPY
half — the Acceptance's "since you were last here" audit — is NOT discharged by
this round because the sentences belong to the card. Name R-0570, R-0752 and
R-0753 as OPEN, and name the next action as T002 part 3: the hero card `.tsx`,
its binding CSS, the copy audit and the CSS conformance guard.
