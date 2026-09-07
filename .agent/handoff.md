# Handback — F274 ROUND 6 — the `context_budget` brain node is cut, and G6 WENT RED

This file supersedes the session-3-end handback. It is written by the delegated worker on the
reviewer's authored block `.agent/authored/f274-r6.md`.

READ THE DEVIATIONS FIRST. Gate G6 ordered a token sweep to ZERO and it MEASURED FIVE. The five
survivors are all in `scripts/remedy_smoke.sh`, a file that is NOT in this round's change set, and
they are not cosmetic: section 12ai of that script imports `NT_CONTEXT_BUDGET` and
`ET_HAS_CONTEXT_BUDGET` from `packages.orchestration.project_brain`, and after C4 that import
raises `ImportError`. The worker did NOT repair it, because repairing it means writing a path the
block does not list. The reviewer rules it.

## Session

SESSION 4 of feature F274 · round 6 · rounds so far 6

Soft limit 25 rounds / 7 sessions: 6 rounds and 4 sessions used. The session opened with
`.agent/STOP` ABSENT and `gh pr list --state open` returning `[]`.

CONTEXT SELF-ASSESSMENT (amend0905-throughput, one sentence): this round consumed a moderate share
of context — one six-commit bundle, three slice applications, a nine-file production cut read
file-by-file before editing, and eleven measured gate runs across two disposable worktrees — and
enough headroom remains for a further delegated round in this session.

## Range

Review of `fcb77eab139faec83ffd88963bd5888d59dad677`..HEAD, where HEAD is C5, the commit that
writes this file. Six commits precede it, every one single-parent, in exactly the block's ordered
sequence C0a, C0b, C1, C2, C3, C4.

## Commits

### 014c2484 F274 R6 C0a: save the round 6 step block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f274-r6.md | +302 / -0 | the block's 27569 bytes saved verbatim by `shutil.copyfile` |

### b107e842 F274 R6 C0b: mirror the round 6 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +271 / -293 | same bytes mirrored; the round 5 block it replaced was longer |

### b43fed17 F274 R6 C1: point the plan at round 6, the context budget node cut
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +15 / -16 | full replacement by the PLAN6 slice |

### f6b6f752 F274 R6 C2: book the round 5 PASS verdict and register R-0832
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +4 / -0 | RECORD6 appended: the round 5 gate entry and finding R-0832 |

### 9f973824 F274 R6 C3: append round 5 reviewer prose slips
| Path | +/- | Reason |
|------|-----|--------|
| .agent/prose_slips.md | +4 / -0 | SLIPS6 appended: two dated lines, no ids |

### 1755b6db F274 R6 C4: cut the context optimizer edge by deleting the context budget brain node
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/project_brain.py | +1 / -32 | two docstring lines, `NT_CONTEXT_BUDGET`, `ET_HAS_CONTEXT_BUDGET`, the order entry 26, the whole `_build_context_budget_node`, its call; `_all_types` EDITED so `NT_DECISION_QUEUE` survives |
| packages/orchestration/brain_detail.py | +0 / -46 | the sorted-import name, the whole `_detail_context_budget`, the dispatch entry |
| packages/orchestration/brain_viewer.py | +1 / -3 | the `_ZONE_MAP` and `_LAYER_MAP` entries; the colour branch EDITED so `context_pack` survives alone |
| packages/orchestration/brain_viewer_theme.py | +0 / -1 | the `LAYER_CLASSES` entry |
| packages/orchestration/ui_view_model.py | +0 / -5 | `_RANK_MAP`, `_ZOOM_MAP`, `_ZONE_MAP`, `_HUMAN_NODE_LABELS` and the `has_context_budget` edge entry |
| packages/orchestration/ui_copy.py | +1 / -2 | the copy tuple; `_DIAGNOSTICS_ONLY` EDITED so `context_coverage` and `context_pack` both survive |
| tests/orchestration/cluster_deletion_map.txt | +0 / -1 | the `context_optimizer <- project_brain.py` edge line, in the SAME commit as the cut |
| tests/orchestration/test_project_brain.py | +0 / -24 | two whole tests deleted; `test_brain_node_type_order` EDITED, its `NT_DECISION_QUEUE` import and both its assertions untouched |
| tests/ui_server/test_brain_view_model.py | +0 / -10 | the whole `test_detail_context_budget` |

