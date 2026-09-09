# Handback — F275 round 11 — the SIXTH module group: the four-module `builder_routing` component

## Session

SESSION 7 of feature F275 · round 11 · rounds so far 11

Against operator amendment amend0908-f275-finish's soft limit of 20 sessions and 60 rounds,
which is F275's own and travels to no other feature. The limit is not reached: 7 of 20 sessions
and 11 of 60 rounds. No scope report is owed.

Context self-assessment (amend0905-throughput): context was comfortable throughout — the round
spent most of its budget on one 23-minute serial suite run rather than on reading, and the worker
ends with ample headroom.

## Range

Review of `cb89bbc3`..`eed65ba1`.

## Commits

### fadfb7c6 F275 R11 C0a: save the round 11 block verbatim to .agent/authored.

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f275-r11.md | 396/0 | the work order copied by `shutil.copyfile`, never retyped |

### f5e95902 F275 R11 C0b: mirror the round 11 block to .agent/last_block.md.

| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 375/423 | the same bytes mirrored; the churn is round 10's block leaving |

### 390f908d F275 R11 C1: advance the plan to round 11.

| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 28/28 | replaced WHOLE by the PLAN11 slice, §3 item 23 |

### 8ec836ca F275 R11 C2: book the round 10 PASS, register R-0847 to R-0849, and record seven prose slips.

| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 10/0 | LEDGER11 appended: the R10 verdict, the R11 Note on R-0831, R-0847/48/49 |
| .agent/prose_slips.md | 14/0 | SLIPS11 appended: seven dated lines |

### 75a1fa1f F275 R11 C3: release DECISION F274 D4's hold on the builder-routing cockpit section as DECISION F275 D5.

| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 49/0 | DECISION11 appended; it lands BEFORE the commit that cuts the section |

### eed65ba1 F275 R11 C4: delete the four-module builder_routing component and its call sites.

ONE commit, 49 paths, 21 insertions against 6393 deletions.

| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/builder_routing.py | 0/1085 | deleted whole — component module 1 |
| packages/orchestration/candidate_quality.py | 0/796 | deleted whole — component module 2 |
| packages/orchestration/local_candidate_generator.py | 0/778 | deleted whole — component module 3 |
| packages/orchestration/model_route_tournament.py | 0/729 | deleted whole — component module 4 |
| apps/cli/commands/builder_routing_cmd.py | 0/113 | deleted whole — handler of a dying group |
| apps/cli/commands/candidate_quality_cmd.py | 0/146 | deleted whole — handler of a dying group |
| apps/cli/commands/local_candidate_cmd.py | 0/87 | deleted whole — handler of a dying group |
| apps/cli/commands/tournament_cmd.py | 0/101 | deleted whole — handler of a dying group |
| tests/orchestration/test_builder_routing.py | 0/318 | deleted whole — test of a deleted module |
| tests/orchestration/test_candidate_quality.py | 0/285 | deleted whole — test of a deleted module |
| tests/orchestration/test_local_candidate_generator.py | 0/300 | deleted whole — test of a deleted module |
| tests/orchestration/test_model_route_tournament.py | 0/253 | deleted whole — test of a deleted module |
| tests/orchestration/test_model_route_tournament_integration.py | 0/43 | deleted whole — its last test class dies with the component |
| tests/cli/test_builder_routing_cli.py | 0/114 | deleted whole — CLI test of a deleted group |
| tests/cli/test_candidate_quality_cli.py | 0/73 | deleted whole — CLI test of a deleted group |
| tests/cli/test_local_candidate_cli.py | 0/115 | deleted whole — CLI test of a deleted group |
| tests/cli/test_tournament_cli.py | 0/98 | deleted whole — CLI test of a deleted group |
| docs/system/expensive-builder-routing-v0.md | 0/122 | deleted whole — page of a deleted module |
| docs/system/local-candidate-generator-v0.md | 0/106 | deleted whole — page of a deleted module |
| docs/system/candidate-quality-evaluation-v1.md | 0/97 | deleted whole — page of a deleted module |
| docs/system/model-route-tournament-harness-v0.md | 0/87 | deleted whole — page of a deleted module |
| docs/guides/model-route-tournament-user-guide-v0.md | 0/65 | deleted whole — guide of a deleted group |
| apps/cli/command_catalog.py | 0/206 | 14 `CommandEntry` blocks, 4 section banners, 4 `GroupDef` rows |
| apps/cli/commands/__init__.py | 1/5 | four handler imports and four names in the `for mod in (…)` tuple |
| apps/cli/commands/external_builder_cmd.py | 0/26 | `_cmd_external_builder_evaluate` and its `COMMAND_HANDLERS` row; the file survives with seven handlers |
| packages/orchestration/ui_server.py | 0/28 | `_build_builder_routing_section` and its dashboard-dict row, released by DECISION F275 D5 |
| packages/orchestration/worker_registry.py | 4/2 | the `LOCAL_CANDIDATE` next-action branch replaced by a deliberate-absence comment; R-0847 |
| pyproject.toml | 0/2 | two mypy module entries |
| docs/README.md | 0/9 | four quick-find rows and five index rows, keyed on the LINK TARGET |
| docs/system/local-model-advisor-v0.md | 0/2 | see-also bullets linking deleted pages |
| docs/system/orchestrator-brain-v0.md | 0/2 | see-also bullets linking deleted pages |
| docs/system/repair-request-builder-v0.md | 0/2 | see-also bullets linking deleted pages |
| docs/system/self-dogfood-execution-v0.md | 0/1 | see-also bullet linking a deleted page |
| docs/system/development-artifact-boundary-v0.md | 0/2 | the `builder_routing.py` and `candidate_quality.py` table rows |
| docs/system/external-builder-sandbox-v0.md | 0/2 | the `candidate-quality evaluate` line and its continuation in the flow block |
| docs/system/external-builder-worker-contract-v0.md | 1/13 | section 5 whole; section 6 renumbered to 5 |
| docs/system/provider-trust-verification-v1.md | 7/10 | the `## Next` section rewritten; states what survives and records the absence |
| docs/system/worker-registry-route-policy-v0.md | 0/6 | the `### Builder Routing integration` section whole |
| .agent/f275_deletion_order.md | 2/3 | REGENERATED from `measured_order()`; eleven components became ten at R10 and become NINE here |
| tests/orchestration/cluster_deletion_map.txt | 0/1 | the one `builder_routing <- ui_server.py` edge |
| tests/orchestration/import_reachability_allowlist.txt | 0/8 | four modules and four handlers |
| tests/orchestration/test_cluster_deletion_map.py | 1/9 | four `CLUSTER_MODULES` rows, four handler paths, the docstring example re-pointed to `worker_registry` |
| tests/orchestration/test_development_artifact_boundary.py | 0/1 | the `builder_routing.py` allowlist string |
| tests/orchestration/test_external_builder_sandbox.py | 0/26 | `class TestQualityIntegration` whole with its banner |
| tests/orchestration/test_token_economy_integration.py | 0/43 | `class TestRoutingIntegration` whole with its banner and two orphan banners |
| tests/orchestration/test_worker_route_integration.py | 3/52 | the module-level import, `class TestRoutingPolicyConstraint`, the unused `worker_registry` import, three orphan banners, the docstring re-scoped |
| tests/cli/test_cli_ux.py | 2/4 | three names out of `_INTERNAL_GROUPS`, `builder-routing` out of `test_no_internal_names` |
| tests/cli/test_external_builder_cli.py | 0/5 | the `evaluate` leg of the submit test and its now-unused `sid` binding |
| tests/ui_server/test_dashboard_cockpit_truth.py | 0/12 | `test_builder_routing_section_present`, the test DECISION F274 D4's hold protected |

### C5 — this handback (self-reference)

| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten whole | a handoff cannot table the commit that writes it (R-0149 pattern); C5's own numbers belong to the next round's ledger entry, per §3 items 14 and 31 |

## External actions

