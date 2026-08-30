# Handoff — F258 Self-use track v2

## Session

SESSION 3 of feature F258 · round 11 · rounds so far 11

## State

Branch `feature/f258-self-use-v2`, cut from `main` at
`18ae71293cde9b1157aca35d3d02c3a8f4265813` (the merge commit of pull request
225, F040's closure). This round executed
`docs/roadmap/STATUS_closure_protocol.md` Algorithm steps 1 (evidence job)
and 2 (review zip) only — it does NOT close the feature: no `[x]`, no
README sync, no `consumed_by` edit, no PR. Constraint 0 was checked first
and cleanly: `gh pr list --state open ...` returned `[]`, `git rev-parse
HEAD` equalled `3d2ab8b558de3ea945ef64cd83c7e7eacf850ae0` (the block's Base
`3d2ab8b5` in full), branch was `feature/f258-self-use-v2`. Commits C0a-C2
saved the block, rewrote `.agent/plan.md` from PLANF258R11 and booked
`Gate: F258 R10` into `.agent/live_review.md`. The branch was pushed at C2
(`49fcc2c645601936d8c426b1eb09523b9b3c7f6f`), then the evidence bundle and
the review zip were built from that clean, pushed tree (nothing under
`packages/`, `apps/`, `tests/`, `scripts/` or `docs/` was edited — confirmed
by `git diff --name-only 3d2ab8b5..49fcc2c6`, which lists only the four
`.agent/` paths). Open findings count in `.agent/live_review.md`: 318
registered R-ids (UNMOVED), 55 distinct resolved (`Done:`, UNMOVED), open
set `len(set(registered) - set(resolved))` = 263 (UNMOVED). This round
registered no id and resolved none, per constraint 7. `Gate: F\d+ R\d+ — `
line count moved 173 → 174 (the one `Gate: F258 R10` append). R-0570 (Low),
R-0736 (Medium) and R-0757 (Medium) stay OPEN, untouched.

The evidence bundle and BOTH review zips (the READY package and the
deliberate red control) were built entirely under the gitignored
`.remedy-wt/` and archived/left under `/home/decodeux/Repos/remedy-history/
zips/`, neither ever staged nor committed — confirmed by `git ls-files
.remedy-wt | wc -l` = 0 and `git ls-files | grep -c remedy-job-evidence` =
0, both after the builds.

## Range

Review of `3d2ab8b5..49fcc2c6` (C2, the accepted HEAD this round's zip
covers). `.agent/handoff.md` (this file, C3) is written and pushed after
this range ends, per the block's own build order (package before handback).

## Item status

Every bundle item and every gate, each appearing exactly once:

| Item | Status | Reason |
|------|--------|--------|
| Constraint 0 (PR list, HEAD, branch) | done | `[]`, HEAD = `3d2ab8b558de3ea945ef64cd83c7e7eacf850ae0`, branch = `feature/f258-self-use-v2` |
| C0a save block to `.agent/authored/f258-r11.md` | done | `shutil.copyfile`, sha256-verified equal to scratch original |
| C0b mirror into `.agent/last_block.md` | done | `shutil.copyfile`, one blob id confirmed both paths |
| C1 rewrite `.agent/plan.md` from PLANF258R11 | done | byte-equal, 1718 bytes, 39 lines |
| C2 append GATEF258R10 to `.agent/live_review.md` | done | whole-file reconstruction holds; negative control REJECTED a flipped copy, ACCEPTED the true one |
| Push at C2 | done | `3d2ab8b5..49fcc2c6 feature/f258-self-use-v2 -> feature/f258-self-use-v2`; origin confirmed at C2 afterward |
| Evidence script adaptation | done | extracted `EVIDENCESCRIPT` from `git show HEAD:.agent/authored/f009-r33.md`; unified diff shows exactly the listed values changed, nothing else |
| Evidence bundle build (`f258-closure`) | done | 7 scoped suites, 408 total passed, all 8 closed-schema gate files present |
| READY review zip | done | `PACKAGE_STATUS=READY_FOR_REVIEW`, archived |
| RED CONTROL review zip | done | `PACKAGE_STATUS=BLOCKED_EVIDENCE`, `EVIDENCE_AUTHORITATIVE=false`, REAL exit 0 — the deliberate control passed (i.e. correctly failed) |
| Archive READY zip | done | already written directly to `/home/decodeux/Repos/remedy-history/zips/` by `scripts/make_review_zip.sh`'s own default `REMEDY_REVIEW_DIR` — no `shutil.move` was needed; see Deviations |
| G1 hygiene | done | `.agent/STOP` absent at both readings; `git status --porcelain` clean throughout |
| G2 transport | done | committed blob and scratch original both sha256 `54b5c9629cf9179cb6ed9f15ba369dea294a08336f7d331b03f070e5de1ea1b6`, 21196 bytes, EQUAL True; C0b's two blob ids equal (`f6d2957e329bd25927bb1e89be7d6783ae833f4b`) |
| G3 the plan at C1 | done | byte-equal to PLANF258R11, 1718 bytes both sides, 39 lines (< 50), one `## Goal`, one `## Next Steps` |
| G4 the record append at C2 | done | `base(1798961) + 1 + GATEF258R10(2630) == committed(1801592)` True; negative control (byte XOR-flip inside the appended region) correctly False; base is a byte prefix; ends in exactly one `\n` |
| G5 the ledger at C2 | done | registered UNMOVED 318 (all distinct), `Done:` UNMOVED (57 mentions / 55 distinct), `Gate:` count 173→174, open set UNMOVED 263; `Gate: F258 R10 — ` count at C2 = 1 |
| G6 the evidence bundle | done | diff is exactly the listed values (12 removed / 14 added lines); all 7 runs: passed 23/18/20/7/3/295/42, failed/skipped/deselected 0 everywhere, `len(node_ids)==selected` True everywhere, `test_files` sorted (single-file lists) everywhere; `_unsafe_text` scan: 0 rejected over real ids/commands, red control on a fabricated absolute path correctly True; all 8 gate files present; `output_hash == sha256(stdout_summary)` True for all 7 runs |
| G7 the review zip | done | READY: filename `remedy-review-20260830-084541-READY_FOR_REVIEW.zip`, sha256 `4b4153ad33f01e4d7014e853663f76ac1f36f61ba06687ed0b3c9c5411f12c50`, REAL exit 0, `PACKAGE_STATUS=READY_FOR_REVIEW`; manifest `package_status=READY_FOR_REVIEW`, `ready_gate_matrix.ok=True`, `blocking_reasons=[]`, `committed_review_subject.head_commit=49fcc2c645601936d8c426b1eb09523b9b3c7f6f` = C2 exactly; CONTROL: `PACKAGE_STATUS=BLOCKED_EVIDENCE`, `EVIDENCE_AUTHORITATIVE=false`, REAL exit 0 (exit code did not distinguish the two, status did); archived path confirmed to exist, 19357817 bytes; `git status --porcelain` = 0 throughout |
| G8 structure and remaining preconditions | done | changeset-minus-range residue (excluding `.agent/handoff.md`) empty; range-minus-changeset residue (full change set) empty; insertions 342/317/2/17 all < 500; all four commits single-parent; `<<<SLICE `/`<<<END ` counts: `plan.md` 0, `live_review.md` 0, `.agent/authored/f258-r11.md` 4 (non-zero control); `git ls-files .remedy-wt` = 0; `git ls-files \| grep -c remedy-job-evidence` = 0; `STATUS.md`/`README.md`/`self_use_queue.json`/`T5_F258.md` all ABSENT from the range diff; precondition 3: `run_integrity_checks().passed` = True, `.fail_count` = 0 |

## Commits

All `+/-` figures are `git diff --numstat` insertions/deletions against
each commit's own parent.

### bd6c5766 docs(f258): save round 11 authored block (C0a)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f258-r11.md` | 342/0 | C0a — verbatim copy of the round's step block, `shutil.copyfile` |

### 5095b4fe docs(f258): mirror round 11 block to last_block.md (C0b)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | 317/180 | C0b — verbatim copy of the same block, `shutil.copyfile`, into the mirror slot (whole-file rewrite, prior round's block replaced) — exempt from the 500-line insertion cap as a single `.agent/**` state-file rewrite, and under it anyway |

### 581118e6 docs(f258): advance plan.md to round 11 (C1)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | 17/21 | C1 — rewritten from slice PLANF258R11, byte-equal, 39 lines |

### 49fcc2c6 docs(f258): book round 10 verdict into live_review.md (C2)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | 2/0 | C2 — GATEF258R10 appended verbatim, `base + "\n" + GATEF258R10` — ACCEPTED HEAD |

Not tabled per the template's self-reference exception: the commit that
writes this handback (C3) — its own numbers are the reviewer's to measure
at the next gate.

## External actions

- `git push origin feature/f258-self-use-v2` (after C2) —
  `3d2ab8b5..49fcc2c6 feature/f258-self-use-v2 -> feature/f258-self-use-v2`,
  success.
- `bash scripts/make_review_zip.sh --evidence-dir
  .remedy-wt/f258_closure_evidence/remedy-job-evidence-f258-closure` (READY
  build) — `PACKAGE_STATUS=READY_FOR_REVIEW`, zip
  `remedy-review-20260830-084541-READY_FOR_REVIEW.zip`, sha256
  `4b4153ad33f01e4d7014e853663f76ac1f36f61ba06687ed0b3c9c5411f12c50`,
  written directly to `/home/decodeux/Repos/remedy-history/zips/` by the
  script's own default archive directory.
- `bash scripts/make_review_zip.sh --evidence-dir
  .remedy-wt/f258_closure_evidence/remedy-job-evidence-f258-closure`
  (re-run, wrapped `bash -c '...; echo REAL_EXIT=$?'` to capture the real
  exit code per constraint 5) — REAL_EXIT=0, produced a second,
  byte-different READY zip (`remedy-review-20260830-084957-
  READY_FOR_REVIEW.zip`, different sha256 because `generated_at` timestamps
  differ between builds) purely to prove the exit code for the record; this
  duplicate was then removed by its exact path with `os.remove` (not a
  glob) so only ONE canonical READY zip remains archived. The FIRST build's
  zip (`...-084541-...`) is the one reported everywhere in this handback as
  the package.
- `bash -c 'bash scripts/make_review_zip.sh --evidence-dir
  .remedy-wt/f258_closure_evidence_CONTROL/remedy-job-evidence-f258-closure-
  control; echo REAL_EXIT=$?'` (the deliberate red control, built from a
  `shutil.copytree` of the real evidence dir with one poisoned absolute-path
  node id appended to run `vr-0001`'s `node_ids`) — REAL_EXIT=0,
  `PACKAGE_STATUS=BLOCKED_EVIDENCE`, zip
  `remedy-review-20260830-084654-BLOCKED_EVIDENCE.zip`, left in place where
  built, not moved, not deleted.
- No `gh pr` command run this round — the Open PR Gate does not apply (no
  PR exists yet on this branch; constraint 0 confirmed `[]` before any
  commit).

## Verification

Every gate below ran with a REAL exit code / measured value in the primary
checkout.

**Constraint 0.** `gh pr list --state open --json number,headRefName,
baseRefName,isDraft` → `[]`. `git rev-parse HEAD` →
`3d2ab8b558de3ea945ef64cd83c7e7eacf850ae0`. `git branch --show-current` →
`feature/f258-self-use-v2`.

**G1 — HYGIENE.** `os.path.exists('.agent/STOP')` → `False` (read before
C0a) and `False` again (read before the zip build, after the C2 push).
`git status --porcelain \| wc -l`: explicitly measured `0` immediately
after C2 and again immediately before the zip build. After C0a, C0b and C1
individually the tree was not separately re-measured with a bare `wc -l`
call, but each subsequent `git status --porcelain` (run immediately before
staging the NEXT file) showed exactly one pending change — the file about
to be committed — and nothing else, which is only possible if the tree was
fully clean immediately after the prior commit; the explicit `0` reading at
C2 and the fully clean tree at every later checkpoint confirm no artifact
was ever left behind. Reported honestly as a reconstructed (not directly
measured) `0` for C0a/C0b/C1 individually.

**G2 — TRANSPORT.** `git show bd6c5766:.agent/authored/f258-r11.md` sha256
`54b5c9629cf9179cb6ed9f15ba369dea294a08336f7d331b03f070e5de1ea1b6`, 21196
bytes; `.remedy-wt/f258-r11/block.md` (reviewer's own scratch original) same
sha256, same 21196 bytes; EQUAL → `True`. `git rev-parse
5095b4fe:.agent/authored/f258-r11.md` and `git rev-parse
5095b4fe:.agent/last_block.md` both print `f6d2957e329bd25927bb1e89be7d6783ae833f4b`
— ONE blob id.

**G3 — THE PLAN AT C1.** `.agent/plan.md` bytes at C1: 1718. PLANF258R11
slice bytes: 1718. Byte-equal → `True`. `wc -l` → 39 (< 50). Count of lines
exactly `## Goal`: 1. Count of lines exactly `## Next Steps`: 1.

**G4 — THE RECORD APPEND AT C2.** Base (`581118e6:.agent/live_review.md`)
1798961 bytes; GATEF258R10 slice 2630 bytes; `base + b"\n" + GATEF258R10 ==
committed` → `True`, committed 1801592 bytes. NEGATIVE CONTROL: one byte
XOR-flipped at offset 1799012 (confirmed inside the appended region, 50
bytes past the separator) → equality `False`, as required. Base is a byte
PREFIX of committed (`committed_now.startswith(base)` → `True`). Committed
blob ends in exactly one `\n` (`endswith(b"\n") and not
endswith(b"\n\n")` → `True`).

**G5 — THE LEDGER AT C2, constraint 7.**
- At `3d2ab8b5`: registered 318 (318 distinct, all distinct → `True`);
  `Done:` 57 lines / 55 distinct ids; `Gate: F\d+ R\d+ — ` count 173; open
  set `len(set(registered) - set(resolved))` = 263.
- At C2 (uncommitted, then committed): registered 318 (UNMOVED, 318
  distinct); `Done:` 57/55 (UNMOVED); `Gate:` count 174 (UP BY ONE); open
  set 263 (UNMOVED).
- Count of `^Gate: F258 R10 — ` at C2: 1.

**G6 — THE EVIDENCE BUNDLE.**
- (a) Unified diff between `EVIDENCESCRIPT` (extracted from `git show
  HEAD:.agent/authored/f009-r33.md`) and the adapted
  `.remedy-wt/f258_evidence.py`: 12 removed lines, 14 added lines, confined
  exactly to `EVIDENCE_DIR`'s folder/job-name line, `BASE`'s value, the
  `runs = [...]` list (5 entries → 7, per the block's exact spec, no `-k`,
  no deselection on any), and the `create_manual_completion_bundle` kwargs
  `job_id`, `job_title`, `prior_job_ids`, `note_prefix`, `review_feature_id`
  (`step_range` and `num_tasks` needed no textual change — same values as
  the template). No other line differs.
- (b) Per run (`run_id` / `selected` / `len(node_ids)` / eq / `passed` /
  `failed` / `skipped` / `deselected` / `test_files` / sorted):
  `vr-0001` 23/23/True/23/0/0/0/[`tests/orchestration/test_self_use_queue.py`]/True;
  `vr-0002` 18/18/True/18/0/0/0/[`tests/orchestration/test_self_use_job.py`]/True;
  `vr-0003` 20/20/True/20/0/0/0/[`tests/orchestration/test_self_use_generator.py`]/True;
  `vr-0004` 7/7/True/7/0/0/0/[`tests/orchestration/test_self_use_runner.py`]/True;
  `vr-0005` 3/3/True/3/0/0/0/[`tests/orchestration/test_self_use_findings.py`]/True;
  `vr-0006` 295/295/True/295/0/0/0/[`tests/docs/test_docs_consistency.py`]/True;
  `vr-0007` 42/42/True/42/0/0/0/[`tests/cli/test_golden_path.py`]/True.
  All expected passes matched exactly (23, 18, 20, 7, 3, 295, 42), failed/
  skipped/deselected 0 everywhere.
- (c) `_unsafe_text` pre-scan over every node id and command in all 7 runs:
  0 rejected. Red control, `_unsafe_text("/home/user/repo/tests/x.py::t")`
  → `"a local absolute path"` (truthy) → correctly True.
- (d) Evidence directory file list (26 entries, `ls -la`):
  `artifact_contract_gate.json`, `change_provenance_gate.json`,
  `commit_execution_gate.json`, `context_strategy.json`,
  `current_change_content_proof.json`, `execution_config.json`,
  `final_job_review.json`, `final_verifier_report.json`,
  `fresh_evidence_gate.json`, `job_report.json`, `job_timeline.json`,
  `manifest_integrity.json`, `manifest.json`, `postmortem_integrity.json`,
  `prompt_trace_summary.json`, `review_commit_chain.json`,
  `review_commit_patches/` (dir), `review_subject.json`,
  `runtime_integration_gate.json`, `scratch_file_guard.json`,
  `target_guard.json`, `task_runs/` (dir), `tasks.json`,
  `token_truth.json`, `verification_tests.json`, `workspace_apply.json`,
  `workspace.diff`. All eight closed-schema gates confirmed present:
  `final_verifier_report.json`, `fresh_evidence_gate.json`,
  `artifact_contract_gate.json`, `change_provenance_gate.json`,
  `manifest_integrity.json`, `postmortem_integrity.json`,
  `commit_execution_gate.json`, `runtime_integration_gate.json`.
- (e) `output_hash == sha256(stdout_summary)`: `True` for all 7 runs
  (vr-0001 through vr-0007).

`create_manual_completion_bundle` result: `job_id=f258-closure`,
`head_commit=49fcc2c645601936d8c426b1eb09523b9b3c7f6f` (= C2 exactly),
`total_passed=408`, `verdict=PASS_WITH_RISKS`, `partition` T001=6/T002=6/
T003=4.

**G7 — THE REVIEW ZIP, constraint 8.**
- (a) READY zip: `remedy-review-20260830-084541-READY_FOR_REVIEW.zip`,
  sha256 `4b4153ad33f01e4d7014e853663f76ac1f36f61ba06687ed0b3c9c5411f12c50`,
  REAL exit 0, `PACKAGE_STATUS=READY_FOR_REVIEW`.
- (b) From `.review_zip_manifest.json` (inside the zip):
  `package_status=READY_FOR_REVIEW`, `ready_gate_matrix.ok=True`,
  `ready_gate_matrix.blocking_reasons=[]` (empty),
  `committed_review_subject.head_commit=49fcc2c645601936d8c426b1eb09523b9b3c7f6f`
  = C2's full sha, exactly.
- (c) RED CONTROL: `PACKAGE_STATUS=BLOCKED_EVIDENCE`,
  `EVIDENCE_AUTHORITATIVE=false`, REAL exit 0 — the exit code did NOT
  distinguish the two builds (both 0); `PACKAGE_STATUS` did. The control
  manifest's `ready_gate_matrix.blocking_reasons` names the poisoned id
  explicitly: `"verification_tests.json field
  verification_tests.runs[0].node_ids[23] carries a local absolute path"`
  and `"verification_tests.json runs[0] node_ids count (24) != selected
  (23)"` and a `final_verifier_report.json` confirmation failure — the
  pipeline caught the corruption on three independent grounds.
- (d) Archived path: `/home/decodeux/Repos/remedy-history/zips/
  remedy-review-20260830-084541-READY_FOR_REVIEW.zip`. Confirmed to exist
  afterward, size 19357817 bytes.
- (e) `git status --porcelain \| wc -l` after all of it: `0`.

**G8 — STRUCTURE AND REMAINING PRECONDITIONS, over `3d2ab8b5..49fcc2c6`.**
- Changeset-minus-range residue, change set WITHOUT `.agent/handoff.md`
  (excluded — C3 writes it after this range ends): `set()` (empty).
- Range-minus-changeset residue, against the FULL 5-path change set:
  `set()` (empty).
- Per-commit insertions (`git diff --numstat` against each commit's own
  parent): `bd6c5766` 342, `5095b4fe` 317, `581118e6` 17, `49fcc2c6` 2. All
  < 500.
- All four commits single-parent (`git log --format='%H %P'
  3d2ab8b5..49fcc2c6`; each line shows exactly one parent hash).
- `<<<SLICE `/`<<<END ` line counts: `.agent/plan.md` at C2: 0;
  `.agent/live_review.md` at C2: 0; `.agent/authored/f258-r11.md` (the
  non-zero control): 4.
- `git ls-files .remedy-wt \| wc -l`: 0. `git ls-files \| grep -c
  remedy-job-evidence`: 0.
- `git diff --numstat 3d2ab8b5..49fcc2c6 -- docs/roadmap/STATUS.md
  README.md scripts/self_use_queue.json
  docs/roadmap/features/T5_F258.md`: no output — all four ABSENT.
- PRECONDITION 3: `from packages.orchestration.integrity_gate import
  run_integrity_checks; result = run_integrity_checks()` →
  `result.passed = True`, `result.fail_count = 0`.

## Authored-text proofs

Two authored slices (PLANF258R11, GATEF258R10) and one whole block
(C0a/C0b) were applied this round, all via disk-to-disk `shutil.copyfile`
or exact byte-reconstruction against the scratch original at
`.remedy-wt/f258-r11/block.md`, never retyped. Both slices were extracted
programmatically by marker-line indexing, never hand-retyped, and (per
constraint 3) re-extracted from the COMMITTED blob `git show
bd6c5766:.agent/authored/f258-r11.md` for every check after C0a.

- C0a/C0b: the whole block, sha256
  `54b5c9629cf9179cb6ed9f15ba369dea294a08336f7d331b03f070e5de1ea1b6`, 21196
  bytes — equal on both the scratch original and the committed blob; C0b's
  two committed blob ids equal (`f6d2957e329bd25927bb1e89be7d6783ae833f4b`).
- PLANF258R11 → `.agent/plan.md`: sha256
  `d1de0b2f02c356a4924224128592cc894db40ec8a160324465ace93dce81fce3`, 1718
  bytes, both sides equal.
- GATEF258R10 → appended to `.agent/live_review.md`: sha256
  `df2688f689627a153d07bf271c926323cedc3c9982e39fd093f2363ed7219396`, 2630
  bytes, proved by whole-file reconstruction AND the negative control.

This block carries no per-slice hash stamped in its own markers (unlike
some prior rounds' blocks) — G2 is the ONE whole-block digest comparison
the block itself orders (its own text: "One digest comparison"), which is
what was run.

## Deviations & assumptions

1. None from the block's ordered commit sequence. Order matched exactly:
   C0a → C0b → C1 (plan.md) → C2 (live_review.md) → push → evidence bundle
   → READY zip → red control → C3 (this handback) → push, with no
   reordering, extra commit, or dropped commit.
2. Guard re-expressions (constraint 5): this session's Bash tool rejected
   several multi-line / multi-statement command forms outright (a
   permission-layer denial, distinct from AGENTS.md's own bash-guard
   validator) — not loops, `$( )`, `${arr[0]}`, `cp`, or env-var assignment
   specifically, but compound single-invocation commands in general. Every
   piece of logic requiring more than one shell statement (slice
   extraction, digest comparison, the append-and-reconstruct arithmetic,
   the negative control, the ledger counts, the residue sets, the red
   control's node-id poisoning) was routed through a standalone Python
   script under the gitignored `.remedy-wt/f258-r11/`, exactly as
   constraint 5 prescribes, and copies used `shutil.copyfile`/
   `shutil.copytree`, never `cp`. Real exit codes were captured with
   `bash -c '<cmd>; echo "REAL_EXIT=$?"'` for both zip builds where the
   exit code itself was part of what had to be reported (the READY
   re-build and the red control); this form was accepted by the guard.
3. `EVIDENCE_DIR` archiving: the block's step 3 assumed the READY zip might
   need `shutil.move`-ing to `/home/decodeux/Repos/remedy-history/zips`.
   In this checkout, `scripts/make_review_zip.sh` already defaults
   `REMEDY_REVIEW_DIR="$HOME/Repos/remedy-history/zips"` (confirmed by
   reading the script) and writes the final zip there directly — there was
   never anywhere else to move it FROM. No `shutil.move` was run; the
   reported archived path is simply where the build placed the file,
   confirmed to exist there afterward. This is recorded here because it is
   a real departure from the step as literally written, even though the
   outcome (a READY zip sitting at that exact absolute path) is identical
   to what the step intended.
4. To obtain a rigorously measured REAL exit code for the READY build (the
   first build was run as a plain, unwrapped Bash invocation and only
   inferred success from its printed success banner), the READY build was
   re-run once, wrapped for exit-code capture, confirming REAL_EXIT=0. This
   produced a second, byte-different zip (`generated_at` timestamps differ
   between builds) which was then deleted by its exact filename via
   `os.remove` — not a glob — so the archive holds exactly one READY
   package. The FIRST build's zip and sha256 are what this handback reports
   throughout; the second build only supplied the exit-code reading.
5. No file under `packages/`, `apps/`, `tests/` or `docs/` was touched, and
   R-0570, R-0736 and R-0757 were not resolved, repaired, or otherwise
   acted upon this round.
6. Nothing else in the block looked wrong. Every stated expectation this
   round's Done-when section named (byte lengths, run counts, gate names,
   `PACKAGE_STATUS` values, the open-set/registered/Done counts) matched
   this worker's own independent measurement exactly.

## Values the next round needs (per the block's Handback section)

- **Evidence job**: `f258-closure`
- **Evidence directory**: `/home/decodeux/Repos/remedy/.remedy-wt/
  f258_closure_evidence/remedy-job-evidence-f258-closure` (gitignored
  scratch, not committed)
- **Package filename**: `remedy-review-20260830-084541-READY_FOR_REVIEW.zip`
- **Package SHA-256**: `4b4153ad33f01e4d7014e853663f76ac1f36f61ba06687ed0b3c9c5411f12c50`
- **Archived path**: `/home/decodeux/Repos/remedy-history/zips/remedy-review-20260830-084541-READY_FOR_REVIEW.zip`
- **Accepted HEAD (C2, full sha)**: `49fcc2c645601936d8c426b1eb09523b9b3c7f6f`

## Next

The next round is the closure commit and the pull request, per
`.agent/plan.md`'s Next Steps: ONE commit flipping F258's `[x]` on
`docs/roadmap/STATUS.md` (using the six values above for the STATUS line's
Evidence-job/package/SHA-256/package-path/accepted-HEAD segments), the
README capability sync, the `scripts/self_use_queue.json` `consumed_by`
edit marking SU-002 consumed by F258, and the final `.agent/` state — then
opening the pull request (not merged this session). This is expected to be
the last round of F258.
