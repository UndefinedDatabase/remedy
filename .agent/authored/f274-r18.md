STEP — F274 ROUND 18 — the integration gate: the full suite on the branch, the full suite at the base, and the two failure sets compared

Goal: run the dedicated integration-gate round docs/roadmap/STATUS_closure_protocol.md precondition
2 requires to have PASSED before F274 can close, following docs/agents/integration_gate.md. THIS
ROUND MEASURES AND DOES NOT REPAIR: no file outside `.agent/` changes, no test is deleted, no
assertion is weakened, and a branch-only failure is a handback that says so rather than a fix
smuggled into a measuring round. It also books round 17's PASS verdict and writes the one dated
prose slip that round declared.

Base commit for every reading in this block: `4f3f0b8f`.

TWO DIFFERENT BASES ARE IN PLAY THIS FEATURE AND THEY ARE NOT THE SAME VALUE. Confusing them is
the R-0530 class, so both are stated here and each is used for exactly one purpose.
  THE GATE BASE, used by G5 and by nothing else, is `d0d8b24da2a080ebcff85e63e73a547e6a8066e6` —
  `git merge-base HEAD origin/main`, which is `origin/main`'s own tip, because this branch merged
  `main` IN at `f85200e4`. It is the right base for THIS gate's question, which is whether the
  BRANCH's own commits introduce a failure: everything between the fork point and that commit is
  main's accepted work and blaming it on F274 would be wrong.
  THE PACKAGE BASE, which this round does NOT use and which the CLOSURE round will, is the FORK
  POINT `13dfaabd93d7b6452a1d23ca698e29ed47ecf035`. Measured by the reviewer at `4f3f0b8f`:
  `rev-list --ancestry-path 13dfaabd..` and `rev-list 13dfaabd..` BOTH return 143, which is the
  equality docs/roadmap/STATUS_closure_protocol.md pitfall (e) requires of a package base, while
  the gate base returns 128 and 136 — unequal, and therefore wrong for a package and right here.

TWO OPEN FINDINGS BIND THIS BLOCK AND BOTH ARE APPLIED RATHER THAN DECLINED (§3 item 34).
  R-0736, Medium, OPEN: `docs/agents/integration_gate.md` step 3 restores base parity by COPYING
  `apps/ui/dist`, and `copytree` preserves the SOURCE mtimes while `git worktree add` stamps every
  checked-out file with the checkout time — so `_frontend_is_stale` fires, the UI is never built,
  and 114 `tests/ui_server/` ids fail with `React UI not built.` on every run that follows the
  recipe literally. R-0736's fix clause is ORDERED IN FULL by G5 below: after copying, stamp the
  dist tree NEWER than the newest file under `apps/ui/src`. The reviewer ran the gate base with
  that clause applied before authoring and measured ZERO occurrences of that marker.
  R-0645, Low, OPEN: the branch-only set derived from ONE run of a command whose failure set is not
  stable is a per-run SAMPLE, and a reviewer re-run once found two ids a worker run did not. The
  counter-measure is not a bigger number in this block; it is that the REVIEWER independently
  re-runs BOTH halves, so the classification rests on two runs by two actors. That is stated here
  so the verdict can say which property it rests on.
  R-0591's argument is ordered too, in the same call: `shutil.copytree(src, dst, symlinks=True)`.
  The default dereferences npm's bin shims and manufactures base-only failures of its own; the
  property that must survive is the SYMLINK, so the argument is named rather than the function.

WHAT THE REVIEWER RAN BEFORE AUTHORING, so the figures below are reference values a correct round
reproduces rather than predictions. THE BRANCH HALF at `4f3f0b8f` in the primary checkout: exit 0,
19767 passed, 23 skipped, 1 warning, 118.71s, FAILED count 0. THE BASE HALF at
`d0d8b24da2a080ebcff85e63e73a547e6a8066e6` in a throwaway worktree with parity restored as G5
orders it: exit 0, 19790 passed, 23 skipped, 1 warning, 141.34s, FAILED count 0, ZERO
`React UI not built.` markers, and no file under `apps/ui/dist` changed mtime during the run.
BOTH FAILURE SETS ARE EMPTY, so both `comm` sets are empty by construction. The branch carries 23
FEWER tests than the base, which is what a deletion feature should read like and is explained in
G6.

