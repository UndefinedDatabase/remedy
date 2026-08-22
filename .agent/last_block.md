── STEP T003 (round one of DECISION F009 D19 — the `job.stop` dispatch) — F009 ──
Goal:        Retire the 501 seam for `job.stop`. The door dispatches it to
             `safe_points.request_stop` under D18's ruled order — effect, then
             the `accepted` audit line, then the nonce publication — answers 200
             with D18's body, audits a raised effect `rejected_effect`, pays
             R-0636 by moving the replay token to `replayed`, and migrates every
             seam pin. `decision.resolve` keeps the seam until its own round.

Fortschritt: ~78 % (T001 gebaut · T002 gebaut · T003 begonnen: Extraktion,
             Publikations-Bound und Vokabular stehen, der `job.stop`-Dispatch
             wird in dieser Runde gebaut) — Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R18 verdict and
             finding R-0638 · C3 DECISION F009 D20 · C4 the dispatch WITH its pins
             in ONE commit · C5 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f009-r19.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `.agent/decisions.md` (C3) · `packages/orchestration/ui_server.py`
             and `tests/ui_server/test_command_channel.py` (both C4) ·
             `.agent/handoff.md` (C5). NOTHING under `apps/` or `docs/` is
             touched, and no NEW file is created outside `.agent/authored/`.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. C2 and C3 are APPENDS — LEDGER19 to `.agent/live_review.md`, DECISION20 to
    `.agent/decisions.md`. Both targets end in exactly ONE newline at the round
    base, which the reviewer measured on the bytes; each append is therefore one
    newline followed by the slice. LEDGER19 carries TWO paragraphs separated by
    one blank line.
 3. C4 carries the door AND its pins TOGETHER, deliberately: a commit moving the
    door without its pins leaves the suite red, and one moving the pins without
    the door pins a status the door does not return — the reason D17 and D18
    both gave for refusing that cut. ONE logical step, kept whole.
 4. C4 APPLIES ALL 14 FROM/TO PAIRS FIRST, AND ONLY THEN THE THREE REPLACEMENTS
    OF CONSTRAINT 5. The order is load-bearing: two pins must NOT take the
    replacement's destination, and the pairs are what remove them from its
    reach. Running a replacement first corrupts them silently — finding R-0638.
 5. After all 14 pairs are applied, and ONLY in
    `tests/ui_server/test_command_channel.py`, make these three replacements over
    every remaining occurrence. The counts are the reviewer's, measured by
    applying this block's own slices to a throwaway tree; report what YOUR run
    replaced and do not adjust it to match:
      `[0] == 501`        -> `[0] == 200`        (reviewer measured 9)
      `status == 501`     -> `status == 200`     (reviewer measured 4)
      `"not_implemented"` -> `"accepted"`        (reviewer measured 4)
    `packages/orchestration/command_audit.py` and
    `tests/orchestration/test_command_audit.py` keep `not_implemented`: it stays
    in the closed vocabulary and `decision.resolve` still writes it. Run these
    replacements nowhere else.
 6. Commit order is C0a, C0b, C1, C2, C3, C4, C5 and is not negotiable.
 7. This round mints ONE id, R-0638, in LEDGER19, and resolves none. It PAYS
    R-0636 in code but writes NO `Done:` line for it: a payment certifies itself
    only after review. The next free id is R-0639 when this round ends.
 8. The `Fortschritt:` line above is relayed deliberately (finding R-0418); the
    handback's state block repeats it VERBATIM across all three of its lines.
 9. SIZE, measured at emission as DECISION F085 D6 requires both numbers to be:
    488 lines TOTAL against D6's 490 cap, 156 of them PROSE against D5's 400.
    Re-measure both from the committed C0a blob; a disagreement is a finding.

