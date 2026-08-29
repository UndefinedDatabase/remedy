# F033 — Hunk-level diff approval · ROUND 1 · RESTART AND CLAIM

SESSION 1 of feature F033. Round 1, rounds so far 1.

You are the WORKER for this round. AGENTS.md is the highest authority and binds
you in full: the mandatory self-review loop before every commit, the Commit
Gate, small commits, push discipline. Do not review your own work and write no
verdict on it.

## Conventions (read once, they bind every slice below)

1. A SLICE is the bytes BETWEEN its `<<<SLICE <NAME>` and `<<<END <NAME>` lines,
   exclusive of both delimiter lines. Apply slices BYTE FOR BYTE. Never reflow,
   re-wrap, re-indent, correct spelling or "fix" anything inside a slice, even
   where it looks wrong. If a slice looks wrong, apply it anyway and say so in
   the handback's deviations.
2. The delimiter lines are transport only and never reach a target file. ANCHOR
   your extraction to the NAMED delimiter at line start — `<<<END RECORDF033R1`,
   not a bare `<<<END ` — because the RECORDF033R1 body legitimately quotes the
   tokens `<<<SLICE ` and `<<<END ` inline, mid-line and inside backticks. A
   naive search for the bare marker truncates that slice.
3. Every WHOLE-FILE slice ends with exactly one trailing newline. Apply it so the
   file ends with exactly one newline and no trailing whitespace is added.
4. Extract every slice from the COMMITTED blob you save at C0a — never retype one
   out of this prompt, and never reconstruct one by hand.
5. Guard re-expressions: this shell rejects loops, `$( )`, `${arr[0]}` and `cp` by
   FORM. Route extraction, application and measurement through Python scripts under
   the gitignored `.remedy-wt/`. Use `shutil.copyfile`, not `cp`. Python here is
   3.10 and forbids a backslash inside an f-string expression, so hoist every regex
   into a named module-level variable. Report every re-expression you make.
6. Capture REAL exit codes. Where you pipe a command, recover the true status —
   piping to `tail` otherwise masks a red.

## Why this round is a RESTART

A previous session claimed F033 on a branch `feature/f033-hunk-approval`, cut
from `32cde54e`, did one round and halted round 2 on a `.agent/STOP` sentinel.
That branch still exists at `ed040812`, locally and on `origin`, and it is 138
commits BEHIND `origin/main` — F256 and F257 have merged since, and F256 rewrote
the very diff surface F033 builds on. The reviewer has ruled that F033 restarts
from current `main` and that the parked branch is retained untouched as history.
The ruling, its alternatives and its reversal are DECISION F033 D1, which the
RECORDF033R1 slice writes into the record this round.

You do not check out, merge, rebase, delete or push the parked branch. You do not
force-push anything. The only thing you take from it is what the SURVEY asks for,
and you take that with `git show`, never by checking it out.

## Goal

Restart F033 on a clean branch from current `main`, claim it, book the three
paragraphs the record is owed — the F257 R12 closure verdict, DECISION F033 D1,
and the new finding R-0738 — and survey the hunk-identity surface T001 builds on.

## Bundle (in this order)

- the branch
- C0a save this block · C0b mirror it
- C1 `.agent/plan.md`
- C2 the three record paragraphs into `.agent/live_review.md`
- C3 the F033 claim in `docs/roadmap/STATUS.md`
- C4 `.agent/context.md`
- C5 the handback, carrying the SURVEY

## Change set — these paths and nothing else

    .agent/authored/f033-r1.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    docs/roadmap/STATUS.md
    .agent/context.md
    .agent/handoff.md

No other path is created, edited or deleted. Scratch under `.remedy-wt/` is
gitignored and is not part of the change set; leave it untracked.

## Step 0 — take main, then cut the branch

The Open PR Gate is already DISCHARGED for this round: pull request 221 was
merged at merge commit `bd8d9529`, which is `origin/main`. Confirm that rather
than assume it, and report the output verbatim:

    gh pr list --state open --json number,headRefName,baseRefName,isDraft

