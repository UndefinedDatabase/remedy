# Handback — F275 round 15

## Session

SESSION 9 of feature F275 · round 15 · rounds so far 15

F275's soft limit is 20 sessions and 60 rounds by operator amendment
amend0908-f275-finish rule 1, and it travels to no other feature. This round is
well inside it, so no scope report is owed.

## Range

Review of `fadf4715`..`HEAD`

## Commits

### d68fa6d2 F275 R15 C0a: save the authored round 15 block.
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f275-r15.md | +433 / -0 | The delegation source copied byte for byte with `shutil.copyfile`, never retyped. |

### 74b90eab F275 R15 C0b: mirror the round 15 block into the last-block state file.
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +408 / -357 | The same bytes mirrored; a single `.agent/**` state-file rewrite. |

### b98dcf29 F275 R15 C1: advance the plan to round 15.
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +20 / -20 | Replaced WHOLE by the PLAN15 slice extracted from the committed C0a blob. |

### a33a93a6 F275 R15 C2: book the round 14 PASS and its slip, record DECISION F275 D7, register R-0855 through R-0858.
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +10 / -0 | LEDGER15 appended: the round 14 PASS and the four registrations. |
| .agent/decisions.md | +14 / -0 | DECISION15 appended: DECISION F275 D7 on the approval gate. |
| .agent/prose_slips.md | +2 / -0 | SLIPS15 appended: the round 14 control-selection slip. |

### 8124377d F275 R15 C3: sweep the dead survivor state round 14's deletion left behind.
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/orchestrator_cmd.py | +0 / -3 | The `advisor` branch that can never fire since round 14 removed the key. |
| packages/orchestration/orchestrator_brain.py | +0 / -13 | The orphaned advisor banner block and `_CONFIDENCE_ORDER`, whose only reader round 14 deleted. |
| tests/orchestration/test_cluster_deletion_map.py | +3 / -1 | The `CLUSTER_MODULES` comment restated to carry NO count, per §3 item 16. |

### 795e4080 F275 R15 C4: delete the managed builder execution module group and repair the survivors.
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/managed_builder_execution.py | +0 / -1694 | The module, whole. |
| apps/cli/commands/managed_builder_execution_cmd.py | +0 / -350 | Its handler file, whole. |
| tests/orchestration/test_managed_builder_execution.py | +0 / -1793 | Its unit tests, whole. |
| tests/cli/test_managed_builder_execution_cli.py | +0 / -95 | Its CLI tests, whole. |
| docs/system/managed-external-builder-execution-v1.md | +0 / -177 | A page whose whole subject this commit deletes. |
| docs/system/managed-external-builder-execution-v1-1-hardening.md | +0 / -88 | Likewise. |
| docs/guides/managed-external-builder-execution-user-guide-v1.md | +0 / -79 | Likewise; documents `execution template-*`. |
| docs/system/controlled-claude-code-operator-path-v0.md | +0 / -146 | Likewise; nearly every numbered step is an `execution` command. |
| apps/cli/command_catalog.py | +0 / -196 | The `execution` `GroupDef` and the section span holding SEVENTEEN `CommandEntry` records. |
| packages/orchestration/run_contract.py | +0 / -34 | Fourteen `EXECUTION_*` members, their fourteen `_DEFAULT_ALLOWED_ACTIONS` rows and three comments. `SELF_EXECUTION_STATUS` survives. |
| apps/cli/commands/__init__.py | +1 / -2 | The handler out of the import block and the `for mod in (…)` tuple. |
| apps/cli/commands/worker_facade_cmd.py | +3 / -54 | The template half of `worker doctor`, `worker add` and `worker disable`. The adapter half survives. |
| packages/orchestration/exec_guard.py | +24 / -21 | Seven prose citations of the dying module; the rlimit reason moves in and is stated ONCE. No behaviour change. |
| tests/cli/test_worker_facade_cmd.py | +7 / -33 | Template patches and assertions dropped; two tests renamed to the half they now exercise. |
| tests/cli/test_cli_ux.py | +1 / -1 | `"execution"` out of `_INTERNAL_GROUPS`. |
| tests/orchestration/test_development_artifact_boundary.py | +0 / -8 | `_PRODUCT_MODULES` entry, one whole test method, one tuple entry. |
| tests/cli/test_product_spine.py | +0 / -5 | `test_no_stale_adapter_flag_in_operator_path`, whose page this commit deletes. |
| tests/orchestration/test_cluster_deletion_map.py | +0 / -2 | The `CLUSTER_MODULES` and `CLUSTER_COMMAND_HANDLERS` entries. |
| tests/test_test_categories.py | +0 / -1 | The deleted test file's row. |
| tests/orchestration/import_reachability_allowlist.txt | +0 / -2 | Module and handler. |
| tests/orchestration/cluster_deletion_map.txt | +0 / -1 | The module's one recorded edge. |
| pyproject.toml | +0 / -1 | The handler module out of packaging. |
| scripts/remedy_test_fast.sh | +0 / -1 | The deleted test file out of the fast lane. |
| .agent/f275_deletion_order.md | +1 / -2 | REGENERATED from `measured_order()`: six components to five AND a reorder. |
| docs/README.md | +0 / -5 | The rows linking the four deleted pages, matched on the LINK TARGET. |
| docs/system/core-product-spine-v0.md | +0 / -1 | The `execution approve/run/show` table row. |
| docs/system/mission-run-loop-morning-report-v0.md | +0 / -2 | The operator-path link and the managed-execution approval bullet. |
| docs/system/development-artifact-boundary-v0.md | +2 / -4 | The module bullet, the `Execution status` row, and the guard-test sentence that still cited a file round 12 deleted. |
| docs/system/test-lanes-v0.md | +0 / -1 | The deleted test file's lane row. |
| docs/guides/simple-operator-quickstart-v0.md | +3 / -3 | Three cells lose their `execution template-*` half and keep the `builder adapter-*` half. |