Done when — run every gate and record its REAL exit code and output:
 G1  Before C0a and again before C5: `.agent/STOP` is ABSENT,
     `git rev-parse --abbrev-ref HEAD` prints
     `feature/f009-single-write-channel`, and `git status --porcelain` prints 0
     lines after each of C0a through C4. Report the round base SHA you read at
     step 0.
 G2  TRANSPORT: `.agent/authored/f009-r19.md` at C0a and `.agent/last_block.md`
     at C0b are byte-equal to each other and to the block you received; report
     sha256, bytes and lines for both. C0b is written FROM the committed C0a
     blob, never from the scratch copy again.
 G3  SLICES: extract every slice from the COMMITTED C0a blob by its `<<<SLICE `
     and `<<<END ` marker lines with a script and apply them programmatically.
     Report each slice's sha256, bytes and lines plus the aggregate count your
     script printed. State no slice count you did not count.
 G4  `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R19 — report `cmp` exit and
     both sha256, with a negative control against another file exiting non-zero
     — and `wc -l` against the 50-line cap of AGENTS.md. Line-anchored,
     `^## Goal$` and `^## Next Steps$` each read 1.
 G5  APPENDS, under TWO independent readers each, with a negative control on the
     FIRST appended paragraph (finding R-0631). For C2 over
     `.agent/live_review.md` based on the round base, and for C3 over
     `.agent/decisions.md` based on the C2 tree: (a) the base blob is a
     byte-exact PREFIX and the remainder equals a newline plus the slice —
     report each remainder's sha256, bytes and lines; (b) N is counted BY YOUR
     SCRIPT and the last N blank-line units equal the slice's N paragraphs IN
     ORDER. Then flip one printable byte in the FIRST appended paragraph, at
     equal length, and report that BOTH readers REJECT the flip while both
     ACCEPT the true file, for BOTH appends. Report before/after bytes and lines.
 G6  Line-anchored at line START over `.agent/live_review.md` at the round base
     and at C2 (finding R-0630): a leading `- R-` id with every captured id
     DISTINCT at each; a leading `Done: R-` id; a leading `Landed: `; a leading
     `Gate: R` key over that many DISTINCT keys; the `Gate: R19` key; a leading
     `- R-0638` entry; and a leading `- R-0639` entry, which must read 0 at both
     because this round mints one id and it is not that one. Report each pair of
     readings, the max id, and the open count by DECISION F009 D10's rule at C2.
     Report what you measure, not what this sentence expects.
 G7  Line-anchored over `.agent/decisions.md` at the round base and at C3: a
     leading `## DECISION F009 D` number with every captured number DISTINCT at
     each, the `## DECISION ` total, and `## DECISION F009 D20`. Report both.
 G8  PAIRS, measured in the file each lands in, BEFORE and AFTER C4, both
     whole-line and indent-agnostic, the two readings AGREEING at every count:
     each FROM reads 1 before and 0 after; each TO reads 0 before and 1 after.
     Report the containment reading `TO contains FROM` for all 14 — the reviewer
     measured it TRUE for U1CONST alone, which appends constants after the block
     it quotes, and FALSE for the other 13; a different answer is a finding you
     report, not one you fix.
 G9  REPLACEMENTS: report, from YOUR script, how many occurrences each of the
     three replacements of constraint 5 changed, and that afterwards
     `[0] == 501`, `status == 501` and the quoted `not_implemented` each read 0
     in `tests/ui_server/test_command_channel.py` while the quoted `replayed`
     reads 1 — and that the quoted `not_implemented` still reads non-zero in
     `packages/orchestration/command_audit.py`, untouched by this round.
 G10 SUITES, run SERIALLY in the PRIMARY checkout, never two pytest processes at
     once and never in a worktree. Report each command's REAL exit code and the
     count IT printed — predict no number:
       `python3 -m ruff check packages/orchestration/ui_server.py
        tests/ui_server/test_command_channel.py`
       `python3 -m pytest tests/ui_server/ -q -rf`
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
        tests/regression/test_resource_safety.py
        tests/orchestration/test_integrity_gate.py -q -rf`
       `python3 -m pytest tests/orchestration/test_command_audit.py -q -rf`
     The reviewer ran ruff and all four at the round base first: each exits 0,
     so each can fail honestly (R-0364).
 G11 RANGE: the range from the round base to C4 lists EXACTLY the declared paths
     other than `.agent/handoff.md`, the set difference EMPTY in both directions,
     and 0 paths beginning `apps/` or `docs/`. Each commit has ONE parent;
     `git show --numstat` and `git diff --numstat` AGREE on every cell — invoke
     `git show` WITHOUT a `--` before the SHA, which turns it into a pathspec and
     prints nothing — a vacuous comparison the reviewer hit and fixed re-running
     R18; every cell equals the `+/-` column of the handback's `## Commits` table
     (checklist item 28), compared cell by cell. Report each pre-handback
     commit's insertions against the 500 cap of AGENTS.md DECISION F104 D1; the
     handback commit's own numbers belong in the round report (item 14). Leading
     `<<<SLICE ` and `<<<END ` read 0 LINES in EVERY file any slice lands in, a
     set the reviewer counted at five: `.agent/plan.md`,
     `.agent/live_review.md`, `.agent/decisions.md`,
     `packages/orchestration/ui_server.py` and
     `tests/ui_server/test_command_channel.py`. `git ls-files .remedy-wt` reads
     0. Classify THIS ROUND's reflog rows by the operation before the first `:`
     and report `amend`, `rebase` and `cherry` each 0; assert no total over the
     whole reflog (R-0601). Create NO worktree, so `git worktree list` prints 1.
 G12 The handback carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each of C0a, C0b,
     C1, C2, C3, C4 and C5, the round base SHA, one line per gate with the
     transcripts in the round report and not in the file (R-0582), and this
     block's `Fortschritt:` line VERBATIM. Report its `wc -l` against the 100
     lines a bundle of more than five commits allows.

