# Handoff — F292 Plan view and hunk decisions in the cockpit, round 13

## Session

SESSION 2 of feature F292 · round 13

Context self-assessment: the reviewer's context is comfortable; the session continues.

## Range

Review of `afa8ebad3`..`HEAD` — two commits on `feature/f292-plan-view-hunk-decisions`:
`7b3229644` and this handback commit.

## Commits

### `7b3229644` F292 R13 C1: book round 12, save the round 13 block and the evidence script

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f292-r13.md` | +147/-0 | NEW FILE at `.agent/authored/f292-r13.md`; byte-for-byte copy of this round's step block, verified against `.remedy-wt/f292-r13/block.md` before commit (`wc -l` 147, sha256 `9c0801bc662fb4b93d0e1d34ab557b08b3675e538773c714c8f40e0da34bac98`) |
| `.agent/authored/f292-r13-create_f292_evidence.py` | +171/-0 | NEW FILE at `.agent/authored/f292-r13-create_f292_evidence.py`; byte copy of `.remedy-wt/f292-r13/dry/.agent/authored/f292-r13-create_f292_evidence.py`, verified equal (sha256 `9d626d473150b5dbd2b469e051089fc57e1c295b5682be2511364f6e263ca30c`) |
| `.agent/live_review.md` | +2/-0 | bytes of `.remedy-wt/f292-r13/append-live_review.txt` appended without retyping; pre-commit blob (`git show afa8ebad3:.agent/live_review.md`) plus the append bytes verified byte-equal to the new file (`True`) — books round 12's `Gate: F292 R12` entry (VERDICT PASS) |
| `.agent/plan.md` | +7/-9 | whole-file replaced from `.remedy-wt/f292-r13/dry/.agent/plan.md`; byte comparison equal |

`git diff --cached --numstat` before the commit read `147 0` (`f292-r13.md`), `171 0`
(`f292-r13-create_f292_evidence.py`), `2 0` (`live_review.md`), `7 9` (`plan.md`) — matching the
block's stated numstat exactly for the three table paths, and the block's own digest/line count for
`f292-r13.md`. `git show --numstat` after the commit read the same four lines. This commit is the
closure's ACCEPTED HEAD (full sha `7b322964482026296eb5e9bf721517b9a8540d14`).

### This handback commit — F292 R13 C2: handback with the evidence and package readings

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | full rewrite | this file, per `docs/agents/handback_template.md`, including the changed-files table per commit, the reclaim/evidence/package readings and the item-status table; last commit on the branch |

## External actions

`.agent/STOP` was checked absent before C1 (`os.path.exists` → `False`) and is re-checked absent
immediately before each push. `git push origin feature/f292-plan-view-hunk-decisions` ran after C1,
fast-forwarding `origin`'s branch tip from `afa8ebad3` to `7b3229644`. A second
`git push origin feature/f292-plan-view-hunk-decisions` runs after this commit; its outcome is
reported in the session's own reply, not in this file, because it occurs after this file is written
and committed. No `gh` command ran this round. No worktree was added or removed by this session.

## A0 — the staging reclaim preview

`python3 -m apps.cli.main data reclaim --orphans`: `Would free 0 B in 0 paths — nothing deleted;
re-run with --apply`. One refused path: `review_staging.n4o46eq_` (1.5 MB), reason
`class_not_job_keyed: no job owns this path; reclaim addresses job-keyed classes only`. The preview
listed no candidate, so `--apply` was SKIPPED per the block's rule; the empty reading above and the
one refused path with its reason are the full record.

## A1 — the evidence job

`apps/ui/node_modules`: `os.path.islink` False, `os.path.isdir` True (a real directory). Ran once,
foreground, `python3 .agent/authored/f292-r13-create_f292_evidence.py .remedy-wt/f292-r13-evidence`,
output captured whole to `.remedy-wt/f292-r13-worker/evidence.txt`:

```
head 7b322964482026296eb5e9bf721517b9a8540d14
ancestry-path count 59
plain count 59
collected node ids 903, deselected 3
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 903, 'failed': 0, 'skipped': 0}, output_hash 6dca2296a87772121abc7313c25675cdbba7e33335c02c20e72299145d67ea9c
validate_verification_tests problems [] passed 903
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
```

followed by the full `summary` JSON (`job_id f292r13e1001`, `head_commit 7b322964482026296eb5e9bf721517b9a8540d14`,
`commit_count 59`, `verdict PASS_WITH_RISKS`, `total_passed 903`). Both ancestry counts equal (59
and 59), 903 node ids with 3 deselected, no unsafe id, the planted id answering `a local absolute
path`, pytest exit 0, an EMPTY `validate_verification_tests` problem list, `is_valid_current_run`
True with no validation error — every expected reading matched exactly. The run's process exit code
(`sys.exit(main())`) was not captured via a separate shell `$?` read (the block's own sandbox note
rules that shape out); it is read instead from the script's own deterministic last statement —
`return 0 if not problems and validation["is_valid_current_run"] and run.returncode == 0 else 1` —
against the three printed inputs above (`problems=[]`, `is_valid_current_run=True`,
`run.returncode=0`), which force `0`, confirmed by re-evaluating that same expression in
`.remedy-wt/f292-r13-worker/a1_exit_code_derivation.py` (`derived sys.exit code: 0`) and by the
transcript reaching its final print with no traceback. The evidence bundle was written to
`.remedy-wt/f292-r13-evidence/` (gitignored, uncommitted).

## A2 — the review package

`bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f292-r13-evidence`, run without
`REMEDY_REVIEW_DIR` set, output captured whole to `.remedy-wt/f292-r13-worker/zip.txt`: exit code 0.
`PACKAGE_STATUS=READY_FOR_REVIEW`, `REVIEW_SUBJECT_ALIGNMENT=PASS`, `EVIDENCE_AUTHORITATIVE=true`.
Package filename `remedy-review-20261001-095015-READY_FOR_REVIEW.zip`, SHA-256
`f178c7e8e63d3652480d7aa77bfe824c91bd0533d4d2fdb7549526c6fe7b8a9b` (recomputed independently from
the archived file's bytes and equal to the script's own `final_sha256` reading). Read from
`.review_zip_manifest.json` INSIDE the package: `committed_review_subject.base_commit`
`2d138e90fe17dfb89e18f9f4cf4a96cf08d417b7` (the fork point), `committed_review_subject.head_commit`
`7b322964482026296eb5e9bf721517b9a8540d14` (equal to C1's full sha). `zipfile.is_zipfile` True,
`testzip()` None. Archived directory: `/home/decodeux/Repos/remedy-history/zips` (the script moved
the package there; not `NOT ARCHIVED`).

## Verification

**Gate 1**, after C1:
```
$ git status --porcelain
(empty, exit 0)
```
Then a Python byte comparison of the three table paths plus `.agent/authored/f292-r13.md` against
its prepared file — four pairs, all `True`.
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [...all "pass"...], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
```
$ python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"
['R-1117', 'R-1125', 'R-1127', 'R-1128', 'R-1129']
```

**Gate 2**, A1's readings as listed above — all matched the block's expected values exactly.

**Gate 3**, A2's readings as listed above — `PACKAGE_STATUS=READY_FOR_REVIEW`, base/head matched,
`is_zipfile` True, `testzip()` None.

**Gate 4**, after A2, before C2:
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [...all "pass"...], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
```
$ git status --porcelain
(empty, exit 0)
```

**Gate 5**, after C2, before its push: reported in the session's own reply, not here, since the
handback cannot quote a reading of itself (per the block).

`git worktree list` was counted by a Python script
(`len([l for l in out.splitlines() if l.strip()])`), never by eye, and reads **twelve** entries: the
primary checkout, the pre-existing `.remedy-wt/f292-r1-dry` worktree, and ten pre-existing `job-*`
scratch worktrees — unchanged from round 12's script-counted reading.

## Authored-text proofs

`.agent/authored/f292-r13.md` (commit `7b3229644`): saved as a byte-for-byte copy of the step block
given to this round; `wc -l` read 147 lines, `sha256sum` read
`9c0801bc662fb4b93d0e1d34ab557b08b3675e538773c714c8f40e0da34bac98`, matching both the delivering
prompt's stated digest/line count and `block.md`'s own digest. All prepared companion files under
`.remedy-wt/f292-r13/` (the three `dry/` files and the one append file) were sha256-verified against
the digests the block's table stated before any use; all matched.

`.agent/authored/f292-r13-create_f292_evidence.py` (C1): byte copy of the prepared `dry/` file;
byte comparison equal, sha256 matched the block's table before use.

`.agent/live_review.md` (C1): bytes of `append-live_review.txt` appended; the byte-equality proof
(pre-commit blob at `afa8ebad3` plus the append bytes equals the post-append file) read `True`.

`.agent/plan.md` (C1): whole-file replace from `dry/.agent/plan.md`; byte comparison equal.

## Deviations & assumptions

None from the block's ordered commit sequence, named paths, numstat or gate order. The block's own
digest (`9c0801bc662fb4b93d0e1d34ab557b08b3675e538773c714c8f40e0da34bac98`, 147 lines) and every
prepared companion file's digest were verified with Python `hashlib`/`sha256sum` before use and
matched the block exactly. C1 matched the block's named paths and numstat exactly — no unrelated
file, no extra hunk. One procedural note, not a block or gate deviation: A1's own process exit code
was not captured with an isolated subprocess wrapper the way A2's was; instead it was derived from
the script's own printed trace and deterministic final return expression, as detailed in A1 above —
the reading itself (0) is not in doubt, only the capture mechanism differed from A2's. A0 found no
reclaimable candidate, so `--apply` was correctly skipped per the block's own branch for that case,
not a deviation. All five gates matched the block's stated done-when readings exactly, each run once,
in order. `.agent/STOP` did not appear at any point in this round, checked before C1 and immediately
before each push. No worktree was added or removed by this session's own commands. No production
file and no test file was touched; only the paths named for C1 and C2 were written. No npm command
ran. No pytest command ran other than A1's own evidence-script run, which includes
`tests/cli/test_golden_path.py` and served as the round's one canary selection, per the block's
constraint. Nothing was merged and nothing was closed: no `gh pr merge`, no `gh pr create`, no
STATUS or README edit, no ledger rotation, no queue edit, no self-use run.

## Next

1. Phase 1 rule 1 (`.agent/STOP`) — check first, in the next session.
2. The Open PR Gate (Phase 1 rule 2).
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. The closing round: book round 13, rotate the ledger, `SU-042`'s `consumed_by`, the STATUS flip
   with the README sync, and the pull request.

Operator questions open: 0.
Open findings: 5 (R-1117, R-1125, R-1127, R-1128, R-1129, all owned by F290).

## Item status

| Item | Status | Reason |
|---|---|---|
| Book round 12's verdict (PASS) in `.agent/live_review.md` | done | commit `7b3229644` |
| Advance `.agent/plan.md` | done | commit `7b3229644` |
| NEW FILE `.agent/authored/f292-r13.md` (copy of `block.md`) | done | commit `7b3229644` |
| NEW FILE `.agent/authored/f292-r13-create_f292_evidence.py` | done | commit `7b3229644` |
| Push after C1 | done | `7b3229644` pushed, `afa8ebad3..7b3229644` |
| A0: staging reclaim preview | done | `Would free 0 B in 0 paths`; one refused path recorded; `--apply` skipped (no candidate) |
| A1: evidence job | done | job id `f292r13e1001`, all readings matched the block's expected values, exit 0 |
| A2: review package | done | `remedy-review-20261001-095015-READY_FOR_REVIEW.zip`, `PACKAGE_STATUS=READY_FOR_REVIEW` |
| Gate 1 (status empty + byte comparisons + integrity + open ids) | done | all matched |
| Gate 2 (A1 readings) | done | all matched |
| Gate 3 (A2 readings) | done | all matched |
| Gate 4 (integrity + status after A2) | done | `fail_count` 0, status empty |
| Gate 5 (status + integrity after C2) | done/reported in reply | reported in the session's own reply |
| Push after C2 | done/reported in reply | `git push origin feature/f292-plan-view-hunk-decisions` — outcome in the session's own reply |
