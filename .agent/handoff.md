# Handback — F151 round 9

## Session

SESSION 2 of feature F151 · round 9 · rounds so far 9.

Context self-assessment: every prepared file this round used (`block.md`, `digests.txt`, all three
`c1-*` files, the `c2-*` evidence script, `launch.py`, `wait.py`, `verify.py`) was checked against
`digests.txt`'s sha256 before use, `digests.txt` itself was checked against the sha256 given in the
prompt before any of its listed files were trusted, the whole block, `docs/agents/handback_template.md`,
`docs/roadmap/STATUS_closure_protocol.md` and `.agent/authored/f133-r6.md` (the analogous round of
F133) were read in full before acting, and every number below (insertion counts, byte sizes, gate
readings, the evidence job's and the zip job's own output) was produced by running the thing, not
recalled.

Fortschritt: ~95 % (everything but the closing round is done) — Schätzung

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | three prepared paths copied and proved byte-identical, then committed: a new `.agent/authored/f151-r9.md`, R-1441's `Landed:` line replaced by the reviewer's `Done:` text plus a new `Gate: F151 R8` entry, and the plan advanced to round 9 |
| C2 | done | the evidence script copied and proved byte-identical, committed alone, pushed |
| A1 | done | preview read "Reclaimable: nothing", would free 0 B in 0 paths; no candidate, so `--apply` was skipped |
| A2 | done | evidence job run once, exit 0; `12585` node ids collected, `251` deselected; pytest `12579 passed, 0 failed, 6 skipped`; `is_valid_current_run True`, `validation_errors []` |
| A3 | done | zip built on the first attempt; `PACKAGE_STATUS=READY_FOR_REVIEW`, no sandbox-write refusal, no retry needed |
| C3 | done | this handback |
| R-1441 | done | booked as Done in C1, carried over from round 8's repair; re-confirmed by this round's evidence job, whose scoped pytest run passed with the repaired docs page in the tree |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` every line `True`, last line `ALL True` (`C3` read `absent` at that time) |
| Gate 2 | done | `evidence.exit` read `exit 0 wall 1735.5`; `zip.exit` read `exit 0 wall 18.2` |
| Gate 3 | done | `fail_count` 0 (6 checks, all `pass`); the open set reads the eleven ordered ids; `git status --porcelain` empty |

## Evidence and package

Evidence job id `f151r9e1001` (quoted from the job summary's `"job_id": "f151r9e1001"`).

A2's lines, quoted verbatim from the evidence script's own output:

```
head 76fd568651d04b420027a0f0a233b458fdcc9896
ancestry-path count 40
plain count 40
collected node ids 12585, deselected 251
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 12579, 'failed': 0, 'skipped': 6}, output_hash 6b3a1f21a69fa53214f70fd6765eb8bf0cb8f30633a1aea08c8592f630bba761
validate_verification_tests problems [] passed 12579
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
```

The job summary's decisive fields: `"authority_count": 27`, `"commit_count": 40`, `"verdict": "PASS_WITH_RISKS"`,
`"manual_completion": true`, `"total_passed": 12579`. The launcher's own `.exit` line: `exit 0 wall 1735.5`.

A3's package, quoted verbatim from the zip build's own output, with this machine's home folder
written as `~` (the build's own line named an absolute path; the rest of the line is otherwise
verbatim): `PACKAGE_STATUS=READY_FOR_REVIEW`, `REVIEW_SUBJECT_ALIGNMENT=PASS`,
`EVIDENCE_AUTHORITATIVE=true`. The build's own JSON line:
`{"member_count": 2101, "authoritative_count": 27, "symlink_count": 0, "tombstone_count": 0,
"final_path": "~/Repos/remedy-history/zips/remedy-review-20261023-180445-READY_FOR_REVIEW.zip",
"final_sha256": "ff7cc953206489a10d4197704b1016b77d5284f5255e8ba34e34aee3b1906f5c",
"publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW", "evidence_authoritative": true,
"review_subject_alignment": "PASS", "manifest_sha256": "1208c12b4f7320819a70574e90f063c3cbbb5af05ed7ab55066619f09d94119d"}`.
The launcher's own `.exit` line: `exit 0 wall 18.2`.

Package file name: `remedy-review-20261023-180445-READY_FOR_REVIEW.zip`. SHA-256, re-measured by this
worker with a dedicated `python3` script over the file's bytes (not copied from the build's own
printed line): `ff7cc953206489a10d4197704b1016b77d5284f5255e8ba34e34aee3b1906f5c` — matches the build's
`final_sha256` exactly. Directory the package ended up in: `~/Repos/remedy-history/zips`.
`zipfile.is_zipfile` on the package: `True`. `testzip()`: `None`. `.review_zip_manifest.json` inside the
package, read by this worker directly, `committed_review_subject`: base
`4232c579e8e1e6d076bb4d8d1a6f7687ea5f9b8a` (the written-in-full fork point the block names), head
`76fd568651d04b420027a0f0a233b458fdcc9896` (C2's full sha). Accepted HEAD: `76fd568651d04b420027a0f0a233b458fdcc9896`.

## Staging reclaim

`python3 -m apps.cli.main data reclaim --orphans` (preview, run once): "Reclaimable: nothing"; every
listed data-root class (`api`, `autonomy`, `control`, `crash`, `evidence_exports`, `job_apply_records`,
`job_evidence_index`, `job_logs`, `jobs`, `logs`, `memory`, `missions`, `projects`, `review_reports`,
`roadmap`, `runs`, `serve`) read `durable`, none refused; "Would free 0 B in 0 paths — nothing deleted;
re-run with --apply". No candidate was listed, so `--apply` was skipped per the block; the empty reading
above is the recorded one.

## Range

Review of `5797b2e42`..`HEAD` (`HEAD` is this handback's own commit).

## Commits

### `4199d4596` F151 R9 C1: book round 8, resolve R-1441, the plan, the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f151-r9.md` | +121/-0 (new) | byte copy of the block, proved equal to `block.md` (line count 121, sha256 `1951da94726c3f3ab6a1d3d8b82f702dd7e8a14d49cb133462cb45b7a56e6966`) |
| `.agent/live_review.md` | +4/-0 | R-1441's `Landed:` paragraph replaced by the reviewer's `Done:` resolution, and a new `Gate: F151 R8` entry appended |
| `.agent/plan.md` | +4/-6 | rewritten for round 9 |

