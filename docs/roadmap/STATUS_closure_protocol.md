# STATUS.md Closure Protocol (v1)

> The only path from `[~]` to `[x]`. Reviewer (Window 1) authors; worker
> (Window 2) executes and commits. Grammar reference: ROADMAP.md Part C and
> the accepted F017/F018/F146 lines, which are the living precedent.

## Preconditions — ALL must hold; any failure aborts closure
1. Every step has a PASS round; every R-XXXX finding is Resolved or listed
   as a documented Medium/Low risk. Latest live_review verdict is PASS or
   PASS WITH RISKS — never PENDING/FAIL.
2. Full relevant suite green — verified by the reviewer running it where it
   has execution; otherwise via raw transcripts (exact command, exit code,
   real output) plus one reviewer-chosen spot-check run by worker or
   operator. Never by trusting a summary.
3. `remedy integrity check --json` → PASS; no relevant untracked files.
4. Feature file's Built State section is current.
5. Working tree clean, branch pushed, worker idle.

## Algorithm
1. **Evidence job (worker).** Final evidence run, fresh job id, feature-
   scoped (`feature_id=<fxxx>` threading via refresh_review_evidence.py /
   runtime gate). Record: `Evidence job <job_id>`.
2. **Review zip (worker).** scripts/make_review_zip.sh. Verify the
   manifest's committed_review_subject spans BASE..HEAD and the zip import
   check passes. Record `package <filename>` and `SHA-256 <hash>`.
3. **Runtime actuals (reviewer; observed numbers only).** Rounds, wall
   clock, models, tokens/cost where the ledger has them. `not-measured`
   beats a guess. These go in the PR description and final report.
4. **STATUS line (reviewer authors, worker applies verbatim).** Template:
   `[x] <Fxxx> — <Name> (<T-slices> complete; accepted <YYYY-MM-DD> · live review <PASS|PASS_WITH_RISKS> — ACCEPTED[ · external verdict <V> — ACCEPTED] · Evidence job <job_id> · package <zip filename> · SHA-256 <hash> · accepted HEAD <full sha>)`
   `accepted HEAD` = the reviewed head the verdict and zip cover (manifest
   committed_review_subject.head_commit) — deterministic, known before the
   STATUS commit. Include the external-verdict segment only when an
   external round actually happened. Touch no other line.
5. **Final commit + PR (worker).** STATUS edit is the last commit on the
   feature branch (Rule A4), together with final .agent/ state and Built
   State touch-up. Then the AGENTS.md Pull Request Workflow; the PR
   description carries what/why, key decisions, how to review, changed-
   files table, latest verdict, open-findings count, runtime actuals.
6. **Merge (operator).** Agents do not merge without instruction. After
   merge: `git checkout main && git pull --ff-only`.
7. **End Window 1.** Next feature → fresh session; Rule A5 selects it.

## Failure honesty
If any precondition fails, the feature does NOT close. In order: another
repair round; `[!] <Fxxx> — <name> (blocked: <reason>)` authored by the
reviewer, committed by the worker; or an explicit operator decision in
.agent/decisions.md. Pretending completion is the one unforgivable failure
mode (AGENTS.md If-Blocked; P1 verify-before-claiming).
