── STEP T003-b / F111 — Round 17 ─────────────────────────────
Goal:
  Record the R16 verdict, then close the APPLY half of T003: a repair answer
  that arrives as a unified-diff wrapper is routed through `apply_diff_repair`
  inside the existing bridge, and any conflict discards the attempt whole,
  names the reason, and puts the NEXT cycle back on the full-file path. R16
  wired what a repair round SENDS; this wires what it ACCEPTS.

Bundle (ordered; one commit each, push after EVERY commit per R-0289):
  C1  save this block verbatim to .agent/authored/f111-r17-1.md
  C2  mirror the same bytes into .agent/last_block.md
  C3  .agent/live_review.md, TEXT-A appended, one commit
  C4  the diff channel, in packages/orchestration/builder_bridge.py
  C5  tests, in tests/orchestration/test_builder_repair_loop.py
  C6  replace .agent/plan.md with TEXT-B, then rewrite .agent/handoff.md

Scope — EXACTLY these seven paths, no others:
  1 .agent/authored/f111-r17-1.md   2 .agent/last_block.md
  3 .agent/live_review.md           4 packages/orchestration/builder_bridge.py
  5 tests/orchestration/test_builder_repair_loop.py
  6 .agent/plan.md                  7 .agent/handoff.md

Change — C4, packages/orchestration/builder_bridge.py. Four edits, no others.

  EDIT 1 — one new stop reason. Add `"diff_repair_fell_back"` to the
  `STOP_REASONS` frozenset, keeping the existing formatting.

  EDIT 2 — `BridgeResult` gains two fields, each with the one-line WHY comment
  above it that this repo's conventions require:
    diff_repair_mode: str = ""        # "" when the round used no diff channel
    diff_fallback_reason: str = ""

  EDIT 3 — `run_builder_bridge` gains ONE keyword-only argument,
  `diff_response: Any = None` (a `DiffRepairResponse` when the caller decoded
  one). Two places change inside it and nothing else:

  (a) Stage 1. Replace the single `parse_result = parse_builder_patch(output)`
      line with a branch. When `diff_response` is None, behaviour is exactly
      what it is today. When it is not None, build the parse result from the
      converted patch instead of re-reading the raw text:

        import hashlib
        raw = output.structured_patch_text or ""
        parse_result = BuilderPatchResult(
            parse_success=True,
            patch=diff_repair_response_to_patch(diff_response),
            target_paths=list(diff_response.files),
            output_hash=hashlib.sha256(raw.encode()).hexdigest()[:16],
            output_length=len(raw),
        )

      `risk` and `requires_approval` keep their model defaults on purpose.
      State that as a one-line comment: risk classification lives in the
      structured-patch parser, and Remedy deliberately does not compute a
      second risk level on the diff channel in v1. Everything downstream of
      this assignment — the `builder_patch_parsed` emit, the approval gate,
      `_create_and_approve_intent` — is UNCHANGED and runs for both channels.

  (b) Stage 3. Keep the existing `set_permission` line and the existing
      `apply_structured_patch` block exactly as they are for the
      `diff_response is None` case. When `diff_response` is not None, call
      `apply_diff_repair` INSTEAD of `apply_structured_patch`:

        diff_result = apply_diff_repair(
            diff_response, repo_path,
            job=job, intent_id=intent_id, data_dir=data_dir,
        )
        result.diff_repair_mode = diff_result.mode
        result.diff_fallback_reason = diff_result.fallback_reason
        _emit(data_dir, job.id, "diff_repair_applied", {
            "mode": diff_result.mode,
            "applied": diff_result.applied,
            "fallback_reason": diff_result.fallback_reason,
            "files_modified": diff_result.files_modified,
            "rollback_incomplete": diff_result.rollback_incomplete,
            "error_count": len(diff_result.errors),
        })
        if not diff_result.applied:
            result.stage = "diff_fallback"
            result.stop_reason = "diff_repair_fell_back"
            return result
        result.apply_success = True
        result.stage = "applied"

      Stage 4 (tests) then runs for the diff channel exactly as it does today,
      because a landed diff is an applied patch and nothing distinguishes it
      downstream.

  EDIT 4 — `run_builder_bridge_loop`. Between the existing
  `repair_loop_cycle_started` emit and the existing `run_builder_bridge` call,
  decode the answer only when the PREVIOUS cycle asked for a diff:

    diff_response = None
    if diff_mode and repair_ctx is not None and repair_ctx.get("repair_mode") == "diff":
        diff_response, decode_reason = parse_diff_repair_response(
            output.structured_patch_text or ""
        )
        if diff_response is None:
            _emit(data_dir, job.id, "diff_repair_not_used", {
                "cycle": cycle, "reason": decode_reason,
            })

  Pass `diff_response=diff_response` to the existing `run_builder_bridge` call
  and change nothing else about that call.

  Then, immediately AFTER `loop_result.final_result = bridge_result` and
  BEFORE the existing `if bridge_result.stage in ("parse_failed",
  "apply_failed"):` check, handle the fallback:

    if bridge_result.stage == "diff_fallback":
        _emit(data_dir, job.id, "repair_round_fell_back_to_full_file", {
            "cycle": cycle,
            "reason": bridge_result.diff_fallback_reason,
        })
        if cycle < max_cycles:
            repair_ctx = build_repair_context(
                job.id,
                {"metadata": {"exit_code": 1, "passed": False, "cycle": cycle}},
                load_run_events(data_dir, job.id),
            )
            repair_ctx["repair_mode"] = "full_file"
            repair_ctx["full_file_reason"] = bridge_result.diff_fallback_reason
            loop_result.repair_contexts.append(repair_ctx)
        continue

  Write a one-line WHY comment above that block: a discarded diff attempt is
  not a dead end and not an applied patch, so the round continues on the
  full-file path with the reason recorded, and Remedy deliberately does not
  retry the SAME answer in full-file mode — the answer was diff-shaped, so the
  next prompt has to ask for a full file.

  Imports: add `apply_diff_repair`, `diff_repair_response_to_patch` and
  `parse_diff_repair_response` from their existing modules. Put them where
  the R16 `diff_repair` import already sits if that does not create a cycle;
  if it does, use a function-local import and say so in the handback. Do not
  change any existing import.

  Change NOTHING else: not the cycle bounds, not the repeated-patch detection,
  not `_attach_diff_repair_hunks`, and nothing in `diff_repair.py`,
  `diff_repair_response.py`, `diff_repair_apply.py`, `repair_context.py` or
  `source_apply.py`.

