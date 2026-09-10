# Handback — F275 round 22

## Session

SESSION 12 of feature F275 · round 22 · rounds so far 22

F275's soft limit is 20 sessions and 60 rounds by operator amendment
amend0908-f275-finish rule 1, and it travels to no other feature. Round 22 of
session 12 is inside both, so no scope report is owed.

**T001's module list is now EMPTY.** This round deleted the last component of
`.agent/f275_deletion_order.md` — the strongly connected pair
`packages.orchestration.provider_trust` and
`packages.orchestration.provider_trust_verification` — with
`apps/cli/commands/provider_cmd.py`, the whole `provider` command group (five ids),
six `ContractAction` members, four whole test files and two documentation pages.
`CLUSTER_MODULES` is the empty tuple and `cluster_deletion_map.txt` carries no edge
lines.

Context self-assessment: comfortable. The round was one large deletion plus prose
work; nothing about the context suggests a boundary is needed.

## Range

Review of `5178df03`..`0242c0a3`, plus the C5 commit that writes this file. Its SHA is
not stated here because a handoff cannot measure the commit that carries it, and an
unmeasured SHA is worse than none; `git log --oneline -1` names it.

## Commits

### 05cdebe2 F275 R22 C0a: save the round 22 step block.
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f275-r22.md | +490/-0 | the block copied verbatim with `shutil.copyfile` |

### f1d77cac F275 R22 C0b: mirror the round 22 step block.
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +419/-418 | the same bytes taken from the COMMITTED C0a blob via `git show` |

### 80268fd0 F275 R22 C1: the round 22 plan.
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +20/-24 | whole-file replacement by the PLAN22 slice |

### c9b439b3 F275 R22 C2: book the round 21 PASS verdict, register R-0866, R-0867 and R-0868, record three prose slips.
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +10/-0 | LEDGER22 appended (the R21 `Gate:` record, three registrations, one `Note:`) |
| .agent/prose_slips.md | +4/-0 | SLIPS22 appended (three reviewer slips of round 21) |

### 6992661a F275 R22 C3: rule DECISION F275 D11 - the three survivors of the Provider Trust Gate degrade.
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +66/-0 | DECISION22 appended; this commit PRECEDES the first `git rm` |

### 0242c0a3 F275 R22 C4: delete the provider trust pair, its handler and the whole provider command group, and degrade the three survivors.
| Path | +/- | Reason |
|---|---|---|
| .agent/f275_deletion_order.md | +0/-1 | the last component line; the 26-line header is byte-identical |
| apps/cli/command_catalog.py | +3/-97 | the `provider` GroupDef, the whole provider section (5 ids), the ORPHANED overnight-mission section comment, and three repaired `related=` tuples |
| apps/cli/commands/\_\_init\_\_.py | +1/-2 | `provider_cmd` out of the sorted import block and the dispatcher tuple |
| apps/cli/commands/provider_cmd.py | +0/-170 | DIES WHOLE |
| apps/cli/commands/repair_cmd.py | +0/-1 | the `output_intake_command` print line |
| docs/README.md | +0/-4 | four index rows (quick-find + system table, two pages each) |
| docs/archive/candidate-generator-adapter-future.md | +6/-6 | the See-also link, the intake pipeline and the two deleted ContractActions |
| docs/system/orchestrator-brain-v0.md | +10/-11 | trust signals, loop-guard list, anti-loop paragraph, Future bullet, two See-also links |
| docs/system/provider-patch-materialization-v0.md | +11/-9 | the inline first-sentence link, two See-also links, and two dead command advertisements |
| docs/system/provider-trust-gate-v0.md | +0/-97 | DIES WHOLE |
| docs/system/provider-trust-verification-v1.md | +0/-132 | DIES WHOLE |
| docs/system/quality-baseline-v0.md | +0/-1 | the coverage row for the deleted handler |
| docs/system/repair-request-builder-v0.md | +8/-9 | two See-also links plus the "Re-entry is mandatory" section, now a deliberate absence |
| docs/system/self-dogfood-execution-v0.md | +29/-11 | Flow block, re-entry rule, States paragraph, See-also — the deliberate absence naming R-0866 |
| packages/orchestration/orchestrator_brain.py | +5/-82 | two `OptionKind` members, two `_BASE_SCORE` entries, two sig defaults, two try-blocks, three option blocks, two fingerprint fields, the `trust_rejected` loop-guard branch, the narrowed `needs_candidate` and its reason string |
| packages/orchestration/provider_patch_material.py | +15/-24 | the top-level import block, the two local imports and the `paths_safe` / `trust_report_accepted` checks; deliberate absence naming R-0867 |
| packages/orchestration/provider_trust.py | +0/-1058 | DIES WHOLE |
| packages/orchestration/provider_trust_verification.py | +0/-1020 | DIES WHOLE |
| packages/orchestration/repair_request_builder.py | +17/-34 | five advertisements, the two REMOVED result fields on both dataclasses and both `to_dict` bodies |
| packages/orchestration/run_contract.py | +0/-19 | six `ContractAction` members, two comment blocks, six safe-action tuple lines |
| packages/orchestration/self_dogfood.py | +0/-16 | the trust-accepted-not-materialized try-block and a roadmap rule that could never fire again |
| packages/orchestration/self_dogfood_execution.py | +23/-42 | the candidate-linking block, `_self_provider_label`, two next-safe-action strings, two docstrings, one falsified request-text sentence |
| pyproject.toml | +0/-1 | the `per-file-ignores` entry for a file that no longer exists |
| tests/cli/test_provider_material_cli.py | +0/-125 | DIES WHOLE |
| tests/cli/test_provider_trust_cli.py | +0/-136 | DIES WHOLE |
| tests/cli/test_provider_verification_cli.py | +0/-118 | DIES WHOLE |
| tests/cli/test_repair_request_cli.py | +6/-3 | the JSON-shape assertion (fields ABSENT) and the TEXT-surface assertion |
| tests/cli/test_self_dogfood_execution_cli.py | +1/-1 | the one `next_safe_action` assertion |
| tests/orchestration/cluster_deletion_map.txt | +0/-5 | REGENERATED from the live import graph; header kept, no edge lines |
| tests/orchestration/import_reachability_allowlist.txt | +0/-3 | exactly three entries |
| tests/orchestration/test_cluster_deletion_map.py | +1/-4 | `CLUSTER_MODULES` becomes the annotated EMPTY tuple |
| tests/orchestration/test_provider_patch_material.py | +9/-182 | three test classes, one guard, the `env` fixture and the `_job`/`_intake`/`_md_diff` helpers |
| tests/orchestration/test_provider_trust.py | +0/-348 | DIES WHOLE |
| tests/orchestration/test_provider_trust_verification.py | +0/-359 | DIES WHOLE |
| tests/orchestration/test_repair_request_builder.py | +18/-72 | the simulated end-to-end section and the strengthened catalog guard |
| tests/orchestration/test_self_dogfood_execution.py | +20/-81 | two tests deleted, two re-pinned, one strengthened |

### C5 (SHA unmeasurable here) F275 R22 C5: the round 22 handback.
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | whole-file rewrite | a handoff cannot table the commit that writes it (R-0149 pattern) |

