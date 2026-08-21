── STEP R5/5 — F009 The single write channel ────────────────────────
Goal:        Close the session honestly. Register R-0632 — this repository has no
             agreed derivation for its own open-finding count, and the R4
             handback states one that the only written rule contradicts — rule
             that derivation as DECISION F009 D10, record the R4 verdict, and
             rewrite the handback with the number its own stated rule produces.
             No production code. This round is DECLARED as exceeding the
             four-round cap this session announced; the reason is in the plan.

Bundle:      C0a save the block · C0b mirror the block · C1 the plan ·
             C2 the finding, in its own commit · C3 the ruling ·
             C4 the R4 verdict · C5 the handback.

Change set:  `.agent/authored/f009-r5.md`, `.agent/last_block.md`,
             `.agent/plan.md`, `.agent/live_review.md`, `.agent/decisions.md`,
             `.agent/handoff.md`. Nothing else. No path under `packages/`,
             `apps/`, `tests/` or `docs/` is edited this round.

## Step 0 — before any commit
    ls -la .agent/STOP
    git rev-parse --abbrev-ref HEAD
    git status --porcelain
    git rev-parse HEAD

`.agent/STOP` MUST be absent; if it exists, stop, write the handoff and end. The
branch MUST already be `feature/f009-single-write-channel`. Do NOT run an Open PR
Gate and do NOT create a pull request. The SHA `git rev-parse HEAD` prints is the
ROUND BASE — it is `ab6eeba1` unless something has moved; report what you read.

## Transport
This block lives at `.remedy-wt/f009-r5.md`. Its sha256, byte count and line
count are stated in the task prompt that handed you that path. Verify it BEFORE
using any byte of it. Save it byte for byte as `.agent/authored/f009-r5.md`
(C0a), then mirror it to `.agent/last_block.md` (C0b) FROM THE COMMITTED C0a
BLOB — `git show <C0a>:.agent/authored/f009-r5.md` — never from this file again.

## Slice convention
The authored units below are delimited by one-line markers, `<<<SLICE <NAME>`
opening and `<<<END <NAME>` closing. Extract every slice from the COMMITTED C0a
BLOB by its marker lines with a script. The marker lines are NOT part of any
slice. Every slice is newline-terminated, none begins with a blank line, and none
carries trailing whitespace on any line — report those three readings.

## C1 — the plan, the first substantive commit
This round registers a finding, so `.agent/plan.md` advances first (item 23).

<<<SLICE PLANF009R5
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
R5 closes this session. It registers R-0632, rules the open-count derivation as
DECISION F009 D10, records the R4 verdict, and rewrites the handback with the
number D10's rule produces. IT IS DECLARED AS A FIFTH ROUND AGAINST A STATED
FOUR-ROUND CAP: the reviewer found, while auditing the R4 handback, that three
authored texts this session each stated a different open-finding count and none
was derived by the only rule this repository has written down. A finding that
exists only in a session's chat is lost when that session ends, so persisting it
was worth one short round; taking on NEW work would not have been.

## Next Steps
1. R6 is the first BUILD round: T001's door — the POST route on `_RemedyHandler`
   dispatching `/api/jobs/<job_id>/commands`, the bearer plus X-Remedy-CSRF pair
   D2 rules, request-shape validation with typed errors naming the offending
   field, and BOTH halves of D3's constant-time comparison in one commit,
   compared as BYTES rather than as str, because `secrets.compare_digest` raises
   TypeError on a non-ASCII str and a query parameter is attacker-controlled.
   `import secrets` is already present, so D3 adds no import. Contract tests go
   in `tests/ui_server/test_command_channel.py` per D1.
2. R7 the catalog subset D4 rules and the rate limit D9 rules as a typed
   `ConfigKeySpec`; R8 the nonce store and audit record per D6, D7 and D8.
3. T003's effect table per D5, the plan-approval extraction landing as its own
   commit; then the integration gate, then closure.

## Risks
- R6 is the first round to touch `packages/orchestration/ui_server.py` on this
  branch and it changes a live authentication line. It is a SPLIT round and
  `tests/ui_server/test_live_state.py` already asserts the `invalid token`
  response the change must preserve.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which is
  R-0622 and routes to a paydown branch.
<<<END PLANF009R5

## C2 — the finding, in its own commit
Append R0632 to `.agent/live_review.md` as the LAST paragraph, one blank line
after the current last paragraph. Read the base bytes with `git show <round
base>:.agent/live_review.md` into `.remedy-wt/` scratch; never write a base blob
over the tracked file.

