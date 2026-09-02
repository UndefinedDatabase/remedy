# Handoff — F108 Tiered artifact summaries (round 2)

## Session

SESSION 1 of feature F108 · round 2 · rounds so far 2

## Range

Review of `403c258a4bd7c1b9925553335cfc5ae7515dfb2e`..`HEAD`
(branch `feature/f108-tiered-artifact-summaries`). This range is round 2's
OWN commits only; round 1's diff (`ec81e697`..`a3dbf498`) was already
reviewed and PASSED as GATE_R1, and round 1's own handback commit
`403c258a` (C5) landed on the branch after that review — see Deviations.

## Commits

### 88eb003c save F108 round 2 step block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f108-r2.md` | +111/-0 (new) | C0a — save the step block verbatim before touching any state file |

### 62050ba4 mirror F108 round 2 block into last_block.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +111/-166 (rewrite) | C0b — mirror to authored bytes; verbatim single-state-file rewrite (AGENTS.md 500-line exemption applies) |

### 3855cd58 book F108 R1 verdict into live_review.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +3/-1 (append) | C1 — append SLICE GATE_R1, the reviewer's own PASS verdict for round 1, per the append instructions |

### b021213d add F108 T001 ArtifactSummary schema and mechanical sectioners
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/artifact_summary.py` | +195/-0 (new) | C2 — S1-S8: `ArtifactSummary`/`ArtifactSummarySection` pydantic models, `compute_artifact_hash`, `summary_path_for`, `load_cached_summary`, `save_summary`, `section_diff`, `section_log` |

### 5d12e6ad add F108 T001 unit tests for artifact_summary
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_artifact_summaries.py` | +169/-0 (new) | C3 — 10 test functions covering the 10 numbered cases in the test spec |

