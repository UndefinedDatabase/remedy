── STEP R3/3 — F009 The single write channel ────────────────────────
Goal:        Record the R2 verdict, then RULE the write channel's shape as
             operator-visible DECISIONS grounded in R2's measurements — the auth
             pair, the exposed subset, the effect table, the audit record, the
             fingerprint, the nonce store and the rate limit — and amend the one
             feature-file line whose path does not exist. No production code is
             written this round; T001 builds against these rulings from R4.

Bundle:      C0a save the block · C0b mirror the block · C1 the plan ·
             C2 the R2 verdict in the review record · C3 the decisions ·
             C4 the feature-file amendment · C5 the context file ·
             C6 the handback.

Change set:  `.agent/authored/f009-r3.md`, `.agent/last_block.md`,
             `.agent/plan.md`, `.agent/live_review.md`, `.agent/decisions.md`,
             `docs/roadmap/features/T5_F009.md`, `.agent/context.md`,
             `.agent/handoff.md`. Nothing else. No path under `packages/`,
             `apps/` or `tests/` is edited this round.

## Step 0 — before any commit
    ls -la .agent/STOP
    git rev-parse --abbrev-ref HEAD
    git status --porcelain
    git rev-parse HEAD

`.agent/STOP` MUST be absent; if it exists, stop, write the handoff and end. The
branch MUST already be `feature/f009-single-write-channel`. Do NOT run an Open PR
Gate and do NOT create a pull request. The SHA `git rev-parse HEAD` prints is the
ROUND BASE — it is `ee2fdda7` unless something has moved; report what you read.

## Transport
This block lives at `.remedy-wt/f009-r3.md`. Its sha256, byte count and line
count are stated in the task prompt that handed you that path. Verify it BEFORE
using any byte of it. Save it byte for byte as `.agent/authored/f009-r3.md`
(C0a), then mirror it to `.agent/last_block.md` (C0b) FROM THE COMMITTED C0a
BLOB — `git show <C0a>:.agent/authored/f009-r3.md` — never from this file again
and never by retyping.

## Slice convention
The authored units below are delimited by one-line markers, `<<<SLICE <NAME>`
opening and `<<<END <NAME>` closing. Extract every slice from the COMMITTED C0a
BLOB by its marker lines with a script. The marker lines are NOT part of any
slice. Every slice is newline-terminated, none begins with a blank line, and none
carries trailing whitespace on any line — report those three readings as your
script measured them. Marker lines never reach a target file.

## C1 — the plan, the first substantive commit
Apply PLANF009R3 as the WHOLE file.

<<<SLICE PLANF009R3
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
R3 records the R2 verdict and rules the channel's shape as DECISIONS F009 D1
through D9, each grounded in a citation R2 measured rather than in the feature
file's wording: the test home, the auth pair, the token comparison, the exposed
subset, the effect table, the audit record, the fingerprint, the nonce store and
the rate limit. It also amends the one feature-file line naming a directory this
repository does not have.

## Next Steps
1. R4 builds T001's first half against D2, D3 and D4: the POST route, the bearer
   and CSRF checks, the constant-time comparison for both doors, and the typed
   validation errors, with contract tests in `tests/ui_server/`.
2. R5 completes T001 with the rate limit as the typed config key D9 rules, then
   T002's nonce store and audit record per D6, D7 and D8.
3. T003's effect table and queue-only guards per D5, including the plan-approval
   extraction, which lands as its own commit before the endpoint uses it.
4. The integration gate before closure, then the closure round.

## Risks
- D3 touches the EXISTING GET token check, the only line this feature changes
  outside its own new surface. It is declared, it is two lines, and the
  `tests/ui_server/` suite gates it.
- D5's plan-approval extraction is a refactor of `apps/cli/commands/decision.py`;
  AGENTS.md forbids mixing it with feature code, so it is its own commit.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which is
  R-0622 and routes to a paydown branch.
<<<END PLANF009R3

