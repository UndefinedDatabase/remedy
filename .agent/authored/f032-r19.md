STEP CLOSURE 2 OF 2 / F032 — ROUND R19 — the STATUS flip, the README sync, the PR

BASE. This block is authored against `eb243fcd393fa4411cbb6cf55c9e273629c690c0`,
the tip of `feature/f032-evidence-triple` and the handback of R18, measured with
`git rev-parse HEAD` in full rather than copied from a short form. Every reading
below was taken there by the reviewer unless another SHA is named.

FRAME CONVENTION. Every rule line in this block is exactly ten hyphens, and no
other line is a run of one repeated character. Nothing in the frame is
appliable: the appliable bytes are the slices and the FROM/TO pairs, each proved
against its own target by its own gate.

----------

GOAL

Close F032. Book the R18 verdict, flip the STATUS line to `[x]` and sync the
README's capability prose and its two ledger-derived counts in the SAME commit,
then open the pull request. The PR is NOT merged in this session — it merges at
the next feature's start via the Open PR Gate, which is the operator's manual
review window.

----------

WHAT THE REVIEWER READ AND MEASURED BEFORE ORDERING ANY OF THIS

(a) CLOSURE PRECONDITIONS, each checked against disk at the base. 1 HOLDS: the
    latest verdict is PASS and every finding is either resolved or carried as a
    documented open risk; the open set is 251 with maximum `R-0714`, and the
    STATUS line below therefore reads PASS_WITH_RISKS, exactly as F022's and
    F031's accepted lines do. 2 HOLDS: R17's integration gate passed and the
    reviewer re-ran the full suite itself, exit 0 at `17982 passed, 20
    skipped`. 3 HOLDS BY THE MODULE ROUTE: the `remedy` CLI is refused by this
    session's guard, and `packages.orchestration.integrity_gate.
    run_integrity_checks` returned `passed: true`, `fail_count: 0` at R18. 4
    HOLDS: `docs/roadmap/features/T5_F032.md` gained its Built State section at
    `c3cf408f`. 5 HOLDS: tree clean, branch pushed, remote tip equal.
(b) THE CLOSURE ARTIFACTS, from R18's handback and re-read from the evidence
    directory itself rather than from that file's prose. `review_subject.json`
    in `.remedy-wt/f032_closure_evidence/remedy-job-evidence-f032-closure`
    records `base_commit` `a399a3304f9d962cd920c251488c40c486b35fdc`,
    `base_is_ancestor` `True`, and `head_commit`
    `c3cf408f537de393bb156e45feae46d5de9f63da` over 134 commits.
    `verification_tests.json` carries four runs whose `selected` equals their
    node-id count in every case, at 134, 35, 55 and 4 — the same four numbers
    the reviewer measured independently at `12f28a42`.
(c) WHAT THE REVIEWER COULD NOT VERIFY, stated here so the STATUS line's
    provenance is honest. The package was archived to
    `/home/decodeux/Repos/remedy-history/zips`, which lies OUTSIDE this
    session's allowed working directories: both `ls` and `sha256sum` are
    refused there. THE PACKAGE FILENAME, ITS SHA-256 AND ITS ARCHIVED PATH
    THEREFORE REST ON R18's TRANSCRIPT AND NOT ON THE REVIEWER'S OWN READING.
    Everything else in the STATUS line was measured by the reviewer directly.
(d) THE STATUS LINE'S GRAMMAR, taken from the two accepted lines above F032's
    rather than from the template alone: `docs/roadmap/STATUS.md` line 80 is
    F022's and line 81 is F031's, both of the form `- [x] F0NN — <Name>
    (T001–T003 complete; accepted <date> · live review PASS_WITH_RISKS —
    ACCEPTED · Evidence job <id> · package <zip> · SHA-256 <hash> · accepted
    HEAD <sha>)` with an EN DASH in `T001–T003` and EM DASHES elsewhere.
    F032's line adds the `· package path <dir>` segment before `accepted HEAD`,
    which DECISION amend0827 D1 introduced after F031 closed and which is why
    neither neighbour carries it.
(e) THE README PINS THAT NO ONE WOULD FIND BY READING, and which the reviewer
    found by DRY-RUNNING the closure edits in a disposable worktree at
    `eb243fcd`. With only the STATUS flip and the capability paragraph applied,
    `python3 -m pytest tests/docs/ -q` went RED at `2 failed, 293 passed`:
    `test_the_readme_accepted_count_equals_the_status_count` and
    `test_the_readme_tier_table_done_column_matches_the_ledger`. That red is
    this round's control. Both pass once the two counts move, and the reviewer
    then measured `295 passed` with all four edits applied. The derivations:
    `README.md` line 19 reads `58 of 255 registered items accepted.` while the
    flipped ledger holds 59 `^- \[x\] F\d{3} — ` lines; and line 28 reads
    `| 5 | Operator Cockpit | 6 | 29 |` while the ledger derives 7 accepted
    Tier-5 features once F032 joins, `T5_F032.md` giving F032 its tier.
(f) THE NEXT FEATURE, for the README's `Next:` clause. `docs/roadmap/STATUS.md`
    line 83 is `- [ ] F037 — Rendered diff viewer`, the first unclaimed line
    after F032.
(g) `.agent/live_review.md` at the base: 274 paragraphs matching
    `^- R-\d+ — ` plus R-0714 gives 275 registered, 24 lines matching
    `^Done: R-\d+ — `, so the OPEN SET is 251 and the maximum id is `R-0714`.
    This round registers nothing and resolves nothing.
(h) THE R16/R17 GATE ENTRY IS KEYED IN A SHAPE THE RECORD'S OWN PATTERN CANNOT
    MATCH, and it is the reviewer's defect. LEDGER18 opened `Gate: F032 R16 and
    R17 — `, so `^Gate: F\d+ R\d+ — ` counted 69 before and after C2 of R18 and
    added no key. The entry is present and correct in every other respect. IT
    IS NOT REWRITTEN: this record is append-only and item 20 of the reviewer's
    checklist forbids overwriting landed text, so LEDGER19 below carries the
    dated correction that indexes it, and SLIP19 records the authoring failure.

----------

BUNDLE

C0a  save this block verbatim to `.agent/authored/f032-r19.md`
C0b  mirror the same bytes over `.agent/last_block.md`
C1   `.agent/plan.md`, slice PLANF032R19 applied whole
C2   `.agent/live_review.md` slice LEDGER19 appended, and
     `.agent/prose_slips.md` slice SLIP19 appended
C3   THE CLOSURE COMMIT: `docs/roadmap/STATUS.md` pair STATUSFLIP, `README.md`
     pairs READMECAP, READMECOUNT and READMETIER, and `.agent/handoff.md`
     rewritten — ONE commit, the LAST on the branch
C4   no commit. The pull request is opened after C3 and commits nothing.

CHANGE SET. Exactly these paths, and nothing else is created, edited or
deleted: `.agent/authored/f032-r19.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `.agent/prose_slips.md`,
`docs/roadmap/STATUS.md`, `README.md`, `.agent/handoff.md`. NO file under
`packages/`, `apps/`, `tests/` or `docs/roadmap/features/` is touched: the
Built State landed at `c3cf408f` and the accepted HEAD must stay where the
manifest recorded it.

