# STEP — F260 round 18: register the follow-up feature F272

Feature F260 "One world: mission → job → run", session 7, round 18. Base for this
round: `7a1ce69d594043dfaad6c69161c93613d4229821`, the branch tip, the same object
as `origin/feature/f260-one-world`. Frame convention: this block uses NO runs of
repeated characters; slice delimiters are the single lines `<<<BEGIN name>>>` and
`<<<END name>>>`.

## Goal

Apply DECISION F260 D8, which round 17 recorded: register F272 — the remaining
scope of F260 — as a new feature whose STATUS line sits IMMEDIATELY after F260's
inside the same tier heading, per operator order amend0906-split-placement, so
that Rule A5 proposes it before any other unchecked feature. The ledger pin, the
README counters, the STATUS line and the detail file move in ONE commit, because
`tests/docs/test_docs_consistency.py` pins the feature count, the id contiguity
and the filename tier against each other, and any split of that edit is red.

## Bundle, in this exact order

- C0a — save this block verbatim to `.agent/authored/f260-r18.md`
- C0b — mirror the same source file to `.agent/last_block.md`
- C1 — `.agent/plan.md`, whole-file replacement from the PLAN slice
- C2 — the record: `.agent/live_review.md` gains GATE_R17, then
  `.agent/prose_slips.md` gains SLIP24 — ONE commit, in that file order
- C3 — THE REGISTRATION, one atomic commit over the paths listed below
- C4 — rewrite `.agent/handoff.md` as the handback

## Change set — no path outside this list may be written

- `.agent/authored/f260-r18.md` (C0a) · `.agent/last_block.md` (C0b) ·
  `.agent/plan.md` (C1) · `.agent/live_review.md` and `.agent/prose_slips.md` (C2)
  · `.agent/handoff.md` (C4)
- C3, and every one of these lands in that ONE commit:
  `docs/roadmap/features/T2_F272.md` (NEW FILE, the F272FILE slice) ·
  `docs/roadmap/STATUS.md` (STATUSPAIR) · `README.md` (READMECOUNT, READMETIER) ·
  `tests/docs/test_docs_consistency.py` (PINPAIR) ·
  `docs/roadmap/features/T2_F261.md`, `T2_F268.md`, `T2_F269.md`, `T2_F270.md`,
  `T2_F271.md` (GENPAIR, once in each) ·
  `docs/roadmap/features/T2_F263.md` (F263PAIR)

`docs/roadmap/features/T2_F260.md` is NOT touched; round 17 wrote its Built State.
Nothing under `packages/`, `apps/` or `scripts/` is touched, and
`tests/docs/test_docs_consistency.py` is the ONLY file under `tests/` this round
writes — only its `TOTAL_FEATURES` pin and the comment above it.

## Constraints

1. Apply every slice BYTE FOR BYTE. If a slice or a gate looks wrong, apply it as
   written and DECLARE the problem in the handback. Never adjust a slice, a test
   or a gate to make a reading come out as ordered.
2. TERMINAL BYTES, measured by the reviewer at `7a1ce69d`: `.agent/live_review.md`
   959115 bytes and `.agent/prose_slips.md` 122752 bytes, each ending in exactly
   ONE newline. Derive each recipe from its own target's measured terminal byte
   and `assert` the count before writing anyway — that is what makes a wrong
   measurement abort instead of corrupt.
3. C3 IS ONE COMMIT. Every path listed under C3 above is staged and committed
   together. Committing the STATUS line without the detail file, or the counters
   without the pin, leaves a state in which `tests/docs/` is red, and the README
   and the ledger may never disagree in any committed state.
4. Every pair is applied with `str.replace(FROM, TO, 1)` AFTER asserting the FROM
   occurs EXACTLY ONCE in the file being edited; GENPAIR is asserted once PER
   FILE, not once overall. `T2_F272.md` is a NEW file — write the F272FILE slice
   plus exactly one trailing newline, never by copying another feature file.
5. Do NOT author a `Done:` or `Landed:` paragraph. GATE_R17 is a `Gate:` record
   and registers nothing; the open set does not move this round.
