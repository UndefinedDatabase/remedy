── STEP REPAIR ROUND / F031 — ROUND R50 ───────────────────────────────
Goal:        Record R49's PASS, then repair the defects R48 left in code.
             R-0702: the docstring of `_dispatch_decision_resolve` stops naming
             a round number and names the DECISION instead. R-0701: the
             server-start helper that is byte-identical in two classes of
             `tests/ui_server/test_command_dispatch.py` becomes one module-level
             function both call. NEITHER CHANGES BEHAVIOUR, and the branch tip
             must still be green when the round ends.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the R49 gate entry · C3 the docstring repair · C4 the helper
             extraction · C5 the two resolutions · C6 handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r50.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `packages/orchestration/ui_server.py`,
             `tests/ui_server/test_command_dispatch.py`, `.agent/handoff.md`.
             NOTHING UNDER `apps/` OR `docs/`, AND NOTHING UNDER `packages/` OR
             `tests/` OTHER THAN THE FILES NAMED ABOVE. `.agent/decisions.md` IS
             NOT IN THIS CHANGE SET: no decision is ruled this round, the plan's
             renumbering of the clarification FORM to R51 is rewritten state
             rather than a ruling, and the two attributions in
             `.agent/decisions.md` that name R48 are DELIBERATELY LEFT STANDING,
             because a decisions entry is a dated record of what was decided
             THEN while a docstring describes what is true NOW.

