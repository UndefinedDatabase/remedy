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

## Reviewer verdict on round 19 — appended after the handback, by the reviewer's authored text

VERDICT ROUND 19: **PASS.** Written by the planner and reviewer of SESSION 10 AFTER reading the
committed range `c878073e`..`e3879c82` and RE-RUNNING every gate independently against the
committed blobs; the worker's report was not taken as evidence for any line below. It is carried
here because under `docs/agents/self_drive_protocol.md` a verdict that stays in the session is
lost, and it is booked into `.agent/live_review.md` by the FIRST substantive commit of round 20,
per amend0827-process-diet rule 1.

WHAT THE REVIEWER RE-MEASURED. Six single-parent commits C0a `f172303d`, C0b `a211cea3`, C1
`0b9c05d1`, C2 `ddaf9101`, C3 `0f19c86a` and C4 `e3879c82`, per-commit insertions 310, 246, 15, 8
and 7 for the five before the handback, every one far under the AGENTS.md DECISION F104 D1 cap of
500. G1 IS THE PRIMARY PROOF OF §4 ITEM 9 AND NOT THE DIGEST FALLBACK: the reviewer's own
delegation source and both committed copies are 25581 bytes at
`8b40fbd855485160db7aef589b2c49f51a8bcf1f543ae375280d8e5e82afdee8` and compare BYTE-EQUAL; per §3
item 37 that chain covers those three artefacts and claims nothing about the emitted bytes. G2:
`.agent/plan.md` at C1 is byte-identical to the PLAN19 slice at 41 lines against the cap of 50 with
both mandated headings present; all three slices occur EXACTLY ONCE in their targets and NO marker
line reached any file; and the `mission_readiness.py` edit is THREE lines, every one inside the
module docstring, rewriting the two sentences that claimed the deleted module was "still on disk"
into the past tense naming F275 round 19, with the sentence about F261 owning renames untouched.
G3, over two appends: `^Gate: ` rose 40 to 41, `^Gate: F275 R18 ` and `^- R-0864 — ` each occur
exactly once, and THE OPEN SET WENT 86 TO 87 BY DISTINCT ID against registrations 92 to 93 and
resolutions 6 to 6, with 34 distinct `Landed:` ids present and never subtracted.

G4 IS THE GATE THIS ROUND'S OWN GUARD COULD NOT ANSWER, AND IT IS CLEAN. The reviewer re-ran the
sweep with its own script over the 1668 tracked files outside `.agent/` and `.data/` at
`e3879c82`: RAW 6, printed in full and not truncated, against RAW 11 measured in the applied dry
run before the round. Three are history prose in `docs/roadmap/features/`. The other three are
exactly the classes the block declared legitimate in advance: two `mission_readiness.py` docstring
sentences, one of which this round rewrote, and the `test_mission_cmd.py` ratchet asserting the
cluster module is not imported. The spaced form `remedy overnight` returns ZERO hits, so no page
anywhere still instructs an operator to run a command this round deleted — which is the property
R-0861's fix clause exists to protect and which `tests/cli/test_advertised_commands.py` CANNOT
establish here, because deleting the whole group removed it from that guard's `GROUPS` and the
guard skips what it cannot resolve. The worker ran that guard, got exit 0, and stated in its own
handback that the PASS is not evidence for this round. That is R-0847 being handled correctly
rather than being relied on.

G5's STOP CONDITION DID NOT FIRE, which is the round's most load-bearing single reading: mutating
`build_overnight_readiness` in the SURVIVING `mission_readiness.py` moved its node set from a
control of 128 passed to 16 failed and 112 passed, and back to 128 on revert. The carry-over is
genuinely pinned by tests after its twin's deletion, so the capability F260's Design ordered
carried is demonstrably still covered rather than merely still present.

G6: the affected guards 716 passed, the canary 42, the documentation gate 303, and THE FULL SUITE
WAS RE-RUN BY THE REVIEWER SERIALLY IN THE PRIMARY CHECKOUT and was GREEN at 18515 passed, 23
skipped and ZERO failed, with a separately measured collection of 18538 equal to 18515 plus 23.
Ruff is clean over the change set and carries 24 pre-existing errors at BOTH the base and C3, none
in a file this round touches, so the round adds none. The catalog reads 233 commands in 46 groups
with ZERO ids beginning `overnight.` and the `overnight` group absent; the only `related=` entries
naming a missing id are the two pre-existing ones, `dogfood.run-loop` and `readiness.show`, which
R-0859 already holds open. The tree gate holds: no `.agent/STOP`, porcelain empty, one worktree,
branch correct.

