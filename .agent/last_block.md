Goal: Book round 2's verdict into the ledger, then build F108's T002 slice — declare the `summary` provider-call role, wire a schema-validated generation call over T001's sections, and add the "never silent, never blocking" fallback — with fake-provider tests. This IS a production-code round (SPLIT type, mandatory). You write the code under AGENTS.md's self-review loop; nothing here is byte-exact except the two `.agent/` state texts named below.

Pre-flight:
    git status
    git rev-parse HEAD    # branch feature/f108-tiered-artifact-summaries; report actual HEAD
If HEAD is not the branch tip you expect, or `git status --porcelain` is non-empty, STOP and declare it in the handoff rather than proceeding.

Bundle (commits, in this exact order):
- C0a: write `.agent/authored/f108-r3.md` (this block, verbatim).
- C0b: mirror `.agent/last_block.md` to the same bytes.
- C1: append SLICE GATE_R2 to `.agent/live_review.md` (append instructions below).
- C2: edit `packages/orchestration/role_config.py` per S15 below.
- C3: edit `packages/orchestration/artifact_summary.py`, ADDING (not removing anything from T001) the S9-S14 code below.
- C4: extend `tests/orchestration/test_artifact_summaries.py` with the new test functions described below (append new test functions to the existing file; do not remove or rewrite the T001 tests already there).
- C5: rewrite `.agent/plan.md` to SLICE PLAN_R3's bytes exactly (below).
- C6 (handback): rewrite `.agent/handoff.md` per docs/agents/handback_template.md.

Change set — exactly these paths, nothing else: `.agent/authored/f108-r3.md` (new), `.agent/last_block.md` (rewrite), `.agent/live_review.md` (append), `packages/orchestration/role_config.py` (edit), `packages/orchestration/artifact_summary.py` (edit, additive), `tests/orchestration/test_artifact_summaries.py` (edit, additive), `.agent/plan.md` (rewrite), `.agent/handoff.md` (rewrite).

BEGIN SLICE GATE_R2
Gate: F108 R2 — T001 BUILT: ArtifactSummary SCHEMA, MECHANICAL DIFF/LOG SECTIONERS, HASH-INVALIDATED STORAGE, TEN UNIT TESTS. VERDICT PASS. The reviewer independently re-verified round 2's committed diff `403c258a`..`3d92b5cc` against the real files, not the worker's own report. G1 TRANSPORT: `.agent/plan.md` independently sha256'd at `c84335da66a9f5cbc500a816c6f0e08f3d10c3cd3968ebcde6cb392a9d4e4498` (39 lines), matching the reviewer's own scratch original; `.agent/live_review.md`'s GATE_R1 append independently confirmed byte-equal with the required `\n\n` separator, no trailing newline. G2 LEDGER APPEND: `.agent/live_review.md` independently re-measured at 1922043 bytes, sha256 `b93d0ad7e0d4da07a693a5abc9bd1662403b8d8c1a3dabdf22c4454a7df1707c`; `grep -c "^Gate: "` independently re-measured at 218 (up from 217), `grep -c "F108 R1"` exactly 1. G3 THE MODULE: `packages/orchestration/artifact_summary.py` (195 lines) independently read in full — `ArtifactSummary`/`ArtifactSummarySection` pydantic models, `compute_artifact_hash`, `summary_path_for`, `load_cached_summary` (hash-invalidated, narrow exception handling, no bare `except:`), `save_summary`, `section_diff` (file-boundary split, independent of `diff_parser.py`'s heavier hunk structure as ordered), `section_log` (blank-line blocks + fixed-chunk fallback) — matches the S1-S8 spec exactly, no scope creep, no `REMEDY_DATA_DIR` access. G4 THE TESTS: `python3 -m pytest tests/orchestration/test_artifact_summaries.py -q` independently re-run, real exit 0, 10 passed, matching the round's own reading. G5 MUTATION RED-PROOF: independently reproduced in a fresh disposable worktree (`.remedy-wt/f108-review-mutant`, removed after) — replacing `load_cached_summary`'s hash-comparison condition with `False` made `test_load_cached_summary_invalidates_on_hash_mismatch` FAIL (real exit 1, the exact AssertionError showing the stale object returned instead of `None`); the same test independently re-confirmed green (real exit 0) in the unmutated primary checkout immediately after, tree confirmed clean throughout. G6 SUITES: independently re-ran both of the round's own remaining gates from a clean shell — `pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q` (604 passed) and `pytest tests/cli/test_golden_path.py -q` (42 passed), both real exit 0, matching the round's own base and post readings exactly (unchanged, as expected — no path under either gate's scope was touched). G7 THE TREE: `git status --porcelain` empty; HEAD confirmed pushed and equal to `origin/feature/f108-tiered-artifact-summaries` at `3d92b5cc`; every commit's insertions independently re-measured under 500 (largest 195); `git diff --stat 403c258a..HEAD` independently confirmed to touch exactly the 7 declared paths, nothing else. No deviation found; the worker's two declared deviations (HEAD one commit ahead of the block's stated pre-flight base, and the `main..HEAD` vs the round's own range for G8's path-set reading) were both correctly reasoned and left no false claim on the record — independently confirmed against `git log --oneline main..HEAD` and the per-commit diffs.
END SLICE GATE_R2
(sha256 of the slice content above, with NO trailing newline: d8f06fdbe3e7541a9438c1c62a91fb0e06cec5af5d91760a42dadc873c5ec0d6 — 3240 bytes, single paragraph)

