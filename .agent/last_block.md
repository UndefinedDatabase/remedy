── STEP T003b-ii/T003 — F108 Tiered artifact summaries ────────────────────────
Goal: wire tiering into the reviewer prompt's SCOPED diff branch only
(`compose_reviewer_prompt`'s `reviewer_focused_diff` segment), mirroring
round 7's builder-side wiring but using the scope packet's own
`changed_files` as the relevant-section file list (never a narrower
subset — DECISION F108 D4, below), since the reviewer must see every
changed file, only compressed when oversized. The fallback branch
(`reviewer_staged_diff`, reached only when no scope packet exists) and
`diff_summary` stay untouched this round — deferred per DECISION F108 D4.

Bundle:
  C0a. Save this entire step block verbatim to `.agent/authored/f108-r8.md`
       (copy the bytes between the two `=== BEGIN/END STEP BLOCK ===` marker
       lines, excluding the marker lines themselves).
  C0b. Mirror `.agent/authored/f108-r8.md` byte-for-byte to `.agent/last_block.md`.
  C1.  Append SLICE_LEDGER_R8 (two paragraphs: `Gate: F108 R7`, then
       `DECISION F108 D4`) to `.agent/live_review.md`, exactly as given below.
  C1b. Append SLICE_SLIP_R8 (one line) to `.agent/prose_slips.md`, exactly
       as given below.
  C2.  Implement SPEC S1-S6 in `packages/orchestration/pingpong_loop.py`
       (below).
  C3.  Add the new tests named in SPEC S7 to
       `tests/orchestration/test_reviewer_prompt_golden.py`.
  C4.  Rewrite `.agent/plan.md` to SLICE_PLAN_R8 (exact bytes given below).
  C5.  Rewrite `.agent/handoff.md` per AGENTS.md's `### handoff.md` section
       (this round's own completion report; no length cap, amend0827 rule 3).

Change (bounds this round's FILE WRITES only — push and worktree cleanup
are separate obligations, stated in Handback below):
  .agent/authored/f108-r8.md (new), .agent/last_block.md, .agent/live_review.md,
  .agent/prose_slips.md, packages/orchestration/pingpong_loop.py,
  tests/orchestration/test_reviewer_prompt_golden.py, .agent/plan.md,
  .agent/handoff.md. Nothing else. Keep each commit under 500 inserted
  lines (AGENTS.md); the `.agent/**` single-file-rewrite exemption applies
  per commit that is a verbatim rewrite of ONE state file.

Constraints:
  - Do NOT touch the fallback branch of `compose_reviewer_prompt`
    (`elif resume_hunks_text: ... elif safe_diff: ... elif diff_summary:`
    OUTSIDE the `if scoped:` block), `_REVIEWER_DIFF_CAP`, or
    `compose_builder_prompt`/`_builder_tiered_diff_text` — out of scope
    this round by DECISION F108 D4.
  - Do NOT wire disk caching or a real persisted `full_ref` path — same
    deferral as round 7 (DECISION F108 D3), unchanged this round.
  - `_reviewer_tiered_diff_text`'s `call_fn_factory` parameter must be
    invoked ONLY inside the branch that actually needs its result — never
    eagerly, mirroring `_builder_tiered_diff_text`'s own rule.
  - The existing golden fixtures/frozen renders in
    `test_reviewer_prompt_golden.py` (`_FROZEN_RENDERS`, `_SHAPES`) are
    NEVER edited — your new tests are additive only, in new test classes.
  - Follow AGENTS.md File Editing Safety Rules: read each file's relevant
    region in full before editing, re-read after, verify syntax and logical
    consistency. Re-read `packages/orchestration/pingpong_loop.py`'s exact
    current bytes at every anchor below before editing — round 7 already
    changed line numbers in this file; do not trust any number here without
    re-grepping it yourself first.

=== SPEC (production code — described, not sliced; you write the code,
following AGENTS.md conventions, to this exact shape) ===

S1. In `packages/orchestration/pingpong_loop.py`, immediately after the
existing line `_REVIEWER_SCOPED_DIFF_CAP = 12000` (grep for it first to
confirm it is still there, unedited, before applying), insert:
```python

#: F108 DECISION D4 — deliberately equal to `_REVIEWER_SCOPED_DIFF_CAP`:
#: tiering activates exactly where the scoped flat truncation used to,
#: mirroring DECISION D3's own pattern on the builder side.
_OVERSIZED_REVIEWER_SCOPED_DIFF_THRESHOLD_CHARS = _REVIEWER_SCOPED_DIFF_CAP
```

S2. `compose_reviewer_prompt`'s signature gains one new keyword parameter,
`tiered_diff_text: str = ""`, inserted immediately after the existing
`resume_hunks_text: str = "",` line and before the `) -> ComposedPrompt:`
line that closes the signature.

S3. In the SAME function's body, inside the EXISTING `if scoped:` block,
insert a new `elif tiered_diff_text:` branch between the existing
`if resume_hunks_text:` sub-block and the existing `elif safe_diff:`
sub-block (the one that uses `_REVIEWER_SCOPED_DIFF_CAP` — NOT the
`diff_summary` branch, and NOT the fallback branch outside `if scoped:`,
which uses `_REVIEWER_DIFF_CAP` instead and must stay untouched). Same
segment name `reviewer_focused_diff`, same rank
`SegmentStabilityRank.STEERING` the flat-cap branch already uses:
```python
        elif tiered_diff_text:
            # F108 DECISION D4: a pre-rendered L1+relevant-L2 replacement
            # for an oversized scoped diff, for the SAME segment name/rank
            # the flat-cap branch below uses -- the caller (run_pingpong's
            # `_reviewer_tiered_diff_text`) supplies this pre-rendered,
            # exactly like `resume_hunks_text` above; this function performs
            # no summarization of its own. An empty string always falls
            # through to the flat-cap branch below. Only the SCOPED branch
            # gets tiering this round (DECISION F108 D4) -- the fallback
            # branch below never sees `tiered_diff_text`.
            specs.append((
                "reviewer_focused_diff", SegmentStabilityRank.STEERING,
                [tiered_diff_text],
            ))
```
Precedence after this change, inside `if scoped:`, top to bottom:
`resume_hunks_text` > `tiered_diff_text` > `safe_diff` (flat cap) >
`diff_summary`. Verify by reading the applied function that this is the
actual resulting order, and that the OUTER fallback chain (`elif
resume_hunks_text: ... elif safe_diff: ... elif diff_summary:`, reached
only when `scoped` is false) is completely unedited.

S4. Add a new module-level function, placed directly after
`compose_reviewer_prompt`'s closing
`return compose_prompt_segments(registry.registered_segments())` line and
before `def _build_reviewer_prompt(` (re-grep both anchors first to
confirm their current exact text and that nothing sits between them today):
```python
def _reviewer_tiered_diff_text(
    safe_diff: str,
    scope_packet: dict[str, Any] | None,
    is_resumed: bool,
    call_fn_factory: Callable[[], Callable[[str, int], str] | None],
    *,
    threshold_chars: int,
    full_ref: str,
) -> str:
    """Compute the reviewer's tiered-summary replacement for an oversized
    scoped diff, or "" when tiering does not apply -- the caller's existing
    flat-cap fallback (`compose_reviewer_prompt`'s scoped `elif safe_diff:`
    branch) then applies unchanged (F108 DECISION D4).

    Only the SCOPED branch is covered this round: `scope_packet` is `None`
    on the fallback branch, and this function returns "" whenever it is,
    leaving the fallback's own diff branches entirely untouched (DECISION
    F108 D4's own scope). `file_refs` is `scope_packet["changed_files"]` --
    every file the diff touches, never a narrower subset, since the
    reviewer's job on this branch is to see the WHOLE diff, only compressed
    when it is oversized (unlike the builder's findings-narrowed repair
    diff). `is_resumed` mirrors the caller's own precedence, matching
    `_builder_tiered_diff_text`'s own reasoning: a resumed session's shrunk
    hunk render already takes priority (DECISION F106 D1(b), Reviewer
    side), so `call_fn_factory` (`summary_call_fn` itself, unapplied) is
    invoked only inside the branch that needs its result.
    """
    if is_resumed or not safe_diff or not scope_packet:
        return ""
    if len(safe_diff) <= threshold_chars:
        return ""
    file_refs = scope_packet.get("changed_files") or []
    return render_tiered_diff_text(
        safe_diff, file_refs, call_fn_factory(),
        threshold_chars=threshold_chars, full_ref=full_ref,
    )
```
(`render_tiered_diff_text` and `summary_call_fn` are already imported at
this file's top from round 7 — do not add a duplicate import.)

S5. `_build_reviewer_prompt` (the thin wrapper below `compose_reviewer_prompt`)
gets the SAME new parameter (`tiered_diff_text: str = ""`, inserted after
`resume_hunks_text: str = "",` in its signature) and forwards it unchanged
(`tiered_diff_text=tiered_diff_text,` inserted after
`resume_hunks_text=resume_hunks_text,` in its call to
`compose_reviewer_prompt`). Its docstring's sentence naming
`resume_hunks_text` as forwarded unchanged is extended to also name
`tiered_diff_text`.

S6. In `run_pingpong` (the function containing the ONLY production call
site of `compose_reviewer_prompt`), find the existing block that computes
`reviewer_resume_hunks_text` and immediately calls `compose_reviewer_prompt`
(re-read this region in full before editing, per AGENTS.md File Editing
Safety Rules, to confirm it has not shifted from what you find via grep).
Immediately after the existing `reviewer_resume_hunks_text = ...`
computation block ends (right before the existing
`reviewer_composed = compose_reviewer_prompt(` call begins), insert:
```python
            reviewer_tiered_diff_text = _reviewer_tiered_diff_text(
                reviewer_safe_diff, runtime_scope_packet,
                bool(reviewer_resume_ref and reviewer_safe_diff), summary_call_fn,
                threshold_chars=_OVERSIZED_REVIEWER_SCOPED_DIFF_THRESHOLD_CHARS,
                full_ref=f"reviewer diff, round {round_num} (F108: not yet persisted to evidence)",
            )
```
and add `tiered_diff_text=reviewer_tiered_diff_text,` as a new line inside
the existing `compose_reviewer_prompt(...)` call's argument list,
immediately after its existing `resume_hunks_text=reviewer_resume_hunks_text,`
line.

=== SPEC S7 (new tests in tests/orchestration/test_reviewer_prompt_golden.py) ===
Add, near the existing `TestResumeHunksTextReplacesTheDiffOnEitherBranch`
class, extending the file's import block with `_OVERSIZED_REVIEWER_SCOPED_DIFF_THRESHOLD_CHARS`
and `_reviewer_tiered_diff_text` from `packages.orchestration.pingpong_loop`,
plus `FALLBACK_MARKER` from `packages.orchestration.artifact_summary`, TWO
new test classes with exactly these test methods (use `_TEST_RESULT`,
already defined in this file, so the diff segment is never the LAST
segment -- matching this file's own existing care about the
trailing-newline-drop mechanism, e.g. `scoped_full`'s own shape):

`TestTieredDiffTextReplacesTheScopedFlatCap`:
1. `test_tiered_diff_text_replaces_the_scoped_flat_capped_diff` -- call
   `compose_reviewer_prompt(_GOAL, _BUILDER_SUMMARY, scope_packet=_SCOPE_PACKET,
   safe_diff=_SAFE_DIFF, test_result=_TEST_RESULT, tiered_diff_text=<a
   literal multi-line string of your choosing ending in "\n">)`; assert
   `_segment_texts(composed)["reviewer_focused_diff"]` equals that string
   with `.rstrip("\n")` applied.
2. `test_resume_hunks_text_still_takes_precedence_over_tiered_diff_text_on_scoped`
   -- same call PLUS `resume_hunks_text=_RESUME_HUNKS_TEXT`; assert
   `texts["reviewer_focused_diff"] == _RESUME_HUNKS_TEXT.rstrip("\n")`.
3. `test_an_empty_tiered_diff_text_falls_back_to_the_scoped_flat_capped_diff`
   -- `tiered_diff_text=""`; assert `texts["reviewer_focused_diff"] ==
   "## Focused Staged Diff\n\`\`\`diff\n" + _SAFE_DIFF + "\n\`\`\`"` (matching
   this file's existing `test_scoped_fulls_diff_segment_is_unchanged_by_resumed_existing`
   assertion exactly).
4. `test_tiered_diff_text_is_inert_on_the_fallback_branch` -- call
   `compose_reviewer_prompt(_GOAL, _BUILDER_SUMMARY, safe_diff=_SAFE_DIFF,
   test_result=_TEST_RESULT, tiered_diff_text=<the same literal string as
   test 1>)` -- NO `scope_packet`, so this is the fallback branch; assert
   `texts["reviewer_staged_diff"] == "## Staged Unified Diff\n\`\`\`diff\n" +
   _SAFE_DIFF + "\n\`\`\`"` (the unchanged flat-cap fallback render) AND
   assert `"reviewer_focused_diff" not in texts` (proving `tiered_diff_text`
   was never consulted on this branch, per DECISION F108 D4's scope).

`TestReviewerTieredDiffTextHelper` (direct unit tests of the new pure
helper, imported from `packages.orchestration.pingpong_loop`):
5. `test_returns_empty_when_resumed` -- `is_resumed=True`, everything else
   populated (`_SAFE_DIFF`, `_SCOPE_PACKET`, a `call_fn_factory` that would
   raise if called), `threshold_chars=10`; assert result is `""`.
6. `test_returns_empty_when_no_scope_packet` -- `scope_packet=None`, long
   `safe_diff` (e.g. `"x" * 100`), `is_resumed=False`, `call_fn_factory`
   that would raise if called; assert result is `""`.
7. `test_returns_empty_when_under_threshold` -- `_SAFE_DIFF`,
   `_SCOPE_PACKET`, `is_resumed=False`, `threshold_chars` larger than
   `len(_SAFE_DIFF)`, `call_fn_factory` that would raise if called; assert
   result is `""`.
8. `test_over_threshold_calls_render_tiered_diff_text_and_call_fn_factory_only_then`
   -- a `safe_diff` over `_OVERSIZED_REVIEWER_SCOPED_DIFF_THRESHOLD_CHARS`
   (e.g. `"x" * (_OVERSIZED_REVIEWER_SCOPED_DIFF_THRESHOLD_CHARS + 100)`),
   `_SCOPE_PACKET`, `is_resumed=False`, a `call_fn_factory` that increments
   a counter when called and returns `None`; assert the counter is exactly
   1 after the call (proving lazy, exactly-once invocation) and assert the
   result is a non-empty string containing `FALLBACK_MARKER`.

For test 1's and test 4's literal string, and for `_SCOPE_PACKET`'s
`changed_files` value (already `["packages/widget.py"]` in this file),
your literal `file_refs`-independent test string does not need to match
any specific section name -- these four tests exercise `compose_reviewer_prompt`'s
WIRING of a pre-rendered string, not `render_tiered_diff_text`'s own
section-selection logic (already tested in round 7's
`test_artifact_summaries.py`).

Verify after writing: `python3 -m pytest tests/orchestration/test_reviewer_prompt_golden.py -q`
must show exactly 38 passed (30 base + 8 new).

=== SLICE_LEDGER_R8 (C1 — append to .agent/live_review.md) ===
Append EXACTLY the following two paragraphs to the END of
`.agent/live_review.md`, separated from the file's current content by
`"\n\n"` and from each other by `"\n\n"`, with NO trailing newline after the
final paragraph (mirror the file's existing convention exactly -- read the
file's current last 300 bytes yourself with a short Python script before
editing, to confirm your starting point, then apply):

Gate: F108 R7 — T003b-i BUILDER REPAIR-DIFF TIERING BUILT, WIRED, AND MUTATION-PROVEN; DECISION F108 D3'S SCOPE HELD EXACTLY. VERDICT PASS. The reviewer independently re-verified round 7's committed diff `e7ef578f`..`ce59e42f` against the real files, not the worker's own report. G1 TRANSPORT: `.agent/authored/f108-r7.md` and `.agent/last_block.md` independently sha256'd, both `bd03602bd11faa1729314f9f5e0d7c3e962a4fa7155a4254b3130e5baee4a378` at 33431 bytes, IDENTICAL. G2 LEDGER APPEND: `.agent/live_review.md` independently re-measured at 1961415 bytes, sha256 `8d90730092b1d13729d623eb9f0529fe76882a1bc02fa79acaa8a927ffa89e1a`, matching the round's own stated result exactly; `grep -c "^Gate: "` independently re-measured at 223, `grep -cE "^DECISION F[0-9]+ D[0-9]+ — "` at 24, `grep -cE "^- R-[0-9]{4} — "` unchanged at 326. G3 THE MODULE: `packages/orchestration/artifact_summary.py`'s new `render_tiered_diff_text` independently read in full — matches DECISION F108 D3's CHOSEN description exactly: "" at/under `threshold_chars`, otherwise sections/generates/selects/renders via the existing T001/T002/T003a primitives, never raises. G4 THE WIRING: `packages/orchestration/pingpong_loop.py`'s new `_OVERSIZED_DIFF_THRESHOLD_CHARS` (`= _REPAIR_DIFF_CAP`), `_builder_tiered_diff_text` (correctly short-circuits on `is_resumed`/no findings/under threshold BEFORE invoking `call_fn_factory`), `compose_builder_prompt`'s new `elif tiered_diff_text:` branch (correctly sits between `resume_hunks_text` and the flat-cap `elif safe_diff and findings:`, same segment name/rank), `_build_builder_prompt`'s forwarding, and `run_pingpong`'s call site (correct precedence argument `bool(builder_resume_ref and repair_diff)`, correct `findings if is_repair else None` mirroring the neighboring `compose_builder_prompt` call) all independently read in full and confirmed to match DECISION F108 D3's CHOSEN shape exactly — no scope creep into `compose_reviewer_prompt` or disk caching, confirmed absent by `git diff e7ef578f..HEAD -- packages/orchestration/pingpong_loop.py` showing only the declared hunks. G5 THE TESTS: `python3 -m pytest tests/orchestration/test_artifact_summaries.py -q` independently re-run, real exit 0, 25 passed (21 base + 4 new); `python3 -m pytest tests/orchestration/test_builder_prompt_golden.py -q` independently re-run, real exit 0, 35 passed (28 base + 7 new); `python3 -m pytest tests/orchestration/test_pingpong_cli.py -q` independently re-run, real exit 0, 172 passed, unchanged. G6 MUTATION RED-PROOFS — INDEPENDENTLY REPRODUCED, not merely re-read: in a fresh disposable worktree (`.remedy-wt/f108r7-review-mutant`, removed after), replacing `render_tiered_diff_text`'s `if len(diff_text) <= threshold_chars:` with `if False:` made `test_render_tiered_diff_text_under_threshold_returns_empty_string` FAIL with a real `AssertionError` (the un-truncated fallback text where `""` was expected); replacing `compose_builder_prompt`'s `elif tiered_diff_text:` with `elif False and tiered_diff_text:` made `test_tiered_diff_text_replaces_the_flat_capped_diff` FAIL with a real `AssertionError` (the flat-capped diff where the tiered text was expected); both tests independently re-confirmed green in the primary checkout afterward, tree confirmed clean throughout (`git status --porcelain` empty, worktree removed). G7 STATE READERS + CANARY: `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q` independently re-run, real exit 0, 604 passed; `python3 -m pytest tests/cli/test_golden_path.py -q` independently re-run, real exit 0, 42 passed; both matching base exactly. G8 TREE: `git status --porcelain` empty; HEAD confirmed pushed and equal to `origin/feature/f108-tiered-artifact-summaries` at `ce59e42f`; `git diff --stat e7ef578f..HEAD` independently confirmed to touch exactly the 8 declared paths, nothing else, every commit's insertions independently re-measured under 500 (largest 446, C0a). ONE DEVIATION, CORRECTLY HANDLED, NOT A DEFECT: the round's own block (this reviewer's own prose) carried a stale base SHA (`76982f2f`, round 5's tip, copy-pasted from round 6's own G8 text) in its G8 clause instead of round 7's true base (`e7ef578f`); the worker ran the literal command AND the semantically-correct one, declared the discrepancy, and independently confirmed the change set is exactly the 8 declared paths against the correct base — the reviewer's own citation went stale, nothing on disk did (checklist item 9's class; booked as a `.agent/prose_slips.md` line per AGENTS.md rule 2, no R-id, no correction round). No other deviation found.

DECISION F108 D4 — REVIEWER-SIDE TIERING WIRES ONLY THE SCOPED BRANCH (`reviewer_focused_diff`), USING THE SCOPE PACKET'S OWN `changed_files` AS file_refs; THE FALLBACK BRANCH AND `diff_summary` STAY UNTOUCHED. THE PROBLEM: unlike the builder's repair-diff branch, `compose_reviewer_prompt` has no `findings`-shaped narrowing signal available at every call site -- `scope_packet` is built by `_build_runtime_scope_packet` and is `None` only when `safe_diff`/`staged_files` was empty or diff-parsing raised (a rare fallback), so the fallback branch (`elif safe_diff:` at `_REVIEWER_DIFF_CAP`) has no reliable file list to narrow against, and the reviewer's job on that path is to see the WHOLE diff regardless -- tiering it against an empty or absent file set would silently drop L2 detail the reviewer still needs, which `select_relevant_sections`' own design (T003a, round 6: "never a silent fallback to everything, which would defeat the size reduction the whole feature exists for") makes a real risk if misapplied here rather than a safe default. CHOSEN: the scope packet's `changed_files` field (independently confirmed at `_build_runtime_scope_packet`, `pingpong_loop.py:1277`: every file the just-computed safe diff touches, sorted, the SAME file set `section_diff` would section the diff into) is exactly the right `file_refs` for the scoped branch -- using it selects EVERY section the diff actually contains, dropping none, so tiering only ever compresses an oversized section's TEXT, never the reviewer's FILE coverage. This differs from the builder's repair-diff case (DECISION F108 D3), where `file_refs` = only the files named by open findings -- a genuine, intentional narrowing appropriate there because the builder is told to fix ONLY those findings; the reviewer has no such narrower mandate, so its `file_refs` set is deliberately the full changed-file list, never a subset. A new gating helper, `_reviewer_tiered_diff_text(safe_diff, scope_packet, is_resumed, call_fn_factory, *, threshold_chars, full_ref)`, mirrors `_builder_tiered_diff_text`'s short-circuit shape (resumed session / no `scope_packet` / under threshold all return "" before any provider resolve) and derives `file_refs` from `scope_packet["changed_files"]`. `compose_reviewer_prompt` gains one new parameter, `tiered_diff_text: str = ""`, checked in a new `elif tiered_diff_text:` branch inside the EXISTING `if scoped:` block, between `if resume_hunks_text:` and `elif safe_diff:` -- same segment name/rank (`reviewer_focused_diff`, STEERING) the flat-cap branch already uses, mirroring `resume_hunks_text`'s own precedent there (round 12, DECISION F106 D1(b)) exactly as DECISION F108 D3 mirrored it on the builder side; the fallback branch's `elif safe_diff:`/`elif diff_summary:` chain is NOT touched, so `tiered_diff_text` is inert whenever `scoped` is false. New threshold constant `_OVERSIZED_REVIEWER_SCOPED_DIFF_THRESHOLD_CHARS = _REVIEWER_SCOPED_DIFF_CAP` (12000), mirroring D3's own "deliberately equal to the cap it replaces" pattern. `full_ref` stays the same descriptive-label shape D3 chose (`f"reviewer diff, round {round_num} (F108: not yet persisted to evidence)"`) -- real persistence is still T003c, unchanged from D3. ALTERNATIVES CONSIDERED: (a) tier the fallback branch too, using `prior_findings` as `file_refs` on repair rounds and skipping tiering on a true first-pass review -- rejected this round: the fallback branch is reached only when `_build_runtime_scope_packet` itself failed, an already-degraded path, and adding a second helper with different narrowing semantics (findings-scoped, like the builder) beside a first-scoped one (file-list-scoped) in the same round risked exactly the kind of design confusion this DECISION exists to avoid; deferred, tracked in `.agent/plan.md`. (b) tier using `prior_findings` instead of `changed_files` on the scoped branch too, for symmetry with the builder -- rejected: `scoped` is true for nearly every non-empty diff in production (`scope_packet` is built whenever `safe_diff and staged_files`, independent of `prior_findings`/repair status), so narrowing to `prior_findings` would silently drop L2 coverage for files with no open finding on the FIRST review pass of every job, which is precisely the safety regression D4's THE PROBLEM section above warns against. WHAT REMAINS: the fallback branch, real evidence persistence (`full_ref`, T003c), disk caching (T003c), and the long-artifact fixture/size comparison (T003d) -- unchanged from DECISION F108 D3's own list, plus the fallback-branch deferral this DECISION adds. HOW TO REVERSE: delete `_reviewer_tiered_diff_text`, the `tiered_diff_text` parameter and its call site, and their tests; `compose_reviewer_prompt`'s remaining branches are byte-for-byte what they were before. WHAT IT COSTS TO BE WRONG: if `changed_files` later proves too wide (e.g. a future caller wants genuine narrowing on the scoped branch), the cost is one parameter change to the helper -- the segment-level wiring inside `compose_reviewer_prompt` does not change, since it only ever sees the caller's already-rendered text.

After applying, independently verify with a short Python script (read the
file, decode utf-8, check length/hash): the file's new length is 1971244
bytes and its sha256 is `c287789acb0e17ce112349ee347dfbad8bb3cac4dd1500f3dba235d428182757`.
Also verify `grep -c "^Gate: "` reads 224, `grep -cE "^DECISION F[0-9]+ D[0-9]+ — "`
reads 25, and `grep -cE "^- R-[0-9]{4} — "` is UNCHANGED at 326 (this round
mints no new R-id). If any of these four numbers do not match, STOP, do not
commit, and report the mismatch in your handback instead of forcing a match.

=== SLICE_SLIP_R8 (C1b — append to .agent/prose_slips.md) ===
Append EXACTLY the following ONE line to the END of `.agent/prose_slips.md`,
separated from the file's current content by `"\n\n"`, no trailing newline
after it (read the file's current tail yourself first to confirm your
starting point):

2026-09-02 · F108 R7 · The reviewer's own step block's G8 clause quoted a stale base SHA (`76982f2f`, round 5's tip, carried over from round 6's own G8 text) instead of round 7's actual base (`e7ef578f`); the worker ran both the literal and the semantically-correct command and declared the discrepancy, confirming the change set was exactly the 8 declared paths. Reviewer-prose citation drift, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

After applying, independently verify: the file's new length is 39682 bytes
and its sha256 is `0e9b00f83b3074218d9d11cdabb36b92f6edf0274fc3a9e3e7f35c90861d4a82`.
If this does not match, STOP, do not commit, and report the mismatch.

=== SLICE_PLAN_R8 (C4 — rewrite .agent/plan.md to exactly this text) ===
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
| T002 generation call + fallback | done | round 3 |
| T002 `summary` role registration | done | round 5, DECISION F108 D1 |
| T003 re-scoped: real hook is `pingpong_loop.py` | done | round 6, R-0765/D2 |
| T003a generation-call bridge + relevant-section matching | done | round 6 |
| T003b-i builder repair-diff wiring + tests | done | round 7, DECISION F108 D3 |
| T003b-ii reviewer scoped-diff wiring + tests | done | round 8, DECISION F108 D4 |
| T003b-iii reviewer fallback-branch wiring | pending | deferred, DECISION F108 D4 |
| T003c real persisted `full_ref` + disk caching | pending | after T003b-iii |
| T003d long-artifact fixture + size comparison (DONE evidence) | pending | after T003c |

## Next Steps
1. Round 9: decide whether T003b-iii (findings-scoped fallback-branch
   tiering) is worth building given how rarely that branch is reached in
   production, or proceed to T003c with it deferred — a DECISION either
   way, per DECISION F108 D4's own note.
2. T003c: persist the diff to evidence, pass a real `full_ref` path, wire
   T001's `load_cached_summary`/`save_summary` at both call sites.
3. T003d: the long-artifact fixture and size-comparison recording — the
   feature's own DONE-condition evidence.
4. Integration gate (full suite, both required runs) before closure.
5. Closure sequence: README sync, STATUS `[x]`, evidence bundle, review
   package.

## Risks
- T003c persists real diffs to evidence for the first time under F108 —
  the round names the exact evidence path convention (mirroring an
  existing evidence writer rather than inventing one) before writing to
  disk, and confirms cache invalidation (T001's hash check) actually
  fires across two different rounds of the SAME job.

Independently verify after applying: 49 lines, 2569 bytes, sha256
`8af01559213d544d0de503c51963fbe3d256e8bc484e2096d0951af8e1b2d39a`. If
these do not match your applied file, STOP, do not commit, and report the
mismatch.

Done when (verification commands — run every one yourself, record real exit
codes and full output in your handback, never assert "green" as a word):
  G1 TRANSPORT: `sha256sum .agent/authored/f108-r8.md .agent/last_block.md`
      -- both digests IDENTICAL.
  G2 LEDGER + SLIP APPEND: the four `live_review.md` independent-verification
      numbers named above (byte count, sha256, Gate count, DECISION count)
      all match; R- count unchanged at 326; the `prose_slips.md` byte
      count/sha256 named above both match.
  G3 NEW CODE + MUTATION RED-PROOF #1: `python3 -c "import packages.orchestration.pingpong_loop"`
      exits 0. THEN, in a disposable `git worktree` only (never the primary
      checkout; remove the worktree after): edit your new
      `_reviewer_tiered_diff_text`'s `if len(safe_diff) <= threshold_chars:`
      line so the condition is always `False` (e.g. replace with
      `if False:`), run
      `tests/orchestration/test_reviewer_prompt_golden.py::TestReviewerTieredDiffTextHelper::test_returns_empty_when_under_threshold`
      and confirm it FAILS with a real AssertionError; then confirm it
      PASSES again unmutated in the primary checkout. Report both readings.
  G4 REGRESSION + MUTATION RED-PROOF #2:
      `python3 -m pytest tests/orchestration/test_reviewer_prompt_golden.py tests/orchestration/test_builder_prompt_golden.py tests/orchestration/test_artifact_summaries.py -q`
      shows exactly 98 passed (38 + 35 + 25). THEN, same disposable worktree
      discipline: edit your new `elif tiered_diff_text:` branch's condition
      inside `compose_reviewer_prompt` to always be `False` (e.g.
      `elif False and tiered_diff_text:`), run
      `tests/orchestration/test_reviewer_prompt_golden.py::TestTieredDiffTextReplacesTheScopedFlatCap::test_tiered_diff_text_replaces_the_scoped_flat_capped_diff`
      and confirm it FAILS; confirm it PASSES again unmutated. Report both
      readings.
  G5 CALL-SITE REGRESSION: `python3 -m pytest tests/orchestration/test_pingpong_cli.py -q`
      shows exactly 172 passed (unchanged -- this file is not edited this
      round; this gate proves the wiring introduced no import-time or
      collection-time breakage).
  G6 STATE READERS: `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q`
      shows 604 passed (unchanged from base).
  G7 CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` shows 42
      passed (unchanged from base).
  G8 TREE + PLAN + SIZE: `git status --porcelain` empty after the final
      commit (before push); `.agent/plan.md` is exactly 49 lines; every
      commit's insertions (the `+` column of `git diff --stat` per commit)
      are under 500; `git diff --stat ce59e42f..HEAD` (excluding the final
      handoff commit; `ce59e42f` is round 7's own tip -- re-confirm this
      SHA yourself with `git log --oneline` before using it, per the prose
      slip you just booked in C1b) touches exactly the 8 declared
      change-set paths, nothing else.

Handback: after all commits land, `git push -u origin feature/f108-tiered-artifact-summaries`
and report the real exit code and the remote tip SHA (`git ls-remote origin
feature/f108-tiered-artifact-summaries`). Then write the completion report
+ rewrite `.agent/handoff.md` (C5) per AGENTS.md's `### handoff.md` section:
feature+round, SESSION NUMBER (session 2 of F108, same as round 7 -- this
is round 8 of that same session), branch, commit SHAs, changed-files table
with real `+/-` per commit, verification results (every G1-G8 reading,
real, not summarized as "green"), open findings count (0 -- this round
mints no new R-id), next expected action (round 9, per the Next Steps
above). If ANY gate above goes red, do NOT force a fix that isn't in this
block's scope -- stop, declare the exact failure, and leave the tree at the
last clean commit; do not push a red state silently.
── end step ──────────────────────────────────────────────────────────────