Handback:    completion report + rewrite `.agent/handoff.md`. Push after C5.
             Create NO pull request: F009 opens one at its own closure.
─────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF009R19
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
R19 is round one of DECISION F009 D19: the door dispatches `job.stop` to
`safe_points.request_stop`, answers 200 with the body DECISION F009 D18 rules,
audits a raised effect as `rejected_effect`, pays R-0636 by moving the replay
token to `replayed`, and migrates the seam pins. `decision.resolve` keeps the
501 seam. DECISION F009 D20 rules the two arguments the client does not supply
and records the migration's MEASURED shape, correcting D19 per finding R-0638.

## Next Steps
1. Round two of D19: the effect assertions in a NEW file,
   `tests/ui_server/test_command_dispatch.py` — that the stop request the
   dispatch published exists and carries the door's source, that the nonce
   record holds the body the client received, and that a retry of the same
   nonce is audited `replayed`. Purely additive; it edits no existing test.
2. Then `decision.resolve` dispatches and the seam is gone; then the
   `command.accepted` SSE event; then the queue-only import guard, the
   per-command side-effect assertions and the route-walking 405 test; then the
   integration gate and closure.

## Risks
- `rejected_effect` is written from R19 but no shipped test reaches it; the
  reviewer's own worktree probe did, and round two owes it a permanent test.
- `test_an_audit_writer_that_raises_changes_neither_status_nor_body` submits the
  SAME default nonce in both of its loops, so its second seam call is now a
  REPLAY. R19 moves that site to `replayed` by its own FROM/TO pair.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
<<<END PLANF009R19

