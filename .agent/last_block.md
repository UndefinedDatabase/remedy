── STEP T002/3 — F009 ────────────────────────────────────────
Goal:        Land the NONCE half of T002 — a per-job, create-only store keyed by a
             validated client nonce, and the door's replay lookup — and close the
             record for R10: register the reviewer's own spec defect, record the
             R10 verdict, and resolve R-0634.

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 register R-0635
             · C3 the R10 verdict · C4 resolve R-0634 · C5 DECISION F009 D15
             · C6 the nonce store · C7 the door's replay lookup · C8 handback.

THE ROUND BASE is `db50d0bbaa0d94ab6d6769c12980f3e78a5e9028`. Every gate reading
below said to be "at the round base" is measured against that SHA. C8's own SHA
cannot exist inside C8, so C8 is named by role and the round report carries its
value (R-0371).

Change set — these paths and nothing else:
  `.agent/authored/f009-r11.md`
  `.agent/last_block.md`
  `.agent/plan.md`
  `.agent/live_review.md`
  `.agent/decisions.md`
  `packages/orchestration/command_nonce.py`      (new)
  `packages/orchestration/ui_server.py`
  `tests/orchestration/test_command_nonce.py`    (new)
  `tests/ui_server/test_command_channel.py`
  `.agent/handoff.md`

Slice convention: the authored units below are delimited by `<<<SLICE <NAME>` and
`<<<END <NAME>` lines. Extract each from the COMMITTED C0a blob by those marker
lines, with a script, and apply it programmatically. The marker lines themselves
are never written into any target file. Everything OUTSIDE a slice is a
specification you implement — the code below is described, not authored, and you
write it.

<<<SLICE PLANF009R11
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
R11 lands the NONCE half of T002 and closes R10's record. DECISION F009 D15 rules
where the replay lookup sits in the door's order and what may publish a record: a
new `packages/orchestration/command_nonce.py` owns the create-only per-nonce
store, the door validates the nonce as a path component and answers a replay from
the store, and PUBLICATION waits for the round that retires the 501 seam, because
a 501 is not a result worth freezing. The round also registers R-0635 against the
reviewer's own R10 spec and resolves R-0634.

## Next Steps
1. T003's effect table per D5 — the round that finally retires the 501 seam —
   which is also the round that publishes a nonce record and writes the `accepted`
   audit outcome D14 reserved. The `command.accepted` SSE event lands with it.
2. Then the client wiring that sends both headers, the route-walking 405 test and
   the import guard, the integration gate, and closure.

## Risks
- Publication and lookup land in different rounds by D15, so until T003 the
  lookup can only ever miss at the door; its tests seed the store through the
  module's own publish function rather than through a test-only path.
- A nonce becomes a FILENAME, so its character class is the guard: it reuses the
  same `_ID_RE` that already guards the job segment of that directory.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which is
  R-0622 and routes to a paydown branch.
<<<END PLANF009R11