FRAME CONVENTION. Every slice is delimited by a line reading `BEGIN <NAME> sha256=<hex> bytes=<n>`
and a line reading `END <NAME>`; the slice is the bytes BETWEEN those two lines — its leading
newline INCLUDED and its trailing newline INCLUDED, the terminal byte being exactly what round
17's convention left unstated — and marker lines never reach any file. No line of this block's
FRAME is a run of a single repeated character.


## Bundle — the commits of this round, in this order

C0a  Save this block verbatim as `.agent/authored/f274-r18.md`.
C0b  Mirror the same bytes into `.agent/last_block.md`.
C1   Replace `.agent/plan.md` with the PLAN18 slice.
C2   Append the RECORD18 slice to `.agent/live_review.md` — books round 17's PASS verdict.
C3   Append the SLIP18 slice to `.agent/prose_slips.md` — the one dated line round 17 declared.
C4   THE GATE: run both halves, write the evidence files under `.agent/gate_f274_r18/`, commit
     that directory. ONE commit, and the ONLY commit of this round that adds a new path.
C5   The handback: rewrite `.agent/handoff.md`, then push.

C1 is the first substantive commit because this round touches the finding ledger and the plan must
be current before every commit (§3 item 23). C2 precedes C3 because the verdict is what the slip
belongs to.


## Change set — these paths and nothing else

  .agent/authored/f274-r18.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/prose_slips.md
  .agent/gate_f274_r18/
  .agent/handoff.md


## C4 — the evidence directory

Write these files under `.agent/gate_f274_r18/`, all with `.txt` names and never `.log`, because
`.gitignore` drops `*.log` silently and the review-zip guard rejects any member matching `\.log$`
(R-0169). Their CONTENT is measured, not authored — the block dictates the filenames and what each
holds, and the numbers are whatever the runs really produce.

  branch_run_tail.txt        the branch run's command, exit code, final summary line, wall time
  branch_failed.txt          one node id per line, sorted; empty file if there are none
  base_run_tail.txt          the base run's command, base commit, exit code, summary, wall time
  base_failed.txt            one node id per line, sorted; empty file if there are none
  branch_only.txt            `comm -13 base_failed.txt branch_failed.txt`
  base_only.txt              `comm -23 base_failed.txt branch_failed.txt`
  dist_mtime_window.txt      the R-0444 EVENT measurement described in G5
  gate_summary.txt           the three steps of docs/agents/integration_gate.md with their real
                             readings, in the shape `.agent/gate_f272_r27/gate_summary.txt` uses

A RUN LOG IS NEVER WRITTEN INSIDE A WORKTREE WHILE THAT WORKTREE'S SUITE IS RUNNING (R-0176: a log
growing in-repo during the run changes the worktree digest mid-run and produced four false
failures in the manifest-identity ids). Capture each run's output through the subprocess pipe and
write every file above only AFTER that run has exited.


## Constraints

1. Apply every slice BYTE FOR BYTE. Do not reflow, retype or re-indent one. If something looks
   wrong, apply it as given and DECLARE the doubt in the handback.
2. RECORD18 and SLIP18 are APPENDS: the target's existing bytes are a byte-exact PREFIX of the
   result and the slice is an exact SUFFIX of it. Each carries its OWN leading newline — ADD NO
   SEPARATOR of your own, and do not strip one. PLAN18 REPLACES `.agent/plan.md` entirely and has
   no leading newline. FORTSCHRITT is appended to no file.
3. Extract each slice from the COMMITTED `.agent/authored/f274-r18.md` by its BEGIN and END marker
   lines and apply it with a script. Do not retype a slice by hand into a target.
4. THIS ROUND REPAIRS NOTHING. If the gate goes red, you record the red, attribute it as step 4 of
   docs/agents/integration_gate.md prescribes, and hand back. You do not delete a test, weaken an
   assertion, raise a ceiling or touch a file outside the change set to make a number look better.
5. The base run happens ONLY in a throwaway `git worktree` created ON A THROWAWAY BRANCH
   (`git worktree add -b tmp/f274-r18-base <path> d0d8b24da2a080ebcff85e63e73a547e6a8066e6`): the
   self-dogfood branch guard refuses a detached head by design. Remove and prune it afterwards and
   delete the temporary branch. There are 14 worktrees registered before you start; leave that
   number as you found it, and `git status --porcelain` empty at every commit boundary.
6. Run the BRANCH half in the PRIMARY checkout. Do not rebuild `apps/ui/dist` there beforehand;
   measure it warm, as it is.
7. Every gate below runs at a commit STRICTLY EARLIER than C5, so the handback can quote each
   one's real result (§3 item 31). Take G2, G3 at C1 and C3; take G4, G5 and G6 at C4; take G1, G7
   and G8 at C4.
