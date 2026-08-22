── STEP CLOSURE 2 — F021 Live activity feed + now-card ────────────────
Goal:        Close F021: record the R40 verdict, rule R-0663 as a DECISION,
             then write the STATUS `[x]` line, the README capability sync and
             the closure candidates in ONE commit and open the pull request.
Bundle:      C0a save this block · C0b mirror it · C1 the plan · C2 the ledger
             (RECORD41 and DONE0663) · C3 the closure commit and the PR.
Change:      C0a `.agent/authored/f021-r41.md` (new) · C0b `.agent/last_block.md`
             · C1 `.agent/plan.md` · C2 `.agent/live_review.md` · C3
             `docs/roadmap/STATUS.md`, `README.md`, `.agent/candidates.md` and
             `.agent/handoff.md`. Nothing else. No file under `apps/`,
             `packages/`, `tests/` or `docs/` other than the one STATUS path.
Constraints:
 1. Every slice below is applied BYTE FOR BYTE. Never retype one, never
    rewrap it, never fix its spelling. Copy it out of the file named in G2.
 2. The commit order is exactly C0a, C0b, C1, C2, C3 — none extra, none
    dropped, none reordered. C1 precedes C2 because this round writes the
    finding ledger (`planner_reviewer_prompt.md` §3 item 23).
 3. This is the LAST round of this branch. Its own verdict has no on-disk
    gate entry by construction (§4 item 13); it lives in `.agent/handoff.md`
    and in the pull request. Do NOT open a repair round to close that gap.
 4. NO finding id is minted this round and NOTHING but R-0663 is resolved.
    Closure-round observations are CANDIDATES without ids
    (`docs/roadmap/STATUS_closure_protocol.md`, "Closure-candidate findings"),
    and the CANDIDATES slice is the carrier of record.
 5. The pull request is created and NOT merged. No `gh pr merge` this
    session, no force push, no history rewrite, no branch deletion.
 6. The gates C3's paths are subject to run on the WORKING TREE after the
    edits are applied and BEFORE `git commit` — C3 also writes the handback
    that must quote them (§3 item 31). G8 orders the proof that the bytes
    gated are the bytes committed.
 7. `npm run lint` and `npx tsc` are NOT run and are NOT gates: both are red
    at base (R-0622, R-0364). No formatter and no linter runs this round.
 8. Two pytest processes never run at once. Every suite runs SERIALLY in the
    primary checkout. No worktree is created or removed this round.
 9. Slice sizes: report the numbers YOU measure. This block states no count
    of its own slices or of its marker lines.
