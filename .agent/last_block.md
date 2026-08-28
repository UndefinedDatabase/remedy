STEP INTEGRATION GATE / F032 — ROUND R17 — the full suite, twice, with parity

BASE. This block is authored against `c1e208334cd8c7c0cef0a0ae3e5a1e63a4dc65d5`,
the tip of `feature/f032-evidence-triple` and the handback of R16. Every reading
below was taken there by the reviewer unless another SHA is named.

FRAME CONVENTION. Every rule line in this block is exactly ten hyphens, and no
other line is a run of one repeated character. Nothing in the frame is
appliable: the appliable bytes are the slices, each proved against its own
target by its own gate.

----------

GOAL

Run the integration gate of docs/agents/integration_gate.md for F032, which R16
could not start: the full suite on this branch, the full suite at the merge base
with artifact parity restored and measured, the two failure sets compared, and
every branch-only id attributed. This round writes NO production code. Its
product is the evidence directory and an honest verdict about whether this
branch may proceed to closure.

----------

WHY R16 STOPPED, AND WHAT CHANGED

R16 was ordered to build the frontend before the branch run. It could not: this
session's permission layer denied `npm run build` in every form the worker
tried, while `npm --version` and `node --version` both answered normally. The
worker did the right thing — it refused both available substitutes, because
`REMEDY_UI_NO_AUTO_BUILD=1` would have gated a pre-R14 `dist` and touching
`index.html`'s mtime would have falsified the staleness predicate while leaving
stale bytes on disk, and each makes the gate green about something it did not
test. It stopped and handed back, which is guardrail G8 working as designed.

THE REVIEWER HAS SINCE PERFORMED THAT BUILD ITSELF, and this block states it
plainly because a later reader must not have to guess who ran what. From
`apps/ui`, `npm run build` — `vite v6.4.2`, `986 modules transformed`, `built in
1.35s`, emitting `dist/index.html`, `dist/assets/index-D0y3OK7n.css` and
`dist/assets/index-D_a-qpxM.js`. It is available to the reviewer's session and
was not available to the worker's; that asymmetry is the whole of the change.

This is a GITIGNORED BUILD ARTIFACT and not a change to the work tree. `git
check-ignore -v` resolves `apps/ui/dist` to `.gitignore` line 13, `git status
--porcelain` is 0 lines after the build, and nothing reviewable was authored by
the reviewer: the artifact is derived from committed source and reproducible by
anyone holding the toolchain. THE WORKER STILL MEASURES IT RATHER THAN TAKING
THE REVIEWER'S WORD, which is what S1 below is for — the gate's evidence comes
from the worker's own readings, as it does for every other gate.

----------

WHAT THE REVIEWER READ AND MEASURED BEFORE ORDERING ANY OF THIS

(a) `git merge-base HEAD main` is
    `a399a3304f9d962cd920c251488c40c486b35fdc`, which is also the commit
    `.agent/plan.md` names as this branch's cut point. That is the base run's
    commit.
(b) THE FRONTEND IS NOW CURRENT IN THE PRIMARY CHECKOUT.
    `packages/orchestration/ui_server.py` defines `_frontend_is_stale()` at line
    3050: it returns True when ANY file under `apps/ui/src` has an mtime newer
    than `apps/ui/dist/index.html`. Measured at the base AFTER the reviewer's
    build: `dist/index.html` carries `Fri Aug 28 02:46:30 2026` while the newest
    source file, `apps/ui/src/components/panels/RightLivePanel.module.css`,
    carries `Fri Aug 28 02:25:15 2026`, and `_frontend_is_stale()` returns
    `False`. Line 3141 of that module reaches `_auto_build_frontend` only on the
    True branch, so no run started now rebuilds `dist` mid-run — which is the
    condition findings R-0169 and R-0176 exist to prevent, and the condition R16
    correctly refused to fake.
(c) `apps/ui/dist` and `apps/ui/node_modules` both EXIST in the primary
    checkout and are both gitignored — `git check-ignore -v` resolves them to
    `.gitignore` lines 13 and 221. A fresh worktree therefore carries NEITHER,
    which is precisely the environment class step 3 of
    docs/agents/integration_gate.md exists to neutralise.
