# Handback — F032 R10 (T002e: the two producers that cite nothing)

## Session

SESSION 3 of feature F032 · round R10 · rounds so far 10

Session 1 was R1 through R5, session 2 was R6 through R9, and session 3 opens
here at R10. Ten rounds across three sessions is inside the soft limit of 25
rounds or 7 sessions, so no limit report is owed.

## State

- Feature: F032, approval with the evidence triple. Round R10, task slice T002e.
- Branch: `feature/f032-evidence-triple`, round base `0216c5bb` (the commit that
  closed session 2).
- Commits this round: `b1790261`, `83529164`, `aace7acb`, `c3bc8bb3`,
  `68ff6d8c`, `e2e9471b`, `0a6c17bf`, plus this handback commit.
- Open findings after C2: 250 (274 registered ids minus 24 resolved). Maximum id
  `R-0713`, which C2 resolves.
- SIX of the eight producing types are now enforced: `token_budget`,
  `test_failure`, `patch_approval`, `stop_reason`, `repo_dirty`,
  `memory_review`. `flight_plan_approval` and `task_decision` remain.
- No pull request was created and nothing was merged.

## Range

Review of `0216c5bb`..HEAD.

## Commits

Every `+/-` below is read from `git diff --numstat <sha>^ <sha>`, summed over the
commit's files. The same reading produces the insertion counts reported under G8;
the two were derived from one `git diff --numstat` pass and compared cell by
cell, and they agree.

### b1790261 docs(agent): save the F032 R10 step block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f032-r10.md | +332 / -0 | C0a — byte-preserving copy of `.remedy-wt/f032-r10.md` |

### 83529164 docs(agent): mirror the R10 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +274 / -292 | C0b — same bytes as C0a; git resolves both to blob `a991368a` |

### aace7acb docs(agent): set the plan to the R10 round
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +22 / -22 | C1 — the PLANF032R10 slice, applied byte for byte |

### c3bc8bb3 docs(agent): book the R9 verdict and resolve R-0713
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +4 / -0 | C2 — the LEDGER10 slice appended; the only commit touching the ledger |

### 68ff6d8c feat(orchestration): the dirty-repo card cites the reading it came from
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/decision_queue.py | +47 / -0 | C3 — S2 and S3: the two repo-dirty refs and the one unkeyed outcome |
| packages/orchestration/decision_evidence.py | +1 / -0 | C3 — `repo_dirty` joins `TRIPLE_REQUIRED_TYPES` in the same commit |

### e2e9471b feat(orchestration): the memory-review card cites the card and its flags
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/decision_queue.py | +54 / -0 | C4 — S4 and S5: three guarded refs and the one unkeyed outcome |
| packages/orchestration/decision_evidence.py | +1 / -1 | C4 — `memory_review` joins `TRIPLE_REQUIRED_TYPES` in the same commit |

### 0a6c17bf test(orchestration): pin the two thinnest triples and repoint the guards
| Path | +/- | Reason |
|------|-----|--------|
| tests/orchestration/test_decision_evidence.py | +341 / -3 | C5 — S6 and S7: the new T002e tests, the two repointed guards, the exact-membership update |

### C6 — this handback
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | not tabled | A handoff cannot table the commit that writes it (R-0149 pattern); C6's own numstat is not a value this round writes anywhere |

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | |
| C0b mirror into `last_block` | done | |
| C1 the plan | done | |
| C2 the R9 verdict and `Done: R-0713` | done | |
| C3 the repo-dirty triple and its gate entry | done | |
| C4 the memory-review triple and its gate entry | done | |
| C5 the tests and the two repointed guards | done | |
| C6 the handback | done | this commit |
| S1 read the emitter and the fixtures first | done | confirmed on disk; see Deviations for what the reading found |
| S2 the repo-dirty refs | done | one unguarded event-name ref, one guarded `status_hash` ref |
| S3 the repo-dirty unkeyed outcome | done | no `payload`; one outcome keyed `UNKEYED_OPTION` |
| S4 the memory-review refs, all three guarded | done | the two booleans R5 computes are reused, not re-read |
| S5 the memory-review unkeyed outcome | done | no `payload`; one outcome keyed `UNKEYED_OPTION` |
| S6 the two guards repointed, never deleted | done | both moved to `flight_plan_approval`; docstring corrected; exact membership updated to six |
| S7 the new tests | done | 22 new tests, all driving the real branches through `list_decisions` |

