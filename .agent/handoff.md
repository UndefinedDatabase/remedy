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

## Reviewer verdict on round 14 — appended after the handback, by the reviewer's authored text

VERDICT ROUND 14: **PASS.** Written by the planner and reviewer of SESSION 8 AFTER reading the
committed range `16494bbd`..`5fb38765` and RE-RUNNING every one of the eight gates independently
against the committed blobs; the worker's report was not taken as evidence for any line below. It
is carried here because under `docs/agents/self_drive_protocol.md` a verdict that stays in the
session is lost, and it is booked into `.agent/live_review.md` by the FIRST substantive commit of
round 15, per amend0827-process-diet rule 1. It is NOT a `Done:` paragraph and resolves no finding.

WHAT THE REVIEWER RE-MEASURED. Six single-parent commits C0a `490221e8`, C0b `dbffaba9`, C1
`11b4dff7`, C2 `ed9a78b0`, C3 `b3ddaa35` and C4 `5fb38765`, each parent read from `git log`, with
per-commit insertions 382, 346, 18, 10, 14 and 233, every one under the AGENTS.md DECISION F104 D1
cap of 500. G1 IS THE PRIMARY PROOF OF §4 ITEM 9 AND NOT THE DIGEST FALLBACK: the reviewer's own
scratchpad original and both committed copies are 37397 bytes at
`e8108d5345442dbf948921396afaf07dba35045ab51941fb0c318158e56b073d` and compare BYTE-EQUAL; per §3
item 37 that chain covers those three artefacts and claims nothing about the emitted bytes. G2:
`.agent/plan.md` byte-identical to PLAN14 at 2720 bytes, 45 lines against the cap of 50, both
mandated headings present; the block re-measured from the C0a blob at 382 lines TOTAL and 329
PROSE, inside both caps. G3: `.agent/live_review.md` 608189 to 618783, growth 10594 = 1 + 10593;
`.agent/prose_slips.md` 183299 to 184231, growth 932 = 1 + 931; for both the prefix and suffix are
byte-exact and the joining byte was read back as a newline; N was COUNTED from each slice by the
reviewer's own reader as 4 and 1, with ordered equality holding over the WHOLE appended region and
a per-unit sha256 printed on both sides; and BOTH negative controls, flipped in memory inside the
FIRST appended paragraph per §3 item 36, were REJECTED by both readers, with both tracked files
re-read from disk afterwards and byte-equal to their committed post-blobs. `^Gate: ` 35 to 36, and
`^Gate: F275 R13 `, `^Note: F275 R14 `, `^- R-0853 — ` and `^- R-0854 — ` exactly 1 each; THE OPEN
SET 77 TO 79 BY DISTINCT ID against registrations 81 to 83 and resolutions 4 to 4. G4: all five
whole-file removals absent from `git ls-tree` at C3 over 4574 tracked files, and the sweep over the
1690 tracked files outside `.agent/` and `.data/`, printed IN FULL with the four SURVIVING advisor
tokens neutralised first, read exactly FOUR lines RAW and ONE with backtick-quoted spans stripped,
which is the binding count and is the single `docs/system/vocabulary.md` line the block's scope
ruling leaves to R-0843. G5: through the SHIPPED readers, by import with the resolved `__file__`
printed, `_BASE_CATALOG` and `collect_all_handlers()` both fell 269 to 267, `GROUPS` 50 to 49 and
`ALL_KNOWN_ACTIONS` 122 to 120, with zero duplicate ids, both deleted ids ABSENT from both readers,
`local-advisor` gone from `GROUPS`, and `orchestrator.decide`, `orchestrator.inspect`,
`orchestrator.report`, `provider.verify`, `patch.approve` and `do.continue` all PRESENT — the human
approval path is untouched; `orchestrator.decide` args fell to `('--job-id', '--json')`; the
exported decision key set fell from 20 keys to 19 with `advisor` gone; and the regenerated order
file holds SIX components against seven with its 26-line header sha256 unchanged at `aff913e6…`.
G6: ALL FOUR RED-PROOFS WERE RE-RUN BY THE REVIEWER IN ITS OWN DISPOSABLE WORKTREE, each with its
OWN matched control over its OWN selection — probe A control exit 0 at 3 passed against mutated
exit 1; probe B control exit 0 at 6 passed against mutated exit 1 at 2 failed; probe C control exit
0 at 499 passed against mutated exit 0 at 507 passed; probe D control exit 0 at 61 passed against
mutated exit 0 at 61 passed — every file restored byte-identically and proved by sha256. G7: ruff
`All checks passed!` over the eight edited Python files still existing at C3 and repo-wide `Found
26 errors.` at both ends; the ratchets and canary 484 passed at exit 0; and THE FULL SUITE WAS
RE-RUN BY THE REVIEWER SERIALLY IN THE PRIMARY CHECKOUT and was GREEN at 18844 passed, 23 skipped
and ZERO failed — the worker's figure exactly — with 18844 + 23 = 18867 equal to the C3 collection
against 18919 at the base, a fall of 52 with zero gained. G8: `.agent/STOP` absent, porcelain
empty, ONE worktree, branch correct, and `ed9a78b0..b3ddaa35` naming the 24 paths in an EXACT SET
MATCH, nothing extra and nothing missing.