### C5 — the handback (self-reference)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | (this commit) | Rewritten WHOLE. A handoff cannot table the commit that writes it (R-0149 pattern). |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/r15base fadf4715` | created; used for the G5 base end, the G7 (b) base ruff and the G7 (f) base collection |
| `git worktree remove --force .remedy-wt/r15base` | removed |
| `git worktree add --detach .remedy-wt/r15c4 795e4080` | created; the ONE disposable worktree of the four G6 red-proofs |
| `git worktree remove --force .remedy-wt/r15c4` | removed |
| `git worktree prune` | clean; `git worktree list` names the primary checkout ALONE |
| `git push` | ONCE, after C5 — see below |

No PR was created, edited or merged.

## Verification

ONE LINE PER GATE, with its REAL exit code.

- **G1 TRANSPORT** — exit 0. The delegation source, the committed
  `.agent/authored/f275-r15.md` at C0a and the committed `.agent/last_block.md`
  at C0b are all 48472 bytes at
  `bbb87d8b66a18521c37f6214526202700667be0174b9b3a543df3442216eb0e4`; one digest
  comparison, all three BYTE-EQUAL.
- **G2 THE PLAN AND THE BLOCK** — exit 0. `.agent/plan.md` at C1 is 2588 bytes at
  `5a43749f…`, BYTE-IDENTICAL to the PLAN15 slice extracted from the committed
  C0a blob between its markers; **45 lines** against the cap of 50 (the block
  says 44 — declared below); `## Goal` and `## Next Steps` both present. C0a blob
  TOTAL 433 lines, slice bodies 68, **PROSE 365**.
- **G3 THE RECORD** — exit 0, over three appends. (a) BYTE READER:
  live_review 618783→634559 growth 15776 = 1 + 15775; prose_slips
  184231→185058 growth 827 = 1 + 826; decisions 966757→970963 growth 4206 =
  1 + 4205; in each the pre-blob is a byte-exact PREFIX, the slice a byte-exact
  SUFFIX, and the joining byte read back out of the post-blob is `b'\n'`.
  (b) STRUCTURAL READER: N COUNTED from each slice as **5, 1 and 7**; the last N
  blank-line units of each post-file equal the slice's N paragraphs IN ORDER,
  per-unit sha256 printed on both sides, all equal. (c) NEGATIVE CONTROL: one
  byte flipped in memory inside the FIRST appended paragraph of each file at
  offsets 621411, 184644 and 966849 — reader (a) and reader (b) BOTH accepted the
  truth and BOTH rejected the mutant, all three files; re-read from disk
  afterwards and byte-equal to their committed post-blobs. (d) COUNT PATTERNS:
  `^Gate: ` 36 → 37, a rise of exactly 1; `^Gate: F275 R14 `, `^- R-0855 — `,
  `^- R-0856 — `, `^- R-0857 — `, `^- R-0858 — ` and `^## DECISION F275 D7 `
  exactly 1 each. (e) THE OPEN SET BY DISTINCT ID, `Landed:` never subtracted:
  **83 / 4 / 79 before → 87 / 4 / 83 after**; the base reading matches the
  reviewer's 83 / 4 / 79 exactly; newly registered R-0855, R-0856, R-0857, R-0858.
