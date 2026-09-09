# Handback — F275 round 13

## Session

SESSION 7 of feature F275 · round 13 · rounds so far 13

Soft limit, operator amendment amend0908-f275-finish: 20 sessions and 60 rounds, by name for
F275. At 7 sessions and 13 rounds the feature is well inside it, so no scope report is owed.

CONTEXT SELF-ASSESSMENT, as amend0905-throughput requires in one sentence: context is
comfortable — this round read three authority files, one work order and eight edited or deleted
targets, ran every gate once, and never needed to re-read a file it had already measured, so the
session can carry further rounds without a boundary.

## Range

Review of `053a25a7`..`04ca209c` for the gated work, plus this handback commit.

## Commits

### 3a9ebc38 F275 R13 C0a: save the round 13 block verbatim.
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f275-r13.md | 232/0 | the work order saved by `shutil.copyfile`, never retyped |

### ca833831 F275 R13 C0b: mirror the round 13 block to last_block.
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 150/238 | the same bytes mirrored, over the round 12 block |

### a991c91c F275 R13 C1: advance the plan to round 13.
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 16/18 | replaced WHOLE by the PLAN13 slice, per constraint 5 and §3 item 23 |

### 8a688931 F275 R13 C2: book the round 12 PASS, note R-0843, register R-0852.
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 6/0 | LEDGER13 appended: the round 12 PASS, the R-0843 note, R-0852 |
| .agent/prose_slips.md | 2/0 | SLIPS13 appended: one dated line |

### 04ca209c F275 R13 C3: delete the external builder sandbox module group whole.
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/external_builder_sandbox.py | 0/560 | the eighth module group, deleted whole |
| apps/cli/commands/external_builder_cmd.py | 0/161 | the handler file dies WITH it — all seven surviving handlers drove the sandbox |
| tests/orchestration/test_external_builder_sandbox.py | 0/269 | the module's test file |
| tests/cli/test_external_builder_cli.py | 0/153 | the handler's test file |
| docs/system/external-builder-sandbox-v0.md | 0/70 | describes the deleted store |
| docs/system/external-builder-worker-contract-v0.md | 0/94 | describes an ingress contract no command can now receive |
| apps/cli/command_catalog.py | 0/82 | the seven `CommandEntry` blocks with their section comment, plus the `external-builder` `GroupDef` line |
| apps/cli/commands/__init__.py | 1/2 | the `external_builder_cmd` import and its name in the `for mod in (…)` tuple |
| docs/README.md | 0/4 | two quick-find rows and two index rows, keyed on the LINK TARGET |
| docs/archive/external-builder-sandbox-future.md | 1/1 | its DEPRECATED banner claimed a built page this round deleted |
| tests/orchestration/import_reachability_allowlist.txt | 0/2 | the module and its handler |
| tests/orchestration/test_cluster_deletion_map.py | 0/2 | the `CLUSTER_MODULES` row and the handler-path row |
| .agent/f275_deletion_order.md | 0/1 | REGENERATED from `measured_order()`; eight components become seven |

Commit shape: 13 paths, 2 insertions against 1401 deletions, exactly the shape constraint 8 states.

### 04ca209c → this handback commit
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C4, this file; a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

| Command | Outcome |
|---|---|
| `gh pr list --state open --json number,headRefName,baseRefName,isDraft` | `[]` — no open PR, Open PR Gate clear |
| `git worktree add --detach .remedy-wt/base13 053a25a7` | created, for the base-side readings of G6 and G7 only |
| `git worktree remove --force .remedy-wt/base13` + `git worktree prune` | removed; `git worktree list` names the primary checkout alone |
| `git push -u origin feature/f275-one-world-completion-part-three` | run ONCE, after this commit |

No PR created, nothing merged: the PR belongs to this feature's closure sequence.

## Verification

Every gate was RUN and its exit code read from the process object, never through a pipe and
never inferred.

