# STEP — F260 round 16: bring `origin/main` onto the branch and book round 15

Feature F260 "One world: mission → job → run", session 7, round 16.
Base for this round: `08dca210f8dd8e58c0e21b23fcb1e4b6ee9ffa93` (the branch tip,
identical to `origin/feature/f260-one-world`).

Frame convention: this block uses NO runs of repeated characters. Slice
delimiters are the single lines `<<<BEGIN name>>>` and `<<<END name>>>`.

## Goal

Merge `origin/main` into `feature/f260-one-world`, book the round-15 PASS verdict
and its prose slip into the record, and point `.agent/plan.md` at this session's
endgame. `origin/main` carries operator order amend0906-split-placement, which is
the rule that governs the split-and-close this session performs; the branch must
hold that rule before the round that applies it.

## Bundle, in this exact order

- C0a — save this block verbatim to `.agent/authored/f260-r16.md`
- C0b — mirror the same source file to `.agent/last_block.md`
- C1 — the merge of `origin/main`, with `.agent/decisions.md` resolved
- C2 — `.agent/plan.md`, whole-file replacement from the PLAN slice
- C3 — `.agent/live_review.md` gains GATE_R15; `.agent/prose_slips.md` gains SLIP20
- C4 — rewrite `.agent/handoff.md` as the handback

## Change set — no path outside this list may be written

- `.agent/authored/f260-r16.md` (C0a)
- `.agent/last_block.md` (C0b)
- every path the merge C1 carries from `origin/main`, and no other (see G2)
- `.agent/plan.md` (C2)
- `.agent/live_review.md` (C3)
- `.agent/prose_slips.md` (C3)
- `.agent/handoff.md` (C4)

## Constraints

1. Apply every slice BYTE FOR BYTE. If a slice looks wrong, apply it as written
   and declare the problem in the handback. Never adjust a slice, a test or a
   gate to make a reading come out as ordered.
2. Terminal-byte measurements, taken by the reviewer at `08dca210`:
   `.agent/live_review.md` 947109 bytes ending in exactly ONE newline;
   `.agent/prose_slips.md` 118817 bytes ending in exactly ONE newline. Derive each
   append recipe from the target's OWN measured terminal byte and `assert` that
   count is 1 before writing, so a wrong measurement aborts rather than corrupts.
3. C1 PRECEDES C2, and this is a declared departure from
   docs/agents/planner_reviewer_prompt.md §3 item 23, which asks a round touching
   the finding ledger to advance `.agent/plan.md` as its first substantive commit.
   The reason is stated rather than left for you to discover: C1 rewrites
   `.agent/decisions.md` as a merge resolution, and running that resolution after
   a hand-written commit in the same directory risks re-resolving a file that has
   moved underneath it. **`.agent/plan.md` becomes current at C2**, before the
   ledger append at C3, which is the property item 23 exists to protect.
4. C3 writes `.agent/live_review.md` FIRST and `.agent/prose_slips.md` SECOND,
   in ONE commit.
5. Do NOT author a `Done:` or `Landed:` paragraph for any finding this round.
   GATE_R15 is a `Gate:` record and registers nothing; the open set does not move.
6. Do not touch any file under `packages/`, `apps/`, `tests/`, `docs/` or
   `scripts/` by hand. C1 may change such files ONLY as the merge carries them.
7. `.agent/STOP` does not exist at `08dca210`. If it appears at any point,
   finish the commit in flight, hand off and end (self-drive guardrail G6). Do
   not delete it and do not commit it.
8. `cmp` and `remedy` are denied in this sandbox. Use `filecmp.cmp(shallow=False)`
   plus sha256 for byte comparisons, and `python3 -m apps.cli.grouped` for the
   CLI. Take every exit code from a Python `subprocess.run(...).returncode`; the
   bash guard rejects `$?`, `$( )` and shell loop forms BY FORM.
9. Scratch goes under the gitignored `.remedy-wt/`. Never `git add` anything
   there. Remove any worktree you create BY EXACT PATH, never by glob.
