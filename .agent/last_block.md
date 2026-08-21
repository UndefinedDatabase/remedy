── STEP T002/3 — F009 ────────────────────────────────────────
Goal:        Persist the one defect this session's last review found — a shipped
             concurrency test whose claim its own construction cannot verify —
             and record the R8 verdict, then close the session.

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 register R-0634
             · C3 the R8 verdict into the review record · C4 handback.

THE ROUND BASE is `d8d8610e1887766a935eae7a2eeb53ad5626b3ec`. Every gate reading
below said to be "at the round base" is measured against that SHA. C4's own SHA
cannot exist inside C4, so C4 is named by role and the round report carries its
value (R-0371).

THIS IS A FIFTH ROUND AGAINST A STATED FOUR-ROUND CAP, and it is declared as one
rather than slipped in. The reviewer's own red-proof of R8 measured a shipped
test 10 times with the lock it names removed and it stayed green 10 times out of
10. A finding that exists only in a session's chat is lost when that session
ends, so persisting it is worth one short round of NO new work; taking on the
next build round would not have been. NO PRODUCTION CODE IS WRITTEN and no path
under `packages/`, `apps/`, `tests/` or `docs/` is touched.

Change set — these paths and nothing else:
  `.agent/authored/f009-r9.md`
  `.agent/last_block.md`
  `.agent/plan.md`
  `.agent/live_review.md`
  `.agent/handoff.md`

Slice convention: the authored units below are delimited by `<<<SLICE <NAME>` and
`<<<END <NAME>` lines. Extract each from the COMMITTED C0a blob by those marker
lines, with a script, and apply it programmatically. The marker lines themselves
are never written into any target file.

<<<SLICE PLANF009R9
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
R9 closes this session. It registers R-0634 and records the R8 verdict, and it
writes no production code. IT IS DECLARED AS A FIFTH ROUND AGAINST A STATED
FOUR-ROUND CAP: the reviewer's own red-proof of R8 removed the lock that
`test_concurrent_callers_never_oversubscribe_one_budget` names and measured the
test green ten times out of ten, so the suite carries a thread-safety claim
nothing verifies. That finding existed only in the reviewer's session, and a
finding that is not on disk when a session ends is lost.

## Next Steps
1. R10 the nonce store and the audit record per D6, D7 and D8 — a replay returns
   the ORIGINAL body, and every refusal this door already makes, the 429
   included, becomes an audited rejection. R-0634's repair is small and belongs
   to whichever round next touches `tests/ui_server/test_command_channel.py`.
2. T003's effect table per D5 — the round that finally retires the 501 seam —
   with the plan-approval extraction landing as its own commit.
3. Then the client wiring that sends both headers, the integration gate, and
   closure.

## Risks
- The rate limiter's lock is CORRECT and is not the defect; R-0634 is about the
  test's claim, so no production change is owed and none may be made in its name.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which is
  R-0622 and routes to a paydown branch.
<<<END PLANF009R9

<<<SLICE R0634
- R-0634 — Low, A SHIPPED CONCURRENCY TEST NAMES THE LOCK IT CANNOT DETECT, SO THE SUITE CARRIES A THREAD-SAFETY CLAIM NOTHING VERIFIES. Raised by the reviewer at the R8 gate, against code that round shipped, and PROVED rather than argued. `tests/ui_server/test_command_channel.py::TestCommandRateLimiter::test_concurrent_callers_never_oversubscribe_one_budget` at `84c63d31` starts eight threads on a barrier, has each attempt ten acquisitions against a limit of twenty, and asserts exactly twenty were accepted; its docstring reads "The lock is the point: two threads must not both take the last unit." In a disposable worktree at `d8d8610e` the reviewer replaced the `with _COMMAND_RATE_LOCK:` line of `accept_command_under_rate_limit` in `packages/orchestration/ui_server.py` with `if True:` — one line, whose whole-line and indent-agnostic occurrence counts in that file are both 1 — and ran that single node ten times: EXIT 0 on all ten, against three unmutated control runs that were also EXIT 0. A test that stays green when the mechanism it names is deleted is not testing that mechanism. THE LOCK IS CORRECT AND MUST NOT BE REMOVED, and that is why this is Low rather than Medium: the critical section is a read-compare-write over a dict, CPython's interpreter switch interval is long relative to it, and the interleaving that would lose an update is simply too rare to arrive inside eighty attempts — so the property holds in practice under this interpreter and would stop holding under a shorter switch interval or a free-threaded build, which is exactly the case a test is supposed to cover and this one does not. This is the R-0438, R-0502 and R-0504 family — a check that cannot fail honestly — but it is registered separately from R-0504 because the fix is different in kind: R-0504's counter-measure is to parse the AST instead of searching text, which has no bearing on a race. FIX, for whichever round next touches that file: either force the interleaving instead of hoping for it — inject a hook into the critical section between the read and the write so the test can suspend one caller there deterministically, which turns the assertion into a real discriminator — or lower the docstring and the test name to the property actually measured, that concurrent callers do not exceed the budget under ordinary scheduling, and state in the same breath that mutual exclusion is held by inspection rather than by test. Do NOT resolve this by deleting the test: it is a reasonable smoke check, and only its claim overreaches.
<<<END R0634

