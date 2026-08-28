STEP INTEGRATION GATE / F032 — ROUND R16 — the full suite, twice, with parity

BASE. This block is authored against `2a8722271815f6560220d84243d7d59daa49b6c0`,
the tip of `feature/f032-evidence-triple` and the last commit of R15. Every
reading below was taken there by the reviewer unless another SHA is named.

FRAME CONVENTION. Every rule line in this block is exactly ten hyphens, and no
other line is a run of one repeated character. Nothing in the frame is
appliable: the appliable bytes are the slices, each proved against its own
target by its own gate.

----------

GOAL

Run the integration gate of docs/agents/integration_gate.md for F032: the full
suite on this branch, the full suite at the merge base with artifact parity
restored, the two failure sets compared, and every branch-only id attributed.
This round writes NO production code. Its product is the evidence directory and
an honest verdict about whether this branch may proceed to closure.

----------

WHAT THE REVIEWER READ AND MEASURED BEFORE ORDERING ANY OF THIS

(a) `git merge-base HEAD main` at the base is
    `a399a3304f9d962cd920c251488c40c486b35fdc`, which is also the commit
    `.agent/plan.md` names as this branch's cut point. That is the base run's
    commit.
(b) THE FRONTEND IS STALE IN THE PRIMARY CHECKOUT RIGHT NOW, and this is the
    load-bearing reading of this block. `packages/orchestration/ui_server.py`
    defines `_frontend_is_stale()` at line 3050: it returns True when ANY file
    under `apps/ui/src` has an mtime newer than `apps/ui/dist/index.html`.
    Measured at the base: `dist/index.html` carries `Thu Aug 27 23:05:36 2026`
    while the newest source file,
    `apps/ui/src/components/panels/RightLivePanel.module.css`, carries `Fri Aug
    28 02:25:15 2026`, and `_frontend_is_stale()` returns `True`. R14 and R15
    both edited `apps/ui/src`, which is why. Line 3141 of the same module
    reaches `_auto_build_frontend` on that condition, so a full-suite run
    started now would rebuild `dist` MID-RUN — the exact class R-0169 records,
    where a dist rewritten during a run produced false manifest-identity
    failures. G6 therefore builds the frontend BEFORE the branch run and proves
    staleness is gone, rather than discovering it as failures.
(c) `apps/ui/dist` and `apps/ui/node_modules` both EXIST in the primary
    checkout and are both gitignored — `git check-ignore -v` resolves them to
    `.gitignore` lines 13 and 221. A fresh worktree therefore carries NEITHER,
    which is precisely the environment class step 3 of
    docs/agents/integration_gate.md exists to neutralise.
(d) `apps/ui/package.json` declares `"build": "vite build"`, so the build
    command is `npm run build` from `apps/ui`.
(e) `.agent/gate_f255_r18/` is the most recent gate evidence directory and its
    file names are `attribution.txt`, `base_failed.txt`, `base_parity.txt`,
    `branch_failed.txt`, `branch_meta.txt`, `branch_run_tail.txt`,
    `comm_base_only_failures.txt`, `comm_branch_only_failures.txt` and
    `full_log_provenance.txt`. This round reuses those names exactly rather
    than inventing a second vocabulary.
(f) `.agent/live_review.md` at the base, read mechanically: 274 paragraphs
    matching `^- R-\d+ — `, 24 lines matching `^Done: R-\d+ — `, so the OPEN
    SET is 250 and the maximum id is `R-0713`. `^Gate: F\d+ R\d+ — ` counts 67
    and its newest key is `F032 R14`.
(g) `.agent/prose_slips.md` at the base is 43 lines and its entries are of the
    form `- <date> · F032 R<n> · <sentence>`, wrapped with two-space
    continuation indent. SLIP16 below matches that shape.