----------

CONSTRAINTS

1.  A slice or a pair is applied BYTE FOR BYTE. Never retyped from memory,
    never reflowed, never trimmed, never corrected — if one looks wrong, apply
    it as given and say so in the handback's deviations.
2.  SLICE CONVENTION. A slice begins at the line after `<<<SLICE NAME>>>` and
    ends at the line before `<<<END NAME>>>`; a pair's FROM and TO are the
    bodies of `<<<FROM NAME>>>` and `<<<TO NAME>>>` under the same convention.
    Extract them PROGRAMMATICALLY from the committed C0a blob — `git show
    <C0a>:.agent/authored/f032-r19.md` — never by retyping from this prompt.
    PLANF032R19 REPLACES `.agent/plan.md` whole. LEDGER19 and SLIP19 are
    APPENDS: existing bytes, one newline, the slice.
3.  PAIR SHAPES, each classified by a containment test the reviewer RAN rather
    than judged, and each stated with the test's own output. READMECAP: `TO
    contains FROM: true` — an APPEND, so the obligation is FROM exactly 1x in
    the file before the edit plus each TO-ONLY added line exactly 1x among that
    commit's ADDED lines, and NEVER a FROM-zero count. STATUSFLIP: `TO contains
    FROM: false` — a REWRITE, so FROM 0x and TO 1x after. READMECOUNT: `TO
    contains FROM: false` — a REWRITE. READMETIER: `TO contains FROM: false` —
    a REWRITE. Every FROM occurs exactly ONCE in its target before the edit;
    the reviewer measured all four at `eb243fcd`.
4.  THE CLOSURE COMMIT IS THE LAST COMMIT ON THE BRANCH and it carries the
    STATUS flip and the README sync TOGETHER. They may never disagree in any
    committed state — that is the R-0154 pin and the reason the two files share
    one commit rather than two.
5.  The commits happen in the order the Bundle lists. C1 is the first
    substantive commit.
6.  Every commit passes the AGENTS.md self-review loop and the Commit Gate, and
    the tree is clean after each. Commit subjects carry no leading-slash token,
    no absolute path and no secret-like string.
7.  Push after C3. THEN open the pull request with `gh pr create`, base `main`,
    head `feature/f032-evidence-triple`. DO NOT MERGE IT, and do not merge
    anything else: the closure PR merges at the next feature's start via the
    Open PR Gate, and that gap is the operator's review window.
8.  Read `.agent/STOP` from disk twice — once before C0a and once before C3 —
    and report the exact command output both times. If it EXISTS at either
    reading, stop, write the handback, and end without creating the PR.
9.  Where a command's exit code is needed and this session's shell refuses
    `$?`, chain `&& echo <MARKER>` and report whether the marker printed.
10. Run no `npm`, `npx`, `node` or `vite`, and build no package: R18 built the
    one this round records, and a second package would not be the one the
    manifest covers.

----------

SPEC — what this round produces

S1. THE RECORD MOVES FIRST. C2 appends LEDGER19 to `.agent/live_review.md` and
    SLIP19 to `.agent/prose_slips.md`. Nothing is resolved, so `^Done: R-\d+ —
    ` does not move and the open set stays 251 with maximum `R-0714`.

S2. THE STATUS FLIP, pair STATUSFLIP against `docs/roadmap/STATUS.md`. Exactly
    one line changes and no other line in that file is touched.

S3. THE README SYNC, three pairs against `README.md` in this order: READMECAP
    adds F032's capability paragraph after F031's, READMECOUNT moves the
    accepted count and the `Next:` clause, READMETIER moves the Tier 5 Done
    cell. APPLY THEM IN THAT ORDER — READMECAP's anchor is a line the other two
    do not touch, and applying a rewrite first would not disturb it either, but
    a fixed order makes the diff reproducible.

S4. S2 AND S3 LAND IN ONE COMMIT WITH THE HANDBACK, which is C3 and the last
    commit on the branch. README and STATUS may never disagree in a committed
    state.

S5. THE PULL REQUEST, after C3 and after the push. Its description carries:
    what changed and why; the key decisions, naming DECISION F032 D1 through D8
    and amendments A1 through A7 by number; how to review; a changed-files
    table at feature granularity; the latest verdict; the open-findings count;
    and the runtime actuals S6 gives. Report the PR number and URL.

S6. RUNTIME ACTUALS, observed only and never guessed. Rounds: 19. Sessions: 4.
    Wall clock, models, tokens and cost: `not-measured` — this workflow records
    none of them, and `not-measured` beats an invented figure.

S7. NOTHING ELSE CHANGES. No production code, no test, no feature file, no
    evidence directory, no package.

S8. THE SPEC AND THE BUNDLE AGREE. S1 is C2; S2, S3 and S4 are C3; S5 and S6
    happen after C3 and commit nothing. Nothing in this SPEC is performed by a
    commit the Bundle does not list.

----------

SLICES AND PAIRS

<<<SLICE PLANF032R19>>>
# Plan — F032 Approval with the evidence triple

Branch: feature/f032-evidence-triple, cut from `main` at `a399a330`, the merge
commit of pull request #216 which closed the amend0827 process-diet order.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F032 D1 through D8.

## Goal
No decision without its receipts. Every decision a human is asked to answer
carries the evidence triple — `evidence_refs[]`, `expected_outcome` and
`downside` — the inbox card renders all three, and a producer that omits one
fails its own test. `docs/roadmap/features/T5_F032.md` holds Goal & Done, the
task slicing and the design amendments that reconcile it with the source.

## Current Step
R19 CLOSES F032. T001, T002 and T003 are complete, the integration gate passed
at R17 with an empty branch-only failure set, and R18 produced the evidence
bundle and the review package from the accepted HEAD `c3cf408f`. This round
books the R18 verdict, flips the STATUS line to `[x]` and syncs the README's
capability prose and its two ledger-derived counts in the SAME commit — they
may never disagree in a committed state — and then opens the pull request.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R18 verdict and the reviewer's slip | ordered | the record is touched first |
| C3 the closure commit and the handback | ordered | STATUS and README together, last on the branch |
| the pull request | ordered | after C3; NOT merged this session |

## Next Steps
1. The pull request merges at the NEXT feature's start, through the Open PR
   Gate of AGENTS.md. The gap is the operator's manual review window, and the
   operator may merge manually at any time instead.
2. The next feature is chosen by Rule A5 from `docs/roadmap/STATUS.md`, in a
   fresh session. `docs/roadmap/STATUS.md` names F037 as the next open line.

## Risks
- The package's filename, SHA-256 and archived path rest on R18's transcript:
  the archive directory lies outside this session's allowed working
  directories, so the reviewer could not re-read them.
- R-0714 is open and Medium. It does not touch F032's own code; it makes the
  integration gate's auto-build lever unenforceable and belongs to whoever
  repairs `tests/ui_server/test_dashboard_contract.py`.
<<<END PLANF032R19>>>

<<<SLICE LEDGER19>>>
Gate: F032 R18 — the closure part-one entry, and the last gate F032 records. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran them itself at `eb243fcd` except where this entry says otherwise. TRANSPORT IS PROVED FROM A VALUE THE REVIEWER HELD BEFORE DELEGATING: sha256 `f2a2f0895d9032f7fd7441ca4f4bcc3253113b3f0664a501917c1451b0c2ec37` over 35058 bytes and 452 lines, equal across the scratch original `.remedy-wt/f032-r18.md`, the committed `.agent/authored/f032-r18.md` blob and the committed `.agent/last_block.md` blob, the two committed paths being one git blob; that chain covers the original, the saved copy and the mirror and claims nothing about any prompt's bytes. THE THREE APPENDS ARE BYTE-IDENTICAL AND THE REVIEWER RECOMPUTED ALL OF THEM: `.agent/live_review.md` equals its pre-commit bytes plus one newline plus LEDGER18 plus one newline plus FINDING714, `.agent/prose_slips.md` equals its base plus SLIP18, and `docs/roadmap/features/T5_F032.md` equals its base plus BUILTSTATE, with the pre-commit blob a byte PREFIX in every case; the plan at `c084172b` is byte-equal to `PLANF032R18` with the trailing-newline negative control `False`, at 42 lines. THE OPEN SET MOVED EXACTLY AS ORDERED, from 250 to 251, with `R-0714` the single id added, nothing resolved and the maximum now `R-0714`. THE EVIDENCE BUNDLE IS REAL AND THE REVIEWER READ IT RATHER THAN THE HANDBACK'S PROSE: `review_subject.json` records `base_commit` `a399a3304f9d962cd920c251488c40c486b35fdc`, `base_is_ancestor` `True` and `head_commit` `c3cf408f537de393bb156e45feae46d5de9f63da` across 134 commits, and `verification_tests.json` carries four runs whose `selected` equals their node-id count at 134, 35, 55 and 4 — the same four numbers the reviewer had measured itself at `12f28a42` before ordering them, over `tests/orchestration/test_decision_evidence.py`, `tests/orchestration/test_decision_inbox.py`, `tests/ui_contracts/test_decision_answer_wiring.py` and `tests/ui_server/test_decisions_endpoint.py`. The directory holds the full closed-schema gate set the closure protocol names, `final_verifier_report`, `fresh_evidence_gate`, `artifact_contract_gate`, `change_provenance_gate`, `manifest_integrity`, `postmortem_integrity`, `commit_execution_gate` and `runtime_integration_gate`, and it is NOT committed, `git ls-files .remedy-wt` returning 0 lines. THE CANARY AND THE DOCS GATE WERE RE-RUN BY THE REVIEWER at exit 0 and `42 passed` and `295 passed`. WHAT THE REVIEWER COULD NOT VERIFY IS STATED RATHER THAN IMPLIED: the package was archived to a directory OUTSIDE this session's allowed working directories, where both `ls` and `sha256sum` are refused, SO THE PACKAGE FILENAME, ITS SHA-256 AND ITS ARCHIVED PATH REST ON R18's TRANSCRIPT AND NOT ON THE REVIEWER'S OWN READING; the STATUS line records them on that basis and this sentence is its provenance. THE WORKER DECLARED SEVEN DEVIATIONS AND THREE ARE WORTH THE RECORD. It built the zip TWICE, the first exit code having been masked by a pipe to `tail`, and rebuilt from the same clean tree at the same commit; the superseded package is still in the archive directory and nothing references it, which is the right disposition and is named here so no later reader mistakes it for the accepted one. Its first negative control for reader (b) applied a CHARACTER offset to a bytearray over em-dash-bearing text and so flipped a byte outside the appended region; it caught that itself, re-ran with a proven in-slice byte offset, and both readers then rejected in all three files — a defect of the control and not of the appends, found and fixed by the worker before any claim rested on it. AND IT REPORTED THAT THE GATE-KEY PATTERN DID NOT MOVE, 69 before and 69 after, which is the reviewer's own defect and is the correction this entry carries: the entry for rounds R16 and R17 is keyed `Gate: F032 R16 and R17 — `, which `^Gate: F\d+ R\d+ — ` cannot match, so a reader counting gate keys will not find it and a reader searching for either round must search for that literal string instead. IT IS NOT REWRITTEN — this record is append-only and landed text stays as it landed — and this sentence is its index. `.agent/prose_slips.md` carries the authoring failure. NOTHING ELSE MOVED: `docs/roadmap/STATUS.md`, `README.md`, `packages/`, `apps/` and `tests/` all EMPTY across the whole range, both path residues empty, `git worktree list` one line, `git branch --list "tmp/*"` empty, the remote tip equal to the local tip and the Open PR Gate `[]`. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END LEDGER19>>>

<<<SLICE SLIP19>>>
- 2026-08-28 · F032 R18 · The LEDGER18 slice was headed `Gate: F032 R16 and R17
  — `, a shape the record's own `^Gate: F\d+ R\d+ — ` pattern cannot match, so
  the entry for those two rounds adds no gate key and the count stood still at
  69 across the commit that wrote it. The reviewer's own pre-emission checklist
  requires a slice joining a repeating record format to be compared
  MECHANICALLY against the headers it joins, and that comparison was not run;
  the block's own gate reported the standing count and the worker declared it.
  The landed entry is not rewritten — the R19 entry carries the dated
  correction that indexes it. One round, one key: where an entry covers two,
  give it the later round's key and name the earlier one in the body.
<<<END SLIP19>>>

<<<FROM STATUSFLIP>>>
- [~] F032 — Approval with the evidence triple
<<<END STATUSFLIP>>>

<<<TO STATUSFLIP>>>
- [x] F032 — Approval with the evidence triple (T001–T003 complete; accepted 2026-08-28 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f032-closure · package remedy-review-20260828-032101-READY_FOR_REVIEW.zip · SHA-256 a368e28c61381e17de4bb46a5b35ecc975046be85d456983adf469759c1e2cf4 · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD c3cf408f537de393bb156e45feae46d5de9f63da)
<<<END STATUSFLIP>>>

<<<FROM READMECAP>>>
live, and answerable from the card through the one existing write channel).
<<<END READMECAP>>>

<<<TO READMECAP>>>
live, and answerable from the card through the one existing write channel).
F032 approval with the evidence triple (every producing decision carries its
evidence refs, an expected outcome and a downside, enforced where the decision
is derived so a producer that omits one fails its own test; the inbox card
renders the receipts, the honest note when a card has none, and each answer's
own outcome and downside under the answer it belongs to).
<<<END READMECAP>>>

<<<FROM READMECOUNT>>>
58 of 255 registered items accepted. Next: F032 (Approval with the evidence triple).
<<<END READMECOUNT>>>

<<<TO READMECOUNT>>>
59 of 255 registered items accepted. Next: F037 (Rendered diff viewer).
<<<END READMECOUNT>>>

<<<FROM READMETIER>>>
| 5 | Operator Cockpit | 6 | 29 |
<<<END READMETIER>>>

<<<TO READMETIER>>>
| 5 | Operator Cockpit | 7 | 29 |
<<<END READMETIER>>>

----------

DONE WHEN — the gates, in this order

Every gate is EXECUTED and its real output recorded. "Green" as a word is a
finding. G1 through G7 run at commits strictly earlier than C3, so the handback
C3 writes can quote all of them; G8 is the only gate that reads C3 itself and
its readings go in the round report, not in the handback.

G1 HYGIENE, BASE, SENTINEL. `git rev-parse HEAD` before C0a — REPORT it in full
   and confirm it equals the base this block names. `git rev-parse --abbrev-ref
   HEAD` is `feature/f032-evidence-triple`. `git status --porcelain | wc -l` is
   `0` after each of C0a, C0b, C1 and C2. `ls -la .agent/STOP` before C0a and
   again before C3 — report the exact output of both.

G2 TRANSPORT. One digest comparison, disk to disk. Report `sha256sum` over the
   reviewer's gitignored scratch original `.remedy-wt/f032-r19.md`, over
   `.agent/authored/f032-r19.md` at C0a and over `.agent/last_block.md` at C0b —
   all three equal — plus the git blob id of the two committed paths, which must
   be one blob. That chain covers the original, the copy and the mirror, and
   makes no claim about any prompt's bytes.

G3 EXTRACTION AND CAPS, measured on the COMMITTED C0a blob. Report the content
   line count of EACH slice and pair region found and how many regions there
   were, the block's TOTAL line count, and PROSE as TOTAL minus the content
   total. PROSE must be under 400 and TOTAL under 490.

G4 THE PLAN, at C1. `.agent/plan.md` is byte-equal to slice PLANF032R19
   extracted from the committed C0a blob — report `True`. NEGATIVE CONTROL: the
   same comparison with the slice's trailing newline removed — report `False`.
   Report `wc -l`, which must be under 50, and the counts of `^## Goal$` and
   `^## Next Steps$`, one each.

