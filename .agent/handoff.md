# Handback — F256 Diff viewer completion, round 10 (THE CLOSURE)

## Session

SESSION 2 of feature F256 · round 10 · THE CLOSURE · rounds so far 10

## Range

Review of `64c3774f`..HEAD

## Commits

### d28a0c54 chore(f256): save the round 10 closure block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f256-r10.md` | +359 / -0 | C0a, the block saved verbatim |

### e04c1e0c chore(f256): mirror the round 10 block to last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +295 / -345 | C0b, mirrored from the C0a blob |

### fdb0200f docs(f256): advance the plan to the closure round
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +11 / -13 | C1, whole-file PLANF256R10 |

### 5a1b94ed docs(f256): resolve R-0732 and book the round 9 verdict
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +12 / -0 | C2, DONER0732 then GATEF256R9 |

### C3 — the closure commit (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/STATUS.md` | +1 / -1 | S1, the F256 line flipped to `[x]` |
| `README.md` | +8 / -2 | S2, S3 and the S4 CAPABILITY insertion |
| `.agent/handoff.md` | self-reference | this file; a handoff cannot table its own commit |

Rule A4 holds: C3 is the last commit on the branch. The closure gate raised no
candidate, so the one permitted successor (DECISION amend0827 D2's
`.agent/candidates.md`-only commit) was not created and `.agent/candidates.md`
stays empty.

## Closure record

| Field | Value |
|-------|-------|
| Evidence job | `f256-closure` |
| Package | `remedy-review-20260828-233819-READY_FOR_REVIEW.zip` |
| SHA-256 | `5f18d7acdeab790b0f79181c7179023535b389ce0b76ec427f2765b20cda4ad5` |
| Archived path | `/home/decodeux/Repos/remedy-history/zips` |
| Accepted HEAD | `c6775b3c41f1d1fa4b0f4bb7907307573855a61b` |

All five were measured in round 9 and are carried, not re-derived.

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`
  (the constraint-0 Open PR Gate reading, before any write).
- `git push -u origin feature/f256-diff-viewer-completion` after C3.
- `gh pr create` after C3, base `main`, head
  `feature/f256-diff-viewer-completion`, title `F256 — Diff viewer completion`,
  body exactly the PRBODY slice. The PR NUMBER cannot appear in this file — the
  PR is created after C3 and this file is inside C3 — so it is reported in the
  round's final message and in the PR itself.
- The PR is deliberately NOT merged. Nothing was force-pushed, rebased, amended
  or deleted.

## Verification — one line per gate

- G1 HYGIENE — PASS. `.agent/STOP` absent before C0a and again before C3. HEAD
  before C0a `64c3774f64c93decc864c8389181de8ed8dd91b1`, branch
  `feature/f256-diff-viewer-completion`, `git status --porcelain | wc -l` = 0
  after each of C0a, C0b, C1, C2 and C3. `64c3774f..C3` `git diff --name-only`
  is exactly the change set, both residues empty. `git diff --stat` restricted
  to `apps/`, `packages/`, `tests/` and `docs/roadmap/features/` printed NOTHING
  for all four. Insertions per commit 359, 295, 11, 12 and 168 — each under 500 —
  and all five commits single-parent. `<<<SLICE ` and `<<<END ` counts are 0 in
  `.agent/plan.md`, `.agent/live_review.md`, `docs/roadmap/STATUS.md` and
  `README.md`, against the non-zero control in `.agent/authored/f256-r10.md`.
  `git ls-files .remedy-wt | wc -l` = 0.
- G2 TRANSPORT — PASS. The C0a blob and the reviewer's own
  `.remedy-wt/f256-r10-block.md` are both 23158 bytes with sha256
  `4025d4b68d51f69fbbb4725f1af9c26f6f9053273ee8401f5bdde0c57973337e`; EQUAL True.
  At C0b `.agent/authored/f256-r10.md` and `.agent/last_block.md` are ONE blob id,
  `98fbd1447a9020e3b3f3a02b7c858e1d6b13ab99`.
- G3 THE PLAN AT C1 — PASS. C1 blob equals PLANF256R10 including the trailing
  newline: True. 32 lines (under 50); exactly one `## Goal` and one
  `## Next Steps`.
- G4 THE RECORD AT C2 — PASS. base + newline + DONER0732 + newline + GATEF256R9
  equals the C2 blob: True. The pre-round blob is a byte PREFIX: True. The
  negative control flipped byte offset 1369470, confirmed inside the first
  appended paragraph's span (1369370, 1371176), and the equality became False.
  N = 6 appended paragraphs, counted by the script; the LAST 6 blank-line units
  match them IN ORDER: True. `Done: R-0732 — ` occurs once; `Gate: F256 R9`
  occurs once.
- G5 THE LEDGER AT C2 — PASS. Registrations UNMOVED at 293 and all DISTINCT.
  `^Landed: R-` UNMOVED at 11. `^Done: R-\d+ — ` 43 → 44, rise of exactly one.
  `^Gate: F\d+ R\d+ — ` 105 → 106, rise of exactly one. The OPEN SET as a set
  252 → 251, a fall of exactly one, and the sole departure is `R-0732`: it WAS
  in the open set at `64c3774f` and is NOT in it at C2.
- G6 THE CLOSURE EDIT AT C3 — PASS. FROM count at `64c3774f` is 1 for each of
  S1, S2 and S3; at C3 each TO count is 1 and each FROM count is 0. The S4
  anchor line counted 1 before the insertion; the CAPABILITY text occurs exactly
  once at C3, the F037 paragraph above it is byte-unchanged, and CAPABILITY sits
  immediately after it. `git diff --numstat 64c3774f..C3 -- docs/roadmap/STATUS.md`
  is exactly 1 insertion and 1 deletion. Lines matching `^- \[x\] F\d{3} — ` in
  STATUS at C3 = 61, and the README's `N of 257` line states 61 — EQUAL.