Constraints:
 1. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. A slice's text is its content lines joined with a newline
    plus ONE trailing newline; a slice that ends in blank content lines carries
    those blank lines on purpose and they are part of it. If a slice looks
    wrong, say so in the handback and finish the round anyway — a corrected
    slice destroys the transport proof.
 2. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5, C6. No pair may be
    reordered and none may be merged.
 3. THE RESOLUTIONS LAND AFTER THE FIXES AND AFTER THE PROBE THEY DESCRIBE.
    DONE50 states facts about this round's OWN C3 and C4 and about the result of
    the probe G6 orders. Constraint 2's order, plus G6 running before C5, is
    what makes those sentences true on landing; nothing else does.
 4. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R49. That is
    ordered: the plan becomes current at C1.
 5. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Done:` paragraph and
    never edit a finding's or a resolution's wording.
 6. A REFACTOR NEVER SHARES A COMMIT (AGENTS.md). C3 changes only the docstring
    sentence in `packages/orchestration/ui_server.py`; C4 changes only
    `tests/ui_server/test_command_dispatch.py`. Neither touches the other's
    file, and neither carries a `.agent/` path.
 7. THE LEDGER SETS MOVE ONCE EACH. Across C2 the gate-key pattern moves 30 to
    31 with the ADDED key exactly `F031 R49`. Across C5 the resolution pattern
    moves 6 to 8 with the ADDED ids exactly `R-0701` and `R-0702`. Across both,
    the finding pattern stays 263, `^Landed: R-` stays 0 and `^Gate: R\d+ — `
    stays 19. NO NEW FINDING ID IS MINTED THIS ROUND. The open set is 257
    before C2 and 255 after C5.
 8. RE-READ `.agent/STOP` FROM DISK before C0a and again before C6. If it exists
    at either reading, finish the commit in hand, write the handback and STOP.
    Never create it, never delete it.
 9. DESTRUCTIVE VERIFICATION IS ISOLATED. G6's probe runs ONLY inside a
    disposable `git worktree` you create under `.remedy-wt/` and remove again BY
    ITS EXACT PATH before C5 — never by glob, and never in the primary checkout,
    which reads `git status --porcelain` 0 lines at every commit. Earlier
    rounds' scratch under `.remedy-wt/` is left alone. Nothing under
    `.remedy-wt/` is ever committed.
10. YOUR HANDBACK'S CAP. AGENTS.md gives 60 lines at most, or 100 at most when
    per-commit tables of more than five commits require it. THERE IS NO TIER
    ABOVE 100. Derive your cap from the commits the Bundle above orders and stay
    inside it; if the MANDATED content genuinely does not fit, write the
    DECISION D15 "Deviations, declared" line naming your actual line count and
    the specific mandated content that caused the overage. Do not invent a tier.
11. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `cp`, brace literals containing a quote character, and every form
    of environment assignment. Route anything that counts, hashes or compares
    through a quoted python heredoc, read real exit codes from
    `subprocess.run(...).returncode`, and copy with `shutil.copyfile`. Run
    pytest SERIALLY — never two pytest processes alive at once. `--timeout` IS
    NOT AVAILABLE to pytest in this repository: passing it exits 4 and reports
    no failure at all, so never add it to any run this block orders.

Spec — apply in this order, each item byte for byte from its slice:
 S1. `packages/orchestration/ui_server.py`, inside the docstring of
     `_dispatch_decision_resolve`: replace S1FROM with S1TO. The containment
     test was run at emission and its output is `TO contains FROM: false`, so
     this pair is a REWRITE and its obligation is S1FROM 0x and S1TO 1x in that
     file after C3. S1FROM occurs exactly 1x in that file at `cd676e4c`.
 S2. `tests/ui_server/test_command_dispatch.py`: DELETE every occurrence of
     S2DEL. It occurs exactly 2x in that file at `cd676e4c` — once in
     `TestJobStopDispatchEffects` and once in
     `TestFlightPlanApprovalDispatchEffects` — and 0x after C4.
 S3. Same file: INSERT S3HELPER immediately BEFORE the line
     `class TestJobStopDispatchEffects:`, which occurs exactly 1x in that file
     at `cd676e4c`. S3HELPER's own trailing blank lines are what separate it
     from that class line; add nothing of your own.
 S4. Same file, AFTER S2 and S3 have been applied: replace every occurrence of
     S4FROM with S4TO. The containment test was run at emission and its output
     is `TO contains FROM: false`, so this pair is a REWRITE. S4FROM occurs
     exactly 6x in that file at `cd676e4c`.

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
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R50 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G4. THE APPENDS, EACH PROVED TWICE, THE SECOND READER COVERING THE WHOLE
     APPENDED REGION. Read every non-current revision with
     `git show <rev>:<path>` into memory; never write a past blob over a tracked
     file to read it. `.agent/live_review.md` at C2 equals its pre-commit blob
     plus ONE newline plus LEDGER50; at C5 equals ITS OWN pre-commit blob —
     which you READ rather than take from this block — plus ONE newline plus
     DONE50. The reviewer measured the BASE blob at `cd676e4c` itself:
     `.agent/live_review.md` is 888399 bytes. If it reads differently before C2,
     something moved that this round did not order — stop and hand back. For
     EACH append report both byte counts and the sum. Then confirm EACH with a
     SECOND, independent reader: split the whole file on blank lines, let N be
     the number of paragraphs YOUR SCRIPT COUNTS in that slice — never a number
     this block asserts — and compare the LAST N units of the file against the
     slice's N paragraphs IN ORDER. Report N and the unit count before and after
     for each. THE NEGATIVE CONTROL GOES ON THE FIRST APPENDED PARAGRAPH, which
     is the position a tail-only reading cannot see: flip ONE byte IN MEMORY
     inside paragraph 1 of each slice and report that BOTH readers REJECT it.
     For any slice whose N is 1, say so and note that paragraph 1 is also the
     last. Never mutate the tracked file.
 G5. THE LEDGER SETS. Report at three points — before C2, after C2, after C5 —
     the line-anchored counts of `^- R-\d+ — `, `^Done: R-\d+ — `,
     `^Landed: R-`, `^Gate: R\d+ — ` and `^Gate: F\d+ R\d+ — `, plus the ids and
     gate keys ADDED and REMOVED as SETS at each step, whether all ids are
     DISTINCT, and the maximum id. Every movement constraint 7 names is checked
     here, INCLUDING the ones that must NOT move. Report the open set as
     `^- R-\d+ — ` minus `^Done: R-\d+ — ` before C2 and after C5.
 G6. THE CODE, AND THE EXTRACTION PROVED REACHED RATHER THAN MERELY PRESENT.
     (a) At C3, in `packages/orchestration/ui_server.py`: S1FROM 0x, S1TO 1x,
         and over that WHOLE file the substrings `R48` 0x and `Round R` 0x.
         `git diff --name-only C2..C3` is that one path and nothing else.
     (b) At C4, in `tests/ui_server/test_command_dispatch.py`: S2DEL 0x,
         S3HELPER 1x, S4FROM 0x, S4TO 6x, and the substrings `def _start_server`
         0x and `def _start_ui_server_for_job` 1x.
         `git diff --name-only C3..C4` is that one path and nothing else.
     (c) `python3 -m ruff check packages/orchestration/ui_server.py
         tests/ui_server/test_command_dispatch.py` at C4, REAL exit 0. The
         reviewer ran that exact command line at `cd676e4c` and it exits 0
         there, so a red here is this round's own doing.
     (d) THE PROBE, in a disposable worktree at C4 under `.remedy-wt/`, never in
         the primary checkout. In THAT WORKTREE's copy of
         `tests/ui_server/test_command_dispatch.py`, first COUNT the line
         `            return json.loads(Path(info_file).read_text())["port"], token`
         in that file and report the count, which must be 1; then replace it
         with the line `            return 1, token` and run
         `python3 -m pytest tests/ui_server/test_command_dispatch.py -q` in that
         worktree. REPORT THE REAL EXIT CODE, WHICH MUST BE NON-ZERO, and report
         whether the output names BOTH `TestJobStopDispatchEffects` and
         `TestFlightPlanApprovalDispatchEffects`. Report no failure count and
         name no test. Then remove that worktree by its exact path and report
         `git worktree list` back to 1 line. This probe is the only thing that
         separates a helper both classes CALL from one that merely exists: an
         unwired extraction leaves the file green.
 G7. NOTHING ELSE MOVED, MARKERS, PATHS, COMMITS. Compare the path set of
     `git diff --name-only cd676e4c..C5` BOTH WAYS against this round's expected
     set — the Change line's list MINUS `.agent/handoff.md`, excluded because
     the handback is written at C6, outside a range ending at C5 — and report
     both residues EMPTY. Report `git diff --stat cd676e4c..C5` restricted to
     `apps/` and to `docs/` and confirm each is EMPTY. Line-anchored
     `^<<<SLICE ` and `^<<<END ` are 0 and 0 in `.agent/plan.md` at C1,
     `.agent/live_review.md` at C5, `packages/orchestration/ui_server.py` at C3
     and `tests/ui_server/test_command_dispatch.py` at C4, against a CONTROL
     count over the C0a blob, which is not 0. Report each commit's insertions
     from `git diff --numstat` for C0a through C5, confirm each is single-parent
     and under 500. Report `git ls-files .remedy-wt` as 0 and `git worktree
     list` as 1 line at C5. Report the reflog FOR THIS ROUND'S OWN COMMITS ONLY:
     every operation prefix must read `commit`, and among those entries `amend`,
     `rebase` and `cherry` must be 0 each. Do not count those words over the
     whole reflog, which holds this repository's entire history and is not what
     this gate asks.
 G8. THE CANARY AND THE STATE READERS, AND THE TIP STILL GREEN. In the PRIMARY
     checkout at C5, run SERIALLY — never two pytest processes alive at once —
     the canary `python3 -m pytest tests/cli/test_golden_path.py -q` and the
     four state readers `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py` and
     `tests/orchestration/test_integrity_gate.py`, reporting each REAL exit code
     and count. At `cd676e4c` the reviewer measured these itself at 42, 486, 52,
     21 and 16, every one at exit 0. `tests/ui_server/` is ordered because C4
     edits a file inside it; the other four are ordered because this round
     rewrites `.agent/` state and those suites read it.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C6: feature and round, branch, the per-commit changed-files table
             with the `+/-` column taken from `git diff --numstat` ITSELF and
             agreeing cell for cell with G7's readings, the item-status table
             covering C0a, C0b, C1, C2, C3, C4, C5, C6 and the push, ONE LINE
             PER GATE for G1 through G8 with its real exit code, an explicit
             line naming R-0701 and R-0702 as RESOLVED this round, the
             open-findings count, and the next expected action. SAY PLAINLY
             WHETHER THE BRANCH TIP IS GREEN AND WHAT G6's PROBE RETURNED. THE
             NEXT ACTION SECTION NAMES, IN THIS ORDER: re-read `.agent/STOP`
             from disk first, then the Open PR Gate, then review this round's
             handback, then R51. Obey constraint 10's cap. Then push with
             `git push origin feature/f031-decision-inbox`.
──────────────────────────────────────────────────────────────────────

<<<SLICE PLANF031R50
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D25.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R50 is a REPAIR ROUND: it records R49's PASS and then fixes the defects R48
left in code. The docstring of `_dispatch_decision_resolve` stops naming a round
number and names DECISION F031 D24 instead (R-0702), and the server-start helper
that was byte-identical in two classes of
`tests/ui_server/test_command_dispatch.py` becomes one module-level function
both classes call (R-0701). Neither changes behaviour.

## Next Steps
1. R51: the clarification FORM over `payload.clarifications`, so an operator
   answering from the inbox can choose something other than every default.
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
- APPROVING FROM THE INBOX ACCEPTS EVERY CLARIFICATION DEFAULT. DECISION F031
  D24 rules that and R51's FORM is where an operator gains any other choice.
- SIX ROUNDS RAISED A REVIEWER-SPEC DEFECT WITH ONE ROOT CAUSE — a block
  ordering something against a file it had not read. Step 2 above is the fix
  and it is the highest-value work left in this feature.
- A ROUND NUMBER IS THE LEAST STABLE IDENTIFIER THIS PROJECT HAS. Shipped text
  that must point forward names the DECISION or the feature; R-0702 is the
  instance that paid for the rule.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 257 at `cd676e4c`
  and this round takes it to 255.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R50

<<<SLICE LEDGER50
Gate: F031 R49 — the F031 R49 entry. R49 PASSED ON EVERY GATE ITS BLOCK ORDERED, G1 THROUGH G7, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced cell for cell. THE ROUND CHANGED NO EXECUTABLE FILE, and the reviewer proved that rather than accepting it: `git diff --name-only 4f474e19..024e6a95` is four paths, every one beginning `.agent/`, and `git diff --stat` restricted to `apps/`, `packages/`, `tests/` and `docs/` is EMPTY for all four. TRANSPORT HELD IN ITS STRONGEST FORM AVAILABLE TO THIS WORKFLOW AGAIN: the C0a blob, the C0b blob and the reading taken at C3 are byte-identical at sha256 `a5605e52…e438e8a6` over 24239 bytes and 215 lines, with C0a and C0b resolving to the SAME git blob `c794f03e`. THE EXTRACTION printed 3 slices, CONTENT 54 and TOTAL 215, so PROSE was 161 against 400 and TOTAL 215 against 490. THE PLAN at `c9317a82` is byte-equal to PLANF031R49 with the minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` 48. THE TWO APPENDS ARE EXACT: 878135 + 1 + 5151 = 883287 and 883287 + 1 + 5111 = 888399, with the pre-C2 blob equal to the base blob the block named; N counted by the reviewer's own script at 3 and 1; units 359 to 362 and 362 to 363; and the byte flip placed on the FIRST appended paragraph REJECTED by BOTH readers on both. THE SETS MOVED ONLY WHERE CONSTRAINT 5 ALLOWED: `^- R-\d+ — ` 260 to 263 with the ADDED ids exactly `R-0700`, `R-0701` and `R-0702` and none REMOVED; `^Gate: F\d+ R\d+ — ` 29 to 30 with the ADDED key exactly `F031 R48`; `^Done: R-\d+ — ` 6, `^Landed: R-` 0 and `^Gate: R\d+ — ` 19 throughout; all ids DISTINCT with the maximum `R-0702`; open set 254 to 257. THE SUITES THE REVIEWER RE-RAN SERIALLY IN THE PRIMARY CHECKOUT at `cd676e4c`, every one at a REAL exit 0: canary 42, `tests/ui_server/` 486, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21 and `tests/orchestration/test_integrity_gate.py` 16 — the five the R49 block ordered because a round that touches no code can still turn a state reader red. THE MARKER SWEEP reads 0 and 0 in `.agent/plan.md` at C1 and `.agent/live_review.md` at C3 against a CONTROL of 3 and 3 over the C0a blob; both path residues are EMPTY; the insertions are 215, 147, 22, 6, 2 and 42, each commit single-parent and far under 500; `git ls-files .remedy-wt` is 0 lines and `git worktree list` is 1 line; and the reflog entries for this round's OWN commits all read prefix `commit`, with `amend`, `rebase` and `cherry` 0 each among them. THE HANDBACK'S OWN CAP IS THE ONE R-0700 IS ABOUT, AND THIS HANDBACK OBEYED IT: 84 lines inside the 100-line band AGENTS.md gives when per-commit tables of more than five commits require it, with no invented tier and no overage to declare — the round that registered the finding is the round that demonstrates the rule. THE PER-COMMIT TABLE AGREES CELL FOR CELL with `git diff --numstat`, which the reviewer re-derived rather than read back. THE ONE ERRATUM IS THE REVIEWER'S OWN AND COST NOTHING: constraint 8 of the R49 block said the round makes FIVE commits while its own Bundle ordered six, and the worker made the six the Bundle ordered, derived its handback cap from six, and declared the contradiction rather than resolving it silently. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing table, no unverified completion claim and no silent scope change.
<<<END LEDGER50

