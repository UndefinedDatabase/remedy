── STEP T002/3 — F009 ────────────────────────────────────────
Goal:        Give the command door DECISION F009 D9's rate limit — a typed
             `ConfigKeySpec` bounding accepted commands per token fingerprint
             and job per minute, refusing the excess with 429 rather than
             waiting — with D7's fingerprint helper introduced where it is
             first used.

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 DECISION F009
             D13 · C3 the R7 verdict into the review record · C4 the config key,
             the fingerprint, the limiter and the tests · C5 handback.

THE ROUND BASE is `43b438e330f7ea0ec23f958c7a37aacd8b99fbaa`. Every gate reading
below said to be "at the round base" is measured against that SHA. C5's own SHA
cannot exist inside C5, so C5 is named by role and the round report carries its
value (R-0371).

THIS ROUND MINTS NO FINDING ID. The defect R7 surfaced — a block constraint
forbidding edits to existing tests that the same round's own change made
unsatisfiable — is already registered OPEN as R-0417, whose counter-measure (1)
reads that a zero-deletion gate may only be ordered over regions the round does
not make stale. Checklist item 30 forbids a second id for a defect the open set
already holds, so the recurrence is recorded inside the R8 verdict entry.

Change set — these paths and nothing else:
  `.agent/authored/f009-r8.md`
  `.agent/last_block.md`
  `.agent/plan.md`
  `.agent/live_review.md`
  `.agent/decisions.md`
  `packages/orchestration/config.py`
  `packages/orchestration/ui_server.py`
  `tests/ui_server/test_command_channel.py`
  `.agent/handoff.md`

Slice convention: the authored units below are delimited by `<<<SLICE <NAME>` and
`<<<END <NAME>` lines. Extract each from the COMMITTED C0a blob by those marker
lines, with a script, and apply it programmatically. The marker lines themselves
are never written into any target file.

<<<SLICE PLANF009R8
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
R8 rate-limits the door per DECISION F009 D9: a typed `ConfigKeySpec` bounds the
commands one token fingerprint may have accepted for one job per minute, and the
excess is refused with 429 rather than made to wait, because an inbound request
is holding a connection. D7's fingerprint — a truncated digest that never carries
the raw token — is introduced here, where it is first used. DECISION F009 D13
rules that the limit is consulted only for a request that would otherwise be
accepted, so a malformed or unexposed command cannot spend a client's budget.
The 429 is NOT yet audited; the audit record is D6 and lands with the nonce store.

## Next Steps
1. R9 the nonce store and the audit record per D6, D7 and D8 — a replay returns
   the ORIGINAL body, and every refusal this door already makes, the 429
   included, becomes an audited rejection.
2. T003's effect table per D5 — the round that finally retires the 501 seam —
   with the plan-approval extraction landing as its own commit.
3. Then the client wiring that sends both headers, the integration gate, and
   closure.

## Risks
- The limiter is in-process state on a threaded server, so it is read and written
  under one lock, and its bucket map must not grow without bound.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which is
  R-0622 and routes to a paydown branch.
<<<END PLANF009R8

<<<SLICE DECISION13
## DECISION F009 D13 — the rate limit is consulted only for a request that would otherwise be accepted (2026-08-21)

D9 ruled the limit a typed `ConfigKeySpec` keyed by the pair (token fingerprint, job id) and ruled that exceeding it refuses with 429, without fixing WHERE in the door's decision order the limit is consulted. That position is observable, so it is ruled rather than left to the implementation. The door's order at `43b438e3` is credentials, then job resolution, then request shape, then the UI-exposed subset, then the seam.

CHOSEN: the limit is consulted LAST, immediately before the seam, and only a request that passes every earlier check spends budget. D9's own words are "the maximum accepted commands", and this is the reading that makes them true.

