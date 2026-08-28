STEP R1 / F037 — RENDERED DIFF VIEWER
Goal:        CLAIM F037. Cut the branch, flip `docs/roadmap/STATUS.md` from
             `[ ]` to `[~]`, reset the live-review header for the new feature
             carrying every finding record forward, append the F032 R19 gate
             entry the reviewer authored, and put the F037 SOURCE INVENTORY on
             disk. The inventory is this round's substance, not its
             bookkeeping: the feature file specifies a JSON contract with a
             `binary` file status and a unified-diff parser, while
             `packages/orchestration/review_scope.py` ALREADY parses unified
             diffs and `packages/orchestration/review_subject.py` ALREADY names
             a file-status vocabulary that carries `copied` and `type_changed`
             and no `binary`. What already exists, and what each existing
             reader DISCARDS, is a MEASUREMENT this feature must take before it
             plans T001.
             YOU CREATE NO PULL REQUEST THIS ROUND AND YOU MERGE NOTHING.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the
             plan and the context · C2 the STATUS claim · C3 the live-review
             header reset and the F032 R19 gate append · C4 the inventory ·
             C5 the handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f037-r1.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/context.md`,
             `docs/roadmap/STATUS.md`, `.agent/live_review.md`,
             `.agent/f037_inventory.md`, `.agent/handoff.md`. This list bounds
             what you WRITE INTO THE REPOSITORY. It does NOT bound what you DO:
             G8 orders a branch creation and a push. NOTHING under `apps/`,
             `packages/` or `tests/` is written, and under `docs/` ONLY
             `docs/roadmap/STATUS.md`.

Constraints:
 1. THIS BLOCK REACHES YOU AS A FILE, NOT AS PROSE IN A PROMPT. Read
    `.remedy-wt/f037-r1.md` from disk and copy it BYTE FOR BYTE to
    `.agent/authored/f037-r1.md` — with `shutil.copyfile` or a read-then-write
    in python, never by retyping it and never with `cp`, which this session's
    guard rejects. This block asserts NO digest of its own, because a digest
    written inside the text it measures cannot be true; G2 has you measure four
    points and prove them EQUAL, and the reviewer holds the scratch value
    independently.
 2. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. A SLICE begins at the line AFTER `<<<SLICE NAME` and ends at
    the line BEFORE `<<<END NAME`; its text is its content lines joined with a
    newline plus ONE trailing newline. If a slice contradicts something you
    measure, apply it anyway and DECLARE the contradiction in the handback
    under Deviations — a corrected slice destroys the transport proof.
    Declaring beats fixing every time, because a declared contradiction reaches
    a reviewer who can measure it while a silent fix reaches nobody.
 3. THE BRANCH IS CUT BEFORE C0a. From `main` at `9dde5495`, which is where
    your `git rev-parse HEAD` must already stand, run
    `git checkout -b feature/f037-rendered-diff-viewer`. Every commit of this
    round lands on that branch. NEVER COMMIT ON `main`.
 4. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5. Every sentence in
    PLANF037R1 that describes THIS round's own landed change depends on that
    order, and this constraint is what fixes it.
 5. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES F032. That is
    ordered: the plan becomes current at C1, which is the FIRST substantive
    commit of the round.
 6. NOTHING IS EDITED OUT OF THE FINDINGS REGION. `.agent/live_review.md` is
    append-only from its `## Findings` heading down. This round rewrites ONLY
    the header region ABOVE that heading, via the single LFROM/LTO pair, and
    APPENDS the GATEF032R19 slice at end of file. No finding
    paragraph, no `Done:` line and no existing `Gate:` paragraph is rewritten,
    deleted, renumbered or touched, and NO finding is registered or resolved
    this round.
 7. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Gate:` paragraph of
    your own, never mint a finding id and never author a `Done:` line. If you
    find a defect, report it in the handback under Deviations and let the
    reviewer rule on it.
 8. THE INVENTORY IS YOURS TO WRITE AND IT IS THE ONLY SUCH FILE. Everything
    in `.agent/f037_inventory.md` is YOUR OWN MEASUREMENT, written by you, not
    a slice. Every answer cites `path:line` or a command and its real output.
    WHERE YOU CANNOT MEASURE SOMETHING, WRITE THAT YOU COULD NOT AND WHY —
    an honest gap is worth more to the next round than a confident guess, and
    a guess in an inventory becomes a wrong T001 plan.
 9. RE-READ `.agent/STOP` FROM DISK before C0a and again before C5. If it
    exists at either reading, finish the commit in hand, write the handback and
    STOP.
10. NOTHING DESTRUCTIVE IS ORDERED THIS ROUND. Create no worktree. Run no
    `npm`, `npx`, `node` or `vite`, and build nothing. The primary checkout
    reads `git status --porcelain` 0 lines at every commit.
11. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `${...}` and every other expansion, `cp`, brace literals
    containing a quote character, `cd x && y`, file redirects, and every form
    of environment assignment. Route anything that counts, hashes or compares
    through a quoted python heredoc, read real exit codes from
    `subprocess.run(...).returncode`, and pass `cwd=` rather than `cd`. Run
    pytest SERIALLY — never two pytest processes alive at once. `--timeout` IS
    NOT AVAILABLE to pytest here: passing it exits 4 and reports no failure.
12. EVERY NUMERAL THIS BLOCK STATES ABOUT THE ROUND BASE `9dde5495` was
    measured by the reviewer at that commit. It is a REFERENCE to report
    against, NOT a target to reproduce. Where your measurement differs, report
    BOTH and reconcile NOTHING.
13. THE REPLACEMENT PAIRS ARE CLASSIFIED BY A MECHANICAL CONTAINMENT TEST
    THE REVIEWER RAN, one reading per pair, and the output is printed here.
    LFROM/LTO — `TO contains FROM: false`, so REWRITE. SFROM/STO —
    `TO contains FROM: false`, so REWRITE. Both therefore carry the FROM-zero
    obligation of `docs/agents/planner_reviewer_prompt.md` §4.9 and neither
    carries the append obligation. GATEF032R19 is not a pair at all: it is an
    EOF APPEND to `.agent/live_review.md`, proved by G5's reconstruction.
14. YOUR HANDBACK CARRIES A `## Session` SECTION reading that this is SESSION 1
    of F037 and that R1 is the round. The handback has NO LENGTH CAP — operator
    amendment amend0827 rule 3 withdrew every tier — so do not declare, measure
    or apologise for its length. It is VALID when its mandated sections are
    present, and DROPPING one is the finding the cap used to stand in for.

