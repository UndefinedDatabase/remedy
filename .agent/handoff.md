# Handback — F275 round 18

## Session

SESSION 10 of feature F275 · round 18 · rounds so far 18

F275's soft limit is 20 sessions and 60 rounds by operator amendment
amend0908-f275-finish rule 1, and it travels to no other feature. This round is
well inside it, so no scope report is owed.

This was a DELETION round: the TWELFTH module group of the prototype cluster,
`packages.orchestration.overnight_executor`, component 1 of
`.agent/f275_deletion_order.md`, in ONE commit. It first booked round 17's PASS
verdict, the R-0861 resolution and one prose slip from the pushed
`.agent/handoff.md`, per amend0827-process-diet rule 1, and then ruled DECISION
F275 D8 on disk BEFORE the first `git rm`, per F275 T001 RULE 3.

Context self-assessment (amend0905-throughput): context is comfortable; the
round's cost was dominated by the 23-minute serial full suite, not by reading.

## Range

Review of `c4c314c2`..`HEAD`

## Commits

Six single-parent commits. C5 is the handoff commit itself and is not tabled
against its own numbers (R-0149 pattern, §3 item 14).

### ec9d8cf8 F275 R18 C0a: save the round 18 step block under the authored texts.
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f275-r18.md | +430/-0 | the reviewer's step block, saved verbatim; C0a is the blob every slice is extracted from |

### 726cc79a F275 R18 C0b: mirror the round 18 step block into the last-block state file.
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +409/-233 | the same bytes mirrored into the last-block state file, extracted from the committed C0a blob |

### 97f5a618 F275 R18 C1: advance the plan to round 18.
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +20/-23 | replaced WHOLE by the PLAN18 slice; 41 lines against the AGENTS.md cap of 50 |

### 2bf8a0a0 F275 R18 C2: book the round 17 PASS verdict, the R-0861 resolution and two new findings.
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +8/-0 | the LEDGER18 slice appended: the R17 `Gate:` record, `Done: R-0861`, and the R-0862 and R-0863 registrations |
| .agent/prose_slips.md | +2/-0 | the SLIPS18 slice appended: the round 17 SPINE17 region-description slip |

### eeb3cdfe F275 R18 C3: rule DECISION F275 D8 on the live-review parser before the deletion.
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +66/-0 | DECISION F275 D8 appended; it lands BEFORE any `git rm`, per block constraint 4 |

### ead50596 F275 R18 C4: delete the overnight_executor module group and unthread its three surviving consumers.
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/overnight_executor.py | +0/-1119 | the module, deleted whole |
| tests/orchestration/test_overnight_executor.py | +0/-394 | its unit tests, deleted whole |
| tests/cli/test_overnight_executor_cli.py | +0/-137 | its CLI tests, deleted whole |
| docs/system/bounded-overnight-executor-v0.md | +0/-112 | its documentation page, deleted whole |
| apps/cli/commands/overnight_cmd.py | +0/-28 | `_cmd_overnight_run` and its COMMAND_HANDLERS line; the file SURVIVES with its other three commands |
| apps/cli/command_catalog.py | +0/-28 | the `overnight.run` CommandEntry, deleted whole |
| packages/orchestration/self_dogfood.py | +0/-41 | `_review_findings`, `_detect_review`, the call site, the `has("overnight_executor.py")` roadmap rule, and the section banner left readerless |
| packages/orchestration/self_dogfood_execution.py | +0/-18 | `_review_blocks` and the review gate in `evaluate_self_execution_eligibility`; every other gate untouched |
| packages/orchestration/orchestrator_brain.py | +12/-42 | `_review_state` and its call site, the four unthreaded parameters, and the now-readerless `_agent_dir` |
| tests/orchestration/test_orchestrator_brain.py | +0/-18 | the two tests that pinned the review-driven human-review tier |
| tests/orchestration/test_self_dogfood.py | +14/-23 | two deleted review tests, plus the RE-BASED ambiguous-selection test and the widened `_job` helper |
| tests/orchestration/test_self_dogfood_execution.py | +0/-7 | `TestEligibility::test_pending_review_blocks` |
| tests/orchestration/test_development_artifact_boundary.py | +0/-1 | the `_ALLOWED_LEGACY` entry, load-bearing: `TestAllowlistCompleteness` asserts the path exists |
| docs/system/development-artifact-boundary-v0.md | +0/-1 | the allowed-uses table row naming the module |
| tests/orchestration/test_cluster_deletion_map.py | +0/-1 | the `CLUSTER_MODULES` entry |
| tests/orchestration/cluster_deletion_map.txt | +0/-3 | the three consumer-edge lines, cut in the same commit as their edges |
| tests/orchestration/import_reachability_allowlist.txt | +0/-1 | the reachability allowlist line |
| .agent/f275_deletion_order.md | +1/-2 | REGENERATED from the live graph, not line-edited; the remainder reorders |
| docs/README.md | +0/-1 | the index row for the deleted page (AGENTS.md Documentation Updates) |
| docs/system/repair-loop-v1.md | +0/-1 | one cross-link bullet |
| docs/system/provider-trust-gate-v0.md | +0/-1 | one cross-link bullet |
| docs/guides/do-continue-v1.md | +0/-3 | one cross-link bullet |
| docs/archive/self-dogfood-overnight-future.md | +0/-1 | one cross-link bullet |
| docs/archive/bounded-overnight-prep-v0.md | +0/-10 | TWO references: the `## How the executor uses this` section (one sentence) and one cross-link bullet |

