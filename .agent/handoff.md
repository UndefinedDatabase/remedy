# Handback — F275 round 20

## Session

SESSION 11 of feature F275 · round 20 · rounds so far 20

F275's soft limit is 20 sessions and 60 rounds by operator amendment
amend0908-f275-finish rule 1, and it travels to no other feature. This round is
inside it, so no scope report is owed.

This round deleted the FOURTEENTH module group of the prototype cluster,
`packages.orchestration.worker_registry`, component 1 of
`.agent/f275_deletion_order.md`, in ONE commit — the module, its handler, the
WHOLE `route-policy` command group, the three `worker.registry-*` commands, its
cockpit section, four `ContractAction` members, two documentation pages and
three test files. It is NOT a pure deletion round under
amend0906-triage-throughput: the surviving consumer
`packages/orchestration/token_economy.py` had its approval logic rewritten, so
the four-measurement shortcut does not apply and the mutation red-proof was
ordered and run in full as G5. DECISION F275 D9, committed BEFORE the first
`git rm`, authorises that survivor's FAIL-SAFE degradation. The round also
booked round 19's PASS verdict from the pushed `.agent/handoff.md` per
amend0827-process-diet rule 1, registered R-0865, and recorded two prose slips.

Context self-assessment (amend0905-throughput): context is comfortable. The
round's cost was dominated by the 21-minute serial full suite, the two
`--collect-only` sweeps behind the node-id set difference and one read-only base
worktree; reading the targets was cheap.

## Range

Review of `0d18e58a`..`HEAD` (C5, the commit that writes this file).

## Commits

### dd607168 F275 R20 C0a: save the round 20 step block verbatim under .agent/authored.

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f275-r20.md | 483/0 | the round 20 step block, copied byte for byte from the delegation source with `shutil.copyfile`; 40139 bytes, sha256 `1b8d1b0b…84cc61` |

### 2363da0a F275 R20 C0b: mirror the round 20 block bytes into the last-block state file.

| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 446/273 | the same bytes, taken from the COMMITTED C0a blob via `git show`, not from the scratch file |

### c98186af F275 R20 C1: advance the plan to round 20.

| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 20/17 | replaced WHOLE by the PLAN20 slice extracted from the committed C0a blob; 44 lines against the AGENTS.md cap of 50 |

### 85379a77 F275 R20 C2: book the round 19 PASS verdict, register R-0865, record two prose slips.

| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 6/0 | LEDGER20 appended: the `Gate: F275 R19` PASS record, the R-0865 registration and the `Note: F275 R20` widening of R-0858 |
| .agent/prose_slips.md | 4/0 | SLIPS20 appended: the round 19 no-op change-set entry and the round 19 suite-delta arithmetic |

### ce71d139 F275 R20 C3: rule DECISION F275 D9 - token economy degrades fail-safe.

| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 72/0 | DECISION20 appended: DECISION F275 D9, the ruling that authorises the survivor's degradation, committed BEFORE the first `git rm` |

### 1abe8ac2 F275 R20 C4: delete the worker_registry module group and degrade token_economy fail-safe.

| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/worker_registry.py | 0/1035 | the module itself — component 1 of the deletion order |
| apps/cli/commands/route_policy_cmd.py | 0/196 | its command handler; a cluster handler, so its imports were never a blocking edge |
| tests/orchestration/test_worker_registry.py | 0/380 | tests of a deleted module die with it (36 node ids) |
| tests/cli/test_route_policy_cli.py | 0/107 | tests of the deleted handler (11 node ids) |
| tests/orchestration/test_worker_route_integration.py | 0/27 | integration test of the deleted pair (1 node id) |
| docs/guides/worker-route-policy-user-guide-v0.md | 0/88 | user guide for commands that no longer exist |
| docs/system/worker-registry-route-policy-v0.md | 0/106 | system doc for a deleted module |
| apps/cli/command_catalog.py | 0/79 | the `route-policy` GroupDef, the three `worker.registry-*` entries with their section comment, and the three `route-policy.*` entries with theirs |
| apps/cli/commands/__init__.py | 1/2 | `route_policy_cmd` dropped from BOTH the sorted import block and the dispatcher tuple |
| packages/orchestration/ui_server.py | 1/48 | `_build_worker_registry_section` and its dashboard key deleted; SEPARATELY the surviving `_build_token_economy_section` loses its registry import and its `ollama_placeholder_available` key in both returns — the user-observable loss R-0865 records |
| packages/orchestration/token_economy.py | 20/61 | THE SURVIVOR'S DEGRADATION, ruled by DECISION F275 D9: all three registry imports and `estimate_route_token_band` deleted, `recommended_worker_id` left empty, `estimated_cost_band` UNKNOWN, approval UNCONDITIONAL, the ladder collapsed to two branches naming only surviving commands, both head-docstring paragraphs and the function docstring rewritten in the past tense naming F275 round 20 |
| packages/orchestration/run_contract.py | 0/12 | the Step 1726 comment, the four `ContractAction` members and their four safe-action tuple lines |
| tests/cli/test_cli_ux.py | 1/1 | `"route-policy"` removed from the hand-maintained `_INTERNAL_GROUPS`; only the applied dry run finds this one — no grep for the module name reaches it |
| tests/orchestration/test_token_economy.py | 7/11 | `test_route_band_unknown_stays_unknown` deleted with its function; the two-way `route-policy` disjunct narrowed away; `test_local_route_no_approval_when_cheap` REPLACED by `test_no_route_spec_fail_safe_requires_approval` |
| tests/orchestration/test_token_economy_integration.py | 4/30 | the whole `TestPlaceholderHardening` class deleted; the docstring's last sentence rewritten as a deliberate absence |
| tests/ui_server/test_dashboard_cockpit_truth.py | 0/15 | `test_worker_registry_section_present`, the only test of the deleted cockpit section |
| tests/orchestration/test_cluster_deletion_map.py | 1/3 | the module dropped from `CLUSTER_MODULES`, the handler from `CLUSTER_COMMAND_HANDLERS`, and `_cluster_module_of`'s docstring example re-pointed at `provider_trust`, which still exists |
| tests/orchestration/cluster_deletion_map.txt | 0/2 | BOTH `worker_registry <- ` lines, the `token_economy.py` one and the `ui_server.py` one |
| tests/orchestration/import_reachability_allowlist.txt | 0/2 | BOTH `apps.cli.commands.route_policy_cmd` and `packages.orchestration.worker_registry` |
| docs/README.md | 0/3 | the three index rows naming the two deleted pages — quick-find, system table, guides table |
| docs/system/token-economy-context-budget-optimizer-v0.md | 10/8 | the local-route paragraph and the "Expensive route justification" section rewritten: approval UNCONDITIONAL, the floor surviving by degradation, `hard_safety_requires_approval` gone, F110 named as the inheritor |
| docs/system/quality-baseline-v0.md | 0/1 | the coverage-table row for the deleted handler |
| .agent/f275_deletion_order.md | 0/1 | REGENERATED from the live import graph by `measured_order()`; the 26 header lines are byte-identical to the base and ONE component line remains |

