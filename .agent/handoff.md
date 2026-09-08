# Handback — F275 ROUND 9 — round 8's PASS is booked, R-0841 is RESOLVED, R-0843 and R-0844 are registered, and the FOURTH module group `review_bundle` is gone with the tree green

This file supersedes the F275 round 8 handback. It is written by the delegated worker of F275
round 9 on the reviewer's authored text; the reviewer never edits a work-tree file. It carries NO
verdict of its own — verdicts live in `.agent/live_review.md`, and this round's C2 booked the
reviewer's authored F275 round 8 PASS there. C2 also lands the reviewer-authored `Done: R-0841`
paragraph and REGISTERS R-0843 and R-0844, so the open set moves 68 → 69 by distinct id
(measured at G3(f): two registrations, one resolution). Block constraint 3 forbids the worker
writing any `Done:` paragraph of its own, and none was written. The next free id after this round
is R-0845.

THE FOURTH `git rm` OF F275, AND THE FIRST ONE WHOSE ONLY SURVIVING IMPORTER WAS INVISIBLE TO AN
IMPORT GRAPH. `packages/orchestration/review_bundle.py` (2254 lines),
`tests/orchestration/test_review_bundle.py` (1358 lines),
`tests/cli/test_review_bundle_runtime.py` (327 lines) and the two `docs/system/` pages whose
subject the module was (73 + 96 lines) are deleted whole, together with the ONE `review.bundle`
catalog entry, the ONE handler function `_cmd_review_bundle` and its handler-table line, the
STRING-keyed `importlib` doctor probe in `apps/cli/commands/worker_facade_cmd.py` that no AST
sweep can see, one allowlist line, one `CLUSTER_MODULES` line, two `pyproject.toml` lines, the
runtime lane's array member and its header comment, three lane-roster lines across two files,
27 test functions in 16 surviving files, the 10 class headers those left empty, 10 orphaned
imports, eight doc lines across seven pages, and the regenerated deletion-order file — ONE
commit, `6c601b35`, **11 insertions against 4694 deletions over 40 paths**.

THE FILE `apps/cli/commands/review_cmd.py` SURVIVES, and that is the scope line of this round.
It held FIVE handlers; only `_cmd_review_bundle` imported the deleted module and the other four
drive `packages/orchestration/reviewer.py`, which is NOT on F260's Design list. So the `review`
group, its `GroupDef` and four of its five catalog entries survive — G5(c) prints all four as
PRESENT through the shipped readers. The session-4 map that prescribed deleting the file whole
was measured RED at fifteen failures before authoring; that correction is recorded as the second
`.agent/prose_slips.md` line this round appends.

THIS ROUND IS NOT A DELETION ROUND under operator amendment amend0906-triage-throughput: it edits
lines under `packages/`, `apps/`, `scripts/`, `tests/` and `docs/`, so the four-measurement
shortcut does not apply and it was gated as a production-code round — a three-mutation ratchet
red-proof in a disposable worktree with an unmutated control on both sides, and the full suite run
SERIALLY in the primary checkout.

## Session

`SESSION 5 of feature F275 · round 9 · rounds so far 9`

CONTEXT SELF-ASSESSMENT (operator amendment amend0905-throughput): this worker's context is
comfortable — the round cost one block read, seventeen ordered edit steps over 40 paths and eight
gates, with the 24-minute full suite as the only long wall-clock item; nothing was re-read twice
and no gate had to be repeated.

F275's soft limit is 20 sessions and 60 rounds by operator amendment amend0908-f275-finish, BY
NAME. At session 5 / round 9 the feature is well inside it, so no scope report is owed.

## Range

Review of `aae6d313dbedc64c84703eae7a782e67439ccdec`..`6c601b35` (C4 excluded — a handoff cannot
table the commit that writes it; R-0149 pattern).

## Commits

### b3db8d01 F275 R9 C0a: save the round 9 step block verbatim.

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f275-r9.md | +400/-0 | the round 9 step block, copied with `shutil.copyfile`, digest `178bd6ca…` |

### effecd77 F275 R9 C0b: mirror the round 9 block into last_block.

| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +372/-369 | the SAME bytes, copied with `shutil.copyfile`; same digest |

### 2901e0b2 F275 R9 C1: the round 9 plan.

| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +19/-17 | replaced whole by the PLAN9 slice, byte for byte |

### ea039fc8 F275 R9 C2: book the round 8 PASS, resolve R-0841, register R-0843 and R-0844.

| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +8/-0 | LEDGER9 appended: `Gate: F275 R8` PASS, `Done: R-0841`, `- R-0843`, `- R-0844` |
| .agent/prose_slips.md | +4/-0 | SLIPS9 appended: the R8 catalog-blank-line slip and the R9 over-wide-map slip |

### 6c601b35 F275 R9 C3: delete the review_bundle module group and its call sites.

| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/review_bundle.py | +0/-2254 | step (1) — the module, deleted whole |
| tests/orchestration/test_review_bundle.py | +0/-1358 | step (1) — its unit suite, deleted whole |
| tests/cli/test_review_bundle_runtime.py | +0/-327 | step (1) — its runtime suite, deleted whole |
| docs/system/review-bundle-v1.md | +0/-73 | step (1) — the ist-doc whose subject it was |
| docs/system/review-bundle-structured-error-reporting-v1.md | +0/-96 | step (1) — ditto |
| apps/cli/commands/review_cmd.py | +0/-31 | step (2) — `_cmd_review_bundle` + its handler-table line; the FILE and the other four handlers survive |
| apps/cli/command_catalog.py | +0/-14 | step (3) — the ONE `review.bundle` `CommandEntry`; the group comment and `GroupDef` survive |
| tests/orchestration/import_reachability_allowlist.txt | +0/-1 | step (4) — the module's allowlist line; `apps.cli.commands.review_cmd` kept |
| tests/orchestration/test_cluster_deletion_map.py | +0/-1 | step (5) — the `CLUSTER_MODULES` member |
| apps/cli/commands/worker_facade_cmd.py | +0/-1 | step (6) — the STRING-keyed `importlib` doctor probe, the R-0832 class |
| tests/cli/test_worker_facade_cmd.py | +1/-1 | step (7) — the fake-`ImportError` probe retargeted to `run_contract` so the branch stays reachable |
| packages/orchestration/ui_server.py | +1/-1 | step (8a) — R-0841 sweep: the comment naming the deleted module beside `do_run`/`proof_chain` |
| tests/orchestration/test_progress_redaction.py | +1/-1 | step (8c) — R-0841 sweep: test renamed to `test_progress_ledger_export_no_raw_secrets` |
| pyproject.toml | +0/-2 | step (9) — the `F402` per-file ignore and the mypy override entry |
| scripts/remedy_test_runtime.sh | +2/-4 | step (10) — the array member gone, the header comment rewritten, `NODE_ISOLATED_FILES=()` kept |
| tests/test_test_categories.py | +0/-2 | step (12a) — both lane-roster occurrences |
| tests/cli/test_product_spine.py | +0/-13 | steps (12b) + (13) — the `heavy` roster line and two lane self-tests |
| tests/orchestration/test_development_artifact_boundary.py | +2/-37 | steps (8b), (11), (13) — rename, `_ALLOWED_LEGACY` line, two functions |
| tests/orchestration/test_config.py | +0/-50 | step (13) — three `TestRedactionClosure` functions |
| tests/orchestration/test_do_continue.py | +0/-20 | step (13) — one function |
| tests/orchestration/test_external_builder_sandbox.py | +1/-67 | steps (13)(14)(15) — 2 functions, 2 class headers, `UUID` narrowed out |
| tests/orchestration/test_job_fulfillment.py | +0/-81 | steps (13)(14) — 5 functions, 3 class headers |
| tests/orchestration/test_model_route_tournament_integration.py | +0/-10 | steps (13)(15) — one function, `import json` |
| tests/orchestration/test_overnight_executor.py | +0/-33 | steps (13)(14)(15) — one function, `TestRedaction`, `import json` |
| tests/orchestration/test_overnight_mission_integration.py | +0/-18 | steps (13)(15) — two functions, `import json` |
| tests/orchestration/test_provider_patch_material.py | +0/-23 | step (13) — one function |
| tests/orchestration/test_provider_trust.py | +0/-39 | steps (13)(14) — one function, `TestRedaction` |
| tests/orchestration/test_repair_request_builder.py | +0/-34 | steps (13)(14)(15) — one function, `TestRedaction`, `import json` |
| tests/orchestration/test_self_dogfood.py | +2/-35 | steps (13)(14)(15) — one function, `TestRedaction`, three import narrowings |
| tests/orchestration/test_self_dogfood_execution.py | +0/-31 | steps (13)(14)(15) — one function, `TestRedaction`, `import json` |
| tests/orchestration/test_token_economy_integration.py | +0/-16 | steps (13)(15) — two functions, `import json` |
| tests/orchestration/test_worker_route_integration.py | +0/-9 | step (13) — one function |
| docs/README.md | +0/-3 | step (16) — one quick-find row and two index rows for the two deleted pages |
| docs/system/test-lanes-v0.md | +1/-2 | step (16) — the table row, and only the parenthetical out of the paragraph |
| docs/system/development-artifact-boundary-v0.md | +0/-1 | step (16) — the `Review bundle artifact inclusion` row |
| docs/system/run-contract-v1.md | +0/-1 | step (16) — the `- **review_bundle**:` bullet |
| docs/system/snapshot-rollback-v1.md | +0/-1 | step (16) — the `` `review_bundle.py` `` row |
| docs/guides/self-repair-proposal-user-guide-v0.md | +0/-1 | step (16) — the `review_bundle:<section_name>` bullet |
| docs/system/run-replay-to-self-repair-proposal-v0.md | +0/-1 | step (16) — the `review_bundle:<section_name>` bullet |
| .agent/f275_deletion_order.md | +0/-1 | step (17) — REGENERATED by the shipped `measured_order()`; pure deletion, twelve components → eleven |

### C4 (this commit) F275 R9 C4: the round 9 handback.

| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | (self-reference) | this file — a handoff cannot table the commit that writes it |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/r9-redproof 6c601b35` | added at detached `6c601b35` — G5(e) red-proof |
| `git worktree remove --force .remedy-wt/r9-redproof` + `git worktree prune` | removed and pruned |
| `git worktree add --detach .remedy-wt/r9-ruffbase aae6d313…` | added at the base — G6 base-side ruff reading |
| `git worktree remove --force .remedy-wt/r9-ruffbase` + `git worktree prune` | removed and pruned |
| `git worktree add --detach .remedy-wt/r9-collectbase aae6d313…` | added at the base — G7 base-side `--collect-only` readings |
| `git worktree remove --force .remedy-wt/r9-collectbase` + `git worktree prune` | removed and pruned |
| `git push -u origin feature/f275-one-world-completion-part-three` | run after C4 — see the Push line below |
| PR create / edit / merge | NONE — the block forbids it |
| `remedy` CLI | NEVER INVOKED — denied in this environment, and no gate needs it |

Push after C4: pushed `b3db8d01`, `effecd77`, `2901e0b2`, `ea039fc8`, `6c601b35` and C4 to
`origin/feature/f275-one-world-completion-part-three`. No force, no PR.

## Verification

ALL EIGHT GATES WERE RUN. Real exit codes and real numbers; no gate is reported as a word.

**G1 TRANSPORT — PASS.** One digest comparison over three artefacts.
`.agent/authored/f275-r9.md` at `b3db8d01` = 36871 bytes,
sha256 `178bd6cae149517cab73a806385dd9bd608176e4416247713b3c6ca34333d7fe`;
`.agent/last_block.md` at `effecd77` = 36871 bytes, same sha256; both re-read at `HEAD`, same
sha256; and all three equal the digest stated in the delegation. Per §3 item 37 this claims
NOTHING about the bytes the reviewer emitted — all three artefacts are this worker's own output
and the comparison can only detect a fault in my own copying, not in the transport that reached me.

**G2 THE PLAN — PASS.** Committed `.agent/plan.md` at `2901e0b2` = 2616 bytes, sha256
`8f034865f73fda9287f167b16e80871f06e38b07f3c39d16ced2e204cf63279f`; PLAN9 slice = 2616 bytes, same
sha256; BYTE-IDENTICAL True. Line count 45 against the AGENTS.md cap of 50. `^## Goal$` × 1,
`^## Next Steps$` × 1.