<<<SLICE LEDGER9
Gate: R9 — the R8 entry. R8 PASSED. Every value the handback reported reproduced when the reviewer re-derived it from the committed blobs, the round declared no deviation and needed none, and the one defect the reviewer found is registered directly above as R-0634 against the round's own new test rather than against its conduct. TRANSPORT HELD THREE WAYS INCLUDING THE REVIEWER'S OWN COPY: `.remedy-wt/f009-r8.md` as emitted, `.agent/authored/f009-r8.md` at `48987aec` and `.agent/last_block.md` at `21f0467c` are all sha256 b646a9886af360bfed256d66fbe7ba46a0606ce08c7e37585d64ce617ba15ddd over 25972 bytes and 285 lines. THE SLICES LANDED WHOLE — PLANF009R8 3f464048/2355/41, DECISION13 3f864d99/2101/13 and LEDGER8 fa8138cf/6135/1 — and `.agent/plan.md` at `638d407c` is BYTE-EQUAL to PLANF009R8 at 41 lines under the 50-line cap. BOTH APPENDS HOLD UNDER BOTH READERS with their own counted N and their own control on the FIRST appended paragraph: DECISION13 at `efba382d` (remainder 9450fec0, 2102 bytes, N COUNTED 7 against 1116 units) and LEDGER8 at `69394fea` (remainder 73872996, 6136 bytes, N COUNTED 1 against 212 units), each LAST-N comparison holding IN ORDER and each one-byte flip REJECTED by both readers while the unflipped value is ACCEPTED by both. THE SETS HELD: `^- R-\d+ — ` 199 at the round base and at `69394fea` with all ids DISTINCT at both — the round minted no id — `^Done: R-\d+ — ` 1, `^Landed: ` 0 and `^> Next free id` 0 at both, `^Gate: R\d+ — ` 7 then 8 over that many DISTINCT keys with seven of the eight matching the n-minus-one shape, `^## DECISION F009 D\d+ — ` 12 then 13 over the DISTINCT keys D1 through D13 and `^## DECISION ` 97 then 98, and item 10's rule giving 198 open at `69394fea`. THE RANGE HOLDS: the path set from the round base to `84c63d31` is EXACTLY the eight declared paths with the set difference empty both ways, seven single-parent commits with `git show --numstat` and `git diff --numstat` AGREEING on every cell and every cell equal to the `## Commits` column, insertions 285, 176, 17, 14, 2, 355 and 63, zero marker lines in all six committed targets, eight reflog rows all `commit` with `amend`, `rebase` and `cherry` each 0, `git ls-files .remedy-wt` 0, a clean tree, and an 89-line handback under the 100 its bundle allows. THE SUITES ARE THE REVIEWER'S OWN, run in the primary checkout at `d8d8610e`: `ruff check` over the three changed paths EXITS 0 at `All checks passed!`, the command-channel and config modules together EXIT 0 at 127 passed — 64 and 63, the module's own contribution being exactly the 47 of the previous round plus 17 — the state-reader group EXITS 0 at 487 passed, which is the 470 measured at R7 plus the same 17, and the canary EXITS 0 at 42 passed. THE REVIEWER READ THE CODE FOR THE TWO FAILURES A GREEN SUITE WOULD NOT SHOW and neither is present: `get_key_spec` really exists in `packages/orchestration/config.py` at `d8d8610e`, so the mistyped-limit fallback resolves rather than raising ImportError on every request; and `_load_job` can return a `_JobPlanAdapter` rather than a core `Job`, so the new `str(job.id)` in the rate-limit call would raise on a job-flow id if that adapter had no `id` — its `__init__` sets `self.id = plan.job_id`, so both branches are safe. THE RED-PROOF IS THE REVIEWER'S OWN AND WENT WELL BEYOND THE ONE ORDERED, five mutations run one at a time in the reviewer's own disposable worktree with the source restored byte-identically after each: making the limiter admit everything fails eight tests, reproducing the worker's reading id for id; removing the expiry sweep fails the window-roll and the map-bound tests, so contract D's bound is pinned rather than merely commented; spending the budget BEFORE the subset check fails four tests including both "does not spend budget" cases, so DECISION F009 D13's placement is a tested property; and making the fingerprint return the raw token fails both fingerprint tests, so D7's non-reversibility is pinned too. THE FIFTH MUTATION IS WHY R-0634 EXISTS: removing the lock changed nothing, ten runs out of ten. THE ROUND'S THREE VOLUNTEERED NOTES WERE ALL CORRECT AND ALL WORTH THE SPACE. It declared that constraint 6 went unexercised because each test's server mints its own token and therefore its own budget, which the reviewer confirmed by reading the fixture. It declared the mistyped-limit fallback as a judgement rather than burying it, and the judgement is right: `_resolve_key` passes an uncoercible value through as a raw string, so `int()` on it would turn every command into a 500 while the typo stood, and the door must stay limited through a typo rather than fail open or fall over. And it reported that two of its seventeen new tests survive the ordered mutation, naming both and explaining why — the map-bound test and the mistyped-limit test measure properties an "admit everything" mutation does not touch — which is the R-0633 discipline being applied by a worker one round after the reviewer registered it against itself.
<<<END LEDGER9