Change — C5, tests/orchestration/test_builder_repair_loop.py:
  Add THREE tests to the existing `TestRepairLoopDiffMode` class or a new class
  beside it. Do not modify the nine tests already in the file. Reuse the
  `_write_diff_repo` / `_make_diff_output` scaffolding already there.

  1. `test_a_diff_shaped_answer_lands_through_the_diff_channel`
     Cycle 1 applies the wrong fix through the normal channel and its tests
     fail, so cycle 2's repair context carries `repair_mode == "diff"`. Have
     cycle 2's `build_fn` return a BuilderOutput whose `structured_patch_text`
     is the diff-repair wrapper — a JSON object with `format` `unified_diff`,
     `version` 1, a `diff` that fixes calc.py, and `files` naming calc.py.
     Assert the loop SUCCEEDS, that calc.py on disk contains the fixed body,
     and that a `diff_repair_applied` event exists whose metadata has
     `mode == "diff"` and `applied is True`.
  2. `test_a_conflicting_diff_is_discarded_whole_and_the_round_falls_back`
     Same shape, but cycle 2's diff has context that does NOT match the file
     (change one context line so the strict applier rejects it). Assert:
     calc.py is BYTE-IDENTICAL to its pre-attempt content (read it before the
     loop and compare bytes — this is the feature's "zero partial application"
     acceptance line); a `diff_repair_applied` event with
     `mode == "full_fallback"` and a `fallback_reason` that is non-empty; a
     `repair_round_fell_back_to_full_file` event; and that the LAST repair
     context has `repair_mode == "full_file"` with a non-empty
     `full_file_reason`. Both attempts must be visible in the events — assert
     that too.
  3. `test_a_non_diff_answer_after_a_diff_prompt_is_reported_not_crashed`
     Cycle 2 returns an ordinary full-file answer even though the prompt asked
     for a diff. Assert a `diff_repair_not_used` event exists with a non-empty
     `reason`, and that the round still proceeds through the normal channel
     (no exception, and the loop reaches a terminal state).

  Read events with `packages.orchestration.timeline.load_run_events`.

Constraints:
  - SPLIT round. You are the worker; you make every commit. AGENTS.md is the
    highest authority: self-review loop before every commit, plan.md current,
    clean tree, push after each commit.
  - Never work on main, never force-push, never merge. No PR this round.
  - Destructive checks run ONLY inside a disposable `git worktree`, removed
    before the handback. `git status --porcelain` in the primary checkout is
    empty at every commit and at the handback. NOTE: `cd` may not take effect
    in some shells here — use absolute paths and verify with `pwd` before any
    mutation, and re-check `git status --porcelain` in the primary checkout
    immediately after.
  - Do NOT write a `Done:` paragraph of your own in `.agent/live_review.md`
    (planner_reviewer_prompt.md §4.4). If you land a fix this block did not
    order, mark it `Landed: R-XXXX — <one line>` instead.
  - Apply TEXT-A and TEXT-B BYTE FOR BYTE. If a text violates a rule, do not
    repair it — apply it and declare the deviation.
  - If any gate is red, or the block contradicts the code you find, stop at
    that point, commit what is clean, and say so in the handback. Do not widen
    scope to route around it. In particular: if adding the diff-channel
    imports at module level creates an import cycle, STOP, use a function-local
    import, and report it.