**G3 THE RECORD — PASS.** Read from the committed blobs at C1 (`2901e0b2`, pre) and C2
(`ea039fc8`, post); the worktree was never the source.
- (a) `.agent/live_review.md` 552280 → 559516, growth 7236 = 1 + 7235 ✓.
  `.agent/prose_slips.md` 173925 → 175541, growth 1616 = 1 + 1615 ✓.
- (b) pre-blob is a byte-exact PREFIX and the slice a byte-exact SUFFIX of the post-file, for
  BOTH files; the joining byte read back as `b'\n'` in both.
- (c) INDEPENDENT structural reader: N counted from the slice itself = 4 paragraphs for LEDGER9
  and 2 for SLIPS9; the file's LAST N blank-line-separated units equal the slice's N paragraphs
  IN ORDER — True in both, per-unit sha256 printed for all six units.
- (d) NEGATIVE CONTROL on the FIRST appended paragraph of each, flipped IN MEMORY ONLY at offsets
  552281 and 173926: reader (b) REJECTS True, reader (c) REJECTS True, for both files. The
  tracked files were re-read from disk afterwards and are byte-equal to the committed post-blobs.
- (e) `^Gate: ` 30 → 31 (delta +1), `^Gate: F275 R8 ` = 1, `^Done: R-0841 ` = 1, `^- R-0843 — ` = 1,
  `^- R-0844 — ` = 1.
- (f) OPEN SET BY DISTINCT ID: pre 71 registrations / 3 resolutions / **68 open**; post 73 / 4 /
  **69 open**. Registrations this round: R-0843, R-0844 (two). Resolutions this round: R-0841
  (one). Exactly the 68 → 69 the block predicts.

**G4 THE DELETION IS COMPLETE — PASS.** `git ls-tree -r 6c601b35 --name-only` reads 4632 tracked
files and contains NONE of the five files of step (1) (each printed False). Scope = the tracked
tree excluding `.agent/` and `.data/` = 1753 files. All ten strings at ZERO hits:
`build_review_bundle` 0, `export_review_bundle_json` 0, `summarize_review_bundle` 0,
`ReviewBundleResult` 0, `packages.orchestration.review_bundle` 0, `_cmd_review_bundle` 0,
`"review.bundle"` 0, `test_review_bundle_runtime` 0, `review-bundle-v1` 0,
`review-bundle-structured-error-reporting` 0. The whole-word token `review_bundle` over that same
scope reads **EXACTLY FIVE lines**, all five printed:

    docs/roadmap/features/T2_F260.md:346          (the specification)
    docs/roadmap/features/T2_F272.md:744          (the specification)
    packages/orchestration/self_repair_proposal.py:441   (a cluster module — RULE 2 defers it)
    packages/orchestration/self_repair_proposal.py:442   (ditto)
    packages/orchestration/self_repair_proposal.py:532   (ditto)

No sixth line.

**G5 RATCHETS, READERS AND THE RED-PROOF — PASS with one measured disagreement in (c).**
- (a) `python3 -B -m pytest tests/orchestration/test_import_reachability.py
  tests/orchestration/test_cluster_deletion_map.py tests/orchestration/test_cluster_deletion_order.py -q`
  → **exit 0, 9 passed** in 5.39s.
- (b) `python3 -B -m pytest tests/docs/ -q` → **exit 0, 303 passed** in 0.49s. Canary
  `python3 -B -m pytest tests/cli/test_golden_path.py -q` → **exit 0, 42 passed** in 20.82s.
- (c) THROUGH THE SHIPPED READERS: `len(apps.cli.command_catalog._BASE_CATALOG)` = **334** and
  `len(apps.cli.commands.collect_all_handlers())` = **334** at C3, against **335** for both at the
  base. The block predicts 335 at C3 against 336 at the base. THE DELTA IS EXACTLY THE PREDICTED
  −1; the ABSOLUTE numbers are each one lower than the block states. See deviation 2. `review.bundle`
  is ABSENT from both readers (False, False) and the four survivors are PRESENT in both:
  `review.run` catalog=True handlers=True, `review.list` True/True, `review.accept` True/True,
  `review.reject` True/True.
- (d) `.agent/f275_deletion_order.md` holds **ELEVEN** components at C3 against twelve at the base,
  and `git show --numstat 6c601b35 -- .agent/f275_deletion_order.md` reads `0	1` — a PURE DELETION.
  The file was REGENERATED by importing the shipped `measured_order()` from
  `tests/orchestration/test_cluster_deletion_order.py` and rendering its output under the
  26-line comment header kept verbatim; it was not hand-edited.
- (e) RED-PROOF, in the disposable worktree `.remedy-wt/r9-redproof` at `6c601b35` and NOWHERE
  ELSE, `__pycache__` purged before every run and `python3 -B` throughout. Selection = the
  three-test command of (a). Each FROM string was counted 1 in its own named file first, each
  mutation applied ALONE and reverted, the revert re-checked by sha256:

      control #1 (unmutated)                                  EXIT=0  failures=0   9 passed
      (i)   CLUSTER_MODULES line restored, test_cluster_deletion_map.py
            FROM count 1 → MUTATED                            EXIT=1  failures=2   2 failed, 7 passed
            reverted byte-identically: sha256 3fe01a9f82ed3423 == 3fe01a9f82ed3423
      (ii)  `packages.orchestration.review_bundle` restored as the FIRST body line of
            .agent/f275_deletion_order.md
            FROM count 1 → MUTATED                            EXIT=1  failures=2   2 failed, 7 passed
            reverted byte-identically: sha256 b92ffe55f452d5eb == b92ffe55f452d5eb
      (iii) the same line restored to import_reachability_allowlist.txt
            FROM count 1 → MUTATED                            EXIT=1  failures=1   1 failed, 8 passed
            reverted byte-identically: sha256 d259cf59e34caa29 == d259cf59e34caa29
      control #2 (after all reverts)                          EXIT=0  failures=0   9 passed

  The ORDER of colours is control 0 → 1 → 1 → 1 → control 0, exactly as the block expects. The
  worktree was then removed and pruned, and `git worktree list` printed
  `/home/decodeux/Repos/remedy  6c601b35 [feature/f275-one-world-completion-part-three]` — the
  primary checkout ALONE.

