# Handback — F275 round 108

## Session

`SESSION 35 of feature F275 · round 108 · rounds so far 108`

## Range

Review of `7040f192`..`HEAD`: five commits (C0a, C0b, C1, C2, C3), plus this handback commit C4. `.agent/STOP` was
ABSENT at all three readings constraint 2 orders (before C0a, before C2, before C4): `ls /home/decodeux/Repos/remedy/.agent/STOP`
exit 2 each time, "No such file or directory".

**CLOSURE ROUND A IS DONE: THE PACKAGE BUILT `READY_FOR_REVIEW`.** The rotation script moved 23 gate records and 26
finding pairs, and it left its own open-findings count at 87 before and after. The evidence job at C2 `d285f47a` returned
`PASS_WITH_RISKS`. The review package built with `REVIEW_SUBJECT_ALIGNMENT=PASS` and `EVIDENCE_AUTHORITATIVE=true`.
The round's one serial full-suite run exited **0**: `18442 passed, 23 skipped, 1 warning in 1350.62s (0:22:30)`, with no bad node.

## STATUS values for closure round B

These are spelled exactly as the tools printed them:

    Evidence job   f3fff86c9b2c58a9
    package        remedy-review-20260914-230931-READY_FOR_REVIEW.zip
    SHA-256        e18ab493640adf6e5e82b72dea9c59ee9469b730d75085c533645e29a1cd1da0
    package path   /home/decodeux/Repos/remedy-history/zips
    accepted HEAD  d285f47a8a28f1868da9078ed60834752eeec3a8

The package `remedy-review-20260914-230148-READY_FOR_REVIEW.zip` in the same directory is the reviewer's dry run from
the throwaway head `847335e2`. It is NOT this closure's package. I left it untouched, and it is still listed there.

## Commits

### b407a389 F275 R108 C0a: save the round 108 block as authored text

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r108.md` | +216 / -0 | the block as received. Before copying, I checked its sha256 `0aec9602…2058a6` (16739 bytes) against the digest received |

### 3358c7c7 F275 R108 C0b: mirror the round 108 block into the last-block state file

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +166 / -172 | the same bytes, the mirror |

### 68ecd1ec F275 R108 C1: book round 107's PASS with the recurrences of R-0784 and R-0838, and plan closure round A

This is the FIRST SUBSTANTIVE COMMIT.

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +12 / -0 | slice RECORD108 appended, 3600 bytes: `Gate: F275 R107` VERDICT PASS, plus the recurrences of R-0784 and R-0838 |
| `.agent/plan.md` | +22 / -23 | slice PLAN108, a full replacement: 2417 bytes, 40 lines |

### d285f47a F275 R108 C2: rotate the live-review ledger with the rotation script, 23 gate records and 26 finding pairs moved to the archive

This is THE ACCEPTED HEAD.

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +0 / -162 | the records the script moved out |
| `.agent/live_review_archive.md` | +162 / -0 | the same records, appended byte-verbatim by the script |

### aa36e9cf F275 R108 C3: commit the transcript of the round's one full-suite run, exit 0 with no bad node

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r108-suite.txt` | +2 / -0 | `EXIT=0` and the summary line. There is no bad node, so the file has 2 lines (65 bytes) |

### C4 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS | constraint 10 runs nothing after C4, and a handback cannot read the commit that writes it. C4's numbers are the reviewer's |

Every cell above comes from `git show --numstat`. I compared each cell against G6's rows:

- C0a +216 -0, 1 path
- C0b +166 -172, 1 path
- C1 +34 -23, 2 paths
- C2 +162 -162, 2 paths
- C3 +2 -0, 1 path

Every sum and every path count agrees.

## External actions

| Command | Outcome |
|---|---|
| `git push -u origin feature/f275-one-world-completion-part-three` after C1 | exit 0, `7040f192..68ecd1ec`, carrying C0a, C0b and C1 |
| `git push origin feature/f275-one-world-completion-part-three` after C2 | exit 0, `68ecd1ec..d285f47a` |
| the same after C3 | exit 0, `d285f47a..aa36e9cf` |
| the same after C4 | runs after this commit. Its result is in the round report |
| `bash scripts/make_review_zip.sh --evidence-dir …/r108w/evidence-423ba1f9` | exit 0, `READY_FOR_REVIEW`. The package was written to `/home/decodeux/Repos/remedy-history/zips/` and was not moved, renamed or deleted |
| `gh` / `remedy` / worktrees / branches | NOT RUN. No pull request, no merge, no force-push, no history rewrite, no branch or worktree created or deleted |

## Verification