Per-commit insertions against the DECISION F104 D1 cap of 500, single parent
each: 430, 409, 20, 10, 66, 27. The `+/-` column above was compared cell by cell
against `git show --numstat` per commit and they AGREE (G6(g)).

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/r18probe ead50596` | created; the G5 red-proofs ran only there |
| `git worktree remove --force .remedy-wt/r18probe` + `git worktree prune` | removed and pruned before C5 |
| `git worktree add --detach .remedy-wt/r18base c4c314c2` | created READ-ONLY, to collect the base test count and the two deleted files' count |
| `git worktree remove --force .remedy-wt/r18base` + `git worktree prune` | removed and pruned |
| `git worktree add --detach .remedy-wt/r18base2 c4c314c2` | created READ-ONLY, to measure the base ruff error count |
| `git worktree remove --force .remedy-wt/r18base2` + `git worktree prune` | removed and pruned |
| `git push -u origin feature/f275-one-world-completion-part-three` | run ONCE, after C5 |

No PR created, nothing merged, no `gh` command run.

## Verification

Every gate below was EXECUTED and its REAL exit code recorded with
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`.

### G1 TRANSPORT — exit 0

    delegation source  .remedy-wt/f275-r18.md        35020 bytes  4322efd9bed4c28b059739c9b391fb773362278e19782875e5f8d5bbaafc6a36
    committed          ec9d8cf8:.agent/authored/f275-r18.md  35020 bytes  4322efd9…
    committed          ead50596:.agent/last_block.md         35020 bytes  4322efd9…
    ALL THREE BYTE-EQUAL: True

Per §3 item 37 this chain covers those three artefacts and claims nothing about
the bytes the reviewer emitted.

### G2 THE PLAN AND THE DECISION SLICE — exit 0

    block TOTAL lines                       : 430 against its cap of 490
    .agent/plan.md at C1 bytes              : 2338
    .agent/plan.md at C1 sha256             : 4640c33788ca986944885badb88f9476be1f4be83803b86a87bfe96e9ebca7e2
    byte-identical to the PLAN18 slice      : True
    .agent/plan.md lines                    : 41 against the AGENTS.md cap of 50
    heading `## Goal` occurrences           : 1
    heading `## Next Steps` occurrences     : 1
    DECISION18 occurrences in decisions.md at C3 : 1
    slice own sha256                        : 93a1b428bfde7c4a3aba9f08ad6bcb7236d1e5cb3c897afe50619e1f4e4042ea
    bytes at that site re-hashed            : 93a1b428bfde7c4a3aba9f08ad6bcb7236d1e5cb3c897afe50619e1f4e4042ea
    site re-hash equal                      : True

### G3 THE RECORD, over TWO appends — exit 0