G5 THE APPENDS, at C2, each read with `git show <base-sha>:<path>` so no tracked
   file is ever overwritten to get a baseline. For EACH of
   `.agent/live_review.md` and `.agent/prose_slips.md`: READER (a), byte
   identity against the pre-commit bytes plus one newline plus the slice —
   report `True`, the arithmetic, and that the pre-commit blob is a byte PREFIX.
   READER (b), structural — count N, the paragraphs the slice contributes, and
   compare the LAST N blank-line units of the post-commit file against them IN
   ORDER; report N and the result. NEGATIVE CONTROL for each: flip one byte IN
   MEMORY inside the FIRST appended paragraph, at a BYTE offset and never a
   character offset, and report that BOTH readers reject it. Then report the
   open set and the maximum id before and after C2: both must be unmoved at 251
   and `R-0714`, because this round registers and resolves nothing.

G6 THE FOUR PAIRS, at C3, each proved in the shape constraint 3 assigns it.
   BEFORE the edit, report each FROM's occurrence count in its target file,
   which must be 1 for all four. AFTER the edit: for the three REWRITES
   (STATUSFLIP, READMECOUNT, READMETIER) report FROM 0x and TO 1x in the target;
   for the APPEND (READMECAP) report FROM exactly 1x and each TO-ONLY line
   exactly 1x AMONG THE LINES C3's DIFF ADDS, and order no FROM-zero count,
   which is unattainable by construction. Report `git show --numstat <C3> --
   README.md docs/roadmap/STATUS.md`.