6. `cmp` and the `remedy` binary are denied in this sandbox: use
   `filecmp.cmp(shallow=False)` plus sha256, and `python3 -m apps.cli.grouped`.
   Take every exit code from a Python `subprocess.run(...).returncode`; the bash
   guard rejects `$?`, `$( )` and shell loop forms BY FORM. Scratch goes under the
   gitignored `.remedy-wt/`, is never `git add`ed, and any worktree you create is
   removed BY EXACT PATH, never by glob.
7. `.agent/STOP` does not exist at `7a1ce69d`. If it appears at any point, finish
   the commit in flight, hand off and end. Do not delete it, do not commit it.
8. The handback cannot table its own commit (the R-0149 pattern). Report C4's own
   numbers nowhere; the reviewer measures them at the next gate. Create no pull
   request, merge nothing, never force-push, never work on `main`.

## The pairs

The reviewer ran the containment test on each pair and reports its OUTPUT here.
Every FROM below occurs EXACTLY ONCE in its own target file, and all six read
`TO contains FROM: false` ⇒ REWRITE, so every FROM count after its edit must be 0.

STATUSPAIR — `docs/roadmap/STATUS.md`. The FROM spans F260's line AND the line
that follows it, so the pair PROVES the new line lands between them and nowhere
else — which is what amend0906-split-placement requires.

<<<BEGIN STATUSPAIR_FROM>>>
- [~] F260 — One world: mission → job → run
- [ ] F261 — CLI vocabulary v2 (rename & prune)
<<<END STATUSPAIR_FROM>>>
<<<BEGIN STATUSPAIR_TO>>>
- [~] F260 — One world: mission → job → run
- [ ] F272 — One world completion — the run re-key, the consumers, the classic runner and the cluster deletion
- [ ] F261 — CLI vocabulary v2 (rename & prune)
<<<END STATUSPAIR_TO>>>

READMECOUNT — `README.md`.

<<<BEGIN READMECOUNT_FROM>>>
73 of 271 registered items accepted.
<<<END READMECOUNT_FROM>>>
<<<BEGIN READMECOUNT_TO>>>
73 of 272 registered items accepted.
<<<END READMECOUNT_TO>>>

READMETIER — `README.md`. F272 is Tier 2, so that tier's TOTAL rises by one; its
DONE column does not move, because F272 is registered unchecked and F260 is still
`[~]` at this commit.

<<<BEGIN READMETIER_FROM>>>
| 2 | Minimal Self-Build Runtime | 16 | 24 |
<<<END READMETIER_FROM>>>
<<<BEGIN READMETIER_TO>>>
| 2 | Minimal Self-Build Runtime | 16 | 25 |
<<<END READMETIER_TO>>>

PINPAIR — `tests/docs/test_docs_consistency.py`. The comment block above the
constant narrates every registration batch, so the new batch is narrated in the
same commit that changes the number.

<<<BEGIN PINPAIR_FROM>>>
#: T2_F269.md, T2_F270.md and T2_F271.md.
TOTAL_FEATURES = 271
<<<END PINPAIR_FROM>>>
<<<BEGIN PINPAIR_TO>>>
#: T2_F269.md, T2_F270.md and T2_F271.md. One more, F272 (one world
#: completion: the run re-key, the consumers, the classic runner and the
#: prototype cluster deletion), was registered on 2026-09-06 by DECISION
#: F260 D8, which split it off F260 at the amend0905-throughput soft limit
#: and placed it directly after its parent per amend0906-split-placement;
#: see T2_F272.md.
TOTAL_FEATURES = 272
<<<END PINPAIR_TO>>>

GENPAIR — applied ONCE IN EACH of `docs/roadmap/features/T2_F261.md`,
`T2_F268.md`, `T2_F269.md`, `T2_F270.md` and `T2_F271.md`, which already carry the
placeholder clause the operator's amend0906 commit wrote. This pair replaces the
placeholder with the concrete id, which is what amend0906-split-placement asks for
and what AGENTS.md's one-spelling-per-concept rule prefers over keeping both.

<<<BEGIN GENPAIR_FROM>>>
 and any follow-up feature split off F260 (amend0906-split-placement)
