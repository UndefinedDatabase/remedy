── STEP T003/3 — F009 ────────────────────────────────────────
Goal:        Open T003 with the half DECISION F009 D5 orders to land first and
             ALONE: extract the plan approval into the package function
             `resolve_flight_plan_approval`, with `apps/cli/commands/decision.py`
             as its first caller. Also record the R12 verdict.

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R12 verdict
             · C3 the extraction · C4 handback.

THE ROUND BASE is `9a46a4489d0b067563b2a68f92fe54d193022da4`. Every gate reading
below said to be "at the round base" is measured against that SHA. C4's own SHA
cannot exist inside C4, so C4 is named by role and the round report carries its
value (R-0371).

THIS IS A REFACTOR AND NOTHING ELSE. DECISION F009 D5 rules that the plan-approval
extraction "is ITS OWN COMMIT and lands before any endpoint code calls it". No
endpoint changes this round: the 501 seam stands, no `accepted` outcome is
written, no nonce record is published, and R-0636 and R-0637 stay unpaid — all of
that belongs to the NEXT round, which retires the seam. The proof that the
extraction preserves behaviour is that the CLI remains the only caller and the
approval suites stay green, plus a probe showing those suites actually REACH the
new function.

Change set — these paths and nothing else:
  `.agent/authored/f009-r13.md`
  `.agent/last_block.md`
  `.agent/plan.md`
  `.agent/live_review.md`
  `packages/orchestration/flight_plan.py`
  `apps/cli/commands/decision.py`
  `.agent/handoff.md`

Slice convention: the authored units below are delimited by `<<<SLICE <NAME>` and
`<<<END <NAME>` lines. Extract each from the COMMITTED C0a blob by those marker
lines, with a script, and apply it programmatically. The marker lines themselves
are never written into any target file. A slice's content is every line strictly
between its two markers, newline-terminated.

<<<SLICE PLANF009R13
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
R13 opens T003 with the half DECISION F009 D5 orders to land first and alone: the
plan approval becomes the package function `resolve_flight_plan_approval` and
`apps/cli/commands/decision.py` becomes its first caller. It is a refactor, so it
carries no endpoint change and no new behaviour. The round also records the R12
verdict.

## Next Steps
1. The effect table itself: the three exposed commands dispatch, the 501 seam is
   retired, DECISION F009 D14's reserved `accepted` outcome is written,
   `publish_nonce_result` gains its door call site with R-0637's bound applied at
   publication, R-0636's replay token moves off `not_implemented`, and the
   `command.accepted` SSE event lands with it.
2. Then the queue-only import guard and the per-command side-effect assertions,
   the route-walking 405 test, the client wiring that sends both headers, the
   integration gate, and closure.

## Risks
- R-0636 and R-0637 are owed by the round that retires the 501 seam, which is the
  NEXT round and not this one: both depend on the publish call site it adds.
- A green approval suite proves nothing on its own if it never reaches the new
  function, so the extraction is gated by a probe as well as by a colour.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which is
  R-0622 and routes to a paydown branch.
<<<END PLANF009R13