- **G4 THE DELETION IS COMPLETE** — exit 0. `git ls-tree -r 795e4080` holds none
  of the eight whole-file removal paths; **4567 tracked files**. The 35-token
  sweep (seventeen of them `execution.<sub>` ids) over the **1682** tracked files
  outside `.agent/` and `.data/` read **RAW 10** lines, printed IN FULL, and
  **STRIPPED 4** after deleting every backtick-quoted span — exactly the
  reviewer's numbers. The stripped four are `T2_F262.md` twice, `T2_F267.md`
  once, and the DECLARED false positive at
  `tests/cli/test_real_test_execution_cli.py:79`, where `execution.list` matches
  inside `real_test_execution.list_test_runs`. **No undeclared line falls outside
  `docs/roadmap/features/`.**
- **G5 THE SHIPPED READERS AND THE ORDER FILE** — exit 0 at both ends, read BY
  IMPORT with `sys.path` pinned and the resolved `__file__` PRINTED FIRST.
  `len(_BASE_CATALOG)` **267 → 250**, `len(collect_all_handlers())` **267 → 250**,
  `len(GROUPS)` **49 → 48**, `len(ALL_KNOWN_ACTIONS)` **120 → 106**, duplicate ids
  **0 at both ends** — every figure the reviewer predicted. `execution` ABSENT
  from `GROUPS` at C4 and all seventeen `execution.` ids ABSENT from BOTH readers
  (17 present in both at the base). `patch.approve`, `do.continue`,
  `worker.doctor`, `worker.add`, `worker.disable`, `mission.run`, `doctor.core`
  and `builder.adapter-show` all PRESENT in both readers at C4. Order file: **six
  components → five**, its 26 header lines byte-identical at both ends at sha256
  `aff913e6eedb4d9c7e5ab6e76578be881ffffa3612018cf58b5a48ad508b0cc2`, EQUAL to a
  fresh regeneration from the live import graph at both ends, and the REORDER is
  visible — `main_builder_adapter` moved from position four to position **one**.
- **G6 THE RED-PROOFS** — exit 0, four probes in ONE disposable worktree at C4,
  `__pycache__` purged before EVERY run, `python3 -B`, each control run over the
  probe's OWN selection in the SAME script immediately before its mutation.
  **A** control exit 0 at 3 passed → mutant exit 1 at 1 failed.
  **B** control exit 0 at 3 passed → mutant exit 1 at 1 failed.
  **C** control exit 0 at 3 passed → mutant exit 1 at 2 failed.
  **D** control exit 0 at 51 passed → mutant exit 1 at 2 failed.
  Every one matches the reviewer's own run. Every target restored by
  `git checkout --` and proved byte-identical by sha256 before and after; the
  worktree porcelain was EMPTY at the end.
