── STEP T001/3 — F009 ────────────────────────────────────────
Goal:        Put DECISION F009 D4's UI-exposed catalog subset in front of the
             command door's R7 seam, so that only `job.stop` and
             `decision.resolve` reach it and every other command id is refused
             by a typed 400 naming the `command` field.

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 register R-0633
             against the R6 block · C3 DECISION F009 D12 · C4 the R6 verdict into
             the review record · C5 the exposed subset, the endpoint check and
             the tests · C6 handback.

THE ROUND BASE is `98592b721a5aab3da28beb9a19f3fd4074c26b85`. Every gate reading
below said to be "at the round base" is measured against that SHA. C6's own SHA
cannot exist inside C6, so C6 is named by role and the round report carries its
value (R-0371).

Change set — these paths and nothing else:
  `.agent/authored/f009-r7.md`
  `.agent/last_block.md`
  `.agent/plan.md`
  `.agent/live_review.md`
  `.agent/decisions.md`
  `apps/cli/command_catalog.py`
  `packages/orchestration/ui_server.py`
  `tests/ui_server/test_command_channel.py`
  `.agent/handoff.md`

Slice convention: the authored units below are delimited by `<<<SLICE <NAME>` and
`<<<END <NAME>` lines. Extract each from the COMMITTED C0a blob by those marker
lines, with a script, and apply it programmatically. The marker lines themselves
are never written into any target file.

<<<SLICE PLANF009R7
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
R7 declares DECISION F009 D4's `UI_EXPOSED_COMMANDS` beside the catalog it
constrains and puts it in front of the door's seam: a command id outside the set
is refused with a typed 400 naming the `command` field, per DECISION F009 D12.
The 501 seam SURVIVES this round and is merely narrowed — only `job.stop` and
`decision.resolve` now reach it — because a command still has no effect to run
until D5's effect table lands. R7 also registers R-0633 against the R6 block.

## Next Steps
1. R8 the rate limit D9 rules as a typed `ConfigKeySpec` keyed by the pair
   (token fingerprint, job id), refusing with 429 rather than waiting, with the
   fingerprint helper D7 rules introduced where it is first used.
2. R9 the nonce store and the audit record per D6, D7 and D8, so that a replay
   returns the ORIGINAL body and a rejection is audited.
3. T003's effect table per D5 — the round that finally retires the 501 seam —
   with the plan-approval extraction landing as its own commit; then the client
   wiring that sends both headers, the integration gate, then closure.

## Risks
- `apps/cli/command_catalog.py` is 4824 lines and is imported by the whole CLI.
  This round adds one module-level name to it and edits no entry of `CATALOG`.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which is
  R-0622 and routes to a paydown branch.
<<<END PLANF009R7

<<<SLICE R0633
- R-0633 — Low, A REVIEWER GATE ORDERED A RED-PROOF WHOSE STATED PROPERTY NAMED A TEST ITS OWN MUTATION CANNOT REACH. The defect is the reviewer's, in the F009 R6 block saved at `460d9898`, and it was FOUND AND DECLARED BY THE WORKER as deviation 3 of the R6 handback. G9 ordered the bearer comparison mutated so that it always succeeds, and then stated "the expectation is that (b) is RED where (a) is GREEN, and that the wrong-bearer and missing-bearer tests are among the failures". The missing-bearer test cannot be among them: `_bearer_token_accepted` in `packages/orchestration/ui_server.py` at `6cd082c2` rejects an absent or malformed `Authorization` at its form check — `scheme != "Bearer" or not supplied` — and returns BEFORE the token comparison, so no mutation of that comparison is reachable from a request carrying no bearer at all. This is the class docs/agents/planner_reviewer_prompt.md §3 item 18 already governs — an ordered recipe and the property it is ordered to establish, not read against each other before emission — so the rule was on disk and binding and the block broke it anyway. The block's own hedge, "Report the outcome you got", is what kept the record honest and is why this is Low rather than Medium: the worker reported two failures and named them, rather than reshaping the mutation until it matched the reviewer's sentence. It still cost the round a declared deviation to prove a reviewer's mistake. FIX: when a block names the tests a mutation should fail, it derives them by READING THE GUARD'S CONTROL FLOW from the mutation point outward — every early return above the mutated line is a test the mutation cannot reach — or it names no tests at all and orders only the colour plus "report the failing node ids", which is what §3 item 5 already prefers. This finding registers the instance; the counter-measure is item 18's and needs no new checklist entry.
<<<END R0633