## External actions

- `git worktree add --detach .remedy-wt/f032-r10-mut 0a6c17bf` — created, used for
  the three G7 mutations, then `git worktree remove` + `git worktree prune`.
  `git worktree list` is back to 1 line.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — `[]`.
  Nothing merged, nothing created, as the block orders.
- `git push -u origin feature/f032-evidence-triple` after this commit.
- Gate scratch scripts were written under the gitignored `.remedy-wt/`;
  `git ls-files .remedy-wt` is 0 lines.

## Verification

- G1 HYGIENE, BASE AND THE SENTINEL — `git rev-parse HEAD` before C0a printed
  `0216c5bb9d4885e9120f64194c946847ed372bde`, the round base of constraint 12;
  `git rev-parse --abbrev-ref HEAD` printed `feature/f032-evidence-triple`;
  `git status --porcelain | wc -l` printed 0 after each of C0a, C0b, C1, C2, C3,
  C4 and C5. `ls -la .agent/STOP` exited 2 with
  `ls: cannot access '.agent/STOP': No such file or directory` at BOTH readings
  constraint 9 orders — once before C0a and once before C6. See Deviations for
  the one part of G1 that cannot be written into C6.
- G2 TRANSPORT — sha256
  `bd2560b02c3bfd65c497fcde4ce0811f30013658040703fdfd0f7aa950990a4a` over 27191
  bytes and 332 lines is EQUAL for all three artefacts: the reviewer's scratch
  original `.remedy-wt/f032-r10.md`, the committed `.agent/authored/f032-r10.md`
  blob at `b1790261` and the committed `.agent/last_block.md` blob at `83529164`.
  `git rev-parse` on both committed paths returns the SAME blob,
  `a991368a80c90618c886fdc4d6df4903becc141d`. This proves the scratch original,
  the saved copy and the mirror agree; it says NOTHING about the bytes of any
  prompt.
- G3 EXTRACTION AND CAPS — from the committed C0a blob: region `PLANF032R10`
  with 48 content lines, region `LEDGER10` with 3 content lines; 2 regions;
  CONTENT total 51; TOTAL 332 lines; PROSE 281. PROSE under 400 = True, TOTAL
  under 490 = True.
- G4 THE PLAN — `.agent/plan.md` at `aace7acb` is byte-equal to slice
  PLANF032R10 under constraint 2 (True). NEGATIVE CONTROL with the trailing
  newline removed: False, as required. `wc -l` = 48, under 50 = True.
  `^## Goal` = 1, `^## Next Steps` = 1.
- G5 THE LEDGER APPEND — `git show 0216c5bb:.agent/live_review.md` gives 1071711
  bytes over 425 blank-line units, matching the reviewer's measurement exactly.
  READER 1, byte identity: 1071711 + 1 + 4760 = 1076472, the C2 blob is 1076472
  bytes, BYTE-EQUAL = True, and the pre-commit blob is a byte PREFIX of the
  result = True. READER 2, structural: the LEDGER10 slice is 2 blank-line
  paragraphs, and the LAST 2 units of the file match those 2 paragraphs IN ORDER
  = True. NEGATIVE CONTROL, one byte flipped in memory at offset 1071752 inside
  the FIRST appended paragraph: reader 1 rejects = True, reader 2 rejects = True.
  Counts before → after C2: `^Gate: F\d+ R\d+ — ` 61 → 62; `^- R-\d+ — ` 274 →
  274; `^Done: R-\d+ — ` 23 → 24; `^Landed: R-` 1 → 1; `^Gate: R\d+ — ` 19 → 19.
  Open set 251 → 250. Maximum id `R-0713` both before and after. Gate key ADDED:
  `F032 R9`, one key. Id ADDED to the resolved set: `R-0713`, one id. All five
  base numbers and the base open set and maximum match what the block states.
