# Handback — F041, round 2: book round 1, register R-1105, land the file route and its repair

## Session

SESSION 1 of feature F041 · round 2 · rounds so far 2. This session read the round 2 block whole,
verified its bytes and every payload, booked round 1's gate entry, registered R-1105 and recorded
DECISION F041 D2 (C1a, C1b, C2), wrote S1 to S3 (C3), applied the reviewer's tests unedited (C4),
wrote and red-proved the round's mutation tool in a real worktree (C5), and ran every gate for
real before writing this handback (C6). Context self-assessment: a comfortable amount of context
remains; the round completed inside one session with no blocked handback and no deviation.

For the operator, in plain words: F041's round 2 is now COMPLETE. A job's screenshot bytes and its
whole README are now servable from the cockpit's own file route, behind headers that keep a served
file from ever running as a page, and R-1105 (the static-asset containment gap) is repaired. Every
reviewer test — the new file-route tests, the header tests, the containment test and the upper-case
scheme case — passes unedited, and all seven named mutations are red-proved in a disposable
worktree. Nothing is merged; no pull request exists yet — the branch is pushed and waits for review.

## Range

Review of e1dc49dd7..HEAD (5f61f1fea before this commit)

## Commits

### 34767c939 F041 R2 C1a: copy round 2 block and plan payload into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f041-r2-block.md | +233/-0 | verbatim copy of this round's block |
| .agent/authored/f041-r2-plan.md | +29/-0 | verbatim copy of the plan.md payload |

Measured: 262 insertions (233+29), matching "this block's line count plus 29" (233+29=262) exactly.

### 6eab67e80 F041 R2 C1b: copy round 2 records and tests diffs into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f041-r2-records.diff | +39/-0 | verbatim copy of the records.diff payload |
| .agent/authored/f041-r2-tests.diff | +231/-0 | verbatim copy of the tests.diff payload |

Measured: 270 insertions, matching the block's expected 270 exactly.

### 8bd978b2c F041 R2 C2: book round 1, register R-1105, record D2
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +10/-0 | DECISION F041 D2 appended, via records.diff |
| .agent/live_review.md | +4/-0 | F041 R1 Gate entry and R-1105 registration appended, via records.diff |
| .agent/plan.md | +9/-14 | rewritten to the round's plan.md payload |
| .agent/prose_slips.md | +1/-0 | one dated line appended, via records.diff |

Measured: 10/0, 4/0, 9/14, 1/0 — matches the block's expected table exactly.

### ea2b447b6 F041 R2 C3: serve an artifact's bytes behind no-run headers and fix R-1105
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/artifact_preview.py | +70/-0 | S1: `FILE_MAX_BYTES`, `README_CONTENT_TYPE`, `ArtifactFile`, `read_artifact_file` |
| packages/orchestration/ui_server.py | +50/-1 | S2: `_read_artifact_file`, the structural route, `ARTIFACT_RESPONSE_HEADERS`, `_send_artifact_bytes`; S3: R-1105's one-line fix |

Measured: 70/0, 50/1 — no count was expected by the block for this commit; both stay well under
the 500-insertion cap.

### 74bb5fb9a F041 R2 C4: add the reviewer's file route, header and containment tests
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_artifact_markdown.py | +3/-0 | the upper-case scheme parametrize cases |
| tests/orchestration/test_artifact_preview.py | +70/-0 | `TestReadArtifactFile` |
| tests/ui_server/test_artifacts_route.py | +94/-1 | `TestArtifactFileRoute`, `TestStaticAssetContainment`, the `_ServerHarness` split |
| tests/ui_server/test_command_channel.py | +1/-0 | the file route added to `_walkable_paths` |

Measured: 3/0, 70/0, 94/1, 1/0 — matches the block's expected table exactly.

### 5f61f1fea F041 R2 C5: add the round 2 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f041-r2-mutations.py | +107/-0 | the G4 mutation tool, n1-n7 |

Measured: 107 insertions — no count was expected by the block for this commit.

### (this commit) F041 R2 C6: rewrite handoff for round 2
| Path | Reason |
|---|---|
| .agent/handoff.md | rewritten per the template (self-reference exception, R-0149 pattern) |

## External actions

- `git worktree add --detach .remedy-wt/f041-r2-mut 5f61f1fea` (at C5): exit 0. Mutation tool run
  (see Verification, G4). `git worktree remove --force .remedy-wt/f041-r2-mut` then `git worktree
  prune`: exit 0. `git worktree list | wc -l`: 64 before and after, matching the step-4 reading.