It must come back as an EMPTY list. If any pull request comes back, STOP, write
the handoff and end — do not merge anything and do not guess.

Then:

    git checkout main
    git pull --ff-only
    git rev-parse HEAD
    git checkout -b feature/f033-hunk-approval-v2

`git rev-parse HEAD` must print `bd8d952942d8ec1d243d787ccfe16e0ad04360d2`. That
commit is the BASE for every "before" reading in the gates below; call it BASE.
If it prints anything else, STOP and hand off — the ground moved and every
number in this block was measured against `bd8d9529`.

Never force-push. Never rewrite history. Delete no branch.

## The commits

### C0a — save this block

Copy the reviewer's block file `.remedy-wt/f033-r1-block.md` byte for byte to
`.agent/authored/f033-r1.md` with `shutil.copyfile`. Do not retype it and do not
edit it in passing. Commit alone: `docs(f033): save the round 1 restart block`.

### C0b — mirror it

Copy that committed file to `.agent/last_block.md` with `shutil.copyfile` so the
two are ONE blob id. Commit alone:
`chore(f033): mirror the round 1 block to last_block`.

### C1 — the plan

Replace `.agent/plan.md` ENTIRELY with the PLANF033R1 slice.
Commit alone: `docs(f033): open the plan for the hunk approval feature`.

### C2 — the record

APPEND to `.agent/live_review.md`: one newline, then the RECORDF033R1 slice. The
file's existing bytes are untouched and remain a byte PREFIX of the result.
Commit alone: `docs(f033): book the F257 closure verdict, DECISION D1 and R-0738`.

### C3 — claim F033

In `docs/roadmap/STATUS.md` replace the STATUSFROM slice with the STATUSTO slice.
One occurrence, one replacement, nothing else in the file changes.
Commit alone: `docs(f033): claim F033 in STATUS`.

### C4 — the context

Replace `.agent/context.md` ENTIRELY with the CONTEXTF033R1 slice.
Commit alone: `docs(f033): set the branch context for F033`.

### C5 — the handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md, carrying the
SURVEY below. Commit alone: `docs(f033): hand back the round 1 restart result`.

Push with `git push -u origin feature/f033-hunk-approval-v2`. Do NOT open a pull
request this round and do NOT merge anything.

## The slices

<<<SLICE PLANF033R1
# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 1 of this feature.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| restart F033 from current main | done | round 1, DECISION F033 D1 |
| book the F257 R12 closure verdict | done | round 1, amend0827 rule 1 |
| register R-0738 | done | round 1 |
| claim F033 in STATUS | done | round 1 |
| survey the hunk-identity surface | done | round 1, in the handback |
| T001 stable ids, JSON v2, shared helper | open | round 2 onward |
| T002 approve_hunks, subset atomicity, ledger | open | |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. Author T001 from the survey: the content-hash id function, its home, the
   `DIFF_VIEW_VERSION` bump and the stability property tests.
2. Consolidate the diff-repair hunk helper onto the shared identity, keeping
   `tests/orchestration/test_diff_repair.py` green.
3. T002's command, its validation and the all-or-nothing subset apply.

## Risks
- The shared-helper consolidation crosses two modules that ship today; their
  regression suites are the safety net and are named in every order touching them.
- `packages/orchestration/diff_parser.py` is PURE and TOTAL by its own docstring
  and never raises on malformed input. Content-hash ids must not change that.
- The parked branch `feature/f033-hunk-approval` at `ed040812` holds a 574-line
  inventory taken at `32cde54e`, before F256 rewrote the diff surface. It is
  INPUT to be re-derived, never a source of fact.
<<<END PLANF033R1

