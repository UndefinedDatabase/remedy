── STEP R21 — F255 Teacher role · CLOSURE ──────────────────────
Goal:        CLOSE F255. R20 PASSED and built both artifacts: the evidence bundle
             and a READY_FOR_REVIEW package the reviewer re-hashed off disk. This
             round records that verdict, then writes the STATUS `[x]` line, syncs
             the README in the SAME commit, empties the closure-candidate carrier,
             and opens the pull request. The PR is NOT merged in this session: it
             merges at the NEXT feature's Open PR Gate, which is the operator's
             manual-review window.

Bundle:      C0a save this block · C0b mirror it · C1 the plan, FIRST · C2 record
             the R20 verdict · C3 THE CLOSURE COMMIT — STATUS, README and the
             candidate carrier together · then the pull request · C4 the handback,
             then push.

Change:      Exactly these paths, in this order.
             C0a `.agent/authored/f255-r21.md`
             C0b `.agent/last_block.md`
             C1  `.agent/plan.md`
             C2  `.agent/live_review.md`
             C3  `docs/roadmap/STATUS.md`, `README.md` and
                 `.agent/candidates.md` — ONE commit, never three
             C4  `.agent/handoff.md`
             Nothing else is created, modified, deleted or staged. NO source file
             and NO test file is touched. These paths are PRESENT at the base
             `a4f0fafd` and must stay untouched:
             `docs/roadmap/features/T5_F255.md`, `.agent/decisions.md`,
             `packages/orchestration/teacher_model.py`,
             `apps/cli/commands/teach_cmd.py`.

             WHY STATUS AND README SHARE ONE COMMIT (R-0154): the README's
             accepted COUNT and its tier-table Done column are both pinned to the
             STATUS ledger by `tests/docs/test_docs_consistency.py`, so any
             committed state in which one has moved and the other has not is RED.
             They may never disagree in any committed state, which a two-commit
             split cannot honour. `.agent/candidates.md` joins them because
             `.agent/**` is already inside the R-0154 path set and the carrier is
             read at the NEXT feature's bootstrap.

             WHY THE HANDBACK IS ITS OWN COMMIT AFTER THE PR. Rule A4 makes the
             STATUS edit the last CONTENT commit, and DECISION F085 D9 rules that
             A4 does not seal the branch: a verdict or a record that lives only in
             a chat window is one this project cannot audit. The pull request is
             created AFTER C3 and its number is a value C3 cannot contain, so the
             handback that must record it is written after it exists.

             THE VALUES IN THE STATUS LINE ARE R20'S, RE-MEASURED BY THE REVIEWER
             AT `a4f0fafd` RATHER THAN COPIED FROM THE HANDBACK: the package
             `remedy-review-20260821-051015-READY_FOR_REVIEW.zip` hashes to
             f142a9935d2730c01a80d98a619d2b297899c144f29ad16fd5c01aa1f493fcc2 over
             60194458 bytes with `zipfile.testzip()` returning None and 10646
             members; its own `.review_zip_manifest.json` reads
             `package_status` READY_FOR_REVIEW with `committed_review_subject`
             base b35d350b84b1d371064a1f44e43f40da3ccfa540 and head
             c96f82c3372520bfd0545c7ce640886479197a08, and that head is the commit
             R20's C3 created. The evidence bundle holds 27 entries and its
             `final_verifier_report.json` reads verdict PASS_WITH_RISKS.

             THE PULL REQUEST, after C3 and before C4. Title:
             `F255 — Teacher role (Tier 5)`. The description carries what changed
             and why, the four DECISIONs D7 through D10, how to review, a
             changed-files summary, the latest verdict, the open-findings count
             and the runtime actuals below. DO NOT MERGE IT and do not enable
             auto-merge. Report the PR number and URL.
             RUNTIME ACTUALS, observed only — `not-measured` beats a guess:
             rounds R1 through R21 on this branch; 21 rounds, of which this
             session drove R16 through R21; models and token cost `not-measured`,
             because no ledger row covers the reviewer's or the worker's own
             session; the full suite runs `17315 passed, 20 skipped` in about
             145 s with `-n auto`.

Constraints:
1. NO SLICE IS EDITED. Every text between the SLICE and END markers is applied
   byte for byte, and every FROM is matched EXACTLY once in its target file
   before its TO replaces it. A slice you believe is wrong is applied anyway and
   DECLARED. Marker lines never reach a target file.
2. TRANSPORT. `.remedy-wt/f255-r21.md` is this block on disk. C0a copies that
   FILE to `.agent/authored/f255-r21.md` and C0b copies the same file to
   `.agent/last_block.md`. Prove all three byte-EQUAL.
