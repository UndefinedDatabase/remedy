# Handback — F275 ROUND 8 — round 7's PASS is booked, R-0841 and R-0842 are registered, DECISION F275 D4 rules an EVENT-COUPLED consumer dies with its emitter, and the THIRD module group `context_pack` is gone with the tree green

This file supersedes the F275 round 7 handback. It is written by the delegated worker of F275
round 8 on the reviewer's authored text; the reviewer never edits a work-tree file. It carries NO
verdict of its own — verdicts live in `.agent/live_review.md`, and this round's C2 booked the
reviewer's authored F275 round 7 PASS there. C2 also REGISTERS two findings, R-0841 and R-0842,
so the open set moves 66 → 68 by distinct id (measured at G3(f)). C5 writes `Landed: R-0841` and
NOT `Done:` — §4 item 4 reserves resolution text for the reviewer, and block constraint 3 orders
the split explicitly. The next free id after this round is R-0843.

THE THIRD `git rm` OF F275, AND THE FIRST ONE WHOSE SURVIVING READERS WERE COUPLED BY EVENT NAME
RATHER THAN BY IMPORT. `packages/orchestration/context_pack.py` (317 lines),
`apps/cli/commands/context_pack_cmd.py` (83 lines) and `tests/test_context_pack.py` (176 lines)
are deleted whole, together with the `context.pack` catalog entry, the `related=` line naming it
on the SURVIVING `context.inspect` entry, the dispatch-table import and tuple member, the brain
node builder and its two edge types, the detail renderer, four presentation maps, two dead
`ui_server.py` readers, the humanized stream-event line in the cockpit's TypeScript catalog,
three smoke-script sections with their eight guard tests, seven surviving test call sites, one
ist-doc section and two ist-doc causal-chain lines, two allowlist lines and two cluster-map lines
— ONE commit, `d85f65e6`, **13 insertions against 955 deletions over 24 paths**. The FULL suite
is green after it at **19728 passed, 23 skipped, exit 0**, down exactly the THIRTY-TWO tests this
commit removes from the base's 19760, and that 32 is independently confirmed by `--collect-only`
over the five affected test files falling 317 → 285.

THIS ROUND IS NOT A DELETION ROUND. It edits lines under `packages/`, `apps/`, `scripts/` and
`tests/`, so operator amendment amend0906-triage-throughput's four-measurement shortcut does not
apply. It was gated as a production-code round: a three-mutation ratchet red-proof in a
disposable worktree, and the full suite run SERIALLY in the primary checkout. DECISION F275 D4,
which C3 lands, records that reasoning.

C3 precedes C4 by the block's design: DECISION F275 D4 is what authorises deleting the
event-coupled readers in the same commit as the emitter, so the ruling is on disk before the
deletion it authorises.

## Session

`SESSION 4 of feature F275 · round 8 · rounds so far 8`

CONTEXT SELF-ASSESSMENT (operator amendment amend0905-throughput): this worker's context is
comfortable — the round cost one block read, twenty-two targeted file edits and eight gates, with
two full-suite runs (24 minutes each) dominating wall clock rather than context. Nothing here
argues for ending the session; F275's soft limit is 20 sessions and 60 rounds by
amend0908-f275-finish RULE 1 and the feature stands at session 4, round 8.

## Range

Review of `65409e647b04939746ff010a687c48621022b9e3`..`83bd642a91383be01e223829d9f87d5cafb59062`

## Commits

Seven commits, every one single-parent, in the block's fixed order C0a, C0b, C1, C2, C3, C4, C5,
verified by `git rev-list --parents` (G8). C6 is the commit that writes this file and is not
tabled here — a handoff cannot table the commit that writes it (R-0149 pattern).

