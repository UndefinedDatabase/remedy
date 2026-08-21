── STEP T002/3 — F009 ────────────────────────────────────────
Goal:        Land the AUDIT half of T002 — every attempt this door already
             refuses becomes a per-job audited rejection, written through an
             append-only line writer this repository does not yet have — and
             repair R-0634 in the test file this round is already touching.

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R9 verdict
             · C3 DECISION F009 D14 · C4 the control-fd rename · C5 the
             secure_fs append writer · C6 the command_audit module · C7 the
             door wiring · C8 the R-0634 repair · C9 handback.

THE ROUND BASE is `f7f43edf82974ea5ac999c0285358f56be94822f`. Every gate reading
below said to be "at the round base" is measured against that SHA. C9's own SHA
cannot exist inside C9, so C9 is named by role and the round report carries its
value (R-0371).

WHY THIS ROUND IS THE AUDIT ONLY, where `.agent/plan.md` at the round base named
the nonce store and the audit record together: the two together need a shared
module, a new secure_fs primitive, a nonce character class, create-only
publication and a replay path, and the commit sequence below is already at the
top of the bundle range without any of the nonce half. The nonce store is R11 and
nothing about D8 changes. R-0634's repair is HERE rather than deferred because
the round base's plan routes it to whichever round next touches
`tests/ui_server/test_command_channel.py`, and C7 touches it.

Change set — these paths and nothing else:
  `.agent/authored/f009-r10.md`
  `.agent/last_block.md`
  `.agent/plan.md`
  `.agent/live_review.md`
  `.agent/decisions.md`
  `packages/common/secure_fs.py`
  `packages/orchestration/safe_points.py`
  `packages/orchestration/command_audit.py`      (new)
  `packages/orchestration/ui_server.py`
  `tests/orchestration/test_secure_fs.py`        (new)
  `tests/orchestration/test_command_audit.py`    (new)
  `tests/ui_server/test_command_channel.py`
  `.agent/handoff.md`

Slice convention: the authored units below are delimited by `<<<SLICE <NAME>` and
`<<<END <NAME>` lines. Extract each from the COMMITTED C0a blob by those marker
lines, with a script, and apply it programmatically. The marker lines themselves
are never written into any target file. Everything OUTSIDE a slice is a
specification you implement — the code below is described, not authored, and you
write it.

<<<SLICE PLANF009R10
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
R10 lands the AUDIT half of T002 and leaves the nonce store to R11. DECISION F009
D14 rules the three halves D6 left open, `packages/common/secure_fs.py` gains the
append-only line writer this repository does not have, a new
`packages/orchestration/command_audit.py` writes the per-job record, and every
refusal the door already makes becomes an audited rejection. The round also
repairs R-0634 in the test file it is already touching.

## Next Steps
1. R11 the nonce store per D8 — create-only publication, a validated nonce
   character class, and a replay that returns the ORIGINAL body. Whether a replay
   spends rate budget is open and is ruled by that round.
2. T003's effect table per D5 — the round that finally retires the 501 seam —
   with the plan-approval extraction landing as its own commit.
3. Then the client wiring that sends both headers, the integration gate, and
   closure.

## Risks
- An audit write that fails must never turn a refusal into a 500; D14 rules that
  a failed write leaves the response it was recording unchanged.
- The audit runs before the job's control directory is known to exist, so the
  pre-credential path must never CREATE one — D14 rules that half too.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which is
  R-0622 and routes to a paydown branch.
<<<END PLANF009R10

<<<SLICE DECISION14
## DECISION F009 D14 — what an audited attempt requires, and the three fields D6 left unfixed (2026-08-21)

D6 ruled the audit record's path, its mode, its append-only shape and its field ORDER — `ts`, `token_fp`, `command`, `args_hash`, `nonce`, `outcome` — and ruled that every attempt is audited rather than only accepted ones. Building it surfaced three halves that ruling does not fix and one ordering hazard it cannot have foreseen, and two later features already plan to READ this file, so they are ruled here rather than left to the implementation.