### HEAD F274 R6 C5: hand back round 6 (self-reference exception, R-0149 pattern)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | rewrite | this file; a handoff cannot table the commit that writes it |

## External actions

| Command | Outcome |
|---------|---------|
| `gh pr list --state open --json number,headRefName,baseRefName,isDraft` | `[]` — Open PR Gate clear |
| `git worktree add .remedy-wt/r6g4 1755b6db --detach` | created for G4; 14 -> 15 entries |
| `git worktree add .remedy-wt/r6base fcb77eab --detach` | created for the G5 base counts and G7's base lint; 15 -> 16 |
| `git worktree remove --force .remedy-wt/r6g4` | removed |
| `git worktree remove --force .remedy-wt/r6base` | removed |
| `git worktree prune` | ran; `git worktree list` back to 14 entries |
| `git push` | see below |

No PR was created. No branch was created or switched. Nothing was force-pushed.

## Verification

G1 TRANSPORT, at C0b — PASS. `git show b107e842:.agent/authored/f274-r6.md | sha256sum` and
`git show b107e842:.agent/last_block.md | sha256sum` both give
`bd1d2cb8c10835c99c4ae7a0a2fcad4603febe145a30868f4ebe7af881f4b176`, which is the digest the
delegation states, and both blobs are 27569 bytes. One comparison, no chain.

G2 THE RECORD APPEND, at C2, re-derived from the committed blobs — PASS.
(a) 535659 -> 543921 bytes, pre-image a byte-exact PREFIX, post-image equal to pre plus the
8262-byte RECORD6 slice with NO separator added: both clauses True.
(b) unit = a maximal run of consecutive non-empty lines; N counted from the slice itself = 2;
units 215 -> 217; the file's last 2 units equal the slice's 2 units IN ORDER and everything before
them is unchanged: True.
(c) NEGATIVE CONTROL: post-image byte at zero-indexed offset 535660 read as BYTES is `G`, the `G`
that opens `Gate:`; flipped to `g` in memory, reader (a) REJECTS and reader (b) REJECTS. The
primary checkout was never touched.
(d) COUNTS over the post-image: registrations 65 -> 66, resolutions 3 -> 3 BY DISTINCT ID,
OPEN SET 62 -> 63 BY DISTINCT ID, `^Gate: ` 36 -> 37, `^Gate: F274 R5` 0 -> 1,
`^- R-0832 — ` exactly 1.
Note on the resolutions number: `^Done: R-\d+ — ` matches 5 LINES but only 3 DISTINCT IDS, at
both the pre- and the post-image. The block's "3 -> 3" is the distinct-id reading and it holds;
the line reading would have been 5 -> 5. Nothing moved either way.

G3 THE STATE PROSE FILES — PASS.
(a) `.agent/plan.md` at C1 is BYTE-EQUAL to the PLAN6 slice, sha256
`715a57a19adf05d4e08ed0828b8a4dce01aa93d97d2b01624968ebd50de0f7c3`, 2532 bytes, 43 lines against
the cap of 50, and carries both `## Goal` and `## Next Steps`.
(b) `.agent/prose_slips.md` at C3: pre-image a byte-exact PREFIX, post-image pre plus the 555-byte
SLIPS6 slice, 158178 -> 158733 bytes, and each of the two appended lines occurs EXACTLY ONCE.

