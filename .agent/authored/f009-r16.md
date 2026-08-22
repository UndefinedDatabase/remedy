── STEP T003 (record round, between rounds 1 and 2 of DECISION F009 D17) — F009 ──
Goal:        Put this session's remaining judgements on disk before the session
             ends. The round records the R15 verdict, resolves R-0637 with the
             reviewer's own verification, and adds the three R15 recurrences to
             the OPEN findings that already describe them. It writes NO
             production code, which is what it exists for: a verdict that lives
             only in a session's chat is lost when that session ends.

Fortschritt: ~70 % (T001 gebaut · T002 gebaut, jetzt mit Publikations-Bound ·
             T003 begonnen: Extraktion und Vorbedingungen stehen, der Dispatch
             fehlt) — Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R15 verdict
             and the three recurrences · C3 resolve R-0637 · C4 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f009-r16.md` (NEW, C0a)
             `.agent/last_block.md` (C0b)
             `.agent/plan.md` (C1)
             `.agent/live_review.md` (C2, C3)
             `.agent/handoff.md` (C4)
             NOTHING under `packages/`, `apps/`, `tests/` or `docs/` is touched.
             This round writes no production code and pays no finding in code.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. C2 is an APPEND to `.agent/live_review.md`. C3 is the ONE sanctioned
    non-append edit to that file: docs/agents/planner_reviewer_prompt.md §4.4
    requires the reviewer's `Done:` text to REPLACE the worker's `Landed:`
    line, and commit `29ee4b08` on this branch is the precedent — a 1-line-for-
    1-line replacement. DONE0637_FROM is that whole single line; it occurs
    EXACTLY ONCE in the file at the round base, which the reviewer measured.
    Nothing else in the file is touched by either commit.
 3. The pair DONE0637_FROM → DONE0637_TO was classified MECHANICALLY before
    emission: the script printed `TO contains FROM: false`, so it is a REWRITE
    and carries the FROM-0x / TO-1x obligation, not an append obligation.
 4. Commit order is C0a, C0b, C1, C2, C3, C4 and is not negotiable. C1 is the
    first substantive commit because this round writes the finding ledger and
    the plan must be current before it (§3 item 23).
 5. This round mints NO new finding id. All three R15 recurrences are added to
    findings the open set ALREADY holds — R-0585, R-0629 and R-0418 — because
    §3 item 30 requires the open set to be searched for the DEFECT before an id
    is minted, and the reviewer searched it and found all three. The next free
    id is therefore still R-0638 when this round ends.
 6. The `Fortschritt:` line above is relayed deliberately. The R15 block carried
    none, the worker had to declare that as an assumption, and finding R-0418 is
    exactly that defect; the handback's state block repeats this line VERBATIM.

Done when — run every gate and record its REAL exit code and output:
 G1  Before C0a and again before C4: `.agent/STOP` is ABSENT,
     `git rev-parse --abbrev-ref HEAD` prints
     `feature/f009-single-write-channel`, and `git status --porcelain` prints 0
     lines after each of C0a through C4. Report the round base SHA you read at
     step 0.
 G2  TRANSPORT: `.agent/authored/f009-r16.md` at C0a and `.agent/last_block.md`
     at C0b are byte-equal to each other and to the block you received. Report
     sha256, byte count and line count for both. C0b is written FROM the
     committed C0a blob, never from the scratch copy again.
 G3  SLICES: extract every slice from the COMMITTED C0a blob by its
     `<<<SLICE ` and `<<<END ` marker lines with a script, and apply them
     programmatically. Report each slice's sha256, bytes and lines, plus the
     aggregate count your script printed. State no slice count you did not
     count.
 G4  `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R16 — report `cmp` exit
     and both sha256 — and `wc -l` reads it against the 50-line cap of
     AGENTS.md. Line-anchored, `^## Goal$` and `^## Next Steps$` each read 1.
 G5  APPEND, under TWO independent readers with a negative control on the FIRST
     appended paragraph (finding R-0631). For C2 over `.agent/live_review.md`
     with the round base as base: (a) the base blob is a byte-exact PREFIX and
     the remainder equals a newline plus LEDGER16 — report the remainder's
     sha256, bytes and lines; (b) N is counted BY YOUR SCRIPT, not asserted,
     and the last N blank-line units of the file equal LEDGER16's N paragraphs
     IN ORDER. Then flip one printable byte in the FIRST appended paragraph and
     report that BOTH readers REJECT the flip while both accept the true file.
     Report the before/after byte and line counts.
 G6  C3 IS A REPLACEMENT, NOT AN APPEND, so prove it as one. At C3 in
     `.agent/live_review.md`: DONE0637_FROM reads 0 and DONE0637_TO reads 1,
     with the whole-line and the indent-agnostic counts BOTH taken and
     AGREEING. Then show that the C2 blob of that file with the single pair
     applied is BYTE-EQUAL to what C3 landed, so no other byte of the file
     changed. Report `git show --numstat` for C3 over that path and state
     whether it reads 1 insertion and 1 deletion.
 G7  Line-anchored over `.agent/live_review.md` at the round base and at C3
     (finding R-0630 — state that the anchor is line-start): `^- R-\d+ — ` with
     every captured id DISTINCT at each; `^Done: R-\d+ — `; `^Landed: `;
     `^Gate: R\d+ — ` over that many DISTINCT keys; `^Gate: R16 — `; and
     `^- R-0638 — `, which must read 0 at both because this round mints no id.
     Report each pair of readings, the max id, and the open count by DECISION
     F009 D10's rule — line-anchored entries minus line-anchored `Done:` lines
     — at C3. The `Done:` reading is EXPECTED to rise by one and the `Landed:`
     reading to fall to 0; report what you measure, not what this sentence
     predicts.
 G8  The three findings this round adds evidence to are named in LEDGER16 and
     each already exists: report `^- R-0585 — `, `^- R-0629 — ` and
     `^- R-0418 — ` each reading 1 at the round base, line-anchored. This gate
     exists because §3 item 30 forbids a second id for a defect the open set
     already holds, and a claim that an id is already there is worth measuring.
 G9  SUITES, run SERIALLY in the PRIMARY checkout, never two pytest processes
     at once and never in a worktree. Report each command's REAL exit code and
     the count IT printed — predict no number:
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
        tests/regression/test_resource_safety.py
        tests/orchestration/test_integrity_gate.py -q -rf`
     The canary is unconditional and the four-path group is owed because this
     round's change set holds `.agent/` state files (finding R-0607). The
     reviewer ran both at the round base before ordering them: each exits 0, so
     each can fail honestly.
 G10 RANGE: the range from the round base to C3 lists EXACTLY the four declared
     paths other than `.agent/handoff.md` — `.agent/authored/f009-r16.md`,
     `.agent/last_block.md`, `.agent/plan.md` and `.agent/live_review.md` — the
     set difference EMPTY in both directions, and holds 0 paths beginning
     `packages/`, `apps/`, `tests/` or `docs/`, which is this round's
     no-production-code constraint as a measurement. Each commit has ONE
     parent; `git show --numstat` and `git diff --numstat` AGREE on every cell;
     every cell equals the `+/-` column of the handback's `## Commits` table
     (§3 item 28) — compare them cell by cell and say so. Report each
     pre-handback commit's insertions against the 500 cap of AGENTS.md DECISION
     F104 D1; the handback commit's own numbers belong in the round report, not
     here (§3 item 14). `^<<<SLICE ` and `^<<<END ` read 0 lines in BOTH files
     any slice lands in — `.agent/plan.md` and `.agent/live_review.md`; that
     set has two members and the reviewer counted it. `git ls-files .remedy-wt`
     reads 0. Classify THIS ROUND's reflog rows by the operation before the
     first `:` and report `amend`, `rebase` and `cherry` each reading 0; assert
     no total over the whole reflog (finding R-0601). Create NO worktree: no
     gate this round needs one, so `git worktree list` prints 1 line throughout.
 G11 The handback carries every mandated section of
     docs/agents/handback_template.md, an item-status table with exactly one
     row for each of C0a, C0b, C1, C2, C3 and C4, the round base SHA, one line
     per gate with the transcripts in the round report rather than in the file
     (finding R-0582), and the `Fortschritt:` line of this block VERBATIM.
     Report its `wc -l` against the 100 lines a bundle of more than five
     commits allows.

