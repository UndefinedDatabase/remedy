### STEP T002 — F257 Self-use track, round 12 (THE CLOSURE COMMIT AND THE PR)

Goal: book the round 11 verdict, then CLOSE F257 — the `[x]` flip, the README
sync that may never disagree with it, the `consumed_by` edit that marks SU-001
consumed, the final `.agent/` state — and open the pull request. This is the last
round on this branch.

THE PR IS NOT MERGED. Closure-protocol step 6 defers the merge to the next
feature's Open PR Gate; the gap is the operator's manual-review window. Creating
the PR is in scope; merging it is forbidden.

Base: `f459c431`, the tip of `feature/f257-self-use-track` and the handback this
round starts from.

Bundle, in commit order:

- C0a save this block verbatim to `.agent/authored/f257-r12.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 book the F257 R11 verdict into `.agent/live_review.md`
- C2 THE CLOSURE COMMIT — and it is the LAST commit on this branch (Rule A4)
- then push and open the pull request

Change set — these paths and nothing else:

- `.agent/authored/f257-r12.md`
- `.agent/last_block.md`
- `.agent/live_review.md`
- `docs/roadmap/STATUS.md`
- `README.md`
- `scripts/self_use_queue.json`
- `.agent/plan.md`
- `.agent/handoff.md`

The last five are C2's, and C2 carries exactly those five and nothing else. There
is NO separate plan-advance commit this round: the plan committed at `f459c431`
already names the closure commit and the PR as the next steps, so it is current
for C0a, C0b and C1, and C2 replaces it with the final state. `.agent/candidates.md`
is NOT touched — the closure gate has raised no candidate; if one is raised later
it rides in its own commit under DECISION amend0827 D2.

RULE A4: the STATUS edit is the last commit on the branch. Nothing may follow C2
except, if the reviewer's closure gate raises one, a `.agent/candidates.md`-only
commit. Do not add a tidy-up commit, a lint fix or a second handoff rewrite after
C2.

### Constraints

0. BEFORE ANYTHING: report `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
   — it was `[]` when this block was written, and if it is not `[]` now, STOP and
   hand back without committing. Report `git rev-parse HEAD`, which must equal
   `f459c431`'s full sha, and `git branch --show-current`, which must be
   `feature/f257-self-use-track`. Create no branch. Never force-push and never
   rewrite history.
1. Apply every authored slice BYTE FOR BYTE — no reflow, rewording, retitling,
   correction or shortening. If a slice looks wrong, apply it as written and say
   so in the handback's deviations. THIS BINDS HARDEST ON THE STATUS LINE: it is
   reviewer-authored text that the closure protocol requires you to apply
   verbatim, and the handback carries proof it landed byte-identical.
2. The delimiter lines `<<<SLICE …` and `<<<END …` are transport only and never
   reach a target file.
3. Extract every slice from the COMMITTED blob with
   `git show <C0a>:.agent/authored/f257-r12.md`, never from this prompt's text.
4. AGENTS.md binds in full: the self-review loop before every commit, one
   logical step per commit, a clean tree, and the push.
5. Shell forms rejected by this session's guard are RE-EXPRESSED, never skipped
   and never weakened. Loops, `$( )`, `${arr[0]}`, `cp`, brace literals
   containing quotes, and every form of environment-variable assignment are
   rejected by FORM; route such work through a scratch script under the
   gitignored `.remedy-wt/`, and copy with `shutil.copyfile`. Capture real exit
   codes with `bash -c '<cmd>; echo "REAL_EXIT=$?"'` or from `subprocess`. This
   Python is 3.10: an f-string expression may not contain a backslash, so hoist
   any regex into a named variable. Report every re-expression.
6. THE APPEND CONVENTION: an appended slice is separated from the text before it
   by exactly ONE BLANK LINE and the file ends with exactly one trailing
   newline. Concretely, for a target whose last byte is already a newline, write
   one newline then the slice, the slice carrying its own single terminator.
   This constraint is the authority on separators; if a gate formula below
   disagrees, follow this constraint and declare the disagreement.
7. THE OPEN SET IS COUNTED BY DISTINCT ID, as
   `len(set(registered ids) - set(resolved ids))`. It reads 256 at `f459c431`.
   THIS ROUND REGISTERS NO ID AND RESOLVES NONE, so it must still read 256 at C1
   and the registered count must be UNMOVED at 298.