<<<SLICE DONE50
Done: R-0701 — RESOLVED AT F031 R50 BY THE EXTRACTION COMMIT THIS ROUND'S BLOCK ORDERS, which constraint 2 of that block fixes ahead of this paragraph. `tests/ui_server/test_command_dispatch.py` now defines `_start_ui_server_for_job` once at module level and both `TestJobStopDispatchEffects` and `TestFlightPlanApprovalDispatchEffects` call it, and neither class defines `_start_server` any more. THE WORKER'S REASON FOR DEFERRING IT WAS SOUND AND IS WHY IT LANDS HERE: AGENTS.md forbids mixing a refactor into another commit, so the extraction needed a commit of its own rather than a ride along with the tests that created the duplicate. THE EXTRACTION IS PROVED REACHED RATHER THAN MERELY PRESENT, which is the part a passing suite cannot show: with the single helper's return line broken inside a disposable worktree the file's tests go RED and the output names BOTH classes, so the one surviving copy really is the live path for each — an unwired helper would have left the file green.

Done: R-0702 — RESOLVED AT F031 R50 BY THE DOCSTRING COMMIT THIS ROUND'S BLOCK ORDERS, which constraint 2 of that block likewise fixes ahead of this paragraph. `_dispatch_decision_resolve` in `packages/orchestration/ui_server.py` no longer names a round: the sentence now says that the FORM over `payload.clarifications` which DECISION F031 D24 points forward to is where any other choice comes from, and the substring `R48` occurs nowhere in that file. THE ATTRIBUTIONS IN `.agent/decisions.md` ARE DELIBERATELY LEFT STANDING, because a decisions entry is a dated record of what was decided THEN while a docstring describes what is true NOW. THE GENERAL RULE THIS INSTANCE PAID FOR, and the reason the repair names a DECISION rather than a later round: a round number is the least stable identifier this project has, having been renumbered three times in F031 alone, while a DECISION id and a feature id are stable by construction.
<<<END DONE50

