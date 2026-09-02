── STEP T003b-i/T003 — F108 Tiered artifact summaries ────────────────────────
Goal: wire T003a's `summary_call_fn`/`select_relevant_sections` into the
builder repair-diff branch of `pingpong_loop.py`, replacing `_REPAIR_DIFF_CAP`'s
flat truncation for oversized diffs with a tiered L1+relevant-L2 summary,
per DECISION F108 D2 and this round's own DECISION F108 D3 (below). The
flat cap stays as the backstop for diffs at/under the new threshold.
Reviewer-side wiring (`compose_reviewer_prompt`), real evidence persistence
of `full_ref`, and the long-artifact fixture are explicitly OUT of scope
this round — deferred to rounds 8+ per DECISION F108 D3.

Bundle:
  C0a. Save this entire step block verbatim to `.agent/authored/f108-r7.md`
       (copy the bytes between the two `=== BEGIN/END STEP BLOCK ===` marker
       lines, excluding the marker lines themselves).
  C0b. Mirror `.agent/authored/f108-r7.md` byte-for-byte to `.agent/last_block.md`.
  C1.  Append SLICE_LEDGER_R7 (two paragraphs: `Gate: F108 R6`, then
       `DECISION F108 D3`) to `.agent/live_review.md`, exactly as given below.
  C2.  Implement SPEC S1-S8 in `packages/orchestration/artifact_summary.py`
       and `packages/orchestration/pingpong_loop.py` (below).
  C3.  Add the new tests named in SPEC S9 to
       `tests/orchestration/test_artifact_summaries.py`.
  C4.  Add the new tests named in SPEC S10 to
       `tests/orchestration/test_builder_prompt_golden.py`.
  C5.  Rewrite `.agent/plan.md` to SLICE_PLAN_R7 (exact bytes given below).
  C6.  Rewrite `.agent/handoff.md` per AGENTS.md's `### handoff.md` section
       (this round's own completion report; no length cap, amend0827 rule 3).

Change (bounds this round's FILE WRITES only — push and worktree cleanup
are separate obligations, stated in Handback below):
  .agent/authored/f108-r7.md (new), .agent/last_block.md, .agent/live_review.md,
  packages/orchestration/artifact_summary.py, packages/orchestration/pingpong_loop.py,
  tests/orchestration/test_artifact_summaries.py,
  tests/orchestration/test_builder_prompt_golden.py, .agent/plan.md, .agent/handoff.md.
  Nothing else. Commit C0a/C0b together or separately at your discretion, but
  keep each commit under 500 inserted lines (AGENTS.md; the two `.agent/**`
  single-file-rewrite exemptions apply to C1/C5/C6 only if each stays a
  verbatim rewrite of ONE state file per commit).

Constraints:
  - Do NOT touch `compose_reviewer_prompt`, `_REVIEWER_DIFF_CAP`,
    `_REVIEWER_SCOPED_DIFF_CAP`, or any reviewer-prompt code — out of scope
    this round by DECISION F108 D3.
  - Do NOT wire disk caching (`load_cached_summary`/`save_summary`) at the
    new call site — `full_ref` this round is a descriptive string, not a
    real path (DECISION F108 D3 point 5). Do not invent a real path.
  - Every new/changed function keeps the module's existing style: a WHY
    comment only where non-obvious, google/numpy-free plain docstrings
    matching neighbors, no bare `except:`.
  - `_builder_tiered_diff_text`'s `call_fn_factory` parameter must be called
    (invoked) ONLY inside the branch that actually needs its result — never
    eagerly — because `summary_call_fn()` does a live Ollama-availability
    resolve that must not be spent when the branch short-circuits to "".
  - The existing golden fixtures/frozen renders in
    `test_builder_prompt_golden.py` (`_FROZEN_RENDERS`, `_SHAPES`) are NEVER
    edited — your new tests are additive only, in new test functions/classes.
  - Follow AGENTS.md File Editing Safety Rules: read each file's relevant
    region in full before editing, re-read after, verify syntax and logical
    consistency.

=== SPEC (production code — described, not sliced; you write the code,
following AGENTS.md conventions, to this exact shape) ===

S1. In `packages/orchestration/artifact_summary.py`, change the module
docstring's FIRST LINE (currently
`"""Tiered artifact summary schema, sectioners, generation, and the T003a call bridge (F108 T001/T002/T003a).`)
to:
`"""Tiered artifact summary schema, sectioners, generation, the T003a call bridge, and T003b diff-tiering rendering (F108 T001/T002/T003a/T003b).`
— an exact FROM/TO REWRITE of that one line (verify it occurs exactly once;
it is the file's first line).

S2. At the END of `packages/orchestration/artifact_summary.py` (after the
existing `select_relevant_sections` function, which is currently the file's
last top-level definition — verify this is still true before appending),
append, separated by two blank lines and preceded by a section-header comment
matching the style of the existing "F108 T003a" header a few lines above it:

```python
def render_tiered_diff_text(
    diff_text: str,
    file_refs: Iterable[str],
    call_fn: Callable[[str, int], str] | None,
    *,
    threshold_chars: int,
    full_ref: str,
) -> str:
    """Render a tiered L1+relevant-L2 replacement for an oversized diff, or "".

    F108 T003b: the pre-rendered text a caller (``pingpong_loop.py``'s
    ``_builder_tiered_diff_text``) substitutes for its own flat-capped diff
    segment. Returns "" when ``diff_text`` is at or under ``threshold_chars``
    -- the caller's signal to keep its own flat-cap behavior unchanged.
    Above threshold: sections the diff (``section_diff``), generates via
    ``generate_artifact_summary`` (never raises -- the fallback IS the error
    path), selects only the sections matching ``file_refs``
    (``select_relevant_sections``), and renders the L1 summary plus each
    selected L2 section plus a ``full_ref`` line so the model knows more
    exists.
    """
    if len(diff_text) <= threshold_chars:
        return ""
    sections = section_diff(diff_text)
    artifact_hash = compute_artifact_hash(diff_text.encode("utf-8"))
    summary = generate_artifact_summary(sections, full_ref, artifact_hash, call_fn)
    relevant = select_relevant_sections(summary, file_refs)
    lines = [f"## Current Staged Diff (summarized)\n{summary.l1}\n"]
    for entry in relevant:
        lines.append(f"### {entry.section} ({entry.span_ref})\n{entry.summary}\n")
    lines.append(f"Full diff: {full_ref} ({len(diff_text)} characters)\n")
    return "\n".join(lines)
```
Use a section-header comment reading `# F108 T003b — rendering the tiered
diff-inclusion text` (matching the `# ---...---` style already used above
`summary_call_fn` in this file).

S3. In `packages/orchestration/pingpong_loop.py`, add one new import line,
alphabetically ordered, immediately before the existing
`from packages.orchestration.exec_guard import run_guarded_test_command`
line:
`from packages.orchestration.artifact_summary import render_tiered_diff_text, summary_call_fn`

S4. In `packages/orchestration/pingpong_loop.py`, immediately after the
existing line `_REPAIR_DIFF_CAP = 20000`, insert (as an EOF-of-that-line
append, i.e. the existing line is untouched, new lines follow it):
```python

#: F108 DECISION D3 — deliberately equal to `_REPAIR_DIFF_CAP`: tiering now
#: activates exactly where flat truncation used to, replacing it rather than
#: adding a second, disconnected size boundary.
_OVERSIZED_DIFF_THRESHOLD_CHARS = _REPAIR_DIFF_CAP
```

S5. In `packages/orchestration/pingpong_loop.py`, `compose_builder_prompt`'s
signature gains one new keyword parameter, `tiered_diff_text: str = ""`,
inserted immediately after the existing `resume_hunks_text: str = "",` line
and before the `) -> ComposedPrompt:` line that closes the signature.

S6. In the SAME function's body, insert a new `elif tiered_diff_text:`
branch between the existing `if resume_hunks_text:` block and the existing
`elif safe_diff and findings:` block (same segment name `builder_staged_diff`,
same rank `SegmentStabilityRank.JOB_CONTEXT` the flat-cap branch already
uses):
```python
    elif tiered_diff_text:
        # F108 DECISION D3: a pre-rendered L1+relevant-L2 replacement for an
        # oversized diff, for the SAME segment name/rank the flat-cap branch
        # below uses -- the caller (run_pingpong's `_builder_tiered_diff_text`)
        # supplies this pre-rendered, exactly like `resume_hunks_text` above;
        # this function performs no summarization of its own. An empty
        # string always falls through to the flat-cap branch below.
        specs.append((
            "builder_staged_diff", SegmentStabilityRank.JOB_CONTEXT,
            [tiered_diff_text],
        ))
```
Precedence after this change, top to bottom: `resume_hunks_text` >
`tiered_diff_text` > `safe_diff and findings` (flat cap). Verify by reading
the applied function that this is the actual resulting order.

S7. `_build_builder_prompt` (the thin wrapper a few lines below
`compose_builder_prompt`) gets the SAME new parameter
(`tiered_diff_text: str = ""`, inserted after `resume_hunks_text: str = "",`
in its signature) and forwards it unchanged
(`tiered_diff_text=tiered_diff_text,` inserted after
`resume_hunks_text=resume_hunks_text,` in its call to
`compose_builder_prompt`). Its docstring's sentence naming
`hunk_ledger`/`resume_hunks_text` as forwarded unchanged is extended to also
name `tiered_diff_text`.

S8. In `run_pingpong` (the function containing the ONLY production call
site of `compose_builder_prompt`), find the existing block that computes
`builder_resume_hunks_text` and immediately calls `compose_builder_prompt`
(it reads, verbatim, starting at `builder_resume_hunks_text = ""` and ending
at the `compose_builder_prompt(...)` call's closing `)` -- re-read this
region in full before editing, per AGENTS.md File Editing Safety Rules, to
confirm it has not shifted). Add:

  (a) A new module-level function (place it directly after
  `compose_builder_prompt`'s closing `return compose_prompt_segments(...)`
  line and before `def _build_builder_prompt(`, i.e. between those two
  existing definitions):
```python
def _builder_tiered_diff_text(
    repair_diff: str,
    findings: list[ReviewFinding] | None,
    is_resumed: bool,
    call_fn_factory: Callable[[], Callable[[str, int], str] | None],
    *,
    threshold_chars: int,
    full_ref: str,
) -> str:
    """Compute the builder's tiered-summary replacement for an oversized
    repair diff, or "" when tiering does not apply -- the caller's existing
    flat-cap fallback (`compose_builder_prompt`'s `elif safe_diff and
    findings:` branch) then applies unchanged (F108 DECISION D3).

    `is_resumed` mirrors the caller's own precedence: a resumed session's
    shrunk hunk render already takes priority over the flat diff (DECISION
    F106 D1(b)), so this function must not spend a provider-availability
    resolve computing a value the caller would discard -- `call_fn_factory`
    (`summary_call_fn` itself, unapplied) is invoked only inside the branch
    that needs its result.
    """
    if is_resumed or not repair_diff or not findings:
        return ""
    if len(repair_diff) <= threshold_chars:
        return ""
    file_refs = {f.file for f in findings}
    return render_tiered_diff_text(
        repair_diff, file_refs, call_fn_factory(),
        threshold_chars=threshold_chars, full_ref=full_ref,
    )
```

  (b) In `run_pingpong`'s own body, immediately after the existing
  `builder_resume_hunks_text = ...` computation block ends (right before the
  existing `builder_composed = compose_builder_prompt(` call begins), insert:
```python
            builder_tiered_diff_text = _builder_tiered_diff_text(
                repair_diff, findings if is_repair else None,
                bool(builder_resume_ref and repair_diff), summary_call_fn,
                threshold_chars=_OVERSIZED_DIFF_THRESHOLD_CHARS,
                full_ref=f"repair diff, round {round_num} (F108: not yet persisted to evidence)",
            )
```
  and add `tiered_diff_text=builder_tiered_diff_text,` as a new line inside
  the existing `compose_builder_prompt(...)` call's argument list,
  immediately after its existing `resume_hunks_text=builder_resume_hunks_text,`
  line.

=== SPEC S9 (new tests in tests/orchestration/test_artifact_summaries.py) ===
Add a new section (after the existing T003a tests, matching the file's
`# ---...---` header convention) with exactly these 4 new test functions,
importing `render_tiered_diff_text` from the module under test:

1. `test_render_tiered_diff_text_under_threshold_returns_empty_string` --
   a short `diff_text` (well under a small `threshold_chars` you pass, e.g.
   `threshold_chars=100` with a 20-char diff_text), any `file_refs`,
   `call_fn=None` -- assert the result is `""`.
2. `test_render_tiered_diff_text_over_threshold_selects_only_relevant_sections`
   -- build a `diff_text` over your chosen `threshold_chars` (e.g.
   `threshold_chars=50` with a diff_text over 50 chars covering two files,
   `foo.py` and `bar.py`, using the module's own `_TWO_FILE_DIFF`-style
   git-header format so `section_diff` splits it into two sections), a fake
   `call_fn` returning a JSON body (mirroring the existing
   `test_generate_artifact_summary_success_with_fake_provider` pattern in
   this same file) with `l1` plus TWO `l2` entries matching sections
   `foo.py` and `bar.py`, and `file_refs=["foo.py"]`. Assert the result
   string contains the `foo.py` L2 summary text and does NOT contain the
   `bar.py` L2 summary text; assert it contains `"Full diff:"` and the
   `full_ref` value you passed.
3. `test_render_tiered_diff_text_over_threshold_no_call_fn_uses_fallback` --
   same over-threshold `diff_text` shape, `call_fn=None`. Assert the result
   contains `FALLBACK_MARKER` (already imported in this file) and contains
   `"Full diff:"`.
4. `test_render_tiered_diff_text_reduces_size_by_an_order_of_magnitude_on_a_long_diff_fixture`
   -- build a long synthetic diff fixture of at least 25000 characters (e.g.
   50 synthetic files of ~500 chars each in the `_TWO_FILE_DIFF` git-header
   format, looped), `threshold_chars=20000`, a fake `call_fn` returning a
   short JSON body (`l1` ~100 chars, ONE `l2` entry for one of the fixture's
   file sections), `file_refs` naming only that one file. Assert
   `len(result) < len(diff_text) / 10` (the feature's own "order of
   magnitude" acceptance wording, measured directly) and assert the result
   contains `"Full diff:"`.

Verify after writing: `python3 -m pytest tests/orchestration/test_artifact_summaries.py -q`
must show exactly 25 passed (21 base + 4 new).

=== SPEC S10 (new tests in tests/orchestration/test_builder_prompt_golden.py) ===
Add, near the existing `TestResumeHunksTextReplacesTheFullDiff` class (same
file, same import block extended with `_builder_tiered_diff_text` and
`_OVERSIZED_DIFF_THRESHOLD_CHARS` from `packages.orchestration.pingpong_loop`),
TWO new test classes with exactly these test methods:

`TestTieredDiffTextReplacesTheFlatCap` (mirrors
`TestResumeHunksTextReplacesTheFullDiff` exactly, for the new parameter):
1. `test_tiered_diff_text_replaces_the_flat_capped_diff` -- call
   `compose_builder_prompt(_GOAL, _CONTEXT, round_number=_ROUND,
   findings=_FINDINGS, safe_diff=_SAFE_DIFF, tiered_diff_text=<a literal
   multi-line string of your choosing ending in "\n">)`; assert
   `_segment_texts(composed)["builder_staged_diff"]` equals that string with
   `.rstrip("\n")` applied (mirroring how the existing resumed test asserts
   `texts["builder_staged_diff"] == _RESUME_HUNKS_TEXT.rstrip("\n")`).
2. `test_resume_hunks_text_still_takes_precedence_over_tiered_diff_text` --
   same call PLUS `resume_hunks_text=_RESUME_HUNKS_TEXT`; assert
   `texts["builder_staged_diff"] == _RESUME_HUNKS_TEXT.rstrip("\n")` (the
   tiered text you also passed must NOT appear).
3. `test_an_empty_tiered_diff_text_falls_back_to_the_flat_capped_diff` --
   `tiered_diff_text=""`; assert `texts["builder_staged_diff"] ==
   "## Current Staged Diff\n\`\`\`diff\n" + _SAFE_DIFF + "\n\`\`\`"` (the
   existing flat-cap render, same as the `full` shape's own assertion
   elsewhere in this file).

`TestBuilderTieredDiffTextHelper` (direct unit tests of the new pure helper,
imported from `packages.orchestration.pingpong_loop`):
4. `test_returns_empty_when_resumed` -- `is_resumed=True`, everything else
   populated (non-empty `repair_diff`, non-empty `findings`, a
   `call_fn_factory` that would raise if called), `threshold_chars=10`;
   assert result is `""`.
5. `test_returns_empty_when_no_findings` -- `findings=None`, long
   `repair_diff`, `is_resumed=False`, `call_fn_factory` that would raise if
   called; assert result is `""`.
6. `test_returns_empty_when_under_threshold` -- short `repair_diff`,
   non-empty `findings`, `is_resumed=False`, `threshold_chars` larger than
   `len(repair_diff)`, `call_fn_factory` that would raise if called; assert
   result is `""`.
7. `test_over_threshold_calls_render_tiered_diff_text_and_call_fn_factory_only_then`
   -- a `repair_diff` over `threshold_chars`, non-empty `findings` whose
   `.file` values you choose, `is_resumed=False`, a `call_fn_factory` that
   increments a counter when called and returns `None`; assert the counter
   is exactly 1 after the call (proving it is invoked lazily, exactly once,
   only in the branch that needs it) and assert the result is a non-empty
   string containing `FALLBACK_MARKER` (import `FALLBACK_MARKER` from
   `packages.orchestration.artifact_summary` for this assertion).

For tests 4-7, use `_FINDINGS` (already defined in this file) or a minimal
list of `ReviewFinding` for `findings`, matching this file's existing
construction pattern.

Verify after writing: `python3 -m pytest tests/orchestration/test_builder_prompt_golden.py -q`
must show exactly 35 passed (28 base + 7 new).

=== SLICE_LEDGER_R7 (C1 — append to .agent/live_review.md) ===
Append EXACTLY the following two paragraphs to the END of
`.agent/live_review.md`, separated from the file's current content by
`"\n\n"` and from each other by `"\n\n"`, with NO trailing newline after the
final paragraph (mirror the file's existing convention exactly -- read the
file's current last 300 bytes yourself with a short Python script before
editing, to confirm your starting point, then apply):

Gate: F108 R6 — T003a's GENERATION-CALL BRIDGE AND RELEVANT-SECTION MATCHING BUILT AND TESTED; R-0765/DECISION F108 D2's RE-SCOPE CORRECTLY BOOKED. VERDICT PASS. The reviewer independently re-verified round 6's committed diff `76982f2f`..`e7ef578f` against the real files, not the worker's own report. G1 TRANSPORT: `.agent/authored/f108-r6.md` and `.agent/last_block.md` independently sha256'd, both `cdaa371d2e36945f7ffa2f547a44713fa3304b458d9790f507ea2debf97d5f2a` at 26263 bytes, IDENTICAL. G2 LEDGER APPEND: `.agent/live_review.md` independently re-measured at 1953143 bytes, sha256 `3dec73df24aba9bbe717cc5d25c36e29f261b534fc9c2b3c160afbab65338ad9`, matching the round's own stated result exactly; `grep -c "^Gate: "` independently re-measured at 222, `grep -cE "^- R-[0-9]{4} — "` at 326, `grep -cE "^DECISION F[0-9]+ D[0-9]+ — "` at 23, all matching the handback's own counts. G3 R-0765 INDEPENDENTLY RE-VERIFIED: `grep -n "tiered\|summary\|artifact" packages/orchestration/context_compiler.py` independently re-run, zero matches, confirming the finding's central claim (the module's docstring never anticipated tiered summaries) still holds against the real file. G4 THE MODULE: `packages/orchestration/artifact_summary.py`'s new `summary_call_fn`/`select_relevant_sections` independently read in full — matches DECISION F108 D2's CHOSEN description exactly: `summary_call_fn` resolves the `summary` role via `resolve_role_config` and feeds the model into `make_structured_call_fn` (signature independently confirmed at `intake.py:280-284`, `model` keyword accepted); `select_relevant_sections` is exact `section` string equality against `file_refs`, empty on no match, never raises. `packages/orchestration/role_config.py`'s corrected comment independently read: the false "nothing in production code currently calls" sentence is gone (0 matches), replaced with a sentence correctly naming `summary_call_fn` (1 match); `KNOWN_ROLES` itself untouched. G5 THE TESTS: `python3 -m pytest tests/orchestration/test_artifact_summaries.py -q` independently re-run, real exit 0, 21 passed (16 base + 5 new); `python3 -m pytest tests/orchestration/test_role_config.py -q` independently re-run, real exit 0, 34 passed, unchanged. G6 STATE READERS: `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q` independently re-run, real exit 0, 604 passed, matching base exactly. G7 CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` independently re-run, real exit 0, 42 passed, matching base exactly. G8 TREE: `git status --porcelain` empty at review time; HEAD confirmed pushed and equal to `origin/feature/f108-tiered-artifact-summaries` at `e7ef578f`; `git diff --stat 76982f2f..HEAD` independently confirmed to touch exactly the 8 declared paths (`.agent/authored/f108-r6.md`, `.agent/handoff.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `packages/orchestration/artifact_summary.py`, `packages/orchestration/role_config.py`, `tests/orchestration/test_artifact_summaries.py`), nothing else, every commit's insertions independently re-measured under 500 (largest 167, C0a). No deviation found beyond the two the worker itself declared (the disposable-worktree BEFORE reading, and S2's own five-quoted-lines-vs-"last four" prose miscount) — both independently confirmed real and correctly handled: the worktree's removal left `git status --porcelain` empty and HEAD unchanged throughout, and the FROM/TO text for the role_config.py comment matched disk byte-for-byte regardless of the miscounted adjective.

DECISION F108 D3 — T003b'S FIRST ROUND WIRES ONLY THE BUILDER REPAIR-DIFF BRANCH; A NEW STANDALONE RENDERING HELPER CARRIES THE THRESHOLD/SELECTION LOGIC; full_ref IS A DESCRIPTIVE LABEL, NOT YET A PERSISTED PATH; REVIEWER-SIDE WIRING AND DISK CACHING ARE DEFERRED. THE PROBLEM: DECISION F108 D2 named `pingpong_loop.py`'s `compose_builder_prompt`/`compose_reviewer_prompt` diff-inclusion branches as T003b's targets in general terms but left the exact call-site precedence, the new threshold constant's value, and the caching/persistence question undecided — `.agent/plan.md`'s own Risks section flags exactly this ("the round inspects the exact call-site precedence... before extending it"). CHOSEN: (1) a new pure function `render_tiered_diff_text(diff_text, file_refs, call_fn, *, threshold_chars, full_ref)` in `artifact_summary.py` sections the diff (`section_diff`), generates via `generate_artifact_summary`, selects via `select_relevant_sections`, and renders a "## Current Staged Diff (summarized)" text, or "" at/under `threshold_chars` (the caller's signal to keep its existing flat-cap behavior). (2) a new pure gating helper `_builder_tiered_diff_text(repair_diff, findings, is_resumed, call_fn_factory, *, threshold_chars, full_ref)` in `pingpong_loop.py` fixes the precedence this round inspects: a resumed session (`is_resumed`) or no findings or a diff at/under threshold always returns "", so `compose_builder_prompt`'s existing `resume_hunks_text` precedence (DECISION F106 D1(b)) is preserved untouched and `summary_call_fn`'s Ollama-availability resolve is never spent when its result would be discarded — `call_fn_factory` is called (`summary_call_fn` itself, unapplied) only inside the branch that needs it. (3) `compose_builder_prompt` gains one new keyword parameter, `tiered_diff_text: str = ""`, checked in a new `elif tiered_diff_text:` branch between the existing `if resume_hunks_text:` and `elif safe_diff and findings:` — same segment name/rank (`builder_staged_diff`, JOB_CONTEXT) the flat-cap branch already uses, mirroring exactly how `resume_hunks_text` itself was added (round 12, DECISION F106 D1(b)); an empty string always falls through to the unchanged flat-cap branch, so every existing golden-test shape (`minimal`/`scope_task`/`staged`/`full`/`resumed`) is untouched. (4) the new threshold constant, `_OVERSIZED_DIFF_THRESHOLD_CHARS`, is set equal to the existing `_REPAIR_DIFF_CAP` (20000) — tiering activates exactly where the flat truncation used to activate, so this round literally REPLACES `_REPAIR_DIFF_CAP`'s truncation behavior for oversized diffs rather than adding a second, disconnected magic number. (5) `full_ref` this round is the descriptive string `f"repair diff, round {round_num} (F108: not yet persisted to evidence)"` — honest about NOT being a real path yet, since no artifact file is written to disk this round (T001's `save_summary`/`load_cached_summary` file-based caching stays unwired here); a later round persists the diff to evidence and passes a real path, which is WHEN the feature's literal "reference path present" Done condition is met for this call site. ALTERNATIVES CONSIDERED: (a) wire disk caching plus a real evidence path in the same round — rejected, too large for the 8-gate budget on top of the compose_builder_prompt/call-site changes and untested precedent (no existing call site writes ephemeral diff text to evidence for hashing); (b) wire `compose_reviewer_prompt`'s three diff branches in the same round — rejected for the same size reason; deferred to a follow-up round, tracked in `.agent/plan.md`. WHAT REMAINS FOR F108's DONE CONDITION: reviewer-side wiring (three cap sites: `_REVIEWER_DIFF_CAP`, `_REVIEWER_SCOPED_DIFF_CAP`, and the unscoped/scoped precedence already established in `compose_reviewer_prompt`), a real persisted `full_ref` path (disk caching wired), and the long-artifact fixture plus size-comparison recorded as the feature's own acceptance evidence — all tracked as open items in `.agent/plan.md`'s Next Steps, not claimed done here. HOW TO REVERSE: delete `render_tiered_diff_text`, `_builder_tiered_diff_text`, the `tiered_diff_text` parameter and its call site, and their tests; `compose_builder_prompt`'s remaining branches are byte-for-byte what they were before. WHAT IT COSTS TO BE WRONG: if the reviewer-side wiring later finds a different precedent shape is needed, the cost is one more standalone tested function plus one more parameter — the builder side stays correct and inert-safe (a "" `tiered_diff_text` is always a legal, already-tested input) regardless.

