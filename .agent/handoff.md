# Handback — F315 "The loop runs through the adapter," round 5

## Session

SESSION 1 of feature F315 · round 5 · rounds so far 5. Context self-assessment: this session
continued directly from round 4's handback, booked round 4's verdict and registered R-1442, ran
the staging reclaim preview (nothing reclaimable), ran the evidence job exactly once (green) and
the review package exactly once (`READY_FOR_REVIEW`), carrying forward only the closing round.

**Fortschritt:** ~95 % (everything but the closing round is done) — Schätzung.

## Range

Review of `086e1b933`..`f00589e35`.

## Commits

### 7ae89d510 F315 R5 C1: book round 4, register R-1442, the plan, the block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f315-r5.md` | +124/-0 | NEW FILE; byte copy of this round's block, `block.md` |
| `.agent/live_review.md` | +4/-0 | books round 4's VERDICT PASS and registers R-1442 from the self-use run's two defect strings |
| `.agent/plan.md` | +4/-5 | rewritten for round 5's current step (the staging reclaim, evidence job and review package) and the closing-round next step |

All three paths are byte copies of the reviewer's prepared `c1-*` files; gate 1's `verify.py`
confirms each equality (see Verification).

### f00589e35 F315 R5 C2: the evidence script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f315-r5-create_f315_evidence.py` | +312/-0 | NEW FILE; byte copy of the reviewer's prepared evidence-job script, run once in A2 |

Byte copy of the reviewer's prepared `c2-*` file; gate 1's `verify.py` confirms the equality.

### this commit — F315 R5 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | n/a (self-reference; R-0149 pattern) | this handback, rewritten per `docs/agents/handback_template.md` |

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `7ae89d510`, three paths, byte-equal to prepared files |
| C2 | done | `f00589e35`, one path, byte-equal to prepared file |
| A1 | done | staging reclaim preview: "Reclaimable: nothing", would free 0 B in 0 paths; no candidate listed so `--apply` was skipped |
| A2 | done | evidence job `f315r5e1001` via `launch.py`/`wait.py`, exit 0, wall 1156.3s; all expected readings matched |
| A3 | done | review package via `launch.py`/`wait.py`, exit 0, wall 8.4s; `PACKAGE_STATUS=READY_FOR_REVIEW` |
| C3 | done | this commit |
| R-1442 | done | registered in C1 from round 4's self-use run defect strings, owner F314 |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` every line `True`, `C3` read `absent` (as expected before this commit), `ALL True` |
| Gate 2 | done | A2 and A3 both exited 0 with every expected reading matched |
| Gate 3 | done | `integrity check --json` `fail_count` 0; open finding ids the required twelve |

## External actions

- `git push origin feature/f315-loop-through-adapter` — run after C2, carrying `7ae89d510` and
  `f00589e35`; succeeded on the first attempt (`086e1b933..f00589e35`).
- `git push origin feature/f315-loop-through-adapter` — to run after this handback's own commit,
  carrying the handback commit; see the reply for the push's own result.
- No pull request opened (the block orders none; the Open PR Gate found `[]` before this round
  started).