WHAT ROUND 14 ACHIEVED. The NINTH module group, `local_model_advisor` at 947 module lines, in ONE
commit at 14 insertions against 1845 deletions over 24 paths, taking its 101-line handler file
whole, two commands, the `local-advisor` group, two test files, one doc page and two
`ContractAction` members with it, and repairing seven surviving documentation pages whose links the
deletion would otherwise have broken. Unlike rounds 11 to 13 this was a PRODUCTION round: three
survivors lost code and one of the losses changed an exported JSON contract.

THE WORKER'S SIX DECLARED DEVIATIONS ARE ALL SUSTAINED, and two of them are the reviewer's own.
FIRST AND LOAD-BEARING, the worker is RIGHT about probe C's control. The reviewer's LEDGER14 text
records the unmutated control at "470 passed" beside a mutated 507; 470 was a reading taken over a
SIX-file selection while probe C runs over THREE, and the correctly matched control is 499, which
the reviewer re-measured independently at 499 against 507. The finding's conclusion is untouched,
because it rests on the mutated reading alone — an orphan `GroupDef` passes at exit 0 either way —
so this is a non-load-bearing prose inaccuracy that put nothing wrong on disk, and under
amend0827-process-diet rule 2 it is a dated `.agent/prose_slips.md` line rather than an id and
earns no correction round. SECOND, the worker's withdrawn base-ruff reading of 34 was its own
scratch files being linted, and it deleted them, re-read 26 at both ends and recorded the
retraction rather than dropping it silently; that is the record working as intended. THIRD, its
base ruff and base collection were taken in the primary checkout while the branch still stood at
the base, before any commit, with a clean tree and nothing written — read-only, so guardrail G5 is
untouched, and the reviewer's own base readings were taken in a worktree and agree.

WHAT THE ROUND LEFT ON DISK, WHICH IS THE REVIEWER'S AUTHORING MISS AND NOT THE WORKER'S. The
worker's deviation 4 names three artefacts the block's anchors did not reach, and the reviewer
re-measured all three at `5fb38765` and confirms every one. They are registered as R-0855 below.
The worker was RIGHT to declare rather than widen: constraint 3 bound its change set and AGENTS.md
Scope Control forbids an unordered edit, so declaring is the sanctioned move and the same one round
12's worker was credited for.

## Finding drafted by session 8, to be booked by round 15's FIRST substantive commit