## C2 — the R2 verdict
Append LEDGER3 to `.agent/live_review.md` as the LAST paragraph, separated from
the current last paragraph by exactly one blank line. Read the base bytes with
`git show <round base>:.agent/live_review.md` into `.remedy-wt/` scratch; never
write a base blob over the tracked file.

<<<SLICE LEDGER3
Gate: R3 — the R2 entry. R2 PASSED. NO finding is registered against the worker, no deviation and no objection were declared, and the round earned more than a pass: its inventory is the most carefully measured artefact this branch has produced. THE BYTE PROOFS ARE THE REVIEWER'S OWN, re-derived from the committed blobs rather than read back. Transport is EQUAL THREE WAYS including the reviewer's own copy: `.remedy-wt/f009-r2.md` as emitted, `.agent/authored/f009-r2.md` at `d7fc0801` and `.agent/last_block.md` at `c418b13c` are all sha256 ef766a8c474548c03e5e850e69c28f21a5f43058c51f8582f8061ef7eb638891 over 20682 bytes and 242 lines. THE APPEND AT `81ea873e` IS PROVED TWICE OVER: the round-base blob is a byte-exact PREFIX of the C2 blob, the remainder is 5575 bytes and 2 lines equal to a newline plus the reviewer's OWN LEDGER2 slice, and an INDEPENDENT blank-line split of the whole file yields 203 units whose LAST is that paragraph — with a one-byte printable flip REJECTED by BOTH readings and the unflipped value ACCEPTED by both. THE SETS HELD: `^- R-\d+ — ` 196 with 196 DISTINCT ids at the base and at C2 — this round minted no id — `^Done: R-\d+ — ` 1, `^Landed: ` 0, `^- R-0630 — ` 1 and `^> Next free id` 0 at both, `^Gate: R\d+ — ` 1 then 2 over 2 DISTINCT keys, and of the two headers at C2 exactly one matches `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one less than the first while the non-match reads `Gate: R1 — the F008 R36 entry.`, which is the expected shape for a record whose first entry gates the PREVIOUS branch's last round. THE CITATION AUDIT IS THE GATE THAT MAKES AN INVENTORY EVIDENCE, and the reviewer ran its own over the committed C3 blob rather than accepting the worker's: 191 citations extracted, 43 distinct files, ZERO paths missing at C3 and ZERO line numbers past their file's length, with per-question counts 19, 28, 50, 25, 33 and 20 and 16 more in the open-questions section — so no question is answered without evidence and none is averaged away by a neighbour. THE SUITES ARE THE REVIEWER'S OWN, serial, in the primary checkout: the state-reader group EXITS 0 at 423 passed and the canary EXITS 0 at 42, reproducing both of the worker's numbers; the docs gate was correctly NOT ordered and NOT run, no path under `docs/` being in the change set, and the round said so rather than running it silently. THE RANGE HOLDS: the path set is EXACTLY the six declared paths, five single-parent commits before the handback with insertions 242, 186, 21, 2 and 425 — every one under the 500 cap — each cell equal to the `## Commits` column, 0 marker lines in all three committed targets, `amend`, `rebase` and `cherry` each 0, a clean tree, `git worktree list` naming the primary checkout alone, and a 69-line handback carrying a DECISION D15 stated-cause line and under the 100 its six commits allow. WHAT MAKES THE INVENTORY WORTH THIS MUCH OF AN ENTRY is that the reviewer spot-checked ELEVEN of its substantive claims against the source and all eleven held, which is the check a resolving citation does not perform: `secrets.compare_digest` really occurs 0 times in `packages/orchestration/ui_server.py`; `SSE_MAX_STREAMS_PER_JOB = 4` really stands at `packages/orchestration/ui_server.py:2837` under the comment the inventory cites; the single case-insensitive `nonce` hit really is `class TestWorkerRunOnce:` at `tests/orchestration/test_worker_queue.py:169`, a false positive the round identified rather than reported as a finding; `fetchJson` really hard-codes `{ method: "GET", credentials: "same-origin" }`; `request_stop` really publishes create-only and its own docstring names the idempotency-under-race property the inventory proposes reusing; `answer_task_decision`'s signature and its non-open refusal are exactly as cited; the plan approval really is inline CLI code mutating `fp["_approval"]` and calling `save_job`; and `packages/orchestration/decision_queue.py` really exposes only `list_`, `get_`, `explain_`, `export_`, `sort_`, `open_`, `render_` and `build_` functions, so "enqueue into the decision queue" has no write target and the feature file's phrase does not resolve. THE ROUND ALSO SEPARATED A REDACTION PATTERN FROM A PARSER, which is the distinction a careless search collapses: every `Bearer` hit under `packages/` is a secret-scrubbing regex, so "no bearer authentication exists" is true while "no occurrence of the word" would have been false, and the inventory said which it meant. IT DECLINED TO MINT IDS IT HAD GROUNDS FOR — the non-constant-time token comparison and a stale module comment — and routed both to this round instead, which is correct: only reviewer-authored text registers a finding, and an inventory that quietly widened into the ledger would be the worker writing verdicts. THE ONE THING THIS ENTRY OWES THE RECORD is that the reviewer's own ad-hoc check for the open-questions heading used a SUBSTRING search and matched the heading's own QUOTATION in the file's preamble before the section itself — the R-0584 shape, in the reviewer's throwaway code, one round after registering R-0630 for exactly that class. The gate the block ORDERED was line-anchored and read 1 correctly; nothing false landed, and no id is minted for a scratch script. It is recorded because the lesson is that the anchor discipline has to reach the reviewer's disposable checks too, not only the gates that reach a worker.
<<<END LEDGER3