<<<SLICE R0635
- R-0635 — Low — A REVIEWER SPEC ORDERED AN ARGUMENT WHOSE REAL BEHAVIOUR CONTRADICTED THE PROPERTY THE SAME SENTENCE DEMANDED, AND ONLY THE WORKER'S MEASUREMENT CAUGHT IT. The R10 block, committed at `6b55de93`, specified C6's audit line as serialised "with `secure_fs.json_bytes(..., indent=0)` onto one line". Those two clauses cannot both hold. Measured by the reviewer at `db50d0bb` over the shipped helper: `json_bytes(record, indent=0, sort_keys=True)` returns 8 newline bytes for the six-field record D6 fixes, because `json.dumps` with `indent=0` still breaks after every element and merely indents by zero — so every record would have carried interior newlines, `append_line_at` refuses exactly those by design, and every audit write in the round would have raised. The gate the same block ordered could not have passed. A SECOND HALF OF THE SAME DEFECT went unstated: `json_bytes` defaults to `sort_keys=True`, which alphabetises the object and would have destroyed the `ts`, `token_fp`, `command`, `args_hash`, `nonce`, `outcome` order that DECISION F009 D6 fixes and that T5_F035 and T9_F167 already plan to read. The block named a MECHANISM and not its arguments, and the mechanism's real defaults destroyed the property the specification existed to establish — the class item 18 of `docs/agents/planner_reviewer_prompt.md` already forbids, widened by R-0591 in exactly these words, and simply not run. WHY LOW: nothing false reached disk and no artifact is wrong. The worker measured `json.dumps` before writing anything, applied the stated PROPERTY — one line, D6's order — with `indent=None, sort_keys=False`, declared the objection with its measurement, and the audit record on disk is correct in both respects. The whole cost is one declared deviation, and the round is otherwise a clean pass. THIS FINDING DELIBERATELY PROPOSES NO NEW CHECKLIST ITEM, on R-0597's reasoning: item 18 is the counter-measure, it is already on disk in the widened form R-0591 gave it, and a checklist that grows an entry every time an existing entry is skipped protects nothing. FIX: none is owed in the code. The reviewer's obligation is to run item 18 against every mechanism a block names — read the argument defaults, not the intent — and this entry is the record that it was not run at R10.
<<<END R0635

<<<SLICE LEDGER11
Gate: R11 — the R10 entry. R10 PASSED. Every gate the block ordered was re-run by the reviewer and every value reproduced, the two deviations the round declared are both correct, and the one defect found is the reviewer's own and is registered directly above as R-0635. TRANSPORT AND SLICES HELD — the scratch file as emitted, `.agent/authored/f009-r10.md` at `6b55de93` and `.agent/last_block.md` at `d0e7823e` are all sha256 17a2f22543a4ac6f8d3c40d1313e5d611f20703d5bd8500788b3398125458271 over 28368 bytes and 326 lines, and the reviewer's own ordered extraction gives PLANF009R10 8db516d9/2315/41, DECISION14 cd4dd401/4205/13 and LEDGER10 db323595/3614/1. `.agent/plan.md` at `5dcbede4` is BYTE-EQUAL to PLANF009R10 at 41 lines under the 50-line cap. BOTH APPENDS HOLD BY DIRECT COMPARISON: at `728247a9` the round-base blob is a byte-exact prefix and the remainder is exactly a newline plus LEDGER10 over 3615 bytes, and at `7bd32ecd` the same holds for DECISION14 over 4206 bytes into `.agent/decisions.md`, whose line-anchored `^## DECISION F009 D\d+ — ` keys go 13 to 14, all DISTINCT. THE SETS HELD line-anchored at the round base, at `728247a9` and at `1305a9b0`: `^- R-\d+ — ` 200 at all three with every id DISTINCT, `^Done: R-\d+ — ` 1, `^> Next free id` 0, `^Landed: ` 0, 0 and 1, `^Gate: R\d+ — ` 9, 10 and 10 over that many DISTINCT keys, max id R-0634, and item 10's rule giving 199 open at `1305a9b0`. THE RANGE HELD: the path set from the round base to `1305a9b0` is exactly the twelve declared paths other than the handback's, the set difference empty both ways; twelve single-parent commits with `git show --numstat` and `git diff --numstat` AGREEING on every cell and every cell equal to the `## Commits` column, insertions 326, 254, 13, 2, 14, 10, 214, 315, 241, 64, 17 and 80, all under the 500-insertion cap; zero marker lines in the three committed state targets; twelve reflog rows all `commit` with `amend`, `rebase` and `cherry` 0 each; `git ls-files .remedy-wt` 0; and a clean tree. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout at `db50d0bb`: the three groups EXIT 0 at 106, 42 and 499 passed, each equal to the count the handback reported and none of them predicted by it, and `ruff check` EXITS 0 over all seven paths at `db50d0bb` and over the four that exist at the round base, the baseline half read through `--stdin-filename` so `per-file-ignores` resolved. THE IMPORT SET grew by exactly one module, `packages.orchestration.command_audit`, measured by AST diff over `packages/orchestration/ui_server.py` at 61 modules against 62, with nothing removed. THE R-0634 REPAIR IS A REAL DISCRIMINATOR AND THE REVIEWER PROVED IT INDEPENDENTLY, in its own disposable worktree at `db50d0bb`: the target `with _COMMAND_RATE_LOCK:` is unique in that file by whole-line, indent-agnostic and substring counting alike, and with it replaced by `if True:` the new `test_the_lock_actually_excludes_a_second_caller` FAILED 10 runs out of 10 while the old eight-thread `test_concurrent_callers_never_oversubscribe_one_budget` PASSED 10 out of 10 — the second half being R-0634 reproduced exactly, and the first being the repair doing what the old test could not. Unmutated, the new test passed 3 out of 3, and the source was restored byte-identically. THE AUDIT WIRING IS PINNED: with `audit_command_attempt` made to return False without writing, the door's suite went from 76 passed to 9 failed and 67 passed, and the nine are precisely the audit tests — one per outcome token plus the vocabulary and the raw-token tests. The reviewer's first attempt at the lock mutation used a wrongly-indented target string and therefore changed nothing; it was caught by the whole-line count reading 0 and re-run against the measured line, which is the R-0629 discipline catching the reviewer rather than the worker. BOTH DECLARED DEVIATIONS ARE CORRECT. The extra commit `b60c6393` repairs a real red: `except Exception` in C7 trips the standing AST guard `tests/orchestration/test_test_runner.py::TestNoBroadExceptAndDegradedSignals::test_no_broad_except_exception_in_dashboard`, and the replacement set is right rather than merely narrower — the reviewer confirmed at `db50d0bb` that `StopControlError` and `SecureFsError` are both `RuntimeError` subclasses, so the named tuple genuinely covers what the writer raises. The `indent=0` objection is upheld in full and is the reviewer's defect, not the round's. THE TESTS THEMSELVES WERE READ AND ARE NOT VACUOUS: the raw-token test asserts the token's absence AND that two records exist, so it cannot pass on an empty file; the D14 clause-one test asserts that no `control` directory exists at all after an unauthenticated attempt; and the swallow test asserts `calls == ["rejected_token", "rejected_csrf", "not_implemented"]` before comparing responses, which is R-0633's own rule — the mutation must reach the code — applied by the worker to its own test.
<<<END LEDGER11

