Goal: Book round 1's verdict into the ledger, then build F108's T001 slice — the `ArtifactSummary` schema, two mechanical sectioners (diff-per-file, log-by-block), and hash-invalidated sibling-file storage/caching — with unit tests, per docs/roadmap/features/T3_F108.md's Task slicing and `.agent/f108_inventory.md`'s findings. This IS a production-code round (SPLIT type, mandatory per §3 round types) — you write the code under AGENTS.md's self-review loop; nothing here is a byte-exact slice except the two `.agent/` state texts named below.

Pre-flight:
    git status
    git rev-parse HEAD    # must equal a3dbf49813a636e3db802b5ae8c8531e80a5dbef, on feature/f108-tiered-artifact-summaries
If not on that branch at that commit, `git checkout feature/f108-tiered-artifact-summaries` and confirm before proceeding.

Bundle (commits, in this exact order):
- C0a: write `.agent/authored/f108-r2.md` (this block, verbatim).
- C0b: mirror `.agent/last_block.md` to the same bytes.
- C1: append SLICE GATE_R1 to `.agent/live_review.md` (append instructions below). This books round 1's own verdict, which cannot record itself — normal for the round immediately after a claim+inventory round.
- C2: new file `packages/orchestration/artifact_summary.py` implementing S1-S8 below.
- C3: new file `tests/orchestration/test_artifact_summaries.py` implementing the test spec below.
- C4: rewrite `.agent/plan.md` to SLICE PLAN_R2's bytes exactly (below).
- C5 (handback): rewrite `.agent/handoff.md` per docs/agents/handback_template.md.

Change set — exactly these paths, nothing else: `.agent/authored/f108-r2.md` (new), `.agent/last_block.md` (rewrite), `.agent/live_review.md` (append), `packages/orchestration/artifact_summary.py` (new), `tests/orchestration/test_artifact_summaries.py` (new), `.agent/plan.md` (rewrite), `.agent/handoff.md` (rewrite).

BEGIN SLICE GATE_R1
Gate: F108 R1 — F108 CLAIMED, THE F106 CLOSURE CANDIDATE DISCHARGED AS R-0762, SOURCE INVENTORY ON DISK. VERDICT PASS. The reviewer independently re-verified round 1's committed diff `ec81e697`..`a3dbf498` against the real files, not the worker's own report. G1 TRANSPORT: `.agent/plan.md`, `.agent/context.md` and `.agent/candidates.md` independently sha256'd at `0dd6bff3e40299db3825b5839a1a117d44eafa5758d36b0fb8b4175bce4283e5` (35 lines), `64f3b87229fd3adb974da27ccb00d83e8cb518edb9a72fa4da30c34f5f5a6b6c` (47 lines) and `3edd7f964bd2da624eafefef8713710567ab52ba1b11c3584ec1ab6ddaa415c0` (14 lines) respectively, all three byte-identical to the reviewer's own scratch originals computed before delegation. G2 STATUS LINE: `docs/roadmap/STATUS.md` line 15 independently confirmed reading exactly `- [~] F108 — Tiered artifact summaries`; `git diff ec81e697..HEAD -- docs/roadmap/STATUS.md` independently re-run and confirmed to touch exactly that one line. G3 LEDGER APPEND: `.agent/live_review.md` independently re-measured at 1919122 bytes, sha256 `7e31a16b69b99faf7ae671410eac695f8cd61082a03ba57f8f43de92db04f16c`; the file's tail independently confirmed byte-equal to the R-0762 slice with the required `\n\n` separator; a negative control (in-memory byte flip of the slice's first byte) independently confirmed produces a different digest, tracked file never mutated; `grep -c "^- R-[0-9]\{4\} — "` independently re-measured at 323 (up from 322), the `Done:` count unmoved at 60, the `DECISION` count unmoved at 21, `R-0762` occurring exactly once. G4 SUITES: independently re-ran all three of the round's own gates from a clean shell — `pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q` (604 passed), `pytest tests/orchestration/test_roadmap_index.py tests/docs/ -q` (325 passed), `pytest tests/cli/test_golden_path.py -q` (42 passed), all real exit 0, matching the round's own base and post readings exactly. G5 THE TREE: `git status --porcelain` empty; HEAD confirmed pushed and equal to `origin/feature/f108-tiered-artifact-summaries` at `a3dbf498`; every commit's insertions independently re-measured under 500. G6 THE INVENTORY: `.agent/f108_inventory.md` spot-checked against the real source for three citations (`DEFAULT_CONTEXT_TOKEN_BUDGET`/`DEFAULT_INLINE_SIZE_CAP_BYTES` at context_compiler.py:143/603, `KNOWN_ROLES` at role_config.py:60-69, `parse_unified_diff_to_view`/`DIFF_VIEW_MAX_BODY_LINES`/`DIFF_VIEW_MAX_FILES` at diff_parser.py:461/131/147) — all three confirmed exact against the real committed files. No deviation found; the worker's one declared deviation (a commit-staging correction caught and fixed before any commit landed) left no trace on the final commit sequence, independently confirmed by `git log --oneline main..HEAD` matching the block's ordered C0a-C5 exactly.
END SLICE GATE_R1
(sha256 of the slice content above, with NO trailing newline: 8d2d1623b38cd544f8b0cf2e0d895b0b278f3f60e24d12fa7f985891c7a6beeb — 2919 bytes, single paragraph)