## C3 — the decisions
Append DECISIONS to `.agent/decisions.md` as its new last content, separated from
the current last paragraph by exactly one blank line. Same base-read rule as C2.

<<<SLICE DECISIONS
## DECISION F009 D1 — the command-channel contract test lives in `tests/ui_server/` (2026-08-21)

The feature file's Do not touch section named `tests/ui_contract/test_command_channel.py`. Measured at R2: that directory does not exist. Two candidates do — `tests/ui_contracts/`, whose modules are Python files asserting over React `.tsx` SOURCE, and `tests/ui_server/`, which holds every HTTP route contract this server has, including `test_sse_stream.py` and `test_auth_redaction.py`.

CHOSEN: `tests/ui_server/test_command_channel.py`. The surface under test is an HTTP route on `_RemedyHandler`, which is what every module in that directory already tests, and AGENTS.md's discoverability rules ask for one spelling per concept and a test file named after the source it covers.

ALTERNATIVES: (a) create `tests/ui_contract/` as the feature file names it — rejected, it would be a third directory one character from an existing one, which is precisely the synonym drift those rules forbid. (b) `tests/ui_contracts/` — rejected, its subject is component source, not server behaviour.

REVERSE by moving the file and restoring the feature-file line; C4 of this round is the amendment and it is a two-line pair.

## DECISION F009 D2 — POST authenticates by bearer plus CSRF, and the GET routes keep their query token (2026-08-21)

Measured at R2: the only authentication is a query-string token compared inside `do_GET`, the React client appends that token as a query parameter, and no bearer or CSRF handling exists anywhere in the server or the client.

CHOSEN: the new POST route requires `Authorization: Bearer <token>` AND an `X-Remedy-CSRF` header double-submitted against the served app; the existing GET routes keep the query parameter unchanged in this feature. Two token transports therefore coexist deliberately, and the code says so where a reader would search.

WHY THE GET HALF DOES NOT MIGRATE, and this is a technical constraint rather than a scope preference: the cockpit consumes the event stream through the browser `EventSource` API, which cannot set request headers at all. A bearer-only server would make the F008 stream unauthenticatable. The query token is what a stream can carry, and a header is what a write must carry so it cannot be replayed out of a URL, a referrer or a shell history.

ALTERNATIVES: (a) migrate every route to bearer — rejected on the EventSource constraint above. (b) accept the query token on POST too — rejected: it puts a mutating credential in URLs and defeats the CSRF pair's purpose.

REVERSE by deleting the two header checks and reading the query token in the POST path; nothing else depends on the choice.