`.agent/live_review.md` <- LEDGER18

    (a) BYTE READER
        pre  659974  81bb7a48187c72c912b3bf1c3b9493a891c8146a5fd42abf021616713016689e
        post 666602  4545982f94b952a44485f13980818c89bc3d3d961de3eb40258d7ef0b3e178ac
        growth == 1 + slice length (6628 == 1 + 6627) : True
        pre is a byte-exact PREFIX of post            : True
        slice is a byte-exact SUFFIX of post          : True
        joining byte read back                        : b'\n'
    (b) STRUCTURAL READER
        N COUNTED BY THE SCRIPT from the slice        : 4
        last 4 blank-line units of the WHOLE post-file == the slice's 4 paragraphs IN ORDER : True
        per-unit sha256 (post/slice, first 16): 4a335fee42fb2ec5/4a335fee42fb2ec5,
            591f50826e31d909/591f50826e31d909, 3c1976d776ea4d25/3c1976d776ea4d25,
            a3150de78a61494b/a3150de78a61494b — all equal
    (c) NEGATIVE CONTROL — one byte flipped IN MEMORY in the FIRST appended paragraph
        byte reader REJECTS the mutant       : True
        structural reader REJECTS the mutant : True
        byte reader ACCEPTS the truth        : True
        structural reader ACCEPTS the truth  : True
        file re-read from disk == committed post-blob : True

`.agent/prose_slips.md` <- SLIPS18

    (a) BYTE READER
        pre  191891  efe99ef767ae2c7e58ef972e20be06ba2eb0d9cfaffc2c95b0fde61200595b70
        post 192846  c36e22a9669bdcba66f6139f5417d8084532816af67626f52ad2083748b9ac2b
        growth == 1 + slice length (955 == 1 + 954) : True
        pre is a byte-exact PREFIX of post          : True
        slice is a byte-exact SUFFIX of post        : True
        joining byte read back                      : b'\n'
    (b) STRUCTURAL READER
        N COUNTED BY THE SCRIPT from the slice      : 1
        ordered equality over the whole appended region : True
        per-unit sha256 (post/slice, first 16): d378dab1bb61070f/d378dab1bb61070f
    (c) NEGATIVE CONTROL — one byte flipped IN MEMORY in the FIRST appended paragraph
        both readers REJECT the mutant and both ACCEPT the truth : True
        file re-read from disk == committed post-blob            : True

    (d) COUNT PATTERNS in the C2 post-blob of .agent/live_review.md
        `^Gate: ` rise            : 39 -> 40
        `^Gate: F275 R17 `        : exactly 1
        `^Done: R-0861 — `        : exactly 1
        `^- R-0862 — `            : exactly 1
        `^- R-0863 — `            : exactly 1

    (e) THE OPEN SET BY DISTINCT ID, `Landed:` lines never subtracted
        base c4c314c2 : registered 90  done 5  open 85  distinct Landed ids present 34
        C2   2bf8a0a0 : registered 92  done 6  open 86  distinct Landed ids present 34
        THE BASE REPRODUCES the reviewer's measurement exactly.

### G4 THE SWEEP IS CLEAN — sweep exit 0, `test_advertised_commands.py` exit 0

Sweep over every tracked file outside `.agent/` and `.data/` — 1672 files, 8
tokens (`overnight_executor`, `run_overnight_executor`, `parse_review_findings`,
`review_findings_block_execution`, `render_overnight_run_report_markdown`,
`bounded-overnight-executor-v0`, `overnight.run`, `overnight run`).

    RAW 9   STRIPPED 6      (base c4c314c2 over 1676 files: RAW 76, STRIPPED 70)