Append instructions: `.agent/live_review.md` at your round's base (HEAD `a3dbf498`) is 1919122 bytes, sha256 `7e31a16b69b99faf7ae671410eac695f8cd61082a03ba57f8f43de92db04f16c`, ends with the bytes `OPEN.` and no trailing newline. Append exactly `\n\n` then SLICE GATE_R1's bytes, no trailing newline after. Verify independently: result must be 1922043 bytes, sha256 `b93d0ad7e0d4da07a693a5abc9bd1662403b8d8c1a3dabdf22c4454a7df1707c`. If your own measurement does not match, STOP and declare the mismatch rather than committing. `grep -c "^Gate: "` must read 218 (up from 218... wait: up from 217).

BEGIN SLICE PLAN_R2
# Plan — F108 Tiered artifact summaries

Branch: feature/f108-tiered-artifact-summaries, cut from `main` at
`ec81e697bf498a6753d82d7e6a8d3c72467cd5d7`.

## Goal
Oversized artifacts (diffs, logs, reports) get a tiered representation — an
L1 summary, sectioned L2 summaries, and the full reference path — so a
follow-up prompt consumes L1 plus only the relevant L2 sections instead of
the whole artifact. DONE when a fixture long log enters a follow-up prompt
at a fraction of its size with the reference path present, summaries are
generated by the configured cheap route and labeled, and a missing/failed
summary never blocks the run.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| Claim F108, discharge R-0762, inventory | done | round 1 |
| T001 schema + mechanical sectioners + storage/caching + unit tests | done | round 2, `packages/orchestration/artifact_summary.py` |
| T002 generation call + summary role + fallback | pending | next round |
| T003 compiler integration + fixture | pending | later round |

## Next Steps
1. Round 3: declare the `summary` role in `role_config.py`'s `KNOWN_ROLES`,
   wire a provider call using T001's sections as input, validate the
   response with `packages/orchestration/schemas/validation.py`'s
   `validate_response`, and add the fallback (truncated head+tail with the
   "[summary unavailable — truncated view]" marker) for a failed
   generation.
2. T003: hook the new representation into
   `packages/orchestration/context_compiler.py`'s selection/rendering (a
   third `rendering` value beside `"full"`/`"signatures"`), build the
   long-log fixture, and record the size comparison.
3. Integration gate (full suite, both required runs) before closure.

## Risks
- T002's fallback rule ("never silent, never blocking") is the one Design
  requirement T001 does not touch at all; round 3 owns it fully.
END SLICE PLAN_R2
(sha256 of the slice content above, exactly as it must land in `.agent/plan.md`: c84335da66a9f5cbc500a816c6f0e08f3d10c3cd3968ebcde6cb392a9d4e4498 — 1885 bytes, 39 lines)

PRODUCTION CODE SPEC — new file `packages/orchestration/artifact_summary.py`. Follow this repository's existing style for a small schema/utility module (see `packages/orchestration/schemas/validation.py` for the docstring and import style: `from __future__ import annotations`, module docstring stating what F108/T001 this is and the rules it enforces). Implement exactly these public names with exactly this behavior — you choose the internal implementation, variable names, and helper decomposition, but the public contract below is fixed:

S1. `class ArtifactSummarySection(BaseModel)` — pydantic model, fields: `section: str`, `span_ref: str`, `summary: str`.

S2. `class ArtifactSummary(BaseModel)` — pydantic model, fields: `l1: str`, `l2: list[ArtifactSummarySection]`, `full_ref: str`, `generator: str`, `generated_at: str`, `artifact_hash: str`. This is the `artifact.summary.json` schema the feature file's Design section names; T002 (not this round) is what populates `generator`/`generated_at`/`summary` text via a real provider call — this round's tests may put any string in those fields.