- R-0855 — Medium, ROUND 14's DELETION LEFT DEAD SURVIVOR STATE ITS ANCHORS DID NOT REACH, IN TWO FILES, AND ONE OF THE TWO IS A CODE PATH THAT READS A JSON KEY THE SAME ROUND REMOVED. Raised by the reviewer of session 8 at the round 14 gate, from the worker's declared deviation 4, and re-measured independently at `5fb38765` before this text was written. It is ONE id rather than two because the defect, the cause and the fix are one: an ordered anchor deleted a definition without sweeping the neighbourhood the definition served, and one sweep repairs both — which is exactly the counter-measure the resolved R-0841 and the open R-0843 already state and which this block failed to apply to its own orders. FIRST INSTANCE, `apps/cli/commands/orchestrator_cmd.py`, in `_cmd_orchestrator_decide`: the three lines `adv = data.get("advisor")`, `if adv:` and the print beneath them SURVIVE, while the same round removed `"advisor"` from `export_decision_json`, so `data.get("advisor")` is now always `None` and the branch can never fire. That is the attic AGENTS.md Scope Control forbids by name, and it is worse than ordinary dead code because a reader takes it as evidence that the exported key still exists. SECOND INSTANCE, `packages/orchestration/orchestrator_brain.py` lines 922 to 931: the ten-line section banner `# Local Model Advisor integration (Steps 1509-1511) — advisory ONLY.` and its explanatory paragraph describe an integration this round deleted, and the constant `_CONFIDENCE_ORDER` beneath it now has EXACTLY ONE occurrence repo-wide — its own definition — because its only reader was `_lower_confidence`, which the same commit removed. A THIRD INSTANCE WAS FOUND BY THE SAME SWEEP AND PREDATES THIS ROUND: `tests/orchestration/test_cluster_deletion_map.py` line 41 reads `# The twenty-four modules F260's Design lists as the prototype cluster.` above a `CLUSTER_MODULES` tuple that holds SEVEN, having shrunk once per group commit since round 7. It is named here rather than given an id of its own because the same sweep fixes it. WHY THIS IS AN ID AND NOT A PROSE SLIP: all three are wrong state on disk under `apps/`, `packages/` and `tests/`, which is precisely what amend0827-process-diet rule 2 reserves an R-id for, and the first instance is a live code path rather than a comment. NO GATE COULD SEE ANY OF THEM — ruff reports no error, the full suite is green at 18844 passed, and the round 14 sweep could not fire because none of the three names a deleted symbol. WHAT WOULD RESOLVE IT: one commit deleting the three lines in `orchestrator_cmd.py`, the banner and `_CONFIDENCE_ORDER` in `orchestrator_brain.py`, and correcting the `CLUSTER_MODULES` comment to state no numeral at all per §3 item 16. FIX CLAUSE, BINDING ON EVERY REMAINING DELETION ROUND OF THIS FEATURE: a block that orders a definition deleted also orders the reader to sweep, in the same commit, for the callers of that definition, for the constants left with no reader, and for the section comment above it — and the block says so in its own text rather than leaving the worker to choose between an unordered edit and a declared deviation.

## Prose slip drafted by session 8, to be appended by round 15's ledger commit

2026-09-09 · F275 R14 · The reviewer's LEDGER14 slice recorded probe C's unmutated control as "470 passed" beside a mutated reading of 507; 470 was measured over a SIX-file selection while probe C runs over THREE, so the two numbers in that sentence come from different selections and are not comparable as written. The worker measured the matched control at 499 and declared the difference, and the reviewer re-measured 499 against 507 independently. Nothing is wrong on disk and the finding's conclusion is untouched, because it rests on the mutated reading alone: at exit 0 either way, an orphan `GroupDef` is invisible to every catalog guard. The lesson is that a control belongs to a SELECTION, not to a worktree, and a probe's control must be run over the probe's own selection in the same script that runs the probe.

## THE ROUND 15 MAP — MEASURED AT `5fb38765` BY AN APPLIED, INCOMPLETE DRY RUN

Everything below was measured by the reviewer of session 8 against the tree at the commit named
above. Unlike the session 7 map this is an APPLIED dry run, not a consumer map read from source —
which is why it is trustworthy about scope and why it can say what it does NOT yet cover. THE DRY
RUN IS INCOMPLETE AND WAS LEFT INCOMPLETE DELIBERATELY: the mechanical half was applied and the
suite was run to establish the boundary by execution, and twelve tests are RED, each needing a
judgement the next session should make rather than inherit.

THE MODULE: `packages/orchestration/managed_builder_execution.py`, 1694 lines, component line 1 of
`.agent/f275_deletion_order.md`, a SINGLE module.

DIES WITH IT, and all six were applied cleanly: `apps/cli/commands/managed_builder_execution_cmd.py`
(350 lines, SEVENTEEN handlers), `tests/orchestration/test_managed_builder_execution.py` (1793),
`tests/cli/test_managed_builder_execution_cli.py` (95),
`docs/system/managed-external-builder-execution-v1.md` and
`docs/system/managed-external-builder-execution-v1-1-hardening.md`.

THE CATALOG: the `execution` `GroupDef` at line 151 and a 195-line block holding exactly SEVENTEEN
`CommandEntry` ids, counted from the block by the applier rather than by hand —
`execution.template-list`, `template-show`, `template-create`, `template-enable`,
`template-disable`, `template-update`, `approve`, `run`, `show`, `list`, `debug-bundle`,
`integrity`, `approval-show`, `approval-validate`, `approval-list`, `operator-runbook` and
`claude-doctor`.

