# Handback — F274 round 4 — three of the deletion map's forty-two edges cut

The round split the cluster-bound command handlers out of the two files that hosted BOTH
surviving and cluster-bound commands, so those two files stop being surviving consumers of the
prototype cluster. NOTHING WAS DELETED and no command id changed: the dispatch table is 341
before and 341 after. Round 3's PASS verdict is booked into `.agent/live_review.md` in this
round's C2, under operator amendment amend0827-process-diet rule 1.

THE HEADLINE MEASUREMENT: the deletion map falls from 42 edges to 39, and the number of cluster
modules carrying at least one edge STAYS AT 22 — not 20, as the session-2 handback's round-4
plan predicted. Neither `context_pack` nor `worker_recommend` lost its only consumer, and the
block that ordered this round had already corrected that reason before the work started.

## Session

SESSION 3 of feature F274 · round 4 · rounds so far 4 (soft limit 25) · sessions 3 of 7.

`.agent/STOP` was ABSENT at the start of the round. No pull request was created and nothing was
merged.

## Range

Review of `57d6698bf0af530dedd3d4df4b82cfb17163ba6b`..`<C6>` — eight commits, every one
single-parent, in the block's ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6 with no
departure.

## Commits

### 485e09fa F274 R4 C0a: save the round 4 block as the authored original
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f274-r4.md` | +327/-0 | the reviewer's block, copied by `shutil.copyfile`, never retyped |

### 373bf089 F274 R4 C0b: mirror the round 4 block into the last block slot
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +266/-248 | the same file mirrored by `shutil.copyfile`; the round 3 block it replaces accounts for the deletions |

### 1291aac6 F274 R4 C1: advance the plan to round 4
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +11/-8 | whole-file replacement by PLANF274R4; the plan advances before any substantive commit |

### e90f7419 F274 R4 C2: book the round 3 PASS verdict into the record
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-0 | RECORD4 appended to the end of the append-only findings region |

### b74d3deb F274 R4 C3: record the round 3 prose slips
| Path | +/- | Reason |
|---|---|---|
| `.agent/prose_slips.md` | +8/-0 | SLIPS4 appended; four dated lines, no id spent, nothing gated |

### 684d50d1 F274 R4 C4: split the cluster-bound context handlers into their own files
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/__init__.py` | +3/-1 | both new modules added to the alphabetical import block and to the `for mod in (...)` merge tuple |
| `apps/cli/commands/context.py` | +0/-161 | the three cluster-bound bodies and their three dict entries removed; the module header is UNCHANGED |
| `apps/cli/commands/context_optimizer_cmd.py` | +143/-0 | new: `_cmd_context_explain` and `_cmd_context_optimize`, moved byte-for-byte |
| `apps/cli/commands/context_pack_cmd.py` | +83/-0 | new: `_cmd_context_pack`, moved byte-for-byte |
| `tests/orchestration/cluster_deletion_map.txt` | +0/-2 | the two `<- apps/cli/commands/context.py` edge lines deleted in the commit that cuts them |
| `tests/orchestration/import_reachability_allowlist.txt` | +2/-0 | both new dotted names, list kept sorted |
| `tests/orchestration/test_cluster_deletion_map.py` | +2/-0 | both new paths added to `CLUSTER_COMMAND_HANDLERS`, tuple kept sorted |

