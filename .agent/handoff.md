# Handoff — F276 Data-root hygiene & disk budget · Round 3

## Session

SESSION 1 of feature F276 · round 3 · rounds so far 3

Context self-assessment: the worker read the step block and verified its sha256 before anything else, then AGENTS.md in full, `docs/agents/handback_template.md`, `docs/roadmap/features/T2_F276.md`, the `decisions.md` payload (DECISION F276 D4, which rules where the block is terser), the `ledger.md` payload carrying R-1002 and the whole 869-line code diff before applying a single slice of it, and held all of it without loss; every numeral below is the output of a command run in this round, not a recollection.

## Range

Review of 94441e34..HEAD — branch `feature/f276-data-root-hygiene`.

## Summary

Round 3 books round 2's verdict, registers R-1002 and repairs it.
- C1 books round 2's PASS over the seven commits of `96fd8f9c`..`94441e34`, registers R-1002 from the reviewer's own measurement of the operator's data root, appends DECISION F276 D4 and rewrites the plan to this round; the four reviewer payloads are saved byte-exact under `.agent/authored/`.
- C2 lands the orphan rule: `data reclaim --orphans`, off by default, with the `ORPHAN_MIN_AGE_DAYS` floor, the `orphan_too_young` refusal, the `no_record` machine-shape mark, the deletion-time re-verdict and the default human discoverability line.
- C3 adds the orphan behaviour tests; C4 adds the architecture section and the feature-file amendment.
- C5 is this handoff. No pull request was opened.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | |
| C2 the orphan rule | done | |
| C3 the orphan behaviour tests | done | |
| C4 the docs | done | |
| C5 handoff | done | |
| G1 transport + state | done | 11 readings, every one True |
| G2 code transport | done | four object ids as ordered; seven paths and no other |
| G3 targeted suite | done | `904 passed in 168.53s`, exit 0, 0 failed |
| G4 ruff | done | `All checks passed!`, exit 0 |
| G5 mutation red-proofs | done | control green; all three mutations red; none stayed green |
| G6 push + clean tree | done | reported in the round report; it follows this commit |

R-1002 is not an ordered bundle item and deliberately has no row here: its repair LANDED this round (see below), and only the reviewer's own authored text resolves a finding.

## Commits

### 5a78b0fa F276 R3 C1: the round 3 bookkeeping

| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f276-r3-block.md | 98/0 | byte copy of the step block |
| .agent/authored/f276-r3-decisions.md | 45/0 | byte copy of the D4 payload |
| .agent/authored/f276-r3-ledger.md | 4/0 | byte copy of the ledger payload |
| .agent/authored/f276-r3-plan.md | 31/0 | byte copy of the plan payload |
| .agent/decisions.md | 45/0 | `94441e34` bytes + the D4 payload |
| .agent/live_review.md | 4/0 | `94441e34` bytes + the ledger payload: round 2's PASS and R-1002 |
| .agent/plan.md | 5/5 | rewritten to the plan payload |

Insertions 232.

### 3a54f32c F276 R3 C2: the orphan rule

| Path | +/- | Reason |
|------|-----|--------|
| apps/cli/command_catalog.py | 7/0 | `--orphans` declared `is_flag` |
| apps/cli/commands/data_cmd.py | 38/5 | the flag threaded through, the split totals, the default hint |
| packages/orchestration/data_reclaim.py | 146/14 | the orphan rule, the floor, the deletion-time re-verdict |
| tests/cli/test_data_cmd.py | 20/0 | the flag parse and its composition |

Insertions 211.

### f09b3773 F276 R3 C3: the orphan behaviour tests

| Path | +/- | Reason |
|------|-----|--------|
| tests/orchestration/test_data_reclaim.py | 349/0 | the default-JSON byte identity, every narrowing, both re-verdict branches, the hint's three states |

Insertions 349.

### 8e99225e F276 R3 C4: the docs

| Path | +/- | Reason |
|------|-----|--------|
| docs/roadmap/features/T2_F276.md | 30/0 | the round 3 amendment to T002 |
| docs/system/architecture.md | 33/1 | the orphans section and the command's flag list |