<<<SLICE RECORDF033R1
Gate: F257 R12 — THE CLOSURE ROUND, gated here in the next feature's first round because Rule A4 leaves it no successor on its own branch (docs/agents/planner_reviewer_prompt.md §4 item 13, the branch terminator, with amend0827 rule 1 fixing where the entry lands). THE ROUND PASSED AND F257 IS CLOSED. Every gate was re-executed by the reviewer at `1209dfb9` from scripts of its own under `.remedy-wt/`, and every reading reproduced. STRUCTURE: four SINGLE-PARENT commits of 349, 275, 8 and 215 insertions, each under 500; the range's path set equals the declared change set exactly, with nothing touched that the block did not name and nothing named that it did not touch; `1209dfb9` is the LAST commit and carries exactly `.agent/handoff.md`, `.agent/plan.md`, `README.md`, `docs/roadmap/STATUS.md` and `scripts/self_use_queue.json`; `git ls-files .remedy-wt` reads 0; and the `<<<SLICE `/`<<<END ` residue is 0 and 0 in all four applied targets against a 14/14 control in `.agent/authored/f257-r12.md`. TRANSPORT: the committed block blob is 21223 bytes at sha256 `c9a79545…7fbdfa`, EQUAL to the reviewer's own scratch original `.remedy-wt/f257-r12-block.md`, which was written in the PRECEDING session and therefore predates the worker — so this reading covers delivery from reviewer to worker and not merely the worker's self-consistency, which is the distinction R-0705 exists to force; and `b8a17299:.agent/authored/f257-r12.md` and `b8a17299:.agent/last_block.md` are ONE blob id `d59edbe9…ae124`. THE RECORD APPEND at `d053b2f7`: 1420016 bytes plus one newline plus a 2862-byte slice equals 1422879, the committed blob exactly, with the pre-round blob a byte PREFIX and the file ending in exactly one newline; the NEGATIVE CONTROL flipped one byte at offset 1420056, proved to lie inside the appended paragraph, reads False as it must. THE LEDGER at that commit: registered `^- R-\d+ — ` 298 to 298 all DISTINCT, `Done: R-\d+ — ` 44 lines over 42 distinct ids, `Landed: R-` 11, `Gate: F\d+ R\d+ — ` 116 to 117, the open set UNMOVED at 256, and `^Gate: F257 R11 — ` reading exactly 1. THE CLOSURE EDITS at `1209dfb9`: all five pairs are REWRITES by a mechanical containment test — TO contains FROM: false, one reading per pair — each FROM occurring once in the base blob and zero times after, each TO exactly once after; and per FILE the committed blob equals the base blob with ONLY its own pairs applied, `docs/roadmap/STATUS.md` 31864 to 32134, `README.md` 8327 to 8821 and `scripts/self_use_queue.json` 2519 to 2523, every reading True. The claimed STATUS line is BYTE-IDENTICAL to the STATUSTO slice at exactly one occurrence, which is the closure protocol's apply-verbatim proof, and `.agent/plan.md` equals PLANFINALF257 exactly at 1923 bytes over 39 lines. THE LEDGER PINS: `- [x] F\d{3} — ` reads 62 and the README's "62 of 257 registered items accepted" agrees with it, its 257 equal to the `TOTAL_FEATURES` pin in `tests/docs/test_docs_consistency.py`; `- [~] F\d{3} —` reads 0; the first `- [ ] F\d{3} — ` line is F033 and the README `Next:` clause names F033; and the tier-5 Done cell of 10 equals the 10 accepted ids owning a `docs/roadmap/features/T5_F???.md` file — F008, F009, F021, F022, F031, F032, F037, F255, F256 and F257. THE SUITES were re-run by the reviewer SERIALLY in the primary checkout, one pytest process at a time, every path first resolved on disk: `tests/docs/test_docs_consistency.py` 295 passed, `tests/orchestration/test_self_use_job.py` 18 passed, `tests/orchestration/test_self_use_queue.py` 18 passed, and the canary `tests/cli/test_golden_path.py` 42 passed, every REAL exit 0. THIS IS THE READING R-0737 EXISTS FOR, and it is taken here with the queue exhausted on disk in the primary checkout rather than inside a worktree: through the SHIPPED loader `next_self_use_item()` answers None, `pending_self_use_items()` answers the empty tuple, `load_self_use_queue()` still returns its single item and that item's `consumed_by` reads `F257` — the consumption proved through the code rather than through the JSON text, with both self-use suites green in exactly that state. G8 is the one gate round 12 could not take, because its readings are ABOUT the commit that would have had to carry them; the reviewer measured it here instead, which is what §4 item 31 requires of any value a handback routes to a round report. CI on `1209dfb9` completed `success`. That round registered no finding and resolved none, and the open set stood at 256.