- **G7 RUFF, THE RATCHETS AND THE FULL SUITE** — (a) `python3 -m ruff check` over
  the thirteen edited `.py` files still existing at C4: `All checks passed!`,
  exit **0**. (b) `python3 -m ruff check .` repo-wide: real exit **1 at both
  ends** by design, **26 diagnostics at both ends**, and the two diagnostic SETS
  compared ITEM BY ITEM are IDENTICAL — nothing in BASE only, nothing in C4 only.
  (c) the ratchet batch (`test_import_reachability`, `test_cluster_deletion_map`,
  `test_cluster_deletion_order`, `tests/docs/`, `test_advertised_commands`,
  `test_cli_ux`, `test_product_spine`, `test_grouped_cli`): **870 passed**, exit
  **0**. (d) the canary `tests/cli/test_golden_path.py`: **42 passed**, exit
  **0**. (e) THE FULL SUITE, `python3 -B -m pytest tests/ -q`, SERIALLY, in the
  PRIMARY checkout with C4 COMMITTED: **18689 passed, 23 skipped, ZERO failed**,
  exit **0**, in 21m31s — and 18689 + 23 = **18712**, equal to the C4 collection.
  (f) THE ARITHMETIC BY THE ID SET, both sides collected in the same environment:
  base **18867**, C4 **18712**, **157 LOST** and **2 GAINED**, and
  18867 − 157 + 2 = 18712. LOST per-file attribution: 133
  `tests/orchestration/test_managed_builder_execution.py`, 12
  `tests/cli/test_managed_builder_execution_cli.py`, 8
  `tests/test_grouped_cli.py`, 2 `tests/cli/test_worker_facade_cmd.py`, 1
  `tests/cli/test_product_spine.py`, 1
  `tests/orchestration/test_development_artifact_boundary.py`. The GAINED set is
  exactly the two renames C4 orders —
  `TestWorkerAdd::test_add_enables_adapter` and
  `TestWorkerDisable::test_disable_adapter`. Every figure matches the reviewer's.
- **G8 THE TREE** — exit 0. `.agent/STOP` re-read from disk and ABSENT.
  `git status --porcelain` EMPTY. `git worktree list` names the primary checkout
  ALONE. Branch `feature/f275-one-world-completion-part-three`, correct.
  `git diff --name-only a33a93a6..8124377d` against the block's three C3 paths:
  MISSING set EMPTY, EXTRA set EMPTY. `git diff --name-only 8124377d..795e4080`
  against the block's thirty C4 paths: MISSING set EMPTY, EXTRA set EMPTY.
  Every commit before C5 has ONE parent and is under the DECISION F104 D1 cap of
  500 insertions: C0a 433, C0b 408, C1 20, C2 26, C3 3, C4 42.

## Authored-text proofs

| Slice | Target | Result |
|---|---|---|
| PLAN15 | `.agent/plan.md` @ C1 | BYTE-IDENTICAL to the slice extracted from the committed C0a blob — 2588 bytes, sha256 `5a43749fd4b5ae0ec55c22c20e560912dfefef16dd4858b9f3a2c28ce01d5d7f` on both sides. |
| LEDGER15 | `.agent/live_review.md` @ C2 | Byte-exact SUFFIX of the post-blob; 15775 bytes, sha256 `43cd2b51bf038c5c7fe94a2ec54c510172b31900ee91e68edf453cc5789fc922`; five units matched IN ORDER by per-unit sha256. |
| SLIPS15 | `.agent/prose_slips.md` @ C2 | Byte-exact SUFFIX; 826 bytes, sha256 `389d57fc7fb2c71d9e8f5d699426a80bdba9e72b506be750527b3ec88fca8e42`; one unit matched. |
| DECISION15 | `.agent/decisions.md` @ C2 | Byte-exact SUFFIX; 4205 bytes, sha256 `df358855f36511ffdd7031c929e418bd4eac9370bf2dba3b70ba2eccd3d9c265`; seven units matched IN ORDER. |

Every slice was applied BYTE FOR BYTE from the COMMITTED C0a blob and never
retyped. No slice was edited.

## Deviations & assumptions

Seven, all declared rather than repaired. No block order was disobeyed.

1. **The slice's trailing newline — the block's constraint 3 does not describe
   this repository's slice convention, and the convention was followed.**
   Constraint 3 states "the slice carries no trailing newline of its own". As
   measured, every one of the four slices DOES carry the newline that terminates
   its last body line. The convention was not assumed: it was PROVED against
   round 14 before any byte was written. With the trailing newline INCLUDED, the
   PLAN14 slice of the committed block `ed9a78b0` is 2720 bytes and equals the
   committed `.agent/plan.md` at `11b4dff7` byte for byte, and
   `post == pre + b"\n" + LEDGER14` holds exactly over `.agent/live_review.md`
   (608189 → 618783, growth 10594 = 1 + 10593). With it EXCLUDED, neither holds.
   The inclusive reading was therefore applied, and the growth arithmetic
   constraint 3 and G3 (a) actually order — `growth == 1 + len(slice)` — is
   satisfied exactly on all three files. The exclusive reading would also have
   left all three record files without a terminating newline, which no round of
   this feature has done.
