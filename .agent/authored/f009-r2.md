── STEP R2/2 — F009 The single write channel ────────────────────────
Goal:        Record the R1 verdict, then INVENTORY the ground F009 builds on —
             the command catalog, the UI server's current authentication, each
             effect backend, the event-append seam and the test layout — every
             answer MEASURED in the source and carried as a `path:line` citation
             rather than read off the feature file. No production code is written
             this round and no behaviour changes.

Bundle:      C0a save the block · C0b mirror the block · C1 the plan ·
             C2 the R1 verdict in the review record · C3 the inventory ·
             C4 the handback.

Change set:  `.agent/authored/f009-r2.md`, `.agent/last_block.md`,
             `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/f009_inventory.md`, `.agent/handoff.md`. Nothing else. No
             path under `packages/`, `apps/`, `tests/`, `docs/` or
             `docs/roadmap/` is edited this round — this round only READS them.

## Step 0 — before any commit
    ls -la .agent/STOP
    git rev-parse --abbrev-ref HEAD
    git status --porcelain
    git rev-parse HEAD

`.agent/STOP` MUST be absent; if it exists, stop, write the handoff and end. The
branch MUST already be `feature/f009-single-write-channel` — do NOT create a
branch and do NOT run an Open PR Gate this round: this branch carries no pull
request and F009 opens one at its own closure. The SHA that `git rev-parse HEAD`
prints is the ROUND BASE, and it is `87ad9e5c` unless something has moved; report
the value you read.

## Transport
This block lives at `.remedy-wt/f009-r2.md`. Its sha256, byte count and line
count are stated in the task prompt that handed you that path — a file cannot
carry its own digest, so the digest travels beside it. Verify it BEFORE using any
byte of it. Save it byte for byte as `.agent/authored/f009-r2.md` (C0a), then
mirror it to `.agent/last_block.md` (C0b) FROM THE COMMITTED C0a BLOB —
`git show <C0a>:.agent/authored/f009-r2.md` — never from this file again and
never by retyping.

## Slice convention
The authored units below are delimited by one-line markers, `<<<SLICE <NAME>`
opening and `<<<END <NAME>` closing. Extract every slice from the COMMITTED C0a
BLOB by its marker lines with a script, never from this message and never by
hand. The marker lines are NOT part of any slice. Every slice is
newline-terminated, none begins with a blank line, and none carries trailing
whitespace on any line — report those three readings as your script measured
them. Marker lines never reach a target file.

## C1 — the plan, the first substantive commit
Apply PLANF009R2 as the WHOLE file.

<<<SLICE PLANF009R2
# Plan — F009 The single write channel

Branch: feature/f009-single-write-channel, cut from `main` at `ce49348b`, the
merge commit of pull request #209. `.agent/live_review.md` is the source of truth
for the open set, the round map and the finding-id ceiling, which is derived with
`max` over its line-anchored entries rather than read from a header sentence.

## Goal
Exactly ONE door for UI-initiated change: POST /api/jobs/{jid}/commands validates
against the UI command catalog, authenticates with a bearer token plus an
X-Remedy-CSRF double-submit, rate-limits per token and job, deduplicates by
client nonce, and ENQUEUES into the existing decision, approval and control
machinery without touching files, jobs or shells directly. Every other POST, PUT
and DELETE answers 405. DONE when the exposed commands round-trip through queue
effects on fixtures, replayed nonces are idempotent, unauthenticated and
cross-site attempts fail closed and are audited as rejected, and a route-walking
test plus an import guard prove no other mutating route exists.

## Current Step
R2 records the R1 verdict and inventories the ground this feature builds on: the
command catalog and whether a UI-exposed subset already exists, how the UI
server authenticates today, which module owns each effect backend the feature
names, where an event reaches the ledger the F008 stream reads, whether any nonce
or rate-limit machinery exists to reuse, and which test directory the contract
tests belong in. Every answer is MEASURED in the source and carried as a
`path:line` citation; an answer of "this does not exist" names the search that
established the absence.

## Next Steps
1. R3 records R2 and rules the channel's shape as a DECISION: the auth pair, the
   nonce replay window, the rate-limit configuration, the audit record's fields
   and the effect table for the initially exposed commands.
2. R4 onward the built work, in the T001/T002/T003 order the feature file's Task
   slicing names, gated on the SSE stream per its Orchestrator brief.
3. The integration gate before closure, then the closure round itself.

## Risks
- The feature file names `tests/ui_contract/test_command_channel.py` and no such
  directory exists; the repository has `tests/ui_contracts/`. R2 measures it and
  R3 rules it, rather than a builder guessing mid-round.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  configuration installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
<<<END PLANF009R2

## C2 — the R1 verdict
Append LEDGER2 to `.agent/live_review.md` as the LAST paragraph, separated from
the current last paragraph by exactly one blank line. Read the base bytes with
`git show <round base>:.agent/live_review.md` into `.remedy-wt/` scratch; never
write a base blob over the tracked file.