<<<SLICE LEDGER13
Gate: R13 — the R12 entry. R12 PASSED. Every gate was re-run by the reviewer against the committed blobs and every value reproduced. TRANSPORT AND SLICES HELD — `.agent/authored/f009-r12.md` at `0f198286` and `.agent/last_block.md` at `20a7fc3a` are both sha256 1672d8922c5e11d9cb9079d428fe9b23cb02c12568041447d4b4aa07c9027c7c over 20456 bytes and 182 lines, and the reviewer's own ordered marker extraction gives exactly the four slices PLANF009R12, R0636, R0637 and LEDGER12 at 2221, 2728, 2082 and 4348 bytes, aggregating to 11379 bytes over 41 lines. `.agent/plan.md` at `61c31dde` is BYTE-EQUAL to PLANF009R12 at 38 lines, with `^## Goal$` and `^## Next Steps$` matching one line each and `F009` the first `\bF\d{3}\b` match. THE THREE APPENDS HOLD UNDER BOTH READERS, each from its own base: at `95cf9fe2`, `ff61faa0` and `3cfb44d2` the previous blob is a byte-exact prefix and each remainder is exactly a newline plus its slice, over 2729, 2083 and 4349 bytes, while the file goes 445503 to 448232 to 450315 to 454664 bytes and 1076 to 1078 to 1080 to 1082 lines; under the paragraph reader the last blank-line unit equals the appended slice at each of the three. THE NEGATIVE CONTROLS ARE THE REVIEWER'S OWN, recomputed in memory rather than accepted from the handback: flipping one bit of the byte at offset 445506, 448235 and 450316 — which read `R`, `R` and `G`, the characters the handback named — makes BOTH readers reject the flipped file while both accept the true one, twelve outcomes in all. THE SETS HELD line-anchored at the round base, C2, C3 and C4: `^- R-\d+ — ` 201, 202, 203 and 203 with every id DISTINCT at each, `^- R-0636 — ` 0, 1, 1 and 1, `^- R-0637 — ` 0, 0, 1 and 1, `^Done: R-\d+ — ` 2 throughout, `^Landed: ` 0 throughout, `^> Next free id` 0 throughout, `^Gate: R\d+ — ` 11, 11, 11 and 12 over that many DISTINCT keys, max id R-0637, and item 10's rule giving 201 open at `3cfb44d2`. Of the twelve `Gate: ` lines at C4, eleven match `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one less than the first, and the one non-match reads `Gate: R1 — the F008 R36 entry.`, exactly as the block said it would. THE RANGE HELD: seven single-parent commits, `git show --numstat` and `git diff --numstat` AGREEING on every cell, insertions 182, 110, 12, 2, 2, 2 and 32, all under the 500-insertion cap of AGENTS.md DECISION F104 D1, and every cell for C0a through C4 equal to the `+/-` column of the handback's `## Commits` table, whose C5 row correctly reads `rewrite` rather than a count that commit could not have held (checklist item 14). The path set from the round base to `3cfb44d2` is exactly `.agent/authored/f009-r12.md`, `.agent/last_block.md`, `.agent/plan.md` and `.agent/live_review.md`, the set difference empty in both directions, with no path beginning `packages/`, `apps/`, `tests/` or `docs/` — constraint 3 confirmed as a measurement. `^<<<SLICE ` and `^<<<END ` read 0 lines in both committed state targets and `git ls-files .remedy-wt` reads 0. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout: `python3 -m pytest tests/cli/test_golden_path.py -q -rf` EXITS 0 at 42 passed and the four-path group EXITS 0 at 507 passed, each equal to what the handback reported and neither predicted by it. THE HANDBACK IS WHOLE: 84 lines against the 100 a bundle of more than five commits allows, every mandated section of docs/agents/handback_template.md present, an item-status table with exactly one row for each of C0a through C5, the round base SHA present, and one line per gate with the transcripts left to the round report per R-0582. NO PRODUCTION CODE WAS WRITTEN, which is precisely what the round existed for: two defects of the reviewer's own R11 specification and one verdict now survive the session that found them.
<<<END LEDGER13

<<<SLICE EXTRACT


def resolve_flight_plan_approval(
    job: Any,
    *,
    reason: str,
    answers: dict[str, str],
    questions: list[dict[str, Any]],
) -> Path | None:
    """Approve or reject a job's pending flight plan and persist the outcome.

    Extracted from `apps/cli/commands/decision.py` for DECISION F009 D5, so the UI
    write door can reach the SAME code the CLI has always run instead of growing a
    second copy of the approval sequence beside it — the duplication the P3 contract
    exists to prevent. The CLI stays the first caller and keeps every `print`: this
    function performs the mutation, the save and the assumption log, and hands the
    log path back for the caller to report.

    The caller validates `reason` and the plan's pending state before calling,
    because the CLI and the write door word their refusals differently and neither
    wording belongs in a package. Any `reason` other than `"approve"` rejects, which
    is the branch the extracted code already had.

    Returns the assumption-log path on an approval and None on a rejection.
    """
    from packages.orchestration.storage import save_job

    fp = job.flight_plan
    if reason != "approve":
        fp["_approval"] = "rejected"
        job.flight_plan = fp
        save_job(job)
        return None
    if questions:
        fp["clarifications_resolved"] = apply_clarification_answers(
            fp.get("clarifications_resolved"), answers)
    fp["_approval"] = "approved"
    job.flight_plan = fp
    save_job(job)
    from packages.orchestration.data_paths import job_evidence_export_dir
    return write_assumptions_md(
        fp.get("clarifications_resolved"),
        job_evidence_export_dir(str(job.id)))
<<<END EXTRACT

