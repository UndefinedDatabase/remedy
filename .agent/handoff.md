# Handback — F275 ROUND 6 — round 5's PASS is booked and the FIRST `git rm` of this feature has landed: the `context_optimizer` module group is gone and the tree is green

This file supersedes the F275 round 5 handback. It is written by the delegated worker of F275
round 6 on the reviewer's authored text; the reviewer never edits a work-tree file. It carries NO
verdict of its own — verdicts live in `.agent/live_review.md`, and this round's C2 booked the
reviewer's authored F275 round 5 PASS there. NO finding is minted and NONE is resolved this
round: RECORD6 is a `Gate:` entry, matching neither the registration pattern nor the resolution
pattern, so the open set does not move (measured at G3(f): 66 → 66 by distinct id).

THIS IS THE FIRST `git rm` OF F275, AND OF THE THREE FEATURES THAT CARRIED THIS DELETION BEFORE
IT. `packages/orchestration/context_optimizer.py` and `apps/cli/commands/context_optimizer_cmd.py`
are deleted whole, together with their two catalog entries, the `related` member naming one of
them, the humanize-catalog entry for the event only that handler emitted, their tests, their
allowlist lines and their cluster-map lines — one commit, `57caf5a0`, and the FULL suite is
green after it at 19768 passed and 23 skipped, exit 0.

## State

| Field | Value |
|---|---|
| Feature | **F275** — One World Completion, part three |
| Round | **6** |
| Session | **3** |
| Branch | `feature/f275-one-world-completion-part-three` |
| Base (round start) | `a1df5d70` — `merge main (amend0908-brainstorm-intake) into f275` |
| HEAD after C3 (the deletion) | `57caf5a0` |
| HEAD after C5 | the C5 commit that writes this file — see "Deviations & assumptions" |
| Commits this round | C0a `3bad8eea`, C0b `e16aff01`, C1 `717fd1e4`, C2 `9b698482`, C3 `57caf5a0`, plus the C5 commit that writes this file. C4 runs the gates and writes no file, so it has no commit. |
| Change set | FIFTEEN paths, exactly the block's enumeration, fourteen of them landed in C0a..C3 and the fifteenth being this file |
| Open findings | **66 by distinct id** — 69 distinct registrations against 3 distinct resolutions, UNCHANGED, measured at G3(f) |
| Pull request | none, and none is owed: under `docs/roadmap/STATUS_closure_protocol.md` the PR belongs to the closure sequence |
| `.agent/STOP` | does not exist — re-read before C0a, again at G7, and again immediately before this file was written |

Full SHAs: `3bad8eea4cf5dc69fc8734d4146fbc32c99abbe5`, `e16aff011dc8ba975b4b27529fe99728ac094a59`,
`717fd1e4778651130e90bb0205542d7ce3a7055c`, `9b698482fdc4847f6454dfec231a36cfcd85c726`,
`57caf5a0dadd954da53c1ae4c747ea795f073c31`.

## Session

`SESSION 3 of feature F275 · round 6 · rounds so far 6`

F275's soft limit is 20 sessions and 60 rounds by operator order amend0908-f275-finish, named for
F275 alone; at 3 sessions and 6 rounds the limit is far off and no scope report is owed.

## Range

Review of `a1df5d70b09cf30e2519a44d8c4686f06f6e9a6b`..HEAD.

The previous reviewed tip was `250c9089`, the round 5 verdict append; `a1df5d70` is the merge of
`main` at `b6e0f257` (amend0908-brainstorm-intake, PR 247) into this branch, and it is the base
the block names.

## Commits