<<<SLICE LEDGER19
Gate: R19 — the R18 entry. R18 PASSED. Every gate was RE-EXECUTED by the reviewer off disk rather than read back out of the handback, and every value reproduced. TRANSPORT HELD: `.agent/authored/f009-r18.md` at `92d2d425` and `.agent/last_block.md` at `9ff14cfd` are both sha256 767befc4ca5932b45c1e8dedefef8f9472ff5972866e0b5ebd577bbdb7370934 over 20867 bytes and 200 lines, and byte-equal to each other. The reviewer's own ordered extraction out of the committed C0a blob gives 3 slices aggregating 11848 bytes over 60 lines — the same aggregate the handback printed — with PLANF009R18 at `cc3780d5…`, LEDGER18 at `69730c99…` and DECISION19 at `643cd1d9…`. `.agent/plan.md` at `b72c9aa4` is BYTE-EQUAL to PLANF009R18 at 48 lines against the 50-line cap, its negative control unequal, `^## Goal$` and `^## Next Steps$` reading 1 each. THE TWO APPENDS HOLD UNDER THE REVIEWER'S OWN TWO READERS EACH: at `f5b7d497` the round-base blob is a byte-exact prefix of `.agent/live_review.md` and the remainder is exactly a newline plus LEDGER18, sha256 `9c46ec16…` over 5407 bytes and 2 lines, the file going 480991 to 486398 bytes and 1094 to 1096 lines, N counted at 1 by the reviewer's own extractor; at `63b51e52` the C2 blob is a byte-exact prefix of `.agent/decisions.md` and the remainder is exactly a newline plus DECISION19, sha256 `9d00e7c2…` over 3612 bytes and 12 lines, the file going 454550 to 458162 bytes and 6845 to 6857 lines, N counted at 6. For BOTH appends, flipping byte 0 of the FIRST appended paragraph at equal length — `G` to `!` and `#` to `!` — makes BOTH readers REJECT while both ACCEPT the true file. THE SETS HELD line-anchored at line start, at the round base and at C2: entries matching a leading `- R-` id 203 and 203 with every id DISTINCT at each, leading `Done:` ids 3 at both, leading `Landed: ` 0 at both, leading `Gate: R` keys 17 and 18 over that many DISTINCT keys, the `Gate: R18` key 0 and 1, a leading `- R-0638` entry 0 at both, max id R-0637 at both, and 200 open by DECISION F009 D10's rule at both — a round that minted no id and resolved none, exactly as its constraint 4 required. Leading `## DECISION F009 D` numbers read 18 and 19 with every number DISTINCT, and the `## DECISION ` total 103 and 104. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout: the canary EXITS 0 at 42 passed and the four-path state-reader group EXITS 0 at 507 passed — the same two results the handback reported and neither of them predicted by it. THE NO-PRODUCTION-CODE CONSTRAINT IS A MEASUREMENT AND NOT A CLAIM: the range from the round base to C3 lists exactly the five declared paths with the set difference EMPTY in both directions and 0 paths beginning `packages/`, `apps/`, `tests/` or `docs/`. THE RANGE HELD: six single-parent commits; `git show --numstat` and `git diff --numstat` agree on every cell and every cell equals the `+/-` column of the handback's own tables, at 200/0, 97/219, 20/17, 2/0 and 12/0, compared cell by cell; pre-handback insertions 200, 97, 20, 2 and 12, every one under the 500 cap; zero `<<<SLICE ` and `<<<END ` LINES in all three slice targets; `git ls-files .remedy-wt` 0; this round's six reflog rows all classify as `commit` with `amend`, `rebase` and `cherry` each 0 and no total asserted over the whole reflog; one worktree throughout and a clean tree at the verdict; and `git ls-remote` shows the branch pushed to `aa1e2780`, the same SHA the reviewer read. The handback carries every mandated section of docs/agents/handback_template.md in order, an item-status row for each of C0a through C4, the round base SHA, one line per gate, and the block's `Fortschritt:` line verbatim across all three of its lines, at 90 lines against the 100 a bundle of more than five commits allows. NO DEVIATION WAS DECLARED AND NONE IS FOUND. One id is minted against the round's CONTENT rather than against its execution, R-0638, and it is registered below.