FIRST, WHICH ATTEMPTS REACH A RECORD AT ALL. Read at `f7f43edf`, and the round that carries this decision changes neither half: `_handle_command_submission` decides credentials BEFORE it resolves the job, deliberately, so an unauthenticated caller never learns which jobs exist. A record is per job and lives in `job_control_dir(job_id)`, so auditing a refusal that happened before the job resolved means reaching that directory on behalf of a caller who has presented nothing. CHOSEN: an attempt whose bearer or CSRF check failed is audited ONLY into a job control directory that ALREADY EXISTS, opened with `create=False`, and writes nothing at all when it does not; an attempt that has passed both credential checks is audited with `create=True`. The check ORDER does not change and neither does any status code. ALTERNATIVES: (a) resolve the job before the credentials so every rejection can be audited — rejected, it hands an unauthenticated caller a job-existence oracle through the 404-versus-403 split, which is the property the current order exists to protect. (b) audit pre-credential refusals with `create=True` — rejected, it lets an unauthenticated caller create an arbitrary control directory per request, which is litter an attacker steers and a resource this door must not spend on a caller it has already refused. The cost is stated plainly rather than hidden: a wrong-credential attempt against a job that has never had a control directory leaves no record, and the Acceptance line "wrong or missing auth is audited as rejected" is met for every job the cockpit has actually operated on and not for one it has not.

SECOND, THE `args_hash` FORMAT. CHOSEN: `"ah:" + sha256(secure_fs.json_bytes(args)).hexdigest()[:16]`, the prefix matching `token_fp`'s `tf:` so a reader can tell the two digests apart on a line, and `json_bytes` because it already sorts keys, which is what makes the hash stable across two clients that spell the same object in different orders. The raw `args` are NEVER written: they are client-supplied and may name paths or ids that the redaction denylist would have to reason about, and the hash answers the only question this record needs to answer, which is whether two attempts carried the same arguments.

THIRD, THE `outcome` VOCABULARY, which is the field the two reading features consume. CHOSEN: a closed set of lowercase tokens — `rejected_token`, `rejected_csrf`, `rejected_job`, `rejected_shape`, `rejected_command`, `rejected_rate`, and `not_implemented` for the 501 that the seam at the end of that same function answers at `f7f43edf`. `accepted` is reserved and is written by the round that retires the seam, because nothing is accepted while a 501 stands and a record claiming otherwise would be false. Every token names the CHECK that refused, never the client's message, so the vocabulary cannot drift with a wording change.

FOURTH, WHAT A FAILED AUDIT WRITE DOES. CHOSEN: for a REJECTION it changes nothing — the refusal the door had already decided is sent unchanged, and the exception is swallowed at the call site rather than propagating, because turning a 403 into a 500 would let a full disk convert a correctly-refused attempt into a server fault. The accepted case is deliberately NOT ruled here: nothing is accepted until the seam is retired, and whether a command may take effect when its audit record cannot be written is a question about effects, which the round that lands the effect table answers with the effects in front of it.

REVERSE by deleting the audit call sites; the record's path, mode and field order come from D6 and are unchanged by this decision.
<<<END DECISION14

