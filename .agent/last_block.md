── STEP T003d/T003 — F108 Tiered artifact summaries ────────────────────────
Goal: prove the feature's own DONE-condition wording — "a fixture long
[artifact] enters a follow-up prompt at a fraction of its size with the
reference path present" — with an end-to-end test that drives real
`run_pingpong` builder AND reviewer phases through round-9's already-landed
tiering wiring, per DECISION F108 D6 (below), discharging plan.md's Risk
note and closing out T003.

Bundle:
  C0a. Save this entire step block verbatim to `.agent/authored/f108-r10.md`
       (copy the bytes between the two `=== BEGIN/END STEP BLOCK ===` marker
       lines, excluding the marker lines themselves).
  C0b. Mirror `.agent/authored/f108-r10.md` byte-for-byte to `.agent/last_block.md`.
  C1.  Append SLICE_LEDGER_R10 (two paragraphs: `Gate: F108 R9`, then
       `DECISION F108 D6`) to `.agent/live_review.md`, exactly as given below.
  C2.  Implement SPEC S1-S2 in `tests/orchestration/test_pingpong_cli.py`
       (below) — new imports plus one new end-to-end test.
  C3.  Rewrite `.agent/plan.md` to SLICE_PLAN_R10 (exact bytes given below).
  C4.  Rewrite `.agent/handoff.md` per AGENTS.md's `### handoff.md` section
       (this round's own completion report; no length cap, amend0827 rule 3).

Change (bounds this round's FILE WRITES only — push and worktree cleanup
are separate obligations, stated in Handback below):
  .agent/authored/f108-r10.md (new), .agent/last_block.md,
  .agent/live_review.md, tests/orchestration/test_pingpong_cli.py,
  .agent/plan.md, .agent/handoff.md. Nothing else. Keep each commit under
  500 inserted lines (AGENTS.md); the `.agent/**` single-file-rewrite
  exemption applies per commit that is a verbatim rewrite of ONE state file.

Constraints:
  - Do NOT touch `packages/orchestration/artifact_summary.py` or
    `packages/orchestration/pingpong_loop.py` — this round ships NO new
    production code; round 9's landed wiring is exercised, not modified.
  - Do NOT touch `tests/orchestration/test_artifact_summaries.py`,
    `test_builder_prompt_golden.py`, or `test_reviewer_prompt_golden.py`.
  - The new test's large fixture content must be GOAL-INDEPENDENT (see
    DECISION F108 D6) — do not derive its size from the `goal` string passed
    to `run_pingpong`.
  - Follow AGENTS.md File Editing Safety Rules: read
    `tests/orchestration/test_pingpong_cli.py`'s relevant regions in full
    before editing, re-read after, verify syntax and logical consistency.
    Re-grep every anchor named below for its current exact bytes before
    editing — do not trust a line number stated anywhere in this block.

=== SPEC S1 (imports — tests/orchestration/test_pingpong_cli.py) ===
Two edits to this file's import section (currently lines 16-44 of the
branch tip; re-grep to confirm before editing):

1. In the existing `from packages.orchestration.pingpong_loop import (`
   block, insert two new lines immediately BEFORE the existing
   `_STAGING_NOISE_DIRS,` line:
     _OVERSIZED_DIFF_THRESHOLD_CHARS,
     _OVERSIZED_REVIEWER_SCOPED_DIFF_THRESHOLD_CHARS,
   and insert one new line immediately BEFORE the existing
   `_snapshot_target,` line:
     _pingpong_runs_dir,
2. Immediately after that whole import block's closing `)`, on its own new
   line, add:
     import packages.orchestration.pingpong_loop as pingpong_loop
   (a module-qualified import, needed so the new test in S2 can
   `monkeypatch.setattr(pingpong_loop, ...)` — every existing import in this
   file imports individual NAMES, never the module object itself, so this is
   new.)

=== SPEC S2 (new test — tests/orchestration/test_pingpong_cli.py, end of file) ===
Append, after the file's final existing test (`TestRunPingpongPromptNoLeak`,
ending with `test_builder_prompt_safe_context_present` at the branch tip),
a new section-comment block matching this file's own `# --- ... ---` visual
convention, then exactly ONE new test class with ONE test method:

```python
# ---------------------------------------------------------------------------
# F108 T003d: end-to-end tiered summaries reduce composed prompt size
# ---------------------------------------------------------------------------

class TestTieredSummariesReduceComposedPromptSize:
    def test_both_call_sites_tiered_and_prompt_shrinks_an_order_of_magnitude(
        self, demo_repo, monkeypatch,
    ):
        big_content = "\n".join(f"# line {i:05d}: " + "x" * 70 for i in range(1000))

        def fake_apply(staging, builder_output, goal):
            for rel_path in builder_output.files_changed:
                fp = staging / rel_path
                fp.parent.mkdir(parents=True, exist_ok=True)
                fp.write_text(big_content)

        monkeypatch.setattr(pingpong_loop, "_apply_fake_builder_changes", fake_apply)

        fake_response = json.dumps({
            "l1": "x" * 100,
            "l2": [
                {"section": "big.py", "span_ref": "file:big.py", "summary": "SECTION SUMMARY"},
            ],
        })

        def fake_call_fn(prompt: str, attempt: int) -> str:
            return fake_response

        monkeypatch.setattr(pingpong_loop, "summary_call_fn", lambda: fake_call_fn)

        provider = FakeProvider(builder_files=["big.py"], fail_on_round=1, pass_on_round=2)
        result = run_pingpong(
            "Fix big file", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            max_rounds=2, repair_rounds=2,
        )
        assert len(result.rounds) == 2

        reviewer_trace = next(
            t for t in result.prompt_traces if t.role == "reviewer" and t.round == 1)
        builder_trace = next(
            t for t in result.prompt_traces if t.role == "builder" and t.round == 2)

        reviewer_artifact = (
            _pingpong_runs_dir() / result.run_id / "calls" / "reviewer"
            / "round-01" / "tiered_diff.diff")
        builder_artifact = (
            _pingpong_runs_dir() / result.run_id / "calls" / "builder"
            / "round-02" / "tiered_diff.diff")
        assert reviewer_artifact.exists()
        assert builder_artifact.exists()

        raw_reviewer_len = len(reviewer_artifact.read_text())
        raw_builder_len = len(builder_artifact.read_text())
        assert raw_reviewer_len > _OVERSIZED_REVIEWER_SCOPED_DIFF_THRESHOLD_CHARS
        assert raw_builder_len > _OVERSIZED_DIFF_THRESHOLD_CHARS

        assert reviewer_trace.prompt_chars < raw_reviewer_len / 10
        assert builder_trace.prompt_chars < raw_builder_len / 10
```

`json` is already imported at this file's top (`import json`); `FakeProvider`
and `run_pingpong` are already imported. Do not add any other test.

Verify after writing: `python3 -m pytest tests/orchestration/test_pingpong_cli.py -q`
must show exactly 173 passed (172 base + 1 new).

=== SLICE_LEDGER_R10 (C1 — append to .agent/live_review.md) ===
Append EXACTLY the following two paragraphs to the END of
`.agent/live_review.md`, separated from the file's current content by
`"\n\n"` and from each other by `"\n\n"`, with NO trailing newline after the
final paragraph (mirror the file's existing convention exactly — read the
file's current last 300 bytes yourself with a short Python script before
editing, to confirm your starting point, then apply):