### ce1b3021 F275 R8 C0a: save the round 8 step block as authored text.
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r8.md` | +397/-0 | the step block, copied with `shutil.copyfile`, never retyped |

### 859f1552 F275 R8 C0b: mirror the round 8 step block into last_block.
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +374/-362 | the same bytes mirrored, one digest across all three artefacts |

### f622d5fe F275 R8 C1: the round 8 plan.
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +21/-19 | the PLAN8 slice, byte-identical; first substantive commit per §3 item 23 |

### 56589bf8 F275 R8 C2: book round 7's PASS, register R-0841 and R-0842, and record three prose slips.
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +6/-0 | the LEDGER8 slice: the round 7 `Gate:` record plus the R-0841 and R-0842 registrations |
| `.agent/prose_slips.md` | +6/-0 | the SLIPS8 slice: three dated lines for round 7's three wrong gate clauses |

### a3ab3c0c F275 R8 C3: DECISION F275 D4 rules an event-coupled consumer dies with its emitter.
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +16/-0 | the DECISION8 slice, eight paragraphs appended in order |

### d85f65e6 F275 R8 C4: delete the context_pack module group and its event-coupled readers.
| Path | +/- | Reason |
|---|---|---|
| `.agent/f275_deletion_order.md` | +0/-1 | REGENERATED by the shipped `measured_order()`; 13 components → 12 |
| `apps/cli/command_catalog.py` | +0/-16 | the `context.pack` entry and the `related=` line on the surviving `context.inspect` |
| `apps/cli/commands/__init__.py` | +1/-2 | the import line and the `for mod in (...)` tuple member |
| `apps/cli/commands/context_pack_cmd.py` | +0/-83 | `git rm` — the cluster command handler |
| `apps/ui/src/api/humanizeCatalog.ts` | +0/-1 | the humanized form of the `context_pack_created` stream event |
| `docs/system/architecture.md` | +2/-14 | the Step 49 section deleted; two causal-chain lines swept (R-0841 fix clause) |
| `packages/orchestration/brain_detail.py` | +0/-41 | `_detail_context_pack`, its import and its dispatch entry |
| `packages/orchestration/brain_viewer.py` | +0/-3 | layer, order and colour for the node type |
| `packages/orchestration/brain_viewer_theme.py` | +0/-1 | the theme entry |
| `packages/orchestration/context_pack.py` | +0/-317 | `git rm` — the cluster module itself |
| `packages/orchestration/project_brain.py` | +1/-33 | node/edge constants, `_build_context_pack_node`, the `summarizes` causal edge, the build call |
| `packages/orchestration/ui_copy.py` | +1/-2 | the label pair and the `_DIAGNOSTICS_ONLY` member |
| `packages/orchestration/ui_server.py` | +0/-10 | the dead `token_mode` block and the planner-bucket token-role branch |
| `packages/orchestration/ui_view_model.py` | +0/-1 | the `summarizes` edge humanization |
| `scripts/remedy_smoke.sh` | +5/-77 | section 12j deleted whole; 12l loses its event checks; 12s keeps only its token-policy half |
| `tests/cli/test_context_inspect_cli.py` | +0/-7 | `test_context_inspect_related_commands`, which asserted the deleted `related` value |
| `tests/conftest.py` | +0/-1 | the deleted test file's registry line |
| `tests/orchestration/import_reachability_allowlist.txt` | +0/-2 | both allowlist lines; the file is NOT re-sorted |
| `tests/orchestration/test_cluster_deletion_map.py` | +1/-3 | both map lines, plus the falsified handler comment (R-0841 sweep) |
| `tests/orchestration/test_project_brain.py` | +0/-2 | the builder name and the module path this test read from disk |
| `tests/regression/test_named_bugs.py` | +0/-1 | the module path this test read from disk |
| `tests/storage/test_persistence.py` | +1/-107 | four importing methods, `TestContextPackMemory` with its orphaned banner, and the R-0841 docstring fix |
| `tests/test_context_pack.py` | +0/-176 | `git rm` — the module's own suite |
| `tests/test_remedy_smoke_script.py` | +1/-54 | eight guard tests with two section headers, plus the R-0841 `Step 64` header fix |

### 83bd642a F275 R8 C5: record R-0841 as landed, awaiting the reviewer's resolution text.
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-0 | the LANDED8 slice; a worker never writes its own `Done:` |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/r8-redproof d85f65e6` | created, detached at C4 — the ONLY place any mutation ran |
| `git checkout --detach 65409e64…` inside that worktree | moved to the base for G7's base-side ruff and collect-only readings |
| `git worktree remove --force .remedy-wt/r8-redproof` | removed |
| `git worktree prune` | pruned; `git worktree list` now shows the primary checkout ALONE |
| `git push -u origin feature/f275-one-world-completion-part-three` | run AFTER C6, which is the commit that writes this file; its real result is reported in the session output rather than here, because a handoff cannot record the outcome of pushing itself |

No `gh` command was run. No PR was created, edited or merged. The `remedy` CLI was NOT invoked at
any point — it is denied in this environment and no gate needed it.

## Verification

Eight gates, all RUN, real exit codes and real numbers. Every numeric prediction the block made
was MET; no gate clause disagreed with a measurement this round.