### b0923444 F274 R4 C5: split the cluster-bound worker handlers into their own file
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/__init__.py` | +2/-1 | `worker_recommend_cmd` added to both lists |
| `apps/cli/commands/worker.py` | +0/-76 | the two cluster-bound bodies, their two dict entries, and the three imports they alone used |
| `apps/cli/commands/worker_recommend_cmd.py` | +109/-0 | new: `_cmd_worker_recommend` and `_cmd_worker_explain`, moved byte-for-byte |
| `tests/orchestration/cluster_deletion_map.txt` | +0/-1 | the `<- apps/cli/commands/worker.py` edge line deleted in the commit that cuts it |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | the new dotted name, list kept sorted |
| `tests/orchestration/test_cluster_deletion_map.py` | +6/-2 | the new path added to `CLUSTER_COMMAND_HANDLERS`, plus the stale-comment sweep declared as deviation 1 |

### `<C6>` F274 R4 C6: hand back round 4 with its real gate results
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | see the reviewer's own `git diff --numstat` | this file; a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

| Action | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f274-r4-gate b0923444` | created; worktrees 14 → 15 |
| `git worktree remove .remedy-wt/f274-r4-gate` + `git worktree prune` | removed; worktrees 15 → 14 |
| `git worktree add --detach .remedy-wt/f274-r4-base 57d6698b…` | created for the G5 BASE lint reading; worktrees 14 → 15 |
| `git worktree remove .remedy-wt/f274-r4-base` + `git worktree prune` | removed; worktrees 15 → 14 |
| `git worktree add --detach .remedy-wt/f274-r4-g6-base 57d6698b…` (driven from the G6 script) | created for the G6 base table reading; worktrees 14 → 15 |
| `git worktree remove .remedy-wt/f274-r4-g6-base` + `git worktree prune` | removed; worktrees 15 → 14 |
| `git push -u origin feature/f274-one-world-completion-part-two` | see the push line below |
| PR create / merge | NONE. No pull request was created and nothing was merged. |

Worktree count: 14 before the round, 14 after it. `git ls-files .remedy-wt` is empty.

## Verification

One line per gate, each with its REAL exit code and real numbers.

- **G1 TRANSPORT — EXIT 0.** `.remedy-wt/f274-r4-block.md`, `.agent/authored/f274-r4.md` and
  `.agent/last_block.md` are all **28379 bytes** and all hash to
  `88e60a6ee1dd0468158f9eac7182d4cb595bf46ef0697120761fcc522a63cc55`. This chain covers those
  three artefacts and claims nothing about the bytes emitted into the worker's prompt.
- **G2 THE RECORD APPEND — EXIT 0.** Measured across commit `e90f7419` from the COMMITTED blobs.
  (a) BYTE: the pre-image (522330 bytes, `0f9da52e…`) is a byte-exact PREFIX of the post-image
  (528978 bytes, `6b8723e5…`), and post == pre + RECORD4 (6648 bytes, `087390b1…`) exactly,
  522330 + 6648 = 528978, with no separator newline added; the committed post-image equals the
  working-tree file. (b) STRUCTURAL — UNIT DEFINITION STATED: a UNIT is a maximal run of
  consecutive NON-EMPTY lines of `text.split("\n")`; empty lines are separators and belong to no
  unit, so a leading or trailing newline contributes no unit of its own. N counted FROM THE SLICE
  = 1; units 213 → 214; the last 1 unit of the post-image equals RECORD4's 1 paragraph and every
  earlier unit is unchanged. (c) NEGATIVE CONTROL: the append begins at byte 522330 and the FIRST
  appended paragraph at 522331 (RECORD4 carries its own leading newline); byte 522381 was flipped
  from `P` to `Q` and BOTH readers rejected the result; the file on disk is unchanged, sha256
  `6b8723e549c3bcfd44cb673a2368a1caa238b7886593a2f1f0031d68afa21dbf` before and after. The
  control was run on an IN-MEMORY copy — see deviation 3. (d) COUNTS across the commit: distinct
  registrations 65 → 65, distinct resolutions 3 → 3, **OPEN SET BY DISTINCT ID 62 → 62**,
  `^Gate: ` 34 → 35, `^Gate: F274 R3` 0 → 1. The base figures the block asserted — open set 62,
  65 registrations, 3 resolutions, `^Gate: ` 34 — all reproduced.
- **G3 THE PLAN — EXIT 0.** `.agent/plan.md` is byte-equal to PLANF274R4 (2377 bytes, both
  `99e79842…`), **43 lines against the cap of 50**, and carries both `## Goal` and `## Next Steps`.