Every `+/-` cell above was compared CELL BY CELL against `git show --numstat` for its
commit. THEY ALL AGREE — the table is transcribed from that output, not from memory.

## External actions

| Command | Outcome |
|---|---|
| `git worktree add -q .remedy-wt/f275r22-wt-g5 HEAD` | created, used for the G5 mutation red-proof |
| `git worktree add -q --detach .remedy-wt/f275r22-wt-base 5178df03` | created, used for the G6 and G7(d) base readings |
| `git worktree remove --force .remedy-wt/f275r22-wt-g5` | removed |
| `git worktree remove --force .remedy-wt/f275r22-wt-base` | removed |
| `git worktree prune` | ran; `git worktree list` holds ONE entry |
| `git reset --soft HEAD~1` (once, on the UNPUSHED first C4) | see deviation 1 |
| `git push -u origin feature/f275-one-world-completion-part-three` | after C5 |

No PR created, no PR merged, no `gh` command run. No force-push, no history rewrite.

## Verification

ONE line per gate, real exit code, real numbers. Every gate was run as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`.

- **G1 TRANSPORT — REAL_EXIT=0.** The delegation source `.remedy-wt/f275-r22.md`, the
  committed `.agent/authored/f275-r22.md@05cdebe2` and the committed
  `.agent/last_block.md@f1d77cac` are all **49993 bytes** at
  `101928f714785319151732c17c8758b4ded01df8221e0b7b41a7020aabff56cc` and compare
  BYTE-EQUAL. C0a copied with `shutil.copyfile`; C0b took its bytes from the COMMITTED
  C0a blob via `git show`. Per §3 item 37 this chain covers those three artefacts and
  claims NOTHING about the bytes the reviewer emitted.
- **G2 THE PLAN AND THE SLICES — REAL_EXIT=0.** `.agent/plan.md@80268fd0` is **2300
  bytes** at `0d6afa38…`, BYTE-IDENTICAL to the PLAN22 slice, **40 lines** against the
  cap of 50, with `## Goal` and `## Next Steps` each exactly once. **SLICE COUNT = 4**;
  each occurs EXACTLY ONCE in its own target. **MARKER COUNT = 8**; marker hits are
  **0** in every one of the four targets (total 0).
- **G3 THE RECORD — REAL_EXIT=0.** Three appends, each with a byte reader, a structural
  reader and a negative control. `live_review.md` 688661→702413 (slice 13751),
  `prose_slips.md` 199148→201417 (slice 2268), `decisions.md` 986483→991391 (slice
  4907). The joining byte was READ BACK from each post blob at offset `len(pre)` and is
  `b'\n'` in all three. The structural reader counted N from the slice itself — **5, 1
  and 9** paragraphs — and matched the last N blank-line units of each whole post-file
  IN ORDER with a per-unit sha256 on both sides; the unit BEFORE each region lies inside
  the pre blob in all three cases. Each NEGATIVE CONTROL flipped ONE byte inside the
  FIRST appended paragraph in memory (`'G'→'g'`, `'F'→'f'`, `'D'→'d'`) and BOTH readers
  REJECTED all three while BOTH ACCEPTED all three truths. Counts: `^Gate: ` rose
  **43→44**; `^Gate: F275 R21 `, `^Note: F275 R22 `, `^- R-0866 — `, `^- R-0867 — ` and
  `^- R-0868 — ` each **exactly once**, and `^## DECISION F275 D11 ` exactly once in
  `.agent/decisions.md@6992661a`. **THE OPEN SET BY DISTINCT ID: 88 at the base
  `5178df03` (94 registrations, 6 `Done:`) and 91 at C2 (97 registrations, 6 `Done:`)**,
  with 35 distinct `Landed:` ids never subtracted at either revision.
- **G4 THE DELETION AND THE RAW SWEEP — REAL_EXIT=1 (RED, and the red is a block
  contradiction, not an incomplete deletion — read on).** 1652 tracked files outside
  `.agent/` and `.data/` were swept for the three module names, the five deleted command
  ids, the six deleted `ContractAction` values and the five SPACED advertisement forms.
  The raw list is **20 lines**, printed in full and classified (full output in
  every hit is reproduced below in deviation 2, and the script that produced it was
  deleted with the rest of the scratch under constraint 9, so nothing here points at a
  file the reviewer cannot see). **ZERO hits for any of the five command ids,
  ZERO for any of the six `ContractAction` values, and ZERO for all five SPACED
  advertisement forms — everywhere.** 7 hits are under `docs/roadmap/features/`, the
  legitimate survivor class. The remaining **13** are all bare MODULE-NAME mentions
  under `packages/` and `tests/`, which G4 classes as defects and which the script
  therefore exits 1 on; every one of them is enumerated and justified in deviation 2.
  `tests/cli/test_advertised_commands.py` — **REAL_EXIT=0, 5 passed** — and I state
  PLAINLY that **its pass is NOT evidence for this round**: deleting the whole
  `provider` group removes it from that guard's `GROUPS` and the guard skips what it
  cannot resolve. That is R-0847, and the raw sweep above is what actually carries the
  claim.
- **G5 THE SURVIVORS STILL REFUSE — REAL_EXIT=0 on (a), (b), (d); REAL_EXIT=1 on the
  mutated run (c), which is the colour ordered.** (a) `import
  packages.orchestration.self_dogfood_execution` inside the worktree resolves to
  `/home/decodeux/Repos/remedy/.remedy-wt/f275r22-wt-g5/packages/orchestration/self_dogfood_execution.py`,
  so no editable install shadows it. (b) CONTROL, unmutated, over
  `test_self_dogfood_execution.py` + `test_repair_request_builder.py`: **exit 0, 39
  passed**. (c) MUTATION by PATH in
  `<worktree>/packages/orchestration/self_dogfood_execution.py` — `_transition`'s
  closing `return False` became `return True`, so an illegal transition is accepted
  instead of rejected; the changed bytes occurred **EXACTLY ONCE** (counted before the
  change: 1 occurrence of the old span, 0 of the mutated span). Result **exit 1, 1
  failed, 38 passed**, and the ONE test that went RED is
  `tests/orchestration/test_self_dogfood_execution.py::TestStartAndIdempotency::test_transition_rejects_illegal`.
  (d) REVERT by PATH, `__pycache__` purged, re-run: **exit 0, 39 passed** — the control
  figure returns — and the worktree `git status --porcelain` is EMPTY. `python3 -B` and a
  `__pycache__` purge preceded every run. The STOP CONDITION did not trigger.
- **G6 THE CATALOG AND THE REFERENTIAL CLOSURE — REAL_EXIT=0 at both revisions.** Read
  by IMPORTING `_BASE_CATALOG` and `GROUPS`, never by grepping the source; the base was
  read the same way inside a READ-ONLY disposable worktree at `5178df03`. BASE:
  **227 commands, 45 groups, `"provider"` in GROUPS = True, 5 `provider.` ids**
  (`intake-repair`, `material-show`, `trust-show`, `verification-show`, `verify`),
  **0 duplicate ids**. C4: **222 commands, 44 groups, `"provider"` in GROUPS = False,
  0 `provider.` ids, 0 duplicate ids**. R-0859's STANDING OBLIGATION discharged:
  every `related=` tuple resolved against the LIVE id set — **165 tuples at the base,
  160 at C4** — giving **EXACTLY 2 dangling references at each**, and they are the two
  pre-existing ones by name: `mission.run -> dogfood.run-loop` and
  `repo.status -> readiness.show`. **This round added NONE**; step 7's three repairs
  landed.