### 3bad8eea F275 R6 C0a: save the round 6 step block verbatim.
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r6.md` | +352 / −0 | the round 6 step block, saved by `shutil.copyfile` from the scratch original — never retyped, never through an editor |

### e16aff01 F275 R6 C0b: mirror the round 6 block to the last-block state file.
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +322 / −295 | the same bytes mirrored, again by `shutil.copyfile`, so all three artefacts hold one digest |

### 717fd1e4 F275 R6 C1: plan states round 6, the first module-group deletion.
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +16 / −17 | replaced whole with PLAN6, byte-identical at 2244 bytes |

### 9b698482 F275 R6 C2: book round 5's PASS and its five prose slips.
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2 / −0 | RECORD6 appended — the F275 R5 `Gate:` record |
| `.agent/prose_slips.md` | +10 / −0 | SLIPS6 appended — round 5's five dated reviewer-prose lines |

### 57caf5a0 F275 R6 C3: delete the context_optimizer module group.
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/context_optimizer.py` | +0 / −179 | `git rm` — the module itself |
| `apps/cli/commands/context_optimizer_cmd.py` | +0 / −143 | `git rm` — its command handler |
| `apps/cli/commands/__init__.py` | +1 / −2 | the import line and the same name inside the `for mod in (...)` tuple |
| `apps/cli/command_catalog.py` | +1 / −30 | the `context.explain` and `context.optimize` entries with their banner, and one member of the surviving `context.inspect` `related` tuple |
| `apps/ui/src/api/humanizeCatalog.ts` | +0 / −1 | the `context_budget_optimized` entry, which the UI-contract test pins to the Python emitters |
| `tests/orchestration/test_project_brain.py` | +0 / −61 | the whole `TestContextOptimizer` class and its five test methods, a span of exactly 2791 bytes |
| `tests/orchestration/import_reachability_allowlist.txt` | +0 / −2 | the module's and the handler's allowlist lines |
| `tests/orchestration/test_cluster_deletion_map.py` | +1 / −4 | the `CLUSTER_MODULES` and `CLUSTER_COMMAND_HANDLERS` lines, and the comment above the second that named the deleted file |
| `.agent/f275_deletion_order.md` | +2 / −3 | REGENERATED body from the live graph — deleting the module reorders the condensation, so a line edit would have gone red |

### the C5 commit that writes this file
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | see "Deviations & assumptions" | a handoff cannot table the commit that writes it (R-0149 pattern); the real `+/-` columns go to the reviewer in the round report instead of as a guess written here |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | `3bad8eea` |
| C0b | done | `e16aff01` |
| C1 | done | `717fd1e4` |
| C2 | done | `9b698482` |
| C3 | done | `57caf5a0` |
| C4 | done | gates G1..G7 all RUN; writes no file and has no commit, as the block orders |
| C5 | done | the commit that writes this file, pushed after it |
| G1 | done | exit 0 — one digest across all three artefacts |
| G2 | done | exit 0 — byte-identical to PLAN6 |
| G3 | done | exit 0 — every predicted numeral reproduced |
| G4 | done | deviated on the grep's exclusion set and on one numeral — see deviations 1 and 2; the property holds |
| G5 | done | deviated on the ui_contracts split and on the denied binary — see deviations 3 and 4 |
| G6 | done | exit 0 — ruff clean, full suite 19768 passed / 23 skipped |
| G7 | done | deviated on ordering — see deviation 5 |

## External actions

| Action | Outcome |
|---|---|
| `git push -u origin feature/f275-one-world-completion-part-three` | `a1df5d70..57caf5a0`, branch set up to track origin |
| `git push` (after C5) | pushes the commit that writes this file |
| `remedy --all-commands` | DENIED by the session sandbox, verbatim: `This command requires approval`. G5 permits an honest denial here and routes the binding reading to the catalog. |
| worktree add / remove | NONE. No destructive verification was needed: the whole round is additive-or-deleting on the branch and every gate reads committed blobs or runs a read-only suite. `git worktree list` shows only the primary checkout. |
| PR create / merge | NONE. No PR is created or merged this round. |

## Verification

Seven gates, every one RUN, real exit codes.