(d) `.agent/gate_f255_r18/` is the most recent gate evidence directory and its
    file names are `attribution.txt`, `base_failed.txt`, `base_parity.txt`,
    `branch_failed.txt`, `branch_meta.txt`, `branch_run_tail.txt`,
    `comm_base_only_failures.txt`, `comm_branch_only_failures.txt` and
    `full_log_provenance.txt`. This round reuses those names exactly rather
    than inventing a second vocabulary.
(e) `.agent/live_review.md` at the base, read mechanically: 274 paragraphs
    matching `^- R-\d+ — `, 24 lines matching `^Done: R-\d+ — `, so the OPEN
    SET is 250 and the maximum id is `R-0713`. Its newest `^Gate: F\d+ R\d+ — `
    key is `F032 R15`.
(f) `.agent/plan.md` at the base is NOT the PLANF032R16 slice: R16's declared
    extra commit `87d56883` rewrote it to record the blocker, as AGENTS.md "If
    Blocked" step 2 requires. PLANF032R17 below replaces whatever is there.
(g) THE WORKER'S TOOLCHAIN MAY STILL BE DENIED, and this round needs none of
    it. No item below runs `npm`, `npx`, `node` or `vite`. If any command a
    worker reaches for requires them, that is a sign it has left this block.
(h) R16 REGISTERED NO FINDING AND ITS BLOCKER GOT NO ID, correctly: an
    environment permission is not wrong state on disk under `packages/`,
    `apps/`, `tests/` or `docs/`, and under operator amendment amend0827 rule 2
    an R-id is reserved for a defect with product effect. The open set was
    searched for the defect before that call was made and holds none like it.

----------

BUNDLE

C0a  save this block verbatim to `.agent/authored/f032-r17.md`
C0b  mirror the same bytes over `.agent/last_block.md`
C1   `.agent/plan.md`, slice PLANF032R17 applied whole
C2   `.agent/live_review.md`, slice LEDGER17 appended
C3   the gate evidence directory `.agent/gate_f032_r17/`
C4   the handback