G7 THE DOCS GATE AND THE CANARY, at C3 and BEFORE the pull request is opened.
   `python3 -m pytest tests/docs/ -q` and `python3 -m pytest
   tests/cli/test_golden_path.py -q` — report each exit code and pass line. The
   reviewer dry-ran the docs suite against these exact four edits in a
   disposable worktree at `eb243fcd` and measured `295 passed`, and measured the
   RED CONTROL of `2 failed, 293 passed` with only STATUSFLIP and READMECAP
   applied; report what you measure rather than either figure.

G8 STRUCTURE, THE PR AND THE GATE, reading C3. Report `git diff --name-only
   eb243fcd393fa4411cbb6cf55c9e273629c690c0..<C3>`, which is exactly the Change
   set — report BOTH residues. Report `git diff --stat
   eb243fcd393fa4411cbb6cf55c9e273629c690c0..<C3> -- packages/ apps/ tests/
   docs/roadmap/features/`, which must be EMPTY. Report the insertion count of
   every commit from C0a through C3, each single-parent and each under 500.
   Report `^<<<SLICE `, `^<<<END `, `^<<<FROM ` and `^<<<TO ` counts in
   `.agent/plan.md`, `.agent/live_review.md`, `.agent/prose_slips.md`,
   `docs/roadmap/STATUS.md` and `README.md`, against a CONTROL over the
   committed C0a blob. Report `git ls-files .remedy-wt`, `git worktree list`,
   `git branch --list "tmp/*"`, the push result, and finally `gh pr list --state
   open --json number,headRefName,baseRefName,isDraft` AFTER the PR exists,
   which must show exactly one non-draft PR from this branch into `main`.

