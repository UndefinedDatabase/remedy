# STEP — F260 round 19: the integration gate

Feature F260, session 7, round 19. Base for this round:
`d4f1a55c1aa4e6315e1b52d573f1847308832d90`, the branch tip, the same object as
`origin/feature/f260-one-world`. Frame convention: this block uses NO runs of
repeated characters; slice delimiters are the single lines `<<<BEGIN name>>>` and
`<<<END name>>>`.

## Goal

The integration gate of docs/agents/integration_gate.md — the full suite run once
on this branch and once at the merge base, compared. It is closure precondition 2
and the only round permitted to claim "full suite green". READ THAT FILE FIRST;
this block does not restate it, it adds the three parity steps the file omits and
that have each cost a previous gate a hundred false failures.

The merge base is `f957c4c6dede34e9ba9d3653ae01cc16157b96fc`, which is also the
current tip of `origin/main`, because round 16 merged `origin/main` into this
branch. The reviewer measured that with `git merge-base`.

## Bundle, in this exact order

- C0a — save this block verbatim to `.agent/authored/f260-r19.md`
- C0b — mirror the same source file to `.agent/last_block.md`
- C1 — `.agent/plan.md`, whole-file replacement from the PLAN slice
- C2 — `.agent/live_review.md` gains GATE_R18
- C3 — the gate evidence directory `.agent/gate_f260_r19/`
- C4 — rewrite `.agent/handoff.md` as the handback

## Change set — no path outside this list may be written