<<<SLICE LEDGER10
Gate: R10 — the R9 entry. R9 PASSED. Every value that handback reported was re-derived by the reviewer from the committed blobs and every one of them reproduced: the round is a clean pass with no finding of its own and no deviation. TRANSPORT AND SLICES HELD — `.agent/authored/f009-r9.md` at `e0136413` and `.agent/last_block.md` at `f59c6a78` are both sha256 d04b283d875d177c5f17cceeb9acc73712494f3c9273ea6d404c4c2ffb7f45d7 over 18788 bytes and 179 lines, equal to the digest the prompt named, and the reviewer's own ordered extraction out of the committed C0a blob yields the three slices PLANF009R9 78e4afdb/2359/41, R0634 ad565aa7/2555/1 and LEDGER9 e60d199d/5042/1. `.agent/plan.md` at `9d6b004a` is BYTE-EQUAL to PLANF009R9 at 41 lines under the 50-line cap, with `^## Goal$` and `^## Next Steps$` matching exactly one line each and `F009` the first F-id. BOTH APPENDS HOLD BY DIRECT COMPARISON, which is stronger than the two readers the block ordered: at `7524e76b` the round-base blob is a byte-exact prefix and the remainder is exactly a newline plus R0634 at af804c0b over 2556 bytes, and at `84164cf8` the `7524e76b` blob is a byte-exact prefix and the remainder is exactly a newline plus LEDGER9 at 42636ef3 over 5043 bytes. THE SETS HELD line-anchored at the round base, at `7524e76b` and at `84164cf8`: `^- R-\d+ — ` 199, 200 and 200 with every id DISTINCT at each, `^- R-0634 — ` 0, 1 and 1, `^Done: R-\d+ — ` 1, `^Landed: ` 0 and `^> Next free id` 0 at all three, `^Gate: R\d+ — ` 8, 8 and 9 over that many DISTINCT keys, max id R-0634, and eight of the nine `Gate: ` lines matching the n-minus-one shape with the single non-match reading `Gate: R1 — the F008 R36 entry.` — the same reading the handback reported. Item 10's rule gives 199 open at `84164cf8`. THE RANGE HELD: the path set from the round base to `84164cf8` is exactly `.agent/authored/f009-r9.md`, `.agent/last_block.md`, `.agent/live_review.md` and `.agent/plan.md` with the set difference empty both ways and no path under `packages/`, `apps/`, `tests/` or `docs/`; six single-parent commits with `git show --numstat` and `git diff --numstat` agreeing on every cell and every cell equal to the `## Commits` column, insertions 179, 99, 12, 2, 2 and 27, all under the 500-insertion cap; zero `^<<<SLICE ` and `^<<<END ` lines in both committed targets; `git ls-files .remedy-wt` 0; a clean tree; and a 78-line handback under the 100 its bundle allows. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout at `f7f43edf`: the canary `tests/cli/test_golden_path.py` EXITS 0 at 42 passed and the state-reader group EXITS 0 at 487 passed, both equal to the counts the handback reported and neither predicted by it. THE HANDBACK'S ONE ARITHMETIC ASYMMETRY IS CORRECT AND IS NOT A FINDING: it reports five reflog rows and five insertion counts where the reviewer measures six of each, because the sixth is the handback commit itself, whose own row cannot exist while its text is being written — the item 14 carve-out of docs/agents/planner_reviewer_prompt.md, honestly applied rather than papered over. THE REVIEWER ALSO RE-MEASURED THE TWO CLAIMS R-0634 ITSELF RESTS ON, since a finding is a permanent record: the mutation target `with _COMMAND_RATE_LOCK:` occurs exactly once in `packages/orchestration/ui_server.py` at `d8d8610e` by whole-line, indent-agnostic and substring counting alike, so the red control named a unique line; and neither authored slice carries an unquoted `HEAD`, measured after deleting every backtick-quoted span, which is the R-0586 scan the record now requires of itself.
<<<END LEDGER10

Constraints:
1. Apply PLANF009R10, DECISION14 and LEDGER10 BYTE FOR BYTE out of the committed
   C0a blob — those are the slices, and this list is what "every slice" means
   anywhere below. Do not
   retype, rewrap, reflow, reindent or whitespace-adjust any of them. If a slice
   looks wrong to you, apply it as written and record the objection in the
   handback — an objection is recorded, never acted on.
2. The commit order is C0a, C0b, C1, C2, C3, C4, C5, C6, C7, C8, C9 and nothing
   comes between them. C1 is the first substantive commit (checklist item 23).
3. C4 is a PURE RENAME and changes no behaviour. C5, C6, C7 and C8 each carry
   their own tests in the same commit as the code they cover.
4. The handler may not gain an import of anything that opens a file, spawns a
   process or writes storage directly. The audit writer is the one new import the
   door takes, and it is the module named in the change set.
5. `.remedy-wt/` is gitignored scratch. Every multi-step gate goes into a script
   there; `git status --porcelain` prints 0 lines after each commit.
6. Push with `git push` after C9, the last commit of this round.

The code you write, by commit:

