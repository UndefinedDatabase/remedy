── STEP CODE ROUND / F031 — ROUND R51 ─────────────────────────────────
Goal:        Land the SERVER half of the clarification FORM. The write door's
             `fp:` branch stops hard-coding `answers={}`: it accepts an OPTIONAL
             `args.answers`, validates it against the plan's own open questions,
             and passes it to `resolve_flight_plan_approval`, so an operator
             approving from the inbox can choose something other than every
             default. Also record R50's PASS and rule DECISION F031 D26.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the R50 gate entry · C3 DECISION F031 D26 · C4 the door · C5
             the effect test · C6 handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r51.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/decisions.md`, `packages/orchestration/ui_server.py`,
             `packages/orchestration/decision_inbox.py`,
             `tests/ui_server/test_command_dispatch.py`, `.agent/handoff.md`.
             NOTHING UNDER `apps/` OR `docs/`, and nothing under `packages/` or
             `tests/` other than the three files named above. In particular
             `tests/ui_server/test_command_channel.py` IS NOT IN THIS CHANGE
             SET: the tests pinning the two refusals D26 rules land at R52 with
             the browser form, and D26 itself records why.

Constraints:
 1. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. A slice's text is its content lines joined with a newline
    plus ONE trailing newline; a slice that ends in blank content lines carries
    those blank lines on purpose and they are part of it. If a slice looks
    wrong, say so in the handback and finish the round anyway — a corrected
    slice destroys the transport proof.
 2. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5, C6. No pair may be
    reordered and none may be merged.
 3. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R50. That is
    ordered: the plan becomes current at C1.
 4. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Done:` paragraph,
    never mint a finding id, and never edit a decision's wording. NO FINDING IS
    REGISTERED OR RESOLVED THIS ROUND.
 5. C4 IS ONE LOGICAL STEP ACROSS TWO FILES and carries S1, S2 and S3 in
    `packages/orchestration/ui_server.py` and S4 in
    `packages/orchestration/decision_inbox.py`. S4 is not a drive-by: the
    sentence it replaces says the door "refuses on exactly two conditions", and
    C4 gives the door a third, so leaving it would land a false sentence in
    shipped code. C5 carries S5 and S6 and touches no other file.
 6. THE LEDGER AND DECISION SETS MOVE ONCE EACH. Across C2 the gate-key pattern
    `^Gate: F\d+ R\d+ — ` moves 31 to 32 with the ADDED key exactly `F031 R50`.
    Across C3 `^## DECISION F031 D\d+ ` in `.agent/decisions.md` moves 25 to 26
    with the ADDED id exactly `D26`. Across the whole round `^- R-\d+ — ` stays
    263, `^Done: R-\d+ — ` stays 8, `^Landed: R-` stays 0 and `^Gate: R\d+ — `
    stays 19. The open set is 255 before C2 and 255 after C5.
 7. RE-READ `.agent/STOP` FROM DISK before C0a and again before C6. If it exists
    at either reading, finish the commit in hand, write the handback and STOP.
    Never create it, never delete it.
 8. DESTRUCTIVE VERIFICATION IS ISOLATED. G6's probe runs ONLY inside a
    disposable `git worktree` you create under `.remedy-wt/` and remove again BY
    ITS EXACT PATH before C6 — never by glob, and never in the primary checkout,
    which reads `git status --porcelain` 0 lines at every commit. Earlier
    rounds' scratch under `.remedy-wt/` is left alone. Nothing under
    `.remedy-wt/` is ever committed.
 9. YOUR HANDBACK'S CAP. AGENTS.md gives 60 lines at most, or 100 at most when
    per-commit tables of more than five commits require it. THERE IS NO TIER
    ABOVE 100. Derive your cap from the commits the Bundle above orders and stay
    inside it; if the MANDATED content genuinely does not fit, write the
    DECISION D15 "Deviations, declared" line naming your actual line count and
    the specific mandated content that caused the overage. Do not invent a tier.
10. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `cp`, brace literals containing a quote character, and every form
    of environment assignment. Route anything that counts, hashes or compares
    through a quoted python heredoc, read real exit codes from
    `subprocess.run(...).returncode`, and copy with `shutil.copyfile`. Run
    pytest SERIALLY — never two pytest processes alive at once. `--timeout` IS
    NOT AVAILABLE to pytest in this repository: passing it exits 4 and reports
    no failure at all, so never add it to any run this block orders.

Spec — apply in this order, each item byte for byte from its slice:
 S1. `packages/orchestration/ui_server.py`: INSERT S1HELPER immediately BEFORE
     the line `class _RemedyHandler(BaseHTTPRequestHandler):`, which occurs
     exactly 1x in that file at `242144ff`. S1HELPER's own trailing blank lines
     are what separate it from that class line; add nothing of your own.
 S2. Same file, inside `_dispatch_decision_resolve`: replace S2FROM with S2TO.
     The containment test was run at emission and its output is
     `TO contains FROM: false`, so this pair is a REWRITE and its obligation is
     S2FROM 0x and S2TO 1x after C4. S2FROM occurs exactly 1x at `242144ff`.
 S3. Same file, in that method's DOCSTRING: replace S3FROM with S3TO. The
     containment test output is `TO contains FROM: false`, so this pair is a
     REWRITE. S3FROM occurs exactly 1x at `242144ff`, and it is the paragraph
     C4 would otherwise leave asserting that no answers can be passed here.
 S4. `packages/orchestration/decision_inbox.py`, in
     `_answerable_by_decision_resolve`'s docstring: replace S4FROM with S4TO.
     The containment test output is `TO contains FROM: false`, so this pair is
     a REWRITE. S4FROM occurs exactly 1x at `242144ff`.
 S5. `tests/ui_server/test_command_dispatch.py`: replace S5FROM with S5TO,
     giving `_approve` an OPTIONAL `answers`. The containment test output is
     `TO contains FROM: false`, so this pair is a REWRITE. S5FROM occurs exactly
     1x at `242144ff`, and every existing caller passes no `answers` and is
     therefore unchanged.
 S6. Same file: INSERT S6NEW immediately BEFORE the line
     `    def test_the_accepted_fp_approval_saves_the_job_exactly_once(self, monkeypatch):`,
     which occurs exactly 1x in that file at `242144ff`. S6NEW's own trailing
     blank line is what separates it from that line; add nothing of your own.