(h) THE OPEN SET WAS SEARCHED FOR THE DEFECT SLIP16 RECORDS — a reviewer block
    that failed to carry forward a fix clause another entry had labelled
    binding — before deciding it earns no id. Under operator amendment
    amend0827 rule 2 it is reviewer prose that left nothing wrong under
    `packages/`, `apps/`, `tests/` or `docs/`, so it is one dated line in
    `.agent/prose_slips.md` and never an R-id.

----------

BUNDLE

C0a  save this block verbatim to `.agent/authored/f032-r16.md`
C0b  mirror the same bytes over `.agent/last_block.md`
C1   `.agent/plan.md`, slice PLANF032R16 applied whole
C2   `.agent/live_review.md` slice LEDGER16 appended, and
     `.agent/prose_slips.md` slice SLIP16 appended
C3   the gate evidence directory `.agent/gate_f032_r16/`
C4   the handback

CHANGE SET. Exactly these paths, and nothing else is created, edited or
deleted: `.agent/authored/f032-r16.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `.agent/prose_slips.md`, the files
of `.agent/gate_f032_r16/` named in G8, and `.agent/handoff.md`. NO file under
`packages/`, `apps/`, `tests/` or `docs/` is edited this round. `apps/ui/dist`
is REBUILT, which changes no tracked file because it is gitignored.

----------

CONSTRAINTS

1.  A slice is applied BYTE FOR BYTE. It is never retyped from memory, never
    reflowed, never trimmed and never corrected — if a slice looks wrong, apply
    it as given and say so in the handback's deviations.
2.  SLICE CONVENTION. A slice begins at the line after `<<<SLICE NAME>>>` and
    ends at the line before `<<<END NAME>>>`. The slice's bytes are those lines
    including the newline that ends the last of them. Extract them
    PROGRAMMATICALLY from the committed C0a blob — `git show
    <C0a>:.agent/authored/f032-r16.md` — never by retyping from this prompt.
    PLANF032R16 REPLACES `.agent/plan.md` whole. LEDGER16 and SLIP16 are
    APPENDS: the target's existing bytes, then exactly one newline, then the
    slice.
3.  RUN LOGS ARE WRITTEN OUTSIDE THE REPOSITORY WORKTREE WHILE A SUITE RUNS and
    copied into `.agent/gate_f032_r16/` only after the run has exited. A log
    growing inside the repo during a run changes the worktree digest mid-run
    and fails the manifest-identity ids as false positives (finding R-0176).
    Use `.remedy-wt/` for the live logs; it is gitignored and outside every
    tracked path.
4.  Evidence files carry `.txt` names and never `.log`: `.gitignore` drops
    `*.log` silently and the review-zip guard rejects any member matching
    `\.log$` (finding R-0169).
5.  The base worktree is created ON A THROWAWAY BRANCH, `git worktree add -b
    tmp/base-gate <path> a399a3304f9d962cd920c251488c40c486b35fdc`. The
    self-dogfood branch guard refuses a detached HEAD by design, so a detached
    base worktree fails the guard-dependent ids for a reason that has nothing
    to do with this branch (DECISION D3). The worktree AND the branch are both
    removed before the handback.
6.  The two suite runs are SERIAL — never two pytest processes at once. The
    runtime suites bind ports and a concurrent second process produces false
    reds.
7.  Every commit passes the AGENTS.md self-review loop and the Commit Gate, and
    the tree is clean after each. Commit subjects carry no leading-slash token,
    no absolute path and no secret-like string.
8.  Push after C4: `git push -u origin feature/f032-evidence-triple`. Create no
    pull request and merge nothing.
9.  Read `.agent/STOP` from disk twice — once before C0a and once before C4 —
    and report the exact command output both times. If it EXISTS at either
    reading, stop, write the handback, and end.
10. Where a command's exit code is needed and this session's shell refuses
    `$?`, chain `&& echo <MARKER>` and report whether the marker printed. Never
    report an exit code that was not observed.
11. NOTHING IN THIS ROUND MAY BE MADE GREEN BY EDITING A TEST. If the gate
    finds a reproducible branch-only failure coupled to this feature's code,
    that is a BLOCKER: stop, write the handback naming the id and the evidence,
    and end the round. The repair is its own reviewer-gated round.

----------

SPEC — what this round produces

S1. THE FRONTEND IS BUILT BEFORE THE BRANCH RUN, for reading (b). From
    `apps/ui`, run `npm run build`. Then prove the staleness is gone by
    importing `_frontend_is_stale` from `packages.orchestration.ui_server` and
    reporting that it returns `False`, together with the mtime of
    `apps/ui/dist/index.html` and of the newest file under `apps/ui/src`. If it
    still returns `True`, stop and report — a run started stale is not a gate.

S2. THE BRANCH RUN, then THE BASE RUN, in that order and serially, per
    docs/agents/integration_gate.md steps 1 and 2.

S3. BASE PARITY IS RESTORED BEFORE THE BASE RUN, and the restoration is
    MEASURED rather than asserted, per step 3 of that file. Copy the primary
    checkout's `apps/ui/node_modules` and `apps/ui/dist` INTO the base
    worktree with `shutil.copytree(src, dst, symlinks=True)`. THE
    `symlinks=True` ARGUMENT IS THE POINT AND IS NOT OPTIONAL: `copytree`
    defaults to `symlinks=False`, which DEREFERENCES npm's bin shims and itself
    causes base-only failures the parity exists to prevent (finding R-0591).
    Never symlink either directory into the worktree — the UI auto-build writes
    THROUGH such a symlink into the primary checkout. If this session's sandbox
    refuses to create a symlink inside the destination, report the exact
    refusal and continue to S4's attribution route instead of silently copying
    without it.

S4. THE AUTO-BUILD IS NEUTRALISED TWICE OVER FOR THE BASE RUN, because the env
    var alone has been ignored once before (finding R-0169). FIRST, after the
    copy, set `apps/ui/dist/index.html`'s mtime in the base worktree to NOW, so
    `_frontend_is_stale()` is False by construction against source files a
    fresh checkout stamped at checkout time; report the function's return value
    IN THE BASE WORKTREE and it must be `False`. SECOND, set
    `REMEDY_UI_NO_AUTO_BUILD=1` in the base run's environment. THIRD, verify by
    measuring the EVENT and not the outcome (finding R-0444): record the mtime
    of EVERY file under the base worktree's `apps/ui/dist` immediately before
    the base run and immediately after it, and report the run's start and end
    times. ANY mtime falling inside that window VOIDS the parity claim, and the
    verdict then requires per-id attribution of every base-only failure by
    direct evidence. A content hash may accompany the mtime reading but never
    replaces it, because equal content is consistent both with no rebuild and
    with a byte-identical one.

S5. THE COMPARISON, per step 3. Sort both FAILED lists. `comm -13
    base_failed.txt branch_failed.txt` is the BRANCH-ONLY set; `comm -23` is
    the set the branch FIXED or that fails only at base. Report both in full,
    never truncated — no `head`, no `tail` on either list.

S6. ATTRIBUTION OF EVERY BRANCH-ONLY ID, per step 4, one id at a time and none
    skipped. Re-run the exact node id SERIALLY. A serial PASS is the xdist
    flake class: record it, it is not a blocker. A serial FAIL is reproduced at
    the merge base before this feature is blamed. A reproducible branch-only
    failure coupled to this feature's code is a BLOCKER under constraint 11.
    Report, per id, which of the three it was and the evidence that decided it.

S7. EVERY BASE-ONLY ID IS ATTRIBUTED TOO whenever the parity claim did not hold
    on the mtime reading of S4, and the attribution names the missing artifact
    per id. This obligation is stated unconditionally for the ids themselves:
    if the parity claim DID hold and base-only ids nonetheless exist, they are
    still reported in full and still attributed, because a base-only failure
    with parity intact is a real base failure and is exactly what this gate
    must not swallow.

S8. THE EVIDENCE DIRECTORY. `.agent/gate_f032_r16/` is created with the file
    names reading (e) lists, carrying: the branch run's meta and raw tail and
    sorted FAILED list; the base run's parity record and sorted FAILED list;
    both `comm` outputs; the per-id attribution; and a provenance note saying
    where each full log lived while its run was in flight and when it was
    copied in. No file in it is a `.log`.

S9. THE SPEC AND THE BUNDLE AGREE. S1 to S7 are the work whose OUTPUT C3
    commits as S8's directory. Nothing in this SPEC is performed by a commit
    the Bundle does not list.

----------

SLICES

<<<SLICE PLANF032R16>>>
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
T003 is COMPLETE: the model carries the triple, the card renders it, and the
receipt chip is the entry point F023 wires. R16 is the integration gate of
docs/agents/integration_gate.md — the full suite on this branch and at the
merge base `a399a330` with artifact parity restored and measured, the two
failure sets compared, every branch-only id attributed. It writes no production
code. The frontend is REBUILT before the branch run, because R14 and R15 edited
`apps/ui/src` and a stale dist makes the suite rebuild itself mid-run.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R15 verdict and the reviewer's prose slip | ordered | the record is touched first |
| C3 the gate evidence directory | ordered | S1 to S8 |
| C4 the handback | ordered | |

## Next Steps
1. The closure sequence, part one: the evidence job and a FRESH review zip, per
   docs/roadmap/STATUS_closure_protocol.md.
2. The closure sequence, part two: the authored STATUS line committed last on
   the branch, then the pull request, which is NOT merged in this session.

## Risks
- A branch-only failure that reproduces serially and touches this feature's
  code is a blocker, not a repair to fold into this round; it would cost a
  reviewer-gated round of its own before closure can start.
- The base worktree carries neither `node_modules` nor `dist`, both gitignored.
  Parity is restored by copy and then MEASURED by an mtime window, because the
  environment variable that disables the auto-build has been ignored once.
<<<END PLANF032R16>>>

<<<SLICE LEDGER16>>>
Gate: F032 R15 — the F032 T003c ENTRY-POINT entry, and the close of T003. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran all eight itself at `2a872227`. TRANSPORT IS PROVED FROM A VALUE THE REVIEWER HELD BEFORE DELEGATING, which is the strongest shape this workflow can produce: sha256 `43605b6b924f123c59415e36f390bb4701644a0f8ab27b2751653ae7be5c9991` over 33459 bytes and 488 lines was computed on the scratch original `.remedy-wt/f032-r15.md` at authoring time, before the worker was delegated to, and the reviewer re-read that original after the handback and compared it BYTE FOR BYTE against the committed `.agent/authored/f032-r15.md` blob and the committed `.agent/last_block.md` blob: all three equal, the two committed paths being the SAME git blob `c365552eb6019179032ee5a61345acf4a5e24f93`. THAT CHAIN COVERS THE SCRATCH ORIGINAL, THE SAVED COPY AND THE MIRROR AND NOTHING MORE; under docs/agents/self_drive_protocol.md there is no paste relay and no claim about any prompt's bytes is made here. THE ROUND'S DESIGN MOVE IS THE ONE THAT MATTERS AND THE REVIEWER MEASURED THE GROUND IT RESTS ON RATHER THAN ACCEPTING IT: `docs/roadmap/features/T5_F032.md` makes the chips' deep link into the evidence panel part of Goal & Done, that panel is `docs/roadmap/features/T5_F023.md` T003, `docs/roadmap/STATUS.md` carries F023 as `[ ]` unclaimed, and the only detail surface in `apps/ui/src` is the per-task `DetailPopover` which `docs/ui/design_reference/component_spec.md` names the DetailPanel/EvidencePanel entry and which has no tab and no prop for a decision's evidence ref. So the destination genuinely does not exist, F032 depends on F031 and not on F023, and DECISION F032 D8 rules the honest half: an OPTIONAL `onOpenEvidence` handler, a receipt that is a `<button>` only when one is supplied and the `<span>` R14 shipped when none is, and a ref's `target` still reaching no markup. That is the pattern the canonical design reference itself prescribes for an entry point whose destination is unbuilt, and D8 records the rejected alternatives with a reversal recipe. WHAT THE REVIEWER MEASURED ITSELF, every number its own run: `npx tsc --noEmit` from `apps/ui` printed only the chained marker, so exit 0 with no output; `python3 -m pytest tests/ui_contracts/ -q` exit 0 at `580 passed, 4 skipped` against the `574 passed, 4 skipped` it had taken at `a4a24663`, so passed grew by exactly the six new guards and skipped did not move; the golden-path canary exit 0 at `42 passed`; the docs gate, owed because this round's change set includes `docs/roadmap/`, exit 0 at `295 passed`; the PLAN byte-equal to slice `PLANF032R15` extracted from the committed C0a blob `True` with the trailing-newline negative control `False` at 45 lines; and all three appends byte-identical to base plus one newline plus their slice with the base a byte PREFIX in each case — `.agent/live_review.md` 1096449 + 1 + 5039 = 1101489 at one paragraph, `.agent/decisions.md` 645690 + 1 + 4286 = 649977 at six paragraphs, and `docs/roadmap/features/T5_F032.md` 10538 + 1 + 1189 = 11728 at one paragraph — each structural reader matching the file's last N units against the slice's N paragraphs IN ORDER. THE OPEN SET IS UNMOVED AND WAS RECOMPUTED RATHER THAN CARRIED: 274 registered minus 24 resolved gives 250 open, maximum `R-0713`, ids added to either set `[]`, while `^Gate: F\d+ R\d+ — ` gained exactly the `F032 R14` key and `^## DECISION F032 D\d+ ` went 7 to 8 adding exactly `DECISION F032 D8`. THE REVIEWER RAN TWO MUTATIONS OF ITS OWN CHOOSING, neither ordered by the block, in a disposable worktree at `2a872227`, each exact byte string counted 1 in its named file before it was applied: adding `cursor: pointer` to the SHARED `.decisionEvidenceChip` rule in `apps/ui/src/components/panels/RightLivePanel.module.css` gave exit 1 at `1 failed, 54 passed` naming `test_the_pressable_receipt_shows_where_the_keyboard_is`; and replacing the discriminator `onOpenEvidence ? (` with `true ? (` in `apps/ui/src/components/panels/DecisionInboxCard.tsx`, which is the mutation that makes the inert chip pressable and is the exact dishonesty D8 exists to prevent, gave exit 1 at `1 failed, 54 passed` naming `test_a_card_with_no_handler_still_renders_the_plain_chip`. The controls before the first mutation and after both restorations were a real exit 0 at `55 passed`, the worktree's `git status --porcelain` 0 lines, and it was removed and pruned. SO THE HONESTY PROPERTY IS PINNED AND NOT MERELY ASSERTED. THE WORKER'S DEVIATION 2 IS ACCEPTED AND IS BETTER THAN WHAT THE BLOCK ORDERED: item S5 said only that the span case must stay untouched, and the worker scoped its three new rules to `button.decisionEvidenceChip` rather than writing them on the shared class, leaving `.decisionEvidenceChip` byte-unchanged so no pointer cursor or hover border can dress the inert arm as a control. The reviewer's first mutation above is the guard that now pins exactly that. ONE EXTRA COMMIT WAS MADE AND DECLARED, `2a872227`, repairing a false unmeasured sentence about `.remedy-wt/` in the handback the previous commit had written. The sentence was not load-bearing, so under amend0827 rule 2 it earns no id; but the F032 R12 entry of this record already carries a clause BINDING ON THE NEXT BLOCK THAT ORDERS A HANDBACK, that a false numeral in `.agent/handoff.md` is corrected by a deviation line in the NEXT handback and never by a commit of its own, and the R15 block did not carry that clause forward to the worker. THAT OMISSION IS THE REVIEWER'S AND IS RECORDED IN `.agent/prose_slips.md` FOR THIS ROUND; the worker's commit is accepted as declared, and the clause is carried explicitly in the R16 block. NOTHING ELSE MOVED: `git diff --name-only a4a24663..2a872227` is exactly the block's change set, `packages/` and `apps/ui/src/api/` EMPTY across the whole range, per-commit insertions 488, 464, 21, 2, 83, 65, 126, 126 and 16 each single-parent and each under 500, markers 0 in every written file against a control of 8 over the C0a blob, `git ls-files .remedy-wt` 0 lines, `git worktree list` one line, `git branch --list "tmp/*"` empty, the remote tip equal to the local tip and the Open PR Gate `[]`. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END LEDGER16>>>