The scripts and their raw outputs are under `.remedy-wt/r108w/`, not committed. Each exit code is the real process
return code that the Bash tool reported.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport and bookkeeping | after C1 `68ecd1ec` | `g1.py` 0 | `f275-r108.md` at C0a has sha256 **equal** to the received digest (16739 bytes). `last_block.md` at C0b is **byte-identical** to it. Slices FOUND: **2** (PLAN108 2417 bytes, RECORD108 3600), each **matching** its BEGIN-marker sha256. `plan.md` at C1 **equals** PLAN108: **40** lines, `## Goal` **1**, `## Next Steps` **1**. `live_review.md`: the base blob at `7040f192` is 1195998 bytes, and that blob followed by RECORD108 (3600) **equals** C1's file (1199598). `^Gate: F\d+ R\d+ — ` reads **129** at `7040f192` and **130** at C1; `Gate: F275 R107 — ` reads **1**. The open set by distinct id reads **89** at both, with **identical membership** |
| G2 the rotation | at C2 `d285f47a` | `rotate_live_review.py` 0 (stderr empty); `g2.py` 0 | See the full stdout below. The script's count is **87 → 87**. The distinct-id open set is **89 → 89**, with **identical membership**. `R-0784`, `R-0809`, `R-0838` and `R-0880` each have **1** registration line in the ledger at C2, and each is still open. The archive's bytes at C1 (2701739) are an **exact prefix** of its bytes at C2 (2948965). `git show --numstat` of C2 names **exactly** `.agent/live_review.md` (0/162) and `.agent/live_review_archive.md` (162/0): **162 insertions** |
| G3 the evidence job | after C2, before the suite | `evidence.py` 0 | See the G3 readings below |
| G4 the package and the preconditions | after G3, before the suite | `zip_launch.py` 0 (script 0); `g4.py` **1**, then `g4_manifest.py` 0 (Deviation 1) | See the G4 readings below |
| G5 the suite | after SPEC Z; transcript reading at C3 `aa36e9cf` | pytest **0**; `build_transcript.py` 0; `cmp` 0 | Summary `18442 passed, 23 skipped, 1 warning in 1350.62s (0:22:30)`, with a wall time of 1352.5 s. Bad nodes: **0**. No line starts with `FAILED ` or `ERROR `, no line starts with `E   `, and stderr was 0 bytes. So no alone re-run was owed, and **no bad node is left after removing FLAKY ones**. At C3, the committed transcript (65 bytes) **equals** the file rebuilt from the saved stdout |
| G6 tree, path set, cap | after C3 `aa36e9cf` | `g6.py` 0 | `git status --porcelain` printed `''`. `git worktree list`: **1** row. Changed paths `7040f192..aa36e9cf`: **6**, which are the Bundle's paths other than `handoff.md`. **MISSING none, EXTRA none**. Rows: C0a `b407a389` +216 -0, 1 path; C0b `3358c7c7` +166 -172, 1; C1 `68ecd1ec` +34 -23, 2; C2 `d285f47a` +162 -162, 2; C3 `aa36e9cf` +2 -0, 1. **Commits reaching 500 insertions: none** |

### G2: the script's full stdout

```
gate records moved: 23
finding pairs moved: 26 (52 records)
old ledger size: 1199598 bytes
new ledger size: 952372 bytes
old archive size: 2701739 bytes
new archive size: 2948965 bytes
open findings before: 87
open findings after: 87
written: /home/decodeux/Repos/remedy/.agent/live_review.md and /home/decodeux/Repos/remedy/.agent/live_review_archive.md
```

Every figure matches the reviewer's dry run: 23 gate records, 26 finding pairs, a ledger of 1199598 → 952372 bytes and
an archive of 2701739 → 2948965 bytes. The script's own count (87) uses its line formula: registration lines minus
`Done:` lines. The distinct-id reading (89) is a different measure, and each one is identical before and after.

### G3 readings

- **E1.** HEAD `d285f47a8a28f1868da9078ed60834752eeec3a8` is C2. `rev-list --ancestry-path a5bf8949..C2` gives **934**,
  and plain `rev-list` gives **934**, so they are **EQUAL**. The base is an ancestor of `origin/main`: **True**.
  `git status --porcelain`: `''`. `git worktree list` showed 1 row beforehand.
- **E2.** I ran `python3 -B -m pytest tests/docs/ -q -p no:randomly` and its `--collect-only`, from the primary root,
  with `PYTHONPATH`, `REMEDY_PROJECT` and `REMEDY_DATA_DIR` popped. collect-only exited 0. The run exited **0**, and
  its last line was `306 passed in 0.50s`. Entry: `exit_code` **0**, `passed` **306**, `failed` 0, `skipped` 0,
  `deselected` 0, `selected` **306**. `len(node_ids)` is **306**, and `len(test_files)` is **3**:
  `tests/docs/test_docs_consistency.py`, `tests/docs/test_named_source_paths.py`, `tests/docs/test_vocabulary.py`.
  `duration_seconds` is 0.72, and `output_hash` equals sha256 of `stdout_summary`. The pre-scan read 309 strings with
  `_unsafe_text`, loaded by file path, and returned **0 flags**. For information only: the command and
  `stdout_summary` also read `None`, and the red control `/home/user/repo/tests/x.py::t` read `a local absolute path`.