### `76fd56865` F151 R9 C2: the evidence script

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f151-r9-create_f151_evidence.py` | +304/-0 (new) | byte copy of the prepared evidence script, proved equal to it |

### this commit — F151 R9 C3: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback, per `docs/agents/handback_template.md`; a handback cannot table the commit that writes it (R-0149 pattern) |

## External actions

- Open PR Gate was run before any write: `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
  returned `[]`, the branch was already `feature/f151-worker-adapter-contract`, so no new branch was
  created and no merge was needed.
- `git push origin feature/f151-worker-adapter-contract` → run once, immediately after C2, succeeded on
  the first attempt (`5797b2e42..76fd56865`); no HTTP 500, no retry needed.
- A second push is ordered after this commit (C3), below.
- No worktree was added or removed by this worker. No pull request created, none merged.

## Verification

Interpreter: the repository's configured Python 3. All gates were run once, after A3 and before this
commit, per the block.

Gate 1 — after C2: `git status --porcelain` → empty. `python3 .remedy-wt/f151-r9/prep/verify.py .` →
every line `True`: both commits single-parent, both carry an `F151 R9 Cn` subject, on the right
branch, C1's three paths exact and byte-equal to their `c1-` snapshots, C2's one path exact and
byte-equal to its `c2-` snapshot, `C3` read `absent` (not yet committed), the saved block equal to
`block.md`; last line `ALL True`.

Gate 2 — `.remedy-wt/f151-r9-worker/evidence.exit` → `exit 0 wall 1735.5`.
`.remedy-wt/f151-r9-worker/zip.exit` → `exit 0 wall 18.2`. Both readings and the decisive lines each
job printed are in "Evidence and package" above.

Gate 3 — `python3 -m apps.cli.main integrity check --json` → `"fail_count": 0`, each of 6 checks
`pass`: `handler_import` (`handlers=197`), `live_review_verdict` (`last Gate verdict PASS`),
`plan_consistency` (`unchecked=0, context_complete=False`), `relevant_untracked`
(`untracked=0, relevant=0`), `repo_root_hygiene` (`no reviewer scratch, evidence dir or archive at
the root`), `high_blockers_open` (`no open blocker/high findings`).
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1246', 'R-1281', 'R-1326', 'R-1351', 'R-1353', 'R-1418', 'R-1421', 'R-1425', 'R-1426', 'R-1427', 'R-1428']`
— exactly the eleven ordered ids. `git status --porcelain` → empty.

## Authored-text proofs

C1's three paths and C2's one path are all reviewer-authored text applied this round. Each was
copied from its prepared `c1-*`/`c2-*` file under `.remedy-wt/f151-r9/prep/` by a dedicated `python3`
script under `.remedy-wt/f151-r9-worker/` (`c1_copy.py`, `c2_copy.py`), each copy proved
byte-identical by direct bytes equality immediately after the copy and before `git add`; all four
read `True`. `block.md` itself was separately checked: line count `121` and sha256
`1951da94726c3f3ab6a1d3d8b82f702dd7e8a14d49cb133462cb45b7a56e6966`, matching the digest given in the
prompt and `digests.txt` — confirmed again by `verify.py`'s own "the saved block equals block.md"
check, which read `True`.

## Deviations & assumptions

None. `git branch --show-current` was run as a standalone command, never joined to another, immediately
before both the C1 and C2 commits, and read `feature/f151-worker-adapter-contract` both times. Two
commits this round, C1 and C2, each exactly the paths its own heading names, followed by this
handback as C3. A1 found no reclaim candidate, so `--apply` was correctly skipped rather than run.
A2 and A3 each ran exactly once and each succeeded on the first attempt, so the block's one-retry
allowance for the zip build was not needed. No file outside the paths named per commit was touched.
No production or test file was edited. No merge, no PR, no STATUS or README edit, no rotation, no
queue edit, no self-use run, no provider call.

## For the operator, in plain sentences

The evidence of this feature was collected fresh at the accepted head and checked by every validator
the closure protocol requires, and it came back clean: the full test selection passed, nothing in it
looked unsafe to publish, and the evidence bundle validated as current. The review package was then
built from that same clean, pushed state and came back ready for review, stored outside this
repository's own checkout in this machine's review-package archive.

## Next

1. Phase 1 rule 1: check whether `.agent/STOP` exists (absent at the time of this handback).
2. Phase 1 rule 2: the Open PR Gate (no pull request is open for this branch yet).
3. The reviewer reviews round 9 and books its verdict in the next round's first commit.
4. The closing round: the Built State, the rotation, SU-078's `consumed_by`, the STATUS flip with the
   README sync, and the pull request, left unmerged.

Operator questions open: 0. Open findings (the set gate 3 reads): `R-1246`, `R-1281`, `R-1326`,
`R-1351`, `R-1353`, `R-1418`, `R-1421`, `R-1425`, `R-1426`, `R-1427`, `R-1428` (11).