| Gate | Exit | Headline |
|---|---|---|
| G1 TRANSPORT | 0 | scratch original, `.agent/authored/f275-r6.md` and `.agent/last_block.md` all **26012 bytes** at `689b75aba03bfa19730fb9cace7495290cc9341fbd48046d99a62b2b0748be99` — ONE value |
| G2 THE PLAN | 0 | `.agent/plan.md` **2244 bytes**, sha256 `8e92db53…c586c7`, byte-identical to PLAN6; **40 lines** against the AGENTS.md cap of 50; `^## Goal$` ×1, `^## Next Steps$` ×1 |
| G3 THE RECORD | 0 | live_review 533079→536113 (gain 3034 = 1+3033); prose_slips 169429→171102 (gain 1673 = 1+1672); both edges exact; N counted from the slices = 1 and 5; negative controls REJECTED by both readers with the tracked files unchanged on disk; units 220→221 and 237→242; `^Gate: ` 27→28; `^Gate: F275 R5 ` 0→1; **open set 66→66 by distinct id** |
| G4 THE DELETION IS COMPLETE | 0 | both paths absent from `git ls-tree` at the tip; six dead symbols at ZERO over the tracked tree; `context_optimizer` at EXACTLY ONE non-ignored file; `context_budget_optimized` in exactly the THREE named files — see deviations 1 and 2 |
| G5 RATCHETS AND DISPATCH | 0 | ratchets **9 passed**; `tests/ui_contracts/` **809 passed, 4 skipped**; dispatch table **338**, `context.explain`/`context.optimize` ABSENT, `context.inspect`/`context.pack` PRESENT; catalog carries ZERO of the two dead ids in a `command_id` or a `related` tuple — see deviations 3 and 4 |
| G6 RUFF AND THE FULL SUITE | 0 | `All checks passed!`; FULL suite in the PRIMARY checkout **19768 passed, 23 skipped, 1 warning in 1433.97s**, exit **0**, ZERO failures — so the known-environment question G6 raises never arose |
| G7 THE TREE | 0 | no `.agent/STOP`; `git status --porcelain` EMPTY (0 lines); branch correct; ONE worktree; range = the block's paths; every commit single-parent in order C0a, C0b, C1, C2, C3 with NO C4 commit — see deviation 5 |

### G1 — transport

    git show HEAD:.agent/authored/f275-r6.md | sha256sum   → 689b75ab…48be99, 26012 bytes
    git show HEAD:.agent/last_block.md       | sha256sum   → 689b75ab…48be99, 26012 bytes
    sha256sum .remedy-wt/f275-r6-block.md                  → 689b75ab…48be99, 26012 bytes

Per §3 item 37 this chain covers the saved copy and its mirror against the scratch original the
reviewer handed over; it claims nothing about the bytes that were emitted.

### G3 — the record, from the committed blobs at `a1df5d70` and at HEAD

    .agent/live_review.md
      (a) BYTES 533079 -> 536113  gain 3034 = 1 + 3033
      (b) EDGES  pre-blob is a byte-exact PREFIX: True;  '\n'+slice is a byte-exact SUFFIX: True
      (c) ORDERED EQUALITY  N counted from the slice = 1;  last 1 units equal the 1 paragraphs IN ORDER: True
      (d) NEGATIVE CONTROL  byte 534596 of the FIRST appended paragraph flipped in memory:
          (b) prefix=True suffix=False -> REJECTS=True;  (c) ordered equality -> REJECTS=True
          tracked file re-read from disk: 536113 -> 536113 bytes, UNCHANGED: True
      (e) blank-line units 220 -> 221;  '^Gate: ' 27 -> 28;  '^Gate: F275 R5 ' 0 -> 1
      (f) distinct '^- R-\d+ — ' ids 69 -> 69;  distinct '^Done: R-\d+ — ' ids 3 -> 3
          OPEN BY DISTINCT ID 66 -> 66
    .agent/prose_slips.md
      (a) BYTES 169429 -> 171102  gain 1673 = 1 + 1672
      (b) EDGES  PREFIX: True;  SUFFIX: True
      (c) ORDERED EQUALITY  N counted from the slice = 5;  last 5 units equal the 5 paragraphs IN ORDER: True
      (d) NEGATIVE CONTROL  byte 169593 flipped in memory: (b) REJECTS=True;  (c) REJECTS=True
          tracked file re-read from disk: 171102 -> 171102 bytes, UNCHANGED: True
      (e) blank-line units 237 -> 242

N was counted from the SLICE bytes with the worker's own paragraph reader, not read off the block.
Both negative controls were performed in memory on a `bytes` copy; the flip was an XOR of one byte
inside the FIRST appended paragraph, and the tracked file's size on disk is identical before and
after, so the control provably touched no disk state.

### G4 — the deletion is complete

    git ls-tree -r HEAD --name-only -- packages/orchestration/context_optimizer.py \
                                       apps/cli/commands/context_optimizer_cmd.py
    (no output — NEITHER path exists at the tip)

Six dead symbols, over the TRACKED tree at HEAD excluding `.agent/` and `.data/`:

    explain_context        0
    optimize_context       0
    context.explain        0
    context.optimize       0
    _cmd_context_explain   0
    _cmd_context_optimize  0