<<<SLICE DECISION12
## DECISION F009 D12 — a command outside the exposed subset is a typed 400 on the `command` field (2026-08-21)

D4 ruled the exposed subset a `UI_EXPOSED_COMMANDS` frozenset of catalog `command_id` values and ruled that the endpoint imports it, without fixing what the door answers when a well-formed request names an id outside it. The door already has two refusal vocabularies at `98592b72`: 403 with `{"error": ...}` for a credential that fails, and 400 with `{"error": ..., "field": ...}` for a request whose shape is wrong.

CHOSEN: an unexposed `command_id` is 400 with `field` set to `command`, reusing the shape D.4 of the R6 contract established. It is a statement about the request the client sent, and the field it must change to send a different one is `command`.

ALTERNATIVES: (a) 403 — rejected, it means "your credential failed" on this door, and a client that retried authentication on a policy refusal would be chasing the wrong repair. (b) 404 — rejected, a command id is not a resource this API exposes at a URL, and a 404 on the commands path already means the JOB did not resolve. (c) a distinct 422 — rejected, it adds a third vocabulary for a case the second already covers.

THE REFUSAL DELIBERATELY DOES NOT DISTINGUISH an id that is absent from the catalog entirely from one that exists but is not UI-exposed. Both are "not a command this door accepts", and separating them would let an unauthenticated-but-credentialed caller enumerate the CLI surface through the write door.

REVERSE by giving the unexposed case its own status; the field name does not change.
<<<END DECISION12