### C5 — the handoff commit (self-reference exception, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this file; a handoff cannot table the commit that writes it |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/g5 1abe8ac2` | created; the G5 mutation red-proof ran only here |
| `git worktree add --detach .remedy-wt/base 0d18e58a` | created READ-ONLY; the base collect-only, the base ruff distribution and the base catalog read |
| `git worktree remove --force .remedy-wt/g5` | removed before C5 |
| `git worktree remove --force .remedy-wt/base` | removed before C5 |
| `git worktree prune` | ran; `git worktree list` holds ONE entry |
| `git push -u origin feature/f275-one-world-completion-part-three` | ONCE, after C5 |

No PR was created, nothing was merged, and no `gh` command was run.

## Verification

Every gate below was run as `bash -c '<cmd>; echo "REAL_EXIT=$?"'` and carries
its REAL exit code.

**G1 TRANSPORT — exit 0.** One digest comparison over three artefacts and
nothing else. Delegation source `.remedy-wt/f275-r20.md`, committed
`.agent/authored/f275-r20.md` and committed `.agent/last_block.md` are all
**40139 bytes** at sha256
`1b8d1b0bf7892a84ec83b3a581267bd557de89118b5df0dfa49cbe95db84cc61`, and all
three compare BYTE-EQUAL. Per §3 item 37 this chain covers those three artefacts
and claims nothing about the bytes that were emitted.

**G2 THE PLAN AND THE SLICES — exit 0.** `.agent/plan.md` at C1 `c98186af` is
2442 bytes at `66a58691…4742f7`, BYTE-IDENTICAL to the PLAN20 slice extracted
from the committed C0a blob. 44 lines against the AGENTS.md cap of 50; `## Goal`
occurs exactly once and `## Next Steps` exactly once. For all four slices: the
block carries 8 marker strings, each slice occurs EXACTLY ONCE in its target
(PLAN20 → `plan.md`, LEDGER20 → `live_review.md`, SLIPS20 → `prose_slips.md`,
DECISION20 → `decisions.md`), and a grep for every one of the 8 marker strings
over each of the four target files returns **0** for each file.

**G3 THE RECORD — exit 0**, over three appends, each with a byte reader, a
structural reader and a negative control.

| Append | pre | post | slice | growth = 1 + slice | prefix | suffix | joining byte |
|---|---|---|---|---|---|---|---|
| LEDGER20 → live_review.md | 671839 `25bec09a…` | 680095 `f8131353…` | 8255 `0ef9bb84…` | 8256 = 1 + 8255 ✓ | ✓ | ✓ | `b'\n'` |
| SLIPS20 → prose_slips.md | 194749 `93c5b2a5…` | 196492 `3e5a1ceb…` | 1742 `6f640cb3…` | 1743 = 1 + 1742 ✓ | ✓ | ✓ | `b'\n'` |
| DECISION20 → decisions.md | 975891 `9c5791aa…` | 981656 `1d46a248…` | 5764 `c492ddc2…` | 5765 = 1 + 5764 ✓ | ✓ | ✓ | `b'\n'` |

STRUCTURAL READER. N was counted BY THE SCRIPT from the slice, never asserted by
the block: **N = 3** for LEDGER20, **N = 2** for SLIPS20, **N = 7** for
DECISION20. For each append the LAST N blank-line units of the whole post-file
were compared IN ORDER against the slice's N paragraphs with a per-unit sha256
on both sides — all 12 unit pairs equal. The unit BEFORE them was shown to lie
inside the PRE blob in every case: `25ed378e…`, `a1dd14b0…`, `44418a13…`.

NEGATIVE CONTROL. One byte was flipped IN MEMORY inside the FIRST appended
paragraph of each append — offset 674066 `a`→`` ` ``, offset 195222 `n`→`o`,
offset 975987 `' '`→`'!'`, each verified to lie within the first paragraph's
span. BOTH readers REJECTED all three tampers while BOTH ACCEPTED all three
truths. Each file was re-read from disk afterwards and equals its committed
post-blob.

COUNTS. `^Gate: ` **41 before, 42 after**. `^Gate: F275 R19 ` = 1,
`^- R-0865 — ` = 1, `^Note: F275 R20 ` = 1, `^## DECISION F275 D9 ` = 1 — each
exactly once.

THE OPEN SET BY DISTINCT ID, `Landed:` never subtracted:

| Revision | registrations | resolutions | OPEN | distinct `Landed:` ids present |
|---|---|---|---|---|
| base `0d18e58a` | 93 | 6 | **87** | 34 |
| C3 `ce71d139` | 94 | 6 | **88** | 34 |

**G4 THE SWEEP, READ BY HAND — exit 0.** Over **1661** tracked files outside
`.agent/` and `.data/`, for the fifteen ordered tokens. RAW = **6**, exactly
what the applied dry run measured at C4, so there is nothing to reconcile. THE
RAW LIST IN FULL, NOT TRUNCATED:

```
docs/roadmap/features/T2_F260.md:341: [worker_registry] `worker_registry.py`, `model_route_tournament.py`, `context_pack.py`,
docs/roadmap/features/T2_F260.md:363: [route_policy_cmd] (`route_policy_cmd.py`: `prefer_local_for_cheap_tasks`,
docs/roadmap/features/T2_F260.md:366: [worker_registry] `prefer_local_advisor`, `require_human_approval`; `worker_registry`: `risk_tier`,
docs/roadmap/features/T2_F262.md:76: [worker.registry-list] `worker.registry-list` (no date field on their row shape) and
docs/roadmap/features/T2_F267.md:28: [worker.registry-list] `execution.template-list`, `worker.registry-list` (no date on their row shape)
docs/roadmap/features/T8_F151.md:19: [worker_registry] Real modules exist: worker_registry.py (declarative WorkerSpec
```

CLASSIFICATION, line by line. All six are history prose under
`docs/roadmap/features/` and none is production code, a test, a guide or an
index. Three sit in `T2_F260.md` (lines 341, 363, 366) — F260's own account of
what the prototype cluster contained, which is a historical record of a `[x]`
feature. One sits in `T2_F262.md` line 76, likewise `[x]`, the reading R-0858
already applies to `T2_F085.md`. One sits in `T2_F267.md` line 28 — this is the
OPEN one, and it is exactly the line the `Note: F275 R20 ` record appended to
the ledger this round widens R-0858 to cover: F267 is `[ ]` and its plan now
names three deleted commands rather than two. One sits in `T8_F151.md` line 19,
an unchecked feature's inventory of modules that existed when it was written.
The spaced advertisement forms `remedy route-policy` and `remedy worker
registry-` return **ZERO** hits, so no page anywhere still instructs an operator
to run a command this round deleted.

`tests/cli/test_advertised_commands.py` was run separately: **exit 0, 5
passed**. STATED PLAINLY: that pass is NOT evidence for this round. Deleting the
whole `route-policy` group removes it from that guard's `GROUPS`, and the guard
skips what it cannot resolve — finding R-0847. The gate above, read by hand from
its RAW list, is the evidence.