Insertions 63.

### C5 — this handoff

`.agent/handoff.md` alone. A handoff cannot table the commit that writes it (R-0149 pattern).

Every commit is under the 500-insertion cap of AGENTS.md Commit Discipline; none was declared oversize.

## External actions

- `git worktree add --detach /home/decodeux/Repos/remedy/.remedy-wt/f276-r3-wt 8e99225e` — exit 0, created for G5 only.
- `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f276-r3-wt` — exit 0, as G5's last action. `git worktree list` afterwards shows the primary checkout and the operator's `job-468c8e62a2cc4fac` and nothing else.
- `git push origin feature/f276-data-root-hygiene` — reported in the round report; it follows this commit.
- No pull request created, edited or merged. No branch created or deleted. No `gh` command run.

## Verification

- G1 transport + state — `python3 -B .remedy-wt/f276-r3/g1.py` → exit 0. Four payload digests True, four `.agent/authored/f276-r3-*` copies equal their payload True, `.agent/live_review.md` == `94441e34` bytes + ledger.md True, `.agent/decisions.md` == `94441e34` bytes + decisions.md True, `.agent/plan.md` == plan.md True. `ALL 11 READINGS TRUE: True`. Saved block 98 lines sha256 `61ded6c52ea942c8281f6ea148a94c11e6840075c1de476ea2f623396ed92bdb`; source block 98 lines, same sha256.
- G2 code transport — `git rev-parse 8e99225e:packages 8e99225e:apps 8e99225e:tests 8e99225e:docs` → exit 0, `bdb14143c4f4af92a38e114060b0feca88157bb4`, `c6512f5298473ca4de84e8c8dbb811283c8e0f60`, `73d3a71f1212275906c453ff300655e00d39636d`, `32845b649f7f57e021f598ccd60d87aaaa52530b` — the four objects the block ordered. `git diff --name-only 5a78b0fa 8e99225e` → exit 0, exactly 7 paths: `apps/cli/command_catalog.py`, `apps/cli/commands/data_cmd.py`, `docs/roadmap/features/T2_F276.md`, `docs/system/architecture.md`, `packages/orchestration/data_reclaim.py`, `tests/cli/test_data_cmd.py`, `tests/orchestration/test_data_reclaim.py`.
- G3 targeted suite — the block's fifteen paths, serial, no `-n`, in the primary checkout → `904 passed in 168.53s (0:02:48)`, exit 0, 0 failed.
- G4 ruff — `python3 -m ruff check packages/orchestration/data_reclaim.py apps/cli/commands/data_cmd.py apps/cli/command_catalog.py tests/orchestration/test_data_reclaim.py tests/cli/test_data_cmd.py` → `All checks passed!`, exit 0.
- G5 mutation red-proofs — in the disposable worktree at `8e99225e`; imported `packages.orchestration.data_reclaim` resolved to `/home/decodeux/Repos/remedy/.remedy-wt/f276-r3-wt/packages/orchestration/data_reclaim.py`, so no editable install shadowed it. Control `42 passed in 1.59s`, exit 0. (a) `ORPHAN_MIN_AGE_DAYS: float = 1.0` → `0.0`, 1 occurrence: exit 1, `4 failed, 38 passed`, FAILED `test_a_young_orphan_is_refused_as_orphan_too_young_even_with_the_flag`, `test_orphans_apply_deletes_exactly_the_previewed_orphans_and_a_second_run_is_a_noop`, `test_the_orphan_json_shape`, `test_an_orphan_freshened_between_the_plan_and_the_apply_is_refused_as_too_young`. (b) the two `_orphan_deletion_refusal` lines in `apply_reclaim` deleted, 1 occurrence: exit 1, `2 failed, 40 passed`, FAILED `test_a_record_that_appears_between_the_plan_and_the_apply_saves_the_orphan`, `test_an_orphan_freshened_between_the_plan_and_the_apply_is_refused_as_too_young`. (c) `    if not orphans:` → `    if False and not orphans:`, 1 occurrence: exit 1, `1 failed, 41 passed`, FAILED `test_the_default_human_preview_names_the_unresolved_bytes_and_the_flag`. No mutation stayed green. Both files restored byte-identically — `data_reclaim.py` `ca7bdc9190e20e3e69e3119d9745b2ad416670b3bc3b60ef67665b84fab9c5c4`, `data_cmd.py` `b16f4611fef56943faa47d504ce7e9f144f649473016d0761fb2c31a3e1b598a`, both matching their pre-mutation readings — and the worktree's `git status --porcelain` was empty before removal.
- G6 push + clean tree — follows this commit; reported in the round report.
- Per-commit greens (constraint 7): C2 alone `113 passed in 92.44s` exit 0 over the reclaim, data-cmd, catalog and class tests; C3 alone `42 passed in 85.87s` exit 0; C4 alone `344 passed in 84.39s` exit 0 over `tests/docs` and `tests/orchestration/test_roadmap_index.py`.
- Full suite: NOT run, per the block (amend0917-throughput rule 1).