Handback:    completion report + rewrite `.agent/handoff.md`. Push after C4.
             Create NO pull request: F009 opens one at its own closure. This is
             the LAST round of the session; the handback's `## Next` names
             Phase 1 rule 1 (the `.agent/STOP` re-read) as the next session's
             FIRST action and the Open PR Gate as its SECOND.
─────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF009R16
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
R16 closes this session and writes no production code. It records the R15
verdict, resolves R-0637 with the reviewer's own verification, and adds the
three R15 recurrences to the open findings that already describe them — no new
id is minted. The nonce store's publication bound and the `accepted` and
`replayed` audit tokens landed at R15.

## Next Steps
1. Round 2 of DECISION F009 D17: `packages/orchestration/ui_server.py`
   dispatches `job.stop` to `safe_points.request_stop`, writes the `accepted`
   outcome, publishes the nonce record, and moves the replay audit token to
   `replayed`, which pays R-0636. The seam pins in
   `tests/ui_server/test_command_channel.py` migrate in that same round —
   roughly seventeen sites, which is why D17 gave that round its own budget.
   `decision.resolve` keeps answering 501.
2. Then `decision.resolve` dispatches and the seam is gone; then the
   `command.accepted` SSE event; then the queue-only import guard, the
   per-command side-effect assertions and the route-walking 405 test; then the
   integration gate and closure.