**G6 RUFF AND BASH — PASS.** `git diff --name-only aae6d313…..6c601b35` names 45 paths, 27 of them
`.py`; three of those 27 are the deleted files, so **24** `.py` files still exist at C3 and are the
ones ruff can read. `python3 -m ruff check` over exactly those 24, named from the diff:
**`All checks passed!`, exit 0**. `python3 -m ruff check packages/ apps/cli/ tests/` reads
**`Found 24 errors.` (exit 1) at C3** in the primary checkout, and the SAME command read at the
base `aae6d313dbedc64c84703eae7a782e67439ccdec` inside the disposable worktree
`.remedy-wt/r9-ruffbase` — never by overwrite-and-restore in the primary checkout — also reads
**`Found 24 errors.` (exit 1)**. Unchanged, as the block predicts. That worktree was removed and
pruned. `bash -n scripts/remedy_test_runtime.sh` → **exit 0**, no output.

**G7 THE FULL SUITE — PASS, and the arithmetic closes exactly.**
`python3 -m pytest tests/ -q` in the PRIMARY CHECKOUT, SERIALLY (no `-n auto`), exit code read
from the process object and never from a pipe:

    REAL EXIT CODE FROM THE PROCESS = 0
    19590 passed, 23 skipped, 1 warning in 1436.14s (0:23:56)

The one warning is the pre-existing `model_routing.py:1392` undeclared-role `UserWarning`, not
this round's. The four numbers:

| Reading | Value |
|---|---|
| `--collect-only tests/` at the base | **19751** |
| `--collect-only tests/` at C3 | **19613** |
| the fall | **138** |
| the two deleted test files at the base | **104** |
| collected-id fall over the 16 files of step (13) | **534 → 500 = 34** |
| 104 + 34 | **138** — closes against the fall |
| the suite's own pass+skip total at C3 | 19590 + 23 = **19613**, down 138 from the base's 19728 + 23 = 19751 |

The base-side `--collect-only` readings for the two deleted files and for the 16 step-(13) files
were taken in the disposable worktree `.remedy-wt/r9-collectbase` at the base commit, which was
then removed and pruned; the whole-suite base reading of 19751 was taken in the primary checkout
BEFORE C3, while its code tree was still byte-identical to the base (C0a…C2 touch `.agent/` only).

**G8 THE TREE — PASS, with one measured disagreement in the path numeral.**
- `.agent/STOP` re-read from disk: **does not exist**.
- `git status --porcelain` → **0 bytes, EMPTY**.
- `git worktree list` → `/home/decodeux/Repos/remedy  6c601b35 [feature/f275-one-world-completion-part-three]`
  — the primary checkout **ALONE**; all three disposable worktrees removed and pruned.
- branch = `feature/f275-one-world-completion-part-three`.
- `git diff --name-only aae6d313dbedc64c84703eae7a782e67439ccdec..6c601b35` names **45** paths.
  Set-compared against the block's own enumerated change set minus `.agent/handoff.md`, which
  mechanically counts **45** paths (the enumeration holds 46 distinct paths in total):
  **EXACT SET MATCH True — nothing extra, nothing missing.** The block's headline "45 paths" and
  G8's "44 paths" are each one low; see deviation 1. The SET is exactly right.
- Every commit in the range is SINGLE-PARENT, in the block's order:

| Commit | SHA | parents | insertions (`+` only) | deletions | cap 500 |
|---|---|---|---|---|---|
| C0a | b3db8d01 | 1 | 400 | 0 | under |
| C0b | effecd77 | 1 | 372 | 369 | under |
| C1 | 2901e0b2 | 1 | 19 | 17 | under |
| C2 | ea039fc8 | 1 | 12 | 0 | under |
| C3 | 6c601b35 | 1 | **11** | 4694 | under |

Insertions only, per AGENTS.md DECISION F104 D1. No oversize commit and none declared. C4's own
numbers belong to the next round's ledger entry (§3 item 31) and are not stated here.

## Authored-text proofs

| Slice | Bytes | sha256 | Applied to | Disk-to-disk result |
|---|---|---|---|---|
| PLAN9 | 2616 | `8f034865f73fda92…cf63279f` | `.agent/plan.md` (replaced whole, C1) | committed blob byte-identical to the slice — G2 |
| LEDGER9 | 7235 | `10c3aedcfe88e740…6904d10a8` | `.agent/live_review.md` (appended, C2) | byte-exact SUFFIX of the committed post-blob; growth 1 + 7235 — G3 |
| SLIPS9 | 1615 | `d2443a066f5e2c85…b4911c7f90` | `.agent/prose_slips.md` (appended, C2) | byte-exact SUFFIX of the committed post-blob; growth 1 + 1615 — G3 |

Each slice was extracted as the bytes strictly BETWEEN its `BEGIN` and `END` delimiter lines, and
its byte count and sha256 were verified against the values on its own `BEGIN` line BEFORE it was
used. The block file itself was verified at 36871 bytes / sha256
`178bd6cae149517cab73a806385dd9bd608176e4416247713b3c6ca34333d7fe` as the FIRST action of the
round, before anything was written. Both `.agent/` copies were made with `shutil.copyfile`, never
by retyping. No slice was edited, reflowed, rewrapped or corrected.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | |
| C0b mirror to `last_block.md` | done | |
| C1 PLAN9 → `.agent/plan.md` | done | byte-identical |
| C2 LEDGER9 + SLIPS9 appends | done | both growths exact |
| C3 step (1) `git rm` five files | done | 2254 / 1358 / 327 / 73 / 96 lines, all counts confirmed on disk first |
| C3 step (2) `review_cmd.py` | done | function + blank run + handler-table line; the FILE survives |
| C3 step (3) catalog entry | done | 14 lines, 4086–4099; group comment and `GroupDef` survive |
| C3 step (4) allowlist line | done | `apps.cli.commands.review_cmd` deliberately kept; file not re-sorted |
| C3 step (5) `CLUSTER_MODULES` line | done | |
| C3 step (6) the string-keyed doctor probe | done | the ONE surviving importer, R-0832 class |
| C3 step (7) retarget the fake `ImportError` | done | now `packages.orchestration.run_contract` |
| C3 step (8) the R-0841 sweep, three sites | done | `ui_server.py` comment, two test renames |
| C3 step (9) `pyproject.toml` two lines | done | |
| C3 step (10) runtime lane | done | array member gone, header rewritten to two lines, `NODE_ISOLATED_FILES=()` kept, `bash -n` exit 0 |
| C3 step (11) `_ALLOWED_LEGACY` line | done | |
| C3 step (12) two lane rosters | done | 2 occurrences in `test_test_categories.py`, 1 in `test_product_spine.py` |
| C3 step (13) 27 test functions | done | 27 removed across 16 files, counted by the script; 34 collected ids, confirmed at G7 |
| C3 step (14) 10 class headers | done | line-based, as ordered; all 24 edited `.py` files re-parsed with `ast` afterwards |
| C3 step (15) 10 import narrowings | done | each FROM counted exactly 1 in its own file first |
| C3 step (16) the docs | done | 10 edits across 7 pages |
| C3 step (17) regenerate the order file | done | shipped `measured_order()`, `+0/-1`, twelve → eleven |
| C4 the handback | done | this file |
| R-0841 | done | RESOLVED by the reviewer-authored `Done:` paragraph in LEDGER9; the worker wrote no resolution text of its own |
| R-0843 | done | registered by LEDGER9 |
| R-0844 | done | registered by LEDGER9 |
| G1 … G8 | done | all eight RUN, real exit codes above |