**G5 THE FAIL-SAFE IS PINNED, NOT MERELY WRITTEN — control exit 0, mutation
exit 1, post-revert exit 0.** Run inside the disposable worktree
`.remedy-wt/g5` created at C4 `1abe8ac2`, with `__pycache__` purged and
`python3 -B` before every run.

- (a) REVERT TARGET BY PATH:
  `.remedy-wt/g5/packages/orchestration/token_economy.py`. The exact mutated
  bytes `    d.requires_human_approval = True` occur **1** time in THAT file.
- (b) NOT SHADOWED BY THE EDITABLE INSTALL:
  `import packages.orchestration.token_economy` resolves to
  `/home/decodeux/Repos/remedy/.remedy-wt/g5/packages/orchestration/token_economy.py`.
- (c) CONTROL, unmutated, over the node set — **exit 0, 72 passed**.
- (d) MUTATION, `d.requires_human_approval = True` → `False` in
  `compute_token_economy_decision` — **exit 1, 5 failed, 67 passed**. The five:
  `TestDecision::test_unknown_context_requires_approval`,
  `TestDecision::test_unknown_context_hint_not_local_first`,
  `TestDecision::test_no_route_spec_fail_safe_requires_approval`,
  `TestDecision::test_over_threshold_requires_approval` and
  `TestIntegrity::test_real_unknown_decision_is_safe_under_audit` — the last
  being this module's own R-0099 audit invariant, exactly as DECISION F275 D9
  predicted.
- (e) REVERTED BY PATH with `git checkout --`, purged, re-run — **exit 0, 72
  passed** — and the worktree porcelain is EMPTY (0 lines).

THE STOP CONDITION DID NOT FIRE: the mutation is RED, so the fail-safe is pinned
by tests that bite and DECISION F275 D9's premise holds. Every figure matches
the applied dry run exactly.

**G6 THE GUARDS, THE SUITE AND RUFF.**

- (a) exit 0 — the nine affected guards, **548 passed** (dry run: 548).
- (b) exit 0 — the canary `tests/cli/test_golden_path.py`, **42 passed**.
- (c) exit 0 — `tests/docs/`, **303 passed**; this round edits `docs/`.
- (d) exit 0 — THE FULL SUITE, `python3 -B -m pytest tests/ -q`, run SERIALLY in
  the PRIMARY checkout with C4 committed, never `-n auto`: **18454 passed, 23
  skipped, ZERO failed** in 1300.69s. A separate `--collect-only` gives
  **18477 = 18454 + 23**.

  THE ARITHMETIC AGAINST THE BASE, closed by a node-id SET DIFFERENCE of
  `--collect-only` and not by counting functions. Base `0d18e58a` collects
  **18538** in a read-only worktree; C4 collects **18477**; the fall is
  **61**, and it is **62 ids removed against 1 added**. The attribution
  reproduces the dry run's exactly:

  | Source | ids removed |
  |---|---|
  | tests/orchestration/test_worker_registry.py (deleted) | 36 |
  | tests/cli/test_route_policy_cli.py (deleted) | 11 |
  | tests/orchestration/test_worker_route_integration.py (deleted) | 1 |
  | tests/test_grouped_cli.py — 8 parametrized `[route-policy]` cases GENERATED from the catalog `GROUPS`, in a file the change set never names | 8 |
  | tests/orchestration/test_token_economy_integration.py — `TestPlaceholderHardening` | 3 |
  | tests/orchestration/test_token_economy.py | 2 |
  | tests/ui_server/test_dashboard_cockpit_truth.py | 1 |
  | **total removed** | **62** |

  The 1 added id is
  `tests/orchestration/test_token_economy.py::TestDecision::test_no_route_spec_fail_safe_requires_approval`,
  the replacement fail-safe test. 62 − 1 = 61. Nothing to reconcile.

- (e) exit 0 — `python3 -B -m ruff check` over all ten surviving `.py` paths of
  the change set: **All checks passed!**. PARITY over `packages`, `apps` and
  `tests`: **`Found 24 errors.` at BOTH** base `0d18e58a` (read in a DISPOSABLE
  READ-ONLY worktree, never by writing a base blob over a tracked file) and C4,
  each exit 1, and the per-file distributions are IDENTICAL — a `diff` of the
  two distributions is empty. Not one of the 24 is in a file this round touches:
  they sit in `tests/cli/test_plan_approval.py` (6),
  `tests/orchestration/test_long_run_executor.py` (2),
  `tests/orchestration/test_prompt_trace.py` (2),
  `tests/test_project_context_coverage.py` (2) and twelve files with one each,
  including `packages/orchestration/dag_schedule.py` and
  `packages/orchestration/gauntlet_injection.py`. Per constraint 6 they are
  pre-existing and were not repaired.

**G7 THE RATCHETS AND THE CATALOG AGREE WITH THE DISK — exit 0.** The SHIPPED
catalog was read by importing `_BASE_CATALOG` and `GROUPS` from
`apps.cli.command_catalog`, never by grepping the source; the BASE revision was
read the same way inside the READ-ONLY disposable worktree at `0d18e58a`.

| | base `0d18e58a` | C4 `1abe8ac2` |
|---|---|---|
| commands | 233 | **227** |
| groups | 46 | **45** |
| `"route-policy"` in `GROUPS` | present | **absent** |
| ids beginning `route-policy.` | 3 | **0 (EMPTY)** |
| ids beginning `worker.registry-` | 3 | **0 (EMPTY)** |
| duplicate ids | 0 | **0** |
| dangling `related=` | 2 | **2** |

DISCHARGING R-0859's STANDING OBLIGATION on every deletion round of this feature
until its closure test exists: every `related=` tuple in the catalog was
resolved against the LIVE id set at both revisions. Exactly **2** dangle at each
— `mission.run -> dogfood.run-loop` and `repo.status -> readiness.show`, both
PRE-EXISTING, both held by R-0859 and bound to the DECISION F260 D3 round. This
round ADDED NONE; per constraint 5 neither was repaired.

`.agent/f275_deletion_order.md` now holds **ONE** component line,
`packages.orchestration.provider_trust, packages.orchestration.provider_trust_verification`.
The file was REGENERATED from the live import graph with `measured_order()` and
never line-edited; a fresh regeneration re-run reproduces the committed bytes
exactly (1784 bytes, `9b1cf343…0d1652`, `on disk equals regeneration True`), and
its 26-line header is byte-identical to the header at the base. Neither
`cluster_deletion_map.txt`, `import_reachability_allowlist.txt`,
`CLUSTER_MODULES` nor `CLUSTER_COMMAND_HANDLERS` still names this group's module
or handler — a grep for both names over all three files returns ZERO.

**G8 THE TREE — exit 0.**

- `.agent/STOP` re-read from disk: **does not exist**.
- `git status --porcelain`: **EMPTY**.
- `git worktree list`: **ONE** entry, the primary checkout.
- branch: `feature/f275-one-world-completion-part-three`.
- `git diff --name-only ce71d139..1abe8ac2` compared as a SET against the block's
  23 paths: **23 vs 23**, MISSING = **EMPTY**, EXTRA = **EMPTY**.
