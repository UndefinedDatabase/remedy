── STEP T003 (rule the `decision.resolve` effect, land its audit token) — F009 ──
Goal:        Rule DECISION F009 D21 and land the ONE vocabulary token it needs,
             touching NO door. D21 fixes what `decision.resolve`'s effect is and
             where it becomes durable, performs the re-examination of D18's
             clause three that D18 itself names as this round's obligation, and
             rules the refusal that did not raise. The token `rejected_state`
             lands in `packages/orchestration/command_audit.py` one round ahead
             of its writer — the convention D17 set for `accepted` and
             `replayed` and D18 followed for `rejected_effect` — so that R23,
             which retires the 501 seam, changes the door alone.

Fortschritt: ~84 % (T001 gebaut · T002 gebaut · T003 begonnen: der
             `job.stop`-Dispatch steht und ist wirkungsgeprüft, die
             `decision.resolve`-Wirkung ist geregelt; offen bleiben der Dispatch
             selbst, das SSE-Event, der Import-Guard und die 405-Routenprobe) —
             Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R21 verdict ·
             C3 DECISION F009 D21 · C4 the `rejected_state` token and its pin ·
             C5 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f009-r22.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `.agent/decisions.md` (C3) · `packages/orchestration/command_audit.py`
             and `tests/orchestration/test_command_audit.py` (C4) ·
             `.agent/handoff.md` (C5). NOTHING under `apps/` or `docs/` is
             touched, and `packages/orchestration/ui_server.py` is NOT touched:
             this round rules the door's behaviour and does not write it.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. TWO APPENDS. C2 appends LEDGER22 to `.agent/live_review.md`; C3 appends
    DECISION21 to `.agent/decisions.md`. The reviewer measured BOTH targets on
    the bytes at the round base: each ends in exactly ONE newline, so each
    append is one newline followed by the slice. LEDGER22 carries ONE paragraph
    and DECISION21 carries TEN, separated by single blank lines.
 3. FOUR FROM/TO PAIRS, and they are the whole of C4. The reviewer CLASSIFIED
    every one of them before writing the gate that measures them, which is
    finding R-0639's binding fix: for all four the TO does NOT contain the FROM
    as a contiguous line block, because each TO either replaces the FROM's only
    line or inserts new lines INSIDE it. None is append-shaped, so the
    after-clause for all four is "the FROM reads 0 and the TO reads 1" —
    measure it, do not assume it.
 4. Commit order is C0a, C0b, C1, C2, C3, C4, C5 and is not negotiable. C1
    precedes the ledger because the plan must be current before it (checklist
    item 23), and C3 precedes C4 because a token's ruling lands before the
    vocabulary that carries it.
 5. This round mints NO id and resolves none: R21 was clean and LEDGER22 is a
    verdict paragraph with no finding under it. It writes no `Done:` line. The
    next free id is R-0641 when this round ends, exactly as when it started.
 6. The `Fortschritt:` line above is relayed deliberately (finding R-0418); the
    handback's state block repeats it VERBATIM across all FIVE of its lines.
    Five is the reviewer's own count of this block's bytes.
 7. SIZE, measured at emission by reading it back out of the assembled bytes and
    computing PROSE as TOTAL minus the slices' CONTENT lines, with marker lines
    counted as prose per DECISION F085 D5, which is finding R-0640's fix: this
    block is 282 lines TOTAL against DECISION F085 D6's 490 cap, 193 of them
    PROSE against D5's 400. Re-measure both from the committed C0a blob; a
    disagreement is a finding.