| Gate | Result |
|---|---|
| G1 TRANSPORT | PASS — the scratch original, the committed `.agent/authored/f275-r8.md` and the committed `.agent/last_block.md` are all **44438 bytes** at **`26d8266f11ea4bd868ad172f1ed588607ba30430f9b8555012d5c31ef3ca4457`**. Per §3 item 37 this chain covers those three artefacts and claims nothing about the emitted bytes. |
| G2 THE PLAN | PASS — committed `.agent/plan.md` is BYTE-IDENTICAL to PLAN8: 2614 bytes, sha `a661322e…`, **43 lines** against the AGENTS.md cap of 50, `^## Goal$` × 1, `^## Next Steps$` × 1. |
| G3 THE RECORD | PASS — read from the committed blobs at C1 (pre) and C2 (post). (a) `live_review.md` 541694 → 551407, gain **9713 = 1 + 9712**; `prose_slips.md` 172799 → 173925, gain **1126 = 1 + 1125**. (b) both: pre-blob a byte-exact PREFIX, one newline plus the slice a byte-exact SUFFIX. (c) N counted from each slice by my own reader = **3** and **3**; the last N units equal the slice's N paragraphs IN ORDER for both. (d) negative control on the FIRST appended paragraph of each, IN MEMORY ONLY, REJECTED by both readers (b) and (c); tracked files re-read from disk afterwards unchanged. (e) `^Gate: ` 29 → 30, `^Gate: F275 R7 ` 0 → 1, `^- R-0841 — ` = 1, `^- R-0842 — ` = 1. (f) OPEN SET **66 → 68 by distinct id**; registrations 69 → 71, resolutions 3 → 3. |
| G4 THE DECISION | PASS — committed blobs at C2 (pre) and C3 (post). `decisions.md` 953044 → 958331, gain **5287 = 1 + 5286**; both edges exact; N counted from the slice = **8**, ordered equality holds; negative control on the first appended paragraph REJECTED by both readers, in memory only, tracked size unchanged on disk; `^## DECISION F275 D` 3 → 4; `^## DECISION F275 D4 ` heads exactly ONE section. |
| G5 THE DELETION IS COMPLETE | PASS — `git ls-tree -r d85f65e6 --name-only` finds NONE of the three deleted files. Over the TRACKED tree at C4, outside `.agent/`, all ELEVEN strings are at **ZERO**: `context_pack_created`, `build_context_pack`, `export_context_pack_json`, `summarize_context_pack`, `NT_CONTEXT_PACK`, `ET_HAS_CONTEXT_PACK`, `ET_SUMMARIZES`, `_build_context_pack_node`, `_detail_context_pack`, `context_pack_cmd`, `context.pack`. The WHOLE-WORD token `context_pack` outside `.agent/` reads **SEVEN**, exactly the predicted survivor set, EVERY HIT PRINTED: `docs/roadmap/features/T2_F260.md:341` ×1, `packages/orchestration/main_builder_adapter.py:36,446,460` ×3, `tests/orchestration/test_main_builder_adapter.py:162` ×1, `tests/orchestration/test_managed_builder_execution.py:1634,1734` ×2 — all of them must-not-touch items. |
| G6 RATCHETS, READERS, RED-PROOF | PASS — primary checkout: the three-suite ratchet command **EXIT 0, 9 passed**; the docs trio **EXIT 0, 345 passed**; the canary `tests/cli/test_golden_path.py` **EXIT 0, 42 passed**. Through the SHIPPED readers, `apps.cli.commands.collect_all_handlers` is **335** and `apps.cli.command_catalog._BASE_CATALOG` is **335** (both 336 at the base — the one deleted command), with `context.pack` ABSENT from both and `context.inspect` PRESENT in both. The regenerated order body is printed in full below. RED-PROOF, in the disposable worktree at C4 and nowhere else, `__pycache__` purged and `python3 -B` before every run, each FROM string counted at 1 in its own named file, each mutation applied ALONE and reverted byte-identically (sha256 re-checked, all three `True`): control **EXIT 0** (9 passed) → (i) `CLUSTER_MODULES` **EXIT 1** (2 failed, 7 passed) → (ii) order-file body line **EXIT 1** (2 failed, 7 passed) → (iii) allowlist **EXIT 1** (1 failed, 8 passed) → control **EXIT 0** (9 passed). The reviewer predicted 0, 1, 1, 1, 0 and that is what ran. Worktree removed and pruned; `git worktree list` shows the primary checkout ALONE. |
| G7 RUFF AND THE FULL SUITE | PASS — `python3 -m ruff check` over all sixteen Python files this round edits: **`All checks passed!`**. `python3 -m ruff check packages/ apps/cli/ tests/` reads **24 at the base** (taken in the disposable worktree, never over the primary checkout) and **24 at C4**; grouping the C4 errors by file shows NONE in any file this round touches. `bash -n scripts/remedy_smoke.sh` **EXIT 0**. `python3 -m pytest tests/ -q` SERIALLY, no `-n auto`: **EXIT 0, 19728 passed, 23 skipped, 1 warning** in 23:21. `--collect-only -q` over the five named files at the base = **317**; over the four survivors at C4 = **285**; fall = **32**. The suite fall is 19760 − 19728 = **32**. The two falls AGREE. |
| G8 THE TREE | PASS — `.agent/STOP` does not exist; `git status --porcelain` EMPTY; branch `feature/f275-one-world-completion-part-three`; `git worktree list` shows the primary checkout alone. `git diff --name-only <base>..<C5>` names **30 paths**, EXACTLY the block's 31-path change set minus `.agent/handoff.md`, with no extra and none missing. Every commit in the range is single-parent in the order C0a, C0b, C1, C2, C3, C4, C5. Per-commit INSERTIONS (the `+` column only, per AGENTS.md DECISION F104 D1) against the cap of 500: C0a **397**, C0b **374**, C1 **21**, C2 **12**, C3 **16**, C4 **13**, C5 **2**. |