Inventory spec — `.agent/f037_inventory.md`, answer each, MEASURED:
 Q1. THE PARSERS THAT ALREADY EXIST, which is the question that decides T001.
     For `packages/orchestration/review_scope.py`, give the signature and the
     return shape of `_parse_diff`, `parse_diff_line_ranges` and
     `split_diff_by_path`, and state for EACH what it DISCARDS of what F037's
     contract needs: the per-line kind (`ctx`/`add`/`del`), old and new line
     numbers, the hunk header text, rename headers, binary markers. Then run
     `rg -ln 'unified|@@' packages/ --type py` and, for every module it
     returns that really reads unified-diff syntax, name the module and what
     it parses in one line each. Answer in ONE sentence: can F037's JSON
     contract v1 be produced by extending an existing reader, or does it need
     a new module?
 Q2. THE FILE-STATUS VOCABULARY. From `packages/orchestration/review_subject.py`
     list every `STATUS_*` constant and the whole of `_GIT_STATUS_MAP` with
     `path:line`. F037's contract names `modified|added|deleted|renamed|binary`.
     State exactly which of those five exist, which do not, and which existing
     constants the contract omits. Then find what this repository does with a
     BINARY file in a diff today and cite the code that decides it; if nothing
     does, say so plainly.
 Q3. WHERE A DIFF COMES FROM AT RUNTIME. Name every place a unified diff TEXT
     is produced or stored for a job, task or attempt — the module, the
     function, and the on-disk path if it is persisted. State whether a diff is
     kept PER ATTEMPT or only for the latest state, because the feature file's
     endpoint takes an attempt parameter and that answer decides whether it can
     be served at all.
 Q4. THE SERVER ROUTE TABLE. In `packages/orchestration/ui_server.py` list
     EVERY request path the handler answers, with `path:line`, and show the
     exact code shape by which a route is added. Then run
     `rg -ln 'ui_server' tests/` and name every test that pins the route set,
     an exact endpoint list, or counts something over the whole of
     `ui_server.py` — the guards a new endpoint would turn red. Cite
     `path:line` for each.
 Q5. THE ATTEMPT IDENTIFIER. Three attempt notions appear in
     `ui_server.py`: `list_repair_attempts`, the `repair_attempts_v1` job
     metadata, and `self_dogfood_execution.list_attempts`. For each name the
     module, the id field and its type. Answer in ONE sentence whether a single
     canonical attempt id exists across all three, because the endpoint's
     parameter must name exactly one.
 Q6. THE CLIENT ENTRY POINT. `docs/ui/design_reference/component_spec.md`
     names `onOpenDiff(taskId)` on the DetailPopover as the viewer's entry
     point. Run `rg -n 'onOpenDiff|DiffViewer' apps/ui/src/` and report the
     REAL count and every hit. Then report what props
     `apps/ui/src/components/detail/DetailPopover.tsx` takes today and name the
     test file that pins that component.
 Q7. THE FETCH SEAM AND THE BUNDLE BUDGET. In `apps/ui/src/api/remedyApi.ts`
     name the function that performs a GET, its error and degraded convention,
     and how a caller reaches it. Then search the suite for any bundle-size or
     asset-size budget (`rg -ln 'bundle|dist|asset' tests/`) and report the
     exact ceiling and the file that holds it, or state that none exists —
     F037 lazy-loads language bundles and that budget binds T003.
 Q8. THE GUARDS A NEW MODULE MUST SATISFY. Run
     `rg -ln 'review_scope|review_subject' tests/` and, for what it returns,
     list every assertion that COUNTS something over a whole file, pins an
     exact field set, an exact export set or an exact list of statuses — the
     equality guards a new parser or a widened vocabulary would turn red. Cite
     `path:line` for each.

