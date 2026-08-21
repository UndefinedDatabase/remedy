── STEP R4/4 — F009 The single write channel ────────────────────────
Goal:        Persist finding R-0631 against the reviewer's own R3 gate design,
             record the R3 verdict, and set the plan so the NEXT session opens
             directly on T001's build. This is the last round of this session,
             which ends at its stated four-round cap with a written handoff.
             No production code is written and no test file is created.

Bundle:      C0a save the block · C0b mirror the block · C1 the plan ·
             C2 the finding, in its own commit · C3 the R3 verdict ·
             C4 the handback.

Change set:  `.agent/authored/f009-r4.md`, `.agent/last_block.md`,
             `.agent/plan.md`, `.agent/live_review.md`, `.agent/handoff.md`.
             Nothing else. No path under `packages/`, `apps/`, `tests/` or
             `docs/` is edited this round.

## Step 0 — before any commit
    ls -la .agent/STOP
    git rev-parse --abbrev-ref HEAD
    git status --porcelain
    git rev-parse HEAD

`.agent/STOP` MUST be absent; if it exists, stop, write the handoff and end. The
branch MUST already be `feature/f009-single-write-channel`. Do NOT run an Open PR
Gate and do NOT create a pull request. The SHA `git rev-parse HEAD` prints is the
ROUND BASE — it is `8b3591dd` unless something has moved; report what you read.

## Transport
This block lives at `.remedy-wt/f009-r4.md`. Its sha256, byte count and line
count are stated in the task prompt that handed you that path. Verify it BEFORE
using any byte of it. Save it byte for byte as `.agent/authored/f009-r4.md`
(C0a), then mirror it to `.agent/last_block.md` (C0b) FROM THE COMMITTED C0a
BLOB — `git show <C0a>:.agent/authored/f009-r4.md` — never from this file again.

## Slice convention
The authored units below are delimited by one-line markers, `<<<SLICE <NAME>`
opening and `<<<END <NAME>` closing. Extract every slice from the COMMITTED C0a
BLOB by its marker lines with a script. The marker lines are NOT part of any
slice. Every slice is newline-terminated, none begins with a blank line, and none
carries trailing whitespace on any line — report those three readings.

## C1 — the plan, the first substantive commit
This round registers a finding, so `.agent/plan.md` advances first (checklist
item 23). Apply PLANF009R4 as the WHOLE file.

<<<SLICE PLANF009R4
# Plan — F009 The single write channel

Branch: feature/f009-single-write-channel, cut from `main` at `ce49348b`, the
merge commit of pull request #209. `.agent/live_review.md` is the source of truth
for the open set, the round map and the finding-id ceiling, which is derived with
`max` over its line-anchored entries.

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
R4 registers R-0631 against the reviewer's own R3 gate design and records the R3
verdict. It writes no code: this session ends here at its stated four-round cap,
and the build opens the next one with DECISIONS F009 D1 through D9 already ruled.

## Next Steps
1. R5 lands T001's door: the POST route on `_RemedyHandler` dispatching
   `/api/jobs/<job_id>/commands`, the bearer plus X-Remedy-CSRF pair D2 rules,
   the request-shape validation with typed errors naming the offending field,
   and BOTH halves of D3's constant-time comparison in one commit — the existing
   GET check at the `token != self.server_token` line and the new POST check —
   compared as BYTES rather than as str, because `secrets.compare_digest` raises
   TypeError on a non-ASCII str and a query parameter is attacker-controlled.
   `import secrets` is already present, so D3 adds no import. Contract tests go
   in `tests/ui_server/test_command_channel.py` per D1.
2. R6 the catalog subset D4 rules and the rate limit D9 rules as a typed
   `ConfigKeySpec`; R7 the nonce store and audit record per D6, D7 and D8.
3. T003's effect table per D5, the plan-approval extraction landing as its own
   commit; then the integration gate, then closure.

## Risks
- R5 is the first round to touch `packages/orchestration/ui_server.py` on this
  branch and it changes a live authentication line. It is a SPLIT round, the
  `tests/ui_server/` suite gates it, and `tests/ui_server/test_live_state.py`
  already asserts the `invalid token` response the change must preserve.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which is
  R-0622 and routes to a paydown branch.
<<<END PLANF009R4

## C2 — the finding, in its own commit
Append R0631 to `.agent/live_review.md` as the LAST paragraph, separated from the
current last paragraph by exactly one blank line. Read the base bytes with
`git show <round base>:.agent/live_review.md` into `.remedy-wt/` scratch; never
write a base blob over the tracked file. Findings persist in their own commit
BEFORE the verdict that reports them, so nothing is lost if a session dies
(docs/agents/planner_reviewer_prompt.md §4 item 4).