## DECISION F009 D3 — the token comparison becomes constant-time, for both doors, inside this feature (2026-08-21)

Measured at R2: the comparison is a plain `!=` and `secrets.compare_digest` occurs zero times in the module.

CHOSEN: T001 replaces that comparison with `secrets.compare_digest` for the existing GET check AND the new POST check. This is the one line this feature changes outside its own new surface, and it is declared here rather than discovered in review.

WHY IT IS IN SCOPE: the feature's own Acceptance requires that unauthenticated attempts fail closed. Putting a write door behind a token whose comparison leaks its prefix in timing, while leaving the weaker half untouched because it predates the feature, would be shipping a knowingly weaker guard on the same secret. The change is two lines and the `tests/ui_server/` suite already covers both paths.

ALTERNATIVES: (a) leave it and register a finding — rejected, a finding routes work to a paydown branch that has no scheduled round, and this feature is the reason it now matters. (b) constant-time on POST only — rejected, both doors accept the same secret.

REVERSE by restoring `!=`; the behaviour is identical for every non-attacker input.

## DECISION F009 D4 — the exposed subset is catalog ids, declared beside the catalog (2026-08-21)

Measured at R2: the catalog is `apps/cli/command_catalog.py` with 340 entries over 60 groups, no UI-exposed subset exists as a declared thing, and the UI server never imports the catalog. Measured by the reviewer at R3: the three commands the feature file names map onto only TWO `command_id` values — `job.stop` and `decision.resolve` — because plan approval has no id of its own and reaches the CLI as a `fp:`-prefixed decision id routed inside `decision.resolve`.

CHOSEN: a `UI_EXPOSED_COMMANDS` frozenset of `command_id` values declared in `apps/cli/command_catalog.py` beside `CATALOG`, holding `job.stop` and `decision.resolve`. The API's `command` field IS a catalog `command_id`; plan approval reaches the channel as `decision.resolve` carrying a `decision_id` argument with the `fp:` prefix, exactly as the CLI spells it. The endpoint imports that set, which is the single source the feature file's How-it-fits section requires.

ALTERNATIVES: (a) invent a third API command name for plan approval — rejected, it would be a second spelling for one concept and the prefix routing would still have to exist underneath. (b) declare the subset in the server — rejected, it separates the subset from the catalog it constrains.

REVERSE by deleting the frozenset and inlining the two ids at the endpoint.

## DECISION F009 D5 — the effect table, and the plan-approval extraction lands as its own commit (2026-08-21)

Measured at R2: `safe_points.request_stop` is an importable package function with no CLI coupling; `escalation.answer_task_decision` is likewise importable and does not persist, its CLI caller invoking `save_job` afterwards; the plan approval is inline CLI code that mutates the flight plan, calls `save_job`, writes an assumptions log and prints; and `decision_queue.py` is a read-only aggregation with no write target at all.

CHOSEN: stop maps to `request_stop`. A decision answer maps to `answer_task_decision` followed by `save_job`. Plan approval maps to a NEW package-level function extracted from `apps/cli/commands/decision.py`, keeping the CLI as its first caller so the extraction is provably behaviour-preserving; the printing stays in the CLI and does not move into the package. That extraction is a refactor, so per AGENTS.md it is ITS OWN COMMIT and lands before any endpoint code calls it.

WHAT "QUEUE-ONLY SIDE EFFECTS" MEANS HERE, since the feature file's phrase does not resolve against the source: the handler may import exactly the three effect functions plus the audit writer, and nothing that opens a file, spawns a process or writes storage directly. The import guard asserts that set, and the per-command tests assert that the effect function was called and that no other file under the job's tree changed.

ALTERNATIVES: (a) duplicate the approval guard sequence in the handler — rejected, it is the coupling the P3 contract exists to prevent and it would drift from the CLI. (b) build a real queue for decision answers to enqueue into — rejected as this feature's work; nothing consumes such a queue today and inventing one would widen F009 into the machinery it is supposed to reuse.

REVERSE by re-inlining the extracted function into the CLI command.