THE RAW LIST, IN FULL, NEVER TRUNCATED (marker = whether the line survives
stripping of backtick-quoted spans; R-0861's fix clause makes the RAW list the
binding read):

    [STRIPPED-SURVIVOR] docs/archive/bounded-overnight-prep-v0.md:7: FUTURE bounded overnight run. This block is preparation only — there is **no
    [STRIPPED-SURVIVOR] docs/archive/bounded-overnight-prep-v0.md:17: ## Readiness vs. actual overnight run
    [quoted-only      ] docs/roadmap/features/T2_F260.md:342: `context_optimizer.py`, `overnight_mission.py`, `overnight_executor.py`,
    [quoted-only      ] docs/roadmap/features/T2_F260.md:361: (`overnight_executor.render_overnight_run_report_markdown`) → `mission readiness`
    [quoted-only      ] docs/roadmap/features/T2_F272.md:744: FIRST — THE TWELVE CLUSTER-BOUND CONSUMERS ARE NEVER MIGRATED. … `overnight_executor.py`, …
    [STRIPPED-SURVIVOR] docs/system/repair-loop-v1.md:134: overnight run; provider/Ollama execution; contract relaxation; budget increase.
    [STRIPPED-SURVIVOR] packages/orchestration/mission_readiness.py:61: """Conservative bounds for a FUTURE bounded overnight run.
    [STRIPPED-SURVIVOR] packages/orchestration/overnight_readiness.py:79: """Conservative bounds for a FUTURE bounded overnight run.
    [STRIPPED-SURVIVOR] tests/cli/test_product_spine.py:145: "test_overnight_executor_cli.py",

WHY EACH SURVIVOR IS WHAT IT IS. THREE CLASSES, not the ONE the block predicts —
this is DEVIATION 1 below.

1. The three `docs/roadmap/features/` lines are the class the block names: prose
   naming the deletion as history. Correct, and they stay.
2. Five lines match the token `overnight run` as an ENGLISH PHRASE, never as the
   command `remedy overnight run`: "a FUTURE bounded overnight run", a heading
   "Readiness vs. actual overnight run", and a "this block does NOT" list. All
   five are byte-identical at base `c4c314c2`, none names a deleted symbol or a
   deleted page, and none is an advertisement a user could follow. They are an
   artefact of sweeping the spaced command form against English prose.
3. `tests/cli/test_product_spine.py:145` names the string
   `"test_overnight_executor_cli.py"` inside a NEGATIVE assertion list — "Fast
   lane must not include heavy runtime file". The assertion still passes; the
   string is now stale because this round deletes that file. THE PATH IS NOT IN
   THE BLOCK'S CHANGE SET, so under block constraint 2 it was NOT touched. It is
   reported here rather than routed around.

The violation set fell from 73 at base to 6, and EVERY ONE of the 6 is
byte-identical at base: this round introduced ZERO new hits and removed 67.

    python3 -B -m pytest tests/cli/test_advertised_commands.py -q
    5 passed in 0.29s
    REAL_EXIT=0

The guard the block predicted would fail at base is green here because the doc
it named, `docs/system/bounded-overnight-executor-v0.md`, is deleted by C4;
the guard was run at C4, after the deletion. R-0847 stays open.

Also re-measured by hand this round, because R-0859 records that nothing
resolves it automatically: the catalog's `related=` closure. 236 command ids;
`overnight.run` appears in NO `related=` tuple and in no `command_id`; the
dangling set is EXACTLY the two pre-existing ids R-0859 already names,
`dogfood.run-loop` and `readiness.show`, unchanged by this round.

### G5 THE RED-PROOFS — all in the disposable worktree `.remedy-wt/r18probe` at C4 `ead50596`