Done when:
 G1. HYGIENE, THE BRANCH AND THE SENTINEL. Report `git rev-parse HEAD` BEFORE
     the branch is cut, which must be
     `9dde54956afbe5f432bfd429bf4ba0bb272f6d07`, and `git branch
     --show-current` after C0a, which must be
     `feature/f037-rendered-diff-viewer`. Report `git status --porcelain` as a
     LINE COUNT after each of C0a, C0b, C1, C2, C3 and C4, each 0. C5's own
     reading is NOT ordered here and belongs in no file this round writes: C5
     is the commit that writes the handback, so the reviewer takes that reading
     itself at the gate. Report `.agent/STOP` read from disk before C0a and
     before C5, both ABSENT.
 G2. TRANSPORT. Report the sha256, byte count and line count of this block as
     read from `.remedy-wt/f037-r1.md`, as saved at C0a, as mirrored at C0b and
     as read off disk at C4 — all four must be EQUAL — and say whether C0a and
     C0b are the same git blob. Report whether any line of the block as saved
     is a run of a single repeated character at length 4 or more, which must
     come back as none. THEN STATE IN ONE SENTENCE WHAT THIS PROOF COVERS: the
     scratch file, the saved copy, its mirror and the working copy, and NOT the
     bytes of any prompt.
 G3. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES. Report how many slices your extractor printed, each
     slice's own line count, the CONTENT total, the TOTAL line count, and PROSE
     as TOTAL minus CONTENT. MARKERS ARE PROSE. PROSE at most 400, TOTAL at
     most 490.
 G4. THE PLAN AND THE CONTEXT. `.agent/plan.md` at C1 is BYTE-EQUAL to
     PLANF037R1 and `.agent/context.md` at C1 is BYTE-EQUAL to CTXF037R1, both
     under the newline-INCLUDED convention. Run the negative control against
     each slice MINUS its trailing newline and report both FALSE. Then report
     the contract readings: in `.agent/plan.md`, `^## Goal$` 1,
     `^## Next Steps$` 1, a match for `\bF\d{3}\b`, and `wc -l` STRICTLY UNDER
     50; in `.agent/context.md`, `^## Active Branch$` 1, a match for
     `feature/`, a match for `\bF\d{3}\b`, and the substring `Steps` present.
 G5. THE LEDGER RESET, THE GATE APPEND, AND THE FINDINGS REGION PROVED
     UNTOUCHED. Apply the LFROM/LTO pair, then append GATEF032R19 as: the file
     as it stood before C3, plus exactly ONE newline, plus the slice. Prove the
     result by RECONSTRUCTION: build, in memory, LTO plus two newlines plus
     everything from the first byte of the line `## Findings` in the PRE-COMMIT
     blob to its end, plus one newline, plus GATEF032R19 — and report that it
     is BYTE-EQUAL to `.agent/live_review.md` at C3. Report a NEGATIVE CONTROL:
     the same comparison with ONE byte flipped, at a byte offset you assert and
     report to lie INSIDE the appended paragraph, must come back FALSE. Then,
     comparing the pre-commit blob with the file at C3: LFROM occurs EXACTLY
     ONCE before and 0 times after, LTO 0 before and EXACTLY ONCE after, and
     the pre-commit blob is NOT a byte prefix of the result, because the header
     changed. Report the byte count and sha256 of the region from the first
     byte of `## Findings` to the END OF THE PRE-COMMIT BLOB at both points and
     prove them EQUAL — the reviewer measured that region at the round base as
     1124868 bytes, sha256
     `abc8bdb4f682d04bc84d56ca0eda9d23dc17c32cb5987fab8e3d91c932a7f528`. Report
     the line-anchored counts of `^- R-\d+ — `, `^Done: R-\d+ — `,
     `^Landed: R-`, `^Gate: R\d+ — ` and `^Gate: F\d+ R\d+ — ` at both points;
     the reviewer measured 275, 24, 1, 19 and 70 at the base, and every one
     MUST be unchanged EXCEPT the last, which must read 71. Report the finding
     ids and the resolved ids ADDED and REMOVED as SETS — all four EMPTY —
     whether all ids are DISTINCT, the maximum id at each point, which is
     `R-0714`, and the open set at each point, which is 251. Report that
     `^## Findings$` occurs exactly 1 at both points, that `Steps` is present
     at both, and that the literal string `Gate: F032 R19 — ` occurs 0 times
     before and EXACTLY ONCE after.
 G6. THE STATUS CLAIM AND THE DOCS GATE. Apply the SFROM/STO pair, then BEFORE
     committing C2 run, as ONE pytest process, `python3 -m pytest tests/docs/
     tests/orchestration/test_roadmap_index.py -q` from the repository root and
     report the REAL exit code and the summary line VERBATIM; the reviewer
     measured `325 passed` at a real exit 0 at the round base. Then report, for
     `docs/roadmap/STATUS.md` at C2: SFROM occurs 0 times and STO occurs
     EXACTLY ONCE; the line-anchored counts of `^- \[ \] `, `^- \[x\] ` and
     `^- \[~\] ` at both points, which the reviewer measured as 196, 59 and 0
     at the base and which must read 195, 59 and 1 after; and that the total
     count of lines matching `^- \[` is UNCHANGED at both points.
 G7. THE STATE READERS AND THE CANARY, run AFTER C4 and BEFORE C5. This round
     rewrites `.agent/` state, so `.agent/context.md`'s standing constraint
     binds: run, as ONE pytest process and never two at once, `python3 -m
     pytest tests/ui_server/ tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py
     tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py
     -q` from the repository root. Report the REAL exit code, the summary line
     VERBATIM, and the COUNT of lines matching `^FAILED`. PROVE YOUR `^FAILED`
     EXTRACTOR IS NOT BLIND by running it over a string you know contains such
     a line and reporting that it matched. The reviewer measured `620 passed`
     at a REAL exit 0 with zero `^FAILED` lines at the round base. IF YOUR RUN
     IS RED, report the failing node ids VERBATIM and hand back.
 G8. STRUCTURE, ARTIFACTS, THE OPEN PR GATE AND THE PUSH. Compare the path set
     of `git diff --name-only 9dde5495..C4` BOTH WAYS against this round's
     expected set — the Change line's list MINUS `.agent/handoff.md`, which C5
     writes — and report both residues EMPTY. Report `git diff --stat
     9dde5495..C4` restricted to `apps/`, `packages/`, `tests/` and `docs/` —
     the last WHOLE — and confirm the first three EMPTY and the fourth holding
     `docs/roadmap/STATUS.md` alone. Report each commit's insertions from `git
     diff --numstat` for C0a through C4, confirm each single-parent and under
     500. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0 and 0 in
     `.agent/plan.md`, `.agent/context.md` and `.agent/live_review.md` at their
     commits, against a CONTROL over the C0a blob which is not 0. Report `git
     ls-files .remedy-wt` 0 lines, `git worktree list` 1 line, and `git branch
     --list "tmp/*"` 0 lines. Run `gh pr list --state open --json
     number,headRefName,baseRefName,isDraft` and report it VERBATIM; the
     reviewer read `[]` at the round base; MERGE NOTHING and CREATE NOTHING.
     After C5, run `git push -u origin feature/f037-rendered-diff-viewer`. ITS
     OUTCOME IS NOT A VALUE OF ANY FILE THIS ROUND WRITES: C5 is authored
     before the push exists, so `.agent/handoff.md` states the push only as an
     INTENT under `## External actions`, with NO exit code and NO remote tip.
     Report the real exit code and the resulting remote tip in your completion
     report instead.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C5: the `## Session` section constraint 14 orders, feature and
             round, branch, the round base SHA `9dde5495`, the per-commit
             changed-files table with the `+/-` column taken from `git diff
             --numstat` ITSELF and agreeing cell for cell with G8, an
             item-status row for EVERY Bundle item AND every Q1-Q8 inventory
             question, ONE LINE PER GATE for G1 through G8 with its real exit
             code, the open-findings count after this round, and the next
             expected action. C5 cannot table its own numstat — write `self` in
             that cell, as `R-0149` requires, and put C5's own numbers nowhere.
             STATE PLAINLY in the Deviations section what Q1 and Q2 measured,
             because those two answers decide whether the feature file's
             contract survives contact with the source and the reviewer rules
             on it next round.
             ANY COMMIT YOU MAKE BEYOND THE ORDERED SEQUENCE RECEIVES ITS OWN
             `## Commits` ROW AND ITS OWN ITEM-STATUS ROW, and the Deviations
             section says so in those same words.