WHY IT IS NOT CONSULTED EARLIER, which is the tempting alternative because an early check is cheaper: budget is spent per token fingerprint, and a client that is mid-rollout or simply buggy would otherwise lock ITSELF out of a job by sending malformed bodies — a self-inflicted denial of service produced by the guard rather than prevented by it. The cheapness argument does not survive contact with the threat model either: the fingerprint is derived from the server token, so anyone able to spend budget at all already holds the credential that grants full read access and every write this door exposes. The limit exists to bound the RATE of accepted change, not to defend the parser.

ALTERNATIVES: (a) consult it immediately after the credentials — rejected on the self-lockout argument above. (b) count every request that reaches the door regardless of outcome — rejected for the same reason, and it would make the 429 depend on traffic the client cannot see.

CONSEQUENCE FOR D6, stated here so the audit round does not have to rediscover it: a 429 is a REJECTION and is audited as one, and because the limit sits last, an audited 429 always names a command that was well formed and UI-exposed.

REVERSE by moving the call earlier in `_handle_command_submission`; the key, the window and the status do not change.
<<<END DECISION13

<<<SLICE LEDGER8
Gate: R8 — the R7 entry. R7 PASSED. Every value the handback reported reproduced when the reviewer re-derived it from the committed blobs, the reviewer ran every suite and every mutation itself, and the round's one declared deviation was correct, minimal and forced by a defect in the reviewer's own block. TRANSPORT HELD THREE WAYS INCLUDING THE REVIEWER'S OWN COPY: `.remedy-wt/f009-r7.md` as emitted, `.agent/authored/f009-r7.md` at `c7899ebc` and `.agent/last_block.md` at `95c6a799` are all sha256 0a3ded8c40ef528b99fc9b1884d4c07b6fb74cf0872cd9bbb88b8ec86418b34f over 25939 bytes and 273 lines. THE FOUR SLICES landed byte-exact — PLANF009R7 7e62f1c0/2353/40, R0633 e3b4cadf/1915/1, DECISION12 f3e51553/1598/11 and LEDGER7 21f58096/5483/1 — all newline-terminated, none with a leading blank line or trailing whitespace, and `.agent/plan.md` at `3bf7dc94` is BYTE-EQUAL to PLANF009R7 at 40 lines under the 50-line cap. ALL THREE APPENDS HOLD UNDER BOTH READERS with their own counted N and their own control on the FIRST appended paragraph: R0633 at `4be0ed50` (remainder 1d0b3a16, 1916 bytes, N COUNTED 1 against 210 units), DECISION12 at `538e86e6` (remainder e46c6e32, 1599 bytes, N COUNTED 6 against 1109 units) and LEDGER7 at `6201613c` (remainder 9883287f, 5484 bytes, N COUNTED 1 against 211 units), each LAST-N comparison holding IN ORDER and each one-byte flip REJECTED by both readers while the unflipped value is ACCEPTED by both. THE SETS MOVED AS ORDERED: `^- R-\d+ — ` 198, 199 and 199 with every id DISTINCT at each, `^- R-0633 — ` 0, 1 and 1, `^Done: R-\d+ — ` 1 throughout, `^Landed: ` and `^> Next free id` 0 throughout, `^Gate: R\d+ — ` 6, 6 and 7 over that many DISTINCT keys with six of the seven matching the n-minus-one shape and the single non-match reading `Gate: R1 — the F008 R36 entry.`, `^## DECISION F009 D\d+ — ` 12 at `538e86e6` over the DISTINCT keys D1 through D12, and item 10's rule giving 198 open at `6201613c`. THE RANGE HOLDS: the path set from the round base to `b10ef584` is EXACTLY the eight declared paths with the set difference empty both ways, eight single-parent commits with `git show --numstat` and `git diff --numstat` AGREEING on every cell and every cell equal to the `## Commits` column, insertions 273, 171, 15, 2, 12, 2, 171 and 45, zero marker lines in all six committed targets, nine reflog rows all `commit` with `amend`, `rebase` and `cherry` each 0, `git ls-files .remedy-wt` 0, a clean tree, and an 80-line handback under the 100 its bundle allows. THE EXPOSED SET IS WHAT D4 RULED, read by IMPORT rather than by grep: `sorted(UI_EXPOSED_COMMANDS)` is `['decision.resolve', 'job.stop']`, length 2, a frozenset, and both members resolve through `get_command` — `job.stop` in the `job` group and `decision.resolve` in the `decision` group, both `write_metadata`. THE CATALOG WAS NOT EDITED, and the reviewer measured the stronger property the gate asked for and then some: `len(CATALOG)` is 340 at the round base and 340 at `b10ef584`, and the ORDERED list of all 340 `command_id` values is IDENTICAL at both, so no entry was added, removed or reordered. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout at `43b438e3`: `ruff check` over the three changed paths EXITS 0 at `All checks passed!`, `tests/ui_server/test_command_channel.py` EXITS 0 at 47 passed, the catalog trio EXITS 0 at 552 passed, the state-reader group EXITS 0 at 470 passed — exactly the 459 measured at the previous round plus the 11 this one adds — and the canary EXITS 0 at 42 passed. THE RED-PROOF IS THE REVIEWER'S OWN AND WENT BEYOND THE ONE ORDERED, four mutations run one at a time in the reviewer's own disposable worktree with both files restored byte-identically after each: making the subset check accept everything fails exactly the four subset tests, which reproduces the worker's reading id for id; making it REJECT everything fails exactly the four seam tests, which is the complementary half no ordered probe asked for; and adding `job.list` to the frozenset fails four tests including the one that pins the set's exact contents, so the set cannot be widened silently. A FIFTH MUTATION INVERTED THE DECISION ORDER, refusing an unexposed command before the credentials are checked, and `test_unexposed_command_with_a_bad_bearer_is_403_and_never_400` is among the tests that then fail — so the order D12 depends on is pinned by a test rather than only by a comment. THE ROUND'S TESTS EARN A SENTENCE OF THEIR OWN because two of them assert properties rather than values: `test_the_two_refusals_are_indistinguishable` compares the FULL status-and-body pair returned for a real-but-unexposed catalog id against the pair returned for a string in no catalog, which is what makes D12's non-disclosure a measured property instead of a comment; and `test_empty_command_is_still_a_shape_error_not_a_subset_error` asserts that the two 400s carry the SAME field and DIFFERENT messages, pinning the order of shape against subset from the outside. WHAT THE REVIEWER GOT WRONG IS RECORDED HERE AND MINTS NO ID. Contract E of the R7 block, saved at `c7899ebc`, ordered the worker to "keep the existing 36 tests passing unchanged" while contract C of the SAME block made three of them unsatisfiable: `_valid_body` defaulted to `pause_job` and one test sent `resume_job`, and neither string is a `command_id` anywhere in `CATALOG`, so the subset check the round existed to add necessarily refused them. The reviewer had read that test file and had the catalog open, and never checked one against the other. That is R-0417 — a no-edit constraint ordered over a region the round's own change makes stale — whose counter-measure (1) already states the rule, so checklist item 30 forbids a second id and this paragraph is the record of its recurrence, the second in this feature after R-0607's at R6. The worker changed only the command ids those three tests carry, to `job.stop` and `decision.resolve`, left every assertion's shape and status untouched, deleted nothing, weakened nothing, and declared the whole of it before the reviewer read the diff.
<<<END LEDGER8

