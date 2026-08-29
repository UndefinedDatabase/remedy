# Handback — F257 Self-use track, round 9

## Session

SESSION 3 of feature F257 · round 9 · rounds so far 9

Roster of this session's rounds, this round included: R8, R9. Session 2 ran R4–R7
and ended at `ba28d224`; session 3 opened at R8 and continues with this round.

## Range

Review of `fcf90e85`..HEAD.

## Values the next round needs and cannot re-derive

- Evidence job `f257-closure`
- package `remedy-review-20260829-025133-READY_FOR_REVIEW.zip`
- SHA-256 `c2cf586f90213fc18964ca47c13111111786e8ec3a85c9ec7ad3944252a078fc`
- package path `/home/decodeux/Repos/remedy-history/zips`
- ACCEPTED HEAD `506bbab5d719974f69593087f8d4fa31f45edfb1` (C2)
- base of the packaged review subject `f17b1d0d03e4042df8452b2019b719cbe4704b21`

## Commits

### f8f643c6 docs(f257): save the round 9 block verbatim

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f257-r9.md` | +331/-0 | C0a — the round 9 block saved byte for byte |

### 65fec797 chore(f257): mirror the round 9 block to last_block

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +198/-152 | C0b — same bytes as C0a; one blob id |

### e0b4174c docs(f257): advance the plan to the package round

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +9/-9 | C1 — PLANF257R9 whole-file replacement |

### 506bbab5 docs(f257): book the round 8 gate verdict

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +10/-0 | C2 — GATEF257R8 appended; ACCEPTED HEAD |

### (C3, sha not knowable here) docs(f257): hand back the package round result

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | whole-file rewrite | C3 — this file. A handoff cannot table the commit that writes it (R-0149 pattern), and its own sha is unmeasurable at authoring time, so no numeral is invented for either cell. |

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`.
- `git push origin feature/f257-self-use-track` after C2 → exit 0,
  `fcf90e85..506bbab5`.
- `git push origin feature/f257-self-use-track` after C3 → see the final push line
  below.
- No branch created, no PR created, no merge, no force-push, no history rewrite.

## Artifact-build attempts (AGENTS.md — every attempt, status included)

1. Evidence bundle `f257-closure` — SUCCEEDED. Producer
   `packages.orchestration.job_evidence.create_manual_completion_bundle`, exit 0,
   verdict `PASS_WITH_RISKS`, `total_passed` 373, `authority_count` 10,
   `commit_count` 53, `head_commit` `506bbab5…`. Directory
   `.remedy-wt/f257_closure_evidence/remedy-job-evidence-f257-closure`, never
   committed.
2. Review zip (real) — SUCCEEDED, `PACKAGE_STATUS=READY_FOR_REVIEW`.
3. Review zip (DELIBERATE RED CONTROL, declared per constraint 4) — produced
   `PACKAGE_STATUS=BLOCKED_EVIDENCE` at REAL exit 0, which is the intended
   outcome. Built from a copy of the evidence dir with one fabricated
   absolute-path node id appended; the real bundle was not touched.

No attempt failed for a blocking reason. No attempt was abandoned.

## Verification — one line per gate, real transcripts

G1 HYGIENE — PASS. `os.path.exists('.agent/STOP')` → `False` before C0a and
`False` again before the zip build. `gh pr list …` → `[]`;
`git rev-parse HEAD` → `fcf90e85a22206afe95e019e1bfcff2f9c3b0bfc`;
`git branch --show-current` → `feature/f257-self-use-track`.
`git status --porcelain | wc -l` → 0 after C0a, 0 after C0b, 0 after C1, 0 after
C2, and 0 immediately before the zip build.

