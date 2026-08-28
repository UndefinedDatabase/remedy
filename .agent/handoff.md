# Handback — F257 Self-use track, round 2 (THE QUEUE)

## Session

SESSION 1 of feature F257 · round 2 · rounds so far 2

## Range

Review of `cbf081eb`..HEAD

`cbf081eb2ea9d2d6572891ee8185f66f56041c0c` is BASE — the tip of
`feature/f257-self-use-track` at the end of round 1, verified by
`git rev-parse HEAD` before the first commit.

## Commits

Every `+/-` cell below is taken from `git diff --numstat` and matches, cell for
cell, the figures G8 reports.

### 204bbfd7 chore(f257): save the round 2 queue block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f257-r2.md` | +329 / -0 | C0a, the block saved verbatim |

### f2a22a9a chore(f257): mirror the round 2 block to last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +256 / -300 | C0b, mirrored from the same source bytes |

### 9f107573 docs(f257): advance the plan to the queue round
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +8 / -9 | C1, whole-file PLANF257R2 |

### 1026aae5 docs(f257): book the round 1 verdict and the two prose slips
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +10 / -0 | C2, GATEF257R1 appended |
| `.agent/prose_slips.md` | +4 / -0 | C2, SLIPSF257R1 appended |

### 5a0c5346 feat(f257): add the self-use queue and its read-only loader
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/self_use_queue.py` | +191 / -0 | C3, the loader (S4–S7) |
| `scripts/self_use_queue.json` | +13 / -0 | C3, the curated queue (S1–S3) |
| `tests/orchestration/test_self_use_queue.py` | +193 / -0 | C3, the tests (S8) |

### C4 — the handback commit (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | self-reference | this file; a handoff cannot table its own commit |

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → exit
  0, output verbatim `[]`. Constraint 0 satisfied; no pull request existed and
  none was created.
- `git rev-parse HEAD` → `cbf081eb2ea9d2d6572891ee8185f66f56041c0c`, equal to the
  BASE constraint 0 names. `git branch --show-current` →
  `feature/f257-self-use-track`.
- `git worktree add .remedy-wt/g6 5a0c5346 --detach` → exit 0, detached at
  `5a0c5346`. Used for G6 only.
- `git worktree remove --force .remedy-wt/g6` → exit 0. Afterwards
  `git worktree list` prints ONE line, the primary checkout at `5a0c5346`, and
  `git status --porcelain | wc -l` = 0 in the primary.
- `git push origin feature/f257-self-use-track` after C4. The outcome cannot be
  written into this file, which is inside C4; it is reported in the round's final
  message.
- NO pull request was created, nothing was merged, nothing was force-pushed,
  rebased or amended, and no history was rewritten.

## Verification — one line per gate

- G1 HYGIENE — PASS. `.agent/STOP` absent before C0a (`os.path.exists` → False)
  and absent again before C3 (False). Constraint 0's three readings are under
  External actions above: `gh pr list` → `[]`, HEAD → `cbf081eb…`, branch →
  `feature/f257-self-use-track`. `git status --porcelain | wc -l` = 0 after C0a,
  0 after C0b, 0 after C1, 0 after C2 and 0 after C3 — five direct readings.
- G2 TRANSPORT — PASS. The committed C0a blob
  `git show 204bbfd7:.agent/authored/f257-r2.md` and the reviewer's own original
  `.remedy-wt/f257-r2-block.md` are both 21619 bytes with sha256
  `4eb114cad7a8059de6b870894193cd11a086efb5add9171c375802a8c654655f`; EQUAL True.
  That original was written before this worker existed and is not this worker's
  output, so the reading covers real transport and not merely self-consistency;
  it covers no EMISSION, because this workflow has none. At C0b,
  `git rev-parse f2a22a9a:.agent/authored/f257-r2.md` and
  `git rev-parse f2a22a9a:.agent/last_block.md` print ONE blob id,
  `7696a515198319d27abd6972e08515998a1fd6c8`.
- G3 THE PLAN AT C1 — PASS. `.agent/plan.md` at C1 equals PLANF257R2 including
  the trailing newline: True. `wc -l` = 35, under 50. Lines exactly `## Goal` =
  1; lines exactly `## Next Steps` = 1.