- **G7(a) THE GUARDS — REAL_EXIT=0, 884 passed.** All twelve ordered targets.
- **G7(b) THE CANARY — REAL_EXIT=0, 42 passed** (`tests/cli/test_golden_path.py`).
- **G7(c) THE FULL SUITE — REAL_EXIT=0. 18352 passed, 23 skipped, ZERO failed, 1
  warning, in 1307.13s (21m47s).** Run SERIALLY (`python3 -B -m pytest tests/ -q`, never
  `-n auto`) in the PRIMARY CHECKOUT with C4 committed. The arithmetic closes by NODE-ID
  SET DIFFERENCE of two `--collect-only` runs, the WHOLE LINE taken as the node id:
  **base 18478 distinct ids → C4 18375 distinct ids, 104 REMOVED and 1 ADDED**.
  18478 − 104 + 1 = 18375, and 18352 + 23 = 18375. Removals attributed by file:
  `test_provider_trust.py` 34, `test_provider_trust_verification.py` 27,
  `test_provider_patch_material.py` 9, `test_provider_trust_cli.py` 8,
  `test_grouped_cli.py` 8, `test_provider_material_cli.py` 7,
  `test_provider_verification_cli.py` 7, `test_self_dogfood_execution.py` 2,
  `test_repair_request_cli.py` 1, `test_repair_request_builder.py` 1. The one ADDED id is
  `tests/cli/test_repair_request_cli.py::test_text_surface_advertises_no_dead_command`.
  See deviation 6 — the block expected 105 and 2.
- **G7(d) RUFF — REAL_EXIT=0 on the change set and 0 on the parity reading.** `python3 -B
  -m ruff check` over the **15 surviving `.py` paths** of the change set: `All checks
  passed!`. Repo-wide over `packages apps tests` at BOTH revisions, the base taken in a
  DISPOSABLE READ-ONLY worktree and NEVER by writing a base blob over a tracked file:
  ruff's own summary line reads **`Found 24 errors.` at both**, my parser **PARSED 24
  findings over 16 files at both** (so no silent parse failure is hiding behind the
  agreement), and the `diff` of the two per-file distributions is **EMPTY — the
  distributions are IDENTICAL**. Paired with a RED CONTROL: adding one synthetic finding
  to `packages/orchestration/dag_schedule.py` makes the comparison report
  `identical=False`, so the comparison can fail. None of the 24 is in a file this round
  touched.
- **G8 THE TREE — REAL_EXIT=0.** `.agent/STOP` re-read from disk: does not exist.
  `git status --porcelain` **EMPTY**. `git worktree list` holds **ONE** entry. Branch is
  `feature/f275-one-world-completion-part-three`. `git diff --name-only 6992661a..0242c0a3`
  compared AS A SET against the block's C4 paths: **measured 36, block 36, MISSING 0,
  EXTRA 0**. Per-commit insertions with parent counts, each against the DECISION F104 D1
  cap of 500: C0a +490 (1 parent), C0b +419 (1), C1 +20 (1), C2 +14 (1), C3 +66 (1),
  C4 +183 (1) — **every one under 500, every one single-parent**. C4's `-4284` deletions
  do not count against that cap, which reads the `+` column only.

## Authored-text proofs

All four reviewer-authored slices were extracted PROGRAMMATICALLY from the COMMITTED
`.agent/authored/f275-r22.md` blob between their marker lines, with the markers
EXCLUDED, and applied byte for byte. None was retyped and none was edited.

| Slice | bytes | sha256 (head) | target | disk-to-disk result |
|---|---|---|---|---|
| PLAN22 | 2300 | `0d6afa38…` | `.agent/plan.md` (whole file) | byte-identical; occurs exactly once |
| LEDGER22 | 13751 | `d480e868…` | `.agent/live_review.md` (append) | `post == pre + b"\n" + slice`; occurs exactly once |
| SLIPS22 | 2268 | `2f1bfaf0…` | `.agent/prose_slips.md` (append) | `post == pre + b"\n" + slice`; occurs exactly once |
| DECISION22 | 4907 | `132fd3af…` | `.agent/decisions.md` (append) | `post == pre + b"\n" + slice`; occurs exactly once |

The production code was SPECIFIED rather than sliced, so its prose is mine; the block's
per-file insertion figures are the reviewer's dry-run expectations and are compared
against my measurements in deviation 6.

## Deviations & assumptions

**1. C4 WAS COMMITTED TWICE, AND THE FIRST ONE WAS UNSTAGED WITH `git reset --soft
HEAD~1`. THIS IS A DEPARTURE FROM THE ORDERED COMMIT SEQUENCE AND I AM DECLARING IT AS
ONE.** The first C4 (`7a81c375`) was committed, then G4 came out red on genuine dead
advertisements the block's steps had not named — the intake pipeline still drawn in
`docs/archive/candidate-generator-adapter-future.md`, two advertised commands in
`docs/system/provider-patch-materialization-v0.md`, the "Re-entry is mandatory" section
of `docs/system/repair-request-builder-v0.md`, and a `_detect_roadmap` rule in
`packages/orchestration/self_dogfood.py` gated on `has("provider_trust.py")` that could
never fire again. Constraint 3 makes C4 ONE atomic commit, so folding the repair into a
second commit would have left a half-swept deletion in the history the operator rule
forbids. The commit was UNPUSHED and nothing referenced it, so I unstaged it with
`git reset --soft HEAD~1`, applied the repairs, and re-committed the whole deletion as
ONE C4 (`0242c0a3`). No history was rewritten in any published sense, no force-push, no
branch deletion; per the standing ruling an unstage of an unpushed commit is not a
rewrite. `7a81c375` survives only in the reflog. Net effect on the ordered sequence:
zero — six commits precede C5, in the ordered order, one per step.