<<<SLICE PLANF037R1
# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495`, the
merge commit of pull request #217 which closed F032.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint per task and attempt, and the client renders it with a file sidebar,
hunk collapse, virtual scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the orchestrator brief.

## Current Step
R1 claims F037 in the roadmap ledger, cuts the branch, resets this record set
for the new feature, books the F032 R19 verdict, and puts the F037 source
inventory on disk. The inventory is the round's substance: `review_scope.py`
already parses unified diffs and `review_subject.py` already names a
file-status vocabulary, while the feature file specifies a contract matching
neither exactly, so what already exists is measured before T001 is planned.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 plan and context for F037 | ordered | first substantive commit |
| C2 STATUS claim, open to active | ordered | |
| C3 ledger reset and the F032 R19 gate | ordered | findings carried forward |
| C4 the F037 source inventory | ordered | Q1-Q8, each measured |
| C5 the handback | ordered | |

## Next Steps
1. Book R1's verdict and plan T001 against the inventory — the parser seam, the
   status vocabulary and the route the read endpoint attaches to.
2. T001: the unified-to-JSON parser, its corpus tests and the read endpoint.
3. T002 the rendering core, then T003 sidebar, virtual scrolling, lazy
   languages and the L3 tab.

## Risks
- The feature file's contract names a `binary` file status that
  `review_subject.py`'s vocabulary does not carry, and that vocabulary carries
  `copied` and `type_changed` which the contract omits. If the inventory
  confirms this, the reviewer rules a DECISION under §4 item 7 rather than
  widening scope silently.
