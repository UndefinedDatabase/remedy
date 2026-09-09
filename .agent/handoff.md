# Handback — F275 ROUND 10 — round 9's PASS is booked, R-0845 and R-0846 are registered, and the FIFTH module group — the first that is a CYCLE — is gone with the tree green

This file supersedes the F275 round 9 handback. It is written by the delegated worker of F275
round 10 on the reviewer's authored text; the reviewer never edits a work-tree file. It carries
NO verdict of its own — verdicts live in `.agent/live_review.md`, and this round's C2 booked the
reviewer's authored F275 round 9 PASS there. C2 also REGISTERS R-0845 and R-0846, so the open set
moves 69 → 71 by distinct id (measured at G3(f): two registrations, no resolution). Block
constraint 2 forbids the worker writing any `Done:` paragraph, verdict, finding or registration
of its own, and none was written. The next free id after this round is R-0847.

THE FIFTH `git rm` OF F275, AND THE FIRST WHOSE ATOMIC UNIT IS A STRONGLY CONNECTED COMPONENT
RATHER THAN A MODULE. Six modules that import each other —
`packages/orchestration/dogfood_run.py` (1725 lines), `feature_planner.py` (1045),
`overnight_mission.py` (918), `progress_ledger.py` (2284), `repair_loop_v2.py` (1167) and
`self_repair_proposal.py` (813) — go in ONE commit under DECISION F275 D2 and operator
amendment amend0908-f275-finish RULE 3, together with their five `apps/cli/commands/*_cmd.py`
handler files, 38 `CommandEntry` blocks, the three `GroupDef`s of `dogfood`, `progress` and
`self-repair`, eleven test files whose subject is a dying module, five doc pages whose subject is
a dying module, five index rows, eleven allowlist lines, one map edge, six `CLUSTER_MODULES`
lines, five `pyproject.toml` lines, twelve test definitions across ten surviving files and the
regenerated deletion-order file — ONE commit, `e9944c64`, **31 insertions against 14365 deletions
over 55 paths**, exactly the figures the block states.

THE TWO SURVIVORS THAT LOSE BEHAVIOUR, AND WHY BOTH ARE REGISTERED RATHER THAN STUBBED.
`apps/cli/commands/worker_facade_cmd.py` SURVIVES and loses the dogfood half of
`remedy mission run`: `_cmd_mission_run` carried TWO modes on one name, resolved between by
`_names_a_mission`, and the second mode was a real
`from packages.orchestration.dogfood_run import run_mission_loop` in the function body — a live
production code path, not the string-keyed `importlib` probe an inherited map recorded. The
resolver and the second mode both die; the command now resolves exactly one object.
`packages/orchestration/main_builder_adapter.py` SURVIVES and loses its
`remedy repair evaluate` next-action, which becomes the empty string with a comment saying where
a reader would search for it that no surviving command evaluates a repair WORK ITEM. Both losses
are user-observable, so operator RULE 4 obliges a finding naming the inheriting feature, and
R-0845 and R-0846 in C2 are those findings. No stub, shim, alias or compatibility reader was
written anywhere: AGENTS.md Scope Control forbids them by name.

## Session

`SESSION 6 of feature F275 · round 10 · rounds so far 10`

CONTEXT SELF-ASSESSMENT (operator amendment amend0905-throughput): this worker's context is
comfortable. The round cost one block read, twelve ordered edit steps over 55 paths and eight
gates; the only long wall-clock items were the 23m32s serial full suite and two base-side
collections. Nothing was re-read twice and no gate needed a second attempt. F275's soft limit is
20 sessions and 60 rounds by operator amendment amend0908-f275-finish RULE 1, and the feature
stands at session 6, round 10 — well inside it, so no scope report is owed.

## Range

Review of `982d016b`..`HEAD`.

## Commits