- `git push` (this commit, C6): outcome reported in the reply, since C6 cannot contain it.
- No `gh pr create`, no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push, no
  `git stash`, no reset of a pushed commit.

## Verification

**G1 TRANSPORT** — every payload verified against the PAYLOADS table before use:

| file | lines | bytes | sha256 | match |
|---|---|---|---|---|
| records.diff | 39 | 12108 | 9d86132434a77f544e32b21adedd4f10b5af6dbad00bdd2cbf7c1255872b6fa5 | exact |
| tests.diff | 231 | 11226 | 80730dd9ac114ab797a3bedb9f1dc8e4636abf1096b77cde28e48ad0b341bd28 | exact |
| plan.md | 29 | 970 | 777c82411db01589eac3f140f0a20b871f4b48b105d83e0d736c630b967d45cc | exact |

Each `.agent/authored/f041-r2-*` copy read back with `git show <commit>:<path>` and compared byte
for byte with its source:

| committed path | commit | bytes | sha256 | identical to source |
|---|---|---|---|---|
| .agent/authored/f041-r2-block.md | 34767c939 | 17440 | b5e59f32ee0ff2eef7f44b91f2bd4560d72d8ba638d9dc1fcf2ef2e27280b9ec | True |
| .agent/authored/f041-r2-plan.md | 34767c939 | 970 | 777c82411db01589eac3f140f0a20b871f4b48b105d83e0d736c630b967d45cc | True |
| .agent/authored/f041-r2-records.diff | 6eab67e80 | 12108 | 9d86132434a77f544e32b21adedd4f10b5af6dbad00bdd2cbf7c1255872b6fa5 | True |
| .agent/authored/f041-r2-tests.diff | 6eab67e80 | 11226 | 80730dd9ac114ab797a3bedb9f1dc8e4636abf1096b77cde28e48ad0b341bd28 | True |

**G2 THE RECORDS AND THE TESTS** — every reading equals the reviewer's simulation-tree reading
exactly:

| path | at | bytes | sha256 | match |
|---|---|---|---|---|
| .agent/decisions.md | C2 (8bd978b2c) | 2455145 | c9aac5a1c21717634f3a27aa8d8d0e070b8fb8ccff5bd629b0bf73727c01ad0d | exact |
| .agent/live_review.md | C2 (8bd978b2c) | 298288 | 74e64663de3580a93af28dd0407cb9fd0da6e8ac15df417c2aa1ae00b2b68f9c | exact |
| .agent/plan.md | C2 (8bd978b2c) | 970 | 777c82411db01589eac3f140f0a20b871f4b48b105d83e0d736c630b967d45cc | exact |
| .agent/prose_slips.md | C2 (8bd978b2c) | 376997 | 7062b8ca9e665ec060b9e271dc13f8f734f2f8b74d2d42b27b2578595cee6ace | exact |
| tests/orchestration/test_artifact_markdown.py | C4 (74bb5fb9a) | 13014 | 705f576bbb1a42cb5807ba01f28d8f70f70a357691e86148a1a00086fe4e5825 | exact |
| tests/orchestration/test_artifact_preview.py | C4 (74bb5fb9a) | 9865 | df7ea8ed899bb6dbc8a3db797c9901e54571b982e72c9db36f96ac57028fa211 | exact |
| tests/ui_server/test_artifacts_route.py | C4 (74bb5fb9a) | 9277 | 1b10b44b902e9d80717f42ee2e2322205f81bd2c64cadbf64317c873bda445a0 | exact |
| tests/ui_server/test_command_channel.py | C4 (74bb5fb9a) | 103129 | 9a01b127bda1f16d1f9b4310fc7ddb6f8988520a1a6d876f2cca2b0993171d77 | exact |

`open_finding_ids` from `scripts/rotate_live_review.py`, over `.agent/live_review.md` read with
`git show`: at `e1dc49dd7` → `[]`; at C2 (`8bd978b2c`) → `['R-1105']` — both match the reviewer's
stated readings exactly.

**G3 THE CODE AND THE TESTS**

`python3 -m ruff check` on all seven named files (both production modules, all four named test
files, the mutation tool), at C5: `All checks passed!`, REAL_EXIT=0.

The whole diff of `packages/orchestration/ui_server.py` at C3 is reproduced in full above the
Commits table's own reading of `+50/-1`: `_read_artifact_file` (directly after
`_build_artifacts_json`), the structural route (directly before the final 404 fallback),
`ARTIFACT_RESPONSE_HEADERS` and `_send_artifact_bytes` (directly before `_MIME_TYPES`), and
R-1105's one-line containment fix in `_serve_static` — nothing else in the file changes.