8. EVERY PAIR IS APPLIED BY EXACT MATCH. Each FROM block below occurs EXACTLY
   ONCE in its target at `f459c431` — the reviewer measured all five and each
   read 1. VERIFY THAT COUNT IS 1 BEFORE REPLACING, and if any is not 1, STOP and
   hand back without committing. Replace the FROM bytes with the TO bytes and
   change nothing else by that replacement.
   EVERY PAIR IS WHOLE-LINE AND ITS OWN TRAILING NEWLINE IS PART OF THE BYTES.
   Each FROM and each TO begins at a line start and ends with the newline that
   closes its last line, exactly as the slice extractor yields it — do not strip
   it and do not add another. The reviewer measured all five counts with the
   terminator included. One newline either way moves a count, which is why this
   is stated rather than left to reading.

### The authored slices

<<<SLICE GATEF257R11
Gate: F257 R11 — THE PACKAGE REBUILT AT THE REPAIRED HEAD. THE ROUND PASSED. Every gate was re-executed by the reviewer at `f459c431`. Transport EQUAL at sha256 `8d258889…57fa9a` over 23977 bytes with ONE blob id at C0b; the plan byte-equal at 2413 bytes over 45 lines. BOTH APPENDS RECONSTRUCTED SEPARATELY, each with its own negative control: `.agent/live_review.md` 1415933 → 1420016 from GATEF257R10, and `.agent/prose_slips.md` 17363 → 17728 from SLIPF257R11, the slip landing as exactly ONE line matching `^2026-\d\d-\d\d · F257 R10 · ` and the file carrying ZERO lines beginning `- R-`, which is what makes it a slip record and not a ledger. The ledger itself is UNMOVED at 298 registered all DISTINCT and 256 open, `Done:` 44 over 42 and `Landed:` 11 unmoved, `Gate:` 115 → 116, `^Gate: F257 R10 — ` reading 1. Both residues empty over five SINGLE-PARENT commits of 339, 214, 7, 10 and 2 insertions; `.remedy-wt` untracked at 0; and STATUS.md, README.md, the queue file and the repaired test file all ABSENT from the range.

THE BUNDLE AND THE PACKAGE WERE READ OFF DISK BY THE REVIEWER, NOT OFF THE HANDBACK. The fresh evidence directory holds 27 files and all eight closed-schema gates. All four verification runs satisfy `len(node_ids) == selected` at 18, 18, 295 and 42 with zero failed and zero skipped, every `test_files` list SORTED, and every `output_hash` equal to sha256 of its own `stdout_summary`. The package `remedy-review-20260829-031830-READY_FOR_REVIEW.zip` is 18265107 bytes and hashes to `0a4b5fc1…57acdd` under the reviewer's own sha256 over the archived file; its manifest reads `package_status` `READY_FOR_REVIEW`, `ready_gate_matrix.ok` True, `blocking_reasons` `[]`, `committed_review_subject.head_commit` `fb10b3754978d9fc4112b2818eb9e7e31f4fdc78` — EQUAL to C3 — and `base_commit` `f17b1d0d03e4042df8452b2019b719cbe4704b21`, the merge base with `main`.

THE RED CONTROL WAS OPENED AND READ, NOT TAKEN ON TRUST. `remedy-review-20260829-031910-BLOCKED_EVIDENCE.zip` carries `package_status` `BLOCKED_EVIDENCE` and `ready_gate_matrix.ok` False, with three blocking reasons naming the injected local absolute path, the resulting `node_ids` count of 19 against `selected` 18, and the unconfirmable VerificationTests total. It was built at REAL exit 0, the same exit code as the READY package. The status is the reading; the exit code never was.

THE ARCHIVE WAS NOT DAMAGED, WHICH IS THE INSTRUCTION THAT MATTERED MOST. `/home/decodeux/Repos/remedy-history/zips` went from 23 to 25 entries, and the superseded round 9 package `remedy-review-20260829-025133-READY_FOR_REVIEW.zip` is still present at its original 18146705 bytes. Nothing was deleted, nothing overwritten, and both the superseded and the live filenames are named in the handback so no later reader has to guess which package covers the closed head.
<<<END GATEF257R11

<<<SLICE PLANFINALF257
# Plan — F257 Self-use track (CLOSED)