### d6c7694a  F275 R10 C0a: save the round 10 block verbatim under .agent/authored.
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r10.md` | +444/-0 | the block saved verbatim by `shutil.copyfile` (A) |

### bf9ffe68  F275 R10 C0b: mirror the round 10 block into last_block.
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +417/-373 | the SAME bytes mirrored by `shutil.copyfile` |

### ccf684bd  F275 R10 C1: the round 10 plan.
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +28/-24 | replaced WHOLE by the PLAN10 slice, 2948 bytes, 49 lines |

### eac1082e  F275 R10 C2: book the round 9 PASS and register R-0845 and R-0846.
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +6/-0 | LEDGER10 appended: `Gate: F275 R9`, `- R-0845`, `- R-0846` |
| `.agent/prose_slips.md` | +6/-0 | SLIPS10 appended: three dated F275 R10 lines |

### e9944c64  F275 R10 C3: delete the six-module prototype component and its call sites.
| Path | +/- | Reason |
|---|---|---|
| `.agent/f275_deletion_order.md` | +0/-1 | REGENERATED from `measured_order()`; eleven components → ten |
| `apps/cli/command_catalog.py` | +0/-489 | the 38 `CommandEntry(` blocks and 3 `GroupDef` lines |
| `apps/cli/commands/__init__.py` | +1/-6 | 5 handler imports and 5 names out of the `for mod in (…)` tuple |
| `apps/cli/commands/dogfood_cmd.py` | +0/-281 | handler, deleted whole (D) |
| `apps/cli/commands/overnight_mission_cmd.py` | +0/-156 | handler, deleted whole (D) |
| `apps/cli/commands/progress_cmd.py` | +0/-57 | handler, deleted whole (D) |
| `apps/cli/commands/repair_loop_v2_cmd.py` | +0/-187 | handler, deleted whole (D) |
| `apps/cli/commands/self_repair_cmd.py` | +0/-213 | handler, deleted whole (D) |
| `apps/cli/commands/worker_facade_cmd.py` | +14/-61 | `_names_a_mission` gone, `_cmd_mission_run` replaced by CODE1, 2 probes gone |
| `docs/README.md` | +0/-5 | the five index rows of the five deleted pages |
| `docs/guides/overnight-mission-user-guide-v0.md` | +0/-70 | doc page, deleted whole (D) |
| `docs/guides/token-aware-repair-loop-user-guide-v1.md` | +0/-83 | doc page, deleted whole (D) |
| `docs/system/development-artifact-boundary-v0.md` | +1/-5 | 2 table rows, 1 bullet, 1 row; `Mission status` re-sourced |
| `docs/system/open-ended-dogfood-run-orchestrator-replay-analyzer-v0.md` | +0/-173 | doc page, deleted whole (D) |
| `docs/system/overnight-mission-contract-review-repair-spine-v0.md` | +0/-114 | doc page, deleted whole (D) |
| `docs/system/real-test-execution-snapshot-rollback-proof-v1.md` | +0/-6 | the whole `## Mission contract gate relationship` section |
| `docs/system/run-contract-v1.md` | +0/-2 | the `progress_ledger` and `feature_planner` bullets |
| `docs/system/snapshot-rollback-v1.md` | +0/-2 | the `progress_ledger.py` and `feature_planner.py` table rows |
| `docs/system/token-aware-repair-loop-v1-v2.md` | +0/-105 | doc page, deleted whole (D) |
| `packages/orchestration/dogfood_run.py` | +0/-1725 | module, deleted whole (D) |
| `packages/orchestration/feature_planner.py` | +0/-1045 | module, deleted whole (D) |
| `packages/orchestration/main_builder_adapter.py` | +5/-2 | CODE2-FROM → CODE2-TO, the `repair evaluate` next-action |
| `packages/orchestration/overnight_mission.py` | +0/-918 | module, deleted whole (D) |
| `packages/orchestration/progress_ledger.py` | +0/-2284 | module, deleted whole (D) |
| `packages/orchestration/repair_loop_v2.py` | +0/-1167 | module, deleted whole (D) |
| `packages/orchestration/self_repair_proposal.py` | +0/-813 | module, deleted whole (D) |
| `pyproject.toml` | +0/-5 | 1 `per-file-ignores` entry and 4 mypy `module = [` entries |
| `scripts/remedy_test_fast.sh` | +0/-2 | the two deleted test files' lanes |
| `tests/cli/test_cli_ux.py` | +3/-3 | 2 group names out of two rosters (see deviation 1) |
| `tests/cli/test_overnight_mission_cli.py` | +0/-89 | test file, deleted whole (D) |
| `tests/cli/test_progress_feature_runtime.py` | +0/-73 | test file, deleted whole (D) |
| `tests/cli/test_repair_loop_v2_cli.py` | +0/-94 | test file, deleted whole (D) |
| `tests/cli/test_self_repair_cmd.py` | +0/-203 | test file, deleted whole (D) |
| `tests/cli/test_worker_facade_cmd.py` | +1/-27 | 1 test, 1 assertion, `MagicMock`, `_MISSION_LOOP` |
| `tests/orchestration/cluster_deletion_map.txt` | +0/-1 | the one `dogfood_run <- worker_facade_cmd.py` edge |
| `tests/orchestration/import_reachability_allowlist.txt` | +0/-11 | 6 modules + 5 handlers |
| `tests/orchestration/test_builder_routing.py` | +0/-94 | class `TestEmittedCommandsRunnable` |
| `tests/orchestration/test_cluster_deletion_map.py` | +1/-7 | 6 `CLUSTER_MODULES` lines + the docstring example |
| `tests/orchestration/test_development_artifact_boundary.py` | +0/-27 | 2 methods + 3 allowlist string lines |
| `tests/orchestration/test_do_continue.py` | +0/-43 | class `TestContinuationIntegrations` |
| `tests/orchestration/test_dogfood_run.py` | +0/-1194 | test file, deleted whole (D) |
| `tests/orchestration/test_feature_planner.py` | +0/-264 | test file, deleted whole (D) |
| `tests/orchestration/test_local_model_advisor.py` | +0/-18 | method `TestAdvisorImpact.test_advisor_dict_redacted_for_downstream` |
| `tests/orchestration/test_main_builder_adapter.py` | +5/-2 | CODE3-FROM → CODE3-TO, the assertion R-0846 describes |
| `tests/orchestration/test_model_route_tournament_integration.py` | +0/-44 | classes `TestProgressLedger`, `TestFeatureSuggestions` |
| `tests/orchestration/test_overnight_mission.py` | +0/-285 | test file, deleted whole (D) |
| `tests/orchestration/test_overnight_mission_integration.py` | +0/-28 | class `TestProgressLedger` |
| `tests/orchestration/test_progress_ledger.py` | +0/-388 | test file, deleted whole (D) |
| `tests/orchestration/test_progress_redaction.py` | +0/-105 | test file, deleted whole (D) |
| `tests/orchestration/test_real_test_execution.py` | +0/-40 | class `TestMissionGates` |
| `tests/orchestration/test_repair_loop_v2.py` | +0/-443 | test file, deleted whole (D) |
| `tests/orchestration/test_self_repair_proposal.py` | +0/-800 | test file, deleted whole (D) |
| `tests/orchestration/test_token_economy_integration.py` | +0/-59 | classes `TestProgressLedger`, `TestFeatureSuggestions` |
| `tests/orchestration/test_worker_route_integration.py` | +0/-45 | classes `TestProgressLedgerItems`, `TestFeatureSuggestions` |
| `tests/test_test_categories.py` | +0/-1 | the one `"test_dogfood_run.py",` line |

### C4 — the commit that writes this file
A handoff cannot table the commit that writes it (R-0149 pattern). C4 changes exactly one path,
`.agent/handoff.md`, rewritten whole; it is the only commit of this round outside the block's
C0a–C3 range and carries no other file.

## External actions

| Action | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/r10-redproof e9944c64` | created for G5(e); REMOVED and pruned |
| `git worktree add --detach .remedy-wt/r10-base 982d016b` | created for G6's base-side ruff; REMOVED and pruned |
| `git worktree add --detach .remedy-wt/r10-base2 982d016b` | created for G7's base-side id set; REMOVED and pruned |
| `git worktree remove --force` ×3, `git worktree prune -v` | `git worktree list` names the primary checkout ALONE |
| `git push -u origin feature/f275-one-world-completion-part-three` | issued ONCE, after C4 |

No pull request was created, none was merged, nothing was force-pushed, no history was rewritten.
The `remedy` CLI is denied in this environment and was never invoked; no gate needs it.

## Verification

Every gate was RUN. Exit codes are read from the process object, never through a pipe.

- **G1 TRANSPORT** — exit 0. `.agent/authored/f275-r10.md` @`d6c7694a` and `.agent/last_block.md`
  @`bf9ffe68` are each 41781 bytes at sha256
  `cd016eb03ec8698d0b61eee5bf1a5fb1e42d78750eef66c41ff150e605d2ca10`, equal to each other and to
  the pair the delegation states. Per §3 item 37 this claims nothing about the bytes the reviewer
  emitted — all three artefacts are this worker's output.
- **G2 THE PLAN** — exit 0. `.agent/plan.md` @`ccf684bd` is 2948 bytes at sha256
  `8e583c36e2f8f12a29f7ac446ed822d8492a3e37d092ae5f6dfea1e7eba65643`, byte-identical to the
  PLAN10 slice, 49 lines against the AGENTS.md cap of 50.
- **G3 THE RECORD** — exit 0, read from the committed blobs at C1 (pre) and C2 (post), never from
  the worktree. (a) `.agent/live_review.md` 559516 → 569448, growth 9932 = 1 + 9931;
  `.agent/prose_slips.md` 175541 → 177821, growth 2280 = 1 + 2279. (b) pre-blob a byte-exact
  PREFIX and the slice a byte-exact SUFFIX of each post-file; joining bytes at offsets 559516 and
  175541 both read back as `b'\n'`. (c) N COUNTED from each slice = 3 and 3; the file's last N
  blank-line-separated units equal the slice's N paragraphs IN ORDER, per-unit sha256 printed and
  all six equal. (d) negative controls flipped one byte IN MEMORY inside the FIRST appended
  paragraph of each file (offsets 561540 and 175997) and were REJECTED by both reader (b) and
  reader (c); both tracked files re-read from disk afterwards are byte-equal to the committed
  post-blobs. (e) `^Gate: ` 31 → 32, and `^Gate: F275 R9 `, `^- R-0845 — `, `^- R-0846 — `
  exactly 1 each. (f) THE OPEN SET BY DISTINCT ID: 73/4/**69** open before, 75/4/**71** open
  after — registrations +2, resolutions +0.
- **G4 THE DELETION IS COMPLETE** — exit 0. `git ls-tree -r e9944c64 --name-only` over 4606
  tracked files prints **False for all 27** deleted paths. The whole-word sweep over the 1726
  tracked files EXCLUDING `.agent/` and `.data/` finds **12 distinct remaining lines** (15
  module-line pairs: `dogfood_run` 2, `feature_planner` 1, `overnight_mission` 4,
  `progress_ledger` 5, `repair_loop_v2` 2, `self_repair_proposal` 1), every line printed in full,
  never truncated. **Every one of the 12 is a must-not-touch item**: 11 in
  `docs/roadmap/features/` (`T1_F034.md`, `T2_F260.md` ×5, `T2_F269.md`, `T2_F272.md`,
  `T2_F277.md` ×3) and 1 at `docs/system/vocabulary.md:245`, which step (11) names as a survivor.
  **Zero lines outside those areas**, so the gate's own failure condition — "a line that is NOT
  one of those" — did not trigger. The block predicted 28 lines; see deviation 2. Zero-gated
  symbols: `_names_a_mission` 0, `run_mission_loop` 0, `list_self_repair_proposals` 0,
  `build_progress_ledger` 0, `build_feature_plan` 0, `_cmd_mission_run` in
  `apps/cli/commands/dogfood_cmd.py` 0 (the file is absent from the tree);
  `build_mission_morning_report` is **1**, not 0 — see deviation 3.
- **G5(a) RATCHETS** — `python3 -B -m pytest tests/orchestration/test_import_reachability.py
  tests/orchestration/test_cluster_deletion_map.py
  tests/orchestration/test_cluster_deletion_order.py
  tests/orchestration/test_main_builder_adapter.py -q` → **exit 0, 60 passed in 5.41s**.
- **G5(b) DOCS AND CANARY** — `python3 -B -m pytest tests/docs/ -q` → **exit 0, 303 passed in
  0.67s**; `python3 -B -m pytest tests/cli/test_golden_path.py -q` → **exit 0, 42 passed in
  20.50s**.
- **G5(c) THE SHIPPED READERS** — exit 0, through `apps.cli.command_catalog` and
  `apps.cli.commands`, not by grep. `len(_BASE_CATALOG)` **334 → 296**,
  `len(collect_all_handlers())` **334 → 296**, `len(GROUPS)` **59 → 56**. All **38** dying ids
  ABSENT from both readers (printed one per line); all **10** named survivors PRESENT in both;
  `dogfood`, `progress`, `self-repair` absent from `GROUPS` while `overnight` and `repair` are
  present.
- **G5(d) THE ORDER FILE** — exit 0. `.agent/f275_deletion_order.md` holds **TEN** components at
  C3 against **eleven** at the base; new first body line
  `packages.orchestration.builder_routing, packages.orchestration.candidate_quality,
  packages.orchestration.local_candidate_generator, packages.orchestration.model_route_tournament`;
  `git show --numstat e9944c64 -- .agent/f275_deletion_order.md` reads **`0	1`**. The 26-line
  comment header was carried byte for byte (sha256 of the header text
  `aff913e6eedb4d9c7e5ab6e76578be881ffffa3612018cf58b5a48ad508b0cc2`) and the body was rendered by
  `", ".join(component)` over `measured_order()`; the file was never hand-edited.
- **G5(e) THE RED-PROOF** — run in the disposable worktree `.remedy-wt/r10-redproof` at C3 and
  NOWHERE ELSE, `__pycache__` purged before every run, `python3 -B` and
  `PYTHONDONTWRITEBYTECODE=1` throughout, selection = the four-file command of G5(a). Each FROM
  string was counted in its own named file first and was exactly 1; each mutation was applied
  ALONE, reverted, and the revert re-checked by sha256 (all three matched their pre-mutation
  digest). **THE COLOUR SEQUENCE, IN ORDER**: control **exit 0, 60 passed** → (i) `CLUSTER_MODULES`
  regains `dogfood_run` **exit 1, 2 failed** → (ii) the allowlist regains
  `packages.orchestration.dogfood_run` **exit 1, 1 failed** → (iii) `main_builder_adapter.py`
  regains CODE2-FROM's second line **exit 1, 1 failed** → control **exit 0, 60 passed**. The
  worktree's `git status --porcelain` was empty after the proof, and the worktree was removed and
  pruned.
- **G6 RUFF AND BASH** — `python3 -m ruff check` over exactly the **18** `.py` files that
  `git diff --name-only 982d016b..e9944c64` names and that still exist at C3 → **`All checks
  passed!`, exit 0**. Repo-wide `python3 -m ruff check .` reads **`Found 26 errors.`, exit 1** at
  C3 and **`Found 26 errors.`, exit 1** at the base read in the disposable worktree
  `.remedy-wt/r10-base` at `982d016b` — the round adds none, and 26 is the ceiling
  `tests/orchestration/test_ci_budgets.py` holds. `bash -n scripts/remedy_test_fast.sh` →
  **exit 0**, no output.
- **G7 THE FULL SUITE** — `python3 -B -m pytest tests/ -q`, SERIALLY (no `-n auto`) in the PRIMARY
  checkout, exit code read from the process object → **exit 0, 19209 passed, 23 skipped, 1
  warning in 1412.72s (0:23:32)**. THE ARITHMETIC IS CLOSED BY THE ID SET, not by a file-level
  count: `--collect-only tests/` is **19613** at the base and **19232** at C3, a fall of **381**,
  with **0 ids gained**. Attributed: **325** in the eleven deleted test files, **32** across the
  ten files of step (8) (4+5+4+4+3+2+6+2+1+1, printed per file), **24** in
  `tests/test_grouped_cli.py`, which the deletion never names and which parametrises over the
  catalog, and **0 anywhere else**. 325 + 32 + 24 = 381 exactly. 19232 collected = 19209 passed +
  23 skipped. The base-side COUNT was taken before C3 while the code tree was byte-identical to
  `982d016b` (proved by an empty `git diff --stat 982d016b..HEAD -- . ':(exclude).agent'`); the
  base-side ID SET was taken in the disposable worktree `.remedy-wt/r10-base2` at `982d016b`.
- **G8 THE TREE** — exit 0. `.agent/STOP` re-read from disk: **absent**. `git status --porcelain`:
  **empty**. `git worktree list`: **the primary checkout ALONE**. Branch:
  **`feature/f275-one-world-completion-part-three`**. SET COMPARISON: `git diff --name-only
  982d016b..e9944c64` names **60** paths, not 55 — the five extra are the block's own C0a/C0b/C1/C2
  `.agent/` writes, listed with their commit in deviation 4; **nothing is MISSING**. The exact-55
  match holds for C3's own commit, `git diff --name-only eac1082e..e9944c64`: **55 paths, EXACT SET
  MATCH, nothing extra, nothing missing**. Every commit C0a–C3 is **single-parent**, with
  insertions **444, 417, 28, 12, 31** — all under the AGENTS.md DECISION F104 D1 cap of 500. C4's
  own numbers belong to the next round's ledger entry (§3 items 14 and 31) and are not claimed here.

## Authored-text proofs

| Text | Proof |
|---|---|
| the block | `shutil.copyfile` from the delegation's file to `.agent/authored/f275-r10.md` and to `.agent/last_block.md`; both re-read at 41781 bytes / `cd016eb0…5d2ca10`, equal to the delegation's stated pair and to each other (G1) |
| PLAN10 | extracted as the bytes STRICTLY between its BEGIN and END marker lines; verified 2948 bytes / `8e583c36…ba65643` against its own BEGIN line BEFORE use; committed blob re-verified at G2 |
| LEDGER10 | extracted the same way; verified 9931 bytes / `e21bd30f…c6a6a611` before use; committed blob re-verified at G3 as a byte-exact SUFFIX with per-paragraph sha256 |
| SLIPS10 | extracted the same way; verified 2279 bytes / `cda11055…6145ce45` before use; committed blob re-verified at G3 the same way |
| CODE1, CODE2-FROM/TO, CODE3-FROM/TO | extracted verbatim from the COMMITTED `.agent/authored/f275-r10.md` by header line and blank-line run, never retyped; each FROM string counted in its own named file and required to be exactly 1 before replacement (both were 1) |

No slice was edited, reflowed, rewrapped, corrected or renumbered.

## Deviations & assumptions

The block's ORDERED COMMIT SEQUENCE was followed exactly: C0a, C0b, C1, C2, C3, C4, in that order,
no extra commit, none dropped, none reordered. C3 is ONE commit carrying all 55 paths, per
constraint 3. C2 precedes C3, per constraint 4. `.agent/plan.md` was advanced at C1, per
constraint 5. `.agent/STOP` was re-read from disk before C0a and again at G8, absent both times,
per constraint 8.

**1. Step (8), `tests/cli/test_cli_ux.py`: one of the three named strings does not exist.** The
block orders removing `"self-repair"`, `"dogfood"` and `"progress"` from `_INTERNAL_GROUPS`. The
first two are present and were removed. **`"progress"` does not occur anywhere in that file** —
`grep -n progress tests/cli/test_cli_ux.py` returns nothing at the base `982d016b` and nothing at
C3. `_INTERNAL_GROUPS` holds `tournament, local-candidate, candidate-quality, route-policy, token,
context-pack, self-repair, execution, builder, dogfood, snapshot, contract, integrity` and never
held `progress`. The block's own `+3/-3` numstat for this file is reached EXACTLY without it —
one changed line in each of the two `_INTERNAL_GROUPS` rows and one in the wrapped list inside
`TestNoInternalInDefault.test_no_internal_names` — and the measured numstat is `3 3`. Nothing was
invented to make the third removal happen and the change set is unaffected.

**2. G4: the sweep is CLEANER than the block predicts, and the missing lines are the ones step
(11) removes.** The block states 28 remaining lines — `dogfood_run` 6, `feature_planner` 3,
`overnight_mission` 7, `progress_ledger` 8, `repair_loop_v2` 3, `self_repair_proposal` 1 — split
18 in `docs/roadmap/features/`, 1 in `docs/system/vocabulary.md` and 9 in other `docs/system/`
pages. MEASURED at C3 over the same scope: **12 distinct lines** (15 module-line pairs, since two
lines name several modules), split **11 / 1 / 0**. The gap is accounted for: the four
`docs/system/` pages this round EDITS held **10** matching lines at `982d016b` and hold **0** at
C3 — `development-artifact-boundary-v0.md` 5 → 0, `run-contract-v1.md` 2 → 0,
`snapshot-rollback-v1.md` 2 → 0, `real-test-execution-snapshot-rollback-proof-v1.md` 1 → 0 — each
line printed in the gate transcript with its base line number. So the block's 28 appears to have
been counted BEFORE step (11)'s doc edits were applied. This is a numeral disagreement in the
reviewer's favour: the gate's stated failure condition is "if your sweep finds a line that is NOT
one of those, that is a real miss", and no such line exists. Nothing was fixed, because nothing
was missed.

**3. G4: `build_mission_morning_report` is 1, not 0, and the 1 is a guard asserting its absence.**
The single occurrence is `tests/cli/test_mission_cmd.py:1469`, the line
`assert "build_mission_morning_report" not in source` inside
`test_the_facade_module_no_longer_names_the_cluster_builder`, which reads
`apps/cli/commands/worker_facade_cmd.py` and asserts the symbol is NOT there. The line is present
verbatim at the base `982d016b` at the same line number, and `tests/cli/test_mission_cmd.py` is
NOT in this round's change set, so this round neither created it nor could remove it without
widening the change set — which was not done. The symbol has zero LIVE references: the gate's
intent holds. The other five zero-gated symbols and `_cmd_mission_run` in the deleted handler are
all genuinely 0.

**4. G8: `git diff --name-only 982d016b..<C3>` cannot name exactly 55 paths, by the block's own
construction.** That range spans C0a, C0b, C1, C2 and C3, and the same block orders `.agent/`
writes in the first four. The range names **60** paths: the 55 of the change set plus
`.agent/authored/f275-r10.md` (C0a), `.agent/last_block.md` (C0b), `.agent/plan.md` (C1),
`.agent/live_review.md` (C2) and `.agent/prose_slips.md` (C2) — exactly the block's own declared
"six `.agent/` paths across C0a, C0b, C1, C2 and C4" minus `.agent/handoff.md`, which belongs to
C4 and lies outside the range. Nothing is MISSING and nothing unaccounted-for is present. The
EXACT-55 set match the gate is asking for holds when scoped to C3's own commit,
`git diff --name-only eac1082e..e9944c64`: 55 paths, nothing extra, nothing missing. Both readings
are printed in the G8 transcript.

**5. Method note on base-side readings (not a defect, stated because the gates name a route).**
G6's base-side repo-wide ruff was read in a disposable worktree at `982d016b`, as the gate words
it (`Found 26 errors.`). An earlier read taken in the primary checkout BEFORE C3, while the code
tree was byte-identical to the base, gave the same 26; both are reported. G7's base-side
collection COUNT (19613) was taken before C3 in the primary checkout under that same
byte-identity, which the gate explicitly permits — and the base-side ID SET needed to close the
381 arithmetic was taken in a disposable worktree at `982d016b`. No base-side reading ever wrote
to the primary checkout, and no overwrite-and-restore was used anywhere (constraint 6, §3 item 29).

**6. One correction to my own tooling, declared for completeness.** The AST-based remover of step
(8) initially consumed the file-terminating empty element of
`tests/orchestration/test_development_artifact_boundary.py` as part of the "blank run that
FOLLOWS" the last removed method, which would have deleted the blank line PRECEDING it and made
that file `+0/-28` instead of the block's `+0/-27`. This was caught by comparing against the
block's stated numstat before C3, corrected in the working tree before any commit, and verified:
the committed file is exactly the base's lines 1–239 minus the three allowlist strings, numstat
`0 27`. No commit ever carried the wrong version.

No gate went red. No question arose that the rules do not answer. The change set was never
widened: every path written is one of the 55 of C3 or one of the six `.agent/` paths the block
names.

## Item-status table

The block's ordered items are its six commits and its twelve deletion steps. Every one appears
exactly once.

| Item | Status | Reason |
|---|---|---|
| C0a save the block to `.agent/authored/f275-r10.md` | done | `shutil.copyfile`, `d6c7694a` |
| C0b mirror to `.agent/last_block.md` | done | `shutil.copyfile`, same bytes, `bf9ffe68` |
| C1 `.agent/plan.md` replaced by PLAN10 | done | byte-identical, `ccf684bd` |
| C2 append LEDGER10 and SLIPS10 | done | both appends byte-exact, `eac1082e` |
| C3 the deletion, all 55 paths, ONE commit | done | 31 insertions / 14365 deletions, `e9944c64` |
| C4 `.agent/handoff.md` rewritten | done | this file |
| (1) `git rm` the 27 whole files | done | all 27 absent from `git ls-tree -r e9944c64` |
| (2) 38 `CommandEntry` blocks + 3 `GroupDef` lines | done | `+0/-489`; 334 blocks parsed, 38 matched by `command_id`, 3 `GroupDef` lines each unique |
| (3) 5 handler imports + the `for mod in (…)` tuple | done | `+1/-6`; tuple 64 → 59 names |
| (4) `worker_facade_cmd.py`: 2 probes, `_names_a_mission`, CODE1 | done | `+14/-61`; banner comment untouched |
| (5) `main_builder_adapter.py` CODE2-FROM → CODE2-TO | done | `+5/-2`; FROM count was 1 |
| (6) `test_main_builder_adapter.py` CODE3-FROM → CODE3-TO | done | `+5/-2`; FROM count was 1 |
| (7) the ratchet inputs | done | `+0/-11`, `+0/-1`, `+1/-7`; docstring example re-pointed at `builder_routing` |
| (8) the surviving tests | deviated | all twelve named definitions and both extra edits done; `"progress"` is absent from `_INTERNAL_GROUPS` — deviation 1. `TestMissionRun` keeps `test_run_no_run_id` and is not empty |
| (9) `.agent/f275_deletion_order.md` REGENERATED | done | eleven → ten components, numstat `0 1`, header byte-for-byte |
| (10) `pyproject.toml`, `remedy_test_fast.sh`, `test_test_categories.py` | done | `+0/-5`, `+0/-2`, `+0/-1` |
| (11) the doc edits | done | `+0/-5`, `+1/-5`, `+0/-2`, `+0/-2`, `+0/-6`; `docs/system/vocabulary.md` NOT touched |
| (12) the five must-not-touch spec files | done | `T1_F034.md`, `T2_F260.md`, `T2_F269.md`, `T2_F272.md`, `T2_F277.md` all absent from the change set and unchanged in the range |
| R-0845 registration | done | reviewer's text, applied verbatim inside LEDGER10 at C2; exactly 1 `^- R-0845 — ` |
| R-0846 registration | done | reviewer's text, applied verbatim inside LEDGER10 at C2; exactly 1 `^- R-0846 — ` |

## Open findings

**71 open by distinct id** (75 registrations − 4 resolutions), measured at G3(f) from the
committed blob at C2. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's rather than
this feature's, per DECISION F272 D12. The next free id is R-0847.

## Next

The reviewer reviews `982d016b`..`HEAD`, re-runs the eight gates itself against the committed
blobs, and issues the round 10 verdict. Under operator amendment amend0827-process-diet rule 1
that verdict is booked into `.agent/live_review.md` by the FIRST commit of round 11, not by a
round of its own. Round 11's own work is the next component in the regenerated order file:
`packages.orchestration.builder_routing, …candidate_quality, …local_candidate_generator,
…model_route_tournament` — four modules that import each other, so DECISION F275 D2 makes the
whole component ONE commit. Before authoring it, Phase 1 rule 1: re-read `.agent/STOP` from disk.

## Reviewer verdict on round 10 — appended after the handback, by the reviewer's authored text

VERDICT ROUND 10: **PASS.** Written by the planner/reviewer of session 6 AFTER reading the
committed range `982d016b`..`57058636` and RE-RUNNING every one of the eight gates independently
against the committed blobs; the worker's report was not taken as evidence for any line below.
It is carried here because under `docs/agents/self_drive_protocol.md` a verdict that stays in
the session is lost, and it is booked into `.agent/live_review.md` by the FIRST substantive
commit of the next round, per amend0827-process-diet rule 1. It is NOT a `Done:` paragraph and
resolves no finding.

WHAT THE REVIEWER RE-MEASURED. Six single-parent commits C0a `d6c7694a`, C0b `bf9ffe68`,
C1 `ccf684bd`, C2 `eac1082e`, C3 `e9944c64` and C4 `57058636`, each parent read from
`git rev-list --parents`, with per-commit insertions 444, 417, 28, 12, 31 and 339, every one
under the AGENTS.md DECISION F104 D1 cap of 500. G1 IS THE PRIMARY PROOF OF §4 ITEM 9 AND NOT
THE DIGEST FALLBACK: the reviewer's own scratchpad original and the committed
`.agent/authored/f275-r10.md` and `.agent/last_block.md` are all 41781 bytes at
`cd016eb03ec8698d0b61eee5bf1a5fb1e42d78750eef66c41ff150e605d2ca10`, and the two committed blobs
compare byte-equal to the scratchpad original, so this round's chain does reach the emitted
bytes — which §3 item 37 says the digest-only form cannot. G2: `.agent/plan.md` byte-identical
to PLAN10 at 2948 bytes and 49 lines against the cap of 50. G3: `.agent/live_review.md` 559516
to 569448, growth 9932 = 1 + 9931; `.agent/prose_slips.md` 175541 to 177821, growth
2280 = 1 + 2279; both edges byte-exact with the joining byte read back as a newline; N counted
from each slice by the reviewer's own reader as 3 and 3 with ordered equality holding over the
WHOLE appended region and a per-unit sha256 printed for all six units; and BOTH negative
controls — flipped in memory inside the FIRST appended paragraph, per §3 item 36 — REJECTED by
both readers, with the tracked files re-read from disk afterwards and byte-equal to the
committed post-blobs. `^Gate: ` 31 to 32, and `^Gate: F275 R10`'s three keys `^Gate: F275 R9 `,
`^- R-0845 — ` and `^- R-0846 — ` exactly 1 each, with THE OPEN SET 69 TO 71 BY DISTINCT ID
against registrations 73 to 75 and resolutions 4 to 4. G4: all 27 whole-file removals absent
from `git ls-tree` at C3 over 4606 tracked files, and the whole-word sweep for the six module
names over the 1726 tracked files outside `.agent/` and `.data/` printed IN FULL — 15
module-name hits on 12 DISTINCT lines, every one a must-not-touch item: eleven in
`docs/roadmap/features/` (`T1_F034.md`, `T2_F260.md`, `T2_F269.md`, `T2_F272.md`, `T2_F277.md`)
and one at `docs/system/vocabulary.md` line 245, which step (11) names and deliberately keeps.
Eight of the nine gated symbols read ZERO; the ninth is deviation 3 below. G5: the four ratchets
60 passed at exit 0, `tests/docs/` 303 passed, the canary 42 passed; through the SHIPPED readers
`_BASE_CATALOG` and `collect_all_handlers()` both fell 334 to 296 and `GROUPS` 59 to 56, with
all 38 deleted ids ABSENT from both readers, all ten named survivors PRESENT in both,
`dogfood`, `progress` and `self-repair` gone from `GROUPS` while `overnight` and `repair`
remain, and zero duplicate command ids; the regenerated order file holds TEN components against
eleven at a `0 1` numstat, a PURE DELETION, with its 26-line header intact. THE RED-PROOF WAS
RE-RUN BY THE REVIEWER IN ITS OWN DISPOSABLE WORKTREE AT `e9944c64`: control exit 0 at 60
passed, then the three mutations exit 1 at 2, 1 and 1 failures, then the control exit 0 again,
each FROM string counted unique in its named file first and each file reverted byte-identically
by sha256. G6: ruff `All checks passed!` over the 18 edited Python files still existing at C3,
every one re-parsed with `ast` without error, and repo-wide `Found 26 errors.` at BOTH the base
— read in a disposable worktree, never by writing to the primary checkout — and the tip, so this
round adds none and sits exactly on the `test_ci_budgets.py` ceiling; `bash -n` exit 0. G7: THE
FULL SUITE WAS RE-RUN BY THE REVIEWER SERIALLY IN THE PRIMARY CHECKOUT at exit code 0 read from
the process object, 19209 passed and 23 skipped, and the arithmetic closes exactly:
`--collect-only` 19613 at the base and 19232 at C3, a fall of 381 = 325 for the eleven deleted
test files plus 32 over the ten swept files plus 24 in `tests/test_grouped_cli.py`, with ZERO
ids gained, and 19209 + 23 = 19232 equal to the collection. G8: `.agent/STOP` absent,
`git status --porcelain` empty, one worktree, branch correct, and `eac1082e..e9944c64` naming
55 paths in an EXACT SET MATCH against the block's enumeration — nothing extra, nothing missing,
and every whole-file removal named in the block.

WHAT THIS ROUND ACHIEVED. The fifth module group is gone and it is the FIRST that is a strongly
connected COMPONENT rather than a single module: `dogfood_run`, `feature_planner`,
`overnight_mission`, `progress_ledger`, `repair_loop_v2` and `self_repair_proposal`, 7952 module
lines, deleted in ONE commit as DECISION F275 D2 and operator RULE 1 require, at 31 insertions
against 14365 deletions over 55 paths. With them went five handler files, 38 catalog entries,
the `dogfood`, `progress` and `self-repair` groups with their `GroupDef`s, eleven test files and
five doc pages. THE SCOPE WAS ESTABLISHED BY APPLYING THE DELETION AND RUNNING THE SUITE, not by
reading the inherited map, and that is what the round is worth: the applied dry run turned 53
real failures into the boundary, and six of its work items appear in no map — the three
operator-facing pages `tests/cli/test_advertised_commands.py` reads for command strings, the
`main_builder_adapter.py` advertisement of a dying command, the `tests/orchestration/test_evidence_index.py`
enumeration that is a dirty-tree artefact rather than a defect, and the 24 parametrised ids in
`tests/test_grouped_cli.py` that no file-level reading of the fall can predict.

THE INHERITED MAP WAS WRONG IN THREE PLACES AND THE APPLIED DRY RUN FOUND ALL THREE. First, the
session-5 map stated that neither of F260's two carry-overs had landed and ordered the next
session to settle their ordering as a dated DECISION; both had landed at rounds 3 and 4, as
`Gate: F275 R4` records, so that DECISION was owed by nobody and this round correctly did not
write it. Second, the map recorded `worker_facade_cmd.py`'s coupling as two string-keyed
`importlib` probes; a third site, a real `from packages.orchestration.dogfood_run import
run_mission_loop` inside `_cmd_mission_run`, carried the dogfood-facade half of
`remedy mission run` and would have been deleted out from under a live production path. Third,
the map named two dying doc pages where five exist. All three are the reviewer's own prose and
are dated `.agent/prose_slips.md` lines rather than ids, per amend0827 rule 2, because none left
anything wrong on disk.

SIX DEVIATIONS WERE DECLARED AND ALL SIX ARE SUSTAINED; FOUR ARE THE REVIEWER'S OWN BLOCK TEXT
AND NONE EARNS AN ID. DEVIATION 1: step (8) ordered `"progress"` removed from `_INTERNAL_GROUPS`
in `tests/cli/test_cli_ux.py`, and the reviewer confirmed by reading the blob at `982d016b` that
the string was never there — the block ordered a removal with no target, the worker declared it
rather than inventing one, and the `+3/-3` the block predicts was reached exactly without it.
DEVIATION 2: G4 predicted 28 remaining sweep lines against a measured 12 distinct; the block's
figure was taken before the round's own docs pass was applied, so it described an intermediate
state of the reviewer's dry run rather than the change set it shipped with, and the gate's real
condition — that no remaining line is anything but a must-not-touch item — held on every one.
DEVIATION 3 IS THE R-0584 CLASS AND THE MOST INSTRUCTIVE: G4 gated `build_mission_morning_report`
to ZERO, and it reads 1, at `tests/cli/test_mission_cmd.py` line 1469, where the line is
`assert "build_mission_morning_report" not in source` — an ABSENCE GUARD that must quote the
symbol in order to forbid it. The gate as worded was unmeetable by any correct round, the guard
is right and worth keeping, and the worker was right to declare rather than delete it; a
zero-gate over a bare symbol must strip quoted spans first, exactly as §3 item 20's R-0586
clause already requires of the record scan. DEVIATION 4: G8 ordered the 55-path SET MATCH over
`982d016b..<C3>`, a range that also spans C0a through C2 and therefore names 60; the reviewer
re-measured both readings and confirms 60 over that range and exactly 55 over
`eac1082e..e9944c64`, with the set match holding — the §3 item 16 / R-0585 shape, a count
resolved against the wrong list, in a gate the same block wrote. DEVIATION 5 records the routes
taken for the base-side readings and is exactly what §3 item 29 asks for; the reviewer confirms
no base reading was taken by overwrite-and-restore. DEVIATION 6 is a tooling bug the worker
caught in its own AST remover before any commit carried it, found by comparing against the
block's numstat — the block's per-file `+/-` column doing the work it was included for.

FOUR AUTHORING SLIPS IN ONE BLOCK IS A SIGNAL AND IS NAMED RATHER THAN DRESSED UP. None is
load-bearing: none reached `.agent/live_review.md`, none changed a path, and every substantive
claim LEDGER10 makes was re-measured true. But operator amendment amend0908-f275-finish rule 5
makes "authoring errors accumulating" an honest reason to end a session only after at least four
delegated rounds, and this session has run one, so the reason is recorded for the next session
to weigh rather than cited here.