- G7 THE DOCS GATE AND THE SUITES — PASS, in the primary checkout, one pytest
  process at a time, on the tree carrying exactly C3's content:
  `tests/docs/` 295 passed in 0.54 s, exit 0; `tests/ui_contracts/` 664 passed,
  4 skipped in 6.04 s, exit 0; `tests/ui_server/` 497 passed in 30.54 s, exit 0;
  the canary `tests/cli/test_golden_path.py` 42 passed in 20.57 s, exit 0.
  THE FOUR EDITS TRAVEL IN ONE COMMIT FOR A MEASURED REASON: the reviewer
  measured, in a disposable worktree at `64c3774f`, that applying S1 ALONE — the
  STATUS flip with `README.md` untouched — turns `tests/docs/` RED at 2 failed
  and 293 passed, naming `test_the_readme_accepted_count_equals_the_status_count`
  and `test_the_readme_tier_table_done_column_matches_the_ledger`. That is the
  R-0154 ledger cross-check pin, and it is why STATUS and README may never
  disagree in any committed state.
- G8 THE PULL REQUEST — created after C3, so its number cannot be written into
  this file, which is inside C3. The PR is created with `gh pr create` against
  base `main` from `feature/f256-diff-viewer-completion`, title
  `F256 — Diff viewer completion`, body exactly the PRBODY slice; the number and
  URL are reported in the round's final message. It is NOT merged. C3 is the
  last commit on the branch.

## Authored-text proofs

Every piece of reviewer-authored applied text is byte-identical to the authored
slice or pair it came from, each measured against the COMMITTED blob
`.agent/authored/f256-r10.md` rather than against any prompt text:

- `.agent/plan.md` at C1 — whole-blob equality with PLANF256R10, True (G3).
- `.agent/live_review.md` at C2 — the whole file reconstructs byte for byte as
  base + newline + DONER0732 + newline + GATEF256R9, True, with the pre-round
  blob a byte prefix and a negative control rejected (G4).
- The STATUS line — the S1 TO string occurs exactly once at C3 and the FROM
  string zero times.
- The README pins — the S2 and S3 TO strings each occur exactly once at C3 and
  their FROM strings zero times.
- The CAPABILITY paragraph — occurs exactly once at C3, immediately after a
  byte-unchanged F037 paragraph.

## Deviations & assumptions

1. NO DEPARTURE FROM THE ORDERED COMMIT SEQUENCE. C0a, C0b, C1, C2 and C3 were
   committed in that order, none added, none dropped, none reordered. No
   `.agent/candidates.md` commit follows C3 because the closure gate raised no
   candidate.
2. The Session line carries the block's exact string
   `SESSION 2 of feature F256 · round 10 · THE CLOSURE` and then appends
   `· rounds so far 10`, because docs/agents/handback_template.md mandates the
   `rounds so far <total>` field. Both requirements are met rather than one
   chosen over the other.
3. GUARD RE-EXPRESSIONS, none skipped and none weakened. This session's shell
   guard rejected `${PIPESTATUS[0]}` in the suite invocation; the check was
   re-expressed as `.remedy-wt/f256_r10_suite.py`, which runs the same pytest
   command and prints the REAL exit code, and prints the full untruncated output
   on any non-zero exit. All other work ran through script files under the
   gitignored `.remedy-wt/`: the slice extractor, the G4, G5 and G6 measurement
   scripts and the C3 applier. Nothing was checked by a weaker spelling.
4. The PLANF256R10 slice books "the STATUS closure and the PR" as `done` in
   `.agent/plan.md` at C1 — that is, one commit BEFORE the closure commit and two
   before the PR exists. It is the reviewer's authored text and was applied
   verbatim under constraint 1; it is declared here because at C1 the claim ran
   ahead of the disk. It is true at C3.
5. G8's PR number cannot appear in this file. The block anticipates this; the
   number and URL are in the round's final message and on the PR itself.
6. G7 was run on the working tree carrying exactly C3's content for every file
   the four edits touch, immediately before C3 was committed, because a suite
   result must be inside the handoff and the handoff is inside C3. The blob
   contents the suites read are identical to C3's.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block | done | |
| C0b mirror to last_block | done | |
| C1 advance the plan | done | |
| C2 resolve R-0732, book the R9 verdict | done | |
| C3 the closure commit | done | STATUS, README and this file in ONE commit |
| the pull request | done | created after C3, NOT merged |
| G1 hygiene and structure | done | PASS |
| G2 transport | done | PASS |
| G3 the plan at C1 | done | PASS |
| G4 the record at C2 | done | PASS |
| G5 the ledger at C2 | done | PASS |
| G6 the closure edit at C3 | done | PASS |
| G7 the docs gate and the suites | done | PASS, all four exit 0 |
| G8 the pull request | done | created, unmerged; number in the final message |

## Open findings

251 open in the ledger, all inherited from earlier features. NONE is open
against F256: `R-0732`, the only finding this feature registered, is resolved in
C2 of this round.

## Next

The single expected next action is THE OPEN PR GATE AT THE NEXT FEATURE'S START.
This PR is deliberately left unmerged — that gap is the operator's manual-review
window, and the operator may merge it by hand at any time. Rule A5's next
feature is F257 — Self-use track, the first unchecked STATUS line after F256.