Done when — run every gate yourself and record its REAL exit code. G1 through G8
run at commits STRICTLY EARLIER than C6, so the handback can quote them; the
push is ordered after C6 and its reading is NOT written into the handback.
 G1. BRANCH, CLEANLINESS, TRANSPORT. Branch is `feature/f031-decision-inbox`.
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2, C3,
     C4 and C5. `.agent/STOP` read from disk before C0a and before C6, both
     ABSENT. Report the sha256, byte count and line count of this block as saved
     at C0a, as mirrored at C0b, and as read off disk at C5 — all three must be
     EQUAL — and say whether C0a and C0b are the same git blob.
 G2. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES, never from the prompt. Report how many slices your
     extractor printed, the CONTENT line total, the TOTAL line count, and PROSE
     as TOTAL minus CONTENT. MARKERS ARE PROSE. PROSE must be at most 400 and
     TOTAL at most 490.
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R51 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G4. THE TWO APPENDS, EACH PROVED TWICE, THE SECOND READER COVERING THE WHOLE
     APPENDED REGION. Read every non-current revision with
     `git show <rev>:<path>` into memory; never write a past blob over a tracked
     file to read it. `.agent/live_review.md` at C2 equals its pre-commit blob
     plus ONE newline plus LEDGER51. `.agent/decisions.md` at C3 equals ITS OWN
     pre-commit blob — which you READ rather than take from this block — plus
     ONE newline plus DECISION26. The reviewer measured both BASE blobs at
     `242144ff` itself: `.agent/live_review.md` is 893819 bytes and
     `.agent/decisions.md` is 613277 bytes. If either reads differently before
     its append, something moved that this round did not order — stop and hand
     back. For EACH append report both byte counts and the sum. Then confirm
     EACH with a SECOND, independent reader: split the whole file on blank
     lines, let N be the number of paragraphs YOUR SCRIPT COUNTS in that slice —
     never a number this block asserts — and compare the LAST N units of the
     file against the slice's N paragraphs IN ORDER. Report N and the unit count
     before and after for each. THE NEGATIVE CONTROL GOES ON THE FIRST APPENDED
     PARAGRAPH, which is the position a tail-only reading cannot see: flip ONE
     byte IN MEMORY inside paragraph 1 of each slice and report that BOTH
     readers REJECT it. For any slice whose N is 1, say so and note that
     paragraph 1 is also the last. Never mutate a tracked file.
 G5. THE LEDGER AND DECISION SETS. Report at three points — before C2, after C2,
     after C5 — the line-anchored counts over `.agent/live_review.md` of
     `^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-`, `^Gate: R\d+ — ` and
     `^Gate: F\d+ R\d+ — `, plus the ids and gate keys ADDED and REMOVED as SETS
     at each step, whether all ids are DISTINCT, and the maximum id. Report the
     open set as `^- R-\d+ — ` minus `^Done: R-\d+ — ` before C2 and after C5.
     Separately report `^## DECISION F031 D\d+ ` over `.agent/decisions.md`
     before C3 and after C3 with the ADDED and REMOVED ids as SETS. Every
     movement constraint 6 names is checked here, INCLUDING the ones that must
     NOT move.
 G6. THE CODE, AND THE FORM PROVED TO REACH THE RECORD.
     (a) At C4, in `packages/orchestration/ui_server.py`: S1HELPER 1x, S2FROM
         0x, S2TO 1x, S3FROM 0x, S3TO 1x, and over that WHOLE file the substring
         `answers={}` 0x. In `packages/orchestration/decision_inbox.py`: S4FROM
         0x, S4TO 1x, and the substring `exactly two conditions` 0x.
         `git diff --name-only C3..C4` is exactly those two paths.
     (b) At C5, in `tests/ui_server/test_command_dispatch.py`: S5FROM 0x, S5TO
         1x, S6NEW 1x. `git diff --name-only C4..C5` is that one path only.
     (c) `python3 -m ruff check packages/orchestration/ui_server.py
         packages/orchestration/decision_inbox.py
         tests/ui_server/test_command_dispatch.py` at C5, REAL exit 0. The
         reviewer ran that exact command line over these files at `242144ff`
         and it exits 0 there, so a red here is this round's own doing.
     (d) THE PROBE, in a disposable worktree at C5 under `.remedy-wt/`, never in
         the primary checkout. In THAT WORKTREE's copy of
         `packages/orchestration/ui_server.py`, first COUNT the three-line
         sequence that reads, in order,
         `            answers = _validated_clarification_answers(args, questions)`
         then `            if answers is None:` then `                return None`
         and report the count, which must be 1; then replace those three lines
         with the single line `            answers = {}` and run
         `python3 -m pytest tests/ui_server/test_command_dispatch.py -q` in that
         worktree. REPORT THE REAL EXIT CODE, WHICH MUST BE NON-ZERO. Report no
         failure count and name no test. Then remove that worktree by its exact
         path and report `git worktree list` back to 1 line. This probe is what
         separates a door that CARRIES the operator's answers from one that
         merely accepts the field and drops it: reverting the whole feature must
         turn the effect test red, because a 200 alone proves nothing.
 G7. NOTHING ELSE MOVED, MARKERS, PATHS, COMMITS. Compare the path set of
     `git diff --name-only 242144ff..C5` BOTH WAYS against this round's expected
     set — the Change line's list MINUS `.agent/handoff.md`, excluded because
     the handback is written at C6, outside a range ending at C5 — and report
     both residues EMPTY. Report `git diff --stat 242144ff..C5` restricted to
     `apps/` and to `docs/` and confirm each is EMPTY. Line-anchored
     `^<<<SLICE ` and `^<<<END ` are 0 and 0 in `.agent/plan.md` at C1,
     `.agent/live_review.md` at C2, `.agent/decisions.md` at C3,
     `packages/orchestration/ui_server.py` at C4 and
     `tests/ui_server/test_command_dispatch.py` at C5, against a CONTROL count
     over the C0a blob, which is not 0. Report each commit's insertions from
     `git diff --numstat` for C0a through C5, confirm each is single-parent and
     under 500. Report `git ls-files .remedy-wt` as 0 and `git worktree list` as
     1 line at C5. Report the reflog FOR THIS ROUND'S OWN COMMITS ONLY: every
     operation prefix must read `commit`, and among those entries `amend`,
     `rebase` and `cherry` must be 0 each. Do not count those words over the
     whole reflog, which holds this repository's entire history and is not what
     this gate asks.
 G8. THE CANARY, THE STATE READERS, AND THE SUITES THIS ROUND CAN MOVE. In the
     PRIMARY checkout at C5, run SERIALLY — never two pytest processes alive at
     once — reporting each REAL exit code and count:
     `python3 -m pytest tests/cli/test_golden_path.py -q` (the canary),
     `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py`,
     `tests/orchestration/test_integrity_gate.py`,
     `tests/orchestration/test_decision_inbox.py`,
     `tests/cli/test_plan_approval.py` and `tests/cli/test_decision_answers.py`.
     At `242144ff` the reviewer measured the first five itself at 42, 486, 52,
     21 and 16 and the last three at 35, 27 and 29, every one at exit 0. DO NOT
     PREDICT the new `tests/ui_server/` count: report what you measure, and say
     how it compares with 486, noting that this round adds exactly one test
     under that path and changes no other test there. The last three are ordered
     BECAUSE they must NOT move: `tests/cli/test_plan_approval.py` and
     `tests/cli/test_decision_answers.py` are the CLI's own approval and
     `--answer` suites, and they are what proves this round changed no CLI
     semantics while touching the function the CLI shares with the door.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C6: feature and round, branch, the per-commit changed-files table
             with the `+/-` column taken from `git diff --numstat` ITSELF and
             agreeing cell for cell with G7's readings, the item-status table
             covering C0a, C0b, C1, C2, C3, C4, C5, C6 and the push, ONE LINE
             PER GATE for G1 through G8 with its real exit code, the
             open-findings count, and the next expected action. SAY PLAINLY
             WHETHER THE BRANCH TIP IS GREEN, WHAT G6's PROBE RETURNED, AND
             WHETHER THE THREE MUST-NOT-MOVE SUITES MOVED. THE NEXT ACTION
             SECTION NAMES, IN THIS ORDER: re-read `.agent/STOP` from disk
             first, then the Open PR Gate, then review this round's handback,
             then R52. Obey constraint 9's cap. Then push with
             `git push origin feature/f031-decision-inbox`.