10. The handback cannot table its own commit (the R-0149 pattern). Report C4's
    own numbers nowhere; the reviewer measures them at the next gate.

## C1 — the merge, and exactly how to resolve it

Run `git merge origin/main`. It will report exactly ONE conflict, in
`.agent/decisions.md`; every other path merges cleanly. The reviewer reproduced
this in a disposable worktree at `08dca210` and measured the resolution.

DO NOT hand-edit the conflict markers. Construct the resolved bytes
deterministically instead, from the three blobs:

    BASE   = git show b5cd6c20782283923f0e276d9479751e475b9359:.agent/decisions.md
    OURS   = git show 08dca210:.agent/decisions.md
    THEIRS = git show origin/main:.agent/decisions.md

    resolved = BASE + OURS[len(BASE):] + THEIRS[len(BASE):]

The reviewer measured, at `08dca210` and at `origin/main`: BASE is 836338 bytes
and is a byte-exact PREFIX of both OURS (845072 bytes) and THEIRS (839303 bytes);
the OURS tail is 8734 bytes and the THEIRS tail is 2965 bytes. The construction
keeps both appends in full, ours first — the three F260 rulings D5, D6 and D7 —
then the operator's amend0906-split-placement DECISION, which is the order the
file reads in on `origin/main` and leaves the operator order as the file's last
word. Write `resolved` over `.agent/decisions.md`, `git add` it, and complete the
merge with `git commit --no-edit` (or `git merge --continue`).

C1 is a MERGE COMMIT and therefore has TWO parents. That is expected and is the
only two-parent commit this round; every other commit is single-parent.

## The slices

<<<BEGIN PLAN>>>
# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20. Rounds 1 to 15 are
reviewed and 2 to 15 PASSED. T001 is CLOSED. T002 is open on the RUN side: the job
record has MOVED, both resolvers return `str`, the ping-pong and run-log stores
have one spelling on the production side, and a run is now an INVOCATION rather
than an event (DECISION F260 D7).

## Goal

SESSION 7 REACHES THE SOFT LIMIT — 25 rounds or 7 sessions, whichever comes first,
and this is session 7. The obligation is a SCOPE REPORT and then the standing
default of operator amendment amend0905-throughput: SPLIT-AND-CLOSE, executed on
this session's own authority. F260 closes at the scope it has actually built; the
remaining scope is registered as a new follow-up feature placed directly after
F260, per operator order amend0906-split-placement.

## Current Step

Round 16 brings `origin/main` onto the branch — it carries
amend0906-split-placement, the rule that governs this session's split — books the
round-15 PASS verdict and its prose slip into the record, and rewrites this plan.

## Next Steps

1. Register the follow-up feature: its detail file, its STATUS line directly after
   F260's inside the same tier heading, the README counters, the TOTAL_FEATURES
   pin and the downstream "Depends on" lines, in ONE commit; a DECISION records
   the split and how to reverse it.
2. The integration gate: the full suite at the branch head and at the merge base.
3. Closure part 1: the self-use item, the evidence job and the review zip.
4. Closure part 2: the verdict bookings and the ledger rotation.
5. Closure part 3: the STATUS accepted flip, the README sync, the handback and the
   pull request, which is left UNMERGED as the operator's review window.

## Risks

- The feature file's Orchestrator brief names the split point "between T003 and
  T004"; this split falls inside T002 and therefore amends that brief. It is ruled
  as a DECISION and proceeded under, never asked as a question
  (docs/agents/planner_reviewer_prompt.md §4 item 7).
- README.md and docs/roadmap/STATUS.md may never disagree in any committed state,
  so the registration counters and the closure flip each land in one commit.
<<<END PLAN>>>