G2 TRANSPORT — PASS. `git show f8f643c6:.agent/authored/f257-r9.md` → 22597 bytes,
sha256 `4d995a0a69cac34a38db5a2f03bb4190f3050723b9ef43118bf1673768e9d133`;
`.remedy-wt/f257-r9-block.md` → 22597 bytes, same sha256; **EQUAL: True**. That
original was written before this worker existed, so the reading covers more than
self-consistency; and it covers no emission, because this workflow has none — the
block reached disk as a file the reviewer wrote, not as text a model re-typed.
`git rev-parse 65fec797:.agent/authored/f257-r9.md` and
`git rev-parse 65fec797:.agent/last_block.md` both print ONE blob id
`3305242c55c9db590f9daf3cbcfa57bbb4a36562`.

G3 THE PLAN AT C1 — PASS. `.agent/plan.md` at `e0b4174c` equals PLANF257R9
including the trailing newline: **True**, slice 2177 bytes, blob 2177 bytes.
`wc -l` 42 (under 50). Lines exactly `## Goal`: 1. Lines exactly `## Next Steps`: 1.

G4 THE RECORD APPEND AT C2 — PASS. Reconstruction `fcf90e85` blob + one newline +
GATEF257R8 (constraint 6) equals the C2 blob: **True**. 1405901 + 1 + 3554 =
1409456 = C2 blob length; both sides sha256
`7a964e503d625315829cc4bebd55d56559c997a0cc7d44703c3631078d23a95a`. NEGATIVE
CONTROL: byte flipped at offset 1407679, which the script confirmed lies inside
the appended region [1405902, 1409456) — equality then reads **False**. The
pre-round blob is a byte PREFIX of C2: **True** (1405901 of 1409456). C2 ends in
exactly ONE newline: True.

G5 THE LEDGER AT C2 — PASS, counted under constraint 7 as
`len(set(registered) - set(resolved))`.

| Reading | `fcf90e85` | C2 `506bbab5` |
|---------|-----------|---------------|
| `^- R-\d+ — ` lines | 297, all DISTINCT True | 297, all DISTINCT True |
| `^Done: R-\d+ — ` lines | 44 | 44 |
| DISTINCT ids among them | 42 | 42 |
| `^Landed: R-` | 11 | 11 |
| `^Gate: F\d+ R\d+ — ` | 113 | 114 |
| OPEN SET | 255 | 255 |

`^Gate: F257 R8 — ` at C2: 1. Registered UNMOVED at 297, `Done:`/`Landed:`
UNMOVED, `Gate:` 113 → 114, open set UNMOVED at 255 — a round that registers
nothing and resolves nothing.

G6 THE EVIDENCE BUNDLE — PASS.

(a) `EVIDENCESCRIPT` was extracted from the COMMITTED blob
`HEAD:.agent/authored/f009-r33.md` (6675 bytes, 148 lines), copied with
`shutil.copyfile`, and only the listed values changed. `diff -u` reports 14
removed and 13 added lines, in exactly four hunks, and each changed line is one
of the listed values:
- `EVIDENCE_DIR` line: `"f009_closure_evidence", "remedy-job-evidence-f009-closure"`
  → `"f257_closure_evidence", "remedy-job-evidence-f257-closure"` (1 line).
- `BASE = "ce49348b…"` → `BASE = "f17b1d0d03e4042df8452b2019b719cbe4704b21"`
  (1 line), measured with `git merge-base main HEAD`; 40 characters, and the
  template's own `assert len(BASE) == 40` passed.
- the `runs = [...]` list: 5 template lines removed, 4 added — `vr-0001`
  test_self_use_queue.py 18, `vr-0002` test_self_use_job.py 18, `vr-0003`
  test_docs_consistency.py 295, `vr-0004` test_golden_path.py 42; no `-k` and no
  deselection on any of them.
- the `create_manual_completion_bundle` kwargs: 7 lines — `job_id`, `job_title`,
  `step_range`, `prior_job_ids`, `num_tasks`, `note_prefix`, `review_feature_id`.
Everything else — the double path scrub in `_tail`, node ids from
`--collect-only`, the `len(node_ids) == selected` assert, the sorted
`test_files`, the `_unsafe_text` pre-scan with its red control, and the
`OUTPUT_HASH` re-derivation — is byte for byte the template's.