- G6 THE CODE, LINTED AND READ BACK —
  `python3 -m ruff check packages/orchestration/decision_queue.py packages/orchestration/decision_evidence.py`
  exit code 0, verbatim output `All checks passed!`. Calling `list_decisions` at
  C4:
  - repo-dirty from the THIN event of S1 (`metadata` = `{"dirty": True}`) —
    refs `[('failure', 'git_status_read', 'the run-log event that reported the working tree dirty')]`;
    outcomes `[('', "Committing or stashing the target repository's changes leaves a clean tree, so a later diff shows only what this job did.", "The job waits while that happens, and stashing work that is not this job's can hide changes their author still needs.")]`.
  - repo-dirty from the FULL metadata of S1 — refs
    `[('failure', 'git_status_read', 'the run-log event that reported the working tree dirty'), ('failure', '6f1c2d3e4a5b6c7d', 'the status fingerprint that reading recorded')]`;
    the same one outcome.
  - memory review, stale only — refs
    `[('decision', 'deploy-target', 'the memory card this review is about'), ('failure', 'stale', 'the validity the card carries')]`;
    outcomes `[('', 'Opening the named card shows what it claims and when that was last confirmed, so it can be re-approved, corrected or superseded instead of trusted blind.', 'Reading it takes time now, and a card left in place while it is checked keeps feeding whatever already reads it.')]`.
  - memory review, flagged only — refs
    `[('decision', 'api-contract', 'the memory card this review is about'), ('failure', 'needs_review', 'the review status the card carries')]`;
    the same one outcome.
  - memory review, stale AND flagged — refs
    `[('decision', 'db-dsn', 'the memory card this review is about'), ('failure', 'stale', 'the validity the card carries'), ('failure', 'needs_review', 'the review status the card carries')]`;
    the same one outcome.
  - memory review, stale with an EMPTY key — refs
    `[('failure', 'stale', 'the validity the card carries')]`; the same one
    outcome. Rule (a) is satisfied with no key at all, which is the argument the
    key's guard rests on.

  `export_decision_json`'s `evidence_status` is `present` for the repo-dirty card
  and `present` for the memory-review card. `sorted(TRIPLE_REQUIRED_TYPES)` =
  `['memory_review', 'patch_approval', 'repo_dirty', 'stop_reason', 'test_failure', 'token_budget']`.