<<<END GENPAIR_FROM>>>
<<<BEGIN GENPAIR_TO>>>
, F272 (one world completion — the run re-key, the consumers, the classic runner and the cluster deletion)
<<<END GENPAIR_TO>>>

F263PAIR — `docs/roadmap/features/T2_F263.md` ONLY. That file names F260 in its
"Depends on" line and did NOT receive the operator's placeholder clause — the
amend0906 commit reached five of the six dependents — so it needs its own pair.

<<<BEGIN F263PAIR_FROM>>>
F260 (one world: mission → job → run) · Blocks/used by:
<<<END F263PAIR_FROM>>>
<<<BEGIN F263PAIR_TO>>>
F260 (one world: mission → job → run), F272 (one world completion — the run re-key, the consumers, the classic runner and the cluster deletion) · Blocks/used by:
<<<END F263PAIR_TO>>>

## The slices

<<<BEGIN F272FILE>>>
# T2_F272 — One world completion — the run re-key, the consumers, the classic runner and the cluster deletion
**Tier 2 · Depends on: F259 (the binding concept model, `docs/system/vocabulary.md`), F260 (the one job record and the one id shape it closed at) · Blocks/used by: F261, F266, F268, F269, F270, F271, F263 — everything later that names a job, a run or a command**

> Registered 2026-09-06 by DECISION F260 D8 in `.agent/decisions.md`, which split
> the remaining scope off F260 at the amend0905-throughput soft limit and placed
> this line directly after its parent per operator order amend0906-split-placement.
> The closure evidence this feature starts from — the accepted HEAD, the evidence
> job, the package name and its SHA-256 — is recorded on F260's own accepted line
> in `docs/roadmap/STATUS.md` and deliberately not copied here, because a second
> copy of a value drifts and the ledger line is the durable carrier.
> REGISTRATION ONLY — nothing in this file has been implemented.

## Goal & Done
Finish what F260 began. F260 settled WHAT a job is — one record at
`<data_root>/jobs/<16hex>/job.json`, one id shape, one minting function per kind,
and a run that is an INVOCATION rather than an event. This feature spends that
settlement: a Job carries MANY runs, every consumer moves onto the unified model,
and the classic runner, its resolver and the prototype cluster are deleted.

DONE when every Acceptance item below holds — they are F260's Acceptance list,
carried over unchanged, because none of them held at F260's close — and when
DECISION F260 D3, the deletion paragraph, exists and names every deleted module
and the feature that inherited its idea.

## Why this exists
Not because F260 was wrong, and not because anything it built is being redone.
F260 reached the operator's soft limit of 7 sessions during T002, earlier than the
split point its own Orchestrator brief anticipated, and DECISION F260 D8 closed it
at a self-consistent scope rather than running past the limit or narrowing the
Acceptance list to fit. Every ruling F260 recorded — D-A, D0, D1, D2, D4, D5, D6,
D7 — stays binding here and is NOT restated: read
`docs/roadmap/features/T2_F260.md`, which keeps its Goal, Design, T-slice and
Acceptance sections unedited for exactly this purpose, and its Built State for
what is already on disk. The one measurement worth repeating, because it is this
feature's first prerequisite and F260 paid for it: before F260's round 15 a "run"
was an EVENT, so five events of one resume became five runs in five files; after
it, one invocation is one run. `Job.run_refs` is truthful only on the far side of
that change, and the re-key only on the far side of `run_refs`.

## T001 — The plural run list and the run re-key
`Job.run_refs`, the plural run list DECISION F260 D1 names and nothing on disk
carries yet. Then the re-key: `run_log_dir` and `pingpong_run_dir` collapse onto
one `run_dir` keyed by RUN id, per D1. The reader side needs a job to name its
runs, so `run_refs` is the prerequisite and lands first.

The test-side spelling sweep DECISION F260 D6 declined is inherited HERE and
touched once, in this task. It needs its own red-proof plan: F260's round 15 could
go red only because `tests/test_timeline.py`, `tests/test_run_log.py` and
`tests/test_data_paths.py` still hand-spell the old path, so a round that sweeps
them consumes its own observer. The pre-sweep and post-sweep PAIR is the shape.