- G4 THE RECORD APPEND AT C2 — PASS, both readers, over `.agent/live_review.md`.
  (a) The `cbf081eb` blob + newline + GATEF257R1 + newline equals the C2 blob
  under constraint 8: True. NEGATIVE CONTROL: byte offset 1375223, which the
  script confirmed lies inside the FIRST appended paragraph (context
  `which merged the F256 closure `), was flipped and the equality became False.
  (b) N = 5, the number of blank-line paragraphs GATEF257R1 holds, counted by the
  script FROM THE SLICE and never read off the block; the LAST 5 units of the C2
  file match those 5 paragraphs IN ORDER, unit by unit, all True, at lengths 299,
  593, 961, 647 and 675. The pre-round blob is a byte PREFIX of the C2 blob:
  True, 1375172 bytes → 1378357 bytes. Separately, `.agent/prose_slips.md` at C2
  reconstructs from its `cbf081eb` blob and SLIPSF257R1 under constraint 8: True,
  14908 bytes → 15556 bytes.
- G5 THE LEDGER AT C2 — PASS. Over `.agent/live_review.md`, `cbf081eb` → C2:
  lines matching `^- R-\d+ — ` 293 → 293, UNMOVED, and ALL DISTINCT at both
  points; `^Done: R-\d+ — ` 44 → 44, UNMOVED; `^Landed: R-` 11 → 11, UNMOVED;
  `^Gate: F\d+ R\d+ — ` 106 → 107, risen by exactly one; OPEN SET
  (registrations − resolutions) 249 → 249, UNMOVED. Lines matching
  `^Gate: F257 R1 — ` at C2 = 1. See deviation 5 on the open-set figure.
- G6 THE LOADER RED-PROOF AT C3 — PASS, entirely inside the disposable worktree
  `.remedy-wt/g6`, never in the primary. UNMUTATED CONTROL FIRST, in that
  worktree: `python3 -m pytest tests/orchestration/test_self_use_queue.py -q` →
  REAL exit 0, 18 passed. MUTATION (i), breaking S5 by returning an empty tuple
  instead of raising when the queue file is missing (anchor asserted unique,
  count = 1) → REAL exit 1, 1 failed / 17 passed, the failure being
  `TestLoaderRaisesRatherThanReturningEmpty::test_missing_file_raises`
  ("DID NOT RAISE"). Reverted byte-clean (sha256 back to
  `c3359e5b2ce3f50b9609b22e3dfc3fa0b2d67b7c4da943bb49a1f2fa999c5d3f`). MUTATION
  (ii), breaking S6 by answering the first item regardless of `consumed_by`
  (anchor asserted unique, count = 1) → REAL exit 1, 2 failed / 16 passed,
  the failures being `TestNextSelfUseItem::test_skips_a_consumed_item` and
  `TestNextSelfUseItem::test_all_consumed_answers_none`. Reverted byte-clean to
  the same sha256. CONTROL AGAIN, module restored: REAL exit 0, 18 passed, and
  `git status --porcelain` inside the worktree printed nothing, so the module was
  byte-identical to the committed blob. After removal, `git worktree list` prints
  one line — `/home/decodeux/Repos/remedy 5a0c5346 [feature/f257-self-use-track]`
  — and `git status --porcelain | wc -l` = 0 in the primary.
- G7 THE SUITES AT C3 — PASS. One pytest process at a time, from the repository
  root, in the PRIMARY checkout, each with its REAL exit code:
  `tests/orchestration/test_self_use_queue.py` 18 passed, exit 0;
  `tests/test_data_paths.py` 23 passed, exit 0;
  `tests/test_path_utils.py` 28 passed, exit 0;
  `tests/regression/test_named_bugs.py` 64 passed / 6 skipped, exit 0;
  `tests/orchestration/test_development_artifact_boundary.py` 18 passed, exit 0;
  `tests/ui_server/` 497 passed, exit 0;
  `tests/orchestration/test_test_runner.py` 52 passed, exit 0;
  `tests/regression/test_resource_safety.py` 21 passed, exit 0;
  `tests/orchestration/test_integrity_gate.py` 16 passed, exit 0;
  `tests/orchestration/test_job_promote.py` 85 passed, exit 0;
  `tests/orchestration/test_fences.py` 78 passed, exit 0;
  the canary `tests/cli/test_golden_path.py` 42 passed, exit 0.
  Twelve runs, twelve exit-0 readings, none red.