8. Do not write a `Done:` paragraph or a finding registration of your own. This round registers no
   finding and resolves none; the open set is 63 by distinct id at both ends of it.
9. Report each gate's REAL result, including a failure. A gate that fails is a handback that says
   so; it is never a gate quietly re-scoped until it passes.


## The slices

BEGIN PLAN18 sha256=cdd483a33f18330c799000f742a1e5f559515b25de115e767b9ac2ddc4ca6d75 bytes=2416
# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Close F274 at the edge work it actually built and carry the cluster deletion, the atomic record
flip and the classic runner to F275, per DECISION F274 D8 — the split-and-close default operator
amendment amend0905-throughput makes standing at the soft limit, which this feature reached at
session seven of seven. F275 is registered; what remains is the closure itself.

## Current Step

The integration-gate round, per docs/agents/integration_gate.md: the full suite on the branch in
the primary checkout, the full suite at the base in a throwaway worktree with build parity
restored, and the two failure sets compared. It MEASURES and does not repair — no file outside
`.agent/` changes. It also books round 17's PASS verdict and the one dated prose slip that round
declared.

## Next Steps

1. The self-use item closure precondition 6 requires. Every queue item is consumed, so
   `generate_and_append_if_empty` runs FIRST; whatever it yields is planned and run to the normal
   approval gate, and every defect its findings reader returns is registered before the close.
2. The ledger rotation by `scripts/rotate_live_review.py`, as its own commit, after the verdict
   bookings and before the STATUS flip.