<<<SLICE LEDGER2
Gate: R2 — the R1 entry. R1 PASSED. NO finding is registered against the worker: every value it reported reproduced when the reviewer re-derived it off disk, and the one thing it got back was a defect in the reviewer's own slice text, declared as an objection and correctly not acted on. THE OPEN PR GATE WAS EXECUTED, NOT ASSUMED: pull request 209 reads `MERGED` with `mergedAt` 2026-08-21T18:35:07Z and `mergeCommit` ce49348b8f5b0374417f5b6c47d8c04966e7108e, which is exactly the branch point this round's commits sit on and an ancestor of the branch tip; `git ls-remote --heads origin feature/f008-sse-event-stream` prints nothing, so the gate's own `--delete-branch` really removed it; and `gh pr list --state open` prints `[]`. That pull request was created by a PREVIOUS session, so merging it here is the Open PR Gate rather than a same-session merge, which guardrail G1 of docs/agents/self_drive_protocol.md forbids. TRANSPORT HELD THREE WAYS AND THE THIRD IS THE REVIEWER'S OWN COPY: `.remedy-wt/f009-r1.md` as emitted, `.agent/authored/f009-r1.md` at `e160f083` and `.agent/last_block.md` at `720b95fc` are all sha256 293b43290fa3180c58209deea79e64927c52df2677611be19a8e9ef712fcf605 over 31011 bytes and 409 lines, so the block the worker applied is byte-identical to the block the reviewer authored rather than merely self-consistent. THE RESET IS THE ROUND'S REAL WORK AND IT WAS RE-DERIVED FROM THE BASE BLOB, not read back: at `ce49348b` the record holds 201 registered paragraphs and 6 line-anchored `Done:` lines, so the open set is 195; at `7a325c37` the record carries 196 registered paragraphs of which 195 are those same ids, the SYMMETRIC DIFFERENCE against the base open set is EMPTY, the ORDER is preserved, and every one of the 195 paragraphs is BYTE-EQUAL to its base original — the reviewer compared the paragraph objects themselves, not their ids. NEGATIVE CONTROL, without which 195 equalities prove only that a comparison ran: one printable byte flipped in the first carried paragraph is REJECTED by the byte-presence check while the unflipped paragraph is ACCEPTED. THE READINGS AT C2 ARE THE REVIEWER'S OWN: `^- R-\d+ — ` 196 with 196 DISTINCT ids, `^Done: R-\d+ — ` 1 naming R-0406, `^Landed: ` 0, `^Gate: R\d+ — ` 1, `^- R-0630 — ` 1, `^> Next free id` 0 lines, 0 marker lines, `Steps` present, max id R-0630, and the single gate header reading `Gate: R1 — the F008 R36 entry.`, whose shape matches the series it opens. R-0406 IS GENUINELY RESOLVED RATHER THAN DECLARED RESOLVED: the retired header claimed `Next free id: R-0612.` while that record's highest registered entry was R-0629, understating the ceiling by seventeen, and the header this round wrote carries no such sentence — the `^> Next free id` reading of 0 is the measurement, anchored at the header's own form because DONE0406 legitimately QUOTES the retired sentence and a bare substring count would have been unmeetable by construction. THE CLAIM PAIR APPLIED CLEANLY: STATUSFROM reads 1 at the branch point and 0 at `0e60102c`, STATUSTO 0 then 1, and the branch-point blob with that ONE substitution is BYTE-EQUAL to the C3 blob, which is also the proof no other line of that ledger moved; `^- \[~\] ` goes 0 to 1 and `^- \[x\] F\d{3} — ` reads 54 at BOTH, so claiming F009 moved nothing into the accepted set, and `README.md` is correctly ABSENT from the change set — a claim round owes no README edit where a closure round does. THE SLICES LANDED WHOLE: `.agent/plan.md`, `.agent/candidates.md` and `.agent/context.md` are each BYTE-EQUAL to their authored slice, the record STARTS with LRHEADER and ENDS with GATE1, and R0630 and DONE0406 each occur exactly once. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout at the branch tip and reproducing all four of the worker's numbers exactly: `tests/docs/` EXIT 0 at 295 passed, `tests/orchestration/test_roadmap_index.py` EXIT 0 at 30, the state-reader group of `tests/ui_server/` with `test_test_runner.py`, `test_resource_safety.py` and `test_integrity_gate.py` EXIT 0 at 423, and the canary `tests/cli/test_golden_path.py` EXIT 0 at 42. THE RANGE HOLDS: the path set from the branch point is EXACTLY the eight declared paths, seven single-parent commits before the handback with insertions 409, 380, 30, 33, 1, 3 and 35 — every one under the 500 cap — each cell equal to the `+/-` column of the handback's `## Commits` table, 0 marker lines in all five committed targets, `amend`, `rebase` and `cherry` each 0 in this round's reflog entries, an 81-line handback under the 100 its eight commits allow, a clean tree and `git worktree list` naming the primary checkout alone. THE OBJECTION THE WORKER RAISED IS CORRECT AS A READING AND IS NOT A FINDING, and it is recorded here rather than repaired because the text has landed in an append-only record. The LRHEADER paragraph resolving R-0406 reads "ruled the stored value a second source of truth for a number" and continues into a relative clause whose relativizer is elided across a line break, so it scans as a dropped clause; it is grammatical and it states nothing false, which is why no id is minted and why the landed bytes are not rewritten — §3 item 20's counter-measure is a dated correction, never an overwrite. THE DRAFTING LESSON IS THE REVIEWER'S TO CARRY: a restrictive clause with an elided relativizer, split across a line break, reads as truncation to exactly the careful reader this workflow depends on, and the worker was right to stop, say so, and apply the bytes as written rather than improve them.
<<<END LEDGER2

