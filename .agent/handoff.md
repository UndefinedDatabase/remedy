# Handback — F275 One world completion, part three · round 14

## Session

SESSION 8 of feature F275 · round 14 · rounds so far 14

Soft limit is 20 sessions and 60 rounds by operator amendment amend0908-f275-finish
RULE 1, so no scope report is owed.

CONTEXT SELF-ASSESSMENT, as amend0905-throughput requires in one sentence: context is
comfortable — this round read two authority files, one work order and the whole of every
file it edited, ran each of the eight gates once, and re-read nothing it had already
measured, so the session can carry further rounds without a boundary.

## Range

Review of `16494bbd`..`b3ddaa35` for the gated work, plus this handback commit.

## Commits

### 490221e8 F275 R14 C0a: save the round 14 authored block.
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f275-r14.md | +382 / -0 | the delegation source copied with `shutil.copyfile`, never retyped |

### dbffaba9 F275 R14 C0b: mirror the round 14 block to the last-block state file.
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +346 / -196 | the same bytes mirrored with `shutil.copyfile` |

### 11b4dff7 F275 R14 C1: advance the plan to round 14.
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +18 / -18 | replaced WHOLE by the PLAN14 slice, per constraint 5 |

### ed9a78b0 F275 R14 C2: book the round 13 PASS, note R-0847, register R-0853 and R-0854.
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +8 / -0 | LEDGER14 appended as `post = pre + b"\n" + slice` |
| .agent/prose_slips.md | +2 / -0 | SLIPS14 appended the same way |

### b3ddaa35 F275 R14 C3: delete the local model advisor module group and repair the survivors.
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/local_model_advisor.py | +0 / -947 | the module, deleted whole |
| apps/cli/commands/local_advisor_cmd.py | +0 / -101 | its handler file; both handlers drove it |
| tests/orchestration/test_local_model_advisor.py | +0 / -396 | the module's tests |
| tests/cli/test_local_advisor_cli.py | +0 / -96 | the handler's tests |
| docs/system/local-model-advisor-v0.md | +0 / -96 | the page that described the adapter |
| packages/orchestration/orchestrator_brain.py | +0 / -127 | the 125-line span from `_lower_confidence` to the Report banner, the `advisor` dataclass field, the `advisor` export key |
| packages/orchestration/run_contract.py | +0 / -8 | the four-line comment, two `ContractAction` members, two `_DEFAULT_ALLOWED_ACTIONS` lines |
| apps/cli/commands/orchestrator_cmd.py | +1 / -10 | two imports, the `use_advisor` local, the whole branch; the call now reads `persist=True` |
| apps/cli/grouped.py | +0 / -2 | the `--use-local-advisor` parser branch |
| apps/cli/command_catalog.py | +1 / -33 | the `GroupDef`, two `ArgDef`s, the `related` entry, both `CommandEntry` blocks with their section comment and separating blank line |
| apps/cli/commands/__init__.py | +1 / -2 | `local_advisor_cmd` out of the import block and the `for mod in (…)` tuple |
| packages/orchestration/provider_trust_verification.py | +1 / -1 | one docstring line; the safety invariant is unchanged |
| pyproject.toml | +0 / -2 | two packaging entries |
| tests/orchestration/import_reachability_allowlist.txt | +0 / -2 | two allowlist entries |
| tests/orchestration/cluster_deletion_map.txt | +0 / -1 | the map line |
| tests/orchestration/test_cluster_deletion_map.py | +0 / -2 | `CLUSTER_MODULES` and `CLUSTER_COMMAND_HANDLERS` entries |
| .agent/f275_deletion_order.md | +0 / -1 | REGENERATED from `measured_order()`; header kept byte-verbatim |
| docs/README.md | +0 / -2 | the quick-find row and the index row, matched on the LINK TARGET |
| docs/system/orchestrator-brain-v0.md | +5 / -7 | the five-line rewrite and the two-line Future bullet |
| docs/system/provider-trust-verification-v1.md | +2 / -3 | one wording change and the trailing See-link |
| docs/system/self-dogfood-execution-v0.md | +0 / -1 | the See-also bullet |
| docs/system/bounded-overnight-executor-v0.md | +0 / -1 | the See-also bullet |
| docs/archive/expensive-builder-routing-future.md | +2 / -3 | two unlinkings and the See-also bullet; history not rewritten |
| docs/archive/expensive-builder-routing-v0-plan.md | +1 / -1 | one unlinking |