<<<SLICE SLIP16>>>
- 2026-08-28 · F032 R15 · The block did not carry forward the clause the F032
  R12 gate entry had labelled binding on the next block ordering a handback —
  that a false numeral in `.agent/handoff.md` is repaired by a deviation line
  in the NEXT handback rather than by a commit of its own — so the worker,
  finding an unmeasured sentence in its own committed handback, spent a ninth
  commit repairing it and declared the write-once breach itself. Nothing on
  disk under `packages/`, `apps/`, `tests/` or `docs/` was wrong, so no id was
  spent; the clause is quoted in the R16 block instead.
<<<END SLIP16>>>

----------

DONE WHEN — the gates, in this order

Every gate is EXECUTED and its real output recorded. "Green" as a word is a
finding. Each gate runs at a commit strictly earlier than C4, so the handback
can quote all of them; C4's own numbers are not gated and are not owed.

G1 HYGIENE, BASE, SENTINEL. `git rev-parse HEAD` before C0a — REPORT it and
   confirm it equals the base this block names. `git rev-parse --abbrev-ref
   HEAD` is `feature/f032-evidence-triple`. `git status --porcelain | wc -l` is
   `0` after each of C0a, C0b, C1, C2 and C3. `ls -la .agent/STOP` before C0a
   and again before C4 — report the exact output of both.