<<<SLICE CLIFROM_B
    elif decision_id.startswith("fp:"):
        from packages.orchestration.data_paths import resolve_job_id as _rji
        from packages.orchestration.storage import JobNotFoundError, load_job, save_job
<<<END CLIFROM_B

<<<SLICE CLITO_B
    elif decision_id.startswith("fp:"):
        from packages.orchestration.data_paths import resolve_job_id as _rji
        from packages.orchestration.storage import JobNotFoundError, load_job
<<<END CLITO_B

<<<SLICE CLIFROM_A
        from packages.orchestration.flight_plan import (
            apply_clarification_answers,
            clarifications_already_resolved,
            open_clarification_questions,
            write_assumptions_md,
        )
<<<END CLIFROM_A

<<<SLICE CLITO_A
        from packages.orchestration.flight_plan import (
            clarifications_already_resolved,
            open_clarification_questions,
            resolve_flight_plan_approval,
        )
<<<END CLITO_A

<<<SLICE CLIFROM_C
        if reason == "approve":
            if questions:
                fp["clarifications_resolved"] = apply_clarification_answers(
                    fp.get("clarifications_resolved"), answers)
            fp["_approval"] = "approved"
            job.flight_plan = fp
            save_job(job)
            from packages.orchestration.data_paths import job_evidence_export_dir
            log_path = write_assumptions_md(
                fp.get("clarifications_resolved"),
                job_evidence_export_dir(str(job.id)))
            print(f"Flight plan approved for job {job_id_str}.")
            for q in questions:
                qid = q["id"]
                source = "human" if qid in answers else "default"
                print(f"  {qid} ({source}): "
                      f"{answers.get(qid, q['default_answer'])}")
            print(f"Assumption log: {log_path}")
            # F056: last, and only on an explicit --as-mission. An approval
            # without the flag leaves no mission behind — the default is NO.
            if as_mission:
                _create_mission_for_job(job)
        else:
            fp["_approval"] = "rejected"
            job.flight_plan = fp
            save_job(job)
            print(f"Flight plan rejected for job {job_id_str}.")
            print(f"Run: remedy do replan {job_id_str}")
<<<END CLIFROM_C

<<<SLICE CLITO_C
        if reason == "approve":
            log_path = resolve_flight_plan_approval(
                job, reason="approve", answers=answers, questions=questions)
            print(f"Flight plan approved for job {job_id_str}.")
            for q in questions:
                qid = q["id"]
                source = "human" if qid in answers else "default"
                print(f"  {qid} ({source}): "
                      f"{answers.get(qid, q['default_answer'])}")
            print(f"Assumption log: {log_path}")
            # F056: last, and only on an explicit --as-mission. An approval
            # without the flag leaves no mission behind — the default is NO.
            if as_mission:
                _create_mission_for_job(job)
        else:
            resolve_flight_plan_approval(
                job, reason="reject", answers=answers, questions=questions)
            print(f"Flight plan rejected for job {job_id_str}.")
            print(f"Run: remedy do replan {job_id_str}")
<<<END CLITO_C

Constraints:
1. Apply PLANF009R13, LEDGER13, EXTRACT and the three FROM/TO pairs BYTE FOR BYTE
   out of the committed C0a blob — those are the slices, and this list is what
   "every slice" means anywhere below. Do not retype, rewrap, reflow, reindent or
   whitespace-adjust any of them. If a slice looks wrong to you, apply it as
   written and record the objection in the handback — an objection is recorded,
   never acted on.
2. The commit order is C0a, C0b, C1, C2, C3, C4 and nothing comes between them.
   C1 is the first substantive commit (checklist item 23).
3. PAIR SHAPES, each produced by the reviewer's own mechanical containment test on
   the final bytes and reported here as that test's own output. CLITO_B contains
   CLIFROM_B: false — REWRITE. CLITO_A contains CLIFROM_A: false — REWRITE.
   CLITO_C contains CLIFROM_C: false — REWRITE. Each of the three therefore carries
   the rewrite obligation: its FROM goes 1 to 0 and its TO goes 0 to 1 in
   `apps/cli/commands/decision.py`. EXTRACT is a CODE APPEND to
   `packages/orchestration/flight_plan.py` and carries the ORDERED EQUALITY
   obligation of R-0531 instead of any per-line count.