3. The evidence job and the fresh review zip. The zip's `base_commit` is the FORK POINT
   `13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, whose ancestry-path and plain `rev-list` counts are
   EQUAL — never `git merge-base`, which names `origin/main`'s tip here and gives unequal counts.
4. The closure commit: the STATUS `[x]` flip with the README sync and the one `consumed_by` edit,
   in ONE commit; then the pull request.

## Risks

- The map was blind twice and is fixed once: R-0834's file-type blindness is closed, R-0832's
  event-name coupling is OPEN. Treat every "zero edges" reading as a claim about the WALKER.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
- R-0736 is OPEN: the integration gate's own parity recipe manufactures false base failures unless
  the copied `apps/ui/dist` is stamped NEWER than the newest file under `apps/ui/src`.
END PLAN18

BEGIN RECORD18 sha256=71736a007fe439a66b16b2abe30b76d4bd30944619ee6a4f2510a546a089ccc4 bytes=5871

Gate: F274 R17 — the F274 round 17 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER ITSELF against the COMMITTED blobs, in the primary checkout. Range `7bd19462`..`4f3f0b8f`, seven commits, every one single-parent, in the ordered sequence C0a, C0b, C1, C2, C3, C4, C5. THIS ROUND EXECUTED THE SPLIT DECISION F274 D8 RULED IN ROUND 16, and it is the second round of F274's closure sequence. G1 TRANSPORT covers the chain this workflow can walk, per docs/agents/planner_reviewer_prompt.md §3 item 37 and NOT the emitted bytes, and it walked TWO chains this round because the new feature file was too large to travel inside the block: the reviewer's scratch original `.remedy-wt/f274-r17-FINAL.md` and both committed copies are all 28775 bytes at `cbad04b949b69e0ca190ea711bdc4641b7c41dc847476dab4a81090422b6f942`, and the committed `docs/roadmap/features/T2_F275.md` is byte-identical to the scratch source `.remedy-wt/f274-r17-F275FILE.txt` at 9701 bytes and `ba5445586c11c28909aab801be1e560e06f0a4bceb31a756eadba298f1f6568d`, copied with `shutil.copyfile` and gated by digest rather than by trusting the call. G2 THE PLAN at `473c8be2`: byte-equal to its slice at 2142 bytes and 39 lines against the AGENTS.md cap of 50, carrying exactly one `## Goal` and one `## Next Steps`. G3 THE RECORD APPEND at `262da752`: 616218 to 622238 bytes, exact append, N counted as 1, ordered equality true, the control at byte offset 616219 rejected by BOTH readers; units 241 to 242, `^Gate: ` 47 to 48, `^Gate: F274 R16 ` 0 to 1, registrations 70 to 70, distinct resolutions 7 to 7, OPEN SET 63 TO 63 BY DISTINCT ID. G4 THE ATOMIC REGISTRATION at `73489a46`, read as THAT COMMIT'S OWN DIFF and never as a range beginning at the round's base — which is the counter-measure the R-0819 recurrence booked in round 16 requires, applied in the very next block: `git show --name-only --format= 73489a46` returns EXACTLY TEN PATHS, `README.md`, `docs/roadmap/STATUS.md`, the six open feature files whose `Depends on` line named F274, the new `docs/roadmap/features/T2_F275.md`, and `tests/docs/test_docs_consistency.py`. Every pair reproduced its declared shape and its ordered counts: S2, S3 and S4 are REWRITEs reading FROM 0 and TO 1, and S1 and S5 are APPEND-shaped and read FROM 1 and TO 1 — S5 in each of its six files — with NO "FROM 0x" count ordered for either, because that count is unattainable by construction when the TO contains the FROM. THE THREE LEDGER NUMBERS `tests/docs/` PINS TO EACH OTHER ALL READ 275: `TOTAL_FEATURES`, the count of STATUS entries, and the count of feature detail files. G5 THE DOCS GATES, each run ALONE by the reviewer in the primary checkout: `tests/docs/` 303 passed, `tests/orchestration/test_roadmap_index.py` 30 passed, and `ruff check` on the edited pin file EXIT 0 with `All checks passed!`. G6 THE BUILT STATE APPEND at `6b8d731b`: `docs/roadmap/features/T2_F274.md` 9344 to 12016 bytes, exact append, N counted as 4, ordered equality true, the control at byte offset 9345 rejected by both readers, and exactly ONE line beginning `## Built State` in the result — the section amend0906-split-placement requires to name which slices moved, and F274's file had never carried one. G7 THE SUITES AND THE SCOPE GUARD: the canary and the progress ledger at 73 passed, the whole range naming FIFTEEN paths of which ZERO begin `packages/`, `apps/` or `scripts/`, and `tests/orchestration/cluster_deletion_map.txt` BYTE-IDENTICAL at the base and at C4, both `7fbf3909fd6d094e0ab3654e8842222a1adf6a51cd6c74bf119b1f7c256d5155`. G8 THE TREE AND THE NUMBERS: porcelain empty, `git ls-files .remedy-wt` empty, worktrees 14 at both ends, per-commit insertions 367, 297, 18, 2, 151 and 35 for C0a through C4, every one under the DECISION F104 D1 cap of 500, and the unquoted `\bHEAD\b` count in the RECORD17 slice is ZERO after backtick-quoted spans are deleted. SIX DEVIATIONS WERE DECLARED AND THE REVIEWER SUSTAINS ALL SIX; ONE OF THEM IS THE REVIEWER'S OWN DEFECT AND IT IS ROUTED TO `.agent/prose_slips.md` RATHER THAN TO AN ID. That one is the fifth: the block's PAIRS17 convention paragraph said a pair block is "every following line up to the next marker line", which does not settle whether the block's trailing newline belongs to it, and under the trailing-newline reading the block CONTRADICTS ITSELF — S5's TO would not contain its FROM although the block's own containment table records `true`, and S2's FROM would occur zero times in `README.md` although the block records exactly one. The worker measured BOTH readings, applied the one under which every stated property holds, and declared the gap rather than choosing silently; that is the same reading the reviewer's own pre-emission dry run used, so the applied state is correct and nothing wrong reached disk. Under operator amendment amend0827-process-diet rule 2 a reviewer-prose imprecision that left nothing wrong on disk earns ONE dated line in `.agent/prose_slips.md` and no id, no severity and no correction round, and this round writes that line. The other five are sustained without further comment: the shell guard refusing `$?` by FORM so every exit code came through a Python runner; the absence of any disposable worktree, which is STRICTER than the block because no product mutation was ordered and both negative controls were computed in memory; the round's scratch scripts living under the gitignored `.remedy-wt/`; `.agent/plan.md` being one round stale at the C0a and C0b boundaries, which is exactly the case §3 item 23 permits; and the worker's own first unit reader comparing unstripped paragraphs and reporting a false negative it then corrected, reported both ways, and which touched no byte on disk. NO FINDING IS REGISTERED BY THIS GATE AND NO NEW ID IS MINTED, so the open set stands at 63 by distinct id and the next free id is R-0837.
END RECORD18

BEGIN SLIP18 sha256=a4b532b3e61442ecb1c8c84ddc5194858eecdef488333c2ae5d0f5825ad0ce0d bytes=958