Done when:
 G1 `.agent/STOP` is ABSENT — read from disk before C0a and again before C3 —
    and the branch is `feature/f021-live-activity-feed` at both. Report
    `git status --porcelain` as a LINE COUNT after each of C0a, C0b, C1 and C2;
    it must be 0 each time. Resolve the ROUND BASE with
    `git rev-parse 4db0a2e4` and report the full 40 characters.
 G2 TRANSPORT. This block lives at `.remedy-wt/f021-r41.md` with the sha256,
    byte count and line count the handoff of this round reports; recompute all
    three from that file before using it. C0a copies that file to
    `.agent/authored/f021-r41.md`; report the sha256 of the COMMITTED blob and
    of `.agent/last_block.md` at C0b, and all three readings must be EQUAL.
    C0b is written FROM the committed C0a blob, never from the scratch file.
 G3 EXTRACTION. Extract every slice from the COMMITTED C0a blob by its marker
    line — never from this prompt. Report, per slice, its name, sha256, byte
    count and line count, and report how many marker lines you matched. Report
    the summed slice CONTENT lines, the block TOTAL, and TOTAL minus CONTENT as
    PROSE. TOTAL must be at most 490 (DECISION F085 D6) and PROSE at most 400
    (DECISION F085 D5, under which a marker line is prose because it is not a
    slice).
 G4 THE PLAN. `.agent/plan.md` at C1 is byte-equal to the PLANF021R41 slice
    plus ONE terminating newline. Prove it with a comparison that prints its
    own result, and run the NEGATIVE CONTROL against the bare slice with no
    added newline, which must NOT compare equal. Report the byte count, the
    last byte in hex, `wc -l`, and the line-anchored counts of `^## Goal$` and
    `^## Next Steps$`, which are 1 each. `wc -l` must be under AGENTS.md's 50.
 G5 THE APPEND at C2 adds RECORD41 and DONE0663 to `.agent/live_review.md` and
    edits NOTHING already in it. Prove it under TWO readers, both of which must
    ACCEPT the true file: (a) the `4db0a2e4` blob is a byte-exact PREFIX of the
    C2 blob and the remainder is EXACTLY one newline, then RECORD41, then one
    newline, then one newline, then DONE0663, then one newline — report the
    remainder's byte count; (b) split the C2 blob on blank lines with YOUR OWN
    script, report the number of units it found, and show that the last two
    units equal RECORD41 and DONE0663 in that order. NEGATIVE CONTROL,
    required: flip the FIRST byte of the appended RECORD41 paragraph to a
    different character at UNCHANGED file length and report that reader (a) AND
    reader (b) both REJECT it. Report the first 20 bytes of the first appended
    paragraph.
 G6 THE SETS, at the ROUND BASE and again at C2, every count line-anchored and
    both readings reported: canonical `^- R-\d+ — `, which is 228 at the base
    and must stay 228 because this round mints nothing; loose `^- R-`, 229 at
    the base; `^Done: R-`, 1 at the base and 2 at C2; `^Done: R-0663 — `, 0 at
    the base and 1 at C2; `^Landed: `, 0 at both; `^Gate: R`, 39 at the base;
    `^Gate: R41`, 0 at the base and 1 at C2; `^Recurrence: `, 16 at both.
    Report the ids as ALL DISTINCT and the maximum as R-0665 at BOTH points.
    Report OPEN as canonical minus `^Done: R-`: 227 at the base, 226 at C2.
 G7 THE CLOSURE EDITS at C3. Apply the STATUSLINE slice as the whole
    replacement of the single line `- [~] F021 — Live activity feed + "agent is
    doing now"` in `docs/roadmap/STATUS.md`, and the three README pairs below,
    each FROM replaced by its matching TO in `README.md`. Before each
    replacement, COUNT the FROM string in its target file and report the count,
    which must be 1 for each of the four. After the edits, report the
    line-anchored count of `^- \[~\] F\d+ — ` in `docs/roadmap/STATUS.md`,
    which must be 0, and of `^- \[x\] F\d+ — `, which must be 56.
 G8 THE GATES ON THE EDITED TREE, all four run from the repository root BEFORE
    `git commit` for C3, each under a wrapper that captures the REAL exit code
    and never through a pipe. Report command, REAL exit code and the final
    summary line of each: `python3 -m pytest tests/docs/ -q -rf`, which reads
    295 passed at the base; `python3 -m pytest
    tests/orchestration/test_roadmap_index.py -q -rf`, 30 at the base;
    `python3 -m pytest tests/ui_server/
    tests/orchestration/test_test_runner.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_integrity_gate.py -q -rf`, 528 at the base COUNTED
    BY PASSED PLUS SKIPPED; and the canary `python3 -m pytest
    tests/cli/test_golden_path.py -q -rf`, 42 at the base. Every one must exit
    0. THEN, after C3 exists, report the sha256 of `docs/roadmap/STATUS.md` and
    of `README.md` as you gated them and again from `git show C3:<path>`, and
    the two must be EQUAL per path — that is what makes the pre-commit reading
    a reading of the committed bytes.
 G9 STRUCTURE. Report `git diff --name-only <ROUND BASE>..HEAD` at C2 and again
    at C3, and both set differences against the `Change:` list, which must be
    EMPTY at both. Report the commit count before C3, each commit's parent
    count, which is 1, and each commit's insertions from `git diff --numstat`,
    each under 500; C3's own numbers cannot exist inside the file C3 writes and
    are left to the next session (§3 item 31). Report the line-anchored counts
    of `^<<<SLICE ` and `^<<<END ` over `.agent/plan.md`,
    `.agent/live_review.md`, `docs/roadmap/STATUS.md`, `README.md` and
    `.agent/candidates.md`, which are 0 for each file and each prefix. Report
    `git ls-files .remedy-wt` as a line count, which is 0, and
    `git worktree list` as a line count, which is 1. Report the reflog rows of
    THIS round BY OPERATION: every one must read `commit`, with 0 each for
    `amend`, `rebase` and `cherry` in that field.
 G10 THE PULL REQUEST, after C3 is pushed. Run `gh pr list --state open --json
    number,headRefName,baseRefName,isDraft` FIRST and report its output
    verbatim; it must be `[]`. Then `gh pr create --base main --head
    feature/f021-live-activity-feed` with a title naming F021 and a body
    carrying what changed, why, the key decisions including the R-0663 ruling,
    how to review, the changed-files table, the latest verdict, the
    open-findings count of 226 and the runtime actuals you can observe. The
    title and the body contain NO leading-slash token and NO absolute path
    (AGENTS.md Commit Discipline). Report the PR number and its URL. Do NOT
    merge it. Re-run the list command afterwards and report its output.
 G11 THE HANDBACK carries every mandated section of
    `docs/agents/handback_template.md`, a row per `Bundle:` item, the round
    base SHA, ONE LINE PER GATE with the transcripts left out of this file,
    both points of every two-point reading, a `## Closure values` table, and
    the `Fortschritt:` block below VERBATIM. Its `+/-` cells are the
    `git diff --numstat` readings and are compared cell by cell against the
    numbers G9 reports (§3 item 28). Declare its line count under DECISION D15
    if it exceeds the tier.