## DECISION F009 D6 — the audit record: per-job, private, append-only, and its fields are fixed here (2026-08-21)

Measured at R2: `commands_audit.jsonl` exists nowhere, while `docs/roadmap/features/T5_F035.md` and `docs/roadmap/features/T9_F167.md` already plan to READ it. Two later features therefore depend on this choice, which is why it is ruled now rather than at T002.

CHOSEN: `commands_audit.jsonl` in the per-job control directory `job_control_dir(job_id)` — the private 0o700 directory `safe_points` already owns — written through `packages.common.secure_fs` with the 0o600 file mode that directory's other files use. One JSON object per line, append-only, never rewritten. Fields, in this order: `ts`, `token_fp`, `command`, `args_hash`, `nonce`, `outcome`.

EVERY ATTEMPT IS AUDITED, not only accepted ones: the feature's Acceptance requires wrong or missing auth to be audited as rejected, so `outcome` carries the rejection reason and a rejected attempt writes a record before the response is sent.

ALTERNATIVES: (a) the evidence export directory — rejected, it is packaged into review zips and an audit log carrying token fingerprints does not belong in a shareable artefact. (b) the run log — rejected, it is per RUN and keyed to a run id, while this record is per JOB and must survive across runs.

REVERSE by changing the path helper; the field set is the half two other features depend on and should be changed only with them.

## DECISION F009 D7 — the token fingerprint is a truncated digest, and rotation deliberately changes it (2026-08-21)

The feature file asks for fingerprints "stable per token id, not raw tokens". Measured at R2: there is no token-id concept in this repository — `start_ui_server` mints a token per run with `secrets.token_urlsafe(24)` — so "token id" has no referent and is read here as the token VALUE.

CHOSEN: `token_fp` is `"tf:" + sha256(token.encode()).hexdigest()[:16]`. It never carries the raw value, which the redaction denylist in `packages/orchestration/stream_evidence.py` forbids writing at all.

ROTATION CHANGES THE FINGERPRINT, and that is the intended reading rather than a limitation: the audit answers which credential acted, not which human, and a rotated token is a different credential. A record that survived rotation would be claiming an identity this system does not model.

ALTERNATIVES: (a) a random per-token id stored beside the token — rejected, it adds a persisted mapping for no gain. (b) the full digest — rejected, sixteen hex characters distinguish every token a job will ever see and keep the line readable.

REVERSE by changing the helper; the field name does not change.

## DECISION F009 D8 — the nonce store is one create-only file per nonce, and the window is the job (2026-08-21)

Measured at R2: no nonce, replay-window or deduplication machinery exists; the run log is append-only and per run, so it cannot return a body; and the closest in-repo precedent is `request_stop`, which publishes create-only so a race converges on one record.

CHOSEN: `commands_nonce/<nonce>.json` inside the same per-job control directory, one file per nonce, holding the response body that was returned. Publication is CREATE-ONLY through the same `secure_fs` path `request_stop` uses: the loser of a race reads the winner's file and returns the SAME body, which is exactly the "a seen nonce returns the ORIGINAL result, idempotent, not an error" contract the feature file states. The replay window is the JOB's lifetime — the directory dies with the job — rather than a duration.

ALTERNATIVES: (a) a time-bounded window with a sweeper — rejected, it adds a background concern and a clock dependency to buy an expiry nobody has asked for. (b) a single map file — rejected, concurrent writers would have to lock it, where one file per nonce gets atomicity from the filesystem, which is the precedent that already works here.

The nonce is a client-supplied string and becomes a PATH component, so it is validated against a strict character class and a length bound before it is used, the way `validate_job_id` guards the job segment of the same directory. A nonce that fails validation is a typed 4xx and is audited as rejected.

REVERSE by replacing the directory with another store; the endpoint contract does not change.

## DECISION F009 D9 — the rate limit is a typed config key, per token and job (2026-08-21)

