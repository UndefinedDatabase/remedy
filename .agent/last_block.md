── STEP T001/3 — F009 ────────────────────────────────────────
Goal:        Build T001's door — the authenticated POST route
             `/api/jobs/<job_id>/commands` on `_RemedyHandler`, with request-shape
             validation returning typed errors that name the offending field, and
             both halves of D3's constant-time token comparison — under contract
             tests in `tests/ui_server/test_command_channel.py`.

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R5 verdict
             into the review record · C3 DECISION F009 D11 · C4 the route, the
             comparison and the tests · C5 handback.

THE ROUND BASE is `b6d80e8e4d6cdd27c750488a40595de3f70be7a1`. Every gate reading
below said to be "at the round base" is measured against that SHA. C5's own SHA
cannot exist inside C5, so C5 is named by role and the round report carries its
value (R-0371).

THIS ROUND MINTS NO FINDING ID. The defect R5 carried — a block ordering no
canary and no state-reader suite over a change set of `.agent/` state files — is
already registered OPEN as R-0607, whose FIX clause states exactly that rule.
Checklist item 30 forbids a second id for a defect the open set already holds, so
the recurrence is recorded inside the R6 verdict entry instead, which is the form
this record already uses for a lesson that mints nothing.

Change set — these paths and nothing else:
  `.agent/authored/f009-r6.md`
  `.agent/last_block.md`
  `.agent/plan.md`
  `.agent/live_review.md`
  `.agent/decisions.md`
  `packages/orchestration/ui_server.py`
  `tests/ui_server/test_command_channel.py`
  `.agent/handoff.md`

Slice convention: the authored units below are delimited by `<<<SLICE <NAME>` and
`<<<END <NAME>` lines. Extract each from the COMMITTED C0a blob by those marker
lines, with a script, and apply it programmatically. The marker lines themselves
are never written into any target file.

<<<SLICE PLANF009R6
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
R6 builds T001's door: the POST route dispatching `/api/jobs/<job_id>/commands`,
the bearer plus X-Remedy-CSRF pair D2 and D11 rule, request-shape validation
returning typed errors that name the offending field, and BOTH halves of D3's
constant-time comparison — compared as BYTES, because `secrets.compare_digest`
raises TypeError on a non-ASCII str and the query token is attacker-controlled.
A well-formed authenticated command reaches a 501 seam, which is the honest
answer while D4's exposed subset is unbuilt. Contract tests go in
`tests/ui_server/test_command_channel.py` per D1.

## Next Steps
1. R7 replaces the 501 seam with the catalog subset D4 rules, and adds the rate
   limit D9 rules as a typed `ConfigKeySpec`.
2. R8 the nonce store and the audit record per D6, D7 and D8, so that a replay
   returns the ORIGINAL body and a rejection is audited.
3. T003's effect table per D5, the plan-approval extraction landing as its own
   commit; then the client wiring that sends both headers, the integration gate,
   then closure.

## Risks
- R6 changes a live authentication line on the GET door. It is a SPLIT round and
  `tests/ui_server/test_live_state.py` already asserts the `invalid token`
  response the change must preserve.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which is
  R-0622 and routes to a paydown branch.
<<<END PLANF009R6

<<<SLICE DECISION11
## DECISION F009 D11 — the `X-Remedy-CSRF` header carries the server token (2026-08-21)

D2 ruled that the POST door requires `Authorization: Bearer <token>` AND an `X-Remedy-CSRF` header "double-submitted against the served app", without fixing what value that header carries. There is no cookie to double-submit against: the shell at `/` is served without a token and the React client reads the token from the URL query — `apps/ui/src/RemedyApp.tsx` line 10 at `b6d80e8e` — so the only secret the app holds is the server token itself.

CHOSEN: `X-Remedy-CSRF` carries that same server token, compared constant-time as bytes by the same helper the bearer check uses. A cross-site page cannot set a custom header on a cross-origin request without a preflight this server never grants, so the header's PRESENCE is what defeats CSRF; requiring its VALUE additionally makes the door fail closed on a half-wired client instead of silently accepting one.

ALTERNATIVES: (a) accept any non-empty `X-Remedy-CSRF` — rejected, it makes a wiring bug indistinguishable from a working client. (b) mint a separate CSRF secret and embed it in the shell — rejected for this feature: it adds a second secret to serve, rotate and redact, against no attacker the first one does not already stop, and the shell embeds the token by plain string substitution today.