CHANGE SET. Exactly these paths, and nothing else is created, edited or
deleted: `.agent/authored/f032-r17.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, the files of
`.agent/gate_f032_r17/` named in G8, and `.agent/handoff.md`. NO file under
`packages/`, `apps/`, `tests/` or `docs/` is edited this round, and no build is
run, so `apps/ui/dist` is not rewritten either.

----------

CONSTRAINTS

1.  A slice is applied BYTE FOR BYTE. It is never retyped from memory, never
    reflowed, never trimmed and never corrected — if a slice looks wrong, apply
    it as given and say so in the handback's deviations.
2.  SLICE CONVENTION. A slice begins at the line after `<<<SLICE NAME>>>` and
    ends at the line before `<<<END NAME>>>`. The slice's bytes are those lines
    including the newline that ends the last of them. Extract them
    PROGRAMMATICALLY from the committed C0a blob — `git show
    <C0a>:.agent/authored/f032-r17.md` — never by retyping from this prompt.
    PLANF032R17 REPLACES `.agent/plan.md` whole. LEDGER17 is an APPEND: the
    target's existing bytes, then exactly one newline, then the slice.
3.  RUN LOGS ARE WRITTEN OUTSIDE THE REPOSITORY WORKTREE WHILE A SUITE RUNS and
    copied into `.agent/gate_f032_r17/` only after the run has exited. A log
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
7.  NO BUILD IS RUN THIS ROUND, by you or by anything you start. You do not
    need `npm`, `npx`, `node` or `vite` for any item below; the reviewer has
    already built the frontend and S1 only MEASURES the result. If something
    you are about to run would invoke them, stop and report rather than
    improvising.
8.  Every commit passes the AGENTS.md self-review loop and the Commit Gate, and
    the tree is clean after each. Commit subjects carry no leading-slash token,
    no absolute path and no secret-like string.
9.  Push after C4: `git push -u origin feature/f032-evidence-triple`. Create no
    pull request and merge nothing.
10. Read `.agent/STOP` from disk twice — once before C0a and once before C4 —
    and report the exact command output both times. If it EXISTS at either
    reading, stop, write the handback, and end.
11. Where a command's exit code is needed and this session's shell refuses
    `$?`, chain `&& echo <MARKER>` and report whether the marker printed. Never
    report an exit code that was not observed.
12. NOTHING IN THIS ROUND MAY BE MADE GREEN BY EDITING A TEST. If the gate
    finds a reproducible branch-only failure coupled to this feature's code,
    that is a BLOCKER: stop, write the handback naming the id and the evidence,
    and end the round. The repair is its own reviewer-gated round.

----------

SPEC — what this round produces

S1. THE FRONTEND'S CURRENCY IS MEASURED, NOT ASSUMED AND NOT REBUILT. Import
    `_frontend_is_stale` from `packages.orchestration.ui_server` and report its
    return value, which must be `False`; report the mtime of
    `apps/ui/dist/index.html`, the path and mtime of the NEWEST file under
    `apps/ui/src`, and the file names present under `apps/ui/dist/assets`,
    which must be the two the reviewer's build emitted and which reading (b)
    names. If the function returns `True`, STOP and report — a run started
    stale is not a gate, and the answer is a fresh session, never a substitute.

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
    IN THE BASE WORKTREE and it must be `False`. This is legitimate there and
    was not in the primary checkout, and the difference is worth stating: the
    base worktree's `dist` holds the bytes the primary's build really produced,
    so the mtime is being corrected to match content that is genuinely current
    for those sources, whereas in the primary the same touch would have
    asserted currency about bytes that predated two rounds of edits. SECOND,
    set `REMEDY_UI_NO_AUTO_BUILD=1` in the base run's environment. THIRD,
    verify by measuring the EVENT and not the outcome (finding R-0444): record
    the mtime of EVERY file under the base worktree's `apps/ui/dist`
    immediately before the base run and immediately after it, and report the
    run's start and end times. ANY mtime falling inside that window VOIDS the
    parity claim, and the verdict then requires per-id attribution of every
    base-only failure by direct evidence. A content hash may accompany the
    mtime reading but never replaces it, because equal content is consistent
    both with no rebuild and with a byte-identical one.

S5. THE COMPARISON, per step 3. Sort both FAILED lists. `comm -13
    base_failed.txt branch_failed.txt` is the BRANCH-ONLY set; `comm -23` is
    the set the branch FIXED or that fails only at base. Report both in full,
    never truncated — no `head`, no `tail` on either list.

S6. ATTRIBUTION OF EVERY BRANCH-ONLY ID, per step 4, one id at a time and none
    skipped. Re-run the exact node id SERIALLY. A serial PASS is the xdist
    flake class: record it, it is not a blocker. A serial FAIL is reproduced at
    the merge base before this feature is blamed. A reproducible branch-only
    failure coupled to this feature's code is a BLOCKER under constraint 12.
    Report, per id, which of the three it was and the evidence that decided it.

S7. EVERY BASE-ONLY ID IS ATTRIBUTED TOO. This obligation is unconditional: if
    the parity claim HELD on S4's mtime reading and base-only ids nonetheless
    exist, they are still reported in full and still attributed, because a
    base-only failure with parity intact is a real base failure and is exactly
    what this gate must not swallow. Where parity did NOT hold, the attribution
    additionally names the missing or rewritten artifact per id.

S8. THE EVIDENCE DIRECTORY. `.agent/gate_f032_r17/` is created with the file
    names reading (d) lists, carrying: the branch run's meta and raw tail and
    sorted FAILED list; the base run's parity record and sorted FAILED list;
    both `comm` outputs; the per-id attribution; and a provenance note saying
    where each full log lived while its run was in flight, when it was copied
    in, and that the frontend build behind these runs was performed by the
    reviewer before the round rather than by this worker. No file in it is a
    `.log`.

S9. THE SPEC AND THE BUNDLE AGREE. S1 to S7 are the work whose OUTPUT C3
    commits as S8's directory. Nothing in this SPEC is performed by a commit
    the Bundle does not list.

----------

SLICES

<<<SLICE PLANF032R17>>>
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
T003 is COMPLETE. R17 is the integration gate of docs/agents/integration_gate.md,
which R16 could not start because its session was denied `npm run build` and it
refused to fake the precondition. The reviewer has since built the frontend, so
`_frontend_is_stale()` is False and no run rebuilds `dist` mid-flight. R17 runs
the full suite on this branch and at the merge base `a399a330` with artifact
parity restored and MEASURED by an mtime window, compares the failure sets and
attributes every branch-only id. It writes no production code and runs no build.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R16 verdict | ordered | the record is touched first |
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
<<<END PLANF032R17>>>

<<<SLICE LEDGER17>>>
Gate: F032 R16 — the F032 integration-gate attempt that correctly refused to run. THE ROUND DID NOT COMPLETE ITS ORDERED WORK AND THAT IS THE RIGHT OUTCOME, so this entry records an INCOMPLETE round rather than a pass or a failure, and no finding id is spent. S1 of the R16 block ordered the frontend rebuilt before the branch run and ruled that a run started stale is not a gate; this session's permission layer denied `npm run build` in every form the worker tried — the `apps/ui` working directory, `npm --prefix`, the local `vite` binary, `npx vite build` and `node`'s direct invocation of `vite.js` — each answering `Permission to use Bash has been denied`, while `npm --version` printed `10.9.7` and `node --version` printed `v22.22.2` in the same session, so the denial was specific to the build and not to the toolchain's existence. THE WORKER REFUSED BOTH AVAILABLE SUBSTITUTES AND WAS RIGHT TO: setting `REMEDY_UI_NO_AUTO_BUILD=1` for the branch run would have gated a `dist` predating R14 and R15, and touching `dist/index.html`'s mtime would have made `_frontend_is_stale()` return False while the stale bytes stayed on disk. Each makes the gate green about something it did not test, which is the defect an integration gate exists to prevent rather than to commit. It started NEITHER suite, created NO base worktree, made NO parity claim, and deliberately did not create `.agent/gate_f032_r16/`, on the ground that a gate-named evidence directory with no run behind it is false evidence — the reviewer agrees and records that judgement here as the correct general rule. WHAT R16 DID COMMIT IS ENTIRELY CORRECT AND THE REVIEWER RE-VERIFIED ALL OF IT at `c1e20833`. TRANSPORT IS PROVED FROM A VALUE THE REVIEWER HELD BEFORE DELEGATING: sha256 `5b3d7191b0950308df76e24efddcb5ca57301afaa2da9aa1ba3e2add7bbf40e0` over 28170 bytes and 382 lines was computed on the scratch original `.remedy-wt/f032-r16.md` at authoring time, and that original, the committed `.agent/authored/f032-r16.md` blob and the committed `.agent/last_block.md` blob are all three byte-equal, the two committed paths being one git blob. That chain covers the original, the saved copy and the mirror and claims nothing about any prompt's bytes. THE PLAN AT `10f5c5bc` is byte-equal to slice `PLANF032R16` extracted from the committed C0a blob, `True`, with the trailing-newline negative control `False`, at 44 lines. BOTH APPENDS AT `c71ddde7` are byte-identical to base plus one newline plus their slice with the base a byte PREFIX: `.agent/live_review.md` 1101489 + 1 + 6398 = 1107888 and `.agent/prose_slips.md` 2328 + 1 + 604 = 2933. THE OPEN SET IS UNMOVED, recomputed rather than carried: 274 registered minus 24 resolved gives 250 open, maximum `R-0713`, ids added to either set `[]`, and `^Gate: F\d+ R\d+ — ` gained exactly the `F032 R15` key. THE ONE EXTRA COMMIT, `87d56883`, rewrote `.agent/plan.md` to record the blocker and is exactly what AGENTS.md "If Blocked" step 2 requires; its path was already in the round's change set, so no scope was widened, and `.agent/handoff.md` was written exactly once, which is the clause the R15 entry carried forward and the R16 block quoted. NOTHING ELSE MOVED: `git diff --stat 2a872227..87d56883 -- packages/ apps/ tests/ docs/` EMPTY, `git ls-files .remedy-wt` 0 lines, `git worktree list` one line, `git branch --list "tmp/*"` empty, the remote tip equal to the local tip and the Open PR Gate `[]`. THE BLOCKER EARNS NO FINDING ID: a permission this session withholds is not wrong state on disk under `packages/`, `apps/`, `tests/` or `docs/`, and under operator amendment amend0827 rule 2 an id is reserved for a defect with product effect. THE REVIEWER HAS SINCE RUN THE BUILD ITSELF, from `apps/ui`, `vite v6.4.2` transforming 986 modules in 1.35s and emitting `dist/index.html`, `dist/assets/index-D0y3OK7n.css` and `dist/assets/index-D_a-qpxM.js`; `apps/ui/dist` is gitignored at `.gitignore` line 13 and `git status --porcelain` stayed 0 lines, so no tracked file changed and nothing reviewable was authored by the reviewer. `_frontend_is_stale()` now returns `False` against `dist/index.html` at `Fri Aug 28 02:46:30 2026` and a newest source file at `Fri Aug 28 02:25:15 2026`. THE GATE IS RE-ORDERED AS R17 WITH THAT PRECONDITION REMOVED AND ITS MEASUREMENT KEPT: the worker still reads `_frontend_is_stale()` for itself rather than taking this entry's word for it. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change — the round claimed less than it was asked for and proved exactly what it claimed.
<<<END LEDGER17>>>

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
   reviewer's gitignored scratch original `.remedy-wt/f032-r17.md`, over
   `.agent/authored/f032-r17.md` at C0a and over `.agent/last_block.md` at C0b —
   all three equal — plus the git blob id of the two committed paths, which must
   be one blob. That chain covers the original, the copy and the mirror, and
   makes no claim about any prompt's bytes.

G3 EXTRACTION AND CAPS, measured on the COMMITTED C0a blob. Report the content
   line count of EACH slice region found and how many regions there were, the
   block's TOTAL line count, and PROSE as TOTAL minus the content total. PROSE
   must be under 400 and TOTAL under 490.

G4 THE PLAN, at C1. `.agent/plan.md` is byte-equal to slice PLANF032R17
   extracted from the committed C0a blob — report `True`. NEGATIVE CONTROL: the
   same comparison with the slice's trailing newline removed — report `False`.
   Report `wc -l`, which must be under 50, and the counts of `^## Goal$` and
   `^## Next Steps$`, one each.

