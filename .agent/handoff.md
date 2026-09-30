# Handoff — F293 Test load diet, round 23

## Session

SESSION 6 of feature F293 · round 23

Context self-assessment: the reviewer's context is comfortable; the session continues.

## Range

Review of `785cfe70e`..`HEAD` — one commit on `feature/f293-test-load-diet`: `b59d42cc9`, and this
handback commit (not yet made at the time this line was drafted).

## Commits

### `b59d42cc9` F293 R23 C1: book round 22, save the round 23 block and the evidence script

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f293-r23.md` | +122/-0 | NEW FILE at `.agent/authored/f293-r23.md`; byte-for-byte copy of this round's step block, `cmp`-verified against `.remedy-wt/f293-r23-block.md` before commit (`wc -l` 122, sha256 `bc425c1ff7b1c8e7fe8940fa334234d00e78259ef2ca2e5d6339c6de40e6f07e`) |
| `.agent/authored/f293-r23-create_f293_evidence.py` | +163/-0 | NEW FILE at `.agent/authored/f293-r23-create_f293_evidence.py`; byte-for-byte copy of the round's evidence script, `cmp`-verified against `.remedy-wt/f293-r23-create_f293_evidence.py` before commit (`wc -l` 163, sha256 `b1abcc1160c2f8e6975fa63fd1e367ab1b813596078da820c4e73cf643f7e9f6`) |
| `.agent/live_review.md` | +2/-0 | the F293 R22 Gate entry (VERDICT PASS) appended verbatim (bytes from `.remedy-wt/f293-r23-append-live_review.txt`); pre-commit blob (`git show 785cfe70e:.agent/live_review.md`) + append bytes verified byte-equal to the new file (`True`) |
| `.agent/plan.md` | +13/-15 | replaced whole-file by `cp` from `.remedy-wt/f293-r23-plan.md`; `cmp` silent |

`git diff --cached --numstat` before the commit read `163 0 .agent/authored/f293-r23-create_f293_evidence.py`,
`122 0 .agent/authored/f293-r23.md`, `2 0 .agent/live_review.md`, `13 15 .agent/plan.md` — matching
the block's stated `2 0` and `13 15` exactly (the two new files carry no stated numstat in the
block beyond their own `wc -l`). `git show --numstat b59d42cc9` after the commit read the same four
lines. This commit is the closure's ACCEPTED HEAD: `b59d42cc9ec43cfdc8199f777ec9c0bc3929d81e`.

### This handback commit — F293 R23 C2: handback with the evidence and package readings

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | full rewrite | this file, per `docs/agents/handback_template.md` |

## External actions

`git push origin feature/f293-test-load-diet` after C1 — outcome `785cfe70e..b59d42cc9
feature/f293-test-load-diet -> feature/f293-test-load-diet`, exit 0. `git fetch origin` run before
writing this handback confirmed `origin/feature/f293-test-load-diet` equals `b59d42cc9ec43cfdc8199f777ec9c0bc3929d81e`
— this round's accepted head — so no peer session pushed ahead during this round. `gh pr list
--state open --json number,headRefName,baseRefName,isDraft` read `[]` both at round start and again
before this handback, so the Open PR Gate needed no merge; none opened or reviewed this round. No
`git worktree` added or removed this session (`git worktree list` read 11 entries before and after:
the primary checkout plus 10 job worktrees pre-existing from other sessions). `git push origin
feature/f293-test-load-diet` after this handback commit — outcome reported in the session's own
reply, not in this file.

## Verification

All actions and gates were run once each, in the block's order, after C1 and before C2.

**A0 — staging reclaim preview, `python3 -m apps.cli.main data reclaim --orphans`:**
```
Data root: /home/decodeux/Repos/remedy/.data
  Reclaimable: nothing
  Refused (kept, with the reason):
    review_staging.n4o46eq_  class_not_job_keyed: no job owns this path; reclaim addresses job-keyed classes only  1.5 MB
  Would free 0 B in 0 paths — nothing deleted; re-run with --apply