After applying, independently verify with a short Python script (read the
file, decode utf-8, check the tail): the file's new length is 1961415 bytes
and its sha256 is `8d90730092b1d13729d623eb9f0529fe76882a1bc02fa79acaa8a927ffa89e1a`.
Also verify `grep -c "^Gate: "` reads 223, `grep -cE "^DECISION F[0-9]+ D[0-9]+ — "`
reads 24, and `grep -cE "^- R-[0-9]{4} — "` is UNCHANGED at 326 (this round
mints no new R-id). If any of these four numbers do not match, STOP, do not
commit, and report the mismatch in your handback instead of forcing a match.

=== SLICE_PLAN_R7 (C5 — rewrite .agent/plan.md to exactly this text) ===
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
| T003b-ii reviewer-side wiring (3 cap sites) | pending | next round |
| T003c real persisted `full_ref` + disk caching | pending | after T003b-ii |
| T003d long-artifact fixture + size comparison (DONE evidence) | pending | after T003c |

## Next Steps
1. Round 8: T003b-ii — wire the same `render_tiered_diff_text` shape into
   `compose_reviewer_prompt`'s three diff branches (`_REVIEWER_DIFF_CAP`,
   `_REVIEWER_SCOPED_DIFF_CAP`, and the resume/scoped precedence already
   there), per DECISION F108 D3's deferral.