Handback:    completion report + rewrite `.agent/handoff.md` inside C3.
Fortschritt: ~100 % (T001, T002 und T003 gebaut und verifiziert ·
             Integrations-Gate BESTANDEN · Evidence-Job und Review-Zip gebaut ·
             STATUS-Zeile, README-Sync und Pull Request in dieser Runde —
             danach ist F021 fertig) — Schaetzung
──────────────────────────────────────────────────────────────────────

The slices follow. Each begins with a `<<<SLICE <name>` line and ends with a
`<<<END <name>` line; neither marker line is part of the slice, and no slice
includes a terminating newline unless a gate above says it does.

<<<SLICE PLANF021R41
# Plan — F021 Live activity feed + now-card

Branch: feature/f021-live-activity-feed, cut from `main` at `4548995d`, the merge
commit of pull request #210. `.agent/live_review.md` is the source of truth for
the open set, the round map and the finding-id ceiling.

## Goal
The raw SSE event stream becomes a story a human can follow: a humanization
catalog maps event kinds to plain lines, a NowCard shows the newest ACTION-class
event with a recency dot, and feed rows carry their seq and click-jump to their
node. DONE when the catalog covers the kind set DECISION F021 D3 rules and an
unknown kind renders an honest generic line rather than vanishing, the feed
renders fixture streams per the binding CSS, jump-to-node focuses the right
node, and the steering input renders DISABLED with its tooltip until F030.

## Current Step
R41 is closure round two and the LAST round of this branch. It records the R40
verdict, rules R-0663 by DECISION rather than by a patch, then writes the STATUS
`[x]` line, the README capability sync and the closure candidates in ONE commit
and opens the pull request. That request is NOT merged in this session.

## Next Steps
1. The pull request merges at the next feature's start via the Open PR Gate,
   which is the operator's manual-review window.
2. The next session's FIRST reviewed round registers every entry
   `.agent/candidates.md` carries, or resolves it as a DECISION, and empties
   that file in the same round.