Gate: F108 R9 — T003c REAL PERSISTED full_ref + HASH-INVALIDATED CACHE, BOTH CALL SITES, LANDED AND MUTATION-PROVEN; DECISION F108 D5'S SCOPE HELD EXACTLY. VERDICT PASS. This reviewer (session 3, a fresh session carrying no memory of round 9's own work) independently re-verified round 9's committed diff `0bd996ac`..`07749d21` against the real files on disk, not the worker's own handback report. G1 CODE: `packages/orchestration/artifact_summary.py`'s `render_tiered_diff_text` (new optional `artifact_path: Path | None = None` parameter, cache-aware body -- writes `diff_text` to `artifact_path`, checks `load_cached_summary(artifact_path)`, calls `generate_artifact_summary` only on a miss, `save_summary(artifact_path, summary)` after a fresh generation) and `packages/orchestration/pingpong_loop.py`'s `_builder_tiered_diff_text`/`_reviewer_tiered_diff_text` (pure forwarding of the same new parameter) and both `run_pingpong` call sites (real `_pingpong_runs_dir() / result.run_id / "calls" / "<role>" / f"round-{round_num:02d}" / "tiered_diff.diff"` paths, passed as both `full_ref` and `artifact_path`) were all independently read in full and confirmed to match DECISION F108 D5's CHOSEN shape exactly; the parameter's optionality (`None` default, original stateless contract unchanged) was confirmed by reading every pre-round-9 call site of `render_tiered_diff_text` and finding none of them pass it. G2 TESTS: `python3 -m pytest tests/orchestration/test_artifact_summaries.py tests/orchestration/test_builder_prompt_golden.py tests/orchestration/test_reviewer_prompt_golden.py tests/orchestration/test_pingpong_cli.py -q` independently re-run by this reviewer, real exit 0, 274 passed (27+39+36+172), matching the round's own claimed per-file counts exactly. G3 MUTATION RED-PROOFS -- INDEPENDENTLY REPRODUCED FROM SCRATCH, NOT TAKEN ON THE WORKER'S WORD: in a fresh disposable worktree (`git worktree add .remedy-wt/f108-r10-review-mutation HEAD --detach`), changing `render_tiered_diff_text`'s `summary = load_cached_summary(artifact_path)` line to `summary = None  # MUTATION: force cache miss always` made `test_render_tiered_diff_text_with_artifact_path_cache_hit_skips_generation` FAIL with a real `AssertionError: assert 'cached summary, never regenerated' in '## Current Staged Diff (summarized)\n[summary unavailable -- truncated view]\n...'`; after reverting that file to its committed state, dropping `_builder_tiered_diff_text`'s `artifact_path=artifact_path,` argument from its own `render_tiered_diff_text(...)` call made `TestBuilderTieredDiffTextHelper::test_forwards_artifact_path_to_render_tiered_diff_text` FAIL with a real `AssertionError: assert False, where False = exists()`; `git status --porcelain` on the PRIMARY checkout was read empty immediately before the worktree was created, immediately after each mutating edit, and again after the worktree was removed -- the primary checkout was never mutated at any point. G4 LEDGER + PLAN: `.agent/live_review.md` independently re-measured at 1980392 bytes, sha256 `b67820ab9d35b2cc594949d03b58ea0934d8ae285dffc04d63e4211d0524c343`, `grep -c "^Gate: "` at 225, `grep -cE "^DECISION F[0-9]+ D[0-9]+ -- "` at 26, `grep -cE "^- R-[0-9]{4} -- "` unchanged at 326, all matching the round's own stated result exactly; `.agent/plan.md` independently re-measured at 42 lines, 2113 bytes, sha256 `430a6580045a39295fb99fa556e2e7fd933ed5d9667321e04bd4ea50c3e122ea`, matching the round's stated SLICE_PLAN_R9 digest exactly. G5 TREE: `git status --porcelain` empty; `git diff --stat 0bd996ac..HEAD` independently confirmed to touch exactly the 9 non-handoff declared paths plus the handoff commit itself (10 files, 843 insertions, 480 deletions total), matching the handback's own accounting. ONE PROSE-ONLY INACCURACY IN THE ROUND'S OWN HANDBACK, NOTED, NO PRODUCT EFFECT, NOT REPAIRED: the R9 block's own G8 text said "8 declared change-set paths" for the non-handoff sweep while the real, correctly-matching count is 9 -- the round's own handback already caught and disclosed this itself under "Deviations & assumptions" rather than silently miscounting, so no correction is owed beyond this note carrying it forward into the permanent gate record. No deviation found in the round's own committed product code or tests.