<<<SLICE DONE0634
Done: R-0634 — Resolved at `1305a9b0`, and the resolution was verified by the reviewer's own mutation rather than accepted from the handback. The repair adds `tests/ui_server/test_command_channel.py::TestCommandRateLimiter::test_the_lock_actually_excludes_a_second_caller`, which turns the EXISTING `now` injection into the suspension point instead of adding a production hook: `accept_command_under_rate_limit` calls `now()` inside the critical section, so thread A's `now` runs while `_COMMAND_RATE_LOCK` is held, waits for thread B to signal that it is attempting entry — failing the test if that signal never arrives, so the check cannot pass vacuously — and then asserts B is STILL not inside after a bounded second. `packages/orchestration/ui_server.py` is unchanged by the repair, which is what the finding required: the lock was always correct and only the test's claim overreached. MEASURED BY THE REVIEWER at `db50d0bb` in a disposable worktree, with the unique line `with _COMMAND_RATE_LOCK:` replaced by `if True:`: the new test FAILED 10 runs out of 10, and unmutated it PASSED 3 out of 3. The old eight-thread test PASSED 10 out of 10 under the same mutation, which is R-0634 reproduced exactly; it is kept as the aggregate smoke check it always was, with a docstring that now names this finding instead of claiming to test the lock.
<<<END DONE0634

<<<SLICE DECISION15
## DECISION F009 D15 — the nonce record is published only by an accepted command, and a replay spends no rate budget (2026-08-22)