## T002 — The rest of the unified record
The administrative fields — eight of D1's eleven have no counterpart in `JobPlan`
— and the Mission extension: the order, the contract (D9 shape, may be empty until
F269 fills it), the mission plan and the ordered job references.

## T003 — Move the consumer list
Every consumer named under "Design" in `docs/roadmap/features/T2_F260.md` onto the
unified model, one consumer per commit where the diff allows, each with the test
that proves it works on a job created through the ping-pong path. That list is not
copied here on purpose: F260's file measures it with line citations, and a second
copy would drift.

## T004 — Delete the classic runner
`job.run --cycles`, `job.run-next`, `job.run-loop`, their handlers and tests; the
resolver collapse DECISION F260 D5 placed here, in the SAME commit range that
deletes the classic store, because the collapse is a behaviour change to a shared
error path and is harmless only once that store is gone; `resolve_any_job_id`, the
"TWO job stores" paragraph, every which-store branch, and the absence test.

## T005 — Reachability test and cluster deletion (last, the deletion round)
The D11c reachability test in `tests/`, run and green BEFORE deletion; the two
carry-overs F260's Design section names; DECISION F260 D3 drafted; then the
deletion of every module, handler, catalog entry, `ui_server.py` section and test
that section lists, one commit per module group. A module that turns out to be
REACHABLE is reported with its import chain, never deleted.

## Acceptance
THE ACCEPTANCE LIST OF THIS FEATURE IS THE ONE IN
`docs/roadmap/features/T2_F260.md`, IN FULL AND UNCHANGED. It is referenced rather
than copied for the same reason the consumer list and the module list above are:
every item of it was measured OPEN at F260's close, F260's file keeps that section
unedited on purpose, and a second copy of a contract is a copy that drifts. Read it
there; it binds here.

Five of its items were raised by the operator's tests.md run of 2026-09-05 and
carry finding ids, named here so a reader can find them by id without opening the
other file: R-0803 (the suite never writes into the configured data root),
R-0804 (every cockpit read endpoint returns 200 for a ping-pong-created job, and
the `_JobPlanTaskAdapter` shim is deleted rather than fixed), R-0807 (one ledger
row per provider call, with its role), R-0810 (the fake builder is idempotent per
task) and R-0812 (the narration table covers every emitted event kind).

## Do not touch
Everything F260's own "Do not touch" section names, unchanged: the scope-fence
builtin deny list (F017), the approval gate, STATUS semantics. No command is
RENAMED here — F261 owns renames. No module outside F260's Design lists is
deleted.

## Orchestrator brief
T001 first, because `run_refs` and the re-key are what every later task reads
through; then T002, T003 consumer by consumer, T004, and T005 LAST as the deletion
round with the reachability test run before the first `git rm`. F260's brief
prohibition binds here unchanged and is the one hard rule of the sequencing: NEVER
SPLIT INSIDE T005. A half-performed deletion is the single state this work must
not leave behind, so a session reaching its own soft limit splits between T003 and
T004, or before T005, and never within it.
Findings carried: R-0816 (open, owned here).
<<<END F272FILE>>>
<<<BEGIN PLAN>>>
# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, `origin/main` merged
in at round 16. Rounds 1 to 17 are reviewed; round 1 FAILED and was repaired, and
2 to 17 PASSED.

## Goal

Session 7 reaches the amend0905-throughput soft limit of 7 sessions, so this
session performs SPLIT-AND-CLOSE on its own authority. DECISION F260 D8, recorded
in round 17, closes F260 at the scope it built — T001 whole, and the RUN side of
T002 — and moves the remainder to a follow-up feature registered directly after
F260 per operator order amend0906-split-placement.

## Current Step

Round 18 REGISTERS that follow-up as F272: its detail file, its STATUS line
between F260's and F261's, the README counters, the `TOTAL_FEATURES` pin and the
six downstream "Depends on" lines, all in ONE commit, because the docs suite pins
those values against each other.

## Next Steps

1. The integration gate: the full suite at the branch head and at the merge base,
   per docs/agents/integration_gate.md.