C4 — `packages/orchestration/safe_points.py`. Rename `_open_job_control_fd` to
`open_job_control_fd`, a public name, and update its call sites in that file. It
is the verified-directory-handle helper the audit writer needs and nothing
outside that file references it today. Give it the one-line WHY comment directly
above the definition that AGENTS.md's discoverability rules ask for, naming that
it is the shared way into a job's private control directory. Change nothing else
about it — not its signature, not its body, not its docstring.

C5 — `packages/common/secure_fs.py`. Add `append_line_at(dir_fd, name, line, *,
file_mode=0o600, error_cls=SecureFsError, noun="line")` and register it in
`__all__`. It appends ONE line to `name` through the held directory fd, opening
with `O_WRONLY | O_CREAT | O_APPEND | O_NOFOLLOW` at `file_mode`, and it exists
because this repository has no append writer at all: `write_file_atomically`
writes a whole file and an audit log is append-only by construction. It requires
`line` to be bytes ending in exactly one newline with no other newline in it, and
it bounds the length — a JSONL record is one line and a caller handing it two is
a bug, not a stream. It performs a SINGLE `os.write` and treats a short write as
an error rather than looping: under `O_APPEND` one write is what the kernel
places atomically at the end, and a loop is precisely what would interleave two
concurrent writers mid-record. Say that in the docstring, because it is the
reason the obvious loop is absent. `fsync` before close. Its tests go in
`tests/orchestration/test_secure_fs.py`, a new module named for the source it
covers, and they cover at least: two records appended in order; the file created
at the requested mode; a line without a trailing newline refused; a line
containing an interior newline refused; an oversize line refused; a symlink at
`name` refused rather than followed; and concurrent appenders from several
threads each landing exactly one intact line.

C6 — `packages/orchestration/command_audit.py`, new. It owns the record D6 ruled
and nothing else. Export the filename constant, the record's field order, and
`audit_command_attempt(job_id, *, token_fp, command, args, nonce, outcome,
create=..., control_root_path=None) -> bool`, returning whether a record was
written. It resolves the job's control directory through the C4 helper, builds
the object with `ts` from `safe_points.utc_now_iso()` and the remaining fields
exactly as D6 orders them, serialises with `secure_fs.json_bytes(..., indent=0)`
onto one line, and appends through C5's writer at `0o600`. `args_hash` is
computed as D14 rules; `token_fp` arrives from the caller already fingerprinted
and this module never sees a raw token — say so in a comment where a reader would
look for the fingerprinting. With `create=False` and no such directory it writes
nothing and returns False. A `job_id` that does not validate writes nothing and
returns False rather than raising, so the door never has to pre-validate. `nonce`
may be absent and is written as an empty string then. Tests in
`tests/orchestration/test_command_audit.py`, new, covering at least: a record's
field ORDER on the line as written; the file's 0o600 mode and its location under
the job's control directory; two attempts appending two lines; `create=False`
against a missing directory writing nothing and returning False; `create=True`
making the directory; a job id that does not validate writing nothing and
returning False; the raw token and the raw args values appearing NOWHERE in the
file's bytes; and equal args hashing equal while different args hash differently.

C7 — `packages/orchestration/ui_server.py`. Wire `_handle_command_submission` so
each refusal writes its record before its response is sent, with the outcome
token D14 fixes for that check: the bearer failure and the CSRF failure with
`create=False`, and the job-resolution failure, the shape failure, the
unexposed-command failure, the rate-limit failure and the 501 seam with
`create=True`. The two pre-credential calls pass the job id STRING from the path.
Every call site swallows the writer's exceptions per D14's fourth clause and the
response is unchanged in every case. Add the tests to
`tests/ui_server/test_command_channel.py`: at minimum one per outcome token above
asserting the token and the command that landed, one asserting a wrong-credential
attempt against a job with no control directory leaves no file and still answers
403, one asserting the raw token never appears in the audit file after a rejected
attempt, and one asserting that an audit writer raising leaves the door's status
code and body exactly as they are without it.