DECISION F108 D6 — T003D'S FIXTURE DRIVES `run_pingpong` END TO END WITH A MONKEYPATCHED `_apply_fake_builder_changes`, NOT A GOAL-STRING-INFLATED `FakeProvider` OR A STATEFUL `claude-cli` BASH FIXTURE. THE PROBLEM: T003d (plan.md's own Risk note) requires a fixture that exercises the REAL call sites inside `run_pingpong` -- not `render_tiered_diff_text` in isolation -- and asserts the actually-SENT composed prompt is an order of magnitude smaller than the raw diff. The obvious route, inflating `FakeProvider`'s own `goal` argument so `_apply_fake_builder_changes`'s `content += f"\n\n<!-- Remedy: {goal} -->\n"` line writes a large staged file, is a dead end: `compose_builder_prompt`/`compose_reviewer_prompt` also embed the full `goal` text verbatim in their own "Goal" segment regardless of tiering, so inflating `goal` inflates the composed prompt by the SAME amount it inflates the raw diff and the order-of-magnitude comparison the DONE condition asks for becomes unmeasurable by construction. CHOSEN: `FakeProvider(builder_files=["big.py"], fail_on_round=1, pass_on_round=2)` drives exactly two rounds (round 1 needs_repair with one finding on `big.py`, round 2 pass -- the existing `TestRepairRoundGetsDiff` pattern), with `max_rounds=2, repair_rounds=2`; the test's own `monkeypatch.setattr(pingpong_loop, "_apply_fake_builder_changes", ...)` replaces ONLY the fake-content-authoring internal for the duration of the test with a version that writes a large, deterministic, goal-INDEPENDENT string (~86000 characters, no provider call, no network) into `big.py`, so the raw diff is large while the composed prompt's "Goal" segment stays a short literal goal string; `monkeypatch.setattr(pingpong_loop, "summary_call_fn", lambda: fake_call_fn)` makes the tiered summary itself deterministic and offline, mirroring round 7's and round 9's own fake-provider JSON-fixture pattern. The reviewer's own scoped-diff site fires in round 1 (its gate does not depend on repair at all, only on `is_resumed=False` and a non-empty safe diff); the builder's own repair-diff site fires in round 2 (`repair_diff` is computed from round 1's `result.staged_files`, and round 2's `findings` come from round 1's one real `ReviewFinding`) -- both are DECISION-independent facts of the already-landed round-9 wiring, re-read from `pingpong_loop.py`'s exact current bytes before this DECISION was written, not assumed. The test reads back the two real persisted `tiered_diff.diff` artifact files at their real, deterministic paths and compares each one's length against its matching `result.prompt_traces` entry's real `.prompt_chars` field (the exact composed-prompt length `run_pingpong` actually sent), asserting `prompt_chars < raw_len / 10` at both call sites -- the feature's own "enters a follow-up prompt... at a fraction of its size" DONE-condition wording, measured on the real call sites the plan.md Risk note demands. ALTERNATIVES CONSIDERED: (a) a stateful `fake_claude_builder_bin`/`fake_claude_reviewer_bin` bash-script pair (the existing claude-cli fixture family) -- rejected as heavier for no added correctness: no existing reviewer fixture is call-count-aware (round 1 fail, round 2 pass), so this route would add a small state-file protocol to a bash script for a property `FakeProvider`'s own `fail_on_round`/`pass_on_round` constructor args already give for free. (b) drive both call sites through `render_tiered_diff_text` directly, as round 7's own fixture test does -- rejected, this is exactly the isolation plan.md's Risk note names as insufficient for T003d's own DONE condition ("not just `render_tiered_diff_text` in isolation"). WHAT REMAINS: the integration gate and the closure sequence -- both plan.md `Next Steps` items, unaffected by this DECISION. HOW TO REVERSE: delete the new test class and its two monkeypatches; nothing else in `pingpong_loop.py` or `artifact_summary.py` is touched by this round, so no production code needs unwinding. WHAT IT COSTS TO BE WRONG: if the ~86000-character deterministic fixture string ever proves too small against a future threshold change, the cost is raising one literal in the test, not a design change -- the monkeypatch shape itself (goal-independent content, both real call sites exercised, real `prompt_traces` read back) is the part this DECISION commits to, not the exact byte count.

After applying, independently verify with a short Python script (read the
file, decode utf-8, check length/hash): the file's new length is 1989050
bytes and its sha256 is `cf2de0297d9761de40f9a16aeaad46d4739775a917c560a172881f2a8d43e5b2`.
Also verify `grep -c "^Gate: "` reads 226, `grep -cE "^DECISION F[0-9]+ D[0-9]+ — "`
reads 27, and `grep -cE "^- R-[0-9]{4} — "` is UNCHANGED at 326 (this round
mints no new R-id). If any of these four numbers do not match, STOP, do not
commit, and report the mismatch in your handback instead of forcing a match.
Note the two "--" occurrences you are copying inside the Gate/DECISION
paragraph text above are literal double-hyphens (ASCII), matching this
file's own established prose style — only the em dash right after `F108 R9`
and right after `F108 D6` is the real "—" character; copy the paragraph
text exactly as given, character for character, do not substitute either
dash style for the other.

=== SLICE_PLAN_R10 (C3 — rewrite .agent/plan.md to exactly this text) ===
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
| T003c real persisted `full_ref` + disk caching, both call sites | done | round 9, D5 |
| T003b-iii reviewer fallback-branch wiring | pending | deferred, D4 |
| T003d long-artifact fixture + size comparison (DONE evidence) | done | round 10, D6 |

## Next Steps
1. Integration gate (full suite, both required runs) before closure.
2. Closure sequence: README sync, STATUS `[x]`, evidence bundle, review
   package.

## Risks
- None open. T003d's fixture exercised the REAL call sites (`run_pingpong`'s
  builder/reviewer phases) per DECISION F108 D6, discharging the prior
  round's Risk note.