## Risks
- This round's own verdict has no on-disk gate entry by construction
  (`docs/agents/planner_reviewer_prompt.md` §4 item 13). It lives in
  `.agent/handoff.md` and in the pull request, and that absence is the branch
  terminator rather than a missing gate.
- The two High findings open at closure, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks rather than F021
  defects. That is why the verdict is PASS_WITH_RISKS, exactly as F008 and F009
  closed before it.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
<<<END PLANF021R41

<<<SLICE RECORD41
Gate: R41 — the R40 entry. R40 PASSED ON EVERY GATE, EACH ONE RE-MEASURED BY THE REVIEWER FROM THE COMMITTED BLOBS AND BY RE-RUNNING THE SUITES AND RE-DERIVING THE DIGESTS ITSELF RATHER THAN READING THE HANDBACK BACK. TRANSPORT HELD at sha256 `458138df2c127076752cf655d7f55015f5b4f1869fe4b131650cb1456df667be` over 29048 bytes and 420 lines, EQUAL across `.agent/authored/f021-r40.md` at `f9a649fd` and `.agent/last_block.md` at `9f5eb4d8`, and the reviewer's own extractor read the three whole texts out of the committed C0a blob by marker line and re-derived every digest: PLANF021R40 `d42548a7a582edd27e6fa0065f59c63a897505c86392bab473a358953dc116d7` 2208 bytes 39 lines, RECORD40 `c75bfbb73202062440a246376eb29b5118b5d3e598a3f6ac04d04b5dba0df62e` 4466 bytes 1 line, EVIDENCESCRIPT `369a3cc57e33bd51a47997dcd004df3260e2fad4668a53b67e9ff1643c3b70ca` 5712 bytes 139 lines, all three EQUAL to the block's own readings. THE SIZE ARITHMETIC IS CONFIRMED WITH ITS CONVENTION STATED: summed slice CONTENT 179 against TOTAL 420, so PROSE is 241 against DECISION F085 D5's 400 and TOTAL is 420 against DECISION F085 D6's 490; the reviewer's first extraction read PROSE 235 because it excluded the marker lines, and 241 is the reading D5 rules, because D5 lifts the cap off the SLICES a block transports and a marker line is not a slice. THE PLAN WRITE HELD: `.agent/plan.md` at `b268188f` is byte-equal to PLANF021R40 plus one terminating newline and NOT to the bare slice, 2209 bytes with last byte `0x0a`, `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 39 under AGENTS.md's 50, and unchanged again at `4db0a2e4`. THE APPEND HELD UNDER BOTH READERS: at `a0a883f7` the `68df0d89` blob is a byte-exact PREFIX and the remainder is EXACTLY one newline plus RECORD40 plus one newline over 4468 bytes; the reviewer's own blank-line split reads the last unit as RECORD40 exactly; the first appended paragraph opens with the bytes `Gate: R40 — the R39 en`; and the NEGATIVE CONTROL, flipping that paragraph's first byte at unchanged file length, is REJECTED by reader (a) AND by reader (b), so neither reader is vacuous. THE SETS DID NOT MOVE, base then C2: canonical `^- R-\d+ — ` 228 then 228, ALL DISTINCT at both, maximum R-0665 at both, so the round minted nothing and the next free id is R-0666; loose `^- R-` 229 then 229; `^Done: R-` 1 then 1; `^Landed: ` 0 then 0; `^Gate: R` 38 then 39, DISTINCT at both; `^Gate: R40` 0 then 1; `^Recurrence: ` 16 then 16; OPEN 227 at both, and by severity that open set is 156 Low, 69 Medium and 2 High, the two Highs being R-0495 and R-0574, both inherited from the already-closed F085 and F086. STRUCTURE: five commits over `68df0d89..4db0a2e4`, every one single-parent, `git show --numstat` and `git diff --numstat` agreeing cell by cell, insertions 420, 377, 19, 2 and 95, each under 500; four paths at `a0a883f7` and five at `4db0a2e4`, both set differences against that block's `Change:` list EMPTY at both points, and `docs/roadmap/STATUS.md` and `README.md` ABSENT from both; the marker sweep 0 for each of `^<<<SLICE ` and `^<<<END ` over `.agent/plan.md` and `.agent/live_review.md`; `git ls-files .remedy-wt` 0; `git worktree list` one entry; every reflog row of the round carrying `commit` in its operation field with no amend, rebase or cherry-pick among them; `gh pr list --state open` printing `[]`. THE CANARY IS THE REVIEWER'S OWN, serial and in the primary checkout: `python3 -m pytest tests/cli/test_golden_path.py -q -rf` REAL exit 0 at `42 passed`, equal to the block's base reading. THE THREE CLOSURE ARTEFACTS WERE RE-OPENED RATHER THAN READ BACK. The evidence bundle at `.remedy-wt/f021_closure_evidence/remedy-job-evidence-f021-closure` holds 27 entries; the reviewer re-derived each verification run's `output_hash` as the sha256 of its own `stdout_summary` on disk and all four MATCH, each run's `test_files` is SORTED, each run's `selected` EQUALS its `len(node_ids)` at 9, 67, 66 and 51 with 0 deselected, no node id contains a parent-directory segment, and `verification_tests.json` reads exit 0 at 193 passed and 0 failed; `final_verifier_report.json` reads verdict `PASS_WITH_RISKS` with `manual_completion` true over `operator_attested_tasks` T001, T002 and T003. The INTEGRITY CHECK re-run by the reviewer through `run_integrity_checks()` reads `passed` true and `fail_count` 0 over five checks — handler_import, live_review_verdict, plan_consistency, relevant_untracked and high_blockers_open — the last of which is blind for the already-registered reason R-0648 names. THE ZIP: a fresh sha256 over `remedy-review-20260823-005026-READY_FOR_REVIEW.zip` on disk RECOMPUTES `be70b65dd4a397ac7697a3c37b2f5cfb1a52197c9434cde67dec4a0a502e3dd8` over 79906347 bytes, `zipfile.namelist()` reads 13921 members, and the manifest INSIDE the package reads `base_commit` `4548995de3e46dc5304d3584dc249262d54edac9` at full length, `head_commit` `a0a883f7bf47e92bd3c084d127bf56f5f4feaad2` which EQUALS C2, `base_is_ancestor` true, `commit_count` 248, `file_count` 99, `packaged_evidence_job_id` `f021-closure`, `ready_gate_matrix.ok` true over an empty `blocking_reasons`, and `review_subject_evidence_alignment.verdict` `PASS` with 0 issues and 0 hash mismatches. OWED TO THIS ENTRY BECAUSE C3 COULD NOT STATE THEM ABOUT ITSELF: C3's SHA is `4db0a2e4`, its insertion count is 95, and `git status --porcelain` printed 0 lines at it. ALL SIX OF R40'S DECLARED DEVIATIONS ARE ACCEPTED, including its newline convention, its reader (b) definition and its 139-line size under DECISION D15. ONE CORRECTION, carried with NO id spent because a closure round mints none: R40's deviation 4(b) located the commit-execution verdict at a package-manifest key `gate_verdicts.commit_execution_gate`, and the manifest carries no `gate_verdicts` key at all, so that address does not resolve; the VALUE it reports is real and the reviewer confirmed it at two other addresses — `commit_execution_gate.json` in the evidence bundle and the `commit_execution_gate` field of `final_verifier_report.json` both read `NEEDS_HUMAN_APPROVAL`, beside `human_final_reviewer_required` true — so the observation stands on its substance and only its pointer was wrong. It is carried into `.agent/candidates.md` by this round with the address corrected, which is where a closure-round observation belongs.
<<<END RECORD41