2026-09-08 · F274 R17 · The round 17 block's PAIRS17 convention paragraph defined a pair block as "every following line up to the next marker line" without settling whether that block's trailing newline belongs to it, and under the trailing-newline reading the block contradicts its own stated properties — S5's TO would not contain its FROM although the block's containment table records `true`, and S2's FROM would occur zero times in `README.md` although the block records exactly one. The worker measured both readings, applied the one under which every stated property holds — which is also the reading the reviewer's pre-emission dry run used, so the applied state is correct and nothing wrong reached disk — and declared the gap. The lesson is that a slice-delimiting convention states what happens to the TERMINAL NEWLINE of a block, because "up to the next marker" is silent about the one byte that decides whether a pair is append-shaped.
END SLIP18

BEGIN FORTSCHRITT sha256=d8df47894df79435e47fd422698d26b272bf730358a9033cc60b9fcd070e1c66 bytes=236
Fortschritt: F274 schließt bei ~35 % des ursprünglichen Umfangs, F275 ist registriert, Integrationsgate läuft (Löschkarte ✅ · Reachability-Ratsche ✅ · D1–D8 ✅ · F275 ✅ · Self-Use-Item und Closure offen) — Schätzung
END FORTSCHRITT


## Done when

G1  TRANSPORT, one digest comparison, at C4. `.agent/authored/f274-r18.md` and
    `.agent/last_block.md` are BYTE-IDENTICAL to each other and to the reviewer's scratch original
    at `/home/decodeux/Repos/remedy/.remedy-wt/f274-r18-FINAL.md`. Report the sha256 and byte count
    of all three. This proof covers the chain this workflow can walk and claims nothing about the
    bytes that reached you (§3 item 37).

G2  THE PLAN, at C1. `.agent/plan.md` is byte-identical to the PLAN18 slice; report its sha256,
    byte count and line count, and that it carries exactly one `## Goal` and one `## Next Steps`.
    Reference: 2416 bytes, 42 lines, both headings once, against the AGENTS.md cap of 50 lines.

G3  THE TWO PROSE APPENDS, at C2 and C3. For each of `.agent/live_review.md` with RECORD18 and
    `.agent/prose_slips.md` with SLIP18, report from the file itself: byte count before and after;
    that the post-image equals the pre-image concatenated with the slice EXACTLY; N, the number of
    blank-line paragraphs in the slice, COUNTED by your script and not taken from this block; that
    the last N blank-line units of the whole file equal the slice's N paragraphs IN ORDER; and that
    a control flipping one byte inside the FIRST appended paragraph — at byte offset 622239 for the
    ledger and 163911 for the slips — is REJECTED by both the byte reader and the ordered-unit
    reader. For the ledger also report before and after: blank-line units; `^Gate: `;
    `^Gate: F274 R17 `; distinct `^- R-\d+ — `; distinct `^Done: R-\d+ — `; and the open set as the
    first minus the second. Reference: ledger 622238 to 628109 bytes, N is 1, units 242 to 243,
    `^Gate: ` 48 to 49, `^Gate: F274 R17 ` 0 to 1, registrations 70 to 70, distinct resolutions 7
    to 7, OPEN SET 63 TO 63 BY DISTINCT ID; slips 163910 to 164868 bytes, N is 1.

G4  THE BRANCH RUN — step 1 of docs/agents/integration_gate.md — in the PRIMARY checkout, at C3
    (that is, before C4 exists), with the tree clean:
      python3 -m pytest -n auto -q
    Report the exact command, the REAL exit code, the final summary line verbatim, the wall clock,
    and the full sorted list of `FAILED` node ids, which goes to `branch_failed.txt` one per line.
    Reference at `4f3f0b8f`: exit 0, 19767 passed, 23 skipped, 118.71s, FAILED count 0 — your run
    is at a later commit and its numbers are whatever it really measures.