Independently verify after applying: 35 lines, 1621 bytes, sha256
`73785aa588e2084a52589b0762f7fcb52302d5dbe23917c45f8b09d82a97f16f`. If
these do not match your applied file, STOP, do not commit, and report the
mismatch.

Done when (verification commands — run every one yourself, record real exit
codes and full output in your handback, never assert "green" as a word):
  G1 TRANSPORT: `sha256sum .agent/authored/f108-r10.md .agent/last_block.md`
      — both digests IDENTICAL.
  G2 LEDGER APPEND: the length/hash/count numbers named above (1989050
      bytes, the stated sha256, Gate=226, DECISION=27) all match; R- count
      unchanged at 326.
  G3 NEW TEST + IMPORT WIRING + MUTATION RED-PROOFS:
      `python3 -m pytest tests/orchestration/test_pingpong_cli.py -q` shows
      exactly 173 passed (172 base + 1 new). THEN, in a disposable
      `git worktree` only (never the primary checkout; remove the worktree
      after; run `git status --porcelain` on the PRIMARY the moment each
      mutation is typed): (a) change
      `_reviewer_tiered_diff_text`'s current line
      `if is_resumed or not safe_diff or not scope_packet:`
      (pingpong_loop.py, re-grep to confirm) to `if True:`, run
      `TestTieredSummariesReduceComposedPromptSize::test_both_call_sites_tiered_and_prompt_shrinks_an_order_of_magnitude`
      and confirm it FAILS with a real AssertionError (reviewer artifact
      never written); revert; confirm PASSES again unmutated. (b) change
      `_builder_tiered_diff_text`'s current line
      `if is_resumed or not repair_diff or not findings:`
      to `if True:`, run the SAME test, confirm it FAILS with a real
      AssertionError (builder artifact never written); revert; confirm
      PASSES again unmutated. Report all four readings (2 mutated-red, 2
      unmutated-green) plus the `git status --porcelain` reading taken
      immediately after each mutation.
  G4 REGRESSION (unchanged, no new production code this round):
      `python3 -m pytest tests/orchestration/test_artifact_summaries.py tests/orchestration/test_builder_prompt_golden.py tests/orchestration/test_reviewer_prompt_golden.py -q`
      shows exactly 102 passed (27 + 39 + 36), unchanged from round 9.
  G5 STATE READERS: `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q`
      shows 604 passed (unchanged from base).
  G6 CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` shows 42
      passed (unchanged from base).
  G7 TREE + PLAN + SIZE: `git status --porcelain` empty after the final
      commit (before push); `.agent/plan.md` is exactly 35 lines, 1621
      bytes; every commit's insertions (the `+` column of `git diff --stat`
      per commit) are under 500; `git diff --stat 07749d21..HEAD`
      (excluding the final handoff commit; re-confirm `07749d21` is really
      round 9's own tip with `git log --oneline` before using it) touches
      exactly the 5 declared non-handoff change-set paths, nothing else.

Handback: after all commits land, `git push -u origin feature/f108-tiered-artifact-summaries`
and report the real exit code and the remote tip SHA (`git ls-remote origin
feature/f108-tiered-artifact-summaries`). Then write the completion report
+ rewrite `.agent/handoff.md` (C4) per AGENTS.md's `### handoff.md` section:
feature+round, SESSION NUMBER (this is SESSION 3 of F108 — a new Claude Code
session with no memory of sessions 1-2 — round 10), branch, commit SHAs,
changed-files table with real `+/-` per commit, verification results (every
G1-G7 reading, real, not summarized as "green"), open findings count (0 —
this round mints no new R-id), next expected action (the integration gate,
per the Next Steps above). If ANY gate above goes red, do NOT force a fix
that isn't in this block's scope — stop, declare the exact failure, and
leave the tree at the last clean commit; do not push a red state silently.
── end step ──────────────────────────────────────────────────────────────