DECISION F033 D1 — F033 RESTARTS FROM CURRENT `main` ON A NEW BRANCH, AND THE PARKED BRANCH IS RETAINED UNTOUCHED AS HISTORY. THE SITUATION: a previous session claimed F033 on `feature/f033-hunk-approval`, cut from `32cde54e`, completed one round and halted round 2 on a `.agent/STOP` sentinel; that branch still exists at `ed040812` on both local and `origin`, is 138 commits BEHIND `bd8d9529`, and carries a 574-line `.agent/f033_inventory.md` taken before F256 and F257 merged. CHOSEN: cut `feature/f033-hunk-approval-v2` from `bd8d9529` and treat the parked branch's inventory as INPUT to be re-derived rather than as fact. ALTERNATIVE 1, resume the parked branch and merge `main` into it, REJECTED: reconciling `.agent/live_review.md` between a branch that reset the record at F037 R27 and a `main` that has since booked the whole of F256's and F257's round history means hand-resolving a conflict inside the APPEND-ONLY permanent record, which is the one artifact this workflow exists to keep honest, and docs/agents/self_drive_protocol.md G2 forbids the rebase that would otherwise linearise it. ALTERNATIVE 2, delete the parked branch and reuse its name, REJECTED outright: G2 forbids branch deletion. WHY THE STALENESS IS DISQUALIFYING AND NOT MERELY INCONVENIENT: F256 was "Diff viewer completion" and it rewrote exactly the surface F033 builds on — measured between `32cde54e` and `bd8d9529`, `apps/ui/src/components/diff/DiffView.tsx` moves by 192 added lines, `apps/ui/src/components/diff/DiffView.module.css` by 63 and `apps/ui/src/components/diff/DiffFileSidebar.tsx` by 45, and `tests/ui_server/test_diff_endpoint.py` is 298 lines that did not exist — so an inventory answering questions about the hunk id, the viewer's readers and the diff endpoint at the older commit is stale precisely where this feature needs it to be right. HOW TO REVERSE: the parked branch is untouched at `ed040812`; `git checkout feature/f033-hunk-approval` restores that state exactly and `git show ed040812:.agent/f033_inventory.md` retrieves the inventory at any time, so nothing is lost by this ruling and it can be undone by a later relay without recovering anything from a session.