REVERSE by dropping the value comparison and checking only that the header is present; nothing else about the route changes.
<<<END DECISION11

<<<SLICE LEDGER6
Gate: R6 — the R5 entry. R5 PASSED. Every value it reported reproduced when the reviewer re-derived it from the committed blobs rather than reading it back, and no finding is registered against the worker. TRANSPORT HELD: `.agent/authored/f009-r5.md` at `264d7d04` and `.agent/last_block.md` at `ebc343e5` are both sha256 06f17977fdd896a515b2f579912388360445e489efa9cfe0dc5c634ba7874fd5 over 20578 bytes and 217 lines. THE FOUR SLICES extracted from the committed C0a blob carry the newline-included digests, byte counts and line counts the handback reports, all newline-terminated, none with a leading blank line or trailing whitespace, and `.agent/plan.md` at `6d9a02b0` is BYTE-EQUAL to PLANF009R5 at 48 lines under the 50-line cap. ALL THREE APPENDS HOLD UNDER BOTH READERS, re-run by the reviewer: at `38cc3eed` and at `5f0a8112` over `.agent/live_review.md` and at `8c7ef452` over `.agent/decisions.md`, the previous blob is a byte-exact PREFIX and the remainder equals a newline plus the slice, while an INDEPENDENT blank-line split of the whole file puts the slice's N paragraphs LAST and IN ORDER over 207, 208 and 1098 units — with N COUNTED at 1, 1 and 6, and a one-byte flip of the FIRST appended paragraph REJECTED by both readers in all three positions while the unflipped value is ACCEPTED by both. The decisions append is the FIRST multi-paragraph exercise of R-0631's fix and it was run in the general form rather than the N=1 shortcut. THE SETS MOVED AS ORDERED: `^- R-\d+ — ` 197, 198 and 198 with every id DISTINCT at each, `^- R-0632 — ` 0, 1 and 1, `^Done: R-\d+ — ` 1 throughout, `^Landed: ` and `^> Next free id` 0 throughout, `^Gate: R\d+ — ` 4, 4 and 5 over that many DISTINCT keys, and of the five headers at `5f0a8112` exactly four match `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one less than the first while the single non-match reads `Gate: R1 — the F008 R36 entry.` `^## DECISION F009 D\d+ — ` goes 10 at `8c7ef452` over the DISTINCT keys D1 through D10 and `^## DECISION ` goes 94 to 95. THE RANGE HOLDS: the path set from the round base to `5f0a8112` is EXACTLY the five declared paths with the set difference empty both ways, six single-parent commits before the handback with insertions 217, 128, 19, 2, 12 and 2, every cell of `git show --numstat` AGREEING with `git diff --numstat` and with the `+/-` column of the handback's `## Commits` table, 0 lines beginning `<<<SLICE ` or `<<<END ` in all three committed targets, eight reflog rows touching this round's commits and the round base, ALL of them `commit`, with `amend`, `rebase` and `cherry` each 0, `git ls-files .remedy-wt` 0, a clean tree, and a 72-line handback under the 100 that seven commits allow. THE ROUND'S OWN NUMBER IS RIGHT AND IS DERIVED RATHER THAN RECALLED: item 10's rule gives 198 minus 1 = 197 open findings at `5f0a8112` and 196 at the round base, which is the movement DECISION F009 D10 exists to make legible, and the handback states the rule and the commit beside the number as D10 requires. WHAT THIS ENTRY OWES THE RECORD IS A RECURRENCE, AND IT MINTS NO ID FOR IT. The R5 block ordered no canary and no state-reader suite over a change set that rewrote `.agent/plan.md`, `.agent/last_block.md` and `.agent/handoff.md` and appended to `.agent/live_review.md` and `.agent/decisions.md` — the exact defect already registered OPEN as R-0607, whose FIX clause reads that a block's done-when carries the canary unconditionally and that a change set holding any `.agent/` state file also carries the four state-reader files. `.agent/context.md` states the same obligation for this branch in its own words. Checklist item 30 forbids a second id for a defect the open set already holds, so this is recorded against R-0607 rather than minted: it is that finding's second instance, and the first inside F009. THE OMISSION COST NOTHING, and that is measurement rather than luck — the reviewer ran both suites itself in the primary checkout at `b6d80e8e`, serially, and measured `tests/ui_server/` with `tests/orchestration/test_test_runner.py`, `tests/regression/test_resource_safety.py` and `tests/orchestration/test_integrity_gate.py` at EXIT 0 and 423 passed, and the canary `tests/cli/test_golden_path.py` at EXIT 0 and 42 passed. R5 claimed no colour for either, having measured neither, which is the honest half of the same round.
<<<END LEDGER6