S3. `def compute_artifact_hash(artifact_bytes: bytes) -> str` — sha256 hex digest of the given bytes. No input makes this raise (any `bytes`, including `b""`, is valid).

S4. `def summary_path_for(artifact_path: Path) -> Path` — returns the sibling cache path: `artifact_path`'s own name with `.summary.json` appended (e.g. `workspace.diff` → `workspace.diff.summary.json`), same parent directory. Pure path arithmetic, no filesystem access, never raises.

S5. `def load_cached_summary(artifact_path: Path) -> ArtifactSummary | None` — returns the cached `ArtifactSummary` if and only if (a) `summary_path_for(artifact_path)` exists and parses as valid JSON matching the schema, (b) `artifact_path` itself exists, and (c) the parsed summary's `artifact_hash` field equals `compute_artifact_hash(artifact_path.read_bytes())` — the artifact's CURRENT bytes. Any of: missing cache file, missing artifact file, unparseable/invalid cache JSON, or a hash mismatch → return `None` (never raise; catch the parse/validation failure narrowly, never a bare `except:`). Put a one-line `# WHY` comment directly above the hash comparison stating that a hash mismatch means the artifact changed since the summary was generated and must be treated exactly like a missing cache (the Design section's "invalidated by artifact hash" rule) — this is the ONE fact that comment must carry, no more.

S6. `def save_summary(artifact_path: Path, summary: ArtifactSummary) -> None` — writes `summary` as JSON to `summary_path_for(artifact_path)`, overwriting any existing file. Uses pydantic's own JSON serialization (this is a round-trip of Remedy's OWN previously-validated data, not an untrusted provider response — do not route this through `schemas/validation.py`'s `validate_response`, which is for parsing raw provider text; that entry point is T002's, not this round's).

S7. `def section_diff(diff_text: str) -> list[dict[str, str]]` — mechanically splits a unified diff into one entry per file, in the diff's own file order. Each entry: `{"section": <file path>, "span_ref": f"file:{path}", "text": <that file's own diff text, its `diff --git` header line included>}`. Split on lines matching `^diff --git a/(\S+) b/(\S+)$` (the boundary every git unified diff in this repository uses); the file path is the `b/` side (or the `a/` side if `b/` is `/dev/null` for a deletion — mirror `diff_parser.py`'s `_strip_side_prefix` idea inline rather than importing that private helper). A diff with NO such boundary at all (a bare unified diff with no git header, or an empty string) returns a single entry `{"section": "(unsectioned)", "span_ref": "file:(unsectioned)", "text": diff_text}` — for `diff_text == ""` this means one entry whose `"text"` is `""`, never an empty list and never a raise. Do not import or reuse `parse_unified_diff_to_view` — that function returns rendering-oriented structured hunk data for the diff VIEWER (a different consumer with different needs); duplicate the small file-boundary split instead of coupling to it, which keeps this sectioner mechanical and independent per the Design section's "sectioning is mechanical first" language.

S8. `def section_log(log_text: str, chunk_lines: int = 200) -> list[dict[str, str]]` — mechanically splits free-text log content into blocks. PRIMARY rule: split on any run of two or more consecutive newlines (a blank-line gap) — the "marker block" boundary for logs with no structured timestamp format. Each resulting non-empty block becomes one entry: `{"section": f"block-{i}", "span_ref": f"lines:{start}-{end}", "text": <block text>}` (1-indexed, inclusive line numbers, `i` 0-indexed for the section label). FALLBACK rule: if the primary split produces exactly ONE block (no blank-line boundary found at all) and that block has more than `chunk_lines` lines, re-split it into fixed-size chunks of `chunk_lines` lines each (last chunk may be shorter), same entry shape, section labels `block-0`, `block-1`, ... . `log_text == ""` returns `[]`. Never raises for any string input.

Import `BaseModel` from `pydantic`, matching `packages/orchestration/schemas/validation.py`'s import line. Do not read `REMEDY_DATA_DIR` or any data-root resolution in this module — every function above takes a `Path` the CALLER already resolved, so this module needs no path-utils reuse and stays outside the repo-wide single-reader/single-implementation guards `.agent/context.md` names. No bare `except:` anywhere.

TEST SPEC — new file `tests/orchestration/test_artifact_summaries.py`, using `tmp_path` (pytest fixture) for filesystem tests, no network, no `REMEDY_DATA_DIR` involvement. Cover, at minimum (you may add more; do not omit any of these):
1. `compute_artifact_hash` returns different digests for different byte content and the same digest for the same content (deterministic).
2. `load_cached_summary` returns `None` when no cache file exists yet.
3. Round trip: `save_summary` then `load_cached_summary` on the SAME unmodified artifact returns an `ArtifactSummary` equal (field-by-field) to what was saved.
4. **`test_load_cached_summary_invalidates_on_hash_mismatch`** (this exact test name — the mutation red-proof below targets it by name): save a summary while the artifact holds content A (so `artifact_hash` matches A's hash), then overwrite the artifact file's bytes with different content B on disk, then call `load_cached_summary` again — assert it returns `None` (not the stale object), because B's hash no longer matches the cached `artifact_hash`.
5. `section_diff` on a small fixture diff touching exactly two files: assert exactly 2 entries, correct `span_ref` for each (naming the right file), and that each entry's `"text"` contains that file's own `diff --git` header line and does NOT contain the other file's path string.
6. `section_diff` on a diff/text with no `diff --git` header: assert exactly one entry with `"section": "(unsectioned)"`.
7. `section_diff("")` returns one entry with `"text": ""`.
8. `section_log` on text containing 3 blocks separated by blank lines: assert exactly 3 entries in order.
9. `section_log` on a single blob of at least 450 lines with NO blank line anywhere: assert the fixed-chunk fallback fires — more than one entry, each `<= chunk_lines` lines, and the entries' texts concatenated (in order) reconstruct the original content.
10. `section_log("")` returns `[]`.

Done when (run every command for real and record the real exit code; never report "green" as a word):
G1 TRANSPORT — sha256 `.agent/authored/f108-r2.md` and `.agent/last_block.md`, confirm equal to each other; confirm the SLICE GATE_R1 and SLICE PLAN_R2 regions inside the committed authored file match the digests stated beside each above.
G2 LEDGER APPEND — `.agent/live_review.md` sha256 equals `b93d0ad7e0d4da07a693a5abc9bd1662403b8d8c1a3dabdf22c4454a7df1707c` at 1922043 bytes; `grep -c "^Gate: "` reads 218 (up from 217); `grep -c "F108 R1"` in the file reads exactly 1.
G3 NEW TESTS — `python3 -m pytest tests/orchestration/test_artifact_summaries.py -q` real exit 0; report the real pass count (at least the 10 cases above, one test function each or more).
G4 MUTATION RED-PROOF (isolated per self_drive_protocol.md guardrail G5 — a DISPOSABLE worktree, never the primary checkout): `git worktree add .remedy-wt/f108-r2-mutant HEAD` (after C2/C3 are committed), inside that worktree edit ONLY `packages/orchestration/artifact_summary.py`'s `load_cached_summary` to replace the hash-comparison condition (`summary.artifact_hash != current_hash`, or whatever exact expression you wrote for it) with the literal `False`, run `python3 -m pytest tests/orchestration/test_artifact_summaries.py::test_load_cached_summary_invalidates_on_hash_mismatch -q` there with `cwd` set to the worktree path (use `subprocess.run(..., cwd=<worktree>)`, not shell `cd`, which does not reliably take effect in this sandbox) — record the real exit code (expect non-zero / FAILED) and the specific assertion that failed. Then `git worktree remove .remedy-wt/f108-r2-mutant --force` and re-run the SAME test in the PRIMARY checkout to confirm it is green there (exit 0) — report both readings side by side, mutated and unmutated. Immediately after, run `git status --porcelain` in the primary checkout and confirm empty.
G5 STATE READERS — `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q`, real exit 0 (reviewer's own base reading: 604 passed — this round adds no new file under any of those four paths, so the count should be unchanged; report your own real number regardless).
G6 CANARY — `pytest tests/cli/test_golden_path.py -q`, real exit 0 (reviewer's own base reading: 42 passed).
G7 PLAN — `.agent/plan.md` sha256 equals `c84335da66a9f5cbc500a816c6f0e08f3d10c3cd3968ebcde6cb392a9d4e4498`, 39 lines (under the 50-line cap).
G8 TREE + SIZE — `git status --porcelain` empty; HEAD pushed and equal to `origin/feature/f108-tiered-artifact-summaries`; every commit's insertions under 500 lines; `git diff --stat main..HEAD` touches exactly the 7 paths named in the change set above, nothing else.

Handback: write the completion report inline in your final message AND rewrite `.agent/handoff.md` per docs/agents/handback_template.md (Session, Range, Commits per-commit table, External actions, Verification with real transcripts including BOTH mutation readings, Authored-text proofs, Deviations & assumptions, Next). The Session line reads `SESSION 1 of feature F108 · round 2 · rounds so far 2`. Do not create a pull request this round — T002 and T003 are still open, so the branch is not yet reviewable as a whole; state that under Next ("Round 3: T002 — the summary role, the provider call, validation, fallback").