```
Exit 0. The preview listed no candidate, so `--apply` was SKIPPED per the block's rule. The one
refused path and its reason are recorded above in full.

**A1 — `ls -la apps/ui/node_modules`:** a real directory (209 entries, `drwxrwxr-x`), not a symlink
(`os.path.islink` False, `os.path.isdir` True). Exit 0.

**A1 — `python3 .agent/authored/f293-r23-create_f293_evidence.py .remedy-wt/f293-r23-evidence`**,
output captured to `.remedy-wt/f293-r23-worker/evidence.log`:
```
head b59d42cc9ec43cfdc8199f777ec9c0bc3929d81e
ancestry-path count 81
plain count 81
collected node ids 1195, deselected 12
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 1192, 'failed': 0, 'skipped': 3}, output_hash 5be299d3aa8b12f9814f933013a00312bb2841a4ef6af90b87bc9b04d931f235
validate_verification_tests problems [] passed 1192
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
```
Exit 0. Both ancestry counts equal (81 and 81); 1195 node ids with 12 deselected, matching
`len(node_ids)`; zero unsafe node ids; the planted red-control id read `a local absolute path`;
pytest exit 0; `validate_verification_tests` problem list empty; `is_valid_current_run` True with no
validation error. Evidence job id `f293r23e1001`, step range `T001-T004`, feature `f293`, run id
`vr-1201`, base `8a067a3b93fb3d7080053f9cf742379534bed447` (the fork point). Never edited by hand.

**A2 — `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f293-r23-evidence`** (no
`REMEDY_REVIEW_DIR` set), output captured to `.remedy-wt/f293-r23-worker/zip.log`:
```
{"member_count": 7464, "authoritative_count": 31, "symlink_count": 0, "tombstone_count": 0, "final_path": "/home/decodeux/Repos/remedy-history/zips/remedy-review-20261001-005405-READY_FOR_REVIEW.zip", "final_sha256": "2c72c60f7058a7c2d9d7a0ad72a161115c282162a7ebc994bd7f0118ea704fb6", "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW", "evidence_authoritative": true, "review_subject_alignment": "PASS", "manifest_sha256": "348b79185372fde58c828418cc6c5d3b618644652664235754050b501d236eae"}
PACKAGE_STATUS=READY_FOR_REVIEW
REVIEW_SUBJECT_ALIGNMENT=PASS
EVIDENCE_AUTHORITATIVE=true
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20261001-005405-READY_FOR_REVIEW.zip
```
Exit 0. `PACKAGE_STATUS` reads `READY_FOR_REVIEW`. Package filename
`remedy-review-20261001-005405-READY_FOR_REVIEW.zip`, SHA-256
`2c72c60f7058a7c2d9d7a0ad72a161115c282162a7ebc994bd7f0118ea704fb6` (as printed by the tool itself;
the file lives outside the allowed working directory so a second independent hash could not be
computed in this session). Inside the package, `.review_zip_manifest.json`'s
`committed_review_subject` read `base_commit` `8a067a3b93fb3d7080053f9cf742379534bed447` (the fork
point) and `head_commit` `b59d42cc9ec43cfdc8199f777ec9c0bc3929d81e` (C1's full sha) —
`base_is_ancestor` true. `zipfile.is_zipfile(path)` read `True`, `ZipFile.testzip()` read `None`.
Archived directory: `/home/decodeux/Repos/remedy-history/zips` (absolute; not `NOT ARCHIVED`).

**Gate 1 (after C1) — `git status --porcelain`, `cmp` x2, integrity, open-finding-ids:**
```
$ git status --porcelain
(empty)
$ cmp .agent/authored/f293-r23.md .remedy-wt/f293-r23-block.md
(silent)
$ cmp .agent/authored/f293-r23-create_f293_evidence.py .remedy-wt/f293-r23-create_f293_evidence.py
(silent)
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, ..., "fail_count": 0, "ok": true, "passed": true, ...}
$ python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"
['R-1117', 'R-1125']
```
All exit 0. `fail_count` 0; open set `['R-1117', 'R-1125']` matching the block's stated done-when
exactly.

**Gate 2 (A1's readings)** — see the A1 transcript above; all fields matched the block's stated
expectations exactly.

**Gate 3 (A2's readings)** — see the A2 transcript above; all fields matched the block's stated
expectations exactly.

**Gate 4 (after A2) — integrity, `git status --porcelain`, `git worktree list | wc -l`:**
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"name": "handler_import", "status": "pass"}, {"name": "live_review_verdict", "status": "pass"}, {"name": "plan_consistency", "status": "pass"}, {"name": "relevant_untracked", "status": "pass"}, {"name": "repo_root_hygiene", "status": "pass"}, {"name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true}
$ git status --porcelain
(empty)
$ git worktree list | wc -l
11
```
Exit 0 for all three. Six checks `pass`, `fail_count` 0; status empty; 11 worktrees (primary plus
10 pre-existing job worktrees from other sessions, none added or removed this round).