- G7 TESTS GREEN, THEN RED UNDER MUTATION —
  `python3 -B -m pytest tests/orchestration/test_decision_evidence.py -q` in the
  PRIMARY checkout at C5: exit code 0, `86 passed in 0.32s`, 0 `^FAILED` lines.
  In the disposable worktree at `0a6c17bf`, with `__pycache__` purged and `-B`
  passed before every run, and each exact byte string counted 1 in its file
  before it was applied and the file restored byte for byte afterwards:
  - CONTROL before any mutation — exit 0, `86 passed in 0.32s`, 0 `^FAILED`.
  - mutation (a), the `status_hash` ref of S2 made unconditional
    (`            if _rd_status_hash:` → `            if True:` in
    `decision_queue.py`, count 1) — exit 1, `3 failed, 83 passed in 0.39s`, 3
    `^FAILED`: `test_the_thin_git_status_event_still_yields_a_valid_repo_dirty_card`,
    `test_no_repo_dirty_ref_ever_points_at_nothing[thin-event]`,
    `test_the_repo_dirty_card_carries_exactly_one_unkeyed_outcome[thin-event]`.
  - mutation (b), the `review_status` ref of S4 made unconditional
    (`            if is_flagged_for_review:` → `            if True:` in
    `decision_queue.py`, count 1) — exit 1, `2 failed, 84 passed in 0.35s`, 2
    `^FAILED`: `test_the_memory_review_card_cites_the_card_and_its_staleness`,
    `test_the_memory_review_card_stays_valid_with_no_key_at_all`.
  - mutation (c), `repo_dirty` removed from `TRIPLE_REQUIRED_TYPES`
    (`    "repo_dirty", "memory_review",` → `    "memory_review",` in
    `decision_evidence.py`, count 1) — exit 1, `2 failed, 84 passed in 0.35s`, 2
    `^FAILED`: `test_the_shipped_required_type_set_holds_exactly_the_upgraded_producers`,
    `test_a_repo_dirty_decision_without_a_triple_is_refused_by_the_gate`.
  - CONTROL after all three restorations — exit 0, `86 passed in 0.32s`, 0
    `^FAILED`, and the worktree's `git status --porcelain` was the empty string.

  Then, as ONE pytest process in the primary checkout:
  `python3 -B -m pytest tests/orchestration/test_decision_evidence.py tests/orchestration/test_decision_inbox.py tests/orchestration/test_approval_queue.py -q`
  — exit code 0, `146 passed in 0.65s`, 0 `^FAILED` lines.