THE SEVEN DECLARED DEVIATIONS ARE ALL SUSTAINED, and the two load-bearing ones are the reviewer's
own errors rather than the worker's. FIRST, the block ordered the deletion of every line in
`tests/orchestration/cluster_deletion_map.txt` beginning `packages.orchestration.overnight_readiness <-`,
and the reviewer has now confirmed at `c878073e` that the file contains no such line and never
mentioned that module at all. The ordered edit was a NO-OP, the worker declined to touch the file
rather than manufacture a change, and that path is therefore the single MISSING entry in the C3
path set. Declining was correct: a named path that needs no edit is a defect of the block, not of
the round. SECOND, the block's suite arithmetic said the count would fall by the contents of two
deleted test files; the real fall is 37, because eight parametrized `[overnight]` cases in
`tests/test_grouped_cli.py` are GENERATED from the catalog `GROUPS` and disappeared with the group.
The worker closed that gap properly, by a node-id set difference of `--collect-only` against a
read-only base worktree showing 22 + 7 + 8 = 37 with NO node id added, which is a stronger reading
than the one the block asked for. The remaining five are sound: the archive advertisement was an
indented rather than a fenced block; only one of the two docstring survivor lines was rewritten
because the block ordered the other paragraph kept byte-identical; a pre-existing empty section
comment was left in the catalog because it introduces a different section the block does not name;
the affected-guards gate was additionally run once before C3 over an identical tree during the
self-review loop; and three worktrees were created and all removed and pruned before the handback.

## Prose slips drafted by session 10, to be appended by round 20's ledger commit

2026-09-09 · F275 R19 · The round 19 block ordered the worker to delete every line of `tests/orchestration/cluster_deletion_map.txt` beginning `packages.orchestration.overnight_readiness <-`, and that file holds no such line and names that module nowhere. The order was carried over by shape from round 18, whose module DID have three such lines, without measuring the file for round 19's module. The reviewer's own dry-run script hid it: the script filtered the lines and printed a completion message unconditionally, so removing zero lines looked exactly like removing three. Nothing landed wrong — the worker declined the no-op and declared it, which left one MISSING path in the round's path set. The lesson is that a filter used as a measurement prints the COUNT it removed, never a fixed message, and that a change-set entry carried over from the previous round's shape is re-measured against this round's subject before it is ordered.

2026-09-09 · F275 R19 · The round 19 block told the worker the suite count "MUST fall" because the round deletes two whole test files, and the real fall was 37 against the 29 those two files hold. The other eight are parametrized `[overnight]` cases in `tests/test_grouped_cli.py` generated from the catalog `GROUPS`, so deleting a command GROUP deletes tests in a file the change set never names. The worker closed the gap by a node-id set difference rather than by arithmetic and showed no node id was added, which is the stronger reading. The lesson is that a round deleting a catalog GROUP predicts its suite delta from the generated cases as well as from the deleted files, because a parametrized suite couples test count to production data and the coupling is invisible in a change set.

## THE ROUND 20 MAP — MEASURED AT `e3879c82`, AND WHY THIS ROUND NEEDS ITS OWN SESSION

THE MODULE: `packages/orchestration/worker_registry.py`, 1035 lines, now the first component line
of `.agent/f275_deletion_order.md`, a SINGLE module. Its group takes six commands —
`worker.registry-list`, `worker.registry-show`, `worker.registry-integrity`, `route-policy.show`,
`route-policy.set` and `route-policy.evaluate` — the handler `apps/cli/commands/route_policy_cmd.py`,
the cockpit section `_build_worker_registry_section` in `ui_server.py` with its dashboard line, and
the `WORKER_REGISTRY_SHOW` member of `ContractAction` in `run_contract.py`.

TWO QUESTIONS ARE ALREADY ANSWERED AND THE NEXT SESSION SHOULD NOT RE-OPEN THEM. FIRST, F260's
SECOND CARRY-OVER IS DISCHARGED: every user-settable route-policy knob was audited against F110's
config keys and none has an equivalent, which F260's Design rules is a FINDING and never a rebuild.
R-0831 is that finding and it is open. SECOND, THIS COCKPIT SECTION IS NOT UNDER A HOLD: DECISION
F274 D4 held exactly two sections, `_build_builder_routing_section` and `_build_overnight_section`,
and DECISION F275 D5 released the first while the second survives on the carried
`mission_readiness`. `_build_worker_registry_section` is neither, so it dies with its module under
T001 RULE 1 and needs no release.

WHAT IS NOT ANSWERED, AND WHY IT IS A DECISION RATHER THAN A MEASUREMENT. The SURVIVING module
`packages/orchestration/token_economy.py` does not merely import a helper from the dying module —
its routing recommendation is built out of it. Measured at `e3879c82`, it imports
`WorkerSelectionRequest`, `evaluate_worker_selection`, `get_worker_spec`,
`hard_safety_requires_approval` and `load_worker_registry` at line 584, `estimate_token_cost_band`
at line 166 and `classify_route_cost` at line 613. One of those is not a convenience:

    worker_registry.py:834  hard_safety_requires_approval(spec) -> bool
    token_economy.py:625    hard = bool(spec is not None and hard_safety_requires_approval(spec))