- R-0638 — Low — A DECISION'S SIZING PROSE CALLED THREE STRING MIGRATIONS "UNIFORM" WHEN ONLY ONE OF THEM IS, AND THE ROUND IT SIZED WOULD HAVE BEEN ORDERED ON THAT ARITHMETIC. DECISION F009 D19, committed at `63b51e52`, states that `[0] == 501` at 9 occurrences, `assert status == 501` at 7 and the quoted token `not_implemented` at 5 are "three uniform byte-string transformations the block can order once each and count", and `.agent/plan.md` at `b72c9aa4` repeats it. The reviewer re-measured all three at `aa1e2780` in `tests/ui_server/test_command_channel.py` by READING EVERY SITE rather than by counting the string. `[0] == 501` IS uniform: all 9 carry `job.stop` and all 9 become 200. The other two are NOT. `assert status == 501` has two sites that do not become 200 — the `decision.resolve` case at line 400, which keeps the seam because only `job.stop` is dispatched in D19's round one, and the exposed-subset loop at line 425, which spans BOTH exposed ids and has to split — so a single ordered replacement would have made two assertions claim that `decision.resolve` returns a status the door does not return, and the suite would have gone red on a test the block believed it was leaving alone. The quoted `not_implemented` has one site that becomes the quoted `replayed` and not the quoted `accepted`: the raising-writer test at line 777, whose second loop replays the first loop's default nonce, which is exactly the site finding R-0636 named as its payer. WHY LOW: THE DEFECT IS IN THE SIZING PROSE ALONE. D19's ruling — that the dispatch round splits in two, where the cut falls and why — is unaffected and stands, nothing false reached a source file, and the error was caught by the next round's own measurement before a single slice was authored. THE CLASS IS A COUNT STANDING IN FOR A PREDICATE: "occurs N times" was read as "is one transformation N times", and those are the same statement only when every site shares one destination — which is a property of the SITES, readable only by reading them, and never a property of the count. R-0492 is the nearest relative and it binds an inventory set to an AST predicate rather than to a grep; this is the same mistake made about a REWRITE rather than about a set. FIX, APPLIED THIS ROUND: DECISION F009 D20 records the measured site table, and the R19 block orders its 14 FROM/TO pairs BEFORE the three ordered replacements so that each replacement runs over a remainder whose destination really is single-valued — measured by the reviewer at 9, 4 and 4 by applying the block's own slices to a throwaway tree and reading what the script printed.
<<<END LEDGER19

<<<SLICE DECISION20
## DECISION F009 D20 — what `job.stop`'s dispatch passes to `request_stop`, what a raised effect answers on the wire, and the MEASURED shape of the pin migration (2026-08-22)

FIRST, THE TWO ARGUMENTS THE CLIENT DOES NOT SUPPLY. `safe_points.request_stop(job_id, reason, source)` takes two values that no part of a command submission names. CHOSEN: `source` is a new constant `COMMAND_EFFECT_SOURCE` carrying the value `ui`, and `reason` is the `reason` member of `args` when it is a `str` and the empty string otherwise. The source is fixed rather than client-supplied because it is the field that tells a stop asked for through the UI apart from one asked for by `remedy job stop`, and a client that could set it could erase that distinction inside the archived signal itself. The reason DEGRADES rather than raising because `args` is client-supplied and DECISION F009 D14's shape check types the object but not its contents; `_bounded` in `safe_points` already truncates an over-long one, so the only case left to rule is a non-string, and answering 500 for it would turn a well-formed request into a server fault. ALTERNATIVE: reject a non-string reason as a 400 shape error — rejected because `args` is per-command and this door deliberately does not know any command's argument schema, which is the property DECISION F009 D5's import guard exists to keep.

SECOND, WHAT A RAISED EFFECT PUTS ON THE WIRE. DECISION F009 D18 clause four already ruled the token `rejected_effect`, the `create=True` audit and the status 500; it did not name the body. CHOSEN: a new constant `COMMAND_EFFECT_FAILED_MESSAGE` carrying the sentence "command could not be carried out", sent through the existing `_safe_error` path. The exception's own text never reaches the wire: it is written by code this door does not own and may name a control path the client has no business learning.

THIRD, THE MEASURED SHAPE OF THE PIN MIGRATION, which corrects this decision's predecessor. Finding R-0638 records that DECISION F009 D19 called three string migrations uniform when only one of them is. MEASURED at `aa1e2780`, first by reading every site and then by applying the R19 block's own slices to a throwaway tree: 14 FROM/TO pairs are applied FIRST, and only then do three ordered replacements run over what is left — `[0] == 501` to `[0] == 200` at 9 sites, `status == 501` to `status == 200` at 4, and the quoted `not_implemented` to the quoted `accepted` at 4. The two counts that differ from D19's are not a correction of its arithmetic but a consequence of the ordering: the pairs consume the sites whose destination differs, and that is precisely what leaves the remainder single-valued and the replacement safe. RULE, binding on every later round of this feature: a block may order a repository-wide string replacement only over a remainder it has first made single-valued, and the count it states must be one a dry run PRINTED rather than one a grep suggested.

REVERSE the first clause by making `source` client-supplied, which requires re-reading D14's shape check first; the second by pinning a different message, which no test outside this feature reads; the third only by finding a site the measurement missed, in which case that site is the correction and this paragraph is the record of how the count was taken.
<<<END DECISION20