- `.agent/live_review.md` is append-only below `## Findings`. R1 rewrites the
  header region and appends the F032 R19 gate entry, and G5 proves both.
<<<END PLANF037R1

<<<SLICE CTXF037R1
# Context — F037 Rendered diff viewer

## Active Branch
feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495`, the merge
commit of pull request #217 which closed F032.

## Scope
Feature F037 per `docs/roadmap/features/T5_F037.md`: a versioned structured
diff JSON served as a read endpoint per task and attempt, and a client viewer
that renders files, hunks, lines and intraline spans with a file sidebar, hunk
collapse, virtual scrolling beyond 2k lines and lazily loaded language bundles.

## Do not touch
The feature file's own list: hunk-id stability, which is F033's contract; apply
mechanics; evidence formats. No approval logic is added early — the viewer
precedes hunk approval in STATUS deliberately. R1 additionally writes no file
under `packages/`, `apps/` or `tests/` at all.

## Assumptions
- Rule A5 chose F037: `docs/roadmap/STATUS.md` carried no `[~]` and no `[!]`
  line and F037 was the first `[ ]`, measured at `9dde5495`.
- `.agent/candidates.md` is EMPTY at the claim, so no block condition stands.
- The feature file's Design is a SUGGESTED shape, not a settled spec; the
  inventory measures the real one before T001 is planned.
- This is a UI feature, so `docs/ui/design_reference/` is binding from T002 on
  and any visual deviation is documented with a technical reason.

## Constraints
The bullets in this first group are STANDING project constraints, carried
forward from the context this file replaced. They are not this feature's, and
deleting them with the rest of a rewrite is what cost an earlier round a red
CI run.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout, which satisfies
  `git status --porcelain` empty at every verdict.
- THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE. The full contract those
  readers hold over the three state files, so a rewrite is checked against it
  directly rather than rediscovered from a red: this file carries
  `## Active Branch`, a `feature/` branch name, a roadmap feature id matching
  `\bF\d{3}\b` and the word `Steps`; `.agent/plan.md` carries `## Goal`,
  `## Next Steps` and a feature id; `.agent/live_review.md` carries `Steps`.