- R-0738 — Medium, A TASK REPORTS ITS CHANGES AS `applied` WHEN ANY ONE OF THEM IS APPLIED, SO NO PARTIAL APPLY STATE IS TELLABLE FROM A COMPLETE ONE. In `packages/orchestration/ui_server.py`, read at `bd8d9529`, the per-task fold over change apply states is `apply_states = [getattr(c, "apply_state", "") for c in changes]` followed by `if "applied" in apply_states: apply_by_task[tid] = "applied"`, then `elif "reverted" in apply_states: … "reverted"`, else `"not_applied"`. Membership, not agreement: a task holding eight changes of which ONE applied reports `applied`, and the surface a human reads cannot distinguish it from a task all eight of which applied. THE CONTRAST THAT MAKES THIS A DEFECT RATHER THAN A CHOICE sits three lines above it in the same loop, over the same `changes` list: the proof-status fold takes `applicable = [p for p in proofs if p != PROOF_NOT_APPLICABLE]` and asks `all(p == PROOF_VERIFIED for p in applicable)`, reserving a distinct `"incomplete"` state for the mixed case. One fold in this function models partial truth and the fold beside it does not. WHY THIS IS F033's AND NOT A DRIVE-BY: F033's Goal & Done requires that "every partial state renders truthfully in viewer and report" and its Design names the report line "partially approved (5/8 hunks)"; hunk-level approval makes the mixed case the NORMAL case rather than an edge one, so this fold moves from understating a rare state to misreporting the state the feature exists to produce. WHY MEDIUM AND NOT HIGH: nothing is applied that should not be, and no apply operation is wrong — the defect is confined to how the outcome is REPORTED, and today a mixed apply state is rare because nothing yet produces one deliberately. THE FIX is to give the apply fold the same shape as its proof-status neighbour: an agreement test rather than a membership test, with a distinct partial state carried through to the viewer badge, the node glyph and the report line, and the count of applied changes against the total available where the surface has room for it. Resolved when a task with a mixed apply state renders as partial on all three surfaces, proved by a test that builds the mixed case explicitly rather than by one that observes whatever the fixture happens to produce.
<<<END RECORDF033R1

<<<SLICE STATUSFROM
- [ ] F033 — Hunk-level diff approval
<<<END STATUSFROM

<<<SLICE STATUSTO
- [~] F033 — Hunk-level diff approval
<<<END STATUSTO

<<<SLICE CONTEXTF033R1
# Context — F033 Hunk-level diff approval

## Active Branch
feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge commit
of pull request 221. The parked branch `feature/f033-hunk-approval` at
`ed040812` is a previous attempt, retained as history under DECISION F033 D1 and
never checked out, merged or deleted by this feature.

## Scope
Feature F033, `docs/roadmap/features/T5_F033.md` — stable content-hash hunk ids,
the `approve_hunks` command with an all-or-nothing subset apply, and the
rejection-to-repair loop with truthful partial-state rendering.

## Do not touch
Applicator internals, fence rules and review verdict semantics, per the feature
file's own Do-not-touch. `packages/orchestration/diff_parser.py` stays PURE and
TOTAL as its docstring rules: text in, plain data out, no file system, no
subprocess, no network, and it NEVER raises on malformed input.
`docs/roadmap/ROADMAP.md` is not edited.

## Assumptions
- The hunk id is a hash of the path plus the old-side context normalised for
  whitespace, so an edit elsewhere in a file leaves other hunks' ids unchanged.
- `DIFF_VIEW_VERSION` is the declared seam for that change: the feature file and
  `packages/orchestration/diff_parser.py` both say so, and version 1 has never
  been served to an endpoint.
- One hunk identity spans repair and approval; the v1-local helper in
  `packages/orchestration/diff_repair.py` retires onto it.

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
- Destructive verification runs only inside a disposable git worktree, never in
  the primary checkout, which satisfies `git status --porcelain` empty at every
  verdict.
- THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE. The full contract those
  readers hold over the three state files, so a rewrite is checked against it
  directly rather than rediscovered from a red: this file carries
  `## Active Branch`, a `feature/` branch name, a roadmap feature id matching
  `\bF\d{3}\b` and the word `Steps`; `.agent/plan.md` carries `## Goal`,
  `## Next Steps` and a feature id; `.agent/live_review.md` carries `Steps`.

- A new module under `packages/orchestration/` is swept by repo-wide guards that
  name no path: the `REMEDY_DATA_DIR` single-reader invariant, the path-utils
  single-implementation invariant, the bare-`except: pass` ban, and the
  development-artifact boundary.

## Steps
The item-status table for this feature lives in the `## Current Step` section
of `.agent/plan.md`. This file deliberately does not restate it — a second copy
of the map is what fell out of step and cost F022 a finding.
<<<END CONTEXTF033R1

## The SURVEY — answer in the handback, write no file for it

Read the code at BASE and answer each item with PATH plus SYMBOL and a line
number. Where the answer is "none", say so and say what you grepped for. This is
the material round 2's T001 order is written from, so a guess is worse than a gap.

