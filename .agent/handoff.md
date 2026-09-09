# Handback — F275 round 19

## Session

SESSION 10 of feature F275 · round 19 · rounds so far 19

F275's soft limit is 20 sessions and 60 rounds by operator amendment
amend0908-f275-finish rule 1, and it travels to no other feature. This round is
well inside it, so no scope report is owed.

This was a DELETION round: the THIRTEENTH module group of the prototype cluster,
`packages.orchestration.overnight_readiness`, component 1 of
`.agent/f275_deletion_order.md`, in ONE commit. It takes the WHOLE `overnight`
command group with it — the `GroupDef`, the three remaining read-only commands,
the handler file round 18 left alive, and two test files — because
`packages/orchestration/mission_readiness.py` has carried the same capability
since rounds 1 and 2. It first booked round 18's PASS verdict and the R-0864
registration from the pushed `.agent/handoff.md`, per amend0827-process-diet
rule 1, and two prose slips. There was no DECISION commit: DECISION F275 D1
already ruled the carry-over and DECISION F274 D2 already ruled the naming.

Context self-assessment (amend0905-throughput): context is comfortable; the
round's cost was dominated by the 21-minute serial full suite and by the two
read-only base worktrees the reconciliation arithmetic needed, not by reading.

## Range

Review of `c878073e`..`HEAD` (C4, the commit that writes this file).

## Commits

### f172303d F275 R19 C0a: save the round 19 step block verbatim.
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f275-r19.md | +310 -0 | the round 19 step block saved verbatim; the C0a blob every authored slice is extracted from |

### a211cea3 F275 R19 C0b: mirror the round 19 block into the last-block state file.
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +246 -366 | the same bytes mirrored into the standing state file, written from the committed C0a blob |

### 0b9c05d1 F275 R19 C1: advance the plan to round 19.
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +15 -15 | replaced WHOLE by the PLAN19 slice; Current Step is round 19, Risks names R-0847 as this round's worst |

### ddaf9101 F275 R19 C2: book the round 18 PASS verdict, register R-0864, record two prose slips.
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4 -0 | LEDGER19 appended: the reviewer-authored round 18 PASS verdict and the R-0864 registration |
| .agent/prose_slips.md | +4 -0 | SLIPS19 appended: the two round 18 reviewer-prose slips |

### 0f19c86a F275 R19 C3: delete the overnight_readiness module group and its whole command group.
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/overnight_readiness.py | +0 -894 | the module itself; its capability has been carried by `mission_readiness.py` since rounds 1 and 2 |
| apps/cli/commands/overnight_cmd.py | +0 -81 | the handler file dies ENTIRELY; round 18 took its fourth command, all three remaining go now |
| tests/orchestration/test_overnight_readiness.py | +0 -259 | the module's own tests, deleted with the module (22 test functions) |
| tests/cli/test_overnight_cli.py | +0 -105 | the command group's CLI tests, deleted with the group (7 test functions) |
| apps/cli/command_catalog.py | +0 -43 | the `"overnight"` GroupDef, the three `CommandEntry` blocks and the section comment that introduced them |
| apps/cli/commands/__init__.py | +1 -2 | `overnight_cmd` dropped from BOTH the sorted import block and the dispatcher tuple |
| packages/orchestration/mission_readiness.py | +3 -3 | the surviving twin's docstring: the two sentences claiming the module is "still on disk" rewritten in the PAST tense, naming F275 round 19 |
| tests/orchestration/test_job_fulfillment.py | +3 -3 | three `_integrity_status` imports re-pointed from the dying module to `mission_readiness`, which carries the definition; nothing copied |
| tests/orchestration/test_cluster_deletion_map.py | +0 -2 | the module dropped from `CLUSTER_MODULES` and the handler from `CLUSTER_COMMAND_HANDLERS` |
| tests/orchestration/import_reachability_allowlist.txt | +0 -2 | TWO lines, the module and the handler; the dry run went red on exactly the second |
| .agent/f275_deletion_order.md | +0 -1 | REGENERATED from the live import graph, not line-edited; two component lines remain |
| docs/archive/bounded-overnight-prep-v0.md | +0 -6 | the three dead `remedy overnight …` advertisements and the line introducing them; the archive page stays |
| docs/system/quality-baseline-v0.md | +0 -1 | the coverage-table row for the deleted handler file |