<<<SLICE LEDGER7
Gate: R7 — the R6 entry. R6 PASSED, and it is the first round of this feature to put production code on the branch. Every value the handback reported reproduced when the reviewer re-derived it from the committed blobs, and the reviewer ran every suite and every mutation itself rather than reading a colour back. TRANSPORT HELD THREE WAYS INCLUDING THE REVIEWER'S OWN COPY: `.remedy-wt/f009-r6.md` as emitted, `.agent/authored/f009-r6.md` at `460d9898` and `.agent/last_block.md` at `817d38e7` are all sha256 2cf6c40adb8e51fea9eb439ab1fd2fa6b3bb0c71ccb60068408a0f1aa03c58d4 over 23544 bytes and 281 lines. THE SLICES LANDED WHOLE: PLANF009R6 63c153e5/2351/42, DECISION11 648d943a/1481/9 and LEDGER6 7451ea15/4386/1, all newline-terminated with no leading blank line and no trailing whitespace, and `.agent/plan.md` at `8c6b887f` BYTE-EQUAL to PLANF009R6 at 42 lines under the 50-line cap. BOTH APPENDS HOLD UNDER BOTH READERS with their own counted N and their own control: at `cd163c19` over `.agent/live_review.md` the base blob is a byte-exact PREFIX and the remainder equals a newline plus LEDGER6 (9d0449d1, 4387 bytes, 2 lines) with N COUNTED 1 against 209 independent blank-line units, and at `ba354bce` over `.agent/decisions.md` the remainder equals a newline plus DECISION11 (2868a293, 1482 bytes, 10 lines) with N COUNTED 5 against 1103 units, each LAST-N comparison holding IN ORDER and each one-byte flip of the FIRST appended paragraph REJECTED by both readers while the unflipped value is ACCEPTED by both. THE SETS ARE WHAT THE ROUND CLAIMED: `^- R-\d+ — ` 198 at the round base AND at `cd163c19` with all 198 ids DISTINCT at both — the round minted no id, recording its recurrence against R-0607 instead — `^Done: R-\d+ — ` 1, `^Landed: ` 0 and `^> Next free id` 0 at both, `^Gate: R\d+ — ` 5 then 6 over that many DISTINCT keys with five of the six matching the n-minus-one shape, `^## DECISION F009 D\d+ — ` 11 at `ba354bce` over the DISTINCT keys D1 through D11 and `^## DECISION ` 95 then 96, and item 10's rule giving 197 open at both commits. THE RANGE HOLDS: the path set from the round base to `cbf46063` is EXACTLY the seven declared paths with the set difference empty both ways, eight single-parent commits with `git show --numstat` and `git diff --numstat` AGREEING on every cell and every cell equal to the `## Commits` column, insertions 281, 231, 15, 2, 10, 420, 130 and 47, zero lines beginning `<<<SLICE ` or `<<<END ` in all five committed targets, nine reflog rows touching this round's commits and the round base with `amend`, `rebase` and `cherry` each 0, `git ls-files .remedy-wt` 0, a clean tree, and an 80-line handback under the 100 its bundle allows. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout at `98592b72`: `ruff check` over both changed code paths EXITS 0 at `All checks passed!`, `tests/ui_server/test_command_channel.py` EXITS 0 at 36 passed, the state-reader group EXITS 0 at 459 passed — exactly the 423 measured before this round plus the 36 the new module contributes — and the canary EXITS 0 at 42 passed. THE RED-PROOF IS THE REVIEWER'S OWN AND IT WENT FURTHER THAN THE ONE ORDERED, four mutations run one at a time in the reviewer's own disposable worktree at `98592b72` with the source restored byte-identically after each: making the bearer comparison always succeed fails exactly the wrong-bearer and non-ASCII-bearer tests; making the CSRF comparison always succeed fails exactly the missing-CSRF and wrong-CSRF tests; making the GET door's comparison always succeed fails exactly the two GET-door tests, which is what proves D3's SECOND half is pinned rather than merely written; and allowing an empty `command` fails exactly the empty-command test. Each guard is therefore independently load-bearing and the module's green is a measurement rather than a decoration. THE ROUND EARNED ITS PASS THREE TIMES OVER ON CONDUCT. It SPLIT C4 rather than declaring an overage: staged whole the commit measured 550 insertions against the 500-line cap, and the block ordered a split, so it shipped C4a with the production code plus the 23 tests that exercise the door end to end — keeping the constraint that a code commit's gate must run — and C4b with the shape and seam tests, cutting no test to meet the cap. It repaired an EXISTING test in PRODUCTION CODE rather than in the test: `tests/ui_server/test_cockpit_contract.py::TestReadOnlyMethods::test_post_returns_405` builds a bare handler through `__new__` with no `path`, the first `do_POST` raised AttributeError on it, and the fix reads the path defensively and falls through to 405 — the fail-closed answer — leaving that file untouched and its assertion unchanged, which the reviewer confirmed by measuring the round's path set. And it MEASURED COLOUR STABILITY before committing, running the new module ten times serially at exit 0 and 36 passed, because the oversize-body test rejects on `Content-Length` without draining the socket and that is the one place this module could have raced. WHAT THE REVIEWER GOT WRONG IS REGISTERED DIRECTLY ABOVE AS R-0633 and it is the reviewer's alone: G9's stated property named the missing-bearer test among the expected failures, and the guard's own form check returns before the mutated comparison, so no run could have shown it. The worker reported the outcome it measured instead of reshaping the mutation to match the sentence, which is the whole reason the record is true.
<<<END LEDGER7

Constraints:
1. Apply the four slices BYTE FOR BYTE out of the committed C0a blob. Do not
   retype, rewrap, reflow, reindent or whitespace-adjust any of them. If a slice
   looks wrong to you, apply it as written and record the objection in the
   handback — an objection is recorded, never acted on.