- G8 STRUCTURE, CANARY AND THE PR GATE —
  `python3 -B -m pytest tests/cli/test_golden_path.py -q` exit code 0,
  `42 passed in 20.70s`. `git diff --name-only 0216c5bb..0a6c17bf` yields exactly
  the seven Change-set paths other than `.agent/handoff.md`; BOTH residues are
  EMPTY (actual-minus-change-set `[]`, change-set-minus-actual `[]`).
  `git diff --stat 0216c5bb..0a6c17bf -- apps/` and the same for `-- docs/` are
  both the empty string. Per-commit insertions, each single-parent and each under
  500: `b1790261` 332, `83529164` 274, `aace7acb` 22, `c3bc8bb3` 4, `68ff6d8c`
  48, `e2e9471b` 55, `0a6c17bf` 341. Those counts and the `+/-` column of the
  `## Commits` section above are one reading written twice, derived from
  `git diff --numstat`, compared cell by cell, and they AGREE. Marker sweep,
  counts of `^<<<SLICE ` and `^<<<END `: `.agent/plan.md` 0/0,
  `.agent/live_review.md` 0/0, `packages/orchestration/decision_queue.py` 0/0,
  `packages/orchestration/decision_evidence.py` 0/0,
  `tests/orchestration/test_decision_evidence.py` 0/0 — against the CONTROL over
  the committed C0a blob, which is 2/2 and therefore non-zero.
  `git ls-files .remedy-wt` 0 lines, `git worktree list` 1 line,
  `git branch --list "tmp/*"` 0 lines.
  `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
  printed `[]`; nothing was merged and nothing was created.

## Authored-text proofs

Two reviewer-authored slices were applied, plus the block itself.

- The BLOCK — `.remedy-wt/f032-r10.md`, the committed `.agent/authored/f032-r10.md`
  blob and the committed `.agent/last_block.md` blob all carry sha256
  `bd2560b02c3bfd65c497fcde4ce0811f30013658040703fdfd0f7aa950990a4a` over 27191
  bytes and 332 lines, and the two committed paths are the same git blob
  `a991368a`. Disk-to-disk comparison: EQUAL.
- Slice PLANF032R10 — `.agent/plan.md` at `aace7acb` is byte-equal to the slice
  extracted from the committed C0a blob under convention 2. The negative control
  (trailing newline removed) is False, so the comparison is not vacuous.
- Slice LEDGER10 — `.agent/live_review.md` at `c3bc8bb3` is byte-equal to the
  `0216c5bb` blob plus one newline plus the slice, proven by two independent
  readers, with a one-byte negative control that both readers reject.

No slice was edited. Nothing looked wrong enough to report under constraint 1.

## Deviations & assumptions

- ONE PART OF G1 IS NOT WRITABLE. G1 asks for the `git status --porcelain` line
  count after each of C0a THROUGH C6, but the block's own "Done when" preamble
  puts G1 at commits strictly earlier than C6, and a post-C6 reading cannot exist
  in the file C6 writes. C0a through C5 are reported above, each 0. The post-C6
  reading is reported in this round's session output instead of being invented
  here.
- ONE TEST BEYOND S7'S LIST. C5 also carries
  `test_the_repo_dirty_card_cites_no_branch_no_commit_and_no_count`, which pins
  the second half of S2 — that `branch`, `head_sha` and `changed_file_count` stay
  UNCITED, per amendment A2. S7 orders the tests for what IS emitted; nothing
  ordered a guard over what is deliberately absent, and without one a later round
  could cite a branch name as a `file` ref and no test would notice.
- ONE TYPE ANNOTATION NOT IN THE SPEC. `_mr_refs` is declared as
  `list[DecisionEvidenceRef]` because, unlike the other four producers, its list
  starts EMPTY (all three of its refs are guarded) and an unannotated empty list
  gives the checker nothing to infer from. `python3 -m ruff check` is exit 0
  either way; this is a readability choice, not a fix.
- COMMIT ORDER WAS EXACTLY C0a, C0b, C1, C2, C3, C4, C5, C6, with no commit
  between them, no extra commit and no reordering. C2 is the only commit touching
  `.agent/live_review.md`, and each of C3 and C4 lands one producer's triple
  together with that type's `TRIPLE_REQUIRED_TYPES` entry, per DECISION F032 D5.
- THE SUITE WAS NOT RUN AT C3 OR C4, and no claim is made about its colour there.
  S6's repointed guards and the exact-membership assertion are updated at C5, so
  C3 and C4 are intermediate states of an ordered pair that constraint 7 requires
  to be committed in that order. Every colour reported under G7 was measured at
  C5 or later.
- GATE SCRATCH LIVES IN `.remedy-wt/`. The G2 through G8 measurement scripts were
  written there because it is gitignored; `git ls-files .remedy-wt` is 0 lines and
  the primary checkout is clean at every commit.
- S1 CONFIRMED ON DISK, with one addition worth recording. Everything S1 states
  is true at `0216c5bb`: `apps/cli/commands/repo.py` passes `outcome` as a NAMED
  field of `RunLogWriter.log` and writes `is_git_repo`, `git_available`,
  `branch`, `head_sha`, `dirty`, `changed_file_count` and `status_hash` into
  `metadata`; `_fixture_repo_dirty` writes `metadata` `{"dirty": True}` and
  nothing else; `MemoryEntry.key` defaults to the empty string. The addition:
  branch 6 sits inside `except (ImportError, ValueError, OSError)`, and
  `DecisionEvidenceError` is a `ValueError` subclass — but the emit gate runs
  AFTER that `try` block, at the end of `list_decisions`, so a memory-review
  regression raises out of `list_decisions` and is not swallowed. Mutation (c)'s
  sibling behaviour under G7 confirms the gate fires rather than being caught.

## Next

1. Phase 1 rule 1 of `docs/agents/self_drive_protocol.md`: re-read `.agent/STOP`
   FROM DISK before anything else. It does not exist as of this handback, but the
   check is one-shot per round and binds at any point.
2. The Open PR Gate —
   `gh pr list --state open --json number,headRefName,baseRefName,isDraft`. It
   returned `[]` at this handback; re-run it, do not assume.
3. T002f, the flight-plan approval. Its PENDING arm carries `payload["options"]`
   and its RESOLVED arm carries none, and the emit gate does not branch on
   status, so enforcing that type needs a ruling on what a resolved card owes.
4. T002g, the task decision, whose options come from the escalation record and
   are arbitrary, so its outcomes are built per option rather than written out.
   With it the gate set is complete and T002 ends.