C8 — the R-0634 repair, in `tests/ui_server/test_command_channel.py`, plus its
`Landed:` line. That finding records that
`TestCommandRateLimiter::test_concurrent_callers_never_oversubscribe_one_budget`
names a lock its construction cannot detect: with the lock removed the test was
green ten times out of ten. Repair it by making the EXISTING `now` injection the
suspension point rather than adding a production hook — the function
`accept_command_under_rate_limit` calls `now()` inside the critical section, so a
`now` that blocks there holds the lock while a second thread attempts entry. The
shape: thread A enters with a `now` that sets an "inside" flag, waits a bounded
time for B's "entered" flag and then returns a moment; thread B sets an
"attempting" flag and calls the function. A first waits for B's "attempting" flag
and FAILS if it never arrives, so the test cannot pass vacuously; it then asserts
B's "entered" flag is still unset after the bounded wait, which is mutual
exclusion observed rather than hoped for. Use one second for the bounded wait and
say in a comment why a second is the right order of magnitude: an unlocked B
enters in microseconds, so the gap between the two outcomes is six orders of
magnitude and not a race. Keep the existing eight-thread oversubscription test as
the smoke check it is, and correct its docstring so it no longer claims to be
testing the lock. In the same commit append to `.agent/live_review.md` exactly
one line beginning `Landed: R-0634 — ` naming what changed and the C8 commit;
write no `Done:` paragraph, which is reserved for reviewer-authored text.

Done when:
- G1 `.agent/STOP` ABSENT, read at Step 0 and again before C9.
  `git rev-parse --abbrev-ref HEAD` prints `feature/f009-single-write-channel` at
  every reading. `git status --porcelain` prints 0 lines after each of C0a
  through C9. Report the round base SHA you read at Step 0.
- G2 Transport EQUAL: the scratch file as received, `.agent/authored/f009-r10.md`
  at C0a and `.agent/last_block.md` at C0b all carry the same sha256, byte count
  and line count, equal to the digest in the task prompt. Write C0b from the
  COMMITTED C0a blob, never from the scratch file again.
- G3 Report, per slice, the newline-included sha256, byte count and line count;
  the COUNT of slices from your own ordered extraction out of the committed C0a
  blob; and the aggregate byte count, line count and slice count over them.
- G4 `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R10. Report its line count
  against the 50-line cap; `^## Goal$` and `^## Next Steps$` each match exactly
  1 line; the first `\bF\d{3}\b` match is `F009`.
- G5 The append at C2 to `.agent/live_review.md` and the append at C3 to
  `.agent/decisions.md`, each proved TWICE over independent extractors in the
  general N-paragraph form: (a) the previous blob is a byte-exact PREFIX and the
  remainder EQUALS a newline plus the slice, reported with its sha256, bytes and
  lines; (b) with N COUNTED BY YOUR SCRIPT AND REPORTED, the LAST N blank-line
  units of the whole file equal the slice's N paragraphs IN ORDER. NEGATIVE
  CONTROL on the FIRST appended paragraph of each: flip ONE printable ASCII byte
  and confirm BOTH readings REJECT it while both ACCEPT the unflipped value;
  report all four outcomes per append. The base for C2 is the round base; the
  base for C3 is the round base.
- G6 Line-anchored over `.agent/live_review.md` at the round base, at C2 and at
  C8: `^- R-\d+ — ` 200 at all three with all ids DISTINCT at each;
  `^Done: R-\d+ — ` 1 at all three; `^> Next free id` 0 at all three;
  `^Landed: ` 0, 0 and 1; `^Gate: R\d+ — ` 9, 10 and 10 over that many DISTINCT
  keys. Report the max id at C8 and the count item 10's rule gives at C8 —
  line-anchored `^- R-\d+ — ` minus line-anchored `^Done: R-\d+ — `. State that
  value in the handback WITH the rule and the commit beside it, per DECISION F009
  D10, and report what your script printed rather than restating it here. Over
  `.agent/decisions.md` at the round base and at C3 report line-anchored
  `^## DECISION F009 D\d+ — ` 13 and 14 over that many DISTINCT keys.