- **G4 THE EDGE CUT AND THE RATCHET BOTH WAYS — EXIT 0**, entirely inside the disposable
  worktree `.remedy-wt/f274-r4-gate` at `b0923444`, every pytest run with `python3 -B` after a
  `__pycache__` purge, every mutation restored BY EXACT PATH and byte-verified.
  (a) UNMUTATED CONTROL, both suites in ONE command:
  `python3 -B -m pytest tests/orchestration/test_cluster_deletion_map.py tests/orchestration/test_import_reachability.py -q`
  → **exit 0, 6 passed** — which is what proves the map test's reuse import of the reachability
  walker resolves under collection.
  (b) **measured edges 39, recorded edges 39, EQUAL**; cluster modules carrying at least one edge
  **22**. (The map was 42 edges over 22 modules at the base; three edges are gone, the module
  count is unchanged.)
  (c) RED, MAP: the three cut edge lines appended back → **exit 1, `DISAPPEARED (3)`**, naming
  `context_optimizer <- apps/cli/commands/context.py`,
  `context_pack <- apps/cli/commands/context.py` and
  `worker_recommend <- apps/cli/commands/worker.py`; after restoring
  `tests/orchestration/cluster_deletion_map.txt` by exact path (bytes match) → **exit 0, 3 passed**.
  (d) RED, HANDLERS: the exact bytes `    "apps/cli/commands/worker_recommend_cmd.py",\n` occur
  **exactly 1** time in `tests/orchestration/test_cluster_deletion_map.py`; removing that one
  occurrence → **exit 1, `APPEARED (1)`**, naming
  `worker_recommend <- apps/cli/commands/worker_recommend_cmd.py`; restored by exact path (bytes
  match) → **exit 0, 3 passed**.
  (e) RED, ALLOWLIST: the three added dotted names removed →
  `tests/orchestration/test_import_reachability.py` **exit 1**, naming
  `apps.cli.commands.context_pack_cmd` among the newly unallowed reachable modules; restored by
  exact path (bytes match) → **exit 0, 3 passed**.
  `git status --porcelain` inside the worktree was EMPTY after every restore.
- **G5 THE LINT CEILING AND THE BUDGETS — EXIT 0.** BASE reading, mechanism stated: `python3 -m
  ruff check .` run with cwd set to the disposable worktree `.remedy-wt/f274-r4-base` checked out
  at `57d6698bf0af530dedd3d4df4b82cfb17163ba6b`, so that worktree's own `pyproject.toml` and its
  `per-file-ignores` resolve against the same paths the command walks; nothing in the primary
  checkout was overwritten to obtain it → **Found 26 errors** (ruff's own exit 1, which is what
  26 outstanding errors means). HEAD reading, mechanism stated: the same command with cwd set to
  the primary checkout at C5 → **Found 26 errors**. **BOTH 26** — the ceiling DECISION F083 D5
  freezes is untouched, and `ruff --fix` was never run.
  `python3 -m pytest tests/orchestration/test_ci_budgets.py -q` → **exit 0, 10 passed**.
- **G6 THE DISPATCH TABLE IS INTACT — EXIT 0.** Read through the SHIPPED reader
  `apps.cli.commands.collect_all_handlers`, not a re-implementation: **341 → 341**, the base
  figure MEASURED in a disposable worktree at `57d6698b` rather than quoted from the block. All
  eight ids present at HEAD: `context.pack`, `context.explain`, `context.optimize`,
  `context.inspect`, `worker.recommend`, `worker.explain`, `worker.list`, `worker.status`.
- **G7 THE SUITES — EXIT 0 for all ten**, run SERIALLY in the PRIMARY checkout, the four state
  readers as FOUR separate commands per constraint 9:
  `test_cluster_deletion_map.py` exit 0 / 3 passed · `test_import_reachability.py` exit 0 /
  3 passed · `test_command_discovery.py` exit 0 / 17 passed · `tests/cli/test_context_inspect_cli.py`
  exit 0 / 13 passed · `tests/storage/test_persistence.py` exit 0 / 26 passed ·
  `tests/ui_server/` exit 0 / 515 passed · `test_test_runner.py` exit 0 / 52 passed ·
  `tests/regression/test_resource_safety.py` exit 0 / 21 passed · `test_integrity_gate.py`
  exit 0 / 16 passed · canary `tests/cli/test_golden_path.py` exit 0 / 42 passed. RED SUITES: none.