THE RUN-PERMISSION VOCABULARY: FOURTEEN `ContractAction` members in
`packages/orchestration/run_contract.py` and their fourteen rows in `_DEFAULT_ALLOWED_ACTIONS`, 28
lines in total, all of them `EXECUTION_*` and all of them reachable only through the dying handler.

A DATED DECISION IS OWED BEFORE THE FIRST `git rm`, and this is the round's real planning work.
`remedy execution approve` is a HUMAN approval command — `remedy worker add` prints it as step 4 of
its own quickstart and states "Execution still requires explicit approval per session" — while
F275's Do-not-touch section protects "the approval gate". DECISION F275 D6 does NOT settle this: it
ruled about `execution_approval_policy.py` and named F017's `patch approve` / `do continue` /
`approval_required` path as the protected gate. The next session must rule, as a dated DECISION in
`.agent/decisions.md`, whether deleting a gate TOGETHER WITH
the thing it gates leaves any ungated path — the reviewer's reading is that it does not, because
managed builder execution itself dies in the same commit, but that reading is a recommendation and
not yet a ruling.

THE SURVIVORS THAT LOSE CODE. `apps/cli/commands/worker_facade_cmd.py` keeps `mission.run` and
`doctor.core` and loses the TEMPLATE half of three user-facing commands — `worker doctor` loses its
`template_exists` and `template_enabled` checks, `worker add` its `template_enabled` result and the
two quickstart lines naming `execution approve` and `execution template-show`, and `worker disable`
its `template_disabled` result. Each of those three PAIRS a template with an ADAPTER from
`packages/orchestration/main_builder_adapter`, which is component line 1 of the REGENERATED order
file and therefore dies in a LATER round, so this round leaves each command holding its adapter
half alone and the next-but-one round takes the rest. `packages/orchestration/exec_guard.py`
SURVIVES comfortably — six modules import it, among them `integrity_gate`, `ci_run`,
`pingpong_loop`, `pingpong_promote` and `runtime_supervisor` — and loses only SEVEN docstring
citations of `managed_builder_execution` at lines 91, 550, 606, 642, 722, 812 and 889, which are
prose and must be swept rather than left dangling.

THE ORDER FILE REORDERS RATHER THAN SHRINKING PURELY, which round 13's did not: regeneration gives
SIX components falling to FIVE, and `main_builder_adapter` moves from position four to position
one while `overnight_readiness` moves too, because deleting this module changes the import graph's
topological order. The 26-line header sha256 is unchanged at `aff913e6…`. A block that predicts a
`0 1` numstat for this file will be wrong.

TWELVE TESTS ARE RED AFTER THE MECHANICAL HALF, IN FOUR FILES THAT NO CONSUMER MAP PREDICTED, and
this list is the round's real remaining work:
  - `tests/cli/test_worker_facade_cmd.py` — SEVEN: `TestWorkerDoctor` `test_doctor_all_ready`,
    `test_doctor_binary_missing`, `test_doctor_adapter_disabled`, `test_doctor_text_output`;
    `TestWorkerAdd` `test_add_enables_both`, `test_add_already_enabled`; `TestWorkerDisable`
    `test_disable_both`. All seven patch `packages.orchestration.managed_builder_execution`
    symbols by dotted path at lines 126, 128 and 129, and their assertions describe the paired
    adapter-and-template behaviour this round halves. Each needs a judgement about what the
    surviving command asserts, not a mechanical edit.
  - `tests/orchestration/test_development_artifact_boundary.py` — TWO:
    `TestProductModulesNoLiveReview::test_managed_builder_execution`, which imports the module, and
    `TestFunctionalNoAgent::test_worker_doctor_core_no_agent`. The module also appears in the list
    at line 15 and at line 167.
  - `tests/cli/test_cli_ux.py` — TWO: `TestHiddenCallable::test_hidden_group_callable` and
    `TestGroupDefIntegrity::test_internal_groups_marked`. Both hold `"execution"` in a hardcoded
    group-id list, at lines 17 and 124.
  - `tests/docs/test_docs_consistency.py::TestPrimaryDocLinksResolve` for `docs/README.md`, which
    still links both deleted doc pages. Note that this gate DID fire here and did NOT fire in round
    14, because a README row links these pages and no README row linked round 14's.