Branch: feature/f257-self-use-track, cut from `main` at the merge commit of pull
request #220. F257 is CLOSED: `docs/roadmap/STATUS.md` carries its `[x]` line and
the pull request is open and UNMERGED.

## Goal
Remedy is used on Remedy on a schedule that cannot be skipped: a curated queue of
small maintenance jobs, exactly one consumed per feature close, run through
`do job-plan` and `do job-run` against this repository and taken to the normal
approval gate. DONE.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the queue, the loader, the job-path seam | done | rounds 2-5, 36 tests |
| the integration gate | done | round 6, 18186 passed 0 failed |
| the feature file's Built State | done | round 7, precondition 4 |
| plan SU-001 and stop at the approval gate | done | round 8, precondition 6 |
| three tests survive their own feature's close | done | round 10, R-0737 |
| the evidence bundle and the review zip | done | round 11, READY_FOR_REVIEW |
| the closure commit | done | this round, Rule A4's last commit |
| the pull request | done | opened and NOT merged |

## Next Steps
1. Nothing further on this branch. The next feature's Open PR Gate merges this
   pull request, or the operator merges it manually at any time.
2. Rule A5 selects F033 — Hunk-level diff approval — as the next feature, in a
   fresh session.

## Risks
- THE SELF-USE QUEUE IS NOW EXHAUSTED. SU-001 is consumed by F257 and no pending
  item remains, so the next feature's close records
  `self-use NONE (queue exhausted)` until an operator curates more items into
  `scripts/self_use_queue.json`. That is the track asking for curation, and
  closure precondition 6 explicitly does not treat it as a blocker.
- R-0734 and R-0736 stay registered and unrepaired, both outside F257's surface.
  They are the documented Medium risks behind the PASS_WITH_RISKS verdict.
<<<END PLANFINALF257

### The five authored pairs for C2

Each FROM occurs EXACTLY ONCE in its target at `f459c431`. Verify before replacing
(constraint 8).

PAIR 1 of 5 — `docs/roadmap/STATUS.md`. The `[x]` flip. The TO line is the
protocol's step 4 template filled from values the reviewer measured itself: the
package hash is the reviewer's own sha256 over the archived file, and the accepted
HEAD is the commit the manifest records.

<<<SLICE STATUSFROM
- [~] F257 — Self-use track (one curated maintenance job per feature close, run through job-plan/job-run against Remedy itself)
<<<END STATUSFROM

<<<SLICE STATUSTO
- [x] F257 — Self-use track (T001–T002 complete; accepted 2026-08-29 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f257-closure · package remedy-review-20260829-031830-READY_FOR_REVIEW.zip · SHA-256 0a4b5fc189ac7ed6b968f878b1186a23e2d5ac3425b6d1f46faad271b157acdd · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD fb10b3754978d9fc4112b2818eb9e7e31f4fdc78)
<<<END STATUSTO

PAIR 2 of 5 — `README.md`. The accepted count AND its `Next:` clause, which
`test_the_readme_accepted_count_equals_the_status_count` pins to the ledger.

<<<SLICE COUNTFROM
61 of 257 registered items accepted. Next: F257 (Self-use track).
<<<END COUNTFROM

<<<SLICE COUNTTO
62 of 257 registered items accepted. Next: F033 (Hunk-level diff approval).
<<<END COUNTTO

PAIR 3 of 5 — `README.md`. The tier-5 Done cell, which
`test_the_readme_tier_table_done_column_matches_the_ledger` pins to the accepted
features resolving through their `T5_F???.md` feature files. This is the half
nobody re-reads.

<<<SLICE TIERFROM
| 5 | Operator Cockpit | 9 | 31 |
<<<END TIERFROM

<<<SLICE TIERTO
| 5 | Operator Cockpit | 10 | 31 |
<<<END TIERTO

PAIR 4 of 5 — `README.md`. The capability paragraph, inserted directly after the
F256 paragraph's closing line and before the blank line, which is where the F256
closure put its own.

<<<SLICE CAPFROM
sidebar's visual treatment ruled by a named design authority and applied).

Full per-feature state: [`docs/roadmap/STATUS.md`](docs/roadmap/STATUS.md)
<<<END CAPFROM