| Command | Outcome |
|---|---|
| `gh pr list --state open --json number,headRefName,baseRefName,isDraft` | `[]` — no open PR; the Open PR Gate passes |
| `git worktree add --detach .remedy-wt/base-r11 cb89bbc3` | created, for the base-side ruff / catalog / collect-only readings only |
| `git worktree remove --force .remedy-wt/base-r11` + `git worktree prune` | removed; `git worktree list` names the primary checkout alone |
| `git push -u origin feature/f275-one-world-completion-part-three` | run ONCE, after this commit |

No PR created, nothing merged: the PR belongs to this feature's closure sequence.

## Verification

Eight gates, every one RUN, every exit code read from the process object
(`subprocess.CompletedProcess.returncode`), never through a pipe and never inferred.

| Gate | Exit | Measured |
|---|---|---|
| G1 TRANSPORT | 0 | source, `.agent/authored/f275-r11.md` at C0a and `.agent/last_block.md` at C0b are all 47959 bytes at sha256 `bce4e44492d94253bf84fbb8d190d827a31f85da50039b39e6e5e8af46f8398c`; all three compare EQUAL |
| G2 THE PLAN | 0 | `.agent/plan.md` at C1 byte-identical to PLAN11: 3029 bytes, sha256 `3e744146ac9c38fc59e323b5184f7e37aa216a392d4c40632743011c298f93ce`, 49 lines against the AGENTS.md cap of 50 |
| G3 THE RECORD | 0 | (a) live_review 569448→586275 growth 16827 = 1+16826; prose_slips 177821→181173 growth 3352 = 1+3351; decisions 958331→962212 growth 3881 = 1+3880; pre a byte-exact PREFIX and slice a byte-exact SUFFIX in all three, joining byte re-read as `b'\n'`. (b) N counted BY THE SCRIPT from each slice as 5, 7 and 7; the last N units equal the slice's units IN ORDER, per-unit sha256 printed for all 19 pairs. (c) one byte flipped IN MEMORY inside the FIRST appended paragraph of each file — BOTH readers REJECTED all three, and the three tracked files re-read from disk are byte-equal to the committed post-blobs. (d) `^Gate: ` 32→33; `^Gate: F275 R10 `, `^Note: F275 R11 `, `^- R-0847 — `, `^- R-0848 — `, `^- R-0849 — `, `^## DECISION F275 D5 ` exactly 1 each. (e) OPEN SET BY DISTINCT ID 75/4/71 before, 78/4/74 after |
| G4 THE DELETION IS COMPLETE | 0 | all 22 deleted paths print False from `git ls-tree -r eed65ba1 --name-only` over 4585 tracked files; the whole-word sweep for the four module names over the 1704 tracked files outside `.agent/` and `.data/` printed IN FULL, nothing truncated — FOUR remaining lines, EVERY one a must-not-touch item under `docs/roadmap/features/` (`T2_F260.md` 340, 341, 365 and `T2_F272.md` 744), zero outside; the four zero-gated symbols read 0, 0, 0, 0 after backtick-quoted spans were deleted from each line |
| G5 THE FOUR MEASUREMENTS | 0 | (a) ratchets `317 passed` at exit 0. (b) through the SHIPPED readers: `len(_BASE_CATALOG)` 296→282, `len(collect_all_handlers())` 296→282, `len(GROUPS)` 56→52 (the 296/296/56 base side measured in the disposable worktree, not restated), duplicate ids 0; all 14 deleted ids ABSENT from both readers and all four groups absent from `GROUPS`, printed one per line; `external-builder.submit`, `external-builder.integrity`, `route-policy.show`, `worker.registry-list`, `token.estimate` PRESENT in both. (c) the order file holds NINE components against ten at the base, the 26-line comment header unchanged, and all nine body lines equal `", ".join(component)` over `measured_order()`; regenerated, never hand-edited. (d) canary `42 passed` at exit 0 |
| G6 RUFF AND BASH | 0 | `All checks passed!` at exit 0 over the 13 `.py` files the range `cb89bbc3..eed65ba1` names that still exist at C4; repo-wide `Found 26 errors.` at BOTH C4 and the base `cb89bbc3` read in the disposable worktree — the `tests/orchestration/test_ci_budgets.py` ceiling holds and this round adds none; `bash -n scripts/remedy_test_fast.sh` exit 0 |
| G7 THE FULL SUITE | 0 | `python3 -B -m pytest tests/ -q` SERIALLY in the PRIMARY CHECKOUT: **19050 passed, 23 skipped, 0 failed** in 1382.89s. The arithmetic closes BY THE ID SET: `--collect-only tests/` 19232 at the base (disposable worktree) and 19073 at C4, a FALL OF 159 with 0 ids GAINED, and 19050 + 23 = 19073. Attributed: 118 over the nine deleted test files, 32 in `tests/test_grouped_cli.py` (the catalog parametrisation no file-level reading predicts), and 9 over the five swept survivors |
| G8 THE TREE | 0 | `.agent/STOP` re-read from disk: absent. `git status --porcelain`: empty. `git worktree list`: the primary checkout ALONE. Branch `feature/f275-one-world-completion-part-three`. `git diff --name-only 75a1fa1f..eed65ba1` an EXACT SET MATCH of the 49 paths — nothing extra, nothing missing. C0a..C4 all single-parent at insertions 396, 375, 28, 24, 49 and 21, every one under the DECISION F104 D1 cap of 500 |