### C4 — the commit that writes this file
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | (self-reference) | this handback; a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/wt-r19 HEAD` | exit 0 — the disposable worktree for the G5 red-proof |
| `git worktree remove --force .remedy-wt/wt-r19` + `git worktree prune` | exit 0 — removed and pruned before C4 |
| `git worktree add --detach .remedy-wt/wt-base c878073e` (twice) | exit 0 — READ-ONLY base worktrees, once for the base `--collect-only` node-id set and once for the base ruff parity total |
| `git worktree remove --force .remedy-wt/wt-base` + `git worktree prune` (twice) | exit 0 — both removed and pruned before C4 |
| `git push -u origin feature/f275-one-world-completion-part-three` | run ONCE, after C4 — see Next |
| PR create / merge / any `gh` command | None — forbidden by the block |

## Verification

One line per gate, with its REAL exit code taken from
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`.

**G1 TRANSPORT — REAL_EXIT=0.** One digest comparison over the three artefacts
§3 item 37 covers and nothing else:

| Artefact | bytes | sha256 |
|---|---|---|
| `.remedy-wt/f275-r19.md` (delegation source) | 25581 | `8b40fbd855485160db7aef589b2c49f51a8bcf1f543ae375280d8e5e82afdee8` |
| committed `.agent/authored/f275-r19.md` | 25581 | `8b40fbd855485160db7aef589b2c49f51a8bcf1f543ae375280d8e5e82afdee8` |
| committed `.agent/last_block.md` | 25581 | `8b40fbd855485160db7aef589b2c49f51a8bcf1f543ae375280d8e5e82afdee8` |

ALL THREE BYTE-EQUAL: True.

**G2 THE PLAN AND THE SURVIVOR'S DOCSTRING — REAL_EXIT=0.** The block's TOTAL
line count is 310 against its cap of 490. `.agent/plan.md` at C1 is 2259 bytes,
sha256 `7278e1538a08a2a71d4b91972123e468d0393cc369db8de80f23cd37b7f57461`,
BYTE-IDENTICAL to the PLAN19 slice extracted from the committed C0a blob
(same length, same digest), 41 lines against the AGENTS.md cap of 50, with
`## Goal` exactly once and `## Next Steps` exactly once, and no marker line
present. For `packages/orchestration/mission_readiness.py` the numstat of the
docstring edit is `3	3	packages/orchestration/mission_readiness.py`. The module
docstring occupies lines 1..17 of the new file (measured with `ast`, not by eye);
old and new both have 745 lines; the line-by-line comparison gives changed line
numbers `[14, 15, 16]`, so ALL CHANGED LINES ARE INSIDE THE MODULE DOCSTRING and
no line outside it changed. The F261-renames sentence is byte-identical.

```
-two consumers are why `packages/orchestration/overnight_readiness.py` has no
-surviving consumer left. That module is still on disk and is deleted with its
-cluster group; it was never touched by this move.
+two consumers were why `packages/orchestration/overnight_readiness.py` had no
+surviving consumer left. F275 round 19 deleted that module with its cluster group;
+it was never touched by this move.
```

**G3 THE RECORD, over TWO appends — REAL_EXIT=0.**

`.agent/live_review.md` <- LEDGER19:
- (a) BYTE READER: pre 666602 bytes sha256 `4545982f94b952a44485f13980818c89bc3d3d961de3eb40258d7ef0b3e178ac`;
  post 671839 bytes sha256 `25bec09abaa522554b47314afd0a4e206f9eacc9bd396a81db0dc2c3d4fd9e0c`;
  slice 5236 bytes sha256 `514b21de7edabc2db5e116b707bce2178ad87818ff917314a73280461cfe58ea`;
  growth 5237 == 1 + 5236; pre a byte-exact PREFIX: True; slice a byte-exact
  SUFFIX: True; joining byte read back as `b'\n'`: True.