──────────────────────────────────────────────────────────────────────

<<<SLICE PLANF031R51
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D26.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R51 lands the SERVER half of the clarification FORM. `_dispatch_decision_resolve`
stops hard-coding `answers={}`: it takes an OPTIONAL `args.answers`, validates it
against the plan's own open questions, and passes it through, so an operator
approving from the inbox can choose something other than every default. The
round also records R50's PASS and rules DECISION F031 D26.

## Next Steps
1. R52: the BROWSER half — the pending card renders a field per open
   clarification and posts them — together with the tests pinning the two
   refusals DECISION F031 D26 rules, which R51 ships documented but unguarded.
2. A reviewer-file round landing the §3 checklist item R-0694 through R-0699
   share: a block reads the TARGET before ordering anything against it — every
   guard whose ruled set the change widens, every constant a test compares
   against, and every fixture whose state decides an outcome.
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- THE TWO REFUSALS D26 RULES SHIP UNGUARDED FOR ONE ROUND. The 490-line block
  cap forced the split; R52's first commit is their test, and until it lands the
  door's own docstring is the only record of the contract.
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  R-0693 measures the gap; the rest are outside F031's scope, and the inbox
  tells the truth about every one of them rather than offering a refused button.
- SIX ROUNDS RAISED A REVIEWER-SPEC DEFECT WITH ONE ROOT CAUSE — a block
  ordering something against a file it had not read. Step 2 above is the fix
  and it is the highest-value work left in this feature.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 255 at `242144ff`
  and this round leaves it at 255.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R51