4. FROM UNIQUENESS, measured by the reviewer in `apps/cli/commands/decision.py` at
   the round base, whole-line and indent-agnostic readings AGREEING at 1 for each:
   CLIFROM_B 1 and 1, CLIFROM_A 1 and 1, CLIFROM_C 1 and 1. CLIFROM_B deliberately
   spans three lines: its last line alone occurs TWICE in that file, so a
   single-line FROM would not have named a unique target (checklist item 25).
5. C2 is an APPEND to `.agent/live_review.md`. Nothing in that file is edited — it
   is an append-only record.
6. WRITE NOTHING BEYOND THE CHANGE SET. In particular: touch nothing under
   `tests/` or `docs/`, add no endpoint code, retire no seam, publish no nonce
   record, and pay down neither R-0636 nor R-0637 — the next round owes all of it.
7. `.remedy-wt/` is gitignored scratch. Every multi-step gate goes into a script
   there; `git status --porcelain` prints 0 lines after each commit. Any worktree
   you create is removed and pruned before the handback.
8. Push with `git push` after C4, the last commit of this round.

Done when:
- G1 `.agent/STOP` ABSENT, read at Step 0 and again before C4.
  `git rev-parse --abbrev-ref HEAD` prints `feature/f009-single-write-channel` at
  every reading. `git status --porcelain` prints 0 lines after each of C0a
  through C4. Report the round base SHA you read at Step 0.
- G2 Transport EQUAL: the scratch file as received, `.agent/authored/f009-r13.md`
  at C0a and `.agent/last_block.md` at C0b all carry the same sha256, byte count
  and line count, equal to the digest named in the task prompt. Write C0b from the
  COMMITTED C0a blob, never from the scratch file again.
- G3 Report, per slice, the newline-included sha256, byte count and line count;
  the COUNT of slices from your own ordered extraction out of the committed C0a
  blob; and the aggregate byte count, line count and slice count over them.
- G4 `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R13. Report its line count
  against the 50-line cap; `^## Goal$` and `^## Next Steps$` each match exactly
  1 line; the first `\bF\d{3}\b` match is `F009`.
- G5 The append at C2 to `.agent/live_review.md`, proved TWICE over independent
  extractors in the general N-paragraph form: (a) the round-base blob is a
  byte-exact PREFIX and the remainder EQUALS a newline plus LEDGER13, reported with
  its sha256, bytes and lines; (b) with N COUNTED BY YOUR SCRIPT AND REPORTED, the
  LAST N blank-line units of the whole file equal LEDGER13's N paragraphs IN ORDER.
  NEGATIVE CONTROL on the FIRST appended paragraph: flip ONE printable ASCII byte
  and confirm BOTH readings REJECT it while both ACCEPT the unflipped value; report
  all four outcomes.
- G6 Line-anchored over `.agent/live_review.md` at the round base and at C2:
  `^- R-\d+ — ` 203 and 203 with all ids DISTINCT at each; `^Done: R-\d+ — ` 2 at
  both; `^Landed: ` 0 at both; `^> Next free id` 0 at both; `^Gate: R\d+ — ` 12 and
  13 over that many DISTINCT keys; `^Gate: R13 — ` 0 and 1. Report the max id at C2
  and the count item 10's rule gives at C2 — line-anchored `^- R-\d+ — ` minus
  line-anchored `^Done: R-\d+ — `. State that value in the handback WITH the rule
  and the commit beside it, per DECISION F009 D10, and report what your script
  printed rather than restating any number from here.
- G7 THE EXTRACTION'S SHAPE, at C3, each half proved separately.
  (a) `packages/orchestration/flight_plan.py`: the round-base blob is a byte-exact
  PREFIX of the C3 file, EXTRACT is an exact SUFFIX of it, and the lines that C3's
  diff ADDS to this path are EXACTLY EXTRACT's lines IN ORDER (R-0531). Report the
  added-line count and confirm the ordered equality as a boolean your script
  printed.
  (b) `apps/cli/commands/decision.py`: for each of the three pairs report, at the
  round base and at C3, the whole-line and the indent-agnostic occurrence counts of
  its FROM and of its TO, the two readings AGREEING; FROM must read 1 then 0 and TO
  0 then 1 for all three. Report also that the C3 file is byte-equal to the file
  obtained by applying the three replacements to the round-base blob in the order
  B, A, C — one reconstruction, one boolean.