At C5, in the primary checkout, serially, the full ordered selection:
```
python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_artifact_markdown.py tests/orchestration/test_artifact_preview.py tests/ui_server/test_artifacts_route.py tests/ui_server/test_command_channel.py tests/ui_server/test_live_state.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py
```
`SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine`, then `738 passed, 1 skipped in
84.30s`. REAL_EXIT=0 — matches the reviewer's stated reading exactly (`738 passed, 1 skipped`),
same one SKIPPED line.

`--collect-only -q` node counts: `test_artifact_markdown.py` 108, `test_artifact_preview.py` 39,
`test_artifacts_route.py` 14 — match the reviewer's stated 108/39/14 exactly.

`python3 -m apps.cli.main integrity check --json`, at C5: **all six checks `pass`**, `fail_count:
0`, `ok: true`. REAL_EXIT=0.

**G4 THE RED PROOFS** — run in a worktree ADDED at C5:

`git worktree add --detach .remedy-wt/f041-r2-mut 5f61f1fea`: exit 0.
`python3 -B .agent/authored/f041-r2-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f041-r2-mut`,
whole output:
```
CONTROL (unmutated, first):
  tests/ui_server/test_artifacts_route.py: exit=0 failed=0
  tests/orchestration/test_artifact_preview.py: exit=0 failed=0
n1: exit=1 failed=1 caught=True
restored byte-identical: True
n2: exit=1 failed=2 caught=True
restored byte-identical: True
n3: exit=1 failed=2 caught=True
restored byte-identical: True
n4: exit=1 failed=5 caught=True
restored byte-identical: True
n5: exit=1 failed=1 caught=True
restored byte-identical: True
n6: exit=1 failed=1 caught=True
restored byte-identical: True
n7: exit=1 failed=1 caught=True
restored byte-identical: True
CONTROL (unmutated, last):
  tests/ui_server/test_artifacts_route.py: exit=0 failed=0
  tests/orchestration/test_artifact_preview.py: exit=0 failed=0
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
All seven mutations caught (nonzero exit), all seven restorations byte-identical. `git worktree
remove --force .remedy-wt/f041-r2-mut` then `git worktree prune`: exit 0; `git worktree list | wc
-l`: 64, matching the step-4 reading.

**G5** — reported in the reply (this file cannot contain the push outcome per the block).

## Authored-text proofs

All four reviewer-authored texts applied this round, each compared disk-to-disk against its
committed `.agent/authored/f041-r2-*` blob (read via `git show <sha>:<path>`):

| authored file | applied as | result |
|---|---|---|
| f041-r2-block.md | (verification copy of this block, at 34767c939) | IDENTICAL |
| f041-r2-plan.md | rewrote `.agent/plan.md` at C2 | IDENTICAL |
| f041-r2-records.diff | `git apply`'d, committed at C2 | applied clean, `--check` exit 0, real apply exit 0 |
| f041-r2-tests.diff | `git apply`'d, committed at C4 | applied clean, `--check` exit 0, real apply exit 0 |

## Deviations & assumptions

None. Every payload matched its stated line count, byte count and sha256 before use; every
`git apply --check` and real apply exited 0; every commit's `git show --numstat` matched the
block's expected table exactly where one was given; every gate (G1-G4) matched the reviewer's
stated reading exactly; ruff was clean; all seven named mutations were caught and restored
byte-identical; the tracked path set at `git diff --name-only e1dc49dd7` (before C6) was exactly
the `.agent/authored/f041-r2-*` copies and tool, `.agent/decisions.md`, `.agent/live_review.md`,
`.agent/plan.md`, `.agent/prose_slips.md`, `packages/orchestration/artifact_preview.py`,
`packages/orchestration/ui_server.py`, and the four test files — nothing from `apps/ui/`,
`.agent/context.md`, `.agent/candidates.md`, `.agent/operator_questions.md` or `README.md` was
touched. No worktree, branch or stash other than the round's own `.remedy-wt/f041-r2-mut` (added
and removed by this round, per its own instructions) was touched.

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk at the start of the next session.
2. Round 2 is COMPLETE and awaits the review of round 2.
3. T002 next: the preview commands, their intent and its consumer.

Open findings: 1 (R-1105, repaired this round and awaiting its resolution). Operator-questions
count: 1 (`.agent/operator_questions.md`, unanswered, carried forward unchanged by this round).