<<<SLICE DONE0663
Done: R-0663 — RESOLVED BY DECISION AT F021'S CLOSURE, and deliberately not by a patch. The finding's own fix clause offered exactly two routes and forbade taking both or neither: rule that the CSS-module realization satisfies the acceptance clause, or order the one-line `gap` repair in its own reviewer-gated round. CHOSEN: THE REALIZATION SATISFIES THE CLAUSE. THE REASON IS THE RESTRUCTURING THE FINDING ITSELF MEASURED. `docs/roadmap/features/T5_F021.md`'s Design section fixes the row as `.feed-row{display:flex;gap:10px;padding:9px 14px;font:500 13px/1.45 var(--remedy-font-ui);color:var(--remedy-ink)}`, and the shipped rule is `.activityItem` in `apps/ui/src/components/panels/RightLivePanel.module.css`, measured by the reviewer at `2428f021`. The selector name differs, the padding is not on that selector, and the `font:` shorthand is not on it either, because the row renders three distinct text roles rather than one and its typography lives on `.activityMeta strong`, `.activityItem p` and `.activityTag`. Once the shorthand and the padding are legitimately distributed, `gap` is the ONLY property of that snippet left that could be copied literally, and copying it alone would assert a literal conformance the rest of the rule does not have and was never intended to have — a false precision is worse than a measured two-pixel difference. The property the clause protects is a flex row with one small uniform gutter and the design_reference typography scale, and that property holds on disk. ALTERNATIVE CONSIDERED AND REJECTED: the one-line repair to `gap: 10px`. It changes shipped UI on a closure branch for two pixels, it requires a further round carrying its own vitest and tsc gates, and it would leave the selector name, the padding and the shorthand restructured while making one property literal. THE DEVIATION IS DOCUMENTED HERE BECAUSE HERE IS THE ONLY CARRIER THAT EXISTS: the feature file's header routes any visual deviation to an `assumption_log`, and R-0665 measured that NO tracked path in this repository carries that string in its name, so this ledger entry is the record and R-0665 owns the repair of the route. HOW TO REVERSE: set `gap` to `10px` on `.activityItem` in that file and delete this paragraph; the finding then returns to OPEN with its two routes intact. Recorded as an operator-visible DECISION under `docs/agents/planner_reviewer_prompt.md` §4 item 7 — loud, persisted and reversible by any later relay, and never a question to the operator. R-0664 and R-0665 are NOT resolved by this ruling and stay OPEN as documented Low risks, R-0664's fix belonging to `tests/ui_contracts/test_brain_stream_ring.py` and R-0665's to a repository-wide paydown branch.
<<<END DONE0663