`__pycache__` purged before every run, `python3 -B`, control run FIRST over the
SAME node set in the SAME script as its mutation, then revert and re-run.

    ===== P2 — the approval gate SURVIVES and is still pinned =====
      revert target by PATH : packages/orchestration/self_dogfood_execution.py
      target sha256 before  : 4ecf1b92fb6dc14640b95f5f7f7b2f2f0466dcc1e1ae7a22ddcd456cd7108c9e
      mutated bytes occur   : 1 time in that file
      node set              : tests/orchestration/test_self_dogfood_execution.py::TestEligibility
      CONTROL   exit 0  | 6 passed in 0.28s
      MUTATION  exit 1  | 1 failed, 5 passed in 0.29s
      REVERTED  exit 0  | 6 passed in 0.28s
      target sha256 after   : 4ecf1b92…  restored byte-identically: True
      PROPERTY HELD: control 0, mutation 1 — the reviewer's 6 passed / 1 failed 5 passed reproduced.

    ===== P3 — the RE-BASED ambiguous-selection test genuinely BITES =====
      revert target by PATH : packages/orchestration/self_dogfood.py
      target sha256 before  : 6c22f0c5d69e0639b77e3caffff21d50ef24342715b0ea4c7bd71f382e9030ed
      mutated bytes occur   : 1 time in that file  (Priority.HIGH -> Priority.LOW on the per-failure EVIDENCE_GAP item)
      node set              : tests/orchestration/test_self_dogfood.py::TestPlanAndPropose::test_propose_ambiguous_requires_selection
      CONTROL   exit 0  | 1 passed in 0.25s
      MUTATION  exit 1  | 1 failed in 0.26s
      REVERTED  exit 0  | 1 passed in 0.25s
      target sha256 after   : 6c22f0c5…  restored byte-identically: True
      PROPERTY HELD: control 0, mutation 1 — the reviewer's 1 passed / 1 failed reproduced.

    ===== P1 — ORDERED AS A PROBE, NOT AS A COLOUR (§3 item 5) =====
      revert target by PATH : packages/orchestration/orchestrator_brain.py
      target sha256 before  : 5a258580f9d921d48bed644eb2048baa7a0f8208a9fa202cf312d27d15ef1cc2
      mutated bytes occur   : 1 time in that file  (the surviving loop-guard condition in `_routing_plan` -> constant false)
      node set              : tests/orchestration/test_orchestrator_brain.py::TestAntiLoop and ::TestModelRouting
      CONTROL   exit 0  | 5 passed in 0.31s
      MUTATION  exit 0  | 5 passed in 0.31s
      REVERTED  exit 0  | 5 passed in 0.31s
      target sha256 after   : 5a258580…  restored byte-identically: True
      COLOUR REPORTED, NOT ASSERTED: the mutation is GREEN. The branch is not
      pinned once this round's two routing tests are deleted. This reproduces the
      reviewer's own reading exactly and is the coverage loss R-0862 records.

Worktree porcelain was empty at removal; the worktree was removed and pruned
before C5 and `git worktree list` now shows the primary checkout only.

### G6 THE GUARDS, THE SUITE AND THE TREE

(a) exit 0

    python3 -B -m pytest tests/orchestration/test_development_artifact_boundary.py \
      tests/orchestration/test_cluster_deletion_map.py \
      tests/orchestration/test_import_reachability.py \
      tests/orchestration/test_cluster_deletion_order.py \
      tests/orchestration/test_orchestrator_brain.py \
      tests/orchestration/test_self_dogfood.py \
      tests/orchestration/test_self_dogfood_execution.py -q
    69 passed in 6.56s
    REAL_EXIT=0

The reviewer's applied run gave 69 passed at exit 0; reproduced exactly.

(b) THE CANARY — exit 0

    python3 -B -m pytest tests/cli/test_golden_path.py -q
    42 passed in 19.38s
    REAL_EXIT=0

(c) THE DOCUMENTATION GATE — exit 0

    python3 -B -m pytest tests/docs/ -q
    303 passed in 0.65s
    REAL_EXIT=0

(d) THE FULL SUITE, SERIALLY, IN THE PRIMARY CHECKOUT with C4 committed — exit 0

    python3 -B -m pytest tests/ -q
    18552 passed, 23 skipped, 1 warning in 1380.70s (0:23:00)
    REAL_EXIT=0

    python3 -B -m pytest tests/ -q --collect-only
    18575 tests collected in 17.18s
    REAL_EXIT=0

    passed + skipped = 18552 + 23 = 18575 = collected.  ZERO failed.

THE ARITHMETIC AGAINST THE BASE, measured rather than hand-waved. The base
`c4c314c2` was re-collected in a read-only worktree: 18626 collected, and the two
deleted test files collected 46 tests there
(`tests/orchestration/test_overnight_executor.py` +
`tests/cli/test_overnight_executor_cli.py`, one collect-only run). This round
also deletes FIVE test functions — `TestDecisionQuality::test_open_blocker_forces_human_review`,
`TestModelRouting::test_open_blocker_high_human_review`,
`TestInspection::test_pending_review_is_blocker`,
`TestInspection::test_open_blocker_finding`,
`TestEligibility::test_pending_review_blocks` — and RE-BASES one, which changes no
count. So 18626 − 46 − 5 = 18575, which is the measured collection exactly, and
the skip count is unchanged at 23.