<<<SLICE R0632
- R-0632 — Low — THIS REPOSITORY HAS NO AGREED DERIVATION FOR ITS OWN OPEN-FINDING COUNT, AND THREE AUTHORED TEXTS IN ONE SESSION EACH STATED A DIFFERENT ONE. Found by the reviewer while auditing the R4 handback, and registered rather than corrected in place, because the texts have landed and §3 item 20's counter-measure is a dated correction and never an overwrite. THE ONLY WRITTEN RULE is `docs/agents/planner_reviewer_prompt.md` §3 item 10, which derives the set as "every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line". MEASURED BY THE REVIEWER at `ab6eeba1`: 197 registered paragraphs, 1 line-anchored `Done:` line naming R-0406, so item 10 gives 196. THE THREE TEXTS: the F009 R1 context slice said "196 findings are open" at a commit where item 10 gave 195; the R3 context slice repeated 196 where item 10 gave 195, and that same sentence is now accidentally correct because a later round registered an id; and the R4 handback's `## Next` says "197 findings are OPEN", which is the REGISTERED count rather than the open one. All three are the reviewer's own wording or a worker's faithful inheritance of it — no worker invented a number. THE RECORD ITSELF DISAGREES IN A FOURTH WAY, which is why this is an ambiguity rather than an arithmetic slip: the F008 R36 handback named SEVEN ids as "all still OPEN" while item 10 gave 195 at that commit, and the F008 context file said 185. So the phrase carries at least three live meanings in this repository — every unresolved paragraph, the small set of findings actionable for the current feature, and the raw registered total — and no gate has ever measured which one a given sentence meant. A TRAILING `OPEN.` MARKER IS NOT THE ANSWER EITHER, and the reviewer measured that before proposing anything: 92 of the 197 paragraphs end with `OPEN.`, while 6 of the 7 ids the F008 handback called open do not, so the marker is decoration on some paragraphs rather than a field. WHY LOW: no decision has ever turned on the number, the id ceiling is derived separately with `max` and has always been right, and the F009 R4 handback's own `## Next` correctly tells the next session to derive that ceiling mechanically. The cost is that a number a reader would reasonably trust is unfounded in three state files, one of which is `.agent/handoff.md`, the only return channel a session has. THE FIX IS THE RULING BESIDE THIS ENTRY, DECISION F009 D10 in `.agent/decisions.md`, committed by this same round: a state file that states an open-finding count states the RULE that produced it and the COMMIT it was measured at, or states no number at all. The open set is item 10's, and any narrower set is named as what it is — "the findings this feature must still act on" — rather than called "open" without qualification. THE COUNTER-MEASURE IS NOT A SWEEP: the landed sentences in the R1 and R3 context slices and the R4 handback are NOT rewritten, because two of them are in files this workflow rewrites every round and will correct themselves at the next rewrite, and the third has landed in a record that is corrected by dating rather than by editing (R-0417, R-0525). OPEN.
<<<END R0632

## C3 — the ruling
Append DECISION10 to `.agent/decisions.md` as its new last content, one blank
line after the current last paragraph. Same base-read rule as C2.

<<<SLICE DECISION10
## DECISION F009 D10 — an open-finding count is stated with the rule that produced it, or not at all (2026-08-21)

Finding R-0632 records that "N findings are open" carries at least three live meanings in this repository — every registered paragraph not answered by a `Done:` line, the small set of findings the current feature must still act on, and the raw registered total — and that three authored texts in the F009 session each stated a different number without naming which they meant.

CHOSEN: the open set is the one `docs/agents/planner_reviewer_prompt.md` §3 item 10 already defines — every line-anchored `^- R-\d+ — ` paragraph minus every line-anchored `^Done: R-\d+ — ` line — and a state file that states a count states BOTH the rule and the commit it was measured at, in the same sentence. Measured at `ab6eeba1` that count is 196. A narrower set may still be stated and is often the useful one, but it is named as what it is — "the findings this feature must still act on" — and never called "open" unqualified.

ALTERNATIVES: (a) add a trailing `OPEN.` marker to every unresolved paragraph and count that — rejected, it would require editing 105 landed paragraphs in an append-only record, which §3 item 20 forbids outright, and the reviewer measured that the marker is currently decoration: 92 of 197 paragraphs carry it while 6 of the 7 ids the F008 closure called open do not. (b) stop stating the number anywhere — rejected, it is genuinely useful in a handback, and item 10 already requires the set to be recomputed at every emission, so the derivation costs nothing beyond naming it.

WHY NO SWEEP: the landed sentences are not rewritten. `.agent/context.md` and `.agent/handoff.md` are rewritten wholesale every round and will carry the ruled form from the next rewrite onward; `.agent/live_review.md` is append-only and is corrected by dating rather than editing.

REVERSE by deleting this decision and R-0632's fix clause; nothing depends on the count.
<<<END DECISION10