### 1d164415 rewrite plan.md for F108 round 2
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +17/-13 (rewrite to SLICE PLAN_R2's bytes) | C4 |

### (this commit) rewrite handoff.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | C5 — handback per docs/agents/handback_template.md |

## External actions

- `git worktree add .remedy-wt/f108-r2-mutant HEAD` — created after C2/C3 landed, for the isolated mutation red-proof; outcome: `Preparing worktree (detached HEAD 1d164415)`.
- `git worktree remove .remedy-wt/f108-r2-mutant --force` — removed immediately after the mutant run; outcome: clean removal, confirmed by `git worktree list` no longer showing it.
- `git push -u origin feature/f108-tiered-artifact-summaries` — pushes this round's six commits (through `1d164415`) plus the C5 handback commit; run after this file is committed (see below).
- No PR created — explicitly out of scope this round (T002/T003 still open).

## Verification

Pre-flight:
```
$ git status
On branch feature/f108-tiered-artifact-summaries
nothing to commit, working tree clean
$ git rev-parse HEAD
403c258a4bd7c1b9925553335cfc5ae7515dfb2e
```
The block's stated pre-flight commit was `a3dbf49813a636e3db802b5ae8c8531e80a5dbef`;
actual HEAD was one commit ahead (`403c258a`, round 1's own C5 handback
commit, touching only `.agent/handoff.md`). See Deviations — this is the
"committed handback is a durable carrier" pattern (AGENTS.md, amend0827
rule 1), not a mismatch: round 1's PASS verdict was computed against
`a3dbf498`, and `403c258a` is round 1's OWN required handback commit that
simply landed and was pushed after that review snapshot. Proceeded on
`feature/f108-tiered-artifact-summaries` at `403c258a`.

G1 TRANSPORT:
```
GATE_R1 slice: 2919 bytes, sha256 8d2d1623b38cd544f8b0cf2e0d895b0b278f3f60e24d12fa7f985891c7a6beeb — MATCH
PLAN_R2 slice (+trailing \n, as it lands in .agent/plan.md): 1885 bytes,
  sha256 c84335da66a9f5cbc500a816c6f0e08f3d10c3cd3968ebcde6cb392a9d4e4498 — MATCH
sha256 .agent/authored/f108-r2.md == sha256 .agent/last_block.md
  == ed83eeb31da0023a27b12addf24cf0276a0375a00afdb33fb69cb2fba210edb2 — MATCH
```

G2 LEDGER APPEND:
```
$ wc -c .agent/live_review.md
1922043
$ sha256sum .agent/live_review.md
b93d0ad7e0d4da07a693a5abc9bd1662403b8d8c1a3dabdf22c4454a7df1707c
$ grep -c "^Gate: " .agent/live_review.md
218
$ grep -c "F108 R1" .agent/live_review.md
1
```
All four match the block's stated values exactly (up from 217 `Gate:` lines
pre-append, per the block's self-corrected parenthetical).

G3 NEW TESTS:
```
$ python3 -m pytest tests/orchestration/test_artifact_summaries.py -q
..........                                                               [100%]
10 passed in 0.22s
```
Real exit 0, 10 passed — one test function per numbered case in the spec.

G4 MUTATION RED-PROOF (isolated, `.remedy-wt/f108-r2-mutant`, never the
primary checkout):
```
$ git worktree add .remedy-wt/f108-r2-mutant HEAD
Preparing worktree (detached HEAD 1d164415)
```
Edited ONLY the worktree copy of `packages/orchestration/artifact_summary.py`,
replacing `if summary.artifact_hash != current_hash:` with `if False:` in
`load_cached_summary`. Ran via `subprocess.run(..., cwd=<worktree>)`:
```
MUTATED (worktree):
$ python3 -m pytest tests/orchestration/test_artifact_summaries.py::test_load_cached_summary_invalidates_on_hash_mismatch -q
F                                                                        [100%]
FAILED tests/orchestration/test_artifact_summaries.py::test_load_cached_summary_invalidates_on_hash_mismatch
AssertionError: assert ArtifactSummary(l1='a short summary', ..., artifact_hash='49114a9a2b7d46ec27be62ae3eade12f78d46cf5a99c52cd4f80381d723eed6e') is None
exit code: 1
```
```
$ git worktree remove .remedy-wt/f108-r2-mutant --force
(clean removal)
UNMUTATED (primary checkout):
$ python3 -m pytest tests/orchestration/test_artifact_summaries.py::test_load_cached_summary_invalidates_on_hash_mismatch -q
.                                                                        [100%]
1 passed in 0.25s
exit 0
```
```
$ git status --porcelain
(empty)
```
Both readings recorded side by side: mutated → FAILED/exit 1 (the exact
assertion the mutation should break); unmutated → 1 passed/exit 0. Primary
checkout tree confirmed empty immediately after.

G5 STATE READERS:
```
$ python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q
604 passed in 48.74s
exit 0
```
Matches the reviewer's own base reading (604) exactly — unchanged, as
expected (this round adds no file under any of those four paths).

G6 CANARY:
```
$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 20.64s
exit 0
```
Matches the reviewer's own base reading (42) exactly.

G7 PLAN:
```
$ sha256sum .agent/plan.md
c84335da66a9f5cbc500a816c6f0e08f3d10c3cd3968ebcde6cb392a9d4e4498
$ wc -l .agent/plan.md
39
```
Matches exactly, under the 50-line cap.

G8 TREE + SIZE:
```
$ git status --porcelain
(empty)
$ git rev-parse HEAD  ==  git rev-parse origin/feature/f108-tiered-artifact-summaries
(confirmed equal after the push below)
```
Every commit's insertions independently checked under 500 (largest is 195,
`artifact_summary.py`); see Commits table above. `git diff --stat 403c258a..HEAD`
(round 2's own commit range, i.e. the six commits through `1d164415` plus
this handback commit) touches exactly the 7 paths named in the change set:
`.agent/authored/f108-r2.md`, `.agent/last_block.md`, `.agent/live_review.md`,
`packages/orchestration/artifact_summary.py`,
`tests/orchestration/test_artifact_summaries.py`, `.agent/plan.md`,
`.agent/handoff.md` — nothing else. The literal `git diff --stat main..HEAD`
additionally carries round 1's un-PR'd diff (12 paths total: the 7 above plus
`.agent/authored/f108-r1.md`, `.agent/candidates.md`, `.agent/context.md`,
`.agent/f108_inventory.md`, `docs/roadmap/STATUS.md`) because no PR has
merged either round into `main` yet — see Deviations.