<<<SLICE LEDGER51
Gate: F031 R50 — the F031 R50 entry. R50 PASSED ON EVERY GATE ITS BLOCK ORDERED, G1 THROUGH G8, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced cell for cell. THE STRONGEST CHECK THE REVIEWER RAN IS NOT ONE THE BLOCK ORDERED: it applied the block's own SPEC to the base blobs independently, in memory, and the two landed files are BYTE-IDENTICAL to that simulation — `packages/orchestration/ui_server.py` at `ed4e1b2a` and `tests/ui_server/test_command_dispatch.py` at `c94c3ecb` — so the worker applied exactly what was specified and nothing else. TRANSPORT HELD: the C0a blob, the C0b blob and the reading taken at C5 are byte-identical at sha256 `18709505…5fd11e24` over 25929 bytes and 346 lines, with C0a and C0b resolving to the SAME git blob `5fbb344f`, and the slices extracted from that blob match the BASE files exactly — S1FROM 1x, S2DEL 2x and S4FROM 6x at `cd676e4c` — which is what proves the block reached the worker unmangled. THE EXTRACTION printed 9 slices, CONTENT 113 and TOTAL 346, so PROSE was 233 against 400 and TOTAL 346 against 490. THE PLAN at `a6db8474` is byte-equal to PLANF031R50 with the minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` 47. THE TWO APPENDS ARE EXACT: 888399 + 1 + 3486 = 891886 and 891886 + 1 + 1932 = 893819, with the pre-C2 blob equal to the base the block named; N counted by the reviewer's own script at 1 and 2; units 363 to 364 and 364 to 366; and the byte flip placed on the FIRST appended paragraph REJECTED by BOTH readers on both. THE SETS MOVED ONLY WHERE CONSTRAINT 7 ALLOWED: `^Gate: F\d+ R\d+ — ` 30 to 31 with the ADDED key exactly `F031 R49`; `^Done: R-\d+ — ` 6 to 8 with the ADDED ids exactly `R-0701` and `R-0702`; `^- R-\d+ — ` 263 throughout with no id minted; `^Landed: R-` 0 and `^Gate: R\d+ — ` 19 throughout; all ids DISTINCT with the maximum `R-0702`; open set 257 to 255. THE TWO CODE COMMITS WERE READ LINE BY LINE AND EACH IS FAITHFUL TO ITS SPEC: `ed4e1b2a` replaces one docstring sentence so the paragraph names DECISION F031 D24 instead of a round number, leaving `R48` and `Round R` at 0 over the whole file; and `c94c3ecb` deletes the byte-identical `_start_server` from BOTH classes, inserts one module-level `_start_ui_server_for_job` above the first of them, and rewrites all six call sites, with `def _start_server` 0x and the helper defined 1x. THE PROBE DISCRIMINATES AND THE REVIEWER RE-RAN IT ITSELF in its own disposable worktree rather than accepting the report: with the helper's single return line replaced by a dead port the file goes RED at a REAL exit code of 1 and the output names BOTH `TestJobStopDispatchEffects` and `TestFlightPlanApprovalDispatchEffects`, so the one surviving copy is the live path for each class rather than merely present; the worktree was removed and `git worktree list` returned to 1 line. RUFF over both edited files is REAL exit 0 at the tip and was also 0 at `cd676e4c`, so the gate was not vacuous. THE SUITES THE REVIEWER RE-RAN SERIALLY IN THE PRIMARY CHECKOUT at `242144ff`, every one at a REAL exit 0: canary 42, `tests/ui_server/` 486, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21 and `tests/orchestration/test_integrity_gate.py` 16. THE MARKER SWEEP reads 0 and 0 in all four targets against a CONTROL of 9 and 9 over the C0a blob; both path residues are EMPTY over six paths; the insertions are 346, 280, 14, 2, 4, 37 and 4, each commit single-parent and far under 500; `git ls-files .remedy-wt` is 0 lines and `git worktree list` is 1 line; and the reflog entries for this round's own commits all read prefix `commit`, with `amend`, `rebase` and `cherry` 0 each among them. THE HANDBACK IS 96 LINES, inside the 100-line band AGENTS.md gives when per-commit tables of more than five commits require it, and its per-commit `+/-` column agrees cell for cell with `git diff --numstat` — the third-writer check finding R-0592 asked for. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing table, no unverified completion claim and no silent scope change, and no erratum of the reviewer's own recurred.
<<<END LEDGER51