- **S1 — where hunk identity lives today.** Every place a hunk gets an id or an
  identity-like key: the provisional `"<file_index>:<hunk_index>"` in
  `packages/orchestration/diff_parser.py`, and whatever identifies a `RepairHunk`
  in `packages/orchestration/diff_repair.py`. Report both shapes exactly.
- **S2 — the consumers.** Every reader of `DIFF_VIEW_VERSION` and every reader of
  a hunk `id`, across `packages/`, `apps/ui/src/` and `tests/`. One line each.
- **S3 — what pins version 1.** Every test asserting `DIFF_VIEW_VERSION == 1`, or
  asserting an id of the literal form `"<n>:<m>"`. These are the tests a bump to 2
  must move, so an omission here becomes a red round 2.
- **S4 — does the UI parse the id?** In `apps/ui/src/components/diff/DiffView.tsx`,
  is the hunk `id` treated as an OPAQUE string, or is it split, indexed or parsed?
  Quote the lines. A parse is a blocker for content-hash ids and must be named now.
- **S5 — subset apply.** Does `packages/orchestration/repo_applicator.py` already
  expose a way to apply a SUBSET of hunks atomically, or must T002 build one?
  Name the entry point if it exists.
- **S6 — what the parked inventory got wrong.** Run
  `git diff --stat 32cde54e..bd8d9529` restricted to
  `packages/orchestration/diff_parser.py`,
  `packages/orchestration/diff_view_source.py`, `apps/ui/src/components/diff/`
  and `tests/ui_server/`, and report the per-file result. Read
  `git show ed040812:.agent/f033_inventory.md` — do NOT check that branch out —
  and name which of ITS answers about those paths the diff invalidates. Report
  only that; do not port the inventory this round.

## Done when — the gates

Run every one. Record the REAL exit code and the actual numbers, never the word
"green". One line per gate in the handback.

- **G1 HYGIENE.** `.agent/STOP` read from disk twice — before C0a and before C5 —
  and absent both times; if it ever exists, finish the current commit, write the
  handoff and end. `git status --porcelain` empty after EVERY commit.
  `git branch --show-current` reads `feature/f033-hunk-approval-v2` at C0a through
  C5. No force-push, no history rewrite, no branch deletion, and the parked branch
  `feature/f033-hunk-approval` is not checked out, merged or moved — confirm
  `git rev-parse feature/f033-hunk-approval` still reads `ed040812` at C5.
- **G2 TRANSPORT.** One digest comparison, and no expected value is stated here
  because a block cannot carry its own digest: compute sha256 of the committed
  blob `<C0a>:.agent/authored/f033-r1.md` and sha256 of the reviewer's own
  original `.remedy-wt/f033-r1-block.md`, and report BOTH digests, BOTH byte
  lengths, and whether they are EQUAL. They must be equal. The reviewer holds
  that original and re-checks the value you report against it. Then
  `git rev-parse <C0b>:.agent/authored/f033-r1.md` and
  `git rev-parse <C0b>:.agent/last_block.md` must print ONE identical blob id.
- **G3 THE RECORD APPEND at C2.** Two independent readers, because a byte reader
  and a structural reader fail differently. (a) BYTES: the
  `.agent/live_review.md` blob at BASE, which must be 1422879 bytes, plus one
  newline, plus the RECORDF033R1 slice, must equal the C2 blob byte for byte;
  report all three lengths, and confirm the BASE blob is a byte PREFIX of the C2
  blob and that the C2 blob ends in exactly one newline. (b) STRUCTURE: let N be
  the number of blank-line-separated paragraphs your script COUNTS in the slice —
  report N, do not assume it — and compare the LAST N blank-line units of the C2
  file against the slice's N paragraphs IN ORDER, each one equal. NEGATIVE
  CONTROL: flip one byte at an offset your script PROVES lies inside the FIRST
  appended paragraph, and report that BOTH readers then reject it. A control that
  does not go False means the reader is blind — say so rather than passing the gate.