<<<SLICE STATUSLINE
- [x] F021 — Live activity feed + "agent is doing now" (T001–T003 complete; accepted 2026-08-23 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f021-closure · package remedy-review-20260823-005026-READY_FOR_REVIEW.zip · SHA-256 be70b65dd4a397ac7697a3c37b2f5cfb1a52197c9434cde67dec4a0a502e3dd8 · accepted HEAD a0a883f7bf47e92bd3c084d127bf56f5f4feaad2)
<<<END STATUSLINE

<<<SLICE READMEFROM1
55 of 255 registered items accepted. Next: F021 (Live activity feed + "agent is doing now").
<<<END READMEFROM1

<<<SLICE READMETO1
56 of 255 registered items accepted. Next: F022 (Live cost ticker).
<<<END READMETO1

<<<SLICE READMEFROM2
| 5 | Operator Cockpit | 3 | 29 |
<<<END READMEFROM2

<<<SLICE READMETO2
| 5 | Operator Cockpit | 4 | 29 |
<<<END READMETO2

<<<SLICE READMEFROM3
F009 the single write channel (one authenticated, CSRF-guarded, rate-limited
and nonce-idempotent POST endpoint for UI-initiated commands, every other
mutating route answering 405 under a route-walking test).
<<<END READMEFROM3

<<<SLICE READMETO3
F009 the single write channel (one authenticated, CSRF-guarded, rate-limited
and nonce-idempotent POST endpoint for UI-initiated commands, every other
mutating route answering 405 under a route-walking test).
F021 live activity feed and now-card (a humanization catalog that turns every
Part E event kind into a plain line with an honest generic fallback for an
unknown kind, a NowCard over the ACTION-class subset with a recency dot, and
feed rows that carry their seq and focus their node on click).
<<<END READMETO3