Done when — run every gate and record its REAL exit code and output:
 G1  Before C0a and again before C5: `.agent/STOP` is ABSENT,
     `git rev-parse --abbrev-ref HEAD` prints
     `feature/f009-single-write-channel`, and `git status --porcelain` prints 0
     lines after each of C0a, C0b, C1, C2, C3 and C4. Report the round base SHA
     you read at step 0.
 G2  TRANSPORT: `.agent/authored/f009-r22.md` at C0a and `.agent/last_block.md`
     at C0b are byte-equal to each other and to the block you received; report
     sha256, bytes and lines for both. C0b is written FROM the committed C0a
     blob, never from the scratch copy again.
 G3  SLICES: extract every slice from the COMMITTED C0a blob by its `<<<SLICE `
     and `<<<END ` marker lines with a script and apply them programmatically.
     Report each slice's sha256, bytes and lines plus the aggregate count your
     script printed. State no slice count you did not count. Re-measure
     constraint 7's two numbers from that same blob — TOTAL, and PROSE as TOTAL
     minus the summed slice-CONTENT lines — and report both.
 G4  `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R22 — report `cmp` exit and
     both sha256, with a negative control against another file exiting non-zero
     — and `wc -l` against the 50-line cap of AGENTS.md. Line-anchored,
     `^## Goal$` and `^## Next Steps$` each read 1.
 G5  THE TWO APPENDS, each under TWO independent readers, each with a negative
     control on its FIRST appended paragraph (finding R-0631). For C2 over
     `.agent/live_review.md` and for C3 over `.agent/decisions.md`, each based
     on that file's round-base blob: (a) the base blob is a byte-exact PREFIX
     and the remainder equals a newline plus the slice — report its sha256,
     bytes and lines; (b) N is counted BY YOUR SCRIPT and the last N blank-line
     units equal the slice's N paragraphs IN ORDER. Then, for EACH append, flip
     one printable byte in the FIRST appended paragraph, at equal length, and
     report that BOTH readers REJECT the flip while both ACCEPT the true file.
     Report before/after bytes and lines for both files.
 G6  Line-anchored at line START over `.agent/live_review.md` at the round base
     and at C2 (finding R-0630): a leading `- R-` id with every captured id
     DISTINCT at each; a leading `Done: R-` id; a leading `Landed: `; a leading
     `Gate: R` key over that many DISTINCT keys; the `Gate: R22` key; and a
     leading `- R-0641` entry, which must read 0 at BOTH because this round
     mints no id at all. Report each pair of readings, the max id, and the open
     count by DECISION F009 D10's rule at C2. Report what you measure, not what
     this sentence expects.
 G7  Line-anchored over `.agent/decisions.md` at the round base and at C3: the
     `## DECISION ` total; leading `## DECISION F009 D` numbers with every
     captured number DISTINCT at each and the max reported; and the
     `## DECISION F009 D21 ` key, which reads 0 at the base and 1 at C3. Report
     both readings of each.
 G8  THE FOUR PAIRS, proved as pairs. For each of AUDITDOC, AUDITSET, PINDOC and
     PINSET, count its FROM block and its TO block in the file it targets, BOTH
     whole-line and indent-agnostic, and require the two readings to AGREE at
     every count. Before C4 every FROM reads 1 and every TO reads 0; after C4
     every FROM reads 0 and every TO reads 1 — constraint 3 classified all four
     as NOT append-shaped, so also report, for each pair, whether the TO
     contains the FROM as a contiguous line block, a value your SCRIPT prints
     and which must be FALSE four times. Report the counts, not the conclusion.
 G9  RUFF AND SUITES, run SERIALLY in the PRIMARY checkout, never two pytest
     processes at once and never in a worktree. Report each command's REAL exit
     code and the count IT printed — predict no number:
       `python3 -m ruff check packages/orchestration/command_audit.py
        tests/orchestration/test_command_audit.py`
       `python3 -m pytest tests/orchestration/test_command_audit.py -q -rf`
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
        tests/regression/test_resource_safety.py
        tests/orchestration/test_integrity_gate.py -q -rf`
     The audit suite is owed because C4 edits it and the module it covers; the
     canary is unconditional; the four-path group is owed because this round's
     change set holds `.agent/` state files (finding R-0607). The reviewer ran
     all four at the round base before ordering them: each exits 0, so each can
     fail honestly (R-0364). Ruff over these two paths is exit 0 at base, so
     exit 0 is orderable rather than a multiset comparison.
 G10 RANGE: the range from the round base to C4 lists EXACTLY the declared paths
     other than `.agent/handoff.md`, the set difference EMPTY in both
     directions, and 0 paths beginning `apps/` or `docs/` and 0 equal to
     `packages/orchestration/ui_server.py`, which is this round's no-door
     constraint as a measurement. Each commit has ONE parent; `git show
     --numstat` and `git diff --numstat` AGREE on every cell — invoke `git show`
     WITHOUT a `--` before the SHA, which turns it into a pathspec and prints
     nothing; every cell equals the `+/-` column of the handback's `## Commits`
     table (checklist item 28), compared cell by cell. Report each pre-handback
     commit's insertions against the 500 cap of AGENTS.md DECISION F104 D1; the
     handback commit's own numbers belong in the round report (item 14).
     Leading `<<<SLICE ` and `<<<END ` read 0 LINES in every file a slice lands
     in, a set the reviewer counted at five: `.agent/plan.md`,
     `.agent/live_review.md`, `.agent/decisions.md`,
     `packages/orchestration/command_audit.py` and
     `tests/orchestration/test_command_audit.py`. `git ls-files .remedy-wt`
     reads 0. Classify THIS ROUND's reflog rows by the operation before the
     first `:` and report `amend`, `rebase` and `cherry` each 0; assert no total
     over the whole reflog (R-0601). Create NO worktree, so `git worktree list`
     prints 1 line throughout.
 G11 The handback carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each of C0a, C0b,
     C1, C2, C3, C4 and C5, the round base SHA, one line per gate with the
     transcripts in the round report and not in the file (R-0582), and this
     block's `Fortschritt:` line VERBATIM across all five of its lines. Report
     its `wc -l` against the 60-line cap, or against 100 with a stated cause.