D8 ruled the nonce store's shape — `commands_nonce/<nonce>.json` in the job's control directory, one create-only file per nonce holding the response body that was returned, the replay window being the job's lifetime. It did not fix WHEN a record is published or WHERE the lookup sits in the door's decision order, and both are observable, so both are ruled here rather than left to the implementation.

FIRST, WHAT MAY PUBLISH. Read at `db50d0bb`, the door's last act is a 501 seam: `_handle_command_submission` authenticates, resolves, validates, checks the exposed subset and the rate limit, and then answers 501 because DECISION F009 D5's effect table does not exist yet. CHOSEN: a nonce record is published ONLY for a command that was ACCEPTED, so while the seam stands nothing publishes at the door at all, and the publish call site lands in the round that retires the seam — the same round that writes D14's reserved `accepted` audit outcome. ALTERNATIVES: (a) publish the 501 body under the nonce, so the store is exercised end to end now — rejected, and this is the whole reason the decision exists: D8's contract is that a seen nonce returns the ORIGINAL result, so a published 501 would be returned for that nonce forever, freezing a transient seam into a permanent answer for the one client that retried during it, and the bug would outlive the seam by the lifetime of the job. (b) publish at the seam but expire such records when the seam retires — rejected, it buys nothing and adds a migration to a store whose whole appeal is that it has none. THE COST IS STATED: until T003 the door's lookup can only miss, so its tests seed the store through this module's own publish function, which is production code exercised by production means rather than a test-only path.

SECOND, WHERE THE LOOKUP SITS AND WHAT IT SPENDS. CHOSEN: the lookup runs after the UI-exposed subset check and BEFORE the rate limit, and a replay that hits returns the stored body while spending NO budget. WHY NOT AFTER THE LIMIT, which would be the simpler insertion: D9's own words are "the maximum accepted commands", and a replay accepts nothing new — it returns a decision the server already made. Charging it would penalise a client for the server's own idempotency guarantee, and the client that retries after a network timeout is precisely the case a nonce exists to serve, so a limit that punished it would break the contract it sits next to. ALTERNATIVES: (a) charge a replay like any request — rejected on the argument above. (b) place the lookup first, before the credentials — rejected outright, it would answer an unauthenticated caller out of the store and turn the nonce into an oracle for other clients' responses.

THIRD, THE NONCE'S CHARACTER CLASS. It becomes a FILENAME, so it is validated before it is used: CHOSEN, `safe_points.is_safe_id`, the same `_ID_RE` that already guards the job segment of the same directory, checked in `_read_command_payload` beside the existing non-empty check. A nonce that fails it is the 400 on field `client_nonce` that shape errors already produce and is audited `rejected_shape` — so D14's closed outcome vocabulary is UNCHANGED and gains no token.

REVERSE by moving the publish call and the lookup; the store's path, shape and window come from D8 and are unchanged by this decision.
<<<END DECISION15

Constraints:
1. Apply PLANF009R11, R0635, LEDGER11, DONE0634 and DECISION15 BYTE FOR BYTE out
   of the committed C0a blob — those are the slices, and this list is what "every
   slice" means anywhere below. Do not retype, rewrap, reflow, reindent or
   whitespace-adjust any of them. If a slice looks wrong to you, apply it as
   written and record the objection in the handback — an objection is recorded,
   never acted on.
2. The commit order is C0a, C0b, C1, C2, C3, C4, C5, C6, C7, C8 and nothing comes
   between them. C1 is the first substantive commit (checklist item 23).
3. C2, C3 and C5 are APPENDS. C4 is the ONE replacement this round makes: it
   replaces the single line of `.agent/live_review.md` matching `^Landed: R-0634 — `
   with the DONE0634 slice. Locate that line BY THAT ANCHOR with a script, confirm
   it matches exactly 1 line before you touch anything, and stop if it does not.
   Nothing else in that file is edited, ever — it is an append-only record and the
   `Landed:` marker is the one exception, replaced by reviewer-authored text at the
   next gate per docs/agents/planner_reviewer_prompt.md §4 item 4.