G4 THE RATCHET, BOTH WAYS, in a disposable worktree at C4 — PASS. `__pycache__` purged (0 found,
the worktree was cold) and every run used `python3 -B`.
(a) CONTROL `python3 -B -m pytest tests/orchestration/test_cluster_deletion_map.py
tests/orchestration/test_import_reachability.py -q` — EXIT 0, `6 passed in 2.60s`.
(b) measured edges 37, recorded edges 37, `measured == recorded` True, APPEARED `[]`,
DISAPPEARED `[]`. Measured consumers of `packages.orchestration.context_optimizer` are `[]` and
recorded consumers are `[]` — THE EMPTY LIST, which is what this round existed for. Modules with
no edge are exactly `['context_optimizer', 'context_pack', 'review_bundle',
'self_repair_proposal']`; 20 of the 24 cluster modules still carry an edge.
(c) RED ONE: appended the deleted line back to `tests/orchestration/cluster_deletion_map.txt`
(4038 -> 4122 bytes). `python3 -B -m pytest tests/orchestration/test_cluster_deletion_map.py -q`
— EXIT 1, `1 failed, 2 passed in 1.42s`, output carries
`DISAPPEARED (1)` and names
`packages.orchestration.context_optimizer <- packages/orchestration/project_brain.py`.
Restored BY EXACT PATH; sha256 back to
`b0501ec816fd3a50a90862c230d6a1da0eed8132796fb21355274d1cdf59f0c3` at 4038 bytes,
byte-identical True.
(d) RED TWO: appended `from packages.orchestration import context_optimizer` to
`packages/orchestration/ui_server.py` (193573 -> 193626 bytes). Same command — EXIT 1,
`1 failed, 2 passed in 1.39s`, output carries `APPEARED (1)` and names
`packages.orchestration.context_optimizer <- packages/orchestration/ui_server.py`. So the map
still SEES that consumer: the cut is a real cut, not a hidden exclusion. Restored BY EXACT PATH;
sha256 back to `c835941781716ffd33ca0a419a03b597df932b240be576dc4902ae22bc618a84` at 193573
bytes, byte-identical True.
(e) The control of (a) returned to EXIT 0, `6 passed in 2.50s`, and
`git -C .remedy-wt/r6g4 status --porcelain` was EMPTY after both restorations.

G5 THE ORDERED COUNTS, run SERIALLY in the primary checkout at C4 — PASS. Base counts were
measured in the `fcb77eab` worktree, not assumed.
(a) MOVED, each falling by exactly the stated amount:
`tests/orchestration/test_project_brain.py` 84 -> 82 (two tests deleted, one edited);
`tests/ui_server/test_brain_view_model.py` 39 -> 38;
`tests/ui_server/` 514 -> 513. All three EXIT 0.
(b) NOT MOVED — each EXIT 0 and each at the SAME count as the base commit:
`test_event_ledger.py` 21 -> 21, `test_token_economy.py` 42 -> 42,
`test_token_cost_policy.py` 11 -> 11, `test_source_apply.py` 34 -> 34.
Together 21+42+11+34 = 108 passed, exactly as the block states.
(c) CANARY `pytest tests/cli/test_golden_path.py -q` — EXIT 0, `42 passed in 21.25s`.

G6 THE SWEEP, at C4 — **RED on the token clause, PASS on the other two.**
Token sweep over `packages/`, `apps/`, `tests/`, `scripts/`, excluding `node_modules`, `dist` and
`__pycache__`, 1313 files scanned. The block ordered a TOTAL OF ZERO. **THE MEASURED TOTAL IS 5.**
Per token at C4: `NT_CONTEXT_BUDGET` 3, `ET_HAS_CONTEXT_BUDGET` 2, `_build_context_budget_node` 0,
`_detail_context_budget` 0, `has_context_budget` 0.
ALL FIVE ARE IN ONE FILE, `scripts/remedy_smoke.sh`, at lines 1942, 1943, 1956, 1963 and 1968.
The same sweep at the base commit totals 30 across six files
(`project_brain.py` 10, `test_project_brain.py` 8, `brain_detail.py` 5, `remedy_smoke.sh` 5,
`ui_view_model.py` 1, `test_brain_view_model.py` 1), so all 25 occurrences the block's change set
covers were removed exactly as specified and the 5 that remain were never in the change set.
The other two clauses of G6 hold:
 - the colour branch in `packages/orchestration/brain_viewer.py` is now
   `if(t==='context_pack')return'var(--remedy-cyan)';` — `context_pack` occurs EXACTLY ONCE on it
   and `context_budget` zero times;
 - all seven DO-NOT-TOUCH files are BYTE-IDENTICAL between `fcb77eab` and C4, read with
   `git show <sha>:<path>` into memory: `token_economy.py`, `token_cost_policy.py`,
   `event_schemas.py`, `worker_registry.py`, `humanizeCatalog.ts`, `actionClass.ts`,
   `context_optimizer_cmd.py`. The primary checkout was never dirtied to read them.