- G8 `python3 -m ruff check` EXITS 0 over `packages/orchestration/flight_plan.py`
  and `apps/cli/commands/decision.py` at C3, run in the primary checkout. Take the
  SAME reading at the round base WITHOUT writing to either tracked file: pipe
  `git show <round base>:<path>` into
  `python3 -m ruff check --stdin-filename <path> -`, so `per-file-ignores` still
  resolves by path (checklist item 29). Report both exit codes and, if either is
  non-zero, the rule-code multiset at each so the two can be compared rather than
  demanded equal to zero. The reviewer measured EXIT 0 for both paths at the round
  base; report what YOUR run printed.
- G9 In the PRIMARY checkout at C3, run SERIALLY, never two pytest processes at
  once, and report each exit code and its passed-plus-skipped total without
  predicting either:
  `python3 -m pytest tests/cli/test_plan_approval.py tests/cli/test_decision_answers.py tests/cli/test_mission_cmd.py tests/orchestration/test_bundled_clarification.py -q -rf`
  then `python3 -m pytest tests/cli/test_golden_path.py -q -rf`. Both must EXIT 0.
  The first group is the behaviour-preservation gate for the extraction; the second
  is the canary every handback owes.
- G10 THE PROBE, ordered as a probe and NOT as a colour (checklist item 5). In a
  DISPOSABLE `git worktree` at C3 and never in the primary checkout, replace
  everything AFTER the docstring of `resolve_flight_plan_approval` with the single
  line `    raise AssertionError("probe")` and re-run the first command of G9 in
  that worktree. Report the control's passed count, the exit code and the FULL list of
  failing node ids, taken from the run's own `-rf` short summary and never from a
  regex over `-v` output (R-0611). Then restore the source byte-identically,
  confirm the restoration by sha256 against the C3 blob, remove the worktree and
  run `git worktree prune`. State the resulting `git worktree list` line count.
  Whatever the probe shows is the finding — do NOT adjust the code to produce an
  expected colour, and if NO test fails, say so plainly: that would mean the
  approval suites never reach the extracted function and the extraction has no
  behavioural proof at all.
- G11 The range from the round base to C3: `git diff --name-only` lists EXACTLY
  the paths of the change set above other than `.agent/handoff.md`, the set
  difference empty in both directions. Walk `git rev-list --reverse` and report,
  per commit, that it has ONE parent and its `git show --numstat` insertions, with
  `git diff --numstat` AGREEING on every cell and every cell equal to the `+/-`
  column of your handback's `## Commits` table (checklist item 28). Every commit
  stays under the 500-insertion cap of AGENTS.md DECISION F104 D1. `^<<<SLICE ` and
  `^<<<END ` read 0 lines in `.agent/plan.md`, `.agent/live_review.md`,
  `packages/orchestration/flight_plan.py` and `apps/cli/commands/decision.py` at
  C3. Classify this round's own reflog entries by the operation before the first
  `:` in the reflog subject and report `amend`, `rebase` and `cherry`, which must
  each be 0; assert no total over the whole reflog (R-0601). Report
  `git ls-files .remedy-wt` as a count.
- G12 The handback carries every mandated section of
  docs/agents/handback_template.md, an item-status table holding exactly one row
  for each of C0a, C0b, C1, C2, C3 and C4, the round base SHA, and one line per
  gate — the raw transcripts go in the round report, not in the handback (R-0582).
  Report its line count against the 100 that AGENTS.md allows a bundle of more
  than five commits, and if it exceeds that, carry the AGENTS.md DECISION D15
  stated-cause line naming the count and the mandated content that caused it. Its
  `## Next` section states, in this order: that no `.agent/STOP` is present; the
  open-finding count from G6 WITH item 10's rule and the commit named beside it;
  that the next free id is derived with `max` over the line-anchored entries and
  what that gives; that `.agent/candidates.md` is EMPTY; that the next round is the
  effect table that retires the 501 seam and therefore owes the fixes for R-0636
  and R-0637; and that R-0403, R-0607, R-0608, R-0609, R-0611, R-0613, R-0622,
  R-0630, R-0633 and R-0635 stay routed to a paydown branch.

Handback:    completion report + rewrite `.agent/handoff.md`. The state block
             repeats this Fortschritt line verbatim: 65 % (T001 gebaut · T002
             gebaut bis auf die Publikation · T003 begonnen: die Extraktion) —
             Schätzung
──────────────────────────────────────────────────────────────