- **E3.** `evidence_dir` is `/home/decodeux/Repos/remedy/.remedy-wt/r108w/evidence-423ba1f9`, which was fresh.
  `timestamp` and `generated_at` are both `2026-09-14T21:08:19Z`. The producer's returned summary, IN FULL:
  `{"authority_count": 401, "commit_count": 934, "head_commit": "d285f47a8a28f1868da9078ed60834752eeec3a8", "job_id": "f3fff86c9b2c58a9", "manual_completion": true, "operator_attested_tasks": ["T001", "T002", "T003"], "partition": {"T001": 134, "T002": 134, "T003": 133}, "total_passed": 306, "verdict": "PASS_WITH_RISKS"}`.
  **job_id `f3fff86c9b2c58a9`, verdict `PASS_WITH_RISKS`.** `git status --porcelain` after the run: `''`.

### G4 readings

- **The script's full stdout** (exit **0**, stderr empty):

```
UNCHANGED: runtime_integration_gate.json — rebuilt from source; identical to existing
Evidence refresh completed for staged copy.
Observability index generated from staged bytes: evidence/current/self_run_observability_index.json
{"member_count": 5058, "authoritative_count": 401, "symlink_count": 0, "tombstone_count": 122, "final_path": "/home/decodeux/Repos/remedy-history/zips/remedy-review-20260914-230931-READY_FOR_REVIEW.zip", "final_sha256": "e18ab493640adf6e5e82b72dea9c59ee9469b730d75085c533645e29a1cd1da0", "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW", "evidence_authoritative": true, "review_subject_alignment": "PASS", "manifest_sha256": "a04b3b8b92c6e8f8e3c8ccfbd9cc159279543ce0d9b12a2d06d77931c0a000e4"}

============================================
REVIEW_PACKAGE_CREATED=true
PACKAGE_STATUS=READY_FOR_REVIEW
PACKAGING_CWD=/home/decodeux/Repos/remedy
EVIDENCE_DIR=/home/decodeux/Repos/remedy/.remedy-wt/r108w/evidence-423ba1f9
REVIEW_SUBJECT_ALIGNMENT=PASS
EVIDENCE_AUTHORITATIVE=true
REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260914-230931-READY_FOR_REVIEW.zip
============================================

ZIP CREATED AND READY FOR FINAL REVIEW

34M	/home/decodeux/Repos/remedy-history/zips/remedy-review-20260914-230931-READY_FOR_REVIEW.zip
Included files: 5058
Branch: feature/f275-one-world-completion-part-three
Commit: d285f47a8a28f1868da9078ed60834752eeec3a8
Evidence: evidence/current/
```

- **Status.** `PACKAGE_STATUS` **READY_FOR_REVIEW**, `REVIEW_SUBJECT_ALIGNMENT` **PASS**, `EVIDENCE_AUTHORITATIVE` **true**.
- **The file.** Filename `remedy-review-20260914-230931-READY_FOR_REVIEW.zip`. The SHA-256 as printed is
  `e18ab493640adf6e5e82b72dea9c59ee9469b730d75085c533645e29a1cd1da0`, and as recomputed from the file it is the same
  value: they **agree**. Directory `/home/decodeux/Repos/remedy-history/zips`.
- **Counts.** `member_count` **5058**, `authoritative_count` **401**, `tombstone_count` **122**.
- **The subject.** Read OUT of the package's `.review_zip_manifest.json`, `committed_review_subject` has `base_commit`
  `a5bf894946ab6de053a4232109d6341a63533768` (**the fork point**) and `head_commit`
  `d285f47a8a28f1868da9078ed60834752eeec3a8` (**C2**). The same manifest reads `packaged_evidence_job_id`
  `f3fff86c9b2c58a9`, and `packaging_warnings` is `[]`.
- **The two test runs.** Both ran from the primary root. `python3 -B -m pytest tests/docs/ -q` exited **0**,
  `306 passed in 0.51s`. `python3 -B -m pytest tests/cli/test_golden_path.py -q` exited **0**, `42 passed in 18.99s`.
- **The integrity checks.** `run_integrity_checks()` gave `.passed` **True** and `.fail_count` **0**. The check
  `high_blockers_open` reads, verbatim: name `'high_blockers_open'`, status `<IntegrityStatus.PASS: 'pass'>`, message
  `'no open blocker/high findings'`.