(b) Per verification run, from the written `verification_tests.json`:

| run_id | selected | len(node_ids) | equal | passed | failed | skipped | deselected | test_files | sorted |
|--------|----------|---------------|-------|--------|--------|---------|------------|-----------|--------|
| vr-0001 | 18 | 18 | True | 18 | 0 | 0 | 0 | `['tests/orchestration/test_self_use_queue.py']` | True |
| vr-0002 | 18 | 18 | True | 18 | 0 | 0 | 0 | `['tests/orchestration/test_self_use_job.py']` | True |
| vr-0003 | 295 | 295 | True | 295 | 0 | 0 | 0 | `['tests/docs/test_docs_consistency.py']` | True |
| vr-0004 | 42 | 42 | True | 42 | 0 | 0 | 0 | `['tests/cli/test_golden_path.py']` | True |

(c) `build_review_manifest._unsafe_text` pre-scan over every node id and every
command: 377 strings scanned, **0 rejected**. Its red control on the fabricated
id `/home/user/repo/tests/x.py::t` returns the truthy reason string
`'a local absolute path'` (`bool` **True**) — the scanner rejects something, so
the zero above is a reading and not a silence.

(d) Gate files the producer wrote into the evidence directory (27 entries):
`artifact_contract_gate.json`, `change_provenance_gate.json`,
`commit_execution_gate.json`, `context_strategy.json`,
`current_change_content_proof.json`, `execution_config.json`,
`final_job_review.json`, `final_verifier_report.json`, `fresh_evidence_gate.json`,
`job_report.json`, `job_timeline.json`, `manifest.json`,
`manifest_integrity.json`, `postmortem_integrity.json`,
`prompt_trace_summary.json`, `review_commit_chain.json`, `review_commit_patches/`,
`review_subject.json`, `runtime_integration_gate.json`, `scratch_file_guard.json`,
`target_guard.json`, `task_runs/`, `tasks.json`, `token_truth.json`,
`verification_tests.json`, `workspace.diff`, `workspace_apply.json`. All eight
closed-schema gates PRESENT: `final_verifier_report`, `fresh_evidence`,
`artifact_contract`, `change_provenance`, `manifest_integrity`,
`postmortem_integrity`, `commit_execution`, `runtime_integration` — **True** for
each and True for the conjunction.

(e) `output_hash == sha256(stdout_summary)` EXACTLY: vr-0001 True, vr-0002 True,
vr-0003 True, vr-0004 True.

G7 THE REVIEW ZIP, read under constraint 8 — PASS.

(a) `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f257_closure_evidence/remedy-job-evidence-f257-closure`
— REAL exit code **0**, `PACKAGE_STATUS=READY_FOR_REVIEW`, filename
`remedy-review-20260829-025133-READY_FOR_REVIEW.zip`, SHA-256
`c2cf586f90213fc18964ca47c13111111786e8ec3a85c9ec7ad3944252a078fc` (independently
recomputed over the archived file, identical to the value the script printed),
3349 members, 10 authoritative.

(b) From `.review_zip_manifest.json` as packaged inside the zip:
`package_status` `READY_FOR_REVIEW`; `ready_gate_matrix.ok` **True**;
`ready_gate_matrix.blocking_reasons` **`[]`** — empty;
`committed_review_subject.head_commit`
`506bbab5d719974f69593087f8d4fa31f45edfb1`, which EQUALS C2's full sha
`506bbab5d719974f69593087f8d4fa31f45edfb1`;
`committed_review_subject.base_commit` `f17b1d0d03e4042df8452b2019b719cbe4704b21`.
Gate verdicts in the matrix: artifact_contract PASS, change_provenance PASS,
commit_execution NEEDS_HUMAN_APPROVAL, final_verifier_report PASS_WITH_RISKS,
fresh_evidence PASS, manifest_integrity ok=true, postmortem_integrity ok=true,
runtime_integration PASS.