THE REGENERATED `.agent/f275_deletion_order.md` BODY, IN FULL, as committed at C4 — twelve
components where the base had thirteen, `review_bundle` now first, produced by running the shipped
`measured_order()` against the live import graph after steps (1) to (21) were on disk, never typed:

```
packages.orchestration.review_bundle
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
```

The 26-line `# ` comment header was kept VERBATIM and only the body below it was rewritten, per
block constraint 7. The regeneration is a PURE DELETION in the diff (`+0/-1`), which is itself
evidence that the surviving order did not move: had a line been retyped or a component reordered,
the numstat would carry insertions.

## Authored-text proofs

Five reviewer-authored slices, each extracted by its own BEGIN/END delimiters from the block on
disk, each digest verified BEFORE use, each applied BYTE FOR BYTE with no edit, reflow or
correction:

| Slice | Declared bytes | Declared sha256 | Measured | Verdict |
|---|---|---|---|---|
| PLAN8 | 2614 | `a661322e908605f9…` | 2614 / `a661322e908605f9…` | MATCH — and the committed `.agent/plan.md` is byte-identical to it (G2) |
| LEDGER8 | 9712 | `3976b5eb4bd5860e…` | 9712 / `3976b5eb4bd5860e…` | MATCH — appended, both edges byte-exact (G3) |
| SLIPS8 | 1125 | `2f9600d26575369d…` | 1125 / `2f9600d26575369d…` | MATCH — appended, both edges byte-exact (G3) |
| DECISION8 | 5286 | `634502400c89f1b7…` | 5286 / `634502400c89f1b7…` | MATCH — appended, both edges byte-exact (G4) |
| LANDED8 | 872 | `680d3828d40842cc…` | 872 / `680d3828d40842cc…` | MATCH — appended at C5, both edges byte-exact |

The block itself: 44438 bytes at `26d8266f…`, verified against the delegation's two stated values
BEFORE any file was written, and carried to both `.agent/` destinations with `shutil.copyfile`.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | this commit |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | |
| G5 | done | |
| G6 | done | |
| G7 | done | |
| G8 | done | |

## Deviations & assumptions

The block's ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5, gates, C6 was followed EXACTLY.
No commit was added, dropped or reordered. Five items are declared below; none is a departure from
the sequence and none required a judgement the block forbade.

**1. THE FULL SUITE WAS RUN TWICE, AND THE SECOND RUN IS THE ONE REPORTED.** The first invocation
was piped to `tail`, which made `$?` the exit code of `tail` rather than of pytest, so the numeric
code was never observed. Rather than report an exit code I had not seen, I re-ran the identical
command through `subprocess.run` and read `returncode` directly: **0**, at 19728 passed and 23
skipped, identical counts to the first run. Both runs took ~23.5 minutes. This costs wall clock
and nothing else; no file was touched between them and the tree was clean throughout.