Its own docstring calls it a "HARD safety invariant (R-0095)" and states that a user policy "may
add stricter approval but must NEVER weaken this". It forces human approval for expensive or
unknown cost, high, blocked or unknown risk, the external-builder and cloud kinds, and every
placeholder route. So the deletion removes an approval-forcing invariant from a surviving module,
and F275's own "Do not touch" section names THE APPROVAL GATE among the things this feature may not
touch. That collision is real, it is not resolved anywhere on disk, and T001 RULE 3 — the survivor
loses the call site and never gains a copy — points straight into it.

The next session's first work is therefore a dated DECISION in `.agent/decisions.md`, before the
first `git rm`, ruling which of these the round does, with the alternatives and the reversal
recorded: whether `token_economy`'s routing recommendation survives the loss of the registry in a
FAIL-SAFE form, where an absent spec means unknown and unknown already forces approval by that
module's own R-0098 rule, so the invariant is preserved by degradation rather than by a copy; or
whether the recommendation itself is cluster surface that dies with the registry, which is a larger
claim about a surviving module's purpose and needs its own measurement of every consumer of
`token_economy`. Both readings are available and neither is the obvious default. Unlike round 18,
where the measurement showed the deleted gate had been jammed shut and could not discriminate, this
gate DOES discriminate today, so no equivalent measurement rescues the question.

## Session 10 ends here — TWO delegated rounds, both PASS, both independently re-gated

Stated plainly rather than dressed up, because the number is below the floor.
`docs/agents/self_drive_protocol.md` G7, as amended by amend0905-throughput, targets SIX TO EIGHT
delegated rounds per session with FOUR as the floor, and this session ran TWO. That is a real
shortfall and it is reported as one.

THE REASON IS THE ONE amend0905 SANCTIONS AND IT IS OFFERED AS A MEASUREMENT: round 20 is a round
that explicitly needs a fresh session. The measurement is the four lines quoted above — a hard
safety invariant, documented as un-weakenable, consumed by a surviving module, inside a feature
whose "Do not touch" names the approval gate. Authoring that block against an unmade ruling is what
this feature's own record shows costs a round, and it is the same category of reason session 9 gave
for round 18, which then landed clean. The OTHER sanctioned reason is explicitly NOT claimed:
operator amendment amend0908-f275-finish rule 5 permits "authoring errors accumulating" to end a
session only after at least four delegated rounds, and this session ran two, so that reason is
unavailable and is not being used. Both of this session's rounds passed, and the four prose slips
it recorded were all caught by a worker or by the reviewer's own re-gate before anything reached
disk wrongly.

WHAT THIS SESSION LANDED. Round 18, the `overnight_executor` group at 1119 module lines over 24
paths, 27 insertions against 1993 deletions, taking one command, four test functions, one whole
documentation page with its index row and five inbound cross-links, and unthreading a live-review
gate from THREE surviving production modules under DECISION F275 D8 — which ruled the question
session 9 left open by measuring that the gate could not read this repository's own ledger format
and therefore blocked unconditionally rather than discriminating. Round 19, the
`overnight_readiness` group at 894 module lines over 13 paths, 7 insertions against 1402 deletions,
taking the WHOLE `overnight` command group, its GroupDef, its handler file and two test files, with
the surviving carry-over pinned by a mutation rather than by assertion. Findings R-0862, R-0863 and
R-0864 were registered and R-0861 was resolved by reviewer-authored text. The full suite is green
at 18515 passed, 23 skipped and ZERO failed. THIRTEEN of F260's prototype-cluster module groups are
now gone and TWO components remain in `.agent/f275_deletion_order.md`.

CONTEXT SELF-ASSESSMENT, as amend0905-throughput requires in one sentence: the reviewer's context
was long but not exhausted and is NOT the reason this session ends — it ran four full serial suites,
two of them establishing round boundaries by an applied dry run and two of them independent
re-gates, and it ends on the round-20 boundary being measured rather than on the reviewer running
out of room.

## What the next session owes, in order

FIRST, Phase 1 rule 1: re-read `.agent/STOP` from disk before the Open PR Gate. It does not exist
as this session ends and was measured absent at the Phase 0 probe and again before each round. Then
the Open PR Gate: no pull request is open, and none is owed until the closure sequence.

SECOND, round 20's FIRST substantive commit books, from this file as the durable carrier under
amend0827-process-diet rule 1: the ROUND 19 PASS verdict above as a `Gate: F275 R19` entry in
`.agent/live_review.md`, and the two prose slips as dated lines in `.agent/prose_slips.md`. The
open set is 87 by distinct id and the next free id is R-0865.

THIRD, round 20 itself: rule the `token_economy` hard-safety question as a dated DECISION BEFORE
the first `git rm`, complete an applied dry run to a green suite before authoring anything, and
order the mutation red-proofs in full, because a surviving production module loses code and one of
the removed calls is an approval-forcing invariant.