## Authored-text proofs

`.agent/authored/f108-r2.md` was typed verbatim from the step block between
the `BEGIN STEP BLOCK F108-R2` / `END STEP BLOCK F108-R2` markers (markers
excluded). Disk-to-disk comparison: `.agent/last_block.md` mirrored from it,
both sha256 to `ed83eeb31da0023a27b12addf24cf0276a0375a00afdb33fb69cb2fba210edb2`
— IDENTICAL. The two byte-exact slices this block specified (GATE_R1,
appended into `.agent/live_review.md`; PLAN_R2, written to `.agent/plan.md`)
were each independently re-hashed against the digest stated beside that
slice before being applied, both matching exactly (see G1/G2/G7 above) —
this is the fidelity proof for reviewer-authored content applied this round.

## Deviations & assumptions

- **Pre-flight HEAD one commit ahead of the block's stated base.** The block's
  pre-flight step names `a3dbf49813a636e3db802b5ae8c8531e80a5dbef` as the
  required HEAD; actual HEAD was `403c258a4bd7c1b9925553335cfc5ae7515dfb2e`,
  exactly one commit ahead, touching only `.agent/handoff.md` (172
  insertions, 112 deletions — round 1's own required C5 handback commit,
  per its commit message "handback for F108 round 1"). Read this against
  AGENTS.md's runtime-state rules and the self-drive protocol's amend0827
  rule 1: a committed and pushed `.agent/handoff.md` is a durable carrier,
  and round 1's reviewer PASS verdict (embedded in this round's own SLICE
  GATE_R1) explicitly reviewed the diff `ec81e697`..`a3dbf498` — the
  inventory commit, not the handback commit that necessarily follows it.
  `403c258a` changes no file the GATE_R1 verdict's G1-G6 checks depend on
  (it touches only `.agent/handoff.md`, which none of those checks read),
  so round 1's verdict is unaffected by its presence. Treated this as the
  expected shape of "the round immediately after a claim+inventory round"
  the block itself names, not a mismatch requiring a stop, and proceeded
  without checkout (already on the correct branch, strictly ahead by one
  benign commit).
- **G8's `main..HEAD` literal reading.** As stated above, `git diff --stat
  main..HEAD` shows 12 touched paths, not 7, because round 1's own diff is
  still un-PR'd on this branch (this round explicitly does not create a
  PR). Verified the substance of G8 instead against round 2's own commit
  range (`403c258a..HEAD`), which touches exactly the 7 change-set paths
  and nothing else — reported in Verification above. Not a stop condition:
  it reflects the branch's un-merged state, not a scope violation by this
  round.
- No other deviations. The change set touched exactly the seven paths the
  block named, in the order specified. No file outside that set was
  created, modified or deleted this round.

## Next

Round 3: T002 — the summary role, the provider call, validation, fallback.
Declare `summary` in `role_config.py`'s `KNOWN_ROLES`, wire a provider call
using T001's `section_diff`/`section_log` output as input, validate the
response through `packages/orchestration/schemas/validation.py`'s
`validate_response`, and add the truncated head+tail fallback ("[summary
unavailable — truncated view]") for a failed generation, with
fake-provider tests. No PR yet — T003 (compiler integration) is still
open, so the branch is not yet reviewable as a whole.