| Gate | Exit | What it measured |
|---|---|---|
| G1 TRANSPORT | 0 | delegation source, C0a blob and C0b blob all 27171 bytes at `5b3ad1d125cdb0bf55a47e73c601b0cf005d087aa73b1bcaaf32324123df5010`; all three compare BYTE-EQUAL |
| G2 THE PLAN | 0 | `.agent/plan.md` at C1 byte-identical to PLAN13: 2697 bytes, `ab13e2491c8f3792114e818bc14ad63bf87f5c0cb514c625d30448e9b27d00bf`, 45 lines against the AGENTS.md cap of 50 |
| G3 THE RECORD | 0 | all five parts, from the COMMITTED blobs at C1 and C2 — see below |
| G4 THE DELETION IS COMPLETE | 0 | 6 paths absent from the C3 tree (4578 tracked files); sweep run TWICE over 1695 tracked files outside `.agent/` and `.data/` |
| G5 THE FOUR MEASUREMENTS | 0 | ratchets 442 passed; shipped readers 276→269 / 276→269 / 51→50; order file 8→7; canary 42 passed |
| G6 RUFF AND BASH | 0 | `All checks passed!` over the 3 surviving changed `.py` files; `Found 26 errors.` at BOTH tip and base; `bash -n` exit 0 |
| G7 THE FULL SUITE | 0 | 18896 passed, 23 skipped, ZERO failed, SERIALLY in the primary checkout; fall of 39 by the id set with 0 gained |
| G8 THE TREE | 0 | STOP absent, porcelain empty, ONE worktree, branch correct, EXACT 13-path set match, every commit single-parent under 500 insertions |

### G1 — transport
    delegation source    27171  5b3ad1d125cdb0bf55a47e73c601b0cf005d087aa73b1bcaaf32324123df5010
    C0a blob             27171  5b3ad1d125cdb0bf55a47e73c601b0cf005d087aa73b1bcaaf32324123df5010
    C0b blob             27171  5b3ad1d125cdb0bf55a47e73c601b0cf005d087aa73b1bcaaf32324123df5010
    all three compare equal: True

The three delegated values were verified against the file on disk BEFORE any commit: 27171
bytes, sha256 as above, 232 lines. All three agreed.

### Slice transport, verified BEFORE use

| Slice | Bytes | sha256 | N counted from the slice |
|---|---|---|---|
| PLAN13 | 2697 | `ab13e2491c8f3792114e818bc14ad63bf87f5c0cb514c625d30448e9b27d00bf` | whole-file replacement, 45 lines |
| LEDGER13 | 10675 | `80ae6e94f6b621a472f08503caf05033c449085526964ae5d7d80040d3246d8f` | 3 |
| SLIPS13 | 602 | `429570a0ce6e766cc78faab68ad8fea7a64ecd70048eef13eb452ce16b73376e` | 1 |

Each slice is the bytes STRICTLY BETWEEN its `BEGIN-<NAME>` line and its `END-<NAME>` line; no
marker line landed in any target file. SLIPS13's N was COUNTED from the slice by the reader, not
assumed: it is 1.

### G3 — the record, from the committed blobs at C1 (pre) and C2 (post)

(a) THE BYTE ARITHMETIC.

    .agent/live_review.md   pre 597513  post 608189  growth 10676 == 1 + 10675
    .agent/prose_slips.md   pre 182696  post 183299  growth   603 == 1 +   602
    prefix exact: True   suffix exact: True   joining byte re-read: b'\n'   (both files)

(b) ORDERED UNIT EQUALITY, N counted by the reader from each slice.

    .agent/live_review.md  N = 3
      unit 1  file fec669926018e3375d204ccc  slice fec669926018e3375d204ccc  equal  5000 bytes
      unit 2  file 3ded4de87c8cfc5563c9bb9b  slice 3ded4de87c8cfc5563c9bb9b  equal  2312 bytes
      unit 3  file a7b0f5532d6f0789f5572abc  slice a7b0f5532d6f0789f5572abc  equal  3358 bytes
    .agent/prose_slips.md  N = 1
      unit 1  file 40a95d77142a733c79d437eb  slice 40a95d77142a733c79d437eb  equal   601 bytes