<<<SLICE R0631
- R-0631 — Low — A TWO-READER APPEND GATE WHOSE SECOND READER COVERED ONE PARAGRAPH OF FIFTY-ONE, SO ITS NEGATIVE CONTROL COULD ONLY EVER PROBE THE TAIL. The defect is the reviewer's, in the R3 block, and it was FOUND AND DECLARED BY THE WORKER as deviation 2 of that round rather than by any gate. G7 ordered the `.agent/decisions.md` append proved "TWICE over independent extractors": (a) the base blob is a byte-exact prefix and the remainder equals a newline plus DECISIONS, and (b) "an INDEPENDENT blank-line split of the whole C3 file ends in DECISIONS' last paragraph". Reading (b) is a TOTAL check when the appended slice is ONE paragraph, which is the shape every previous round used it in — LEDGER2 and LEDGER3 are single paragraphs and G5 has been sound every time. DECISIONS is 51 paragraphs, and against a multi-paragraph append the same sentence degenerates to a check of the LAST one. MEASURED by the reviewer at `f19abdfb` after the round: with one printable byte flipped in the FIRST appended paragraph, reader (a) REJECTS, a tail comparison of the last 51 units against the slice's 51 paragraphs REJECTS, and reader (b) AS WORDED ACCEPTS — so the independence the gate claimed covered one paragraph in fifty-one. THE OPEN SET WAS SEARCHED FOR THE DEFECT BEFORE THIS ID WAS MINTED (§3 item 30), and R-0573 is the entry that comes closest: it registers a transport gate that re-used the very extractor it was meant to check, and its counter-measure requires an equality gate to name an extraction INDEPENDENT of the one that produced the text and to carry a NEGATIVE CONTROL. That clause was FOLLOWED here and did not prevent this: extractor (b) genuinely is independent of extractor (a), and a negative control genuinely was ordered. What R-0573 does not say is that the control must be placed where the weaker reader is weakest, or equivalently that the second reader's COVERAGE must equal the appended region rather than merely touch it. Different fix, so a separate id, on the precedent by which R-0572 and R-0573 were themselves registered separately. WHY LOW AND NOT MEDIUM: reader (a) is a total byte comparison of the whole appended region against the authored slice, it was ordered in the same gate, and it rejected every mutation — so the append WAS fully proved and nothing false landed. The cost is that the gate's second half certified less than its own sentence claimed, which is the vacuous-gate family arriving through SCOPE rather than through a missing path or a re-used method. THE WORKER'S CONDUCT IS WHY THIS COST NOTHING: it noticed that a first-paragraph flip passed reading (b), said so in a declared deviation, ran the stronger 51-unit tail comparison as well, reported BOTH measurements, and placed the control where both readers reject rather than quietly choosing whichever produced a green — and it did not re-run anything to obtain a colour. THE FIX, binding on the next block that orders a multi-paragraph append: reading (b) compares the LAST N blank-line units of the whole file against the slice's N paragraphs IN ORDER, where N is a value the script counts rather than the block asserts, and the negative control is applied to the FIRST appended paragraph, because that is the position the tail-only reading cannot see. A single-paragraph append is the N=1 case of the same sentence, so one wording covers both and no block has to decide which shape it is holding. OPEN.
<<<END R0631

## C3 — the R3 verdict
Append LEDGER4 to `.agent/live_review.md` as the LAST paragraph, one blank line
after R0631. Same base-read rule; the base for THIS append is the C2 blob.