- Per-commit insertions against the DECISION F104 D1 cap of 500, with parent
  counts — every commit SINGLE-PARENT, every commit under the cap:

  | Commit | + | − | parents | under 500 |
  |---|---|---|---|---|
  | dd607168 C0a | 483 | 0 | 1 | ✓ |
  | 2363da0a C0b | 446 | 273 | 1 | ✓ (also exempt: a single `.agent/**` state file rewrite) |
  | c98186af C1 | 20 | 17 | 1 | ✓ |
  | 85379a77 C2 | 10 | 0 | 1 | ✓ |
  | ce71d139 C3 | 72 | 0 | 1 | ✓ |
  | 1abe8ac2 C4 | 45 | 2218 | 1 | ✓ |

- §3 item 28: every `+/-` cell of the `## Commits` tables above was compared CELL
  BY CELL against `git show --numstat` for its commit. **They agree**, all 29
  cells across the six commits.

## Authored-text proofs

Four reviewer-authored slices were applied this round, every one extracted BYTE
FOR BYTE from the COMMITTED C0a blob `dd607168:.agent/authored/f275-r20.md`
between its marker lines with the markers EXCLUDED. None was retyped and none
was edited.

| Slice | bytes | sha256 | Target | Result |
|---|---|---|---|---|
| PLAN20 | 2442 | `66a58691…4742f7` | `.agent/plan.md` (WHOLE) | byte-identical at C1; occurs exactly once |
| LEDGER20 | 8255 | `0ef9bb84…80d72d` | `.agent/live_review.md` (append) | byte-exact SUFFIX at C2; occurs exactly once |
| SLIPS20 | 1742 | `6f640cb3…b5ca33` | `.agent/prose_slips.md` (append) | byte-exact SUFFIX at C2; occurs exactly once |
| DECISION20 | 5764 | `c492ddc2…12c02b` | `.agent/decisions.md` (append) | byte-exact SUFFIX at C3; occurs exactly once |

No marker line reached any target file: a grep for all 8 marker strings over all
four targets returns 0 for each.

## Item status

The block's ordered specification, every item exactly once. D1–D7 are the whole
files deleted; 1–16 are its numbered edits.

| Item | Path | Status | Reason |
|---|---|---|---|
| D1 | packages/orchestration/worker_registry.py | done | |
| D2 | apps/cli/commands/route_policy_cmd.py | done | |
| D3 | tests/orchestration/test_worker_registry.py | done | |
| D4 | tests/cli/test_route_policy_cli.py | done | |
| D5 | tests/orchestration/test_worker_route_integration.py | done | |
| D6 | docs/guides/worker-route-policy-user-guide-v0.md | done | |
| D7 | docs/system/worker-registry-route-policy-v0.md | done | |
| 1 | apps/cli/command_catalog.py | done | 0/79, exactly the dry run's figure |
| 2 | apps/cli/commands/__init__.py | done | BOTH the import block and the dispatcher tuple |
| 3 | packages/orchestration/ui_server.py | done | both edits, including the surviving section's lost key |
| 4 | packages/orchestration/token_economy.py | deviated | every ordered semantic element applied; measured 20/61 against the block's stated 22/62, and the FUNCTION docstring was rewritten in addition to the two head-docstring paragraphs. See Deviations 1 and 2 |
| 5 | packages/orchestration/run_contract.py | done | |
| 6 | tests/cli/test_cli_ux.py | done | |
| 7 | tests/orchestration/test_token_economy.py | deviated | all three ordered changes applied; the replacement test carries a FOURTH assertion the block did not name. See Deviation 3 |
| 8 | tests/orchestration/test_token_economy_integration.py | done | 4/30, exactly the dry run's figure |
| 9 | tests/ui_server/test_dashboard_cockpit_truth.py | done | |
| 10 | tests/orchestration/test_cluster_deletion_map.py | done | example re-pointed at `provider_trust` |
| 11 | tests/orchestration/cluster_deletion_map.txt | done | BOTH lines existed and BOTH were removed |
| 12 | tests/orchestration/import_reachability_allowlist.txt | done | |
| 13 | .agent/f275_deletion_order.md | done | REGENERATED, never line-edited; header byte-identical; one component line remains |
| 14 | docs/README.md | done | all three rows |
| 15 | docs/system/token-economy-context-budget-optimizer-v0.md | done | 10/8, exactly the dry run's figure |
| 16 | docs/system/quality-baseline-v0.md | done | |

The block's ordered COMMIT bundle, every item exactly once:

| Commit | Status | Reason |
|---|---|---|
| C0a | done | dd607168 |
| C0b | done | 2363da0a |
| C1 | done | c98186af |
| C2 | done | 85379a77 |
| C3 | done | ce71d139 — precedes the first `git rm`, as constraint 3 orders |
| C4 | done | 1abe8ac2 — ONE commit, never split, as constraint 2 and T001 RULE 1 order |
| C5 | done | this commit |

There was NO departure from the block's ordered commit sequence: six commits, in
the ordered order, no extra commit, none dropped, none reordered.

## Deviations & assumptions

**1. `token_economy.py` measured 20/61, not the block's stated 22/62.** The
bundle total is therefore 45 insertions / 2218 deletions against the block's
stated 47 / 2219, and every other one of the 23 paths matches its stated figure
to the line. The difference is entirely prose-line variance: my rewrite of the
two head-docstring paragraphs, the function docstring, the two replacement
comment blocks and the else-branch is two lines shorter than the reviewer's
applied dry run's, and one deletion differs because `else:` fell out as shared
context rather than as a delete/insert pair. Every semantic element the block
ordered is present and was verified by grep: no `worker_registry` import
survives, `estimate_route_token_band` and its `Public API::` line are gone,
`recommended_worker_id` is left at its empty default, `estimated_cost_band` is
set to `TokenBand.UNKNOWN`, `d.requires_human_approval = True` is unconditional
and carries a comment naming the pre-deletion `or not spec` term it replaces,
the ladder is two branches, and a grep for `remedy route-policy`,
`remedy worker registry-`, `hard_safety_requires_approval`, `classify_route_cost`
and `selection.` over the module returns ZERO — all four of the base's dead
command strings died.

**2. The FUNCTION docstring of `compute_token_economy_decision` was rewritten
too.** Item 4 orders only "the two head-docstring paragraphs". I also rewrote
the function's own four-line docstring into three lines, because it stated that
the function combines "the budget profile + context estimate + Worker Registry
route policy" and that "placeholder routes always require human approval (Worker
Registry hard-safety floor)" — both false once the registry is deleted, and
false prose sitting directly above correct code is the R-0838 pattern. This is a
WIDENING of the specified change set within an already-listed path, and it is
declared here rather than silently absorbed. The block's own deletion figure of
62 is only reachable with this rewrite included, so I believe the reviewer's
applied dry run made the same edit and the specification prose simply did not
name it — but I am reporting what I did, not what I infer.