Done when — every command run for real, exit code recorded, no value guessed:
  a. TRANSPORT: `sha256sum .agent/authored/f111-r17-1.md .agent/last_block.md`
     -> both digests identical, `cmp` exits 0. State the digest, the byte count
     and `wc -l`, which must be under 400.
  b. `.agent/live_review.md`: `grep -c '^Done:'` -> 11 (unchanged, no finding
     resolved this round); `grep -c '^- R-0'` -> 42 (unchanged);
     `grep -c '^### R16 — PASS'` -> 1; `grep -c '^Landed:'` -> prints 0.
  c. `grep -c 'diff_repair_fell_back' packages/orchestration/builder_bridge.py`
     -> 2 (the STOP_REASONS entry and the one assignment).
     `grep -c 'diff_repair_applied' …/builder_bridge.py` -> 1.
     `grep -c 'diff_response' …/builder_bridge.py` -> report the real number.
  d. VALUE PROBE, the diff channel lands: print the `diff_repair_applied`
     event's `mode` and `applied`, and the post-loop content of calc.py.
     Paste the exact printed values.
  e. VALUE PROBE, the conflict path: print the `diff_repair_applied` `mode` and
     `fallback_reason`, and whether calc.py's bytes are unchanged (True/False).
     Paste the exact printed values.
  f. `python3 -m pytest tests/orchestration/test_builder_repair_loop.py -q`
     -> 12 passed (was 9).
  g. `python3 -m pytest tests/orchestration/test_diff_repair.py
     tests/orchestration/test_diff_repair_response.py
     tests/orchestration/test_diff_repair_apply.py -q` -> 71 passed, unmoved.
  h. IMPORT FALLOUT: `python3 -m pytest tests/ui_server/test_pipeline_contract.py
     tests/orchestration/test_builder_visibility.py
     tests/orchestration/test_stop_reasons.py
     tests/orchestration/test_repair_loop_hardened.py
     tests/orchestration/test_small_repo_fixtures.py
     tests/orchestration/test_self_healing_cycles.py
     tests/orchestration/test_builder_bridge_smoke.py
     tests/orchestration/test_event_replay.py
     tests/orchestration/test_builder_bridge.py -q` -> was 137 passed, 1
     skipped. Report the real numbers; any drop is a finding, report it.
  i. CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` -> 42 passed.
  j. MUTATION PROBE, in a disposable worktree only: change the fallback branch
     so it sets `result.apply_success = True` and does NOT return — i.e. make a
     rejected diff look applied — and report WHICH tests fail and how many.
     Report the real result whatever it is; if nothing fails, say so, because
     that would mean the conflict path is unpinned and is a finding, not your
     fault. Remove the worktree and show `git worktree list`.
  k. `git status --porcelain` -> empty. `git diff --name-only c0ed5dd1..HEAD`
     -> exactly the seven scoped paths. Per-commit insertions from
     `git log --numstat`, each under 500.
     `git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD`
     -> 0 and 0 after the final push.

Handback: completion report + rewrite .agent/handoff.md (item-status table for
C1-C6, changed-files table, the eleven gate results a-k with their real values,
open-findings count, next expected action). Repeat the Fortschritt line from
TEXT-B verbatim. Do not write your own insertion count for C6 inside C6.

──────────────────────── TEXT-A — append to .agent/live_review.md ───────────

### R16 — PASS (2026-08-13)
Reviewed by the main session over d457219a..c0ed5dd1. Every gate was re-run by
the reviewer on this machine; nothing was read off the handback. Transport:
`.agent/authored/f111-r16-1.md` and `.agent/last_block.md` are byte-identical
under `cmp`, 18501 bytes, 316 lines, sha256
c361c291408ccbc09c051ccedc08859de0111c70c3a43189670cccd5945a880a, and no line
carries trailing whitespace. `.agent/plan.md` was compared against the TEXT-D
slice extracted from the committed authored file and is identical at 42 lines,
under the 50-line cap. Each authored text occurs exactly once in
`.agent/live_review.md`. Markers counted: eleven resolution paragraphs, 42
registered findings, one R15 gate heading, zero unreviewed-fix markers. Scope:
exactly the seven ordered paths. Per-commit insertions 316/287/82/70/142/102,
each under 500. `git status --porcelain` empty, one worktree, and 0 ahead and
0 behind the remote.

Tests re-run by the reviewer: 9 for the repair loop (was 6), 71 for the three
diff-repair files — unmoved — and 42 for the golden-path canary. The new
module-level `diff_repair` import was checked for fallout across the nine test
files that import `builder_bridge`: 137 passed, 1 skipped, no cycle. The
helper resolves to exactly two hits, the def at line 269 and the single call
site at line 412.

The reviewer ran an INDEPENDENT value probe the block did not order, on a
margin the tests never assert: driving the loop with `diff_margin_lines=1` over
a patch naming line 3 only returns `repair_mode` `diff` with `start_line` 2 and
`end_line` 4, and the carried text is post-apply SOURCE, not diff text. So the
margin argument is genuinely plumbed and not merely defaulted. The emitted
metadata was read directly and carries `cycle`, `mode`, `hunk_count`,
`total_chars` and `omitted` — counts only, no hunk text, exactly as the block's
deliberate absence claims.

A second reviewer mutation, also unordered, ran inside a disposable git
worktree that was removed before this verdict: flipping the `diff_mode` default
from True to False fails two of the three new tests. The feature file's
"Config: repair.diff_mode (default on)" is therefore pinned by the suite rather
than only asserted in prose. The worker's own ordered mutation is confirmed as
reported — neutralising the helper fails five tests, three of them pre-existing
ones that now traverse the default-on path, and the diff-mode-off test stays
green, which is the correct signature.

The declared handoff overage is upheld: 105 lines with the DECISION D15
stated-cause line naming the mandated content, no section dropped. The ordered
pre-C4 key-set check was performed and reported with its real result (32 hits,
none pinning an exact key set), which is the shape §4.8 asks for.

DECISION F111 D8 (2026-08-13, reviewer, authored for R17) — the apply-side diff
channel attaches INSIDE `run_builder_bridge`, as a branch in Stage 1 and Stage
3 only, and not as a second pipeline in the loop. The loop decodes the answer
and passes a `DiffRepairResponse` in; the bridge converts it with
`diff_repair_response_to_patch` into the same `StructuredPatch` shape Stage 1
already produces, so the approval gate, the intent creation, the test stage and
DECISION F111 D3's range source all keep exactly one implementation. Only the
applicator call differs. Alternatives considered and rejected: routing the diff
through `apply_structured_patch` after conversion, which would bypass
`apply_diff_repair`'s fence precheck and its named fallback reasons; and
running a parallel apply-and-test path in the loop, which would duplicate the
approval gate and the test stage. Reverse this decision by deleting the
`diff_response` argument and moving the branch into the loop.

DECISION F111 D9 (2026-08-13, reviewer, authored for R17) — "token actuals" are
recorded as PAYLOAD CHARACTER COUNTS in v1, never as token numbers. This
repository has no tokenizer: a search of `packages/` for a token-counting
function returns nothing, so any field named `tokens` would carry a fabricated
number, which is a block condition under §4.5. `select_repair_hunks` already
returns `total_chars`, and the R18 comparison test records
`diff_payload_chars` against `full_file_payload_chars`. The names say chars
because the values are chars. Alternative considered and rejected for v1:
adding a tokenizer dependency, which would put a new third-party contract into
a wiring slice. Reverse this decision by wiring a real tokenizer and renaming
the fields in the same commit — never renaming them alone.

──────────────────── TEXT-B — full replacement of .agent/plan.md ────────────

# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged, no PR by design. Last reviewed SHA: c0ed5dd1 (R16 PASS).
Next free finding ID: R-0318. Open findings: 31 — 42 registered minus
11 resolved. None is High.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
R17 is T003's apply half. `run_builder_bridge` takes a decoded
`DiffRepairResponse` and routes it through `apply_diff_repair`
instead of `apply_structured_patch`, keeping Stage 1's conversion,
the approval gate and the test stage on one implementation
(DECISION F111 D8). A conflict returns stage `diff_fallback`, the
loop records the reason and puts the next cycle back on the
full-file path. R16's prompt half is complete and gated.

## Next Steps
1. R18 — the measurement: record payload character counts per repair
   round and add the fixture comparison test that shows the diff path
   costs a fraction of the full-file path (DECISION F111 D9 — chars,
   never fabricated token numbers). That is the feature's DONE line.
2. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids
  (R-0286): the integration gate compares base against branch.
- `builder_bridge.py` now imports four diff-repair symbols at module
  level; an import cycle would surface as collection errors across
  the nine test files that import it, so that fallout check is a
  standing gate, not a one-off.
- All-or-nothing rests entirely on source_apply's durable snapshot;
  `apply_diff_repair` adds no rollback of its own, and R-0316's fix
  means a failed rollback is now reported rather than hidden.

Fortschritt: ~86 % (T001 ✅ · T002 ✅ · T003 Prompt-Hälfte ✅ · T003
Apply-Hälfte in dieser Runde · Messung offen) — Schätzung