<<<SLICE LEDGER4
Gate: R4 — the R3 entry. R3 PASSED. Its nine DECISIONS, its ledger append, its decisions append, its feature-file amendment and its context rewrite all landed byte-exact, every gate reproduced when the reviewer re-derived it from the committed blobs, and the ONE defect the round surfaced is the reviewer's own and is registered directly above as R-0631. TRANSPORT HELD THREE WAYS INCLUDING THE REVIEWER'S OWN COPY: `.remedy-wt/f009-r3.md` as emitted, `.agent/authored/f009-r3.md` at `87e1e8bf` and `.agent/last_block.md` at `7aabbd33` are all sha256 4bb755d088a35f4a466efd3c563b14dcab1518130c7b249770147648c80ada76 over 35658 bytes and 390 lines. THE LEDGER APPEND at `d836b061` is a byte-exact prefix plus a 5448-byte remainder equal to a newline plus the reviewer's OWN LEDGER3 slice, agreed by an independent 204-unit blank-line split whose last unit is that paragraph. THE DECISIONS APPEND at `f19abdfb` is the same prefix-plus-remainder shape over 12970 bytes, and `^## DECISION F009 D\d+ — ` goes 0 to 9 over the DISTINCT keys D1 through D9 while `^## DECISION ` goes 85 to 94 — the round REPORTED both totals rather than predicting them, which is what the gate asked for and the reason no arithmetic could be wrong. THE AMENDMENT at `215e4ba0` is a one-pass substitution: FEATFROM 1 then 0, FEATTO 0 then 1, and the base blob with that single substitution BYTE-EQUAL to the C4 blob, which is also the proof no other line of that feature file moved; 90 lines became 92, and `tests/ui_contract/` reads 1 at BOTH commits because the replacement text deliberately QUOTES the retired path while explaining the amendment — the gate ordered that count REPORTED rather than driven to zero, which is the item-2 trap avoided rather than merely survived. THE SETS HELD: `^- R-\d+ — ` 196 with 196 DISTINCT ids at the base and at C2, `^Done: R-\d+ — ` 1, `^Landed: ` 0, `^- R-0630 — ` 1 and `^> Next free id` 0 at both, `^Gate: R\d+ — ` 2 then 3 over 3 DISTINCT keys, and of the three headers exactly two match the n-minus-one shape while the single non-match reads `Gate: R1 — the F008 R36 entry.` THE SUITES ARE THE REVIEWER'S OWN, serial, in the primary checkout: `tests/docs/` EXITS 0 at 295 passed, `tests/orchestration/test_roadmap_index.py` EXITS 0 at 30, the state-reader group EXITS 0 at 423 and the canary EXITS 0 at 42, reproducing all four of the worker's numbers. THE RANGE HOLDS: the path set is EXACTLY the eight declared paths, seven single-parent commits before the handback with insertions 390, 319, 24, 2, 102, 3 and 26 — every one under the 500 cap — each equal to the `## Commits` column, 0 marker lines in all five committed targets, `amend`, `rebase` and `cherry` each 0, `git ls-files .remedy-wt` 0, a clean tree, `git worktree list` naming the primary checkout alone, and an 81-line handback under the 100 its eight commits allow. THE ROUND ALSO SAID THE HARDER TRUE THING WHERE A SOFTER ONE WAS AVAILABLE: G10 ordered the docs suite because C4 edits a path under `docs/roadmap/`, and the handback states plainly that NEITHER `tests/docs/` nor the roadmap-index module asserts anything about a feature file's BODY — the first deriving ids from FILENAMES and reading bodies only of three T0 files, the second parsing only each file's title and dependency lines while the amendment sits below them — so G8's byte proof rather than either suite is what establishes the amendment landed. A green suite reported as if it had verified the change would have been the easy sentence and a false one. TWO FURTHER DECLARATIONS WERE CORRECT AND ARE NOT FINDINGS: the round took ONE `.agent/STOP` reading at Step 0 rather than the two G1's wording implies, and it was right that no commit intervened between that reading and C0a, so the property G1 exists to establish held; and it pushed once more after the handback commit, which AGENTS.md's push discipline requires and which no handback can ever record because it follows the file being written. WHAT THIS ROUND SETTLES BEYOND ITS OWN CHANGE SET is that the design of this feature is now decided rather than assumed: the auth pair is ruled against a real constraint — the cockpit's `EventSource` cannot set headers, so the stream's query token is not a legacy accident — the exposed subset is two catalog ids rather than the three the feature file's prose implies, because plan approval has no id of its own, and the audit record's fields are fixed now because two later features already plan to read them.
<<<END LEDGER4

## Constraints
1. Apply every slice BYTE FOR BYTE out of the committed C0a blob. Do not retype,
   rewrap, reflow, reindent or whitespace-adjust any of them. If a slice looks
   wrong to you, apply it as written and record the objection in the handback
   under "Deviations & assumptions" — an objection is recorded, never acted on.
2. The commit order is C0a, C0b, C1, C2, C3, C4 and nothing comes between them.
   C1 is the first substantive commit and C2 precedes C3.
3. The change set is the five paths named above. Write no code, create no test
   file, and touch nothing under `packages/`, `apps/`, `tests/` or `docs/`.
4. `.remedy-wt/` is gitignored scratch. Every multi-step gate goes into a script
   there; `git status --porcelain` prints 0 lines after each commit.
5. Push with `git push` after C4, which is the last commit of this session.