Also mechanical and already applied: `pyproject.toml` (1 line),
`tests/orchestration/import_reachability_allowlist.txt` (2),
`tests/orchestration/cluster_deletion_map.txt` (1), `tests/orchestration/test_cluster_deletion_map.py`
(2), `tests/test_test_categories.py` (1), `scripts/remedy_test_fast.sh` (1) and
`docs/system/test-lanes-v0.md` (1).

AT LEAST ONE FINDING IS OWED under operator RULE 3: the `execution` group and its seventeen
commands, which is the whole managed-external-builder execution surface — templates, approval,
execution, integrity, the debug bundle, the operator runbook and the Claude doctor. Whether the
loss of the three `worker` commands' template half is a second id or belongs to the same one is a
judgement for the round that ships it, and §3 item 30 requires the open set to be searched for the
defect before either is minted.

## Session 8 ends here — ONE delegated round, reviewed and PASSED, BELOW the four-round floor

This is stated plainly rather than dressed up. `docs/agents/self_drive_protocol.md` G7, as amended
by amend0905-throughput, sets a target of six to eight delegated rounds per session with FOUR as
the floor, and this session ran ONE. The honest reason is the one amend0905 names — a round that
explicitly needs a fresh session — and it is offered as a MEASUREMENT rather than a preference:
round 15 was mapped by an APPLIED dry run, not by reading source, and that dry run establishes
that the round needs a dated DECISION on whether `remedy execution approve` is the approval gate
F275's Do-not-touch protects, that it removes seventeen commands and fourteen run-permission
actions, and that it leaves twelve tests red across four files no consumer map predicted, seven of
them requiring the assertions of three surviving user-facing commands to be rewritten rather than
deleted. Beginning that round on the remainder of this session would have meant authoring its block
against an incomplete dry run, which is the one thing this feature's record shows costs a round.

WHAT THIS SESSION LANDED. Round 14 alone: the ninth module group, applied by the reviewer in a
disposable worktree and run to a full green suite BEFORE its block was authored, then delegated,
then independently re-gated against the committed blobs with all four red-proofs re-run and the
full suite re-run serially in the primary checkout. Two findings were registered by the round
itself, R-0853 and R-0854, and one more, R-0855, is drafted above for round 15 to book. The
reviewer's own authoring miss is recorded as R-0855 rather than hidden in a deviation, because the
dead code it names is on disk under `apps/` and `packages/`.

WHAT THE SESSION-7 MAP GOT WRONG, recorded because it is the reason this session re-measured
everything. That map named four survivors and missed `packages/orchestration/run_contract.py`,
whose two `ContractAction` members existed only for the adapter; it missed the enum USE SITES at
`orchestrator_brain.py` lines 687 and 807, which are what decide whether the two enum members may
die; it missed the surviving assertion at `tests/orchestration/test_orchestrator_brain.py` line
210, which would have gone red had they been deleted; and it missed one archive See-also link. A
handback map is a lead, and §3 item 34's "read every file the block orders a change against" is
what caught it.

CONTEXT SELF-ASSESSMENT, as amend0905-throughput requires in one sentence: the reviewer's context
was NOT the binding constraint and remained comfortable throughout — this session ran three full
serial suites at roughly 22 minutes each, one to establish round 14's boundary by execution, one to
gate it independently, and one inside round 15's dry run — and the session ends with round 15's
boundary measured by execution rather than read from source.

## What the next session owes, in order

FIRST, Phase 1 rule 1: re-read `.agent/STOP` from disk before the Open PR Gate. It does not exist
as this session ends, and was measured absent at the Phase 0 probe, again before authoring round
14, and again now. Then the Open PR Gate: no pull request is open, and none is owed until the
closure sequence.

SECOND, round 15's FIRST substantive commit books, from this file as the durable carrier under
amend0827-process-diet rule 1: the ROUND 14 PASS verdict above as a `Gate: F275 R14` entry in
`.agent/live_review.md`, the R-0855 registration, the prose slip as a dated line in
`.agent/prose_slips.md`, and `.agent/plan.md` advanced in the same commit per §3 item 23. The open
set is 79 by distinct id and the next free id is R-0856.

THIRD, round 15 itself, as a PRODUCTION-CODE round under §3 Round-types: complete the applied dry
run above to a green suite before authoring anything, rule the approval-gate question as a dated
DECISION in `.agent/decisions.md` before the first `git rm`, order the mutation red-proofs in full,
and register the RULE 3 finding the map names.