## C3 — the inventory
Write `.agent/f009_inventory.md`. THIS FILE'S CONTENT IS YOURS, NOT MINE: it
records what you MEASURE in the source, and no part of it is authored above. Do
not guess, do not summarise the feature file, and do not repeat this block's
wording as if it were a finding.

Answer each question below under its own `## Q<n>` heading, in this order. Every
factual claim carries at least one citation in the exact form `path:line` or
`path:line-line`, naming a real file and a real line, and the answer to a
question whose subject DOES NOT EXIST says so explicitly and names the search
that established the absence — the command you ran and what it returned. A
measured absence is a first-class answer here; a guess is not.

- **Q1 The catalog.** Where is the command catalog defined, what declares an
  entry, and does a UI-exposed subset already exist as a declared thing or would
  F009 be introducing that concept? Name the module, the type or structure an
  entry has, and how a command's arguments are described today, if they are.
- **Q2 The current door.** How does the UI server authenticate a request today,
  exactly — which function, which comparison, which transport carries the token?
  Does ANY bearer-header or CSRF handling exist anywhere in the server or its
  client, or would F009 introduce both? Name what `do_POST`, `do_PUT` and
  `do_DELETE` do today and where the 405 comes from.
- **Q3 The effect backends.** For each of the three commands the feature file
  exposes first — stop, decision answer, approve plan — name the module and
  function that performs the effect TODAY, and how it is invoked now (CLI
  command, direct call, file write). The feature file calls the stop backend a
  "kill-switch control file"; establish what that really is in this repository,
  or that no such thing exists under that or any name you searched.
- **Q4 The event seam.** Where does an event get APPENDED to the ledger the F008
  stream reads? Name the writer function and the module, and state whether an
  emitter reachable from an HTTP handler already exists or whether F009 must
  introduce one. Name the envelope's required fields as the schema defines them.
- **Q5 Nonce, rate limit, audit.** Does any nonce, replay-window, rate-limit or
  per-job audit-log machinery already exist in this repository that F009 could
  reuse? Search for each of the four separately and report each result, including
  the negative ones. If a redaction denylist governs what may be written to an
  audit record, name it and the module that applies it.
- **Q6 The test home.** The feature file's Do-not-touch section names
  `tests/ui_contract/test_command_channel.py`. Establish, by listing, which test
  directories actually exist for this surface and what each currently holds, and
  state which one a command-channel contract test belongs in. Do not create the
  file or the directory this round.

Close the file with a `## Open questions for R3` section listing every question
your measurements did NOT settle, one per line. An empty section is a claim; if
you write one, say what you checked to be able to make it.

## Constraints
1. Apply PLANF009R2 and LEDGER2 BYTE FOR BYTE out of the committed C0a blob. Do
   not retype, rewrap, reflow, reindent or whitespace-adjust either. If a slice
   looks wrong to you, apply it as written and record the objection in the
   handback under "Deviations & assumptions" — an objection is recorded, never
   acted on. Your objection last round was correct and correctly handled.
2. The commit order is C0a, C0b, C1, C2, C3, C4 and nothing comes between them.
   C1 is the first substantive commit.
3. The change set is the six paths named above. Touch no other path. In
   particular, create no file under `tests/` and edit nothing under `packages/`
   or `apps/` — this round only reads them.
4. `.remedy-wt/` is gitignored scratch. Every multi-step gate goes into a script
   there and runs from there; `git status --porcelain` prints 0 lines after each
   commit.
5. Push with `git push` after C3. Do NOT create a pull request.

## Done when
- G1 `.agent/STOP` ABSENT, read at Step 0 and again immediately before C0a.
  `git rev-parse --abbrev-ref HEAD` prints `feature/f009-single-write-channel`
  at every reading. `git status --porcelain` prints 0 lines after each of C0a
  through C4. Report the round base SHA from Step 0.