**3. The replacement fail-safe test carries a FOURTH assertion.** Item 7 names
three: the empty `recommended_worker_id`, the UNKNOWN cost band and
`requires_human_approval is True`. `test_no_route_spec_fail_safe_requires_approval`
asserts all three and additionally `assert "No route spec is available" in
d.reason`, which pins the else-branch reason string item 4 orders. This is a
widening; it is why the file measured 7/11 with a one-line comment where a
two-line comment would have made it 8/11.

**4. C4 was committed BEFORE the G5 mutation red-proof ran.** The block orders
the proof "inside a disposable worktree at C4" and, in the same gate, orders a
handback "without committing C4" should the mutation come out GREEN. A worktree
AT a commit cannot exist before that commit does, so the two clauses cannot both
be satisfied literally. I resolved it by committing C4, creating the worktree at
`1abe8ac2`, running the proof there, and holding the option of resetting the
UNPUSHED C4 had the STOP condition fired — no push happened until after C5. The
mutation was RED, so the option was never exercised and nothing was rewritten. I
believe the constraint as written is unsatisfiable rather than wrong in intent,
and I obeyed the intent; a future block could say "a worktree at the C4 tree,
created from the staged index" if the literal reading matters.

**5. No `Landed:` line was written.** Constraint 9 forbids one for R-0831 this
round, and no other open finding's fix landed here. R-0865 is a REGISTRATION,
made by the reviewer's LEDGER20 slice, not by me. R-0858 gained new evidence
through the `Note: F275 R20 ` record in the same slice, which is not a
resolution. I wrote no verdict, no `Done:` paragraph and no finding of my own.

**6. Constraints 5 and 6 were obeyed as written and both cost the round
nothing.** The two pre-existing dangling `related=` references were left alone
and G7 shows the count is 2 at BOTH revisions, so this round added none. The 24
pre-existing repo-wide ruff errors were left alone and G6(e) shows an identical
per-file distribution at both revisions, none of them in a touched file.

**7. Scratch discipline.** All disposable work lived under the gitignored
`.remedy-wt/`; `/tmp` is denied in this environment. Both worktrees were removed
and pruned before C5, and every helper `.py` script under `.remedy-wt/r20/` was
deleted before the final `git status --porcelain`, so no untracked `.py` file
remains anywhere in the tree for
`tests/orchestration/test_ci_budgets.py` to lint.

I disagree with no constraint in this block. Deviations 2 and 3 are widenings I
chose and am declaring so that a reviewer can reject them; deviations 1 and 4
are reports of measurement and of an unsatisfiable literal reading.

## Next

The reviewer independently re-runs all eight gates against the committed blobs
`0d18e58a`..`HEAD` and issues the round 20 verdict. Then round 21: the
`provider_trust` / `provider_trust_verification` pair — the last cycle and the
LAST component in `.agent/f275_deletion_order.md`, which after this round holds
exactly one line. Phase 1 rule 1 first: re-read `.agent/STOP` from disk before
authoring.

## Reviewer verdict on round 20 — appended after the handback, by the reviewer's authored text

VERDICT ROUND 20: **PASS.** Written by the planner and reviewer of SESSION 11 AFTER reading the
committed range `0d18e58a`..`d991ecaa` and RE-RUNNING EVERY GATE INDEPENDENTLY against the committed
blobs; the worker's report was not taken as evidence for any line below. It is carried here because
under `docs/agents/self_drive_protocol.md` a verdict that stays in the session is lost, and it is
booked into `.agent/live_review.md` by the FIRST substantive commit of round 21, per
amend0827-process-diet rule 1.

WHAT THE REVIEWER RE-MEASURED. Seven single-parent commits C0a `dd607168`, C0b `2363da0a`, C1
`c98186af`, C2 `85379a77`, C3 `ce71d139`, C4 `1abe8ac2` and C5 `d991ecaa`, per-commit insertions 483,
446, 20, 10, 72, 45 and 424, every one under the AGENTS.md DECISION F104 D1 cap of 500, and every
parent count read from `git log --format=%p`. G1 IS THE PRIMARY PROOF OF §4 ITEM 9 AND NOT THE DIGEST
FALLBACK: the reviewer's own delegation source `.remedy-wt/f275-r20.md` and both committed copies are
40139 bytes at `1b8d1b0bf7892a84ec83b3a581267bd557de89118b5df0dfa49cbe95db84cc61` and compare
BYTE-EQUAL; per §3 item 37 that chain covers those three artefacts and claims nothing about the
emitted bytes. G2: `.agent/plan.md` at C1 is 2442 bytes and byte-identical to the PLAN20 slice plus
its terminating newline, 44 lines against the cap of 50, with `## Goal` and `## Next Steps` each
exactly once; all four slices occur EXACTLY ONCE in their targets and a sweep for all eight marker
strings over the four target files returns ZERO for every file.

G3 HELD OVER THREE APPENDS, AND THE REVIEWER PROVED THEM BY WHOLE-FILE IDENTITY RATHER THAN BY
ARITHMETIC ALONE: for `.agent/live_review.md`, `.agent/prose_slips.md` and `.agent/decisions.md` the
committed post-blob equals `pre + newline + slice + newline` EXACTLY, so the pre blob is a byte-exact
prefix and the slice with its terminating newline a byte-exact suffix. The structural reader counted
N from the slice itself — 3, 2 and 7 paragraphs — and matched the last N blank-line units of each
whole post-file IN ORDER, with the unit before each region shown to lie inside the pre blob. All three
NEGATIVE CONTROLS were flipped inside the FIRST appended paragraph, per §3 item 36, and BOTH readers
rejected all three while accepting all three truths. `^Gate: ` rose 41 to 42; `^Gate: F275 R19 `,
`^- R-0865 — `, `^Note: F275 R20 ` and `^## DECISION F275 D9 ` each occur EXACTLY ONCE. THE OPEN SET
WENT 87 TO 88 BY DISTINCT ID against registrations 93 to 94 and resolutions 6 to 6, with 34 distinct
`Landed:` ids present and never subtracted.

G4 IS AGAIN THE GATE THIS ROUND'S OWN GUARD COULD NOT ANSWER, AND IT IS CLEAN. The reviewer re-ran the
fifteen-token sweep with its own script over the 1660 tracked files outside `.agent/` and `.data/`:
RAW 6, printed in full and not truncated, and every one of the six is history prose under
`docs/roadmap/features/` — three in `T2_F260.md`, one each in `T2_F262.md`, `T2_F267.md` and
`T8_F151.md`. The spaced forms `remedy route-policy` and `remedy worker registry-` return ZERO hits, so
no page anywhere still instructs an operator to run a command this round deleted. That is the property
R-0861's fix clause exists to protect and the one `tests/cli/test_advertised_commands.py` cannot
establish here, because deleting the whole `route-policy` group removed it from that guard's `GROUPS`
and the guard skips what it cannot resolve. The worker ran that guard, got exit 0, and said in its own
handback that the pass is not evidence for this round — R-0847 handled correctly rather than relied on.

