# Handoff — F253 round 35: book round 34; the evidence job ran, validation FAILED, no review package built (BLOCKED)

## Session

SESSION 6 of feature F253 · round 35 · rounds so far 35

Context self-assessment: "The reviewer's context is long after eleven rounds in this session; the closing round follows, and the next session resumes from this handoff if this one ends first."

Fortschritt: ~97 % (everything but a repair of five old commit subjects, the evidence, the package and the closing commit is done) — Schätzung

## Range

Review of `6f8d7d43fec19289faea1f779e3c4a6c9842e6db`..`380565addeebcf867057a7ac62a77563964a26d1` (C1, the accepted head; this handback commit follows it).

## Commits

### 380565add F253 R35 C1: book round 34, the plan, save the block and the evidence script

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f253-r35.md` | 170/0 | new file, byte copy of `block.md` (170 lines, sha256 `a5f5c67fecff7adfc1975bac17f13efc7aa14501f3694bc68fd97f6342e9417d`) |
| `.agent/authored/f253-r35-create_f253_evidence.py` | 205/0 | new file, byte copy of the prepared script (205 lines, sha256 `ee9941a7bd5186bfea7473cf800ed158cc08998a87188b061aa3ca35e55067b4`) |
| `.agent/live_review.md` | 2/0 | its bytes at `6f8d7d43f` followed by `append-live_review.txt` (round 34's gate entry, PASS); 447 lines, sha256 `53f262855f707b2a6ca1fbfe21ec02bc3f19752ab849e0d527fa9d63b6efdb59` |
| `.agent/plan.md` | 5/5 | `dry-plan.md`, byte for byte (40 lines, sha256 `b4df56ffd4ed5d591ba46b7722d76375bcc0360baccc20035ee2c3bd54d660d8`) |

### This commit (self-reference)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file |

## External actions

- `git push origin feature/f253-public-http-api` after C1: `6f8d7d43f..380565add  feature/f253-public-http-api -> feature/f253-public-http-api` (one attempt).
- A0 `python3 -m apps.cli.main data reclaim --orphans`: ran once, `Reclaimable: nothing`, last line `Would free 0 B in 0 paths — nothing deleted; re-run with --apply`. `--apply` skipped as the block orders. One refused path: `review_staging.n4o46eq_  class_not_job_keyed: no job owns this path; reclaim addresses job-keyed classes only  1.5 MB`.
- A1 the evidence script: ran once, exit 1 (below). A2 NOT RUN: `NOT ARCHIVED`, no package exists.
- No pull request, no merge, no mutation, no worktree, no force-push, no pull, no full suite, no other pytest command. The worker's scripts and logs are under `.remedy-wt/f253-r35-worker/` (gitignored); the evidence bundle is `.remedy-wt/f253-r35-evidence/` (gitignored, not committed).

## Verification

0. Preconditions: all four prepared files matched `digests.txt` (`block.md` 170 lines); HEAD and origin both `6f8d7d43fec19289faea1f779e3c4a6c9842e6db`; `git status --porcelain` empty; `.agent/STOP` absent; branch `feature/f253-public-http-api`.
1. Gate 1: `git status --porcelain` empty (exit 0). Proofs with `git show 380565add:<path>` against the prepared files: block copy True, script copy True, plan True, ledger (blob at `6f8d7d43f` plus the slice) True. Local tip equalled `origin/feature/f253-public-http-api` after the push.
2. Gate 2 (A1), evidence script exit code 1. Raw log `.remedy-wt/f253-r35-worker/evidence.log`:
   - `head 380565addeebcf867057a7ac62a77563964a26d1`, `ancestry-path count 135`, `plain count 135`
   - `collected node ids 2209, deselected 44`
   - `red control: unsafe among the real ids 0 []`; `red control: planted id -> a local absolute path`
   - `pytest exit 0, {'passed': 2206, 'failed': 0, 'skipped': 3}, output_hash d6697af095137ab09bf5de5343a2e1f8d9e91db78eb578808eb5e6da5b2ea753`
   - `validate_verification_tests problems [] passed 2206`
   - `is_valid_current_run False`
   - `validation_errors ['review_subject commit[1] subject is missing, too long, or carries a secret/path/control', ... commit[5], commit[9], commit[20], commit[35] (same text)]`
   - gates written: artifact_contract, change_provenance, commit_execution, fresh_evidence, runtime_integration, final_verifier_report; summary job `f253r35e1001`, commit_count 135, verdict `PASS_WITH_RISKS`, total_passed 2206.
   - Failed test node ids: none (pytest exit 0). `git reflog -n 3` and branch identical before and after the run (newest entry C1; branch `feature/f253-public-http-api`).
3. Gate 3 (A2): not run, blocked.
4. Gate 4 (integrity, open ids, worktree count): not run, because A2 did not run.

### Cause of the validation failure (read-only follow-up)

`validate_review_commit_schema` (`packages/orchestration/review_subject.py:803-805`) rejects a commit subject that `_metadata_is_safe` reads as carrying a local path. Listing `git log --reverse 1474a65ea..HEAD` (index 0 = oldest) and applying `_metadata_is_safe` to every subject gives exactly the indexes 1, 5, 9, 20 and 35, and no other:

- 1 `bb01d85cf` F253 R1 C2: ... GET /api/v1/interface ...
- 5 `00be6f560` F253 R2 C2: ... GET /api/v1/digest ...
- 9 `352e1d17b` F253 R3 C2: GET /api/v1/jobs/{job}/proof ...
- 20 `c3fe32384` F253 R5 C3: GET /api/v1/changes ...
- 35 `300105d0f` F253 R8 C3: POST /api/v1/jobs/{job}/decisions/{decision} ...

Each carries a slash-led route token, the pattern AGENTS.md "Commit Discipline" forbids in subjects. They are history of the branch, not of this round. A repair needs the reviewer's decision (rewriting five pushed subjects changes every later sha, which the block forbids as a force-push; or a change to the packaging scan or the base choice).

## Authored-text proofs

- `block.md` to `.agent/authored/f253-r35.md`: 170 lines, byte-equal, sha256 `a5f5c67fecff7adfc1975bac17f13efc7aa14501f3694bc68fd97f6342e9417d`.
- `f253-r35-create_f253_evidence.py` to `.agent/authored/f253-r35-create_f253_evidence.py`: 205 lines, byte-equal, sha256 `ee9941a7bd5186bfea7473cf800ed158cc08998a87188b061aa3ca35e55067b4`.
- `append-live_review.txt`: "post equals pre plus slice" True against the blob at `6f8d7d43f`.
- `dry-plan.md` to `.agent/plan.md`: byte-equal.

## Deviations & assumptions

- A1 exited 1, so the block's stop rule applied: A2 and gate 4 were not run, and C2 is this handoff alone, written with the raw log's readings.
- The tool shows no exit code of its own; each exit code above was printed by a Python wrapper (A1) or read from the summary line.
- The read-only follow-up scripts (`subjects.py`, `subj_check.py`) were extra to the block; they only list subjects and call `_metadata_is_safe`.

## Round verdicts

Rounds 1 to 34 are booked in the ledger (round 34 by this round's C1: PASS). Round 35's verdict is the reviewer's to give and book in the next round's first commit.

## For the operator, in plain sentences

Remedy was to build the review package for the feature that lets a program on this computer drive Remedy over a local web interface with its own key: read what Remedy can do and what is happening, answer its questions, approve or decline a result, and start and follow work, with every call written down. The package was NOT built. The evidence run ran 2209 tests selected (44 left out) and 2206 passed, 3 were skipped and none failed, but the packaging check refused the history: five old commit subjects of this branch name web routes starting with a slash, which the check reads as a file path on this computer. No package file was saved and no folder holds one. No old scratch copies were cleaned up: nothing was eligible, and 0 bytes were freed. Nothing waits for you; the reviewer decides how the five subjects are handled.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and stop.
2. Phase 1 rule 2 (Open PR Gate): no pull request is open for this branch yet, none to merge.
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. The reviewer reviews round 35 and books its verdict in the next round's first commit.
5. Decide how the five commit subjects named above are made acceptable to the packaging scan (they are pushed history), then repeat the evidence job and the package from the accepted head.
6. The closing round: book round 35, rotate the ledger, the open findings stay with F297, the self-use entry SU-050's consumed_by, the STATUS flip with the README sync, and the pull request, left unmerged.

Operator questions open: 4.
Open findings: 15 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196, R-1219, R-1220 and R-1225, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 34, the plan, save the block and the evidence script | done | `380565add` |
| Push after C1 | done | `6f8d7d43f..380565add` |
| Gate 1 | done | green |
| A0: the staging reclaim | done | nothing reclaimable, `--apply` skipped |
| A1: the evidence job | deviated | exit 1: pytest green, `is_valid_current_run` False (five commit subjects) |
| Gate 2 | deviated | readings recorded above, validation red |
| A2: the review package | skipped | blocked by A1; NOT ARCHIVED |
| Gate 3 | skipped | no package |
| Gate 4 | skipped | A2 did not run |
| C2: this handback | done | this commit |
| Push after C2, Gate 5 | pending | reported in the worker's reply |