Transcript details, trimmed to command, exit code and decisive lines:

```
G1  python3 g1.py                                            -> 0
    SOURCE / C0a authored / C0b last_block: 47959 bytes each, sha256 bce4e444…8398c
    ALL THREE COMPARE EQUAL: True

G2  python3 g2.py                                            -> 0
    PLAN11 slice  bytes=3029 lines=49 sha256=3e744146…f93ce
    plan.md at C1 bytes=3029 lines=49 sha256=3e744146…f93ce
    BYTE-IDENTICAL: True   LINE COUNT 49 against the cap of 50: UNDER CAP

G3  python3 g3.py                                            -> 0
    growth 16827/3352/3881 == 1+16826/1+3351/1+3880 : True True True
    N counted from each slice = 5, 7, 7 ; all 19 per-unit sha256 pairs equal
    negative control: reader A REJECTS=True reader B REJECTS=True (x3)
    disk re-read == committed post-blob (x3): True
    ^Gate: 32 -> 33 ; the six exact-1 patterns all count=1
    open set 75/4/71 -> 78/4/74

G4  python3 g4.py                                            -> 0
    tracked files at C4: 4585 ; all 22 deleted paths present=False
    corpus 1704 files ; REMAINING LINES: 4, printed IN FULL, none truncated
      docs/roadmap/features/T2_F260.md:340,341,365
      docs/roadmap/features/T2_F272.md:744
    lines outside docs/roadmap/features/ and docs/archive/: 0
    select_builder_routing_decision=0 evaluate_candidate_quality=0
    _build_builder_routing_section=0 BuilderRoutingPolicy=0

G5a python3 -B -m pytest tests/orchestration/test_import_reachability.py
      tests/orchestration/test_cluster_deletion_map.py
      tests/orchestration/test_cluster_deletion_order.py tests/docs/
      tests/cli/test_advertised_commands.py -q                -> 0
    317 passed in 5.56s
G5b python3 g5b.py                                           -> 0
    _BASE_CATALOG 296->282, collect_all_handlers 296->282, GROUPS 56->52, dupes 0
G5c python3 g5c.py                                           -> 0
    base 10 components, C4 9 components, 26-line header UNCHANGED, all 9 rows equal
G5d python3 -B -m pytest tests/cli/test_golden_path.py -q    -> 0
    42 passed in 19.97s

G6a python3 g6a.py                                           -> 0
    13 .py files still existing at C4 -> All checks passed!  (ruff exit 0)
G6b python3 g6b.py                                           -> 0
    C4 (primary checkout)    ruff tail=['Found 26 errors.']
    base cb89bbc3 (worktree) ruff tail=['Found 26 errors.']
    bash -n scripts/remedy_test_fast.sh -> 0

G7  python3 -B -m pytest tests/ -q                           -> 0
    19050 passed, 23 skipped, 1 warning in 1382.89s (0:23:02)
    collect-only: base 19232 (worktree), C4 19073 (primary), fall 159, gained 0
    19050 + 23 = 19073

G8  python3 g8.py                                            -> 0
    STOP absent ; porcelain '' ; 1 worktree ; branch correct
    C3..C4 EXACT SET MATCH of 49 paths (extra [], missing [])
    insertions 396 / 375 / 28 / 24 / 49 / 21, all single-parent, all < 500
```