- **G4 THE LEDGER at C2.** At BASE and at C2, count `^- R-\d+ — ` with its
  distinct-id count, `^Done: R-\d+ — ` lines with distinct ids, `^Landed: R-`,
  and `^Gate: F\d+ R\d+ — `. Report the OPEN SET as
  `len(set(registered) - set(resolved))` at both. Expected, and each is a reading
  you take rather than repeat: registered 298 to 299 all DISTINCT, `Done:` 44
  lines over 42 distinct ids UNMOVED, `Landed:` 11 UNMOVED, `Gate:` 117 to 118,
  the open set 256 to 257 — the single id this round registers. Report
  `^Gate: F257 R12 — ` and `^- R-0738 — ` at C2; each must read exactly 1, and
  `^- R-0738 — ` must read 0 at BASE.
- **G5 THE CLAIM at C3.** Count STATUSFROM in the BASE blob (must be 1) and in the
  C3 blob (must be 0); count STATUSTO in the C3 blob (must be 1). Print the
  containment test's own output — the words `TO contains FROM: false` — and note
  that the pair is therefore a REWRITE, which is what makes the FROM-zero count
  the right proof. Then show the C3 blob equals the BASE blob with ONLY that one
  pair applied. Finally, in the C3 blob, `^- \[~\] F\d{3} —` must read 1 and
  `^- \[x\] F\d{3} — ` must read 62, unmoved.
- **G6 THE PROSE FILES.** Byte equality only. `.agent/plan.md` at C1 equals the
  PLANF033R1 slice exactly including the trailing newline — report bytes and
  `wc -l`, which must be under 50. `.agent/context.md` at C4 equals the
  CONTEXTF033R1 slice exactly. Then confirm the C4 blob contains each of
  `## Active Branch`, a `feature/` branch slug, a match of `\bF\d{3}\b`, the word
  `Steps` and the word `pytest` — the four state readers' full contract.
- **G7 THE SUITES.** First assert every path below resolves on disk and report the
  missing list; `pytest` exits 4 on a missing path and says so only quietly. Then
  run each SERIALLY, one pytest process at a time, in the PRIMARY checkout, as
  `python3 -m pytest -q <path>`, reporting the REAL exit code and the summary
  line for each: `tests/docs/`, `tests/orchestration/test_roadmap_index.py`,
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py`,
  `tests/orchestration/test_integrity_gate.py`, and the canary
  `tests/cli/test_golden_path.py`. Every one must exit 0. The reviewer ran all
  seven at `1209dfb9`, whose tree is the tree `bd8d9529` merged, and got 295, 30,
  497, 52, 21, 16 and 42 passed at exit 0 — so a red here is this round's doing.
- **G8 STRUCTURE.** Walk `git rev-list --reverse BASE..C4` mechanically, one
  reading per commit: each must have exactly ONE parent, and each must be under
  500 INSERTIONS — the `+` column of `git diff --numstat`, never insertions plus
  deletions. Report the per-commit list. C5's own numbers are NOT ordered here:
  a commit cannot carry its own insertion count, so the reviewer measures C5 at
  the next gate. Report the range's path set against the change set above, in
  BOTH directions — paths touched that it does not name, and paths it names that
  were never touched. Count `<<<SLICE ` and `<<<END ` in `.agent/plan.md`,
  `.agent/context.md` and `docs/roadmap/STATUS.md`: each must read 0, against
  `.agent/authored/f033-r1.md` as a non-zero control, whose count you report.
  `git ls-files .remedy-wt` must read 0.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It carries the
SESSION number (1), the round (1), BASE, the changed-files table with real `+/-`
from `git diff --numstat`, one line per gate with real numbers, the SURVEY
answers, the item-status table with every ordered item present exactly once, and
your deviations. It has no length cap. Write no verdict on your own work — the
reviewer gates this round.