2. The commit order is C0a, C0b, C1, C2, C3, C4, C5, C6 and nothing comes between
   them. C1 is the first substantive commit (checklist item 23).
3. C5 is the ONLY commit that touches `apps/` or `packages/` or `tests/`. If it
   measures 500 insertions or more when staged, SPLIT it — production code first
   with enough tests that its gate runs, the remaining tests second — and declare
   the split. Never declare an overage instead of splitting.
4. C5 is production code and this is a SPLIT round: you write it, the reviewer
   gates it. Run the AGENTS.md self-review loop before it — `git diff --stat`
   then `git diff`, read for scope drift and debug leftovers, repeat until clean.
5. THE CODE IS YOURS TO WRITE. The contract below fixes the OBSERVABLE behaviour;
   naming, decomposition and control flow are yours, within AGENTS.md's
   discoverability conventions.
6. `.remedy-wt/` is gitignored scratch. Every multi-step gate goes into a script
   there; `git status --porcelain` prints 0 lines after each commit.
7. Destructive verification — the red-proof of G10 — runs ONLY inside a
   disposable `git worktree` under `.remedy-wt/`, never in the primary checkout,
   and the worktree is removed and pruned before C6. Suite commands otherwise run
   in the PRIMARY checkout, because a fresh worktree lacks `apps/ui/node_modules`
   (R-0518).
8. Push with `git push` after C6, the last commit of this session.

The C5 contract — observable behaviour:

A. `apps/cli/command_catalog.py` gains ONE module-level name beside `CATALOG`:
   `UI_EXPOSED_COMMANDS`, a `frozenset[str]` holding exactly the two
   `command_id` values `job.stop` and `decision.resolve` (DECISION F009 D4).
   It carries the one-line WHY comment directly above it, naming that this is
   the UI write door's whole surface and that plan approval reaches it as
   `decision.resolve` with an `fp:`-prefixed decision id rather than as an id of
   its own. Add it to the `Public API::` block of the module docstring, which is
   that file's own convention for its exported names. Change NO entry of
   `CATALOG` and no other module-level name.
B. `packages/orchestration/ui_server.py` checks the submitted `command` against
   that set AFTER the credential checks and AFTER the request-shape validation,
   and BEFORE the 501 seam. Import the set INSIDE the function, matching the
   idiom this repository already uses for the same module —
   `packages/orchestration/do_run.py` line 85,
   `packages/orchestration/proof_chain.py` line 317 and
   `packages/orchestration/review_bundle.py` line 1748 each carry
   `from apps.cli.command_catalog import CATALOG` inside a function at
   `98592b72`, which the reviewer read back line by line before emitting this.
C. A command id outside the set → 400 with an `error` key and a `field` key set
   to `command` (DECISION F009 D12). The message does NOT reveal whether the id
   exists in the catalog at all; D12 rules that distinction out deliberately and
   the WHY comment says so where a reader would search.
D. An exposed command still reaches the 501 seam unchanged. Update the seam's
   WHY comment: what now blocks it is D5's effect table, not the catalog subset,
   and the round that lands that table is the one that retires the seam.
E. `tests/ui_server/test_command_channel.py` gains, at minimum: an exposed
   command reaching the seam for BOTH members of the set; a real catalog id that
   is NOT exposed — pick one that `get_command` resolves at `98592b72` — refused
   400 on field `command`; a string that is in no catalog at all refused the same
   way, with the two refusals asserted to carry the SAME message, which is what
   makes C's non-disclosure a tested property rather than a comment; the ORDER,
   that an unexposed command from a caller with a bad bearer still answers 403
   and never 400; and that every member of `UI_EXPOSED_COMMANDS` resolves
   through `get_command`, so the set cannot drift from the catalog it names.
   Keep the existing 36 tests passing unchanged.

Done when:
- G1 `.agent/STOP` ABSENT, read at Step 0 and again before C5.
  `git rev-parse --abbrev-ref HEAD` prints `feature/f009-single-write-channel` at
  every reading. `git status --porcelain` prints 0 lines after each of C0a
  through C6. Report the round base SHA you read at Step 0.