G5's STOP CONDITION DID NOT FIRE, AND IT IS THE ROUND'S MOST LOAD-BEARING READING. The reviewer re-ran
the red-proof itself in a disposable worktree at C4 `1abe8ac2`: the mutated bytes occur exactly ONCE in
the named path, the unmutated CONTROL is exit 0 at 72 passed, forcing `d.requires_human_approval` to
`False` is exit 1 at 5 failed and 67 passed, and the revert returns exit 0 at 72 passed with the
worktree porcelain empty. The five named failures include
`TestIntegrity::test_real_unknown_decision_is_safe_under_audit`, this module's own R-0099 audit
invariant, so the fail-safe DECISION F275 D9 installs is held by tests that bite rather than by a
comment. That is what makes the degradation defensible: approval is now unconditional, which is
strictly stricter than the hard-safety floor it replaces, and nothing that previously required
approval stops requiring it.

G6: the affected guards 548 passed, the canary 42, the documentation gate 303, and THE FULL SUITE WAS
RE-RUN BY THE REVIEWER SERIALLY IN THE PRIMARY CHECKOUT and was GREEN at 18454 passed, 23 skipped and
ZERO failed, with a separately measured collection of 18477 equal to 18454 plus 23. THE ARITHMETIC
CLOSES BY THE ID SET, not by counting functions: 18538 ids at base `0d18e58a` against 18477 at the tip,
a fall of exactly 61, being 62 ids REMOVED against 1 ADDED. The 62 are 48 across the three deleted test
files (36, 11 and 1), 8 parametrized `[route-policy]` cases in `tests/test_grouped_cli.py` which are
generated from the catalog `GROUPS` and die with the GroupDef, 3 in `TestPlaceholderHardening`, 2 in
`test_token_economy.py` and 1 in `test_dashboard_cockpit_truth.py`; the single added id is the
replacement fail-safe test. Ruff is clean over the change set and reads `Found 24 errors.` at BOTH
`0d18e58a` and the tip with an IDENTICAL per-file distribution, not one of them in a file this round
touches, so the round adds none. G7: the SHIPPED catalog reader gives 227 commands in 45 groups against
233 and 46 at the base, `"route-policy"` absent from `GROUPS`, the id sets beginning `route-policy.`
and `worker.registry-` both EMPTY, and zero duplicate ids. Resolving every `related=` tuple against the
live id set gives exactly TWO dangling references at BOTH revisions — `mission.run -> dogfood.run-loop`
and `repo.status -> readiness.show`, both pre-existing and both held by R-0859 — so this round ADDS
NONE, which is the standing obligation R-0859 places on every deletion round until its closure test
exists. The order file is a fresh regeneration with its 26-line header unchanged and ONE component line
left, and neither the map, the reachability allowlist, `CLUSTER_MODULES` nor `CLUSTER_COMMAND_HANDLERS`
still names this group's module or handler. G8: no `.agent/STOP`, porcelain EMPTY, ONE worktree, the
branch correct, and `ce71d139..1abe8ac2` naming the 23 declared paths in an EXACT SET MATCH with MISSING
and EXTRA both empty.

THE SEVEN DECLARED DEVIATIONS ARE ALL SUSTAINED, and the three load-bearing ones are the reviewer's own
errors rather than the worker's. FIRST, the block predicted `packages/orchestration/token_economy.py` at
22 insertions and 62 deletions and the real figure is 20 and 61, so the bundle totals are 45 and 2218
rather than 47 and 2219; production code is SPECIFIED rather than sliced in this workflow, so a
prose-line difference is expected and the other 22 paths match the reviewer's applied dry run to the
line. SECOND, the block's item 4 named "the two head-docstring paragraphs" and did NOT name the
docstring of `compute_token_economy_decision` itself, while that docstring asserted facts about the
Worker Registry that the same commit falsified and the block's own deletion figure was only reachable
with it included; the worker rewrote it, declared the widening, and was right to. THIRD, G5 ordered the
proof "inside a disposable worktree at C4" while its STOP condition ordered the worker to "hand back
without committing C4" — those two cannot both hold literally, and the worker resolved the
contradiction in the only honest way available, by committing C4, proving in a worktree at `1abe8ac2`,
and holding the option of resetting an unpushed commit that the red mutation made unnecessary. The
remaining four are sound: the replacement fail-safe test carries a fourth assertion beyond the three
named, which strengthens it; no `Landed:` line was owed; constraints 5 and 6 were obeyed with neither
the dangling `related=` pair nor the 24 pre-existing ruff errors repaired; and every scratch file and
both worktrees were removed, leaving no untracked `.py` anywhere.

## Evidence for the OPEN finding R-0855, to be booked by round 21's ledger commit

Note: F275 R21 — new evidence for the OPEN finding R-0855, added rather than given an id of its own per
`docs/agents/planner_reviewer_prompt.md` §3 item 30, which orders the open set searched for the DEFECT
before an id is minted. R-0855 records that an ordered anchor deletes a definition without sweeping the
neighbourhood that definition served, and names three instances. THIS IS A FOURTH, MEASURED BY THE
REVIEWER AT `1abe8ac2` while re-gating round 20:
`packages/orchestration/token_economy.py` line 593 still reads
`# Approval: unknown context OR hard-safety floor OR over-budget OR over the approval threshold.`
and it sits directly above `d.requires_human_approval = True`. Not one of the four disjuncts that
comment names is a term of the expression beneath it any more: `hard_safety_requires_approval` does not
occur anywhere in the module after this round, and `unknown_context` is not part of the approval
expression at all. The round's own correct comment sits two lines below it saying the opposite, so the
file carries two adjacent comments about one assignment and only the lower one is true. NO GATE COULD
SEE IT — ruff is clean, the full suite is green, and the round's fifteen-token sweep does not match the
words `hard-safety floor`, because the deletion sweep hunts IDENTIFIERS and this is prose. It is wrong
state on disk under `packages/`, which amend0827-process-diet rule 2 reserves an id for, and it is
folded into R-0855 rather than given one because the defect, the cause and the fix are the same.
FIX CLAUSE, binding on the round that next edits `packages/orchestration/token_economy.py`: delete that
comment line, and run the R-0843 counter-measure — sweep EVERY surviving file of the change set for
PROSE the deletion falsified, in the file's own words rather than in the deleted module's identifiers.

## Prose slips drafted by session 11, to be appended by round 21's ledger commit

2026-09-10 · F275 R20 · The round 20 block stated `packages/orchestration/token_economy.py` at 22 insertions and 62 deletions, taken from the reviewer's own applied dry run, and the worker measured 20 and 61, which made the block's bundle totals 47 and 2219 against a real 45 and 2218. Production code is SPECIFIED rather than sliced in this workflow precisely so the worker writes the prose, so a per-file insertion figure quoted from the reviewer's dry run is a PREDICTION about wording and not a measurement the worker can reproduce. The other 22 paths matched to the line, because every one of them is a deletion or a mechanical edit with no prose in it. The lesson is that a block quoting per-file `+/-` for a SPECIFIED production file quotes it as an approximate expectation and says so, or omits the insertion column for that file and keeps only the deletion count, which is determined by the anchors.