(c) NEGATIVE CONTROL — one byte flipped IN MEMORY inside the FIRST appended paragraph of each
file, per §3 item 36. BOTH readers rejected BOTH flips.

    .agent/live_review.md  offset 600014  b'`' -> b'@'   byte reader REJECTS: True   paragraph reader REJECTS: True
    .agent/prose_slips.md  offset 182997  b'e' -> b'E'   byte reader REJECTS: True   paragraph reader REJECTS: True

Both tracked files were then RE-READ FROM DISK and compare byte-equal to their committed
post-blobs: live_review 608189 bytes, prose_slips 183299 bytes. The flip existed only in memory.

(d) THE COUNT GATES.

    ^Gate:            34 -> 35   (block says 34 -> 35)   MATCH
    ^Gate: F275 R12   exactly 1  MATCH
    ^Note: F275 R13   exactly 1  MATCH
    ^- R-0852 —       exactly 1  MATCH

(e) THE OPEN SET BY DISTINCT ID, DECISION F085 D7 (OPEN = REGISTERED − DONE, `Landed:` never
subtracted).

    before (C1)  registered 80  resolved 4  OPEN 76   block says 80/4/76   MATCH
    after  (C2)  registered 81  resolved 4  OPEN 77   block says 81/4/77   MATCH

### G4 — the deletion is complete

All 6 deleted paths print `present: False` against `git ls-tree -r 04ca209c --name-only`, over
4578 tracked files at C3. The corpus for the sweep is the 1695 tracked files outside `.agent/`
and `.data/`. The sweep ran TWICE and printed every remaining line IN FULL; nothing was
truncated.

RAW — exactly TWO lines, both must-not-touch spec files, exactly the two the block names:

    docs/roadmap/features/T2_F260.md:337:   two plus `apps/cli/commands/provider_cmd.py`), `external_builder_sandbox.py`,
    docs/roadmap/features/T2_F272.md:744: FIRST — THE TWELVE CLUSTER-BOUND CONSUMERS ARE NEVER MIGRATED. Cross-referencing the inventory's 72 production consumers against the 24-module cluster list in `docs/roadmap/features/T2_F260.md`'s Design section gives twelve files on both: `builder_routing.py`, `candidate_quality.py`, `dogfood_run.py`, `external_builder_sandbox.py`, `local_candidate_generator.py`, `overnight_executor.py`, `overnight_mission.py`, `overnight_readiness.py`, `provider_trust.py`, `provider_trust_verification.py`, `repair_loop_v2.py` and `review_bundle.py`. Porting any of them onto the unified record is work T005 throws away. They keep their classic-store imports until T005 deletes them, and no round spends a line on them. T004's real remaining size is therefore 60 production files beside the 127 under `tests/`, and that is the figure a scope report uses rather than the headline 199.

Lines OUTSIDE `docs/roadmap/features/` and `docs/archive/`: 0. No real miss.

STRIPPED, with backtick-quoted spans DELETED from each line before matching — the BINDING
zero-gate: 0 lines anywhere.

Zero-gated symbols, quoted spans deleted first:

    get_external_submission     0
    load_external_packages      0
    external_builder_integrity  0

### G5 — the four measurements of a deletion round, at C3

(a) RATCHETS, exit 0:

    python3 -B -m pytest tests/orchestration/test_import_reachability.py \
      tests/orchestration/test_cluster_deletion_map.py \
      tests/orchestration/test_cluster_deletion_order.py tests/docs/ \
      tests/cli/test_advertised_commands.py tests/cli/test_cli_ux.py \
      tests/cli/test_product_spine.py -q
    442 passed in 6.62s