<<<SLICE DECISION26
## DECISION F031 D26 (2026-08-27) — the write door takes the operator's clarification answers, and it refuses a question id it does not know

THE GAP DECISION F031 D24 LEFT ON PURPOSE: that entry ruled that the `fp:`
branch passes `answers={}`, so every open clarification takes its own
`default_answer` and an operator approving from the inbox accepts them all, and
it named a FORM over `payload.clarifications` as where any other choice would
come from. The card has carried those questions all along — the pending arm of
`decision_queue.py` exports `payload["clarifications"]` from
`open_clarification_questions` — so the door was the only half that could not
receive an answer.

CHOSEN, `args.answers` IS OPTIONAL AND VALIDATED. ABSENT, the door behaves
exactly as D24 ruled, so every client written against D24 stays correct and no
existing test moves. PRESENT, it must be a map of OPEN question ids to strings,
and `_validated_clarification_answers` refuses the whole request otherwise, with
the same 409 and `rejected_state` the door's other refusals give. The
alternative — dropping an unknown id and carrying on — is REJECTED because
`apply_clarification_answers` would then write `answered_by="default"` for a
question the operator really answered, and saying who decided is the one job the
assumption log has.

CHOSEN, THE FORM LANDS IN TWO ROUNDS, SERVER THEN BROWSER. R51 is the door plus
the effect test that reads the operator's own words back off disk; R52 is the
browser form together with the tests pinning the two refusals this entry rules.
The split is forced by DECISION F085 D6's 490-line block cap — one block cannot
carry both halves and their slices — and it is recorded here rather than left
implicit because for one round the door refuses on a condition no test guards.
The seam is real rather than convenient: the door is reachable by any client, so
the capability is usable and provable before a component exists.
<<<END DECISION26

<<<SLICE S1HELPER
def _validated_clarification_answers(
    args: dict[str, Any], questions: list[dict[str, str]],
) -> dict[str, str] | None:
    """The `answers` a flight-plan approval may carry, or None to refuse it.

    DECISION F031 D26. ABSENT means "accept every default": that is DECISION
    F031 D24's original contract and the reading of every client written before
    this form existed, so it stays valid and stays the default.

    PRESENT means the operator chose, and it is then validated the way
    `apps/cli/commands/decision.py::parse_answer_options` validates `--answer`,
    because the CLI is the vocabulary this door mirrors: an unknown question id
    is a spec error there rather than a silent default.

    Remedy deliberately does NOT drop an unknown id and carry on, and a reader
    looking for that leniency should stop here: `apply_clarification_answers`
    would then write `answered_by="default"` for a question the operator really
    answered, and an assumption log that misreports who decided is worse than a
    refused request the client can correct.
    """
    raw = args.get("answers")
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        return None
    known = {str(q.get("id", "")) for q in questions}
    out: dict[str, str] = {}
    for qid, value in raw.items():
        if not isinstance(qid, str) or qid not in known:
            return None
        if not isinstance(value, str):
            return None
        out[qid] = value
    return out