2026-09-10 · F275 R20 · The round 20 block's item 4 ordered the two module-docstring paragraphs of `token_economy.py` rewritten and never named the docstring of `compute_token_economy_decision` itself, although that docstring asserted that the function combines "the Worker Registry route policy" and that "a cheap small task under the local-preference threshold recommends a local route" — both falsified by the same commit. The reviewer's own applied dry run HAD rewritten it, as part of the same anchor that removed the imports, so the block's stated deletion figure was only reachable with it included and the worker had to widen the order to meet the number. The worker declared the widening and was right. The lesson is that when a block SPECIFIES a production edit by naming the docstrings it rewrites, it enumerates every docstring the applied dry run touched, and the surest way to enumerate them is to read the dry run's own diff rather than the reviewer's memory of it.

2026-09-10 · F275 R20 · The round 20 block's G5 ordered the red-proof run "inside a disposable worktree at C4" and, in the same gate, ordered the worker to "hand back without committing C4" if the mutation came out green. Those two clauses cannot both be obeyed: a worktree at C4 requires C4 to exist. The worker committed C4, proved in a worktree at `1abe8ac2`, and kept the option of resetting an unpushed commit, which the red mutation made unnecessary; it declared the contradiction rather than silently picking a half. The lesson is that a STOP condition attached to a gate which itself runs at a named commit is written as an instruction to RESET that commit, not to withhold it, because the gate's own recipe already presupposes the commit exists.

## THE ROUND 21 MAP — MEASURED BY AN APPLIED DRY RUN AT `d991ecaa`, AND WHY IT NEEDS ITS OWN SESSION

Round 21 deletes the LAST component of `.agent/f275_deletion_order.md`: the strongly connected pair
`packages.orchestration.provider_trust` and `packages.orchestration.provider_trust_verification`,
1081 and 1021 lines. It completes T001 — `CLUSTER_MODULES` becomes the EMPTY tuple and the deletion map
loses its last eight edge lines. The reviewer of session 11 APPLIED the whole deletion in a disposable
worktree and measured what follows; none of it is a prediction, and re-buying it is the expense this
section exists to prevent.

WHAT DIES: the two modules; `apps/cli/commands/provider_cmd.py` at 170 lines with the WHOLE `provider`
command group — its `GroupDef` and all five commands `provider.intake-repair`, `provider.trust-show`,
`provider.material-show`, `provider.verify` and `provider.verification-show`; the six provider members
of `ContractAction` in `run_contract.py`, none of which is referenced outside that file; and
`tests/orchestration/test_provider_trust.py` and `test_provider_trust_verification.py`, 348 and 359
lines. There is NO `ui_server.py` cockpit section for this pair, which was measured rather than assumed.

THE FIRST RULING THE ROUND NEEDS, AND IT IS ALREADY ANSWERED BY MEASUREMENT. Seven SURVIVING modules
import `_scrub_public` and three of them also import `_safe_path_label` from the dying
`provider_trust.py`: `orchestrator_brain.py`, `provider_patch_material.py`, `real_test_execution.py`,
`repair_request_builder.py`, `self_dogfood.py`, `self_dogfood_execution.py` and `token_economy.py`.
`_scrub_public` masks secrets, absolute paths and tracebacks in every publicly surfaced string, so
deleting the call sites would remove REDACTION from seven survivors — a weakening in the unsafe
direction, and the opposite of round 20's degradation. These are shared redaction utilities that happen
to live in a cluster file, not cluster capability, so the answer is DECISION F275 D1's precedent: a
BYTE-IDENTICAL MOVE, not a copy and not a rewrite. THE DESTINATION IS MEASURED:
`packages/common/path_redaction.py` is the repository's shared redaction home, is already imported by
four modules under `packages/orchestration/` and `packages/runtimes/`, imports `re`, and is
COLLISION-FREE on all five moved names — `_scrub_public`, `_safe_path_label`, `_SECRET_PATTERNS`,
`_ABS_PATH_RE` and `_TRACEBACK_RE`. The obvious-looking alternative,
`packages/orchestration/redaction_patterns.py`, IS NOT USABLE: it already defines `_TRACEBACK_RE` with a
different, looser, case-insensitive regex, so a byte-identical move would collide and a rename would
stop the move being byte-identical. The seven repoints are then purely mechanical — one or two import
lines each, with every call site unchanged, including the `_REDACTION_HELPERS` tuples in
`real_test_execution.py` and `token_economy.py`.

THE SECOND RULING, ALSO ANSWERED BY MEASUREMENT. `packages/orchestration/provider_patch_material.py`
SURVIVES — it is not on F260's Design list — and takes six names from the dying pair, including
`validate_paths`, `get_trust_report`, `TrustStatus` and `Severity`, which supply two of the seven checks
in `verify_provider_patch_material`: `paths_safe` and `trust_report_accepted`. Removing them makes that
function's `v.ok` EASIER to satisfy, which would be a weakening in the unsafe direction. IT IS NOT
REACHABLE. Measured by walking every call site in the surviving tree: after the pair dies,
`verify_provider_patch_material` has NO caller under `packages/` or `apps/` — only its own tests — and
`materialize_provider_repair`, `load_material_manifest`, `revoke_material`, `read_material_patch` and
`export_materialization_result_json` have no caller at all. Only `load_materials` survives, called by
`orchestrator_brain.py` and `ui_server.py`, and it is a pure read of material that already exists on
disk, because the command that created material dies with the handler. So `provider_patch_material.py`
is reduced to ONE reachable function while remaining undeletable under this feature's scope, which is
itself owed a finding naming the feature that should reap it.

THE THIRD QUESTION IS NOT ANSWERED, AND IT IS WHY THIS ROUND GETS A FRESH SESSION. It surfaced only in
the applied dry run, after both rulings above were settled. `packages/orchestration/orchestrator_brain.py`
carries a live option-generating path that ADVERTISES A COMMAND THIS ROUND DELETES, and unlike the
neighbouring trust-signal blocks it is NOT dead after the deletion:

    orchestrator_brain.py:550  if sig.get("self_attempts_awaiting", 0) > 0:
    orchestrator_brain.py:552      command=(f"remedy provider intake-repair {job_id} --input <file> "
    orchestrator_brain.py:553               f"--provider self_dogfood --json"),

`self_attempts_awaiting` is computed from the SELF-DOGFOOD attempt store, which survives this round
untouched, so the condition still fires and the brain still tells a user to run
`remedy provider intake-repair` — a command that will not exist. That is the R-0861 class arriving
through a live code path rather than through a documentation page, and no gate in the repository can see
it: `tests/cli/test_advertised_commands.py` scans scripts and documentation, never production source,
and deleting the whole `provider` group additionally removes it from that guard's `GROUPS`, which is
R-0847. The deeper problem is that this is the ONLY route by which an external candidate enters a
self-improvement attempt, so deleting it removes a capability with no replacement anywhere in the
surviving tree, and `OptionKind.IMPORT_CANDIDATE` together with the `self_attempts_awaiting` path
becomes a dead end rather than dead code. Whether the round deletes that option, or the whole
self-dogfood external-candidate path with it, or registers the loss and leaves the surviving code
unreachable, is a ruling with real product consequences that this feature's own record does not settle.
Round 21's first work is therefore a dated DECISION in `.agent/decisions.md`, before the first
`git rm`, exactly as round 20's D9 was — with the alternatives and the reversal recorded.