**Gate 5 — `python3 -m pytest tests/cli/test_golden_path.py -q -n auto`:**
```
42 passed in 7.69s
```
Exit 0. **42 passed**, matching the block's stated done-when exactly. This was the round's only
pytest invocation besides the evidence script's own two internal pytest runs (`--collect-only` and
the real run); no two test commands ran at the same time.

## Authored-text proofs

`.agent/authored/f293-r23.md` (commit `b59d42cc9`): saved as a byte-for-byte copy of the step block
given to this round; `wc -l` read 122 lines, `sha256sum` read
`bc425c1ff7b1c8e7fe8940fa334234d00e78259ef2ca2e5d6339c6de40e6f07e`, and `cmp` against
`.remedy-wt/f293-r23-block.md` was silent (exit 0) both before the commit and again in this round's
Gate 1.

`.agent/authored/f293-r23-create_f293_evidence.py` (commit `b59d42cc9`): saved as a byte-for-byte
copy of the round's evidence script; `wc -l` read 163 lines, `sha256sum` read
`b1abcc1160c2f8e6975fa63fd1e367ab1b813596078da820c4e73cf643f7e9f6`, and `cmp` against
`.remedy-wt/f293-r23-create_f293_evidence.py` was silent (exit 0) both before the commit and again
in this round's Gate 1.

`.agent/live_review.md` (commit `b59d42cc9`): the pre-commit blob at `785cfe70e` was read with `git
show`, concatenated in Python with the prepared append file's raw bytes
(`.remedy-wt/f293-r23-append-live_review.txt`, sha256
`68487bd1a819cdbc8610dfd5d895138c95dfceeb702632d26a30514bacecbbce`, matching the block's stated
digest), and compared for byte equality against the resulting committed file: `True`. No text was
retyped.

`.agent/plan.md` (commit `b59d42cc9`): replaced whole-file via `cp` from `.remedy-wt/f293-r23-plan.md`
(sha256 `f455d2840b22bfcc89526f62a4f98c8405e6c1fb7350f2bebb2b2f151e985542`, matching the block's
stated digest); `cmp` against the source was silent both before the commit and again in this round's
Gate 1.

## Deviations & assumptions