Constraints:
1. Apply the three slices BYTE FOR BYTE out of the committed C0a blob. Do not
   retype, rewrap, reflow, reindent or whitespace-adjust any of them. If a slice
   looks wrong to you, apply it as written and record the objection in the
   handback — an objection is recorded, never acted on.
2. The commit order is C0a, C0b, C1, C2, C3, C4, C5 and nothing comes between
   them. C1 is the first substantive commit (checklist item 23).
3. C4 is the ONLY commit that touches `packages/` or `tests/`. It carries both
   the route and its tests, because a code commit whose gate cannot run is not
   reviewable, and it carries BOTH halves of D3 per that decision.
4. C4 is production code and this is a SPLIT round: you write it, the reviewer
   gates it. Follow the AGENTS.md self-review loop before it — `git diff --stat`
   then `git diff`, read for scope drift and debug leftovers, repeat until clean.
5. THE CODE IS YOURS TO WRITE. The contract below fixes the OBSERVABLE behaviour
   — routes, status codes, body keys, header names, comparison semantics. Naming,
   helper decomposition and control flow are yours, within AGENTS.md's
   discoverability conventions: a public or module-level name carries 2–4 words
   including one domain word, and the one-line WHY comment sits directly above
   the definition.
6. `.remedy-wt/` is gitignored scratch. Every multi-step gate goes into a script
   there; `git status --porcelain` prints 0 lines after each commit.
7. Destructive verification — the red-proof of G9 — runs ONLY inside a disposable
   `git worktree` under `.remedy-wt/`, never in the primary checkout, and the
   worktree is removed and pruned before C5. Suite commands otherwise run in the
   PRIMARY checkout, because a fresh worktree lacks `apps/ui/node_modules`
   (R-0518).
8. Push with `git push` after C5, the last commit of this session.

The C4 contract — observable behaviour:

A. A module-level constant-time token comparison, taking the supplied token and
   the expected token and returning a bool. It compares them AS BYTES, encoding
   each with UTF-8 before `secrets.compare_digest`, because that function raises
   TypeError on a non-ASCII `str` and both tokens here are attacker-supplied.
   `import secrets` is already present at line 26 as of `b6d80e8e`; add no import
   for it. A missing header — `self.headers.get(...)` returning None — is treated
   as the empty string and never reaches `.encode`.
B. `do_GET`'s existing check becomes a call to that helper. Its 403 response body
   stays exactly `{"error": "invalid token"}`: `tests/ui_server/test_live_state.py`
   asserts that string at `b6d80e8e`, and the response is unchanged for every
   non-attacker input.
C. `do_POST` dispatches `POST /api/jobs/<job_id>/commands`. Every OTHER path, and
   every PUT and DELETE, keeps answering 405 with the body it answers today.
D. On the commands path, in this order, each failure returning at once:
   1. `Authorization` absent, not of the form `Bearer <token>`, or its token not
      matching by the helper of A → 403 `{"error": "invalid token"}`.
   2. `X-Remedy-CSRF` absent or not matching by the helper of A → 403
      `{"error": "invalid csrf token"}` (DECISION F009 D11).
   3. The job id not resolving → the same error the GET door returns for an
      unresolvable job, produced by the same loader.
   4. Request shape, each failure a 400 whose body carries BOTH an `error` key
      and a `field` key naming the offending field: a body that is absent, over
      64 KiB by `Content-Length`, not valid JSON, or not a JSON object → field
      `body`; `command` missing, not a string, or empty → field `command`;
      `client_nonce` missing, not a string, or empty → field `client_nonce`;
      `args` present but not a JSON object → field `args`. `args` absent is
      VALID and means the empty object.
   5. Otherwise → 501 `{"error": "command channel not yet accepting commands",
      "command": <the submitted command>}`. This is the R7 seam and carries the
      one-line WHY comment naming R7 and D4 as what replaces it. Auth and shape
      are decided BEFORE it, so an unauthenticated caller never learns that the
      seam exists.