## Steps
The round map for this feature lives in the `## Steps` section of
`.agent/live_review.md`, and the current round's items in the `## Current Step`
table of `.agent/plan.md`. This file deliberately restates neither — a second
copy of the map is what fell out of step and cost F022 a finding.
<<<END CTXF037R1

<<<SLICE LFROM
# Live Review — F032 Approval with the evidence triple

> Round-by-round review record for the F032 branch, reset at the feature claim.
> The F031 record closed with pull request #215, merged into `main` as
> `f4eae1d4`, and the operator collection order amend0827 which followed it
> merged as pull request #216 at `a399a330`, this branch's point. F031's LAST
> round has no gate entry in its own record by construction, because a round's
> verdict is written by the NEXT reviewed round (DECISION F085 D9) and it was
> the last round F031 had; the amend0827 order was a single-session micro-round
> whose verdict lives in its own handback and in pull request #216, and it
> appended its notes to this file without a gate entry for the same reason.
> Finding ids continue the monotonic R-XXXX series across the reset, and every
> finding record F031 carried is carried forward unchanged: measured at
> `a399a330`, 270 findings, 21 resolved, 249 open, the maximum id `R-0709`.

## Steps

R1 claim F032 in the roadmap ledger, cut the branch, reset this record carrying
every finding record forward, and put the F032 source inventory on disk — the
eight producing branches of `decision_queue.list_decisions`, the record each
derives from, whether any enqueue seam is common to them, the evidence-ref
vocabulary and its resolver, the options a decision offers, the card's
rendering surface, the migration precedent and the guards a schema change must
satisfy → R2 book the R1 verdict and plan T001 against that inventory → T001
the schema, the enforcement point, legacy rendering and the CI canary → T002
the per-producer upgrades → T003 card enrichment and the chip deep links.
<<<END LFROM

<<<SLICE LTO
# Live Review — F037 Rendered diff viewer

> Round-by-round review record for the F037 branch, reset at the feature claim.
> The F032 record closed with pull request #217, merged into `main` as
> `9dde5495`, this branch's point. F032's LAST round, R19, is the round whose
> own bundle CREATED that pull request, so it is a branch terminator under
> `docs/agents/planner_reviewer_prompt.md` §4 item 13 and owes this record no
> entry. Its verdict is nevertheless the first `Gate:` paragraph below, because
> the finding record carries across the reset and an entry therefore costs this
> round nothing — the disposition F031's own R1 chose for F022 R19. Finding ids
> continue the monotonic R-XXXX series across the reset, and every finding
> record F032 carried is carried forward unchanged: measured at `9dde5495`,
> 275 findings, 24 resolved, 251 open, the maximum id `R-0714`.

## Steps

R1 claim F037 in the roadmap ledger, cut the branch, reset this record carrying
every finding record forward, gate F032 R19, and put the F037 source inventory
on disk — the unified-diff readers that already exist and what each discards,
the file-status vocabulary and whether it names `binary`, where a diff is
produced and whether one is kept per attempt, the server route table and the
guards over it, what identifies an attempt, the client entry point the design
reference names, the fetch seam and the bundle budget, and the guards a new
parser must satisfy → R2 book the R1 verdict and plan T001 against that
inventory → T001 the parser, its corpus and the read endpoint → T002 the
rendering core, the binding CSS and the goldens → T003 sidebar, virtual
scrolling, lazy languages and the L3 tab.
<<<END LTO