Handback:    completion report + rewrite `.agent/handoff.md`. Push after C5.
             Create NO pull request: F009 opens one at its own closure.
─────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF009R22
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
R22 rules DECISION F009 D21 — what `decision.resolve`'s effect is and where it
becomes durable, the re-examination of D18's clause three that D18 names as this
round's obligation, and the refusal that did not raise — and lands the audit
token `rejected_state` one round ahead of its writer. It touches NO door.

## Next Steps
1. R23 edits `packages/orchestration/ui_server.py` alone: `decision.resolve`
   dispatches to `answer_task_decision` followed by `save_job` under D21, the
   501 seam and its `not_implemented` writer go, and the two pins that still
   expect 501 migrate — the absent-args test and the exposed-subset loop's
   `else` branch.
2. Then the `command.accepted` SSE event on the F008 stream.
3. Then the queue-only import guard, the per-command side-effect assertions and
   the route-walking 405 test; then the integration gate and closure.

## Risks
- D21 rules `save_job` to be PART of the effect rather than a post-effect write,
  which is the substantive difference from `job.stop`: the answer is durable
  only after it returns. A round that treated it as D18's third write would
  answer 200 for an answer no later reader can find.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
<<<END PLANF009R22

<<<SLICE LEDGER22
Gate: R22 — the R21 entry. R21 PASSED, and it PASSED CLEAN: no finding, no deviation, and every numeral it stated about its own bytes reproduced. Every gate was RE-EXECUTED by the reviewer off disk rather than read back out of the handback. TRANSPORT: `.agent/authored/f009-r21.md` at `bc035156` and `.agent/last_block.md` at `0c7070de` are byte-equal to each other at sha256 29bc2a7f4504c137614a74f55b0de69cc5d43f679210554bd51376987858b0b8 over 18556 bytes and 181 lines, `cmp` exiting 0. THE REVIEWER'S OWN EXTRACTION out of the committed C0a blob prints an aggregate of 2 slices — PLANF009R21 at `fb70be12…` over 2396 bytes and 42 lines, LEDGER21 at `1b674523…` over 7071 bytes and 3 lines — and constraint 6's two numerals re-measure from that same blob as 181 TOTAL and 136 PROSE, TOTAL minus the 45 summed slice-CONTENT lines with marker lines counted as prose, both under DECISION F085 D6's 490 and D5's 400. That is finding R-0640's fix holding in the very round that registered it. `.agent/plan.md` at `5ab95500` is BYTE-EQUAL to PLANF009R21 at both `fb70be12…`, 42 lines against the 50-line cap, `^## Goal$` and `^## Next Steps$` reading 1 each, its negative control against `.agent/context.md` unequal. THE APPEND HOLDS UNDER THE REVIEWER'S OWN TWO READERS: at `fcbb0bb3` the round-base blob is a byte-exact prefix of `.agent/live_review.md`, the remainder is exactly a newline plus LEDGER21 at sha256 `a9aa70b8…` over 7072 bytes and 4 lines, the file going 501154 to 508226 bytes and 1104 to 1108 lines, N counted at 2 BY THE SCRIPT and the last 2 blank-line units equal LEDGER21's 2 paragraphs IN ORDER, the base ending in exactly ONE newline measured on the bytes; flipping the printable byte at the first appended paragraph's start at equal length, `G` to `H`, makes BOTH readers REJECT while both ACCEPT the true file. THE SETS HELD line-anchored at line start, round base and C2: entries 205 and 206 with every id DISTINCT at each, leading `Done:` ids 3 at both, leading `Landed: ` 0 at both, `Gate: R` keys 20 and 21 over that many DISTINCT keys, the `Gate: R21` key 0 and 1, a leading `- R-0640` entry 0 and 1, a leading `- R-0641` entry 0 at both, max id R-0639 and R-0640, and 202 then 203 open by DECISION F009 D10's rule. `.agent/decisions.md` is BYTE-IDENTICAL at the round base and at HEAD at sha256 `518e00e0…` over 461478 bytes, which is that round's rules-nothing constraint as a measurement rather than a claim. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout: the canary EXITS 0 at 42 passed and the four-path state-reader group EXITS 0 at 511 passed, neither predicted by the handback. THE RANGE HELD: five single-parent commits, the range to C2 listing exactly the four declared paths with the set difference EMPTY in both directions and 0 paths beginning `packages/`, `apps/`, `tests/` or `docs/`, which is that round's no-code constraint as a measurement; `git show --numstat` and `git diff --numstat` agree on every cell and every cell equals the `+/-` column of the handback's own tables, at 181/0, 91/239, 13/11 and 4/0; pre-handback insertions 181, 91, 13 and 4, every one under the 500 cap; zero leading `<<<SLICE ` and `<<<END ` LINES in both slice targets; `git ls-files .remedy-wt` 0; this round's five reflog rows all classify as `commit` with `amend`, `rebase` and `cherry` each 0 and no total asserted over the whole reflog; one worktree and a clean tree at the verdict, and `git ls-remote` shows the branch pushed to `09d473d6`, the same SHA the reviewer read. THE HANDBACK'S OWN SELF-NUMERALS WERE MEASURED RATHER THAN READ, which is the second half of R-0640's fix and the reason this entry records no new finding: its declared 82 lines are 82, its "five per-commit changed-files tables (25 lines)" region measures 5 headings and 15 pipe lines over 25 lines, its "six-row item-status table" is a header plus 5 data rows, and its "ten gates" are 10 gate lines. The stated-cause overage at 82 against the 60-line cap is DECISION D15's and is correctly declared: the cause named is mandated content only, no section was dropped and no transcript was inlined. The block's `Fortschritt:` line is present on FOUR physical lines in the block and reproduced VERBATIM across four in the handback, byte for byte by the reviewer's own comparison — constraint 5 of that block, and the other half of R-0640, both holding.
<<<END LEDGER22