Totals for C3 read from `git show --numstat`: 24 files, +14 / -1845, exactly the
change set the block fixed, path for path and column for column.

### C4 — F275 R14 C4: the round 14 handback.
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | (this file) | rewritten WHOLE at C4; a handoff cannot table the commit that writes it, and its sha is unmeasurable from inside itself |

## External actions

- `git worktree add --detach .remedy-wt/wt-base 16494bbd` — created for the base-side
  readings of G5 and G7(b). Removed with `git worktree remove --force`, then `git worktree prune`.
- `git worktree add --detach .remedy-wt/wt-c3 b3ddaa35` — created for the four G6 red-proofs.
  Removed with `git worktree remove --force`, then `git worktree prune`.
- `git worktree list` after cleanup names the primary checkout ALONE.
- `git push -u origin feature/f275-one-world-completion-part-three` — ONCE, after C4.
- No PR created, none edited, none merged. No `gh` command run.

## Verification

Every exit code below was read from the `CompletedProcess` object returned by
`subprocess.run`, never from a pipe and never inferred.

- **G1 TRANSPORT — exit 0.** Delegation source `.remedy-wt/f275-r14.md`, the C0a blob
  `.agent/authored/f275-r14.md` and the C0b blob `.agent/last_block.md` are all
  37397 bytes at
  `e8108d5345442dbf948921396afaf07dba35045ab51941fb0c318158e56b073d`; all three
  byte-identical. This chain covers those three artefacts and claims nothing about the
  bytes the reviewer emitted.
- **G2 THE PLAN AND THE BLOCK — exit 0.** `.agent/plan.md` at C1 is 2720 bytes at
  `cc13dc6513d6a3967147857d87dd10cf5262679ce1b805019fca074248babf15`, byte-identical to
  the PLAN14 slice; 45 lines against the AGENTS.md cap of 50; `## Goal` present, `## Next
  Steps` present. Re-measured from the C0a blob: TOTAL 382 lines, slice body lines 53,
  PROSE 329 — both within constraint 9's 490 and 400.
- **G3 THE RECORD — exit 0, all five parts.**
  (a) `.agent/live_review.md` 608189 → 618783, growth 10594 == 1 + 10593; `.agent/prose_slips.md`
  183299 → 184231, growth 932 == 1 + 931; prefix exact and suffix exact for both; the
  joining byte re-read out of each post-blob is `b'\n'`.
  (b) N counted by the script from each slice: 4 and 1. The last 4 and last 1 blank-line
  units of the whole file equal the slice's paragraphs IN ORDER, unit by unit.
  (c) One byte flipped IN MEMORY inside the FIRST appended paragraph of each file
  (offsets 608195 and 183305). Reader A (byte arithmetic) and reader B (ordered units)
  both ACCEPT the truth and both REJECT the mutant. Both files re-read from disk are
  byte-equal to their committed post-blobs.
  (d) `^Gate: ` 35 → 36. `^Gate: F275 R13 `, `^Note: F275 R14 `, `^- R-0853 — ` and
  `^- R-0854 — ` are each exactly 1 in the post-blob.
  (e) THE OPEN SET BY DISTINCT ID, `Landed:` never subtracted: before 81 registered /
  4 done / 77 OPEN; after 83 / 4 / 79.
- **G4 THE DELETION IS COMPLETE — exit 0.** `git ls-tree -r b3ddaa35` holds 4574 paths;
  all five deleted paths ABSENT. Sweep corpus 1690 tracked files outside `.agent/` and
  `.data/`, with the four surviving tokens neutralised per line before matching. RAW
  result, printed in full, 4 lines:
  `docs/roadmap/features/T2_F260.md:338`, `docs/roadmap/features/T2_F260.md:339`,
  `docs/system/core-product-spine-v0.md:129`, `docs/system/vocabulary.md:155`.
  After deleting every backtick-quoted span, the STRIPPED count — the binding gate — is
  EXACTLY 1: `docs/system/vocabulary.md:155`, which the round's scope ruling leaves to
  the open finding R-0843.