The feature file says "rate limit per token+job (config)" without naming a config source. Measured at R2: the only limiter is `packages/orchestration/rate_governor.py`, which is OUTBOUND and per provider and inherits nothing here, and the only inbound precedent is the hard-coded `SSE_MAX_STREAMS_PER_JOB`. Measured by the reviewer at R3: `packages/orchestration/config.py` is a typed system with `ConfigKeySpec`, env-over-TOML-over-default precedence and a `get_config()` accessor, so "config" resolves to it.

CHOSEN: a `ConfigKeySpec` declaring the maximum accepted commands per token fingerprint and job per minute, with a built-in default, resolved through `get_config()`. The key is the pair `(token_fp, job_id)`. Exceeding it REFUSES with a typed 429 and audits the attempt as rejected — it does not wait, which is what the outbound governor does and would be wrong for an inbound request holding a connection.

ALTERNATIVES: (a) a module constant like the SSE cap — rejected, the feature file says config and a typed key costs one spec entry. (b) reuse `ProviderRateGovernor` — rejected, it is keyed by provider, it waits rather than refuses, and its own docstring states it neither coordinates across processes nor orders acquirers fairly.

REVERSE by deleting the key spec and reading a module constant.
<<<END DECISIONS

## C4 — the feature-file amendment
One two-line pair in `docs/roadmap/features/T5_F009.md`. The reviewer's
containment test printed `FEAT pair — TO contains FROM: False`, and the REWRITE
label is derived from that output, so this pair owes the FROM-0x reading rather
than the append obligation of §4.9. This is the §4.7 route: a spec defect is
amended by the reviewer into the block and recorded as a DECISION, which D1 is.

<<<SLICE FEATFROM
access from handlers (forbidden by contract). Suggested tests:
tests/ui_contract/test_command_channel.py.
<<<END FEATFROM

<<<SLICE FEATTO
access from handlers (forbidden by contract). Suggested tests:
tests/ui_server/test_command_channel.py — amended at F009 R3 from
`tests/ui_contract/`, a directory this repository does not have; DECISION
F009 D1 in `.agent/decisions.md` carries the measurement and the reasoning.
<<<END FEATTO

## C5 — the context file
`.agent/context.md` becomes CONTEXTF009R3 as the WHOLE file. Its readers span
several test modules: the dashboard contract asserts the substring "Steps" and a
`## Active Branch` heading with a `feature/` slug, `test_test_runner.py` asserts
a roadmap F-id, and `tests/regression/test_resource_safety.py` asserts "resource"
or "pytest" — validate the applied file against ALL of them.

<<<SLICE CONTEXTF009R3
# Context — F009 The single write channel

## Active Branch
feature/f009-single-write-channel, cut from `main` at `ce49348b`, the merge
commit of pull request #209, which R1 merged at the Open PR Gate. Self-drive
session per docs/agents/self_drive_protocol.md: the main session plans and
reviews and writes nothing in the work tree, one delegated worker per round makes
every commit. The branch carries no pull request; F009 opens one at its closure.

## Scope
In: ONE authenticated POST door for UI-initiated change —
`/api/jobs/<job_id>/commands` taking {command, args, client_nonce}, validated
against the UI-exposed catalog subset, authenticated by bearer plus an
X-Remedy-CSRF double-submit, rate-limited per token and job, deduplicated by
nonce so a replay returns the ORIGINAL body, audited per job including rejections,
and reaching the effect functions that already exist. Also in: the
`command.accepted` event on the F008 stream, the route-walking proof that every
other POST, PUT and DELETE answers 405, and the two lines D3 rules — the token
comparison becoming constant-time on BOTH doors.

Out, per the feature file's Do not touch: the effect backends' semantics, the
catalog's CLI half, and any file or shell access from a handler, forbidden by the
P3 contract and enforced by an import guard rather than by convention.