<<<SLICE DECISION21
## DECISION F009 D21 — the `decision.resolve` effect, D18 clause three re-examined, and a refusal that did not raise (2026-08-22)

Measured by the reviewer at `09d473d6`, before this round was delegated, by reading `packages/orchestration/escalation.py`, `apps/cli/commands/decision.py` and the door's own seam: `answer_task_decision(job, decision_id, *, answer, source, now)` mutates an in-memory `Job` and returns the updated record or None, and it is `storage.save_job(job)` that persists it — the CLI's own answer path calls exactly that pair in exactly that order. The door already holds a freshly loaded `Job` from `_load_job`, so no second load is needed.

FIRST, THE EFFECT AND WHERE IT BECOMES DURABLE. CHOSEN: both calls ARE the effect and both sit inside the dispatch method that DECISION F009 D18's `try` already wraps. `save_job` is NOT one of D18's two post-effect writes. This is the substantive difference from `job.stop` and the reason D18 refused to let this round inherit its clause three: `safe_points.request_stop` is durable the moment it returns, so an audit line or a publication failing on top of it fails on top of a completed effect, whereas a `decision.resolve` whose `save_job` failed has changed NOTHING on disk. Treating `save_job` as a post-effect soft write would answer 200 for an answer no later reader can find. A raise from EITHER call is D18 clause four's `rejected_effect` and 500, unchanged.

SECOND, D18's CLAUSE THREE, RE-EXAMINED AS D18 REQUIRES RATHER THAN INHERITED. D18 made the soft failure of the nonce publication conditional on every effect in D5's table being idempotent at its own layer, and named this round as the one that must check that against this effect. MEASURED in `escalation.py`: `answer_task_decision` returns None when the decision is absent OR when its status is not OPEN, so an answer is written ONCE and a re-run cannot overwrite the one the run acted on. CHOSEN: clause three STANDS, with its cost restated for this command rather than assumed from the other. A lost publication cannot produce a SECOND answer — the dangerous reading of non-idempotency does not arise here — it can only make a client's retry of that same nonce miss the replay lookup, re-run the effect, be refused by the paragraph below, and receive a refusal for a command that in fact SUCCEEDED. A misleading refusal is strictly safer than a duplicate write.

ALTERNATIVE to that clause: fail the request when the publication fails. Rejected — it would report an answer that IS durable as one that is not, which is the same falsehood D18 rejected for `job.stop`, merely in the opposite direction.

THIRD, A REFUSAL THAT DID NOT RAISE, which no existing token covers. `answer_task_decision` returning None is not an exception, so `rejected_effect` — D18 clause four's token, defined as a dispatch that RAISED — does not describe it, and `accepted` would be false. CHOSEN: a new closed-set token `rejected_state`, audited with `create=True`, answered 409. The name states the CHECK that refused, as D14 requires of every token in the set: the decision is not in a state that can be answered. T5_F035 and T9_F167 read `commands_audit.jsonl` to count what the door DID, and an effect that ran and declined has to be distinguishable from one that broke.