E. `_RemedyHandler`'s class docstring reads "Read-only handler. No POST/PUT/DELETE."
   at `b6d80e8e` and is false once D lands. Rewrite it to state the one mutating
   door and that every other mutating route answers 405. Deliberate absences are
   documented where a reader would search for them.
F. `tests/ui_server/test_command_channel.py` covers, at minimum: 405 for a POST to
   a non-commands path and for PUT and DELETE; 403 for a missing, malformed and
   wrong bearer; 403 for a missing and a wrong CSRF header; the four 400 field
   values of D.4, each asserted on the `field` key and not only on the status; an
   unresolvable job id; the 501 seam for a well-formed authenticated request; and
   a REGRESSION for the TypeError trap of A — a non-ASCII token supplied to the
   GET door answers 403 rather than raising. It also asserts the GET door still
   answers 200 for the correct token, so D3's change is proved not to have broken
   the half it touches. Follow the fixture idiom of
   `tests/ui_server/test_live_state.py`, which starts a real server on a port.

Done when:
- G1 `.agent/STOP` ABSENT, read at Step 0 and again before C4.
  `git rev-parse --abbrev-ref HEAD` prints `feature/f009-single-write-channel` at
  every reading. `git status --porcelain` prints 0 lines after each of C0a
  through C5. Report the round base SHA you read at Step 0.
- G2 Transport EQUAL: the scratch file as received, `.agent/authored/f009-r6.md`
  at C0a and `.agent/last_block.md` at C0b all carry the same sha256, byte count
  and line count, equal to the digest in the task prompt. Write C0b from the
  COMMITTED C0a blob, never from the scratch file again.
- G3 Report, per slice, the newline-included sha256, byte count and line count;
  the COUNT of slices from your own ordered extraction out of the committed C0a
  blob; and the three aggregates — all newline-terminated, any leading blank
  line, any trailing whitespace.
- G4 `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R6. Report its line count
  against the 50-line cap; `^## Goal$` and `^## Next Steps$` each match exactly
  1 line; the first `\bF\d{3}\b` match is `F009`.
- G5 The append at C2, base = the round base, proved TWICE over independent
  extractors in the general N-paragraph form: (a) the base blob is a byte-exact
  PREFIX and the remainder EQUALS a newline plus LEDGER6, reported with its
  sha256, bytes and lines; (b) with N COUNTED BY YOUR SCRIPT AND REPORTED, the
  LAST N blank-line units of the whole file equal the slice's N paragraphs IN
  ORDER. NEGATIVE CONTROL on the FIRST appended paragraph: flip ONE printable
  ASCII byte and confirm BOTH readings REJECT it while both ACCEPT the unflipped
  value; report all four outcomes.
- G6 The append at C3 to `.agent/decisions.md`, base = the round base, proved the
  same two ways with its own control and its own counted N. REPORT — do not
  predict — `^## DECISION F009 D\d+ — ` and `^## DECISION ` at the round base and
  at C3, and the DISTINCT F009 keys the file carries at C3.