2. T003c: persist the diff to evidence, pass a real `full_ref` path, wire
   T001's `load_cached_summary`/`save_summary` at both call sites.
3. T003d: the long-artifact fixture and size-comparison recording — the
   feature's own DONE-condition evidence.
4. Integration gate (full suite, both required runs) before closure.
5. Closure sequence: README sync, STATUS `[x]`, evidence bundle, review
   package.

## Risks
- T003b-ii repeats T003b-i's own risk one branch over: `compose_reviewer_prompt`'s
  scoped/unscoped/resume precedence is a four-way branch (DECISION F108 D3's
  builder-side helper only covers three), so that round re-derives it from
  the real code rather than assuming symmetry with the builder side.

Independently verify after applying: 47 lines, 2448 bytes, sha256
`a69307b0895c8005177d2dcd4f1d66db1b3f98ced5d5c0ed66a0a3691ae7be02`. If these
do not match your applied file, STOP, do not commit, and report the mismatch.

Done when (verification commands — run every one yourself, record real exit
codes and full output in your handback, never assert "green" as a word):
  G1 TRANSPORT: `sha256sum .agent/authored/f108-r7.md .agent/last_block.md`
      -- both digests IDENTICAL.
  G2 LEDGER APPEND: the four independent-verification numbers named above
      (byte count, sha256, Gate count, DECISION count) all match; R- count
      unchanged at 326.
  G3 NEW CODE: `python3 -c "import packages.orchestration.artifact_summary"`
      exits 0; `python3 -m pytest tests/orchestration/test_artifact_summaries.py -q`
      shows exactly 25 passed. THEN a mutation red-proof, in a disposable
      `git worktree` only (never the primary checkout; remove the worktree
      after): edit your new `render_tiered_diff_text`'s
      `if len(diff_text) <= threshold_chars:` line so the condition is
      always `False` (e.g. replace with `if False:`), run
      `test_render_tiered_diff_text_under_threshold_returns_empty_string`
      and confirm it FAILS with a real AssertionError; then confirm it
      PASSES again unmutated in the primary checkout. Report both readings.
  G4 PINGPONG WIRING: `python3 -m pytest tests/orchestration/test_builder_prompt_golden.py -q`
      shows exactly 35 passed. THEN a mutation red-proof, same disposable
      worktree discipline: edit your new `elif tiered_diff_text:` branch's
      condition to always be `False` (e.g.
      `elif False and tiered_diff_text:`), run
      `test_tiered_diff_text_replaces_the_flat_capped_diff` and confirm it
      FAILS; confirm it PASSES again unmutated. Report both readings.
  G5 CALL-SITE REGRESSION: `python3 -m pytest tests/orchestration/test_pingpong_cli.py -q`
      shows exactly 172 passed (unchanged from base -- this file is not
      edited this round, this gate proves the wiring introduced no
      import-time or collection-time breakage).
  G6 STATE READERS: `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q`
      shows 604 passed (unchanged from base).
  G7 CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` shows 42
      passed (unchanged from base).
  G8 TREE + PLAN + SIZE: `git status --porcelain` empty after the final
      commit (before push); `.agent/plan.md` is exactly 47 lines; every
      commit's insertions (the `+` column of `git diff --stat` per commit)
      are under 500; `git diff --stat 76982f2f..HEAD` (excluding the final
      handoff commit) touches exactly the 8 declared change-set paths,
      nothing else.

Handback: after all commits land, `git push -u origin feature/f108-tiered-artifact-summaries`
and report the real exit code and the remote tip SHA (`git ls-remote origin
feature/f108-tiered-artifact-summaries`). Then write the completion report
+ rewrite `.agent/handoff.md` (C6) per AGENTS.md's `### handoff.md` section:
feature+round, SESSION NUMBER (this is session 2 of F108 -- the prior
handoff read "SESSION 1"), branch, commit SHAs, changed-files table with
real `+/-` per commit, verification results (every G1-G8 reading, real,
not summarized as "green"), open findings count (0 -- this round mints no
new R-id), next expected action (round 8, T003b-ii, per the Next Steps
above). If ANY gate above goes red, do NOT force a fix that isn't in this
block's scope -- stop, declare the exact failure, and leave the tree at the
last clean commit; do not push a red state silently.
── end step ──────────────────────────────────────────────────────────────