## Risks
- The door will briefly dispatch one exposed id and refuse the other with 501.
  That is honest, but the tests must assert it deliberately rather than inherit
  it, and `test_every_exposed_command_reaches_the_seam` loops over both ids and
  must be split when that round lands.
- `accepted` and `replayed` are in the vocabulary with no caller. The door's own
  guard still asserts it writes no `accepted`, which keeps the gap visible.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
<<<END PLANF009R16

<<<SLICE LEDGER16
Gate: R16 — the R15 entry. R15 PASSED. Every gate was RE-EXECUTED by the reviewer off disk rather than read back out of the handback, and every value reproduced. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f009-r15.md` at `89919dbd` and `.agent/last_block.md` at `4ea0aef3` are both sha256 9267d80767b2069481d1cfdf66363804f9ae832dec5086653f9734da03b22f15 over 30644 bytes and 429 lines, and the reviewer compared them not merely against the digest it had recorded but against the emitted bytes THEMSELVES, which were still on disk — `cmp`-against-original, not the digest fallback of §4.9. The reviewer's own ordered extraction out of the committed C0a blob gives 16 slices aggregating 18149 bytes over 206 lines, the same aggregate the handback printed. `.agent/plan.md` at `c92a41b7` is BYTE-EQUAL to PLANF009R15 at 43 lines against the 50-line cap, `^## Goal$` and `^## Next Steps$` reading 1 each. THE APPENDS HOLD UNDER THE REVIEWER'S OWN READERS: at `db2c6c23` the base blob is a byte-exact prefix and the remainder is exactly a newline plus LEDGER15, sha256 `09ef4431…` over 4343 bytes and 2 lines, the file going 463574 to 467917 bytes and 1086 to 1088 lines; at `5188259d` the C2 blob is a byte-exact prefix and the remainder is exactly a newline plus DECISION17, sha256 `d3d79605…` over 4121 bytes and 16 lines, the file going 445935 to 450056 bytes and 6811 to 6827 lines. THE CODE IS EXACTLY THE AUTHORED SLICES AND NOTHING MORE, which is the reading that matters for a round that touches `packages/`: the reviewer rebuilt each of the four changed files from its round-base blob by applying only the authored pairs, and all four reconstructions are BYTE-EQUAL to what landed — `command_nonce.py` and `test_command_nonce.py` at `f52d6534`, `command_audit.py` and `test_command_audit.py` at `8604e557`. For `tests/orchestration/test_command_nonce.py` the three-reading proof holds as the block ordered it: the round-base blob is NOT a prefix of the result, the blob with NONCE_TESTIMPORT applied alone IS a byte-exact prefix, NONCE_TESTAPPEND is an exact suffix, and the landed file equals prefix plus slice with nothing between. THE SETS HELD line-anchored at the round base and at C6: `^- R-\d+ — ` 203 and 203 with every id DISTINCT at each, `^Done: R-\d+ — ` 2 at both, `^Landed: R-\d+ — ` 0 and 1, `^Gate: R\d+ — ` 14 and 15 over that many DISTINCT keys, `^Gate: R15 — ` 0 and 1, max id R-0637, and 201 open by DECISION F009 D10's rule. `^## DECISION F009 D\d+ — ` reads 16 and 17 with every number DISTINCT, and the `^## DECISION ` total 101 and 102. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout: ruff over the four changed paths EXITS 0, the nonce and audit pair EXITS 0 at 45 passed, the canary EXITS 0 at 42 passed and the four-path state-reader group EXITS 0 at 507 passed — the same four results the handback reported and not one of them predicted by it. THE RED CONTROLS ARE REAL, and the reviewer had run both itself in a disposable worktree BEFORE the round was delegated: removing the publication bound fails exactly `test_a_record_over_the_bound_is_refused_at_publication` and `test_the_bound_refuses_before_the_store_is_created`, and removing the two vocabulary tokens fails exactly `test_the_outcome_vocabulary_is_the_closed_set_d14_ruled` — so the three tests this round ships genuinely reach the code it changed. THE DOOR IS UNTOUCHED, which this round existed to guarantee: the range holds 0 paths equal to `packages/orchestration/ui_server.py` and 0 under `tests/ui_server/`, and that suite passes UNMODIFIED inside the 507. THE RANGE HELD: nine single-parent commits over exactly the nine declared paths plus the handback's own, the set difference empty in both directions, pre-handback insertions 429, 395, 18, 2, 16, 58, 14 and 2, every one under the 500 cap; zero `^<<<SLICE ` and `^<<<END ` lines in all seven slice targets; `git ls-files .remedy-wt` 0; a clean tree and one worktree. THREE DEVIATIONS WERE DECLARED AND ALL THREE ARE THE REVIEWER'S OWN BLOCK DEFECTS, found by the worker, confirmed by the reviewer's measurement, and each belonging to a finding THIS RECORD ALREADY HOLDS OPEN — so no id is minted for any of them, on §3 item 30's rule that the open set is searched for the DEFECT and not merely for an id. FIRST, G12 ordered the marker count over "ALL SIX committed targets" while the slice-target set is SEVEN files; all seven read 0, so the property held over a set one larger than the numeral, and the gate named no list a reader could have checked the numeral against. That is R-0585 recurring — a done-when counting a list it does not name — and its counter-measure, prefer naming the list over counting it, is what would have caught it. SECOND, G11a stated that the bare line `    return None` occurs 14 times in `command_nonce.py` at C4; measured whole-line at its real eight-space indent it occurs 12, and 14 is the indent-agnostic reading, so the gate stated one numeral without naming which of the two readings produced it. The block's point stands under both — the bare line is not unique, the three-line sequence is, and the reviewer re-measured that sequence at 1 under both readings — but R-0629's counter-measure is precisely that a destructive control's target is counted under BOTH readings with both reported, and only one was. That is R-0629 recurring inside the block that was obeying it. THIRD, the R15 block relayed NO `Fortschritt:` line while its own G13 ordered the handback to carry one, so the worker correctly declared an assumption and carried R14's line forward verbatim rather than inventing a number. That is R-0418 exactly — a self-drive block that does not carry the operator brief leaves the worker with no source for it — and the R16 block that carries this entry ships a `Fortschritt:` slice, which is the counter-measure applied rather than merely recorded. NONE of the three put a false statement on disk: each was measured and declared by the worker before the reviewer looked, which is the handback working as designed. NO NEW CHECKLIST ITEM IS PROPOSED, on R-0635's and R-0597's reasoning: all three counter-measures are already on disk, and a checklist that grows an entry every time an existing entry goes unrun protects nothing.
<<<END LEDGER16