<<<SLICE CANDIDATES
# Closure Candidates — carrier of record

> Written per docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate
> findings", disk-vehicle rule, operator ruling 2026-08-01). Read at Window-1
> session bootstrap (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present at
> feature-claim time is a block condition.

NON-EMPTY. Three candidates, raised by the reviewer during the F021 closure
review and recorded here without ids because the closure protocol reserves ids
for the next session's first reviewed round. Each was MEASURED by the reviewer
at `4db0a2e4`, not read back out of a handback.

- AN ALIGNMENT SUMMARY REPORTS ONE DIRTY FILE WHILE EVERY LIST IT SUMMARIZES IS
  EMPTY · F021 R40 · 2026-08-23. In the manifest inside
  `remedy-review-20260823-005026-READY_FOR_REVIEW.zip`,
  `review_subject_evidence_alignment.dirty_file_count_total` reads 1 while
  `dirty_source_test_files` and `uncovered_source_test_files` are both empty,
  `issues` is empty and the verdict is `PASS`. The package was built from a tree
  whose `git status --porcelain` printed 0 lines, so either that count has a
  source none of the lists expose or it is stale. Nothing about this closure is
  unsound because of it — the verdict rests on the empty lists and the PASS —
  but a non-zero count beside three empty collections is the kind of number a
  later reader will either trust or panic about, and neither is justified today.
  Candidate counter-measure: find the producer of that field, and either make it
  name the file it counted or derive it from the lists it sits beside.

- TWO GATES IN ONE PACKAGE DISAGREE ABOUT WHETHER A HUMAN MUST STILL APPROVE ·
  F021 R40 · 2026-08-23. `commit_execution_gate.json` in the evidence bundle and
  the `commit_execution_gate` field of `final_verifier_report.json` both read
  `NEEDS_HUMAN_APPROVAL`, and `human_final_reviewer_required` is true, while the
  same package's `ready_gate_matrix.ok` is true over an empty
  `blocking_reasons` and `PACKAGE_STATUS` is `READY_FOR_REVIEW`. Both readings
  are defensible on their own terms and the closure protocol treats the ready
  gate as the blocker, so nothing here blocked F021; the cost is that a reader
  cannot tell from the package alone which authority governs. NOTE ON ITS
  ADDRESS, because the R40 handback got this wrong and the correction belongs
  with the candidate: that handback located the verdict at a manifest key
  `gate_verdicts.commit_execution_gate`, and the package manifest carries no
  `gate_verdicts` key at all — the two addresses above are where the value
  really lives. Candidate counter-measure: have the packager either surface the
  commit-execution verdict in the manifest beside the ready gate, or record why
  the ready gate supersedes it.

- EVERY CLOSURE BUNDLE ON THIS MACHINE CARRIES A ZERO-BYTE `job_report.json` ·
  F021 R40 · 2026-08-23. The reviewer measured all thirteen
  `remedy-job-evidence-*` directories under `.remedy-wt/` and `job_report.json`
  is 0 bytes in every one of them, F021's included. The producer emits the file
  and writes nothing into it, inside a bundle whose entire purpose is evidence,
  and no gate notices because nothing reads it. This is not an F021 defect and
  it blocked nothing — the substance lives in `final_verifier_report.json`,
  `verification_tests.json` and `review_subject.json`, all of which the reviewer
  read and re-derived — but an always-empty evidence artifact is either a
  producer bug or a file that should not be emitted. Candidate counter-measure:
  decide which, and either populate it or stop writing it.

NOT A CANDIDATE, recorded so the next round does not mint an id for it
(`docs/agents/planner_reviewer_prompt.md` §3 item 30): 10646 of the package's
13921 members are `.remedy-wt/` scratch. That is the already-registered R-0403,
which routes to a paydown branch, and it is unchanged rather than new.
<<<END CANDIDATES
