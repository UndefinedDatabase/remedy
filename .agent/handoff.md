# Handoff — F108 Tiered artifact summaries (round 3)

## Session

SESSION 1 of feature F108 · round 3 · rounds so far 3

## Range

Review of `3d92b5ccdcdc789e7a708403b19bbbca61a15717`..`HEAD`
(branch `feature/f108-tiered-artifact-summaries`). Pre-flight confirmed HEAD
at exactly the branch tip the block expected, `git status --porcelain`
empty. This round's own commits only.

**Round STOPPED PARTWAY through its bundle.** C2 (`packages/orchestration/role_config.py`,
declaring the `summary` role) was NOT applied: the block's S15 spec rested on
a factual claim — "no test in this repository references `KNOWN_ROLES` at
all (`grep -rn "KNOWN_ROLES" tests/` is empty)" — that is false, and the
addition it authorized would have broken a real, existing, closed-set test.
See Deviations for the full evidence. C3/C4 (the T002 generation function and
its tests) do not depend on C2 and were built and verified in full. C5/C6 were
adapted to state the true, partial status rather than land the block's
byte-exact (but now false) PLAN_R3 claim. Full detail below.

## Commits

### c801e95d docs(agent): save F108 R3 step block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f108-r3.md` | +100/-0 (new) | C0a — save the step block verbatim before touching any state file |

### 2ec2b13c docs(agent): mirror last_block to F108 R3
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +100/-111 (rewrite) | C0b — mirror to authored bytes; verbatim single-state-file rewrite (AGENTS.md 500-line exemption applies) |

### 1b963a26 docs(agent): book F108 R2's PASS verdict into the ledger
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +3/-1 (append) | C1 — append SLICE GATE_R2, the reviewer's own PASS verdict for round 2, per the append instructions |

### 147871ec feat(orchestration): generate_artifact_summary with never-blocking fallback
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/artifact_summary.py` | +132/-0 | C3 — S9-S14: `GeneratedSummaryContent`, `FALLBACK_MARKER`/`_FALLBACK_HEAD_CHARS`/`_FALLBACK_TAIL_CHARS`, `_build_summary_prompt`, `_fallback_summary`, `generate_artifact_summary` |

### 85c4aa8c fix(orchestration): give GeneratedSummaryContent a SCHEMA_V constant
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/artifact_summary.py` | +8/-0 | Not in the block's bundle — a same-round self-review fix, see Deviations. `run_structured_call` requires `schema_v_of(model_cls)` to resolve via a `SCHEMA_V` class constant; the block's S9 spec named only `l1`/`l2` and omitted it, so the first version silently fell back on every real call |

### a22c7d8a test(orchestration): cover generate_artifact_summary with fake providers
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_artifact_summaries.py` | +99/-1 | C4 — 6 new test functions per the test spec, T001's 10 existing tests unchanged |

### 6f5566dc docs(agent): plan.md reflects T002's real state, not the block's PLAN_R3
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +20/-14 (rewrite, NOT byte-exact to PLAN_R3) | C5, deviated — see Deviations |

### (this commit) rewrite handoff.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | C6 — handback per docs/agents/handback_template.md |

## External actions

- `git worktree add .remedy-wt/f108-r3-mutant HEAD` — created after C3/C4 landed, for the isolated mutation red-proof; outcome: `Preparing worktree (detached HEAD a22c7d8a)`.
- `git worktree remove .remedy-wt/f108-r3-mutant --force` — removed immediately after the mutant run; outcome: clean removal, confirmed by `git worktree list` no longer showing it (one pre-existing, unrelated worktree `job-f76686b8435640e9` remains — not created or touched by this round).
- `git push -u origin feature/f108-tiered-artifact-summaries` — pushes this round's commits through this handback commit; run after this file is committed (see below).
- No PR created — explicitly out of scope this round (T002's role registration is blocked, T003 still open).

## Verification

Pre-flight:
```
$ git status
On branch feature/f108-tiered-artifact-summaries
Your branch is up to date with 'origin/feature/f108-tiered-artifact-summaries'.
nothing to commit, working tree clean
$ git rev-parse HEAD
3d92b5ccdcdc789e7a708403b19bbbca61a15717
```
Matches the block's expected branch tip exactly. No deviation here.

G1 TRANSPORT:
```
GATE_R2 slice extracted from .agent/authored/f108-r3.md: 3240 bytes,
  sha256 d8f06fdbe3e7541a9438c1c62a91fb0e06cec5af5d91760a42dadc873c5ec0d6 — MATCH