(b) THE SHIPPED READERS, through `apps.cli.command_catalog` and `apps.cli.commands` by import,
never by grep:

    len(_BASE_CATALOG)         276 -> 269
    len(collect_all_handlers)  276 -> 269
    len(GROUPS)                 51 -> 50
    duplicate command ids: 0

    ABSENT from BOTH readers, one per line:
      external-builder.package-create    catalog False  handlers False
      external-builder.package-show      catalog False  handlers False
      external-builder.package-list      catalog False  handlers False
      external-builder.submit            catalog False  handlers False
      external-builder.submission-show   catalog False  handlers False
      external-builder.submission-list   catalog False  handlers False
      external-builder.integrity         catalog False  handlers False
      'external-builder' in GROUPS: False

    PRESENT in BOTH — the trust, verification and human-approval path R-0852 turns on:
      provider.verify        catalog True  handlers True
      patch.approve          catalog True  handlers True
      do.continue            catalog True  handlers True
      worker.registry-list   catalog True  handlers True

The 276 -> 269 and 51 -> 50 falls were confirmed from BOTH ends: the base side was read by
importing the SAME shipped readers inside the disposable worktree at `053a25a7`, with
`PYTHONPATH` pinned to the worktree so the editable install at
`_editable_impl_remedy.pth` could not shadow it. That probe printed the module resolving to
`.remedy-wt/base13/apps/cli/command_catalog.py` and read 276 / 276 / 51 with
`'external-builder' in GROUPS: True`.

(c) THE ORDER FILE. Regenerated from `measured_order()`, never hand-edited.

    components   8 at the base -> 7
    26-line comment header sha256  aff913e6eedb4d9c7e5ab6e76578be881ffffa3612018cf58b5a48ad508b0cc2
    header unchanged vs the base blob: True
    body == ", ".join(component) over measured_order(): True
    numstat 053a25a7..C3:  0  1   — a pure deletion, no surviving component reorders

The regenerated first line is `packages.orchestration.local_model_advisor`, which is the
component PLAN13 names as the next round's target.

(d) THE CANARY, exit 0:

    python3 -B -m pytest tests/cli/test_golden_path.py -q
    42 passed in 19.84s

### G6 — ruff and bash

`git diff --name-only 053a25a7..04ca209c` names 7 `.py` files, of which 3 still exist at C3:
`apps/cli/command_catalog.py`, `apps/cli/commands/__init__.py`,
`tests/orchestration/test_cluster_deletion_map.py`.

    python3 -m ruff check <those 3>          All checks passed!        exit 0
    python3 -m ruff check .   at C3          Found 26 errors.          exit 1
    python3 -m ruff check .   at 053a25a7    Found 26 errors.          exit 1   (disposable worktree)
    bash -n scripts/remedy_test_fast.sh                                exit 0

The repo-wide ceiling `tests/orchestration/test_ci_budgets.py` holds: 26 at both ends, unmoved by
this round. Exit 1 on the repo-wide runs is ruff's own report of the pre-existing 26 and is the
expected reading at BOTH ends, not a red gate; the gate is the equality of the two counts.
`scripts/remedy_test_fast.sh` names no deleted test file this round — grepped for
`external_builder` and `test_external`, zero hits — so it is correctly outside the change set.

### G7 — the full suite, SERIALLY, in the primary checkout

    python3 -B -m pytest tests/ -q          (no -n auto)
    18896 passed, 23 skipped, 1 warning in 1337.56s (0:22:17)
    ---- REAL EXIT CODE from the process object: 0 ----

GREEN, zero failed. The single warning is a pre-existing `UserWarning` from
`packages/orchestration/model_routing.py` raised by a test that asserts that very behaviour.