4. C6 and C7 each carry their own tests in the same commit as the code they cover.
   The handler gains exactly one new import, the nonce module named in the change
   set, and nothing that opens a file, spawns a process or writes storage directly.
5. `.remedy-wt/` is gitignored scratch. Every multi-step gate goes into a script
   there; `git status --porcelain` prints 0 lines after each commit.
6. Push with `git push` after C8, the last commit of this round.

The code you write, by commit:

C6 — `packages/orchestration/command_nonce.py`, new. It owns D8's store and
nothing else: it decides no status code and never reads a request. Export the
directory name `commands_nonce`, the file mode `0o600`, and three functions —
`nonce_is_valid(nonce)`, which is `safe_points.is_safe_id`; `publish_nonce_result(
job_id, nonce, body, *, control_root_path=None)`, which publishes CREATE-ONLY and
returns the body that is in force afterwards; and `lookup_nonce_result(job_id,
nonce, *, control_root_path=None)`, which returns the stored body or None. Reach
the job's control directory through `safe_points.open_job_control_fd` and the
nonce subdirectory through `secure_fs.open_verified_dir`, creating it only on the
publish path. Publish with `secure_fs.write_file_atomically(..., create_only=True)`:
when it returns False another caller won the race, so READ that winner's file and
return ITS body — the loser's result never existed, which is `request_stop`'s own
idiom for the same problem and the reason D8 chose one file per nonce over a map.
An invalid nonce, a missing directory or an unreadable record is None or False,
never an exception, for the same reason the audit module raises nothing at its
callers. Say in a module docstring that PUBLICATION HAS NO DOOR CALL SITE YET and
name DECISION F009 D15 as the reason, so a reader who greps for the caller finds
the answer rather than a hole. Tests in `tests/orchestration/test_command_nonce.py`,
new, covering at least: a published body read back byte-equal; the record's 0o600
mode and its location under `commands_nonce` inside the job's control directory; a
second publish of the SAME nonce returning the FIRST body and leaving the file
unchanged; two different nonces coexisting; a lookup of an unpublished nonce
returning None; a lookup against a job with no control directory returning None;
every nonce that fails the character class refused by both functions, with
`../escape`, an empty string, a 65-character string and a slash-bearing string
among the cases; and concurrent publishers of one nonce from several threads all
receiving the SAME body.

C7 — `packages/orchestration/ui_server.py`. Two changes and no more. First, in
`_read_command_payload`, reject a `client_nonce` that fails `nonce_is_valid` with
the existing field error on `client_nonce`, beside the non-empty check that is
already there; it is the same 400 and the same audited `rejected_shape`, so D14's
vocabulary is untouched. Second, in `_handle_command_submission`, after the
UI-exposed subset check and BEFORE the rate-limit call, look the nonce up; on a
hit, send the stored body with its stored status and return, spending no budget,
and audit that replay with the outcome the ORIGINAL attempt would have carried.
Store the status alongside the body so a replay can reproduce both — a body
without its status cannot answer a replay truthfully. Add the tests to
`tests/ui_server/test_command_channel.py`: a replay of a nonce seeded through
`publish_nonce_result` returning the stored status and body BYTE-EQUAL; that same
replay leaving the rate-limit budget untouched, proved by exhausting the budget
afterwards and counting the accepted attempts; a nonce failing the character class
answering 400 on field `client_nonce` and auditing `rejected_shape`; an unseeded
nonce still reaching the 501 seam; and a replay never reaching the seam, proved by
the response rather than by inspection.

Done when:
- G1 `.agent/STOP` ABSENT, read at Step 0 and again before C8.
  `git rev-parse --abbrev-ref HEAD` prints `feature/f009-single-write-channel` at
  every reading. `git status --porcelain` prints 0 lines after each of C0a
  through C8. Report the round base SHA you read at Step 0.