2. Closure part 1: the self-use item, the evidence job and the review zip.
3. Closure part 2: the verdict bookings and the ledger rotation.
4. Closure part 3: the STATUS accepted flip, the README sync, the handback and the
   pull request, which is left UNMERGED as the operator's review window.

## Risks

- README.md and docs/roadmap/STATUS.md may never disagree in any committed state.
  This round moves both plus the pin in one commit; the closure flip moves both
  again in one commit; no other commit of this session touches either.
- The self-use queue is EXHAUSTED — all ten entries carry a `consumed_by` — so
  closure precondition 6 runs `generate_and_append_if_empty` FIRST and records
  `self-use NONE (queue exhausted)` only after that also answers `None`.
<<<END PLAN>>>
<<<BEGIN GATE_R17>>>
Gate: R17 — the F260 R17 entry. R17 RULED THE SPLIT AS DECISION F260 D8 AND STATED WHAT F260 ACTUALLY BUILT. VERDICT PASS. Range `867f34ae0c4632c961ad4a0dc9ef168d595606fc`..`7a1ce69d594043dfaad6c69161c93613d4229821`, six commits, EVERY ONE SINGLE-PARENT, in exactly the bundle's ordered sequence C0a, C0b, C1, C2, C3, C4 with nothing added, dropped or reordered; insertion counts 324, 242, 15, 12 and 50 for the five commits before the handback, every one far under the 500 cap. The reviewer re-ran every gate itself rather than reading the handback's numbers. TRANSPORT: the reviewer's scratchpad original `.remedy-wt/f260-r17-block.md`, the committed `.agent/authored/f260-r17.md` and `.agent/last_block.md` are all 31781 bytes and all hash to `ceec367fcf541c704f86a2d2259929445044cc49b729809a61e20fc63aeb4a03`; per §3 item 37 that chain covers the reviewer's scratch file, the worker's saved copy and the mirror, it is a COPY chain in which nothing is retyped, and it is not a claim about the bytes emitted into a prompt. THE RECORD: `.agent/live_review.md` 953191 to 959115 bytes and `.agent/decisions.md` 848037 to 853742 bytes, each equal to its pre-image plus its own recipe exactly, each with the pre-image a byte-exact prefix, blank-line units 438 to 439 and 1899 to 1900, and each proved a THIRD time by an in-memory negative control that flipped one byte inside the first appended paragraph, was REJECTED by both the byte reader and the structural reader, and was accepted by both after restoration. The two files needed DIFFERENT recipes and the worker derived each from its own target: `.agent/decisions.md` ended in ZERO newlines after the round-16 merge left it on `origin/main`'s convention, so its recipe opened with two newlines and closed with one, restoring a trailing newline the file now has. `.agent/prose_slips.md` 119984 to 122752 bytes, units 151 to 154, carrying SLIP21, SLIP22 and SLIP23 as its last three units in that order. THE FEATURE FILE: `docs/roadmap/features/T2_F260.md` 28449 to 32057 bytes, and the reviewer reconstructed it INDEPENDENTLY from the pre-edit text — the three pairs applied in order, then the Built State appended by the recipe derived from the file's own terminal byte — and the reconstruction equals the committed bytes exactly. The three pairs each read FROM exactly 1 before; the containment test printed `true` for the header-note pair and the Orchestrator-brief pair, which are append-shaped and whose FROM therefore survives inside the TO, and `false` for the REGISTRATION ONLY pair, whose FROM reads 0 after. The file ends with exactly one newline and no block marker line reached it. CENSUS: `^Gate: ` 26 with `^Gate: R17 — ` not yet present and `^Gate: R16 — ` at exactly 1; registrations 301 over 301 DISTINCT ids; `^Done: ` 5 lines over THREE distinct ids; OPEN SET 298 BY DISTINCT ID, unchanged, which is correct because this round registered and resolved nothing. TWO CLAIMS INSIDE THE AUTHORED SLICES WERE FLAGGED BY THE WORKER AS TRANSPORTED ON THE BLOCK'S AUTHORITY RATHER THAN INDEPENDENTLY MEASURED, WHICH WAS EXACTLY RIGHT OF IT TO SAY, AND THE REVIEWER HAS NOW MEASURED BOTH. DECISION F260 D8's sentence "Every round from 2 to 16 PASSED, one round FAILED and was repaired" is TRUE: the sixteen F260 `Gate:` records were parsed as whole blank-line units and read one `VERDICT FAIL`, at R1, and fifteen `VERDICT PASS`, at R2 through R16, with none neither. The Built State's round attributions are accurate with one qualification now recorded here rather than left for a later reader: R6 STRADDLES the boundary the section draws, because it carries DECISION F260 D4 — the ruling that closes T001 by moving the resolver out of it — and ALSO the first `data_paths` spelling of D1's layout, which is T002 work; the section says T001 ran rounds 1 to 6 and T002 rounds 7 to 15, which describes where each task's work sat and does not claim exclusivity, so it stands. SUITES re-run by the reviewer in the primary checkout, serially: `tests/docs/` exit 0 at 303 passed, `tests/orchestration/test_roadmap_index.py` exit 0 at 30 passed, the canary `tests/cli/test_golden_path.py` exit 0 at 42 passed, each with zero `FAILED` and zero `ERROR` lines, and `python3 -m apps.cli.grouped integrity check --json` exit 0 with `"passed": true` and `"fail_count": 0` over five checks. The reviewer had additionally dry-run the whole of C3 before emitting the block — the three pairs and the append applied to a scratch copy in a disposable worktree, with both docs suites green on the result — and removed that worktree by exact path. `git status --porcelain` EMPTY and `git ls-files .remedy-wt` EMPTY in the primary checkout. NINE ITEMS WERE DECLARED AND ALL NINE ARE UPHELD; two are consequences of the reviewer's own choice of pair anchors and neither leaves anything false on disk. The header-note pair anchored on the file's OLDEST registration line, so the new "BUILT across rounds 1 to 17" sentences now sit ABOVE the "Rewritten 2026-09-05" line rather than below it — chronologically interleaved prose in a header block, recorded as one dated line in `.agent/prose_slips.md`. The Orchestrator-brief pair's FROM ended mid-line, so its replacement leaves one line of about 105 characters where the file's convention is roughly 80; the markdown and the link inside it are intact and nothing was reflowed, because reflowing is an edit the block did not order.
<<<END GATE_R17>>>
<<<BEGIN SLIP24>>>
2026-09-06 · F260 R17 (reviewer) · The round-17 block's header-note pair for `docs/roadmap/features/T2_F260.md` anchored its FROM on the file's OLDEST line, "Registered 2026-08-31 by operator order amend0831-vocab-registrations.", and appended the new BUILT sentences directly after it — but that header block carries a SECOND, later line, "Rewritten 2026-09-05 by operator order amend0905-vocab-rebuild", so the applied result reads 2026-08-31, then 2026-09-06, then 2026-09-05. The worker applied it byte for byte and declared the interleave, which was right. THE LESSON is that an append-shaped pair whose purpose is to EXTEND a block anchors on the LAST line of that block, not the first: the FROM must read forward far enough to prove what the new text lands in front of, which is the same obligation an insert-after pair has and which this pair had only for the line it replaced. Nothing under `packages/`, `apps/`, `tests/` or `docs/` is false as a result — every sentence in that header is true, and only their order is odd — so no id is spent (amend0827-process-diet rule 2).
<<<END SLIP24>>>