THE ARITHMETIC CLOSES BY THE ID SET. The base side was collected in the disposable worktree at
`053a25a7`, the tip side at C3 in the primary checkout:

    base ids  18958        tip ids  18919        FALL  39        GAINED  0

    attributed per file:
      20  tests/orchestration/test_external_builder_sandbox.py
      11  tests/cli/test_external_builder_cli.py
       8  tests/test_grouped_cli.py   (parametrises over the catalog; in no change set)

The block measured 18958 at the base and 18919 at the tip, a fall of 39. I measure exactly those
three numbers. The run closes against the collection independently: 18896 passed + 23 skipped =
18919 = the tip collection.

### G8 — the tree

    .agent/STOP re-read from disk — exists: False
    git status --porcelain            ''      empty
    git worktree list                 1 entry: /home/decodeux/Repos/remedy  [feature/f275-one-world-completion-part-three]
    branch                            feature/f275-one-world-completion-part-three

    git diff --name-only 8a688931..04ca209c — SET COMPARISON against the 13 paths
      count 13, expected 13
      missing (in change set, not in diff):  []
      extra   (in diff, not in change set):  []
      EXACT SET MATCH: True

    commit   sha        parents   insertions   under 500
    C0a      3a9ebc38   1         232          True
    C0b      ca833831   1         150          True
    C1       a991c91c   1          16          True
    C2       8a688931   1           8          True
    C3       04ca209c   1           2          True

C4's own numbers belong to the next round's ledger entry and are not claimed here.

## Authored-text proofs

Three reviewer-authored slices were applied this round. Each was extracted from the work order,
its byte count and sha256 verified BEFORE use, and the applied result compared disk-to-disk
against the committed `.agent/authored/f275-r13.md`:

| Slice | Target | Applied how | Proof |
|---|---|---|---|
| PLAN13 | `.agent/plan.md` | whole-file replacement by `shutil.copyfile` | G2: byte-identical, 2697 bytes, sha256 equal |
| LEDGER13 | `.agent/live_review.md` | append after one `b'\n'` separator | G3(a)(b)(c): growth 1+10675, prefix/suffix exact, 3 units equal in order, negative control rejected |
| SLIPS13 | `.agent/prose_slips.md` | append after one `b'\n'` separator | G3(a)(b)(c): growth 1+602, prefix/suffix exact, 1 unit equal, negative control rejected |

The work order itself is proved by G1: source, C0a blob and C0b blob are byte-identical at
27171 bytes. No slice was edited, reflowed or renumbered; constraint 1 held with nothing to
declare under it.

## Deviations & assumptions

NO DEVIATION FROM THE BLOCK'S ORDERED COMMIT SEQUENCE. The bundle ordered six commits — C0a,
C0b, C1, C2, C3, C4 — and six commits landed, in that order, with no extra, none dropped and
none reordered. There is no DECISION slice this round, so the deletion is C3 and this handback
is C4; gates G4 through G8 are worded "at C3" and were read against C3 = `04ca209c`.

NO NUMERIC DEVIATION. Every figure the block states was re-measured and every one matched:
all six deleted-file line counts (560, 161, 269, 153, 70, 94); all thirteen per-path numstats;
the commit shape 2 insertions against 1401 deletions; 442 ratchet passes; 276→269, 276→269 and
51→50 through the shipped readers; the order file's 8→7 with the header sha256 unchanged at
`aff913e6…`; `Found 26 errors.` at both ends; the open set 80/4/76 → 81/4/77; the two RAW sweep
lines at `T2_F260.md:337` and `T2_F272.md:744` with zero stripped; and the base 18958, tip 18919,
fall 39, gained 0.

TWO FIGURES I REPORT AS MINE RATHER THAN RESTATING THE BLOCK'S, neither a defect:

1. THE SUITE'S PASS COUNT. The block's `18888 passed` is the reviewer's DRY RUN inside a
   disposable worktree, where it declared two known worktree artefacts. My run is the one the
   block actually orders — SERIAL, in the PRIMARY checkout, with the change COMMITTED and
   `apps/ui/node_modules` present — and reads 18896 passed, 23 skipped, ZERO failed. The two
   artefact failures do not occur here, exactly as the block predicts, and the six-test
   difference in the skip count is the `node_modules`-dependent nodes running instead of
   skipping. The collection arithmetic closes on my numbers: 18896 + 23 = 18919 = the tip
   collection.