3. THE PLAN COMES FIRST (R-0377, R-0491, R-0548). Only C0a and C0b precede it.
4. THIS ROUND REGISTERS NO FINDING AND RESOLVES NONE: registered stays 187,
   resolved stays 4, open stays 183. RECORDR20 is a `Gate:` paragraph and adds
   neither kind of line.
5. RECORDR20 IS SINGLE-PARAGRAPH — the reviewer measured it for an interior blank
   line and found none — and is appended preceded by exactly one blank line
   (R-0578), so the LAST-UNIT paragraph reading is exact for it.
6. THE FOUR PAIRS ARE ALL REWRITES, and the reviewer measured each mechanically
   rather than by eye (checklist item 15). For every pair, `TO contains FROM:
   false`, so each owes the REWRITE proof — FROM 0x and TO 1x in the target after
   the edit — and none owes an append reading. Each FROM occurs EXACTLY 1x in its
   target at `a4f0fafd`, measured by the reviewer.
7. YOU NEVER WRITE A `Done:` OR A `Landed:` PARAGRAPH.
8. `.agent/STOP` is read from disk before C0a. If it exists, stop and write the
   handback instead.
9. `git status --porcelain` is EMPTY after every commit and at the handback. No
   git worktree is created. The zip and the evidence dir are NOT committed and
   NOT deleted.
10. YOU DO NOT MERGE THE PULL REQUEST, you do not enable auto-merge, and you do
    not wait on the CI run the push starts. If `gh` cannot create the PR, report
    the raw error, write the handback and end — the branch is still closed on
    disk and the PR is the only thing missing.

<<<SLICE PLAN255R21
# Plan — F255 Teacher role

Branch: feature/f255-teacher-role, cut from `main` at b35d350b, the merge commit
of pull request #207. The closure pull request is created by THIS round and is
NOT merged in this session; it merges at the next feature's Open PR Gate.
`.agent/live_review.md` is the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