G2 TRANSPORT. One digest comparison, disk to disk. Report `sha256sum` over the
   reviewer's gitignored scratch original `.remedy-wt/f032-r16.md`, over
   `.agent/authored/f032-r16.md` at C0a and over `.agent/last_block.md` at C0b —
   all three equal — plus the git blob id of the two committed paths, which must
   be one blob. That chain covers the original, the copy and the mirror, and
   makes no claim about any prompt's bytes.

G3 EXTRACTION AND CAPS, measured on the COMMITTED C0a blob. Report the content
   line count of EACH slice region found and how many regions there were, the
   block's TOTAL line count, and PROSE as TOTAL minus the content total. PROSE
   must be under 400 and TOTAL under 490.

G4 THE PLAN, at C1. `.agent/plan.md` is byte-equal to slice PLANF032R16
   extracted from the committed C0a blob — report `True`. NEGATIVE CONTROL: the
   same comparison with the slice's trailing newline removed — report `False`.
   Report `wc -l`, which must be under 50, and the counts of `^## Goal$` and
   `^## Next Steps$`, one each.

G5 THE APPENDS, at C2, each read with `git show <base-sha>:<path>` so no
   tracked file is ever overwritten to get a baseline. For EACH of
   `.agent/live_review.md` and `.agent/prose_slips.md`: READER (a), byte
   identity — the post-commit bytes equal the pre-commit bytes plus one newline
   plus the slice — report `True`, the arithmetic as three numbers summing to
   the result, and that the pre-commit blob is a byte PREFIX. READER (b),
   structural — count N, the number of blank-line-separated paragraphs in the
   slice, and compare the LAST N blank-line units of the post-commit file
   against the slice's N paragraphs IN ORDER; report N and the result. NEGATIVE
   CONTROL for each: flip one byte IN MEMORY inside the FIRST appended
   paragraph and report that BOTH readers reject it. Then report, before and
   after C2, the counts of `^Gate: F\d+ R\d+ — `, `^- R-\d+ — `,
   `^Done: R-\d+ — ` and `^Landed: R-`, the size of the open set, the maximum
   id, and the lists of gate keys and ids ADDED. The reviewer measured the open
   set at 250 and the maximum at `R-0713`; this round registers and resolves
   nothing, so both must be unmoved.