Constraints:
1. Apply the three slices BYTE FOR BYTE out of the committed C0a blob. Do not
   retype, rewrap, reflow, reindent or whitespace-adjust any of them. If a slice
   looks wrong to you, apply it as written and record the objection in the
   handback — an objection is recorded, never acted on.
2. The commit order is C0a, C0b, C1, C2, C3, C4, C5 and nothing comes between
   them. C1 is the first substantive commit (checklist item 23).
3. C4 is the ONLY commit that touches `packages/` or `tests/`. If it measures 500
   insertions or more when staged, SPLIT it — production code first with enough
   tests that its gate runs, the remaining tests second — and declare the split.
   Never declare an overage instead of splitting.
4. C4 is production code and this is a SPLIT round: you write it, the reviewer
   gates it. Run the AGENTS.md self-review loop before it.
5. THE CODE IS YOURS TO WRITE. The contract below fixes the OBSERVABLE behaviour;
   naming, decomposition and control flow are yours, within AGENTS.md's
   discoverability conventions.
6. YOU MAY EDIT EXISTING TESTS IN `tests/ui_server/test_command_channel.py` where
   this round's own change makes them unsatisfiable, and you must declare each
   such edit in the handback with the reason. Do not delete a test, weaken an
   assertion, or widen a bound to make a check green — R-0417's counter-measure
   is why this constraint is written this way rather than as a no-edit rule.