- **G8 THE TREE AND THE COMMITS — EXIT 0.** `git status --porcelain` was EMPTY at every commit
  boundary and is empty now; `git ls-files .remedy-wt` is empty; `git worktree list` 14 before
  and 14 after (three add/remove pairs in between, each returning to 14).
  `git diff --name-only 57d6698bf0af530dedd3d4df4b82cfb17163ba6b` over the round names exactly
  **15 paths** — the fourteen measured through C5 plus `.agent/handoff.md` staged for C6 — every
  one in the block's change set and **nothing outside it**. Per-commit insertions against the
  DECISION F104 D1 cap of 500 (the `+` column only): C0a **+327**, C0b **+266**, C1 **+11**,
  C2 **+2**, C3 **+8**, C4 **+233**, C5 **+118**. All under the cap; no oversize commit, declared
  or otherwise. Every commit single-parent.

## Authored-text proofs

Disk-to-disk against the COMMITTED `.agent/authored/f274-r4.md` (the in-session replacement for
the hash-stamp ritual), re-extracting each text by its `<<<BEGIN <NAME> ` / `<<<END <NAME>>>`
marker lines rather than by hand:

| Text | Target | Result |
|---|---|---|
| PLANF274R4 (2377 B, `99e79842…`) | `.agent/plan.md` | whole-file EQUAL |
| RECORD4 (6648 B, `087390b1…`) | `.agent/live_review.md` | appended region EQUAL; post == pre + slice |
| SLIPS4 (2007 B, `f63c9548…`) | `.agent/prose_slips.md` | appended region EQUAL; post == pre + slice |

All three were extracted programmatically from the block file; none was hand-typed. The block
itself was received at 28379 bytes / `88e60a6e…`, matching the length and digest the work order
stated, before any work began.

## Deviations & assumptions

THE BLOCK'S ORDERED COMMIT SEQUENCE WAS FOLLOWED EXACTLY — C0a, C0b, C1, C2, C3, C4, C5, C6 —
with no extra commit, no dropped commit and no reordering.

1. **An edit the SPEC did not order: the stale comment above `CLUSTER_COMMAND_HANDLERS`**
   (`tests/orchestration/test_cluster_deletion_map.py`, landed in C5). The block's wiring SPEC
   ordered only that each new module's path be added to that tuple. The comment directly above it
   read "`apps/cli/commands/worker.py` and `apps/cli/commands/context.py` host surviving commands
   alongside cluster ones and must stay measurable" — a sentence THIS ROUND MAKES FALSE, since
   after C4 and C5 neither file hosts a cluster command any more. The path is inside the block's
   change set, and leaving a false statement beside the tuple it exists to explain would land a
   staleness defect in a file whose whole purpose is to stop the plan going quietly stale. The
   comment now says the two files keep only SURVIVING commands, are deliberately NOT listed, and
   names the three files F274 round 4 moved the cluster-bound handlers into. The WHY and the
   "never matched by filename pattern" rule are unchanged. Nothing executable changed.
2. **One byte more than "the whole of the line" in `worker.py`.** The SPEC ordered the removal of
   the WHOLE of `from uuid import UUID` and the WHOLE of
   `from packages.orchestration.storage import JobNotFoundError, load_job`. The storage import was
   its own import GROUP, preceded by a blank line; removing only the line itself would have left
   that blank line orphaned beside the one the group already had, giving a stray double blank
   between the import block and `if TYPE_CHECKING:`. The storage line was therefore removed
   together with its preceding blank line. The resulting header is
   `__future__` / `json as _json` / `sys` / `Callable` / `TYPE_CHECKING`, blank,
   `if TYPE_CHECKING:` — and `python3 -m ruff check .` reads 26, not 29, so the ceiling holds and
   no `F401` was left behind. Verified mechanically, not by eye: the strings `UUID`,
   `JobNotFoundError` and `load_job` occur ZERO times in `worker.py` after the split, while
   `_json`, `sys`, `Callable`, `TYPE_CHECKING` and `argparse` all remain in use.
3. **G2(c)'s negative control was run on an IN-MEMORY copy of the post-image**, not by writing a
   mutated file into the primary checkout and restoring it. Constraint 8 confines destructive
   verification to a disposable worktree, and the gate itself requires the disk file to be
   unchanged; mutating in memory satisfies both without weakening the control. Both readers still
   reject the flipped image, and the disk file's sha256 is reported identical before and after.