## Done when — the gates. Report ONE LINE PER GATE with its REAL exit code.

**G1 TRANSPORT — one comparison.** Before staging C0a, sha256 over the
delegation's source file, `.agent/authored/f260-r18.md` and
`.agent/last_block.md`; all three must equal the digest the delegation names.
Both writes are `shutil.copyfile`, each proved with `filecmp.cmp(shallow=False)`.

**G2 THE RECORD, at C2.** For `.agent/live_review.md`, three readings:
(a) exact image — `post == pre + b"\n" + GATE_R17 + b"\n"` True and
`post[:len(pre)] == pre` True; report both byte counts;
(b) structural, independent of (a) — split the WHOLE file on a blank line and
compare the last N units against the slice's N paragraphs IN ORDER, N counted by
your script from the slice and never asserted by this block; report units before
and after;
(c) negative control IN MEMORY on a `bytes` object: flip one byte inside the FIRST
appended paragraph; both readers must REJECT; restore and both must ACCEPT with
the restored image equal to the disk image.
For `.agent/prose_slips.md`, byte equality is enough: `post == pre + b"\n" +
SLIP24 + b"\n"` True; report byte counts and units before and after.

**G3 THE PLAN, at C1.** `.agent/plan.md` equals the PLAN slice plus exactly one
trailing newline. Report byte count and line count; under the 50-line cap, and
carrying `## Goal` and `## Next Steps`.