`context_optimizer`, EXACTLY ONE hit, and it is the file constraint 6 keeps on purpose:

    docs/roadmap/features/T2_F260.md:342:  `context_optimizer.py`, `overnight_mission.py`, `overnight_executor.py`,

`context_budget_optimized`, in exactly the THREE files the block names — TRAP 3's two survivors
plus the test that pins one of them:

    apps/ui/src/api/actionClass.ts:19:          "context_budget_optimized",
    packages/orchestration/event_schemas.py:39:    "context_budget_optimized": frozenset({
    tests/orchestration/test_event_ledger.py:49:        assert "context_budget_optimized" in EVENT_METADATA_SCHEMAS
    tests/orchestration/test_event_ledger.py:61:        budget = EVENT_METADATA_SCHEMAS["context_budget_optimized"]
    tests/orchestration/test_event_ledger.py:105:    def test_context_budget_optimized_schema(self):
    tests/orchestration/test_event_ledger.py:107:        schema = EVENT_METADATA_SCHEMAS["context_budget_optimized"]

### G5 — the ratchets, the dispatch table and the catalog

    python3 -m pytest tests/orchestration/test_import_reachability.py \
      tests/orchestration/test_cluster_deletion_map.py \
      tests/orchestration/test_cluster_deletion_order.py -q
    9 passed in 5.38s                                   exit=0

    python3 -m pytest tests/ui_contracts/ -q
    809 passed, 4 skipped in 5.54s                      exit=0

Through the SHIPPED reader `apps.cli.commands.collect_all_handlers`:

    table size: 338
      context.explain    resolves: False
      context.optimize   resolves: False
      context.inspect    resolves: True
      context.pack       resolves: True

Through `apps.cli.command_catalog` — the BINDING reading, ordered unconditionally:

    CATALOG entries: 338
    surviving entries whose command_id is context.explain or context.optimize: 0
    surviving entries whose related tuple names either: 0 []
    context.inspect related tuple now: ('context.pack',)

The regenerated body of `.agent/f275_deletion_order.md`, in full, read back from the committed
blob at C3 — fourteen components where round 5 recorded fifteen:

    packages.orchestration.review_bundle
    packages.orchestration.worker_recommend
    packages.orchestration.context_pack
    packages.orchestration.dogfood_run, packages.orchestration.feature_planner, packages.orchestration.overnight_mission, packages.orchestration.progress_ledger, packages.orchestration.repair_loop_v2, packages.orchestration.self_repair_proposal
    packages.orchestration.builder_routing, packages.orchestration.candidate_quality, packages.orchestration.local_candidate_generator, packages.orchestration.model_route_tournament
    packages.orchestration.execution_approval_policy
    packages.orchestration.external_builder_sandbox
    packages.orchestration.local_model_advisor
    packages.orchestration.managed_builder_execution
    packages.orchestration.overnight_executor
    packages.orchestration.worker_registry
    packages.orchestration.main_builder_adapter
    packages.orchestration.overnight_readiness
    packages.orchestration.provider_trust, packages.orchestration.provider_trust_verification

The first three lines are `review_bundle`, `worker_recommend`, `context_pack` — exactly what the
reviewer's own run of the recipe produced. The body was NOT edited toward that prediction; the
shipped `measured_order()` was run after steps (1) to (7) were on disk, and this is its output.
TRAP 1 is confirmed by the diff: `worker_recommend` moved from the fourth line to the second and
`context_pack` from the sixth to the third, and the two multi-module components moved down past
them, so a line-edit of this file would have gone red.

### G6 — ruff and the full suite

    python3 -m ruff check apps/cli/commands/__init__.py apps/cli/command_catalog.py \
      tests/orchestration/test_project_brain.py tests/orchestration/test_cluster_deletion_map.py
    All checks passed!                                  exit=0

    python3 -m pytest tests/ -q
    19768 passed, 23 skipped, 1 warning in 1433.97s (0:23:53)
                                                        exit=0

ZERO failures, so neither `tests/orchestration/test_test_runner.py`'s vitest node nor
`tests/ui_server/test_command_channel.py` needed a base control: the clause that would have
demanded one is unreached. The single warning is `model_routing.py`'s pre-existing
`undeclared_role` UserWarning, raised by a test that asserts that warning.

### G7 — the tree, run LAST

    ls -la .agent/STOP        → No such file or directory
    git status --porcelain    → 0 lines
    git branch --show-current → feature/f275-one-world-completion-part-three
    git worktree list         → /home/decodeux/Repos/remedy  57caf5a0  (the primary checkout ALONE)

    git diff --name-only a1df5d70..57caf5a0
    .agent/authored/f275-r6.md
    .agent/f275_deletion_order.md
    .agent/last_block.md
    .agent/live_review.md
    .agent/plan.md
    .agent/prose_slips.md
    apps/cli/command_catalog.py
    apps/cli/commands/__init__.py
    apps/cli/commands/context_optimizer_cmd.py
    apps/ui/src/api/humanizeCatalog.ts
    packages/orchestration/context_optimizer.py
    tests/orchestration/import_reachability_allowlist.txt
    tests/orchestration/test_cluster_deletion_map.py
    tests/orchestration/test_project_brain.py

Fourteen paths, and they are the block's fifteen minus `.agent/handoff.md`, which C5 adds after
this gate by the block's own ordering — see deviation 5.

Every commit in the range single-parent, from `git rev-list --parents`, oldest first:

    3bad8eea a1df5d70 | F275 R6 C0a: save the round 6 step block verbatim.
    e16aff01 3bad8eea | F275 R6 C0b: mirror the round 6 block to the last-block state file.
    717fd1e4 e16aff01 | F275 R6 C1: plan states round 6, the first module-group deletion.
    9b698482 717fd1e4 | F275 R6 C2: book round 5's PASS and its five prose slips.
    57caf5a0 9b698482 | F275 R6 C3: delete the context_optimizer module group.

Exactly one parent each, in the block's order, with NO C4 commit.

Insertions against the DECISION F104 D1 cap of 500 — the `+` column only:

| Commit | Insertions | Cap 500 |
|---|---|---|
| C0a `3bad8eea` | 352 | UNDER |
| C0b `e16aff01` | 322 | UNDER (and a single `.agent/**` state-file rewrite, exempt in any case) |
| C1 `717fd1e4` | 16 | UNDER (and likewise exempt) |
| C2 `9b698482` | 12 | UNDER |
| C3 `57caf5a0` | 5 | UNDER — the deletion inserts five lines and deletes 425 |

No commit is oversize and no exception is claimed.

## Authored-text proofs

Three authored slices, all extracted from the block by their own delimiters and verified against
their own stamps BEFORE anything was applied:

| Slice | Bytes (measured / stamped) | sha256 (measured / stamped) | Match |
|---|---|---|---|
| PLAN6 | 2244 / 2244 | `8e92db53…c586c7` / same | yes |
| RECORD6 | 3033 / 3033 | `34981eb5…4df09d3` / same | yes |
| SLIPS6 | 1672 / 1672 | `32d5fcb4…e1ad0fd` / same | yes |

Disk-to-disk after application: the committed `.agent/plan.md` blob is byte-identical to the
extracted PLAN6 slice (G2). The committed `.agent/live_review.md` and `.agent/prose_slips.md`
carry `\n` + their slice as a byte-exact SUFFIX, and their pre-blobs as a byte-exact PREFIX
(G3(b)), with ordered paragraph equality over the appended region (G3(c)).

The block itself: `.agent/authored/f275-r6.md` and `.agent/last_block.md` were both produced by
`shutil.copyfile` from the scratch original and never by retyping or an editor round trip; all
three hold one digest (G1).

## Deviations & assumptions

**1. G4's grep exclusion set does not exclude build caches, so the literal command is not zero
over the working directory.** The block orders "a repo-wide grep, excluding `.git/`, `.data/`,
`.agent/` and `.remedy-wt/`". Run exactly that way it returns hits in
`.mypy_cache/`, `.ruff_cache/`, `apps/cli/commands/__pycache__/context_optimizer_cmd.cpython-310.pyc`
(binary), `.pytest_cache/v/cache/nodeids`, `.coverage_reports/coverage.json` and three files under
`.brain/`. NOTHING WAS DELETED TO MAKE THE GATE GREEN. Instead the residue was CLASSIFIED: the
literal grep matches six text files; `git check-ignore` reports FIVE of them ignored — all stale
build and run artefacts of the very code this commit deleted — and exactly ONE not ignored, and
that one is `docs/roadmap/features/T2_F260.md`, which constraint 6 keeps on purpose. The binding
measurement reported above is therefore taken with `git grep` over the TRACKED tree at HEAD, which
excludes ignored artefacts by construction, and it is ZERO for all six symbols and ONE for
`context_optimizer`. The stale `.pyc` is left where it is: it is untracked, `git status
--porcelain` is empty with it present, and AGENTS.md-adjacent practice forbids deleting artefacts
by glob.

**2. G4's `context_budget_optimized` numeral counts FILES, not lines.** The block orders "EXACTLY
THREE hits, in `packages/orchestration/event_schemas.py`, `apps/ui/src/api/actionClass.ts` and
`tests/orchestration/test_event_ledger.py`". The real reading is SIX line hits in exactly those
three files — one each in the first two, and FOUR in `test_event_ledger.py` (lines 49, 61, 105
and 107), which is the suite TRAP 3 says asserts the key is present. The property the gate exists
for holds exactly as stated: the surviving occurrences are confined to the three named files and
nowhere else. Nothing was changed to fit the numeral.

**3. `tests/ui_contracts/` splits 809/4 here, where the reviewer measured 808/5.** The TOTAL is
813 in both readings; one test that skipped for the reviewer passes here. The four skips are all
the `D3 quarantine (F252)` legacy-`.tsx` skips in `test_graph_architecture.py` and
`test_ux_quality.py`. The split was stable across two independent runs in this checkout. Exit code
0 either way, and the property the gate exists for — TRAP 2's humanize-catalog contract green
after the entry is deleted — holds.

**4. `remedy --all-commands` is DENIED to this session's shell.** The verbatim response is
`This command requires approval`. G5 states this clause is satisfied by an honest denial and
routes the binding reading to the catalog, which was run unconditionally and reports ZERO
surviving `context.explain` / `context.optimize` in a `command_id` or a `related` tuple.

**5. G7 is ordered to run LAST, before C5, yet its own commit-sequence clause names C5.** The
block's constraint 8 says "G7 runs LAST, after G1..G6, and C5 is committed after it", while G7
itself requires the range to equal the block's fifteen-path list and the sequence to be "C0a, C0b,
C1, C2, C3, C5". Those cannot both be true at one moment. The ORDERING was obeyed as written: G7
ran at tip `57caf5a0`, before C5, and reports fourteen paths and five single-parent commits. The
missing fifteenth path is `.agent/handoff.md` and the missing sixth commit is C5, both of which
this commit adds. The reviewer can close the clause by re-running the two range readings at the
post-C5 tip; the worker reports the post-C5 numbers to the reviewer in the round report rather
than writing a self-referential guess into this file.

**6. No `git worktree` was created this round.** Guardrail G5 requires isolation for destructive
or mutating verification; this round had none. The two negative controls G3(d) orders were
performed on in-memory `bytes` copies and the tracked files were re-read from disk afterwards at
unchanged sizes, which is proof the control never reached disk. The primary checkout satisfied
`git status --porcelain` empty at every commit boundary and at this handback.

**7. C5 cannot table its own numstat columns.** Per the R-0149 pattern the handoff commit's
`+/-` are reported to the reviewer in the round report instead of being guessed here.

## Context self-assessment

Context is comfortable. The round's largest single cost was G6's full suite at 23 minutes 54
seconds, whose output was read as a tail rather than in full; nothing else pressed against a limit
and no reviewer-prose slip of my own accumulated.

Fortschritt: ~38 % (T001: Claim ✅ · Record ✅ · D1 ✅ · Carry-over readiness ✅ · Carry-over
report ✅ · R-0831 geprüft ✅ · Löschreihenfolge ✅ · D2 ✅ · Löschung 1 von 15 Gruppen ✅
(`context_optimizer`) · 14 Gruppen offen · F260 D3 offen · T002 offen · T003 offen) — Schätzung

## Next

The `review_bundle` group, the regenerated order file's NEW first line, in its own commit: the
module, any handler, catalog entries, cockpit section, tests and map lines together, leaving the
tree green. Before authoring it the reviewer re-reads `.agent/STOP` (Phase 1 rule 1 before rule
2), and TRAP 2 now generalises: every group whose module emits a stream event must delete the
matching `apps/ui/src/api/humanizeCatalog.ts` key in the SAME commit, because
`tests/ui_contracts/test_humanize_catalog.py` derives the emitter set by AST walk and compares it
to that catalog's keys.