- (b) STRUCTURAL READER: N COUNTED BY THE SCRIPT FROM THE SLICE = 2. The
  post-file holds 265 blank-line units; its LAST 2 units match the slice's 2
  paragraphs IN ORDER, per-unit sha256 on both sides:
  `18034a8415ebd1aa7fbc8c7917ce511da1db3a47cd06ff02040c170474aec5ab` and
  `25ed378e6003f017498cb1028254c132482550379b13b36607e2fc3e30d4ca90`. The unit
  before them, `a3150de78a61494b41fd7fb16fe5d0f6089cc7d41ae33205268d086a45421de3`,
  is inside the PRE blob, so the region is whole and not just its tail.
- (c) NEGATIVE CONTROL: one byte flipped IN MEMORY at file offset 666643, inside
  the FIRST appended paragraph. Byte reader REJECTED the mutant (suffix False),
  structural reader REJECTED it (tail != slice paragraphs); both readers ACCEPT
  the truth; re-read from disk equals the committed post-blob (same sha256).
- (d) COUNT PATTERNS: `^Gate: ` rose 40 -> 41; `^Gate: F275 R18 ` 0 -> 1 (exactly
  once); `^- R-0864 — ` 0 -> 1 (exactly once).
- (e) THE OPEN SET BY DISTINCT ID, `Landed:` never subtracted: at base
  `c878073e` registered 92, done 6, open 86, with 34 distinct `Landed:` ids —
  THE BASE REPRODUCES EXACTLY. At C2: registered 93, done 6, OPEN 87, 34 distinct
  `Landed:` ids.

`.agent/prose_slips.md` <- SLIPS19:
- (a) BYTE READER: pre 192846 bytes sha256 `c36e22a9669bdcba66f6139f5417d8084532816af67626f52ad2083748b9ac2b`;
  post 194749 bytes sha256 `93c5b2a59acdb309a679e037899a6927858611a552264945ff0b1439fe1f6b34`;
  slice 1902 bytes sha256 `68a92776d553171e953ea1a1f4b1d1b7858a2b709bf2fc7c02b7597748a354eb`;
  growth 1903 == 1 + 1902; prefix True; suffix True; joining byte `b'\n'`.
- (b) STRUCTURAL READER: N = 2 counted from the slice; 278 units in the post-file;
  last 2 match in order, `30b7193911994834d34f97d3f6a356c816323d0aec2d665410202386666c7f59`
  and `a1dd14b0286b65c7487ae2c0784a63e10fd0d0c76618bcc4ed36df8e24438b33`; the
  preceding unit `d378dab1bb61070f33cbde93c0d6eaae6887c1dcf1f02c5bcf59db8fb27e8222`
  is inside the PRE blob.
- (c) NEGATIVE CONTROL: byte flipped at offset 192887 inside the FIRST appended
  paragraph; BOTH readers rejected the mutant and accepted the truth; disk equals
  the committed post-blob.

**G4 THE SWEEP IS CLEAN — REAL_EXIT=0.** 1668 tracked files scanned (of 4557
tracked; `.agent/` and `.data/` excluded), over exactly the seven ordered tokens
`packages.orchestration.overnight_readiness`, `overnight_readiness.py`,
`overnight_cmd`, `overnight.readiness`, `overnight.plan`, `overnight.report` and
the spaced form `remedy overnight`. THE RAW LIST IN FULL, UNTRUNCATED — RAW = 6:

```
docs/roadmap/features/T2_F260.md:343: [overnight_readiness.py] `overnight_readiness.py`, `repair_loop_v2.py`, `dogfood_run.py`,
docs/roadmap/features/T2_F260.md:359: [overnight_readiness.py] (`overnight_readiness.py`: capabilities, risks, budget and evidence summaries)
docs/roadmap/features/T2_F272.md:744: [overnight_readiness.py] FIRST — THE TWELVE CLUSTER-BOUND CONSUMERS ARE NEVER MIGRATED. Cross-referencing the inventory's 72 production consumers against the 24-module cluster list in `docs/roadmap/features/T2_F260.md`'s Design section gives twelve files on both: `builder_routing.py`, `candidate_quality.py`, `dogfood_run.py`, `external_builder_sandbox.py`, `local_candidate_generator.py`, `overnight_executor.py`, `overnight_mission.py`, `overnight_readiness.py`, `provider_trust.py`, `provider_trust_verification.py`, `repair_loop_v2.py` and `review_bundle.py`. Porting any of them onto the unified record is work T005 throws away. They keep their classic-store imports until T005 deletes them, and no round spends a line on them. T004's real remaining size is therefore 60 production files beside the 127 under `tests/`, and that is the figure a scope report uses rather than the headline 199.
packages/orchestration/mission_readiness.py:7: [overnight_readiness.py] in `packages/orchestration/overnight_readiness.py`, so the move is provable by a
packages/orchestration/mission_readiness.py:14: [overnight_readiness.py] two consumers were why `packages/orchestration/overnight_readiness.py` had no
tests/cli/test_mission_cmd.py:1421: [packages.orchestration.overnight_readiness] assert "packages.orchestration.overnight_readiness" not in source
```