----------

HANDBACK

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md, INSIDE C3 —
the closure commit carries it, which is why G8's readings belong to the round
report and not to this file. It has no length cap; it is valid when its
mandated sections are present. It carries: the feature and round, the SESSION
NUMBER — this is SESSION 4 of F032, whose rounds so far are R1 to R5 in session
1, R6 to R9 in session 2, R10 to R14 in session 3, and R15 through R19 in this
one — the branch, the base and every commit SHA, a per-commit changed-files
table with the `+/-` column for C0a through C2, ONE LINE PER GATE G1 to G7
carrying its real readings, the item-status table covering C0a to C4 and S1 to
S8 with every item present exactly once, the open-findings count, the
deviations and assumptions, and the closure artifacts R18 recorded, carried
forward verbatim so the STATUS line's provenance survives this rewrite.

STATE PLAINLY, in its own sentence, that the pull request was CREATED and NOT
MERGED, and that it merges at the next feature's start through the Open PR
Gate.

WRITE THIS FILE ONCE. `.agent/handoff.md` is rewritten in full every round and
is not an append-only record, so if a sentence in it turns out to be false, the
repair is a deviation line in the NEXT round's handback and NEVER a commit of
its own — that clause is carried here from the F032 R12 entry of
`.agent/live_review.md`, which labelled it binding on the next block ordering a
handback. Measure every numeral before writing it, and state no count you did
not count.
