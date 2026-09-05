STEP OPERATOR RULING (OPTION B) + F267 REGISTRATION / ROUND 24 - F262 List commands v2 (dates, sort, filter)
FEATURE F262 - List commands v2 (dates, sort, filter) (Tier 2) - SESSION 9, ROUND 24

Goal
  Book round 23's PASS verdict (RECORD23) and one reviewer numeral slip
  (SLIPF262R24); record the operator's 2026-09-05 ruling, Option B, as
  DECISION F262 D5 together with D6 (the ordered packaging finding,
  examined on the evidence and declined); register the follow-up
  feature F267 with ledger atomicity; bring T2_F262.md's Built State
  current (closure precondition 4) and point .agent/context.md at the
  new scope. No production code, no test behaviour change (the only
  tests/ edit is the TOTAL_FEATURES pin and its comment).

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f262-r24.md
  C0b mirror it to .agent/last_block.md
  C1  apply RECORD23 to .agent/live_review.md (append), SLIPF262R24 to
      .agent/prose_slips.md (append), PLAN25 to .agent/plan.md
      (whole-file replacement)
  C2  apply DECISIONS to .agent/decisions.md (append)
  C3  THE REGISTRATION COMMIT, four files in ONE commit: write F267FILE
      as the NEW file docs/roadmap/features/T2_F267.md; apply the
      STATUS pair to docs/roadmap/STATUS.md, the TESTPIN pair to
      tests/docs/test_docs_consistency.py, the README_COUNT and
      README_TIER2 pairs to README.md
  C4  apply the F262BANNER pair to docs/roadmap/features/T2_F262.md,
      then append F262APPEND to it; apply the CONTEXT pair to
      .agent/context.md
  C5  rewrite .agent/handoff.md - the handback; then push