Line by line, why each survivor is legitimate:
1. `docs/roadmap/features/T2_F260.md:343` — history prose: F260's Design section
   listing the cluster's modules as they stood. Byte-identical at the base.
2. `docs/roadmap/features/T2_F260.md:359` — history prose, same class, same
   section, describing what the module used to carry. Byte-identical at the base.
3. `docs/roadmap/features/T2_F272.md:744` — history prose: F272's ruling naming
   the twelve cluster-bound consumers it would never migrate. Byte-identical at
   the base.
4. `packages/orchestration/mission_readiness.py:7` — the surviving twin's
   docstring sentence recording that each definition is a byte-identical move of
   the definition of the same name in the deleted module. The block ordered every
   sentence outside the two rewritten ones kept BYTE-IDENTICAL, so this line is
   legitimate by the block's own instruction.
5. `packages/orchestration/mission_readiness.py:14` — the first of the two
   sentences THIS ROUND REWROTE, now in the past tense.
6. `tests/cli/test_mission_cmd.py:1421` — the ratchet the block declares NOT
   TOUCHED: it keeps `mission_cmd` off the cluster and stays GREEN. R-0864's fix
   clause already routes it.

No hit outside those classes. The spaced form `remedy overnight` returns ZERO
hits, so the three advertisements in `docs/archive/bounded-overnight-prep-v0.md`
were the last ones on disk.

`python3 -B -m pytest tests/cli/test_advertised_commands.py -q` — 5 passed,
REAL_EXIT=0. **STATED PLAINLY, AS THE BLOCK REQUIRES: THAT PASS IS NOT EVIDENCE
FOR THIS ROUND.** Deleting the whole group removed `"overnight"` from that
guard's `GROUPS`, and the guard skips what it cannot resolve, so it went BLIND to
every `remedy overnight <sub>` advertisement at exactly the moment those
advertisements went dead — finding R-0847. The evidence for the advertisements is
the hand-read RAW list above, not this exit code.

**G5 THE SURVIVOR IS STILL PINNED — control REAL_EXIT=0, mutation REAL_EXIT=1,
post-revert REAL_EXIT=0.** Run entirely inside the disposable worktree
`.remedy-wt/wt-r19` at C3 (`0f19c86a`), never in the primary checkout.

- REVERT TARGET NAMED BY PATH:
  `/home/decodeux/Repos/remedy/.remedy-wt/wt-r19/packages/orchestration/mission_readiness.py`.
  The mutated bytes — the six-line `def build_overnight_readiness(...)` signature
  through its docstring line — occur EXACTLY ONCE in that file (measured before
  mutating: `anchor occurrences in that file: 1`).
- Sanity probe before any run: inside the worktree,
  `import packages.orchestration.mission_readiness` resolves to
  `…/.remedy-wt/wt-r19/packages/orchestration/mission_readiness.py`, so the
  editable install at `/home/decodeux/.local/lib/python3.10/site-packages/_editable_impl_remedy.pth`
  (which puts the PRIMARY checkout on `sys.path`) does not shadow the worktree.
  The mutation going red is the second, decisive proof of that.
- CONTROL FIRST, unmutated, over the same node set in the same worktree:
  `python3 -B -m pytest tests/orchestration/test_mission_readiness.py tests/cli/test_mission_cmd.py -q`
  → last summary line `128 passed in 45.62s`, REAL_EXIT=0.