<<<END S1HELPER

<<<SLICE S2FROM
            if answer not in ("approve", "reject"):
                return None
            resolve_flight_plan_approval(
                job, reason=answer, answers={},
                questions=open_clarification_questions(
                    fp.get("clarifications_resolved")))
<<<END S2FROM

<<<SLICE S2TO
            if answer not in ("approve", "reject"):
                return None
            questions = open_clarification_questions(
                fp.get("clarifications_resolved"))
            answers = _validated_clarification_answers(args, questions)
            if answers is None:
                return None
            resolve_flight_plan_approval(
                job, reason=answer, answers=answers, questions=questions)
<<<END S2TO

<<<SLICE S3FROM
        returns. `answers={}` is DELIBERATE: through this door every open
        clarification takes its own `default_answer`, so an operator approving
        from the inbox is ACCEPTING THE DEFAULTS. The FORM over
        `payload.clarifications` that DECISION F031 D24 points forward to is
        where any other choice comes from, and there is deliberately no way to
        pass answers here.
<<<END S3FROM

<<<SLICE S3TO
        returns. `args.answers` is DECISION F031 D26's FORM over
        `payload.clarifications`, and it is OPTIONAL. ABSENT, every open
        clarification takes its own `default_answer` and an operator approving
        from the inbox is ACCEPTING THE DEFAULTS, which is DECISION F031 D24's
        contract unchanged. PRESENT, it is validated by
        `_validated_clarification_answers`, and an unknown question id refuses
        the whole request rather than defaulting one answer silently.
<<<END S3TO

<<<SLICE S4FROM
    ``ui_server._dispatch_decision_resolve`` now has TWO branches, and each
    refuses on exactly two conditions, so this predicate mirrors both.
<<<END S4FROM

<<<SLICE S4TO
    ``ui_server._dispatch_decision_resolve`` now has TWO branches, and this
    predicate mirrors every refusal of theirs that is a property of the JOB.
    The door ALSO refuses a malformed ``args.answers`` (DECISION F031 D26), and
    this predicate deliberately does NOT mirror that one: it is a property of
    the REQUEST BODY, invisible to a card, and a card is answerable whenever a
    well-formed request would be accepted.
<<<END S4TO

<<<SLICE S5FROM
    def _approve(self, port, token, nonce):
        payload = {"command": "decision.resolve", "client_nonce": nonce,
                   "args": {"decision_id": "fp:approval", "answer": "approve"}}
<<<END S5FROM

<<<SLICE S5TO
    def _approve(self, port, token, nonce, answers=None):
        args = {"decision_id": "fp:approval", "answer": "approve"}
        if answers is not None:
            args["answers"] = answers
        payload = {"command": "decision.resolve", "client_nonce": nonce,
                   "args": args}
<<<END S5TO

<<<SLICE S6NEW
    def test_a_supplied_clarification_answer_is_recorded_as_human(self):
        """DECISION F031 D26's whole point, read off disk rather than the wire.

        A 200 proves only that the door took the request. What makes the form
        real is that the operator's own words reach the stored record and that
        `answered_by` says `human` — the field the assumption log reports, and
        the one that stays `default` if the door drops the answers it was sent.
        """
        from packages.orchestration.storage import load_job, save_job

        self.job.flight_plan = {"_approval": "pending", "clarifications_resolved": [
            {"id": "q1", "question": "Which store?", "default_answer": "sqlite"}]}
        save_job(self.job)
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._approve(port, token, "nonce-fp-answered",
                                     answers={"q1": "use PostgreSQL"})

        assert status == 200, body
        resolved = load_job(self.job.id).flight_plan["clarifications_resolved"]
        assert resolved[0]["answer"] == "use PostgreSQL", resolved
        assert resolved[0]["answered_by"] == "human", resolved

<<<END S6NEW