7. `.remedy-wt/` is gitignored scratch. Every multi-step gate goes into a script
   there; `git status --porcelain` prints 0 lines after each commit.
8. Destructive verification — the red-proof of G10 — runs ONLY inside a
   disposable `git worktree` under `.remedy-wt/`, never in the primary checkout,
   and the worktree is removed and pruned before C5. Suite commands otherwise run
   in the PRIMARY checkout (R-0518).
9. Push with `git push` after C5, the last commit of this session.

The C4 contract — observable behaviour:

A. A token fingerprint helper (DECISION F009 D7): `"tf:"` followed by the first
   sixteen hex characters of the SHA-256 of the token's UTF-8 bytes. It NEVER
   returns or logs the raw token. At the round base `packages/orchestration/
   ui_server.py` has NO module-level `hashlib` import — the only occurrence is
   `import hashlib as _hl` inside a function at line 2570 — so add the import in
   whichever form leaves `ruff check` clean, and let the `I` rules place it.
B. A `ConfigKeySpec` in `packages/orchestration/config.py`, registered in the
   same tuple the other keys live in, bounding the commands one token
   fingerprint may have accepted for one job per minute. `value_type=int`, a
   built-in default you choose and justify in the spec's `description`, and an
   `env_var` following the `REMEDY_`-prefixed convention of its neighbours. The
   description names DECISION F009 D9. Add NO other key and change no existing
   one.
C. An in-process limiter in `packages/orchestration/ui_server.py`, keyed by the
   PAIR (token fingerprint, job id), counting a fixed one-minute window and
   REFUSING the excess rather than waiting. Follow the idiom this module already
   uses for the same problem: `acquire_sse_slot` at the round base holds a
   module-level `threading.Lock` and a module-level dict, reads and writes the
   count under that one lock, and says in its docstring why. The server is
   threaded, so two requests arriving together must not both see the last unit
   of budget.
D. THE BUCKET MAP MUST NOT GROW WITHOUT BOUND. It is keyed by a pair one of whose
   halves is a per-run token and the other a job id, and the process is
   long-lived, so an entry whose window has expired is dropped rather than kept.
   Say in a comment where a reader would search how that bound is maintained.
E. The clock is INJECTED the way `_send_sse_stream` injects `now` at the round
   base, so that the window's roll is a fact a test asserts rather than a minute
   a test waits out.
F. The limit is consulted LAST, immediately before the 501 seam, and ONLY for a
   request that has passed the credentials, the job resolution, the shape
   validation and the UI-exposed subset (DECISION F009 D13). Exceeding it answers
   429. Match the body shape the door's other refusals use — the existing SSE 429
   at the round base answers `{"error": "too many streams for this job"}` — and
   carry the one-line WHY comment naming D13 and the self-lockout reason.