## Constraints
- Merges only at the Open PR Gate; never force-push; never work on main.
- DECISIONS F009 D1 THROUGH D9 ARE RULED as of R3 and bind every later round:
  the test home, the auth pair, the constant-time comparison, the exposed subset
  and its two catalog ids, the effect table with its own commit for the
  plan-approval extraction, the audit record's path and fields, the fingerprint,
  the nonce store, and the rate limit as a typed config key. They are in
  `.agent/decisions.md`; a round that departs from one amends it there first.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/** also gates
  tests/docs/ and tests/orchestration/test_roadmap_index.py — the second by
  R-0493, tests/docs/ asserting nothing about a feature file's body — and a round
  rewriting `.agent/` state or touching the UI server also gates
  tests/ui_server/, tests/orchestration/test_test_runner.py,
  tests/regression/test_resource_safety.py and
  tests/orchestration/test_integrity_gate.py. Destructive and red-proof checks
  run only inside a disposable git worktree under .remedy-wt/, so resource safety
  stays intact. Two pytest processes never run at once.
- COUNT BY PASSED-PLUS-SKIPPED. Data-dependent `pytest.skip(...)` calls in
  tests/ui_server/ make the split vary run to run at an unchanged tree.
- This is a UI-facing feature: docs/ui/design_reference/ is binding for every
  visual surface and assets_spec.md is the asset authority.
- Repository-wide `ruff check .` is RED at base and is NOT a gate (R-0364); ruff
  is gated scoped to the files a round touches, measured against the SAME files
  at the base. `npm run lint` in `apps/ui` is likewise red at base and is R-0622.
- 196 findings are open and none is a code defect of F009. R-0403, R-0607,
  R-0608, R-0609, R-0611, R-0613 and R-0630 stay routed to a paydown branch.

## Steps
Stated once, in `.agent/plan.md`. This file tracks scope and constraints only.
<<<END CONTEXTF009R3

## Constraints
1. Apply every slice BYTE FOR BYTE out of the committed C0a blob. Do not retype,
   rewrap, reflow, reindent or whitespace-adjust any of them. If a slice looks
   wrong to you, apply it as written and record the objection in the handback
   under "Deviations & assumptions" — an objection is recorded, never acted on.
2. The commit order is C0a, C0b, C1, C2, C3, C4, C5, C6 and nothing comes
   between them. C1 is the first substantive commit.
3. The change set is the eight paths named above. Touch no other path. Write no
   code and create no test file: every DECISION here is a ruling for LATER rounds
   to build against, and building any of it this round is scope drift.
4. `.remedy-wt/` is gitignored scratch. Every multi-step gate goes into a script
   there; `git status --porcelain` prints 0 lines after each commit.
5. Push with `git push` after C5. Do NOT create a pull request.

## Done when
- G1 `.agent/STOP` ABSENT, read at Step 0 and again immediately before C0a.
  `git rev-parse --abbrev-ref HEAD` prints `feature/f009-single-write-channel` at
  every reading. `git status --porcelain` prints 0 lines after each of C0a
  through C6. Report the round base SHA from Step 0.
- G2 Transport EQUAL: `.remedy-wt/f009-r3.md` as received, `.agent/authored/
  f009-r3.md` at C0a and `.agent/last_block.md` at C0b all carry the same sha256,
  byte count and line count, equal to the digest in the task prompt.
- G3 Report, per slice, the newline-included sha256, byte count and line count,
  the COUNT of slices from your own ordered extraction out of the committed C0a
  blob, and the three aggregate readings: any trailing whitespace, any leading
  blank line, all newline-terminated.
- G4 `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R3; report its line count
  against the 50-line cap; `Steps` occurs; `^## Goal$` and `^## Next Steps$` each
  match exactly 1 line; the first `\bF\d{3}\b` match is `F009`.
- G5 The append at C2, proved TWICE over independent extractors. (a) The round
  base blob is a byte-exact PREFIX of the C2 blob and the remainder EQUALS a
  newline plus LEDGER3 — report the remainder's sha256, bytes and lines. (b) An
  INDEPENDENT blank-line split of the WHOLE C2 file, its terminating newline
  normalised first, yields N units whose LAST is LEDGER3's paragraph — report N.
  NEGATIVE CONTROL: flip ONE printable ASCII byte of the remainder and confirm
  BOTH readings REJECT it while both ACCEPT the unflipped value; report all four.
- G6 At the round base and at C2, line-anchored: `^- R-\d+ — ` 196 and 196 —
  this round mints NO id — `^Done: R-\d+ — ` 1 and 1, `^Landed: ` 0 and 0,
  `^- R-0630 — ` 1 and 1, `^> Next free id` 0 and 0, and `^Gate: R\d+ — ` 2 then
  3 over that many DISTINCT keys. Of the `Gate: ` lines at C2, report how many
  match `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one less
  than the first, and quote to its first period any that does not — the expected
  reading is two matches and one non-match reading `Gate: R1 — the F008 R36
  entry.`
- G7 The append at C3, proved the same two ways as G5 with its own negative
  control: the round-base `.agent/decisions.md` blob is a byte-exact PREFIX of
  the C3 blob and the remainder EQUALS a newline plus DECISIONS; and an
  INDEPENDENT blank-line split of the whole C3 file ends in DECISIONS' last
  paragraph. Report `^## DECISION F009 D\d+ — ` at the base and at C3, which
  must read 0 then 9 over 9 DISTINCT keys D1 through D9, and `^## DECISION ` at
  both — report both totals rather than predicting them.
- G8 The amendment at C4: FEATFROM reads 1 at the round base and 0 at C4,
  FEATTO reads 0 then 1, and the base blob of `docs/roadmap/features/T5_F009.md`
  with that substitution applied ONCE is BYTE-EQUAL to the C4 blob — which is
  also the proof no other line of that file changed. Read the base bytes with
  `git show <round base>:docs/roadmap/features/T5_F009.md` into scratch, never
  over the tracked file. Report the file's line count at both commits, and report
  `tests/ui_contract/` at the base and at C4 over that file.
- G9 `.agent/context.md` at C5 is BYTE-EQUAL to CONTEXTF009R3; report the four
  reader assertions as four readings taken over the APPLIED file.
- G10 In the PRIMARY checkout, SERIALLY, one process at a time, at C5:
  `python3 -m pytest tests/docs/ -q -rf`, then `python3 -m pytest
  tests/orchestration/test_roadmap_index.py -q -rf`, then `python3 -m pytest
  tests/ui_server/ tests/orchestration/test_test_runner.py
  tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
  -q -rf`, then the canary `python3 -m pytest tests/cli/test_golden_path.py -q
  -rf`. Report each exit code and its passed-plus-skipped sum. The docs gate IS
  ordered this round because C4 edits a path under `docs/roadmap/`; state
  plainly in the handback that neither `tests/docs/` nor the roadmap-index module
  asserts anything about a feature file's BODY, so G8's byte proof rather than
  either suite is what establishes the amendment landed.
- G11 The range from the round base to C5: `git diff --name-only` lists EXACTLY
  the seven paths of the change set other than `.agent/handoff.md`, the set
  difference empty in both directions. Walk `git rev-list --reverse` and report,
  per commit, that it has ONE parent and its `git show --numstat` insertions,
  with `git diff --numstat` AGREEING on every cell and every cell equal to the
  `+/-` column of your `## Commits` table. `^<<<SLICE ` and `^<<<END ` read 0
  lines in each of `.agent/plan.md`, `.agent/live_review.md`,
  `.agent/decisions.md`, `docs/roadmap/features/T5_F009.md` and
  `.agent/context.md`. Classify this round's own reflog entries by the operation
  before the first `:` in `%gs` and report `amend`, `rebase` and `cherry`, which
  must each be 0; assert no total over the whole reflog (R-0601).
- G12 The handback carries every mandated section of
  docs/agents/handback_template.md, an item-status table holding exactly one row
  for each of C0a, C0b, C1, C2, C3, C4, C5 and C6, the round base SHA, and one
  line per gate — raw transcripts belong in the round report (R-0582). Report its
  line count against the 100 that eight commits allow.

Handback:    completion report + rewrite `.agent/handoff.md`. The state block
             repeats this Fortschritt line verbatim: 10 % (T001 offen · T002
             offen · T003 offen — R1 beansprucht, R2 vermessen, R3 entschieden;
             gebaut wurde noch nichts) — Schätzung
──────────────────────────────────────────────────────────────