## Done when
- G1 `.agent/STOP` ABSENT, read at Step 0. `git rev-parse --abbrev-ref HEAD`
  prints `feature/f009-single-write-channel` at every reading. `git status
  --porcelain` prints 0 lines after each of C0a through C4. Report the round base
  SHA from Step 0.
- G2 Transport EQUAL: `.remedy-wt/f009-r4.md` as received, `.agent/authored/
  f009-r4.md` at C0a and `.agent/last_block.md` at C0b all carry the same sha256,
  byte count and line count, equal to the digest in the task prompt.
- G3 Report, per slice, the newline-included sha256, byte count and line count,
  the COUNT of slices from your own ordered extraction out of the committed C0a
  blob, and the three aggregate readings: any trailing whitespace, any leading
  blank line, all newline-terminated.
- G4 `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R4; report its line count
  against the 50-line cap; `Steps` occurs; `^## Goal$` and `^## Next Steps$` each
  match exactly 1 line; the first `\bF\d{3}\b` match is `F009`.
- G5 The append at C2, proved TWICE over independent extractors, in the shape
  R-0631's own fix clause prescribes — this round is the first to owe it. (a) The
  round-base blob is a byte-exact PREFIX of the C2 blob and the remainder EQUALS
  a newline plus R0631; report its sha256, bytes and lines. (b) Let N be the
  number of blank-line paragraphs in the R0631 slice, COUNTED by your script and
  reported, not assumed: the LAST N blank-line units of the whole C2 file, its
  terminating newline normalised first, equal the slice's N paragraphs IN ORDER.
  NEGATIVE CONTROL applied to the FIRST appended paragraph: flip ONE printable
  ASCII byte there and confirm BOTH readings REJECT it while both ACCEPT the
  unflipped value; report all four outcomes.
- G6 The append at C3, with the C2 blob as its base, proved the same two ways and
  with its own negative control on the first appended paragraph; report the same
  values. Report N for this slice too, counted the same way.
- G7 At the round base, at C2 and at C3, line-anchored: `^- R-\d+ — ` 196, 197
  and 197 with all ids DISTINCT at each; `^- R-0631 — ` 0, 1 and 1;
  `^Done: R-\d+ — ` 1 at all three; `^Landed: ` 0 at all three; `^> Next free id`
  0 at all three; `^Gate: R\d+ — ` 3, 3 and 4 over that many DISTINCT keys.
  Report the max id the file carries at C3. Of the `Gate: ` lines at C3, report
  how many match `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one
  less than the first, and quote to its first period any that does not — the
  expected reading is three matches and one non-match reading `Gate: R1 — the
  F008 R36 entry.`
- G8 The range from the round base to C3: `git diff --name-only` lists EXACTLY
  the four paths of the change set other than `.agent/handoff.md`, the set
  difference empty in both directions. Walk `git rev-list --reverse` and report,
  per commit, that it has ONE parent and its `git show --numstat` insertions,
  with `git diff --numstat` AGREEING on every cell and every cell equal to the
  `+/-` column of your `## Commits` table. `^<<<SLICE ` and `^<<<END ` read 0
  lines in `.agent/plan.md` and `.agent/live_review.md` at C3. Classify this
  round's own reflog entries by the operation before the first `:` in `%gs` and
  report `amend`, `rebase` and `cherry`, which must each be 0; assert no total
  over the whole reflog (R-0601). Report `git ls-files .remedy-wt` as a count.
- G9 The handback carries every mandated section of
  docs/agents/handback_template.md, an item-status table holding exactly one row
  for each of C0a, C0b, C1, C2, C3 and C4, the round base SHA, and one line per
  gate — raw transcripts belong in the round report (R-0582). Report its line
  count against the 60 AGENTS.md sets, or carry a DECISION D15 stated-cause line.
  Its `## Next` section states, in this order: that this session ended at its
  stated four-round cap with no `.agent/STOP` present; that the next session's
  FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1) and its SECOND the
  Open PR Gate (Phase 1 rule 2), which is EMPTY because this branch carries no
  pull request and F009 opens one at its closure; that the next free finding id
  is derived with `max` over the line-anchored entries rather than read from a
  header; that `.agent/candidates.md` is EMPTY; and that R5 is the T001 door as
  `.agent/plan.md` describes it.

Handback:    completion report + rewrite `.agent/handoff.md`. The state block
             repeats this Fortschritt line verbatim: 10 % (T001 offen · T002
             offen · T003 offen — beansprucht, vermessen, entschieden; der Bau
             beginnt in R5 mit D1 bis D9 als Vorgabe) — Schätzung
──────────────────────────────────────────────────────────────