4. **Every gate was re-expressed as a Python script under `.remedy-wt/`, run with `python3 -B`.**
   This session's shell guard REFUSES, by FORM, shell loops, `$(...)` command substitution and
   `$?` inside a compound command — the first attempt at G1 was rejected for the `$?` alone. The
   gates' CONTENT is unchanged; only the driver is Python. Scripts:
   `f274_r4_extract.py` (text extraction), `f274_r4_g1.py`, `f274_r4_g2.py`, `f274_r4_g3.py`,
   `f274_r4_g4.py`, `f274_r4_g5.py`, `f274_r4_g6.py`, `f274_r4_g7.py`, `f274_r4_g8.py`,
   `f274_r4_c4_build.py`, `f274_r4_c5_build.py`, `f274_r4_textproof.py`. All live under the
   gitignored `.remedy-wt/`; `git ls-files .remedy-wt` is empty.
5. **G6's base figure was MEASURED, not quoted.** The block states the base table size as 341.
   Rather than assert it, the gate created a third disposable worktree at
   `57d6698bf0af530dedd3d4df4b82cfb17163ba6b`, ran the shipped reader there, removed the worktree
   and pruned. That is one worktree add/remove pair the block did not explicitly order; it is
   reported in External actions and the count returns to 14.
6. **The moves were proved byte-for-byte BEFORE anything was written.** Both build scripts assert
   that each moved function body and each moved dict entry appears verbatim in its new file and no
   longer appears in the old one, and abort before writing if either fails. Byte lengths of the
   moved units: `_cmd_context_pack` 1361, `_cmd_context_explain` 1532, `_cmd_context_optimize`
   2024, `_cmd_worker_recommend` 980, `_cmd_worker_explain` 1514; dict entries 211, 236, 191, 96
   and 92. This is not a departure from the block, but it is the mechanism by which "the move is
   byte-for-byte" was made checkable rather than asserted.

NO ASSUMPTION WAS MADE ABOUT THE GUARDS THE BLOCK DESCRIBED. `test_no_shell_true` over
`worker.py`, `test_context_inspect_in_handlers` over the context table, and every other test
naming either module were RUN, not read: `test_command_discovery.py` 17 passed,
`tests/cli/test_context_inspect_cli.py` 13 passed, `tests/storage/test_persistence.py` 26 passed.

NO `Done:` PARAGRAPH WAS WRITTEN and no finding was resolved by the worker. Nothing landed this
round that a reviewer's authored resolution is owed for, so there is no `Landed:` line either.

## Open findings

**62 open by distinct id** — unchanged across the round (65 distinct registrations against 3
distinct resolutions). The four open High findings remain R-0803, R-0804, R-0806 and R-0807, all
F273's rather than this feature's, per DECISION F272 D12. R-0830 and R-0831 both stay open.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a  | done   | |
| C0b  | done   | |
| C1   | done   | |
| C2   | done   | |
| C3   | done   | |
| C4   | done   | |
| C5   | deviated | carries deviations 1 and 2: the stale-comment sweep in `test_cluster_deletion_map.py`, and the blank line removed with the dead storage import in `worker.py` |
| C6   | done   | this file |

| Gate | Status | Exit |
|------|--------|------|
| G1 TRANSPORT | done | 0 |
| G2 THE RECORD APPEND | done | 0 |
| G3 THE PLAN | done | 0 |
| G4 THE EDGE CUT AND THE RATCHET | done | 0 |
| G5 THE LINT CEILING AND THE BUDGETS | done | 0 |
| G6 THE DISPATCH TABLE | done | 0 |
| G7 THE SUITES | done | 0 (all ten) |
| G8 THE TREE AND THE COMMITS | done | 0 |

No gate went red at any point, and no gate was worked around.

## Next

The reviewer reads `git diff 57d6698bf0af530dedd3d4df4b82cfb17163ba6b..HEAD` bottom-up and
re-runs G1 through G8 itself, then issues a verdict for round 4. Before AUTHORING round 5 it
re-reads `.agent/STOP` from disk (Phase 1 rule 1 before rule 2). Round 5's natural work is the
next group of edge cuts the map records: 39 edges remain over 22 cluster modules, and
`review_bundle` and `self_repair_proposal` still carry none at all.