(c) THE RED CONTROL — `PACKAGE_STATUS=BLOCKED_EVIDENCE`,
`EVIDENCE_AUTHORITATIVE=false`, REAL exit code **0**, file
`remedy-review-20260829-025231-BLOCKED_EVIDENCE.zip`, sha256
`816f494b6e0e29d453ba5d6ec6751f3f09af99a1c471a812e87b65631d238c1f`. Stated
plainly: **the exit code did not distinguish the two builds — both were 0 — and
the status did.** Reading the zip green off an exit code would have passed a
BLOCKED_EVIDENCE package here.

(d) The READY zip is at
`/home/decodeux/Repos/remedy-history/zips/remedy-review-20260829-025133-READY_FOR_REVIEW.zip`;
the file EXISTS there after the control build, size **18146705 bytes**. The
archive directory is `/home/decodeux/Repos/remedy-history/zips`.

(e) `git status --porcelain | wc -l` after all of it: **0**. Both artifacts are
gitignored and neither dirtied the tree.

G8 STRUCTURE AND THE REMAINING PRECONDITIONS — PASS, over `fcf90e85..506bbab5`.
Range paths: `.agent/authored/f257-r9.md`, `.agent/last_block.md`,
`.agent/live_review.md`, `.agent/plan.md`. The path EXCLUDED from the
changeset-minus-range computation is **`.agent/handoff.md`**, which C3 writes
after this range ends. changeset-minus-range residue (change set without that one
path): **empty**. range-minus-changeset residue, computed against the FULL change
set: **empty**. Insertions and parents: C0a `f8f643c6` 331, single-parent; C0b
`65fec797` 198, single-parent; C1 `e0b4174c` 9, single-parent; C2 `506bbab5` 10,
single-parent — each under 500. Delimiters at C2: `.agent/plan.md` `<<<SLICE ` 0 /
`<<<END ` 0; `.agent/live_review.md` 0 / 0; non-zero control
`.agent/authored/f257-r9.md` 2 / 2. `git ls-files .remedy-wt | wc -l` **0**;
`git ls-files | grep -c remedy-job-evidence` **0** — the evidence dir is not
committed. `git diff --numstat` over the range for `docs/roadmap/STATUS.md`,
`README.md`, `scripts/self_use_queue.json` and
`docs/roadmap/features/T5_F257.md`: all four **ABSENT**. PRECONDITION 3 —
`run_integrity_checks()` returns an `IntegrityGateResult`; `result.passed`
**True**, `result.fail_count` **0**.

## Authored-text proofs

- `PLANF257R9` and `GATEF257R8` were both extracted from the COMMITTED blob
  `65fec797:.agent/authored/f257-r9.md` by their `<<<SLICE`/`<<<END` marker
  lines, never from the prompt text (constraint 3). No delimiter line reached any
  target file — G8 measures 0/0 in both targets against a 2/2 control.
- Disk-to-disk: the committed `.agent/authored/f257-r9.md` blob is byte-identical
  to the reviewer's own `.remedy-wt/f257-r9-block.md` (G2, 22597 bytes, equal
  sha256), so both applied slices are byte-identical to the authored source by
  construction, and G3 and G4 confirm each on its target.
- The evidence script's template slice `EVIDENCESCRIPT` was likewise extracted
  from the committed blob `HEAD:.agent/authored/f009-r33.md`.

## Deviations & assumptions

1. **The archive move was a no-op and `shutil.move` was not called.**
   `scripts/make_review_zip.sh` writes its output directly into
   `REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips`, which is
   exactly the destination the block's step 3 orders. The READY zip was therefore
   already at the ordered absolute path when the build finished; moving a file
   onto itself would have been the only way to execute the literal instruction.
   The recorded archived path is unchanged and is
   `/home/decodeux/Repos/remedy-history/zips`; existence and size at that path are
   reported under G7(d).