<<<SLICE GATEF032R19
Gate: F032 R19 — the F032 closure round, and the entry F032's own record could not write. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran the reproducible ones itself at `97e91098` before merging the pull request; because R19 created that pull request it is a branch terminator under `docs/agents/planner_reviewer_prompt.md` §4 item 13, and this paragraph is written by the next feature's first round rather than by a round of F032. TRANSPORT IS PROVED OVER THE THREE DISK COPIES AND NO FURTHER: sha256 `bccbd4be2011a1b90f2533bea086d6f2fe6aa548c1fc0c22aaf29e0e206a35ff` is equal across the working copies of `.agent/authored/f032-r19.md` and `.agent/last_block.md` at `97e91098`, and the two committed paths are ONE git blob, `3797fb6373eb133fc0fcf3e47d3d5d329db012f1`. The reviewer of this round held no scratch original, R19 having been authored in a previous session, so the chain covers the saved copy, its mirror and the working copy, and claims NOTHING about the bytes of any prompt — the limit operator amendment amend0827 rule 5 and finding R-0705 both require to be stated rather than implied. EXTRACTION REPRODUCES THE BLOCK'S OWN ARITHMETIC: 11 regions extracted from the committed C0a blob at their marker lines, at 44, 1, 10, 1, 1, 1, 6, 1, 1, 1 and 1 content lines, CONTENT 68 against a TOTAL of 405, so PROSE is 337 and both caps hold. THE PLAN IS BYTE-EQUAL to slice PLANF032R19 with the trailing-newline negative control `False`, at 44 lines. BOTH APPENDS RECONSTRUCT EXACTLY: `.agent/live_review.md` and `.agent/prose_slips.md` each equal their pre-commit blob at `0b83f8a1` plus one newline plus their slice, with the pre-commit blob a byte PREFIX in each case. THE FOUR PAIRS HOLD IN THE SHAPE THE BLOCK ASSIGNED THEM, measured against `e9af5b63`: every FROM occurred exactly 1x before the edit; STATUSFLIP, READMECOUNT and READMETIER are REWRITES and read FROM 0x and TO 1x after; READMECAP is the APPEND, its TO containing its FROM, and reads FROM 1x and TO 1x after. THE CLOSURE COMMIT'S NUMSTAT AGREES WITH THE HANDBACK CELL FOR CELL — `git show --numstat 97e91098` reads `7 2 README.md` and `1 1 docs/roadmap/STATUS.md`, which is what the handback reported from the tree that became that commit, so its declared deviation about the timing of that reading cost the record nothing. THE LEDGER-DERIVED COUNTS IN THE README ARE TRUE AND NOT MERELY APPLIED, which is the reading the block's own gates did not order: derived mechanically from `docs/roadmap/STATUS.md` at `97e91098`, the accepted lines number 59 of 255 and Tier 5 stands at 7 of 29, and the README states exactly those two figures and names F037 as next, which is the first `[ ]` line in that file. THE TWO SUITES WERE RE-RUN BY THIS REVIEWER at a real exit 0: `python3 -m pytest tests/docs/ -q` → `295 passed in 0.44s`, and `python3 -m pytest tests/cli/test_golden_path.py -q` → `42 passed in 20.62s`. THE RECORD DID NOT MOVE, as ordered: `^- R-\d+ — ` 275, `^Done: R-\d+ — ` 24, open set 251, maximum id `R-0714`, and every id distinct. HYGIENE HELD AT THE VERDICT: `git status --porcelain` 0 lines, `git worktree list` one line, `git ls-files .remedy-wt` 0 lines, and the remote tip equal to the local tip. WHAT THIS REVIEWER DID NOT VERIFY IS STATED RATHER THAN IMPLIED: the package filename `remedy-review-20260828-032101-READY_FOR_REVIEW.zip`, its SHA-256 and its archived path `/home/decodeux/Repos/remedy-history/zips` rest on R18's transcript and on R19's application of them, because that directory lies outside this session's allowed working directories where `ls` and `sha256sum` are both refused; the STATUS line records them on that basis and this sentence is their provenance. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change. PULL REQUEST #217 WAS MERGED AT THE OPEN PR GATE after this verdict, with CI reported `pass` and the merge state `CLEAN`, and `main` fast-forwarded to `9dde54956afbe5f432bfd429bf4ba0bb272f6d07`, which is the point F037's branch is cut from.
<<<END GATEF032R19

<<<SLICE SFROM
- [ ] F037 — Rendered diff viewer
<<<END SFROM

<<<SLICE STO
- [~] F037 — Rendered diff viewer
<<<END STO