- **G5 THE SHIPPED READERS AND THE ORDER FILE — exit 0 at both ends.** Read BY IMPORT,
  never by grep, with `sys.path` pinned and the resolved `__file__` printed first: at the
  base it resolved under `.remedy-wt/wt-base/`, at C3 under the primary checkout, so no
  editable install shadowed either reading. `_BASE_CATALOG` 269 → 267,
  `collect_all_handlers()` 269 → 267, `GROUPS` 50 → 49, `ALL_KNOWN_ACTIONS` 122 → 120,
  duplicate ids 0 at both ends. `local-advisor.status` and `local-advisor.run` ABSENT from
  both readers at C3; `local-advisor` gone from `GROUPS`. `orchestrator.decide`,
  `orchestrator.inspect`, `orchestrator.report`, `provider.verify`, `patch.approve` and
  `do.continue` PRESENT in both readers at C3. `orchestrator.decide` args fall from
  `['--job-id', '--use-local-advisor', '--new', '--json']` to `['--job-id', '--json']`.
  The exported decision key set falls 20 → 19 with `advisor` gone. The regenerated order
  file holds SIX components against seven, its 26-line header sha256 is
  `aff913e6eedb4d9c7e5ab6e76578be881ffffa3612018cf58b5a48ad508b0cc2` at both ends, and the
  file is EQUAL to a fresh regeneration from the live import graph; its first component is
  `packages.orchestration.managed_builder_execution`.
- **G6 THE RED-PROOFS — all four run inside the disposable worktree at C3, `__pycache__`
  purged before every run, `python3 -B`, control FIRST.** Each target was restored with
  `git checkout --` and the restore proved by sha256; the worktree porcelain was empty at
  the end.
  - Probe A, `import_reachability_allowlist.txt`: control exit 0 at 3 passed, MUTATED
    **exit 1** at 1 failed / 2 passed. Target sha256 before and after identical.
  - Probe B, `test_cluster_deletion_map.py` `CLUSTER_MODULES`: control exit 0 at 6 passed,
    MUTATED **exit 1** at 2 failed / 4 passed. Target sha256 before and after identical.
  - Probe C, the orphan `"local-advisor": GroupDef(...)` with no command and no handler:
    control exit 0 at 499 passed, MUTATED **exit 0** at 507 passed. Target sha256 before
    and after identical.
  - Probe D, `"advisor": None,` back into `export_decision_json`: control exit 0 at
    61 passed, MUTATED **exit 0** at 61 passed. Target sha256 before and after identical.
- **G7 RUFF, THE RATCHETS AND THE FULL SUITE.**
  (a) `python3 -m ruff check` over the eight edited `.py` files that still exist at C3 —
  `All checks passed!`, **exit 0**.
  (b) `python3 -m ruff check .` repo-wide: `Found 26 errors.` at C3 in the primary
  checkout, **exit 1**; `Found 26 errors.` at the base `16494bbd` inside the disposable
  worktree, **exit 1**. The two diagnostic SETS were compared item by item and are
  identical — 26 diagnostics each, nothing only at one end. The gate is the equality, and
  exit 1 is ruff reporting the pre-existing 26 at both ends.
  (c) `python3 -B -m pytest` over `test_import_reachability.py`, `test_cluster_deletion_map.py`,
  `test_cluster_deletion_order.py`, `tests/docs/`, `test_advertised_commands.py`,
  `test_cli_ux.py` and `test_product_spine.py` — **442 passed, exit 0**.
  (d) canary `python3 -B -m pytest tests/cli/test_golden_path.py -q` — **42 passed, exit 0**.
  (e) THE FULL SUITE, `python3 -B -m pytest tests/ -q`, SERIALLY, in the PRIMARY checkout,
  with the change COMMITTED: **18844 passed, 23 skipped, ZERO failed, 1 warning, exit 0**,
  in 1376.65s. Both binding conditions hold: zero failed, and 18844 + 23 = 18867, which
  equals the C3 collection exactly.
  (f) THE ARITHMETIC, BY THE ID SET, both sides collected in the PRIMARY checkout — the
  same environment as each other: base 18919 node ids, C3 18867, a FALL of **52** with
  **ZERO gained**. Attribution of the 52 lost ids by file:
  `tests/orchestration/test_local_model_advisor.py` 38, `tests/test_grouped_cli.py` 8 (it
  parametrises over the catalog and is in no change set), `tests/cli/test_local_advisor_cli.py` 6.