(e) RUFF over every `.py` path in this round's change set — exit 0

    python3 -B -m ruff check apps/cli/command_catalog.py apps/cli/commands/overnight_cmd.py \
      packages/orchestration/orchestrator_brain.py packages/orchestration/self_dogfood.py \
      packages/orchestration/self_dogfood_execution.py \
      tests/orchestration/test_cluster_deletion_map.py \
      tests/orchestration/test_development_artifact_boundary.py \
      tests/orchestration/test_orchestrator_brain.py tests/orchestration/test_self_dogfood.py \
      tests/orchestration/test_self_dogfood_execution.py
    All checks passed!
    REAL_EXIT=0

Repo-wide, `python3 -B -m ruff check` reports 26 errors at HEAD and 26 at base
`c4c314c2` (measured in a read-only worktree), none of them in a file this round
touches. The block states 13; that numeral does not reproduce and is DEVIATION 2
below. The binding condition — exit 0 over the change set, and zero errors added —
holds.

(f) THE TREE

    ls -la .agent/STOP            -> No such file or directory (re-read from disk at C4)
    git status --porcelain        -> (empty)
    git worktree list             -> /home/decodeux/Repos/remedy  ead50596 [feature/f275-one-world-completion-part-three]
    git branch --show-current     -> feature/f275-one-world-completion-part-three

    git diff --name-only eeb3cdfe..ead50596 against the block's C4 path set:
      block C4 path set : 24
      measured C4 paths : 24
      MISSING : []
      EXTRA   : []
      EXACT MATCH: True

Per-commit insertions for every commit BEFORE C5, each single-parent, against the
AGENTS.md DECISION F104 D1 cap of 500 insertions:

    | Commit   | insertions | deletions | parents | cap 500 |
    |----------|-----------|-----------|---------|---------|
    | ec9d8cf8 | 430       | 0         | 1       | OK      |
    | 726cc79a | 409       | 233       | 1       | OK      |
    | 97f5a618 | 20        | 23        | 1       | OK      |
    | 2bf8a0a0 | 10        | 0         | 1       | OK      |
    | eeb3cdfe | 66        | 0         | 1       | OK      |
    | ead50596 | 27        | 1993      | 1       | OK      |

C5's own numbers are not reported here; the reviewer books them (§3 item 14).

(g) The `+/-` cells of the `## Commits` tables above were compared CELL BY CELL
against `git show --numstat` per commit and they AGREE on all 30 rows (§3 item 28).

### G7 THE RATCHETS AGREE WITH THE DISK — exit 0

    .agent/f275_deletion_order.md, non-comment lines: 3, in the regenerated order
      packages.orchestration.overnight_readiness
      packages.orchestration.worker_registry
      packages.orchestration.provider_trust, packages.orchestration.provider_trust_verification
    recorded_order() == measured_order() from the LIVE import graph : True
    tests/orchestration/cluster_deletion_map.txt lines naming overnight_executor : 0
    tests/orchestration/import_reachability_allowlist.txt lines naming it        : 0
    CLUSTER_MODULES read through the SHIPPED reader: 4 members, and
      "packages.orchestration.overnight_executor" in CLUSTER_MODULES -> False
    The 26-line header of the order file is UNCHANGED at sha256
      aff913e6eedb4d9c7e5ab6e76578be881ffffa3612018cf58b5a48ad508b0cc2 — the file
      was REGENERATED from the live graph, header preserved, not line-edited.

## Authored-text proofs

Four reviewer-authored slices, all extracted from the COMMITTED C0a blob
`ec9d8cf8:.agent/authored/f275-r18.md` between their marker lines, markers
excluded, and applied without retyping. No marker line reached any target file
(checked on each target after writing).

| Slice | bytes | sha256 | target | result |
|---|---|---|---|---|
| PLAN18 | 2338 | 4640c33788ca986944885badb88f9476be1f4be83803b86a87bfe96e9ebca7e2 | `.agent/plan.md`, replaced WHOLE | file byte-identical to the slice |
| LEDGER18 | 6627 | 738f017c803f0374a550e3920a3384e4f141c9fed1337764a6657c7a0be37374 | `.agent/live_review.md`, appended | byte-exact suffix, 4 paragraphs equal in order |
| SLIPS18 | 954 | 21417814e68430b3e49c405db8db1dcd6cc84b153081b19a4680e75f9176a435 | `.agent/prose_slips.md`, appended | byte-exact suffix, 1 paragraph equal |
| DECISION18 | 4927 | 93a1b428bfde7c4a3aba9f08ad6bcb7236d1e5cb3c897afe50619e1f4e4042ea | `.agent/decisions.md`, appended | occurs exactly once, site re-hashes to the slice digest |