- MUTATION — `build_overnight_readiness` made to raise immediately
  (`raise RuntimeError("G5 MUTATION: build_overnight_readiness is disabled")` as
  its first statement), `__pycache__` purged, `python3 -B`:
  → last summary line `16 failed, 112 passed in 45.94s`, REAL_EXIT=1. Named
  failures include
  `tests/cli/test_mission_cmd.py::TestMissionReadinessIsWiredToTheCarriedModule::test_the_cockpit_reads_the_carried_module_and_says_so`
  and
  `tests/cli/test_mission_cmd.py::TestMissionReportIsTheCarriedReportView::test_the_real_cli_answers_with_the_carried_report`.
- REVERTED by path, `__pycache__` purged, re-run:
  → `git status --porcelain` in the worktree empty, last summary line
  `128 passed in 45.77s`, REAL_EXIT=0.

THE STOP CONDITION DID NOT FIRE: the mutation is RED, so the carry-over is
genuinely pinned — the carried module, not the deleted one, is what serves
`remedy mission readiness` and `remedy mission report`, and it is still covered
after its twin is gone.

**G6 THE GUARDS, THE SUITE AND THE TREE.**

- (a) `python3 -B -m pytest tests/orchestration/test_cluster_deletion_map.py
  tests/orchestration/test_cluster_deletion_order.py
  tests/orchestration/test_import_reachability.py
  tests/orchestration/test_job_fulfillment.py
  tests/orchestration/test_mission_readiness.py tests/cli/test_mission_cmd.py
  tests/cli/test_advertised_commands.py tests/test_grouped_cli.py
  tests/cli/test_cli_ux.py -q` → `716 passed in 93.69s`, REAL_EXIT=0, run at C3
  committed. Exactly the reviewer's applied-run figure of 716.
- (b) the canary, `python3 -B -m pytest tests/cli/test_golden_path.py -q` →
  `42 passed in 19.11s`, REAL_EXIT=0.