`.agent/authored/f260-r19.md` (C0a) · `.agent/last_block.md` (C0b) ·
`.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
`.agent/gate_f260_r19/` (C3, new directory) · `.agent/handoff.md` (C4)

NOTHING under `packages/`, `apps/`, `tests/`, `docs/`, `scripts/` or `README.md`
is written this round. This is a MEASURING round: if it finds a defect, that
defect is reported, not fixed — the fix is its own reviewer-gated round.

## Constraints

1. Apply every slice BYTE FOR BYTE. If a slice or a gate looks wrong, apply it as
   written and DECLARE the problem in the handback. Never adjust a slice, a test
   or a gate to make a reading come out as ordered. Above all: NEVER delete a
   test, weaken an assertion or raise a ceiling to make a run green.
2. TERMINAL BYTE, measured by the reviewer at `d4f1a55c`: `.agent/live_review.md`
   is 964554 bytes ending in exactly ONE newline. Derive the append recipe from
   the target's own measured terminal byte and `assert` the count before writing.
3. Evidence files under `.agent/gate_f260_r19/` are named `.txt`, NEVER `.log`:
   `.gitignore` drops `*.log` silently and the review-zip guard rejects any member
   ending `.log` (R-0169).
4. NO LOG FILE MAY GROW INSIDE A REPO WORKTREE WHILE A SUITE RUNS (R-0176): a
   file changing under the tree mid-run alters the worktree digest and fails the
   manifest-identity ids as false positives. Capture each run with
   `subprocess.run(..., capture_output=True)` IN MEMORY and write the captured
   text to `.agent/gate_f260_r19/` only after that run has exited.
5. Do NOT author a `Done:` or `Landed:` paragraph. GATE_R18 is a `Gate:` record;
   the open set does not move this round.
6. `cmp` and the `remedy` binary are denied in this sandbox: use
   `filecmp.cmp(shallow=False)` plus sha256, and `python3 -m apps.cli.grouped`.
   Take every exit code from a Python `subprocess.run(...).returncode`; the bash
   guard rejects `$?`, `$( )`, `cp` and shell loop forms BY FORM, and rejects
   environment assignments on the command line — pass `env=` to `subprocess.run`.
   Scratch goes under the gitignored `.remedy-wt/` and is never `git add`ed.
7. `.agent/STOP` does not exist at `d4f1a55c`. If it appears, finish the commit in
   flight, hand off and end. Do not delete it, do not commit it.
8. The handback cannot table its own commit (the R-0149 pattern). Report C4's own
   numbers nowhere. Create no pull request, merge nothing, never force-push,
   never work on `main`.

## The three parity steps docs/agents/integration_gate.md does not state

These are findings this repository has already paid for. Apply all three.

FIRST, `shutil.copytree(src, dst, symlinks=True)` — `symlinks=True` is
LOAD-BEARING and is not the default. The default DEREFERENCES npm's `.bin`
shims, of which this tree has 23, and CAUSES base-only failures the parity exists
to prevent (finding R-0591, seven of them at F085 R23). Never symlink the
DIRECTORIES themselves: the auto-build writes THROUGH such a symlink into the
primary checkout (F053 R3).

SECOND, ADVANCE THE COPIED `dist` MTIMES (finding R-0736, Medium, OPEN).
`shutil.copytree` preserves source mtimes while `git worktree add` stamps every
checked-out file with the checkout time, so the copied build is byte-correct and
mtime-STALE. `ui_server._frontend_is_stale()` returns True when any file under
`apps/ui/src/` is newer than `dist/index.html`; `REMEDY_UI_NO_AUTO_BUILD=1` then
correctly suppresses the rebuild, the UI is never built, and every test reaching
the door dies on `ERROR: React UI not built.` — 114 false base-only ids when this
was last measured literally. After copying, raise `dist/index.html`'s mtime above
every file under THAT WORKTREE's `apps/ui/src`. Nothing is faked: the copy is
already byte-correct and what is corrected is a timestamp the copy cannot carry
meaningfully across a fresh checkout.

THIRD, PROVE THE REPAIR BY CALLING THE REAL PREDICATE, not by reasoning about it:
import `_frontend_is_stale` from the BASE WORKTREE's own
`packages/orchestration/ui_server.py` — confirm `__file__` resolves inside that
worktree and report the path — and record that it answers False there BEFORE the
base run starts.

## The slices

<<<BEGIN PLAN>>>
# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, `origin/main` merged in at round 16. Rounds 1 to
18 are reviewed; round 1 FAILED and was repaired, and 2 to 18 PASSED. DECISION
F260 D8 (round 17) closes this feature at the scope it built; F272 carries the
remainder and was registered in round 18, directly after F260 in the ledger.

## Goal

Session 7 performs SPLIT-AND-CLOSE at the amend0905-throughput soft limit of 7
sessions. The split is ruled and registered; what remains is the closure sequence
itself, and the integration gate that closure precondition 2 requires.

## Current Step

Round 19 is the INTEGRATION GATE: the full suite run once on this branch and once
in a disposable worktree at the merge base `f957c4c6`, with UI parity restored
before the base run, and the two failure sets compared. It measures; it does not
repair. A reproducible branch-only failure coupled to feature code is a BLOCKER
and buys its own reviewer-gated round.

## Next Steps

1. Closure part 1: the self-use item, the evidence job and the review zip.
2. Closure part 2: the verdict bookings and the ledger rotation.
3. Closure part 3: the STATUS accepted flip, the README sync, the handback and the
   pull request, which is left UNMERGED as the operator's review window.

## Risks

- The base worktree lacks `apps/ui/node_modules` and `apps/ui/dist`, and a copy
  of them carries stale mtimes that make the UI read as un-built. Both are
  repaired before the base run and the repair is proved by calling the real
  predicate, not by asserting it.
- The self-use queue is EXHAUSTED — all ten entries carry a `consumed_by` — so
  closure precondition 6 runs `generate_and_append_if_empty` FIRST and records
  `self-use NONE (queue exhausted)` only after that also answers `None`.
<<<END PLAN>>>
<<<BEGIN GATE_R18>>>
Gate: R18 — the F260 R18 entry. R18 REGISTERED F272, THE FOLLOW-UP FEATURE DECISION F260 D8 SPLIT OFF THIS ONE, DIRECTLY AFTER ITS PARENT IN THE LEDGER. VERDICT PASS. Range `7a1ce69d594043dfaad6c69161c93613d4229821`..`d4f1a55c1aa4e6315e1b52d573f1847308832d90`, six commits, every one single-parent, in exactly the bundle's ordered sequence C0a, C0b, C1, C2, C3, C4 with nothing added, dropped or reordered; insertion counts 399, 337, 23, 4 and 124 for the five commits before the handback, every one far under the 500 cap. The reviewer re-ran every gate itself rather than reading the handback's numbers. TRANSPORT: the reviewer's scratchpad original `.remedy-wt/f260-r18-block.md`, the committed `.agent/authored/f260-r18.md` and `.agent/last_block.md` are all 28307 bytes and all hash to `657022416f31310536a64d78d191c5aa264184258399aa9f1cd10f8f6d9e62b1`; per §3 item 37 that chain covers the reviewer's scratch file, the worker's saved copy and the mirror, and is not a claim about the bytes emitted into a prompt. THE RECORD: `.agent/live_review.md` 959115 to 964554 bytes and `.agent/prose_slips.md` 122752 to 123846 bytes, each equal to its pre-image plus its own recipe exactly and each with the pre-image a byte-exact prefix. `.agent/plan.md` equals its slice plus one newline at 1820 bytes and 38 lines, under the 50-line cap. THE REGISTRATION, which is the point of the round, LANDED AS ONE ATOMIC COMMIT over fifteen paths, and the reviewer recomputed every edited file INDEPENDENTLY from its pre-edit bytes with only its own pairs applied: `docs/roadmap/STATUS.md`, `README.md`, `tests/docs/test_docs_consistency.py` and the six feature files `T2_F261.md`, `T2_F263.md`, `T2_F268.md`, `T2_F269.md`, `T2_F270.md`, `T2_F271.md` — nine reconstructions, every one byte-equal to the committed bytes. All six pairs read FROM exactly 1 before and 0 after with `TO contains FROM: false`, so every one is a REWRITE and every FROM was consumed. `docs/roadmap/features/T2_F272.md` is a NEW file of 6852 bytes equal to its slice plus one newline, absent at the round's base, and no block marker line reached it. PLACEMENT, WHICH IS WHAT operator order amend0906-split-placement ACTUALLY REQUIRES: the STATUS ids in file order read F259, F260, F272, F261 — F272 sits IMMEDIATELY after its parent and inside the same `## Tier 2` heading, so Rule A5 proposes it before any other unchecked feature, and its filename tier and its STATUS tier are both 2. THE LEDGER AND THE README AGREE at the registration commit, measured by the reviewer: 272 feature detail files and 272 STATUS entries, with the set of ids missing from 1 through 272 EMPTY for both; `TOTAL_FEATURES` 272; accepted `[x]` 73 and claimed `[~]` 1; and the README numeral parsing to 73 of 272. SUITES re-run by the reviewer in the primary checkout, serially: `tests/docs/` exit 0 at 303 passed, `tests/orchestration/test_roadmap_index.py` exit 0 at 30 passed, the canary `tests/cli/test_golden_path.py` exit 0 at 42 passed, `python3 -m apps.cli.grouped integrity check --json` exit 0 with `"passed": true` and `"fail_count": 0`, and `ruff check` over the one edited Python file exit 0. The reviewer had additionally dry-run the WHOLE registration before emitting the block, in a disposable worktree removed afterwards by exact path, together with a RED CONTROL that reverted only the `TOTAL_FEATURES` pin and confirmed `tests/docs/` really goes red — exit 1 at 3 failed and 300 passed — which is the measured justification for ordering those fifteen paths as ONE commit rather than several. CENSUS: `^Gate: ` 27 with `^Gate: R17 — ` at exactly 1; registrations 301 over 301 DISTINCT ids; `^Done: ` 5 lines over THREE distinct ids; OPEN SET 298 BY DISTINCT ID, unchanged, correctly, because this round registered and resolved nothing. TEN ITEMS WERE DECLARED AND ALL TEN ARE UPHELD; two deserve recording here. The worker MEASURED rather than assumed which feature files name F260 in their "Depends on" line, found exactly six, edited all six, and reported that the operator's own amend0906 commit had reached only five of them — `T2_F263.md` carried no placeholder clause and needed a pair of its own, which this block supplied. And the worker noticed that F272's "Blocks/used by" names F266 while `T4_F266.md` names neither F260 nor F272 in its own "Depends on" line, leaving a one-directional cross-reference; the reviewer measured that this asymmetry PRE-EXISTS F272 — F260's own "Blocks/used by" names F266 identically and F266 has never named F260 — so amend0906's rule, which binds only files naming the parent in a DEPENDS-ON line, did not reach F266 and nothing new is wrong. It is recorded rather than repaired because repairing it would write a path outside the round's change set.
<<<END GATE_R18>>>