G7 THE LINT CEILING — PASS. `python3 -m ruff check .` run FROM THE WORKTREE'S OWN ROOT in a
disposable worktree checked out at `fcb77eab139faec83ffd88963bd5888d59dad677`: `Found 26 errors.`
The same command in the primary checkout at C4: `Found 26 errors.` DECISION F083 D5's frozen
ceiling is untouched. `python3 -B -m pytest tests/orchestration/test_ci_budgets.py -q` — EXIT 0,
`10 passed in 0.26s`.

G8 THE TREE, at C4 — PASS.
`git status --porcelain` EMPTY. `git ls-files .remedy-wt` EMPTY.
`git worktree list` 14 entries before the first `worktree add` and 14 after the last `prune`.
`git diff --name-only fcb77eab..1755b6db` names exactly 14 paths — the 15 of the change set minus
`.agent/handoff.md`, which C5 writes — and nothing else.
Every commit C0a through C4 is SINGLE-PARENT.
INSERTIONS ONLY, per AGENTS.md DECISION F104 D1: C0a 302, C0b 271, C1 15, C2 4, C3 4, C4 3.
Every one is under the 500 cap; no oversize commit was declared or needed. C4, the cut itself, is
+3 / -124 — the three insertions are the three EDITED lines the block names, one each in
`brain_viewer.py`, `ui_copy.py` and `project_brain.py`. C5's own numbers are deliberately not
quoted here; that commit does not exist while this file is being written.

## Authored-text proofs

| Slice | Bytes | sha256 | Result |
|-------|-------|--------|--------|
| PLAN6 | 2532 | `715a57a1…0de0f7c3` | verified against its BEGIN marker before applying; committed `.agent/plan.md` at C1 is BYTE-EQUAL |
| RECORD6 | 8262 | `beb0acba…4d417f6f` | verified before applying; committed `.agent/live_review.md` at C2 is pre + slice exactly, no separator |
| SLIPS6 | 555 | `16646ff7…077e8c16` | verified before applying; committed `.agent/prose_slips.md` at C3 is pre + slice exactly, no separator |
| whole block | 27569 | `bd1d2cb8…81f4b176` | measured on `.remedy-wt/f274-r6-block.md` BEFORE use, and again on both committed copies |

Every slice was applied byte for byte with a file write of the extracted bytes. Nothing was
reflowed, re-indented or retyped.

## Deviations & assumptions

| Item | Status | Reason |
|------|--------|--------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |
| G1 | done | PASS |
| G2 | done | PASS |
| G3 | done | PASS |
| G4 | done | PASS |
| G5 | done | PASS |
| G6 | **deviated** | token clause RED at 5, not 0 — see D1 below; the other two clauses PASS |
| G7 | done | PASS |
| G8 | done | PASS |

No departure from the block's ordered commit sequence: six commits, C0a through C4 then C5, in
that order, none added, none dropped, none reordered.