- (c) `python3 -B -m pytest tests/docs/ -q` → `303 passed in 0.48s`, REAL_EXIT=0
  (verification tier 5: this round's change set includes `docs/` pages).
- (d) THE FULL SUITE, `python3 -B -m pytest tests/ -q`, SERIALLY, in the PRIMARY
  checkout with C3 committed → `18515 passed, 23 skipped, 1 warning in 1265.04s
  (0:21:05)`, ZERO failed, REAL_EXIT=0. Separate `--collect-only`:
  `18538 tests collected`, REAL_EXIT=0. 18515 + 23 = 18538 = collected. THE
  ARITHMETIC AGAINST THE BASE: base 18552 passed / 23 skipped / 18575 collected;
  the fall is 37 in passed and 37 in collected. The two deleted test files hold
  only 29 test functions (22 in `test_overnight_readiness.py`, 7 in
  `test_overnight_cli.py`, none parametrized), so 8 were unaccounted for. MEASURED
  by a node-id set diff of `--collect-only` at the base (read-only worktree at
  `c878073e`, 18575 ids) against C3 (18538 ids): the 37 removed ids are 22 +
  7 + EIGHT parametrized `[overnight]` cases in `tests/test_grouped_cli.py`
  (`test_group_help_flag[overnight]`, `test_group_help_has_commands_box[overnight]`,
  `test_group_help_has_options[overnight]`, `test_group_help_has_usage[overnight]`,
  `test_group_help_lists_subcommands[overnight]`,
  `test_group_help_exits_zero[overnight]`,
  `test_help_no_sensitive_leaks[overnight]`,
  `test_main_entrypoint_delegates_group_help_to_grouped_cli[overnight]`) — those
  are parametrized over the catalog's `GROUPS` and die with the `GroupDef`.
  22 + 7 + 8 = 37, and NO node id was ADDED. See the deviations.
- (e) `python3 -B -m ruff check` over every `.py` path in this round's change set
  (`apps/cli/command_catalog.py`, `apps/cli/commands/__init__.py`,
  `packages/orchestration/mission_readiness.py`,
  `tests/orchestration/test_cluster_deletion_map.py`,
  `tests/orchestration/test_job_fulfillment.py`) → `All checks passed!`,
  REAL_EXIT=0. PARITY over `packages/`, `apps/` and `tests/`: at base `c878073e`
  `Found 24 errors.` REAL_EXIT=1; at C3 `0f19c86a` `Found 24 errors.`
  REAL_EXIT=1. The per-file distribution is IDENTICAL at both revisions (6 in
  `tests/cli/test_plan_approval.py`, 2 each in `tests/test_project_context_coverage.py`,
  `tests/orchestration/test_prompt_trace.py`, `tests/orchestration/test_long_run_executor.py`,
  and 1 each in twelve further files, of which two are under `packages/`), and NOT
  ONE of them is in a file this round touches. The round ADDED none. The
  pre-existing 24 were not fixed, as ordered.
- (f) THE TREE. `.agent/STOP` re-read from disk: does not exist.
  `git status --porcelain`: EMPTY. `git worktree list`: one entry only,
  `/home/decodeux/Repos/remedy  0f19c86a [feature/f275-one-world-completion-part-three]`.
  Branch: `feature/f275-one-world-completion-part-three`.
  `git diff --name-only ddaf9101..0f19c86a` yields 13 paths;
  against the block's C3 path set of 14: **MISSING = {`tests/orchestration/cluster_deletion_map.txt`}**,
  **EXTRA = {} (empty)**. The single missing path is the declared deviation below.
  Per-commit insertions before C4, against the DECISION F104 D1 cap of 500:

  | Commit | parents | + | - | under cap |
  |---|---|---|---|---|
  | f172303d | 1 | 310 | 0 | yes |
  | a211cea3 | 1 | 246 | 366 | yes |
  | 0b9c05d1 | 1 | 15 | 15 | yes |
  | ddaf9101 | 1 | 8 | 0 | yes |
  | 0f19c86a | 1 | 7 | 1402 | yes |

  Every commit is single-parent. Per §3 item 14, C4's own numbers are not
  reported here.
- (g) The `+/-` cells of the `## Commits` tables above were compared CELL BY CELL
  against `git show --numstat` per commit and THEY AGREE — §3 item 28. The
  numstat output they were checked against:
  `f172303d`: `310 0 .agent/authored/f275-r19.md`.
  `a211cea3`: `246 366 .agent/last_block.md`.
  `0b9c05d1`: `15 15 .agent/plan.md`.
  `ddaf9101`: `4 0 .agent/live_review.md`, `4 0 .agent/prose_slips.md`.
  `0f19c86a`: `0 1 .agent/f275_deletion_order.md`, `0 43 apps/cli/command_catalog.py`,
  `1 2 apps/cli/commands/__init__.py`, `0 81 apps/cli/commands/overnight_cmd.py`,
  `0 6 docs/archive/bounded-overnight-prep-v0.md`, `0 1 docs/system/quality-baseline-v0.md`,
  `3 3 packages/orchestration/mission_readiness.py`,
  `0 894 packages/orchestration/overnight_readiness.py`,
  `0 105 tests/cli/test_overnight_cli.py`,
  `0 2 tests/orchestration/import_reachability_allowlist.txt`,
  `0 2 tests/orchestration/test_cluster_deletion_map.py`,
  `3 3 tests/orchestration/test_job_fulfillment.py`,
  `0 259 tests/orchestration/test_overnight_readiness.py`.

**G7 THE RATCHETS AGREE WITH THE DISK — REAL_EXIT=0.** The component lines now in
`.agent/f275_deletion_order.md`, TWO of them, regenerated from the live graph:

```
packages.orchestration.worker_registry
packages.orchestration.provider_trust, packages.orchestration.provider_trust_verification
```

`tests/orchestration/cluster_deletion_map.txt` holds ZERO lines naming
`overnight_readiness` (0 hits). The reachability allowlist names neither
`packages.orchestration.overnight_readiness` nor `apps.cli.commands.overnight_cmd`
(empty result set). `CLUSTER_MODULES` is now 3 entries and does NOT name this
group's module; `CLUSTER_COMMAND_HANDLERS` is now 8 entries and does NOT name
`apps/cli/commands/overnight_cmd.py`. The catalog's total command count is 233,
`GROUPS` is 46 keys, `"overnight"` is no longer a `GROUPS` key, and the set of
command ids beginning `overnight.` is EMPTY.

## Authored-text proofs

Three reviewer-authored slices were applied this round, each extracted from the
COMMITTED C0a blob (`f172303d:.agent/authored/f275-r19.md`) between its marker
lines, markers excluded, and applied byte for byte without retyping:

| Slice | bytes | sha256 | applied to | result |
|---|---|---|---|---|
| PLAN19 | 2259 | `7278e1538a08a2a71d4b91972123e468d0393cc369db8de80f23cd37b7f57461` | `.agent/plan.md`, replaced WHOLE | `cmp` clean; committed blob byte-identical to the slice (G2) |
| LEDGER19 | 5236 | `514b21de7edabc2db5e116b707bce2178ad87818ff917314a73280461cfe58ea` | `.agent/live_review.md`, appended | byte-exact SUFFIX of the committed post-blob (G3) |
| SLIPS19 | 1902 | `68a92776d553171e953ea1a1f4b1d1b7858a2b709bf2fc7c02b7597748a354eb` | `.agent/prose_slips.md`, appended | byte-exact SUFFIX of the committed post-blob (G3) |

NO MARKER LINE REACHED ANY TARGET FILE: a grep for all six marker strings over
`.agent/plan.md`, `.agent/live_review.md` and `.agent/prose_slips.md` returns 0
for each file.

No verdict, no `Done:` paragraph and no finding of the worker's own was composed.
No `Landed:` line was owed this round: R-0861 was already resolved in round 18,
R-0847 is a guard-blindness finding this round complied with rather than repaired,
and R-0864's fix clause binds the round that next edits
`tests/cli/test_product_spine.py`, which the block declares NOT TOUCHED.

## Deviations & assumptions

1. **`tests/orchestration/cluster_deletion_map.txt` was NOT edited — the ordered
   edit is a no-op on disk.** The block orders "Delete every line beginning
   `packages.orchestration.overnight_readiness <-`". MEASURED at the base
   `c878073e` and again at C3: that file holds ZERO such lines — its ten edge
   lines name only `provider_trust`, `provider_trust_verification` and
   `worker_registry`, which is consistent with the block's own prose that
   `mission_readiness.py` left the dying module with no surviving consumer. So no
   line existed to delete and the file is not in the C3 diff. This is why G6(f)
   reports MISSING = {that path}. I did not touch the file to satisfy the path
   set, and `test_cluster_deletion_map.py` is green in both directions (G6a).
2. **G6(d)'s fall is 37, not the 29 the two deleted test files account for.** The
   remaining 8 are parametrized `[overnight]` cases in `tests/test_grouped_cli.py`
   that are generated from the catalog's `GROUPS` and die with the deleted
   `GroupDef`. The block predicted only that "the count MUST fall" and asked for
   the arithmetic; the arithmetic needed a node-id set diff against a read-only
   base worktree to close, which is the extra measurement recorded under External
   actions. No node id was ADDED anywhere in the suite.
3. **The G4 survivor class in `mission_readiness.py` is TWO docstring LINES, only
   ONE of which this round rewrote.** The block names the class "the two
   `mission_readiness.py` docstring sentences THIS ROUND REWRITES"; on disk the
   RAW list holds line 7 (in the first paragraph, which the block ordered kept
   BYTE-IDENTICAL) and line 14 (the first of the two rewritten sentences). Both
   are legitimate, and the second rewritten sentence no longer carries the token
   at all because it now reads "F275 round 19 deleted that module…". The accurate
   class is "the `mission_readiness.py` module docstring", not "the sentences this
   round rewrites". Nothing was widened; this is a reading of the block's prose
   against the measurement.
4. **The archive advertisement was an INDENTED code block, not a fenced one.**
   The block says "the three-line fenced command block"; on disk
   `docs/archive/bounded-overnight-prep-v0.md` carried a four-space indented
   block. I deleted exactly what the block described — the
   `Commands (all read-only):` line, its following blank line, the three
   `remedy overnight …` lines and the trailing blank line, six lines in total —
   and left the page and all its remaining prose in place.
5. **A pre-existing empty section comment was left in `apps/cli/command_catalog.py`.**
   The line `# ── overnight mission contract (Review/Repair Spine v0) ────` sits
   immediately after the block this round deleted and introduces a DIFFERENT
   (already empty at the base) section. The block names only "the section comment
   that introduces them", so I deleted only
   `# ── overnight (read-only preparation) ───` and left the other one untouched.
   Declaring it so the reviewer does not read it as a missed sweep.
6. **G6(a) was additionally run once BEFORE C3 was committed**, over an identical
   working tree, as the AGENTS.md self-review loop for a deletion of this size. It
   gave the same `716 passed`, exit 0. The figure quoted under G6(a) is from the
   run at C3 COMMITTED, per the block's constraint 7.
7. No `git worktree` was left behind: three were created (one destructive for G5,
   two read-only at the base) and all three were removed and pruned before C4, so
   `git status --porcelain` is empty and `git worktree list` holds one entry.

Assumptions: none beyond the block.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a save the block to `.agent/authored/f275-r19.md` | done | `f172303d`, byte-equal to the delegation source |
| C0b mirror into `.agent/last_block.md` | done | `a211cea3`, written from the committed C0a blob |
| C1 advance `.agent/plan.md` (PLAN19, replaced WHOLE) | done | `0b9c05d1` |
| C2 the record (LEDGER19 + SLIPS19) | done | `ddaf9101` |
| C3 THE MODULE GROUP, one commit, never split | done | `0f19c86a`, one commit, not split |
| C4 the handback | done | this commit |
| DECISION commit | skipped | the block orders none: DECISION F275 D1 already ruled the carry-over, DECISION F274 D2 the naming |
| Delete `packages/orchestration/overnight_readiness.py` | done | -894 |
| Delete `apps/cli/commands/overnight_cmd.py` | done | -81, the whole file |
| Delete `tests/orchestration/test_overnight_readiness.py` | done | -259 |
| Delete `tests/cli/test_overnight_cli.py` | done | -105 |
| Edit `apps/cli/command_catalog.py` | done | GroupDef + three CommandEntry blocks + section comment, -43 |
| Edit `apps/cli/commands/__init__.py` | done | import block AND dispatcher tuple, both |
| Edit `packages/orchestration/mission_readiness.py` docstring | done | past tense, names F275 round 19; no line outside the docstring changed |
| Edit `tests/orchestration/test_job_fulfillment.py` | done | three imports re-pointed, nothing copied |
| Edit `tests/orchestration/test_cluster_deletion_map.py` | done | CLUSTER_MODULES and CLUSTER_COMMAND_HANDLERS, both |
| Edit `tests/orchestration/cluster_deletion_map.txt` | deviated | zero matching lines exist at the base; the ordered deletion is a no-op, file untouched — deviation 1 |
| Edit `tests/orchestration/import_reachability_allowlist.txt` | done | TWO lines, module and handler |
| Regenerate `.agent/f275_deletion_order.md` | done | regenerated from the live graph, not line-edited; two component lines remain |
| Edit `docs/archive/bounded-overnight-prep-v0.md` | done | six lines; page stays — deviation 4 on the "fenced" wording |
| Edit `docs/system/quality-baseline-v0.md` | done | one coverage-table row |
| G1 transport | done | REAL_EXIT=0, all three artefacts byte-equal |
| G2 plan + survivor's docstring | done | REAL_EXIT=0 |
| G3 the record over two appends | done | REAL_EXIT=0, both negative controls rejected |
| G4 the sweep (+ the blind guard) | done | REAL_EXIT=0, RAW = 6, all six classified |
| G5 the survivor is still pinned | done | control 0 / mutation 1 / post-revert 0; STOP condition did not fire |
| G6 guards, suite, tree | done | REAL_EXIT 0 for (a)-(d); (e) 0 over the change set, 1/1 at both revisions for the untouched pre-existing 24 |
| G7 the ratchets agree with the disk | done | REAL_EXIT=0 |

## Open findings

87 by DISTINCT id (registered 93, resolved 6). `Landed:` lines are never
subtracted; 34 distinct ids carry one. Four are High — R-0803, R-0804, R-0806 and
R-0807 — all F273's rather than this feature's, per DECISION F272 D12.

## Next

The planner/reviewer reads the committed range `c878073e`..HEAD, re-runs every
gate itself against the committed blobs and issues the round 19 verdict. Round 20
then deletes `packages.orchestration.worker_registry`, the first line of the
regenerated `.agent/f275_deletion_order.md`. Before authoring it, re-read
`.agent/STOP` from disk (Phase 1 rule 1 before rule 2).