- **The ledger's open High findings, which I read myself.** At C2, the ledger has 89 open ids by distinct id. Four
  registrations carry the severity `High`: **R-0803, R-0804, R-0806, R-0807**. So the check's message is false against
  the ledger, which is what R-0648 records.

Constraint 9, measured on the committed block: **216** lines TOTAL, and 52 slice body lines (PLAN108 40 + RECORD108 12),
so **164** lines are PROSE, as stated. No line is a run of a single repeated character. The three STEP and SLICE header
lines (1, 158, 202) carry only two-character box-drawing rules.

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f275-r108.md`, `.agent/last_block.md` | sha256 `0aec9602…`, **equal** to the received digest at C0a. The mirror is byte-identical at C0b (G1) |
| PLAN108 | `.agent/plan.md` | **equal** to the slice at C1, 2417 bytes. The marker `17529c4d…` matched |
| RECORD108 | `.agent/live_review.md` | post **equals** the 1195998-byte base blob followed by the 3600-byte slice. The marker `260a2102…` matched |

NO SLICE WAS EDITED. The rotation was run by the script and not by hand.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a / C0b | done | two commits, as the Bundle orders |
| C1 bookkeeping (PLAN108, RECORD108) | done | first substantive commit |
| C2 rotation | done | run by the script; its own commit of the two paths; the accepted head |
| SPEC E evidence job | done | job `f3fff86c9b2c58a9`, `PASS_WITH_RISKS`; nothing committed |
| SPEC Z review package | done | `READY_FOR_REVIEW`; not moved |
| SPEC S suite / C3 | done | exit 0, no bad node |
| C4 handback | done | this commit |
| G1 · G2 · G3 · G4 · G5 · G6 | done | readings above. G4's first script run exited 1 on my own lookup (Deviation 1) |

## Deviations & assumptions

1. **G4'S FIRST SCRIPT EXITED 1 BECAUSE OF MY OWN LOOKUP, NOT BECAUSE OF THE PACKAGE.**
   - What failed: `g4.py` searched the zip for a manifest only under the basenames `review_manifest.json`,
     `manifest.json` and `REVIEW_MANIFEST.json`. The package's manifest is `.review_zip_manifest.json`, so the script
     printed "no manifest with committed_review_subject found" and exited 1.
   - What still came from that run: its other readings are the ones reported above (the SHA-256 recomputation, both
     test runs and the integrity checks), and each of them passed.
   - The fix: a second probe, `g4_manifest.py`, read every JSON member that carries the key. It found
     `.review_zip_manifest.json` with the fork point and C2, and it exited 0.
   - What did not happen: nothing was rebuilt, and no second package was made.
2. **HOW THE COMMANDS WERE LAUNCHED.**
   - The Bash guard rejects `$?` and pipes into `tee`, so each command ran through a Python launcher. The launcher
     ran the command with `cwd` set to the primary root and saved its stdout, stderr and return code under
     `.remedy-wt/r108w/`. The rotation (`rotate_launch.py`), the evidence job (`evidence.py`) and the package
     (`zip_launch.py`) all ran this way.
   - The suite ran detached (`suite_launch.py` → `suite_wait.py`, `start_new_session=True`), and I polled with `sleep`.
   - STOP was read with `ls`, which exited 2.
3. **EVIDENCE DETAILS THE SPEC LEAVES OPEN.**
   - The evidence directory is named `evidence-423ba1f9`, with a random suffix, to guarantee a fresh directory.
   - The timestamp is written with a `Z` suffix.
   - The entry's `command` is the argv joined by spaces. It does not state that the environment variables were removed,
     although they were.
   - `duration_seconds` is the launcher's wall measurement around the run (0.72 s), not pytest's own `0.50s`.
4. **G4'S TWO TEST RUNS USED THE SESSION ENVIRONMENT.** The block orders no environment for them.
5. **A STRAY EMPTY SCRATCH DIRECTORY.** I created `.remedy-wt/r108w/c3/` by mistake, and it is empty. It is ignored and
   untracked. I left it in place because constraint 6 deletes nothing.
6. **PUSH GROUPING.** C0a and C0b travelled with the push after C1. The Bundle's commit sequence is unchanged.
7. **THE SHELL'S STARTING DIRECTORY.** The session's working directory was `.remedy-wt/r101`, which is the reviewer's
   scratch. No command ran from it and nothing under it was opened. Every git command used
   `git -C /home/decodeux/Repos/remedy`.

## Next

The reviewer books round 108's verdict. Then comes CLOSURE ROUND B of `.agent/plan.md`: the closure commit carries the
STATUS `[x]` line authored from the five values above, the README sync and `SU-014`'s `consumed_by` set to `F275`. After
that commit comes the pull request.

Operator questions open: 1

Context self-assessment: this worker's context is comfortable, and nothing in the round was cut short.