## Done when — the gates. Report ONE LINE PER GATE with its REAL exit code.

**G1 TRANSPORT — one comparison.** Before staging C0a, sha256 over the
delegation's source file, `.agent/authored/f260-r19.md` and
`.agent/last_block.md`; all three must equal the digest the delegation names.
Both writes `shutil.copyfile`, each proved with `filecmp.cmp(shallow=False)`.

**G2 THE RECORD, at C2.** Three readings on `.agent/live_review.md`:
(a) exact image — `post == pre + b"\n" + GATE_R18 + b"\n"` True and
`post[:len(pre)] == pre` True; report both byte counts;
(b) structural, independent of (a) — split the WHOLE file on a blank line and
compare the last N units against the slice's N paragraphs IN ORDER, N counted by
your script from the slice and never asserted by this block; report units before
and after;
(c) negative control IN MEMORY on a `bytes` object: flip one byte inside the
FIRST appended paragraph; both readers must REJECT; restore and both must ACCEPT
with the restored image equal to the disk image.

**G3 THE PLAN, at C1.** `.agent/plan.md` equals the PLAN slice plus exactly one
trailing newline. Report byte count and line count; under the 50-line cap, and
carrying `## Goal` and `## Next Steps`.

**G4 THE BRANCH RUN.** BEFORE running, assert and report the dist precondition in
the PRIMARY checkout: `apps/ui/dist/index.html` exists, and its mtime is greater
than the mtime of EVERY file under `apps/ui/src` — report the dist mtime, the
newest src file's path and mtime, and the boolean. A cold or stale dist reddens
this suite for a reason that has nothing to do with the branch, so this reading
comes first and is reported whatever it says. Then, from the repo root:

    python3 -m pytest -n auto -q