<<<SLICE CAPTO
sidebar's visual treatment ruled by a named design authority and applied).
F257 self-use track (Remedy now runs a curated maintenance job on its own
repository at every feature close, on a schedule that cannot be skipped: a
shipped queue of operator-curated jobs whose read side owns no writer at all, a
seam that renders one item verbatim onto the job path Remedy already has and
plans it, and a closure precondition that consumes exactly one item per close —
no job may mark its own item consumed, because a run that can check itself off is
not a gate).

Full per-feature state: [`docs/roadmap/STATUS.md`](docs/roadmap/STATUS.md)
<<<END CAPTO

PAIR 5 of 5 — `scripts/self_use_queue.json`. The consumption edit precondition 6
requires, and the ONLY edit this feature ever makes to the queue.

<<<SLICE QUEUEFROM
      "consumed_by": ""
<<<END QUEUEFROM

<<<SLICE QUEUETO
      "consumed_by": "F257"
<<<END QUEUETO

`GATEF257R11` is a SINGLE APPEND to `.agent/live_review.md` at C1 under constraint
6. `PLANFINALF257` is a WHOLE-FILE replacement of `.agent/plan.md` at C2. The five
pairs are all applied in C2.

### The pull request

After C2 is committed and pushed, open the PR with `gh pr create`, base `main`,
head `feature/f257-self-use-track`, and do NOT merge it. The description carries:
what changed and why; the key decisions (DECISION F257 D2 on where consumption
happens; that the shipped modules plan and never run, promote or consume); how to
review (the package filename and SHA-256, and the four scoped suites); a
changed-files summary; the latest verdict `PASS_WITH_RISKS`; the open-findings
count 256; and the runtime actuals — 12 rounds across 3 sessions, wall clock
`not-measured`, tokens and cost `not-measured`. Report the PR number and URL.
Write no leading-slash token, absolute path or secret-like string into the PR
TITLE; the commit-subject rule exists because the metadata scanner reads them.

### Done when

G1 HYGIENE. Read `.agent/STOP` from disk with `os.path.exists` before C0a and
again before C2; report both answers. If it exists at either reading, finish the
commit in hand, write the handback and stop. Report constraint 0's three readings
and `git status --porcelain | wc -l` after each of C0a, C0b, C1 and C2.

G2 TRANSPORT. One digest comparison. Report sha256 and the byte length of the
committed blob `git show <C0a>:.agent/authored/f257-r12.md` and of the reviewer's
own original at `.remedy-wt/f257-r12-block.md`, and whether they are EQUAL. That
original was written before this worker existed, so the reading covers more than
self-consistency; it covers no emission, because this workflow has none — say
both in the handback. Then report that
`git rev-parse <C0b>:.agent/authored/f257-r12.md` and
`git rev-parse <C0b>:.agent/last_block.md` print ONE blob id.

G3 THE RECORD APPEND AT C1. Reconstruct the C1 blob of `.agent/live_review.md`
from the `f459c431` blob plus GATEF257R11 under constraint 6, and report `True` or
`False` with all three lengths. NEGATIVE CONTROL: flip one byte at an offset your
script CONFIRMS lies inside the appended text, recompute, and report the equality
is now `False`. Report that the pre-round blob is a byte PREFIX and that the C1
blob ends in exactly ONE newline.

G4 THE LEDGER AT C1, counted under constraint 7. Report over
`.agent/live_review.md` at `f459c431` and again at C1: the count of lines matching
`^- R-\d+ — ` and whether all are DISTINCT; the count of `^Done: R-\d+ — ` lines
AND the count of DISTINCT ids among them; the count of `^Landed: R-`; the count of
`^Gate: F\d+ R\d+ — `; and the OPEN SET as
`len(set(registered) - set(resolved))`. Expected: registered UNMOVED at 298 all
distinct, the `Done:` numbers and `Landed:` UNMOVED, `Gate:` 116 → 117, the open
set UNMOVED at 256. Report the count of `^Gate: F257 R11 — ` at C1, which must be
1.

G5 THE CLOSURE EDITS AT C2, one reading per pair. For EACH of the five pairs
report the FROM count in the `f459c431` blob, which must be 1, and in the C2 blob,
which must be 0 — EXCEPT pair 5, whose FROM string `      "consumed_by": ""` may
legitimately reappear if the queue ever grows, so for pair 5 report the count of
pending items instead, which must be 0. Report the TO count in the C2 blob, which
must be 1 for every pair. Then report, per FILE, that the C2 blob equals the
`f459c431` blob with its pairs applied and nothing else changed — `True` or
`False` with both byte lengths, for `docs/roadmap/STATUS.md`, `README.md` and
`scripts/self_use_queue.json`. Report that the STATUS line in the C2 blob is
BYTE-IDENTICAL to the `STATUSTO` slice, which is the closure protocol's
apply-verbatim proof. Report that `.agent/plan.md` at C2 equals `PLANFINALF257`
including the trailing newline, with `wc -l` under 50.

