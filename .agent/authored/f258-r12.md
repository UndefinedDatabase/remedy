### STEP CLOSURE — F258 Self-use track v2, round 12 (THE CLOSURE COMMIT AND THE PULL REQUEST)

Goal: book the round 11 verdict, then execute the remainder of
`docs/roadmap/STATUS_closure_protocol.md`'s Algorithm: the STATUS `[x]` flip,
the README capability sync (same commit, R-0154), the `scripts/self_use_queue.json`
`consumed_by` edit precondition 6 requires, the final `.agent/` state, and the
pull request. This is the LAST round of this branch.

Base: `530bd3d8`, the tip of `feature/f258-self-use-v2` and the handback this
round starts from.

Bundle, in commit order:

- C0a save this block verbatim to `.agent/authored/f258-r12.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 book the F258 R11 verdict into `.agent/live_review.md`
- C2 THE CLOSURE COMMIT: `docs/roadmap/STATUS.md`, `README.md`,
  `scripts/self_use_queue.json`, `.agent/plan.md` and `.agent/handoff.md` —
  nothing else
- then `gh pr create`

Change set — these paths and nothing else:

- `.agent/authored/f258-r12.md`
- `.agent/last_block.md`
- `.agent/live_review.md`
- `docs/roadmap/STATUS.md`
- `README.md`
- `scripts/self_use_queue.json`
- `.agent/plan.md`
- `.agent/handoff.md`

No file under `packages/`, `apps/`, `tests/`, `scripts/make_review_zip.sh` or
`docs/roadmap/features/T5_F258.md` is edited this round — the feature file's
Built State is already current from round 10.

### Constraints

0. BEFORE ANYTHING: report
   `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
   — expected `[]`; if it is not `[]` now, STOP and hand back without
   committing. Report `git rev-parse HEAD`, which must equal `530bd3d8`'s
   full sha, and `git branch --show-current`, which must be
   `feature/f258-self-use-v2`. Never force-push and never rewrite history.
1. Apply every authored slice BYTE FOR BYTE — no reflow, rewording,
   retitling, correction or shortening. If a slice looks wrong, apply it as
   written and say so in the handback's deviations.
2. The delimiter lines `<<<SLICE …` and `<<<END …` are transport only and
   never reach a target file.
3. Extract every slice from the COMMITTED blob with
   `git show <C0a>:.agent/authored/f258-r12.md`, never from this prompt's
   text.
4. AGENTS.md binds in full: the self-review loop before every commit, a
   clean tree, and the push. EVERY edit attempt — the STATUS pair, the
   three README edits, the queue.json field mutation — appears in the
   handback with its verified before/after byte counts.
5. Shell forms rejected by this session's guard are RE-EXPRESSED, never
   skipped and never weakened (loops, `$( )`, `${arr[0]}`, `cp`, brace
   literals containing quotes, every form of environment-variable
   assignment). Route such work through a scratch script under the
   gitignored `.remedy-wt/`. Capture real exit codes with
   `bash -c '<cmd>; echo "REAL_EXIT=$?"'` or from `subprocess`.
6. THE APPEND CONVENTION for C1: `.agent/live_review.md` gets ONE append,
   GATEF258R11 below, as `base + b"\n" + GATEF258R11`, base being the
   file's own current bytes immediately before C1.
7. THE OPEN SET IS COUNTED BY DISTINCT ID as
   `len(set(registered ids) - set(resolved ids))`. It reads 263 at
   `530bd3d8`. THIS ROUND REGISTERS NO ID AND RESOLVES NONE, so it must
   still read 263 at C1 and at C2.