<<<SLICE U1CONST_FROM
#: The refusal a client over its budget receives. It mirrors the shape the SSE
#: door's own 429 already uses, so both limits read the same way on the wire.
COMMAND_RATE_LIMIT_MESSAGE = "too many commands for this job"
<<<END U1CONST_FROM
<<<SLICE U1CONST_TO
#: The refusal a client over its budget receives. It mirrors the shape the SSE
#: door's own 429 already uses, so both limits read the same way on the wire.
COMMAND_RATE_LIMIT_MESSAGE = "too many commands for this job"

#: What an effect that RAISED answers (DECISION F009 D18 clause four, D20). The
#: exception's own text never reaches the wire: it is written by code this door
#: does not own and may name a control path the client may not learn.
COMMAND_EFFECT_FAILED_MESSAGE = "command could not be carried out"

#: The `source` every effect dispatched here is attributed to, so a UI stop is
#: told apart from a `remedy job stop` inside the signal (DECISION F009 D20).
COMMAND_EFFECT_SOURCE = "ui"

#: The one id this door dispatches for real; `decision.resolve` still answers the
#: seam. Named rather than inlined so its second call site greps to this line.
JOB_STOP_COMMAND_ID = "job.stop"
<<<END U1CONST_TO

<<<SLICE U2REPLAY_FROM
            # D15 orders the replay audited with the outcome the ORIGINAL attempt
            # carried. While the 501 seam stands nothing at this door publishes a
            # record (D15's first half), so the only result a nonce can hold is the
            # seam's own and `not_implemented` IS that outcome. D14 reserves
            # `accepted` for the round that retires the seam; that round adds the
            # publish call site and moves this token in the same change.
            self._audit_attempt(str(job.id), "not_implemented", create=True,
                                payload=payload)
<<<END U2REPLAY_FROM
<<<SLICE U2REPLAY_TO
            # D15 audits the replay with the ORIGINAL attempt's outcome, and finding
            # R-0636 rules what that token may be: a replay REPEATS an acceptance
            # rather than being one, so `replayed` is its own token. T5_F035 and
            # T9_F167 read this file to count what the door did, and one token for
            # both events would make them indistinguishable to both. R-0636's payer.
            self._audit_attempt(str(job.id), "replayed", create=True,
                                payload=payload)
<<<END U2REPLAY_TO

<<<SLICE U3DISPATCH_FROM
        # The seam: DECISION F009 D5's effect table replaces this answer with a
        # real dispatch, and the round that lands that table is the one that
        # retires the seam. Until then 501 is the honest status — the door
        # authenticates, validates and now also checks the exposed subset, but
        # an accepted command still has no effect to run. `accepted` is therefore
        # NOT the outcome written here: nothing has been accepted yet.
        self._audit_attempt(str(job.id), "not_implemented", create=True, payload=payload)
        self._send_json(501, {
            "error": "command channel not yet accepting commands",
            "command": payload["command"],
        })