G5  THE BASE RUN — step 2 — in the throwaway worktree constraint 5 describes, at
    `d0d8b24da2a080ebcff85e63e73a547e6a8066e6`. In this order:
    (a) Restore build parity: `shutil.copytree(src, dst, symlinks=True)` for the primary's
        `apps/ui/node_modules` and `apps/ui/dist`. Report the file count and the preserved-symlink
        count for each, and that the symlink count matches the primary's.
    (b) APPLY R-0736's FIX CLAUSE: find the newest mtime under `<worktree>/apps/ui/src`, then set
        every entry under `<worktree>/apps/ui/dist` — and the directory itself — to an mtime
        STRICTLY GREATER than it. Report the newest-source mtime, the stamp used, and that
        `dist/index.html` is newer than the newest source file. Content parity alone does not
        neutralise `_frontend_is_stale`; this relation is what that function actually reads.
    (c) Record every `apps/ui/dist` file's mtime BEFORE the run.
    (d) Run `REMEDY_UI_NO_AUTO_BUILD=1 python3 -m pytest -n auto -q` in that worktree. Report the
        exact command, the REAL exit code, the summary line verbatim, the wall clock, and the full
        sorted `FAILED` list to `base_failed.txt`.
    (e) Record every `apps/ui/dist` file's mtime AFTER the run and write `dist_mtime_window.txt`:
        the window start and end, and the per-file before-and-after mtimes. ANY file whose mtime
        falls inside the window VOIDS the parity claim and forces per-id attribution — report that
        outcome honestly rather than the one this block expects (R-0444: measure the EVENT, not the
        outcome; a content hash may accompany the reading but never replaces it).
    Also report the count of the string `React UI not built` in the base run's output. Reference:
    exit 0, 19790 passed, 23 skipped, 141.34s, FAILED count 0, marker count 0, no dist mtime inside
    the window.

G6  THE COMPARISON — step 3 — at C4. Report both, computed from the two sorted files:
      comm -13 base_failed.txt branch_failed.txt   the BRANCH-ONLY set; this is the verdict
      comm -23 base_failed.txt branch_failed.txt   the BASE-ONLY set
    Every id in the branch-only set is attributed per step 4 — serial re-run of the exact node id,
    then classified — and a reproducible branch-only failure coupled to feature code is a BLOCKER
    that stops the round. Every id in the base-only set is attributed to the environment class by
    DIRECT evidence naming the missing artifact per id, or it counts as a genuine base failure and
    blocks the verdict; write those attributions to `base_only_attribution.txt`. Reference: both
    sets EMPTY, which needs no attribution because there is nothing to attribute. Separately report
    the two runs' PASSED counts and their difference, and state that the branch's lower count is
    the tests this feature DELETED rather than tests that vanished — name at least three deleted
    test files from `git diff --name-status d0d8b24d..<C4> -- tests/` as the evidence.

G7  THE SCOPE GUARD AND THE PER-COMMIT NUMBERS, at C4. `git diff --name-only 4f3f0b8f..<C4>` names
    ONLY paths beginning `.agent/` — the base-anchored range is the correct reading because the
    claim is about the WHOLE round's change set — and names NONE beginning `packages/`, `apps/`,
    `tests/`, `scripts/`, `docs/` or `README.md`. Report the full list. Then, for C0a, C0b, C1, C2,
    C3 and C4 and NOT for C5, report the insertion count from `git diff --numstat <parent>..<commit>`
    and confirm each is under the DECISION F104 D1 cap of 500. The `## Commits` table of
    `.agent/handoff.md` carries these same values and its `+/-` cells are the numstat columns cell
    for cell (§3 item 28); state that you compared the two.

G8  THE TREE AND THE RECORD-SLICE SCAN, at C4. `git status --porcelain` is EMPTY; `git ls-files
    .remedy-wt` is EMPTY; report `git worktree list` and confirm it is back to the 14 constraint 5
    names, with the temporary base branch deleted. Report that no file under
    `.agent/gate_f274_r18/` has a `.log` extension. Then, for the RECORD18 and SLIP18 slices as
    committed in `.agent/authored/f274-r18.md`: delete every backtick-quoted span and report the
    count of `\bHEAD\b` in what remains. Reference: ZERO for both (R-0586).


## Handback

Rewrite `.agent/handoff.md` per AGENTS.md and docs/agents/handback_template.md. It has no length
cap (amend0827 rule 3); it is valid when its mandated sections are present. It must carry:

- the state block, naming the feature, the round, THE SESSION NUMBER — session 7 of feature F274 —
  the branch, and the commit SHAs;
- the Fortschritt line, verbatim from the FORTSCHRITT slice above;
- the changed-files table and the `## Commits` table whose `+/-` cells G7 pins;
- ONE LINE PER GATE, G1 through G8, each carrying that gate's REAL measured result;
- the integration gate's own three steps with their real readings, and the explicit statement of
  whether the branch-only set is empty — that sentence is the gate's verdict material;
- the open-findings count, 63 by distinct id, with the arithmetic that produced it;
- every deviation, declared with its reason;
- the item-status table AGENTS.md requires, with every ordered item appearing exactly once;
- the next expected action: the self-use round closure precondition 6 requires.

Then push the branch. Do not create a pull request; the closure sequence creates it in its own
round.