## Deviations & assumptions

The block's ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5 was followed
EXACTLY: six commits before the handback, in that order, none added, none
dropped, none reordered.

**DEVIATION 1 — G4's survivor classification is THREE classes, not the ONE the
block predicts.** The block states "The reviewer's applied run left exactly one
class of survivor: prose in `docs/roadmap/features/` naming the deletion as
history … A hit anywhere else is a violation." My measured RAW list has 9 lines
in three classes (printed in full above): 3 of the predicted class, 5 English-phrase
matches on the spaced token `overnight run`, and 1 stale string in
`tests/cli/test_product_spine.py:145`. ALL SIX of the unpredicted lines are
byte-identical at base `c4c314c2`, so this round introduced none of them; the
violation set FELL from 73 to 6. I did NOT touch `tests/cli/test_product_spine.py`
— block constraint 2 forbids touching a path the block does not name, and the
suite is not red on it (the assertion is negative and still passes). This is
declared rather than routed around, per the block's sanctioned move.

**DEVIATION 2 — the block's ruff baseline numeral does not reproduce.** The
block states "The base carries 13 pre-existing ruff errors in files this round
does not touch". Measured: 26 at base `c4c314c2` and 26 at HEAD, none in a file
this round touches. The binding condition (exit 0 over the change set) holds and
this round adds zero. Non-load-bearing; a candidate `.agent/prose_slips.md` line
for the reviewer to author, not for me to write.

**DEVIATION 3 — three readerless leftovers deleted inside paths the block DOES
name.** R-0855's fix clause binds every deletion round of this feature to sweep
what the anchor leaves readerless, and the R16 precedent sustains deleting them
inside a named path. Deleted beyond the block's literal enumeration:
(a) in `packages/orchestration/self_dogfood.py`, the section banner
`# Live review parser reuse (Step 1402)` whose only member was `_review_findings`;
(b) in `packages/orchestration/orchestrator_brain.py`, `_agent_dir()`, whose ONLY
caller was the deleted `_review_state` — a repo-wide grep of `packages/`, `apps/`
and `tests/` returns its definition and nothing else after the deletion;
(c) in `packages/orchestration/orchestrator_brain.py`, the comment
`# Open blocker/high review forces human-review: execution-like options unsafe.`
which sat directly above the deleted `_score_options` branch. All three are inside
files the block's change set names.

**DEVIATION 4 — one enum member deliberately NOT deleted.**
`StopReason.REVIEW_FINDINGS_OPEN` in `packages/orchestration/self_dogfood_execution.py`
now has no reader inside its own module. It was KEPT: the block enumerates exactly
what leaves that file (`_review_blocks` and the review-gate call site) and an enum
member is a value in a serialized contract rather than a readerless helper, so
removing it is a scope widening the block does not authorise. The same name
survives independently in `packages/orchestration/overnight_readiness.py`, which
is component 3 and not this round. Flagged so the round that deletes
`overnight_readiness` can decide both at once.