<<<END U3DISPATCH_FROM
<<<SLICE U3DISPATCH_TO
        # D5 maps `job.stop` to `safe_points.request_stop`; D18 fixes the order of
        # the three writes an ACCEPTED command performs: the effect FIRST, since
        # the body is unknown until it returns; then the `accepted` audit line,
        # since the record of what this door did must not depend on a store whose
        # key the client picks; then the publication LAST, since D8's replay
        # returns the ORIGINAL result and there is none before the other two.
        if payload["command"] == JOB_STOP_COMMAND_ID:
            try:
                accepted_body = self._dispatch_job_stop(str(job.id), payload)
            except (OSError, RuntimeError, ValueError, TypeError):
                # D18, clause four: an effect that RAISED is neither `accepted`,
                # which would be false, nor unaudited, which would break D6.
                self._audit_attempt(str(job.id), "rejected_effect", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE))
                return
            # D18, clause three: BOTH writes below fail SOFT. The stop is already
            # durable, so refusing after the fact would report a stop that really
            # was requested as one that was not.
            self._audit_attempt(str(job.id), "accepted", create=True, payload=payload)
            self._publish_command_result(str(job.id), payload["client_nonce"],
                                         accepted_body)
            self._send_json(200, accepted_body)
            return
        # `decision.resolve` keeps the seam until its own round: D5 maps it to
        # `answer_task_decision` followed by `save_job`, and that effect is not
        # wired here yet, so 501 is still the honest status for it.
        self._audit_attempt(str(job.id), "not_implemented", create=True, payload=payload)
        self._send_json(501, {
            "error": "command channel not yet accepting commands",
            "command": payload["command"],
        })

    def _dispatch_job_stop(self, job_id: str, payload: Any) -> dict[str, Any]:
        """Run `job.stop`'s effect and build the body DECISION F009 D18 rules for it.

        DECISION F009 D20 rules the two arguments no client supplies: `source` is
        this door, and a non-string `reason` degrades to "" rather than raising,
        because D14 types `args` as an object but never types what is inside it.
        """
        from packages.orchestration.safe_points import request_stop
        args = payload.get("args")
        reason = args.get("reason") if isinstance(args, dict) else ""
        signal = request_stop(
            job_id, reason=reason if isinstance(reason, str) else "",
            source=COMMAND_EFFECT_SOURCE)
        return {"command": payload["command"], "outcome": "accepted",
                "request_id": signal.request_id}

    def _publish_command_result(self, job_id: str, client_nonce: str,
                                body: dict[str, Any]) -> None:
        """Publish one accepted result under its nonce. NEVER changes the response.

        D18 clause three: a failed publication leaves a client whose retry re-runs
        the command, tolerable only because every effect in D5's table is
        idempotent at its own layer — `request_stop` provably so.
        """
        from packages.orchestration.command_nonce import publish_nonce_result
        try:
            publish_nonce_result(job_id, client_nonce, body, status=200)
        except (OSError, RuntimeError, ValueError, TypeError):   # D18, clause three
            return
<<<END U3DISPATCH_TO

<<<SLICE P_A_RESOLVE_FROM
        assert status == 501
        assert body["command"] == "decision.resolve"
<<<END P_A_RESOLVE_FROM
<<<SLICE P_A_RESOLVE_TO
        assert (status, body["command"]) == (501, "decision.resolve")
<<<END P_A_RESOLVE_TO

<<<SLICE P_B_SUBSET_FROM
    def test_every_exposed_command_reaches_the_seam(self):
        """The set itself is the contract, not the two literals above."""
        from apps.cli.command_catalog import UI_EXPOSED_COMMANDS

        port, token = self._start_server()
        for index, command_id in enumerate(sorted(UI_EXPOSED_COMMANDS)):
            status, body = self._request(
                port, "POST", self._commands_path(),
                body=self._valid_body(
                    command=command_id, client_nonce=f"nonce-exposed-{index}"),
                headers=self._auth_headers(token))
            assert status == 501, command_id
            assert body["command"] == command_id
<<<END P_B_SUBSET_FROM
<<<SLICE P_B_SUBSET_TO
    def test_every_exposed_command_reaches_the_answer_its_effect_gives(self):
        """The set itself is the contract, not the two literals above.

        `job.stop` dispatches and answers 200; `decision.resolve` keeps the seam
        until its own round, which is then ONE edit to the expectation below.
        """
        from apps.cli.command_catalog import UI_EXPOSED_COMMANDS

        port, token = self._start_server()
        for index, command_id in enumerate(sorted(UI_EXPOSED_COMMANDS)):
            status, body = self._request(
                port, "POST", self._commands_path(),
                body=self._valid_body(
                    command=command_id, client_nonce=f"nonce-exposed-{index}"),
                headers=self._auth_headers(token))
            expected = 200 if command_id == "job.stop" else 501
            assert status == expected, command_id
            assert body["command"] == command_id
<<<END P_B_SUBSET_TO

<<<SLICE P_C_CALLS_FROM
        # The mutation must REACH the door, or the comparison above proves nothing.
        assert calls == ["rejected_token", "rejected_csrf", "not_implemented"], calls
<<<END P_C_CALLS_FROM
<<<SLICE P_C_CALLS_TO
        # The mutation must REACH the door, or the comparison above proves nothing.
        # The third call is a REPLAY, not an acceptance: both loops submit the same
        # default nonce, so the first loop published it and the second one hits it.
        assert calls == ["rejected_token", "rejected_csrf", "replayed"], calls