**2. G4 IS RED, AND ITS TWO SUB-CLAUSES CANNOT BOTH BE MET TOGETHER WITH STEPS 3(a), 5
AND 9 OF THE SAME BLOCK.** G4 demands that ANY hit for a deleted module name under
`packages/` or `tests/` be treated as a defect of this round. Steps 3(a), 5 and 9 order
me to write deliberate-absence comments "naming what is gone" and naming R-0866/R-0867,
which AGENTS.md's Code Discoverability Conventions require ("deliberate absences are
documented where a reader would search for them"). A note that names what is gone
necessarily contains the name of what is gone. I resolved it by making the sub-clause
that IS meetable pass exactly — the five SPACED advertisement forms are **ZERO
everywhere**, and so are all five command ids and all six `ContractAction` values, so no
copy-pasteable invocation of a dead command survives anywhere in the repository — and by
reporting the 13 remaining bare module-name hits classified rather than deleting text the
block itself ordered. The 13, each with why it stays:
  - `packages/orchestration/self_dogfood_execution.py:672` and
    `packages/orchestration/provider_patch_material.py:500,538` (3 hits) — MY OWN
    deliberate-absence notes, ordered verbatim by steps 3(a) and 5.
  - `packages/orchestration/self_dogfood_execution.py:160,172,188,210` (4 hits) — the
    `provider_trust_report_id` field on `SelfImprovementLinkage` and its
    `to_dict`, twice over. R-0866's fix clause says this round DELIBERATELY KEEPS the
    surviving module's vocabulary, because retiring it is a product change.
  - `packages/orchestration/provider_patch_material.py:441` — the string
    `"provider_trust_report_id"`, a key in PERSISTED job metadata written by
    `materialize_provider_repair`. Changing a persisted key is a data-shape change, not
    a deletion.
  - `packages/common/public_text_redaction.py:4` and
    `packages/orchestration/decision_evidence.py:54` (2 hits) — stale comment
    references in files the change set does NOT name. I did not widen the change set.
    **These two are new material for the reviewer**: the reviewer's dry run reported
    survivors "only under `docs/roadmap/features/`", and these two are under
    `packages/`. They are prose in comments; nothing executes them.
  - `tests/orchestration/test_cluster_deletion_map.py:56` —
    `"apps/cli/commands/provider_cmd.py"` in `CLUSTER_COMMAND_HANDLERS`. This is exactly
    R-0864, and LEDGER22's own `Note: F275 R22` says round 22 does not repair that tuple
    because R-0868 asks whether the whole file should be retired. **New material: the
    Note counts FIVE stale entries; with `provider_cmd.py` it is now SIX.**
  - `tests/orchestration/test_cluster_deletion_map.py:91` — an illustrative docstring
    example (`from packages.orchestration.provider_trust import run`) explaining how the
    importer sweep attributes a dotted name. Now a dead example rather than a wrong
    claim.
  - `tests/orchestration/test_cluster_deletion_order.py:9` — a docstring naming the pair
    as the example cycle. Not in the change set.

**3. THREE FILES IN THE CHANGE SET WERE EDITED BEYOND THE ANCHORS THE BLOCK NAMED,
because constraint 5's prose sweep found falsified text there.** All three are inside
the change set; none widens it.
  - `packages/orchestration/self_dogfood_execution.py`: the self-request text handed to
    an external candidate generator ended "Quarantined + trust-validated; an accepted
    candidate becomes a PENDING patch intent". Nothing quarantines or trust-validates
    anything now. This is the exact surface DECISION F275 D11 (b) rules on for
    `repair_request_builder.py`, so I applied the same rule. No test pinned the string.
  - `packages/orchestration/self_dogfood.py`: `_detect_roadmap`'s first rule is
    `has("provider_trust.py") and has("repair_request_builder.py")`. Its left conjunct
    is now permanently False, so the rule can never fire — a readerless definition under
    constraint 4. Deleted. `test_roadmap_items_cite_evidence` still passes because four
    other rules remain.
  - `docs/system/provider-patch-materialization-v0.md`: the See-also line for
    `repair-request-builder-v0.md` claimed "output re-enters via provider intake".
    Corrected.

**4. TWO RESIDUES I FOUND AND DELIBERATELY DID NOT REPAIR, both inside change-set
files.** `packages/orchestration/repair_request_builder.py` keeps the name
`_import_next_steps` for a helper that no longer describes an import, and keeps the
`trust_report_id` / `intake_result_id` fields on `ExternalCandidateGeneratorRecord`,
which now have no writer. Renaming the helper is not among the block's anchors and would
move a deletion figure the block calls fixed; removing the two fields changes a
persisted record's shape, which is a product change and not a deletion. Both are
reviewer material. Likewise `packages/orchestration/provider_patch_material.py`'s module
docstring still opens "Turns an **accepted** ProviderTrustReport candidate into a real,
applyable pending Repair Patch Intent" — true of the code, unreachable in the product —
and R-0867 already records that module's whole condition and routes the reaping question
to the DECISION F260 D3 round, so I left it.

**5. `_md_diff` WAS DELETED FROM `tests/orchestration/test_provider_patch_material.py`
although step 5 named only the `env` fixture and the `_job`/`_intake` helpers.** Every
one of its eight call sites was inside the deleted classes, so it became readerless —
constraint 4. `dataclasses`, `json`, `UUID`, `uuid4`, `pytest`, the model imports, `PT`,
`load_job` and `save_job` went with it for the same reason, and ruff confirms the file is
clean.