Append instructions: `.agent/live_review.md` at your round's base is 1922043 bytes, sha256 `b93d0ad7e0d4da07a693a5abc9bd1662403b8d8c1a3dabdf22c4454a7df1707c`, ends with the bytes `ctly.` and no trailing newline. Append exactly `\n\n` then SLICE GATE_R2's bytes, no trailing newline after. Verify independently: result must be 1925285 bytes, sha256 `e067e3402028c2dd43e3b8af0ed4d95429d5f9fbc5b65541ac5c8179ee64bea2`. If your own measurement does not match, STOP and declare the mismatch. `grep -c "^Gate: "` must read 219 (up from 218).

BEGIN SLICE PLAN_R3
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
| T001 schema + sectioners + storage/caching | done | round 2 |
| T002 summary role + generation call + fallback | done | round 3, `generate_artifact_summary` |
| T003 compiler integration + fixture | pending | next round |

## Next Steps
1. Round 4: T003 — hook the new representation into
   `packages/orchestration/context_compiler.py`'s selection/rendering (a
   third `rendering` value beside `"full"`/`"signatures"`), the
   relevant-L2-section matching rule, the long-log fixture, and the size
   comparison recorded.
2. Integration gate (full suite, both required runs) before closure.
3. Closure sequence: README sync, STATUS `[x]`, evidence bundle, review
   package.

## Risks
- T003 is the round that proves the whole feature's DONE condition (order-
  of-magnitude prompt-footprint reduction on a fixture); T001/T002 are
  necessary but not sufficient on their own.
END SLICE PLAN_R3
(sha256 of the slice content above, exactly as it must land in `.agent/plan.md`: cb6779108e48e11dbffdc61a973c6424f484fa34c3e5f652326355219fade528 — 1655 bytes, 37 lines)

PRODUCTION CODE SPEC, part A — `packages/orchestration/role_config.py` (S15). Read the file whole first. Above `KNOWN_ROLES`, following the existing `orchestrator`/`teacher` comment paragraphs' shape exactly (each names ONE role and the ONE fact that justifies its CLI-flag/budget posture), add ONE new paragraph for `summary`: state that it is F108 T002's one-shot schema-validated generation call over `run_structured_call` (packages/orchestration/structured_outputs.py), and state — after actually checking, by grepping for any CLI flag or per-role budget wiring in this repository that assumes a FIXED, closed role list (e.g. `--builder-model`-style flags enumerated per role) — whether `summary` needs its own CLI override flags / per-role budget limit or not, and why. Do not invent CLI flags this round; if none exist for a comparable role like `test_worker`, say so and give `summary` the same "no dedicated flags" posture. Then add `"summary",` as a new final entry inside the `KNOWN_ROLES` tuple. Confirmed by the reviewer before this round: no test in this repository references `KNOWN_ROLES` at all (`grep -rn "KNOWN_ROLES" tests/` is empty), so there is no closed-set guard this addition could break.

PRODUCTION CODE SPEC, part B — `packages/orchestration/artifact_summary.py` (S9-S14), ADDED to the file T001 already built (do not modify or remove any T001 code). Add these imports at the top, alongside the existing ones: `from collections.abc import Callable`; `from packages.orchestration.failure_postmortem import FailureSignals, classify, utc_now_iso`; `from packages.orchestration.structured_outputs import run_structured_call`. Implement:

S9. `class GeneratedSummaryContent(BaseModel)` — fields `l1: str`, `l2: list[ArtifactSummarySection]`. This is the NARROW schema the provider is actually asked to fill — never `full_ref`/`artifact_hash`/`generator`/`generated_at`, which this module derives itself and never trusts a provider response for (a provider hallucinating a path or a hash must never corrupt the cache key or the reference path).