<<<END P_C_CALLS_TO

<<<SLICE P_D_GUARD_FROM
        assert "accepted" not in outcomes, "nothing is accepted while the 501 seam stands"
<<<END P_D_GUARD_FROM
<<<SLICE P_D_GUARD_TO
        assert "accepted" in outcomes, "the dispatched job.stop was never accepted"
<<<END P_D_GUARD_TO

<<<SLICE P_E_WELLFORMED_FROM
    def test_well_formed_command_reaches_the_501_seam(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(), body=self._valid_body(),
            headers=self._auth_headers(token))
        assert status == 501
        assert body["error"] == "command channel not yet accepting commands"
        assert body["command"] == "job.stop"
<<<END P_E_WELLFORMED_FROM
<<<SLICE P_E_WELLFORMED_TO
    def test_well_formed_command_is_dispatched_and_accepted(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(), body=self._valid_body(),
            headers=self._auth_headers(token))
        assert status == 200
        assert body["outcome"] == "accepted"
        assert body["command"] == "job.stop"
<<<END P_E_WELLFORMED_TO

<<<SLICE P_F_ARGSNAME_FROM
    def test_present_args_object_is_valid_and_reaches_the_seam(self):
<<<END P_F_ARGSNAME_FROM
<<<SLICE P_F_ARGSNAME_TO
    def test_present_args_object_is_valid_and_is_accepted(self):
<<<END P_F_ARGSNAME_TO

<<<SLICE P_G_AUDITNAME_FROM
    def test_the_seam_is_audited_as_not_implemented(self):
<<<END P_G_AUDITNAME_FROM
<<<SLICE P_G_AUDITNAME_TO
    def test_a_dispatched_command_is_audited_as_accepted(self):
<<<END P_G_AUDITNAME_TO

<<<SLICE P_H_UNSEEDED_FROM
    def test_an_unseeded_nonce_still_reaches_the_seam(self):
        """The lookup must MISS by default, or the door would answer from an empty store."""
        port, token = self._start_server()
        status, body = self._post_command(port, token, "nonce-unseeded")
        assert status == 501
        assert body["error"] == "command channel not yet accepting commands"
<<<END P_H_UNSEEDED_FROM
<<<SLICE P_H_UNSEEDED_TO
    def test_an_unseeded_nonce_is_dispatched_rather_than_replayed(self):
        """The lookup must MISS by default, or the door would answer from an empty store."""
        port, token = self._start_server()
        status, body = self._post_command(port, token, "nonce-unseeded")
        assert status == 200
        assert body["outcome"] == "accepted"
<<<END P_H_UNSEEDED_TO

<<<SLICE P_I_REPLAYNAME_FROM
    def test_a_replay_never_reaches_the_seam(self):
<<<END P_I_REPLAYNAME_FROM
<<<SLICE P_I_REPLAYNAME_TO
    def test_a_replay_is_not_the_acceptance_it_repeats(self):
<<<END P_I_REPLAYNAME_TO

<<<SLICE P_I_REPLAYBODY_FROM
        assert seam == (501, {"error": "command channel not yet accepting commands",
                              "command": "job.stop"})
<<<END P_I_REPLAYBODY_FROM
<<<SLICE P_I_REPLAYBODY_TO
        assert seam[0] == 200
        assert seam[1]["outcome"] == "accepted"
        assert seam[1]["command"] == "job.stop"
<<<END P_I_REPLAYBODY_TO

<<<SLICE P_J_SEEDDOC_FROM
        DECISION F009 D15 leaves the door with NO publish call site while the 501 seam
        stands, so a replay test seeds through the store's own publish function rather
        than through a test-only path: production code exercised by production means.
        """
<<<END P_J_SEEDDOC_FROM
<<<SLICE P_J_SEEDDOC_TO
        The door publishes for itself from R19 onward, but only for the ids it
        dispatches. This helper seeds a result directly so that a replay test can
        name the stored body it expects, byte for byte, instead of depending on
        whatever the effect of the moment happens to return.
        """
<<<END P_J_SEEDDOC_TO