None. All four prepared companion files' digests (`f293-r23-append-live_review.txt`,
`f293-r23-plan.md`, `f293-r23-create_f293_evidence.py`) were verified with `sha256sum` before use
and matched the block exactly, as did the block's own digest
(`bc425c1ff7b1c8e7fe8940fa334234d00e78259ef2ca2e5d6339c6de40e6f07e`, 122 lines). The one commit
(C1) matched the block's named paths and numstat exactly — no unrelated file, no extra hunk.
`git diff --cached` was read before the commit, per AGENTS.md's mandatory self-review loop. No
mutation red-proof ran, no full suite ran, `REMEDY_TEST_MAX_WORKERS` was never set, and no two test
commands ran at the same time — the evidence script's two internal pytest runs and the golden-path
canary each ran alone, in sequence. `.agent/STOP` did not appear at any point in this round
(checked: absent, both before A0 and before this handback). `git fetch origin`, checked before this
handback, confirmed no peer session had pushed past this round's accepted head (`b59d42cc9`). No
worktree was created or removed; all work happened in the primary checkout, as ordered. The
package's SHA-256 is reported from the build tool's own printed reading only — the archived zip
lives under `/home/decodeux/Repos/remedy-history/zips`, outside this session's allowed working
directory, so a second independent `sha256sum` over the file itself could not be run; this is
recorded here as a deviation from "verify every prepared file's digest before use" in the sense
that the PACKAGE (an output, not a prepared input) could not be independently re-hashed, though the
manifest's own `final_sha256` field agrees with the printed value.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Round 22 verdict booked (Gate entry appended, VERDICT PASS) | done | appended verbatim to `.agent/live_review.md`, byte-equality proof `True` |
| Round 23 block saved verbatim (`.agent/authored/f293-r23.md`) | done | 122 lines, sha256 `bc425c1ff7b1c8e7fe8940fa334234d00e78259ef2ca2e5d6339c6de40e6f07e`, `cmp` silent |
| Evidence script saved verbatim (`.agent/authored/f293-r23-create_f293_evidence.py`) | done | 163 lines, sha256 `b1abcc1160c2f8e6975fa63fd1e367ab1b813596078da820c4e73cf643f7e9f6`, `cmp` silent |
| `.agent/plan.md` replaced | done | whole-file `cp`, `cmp` silent |
| C1 committed as the ACCEPTED HEAD | done | `b59d42cc9ec43cfdc8199f777ec9c0bc3929d81e` |
| Push after C1 | done | `785cfe70e..b59d42cc9`, exit 0 |
| Gate 1 (`git status`, two `cmp`, integrity, open-finding-ids) | done | status empty, both `cmp` silent, `fail_count` 0, `['R-1117', 'R-1125']` |
| A0 staging reclaim preview | done | `Would free 0 B in 0 paths`, one refused path (`review_staging.n4o46eq_`, `class_not_job_keyed`); `--apply` skipped per the empty reading |
| A1 node_modules check | done | real directory, not a symlink |
| A1 evidence job (`f293r23e1001`) | done | exit 0; both ancestry counts 81; 1195 node ids/12 deselected; 0 unsafe ids; pytest exit 0 (1192 passed); empty validation problems; `is_valid_current_run` True |
| Gate 2 (A1 readings) | done | all fields matched the block's stated expectations |
| A2 review package | done | `PACKAGE_STATUS=READY_FOR_REVIEW`; filename `remedy-review-20261001-005405-READY_FOR_REVIEW.zip`; SHA-256 `2c72c60f7058a7c2d9d7a0ad72a161115c282162a7ebc994bd7f0118ea704fb6`; manifest base/head match; `is_zipfile` True, `testzip` None; archived at `/home/decodeux/Repos/remedy-history/zips` |
| Gate 3 (A2 readings) | done | all fields matched the block's stated expectations |
| Gate 4 (integrity, status, worktree count) | done | six checks pass, `fail_count` 0, status empty, 11 worktrees unchanged |
| Gate 5 golden-path canary pytest | done | `42 passed` |
| Mutation red-proofs | skipped | none ordered this round; constraints forbid mutation |
| Full suite | skipped | none ordered this round; constraints forbid it |
| Push after C2 | pending | `git push origin feature/f293-test-load-diet`, after this commit |
| PR opened | skipped | block orders no PR this round |
| STATUS/README/ledger rotation | skipped | block orders none this round; deferred to the closing round |

## Next

Operator questions open: 1

1. Phase 1 rule 1 (`.agent/STOP`) — check first.
2. Phase 1 rule 2 (Open PR Gate) — check second.
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. The closing round: book round 23, rotate the ledger, `SU-040`'s `consumed_by`, the STATUS flip
   with the README sync, and the pull request.