## Authored-text proofs

Four BEGIN/END slices were extracted from the delegated work order, digested BEFORE use, and
applied byte for byte. The marker lines are the reviewer's own and did not land in any target.

| Slice | Bytes | Lines | sha256 | Applied to |
|---|---|---|---|---|
| PLAN11 | 3029 | 49 | `3e744146ac9c38fc59e323b5184f7e37aa216a392d4c40632743011c298f93ce` | `.agent/plan.md`, replaced WHOLE (C1) |
| LEDGER11 | 16826 | 9 | `c08b7d7abae1bb049094ab8ca8badbeda15ae319e5ec6e59d0f2bde3d1412c8e` | appended to `.agent/live_review.md` (C2) |
| SLIPS11 | 3351 | 13 | `acc662b4fe61859e500be066967b9035d02fb4375f336819ede304ce13785665` | appended to `.agent/prose_slips.md` (C2) |
| DECISION11 | 3880 | 48 | `065ace7fa4308d53338fdeafe0761866c8551cd82615336906a930b3fc622f20` | appended to `.agent/decisions.md` (C3) |

The work order itself: 47959 bytes, sha256
`bce4e44492d94253bf84fbb8d190d827a31f85da50039b39e6e5e8af46f8398c`, authenticated against the
three values the delegation stated BEFORE the first read of its content, and copied to both
`.agent/` targets by `shutil.copyfile`. G1 is the disk-to-disk proof.

## Deviations & assumptions

**1. C4 was AMENDED once, and the amend is the most important thing on this page.** The first C4
was `4a257571`. It FAILED G4: the sweep found a fifth remaining line, and it was the worker's own
prose — the re-scoped module docstring of `tests/orchestration/test_worker_route_integration.py`
read ``more — `builder_routing` and its route-policy consultation were deleted (F275).`` G4's
whole-word sweep, unlike its zero-gate clause, does NOT strip backtick-quoted spans, so a
backticked mention in a deliberate-absence docstring is a real gate failure. The line was rewritten
to `more — that module and its route-policy consultation were deleted by F275.` — same three
insertion lines, so the file's numstat is still 3/52 — and C4 was amended to `eed65ba1`. The block
does not order the docstring's wording, only that it be "re-scoped to what the file still tests",
so this is a correction of the worker's own text and not a change to the ordered change set. AMEND
RATHER THAN A SEVENTH COMMIT, and the reason is stated rather than hidden: constraint 8 orders C4
to be ONE commit carrying all 49 paths, and every gate from G4 to G8 is worded "at C4", so a
follow-up commit would have left a reviewable C4 that fails its own gate and would have moved the
gates off the commit the block names. Nothing was pushed, nothing was force-pushed, and no commit
that ever left this machine was rewritten. The reviewer sees exactly one C4.

**2. `apps/cli/command_catalog.py` measures 0/206 against the block's 0/205 — one line.** The
block's figure came from a mechanical deletion that kept BOTH blank lines bounding the
`builder-routing` / `local-candidate` / `candidate-quality` run, leaving two consecutive blank
lines inside the `_BASE_CATALOG` literal. This round deleted the leading blank of each of the three
runs instead, so the surviving text keeps the file's own one-blank-line-between-sections
convention. Functionally identical; ruff and the suite are unaffected.

**3. `docs/system/worker-registry-route-policy-v0.md` measures 0/6 against the block's 0/5 — one
line, the same class.** Deleting only the `### Builder Routing integration` heading and its four
body lines would have left two consecutive blank lines before `## CLI`; the blank line following
the section went with it.