- G2 Transport EQUAL: the scratch file as received, `.agent/authored/f009-r11.md`
  at C0a and `.agent/last_block.md` at C0b all carry the same sha256, byte count
  and line count, equal to the digest in the task prompt. Write C0b from the
  COMMITTED C0a blob, never from the scratch file again.
- G3 Report, per slice, the newline-included sha256, byte count and line count;
  the COUNT of slices from your own ordered extraction out of the committed C0a
  blob; and the aggregate byte count, line count and slice count over them.
- G4 `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R11. Report its line count
  against the 50-line cap; `^## Goal$` and `^## Next Steps$` each match exactly
  1 line; the first `\bF\d{3}\b` match is `F009`.
- G5 The appends at C2 and C3 to `.agent/live_review.md` and at C5 to
  `.agent/decisions.md`, each proved TWICE over independent extractors in the
  general N-paragraph form: (a) the previous blob is a byte-exact PREFIX and the
  remainder EQUALS a newline plus the slice, reported with its sha256, bytes and
  lines; (b) with N COUNTED BY YOUR SCRIPT AND REPORTED, the LAST N blank-line
  units of the whole file equal the slice's N paragraphs IN ORDER. NEGATIVE
  CONTROL on the FIRST appended paragraph of each: flip ONE printable ASCII byte
  and confirm BOTH readings REJECT it while both ACCEPT the unflipped value;
  report all four outcomes per append. The base for C2 is the round base, for C3
  the C2 blob, and for C5 the round base.
- G6 C4 is a REPLACEMENT and is proved as one, not as an append. Report, over
  `.agent/live_review.md`: `^Landed: R-0634 — ` matching exactly 1 line at C3 and
  0 lines at C4; `^Done: R-0634 — ` matching 0 lines at C3 and exactly 1 at C4;
  and that the C4 blob equals the C3 blob with that one line replaced by the
  DONE0634 slice's bytes, computed by your script as a byte comparison against a
  reconstruction rather than asserted. Report `git show --numstat` for C4, which
  is the shape of a one-line replacement and not of an append.
- G7 Line-anchored over `.agent/live_review.md` at the round base, at C2 and at
  C4: `^- R-\d+ — ` 200, 201 and 201 with all ids DISTINCT at each;
  `^- R-0635 — ` 0, 1 and 1; `^Done: R-\d+ — ` 1, 1 and 2; `^Landed: ` 1, 1 and
  0; `^> Next free id` 0 at all three. Separately, because the `Gate:` entry
  lands at C3 rather than at C2, report `^Gate: R\d+ — ` at the round base, at C3
  and at C4: 10, 11 and 11, over that many DISTINCT keys at each. Report the
  max id at C4 and the count item 10's rule gives at C4 — line-anchored
  `^- R-\d+ — ` minus line-anchored `^Done: R-\d+ — `. State that value in the
  handback WITH the rule and the commit beside it, per DECISION F009 D10, and
  report what your script printed rather than restating it here. Over
  `.agent/decisions.md` at the round base and at C5 report line-anchored
  `^## DECISION F009 D\d+ — ` 14 and 15 over that many DISTINCT keys.
- G8 The BASELINE half, per path, is
  `git show <round base>:<path> | python3 -m ruff check --stdin-filename <path> -`
  and it EXITS 0 for `packages/orchestration/ui_server.py` and
  `tests/ui_server/test_command_channel.py`. USE `--stdin-filename` AND NOTHING
  ELSE for the base reading: `pyproject.toml` carries `per-file-ignores` keyed by
  path — `"tests/**" = ["F811"]` among them — so a copy of the base blob read at
  any other path is linted under rules the file does not live under, and a copy
  written into the primary checkout is forbidden by guardrail G5 of
  docs/agents/self_drive_protocol.md. At C7 run `python3 -m ruff check` in the
  primary checkout over those two paths together with
  `packages/orchestration/command_nonce.py` and
  `tests/orchestration/test_command_nonce.py`; it must EXIT 0. The two paths the
  C7 half adds are the ones this round creates, which is why the baseline half
  cannot name them. Report both exit codes.