G6 THE LEDGER PINS AT C2, every numeral DERIVED from the flipped ledger and none
of them retyped from this block. Report, all read from the C2 blobs: the count of
lines matching `^- \[x\] F\d{3} — ` in `docs/roadmap/STATUS.md`; the two numbers
the README's `^(\d+) of (\d+) registered items accepted\.` line carries, and
whether the first EQUALS that count; the count of lines matching `^- \[~\] F\d{3} —`,
which must be 0; the first line matching `^- \[ \] (F\d{3}) — `, whose feature id
must be the one the README's `Next:` clause names; and the tier-5 row's Done cell
beside the number of `[x]` features whose id resolves to an existing
`docs/roadmap/features/T5_F???.md`, which must be EQUAL. Finally, load the C2
queue through the SHIPPED loader and report `next_self_use_item()`, which must be
`None`, and `pending_self_use_items()`, which must be empty — the consumption
proved through the code rather than through the JSON text.

G7 THE SUITES AT C2, in the PRIMARY checkout at the closed state, one pytest
process at a time, each with its REAL exit code and its own passed/failed line.
CONFIRM FIRST that every path resolves on disk and report the empty list:
`tests/docs/test_docs_consistency.py` — the suite that pins README to STATUS and
the one this round's edits could plausibly break; `tests/orchestration/test_self_use_job.py`;
`tests/orchestration/test_self_use_queue.py`; and the canary
`tests/cli/test_golden_path.py`. Every one must be exit 0. THIS IS THE READING
R-0737 EXISTS FOR: the two self-use suites are being run for the first time with
the queue genuinely exhausted on disk rather than in a worktree. If any is red,
STOP, do NOT open the pull request, and write the handback with the full
untruncated failure list.

G8 STRUCTURE AND THE PR, over `f459c431..<C2>`. Report the range's paths and both
residues against the change set — each must be empty; nothing is excluded this
round, because C2 writes the handback itself. Report each commit's insertions from
`git diff --numstat`, each under 500, and that each of C0a, C0b, C1 and C2 is
single-parent. Report that C2 is the LAST commit on the branch and that its path
set is exactly the five files named above — Rule A4. Report the number of lines
beginning `<<<SLICE ` and `<<<END ` in `docs/roadmap/STATUS.md`, `README.md`,
`scripts/self_use_queue.json` and `.agent/plan.md` at C2 — each expected 0 —
beside the same counts over `.agent/authored/f257-r12.md` as the non-zero control.
Report `git ls-files .remedy-wt | wc -l`, expected 0. Report the push outcome, the
PR number and URL, and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
AFTER creation, which must show exactly this one PR, not a draft, head
`feature/f257-self-use-track`, base `main`. Report that nothing was merged.

### Handback

Rewrite `.agent/handoff.md` INSIDE C2 per docs/agents/handback_template.md — it is
part of the closure commit's path set, not a commit of its own, because Rule A4
lets nothing follow C2. It carries: `SESSION 3 of feature F257 · round 12`; the
roster of this session's rounds, this round included; the range `f459c431..HEAD`;
a per-commit changed-files table whose `+/-` cells are taken from
`git diff --numstat`; ONE LINE PER GATE G1 through G8 with its real result; the
deviations, including every guard re-expression constraint 5 required; the
item-status table with every C-item and every gate appearing exactly once; the
open-findings count, which must be 256; and the closure values — `Evidence job
f257-closure`, the package filename, its SHA-256, the archived path and the
accepted HEAD.

It also states, in as many words, that the feature is CLOSED, that the pull
request is OPEN and UNMERGED, and that the self-use queue is now EXHAUSTED so the
next feature's close records `self-use NONE (queue exhausted)` until an operator
curates more items.

Do not write a `Done:` or `Gate:` paragraph of your own anywhere — GATEF257R11 is
reviewer-authored text you apply verbatim, and any OTHER such paragraph is a
finding however hedged. Do not merge the pull request. Do not add any commit after
C2.