<<<SLICE DONE0637_FROM
Landed: R-0637 — `publish_nonce_result` now serialises the record first and returns None when it exceeds `MAX_NONCE_RECORD_BYTES`, so a record `_read_record` could never replay is refused at publication instead of written; landed at `f52d6534` with three tests in `tests/orchestration/test_command_nonce.py` covering over, at and before-the-store.
<<<END DONE0637_FROM

<<<SLICE DONE0637_TO
Done: R-0637 — Resolved at `f52d6534`, and the resolution was verified by the reviewer's own red control rather than accepted from the handback. `publish_nonce_result` now serialises the record BEFORE it opens anything, refuses it with `None` when the serialised form exceeds `MAX_NONCE_RECORD_BYTES`, and passes those same bytes to `write_file_atomically` instead of serialising a second time — so a record `_read_record` would refuse at every later lookup is never written, and the refusal takes the same `None` route every other unusable input to that function already takes. The finding asked for three things and all three landed: the bound is enforced at the WRITE side, the constant's own comment now states the rule in terms of the RESPONSE this store holds rather than the request the client sent, and the write side gained the negative control it had never had. MEASURED BY THE REVIEWER in a disposable worktree, at content byte-identical to what landed: with the two guard lines deleted, `tests/orchestration/test_command_nonce.py` EXITS 1 and fails exactly `test_a_record_over_the_bound_is_refused_at_publication` and `test_the_bound_refuses_before_the_store_is_created`, and restored it EXITS 0 — so the shipped tests genuinely reach the guard rather than passing beside it. The third test, `test_a_record_at_the_bound_still_publishes`, pins the boundary as an upper bound rather than an off-by-one and solves its own padding with `secure_fs.json_bytes` at the same arguments `_record_bytes` uses, so its arithmetic cannot drift away from production's serialiser. R-0637's fix clause said the repair was owed "in the same commit that adds the publish call site"; it landed one round EARLIER instead, which DECISION F009 D17 rules and which is strictly stronger — the bound is in force before any door path can reach publication, so the window in which an unreplayable record could be written is never opened rather than closed on arrival.
<<<END DONE0637_TO