- G9 In the PRIMARY checkout at C7, run SERIALLY, never two pytest processes at
  once, and report each exit code and its passed-plus-skipped total without
  predicting either:
  `python3 -m pytest tests/orchestration/test_command_nonce.py tests/orchestration/test_command_audit.py tests/orchestration/test_safe_points.py -q -rf`
  then `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
  then `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`.
  All three must EXIT 0. The third is ordered because R-0607's FIX clause
  requires it of any round whose change set holds an `.agent/` state file.
- G10 PROBE, not a colour, run ONLY in a disposable worktree at C7 with the
  source restored byte-identically afterwards and the worktree removed and
  pruned. Make `lookup_nonce_result` return None unconditionally, run
  `tests/ui_server/test_command_channel.py` and
  `tests/orchestration/test_command_nonce.py`, and REPORT which node ids fail and
  how many. Then, separately and in the same manner, make
  `publish_nonce_result`'s create-only publication overwrite instead — pass
  `create_only=False` — and run `tests/orchestration/test_command_nonce.py`,
  reporting which node ids fail. Name any test that SURVIVES either mutation and
  say why it legitimately does not measure that property (R-0633).
- G11 The range from the round base to C7: `git diff --name-only` lists EXACTLY
  the paths of the change set above other than `.agent/handoff.md`, the set
  difference empty in both directions. Walk `git rev-list --reverse` and report,
  per commit, that it has ONE parent and its `git show --numstat` insertions,
  with `git diff --numstat` AGREEING on every cell and every cell equal to the
  `+/-` column of your handback's `## Commits` table (checklist item 28). Every
  commit stays under the 500-insertion cap of AGENTS.md DECISION F104 D1; a
  commit that would exceed it is SPLIT before it is made and the split is
  declared. `^<<<SLICE ` and `^<<<END ` read 0 lines in `.agent/plan.md`,
  `.agent/live_review.md` and `.agent/decisions.md`. Classify this round's own
  reflog entries by the operation before the first `:` in `%gs` and report
  `amend`, `rebase` and `cherry`, which must each be 0; assert no total over the
  whole reflog (R-0601). Report `git ls-files .remedy-wt` as a count.
- G12 The door's new import: report the module names
  `packages/orchestration/ui_server.py` imports at C7 that it did not import at
  the round base, as a set difference computed by parsing the file's AST rather
  than by grepping text, and confirm the only addition is the nonce module.
- G13 The handback carries every mandated section of
  docs/agents/handback_template.md, an item-status table holding exactly one row
  for each of C0a, C0b, C1, C2, C3, C4, C5, C6, C7 and C8, the round base SHA,
  and one line per gate — the raw transcripts go in the round report, not in the
  handback (R-0582). Report its line count against the 100 that a bundle of more
  than five commits allows, and if it exceeds that, carry the AGENTS.md DECISION
  D15 stated-cause line naming the count and the mandated content that caused it.
  Its `## Next` section states: that no `.agent/STOP` is present; that the next
  session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1) and its
  SECOND the Open PR Gate (Phase 1 rule 2), which is EMPTY because this branch
  carries no pull request and F009 opens one at its own closure; the open-finding
  count from G7 WITH item 10's rule and the commit named beside it; that the next
  free id is derived with `max` over the line-anchored entries and what that
  gives; that `.agent/candidates.md` is EMPTY; that the next round is T003's
  effect table per D5, which retires the 501 seam and is what finally publishes a
  nonce record and writes the `accepted` audit outcome; and that R-0403, R-0607,
  R-0608, R-0609, R-0611, R-0613, R-0622, R-0630, R-0633 and R-0635 stay routed
  to a paydown branch.

Handback:    completion report + rewrite `.agent/handoff.md`. The state block
             repeats this Fortschritt line verbatim: 60 % (T001 gebaut · T002
             gebaut bis auf die Publikation — T003 öffnet die Wirkung) — Schätzung
──────────────────────────────────────────────────────────────