PLAN_R3 slice extracted (+trailing \n, as it would land in .agent/plan.md):
  1655 bytes, sha256 cb6779108e48e11dbffdc61a973c6424f484fa34c3e5f652326355219fade528 — MATCH
  (this slice was NOT applied to .agent/plan.md — see Deviations — but the
  authored file's own transcription of it is verified byte-exact)
$ sha256sum .agent/authored/f108-r3.md .agent/last_block.md
613f09660aa43b992efafe1b336840e05f0bb6c6d95ca5cb9971b83c7753e673  .agent/authored/f108-r3.md
613f09660aa43b992efafe1b336840e05f0bb6c6d95ca5cb9971b83c7753e673  .agent/last_block.md
```
IDENTICAL.

G2 LEDGER APPEND:
```
$ wc -c .agent/live_review.md
1925285
$ sha256sum .agent/live_review.md
e067e3402028c2dd43e3b8af0ed4d95429d5f9fbc5b65541ac5c8179ee64bea2
$ grep -c "^Gate: " .agent/live_review.md
219
$ grep -c "F108 R2" .agent/live_review.md
1
```
All four match the block's stated values exactly.

G3 ROLE_CONFIG — NOT EXECUTED, blocked. `packages/orchestration/role_config.py`
was not touched this round. Evidence the block's premise is false:
```
$ grep -rn "KNOWN_ROLES" tests/
tests/orchestration/test_role_config.py:14:    KNOWN_ROLES,
tests/orchestration/test_role_config.py:115:    @pytest.mark.parametrize("role", KNOWN_ROLES)
tests/orchestration/test_role_config.py:124:        assert KNOWN_ROLES == (
```
This is the literal command the block cited as proof of an empty result; it
is not empty. Line 124 is a closed-set equality assertion
(`TestAllRoles.test_all_eight_roles_present`) that pins the exact 8-tuple.
Reproduced the break in a disposable worktree (`.remedy-wt/f108-r3-probe`,
removed after — not part of the declared bundle, a pre-commit investigation
only):
```
$ python3 -m pytest tests/orchestration/test_role_config.py -q
[inside the probe worktree, packages/orchestration/role_config.py patched
 to append "summary" as KNOWN_ROLES' 9th entry, mechanically, no other change]
FAILED tests/orchestration/test_role_config.py::TestAllRoles::test_all_eight_roles_present
AssertionError: assert ('builder', ... ) == ('builder', ...)
  Left contains one more item: 'summary'
1 failed, 33 passed
```
Unmodified (base) reading, primary checkout, for the record:
```
$ python3 -m pytest tests/orchestration/test_role_config.py -q
.................................                                        [100%]
33 passed in 0.27s
```
Matches the block's stated base reading (33 passed) exactly — confirms this
round changed nothing here; the 33-passed base itself was never in question,
only the block's claim that adding "summary" would leave it at 33.

G4 NEW TESTS:
```
$ python3 -m pytest tests/orchestration/test_artifact_summaries.py -q
................                                                         [100%]
16 passed in 0.24s
```
Real exit 0, 16 passed (10 from T001, unchanged, plus the 6 new T002 cases).

G5 MUTATION RED-PROOF (isolated, `.remedy-wt/f108-r3-mutant`, added AFTER
C3/C4 landed, never the primary checkout):
```
$ git worktree add .remedy-wt/f108-r3-mutant HEAD
Preparing worktree (detached HEAD a22c7d8a)
```
Edited ONLY the worktree copy of `packages/orchestration/artifact_summary.py`:
removed the `try:` / `except Exception as exc:` wrapper around the
`run_structured_call(...)` invocation inside `generate_artifact_summary`
(the four lines `try:`, the `run_structured_call(...)` call, `except
Exception as exc:`, and the two-line `classify(...)` + `_fallback_summary`
return became an unwrapped bare call — the call itself is unchanged, only
the exception containment around it was removed). Ran via
`subprocess.run([...], cwd=<worktree>)`, never shell `cd`:
```
MUTATED (worktree):
$ python3 -m pytest tests/orchestration/test_artifact_summaries.py::test_generate_artifact_summary_provider_exception_falls_back -q
F                                                                        [100%]
FAILED tests/orchestration/test_artifact_summaries.py::test_generate_artifact_summary_provider_exception_falls_back
RuntimeError: boom
1 failed in 0.31s
exit code: 1
```
The failure is an uncaught `RuntimeError("boom")` propagating out of
`fake_call_fn` through `generate_artifact_summary` into the test body itself
(visible in the traceback: `structured_outputs.py:158: in run_structured_call
    last_text = call_fn(prompt, attempt)` then the raise) — not a clean
`AssertionError` at the test's own `assert` line, confirming the mutation
really did remove exception containment rather than merely changing a
comparison.
```
$ git worktree remove .remedy-wt/f108-r3-mutant --force
(clean removal)
UNMUTATED (primary checkout):
$ python3 -m pytest tests/orchestration/test_artifact_summaries.py::test_generate_artifact_summary_provider_exception_falls_back -q
.                                                                        [100%]
1 passed in 0.23s
exit code: 0
```
```
$ git status --porcelain
(empty)
```
Both readings recorded side by side: mutated → FAILED/exit 1, an uncaught
`RuntimeError`; unmutated → 1 passed/exit 0. Primary checkout tree confirmed
empty immediately after.

G6 STATE READERS:
```
$ python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q
604 passed in 48.96s
exit 0
```
Matches the reviewer's own base reading (604) exactly.

G7 CANARY:
```
$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 20.51s
exit 0
```
Matches the reviewer's own base reading (42) exactly.

G8 TREE + PLAN + SIZE:
```
$ sha256sum .agent/plan.md
3164a6733aef0025fb233d2da4a0378ec9bc2ea8fc1ed28addc1e63563424817
$ wc -l .agent/plan.md
45
```
Does NOT equal the block's stated PLAN_R3 digest
(`cb6779108e48e11dbffdc61a973c6424f484fa34c3e5f652326355219fade528`) — by
design, see Deviations; 45 lines, under the 50-line cap.
```
$ git status --porcelain
(empty)
```
Every commit's insertions independently checked under 500 (largest is 132,
`artifact_summary.py`'s S9-S14 addition); see Commits table above.
`git diff --stat 3d92b5cc..HEAD` (this round's own commit range) touches
exactly 7 paths: `.agent/authored/f108-r3.md`, `.agent/last_block.md`,
`.agent/live_review.md`, `packages/orchestration/artifact_summary.py`,
`tests/orchestration/test_artifact_summaries.py`, `.agent/plan.md`,
`.agent/handoff.md` — i.e. 7 of the 8 declared change-set paths, deliberately
missing `packages/orchestration/role_config.py` (never touched this round —
see Deviations). Nothing outside the declared change set was touched.
HEAD pushed and equal to `origin/feature/f108-tiered-artifact-summaries`
(confirmed after the push below).

## Authored-text proofs

`.agent/authored/f108-r3.md` was typed verbatim from the step block between
the `BEGIN STEP BLOCK F108-R3` / `END STEP BLOCK F108-R3` markers (markers
excluded). Disk-to-disk comparison: `.agent/last_block.md` mirrored from it,
both sha256 to `613f09660aa43b992efafe1b336840e05f0bb6c6d95ca5cb9971b83c7753e673`
— IDENTICAL. The GATE_R2 slice (appended into `.agent/live_review.md`) was
independently re-hashed against the digest stated beside it before being
applied, matching exactly (see G1/G2 above) — that is the fidelity proof for
the one reviewer-authored text actually landed on disk this round. The
PLAN_R3 slice was independently re-hashed and confirmed byte-exact as
*transcribed* in the authored file (see G1 above) but was deliberately NOT
applied to `.agent/plan.md` — its content asserts a fact (T002 fully done,
including role registration) that this round's own investigation shows is
false, and AGENTS.md's "If Blocked" section (item 2: "Update `.agent/plan.md`
with the exact blocker") governs that case ahead of the block's byte-exact
instruction.

## Deviations & assumptions

- **BLOCKING CONTRADICTION — S15's premise about `KNOWN_ROLES` is false; C2
  was not applied.** The block states, as justification for adding
  `"summary"` to `KNOWN_ROLES`: "Confirmed by the reviewer before this round:
  no test in this repository references `KNOWN_ROLES` at all (`grep -rn
  "KNOWN_ROLES" tests/` is empty), so there is no closed-set guard this
  addition could break." Running that exact command shows three matches in
  `tests/orchestration/test_role_config.py`, including
  `TestAllRoles.test_all_eight_roles_present`, which asserts `KNOWN_ROLES ==
  (<the current 8-tuple>)` — an exact closed-set equality. Appending
  `"summary"` as a 9th entry (exactly what S15 orders) makes that assertion
  false; reproduced for real in a disposable pre-commit probe worktree
  (`.remedy-wt/f108-r3-probe`, not part of the declared bundle, removed
  before any bundle commit): `1 failed, 33 passed`, the failure being
  `AssertionError: ... Left contains one more item: 'summary'`. G3's
  done-when ("real exit 0 ... it should be unchanged since this is
  additive") is therefore unmeetable as the block states it. Per this
  round's own top-level instruction ("If ANY gate above does not match as
  stated ... a contradiction in this block ... STOP, do not force a fix
  that isn't yours to make, and write `.agent/handoff.md` declaring exactly
  what did not match instead of committing over it") and self-drive
  protocol G8 ("Any red gate, contradiction ... → write the handoff and end
  cleanly"): did NOT apply C2, did NOT edit
  `tests/orchestration/test_role_config.py` (outside the declared 8-path
  change set, and fixing it is not this round's call to make), and did NOT
  land the S15 documentation paragraph either (a paragraph justifying a role
  that is not yet registered would itself be a false/dangling claim on
  disk). C3/C4 (S9-S14, the generation function and its tests) do not
  reference `role_config.py` or `KNOWN_ROLES` at all — `generate_artifact_summary`
  takes `call_fn` as a direct parameter, never via `resolve_role_config` —
  so they were built and fully verified independently of this block. Two
  resolutions are open for the next round, stated in `.agent/plan.md`'s Next
  Steps: (a) register `"summary"` AND update the test's tuple literal in the
  same round, both paths declared, or (b) a DECISION that
  `generate_artifact_summary` never needs `KNOWN_ROLES` membership, since
  nothing built this round or found in the repository wires it through
  `resolve_role_config`.
- **`GeneratedSummaryContent` needed a `SCHEMA_V` constant the block's S9
  spec omitted.** `run_structured_call` calls `schema_v_of(model_cls)`
  (`packages/orchestration/schemas/models.py`), which raises `ValueError`
  when the class has no `SCHEMA_V` class constant. S9 named only `l1: str,
  l2: list[ArtifactSummarySection]` as the model's fields and did not
  mention `SCHEMA_V`. Without it, every real generation call raised
  internally, was caught by the (correctly implemented) `except Exception`
  wrapper, and silently fell back — the fallback path masked the bug rather
  than exposing it, until `test_generate_artifact_summary_success_with_fake_provider`
  failed with `result.l1 == FALLBACK_MARKER` instead of the fake provider's
  text. Fixed by adding `GENERATED_SUMMARY_SCHEMA_V = "generated_summary_v1"`
  and `SCHEMA_V: ClassVar[str] = GENERATED_SUMMARY_SCHEMA_V` on the model,
  matching the `DoDDraft`/`DoD` convention in `dod_schema.py` this round's
  own S13 spec pointed at as the model to mirror. Did NOT add a `schema_v`
  response field (unlike `DoDDraft`, which subclasses `_Structured` and
  requires one) because `GeneratedSummaryContent` is a plain `BaseModel` per
  S9, and the block's own TEST SPEC #2 describes the fake provider's JSON as
  carrying only `l1`/`l2` — adding a required `schema_v` field would break
  that test as specified. Committed as a small separate fix-up commit
  (`85c4aa8c`) rather than folded into `147871ec`, per this session's
  standing instruction to never amend a prior commit.
- **`.agent/plan.md` deviates from the block's byte-exact PLAN_R3.** PLAN_R3
  states "T002 summary role + generation call + fallback | done | round 3" —
  true of the generation call and fallback, false of the role registration
  (blocked, see above). Landing PLAN_R3 verbatim would put a false claim on
  disk. Wrote an honest replacement instead (45 lines, under the 50-line
  cap), keeping the same structure/headings, marking T002's generation half
  done and its role-registration half BLOCKED with a pointer to this file.
- No other deviations. Every other path in the change set was touched
  exactly as the block ordered, in the order specified.

## Next

Round 4 FIRST resolves the `summary`-role registration block per
`.agent/plan.md`'s Next Steps (either register `"summary"` in `KNOWN_ROLES`
AND update `test_role_config.py`'s tuple literal in the same round, both
declared, or a DECISION that `generate_artifact_summary` does not need
`KNOWN_ROLES` membership at all), THEN proceeds to T003 — compiler
integration, the long-log fixture, and the size comparison. No PR yet — T002
is only partially closed and T003 is untouched, so the branch is not yet
reviewable as a whole.