Change set - EXACTLY these paths and nothing else
  .agent/authored/f262-r24.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md, .agent/prose_slips.md, .agent/plan.md (C1) -
  .agent/decisions.md (C2) - docs/roadmap/features/T2_F267.md (new),
  docs/roadmap/STATUS.md, tests/docs/test_docs_consistency.py,
  README.md (C3) - docs/roadmap/features/T2_F262.md, .agent/context.md
  (C4) - .agent/handoff.md (C5)

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by its
     one-line BEGIN/END markers from the COMMITTED
     .agent/authored/f262-r24.md (marker lines EXCLUDED) and write it
     with a Python script (pathlib read_bytes/write_bytes), never by
     retyping. If a slice looks wrong, apply it as written and DECLARE
     it in the handback.
  2. C1 is the first substantive commit of the round (it advances
     .agent/plan.md before anything else moves).
  3. NEWLINE CONVENTIONS, per target: RECORD23 appends to
     .agent/live_review.md as EXACTLY TWO newline bytes followed by the
     slice (this branch's blank-line-separated paragraph convention,
     the same as rounds 21-23); SLIPF262R24 appends to
     .agent/prose_slips.md as EXACTLY TWO newline bytes followed by the
     slice; DECISIONS appends to .agent/decisions.md as EXACTLY ONE
     newline byte followed by the slice (this file's consecutive
     `## DECISION` convention, confirmed at D2/D3/D4's boundaries).
     RECORD23, SLIPF262R24, DECISIONS and PLAN25 carry NO trailing
     newline of their own. F267FILE ENDS WITH exactly one newline (a
     whole file) and creates its target. F262APPEND is PURE
     CONCATENATION onto the end of T2_F262.md (its leading blank line is
     inside the slice, and it ends with one newline).
  4. Pairs are applied with str.replace(FROM, TO, 1) on the named file
     after confirming FROM occurs EXACTLY ONCE in it. Containment
     readings, computed before emission: STATUS `TO contains FROM:
     false` (REWRITE), TESTPIN `TO contains FROM: false` (REWRITE),
     README_COUNT `TO contains FROM: false` (REWRITE), README_TIER2
     `TO contains FROM: false` (REWRITE), F262BANNER `TO contains FROM:
     false` (REWRITE), CONTEXT `TO contains FROM: false` (REWRITE).
     Re-check each reading yourself and report what
     you measured beside what is labelled; no FROM-zero count is
     ordered for any pair.
  5. Read .agent/STOP from disk before C0a, before C3 and before C5. If
     it exists, finish the commit in hand, write the handback, stop.
  6. Sandbox forms this session refuses are RE-EXPRESSED, never
     skipped: `VAR=x cmd`, `export`, `cp`, `cmp`, shell loops, `$( )`
     in compounds, any path under `.remedy-wt/`. Use Python
     (`shutil.copyfile`, `pathlib`, `subprocess.run(...).returncode`)
     and `bash -c '<cmd>; echo REAL_EXIT=$?'` for exit codes. The
     `remedy` binary is denied; nothing this round needs it. Report
     every re-expression.
  7. THE OPEN SET is counted by docs/agents/planner_reviewer_prompt.md
     §3 item 10's line-count formula: registered `^- R-\d{4} — `
     paragraphs minus `^Done: R-\d{4} — ` lines. This round registers
     no id and resolves none: report registered/Done/open BEFORE C1 and
     AFTER C1 and confirm both UNCHANGED at 356 / 77 / 279.
  8. Commit subjects follow `F262 R24 C<n>: <what>` and contain no
     leading-slash token, absolute path or secret-like string.
  9. Attempt `ruff check tests/docs/test_docs_consistency.py` after C3
     and report its result or the exact refusal text; the file's only
     change is a comment and one integer.
  10. This round does not touch packages/ or apps/; tests/ is touched
      only at tests/docs/test_docs_consistency.py (C3). No pull request,
      no merge, `main` untouched. Push after C5:
      `git push -u origin feature/f262-list-commands-v2`, report result.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 HYGIENE. `.agent/STOP` absent at each of constraint 5's
     reads (report all three); `git status --porcelain | wc -l` is 0
     after each of C0a, C0b, C1, C2, C3, C4 (report each);
     `git ls-files .remedy-wt | wc -l` is 0.
  G2 TRANSPORT. `sha256sum .agent/authored/f262-r24.md
     .agent/last_block.md` - one digest, twice; report both lines
     verbatim. (The reviewer compares the committed authored file
     against its own scratch original itself.)
  G3 THE RECORD APPENDS AT C1, each reconstructed. (a)
     .agent/live_review.md: base size immediately before C1 (expect
     2491115, no trailing newline), RECORD23's own byte length (expect
     3578, zero internal newlines), base + 2 + that length (expect
     2494695) versus the post-C1 file's length; second reader: the
     post-C1 bytes from `base` to end equal exactly "\n\n" + RECORD23;
     negative control in a scratch COPY only: flip one byte inside
     RECORD23's text and confirm the second reader REJECTS it. (b)
     .agent/prose_slips.md: base size immediately before C1 (expect
     73583, no trailing newline), SLIPF262R24's own byte length
     (expect 965), base + 2 + that length (expect 74550) versus
     the post-C1 length; tail equality "\n\n" + SLIPF262R24.
  G4 THE DECISIONS APPEND AT C2. Base size of .agent/decisions.md
     immediately before C2 (expect 809282, no trailing newline),
     DECISIONS' own byte length (expect 8760), base + 1 + that
     length (expect 818043) versus the post-C2 length; tail equality
     "\n" + DECISIONS; `grep -c '^## DECISION F262 D5'` and
     `grep -c '^## DECISION F262 D6'` each read 1 after C2 and 0 before.
  G5 THE WHOLE FILES. After C1: .agent/plan.md equals PLAN25 byte for
     byte (report both lengths and the boolean; expect 2039),
     `wc -l .agent/plan.md` under 50 (expect 43, one less
     than its logical line count, no trailing newline), `grep -c
     '^## Goal'` and `grep -c '^## Next Steps'` each 1. After C3:
     docs/roadmap/features/T2_F267.md equals F267FILE byte for byte
     (expect 4772 bytes). After C4: docs/roadmap/features/T2_F262.md
     measures 6829 bytes (it read 4232 at `6991059c`; banner pair
     +84, F262APPEND 2513) and its bytes from the
     pre-append length to the end equal F262APPEND exactly.
  G6 THE PAIRS. For each of STATUS, TESTPIN, README_COUNT,
     README_TIER2 (C3), F262BANNER and CONTEXT (C4): FROM count in the target file
     immediately before applying (must be 1), the measured `TO contains
     FROM` reading beside constraint 4's label. After C3 report the new
     STATUS.md F267 line, README.md's accepted-count line and Tier 2
     row, and `grep -c '^TOTAL_FEATURES = 267'
     tests/docs/test_docs_consistency.py` (expect 1), exactly as they
     read.
  G7 THE SUITES, SERIALLY, EACH ITS OWN INVOCATION, after C4:
       python3 -m pytest tests/docs/ -q                          (expect 295)
       python3 -m pytest tests/orchestration/test_roadmap_index.py -q  (expect 30)
       python3 -m pytest tests/ui_server/ -q                     (expect 515)
       python3 -m pytest tests/orchestration/test_test_runner.py -q    (expect 52)
       python3 -m pytest tests/regression/test_resource_safety.py -q   (expect 21)
       python3 -m pytest tests/orchestration/test_integrity_gate.py -q (expect 16)
       python3 -m pytest tests/cli/test_golden_path.py -q        (expect 42)
     Report each real count; a differing count is reported, never
     papered over. Plus constraint 9's ruff attempt.
  G8 STRUCTURE. Per-commit `git show --numstat --format=""` for C0a,
     C0b, C1, C2, C3 and C4 against this handback's own Commits table,
     cell for cell; each commit single-parent, each under 500
     insertions; `git diff --stat 6991059c..<C4> -- packages/ apps/`
     empty; `git diff --name-only 6991059c..<C4> -- tests/` names
     exactly tests/docs/test_docs_consistency.py; the push result.

