── STEP T003c/T003 — F108 Tiered artifact summaries ────────────────────────
Goal: give `render_tiered_diff_text` real disk persistence and T001's
hash-invalidated caching (an optional `artifact_path` parameter, additive
and backward-compatible), and wire a REAL resolvable path at both existing
call sites (builder repair-diff, reviewer scoped-diff) under the run's own
trace directory, per DECISION F108 D5 (below) — this discharges the
feature's "the reference path present" Done-condition wording for both
call sites landed so far.

Bundle:
  C0a. Save this entire step block verbatim to `.agent/authored/f108-r9.md`
       (copy the bytes between the two `=== BEGIN/END STEP BLOCK ===` marker
       lines, excluding the marker lines themselves).
  C0b. Mirror `.agent/authored/f108-r9.md` byte-for-byte to `.agent/last_block.md`.
  C1.  Append SLICE_LEDGER_R9 (two paragraphs: `Gate: F108 R8`, then
       `DECISION F108 D5`) to `.agent/live_review.md`, exactly as given below.
  C2.  Implement SPEC S1-S6 in `packages/orchestration/artifact_summary.py`
       and `packages/orchestration/pingpong_loop.py` (below).
  C3.  Add the new tests named in SPEC S7 to
       `tests/orchestration/test_artifact_summaries.py`.
  C4.  Add the new tests named in SPEC S8 to
       `tests/orchestration/test_builder_prompt_golden.py` and
       `tests/orchestration/test_reviewer_prompt_golden.py`.
  C5.  Rewrite `.agent/plan.md` to SLICE_PLAN_R9 (exact bytes given below).
  C6.  Rewrite `.agent/handoff.md` per AGENTS.md's `### handoff.md` section
       (this round's own completion report; no length cap, amend0827 rule 3).

Change (bounds this round's FILE WRITES only — push and worktree cleanup
are separate obligations, stated in Handback below):
  .agent/authored/f108-r9.md (new), .agent/last_block.md, .agent/live_review.md,
  packages/orchestration/artifact_summary.py, packages/orchestration/pingpong_loop.py,
  tests/orchestration/test_artifact_summaries.py,
  tests/orchestration/test_builder_prompt_golden.py,
  tests/orchestration/test_reviewer_prompt_golden.py, .agent/plan.md,
  .agent/handoff.md. Nothing else. Keep each commit under 500 inserted
  lines (AGENTS.md); the `.agent/**` single-file-rewrite exemption applies
  per commit that is a verbatim rewrite of ONE state file.

Constraints:
  - `artifact_path` is OPTIONAL and defaults to `None`; every EXISTING call
    of `render_tiered_diff_text` that does not pass it (all of round 7's
    landed tests) must keep behaving EXACTLY as before — no file written,
    no cache consulted.
  - Do NOT touch `task_runs/`, `job_evidence.py`, `artifact_contract_gate.py`,
    or `change_provenance_gate.py` — out of scope this round by DECISION
    F108 D5 (the run's own trace directory is a separate tree those files
    never scan).
  - Do NOT touch the reviewer's fallback branch, `compose_reviewer_prompt`'s
    non-scoped diff chain, or anything named out of scope by DECISION F108
    D3/D4 — unchanged, still deferred.
  - Follow AGENTS.md File Editing Safety Rules: read each file's relevant
    region in full before editing, re-read after, verify syntax and logical
    consistency. Re-read `packages/orchestration/pingpong_loop.py`'s exact
    current bytes at every anchor below before editing — do not trust any
    line number here without re-grepping it yourself first.

=== SPEC (production code — described, not sliced; you write the code,
following AGENTS.md conventions, to this exact shape) ===

S1. In `packages/orchestration/artifact_summary.py`, `render_tiered_diff_text`
gains one new keyword parameter, `artifact_path: Path | None = None`,
inserted immediately after the existing `full_ref: str,` line and before
the `) -> str:` line that closes the signature. (`Path` is already
imported at this file's top.)

S2. Extend `render_tiered_diff_text`'s own docstring with a new paragraph
(after the existing one) stating: `artifact_path`, when given, is where
`diff_text` is persisted (parent directories created as needed) and where
T001's hash-invalidated cache (`load_cached_summary`/`save_summary`) is
checked before, and written after, the provider call — a cache hit skips
`generate_artifact_summary` entirely; `None` (the default) keeps this
function's ORIGINAL stateless contract exactly — no file written, no cache
consulted, every call generates fresh, which is what every round-7-landed
test still exercises; the caller decides `full_ref`'s text independently,
and passing `str(artifact_path)` for both keeps them in agreement, which
this function never invents on its own.

S3. Change the function's body: after computing `artifact_hash`, replace
the single unconditional `summary = generate_artifact_summary(...)` line
with cache-aware logic — when `artifact_path` is given, write `diff_text`
there (creating parent directories first) and check
`load_cached_summary(artifact_path)`; only call `generate_artifact_summary`
when that check misses (or `artifact_path` is `None`), and after a fresh
generation, `save_summary(artifact_path, summary)` whenever `artifact_path`
is given. The rest of the function (section selection, rendering) is
UNCHANGED. Re-read the function's current exact bytes (grep for
`def render_tiered_diff_text`) before editing — do not trust any line
number stated anywhere in this block.

S4. `_builder_tiered_diff_text` (in `pingpong_loop.py`) gains the SAME new
optional parameter, `artifact_path: Path | None = None`, inserted after its
existing `full_ref: str,` line, purely forwarded into its own
`render_tiered_diff_text(...)` call as `artifact_path=artifact_path,`. Add
one sentence to its docstring naming the forwarding.

S5. `_reviewer_tiered_diff_text` gets the identical treatment: same new
parameter, same forwarding, same one-sentence docstring addition.

S6. In `run_pingpong`, at EACH of the two existing call sites (re-grep
`builder_tiered_diff_text = _builder_tiered_diff_text(` and
`reviewer_tiered_diff_text = _reviewer_tiered_diff_text(` to find their
current exact bytes before editing):
  - Builder site: immediately before the `_builder_tiered_diff_text(...)`
    call, compute
    `builder_tiered_artifact_path = _pingpong_runs_dir() / result.run_id / "calls" / "builder" / f"round-{round_num:02d}" / "tiered_diff.diff"`,
    then change the call's existing
    `full_ref=f"repair diff, round {round_num} (F108: not yet persisted to evidence)",`
    line to `full_ref=str(builder_tiered_artifact_path),` and add
    `artifact_path=builder_tiered_artifact_path,` as a new argument.
  - Reviewer site: the same shape, with
    `reviewer_tiered_artifact_path = _pingpong_runs_dir() / result.run_id / "calls" / "reviewer" / f"round-{round_num:02d}" / "tiered_diff.diff"`,
    replacing
    `full_ref=f"reviewer diff, round {round_num} (F108: not yet persisted to evidence)",`
    with `full_ref=str(reviewer_tiered_artifact_path),` and adding
    `artifact_path=reviewer_tiered_artifact_path,`.
  `_pingpong_runs_dir` is already defined and used elsewhere in this same
  file (grep for it) — do not add a new import or a new helper for it.

=== SPEC S7 (new tests in tests/orchestration/test_artifact_summaries.py) ===
Add, in a new section after the existing F108 T003b tests, importing
`ArtifactSummary` (already imported) and using the `tmp_path` pytest
fixture (already used elsewhere in this file for `load_cached_summary`
tests — match that style), exactly these 2 new tests:

1. `test_render_tiered_diff_text_with_artifact_path_persists_and_caches` --
   `artifact_path = tmp_path / "repair.diff"`, a fake `call_fn` returning a
   JSON body with `l1`/one `l2` entry for `foo.py` (mirroring this file's
   existing fake-provider pattern), call
   `render_tiered_diff_text(_TWO_FILE_DIFF, ["foo.py"], fake_call_fn,
   threshold_chars=50, full_ref=str(artifact_path), artifact_path=artifact_path)`.
   Assert the returned text contains the `l2` summary text; assert
   `artifact_path.read_text() == _TWO_FILE_DIFF` (the diff was persisted
   verbatim); assert `load_cached_summary(artifact_path)` now returns a
   non-`None` `ArtifactSummary` whose `l1` matches what the fake call_fn
   returned (the summary was cached).
2. `test_render_tiered_diff_text_with_artifact_path_cache_hit_skips_generation`
   -- pre-populate the cache: write `_TWO_FILE_DIFF` to
   `artifact_path = tmp_path / "repair.diff"`, compute its hash
   (`compute_artifact_hash`, already imported), build an `ArtifactSummary`
   with `l1="cached summary, never regenerated"`, `l2=[]`, matching
   `artifact_hash`, and `save_summary(artifact_path, that_summary)`. Then
   call `render_tiered_diff_text(_TWO_FILE_DIFF, ["foo.py"],
   call_fn_that_raises_if_called, threshold_chars=50,
   full_ref=str(artifact_path), artifact_path=artifact_path)` where
   `call_fn_that_raises_if_called` is a local function that raises
   `AssertionError("generation must not run on a cache hit")` if ever
   invoked. Assert the call does NOT raise and the result contains
   `"cached summary, never regenerated"`.

Verify after writing: `python3 -m pytest tests/orchestration/test_artifact_summaries.py -q`
must show exactly 27 passed (25 base + 2 new).

=== SPEC S8 (new tests: one per helper, in the existing Helper test classes) ===
In `tests/orchestration/test_builder_prompt_golden.py`, inside the existing
`TestBuilderTieredDiffTextHelper` class, add ONE new test method,
`test_forwards_artifact_path_to_render_tiered_diff_text`, using the
`tmp_path` pytest fixture: `artifact_path = tmp_path / "builder_repair.diff"`,
a `repair_diff` over `_OVERSIZED_DIFF_THRESHOLD_CHARS` (already imported in
this file), `_FINDINGS` (already defined), `is_resumed=False`, a
`call_fn_factory` that returns `None` (e.g. `lambda: None`). Call
`_builder_tiered_diff_text(repair_diff, _FINDINGS, False, lambda: None,
threshold_chars=_OVERSIZED_DIFF_THRESHOLD_CHARS, full_ref=str(artifact_path),
artifact_path=artifact_path)`. Assert `artifact_path.exists()`, assert
`artifact_path.read_text() == repair_diff`, assert the result is not `""`.

In `tests/orchestration/test_reviewer_prompt_golden.py`, inside the
existing `TestReviewerTieredDiffTextHelper` class, add the mirror test,
`test_forwards_artifact_path_to_render_tiered_diff_text`, using
`_OVERSIZED_REVIEWER_SCOPED_DIFF_THRESHOLD_CHARS` (already imported) and
`_SCOPE_PACKET` (already defined) in place of `_FINDINGS`, calling
`_reviewer_tiered_diff_text(safe_diff, _SCOPE_PACKET, False, lambda: None,
threshold_chars=_OVERSIZED_REVIEWER_SCOPED_DIFF_THRESHOLD_CHARS,
full_ref=str(artifact_path), artifact_path=artifact_path)`, with the same
three assertions.

Verify after writing:
`python3 -m pytest tests/orchestration/test_reviewer_prompt_golden.py tests/orchestration/test_builder_prompt_golden.py tests/orchestration/test_artifact_summaries.py -q`
must show exactly 102 passed (39 + 36 + 27).

=== SLICE_LEDGER_R9 (C1 — append to .agent/live_review.md) ===
Append EXACTLY the following two paragraphs to the END of
`.agent/live_review.md`, separated from the file's current content by
`"\n\n"` and from each other by `"\n\n"`, with NO trailing newline after the
final paragraph (mirror the file's existing convention exactly -- read the
file's current last 300 bytes yourself with a short Python script before
editing, to confirm your starting point, then apply):

Gate: F108 R8 — T003b-ii REVIEWER SCOPED-DIFF TIERING BUILT, WIRED, AND MUTATION-PROVEN; DECISION F108 D4'S SCOPE HELD EXACTLY. VERDICT PASS. The reviewer independently re-verified round 8's committed diff `ce59e42f`..`0bd996ac` against the real files, not the worker's own report. G1 TRANSPORT: `.agent/authored/f108-r8.md` and `.agent/last_block.md` independently sha256'd, both `2e9bf52b102a690ae3b008550b110bf9c05f7386a440abef244e323b47d2233a` at 33139 bytes, IDENTICAL. G2 LEDGER+SLIP APPEND: `.agent/live_review.md` independently re-measured at 1971244 bytes, sha256 `c287789acb0e17ce112349ee347dfbad8bb3cac4dd1500f3dba235d428182757`, matching the round's own stated result exactly; `grep -c "^Gate: "` at 224, `grep -cE "^DECISION F[0-9]+ D[0-9]+ — "` at 25, `grep -cE "^- R-[0-9]{4} — "` unchanged at 326; `.agent/prose_slips.md` independently re-measured at 39682 bytes, sha256 `0e9b00f83b3074218d9d11cdabb36b92f6edf0274fc3a9e3e7f35c90861d4a82`, matching exactly. G3 THE WIRING: `packages/orchestration/pingpong_loop.py`'s new `_OVERSIZED_REVIEWER_SCOPED_DIFF_THRESHOLD_CHARS` (`= _REVIEWER_SCOPED_DIFF_CAP`), `_reviewer_tiered_diff_text` (correctly short-circuits on `is_resumed`/no `scope_packet`/under threshold BEFORE invoking `call_fn_factory`, correctly derives `file_refs` from `scope_packet["changed_files"]` -- the FULL changed-file list, never a narrower subset, matching DECISION F108 D4's own safety reasoning), `compose_reviewer_prompt`'s new `elif tiered_diff_text:` branch (correctly sits INSIDE the `if scoped:` block, between `resume_hunks_text` and the flat-cap `elif safe_diff:`, same segment name/rank; the OUTER fallback chain independently confirmed byte-for-byte untouched), `_build_reviewer_prompt`'s forwarding, and `run_pingpong`'s call site all independently read in full and confirmed to match DECISION F108 D4's CHOSEN shape exactly. G4 THE TESTS: `python3 -m pytest tests/orchestration/test_reviewer_prompt_golden.py tests/orchestration/test_builder_prompt_golden.py tests/orchestration/test_artifact_summaries.py -q` independently re-run, real exit 0, 98 passed (38+35+25); `python3 -m pytest tests/orchestration/test_pingpong_cli.py -q` independently re-run, real exit 0, 172 passed, unchanged. G5 MUTATION RED-PROOFS -- INDEPENDENTLY REPRODUCED: in a fresh disposable worktree, replacing `_reviewer_tiered_diff_text`'s `if len(safe_diff) <= threshold_chars:` with `if False:` made `test_returns_empty_when_under_threshold` FAIL with a real `AssertionError` (`call_fn_factory` was invoked when it should not have been); replacing `compose_reviewer_prompt`'s `elif tiered_diff_text:` with `elif False and tiered_diff_text:` made `test_tiered_diff_text_replaces_the_scoped_flat_capped_diff` FAIL with a real `AssertionError`; both re-confirmed green afterward. ONE REVIEWER-SIDE TOOLING INCIDENT DURING THIS VERIFICATION, CORRECTLY CAUGHT AND REPAIRED, NOT A DEFECT IN THE ROUND'S OWN PRODUCT: the reviewer's own mutation red-proof used `cd <worktree> && python3 -m pytest ...` for the second mutation's test run, the documented anti-pattern of `self_drive_scratch_location.md` ("cd into a worktree SILENTLY does not take effect"); the `cd` silently no-opped and BOTH mutations landed in the PRIMARY checkout instead of the disposable worktree, discovered only at cleanup via `git diff -- packages/orchestration/pingpong_loop.py`, and reverted immediately with `git checkout --` before this verdict was written -- `git status --porcelain` confirmed empty and HEAD unchanged before and after the repair. The RED readings themselves were still real AssertionErrors against real mutated code, so the PROOF stands; only the ISOLATION guarantee (G5) was transiently breached by the reviewer's own tooling, not by anything the round committed. Memory updated (`self_drive_scratch_location.md`) with a mechanical counter-measure (`git status --porcelain` on the primary checked in the SAME tool-call sequence as any mutation, never deferred to cleanup) so this class does not recur a third time. G6 STATE READERS + CANARY: 604 passed and 42 passed respectively, matching base exactly. G7 TREE: `git status --porcelain` empty; HEAD confirmed pushed and equal to `origin/feature/f108-tiered-artifact-summaries` at `0bd996ac`; `git diff --stat ce59e42f..HEAD` independently confirmed to touch exactly the 8 declared paths, nothing else, every commit's insertions independently re-measured under 500 (largest 392, C0a). No deviation found in the round's own committed work.

DECISION F108 D5 — T003c PERSISTS THE TIERED DIFF UNDER THE RUN'S OWN TRACE DIRECTORY (`_pingpong_runs_dir()/<run_id>/calls/<role>/round-NN/tiered_diff.diff`), REUSING THE EXISTING `call_evidence_dir` NAMING SHAPE FOR A NEW `kind`, NOT `task_runs/<task_id>/` -- WHICH BELONGS TO A SEPARATE, LATER JOB-EVIDENCE-AGGREGATION LAYER THIS FEATURE DOES NOT TOUCH. THE PROBLEM: T003c needs a REAL, resolvable `full_ref` path (the feature's literal Done condition, "the reference path present") plus T001's hash-invalidated caching wired at both call sites; `run_pingpong` itself has no direct access to `task_runs/<task_id>/` -- that tree is assembled by `job_evidence.py` from named, explicitly-collected artifacts (`result.diff`, `safe.diff`, `stream_artifacts.json`, `provider_evidence.json`) AFTER a run completes, and is independently validated by `artifact_contract_gate.py` (`check_stream_artifacts`, the unreferenced-`result.diff` check) and `change_provenance_gate.py` (globs `task_runs/*/safe.diff` for provenance coverage) -- both read by full-file inspection this round, both scanning ONLY their own known filenames, neither scanning the tree generally for "unexpected" files. Writing a brand-new artifact type into `task_runs/` would need its OWN wiring into `job_evidence.py`'s collection step to ever surface in a packaged evidence bundle, and skipping that wiring while still writing into that tree risks a silently-orphaned artifact those two gates never account for -- a second, separate integration surface this DECISION explicitly defers. CHOSEN: `_pingpong_runs_dir()/<run_id>/` is the tree `run_pingpong` ALREADY owns directly (`result.diff`, `prompt_trace.jsonl`, `result.json` all live there today), and `calls/<role>/round-NN/<kind>` is ALREADY its own established per-round-per-role convention (`call_evidence_dir`, `failure_postmortem.py:755`, used today for provider-call post-mortems). `render_tiered_diff_text` gains one new optional parameter, `artifact_path: Path | None = None` -- `None` (the default, what T003b's own landed tests still pass) keeps the function's ORIGINAL stateless contract exactly; given a real path, it writes `diff_text` there (parent dirs created), checks T001's `load_cached_summary` before any provider call, and calls `save_summary` after a fresh generation, so a byte-identical diff recomputed later (a resumed job, a retried round) is a cache HIT, never a second provider call. `_builder_tiered_diff_text`/`_reviewer_tiered_diff_text` each gain the SAME optional `artifact_path` param, purely forwarded. Both `run_pingpong` call sites now compute a real path -- `_pingpong_runs_dir() / result.run_id / "calls" / "builder-or-reviewer" / f"round-{round_num:02d}" / "tiered_diff.diff"` -- and pass `full_ref=str(that_path)`, so the rendered "Full diff:" line names a path that genuinely exists on disk the moment the round runs, discharging the feature's own Done-condition wording for both call sites at once. ALTERNATIVES CONSIDERED: (a) wire the artifact into `task_runs/` and `job_evidence.py`'s collection step in the same round -- rejected, a second cross-cutting integration surface on top of an already substantial round, and the two contract gates read this round give no evidence it is SAFE without also reading `job_evidence.py`'s own collection logic in full, which this round did not do. (b) skip caching, persist the path only -- rejected: T001's cache machinery already exists, is already tested, and the marginal cost of wiring it here (a `load_cached_summary`/`save_summary` pair around the existing `generate_artifact_summary` call) is small next to the value of never re-spending a provider call on an unchanged diff. WHAT REMAINS: T003d, the long-artifact fixture and size-comparison recording -- the feature's own DONE-condition evidence, still open; T003b-iii (the reviewer's fallback branch) stays deferred per DECISION F108 D4, unchanged. HOW TO REVERSE: drop `artifact_path` back to unconditionally `None` at both call sites (or delete the parameter and its cache-check branch entirely); `render_tiered_diff_text`'s stateless behavior for every EXISTING caller is unaffected either way, since the parameter is additive and defaults to today's behavior. WHAT IT COSTS TO BE WRONG: if `task_runs/` later proves the correct home after all (e.g. a future feature wants the tiered diff inside the packaged evidence bundle), the cost is a second write plus the `job_evidence.py` wiring this round explicitly deferred -- the `_pingpong_runs_dir()` copy this round lands is not wasted, since `call_evidence_dir`'s own post-mortem consumers already read that same tree.

After applying, independently verify with a short Python script (read the
file, decode utf-8, check length/hash): the file's new length is 1980392
bytes and its sha256 is `b67820ab9d35b2cc594949d03b58ea0934d8ae285dffc04d63e4211d0524c343`.
Also verify `grep -c "^Gate: "` reads 225, `grep -cE "^DECISION F[0-9]+ D[0-9]+ — "`
reads 26, and `grep -cE "^- R-[0-9]{4} — "` is UNCHANGED at 326 (this round
mints no new R-id). If any of these four numbers do not match, STOP, do not
commit, and report the mismatch in your handback instead of forcing a match.

=== SLICE_PLAN_R9 (C5 — rewrite .agent/plan.md to exactly this text) ===
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
| T001-T002 schema, sectioners, generation, `summary` role | done | rounds 2-5 |
| T003 re-scoped to `pingpong_loop.py` | done | round 6, R-0765/D2 |
| T003a generation-call bridge + relevant-section matching | done | round 6 |
| T003b-i/ii builder+reviewer scoped-diff wiring + tests | done | rounds 7-8, D3/D4 |
| T003c real persisted `full_ref` + disk caching, both call sites | done | round 9, DECISION F108 D5 |
| T003b-iii reviewer fallback-branch wiring | pending | deferred, D4 |
| T003d long-artifact fixture + size comparison (DONE evidence) | pending | next round |

## Next Steps
1. Round 10: T003d — a fixture diff/log large enough to trigger tiering at
   BOTH call sites, an end-to-end assertion that the composed prompt's
   character count is an order of magnitude smaller than the raw diff
   (mirroring `test_artifact_summaries.py`'s own fixture test from round
   7), and the size-comparison numbers recorded — the feature's own
   DONE-condition evidence.
2. Integration gate (full suite, both required runs) before closure.
3. Closure sequence: README sync, STATUS `[x]`, evidence bundle, review
   package.

## Risks
- T003d's fixture must exercise the REAL call sites (`run_pingpong`'s
  builder/reviewer phases), not just `render_tiered_diff_text` in
  isolation, or the DONE condition's "enters a follow-up prompt" clause is
  unmet by the test that claims to prove it.

Independently verify after applying: 42 lines, 2113 bytes, sha256
`430a6580045a39295fb99fa556e2e7fd933ed5d9667321e04bd4ea50c3e122ea`. If
these do not match your applied file, STOP, do not commit, and report the
mismatch.

Done when (verification commands — run every one yourself, record real exit
codes and full output in your handback, never assert "green" as a word):
  G1 TRANSPORT: `sha256sum .agent/authored/f108-r9.md .agent/last_block.md`
      -- both digests IDENTICAL.
  G2 LEDGER APPEND: the four `live_review.md` independent-verification
      numbers named above (byte count, sha256, Gate count, DECISION count)
      all match; R- count unchanged at 326.
  G3 NEW CACHING CODE + MUTATION RED-PROOF: `python3 -c "import packages.orchestration.artifact_summary"`
      exits 0; `python3 -m pytest tests/orchestration/test_artifact_summaries.py -q`
      shows exactly 27 passed. THEN, in a disposable `git worktree` only
      (never the primary checkout; remove the worktree after; run
      `git status --porcelain` on the PRIMARY the moment the mutation is
      typed, per the tooling note above): edit your new cache-check line
      inside `render_tiered_diff_text` so it ALWAYS regenerates (e.g.
      change `summary = load_cached_summary(artifact_path)` to
      `summary = None` unconditionally, or equivalent), run
      `tests/orchestration/test_artifact_summaries.py::test_render_tiered_diff_text_with_artifact_path_cache_hit_skips_generation`
      and confirm it FAILS with a real AssertionError (the "must not run on
      a cache hit" one); confirm it PASSES again unmutated in the primary
      checkout. Report both readings, and the `git status --porcelain`
      reading taken immediately after the mutation.
  G4 WIRING REGRESSION + MUTATION RED-PROOF:
      `python3 -m pytest tests/orchestration/test_reviewer_prompt_golden.py tests/orchestration/test_builder_prompt_golden.py tests/orchestration/test_artifact_summaries.py -q`
      shows exactly 102 passed (39 + 36 + 27). THEN, same disposable
      worktree discipline: edit `_builder_tiered_diff_text`'s call to
      `render_tiered_diff_text` so it no longer forwards `artifact_path`
      (drop that one argument), run
      `tests/orchestration/test_builder_prompt_golden.py::TestBuilderTieredDiffTextHelper::test_forwards_artifact_path_to_render_tiered_diff_text`
      and confirm it FAILS (the file is never written); confirm it PASSES
      again unmutated. Report both readings.
  G5 CALL-SITE REGRESSION: `python3 -m pytest tests/orchestration/test_pingpong_cli.py -q`
      shows exactly 172 passed (unchanged -- no existing fixture diff in
      that file is large enough to trigger the tiering branch, so no new
      file-write side effect is introduced there).
  G6 STATE READERS: `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q`
      shows 604 passed (unchanged from base).
  G7 CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` shows 42
      passed (unchanged from base).
  G8 TREE + PLAN + SIZE: `git status --porcelain` empty after the final
      commit (before push); `.agent/plan.md` is exactly 42 lines; every
      commit's insertions (the `+` column of `git diff --stat` per commit)
      are under 500; `git diff --stat 0bd996ac..HEAD` (excluding the final
      handoff commit; re-confirm `0bd996ac` is really round 8's own tip
      with `git log --oneline` before using it) touches exactly the 8
      declared change-set paths, nothing else.

Handback: after all commits land, `git push -u origin feature/f108-tiered-artifact-summaries`
and report the real exit code and the remote tip SHA (`git ls-remote origin
feature/f108-tiered-artifact-summaries`). Then write the completion report
+ rewrite `.agent/handoff.md` (C6) per AGENTS.md's `### handoff.md` section:
feature+round, SESSION NUMBER (session 2 of F108, same as rounds 7-8 --
this is round 9 of that same session), branch, commit SHAs, changed-files
table with real `+/-` per commit, verification results (every G1-G8
reading, real, not summarized as "green"), open findings count (0 -- this
round mints no new R-id), next expected action (round 10, T003d, per the
Next Steps above). If ANY gate above goes red, do NOT force a fix that
isn't in this block's scope -- stop, declare the exact failure, and leave
the tree at the last clean commit; do not push a red state silently.
── end step ──────────────────────────────────────────────────────────────