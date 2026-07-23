# STATUS.md Closure Protocol (v3)

> The only path from `[~]` to `[x]`. Reviewer (Window 1) authors; worker
> (Window 2) executes and commits. Grammar reference: ROADMAP.md Part C and
> the accepted F017/F018/F146 lines — the living precedent.

## Preconditions — ALL must hold; any failure aborts closure
1. Every step has a PASS round; every R-XXXX finding is Resolved or listed
   as a documented Medium/Low risk. Latest live_review verdict is PASS or
   PASS WITH RISKS — never PENDING/FAIL.
2. Full relevant suite green — verified by the reviewer running it where it
   has execution; otherwise via raw transcripts (command, exit code, real
   output) plus one reviewer-chosen spot-check. Never a summary.
3. `remedy integrity check --json` → PASS; no relevant untracked files.
4. Feature file's Built State section is current.
5. Working tree clean, branch pushed, worker idle.

## Algorithm
1. **Evidence job (worker).** Final evidence run, fresh job id, feature-
   scoped (`feature_id=<fxxx>`). Record: `Evidence job <job_id>`.
2. **Review zip (worker) — MANDATORY, fresh, never skipped.** Build via the
   canonical sequence below. Verify committed_review_subject spans
   BASE..HEAD and the zip import check passes. Record `package <filename>`
   and `SHA-256 <hash>`. **A failing zip build is a closure BLOCKER** —
   fix or go `[!]`; never close without the package.
3. **Runtime actuals (reviewer; observed only).** Rounds, wall clock,
   models, tokens/cost where the ledger has them; `not-measured` beats a
   guess. → PR description + final report.
4. **STATUS line (reviewer authors, worker applies verbatim).** Template:
   `[x] <Fxxx> — <Name> (<T-slices> complete; accepted <YYYY-MM-DD> · live review <PASS|PASS_WITH_RISKS> — ACCEPTED[ · external verdict <V> — ACCEPTED] · Evidence job <job_id> · package <zip filename> · SHA-256 <hash> · accepted HEAD <full sha>)`
   `accepted HEAD` = the reviewed head the verdict and zip cover (manifest
   committed_review_subject.head_commit). External-verdict segment only
   when an external round happened. Touch no other line.
5. **Final commit + PR (worker).** STATUS edit is the last commit on the
   branch (Rule A4), with final .agent/ state (incl. handoff.md rewrite)
   and Built State touch-up. Then the AGENTS.md PR workflow; description
   carries what/why, key decisions, how to review, changed-files table,
   latest verdict, open-findings count, runtime actuals.
6. **Merge — deferred to the next feature.** The closure PR is NOT merged
   in this session. It merges at the next feature's start via the Open PR
   Gate on Window 1's instruction; the gap is the operator's manual-review
   window. The operator may merge manually at any time instead.
7. **End Window 1** with the feature-done banner. Next feature → fresh
   session; Rule A5 selects it.

## Canonical zip build sequence
<!-- PLACEHOLDER — filled by the worker in the evidence-pipeline repair:
the exact, verified command sequence to stage feature-scoped evidence and
build the review zip from the current committed state, including how to
refresh a stale review_archive_plan and how explicit evidence selection is
passed. No deprecated root-dir auto-selection. -->

## Failure honesty
If any precondition fails, the feature does NOT close. In order: another
repair round; `[!] <Fxxx> — <name> (blocked: <reason>)` authored by the
reviewer, committed by the worker; or an explicit operator decision in
.agent/decisions.md. Pretending completion is the one unforgivable failure
mode (AGENTS.md If-Blocked; P1 verify-before-claiming).