**G4 THE FOUR REGISTRATION PAIRS, at C3.** For STATUSPAIR, READMECOUNT,
READMETIER and PINPAIR report FOUR numbers each: FROM count BEFORE (1); the
containment reading printed as the word `true` or `false`; FROM count AFTER; TO
count AFTER (1). All four are REWRITEs, so every FROM count after must be 0. Then
reconstruct each of `docs/roadmap/STATUS.md`, `README.md` and
`tests/docs/test_docs_consistency.py` independently from its pre-edit bytes with
only its own pairs applied — one boolean per file — plus that each still ends
with exactly one newline.

**G5 THE SIX DEPENDS-ON EDITS, at C3.** GENPAIR is applied once in each of its
five files; report PER FILE the FROM count before (1), after (0) and the TO count
after (1). F263PAIR is applied to `T2_F263.md`; report the same numbers, its FROM
count after also 0, because it too is a REWRITE. Then report that
`amend0906-split-placement` appears ZERO times in the five GENPAIR files after the
edit, and that `F272` appears exactly once in the `**Tier` line of all SIX.

**G6 THE NEW FILE, at C3.** `docs/roadmap/features/T2_F272.md` exists and its
bytes equal the F272FILE slice plus exactly one trailing newline — report the byte
count and the boolean, that it holds ZERO lines beginning `<<<BEGIN ` or `<<<END `,
that its first line begins `# T2_F272 — `, and that `git status --porcelain`
showed it as a NEW file before staging.

**G7 THE LEDGER AND THE README AGREE, after C3, then the suites.** Report: feature
detail files 272; STATUS entries 272; the sorted set of ids missing from
`range(1, 273)` for both, empty for both; `^- \[x\] F` 73 and `^- \[~\] F` 1;
the README numeral parsed by `^(\d+) of (\d+) registered items accepted\.` reading
73 and 272; `TOTAL_FEATURES` 272; and F272's filename tier and STATUS tier, both
2. Then, run SERIALLY in the PRIMARY checkout:

    python3 -m pytest tests/docs/ -q -p no:randomly
    python3 -m pytest tests/orchestration/test_roadmap_index.py -q -p no:randomly
    python3 -m pytest tests/cli/test_golden_path.py -q -p no:randomly
    python3 -m apps.cli.grouped integrity check --json

Report each real exit code and pass count; the integrity check must report
`"passed": true` with `"fail_count": 0`. Report any `^FAILED` or `^ERROR` lines;
there must be none.

**G8 TREE, LINT AND STRUCTURE.** `python3 -m ruff check
tests/docs/test_docs_consistency.py` — that is the one `.py` file this round
edits; report its exit code and confirm by counting the `.py` files in `git diff
--name-only 7a1ce69d..C3` yourself. Then `git status --porcelain` EMPTY;
`git ls-files .remedy-wt` EMPTY; every commit C0a through C3 single-parent with
its parent count reported; and each of their INSERTION counts — the `+` column of
`git diff --numstat`, never insertions plus deletions — reported and under 500.

## Handback

Rewrite `.agent/handoff.md`. Mandated sections: the Session block naming SESSION 7
of F260, round 18, rounds so far 18; a one-sentence context self-assessment; the
Range; the per-commit table with `+/-` from `git log --numstat`, never re-derived
by eye; External actions; Verification, one line per gate with its real exit code;
the Authored-text proofs; Deviations and assumptions; the Item-status table with
every bundle item and every gate appearing exactly once as `done`, `skipped` or
`deviated` with a reason; Open findings; and Next. Then
`git push -u origin feature/f260-one-world`.