## Goal
A fourth configured role, `teacher`, that narrates a running mission and answers
operator questions about the operator's own code, and never influences the run.
DONE when passive narration keyed to an enumerated set of ledger events (Stage 1,
deterministic templates, zero tokens) and on-demand Q&A (Stage 2, through the
teacher role's own model) both work, the three grounding sources are never mixed
silently, teacher spend is reported as its own role in the F103 ledger, and the
read-only invariant is proven behaviourally. ALL FOUR HOLD and are reviewed.

## Current Step
R21 CLOSES F255. It records the R20 verdict, writes the STATUS `[x]` line with
the package and `accepted HEAD` values R20 produced, syncs the README count, tier
table and accepted list in the SAME commit, empties the closure-candidate
carrier, and opens the pull request.

## Next Steps
1. The next session's FIRST action is Phase 1 rule 1, the `.agent/STOP` re-read,
   and its SECOND is the Open PR Gate, which merges this feature's pull request
   before any new branch is cut. Rule A5 then selects F008 — SSE event stream —
   as the next feature, it being the first `[ ]` in STATUS order.

## Risks
- FOUR FINDINGS REMAIN OPEN and none is a code defect: R-0607, R-0608, R-0609 and
  R-0611 are all reviewer-process defects whose fixes edit `docs/agents/` or the
  closure protocol, paths the closure commit's own R-0154 path set cannot reach.
  They route to a paydown branch and are named in the pull request.
- THE PACKAGE PACKAGES `.remedy-wt/` SCRATCH, which is the already-registered
  R-0403 and not a new condition of this closure.
<<<END PLAN255R21
<<<SLICE RECORDR20
Gate: R21 — the R20 entry. R20 PASSED and BOTH CLOSURE ARTIFACTS EXIST, which is what R19 could not deliver. NO finding is registered against it: the round did exactly what its block ordered and declared no deviation. THE PACKAGE IS REAL AND THE REVIEWER RE-MEASURED IT OFF DISK rather than reading the handback: `remedy-review-20260821-051015-READY_FOR_REVIEW.zip` is 60194458 bytes at sha256 f142a9935d2730c01a80d98a619d2b297899c144f29ad16fd5c01aa1f493fcc2 — the digest R20 reported — with `zipfile.testzip()` returning None and 10646 members, and its own `.review_zip_manifest.json` reading `package_status` READY_FOR_REVIEW over a `committed_review_subject` whose base is b35d350b84b1d371064a1f44e43f40da3ccfa540, whose head is c96f82c3372520bfd0545c7ce640886479197a08 — the commit R20's C3 created — with `base_is_ancestor` true across 136 commits and 61 files. THE EVIDENCE BUNDLE IS COMPLETE: 27 entries under `.remedy-wt/f255_closure_evidence/remedy-job-evidence-f255-closure`, `final_verifier_report.json` reading verdict PASS_WITH_RISKS, the summary dict reading the same with 141 total passed across three attested tasks, and the string `READY` appearing NOWHERE in that report — which is correct, `READY_FOR_REVIEW` being the zip's vocabulary and not the bundle's (R-0597), and the block having asked what the artifacts SAY rather than asserting a value. THE REPAIR WORKED FOR THE REASON IT WAS DESIGNED TO: EVIDENCESCRIPT2 took node ids from `--collect-only -q` listings instead of parsing `-v` output, and the vr0002 listing carried the space-bearing id `tests/orchestration/test_teacher_qa.py::TestGroundingSourcesAreLabelled::test_no_code_fact_without_real_code` with its parametrised suffix intact — the exact id that truncated R19's extractor and produced R-0611. All six records built with `len(node_ids) == selected`: 18, 19, 5, 38, 19 and 42, each equal to its suite's passed count, 0 failed and 0 skipped throughout, every capture serial. THE ROUND'S OWN SHAPE HOLDS, re-measured by the reviewer: transport byte-equal at the delegated digest sha256 6d54e410b577e638a7a8a24acce0ace50b5213336775702857501b7ff9eda25e over 31253 B and 401 lines; FOUR slices; `.agent/plan.md` at `eaffcc07` byte-equal to PLAN255R20 at 43 lines under the cap; FIND0611 appended at `ec6dbcb8` and RECORDR19 at `c96f82c3`, each a byte-exact prefix-plus-remainder preceded by exactly one blank line, the finding landing BEFORE the verdict as §4.4 requires; sets 186 / 4 / 182 / 0 at `b42cab39` becoming 187 / 4 / 183 / 0 at both later commits, `R-0611` occurring 0x at the base and exactly 1x as a registered line; twenty `Gate: R` headers, all distinct, `Gate: R20 — the R19 entry.` last; six single-parent commits with insertions 401, 230, 18, 2, 2 and 80, every one under the 500 cap; the change set exactly the block's five paths with NEITHER `docs/roadmap/STATUS.md` NOR `README.md` among them, which is what a round that must not close early owes; zero marker leaks; the integrity gate passing with fail_count 0 over five checks and `high_blockers_open` reading "no open blocker/high findings"; the canary and the state-reader four exit 0 at 42 and 160 passed; the tree clean, the branch pushed and `gh pr list --state open` returning an empty list. TWO OBSERVATIONS THE WORKER RAISED AND THE REVIEWER CONFIRMS ARE NOT DEVIATIONS: the C0b cell reads 230/270 under plain `git diff --numstat` and 401/441 under break-rewrite detection, both under the cap and both stated; and the package contains `.remedy-wt/` scratch, which is the already-open R-0403 rather than a new condition of this closure. WHAT R20 PROVES ABOUT THE PROCESS is worth recording beside what it produced: R19 failed on a defect in the reviewer's own authored script, the worker refused all four available shortcuts and stopped, the reviewer registered R-0611 against itself and applied that finding's own counter-measure — dry-running the corrected script's assertions against real captured logs BEFORE emitting the block — and the repair then succeeded on its first attempt with no deviation. The cost of the whole episode was one round.
<<<END RECORDR20
<<<SLICE STATUSFROM
- [~] F255 — Teacher role (evidence-grounded live explainer & learn-along tutor)
<<<END STATUSFROM
<<<SLICE STATUSTO
- [x] F255 — Teacher role (evidence-grounded live explainer & learn-along tutor) (T001–T004 complete; accepted 2026-08-21 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f255-closure · package remedy-review-20260821-051015-READY_FOR_REVIEW.zip · SHA-256 f142a9935d2730c01a80d98a619d2b297899c144f29ad16fd5c01aa1f493fcc2 · accepted HEAD c96f82c3372520bfd0545c7ce640886479197a08)
<<<END STATUSTO
<<<SLICE COUNTFROM
52 of 255 registered items accepted. Next: F255 (Teacher role).
<<<END COUNTFROM
<<<SLICE COUNTTO
53 of 255 registered items accepted. Next: F008 (SSE event stream).
<<<END COUNTTO
<<<SLICE TIERFROM
| 5 | Operator Cockpit | 0 | 29 |
<<<END TIERFROM
<<<SLICE TIERTO
| 5 | Operator Cockpit | 1 | 29 |
<<<END TIERTO
<<<SLICE ACCEPTEDFROM
F086 release capability (wheel, `remedy --version`, release gate).

Full per-feature state:
<<<END ACCEPTEDFROM
<<<SLICE ACCEPTEDTO
F086 release capability (wheel, `remedy --version`, release gate).

Accepted in Tier 5 so far:
F255 teacher role (`remedy teach narrate`, `remedy teach ask`, teacher spend
reported as its own role in the token ledger).

Full per-feature state:
<<<END ACCEPTEDTO
<<<SLICE CANDIDATES
# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

The carrier is empty. F255's closure review produced NO candidate: every defect
this feature surfaced was registered as a numbered finding during the round that
found it, which is what the closure-candidate mechanism exists to avoid needing.
Four of those findings are OPEN at closure and none is a code defect — R-0607,
R-0608, R-0609 and R-0611 are all defects in the reviewer's own block text, and
their fixes edit `docs/agents/planner_reviewer_prompt.md` or
`docs/roadmap/STATUS_closure_protocol.md`, paths the closure commit's R-0154 path
set cannot reach. They route to a paydown branch and are named in the pull
request rather than carried here, because they are registered findings and not
candidates.
<<<END CANDIDATES

Done when:
G1 HYGIENE. `.agent/STOP` read from disk before C0a and reported absent or
   present; branch is feature/f255-teacher-role; `git status --porcelain` EMPTY
   after every commit and at the handback; `git worktree list` reports the
   primary checkout alone.
G2 TRANSPORT. Report the sha256 and the byte and line counts of
   `.remedy-wt/f255-r21.md`, of `.agent/authored/f255-r21.md` at C0a and of
   `.agent/last_block.md` at C0b, and state whether all three are EQUAL.
G3 SLICES EXTRACTED, NEVER RETYPED. Extract each slice from the COMMITTED
   `.agent/authored/f255-r21.md` by its markers; report each slice's name,
   sha256, byte count and line count, naming the newline convention (R-0600).
   Report the number of slices as a COUNT YOU TOOK FROM THAT LISTING (R-0604).
G4 THE PLAN, FIRST. `.agent/plan.md` at C1 byte-equals PLAN255R21; report its
   sha256, byte and line counts, that the line count is under 50, and that
   `## Goal`, `## Next Steps` and a roadmap F-id all occur in it. Report that C1
   is the FIRST commit other than C0a and C0b.
G5 THE R20 VERDICT RECORDED. Over `.agent/live_review.md`: the base blob at
   `a4f0fafd` is a byte-exact PREFIX of the C2 blob; the remainder's sha256, byte
   and line counts; that it equals one newline followed by RECORDR20; and that
   the byte after that leading newline is not a newline. Then a SECOND,
   INDEPENDENT blank-line paragraph split whose LAST unit is RECORDR20, with its
   sha256 under BOTH newline conventions. Re-measure constraint 5. Negative
   control: one character of the expected remainder mutated, rejected by BOTH
   readings.
G6 THE SETS AND THE KEYS. Report registered / resolved / open / line-anchored
   `Landed:` at `a4f0fafd` and at C2, registered being lines matching
   `^- R-\d+ — ` and resolved lines matching `^Done: R-\d+ — `: the reviewer
   measured 187 / 4 / 183 / 0 at `a4f0fafd`, and C2 owes the SAME four numbers.
   Report that `Gate: R21 — the R20 entry.` occurs 0x at `a4f0fafd` and 1x at C2,
   is the LAST line beginning `Gate: R`, and that every such header key is
   distinct, counted LINE-ANCHORED (R-0584).
G7 THE FOUR REWRITES, EACH PROVEN IN ITS TARGET AT C3. For each of the pairs
   STATUS, COUNT, TIER and ACCEPTED, report the FROM's occurrence count in its
   target at `a4f0fafd` — each must be exactly 1 — and, at C3, that the FROM
   occurs 0x and the TO occurs 1x. All four are REWRITES and none owes an append
   reading (constraint 6). Report also that `docs/roadmap/STATUS.md` at C3 holds
   exactly ONE line matching `^- \[x\] F255 — ` and ZERO matching `^- \[~\] F255`.
G8 THE LEDGER AND THE README AGREE, which is the pin a split commit would break.
   At C3 report: the count of lines matching `^- \[x\] F\d{3} — ` in
   `docs/roadmap/STATUS.md`; the N of the README's `N of 255 registered items
   accepted.`; and that the two are EQUAL. The reviewer measured 52 at
   `a4f0fafd`, so C3 owes 53 on both sides. Report the README Tier 5 row's Done
   cell and that it equals the number of accepted STATUS ids whose feature file
   carries the `T5_` prefix — the reviewer measured that as 0 before this round
   and 1 after.
G9 THE DOCS GATE, because this round's change set includes `docs/roadmap/**`.
   Serially in the PRIMARY checkout, after C3:
     `python3 -m pytest tests/docs/ -q -rf`
     `python3 -m pytest tests/orchestration/test_roadmap_index.py -q -rf`
   Report each command, exit code and tail. The reviewer measured exit 0 at 295
   passed and exit 0 at 30 passed at `a4f0fafd`; the F255 closure moves the
   accepted count, so `test_the_readme_accepted_count_equals_the_status_count`
   and `test_the_readme_tier_table_done_column_matches_the_ledger` are the two
   that would go red on a mismatch, and both must be GREEN.
G10 THE CANARY AND THE STATE READERS, UNCONDITIONALLY (R-0607's rule), serially,
   never two pytest processes at once:
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
   Report the exact command, exit code and tail of each. The reviewer measured
   exit 0 at 160 passed and exit 0 at 42 passed at `a4f0fafd`.
G11 THE PULL REQUEST. Report the exact `gh pr create` command, the PR NUMBER and
   its URL, and `gh pr view <n> --json state,mergeable,isDraft` showing it OPEN
   and NOT a draft. State that you did not merge it and did not enable
   auto-merge. If `gh` fails, report the raw error verbatim and end the round.
G12 CHANGE SET, HISTORY AND CAPS. Report `git diff --name-only a4f0fafd..<C3>`
   and state that it equals the Change list minus `.agent/handoff.md`, which C4
   itself adds, with no path on either side alone. Report that each path named
   untouched is PRESENT at the base and ABSENT from the range; that every commit
   has one parent; and each commit's insertion column from `git diff --numstat`
   for C0a through C3, every one under 500, with the same `+/-` cells appearing
   byte-identically in the handback's `## Commits` table. C4's own cell belongs
   to the round report (R-0149). Report that C3 is a SINGLE commit carrying all
   three of its paths — `git show --numstat <C3>` naming exactly
   `docs/roadmap/STATUS.md`, `README.md` and `.agent/candidates.md`.
   THE REFLOG IS TWO MEASURED CLAIMS (R-0601, R-0605): the count of this round's
   entries whose OPERATION PREFIX reads exactly `commit`, WITH the commit it was
   taken at and the number of commits made AT THAT MOMENT, stating the two are
   equal; no total (R-0494). The count whose prefix contains `amend`, `rebase` or
   `cherry` must be 0, and for EVERY `reset` entry report it with the
   demonstration that its destination is the commit the branch already pointed
   at (R-0608).
G13 NO MARKER LEAKED, AND THE PUSH. Report the count of LINES beginning with the
   SLICE or END marker prefixes in `.agent/plan.md` at C1, `.agent/live_review.md`
   at C2, `docs/roadmap/STATUS.md` and `README.md` and `.agent/candidates.md` at
   C3, and `.agent/handoff.md` at C4 — every count 0. `git push` after C3 and
   again after C4, reporting real output each time; the branch must be pushed
   BEFORE the pull request is created.

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             all seven mandated headings in the template's order, the item-status
             table for the C0a..C4 bundle, the `## Commits` table G12 pins, and
             one LINE per gate rather than its transcript (R-0582). Its
             `## External actions` section records the pull request WITH its
             number and URL, and states that it was NOT merged and that
             auto-merge was NOT enabled. Its `## Next` section names the next
             session's FIRST action as Phase 1 rule 1, the `.agent/STOP` re-read,
             and its SECOND as the OPEN PR GATE, which merges this feature's pull
             request before any new branch is cut; Rule A5 then selects F008, the
             first `[ ]` in STATUS order. It states that F255 is CLOSED with its
             STATUS line at C3, that R20 PASSED with its verdict ON DISK at C2,
             that R-0607, R-0608, R-0609 and R-0611 remain OPEN and route to a
             paydown branch, and that R21 IS THE LAST ROUND OF THIS BRANCH — so
             its own verdict has no on-disk gate entry BY CONSTRUCTION
             (planner_reviewer_prompt.md §4 item 13, the terminator), and lives in
             this handback and in the pull request rather than being a missing
             gate. The handback carries this Fortschritt line verbatim (R-0418):
             Fortschritt: 100 % (T001 through T004 COMPLETE and REVIEWED · the
             integration gate PASSED with 0 branch-only failures · evidence job
             and READY_FOR_REVIEW package built and re-verified · STATUS `[x]`,
             README sync and the pull request landed at this round · F255 CLOSED,
             the PR merges at the next feature's Open PR Gate) — Schätzung
──────────────────────────────────────────────────────────────