G. `tests/ui_server/test_command_channel.py` gains, at minimum: that the config
   key resolves through `get_config()` and reports the default you chose; that
   the Nth accepted command succeeds and the next answers 429, with the boundary
   read FROM the configured limit rather than from a literal; that a DIFFERENT
   job id has its own budget and a DIFFERENT token fingerprint has its own; that
   the window ROLLS, driven by the injected clock rather than by waiting; that a
   request refused for shape or for the subset does NOT spend budget, which is
   D13's property and the reason it is ruled; and that the fingerprint never
   contains the raw token. Keep the existing tests passing, editing only those
   this round's change makes unsatisfiable, per constraint 6.

Done when:
- G1 `.agent/STOP` ABSENT, read at Step 0 and again before C4.
  `git rev-parse --abbrev-ref HEAD` prints `feature/f009-single-write-channel` at
  every reading. `git status --porcelain` prints 0 lines after each of C0a
  through C5. Report the round base SHA you read at Step 0.
- G2 Transport EQUAL: the scratch file as received, `.agent/authored/f009-r8.md`
  at C0a and `.agent/last_block.md` at C0b all carry the same sha256, byte count
  and line count, equal to the digest in the task prompt. Write C0b from the
  COMMITTED C0a blob, never from the scratch file again.
- G3 Report, per slice, the newline-included sha256, byte count and line count;
  the COUNT of slices from your own ordered extraction out of the committed C0a
  blob; and the three aggregates.
- G4 `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R8. Report its line count
  against the 50-line cap; `^## Goal$` and `^## Next Steps$` each match exactly
  1 line; the first `\bF\d{3}\b` match is `F009`.
- G5 The append at C3 to `.agent/live_review.md`, base = the C2 blob, proved
  TWICE over independent extractors in the general N-paragraph form: (a) the
  previous blob is a byte-exact PREFIX and the remainder EQUALS a newline plus
  LEDGER8, reported with its sha256, bytes and lines; (b) with N COUNTED BY YOUR
  SCRIPT AND REPORTED, the LAST N blank-line units of the whole file equal the
  slice's N paragraphs IN ORDER. NEGATIVE CONTROL on the FIRST appended
  paragraph: flip ONE printable ASCII byte and confirm BOTH readings REJECT it
  while both ACCEPT the unflipped value; report all four outcomes.
- G6 The append at C2 to `.agent/decisions.md`, base = the round base, proved the
  same two ways with its own control and its own counted N. REPORT — do not
  predict — `^## DECISION F009 D\d+ — ` and `^## DECISION ` at the round base and
  at C2, and the DISTINCT F009 keys the file carries at C2.