captured in memory. Report the real exit code, the wall-clock seconds, the raw
tail line, and the FULL sorted list of `^FAILED` ids written to
`.agent/gate_f260_r19/branch_failed.txt`. Never truncate that list.

**G5 THE BASE RUN.** Create the worktree ON A BRANCH, never detached — the
self-dogfood guard refuses a detached HEAD by design (DECISION D3):

    git worktree add -b tmp/f260-r19-base <path> f957c4c6dede34e9ba9d3653ae01cc16157b96fc

with `<path>` under the gitignored `.remedy-wt/`. Then apply the three parity
steps this block states above, and report, in this order: the two `copytree`
calls with `symlinks=True` and the count of symlinks that survived under
`apps/ui/node_modules/.bin` in the COPY (the primary has 23); the `dist` mtime
before and after the advance; and the value the REAL `_frontend_is_stale()`,
imported from the BASE worktree, returns — with its `__file__` — which must be
False. Record the mtime of every file under the base worktree's `apps/ui/dist`
BEFORE the run and AFTER it, and report the run's wall-clock window: ANY mtime
falling inside that window VOIDS the parity claim, which is reported as void
rather than hidden. Then the identical command, captured in memory, with
`REMEDY_UI_NO_AUTO_BUILD=1` passed through `env=`. Report the exit code, wall
seconds, raw tail, and the FULL sorted `^FAILED` list to
`.agent/gate_f260_r19/base_failed.txt`. Finally remove the worktree BY EXACT
PATH, `git worktree prune`, delete the `tmp/f260-r19-base` branch, and prove all
three with `git worktree list` and `git branch --list "tmp/*"`.

**G6 THE COMPARISON, and BOTH sets are attributed.** Report
`comm -13 base_failed.txt branch_failed.txt` — the BRANCH-ONLY ids — and
`comm -23 base_failed.txt branch_failed.txt` — the ids the branch FIXED or that
the base environment broke. ATTRIBUTE EVERY ID IN BOTH SETS, unconditionally and
whether or not the parity claim held: an unattributed id counts as a genuine
failure and blocks the gate verdict. For every BRANCH-ONLY id, re-run that exact
node id SERIALLY and classify: serial-pass is the xdist-flake class and is
recorded, not a blocker; serial-fail must be reproduced at the merge base before
the feature is blamed; a reproducible branch-only failure coupled to feature code
is a BLOCKER — STOP, write the handback, and do not attempt the fix. If both
sets are empty, say so and report the empty comparison as the reading it is.

**G7 THE EVIDENCE AND THE CHECKS, at C3.** `.agent/gate_f260_r19/` contains
`branch_failed.txt`, `base_failed.txt` and the two captured raw tails, all `.txt`
and all committed; report the directory listing with byte counts, and that
`git ls-files .agent/gate_f260_r19` returns exactly those files. Then
`python3 -m apps.cli.grouped integrity check --json` — exit 0, `"passed": true`,
`"fail_count": 0`.

**G8 TREE AND STRUCTURE.** `git status --porcelain` EMPTY; `git ls-files
.remedy-wt` EMPTY; `git worktree list` showing the primary and the ELEVEN
pre-existing `remedy/job-*` rows and no gate worktree; every commit C0a through
C3 single-parent with its parent count reported; and each of their INSERTION
counts — the `+` column of `git diff --numstat`, never insertions plus deletions
— reported and under 500.

## Handback

Rewrite `.agent/handoff.md`. Mandated sections: the Session block naming SESSION 7
of F260, round 19, rounds so far 19; a one-sentence context self-assessment; the
Range; the per-commit table with `+/-` from `git log --numstat`, never re-derived
by eye; External actions; Verification, one line per gate with its real exit code;
the Authored-text proofs; Deviations and assumptions; the Item-status table with
every bundle item and every gate appearing exactly once as `done`, `skipped` or
`deviated` with a reason; Open findings; and Next. Then
`git push -u origin feature/f260-one-world`.
