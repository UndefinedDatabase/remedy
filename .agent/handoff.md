# Handoff — F112 Prompt budget per task class, round 30 (HALTED at C4 — docs gate RED after the closure commit; PR NOT created)

## Session

Session continuing F112 (same numbering ambiguity round 20's handoff
introduced and rounds 21-29 carried forward unresolved — "6 (or 7)")
· round 30 · rounds so far 30.

This round is NOT a fresh loop-session bootstrap — it is a direct
continuation of round 29's own session, so the session number is
unchanged from round 29.

## Range

Review of `a5df6f2b..HEAD` (base is F112 R29's handback commit).

## Commits

### be0c9e5b F112 R30 C0a: save the round 30 step block verbatim to .agent/authored/f112-r30.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f112-r30.md` | +193/-0 | transport proof — verbatim copy of the supplied step block |

### 954a56cf F112 R30 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +193/-187 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption) |

### 38f52919 F112 R30 C1: append RECORD29 to live_review.md (books R29 PASS-with-declared-deviation, precondition 6 already discharged at R21)
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | append RECORD29 (books round 29's PASS-with-declared-deviation verdict; no new finding registered or resolved) |

### b025d3c2 F112 R30 C2: apply PLAN30 to plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +17/-24 | whole-file replace with PLAN30 |

### 255a4e5f F112 R30 C3: closure commit - STATUS [x], README capability sync, self_use_queue SU-007 consumed
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/STATUS.md` | +1/-1 | flip F112's line from `[~]` to `[x]`, with the accepted/evidence/package metadata the block's item 4a specified byte-exact |
| `README.md` | +13/-0 | insert READMEF112's capability-sync paragraph, byte-exact, between the F110 paragraph and "Accepted in Tier 5 so far:" |
| `scripts/self_use_queue.json` | +1/-1 | SU-007's `consumed_by` field `""` → `"F112"`; every other byte in the file unchanged (confirmed by `git diff`) |

### (this handback commit)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this handback (write-once per PH v3) |

## External actions

None. No push, no `gh pr create`, no merge, no `--approve`, nothing
force-pushed, `main` never touched. Per the block's own constraint
("If ANY gate at C4 is not green, STOP before C5 — no PR on a red
gate") and self-drive protocol G8, C5 (which the block itself bundles
as "Push, then `gh pr create`") was not started at all: the round
halted the instant C4's docs-gate command returned a nonzero exit
code, before any push was attempted.

## Verification

Real, trimmed transcripts for every gate this round's block ordered.

**C0a/C0b — transport:**
```
$ sha256sum .agent/authored/f112-r30.md
0a02207955e2458e06b83d3e3361ba5d69a869af6186d0673da34317b9d6180c  15327 bytes, 193 lines
-> matches the prompt's stated hash/size/line-count exactly.

$ git rev-parse HEAD:.agent/authored/f112-r30.md HEAD:.agent/last_block.md
3d23ac8094b202da5e2fb4ed179c0e4b3086614c
3d23ac8094b202da5e2fb4ed179c0e4b3086614c
-> identical blob ids, confirmed after C0b's own commit.
```

**C1 — the RECORD29 append:** RECORD29 extracted from the committed
authored file (between its `--- BEGIN RECORD29 sha256=... ---` /
`--- END RECORD29 ---` markers, trailing newline before the END marker
stripped) measured exactly `4211` bytes with sha256
`ad73d8470015e65618bdb6577d297fc2f2e9251ce37adee39f4f7d1e3bac2b0d`,
matching the marker's own stamp exactly. Pre-append `.agent/live_review.md`
measured `2338544` bytes; append computed as
`content_bytes + b"\n" + RECORD29_bytes`; post-append measured `2342756`
bytes, exactly `2338544 + 1 + 4211`. The pre-append content is a
byte-exact prefix (verified in Python: `new_live[:len(live)] == live`).
File still ends WITHOUT a trailing newline.

Registered/`Done:`/open counts, counted mechanically (registered =
unique ids matching `^- R-\d{4} — `; resolved = unique ids appearing on
a line matching `^Done: R-\d{4}`, since `R-0721` and `R-0725` each
appear on two `Done:` lines — 76 total `Done:` lines, 74 unique
resolved ids):

| | registered | Done: lines | unique resolved | open |
|---|---|---|---|---|
| before C1 | 354 | 76 | 74 | 280 |
| after C1  | 354 | 76 | 74 | 280 |

UNMOVED on both sides, exactly matching the block's own expectation
(354/74/280), consistent with round 29's own reading of the same
convention.

**C2 — the PLAN30 replacement:** PLAN30 extracted from the committed
authored file measured exactly `1925` bytes with sha256
`2f33269d4192efe07ca13fb2bb6757804649229b4a7144ee3982e50318721f43`,
matching the marker's stamp exactly. `.agent/plan.md` after C2
reproduced byte-identical (same 1925 bytes), no trailing newline,
`wc -l` = 41 (under 50), `## Goal`/`## Next Steps` each occurring
exactly once.

**C3 — the closure commit:**
- Re-verified the zip's SHA-256 myself before committing:
  `sha256sum /home/decodeux/Repos/remedy-history/zips/remedy-review-20260904-123332-READY_FOR_REVIEW.zip`
  → `b0085f28a2c0c50654ed33be647ed986addc07c1c462324b1ee3fc1c8bb05927`,
  matching the block's stated value exactly.
- `docs/roadmap/STATUS.md`: extracted the exact literal TO-text from the
  block's own line 22 (which already carries the correct U+2014 em
  dashes and the U+2013 en dash between `T001` and `T003`, copied
  programmatically rather than retyped) and applied it. Post-edit:
  exactly one line matches `^\- \[x\] F112 — ` (was 0), zero lines match
  `^\- \[~\] F112 — ` (was 1).
- `README.md`: extracted READMEF112 (776 bytes, sha256
  `04b5c0b34aa40cd453a58ae70fa96db1620331582ed1ea467a6d79e3dfbb0b11`,
  matching the marker's stamp) and inserted it verbatim between the
  F110 paragraph's closing text and "Accepted in Tier 5 so far:".
  Confirmed by byte-search: the exact 776-byte span occurs exactly once
  in the post-edit file. Surrounding context reproduced under
  "Authored-text proofs" below.
- `scripts/self_use_queue.json`: `git diff` (full, reproduced above)
  shows exactly one changed line — SU-007's `consumed_by` field,
  `""` → `"F112"` — no reformatting, no key reordering, no whitespace
  change anywhere else in the file. `python3 -c "import json; ..."`
  confirmed the file still parses as valid JSON.
- `git diff --stat` immediately before the C3 commit showed exactly the
  three files the block's item 4 names (`README.md`,
  `docs/roadmap/STATUS.md`, `scripts/self_use_queue.json`) — nothing
  else.

**C4 — GATES (run for real):**

```
$ python3 -m pytest tests/docs/ -q
...
FAILED tests/docs/test_docs_consistency.py::TestPrimaryDocsAreHonest::test_the_readme_accepted_count_equals_the_status_count
FAILED tests/docs/test_docs_consistency.py::TestPrimaryDocsAreHonest::test_the_readme_tier_table_done_column_matches_the_ledger
2 failed, 293 passed in 0.53s
```
RED. Root cause, confirmed independently (compared README.md/STATUS.md
at commit `b025d3c2`, i.e. immediately BEFORE C3, against the current
tree): flipping F112's STATUS line to `[x]` at C3 moved the ledger's
real accepted count from 69 to 70 (`grep -c '^- \[x\] F' docs/roadmap/STATUS.md`
now reads `70`) and Tier 3's derived Done-count from 4 to 5, but
`README.md`'s prose line ("69 of 266 registered items accepted.") and
its Tier-status table's Tier 3 `Done` cell (still `4`) were NOT part of
this round's ordered edit — the block's item 4b instructed inserting
ONLY the READMEF112 paragraph and named nothing else in README.md to
touch. This is a genuine gap in the round's own authored block, not a
worker error: two long-standing pinning tests
(`test_the_readme_accepted_count_equals_the_status_count` /
R-0156, and `test_the_readme_tier_table_done_column_matches_the_ledger`
/ R-0360) require these two README values to move in the SAME commit
that flips a STATUS `[x]` line, and item 4b's change-set for C3 did not
name them.

```
$ python3 -m pytest tests/cli/test_golden_path.py -q
..........................................                               [100%]
42 passed in 21.00s
```
GREEN.

```
$ python3 -c "from packages.orchestration.integrity_gate import run_integrity_checks; r = run_integrity_checks(); print(r.passed, r.fail_count)"
True 0
handler_import: PASS (handlers=342)
live_review_verdict: PASS
plan_consistency: PASS (unchecked=0, context_complete=True)
relevant_untracked: PASS (untracked=0, relevant=0)
high_blockers_open: PASS (no open blocker/high findings)
```
GREEN, taken at C3's own commit (`255a4e5f`, current HEAD).

```
$ git status --porcelain
(empty)
```
CLEAN.

Per the block's own explicit constraint ("If ANY gate at C4 is not
green, STOP before C5 ... and declare the failure fully — do not
attempt a fix on this round's own initiative beyond what the block
already ordered") and self-drive protocol G8 ("Any red gate ... →
write the handoff and end cleanly. Never guess, never widen scope to
route around a block"), this round STOPS HERE. C5 (push + `gh pr
create`) was never started. `README.md`'s prose count and Tier 3 table
cell were deliberately NOT edited by me — fixing them was not ordered,
and the round's own rule forbids initiative fixes beyond what the block
ordered.

## Authored-text proofs

- `.agent/authored/f112-r30.md` (C0a): sha256 of the scratchpad source
  and the committed copy both read
  `0a02207955e2458e06b83d3e3361ba5d69a869af6186d0673da34317b9d6180c`
  (15327 bytes, 193 lines) — identical.
- `.agent/last_block.md` (C0b): `git rev-parse HEAD:...` on both paths
  (after commit) both read blob `3d23ac8094b202da5e2fb4ed179c0e4b3086614c`
  — identical.
- RECORD29 (C1), PLAN30 (C2), and READMEF112 (C3): byte-exact,
  hash-verified as reported under Verification above.
- STATUS.md's new F112 line (C3): extracted verbatim from the block's
  own line 22 (not retyped), applied via exact string match, confirmed
  by regex count (1 match `^\- \[x\] F112 — `, 0 matches
  `^\- \[~\] F112 — `).
- README.md's surrounding context after the READMEF112 insertion
  (lines 84-109 of the post-edit file):
```
84  mechanism is exercised by the suite and inert on real runs today).
85
86  F110 model routing by task class (every role Remedy resolves a runtime
...
95  documented benchmark run, never a bare config edit).
96
97  F112 prompt budget per task class (every task carries a class-scoped
...
108 ones).
109
```
  (line 97 begins the newly-inserted paragraph; the line immediately
  after it, currently blank, is followed by "Accepted in Tier 5 so
  far:" at line 110, confirmed unchanged from before this round.)

## Deviations & assumptions

1. **The round halted at C4, before C5, on a red docs gate the block's
   own C3 change-set did not anticipate.** `tests/docs/` failed two
   tests (`test_the_readme_accepted_count_equals_the_status_count`,
   `test_the_readme_tier_table_done_column_matches_the_ledger`) because
   flipping F112's STATUS line to `[x]` moved two derived numbers
   (README's "N of 266 accepted" prose, now stale at 69 vs the real 70;
   README's Tier 3 Done cell, now stale at 4 vs the real 5) that C3's
   own ordered change-set ("Exactly three files ... nothing else is
   touched in this commit") did not include. This is the SAME class of
   defect the open ledger already knows by name (R-0570: "the root
   README's accepted-feature list is pinned in one direction only";
   R-0360/R-0156 are the two tests that fired here) recurring as a
   BLOCK-AUTHORING gap rather than a worker error — the block ordered
   an edit that its own gate list (item 5, `tests/docs/`) was certain
   to catch as incomplete. I did NOT fix README's prose count or Tier
   3 cell myself: the block explicitly forbids an initiative fix
   beyond what it ordered when a C4 gate is red, so this is left for
   the next round's own authored block to correct (a fourth README
   value edit — "69 of 266" → "70 of 266" and the Tier 3 `Done` cell
   `4` → `5` — most likely folded into a small correction commit before
   C5's push/PR can proceed).
2. No push and no PR were created this round — C5 never started. This
   departs from the block's own ordered sequence (which named C5 as
   "THE PULL REQUEST" and expected it to run) but is exactly what the
   block's own constraint requires when C4 is red.
3. No `git worktree` (disposable) was used for destructive verification
   this round — none of this round's own changes touch production code
   under `packages/`/`apps/`, so G5 does not apply.
4. This round wrote NO new `Done:`/verdict line into
   `.agent/live_review.md` beyond RECORD29's verbatim C1 append —
   booking round 30's own outcome (a HALT, not a PASS) is the
   reviewer's job next round.

## Next

The reviewer should independently re-run `python3 -m pytest tests/docs/ -q`
to confirm the same two failures, then author a small correction block
(NOT this round's own initiative) that fixes exactly the two stale
README values — the "N of 266 accepted" prose (69 → 70) and the Tier 3
`Done` table cell (4 → 5) — in one additional commit before C5 (push +
`gh pr create`) can run. Nothing else on this branch is blocked: C0a
through C3 all verified byte-exact and green per the transcripts above,
the golden-path canary and integrity gate are both green, and the
closure commit's three-file change set is exactly what the block
ordered. The built review-package zip
(`remedy-review-20260904-123332-READY_FOR_REVIEW.zip`, sha256
`b0085f28a2c0c50654ed33be647ed986addc07c1c462324b1ee3fc1c8bb05927`, at
`/home/decodeux/Repos/remedy-history/zips/`) remains valid and
unchanged — it is unaffected by this docs-gate failure, which is a
prose-consistency issue in `README.md`, not a defect in the packaged
evidence.
