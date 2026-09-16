# Handoff — F261 round 27

## Session

SESSION 7 of feature F261 · round 27 · rounds so far 27

Context self-assessment: the round was three record commits, one script-run rotation, one evidence
job and one package build, and the worker's context stayed comfortable throughout.

## Range

Review of `f2872a33`..`HEAD`.

## Commits

### 417ba82e F261 R27 C0a: save the round 27 step block under the authored directory
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r27.md` | +235 / -0 | the block file the delegating message names, copied with `shutil.copyfile`, sha256 `5a5c97f3…f1ee888` verified after the copy |

### f8f8be60 F261 R27 C0b: mirror the round 27 step block into the last block state file
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +177 / -201 | the same bytes, byte-identical to the C0a copy |

### fb510ca7 F261 R27 C1: book round 26's PASS with the recurrences of R-0645, R-0784 and R-0838, and set the closure round A plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md`, `.agent/live_review.md` (2 paths) | +32 / -18 | plan.md full replacement by PLAN27 (+18 / -18); RECORD27 appended to live_review.md (+14 / -0), the `Gate: F261 R26` PASS entry and three recurrence paragraphs. The FIRST SUBSTANTIVE COMMIT of the round |

### 30343f92 F261 R27 C2: rotate the ledger into the archive by the rotation script, 110 gate records and 7 finding pairs moved
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md`, `.agent/live_review_archive.md` (2 paths) | +762 / -762 | written by `python3 -B scripts/rotate_live_review.py` alone (live_review.md +0 / -762, archive +762 / -0). THE ACCEPTED HEAD |

### Item status — the block's ordered bundle

| Item | Status | Reason |
|--------|----------|------------------------------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | the accepted head |
| SPEC E | done | committed nothing; evidence dir untracked under `.remedy-wt/f261r27w/` |
| SPEC Z | done | READY_FOR_REVIEW; committed nothing |
| C3 | done | this commit, then the push |

## External actions

| Command | Outcome |
|---|---|
| `git push origin feature/f261-cli-vocabulary-v2` after C1 | `f2872a33..fb510ca7` |
| `git push origin feature/f261-cli-vocabulary-v2` after C2 | `fb510ca7..30343f92` |
| `git fetch -q origin feature/f261-cli-vocabulary-v2` before SPEC Z | exit 0, to read the remote ref fresh; HEAD == origin == `30343f92` |
| `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f261r27w/evidence-234c8e6f18905013` | exit 0, package READY_FOR_REVIEW in the script's default directory, not moved |
| `git push origin feature/f261-cli-vocabulary-v2` after C3 | run after this commit; its outcome is in the completion message |

No pull request created, edited or merged. No `gh` command. No `remedy` CLI invocation. No runner
or `run_job` call. No worktree created.

## Verification

STOP reads, before C0a, C2 and C3: `ls .agent/STOP` → exit 2, `No such file or directory` each
time.

### G1 TRANSPORT — exit 0

    PASS authored block sha256 at C0a (417ba82e) == delegating digest
         5a5c97f39becefa09a49027b515411e150ee30aae86b990a54be8614cf1ee888
    PASS last_block.md at C0b (f8f8be60) byte-identical to it
    PASS slice PLAN27   FOUND e8fa0859261f87762db06e8865634fdd0041c8e1138a14017fc6b5a15c07c6e5, 1927 bytes, 37 lines
    PASS slice RECORD27 FOUND c951086e67d5bce35ea6eb28b6212820fe4e0387bae2b3e7707dc0d9ff05cc60, 5782 bytes, 14 lines
    block: 235 lines TOTAL, 51 slice-content lines, 184 PROSE; no single-repeated-character line

### G2 THE RECORD at C1 — exit 0

    PASS plan.md byte-identical to PLAN27, 37 lines, ^## Goal$ once, ^## Next Steps$ once
    PASS live_review.md == f2872a33 blob + RECORD27: 1135907 bytes,
         sha256 84301e032a64e0eb77caeb82c4940d21e6cb750fc94a27b05812a93feb480298
    PASS ^Gate: F\d+ R\d+ —          f2872a33=135  C1=136
    PASS Gate: F261 R26 —            f2872a33=0    C1=1
         distinct ^- R-\d+ — ids     f2872a33=134  C1=134
         distinct ^Done: R-\d+ — ids f2872a33=9    C1=9
    PASS open set by distinct id     f2872a33=125  C1=125, identical membership

    python3 -B -m pytest tests/docs/ -q   → exit 0, "310 passed in 1.06s"

### G3 THE ROTATION at C2 — exit 0

    python3 -B scripts/rotate_live_review.py   → exit 0, full stdout:
      gate records moved: 110
      finding pairs moved: 7 (14 records)
      old ledger size: 1135907 bytes
      new ledger size: 620380 bytes
      old archive size: 2948965 bytes
      new archive size: 3464492 bytes
      open findings before: 123
      open findings after: 123
      written: <repo>/.agent/live_review.md and <repo>/.agent/live_review_archive.md
    (the last line printed the two absolute paths under the primary checkout's root)
    PASS live_review.md at C2 620380 bytes, sha256 dfc4747d104149ad7a22e73c61df983bec9c7bc0ff06bf2cec697422a25d576c
    PASS archive at C2 3464492 bytes, sha256 271ee9e7a91d16dac8da56eeaa807b5d3dd010c64d934d667500843c5ff20552
    PASS distinct-id open set C1 125 == C2 125, identical membership
    PASS archive at C1 (2948965 bytes) is an exact prefix of the archive at C2
    git show --numstat --format= 30343f92 → 0 762 .agent/live_review.md; 762 0 .agent/live_review_archive.md
                                            (insertions 762, deletions 762, exactly the two paths)

### G4 THE EVIDENCE JOB, SPEC E — exit 0

    E1 head 30343f927800784c464eaf56706d5b82ece39c81
       rev-list --ancestry-path 7cdde89b..C2 = 183; rev-list 7cdde89b..C2 = 183; equal
       git merge-base --is-ancestor 7cdde89b5d0dc8ef1fb96980105870e956699873 origin/main → exit 0
       git status --porcelain → ''
    E2 python3 -B -m pytest tests/docs/ -q -p no:randomly (PYTHONPATH, REMEDY_PROJECT, REMEDY_DATA_DIR
       removed) → exit 0, "310 passed in 1.05s"; --collect-only → exit 0
       entry: exit_code 0 · passed 310 · failed 0 · skipped 0 · deselected 0 · selected 310 ·
       len(node_ids) 310 · len(test_files) 4 · output_hash 6705653ba41d2d9a54133c676b6b62ae25c254f34b8ac04563a9e0bf8a960da9 ·
       duration_seconds 1.269
       test_files: tests/docs/test_docs_consistency.py, tests/docs/test_named_source_paths.py,
                   tests/docs/test_retired_promote_word.py, tests/docs/test_vocabulary.py
       pre-scan (_unsafe_text, loaded by file path) flags: 0
    E3 evidence_dir .remedy-wt/f261r27w/evidence-234c8e6f18905013 · timestamp = generated_at =
       2026-09-16T13:15:12+00:00
       summary, in full:
       {"authority_count": 223, "commit_count": 183,
        "head_commit": "30343f927800784c464eaf56706d5b82ece39c81", "job_id": "234c8e6f18905013",
        "manual_completion": true, "operator_attested_tasks": ["T001", "T002", "T003"],
        "partition": {"T001": 75, "T002": 75, "T003": 73}, "total_passed": 310,
        "verdict": "PASS_WITH_RISKS"}

The reviewer's dry run read 181 and 181 on a head without the two block-save commits; 183 is that
plus C0a and C0b.

### G5 THE PACKAGE AND THE PRECONDITIONS, SPEC Z — exit 0

    bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f261r27w/evidence-234c8e6f18905013 → exit 0
      REVIEW_PACKAGE_CREATED=true
      PACKAGE_STATUS=READY_FOR_REVIEW
      PACKAGING_CWD=/home/decodeux/Repos/remedy
      EVIDENCE_DIR=.remedy-wt/f261r27w/evidence-234c8e6f18905013
      REVIEW_SUBJECT_ALIGNMENT=PASS
      EVIDENCE_AUTHORITATIVE=true
      REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
      ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260916-151540-READY_FOR_REVIEW.zip
      JSON line: final_sha256 8bc443e91657986bcbb83ad3b6d81cb55afd4b111ff7d4e6930983606f545275,
                 member_count 4377, authoritative_count 223, package_status READY_FOR_REVIEW
    PASS sha256 recomputed from the file == printed, 8bc443e91657986bcbb83ad3b6d81cb55afd4b111ff7d4e6930983606f545275
    from the package's .review_zip_manifest.json:
      package_status READY_FOR_REVIEW
      committed_review_subject.base_commit  7cdde89b5d0dc8ef1fb96980105870e956699873  (fork point)
      committed_review_subject.head_commit  30343f927800784c464eaf56706d5b82ece39c81  (C2)
      committed_review_subject.commit_count 183                                       (E1's count)

    python3 -B -m pytest tests/docs/ -q                   → exit 0, "310 passed in 1.04s"
    python3 -B -m pytest tests/cli/test_golden_path.py -q → exit 0, "42 passed in 17.89s"

    run_integrity_checks(): .passed True · .fail_count 0
      high_blockers_open: name 'high_blockers_open' · status IntegrityStatus.PASS ('pass') ·
                          message 'no open blocker/high findings'
    open High findings read from the ledger at C2 (open `- R-xxxx — High` registrations):
      R-0803, R-0804, R-0807 — the check does not see them, which is R-0648

### G6 TREE, PATH SET, CAP after C2 and its push — exit 0

    git status --porcelain → ''
    git worktree list      → 1 row
    git branch --list 'remedy/job-*' → 17 lines
    git rev-parse HEAD == git rev-parse origin/feature/f261-cli-vocabulary-v2 == 30343f927800784c464eaf56706d5b82ece39c81
    changed paths f2872a33..C2: 5 against the Bundle's 5 (less handoff.md); MISSING none; EXTRA none

    | Commit | insertions | deletions | staged paths |
    |---|---|---|---|
    | 417ba82e C0a | 235 | 0 | 1 |
    | f8f8be60 C0b | 177 | 201 | 1 |
    | fb510ca7 C1 | 32 | 18 | 2 |
    | 30343f92 C2 | 762 | 762 | 2 |
    commits reaching 500 insertions: 30343f92 (C2), declared below

## Closure values for round B's STATUS line

    Evidence job   234c8e6f18905013
    package        remedy-review-20260916-151540-READY_FOR_REVIEW.zip
    SHA-256        8bc443e91657986bcbb83ad3b6d81cb55afd4b111ff7d4e6930983606f545275
    package path   /home/decodeux/Repos/remedy-history/zips
    accepted HEAD  30343f927800784c464eaf56706d5b82ece39c81

Live review verdict carried by the evidence producer: `PASS_WITH_RISKS`.

## Declared oversize commit (constraint 6)

C2 `30343f92` carries 762 insertions, over the 500-line cap. It is declared under AGENTS.md's
declared-oversize exception with DECISION F272 D18's reason: the rotation cannot be split without
leaving records in neither file or in both, and the script verifies every moved record by sha256.
It is this feature's only such commit.

## Authored-text proofs

PLAN27 and RECORD27 were extracted as the bytes strictly between their `BEGIN` and `END` lines and
matched their BEGIN-marker sha256 before use; neither was edited. The applied results were re-read
from the git objects at C1: plan.md equals PLAN27 byte for byte, and live_review.md equals the
`f2872a33` blob plus RECORD27 at the reviewer's 1135907 bytes and sha256 (G2).
`.agent/authored/f261-r27.md` and `.agent/last_block.md` are byte-identical to the delegated block
file (G1). The rotated files at C2 match the reviewer's two digests (G3).

## Deviations & assumptions

None to the ordered commit sequence: C0a, C0b, C1, C2 and C3 landed in that order, each
single-parent, on `f2872a33`. Declared:

1. G2's `tests/docs/` run was first made with `-p no:cacheprovider` added (exit 0, "310 passed in
   1.04s"), then re-run with the exact command, which is the reading reported above.
2. SPEC E's single ISO-8601 UTC value is written in the `+00:00` form
   (`2026-09-16T13:15:12+00:00`), the form earlier closure evidence scripts used, and not with a `Z`.
3. G5's integrity script also printed a "non-pass check" list whose filter was wrong: it compared
   the status enum's string form, so it listed five checks that are all `IntegrityStatus.PASS`.
   `.passed True` and `.fail_count 0` are the readings; nothing was re-run.
4. Two compound shell commands were refused by the command guard by form (one using `$?`); they
   were re-issued as single commands, and nothing ran from the refused forms. The first package
   build attempt was one of them, so the script ran exactly once.
5. `git fetch -q origin feature/f261-cli-vocabulary-v2` was run before SPEC Z to read the remote
   ref fresh; it changed nothing.

## Next

1. Phase 1 rule 1: re-read `.agent/STOP` from disk before anything else.
2. The reviewer's verdict on round 27.
3. Closure round B.

Open findings: 125 by distinct id, with the High ids R-0803, R-0804 and R-0807.

Operator questions open: 1