## C4 — the R4 verdict
Append LEDGER5 to `.agent/live_review.md` as the LAST paragraph, one blank line
after R0632. The base for THIS append is the C2 blob.

<<<SLICE LEDGER5
Gate: R5 — the R4 entry. R4 PASSED. Every gate it reported reproduced when the reviewer re-derived it from the committed blobs, no finding is registered against the worker, and the round did the one thing it existed to do: it put R-0631 on disk, where a finding that had until then existed only in a reviewer's session could not be lost. TRANSPORT HELD THREE WAYS INCLUDING THE REVIEWER'S OWN COPY: `.remedy-wt/f009-r4.md` as emitted, `.agent/authored/f009-r4.md` at `d6a4ac07` and `.agent/last_block.md` at `4f6035b0` are all sha256 d7c9fda9b10dda513749f2aace51475d62e93179457953e0f0394370cd3ea4bf over 19558 bytes and 192 lines. BOTH APPENDS HOLD UNDER THE NEW SHAPE, re-run by the reviewer: at `2995a9f1` the base blob is a byte-exact PREFIX and the remainder equals a newline plus the reviewer's own R0631 slice, and at `a3fb5d54` the C2 blob is a byte-exact PREFIX and the remainder equals a newline plus LEDGER4; reader (b) in its general form — the LAST N blank-line units of the whole file compared against the slice's N paragraphs IN ORDER, with N COUNTED rather than asserted — reads N = 1 for both and agrees with reader (a) in both, over 205 and 206 units. THE SETS MOVED EXACTLY AS ORDERED: `^- R-\d+ — ` 196 at the base, 197 at C2 and 197 at C3, all ids DISTINCT at each; `^- R-0631 — ` 0, 1 and 1; `^Done: R-\d+ — ` 1 throughout; `^Landed: ` 0 throughout; `^> Next free id` 0 throughout; `^Gate: R\d+ — ` 3, 3 and 4 over that many DISTINCT keys, with 3 of the 4 headers at C3 matching the n-minus-one shape and the single non-match reading `Gate: R1 — the F008 R36 entry.` THE RANGE HOLDS: the path set is EXACTLY the five declared paths, five single-parent commits before the handback with insertions 192, 110, 20, 2 and 2, each equal to the `## Commits` column, 0 marker lines in both committed targets, `amend`, `rebase` and `cherry` each 0, `git ls-files .remedy-wt` 0, a clean tree, the branch pushed to `ab6eeba1`, and a 66-line handback carrying every mandated section. THE ROUND EARNED ITS PASS TWICE OVER ON CONDUCT. It ran the new two-reader gate in the GENERAL form even though both its slices were the N=1 case where the old wording would have sufficed, because the wording is what carries forward to a round where N is larger — the opposite of the shortcut that produced R-0631. And it caught a false numeral in its OWN handback before staging it, having drafted the line count as 71, measured 66, corrected both occurrences and re-measured the corrected text to a fixed point rather than assuming the correction was right — which is R-0486 and R-0488's exact failure mode, avoided by measurement rather than by luck. WHAT THE REVIEWER GOT WRONG IS RECORDED DIRECTLY ABOVE AS R-0632, and it is the reviewer's alone: the handback's `## Next` states an open-finding count of 197 where the only written derivation gives 196, and it says so because two earlier context slices the reviewer authored had already conflated the registered total with the open set. The worker inherited a number it had no reason to doubt. DECISION F009 D10, committed by this round, rules the derivation and requires the rule and the commit to travel with the number.
<<<END LEDGER5

## Constraints
1. Apply every slice BYTE FOR BYTE out of the committed C0a blob. Do not retype,
   rewrap, reflow, reindent or whitespace-adjust any of them. If a slice looks
   wrong to you, apply it as written and record the objection in the handback —
   an objection is recorded, never acted on.
2. The commit order is C0a, C0b, C1, C2, C3, C4, C5 and nothing comes between
   them. C1 is the first substantive commit; C2 precedes C3 precedes C4.
3. The change set is the six paths named above. Write no code and touch nothing
   under `packages/`, `apps/`, `tests/` or `docs/`.
4. `.remedy-wt/` is gitignored scratch. Every multi-step gate goes into a script
   there; `git status --porcelain` prints 0 lines after each commit.
5. Push with `git push` after C5, the last commit of this session.

## Done when
- G1 `.agent/STOP` ABSENT, read at Step 0. `git rev-parse --abbrev-ref HEAD`
  prints `feature/f009-single-write-channel` at every reading. `git status
  --porcelain` prints 0 lines after each of C0a through C5. Report the round base
  SHA from Step 0.
