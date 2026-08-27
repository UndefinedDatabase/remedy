── STEP GUARD ROUND / F031 — ROUND R52 ────────────────────────────────
Goal:        Close the gap DECISION F031 D26 named when it split the FORM.
             R51 gave the write door a THIRD refusal — a malformed or unknown
             `args.answers` — and shipped it with no test. This round pins both
             halves of that refusal at the door's own answer surface, so the
             contract D26 rules is guarded rather than merely documented. NO
             PRODUCTION FILE CHANGES.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the R51 gate entry · C3 the two guards · C4 handback · then
             push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r52.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `tests/ui_server/test_command_channel.py`, `.agent/handoff.md`.
             NOTHING UNDER `apps/`, `docs/` OR `packages/`, and no file under
             `tests/` other than the one named. In particular
             `packages/orchestration/ui_server.py` IS NOT IN THIS CHANGE SET:
             R51 already landed the behaviour these tests pin, and this round
             adds no production line. `.agent/decisions.md` is not in it either:
             no decision is ruled this round, because D26 already rules the
             contract being guarded.

Constraints:
 1. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. A slice's text is its content lines joined with a newline
    plus ONE trailing newline; a slice that ends in blank content lines carries
    those blank lines on purpose and they are part of it. If a slice looks
    wrong, say so in the handback and finish the round anyway — a corrected
    slice destroys the transport proof.
 2. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4. No pair may be
    reordered and none may be merged.
 3. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R51. That is
    ordered: the plan becomes current at C1.
 4. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Done:` paragraph and
    never mint a finding id. NO FINDING IS REGISTERED OR RESOLVED THIS ROUND.
 5. APPLY THE PAIRS IN THE ORDER THE SPEC GIVES THEM. S1 is a one-line signature
    pair and S2 rewrites the body beneath it together with the helper that
    follows; applying S2 before S1 leaves S1's FROM still matching, and applying
    them out of order is how a two-pair edit lands twice.
 6. THE LEDGER SETS MOVE ONCE. Across C2 the gate-key pattern
    `^Gate: F\d+ R\d+ — ` moves 32 to 33 with the ADDED key exactly `F031 R51`.
    Across the whole round `^- R-\d+ — ` stays 263, `^Done: R-\d+ — ` stays 8,
    `^Landed: R-` stays 0 and `^Gate: R\d+ — ` stays 19. The open set is 255
    before C2 and 255 after C3.
 7. RE-READ `.agent/STOP` FROM DISK before C0a and again before C4. If it exists
    at either reading, finish the commit in hand, write the handback and STOP.
    Never create it, never delete it.
 8. DESTRUCTIVE VERIFICATION IS ISOLATED. G6's probe runs ONLY inside a
    disposable `git worktree` you create under `.remedy-wt/` and remove again BY
    ITS EXACT PATH before C4 — never by glob, and never in the primary checkout,
    which reads `git status --porcelain` 0 lines at every commit. THE PROBE
    MUTATES A FILE THIS ROUND DOES NOT CHANGE, which is deliberate and is only
    safe because it happens in that worktree: the primary checkout's copy of
    `packages/orchestration/ui_server.py` is never written. Earlier rounds'
    scratch under `.remedy-wt/` is left alone; nothing there is ever committed.
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

Spec — apply in this order, each item byte for byte from its slice, all three in
`tests/ui_server/test_command_channel.py`:
 S1. Replace S1FROM with S1TO, giving `_save_flight_plan` an OPTIONAL
     `clarifications`. The containment test was run at emission and its output
     is `TO contains FROM: false`, so this pair is a REWRITE. S1FROM occurs
     exactly 1x in that file at `743a8f7b`.
 S2. Replace S2FROM with S2TO. This spans the tail of `_save_flight_plan`'s body
     AND the whole of `_resolve_flight_plan`, because the latter also gains an
     OPTIONAL `answers`. The containment test output is
     `TO contains FROM: false`, so this pair is a REWRITE. S2FROM occurs exactly
     1x in that file at `743a8f7b`. Every existing caller of both helpers passes
     neither new argument and is therefore unchanged.
 S3. INSERT S3NEW immediately BEFORE the line
     `    def test_an_fp_approval_answered_with_a_next_action_string_is_409(self):`,
     which occurs exactly 1x in that file at `743a8f7b`. S3NEW's own trailing
     blank line is what separates it from that line; add nothing of your own.

Done when — run every gate yourself and record its REAL exit code. G1 through G8
run at commits STRICTLY EARLIER than C4, so the handback can quote them; the
push is ordered after C4 and its reading is NOT written into the handback.
 G1. BRANCH, CLEANLINESS, TRANSPORT. Branch is `feature/f031-decision-inbox`.
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2 and
     C3. `.agent/STOP` read from disk before C0a and before C4, both ABSENT.
     Report the sha256, byte count and line count of this block as saved at C0a,
     as mirrored at C0b, and as read off disk at C3 — all three must be EQUAL —
     and say whether C0a and C0b are the same git blob.
 G2. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES, never from the prompt. Report how many slices your
     extractor printed, the CONTENT line total, the TOTAL line count, and PROSE
     as TOTAL minus CONTENT. MARKERS ARE PROSE. PROSE must be at most 400 and
     TOTAL at most 490.
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R52 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G4. THE APPEND, PROVED TWICE, THE SECOND READER COVERING THE WHOLE APPENDED
     REGION. Read every non-current revision with `git show <rev>:<path>` into
     memory; never write a past blob over a tracked file to read it.
     `.agent/live_review.md` at C2 equals its pre-commit blob plus ONE newline
     plus LEDGER52. The reviewer measured the BASE blob at `743a8f7b` itself:
     `.agent/live_review.md` is 898056 bytes. If it reads differently before C2,
     something moved that this round did not order — stop and hand back. Report
     both byte counts and the sum. Then confirm with a SECOND, independent
     reader: split the whole file on blank lines, let N be the number of
     paragraphs YOUR SCRIPT COUNTS in that slice — never a number this block
     asserts — and compare the LAST N units of the file against the slice's N
     paragraphs IN ORDER. Report N and the unit count before and after. THE
     NEGATIVE CONTROL GOES ON THE FIRST APPENDED PARAGRAPH, which is the
     position a tail-only reading cannot see: flip ONE byte IN MEMORY inside
     paragraph 1 and report that BOTH readers REJECT it. If N is 1, say so and
     note that paragraph 1 is also the last. Never mutate the tracked file.
 G5. THE LEDGER SETS. Report at three points — before C2, after C2, after C3 —
     the line-anchored counts of `^- R-\d+ — `, `^Done: R-\d+ — `,
     `^Landed: R-`, `^Gate: R\d+ — ` and `^Gate: F\d+ R\d+ — `, plus the ids and
     gate keys ADDED and REMOVED as SETS at each step, whether all ids are
     DISTINCT, and the maximum id. Every movement constraint 6 names is checked
     here, INCLUDING the ones that must NOT move. Report the open set as
     `^- R-\d+ — ` minus `^Done: R-\d+ — ` before C2 and after C3.
 G6. THE GUARDS, AND THAT THEY REALLY GUARD.
     (a) At C3, in `tests/ui_server/test_command_channel.py`: S1FROM 0x, S1TO
         1x, S2FROM 0x, S2TO 1x, S3NEW 1x. `git diff --name-only C2..C3` is that
         one path and nothing else.
     (b) `python3 -m ruff check tests/ui_server/test_command_channel.py` at C3,
         REAL exit 0. The reviewer ran that exact command line at `743a8f7b` and
         it exits 0 there, so a red here is this round's own doing.
     (c) THE PROBE, in a disposable worktree at C3 under `.remedy-wt/`, never in
         the primary checkout. In THAT WORKTREE's copy of
         `packages/orchestration/ui_server.py` — a file this round does not
         change, mutated only there — first COUNT the three-line sequence that
         reads, in order,
         `            answers = _validated_clarification_answers(args, questions)`
         then `            if answers is None:` then `                return None`
         and report the count, which must be 1; then replace those three lines
         with the single line `            answers = {}` and run
         `python3 -m pytest tests/ui_server/test_command_channel.py -q` in that
         worktree. REPORT THE REAL EXIT CODE, WHICH MUST BE NON-ZERO. Report no
         failure count and name no test. Then remove that worktree by its exact
         path and report `git worktree list` back to 1 line. Reverting R51's
         validation is the ONLY thing these two tests exist to catch, so a green
         here would mean they guard nothing.
 G7. NOTHING ELSE MOVED, MARKERS, PATHS, COMMITS. Compare the path set of
     `git diff --name-only 743a8f7b..C3` BOTH WAYS against this round's expected
     set — the Change line's list MINUS `.agent/handoff.md`, excluded because
     the handback is written at C4, outside a range ending at C3 — and report
     both residues EMPTY. Report `git diff --stat 743a8f7b..C3` restricted to
     `apps/`, `docs/` and `packages/` and confirm each is EMPTY. Line-anchored
     `^<<<SLICE ` and `^<<<END ` are 0 and 0 in `.agent/plan.md` at C1,
     `.agent/live_review.md` at C2 and `tests/ui_server/test_command_channel.py`
     at C3, against a CONTROL count over the C0a blob, which is not 0. Report
     each commit's insertions from `git diff --numstat` for C0a through C3,
     confirm each is single-parent and under 500. Report `git ls-files
     .remedy-wt` as 0 and `git worktree list` as 1 line at C3. Report the reflog
     FOR THIS ROUND'S OWN COMMITS ONLY: every operation prefix must read
     `commit`, and among those entries `amend`, `rebase` and `cherry` must be 0
     each. Do not count those words over the whole reflog, which holds this
     repository's entire history and is not what this gate asks.
 G8. THE CANARY AND THE STATE READERS. In the PRIMARY checkout at C3, run
     SERIALLY — never two pytest processes alive at once — reporting each REAL
     exit code and count: `python3 -m pytest tests/cli/test_golden_path.py -q`
     (the canary), `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py` and
     `tests/orchestration/test_integrity_gate.py`. At `743a8f7b` the reviewer
     measured these itself at 42, 487, 52, 21 and 16, every one at exit 0. DO
     NOT PREDICT the new `tests/ui_server/` count: report what you measure, and
     say how it compares with 487, noting that this round adds exactly two tests
     under that path and changes no other test there.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C4: feature and round, branch, the per-commit changed-files table
             with the `+/-` column taken from `git diff --numstat` ITSELF and
             agreeing cell for cell with G7's readings, the item-status table
             covering C0a, C0b, C1, C2, C3, C4 and the push, ONE LINE PER GATE
             for G1 through G8 with its real exit code, the open-findings count,
             and the next expected action. SAY PLAINLY WHETHER THE BRANCH TIP IS
             GREEN, WHAT G6's PROBE RETURNED, AND THAT NO PRODUCTION FILE
             CHANGED THIS ROUND. THE NEXT ACTION SECTION NAMES, IN THIS ORDER:
             re-read `.agent/STOP` from disk first, then the Open PR Gate, then
             review this round's handback, then R53. Obey constraint 9's cap.
             Then push with `git push origin feature/f031-decision-inbox`.
──────────────────────────────────────────────────────────────────────

<<<SLICE PLANF031R52
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
R52 closes the gap DECISION F031 D26 named when it split the FORM in two. R51
gave the write door a THIRD refusal — a malformed or unknown `args.answers` —
and shipped it with no test; this round pins both halves of that refusal at the
door's own answer surface. It changes no production file and records R51's PASS.

## Next Steps
1. R53: the BROWSER half of the FORM — the pending card renders a field per open
   clarification and posts them as `args.answers`. `payload.clarifications`
   already reaches the browser, and `decisionAnswers` already derives the two
   words the door takes, so this is a component and a model field rather than a
   new wire format.
2. A reviewer-file round landing the §3 checklist item R-0694 through R-0699
   share: a block reads the TARGET before ordering anything against it — every
   guard whose ruled set the change widens, every constant a test compares
   against, and every fixture whose state decides an outcome.
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  R-0693 measures the gap; the rest are outside F031's scope, and the inbox
  tells the truth about every one of them rather than offering a refused button.
- THE FORM IS REACHABLE ONLY BY A NON-BROWSER CLIENT UNTIL R53. The door takes
  `args.answers` and the card carries the questions, but nothing in the UI yet
  puts the two together, so an operator's only route is still every default.
- SIX ROUNDS RAISED A REVIEWER-SPEC DEFECT WITH ONE ROOT CAUSE — a block
  ordering something against a file it had not read. Step 2 above is the fix
  and it is the highest-value work left in this feature.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 255 at `743a8f7b`
  and this round leaves it at 255.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R52

<<<SLICE LEDGER52
Gate: F031 R51 — the F031 R51 entry. R51 PASSED ON EVERY GATE ITS BLOCK ORDERED, G1 THROUGH G8, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced cell for cell. THE STRONGEST CHECK IS AGAIN ONE THE BLOCK DID NOT ORDER: the reviewer applied the block's own SPEC to the base blobs independently, in memory, and all THREE landed files are BYTE-IDENTICAL to that simulation — `packages/orchestration/ui_server.py` and `packages/orchestration/decision_inbox.py` at `1ff29dda` and `tests/ui_server/test_command_dispatch.py` at `dac7a471` — so the worker applied exactly what was specified and nothing else. TRANSPORT HELD: the C0a blob, the C0b blob and the reading taken at C5 are byte-identical at sha256 `fe15be6b…a92825f0` over 30931 bytes and 441 lines, with C0a and C0b resolving to the SAME git blob `516c218a`, and every base assertion the block made reproduced against the real files — S2FROM, S3FROM, S4FROM and S5FROM each 1x at `242144ff`, both insertion anchors 1x, and `TO contains FROM` FALSE on all four pairs, so every pair really was the REWRITE the spec declared. THE EXTRACTION printed 13 slices, CONTENT 178 and TOTAL 441, so PROSE was 263 against 400 and TOTAL 441 against 490. THE PLAN at `596ff616` is byte-equal to PLANF031R51 with the minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` 45. THE TWO APPENDS ARE EXACT AND THEY LAND IN DIFFERENT FILES: 893819 + 1 + 4236 = 898056 in `.agent/live_review.md` and 613277 + 1 + 1957 = 615235 in `.agent/decisions.md`, both base blobs reading exactly what the block named; N counted by the reviewer's own script at 1 and 4; units 366 to 367 and 1478 to 1482; and the byte flip placed on the FIRST appended paragraph REJECTED by BOTH readers on both. THE SETS MOVED ONLY WHERE CONSTRAINT 6 ALLOWED: `^Gate: F\d+ R\d+ — ` 31 to 32 with the ADDED key exactly `F031 R50`; `^## DECISION F031 D\d+ ` 25 to 26 with `D26` present exactly once after C3; `^- R-\d+ — ` 263, `^Done: R-\d+ — ` 8, `^Landed: R-` 0 and `^Gate: R\d+ — ` 19 all unmoved; all ids DISTINCT with the maximum `R-0702`; open set 255 throughout, no id minted. THE PRODUCTION CHANGE WAS READ LINE BY LINE AND IS FAITHFUL TO ITS SPEC: `1ff29dda` inserts one module-level `_validated_clarification_answers` above `_RemedyHandler`, rewrites the `fp:` branch to derive `questions` once and refuse when the validator returns None, rewrites the docstring paragraph that until then asserted there was deliberately no way to pass answers, and amends `_answerable_by_decision_resolve`'s docstring so it no longer claims the door refuses on exactly two conditions — the two sentences the change would otherwise have left false in shipped code, both caught by reading the targets before ordering anything against them. `answers={}` is 0x over the whole door file and `exactly two conditions` is 0x over the predicate's. THE PROBE DISCRIMINATES AND THE REVIEWER RE-RAN IT ITSELF in its own disposable worktree rather than accepting the report: the three-line validation sequence counts exactly 1, and replacing it with `answers = {}` turns `tests/ui_server/test_command_dispatch.py` RED at a REAL exit code of 1, so the door genuinely CARRIES the operator's answers to `resolve_flight_plan_approval` rather than accepting the field and dropping it; the worktree was removed and `git worktree list` returned to 1 line. RUFF over the three edited files is REAL exit 0 at the tip and was also 0 at `242144ff`, so the gate was not vacuous. THE SUITES THE REVIEWER RE-RAN SERIALLY IN THE PRIMARY CHECKOUT at `743a8f7b`, every one at a REAL exit 0: canary 42, `tests/ui_server/` 487 against 486 at the base — exactly the one test S6 adds — `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16, and the three that had to STAY PUT and did: `tests/orchestration/test_decision_inbox.py` 35, `tests/cli/test_plan_approval.py` 27 and `tests/cli/test_decision_answers.py` 29, which is what proves this round changed no CLI semantics while editing the function the CLI shares with the door. THE MARKER SWEEP reads 0 and 0 in all five targets against a CONTROL of 13 and 13 over the C0a blob; both path residues are EMPTY over eight paths; the insertions are 441, 317, 14, 2, 30, 55 and 27, each commit single-parent and under 500; `git ls-files .remedy-wt` is 0 lines and `git worktree list` is 1 line; and the reflog entries for this round's own commits all read prefix `commit`, with `amend`, `rebase` and `cherry` 0 each among them. THE HANDBACK IS 98 LINES, inside the 100-line band AGENTS.md gives when per-commit tables of more than five commits require it, and its per-commit `+/-` column agrees cell for cell with `git diff --numstat`. THE ONE THING THIS ROUND LEFT OPEN IT DECLARED IN ADVANCE: DECISION F031 D26 rules that the door's new third refusal ships for one round with no test, and names R52 as where those tests land, so the gap is on the record rather than discovered later. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing table, no unverified completion claim and no silent scope change.
<<<END LEDGER52

<<<SLICE S1FROM
    def _save_flight_plan(self, approval: str) -> None:
<<<END S1FROM

<<<SLICE S1TO
    def _save_flight_plan(self, approval: str, clarifications=None) -> None:
<<<END S1TO

<<<SLICE S2FROM
        self.job.flight_plan = {"_approval": approval}
        save_job(self.job)

    def _resolve_flight_plan(self, port, token, nonce, answer):
        return self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(
                command="decision.resolve", client_nonce=nonce,
                args={"decision_id": "fp:approval", "answer": answer}),
            headers=self._auth_headers(token))
<<<END S2FROM

<<<SLICE S2TO
        flight_plan = {"_approval": approval}
        if clarifications is not None:
            flight_plan["clarifications_resolved"] = clarifications
        self.job.flight_plan = flight_plan
        save_job(self.job)

    def _resolve_flight_plan(self, port, token, nonce, answer, answers=None):
        args = {"decision_id": "fp:approval", "answer": answer}
        if answers is not None:
            args["answers"] = answers
        return self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(
                command="decision.resolve", client_nonce=nonce, args=args),
            headers=self._auth_headers(token))
<<<END S2TO

<<<SLICE S3NEW
    def test_an_fp_approval_answering_an_unknown_question_id_is_409(self):
        """DECISION F031 D26's third refusal, and the only one about the BODY.

        The plan is pending and the answer word is one the door takes, so
        neither refusal that predates the form can fire here: a 409 can only
        have come from the answers map itself. Refusing beats defaulting
        silently, because `apply_clarification_answers` would otherwise record
        `answered_by="default"` for a question the operator really did answer.
        """
        self._save_flight_plan("pending", clarifications=[
            {"id": "q1", "question": "Which store?", "default_answer": "sqlite"}])
        port, token = self._start_server()
        status, body = self._resolve_flight_plan(
            port, token, "nonce-fp-unknown-q", "approve", answers={"q9": "x"})

        assert status == 409, body
        assert body["error"] == "decision is not open", body
        assert self._audit_records()[-1]["outcome"] == "rejected_state"

    def test_an_fp_approval_whose_answers_are_not_a_map_is_409(self):
        """The same refusal reached by SHAPE rather than by an unknown id.

        A list is what a client sends when it serialises the form as pairs, so
        this is the plausible malformation rather than an invented one, and the
        door must never iterate it as if it were a map.
        """
        self._save_flight_plan("pending", clarifications=[
            {"id": "q1", "question": "Which store?", "default_answer": "sqlite"}])
        port, token = self._start_server()
        status, body = self._resolve_flight_plan(
            port, token, "nonce-fp-answers-list", "approve", answers=["q1=x"])

        assert status == 409, body
        assert self._audit_records()[-1]["outcome"] == "rejected_state"

<<<END S3NEW