8. THE QUEUE.JSON EDIT IS A SCRIPT, NEVER A HAND-WRITTEN FROM/TO PAIR: load
   the file with `json.loads`, find the item whose `"id"` is `"SU-002"`,
   assert its `"consumed_by"` is currently `""`, set it to `"F258"`, and
   re-serialize the WHOLE document with
   `json.dumps(data, indent=2, ensure_ascii=False) + "\n"` —
   `ensure_ascii=False` IS LOAD-BEARING: the default `ensure_ascii=True`
   escapes every non-ASCII byte (the file's own em dashes and curly quotes)
   into `\uXXXX` sequences, which would silently rewrite hundreds of bytes
   the module's own docstring calls "the curated bytes" and forbids
   reformatting. Diff the old and new bytes with `difflib` and confirm the
   unified diff touches EXACTLY ONE LINE (`"consumed_by": ""` →
   `"consumed_by": "F258"`) before writing the file. Expected: 10834 bytes
   before, 10838 after, delta exactly +4.
9. THE STATUS.MD AND README.MD EDITS ARE FROM/TO REWRITES (FROM does not
   survive as a prefix of TO in any of the four pairs below — verified by
   the reviewer before authoring this block). Apply each FROM exactly once;
   confirm each FROM is absent and each TO present exactly once after.

### The authored slices

<<<SLICE GATEF258R11
Gate: F258 R11 — THE PACKAGE ROUND, CLOSURE-PROTOCOL ALGORITHM STEPS 1 AND 2. THE ROUND PASSED AND THE PACKAGE BUILT READY_FOR_REVIEW. The reviewer re-ran every gate independently against the real diff `3d2ab8b5..530bd3d8`. G1/G2 TRANSPORT: the block, `.agent/authored/f258-r11.md` and `.agent/last_block.md` all sha256 `54b5c9629cf9179cb6ed9f15ba369dea294a08336f7d331b03f070e5de1ea1b6`, 21196 bytes — equal to the reviewer's own scratch original. G3 THE PLAN AT C1: `.agent/plan.md` byte-equal to the authored PLANF258R11 slice extracted from the committed block, 1718 bytes, 38 lines, `## Goal`/`## Next Steps` present. G4 THE RECORD APPEND AT C2: base 1798961 bytes; `base + b"\n" + GATEF258R10 (2630 bytes) == committed (1801592 bytes)` True; the last `\n\n`-unit equals GATEF258R10 exactly; a negative control (byte flip, disposable worktree, removed after) independently reproduced by the reviewer, correctly rejected, the true original correctly accepted. G5 THE LEDGER: before C2, 318 distinct `R-` ids / 55 distinct `Done:` ids / open set 263 / `Gate: F258 R` lines ending at R9; after, same R-ids/Done-ids/open-set, `Gate: F258 R` lines ADDED exactly `F258 R10` — the round registered nothing and resolved nothing, as required. G6 THE EVIDENCE BUNDLE, independently spot-checked by the reviewer against the real files on disk at `.remedy-wt/f258_closure_evidence/remedy-job-evidence-f258-closure/`: `verification_tests.json` carries exactly the seven ordered runs — `vr-0001`..`vr-0007` at 23/18/20/7/3/295/42 passed, 0 failed/skipped/deselected each, `len(node_ids) == selected` for every one — matching the reviewer's own fresh run of all five self-use suites together (71 passed) plus the independently-confirmed `tests/docs/` (295) and canary (42) baselines. `final_verifier_report.json` reads `"verdict": "PASS_WITH_RISKS"`. All eight closed-schema gate files are present in the bundle directory. G7 THE REVIEW ZIP, read under constraint 8 (PACKAGE_STATUS is the reading, never the exit code): the READY package `remedy-review-20260830-084541-READY_FOR_REVIEW.zip` was independently confirmed by the reviewer, via a fresh read-only check, to exist at the archived path `/home/decodeux/Repos/remedy-history/zips/` with size 19,357,817 bytes and sha256 `4b4153ad33f01e4d7014e853663f76ac1f36f61ba06687ed0b3c9c5411f12c50` — matching the worker's own reported digest exactly, byte for byte. The manifest's `committed_review_subject.head_commit` equals C2's full sha `49fcc2c645601936d8c426b1eb09523b9b3c7f6f`, which is the ACCEPTED HEAD. THE RED CONTROL was independently confirmed present: `remedy-review-20260830-084654-BLOCKED_EVIDENCE.zip` exists at the same archived directory, proving the pipeline reports `PACKAGE_STATUS=BLOCKED_EVIDENCE` at REAL exit 0 for a deliberately poisoned copy — the status distinguishes the two builds, the exit code does not. ONE DISCLOSED DEVIATION IS ACCEPTED, NON-BLOCKING: the worker rebuilt the READY zip once to capture a rigorous exit-code reading and removed the resulting duplicate by its exact filename via `os.remove`, never a glob — the canonical package's own filename, size and sha256 are unaffected and independently reconfirmed above. G8 THE TREE: `git status --porcelain` empty; `git worktree list` shows only the primary checkout; `git branch --list 'tmp/*'` empty; `git ls-files | grep -c remedy-job-evidence` and `git ls-files .remedy-wt | wc -l` both 0 — neither the evidence directory nor the zip ever entered the tree; per-commit insertions 342/317/17/2 from `git show --numstat`, all under 500; `python3 -m apps.cli.main integrity check --json` independently re-run by the reviewer at this HEAD: `"passed": true`, `"fail_count": 0`, `"high_blockers_open"` `"pass"`. THE ROUND PASSES: the branch is pushed and matches `origin` exactly at `530bd3d8`. Closure precondition 3 is re-confirmed MET. Algorithm steps 1 and 2 are complete; the next and final round is the closure commit (STATUS line, README sync, the `consumed_by` edit, final `.agent/` state) and the pull request.
<<<END GATEF258R11

<<<SLICE PLANF258R12CLOSED
# Plan — F258 Self-use track v2 (CLOSED)

Branch: feature/f258-self-use-v2, cut from `main` at the merge commit of pull
request 225. F258 is CLOSED: `docs/roadmap/STATUS.md` carries its `[x]` line
and the pull request is open and UNMERGED.

## Goal
"Remedy is used on Remedy" keeps running with zero operator input: a generator
replenishes the self-use queue with exactly one dated, provenanced item
whenever it is empty at close, the consumed item is actually RUN through the
real job path under a small budget and stopped at the normal approval gate
rather than only planned, and any defect the run surfaces flows back into the
standard finding ledger. DONE.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001/T002/T003, integration gate | done | rounds 2-7 |
| all six closure preconditions | done | rounds 8-10 |
| the evidence bundle and the review zip | done | round 11, READY_FOR_REVIEW |
| the closure commit | done | this round, Rule A4's last commit |
| the pull request | done | opened and NOT merged |

## Next Steps
1. Nothing further on this branch. The next feature's Open PR Gate merges
   this pull request, or the operator merges it manually at any time.
2. Rule A5 selects the next feature in a fresh session.

## Risks
- THE SELF-USE QUEUE HOLDS TWO PENDING ITEMS after this close (SU-003,
  SU-004) — not exhausted, unlike F257's close. No generator action is
  needed at the next feature's close.
- R-0570 (Low) and R-0736 (Medium) stay registered and unrepaired, both
  outside F258's own surface. R-0757 (Medium) IS F258's own defect (the
  self-use runner's silent fake-provider default) and is deliberately not
  repaired on this branch — a follow-up round, not a closure blocker.
  Together these are the documented risks behind the PASS_WITH_RISKS
  verdict.
<<<END PLANF258R12CLOSED

`GATEF258R11` is a SINGLE APPEND to `.agent/live_review.md` under
constraint 6, applied at C1. `PLANF258R12CLOSED` is a WHOLE-FILE
replacement of `.agent/plan.md`, applied at C2.

### The closure commit's four content edits

**Edit 1 — `docs/roadmap/STATUS.md`, a REWRITE.**
FROM (occurs exactly 1x):
`- [~] F258 — Self-use track v2 (self-replenishing queue & executed items)`
TO (occurs exactly 1x after; FROM 0x after):
`- [x] F258 — Self-use track v2 (T001–T003 complete; accepted 2026-08-30 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f258-closure · package remedy-review-20260830-084541-READY_FOR_REVIEW.zip · SHA-256 4b4153ad33f01e4d7014e853663f76ac1f36f61ba06687ed0b3c9c5411f12c50 · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD 49fcc2c645601936d8c426b1eb09523b9b3c7f6f)`
Touch no other line. Expected: 32950 bytes before, 33277 after, delta +327.

**Edit 2 — `README.md`, the accepted-count line, a REWRITE.**
FROM (occurs exactly 1x): `64 of 258 registered items accepted.`
TO (occurs exactly 1x after; FROM 0x after): `65 of 258 registered items accepted.`

**Edit 3 — `README.md`, the Tier 5 table row, a REWRITE.**
FROM (occurs exactly 1x): `| 5 | Operator Cockpit | 12 | 32 |`
TO (occurs exactly 1x after; FROM 0x after): `| 5 | Operator Cockpit | 13 | 32 |`

**Edit 4 — `README.md`, the Tier 5 capability list, a REWRITE (FROM does
NOT survive as a prefix of TO — the new paragraph is inserted between the
two halves of FROM).**
FROM (occurs exactly 1x), exact bytes including the two newlines:
```
re-arms it).

Full per-feature state:
```
TO (occurs exactly 1x after; FROM 0x after), exact bytes:
```
re-arms it).

F258 self-use track v2 (the queue now replenishes itself: a generator appends
exactly one dated, provenanced item whenever the track runs dry, sourced first
from the oldest self-contained open finding in the reviewer's own ledger; the
consumed item is RUN through the real job path to the normal approval gate,
not merely planned; and any defect the run surfaces flows back into that same
ledger as a normal finding).

Full per-feature state:
```
README.md expected: 9206 bytes before, 9625 after (all three edits
combined), delta +419.

**Edit 5 — `scripts/self_use_queue.json`, per constraint 8 (a script, never
a hand-written pair).** Expected: 10834 bytes before, 10838 after, delta
+4, unified diff touching exactly one line.

All five edits, plus the `.agent/plan.md` rewrite and the `.agent/handoff.md`
rewrite, land in ONE commit, C2 — the closure commit, per
`STATUS_closure_protocol.md` Algorithm item 5's ordering rule (README syncs
in the SAME commit as the STATUS flip; nothing else may separate them).

### Done when

G1 HYGIENE. Read `.agent/STOP` from disk before C0a and again before C2;
report both answers. Report constraint 0's three readings.
`git status --porcelain | wc -l` after each of C0a, C0b and C1 must be 0.

G2 TRANSPORT. Report sha256 and byte length of the committed blob
`git show <C0a>:.agent/authored/f258-r12.md` and of the reviewer's own
original at `.remedy-wt/f258-r12/block.md`, and whether they are EQUAL.
Report that `git rev-parse <C0b>:.agent/authored/f258-r12.md` and
`git rev-parse <C0b>:.agent/last_block.md` print ONE blob id.

G3 THE RECORD APPEND AT C1. Reconstruct the C1 blob of
`.agent/live_review.md` from the `530bd3d8` blob plus GATEF258R11 under
constraint 6; report `True`/`False` with all three lengths (expected
1805654 committed). NEGATIVE CONTROL: flip one byte at a confirmed offset
inside the appended text, in a disposable worktree removed after; report
the equality is now `False`, then that the true original is `True`.

G4 THE LEDGER AT C1, under constraint 7. Report over
`.agent/live_review.md` at `530bd3d8` and again at C1: registered/resolved
distinct counts, the open set, and `Gate: F\d+ R\d+ — ` count. Expected:
registered UNMOVED at 318, resolved UNMOVED at 55, open set UNMOVED at
263, `Gate:` count up by exactly one. Report the count of
`^Gate: F258 R11 — ` at C1, which must be 1.

G5 THE FIVE C2 EDITS. For EACH of the five edits above, report: the exact
before/after byte length of its target file, the before/after occurrence
count of its FROM string (or, for the queue.json script, the unified diff
line count and the exact one changed line), and the after occurrence
count of its TO string. All five must match the expected numbers stated
above exactly.

G6 THE PLAN AND HANDOFF AT C2. `.agent/plan.md` byte-equal to
PLANF258R12CLOSED including the trailing newline. `.agent/handoff.md`
exists and is non-empty (its own content is not gated here — see
Handback below for what it must carry).

G7 THE REMAINING PRECONDITIONS, over `530bd3d8..<C2>` for the range. The
change set lists `.agent/handoff.md`, written by C2 itself, so this range
IS the change set (no residue to compute against a later handback commit
— C2 is both the content commit and the last commit before the round
report). Report each commit's insertions from `git diff --numstat`, each
under 500 except a declared exception. Report `git ls-files .remedy-wt |
wc -l`, expected 0, and `git ls-files | grep -c remedy-job-evidence`,
expected 0. Report `python3 -m apps.cli.main integrity check --json`
`result["passed"]` and `result["fail_count"]` at C2 — expected `true`/`0`.
Report `git diff --numstat` for `docs/roadmap/features/T5_F258.md` over
the range, expected ABSENT (its Built State is already current from round
10).

G8 THE STATUS/README CROSS-CHECK. Report
`python3 -m pytest tests/docs/ -q` at C2, REAL exit 0, expected 295
passed unchanged — the pinned README↔STATUS cross-checks
(`test_the_readme_accepted_count_equals_the_status_count`,
`test_the_readme_tier_table_done_column_matches_the_ledger`) are IN this
suite and must be green with the new numbers, not merely asserted by this
block. Report the canary `python3 -m pytest tests/cli/test_golden_path.py
-q`, REAL exit 0, expected 42 passed.

### The pull request

After C2 is committed and pushed, open the PR with `gh pr create`:

- Title: `F258 — Self-use track v2: self-replenishing queue, real
  execution, findings flow back`
- Base: `main`. Head: `feature/f258-self-use-v2`.
- Body: what/why (T001-T003, the acceptance criteria met), key decisions
  (DECISION F258 D1 the schema v2 break), how to review (the review zip
  at the archived path), the changed-files table for the WHOLE branch
  (`git diff --stat main...HEAD`), the latest verdict (PASS_WITH_RISKS),
  open-findings count (263), and runtime actuals where measured
  (session/round counts from the handoff — `not-measured` beats a guess
  for anything not actually timed).
- Do NOT merge it. Report the PR URL and number.

### Handback

Rewrite `.agent/handoff.md` in C2 (the same commit that writes it) per
docs/agents/handback_template.md. It carries: `SESSION 3 of feature F258 ·
round 12 (FINAL)`; the roster of every round this session (8 through 12);
the range `530bd3d8..HEAD`; a changed-files table for C2 whose `+/-` cells
are taken from `git diff --numstat`; ONE LINE PER GATE G1 through G8 with
its real result; any deviations; the open-findings count, 263; the PR
number and URL; and the next expected action — nothing further on this
branch, the next feature's Open PR Gate merges this PR.

Do not write a `Done:` or `Gate:` paragraph of your own anywhere —
GATEF258R11 is reviewer-authored text you apply verbatim, and any OTHER
such paragraph is a finding however hedged. Do not merge the PR. Do not
touch `main`. Do not force-push.

After C2: push with `git push origin feature/f258-self-use-v2` and report
the outcome, THEN create the PR as above.