FOURTH, WHERE THE TOKEN LANDS, AND WHY THIS ROUND EXISTS AT ALL. CHOSEN: `rejected_state` lands in `packages/orchestration/command_audit.py` in THIS round, one round ahead of the door that writes it — the convention D17 set for `accepted` and `replayed` and D18 followed for `rejected_effect` — so that the round retiring the 501 seam changes the door alone and the exact-tuple pin in `tests/orchestration/test_command_audit.py` moves in its own commit rather than in the commit that rewrites the door's control flow. THE BLOCK CAP IS NOT THE REASON THIS TIME AND IS NOT CLAIMED AS ONE: the reviewer estimated the combined round and it fits under DECISION F085 D6's 490, so unlike D18 and D19 this split is a convention rather than a measurement, and it is recorded as such. The wire constant for the 409 body lands WITH the door, as D20's two constants did, because it lives in the door's module and no other module reads it.

FIFTH, `not_implemented` SURVIVES ITS WRITER. When R23 removes the seam, the token STAYS in `OUTCOMES`. Audit files already on disk carry lines whose `outcome` is `not_implemented`, and the vocabulary is what a later reader validates a line against; removing it would make a record this door really wrote fail validation under a version of the code that came after it. The tuple is append-only for that reason, which is also why its order is pinned rather than sorted.

ALTERNATIVES for the third clause: (a) reuse `rejected_shape` for the None return — rejected, D14 binds that token to the REQUEST's shape and this door deliberately does not know any command's argument schema (D20), so it cannot tell a malformed `decision_id` from a well-formed one naming an absent decision. (b) answer 404 — rejected, the door already answers 404 for a missing JOB, and one status for two referents makes them indistinguishable to a client that must decide whether to retry. (c) split None into two tokens, absent and already-answered — rejected, `answer_task_decision` collapses both into one return value and the door would have to call `find_task_decision` first, a second read for a distinction no reading feature has asked for.

REVERSE the first clause by moving `save_job` out of the effect, which requires re-reading D18 clause three first; the third by retiring `rejected_state`, which T5_F035 and T9_F167 would then have to be told about; the fifth by removing `not_implemented` once no audit file predating R23 can still be read.
<<<END DECISION21

<<<SLICE AUDITDOC_FROM
#: and the two reading features cannot tell those apart from the outside.
OUTCOMES = (
<<<END AUDITDOC_FROM

<<<SLICE AUDITDOC_TO
#: and the two reading features cannot tell those apart from the outside.
#: `rejected_state` is DECISION F009 D21's token and the fourth landed with no writer,
#: one round ahead of the door for the reason D17 and D18 both gave. It names an effect
#: that RAN and REFUSED — `answer_task_decision` returning None because the decision is
#: absent or is no longer open — which is neither `rejected_effect`, reserved for a
#: dispatch that RAISED, nor `accepted`, which would be false. The two reading features
#: count what the door DID, and an effect that declined is not one that broke.
OUTCOMES = (
<<<END AUDITDOC_TO

<<<SLICE AUDITSET_FROM
    "rejected_effect",
)
<<<END AUDITSET_FROM

<<<SLICE AUDITSET_TO
    "rejected_effect",
    "rejected_state",
)
<<<END AUDITSET_TO

<<<SLICE PINDOC_FROM
    """The closed set, in order. The last three are the tokens no caller writes yet."""
<<<END PINDOC_FROM

<<<SLICE PINDOC_TO
    """The closed set, in order. The last four are the tokens no caller writes yet."""
<<<END PINDOC_TO

<<<SLICE PINSET_FROM
        "rejected_effect",
    )
    assert "accepted" in OUTCOMES
    assert "replayed" in OUTCOMES, "a replay is not the acceptance it repeats (R-0636)"
    assert "rejected_effect" in OUTCOMES, "an effect that raised is not the acceptance it failed to be"
<<<END PINSET_FROM

<<<SLICE PINSET_TO
        "rejected_effect",
        "rejected_state",
    )
    assert "accepted" in OUTCOMES
    assert "replayed" in OUTCOMES, "a replay is not the acceptance it repeats (R-0636)"
    assert "rejected_effect" in OUTCOMES, "an effect that raised is not the acceptance it failed to be"
    assert "rejected_state" in OUTCOMES, "an effect that refused is not the one that raised"
<<<END PINSET_TO