G5 THE APPEND, at C2, read with `git show <base-sha>:<path>` so no tracked file
   is ever overwritten to get a baseline. READER (a), byte identity — the
   post-commit bytes of `.agent/live_review.md` equal the pre-commit bytes plus
   one newline plus the slice — report `True`, the arithmetic as three numbers
   summing to the result, and that the pre-commit blob is a byte PREFIX. READER
   (b), structural — count N, the number of blank-line-separated paragraphs in
   the slice, and compare the LAST N blank-line units of the post-commit file
   against the slice's N paragraphs IN ORDER; report N and the result. NEGATIVE
   CONTROL: flip one byte IN MEMORY inside the FIRST appended paragraph and
   report that BOTH readers reject it. Then report, before and after C2, the
   counts of `^Gate: F\d+ R\d+ — `, `^- R-\d+ — `, `^Done: R-\d+ — ` and
   `^Landed: R-`, the size of the open set, the maximum id, and the lists of
   gate keys and ids ADDED. The reviewer measured the open set at 250 and the
   maximum at `R-0713`; this round registers and resolves nothing, so both must
   be unmoved.

G6 THE BRANCH RUN, at C2, after S1's measurement. Report `_frontend_is_stale()`
   returning `False`, the mtimes and the asset file names S1 names, and then
   `python3 -m pytest -n auto -q` from the repository root: exit code, wall
   time, the raw tail, and the COMPLETE sorted `^FAILED` list with no
   truncation of any kind. State where the full log lived while the run was in
   flight.

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
   plainly whether any id is a BLOCKER under constraint 12. Report the file
   names actually written under `.agent/gate_f032_r17/` and that none matches
   `\.log$`. Report `git diff --name-only c1e20833..<C3>`, which is exactly the
   Change set less `.agent/handoff.md` — report BOTH residues. Report `git diff
   --stat c1e20833..<C3> -- packages/ apps/ tests/ docs/`, which must be EMPTY.
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
3, and R15, R16 and R17 in this one — the branch, the base and every commit
SHA, a per-commit changed-files table with the `+/-` column, ONE LINE PER GATE
G1 to G8 carrying its real readings, the item-status table covering C0a to C4
and S1 to S9 with every item present exactly once, the open-findings count, the
deviations and assumptions, and the next expected action. State plainly that no
pull request was created and nothing was merged.

WRITE THIS FILE ONCE. `.agent/handoff.md` is rewritten in full every round and
is not an append-only record, so if a sentence in it turns out to be false, the
repair is a deviation line in the NEXT round's handback and NEVER a commit of
its own — that clause is carried here from the F032 R12 entry of
`.agent/live_review.md`, which labelled it binding on the next block ordering a
handback. Measure every numeral before writing it, and state no count you did
not count.