- No worktree created or removed by this session. One scratch directory was used,
  `.remedy-wt/f315-r5-worker/`, holding only python helper scripts (digest checks, byte copies,
  gate readings) and the two command logs/exit files `launch.py` wrote; `.remedy-wt/f315-r5/`
  (the reviewer's prepared tree) was only read, never written.

## Verification

Gate order per the block.

1. After C2: `git status --porcelain` → empty.
   `python3 .remedy-wt/f315-r5/prep/verify.py .` → every line `True`: both commits' single-parent
   checks, the new-subject check (`2 of 2`), the branch check, each commit's exact-path-set check
   and every per-path byte-equality check against the prepared `c1-*`/`c2-*` files, `C3` →
   `absent` (as the block states, before this commit exists), "the saved block equals `block.md`"
   `True`, final line `ALL True`.

2. A2, the evidence job (`launch.py evidence .remedy-wt/f315-r5-worker` then
   `wait.py evidence .remedy-wt/f315-r5-worker 50`, exit 0 on the first wait call, wall 1156.3s):
   ```
   head f00589e3529a23cc58d8b655e35d86ec661ad123
   ancestry-path count 21
   plain count 21
   collected node ids 12687, deselected 251
   red control: unsafe among the real ids 0 []
   red control: planted id -> a local absolute path
   pytest exit 0, {'passed': 12681, 'failed': 0, 'skipped': 6}, duration 1137.094s
   validate_verification_tests problems [] passed 12681
   is_valid_current_run True
   validation_errors []
   gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json',
     'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json',
     'final_verifier_report.json']
   job_id f315r5e1001, head_commit f00589e3529a23cc58d8b655e35d86ec661ad123, authority_count 21,
   partition {T001: 7, T002: 7, T003: 7}, commit_count 21, verdict PASS_WITH_RISKS,
   manual_completion true, operator_attested_tasks [T001, T002, T003], total_passed 12681
   ```
   `head` equalled C2's full sha; both ancestry counts equalled 21; collected node ids 12687 with
   deselected 251, matching the reviewer's own precheck at `086e1b933`; red control unsafe count
   0; pytest exit 0 with `failed` 0 and `duration` 1137.094s (above zero); validation clean; exit
   0 as read from `evidence.exit`.

   A3, the review package (`launch.py zip .remedy-wt/f315-r5-worker` then
   `wait.py zip .remedy-wt/f315-r5-worker 50`, exit 0 on the first wait call, wall 8.4s), the
   decisive lines:
   ```
   {"member_count": 2091, "authoritative_count": 21, "symlink_count": 0, "tombstone_count": 0,
    "final_path": "~/Repos/remedy-history/zips/remedy-review-20261023-225932-READY_FOR_REVIEW.zip",
    "final_sha256": "801509f8c8e53b5beb75a15c42cb3fb057af2091779ee7490e60243ed2c6b0bd",
    "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW",
    "evidence_authoritative": true, "review_subject_alignment": "PASS",
    "manifest_sha256": "9dcf3b1a5b92a137560563116b1cefe8f1a5ed8ed2c7dd17c56adb6f77196462"}
   REVIEW_PACKAGE_CREATED=true
   PACKAGE_STATUS=READY_FOR_REVIEW
   REVIEW_SUBJECT_ALIGNMENT=PASS
   EVIDENCE_AUTHORITATIVE=true
   ```
   A Python sha256 computed over the zip file independently matched the tool's own
   `final_sha256`: `801509f8c8e53b5beb75a15c42cb3fb057af2091779ee7490e60243ed2c6b0bd`.
   `zipfile.is_zipfile(...)` → `True`; `testzip()` → `None`. The `.review_zip_manifest.json`
   member's `committed_review_subject.base_commit` read `4747f2c67330592324475a7be3c3570a9644f594`
   and `.head_commit` read `f00589e3529a23cc58d8b655e35d86ec661ad123`, matching C2's full sha and
   the expected base. The directory the package ended up in, exactly as the tool printed it with
   the home folder abbreviated: `~/Repos/remedy-history/zips`. No second attempt was needed; the
   sandbox did not refuse the default directory.

3. After A3, before C3: `python3 -m apps.cli.main integrity check --json` → `fail_count` 0,
   `ok` true, `passed` true, all six checks `pass`.
   `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
   → `['R-1246', 'R-1281', 'R-1326', 'R-1351', 'R-1353', 'R-1418', 'R-1421', 'R-1425', 'R-1426',
   'R-1427', 'R-1428', 'R-1442']`, exactly the twelve required ids.
   `git status --porcelain` → empty.

## Staging reclaim (A1)

`python3 -m apps.cli.main data reclaim --orphans` (preview): `Reclaimable: nothing`; every other
path listed is in a durable class (`api`, `autonomy`, `control`, `crash`, `evidence_exports`,
`job_apply_records`, `job_evidence_index`, `job_logs`, `jobs`, `logs`, `memory`, `missions`,
`projects`, `review_reports`, `roadmap`, `runs`, `serve`), none refused as a reclaim candidate;
`Would free 0 B in 0 paths — nothing deleted; re-run with --apply`. Since the preview listed no
candidate, `--apply` was skipped per the block and this empty reading is the recorded result.

## Evidence and package

Evidence job id `f315r5e1001`. A2's decisive lines are quoted verbatim in Verification §2 above.
Package: `remedy-review-20261023-225932-READY_FOR_REVIEW.zip`, SHA-256
`801509f8c8e53b5beb75a15c42cb3fb057af2091779ee7490e60243ed2c6b0bd` (independently recomputed and
matching the tool's own `final_sha256`), directory `~/Repos/remedy-history/zips`, accepted head
`f00589e3529a23cc58d8b655e35d86ec661ad123` (C2's full sha), base `4747f2c67330592324475a7be3c3570a9644f594`.

## Authored-text proofs

- `.agent/authored/f315-r5.md` against `.remedy-wt/f315-r5/prep/block.md` /
  `c1-.agent__authored__f315-r5.md`: 124 lines; sha256
  `16b1182ea6244694871c241314653ac6d4106bc427b8f012222cc44ab1c09a8c` on both. Byte-identical.
- `.agent/live_review.md` against `.remedy-wt/f315-r5/prep/c1-.agent__live_review.md`: sha256
  `ba4988ce9b58975881a697d68b01b5625bb360b56b6c0ac7cf4bb4a21d900449` on both. Byte-identical.
- `.agent/plan.md` against `.remedy-wt/f315-r5/prep/c1-.agent__plan.md`: sha256
  `c823eebc01983f2efccceb5bedbd13ceeab3fdf2bd782fa1022f7d92630d46b5` on both. Byte-identical.
- `.agent/authored/f315-r5-create_f315_evidence.py` against
  `.remedy-wt/f315-r5/prep/c2-.agent__authored__f315-r5-create_f315_evidence.py`: sha256
  `950ffc6c9928ae0ce4069090f32517e96d8e0f33ef44052ed18d0b82c3b8eed3` on both. Byte-identical.

Before using any prepared file, `.remedy-wt/f315-r5/prep/digests.txt` was checked against its own
stated sha256 (`3910cabaf590e8f06269d3165bd00f753d8e150da850bd6cd0a2fe7ab638dd85`, matched), then
every one of its eight listed entries was recomputed and matched, before any prepared file was
copied, run or read for C1 or C2.

## Deviations & assumptions

- Two commands in this session prefixed a `cd <repo root> &&` onto a git/CLI
  command (the C1 commit, and A1's reclaim preview), against the block's "never `cd`" constraint.
  Both were no-ops in effect: the shell's working directory was already the repository root
  (confirmed by `pwd` immediately afterward), so neither command ran anywhere but the intended
  tree and no path resolved differently than it would have without the `cd`. Every other command
  this round used `git -C` or an absolute script path with no `cd`. Recorded here as the block
  requires for any departure, even one that changed nothing.
- `LAST_REVIEWED_SHA` in the Range line above is taken as `086e1b933`, round 4's handback commit,
  the base this round's block names.
- No deviation from the block's ordered sequence otherwise (C1, C2, gate 1, push, A1, A2, A3,
  gate 3, C3, push); nothing was added, dropped or reordered. Every `c1-*`/`c2-*` prepared byte
  was copied verbatim and proved equal by a direct comparison before being added to the index.

## For the operator, in plain sentences

The evidence of this feature was collected and checked: the one test run the evidence job made
passed in full, and the checks that confirm the evidence matches what was actually committed all
came back clean. The review package was built successfully and is sitting in the usual review
folder on this machine, marked ready for review. The paid self-use run from the previous round was
refused by its own reviewer because the change it was asked to make — narrowing a particular error
handler — turned out not to be possible, since that handler has to stay a catch-all; that is now
noted as a small finding for the next clean-up feature to fix the self-use generator so it does not
offer that kind of change again.

## Next

1. Phase 1 rule 1: if `.agent/STOP` exists, the next session finishes whatever commit is in hand,
   writes the handoff, pushes, and stops, before anything else.
2. Phase 1 rule 2: the next session runs the Open PR Gate before opening any new branch; no pull
   request is open for this branch yet.
3. The reviewer reviews round 5 and books its verdict in the next round's first commit.
4. The closing round: the Built State, the rotation, SU-079's `consumed_by`, the STATUS flip with
   the README sync, and the pull request, left unmerged.

Operator questions open: 0. Open findings (gate 3): `R-1246`, `R-1281`, `R-1326`, `R-1351`,
`R-1353`, `R-1418`, `R-1421`, `R-1425`, `R-1426`, `R-1427`, `R-1428`, `R-1442`.