<<<BEGIN GATE_R15>>>
Gate: R15 — the F260 R15 entry. R15 GAVE THE TIMELINE ONE RUN ID PER PROCESS, SO AN INVOCATION IS ONE RUN INSTEAD OF ONE EVENT. VERDICT PASS. Range `1d344b485ce6c4e5e7768c6ab001a10bf8ab69d2`..`30da0b702f9374f960dd1829a2afe9a92fad9f63`, seven commits, all single-parent, in exactly the bundle's ordered sequence C0a to C5 with nothing added, dropped or reordered; that range was the branch tip and `origin/feature/f260-one-world` named the same object when the verdict was written. The reviewer re-ran the round's gates itself rather than reading the handback's numbers. TRANSPORT: the reviewer's scratchpad original `.remedy-wt/f260-r15-block.md` still existed at review time, so the primary disk-to-disk comparison was available and the §4 item 9 digest fallback was NOT used; that file, `.agent/authored/f260-r15.md` and `.agent/last_block.md` all hash to `454d291c41432e5c296dc56b28bbaabbcefa1c770f5d18b1555361acb4983d84` at 32568 bytes. Per §3 item 37 that chain covers the reviewer's scratch file, the worker's saved copy and the mirror — a COPY chain in which nothing is retyped — and it is not a claim about the bytes emitted into a prompt. SLICES, extracted from the COMMITTED authored copy and never from a retype: `.agent/plan.md` equals the PLAN slice plus one newline at 2531 bytes and 48 lines, carrying `## Goal` and `## Next Steps`; `.agent/live_review.md` equals its pre-image plus GATE_R14 then FIND816 in that order, 937682 to 947109 bytes, blank-line units 435 to 437; `.agent/decisions.md` the same shape for DEC_D7, 842038 to 845072 bytes, units 1893 to 1894; `.agent/prose_slips.md` the same shape for SLIP18 then SLIP19, 117457 to 118817 bytes, units 148 to 150. All twelve marker lines occur exactly once and ZERO lines beginning `BEGIN ` or `END ` reached any target file. CENSUS, counted by script at `30da0b70`: `^Gate: ` 24, registrations 301 over 301 DISTINCT ids, `^Done: ` 5 lines over THREE distinct ids, OPEN SET 298 BY DISTINCT ID; `R-0816` registered and carrying no `Done:` paragraph, which is correct because only reviewer-authored text sets Resolved. THE DEFECT AND ITS FIX WERE BOTH MEASURED ON DISK, and the pair is the proof: the same probe, run against the SHIPPED `timeline.append_run_event` and reading the `.jsonl` bytes it left rather than asking the writer what it did, found FIVE files, five event lines and FIVE DISTINCT run_id values for one five-event resume at `1d344b48`, and ONE file, five lines and ONE distinct run_id at `30da0b70`; two jobs in one process at `30da0b70` land one file each in two directories that differ. That is finding `R-0816` measured before the fix and measured gone after it. MUTATION RED-PROOF, reproduced independently in the reviewer's own disposable worktree at `30da0b70` with `python3 -B`, `__pycache__` enumerated at 0 and module resolution confirmed to that worktree's own `timeline.py`: the revert target `run_id=_PROCESS_RUN_ID, ` counted EXACTLY 1 before mutating, control exit 0 at 140 passed, mutated exit 1 at 1 failed and 139 passed, restored exit 0 at 140 passed; that worktree's `git status --porcelain` and `git diff` against its own head were both empty, and it was removed BY EXACT PATH and pruned. IMPORT REACHABILITY, the one real risk this diff carried because `timeline.py` moved `run_log` to a MODULE-level import: all 262 modules under `packages/orchestration/` import successfully at `30da0b70`, and `run_log` to `timeline` and `timeline` to `run_log` both exit 0 in fresh interpreters, so no cycle was introduced in either order. SUITES AND LINT re-run by the reviewer: the four-file selection exit 0 at 264 passed; `ruff` over both edited files exit 0. NOT RE-RUN BY THE REVIEWER, stated so the evidence chain stays honest: `tests/orchestration/` and `tests/cli/`, which the worker reports exit 0 at 12805 passed with 10 skipped and at 1537 passed; the reviewer had re-run both itself at the round-14 head and read identical figures, and this round's production diff is four lines in one module whose blast radius is the import graph rather than behaviour — that graph was measured directly, at 262 of 262. ELEVEN DEVIATIONS WERE DECLARED AND ALL ELEVEN ARE UPHELD. The two needing a ruling were 3 and 4. Deviation 3 is a defect of the REVIEWER's own gate and not of the work: G6 ordered the mutation to redden "the three tests SPEC (2) adds" while only `test_all_events_of_one_invocation_share_one_run` can discriminate that mutation, because test (ii) appends ONE event per job and so still yields one file per job under per-event run ids, and test (iii) reads through `load_run_events`, which sorts by timestamp across the whole directory and returns append order under either behaviour — a fact the block's own FIND816 slice states, so the block contradicted itself and an honest worker had to spend a declared deviation on it. The gate's BINDING clause was the COLOUR, which the block itself says in as many words, and the colour was met; the worker correctly did not trip the STOP clause, which is armed for a GREEN mutation, and correctly did not adjust a test to satisfy a gate. Tests (ii) and (iii) are KEPT: they pin per-job separation and append order, which are real properties of DECISION F260 D7 and are what a later regression would break. Nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result, so per operator amendment amend0827-process-diet rule 2 this spends no id and is recorded as one dated line in `.agent/prose_slips.md`. Deviation 4 is `.agent/STOP`, which appeared mid-round as a zero-byte untracked file roughly twenty minutes after the round's last code commit and ended session 6 under self-drive guardrail G6; the worker finished the commit in flight, handed off, and neither deleted nor committed the sentinel, which is exactly right, and `git status --porcelain` reading `?? .agent/STOP` and nothing else is the one and only reason that tree reading was not empty at that verdict. The operator cleared the sentinel before session 7, which re-read that path from disk as Phase 1 rule 1 and found it absent.
<<<END GATE_R15>>>