- G2 Transport EQUAL: `.remedy-wt/f009-r2.md` as received, `.agent/authored/
  f009-r2.md` at C0a and `.agent/last_block.md` at C0b all carry the same sha256,
  byte count and line count, and that digest EQUALS the one in the task prompt.
- G3 Report, per slice, the newline-included sha256, byte count and line count,
  the COUNT of slices from your own ordered extraction out of the committed C0a
  blob, and the three aggregate readings: any trailing whitespace, any leading
  blank line, all newline-terminated.
- G4 `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R2; report its line count
  against the 50-line cap; `Steps` occurs; `^## Goal$` and `^## Next Steps$` each
  match exactly 1 line; the first `\bF\d{3}\b` match is `F009`.
- G5 The append at C2, proved TWICE over independent extractors. (a) The round
  base blob is a byte-exact PREFIX of the C2 blob and the remainder EQUALS a
  newline plus LEDGER2 — report the remainder's sha256, byte count and line
  count. (b) An INDEPENDENT blank-line split of the WHOLE C2 file, its
  terminating newline normalised first, yields N units whose LAST unit is
  LEDGER2's paragraph — report N. NEGATIVE CONTROL: flip ONE printable ASCII
  byte of the remainder to another printable one and confirm BOTH readings
  REJECT it while both ACCEPT the unflipped value; report all four outcomes.
- G6 At the round base and at C2, line-anchored: `^- R-\d+ — ` 196 and 196 —
  this round mints NO id — `^Done: R-\d+ — ` 1 and 1, `^Landed: ` 0 and 0,
  `^- R-0630 — ` 1 and 1, `^> Next free id` 0 and 0, and `^Gate: R\d+ — ` 1 then
  2 over that many DISTINCT keys. HEADER SHAPE (§3 item 26): of the `Gate: `
  lines at C2, report how many match `^Gate: R(\d+) — the R(\d+) entry\.` with
  the second numeral one less than the first, and quote the text to its first
  period of any that does not — the R1 entry does not match that pattern, because
  it names the F008 R36 entry rather than an R0, so the expected reading is one
  match and one non-match whose text is `Gate: R1 — the F008 R36 entry.`
- G7 The inventory at C3. Report: the count of `## Q` headings, which must be 6
  and cover Q1 through Q6 with no repeat; the presence of the
  `## Open questions for R3` heading; and the CITATION AUDIT, run by a script of
  yours over the committed C3 blob — extract every `path:line` and
  `path:line-line` token, and for EACH report whether the path exists at C3 and
  whether the line number is within that file's line count. The count of
  citations that FAIL either check MUST be 0, and report the total count of
  citations audited. Report the per-question count of citations, so a question
  answered with no citation at all is visible rather than averaged away.
- G8 In the PRIMARY checkout, SERIALLY, one process at a time, at C3:
  `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
  tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
  -q -rf`, then the canary `python3 -m pytest tests/cli/test_golden_path.py -q
  -rf`. Report each exit code and its passed-plus-skipped sum. The reviewer
  measured 423 and 42, both exit 0, at `87ad9e5c`. The docs gate is NOT ordered
  this round, because no path under `docs/` or `docs/roadmap/` is in the change
  set — say so rather than running it silently.
- G9 The range from the round base to C3: `git diff --name-only` lists EXACTLY
  the five paths of the change set other than `.agent/handoff.md`, the set
  difference empty in both directions. Walk `git rev-list --reverse` and report,
  per commit, that it has ONE parent and its `git show --numstat` insertions,
  with `git diff --numstat` AGREEING on every cell and every cell equal to the
  `+/-` column of your `## Commits` table. `^<<<SLICE ` and `^<<<END ` read 0
  lines in each of `.agent/plan.md`, `.agent/live_review.md` and
  `.agent/f009_inventory.md`. Classify this round's own reflog entries by the
  operation before the first `:` in `%gs` and report `amend`, `rebase` and
  `cherry`, which must each be 0; assert no total over the whole reflog (R-0601).
- G10 The handback carries every mandated section of
  docs/agents/handback_template.md, an item-status table holding exactly one row
  for each of C0a, C0b, C1, C2, C3 and C4, the round base SHA, and one line per
  gate — raw transcripts belong in the round report (R-0582). Report its line
  count against the 60 that AGENTS.md sets, or carry a DECISION D15 stated-cause
  line naming the mandated content that caused an overage.

Handback:    completion report + rewrite `.agent/handoff.md`. The state block
             repeats this Fortschritt line verbatim: 5 % (T001 offen · T002
             offen · T003 offen — R1 hat beansprucht, R2 hat den Boden vermessen;
             gebaut wurde noch nichts) — Schätzung
──────────────────────────────────────────────────────────────