Constraints:
1. Apply the three slices BYTE FOR BYTE out of the committed C0a blob. Do not
   retype, rewrap, reflow, reindent or whitespace-adjust any of them. If a slice
   looks wrong to you, apply it as written and record the objection in the
   handback — an objection is recorded, never acted on.
2. The commit order is C0a, C0b, C1, C2, C3, C4 and nothing comes between them.
   C1 is the first substantive commit (checklist item 23).
3. WRITE NO CODE. Touch nothing under `packages/`, `apps/`, `tests/` or `docs/`.
   R-0634 names a repair and this round does NOT perform it.
4. `.remedy-wt/` is gitignored scratch. Every multi-step gate goes into a script
   there; `git status --porcelain` prints 0 lines after each commit.
5. Push with `git push` after C4, the last commit of this session.

Done when:
- G1 `.agent/STOP` ABSENT, read at Step 0 and again before C4.
  `git rev-parse --abbrev-ref HEAD` prints `feature/f009-single-write-channel` at
  every reading. `git status --porcelain` prints 0 lines after each of C0a
  through C4. Report the round base SHA you read at Step 0.
- G2 Transport EQUAL: the scratch file as received, `.agent/authored/f009-r9.md`
  at C0a and `.agent/last_block.md` at C0b all carry the same sha256, byte count
  and line count, equal to the digest in the task prompt. Write C0b from the
  COMMITTED C0a blob, never from the scratch file again.
- G3 Report, per slice, the newline-included sha256, byte count and line count;
  the COUNT of slices from your own ordered extraction out of the committed C0a
  blob; and the three aggregates.
- G4 `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R9. Report its line count
  against the 50-line cap; `^## Goal$` and `^## Next Steps$` each match exactly
  1 line; the first `\bF\d{3}\b` match is `F009`.
- G5 The appends at C2 and at C3 to `.agent/live_review.md`, each proved TWICE
  over independent extractors in the general N-paragraph form: (a) the previous
  blob is a byte-exact PREFIX and the remainder EQUALS a newline plus the slice,
  reported with its sha256, bytes and lines; (b) with N COUNTED BY YOUR SCRIPT
  AND REPORTED, the LAST N blank-line units of the whole file equal the slice's N
  paragraphs IN ORDER. NEGATIVE CONTROL on the FIRST appended paragraph of each:
  flip ONE printable ASCII byte and confirm BOTH readings REJECT it while both
  ACCEPT the unflipped value; report all four outcomes per append. The base for
  C2 is the round base; the base for C3 is the C2 blob.