<<<BEGIN SLIP20>>>
2026-09-06 · F260 R15 (reviewer) · Gate G6 of the round-15 block ordered the mutation to redden "the three tests SPEC (2) adds" while only ONE of the three can discriminate it: test (ii) appends one event per job, so a run id per event still leaves one file per job, and test (iii) reads through `load_run_events`, which sorts by timestamp across the whole directory — a fact the block's own FIND816 slice states two hundred lines above the gate, so the block contradicted itself and an honest worker had to spend a declared deviation on it. THE LESSON is that a gate naming WHICH tests must go red is making a reachability claim about each one, and each must be checked against the mutation separately before the gate is written; the safe form is the one the same gate already used for its colour — order the property, name the observer that can see it, and let the run report the rest. Reviewer-authored gate clause unattainable for two of the three tests it named; the colour clause was met, both tests are correct and were kept, and nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result; no id spent (amend0827-process-diet rule 2).
<<<END SLIP20>>>

## Done when — the gates. Report ONE LINE PER GATE with its REAL exit code.

**G1 TRANSPORT — one comparison.** Before staging C0a, sha256 over the delegation's
source file, `.agent/authored/f260-r16.md` and `.agent/last_block.md`. All three
must equal the digest the delegation names. Both writes are `shutil.copyfile` from
the source path, each proved with `filecmp.cmp(shallow=False)` = True. One reading,
not a chain of retypes.

**G2 THE MERGE.** Take these readings at C1:
(a) `.agent/decisions.md` is 848037 bytes and its sha256 is
`e161a74832cc6452f6fc2755d09de4bbd1fd8e3d223ec25b6410904e5cfef463`;
(b) the three-segment equality holds — the first 836338 bytes equal BASE, the next
8734 equal the OURS tail, and the remainder equals the THEIRS tail;
(c) lines beginning `<<<` + `<<<<`, lines exactly equal to seven `=` characters,
and lines beginning `>>>` + `>>>>` each count ZERO in the merged file. The
reviewer measured these three counts at 0 in BASE, OURS and THEIRS as well, so the
gate is not self-satisfied by pre-existing text;
(d) `git diff --name-only --diff-filter=U` is EMPTY;
(e) for every path in `git diff --name-only 08dca210..C1` OTHER than
`.agent/decisions.md`, the blob at C1 is byte-identical to the blob at
`origin/main` — the branch touched none of them, so the merge may not have
invented content. Report the path list and the count;
(f) C1 has exactly TWO parents and they are `08dca210` and `origin/main`'s tip.