2. **`blocking_reasons` is not a top-level manifest key.** G7(b) orders it read
   from `.review_zip_manifest.json`; the manifest has no top-level
   `blocking_reasons`. The field exists at `ready_gate_matrix.blocking_reasons`
   and reads `[]`, the expected empty. Reported from where it actually lives
   rather than reported as absent.
3. **Guard re-expressions (constraint 5).** No shell loop, `$( )`, `${arr[0]}`,
   `cp` or environment-variable assignment was used. All multi-step work was
   routed through scratch scripts under the gitignored `.remedy-wt/`:
   `f257_slice.py` (slice extraction and application), `f257_g4g5.py`,
   `f257_g6.py`, `f257_g7b.py`, `f257_g8.py`, `f257_redctl.py`,
   `f257_evidence.py`. Every file copy used `shutil.copyfile`; the ONE directory
   copy the red control needs used `shutil.copytree`, the directory analogue,
   because `shutil.copyfile` cannot copy a tree. Real exit codes were captured
   with `bash -c '<cmd>; echo "REAL_EXIT=$?"'` throughout. No f-string carries a
   backslash; the ledger regexes are hoisted into named variables in
   `f257_g4g5.py`.
4. **The red-control zip was left where it was built**, at
   `/home/decodeux/Repos/remedy-history/zips/remedy-review-20260829-025231-BLOCKED_EVIDENCE.zip`,
   per the block's step 4. Nothing was deleted by glob. The only path removed
   this round was the red-control evidence copy's own destination directory
   `/home/decodeux/Repos/remedy/.remedy-wt/f257_redcontrol_evidence/remedy-job-evidence-f257-redcontrol`,
   removed by exact path inside `f257_redctl.py` before `copytree` recreated it;
   it did not exist at the time, so the branch did not execute.
5. **No departure from the block's ordered commit sequence.** C0a, C0b, C1, C2,
   push, artifacts, C3 — in that order, no extra commit, none dropped, none
   reordered.
6. **`vr-0001` and `vr-0002` share an `output_hash` prefix** (`11a0325b…`). Both
   suites end in an identical trimmed tail (`18 passed`), so the preimages are
   equal and the digests must be. Noted so a reader does not read it as a copied
   value; G6(e) verified each against its own `stdout_summary`.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block to `.agent/authored/f257-r9.md` | done | `f8f643c6` |
| C0b mirror to `.agent/last_block.md` | done | `65fec797` |
| C1 advance `.agent/plan.md` | done | `e0b4174c` |
| C2 book the F257 R8 verdict | done | `506bbab5`, ACCEPTED HEAD |
| push at C2 | done | exit 0, `fcf90e85..506bbab5` |
| evidence bundle | done | job `f257-closure` |
| review zip | done | READY_FOR_REVIEW |
| red control | done | BLOCKED_EVIDENCE at exit 0, deliberate |
| archive the READY zip | done | already at the ordered path; deviation 1 |
| C3 rewrite `.agent/handoff.md` | done | this commit |
| G1 hygiene | done | green |
| G2 transport | done | green, EQUAL |
| G3 the plan at C1 | done | green, True |
| G4 the record append at C2 | done | green, True; control False |
| G5 the ledger at C2 | done | green, 297/255 unmoved, Gate 113→114 |
| G6 the evidence bundle | done | green, all five sub-readings |
| G7 the review zip | done | green, READY_FOR_REVIEW |
| G8 structure and preconditions | done | green, both residues empty |

Every gate was executed and every reading above is a real one. No gate was red.

## Open findings

255, unchanged from `fcf90e85` — this round registered no id and resolved none.

## Next

The closure commit: in ONE commit, the `[x]` flip on line 85 of
`docs/roadmap/STATUS.md`, the README capability sync that may never disagree with
it, the `scripts/self_use_queue.json` `consumed_by` edit marking SU-001 consumed
by F257, and the final `.agent/` state — then open the pull request, which is NOT
merged in this session.