**2. THE SMOKE SCRIPT'S 12s HEADING WAS REWRITTEN TO DROP ITS DESCRIPTION OF THE DELETED HALF, NOT
ONLY ITS TWO WORDS.** Step (12)(c) orders the heading comment and the `echo` rewritten "from Token
economy to Token policy". The heading also carried `— caveman/compact/standard ordering`, which
described precisely the `python3 -c` block that step deletes. I wrote
`    # 12s. Token policy (Step 56)` and `    echo "--- 12s. Token policy"`. Keeping the ordering
clause would have left a section comment falsified by its own commit — the exact R-0841 class this
round's fix clause orders swept. This is TWO insertions, which is what the step's arithmetic
implies: the five smoke-script insertions measured at C4 are the heading, the echo, the 12l
comment, the 12l echo and the 12l closing `print`, and the round's total lands on 13 exactly as
the reviewer's own application did.

**3. DELETED UNITS WERE TAKEN WITH THEIR SEPARATING BLANK LINES, WHICH IS WHY 955 DELETIONS STAND
AGAINST THE REVIEWER'S 952.** Three cells differ, all in the same direction and all for the reason
round 7 already established and the block itself anticipates: the smoke script's 12s ordering
block was taken together with the blank line that separated it from the surviving
`# Token policy required fields` half, and `tests/storage/test_persistence.py` ends at the last
statement of the class above rather than at a run of trailing blanks. Insertions are UNAFFECTED at
13, and every per-step insertion count the block names as load-bearing reproduces exactly:
`__init__.py` 1, `project_brain.py` 1, `ui_copy.py` 1, `test_remedy_smoke_script.py` 1,
`test_persistence.py` 1, `test_cluster_deletion_map.py` 1, `architecture.md` 2, and
`command_catalog.py` 0.

**4. A STALE COUNT IN `docs/system/architecture.md` WAS LEFT UNTOUCHED, DELIBERATELY.** The
"Groups" table at line ~2977 carries the row `| context | 1 | Build token-budgeted context packs |`.
The description now names a capability the `context` group no longer has, since `context.inspect`
is its only surviving command. I did not edit it: step (21) names exactly two insertions for that
file and neither is this row, the row is not reachable by any string G5 gates, and the same table
is ALREADY stale independently of this round (`worker | 1` against a catalog that ships
`worker.list` and `worker.show`; `memory | 4`). Repairing one row of a table that documents a
Step-N-era snapshot would be an unordered edit and would break the file's stated insertion count.
Flagging it here rather than fixing it, per block constraint 1. It is a candidate for the sweep a
later round runs over that page, not for this one.

**5. THE COMMAND CATALOG'S GROUP SEPARATOR BLANK LINE IS GONE, AS ORDERED.** Step (3) orders the
`context.pack` entry deleted "through its closing `    ),` and the blank line that follows it".
That blank line was the separator before the `# ── change ──` group comment, so the surviving
`context.inspect` entry's `    ),` is now directly followed by that comment, where every other
group boundary in the file has a blank line before its comment. I applied the step as written
rather than preserving the separator. Ruff is clean over the file and the catalog reader is green
(G6: `_BASE_CATALOG` = 335, `context.inspect` present), so nothing is broken; it is a cosmetic
inconsistency the reviewer may want to look at.

NO FINDING WAS MINTED BY THIS WORKER and none was resolved. C2's two registrations, R-0841 and
R-0842, are the REVIEWER's authored text applied byte-for-byte, not this worker's judgement.
`Landed: R-0841` at C5 asserts only that the fix is on disk; whether it discharges the finding is
the reviewer's call at the next gate.

## Next

The reviewer re-runs G1..G8 itself against the committed blobs over
`65409e647b04939746ff010a687c48621022b9e3..HEAD`, reads the C4 diff bottom-up, and issues the
round 8 verdict. On PASS, `LAST_REVIEWED_SHA` advances to this round's tip and round 9 begins with
Phase 1 rule 1 — re-read `.agent/STOP` from disk — before anything else. The next module group in
the regenerated order is `review_bundle`, which DECISION F275 D3 keeps DEFERRED until a session
can carry it whole (2254 lines, sixteen surviving test importers, eight `docs/system/` pages, a
`pyproject.toml` per-file ignore and list entry, and `scripts/remedy_test_runtime.sh`); round 9
should therefore take the next component the order file permits rather than the literal first
line, or open the session that can carry `review_bundle` entire.