- G7 Line-anchored over `.agent/live_review.md` at the round base and at C3:
  `^- R-\d+ — ` 199 at BOTH with all ids DISTINCT at both — THIS ROUND MINTS NO
  ID — `^Done: R-\d+ — ` 1 at both, `^Landed: ` 0 at both, `^> Next free id` 0 at
  both, `^Gate: R\d+ — ` 7 then 8 over that many DISTINCT keys. Report the max id
  at C3. Of the `Gate: ` lines at C3, report how many match
  `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one less than the
  first, and quote to its first period any that does not — the expected reading
  is seven matches and one non-match reading `Gate: R1 — the F008 R36 entry.`
  ALSO report the count item 10's rule gives at C3: line-anchored `^- R-\d+ — `
  minus line-anchored `^Done: R-\d+ — `. State that value in the handback WITH
  the rule and the commit beside it, per DECISION F009 D10, and report what your
  script printed rather than restating it here.
- G8 The config key, read at C4 by IMPORTING it rather than by grepping: report
  its `key`, its `env_var`, its `value_type`, its default, and the value
  `get_config().get(<key>)` returns in a process with no relevant environment
  variable set. Report the COUNT of registered key specs at the round base and at
  C4 — the second must be exactly one more than the first — and that every other
  spec's `key` is unchanged, as a set difference in both directions.
- G9 In the PRIMARY checkout at C4, run these and report each command's EXIT CODE
  and its passed-plus-skipped total, serially — never two pytest processes at
  once (R-0518, F085 R64):
    `python3 -m ruff check packages/orchestration/config.py packages/orchestration/ui_server.py tests/ui_server/test_command_channel.py`
    `python3 -m pytest tests/ui_server/test_command_channel.py -q -rf`
    `python3 -m pytest tests/orchestration/test_config.py -q -rf`
    `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
    `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
  Every one must EXIT 0. The reviewer ran the ruff command line above over those
  three paths at the round base, with this repository's own `pyproject.toml`, and
  it printed `All checks passed!`; `tests/orchestration/test_config.py` EXITS 0 at
  63 passed at the round base, measured by the reviewer, and is ordered because C4
  edits the module it covers. Report your module's contribution from
  `python3 -m pytest tests/ui_server/test_command_channel.py --collect-only -q`
  and NOT by regex over `-v` output (R-0611). Do not predict any total.
- G10 A red-proof PAIR, both halves inside ONE disposable `git worktree` under
  `.remedy-wt/` checked out at C4, the primary checkout never written to:
  (a) UNMUTATED, run `python3 -m pytest tests/ui_server/test_command_channel.py -q -rf`
      and report its exit code and totals.
  (b) MUTATED, make the limiter admit every request — the smallest edit that does
      so — and re-run the SAME command. Report the exact byte string you changed,
      the FILE you changed it in, and its occurrence count IN THAT FILE at C4,
      which must be 1 (checklist item 25); if it is not 1, extend the string until
      it is and report the extended one.
  Report BOTH colours and, for (b), the failing node ids from the run's own `-rf`
  summary. Name NO expected test: report the ids the run printed and state
  whether (b) is RED where (a) is GREEN (R-0633). Remove and prune the worktree
  before C5 and report `git worktree list`.
- G11 The range from the round base to C4: `git diff --name-only` lists EXACTLY
  the eight paths of the change set other than `.agent/handoff.md`, the set
  difference empty in both directions. Walk `git rev-list --reverse` and report,
  per commit, that it has ONE parent and its `git show --numstat` insertions,
  with `git diff --numstat` AGREEING on every cell and every cell equal to the
  `+/-` column of your handback's `## Commits` table (checklist item 28). Every
  commit stays under the 500-insertion cap of AGENTS.md DECISION F104 D1.
  `^<<<SLICE ` and `^<<<END ` read 0 lines in `.agent/plan.md`,
  `.agent/live_review.md`, `.agent/decisions.md`,
  `packages/orchestration/config.py`, `packages/orchestration/ui_server.py` and
  `tests/ui_server/test_command_channel.py`. Classify this round's own reflog
  entries by the operation before the first `:` in `%gs` and report `amend`,
  `rebase` and `cherry`, which must each be 0; assert no total over the whole
  reflog (R-0601). Report `git ls-files .remedy-wt` as a count.
- G12 The handback carries every mandated section of
  docs/agents/handback_template.md, an item-status table holding exactly one row
  for each of C0a, C0b, C1, C2, C3, C4 and C5, the round base SHA, and one line
  per gate — the raw transcripts go in the round report, not in the handback
  (R-0582). Report its line count against the 100 that a bundle of more than five
  commits allows. Its `## Next` section states: that no `.agent/STOP` is present;
  that the next session's FIRST action is the `.agent/STOP` re-read (Phase 1
  rule 1) and its SECOND the Open PR Gate (Phase 1 rule 2), which is EMPTY
  because this branch carries no pull request and F009 opens one at its own
  closure; the open-finding count from G7 WITH item 10's rule and the commit
  named beside it; that the next free id is derived with `max` over the
  line-anchored entries and what that gives; that `.agent/candidates.md` is
  EMPTY; and that R9 is the nonce store and the audit record per D6, D7 and D8.

Handback:    completion report + rewrite `.agent/handoff.md`. The state block
             repeats this Fortschritt line verbatim: 40 % (T001 gebaut · T002
             begonnen — Limit steht, Quittung und Wirkung folgen in R9 und
             T003) — Schätzung
──────────────────────────────────────────────────────────────