The authored slices. Each lies between its own one-line BEGIN and END
marker; markers are excluded from what is applied.

<<<BEGIN RECORD23>>>
Gate: R23 — the F262 R23 entry. R23 WAS THE SCOPE-CORRECTION ROUND, NO CODE BY DESIGN (a wrong spec routed to planning, docs/agents/planner_reviewer_prompt.md §4 item 7): it booked GATE22, converted R-0795 to Done, registered FINDING R-0796 (13 of the catalog's 28 list-shaped commands never wired to `apply_list_options`, not 3), registered DECISION F262 D4 (closure Acceptance scoped to 24 of 28, the 3 static registries and the 1 hybrid excluded by name, the 9 genuine gaps deferred), appended the D4 pointer to `docs/roadmap/features/T2_F262.md`, replaced `.agent/plan.md` with PLAN24 and handed the operator the Option A / Option B proposal — AND THE REVIEWER RE-RAN EVERY GATE ITSELF, in a fresh session (session 9), independently. VERDICT PASS over the range `2e7e68b6..6991059c` (C0a `df0d10cc`, C0b `220780e1`, C1 `b022e1e1`, C2 `1ce38723`, C3 `b3e09695`, C4 `70d08235`, C5 `89ac80ba`, C6 `e89d302f`, handback `6991059c`). TRANSPORT HELD: `sha256sum .agent/authored/f262-r23.md .agent/last_block.md` printed one identical digest, `f14fce8e5ce2f78e6d3d75c3ba3c504bd0d0349aeafcc70aef213be9c6d6a167`, for both files, reproduced exactly. THE LEDGER APPENDS HELD, reproduced by byte reads of the tracked blobs at each commit: 2482540 (at `220780e1`) plus two newlines plus GATE22 (3174 bytes) equals 2485716 (at `b022e1e1`); plus two newlines plus the Done: R-0795 text (1269 bytes) equals 2486987 (at `1ce38723`); plus two newlines plus FINDING R-0796 (4126 bytes) equals 2491115 (at `b3e09695`) — all exact. THE DECISIONS APPEND HELD: 806068 (at `b3e09695`) plus one newline plus DECISION F262 D4 (3213 bytes) equals 809282 (at `70d08235`), exact. THE FEATURE-FILE APPEND HELD: `docs/roadmap/features/T2_F262.md` read 3504 bytes at `70d08235` and 4232 at `89ac80ba`, the 728-byte amendment concatenated verbatim. THE PLAN HELD: `.agent/plan.md` at `6991059c` measured 2248 bytes, byte-for-byte equal to the PLAN24 slice extracted from the committed `.agent/authored/f262-r23.md`. THE SUITES HELD, reproduced independently: `tests/docs/` 295 passed (the docs-round gate, since C5 touched `docs/roadmap/**`), `tests/cli/test_golden_path.py` 42 passed (canary). HYGIENE HELD at `6991059c`: `git status --porcelain` empty, `git ls-files .remedy-wt` empty, `.agent/STOP` absent; `git diff --stat 2e7e68b6..6991059c` names only `.agent/**` paths and `docs/roadmap/features/T2_F262.md`, no `apps/`, `packages/` or `tests/` path, exactly as constraint 5 of that block required. ONE DEVIATION WAS DECLARED BY THE ROUND (PLAN24 written without a trailing newline to land on the ordered 2248 bytes — the on-disk bytes match the slice, nothing wrong on disk). ONE REVIEWER NUMERAL SLIP IS RECORDED THIS ROUND in `.agent/prose_slips.md`, no id spent: R-0796, D4 and PLAN24 all say three rounds of the 25-round soft cap remained after round 23 where two did (rounds 24 and 25), as the round's own handback correctly stated. Open findings after this entry, canonical line-count formula (§3 item 10): 356 registered R-ids minus 77 `Done:` lines equals 279 open, unchanged by this entry; `.agent/candidates.md` remains EMPTY. THE PROPOSAL THE ROUND MADE IS RULED THIS ROUND: the operator's instruction of 2026-09-05 chooses Option B, recorded as DECISION F262 D5 in `.agent/decisions.md` — F262 closes at D4's 24-of-28 scope, the nine remaining wirings split into the newly registered feature F267, and rule 6's operator gate is discharged for F262 exactly as the 2026-09-04 ruling discharged it for F112, so F262's closure sequence continues on its own round budget from here.
<<<END RECORD23>>>

<<<BEGIN SLIPF262R24>>>
2026-09-05 · F262 R24 (reviewer) · Round 23's three authored texts state THREE remaining rounds of the 25-round soft cap — FINDING R-0796 ("3 of the 25-round soft cap remain"), DECISION F262 D4 ("F262 has 3 rounds left of its 25-round soft cap") and PLAN24's Option B ("within the 3 rounds left") — while the same round's handback correctly states two: round 23 of 25 leaves rounds 24 and 25. The reviewer carried the previous block's arithmetic (25 minus 22) into texts written FOR round 23 instead of re-deriving it from the round number those texts themselves carry. THE LESSON: a remaining-budget numeral is derived from the round number the slice itself names (25 minus that round), never copied from the block before. Reviewer-authored numeral slip; nothing wrong on disk under `packages/`, `apps/`, `tests/` or `docs/`, and DECISION F262 D5 supersedes the budget question entirely, so no correction round; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIPF262R24>>>

<<<BEGIN DECISIONS>>>
## DECISION F262 D5 (2026-09-05, F262 R24) — OPERATOR RULING, OPTION B: F262 closes at DECISION F262 D4's 24-of-28 scope; the nine remaining wirings, the catalog-driven handler test and the Acceptance smoke test split into the newly registered feature F267; amend0827 rule 6's operator gate is discharged for F262

CONTEXT. Round 23 (FINDING R-0796, DECISION F262 D4) found nine list-shaped commands with genuine dates still unwired to `apply_list_options` and, at round 23 of the 25-round soft limit and session 8 of the 7-session one, handed the operator the Option A / Option B proposal that amend0827-process-diet rule 6 requires and forbids the session to execute on its own authority. The operator's instruction of 2026-09-05 rules: "THE OPERATOR RULES OPTION B: F262 closes at the 24-of-28 scope DECISION F262 D4 already records; the remaining work splits into a new registered feature. This ruling discharges rule 6's operator gate for F262 exactly as the 2026-09-04 ruling did for F112 — F262's closure continues on its own round budget."

CHOSEN. (1) F262's Acceptance is D4's: 24 of the catalog's 28 list-shaped commands, of which the 15 wired at `6991059c` (job.list, queue.list, loop.list, project.list, patch.list, worker.list, tournament.list, memory.list, blocker.list, decision.list, external-builder.submission-list, review.list, propose.list, config.list, execution.list — measured as the 15 files `grep -rl "apply_list_options(" apps/cli/commands/` names) are F262's built scope and the other 9 (test.list, repair.item-list, builder.session-list, execution.approval-list, mission.list, change.list, event.list, external-builder.package-list, self-repair.proposal-list) leave F262 and become F267's T001. (2) The T001 catalog-driven HANDLER test (proving every list handler honours its flags, not merely parses them — the gap Done: R-0795 named as never built) and the Acceptance smoke test (the ten-second demo) move to F267 as its T002 and T003; F262 keeps the argparse-level catalog pin `tests/test_command_catalog.py::TestListCommandOptions` it already ships. (3) F267 is registered THIS round, registration only, with ledger atomicity: the `TOTAL_FEATURES` pin in `tests/docs/test_docs_consistency.py`, the README counters and the new `docs/roadmap/STATUS.md` line land in one commit with `docs/roadmap/features/T2_F267.md`. The STATUS line sits at the END of the canonical `## Tier 2 — Minimal Self-Build Runtime` block, directly after F086's line, per STATUS.md's own header rule ("absent [an operator-chosen position], at the end of the matching tier block") — the operator named no position, and placing it ahead of F259 inside the amend0831 block would have altered the operator-decided order F262, F259, F260, F261, F263 and falsified that block's "eight lines below" comment. (4) F267 carries forward the round-8 handback's change.list note: the only production emitter of patch-intent creation is `do_run_patch_intent_created`, which no consumer reads, while every reader checks a bare `patch_intent_created` that no production code emits — an event-name mismatch to investigate before change.list is wired. (5) Rule 6's obligation is DISCHARGED for F262: no further scope report is owed and the `SITZUNGS-LIMIT ERREICHT` line is no longer emitted for this feature; the closure sequence (integration gate, preconditions 3 and 6, evidence job, review zip, closure commit, pull request) proceeds as ordinary rounds.

ALTERNATIVES CONSIDERED AND REJECTED. Option A — sessions beyond the soft caps to wire all nine inside F262 — rejected by the operator. Closing F262 with the nine silently dropped — rejected in D4 already. Placing F267 directly after F262's own line — rejected for the ordering reason in CHOSEN (3).

CONSEQUENCE, stated plainly. F262 ships the shared option surface (T001), the CREATED/UPDATED dates (T002) and the sort/filter/limit behaviour with its newest-first default (T003) on 15 commands; nine commands parse the four flags and still ignore them until F267 lands, and FINDING R-0796 stays OPEN across F262's closure as documented Medium risk, owned by F267. F262's ten-second-demo Acceptance is demonstrable today on the 15 wired commands and is proved by a test only when F267 T003 ships.

REVERSE by deleting this decision and F267's registration (its STATUS line, `docs/roadmap/features/T2_F267.md`, the `TOTAL_FEATURES` pin and README counter edits of the same commit); the nine wirings then return to F262's open scope and rule 6's obligation returns with them.
## DECISION F262 D6 (2026-09-05, F262 R24) — the operator-ordered Medium finding "packaging validation is non-deterministic" is NOT registered: the two F114 zips were built from DIFFERENT evidence, the second a deliberate red control

CONTEXT. The operator's instruction of 2026-09-05, Part 1 step 3, orders one new Medium finding on operator-supplied evidence: on 2026-09-04 the F114 closure produced two review zips 44 seconds apart from the same evidence job `f114-closure` — 18:57:43 READY_FOR_REVIEW, 18:58:26 BLOCKED_EVIDENCE — the blocked manifest naming "final_verifier_report.json test_status.passed cannot be confirmed: the VerificationTests total is missing or invalid", "verification_tests.json field verification_tests.runs[0].node_ids[19] carries a local absolute path" and "verification_tests.json runs[0] node_ids count (20) != selected (19)"; the instruction reads same evidence, opposite verdicts, hence non-determinism.

MEASURED by the reviewer on 2026-09-05, over the files on disk, before authoring this round. Both packages exist under `/home/decodeux/Repos/remedy-history/zips`. `remedy-review-20260904-185732-READY_FOR_REVIEW.zip`: manifest generated 2026-09-04T16:57:43Z, `committed_review_subject.head_commit` `6e0c2124723c9f55bfa1481b56bbcfe8ad2d2bc6`, run `vr-0001` selected 19 with 19 node ids, `blocking_reasons` empty. `remedy-review-20260904-185816-BLOCKED_EVIDENCE.zip`: manifest generated 2026-09-04T16:58:26Z, the same head commit, run `vr-0001` selected 19 with TWENTY node ids, the twentieth reading `/home/decodeux/Repos/remedy/tests/orchestration/test_cost_preview.py::test_absolute_path_injection` — a node id no test file defines — and exactly the three blocking reasons quoted above. That twentieth id is the one F114 round 17's block ORDERED: `.agent/authored/f114-r17.md`, section "The zip and the red control", item 2: "Copy the evidence directory to a SECOND directory under `.remedy-wt/`, append ONE node id containing an absolute path to the first run of that copy's `verification_tests.json`, and build a zip from the COPY. It must report `PACKAGE_STATUS=BLOCKED_EVIDENCE` ... Declare this as a DELIBERATE CONTROL." The round's handback (`.agent/handoff.md` at `af075516`, item-status row "red control | done | PACKAGE_STATUS=BLOCKED_EVIDENCE, exit 0, 3 blocking reasons") and the ledger's RECORD17 ("THE RED CONTROL WAS OPENED, NOT TAKEN ON REPORT: the deliberately mutated copy packaged `remedy-review-20260904-185816-BLOCKED_EVIDENCE.zip` ... proving the pipeline distinguishes a poisoned bundle from the real one") both record it as such. The 44-second gap is the control build following the live build.

CHOSEN. No finding is registered. The two zips did not share evidence: one was built from the real bundle, the other from a copy poisoned on purpose with one absolute-path node id, and the validator answered each correctly — READY for the clean bundle, BLOCKED with the three defects the poisoning introduces for the poisoned one. That is the validator being deterministic and right, not wrong. Nothing on disk under `packages/`, `apps/`, `tests/` or `docs/` is defective, so amend0827-process-diet rule 2 leaves no product-effect defect for an R-id to name, and `scripts/build_review_manifest.py` and `packages/orchestration/job_evidence.py` need no paydown item from this. This DECISION is the record of the examination, in place of the finding.

ALTERNATIVE CONSIDERED AND REJECTED. Register the finding as ordered. Rejected: its load-bearing claim — same evidence, opposite verdicts — is false on the evidence above, and a false load-bearing claim in the append-only record is the one thing docs/agents/planner_reviewer_prompt.md §4 item 5 ("fabricated data") and docs/roadmap/STATUS_closure_protocol.md's failure-honesty clause exist to prevent; an operator instruction to record a fact does not make the fact true. Recording the decline loudly and reversibly here follows §4 item 7 rather than asking the operator a question.

REVERSE by deleting this decision; registering the finding afterwards would need evidence that two packages built from one UNMODIFIED evidence directory disagreed, which the 2026-09-04 pair does not supply.
<<<END DECISIONS>>>

<<<BEGIN PLAN25>>>
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md, scoped by DECISION F262 D4; the nine
remaining wirings are F267's per DECISION F262 D5).

## Current Step

Round 24, session 9 — the operator ruled Option B (2026-09-05). This
round books GATE23 and one prose slip, records DECISION F262 D5 (the
ruling) and D6 (the ordered packaging finding examined and declined on
evidence), registers F267 with ledger atomicity (STATUS line,
T2_F267.md, TOTAL_FEATURES 267, README counters), and brings
T2_F262.md's Built State current (closure precondition 4). No code.

## Next Steps

- Integration gate round (docs/agents/integration_gate.md steps 1-5,
  merge-base `7c65d9cc`): the worker measures, the reviewer issues the
  gate verdict at the following round.
- Closure preconditions 3 and 6: `integrity check --json` via the
  `apps.cli.grouped` module route; the self-use queue is exhausted (all
  eight items consumed), so `generate_and_append_if_empty` first, then
  run the item to the approval gate and register what
  `describe_self_use_run_defects` returns.
- Closure algorithm steps 1-2 (evidence job `f262-closure`, fresh review
  zip with red control), then the closure commit (STATUS `[x]`, README
  sync, `consumed_by=F262`) and the pull request.
- Merge under the operator's 2026-09-05 authorization once hosted CI
  reads green (checks read as their own command first).

## Risks

- R-0796 stays OPEN across closure as documented Medium risk, owned by
  F267 — nine commands parse the four flags and ignore them until then.
- The integration gate's base run needs UI parity in the base worktree
  (copytree symlinks=True, dist re-stamp — R-0591, R-0736).
<<<END PLAN25>>>

<<<BEGIN F267FILE>>>
# T2_F267 — List commands v2 completion — sort/filter/limit for the remaining nine commands
**Tier 2 · Depends on: F262 · Blocks/used by: nothing**

> Registered 2026-09-05 by operator ruling amend0905-throughput (DECISION F262
> D5, Option B), splitting the remaining scope off F262 at its closure.
> REGISTRATION ONLY — nothing in this file has been implemented.

## Goal & Done
The nine list-shaped commands F262 left parsing the shared flags but ignoring
them honour `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
exactly as the fifteen F262 wired do, with newest-first as the default, and
two tests F262 never built prove the whole catalog rather than a sample:

- test.list · repair.item-list · builder.session-list ·
  execution.approval-list · mission.list · change.list · event.list ·
  external-builder.package-list · self-repair.proposal-list

DONE when every one of the nine exits non-zero on `--sort bogus` naming its
valid fields, `--limit`/`--since`/`--until` filter its real rows, the
catalog-driven handler test is green over all 24 in-scope commands, and the
ten-second demo is a test, not a claim.

## Why this exists
F262's round 23 (FINDING R-0796 in `.agent/live_review.md`) measured the
catalog mechanically: 28 list-shaped commands, 15 wired to
`packages/orchestration/list_options.apply_list_options`, 13 not. DECISION F262
D4 excluded four of the 13 permanently — `builder.adapter-list`,
`execution.template-list`, `worker.registry-list` (no date on their row shape)
and `approval.policy-list` (browsed by name/state, not recency) — and kept the
nine above IN scope because each has a genuine date field and is exactly the
class T003 exists to fix. They did not fit F262's remaining round budget, and
the operator ruled (DECISION F262 D5) to close F262 at the 24-of-28 scope and
finish the nine here rather than run F262 past its soft limits.

## Design
- Reuse, never re-implement: every wiring is one `apply_list_options` call over
  the handler's already-built row list, with `sort_fields` naming that
  command's own columns and `default_sort_field` naming its genuine date
  (`created_at`, `started_at`, `timestamp`, ...), the same shape as the
  fifteen landed wirings (`apps/cli/commands/job.py` is the reference).
- The same call feeds `--json` and text rendering, so both stay identical.
- `event.list` already carries its own `--since`/`--limit` `ArgDef`s (the one
  pre-existing exception `_with_list_options` names); the wiring keeps their
  spelling and routes them through the shared helper.
- `change.list`'s recency lives in nested `approval`/`apply`/`proof`/`test`/
  `revert` dicts with no flat field; its `date_getter` must resolve that.

## T001 — The nine wirings
Batches of one to three commands per round, each with two regression tests
(`--limit` caps the rows; an unknown `--sort` exits non-zero naming the valid
set), following the F262 R13–R22 precedent. change.list LAST, after the
investigation the Orchestrator brief orders.

## T002 — The catalog-driven handler test
One test that derives the list-command set from `apps/cli/command_catalog.py`
(never a hand-written list), invokes every in-scope handler with `--sort
bogus`, and asserts a non-zero exit naming the valid fields — proving the
HANDLER honours the flag, which `TestListCommandOptions` (argparse-level, F262
T001) cannot. The four D4 exclusions are named in the test by id and reason.

## T003 — The Acceptance smoke test
The ten-second demo as a test: seed a store with a run dated two days ago,
find it with one command using `--since 3d --until 1d`, assert the row.

## Acceptance
- Each of the nine: `--sort bogus` exits non-zero and names the valid fields;
  `--limit 1` returns one row; `--since`/`--until` filter by the row's date.
- The catalog-driven handler test covers all 24 in-scope commands.
- The ten-second demo passes as a test.

## Do not touch
The stores' own schemas beyond adding a missing timestamp, the `--json`
contract's existing keys, and the four D4 exclusions — a feature adding
genuine per-policy history would revisit `approval.policy-list`, not this one.

## Orchestrator brief
INVESTIGATE FIRST, before any change.list wiring (carried forward from F262's
round-8 handback, commit `74cfbd28`): the only production emitter of
patch-intent creation is `do_run_patch_intent_created`, which no consumer
reads, while every reader checks a bare `patch_intent_created` that no
production code emits. change.list's CREATED date (DECISION F262 D1,
Alternative section) depends on settling which event name is real; wiring a
sort over a date that is never populated would be the R-0795 class again.
Then T001 in batches, T002, T003. Findings carried: R-0796 (open, owned here).
<<<END F267FILE>>>

<<<BEGIN F262BANNER_FROM>>>
**Tier 2 · Depends on: none · Blocks/used by: nothing**

> Registered 2026-08-31 by operator order amend0831-vocab-registrations.
> REGISTRATION ONLY — nothing in this file has been implemented.
<<<END F262BANNER_FROM>>>

<<<BEGIN F262BANNER_TO>>>
**Tier 2 · Depends on: none · Blocks/used by: F267**

> Registered 2026-08-31 by operator order amend0831-vocab-registrations.
> Built across rounds 1–23 (2026-09-04/05); scope per DECISION F262 D4 and D5,
> Built State below. The nine remaining wirings are F267's (T2_F267.md).
<<<END F262BANNER_TO>>>

<<<BEGIN F262APPEND>>>

## Amendment (DECISION F262 D5, 2026-09-05 — operator ruling, Option B)
The nine deferred commands above, the catalog-driven HANDLER test and the
ten-second-demo Acceptance smoke test LEAVE F262 and are F267's T001–T003
(`T2_F267.md`). F262 closes on the 15 wired commands; the Acceptance bullets
"the ten-second demo" and "the catalog test proves no list command is missing
a flag" are met here at the argparse level (`TestListCommandOptions`) and on
the wired 15, and are proved catalog-wide by F267. FINDING R-0796 stays open
across this closure as documented Medium risk, owned by F267.

## Built State (2026-09-05, rounds 1–23, ledger `Gate: R1`–`Gate: R23`)
- T001 (round 2): `apps/cli/command_catalog.py` — `_is_list_command` and
  `_with_list_options` attach `--sort`, `--desc`, `--since`, `--until` and
  `--limit` mechanically to every `list`/`*-list` entry when `CATALOG` is
  built (28 commands at `6991059c`); `event.list`'s pre-existing `--since`/
  `--limit` are kept by name. Pinned by
  `tests/test_command_catalog.py::TestListCommandOptions` (every list command
  carries all four flags, exactly one `--desc`, the parser builds).
- T002 (rounds 3–12): CREATED/UPDATED — or the store's own equivalent
  (resolved, started, ended) — surfaced in text and `--json` on the commands
  each round's ledger entry names; DECISION F262 D1 fixed the CREATED source
  for patch/loop rows. Test files touched are listed by
  `git diff --name-only 7c65d9cc..6991059c -- tests/`.
- T003 (rounds 13–22): `packages/orchestration/list_options.py` —
  `apply_list_options`, `parse_time_bound` (ISO-8601 or `2d`/`12h`/`30m`/
  `45s`), `ListOptionError`; newest-first via `default_sort_field`, unknown
  `--sort` raises naming the valid set, `--limit` validated. Unit tests:
  `tests/orchestration/test_list_options.py`. Wired into 15 commands —
  job.list, queue.list, loop.list, project.list, patch.list, worker.list,
  tournament.list, memory.list, blocker.list, decision.list,
  external-builder.submission-list, review.list, propose.list, config.list,
  execution.list — each with `--limit` and unknown-`--sort` regression tests
  in its own `tests/cli/` file. DECISION F262 D2 keeps queue.list's priority
  order and D3 keeps loop.list's config-declaration order as their defaults.
- NOT built here, by decision: the nine wirings, the handler test and the
  smoke test (F267, D5); the four D4 exclusions (permanent).
- Findings: R-0795 resolved (round 22); R-0796 open, owned by F267.
<<<END F262APPEND>>>

<<<BEGIN STATUS_FROM>>>
accepted HEAD f5fa19c368ed15d14ee6067fc69fde4fbc7863a6)

Milestone R1 — Remedy as the daily tool
<<<END STATUS_FROM>>>

<<<BEGIN STATUS_TO>>>
accepted HEAD f5fa19c368ed15d14ee6067fc69fde4fbc7863a6)
- [ ] F267 — List commands v2 completion — sort/filter/limit for the remaining nine commands

Milestone R1 — Remedy as the daily tool
<<<END STATUS_TO>>>

<<<BEGIN TESTPIN_FROM>>>
#: T5_F265.md and T4_F266.md.
TOTAL_FEATURES = 266
<<<END TESTPIN_FROM>>>

<<<BEGIN TESTPIN_TO>>>
#: T5_F265.md and T4_F266.md. One more, F267 (list commands v2 completion:
#: the nine sort/filter/limit wirings DECISION F262 D5 split off F262), was
#: registered on 2026-09-05 under operator ruling amend0905-throughput; see
#: T2_F267.md.
TOTAL_FEATURES = 267
<<<END TESTPIN_TO>>>

<<<BEGIN README_COUNT_FROM>>>
71 of 266 registered items accepted.
<<<END README_COUNT_FROM>>>

<<<BEGIN README_COUNT_TO>>>
71 of 267 registered items accepted.
<<<END README_COUNT_TO>>>

<<<BEGIN README_TIER2_FROM>>>
| 2 | Minimal Self-Build Runtime | 14 | 19 |
<<<END README_TIER2_FROM>>>

<<<BEGIN README_TIER2_TO>>>
| 2 | Minimal Self-Build Runtime | 14 | 20 |
<<<END README_TIER2_TO>>>

<<<BEGIN CONTEXT_FROM>>>
F262 (Tier 2, depends on nothing, blocks nothing): every list command —
<<<END CONTEXT_FROM>>>

<<<BEGIN CONTEXT_TO>>>
F262 (Tier 2, depends on nothing, blocks F267 — the follow-up DECISION F262
D5 split off on 2026-09-05; scope per DECISION F262 D4: 24 of 28 list-shaped
commands, 15 wired here, 9 owned by F267): every list command —
<<<END CONTEXT_TO>>>

Extraction rule for F267FILE and F262APPEND: the slice is every byte
after the BEGIN marker's newline up to and including the newline that
precedes the END marker line - the whole file (F267FILE) or the whole
appended region (F262APPEND), final newline included. For every other slice the slice is the bytes between the BEGIN
marker's newline and the newline before the END marker, EXCLUDING that
final newline.

Handback: write .agent/handoff.md per docs/agents/handback_template.md
and AGENTS.md - Session line `SESSION 9 of feature F262 · round 24 ·
rounds so far 24` with one sentence of context self-assessment, Range
`Review of 6991059c..<C4>`, one changed-files table per commit
(C0a..C4, C5 grouped per the self-reference exception), an item-status
table over C0a..C5 and G1..G8, External actions (the push), raw
Verification per gate, Authored-text proofs, Deviations (every
re-expression and any departure from the commit order), and Next: "the
integration-gate round (docs/agents/integration_gate.md steps 1-5) at
merge-base 7c65d9cc; the reviewer issues the gate verdict at the round
after it". State plainly that the operator ruled Option B and that
F267 is now registered.