- G7 At the round base and at C2, line-anchored over `.agent/live_review.md`:
  `^- R-\d+ — ` 198 at BOTH with all ids DISTINCT at both — THIS ROUND MINTS NO
  ID — `^Done: R-\d+ — ` 1 at both, `^Landed: ` 0 at both, `^> Next free id` 0 at
  both, `^Gate: R\d+ — ` 5 then 6 over that many DISTINCT keys. Report the max id
  at C2. Of the `Gate: ` lines at C2, report how many match
  `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one less than the
  first, and quote to its first period any that does not — the expected reading
  is five matches and one non-match reading `Gate: R1 — the F008 R36 entry.`
  ALSO report the count item 10's rule gives at C2: line-anchored `^- R-\d+ — `
  minus line-anchored `^Done: R-\d+ — `. State that value in the handback WITH
  the rule and the commit beside it, per DECISION F009 D10, and report what your
  script printed rather than restating it from this block.
- G8 In the PRIMARY checkout at C4, run these and report each command's EXIT CODE
  and its passed-plus-skipped total, serially — never two pytest processes at
  once (R-0518, F085 R64):
    `python3 -m ruff check packages/orchestration/ui_server.py tests/ui_server/test_command_channel.py`
    `python3 -m pytest tests/ui_server/test_command_channel.py -q -rf`
    `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
    `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
  Every one must EXIT 0. The ruff reading is ordered as exit 0 because the
  reviewer measured `python3 -m ruff check packages/orchestration/ui_server.py`
  at the round base with this repository's own `pyproject.toml` and it printed
  `All checks passed!`; the test path does not exist at the round base, so no
  baseline reading of it is claimed. Report the count of tests your new module
  contributes, taken from `python3 -m pytest tests/ui_server/test_command_channel.py
  --collect-only -q` and NOT by regex over `-v` output (R-0611). Do not predict
  any of these totals — report what the runs printed.
- G9 A red-proof PAIR, both halves inside ONE disposable `git worktree` under
  `.remedy-wt/` checked out at C4, the primary checkout never written to:
  (a) UNMUTATED, run `python3 -m pytest tests/ui_server/test_command_channel.py -q -rf`
      and report its exit code and totals. This is the control that says what the
      worktree environment does to this module before anything is broken.
  (b) MUTATED, make the bearer comparison of contract A always succeed — the
      smallest edit that does so — and re-run the SAME command. Report the exact
      byte string you changed, the FILE you changed it in, and its occurrence
      count IN THAT FILE at C4, which must be 1 (checklist item 25); if it is
      not 1, extend the string until it is and report the extended one.
  Report BOTH colours and, for (b), the failing node ids from the run's own `-rf`
  summary. The expectation is that (b) is RED where (a) is GREEN, and that the
  wrong-bearer and missing-bearer tests are among the failures. Report the
  outcome you got — if (a) is not green, say so and treat the pair as evidence
  about the worktree rather than about the guard. Remove and prune the worktree
  before C5 and report `git worktree list`.
- G10 The range from the round base to C4: `git diff --name-only` lists EXACTLY
  the seven paths of the change set other than `.agent/handoff.md`, the set
  difference empty in both directions. Walk `git rev-list --reverse` and report,
  per commit, that it has ONE parent and its `git show --numstat` insertions,
  with `git diff --numstat` AGREEING on every cell and every cell equal to the
  `+/-` column of your handback's `## Commits` table (checklist item 28). Every
  commit stays under the 500-insertion cap of AGENTS.md DECISION F104 D1; if C4
  does not, STOP and split it before committing rather than declaring an overage.
  `^<<<SLICE ` and `^<<<END ` read 0 lines in `.agent/plan.md`,
  `.agent/live_review.md`, `.agent/decisions.md`,
  `packages/orchestration/ui_server.py` and
  `tests/ui_server/test_command_channel.py`. Classify this round's own reflog
  entries by the operation before the first `:` in `%gs` and report `amend`,
  `rebase` and `cherry`, which must each be 0; assert no total over the whole
  reflog (R-0601). Report `git ls-files .remedy-wt` as a count.
- G11 The handback carries every mandated section of
  docs/agents/handback_template.md, an item-status table holding exactly one row
  for each of C0a, C0b, C1, C2, C3, C4 and C5, the round base SHA, and one line
  per gate — the raw transcripts go in the round report, not in the handback
  (R-0582). Report its line count against the 100 that seven commits allow. Its
  `## Next` section states: that no `.agent/STOP` is present; that the next
  session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1) and its
  SECOND the Open PR Gate (Phase 1 rule 2), which is EMPTY because this branch
  carries no pull request and F009 opens one at its own closure; the
  open-finding count from G7 WITH item 10's rule and the commit named beside it;
  that the next free id is derived with `max` over the line-anchored entries and
  what that gives; that `.agent/candidates.md` is EMPTY; and that R7 replaces the
  501 seam with D4's catalog subset and adds D9's rate limit.

Handback:    completion report + rewrite `.agent/handoff.md`. The state block
             repeats this Fortschritt line verbatim: 20 % (T001 gebaut · T002
             offen · T003 offen — die Tür steht, Katalog und Quittung folgen in
             R7 und R8) — Schätzung
──────────────────────────────────────────────────────────────