G6 THE BRANCH RUN, at C2, after S1's build. Report the build command's exit
   marker, `_frontend_is_stale()` returning `False` with the mtimes S1 names,
   and then `python3 -m pytest -n auto -q` from the repository root:
   exit code, wall time, the raw tail, and the COMPLETE sorted `^FAILED` list
   with no truncation of any kind. State where the full log lived while the run
   was in flight.

G7 THE BASE RUN, at C2, serially after G6. Report the worktree creation command
   including its `-b tmp/base-gate` argument; the parity copy with its
   `symlinks=True` argument named; `_frontend_is_stale()` returning `False`
   INSIDE the base worktree; the base run's own exit code, wall time, raw tail
   and COMPLETE sorted `^FAILED` list; and the MTIME WINDOW of S4 — the run's
   start and end times against the before-and-after mtimes of every file under
   the base worktree's `apps/ui/dist`, with an explicit statement of whether
   any mtime fell inside the window and therefore whether the parity claim
   HOLDS or is VOID. Then remove the worktree, delete `tmp/base-gate`, and
   report `git worktree list` and `git branch --list "tmp/*"`.

G8 THE COMPARISON, THE ATTRIBUTION AND THE PR GATE, at C3. Report the complete
   `comm -13` branch-only set and the complete `comm -23` base-only set, both
   untruncated. Report the per-id attribution S6 and S7 require, one line per
   id, naming for each which class decided it and on what evidence; state
   plainly whether any id is a BLOCKER under constraint 11. Report the file
   names actually written under `.agent/gate_f032_r16/` and that none matches
   `\.log$`. Report `git diff --name-only 2a872227..<C3>`, which is exactly the
   Change set less `.agent/handoff.md` — report BOTH residues. Report `git diff
   --stat 2a872227..<C3> -- packages/ apps/ tests/ docs/`, which must be EMPTY.
   Report the insertion count of every commit from C0a through C3, each
   single-parent and each under 500, compared cell by cell against the `+/-`
   column of the handback's `## Commits` table. Report `git ls-files
   .remedy-wt`, `git worktree list`, `git branch --list "tmp/*"`, and `gh pr
   list --state open --json number,headRefName,baseRefName,isDraft`.

----------

HANDBACK

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It has no
length cap; it is valid when its mandated sections are present. It carries: the
feature and round, the SESSION NUMBER — this is SESSION 4 of F032, whose rounds
so far are R1 to R5 in session 1, R6 to R9 in session 2, R10 to R14 in session
3, and R15 and R16 in this one — the branch, the base and every commit SHA, a
per-commit changed-files table with the `+/-` column, ONE LINE PER GATE G1 to
G8 carrying its real readings, the item-status table covering C0a to C4 and S1
to S9 with every item present exactly once, the open-findings count, the
deviations and assumptions, and the next expected action. State plainly that no
pull request was created and nothing was merged.

WRITE THIS FILE ONCE. `.agent/handoff.md` is rewritten in full every round and
is not an append-only record, so if a sentence in it turns out to be false, the
repair is a deviation line in the NEXT round's handback and NEVER a commit of
its own — that clause is carried here from the F032 R12 entry of
`.agent/live_review.md`, which labelled it binding on the next block ordering a
handback. Measure every numeral before writing it, and state no count you did
not count.