**G3 THE PLAN.** `.agent/plan.md` at C2 equals the PLAN slice plus exactly one
trailing newline. Report its byte count and line count; it must be under the
50-line cap AGENTS.md sets, and must carry `## Goal` and `## Next Steps`.

**G4 THE RECORD APPEND.** For `.agent/live_review.md` at C3, three readings:
(a) exact image — `post == pre + b"\n" + GATE_R15 + b"\n"` is True, and
`post[:len(pre)] == pre` is True. Report both byte counts;
(b) structural, independent of (a) — split the WHOLE file on a blank line and
compare the last N units against the slice's N paragraphs IN ORDER, where N is a
number your script COUNTS from the slice and never one this block asserts. Report
the unit count before and after;
(c) negative control, run IN MEMORY on a `bytes` object so the primary checkout
never holds known-bad bytes: flip one byte inside the FIRST appended paragraph;
both readers must REJECT. Restore, and both must ACCEPT, with the restored image
equal to the disk image.

**G5 THE PROSE SLIP.** `.agent/prose_slips.md` at C3: `post == pre + b"\n" +
SLIP20 + b"\n"` is True. Report both byte counts and the blank-line unit count
before and after; the last unit must equal SLIP20 once its single trailing
newline is removed.

**G6 THE CENSUS, after C3.** Counted by script over `.agent/live_review.md`:
`^Gate: ` must read 25; registrations `^- R-\d{4} — ` must read 301 over 301
DISTINCT ids; `^Done: R-\d{4} — ` must read 5 lines over 3 distinct ids; the OPEN
SET BY DISTINCT ID must read 298 — unchanged, because this round registers and
resolves nothing. Also report that a line matching `^Gate: R15 — ` counts exactly
1, and that `.agent/live_review.md` and `.agent/prose_slips.md` each contain ZERO
lines beginning `<<<BEGIN ` or `<<<END `.

**G7 THE SUITES, run SERIALLY, in the PRIMARY checkout, after C3.** Report each
one's real exit code and its pass count:

    python3 -m pytest tests/docs/ -q -p no:randomly
    python3 -m pytest tests/cli/test_golden_path.py -q -p no:randomly
    python3 -m pytest tests/test_timeline.py tests/test_run_log.py tests/test_data_paths.py -q -p no:randomly
    python3 -m apps.cli.grouped integrity check --json

`tests/docs/` is in this list because C1 carries `docs/` changes from
`origin/main`. `tests/cli/test_golden_path.py` is the canary. The integrity check
must report `"passed": true` with `"fail_count": 0`. Report any `^FAILED` or
`^ERROR` lines; there must be none.

**G8 LINT, TREE AND STRUCTURE.** `python3 -m ruff check` over any file with a
`.py` extension in `git diff --name-only 08dca210..C3` — count them yourself and
report the count and the names; if there are none, say so and report the gate as
not applicable rather than inventing a target. Then: `git status --porcelain` is
EMPTY; `git ls-files .remedy-wt` is EMPTY; every commit C0a through C3 is
single-parent EXCEPT C1, which has two; and every commit's INSERTION count — the
`+` column of `git diff --numstat`, never insertions plus deletions — is reported
and is under 500. C1 is a merge commit and its diff against its first parent is
the honest reading for it; report that number and note it is a merge.

## Handback

Rewrite `.agent/handoff.md`. Mandated sections: the Session block naming SESSION 7
of F260, round 16, and rounds so far 16; a one-sentence context self-assessment;
the Range; the per-commit table with `+/-` taken from `git log --numstat` and
never re-derived by eye; External actions; Verification, one line per gate with
its real exit code; the Authored-text proofs; Deviations and assumptions; the
Item-status table with every bundle item and every gate appearing exactly once as
`done`, `skipped` or `deviated` with a reason; Open findings; and Next.

Then `git push -u origin feature/f260-one-world`. Create NO pull request. Merge
nothing. Never force-push.