THE REST OF THE RESIDUE, MEASURED AT THE END OF THE DRY RUN so the next session does not rediscover it
piecemeal, as this one did. A twenty-six-token sweep over the applied tree leaves 142 raw lines across
47 files. Read the RAW list rather than a count: a large minority are FALSE POSITIVES on the token
`verification_passed`, which is the job VERIFIER's stream event and has nothing to do with provider
trust — it lives in `apps/cli/commands/job.py`, `apps/ui/src/api/humanizeCatalog.ts`,
`packages/orchestration/context_coverage.py` and four documentation pages, and none of it is touched.
The REAL residue is: seventeen lines in `orchestrator_brain.py`, being the `PROVIDER_TRUST_VERIFICATION`
`OptionKind` and its `_BASE_SCORE` entry, three option blocks, the `trust_accepted` / `trust_rejected`
signal defaults and the situation-key fields that read them; THREE `related=` tuples in
`apps/cli/command_catalog.py` at lines 2726, 2742 and 2801 that name `provider.intake-repair` and would
become the FIRST dangling references this feature has created, which R-0859 forbids by name; the
coverage-table row for the deleted handler in `docs/system/quality-baseline-v0.md`; and SIX
documentation pages — `docs/system/provider-trust-gate-v0.md` and
`docs/system/provider-trust-verification-v1.md` die whole, while
`docs/system/provider-patch-materialization-v0.md`, `docs/system/repair-request-builder-v0.md`,
`docs/system/self-dogfood-execution-v0.md` and `docs/archive/candidate-generator-adapter-future.md` lose
the paragraphs and command advertisements that name the deleted flow, and every one of them needs its
`docs/README.md` index row checked. Three roadmap feature files under `docs/roadmap/features/` name the
pair as history prose and are the legitimate survivor class, exactly as in rounds 19 and 20.

WHAT THE DRY RUN ALREADY PROVED WORKS, so the next session may rely on it: the three moved chunks were
located BYTE-IDENTICALLY in `provider_trust.py` and appended to a destination verified collision-free;
all seven repoints and all four dead-code-path deletions applied against unique anchors; the catalog's
`provider` section was removed as a whole block bounded by the next section comment and yielded exactly
the five expected ids; the map lost exactly eight edge lines; the allowlist lost exactly three entries;
and the order file lost its last component line. What the dry run did NOT reach is a green suite, because
the residue above was still on disk when the ruling question surfaced.

## Session 11 ends here — ONE delegated round, PASS, independently re-gated

Stated plainly rather than dressed up, because the number is below the floor.
`docs/agents/self_drive_protocol.md` G7, as amended by amend0905-throughput, targets SIX TO EIGHT
delegated rounds per session with FOUR as the floor, and this session ran ONE. That is a real shortfall
and it is reported as one.

THE REASON IS THE ONE amend0905 SANCTIONS, AND IT IS OFFERED AS A MEASUREMENT RATHER THAN AS A FEELING:
round 21 is a round that explicitly needs a fresh session. The measurement is the three lines of
`orchestrator_brain.py` quoted above — a surviving, still-firing code path that advertises a command the
round deletes, guarding the only route by which an external candidate enters a self-improvement attempt,
with no replacement anywhere in the surviving tree. That question is not settled by anything on disk, it
surfaced only after the applied dry run had already settled the round's other two rulings, and authoring
a 2100-line deletion against an unmade ruling is what this feature's own record shows costs a round. It
is the same category of reason session 10 gave for round 20, which then landed clean, and the same
category session 9 gave for round 18. THE OTHER SANCTIONED REASON IS EXPLICITLY NOT CLAIMED: operator
amendment amend0908-f275-finish rule 5 permits "authoring errors accumulating" to end a session only
after at least four delegated rounds, this session ran one, so that reason is unavailable and is not
being used. Nor is context claimed as exhausted; it is long but it is not the reason.

WHAT THIS SESSION LANDED. Round 20, the `worker_registry` module group at 1035 module lines over 23
paths, 45 insertions against 2218 deletions, taking the whole `route-policy` command group with its
`GroupDef`, the three `worker.registry-*` commands, a handler file, a cockpit section, four
`ContractAction` members, three test files and TWO whole documentation pages with their three index
rows. Its substance is DECISION F275 D9: the surviving `token_economy.py` degrades FAIL-SAFE rather than
dying with the registry, because that module's approval disjunction already ended in `or not spec` and
nothing resolves a spec now, so the R-0095 hard-safety floor survives by degradation and approval became
UNCONDITIONAL — strictly stricter than the rule it replaces. A mutation red-proof shows the fail-safe is
pinned by five tests including the module's own R-0099 audit invariant, rather than merely written.
Finding R-0865 was registered for the capability genuinely lost, naming F110 as the inheritor. The full
suite is green at 18454 passed, 23 skipped and ZERO failed. FOURTEEN of F260's prototype-cluster module
groups are now gone and ONE component remains in `.agent/f275_deletion_order.md`.

CONTEXT SELF-ASSESSMENT, as amend0905-throughput requires in one sentence: the reviewer's context is
long but not exhausted and is NOT the reason this session ends — it ran four full serial suites, two
establishing round 20's boundaries by an applied dry run and two as independent re-gates, and it ends on
round 21's ruling being surfaced and measured rather than on the reviewer running out of room.

## What the next session owes, in order

FIRST, Phase 1 rule 1: re-read `.agent/STOP` from disk before the Open PR Gate. It does not exist as
this session ends and was measured absent at the Phase 0 probe and again before the round. Then the Open
PR Gate: no pull request is open, and none is owed until the closure sequence.

SECOND, round 21's FIRST substantive commit books, from this file as the durable carrier under
amend0827-process-diet rule 1: the ROUND 20 PASS verdict above as a `Gate: F275 R20` entry in
`.agent/live_review.md`, the R-0855 evidence paragraph as a `Note: F275 R21` entry beside it, and the
three prose slips as dated lines in `.agent/prose_slips.md`. The open set is 88 by distinct id and the
next free id is R-0866.

THIRD, round 21 itself, which completes T001. Rule the `orchestrator_brain` self-dogfood candidate-import
question as a dated DECISION BEFORE the first `git rm`. The other two rulings are already measured above
and should be recorded in that same DECISION rather than re-derived: the byte-identical move of the two
redaction helpers into the collision-free `packages/common/path_redaction.py`, and the unreachability of
`verify_provider_patch_material`'s two lost checks. Order the mutation red-proofs in full, because seven
surviving production modules keep a redaction call whose definition moves — the proof to order is that
`_scrub_public` still bites from its new home, over a node set that reaches at least
`real_test_execution.py` and `token_economy.py`. Expect roughly forty paths, six documentation pages and
three `related=` repairs that R-0859 forbids leaving dangling; the round is large but it is measured.