Deviations 2 and 3 together are the whole of the round's 6393 deletions against the block's 6391.
The insertion count, 21, matches the block exactly, as do all 47 other per-path numstats.

**4. `tests/orchestration/test_token_economy_integration.py` — the 43-line region the block words
as "`class TestRoutingIntegration` whole" also carries two ORPHAN section banners.** The measured
numstat 0/43 is only reachable by taking the "Progress ledger items (Step 1767)" and "Feature
suggestions (Step 1768)" banners with it — both left contentless by earlier rounds, both stranded
between the dying class and the surviving one. Removing the class alone is 33 lines. This is
declared rather than assumed silent because the block's prose named only the class, while its
numstat named the region; the same treatment is ordered EXPLICITLY for the sibling file
`test_worker_route_integration.py`, which is what settles the reading.

**5. G7's numbers are not the block's, and the block predicted that they would not be.** The
reviewer measured 19042 passed / 29 skipped / 2 failed in a disposable worktree. In the primary
checkout the suite is GREEN at exit 0 with 19050 passed / 23 skipped / 0 failed: the two worktree
failures are gone (`apps/ui/node_modules` exists here, and the change IS committed here), and the
eight-pass / six-skip difference is the vitest and evidence-index nodes running rather than
skipping. The block's own G7 wording requires exactly this, so it is reported rather than
reconciled to the worktree figure.

**6. NOT FIXED, because the block does not order it and constraint 3 forbids widening.**
`_job_with_repo` in `tests/orchestration/test_token_economy_integration.py` is now unreferenced —
`TestRoutingIntegration` was its only caller. It is a module-level function, so ruff's selected
rules do not flag it, `Found 26 errors.` holds at both ends, and the suite is green. It is left
on disk and named here rather than deleted on the worker's own authority. No finding is registered
for it: the worker writes none.

**7. Assumption, stated because it decided a numstat.** The block's `docs/README.md · 0/9` says to
key the removal on the LINK TARGET and never on the slug. The nine rows were selected by exact
substring match on the five parenthesised targets; the three surviving `archive/` rows that share
the `expensive-builder-routing-v0` and `model-route-tournament` slugs were asserted still present
after the edit and are.

No other departure from the block's ordered commit sequence: C0a, C0b, C1, C2, C3, C4, C5 landed
in that order, none dropped, none reordered, one amended as declared above.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block to `.agent/authored/f275-r11.md` | done | by `shutil.copyfile`; G1 |
| C0b mirror to `.agent/last_block.md` | done | by `shutil.copyfile`; G1 |
| C1 `.agent/plan.md` replaced WHOLE by PLAN11 | done | G2, 49 lines under the cap of 50 |
| C2 LEDGER11 → `live_review.md`, SLIPS11 → `prose_slips.md` | done | G3 (a)-(e) |
| C3 DECISION11 → `decisions.md` | done | G3; lands BEFORE C4, per constraint 4 |
| C4 the deletion, all 49 paths, ONE commit | deviated | one AMEND after a red G4 on the worker's own docstring; see deviation 1. The commit is one, the paths are 49, the set match is exact |
| C5 `.agent/handoff.md` rewritten whole | done | this file |

## Open findings

**74 open by distinct id**, measured from the committed blob at C3 by DECISION F085 D7's rule
(registrations minus resolutions as a SET DIFFERENCE): 78 registrations, 4 resolutions
(R-0721, R-0725, R-0837, R-0841), 74 open. It was 71 at this round's base `cb89bbc3`; C2's three
registrations R-0847, R-0848 and R-0849 take it to 74. Four are High — R-0803, R-0804, R-0806 and
R-0807 — all F273's rather than this feature's, per DECISION F272 D12.

The worker resolved nothing, registered nothing and wrote no verdict, no `Done:` paragraph and no
finding of its own anywhere.

## Next

Review `cb89bbc3..eed65ba1` and issue the round 11 verdict. If PASS, the next round takes the
`execution_approval_policy` component, which this round's regeneration makes the order file's
FIRST line and which is a SINGLE module, so it is an ordinary group commit. Read `.agent/STOP`
before authoring it (Phase 1 rule 1 before rule 2).