- G7 The BASELINE half, per path, is
  `git show <round base>:<path> | python3 -m ruff check --stdin-filename <path> -`
  and it EXITS 0 for `packages/common/secure_fs.py`,
  `packages/orchestration/safe_points.py`, `packages/orchestration/ui_server.py`
  and `tests/ui_server/test_command_channel.py`. USE `--stdin-filename` AND
  NOTHING ELSE for the base reading: `pyproject.toml` carries
  `per-file-ignores` keyed by path — `"tests/**" = ["F811"]` among them — so a
  copy of the base blob read at any other path is linted under rules the file
  does not live under, and a copy written into the primary checkout is forbidden
  outright by guardrail G5 of docs/agents/self_drive_protocol.md. At C8 run
  `python3 -m ruff check` in the primary checkout over those same paths together
  with `packages/orchestration/command_audit.py`,
  `tests/orchestration/test_secure_fs.py` and
  `tests/orchestration/test_command_audit.py`; it must EXIT 0. The three paths
  the C8 half adds are the ones this round creates, which is why the baseline
  half cannot name them. Report both exit codes.
- G8 In the PRIMARY checkout at C8, run SERIALLY, never two pytest processes at
  once, and report each exit code and its passed-plus-skipped total without
  predicting either:
  `python3 -m pytest tests/orchestration/test_secure_fs.py tests/orchestration/test_command_audit.py tests/orchestration/test_safe_points.py -q -rf`
  then `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
  then `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`.
  All three must EXIT 0. The third is ordered because R-0607's FIX clause
  requires it of any round whose change set holds an `.agent/` state file.
- G9 PROBE, not a colour, run ONLY in a disposable worktree at C8 with the source
  restored afterwards: make `audit_command_attempt` return False without writing
  anything, run `tests/ui_server/test_command_channel.py`, and REPORT which node
  ids fail and how many. Then separately, in the same manner, replace the
  `with _COMMAND_RATE_LOCK:` line of `accept_command_under_rate_limit` in
  `packages/orchestration/ui_server.py` with `if True:` — at C8 that exact line
  must occur exactly once in that file by whole-line, indent-agnostic and
  substring counting, so REPORT all three counts before mutating and STOP if any
  is not 1 — and run `tests/ui_server/test_command_channel.py` TEN times,
  reporting the exit code of each run and the node ids that failed. The R-0634
  repair is what these ten runs measure: report the outcome as counts and ids,
  and do not restate an expected colour here.
- G10 The range from the round base to C8: `git diff --name-only` lists EXACTLY
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
- G11 The door's new import: report the module names
  `packages/orchestration/ui_server.py` imports at C8 that it did not import at
  the round base, as a set difference computed by parsing the file's AST rather
  than by grepping text, and confirm the only addition is the audit module.
- G12 The handback carries every mandated section of
  docs/agents/handback_template.md, an item-status table holding exactly one row
  for each of C0a, C0b, C1, C2, C3, C4, C5, C6, C7, C8 and C9, the round base
  SHA, and one line per gate — the raw transcripts go in the round report, not in
  the handback (R-0582). Report its line count against the 100 that a bundle of
  more than five commits allows. Its `## Next` section states: that no
  `.agent/STOP` is present; that the next session's FIRST action is the
  `.agent/STOP` re-read (Phase 1 rule 1) and its SECOND the Open PR Gate (Phase 1
  rule 2), which is EMPTY because this branch carries no pull request and F009
  opens one at its own closure; the open-finding count from G6 WITH item 10's
  rule and the commit named beside it; that the next free id is derived with
  `max` over the line-anchored entries and what that gives; that
  `.agent/candidates.md` is EMPTY; that R11 is the nonce store per D8; and that
  R-0403, R-0607, R-0608, R-0609, R-0611, R-0613, R-0622, R-0630 and R-0633 stay
  routed to a paydown branch.

Handback:    completion report + rewrite `.agent/handoff.md`. The state block
             repeats this Fortschritt line verbatim: 50 % (T001 gebaut · T002
             zur Hälfte — Quittung steht, Nonce folgt in R11) — Schätzung
──────────────────────────────────────────────────────────────