<<<SLICE S1FROM
        from the inbox is ACCEPTING THE DEFAULTS. Round R48's form over
        `payload.clarifications` is where any other choice comes from, and there
        is deliberately no way to pass answers here.
<<<END S1FROM

<<<SLICE S1TO
        from the inbox is ACCEPTING THE DEFAULTS. The FORM over
        `payload.clarifications` that DECISION F031 D24 points forward to is
        where any other choice comes from, and there is deliberately no way to
        pass answers here.
<<<END S1TO

<<<SLICE S2DEL
    def _start_server(self):
        import secrets

        from packages.orchestration.ui_server import start_ui_server

        info_file = str(self.tmp_path / "server_info.json")
        token = secrets.token_urlsafe(16)

        def run():
            try:
                start_ui_server(self.job_id, host="127.0.0.1", port=0, token=token,
                                open_browser=False, info_file=info_file)
            except (SystemExit, KeyboardInterrupt):
                pass

        threading.Thread(target=run, daemon=True).start()
        for _ in range(50):
            if Path(info_file).exists():
                return json.loads(Path(info_file).read_text())["port"], token
            time.sleep(0.1)
        pytest.fail("Server did not start in time")

<<<END S2DEL

<<<SLICE S3HELPER
def _start_ui_server_for_job(job_id: str, tmp_path: Path) -> tuple[int, str]:
    """Start a real UI server for `job_id` in a thread and return `(port, token)`.

    Module-level because both dispatch-effect classes below need it identically
    (finding R-0701). Two copies of a server-start helper drift, and the failure
    mode is quiet: a timeout raised in one copy makes one class flaky on a slow
    runner while its sibling stays green, and the divergence reads as an
    environment problem rather than as a duplicate.
    """
    import secrets

    from packages.orchestration.ui_server import start_ui_server

    info_file = str(tmp_path / "server_info.json")
    token = secrets.token_urlsafe(16)

    def run():
        try:
            start_ui_server(job_id, host="127.0.0.1", port=0, token=token,
                            open_browser=False, info_file=info_file)
        except (SystemExit, KeyboardInterrupt):
            pass

    threading.Thread(target=run, daemon=True).start()
    for _ in range(50):
        if Path(info_file).exists():
            return json.loads(Path(info_file).read_text())["port"], token
        time.sleep(0.1)
    pytest.fail("Server did not start in time")


<<<END S3HELPER

<<<SLICE S4FROM
        port, token = self._start_server()
<<<END S4FROM

<<<SLICE S4TO
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
<<<END S4TO