**D1 — G6 IS RED, AND THE RESIDUE IS A LIVE BREAKAGE RATHER THAN A DEAD TOKEN.**
`scripts/remedy_smoke.sh` section 12ai ("Brain decision_queue + context_budget nodes", lines
1929-1971) runs an embedded `python3 -c` whose import block reads:

    from packages.orchestration.project_brain import (
        NT_DECISION_QUEUE, NT_CONTEXT_BUDGET,
        ET_HAS_DECISION_QUEUE, ET_HAS_CONTEXT_BUDGET,
        _NODE_TYPE_ORDER, build_project_brain,
    )

Run at C4 that block is EXIT 1 with
`ImportError: cannot import name 'NT_CONTEXT_BUDGET' from 'packages.orchestration.project_brain'`.
So the smoke script is broken by this cut, not merely stale. The worker did NOT repair it: the
block's Change set does not list `scripts/remedy_smoke.sh` and constraint 3 forbids writing any
path outside that list, and the delegation forbids making a gate green by widening it. The
reviewer rules whether this is a new finding, a same-session follow-up commit, or a widening of
the round's change set.

WHY NO GATE CAUGHT IT BEFORE G6. `tests/test_remedy_smoke_script.py` is EXIT 0 at 191 passed at
C4 — it reads the script's structure, not whether each embedded snippet's imports resolve. And
the cluster deletion map cannot see this consumer either: `measured_edges()` walks
`(REPO_ROOT / root).rglob("*.py")`, so a python program embedded in a `.sh` file is invisible to
it even though `scripts` is one of its `CONSUMER_ROOTS`. That is a THIRD blindness shape beside
R-0832's event-name coupling — same class of defect, different syntax — and it means the map may
understate the deletion for every other cluster module too, wherever `remedy_smoke.sh` reaches
one. That question is unmeasured as of this handback.

**D2 — TWO OF THE BLOCK'S MAP NAMES DO NOT MATCH THE MAPS ON DISK; THE SITE SETS ARE STILL
UNAMBIGUOUS AND WERE APPLIED AS SPECIFIED.** The block's C4 section calls the two
`brain_viewer.py` entries "the layer entry and the weight entry"; on disk they are `_ZONE_MAP`
(value `"policy"`) and `_LAYER_MAP` (value `2`), and there is no map named for a weight in that
file. Likewise it calls the two `ui_view_model.py` entries "the two weight maps"; on disk they
are `_RANK_MAP` and `_ZOOM_MAP`. In both files the count and the key are exact — two
`"context_budget"` entries in `brain_viewer.py`, and in `ui_view_model.py` two integer maps plus
the class map (`_ZONE_MAP`), the copy map (`_HUMAN_NODE_LABELS`) and the edge map
(`_EDGE_KIND_MAP`) — so the intended sites were never in doubt. Declared, not repaired; nothing
on disk is wrong because of it.

**D3 — `.agent/plan.md` WAS NOT AMENDED TO CARRY D1's BLOCKER.** AGENTS.md requires the plan to be
current before every commit, and D1 is arguably the next round's first item. The worker left the
plan exactly as the PLAN6 slice wrote it at C1, because the block specifies C5 as a rewrite of
`.agent/handoff.md` alone and constraint 1 forbids improving a slice. Under amend0827 rule 1 this
committed handback is the durable carrier for D1 until the reviewer books it.

No assumption_log entry was needed. No `Done:` paragraph was written anywhere — no finding was
resolved by this round.

## Open findings

63, measured — the G2(d) count over the committed post-image of `.agent/live_review.md` at C2,
by DISTINCT ID: 66 distinct `^- R-\d+ — ` registrations minus 3 distinct `^Done: R-\d+ — `
resolutions. R-0832 is the newest and is open.

## Next

The reviewer re-runs G1 through G8 against this committed diff and rules D1: whether the
`scripts/remedy_smoke.sh` section 12ai breakage is a new finding, a follow-up commit inside this
session, or a widening of round 6's change set — and whether the map's blindness to python
embedded in shell scripts is measured for the other 23 cluster modules before DECISION F260 D3 is
drafted.