**DEVIATION 5 — the ambiguous-selection test was re-based with a WIDENED helper,
as ordered, and its assertion's PATH to the branch changed.**
`_job` gained a `failures=1` keyword (the block: "Widen the `_job` helper with a
count rather than writing a second helper") and the test now asks for two
unresolved failures instead of writing a synthetic review file. The assertion
itself — `stop_reason == "ambiguous_selection"` and no proposed tasks — is
unchanged, and G5 probe P3 proves the re-based node still bites.

**ASSUMPTION.** The block's G4 sweep phrase "the command id `overnight.run` in
both its dotted and its spaced form" was read as the two literal tokens
`overnight.run` and `overnight run`. The looser reading (`remedy overnight run`)
would have hidden the five English-phrase lines; the stricter reading was taken
so nothing is hidden, and the raw list is printed with the classification above.

## Item-status table

Every ordered item of the block's bundle and change set appears exactly once.

| Item | Status | Reason |
|---|---|---|
| C0a save the block to `.agent/authored/f275-r18.md` | done | |
| C0b mirror it into `.agent/last_block.md` | done | |
| C1 `.agent/plan.md` <- PLAN18, replaced WHOLE | done | |
| C2 `.agent/live_review.md` <- LEDGER18 | done | |
| C2 `.agent/prose_slips.md` <- SLIPS18 | done | |
| C3 `.agent/decisions.md` <- DECISION18, before the first `git rm` | done | |
| C4 the module group, ONE commit, never split | done | |
| C5 the handback | done | this commit |
| DELETE `packages/orchestration/overnight_executor.py` | done | |
| DELETE `tests/orchestration/test_overnight_executor.py` | done | |
| DELETE `tests/cli/test_overnight_executor_cli.py` | done | |
| DELETE `docs/system/bounded-overnight-executor-v0.md` | done | |
| EDIT `apps/cli/commands/overnight_cmd.py` | done | file survives with its other three commands |
| EDIT `apps/cli/command_catalog.py` | done | no `related=` tuple named `overnight.run`; re-measured |
| EDIT `packages/orchestration/self_dogfood.py` | deviated | plus the readerless section banner — DEVIATION 3(a) |
| EDIT `packages/orchestration/self_dogfood_execution.py` | deviated | `StopReason.REVIEW_FINDINGS_OPEN` deliberately kept — DEVIATION 4 |
| EDIT `packages/orchestration/orchestrator_brain.py` | deviated | plus `_agent_dir` and one dead comment — DEVIATION 3(b), 3(c) |
| DELETE 2 tests in `test_orchestrator_brain.py` | done | |
| DELETE 2 tests in `test_self_dogfood.py` | done | |
| RE-BASE `test_propose_ambiguous_requires_selection` | deviated | helper widened as ordered — DEVIATION 5 |
| DELETE 1 test in `test_self_dogfood_execution.py` | done | |
| EDIT `tests/orchestration/test_development_artifact_boundary.py` | done | other five `_ALLOWED_LEGACY` entries left alone |
| EDIT `docs/system/development-artifact-boundary-v0.md` | done | |
| EDIT `tests/orchestration/test_cluster_deletion_map.py` | done | |
| EDIT `tests/orchestration/cluster_deletion_map.txt` | done | three lines |
| EDIT `tests/orchestration/import_reachability_allowlist.txt` | done | |
| REGENERATE `.agent/f275_deletion_order.md` | done | header preserved, order re-derived from the live graph |
| SWEEP the advertisements across the six named `docs/` pages | done | seven references removed, one dangling sentence deleted |
| G1 TRANSPORT | done | exit 0 |
| G2 THE PLAN AND THE DECISION SLICE | done | exit 0 |
| G3 THE RECORD over two appends | done | exit 0 |
| G4 THE SWEEP IS CLEAN | deviated | sweep exit 0 and guard exit 0, but three survivor classes — DEVIATION 1 |
| G5 THE RED-PROOFS | done | P2 and P3 held; P1 reported green as ordered |
| G6 THE GUARDS, THE SUITE AND THE TREE | deviated | all exit 0; the block's ruff baseline numeral does not reproduce — DEVIATION 2 |
| G7 THE RATCHETS AGREE WITH THE DISK | done | all four measurements hold |

## Open findings

    open 86 by DISTINCT id, against 92 registered and 6 resolved, `Landed:` lines
    never subtracted (34 distinct `Landed:` ids are present in the record).

Round 18 resolved R-0861 and registered R-0862 and R-0863, so the set moved
85 -> 86, exactly as `.agent/plan.md` states. Four are High — R-0803, R-0804,
R-0806 and R-0807 — all F273's rather than this feature's, per DECISION F272 D12.

## Next

Review the range `c4c314c2`..`HEAD`, re-run all seven gates against the committed
blobs, and issue the round 18 verdict. The next round's work is the
`overnight_readiness` component, which the regenerated
`.agent/f275_deletion_order.md` now names on its FIRST line, ahead of
`worker_registry`; it also carries the three surviving `overnight` commands and
their handler file `apps/cli/commands/overnight_cmd.py`. Before authoring it,
re-read `.agent/STOP` from disk — Phase 1 rule 1 before rule 2.