## Open findings

15 by `scripts/rotate_live_review.py::count_open_findings` and 15 by distinct id, measured on `.agent/live_review.md` as committed at `8e99225e`: R-0499, R-0622, R-0662, R-0819, R-0820, R-0829, R-0866, R-0880, R-0892, R-0950, R-0984, R-0998, R-0999, R-1000, R-1002. Round 2 left 14 by both readings; R-1002 is this round's registration and is the one open High.

Landed: R-1002 — the `--orphans` repair landed at `3a54f32c` (rule), `f09b3773` (tests) and `8e99225e` (docs). The finding stays OPEN: only the reviewer's own authored text resolves a finding, and no `Done:` paragraph was written anywhere this round.

## Authored-text proofs

All four reviewer payloads were copied with `shutil.copyfile` and never retyped. Disk-to-disk byte comparison against the committed `.agent/authored/` copy, all True (G1): `f276-r3-block.md` `61ded6c52ea942c8281f6ea148a94c11e6840075c1de476ea2f623396ed92bdb` (98 lines), `f276-r3-ledger.md` `29e0041a0a7eed721c239650df59d9a8a2be1165cbf8edc614d2b6f4b978eda9` (4 lines), `f276-r3-decisions.md` `ccf099d74a1f27f376711276367aeec7715f619c019120f9857765ca460e70f8` (45 lines), `f276-r3-plan.md` `bd1dffe01d515b4708906774f6b60db231166ccb38968876a8bfd18e88f0e8fc` (31 lines). The code diff `f276-r3.diff` verified at `f73bcd11fbcb3ab9072bb98608d6c8aa558ce51677d725a158dacbb9fdc95b93` before the first `git apply`, and applied in three disjoint `--include` slices, never whole and never edited.

## Deviations & assumptions

- No departure from the block's ordered commit sequence: C1 to C5 in order, one commit each, none added, none dropped, none reordered.
- The `__pycache__` purge before every G5 run reported `purged 0 __pycache__ dirs` on all four runs. That is not a purge that failed: `python3 -B` writes no bytecode and `-p no:cacheprovider` writes no pytest cache, so there was nothing to remove. The purge ran and found the worktree already clean.
- G5's `-rf` short summary is the source of every FAILED node id quoted above; no node id was inferred from a test name.
- `.agent/STOP` was checked from disk before the handoff and does not exist.
- The operator's `.data/` was never read, listed or written. Every test and probe used a tmp root through the suite's own `root` fixture; no `REMEDY_DATA_DIR` was ever set as a shell assignment.
- Nothing under `.remedy-wt/` entered a commit; it is gitignored scratch.

## Next

1. Phase 1 rule 1 of `docs/agents/self_drive_protocol.md` — re-read `.agent/STOP` from disk; if it exists, write the handoff and end the session, doing nothing else.
2. The review of round 3: re-run G1 to G6 independently and read `git diff 94441e34..HEAD` bottom-up, then book the verdict and R-1002's resolution in the reviewer's own authored text.
3. T003 — the copy-mode lifecycle: `release_staging_workspace(job_id)` on the terminal-state hook, a `.gitignore`-aware copy filter and a per-file size ceiling, with the release call's removal as the red proof.

Operator questions open: 5