- G2 Transport EQUAL: the scratch file as received, `.agent/authored/f009-r7.md`
  at C0a and `.agent/last_block.md` at C0b all carry the same sha256, byte count
  and line count, equal to the digest in the task prompt. Write C0b from the
  COMMITTED C0a blob, never from the scratch file again.
- G3 Report, per slice, the newline-included sha256, byte count and line count;
  the COUNT of slices from your own ordered extraction out of the committed C0a
  blob; and the three aggregates — all newline-terminated, any leading blank
  line, any trailing whitespace.
- G4 `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R7. Report its line count
  against the 50-line cap; `^## Goal$` and `^## Next Steps$` each match exactly
  1 line; the first `\bF\d{3}\b` match is `F009`.
- G5 The appends at C2 and at C4 to `.agent/live_review.md`, each proved TWICE
  over independent extractors in the general N-paragraph form: (a) the previous
  blob is a byte-exact PREFIX and the remainder EQUALS a newline plus the slice,
  reported with its sha256, bytes and lines; (b) with N COUNTED BY YOUR SCRIPT
  AND REPORTED, the LAST N blank-line units of the whole file equal the slice's N
  paragraphs IN ORDER. NEGATIVE CONTROL on the FIRST appended paragraph of each:
  flip ONE printable ASCII byte and confirm BOTH readings REJECT it while both
  ACCEPT the unflipped value; report all four outcomes per append. The base for
  C2 is the round base; the base for C4 is the C2 blob.
- G6 The append at C3 to `.agent/decisions.md`, base = the round base, proved the
  same two ways with its own control and its own counted N. REPORT — do not
  predict — `^## DECISION F009 D\d+ — ` and `^## DECISION ` at the round base and
  at C3, and the DISTINCT F009 keys the file carries at C3.
- G7 Line-anchored over `.agent/live_review.md` at the round base, at C2 and at
  C4: `^- R-\d+ — ` 198, 199 and 199 with all ids DISTINCT at each;
  `^- R-0633 — ` 0, 1 and 1; `^Done: R-\d+ — ` 1 at all three; `^Landed: ` 0 at
  all three; `^> Next free id` 0 at all three; `^Gate: R\d+ — ` 6, 6 and 7 over
  that many DISTINCT keys. Report the max id at C4. Of the `Gate: ` lines at C4,
  report how many match `^Gate: R(\d+) — the R(\d+) entry\.` with the second
  numeral one less than the first, and quote to its first period any that does
  not — the expected reading is six matches and one non-match reading
  `Gate: R1 — the F008 R36 entry.` ALSO report the count item 10's rule gives at
  C4: line-anchored `^- R-\d+ — ` minus line-anchored `^Done: R-\d+ — `. State
  that value in the handback WITH the rule and the commit beside it, per DECISION
  F009 D10, and report what your script printed rather than restating it here.
- G8 The exposed set is what D4 ruled, read at C5 by IMPORTING it rather than by
  grepping: report `sorted(UI_EXPOSED_COMMANDS)`, its length, its type, and that
  every member resolves through `get_command` without raising. Report also the
  count of `CATALOG` entries at the round base and at C5 — the two must be EQUAL,
  which is the measurement that says no catalog entry was edited.