## Deviations & assumptions

No commit was added, dropped or reordered: the sequence on the branch is exactly C0a, C0b, C1,
C2, C3, C4 as the block fixes it, and C3 is ONE commit as operator RULE 1 requires. Every path
written is on the block's enumerated change-set list; the change set was never widened. Three
measured disagreements with the block's numerals follow — reported, not adjusted, per the block's
own instruction.

1. **THE CHANGE SET IS 46 ENUMERATED PATHS, NOT 45, AND G8's DIFF IS 45, NOT 44.** The block's
   `Change (45 paths…)` heading and G8's "EXACTLY the 44 paths of the change set other than
   `.agent/handoff.md`" are each ONE LOW. Counted mechanically from the committed
   `.agent/authored/f275-r9.md` by splitting the section on `·` and re-attaching each group
   prefix: **46 distinct paths** (7 under `.agent/`, 2 under `packages/orchestration/`, 3 under
   `apps/cli/`, 2 at root/`scripts/`, 9 under `docs/`, 3 under `tests/cli/`, 2 more under
   `tests/`, 18 under `tests/orchestration/`). Minus `.agent/handoff.md` that is **45**, and
   `git diff --name-only aae6d313..6c601b35` names **45** with an EXACT SET MATCH — no extra path
   and no missing one. So the ENUMERATION is right and only the two headline numerals are stale.
   Nothing on disk is wrong and no scope was widened; this is a reviewer-prose numeral, which
   AGENTS.md `prose_slips.md` rule 2 keeps out of the id space.