- G8 STRUCTURE over `cbf081eb..5a0c5346` — PASS on every clause. The range
  touches exactly eight paths: `.agent/authored/f257-r2.md`,
  `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
  `.agent/prose_slips.md`, `packages/orchestration/self_use_queue.py`,
  `scripts/self_use_queue.json`, `tests/orchestration/test_self_use_queue.py`.
  The path EXCLUDED from the change-set side, as G8 directs, is
  `.agent/handoff.md`, which C4 writes; the changeset-minus-range residue over
  the remaining eight is `[]`, EMPTY. The range-minus-changeset residue, computed
  against the FULL nine-path change set, is `[]`, EMPTY. Per-commit insertions
  from `git diff --numstat`: 329, 256, 8, 14 and 397 — each under 500 — and each
  of C0a, C0b, C1, C2 and C3 is single-parent (1 parent each). Counted
  affirmatively over each file's C3 content, lines beginning `<<<SLICE ` and
  lines beginning `<<<END ` are 0 and 0 in `.agent/plan.md`, 0 and 0 in
  `.agent/live_review.md`, 0 and 0 in `.agent/prose_slips.md`, 0 and 0 in
  `scripts/self_use_queue.json`, 0 and 0 in
  `packages/orchestration/self_use_queue.py`, and 0 and 0 in
  `tests/orchestration/test_self_use_queue.py`, against the non-zero control
  `.agent/authored/f257-r2.md` at 3 and 3. `git ls-files .remedy-wt | wc -l` = 0.

## Authored-text proofs

Every reviewer-authored text applied this round was extracted from the COMMITTED
blob `git show 204bbfd7:.agent/authored/f257-r2.md` under constraint 3, never
from the prompt, and the delimiter lines reached no target file (G8, 0 and 0 in
all six targets against 3 and 3 in the control).

- `.agent/plan.md` at C1 — whole-blob equality with PLANF257R2, True (G3).
- `.agent/live_review.md` at C2 — the whole file reconstructs byte for byte as
  the `cbf081eb` blob + newline + GATEF257R1 + newline, True, with the pre-round
  blob a byte prefix, a negative control rejected, and the last 5 paragraphs
  matching the slice in order (G4).
- `.agent/prose_slips.md` at C2 — reconstructs byte for byte as the `cbf081eb`
  blob + newline + SLIPSF257R1 + newline, True (G4).
- The production code of C3 is DESCRIBED by the block's SPEC rather than sliced,
  so no authored-text proof applies to it; it is proved by G6 and G7 instead.

## Deviations & assumptions

1. NO DEPARTURE FROM THE ORDERED COMMIT SEQUENCE. C0a, C0b, C1, C2, C3 and C4
   were committed in that order; none was added, none dropped, none reordered.
2. The Session line carries the block's exact string
   `SESSION 1 of feature F257 · round 2` and then appends `· rounds so far 2`,
   because docs/agents/handback_template.md mandates the `rounds so far <total>`
   field. Both requirements are met rather than one chosen over the other.
3. GUARD RE-EXPRESSIONS, which constraint 6 obliges reporting. TWO commands were
   ACTUALLY rejected by this session's guard and re-expressed, never skipped and
   never weakened:
   (a) the G5 ledger reader was first written as a `python3 - <<'PY'` heredoc
   whose body contained a brace literal holding quotes (a dict of regex names);
   it was REJECTED, and was re-expressed as a scratch script
   `.remedy-wt/g5_ledger.py` built from parallel `list([...])` structures with no
   quoted brace literal, then run as `python3 .remedy-wt/g5_ledger.py`. Every
   count it makes is the count the gate ordered.
   (b) a combined `bash -c` chaining `git status …; python3 -c …` with nested
   single quotes was REJECTED with a shell syntax error; it was re-expressed as
   two separate single-purpose calls, and both readings were taken.
   Pre-emptively avoided rather than discovered: `cp` was never used (both block
   copies went through `shutil.copyfile`); no environment variable was assigned
   in any of the three rejected spellings (the tests set `REMEDY_DATA_DIR`
   in-process through pytest's `monkeypatch.setenv`); the G6 mutations were
   applied from a scratch script `.remedy-wt/g6_mutate.py` rather than an inline
   heredoc; and every exit code above was captured with
   `bash -c '<cmd>; echo "REAL_EXIT=$?"'` or, for the piped pytest runs, with
   `${PIPESTATUS[0]}` inside such a `bash -c`. Three scratch files
   (`g5_ledger.py`, `g6_mutate.py`, `g8_structure.py`) and one pristine module
   copy (`g6_pristine.py`) were written under the gitignored `.remedy-wt/`;
   `git ls-files .remedy-wt | wc -l` = 0 confirms none is tracked.
4. NO GATE FORMULA CONTRADICTED CONSTRAINT 8 THIS ROUND. Both appends were made
   as base + one newline + slice + one newline, exactly as constraint 8 states,
   and G4's own wording asks for the reconstruction "under constraint 8", so the
   R1 disagreement that constraint 8 exists to prevent did not recur. Declared
   affirmatively because the prompt asked for it either way.
5. G5's OPEN-SET FIGURE IS 249, WHERE THE ROUND 1 HANDBACK SAID 251. The 249 is
   computed by G5's own stated formula — registrations (293) minus resolutions
   (44) — measured identically at `cbf081eb` and at C2, so the round's claim
   (UNMOVED) holds on either reading. The earlier 251 was inherited prose, not
   re-derived by this gate's formula; it is flagged rather than reconciled,
   because reconciling it is not in this round's change set and no id is minted.
6. THE TWO PROSE-SLIP LINES ARE DATED 2026-08-28 and this round ran on
   2026-08-29. They are reviewer-authored text and constraint 1 forbids
   correction, so they were applied byte for byte as written. The same holds for
   GATEF257R1's own dating and its internal readings, all of which are the
   reviewer's measurements at `cbf081eb` and not this round's.
7. CONSTRAINT 7'S GUARDS ARE SATISFIED BY CONSTRUCTION, verified by grep over
   `packages/orchestration/self_use_queue.py` before C3: no
   `os.environ.get("REMEDY_DATA_DIR")`, no `_MAX_PATH_COMPONENT_LENGTH`, no
   `[^a-zA-Z0-9_-]` regex, no bare `except: pass`, and no reference to
   `.agent/live_review.md`. All four named guard suites ran green in G7.
8. NO `Done:` OR `Gate:` PARAGRAPH OF THIS WORKER'S OWN was written anywhere.
   GATEF257R1 is the only such paragraph added to `.agent/live_review.md`, and it
   is reviewer-authored text applied verbatim. This round mints no finding id and
   resolves none.
9. `python3 -B` and `-p no:cacheprovider` were used for the G6 mutation runs so a
   stale `__pycache__` could not mask a mutation. The G6 control runs before and
   after the mutations used the plain command the gate names; both were green.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block to `.agent/authored/f257-r2.md` | done | `204bbfd7` |
| C0b mirror the same bytes into `.agent/last_block.md` | done | `f2a22a9a` |
| C1 advance `.agent/plan.md` | done | `9f107573` |
| C2 book the R1 verdict and append the two prose slips | done | `1026aae5` |
| C3 the queue file, its loader and its tests | done | `5a0c5346` |
| C4 rewrite `.agent/handoff.md` | done | this file |
| the push | done | outcome in the round's final message, not tableable here |
| G1 hygiene | done | PASS; both `.agent/STOP` readings False, five clean-tree readings |
| G2 transport | done | PASS; 21619 bytes, digests EQUAL, one blob id at C0b |
| G3 the plan at C1 | done | PASS; byte-equal True, 35 lines, 1 and 1 |
| G4 the record append at C2 | done | PASS; N = 5, negative control rejected, prefix True |
| G5 the ledger at C2 | done | PASS; 293 / 44 / 11 unmoved, gates 106 → 107, F257 R1 = 1 |
| G6 the loader red-proof at C3 | done | PASS; control 18 green, both mutations exit 1 |
| G7 the suites at C3 | done | PASS; twelve runs, every one exit 0 |
| G8 structure | done | PASS; both residues empty, insertions 329/256/8/14/397 |

## Open findings

249 open in the ledger by G5's formula, all inherited from earlier features and
UNMOVED across this round's range: 293 registrations minus 44 resolutions at
`cbf081eb` and the same at C2. No finding was registered, resolved or moved this
round — the only ledger line added is the reviewer-authored `Gate: F257 R1`
paragraph, which is a verdict and not a finding. None is open against F257. See
deviation 5 on the 249-versus-251 reading.

## Next

The single expected next action is THE NEXT DELEGATED ROUND OF F257, which
renders a pending queue item into a job file and plans it through
`plan_job_from_file`, so the queue reaches the real job path. No pull request
exists for this branch and none was created this round.