- G9 In the PRIMARY checkout at C5, run these and report each command's EXIT CODE
  and its passed-plus-skipped total, serially — never two pytest processes at
  once (R-0518, F085 R64):
    `python3 -m ruff check apps/cli/command_catalog.py packages/orchestration/ui_server.py tests/ui_server/test_command_channel.py`
    `python3 -m pytest tests/ui_server/test_command_channel.py -q -rf`
    `python3 -m pytest tests/test_command_catalog.py tests/cli/test_command_catalog.py tests/test_grouped_cli.py -q -rf`
    `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
    `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
  Every one must EXIT 0. The ruff reading is ordered as exit 0 because the
  reviewer ran that EXACT command line over those three paths at the round base,
  with this repository's own `pyproject.toml`, and it printed `All checks
  passed!` — the third path exists at the round base this round, unlike last.
  The catalog suites are ordered because C5 edits `apps/cli/command_catalog.py`,
  which they guard. Report the count your module contributes from
  `python3 -m pytest tests/ui_server/test_command_channel.py --collect-only -q`
  and NOT by regex over `-v` output (R-0611). Do not predict any total — report
  what the runs printed.
- G10 A red-proof PAIR, both halves inside ONE disposable `git worktree` under
  `.remedy-wt/` checked out at C5, the primary checkout never written to:
  (a) UNMUTATED, run `python3 -m pytest tests/ui_server/test_command_channel.py -q -rf`
      and report its exit code and totals — the control that says what the
      worktree environment does to this module before anything is broken.
  (b) MUTATED, widen the exposed-subset check so that every command id passes it
      — the smallest edit that does so — and re-run the SAME command. Report the
      exact byte string you changed, the FILE you changed it in, and its
      occurrence count IN THAT FILE at C5, which must be 1 (checklist item 25);
      if it is not 1, extend the string until it is and report the extended one.
  Report BOTH colours and, for (b), the failing node ids from the run's own `-rf`
  summary. Name NO expected test: derive nothing about WHICH tests fail, report
  the ids the run printed, and state whether (b) is RED where (a) is GREEN. That
  wording is deliberate and is R-0633's counter-measure, registered by C2 of this
  same round. Remove and prune the worktree before C6 and report
  `git worktree list`.
- G11 The range from the round base to C5: `git diff --name-only` lists EXACTLY
  the eight paths of the change set other than `.agent/handoff.md`, the set
  difference empty in both directions. Walk `git rev-list --reverse` and report,
  per commit, that it has ONE parent and its `git show --numstat` insertions,
  with `git diff --numstat` AGREEING on every cell and every cell equal to the
  `+/-` column of your handback's `## Commits` table (checklist item 28). Every
  commit stays under the 500-insertion cap of AGENTS.md DECISION F104 D1.
  `^<<<SLICE ` and `^<<<END ` read 0 lines in `.agent/plan.md`,
  `.agent/live_review.md`, `.agent/decisions.md`, `apps/cli/command_catalog.py`,
  `packages/orchestration/ui_server.py` and
  `tests/ui_server/test_command_channel.py`. Classify this round's own reflog
  entries by the operation before the first `:` in `%gs` and report `amend`,
  `rebase` and `cherry`, which must each be 0; assert no total over the whole
  reflog (R-0601). Report `git ls-files .remedy-wt` as a count.
- G12 The handback carries every mandated section of
  docs/agents/handback_template.md, an item-status table holding exactly one row
  for each of C0a, C0b, C1, C2, C3, C4, C5 and C6, the round base SHA, and one
  line per gate — the raw transcripts go in the round report, not in the handback
  (R-0582). Report its line count against the 100 that a bundle of more than five
  commits allows. Its `## Next` section states: that no `.agent/STOP` is present;
  that the next session's FIRST action is the `.agent/STOP` re-read (Phase 1
  rule 1) and its SECOND the Open PR Gate (Phase 1 rule 2), which is EMPTY
  because this branch carries no pull request and F009 opens one at its own
  closure; the open-finding count from G7 WITH item 10's rule and the commit
  named beside it; that the next free id is derived with `max` over the
  line-anchored entries and what that gives; that `.agent/candidates.md` is
  EMPTY; and that R8 is D9's rate limit as a typed `ConfigKeySpec`.

Handback:    completion report + rewrite `.agent/handoff.md`. The state block
             repeats this Fortschritt line verbatim: 30 % (T001 gebaut und auf
             den freigegebenen Katalog verengt · T002 offen · T003 offen — Limit,
             Quittung und Wirkung folgen in R8, R9 und T003) — Schätzung
──────────────────────────────────────────────────────────────