- G6 Line-anchored over `.agent/live_review.md` at the round base, at C2 and at
  C3: `^- R-\d+ — ` 199, 200 and 200 with all ids DISTINCT at each;
  `^- R-0634 — ` 0, 1 and 1; `^Done: R-\d+ — ` 1 at all three; `^Landed: ` 0 at
  all three; `^> Next free id` 0 at all three; `^Gate: R\d+ — ` 8, 8 and 9 over
  that many DISTINCT keys. Report the max id at C3. Of the `Gate: ` lines at C3,
  report how many match `^Gate: R(\d+) — the R(\d+) entry\.` with the second
  numeral one less than the first, and quote to its first period any that does
  not — the expected reading is eight matches and one non-match reading
  `Gate: R1 — the F008 R36 entry.` ALSO report the count item 10's rule gives at
  C3: line-anchored `^- R-\d+ — ` minus line-anchored `^Done: R-\d+ — `. State
  that value in the handback WITH the rule and the commit beside it, per DECISION
  F009 D10, and report what your script printed rather than restating it here.
- G7 In the PRIMARY checkout at C3, run the canary
  `python3 -m pytest tests/cli/test_golden_path.py -q -rf` and, because this
  round rewrites `.agent/` state files that the state readers parse,
  `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`.
  Run them SERIALLY, never two pytest processes at once. Both must EXIT 0.
  Report each exit code and its passed-plus-skipped total; do not predict either.
  This gate is ordered because R-0607's FIX clause requires it of any round whose
  change set holds an `.agent/` state file, and because that finding's SECOND
  instance was this feature's R5 omitting exactly these two commands.
- G8 The range from the round base to C3: `git diff --name-only` lists EXACTLY
  the four paths of the change set other than `.agent/handoff.md`, the set
  difference empty in both directions. Walk `git rev-list --reverse` and report,
  per commit, that it has ONE parent and its `git show --numstat` insertions,
  with `git diff --numstat` AGREEING on every cell and every cell equal to the
  `+/-` column of your handback's `## Commits` table (checklist item 28). Every
  commit stays under the 500-insertion cap of AGENTS.md DECISION F104 D1.
  `^<<<SLICE ` and `^<<<END ` read 0 lines in `.agent/plan.md` and
  `.agent/live_review.md`. Classify this round's own reflog entries by the
  operation before the first `:` in `%gs` and report `amend`, `rebase` and
  `cherry`, which must each be 0; assert no total over the whole reflog
  (R-0601). Report `git ls-files .remedy-wt` as a count. Report also that
  `git diff --name-only` over that range holds NO path beginning `packages/`,
  `apps/`, `tests/` or `docs/` — constraint 3, as a measurement.
- G9 The handback carries every mandated section of
  docs/agents/handback_template.md, an item-status table holding exactly one row
  for each of C0a, C0b, C1, C2, C3 and C4, the round base SHA, and one line per
  gate — the raw transcripts go in the round report, not in the handback
  (R-0582). Report its line count against the 100 that a bundle of more than five
  commits allows. Its `## Next` section states, in this order: that THIS SESSION
  ENDED AFTER A FIFTH ROUND DECLARED AGAINST ITS OWN STATED FOUR-ROUND CAP, with
  the reason; that no `.agent/STOP` is present; that the next session's FIRST
  action is the `.agent/STOP` re-read (Phase 1 rule 1) and its SECOND the Open PR
  Gate (Phase 1 rule 2), which is EMPTY because this branch carries no pull
  request and F009 opens one at its own closure; the open-finding count from G6
  WITH item 10's rule and the commit named beside it; that the next free id is
  derived with `max` over the line-anchored entries and what that gives; that
  `.agent/candidates.md` is EMPTY; that R10 is the nonce store and the audit
  record per D6, D7 and D8; and that R-0403, R-0607, R-0608, R-0609, R-0611,
  R-0613, R-0622, R-0630, R-0633 and R-0634 stay routed to a paydown branch.

Handback:    completion report + rewrite `.agent/handoff.md`. The state block
             repeats this Fortschritt line verbatim: 40 % (T001 gebaut · T002
             begonnen — Limit steht, Quittung und Wirkung folgen in R10 und
             T003) — Schätzung
──────────────────────────────────────────────────────────────