2. **PLAN15 is 45 lines, not the 44 constraint 4 asserts.** Measured on the
   FINAL committed bytes: 2588 bytes, 45 lines. It is under the AGENTS.md cap of
   50 either way and carries both mandated headings, so nothing on disk is wrong;
   the numeral in the block's prose is.
3. **`packages/orchestration/exec_guard.py` is +24 / −21, not the +24 / −19 the
   change set predicts.** The insertions match exactly. The two extra deletions
   are the natural consequence of the ordered edits: the deferral sentences in
   `dod_process_exec_policy`, `dod_app_exec_policy`, `runtime_build_exec_policy`
   and `runtime_server_exec_policy` each occupied three lines and the citation of
   `:func:`test_command_exec_policy`` that replaces them fits in two or three. No
   ordered edit was skipped and none was added: all SEVEN citations of
   `managed_builder_execution` are gone, and `grep -c` over the file reads 0.
   Every hunk lies inside a docstring or a `#:` comment; the four
   `ExecGuardPolicy` constructions are untouched, so no behaviour changed.
4. **`apps/cli/command_catalog.py` is 0 / −196, not the 0 / −197 the change set
   predicts.** Counted from the span as the block orders rather than from its
   list: the section runs from the `# ── execution ─` comment through the last
   `CommandEntry` whose `group_id="execution"` and the blank line that separates
   it from the `# ── brain ─` section — **195 lines** — and it holds **SEVENTEEN**
   `CommandEntry` records, which is the number the block asked me to count and
   report. With the `"execution": GroupDef(…)` line that is 196. Deleting one
   line fewer would have left two consecutive blank lines before the `brain`
   section.
5. **C4's total is +42 / −4802, not the +42 / −4801 the header predicts.** The
   insertions match exactly. The deletion delta is precisely deviations 3 and 4
   combined (+2 from `exec_guard.py`, −1 from `command_catalog.py`), so the three
   readings are internally consistent.
6. **G5's `ALL_KNOWN_ACTIONS` — a reader correction inside this round.** My first
   probe read `_DEFAULT_ALLOWED_ACTIONS` and measured 110 → 96. That is not the
   symbol the gate names. `run_contract.py` defines a shipped
   `ALL_KNOWN_ACTIONS: frozenset[str]` derived from every `ContractAction`
   member; read by import, it is **120 → 106**, which is the reviewer's figure.
   Both readings are reported above; the gate is answered by the named symbol.
7. **The C3 comment on `CLUSTER_MODULES` is worker-authored to a SPEC, not
   applied from a slice.** The block orders "a comment that states NO count" at
   3 insertions and ships no marker-delimited text for it, so the three lines are
   mine, written to that spec. They state no numeral of any kind.

No departure from the block's ordered commit sequence: six commits, C0a, C0b, C1,
C2, C3, C4, C5, in exactly that order, none added, none dropped, none reordered.

The block's own numerals were otherwise reproduced exactly, including every G5
catalog figure, the G4 RAW 10 / STRIPPED 4 split, all eight G6 probe readings,
the G7 (b) 26 diagnostics, the G7 (e) 18689 / 23 / 0 and the G7 (f) 157 lost /
2 gained.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |
| R-0855 | done | registered at C2 and swept at C3 — see the `Landed:` line below |
| R-0856 | done | registered at C2; a capability-loss record, resolved by DECISION F260 D3 |
| R-0857 | done | registered at C2; resolved by the round that deletes `main_builder_adapter` |
| R-0858 | done | registered at C2; repair deliberately deferred, not performed here |

Landed: R-0855 — the three dead survivor artefacts round 14's anchors left in `orchestrator_cmd.py`, `orchestrator_brain.py` and `test_cluster_deletion_map.py` are deleted at C3.

## Open findings

**83 by distinct id** at C2 (79 at the base `fadf4715`, plus R-0855 through
R-0858), against 87 registered and 4 resolved. `Landed:` lines are never
subtracted. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's rather
than this feature's, per DECISION F272 D12.

## Next

The planner and reviewer re-runs all eight gates itself against the COMMITTED
blobs over `fadf4715`..`HEAD` and issues the round 15 verdict. Phase 1 rule 1
first: re-read `.agent/STOP` from disk before authoring anything.