S10. Module constants: `FALLBACK_MARKER = "[summary unavailable — truncated view]"`; `_FALLBACK_HEAD_CHARS = 2000`; `_FALLBACK_TAIL_CHARS = 2000` (the small honest heuristic the feature file's edge-cases section asks for — document these two numbers with a one-line comment naming what they bound).

S11. `def _build_summary_prompt(sections: list[dict[str, str]]) -> str` — mechanically builds a prompt from T001's section list: for each entry, a header naming its `section` and `span_ref` followed by its `text`, joined with blank lines, plus one instruction line asking for an L1 summary of about 200 tokens and one L2 entry per given section, each L2 entry's `section`/`span_ref` echoing the INPUT section's own values exactly (so the provider cannot invent section names the caller did not give it — state this constraint in the prompt text itself). Never raises for any input, including `sections == []`.

S12. `def _fallback_summary(sections: list[dict[str, str]], full_ref: str, artifact_hash: str, reason: str) -> ArtifactSummary` — NEVER raises, for any input. Join `sections`' `"text"` values with `"\n\n"` into `combined`. If `len(combined) <= _FALLBACK_HEAD_CHARS + _FALLBACK_TAIL_CHARS`, the fallback L2 summary text is `combined` verbatim (nothing to truncate — do not fabricate a head/tail split when there is nothing to cut). Otherwise it is `combined`'s first `_FALLBACK_HEAD_CHARS` characters, then a line reading exactly `...`, then `combined`'s last `_FALLBACK_TAIL_CHARS` characters. Return `ArtifactSummary(l1=FALLBACK_MARKER, l2=[ArtifactSummarySection(section="fallback", span_ref="fallback", summary=<that text>)], full_ref=full_ref, generator=f"fallback:{reason}", generated_at=utc_now_iso(), artifact_hash=artifact_hash)`.

S13. `def generate_artifact_summary(sections: list[dict[str, str]], full_ref: str, artifact_hash: str, call_fn: Callable[[str, int], str] | None = None, *, on_call: Callable[[int, str, bool, str], None] | None = None, generator_label: str = "summary-role") -> ArtifactSummary` — NEVER raises; the fallback IS the error path, not an exception. Mirrors the three-way shape of `compile_dod` in `packages/orchestration/dod_compiler.py` (`call_fn is None` / try-except-Exception around the structured call / `not outcome.ok`) — read that function first as your model. Behavior: (a) `call_fn is None` → `return _fallback_summary(sections, full_ref, artifact_hash, reason="no provider")`; (b) otherwise build the prompt via `_build_summary_prompt`, call `run_structured_call(GeneratedSummaryContent, prompt, call_fn, on_call=on_call, allow_parse_retry=True)` inside `try`/`except Exception as exc`, and on that exception `classify(FailureSignals(exception=exc))` then `return _fallback_summary(..., reason=classification.failure_class.value)`; (c) if the call returns but `not outcome.ok`, `classify(FailureSignals(error_class=outcome.error_class, error_text=outcome.hint))` then the same fallback shape; (d) on success, return `ArtifactSummary(l1=outcome.value.l1, l2=outcome.value.l2, full_ref=full_ref, generator=generator_label, generated_at=utc_now_iso(), artifact_hash=artifact_hash)` — `full_ref`/`artifact_hash`/`generator`/`generated_at` ALWAYS come from this function's own parameters/clock, never from `outcome.value`.

TEST SPEC — EXTEND `tests/orchestration/test_artifact_summaries.py` (append new test functions; keep every existing T001 test function unchanged). Add a fake `call_fn` helper (a plain function or closure returning a fixed string, or raising, per test) — no real provider, no network. Cover, at minimum:
1. `test_generate_artifact_summary_no_call_fn_returns_fallback` — `call_fn=None`; assert `l1 == FALLBACK_MARKER`, `generator == "fallback:no provider"`, `full_ref`/`artifact_hash` equal the caller-supplied values.
2. `test_generate_artifact_summary_success_with_fake_provider` — a fake `call_fn` that returns a valid JSON string matching `GeneratedSummaryContent` (an `l1` string and a non-empty `l2` list echoing an input section's `section`/`span_ref`); assert the returned `ArtifactSummary.l1`/`l2` come from the fake response and `full_ref`/`artifact_hash`/`generated_at` are set by the function, not left blank or provider-supplied.
3. `test_generate_artifact_summary_invalid_response_falls_back` — a fake `call_fn` that returns non-JSON garbage on every call (so both the initial attempt and the one allowed parse retry fail); assert the result is a fallback (`l1 == FALLBACK_MARKER`) and `generator` starts with `"fallback:"`.
4. `test_generate_artifact_summary_provider_exception_falls_back` — a fake `call_fn` that raises `RuntimeError("boom")`; assert the result is a fallback (`l1 == FALLBACK_MARKER`), and that NO exception propagates out of `generate_artifact_summary` itself.
5. `test_fallback_summary_truncates_with_marker_when_over_budget` — call `_fallback_summary` (or `generate_artifact_summary` with `call_fn=None`) with sections whose combined text exceeds `_FALLBACK_HEAD_CHARS + _FALLBACK_TAIL_CHARS`; assert the L2 summary text contains a line reading exactly `...` and both the first `_FALLBACK_HEAD_CHARS` and last `_FALLBACK_TAIL_CHARS` characters of the combined text are present in it.
6. `test_fallback_summary_no_truncation_when_under_budget` — sections whose combined text is short; assert the L2 summary text equals the combined text verbatim, with NO `...` marker line inserted.

Done when (run every command for real and record the real exit code; never report "green" as a word):
G1 TRANSPORT — sha256 `.agent/authored/f108-r3.md` and `.agent/last_block.md`, confirm equal; confirm the SLICE GATE_R2 and SLICE PLAN_R3 regions inside the committed authored file match the digests stated beside each above.
G2 LEDGER APPEND — `.agent/live_review.md` sha256 equals `e067e3402028c2dd43e3b8af0ed4d95429d5f9fbc5b65541ac5c8179ee64bea2` at 1925285 bytes; `grep -c "^Gate: "` reads 219; `grep -c "F108 R2"` reads exactly 1.
G3 ROLE_CONFIG — `grep -c "\"summary\"," packages/orchestration/role_config.py` reads exactly 1, inside the `KNOWN_ROLES` tuple; `python3 -m pytest tests/orchestration/test_role_config.py -q` real exit 0 (reviewer's own base reading: 33 passed — report your own real number; it should be unchanged since this is additive).
G4 NEW TESTS — `python3 -m pytest tests/orchestration/test_artifact_summaries.py -q` real exit 0; report the real pass count (must be at least 16: the 10 from T001 plus the 6 above, or more if you added extra cases).
G5 MUTATION RED-PROOF (isolated per self_drive_protocol.md guardrail G5 — a DISPOSABLE worktree, never the primary checkout, added AFTER C3/C4 are committed): `git worktree add .remedy-wt/f108-r3-mutant HEAD`; inside that worktree, edit ONLY `packages/orchestration/artifact_summary.py`'s `generate_artifact_summary` to remove its `try`/`except Exception` handling around the `run_structured_call` invocation (let the call run unguarded, so an exception from `call_fn` propagates instead of being caught) — describe in the handback exactly which lines you changed and how; run `python3 -m pytest tests/orchestration/test_artifact_summaries.py::test_generate_artifact_summary_provider_exception_falls_back -q` there with `cwd` set via `subprocess.run(..., cwd=<worktree>)` (never shell `cd`) — record the real exit code (expect non-zero: an uncaught exception surfaces as an ERROR, not a clean assertion failure — report which it is). Then `git worktree remove .remedy-wt/f108-r3-mutant --force`, re-run the SAME test in the PRIMARY checkout to confirm green (exit 0), report both readings side by side, and run `git status --porcelain` in the primary checkout immediately after to confirm empty.
G6 STATE READERS — `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q`, real exit 0 (reviewer's own base reading: 604 passed).
G7 CANARY — `pytest tests/cli/test_golden_path.py -q`, real exit 0 (reviewer's own base reading: 42 passed).
G8 TREE + PLAN + SIZE — `.agent/plan.md` sha256 equals `cb6779108e48e11dbffdc61a973c6424f484fa34c3e5f652326355219fade528` (37 lines, under the 50-line cap); `git status --porcelain` empty; HEAD pushed and equal to `origin/feature/f108-tiered-artifact-summaries`; every commit's insertions under 500 lines; this round's own commit range touches exactly the 8 change-set paths named above, nothing else (measure the round's OWN range, i.e. from the base HEAD you recorded at pre-flight, not `main..HEAD`, since round 1 and round 2 are still un-PR'd on this branch — same reasoning round 2's own handback already used).

Handback: write the completion report inline in your final message AND rewrite `.agent/handoff.md` per docs/agents/handback_template.md (Session, Range, Commits per-commit table, External actions, Verification with real transcripts including BOTH mutation readings, Authored-text proofs, Deviations & assumptions, Next). The Session line reads `SESSION 1 of feature F108 · round 3 · rounds so far 3`. Do not create a pull request this round — T003 is still open, so the branch is not yet reviewable as a whole; state that under Next ("Round 4: T003 — compiler integration, fixture, size comparison").