- **G8 THE TREE — exit 0.** `.agent/STOP` re-read from disk: ABSENT. `git status
  --porcelain`: empty. `git worktree list`: ONE entry, the primary checkout. Branch
  `feature/f275-one-world-completion-part-three`. `git diff --name-only ed9a78b0..b3ddaa35`
  yields 24 paths; compared as a SET against the block's 24, the missing set is EMPTY, the
  extra set is EMPTY, and the match is EXACT. Per commit, parent count and insertions
  against the DECISION F104 D1 cap of 500: C0a 1 parent / +382, C0b 1 / +346, C1 1 / +18,
  C2 1 / +10, C3 1 / +14. Every one under the cap; no oversize commit to declare. C4's own
  numbers belong to the next round's ledger entry.

## Authored-text proofs

Three reviewer-authored slices were applied this round, each taken as the bytes STRICTLY
BETWEEN its `--- BEGIN-<NAME> ---` and `--- END-<NAME> ---` marker lines, the markers never
reaching a target file.

| Slice | Bytes | sha256 | Target | Result |
|---|---|---|---|---|
| PLAN14 | 2720 | `cc13dc6513d6a3967147857d87dd10cf5262679ce1b805019fca074248babf15` | `.agent/plan.md` at C1 | committed blob byte-identical to the slice |
| LEDGER14 | 10593 | `c6b866f90f459f8dace72e908da1822e11cab85e5da20fc4a95774e42158ffaa` | `.agent/live_review.md` at C2 | suffix exact, growth 1 + 10593, 4 paragraphs equal in order |
| SLIPS14 | 931 | `4c6b432e0a25babe3966b944cacf421ee85ef8e805534c4b4b14f9dcc735baaf` | `.agent/prose_slips.md` at C2 | suffix exact, growth 1 + 931, 1 paragraph equal in order |

All three slices were extracted from the COMMITTED C0a blob, not from the scratch copy.
The five-line replacement text of doc pair (8) was likewise cut out of the committed C0a
blob by line index rather than retyped, and its bytes are
`b859594c3060dfeffae749702cf3b0dfaf24e345900199bbc1e51a7207137ba4` at 388 bytes.

## Deviations & assumptions

1. **G6 probe C, the UNMUTATED control pass count differs from the ledger's figure.** The
   block's LEDGER14 paragraph records the probe C control as "exit 0 at 470 passed in the
   same worktree". This round measured the control at **exit 0 at 499 passed**. The
   MUTATED reading agrees exactly with the block — exit 0 at 507 passed — and so does the
   colour the gate turns on, so the finding the paragraph books is unaffected; only the
   baseline numeral differs. Reported rather than repaired, per the block's instruction to
   report the measurement even when it differs from the number the block predicts. The
   arithmetic is consistent on this side: the orphan `GroupDef` adds 8 parametrised cases
   to `tests/test_grouped_cli.py`, and 499 + 8 = 507.
2. **G7(b), a first base-side ruff reading of 34 was my own contamination and is
   withdrawn.** The first `ruff check .` run in the base worktree read `Found 34 errors.`
   The extra 8 diagnostics were traced, by comparing the two diagnostic sets item by item,
   to two probe scripts I had copied into the worktree root (`_g5probe.py`, `_g5full.py`);
   nothing in the repository accounted for any of them. The scripts were deleted, the
   worktree porcelain confirmed empty, and the run repeated: `Found 26 errors.` Both ends
   now read 26 with identical diagnostic sets. The 34 is recorded here so the retracted
   number is not silently dropped.