2. **THE CATALOG READS 334 AT C3 AGAINST 335 AT THE BASE, NOT 335 AGAINST 336.** G5(c) predicts
   `len(_BASE_CATALOG)` and `len(collect_all_handlers())` at 336 → 335; both measured 335 → 334.
   I measured the base figure in the primary checkout BEFORE C3, while its code tree was still
   byte-identical to `aae6d313`, with `python3 -B` and an explicit print of the five `review.*`
   ids, which listed `review.accept, review.bundle, review.list, review.reject, review.run` and
   reported zero duplicate `command_id`s — so the 335 is not a de-duplication artefact. THE DELTA
   IS EXACTLY THE PREDICTED −1 and every qualitative claim of G5(c) holds: `review.bundle` absent
   from both readers, all four survivors present in both. The same off-by-one figure appears
   inside the reviewer-authored R-0844 paragraph ("one of 336 catalog entries", "falls 336 to
   335"), which I applied BYTE FOR BYTE as constraint 1 orders rather than correcting; the
   committed ledger therefore carries a numeral that is one high, and a later round may want a
   `Done:`-side note or a `prose_slips.md` line for it. I raise no id: nothing under `packages/`,
   `apps/`, `tests/` or `docs/` is wrong, and the finding's substance — the command and the doctor
   row are gone with no inheritor — is correct as written.

3. **STEP (13) AS WORDED LEAVES THREE SINGLE-BLANK-LINE SEAMS.** Where the deleted function was
   the LAST member of its class, "delete the function whole, together with the blank run that
   follows it" consumes BOTH blank lines that separated the class from the next top-level
   construct, leaving one. Applied as written per constraint 1; I added nothing back. Measured
   over the 16 files of step (13), counting top-level constructs preceded by exactly one blank
   line: **16 at the base, 19 at C3** — three new, in `tests/orchestration/test_config.py`,
   `tests/orchestration/test_do_continue.py` and
   `tests/orchestration/test_token_economy_integration.py`. The base already carried 16 such
   seams in these same files, so this is a pre-existing shape rather than a new one, and ruff is
   clean over all 24 edited `.py` files (G6): ruff implements the pycodestyle blank-line rules
   `E301`–`E306` in preview only, and this repo's `select = ["E","F","W","I","UP"]` does not enable
   preview, so no configured rule reads this. Step (14) by contrast says "the blank run AROUND it"
   and produced no such seam. If the reviewer wants two blank lines restored, that is a one-line
   step in a later block; I did not take it on my own authority.

4. One assumption, stated because a gate rests on it: the base-side whole-suite `--collect-only`
   reading of 19751 was taken in the PRIMARY checkout before C3 rather than in a worktree, on the
   ground that C0a, C0b, C1 and C2 write only under `.agent/` and therefore leave the collected
   tree byte-identical to `aae6d313`. `git diff --name-only aae6d313..ea039fc8` names only
   `.agent/` paths, which is the check behind that. The base readings that COULD not be taken that
   way — the two deleted files, the 16 step-(13) files, and the base-side ruff count — were all
   taken in disposable worktrees under `.remedy-wt/`, never by mutating the primary checkout.

5. No `Done:` paragraph, `Landed:` line, verdict, finding or registration was authored by this
   worker. `Done: R-0841`, `- R-0843` and `- R-0844` are inside LEDGER9 and are the reviewer's
   text, applied byte for byte (block constraint 3).

## Next

The reviewer of session 5 gates F275 round 9 by re-running all eight gates itself against the
committed blobs over `aae6d313dbedc64c84703eae7a782e67439ccdec`..`<C4>`, reading `.agent/STOP`
from disk FIRST (Phase 1 rule 1 before rule 2), then the Open PR Gate. On PASS the next round
deletes the `dogfood_run` / `feature_planner` / `overnight_mission` / `progress_ledger` /
`repair_loop_v2` / `self_repair_proposal` component, which this round's regeneration has made the
FIRST body line of `.agent/f275_deletion_order.md`: its six modules import each other, so
DECISION F275 D2 makes the whole component ONE commit. That round also inherits R-0844's fix
clause pointer for DECISION F260 D3 and R-0843's clause binding the next block that touches
`docs/system/architecture.md`. The next free finding id is R-0845.

## Reviewer verdict on round 9 — appended after the handback, by the reviewer's authored text

VERDICT ROUND 9: **PASS.** Written by the planner/reviewer of session 5 AFTER reading the
committed range `aae6d313dbedc64c84703eae7a782e67439ccdec`..`1300bd3dd46977d766885862f9831597564df860`
and RE-RUNNING every one of the eight gates independently against the committed blobs; the
worker's report was not taken as evidence for any line below. It is carried here because under
`docs/agents/self_drive_protocol.md` a verdict that stays in the session is lost, and it is
booked into `.agent/live_review.md` by the FIRST substantive commit of the next round, per
amend0827-process-diet rule 1. It is NOT a `Done:` paragraph and resolves no finding.

WHAT THE REVIEWER RE-MEASURED. Six single-parent commits C0a `b3db8d01`, C0b `effecd77`,
C1 `2901e0b2`, C2 `ea039fc8`, C3 `6c601b35` and C4 `1300bd3d`, each parent verified by
`git rev-list --parents`, with per-commit insertions 400, 372, 19, 12, 11 and 365, every one
under the AGENTS.md DECISION F104 D1 cap of 500. G1: the reviewer's OWN scratchpad original and
the committed `.agent/authored/f275-r9.md` and `.agent/last_block.md` are all 36871 bytes at
`178bd6cae149517cab73a806385dd9bd608176e4416247713b3c6ca34333d7fe`, so this round has the
primary cmp-against-scratchpad proof of §4 item 9 rather than the digest fallback; per §3 item
37 that chain covers those three artefacts and claims nothing about the emitted bytes. G2:
`.agent/plan.md` byte-identical to PLAN9 at 2616 bytes and 45 lines. G3: `.agent/live_review.md`
552280 to 559516, growth 7236 = 1 + 7235; `.agent/prose_slips.md` 173925 to 175541, growth
1616 = 1 + 1615; both edges byte-exact with the joining byte read back as a newline, N counted
from each slice by the reviewer's own reader as 4 and 2 with ordered equality holding over the
WHOLE appended region, and both negative controls — flipped in memory on the FIRST appended
paragraph — REJECTED by both readers, the tracked files re-read from disk unchanged afterwards.
`^Gate: ` 30 to 31, and `^Gate: F275 R8 `, `^Done: R-0841 `, `^- R-0843 — ` and `^- R-0844 — `
exactly 1 each, with THE OPEN SET 68 TO 69 BY DISTINCT ID against registrations 71 to 73 and
resolutions 3 to 4. G4: all five deleted files absent from `git ls-tree` at C3 over 4632 tracked
files; all TEN gated strings at ZERO over the 1753 tracked files outside `.agent/` and `.data/`;
and the whole-word token `review_bundle` at EXACTLY FIVE lines, every one printed and every one
a must-not-touch item — `T2_F260.md` line 346 and `T2_F272.md` line 744, the specification, and
three lines in `packages/orchestration/self_repair_proposal.py`, a cluster module RULE 2 defers.
G5: the three ratchets 9 passed at exit 0, and through the SHIPPED readers `_BASE_CATALOG` and
`collect_all_handlers()` both fell 335 to 334 with `review.bundle` ABSENT from both, all four of
`review.run`, `review.list`, `review.accept` and `review.reject` PRESENT in both, the `review`
GroupDef still present and zero duplicate command ids; the regenerated order file holds ELEVEN
components against twelve at a `0  1` numstat, a PURE DELETION. THE RED-PROOF WAS RE-RUN BY THE
REVIEWER IN ITS OWN DISPOSABLE WORKTREE AT `6c601b35`: control exit 0 at 9 passed, then the
three restorations exit 1 at 2, 2 and 1 failures, then the control exit 0 again, each FROM
string counted unique in its named file first and each file reverted byte-identically by sha256.
G6: ruff `All checks passed!` over the 24 edited Python files still existing at C3, every one
re-parsed with `ast` without error, and repo-wide ruff `Found 24 errors.` at BOTH the base —
read in a disposable worktree, never by writing to the primary checkout — and the tip. G7: THE
FULL SUITE WAS RE-RUN BY THE REVIEWER SERIALLY IN THE PRIMARY CHECKOUT at exit code 0 read from
the process object, 19590 passed and 23 skipped, and the arithmetic closes exactly:
`--collect-only` 19751 at the base and 19613 at C3, a fall of 138 = 104 for the two deleted test
files plus 34 for the collected-id fall over the 16 swept files, and 19590 + 23 = 19613. G8:
`.agent/STOP` absent, `git status --porcelain` empty, one worktree, and the range's diff naming
45 paths in an EXACT SET MATCH against the block's enumeration minus `.agent/handoff.md`.

WHAT THIS ROUND ACHIEVED, AND THE SCOPE CORRECTION THAT IS ITS REAL CONTENT. The fourth module
group is gone, and it is the first whose ONLY surviving importer was invisible to every import
graph this repository owns: `apps/cli/commands/worker_facade_cmd.py` probed the module by STRING
through `importlib`, which is why `tests/orchestration/cluster_deletion_map.txt` carried no
`review_bundle` line and the module read as free. That is the R-0832 class reaching the deletion
map itself rather than a cockpit reader. THE SESSION-4 MAP FOR THIS ROUND WAS WRONG AND WAS
CAUGHT BY APPLYING IT. It prescribed deleting `apps/cli/commands/review_cmd.py` whole, the entire
`review` catalog group with its `GroupDef`, the smoke script's section 12ap, three surviving
command-string emitters and about eighteen further tests. Applied in a disposable worktree at
`aae6d313` BEFORE this block was authored, that reading measured RED at FIFTEEN failures, because
only ONE of the five handlers in that file imports `review_bundle` and the other four drive
`packages/orchestration/reviewer.py` — a module that SURVIVES, is not on F260's Design list, and
keeps a production importer at `apps/cli/commands/dev.py` line 125. The over-wide reading would
have deleted four working commands and the coverage of a surviving module. The correct scope runs
green: 2232 passed and ZERO failed over the affected suites, against fifteen failures at the
inherited scope. THE COUNTER-MEASURE, stated as a reading rather than a habit: a `*_cmd.py`
handler file belongs to a module group only for the handlers that IMPORT the module, and the
group's boundary is established by APPLYING the deletion, never by reading the file's name.

THREE DEVIATIONS WERE DECLARED AND ALL THREE ARE SUSTAINED; TWO ARE THE REVIEWER'S OWN NUMERALS
AND NEITHER EARNS AN ID. FIRST, the block's `Change (45 paths…)` heading and G8's "the 44 paths"
are each ONE LOW: the enumeration holds 46 distinct paths, 45 other than `.agent/handoff.md`, and
the reviewer re-counted them mechanically from the committed authored copy and confirmed an EXACT
SET MATCH against the 45-path diff. The enumeration — the half that gets executed — was right and
only the hand-counted heading drifted: the R-0510 class item 16 exists to prevent, arriving in the
very block that had to be trimmed to the 400-line cap. SECOND, the catalog readers are 335 at the
base and 334 at C3, not 336 and 335; the DELTA of −1 the gate exists to establish is exactly
right, and the reviewer confirmed 335 at the base by running the shipped readers in a disposable
worktree at `aae6d313`. The error was carrying round 8's PRE-deletion figure of 336 out of its
handback instead of re-measuring at this round's own base — the item 34 shape, a numeral taken
from prose rather than from the file. That same wrong pair sits inside the R-0844 paragraph this
round appended, which the worker applied BYTE FOR BYTE as constraint 1 required rather than
repairing reviewer text, so the ledger reads "one of 336 catalog entries" and "falls 336 to 335"
where the measured figures are 335 and 334. IT BUYS NO CORRECTION ROUND: the claim is not
load-bearing, because R-0844's substance is that `remedy review bundle` and the doctor row are
gone with no inheritor and that holds at either count, and AGENTS.md permits a correction round
only for a load-bearing false claim in the append-only record. THIRD, step (13) as worded took
both blank lines wherever the deleted function was its class's last member, leaving three
single-blank-line seams; the reviewer measured that these same files already carried sixteen such
seams at the base, ruff is clean because this repository's `select` does not enable the
preview-only `E301`–`E306` rules, and no test reads the shape. Cosmetic, sustained, no repair
round: step (14)'s "the blank run AROUND it" is the wording a later block should reuse.

## Session 5 ends here — ONE delegated round, reviewed and PASSED

`.agent/STOP` does not exist; it was measured absent at the Phase 0 probe, again before authoring
round 9, and again now. No pull request exists and none is owed: under
`docs/roadmap/STATUS_closure_protocol.md` the PR belongs to the closure sequence. F275's soft
limit is 20 sessions and 60 rounds by operator amendment amend0908-f275-finish RULE 1, and the
feature stands at session 5, round 9 — well inside it, so no scope report is owed.

THE REASON THIS SESSION ENDS AT ONE ROUND, STATED PLAINLY, AND IT IS THE SECOND SESSION IN A ROW
TO DO SO. This is a throughput problem and the reviewer names it rather than dressing it up. The
cause is not a nice seam: the next component cannot be split. `.agent/f275_deletion_order.md`
line 1 is a SIX-MODULE strongly connected component, and DECISION F275 D2 plus operator RULE 1
make it ONE commit; the components below it are all imported by it, so nothing smaller is
deletable. Its measured size is 7952 module lines across 46 tracked files, against
`review_bundle`'s 2254 across 40 — and this round proved that establishing such a group's true
boundary requires an APPLIED dry run with a full-suite run, because the boundary is exactly what
the inherited map got wrong. Authoring, delegating and then INDEPENDENTLY verifying a one-commit
deletion of that size does not fit beside the round already completed, and starting it without
the budget to verify it would leave an UNGATED round on the branch, which Phase 1 rule 4 forbids
planning over. That is amend0905-throughput's honest reason "a round that explicitly needs a
fresh session", and it is backed below by measurement rather than by estimate. Operator amendment
amend0908-f275-finish rule 5 is NOT cited: this session does not end on authoring errors
accumulating.

CONTEXT SELF-ASSESSMENT, as amend0905-throughput requires in one sentence: the session spent its
budget on two applied dry runs of the same round — the inherited over-wide scope, which it ran to
red before discarding, and then the corrected scope — plus three full-suite runs of about
twenty-four minutes each, and it ends with enough context to have MEASURED the next round's map
in full but not enough to author, delegate and independently verify a deletion of that size.

## THE ROUND 10 MAP — MEASURED at `1300bd3dd46977d766885862f9831597564df860`, not estimated

Everything below was read off the tree by running the shipped readers and an `ast` pass at the
tip named above. WHERE THE SESSION-4 MAP FOR ROUND 9 WENT WRONG WAS EXACTLY HERE — it assumed a
handler file dies with its module — so the FIRST fact recorded is the one that was assumed last
time, and it is measured this time.

HANDLER PURITY, THE FACT THAT DECIDES THE SCOPE. All five handler files of this component DO die
whole, unlike `review_cmd.py`. Measured by parsing each file's `COMMAND_HANDLERS` — note it is an
ANNOTATED assignment, so an `ast.Assign`-only reader silently finds nothing — and resolving every
`from packages.orchestration.X import` in it:

| Handler file | lines | commands | orchestration imports beyond shared utils |
|---|---|---|---|
| `apps/cli/commands/dogfood_cmd.py` | 281 | 12 | NONE |
| `apps/cli/commands/overnight_mission_cmd.py` | 156 | 7 | NONE |
| `apps/cli/commands/progress_cmd.py` | 57 | 1 | NONE (`storage` only, a shared utility) |
| `apps/cli/commands/repair_loop_v2_cmd.py` | 187 | 11 | NONE |
| `apps/cli/commands/self_repair_cmd.py` | 213 | 7 | NONE |

THIRTY-EIGHT COMMANDS DIE, and the catalog goes 334 to 296. All 38 ids were confirmed present in
the live `_BASE_CATALOG`. By group, and this is the half a `review_bundle`-style sweep cannot see:

- `dogfood` — catalog has 12, all 12 die: THE WHOLE GROUP GOES, `GroupDef` included.
- `progress` — catalog has 1, it dies: THE WHOLE GROUP GOES, `GroupDef` included.
- `self-repair` — catalog has 7, all 7 die: THE WHOLE GROUP GOES, `GroupDef` included.
- `overnight` — catalog has 11 and only 7 die. THE GROUP AND ITS `GroupDef` SURVIVE, keeping
  `overnight.plan`, `overnight.readiness`, `overnight.report` and `overnight.run`.
- `repair` — catalog has 17 and only 11 die. THE GROUP AND ITS `GroupDef` SURVIVE, keeping
  `repair.failure-show`, `repair.propose`, `repair.request`, `repair.request-show`,
  `repair.start` and `repair.status`.

`tests/test_command_catalog.py::TestCatalogIntegrity::test_every_group_has_at_least_one_command`
is what catches a `GroupDef` left behind, and it reads the catalog rather than any module, so no
grep for the six module names can see it.

THE CARRY-OVER COLLIDES WITH THIS ROUND AND MUST BE SETTLED BEFORE IT. `overnight.readiness` and
`overnight.report` are two of the four `overnight` survivors, and they are precisely F260's Design
"two carry-overs before deletion" — overnight readiness and the overnight report become
`mission readiness` and `mission report`, with DECISION F274 D2 ruling that `mission report` is
NOT FREE UNTIL ITS CURRENT HOLDER DIES. Their handler is NOT `overnight_mission_cmd.py`, which
dies here. T001's "WHAT IS OWED HERE, IN ORDER" puts both carry-overs BEFORE the first `git rm`,
and neither has landed. The next session must therefore decide, and record as a DECISION, whether
the carry-over rides in this component's commit or precedes it — that ordering question is the
first thing the round 10 block has to answer, and it is not answered here.

THE SIX MODULES AND THEIR OWN TESTS: `dogfood_run.py` 1725, `progress_ledger.py` 2284,
`repair_loop_v2.py` 1167, `feature_planner.py` 1045, `overnight_mission.py` 918 and
`self_repair_proposal.py` 813 — 7952 lines. Their own suites are
`tests/orchestration/test_dogfood_run.py`, `test_feature_planner.py`, `test_overnight_mission.py`,
`test_progress_ledger.py`, `test_repair_loop_v2.py`, `test_self_repair_proposal.py` and
`tests/cli/test_self_repair_cmd.py`.

THE SURVIVING CONSUMER, and there is exactly one under `apps/` or `packages/`:
`apps/cli/commands/worker_facade_cmd.py` names BOTH `dogfood_run` and `self_repair_proposal`.
Round 9 already removed its `review_bundle` probe; these two are STRING-keyed `importlib` probes
of the same shape, so the same class applies and `tests/cli/test_worker_facade_cmd.py` names
`dogfood_run` too. `tests/orchestration/cluster_deletion_map.txt` carries exactly one edge for
this component, `packages.orchestration.dogfood_run <- apps/cli/commands/worker_facade_cmd.py`,
which goes in the same commit.

THE FOURTEEN OTHER TEST FILES that name a dying module and whose subject SURVIVES need the round 9
treatment — an AST sweep classified by hand, not applied blind: `test_builder_routing.py`,
`test_development_artifact_boundary.py`, `test_do_continue.py`, `test_local_model_advisor.py`,
`test_model_route_tournament_integration.py`, `test_overnight_mission_integration.py`,
`test_progress_redaction.py`, `test_real_test_execution.py`, `test_token_economy_integration.py`,
`test_worker_route_integration.py`, `test_cluster_deletion_map.py`,
`tests/orchestration/import_reachability_allowlist.txt` (six lines) and
`tests/cli/test_worker_facade_cmd.py`. Round 9's lesson applies in full: some of these reference a
SURVIVING artefact that merely shares a name, and deleting the test destroys real coverage —
five tests were spared on exactly that ground last round.

THE DOCS: two pages have a dying module as their SUBJECT and go whole, with their `docs/README.md`
index rows — `docs/system/open-ended-dogfood-run-orchestrator-replay-analyzer-v0.md` and
`docs/system/token-aware-repair-loop-v1-v2.md`. Line-level edits are owed in
`development-artifact-boundary-v0.md`, `run-contract-v1.md`, `snapshot-rollback-v1.md`,
`real-test-execution-snapshot-rollback-proof-v1.md` and `docs/system/vocabulary.md` — that last
one is F259's binding concept model and is edited with care. `pyproject.toml` names three of the
six. MUST NOT BE TOUCHED: `docs/roadmap/features/T1_F034.md`, `T2_F260.md`, `T2_F269.md`,
`T2_F272.md` and `T2_F277.md`, which are the specification and other features' plans.

A WARNING ABOUT THE BLOCK ITSELF. Round 9's block landed at EXACTLY the 400-line cap of §3 item 1
for a 40-path change set, and this round's is larger in every dimension while operator RULE 1
still forbids splitting the commit. The cap binds the BLOCK, not the commit, so the next session
should plan the block as a SPEC plus a per-file roster rather than a per-line FROM/TO enumeration,
and should expect to spend a constraint on that choice.

## What the next session owes, in order

FIRST, Phase 1 rule 1: re-read `.agent/STOP` from disk before the Open PR Gate. It does not exist
as this session ends. Then the Open PR Gate: no PR is open.

SECOND, the next round's FIRST substantive commit books, from this file as the durable carrier:
the ROUND 9 PASS verdict above as a `Gate: F275 R9` entry in `.agent/live_review.md`, and TWO
dated `.agent/prose_slips.md` lines — one for the round 9 block's path-count heading being 45
over a body of 46 and G8's 44 over 45, and one for the catalog numerals 336 and 335 that landed
inside the R-0844 registration where the measured figures are 335 and 334. No id is spent on
either, per amend0827-process-diet rule 2, and neither buys a correction round.
`.agent/plan.md` is advanced in that same commit, per §3 item 23. The next free id is R-0845.

THIRD, settle the carry-over ordering question named above as a dated DECISION, then the work:
the six-module component, whole, in ONE commit, using the map above and re-running its own
applied dry run before authoring. Plan the session around ONE round and do not start the commit
without the budget to verify it.