2. `docs/README.md` LINE 167. The block says the surviving archive index row for
   `archive/external-builder-sandbox-future.md` sits at line 167 and STAYS. At the BASE that row
   is at line 171; it lands at 167 only after this round's four rows are removed. The block
   states the POST-deletion position, and the row does stay. I removed the four rows by matching
   the LINK TARGET, never the slug, exactly as the block requires — the surviving row's own slug
   contains `external-builder-sandbox` and a slug-keyed removal would have taken it.

NOTHING WAS FIXED THAT THE BLOCK DID NOT ORDER. The change set is the 13 paths plus the five
`.agent/` paths of C0a, C0b, C1, C2 and C4, and no fourteenth path was needed. R-0843's docs
sweep is deliberately scheduled for the round that drafts DECISION F260 D3 and was not started
here.

NO VERDICT, NO `Done:` PARAGRAPH, NO FINDING AND NO REGISTRATION OF MY OWN was written anywhere.
The only finding text that landed is the reviewer's own LEDGER13 slice, applied byte for byte.
No `Landed:` line was written because no fix landed this round — this round is a deletion.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block to `.agent/authored/f275-r13.md` | done | `shutil.copyfile`, G1 byte-equal |
| C0b mirror to `.agent/last_block.md` | done | `shutil.copyfile`, G1 byte-equal |
| C1 `.agent/plan.md` replaced WHOLE by PLAN13 | done | G2 byte-identical, 45 lines |
| C2 append LEDGER13 and SLIPS13 | done | G3 all five parts |
| C3 the deletion, all 13 paths, ONE commit | done | 2/1401, exact 13-path set match |
| C4 `.agent/handoff.md` rewritten whole | done | this file |
| G1 TRANSPORT | done | exit 0 |
| G2 THE PLAN | done | exit 0 |
| G3 THE RECORD | done | exit 0 |
| G4 THE DELETION IS COMPLETE | done | exit 0 |
| G5 THE FOUR MEASUREMENTS | done | exit 0 |
| G6 RUFF AND BASH | done | exit 0 |
| G7 THE FULL SUITE | done | exit 0 |
| G8 THE TREE | done | exit 0 |

Every ordered item appears exactly once. None skipped, none deviated.

## Open findings

77 by DISTINCT ID at C2, by DECISION F085 D7 (OPEN = REGISTERED − DONE; a `Landed:` line is
never subtracted): 81 registered against 4 resolved. It was 76 at the round's base `053a25a7`;
this round's C2 registers R-0852 and adds two measured instances to the open R-0843 as a NOTE
rather than minting a second id. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's
rather than this feature's, per DECISION F272 D12.

## What the round achieved

The EIGHTH module group of F260's prototype cluster, `external_builder_sandbox` at 560 module
lines, deleted in ONE commit under amend0908-f275-finish RULE 1: 2 insertions against 1401
deletions over 13 paths, taking its 161-line handler file WHOLE, two test files, two doc pages,
seven commands and the `external-builder` group WHOLE with it. The handler file could not have
died one round earlier — round 11 removed the one handler of its eight that did not drive the
sandbox — so this round is the first at which the file has no surviving reason to exist. No
survivor lost a call site and no cockpit section was involved. Seven components remain in the
regenerated deletion order.

## Next

The reviewer re-runs all eight gates against the committed blobs and issues the round 13 verdict.
Before authoring round 14 it re-reads `.agent/STOP` from disk (Phase 1 rule 1) and then the Open
PR Gate (rule 2). Round 14's target is the order file's new first line, the
`packages.orchestration.local_model_advisor` component, a SINGLE module.