3. **The base-side ruff and collection figures were also taken in the primary checkout
   while HEAD still stood at the base.** Before any commit of this round, with the tree
   clean and nothing written, `ruff check .` read `Found 26 errors.` and `pytest
   --collect-only` read 18919 in the primary checkout at `16494bbd`. Those readings agree
   with the disposable-worktree ruff reading and are what G7(f)'s "same environment as each
   other" condition rests on, since the C3 collection was taken in the same primary
   checkout. No destructive verification touched the primary checkout at any point.
4. **The ordered anchors leave three artefacts standing in the survivors, by construction
   rather than by oversight.** Applied as written, and each confirmed by the block's own
   `+/-` column: (i) `orchestrator_brain.py` keeps the `# Local Model Advisor integration
   (Steps 1509-1511)` banner comment and the `_CONFIDENCE_ORDER` constant, because the
   ordered span begins at `def _lower_confidence` and `_CONFIDENCE_ORDER` now has no
   reader; (ii) `orchestrator_cmd.py` keeps `adv = data.get("advisor")` and its `if adv:`
   print, which the ordered `1 / 10` numstat pins in place and which can no longer fire now
   that the exported decision carries no `advisor` key; (iii) `test_cluster_deletion_map.py`
   keeps its "twenty-four modules" comment above a shrunk `CLUSTER_MODULES`. Nothing was
   added to or removed from the ordered change set to address any of the three.
5. **The two enum members survive as the block ruled.** `RoutingTier.LOCAL_ADVISOR_PREFERRED`
   is the fallthrough return of the surviving `_model_routing_plan`;
   `OptionKind.LOCAL_ADVISOR_NEEDED` and its `_BASE_SCORE` weight were verified at the base
   to have no constructor anywhere. Both left alone, and both are among the four tokens G4
   neutralises before matching.
6. **`docs/system/core-product-spine-v0.md` line 129 and `docs/system/vocabulary.md` line
   155 were NOT touched**, per the round's one scope ruling: both are instances of the open
   finding R-0843, whose fix clause routes the whole `docs/system/` group-name sweep into the
   round that drafts DECISION F260 D3.
7. **No departure from the block's ordered commit sequence.** C0a, C0b, C1, C2, C3, C4 in
   that order, six commits, each single-parent, no extra commit, none dropped, none reordered.
8. No verdict, no `Done:` paragraph, no `Landed:` line and no finding of the worker's own is
   written anywhere in this round. The only finding text that landed is the reviewer's
   LEDGER14 slice, applied byte for byte.

## Item status

| Item | Status | Reason |
|--------|----------|------------------------------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | 24 paths, one commit, +14 / -1845 |
| C4 | done | this file |
| G1 | done | exit 0 |
| G2 | done | exit 0 |
| G3 | done | exit 0, all five parts |
| G4 | done | exit 0, RAW 4 / STRIPPED 1 |
| G5 | done | exit 0 at both ends |
| G6 | done | A exit 1, B exit 1, C exit 0, D exit 0, against four controls at exit 0 |
| G7 | done | (a) 0, (b) 1 and 1 at an equal 26, (c) 0, (d) 0, (e) 0, (f) 0 |
| G8 | done | exit 0, EXACT SET MATCH on 24 paths |

## Open findings

79 OPEN by distinct id at C2 — 83 registered minus 4 with a `Done:` line, `Landed:` lines
never subtracted. Four are High: R-0803, R-0804, R-0806 and R-0807, all F273's rather than
this feature's, per DECISION F272 D12. R-0847 stays open and now carries a second measured
face as a Note. R-0853 and R-0854 are the two ids this round registered.

## Next

The planner and reviewer of session 8 re-run the eight gates against the committed blobs
over `16494bbd`..HEAD — the gated work ends at C3 `b3ddaa35` and the handback commit
follows it — and issue the round 14 verdict. The next production round
deletes the `managed_builder_execution` component, which this round's regeneration makes
the order file's first line and which is a SINGLE module.