- G2 Transport EQUAL: the scratch file as received, `.agent/authored/f009-r5.md`
  at C0a and `.agent/last_block.md` at C0b all carry the same sha256, byte count
  and line count, equal to the digest in the task prompt.
- G3 Report, per slice, the newline-included sha256, byte count and line count,
  the COUNT of slices from your own ordered extraction out of the committed C0a
  blob, and the three aggregate readings.
- G4 `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R5; report its line count
  against the 50-line cap; `Steps` occurs; `^## Goal$` and `^## Next Steps$` each
  match exactly 1 line; the first `\bF\d{3}\b` match is `F009`.
- G5 The appends at C2 and at C4, each proved TWICE over independent extractors
  in the general N-paragraph form: (a) the previous blob is a byte-exact PREFIX
  and the remainder EQUALS a newline plus the slice, reported with its sha256,
  bytes and lines; (b) with N COUNTED BY YOUR SCRIPT AND REPORTED, the LAST N
  blank-line units of the whole file equal the slice's N paragraphs IN ORDER.
  NEGATIVE CONTROL on the FIRST appended paragraph of each: flip ONE printable
  ASCII byte and confirm BOTH readings REJECT it while both ACCEPT the unflipped
  value; report all four outcomes per append. The base for C2 is the round base;
  the base for C4 is the C2 blob.
- G6 The append at C3 to `.agent/decisions.md`, proved the same two ways with its
  own control and its own counted N. Report `^## DECISION F009 D\d+ — ` at the
  round base and at C3, and `^## DECISION ` at both — report the totals rather
  than predicting them — and report the DISTINCT F009 keys the file carries at
  C3.
- G7 At the round base, at C2 and at C4, line-anchored: `^- R-\d+ — ` 197, 198
  and 198 with all ids DISTINCT at each; `^- R-0632 — ` 0, 1 and 1;
  `^Done: R-\d+ — ` 1 at all three; `^Landed: ` 0 at all three; `^> Next free id`
  0 at all three; `^Gate: R\d+ — ` 4, 4 and 5 over that many DISTINCT keys.
  Report the max id at C4. Of the `Gate: ` lines at C4, report how many match
  `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one less than the
  first, and quote to its first period any that does not — the expected reading
  is four matches and one non-match reading `Gate: R1 — the F008 R36 entry.`
  ALSO report, at C4, the count item 10's rule gives: line-anchored
  `^- R-\d+ — ` minus line-anchored `^Done: R-\d+ — `. That value is the one the
  handback must state, WITH the rule and the commit beside it (DECISION F009
  D10). Do not restate it from this block — report what your script printed.
- G8 The range from the round base to C4: `git diff --name-only` lists EXACTLY
  the five paths of the change set other than `.agent/handoff.md`, the set
  difference empty in both directions. Walk `git rev-list --reverse` and report,
  per commit, that it has ONE parent and its `git show --numstat` insertions,
  with `git diff --numstat` AGREEING on every cell and every cell equal to the
  `+/-` column of your `## Commits` table. `^<<<SLICE ` and `^<<<END ` read 0
  lines in `.agent/plan.md`, `.agent/live_review.md` and `.agent/decisions.md`.
  Classify this round's own reflog entries by the operation before the first `:`
  in `%gs` and report `amend`, `rebase` and `cherry`, which must each be 0;
  assert no total over the whole reflog (R-0601). Report `git ls-files
  .remedy-wt` as a count.
- G9 The handback carries every mandated section of
  docs/agents/handback_template.md, an item-status table holding exactly one row
  for each of C0a, C0b, C1, C2, C3, C4 and C5, the round base SHA, and one line
  per gate. Report its line count against the 100 that seven commits allow. Its
  `## Next` section states, in this order: that this session ended after a FIFTH
  round DECLARED against its stated four-round cap, with the reason; that no
  `.agent/STOP` is present; that the next session's FIRST action is the
  `.agent/STOP` re-read (Phase 1 rule 1) and its SECOND the Open PR Gate (Phase 1
  rule 2), which is EMPTY because this branch carries no pull request and F009
  opens one at its own closure; the open-finding count from G7 WITH item 10's
  rule and the commit named beside it, per DECISION F009 D10; that the next free
  id is derived with `max` over the line-anchored entries and what that gives;
  that `.agent/candidates.md` is EMPTY; and that R6 is the T001 door as
  `.agent/plan.md` describes it.

Handback:    completion report + rewrite `.agent/handoff.md`. The state block
             repeats this Fortschritt line verbatim: 10 % (T001 offen · T002
             offen · T003 offen — beansprucht, vermessen, entschieden; der Bau
             beginnt in R6 mit D1 bis D10 als Vorgabe) — Schätzung
──────────────────────────────────────────────────────────────