**6. WHERE MY MEASUREMENTS DIFFER FROM THE BLOCK'S STATED EXPECTATIONS.** The block marks
its insertion figures as the reviewer's dry run and "EXPECTATIONS about wording, not
numbers you owe", and its deletion figures as "fixed by their anchors". Deletions match
EXACTLY on nine files — `run_contract.py` 19, `self_dogfood_execution.py` (before
deviation 3's extra edit) 40, `repair_request_builder.py` 33, `provider_patch_material.py`
24, `command_catalog.py` 97, `commands/__init__.py` 2, `repair_cmd.py` 1, `pyproject.toml`
1, `cluster_deletion_map.txt` 5, `import_reachability_allowlist.txt` 3,
`f275_deletion_order.md` 1, `test_cluster_deletion_map.py` 4 — and the ones that differ
are listed here, measurement first:
  - `orchestrator_brain.py` **+5/-82**, block said 8/83. The one-line difference is a
    blank line at a section boundary; every anchor the step names was removed and no
    trust/verification token survives in the file.
  - `self_dogfood_execution.py` **+23/-42**, block said 24/40. The two extra deletions
    are deviation 3's request-text sentence.
  - `self_dogfood.py` **+0/-16**, block said 0/13. The three extra are deviation 3's
    dead roadmap rule.
  - `test_provider_patch_material.py` **+9/-182**, block said 9/176; the six extra are
    `_md_diff` and its now-unused imports (deviation 5).
  - `test_repair_request_builder.py` **+18/-72**, block said 11/68; my tail removal took
    the two blank lines above the deleted section with it, and the strengthened guard is
    longer than the reviewer's.
  - `test_self_dogfood_execution.py` **+20/-81**, block said 11/79.
  - `test_repair_request_cli.py` **+6/-3**, block said 7/3.
  - `test_self_dogfood_execution_cli.py` **+1/-1**, block said 2/1.
  - `orchestrator-brain-v0.md` **+10/-11**, block said 6/8; `self-dogfood-execution-v0.md`
    **+29/-11**, block said 19/18; `provider-patch-materialization-v0.md` **+11/-9**,
    block said 1/3; `repair-request-builder-v0.md` **+8/-9**, block said 0/2;
    `candidate-generator-adapter-future.md` **+6/-6**, block said 0/1. The four larger
    ones are deviation 1's dead-advertisement repairs and deviation 3's correction;
    the rest is my prose being longer than the reviewer's.
  - Whole-commit totals: **C4 is +183/-4284 over 36 paths**, of which **+183/-4283** lies
    outside `.agent/`. The block's applied dry run measured 128 insertions against 4253
    deletions over the non-`.agent/` paths.
  - **G7(c): 104 ids REMOVED and 1 ADDED**, where the block expected 105 and 2. The
    arithmetic closes either way (18478 − 104 + 1 = 18375 = 18352 passed + 23 skipped);
    the reviewer's dry run evidently split or renamed one CLI test where I re-pinned one
    and renamed one.

**7. ASSUMPTIONS.** (a) The append convention is `post == pre + ONE newline + slice as
extracted`; I verified it against round 21's landed append at `325c0149`
(`pre 680095 → post 687998`, joining byte `b'\n'`) before applying anything, and G3 reads
the joining byte back from each post blob rather than asserting it. (b) `SESSION 12` and
`rounds so far 22` are read from the previous handback's Session line and incremented.
(c) G2 was run AFTER C4 rather than at C1, because it reads committed blobs from four
different commits; nothing is measured differently either way. (d) I wrote NO verdict, NO
`Done:` paragraph, NO finding of my own and — per constraint 7 — NO `Landed:` line.

## Item status

Every ordered item of the block appears exactly once.

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | `shutil.copyfile`, 490 lines, digest verified before use |
| C0b mirror the block | done | bytes taken from the COMMITTED C0a blob via `git show` |
| C1 the plan (PLAN22) | done | whole-file replacement, byte-identical, 40 lines |
| C2 the record (LEDGER22 + SLIPS22) | done | both appended in one commit |
| C3 DECISION F275 D11 (DECISION22) | done | committed BEFORE the first `git rm` |
| C4 the whole deletion | deviated | ONE commit as ordered, but committed twice; the first was unstaged unpushed — deviation 1 |
| C4 step 1 — `git rm` the ten DIES WHOLE paths | done | all ten line counts matched the block; my own sweep found no further such file |
| C4 step 2 — `orchestrator_brain.py` | done | every named anchor; `EXTERNAL_BUILDER_NEEDED` and `self_attempts_awaiting` KEPT |
| C4 step 3 — `self_dogfood_execution.py` + two test files | deviated | (a)–(f) all done; one extra falsified sentence fixed — deviation 3 |
| C4 step 4 — `repair_request_builder.py`, its CLI, two test files | done | five advertisements gone, both fields REMOVED not emptied, both re-pins landed |
| C4 step 5 — `provider_patch_material.py` + test file | deviated | as ordered, plus `_md_diff` — deviation 5 |
| C4 step 6 — `self_dogfood.py`, `run_contract.py` | deviated | both blocks deleted; one dead roadmap rule also — deviation 3 |
| C4 step 7 — catalog + dispatcher | done | group, section (5 ids), the ORPHANED comment, three `related=` repairs, both `__init__.py` sites |
| C4 step 8 — ratchets, order file, `pyproject.toml` | done | map REGENERATED (0 edges), `CLUSTER_MODULES` empty + annotated, 26-line header byte-identical, 3 allowlist entries, 1 pyproject line |
| C4 step 9 — the documentation | deviated | all named pages, plus three dead-advertisement repairs the sweep found — deviations 1 and 3 |
| C5 the handback | done | this file; `.agent/handoff.md` rewritten once |
| Constraint 1 — slices byte for byte | done | extracted from the committed blob, never retyped, never edited |
| Constraint 2 — C3 before the first `git rm` | done | `6992661a` precedes `0242c0a3` |
| Constraint 3 — C4 is ONE commit | done | one commit; see deviation 1 for how it got there |
| Constraint 4 — R-0855 neighbourhood sweep | done | `_self_provider_label`, `_md_diff`, the orphaned catalog comment, a dead roadmap rule; residues in deviation 4 |
| Constraint 5 — R-0843 prose sweep, reported including "nothing" | done | NOT nothing: eight falsified passages found, five ordered and three extra (deviation 3); two more declined (deviation 4) |
| Constraint 6 — no stub, shim, copy or compatibility reader | done | nothing was copied out of either dying module; the survivors lost call sites |
| Constraint 7 — no verdict, no `Done:`, no finding, no `Landed:` | done | none written |
| Constraint 8 — do not repair the 24 ruff findings | done | `Found 24 errors.` at both revisions, identical distribution |
| Constraint 9 — scratch under `.remedy-wt/`, worktrees pruned | done | two worktrees created and removed; `git worktree list` holds ONE entry |
| Constraint 10 — full suite serially, primary checkout | done | `python3 -B -m pytest tests/ -q`, 1307.13s, never `-n auto`, never in a worktree |
| G1 TRANSPORT | done | REAL_EXIT=0 |
| G2 THE PLAN AND THE SLICES | done | REAL_EXIT=0 |
| G3 THE RECORD | done | REAL_EXIT=0 |
| G4 THE DELETION AND THE RAW SWEEP | deviated | REAL_EXIT=1; the ids, the actions and the spaced forms are all ZERO — deviation 2 explains the 13 module-name hits |
| G5 THE SURVIVORS STILL REFUSE | done | control 39, mutation 1 failed / 38 passed, revert 39, worktree clean |
| G6 THE CATALOG AND R-0859's CLOSURE | done | REAL_EXIT=0 at both revisions; 2 dangling at each, none added |
| G7 THE SUITE, THE GUARDS AND RUFF | done | (a) 884, (b) 42, (c) 18352 passed / 23 skipped / 0 failed, (d) 24 = 24 identical |
| G8 THE TREE | done | REAL_EXIT=0; 36 = 36, MISSING 0, EXTRA 0 |

## Next

Reviewer: re-run every gate against the committed range `5178df03`..`0242c0a3` and
issue the round 22 verdict. The two questions the verdict must answer are in
deviation 1 (C4 committed twice, the first unstaged unpushed) and deviation 2 (G4's
`ANY hit under packages/` clause against the same block's order to write deliberate
absences). Session 12 continues from there; Phase 1 rule 1 — re-read `.agent/STOP`
from disk — comes before Phase 1 rule 2.

## Reviewer verdict on round 22 — appended after the handback, by the reviewer's authored text

VERDICT ROUND 22: **PASS.** Written by the planner and reviewer of SESSION 12 after reading the committed
range `5178df03`..`67f83bdd` and RE-RUNNING EVERY GATE INDEPENDENTLY against the committed blobs; the
worker's report was not evidence for any line below. It is carried here because under
`docs/agents/self_drive_protocol.md` a verdict that stays in the session is lost, and it is booked into
`.agent/live_review.md` by the FIRST substantive commit of round 23, per amend0827-process-diet rule 1.

WHAT THE REVIEWER RE-MEASURED. Seven single-parent commits C0a `05cdebe2`, C0b `f1d77cac`, C1 `80268fd0`,
C2 `c9b439b3`, C3 `6992661a`, C4 `0242c0a3` and C5 `67f83bdd`, per-commit insertions 490, 419, 20, 14, 66
and 183 for the six before the handback, every one under the AGENTS.md DECISION F104 D1 cap of 500, each
parent count read from `git log --format=%p`. G1 IS THE PRIMARY PROOF OF §4 ITEM 9 AND NOT THE DIGEST
FALLBACK: the reviewer's own delegation source `.remedy-wt/f275-r22.md` and both committed copies are
49993 bytes at `101928f714785319151732c17c8758b4ded01df8221e0b7b41a7020aabff56cc` and compare BYTE-EQUAL;
per §3 item 37 that chain covers those three artefacts and claims nothing about the emitted bytes. G2:
`.agent/plan.md` at C1 is 2300 bytes byte-identical to the PLAN22 slice, 40 lines against the cap of 50,
with `## Goal` and `## Next Steps` each exactly once; all FOUR slices occur EXACTLY ONCE in their targets
and a sweep for all eight marker strings over the four target files returns ZERO for every file.

G3 HELD OVER THREE APPENDS. For `.agent/live_review.md`, `.agent/prose_slips.md` and
`.agent/decisions.md` the committed post-blob equals the pre-blob, then ONE newline, then the slice
exactly as extracted; the joining byte was READ BACK from each post blob at offset `len(pre)` and is a
newline in all three, rather than asserted — the correction the round 21 slip asked for. The structural
reader counted N from the slice itself — 5, 1 and 9 paragraphs — and matched the last N blank-line units
of each whole post-file IN ORDER, and all three NEGATIVE CONTROLS were flipped inside the FIRST appended
paragraph per §3 item 36 and rejected by BOTH readers while both accepted all three truths. `^Gate: `
rose 43 to 44; `^Gate: F275 R21 `, `^Note: F275 R22 `, `^- R-0866 — `, `^- R-0867 — `, `^- R-0868 — ` and
`^## DECISION F275 D11 ` each occur EXACTLY ONCE. THE OPEN SET WENT 88 TO 91 BY DISTINCT ID against
registrations 94 to 97 and resolutions 6 to 6, with `Landed:` unchanged at 39 lines and 35 distinct ids
and never subtracted — correct for a round that registers three findings and resolves none.

G4 IS RED, AND THE REVIEWER SUSTAINS BOTH THE COLOUR AND THE WORKER'S REFUSAL TO CHASE IT. The gate as
the reviewer wrote it CANNOT PASS, and that is a defect of the block rather than of the round: its final
clause makes ANY hit for a deleted module name under `packages/`, `apps/` or `tests/` a defect of the
round, while steps 3(a), 5 and 9 of the SAME block ORDER deliberate-absence comments that name exactly
those modules, because AGENTS.md's Code Discoverability Conventions require a deliberate absence to be
documented where a reader would search for it. That is `docs/agents/planner_reviewer_prompt.md` §3 item 2
verbatim — a zero-gate counting a string the same block writes into the same file — and it is registered
below as `R-0869`, because amend0827-process-diet rule 2 reserves an id for a gate over production code
shown to be unmeetable.
THE HALF THAT IS MEETABLE HOLDS COMPLETELY, and it is the half R-0861's fix clause exists to protect. The
reviewer re-ran the sweep with its own script over the **1652** tracked files outside `.agent/` and
`.data/`: all five deleted command ids, all six deleted `ContractAction` values and all five SPACED
advertisement forms — `remedy provider intake-repair`, `trust-show`, `material-show`, `verify` and
`verification-show` — return **ZERO hits anywhere in the repository**, so no page and no live code path
still gives an operator a command that cannot run. RAW over the bare module names is **20**, printed in
full and not truncated by the worker, and the reviewer's own classification of it is: **7** are history
prose under `docs/roadmap/features/`, the legitimate survivor class since round 19; **5** are the
deliberate-absence notes the block itself ordered, in `self_dogfood_execution.py` and
`provider_patch_material.py`; **5** are PERSISTED data-shape names — the `provider_trust_report_id` field
and JSON key — which a deletion round must not change, because a stored record's shape is not a code
reference; **2** are illustrative docstring examples inside the two cluster ratchets R-0868 already routes
for retirement; and **1** is the stale `CLUSTER_COMMAND_HANDLERS` entry that is R-0864's own subject.
That leaves exactly **TWO** genuinely new residues, both prose in comments and both in files the change
set did NOT name: `packages/common/public_text_redaction.py:4`, whose provenance sentence cites a path
that no longer exists, and `packages/orchestration/decision_evidence.py:54`, which calls
`provider_trust_verification.ProviderVerificationEvidenceRef` one of "the two nearest existing types" and
is now simply FALSE. The worker found both, declined to widen an exhaustive change set to reach them, and
flagged them for the reviewer — which is the correct handling, and they are folded into R-0855 below
rather than given an id of their own, per §3 item 30.

G5's STOP CONDITION DID NOT FIRE. The reviewer re-ran the red-proof in a disposable worktree at C4
`0242c0a3`: the import resolves inside that worktree so no editable install shadows it, the mutated bytes
occur exactly ONCE in the named path, the unmutated CONTROL is exit 0 at 39 passed, making `_transition`
ACCEPT an illegal transition instead of refusing is exit 1 with EXACTLY ONE failure —
`TestStartAndIdempotency::test_transition_rejects_illegal` — and the revert returns exit 0 at 39 passed
with the worktree porcelain EMPTY. The state machine this round leaves standing is guarded by a test that
bites.

G6 DISCHARGES R-0859's STANDING OBLIGATION BY MEASUREMENT. Reading the SHIPPED catalog by importing
`_BASE_CATALOG` and `GROUPS`, never by grepping source, and reading the base the same way in a READ-ONLY
disposable worktree: commands fall **227 to 222**, groups **45 to 44**, `"provider"` is ABSENT from
`GROUPS`, the id set beginning `provider.` is EMPTY where the base held five, duplicate ids are **0** at
both revisions, and resolving every `related=` tuple against the live id set — 165 tuples at the base, 160
at the tip — gives EXACTLY TWO dangling references at BOTH revisions, `mission.run -> dogfood.run-loop`
and `repo.status -> readiness.show`, both pre-existing and both held by R-0859. THIS ROUND ADDED NONE,
which is what the standing obligation asks, and step 7 repaired the three it would otherwise have created.

G7: the guards 884 passed, the canary 42, and THE FULL SUITE WAS RE-RUN BY THE REVIEWER SERIALLY IN THE
PRIMARY CHECKOUT and was GREEN at **18352 passed, 23 skipped and ZERO failed** in 1287.83s. THE ARITHMETIC
CLOSES BY THE ID SET, taking the WHOLE line as the node id so a parametrized id carrying a space is not
truncated into a collision: **18478** at the base against **18375** at the tip, being **104 ids REMOVED
against 1 ADDED**, and 18352 plus 23 equals 18375 exactly. The 104 are 61 across the two deleted module
test files, 22 across the three deleted CLI test files, 9 in `test_provider_patch_material.py`, 8
parametrized `[provider]` cases in `tests/test_grouped_cli.py` generated from the catalog `GROUPS`, and 4
across three re-pinned files; the single added id is the re-pinned text-surface guard. Ruff reads
`Found 24 errors.` at BOTH revisions with 24 findings PARSED over 16 files on each side and IDENTICAL
per-file distributions, and the reviewer paired that comparison with a RED CONTROL confirming it can fail,
so the agreement is a measurement rather than a silent parse failure. Not one of the 24 is in a file this
round touched. G8: no `.agent/STOP`, porcelain EMPTY, ONE worktree, the branch correct, `C3..C4` naming
**36** paths in an exact set match with MISSING and EXTRA both empty, exactly TEN files deleted whole, and
every one of the **42** `+/-` cells of the handback's `## Commits` tables agreeing with
`git show --numstat` for its commit.

ALL SEVEN DECLARED DEVIATIONS ARE SUSTAINED, and the two that matter are the round rescuing the reviewer.
FIRST, C4 was committed, found wanting by the worker's own G4 run, unstaged with `git reset --soft` while
UNPUSHED, repaired and re-committed as ONE commit. That was correct: constraint 3 makes C4 atomic by
operator RULE 1, so folding the repair into a second commit would have put a half-swept deletion into the
history that rule forbids, and an unstage of an unpushed commit is not a history rewrite. What the repair
ADDED is the reviewer's own gap: FOUR dead advertisements the block's steps had not named — the intake
pipeline still drawn in `docs/archive/candidate-generator-adapter-future.md`, two advertised commands in
`docs/system/provider-patch-materialization-v0.md`, the re-entry section of
`docs/system/repair-request-builder-v0.md`, and a `_detect_roadmap` rule in `self_dogfood.py` gated on
`has("provider_trust.py")` that could never fire again. The reviewer's applied dry run had edited those
first two pages more narrowly and had not reached the other two at all; the spaced-form sweep reads ZERO
because the worker went further than it was told. SECOND, three further widenings inside change-set files
and two residues deliberately left, every one reasoned and every one flagged: a falsified sentence in the
self-request text handed to an external actor, a permanently-False roadmap rule, a stale See-also claim,
against a helper name `_import_next_steps` and two writerless persisted fields left alone because renaming
and re-shaping a stored record are product changes rather than deletions. The remaining assumptions — the
append convention verified against round 21's landed append before use, G2 run after C4 because it reads
blobs from four commits, and one unpushed `--amend` of C5 to remove a pointer at scratch the block
required deleting — are all sound.

## Findings and corrections drafted by session 12, to be booked by round 23's first substantive commit

- R-0869 — Medium, A ZERO-GATE OVER PRODUCTION CODE WAS UNMEETABLE BY CONSTRUCTION, BECAUSE THE SAME BLOCK ORDERED THE VERY TEXT IT FORBADE. Raised by the reviewer of session 12 against its own round 22 block and registered here rather than as a prose slip, because amend0827-process-diet rule 2 reserves an id for "a gate over production code shown to be blind or unmeetable" and this gate was ordered over `packages/`, `apps/` and `tests/`. THE MEASUREMENT, taken at `67f83bdd`: G4's closing clause reads that ANY hit for a deleted module name under `docs/guides/`, `docs/system/`, `packages/`, `apps/`, `scripts/` or `tests/` "is a defect of this round", while steps 3(a), 5 and 9 of the same block order deliberate-absence comments naming `provider_trust` and `provider_trust_verification` into `packages/orchestration/self_dogfood_execution.py`, `packages/orchestration/provider_patch_material.py` and `docs/system/self-dogfood-execution-v0.md` — five hits the block itself commissioned. The worker could satisfy the clause only by deleting text the same block ordered, so it ran the gate, reported exit 1, enumerated all 20 raw hits and declared the contradiction; that is the honest reading and it cost the round a deviation. `docs/agents/planner_reviewer_prompt.md` §3 item 2 states this rule exactly — "a `must be 0` done-when may not count a string that any TO slice in the same block writes into that same file" — and item 2's own note records that it had recurred six times across F104 and F105 before it was written down, so this is the class recurring under the rule rather than a new one. FIX CLAUSE, binding on the next block of this feature that orders a completeness sweep after a deletion: split the sweep into the clause that CAN be zero and the clause that cannot. The command ids, the ContractAction values and the SPACED advertisement forms are the meetable half and stay a hard zero, because nothing the block orders writes a runnable invocation; the BARE MODULE NAME half is ordered as a RAW LIST to be printed and classified, with the block naming in advance the files its own deliberate-absence notes will put a name into, so the worker reconciles against a stated expectation instead of against an impossible zero.

Note: F275 R23 — new evidence for the OPEN finding R-0855, added rather than given an id of its own per `docs/agents/planner_reviewer_prompt.md` §3 item 30, which orders the open set searched for the DEFECT before an id is minted. R-0855 records that an ordered anchor deletes a definition without sweeping the neighbourhood that definition served. THESE ARE THE FIFTH AND SIXTH INSTANCES, both measured by the reviewer at `67f83bdd` while re-gating round 22, and both in files round 22's change set did NOT name, which is why the round's own sweep could only report them: `packages/common/public_text_redaction.py` line 4 cites `packages/orchestration/provider_trust.py` as the origin of the redaction helpers it now hosts, and that path no longer exists, so a reader following the provenance sentence written one round earlier lands on nothing; and `packages/orchestration/decision_evidence.py` line 54 names `provider_trust_verification.ProviderVerificationEvidenceRef` as one of "the two nearest existing types", which is not stale wording but a FALSE claim, since that type is gone and only `orchestrator_brain.OrchestratorEvidenceRef` remains. NO GATE COULD SEE EITHER: ruff is clean, the full suite is green at 18352 passed, and both lines are prose inside comments. The first is the sharper lesson, because the reviewer WROTE that provenance sentence in round 21 knowing round 22 would delete its referent. FIX CLAUSE, binding on the round that drafts DECISION F260 D3: repair both lines — the first by naming the deletion rather than the path, the second by dropping the vanished type and keeping the surviving one — and, before that round's own sweep is declared clean, run it over the files the PREVIOUS round created as well as the files it edited.

Note: F275 R23 — a correction to the `Note: F275 R22 ` entry booked by round 22's C2, which states that `CLUSTER_COMMAND_HANDLERS` in `tests/orchestration/test_cluster_deletion_map.py` names seven handler paths of which FIVE have no file on disk. Measured by the reviewer at `67f83bdd`, after round 22 deleted `apps/cli/commands/provider_cmd.py`: the tuple still names seven and now SIX of them are stale — `dogfood_cmd.py`, `overnight_mission_cmd.py`, `progress_cmd.py`, `provider_cmd.py`, `repair_loop_v2_cmd.py` and `self_repair_cmd.py`, leaving `review_cmd.py` as the only entry that resolves. The earlier entry was true when it was written, at the base of the round that wrote it, and it named no commit — which is the §3 item 20 failure, not the arithmetic. The record is append-only, so that entry is NOT rewritten; this is the dated correction the checklist prescribes instead. The count is not load-bearing to R-0864, whose subject is that a stale entry can never fail, so no correction round is owed and R-0868's fix clause still carries the repair.

Done: R-0862 — Resolved by F275 round 21. The human-review routing tier has a positive pin again. `tests/orchestration/test_orchestrator_brain.py::TestModelRouting::test_loop_guard_forces_human_review_tier` drives two `tested_failed` repair attempts into the loop guard, asserts `LoopGuardStatus.REQUIRE_HUMAN_REVIEW` as a PRECONDITION so the test cannot pass vacuously, and then asserts `_routing_plan` returns `RoutingTier.HUMAN_REVIEW_REQUIRED` with `allow_external` False. THE COLOUR THE FIX CLAUSE ASKED FOR WAS MEASURED, by the reviewer as well as by the worker, in a disposable worktree at `eaea1cff`: the unmutated control is exit 0 at 6 passed, replacing the two-line loop-guard condition at the top of `_routing_plan` with a constant false gives exit 1 with EXACTLY ONE failure, that test, reading `assert 'local_advisor_preferred' == 'human_review_required'`, and the revert returns exit 0 at 6 passed. R-0862's own measurement was that the same mutation left `TestAntiLoop` and `TestModelRouting` GREEN at 5 passed, so the branch went from unpinned to pinned and the finding is closed on its own terms. The tier itself never changed and no capability was inherited by another feature; only its guard was missing, which is why it was Medium.

## Prose slips drafted by session 12, to be appended by round 23's ledger commit

2026-09-10 · F275 R22 · The round 22 block's SLIPS22 slice carried three dated entries separated by single newlines, while every entry already in `.agent/prose_slips.md` is separated from its neighbour by a BLANK line. The three landed as one blank-line unit, so the file's own record shape is broken for them and a reader counting entries by paragraph will find one where there are three. The structural reader in that round's G3 counted N as 1 and was right to; nothing measured the SHAPE against the shape of the entries it joined, which is `docs/agents/planner_reviewer_prompt.md` §3 item 26 applied to a file other than the ledger. The record is append-only so the landed entries stay as they are. The lesson is that item 26's mechanical comparison is run for EVERY append-only target a block writes into, not only for `.agent/live_review.md`, and that the separator is part of the record format rather than presentation.

2026-09-10 · F275 R22 · The round 22 block's documentation step named six pages and the reviewer's applied dry run had edited them, yet the worker's own sweep found FOUR dead advertisements the step had not reached: the intake pipeline still drawn in `docs/archive/candidate-generator-adapter-future.md`, two advertised commands in `docs/system/provider-patch-materialization-v0.md`, the re-entry section of `docs/system/repair-request-builder-v0.md`, and a `_detect_roadmap` rule in `packages/orchestration/self_dogfood.py` gated on a module file that would never exist again. The reviewer's dry run had reached those first three pages and edited only their LINKS, because the token sweep that drove it matched module names and command ids rather than the prose around them. The lesson is that a deletion round's documentation step is derived from a sweep for the CAPABILITY in the pages' own words — "re-enter", "import the response", "intake" — and not only from a sweep for the identifiers being deleted, because a page can advertise a deleted flow without naming a single deleted symbol.

2026-09-10 · F275 R22 · The round 22 block's introduction said `provider_patch_material.py` "loses six of its imports", a figure inherited verbatim from session 11's handoff, and the R-0867 slice repeated it as "takes six names from the dying pair". The reviewer caught it before emission by resolving the module's import statements at the base, where the answer is FOUR — session 11 measured six before F275 round 21 moved `_scrub_public` and `_safe_path_label` out of that dependency — and corrected both occurrences. It is recorded even though nothing landed wrong, because the same session had already written a slip about re-measuring inherited prose and then reproduced the class twice in the next block it wrote. The lesson is that every numeral carried across a session boundary is re-derived from the tree, and that a slip written about a class is not evidence the class has stopped.

## Session 12 ends here — TWO delegated rounds, both PASS, both independently re-gated

Stated plainly, because the number is below the floor. `docs/agents/self_drive_protocol.md` G7, as amended
by amend0905-throughput, targets SIX TO EIGHT delegated rounds per session with FOUR as the floor, and
this session ran TWO. That is a real shortfall and it is reported as one.

THE REASON IS THE ONE amend0905 SANCTIONS — a round that explicitly needs a fresh session — AND IT IS
OFFERED AS A MEASUREMENT. Round 23 is the DECISION F260 D3 round, and it is the round on which EIGHT open
fix clauses fall due together: R-0832's event-name coupling measurement, R-0858's F267 repair, R-0859's
referential-closure test, R-0860's thirteen command ids and the product-spine deliberate-absence note,
R-0864's two vacuous ratchets, R-0866's ruling on the surviving self-dogfood vocabulary, R-0867's ruling
on which feature reaps `provider_patch_material.py`, and R-0868's retirement of the now-empty cluster
scaffolding. Its central artefact is a paragraph that F260's own Design section requires to name EVERY
module deleted in the slice together with the feature that inherited its idea, and F260's mapping
paragraph supplies only seven mappings for the twenty-four modules its Design section lists, so the rest
must be resolved from the feature files before a line of that paragraph can be written. None of that
research is done, it lands in the append-only record where it cannot be corrected, and it is the same
category of reason session 11 gave for round 20 and session 9 for round 18. The OTHER sanctioned reason is
explicitly NOT claimed: operator amendment amend0908-f275-finish rule 5 permits "authoring errors
accumulating" to end a session only after at least four delegated rounds, this session ran two, so that
reason is unavailable — which matters, because four of this session's own authoring slips are recorded
above and it would otherwise have been the honest one.

WHAT THIS SESSION LANDED. Round 21 moved the five shared redaction names out of the dying
`provider_trust.py` into the new `packages/common/public_text_redaction.py` BYTE-IDENTICALLY under
DECISION F275 D10, repointed nine importers, and discharged R-0862's fix clause with the mutation colour
that clause demanded. Round 22 then deleted the LAST component of `.agent/f275_deletion_order.md` — the
strongly connected pair `provider_trust` and `provider_trust_verification` — in ONE commit of 36 paths and
4284 deletions, taking its handler, the whole `provider` command group with all five commands, six
`ContractAction` members, four whole test files and two documentation pages, and degrading three surviving
consumers under DECISION F275 D11 rather than deleting, stubbing or copying into any of them.
**T001's module list is now EMPTY**: `CLUSTER_MODULES` is the empty tuple, `cluster_deletion_map.txt`
holds no edge lines, and `.agent/f275_deletion_order.md` holds no component lines. Every module F260's
Design section named is gone from disk. Three findings — R-0866, R-0867, R-0868 — record the capabilities
that went with the deletion, and the full suite is green at 18352 passed, 23 skipped and ZERO failed.

CONTEXT SELF-ASSESSMENT, as amend0905-throughput requires in one sentence: the reviewer's context is long
but NOT exhausted and is not the reason this session ends — it ran four full serial suites, two as applied
dry runs establishing each round's boundaries and two as independent re-gates, and it ends on round 23's
research being unstarted rather than on the reviewer running out of room.

## What the next session owes, in order

FIRST, Phase 1 rule 1: re-read `.agent/STOP` from disk before the Open PR Gate. It does not exist as this
session ends and was measured absent at the Phase 0 probe and again before each of the two rounds. Then
the Open PR Gate: no pull request is open, and none is owed until the closure sequence.

SECOND, round 23's FIRST substantive commit books, from this file as the durable carrier under
amend0827-process-diet rule 1: the ROUND 22 PASS verdict above as a `Gate: F275 R22` entry in
`.agent/live_review.md`; the `R-0869` registration; the two `Note: F275 R23` entries, one folding two new
instances into R-0855 and one correcting the stale-entry count of round 22's own Note; the `Done: R-0862`
resolution, which replaces the `Landed: R-0862` line round 21 wrote; and the three prose slips above as
dated lines in `.agent/prose_slips.md`, BLANK-LINE SEPARATED. The open set is 91 by distinct id and the
next free id after R-0869 is R-0870; booking R-0869 and resolving R-0862 takes it to 91 again.

THIRD, round 23 itself: DECISION F260 D3. Do the research BEFORE authoring — resolve every module in
F260's Design list to the feature that inherited its idea, because F260's own mapping paragraph covers
only seven of them. The eight fix clauses listed above all fall due in that round; R-0868's asks whether
the empty cluster ratchets are retired or kept with a dated reason, and R-0866's and R-0867's are rulings
rather than repairs. Order the completeness sweep in the split form R-0869's fix clause prescribes, so the
round is not handed a gate that cannot pass. Then T002, the atomic record flip, alone, and then T003.
